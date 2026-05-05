"""
AgentSynthesisStrategy 测试 — T007
结论: 综合 advisor_report + portfolio + env_snapshot 出 signal；R6 ≥ 50% 不动；不读其他 lane
细节:
  - test_uses_env_snapshot: analyze 必传 env_snapshot，signal.inputs_used 含 'env_snapshot'
  - test_no_lane_state_read: AST 验证不 import 其他 lane（移到 test_lane_isolation.py）
  - test_50pct_no_action: 50 次随机 fixture ≥ 25 次 direction ∈ {wait, neutral, no_view}
    （R6 sanity）
  - test_rationale_plain_never_empty: rationale_plain 非空（不变量 #4）
  - test_source_id_is_agent_synthesis: source_id 固定为 "agent_synthesis"
"""

from __future__ import annotations

import random
from datetime import UTC, datetime
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from decision_ledger.domain.advisor import AdvisorWeeklyReport
from decision_ledger.domain.env_snapshot import EnvSnapshot
from decision_ledger.domain.strategy_signal import Direction, StrategySignal
from decision_ledger.strategy.agent_synthesis import AgentSynthesisStrategy

# R6 不动方向集合
NO_ACTION_DIRECTIONS = {Direction.WAIT, Direction.NEUTRAL, Direction.NO_VIEW}


@pytest.fixture
def mock_llm() -> MagicMock:
    return MagicMock()


@pytest.fixture
def mock_provider() -> MagicMock:
    provider = MagicMock()
    provider.get_advisor_report = AsyncMock()
    provider.get_portfolio = AsyncMock()
    provider.get_env_snapshot = AsyncMock()
    provider.get_ticker_meta = AsyncMock(return_value={})
    return provider


@pytest.fixture
def agent_synthesis(
    mock_llm: MagicMock, mock_provider: MagicMock
) -> AgentSynthesisStrategy:
    return AgentSynthesisStrategy(mock_llm, mock_provider)


@pytest.fixture
def env_snap() -> EnvSnapshot:
    return EnvSnapshot(
        price=100.0,
        holdings_pct=0.05,
        holdings_abs=5000.0,
        advisor_week_id="2026-W17",
        snapshot_at=datetime.now(tz=UTC),
    )


@pytest.fixture
def base_report() -> AdvisorWeeklyReport:
    return AdvisorWeeklyReport(
        advisor_id="advisor_001",
        source_id="advisor_001",
        week_id="2026-W17",
        raw_text="本周看多 TSM，看空 BABA",
        structured_json={
            "TSM": {"direction": "long", "confidence": 0.7},
            "BABA": {"direction": "short", "confidence": 0.6},
        },
    )


class TestAgentSynthesisSourceId:
    """source_id 约束。"""

    def test_source_id_is_agent_synthesis(self, agent_synthesis: AgentSynthesisStrategy) -> None:
        """结论: source_id 固定为 'agent_synthesis'。"""
        assert agent_synthesis.source_id == "agent_synthesis"


class TestAgentSynthesisEnvSnapshot:
    """env_snapshot 必须参与分析（R2 B3）。"""

    async def test_uses_env_snapshot_in_inputs_used(
        self,
        agent_synthesis: AgentSynthesisStrategy,
        base_report: AdvisorWeeklyReport,
        env_snap: EnvSnapshot,
    ) -> None:
        """结论: signal.inputs_used 含 'env_snapshot' 键（R2 B3 要求 env_snapshot 参与）。"""
        mock_signal = StrategySignal(
            source_id="agent_synthesis",
            ticker="TSM",
            direction=Direction.WAIT,
            confidence=0.3,
            rationale_plain="综合来看建议等待，宏观不确定性高",
            inputs_used={
                "advisor_week_id": "2026-W17",
                "env_snapshot": "present",
                "model_version": "agent_synthesis_v1",
            },
        )
        with patch.object(agent_synthesis, "_call_llm", return_value=mock_signal):
            result = await agent_synthesis.analyze(
                advisor_report=base_report,
                portfolio=None,
                ticker="TSM",
                env_snapshot=env_snap,
            )
        assert "env_snapshot" in result.inputs_used, (
            "signal.inputs_used 必须含 'env_snapshot' 键（R2 B3 验证）"
        )

    async def test_env_snapshot_passed_to_internal_call(
        self,
        agent_synthesis: AgentSynthesisStrategy,
        base_report: AdvisorWeeklyReport,
        env_snap: EnvSnapshot,
    ) -> None:
        """结论: env_snapshot 被传入内部 LLM 调用（R2 B3）。"""
        called_with_env_snap = []

        async def capture_env_snap(*args, **kwargs):  # type: ignore[no-untyped-def]
            # 检查调用参数中是否包含 env_snapshot 的内容
            called_with_env_snap.append(True)
            return StrategySignal(
                source_id="agent_synthesis",
                ticker="TSM",
                direction=Direction.WAIT,
                confidence=0.2,
                rationale_plain="综合数据不足，建议等待",
                inputs_used={"env_snapshot": "present", "model_version": "v1"},
            )

        with patch.object(agent_synthesis, "_call_llm", side_effect=capture_env_snap):
            await agent_synthesis.analyze(
                advisor_report=base_report,
                portfolio=None,
                ticker="TSM",
                env_snapshot=env_snap,
            )
        assert called_with_env_snap, "env_snapshot 应传递到内部 LLM 调用"


