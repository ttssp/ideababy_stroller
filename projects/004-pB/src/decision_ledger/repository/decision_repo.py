"""
DecisionRepository — T003
结论: 决策档案 CRUD + 领域查询，写路径用 WriterLock 保护
细节:
  - insert: 插入完整 Decision 记录（含 JSON 序列化 env_snapshot / post_mortem）
  - update_post_mortem: N 天后回填 PostMortem（写路径）
  - update_conflict_ref / update_rebuttal_ref: draft 阶段 ref 更新
  - count_since(days): 最近 N 天 committed 决策数（O10 监控用）
  - list_by_action / list_by_ticker: 查询路径（读，不加锁）
  - count_would_have_acted_without_agent: M1 metrics 计算
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

from decision_ledger.domain.decision import Decision, DecisionStatus, PostMortem
from decision_ledger.repository.base import AsyncConnectionPool


class DecisionRepository:
    """决策档案 Repository。"""

    def __init__(self, pool: AsyncConnectionPool) -> None:
        self._pool = pool

    async def insert(self, decision: Decision) -> None:
        """插入一条 Decision 记录（写路径，持有 WriterLock）。

        结论: env_snapshot / post_mortem 序列化为 JSON TEXT 存储。
        """
        async with self._pool.write_connection() as conn:
            await conn.execute(
                """
                INSERT INTO decisions (
                    trade_id, ticker, action, reason, pre_commit_at,
                    env_snapshot_json, conflict_report_ref, devils_rebuttal_ref,
                    post_mortem_json, would_have_acted_without_agent, status,
                    created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    decision.trade_id,
                    decision.ticker,
                    decision.action.value,
                    decision.reason,
                    decision.pre_commit_at.isoformat(),
                    decision.env_snapshot.model_dump_json(),
                    decision.conflict_report_ref,
                    decision.devils_rebuttal_ref,
                    decision.post_mortem.model_dump_json() if decision.post_mortem else None,
                    int(decision.would_have_acted_without_agent),
                    decision.status.value,
                    datetime.now(tz=UTC).isoformat(),
                    datetime.now(tz=UTC).isoformat(),
                ),
            )
            await conn.commit()

    async def get(self, trade_id: str) -> Decision | None:
        """按 trade_id 查询单条 Decision（读路径，不加锁）。"""
        async with self._pool.connection() as conn:
            cursor = await conn.execute(
                "SELECT * FROM decisions WHERE trade_id = ?",
                (trade_id,),
            )
            row = await cursor.fetchone()
            if row is None:
                return None
            return self._row_to_decision(dict(row))

    async def update_post_mortem(self, trade_id: str, post_mortem: PostMortem) -> None:
        """回填 PostMortem（写路径，N 天后调用）。"""
        async with self._pool.write_connection() as conn:
            await conn.execute(
                """
                UPDATE decisions SET post_mortem_json = ?, updated_at = ?
                WHERE trade_id = ?
                """,
                (
                    post_mortem.model_dump_json(),
                    datetime.now(tz=UTC).isoformat(),
                    trade_id,
                ),
            )
            await conn.commit()

    async def update_conflict_ref(self, trade_id: str, conflict_report_ref: str) -> None:
        """更新 conflict_report_ref（写路径）。"""
        async with self._pool.write_connection() as conn:
            await conn.execute(
                """
                UPDATE decisions SET conflict_report_ref = ?, updated_at = ?
                WHERE trade_id = ?
                """,
                (conflict_report_ref, datetime.now(tz=UTC).isoformat(), trade_id),
            )
            await conn.commit()

    async def update_rebuttal_ref(self, trade_id: str, rebuttal_ref: str) -> None:
        """更新 devils_rebuttal_ref（写路径）。"""
        async with self._pool.write_connection() as conn:
            await conn.execute(
                """
                UPDATE decisions SET devils_rebuttal_ref = ?, updated_at = ?
                WHERE trade_id = ?
                """,
                (rebuttal_ref, datetime.now(tz=UTC).isoformat(), trade_id),
            )
            await conn.commit()

    async def count_since(self, days: int) -> int:
        """最近 N 天 committed 决策数（O10 AlertMonitor 用，读路径）。"""
        cutoff = (datetime.now(tz=UTC) - timedelta(days=days)).isoformat()
        async with self._pool.connection() as conn:
            cursor = await conn.execute(
                """
                SELECT COUNT(*) FROM decisions
                WHERE status = ? AND pre_commit_at >= ?
                """,
                (DecisionStatus.COMMITTED.value, cutoff),
            )
            row = await cursor.fetchone()
            return int(row[0]) if row else 0

    async def list_by_action(self, action: str) -> list[Decision]:
        """按 action 查询（读路径）。"""
        async with self._pool.connection() as conn:
            cursor = await conn.execute(
                "SELECT * FROM decisions WHERE action = ? ORDER BY pre_commit_at DESC",
                (action,),
            )
            rows = await cursor.fetchall()
            return [self._row_to_decision(dict(row)) for row in rows]

    async def list_by_ticker(self, ticker: str) -> list[Decision]:
        """按 ticker 查询（读路径）。"""
        async with self._pool.connection() as conn:
            cursor = await conn.execute(
                "SELECT * FROM decisions WHERE ticker = ? ORDER BY pre_commit_at DESC",
                (ticker,),
            )
            rows = await cursor.fetchall()
            return [self._row_to_decision(dict(row)) for row in rows]

    async def count_would_have_acted_without_agent(self) -> int:
        """统计 would_have_acted_without_agent=True 的决策数（M1 metrics，读路径）。"""
        async with self._pool.connection() as conn:
            cursor = await conn.execute(
                "SELECT COUNT(*) FROM decisions WHERE would_have_acted_without_agent = 1",
            )
            row = await cursor.fetchone()
            return int(row[0]) if row else 0

    # ── 私有辅助 ──────────────────────────────────────────────────────────────

    @staticmethod
    def _row_to_decision(row: dict[str, object]) -> Decision:
        """将 DB row dict 构造为 Decision 域对象。

        结论: JSON 字段在此反序列化，domain 模型在 repo 边界翻译。
        """
        from decision_ledger.domain.env_snapshot import EnvSnapshot

        env_snapshot = EnvSnapshot.model_validate_json(str(row["env_snapshot_json"]))
        post_mortem_raw = row.get("post_mortem_json")
        post_mortem = (
            PostMortem.model_validate_json(str(post_mortem_raw))
            if post_mortem_raw
            else None
        )
        return Decision(
            trade_id=str(row["trade_id"]),
            ticker=str(row["ticker"]),
            action=str(row["action"]),  # type: ignore[arg-type]
            reason=str(row["reason"]),
            pre_commit_at=datetime.fromisoformat(str(row["pre_commit_at"])),
            env_snapshot=env_snapshot,
            conflict_report_ref=str(row["conflict_report_ref"]),
            devils_rebuttal_ref=str(row["devils_rebuttal_ref"]),
            post_mortem=post_mortem,
            would_have_acted_without_agent=bool(row["would_have_acted_without_agent"]),
            status=str(row["status"]),  # type: ignore[arg-type]
        )
