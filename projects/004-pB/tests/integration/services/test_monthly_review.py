"""
MonthlyReviewService 集成测试 — T015 (R3 简化版)
结论: 验证月度 review 聚合 SQL + 4 section 内容 + 样本不足 placeholder + 无 LLM 调用
细节:
  - test_generate_returns_4_sections_when_month_seeded:
      seed 1 个月数据 → generate 返回含 4 section 的 dict
  - test_generate_committed_only_when_mixed_status:
      draft 决策不计入统计 (status='committed' only, R2)
  - test_generate_hold_wait_ratio_when_some_inactive:
      hold+wait 不动占比正确
  - test_generate_would_have_acted_count_when_seeded:
      would_have_acted_without_agent=1 的计数
  - test_generate_insufficient_sample_placeholder_when_first_month:
      首月时 benchmark_placeholder 含 "样本" 字样 (Q1 mitigation)
  - test_generate_no_llm_call_when_called (R3 cut 验证):
      generate() 路径 LLM call 计数 = 0
  - test_generate_risk_snapshot_contains_4_risks:
      风险快照包含 OP-1 / OP-2 / TECH-2 / O10 四条
"""

from __future__ import annotations

import ast
import os
import subprocess
import sys
from collections.abc import AsyncIterator
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

import pytest
import pytest_asyncio

from decision_ledger.repository.base import AsyncConnectionPool

PROJECT_ROOT = Path(__file__).resolve().parents[3]


@pytest_asyncio.fixture
async def migrated_pool(tmp_path: Path) -> AsyncIterator[AsyncConnectionPool]:
    """提供经过 alembic upgrade head 迁移的 AsyncConnectionPool。"""
    db_path = tmp_path / "test_monthly.sqlite"
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
    date_str: str = "2026-04-15",
    status: str = "committed",
    would_have_acted: int = 0,
) -> str:
    """插入一条 Decision 到数据库 (month=2026-04)。"""
    trade_id = str(uuid4())
    env_json = (
        '{"price": 100.0, "holdings_pct": null, "holdings_abs": null,'
        ' "advisor_week_id": null, "snapshot_at": "2026-04-15T10:00:00+00:00"}'
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
                f"{date_str}T10:00:00+00:00",
                env_json,
                conflict_id,
                rebuttal_id,
                None,
                would_have_acted,
                status,
                datetime.now(tz=UTC).isoformat(),
                datetime.now(tz=UTC).isoformat(),
            ),
        )
        await conn.commit()

    return trade_id


async def test_generate_returns_4_sections_when_month_seeded(
    migrated_pool: AsyncConnectionPool,
) -> None:
    """should return dict with 4 sections when month data is seeded."""
    from decision_ledger.services.monthly_review_service import MonthlyReviewService

    conflict_id, rebuttal_id = await _seed_conflict_and_rebuttal(migrated_pool)

    for action in ["buy", "sell", "hold", "wait"]:
        await _seed_decision(migrated_pool, action, conflict_id, rebuttal_id)

    svc = MonthlyReviewService(pool=migrated_pool)
    result = await svc.generate(month_id="2026-04")

    # 4 sections 必须存在
    assert "calibration" in result, "section 1: 校准证据聚合 (calibration) 缺失"
    assert "matrix_snapshot" in result, "section 2: 错位矩阵快照 (matrix_snapshot) 缺失"
    assert "risk_snapshot" in result, "section 3: 风险快照 (risk_snapshot) 缺失"
    assert "benchmark_placeholder" in result, "section 4: 12 月对标 placeholder 缺失"


async def test_generate_committed_only_when_mixed_status(
    migrated_pool: AsyncConnectionPool,
) -> None:
    """should count only committed decisions when draft decisions exist (R2)."""
    from decision_ledger.services.monthly_review_service import MonthlyReviewService

    conflict_id, rebuttal_id = await _seed_conflict_and_rebuttal(migrated_pool)

    # 2 committed + 1 draft
    await _seed_decision(migrated_pool, "buy", conflict_id, rebuttal_id, status="committed")
    await _seed_decision(migrated_pool, "sell", conflict_id, rebuttal_id, status="committed")
    await _seed_decision(migrated_pool, "hold", conflict_id, rebuttal_id, status="draft")

    svc = MonthlyReviewService(pool=migrated_pool)
    result = await svc.generate(month_id="2026-04")

    # draft 不算入月度统计
    assert result["calibration"]["total_committed"] == 2


async def test_generate_hold_wait_ratio_when_some_inactive(
    migrated_pool: AsyncConnectionPool,
) -> None:
    """should compute hold+wait ratio correctly when some decisions are inactive."""
    from decision_ledger.services.monthly_review_service import MonthlyReviewService

    conflict_id, rebuttal_id = await _seed_conflict_and_rebuttal(migrated_pool)

    # 3 active (buy/sell) + 2 inactive (hold/wait)
    for action in ["buy", "sell", "buy", "hold", "wait"]:
        await _seed_decision(migrated_pool, action, conflict_id, rebuttal_id)

    svc = MonthlyReviewService(pool=migrated_pool)
    result = await svc.generate(month_id="2026-04")

    cal = result["calibration"]
    assert cal["total_committed"] == 5
    assert cal["inactive_count"] == 2  # hold + wait
    # 不动占比 = 2/5 = 0.4
    assert cal["inactive_ratio"] == pytest.approx(0.4, abs=0.01)


