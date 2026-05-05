"""
test_pause_pipeline_integration.py — T020 unit 测试 (F2-T020 H7/H8/H9 + followup A1)
结论: 验证 pause_pipeline facade 的 R3 ⚠️ H1 + F2 H7/H8/H9 + followup A1 行为
细节:
  - pause_all_pipelines() 调用 ConflictWorker.pause() (同步)
  - T015 (MonthlyScheduler) 缺失时优雅处理 (graceful)
  - DECISION_LEDGER_TEST_MODE=strict → AssertionError (R3 H1)
  - DECISION_LEDGER_TEST_MODE=allow-noop → _Noop 替身 (F2 H7)
  - 生产模式未注入 → _Noop + WARNING + counter 自增 (F2 H7 followup A1)
  - 仅 TEST_MODE=strict 维持 raise (F2 H7 followup A1, CI gate)
  - set_conflict_worker(async方法) → TypeError (F2 H8)
  - reset_conflict_worker() 清空注入实例 + 重置 counter (F2 H9 + followup A1)
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


def test_get_conflict_worker_returns_noop_in_production_when_unwired(
    caplog: pytest.LogCaptureFixture,
) -> None:
    """F2-H7 followup A1: production 默认未 wire 走 _Noop + WARNING + counter 自增。

    替代旧的"未注入必 raise"行为 — v0.1 plugin registry 死代码现实下, raise
    把 R8 panic stop 变成定时炸弹。改 noop + counter + 启动期 BANNER 让"未生效"
    显式可见。
    """
    from decision_ledger.monitor.pause_pipeline import (
        _get_conflict_worker,
        _Noop,
        pause_hook_noop_call_count,
    )

    caplog.set_level("WARNING", logger="decision_ledger.monitor.pause_pipeline")
    with patch.dict(os.environ, {"DECISION_LEDGER_TEST_MODE": ""}, clear=False):
        worker = _get_conflict_worker()

    assert isinstance(worker, _Noop)
    # counter 自增 (autouse fixture 已 reset 到 0)
    assert pause_hook_noop_call_count() == 1
    # WARNING 日志含可识别关键词
    assert any(
        "未 wire" in r.message or "not wired" in r.message.lower()
        for r in caplog.records
    ), f"应有 wiring WARNING, 实际 records: {[r.message for r in caplog.records]}"


def test_get_conflict_worker_strict_mode_still_raises() -> None:
    """F2-H7 followup A1: TEST_MODE=strict 维持 raise (CI gate 抓 wiring drift)。

    production 默认改 noop, 但 CI 必须能识别"代码改完忘了 wire"这种漂移。
    """
    from decision_ledger.monitor.pause_pipeline import _get_conflict_worker

    with (
        patch.dict(os.environ, {"DECISION_LEDGER_TEST_MODE": "strict"}, clear=False),
        pytest.raises(RuntimeError, match="strict"),
    ):
        _get_conflict_worker()


def test_get_conflict_worker_returns_noop_in_allow_noop_mode() -> None:
    """F2-H7: DECISION_LEDGER_TEST_MODE=allow-noop 显式开关下, 也返回 _Noop。"""
    from decision_ledger.monitor.pause_pipeline import _get_conflict_worker, _Noop

    with patch.dict(os.environ, {"DECISION_LEDGER_TEST_MODE": "allow-noop"}):
        worker = _get_conflict_worker()
        assert isinstance(worker, _Noop)
        # noop 行为
        worker.pause()
        worker.resume()
        assert worker.is_paused() is False


def test_get_conflict_worker_unknown_test_mode_falls_back_to_noop(
    caplog: pytest.LogCaptureFixture,
) -> None:
    """followup A1 (self-review N3): 未识别的 TEST_MODE 值走 noop + 警告, 不 raise。

    防止"打字错误"(如 'striict')让 production 静默 raise; 同时 logger.warning
    告知运维该值不被识别。
    """
    from decision_ledger.monitor.pause_pipeline import _get_conflict_worker, _Noop

    caplog.set_level("WARNING", logger="decision_ledger.monitor.pause_pipeline")
    with patch.dict(os.environ, {"DECISION_LEDGER_TEST_MODE": "striict"}, clear=False):
        worker = _get_conflict_worker()

    assert isinstance(worker, _Noop)
    # 应有"未识别"警告 + 走 noop 的警告 (两条)
    msgs = [r.message for r in caplog.records]
    assert any("未识别的" in m for m in msgs), (
        f"应有未识别 TEST_MODE 警告, 实际 records: {msgs}"
    )


def test_pause_hook_noop_counter_increments_per_call() -> None:
    """F2-H7 followup A1: 每次 _Noop 路径调用 counter +1, 给 smoke / 自检用。"""
    from decision_ledger.monitor.pause_pipeline import (
        _get_conflict_worker,
        pause_hook_noop_call_count,
    )

    with patch.dict(os.environ, {"DECISION_LEDGER_TEST_MODE": ""}, clear=False):
        for expected in (1, 2, 3, 4, 5):
            _get_conflict_worker()
            assert pause_hook_noop_call_count() == expected


def test_get_wiring_status_reflects_injection() -> None:
    """F2-H7 followup A1: get_wiring_status() 给启动期 BANNER 自检读 wiring 状态。"""
    from decision_ledger.monitor.pause_pipeline import (
        get_wiring_status,
        reset_conflict_worker,
        set_conflict_worker,
    )

    # 未注入: noop
    assert get_wiring_status()["conflict_worker"] == "noop"

    # 注入后: wired
    worker = _make_mock_conflict_worker()
    set_conflict_worker(worker)
    assert get_wiring_status()["conflict_worker"] == "wired"

    # reset 后: 又 noop
    reset_conflict_worker()
    assert get_wiring_status()["conflict_worker"] == "noop"


def test_reset_conflict_worker_resets_counter() -> None:
    """F2-H7 followup A1 + H9: reset 同时清 wiring + counter, 让测试断言独立。"""
    from decision_ledger.monitor.pause_pipeline import (
        _get_conflict_worker,
        pause_hook_noop_call_count,
        reset_conflict_worker,
    )

    with patch.dict(os.environ, {"DECISION_LEDGER_TEST_MODE": ""}, clear=False):
        _get_conflict_worker()
        _get_conflict_worker()
        assert pause_hook_noop_call_count() == 2

        reset_conflict_worker()
        assert pause_hook_noop_call_count() == 0


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
    """F2-H9 + followup A1: set 后 reset, 再次 _get_conflict_worker 退化为 _Noop。

    (旧版本断言 raise; followup A1 后 production 默认是 noop 不 raise。
    对应 strict 模式仍 raise 的回归覆盖见 test_get_conflict_worker_strict_mode_still_raises。)
    """
    from decision_ledger.monitor.pause_pipeline import (
        _get_conflict_worker,
        _Noop,
        reset_conflict_worker,
        set_conflict_worker,
    )

    worker = _make_mock_conflict_worker()
    set_conflict_worker(worker)
    assert _get_conflict_worker() is worker

    reset_conflict_worker()
    with patch.dict(os.environ, {"DECISION_LEDGER_TEST_MODE": ""}, clear=False):
        result = _get_conflict_worker()
    assert isinstance(result, _Noop)


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
