# ruff: noqa: E501
"""weekly_maintenance

Revision ID: 0004
Revises: 0003
Create Date: 2026-04-27T00:00:00

结论: 添加 weekly_maintenance_log 表（维护工时记录 C13 / OP-4 mitigation）
细节:
  - week_id TEXT PK: "YYYY-WW" 格式 (ISO 周编号，e.g. "2026-W17")
  - hours REAL NOT NULL: 本周实际维护工时（支持小数）
  - signed_at TEXT NOT NULL: 填报时间 ISO 8601
  - 用 raw SQL DDL（op.execute），不引入 ORM
  - downgrade 完整可逆（TECH-8）
"""

from __future__ import annotations

from collections.abc import Sequence

from alembic import op

# revision identifiers
revision: str = "0004"
down_revision: str | None = "0003"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """结论: 创建 weekly_maintenance_log 表。"""
    op.execute("""
        CREATE TABLE IF NOT EXISTS weekly_maintenance_log (
            week_id    TEXT PRIMARY KEY,       -- "YYYY-WW" e.g. "2026-W17"
            hours      REAL NOT NULL           -- 本周维护工时 (含小数, e.g. 1.5)
                CHECK (hours >= 0.0),
            signed_at  TEXT NOT NULL           -- ISO 8601 datetime, 填报时间
        )
    """)


def downgrade() -> None:
    """结论: 删除 weekly_maintenance_log 表（完整可逆）。"""
    op.execute("DROP TABLE IF EXISTS weekly_maintenance_log")
