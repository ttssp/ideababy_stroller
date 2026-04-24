"""
tests/unit/test_pip_policy.py — pip 白名单策略单元测试 (T015)

结论：严苛覆盖所有绕过尝试，验证三条等价白名单 ALLOW，其他全部 DENY。
对齐：architecture §7、T015.md、spec C17、R5。

命名约定：should_<action>_when_<condition>
"""

from __future__ import annotations

import pytest

from pars.safety.pip_policy import PipCommandDecision, evaluate_pip_command, is_pip_install_allowed


# ===========================================================================
# 三条等价白名单 — ALLOW
# ===========================================================================


def test_should_allow_when_pip_locked_with_require_hashes() -> None:
    """白名单1: pip install -r requirements-locked.txt --require-hashes 必须 ALLOW。"""
    cmd = "pip install -r requirements-locked.txt --require-hashes"
    result = evaluate_pip_command(cmd)
    assert result.decision == PipCommandDecision.ALLOW


def test_should_allow_when_uv_pip_install_locked_with_require_hashes() -> None:
    """白名单2: uv pip install -r requirements-locked.txt --require-hashes 必须 ALLOW。"""
    cmd = "uv pip install -r requirements-locked.txt --require-hashes"
    result = evaluate_pip_command(cmd)
    assert result.decision == PipCommandDecision.ALLOW


def test_should_allow_when_uv_sync_frozen() -> None:
    """白名单3: uv sync --frozen 必须 ALLOW（uv 原生 lockfile 模式，hash 等价）。"""
    cmd = "uv sync --frozen"
    result = evaluate_pip_command(cmd)
    assert result.decision == PipCommandDecision.ALLOW


# ===========================================================================
# DENY — 未指定 locked 文件
# ===========================================================================


def test_should_deny_unlocked_when_pip_install_package_directly() -> None:
    """pip install requests 无锁文件 — DENY_UNLOCKED。"""
    cmd = "pip install requests"
    result = evaluate_pip_command(cmd)
    assert result.decision == PipCommandDecision.DENY_UNLOCKED


def test_should_deny_unlocked_when_pip_install_git_url() -> None:
    """pip install git+https://... — DENY_UNLOCKED（git 拉取绕过 hash）。"""
    cmd = "pip install git+https://github.com/example/repo.git"
    result = evaluate_pip_command(cmd)
    assert result.decision == PipCommandDecision.DENY_UNLOCKED


def test_should_deny_unlocked_when_pip_install_wrong_requirements_file() -> None:
    """pip install -r some-other.txt --require-hashes — 错误文件名 DENY_UNLOCKED。"""
    cmd = "pip install -r some-other.txt --require-hashes"
    result = evaluate_pip_command(cmd)
    assert result.decision == PipCommandDecision.DENY_UNLOCKED


def test_should_deny_unlocked_when_pip_install_index_url() -> None:
    """pip install --index-url ... — 绕过官方源，DENY_UNLOCKED。"""
    cmd = "pip install --index-url https://example.com/simple requests"
    result = evaluate_pip_command(cmd)
    assert result.decision == PipCommandDecision.DENY_UNLOCKED


def test_should_deny_unlocked_when_pip_install_missing_dash_r_flag() -> None:
    """pip install requirements-locked.txt (遗漏 -r) — 文件作为包名，DENY_UNLOCKED。"""
    cmd = "pip install requirements-locked.txt"
    result = evaluate_pip_command(cmd)
    assert result.decision == PipCommandDecision.DENY_UNLOCKED


# ===========================================================================
# DENY — 缺少 --require-hashes
# ===========================================================================


def test_should_deny_no_hashes_when_pip_locked_file_without_require_hashes() -> None:
    """pip install -r requirements-locked.txt (无 --require-hashes) — DENY_NO_HASHES。"""
    cmd = "pip install -r requirements-locked.txt"
    result = evaluate_pip_command(cmd)
    assert result.decision == PipCommandDecision.DENY_NO_HASHES


# ===========================================================================
# DENY — 额外参数注入绕过（严格模式：禁止任何额外参数）
# ===========================================================================


def test_should_deny_when_pip_has_extra_verbose_flag() -> None:
    """pip install -r requirements-locked.txt --require-hashes -v — 额外参数，DENY。

    spec T015: 禁止任何额外参数，避免参数注入绕过。
    """
    cmd = "pip install -r requirements-locked.txt --require-hashes -v"
    result = evaluate_pip_command(cmd)
    assert result.decision != PipCommandDecision.ALLOW


def test_should_deny_when_pip_has_editable_flag() -> None:
    """-e 本地 editable 安装可绕 hash — DENY（严格模式：额外参数均拒绝）。"""
    cmd = "pip install -r requirements-locked.txt --require-hashes -e ."
    result = evaluate_pip_command(cmd)
    assert result.decision != PipCommandDecision.ALLOW


# ===========================================================================
# DENY — uv sync 系列
# ===========================================================================


def test_should_deny_uv_sync_unfrozen_when_no_frozen_flag() -> None:
    """uv sync (无 --frozen) — 会更新 lock，DENY_UV_SYNC_UNFROZEN。"""
    cmd = "uv sync"
    result = evaluate_pip_command(cmd)
    assert result.decision == PipCommandDecision.DENY_UV_SYNC_UNFROZEN


