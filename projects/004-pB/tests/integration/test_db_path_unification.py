"""
test_db_path_unification.py — Codex review F3 regression gate

结论: alembic + 运行时 (router_settings/router_onboarding) + scripts
必须使用同一份 SQLite 文件路径, 否则用户跑 alembic upgrade head 后,
onboarding/web UI 写到另一个空文件, silent 失败.

为什么要这条 test:
  - Codex review F3 实证: 此前 alembic env.py:47 写死 db.sqlite,
    router_settings.py 写死 data.sqlite, 两条独立路径
  - 用户跑 ./scripts/start.sh 后 onboarding 撞缺表 → try/except 吞错 →
    "看似启动成功但 DB 没迁移", 用户备份 ~/decision_ledger/data.sqlite
    备的是空文件
  - 修复: Settings.db_path property 作为单一权威入口

本 test 既是 F3 修复的 regression gate, 又是 forward-incompatibility:
未来若有人引入 db.sqlite 字面回退, 此 test 立刻 fail.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_settings_db_path_property_returns_data_sqlite() -> None:
    """F3 修复: Settings.db_path 必须返回 decision_ledger_home / data.sqlite。"""
    # 在 subprocess 里跑, 避免污染当前进程的 env
    result = subprocess.run(  # noqa: S603
        [
            sys.executable,
            "-c",
            """
import os
os.environ['ANTHROPIC_API_KEY'] = 'test-key'
os.environ['TELEGRAM_BOT_TOKEN'] = '000:test'
os.environ['DECISION_LEDGER_HOME'] = '/tmp/dl_unify_test'
from decision_ledger.config import load_settings
s = load_settings()
print(str(s.db_path))
""",
        ],
        cwd=str(PROJECT_ROOT),
        capture_output=True,
        text=True,
        timeout=10,
    )
    assert result.returncode == 0, f"subprocess 失败:\n{result.stderr}"
    db_path = result.stdout.strip()
    assert db_path.endswith("/data.sqlite"), (
        f"F3: Settings.db_path 必须以 data.sqlite 结尾, 实际 {db_path!r}"
    )
    assert "/db.sqlite" not in db_path, (
        f"F3: Settings.db_path 不得含 db.sqlite (旧路径), 实际 {db_path!r}"
    )


def test_alembic_upgrade_creates_data_sqlite_not_db_sqlite(tmp_path: Path) -> None:
    """F3 端到端: alembic upgrade head 必须迁移到 data.sqlite (与运行时一致)。

    这是真正的 user-visible regression gate: 用户跑 ./scripts/start.sh 前
    按 runbook 跑 alembic upgrade head, 文件名必须与运行时一致才能让数据生效。
    """
    import os

    home = tmp_path / "dl_home"
    home.mkdir()

    env = {
        **os.environ,
        "DECISION_LEDGER_HOME": str(home),
        "ANTHROPIC_API_KEY": os.environ.get("ANTHROPIC_API_KEY", "test-key"),
        "TELEGRAM_BOT_TOKEN": os.environ.get("TELEGRAM_BOT_TOKEN", "000:test"),
    }
    # 不设 DECISION_LEDGER_DB_URL → 走默认 home/<filename> 推导
    env.pop("DECISION_LEDGER_DB_URL", None)

    result = subprocess.run(  # noqa: S603
        [sys.executable, "-m", "alembic", "upgrade", "head"],
        cwd=str(PROJECT_ROOT),
        env=env,
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, f"alembic upgrade 失败:\n{result.stderr}"

    # F3 关键断言: 必须是 data.sqlite, 不能是 db.sqlite
    data_sqlite = home / "data.sqlite"
    db_sqlite = home / "db.sqlite"
    assert data_sqlite.exists(), (
        f"F3: alembic upgrade 后必须存在 data.sqlite, 实际目录: "
        f"{list(home.iterdir())}"
    )
    assert not db_sqlite.exists(), (
        f"F3: alembic upgrade 不得创建 db.sqlite (legacy 路径), "
        f"实际目录: {list(home.iterdir())}"
    )


def test_no_legacy_db_sqlite_path_in_runtime_paths() -> None:
    """F3 forward-incompatibility: src/ 与 scripts/ + alembic.ini 不得用 db.sqlite 作为路径。

    检测的是真实**路径字面** (字符串 quote / URL / 路径片段),
    不检测自然语言注释/docstring 的历史描述 (那些是合法的修复说明)。

    豁免:
      - check_secrets.py 自身 (它的 RULES 里把 db.sqlite 当作防回退检测字符串)
      - 注释行 (# 开头) 和 docstring 内的描述性文字
    """
    scan_dirs = [
        PROJECT_ROOT / "src",
        PROJECT_ROOT / "scripts",
        PROJECT_ROOT / "alembic",
    ]
    extra_files = [
        PROJECT_ROOT / "alembic.ini",
    ]

    # 只匹配字符串字面 / URL / 路径形式的 db.sqlite,
    # 不匹配自然语言里的描述
    path_pattern = re.compile(
        r"""(?x)
        (?:
            ['"][^'"]*\bdb\.sqlite\b[^'"]*['"]   # quoted string 含 db.sqlite
          | sqlite:/+[^\s'"]*\bdb\.sqlite        # sqlite:/// URL
          | /\w+/db\.sqlite                       # 路径片段 /xxx/db.sqlite
        )
        """
    )
    exempt_files = {
        PROJECT_ROOT / "scripts" / "check_secrets.py",
    }

    hits: list[str] = []
    for d in scan_dirs:
        if not d.exists():
            continue
        for f in d.rglob("*"):
            if not f.is_file():
                continue
            if f in exempt_files:
                continue
            if f.suffix not in {".py", ".ini", ".cfg", ".toml", ".sh"}:
                continue
            try:
                content = f.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            for lineno, line in enumerate(content.splitlines(), start=1):
                # 跳过纯注释行
                stripped = line.lstrip()
                if stripped.startswith("#") and f.suffix == ".py":
                    continue
                if path_pattern.search(line):
                    hits.append(f"{f.relative_to(PROJECT_ROOT)}:{lineno}: {line.strip()}")

    for f in extra_files:
        if not f.exists():
            continue
        content = f.read_text(encoding="utf-8", errors="replace")
        for lineno, line in enumerate(content.splitlines(), start=1):
            stripped = line.lstrip()
            if stripped.startswith("#"):
                continue
            if path_pattern.search(line):
                hits.append(f"{f.relative_to(PROJECT_ROOT)}:{lineno}: {line.strip()}")

    assert not hits, (
        "F3 nonregression: 检测到 db.sqlite 路径字面 (应统一为 data.sqlite):\n"
        + "\n".join(hits)
    )


def test_runbook_db_path_consistent_with_runtime() -> None:
    """F3 一致性: docs/runbook.md 提到的备份路径必须是 data.sqlite。

    防止文档与代码分裂 (runbook 教用户备份 data.sqlite, 但代码用 db.sqlite)。
    """
    runbook = PROJECT_ROOT / "docs" / "runbook.md"
    if not runbook.exists():
        pytest.skip("runbook.md 不存在")

    content = runbook.read_text(encoding="utf-8")
    # 备份脚本的字面: cp ~/decision_ledger/data.sqlite ...
    assert "~/decision_ledger/data.sqlite" in content, (
        "F3: runbook 必须提到 ~/decision_ledger/data.sqlite (主数据库)"
    )
    # 不得提 db.sqlite (legacy 路径)
    assert "~/decision_ledger/db.sqlite" not in content, (
        "F3: runbook 不得提 ~/decision_ledger/db.sqlite (legacy 路径)"
    )
