"""
BLiteService 集成测试 — T022
结论: 验证 B-lite 降级路径的核心行为（CLI only，R3 删除 UI toggle）
细节:
  - test_engage_pauses_t010_t015: engage() 后 ConflictWorker.is_paused()=True AND
    MonthlyScheduler.is_paused()=True (R2 H1)
  - test_disengage_in_cooling_off_raises: cooling_off 内 disengage 抛 ValueError
  - test_disengage_after_14d_resumes_all: 14 天后 disengage 成功, hook 都 resume
  - test_decision_recorder_still_works_when_engaged: engage 时 T008 录入仍正常
  - test_weekly_review_still_works_when_engaged: T014 周度 review 不受 pause 影响
  - test_cli_engage_subcommand: CLI engage subcommand 后 is_engaged()=True
"""

from __future__ import annotations

import os
import subprocess
import sys
from collections.abc import AsyncIterator
from datetime import UTC, datetime, timedelta
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
import pytest_asyncio

from decision_ledger.repository.base import AsyncConnectionPool

PROJECT_ROOT = Path(__file__).resolve().parents[3]
SCRIPTS_DIR = PROJECT_ROOT / "scripts"


@pytest_asyncio.fixture
async def migrated_pool(tmp_path: Path) -> AsyncIterator[AsyncConnectionPool]:
    """提供经过 alembic upgrade head 迁移的 AsyncConnectionPool。"""
    db_path = tmp_path / "test_b_lite.sqlite"
    db_url = f"sqlite:///{db_path}"

    env = {
        **os.environ,
        "DECISION_LEDGER_DB_URL": db_url,
        "ANTHROPIC_API_KEY": os.environ.get("ANTHROPIC_API_KEY", "test-key-placeholder"),
        "TELEGRAM_BOT_TOKEN": os.environ.get("TELEGRAM_BOT_TOKEN", "test-token-placeholder"),
    }
    result = subprocess.run(  # noqa: S603
        [sys.executable, "-m", "alembic", "upgrade", "heads"],
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


async def test_engage_pauses_t010_t015_when_called(migrated_pool: AsyncConnectionPool) -> None:
    """should pause ConflictWorker AND MonthlyScheduler when engage() is called (R2 H1)."""
    from decision_ledger.services.b_lite_service import BLiteService

    # 准备 mock 的 ConflictWorker 和 MonthlyScheduler
    mock_conflict_worker = MagicMock()
    mock_conflict_worker.is_paused.return_value = False
    mock_monthly_scheduler = MagicMock()
    mock_monthly_scheduler.is_paused.return_value = False

    # 显式调用 pause 后变为 True（模拟真实行为）
    def _cw_pause() -> None:
        mock_conflict_worker.is_paused.return_value = True

    def _ms_pause() -> None:
        mock_monthly_scheduler.is_paused.return_value = True

    mock_conflict_worker.pause.side_effect = _cw_pause
    mock_monthly_scheduler.pause.side_effect = _ms_pause

    with (
        patch(
            "decision_ledger.monitor.pause_pipeline._conflict_worker_instance",
            mock_conflict_worker,
        ),
        patch(
            "decision_ledger.services.monthly_scheduler.monthly_scheduler",
            mock_monthly_scheduler,
        ),
    ):
        svc = BLiteService(pool=migrated_pool)
        await svc.engage(reason="连续 2 周决策 < 2")

    assert mock_conflict_worker.is_paused() is True, "ConflictWorker 应已 pause"
    assert mock_monthly_scheduler.is_paused() is True, "MonthlyScheduler 应已 pause"


async def test_disengage_in_cooling_off_raises_when_within_14d(
    migrated_pool: AsyncConnectionPool,
) -> None:
    """should raise ValueError when disengage() called within 14-day cooling-off period."""
    from decision_ledger.services.b_lite_service import BLiteService

    mock_conflict_worker = MagicMock()
    mock_conflict_worker.is_paused.return_value = False
    mock_conflict_worker.pause.side_effect = lambda: mock_conflict_worker.is_paused.__set__(
        mock_conflict_worker, lambda: True
    )

    def _cw_pause() -> None:
        mock_conflict_worker.is_paused.return_value = True

    mock_conflict_worker.pause.side_effect = _cw_pause

    mock_monthly_scheduler = MagicMock()
    mock_monthly_scheduler.is_paused.return_value = False

    with (
        patch(
            "decision_ledger.monitor.pause_pipeline._conflict_worker_instance",
            mock_conflict_worker,
        ),
        patch(
            "decision_ledger.services.monthly_scheduler.monthly_scheduler",
            mock_monthly_scheduler,
        ),
    ):
        svc = BLiteService(pool=migrated_pool)
        await svc.engage(reason="冷却期测试")

        # 立刻 disengage 应抛 ValueError（14 天内）
        with pytest.raises(ValueError, match="cooling-off"):
            await svc.disengage()


async def test_disengage_after_14d_resumes_all_when_cooling_off_expired(
    migrated_pool: AsyncConnectionPool,
) -> None:
    """should resume ConflictWorker and MonthlyScheduler when disengage() after 14 days."""
    from decision_ledger.services.b_lite_service import BLiteService

    mock_conflict_worker = MagicMock()
    mock_conflict_worker.is_paused.return_value = True

    def _cw_resume() -> None:
        mock_conflict_worker.is_paused.return_value = False

    mock_conflict_worker.resume.side_effect = _cw_resume

    mock_monthly_scheduler = MagicMock()
    mock_monthly_scheduler.is_paused.return_value = True

    def _ms_resume() -> None:
        mock_monthly_scheduler.is_paused.return_value = False

    mock_monthly_scheduler.resume.side_effect = _ms_resume

    # 直接在数据库写入一条 14 天前的 engage 记录（模拟 cooling_off 已过期）
    past_time = datetime.now(tz=UTC) - timedelta(days=15)
    cooling_off_until = past_time + timedelta(days=14)

    with (
        patch(
            "decision_ledger.monitor.pause_pipeline._conflict_worker_instance",
            mock_conflict_worker,
        ),
        patch(
            "decision_ledger.services.monthly_scheduler.monthly_scheduler",
            mock_monthly_scheduler,
        ),
    ):
        svc = BLiteService(pool=migrated_pool)
        await svc._ensure_table()

        # 写入已过期的 engage 记录
        import uuid

        meta_id = str(uuid.uuid4())
        async with migrated_pool.write_connection() as conn:
            await conn.execute(
                """
                INSERT INTO meta_decisions
                    (meta_id, decision_type, reason, created_at, cooling_off_until)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    meta_id,
                    "b_lite_engaged",
                    "过期测试",
                    past_time.isoformat(),
                    cooling_off_until.isoformat(),
                ),
            )
            await conn.commit()

        # 14 天后的 disengage 应成功
        await svc.disengage()

    assert mock_conflict_worker.is_paused() is False, "ConflictWorker 应已 resume"
    assert mock_monthly_scheduler.is_paused() is False, "MonthlyScheduler 应已 resume"


async def test_decision_recorder_still_works_when_engaged(
    migrated_pool: AsyncConnectionPool,
) -> None:
    """should allow DecisionRecorder to record decisions when B-lite is engaged.

    架构 §5 + Glossary: B-lite 砍冲突报告 + 月度 review, 保留档案 + 周度 review。
    decisions 表写入必须仍然正常工作。
    """
    from decision_ledger.domain.decision import Action, Decision, DecisionStatus
    from decision_ledger.domain.env_snapshot import EnvSnapshot
    from decision_ledger.repository.decision_repo import DecisionRepository
    from decision_ledger.services.b_lite_service import BLiteService

    # 先写入必要的 FK 依赖行（conflict_report + rebuttal）
    import uuid

    from datetime import UTC, datetime

    conflict_id = str(uuid.uuid4())
    rebuttal_id = str(uuid.uuid4())

    async with migrated_pool.write_connection() as conn:
        await conn.execute(
            """
            INSERT INTO conflict_reports
                (report_id, divergence_root_cause, has_divergence,
                 rendered_order_seed, signals_json, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (conflict_id, "test", 0, 3, "[]", datetime.now(tz=UTC).isoformat()),
        )
        await conn.execute(
            """
            INSERT INTO rebuttals (rebuttal_id, rebuttal_text, invoked_at)
            VALUES (?, ?, ?)
            """,
            (rebuttal_id, "test rebuttal ok!", datetime.now(tz=UTC).isoformat()),
        )
        await conn.commit()

    # engage B-lite（mock pause 不影响写入路径）
    mock_cw = MagicMock()
    mock_cw.is_paused.return_value = True
    mock_ms = MagicMock()
    mock_ms.is_paused.return_value = True

    with (
        patch(
            "decision_ledger.monitor.pause_pipeline._conflict_worker_instance",
            mock_cw,
        ),
        patch(
            "decision_ledger.services.monthly_scheduler.monthly_scheduler",
            mock_ms,
        ),
    ):
        svc = BLiteService(pool=migrated_pool)
        await svc.engage(reason="test engage")

    # 此时 B-lite 已 engage，但 decisions 表写入应仍正常工作
    decision_repo = DecisionRepository(migrated_pool)
    env_snapshot = EnvSnapshot(
        snapshot_at=datetime.now(tz=UTC),
        price=100.0,
        holdings_pct=0.05,
        holdings_abs=5000.0,
        advisor_week_id="2026-W17",
    )
    trade_id = str(uuid.uuid4())
    decision = Decision(
        trade_id=trade_id,
        ticker="AAPL",
        action=Action.HOLD,
        reason="B-lite 期间录入测试",
        pre_commit_at=datetime.now(tz=UTC),
        env_snapshot=env_snapshot,
        conflict_report_ref=conflict_id,
        devils_rebuttal_ref=rebuttal_id,
        would_have_acted_without_agent=False,
        status=DecisionStatus.COMMITTED,
    )

    # 关键断言: B-lite engage 时决策写入仍然成功
    await decision_repo.insert(decision)

    # 验证写入成功
    async with migrated_pool.connection() as conn:
        cursor = await conn.execute(
            "SELECT trade_id FROM decisions WHERE trade_id = ?",
            (trade_id,),
        )
        row = await cursor.fetchone()

    assert row is not None, "B-lite engage 时 decisions 表应仍可写入"
    assert str(row["trade_id"]) == trade_id


async def test_weekly_review_still_works_when_engaged(
    migrated_pool: AsyncConnectionPool,
) -> None:
    """should allow WeeklyReviewService to run when B-lite is engaged.

    架构 §5: B-lite 保留周度 review，不受 pause 影响。
    """
    from decision_ledger.services.b_lite_service import BLiteService
    from decision_ledger.services.weekly_review_service import WeeklyReviewService

    # engage B-lite
    mock_cw = MagicMock()
    mock_ms = MagicMock()

    with (
        patch(
            "decision_ledger.monitor.pause_pipeline._conflict_worker_instance",
            mock_cw,
        ),
        patch(
            "decision_ledger.services.monthly_scheduler.monthly_scheduler",
            mock_ms,
        ),
    ):
        svc = BLiteService(pool=migrated_pool)
        await svc.engage(reason="weekly review 测试")

    # 关键: 周度 review 不经过 pause hook，直接查 decisions 表
    weekly_svc = WeeklyReviewService(pool=migrated_pool, llm_client=None)
    result = await weekly_svc.generate(week_id="2026-W17")

    # B-lite engage 状态下周度 review 仍正常返回
    assert "total_decisions" in result, "weekly review 在 B-lite engage 时应仍返回正常结果"
    assert result["total_decisions"] >= 0


async def test_cli_engage_subcommand_when_called(
    migrated_pool: AsyncConnectionPool,
    tmp_path: Path,
) -> None:
    """should set is_engaged()=True when CLI engage subcommand is executed (R3 新增)."""
    db_path = tmp_path / "test_cli.sqlite"
    db_url = f"sqlite:///{db_path}"

    env = {
        **os.environ,
        "DECISION_LEDGER_DB_URL": db_url,
        "ANTHROPIC_API_KEY": os.environ.get("ANTHROPIC_API_KEY", "test-key-placeholder"),
        "TELEGRAM_BOT_TOKEN": os.environ.get("TELEGRAM_BOT_TOKEN", "test-token-placeholder"),
    }

    # 先跑 alembic 建表（多 head 必须用 heads，不能用 head）
    alembic_result = subprocess.run(  # noqa: S603
        [sys.executable, "-m", "alembic", "upgrade", "heads"],
        cwd=str(PROJECT_ROOT),
        env=env,
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert alembic_result.returncode == 0, f"alembic 失败: {alembic_result.stderr}"

    # 执行 CLI engage subcommand（通过 subprocess，与真实 CLI 一致）
    cli_script = PROJECT_ROOT / "scripts" / "toggle_b_lite.py"

    # mock pause_all_pipelines 以避免真实 pause
    result = subprocess.run(  # noqa: S603
        [
            sys.executable,
            str(cli_script),
            "engage",
            "--reason=连续 2 周决策 < 2 (CLI 测试)",
        ],
        cwd=str(PROJECT_ROOT),
        env={
            **env,
            # 测试模式: 跳过真实 pause hook（CLI 内部会处理）
            "DECISION_LEDGER_B_LITE_SKIP_PAUSE": "1",
        },
        capture_output=True,
        text=True,
        timeout=15,
    )

    assert result.returncode == 0, f"CLI engage 失败: {result.stderr}\nstdout: {result.stdout}"

    # 验证 meta_decisions 表有一行 engage 记录
    pool = AsyncConnectionPool(str(db_path))
    await pool.initialize()
    try:
        from decision_ledger.services.b_lite_service import BLiteService

        svc = BLiteService(pool=pool)
        status = await svc.status()
        assert status["engaged"] is True, "CLI engage 后 is_engaged 应为 True"
    finally:
        await pool.close()
