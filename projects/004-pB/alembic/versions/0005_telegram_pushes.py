# ruff: noqa: E501
"""telegram_pushes

Revision ID: 0005
Revises: 0004
Create Date: 2026-04-27T00:00:00

结论: 添加 telegram_pushes 表 — rate limiter 滚动窗口数据存储 (T017 R4 红线)
细节:
  - id INTEGER PK AUTOINCREMENT: 自增主键
  - chat_id TEXT NOT NULL: Telegram chat_id (white-list 验证对象)
  - push_type TEXT NOT NULL: 'weekly' | 'event'
  - pushed_at TEXT NOT NULL: ISO 8601 datetime，UTC
  - 索引 idx_telegram_pushes_lookup: (chat_id, push_type, pushed_at) 加速 7 天窗口查询
  - downgrade 完整可逆（TECH-8）
"""

from __future__ import annotations

from collections.abc import Sequence

from alembic import op

# revision identifiers
revision: str = "0005"
down_revision: str | None = "0004"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """结论: 创建 telegram_pushes 表 + 查询索引。"""
    op.execute("""
        CREATE TABLE IF NOT EXISTS telegram_pushes (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id     TEXT    NOT NULL,                  -- Telegram chat_id
            push_type   TEXT    NOT NULL                   -- 'weekly' | 'event'
                CHECK (push_type IN ('weekly', 'event')),
            pushed_at   TEXT    NOT NULL                   -- ISO 8601 UTC datetime
        )
    """)
    op.execute("""
        CREATE INDEX IF NOT EXISTS idx_telegram_pushes_lookup
        ON telegram_pushes (chat_id, push_type, pushed_at)
    """)


def downgrade() -> None:
    """结论: 删除索引和 telegram_pushes 表（完整可逆）。"""
    op.execute("DROP INDEX IF EXISTS idx_telegram_pushes_lookup")
    op.execute("DROP TABLE IF EXISTS telegram_pushes")
