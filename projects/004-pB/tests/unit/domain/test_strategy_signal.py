"""
StrategySignal / ConflictReport / Rebuttal 验证测试 — T002 TDD 先写 (红)
结论: 覆盖不变量 #2 (signals ≥ 3) / #4 (rationale_plain 非空) / R10 (无 priority/winner)
"""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from decision_ledger.domain.conflict_report import ConflictReport
from decision_ledger.domain.rebuttal import Rebuttal
from decision_ledger.domain.strategy_signal import Direction, StrategySignal

# ── fixture 工厂 ───────────────────────────────────────────────────────────────

def _make_signal(
    source_id: str = "advisor",
    direction: Direction = Direction.LONG,
    confidence: float = 0.8,
    rationale_plain: str = "看多理由",
) -> StrategySignal:
    return StrategySignal(
        source_id=source_id,
        ticker="TSM",
        direction=direction,
        confidence=confidence,
        rationale_plain=rationale_plain,
        inputs_used={"advisor_week_id": "2026-W17", "price_at": 150.0},
    )


def _make_three_signals() -> list[StrategySignal]:
    """返回架构不变量 #2 要求的最少 3 条 signal。"""
    return [
        _make_signal(source_id="advisor", direction=Direction.LONG),
        _make_signal(source_id="placeholder_model", direction=Direction.NO_VIEW, confidence=0.0),
        _make_signal(source_id="agent_synthesis", direction=Direction.NEUTRAL),
    ]


# ── StrategySignal 方向 enum 测试 ─────────────────────────────────────────────

def test_direction_enum_values() -> None:
    """结论: Direction enum 必含全部合法值。"""
    assert Direction.LONG == "long"
    assert Direction.SHORT == "short"
    assert Direction.NEUTRAL == "neutral"
    assert Direction.WAIT == "wait"
    assert Direction.NO_VIEW == "no_view"


def test_strategy_signal_valid_pass() -> None:
    """结论: 合法 StrategySignal 不报错。"""
    s = _make_signal()
    assert s.source_id == "advisor"
    assert s.confidence == 0.8


def test_strategy_signal_invalid_direction_raises() -> None:
    """结论: 非法 direction 应触发 ValidationError。"""
    with pytest.raises(ValidationError):
        StrategySignal(
            source_id="advisor",
            ticker="TSM",
            direction="bullish",  # type: ignore[arg-type]
            confidence=0.8,
            rationale_plain="理由",
            inputs_used={},
        )


# ── rationale_plain 非空校验 (不变量 #4) ─────────────────────────────────────

def test_strategy_signal_rationale_plain_empty_raises() -> None:
    """结论: rationale_plain='' 应触发 ValidationError (不变量 #4 R3 红线)。"""
    with pytest.raises(ValidationError, match="rationale_plain"):
        StrategySignal(
            source_id="advisor",
            ticker="TSM",
            direction=Direction.LONG,
            confidence=0.8,
            rationale_plain="",  # 空字符串 → 报错
            inputs_used={},
        )


def test_strategy_signal_confidence_range() -> None:
    """结论: confidence 必须在 0.0-1.0 范围。"""
    # 0.0 合法 (confidence=0.0 表示没意见)
    s = _make_signal(confidence=0.0)
    assert s.confidence == 0.0
    # > 1.0 非法
    with pytest.raises(ValidationError):
        _make_signal(confidence=1.1)
    # < 0.0 非法
    with pytest.raises(ValidationError):
        _make_signal(confidence=-0.1)


# ── ConflictReport signals ≥ 3 校验 (不变量 #2) ──────────────────────────────

def test_conflict_report_signals_3_pass() -> None:
    """结论: signals 恰好 3 条合法 (不变量 #2 最小值)。"""
    cr = ConflictReport(
        signals=_make_three_signals(),
        divergence_root_cause="观点 A/B 分歧在仓位大小",
        has_divergence=True,
        rendered_order_seed=42,
    )
    assert len(cr.signals) == 3


def test_conflict_report_signals_more_than_3_pass() -> None:
    """结论: signals > 3 条合法。"""
    signals = [*_make_three_signals(), _make_signal(source_id="custom_v1")]
    cr = ConflictReport(
        signals=signals,
        divergence_root_cause="分歧",
        has_divergence=True,
        rendered_order_seed=0,
    )
    assert len(cr.signals) == 4


