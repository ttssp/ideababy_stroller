"""tests.integration.test_claude_dir_readonly — .claude/ fail-closed 只读分离集成测试。

T012 · C21 · R6:
验证 ensure_readonly_claude_dir 在各策略下真正阻止 worker 篡改 .claude/。

测试策略：
- 需要真实 bindfs 的测试：若 `bindfs` 未安装 → pytest.skip
- CI 环境：设置 RECALLKIT_ALLOW_UNSAFE_CHMOD=1 跑 chmod 路径（标记 banner 警告）
- Python 面 EACCES 测试（Codex R2）：mount 后 os.chmod / write_text 必须 raise PermissionError
- fail-closed 测试：mock bindfs 和 chflags 都不可用 → ReadonlyFailsClosed

注意：
- integration tests 使用真实 tmp 目录，不依赖网络
- `pytest.mark.integration` 标记所有集成测试
- 真正 bindfs mount 的测试在 `@pytest.mark.skipif` 控制下
"""

from __future__ import annotations

import os
import shutil
import stat
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

from pars.safety.integrity import compute_tree_sha256, verify_tree_unchanged
from pars.safety.readonly_mount import (
    MountResult,
    MountStrategy,
    ReadonlyFailsClosed,
    ReadonlyHandle,
    detect_best_strategy,
    ensure_readonly_claude_dir,
    mount_readonly,
    refuse_to_start,
    unmount,
)

# ---------------------------------------------------------------------------
# 辅助：检测 bindfs 是否真的可用
# ---------------------------------------------------------------------------

HAS_BINDFS = shutil.which("bindfs") is not None
ALLOW_UNSAFE_CHMOD = os.environ.get("RECALLKIT_ALLOW_UNSAFE_CHMOD") == "1"


def _make_template(tmp_path: Path) -> Path:
    """创建一个模拟 worker_claude_dir 的模板目录。"""
    template = tmp_path / "worker_claude_dir"
    template.mkdir()

    (template / "settings.json").write_text('{"version":"0.1"}', encoding="utf-8")
    (template / "CLAUDE.md").write_text("# Worker Instructions", encoding="utf-8")

    hooks = template / "hooks"
    hooks.mkdir()
    hook_script = hooks / "pre_tool_use.sh"
    hook_script.write_text("#!/bin/bash\nexit 0\n", encoding="utf-8")
    hook_script.chmod(0o755)

    return template


# ---------------------------------------------------------------------------
# Test 1: detect_best_strategy 在有 bindfs 时返回 BINDFS（mock which）
# ---------------------------------------------------------------------------

@pytest.mark.integration
def test_detect_best_strategy_should_return_bindfs_when_bindfs_available() -> None:
    """should return BINDFS when bindfs is available in PATH."""
    with (
        patch("pars.safety.readonly_mount.shutil.which") as mock_which,
        patch.dict(os.environ, {}, clear=False),
    ):
        # 清除 RECALLKIT_ALLOW_UNSAFE_CHMOD 避免干扰
        os.environ.pop("RECALLKIT_ALLOW_UNSAFE_CHMOD", None)

        def which_side_effect(name: str) -> str | None:
            if name == "bindfs":
                return "/usr/local/bin/bindfs"
            return None

        mock_which.side_effect = which_side_effect

        result = detect_best_strategy()
        assert result == MountStrategy.BINDFS


# ---------------------------------------------------------------------------
# Test 2: detect_best_strategy 全无 → REFUSE
# ---------------------------------------------------------------------------

@pytest.mark.integration
def test_detect_best_strategy_should_return_refuse_when_nothing_available() -> None:
    """should return REFUSE when bindfs, chflags, chattr all unavailable."""
    with (
        patch("pars.safety.readonly_mount.shutil.which", return_value=None),
        patch.dict(os.environ, {}, clear=False),
    ):
        os.environ.pop("RECALLKIT_ALLOW_UNSAFE_CHMOD", None)

        result = detect_best_strategy()
        assert result == MountStrategy.REFUSE


# ---------------------------------------------------------------------------
# Test 3: detect_best_strategy 在 ALLOW_UNSAFE_CHMOD=1 时返回 UNSAFE_CHMOD
# ---------------------------------------------------------------------------

@pytest.mark.integration
def test_detect_best_strategy_should_return_unsafe_chmod_when_env_set() -> None:
    """should return UNSAFE_CHMOD when RECALLKIT_ALLOW_UNSAFE_CHMOD=1 and no bindfs."""
    with (
        patch("pars.safety.readonly_mount.shutil.which", return_value=None),
        patch.dict(os.environ, {"RECALLKIT_ALLOW_UNSAFE_CHMOD": "1"}),
    ):
        result = detect_best_strategy()
        assert result == MountStrategy.UNSAFE_CHMOD


# ---------------------------------------------------------------------------
# Test 4: mount_readonly (bindfs) — 若可用则真正测试，否则 skip
# ---------------------------------------------------------------------------

