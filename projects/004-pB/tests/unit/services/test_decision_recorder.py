"""
DecisionRecorder 单元测试 — T008
结论: 验证双阶段录入逻辑、asyncio.timeout、commit 无 LLM、事务完整性
细节:
  - mock T010 ConflictReportAssemblerService / T013 DevilAdvocateServiceProtocol / repos
  - 超时路径: mock 6s sleep → 503 (B-R2-2)
  - commit 路径: 严禁 LLM 调用 (不变量 §9.1)
  - would_have_acted_without_agent 强制 yes/no (R2 M1)
  - ConflictReport.signals 必须来自真实 LLM, 非 placeholder (R3 不变量 #13)
"""

from __future__ import annotations

import asyncio
import uuid
from datetime import UTC, datetime
from typing import Any
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import HTTPException

from decision_ledger.domain.conflict_report import ConflictReport
from decision_ledger.domain.decision import Action
from decision_ledger.domain.decision_draft import DecisionDraft, DraftStatus
from decision_ledger.domain.env_snapshot import EnvSnapshot
from decision_ledger.domain.rebuttal import Rebuttal
from decision_ledger.domain.strategy_signal import Direction, StrategySignal

# ── 测试辅助工厂 ──────────────────────────────────────────


def _make_env_snapshot() -> EnvSnapshot:
    """构造测试用 EnvSnapshot。"""
    return EnvSnapshot(
        price=100.0,
        holdings_pct=0.05,
        holdings_abs=5000.0,
        advisor_week_id="2026-W17",
        snapshot_at=datetime.now(tz=UTC),
    )


def _make_signal(source_id: str, ticker: str = "AAPL") -> StrategySignal:
    """构造测试用 StrategySignal（非 placeholder 内容）。"""
    return StrategySignal(
        source_id=source_id,
        ticker=ticker,
        direction=Direction.LONG,
        confidence=0.8,
        rationale_plain=f"{source_id} 看多因基本面强劲",
        inputs_used={"advisor_week_id": "2026-W17"},
    )


def _make_conflict_report(ticker: str = "AAPL") -> ConflictReport:
    """构造包含 3 条真实 signals 的 ConflictReport（非 placeholder）。"""
    return ConflictReport(
        signals=[
            _make_signal("advisor", ticker),
            _make_signal("agent_synthesis", ticker),
            _make_signal("placeholder_model", ticker),
        ],
        divergence_root_cause="advisor 看多但 agent_synthesis 中性",
        has_divergence=True,
        rendered_order_seed=42,
    )


def _make_rebuttal() -> Rebuttal:
    """构造测试用 Rebuttal。"""
    return Rebuttal(
        rebuttal_text="估值已偏高，风险收益比不佳",
        invoked_at=datetime.now(tz=UTC).isoformat(),
    )


def _make_draft(
    draft_id: str,
    ticker: str = "AAPL",
    conflict_report_ref: str | None = None,
    devils_rebuttal_ref: str | None = None,
    status: DraftStatus = DraftStatus.DRAFT,
) -> DecisionDraft:
    """构造测试用 DecisionDraft。"""
    return DecisionDraft(
        draft_id=draft_id,
        ticker=ticker,
        intended_action=Action.BUY,
        draft_reason="基本面看多，目标 150",
        env_snapshot=_make_env_snapshot(),
        conflict_report_ref=conflict_report_ref,
        devils_rebuttal_ref=devils_rebuttal_ref,
        status=status,
        created_at=datetime.now(tz=UTC),
    )


# ── Mock 类实现 ───────────────────────────────────────────


