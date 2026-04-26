"""
DecisionRecorder 服务 + DecisionDraftRepository — T008
结论: 双阶段决策录入核心逻辑
细节:
  - DecisionDraftRepository: 真实 SQLite CRUD，含 gc_expired
  - DecisionRecorder.create_draft: asyncio.timeout(5.0) + asyncio.gather 并行 LLM
    超时时 → 将已创建的 draft 标为 abandoned → raise HTTPException(503)
    不允许 placeholder fallback (R3 B-R2-2)
  - DecisionRecorder.commit_draft: 零 LLM 调用 (不变量 §9.1)
    验证 refs 非 NULL (不变量 #13)、would_have_acted_without_agent 非 None (R2 M1)
  - Protocol 接口隔离 T010/T013 (PEP 544，运行时 duck typing)
"""

from __future__ import annotations

import asyncio
import uuid
from datetime import UTC, datetime
from typing import Any

from fastapi import HTTPException

from decision_ledger.domain.conflict_report import ConflictReport
from decision_ledger.domain.decision import Action, Decision, DecisionStatus
from decision_ledger.domain.decision_draft import DecisionDraft, DraftStatus
from decision_ledger.domain.env_snapshot import EnvSnapshot
from decision_ledger.domain.rebuttal import Rebuttal
from decision_ledger.repository.base import AsyncConnectionPool

# ── DecisionDraftRepository（真实 SQLite 实现）──────────────────────────────


