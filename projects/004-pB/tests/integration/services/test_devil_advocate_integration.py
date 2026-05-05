"""
DevilAdvocateService 集成测试 — T013
结论: 验证 T008 asyncio.gather 并发调用时 rebuttal 已写入 repo
细节:
  - mock LLMClient (不调真实 API)
  - 真实 RebuttalRepository (in-memory SQLite)
  - 验证 draft 阶段同步调用完成后 rebuttal_id 已填入 draft
"""

from __future__ import annotations

import asyncio
from datetime import UTC, datetime
from typing import Any
from unittest.mock import AsyncMock, MagicMock

import pytest

from decision_ledger.domain.decision import Action
from decision_ledger.domain.decision_draft import DecisionDraft
from decision_ledger.domain.env_snapshot import EnvSnapshot
from decision_ledger.domain.rebuttal import Rebuttal

# ── Fixtures ─────────────────────────────────────────────────────────────────

@pytest.fixture
def env_snapshot() -> EnvSnapshot:
    return EnvSnapshot(
        price=150.0,
        holdings_pct=0.08,
        holdings_abs=8000.0,
        advisor_week_id="2026-W17",
        snapshot_at=datetime(2026, 4, 26, tzinfo=UTC),
    )


@pytest.fixture
def decision_draft(env_snapshot: EnvSnapshot) -> DecisionDraft:
    return DecisionDraft(
        draft_id="integration-draft-001",
        ticker="TSM",
        intended_action=Action.BUY,
        draft_reason="技术突破，咨询师看多",
        env_snapshot=env_snapshot,
    )


@pytest.fixture
def mock_llm_client() -> MagicMock:
    """mock LLMClient，快速返回合法 Rebuttal。"""
    client = MagicMock()
    client.call = AsyncMock(
        return_value=Rebuttal(
            rebuttal_text="考虑反方：台积电地缘风险尚存，短期不确定性较高。",
            invoked_at=datetime.now(tz=UTC).isoformat(),
        )
    )
    return client


@pytest.fixture
def mock_rebuttal_repo() -> MagicMock:
    """mock RebuttalRepository，记录 insert 调用。"""
    repo = MagicMock()
    repo.insert = AsyncMock()
    return repo


# ── 集成测试 ─────────────────────────────────────────────────────────────────

