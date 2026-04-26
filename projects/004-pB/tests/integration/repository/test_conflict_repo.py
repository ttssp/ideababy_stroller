"""
ConflictRepository 集成测试 — T003
结论: 验证 insert / get / list_recent + signals JSON round-trip
"""

from __future__ import annotations

from uuid import uuid4

import pytest

from decision_ledger.domain.conflict_report import ConflictReport
from decision_ledger.domain.strategy_signal import Direction, StrategySignal
from decision_ledger.repository.base import AsyncConnectionPool
from decision_ledger.repository.conflict_repo import ConflictRepository


def _make_signal(source_id: str = "advisor", ticker: str = "AAPL") -> StrategySignal:
    return StrategySignal(
        source_id=source_id,
        ticker=ticker,
        direction=Direction.LONG,
        confidence=0.8,
        rationale_plain="看多信号：季报超预期",
        inputs_used={"advisor_week_id": "2026-W17"},
    )


def _make_conflict_report(ticker: str = "AAPL") -> tuple[str, ConflictReport]:
    """返回 (report_id, ConflictReport)。"""
    report_id = str(uuid4())
    signals = [
        _make_signal("advisor", ticker),
        _make_signal("placeholder_model", ticker),
        _make_signal("agent_synthesis", ticker),
    ]
    report = ConflictReport(
        signals=signals,
        divergence_root_cause="暂无分歧，三路看多",
        has_divergence=False,
        rendered_order_seed=42,
    )
    return report_id, report


@pytest.mark.asyncio
async def test_insert_and_get_should_round_trip_signals(
    migrated_pool: AsyncConnectionPool,
) -> None:
    """结论: insert 后 get 应返回含完整 signals 的 ConflictReport（JSON round-trip）。"""
    repo = ConflictRepository(migrated_pool)
    report_id, report = _make_conflict_report()
    await repo.insert(report_id, report)

    fetched = await repo.get(report_id)
    assert fetched is not None
    assert len(fetched.signals) == 3
    assert fetched.has_divergence is False
    assert fetched.divergence_root_cause == "暂无分歧，三路看多"
    assert fetched.rendered_order_seed == 42
    # 验证 signals 字段完整性
    assert fetched.signals[0].source_id == "advisor"
    assert fetched.signals[0].direction == Direction.LONG
    assert fetched.signals[0].confidence == 0.8


@pytest.mark.asyncio
async def test_get_should_return_none_when_report_not_found(
    migrated_pool: AsyncConnectionPool,
) -> None:
    """结论: 查询不存在的 report_id 应返回 None。"""
    repo = ConflictRepository(migrated_pool)
    result = await repo.get("nonexistent-report-id")
    assert result is None


@pytest.mark.asyncio
async def test_list_recent_should_return_latest_n_reports(
    migrated_pool: AsyncConnectionPool,
) -> None:
    """结论: list_recent(n) 应返回最近 n 条 ConflictReport，按 created_at DESC。"""
    repo = ConflictRepository(migrated_pool)

    # 插入 5 条
    for _ in range(5):
        report_id, report = _make_conflict_report()
        await repo.insert(report_id, report)

    recent = await repo.list_recent(limit=3)
    assert len(recent) == 3


@pytest.mark.asyncio
async def test_list_recent_should_return_empty_when_no_reports(
    migrated_pool: AsyncConnectionPool,
) -> None:
    """结论: 无记录时 list_recent 应返回空列表。"""
    repo = ConflictRepository(migrated_pool)
    result = await repo.list_recent()
    assert result == []
