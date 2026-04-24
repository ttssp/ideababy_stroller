"""
tests/integration/test_pip_install_deny_unlocked.py — pip hook 集成测试 (T015)

结论：测试 pre_pip_install.sh 的真实 shell 行为：
      - 合法白名单命令 → exit 0
      - 非法命令 → exit 2
      - JSON stdin 解析
      - Python 模块 import 可达性
      - 非 pip 命令直接放行

对齐：T015.md § tests/integration/test_pip_install_deny_unlocked.py
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# 常量
# ---------------------------------------------------------------------------

# 项目根目录（包含 pars/）
_PROJECT_ROOT = Path(__file__).parent.parent.parent

# hook 路径
_HOOK_PATH = _PROJECT_ROOT / "worker_claude_dir" / "hooks" / "pre_pip_install.sh"


def _make_input_json(command: str) -> str:
    """构造符合 Claude Code hook 协议的 stdin JSON。"""
    return json.dumps({"tool": {"name": "Bash"}, "input": {"command": command}})


def _run_hook(cmd_str: str, *, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    """运行 hook，传入命令字符串，返回 CompletedProcess。

    PYTHONPATH 设置为项目根目录，确保 pars.safety.pip_policy 可 import。
    """
    env = {**os.environ, "PYTHONPATH": str(_PROJECT_ROOT)}
    return subprocess.run(
        ["bash", str(_HOOK_PATH)],
        input=_make_input_json(cmd_str),
        capture_output=True,
        text=True,
        env=env,
        cwd=str(cwd or _PROJECT_ROOT),
        check=False,
    )


# ===========================================================================
# 基础前提：hook 可执行 + Python 可 import
# ===========================================================================


@pytest.mark.integration
def test_hook_file_exists_and_is_executable() -> None:
    """hook 文件存在且可执行。"""
    assert _HOOK_PATH.exists(), f"hook 不存在：{_HOOK_PATH}"
    assert os.access(_HOOK_PATH, os.X_OK), f"hook 不可执行：{_HOOK_PATH}"


@pytest.mark.integration
def test_python_can_import_pip_policy_module() -> None:
    """Python 路径设置正确，pars.safety.pip_policy 可 import。

    T015 Verification: uv run python -c "from pars.safety import evaluate_pip_command..."
    """
    env = {**os.environ, "PYTHONPATH": str(_PROJECT_ROOT)}
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            (
                "from pars.safety.pip_policy import evaluate_pip_command, "
                "is_pip_install_allowed, PipCommandDecision; print('OK')"
            ),
        ],
        capture_output=True,
        text=True,
        env=env,
        cwd=str(_PROJECT_ROOT),
        check=False,
    )
    assert result.returncode == 0, f"import 失败：{result.stderr}"
    assert "OK" in result.stdout


@pytest.mark.integration
def test_pars_safety_package_export_pip_policy() -> None:
    """pars.safety __init__.py 正确导出 T015 符号。"""
    env = {**os.environ, "PYTHONPATH": str(_PROJECT_ROOT)}
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            (
                "from pars.safety import evaluate_pip_command, PipCommandDecision; "
                "print('OK')"
            ),
        ],
        capture_output=True,
        text=True,
        env=env,
        cwd=str(_PROJECT_ROOT),
        check=False,
    )
    assert result.returncode == 0, f"pars.safety 导出失败：{result.stderr}"
    assert "OK" in result.stdout


# ===========================================================================
# 白名单三条 → exit 0
# ===========================================================================


@pytest.mark.integration
def test_hook_allows_pip_install_locked_with_require_hashes() -> None:
    """白名单A: pip install -r requirements-locked.txt --require-hashes → exit 0。"""
    result = _run_hook("pip install -r requirements-locked.txt --require-hashes")
    assert result.returncode == 0, f"期望 exit 0，实际 exit {result.returncode}\nstderr: {result.stderr}"


@pytest.mark.integration
def test_hook_allows_uv_pip_install_locked_with_require_hashes() -> None:
    """白名单B: uv pip install -r requirements-locked.txt --require-hashes → exit 0。"""
    result = _run_hook("uv pip install -r requirements-locked.txt --require-hashes")
    assert result.returncode == 0, f"期望 exit 0，实际 exit {result.returncode}\nstderr: {result.stderr}"


@pytest.mark.integration
def test_hook_allows_uv_sync_frozen() -> None:
    """白名单C: uv sync --frozen → exit 0。"""
    result = _run_hook("uv sync --frozen")
    assert result.returncode == 0, f"期望 exit 0，实际 exit {result.returncode}\nstderr: {result.stderr}"


# ===========================================================================
# 非法命令 → exit 2
# ===========================================================================


@pytest.mark.integration
def test_hook_denies_pip_install_unlocked_package() -> None:
    """pip install requests (无锁文件) → exit 2。

    对应 T015 Verification: echo '{...pip install requests...}' | bash hook → exit=2
    """
    result = _run_hook("pip install requests")
    assert result.returncode == 2, f"期望 exit 2，实际 exit {result.returncode}\nstderr: {result.stderr}"


@pytest.mark.integration
def test_hook_denies_pip_install_without_require_hashes() -> None:
    """pip install -r requirements-locked.txt (缺 --require-hashes) → exit 2。"""
    result = _run_hook("pip install -r requirements-locked.txt")
    assert result.returncode == 2, f"期望 exit 2，实际 exit {result.returncode}\nstderr: {result.stderr}"


@pytest.mark.integration
def test_hook_denies_uv_sync_without_frozen() -> None:
    """uv sync (无 --frozen) → exit 2。"""
    result = _run_hook("uv sync")
    assert result.returncode == 2, f"期望 exit 2，实际 exit {result.returncode}\nstderr: {result.stderr}"


@pytest.mark.integration
def test_hook_denies_uv_add() -> None:
    """uv add requests (修改 lock) → exit 2。"""
    result = _run_hook("uv add requests")
    assert result.returncode == 2, f"期望 exit 2，实际 exit {result.returncode}\nstderr: {result.stderr}"


# ===========================================================================
# 非 pip 命令直接放行
# ===========================================================================


@pytest.mark.integration
def test_hook_skips_non_pip_command_ls() -> None:
    """ls -la (非 pip/uv 命令) → exit 0（直接跳过，不干预）。"""
    result = _run_hook("ls -la")
    assert result.returncode == 0, f"期望 exit 0（跳过），实际 exit {result.returncode}\nstderr: {result.stderr}"


@pytest.mark.integration
def test_hook_skips_python_script_execution() -> None:
    """python train.py (非 pip 命令) → exit 0（直接跳过）。"""
    result = _run_hook("python train.py --epochs 3")
    assert result.returncode == 0, f"期望 exit 0（跳过），实际 exit {result.returncode}\nstderr: {result.stderr}"


@pytest.mark.integration
def test_hook_skips_git_command() -> None:
    """git status (非 pip 命令) → exit 0（直接跳过）。"""
    result = _run_hook("git status")
    assert result.returncode == 0, f"期望 exit 0（跳过），实际 exit {result.returncode}\nstderr: {result.stderr}"


# ===========================================================================
# JSON stdin 解析正确性
# ===========================================================================


@pytest.mark.integration
def test_hook_correctly_parses_full_claude_json_format() -> None:
    """hook 能从完整 Claude Code hook JSON 格式中正确解析 command。"""
    # 使用完整格式 JSON（含 tool.name 字段）
    full_json = json.dumps(
        {
            "tool": {"name": "Bash", "input_schema": {"type": "object"}},
            "input": {"command": "pip install requests", "description": "安装 requests"},
        }
    )
    env = {**os.environ, "PYTHONPATH": str(_PROJECT_ROOT)}
    result = subprocess.run(
        ["bash", str(_HOOK_PATH)],
        input=full_json,
        capture_output=True,
        text=True,
        env=env,
        cwd=str(_PROJECT_ROOT),
        check=False,
    )
    # pip install requests 应被拒绝
    assert result.returncode == 2, (
        f"期望 exit 2（denied），实际 exit {result.returncode}\nstderr: {result.stderr}"
    )


@pytest.mark.integration
def test_hook_handles_empty_stdin_gracefully() -> None:
    """空 stdin 或非 JSON → hook 不崩溃（fail-closed 原则：exit 0 跳过空命令）。"""
    env = {**os.environ, "PYTHONPATH": str(_PROJECT_ROOT)}
    result = subprocess.run(
        ["bash", str(_HOOK_PATH)],
        input="",
        capture_output=True,
        text=True,
        env=env,
        cwd=str(_PROJECT_ROOT),
        check=False,
    )
    # 空命令不含 pip/uv，应直接放行（exit 0）
    assert result.returncode == 0, f"期望 exit 0（空命令放行），实际 {result.returncode}"


# ===========================================================================
# deny 消息包含有用信息
# ===========================================================================


@pytest.mark.integration
def test_hook_deny_message_contains_helpful_guidance() -> None:
    """deny 时，stderr 应包含替代建议（requirements-locked.txt 路径提示）。"""
    result = _run_hook("pip install requests")
    # deny 消息应在 stderr 中
    assert result.returncode == 2
    # stderr 应包含引导信息
    stderr = result.stderr
    assert "DENIED" in stderr or "deny" in stderr.lower() or "requirements" in stderr.lower(), (
        f"deny 消息应包含有用提示，实际 stderr：{stderr!r}"
    )