@pytest.mark.integration
@pytest.mark.skipif(not HAS_BINDFS, reason="bindfs 未安装，跳过真实 mount 测试")
def test_mount_readonly_bindfs_should_prevent_write_when_mounted(tmp_path: Path) -> None:
    """should raise PermissionError when writing to bindfs-mounted read-only directory."""
    template = _make_template(tmp_path)
    worktree = tmp_path / "worktree"
    worktree.mkdir()
    claude_dir = worktree / ".claude"

    handle = ensure_readonly_claude_dir(worktree, template)
    try:
        settings = claude_dir / "settings.json"
        assert settings.exists(), "settings.json 应在 mount 后可见"

        # 核心验证：Python 面写操作必须失败（EACCES）
        with pytest.raises((PermissionError, OSError)):
            settings.write_text("tampered", encoding="utf-8")

        with pytest.raises((PermissionError, OSError)):
            os.chmod(str(settings), 0o644)

    finally:
        handle.release()


# ---------------------------------------------------------------------------
# Test 5: unmount 恢复可写（UNSAFE_CHMOD 模式）
# ---------------------------------------------------------------------------

@pytest.mark.integration
def test_unmount_should_restore_writability_after_unsafe_chmod(tmp_path: Path) -> None:
    """should remove target directory after unmount (UNSAFE_CHMOD mode)."""
    template = _make_template(tmp_path)
    target = tmp_path / "mounted_claude"

    result = mount_readonly(
        source=template,
        target=target,
        strategy=MountStrategy.UNSAFE_CHMOD,
    )

    assert target.exists()

    unmount(result)

    # UNSAFE_CHMOD unmount 会清除目标目录
    assert not target.exists()


# ---------------------------------------------------------------------------
# Test 6: refuse_to_start 输出含 OQ5 引导 + sys.exit(1)
# ---------------------------------------------------------------------------

@pytest.mark.integration
def test_refuse_to_start_should_exit_with_oq5_guidance(capsys: pytest.CaptureFixture[str]) -> None:
    """should print OQ5 guidance to stderr and raise SystemExit."""
    with pytest.raises(SystemExit) as exc_info:
        refuse_to_start("测试原因 · 单元验证")

    # 退出码为 1（fail-closed）
    assert exc_info.value.code == 1

    # stderr 包含 OQ5 关键提示
    captured = capsys.readouterr()
    assert "brew install" in captured.err or "macfuse" in captured.err.lower()
    assert "chmod" in captured.err


# ---------------------------------------------------------------------------
# Test 7: fail-closed — 无策略时 mount_readonly 抛 ReadonlyFailsClosed
# ---------------------------------------------------------------------------

@pytest.mark.integration
def test_mount_readonly_should_raise_readonly_fails_closed_when_strategy_refuse(
    tmp_path: Path,
) -> None:
    """should raise ReadonlyFailsClosed when strategy is REFUSE."""
    template = _make_template(tmp_path)
    target = tmp_path / "target"

    with pytest.raises((ReadonlyFailsClosed, SystemExit)):
        mount_readonly(
            source=template,
            target=target,
            strategy=MountStrategy.REFUSE,
        )


# ---------------------------------------------------------------------------
# Test 8: SHA-256 post-run 校验（第二道验证）
# ---------------------------------------------------------------------------

@pytest.mark.integration
def test_sha256_post_run_should_detect_tampering_after_chmod_mode(tmp_path: Path) -> None:
    """should return False from verify_tree_unchanged when file is modified post-run."""
    template = _make_template(tmp_path)
    target = tmp_path / "mounted"

    result = mount_readonly(
        source=template,
        target=target,
        strategy=MountStrategy.UNSAFE_CHMOD,
    )

    # 记录初始 SHA
    initial_sha = compute_tree_sha256(target)

    # 恢复可写（模拟 unmount 后再篡改，或者 chmod 被绕过的场景）
    for f in result.chmod_files:
        if f.exists():
            f.chmod(f.stat().st_mode | 0o644)

    # 篡改文件
    (target / "settings.json").write_text('{"TAMPERED": true}', encoding="utf-8")

    # post-run 校验：应返回 False（检测到篡改）
    assert verify_tree_unchanged(target, initial_sha) is False

    # 清理
    unmount(result)


# ---------------------------------------------------------------------------
# Test 9: Python 面 EACCES 测试（UNSAFE_CHMOD 模式，Codex R2 要求）
# ---------------------------------------------------------------------------