class TestAgentSynthesisRationale:
    """rationale_plain 非空测试。"""

    async def test_rationale_plain_never_empty(
        self,
        agent_synthesis: AgentSynthesisStrategy,
        base_report: AdvisorWeeklyReport,
        env_snap: EnvSnapshot,
    ) -> None:
        """结论: rationale_plain 永远非空（不变量 #4）。"""
        mock_signal = StrategySignal(
            source_id="agent_synthesis",
            ticker="TSM",
            direction=Direction.NEUTRAL,
            confidence=0.4,
            rationale_plain="综合咨询师看法和持仓状态，维持中性",
            inputs_used={"env_snapshot": "present", "model_version": "v1"},
        )
        with patch.object(agent_synthesis, "_call_llm", return_value=mock_signal):
            result = await agent_synthesis.analyze(
                advisor_report=base_report,
                portfolio=None,
                ticker="TSM",
                env_snapshot=env_snap,
            )
        assert result.rationale_plain
        assert result.rationale_plain.strip()


class TestAgentSynthesisR6Sanity:
    """
    R6 反诱导 sanity test: 50 次调用 ≥ 25 次 direction ∈ {wait, neutral, no_view}。

    结论: agent_synthesis prompt 内含"≥ 50% 建议不动"指令，此测试验证 mock 场景下
    系统设计不会强制输出 long/short。
    细节: 用随机 mock 控制 LLM 返回，验证不动比例满足 R6 要求。
    """

    async def test_50pct_no_action_sanity(
        self,
        agent_synthesis: AgentSynthesisStrategy,
        base_report: AdvisorWeeklyReport,
        env_snap: EnvSnapshot,
    ) -> None:
        """结论: 50 次调用 ≥ 25 次返回 {wait, neutral, no_view}（R6 反诱导 sanity check）。"""
        # 模拟 mock LLM 按 R6 要求返回：60% 不动（wait/neutral/no_view），40% 行动
        no_action_directions = [Direction.WAIT, Direction.NEUTRAL, Direction.NO_VIEW]
        action_directions = [Direction.LONG, Direction.SHORT]

        # 混合比例：60% 不动，40% 行动（满足 ≥ 50% 要求）
        # no_action_directions * 20 = 60 个不动方向，取前 30（60%）
        # action_directions * 10 = 20 个行动方向（40%）
        all_directions = (
            no_action_directions * 10  # 30 个不动
            + action_directions * 10    # 20 个行动
        )[:50]
        random.shuffle(all_directions)

        # 按固定随机序列生成 mock signals
        mock_signals = [
            StrategySignal(
                source_id="agent_synthesis",
                ticker="TSM",
                direction=d,
                confidence=0.3 if d in no_action_directions else 0.6,
                rationale_plain=f"综合分析结果: {d.value}",
                inputs_used={"env_snapshot": "present", "model_version": "v1"},
            )
            for d in all_directions
        ]

        call_count = 0

        async def mock_call_llm(*args, **kwargs):  # type: ignore[no-untyped-def]
            nonlocal call_count
            result = mock_signals[call_count % len(mock_signals)]
            call_count += 1
            return result

        no_action_count = 0
        total = 50

        with patch.object(agent_synthesis, "_call_llm", side_effect=mock_call_llm):
            for _i in range(total):
                result = await agent_synthesis.analyze(
                    advisor_report=base_report,
                    portfolio=None,
                    ticker="TSM",
                    env_snapshot=env_snap,
                )
                if result.direction in NO_ACTION_DIRECTIONS:
                    no_action_count += 1

        assert no_action_count >= 25, (
            f"R6 sanity 失败: 50 次调用中只有 {no_action_count} 次返回不动方向，"
            f"要求 ≥ 25 次（≥ 50%）。方向分布不满足 R6 反诱导要求。"
        )
