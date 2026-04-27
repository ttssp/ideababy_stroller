"""
MonthlyScheduler — T015 (R2 H1 pause hook)
结论: 月度调度器，含 pause/resume/is_paused hook，注册 cron 每月最后一日 21:00
细节:
  - MonthlyScheduler 类暴露 pause/resume/is_paused/set_service/run_monthly_job
  - R2 H1: T020/T022 在 B-lite engage 时调 monthly_scheduler.pause()
  - _paused: bool — 实例级状态 (非类变量), 各实例独立
  - run_monthly_job(): 检查 _paused → 提前返回或调用 service.generate()
  - cron: 每月最后一日 21:00 Asia/Taipei (APScheduler 3.x: day=last)
  - 注册到 T014 plugin registry (register_scheduler_job)
  - 不修改 main.py / scheduler.py (T014 已有)
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Any

logger = logging.getLogger(__name__)

# ── 时区配置 (与 T014 scheduler.py 保持一致) ─────────────────────────────────
try:
    from zoneinfo import ZoneInfo

    SCHEDULER_TIMEZONE = "Asia/Taipei"
    _tz = ZoneInfo(SCHEDULER_TIMEZONE)
except Exception:
    import datetime as _dt

    SCHEDULER_TIMEZONE = "UTC"
    _tz = _dt.UTC  # type: ignore[assignment]


def _current_month_id() -> str:
    """返回当前时间在 Asia/Taipei 时区的月份字符串 (YYYY-MM)。

    结论: 使用 %Y-%m strftime 格式生成月份 ID。
    """
    now = datetime.now(tz=_tz)
    return now.strftime("%Y-%m")


class MonthlyScheduler:
    """月度调度器 — R2 H1 pause hook 版本。

    结论:
      - pause/resume/is_paused 三方法暴露 B-lite pause 接口 (R2 H1)
      - run_monthly_job: paused 时提前 return，不调用 service.generate
      - set_service: 注入 MonthlyReviewService 实例（DI 接口）
      - 各实例状态独立 (_paused 为实例变量)

    T020/T022 用法:
      monthly_scheduler.pause()   # B-lite engage 时暂停月度 review
      monthly_scheduler.resume()  # B-lite 解除时恢复
    """

    def __init__(self) -> None:
        # R2 H1: _paused 为实例变量（非类变量），各实例状态独立
        self._paused: bool = False
        self._service: Any | None = None  # MonthlyReviewService | None

    def pause(self) -> None:
        """暂停月度 review 调度 (R2 H1)。

        结论: 设置 _paused=True，run_monthly_job 将提前返回。
        """
        self._paused = True
        logger.info("MonthlyScheduler paused")

    def resume(self) -> None:
        """恢复月度 review 调度 (R2 H1)。

        结论: 清除 _paused 标志，run_monthly_job 恢复正常执行。
        """
        self._paused = False
        logger.info("MonthlyScheduler resumed")

    def is_paused(self) -> bool:
        """返回当前暂停状态 (R2 H1)。

        结论: 供 T020/T022 查询调度器是否处于 B-lite pause 状态。
        """
        return self._paused

    def set_service(self, service: Any) -> None:
        """注入 MonthlyReviewService 实例 (DI 接口，测试用)。

        结论: 允许测试/main.py 注入真实或 mock 服务。
        """
        self._service = service

    async def run_monthly_job(self) -> None:
        """Cron 回调: 执行月度 review 生成任务。

        结论: paused 时立刻 return 不执行; 否则调用 service.generate()。
        细节:
          - R2 H1: _paused check 是第一优先级，优先于 service 初始化检查
          - 任何异常 catch 后 log，确保 scheduler 不崩溃
        """
        # R2 H1: paused 时跳过 (必须是第一个检查)
        if self._paused:
            logger.info("MonthlyScheduler is paused, skipping this run")
            return

        month_id = _current_month_id()
        logger.info("monthly_review_cron 触发 | month_id=%s", month_id)

        if self._service is None:
            logger.warning("MonthlyReviewService 未注入, 跳过 generate | month_id=%s", month_id)
            return

        try:
            await self._service.generate(month_id=month_id)
            logger.info("monthly_review_cron 完成 | month_id=%s", month_id)
        except Exception as exc:
            logger.error("monthly_review_cron 失败 | month_id=%s | error=%s", month_id, exc)


# ── 全局单例 (供 T020/T022 通过 import 访问) ────────────────────────────────
# 结论: 单例模式，T020/T022 直接 from monthly_scheduler import monthly_scheduler
monthly_scheduler = MonthlyScheduler()


async def _monthly_review_cron_callback() -> None:
    """APScheduler cron 回调函数 (全局单例)。

    结论: 委托给全局 monthly_scheduler 实例执行，保持单点控制。
    """
    await monthly_scheduler.run_monthly_job()


# ── 注册到 plugin registry (模块导入副作用) ──────────────────────────────────
# 结论: 注册 cron 每月最后一日 21:00 Asia/Taipei
# 细节:
#   - APScheduler 3.x: day="last" 表示每月最后一天
#   - 不修改 main.py / T014 scheduler.py
from decision_ledger.plugin import register_scheduler_job  # noqa: E402

register_scheduler_job(
    _monthly_review_cron_callback,
    "cron",
    job_id="monthly_review",
    day="last",
    hour=21,
    minute=0,
    timezone=SCHEDULER_TIMEZONE,
)
