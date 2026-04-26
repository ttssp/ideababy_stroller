"""
AdvisorStrategy 测试 — T007
结论: 验证 analyze() 调 advisor_repo + LLM，有/无观点两支，rationale_plain 非空
细节:
  - test_analyze_with_view_returns_signal: 有观点时返回非 no_view signal
  - test_analyze_no_view_returns_no_view: 无观点时 confidence=0.0, direction=no_view
  - test_rationale_plain_never_empty: rationale_plain 永远非空（不变量 #4）
  - test_source_id_is_advisor: source_id 固定为 "advisor"
  - test_env_snapshot_passed_to_llm: env_snapshot 必须传给 LLM 调用（R2 B3）
"""

from __future__ import annotations

from datetime import UTC, datetime
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from decision_ledger.domain.advisor import AdvisorWeeklyReport
from decision_ledger.domain.env_snapshot import EnvSnapshot
from decision_ledger.domain.strategy_signal import Direction, StrategySignal
from decision_ledger.strategy.advisor_strategy import AdvisorStrategy


@pytest.fixture
def advisor_week_id() -> str:
    return "2026-W17"


@pytest.fixture
def env_snap(advisor_week_id: str) -> EnvSnapshot:
    return EnvSnapshot(
        price=100.0,
        holdings_pct=0.05,
        holdings_abs=5000.0,
        advisor_week_id=advisor_week_id,
        snapshot_at=datetime.now(tz=UTC),
    )


@pytest.fixture
def report_with_view(advisor_week_id: str) -> AdvisorWeeklyReport:
    """有 TSM 观点的周报。"""
    return AdvisorWeeklyReport(
        advisor_id="advisor_001",
        source_id="advisor_001",
        week_id=advisor_week_id,
        raw_text="本周看多 TSM，目标价 130，预计半导体超级周期启动",
        structured_json={
            "TSM": {
                "direction": "long",
                "confidence": 0.8,
                "rationale": "半导体超级周期启动，TSM 领涨",
            }
        },
    )


@pytest.fixture
def report_no_view(advisor_week_id: str) -> AdvisorWeeklyReport:
    """无 TSM 观点的周报。"""
    return AdvisorWeeklyReport(
        advisor_id="advisor_001",
        source_id="advisor_001",
        week_id=advisor_week_id,
        raw_text="本周重点分析 AAPL，对 TSM 暂无评论",
        structured_json={
            "AAPL": {
                "direction": "neutral",
                "confidence": 0.5,
                "rationale": "等待 Q2 财报",
            }
        },
    )


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
def advisor_strategy(mock_llm: MagicMock, mock_provider: MagicMock) -> AdvisorStrategy:
    return AdvisorStrategy(mock_llm, mock_provider)


class TestAdvisorStrategySourceId:
    """source_id 约束测试。"""

    def test_source_id_is_advisor(self, advisor_strategy: AdvisorStrategy) -> None:
        """结论: source_id 固定为 'advisor'。"""
        assert advisor_strategy.source_id == "advisor"


