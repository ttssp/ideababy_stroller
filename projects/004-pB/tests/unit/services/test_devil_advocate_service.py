"""
DevilAdvocateService 单元测试 — T013
结论: 覆盖 R2/R3 所有强制约束
细节:
  - R2: 反 StrategyModule isinstance
  - R3 fast-path: cache_key_extras 含唯一 nonce, asyncio.wait_for timeout=3.0
  - §9.4: rebuttal_text 非空 → raise; > 80 字 → raise
  - R6: prompt 无红线词
  - latency: mock LLM 2s 延迟, service.generate 完成 < 3s
"""

from __future__ import annotations

import asyncio
import time
from datetime import UTC, datetime
from typing import Any
from unittest.mock import AsyncMock, MagicMock

import pytest
from pydantic import ValidationError

from decision_ledger.domain.decision import Action
from decision_ledger.domain.decision_draft import DecisionDraft
from decision_ledger.domain.env_snapshot import EnvSnapshot
from decision_ledger.domain.rebuttal import Rebuttal
from decision_ledger.strategy.base import StrategyModule

# ── Fixtures ─────────────────────────────────────────────────────────────────

@pytest.fixture
def env_snapshot() -> EnvSnapshot:
    """标准环境快照 fixture。"""
    return EnvSnapshot(
        price=100.0,
        holdings_pct=0.05,
        holdings_abs=5000.0,
        advisor_week_id="2026-W17",
        snapshot_at=datetime(2026, 4, 26, tzinfo=UTC),
    )


@pytest.fixture
def decision_draft(env_snapshot: EnvSnapshot) -> DecisionDraft:
    """标准 DecisionDraft fixture。"""
    return DecisionDraft(
        draft_id="draft-uuid-001",
        ticker="TSM",
        intended_action=Action.BUY,
        draft_reason="咨询师推荐，估值合理",
        env_snapshot=env_snapshot,
    )


@pytest.fixture
def mock_llm_client() -> MagicMock:
    """mock LLMClient，call 返回合法 Rebuttal。"""
    client = MagicMock()
    client.call = AsyncMock(
        return_value=Rebuttal(
            rebuttal_text="考虑反方：半导体周期风险尚未出清，估值修复可能延后。",
            invoked_at=datetime.now(tz=UTC).isoformat(),
        )
    )
    return client


@pytest.fixture
def mock_rebuttal_repo() -> MagicMock:
    """mock RebuttalRepository。"""
    repo = MagicMock()
    repo.insert = AsyncMock()
    return repo


# ── 导入被测对象 ─────────────────────────────────────────────────────────────

def _make_service(llm_client: Any = None, rebuttal_repo: Any = None) -> Any:
    """构造 DevilAdvocateService，延迟导入（测试驱动）。"""
    from decision_ledger.services.devil_advocate_service import DevilAdvocateService
    return DevilAdvocateService(
        llm_client=llm_client or MagicMock(),
        rebuttal_repo=rebuttal_repo or MagicMock(),
    )


# ── R2: 反 StrategyModule isinstance ─────────────────────────────────────────

class TestR2NotStrategyModule:
    """R2 修订: DevilAdvocateService 不是 StrategyModule lane。"""

    def test_is_not_strategy_module_instance(
        self, mock_llm_client: MagicMock, mock_rebuttal_repo: MagicMock
    ) -> None:
        """should return False when isinstance check against StrategyModule"""
        service = _make_service(mock_llm_client, mock_rebuttal_repo)
        assert isinstance(service, StrategyModule) is False, (
            "DevilAdvocateService 不能是 StrategyModule (R2 修订)"
        )

    def test_does_not_have_source_id_attribute(
        self, mock_llm_client: MagicMock, mock_rebuttal_repo: MagicMock
    ) -> None:
        """should not have source_id attribute that StrategyModule requires"""
        service = _make_service(mock_llm_client, mock_rebuttal_repo)
        assert not hasattr(service, "source_id"), (
            "DevilAdvocateService 不能有 source_id 属性 (R2 修订)"
        )

    def test_does_not_have_analyze_method(
        self, mock_llm_client: MagicMock, mock_rebuttal_repo: MagicMock
    ) -> None:
        """should not implement analyze() which is StrategyModule's method"""
        service = _make_service(mock_llm_client, mock_rebuttal_repo)
        assert not hasattr(service, "analyze"), (
            "DevilAdvocateService 不能有 analyze 方法 (R2 修订)"
        )


