"""
test_toggle_b_lite_v01.py — F2-T020 followup A2
结论: B-lite CLI 跨进程 disclaimer (subprocess 集成)
细节:
  - engage 真实路径 (无 SKIP_PAUSE) 在 v0.1 默认 wiring 下打 stderr 警告 + exit 0
  - disengage 真实路径同上
  - SKIP_PAUSE 模式下 mock 替换了 _conflict_worker_instance, get_wiring_status 返回 wired,
    所以测试逃生口下不打警告 (这是有意行为)
"""

from __future__ import annotations

import os
import subprocess
import sys
from collections.abc import AsyncIterator
from pathlib import Path

import pytest_asyncio

from decision_ledger.repository.base import AsyncConnectionPool

PROJECT_ROOT = Path(__file__).resolve().parents[3]
SCRIPT_PATH = PROJECT_ROOT / "scripts" / "toggle_b_lite.py"


@pytest_asyncio.fixture
async def migrated_db(tmp_path: Path) -> AsyncIterator[Path]:
    """提供经过 alembic upgrade head 迁移的 SQLite DB。"""
    db_path = tmp_path / "test_b_lite_v01.sqlite"
    db_url = f"sqlite:///{db_path}"

    env = {
        **os.environ,
        "DECISION_LEDGER_DB_URL": db_url,
        "ANTHROPIC_API_KEY": os.environ.get("ANTHROPIC_API_KEY", "test-key-placeholder"),
        "TELEGRAM_BOT_TOKEN": os.environ.get("TELEGRAM_BOT_TOKEN", "test-token-placeholder"),
    }
    result = subprocess.run(  # noqa: S603
        [sys.executable, "-m", "alembic", "upgrade", "head"],
        cwd=str(PROJECT_ROOT),
        env=env,
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, f"alembic upgrade 失败:\n{result.stderr}"

    pool = AsyncConnectionPool(str(db_path))
    await pool.initialize()
    try:
        yield db_path
    finally:
        await pool.close()


def _run_cli(
    args: list[str],
    db_path: Path,
    extra_env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    """subprocess 跑 CLI, 返回结果 (不抛)。"""
    env = {
        **os.environ,
        "DECISION_LEDGER_DB_URL": f"sqlite:///{db_path}",
        "ANTHROPIC_API_KEY": os.environ.get("ANTHROPIC_API_KEY", "test-key-placeholder"),
        "TELEGRAM_BOT_TOKEN": os.environ.get("TELEGRAM_BOT_TOKEN", "test-token-placeholder"),
    }
    if extra_env:
        env.update(extra_env)
    return subprocess.run(  # noqa: S603
        [sys.executable, str(SCRIPT_PATH), *args],
        env=env,
        capture_output=True,
        text=True,
        timeout=30,
    )


def test_engage_prints_cross_process_warning_in_v01(migrated_db: Path) -> None:
    """followup A2: 真实路径 (无 SKIP_PAUSE) 在 v0.1 默认 wiring 下打 stderr 警告且 exit 0。"""
    result = _run_cli(
        ["engage", "--reason=v0.1 smoke test"],
        migrated_db,
        # 不设 SKIP_PAUSE → 走真实路径
    )

    assert result.returncode == 0, (
        f"engage 应 exit 0 (audit trail 仍写入), "
        f"实际 returncode={result.returncode}\nstderr:\n{result.stderr}\nstdout:\n{result.stdout}"
    )
    assert "pause hook is no-op in v0.1" in result.stderr, (
        f"应在 stderr 打跨进程 disclaimer, 实际 stderr:\n{result.stderr}"
    )
    assert "ENGAGED" in result.stdout, (
        f"audit trail 仍应输出 ENGAGED 字样 (DB 写入成功), 实际 stdout:\n{result.stdout}"
    )


def test_engage_skip_pause_does_not_print_warning(migrated_db: Path) -> None:
    """followup A2 反向: SKIP_PAUSE 模式下 mock 替换 wiring, disclaimer 不打。"""
    result = _run_cli(
        ["engage", "--reason=skip-pause smoke"],
        migrated_db,
        extra_env={"DECISION_LEDGER_B_LITE_SKIP_PAUSE": "1"},
    )

    assert result.returncode == 0
    assert "pause hook is no-op" not in result.stderr, (
        f"SKIP_PAUSE 模式不应打 disclaimer (mock 替换了 wiring 视为已 wire), "
        f"实际 stderr:\n{result.stderr}"
    )


def test_disengage_real_path_prints_disclaimer_before_service_call(
    migrated_db: Path,
) -> None:
    """followup A2: disengage 真实路径在调用 BLiteService 前打 disclaimer。

    disengage 业务逻辑可能因 cooling-off 等原因抛 ValueError exit 1, 但
    disclaimer 是 wiring 层 UX 提示, 必须在 service 抛错之前已经写到 stderr。
    本测试只验证"disclaimer 进 stderr", 不约束 exit code。
    """
    # 先用 skip-pause 模式 engage 一次, 让 DB 有 engaged 记录
    engage_result = _run_cli(
        ["engage", "--reason=setup for disengage disclaimer test"],
        migrated_db,
        extra_env={"DECISION_LEDGER_B_LITE_SKIP_PAUSE": "1"},
    )
    assert engage_result.returncode == 0, f"setup engage failed: {engage_result.stderr}"

    # 真实路径 disengage (不 skip-pause)
    # cooling-off 大概率 block, 但 disclaimer 必须先于 ValueError 出现
    result = _run_cli(["disengage"], migrated_db)

    assert "pause hook is no-op in v0.1" in result.stderr, (
        f"disengage 真实路径应打 disclaimer (在 service 调用前), "
        f"实际 stderr:\n{result.stderr}"
    )
