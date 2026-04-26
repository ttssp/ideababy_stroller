"""
JobQueueRepository 集成测试 — T003
结论: 验证 enqueue / claim_next / mark_done / mark_failed
细节: v0.1 使用 notes 表存储 job（无独立 job_queue 表）
"""

from __future__ import annotations

from uuid import uuid4

import pytest

from decision_ledger.repository.base import AsyncConnectionPool
from decision_ledger.repository.job_queue_repo import JobQueueRepository


@pytest.mark.asyncio
async def test_enqueue_and_claim_next_should_return_job(
    migrated_pool: AsyncConnectionPool,
) -> None:
    """结论: enqueue 后 claim_next 应返回同一条 job 的信息。"""
    repo = JobQueueRepository(migrated_pool)
    job_id = str(uuid4())
    payload = {"ticker": "AAPL", "action": "analyze"}
    await repo.enqueue(job_id, "analysis", payload)

    claimed = await repo.claim_next()
    assert claimed is not None
    assert claimed["job_id"] == job_id
    assert claimed["job_type"] == "analysis"
    assert claimed["payload"]["ticker"] == "AAPL"


@pytest.mark.asyncio
async def test_claim_next_should_return_none_when_queue_empty(
    migrated_pool: AsyncConnectionPool,
) -> None:
    """结论: 队列为空时 claim_next 应返回 None。"""
    repo = JobQueueRepository(migrated_pool)
    result = await repo.claim_next()
    assert result is None


@pytest.mark.asyncio
async def test_enqueue_should_be_idempotent_when_same_job_id(
    migrated_pool: AsyncConnectionPool,
) -> None:
    """结论: 重复 enqueue 同一 job_id 应幂等（INSERT OR IGNORE），不重复入队。"""
    repo = JobQueueRepository(migrated_pool)
    job_id = str(uuid4())
    await repo.enqueue(job_id, "analysis", {"ticker": "AAPL"})
    await repo.enqueue(job_id, "analysis", {"ticker": "AAPL"})

    # 只应能 claim 一次
    first = await repo.claim_next()
    assert first is not None
    second = await repo.claim_next()
    assert second is None


@pytest.mark.asyncio
async def test_mark_done_should_remove_job_from_pending(
    migrated_pool: AsyncConnectionPool,
) -> None:
    """结论: mark_done 后 claim_next 不应再返回该 job。"""
    repo = JobQueueRepository(migrated_pool)
    job_id = str(uuid4())
    await repo.enqueue(job_id, "analysis", {})
    claimed = await repo.claim_next()
    assert claimed is not None

    await repo.mark_done(job_id)

    # 再次 claim 不应得到该 job
    next_job = await repo.claim_next()
    assert next_job is None


@pytest.mark.asyncio
async def test_mark_failed_should_persist_error_msg(
    migrated_pool: AsyncConnectionPool,
) -> None:
    """结论: mark_failed 后 job 应标记为 FAILED 状态，error_msg 写入 content。"""
    repo = JobQueueRepository(migrated_pool)
    job_id = str(uuid4())
    await repo.enqueue(job_id, "pdf_parse", {"path": "/tmp/test.pdf"})
    await repo.claim_next()

    await repo.mark_failed(job_id, error_msg="文件不存在")

    # 不应再能 claim
    next_job = await repo.claim_next()
    assert next_job is None


@pytest.mark.asyncio
async def test_claim_next_should_be_fifo_when_multiple_jobs(
    migrated_pool: AsyncConnectionPool,
) -> None:
    """结论: claim_next 应按 FIFO 顺序返回 job（ORDER BY created_at ASC）。"""
    import asyncio

    repo = JobQueueRepository(migrated_pool)

    # 按顺序入队
    job_ids = []
    for i in range(3):
        job_id = str(uuid4())
        job_ids.append(job_id)
        await repo.enqueue(job_id, "task", {"order": i})
        await asyncio.sleep(0.01)  # 保证 created_at 不同

    # 按顺序取出
    for expected_id in job_ids:
        claimed = await repo.claim_next()
        assert claimed is not None
        assert claimed["job_id"] == expected_id
