"""
AlertRepository — T003
结论: 告警 CRUD，支持 insert / latest_active / dismiss
细节:
  - insert: 插入 Alert（写路径，alert_type CHECK 约束由 DB 校验）
  - latest_active: 查询最近未 dismiss 的告警（读路径）
  - dismiss: 填入 dismissed_at（写路径）
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from decision_ledger.domain.alert import Alert, AlertSeverity, AlertType
from decision_ledger.repository.base import AsyncConnectionPool


class AlertRepository:
    """告警 Repository。"""

    def __init__(self, pool: AsyncConnectionPool) -> None:
        self._pool = pool

    async def insert(self, alert: Alert) -> None:
        """插入 Alert 记录（写路径）。

        结论: alert_type / severity 由 DB CHECK 约束校验，额外防护。
        """
        async with self._pool.write_connection() as conn:
            await conn.execute(
                """
                INSERT INTO alerts (
                    alert_id, alert_type, severity, body, created_at, dismissed_at
                ) VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    alert.alert_id,
                    alert.alert_type.value,
                    alert.severity.value,
                    alert.body,
                    alert.created_at.isoformat(),
                    alert.dismissed_at.isoformat() if alert.dismissed_at else None,
                ),
            )
            await conn.commit()

    async def latest_active(self, limit: int = 10) -> list[Alert]:
        """查询最近未 dismiss 的告警（读路径）。

        结论: dismissed_at IS NULL 即为 active，按 created_at DESC 排列。
        """
        async with self._pool.connection() as conn:
            cursor = await conn.execute(
                """
                SELECT * FROM alerts
                WHERE dismissed_at IS NULL
                ORDER BY created_at DESC
                LIMIT ?
                """,
                (limit,),
            )
            rows = await cursor.fetchall()
            return [self._row_to_alert(dict(row)) for row in rows]

    async def dismiss(self, alert_id: str) -> None:
        """将 alert 标记为已处理（写路径）。

        结论: 填入 dismissed_at = now(UTC)，human 确认后调用。
        """
        now = datetime.now(tz=UTC).isoformat()
        async with self._pool.write_connection() as conn:
            await conn.execute(
                "UPDATE alerts SET dismissed_at = ? WHERE alert_id = ?",
                (now, alert_id),
            )
            await conn.commit()

    # ── 私有辅助 ──────────────────────────────────────────────────────────────

    @staticmethod
    def _row_to_alert(row: dict[str, Any]) -> Alert:
        """将 DB row dict 构造为 Alert 域对象。"""
        dismissed_at = None
        if row.get("dismissed_at") is not None:
            dismissed_at = datetime.fromisoformat(str(row["dismissed_at"]))
        return Alert(
            alert_id=str(row["alert_id"]),
            alert_type=AlertType(str(row["alert_type"])),
            severity=AlertSeverity(str(row["severity"])),
            body=str(row["body"]),
            created_at=datetime.fromisoformat(str(row["created_at"])),
            dismissed_at=dismissed_at,
        )
