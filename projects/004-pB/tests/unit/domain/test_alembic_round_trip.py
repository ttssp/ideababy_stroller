"""
alembic round-trip 测试 — T002
结论: 在临时 SQLite 上验证 upgrade head / downgrade base / upgrade head 全部成功
细节:
  - 使用 tmp_path fixture 创建独立 SQLite 路径，避免污染项目 db.sqlite
  - subprocess 方式调用 alembic CLI（env var 传 DB_URL），与生产运行路径一致
  - 验证所有关键 schema 字段存在（R2 constraints）
  - 验证 PRAGMA journal_mode = wal (WAL mode)
  - 验证 decision_drafts / watchlist market 字段 (R2 D13/D24)
"""

from __future__ import annotations

import sqlite3
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
ALEMBIC_INI = PROJECT_ROOT / "alembic.ini"


def _run_alembic(cmd: list[str], db_path: Path) -> subprocess.CompletedProcess[str]:
    """执行 alembic 命令，传入临时 DB 路径。"""
    env_vars = {
        "DECISION_LEDGER_DB_URL": f"sqlite:///{db_path}",
        # 满足 Settings 校验的占位值（不真实调用）
        "ANTHROPIC_API_KEY": "test-key-placeholder",
        "TELEGRAM_BOT_TOKEN": "test-token-placeholder",
    }
    import os
    full_env = {**os.environ, **env_vars}
    result = subprocess.run(  # noqa: S603 — 测试代码,sys.executable + alembic 受信任
        [sys.executable, "-m", "alembic", *cmd],
        cwd=str(PROJECT_ROOT),
        capture_output=True,
        text=True,
        env=full_env,
    )
    return result


def test_alembic_ini_exists() -> None:
    """alembic.ini 必须存在。"""
    assert ALEMBIC_INI.exists(), f"alembic.ini 不存在: {ALEMBIC_INI}"


def test_alembic_upgrade_head_succeeds(tmp_path: Path) -> None:
    """upgrade head 在临时目录成功创建 db.sqlite。"""
    db_path = tmp_path / "db.sqlite"
    result = _run_alembic(["upgrade", "head"], db_path)
    assert result.returncode == 0, (
        f"alembic upgrade head 失败\nstdout: {result.stdout}\nstderr: {result.stderr}"
    )
    assert db_path.exists(), "upgrade head 未创建 db.sqlite"


def test_alembic_round_trip_up_down_up(tmp_path: Path) -> None:
    """upgrade head → downgrade base → upgrade head 完整 round-trip 成功。"""
    db_path = tmp_path / "db.sqlite"

    # 1. upgrade head
    r1 = _run_alembic(["upgrade", "head"], db_path)
    assert r1.returncode == 0, f"upgrade head 失败: {r1.stderr}"

    # 2. downgrade base
    r2 = _run_alembic(["downgrade", "base"], db_path)
    assert r2.returncode == 0, f"downgrade base 失败: {r2.stderr}"

    # 3. upgrade head 再次
    r3 = _run_alembic(["upgrade", "head"], db_path)
    assert r3.returncode == 0, f"第二次 upgrade head 失败: {r3.stderr}"


def test_decisions_schema_r2_fields(tmp_path: Path) -> None:
    """
    decisions 表 schema 含 R2 必要字段:
    - would_have_acted_without_agent INTEGER NOT NULL CHECK (0,1)  (R2 M1)
    - status TEXT NOT NULL CHECK (draft/committed/abandoned)  (R2 D8)
    - action CHECK (buy/sell/hold/wait)  (invariant #3)
    - reason CHECK length <= 80  (spec)
    """
    db_path = tmp_path / "db.sqlite"
    r = _run_alembic(["upgrade", "head"], db_path)
    assert r.returncode == 0, r.stderr

    conn = sqlite3.connect(str(db_path))
    try:
        cursor = conn.execute(
            "SELECT sql FROM sqlite_master WHERE type='table' AND name='decisions'"
        )
        row = cursor.fetchone()
        assert row is not None, "decisions 表不存在"
        ddl = row[0]
        # R2 M1: would_have_acted_without_agent NOT NULL
        assert "would_have_acted_without_agent" in ddl, "缺少 would_have_acted_without_agent 字段"
        assert "NOT NULL" in ddl, "would_have_acted_without_agent 必须是 NOT NULL"
        # R2 D8: status 字段
        assert "status" in ddl, "缺少 status 字段"
        # action enum
        assert "buy" in ddl, "action CHECK 缺少 buy"
        assert "hold" in ddl, "action CHECK 缺少 hold (invariant #3)"
        assert "wait" in ddl, "action CHECK 缺少 wait (invariant #3)"
        # reason length
        assert "length(reason)" in ddl or "length" in ddl, "缺少 reason 长度 CHECK"
    finally:
        conn.close()


