"""
Scheduler — T014
结论: 注册 weekly_review cron 到 plugin registry (周日 21:00 Asia/Taipei)
细节:
  - SCHEDULER_TIMEZONE: 时区常量，优先 Asia/Taipei，失败 fallback UTC
  - weekly_review_cron(): 异步任务函数，调用 WeeklyReviewService.generate()
  - register_scheduler_job() 在模块导入时副作用执行，main.py 无需修改
  - cron 表达式: 0 21 * * 0 → day_of_week=sun, hour=21, minute=0
  - week_id 由当前时间 Asia/Taipei 推导 (ISO 周号格式 YYYY-WW)
"""

from __future__ import annotations

import logging
from datetime import datetime

logger = logging.getLogger(__name__)

# ── 时区配置 ──────────────────────────────────────────────────────────────────
# 结论: 优先用 zoneinfo (Python 3.9+) 取 Asia/Taipei，失败 fallback 到 UTC。
# 细节: zoneinfo.ZoneInfoNotFoundError 在无 tzdata 的 Docker 镜像中可能发生。
try:
    from zoneinfo import ZoneInfo

    SCHEDULER_TIMEZONE = "Asia/Taipei"
    _tz = ZoneInfo(SCHEDULER_TIMEZONE)
except Exception:
    import datetime as _dt

    SCHEDULER_TIMEZONE = "UTC"
    _tz = _dt.UTC  # type: ignore[assignment]


def _current_week_id() -> str:
    """返回当前时间在 Asia/Taipei 时区的 ISO 周号字符串 (YYYY-WW)。

    结论: 使用 %G-W%V strftime 格式生成 ISO 8601 周号。
    """
    now = datetime.now(tz=_tz)
    return now.strftime("%G-W%V")


async def weekly_review_cron() -> None:
    """Cron 回调: 生成当周周报并写日志。

    结论: 调用 WeeklyReviewService.generate()，失败写 error log 不抛出。
    细节:
      - pool 和 llm_client 从 app state 取（通过 DI 注入或全局单例）
      - 本阶段实现为 placeholder，实际 DI 在 T015/T020 连接
      - 任何异常 catch 后 log，确保 scheduler 不崩溃
    """
    week_id = _current_week_id()
    logger.info("weekly_review_cron 触发 | week_id=%s", week_id)

    try:
        # 延迟 import 避免循环依赖，实际 pool/llm_client 由调用方注入
        from decision_ledger.services.weekly_review_service import WeeklyReviewService  # noqa: F401

        # 注意: 生产环境需通过 DI 注入 pool + llm_client
        # 当前 cron 作为占位实现; T015 会将 set_pool() 连接到此处
        logger.info("weekly_review_cron 完成 | week_id=%s (dry-run: pool 未连接)", week_id)
    except Exception as exc:
        logger.error("weekly_review_cron 失败 | week_id=%s | error=%s", week_id, exc)


# ── 注册到 plugin registry (模块导入副作用) ──────────────────────────────────
# 结论: 在模块顶层执行注册，main.py 只需 import 此模块即可完成注册。
# 细节: trigger_kwargs 按 APScheduler 3.x cron 参数命名。
from decision_ledger.plugin import register_scheduler_job  # noqa: E402

register_scheduler_job(
    weekly_review_cron,
    "cron",
    job_id="weekly_review",
    day_of_week="sun",
    hour=21,
    minute=0,
    timezone=SCHEDULER_TIMEZONE,
)
