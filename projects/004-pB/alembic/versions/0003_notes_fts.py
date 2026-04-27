# ruff: noqa: E501
"""notes_fts5

Revision ID: 0003
Revises: 0002
Create Date: 2026-04-27T00:00:00

结论: 添加 SQLite FTS5 虚拟表 notes_fts + 同步触发器，实现全文搜索
细节:
  - notes_fts: FTS5 虚拟表, tokenize="trigram" (改善中文分词, T016 gotcha)
  - trigram tokenizer: SQLite 3.38+ 内置, 对任意语言做 3-gram 分词, 无外部依赖
  - 同步触发器: notes INSERT/UPDATE/DELETE → 自动同步 notes_fts
  - downgrade: 删除触发器 + 虚拟表 (完整可逆, TECH-8)
  - 注意: content_rowid 与 notes 表无关联 (FTS5 content= 语法要求 rowid, 但 notes 用 TEXT PK)
    → 采用 "外部内容表" 方案: notes_fts 存储 note_id/title/content 副本, 触发器保持同步
"""

from __future__ import annotations

from collections.abc import Sequence

from alembic import op

# revision identifiers
revision: str = "0003"
down_revision: str | None = "0002"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """结论: 创建 FTS5 虚拟表 + 3 个同步触发器 (INSERT/UPDATE/DELETE)。"""

    # ── FTS5 虚拟表 (Trigram tokenizer) ──────────────────────────────────────
    # 结论: trigram tokenizer 无需任何外部词典, 对英文/中文/混合内容均有效
    # 细节:
    #   - content: 不与 notes 表绑定 content= (避免 rowid 不匹配问题)
    #   - tokenize="trigram": 将字符串分成 3-char 窗口, 支持任意位置子串匹配
    #   - 副本方案: triggers 负责保持 notes_fts 与 notes 同步
    op.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS notes_fts USING fts5(
            note_id UNINDEXED,
            title,
            content,
            tokenize = 'trigram'
        )
    """)

    # ── INSERT 触发器: notes 插入时同步到 notes_fts ─────────────────────────
    op.execute("""
        CREATE TRIGGER IF NOT EXISTS notes_fts_insert
        AFTER INSERT ON notes
        BEGIN
            INSERT INTO notes_fts (note_id, title, content)
            VALUES (NEW.note_id, NEW.title, NEW.content);
        END
    """)

    # ── UPDATE 触发器: notes 更新时同步 notes_fts ──────────────────────────
    op.execute("""
        CREATE TRIGGER IF NOT EXISTS notes_fts_update
        AFTER UPDATE ON notes
        BEGIN
            DELETE FROM notes_fts WHERE note_id = OLD.note_id;
            INSERT INTO notes_fts (note_id, title, content)
            VALUES (NEW.note_id, NEW.title, NEW.content);
        END
    """)

    # ── DELETE 触发器: notes 删除时清理 notes_fts ──────────────────────────
    op.execute("""
        CREATE TRIGGER IF NOT EXISTS notes_fts_delete
        AFTER DELETE ON notes
        BEGIN
            DELETE FROM notes_fts WHERE note_id = OLD.note_id;
        END
    """)


def downgrade() -> None:
    """结论: 删除触发器 + FTS5 虚拟表 (完整可逆, TECH-8)。"""
    op.execute("DROP TRIGGER IF EXISTS notes_fts_delete")
    op.execute("DROP TRIGGER IF EXISTS notes_fts_update")
    op.execute("DROP TRIGGER IF EXISTS notes_fts_insert")
    op.execute("DROP TABLE IF EXISTS notes_fts")
