"""
WeeklyReviewService — T014
结论: 周度 review 聚合服务，生成 5 个 section 数据 + LLM 摘要 (异步 fallback)
细节:
  - generate(week_id): 聚合本周数据 → dict for template
    * week_id 格式: "YYYY-WW" (ISO 周号, e.g. "2026-W17")
    * SQL 聚合: decisions 按 action 分类 (C13 hold/wait 不动专区, R11)
    * LLM 摘要: 异步调用，失败 fallback 到 None 不阻塞 (OP-3 mitigation)
  - log_maintenance_hours(week_id, hours): 写 weekly_maintenance_log (OP-4 mitigation)
  - get_rolling_avg_hours(current_week_id, weeks=4): 最近 N 周工时滚动平均
  - OP-4 阈值 3h: over_threshold = (current_hours >= 3.0)
  - R11: hold+wait 占比独立 section，不与 buy/sell 合并
"""

from __future__ import annotations

import logging
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any

from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from decision_ledger.llm.client import LLMClient
    from decision_ledger.repository.base import AsyncConnectionPool


class WeeklySummaryOutput(BaseModel):
    """LLM 摘要输出 schema (T014)。"""

    summary: str = Field(..., max_length=400, description="≤ 200 字周报摘要")

logger = logging.getLogger(__name__)

# OP-4 维护工时阈值 (h/周)
_MAINTENANCE_THRESHOLD_HOURS = 3.0


def _week_id_to_date_range(week_id: str) -> tuple[str, str]:
    """将 YYYY-WW 格式转为 ISO 8601 日期范围 (周一 00:00 到下周一 00:00)。

    结论: 使用 datetime.strptime + "%G-W%V" 格式解析 ISO 周号。
    细节:
      - "%G-W%V" 对应 ISO 8601 周日历 (周一为起始日)
      - 返回格式 "YYYY-MM-DDT00:00:00+00:00" 用于 SQL BETWEEN 查询
    """
    # 例: "2026-W17" → 解析为该周的周一
    monday = datetime.strptime(f"{week_id}-1", "%G-W%V-%u").replace(tzinfo=UTC)
    sunday_end = monday.replace(
        hour=23,
        minute=59,
        second=59,
    )
    # 取到周日 23:59:59
    from datetime import timedelta

    sunday_end = monday + timedelta(days=6, hours=23, minutes=59, seconds=59)

    return monday.isoformat(), sunday_end.isoformat()


