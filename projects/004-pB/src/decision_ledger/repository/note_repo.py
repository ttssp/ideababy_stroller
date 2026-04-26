"""
NoteRepository — T003
结论: 笔记 wiki CRUD，含 content_hash 去重 + 全文搜索
细节:
  - insert: 插入 Note（写路径，content_hash 唯一索引防重复）
  - find_by_content_hash: 去重查询（读路径）
  - search_fulltext: title + content LIKE 搜索（读路径，v0.1 简单实现）
"""

from __future__ import annotations

import json
from datetime import datetime
from typing import Any

from decision_ledger.domain.note import Note
from decision_ledger.repository.base import AsyncConnectionPool


class NoteRepository:
    """Note wiki Repository。"""

    def __init__(self, pool: AsyncConnectionPool) -> None:
        self._pool = pool

    async def insert(self, note: Note) -> None:
        """插入 Note（写路径）。

        结论: content_hash UNIQUE INDEX 防止重复插入，INSERT OR IGNORE 实现幂等。
        """
        async with self._pool.write_connection() as conn:
            await conn.execute(
                """
                INSERT OR IGNORE INTO notes (
                    note_id, title, content, tags_json, content_hash, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    note.note_id,
                    note.title,
                    note.content,
                    json.dumps(note.tags, ensure_ascii=False),
                    note.content_hash,
                    note.created_at.isoformat(),
                    note.updated_at.isoformat(),
                ),
            )
            await conn.commit()

    async def find_by_content_hash(self, content_hash: str) -> Note | None:
        """按 content_hash 去重查询（读路径）。"""
        async with self._pool.connection() as conn:
            cursor = await conn.execute(
                "SELECT * FROM notes WHERE content_hash = ?",
                (content_hash,),
            )
            row = await cursor.fetchone()
            if row is None:
                return None
            return self._row_to_note(dict(row))

    async def search_fulltext(self, query: str) -> list[Note]:
        """title + content LIKE 搜索（读路径，v0.1 简单实现）。

        结论: v0.1 用 LIKE，v0.2+ 可升级到 FTS5。
        细节: query 经过 parametrized，防止 SQL 注入（SEC-5）。
        """
        pattern = f"%{query}%"
        async with self._pool.connection() as conn:
            cursor = await conn.execute(
                """
                SELECT * FROM notes
                WHERE title LIKE ? OR content LIKE ?
                ORDER BY updated_at DESC
                """,
                (pattern, pattern),
            )
            rows = await cursor.fetchall()
            return [self._row_to_note(dict(row)) for row in rows]

    # ── 私有辅助 ──────────────────────────────────────────────────────────────

    @staticmethod
    def _row_to_note(row: dict[str, Any]) -> Note:
        """将 DB row dict 构造为 Note 域对象。"""
        return Note(
            note_id=str(row["note_id"]),
            title=str(row["title"]),
            content=str(row["content"]),
            tags=json.loads(str(row["tags_json"])),
            content_hash=str(row["content_hash"]),
            created_at=datetime.fromisoformat(str(row["created_at"])),
            updated_at=datetime.fromisoformat(str(row["updated_at"])),
        )
