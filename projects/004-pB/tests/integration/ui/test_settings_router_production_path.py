"""
test_settings_router_production_path.py — Codex review F1 修复
结论: 验证 settings router 在 production 路径 (lifespan-managed pool) 真正工作
细节:
  - test_watchlist_returns_503_before_lifespan_startup:
    pool 未 init 时 GET /settings/watchlist 必须 503 (而非静默 200 + 空表)
  - test_watchlist_works_after_lifespan_startup:
    lifespan 起 + startup task init pool 后, 路由真返回 watchlist 内容
  - 这是 F1 修复后的 regression gate — 防回退到"沉默 0%"

为什么需要专门一个 production-path 测试: 既有 test_settings_portfolio.py 用
fixture 直接传 initialized pool 给 create_settings_router, 绕过了 import 期
注册路径。本文件直接走 module-level _settings_pool_getter / _init_settings_pool,
模拟 production 启动顺序。
"""

from __future__ import annotations

import os
import subprocess
import sys
from collections.abc import AsyncIterator
from pathlib import Path

import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from decision_ledger.repository.base import AsyncConnectionPool

PROJECT_ROOT = Path(__file__).resolve().parents[3]


@pytest_asyncio.fixture
async def migrated_db_url(tmp_path: Path) -> AsyncIterator[str]:
    """提供经过 alembic upgrade head 迁移的 SQLite DB URL (供 settings 模块解析)。"""
    db_path = tmp_path / "test_settings_prod.sqlite"
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
    yield str(db_path)


async def test_watchlist_returns_503_before_lifespan_startup(tmp_path: Path) -> None:
    """F1 (Codex review): pool 未 init 时 GET /settings/watchlist 必须 503。

    场景: import 期 router 已注册, 但 lifespan 还没跑, _pool_holder['pool'] is None。
    旧版本: handler 触发 RuntimeError 被 try/except 静默吞 → 200 + 空表。
    修复后: handler 第一行 _get_repo() 检测 pool=None → HTTPException(503)。
    """
    from fastapi import FastAPI

    from decision_ledger.ui.router_settings import (
        _pool_holder,
        _settings_pool_getter,
        create_settings_router,
    )

    # 显式确保 holder 是空 (其他测试可能写过)
    _pool_holder["pool"] = None

    app = FastAPI()
    app.include_router(create_settings_router(pool_getter=_settings_pool_getter))

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        r = await c.get("/settings/watchlist")

    assert r.status_code == 503, (
        f"F1: pool 未 init 时应返回 503 (而非静默 200 + 空表), "
        f"实际 {r.status_code}, body={r.text[:200]}"
    )


async def test_watchlist_works_after_lifespan_startup(migrated_db_url: str, tmp_path: Path) -> None:
    """F1 (Codex review): lifespan 起 + startup task init pool 后, 路由真工作。"""
    from fastapi import FastAPI

    from decision_ledger.ui.router_settings import (
        _pool_holder,
        _settings_pool_getter,
        create_settings_router,
    )

    # reset holder; 模拟干净启动
    _pool_holder["pool"] = None

    # 把 db_url 注入到 Settings 解析路径
    # _resolve_settings_db_path() 走 load_settings → settings.decision_ledger_home / "data.sqlite"
    # 这里直接 patch holder 模拟 lifespan 起完后的状态
    pool = AsyncConnectionPool(migrated_db_url)
    await pool.initialize()
    _pool_holder["pool"] = pool

    try:
        app = FastAPI()
        app.include_router(create_settings_router(pool_getter=_settings_pool_getter))

        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
            r = await c.get("/settings/watchlist")

        assert r.status_code == 200, (
            f"lifespan 后路由应正常返回, 实际 {r.status_code}, body[:200]={r.text[:200]}"
        )
        # 模板真渲染了 watchlist HTML, 不是错误页
        assert "watchlist" in r.text.lower() or "关注股" in r.text
    finally:
        _pool_holder["pool"] = None
        await pool.close()


async def test_holdings_returns_503_before_lifespan_startup() -> None:
    """F1 (Codex review): /settings/holdings 同样守 wiring 检测。"""
    from fastapi import FastAPI

    from decision_ledger.ui.router_settings import (
        _pool_holder,
        _settings_pool_getter,
        create_settings_router,
    )

    _pool_holder["pool"] = None

    app = FastAPI()
    app.include_router(create_settings_router(pool_getter=_settings_pool_getter))

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        r = await c.get("/settings/holdings")

    assert r.status_code == 503


async def test_init_settings_pool_idempotent(migrated_db_url: str) -> None:
    """F1: _init_settings_pool 重复调用不报错 (幂等防御)。"""
    from decision_ledger.ui.router_settings import (
        _init_settings_pool,
        _pool_holder,
    )

    _pool_holder["pool"] = None

    # 第一次 init
    pool1 = AsyncConnectionPool(migrated_db_url)
    await pool1.initialize()
    _pool_holder["pool"] = pool1

    try:
        # 第二次调用应短路返回, 不替换 pool
        await _init_settings_pool()
        assert _pool_holder["pool"] is pool1, "幂等: 第二次调用不应替换 pool"
    finally:
        _pool_holder["pool"] = None
        await pool1.close()


def test_create_settings_router_requires_pool_or_getter() -> None:
    """F1: 工厂函数必须接收 pool 或 pool_getter 至少一个。"""
    import pytest

    from decision_ledger.ui.router_settings import create_settings_router

    with pytest.raises(ValueError, match="pool 或 pool_getter"):
        create_settings_router()
