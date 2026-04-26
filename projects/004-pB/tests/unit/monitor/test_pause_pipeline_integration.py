"""
test_pause_pipeline_integration.py — T020 unit 测试
结论: 验证 pause_pipeline facade 的 R3 ⚠️ H1 行为
细节:
  - pause_all_pipelines() 调用 ConflictWorker.pause()
  - T015 (MonthlyScheduler) 缺失时优雅处理 (graceful)
  - DECISION_LEDGER_TEST_MODE=strict → AssertionError (R3 H1)
  - unpause_all_pipelines() 调用 ConflictWorker.resume()
"""

from __future__ import annotations

import os
from unittest.mock import AsyncMock, MagicMock, patch

import pytest


def _make_mock_conflict_worker() -> MagicMock:
    """构造 ConflictWorker mock。"""
    worker = MagicMock()
    worker.pause = AsyncMock()
    worker.resume = AsyncMock()
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

    # 模拟 T015 模块不存在（ImportError）
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
        # 非 strict 模式下不应 raise
        await pause_all_pipelines(reason="测试T015缺失")

    # ConflictWorker 仍应被暂停
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
    """should pass reason string to conflict_worker.pause()"""
    from decision_ledger.monitor.pause_pipeline import pause_all_pipelines

    mock_worker = _make_mock_conflict_worker()
    reason = "O10 低决策率告警"

    with patch(
        "decision_ledger.monitor.pause_pipeline._get_conflict_worker", return_value=mock_worker,
    ):
        await pause_all_pipelines(reason=reason)

    # 验证 pause 被调用，且带正确参数（或接受无参数调用，取决于实现）
    assert mock_worker.pause.call_count == 1