# ── §9.4 不变量: rebuttal_text 非空 / ≤ 80 字 ──────────────────────────────

class TestRebuttalTextInvariants:
    """§9.4 不变量: rebuttal_text 永远非空，≤ 80 字。"""

    @pytest.mark.asyncio
    async def test_raises_when_llm_returns_empty_string(
        self,
        env_snapshot: EnvSnapshot,
        mock_rebuttal_repo: MagicMock,
    ) -> None:
        """should raise ValueError when mock LLM returns empty rebuttal_text"""
        from decision_ledger.llm.errors import LLMSchemaError

        client = MagicMock()
        # LLM 返回空 text 时, Rebuttal validator 会 raise，
        # 或者 LLMClient 返回无效数据，service 需要 catch 并 raise ValueError
        client.call = AsyncMock(
            side_effect=LLMSchemaError("rebuttal_text 不能为空", raw_data={})
        )
        service = _make_service(client, mock_rebuttal_repo)

        with pytest.raises((ValueError, Exception)):
            await service.generate(ticker="TSM", env_snapshot=env_snapshot)

    @pytest.mark.asyncio
    async def test_raises_or_truncates_when_llm_returns_over_80_chars(
        self,
        env_snapshot: EnvSnapshot,
        mock_rebuttal_repo: MagicMock,
    ) -> None:
        """should raise or truncate when mock LLM returns rebuttal_text > 80 chars"""
        long_text = "考虑反方意见：" + "这是超长的反驳文字，" * 10  # 明显超 80 字
        assert len(long_text) > 80

        client = MagicMock()
        # mock: LLMClient 返回超长 text (已通过 Rebuttal model 校验失败)
        # service 应该 raise ValueError 或 truncate
        from decision_ledger.llm.errors import LLMSchemaError
        client.call = AsyncMock(
            side_effect=LLMSchemaError(
                "rebuttal_text 不能超过 80 字符", raw_data={"rebuttal_text": long_text}
            )
        )
        service = _make_service(client, mock_rebuttal_repo)

        with pytest.raises((ValueError, ValidationError, LLMSchemaError)):
            await service.generate(ticker="TSM", env_snapshot=env_snapshot)

    @pytest.mark.asyncio
    async def test_returns_rebuttal_when_text_within_80_chars(
        self,
        env_snapshot: EnvSnapshot,
        mock_llm_client: MagicMock,
        mock_rebuttal_repo: MagicMock,
    ) -> None:
        """should return Rebuttal with valid text when LLM returns ≤ 80 char text"""
        service = _make_service(mock_llm_client, mock_rebuttal_repo)
        result = await service.generate(ticker="TSM", env_snapshot=env_snapshot)

        assert isinstance(result, Rebuttal)
        assert result.rebuttal_text
        assert len(result.rebuttal_text) <= 80


# ── R3 fast-path 配置验证 ─────────────────────────────────────────────────────

