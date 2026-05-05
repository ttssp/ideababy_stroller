"""
PlaceholderModelStrategy 测试 — T007
结论: 永远返回 no_view + confidence=0.0 + rationale_plain 非空
细节:
  - test_always_no_view: 任何输入都返回 direction=no_view（Q6 默认假设）
  - test_always_zero_confidence: confidence 永远为 0.0
  - test_rationale_plain_never_empty: rationale_plain 非空（不变量 #4）
  - test_source_id_is_placeholder_model: source_id 固定为 "placeholder_model"
  - test_rationale_explains_no_view: rationale_plain 解释为何 no_view（透明度）
"""

from __future__ import annotations

from datetime import UTC, datetime
from unittest.mock import MagicMock

import pytest

from decision_ledger.domain.advisor import AdvisorWeeklyReport
from decision_ledger.domain.env_snapshot import EnvSnapshot
from decision_ledger.domain.strategy_signal import Direction
from decision_ledger.strategy.placeholder_model import PlaceholderModelStrategy


@pytest.fixture
def mock_llm() -> MagicMock:
    return MagicMock()


@pytest.fixture
def mock_provider() -> MagicMock:
    return MagicMock()


@pytest.fixture
def placeholder(mock_llm: MagicMock, mock_provider: MagicMock) -> PlaceholderModelStrategy:
    return PlaceholderModelStrategy(mock_llm, mock_provider)


@pytest.fixture
def env_snap() -> EnvSnapshot:
    return EnvSnapshot(
        price=100.0,
        holdings_pct=None,
        holdings_abs=None,
        advisor_week_id="2026-W17",
        snapshot_at=datetime.now(tz=UTC),
    )


@pytest.fixture
def any_report() -> AdvisorWeeklyReport:
    return AdvisorWeeklyReport(
        advisor_id="advisor_001",
        source_id="advisor_001",
        week_id="2026-W17",
        raw_text="任意内容",
        structured_json={"TSM": {"direction": "long", "confidence": 0.9}},
    )


class TestPlaceholderModelAlwaysNoView:
    """PlaceholderModelStrategy 永远 no_view 测试。"""

    async def test_always_returns_no_view_direction(
        self,
        placeholder: PlaceholderModelStrategy,
        any_report: AdvisorWeeklyReport,
        env_snap: EnvSnapshot,
    ) -> None:
        """结论: 任何 ticker 任何时候都返回 direction=no_view（Q6 默认假设）。"""
        for ticker in ["TSM", "AAPL", "NVDA", "BRK.B", "2330.TW"]:
            result = await placeholder.analyze(
                advisor_report=any_report,
                portfolio=None,
                ticker=ticker,
                env_snapshot=env_snap,
            )
            assert result.direction == Direction.NO_VIEW, (
                f"ticker={ticker} 时 PlaceholderModelStrategy 应返回 no_view，"
                f"实际: {result.direction}"
            )

    async def test_always_zero_confidence(
        self,
        placeholder: PlaceholderModelStrategy,
        any_report: AdvisorWeeklyReport,
        env_snap: EnvSnapshot,
    ) -> None:
        """结论: confidence 永远为 0.0（Q6 默认假设，不假装"模型有意见"）。"""
        result = await placeholder.analyze(
            advisor_report=any_report,
            portfolio=None,
            ticker="TSM",
            env_snapshot=env_snap,
        )
        assert result.confidence == 0.0

    async def test_rationale_plain_never_empty(
        self,
        placeholder: PlaceholderModelStrategy,
        any_report: AdvisorWeeklyReport,
        env_snap: EnvSnapshot,
    ) -> None:
        """结论: rationale_plain 永远非空（不变量 #4 R3 红线）。"""
        result = await placeholder.analyze(
            advisor_report=any_report,
            portfolio=None,
            ticker="TSM",
            env_snapshot=env_snap,
        )
        assert result.rationale_plain, "rationale_plain 不得为空字符串"
        assert result.rationale_plain.strip(), "rationale_plain 不得只含空白字符"

    async def test_rationale_plain_explains_no_view(
        self,
        placeholder: PlaceholderModelStrategy,
        any_report: AdvisorWeeklyReport,
        env_snap: EnvSnapshot,
    ) -> None:
        """
        结论: rationale_plain 应解释为何 no_view（透明度，不是黑箱）。
        细节: Q6 设计意图是"反对假精度"，rationale 应说明这是占位，真模型 v0.5+ 替换。
        """
        result = await placeholder.analyze(
            advisor_report=any_report,
            portfolio=None,
            ticker="TSM",
            env_snapshot=env_snap,
        )
        # 应该包含"占位"或"无观点"或"v0.5"之类的说明
        rationale = result.rationale_plain.lower()
        has_explanation = any(
            word in rationale
            for word in ["占位", "无观点", "v0.5", "模型", "placeholder", "保守"]
        )
        assert has_explanation, (
            f"rationale_plain 应解释 no_view 的原因（反对假精度），实际: {result.rationale_plain!r}"
        )


class TestPlaceholderModelSourceId:
    """source_id 约束测试。"""

    def test_source_id_is_placeholder_model(
        self, placeholder: PlaceholderModelStrategy
    ) -> None:
        """结论: source_id 固定为 'placeholder_model'。"""
        assert placeholder.source_id == "placeholder_model"


class TestPlaceholderModelInputsTracking:
    """inputs_used 追溯测试。"""

    async def test_inputs_used_not_empty(
        self,
        placeholder: PlaceholderModelStrategy,
        any_report: AdvisorWeeklyReport,
        env_snap: EnvSnapshot,
    ) -> None:
        """结论: inputs_used 非空，含 model_version 字段（可追溯）。"""
        result = await placeholder.analyze(
            advisor_report=any_report,
            portfolio=None,
            ticker="TSM",
            env_snapshot=env_snap,
        )
        assert result.inputs_used
        assert "model_version" in result.inputs_used
