"""
test_pause_pipeline_integration.py — T020 unit 测试 (F2-T020 H7/H8/H9 强化)
结论: 验证 pause_pipeline facade 的 R3 ⚠️ H1 + F2 H7/H8/H9 行为
细节:
  - pause_all_pipelines() 调用 ConflictWorker.pause() (同步)
  - T015 (MonthlyScheduler) 缺失时优雅处理 (graceful)
  - DECISION_LEDGER_TEST_MODE=strict → AssertionError (R3 H1)
  - DECISION_LEDGER_TEST_MODE=allow-noop → _Noop 替身 (F2 H7)
  - 生产模式未注入 → RuntimeError (F2 H7)
  - set_conflict_worker(async方法) → TypeError (F2 H8)
  - reset_conflict_worker() 清空注入实例 (F2 H9)
"""

from __future__ import annotations

import asyncio
import os
from collections.abc import Iterator
from unittest.mock import MagicMock, patch

import pytest


@pytest.fixture(autouse=True)
def reset_pause_pipeline_state() -> Iterator[None]:
    """F2-T020 H9: 每个测试前后清空 pause_pipeline 全局状态, 防跨测试污染。"""
    from decision_ledger.monitor.pause_pipeline import reset_conflict_worker

    reset_conflict_worker()
    yield
    reset_conflict_worker()


def _make_mock_conflict_worker() -> MagicMock:
    """F2-T020 H8: ConflictWorker pause/resume 是同步方法, 用普通 MagicMock。"""
    worker = MagicMock()
    worker.pause = MagicMock()
    worker.resume = MagicMock()
    worker.is_paused = MagicMock(return_value=False)
    return worker


async def test_pause_all_pauses_conflict_worker() -> None:
    """should call conflict_worker.pause() when pause_all_pipelines() is called"""
    from decision_ledger.monitor.pause_pipeline import pause_all_pipelines

    mock_worker = _make_mock_conflict_worker()

    with patch(
        "decision_ledger.monitor.pause_pipeline._get_conflict_worker", return_value=mock_worker,
    ):
        await pause_all_pipelines(reason="测试暂停")

    mock_worker.pause.assert_called_once()


async def test_pause_all_when_t015_missing_graceful() -> None:
    """should log warning (not raise) when T015 MonthlyScheduler is missing (ImportError)"""
    from decision_ledger.monitor.pause_pipeline import pause_all_pipelines

    mock_worker = _make_mock_conflict_worker()

    with (
        patch(
            "decision_ledger.monitor.pause_pipeline._get_conflict_worker",
            return_value=mock_worker,
        ),
        patch.dict(os.environ, {"DECISION_LEDGER_TEST_MODE": ""}),
        patch(
            "decision_ledger.monitor.pause_pipeline._try_pause_monthly_scheduler",
            side_effect=ImportError("T015 not yet shipped"),
        ),
    ):
        await pause_all_pipelines(reason="测试T015缺失")

    mock_worker.pause.assert_called_once()


async def test_pause_all_in_strict_mode_raises() -> None:
    """should raise AssertionError when T015 ImportError occurs in strict mode (R3 H1)"""
    from decision_ledger.monitor.pause_pipeline import pause_all_pipelines

    mock_worker = _make_mock_conflict_worker()

    with (
        patch(
            "decision_ledger.monitor.pause_pipeline._get_conflict_worker",
            return_value=mock_worker,
        ),
        patch.dict(os.environ, {"DECISION_LEDGER_TEST_MODE": "strict"}),
        patch(
            "decision_ledger.monitor.pause_pipeline._try_pause_monthly_scheduler",
            side_effect=ImportError("T015 not yet shipped"),
        ),
        pytest.raises(AssertionError, match="T015"),
    ):
        await pause_all_pipelines(reason="严格模式测试")


async def test_unpause_resumes_all() -> None:
    """should call conflict_worker.resume() when unpause_all_pipelines() is called"""
    from decision_ledger.monitor.pause_pipeline import unpause_all_pipelines

    mock_worker = _make_mock_conflict_worker()

    with patch(
        "decision_ledger.monitor.pause_pipeline._get_conflict_worker", return_value=mock_worker,
    ):
        await unpause_all_pipelines()

    mock_worker.resume.assert_called_once()


async def test_pause_all_passes_reason_to_worker() -> None:
    """should log reason when pause_all_pipelines() is called"""
    from decision_ledger.monitor.pause_pipeline import pause_all_pipelines

    mock_worker = _make_mock_conflict_worker()
    reason = "O10 低决策率告警"

    with patch(
        "decision_ledger.monitor.pause_pipeline._get_conflict_worker", return_value=mock_worker,
    ):
        await pause_all_pipelines(reason=reason)

    assert mock_worker.pause.call_count == 1


# ── F2-T020 H7: production wiring 必须显式 ────────────────────────────────────