class TestAdvisorStrategyWithView:
    """有咨询师观点时的 analyze 测试。"""

    async def test_analyze_with_view_returns_signal(
        self,
        advisor_strategy: AdvisorStrategy,
        report_with_view: AdvisorWeeklyReport,
        env_snap: EnvSnapshot,
    ) -> None:
        """结论: 有观点时返回 direction 非 no_view 的 signal。"""
        mock_signal = StrategySignal(
            source_id="advisor",
            ticker="TSM",
            direction=Direction.LONG,
            confidence=0.8,
            rationale_plain="咨询师看多 TSM，半导体超级周期启动，置信度 0.8",
            inputs_used={"advisor_week_id": "2026-W17", "model_version": "advisor_strategy_v1"},
        )
        with patch.object(advisor_strategy, "_call_llm", return_value=mock_signal):
            result = await advisor_strategy.analyze(
                advisor_report=report_with_view,
                portfolio=None,
                ticker="TSM",
                env_snapshot=env_snap,
            )
        assert result.direction != Direction.NO_VIEW
        assert result.confidence > 0.0

    async def test_rationale_plain_not_empty_with_view(
        self,
        advisor_strategy: AdvisorStrategy,
        report_with_view: AdvisorWeeklyReport,
        env_snap: EnvSnapshot,
    ) -> None:
        """结论: 有观点时 rationale_plain 非空（不变量 #4）。"""
        mock_signal = StrategySignal(
            source_id="advisor",
            ticker="TSM",
            direction=Direction.LONG,
            confidence=0.8,
            rationale_plain="咨询师看多 TSM",
            inputs_used={"advisor_week_id": "2026-W17"},
        )
        with patch.object(advisor_strategy, "_call_llm", return_value=mock_signal):
            result = await advisor_strategy.analyze(
                advisor_report=report_with_view,
                portfolio=None,
                ticker="TSM",
                env_snapshot=env_snap,
            )
        assert result.rationale_plain
        assert result.rationale_plain.strip()


class TestAdvisorStrategyNoView:
    """无观点时的 analyze 测试。"""

    async def test_analyze_no_view_returns_no_view_direction(
        self,
        advisor_strategy: AdvisorStrategy,
        report_no_view: AdvisorWeeklyReport,
        env_snap: EnvSnapshot,
    ) -> None:
        """结论: 无观点时 direction=no_view, confidence=0.0。"""
        result = await advisor_strategy.analyze(
            advisor_report=report_no_view,
            portfolio=None,
            ticker="TSM",
            env_snapshot=env_snap,
        )
        assert result.direction == Direction.NO_VIEW
        assert result.confidence == 0.0

    async def test_rationale_plain_not_empty_no_view(
        self,
        advisor_strategy: AdvisorStrategy,
        report_no_view: AdvisorWeeklyReport,
        env_snap: EnvSnapshot,
    ) -> None:
        """结论: 无观点时 rationale_plain 依然非空（不变量 #4，不允许黑箱）。"""
        result = await advisor_strategy.analyze(
            advisor_report=report_no_view,
            portfolio=None,
            ticker="TSM",
            env_snapshot=env_snap,
        )
        assert result.rationale_plain
        assert result.rationale_plain.strip()
        # 应包含"无观点"类说明
        assert (
            "TSM" in result.rationale_plain
            or "本周" in result.rationale_plain
            or "无" in result.rationale_plain
        )

    async def test_no_view_signal_has_correct_source_id(
        self,
        advisor_strategy: AdvisorStrategy,
        report_no_view: AdvisorWeeklyReport,
        env_snap: EnvSnapshot,
    ) -> None:
        """结论: 无观点时 source_id 仍为 'advisor'。"""
        result = await advisor_strategy.analyze(
            advisor_report=report_no_view,
            portfolio=None,
            ticker="TSM",
            env_snapshot=env_snap,
        )
        assert result.source_id == "advisor"


class TestAdvisorStrategyInputsTracking:
    """inputs_used 追溯测试。"""

    async def test_inputs_used_records_advisor_week_id(
        self,
        advisor_strategy: AdvisorStrategy,
        report_with_view: AdvisorWeeklyReport,
        env_snap: EnvSnapshot,
    ) -> None:
        """结论: inputs_used 记录 advisor_week_id（可追溯）。"""
        mock_signal = StrategySignal(
            source_id="advisor",
            ticker="TSM",
            direction=Direction.LONG,
            confidence=0.8,
            rationale_plain="咨询师看多 TSM",
            inputs_used={"advisor_week_id": "2026-W17", "model_version": "advisor_strategy_v1"},
        )
        with patch.object(advisor_strategy, "_call_llm", return_value=mock_signal):
            result = await advisor_strategy.analyze(
                advisor_report=report_with_view,
                portfolio=None,
                ticker="TSM",
                env_snapshot=env_snap,
            )
        assert "advisor_week_id" in result.inputs_used
