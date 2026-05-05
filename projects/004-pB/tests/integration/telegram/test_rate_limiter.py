"""
rate_limiter 集成测试 — T017
结论: 验证 7 天滚动窗口 rate limiter (≤ 1 weekly + 5 event)
细节:
  - test_first_weekly_allowed: 第一次 weekly push → True
  - test_second_weekly_blocked: 7 天内第二次 weekly → False
  - test_five_events_allowed: 7 天内 5 次 event → 全部 True
  - test_sixth_event_blocked: 第 6 次 event → False
  - test_old_pushes_not_counted: 8 天前的推送不计入窗口
  - test_weekly_and_event_independent: weekly 和 event 配额互相独立
"""

from __future__ import annotations

import os
import subprocess
import sys
from collections.abc import AsyncIterator
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest
import pytest_asyncio

from decision_ledger.repository.base import AsyncConnectionPool

PROJECT_ROOT = Path(__file__).resolve().parents[3]


@pytest_asyncio.fixture
async def migrated_pool(tmp_path: Path) -> AsyncIterator[AsyncConnectionPool]:
    """提供经过 alembic upgrade head 迁移的 AsyncConnectionPool。"""
    db_path = tmp_path / "test_rate_limiter.sqlite"
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


@pytest.mark.asyncio
async def test_first_weekly_allowed(migrated_pool: AsyncConnectionPool) -> None:
    """should allow first weekly push within 7-day window."""
    from decision_ledger.telegram.rate_limiter import RateLimiter

    rl = RateLimiter(migrated_pool)
    chat_id = "12345"
    result = await rl.try_push(chat_id, push_type="weekly")
    assert result is True


@pytest.mark.asyncio
async def test_second_weekly_blocked(migrated_pool: AsyncConnectionPool) -> None:
    """should block second weekly push within 7-day window."""
    from decision_ledger.telegram.rate_limiter import RateLimiter

    rl = RateLimiter(migrated_pool)
    chat_id = "12345"
    first = await rl.try_push(chat_id, push_type="weekly")
    assert first is True

    second = await rl.try_push(chat_id, push_type="weekly")
    assert second is False


@pytest.mark.asyncio
async def test_five_events_allowed(migrated_pool: AsyncConnectionPool) -> None:
    """should allow up to 5 event pushes within 7-day window."""
    from decision_ledger.telegram.rate_limiter import RateLimiter

    rl = RateLimiter(migrated_pool)
    chat_id = "12345"
    results = [await rl.try_push(chat_id, push_type="event") for _ in range(5)]
    assert all(results), f"Expected all True, got {results}"


@pytest.mark.asyncio
async def test_sixth_event_blocked(migrated_pool: AsyncConnectionPool) -> None:
    """should block 6th event push within 7-day window."""
    from decision_ledger.telegram.rate_limiter import RateLimiter

    rl = RateLimiter(migrated_pool)
    chat_id = "12345"
    for _ in range(5):
        await rl.try_push(chat_id, push_type="event")

    sixth = await rl.try_push(chat_id, push_type="event")
    assert sixth is False


@pytest.mark.asyncio
async def test_old_pushes_not_counted(migrated_pool: AsyncConnectionPool) -> None:
    """should not count pushes older than 7 days in the rolling window."""
    from decision_ledger.telegram.rate_limiter import RateLimiter

    rl = RateLimiter(migrated_pool)
    chat_id = "12345"

    # 手动插入一条 8 天前的 weekly push
    eight_days_ago = datetime.now(tz=UTC) - timedelta(days=8)
    async with migrated_pool.connection() as conn:
        await conn.execute(
            """
            INSERT INTO telegram_pushes (chat_id, push_type, pushed_at)
            VALUES (?, 'weekly', ?)
            """,
            (chat_id, eight_days_ago.isoformat()),
        )
        await conn.commit()

    # 8 天前的不算，当前 window 内没有 weekly → 应允许
    result = await rl.try_push(chat_id, push_type="weekly")
    assert result is True


@pytest.mark.asyncio
async def test_weekly_and_event_independent(migrated_pool: AsyncConnectionPool) -> None:
    """should count weekly and event pushes independently."""
    from decision_ledger.telegram.rate_limiter import RateLimiter

    rl = RateLimiter(migrated_pool)
    chat_id = "12345"

    # weekly 用满 1 次
    await rl.try_push(chat_id, push_type="weekly")

    # event 仍可 push 5 次
    event_results = [await rl.try_push(chat_id, push_type="event") for _ in range(5)]
    assert all(event_results)

    # weekly 被 block，event 也被 block
    assert await rl.try_push(chat_id, push_type="weekly") is False
    assert await rl.try_push(chat_id, push_type="event") is False


@pytest.mark.asyncio
async def test_different_chat_ids_independent(migrated_pool: AsyncConnectionPool) -> None:
    """should track rate limits per chat_id independently."""
    from decision_ledger.telegram.rate_limiter import RateLimiter

    rl = RateLimiter(migrated_pool)
    chat_id_a = "111"
    chat_id_b = "222"

    # A 用满 weekly
    await rl.try_push(chat_id_a, push_type="weekly")
    assert await rl.try_push(chat_id_a, push_type="weekly") is False

    # B 的 weekly 仍未使用
    assert await rl.try_push(chat_id_b, push_type="weekly") is True
