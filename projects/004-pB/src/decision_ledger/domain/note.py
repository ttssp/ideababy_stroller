"""
Note 域模型 — T002
结论: 笔记 wiki 条目，含 content_hash 自动去重
细节:
  - content_hash: sha256(content)，去重逻辑在 Repository 层用
  - tags: 标签列表，便于分类检索
  - T002 只定义数据类，去重实现在 T003 Repository
"""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class Note(BaseModel):
    """笔记 wiki 条目。"""

    model_config = ConfigDict(frozen=True)

    note_id: str                    # UUID 字符串
    title: str
    content: str
    tags: list[str] = []
    content_hash: str               # sha256(content)，Repository 层用于去重
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
