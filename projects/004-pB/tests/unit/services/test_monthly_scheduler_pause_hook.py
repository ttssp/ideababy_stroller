"""
MonthlyScheduler pause hook 单元测试 — T015
结论: 验证 pause/resume/is_paused 三方法 + paused 时 run_monthly_job 提前返回
细节:
  - test_pause_resume: pause → is_paused=True; resume → is_paused=False
  - test_run_monthly_job_skips_when_paused: paused 状态下 run_monthly_job 立刻返回,
    不调用 monthly_review_service.generate
  - test_run_monthly_job_calls_generate_when_not_paused: 未 paused 时调用 generate
  - test_pause_does_not_lose_data: pause 状态是内存 flag, 不影响外部数据
"""

from __future__ import annotations

from unittest.mock import AsyncMock, patch

import pytest


class TestMonthlySchedulerPauseHook:
    """MonthlyScheduler pause/resume hook 验证 (R2 H1)."""

    def test_pause_sets_is_paused_true_when_called(self) -> None:
        """should set is_paused=True when pause() is called."""
        from decision_ledger.services.monthly_scheduler import MonthlyScheduler

        scheduler = MonthlyScheduler()
        assert scheduler.is_paused() is False  # 初始未暂停

        scheduler.pause()
        assert scheduler.is_paused() is True

    def test_resume_clears_is_paused_when_called_after_pause(self) -> None:
        """should clear is_paused flag when resume() is called after pause()."""
        from decision_ledger.services.monthly_scheduler import MonthlyScheduler

        scheduler = MonthlyScheduler()
        scheduler.pause()
        assert scheduler.is_paused() is True

        scheduler.resume()
        assert scheduler.is_paused() is False

    def test_initial_state_is_not_paused(self) -> None:
        """should start with is_paused=False on new instance."""
        from decision_ledger.services.monthly_scheduler import MonthlyScheduler

        scheduler = MonthlyScheduler()
        assert scheduler.is_paused() is False

    def test_pause_is_idempotent_when_called_twice(self) -> None:
        """should remain paused when pause() is called twice."""
        from decision_ledger.services.monthly_scheduler import MonthlyScheduler

        scheduler = MonthlyScheduler()
        scheduler.pause()
        scheduler.pause()  # 再次调用不应出错
        assert scheduler.is_paused() is True

    def test_resume_is_idempotent_when_not_paused(self) -> None:
        """should remain unpaused when resume() is called on unpaused scheduler."""
        from decision_ledger.services.monthly_scheduler import MonthlyScheduler

        scheduler = MonthlyScheduler()
        scheduler.resume()  # 未暂停时 resume 不应出错
        assert scheduler.is_paused() is False


class TestMonthlySchedulerRunMonthlyJob:
    """run_monthly_job 在 paused/unpaused 状态下的行为验证。"""

    @pytest.mark.asyncio
    async def test_run_monthly_job_returns_early_when_paused(self) -> None:
        """should return early without calling generate when paused (R2 H1)."""
        from decision_ledger.services.monthly_scheduler import MonthlyScheduler

        mock_svc = AsyncMock()
        mock_svc.generate = AsyncMock()

        scheduler = MonthlyScheduler()
        scheduler.set_service(mock_svc)
        scheduler.pause()

        await scheduler.run_monthly_job()

        # paused 时 generate 不应被调用
        mock_svc.generate.assert_not_called()

    @pytest.mark.asyncio
    async def test_run_monthly_job_calls_generate_when_not_paused(self) -> None:
        """should call generate when scheduler is not paused."""
        from decision_ledger.services.monthly_scheduler import MonthlyScheduler

        mock_svc = AsyncMock()
        mock_svc.generate = AsyncMock(return_value={})

        scheduler = MonthlyScheduler()
        scheduler.set_service(mock_svc)
        # 不暂停

        await scheduler.run_monthly_job()

        # 未暂停时 generate 应被调用一次
        mock_svc.generate.assert_called_once()

    @pytest.mark.asyncio
    async def test_run_monthly_job_resumes_after_resume_called(self) -> None:
        """should call generate after resume() is called following pause()."""
        from decision_ledger.services.monthly_scheduler import MonthlyScheduler

        mock_svc = AsyncMock()
        mock_svc.generate = AsyncMock(return_value={})

        scheduler = MonthlyScheduler()
        scheduler.set_service(mock_svc)

        scheduler.pause()
        await scheduler.run_monthly_job()
        mock_svc.generate.assert_not_called()

        scheduler.resume()
        await scheduler.run_monthly_job()
        mock_svc.generate.assert_called_once()


class TestPauseDoesNotLoseData:
    """pause 状态不影响外部数据完整性 (R2 Glossary: B-lite 数据完整性)。"""

    def test_pause_does_not_affect_other_schedulers(self) -> None:
        """should not affect other MonthlyScheduler instances when one is paused."""
        from decision_ledger.services.monthly_scheduler import MonthlyScheduler

        scheduler_a = MonthlyScheduler()
        scheduler_b = MonthlyScheduler()

        scheduler_a.pause()

        # a paused, b should remain unpaused (各实例独立状态)
        assert scheduler_a.is_paused() is True
        assert scheduler_b.is_paused() is False

    def test_pause_hook_methods_are_callable(self) -> None:
        """should expose pause/resume/is_paused as callable methods (R2 H1)."""
        from decision_ledger.services.monthly_scheduler import MonthlyScheduler

        scheduler = MonthlyScheduler()

        # 三方法存在且可调用
        assert callable(scheduler.pause)
        assert callable(scheduler.resume)
        assert callable(scheduler.is_paused)
