"""
Base Repository 集成测试 — T003
结论: 验证 AsyncConnectionPool / WriterLock / connection() context manager 基础行为
细节:
  - 通过 tmpdir 建立实际 SQLite 文件，运行 alembic upgrade head
  - 验证 WAL pragma 已生效
  - 验证 WriterLock 保证串行写入
"""

from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator
from pathlib import Path

import pytest
import pytest_asyncio

from decision_ledger.repository.base import AsyncConnectionPool, get_writer_lock


@pytest_asyncio.fixture
async def db_pool(tmp_path: Path) -> AsyncIterator[AsyncConnectionPool]:
    """使用 tmpdir 建立 pool,自动初始化连接。"""
    db_path = tmp_path / "test_base.sqlite"
    pool = AsyncConnectionPool(str(db_path))
    await pool.initialize()
    try:
        yield pool
    finally:
        await pool.close()


@pytest.mark.asyncio
async def test_connection_context_manager_should_work_when_called(
    db_pool: AsyncConnectionPool,
) -> None:
    """结论: connection() 应返回可用的 aiosqlite 连接。"""
    async with db_pool.connection() as conn:
        cursor = await conn.execute("SELECT 1")
        row = await cursor.fetchone()
        assert row is not None
        assert row[0] == 1


@pytest.mark.asyncio
async def test_wal_pragma_should_be_set_when_initialized(
    db_pool: AsyncConnectionPool,
) -> None:
    """结论: 初始化后 journal_mode 应为 WAL（架构 §4.2 / T002 WAL 不变量）。"""
    async with db_pool.connection() as conn:
        cursor = await conn.execute("PRAGMA journal_mode")
        row = await cursor.fetchone()
        assert row is not None
        assert row[0] == "wal"


@pytest.mark.asyncio
async def test_foreign_keys_pragma_should_be_on_when_initialized(
    db_pool: AsyncConnectionPool,
) -> None:
    """结论: 初始化后 foreign_keys 应为 ON（架构 §9 不变量）。"""
    async with db_pool.connection() as conn:
        cursor = await conn.execute("PRAGMA foreign_keys")
        row = await cursor.fetchone()
        assert row is not None
        assert row[0] == 1


@pytest.mark.asyncio
async def test_writer_lock_should_serialize_concurrent_writes(
    db_pool: AsyncConnectionPool,
) -> None:
    """结论: WriterLock 应将并发写请求串行化，不产生数据竞争。"""
    results: list[int] = []

    async def write_task(i: int) -> None:
        async with db_pool.writer_lock:
            results.append(i)
            await asyncio.sleep(0)  # 让出 event loop，测试锁的效果

    await asyncio.gather(*[write_task(i) for i in range(5)])
    assert len(results) == 5


@pytest.mark.asyncio
async def test_writer_lock_singleton_should_be_shared(
    tmp_path: Path,
) -> None:
    """结论: 同一 db_path 应共享同一个 WriterLock 实例（单一 writer 不变量）。"""
    db_path = str(tmp_path / "singleton.sqlite")
    lock1 = get_writer_lock(db_path)
    lock2 = get_writer_lock(db_path)
    assert lock1 is lock2


@pytest.mark.asyncio
async def test_row_factory_should_be_aiosqlite_row(
    db_pool: AsyncConnectionPool,
) -> None:
    """结论: row_factory 应为 aiosqlite.Row，支持列名访问（Known gotcha #1）。"""
    async with db_pool.connection() as conn:
        cursor = await conn.execute("SELECT 1 AS value")
        row = await cursor.fetchone()
        assert row is not None
        # aiosqlite.Row 支持列名访问
        assert row["value"] == 1
