"""
Telegram cadence 集成测试 — O8 SLA 验证
结论: 模拟 10 天内多次触发，断言任意 7 天滚动 ≤ 1 周报 + 5 event
细节:
  - test_rolling_window_weekly_limit: 10 天内尝试 push 5 次 weekly，只有第 1、8+ 天允许
  - test_rolling_window_event_limit: 10 天内尝试 push 12 次 event，验证每 7 天最多 5 次
  - test_mixed_push_cadence: 混合 weekly + event 节奏验证
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

PROJECT_ROOT = Path(__file__).resolve().parents[2]  # tests/integration/../.. → project root


@pytest_asyncio.fixture
async def migrated_pool(tmp_path: Path) -> AsyncIterator[AsyncConnectionPool]:
    """提供经过 alembic upgrade head 迁移的 AsyncConnectionPool。"""
    db_path = tmp_path / "test_cadence.sqlite"
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


async def _insert_push(
    pool: AsyncConnectionPool,
    chat_id: str,
    push_type: str,
    pushed_at: datetime,
) -> None:
    """直接插入历史推送记录（绕过 rate_limiter 的检查，模拟历史数据）。"""
    async with pool.connection() as conn:
        await conn.execute(
            """
            INSERT INTO telegram_pushes (chat_id, push_type, pushed_at)
            VALUES (?, ?, ?)
            """,
            (chat_id, push_type, pushed_at.isoformat()),
        )
        await conn.commit()


@pytest.mark.asyncio
async def test_rolling_window_weekly_limit(migrated_pool: AsyncConnectionPool) -> None:
    """should enforce ≤ 1 weekly push per 7-day rolling window over 10 days."""
    from decision_ledger.telegram.rate_limiter import RateLimiter

    rl = RateLimiter(migrated_pool)
    chat_id = "12345"
    now = datetime.now(tz=UTC)

    # Day 0: push weekly → allowed
    result_d0 = await rl.try_push(chat_id, push_type="weekly", reference_time=now)
    assert result_d0 is True, "Day 0 weekly should be allowed"

    # Day 3: push weekly → blocked (within 7-day window)
    result_d3 = await rl.try_push(
        chat_id, push_type="weekly", reference_time=now + timedelta(days=3)
    )
    assert result_d3 is False, "Day 3 weekly should be blocked (within 7-day window)"

    # Day 6: push weekly → blocked (still within 7-day window)
    result_d6 = await rl.try_push(
        chat_id, push_type="weekly", reference_time=now + timedelta(days=6)
    )
    assert result_d6 is False, "Day 6 weekly should be blocked (still within 7-day window)"

    # Day 8: push weekly → allowed (Day 0 push is now > 7 days ago)
    result_d8 = await rl.try_push(
        chat_id, push_type="weekly", reference_time=now + timedelta(days=8)
    )
    assert result_d8 is True, "Day 8 weekly should be allowed (window rolled past Day 0)"


@pytest.mark.asyncio
async def test_rolling_window_event_limit(migrated_pool: AsyncConnectionPool) -> None:
    """should enforce ≤ 5 event pushes per 7-day rolling window."""
    from decision_ledger.telegram.rate_limiter import RateLimiter

    rl = RateLimiter(migrated_pool)
    chat_id = "12345"
    now = datetime.now(tz=UTC)

    # Days 0-4: push 5 events → all allowed
    for i in range(5):
        result = await rl.try_push(
            chat_id, push_type="event", reference_time=now + timedelta(hours=i)
        )
        assert result is True, f"Event {i+1} should be allowed"

    # Day 0 + 6h: push 6th event → blocked
    result_6th = await rl.try_push(
        chat_id, push_type="event", reference_time=now + timedelta(hours=6)
    )
    assert result_6th is False, "6th event should be blocked"

    # Day 8: push event → allowed (earlier events rolled out of 7-day window)
    result_d8 = await rl.try_push(
        chat_id, push_type="event", reference_time=now + timedelta(days=8)
    )
    assert result_d8 is True, "Event on Day 8 should be allowed (window rolled)"


@pytest.mark.asyncio
async def test_mixed_push_cadence(migrated_pool: AsyncConnectionPool) -> None:
    """should correctly handle mixed weekly + event push cadence over 10 days."""
    from decision_ledger.telegram.rate_limiter import RateLimiter

    rl = RateLimiter(migrated_pool)
    chat_id = "12345"
    now = datetime.now(tz=UTC)

    # Day 0: 1 weekly + 3 events
    assert await rl.try_push(chat_id, push_type="weekly", reference_time=now) is True
    for _ in range(3):
        assert await rl.try_push(chat_id, push_type="event", reference_time=now) is True

    # Day 2: 2nd weekly → blocked; 2 more events → allowed (total 5)
    assert (
        await rl.try_push(chat_id, push_type="weekly", reference_time=now + timedelta(days=2))
        is False
    )
    for _ in range(2):
        assert (
            await rl.try_push(
                chat_id, push_type="event", reference_time=now + timedelta(days=2)
            )
            is True
        )

    # Day 3: 6th event → blocked
    assert (
        await rl.try_push(chat_id, push_type="event", reference_time=now + timedelta(days=3))
        is False
    )

    # Day 8: window rolled, both types available again
    assert (
        await rl.try_push(chat_id, push_type="weekly", reference_time=now + timedelta(days=8))
        is True
    )
    assert (
        await rl.try_push(chat_id, push_type="event", reference_time=now + timedelta(days=8))
        is True
    )


@pytest.mark.asyncio
async def test_any_7day_window_never_exceeds_limits(migrated_pool: AsyncConnectionPool) -> None:
    """O8 SLA: 任意 7 天滚动窗口内 ≤ 1 weekly + ≤ 5 event。"""
    from decision_ledger.telegram.rate_limiter import RateLimiter

    rl = RateLimiter(migrated_pool)
    chat_id = "check-sla"
    now = datetime.now(tz=UTC)

    # 模拟 10 天每天 push: weekly + 2 events
    push_log: list[tuple[str, datetime, bool]] = []
    for day in range(10):
        ts = now + timedelta(days=day)
        weekly_result = await rl.try_push(chat_id, push_type="weekly", reference_time=ts)
        push_log.append(("weekly", ts, weekly_result))

        for _ev in range(2):
            event_result = await rl.try_push(chat_id, push_type="event", reference_time=ts)
            push_log.append(("event", ts, event_result))

    # 对每个允许的 push，验证其 7 天窗口内 weekly ≤ 1, event ≤ 5
    for push_type, pushed_at, allowed in push_log:
        if not allowed:
            continue
        window_start = pushed_at - timedelta(days=7)
        window_count = sum(
            1
            for pt, ts, ok in push_log
            if ok and pt == push_type and window_start <= ts <= pushed_at
        )
        limit = 1 if push_type == "weekly" else 5
        assert window_count <= limit, (
            f"SLA 违规: {push_type} @ {pushed_at.date()} 7天窗口内 {window_count} 次 (limit={limit})"
        )
