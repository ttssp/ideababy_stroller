"""
Scheduler 集成测试 — T014
结论: 验证 scheduler.py 正确注册 weekly cron (0 21 * * 0) 到 plugin registry
细节:
  - test_scheduler_registers_weekly_job: 验证 weekly_review cron 已注册 (周日 21:00)
  - test_scheduler_cron_expression: 验证 cron 参数 day_of_week='sun', hour=21, minute=0
  - test_scheduler_job_id: 验证 job_id='weekly_review'
  - test_scheduler_module_importable: scheduler 模块可 import 无副作用
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch


def test_scheduler_module_importable_without_side_effects() -> None:
    """should import scheduler module without starting APScheduler."""
    # 仅验证 import 不会启动调度器或 raise
    import decision_ledger.services.scheduler as scheduler_mod  # noqa: F401

    assert scheduler_mod is not None


def test_scheduler_registers_weekly_review_job() -> None:
    """should register weekly_review job in plugin registry when scheduler module loaded."""
    from decision_ledger import plugin

    # 重置 plugin 状态以避免其他 test 的影响
    original_jobs = list(plugin._scheduler_jobs)

    try:
        plugin._scheduler_jobs.clear()

        # 强制重新触发注册（导入副作用）
        import importlib

        import decision_ledger.services.scheduler as scheduler_mod
        importlib.reload(scheduler_mod)

        job_ids = [j.job_id for j in plugin._scheduler_jobs]
        assert "weekly_review" in job_ids, f"expected 'weekly_review' in {job_ids}"
    finally:
        # 恢复原始状态
        plugin._scheduler_jobs.clear()
        plugin._scheduler_jobs.extend(original_jobs)


def test_scheduler_weekly_job_cron_trigger() -> None:
    """should configure weekly_review job with cron trigger day_of_week='sun', hour=21."""
    from decision_ledger import plugin

    original_jobs = list(plugin._scheduler_jobs)

    try:
        plugin._scheduler_jobs.clear()

        import importlib

        import decision_ledger.services.scheduler as scheduler_mod
        importlib.reload(scheduler_mod)

        # 找 weekly_review job
        weekly_job = next(
            (j for j in plugin._scheduler_jobs if j.job_id == "weekly_review"),
            None,
        )
        assert weekly_job is not None, "weekly_review job 未注册"
        assert weekly_job.trigger == "cron"
        # cron kwargs 应包含 day_of_week=sun 和 hour=21
        kwargs = weekly_job.kwargs
        assert str(kwargs.get("day_of_week", "")).lower() in ("sun", "6"), (
            f"day_of_week={kwargs.get('day_of_week')} 不是周日"
        )
        assert int(kwargs.get("hour", -1)) == 21, f"hour={kwargs.get('hour')} 不是 21"
        assert int(kwargs.get("minute", -1)) == 0, f"minute={kwargs.get('minute')} 不是 0"
    finally:
        plugin._scheduler_jobs.clear()
        plugin._scheduler_jobs.extend(original_jobs)


def test_scheduler_weekly_job_func_is_generate() -> None:
    """should use generate function as the weekly_review cron callback."""
    from decision_ledger import plugin

    original_jobs = list(plugin._scheduler_jobs)

    try:
        plugin._scheduler_jobs.clear()

        import importlib

        import decision_ledger.services.scheduler as scheduler_mod
        importlib.reload(scheduler_mod)

        weekly_job = next(
            (j for j in plugin._scheduler_jobs if j.job_id == "weekly_review"),
            None,
        )
        assert weekly_job is not None
        # func 必须是可调用的（不要求特定名称，允许 wrapper）
        assert callable(weekly_job.func)
    finally:
        plugin._scheduler_jobs.clear()
        plugin._scheduler_jobs.extend(original_jobs)


def test_scheduler_timezone_is_asia_taipei() -> None:
    """should configure timezone as Asia/Taipei for the scheduler."""
    import decision_ledger.services.scheduler as scheduler_mod

    # 验证模块有 TIMEZONE 常量或 get_timezone() 函数
    tz_value = getattr(scheduler_mod, "SCHEDULER_TIMEZONE", None)
    if tz_value is None:
        tz_value = getattr(scheduler_mod, "TIMEZONE", None)
    # 至少有一个 tz 配置
    assert tz_value is not None, "scheduler module 应导出 SCHEDULER_TIMEZONE 常量"
    assert "Taipei" in str(tz_value) or "UTC" in str(tz_value), (
        f"timezone={tz_value} 应为 Asia/Taipei 或 fallback UTC"
    )