def test_should_deny_uv_add_when_used_to_modify_lock() -> None:
    """uv add requests — 修改 lock 文件，污染 worker，DENY_UV_ADD。"""
    cmd = "uv add requests"
    result = evaluate_pip_command(cmd)
    assert result.decision == PipCommandDecision.DENY_UV_ADD


def test_should_deny_uv_pip_install_single_package() -> None:
    """uv pip install requests (无 -r locked file) — DENY_UNLOCKED。"""
    cmd = "uv pip install requests"
    result = evaluate_pip_command(cmd)
    assert result.decision == PipCommandDecision.DENY_UNLOCKED


# ===========================================================================
# DENY — python -m pip / easy_install / pipx 等变体
# ===========================================================================


def test_should_deny_unknown_when_python_m_pip_install() -> None:
    """python -m pip install requests — 绕过 hook 的变体，DENY_UNKNOWN。"""
    cmd = "python -m pip install requests"
    result = evaluate_pip_command(cmd)
    assert result.decision == PipCommandDecision.DENY_UNKNOWN


def test_should_deny_unknown_when_easy_install() -> None:
    """easy_install pkg — 已废弃安装工具，DENY_UNKNOWN。"""
    cmd = "easy_install requests"
    result = evaluate_pip_command(cmd)
    assert result.decision == PipCommandDecision.DENY_UNKNOWN


# ===========================================================================
# pip3 变体
# ===========================================================================


def test_should_deny_unlocked_when_pip3_install_package() -> None:
    """pip3 install requests — pip3 变体，DENY_UNKNOWN（非 pip/uv 前缀）。"""
    cmd = "pip3 install requests"
    result = evaluate_pip_command(cmd)
    # pip3 不在识别的白名单格式中，deny 即可（具体类型不强制）
    assert result.decision != PipCommandDecision.ALLOW


# ===========================================================================
# 命令注入绕过
# ===========================================================================


@pytest.mark.unit
def test_should_deny_when_command_injection_via_and_operator() -> None:
    """命令注入: pip install -r requirements-locked.txt --require-hashes && malicious。

    shlex.split 的 tokens 数量会超过白名单定义，严格比较即拒绝。
    """
    cmd = "pip install -r requirements-locked.txt --require-hashes && malicious"
    result = evaluate_pip_command(cmd)
    # && 作为 shlex token，tokens 列表会 > 白名单长度，严格匹配失败
    assert result.decision != PipCommandDecision.ALLOW


@pytest.mark.unit
def test_should_deny_when_shell_variable_injection() -> None:
    """shell 变量: pip install $(cat malicious.txt) — DENY（不 exec eval）。

    shlex.split 会把 $(cat malicious.txt) 作为单 token，tokens 不匹配白名单。
    """
    cmd = "pip install $(cat malicious.txt)"
    result = evaluate_pip_command(cmd)
    assert result.decision != PipCommandDecision.ALLOW


# ===========================================================================
# 多空格规范化 (allow)
# ===========================================================================


def test_should_allow_when_multiple_spaces_normalized() -> None:
    """多空格: pip  install  -r requirements-locked.txt --require-hashes — normalize 后 ALLOW。"""
    cmd = "pip  install  -r requirements-locked.txt --require-hashes"
    result = evaluate_pip_command(cmd)
    assert result.decision == PipCommandDecision.ALLOW


# ===========================================================================
# 空字符串与边界情况
# ===========================================================================


def test_should_deny_unknown_when_empty_string() -> None:
    """空字符串 — DENY_UNKNOWN。"""
    result = evaluate_pip_command("")
    assert result.decision == PipCommandDecision.DENY_UNKNOWN


def test_should_allow_when_pip_version_command() -> None:
    """pip --version — 非 install 命令，policy 不干预，ALLOW（或 DENY_UNKNOWN）。

    注：per T015.md: 非 pip install 命令不应被 hook 拦截；
    但 evaluate_pip_command 仅处理 pip/uv 开头命令，pip --version 不含 install，
    此处明确：不是 install 类命令，policy 返回 ALLOW。
    """
    result = evaluate_pip_command("pip --version")
    # pip --version 不是 install 操作，不在 deny 路径
    assert result.decision == PipCommandDecision.ALLOW


def test_should_allow_when_pip_list_command() -> None:
    """pip list — 非 install 命令，ALLOW。"""
    result = evaluate_pip_command("pip list")
    assert result.decision == PipCommandDecision.ALLOW


# ===========================================================================
# is_pip_install_allowed 兼容性接口测试
# ===========================================================================


def test_is_pip_install_allowed_returns_true_for_valid_pip_command() -> None:
    """is_pip_install_allowed 接口：合法命令返回 (True, ...)。"""
    ok, reason = is_pip_install_allowed("pip install -r requirements-locked.txt --require-hashes")
    assert ok is True
    assert isinstance(reason, str)


def test_is_pip_install_allowed_returns_false_for_invalid_pip_command() -> None:
    """is_pip_install_allowed 接口：非法命令返回 (False, reason)。"""
    ok, reason = is_pip_install_allowed("pip install requests")
    assert ok is False
    assert len(reason) > 0  # reason 不为空


def test_is_pip_install_allowed_returns_true_for_uv_sync_frozen() -> None:
    """is_pip_install_allowed 接口：uv sync --frozen 返回 (True, ...)。"""
    ok, _ = is_pip_install_allowed("uv sync --frozen")
    assert ok is True
