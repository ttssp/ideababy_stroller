# ruff: noqa: E501
"""learning_quarters

Revision ID: 0006
Revises: 0005
Create Date: 2026-04-27T00:00:00

结论: 添加 learning_quarters 表 — 季度学习自查数据存储 (T019 R3 简化版)
细节:
  - quarter_id TEXT PK: 季度标识 (e.g. "2026-Q2")
  - generated_at TEXT NOT NULL: ISO 8601 datetime，UTC，抽题时刻
  - questions_json TEXT NOT NULL: JSON 数组，7 个从 checklist.yaml 随机抽取的题目
  - answers_json TEXT: JSON 对象，human 提交的答案 (key=concept_id, value=answer_text)
  - scores_json TEXT: JSON 对象，LLM 评分结果 (key=concept_id, value=0-10 整数)
  - finalized INTEGER NOT NULL DEFAULT 0: 0=未完成, 1=评分完成
  - downgrade 完整可逆（TECH-8）
"""

from __future__ import annotations

from collections.abc import Sequence

from alembic import op

# revision identifiers
revision: str = "0006"
down_revision: str | None = "0005"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """结论: 创建 learning_quarters 表。"""
    op.execute("""
        CREATE TABLE IF NOT EXISTS learning_quarters (
            quarter_id     TEXT    PRIMARY KEY,                -- e.g. "2026-Q2"
            generated_at   TEXT    NOT NULL,                   -- ISO 8601 UTC datetime
            questions_json TEXT    NOT NULL DEFAULT '[]',      -- 7 个抽取概念的 JSON 数组
            answers_json   TEXT    NOT NULL DEFAULT '{}',      -- human 答案 JSON 对象
            scores_json    TEXT    NOT NULL DEFAULT '{}',      -- LLM 评分 JSON 对象
            finalized      INTEGER NOT NULL DEFAULT 0          -- 0=未完成, 1=评分完成
        )
    """)


def downgrade() -> None:
    """结论: 删除 learning_quarters 表（完整可逆）。"""
    op.execute("DROP TABLE IF EXISTS learning_quarters")
