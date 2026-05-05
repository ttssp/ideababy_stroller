"""
T012 — settings 路由集成测试
结论: POST /settings/watchlist + /settings/holdings 写入数据库并可读回
细节:
  - 使用 migrated_pool fixture (alembic upgrade head 真实 schema)
  - 粘贴 30 行 CSV → watchlist 表 30 行
  - 粘贴 JSON → holdings snapshot 写入
  - ticker uppercase / dedupe 在集成层验证
  - BOM CSV 仍能解析
  - 超过 100 ticker 返回 4xx 错误
  - 非法 JSON 返回 4xx 错误
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from collections.abc import AsyncIterator
from pathlib import Path

import pytest
import pytest_asyncio
from fastapi import FastAPI
from fastapi.testclient import TestClient

from decision_ledger.repository.base import AsyncConnectionPool
from decision_ledger.repository.portfolio_repo import PortfolioRepository

PROJECT_ROOT = Path(__file__).resolve().parents[3]


# ─── Fixtures ────────────────────────────────────────────────────────────


@pytest_asyncio.fixture
async def migrated_pool(tmp_path: Path) -> AsyncIterator[AsyncConnectionPool]:
    """T012 专用 migrated_pool — 避免跨模块 fixture 冲突。"""
    db_path = tmp_path / "test_t012.sqlite"
    db_url = f"sqlite:///{db_path}"

    env = {
        **os.environ,
        "DECISION_LEDGER_DB_URL": db_url,
        "ANTHROPIC_API_KEY": os.environ.get("ANTHROPIC_API_KEY", "test-key-placeholder"),
        "TELEGRAM_BOT_TOKEN": os.environ.get(
            "TELEGRAM_BOT_TOKEN", "test-token-placeholder"
        ),
    }
    result = subprocess.run(  # noqa: S603 — 受信任 alembic 调用
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


@pytest.fixture
def portfolio_app(migrated_pool: AsyncConnectionPool) -> TestClient:
    """创建包含 settings router 的 TestClient，注入真实 migrated_pool。"""
    os.environ.setdefault("ANTHROPIC_API_KEY", "test-key-placeholder")
    os.environ.setdefault("TELEGRAM_BOT_TOKEN", "test-token-placeholder")

    from decision_ledger.ui.router_settings import create_settings_router

    app = FastAPI()
    router = create_settings_router(pool=migrated_pool)
    app.include_router(router)

    return TestClient(app, raise_server_exceptions=False)


# ─── GET 路由测试 ─────────────────────────────────────────────────────────


class TestSettingsWatchlistGet:
    """GET /settings/watchlist 路由测试。"""

    def test_should_return_200_when_get_watchlist_page(
        self, portfolio_app: TestClient
    ) -> None:
        """GET /settings/watchlist → 200 + HTML。"""
        response = portfolio_app.get("/settings/watchlist")
        assert response.status_code == 200
        assert "text/html" in response.headers.get("content-type", "")

    def test_should_contain_textarea_when_get_watchlist(
        self, portfolio_app: TestClient
    ) -> None:
        """GET /settings/watchlist 页面含 textarea (CSV 粘贴区)。"""
        response = portfolio_app.get("/settings/watchlist")
        assert b"textarea" in response.content.lower()


class TestSettingsHoldingsGet:
    """GET /settings/holdings 路由测试。"""

    def test_should_return_200_when_get_holdings_page(
        self, portfolio_app: TestClient
    ) -> None:
        """GET /settings/holdings → 200 + HTML。"""
        response = portfolio_app.get("/settings/holdings")
        assert response.status_code == 200
        assert "text/html" in response.headers.get("content-type", "")

    def test_should_contain_textarea_when_get_holdings(
        self, portfolio_app: TestClient
    ) -> None:
        """GET /settings/holdings 页面含 textarea (JSON 粘贴区)。"""
        response = portfolio_app.get("/settings/holdings")
        assert b"textarea" in response.content.lower()


# ─── POST watchlist 路由测试 ──────────────────────────────────────────────


class TestSettingsWatchlistPost:
    """POST /settings/watchlist 路由测试。"""

    def test_should_write_30_rows_when_post_30_line_csv(
        self,
        portfolio_app: TestClient,
        migrated_pool: AsyncConnectionPool,
    ) -> None:
        """粘贴 30 行 CSV → watchlist 表 30 行 (spec §T012 集成测试要求)。"""
        lines = "\n".join(f"TK{i:02d},Tech,Note{i}" for i in range(30))
        response = portfolio_app.post(
            "/settings/watchlist",
            data={"csv_text": lines},
        )
        # 重定向或 200 均可（POST 成功后通常 redirect back）
        assert response.status_code in (200, 303, 302)

        # 读库验证 30 行
        import asyncio

        repo = PortfolioRepository(migrated_pool)
        watchlist = asyncio.get_event_loop().run_until_complete(repo.get_watchlist())
        assert len(watchlist) == 30

    def test_should_uppercase_ticker_when_post_lowercase_csv(
        self,
        portfolio_app: TestClient,
        migrated_pool: AsyncConnectionPool,
    ) -> None:
        """CSV 中 ticker 小写 → 写入后全部 uppercase。"""
        response = portfolio_app.post(
            "/settings/watchlist",
            data={"csv_text": "tsm,Tech,\naapl,Tech,\n"},
        )
        assert response.status_code in (200, 303, 302)

        import asyncio

        repo = PortfolioRepository(migrated_pool)
        watchlist = asyncio.get_event_loop().run_until_complete(repo.get_watchlist())
        tickers = [w.ticker for w in watchlist]
        assert "TSM" in tickers
        assert "AAPL" in tickers
        assert "tsm" not in tickers

    def test_should_dedupe_ticker_when_post_duplicate_csv(
        self,
        portfolio_app: TestClient,
        migrated_pool: AsyncConnectionPool,
    ) -> None:
        """CSV 含重复 ticker → 去重后写入。"""
        response = portfolio_app.post(
            "/settings/watchlist",
            data={"csv_text": "TSM,Tech,\nTSM,Finance,dup\nAAPL,Tech,\n"},
        )
        assert response.status_code in (200, 303, 302)

        import asyncio

        repo = PortfolioRepository(migrated_pool)
        watchlist = asyncio.get_event_loop().run_until_complete(repo.get_watchlist())
        tickers = [w.ticker for w in watchlist]
        assert tickers.count("TSM") == 1
        assert len(watchlist) == 2

    def test_should_handle_bom_csv_when_excel_export(
        self,
        portfolio_app: TestClient,
        migrated_pool: AsyncConnectionPool,
    ) -> None:
        """Excel 导出的 BOM CSV 应正常写入。"""
        bom_csv = "﻿tsm,Tech,Taiwan Semi\naapl,Tech,Apple\n"
        response = portfolio_app.post(
            "/settings/watchlist",
            data={"csv_text": bom_csv},
        )
        assert response.status_code in (200, 303, 302)

        import asyncio

        repo = PortfolioRepository(migrated_pool)
        watchlist = asyncio.get_event_loop().run_until_complete(repo.get_watchlist())
        tickers = [w.ticker for w in watchlist]
        assert "TSM" in tickers
        # 首个 ticker 不含 BOM 残留
        assert not any(t.startswith("﻿") for t in tickers)

    def test_should_return_4xx_when_post_over_100_tickers(
        self, portfolio_app: TestClient
    ) -> None:
        """超过 100 个 ticker → 4xx 错误响应。"""
        lines = "\n".join(f"TK{i:03d},Tech," for i in range(101))
        response = portfolio_app.post(
            "/settings/watchlist",
            data={"csv_text": lines},
        )
        assert response.status_code in (400, 422)

    def test_should_replace_watchlist_when_post_twice(
        self,
        portfolio_app: TestClient,
        migrated_pool: AsyncConnectionPool,
    ) -> None:
        """第二次 POST 应整体替换（不追加）watchlist。"""
        # 第一次：3 条
        portfolio_app.post(
            "/settings/watchlist",
            data={"csv_text": "TSM,Tech,\nAAPL,Tech,\nNVDA,Tech,\n"},
        )
        # 第二次：1 条
        portfolio_app.post(
            "/settings/watchlist",
            data={"csv_text": "MSFT,Tech,\n"},
        )

        import asyncio

        repo = PortfolioRepository(migrated_pool)
        watchlist = asyncio.get_event_loop().run_until_complete(repo.get_watchlist())
        assert len(watchlist) == 1
        assert watchlist[0].ticker == "MSFT"


# ─── POST holdings 路由测试 ──────────────────────────────────────────────


class TestSettingsHoldingsPost:
    """POST /settings/holdings 路由测试。"""

    def test_should_write_snapshot_when_post_valid_json(
        self,
        portfolio_app: TestClient,
        migrated_pool: AsyncConnectionPool,
    ) -> None:
        """粘贴合法 JSON → holdings snapshot 写入数据库 (spec §T012 集成测试要求)。"""
        holdings_json = json.dumps(
            [{"ticker": "TSM", "qty": 100, "cost_basis": 92.0}]
        )
        response = portfolio_app.post(
            "/settings/holdings",
            data={"json_text": holdings_json},
        )
        assert response.status_code in (200, 303, 302)

        # 读库验证 snapshot 写入
        import asyncio

        repo = PortfolioRepository(migrated_pool)
        snapshot = asyncio.get_event_loop().run_until_complete(repo.latest_snapshot())
        assert snapshot is not None
        assert len(snapshot.holdings) == 1
        assert snapshot.holdings[0].ticker == "TSM"

    def test_should_return_4xx_when_post_invalid_json(
        self, portfolio_app: TestClient
    ) -> None:
        """非法 JSON → 4xx 错误响应。"""
        response = portfolio_app.post(
            "/settings/holdings",
            data={"json_text": "not valid json {{{{"},
        )
        assert response.status_code in (400, 422)

    def test_should_return_4xx_when_post_json_not_array(
        self, portfolio_app: TestClient
    ) -> None:
        """JSON 非 array → 4xx 错误响应。"""
        response = portfolio_app.post(
            "/settings/holdings",
            data={"json_text": '{"ticker": "TSM", "qty": 100}'},
        )
        assert response.status_code in (400, 422)

    def test_should_uppercase_ticker_in_holdings_when_post_lowercase(
        self,
        portfolio_app: TestClient,
        migrated_pool: AsyncConnectionPool,
    ) -> None:
        """holdings JSON 中 ticker 小写 → 写入后 uppercase。"""
        holdings_json = json.dumps(
            [{"ticker": "tsm", "qty": 100, "cost_basis": 92.0}]
        )
        response = portfolio_app.post(
            "/settings/holdings",
            data={"json_text": holdings_json},
        )
        assert response.status_code in (200, 303, 302)

        import asyncio

        repo = PortfolioRepository(migrated_pool)
        snapshot = asyncio.get_event_loop().run_until_complete(repo.latest_snapshot())
        assert snapshot is not None
        assert snapshot.holdings[0].ticker == "TSM"

    def test_should_return_4xx_when_exceeds_100_holdings(
        self, portfolio_app: TestClient
    ) -> None:
        """超过 100 条 holdings → 4xx 错误响应。"""
        items = [{"ticker": f"TK{i:03d}", "qty": 10, "cost_basis": 1.0} for i in range(101)]
        response = portfolio_app.post(
            "/settings/holdings",
            data={"json_text": json.dumps(items)},
        )
        assert response.status_code in (400, 422)
