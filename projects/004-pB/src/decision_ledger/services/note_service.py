"""
NoteService — T016 (R3 简化版, 零 LLM)
结论: 笔记 wiki CRUD + content_hash 同步去重 + FTS5 全文搜索 + agent 引用接口
细节:
  - create_note: content_hash 同步去重 (sha256, normalize=lower+strip), 无 LLM
  - search: 委托 NoteRepository.search_fulltext (LIKE 查找)
  - list_summaries_for_topics: SQL LIKE 查找含 topic 关键词的笔记 ref, 不调 LLM
  - R3 真砍: 无 LLM 语义去重, 无 note_dedup prompt
"""

from __future__ import annotations

import hashlib
import uuid
from dataclasses import dataclass
from datetime import datetime

from decision_ledger.domain.note import Note

# ── NoteRef: agent 引用笔记的轻量类型 ──────────────────────────────────────────


@dataclass(frozen=True)
class NoteRef:
    """笔记引用 (轻量, 供 agent T015/T019 调用)。

    结论: 仅含 note_id + title + snippet, 不含完整 content (减少 context size).
    """

    note_id: str
    title: str
    snippet: str  # content 前 120 字符


# ── NoteService ────────────────────────────────────────────────────────────────


class NoteService:
    """笔记 wiki CRUD + 去重 + 搜索 + agent 引用接口 (R3 简化版, 零 LLM)。

    架构约束 (R3):
      - 无 LLM 调用: 去重仅用 content_hash (sha256), 搜索仅用 SQL LIKE
      - 不依赖 LLMClient: __init__ 只接受 NoteRepository
    """

    def __init__(self, repo: object) -> None:
        """
        结论: 仅注入 NoteRepository, 无 LLM 依赖 (R3 cut).
        参数:
          repo: NoteRepository 实例 (duck typing, 避免循环 import)
        """
        self._repo = repo

    # ── 内部工具 ───────────────────────────────────────────────────────────────

    @staticmethod
    def _compute_content_hash(content: str) -> str:
        """计算 normalize 后 content 的 sha256 hash (R3: lower + strip).

        结论: 大小写/首尾空格不同但语义相同的 content 命中同一 hash.
        """
        normalized = content.lower().strip()
        return hashlib.sha256(normalized.encode()).hexdigest()

    # ── CRUD ───────────────────────────────────────────────────────────────────

    async def create_note(
        self,
        title: str,
        content: str,
        tags: list[str],
    ) -> tuple[Note, bool]:
        """创建笔记, content_hash 同步去重.

        结论: 无 LLM 调用; 仅 sha256 hash 检测重复.
        返回:
          (Note, dedup_hint): dedup_hint=True 表示相同 content 已存在, Note 为已有笔记
          (Note, False): 正常新建
        """
        content_hash = self._compute_content_hash(content)

        # 同步 hash 去重查询 (零 LLM)
        existing: Note | None = await self._repo.find_by_content_hash(content_hash)  # type: ignore[attr-defined]
        if existing is not None:
            return existing, True

        note = Note(
            note_id=str(uuid.uuid4()),
            title=title.strip(),
            content=content,
            tags=tags,
            content_hash=content_hash,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        await self._repo.insert(note)  # type: ignore[attr-defined]
        return note, False

    async def get_note(self, note_id: str) -> Note | None:
        """按 note_id 查询单条笔记.

        结论: 简单读路径, 零 LLM.
        """
        result: Note | None = await self._repo.get(note_id)  # type: ignore[attr-defined]
        return result

    async def list_notes(self) -> list[Note]:
        """列出所有笔记 (按 updated_at DESC).

        结论: NoteRepository.list_all() 负责排序.
        """
        results: list[Note] = await self._repo.list_all()  # type: ignore[attr-defined]
        return results

    async def update_note(
        self,
        note_id: str,
        title: str,
        content: str,
        tags: list[str],
    ) -> Note | None:
        """更新笔记 (title/content/tags), 重新计算 content_hash.

        结论: 更新时不做 dedup 检查 (编辑场景已知是自己的笔记).
        返回: 更新后的 Note, 或 None (note_id 不存在时).
        """
        existing: Note | None = await self._repo.get(note_id)  # type: ignore[attr-defined]
        if existing is None:
            return None

        content_hash = self._compute_content_hash(content)
        updated = Note(
            note_id=note_id,
            title=title.strip(),
            content=content,
            tags=tags,
            content_hash=content_hash,
            created_at=existing.created_at,
            updated_at=datetime.now(),
        )
        await self._repo.update(updated)  # type: ignore[attr-defined]
        return updated

    async def delete_note(self, note_id: str) -> None:
        """删除笔记.

        结论: 委托 repo.delete, 无 LLM.
        """
        await self._repo.delete(note_id)  # type: ignore[attr-defined]

    # ── 搜索 ──────────────────────────────────────────────────────────────────

    async def search(self, query: str) -> list[Note]:
        """全文搜索 (FTS5 / LIKE 查找).

        结论: 委托 NoteRepository.search_fulltext, 零 LLM.
        """
        results: list[Note] = await self._repo.search_fulltext(query)  # type: ignore[attr-defined]
        return results

    # ── agent 引用接口 (R3: SQL LIKE, 零 LLM) ─────────────────────────────────

    async def list_summaries_for_topics(self, topics: list[str]) -> list[NoteRef]:
        """返回含 topic 关键词的笔记 ref 列表 (R3 简化: SQL LIKE, 不调 LLM).

        结论: T015/T019 调用此接口获取相关笔记 snippet.
        参数:
          topics: 关键词列表, e.g. ["P/E", "FOMC"]
        返回:
          list[NoteRef]: 匹配笔记的轻量引用 (去重, 按 updated_at DESC)
        细节:
          - 每个 topic 做 SQL LIKE %topic% 查找
          - 多 topic 结果合并去重 (以 note_id 为 key)
          - R3: 不调 LLM, 不做语义相似度
        """
        seen: dict[str, Note] = {}

        for topic in topics:
            notes: list[Note] = await self._repo.list_by_topics_like([topic])  # type: ignore[attr-defined]
            for note in notes:
                if note.note_id not in seen:
                    seen[note.note_id] = note

        # 按 updated_at DESC 排序
        ordered = sorted(seen.values(), key=lambda n: n.updated_at, reverse=True)

        return [
            NoteRef(
                note_id=note.note_id,
                title=note.title,
                snippet=note.content[:120],
            )
            for note in ordered
        ]
