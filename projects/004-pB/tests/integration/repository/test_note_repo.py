"""
NoteRepository 集成测试 — T003
结论: 验证 insert / find_by_content_hash / search_fulltext
"""

from __future__ import annotations

import hashlib
from datetime import UTC, datetime
from uuid import uuid4

import pytest

from decision_ledger.domain.note import Note
from decision_ledger.repository.base import AsyncConnectionPool
from decision_ledger.repository.note_repo import NoteRepository


def _make_note(title: str = "测试笔记", content: str = "笔记内容") -> Note:
    """构造测试用 Note，自动生成 content_hash。"""
    content_hash = hashlib.sha256(content.encode()).hexdigest()
    return Note(
        note_id=str(uuid4()),
        title=title,
        content=content,
        tags=["test", "integration"],
        content_hash=content_hash,
        created_at=datetime.now(tz=UTC),
        updated_at=datetime.now(tz=UTC),
    )


@pytest.mark.asyncio
async def test_insert_and_find_by_content_hash_should_round_trip(
    migrated_pool: AsyncConnectionPool,
) -> None:
    """结论: insert 后 find_by_content_hash 应返回相同内容的 Note。"""
    repo = NoteRepository(migrated_pool)
    note = _make_note(content="唯一内容 ABC123")
    await repo.insert(note)

    fetched = await repo.find_by_content_hash(note.content_hash)
    assert fetched is not None
    assert fetched.note_id == note.note_id
    assert fetched.title == note.title
    assert fetched.content == note.content
    assert fetched.content_hash == note.content_hash


@pytest.mark.asyncio
async def test_find_by_content_hash_should_return_none_when_not_found(
    migrated_pool: AsyncConnectionPool,
) -> None:
    """结论: 查询不存在的 content_hash 应返回 None。"""
    repo = NoteRepository(migrated_pool)
    result = await repo.find_by_content_hash("nonexistent-hash-0000000000000000")
    assert result is None


@pytest.mark.asyncio
async def test_insert_should_be_idempotent_when_same_content_hash(
    migrated_pool: AsyncConnectionPool,
) -> None:
    """结论: 重复插入相同 content_hash 应幂等（INSERT OR IGNORE），不抛异常不重复。"""
    repo = NoteRepository(migrated_pool)
    note = _make_note(content="重复内容测试")
    await repo.insert(note)
    # 第二次插入相同 content_hash — 应静默忽略
    note_dup = Note(
        note_id=str(uuid4()),  # 不同 note_id 但 content_hash 相同
        title="另一标题",
        content="重复内容测试",
        tags=[],
        content_hash=note.content_hash,
        created_at=datetime.now(tz=UTC),
        updated_at=datetime.now(tz=UTC),
    )
    await repo.insert(note_dup)

    # 应只有一条记录（原始的）
    fetched = await repo.find_by_content_hash(note.content_hash)
    assert fetched is not None
    assert fetched.note_id == note.note_id  # 原始记录，不是 dup


@pytest.mark.asyncio
async def test_search_fulltext_should_match_title_and_content(
    migrated_pool: AsyncConnectionPool,
) -> None:
    """结论: search_fulltext 应在 title 和 content 中搜索关键字。"""
    repo = NoteRepository(migrated_pool)

    note_a = _make_note(title="AAPL 分析笔记", content="苹果公司季报超预期")
    note_b = _make_note(title="市场综述", content="AAPL 带动科技板块上涨")
    note_c = _make_note(title="TSLA 分析", content="特斯拉交付量创新高")

    await repo.insert(note_a)
    await repo.insert(note_b)
    await repo.insert(note_c)

    results = await repo.search_fulltext("AAPL")
    assert len(results) == 2
    ids = {r.note_id for r in results}
    assert note_a.note_id in ids
    assert note_b.note_id in ids


@pytest.mark.asyncio
async def test_search_fulltext_should_return_empty_when_no_match(
    migrated_pool: AsyncConnectionPool,
) -> None:
    """结论: 没有匹配的搜索应返回空列表。"""
    repo = NoteRepository(migrated_pool)
    result = await repo.search_fulltext("ZZZNOMATCH99999")
    assert result == []
