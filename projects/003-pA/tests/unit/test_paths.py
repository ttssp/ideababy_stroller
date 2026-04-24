"""
tests.unit.test_paths — pars.paths 路径可移植层单元测试。

覆盖：
- 默认值（无 env var）
- env var 覆盖（有 env var）
- 路径拼接（run_id 追加）
- 绝对路径性质（returned path must be absolute）
- ensure_run_tree 不在 import 时创建目录（延迟创建）
- worktree_dir 无 env override
"""

import os
import subprocess
from pathlib import Path

import pytest


# ---------------------------------------------------------------------------
# 辅助：测试结束后恢复 env
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def clean_env(monkeypatch):
    """确保每个测试有干净的 env（清除可能残留的 override）。"""
    for key in (
        "RECALLKIT_RUN_DIR",
        "RECALLKIT_CKPT_DIR",
        "HF_HOME",
    ):
        monkeypatch.delenv(key, raising=False)
    yield


# ---------------------------------------------------------------------------
# run_dir 测试
# ---------------------------------------------------------------------------

class TestRunDir:
    """should return correct run directory path."""

    def test_should_return_absolute_path_when_no_env_var_set(self):
        """should return absolute path under ./runs/ when RECALLKIT_RUN_DIR not set."""
        from pars.paths import run_dir
        result = run_dir("01HXYZ")
        assert result.is_absolute(), f"期望绝对路径，实际：{result}"

    def test_should_contain_run_id_when_default_path(self):
        """should contain run_id as last component when using default path."""
        from pars.paths import run_dir
        result = run_dir("01HXYZ")
        assert result.name == "01HXYZ", f"期望最后部分为 run_id，实际：{result.name}"

    def test_should_end_with_runs_prefix_when_default_path(self):
        """should have 'runs' parent directory when no env var set."""
        from pars.paths import run_dir
        result = run_dir("01HXYZ")
        # 默认 ./runs/<id> 解析后，parent 名称应为 runs
        assert result.parent.name == "runs", (
            f"期望父目录为 runs，实际：{result.parent}"
        )

    def test_should_use_env_var_when_recallkit_run_dir_set(self, monkeypatch):
        """should return env-var-based path when RECALLKIT_RUN_DIR is set."""
        monkeypatch.setenv("RECALLKIT_RUN_DIR", "/tmp/foo")
        from pars.paths import run_dir
        result = run_dir("01HXYZ")
        # 用 Path.resolve() 比较，兼容 macOS /tmp → /private/tmp symlink
        expected = Path("/tmp/foo/01HXYZ").resolve()
        assert result == expected, (
            f"期望 {expected}，实际：{result}"
        )

    def test_should_not_create_directory_on_call(self, tmp_path, monkeypatch):
        """should NOT create the directory when run_dir() is called (lazy mkdir)."""
        from pars.paths import run_dir
        monkeypatch.setenv("RECALLKIT_RUN_DIR", str(tmp_path / "runs"))
        result = run_dir("01HXYZ")
        # 函数只返回路径，不创建目录
        assert not result.exists(), f"run_dir() 不应创建目录，但 {result} 存在"


# ---------------------------------------------------------------------------
# ckpt_dir 测试
# ---------------------------------------------------------------------------

class TestCkptDir:
    """should return correct checkpoint directory path."""

    def test_should_return_absolute_path_when_no_env_var_set(self):
        """should return absolute path when RECALLKIT_CKPT_DIR not set."""
        from pars.paths import ckpt_dir
        result = ckpt_dir("01HXYZ")
        assert result.is_absolute(), f"期望绝对路径，实际：{result}"

    def test_should_contain_run_id_as_last_part(self):
        """should have run_id as the last path component."""
        from pars.paths import ckpt_dir
        result = ckpt_dir("01HXYZ")
        assert result.name == "01HXYZ"

    def test_should_use_env_var_when_recallkit_ckpt_dir_set(self, monkeypatch):
        """should return env-var-based path when RECALLKIT_CKPT_DIR is set."""
        monkeypatch.setenv("RECALLKIT_CKPT_DIR", "/tmp/ckpts")
        from pars.paths import ckpt_dir
        result = ckpt_dir("01HXYZ")
        # 用 Path.resolve() 比较，兼容 macOS /tmp → /private/tmp symlink
        expected = Path("/tmp/ckpts/01HXYZ").resolve()
        assert result == expected, (
            f"期望 {expected}，实际：{result}"
        )

    def test_should_not_create_directory_on_call(self, tmp_path, monkeypatch):
        """should NOT create directory when ckpt_dir() is called."""
        monkeypatch.setenv("RECALLKIT_CKPT_DIR", str(tmp_path / "ckpts"))
        from pars.paths import ckpt_dir
        result = ckpt_dir("01HXYZ")
        assert not result.exists()