def test_conflict_report_signals_2_raises() -> None:
    """结论: signals < 3 应触发 ValidationError (不变量 #2)。"""
    with pytest.raises(ValidationError, match="3"):
        ConflictReport(
            signals=_make_three_signals()[:2],  # 只给 2 条
            divergence_root_cause="根因",
            has_divergence=True,
            rendered_order_seed=0,
        )


def test_conflict_report_signals_0_raises() -> None:
    """结论: signals=[] 应触发 ValidationError。"""
    with pytest.raises(ValidationError):
        ConflictReport(
            signals=[],
            divergence_root_cause="根因",
            has_divergence=False,
            rendered_order_seed=0,
        )


def test_conflict_report_divergence_root_cause_empty_raises() -> None:
    """结论: divergence_root_cause 不能为空。"""
    with pytest.raises(ValidationError):
        ConflictReport(
            signals=_make_three_signals(),
            divergence_root_cause="",  # 空 → 报错
            has_divergence=False,
            rendered_order_seed=0,
        )


# ── R10 红线: ConflictReport 无 priority/winner/recommended 字段 ───────────────

def test_conflict_report_has_no_priority_field() -> None:
    """结论: ConflictReport Pydantic model 不含 priority 字段 (R10 红线)。"""
    cr = ConflictReport(
        signals=_make_three_signals(),
        divergence_root_cause="根因",
        has_divergence=False,
        rendered_order_seed=0,
    )
    serialized = cr.model_dump()
    assert "priority" not in serialized, "ConflictReport 不能含 priority 字段"


def test_conflict_report_has_no_winner_field() -> None:
    """结论: ConflictReport Pydantic model 不含 winner 字段 (R10 红线)。"""
    cr = ConflictReport(
        signals=_make_three_signals(),
        divergence_root_cause="根因",
        has_divergence=False,
        rendered_order_seed=0,
    )
    serialized = cr.model_dump()
    assert "winner" not in serialized, "ConflictReport 不能含 winner 字段"


def test_conflict_report_has_no_recommended_field() -> None:
    """结论: ConflictReport Pydantic model 不含 recommended 字段 (R10 红线)。"""
    cr = ConflictReport(
        signals=_make_three_signals(),
        divergence_root_cause="根因",
        has_divergence=False,
        rendered_order_seed=0,
    )
    serialized = cr.model_dump()
    assert "recommended" not in serialized, "ConflictReport 不能含 recommended 字段"


def test_conflict_report_rendered_order_seed_present() -> None:
    """结论: ConflictReport 含 rendered_order_seed (R2 D22)。"""
    cr = ConflictReport(
        signals=_make_three_signals(),
        divergence_root_cause="根因",
        has_divergence=False,
        rendered_order_seed=123,
    )
    assert cr.rendered_order_seed == 123


# ── Rebuttal 测试 ─────────────────────────────────────────────────────────────

def test_rebuttal_valid_pass() -> None:
    """结论: 合法 Rebuttal 不报错。"""
    r = Rebuttal(
        rebuttal_text="这笔交易风险被低估，市场情绪随时可能逆转。",
        invoked_at="2026-04-26T12:00:00+08:00",
    )
    assert len(r.rebuttal_text) > 0


def test_rebuttal_text_empty_raises() -> None:
    """结论: rebuttal_text 为空应触发 ValidationError。"""
    with pytest.raises(ValidationError):
        Rebuttal(rebuttal_text="", invoked_at="2026-04-26T12:00:00+08:00")


def test_rebuttal_text_max_80_chars() -> None:
    """结论: rebuttal_text ≤ 80 字，超出应报错。"""
    with pytest.raises(ValidationError, match="80"):
        Rebuttal(
            rebuttal_text="A" * 81,  # 81 字符 → 报错
            invoked_at="2026-04-26T12:00:00+08:00",
        )


def test_rebuttal_text_80_chars_pass() -> None:
    """结论: rebuttal_text 恰好 80 字符不报错。"""
    r = Rebuttal(
        rebuttal_text="A" * 80,
        invoked_at="2026-04-26T12:00:00+08:00",
    )
    assert len(r.rebuttal_text) == 80