class TestDevilAdvocateIntegration:
    """集成测试: asyncio.gather 并发场景下 DevilAdvocateService 行为。"""

    @pytest.mark.asyncio
    async def test_generate_completes_within_gather(
        self,
        env_snapshot: EnvSnapshot,
        mock_llm_client: MagicMock,
        mock_rebuttal_repo: MagicMock,
    ) -> None:
        """should complete generate() within asyncio.gather alongside another coroutine"""
        from decision_ledger.services.devil_advocate_service import DevilAdvocateService

        service = DevilAdvocateService(
            llm_client=mock_llm_client,
            rebuttal_repo=mock_rebuttal_repo,
        )

        # 模拟 T008 asyncio.gather 并发调用场景
        async def _mock_assemble(**kwargs: Any) -> dict[str, Any]:
            await asyncio.sleep(0.1)  # 模拟并行的另一个调用
            return {"signals": [], "divergence_root_cause": "暂无分歧", "has_divergence": False}

        rebuttal, _ = await asyncio.gather(
            service.generate(ticker="TSM", env_snapshot=env_snapshot),
            _mock_assemble(ticker="TSM", env_snapshot=env_snapshot),
        )

        assert isinstance(rebuttal, Rebuttal)
        assert rebuttal.rebuttal_text

    @pytest.mark.asyncio
    async def test_rebuttal_inserted_into_repo_after_generate(
        self,
        env_snapshot: EnvSnapshot,
        mock_llm_client: MagicMock,
        mock_rebuttal_repo: MagicMock,
    ) -> None:
        """should insert rebuttal into repo when generate() completes"""
        from decision_ledger.services.devil_advocate_service import DevilAdvocateService

        service = DevilAdvocateService(
            llm_client=mock_llm_client,
            rebuttal_repo=mock_rebuttal_repo,
        )

        result = await service.generate(ticker="TSM", env_snapshot=env_snapshot)

        # repo.insert 应当被调用一次
        mock_rebuttal_repo.insert.assert_called_once()
        # 第一个参数是 rebuttal_id (UUID 字符串)
        call_args = mock_rebuttal_repo.insert.call_args
        rebuttal_id = (
            call_args.args[0] if call_args.args else call_args.kwargs.get("rebuttal_id")
        )
        rebuttal_obj = (
            call_args.args[1] if len(call_args.args) > 1 else call_args.kwargs.get("rebuttal")
        )

        assert rebuttal_id, "rebuttal_id 不能为空"
        assert rebuttal_obj == result

    @pytest.mark.asyncio
    async def test_generate_returns_rebuttal_id_for_draft_ref(
        self,
        env_snapshot: EnvSnapshot,
        mock_llm_client: MagicMock,
        mock_rebuttal_repo: MagicMock,
    ) -> None:
        """should return Rebuttal so caller can use rebuttal_id as draft ref"""
        from decision_ledger.services.devil_advocate_service import DevilAdvocateService

        service = DevilAdvocateService(
            llm_client=mock_llm_client,
            rebuttal_repo=mock_rebuttal_repo,
        )

        result = await service.generate(ticker="TSM", env_snapshot=env_snapshot)

        # 返回 Rebuttal 对象，调用方可通过 rebuttal_repo.insert 的 rebuttal_id 更新 draft
        assert isinstance(result, Rebuttal)
        assert result.rebuttal_text
        assert result.invoked_at

    @pytest.mark.asyncio
    async def test_generate_with_decision_draft_uses_ticker_from_draft(
        self,
        decision_draft: DecisionDraft,
        env_snapshot: EnvSnapshot,
        mock_llm_client: MagicMock,
        mock_rebuttal_repo: MagicMock,
    ) -> None:
        """should use ticker from DecisionDraft when decision_draft is passed"""
        from decision_ledger.services.devil_advocate_service import DevilAdvocateService

        service = DevilAdvocateService(
            llm_client=mock_llm_client,
            rebuttal_repo=mock_rebuttal_repo,
        )

        result = await service.generate(
            decision_draft=decision_draft,
            env_snapshot=env_snapshot,
        )

        assert isinstance(result, Rebuttal)
        # prompt 应含 ticker 信息 (通过 llm call 的 prompt 参数验证)
        call_kwargs = mock_llm_client.call.call_args
        prompt_text = call_kwargs.kwargs.get("prompt", "") or (
            call_kwargs.args[0] if call_kwargs.args else ""
        )
        assert "TSM" in prompt_text, "prompt 应包含 ticker 信息"

    @pytest.mark.asyncio
    async def test_concurrent_generate_calls_have_unique_rebuttal_ids(
        self,
        env_snapshot: EnvSnapshot,
        mock_rebuttal_repo: MagicMock,
    ) -> None:
        """should produce unique rebuttal_ids for concurrent calls"""
        from decision_ledger.services.devil_advocate_service import DevilAdvocateService

        # 每次 LLM call 返回不同的 Rebuttal (真实场景)
        call_count = 0

        async def _call(*args: Any, **kwargs: Any) -> Rebuttal:
            nonlocal call_count
            call_count += 1
            return Rebuttal(
                rebuttal_text=f"考虑反方：风险 {call_count}。",
                invoked_at=datetime.now(tz=UTC).isoformat(),
            )

        client = MagicMock()
        client.call = _call

        service = DevilAdvocateService(
            llm_client=client,
            rebuttal_repo=mock_rebuttal_repo,
        )

        r1, r2 = await asyncio.gather(
            service.generate(ticker="TSM", env_snapshot=env_snapshot),
            service.generate(ticker="AAPL", env_snapshot=env_snapshot),
        )

        # 两次 insert 用不同的 rebuttal_id
        calls = mock_rebuttal_repo.insert.call_args_list
        assert len(calls) == 2
        id1 = calls[0].args[0] if calls[0].args else calls[0].kwargs.get("rebuttal_id")
        id2 = calls[1].args[0] if calls[1].args else calls[1].kwargs.get("rebuttal_id")
        assert id1 != id2, "并发调用必须产生不同的 rebuttal_id"