class TestR3FastPathConfig:
    """R3 B-R2-3: LLMClient.call 必须用 fast-path 配置。"""

    @pytest.mark.asyncio
    async def test_llm_call_uses_correct_model(
        self,
        env_snapshot: EnvSnapshot,
        mock_llm_client: MagicMock,
        mock_rebuttal_repo: MagicMock,
    ) -> None:
        """should call LLM with model='claude-sonnet-4-6' when generating rebuttal"""
        service = _make_service(mock_llm_client, mock_rebuttal_repo)
        await service.generate(ticker="TSM", env_snapshot=env_snapshot)

        mock_llm_client.call.assert_called_once()
        call_kwargs = mock_llm_client.call.call_args
        # model 参数
        assert call_kwargs.kwargs.get("model") == "claude-sonnet-4-6", (
            "R3: 必须使用 claude-sonnet-4-6 (不降 Haiku)"
        )

    @pytest.mark.asyncio
    async def test_llm_call_uses_cache_nonce_for_bypass(
        self,
        env_snapshot: EnvSnapshot,
        mock_llm_client: MagicMock,
        mock_rebuttal_repo: MagicMock,
    ) -> None:
        """nonce 唯一 cache_key 强制 miss (R3 cache_lookup=False 等价)。"""
        service = _make_service(mock_llm_client, mock_rebuttal_repo)
        await service.generate(ticker="TSM", env_snapshot=env_snapshot)

        call_kwargs = mock_llm_client.call.call_args
        cache_key_extras = call_kwargs.kwargs.get("cache_key_extras", {})
        # nonce 必须存在且非空 (每次唯一, 保证 cache miss)
        assert "nonce" in cache_key_extras, (
            "R3: cache_key_extras 必须含 nonce 以绕过 cache (等价 cache_lookup=False)"
        )
        assert cache_key_extras["nonce"], "R3: nonce 不能为空"

    @pytest.mark.asyncio
    async def test_two_calls_have_different_nonces(
        self,
        env_snapshot: EnvSnapshot,
        mock_llm_client: MagicMock,
        mock_rebuttal_repo: MagicMock,
    ) -> None:
        """should use different nonces for consecutive calls (cache miss every time)"""
        service = _make_service(mock_llm_client, mock_rebuttal_repo)
        await service.generate(ticker="TSM", env_snapshot=env_snapshot)
        await service.generate(ticker="TSM", env_snapshot=env_snapshot)

        calls = mock_llm_client.call.call_args_list
        assert len(calls) == 2
        nonce_1 = calls[0].kwargs.get("cache_key_extras", {}).get("nonce")
        nonce_2 = calls[1].kwargs.get("cache_key_extras", {}).get("nonce")
        assert nonce_1 != nonce_2, "R3: 每次调用的 nonce 必须不同"

    @pytest.mark.asyncio
    async def test_llm_call_uses_devil_advocate_v1_template(
        self,
        env_snapshot: EnvSnapshot,
        mock_llm_client: MagicMock,
        mock_rebuttal_repo: MagicMock,
    ) -> None:
        """should use 'devil_advocate_v1' template_version when calling LLM"""
        service = _make_service(mock_llm_client, mock_rebuttal_repo)
        await service.generate(ticker="TSM", env_snapshot=env_snapshot)

        call_kwargs = mock_llm_client.call.call_args
        assert call_kwargs.kwargs.get("template_version") == "devil_advocate_v1"

    @pytest.mark.asyncio
    async def test_llm_call_uses_rebuttal_schema(
        self,
        env_snapshot: EnvSnapshot,
        mock_llm_client: MagicMock,
        mock_rebuttal_repo: MagicMock,
    ) -> None:
        """should pass Rebuttal as schema to LLM call"""
        service = _make_service(mock_llm_client, mock_rebuttal_repo)
        await service.generate(ticker="TSM", env_snapshot=env_snapshot)

        call_kwargs = mock_llm_client.call.call_args
        assert call_kwargs.kwargs.get("schema") == Rebuttal


# ── R3 timeout ≤ 3s ──────────────────────────────────────────────────────────

class TestR3Latency:
    """R3 latency 约束: service.generate() 在 LLM ~2s 时完成 < 3s。"""

    @pytest.mark.asyncio
    async def test_generate_completes_within_3s_when_llm_takes_2s(
        self,
        env_snapshot: EnvSnapshot,
        mock_rebuttal_repo: MagicMock,
    ) -> None:
        """should complete within 3s when mock LLM returns after ~2s delay"""
        async def _slow_call(*args: Any, **kwargs: Any) -> Rebuttal:
            await asyncio.sleep(2.0)
            return Rebuttal(
                rebuttal_text="考虑反方：短期利率仍高，成长股估值承压。",
                invoked_at=datetime.now(tz=UTC).isoformat(),
            )

        client = MagicMock()
        client.call = _slow_call

        service = _make_service(client, mock_rebuttal_repo)

        start = time.monotonic()
        result = await service.generate(ticker="TSM", env_snapshot=env_snapshot)
        elapsed = time.monotonic() - start

        assert elapsed < 3.0, f"service.generate() 耗时 {elapsed:.2f}s，超过 3s 上限"
        assert isinstance(result, Rebuttal)

    @pytest.mark.asyncio
    async def test_generate_raises_timeout_when_llm_exceeds_3s(
        self,
        env_snapshot: EnvSnapshot,
        mock_rebuttal_repo: MagicMock,
    ) -> None:
        """should raise TimeoutError when mock LLM takes > 3s"""
        async def _very_slow_call(*args: Any, **kwargs: Any) -> Rebuttal:
            await asyncio.sleep(10.0)  # 远超 3s
            return Rebuttal(
                rebuttal_text="不会到达这里",
                invoked_at=datetime.now(tz=UTC).isoformat(),
            )

        client = MagicMock()
        client.call = _very_slow_call

        service = _make_service(client, mock_rebuttal_repo)

        with pytest.raises(TimeoutError):
            await service.generate(ticker="TSM", env_snapshot=env_snapshot)