# ---------------------------------------------------------------------------
# worktree_dir 测试
# ---------------------------------------------------------------------------

class TestWorktreeDir:
    """should return correct worktree directory path with no env override."""

    def test_should_return_absolute_path(self):
        """should return absolute path for worktree dir."""
        from pars.paths import worktree_dir
        result = worktree_dir("01HXYZ")
        assert result.is_absolute()

    def test_should_have_worktrees_parent_dir(self):
        """should have .worktrees as parent directory name."""
        from pars.paths import worktree_dir
        result = worktree_dir("01HXYZ")
        assert result.parent.name == ".worktrees", (
            f"期望父目录为 .worktrees，实际：{result.parent.name}"
        )

    def test_should_not_be_overridden_by_env(self, monkeypatch):
        """should ignore any RECALLKIT_* env vars (worktree is always local)."""
        # worktree 不应有 env override；即使设置其他 env，结果也固定走 .worktrees/
        monkeypatch.setenv("RECALLKIT_RUN_DIR", "/remote/runs")
        from pars.paths import worktree_dir
        result = worktree_dir("01HXYZ")
        assert ".worktrees" in str(result), (
            f"worktree_dir 应走本地 .worktrees/，实际：{result}"
        )


# ---------------------------------------------------------------------------
# hf_home 测试
# ---------------------------------------------------------------------------

class TestHfHome:
    """should return correct HuggingFace cache directory path."""

    def test_should_return_default_cache_path_when_no_env(self):
        """should return ~/.cache/huggingface when HF_HOME not set."""
        from pars.paths import hf_home
        result = hf_home()
        expected = Path.home() / ".cache" / "huggingface"
        assert result == expected, f"期望 {expected}，实际：{result}"

    def test_should_use_env_var_when_hf_home_set(self, monkeypatch):
        """should return HF_HOME value when env var is set."""
        monkeypatch.setenv("HF_HOME", "/data/hf_cache")
        from pars.paths import hf_home
        result = hf_home()
        # 用 resolve() 比较，兼容 macOS symlink 展开
        expected = Path("/data/hf_cache").resolve()
        assert result == expected, (
            f"期望 {expected}，实际：{result}"
        )


# ---------------------------------------------------------------------------
# repo_root 测试
# ---------------------------------------------------------------------------

class TestRepoRoot:
    """should return the git repository root."""

    def test_should_return_absolute_path(self):
        """should return an absolute path when inside a git repo."""
        from pars.paths import repo_root
        result = repo_root()
        assert result.is_absolute()

    def test_should_be_a_git_repo(self):
        """should return a path that contains a .git directory or file."""
        from pars.paths import repo_root
        result = repo_root()
        # git worktree 里 .git 是个文件，主 repo 里是个目录
        assert (result / ".git").exists(), (
            f"{result} 不含 .git（非 git root）"
        )


# ---------------------------------------------------------------------------
# ensure_run_tree 测试
# ---------------------------------------------------------------------------

class TestEnsureRunTree:
    """should create the full run directory tree when called."""

    def test_should_create_run_directory_when_called(self, tmp_path, monkeypatch):
        """should create runs/<id>/ directory when ensure_run_tree() is called."""
        monkeypatch.setenv("RECALLKIT_RUN_DIR", str(tmp_path / "runs"))
        monkeypatch.setenv("RECALLKIT_CKPT_DIR", str(tmp_path / "ckpts"))
        from pars.paths import ensure_run_tree
        ensure_run_tree("01HXYZ")
        expected = tmp_path / "runs" / "01HXYZ"
        assert expected.is_dir(), f"期望 {expected} 已被创建"

    def test_should_create_ckpt_directory_when_called(self, tmp_path, monkeypatch):
        """should create checkpoints/<id>/ directory when ensure_run_tree() is called."""
        monkeypatch.setenv("RECALLKIT_RUN_DIR", str(tmp_path / "runs"))
        monkeypatch.setenv("RECALLKIT_CKPT_DIR", str(tmp_path / "ckpts"))
        from pars.paths import ensure_run_tree
        ensure_run_tree("01HXYZ")
        expected = tmp_path / "ckpts" / "01HXYZ"
        assert expected.is_dir(), f"期望 {expected} 已被创建"

    def test_should_be_idempotent_when_called_twice(self, tmp_path, monkeypatch):
        """should not raise when called twice (idempotent mkdir -p)."""
        monkeypatch.setenv("RECALLKIT_RUN_DIR", str(tmp_path / "runs"))
        monkeypatch.setenv("RECALLKIT_CKPT_DIR", str(tmp_path / "ckpts"))
        from pars.paths import ensure_run_tree
        ensure_run_tree("01HXYZ")
        ensure_run_tree("01HXYZ")  # 第二次不应抛异常
