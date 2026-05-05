"""
risk_dashboard.py — T020
结论: 7 行风险快照聚合 SQL，缺失数据展示 "—"
细节:
  - OP-1 p95 wall-clock: GET /decisions/new → POST commit（含 draft LLM 等待，PRD §S1 原口径）
  - OP-2 累计工时: weekly_maintenance_log（T014 未 ship → "—"）
  - OP-4 周维护 4 周平均: weekly_maintenance_log（T014 未 ship → "—"）
  - TECH-2 LLM 月成本: llm_usage 表
  - TECH-3 PDF 解析失败率: parse_failures / advisor_reports
  - O10 连续低决策周数: decisions WHERE status='committed'
  - BUS-1 上次备份距今: placeholder（v0.1 手动备份，真实检测 TBD）

  阈值颜色:
    - green: 指标达标
    - yellow: 接近边界
    - red: 超出或严重不足
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta

from decision_ledger.repository.base import AsyncConnectionPool

logger = logging.getLogger(__name__)

_PLACEHOLDER = "—"

# OP-1 p95 阈值（秒）
_OP1_GREEN_THRESHOLD_S = 25.0   # < 25s green
_OP1_YELLOW_THRESHOLD_S = 30.0  # < 30s yellow; >= 30s red (C11)

# TECH-2 LLM 月成本阈值（USD）
_TECH2_GREEN_THRESHOLD = 20.0   # < $20 green
_TECH2_YELLOW_THRESHOLD = 40.0  # < $40 yellow; >= $40 red

# TECH-3 PDF 解析失败率阈值
_TECH3_GREEN_THRESHOLD = 0.05   # < 5% green
_TECH3_YELLOW_THRESHOLD = 0.15  # < 15% yellow; >= 15% red

# O10 连续低决策周数阈值
_O10_YELLOW_WEEKS = 1           # >= 1 周 yellow
_O10_RED_WEEKS = 2              # >= 2 周 red


@dataclass
class RiskRow:
    """风险快照单行数据。

    结论: label + value + color_class 三元组，对应 dashboard 表格列。
    """

    label: str
    value: str          # 展示值（缺失时 "—"）
    color_class: str    # "green" | "yellow" | "red" | "gray"


class RiskDashboardRepository:
    """风险快照 7 行聚合查询。

    结论: 提供 get_snapshot() → list[RiskRow]，供模板渲染。
    """

    def __init__(self, pool: AsyncConnectionPool) -> None:
        self._pool = pool

    async def get_snapshot(self) -> list[RiskRow]:
        """结论: 返回 7 行风险快照，缺失数据用 "—"。"""
        rows: list[RiskRow] = []

        rows.append(await self._op1_row())
        rows.append(await self._op2_row())
        rows.append(await self._op4_row())
        rows.append(await self._tech2_row())
        rows.append(await self._tech3_row())
        rows.append(await self._o10_row())
        rows.append(self._bus1_row())

        return rows

    async def _op1_row(self) -> RiskRow:
        """OP-1: GET /decisions/new → POST commit p95 wall-clock（含 draft LLM 等待）。

        结论: 从 request_log 查 p95，覆盖完整路径（PRD §S1 原口径）。
        """
        label = "OP-1 录入 p95 (s)"
        try:
            async with self._pool.connection() as conn:
                # 结论: duration_ms 记录 GET→POST commit 全程，包含 draft LLM 等待
                # 仅统计最近 30 天数据
                cutoff = (datetime.now(tz=UTC) - timedelta(days=30)).isoformat()
                cursor = await conn.execute(
                    """
                    SELECT duration_ms FROM request_log
                    WHERE path = '/decisions/new' AND status_code = 200
                      AND ts >= ?
                    ORDER BY duration_ms
                    """,
                    (cutoff,),
                )
                rows = await cursor.fetchall()

            if not rows:
                return RiskRow(label=label, value=_PLACEHOLDER, color_class="gray")

            durations_ms = [r[0] for r in rows if r[0] is not None]
            if not durations_ms:
                return RiskRow(label=label, value=_PLACEHOLDER, color_class="gray")

            # p95 计算
            p95_idx = max(0, int(len(durations_ms) * 0.95) - 1)
            p95_s = durations_ms[p95_idx] / 1000.0
            value = f"{p95_s:.1f}s"

            if p95_s < _OP1_GREEN_THRESHOLD_S:
                color = "green"
            elif p95_s < _OP1_YELLOW_THRESHOLD_S:
                color = "yellow"
            else:
                color = "red"

            return RiskRow(label=label, value=value, color_class=color)
        except Exception:
            logger.exception("OP-1 row query failed")
            return RiskRow(label=label, value=_PLACEHOLDER, color_class="gray")

    async def _op2_row(self) -> RiskRow:
        """OP-2 累计工时（T014 weekly_maintenance_log；T014 未 ship → placeholder）。"""
        label = "OP-2 累计工时"
        try:
            async with self._pool.connection() as conn:
                cursor = await conn.execute(
                    "SELECT SUM(hours) FROM weekly_maintenance_log"
                )
                row = await cursor.fetchone()
            if row is None or row[0] is None:
                return RiskRow(label=label, value=_PLACEHOLDER, color_class="gray")
            return RiskRow(label=label, value=f"{row[0]:.1f}h", color_class="green")
        except Exception:
            # weekly_maintenance_log 表不存在（T014 未 ship）→ placeholder
            return RiskRow(label=label, value=_PLACEHOLDER, color_class="gray")

    async def _op4_row(self) -> RiskRow:
        """OP-4 周维护 4 周平均（T014；未 ship → placeholder）。"""
        label = "OP-4 周维护 4w 平均"
        try:
            cutoff = (datetime.now(tz=UTC) - timedelta(weeks=4)).isoformat()
            async with self._pool.connection() as conn:
                cursor = await conn.execute(
                    "SELECT AVG(hours) FROM weekly_maintenance_log WHERE week_start >= ?",
                    (cutoff,),
                )
                row = await cursor.fetchone()
            if row is None or row[0] is None:
                return RiskRow(label=label, value=_PLACEHOLDER, color_class="gray")
            return RiskRow(label=label, value=f"{row[0]:.1f}h/w", color_class="green")
        except Exception:
            return RiskRow(label=label, value=_PLACEHOLDER, color_class="gray")

    async def _tech2_row(self) -> RiskRow:
        """TECH-2 LLM 月成本（llm_usage 表）。"""
        label = "TECH-2 LLM 月成本"
        try:
            cutoff = (datetime.now(tz=UTC) - timedelta(days=30)).isoformat()
            async with self._pool.connection() as conn:
                cursor = await conn.execute(
                    "SELECT SUM(cost_usd) FROM llm_usage WHERE called_at >= ?",
                    (cutoff,),
                )
                row = await cursor.fetchone()

            if row is None or row[0] is None:
                return RiskRow(label=label, value="$0.00", color_class="green")

            cost = float(row[0])
            value = f"${cost:.2f}"
            if cost < _TECH2_GREEN_THRESHOLD:
                color = "green"
            elif cost < _TECH2_YELLOW_THRESHOLD:
                color = "yellow"
            else:
                color = "red"
            return RiskRow(label=label, value=value, color_class=color)
        except Exception:
            logger.exception("TECH-2 row query failed")
            return RiskRow(label=label, value=_PLACEHOLDER, color_class="gray")

    async def _tech3_row(self) -> RiskRow:
        """TECH-3 PDF 解析失败率（parse_failures / advisor_reports）。"""
        label = "TECH-3 PDF 解析失败率"
        try:
            async with self._pool.connection() as conn:
                cursor_total = await conn.execute("SELECT COUNT(*) FROM advisor_reports")
                row_total = await cursor_total.fetchone()
                total = int(row_total[0]) if row_total else 0

                if total == 0:
                    return RiskRow(label=label, value="0.0%", color_class="green")

                cursor_fail = await conn.execute(
                    "SELECT COUNT(*) FROM advisor_reports WHERE parse_failed = 1"
                )
                row_fail = await cursor_fail.fetchone()
                failed = int(row_fail[0]) if row_fail else 0

            rate = failed / total
            value = f"{rate * 100:.1f}%"
            if rate < _TECH3_GREEN_THRESHOLD:
                color = "green"
            elif rate < _TECH3_YELLOW_THRESHOLD:
                color = "yellow"
            else:
                color = "red"
            return RiskRow(label=label, value=value, color_class=color)
        except Exception:
            logger.exception("TECH-3 row query failed")
            return RiskRow(label=label, value=_PLACEHOLDER, color_class="gray")

    async def _o10_row(self) -> RiskRow:
        """O10 连续低决策周数（decisions WHERE status='committed'）。"""
        label = "O10 低决策周数"
        try:
            # 结论: 检查最近 8 周，计算连续低决策周数（每周 < 1 条 committed）
            low_weeks = 0
            now = datetime.now(tz=UTC)
            async with self._pool.connection() as conn:
                for week_offset in range(8):
                    week_end = now - timedelta(weeks=week_offset)
                    week_start = week_end - timedelta(weeks=1)
                    cursor = await conn.execute(
                        """
                        SELECT COUNT(*) FROM decisions
                        WHERE status = 'committed'
                          AND pre_commit_at >= ? AND pre_commit_at < ?
                        """,
                        (week_start.isoformat(), week_end.isoformat()),
                    )
                    row = await cursor.fetchone()
                    count = int(row[0]) if row else 0
                    if count < 1:
                        low_weeks += 1
                    else:
                        break  # 连续计数中断

            value = f"{low_weeks}w"
            if low_weeks < _O10_YELLOW_WEEKS:
                color = "green"
            elif low_weeks < _O10_RED_WEEKS:
                color = "yellow"
            else:
                color = "red"
            return RiskRow(label=label, value=value, color_class=color)
        except Exception:
            logger.exception("O10 row query failed")
            return RiskRow(label=label, value=_PLACEHOLDER, color_class="gray")

    def _bus1_row(self) -> RiskRow:
        """BUS-1 上次备份距今（v0.1 placeholder，真实检测 TBD）。"""
        # 结论: v0.1 手动备份，无自动检测；dashboard 展示 placeholder
        return RiskRow(label="BUS-1 上次备份距今", value=_PLACEHOLDER, color_class="gray")
