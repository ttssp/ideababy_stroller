"""
AdvisorRepository — T003
结论: 咨询师周报 CRUD，支持 upsert_weekly / parse_failure 记录
细节:
  - upsert_weekly: INSERT OR REPLACE（按 week_id + source_id 唯一索引）
  - latest_for_week: 最新周报查询（读路径）
  - list_for_ticker: 返回包含该 ticker 的周报（JSON 字段搜索，读路径）
  - record_parse_failure: 写入解析失败记录（写路径）
"""

from __future__ import annotations

import json
from datetime import datetime
from typing import Any

from decision_ledger.domain.advisor import AdvisorWeeklyReport, ParseFailure
from decision_ledger.repository.base import AsyncConnectionPool


class AdvisorRepository:
    """咨询师周报 Repository。"""

    def __init__(self, pool: AsyncConnectionPool) -> None:
        self._pool = pool

    async def upsert_weekly(self, report: AdvisorWeeklyReport) -> None:
        """Upsert 周报记录（按 week_id + source_id 幂等，写路径）。

        结论: 使用 INSERT OR REPLACE 实现 upsert，same week same source 覆盖。
        """
        async with self._pool.write_connection() as conn:
            await conn.execute(
                """
                INSERT OR REPLACE INTO advisor_reports (
                    advisor_id, source_id, week_id, raw_text, structured_json, ingested_at
                ) VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    report.advisor_id,
                    report.source_id,
                    report.week_id,
                    report.raw_text,
                    json.dumps(report.structured_json, ensure_ascii=False),
                    report.parsed_at.isoformat(),
                ),
            )
            await conn.commit()

    async def latest_for_week(self, week_id: str) -> AdvisorWeeklyReport | None:
        """查询指定 week_id 的最新周报（读路径）。"""
        async with self._pool.connection() as conn:
            cursor = await conn.execute(
                """
                SELECT * FROM advisor_reports
                WHERE week_id = ?
                ORDER BY ingested_at DESC
                LIMIT 1
                """,
                (week_id,),
            )
            row = await cursor.fetchone()
            if row is None:
                return None
            return self._row_to_report(dict(row))

    async def list_for_ticker(self, ticker: str) -> list[AdvisorWeeklyReport]:
        """返回所有 structured_json 包含该 ticker 的周报（JSON 搜索，读路径）。

        结论: SQLite JSON 函数 json_extract 用于简单 key 存在性检查。
        细节: structured_json 格式为 {ticker: {direction, confidence, ...}}。
        """
        async with self._pool.connection() as conn:
            cursor = await conn.execute(
                """
                SELECT * FROM advisor_reports
                WHERE json_extract(structured_json, ?) IS NOT NULL
                ORDER BY ingested_at DESC
                """,
                (f"$.{ticker}",),
            )
            rows = await cursor.fetchall()
            return [self._row_to_report(dict(row)) for row in rows]

    async def record_parse_failure(self, failure: ParseFailure) -> None:
        """写入 PDF 解析失败记录（写路径）。

        结论: 失败记录存入 advisor_reports 的兄弟表（v0.1 用 alerts 表，type=parse_failure）。
        细节: v0.1 用 alerts 表 body 字段存储失败信息（架构 §5 parse_failures 方案）。
        """
        async with self._pool.write_connection() as conn:
            await conn.execute(
                """
                INSERT INTO alerts (
                    alert_id, alert_type, severity, body, created_at
                ) VALUES (?, ?, ?, ?, ?)
                """,
                (
                    failure.failure_id,
                    "parse_failure",
                    "warning",
                    json.dumps(
                        {
                            "pdf_path": failure.pdf_path,
                            "error_message": failure.error_message,
                            "advisor_id": failure.advisor_id,
                        },
                        ensure_ascii=False,
                    ),
                    failure.failed_at.isoformat(),
                ),
            )
            await conn.commit()

    # ── 私有辅助 ──────────────────────────────────────────────────────────────

    @staticmethod
    def _row_to_report(row: dict[str, Any]) -> AdvisorWeeklyReport:
        """将 DB row dict 构造为 AdvisorWeeklyReport 域对象。"""
        return AdvisorWeeklyReport(
            advisor_id=str(row["advisor_id"]),
            source_id=str(row["source_id"]),
            week_id=str(row["week_id"]),
            raw_text=str(row["raw_text"]),
            structured_json=json.loads(str(row["structured_json"])),
            parsed_at=datetime.fromisoformat(str(row["ingested_at"])),
        )
