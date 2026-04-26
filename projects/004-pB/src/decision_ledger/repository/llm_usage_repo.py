"""
LLMUsageRepository — T003
结论: LLM API 调用成本日志 CRUD
细节:
  - insert: 插入 LLMUsage 记录（写路径）
  - monthly_total_cost: 按月汇总成本（读路径）
  - cache_hit_rate: 按 service 统计缓存命中率（读路径）
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from decision_ledger.domain.llm_usage import LLMUsage
from decision_ledger.repository.base import AsyncConnectionPool


class LLMUsageRepository:
    """LLM 调用成本日志 Repository。"""

    def __init__(self, pool: AsyncConnectionPool) -> None:
        self._pool = pool

    async def insert(self, usage: LLMUsage) -> None:
        """插入 LLM 调用记录（写路径）。

        结论: 每次 API 调用后写入，用于 D21 cache 命中率 + R2 Q11 latency 监控。
        """
        async with self._pool.write_connection() as conn:
            await conn.execute(
                """
                INSERT INTO llm_usage (
                    call_id, service, model, prompt_template_version,
                    prompt_tokens, output_tokens, cost_usd, cache_hit, latency_ms, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    usage.call_id,
                    usage.service,
                    usage.model,
                    usage.prompt_template_version,
                    usage.prompt_tokens,
                    usage.output_tokens,
                    usage.cost_usd,
                    int(usage.cache_hit),
                    usage.latency_ms,
                    usage.created_at.isoformat(),
                ),
            )
            await conn.commit()

    async def monthly_total_cost(self, year: int, month: int) -> float:
        """按月汇总总成本 (USD)（读路径）。

        结论: SUM(cost_usd) WHERE created_at 在指定月份内。
        细节: 用 LIKE 匹配 ISO 格式日期的年月前缀（e.g. "2024-03%"）。
        """
        prefix = f"{year:04d}-{month:02d}%"
        async with self._pool.connection() as conn:
            cursor = await conn.execute(
                """
                SELECT COALESCE(SUM(cost_usd), 0.0) AS total_cost
                FROM llm_usage
                WHERE created_at LIKE ?
                """,
                (prefix,),
            )
            row = await cursor.fetchone()
            if row is None:
                return 0.0
            return float(row["total_cost"])

    async def cache_hit_rate(self, service: str | None = None) -> float:
        """统计 cache 命中率（读路径）。

        结论: cache_hit_rate = SUM(cache_hit) / COUNT(*) 按 service 过滤或全局。
        细节: D21 监控目标 ≥ 95% 命中率。
        """
        if service is not None:
            query = """
                SELECT
                    CAST(SUM(cache_hit) AS REAL) / NULLIF(COUNT(*), 0) AS hit_rate
                FROM llm_usage
                WHERE service = ?
            """
            params: tuple[Any, ...] = (service,)
        else:
            query = """
                SELECT
                    CAST(SUM(cache_hit) AS REAL) / NULLIF(COUNT(*), 0) AS hit_rate
                FROM llm_usage
            """
            params = ()

        async with self._pool.connection() as conn:
            cursor = await conn.execute(query, params)
            row = await cursor.fetchone()
            if row is None or row["hit_rate"] is None:
                return 0.0
            return float(row["hit_rate"])

    # ── 私有辅助 ──────────────────────────────────────────────────────────────

    @staticmethod
    def _row_to_usage(row: dict[str, Any]) -> LLMUsage:
        """将 DB row dict 构造为 LLMUsage 域对象。"""
        return LLMUsage(
            call_id=str(row["call_id"]),
            service=str(row["service"]),
            model=str(row["model"]),
            prompt_template_version=str(row["prompt_template_version"]),
            prompt_tokens=int(str(row["prompt_tokens"])),
            output_tokens=int(str(row["output_tokens"])),
            cost_usd=float(str(row["cost_usd"])),
            cache_hit=bool(row["cache_hit"]),
            latency_ms=int(str(row["latency_ms"])),
            created_at=datetime.fromisoformat(str(row["created_at"])),
        )
