"""
JobQueueRepository — T003
结论: 轻量作业队列，v0.1 用 notes 表持久化（无独立 job_queue 表）
细节:
  - enqueue: 写入 job（序列化为 notes 行，tag=["job_queue"]，status 在 title 前缀）
  - claim_next: 原子取下一条 pending job 并标记 claimed（写路径）
  - mark_done: 更新 job status=done（写路径）
  - mark_failed: 更新 job status=failed + error_msg（写路径）

  v0.1 妥协: notes 表无专用 status 字段，用 title 前缀约定：
    "JOB_PENDING|{job_id}|{job_type}" / "JOB_CLAIMED|..." / "JOB_DONE|..." / "JOB_FAILED|..."
  v0.2 升级路径: 添加 job_queue 表（独立 status 字段，无需解析 title）

  架构约束（TECH-1）: 所有写入在 asyncio.Lock 内（≤ 100ms），不调 LLM
"""

from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from typing import Any

from decision_ledger.repository.base import AsyncConnectionPool

# ── 内部常量 ────────────────────────────────────────────────────────────────

_PENDING = "JOB_PENDING"
_CLAIMED = "JOB_CLAIMED"
_DONE = "JOB_DONE"
_FAILED = "JOB_FAILED"
_JOB_TAG = json.dumps(["job_queue"])


def _make_title(status: str, job_id: str, job_type: str) -> str:
    """结论: title 约定格式，用于 status 过滤（LIKE 'JOB_PENDING|%'）。"""
    return f"{status}|{job_id}|{job_type}"


def _parse_title(title: str) -> tuple[str, str, str]:
    """结论: 解析 title 为 (status, job_id, job_type)。"""
    parts = title.split("|", 2)
    if len(parts) != 3:
        return ("UNKNOWN", title, "unknown")
    return (parts[0], parts[1], parts[2])


class JobQueueRepository:
    """轻量作业队列 Repository（v0.1 用 notes 表持久化）。"""

    def __init__(self, pool: AsyncConnectionPool) -> None:
        self._pool = pool

    async def enqueue(
        self,
        job_id: str,
        job_type: str,
        payload: dict[str, Any],
    ) -> None:
        """将 job 入队（写路径）。

        结论: job 存为 note 行，title 前缀=JOB_PENDING，content=payload JSON。
        细节: content_hash 基于 job_id，保证幂等（INSERT OR IGNORE）。
        """
        content = json.dumps(payload, ensure_ascii=False, sort_keys=True)
        content_hash = hashlib.sha256(f"job:{job_id}".encode()).hexdigest()
        now = datetime.now(tz=UTC).isoformat()
        title = _make_title(_PENDING, job_id, job_type)
        async with self._pool.write_connection() as conn:
            await conn.execute(
                """
                INSERT OR IGNORE INTO notes (
                    note_id, title, content, tags_json, content_hash, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (job_id, title, content, _JOB_TAG, content_hash, now, now),
            )
            await conn.commit()

    async def claim_next(self) -> dict[str, Any] | None:
        """原子取出下一条 pending job 并标记为 claimed（写路径）。

        结论: LIKE 'JOB_PENDING|%' 过滤，ORDER BY created_at ASC（FIFO）。
        细节: 写路径加锁确保单一 claimer，无竞态。
        """
        async with self._pool.write_connection() as conn:
            cursor = await conn.execute(
                """
                SELECT note_id, title, content FROM notes
                WHERE title LIKE ? AND tags_json = ?
                ORDER BY created_at ASC
                LIMIT 1
                """,
                (f"{_PENDING}|%", _JOB_TAG),
            )
            row = await cursor.fetchone()
            if row is None:
                return None

            job_id = str(row["note_id"])
            old_title = str(row["title"])
            content = str(row["content"])

            _, _, job_type = _parse_title(old_title)
            new_title = _make_title(_CLAIMED, job_id, job_type)
            now = datetime.now(tz=UTC).isoformat()

            await conn.execute(
                "UPDATE notes SET title = ?, updated_at = ? WHERE note_id = ?",
                (new_title, now, job_id),
            )
            await conn.commit()

            payload: dict[str, Any] = json.loads(content)
            return {"job_id": job_id, "job_type": job_type, "payload": payload}

    async def mark_done(self, job_id: str) -> None:
        """将 job 标记为 done（写路径）。

        结论: 更新 title 前缀为 JOB_DONE，保留 job_type。
        """
        await self._update_status(job_id, _DONE)

    async def mark_failed(self, job_id: str, error_msg: str = "") -> None:
        """将 job 标记为 failed，附带 error_msg（写路径）。

        结论: 更新 title 前缀为 JOB_FAILED；error_msg 追加到 content JSON。
        """
        async with self._pool.write_connection() as conn:
            cursor = await conn.execute(
                "SELECT title, content FROM notes WHERE note_id = ?",
                (job_id,),
            )
            row = await cursor.fetchone()
            if row is None:
                return
            _, _, job_type = _parse_title(str(row["title"]))
            new_title = _make_title(_FAILED, job_id, job_type)

            # 将 error_msg 注入 content
            content_dict: dict[str, Any] = json.loads(str(row["content"]))
            content_dict["_error"] = error_msg
            new_content = json.dumps(content_dict, ensure_ascii=False)
            now = datetime.now(tz=UTC).isoformat()

            await conn.execute(
                "UPDATE notes SET title = ?, content = ?, updated_at = ? WHERE note_id = ?",
                (new_title, new_content, now, job_id),
            )
            await conn.commit()

    # ── 私有辅助 ──────────────────────────────────────────────────────────────

    async def _update_status(self, job_id: str, new_status: str) -> None:
        """通用 status 更新辅助（写路径）。"""
        async with self._pool.write_connection() as conn:
            cursor = await conn.execute(
                "SELECT title FROM notes WHERE note_id = ?",
                (job_id,),
            )
            row = await cursor.fetchone()
            if row is None:
                return
            _, _, job_type = _parse_title(str(row["title"]))
            new_title = _make_title(new_status, job_id, job_type)
            now = datetime.now(tz=UTC).isoformat()
            await conn.execute(
                "UPDATE notes SET title = ?, updated_at = ? WHERE note_id = ?",
                (new_title, now, job_id),
            )
            await conn.commit()