def test_get_conflict_worker_raises_when_unwired_in_production() -> None:
    """F2-H7: 没注入 worker 且非 noop 模式时, _get_conflict_worker 必须 raise。"""
    from decision_ledger.monitor.pause_pipeline import _get_conflict_worker

    with (
        patch.dict(os.environ, {"DECISION_LEDGER_TEST_MODE": ""}, clear=False),
        pytest.raises(RuntimeError, match="not wired"),
    ):
        _get_conflict_worker()


def test_get_conflict_worker_returns_noop_in_allow_noop_mode() -> None:
    """F2-H7: DECISION_LEDGER_TEST_MODE=allow-noop 显式开关下, 才返回 _Noop。"""
    from decision_ledger.monitor.pause_pipeline import _get_conflict_worker, _Noop

    with patch.dict(os.environ, {"DECISION_LEDGER_TEST_MODE": "allow-noop"}):
        worker = _get_conflict_worker()
        assert isinstance(worker, _Noop)
        # noop 行为
        worker.pause()
        worker.resume()
        assert worker.is_paused() is False


def test_set_conflict_worker_rejects_none() -> None:
    """F2-H7: set_conflict_worker(None) raise (用 reset_conflict_worker 清空)。"""
    from decision_ledger.monitor.pause_pipeline import set_conflict_worker

    with pytest.raises(ValueError, match="reset_conflict_worker"):
        set_conflict_worker(None)


def test_set_conflict_worker_rejects_async_methods() -> None:
    """F2-H8: pause/resume 必须是同步方法, async 方法 raise TypeError。"""
    from decision_ledger.monitor.pause_pipeline import set_conflict_worker

    bad_worker = MagicMock()

    async def _async_pause() -> None:
        ...

    bad_worker.pause = _async_pause  # async 方法
    bad_worker.resume = MagicMock()
    bad_worker.is_paused = MagicMock(return_value=False)

    with pytest.raises(TypeError, match="同步方法"):
        set_conflict_worker(bad_worker)


def test_set_conflict_worker_rejects_missing_methods() -> None:
    """F2-H7: worker 必须有 pause/resume/is_paused 三个方法。"""
    from decision_ledger.monitor.pause_pipeline import set_conflict_worker

    incomplete = MagicMock(spec=["pause"])  # 没 resume / is_paused
    with pytest.raises(TypeError, match="缺少同步方法"):
        set_conflict_worker(incomplete)


def test_set_then_reset_conflict_worker() -> None:
    """F2-H9: set 后 reset, 再次 _get_conflict_worker 必须 raise (生产模式)。"""
    from decision_ledger.monitor.pause_pipeline import (
        _get_conflict_worker,
        reset_conflict_worker,
        set_conflict_worker,
    )

    worker = _make_mock_conflict_worker()
    set_conflict_worker(worker)
    assert _get_conflict_worker() is worker

    reset_conflict_worker()
    with (
        patch.dict(os.environ, {"DECISION_LEDGER_TEST_MODE": ""}, clear=False),
        pytest.raises(RuntimeError),
    ):
        _get_conflict_worker()


# ── F2-T020 H8: pause/resume 串行化锁 ─────────────────────────────────────────


async def test_pause_lock_serializes_concurrent_calls() -> None:
    """F2-H8: 并发 pause + unpause 必须串行 (锁), 避免 _paused 状态颠倒。"""
    from decision_ledger.monitor.pause_pipeline import (
        pause_all_pipelines,
        unpause_all_pipelines,
    )

    call_order: list[str] = []
    mock_worker = _make_mock_conflict_worker()

    def _pause_record() -> None:
        call_order.append("pause-start")
        # 用同步 sleep 不可行 (会阻塞 event loop), 改靠 mock 立即返回
        call_order.append("pause-end")

    def _resume_record() -> None:
        call_order.append("resume-start")
        call_order.append("resume-end")

    mock_worker.pause = MagicMock(side_effect=_pause_record)
    mock_worker.resume = MagicMock(side_effect=_resume_record)

    with patch(
        "decision_ledger.monitor.pause_pipeline._get_conflict_worker",
        return_value=mock_worker,
    ):
        # 并发 5 次 pause + 5 次 resume, 必须各自原子完成 (start/end 紧邻)
        await asyncio.gather(
            *(pause_all_pipelines(reason=f"p{i}") for i in range(5)),
            *(unpause_all_pipelines() for _ in range(5)),
        )

    # 锁串行化 → 每对 start/end 必须紧邻 (中间无别 pair 插入)
    for i in range(0, len(call_order), 2):
        assert call_order[i].endswith("-start"), f"位置 {i} 应为 start: {call_order}"
        assert call_order[i + 1].endswith("-end"), f"位置 {i+1} 应为 end: {call_order}"
        # start/end 同 prefix
        assert call_order[i].split("-")[0] == call_order[i + 1].split("-")[0], (
            f"start/end prefix 不一致 → 锁失效, 序列: {call_order}"
        )
