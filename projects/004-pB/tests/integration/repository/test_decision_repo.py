"""
DecisionRepository 集成测试 — T003
结论: 验证 Decision CRUD + 领域查询方法的正确性
细节:
  - happy path: insert → get → list 正向流程
  - negative: get 不存在的 trade_id 返回 None
  - post_mortem update / conflict_ref update / rebuttal_ref update
  - count_since / list_by_action / list_by_ticker 查询
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from uuid import uuid4

import pytest

from decision_ledger.domain.conflict_report import ConflictReport
from decision_ledger.domain.decision import Action, Decision, DecisionStatus, PostMortem
from decision_ledger.domain.env_snapshot import EnvSnapshot
from decision_ledger.domain.rebuttal import Rebuttal
from decision_ledger.domain.strategy_signal import Direction, StrategySignal
from decision_ledger.repository.base import AsyncConnectionPool
from decision_ledger.repository.conflict_repo import ConflictRepository
from decision_ledger.repository.decision_repo import DecisionRepository
from decision_ledger.repository.rebuttal_repo import RebuttalRepository


async def _seed_conflict_and_rebuttal(pool: AsyncConnectionPool) -> tuple[str, str]:
    """先创建 conflict_report + rebuttal 记录满足 decisions FK 约束。

    结论: decisions 表对 conflict_report_ref / devils_rebuttal_ref NOT NULL+FK,
    test 必须先插 parent 行才能 insert decision。
    """
    conflict_id = str(uuid4())
    rebuttal_id = str(uuid4())
    signals = [
        StrategySignal(
            source_id="advisor",
            ticker="AAPL",
            direction=Direction.LONG,
            confidence=0.7,
            rationale_plain="test rationale 1",
            inputs_used={"source": "test"},
        ),
        StrategySignal(
            source_id="watchlist_v1",
            ticker="AAPL",
            direction=Direction.LONG,
            confidence=0.6,
            rationale_plain="test rationale 2",
            inputs_used={"source": "test"},
        ),
        StrategySignal(
            source_id="contrarian_v1",
            ticker="AAPL",
            direction=Direction.SHORT,
            confidence=0.5,
            rationale_plain="test rationale 3",
            inputs_used={"source": "test"},
        ),
    ]
    cr = ConflictReport(
        signals=signals,
        divergence_root_cause="测试分歧",
        has_divergence=True,
        rendered_order_seed=0,
    )
    rb = Rebuttal(
        rebuttal_text="test rebuttal text",
        invoked_at=datetime.now(tz=UTC).isoformat(),
    )
    await ConflictRepository(pool).insert(conflict_id, cr)
    await RebuttalRepository(pool).insert(rebuttal_id, rb)
    return conflict_id, rebuttal_id


def _make_env_snapshot() -> EnvSnapshot:
    """构造测试用 EnvSnapshot。"""
    return EnvSnapshot(
        price=100.0,
        holdings_pct=0.05,
        holdings_abs=5000.0,
        advisor_week_id="2026-W17",
        snapshot_at=datetime.now(tz=UTC),
    )


def _make_decision(
    *,
    conflict_id: str,
    rebuttal_id: str,
    ticker: str = "AAPL",
    action: Action = Action.BUY,
    would_have_acted: bool = True,
    pre_commit_at: datetime | None = None,
) -> Decision:
    """构造测试用 Decision。

    结论: conflict_id/rebuttal_id 必须先入库(_seed_conflict_and_rebuttal),
    否则 FK 约束失败。
    """
    return Decision(
        trade_id=str(uuid4()),
        ticker=ticker,
        action=action,
        reason="Test reason ok",
        pre_commit_at=pre_commit_at or datetime.now(tz=UTC),
        env_snapshot=_make_env_snapshot(),
        conflict_report_ref=conflict_id,
        devils_rebuttal_ref=rebuttal_id,
        would_have_acted_without_agent=would_have_acted,
        status=DecisionStatus.COMMITTED,
    )


@pytest.mark.asyncio
async def test_insert_and_get_should_round_trip_when_decision_is_valid(
    migrated_pool: AsyncConnectionPool,
) -> None:
    """结论: insert 后 get 应返回字段完全相同的 Decision 对象。"""
    conflict_id, rebuttal_id = await _seed_conflict_and_rebuttal(migrated_pool)
    repo = DecisionRepository(migrated_pool)
    decision = _make_decision(conflict_id=conflict_id, rebuttal_id=rebuttal_id)
    await repo.insert(decision)

    fetched = await repo.get(decision.trade_id)
    assert fetched is not None
    assert fetched.trade_id == decision.trade_id
    assert fetched.ticker == decision.ticker
    assert fetched.action == decision.action
    assert fetched.reason == decision.reason
    assert fetched.would_have_acted_without_agent == decision.would_have_acted_without_agent
    assert fetched.conflict_report_ref == decision.conflict_report_ref
    assert fetched.devils_rebuttal_ref == decision.devils_rebuttal_ref


@pytest.mark.asyncio
async def test_get_should_return_none_when_trade_id_does_not_exist(
    migrated_pool: AsyncConnectionPool,
) -> None:
    """结论: 查询不存在的 trade_id 应返回 None，不抛出异常。"""
    repo = DecisionRepository(migrated_pool)
    result = await repo.get("nonexistent-trade-id")
    assert result is None


@pytest.mark.asyncio
async def test_update_post_mortem_should_persist_when_called(
    migrated_pool: AsyncConnectionPool,
) -> None:
    """结论: update_post_mortem 后查询应包含 post_mortem 字段。"""
    conflict_id, rebuttal_id = await _seed_conflict_and_rebuttal(migrated_pool)
    repo = DecisionRepository(migrated_pool)
    decision = _make_decision(conflict_id=conflict_id, rebuttal_id=rebuttal_id)
    await repo.insert(decision)

    post_mortem = PostMortem(
        executed_at=datetime.now(tz=UTC),
        result_pct_after_7d=2.5,
        result_pct_after_30d=5.0,
        retrospective_notes="测试回顾",
    )
    await repo.update_post_mortem(decision.trade_id, post_mortem)

    fetched = await repo.get(decision.trade_id)
    assert fetched is not None
    assert fetched.post_mortem is not None
    assert fetched.post_mortem.result_pct_after_7d == 2.5
    assert fetched.post_mortem.retrospective_notes == "测试回顾"


@pytest.mark.asyncio
async def test_update_conflict_ref_should_persist_when_called(
    migrated_pool: AsyncConnectionPool,
) -> None:
    """结论: update_conflict_ref 后查询应包含更新后的 conflict_report_ref。"""
    conflict_id, rebuttal_id = await _seed_conflict_and_rebuttal(migrated_pool)
    repo = DecisionRepository(migrated_pool)
    decision = _make_decision(conflict_id=conflict_id, rebuttal_id=rebuttal_id)
    await repo.insert(decision)

    # 新 conflict 也需先入库
    new_conflict_id, _ = await _seed_conflict_and_rebuttal(migrated_pool)
    await repo.update_conflict_ref(decision.trade_id, new_conflict_id)

    fetched = await repo.get(decision.trade_id)
    assert fetched is not None
    assert fetched.conflict_report_ref == new_conflict_id


@pytest.mark.asyncio
async def test_update_rebuttal_ref_should_persist_when_called(
    migrated_pool: AsyncConnectionPool,
) -> None:
    """结论: update_rebuttal_ref 后查询应包含更新后的 devils_rebuttal_ref。"""
    conflict_id, rebuttal_id = await _seed_conflict_and_rebuttal(migrated_pool)
    repo = DecisionRepository(migrated_pool)
    decision = _make_decision(conflict_id=conflict_id, rebuttal_id=rebuttal_id)
    await repo.insert(decision)

    _, new_rebuttal_id = await _seed_conflict_and_rebuttal(migrated_pool)
    await repo.update_rebuttal_ref(decision.trade_id, new_rebuttal_id)

    fetched = await repo.get(decision.trade_id)
    assert fetched is not None
    assert fetched.devils_rebuttal_ref == new_rebuttal_id


@pytest.mark.asyncio
async def test_count_since_should_count_decisions_within_days(
    migrated_pool: AsyncConnectionPool,
) -> None:
    """结论: count_since(7) 应仅计算最近 7 天内的 decisions。"""
    conflict_id, rebuttal_id = await _seed_conflict_and_rebuttal(migrated_pool)
    repo = DecisionRepository(migrated_pool)

    # 插入 2 条最近 7 天内的
    for _ in range(2):
        await repo.insert(
            _make_decision(
                conflict_id=conflict_id,
                rebuttal_id=rebuttal_id,
                pre_commit_at=datetime.now(tz=UTC),
            )
        )

    # 插入 1 条 30 天前的(应不计入)
    old_decision = _make_decision(
        conflict_id=conflict_id,
        rebuttal_id=rebuttal_id,
        pre_commit_at=datetime.now(tz=UTC) - timedelta(days=30),
    )
    await repo.insert(old_decision)

    count = await repo.count_since(7)
    assert count == 2


@pytest.mark.asyncio
async def test_list_by_action_should_filter_by_action(
    migrated_pool: AsyncConnectionPool,
) -> None:
    """结论: list_by_action('buy') 应仅返回 action=buy 的 decisions。"""
    conflict_id, rebuttal_id = await _seed_conflict_and_rebuttal(migrated_pool)
    repo = DecisionRepository(migrated_pool)
    kw = {"conflict_id": conflict_id, "rebuttal_id": rebuttal_id}

    await repo.insert(_make_decision(action=Action.BUY, **kw))
    await repo.insert(_make_decision(action=Action.BUY, **kw))
    await repo.insert(_make_decision(action=Action.HOLD, **kw))

    buy_decisions = await repo.list_by_action(Action.BUY)
    hold_decisions = await repo.list_by_action(Action.HOLD)

    assert len(buy_decisions) == 2
    assert len(hold_decisions) == 1
    assert all(d.action == Action.BUY for d in buy_decisions)


@pytest.mark.asyncio
async def test_list_by_ticker_should_filter_by_ticker(
    migrated_pool: AsyncConnectionPool,
) -> None:
    """结论: list_by_ticker('AAPL') 应仅返回 ticker=AAPL 的 decisions。"""
    conflict_id, rebuttal_id = await _seed_conflict_and_rebuttal(migrated_pool)
    repo = DecisionRepository(migrated_pool)
    kw = {"conflict_id": conflict_id, "rebuttal_id": rebuttal_id}

    await repo.insert(_make_decision(ticker="AAPL", **kw))
    await repo.insert(_make_decision(ticker="AAPL", **kw))
    await repo.insert(_make_decision(ticker="TSLA", **kw))

    aapl = await repo.list_by_ticker("AAPL")
    tsla = await repo.list_by_ticker("TSLA")

    assert len(aapl) == 2
    assert len(tsla) == 1
    assert all(d.ticker == "AAPL" for d in aapl)


@pytest.mark.asyncio
async def test_count_would_have_acted_without_agent_should_count_true_only(
    migrated_pool: AsyncConnectionPool,
) -> None:
    """结论: count_would_have_acted_without_agent 应仅计 True 的条目。"""
    conflict_id, rebuttal_id = await _seed_conflict_and_rebuttal(migrated_pool)
    repo = DecisionRepository(migrated_pool)
    kw = {"conflict_id": conflict_id, "rebuttal_id": rebuttal_id}

    await repo.insert(_make_decision(would_have_acted=True, **kw))
    await repo.insert(_make_decision(would_have_acted=True, **kw))
    await repo.insert(_make_decision(would_have_acted=False, **kw))

    count = await repo.count_would_have_acted_without_agent()
    assert count == 2
