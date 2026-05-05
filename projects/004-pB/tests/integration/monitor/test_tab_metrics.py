"""
test_tab_metrics.py — T020 tab 打开计数集成测试
结论: 验证 TabMetricsMiddleware 写入 tab_open_log 及比率计算
细节:
  - GET / → tab_open_log 新增一行
  - count_opens_since(days=7) 返回正确计数
  - tab_ratio() = tab_opens / decisions_committed (14d)
  - 中间件写入通过 BackgroundTask 异步完成（不阻塞响应）
"""

from __future__ import annotations

import os
import subprocess
import sys
import uuid
from collections.abc import AsyncIterator
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from decision_ledger.domain.decision import Action, Decision, DecisionStatus
from decision_ledger.domain.env_snapshot import EnvSnapshot
from decision_ledger.repository.base import AsyncConnectionPool
from decision_ledger.repository.decision_repo import DecisionRepository

PROJECT_ROOT = Path(__file__).resolve().parents[3]


@pytest_asyncio.fixture
async def migrated_pool(tmp_path: Path) -> AsyncIterator[AsyncConnectionPool]:
    """提供经过 alembic upgrade head (含 0006) 迁移的 AsyncConnectionPool。"""
    db_path = tmp_path / "test_tab.sqlite"
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


async def test_count_opens_since_returns_zero_on_fresh_db(
    migrated_pool: AsyncConnectionPool,
) -> None:
    """should return 0 when no tab opens recorded"""
    from decision_ledger.monitor.tab_metrics import TabMetricsRepository

    repo = TabMetricsRepository(migrated_pool)
    count = await repo.count_opens_since(days=7)
    assert count == 0


async def test_record_and_count_tab_open(
    migrated_pool: AsyncConnectionPool,
) -> None:
    """should record tab open and count correctly"""
    from decision_ledger.monitor.tab_metrics import TabMetricsRepository

    repo = TabMetricsRepository(migrated_pool)
    await repo.record_open(path="/", user_agent="test-browser")
    await repo.record_open(path="/decisions/new", user_agent="test-browser")

    count = await repo.count_opens_since(days=7)
    assert count == 2


async def test_count_opens_excludes_old_records(
    migrated_pool: AsyncConnectionPool,
) -> None:
    """should not count tab opens older than specified days"""
    from decision_ledger.monitor.tab_metrics import TabMetricsRepository

    repo = TabMetricsRepository(migrated_pool)
    # 写入 1 条最近记录 + 1 条 8 天前记录（直接操作 DB）
    await repo.record_open(path="/", user_agent="new")

    # 直接插入旧记录
    async with migrated_pool.write_connection() as conn:
        old_ts = (datetime.now(tz=UTC) - timedelta(days=8)).isoformat()
        await conn.execute(
            "INSERT INTO tab_open_log (id, path, user_agent, opened_at) VALUES (?, ?, ?, ?)",
            (str(uuid.uuid4()), "/old", "old-browser", old_ts),
        )
        await conn.commit()

    count = await repo.count_opens_since(days=7)
    assert count == 1  # 只算最近 7 天


