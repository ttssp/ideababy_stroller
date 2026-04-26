"""
Repository 基础设施 — T003
结论: 提供 AsyncConnectionPool (单连接 + WAL) / WriterLock / BaseRepository 抽象
细节:
  - AsyncConnectionPool: 封装 aiosqlite 连接，初始化时设置 WAL + foreign_keys
  - WriterLock: asyncio.Lock 保证写路径串行（单一 writer 不变量，架构 §9.6）
  - writer_lock 按 db_path 做单例，防止多处 pool 实例破坏 writer 保证
  - row_factory=aiosqlite.Row 在连接级别设置（Known gotcha #1）
  - 短事务原则: 不在事务内做 LLM/网络调用（TECH-1 / 架构 §9 不变量）
"""

from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import aiosqlite

# 按 db_path 存储 WriterLock 单例（单一 writer 不变量）
# 结论: 同一 db_path 的所有 pool 实例共享同一把锁，避免并发写竞争
_writer_lock_registry: dict[str, asyncio.Lock] = {}


def get_writer_lock(db_path: str) -> asyncio.Lock:
    """获取指定 db_path 对应的 WriterLock（单例）。

    结论: 同一路径返回同一把锁，确保 writer 唯一性。
    """
    if db_path not in _writer_lock_registry:
        _writer_lock_registry[db_path] = asyncio.Lock()
    return _writer_lock_registry[db_path]


# 类型别名，供外部引用
WriterLock = asyncio.Lock


class AsyncConnectionPool:
    """SQLite 异步连接管理 — aiosqlite 单连接 + WAL pragma。

    架构约束:
      - WAL 模式: reader 不阻塞 writer（读路径无锁）
      - foreign_keys=ON: 外键约束默认关闭，必须显式开启
      - row_factory=aiosqlite.Row: 支持列名访问（Known gotcha #1）
      - 写入必须在 writer_lock 下执行（单一 writer 不变量）
    """

    def __init__(self, db_path: str) -> None:
        """
        结论: 仅记录路径，实际连接在 initialize() 时建立。
        """
        self._db_path = db_path
        self._conn: aiosqlite.Connection | None = None
        self.writer_lock: asyncio.Lock = get_writer_lock(db_path)

    async def initialize(self) -> None:
        """建立 SQLite 连接，设置 WAL + foreign_keys pragma。

        结论: initialize() 必须在使用 connection() 前调用。
        细节: WAL 模式下 reader 不阻塞 writer（多 asyncio task 并发读写安全）。
        """
        self._conn = await aiosqlite.connect(self._db_path)
        # row_factory 让 cursor 返回 aiosqlite.Row（支持列名访问）
        self._conn.row_factory = aiosqlite.Row
        # WAL + foreign_keys — 每次连接必须重新设置（SQLite 连接级别设置）
        await self._conn.execute("PRAGMA journal_mode=WAL")
        await self._conn.execute("PRAGMA foreign_keys=ON")
        await self._conn.commit()

    async def close(self) -> None:
        """关闭连接。"""
        if self._conn is not None:
            await self._conn.close()
            self._conn = None

    @asynccontextmanager
    async def connection(self) -> AsyncIterator[aiosqlite.Connection]:
        """返回当前连接的 async context manager。

        结论: 读路径直接使用，写路径需在 writer_lock 下使用。
        细节: 不自动加锁（读路径不需要锁，WAL 保护并发读）。
        """
        if self._conn is None:
            raise RuntimeError("AsyncConnectionPool 尚未初始化，请先调用 initialize()")
        yield self._conn

    @asynccontextmanager
    async def write_connection(self) -> AsyncIterator[aiosqlite.Connection]:
        """获取写入连接 — 自动持有 WriterLock（单一 writer 不变量）。

        结论: 所有写操作必须通过 write_connection()，保证串行写入。
        细节: writer_lock 是 asyncio.Lock，防止多 coroutine 同时写。
        """
        async with self.writer_lock:
            if self._conn is None:
                raise RuntimeError("AsyncConnectionPool 尚未初始化，请先调用 initialize()")
            yield self._conn