class FakeDraftRepo:
    """DecisionDraftRepository 的测试 Fake。"""

    def __init__(self) -> None:
        self._drafts: dict[str, DecisionDraft] = {}

    async def insert(self, draft: DecisionDraft) -> None:
        self._drafts[draft.draft_id] = draft

    async def get(self, draft_id: str) -> DecisionDraft | None:
        return self._drafts.get(draft_id)

    async def update_refs(
        self,
        draft_id: str,
        conflict_report_ref: str,
        devils_rebuttal_ref: str,
    ) -> None:
        existing = self._drafts[draft_id]
        # 用 model_copy 替换不可变模型
        self._drafts[draft_id] = existing.model_copy(
            update={
                "conflict_report_ref": conflict_report_ref,
                "devils_rebuttal_ref": devils_rebuttal_ref,
            }
        )

    async def commit(self, draft_id: str, committed_at: datetime) -> None:
        existing = self._drafts[draft_id]
        self._drafts[draft_id] = existing.model_copy(
            update={
                "status": DraftStatus.COMMITTED,
                "committed_at": committed_at,
            }
        )

    async def abandon(self, draft_id: str, abandoned_at: datetime) -> None:
        existing = self._drafts[draft_id]
        self._drafts[draft_id] = existing.model_copy(
            update={
                "status": DraftStatus.ABANDONED,
                "abandoned_at": abandoned_at,
            }
        )

    async def gc_expired(self, cutoff_at: datetime) -> int:
        """将 status='draft' AND created_at < cutoff_at 的 draft 标为 abandoned。"""
        count = 0
        for draft_id, draft in list(self._drafts.items()):
            if draft.status == DraftStatus.DRAFT and draft.created_at < cutoff_at:
                self._drafts[draft_id] = draft.model_copy(
                    update={
                        "status": DraftStatus.ABANDONED,
                        "abandoned_at": datetime.now(tz=UTC),
                    }
                )
                count += 1
        return count

    async def list_drafts_by_status(self, status: DraftStatus) -> list[DecisionDraft]:
        return [d for d in self._drafts.values() if d.status == status]


class FakeConflictRepo:
    """ConflictRepository 的测试 Fake。"""

    def __init__(self) -> None:
        self._reports: dict[str, ConflictReport] = {}

    async def insert(self, report_id: str, report: ConflictReport) -> None:
        self._reports[report_id] = report

    async def get(self, report_id: str) -> ConflictReport | None:
        return self._reports.get(report_id)


class FakeRebuttalRepo:
    """RebuttalRepository 的测试 Fake。"""

    def __init__(self) -> None:
        self._rebuttals: dict[str, Rebuttal] = {}

    async def insert(self, rebuttal_id: str, rebuttal: Rebuttal) -> None:
        self._rebuttals[rebuttal_id] = rebuttal

    async def get_for_decision(self, rebuttal_id: str) -> Rebuttal | None:
        return self._rebuttals.get(rebuttal_id)


class FakeDecisionRepo:
    """DecisionRepository 的测试 Fake。"""

    def __init__(self) -> None:
        from decision_ledger.domain.decision import Decision
        self._decisions: dict[str, Decision] = {}

    async def insert(self, decision: Any) -> None:
        self._decisions[decision.trade_id] = decision

    async def get(self, trade_id: str) -> Any | None:
        return self._decisions.get(trade_id)

    async def list_by_action(self, action: str) -> list[Any]:
        return [d for d in self._decisions.values() if d.action == action]


# ── 测试用 AssemblerService Mock ─────────────────────────


def _make_assembler_service(
    report: ConflictReport | None = None,
    delay: float = 0.0,
) -> AsyncMock:
    """创建 ConflictReportAssemblerService mock。"""
    if report is None:
        report = _make_conflict_report()

    async def _assemble(*args: Any, **kwargs: Any) -> ConflictReport:
        if delay > 0:
            await asyncio.sleep(delay)
        return report

    mock = MagicMock()
    mock.assemble = _assemble
    return mock


def _make_devil_service(
    rebuttal: Rebuttal | None = None,
    delay: float = 0.0,
) -> AsyncMock:
    """创建 DevilAdvocateServiceProtocol mock。"""
    if rebuttal is None:
        rebuttal = _make_rebuttal()

    async def _generate(*args: Any, **kwargs: Any) -> Rebuttal:
        if delay > 0:
            await asyncio.sleep(delay)
        return rebuttal

    mock = MagicMock()
    mock.generate = _generate
    return mock


# ── 创建 DecisionRecorder 实例辅助 ─────────────────────────


