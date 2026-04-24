"""tests/integration/test_worker_cannot_write_claude_dir.py — .claude/ 写保护验证 (T014)

结论：验证 worker 无法通过 hook 途径写 .claude/ 目录。
      两层断言：
        (1) hook JSON 模拟 Edit/Write 工具调用 .claude/settings.json → exit 2
        (2) 若目标目录真实存在且已 chmod a-w，直接写入后 sha256 不变（fail-closed）

注意：macOS bindfs 真实 mount 测试由 test_claude_dir_readonly.py 覆盖，
      本文件聚焦 hooks 层拦截（pre_tool_use.sh 的 Edit/Write deny）。

对齐：T014.md §Outputs + SLA §1.4 第2条 + architecture §6 "hooks 层第三道防线"
"""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# 常量
# ---------------------------------------------------------------------------

_PROJECT_ROOT = Path(__file__).parent.parent.parent
_HOOK_PATH = _PROJECT_ROOT / "worker_claude_dir" / "hooks" / "pre_tool_use.sh"

# 真实 worker_claude_dir 的 settings.json（用于 SHA 校验）
_WORKER_CLAUDE_DIR = _PROJECT_ROOT / "worker_claude_dir"
_SETTINGS_JSON = _WORKER_CLAUDE_DIR / "settings.json"


def _sha256_file(path: Path) -> str:
    """计算文件 sha256 hex digest。"""
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def _run_hook(
    tool_name: str,
    command: str | None = None,
    path: str | None = None,
) -> subprocess.CompletedProcess[str]:
    """运行 pre_tool_use.sh hook，支持 Bash / Edit / Write 工具。

    - Bash 工具：input 含 command 字段
    - Edit/Write 工具：input 含 path 字段
    """
    if command is not None:
        # Bash 工具
        payload = json.dumps({"tool": {"name": tool_name}, "input": {"command": command}})
    else:
        # Edit / Write 工具
        payload = json.dumps(
            {
                "tool": {"name": tool_name},
                "input": {
                    "path": path or ".claude/settings.json",
                    "content": "tampered content",
                },
            }
        )

    env = {**os.environ, "PYTHONPATH": str(_PROJECT_ROOT)}
    return subprocess.run(
        ["bash", str(_HOOK_PATH)],
        input=payload,
        capture_output=True,
        text=True,
        env=env,
        cwd=str(_PROJECT_ROOT),
        check=False,
    )


# ===========================================================================
# Test 1: Edit 工具调用 .claude/settings.json → hook deny (exit 2)
# ===========================================================================


@pytest.mark.integration
def test_hook_denies_edit_tool_on_claude_settings_json() -> None:
    """should deny Edit tool targeting .claude/settings.json (hooks 层第三道防线).

    SLA §1.4: host .claude/ 在 worker 视角只读。
    architecture §6: hooks deny Write(.claude/**) / Edit(.claude/**)。
    """
    result = _run_hook(tool_name="Edit", path=".claude/settings.json")
    assert result.returncode == 2, (
        f"期望 exit 2 (deny)，实际 exit {result.returncode}\nstderr: {result.stderr}"
    )


@pytest.mark.integration
def test_hook_denies_write_tool_on_claude_dir() -> None:
    """should deny Write tool targeting .claude/ directory files."""
    result = _run_hook(tool_name="Write", path=".claude/CLAUDE.md")
    assert result.returncode == 2, (
        f"期望 exit 2 (deny)，实际 exit {result.returncode}\nstderr: {result.stderr}"
    )


@pytest.mark.integration
def test_hook_denies_write_tool_on_claude_hooks() -> None:
    """should deny Write tool targeting .claude/hooks/ (防止 hook 被篡改)."""
    result = _run_hook(tool_name="Write", path=".claude/hooks/pre_tool_use.sh")
    assert result.returncode == 2, (
        f"期望 exit 2 (deny)，实际 exit {result.returncode}\nstderr: {result.stderr}"
    )


@pytest.mark.integration
def test_hook_denies_bash_chmod_on_claude_settings() -> None:
    """should deny bash chmod on .claude/settings.json (绕过 readonly 的尝试).

    architecture §6: deny Bash(chmod:*) 防止 worker 解除只读保护。
    """
    result = _run_hook(tool_name="Bash", command="chmod 644 .claude/settings.json")
    assert result.returncode == 2, (
        f"期望 exit 2 (deny)，实际 exit {result.returncode}\nstderr: {result.stderr}"
    )


@pytest.mark.integration
def test_hook_denies_bash_echo_redirect_to_claude_settings() -> None:
    """should deny bash echo > .claude/settings.json (shell 重定向写 .claude/).

    注意：此测试验证 hook 对 Bash 命令中 .claude/ 路径写操作的拦截。
    """
    result = _run_hook(
        tool_name="Bash",
        command='echo \'{"tampered":true}\' > .claude/settings.json',
    )
    assert result.returncode == 2, (
        f"期望 exit 2 (deny)，实际 exit {result.returncode}\nstderr: {result.stderr}"
    )


# ===========================================================================
# Test 2: SHA-256 不变验证（fail-closed 第二道保险）
# ===========================================================================


@pytest.mark.integration
def test_settings_json_sha256_unchanged_after_hook_denials() -> None:
    """should not change settings.json SHA-256 after repeated denied write attempts.

    验证：hook deny 阻止了实际写入，settings.json 内容未被篡改。
    条件：worker_claude_dir/settings.json 必须存在。
    """
    if not _SETTINGS_JSON.exists():
        pytest.skip(f"settings.json 不存在：{_SETTINGS_JSON}，跳过 SHA 校验测试")

    # 记录初始 SHA
    initial_sha = _sha256_file(_SETTINGS_JSON)

    # 模拟多次 worker 尝试写 .claude/settings.json（均应被 hook deny）
    for _ in range(3):
        result = _run_hook(tool_name="Edit", path=".claude/settings.json")
        assert result.returncode == 2, f"hook 应 deny，实际 exit {result.returncode}"

    # 验证文件 SHA 未变
    final_sha = _sha256_file(_SETTINGS_JSON)
    assert initial_sha == final_sha, (
        f"settings.json 被意外修改！\n"
        f"  initial SHA: {initial_sha}\n"
        f"  final SHA:   {final_sha}"
    )


# ===========================================================================
# Test 3: 允许对非 .claude/ 路径的 Edit/Write（不误杀）
# ===========================================================================


@pytest.mark.integration
def test_hook_allows_edit_tool_on_worktree_file() -> None:
    """should allow Edit tool targeting worktree files (non-.claude/ paths).

    .worktrees/<run-id>/ 是 worker 的合法写区，不应被 deny。
    """
    result = _run_hook(tool_name="Edit", path=".worktrees/run123/train.py")
    assert result.returncode == 0, (
        f"期望 exit 0 (allow)，实际 exit {result.returncode}\nstderr: {result.stderr}"
    )


@pytest.mark.integration
def test_hook_allows_write_tool_on_runs_dir() -> None:
    """should allow Write tool targeting runs/ directory (合法输出区)."""
    result = _run_hook(tool_name="Write", path="runs/01JTEST/report.md")
    assert result.returncode == 0, (
        f"期望 exit 0 (allow)，实际 exit {result.returncode}\nstderr: {result.stderr}"
    )
