"""
tab_metrics.py — T020
结论: tab 打开计数中间件 + ratio 计算 (OP-6 mitigation)
细节:
  - TabMetricsMiddleware: FastAPI BaseHTTPMiddleware，GET 请求 → BackgroundTask 写 tab_open_log
  - TabMetricsRepository: record_open + count_opens_since
  - calculate_tab_ratio: tab_opens_14d / committed_decisions_14d (None if div-by-zero)
  - middleware 写入通过 BackgroundTask 异步，不阻塞响应（TECH-5 < 30s commit 要求）
"""

from __future__ import annotations

import logging
import uuid
from datetime import UTC, datetime, timedelta
from typing import Any

from fastapi import Request, Response
from fastapi.background import BackgroundTasks
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from decision_ledger.repository.base import AsyncConnectionPool
from decision_ledger.repository.decision_repo import DecisionRepository

logger = logging.getLogger(__name__)

_LOOKBACK_DAYS = 14


class TabMetricsRepository:
    """tab_open_log CRUD。

    结论: 提供 record_open（写）和 count_opens_since（读）。
    """

    def __init__(self, pool: AsyncConnectionPool) -> None:
        self._pool = pool

    async def record_open(self, path: str, user_agent: str | None = None) -> None:
        """结论: 写入一条 tab_open_log 记录（写路径）。"""
        async with self._pool.write_connection() as conn:
            await conn.execute(
                "INSERT INTO tab_open_log (id, path, user_agent, opened_at) VALUES (?, ?, ?, ?)",
                (str(uuid.uuid4()), path, user_agent, datetime.now(tz=UTC).isoformat()),
            )
            await conn.commit()

    async def count_opens_since(self, days: int = 7) -> int:
        """结论: 统计最近 N 天内的 tab 打开次数（读路径）。"""
        cutoff = (datetime.now(tz=UTC) - timedelta(days=days)).isoformat()
        async with self._pool.connection() as conn:
            cursor = await conn.execute(
                "SELECT COUNT(*) FROM tab_open_log WHERE opened_at >= ?",
                (cutoff,),
            )
            row = await cursor.fetchone()
            return int(row[0]) if row else 0


async def calculate_tab_ratio(
    tab_repo: TabMetricsRepository,
    decision_repo: DecisionRepository,
    lookback_days: int = _LOOKBACK_DAYS,
) -> float | None:
    """结论: tab_opens / committed_decisions（14d），零除返回 None。

    细节:
      - tab_opens: count_opens_since(lookback_days)
      - committed_decisions: decision_repo.count_since(days=lookback_days)
      - None 表示"无法计算"（T015 月度 review 应展示 placeholder "—"）
    """
    tab_opens = await tab_repo.count_opens_since(days=lookback_days)
    committed = await decision_repo.count_since(days=lookback_days)

    if committed == 0:
        logger.warning("tab_ratio: 0 committed decisions in %d days, returning None", lookback_days)
        return None

    ratio = tab_opens / committed
    logger.info("tab_ratio: %d opens / %d decisions = %.2f", tab_opens, committed, ratio)
    return ratio


class TabMetricsMiddleware(BaseHTTPMiddleware):
    """FastAPI BaseHTTPMiddleware — GET 请求写入 tab_open_log（BackgroundTask）。

    结论: 仅记录 GET 请求，不影响响应时间（BackgroundTask 异步）。
    细节:
      - 排除 /_partials/* 和 /static/* 路由（非页面访问）
      - BackgroundTask 写入：响应返回后执行，不影响 < 30s commit SLA (TECH-5)
    """

    _EXCLUDE_PREFIXES = ("/_partials/", "/static/", "/favicon")

    def __init__(self, app: Any, pool: AsyncConnectionPool) -> None:
        super().__init__(app)
        self._tab_repo = TabMetricsRepository(pool)

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        """结论: 先响应，再异步写入（BackgroundTask pattern）。"""
        response = await call_next(request)

        # 仅记录 GET 请求（tab 打开 = 页面浏览）
        if request.method == "GET" and not any(
            str(request.url.path).startswith(pfx) for pfx in self._EXCLUDE_PREFIXES
        ):
            path = str(request.url.path)
            user_agent = request.headers.get("user-agent")
            background = BackgroundTasks()
            background.add_task(self._tab_repo.record_open, path=path, user_agent=user_agent)
            response.background = background

        return response