class WeeklyReviewService:
    """周度 review 聚合服务。

    结论: 独立服务，通过 pool 直接执行 SQL 聚合，不依赖 Repository 层。
    细节:
      - llm_client 可为 None (测试时), 为 None 时跳过 LLM 摘要
      - 所有 LLM 调用包在 try/except 内，失败 fallback 到 None
    """

    def __init__(
        self,
        pool: AsyncConnectionPool,
        llm_client: LLMClient | None,
    ) -> None:
        self._pool = pool
        self._llm_client = llm_client

    async def generate(self, week_id: str) -> dict[str, Any]:
        """生成周度 review 数据字典（供模板渲染）。

        结论: 聚合 5 个 section 数据 + LLM 摘要。
        参数:
          week_id: "YYYY-WW" 格式 (e.g. "2026-W17")
        返回: dict 含以下 key:
          - week_id: str
          - total_decisions: int
          - action_breakdown: dict[str, int]  (buy/sell/hold/wait → count)
          - hold_wait_count: int               (R11: 不动专区独立)
          - inactive_ratio: float              (hold+wait / total)
          - llm_cost_usd: float               (本周 LLM 总成本)
          - llm_summary: str | None           (LLM 摘要, 失败时 None)
          - maintenance: dict                  (current_hours, rolling_avg, over_threshold)
        """
        start_iso, end_iso = _week_id_to_date_range(week_id)

        # ── 1. 决策聚合 ──────────────────────────────────────────────────────
        action_breakdown = await self._count_decisions_by_action(start_iso, end_iso)
        total_decisions = sum(action_breakdown.values())
        hold_wait_count = action_breakdown.get("hold", 0) + action_breakdown.get("wait", 0)
        inactive_ratio = (hold_wait_count / total_decisions) if total_decisions > 0 else 0.0

        # ── 2. LLM 成本聚合 ────────────────────────────────────────────────
        llm_cost_usd = await self._sum_llm_cost(start_iso, end_iso)

        # ── 3. 维护工时 ───────────────────────────────────────────────────
        maintenance = await self._get_maintenance_summary(week_id)

        # ── 4. LLM 摘要 (异步, fallback) ─────────────────────────────────
        llm_summary = await self._generate_llm_summary_safe(
            week_id=week_id,
            total_decisions=total_decisions,
            action_breakdown=action_breakdown,
            inactive_ratio=inactive_ratio,
        )

        return {
            "week_id": week_id,
            "total_decisions": total_decisions,
            "action_breakdown": action_breakdown,
            "hold_wait_count": hold_wait_count,
            "inactive_ratio": inactive_ratio,
            "llm_cost_usd": llm_cost_usd,
            "llm_summary": llm_summary,
            "maintenance": maintenance,
        }

    async def log_maintenance_hours(self, week_id: str, hours: float) -> None:
        """记录本周维护工时（UPSERT: 同一 week_id 覆盖写）。

        结论: 写入 weekly_maintenance_log，支持覆盖更新。
        参数:
          week_id: "YYYY-WW" 格式
          hours: 本周实际维护工时 (≥ 0.0)
        """
        signed_at = datetime.now(tz=UTC).isoformat()
        async with self._pool.write_connection() as conn:
            await conn.execute(
                """
                INSERT INTO weekly_maintenance_log (week_id, hours, signed_at)
                VALUES (?, ?, ?)
                ON CONFLICT(week_id) DO UPDATE SET
                    hours = excluded.hours,
                    signed_at = excluded.signed_at
                """,
                (week_id, hours, signed_at),
            )
            await conn.commit()
        logger.info("维护工时已记录 | week_id=%s | hours=%.1f", week_id, hours)

    async def get_rolling_avg_hours(
        self, current_week_id: str, weeks: int = 4
    ) -> float:
        """计算最近 N 周维护工时滚动平均。

        结论: 按 week_id 字典序降序取最近 weeks 条记录，返回平均值。
        细节:
          - week_id "YYYY-WW" 字典序等同时间序（ISO 8601 周号保证此性质）
          - 若不足 weeks 条，用实际有记录的周数平均
        """
        async with self._pool.connection() as conn:
            cursor = await conn.execute(
                """
                SELECT AVG(hours) as avg_hours
                FROM (
                    SELECT hours FROM weekly_maintenance_log
                    WHERE week_id <= ?
                    ORDER BY week_id DESC
                    LIMIT ?
                )
                """,
                (current_week_id, weeks),
            )
            row = await cursor.fetchone()
            if row is None or row["avg_hours"] is None:
                return 0.0
            return float(row["avg_hours"])

    # ── 私有方法 ──────────────────────────────────────────────────────────────

    async def _count_decisions_by_action(
        self, start_iso: str, end_iso: str
    ) -> dict[str, int]:
        """按 action 统计本周 committed 决策数。"""
        async with self._pool.connection() as conn:
            cursor = await conn.execute(
                """
                SELECT action, COUNT(*) as cnt
                FROM decisions
                WHERE status = 'committed'
                  AND pre_commit_at >= ?
                  AND pre_commit_at <= ?
                GROUP BY action
                """,
                (start_iso, end_iso),
            )
            rows = await cursor.fetchall()
            return {row["action"]: int(row["cnt"]) for row in rows}

    async def _sum_llm_cost(self, start_iso: str, end_iso: str) -> float:
        """聚合本周 LLM 调用总成本 (USD)。"""
        async with self._pool.connection() as conn:
            cursor = await conn.execute(
                """
                SELECT COALESCE(SUM(cost_usd), 0.0) as total_cost
                FROM llm_usage
                WHERE created_at >= ?
                  AND created_at <= ?
                """,
                (start_iso, end_iso),
            )
            row = await cursor.fetchone()
            if row is None:
                return 0.0
            return float(row["total_cost"])

    async def _get_maintenance_summary(self, week_id: str) -> dict[str, Any]:
        """获取维护工时摘要 (当前工时 + 4 周滚动平均 + OP-4 阈值判断)。"""
        # 当周工时
        async with self._pool.connection() as conn:
            cursor = await conn.execute(
                "SELECT hours FROM weekly_maintenance_log WHERE week_id = ?",
                (week_id,),
            )
            row = await cursor.fetchone()
            current_hours = float(row["hours"]) if row is not None else 0.0

        rolling_avg = await self.get_rolling_avg_hours(current_week_id=week_id, weeks=4)
        over_threshold = current_hours >= _MAINTENANCE_THRESHOLD_HOURS

        return {
            "current_hours": current_hours,
            "rolling_avg": rolling_avg,
            "over_threshold": over_threshold,
            "threshold": _MAINTENANCE_THRESHOLD_HOURS,
        }

    async def _generate_llm_summary_safe(
        self,
        week_id: str,
        total_decisions: int,
        action_breakdown: dict[str, int],
        inactive_ratio: float,
    ) -> str | None:
        """异步生成 LLM 摘要，失败时 fallback 到 None（不阻塞）。

        结论: LLM 调用包在 try/except，确保 generate() 不因 LLM 失败而中断。
        细节:
          - llm_client 为 None 时直接返回 None (测试/无 API key 场景)
          - 任何 Exception → log warning + return None
        """
        if self._llm_client is None:
            return None

        try:
            prompt = _build_summary_prompt(
                week_id=week_id,
                total_decisions=total_decisions,
                action_breakdown=action_breakdown,
                inactive_ratio=inactive_ratio,
            )
            result = await self._llm_client.call(
                prompt,
                template_version="weekly_review_v1",
                cache_key_extras={"week_id": week_id},
                schema=WeeklySummaryOutput,
            )
            return result.summary
        except Exception as exc:
            logger.warning("LLM 摘要生成失败，fallback 到无摘要 | error=%s", exc)
            return None


def _build_summary_prompt(
    week_id: str,
    total_decisions: int,
    action_breakdown: dict[str, int],
    inactive_ratio: float,
) -> str:
    """构建 LLM 摘要请求 prompt。

    结论: 简洁数据注入，LLM 输出 ≤ 200 字中文摘要。
    """
    breakdown_str = " / ".join(f"{k}:{v}" for k, v in sorted(action_breakdown.items()))
    return (
        f"周报数据 ({week_id}):\n"
        f"- 总决策: {total_decisions} 条\n"
        f"- 按动作: {breakdown_str}\n"
        f"- 不动占比 (hold+wait): {inactive_ratio:.1%}\n\n"
        "请生成 ≤200 字的中文周度 calibration 摘要，"
        "重点: 不动/等待是好事 (R6 反诱导高频交易)，"
        "强调纪律性而非短期活跃度。"
    )
