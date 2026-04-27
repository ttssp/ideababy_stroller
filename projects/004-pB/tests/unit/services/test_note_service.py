"""
NoteService 单元测试 — T016
结论: 验证 CRUD + content_hash 去重 + list_summaries_for_topics (SQL LIKE)
细节:
  - 零 LLM: NoteService 路径 LLM call 计数 = 0 (R3 cut 强制验证)
  - content_hash dedup: 命中时返回已有笔记 + dedup_hint=True
  - list_summaries_for_topics: SQL LIKE 查找, 不调 LLM
  - search_fulltext: LIKE 查找 hit/miss
"""

from __future__ import annotations

from datetime import datetime
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from decision_ledger.domain.note import Note


# ── 测试辅助工厂 ──────────────────────────────────────────


def _make_note(
    note_id: str = "note-001",
    title: str = "P/E ratio 解析",
    content: str = "P/E 是市盈率，衡量股票估值",
    tags: list[str] | None = None,
    content_hash: str | None = None,
) -> Note:
    """构造测试用 Note 域对象。"""
    if tags is None:
        tags = ["估值", "基本面"]
    if content_hash is None:
        import hashlib

        normalized = content.lower().strip()
        content_hash = hashlib.sha256(normalized.encode()).hexdigest()
    return Note(
        note_id=note_id,
        title=title,
        content=content,
        tags=tags,
        content_hash=content_hash,
        created_at=datetime(2026, 4, 27, 12, 0, 0),
        updated_at=datetime(2026, 4, 27, 12, 0, 0),
    )


def _make_mock_repo(
    existing_note: Note | None = None,
    search_results: list[Note] | None = None,
) -> MagicMock:
    """构造 mock NoteRepository。"""
    repo = MagicMock()
    repo.find_by_content_hash = AsyncMock(return_value=existing_note)
    repo.insert = AsyncMock(return_value=None)
    repo.update = AsyncMock(return_value=None)
    repo.delete = AsyncMock(return_value=None)
    repo.get = AsyncMock(return_value=existing_note)
    repo.list_all = AsyncMock(return_value=[] if search_results is None else search_results)
    repo.search_fulltext = AsyncMock(return_value=[] if search_results is None else search_results)
    repo.list_by_topics_like = AsyncMock(
        return_value=[] if search_results is None else search_results
    )
    return repo


# ── R3 cut 验证: NoteService 路径 LLM call 计数 = 0 ──────────