@pytest.mark.integration
def test_unsafe_chmod_should_prevent_write_via_python_pathlib(tmp_path: Path) -> None:
    """should raise PermissionError when write_text attempted on chmod-protected file.

    注意：UNSAFE_CHMOD 模式下，os.chmod 可以绕过（这正是为什么不是生产路径）。
    此测试验证 chmod a-w 能阻止普通写操作，但 os.chmod 本身仍能改回权限。
    """
    template = _make_template(tmp_path)
    target = tmp_path / "mounted"

    result = mount_readonly(
        source=template,
        target=target,
        strategy=MountStrategy.UNSAFE_CHMOD,
    )

    settings = target / "settings.json"
    assert settings.exists()

    # 验证普通写操作被阻止（chmod a-w 效果）
    # 确认文件不可写
    file_stat = settings.stat()
    assert not (file_stat.st_mode & stat.S_IWUSR), "settings.json 应该是只写不可"

    # 尝试写入 → 应该失败（PermissionError）
    with pytest.raises(PermissionError):
        settings.write_text("tampered", encoding="utf-8")

    # 清理
    unmount(result)


# ---------------------------------------------------------------------------
# Test 10: ensure_readonly_claude_dir 在 UNSAFE_CHMOD 模式下成功
# ---------------------------------------------------------------------------

@pytest.mark.integration
def test_ensure_readonly_claude_dir_should_succeed_in_unsafe_chmod_mode(
    tmp_path: Path,
) -> None:
    """should successfully create read-only .claude/ in UNSAFE_CHMOD mode."""
    template = _make_template(tmp_path)
    worktree = tmp_path / "worktree"
    worktree.mkdir()

    handle = ensure_readonly_claude_dir(
        worktree=worktree,
        template=template,
        strategy=MountStrategy.UNSAFE_CHMOD,
    )

    claude_dir = worktree / ".claude"
    assert claude_dir.exists()
    assert (claude_dir / "settings.json").exists()
    assert (claude_dir / "CLAUDE.md").exists()
    assert (claude_dir / "hooks" / "pre_tool_use.sh").exists()

    # 文件不可写
    settings = claude_dir / "settings.json"
    with pytest.raises(PermissionError):
        settings.write_text("tampered", encoding="utf-8")

    handle.release()
    assert not claude_dir.exists(), "release 后 .claude/ 应被清除"


# ---------------------------------------------------------------------------
# Test 11: ReadonlyHandle.release 幂等性（多次调用不崩溃）
# ---------------------------------------------------------------------------

@pytest.mark.integration
def test_readonly_handle_release_should_be_idempotent(tmp_path: Path) -> None:
    """should not crash when release() called multiple times."""
    template = _make_template(tmp_path)
    worktree = tmp_path / "worktree"
    worktree.mkdir()

    handle = ensure_readonly_claude_dir(
        worktree=worktree,
        template=template,
        strategy=MountStrategy.UNSAFE_CHMOD,
    )

    handle.release()  # 第一次
    # 第二次不应抛异常（即使目录已不存在）
    handle.release()  # 第二次


# ---------------------------------------------------------------------------
# Test 12: mount_readonly UNSAFE_CHMOD 应复制模板文件
# ---------------------------------------------------------------------------

@pytest.mark.integration
def test_mount_readonly_unsafe_chmod_should_copy_template_files(tmp_path: Path) -> None:
    """should copy all template files to target directory."""
    template = _make_template(tmp_path)
    target = tmp_path / "target"

    result = mount_readonly(
        source=template,
        target=target,
        strategy=MountStrategy.UNSAFE_CHMOD,
    )

    assert (target / "settings.json").exists()
    assert (target / "CLAUDE.md").exists()
    assert (target / "hooks" / "pre_tool_use.sh").exists()

    unmount(result)


# ---------------------------------------------------------------------------
# Test 13: bindfs 挂载后 Python 面写操作验证（若 bindfs 可用）
# ---------------------------------------------------------------------------

@pytest.mark.integration
@pytest.mark.skipif(not HAS_BINDFS, reason="bindfs 未安装，跳过真实 mount 测试")
def test_bindfs_mount_should_block_os_chmod_attempt(tmp_path: Path) -> None:
    """should raise PermissionError for os.chmod on bindfs-mounted file (Codex R2).

    这是 R1 BLOCKER #3 的关键验证：
    bindfs -o ro 在 kernel 层拒绝所有 write syscall，
    包括 os.chmod（在非 root 下 bindfs 保证此行为）。
    """
    template = _make_template(tmp_path)
    worktree = tmp_path / "worktree"
    worktree.mkdir()

    handle = ensure_readonly_claude_dir(worktree, template)
    settings = worktree / ".claude" / "settings.json"

    try:
        assert settings.exists()

        # bindfs -o ro 下，os.chmod 应抛 PermissionError
        with pytest.raises((PermissionError, OSError)):
            os.chmod(str(settings), 0o777)  # noqa: S103

        # write_text 也应失败
        with pytest.raises((PermissionError, OSError)):
            settings.write_text("tampered", encoding="utf-8")

        # shutil.copy2 也应失败
        with pytest.raises((PermissionError, OSError)):
            shutil.copy2(str(template / "settings.json"), str(settings))

    finally:
        handle.release()
