"""
WeeklyReviewService 集成测试 — T014
结论: 验证周报聚合 SQL + hold/wait 不动占比 + 维护工时填报 (R11 不动专区独立)
细节:
  - test_generate_counts_5_decisions: seed 5 决策 → generate 返回 total=5
  - test_generate_hold_wait_ratio: hold+wait 占比正确计算 (R11 不动专区)
  - test_log_maintenance_hours: POST 工时 → 数据库写入 + 4 周平均计算
  - test_rolling_avg_4_weeks: 4 条工时记录 → 正确计算滚动平均
  - test_llm_summary_fallback: LLM 失败时 fallback 到 None 摘要 (不阻塞)
  - test_maintenance_hours_op4_threshold: 工时 ≥ 3h 时 over_threshold=True (OP-4)
"""

from __future__ import annotations

import os
import subprocess
import sys
from collections.abc import AsyncIterator
from datetime import UTC, datetime
from pathlib import Path
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
import pytest_asyncio

from decision_ledger.repository.base import AsyncConnectionPool

PROJECT_ROOT = Path(__file__).resolve().parents[3]


@pytest_asyncio.fixture
async def migrated_pool(tmp_path: Path) -> AsyncIterator[AsyncConnectionPool]:
    """提供经过 alembic upgrade head 迁移的 AsyncConnectionPool。"""
    db_path = tmp_path / "test_weekly.sqlite"
    db_url = f"sqlite:///{db_path}"

    env = {
        **os.environ,
        "DECISION_LEDGER_DB_URL": db_url,
        "ANTHROPIC_API_KEY": os.environ.get("ANTHROPIC_API_KEY", "test-key-placeholder"),
        "TELEGRAM_BOT_TOKEN": os.environ.get("TELEGRAM_BOT_TOKEN", "test-token-placeholder"),
    }
    result = subprocess.run(  # noqa: S603
        [sys.executable, "-m", "alembic", "upgrade", "head"],
        cwd=str(PROJECT_ROOT),
        env=env,
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, f"alembic upgrade 失败: {result.stderr}"

    pool = AsyncConnectionPool(str(db_path))
    await pool.initialize()
    try:
        yield pool
    finally:
        await pool.close()


async def _seed_conflict_and_rebuttal(pool: AsyncConnectionPool) -> tuple[str, str]:
    """插入 conflict_report + rebuttal 以满足 decisions FK 约束。"""
    conflict_id = str(uuid4())
    rebuttal_id = str(uuid4())

    async with pool.write_connection() as conn:
        await conn.execute(
            """
            INSERT INTO conflict_reports (
                report_id, divergence_root_cause, has_divergence,
                rendered_order_seed, signals_json, created_at
            ) VALUES (?, ?, ?, ?, ?, ?)
            """,
            (conflict_id, "test root cause", 0, 3, "[]", datetime.now(tz=UTC).isoformat()),
        )
        await conn.execute(
            """
            INSERT INTO rebuttals (rebuttal_id, rebuttal_text, invoked_at)
            VALUES (?, ?, ?)
            """,
            (rebuttal_id, "test rebuttal", datetime.now(tz=UTC).isoformat()),
        )
        await conn.commit()

    return conflict_id, rebuttal_id


async def _seed_decision(
    pool: AsyncConnectionPool,
    action: str,
    conflict_id: str,
    rebuttal_id: str,
    week_str: str = "2026-04-21",
) -> str:
    """插入一条 Decision 到数据库。"""
    trade_id = str(uuid4())
    env_json = (
        '{"price": 100.0, "holdings_pct": null, "holdings_abs": null,'
        ' "advisor_week_id": null, "snapshot_at": "2026-04-21T10:00:00+00:00"}'
    )

    async with pool.write_connection() as conn:
        await conn.execute(
            """
            INSERT INTO decisions (
                trade_id, ticker, action, reason, pre_commit_at,
                env_snapshot_json, conflict_report_ref, devils_rebuttal_ref,
                post_mortem_json, would_have_acted_without_agent, status,
                created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                trade_id,
                "AAPL",
                action,
                f"reason {action[:5]}",
                f"{week_str}T10:00:00+00:00",
                env_json,
                conflict_id,
                rebuttal_id,
                None,
                0,
                "committed",
                datetime.now(tz=UTC).isoformat(),
                datetime.now(tz=UTC).isoformat(),
            ),
        )
        await conn.commit()

    return trade_id


async def test_generate_counts_5_decisions_when_seeded(migrated_pool: AsyncConnectionPool) -> None:
    """should count 5 decisions when 5 are seeded for the target week."""
    from decision_ledger.services.weekly_review_service import WeeklyReviewService

    conflict_id, rebuttal_id = await _seed_conflict_and_rebuttal(migrated_pool)

    # seed 5 决策
    for action in ["buy", "sell", "hold", "wait", "hold"]:
        await _seed_decision(migrated_pool, action, conflict_id, rebuttal_id, "2026-04-21")

    svc = WeeklyReviewService(pool=migrated_pool, llm_client=None)
    result = await svc.generate(week_id="2026-W17")

    assert result["total_decisions"] == 5


async def test_generate_hold_wait_ratio_when_3_of_5_inactive(
    migrated_pool: AsyncConnectionPool,
) -> None:
    """should show hold+wait ratio = 60% when 3 of 5 decisions are hold/wait (R11)."""
    from decision_ledger.services.weekly_review_service import WeeklyReviewService

    conflict_id, rebuttal_id = await _seed_conflict_and_rebuttal(migrated_pool)

    # 2 buy/sell + 3 hold/wait
    for action in ["buy", "sell", "hold", "wait", "hold"]:
        await _seed_decision(migrated_pool, action, conflict_id, rebuttal_id, "2026-04-21")

    svc = WeeklyReviewService(pool=migrated_pool, llm_client=None)
    result = await svc.generate(week_id="2026-W17")

    assert result["hold_wait_count"] == 3
    assert result["inactive_ratio"] == pytest.approx(0.6, abs=0.01)


async def test_generate_action_breakdown_when_mixed_actions(
    migrated_pool: AsyncConnectionPool,
) -> None:
    """should break down decisions by action when multiple actions seeded."""
    from decision_ledger.services.weekly_review_service import WeeklyReviewService

    conflict_id, rebuttal_id = await _seed_conflict_and_rebuttal(migrated_pool)

    for action in ["buy", "sell", "hold", "wait", "buy"]:
        await _seed_decision(migrated_pool, action, conflict_id, rebuttal_id, "2026-04-21")

    svc = WeeklyReviewService(pool=migrated_pool, llm_client=None)
    result = await svc.generate(week_id="2026-W17")

    breakdown = result["action_breakdown"]
    assert breakdown.get("buy", 0) == 2
    assert breakdown.get("sell", 0) == 1
    assert breakdown.get("hold", 0) == 1
    assert breakdown.get("wait", 0) == 1


async def test_log_maintenance_hours_when_valid_input(
    migrated_pool: AsyncConnectionPool,
) -> None:
    """should persist maintenance hours when called with valid hours."""
    from decision_ledger.services.weekly_review_service import WeeklyReviewService

    svc = WeeklyReviewService(pool=migrated_pool, llm_client=None)
    await svc.log_maintenance_hours(week_id="2026-W17", hours=3.5)

    async with migrated_pool.connection() as conn:
        cursor = await conn.execute(
            "SELECT hours FROM weekly_maintenance_log WHERE week_id = ?",
            ("2026-W17",),
        )
        row = await cursor.fetchone()

    assert row is not None
    assert float(row["hours"]) == pytest.approx(3.5)


async def test_rolling_avg_4_weeks_when_4_entries(
    migrated_pool: AsyncConnectionPool,
) -> None:
    """should compute 4-week rolling average correctly when 4 entries exist."""
    from decision_ledger.services.weekly_review_service import WeeklyReviewService

    svc = WeeklyReviewService(pool=migrated_pool, llm_client=None)

    # 写入 4 周工时: 2.0, 3.0, 4.0, 1.0 → 平均 2.5
    for week, hours in [
        ("2026-W14", 2.0),
        ("2026-W15", 3.0),
        ("2026-W16", 4.0),
        ("2026-W17", 1.0),
    ]:
        await svc.log_maintenance_hours(week_id=week, hours=hours)

    rolling_avg = await svc.get_rolling_avg_hours(current_week_id="2026-W17", weeks=4)
    assert rolling_avg == pytest.approx(2.5, abs=0.01)


async def test_maintenance_hours_over_threshold_when_gte_3h(
    migrated_pool: AsyncConnectionPool,
) -> None:
    """should set over_threshold=True when hours >= 3 (OP-4 mitigation)."""
    from decision_ledger.services.weekly_review_service import WeeklyReviewService

    svc = WeeklyReviewService(pool=migrated_pool, llm_client=None)
    await svc.log_maintenance_hours(week_id="2026-W17", hours=4.0)

    result = await svc.generate(week_id="2026-W17")
    maint = result["maintenance"]

    assert maint["current_hours"] == pytest.approx(4.0)
    assert maint["over_threshold"] is True


async def test_maintenance_hours_not_over_threshold_when_lt_3h(
    migrated_pool: AsyncConnectionPool,
) -> None:
    """should set over_threshold=False when hours < 3 (OP-4 threshold)."""
    from decision_ledger.services.weekly_review_service import WeeklyReviewService

    svc = WeeklyReviewService(pool=migrated_pool, llm_client=None)
    await svc.log_maintenance_hours(week_id="2026-W17", hours=2.0)

    result = await svc.generate(week_id="2026-W17")
    maint = result["maintenance"]

    assert maint["current_hours"] == pytest.approx(2.0)
    assert maint["over_threshold"] is False


async def test_llm_summary_fallback_when_llm_fails(
    migrated_pool: AsyncConnectionPool,
) -> None:
    """should fallback to None summary when LLM client raises exception (不阻塞)."""
    from decision_ledger.services.weekly_review_service import WeeklyReviewService

    mock_llm = AsyncMock()
    mock_llm.call = AsyncMock(side_effect=Exception("LLM timeout"))

    svc = WeeklyReviewService(pool=migrated_pool, llm_client=mock_llm)
    result = await svc.generate(week_id="2026-W17")

    # LLM 失败时摘要为 None，不抛出异常
    assert result["llm_summary"] is None


async def test_generate_zero_decisions_when_empty_week(
    migrated_pool: AsyncConnectionPool,
) -> None:
    """should return zero counts when no decisions exist for the week."""
    from decision_ledger.services.weekly_review_service import WeeklyReviewService

    svc = WeeklyReviewService(pool=migrated_pool, llm_client=None)
    result = await svc.generate(week_id="2026-W17")

    assert result["total_decisions"] == 0
    assert result["hold_wait_count"] == 0
    assert result["inactive_ratio"] == 0.0


async def test_generate_llm_cost_aggregation_when_usage_exists(
    migrated_pool: AsyncConnectionPool,
) -> None:
    """should aggregate LLM cost from llm_usage table for the week."""
    from decision_ledger.services.weekly_review_service import WeeklyReviewService

    async with migrated_pool.write_connection() as conn:
        await conn.execute(
            """
            INSERT INTO llm_usage (
                call_id, service, model, prompt_template_version,
                prompt_tokens, output_tokens, cost_usd, cache_hit, latency_ms, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                str(uuid4()),
                "WeeklyReviewService",
                "claude-sonnet-4-6",
                "weekly_review_v1",
                100,
                50,
                0.005,
                0,
                500,
                "2026-04-21T10:00:00+00:00",
            ),
        )
        await conn.commit()

    svc = WeeklyReviewService(pool=migrated_pool, llm_client=None)
    result = await svc.generate(week_id="2026-W17")

    assert result["llm_cost_usd"] == pytest.approx(0.005, abs=1e-6)
