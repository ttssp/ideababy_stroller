# ruff: noqa: E501
"""onboarding_state

Revision ID: 0007
Revises: 0005
Create Date: 2026-04-27T00:00:00

结论: 添加 onboarding_state 表 — 7 步引导流程状态机存储 (T021 O6 验证)
细节:
  - step INTEGER NOT NULL: 当前步骤 (1-7, 0 = 未开始)
  - started_at TEXT: ISO 8601 UTC，第一步 enter 时间
  - completed_at TEXT: ISO 8601 UTC，step 7 complete 时间 (NULL = 未完成)
  - total_duration_s REAL: 总耗时秒数 (completed_at - started_at)
  - o6_pass INTEGER: 0/1，total_duration_s <= 900s 时标 1 (O6 验证门槛)
  - step_timestamps_json TEXT: JSON 格式每步 enter/leave timestamp (诊断用)
  - downgrade 完整可逆（TECH-8）
"""

from __future__ import annotations

from collections.abc import Sequence

from alembic import op

# revision identifiers
revision: str = "0007"
down_revision: str | None = "0006"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """结论: 创建 onboarding_state 表 (单行记录，用 id=1 唯一主键)。"""
    op.execute("""
        CREATE TABLE IF NOT EXISTS onboarding_state (
            id                    INTEGER PRIMARY KEY DEFAULT 1,  -- 单行，始终 id=1
            step                  INTEGER NOT NULL DEFAULT 0,     -- 当前步骤 0-7
            started_at            TEXT,                            -- ISO 8601 UTC
            completed_at          TEXT,                            -- ISO 8601 UTC (NULL=未完成)
            total_duration_s      REAL,                           -- 总耗时秒数
            o6_pass               INTEGER NOT NULL DEFAULT 0,     -- 0/1 O6 pass flag
            step_timestamps_json  TEXT NOT NULL DEFAULT '{}'      -- 每步 enter/leave timestamp
        )
    """)
    op.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS idx_onboarding_state_singleton
        ON onboarding_state (id)
    """)


def downgrade() -> None:
    """结论: 删除 onboarding_state 表 (完整可逆)。"""
    op.execute("DROP INDEX IF EXISTS idx_onboarding_state_singleton")
    op.execute("DROP TABLE IF EXISTS onboarding_state")