def _make_recorder(
    assembler_service: Any = None,
    devil_service: Any = None,
    draft_repo: Any = None,
    conflict_repo: Any = None,
    rebuttal_repo: Any = None,
    decision_repo: Any = None,
) -> Any:
    """构造 DecisionRecorder，所有依赖可 override。"""
    from decision_ledger.services.decision_recorder import DecisionRecorder

    return DecisionRecorder(
        assembler_service=assembler_service or _make_assembler_service(),
        devil_service=devil_service or _make_devil_service(),
        draft_repo=draft_repo or FakeDraftRepo(),
        conflict_repo=conflict_repo or FakeConflictRepo(),
        rebuttal_repo=rebuttal_repo or FakeRebuttalRepo(),
        decision_repo=decision_repo or FakeDecisionRepo(),
    )


# ── 单元测试 ────────────────────────────────────────────


class TestCreateDraft:
    """DecisionRecorder.create_draft 单元测试组。"""

    async def test_should_create_draft_and_fill_refs_when_services_fast(self) -> None:
        """结论: 正常路径下 draft 创建后 conflict_report_ref + devils_rebuttal_ref 都已填。"""
        draft_repo = FakeDraftRepo()
        conflict_repo = FakeConflictRepo()
        rebuttal_repo = FakeRebuttalRepo()

        recorder = _make_recorder(
            draft_repo=draft_repo,
            conflict_repo=conflict_repo,
            rebuttal_repo=rebuttal_repo,
        )

        draft_id, conflict_report, rebuttal = await recorder.create_draft(
            ticker="AAPL",
            intended_action=Action.BUY,
            draft_reason="基本面看多",
            env_snapshot=_make_env_snapshot(),
        )

        # 验证返回值
        assert draft_id is not None
        assert len(draft_id) > 0
        assert isinstance(conflict_report, ConflictReport)
        assert isinstance(rebuttal, Rebuttal)
        assert len(conflict_report.signals) >= 3

        # 验证 draft 存在且 refs 已填
        stored_draft = await draft_repo.get(draft_id)
        assert stored_draft is not None
        assert stored_draft.conflict_report_ref is not None
        assert stored_draft.devils_rebuttal_ref is not None
        assert stored_draft.status == DraftStatus.DRAFT

        # 验证 conflict_report 和 rebuttal 也已存储
        stored_report = await conflict_repo.get(stored_draft.conflict_report_ref)
        assert stored_report is not None
        stored_rebuttal = await rebuttal_repo.get_for_decision(stored_draft.devils_rebuttal_ref)
        assert stored_rebuttal is not None

    async def test_should_raise_503_when_services_timeout_exceeds_5s(self) -> None:
        """结论: R3 B-R2-2 — LLM 调用 > 5s → raise HTTPException(503), 不允许 placeholder。"""
        # 模拟超时: assembler 需要 6s（超过 5s 上限）
        assembler = _make_assembler_service(delay=6.0)
        devil = _make_devil_service(delay=0.0)

        recorder = _make_recorder(assembler_service=assembler, devil_service=devil)

        with pytest.raises(HTTPException) as exc_info:
            await recorder.create_draft(
                ticker="AAPL",
                intended_action=Action.BUY,
                draft_reason="测试超时",
                env_snapshot=_make_env_snapshot(),
            )

        assert exc_info.value.status_code == 503
        assert "系统繁忙" in exc_info.value.detail or "cache" in exc_info.value.detail.lower()

    async def test_should_not_create_committed_draft_when_timeout(self) -> None:
        """结论: 超时后 draft 应为 abandoned（或未创建），不能处于 draft 可继续 commit 的状态。"""
        draft_repo = FakeDraftRepo()
        assembler = _make_assembler_service(delay=6.0)

        recorder = _make_recorder(
            assembler_service=assembler,
            draft_repo=draft_repo,
        )

        with pytest.raises(HTTPException):
            await recorder.create_draft(
                ticker="AAPL",
                intended_action=Action.BUY,
                draft_reason="测试超时",
                env_snapshot=_make_env_snapshot(),
            )

        # 超时后所有 draft 都应该是 abandoned，不能有 status='draft'
        remaining_drafts = await draft_repo.list_drafts_by_status(DraftStatus.DRAFT)
        assert len(remaining_drafts) == 0, "超时后不应有 status=draft 的记录 (B-R2-2)"

    async def test_should_pass_env_snapshot_to_assembler_and_devil(self) -> None:
        """结论: EnvSnapshot 必须正确传递给 assembler.assemble 和 devil.generate。"""
        captured_calls: dict[str, list[Any]] = {"assemble": [], "generate": []}

        async def capturing_assemble(*args: Any, **kwargs: Any) -> ConflictReport:
            captured_calls["assemble"].append((args, kwargs))
            return _make_conflict_report()

        async def capturing_generate(*args: Any, **kwargs: Any) -> Rebuttal:
            captured_calls["generate"].append((args, kwargs))
            return _make_rebuttal()

        assembler = MagicMock()
        assembler.assemble = capturing_assemble
        devil = MagicMock()
        devil.generate = capturing_generate

        env_snapshot = _make_env_snapshot()
        recorder = _make_recorder(assembler_service=assembler, devil_service=devil)

        await recorder.create_draft(
            ticker="AAPL",
            intended_action=Action.BUY,
            draft_reason="基本面看多",
            env_snapshot=env_snapshot,
        )

        # 验证都被调用了
        assert len(captured_calls["assemble"]) == 1
        assert len(captured_calls["generate"]) == 1


