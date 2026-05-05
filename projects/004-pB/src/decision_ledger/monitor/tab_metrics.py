"""
tab_metrics.py — T020 (F2-T020 H10 强化)
结论: tab 打开计数中间件 + ratio 计算 (OP-6 mitigation)
细节:
  - TabMetricsMiddleware: FastAPI BaseHTTPMiddleware, GET 请求 → BackgroundTask 写 tab_open_log
  - TabMetricsRepository: record_open + count_opens_since
  - calculate_tab_ratio: tab_opens_14d / committed_decisions_14d (None if div-by-zero)
  - middleware 写入通过 BackgroundTask 异步, 不阻塞响应 (TECH-5 < 30s commit 要求)

F2-T020 H10 强化:
  - path 白名单: 仅记录 _COUNTED_PATH_PREFIXES 命中的页面 GET (decisions 相关页);
    避免攻击者请求 /<random> 海量 URL 把 tab_open_log 撑爆
  - user_agent 截断到 _MAX_UA_LEN=256 字节, 防超大 UA 头打爆磁盘
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
# F2-T020 H10: user_agent 截断 (256 字节, UTF-8 安全截断 → 用 char 数 256 近似)
_MAX_UA_LEN = 256


class TabMetricsRepository:
    """tab_open_log CRUD。

    结论: 提供 record_open (写) 和 count_opens_since (读)。
    """

    def __init__(self, pool: AsyncConnectionPool) -> None:
        self._pool = pool

    async def record_open(self, path: str, user_agent: str | None = None) -> None:
        """结论: 写入一条 tab_open_log 记录 (写路径)。

        F2-T020 H10: user_agent 长度 > _MAX_UA_LEN 时截断, 防 UA 攻击撑爆磁盘。
        """
        truncated_ua: str | None = None
        if user_agent is not None:
            truncated_ua = user_agent[:_MAX_UA_LEN]
        async with self._pool.write_connection() as conn:
            await conn.execute(
                "INSERT INTO tab_open_log (id, path, user_agent, opened_at) VALUES (?, ?, ?, ?)",
                (str(uuid.uuid4()), path, truncated_ua, datetime.now(tz=UTC).isoformat()),
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
    """FastAPI BaseHTTPMiddleware — GET 请求写入 tab_open_log (BackgroundTask)。

    结论: 仅记录命中白名单的 GET 请求, 不影响响应时间 (BackgroundTask 异步)。
    细节:
      - F2-T020 H10: 改为白名单制 — 只记录 _COUNTED_PATH_PREFIXES 中的页面访问;
        避免攻击者请求 /<random> 海量 URL 把 tab_open_log 撑爆 +
        防止健康检查/调试 endpoint 污染 tab_ratio
      - BackgroundTask 写入: 响应返回后执行, 不影响 < 30s commit SLA (TECH-5)
    """

    # F2-T020 H10: 白名单 = OP-6 关心的"用户真实页面打开"
    # 决策列表/详情/草稿/月度复盘等页面命中即记 1 次 tab open
    _COUNTED_PATH_PREFIXES = (
        "/",                    # 首页
        "/decisions",           # 决策列表 / 草稿 / 详情
        "/conflicts",           # 冲突报告
        "/notes",               # 笔记
        "/monthly",             # 月度 review
        "/learning",            # 学习卡片
    )
    # 显式排除子路径 (即使前缀命中也不记)
    _EXCLUDE_PREFIXES = ("/_partials/", "/static/", "/favicon", "/api/")

    def __init__(self, app: Any, pool: AsyncConnectionPool) -> None:
        super().__init__(app)
        self._tab_repo = TabMetricsRepository(pool)

    @classmethod
    def _should_count(cls, path: str) -> bool:
        """F2-T020 H10: 仅白名单前缀且未命中 exclude 时才计数。"""
        if any(path.startswith(pfx) for pfx in cls._EXCLUDE_PREFIXES):
            return False
        # "/" 单独处理: 严格等于才命中, 避免 "/anything" 也吞掉
        if path == "/":
            return True
        return any(
            path == pfx or path.startswith(pfx + "/") or path.startswith(pfx + "?")
            for pfx in cls._COUNTED_PATH_PREFIXES
            if pfx != "/"
        )

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        """结论: 先响应, 再异步写入 (BackgroundTask pattern)。"""
        response = await call_next(request)

        if request.method == "GET" and self._should_count(str(request.url.path)):
            path = str(request.url.path)
            user_agent = request.headers.get("user-agent")
            background = BackgroundTasks()
            background.add_task(self._tab_repo.record_open, path=path, user_agent=user_agent)
            response.background = background

        return response
