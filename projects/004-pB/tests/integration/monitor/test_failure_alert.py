"""
test_failure_alert.py — T020 集成测试
结论: 验证 O10 双通道告警机制 (DB 写入 + bot mock 调用 + banner 渲染)
细节:
  - 模拟 14 天内仅 1 条 committed decision → check() → 断言 alerts 表新增
  - 验证 bot.send_alert mock 被调用（Telegram 通道）
  - 验证 /_partials/alert-banner 含告警内容 + CLI 命令文本
  - decisions count WHERE status='committed' (R2 规则)
  - banner 含 'scripts/toggle_b_lite.py engage' + 'docs/runbooks/b_lite.md' (R3 M2)
"""

from __future__ import annotations

import os
import subprocess
import sys
import uuid
from collections.abc import AsyncIterator
from datetime import UTC, datetime, timedelta
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from decision_ledger.domain.alert import AlertSeverity, AlertType
from decision_ledger.domain.conflict_report import ConflictReport
from decision_ledger.domain.decision import Action, Decision, DecisionStatus
from decision_ledger.domain.env_snapshot import EnvSnapshot
from decision_ledger.domain.rebuttal import Rebuttal
from decision_ledger.domain.strategy_signal import Direction, StrategySignal
from decision_ledger.repository.alert_repo import AlertRepository
from decision_ledger.repository.base import AsyncConnectionPool
from decision_ledger.repository.conflict_repo import ConflictRepository
from decision_ledger.repository.decision_repo import DecisionRepository
from decision_ledger.repository.rebuttal_repo import RebuttalRepository


async def _seed_conflict_and_rebuttal(pool: AsyncConnectionPool) -> tuple[str, str]:
    """先创建 conflict_report + rebuttal 记录满足 decisions FK 约束。"""
    conflict_id = str(uuid.uuid4())
    rebuttal_id = str(uuid.uuid4())
    signals = [
        StrategySignal(
            source_id=src,
            ticker="AAPL",
            direction=Direction.LONG,
            confidence=0.6,
            rationale_plain=f"{src} test rationale",
            inputs_used={"source": "test"},
        )
        for src in ("advisor", "watchlist_v1", "contrarian_v1")
    ]
    cr = ConflictReport(
        signals=signals,
        divergence_root_cause="test",
        has_divergence=False,
        rendered_order_seed=0,
    )
    rb = Rebuttal(
        rebuttal_text="test rebuttal",
        invoked_at=datetime.now(tz=UTC).isoformat(),
    )
    await ConflictRepository(pool).insert(conflict_id, cr)
    await RebuttalRepository(pool).insert(rebuttal_id, rb)
    return conflict_id, rebuttal_id

PROJECT_ROOT = Path(__file__).resolve().parents[3]


@pytest_asyncio.fixture
async def migrated_pool(tmp_path: Path) -> AsyncIterator[AsyncConnectionPool]:
    """提供经过 alembic upgrade head (含 0006) 迁移的 AsyncConnectionPool。"""
    db_path = tmp_path / "test_alert.sqlite"
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
    assert result.returncode == 0, f"alembic upgrade 失败:\n{result.stderr}"

    pool = AsyncConnectionPool(str(db_path))
    await pool.initialize()
    try:
        yield pool
    finally:
        await pool.close()


def _make_committed_decision(
    days_ago: int = 0,
    conflict_id: str = "",
    rebuttal_id: str = "",
) -> Decision:
    """构造指定天数前的已提交决策 fixture(conflict/rebuttal id 必传 — FK 约束)。"""
    pre_commit_at = datetime.now(tz=UTC) - timedelta(days=days_ago)
    return Decision(
        trade_id=f"trade_{uuid.uuid4().hex[:8]}",
        ticker="AAPL",
        action=Action.BUY,
        reason="测试决策理由",
        pre_commit_at=pre_commit_at,
        env_snapshot=EnvSnapshot(
            price=100.0,
            holdings_pct=0.05,
            holdings_abs=5000.0,
            advisor_week_id="2026-W17",
            snapshot_at=pre_commit_at,
        ),
        conflict_report_ref=conflict_id,
        devils_rebuttal_ref=rebuttal_id,
        post_mortem=None,
        would_have_acted_without_agent=True,
        status=DecisionStatus.COMMITTED,
    )


async def test_check_triggers_alert_when_committed_count_less_than_2(
    migrated_pool: AsyncConnectionPool,
) -> None:
    """should trigger alert when committed decisions in 14d < 2"""
    from decision_ledger.monitor.failure_alert import FailureAlertMonitor

    decision_repo = DecisionRepository(migrated_pool)
    alert_repo = AlertRepository(migrated_pool)
    cid, rid = await _seed_conflict_and_rebuttal(migrated_pool)

    # 仅插入 1 条 committed 决策(14 天内)
    await decision_repo.insert(
        _make_committed_decision(days_ago=3, conflict_id=cid, rebuttal_id=rid)
    )

    mock_bot = MagicMock()
    mock_bot.send_alert = AsyncMock()

    monitor = FailureAlertMonitor(
        decision_repo=decision_repo,
        alert_repo=alert_repo,
        bot=mock_bot,
    )
    await monitor.check()

    # 验证 alerts 表新增告警
    active_alerts = await alert_repo.latest_active()
    assert len(active_alerts) >= 1
    alert = active_alerts[0]
    assert alert.alert_type == AlertType.LOW_DECISION_RATE
    assert alert.severity == AlertSeverity.CRITICAL

    # 验证 Telegram bot 被调用（O10 双通道）
    mock_bot.send_alert.assert_called_once()


