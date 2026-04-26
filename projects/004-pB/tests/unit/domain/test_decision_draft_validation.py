"""
DecisionDraft 验证测试 — T002 TDD 先写 (红)
结论: 覆盖 R2 D13 — status enum / draft_reason ≤ 80 / 时间戳字段 / Watchlist.market enum
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from decision_ledger.domain.decision import Action
from decision_ledger.domain.decision_draft import DecisionDraft, DraftStatus
from decision_ledger.domain.env_snapshot import EnvSnapshot
from decision_ledger.domain.portfolio import Market, Watchlist


# ── fixture 工厂 ───────────────────────────────────────────────────────────────

def _make_env_snapshot() -> EnvSnapshot:
    return EnvSnapshot(
        price=None,
        holdings_pct=None,
        holdings_abs=None,
        advisor_week_id=None,
        snapshot_at=datetime.now(tz=timezone.utc),
    )


def _make_valid_draft(**overrides: object) -> dict[str, object]:
    base: dict[str, object] = {
        "draft_id": str(uuid.uuid4()),
        "ticker": "TSM",
        "intended_action": Action.BUY,
        "draft_reason": "初步想法",
        "env_snapshot": _make_env_snapshot(),
        "conflict_report_ref": None,
        "devils_rebuttal_ref": None,
        "status": DraftStatus.DRAFT,
        "created_at": datetime.now(tz=timezone.utc),
        "committed_at": None,
        "abandoned_at": None,
    }
    base.update(overrides)
    return base


# ── DraftStatus enum 测试 (R2 D8/D13) ────────────────────────────────────────

def test_draft_status_enum_values() -> None:
    """结论: DraftStatus 必含 draft / committed / abandoned。"""
    assert DraftStatus.DRAFT == "draft"
    assert DraftStatus.COMMITTED == "committed"
    assert DraftStatus.ABANDONED == "abandoned"


def test_draft_status_draft_pass() -> None:
    """结论: status='draft' 合法 (初始态)。"""
    d = DecisionDraft(**_make_valid_draft(status=DraftStatus.DRAFT))
    assert d.status == DraftStatus.DRAFT


def test_draft_status_committed_pass() -> None:
    """结论: status='committed' 合法 (commit 后)。"""
    d = DecisionDraft(**_make_valid_draft(status=DraftStatus.COMMITTED))
    assert d.status == DraftStatus.COMMITTED


def test_draft_status_abandoned_pass() -> None:
    """结论: status='abandoned' 合法 (GC 后)。"""
    d = DecisionDraft(**_make_valid_draft(status=DraftStatus.ABANDONED))
    assert d.status == DraftStatus.ABANDONED


def test_draft_status_invalid_raises() -> None:
    """结论: 非法 status 应触发 ValidationError。"""
    with pytest.raises(ValidationError):
        DecisionDraft(**_make_valid_draft(status="pending"))  # type: ignore[arg-type]


# ── draft_reason 长度测试 ─────────────────────────────────────────────────────

def test_draft_reason_80_chars_pass() -> None:
    """结论: draft_reason 恰好 80 字符不报错。"""
    d = DecisionDraft(**_make_valid_draft(draft_reason="B" * 80))
    assert len(d.draft_reason) == 80


def test_draft_reason_81_chars_raises() -> None:
    """结论: draft_reason > 80 字符应触发 ValidationError。"""
    with pytest.raises(ValidationError, match="80"):
        DecisionDraft(**_make_valid_draft(draft_reason="B" * 81))


def test_draft_reason_empty_raises() -> None:
    """结论: draft_reason 为空应触发 ValidationError。"""
    with pytest.raises(ValidationError):
        DecisionDraft(**_make_valid_draft(draft_reason=""))


# ── intended_action 测试 ─────────────────────────────────────────────────────

def test_draft_intended_action_invalid_raises() -> None:
    """结论: 非法 intended_action 应触发 ValidationError。"""
    with pytest.raises(ValidationError):
        DecisionDraft(**_make_valid_draft(intended_action="yolo"))  # type: ignore[arg-type]


def test_draft_intended_action_hold_pass() -> None:
    """结论: intended_action='hold' 合法 (不变量 #3)。"""
    d = DecisionDraft(**_make_valid_draft(intended_action=Action.HOLD))
    assert d.intended_action == Action.HOLD


# ── Watchlist.market enum 测试 (R2 D24) ────────────────────────────────────

def test_watchlist_market_us_default() -> None:
    """结论: Watchlist.market 默认 'US' (D24)。"""
    w = Watchlist(ticker="TSM")
    assert w.market == Market.US


def test_watchlist_market_hk_pass() -> None:
    """结论: market='HK' 合法。"""
    w = Watchlist(ticker="0700.HK", market=Market.HK)
    assert w.market == Market.HK


def test_watchlist_market_cn_pass() -> None:
    """结论: market='CN' 合法。"""
    w = Watchlist(ticker="000001.SZ", market=Market.CN)
    assert w.market == Market.CN


def test_watchlist_market_invalid_raises() -> None:
    """结论: market 不在 {US, HK, CN} 应触发 ValidationError (D24)。"""
    with pytest.raises(ValidationError):
        Watchlist(ticker="TSM", market="JP")  # type: ignore[arg-type]


# ── draft 可选 refs 测试 (INSERT 时 NULL 合法) ───────────────────────────────

def test_draft_refs_nullable() -> None:
    """结论: conflict_report_ref / devils_rebuttal_ref INSERT 时可为 None。"""
    d = DecisionDraft(**_make_valid_draft(
        conflict_report_ref=None,
        devils_rebuttal_ref=None,
    ))
    assert d.conflict_report_ref is None
    assert d.devils_rebuttal_ref is None


def test_draft_refs_set_after_asyncio() -> None:
    """结论: asyncio.gather 完成后 refs 可填入 UUID 字符串。"""
    ref = str(uuid.uuid4())
    d = DecisionDraft(**_make_valid_draft(
        conflict_report_ref=ref,
        devils_rebuttal_ref=ref,
    ))
    assert d.conflict_report_ref == ref
    assert d.devils_rebuttal_ref == ref
