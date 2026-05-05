# ruff: noqa: E501
"""tab_open_log

Revision ID: 0002
Revises: 0001
Create Date: 2026-04-26T00:00:00

结论: 添加 tab_open_log 表（tab 打开计数 OP-6）+ request_log 表（OP-1 p95 wall-clock）
细节:
  - tab_open_log: 记录每次页面打开事件 (path, user_agent, opened_at)
  - request_log: 记录 GET→POST commit 全程 wall-clock，用于 OP-1 p95 统计
  - 仅用 raw SQL DDL（op.execute），不引入 ORM
  - downgrade 完整可逆
"""

from __future__ import annotations

from collections.abc import Sequence

from alembic import op

# revision identifiers
revision: str = "0002"
down_revision: str | None = "0001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """结论: 添加 tab_open_log 和 request_log 表。"""
    # ── tab_open_log: tab 打开计数 (OP-6 mitigation) ──────────────────────────
    op.execute("""
        CREATE TABLE IF NOT EXISTS tab_open_log (
            id          TEXT PRIMARY KEY,
            path        TEXT NOT NULL,
            user_agent  TEXT,
            opened_at   TEXT NOT NULL  -- ISO-8601 UTC
        )
    """)

    op.execute("""
        CREATE INDEX IF NOT EXISTS idx_tab_open_log_opened_at
            ON tab_open_log (opened_at)
    """)

    # ── request_log: GET /decisions/new → POST commit wall-clock (OP-1 p95) ──
    # 结论: duration_ms 记录全程耗时，含 draft 阶段 LLM 等待（PRD §S1 原口径）
    op.execute("""
        CREATE TABLE IF NOT EXISTS request_log (
            id          TEXT PRIMARY KEY,
            path        TEXT NOT NULL,
            method      TEXT NOT NULL,
            status_code INTEGER,
            duration_ms INTEGER,        -- 全程 wall-clock ms (含 draft LLM 等待)
            ts          TEXT NOT NULL   -- ISO-8601 UTC
        )
    """)

    op.execute("""
        CREATE INDEX IF NOT EXISTS idx_request_log_ts
            ON request_log (ts)
    """)

    op.execute("""
        CREATE INDEX IF NOT EXISTS idx_request_log_path_status
            ON request_log (path, status_code)
    """)


def downgrade() -> None:
    """结论: 删除 tab_open_log 和 request_log 表（完整可逆）。"""
    op.execute("DROP INDEX IF EXISTS idx_request_log_path_status")
    op.execute("DROP INDEX IF EXISTS idx_request_log_ts")
    op.execute("DROP TABLE IF EXISTS request_log")

    op.execute("DROP INDEX IF EXISTS idx_tab_open_log_opened_at")
    op.execute("DROP TABLE IF EXISTS tab_open_log")
