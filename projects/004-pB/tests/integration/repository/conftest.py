"""
Repository 集成测试共享 Fixtures — T003
结论: 提供迁移完毕的 AsyncConnectionPool 给所有 repo 集成测试
细节:
  - migrated_pool: 每个 test function 使用独立 tmpdir + alembic upgrade head
  - 用 subprocess 跑 alembic,避免与测试进程共享 SQLite 连接 / event loop
  - 防止测试间数据污染
"""

from __future__ import annotations

import os
import subprocess
import sys
from collections.abc import AsyncIterator
from pathlib import Path

import pytest_asyncio

from decision_ledger.repository.base import AsyncConnectionPool

PROJECT_ROOT = Path(__file__).resolve().parents[3]


@pytest_asyncio.fixture
async def migrated_pool(tmp_path: Path) -> AsyncIterator[AsyncConnectionPool]:
    """提供经过 alembic upgrade head 迁移的 AsyncConnectionPool。

    结论: 每个测试函数独立数据库(tmp_path 隔离),避免测试间状态污染。
    细节: 用 subprocess 调 alembic,免于在同一进程内对同一 db 形成并发锁。
    """
    db_path = tmp_path / "test.sqlite"
    db_url = f"sqlite:///{db_path}"

    env = {
        **os.environ,
        "DECISION_LEDGER_DB_URL": db_url,
        # 满足 Settings 校验的占位
        "ANTHROPIC_API_KEY": os.environ.get("ANTHROPIC_API_KEY", "test-key-placeholder"),
        "TELEGRAM_BOT_TOKEN": os.environ.get("TELEGRAM_BOT_TOKEN", "test-token-placeholder"),
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
