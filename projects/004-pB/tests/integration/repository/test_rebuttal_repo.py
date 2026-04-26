"""
RebuttalRepository 集成测试 — T003
结论: 验证 insert / get_for_decision
"""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

import pytest

from decision_ledger.domain.rebuttal import Rebuttal
from decision_ledger.repository.base import AsyncConnectionPool
from decision_ledger.repository.rebuttal_repo import RebuttalRepository


@pytest.mark.asyncio
async def test_insert_and_get_for_decision_should_round_trip(
    migrated_pool: AsyncConnectionPool,
) -> None:
    """结论: insert 后 get_for_decision 应返回相同内容的 Rebuttal。"""
    repo = RebuttalRepository(migrated_pool)
    rebuttal_id = str(uuid4())
    rebuttal = Rebuttal(
        rebuttal_text="市场已定价，风险可控",
        invoked_at=datetime.now(tz=UTC).isoformat(),
    )
    await repo.insert(rebuttal_id, rebuttal)

    fetched = await repo.get_for_decision(rebuttal_id)
    assert fetched is not None
    assert fetched.rebuttal_text == "市场已定价，风险可控"
    assert fetched.invoked_at == rebuttal.invoked_at


@pytest.mark.asyncio
async def test_get_for_decision_should_return_none_when_not_found(
    migrated_pool: AsyncConnectionPool,
) -> None:
    """结论: 查询不存在的 rebuttal_id 应返回 None。"""
    repo = RebuttalRepository(migrated_pool)
    result = await repo.get_for_decision("nonexistent-rebuttal-id")
    assert result is None