async def test_generate_would_have_acted_count_when_seeded(
    migrated_pool: AsyncConnectionPool,
) -> None:
    """should count would_have_acted_without_agent=1 decisions correctly."""
    from decision_ledger.services.monthly_review_service import MonthlyReviewService

    conflict_id, rebuttal_id = await _seed_conflict_and_rebuttal(migrated_pool)

    # 2 would_have_acted=1, 1 would_have_acted=0
    await _seed_decision(migrated_pool, "buy", conflict_id, rebuttal_id, would_have_acted=1)
    await _seed_decision(migrated_pool, "sell", conflict_id, rebuttal_id, would_have_acted=1)
    await _seed_decision(migrated_pool, "hold", conflict_id, rebuttal_id, would_have_acted=0)

    svc = MonthlyReviewService(pool=migrated_pool)
    result = await svc.generate(month_id="2026-04")

    assert result["calibration"]["would_have_acted_count"] == 2


async def test_generate_insufficient_sample_placeholder_when_first_month(
    migrated_pool: AsyncConnectionPool,
) -> None:
    """should show insufficient sample text when data is for first month only (Q1)."""
    from decision_ledger.services.monthly_review_service import MonthlyReviewService

    conflict_id, rebuttal_id = await _seed_conflict_and_rebuttal(migrated_pool)
    await _seed_decision(migrated_pool, "buy", conflict_id, rebuttal_id)

    svc = MonthlyReviewService(pool=migrated_pool)
    result = await svc.generate(month_id="2026-04")

    # 仅 1 个月数据 → placeholder 含"样本"字样
    placeholder = result["benchmark_placeholder"]
    assert "样本" in placeholder, f"placeholder 应含'样本', 实际: {placeholder!r}"


async def test_generate_risk_snapshot_contains_4_risks(
    migrated_pool: AsyncConnectionPool,
) -> None:
    """should include OP-1 / OP-2 / TECH-2 / O10 in risk snapshot (static 4 rows)."""
    from decision_ledger.services.monthly_review_service import MonthlyReviewService

    svc = MonthlyReviewService(pool=migrated_pool)
    result = await svc.generate(month_id="2026-04")

    risk_snapshot = result["risk_snapshot"]
    assert isinstance(risk_snapshot, list), "risk_snapshot 应为 list"
    risk_ids = {r["id"] for r in risk_snapshot}
    assert "OP-1" in risk_ids, "OP-1 缺失"
    assert "OP-2" in risk_ids, "OP-2 缺失"
    assert "TECH-2" in risk_ids, "TECH-2 缺失"
    assert "O10" in risk_ids, "O10 缺失"


async def test_generate_no_llm_call_when_called(
    migrated_pool: AsyncConnectionPool,
) -> None:
    """should make zero LLM calls in generate() path (R3 cut verification)."""
    from decision_ledger.services.monthly_review_service import MonthlyReviewService

    svc = MonthlyReviewService(pool=migrated_pool)
    result = await svc.generate(month_id="2026-04")

    # R3 cut: generate 不调 LLM
    assert result is not None  # 正常返回

    # 验证 monthly_review_service.py 源码不含 LLMClient import
    svc_path = Path(__file__).resolve().parents[3] / "src" / "decision_ledger" / "services" / "monthly_review_service.py"
    source = svc_path.read_text()
    assert "LLMClient" not in source, "R3 cut: monthly_review_service.py 不应 import LLMClient"


async def test_generate_signature_has_no_audience_param(
    migrated_pool: AsyncConnectionPool,
) -> None:
    """should not have audience parameter in generate() signature (R2 M5)."""
    from decision_ledger.services.monthly_review_service import MonthlyReviewService
    import inspect

    sig = inspect.signature(MonthlyReviewService.generate)
    assert "audience" not in sig.parameters, "R2 M5: generate() 不应含 audience 参数"


async def test_generate_matrix_snapshot_is_present(
    migrated_pool: AsyncConnectionPool,
) -> None:
    """should include matrix_snapshot section in result."""
    from decision_ledger.services.monthly_review_service import MonthlyReviewService

    svc = MonthlyReviewService(pool=migrated_pool)
    result = await svc.generate(month_id="2026-04")

    # 错位矩阵快照字段存在 (可以是空 list 或 dict)
    assert "matrix_snapshot" in result


async def test_generate_zero_decisions_when_empty_month(
    migrated_pool: AsyncConnectionPool,
) -> None:
    """should return zero total_committed when no decisions in the month."""
    from decision_ledger.services.monthly_review_service import MonthlyReviewService

    svc = MonthlyReviewService(pool=migrated_pool)
    result = await svc.generate(month_id="2026-04")

    assert result["calibration"]["total_committed"] == 0
    assert result["calibration"]["inactive_ratio"] == 0.0
    assert result["calibration"]["would_have_acted_count"] == 0
