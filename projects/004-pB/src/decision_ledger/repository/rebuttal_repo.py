"""
RebuttalRepository — T003
结论: 反驳记录 CRUD
细节:
  - insert: 插入 Rebuttal（写路径，rebuttal_id 外部生成）
  - get_for_decision: 按关联 decision 的 rebuttal_id 查询（读路径）
"""

from __future__ import annotations

from decision_ledger.domain.rebuttal import Rebuttal
from decision_ledger.repository.base import AsyncConnectionPool


class RebuttalRepository:
    """Rebuttal Repository。"""

    def __init__(self, pool: AsyncConnectionPool) -> None:
        self._pool = pool

    async def insert(self, rebuttal_id: str, rebuttal: Rebuttal) -> None:
        """插入 Rebuttal 记录（写路径）。"""
        async with self._pool.write_connection() as conn:
            await conn.execute(
                """
                INSERT INTO rebuttals (rebuttal_id, rebuttal_text, invoked_at)
                VALUES (?, ?, ?)
                """,
                (rebuttal_id, rebuttal.rebuttal_text, rebuttal.invoked_at),
            )
            await conn.commit()

    async def get_for_decision(self, rebuttal_id: str) -> Rebuttal | None:
        """按 rebuttal_id 查询（读路径）。

        结论: 方法名 get_for_decision 表明用途（从 decision.devils_rebuttal_ref 传入）。
        """
        async with self._pool.connection() as conn:
            cursor = await conn.execute(
                "SELECT * FROM rebuttals WHERE rebuttal_id = ?",
                (rebuttal_id,),
            )
            row = await cursor.fetchone()
            if row is None:
                return None
            return Rebuttal(
                rebuttal_text=str(row["rebuttal_text"]),
                invoked_at=str(row["invoked_at"]),
            )