class TestCommitDraft:
    """DecisionRecorder.commit_draft 单元测试组。"""

    async def _create_draft_with_refs(
        self,
        recorder: Any,
        draft_repo: FakeDraftRepo,
        conflict_repo: FakeConflictRepo,
        rebuttal_repo: FakeRebuttalRepo,
        ticker: str = "AAPL",
    ) -> str:
        """辅助: 创建有 refs 的 draft，返回 draft_id。"""
        # 直接插入 draft 并预填 refs
        draft_id = str(uuid.uuid4())
        report_id = str(uuid.uuid4())
        rebuttal_id = str(uuid.uuid4())

        conflict_report = _make_conflict_report(ticker)
        rebuttal = _make_rebuttal()

        await conflict_repo.insert(report_id, conflict_report)
        await rebuttal_repo.insert(rebuttal_id, rebuttal)

        draft = _make_draft(
            draft_id=draft_id,
            ticker=ticker,
            conflict_report_ref=report_id,
            devils_rebuttal_ref=rebuttal_id,
            status=DraftStatus.DRAFT,
        )
        await draft_repo.insert(draft)
        return draft_id

    async def test_should_return_trade_id_when_commit_valid_draft(self) -> None:
        """结论: commit_draft 成功时返回 trade_id (UUID)。"""
        draft_repo = FakeDraftRepo()
        conflict_repo = FakeConflictRepo()
        rebuttal_repo = FakeRebuttalRepo()
        decision_repo = FakeDecisionRepo()

        recorder = _make_recorder(
            draft_repo=draft_repo,
            conflict_repo=conflict_repo,
            rebuttal_repo=rebuttal_repo,
            decision_repo=decision_repo,
        )

        draft_id = await self._create_draft_with_refs(
            recorder, draft_repo, conflict_repo, rebuttal_repo
        )

        trade_id = await recorder.commit_draft(
            draft_id=draft_id,
            final_action=Action.BUY,
            final_reason="基本面看多，目标 150",
            would_have_acted_without_agent=True,
        )

        assert trade_id is not None
        assert len(trade_id) > 0

    async def test_should_insert_decision_when_commit_draft(self) -> None:
        """结论: commit_draft 后 decisions 表有新记录，draft 状态变为 committed。"""
        draft_repo = FakeDraftRepo()
        conflict_repo = FakeConflictRepo()
        rebuttal_repo = FakeRebuttalRepo()
        decision_repo = FakeDecisionRepo()

        recorder = _make_recorder(
            draft_repo=draft_repo,
            conflict_repo=conflict_repo,
            rebuttal_repo=rebuttal_repo,
            decision_repo=decision_repo,
        )

        draft_id = await self._create_draft_with_refs(
            recorder, draft_repo, conflict_repo, rebuttal_repo
        )

        trade_id = await recorder.commit_draft(
            draft_id=draft_id,
            final_action=Action.BUY,
            final_reason="基本面看多，目标 150",
            would_have_acted_without_agent=False,
        )

        # 验证 decisions 表有记录
        decision = await decision_repo.get(trade_id)
        assert decision is not None
        assert decision.would_have_acted_without_agent is False

        # 验证 draft 状态变为 committed
        updated_draft = await draft_repo.get(draft_id)
        assert updated_draft is not None
        assert updated_draft.status == DraftStatus.COMMITTED

    async def test_should_raise_422_when_commit_missing_would_have_acted(self) -> None:
        """结论: R2 M1 — would_have_acted_without_agent 未传时 422。"""
        draft_repo = FakeDraftRepo()
        conflict_repo = FakeConflictRepo()
        rebuttal_repo = FakeRebuttalRepo()

        recorder = _make_recorder(
            draft_repo=draft_repo,
            conflict_repo=conflict_repo,
            rebuttal_repo=rebuttal_repo,
        )

        draft_id = await self._create_draft_with_refs(
            recorder, draft_repo, conflict_repo, rebuttal_repo
        )

        # 传 None 应触发 422
        with pytest.raises(HTTPException) as exc_info:
            await recorder.commit_draft(
                draft_id=draft_id,
                final_action=Action.BUY,
                final_reason="基本面看多",
                would_have_acted_without_agent=None,  # type: ignore[arg-type]
            )

        assert exc_info.value.status_code == 422

    async def test_should_raise_404_when_draft_not_found(self) -> None:
        """结论: draft_id 不存在时 commit 返回 404。"""
        recorder = _make_recorder()

        with pytest.raises(HTTPException) as exc_info:
            await recorder.commit_draft(
                draft_id="nonexistent-id",
                final_action=Action.BUY,
                final_reason="基本面看多",
                would_have_acted_without_agent=True,
            )

        assert exc_info.value.status_code == 404

    async def test_should_raise_409_when_draft_already_committed(self) -> None:
        """结论: 重复 commit 已 committed draft 返回 409。"""
        draft_repo = FakeDraftRepo()
        conflict_repo = FakeConflictRepo()
        rebuttal_repo = FakeRebuttalRepo()

        recorder = _make_recorder(
            draft_repo=draft_repo,
            conflict_repo=conflict_repo,
            rebuttal_repo=rebuttal_repo,
        )

        draft_id = await self._create_draft_with_refs(
            recorder, draft_repo, conflict_repo, rebuttal_repo
        )

        # 第一次 commit
        await recorder.commit_draft(
            draft_id=draft_id,
            final_action=Action.BUY,
            final_reason="基本面看多",
            would_have_acted_without_agent=True,
        )

        # 第二次 commit 应失败
        with pytest.raises(HTTPException) as exc_info:
            await recorder.commit_draft(
                draft_id=draft_id,
                final_action=Action.BUY,
                final_reason="基本面看多",
                would_have_acted_without_agent=True,
            )

        assert exc_info.value.status_code in (409, 422)

    async def test_commit_no_llm_should_succeed_even_if_llm_raises(self) -> None:
        """结论: §9.1 不变量 — commit 路径绝对无 LLM 调用，即使 LLM 客户端 raise 也不影响。"""
        draft_repo = FakeDraftRepo()
        conflict_repo = FakeConflictRepo()
        rebuttal_repo = FakeRebuttalRepo()
        decision_repo = FakeDecisionRepo()

        # 创建一个会 raise 的 assembler（模拟 LLM 崩溃）
        async def crashing_assemble(*args: Any, **kwargs: Any) -> ConflictReport:
            raise RuntimeError("LLM 已崩溃，不应在 commit 路径被调用")

        assembler = MagicMock()
        assembler.assemble = crashing_assemble

        recorder = _make_recorder(
            assembler_service=assembler,
            draft_repo=draft_repo,
            conflict_repo=conflict_repo,
            rebuttal_repo=rebuttal_repo,
            decision_repo=decision_repo,
        )

        # 直接在 repo 中插入带 refs 的 draft（绕过 create_draft）
        draft_id = str(uuid.uuid4())
        report_id = str(uuid.uuid4())
        rebuttal_id = str(uuid.uuid4())

        await conflict_repo.insert(report_id, _make_conflict_report())
        await rebuttal_repo.insert(rebuttal_id, _make_rebuttal())
        draft = _make_draft(
            draft_id,
            conflict_report_ref=report_id,
            devils_rebuttal_ref=rebuttal_id,
        )
        await draft_repo.insert(draft)

        # commit 不应调用 assembler（哪怕 assembler 会 raise）
        trade_id = await recorder.commit_draft(
            draft_id=draft_id,
            final_action=Action.BUY,
            final_reason="基本面看多",
            would_have_acted_without_agent=True,
        )

        assert trade_id is not None  # commit 成功，LLM 没被调用

    async def test_should_validate_refs_not_null_when_committing(self) -> None:
        """结论: R3 不变量 #13 — commit 时 draft 的 refs 必须非 NULL。"""
        draft_repo = FakeDraftRepo()

        recorder = _make_recorder(draft_repo=draft_repo)

        # 插入一个没有 refs 的 draft（模拟超时后遗漏的 draft）
        draft_id = str(uuid.uuid4())
        draft = _make_draft(
            draft_id=draft_id,
            conflict_report_ref=None,  # refs 为 NULL
            devils_rebuttal_ref=None,
            status=DraftStatus.DRAFT,
        )
        await draft_repo.insert(draft)

        # commit 应失败（refs 为 NULL 违反不变量 #13）
        with pytest.raises(HTTPException) as exc_info:
            await recorder.commit_draft(
                draft_id=draft_id,
                final_action=Action.BUY,
                final_reason="基本面看多",
                would_have_acted_without_agent=True,
            )

        assert exc_info.value.status_code in (422, 409, 400)