async def test_check_no_alert_when_committed_count_2_or_more(
    migrated_pool: AsyncConnectionPool,
) -> None:
    """should not trigger alert when committed decisions in 14d >= 2"""
    from decision_ledger.monitor.failure_alert import FailureAlertMonitor

    decision_repo = DecisionRepository(migrated_pool)
    alert_repo = AlertRepository(migrated_pool)
    cid, rid = await _seed_conflict_and_rebuttal(migrated_pool)

    # 插入 2 条 committed 决策
    await decision_repo.insert(
        _make_committed_decision(days_ago=1, conflict_id=cid, rebuttal_id=rid)
    )
    await decision_repo.insert(
        _make_committed_decision(days_ago=5, conflict_id=cid, rebuttal_id=rid)
    )

    mock_bot = MagicMock()
    mock_bot.send_alert = AsyncMock()

    monitor = FailureAlertMonitor(
        decision_repo=decision_repo,
        alert_repo=alert_repo,
        bot=mock_bot,
    )
    await monitor.check()

    active_alerts = await alert_repo.latest_active()
    assert len(active_alerts) == 0
    mock_bot.send_alert.assert_not_called()


async def test_check_only_counts_committed_not_draft(
    migrated_pool: AsyncConnectionPool,
) -> None:
    """should only count committed decisions, not draft (R2 规则)"""
    from decision_ledger.domain.decision import DecisionStatus
    from decision_ledger.monitor.failure_alert import FailureAlertMonitor

    decision_repo = DecisionRepository(migrated_pool)
    alert_repo = AlertRepository(migrated_pool)
    cid, rid = await _seed_conflict_and_rebuttal(migrated_pool)

    # 插入 1 条 committed + 1 条 draft(draft 不应计入)
    committed = _make_committed_decision(days_ago=2, conflict_id=cid, rebuttal_id=rid)
    await decision_repo.insert(committed)

    # draft 状态的决策不应计入 14d count
    draft = Decision(
        trade_id=f"trade_{uuid.uuid4().hex[:8]}",
        ticker="TSLA",
        action=Action.HOLD,
        reason="草稿决策",
        pre_commit_at=datetime.now(tz=UTC) - timedelta(days=1),
        env_snapshot=EnvSnapshot(
            price=100.0,
            holdings_pct=0.05,
            holdings_abs=5000.0,
            advisor_week_id="2026-W17",
            snapshot_at=datetime.now(tz=UTC),
        ),
        conflict_report_ref=cid,
        devils_rebuttal_ref=rid,
        post_mortem=None,
        would_have_acted_without_agent=False,
        status=DecisionStatus.DRAFT,
    )
    await decision_repo.insert(draft)

    mock_bot = MagicMock()
    mock_bot.send_alert = AsyncMock()

    monitor = FailureAlertMonitor(
        decision_repo=decision_repo,
        alert_repo=alert_repo,
        bot=mock_bot,
    )
    await monitor.check()

    # 因为只有 1 条 committed，应触发告警
    active_alerts = await alert_repo.latest_active()
    assert len(active_alerts) >= 1


async def test_alert_banner_partial_contains_cli_commands(
    migrated_pool: AsyncConnectionPool,
) -> None:
    """should render alert banner with CLI commands and runbook reference (R3 M2 + B-R2-4)"""
    from fastapi import FastAPI
    from fastapi.templating import Jinja2Templates

    from decision_ledger.monitor.failure_alert import FailureAlertMonitor
    from decision_ledger.ui.router_alert_partial import create_alert_partial_router

    decision_repo = DecisionRepository(migrated_pool)
    alert_repo = AlertRepository(migrated_pool)
    cid, rid = await _seed_conflict_and_rebuttal(migrated_pool)

    # 插入 1 条 committed 决策 → 触发告警
    await decision_repo.insert(
        _make_committed_decision(days_ago=3, conflict_id=cid, rebuttal_id=rid)
    )

    mock_bot = MagicMock()
    mock_bot.send_alert = AsyncMock()

    monitor = FailureAlertMonitor(
        decision_repo=decision_repo,
        alert_repo=alert_repo,
        bot=mock_bot,
    )
    await monitor.check()

    # 创建 FastAPI app + 注册 alert partial router
    app = FastAPI()
    templates_dir = (
        Path(__file__).resolve().parents[3]
        / "src"
        / "decision_ledger"
        / "ui"
        / "templates"
    )
    templates = Jinja2Templates(directory=str(templates_dir))
    alert_partial_router = create_alert_partial_router(
        alert_repo=alert_repo,
        templates=templates,
    )
    app.include_router(alert_partial_router)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/_partials/alert-banner")

    assert response.status_code == 200
    html = response.text

    # R3 M2 + B-R2-4: banner 含 CLI 命令 + runbook 引用
    assert "scripts/toggle_b_lite.py engage" in html
    assert "docs/runbooks/b_lite.md" in html


async def test_alert_banner_empty_when_no_active_alert(
    migrated_pool: AsyncConnectionPool,
) -> None:
    """should return empty banner when no active alerts"""
    from fastapi import FastAPI
    from fastapi.templating import Jinja2Templates

    from decision_ledger.ui.router_alert_partial import create_alert_partial_router

    alert_repo = AlertRepository(migrated_pool)

    app = FastAPI()
    templates_dir = (
        Path(__file__).resolve().parents[3]
        / "src"
        / "decision_ledger"
        / "ui"
        / "templates"
    )
    templates = Jinja2Templates(directory=str(templates_dir))
    alert_partial_router = create_alert_partial_router(
        alert_repo=alert_repo,
        templates=templates,
    )
    app.include_router(alert_partial_router)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/_partials/alert-banner")

    assert response.status_code == 200
    # 无告警时应返回空内容
    assert response.text.strip() == ""
