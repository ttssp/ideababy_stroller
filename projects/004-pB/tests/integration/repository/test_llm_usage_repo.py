"""
LLMUsageRepository 集成测试 — T003
结论: 验证 insert / monthly_total_cost / cache_hit_rate
"""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

import pytest

from decision_ledger.domain.llm_usage import LLMUsage
from decision_ledger.repository.base import AsyncConnectionPool
from decision_ledger.repository.llm_usage_repo import LLMUsageRepository


def _make_usage(
    service: str = "ConflictReportAssembler",
    cost_usd: float = 0.01,
    cache_hit: bool = False,
    created_at: datetime | None = None,
) -> LLMUsage:
    """构造测试用 LLMUsage。"""
    return LLMUsage(
        call_id=str(uuid4()),
        service=service,
        model="claude-sonnet-4-6",
        prompt_template_version="conflict_v1",
        prompt_tokens=1000,
        output_tokens=200,
        cost_usd=cost_usd,
        cache_hit=cache_hit,
        latency_ms=1200,
        created_at=created_at or datetime.now(tz=UTC),
    )


@pytest.mark.asyncio
async def test_insert_should_persist_llm_usage_record(
    migrated_pool: AsyncConnectionPool,
) -> None:
    """结论: insert 不应抛出异常，记录正常入库。"""
    repo = LLMUsageRepository(migrated_pool)
    usage = _make_usage()
    # 不应抛出
    await repo.insert(usage)


@pytest.mark.asyncio
async def test_monthly_total_cost_should_sum_costs_within_month(
    migrated_pool: AsyncConnectionPool,
) -> None:
    """结论: monthly_total_cost(2026, 4) 应汇总 2026-04 内的 cost_usd 之和。"""
    repo = LLMUsageRepository(migrated_pool)

    # 插入 3 条 2026-04 的记录
    april = datetime(2026, 4, 15, tzinfo=UTC)
    for _ in range(3):
        await repo.insert(_make_usage(cost_usd=0.05, created_at=april))

    # 插入 1 条 2026-03 的记录（不计入）
    march = datetime(2026, 3, 20, tzinfo=UTC)
    await repo.insert(_make_usage(cost_usd=1.0, created_at=march))

    total = await repo.monthly_total_cost(2026, 4)
    assert abs(total - 0.15) < 1e-9


@pytest.mark.asyncio
async def test_monthly_total_cost_should_return_zero_when_no_records(
    migrated_pool: AsyncConnectionPool,
) -> None:
    """结论: 无记录时 monthly_total_cost 应返回 0.0。"""
    repo = LLMUsageRepository(migrated_pool)
    total = await repo.monthly_total_cost(2099, 1)
    assert total == 0.0


@pytest.mark.asyncio
async def test_cache_hit_rate_should_calculate_correctly(
    migrated_pool: AsyncConnectionPool,
) -> None:
    """结论: cache_hit_rate 应返回 cache_hit=True 的比例。"""
    repo = LLMUsageRepository(migrated_pool)

    # 2 hit + 2 miss = 0.5 命中率
    await repo.insert(_make_usage(cache_hit=True, service="TestService"))
    await repo.insert(_make_usage(cache_hit=True, service="TestService"))
    await repo.insert(_make_usage(cache_hit=False, service="TestService"))
    await repo.insert(_make_usage(cache_hit=False, service="TestService"))

    rate = await repo.cache_hit_rate(service="TestService")
    assert abs(rate - 0.5) < 1e-9


@pytest.mark.asyncio
async def test_cache_hit_rate_should_return_zero_when_no_records(
    migrated_pool: AsyncConnectionPool,
) -> None:
    """结论: 无记录时 cache_hit_rate 应返回 0.0。"""
    repo = LLMUsageRepository(migrated_pool)
    rate = await repo.cache_hit_rate(service="NonExistentService")
    assert rate == 0.0