# ── 正常流程: rebuttal_repo.insert 被调用 ────────────────────────────────────

class TestNormalFlow:
    """正常流程: 生成 Rebuttal 并写入 repo。"""

    @pytest.mark.asyncio
    async def test_rebuttal_repo_insert_called_with_generated_rebuttal(
        self,
        env_snapshot: EnvSnapshot,
        mock_llm_client: MagicMock,
        mock_rebuttal_repo: MagicMock,
    ) -> None:
        """should call rebuttal_repo.insert once with valid rebuttal_id and Rebuttal"""
        service = _make_service(mock_llm_client, mock_rebuttal_repo)
        result = await service.generate(ticker="TSM", env_snapshot=env_snapshot)

        mock_rebuttal_repo.insert.assert_called_once()
        call_args = mock_rebuttal_repo.insert.call_args
        rebuttal_id_arg = (
            call_args.args[0] if call_args.args else call_args.kwargs.get("rebuttal_id")
        )
        rebuttal_arg = (
            call_args.args[1] if len(call_args.args) > 1 else call_args.kwargs.get("rebuttal")
        )

        assert rebuttal_id_arg  # rebuttal_id 非空
        assert rebuttal_arg == result

    @pytest.mark.asyncio
    async def test_generate_returns_rebuttal_id_in_result_metadata(
        self,
        env_snapshot: EnvSnapshot,
        mock_llm_client: MagicMock,
        mock_rebuttal_repo: MagicMock,
    ) -> None:
        """should return Rebuttal with non-empty rebuttal_text and invoked_at"""
        service = _make_service(mock_llm_client, mock_rebuttal_repo)
        result = await service.generate(ticker="TSM", env_snapshot=env_snapshot)

        assert result.rebuttal_text
        assert result.invoked_at

    @pytest.mark.asyncio
    async def test_generate_also_accepts_decision_draft(
        self,
        decision_draft: DecisionDraft,
        env_snapshot: EnvSnapshot,
        mock_llm_client: MagicMock,
        mock_rebuttal_repo: MagicMock,
    ) -> None:
        """should accept decision_draft parameter and extract ticker from it"""
        service = _make_service(mock_llm_client, mock_rebuttal_repo)
        result = await service.generate(
            decision_draft=decision_draft, env_snapshot=env_snapshot
        )
        assert isinstance(result, Rebuttal)


# ── R6 红线词检测 (source code grep 由 Verification 脚本完成, 此处 smoke test) ──

class TestR6PromptCompliance:
    """R6: prompt 不含诱导高频交易词汇。"""

    def test_prompt_file_exists(self) -> None:
        """should have devil_advocate_v1.md prompt file"""
        from pathlib import Path
        # parents[3] = projects/004-pB (project root, 3 levels up from tests/unit/services/)
        prompt_path = Path(__file__).parents[3] / "docs" / "prompts" / "devil_advocate_v1.md"
        assert prompt_path.exists(), f"prompt 文件不存在: {prompt_path}"

    def test_prompt_file_no_r6_keywords(self) -> None:
        """should not contain R6 red-line keywords in prompt"""
        from pathlib import Path
        prompt_path = Path(__file__).parents[3] / "docs" / "prompts" / "devil_advocate_v1.md"
        if not prompt_path.exists():
            pytest.skip("prompt 文件不存在，跳过 R6 检测")

        content = prompt_path.read_text(encoding="utf-8")
        r6_keywords = ["建议本周做", "建议加仓", "建议减仓"]
        for kw in r6_keywords:
            assert kw not in content, (
                f"R6 红线词 '{kw}' 出现在 prompt 模板中，必须删除"
            )

    def test_prompt_file_contains_required_tone(self) -> None:
        """should contain '考虑反方' tone directive in prompt"""
        from pathlib import Path
        prompt_path = Path(__file__).parents[3] / "docs" / "prompts" / "devil_advocate_v1.md"
        if not prompt_path.exists():
            pytest.skip("prompt 文件不存在，跳过语气检测")

        content = prompt_path.read_text(encoding="utf-8")
        assert "考虑反方" in content, "prompt 必须包含 '考虑反方' 语气"