async def test_tab_ratio_with_committed_decisions(
    migrated_pool: AsyncConnectionPool,
) -> None:
    """should calculate tab_ratio = tab_opens / committed_decisions"""
    from decision_ledger.monitor.tab_metrics import TabMetricsRepository, calculate_tab_ratio

    tab_repo = TabMetricsRepository(migrated_pool)
    decision_repo = DecisionRepository(migrated_pool)

    # 先 seed conflict + rebuttal 满足 FK
    from decision_ledger.domain.conflict_report import ConflictReport
    from decision_ledger.domain.rebuttal import Rebuttal
    from decision_ledger.domain.strategy_signal import Direction, StrategySignal
    from decision_ledger.repository.conflict_repo import ConflictRepository
    from decision_ledger.repository.rebuttal_repo import RebuttalRepository

    cid = str(uuid.uuid4())
    rid = str(uuid.uuid4())
    signals = [
        StrategySignal(
            source_id=src,
            ticker="AAPL",
            direction=Direction.LONG,
            confidence=0.5,
            rationale_plain=f"{src} test",
            inputs_used={},
        )
        for src in ("advisor", "watchlist_v1", "contrarian_v1")
    ]
    await ConflictRepository(migrated_pool).insert(
        cid,
        ConflictReport(
            signals=signals,
            divergence_root_cause="t",
            has_divergence=False,
            rendered_order_seed=0,
        ),
    )
    await RebuttalRepository(migrated_pool).insert(
        rid,
        Rebuttal(rebuttal_text="t", invoked_at=datetime.now(tz=UTC).isoformat()),
    )

    # 插入 2 条 committed 决策
    for i in range(2):
        d = Decision(
            trade_id=f"trade_{uuid.uuid4().hex[:8]}",
            ticker="AAPL",
            action=Action.BUY,
            reason="测试",
            pre_commit_at=datetime.now(tz=UTC) - timedelta(days=i),
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
            would_have_acted_without_agent=True,
            status=DecisionStatus.COMMITTED,
        )
        await decision_repo.insert(d)

    # 插入 6 次 tab 打开
    for _ in range(6):
        await tab_repo.record_open(path="/", user_agent="browser")

    ratio = await calculate_tab_ratio(tab_repo=tab_repo, decision_repo=decision_repo)
    # 6 opens / 2 committed decisions = 3.0
    assert abs(ratio - 3.0) < 0.01


async def test_tab_ratio_returns_none_when_no_committed(
    migrated_pool: AsyncConnectionPool,
) -> None:
    """should return None when no committed decisions (avoid division by zero)"""
    from decision_ledger.monitor.tab_metrics import TabMetricsRepository, calculate_tab_ratio

    tab_repo = TabMetricsRepository(migrated_pool)
    decision_repo = DecisionRepository(migrated_pool)

    await tab_repo.record_open(path="/", user_agent="browser")
    ratio = await calculate_tab_ratio(tab_repo=tab_repo, decision_repo=decision_repo)
    assert ratio is None


async def test_middleware_records_tab_open_on_get_request(
    migrated_pool: AsyncConnectionPool,
) -> None:
    """should record tab open via middleware BackgroundTask on GET request"""
    from fastapi import FastAPI
    from fastapi.responses import PlainTextResponse

    from decision_ledger.monitor.tab_metrics import TabMetricsMiddleware, TabMetricsRepository

    app = FastAPI()
    app.add_middleware(TabMetricsMiddleware, pool=migrated_pool)

    @app.get("/")
    async def index() -> PlainTextResponse:
        return PlainTextResponse("ok")

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/")

    assert response.status_code == 200

    # BackgroundTask 应已写入（httpx AsyncClient 同步等待响应完成后 background 也完成）
    tab_repo = TabMetricsRepository(migrated_pool)
    count = await tab_repo.count_opens_since(days=1)
    assert count >= 1


async def test_middleware_does_not_record_post_request(
    migrated_pool: AsyncConnectionPool,
) -> None:
    """should not record POST requests as tab opens"""
    from fastapi import FastAPI
    from fastapi.responses import PlainTextResponse

    from decision_ledger.monitor.tab_metrics import TabMetricsMiddleware, TabMetricsRepository

    app = FastAPI()
    app.add_middleware(TabMetricsMiddleware, pool=migrated_pool)

    @app.post("/submit")
    async def submit() -> PlainTextResponse:
        return PlainTextResponse("ok")

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/submit")

    assert response.status_code == 200

    tab_repo = TabMetricsRepository(migrated_pool)
    count = await tab_repo.count_opens_since(days=1)
    assert count == 0


# ── F2-T020 H10: 路径白名单 + UA 截断 ────────────────────────────────────────


async def test_middleware_skips_unknown_path(
    migrated_pool: AsyncConnectionPool,
) -> None:
    """F2-H10: GET 不在白名单的随机 path → 不记录 (防 log 撑爆)。"""
    from fastapi import FastAPI
    from fastapi.responses import PlainTextResponse

    from decision_ledger.monitor.tab_metrics import TabMetricsMiddleware, TabMetricsRepository

    app = FastAPI()
    app.add_middleware(TabMetricsMiddleware, pool=migrated_pool)

    @app.get("/anything-malicious-{path:path}")
    async def anything(path: str) -> PlainTextResponse:
        return PlainTextResponse("ok")

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        for path in ("/anything-malicious-1", "/anything-malicious-foo", "/anything-malicious-x"):
            r = await client.get(path)
            assert r.status_code == 200

    tab_repo = TabMetricsRepository(migrated_pool)
    count = await tab_repo.count_opens_since(days=1)
    assert count == 0, "F2-H10: 非白名单路径不应进入 tab_open_log"


