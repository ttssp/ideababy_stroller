"""
DraftGCWorker — T008
结论: APScheduler AsyncIOScheduler 定时清理超时 draft（每 5 分钟，30 分钟失效）
细节:
  - 5min cron 触发，cutoff = now() - 30min
  - 调用 DecisionDraftRepository.gc_expired(cutoff)
  - 不依赖 LLM，纯 DB 操作
  - start() / shutdown() 供 lifespan 或测试调用
"""

from __future__ import annotations

import logging
from datetime import UTC, datetime, timedelta
from typing import Any

from apscheduler.schedulers.asyncio import AsyncIOScheduler

logger = logging.getLogger(__name__)

# draft 超时时间（分钟）
_DRAFT_EXPIRY_MINUTES: int = 30

# GC 检查间隔（分钟）
_GC_INTERVAL_MINUTES: int = 5


class DraftGCWorker:
    """Draft GC 定时任务，清理超时未 commit 的 draft。

    结论: APScheduler AsyncIOScheduler，每 5 分钟执行一次 GC。
    """

    def __init__(self, draft_repo: Any) -> None:
        """
        参数:
          draft_repo: 需要有 .gc_expired(cutoff_at: datetime) -> int 方法（duck typing）
        """
        self._draft_repo = draft_repo
        self._scheduler: AsyncIOScheduler | None = None

    def start(self) -> None:
        """启动 GC scheduler（应在 app lifespan 内调用）。"""
        if self._scheduler is not None and self._scheduler.running:
            return
        self._scheduler = AsyncIOScheduler()
        self._scheduler.add_job(
            self._gc_job,
            trigger="interval",
            minutes=_GC_INTERVAL_MINUTES,
            id="draft_gc",
            name="Draft GC Worker",
            replace_existing=True,
        )
        self._scheduler.start()
        logger.info(
            "DraftGCWorker 已启动 (每 %d 分钟检查,%d 分钟过期)",
            _GC_INTERVAL_MINUTES,
            _DRAFT_EXPIRY_MINUTES,
        )

    def shutdown(self, wait: bool = False) -> None:
        """停止 GC scheduler（应在 app shutdown 时调用）。"""
        if self._scheduler is not None and self._scheduler.running:
            self._scheduler.shutdown(wait=wait)
            logger.info("DraftGCWorker 已停止")

    async def _gc_job(self) -> None:
        """GC 任务主体：清理 30 分钟前的 draft。

        结论: cutoff = now() - 30min，调用 repo.gc_expired。
        """
        cutoff = datetime.now(tz=UTC) - timedelta(minutes=_DRAFT_EXPIRY_MINUTES)
        try:
            count = await self._draft_repo.gc_expired(cutoff)
            if count > 0:
                logger.info("GC 清理了 %d 条超时 draft (cutoff=%s)", count, cutoff.isoformat())
        except Exception:
            logger.exception("DraftGCWorker gc_job 执行异常")