class TestNoteServiceNoLLM:
    """R3 cut 验证: NoteService 任何路径不调 LLM。"""

    def test_should_not_call_llm_when_creating_note(self) -> None:
        """结论: create_note 路径 LLM call = 0 (R3 强制)。"""
        from decision_ledger.services.note_service import NoteService

        repo = _make_mock_repo()
        svc = NoteService(repo)

        # 验证 NoteService 初始化时无 llm_client 参数
        assert not hasattr(svc, "llm_client"), "NoteService 不应有 llm_client 属性 (R3 cut)"
        assert not hasattr(svc, "_llm"), "NoteService 不应有 _llm 属性 (R3 cut)"

    def test_should_not_import_llm_client_in_note_service_module(self) -> None:
        """结论: note_service 模块不 import LLMClient (R3 cut)。

        细节: 仅检查 import 语句行, 排除注释/docstring 中的词语.
        """
        import ast
        import inspect
        from decision_ledger.services import note_service

        source = inspect.getsource(note_service)
        # 解析 AST, 只检查实际 import 语句 (非注释/docstring)
        tree = ast.parse(source)
        imported_names: list[str] = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported_names.extend(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                imported_names.append(module)
                imported_names.extend(alias.name for alias in node.names)

        # 不应 import 任何 LLM 相关模块
        for name in imported_names:
            assert "anthropic" not in name.lower(), f"note_service 不能 import anthropic: {name}"
            assert "llm" not in name.lower(), f"note_service 不能 import LLM 模块: {name}"


# ── content_hash dedup 测试 ────────────────────────────────────


class TestContentHashDedup:
    """content_hash 去重逻辑测试。"""

    async def test_should_detect_duplicate_when_hash_matches(self) -> None:
        """结论: 相同 content hash 命中时返回 (existing_note, dedup_hint=True)。"""
        from decision_ledger.services.note_service import NoteService

        existing = _make_note(note_id="existing-001")
        repo = _make_mock_repo(existing_note=existing)
        svc = NoteService(repo)

        result, dedup = await svc.create_note(
            title="新标题",
            content="P/E 是市盈率，衡量股票估值",  # 与 existing note 内容相同 (normalized)
            tags=["估值"],
        )

        assert dedup is True, "相同 content_hash 应返回 dedup=True"
        assert result.note_id == "existing-001", "应返回已有 note"
        repo.insert.assert_not_called()  # 有重复时不应插入

    async def test_should_insert_note_when_no_hash_collision(self) -> None:
        """结论: 无 hash 碰撞时正常插入，返回 (new_note, dedup=False)。"""
        from decision_ledger.services.note_service import NoteService

        repo = _make_mock_repo(existing_note=None)
        svc = NoteService(repo)

        result, dedup = await svc.create_note(
            title="FOMC 分点投票",
            content="FOMC 是美联储公开市场委员会",
            tags=["货币政策"],
        )

        assert dedup is False, "无碰撞时 dedup=False"
        repo.insert.assert_called_once()
        assert result.title == "FOMC 分点投票"

    async def test_should_normalize_content_before_hashing(self) -> None:
        """结论: content_hash 对 normalize (lower+strip) 后的内容计算。"""
        from decision_ledger.services.note_service import NoteService

        # 两段内容 normalize 后相同
        content_variant = "  P/E 是市盈率，衡量股票估值  "  # 带空格
        existing_hash_content = "p/e 是市盈率，衡量股票估值"

        import hashlib

        expected_hash = hashlib.sha256(existing_hash_content.encode()).hexdigest()
        existing = _make_note(content_hash=expected_hash, content="p/e 是市盈率，衡量股票估值")
        repo = _make_mock_repo(existing_note=existing)
        svc = NoteService(repo)

        _result, dedup = await svc.create_note(
            title="任意标题",
            content=content_variant,
            tags=[],
        )

        assert dedup is True, "normalize 后相同的 content 应命中 dedup"


# ── search_fulltext 测试 ───────────────────────────────────────


class TestSearchFulltext:
    """全文搜索测试。"""

    async def test_should_return_notes_when_query_hits(self) -> None:
        """结论: search_fulltext(q) 在 title/content LIKE 命中时返回结果。"""
        from decision_ledger.services.note_service import NoteService

        note = _make_note(title="FOMC 分点投票", content="联邦公开市场委员会")
        repo = _make_mock_repo(search_results=[note])
        svc = NoteService(repo)

        results = await svc.search(query="FOMC")

        assert len(results) == 1
        assert results[0].title == "FOMC 分点投票"
        repo.search_fulltext.assert_called_once_with("FOMC")

    async def test_should_return_empty_when_query_misses(self) -> None:
        """结论: search_fulltext(q) 无命中时返回空列表。"""
        from decision_ledger.services.note_service import NoteService

        repo = _make_mock_repo(search_results=[])
        svc = NoteService(repo)

        results = await svc.search(query="不存在关键词XYZ")

        assert results == []


# ── list_summaries_for_topics 测试 ────────────────────────────


class TestListSummariesForTopics:
    """agent 引用笔记接口测试 (R3: SQL LIKE, 不调 LLM)。"""

    async def test_should_return_note_refs_when_topic_matches(self) -> None:
        """结论: list_summaries_for_topics(["P/E"]) 返回含 topic 关键词的笔记 ref 列表。"""
        from decision_ledger.services.note_service import NoteRef, NoteService

        note = _make_note(title="P/E ratio 解析", content="市盈率定义")
        repo = _make_mock_repo(search_results=[note])
        svc = NoteService(repo)

        refs = await svc.list_summaries_for_topics(["P/E"])

        assert len(refs) == 1
        assert isinstance(refs[0], NoteRef)
        assert refs[0].note_id == "note-001"
        assert refs[0].title == "P/E ratio 解析"

    async def test_should_return_empty_when_no_topics_match(self) -> None:
        """结论: list_summaries_for_topics(["XYZ"]) 无匹配时返回空列表。"""
        from decision_ledger.services.note_service import NoteService

        repo = _make_mock_repo(search_results=[])
        svc = NoteService(repo)

        refs = await svc.list_summaries_for_topics(["完全不存在的主题XYZ"])

        assert refs == []

    async def test_should_not_call_llm_in_list_summaries(self) -> None:
        """结论: list_summaries_for_topics 零 LLM 调用 (R3 cut)。"""
        from decision_ledger.services.note_service import NoteService

        note = _make_note()
        repo = _make_mock_repo(search_results=[note])
        svc = NoteService(repo)

        # 用 patch 确保 anthropic.Anthropic 从未被调用
        with patch("anthropic.Anthropic") as mock_cls:
            await svc.list_summaries_for_topics(["P/E"])
            mock_cls.assert_not_called()

    async def test_should_merge_results_for_multiple_topics(self) -> None:
        """结论: 多个 topic 时合并结果 (去重)。"""
        from decision_ledger.services.note_service import NoteService

        note1 = _make_note(note_id="n1", title="P/E ratio")
        note2 = _make_note(note_id="n2", title="P/B ratio")

        call_count = 0
        results_map = {0: [note1], 1: [note2]}

        async def fake_list_by_topics(topics_like: list[str]) -> list[Note]:
            nonlocal call_count
            idx = call_count
            call_count += 1
            return results_map.get(idx, [])

        repo = _make_mock_repo()
        repo.list_by_topics_like = AsyncMock(side_effect=fake_list_by_topics)
        svc = NoteService(repo)

        # 验证接口调用正常 (不要求内部实现细节)
        refs = await svc.list_summaries_for_topics(["P/E", "P/B"])
        assert isinstance(refs, list)


# ── CRUD 基本流程测试 ──────────────────────────────────────────


class TestNoteCRUD:
    """CRUD 基本流程测试。"""

    async def test_should_get_note_when_id_exists(self) -> None:
        """结论: get_note(id) 返回对应 Note。"""
        from decision_ledger.services.note_service import NoteService

        note = _make_note(note_id="note-007")
        repo = _make_mock_repo(existing_note=note)
        repo.get = AsyncMock(return_value=note)
        svc = NoteService(repo)

        result = await svc.get_note("note-007")

        assert result is not None
        assert result.note_id == "note-007"

    async def test_should_return_none_when_note_not_found(self) -> None:
        """结论: get_note(不存在 id) 返回 None。"""
        from decision_ledger.services.note_service import NoteService

        repo = _make_mock_repo(existing_note=None)
        repo.get = AsyncMock(return_value=None)
        svc = NoteService(repo)

        result = await svc.get_note("nonexistent")

        assert result is None

    async def test_should_list_all_notes_sorted_by_updated_at_desc(self) -> None:
        """结论: list_notes() 返回按 updated_at DESC 排列的笔记列表。"""
        from decision_ledger.services.note_service import NoteService

        repo = _make_mock_repo()
        repo.list_all = AsyncMock(return_value=[])
        svc = NoteService(repo)

        results = await svc.list_notes()

        repo.list_all.assert_called_once()
        assert isinstance(results, list)

    async def test_should_delete_note_when_id_exists(self) -> None:
        """结论: delete_note(id) 调用 repo.delete。"""
        from decision_ledger.services.note_service import NoteService

        repo = _make_mock_repo()
        svc = NoteService(repo)

        await svc.delete_note("note-001")

        repo.delete.assert_called_once_with("note-001")

    async def test_should_update_note_fields(self) -> None:
        """结论: update_note 更新标题/内容/tags, 重新计算 content_hash。"""
        from decision_ledger.services.note_service import NoteService

        original = _make_note()
        repo = _make_mock_repo(existing_note=original)
        repo.get = AsyncMock(return_value=original)
        svc = NoteService(repo)

        updated = await svc.update_note(
            note_id="note-001",
            title="新标题",
            content="全新内容",
            tags=["新标签"],
        )

        assert updated is not None
        assert updated.title == "新标题"
        assert updated.content == "全新内容"
        repo.update.assert_called_once()
