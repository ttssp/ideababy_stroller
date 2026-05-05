"""
rate_limiter.py — T017 R4 节制规则
结论: 7 天滚动窗口 rate limiter，key=(chat_id, push_type)，写入 SQLite telegram_pushes 表
细节:
  - try_push(): 检查 7 天内 push 数是否超限，未超则写入记录并返回 True，超限返回 False
  - 限额: weekly ≤ 1 次/7天，event ≤ 5 次/7天 (架构 §3.5 R4 红线)
  - 写入使用 pool.writer_lock 保证串行（单一 writer 不变量）
  - reference_time 参数供测试注入模拟时间（可选，None 则用 UTC now）
"""

from __future__ import annotations

import logging
from datetime import UTC, datetime, timedelta
from typing import Literal

from decision_ledger.repository.base import AsyncConnectionPool

logger = logging.getLogger(__name__)

# ── 配额常量 (R4 红线) ────────────────────────────────────────────────────────
WEEKLY_LIMIT = 1   # 7 天滚动窗口内最多 1 次 weekly push
EVENT_LIMIT = 5    # 7 天滚动窗口内最多 5 次 event push
WINDOW_DAYS = 7    # 滚动窗口天数

PushType = Literal["weekly", "event"]


class RateLimiter:
    """Telegram push rate limiter — 7 天滚动窗口。

    结论: 每次 try_push 先查 telegram_pushes 表 7 天内的 push 数，
         未超限则写入新记录并返回 True，超限返回 False。

    架构约束:
      - 写入在 writer_lock 下执行（单一 writer 不变量）
      - 不 cache 内存状态，全从 DB 读（确保多进程安全，虽实际单进程）
    """

    def __init__(self, pool: AsyncConnectionPool | None) -> None:
        """
        参数:
            pool: AsyncConnectionPool 实例；None 表示无 DB 连接（测试占位）
        """
        self._pool = pool

    async def try_push(
        self,
        chat_id: str,
        push_type: PushType,
        reference_time: datetime | None = None,
    ) -> bool:
        """尝试 push — 检查配额，未超限则记录并返回 True，超限返回 False。

        结论: 原子性检查+写入（在 writer_lock 下执行）。

        参数:
            chat_id: Telegram chat_id
            push_type: 'weekly' | 'event'
            reference_time: 参考时间，None 则用 UTC now（供测试注入）

        返回:
            True 若本次 push 被允许（并已写入 DB），False 若超限。
        """
        if self._pool is None:
            logger.warning("RateLimiter: pool 未初始化，跳过 rate limit 检查")
            return True

        now = reference_time or datetime.now(tz=UTC)
        window_start = now - timedelta(days=WINDOW_DAYS)
        limit = WEEKLY_LIMIT if push_type == "weekly" else EVENT_LIMIT

        async with self._pool.writer_lock:
            async with self._pool.connection() as conn:
                # 查询 7 天内该 chat_id + push_type 的 push 数
                cursor = await conn.execute(
                    """
                    SELECT COUNT(*) FROM telegram_pushes
                    WHERE chat_id = ?
                      AND push_type = ?
                      AND pushed_at >= ?
                    """,
                    (chat_id, push_type, window_start.isoformat()),
                )
                row = await cursor.fetchone()
                count = row[0] if row else 0

                if count >= limit:
                    logger.info(
                        "RateLimiter: 超限 chat_id=%s type=%s count=%d limit=%d",
                        chat_id,
                        push_type,
                        count,
                        limit,
                    )
                    return False

                # 写入本次 push 记录
                await conn.execute(
                    """
                    INSERT INTO telegram_pushes (chat_id, push_type, pushed_at)
                    VALUES (?, ?, ?)
                    """,
                    (chat_id, push_type, now.isoformat()),
                )
                await conn.commit()

        logger.info(
            "RateLimiter: 允许 chat_id=%s type=%s (window_count=%d/%d)",
            chat_id,
            push_type,
            count + 1,
            limit,
        )
        return True

    async def get_window_count(
        self,
        chat_id: str,
        push_type: PushType,
        reference_time: datetime | None = None,
    ) -> int:
        """查询指定 chat_id + push_type 在 7 天窗口内的 push 数（只读）。

        结论: 供监控/调试使用，不写入。
        """
        if self._pool is None:
            return 0

        now = reference_time or datetime.now(tz=UTC)
        window_start = now - timedelta(days=WINDOW_DAYS)

        async with self._pool.connection() as conn:
            cursor = await conn.execute(
                """
                SELECT COUNT(*) FROM telegram_pushes
                WHERE chat_id = ?
                  AND push_type = ?
                  AND pushed_at >= ?
                """,
                (chat_id, push_type, window_start.isoformat()),
            )
            row = await cursor.fetchone()
            return row[0] if row else 0