class DecisionDraftRepository:
    """decision_drafts 表 CRUD。

    结论: T008 file_domain 内定义，提供 draft 生命周期管理。
    细节:
      - insert / get / update_refs / commit / abandon: 写路径用 write_connection()
      - gc_expired: 批量 UPDATE status='abandoned' WHERE status='draft' AND created_at < cutoff
    """

    def __init__(self, pool: AsyncConnectionPool) -> None:
        self._pool = pool

    async def insert(self, draft: DecisionDraft) -> None:
        """插入新 draft（写路径）。"""
        async with self._pool.write_connection() as conn:
            await conn.execute(
                """
                INSERT INTO decision_drafts (
                    draft_id, ticker, intended_action, draft_reason,
                    env_snapshot_json, conflict_report_ref, devils_rebuttal_ref,
                    status, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    draft.draft_id,
                    draft.ticker,
                    draft.intended_action.value,
                    draft.draft_reason,
                    draft.env_snapshot.model_dump_json(),
                    draft.conflict_report_ref,
                    draft.devils_rebuttal_ref,
                    draft.status.value,
                    draft.created_at.isoformat(),
                ),
            )
            await conn.commit()

    async def get(self, draft_id: str) -> DecisionDraft | None:
        """按 draft_id 查询单条（读路径）。"""
        async with self._pool.connection() as conn:
            cursor = await conn.execute(
                "SELECT * FROM decision_drafts WHERE draft_id = ?",
                (draft_id,),
            )
            row = await cursor.fetchone()
            if row is None:
                return None
            return self._row_to_draft(dict(row))

    async def update_refs(
        self,
        draft_id: str,
        conflict_report_ref: str,
        devils_rebuttal_ref: str,
    ) -> None:
        """填入 conflict_report_ref 和 devils_rebuttal_ref（写路径）。"""
        async with self._pool.write_connection() as conn:
            await conn.execute(
                """
                UPDATE decision_drafts
                SET conflict_report_ref = ?, devils_rebuttal_ref = ?
                WHERE draft_id = ?
                """,
                (conflict_report_ref, devils_rebuttal_ref, draft_id),
            )
            await conn.commit()

    async def commit(self, draft_id: str, committed_at: datetime) -> None:
        """将 draft 状态变更为 committed（写路径）。"""
        async with self._pool.write_connection() as conn:
            await conn.execute(
                """
                UPDATE decision_drafts
                SET status = ?, committed_at = ?
                WHERE draft_id = ?
                """,
                (DraftStatus.COMMITTED.value, committed_at.isoformat(), draft_id),
            )
            await conn.commit()

    async def abandon(self, draft_id: str, abandoned_at: datetime) -> None:
        """将 draft 状态变更为 abandoned（写路径）。"""
        async with self._pool.write_connection() as conn:
            await conn.execute(
                """
                UPDATE decision_drafts
                SET status = ?, abandoned_at = ?
                WHERE draft_id = ?
                """,
                (DraftStatus.ABANDONED.value, abandoned_at.isoformat(), draft_id),
            )
            await conn.commit()

    async def gc_expired(self, cutoff_at: datetime) -> int:
        """将 status='draft' AND created_at < cutoff_at 批量标为 abandoned。

        结论: GC worker 调用，cutoff = now() - 30min。
        返回值: 实际 GC 的条数。
        """
        now_iso = datetime.now(tz=UTC).isoformat()
        cutoff_iso = cutoff_at.isoformat()
        async with self._pool.write_connection() as conn:
            cursor = await conn.execute(
                """
                UPDATE decision_drafts
                SET status = ?, abandoned_at = ?
                WHERE status = ? AND created_at < ?
                """,
                (DraftStatus.ABANDONED.value, now_iso, DraftStatus.DRAFT.value, cutoff_iso),
            )
            await conn.commit()
            return cursor.rowcount if cursor.rowcount is not None else 0

    async def list_drafts_by_status(self, status: DraftStatus) -> list[DecisionDraft]:
        """按 status 查询（读路径）。"""
        async with self._pool.connection() as conn:
            cursor = await conn.execute(
                "SELECT * FROM decision_drafts WHERE status = ? ORDER BY created_at DESC",
                (status.value,),
            )
            rows = await cursor.fetchall()
            return [self._row_to_draft(dict(row)) for row in rows]

    # ── 私有辅助 ─────────────────────────────────────────────────────────────

    @staticmethod
    def _row_to_draft(row: dict[str, Any]) -> DecisionDraft:
        """将 DB row dict 构造为 DecisionDraft 域对象。"""
        from decision_ledger.domain.env_snapshot import EnvSnapshot

        env_snapshot = EnvSnapshot.model_validate_json(str(row["env_snapshot_json"]))

        def _parse_dt(val: Any) -> datetime | None:
            if val is None:
                return None
            return datetime.fromisoformat(str(val))

        return DecisionDraft(
            draft_id=str(row["draft_id"]),
            ticker=str(row["ticker"]),
            intended_action=Action(str(row["intended_action"])),
            draft_reason=str(row["draft_reason"]),
            env_snapshot=env_snapshot,
            conflict_report_ref=(
                str(row["conflict_report_ref"]) if row.get("conflict_report_ref") else None
            ),
            devils_rebuttal_ref=(
                str(row["devils_rebuttal_ref"]) if row.get("devils_rebuttal_ref") else None
            ),
            status=DraftStatus(str(row["status"])),
            created_at=datetime.fromisoformat(str(row["created_at"])),
            committed_at=_parse_dt(row.get("committed_at")),
            abandoned_at=_parse_dt(row.get("abandoned_at")),
        )


# ── DecisionRecorder 服务 ─────────────────────────────────────────────────


class DecisionRecorder:
    """双阶段决策录入服务。

    结论:
      - create_draft: 并行调用 T010/T013，5s 超时无 placeholder fallback
      - commit_draft: 零 LLM 调用，验证 refs 非 NULL
    Protocol 接口隔离:
      - assembler_service: 需有 .assemble(ticker, env_snapshot) -> ConflictReport
      - devil_service: 需有 .generate(ticker, env_snapshot) -> Rebuttal
    """

    # 超时上限（秒），B-R2-2
    _TIMEOUT_SEC: float = 5.0

    def __init__(
        self,
        assembler_service: Any,
        devil_service: Any,
        draft_repo: Any,
        conflict_repo: Any,
        rebuttal_repo: Any,
        decision_repo: Any,
    ) -> None:
        self._assembler = assembler_service
        self._devil = devil_service
        self._draft_repo = draft_repo
        self._conflict_repo = conflict_repo
        self._rebuttal_repo = rebuttal_repo
        self._decision_repo = decision_repo

    async def create_draft(
        self,
        ticker: str,
        intended_action: Action,
        draft_reason: str,
        env_snapshot: EnvSnapshot,
    ) -> tuple[str, ConflictReport, Rebuttal]:
        """创建 draft 并并行调用 LLM（5s 超时，无 placeholder fallback）。

        结论:
          1. 先在 DB 插入 status='draft', refs=NULL
          2. asyncio.timeout(5.0) 内 asyncio.gather(assembler, devil)
          3. 成功 → UPDATE refs
          4. 超时 → abandon draft → HTTPException(503)
        返回: (draft_id, conflict_report, rebuttal)
        """
        draft_id = str(uuid.uuid4())
        now = datetime.now(tz=UTC)

        # 1. 先插入空 draft（refs=NULL）
        draft = DecisionDraft(
            draft_id=draft_id,
            ticker=ticker,
            intended_action=intended_action,
            draft_reason=draft_reason,
            env_snapshot=env_snapshot,
            conflict_report_ref=None,
            devils_rebuttal_ref=None,
            status=DraftStatus.DRAFT,
            created_at=now,
        )
        await self._draft_repo.insert(draft)

        # 2. 并行调用 LLM（5s 超时）
        try:
            async with asyncio.timeout(self._TIMEOUT_SEC):
                conflict_report, rebuttal = await asyncio.gather(
                    self._assembler.assemble(ticker=ticker, env_snapshot=env_snapshot),
                    self._devil.generate(ticker=ticker, env_snapshot=env_snapshot),
                )
        except TimeoutError as err:
            # 超时: 将 draft 标为 abandoned,不允许 placeholder fallback (R3 B-R2-2)
            await self._draft_repo.abandon(draft_id, datetime.now(tz=UTC))
            raise HTTPException(
                status_code=503,
                detail="系统繁忙, 请等 cache warmer 完成或重试",
            ) from err

        # 3. 存储 conflict_report 和 rebuttal
        report_id = str(uuid.uuid4())
        rebuttal_id = str(uuid.uuid4())

        await self._conflict_repo.insert(report_id, conflict_report)
        await self._rebuttal_repo.insert(rebuttal_id, rebuttal)

        # 4. 更新 draft refs
        await self._draft_repo.update_refs(draft_id, report_id, rebuttal_id)

        return draft_id, conflict_report, rebuttal

    async def commit_draft(
        self,
        draft_id: str,
        final_action: Action,
        final_reason: str,
        would_have_acted_without_agent: bool | None,
    ) -> str:
        """将 draft 提交为正式 Decision（零 LLM 调用）。

        结论:
          - 不变量 §9.1: 此方法内禁止任何 LLM 调用
          - 不变量 #13: draft.refs 必须非 NULL
          - R2 M1: would_have_acted_without_agent 必须非 None
        返回: trade_id (新 Decision 的 UUID)
        异常:
          - 404: draft 不存在
          - 409/422: draft 已 committed 或 abandoned
          - 422: refs 为 NULL 或 would_have_acted 为 None
        """
        # R2 M1 校验
        if would_have_acted_without_agent is None:
            raise HTTPException(
                status_code=422,
                detail="would_have_acted_without_agent 不能为空 (R2 M1)",
            )

        # 查询 draft
        draft = await self._draft_repo.get(draft_id)
        if draft is None:
            raise HTTPException(status_code=404, detail=f"draft {draft_id!r} 不存在")

        # 状态校验
        if draft.status != DraftStatus.DRAFT:
            raise HTTPException(
                status_code=409,
                detail=f"draft 已处于 {draft.status!r} 状态，不能重复 commit",
            )

        # 不变量 #13: refs 必须非 NULL
        if draft.conflict_report_ref is None or draft.devils_rebuttal_ref is None:
            raise HTTPException(
                status_code=422,
                detail="draft refs 为 NULL,不满足不变量 #13",
            )

        # 创建 Decision（无 LLM 调用）
        trade_id = str(uuid.uuid4())
        committed_at = datetime.now(tz=UTC)

        decision = Decision(
            trade_id=trade_id,
            ticker=draft.ticker,
            action=final_action,
            reason=final_reason,
            pre_commit_at=committed_at,
            env_snapshot=draft.env_snapshot,
            conflict_report_ref=draft.conflict_report_ref,
            devils_rebuttal_ref=draft.devils_rebuttal_ref,
            would_have_acted_without_agent=would_have_acted_without_agent,
            status=DecisionStatus.COMMITTED,
        )

        # 写入 decisions 表，标记 draft 为 committed
        await self._decision_repo.insert(decision)
        await self._draft_repo.commit(draft_id, committed_at)

        return trade_id
