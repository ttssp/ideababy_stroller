"""
Decision 与 DecisionDraft 验证测试 — T002 TDD 先写 (红)
结论: 覆盖 R2 关键 contract — action enum / reason 长度 / status / would_have_acted_without_agent NOT NULL
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from decision_ledger.domain.decision import Action, Decision, DecisionStatus, PostMortem
from decision_ledger.domain.env_snapshot import EnvSnapshot


# ── fixture 工厂 ───────────────────────────────────────────────────────────────

def _make_env_snapshot() -> EnvSnapshot:
    """返回最小合法 EnvSnapshot。"""
    return EnvSnapshot(
        price=None,
        holdings_pct=None,
        holdings_abs=None,
        advisor_week_id=None,
        snapshot_at=datetime.now(tz=timezone.utc),
    )


def _make_valid_decision(**overrides: object) -> dict[str, object]:
    """返回一个合法的 Decision 构造参数字典，caller 可 override 任意字段。"""
    base: dict[str, object] = {
        "trade_id": str(uuid.uuid4()),
        "ticker": "TSM",
        "action": Action.BUY,
        "reason": "合理买入理由",
        "pre_commit_at": datetime.now(tz=timezone.utc),
        "env_snapshot": _make_env_snapshot(),
        "conflict_report_ref": str(uuid.uuid4()),
        "devils_rebuttal_ref": str(uuid.uuid4()),
        "post_mortem": None,
        "would_have_acted_without_agent": True,
        "status": DecisionStatus.COMMITTED,
    }
    base.update(overrides)
    return base


# ── Action enum 测试 ───────────────────────────────────────────────────────────

def test_action_enum_contains_buy_sell_hold_wait() -> None:
    """结论: Action enum 必须含全部 4 个值 (架构不变量 #3)。"""
    assert Action.BUY == "buy"
    assert Action.SELL == "sell"
    assert Action.HOLD == "hold"
    assert Action.WAIT == "wait"


def test_decision_valid_action_buy() -> None:
    """结论: action='buy' 合法，不应报错。"""
    d = Decision(**_make_valid_decision(action=Action.BUY))
    assert d.action == Action.BUY


def test_decision_valid_action_hold() -> None:
    """结论: action='hold' 合法 (不变量 #3 hold 必含)。"""
    d = Decision(**_make_valid_decision(action=Action.HOLD))
    assert d.action == Action.HOLD


def test_decision_valid_action_wait() -> None:
    """结论: action='wait' 合法 (不变量 #3 wait 必含)。"""
    d = Decision(**_make_valid_decision(action=Action.WAIT))
    assert d.action == Action.WAIT


def test_decision_invalid_action_raises() -> None:
    """结论: 非法 action 值应触发 ValidationError。"""
    with pytest.raises(ValidationError):
        Decision(**_make_valid_decision(action="invalid_action"))  # type: ignore[arg-type]


# ── reason 长度测试 ────────────────────────────────────────────────────────────

def test_decision_reason_max_80_chars_pass() -> None:
    """结论: reason 恰好 80 字符不报错。"""
    reason_80 = "A" * 80
    d = Decision(**_make_valid_decision(reason=reason_80))
    assert len(d.reason) == 80


def test_decision_reason_81_chars_raises() -> None:
    """结论: reason > 80 字符应触发 ValidationError (T002 check constraint)。"""
    reason_81 = "A" * 81
    with pytest.raises(ValidationError, match="80"):
        Decision(**_make_valid_decision(reason=reason_81))


def test_decision_reason_empty_raises() -> None:
    """结论: reason 为空字符串应触发 ValidationError。"""
    with pytest.raises(ValidationError):
        Decision(**_make_valid_decision(reason=""))


# ── would_have_acted_without_agent NOT NULL 测试 (R2 M1) ───────────────────────

def test_decision_would_have_acted_without_agent_true_pass() -> None:
    """结论: would_have_acted_without_agent=True 合法。"""
    d = Decision(**_make_valid_decision(would_have_acted_without_agent=True))
    assert d.would_have_acted_without_agent is True


def test_decision_would_have_acted_without_agent_false_pass() -> None:
    """结论: would_have_acted_without_agent=False 合法。"""
    d = Decision(**_make_valid_decision(would_have_acted_without_agent=False))
    assert d.would_have_acted_without_agent is False


def test_decision_would_have_acted_without_agent_none_raises() -> None:
    """结论: would_have_acted_without_agent=None 应触发 ValidationError (R2 M1 NOT NULL)。"""
    with pytest.raises(ValidationError):
        Decision(**_make_valid_decision(would_have_acted_without_agent=None))  # type: ignore[arg-type]


# ── status enum 测试 (R2) ────────────────────────────────────────────────────

def test_decision_status_committed_pass() -> None:
    """结论: status='committed' 合法。"""
    d = Decision(**_make_valid_decision(status=DecisionStatus.COMMITTED))
    assert d.status == DecisionStatus.COMMITTED


def test_decision_status_draft_pass() -> None:
    """结论: status='draft' 合法 (R2 D8)。"""
    d = Decision(**_make_valid_decision(status=DecisionStatus.DRAFT))
    assert d.status == DecisionStatus.DRAFT


def test_decision_status_abandoned_pass() -> None:
    """结论: status='abandoned' 合法 (R2 D8)。"""
    d = Decision(**_make_valid_decision(status=DecisionStatus.ABANDONED))
    assert d.status == DecisionStatus.ABANDONED


def test_decision_status_invalid_raises() -> None:
    """结论: 无效 status 应触发 ValidationError。"""
    with pytest.raises(ValidationError):
        Decision(**_make_valid_decision(status="unknown_status"))  # type: ignore[arg-type]


# ── PostMortem 子模型测试 ────────────────────────────────────────────────────

def test_decision_post_mortem_optional() -> None:
    """结论: post_mortem=None 合法 (v0.1 可为空)。"""
    d = Decision(**_make_valid_decision(post_mortem=None))
    assert d.post_mortem is None


def test_decision_post_mortem_with_data() -> None:
    """结论: 含数据的 PostMortem 合法。"""
    pm = PostMortem(
        executed_at=datetime.now(tz=timezone.utc),
        result_pct_after_7d=2.5,
        result_pct_after_30d=None,
        retrospective_notes="回顾笔记",
    )
    d = Decision(**_make_valid_decision(post_mortem=pm))
    assert d.post_mortem is not None
    assert d.post_mortem.result_pct_after_7d == 2.5