async def test_middleware_records_whitelisted_subpath(
    migrated_pool: AsyncConnectionPool,
) -> None:
    """F2-H10: 白名单前缀的子路径 (如 /decisions/abc) 命中。"""
    from fastapi import FastAPI
    from fastapi.responses import PlainTextResponse

    from decision_ledger.monitor.tab_metrics import TabMetricsMiddleware, TabMetricsRepository

    app = FastAPI()
    app.add_middleware(TabMetricsMiddleware, pool=migrated_pool)

    @app.get("/decisions/{path:path}")
    async def decisions_path(path: str) -> PlainTextResponse:
        return PlainTextResponse("ok")

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        r = await client.get("/decisions/draft-uuid-xyz")
        assert r.status_code == 200

    tab_repo = TabMetricsRepository(migrated_pool)
    count = await tab_repo.count_opens_since(days=1)
    assert count >= 1


async def test_middleware_skips_api_path(
    migrated_pool: AsyncConnectionPool,
) -> None:
    """F2-H10: /api/ 前缀显式排除 (后端调用不算 tab open)。"""
    from fastapi import FastAPI
    from fastapi.responses import PlainTextResponse

    from decision_ledger.monitor.tab_metrics import TabMetricsMiddleware, TabMetricsRepository

    app = FastAPI()
    app.add_middleware(TabMetricsMiddleware, pool=migrated_pool)

    @app.get("/api/health")
    async def api_health() -> PlainTextResponse:
        return PlainTextResponse("ok")

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        r = await client.get("/api/health")
        assert r.status_code == 200

    tab_repo = TabMetricsRepository(migrated_pool)
    count = await tab_repo.count_opens_since(days=1)
    assert count == 0


async def test_record_open_truncates_long_user_agent(
    migrated_pool: AsyncConnectionPool,
) -> None:
    """F2-H10: user_agent 长度 > 256 必须被截断 (防超大 UA 头打爆磁盘)。"""
    from decision_ledger.monitor.tab_metrics import TabMetricsRepository

    repo = TabMetricsRepository(migrated_pool)
    huge_ua = "X" * 2048
    await repo.record_open(path="/", user_agent=huge_ua)

    async with migrated_pool.connection() as conn:
        cursor = await conn.execute(
            "SELECT user_agent FROM tab_open_log ORDER BY opened_at DESC LIMIT 1"
        )
        row = await cursor.fetchone()
    assert row is not None
    stored_ua: str = row[0]
    assert len(stored_ua) <= 256, f"F2-H10 违反: UA 应截断到 ≤ 256, 实际 {len(stored_ua)}"


async def test_record_open_keeps_short_user_agent_intact(
    migrated_pool: AsyncConnectionPool,
) -> None:
    """F2-H10 反向: 正常 UA 不被截断。"""
    from decision_ledger.monitor.tab_metrics import TabMetricsRepository

    repo = TabMetricsRepository(migrated_pool)
    ua = "Mozilla/5.0 (Macintosh) AppleWebKit/537.36"
    await repo.record_open(path="/", user_agent=ua)

    async with migrated_pool.connection() as conn:
        cursor = await conn.execute(
            "SELECT user_agent FROM tab_open_log ORDER BY opened_at DESC LIMIT 1"
        )
        row = await cursor.fetchone()
    assert row[0] == ua


async def test_record_open_handles_none_user_agent(
    migrated_pool: AsyncConnectionPool,
) -> None:
    """F2-H10 反向: user_agent=None 不报错 (匿名请求)。"""
    from decision_ledger.monitor.tab_metrics import TabMetricsRepository

    repo = TabMetricsRepository(migrated_pool)
    await repo.record_open(path="/", user_agent=None)

    count = await repo.count_opens_since(days=1)
    assert count == 1