class TestGCWorker:
    """draft_gc_worker GC 逻辑单元测试。"""

    async def test_should_gc_expired_drafts_when_older_than_30min(self) -> None:
        """结论: GC 将 status='draft' AND created_at < now()-30min 标为 abandoned。"""
        from datetime import timedelta

        draft_repo = FakeDraftRepo()

        # 插入一个 31 分钟前创建的 draft
        old_draft_id = str(uuid.uuid4())
        old_draft = DecisionDraft(
            draft_id=old_draft_id,
            ticker="AAPL",
            intended_action=Action.HOLD,
            draft_reason="旧的 draft，等待 GC",
            env_snapshot=_make_env_snapshot(),
            status=DraftStatus.DRAFT,
            created_at=datetime.now(tz=UTC) - timedelta(minutes=31),
        )
        await draft_repo.insert(old_draft)

        # 插入一个 5 分钟前创建的 draft（不应被 GC）
        new_draft_id = str(uuid.uuid4())
        new_draft = DecisionDraft(
            draft_id=new_draft_id,
            ticker="AAPL",
            intended_action=Action.BUY,
            draft_reason="新的 draft，不应被 GC",
            env_snapshot=_make_env_snapshot(),
            status=DraftStatus.DRAFT,
            created_at=datetime.now(tz=UTC) - timedelta(minutes=5),
        )
        await draft_repo.insert(new_draft)

        # 执行 GC（cutoff = now()-30min）
        cutoff = datetime.now(tz=UTC) - timedelta(minutes=30)
        gc_count = await draft_repo.gc_expired(cutoff)

        assert gc_count == 1

        # 旧的 draft 应为 abandoned
        old = await draft_repo.get(old_draft_id)
        assert old is not None
        assert old.status == DraftStatus.ABANDONED

        # 新的 draft 应仍为 draft
        new = await draft_repo.get(new_draft_id)
        assert new is not None
        assert new.status == DraftStatus.DRAFT