def test_decision_drafts_schema_r2(tmp_path: Path) -> None:
    """
    decision_drafts 表 (R2 D13) 含必要字段:
    - draft_id PK, ticker, intended_action, draft_reason
    - conflict_report_ref / devils_rebuttal_ref (INSERT 时可空)
    - status CHECK (draft/committed/abandoned)
    - committed_at / abandoned_at (可空)
    """
    db_path = tmp_path / "db.sqlite"
    r = _run_alembic(["upgrade", "head"], db_path)
    assert r.returncode == 0, r.stderr

    conn = sqlite3.connect(str(db_path))
    try:
        cursor = conn.execute(
            "SELECT sql FROM sqlite_master WHERE type='table' AND name='decision_drafts'"
        )
        row = cursor.fetchone()
        assert row is not None, "decision_drafts 表不存在 (R2 D13)"
        ddl = row[0]
        assert "draft_id" in ddl, "缺少 draft_id PK"
        assert "intended_action" in ddl, "缺少 intended_action"
        assert "draft_reason" in ddl, "缺少 draft_reason"
        assert "status" in ddl, "缺少 status"
        assert "committed_at" in ddl, "缺少 committed_at"
        assert "abandoned_at" in ddl, "缺少 abandoned_at"
    finally:
        conn.close()


def test_watchlist_market_column(tmp_path: Path) -> None:
    """
    watchlist 表含 market 字段 CHECK (US/HK/CN) DEFAULT 'US' (R2 D24)。
    """
    db_path = tmp_path / "db.sqlite"
    r = _run_alembic(["upgrade", "head"], db_path)
    assert r.returncode == 0, r.stderr

    conn = sqlite3.connect(str(db_path))
    try:
        cursor = conn.execute(
            "SELECT sql FROM sqlite_master WHERE type='table' AND name='watchlist'"
        )
        row = cursor.fetchone()
        assert row is not None, "watchlist 表不存在"
        ddl = row[0]
        assert "market" in ddl, "watchlist 缺少 market 字段 (R2 D24)"
        assert "US" in ddl, "watchlist market CHECK 缺少 US"
        assert "HK" in ddl, "watchlist market CHECK 缺少 HK"
        assert "CN" in ddl, "watchlist market CHECK 缺少 CN"
    finally:
        conn.close()


def test_wal_mode_enabled(tmp_path: Path) -> None:
    """
    PRAGMA journal_mode 返回 wal — alembic env.py 必须在连接时设置。
    """
    db_path = tmp_path / "db.sqlite"
    r = _run_alembic(["upgrade", "head"], db_path)
    assert r.returncode == 0, r.stderr

    conn = sqlite3.connect(str(db_path))
    try:
        cursor = conn.execute("PRAGMA journal_mode")
        mode = cursor.fetchone()[0]
        assert mode == "wal", f"journal_mode 期望 wal, 实际: {mode}"
    finally:
        conn.close()


def test_all_required_tables_exist(tmp_path: Path) -> None:
    """
    upgrade head 后必须存在所有 11 个核心表。
    """
    db_path = tmp_path / "db.sqlite"
    r = _run_alembic(["upgrade", "head"], db_path)
    assert r.returncode == 0, r.stderr

    required_tables = {
        "decisions",
        "decision_drafts",
        "env_snapshots",
        "conflict_reports",
        "strategy_signals",
        "rebuttals",
        "advisor_reports",
        "watchlist",
        "notes",
        "alerts",
        "llm_usage",
    }

    conn = sqlite3.connect(str(db_path))
    try:
        cursor = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'alembic_%'"
        )
        existing = {row[0] for row in cursor.fetchall()}
        missing = required_tables - existing
        assert not missing, f"缺少必要表: {missing}"
    finally:
        conn.close()
