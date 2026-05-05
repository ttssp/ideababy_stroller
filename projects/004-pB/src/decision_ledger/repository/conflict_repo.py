"""
ConflictRepository — T003
结论: 冲突报告 CRUD，含 signals_json 序列化
细节:
  - insert: 插入 ConflictReport（写路径，signals 序列化为 JSON）
  - get: 按 report_id 查询（读路径）
  - list_recent: 最近 N 条（读路径）
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from typing import Any

from decision_ledger.domain.conflict_report import ConflictReport
from decision_ledger.domain.strategy_signal import Direction, StrategySignal
from decision_ledger.repository.base import AsyncConnectionPool


class ConflictRepository:
    """ConflictReport Repository。"""

    def __init__(self, pool: AsyncConnectionPool) -> None:
        self._pool = pool

    async def insert(self, report_id: str, report: ConflictReport) -> None:
        """插入 ConflictReport（写路径）。

        结论: signals 序列化为 JSON 列表（含完整 StrategySignal 数据）。
        """
        signals_json = json.dumps(
            [s.model_dump() for s in report.signals], ensure_ascii=False
        )
        async with self._pool.write_connection() as conn:
            await conn.execute(
                """
                INSERT INTO conflict_reports (
                    report_id, divergence_root_cause, has_divergence,
                    rendered_order_seed, signals_json, created_at
                ) VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    report_id,
                    report.divergence_root_cause,
                    int(report.has_divergence),
                    report.rendered_order_seed,
                    signals_json,
                    datetime.now(tz=UTC).isoformat(),
                ),
            )
            await conn.commit()

    async def get(self, report_id: str) -> ConflictReport | None:
        """按 report_id 查询（读路径）。"""
        async with self._pool.connection() as conn:
            cursor = await conn.execute(
                "SELECT * FROM conflict_reports WHERE report_id = ?",
                (report_id,),
            )
            row = await cursor.fetchone()
            if row is None:
                return None
            return self._row_to_conflict_report(dict(row))

    async def list_recent(self, limit: int = 10) -> list[ConflictReport]:
        """最近 N 条（读路径）。"""
        async with self._pool.connection() as conn:
            cursor = await conn.execute(
                "SELECT * FROM conflict_reports ORDER BY created_at DESC LIMIT ?",
                (limit,),
            )
            rows = await cursor.fetchall()
            return [self._row_to_conflict_report(dict(row)) for row in rows]

    # ── 私有辅助 ──────────────────────────────────────────────────────────────

    @staticmethod
    def _row_to_conflict_report(row: dict[str, Any]) -> ConflictReport:
        """将 DB row dict 构造为 ConflictReport 域对象。"""
        signals_data = json.loads(str(row["signals_json"]))
        signals = [
            StrategySignal(
                source_id=s["source_id"],
                ticker=s["ticker"],
                direction=Direction(s["direction"]),
                confidence=s["confidence"],
                rationale_plain=s["rationale_plain"],
                inputs_used=s["inputs_used"],
            )
            for s in signals_data
        ]
        return ConflictReport(
            signals=signals,
            divergence_root_cause=str(row["divergence_root_cause"]),
            has_divergence=bool(row["has_divergence"]),
            rendered_order_seed=int(str(row["rendered_order_seed"])),
        )
