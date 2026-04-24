"""tests.unit.test_worktree — git worktree 生命周期单元测试。

结论:
  使用 tmp git repo(tmp_git_repo fixture)进行真实 git 操作,
  覆盖 create_worktree / remove_worktree / list_worktrees 的所有路径。

测试矩阵(>=8):
  1. should create worktree when given valid run_id
  2. should create directory and branch when worktree created
  3. should use worktree- prefix for branch naming
  4. should use specified base_ref when creating worktree
  5. should raise CalledProcessError when branch already exists
  6. should remove worktree and branch when remove_worktree called
  7. should raise CalledProcessError when dirty worktree with force=False
  8. should remove dirty worktree when force=True
  9. should list only worktree-* branches in list_worktrees
  10. should return empty list when no worktree-* branches exist
"""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from pars.orch.worktree import (
    WorktreeHandle,
    create_worktree,
    list_worktrees,
    remove_worktree,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def tmp_git_repo(tmp_path: Path) -> Path:
    """创建一个带初始 commit 的临时 git 仓库,供 worktree 测试使用。"""
    repo = tmp_path / "repo"
    repo.mkdir()

    subprocess.run(["git", "init", "-b", "main"], cwd=str(repo), check=True, capture_output=True)
    subprocess.run(
        ["git", "config", "user.email", "test@example.com"],
        cwd=str(repo), check=True, capture_output=True,
    )
    subprocess.run(
        ["git", "config", "user.name", "Test"],
        cwd=str(repo), check=True, capture_output=True,
    )

    # 创建初始 commit(git worktree 需要至少一个 commit)
    readme = repo / "README.md"
    readme.write_text("# test\n", encoding="utf-8")
    subprocess.run(["git", "add", "."], cwd=str(repo), check=True, capture_output=True)
    subprocess.run(
        ["git", "commit", "-m", "init"],
        cwd=str(repo), check=True, capture_output=True,
    )
    return repo


@pytest.fixture()
def worktree_base(tmp_path: Path) -> Path:
    """独立的 worktree 目标根目录。"""
    base = tmp_path / "worktrees"
    base.mkdir()
    return base


# ---------------------------------------------------------------------------
# create_worktree 测试
# ---------------------------------------------------------------------------


def test_should_create_worktree_when_given_valid_run_id(
    tmp_git_repo: Path, worktree_base: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    """should create worktree when given valid run_id — 基本创建路径。"""
    monkeypatch.chdir(tmp_git_repo)

    run_id = "test-run-001"
    handle = create_worktree(worktree_base, run_id)

    assert isinstance(handle, WorktreeHandle)
    assert handle.path == worktree_base / run_id
    assert handle.branch == f"worktree-{run_id}"

    # 清理
    remove_worktree(handle)


def test_should_create_directory_when_worktree_created(
    tmp_git_repo: Path, worktree_base: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    """should create directory and branch when worktree created — 目录和 branch 应存在。"""
    monkeypatch.chdir(tmp_git_repo)

    run_id = "test-run-002"
    handle = create_worktree(worktree_base, run_id)

    # 目录存在
    assert handle.path.is_dir()

    # branch 存在:git branch --list worktree-test-run-002
    result = subprocess.run(
        ["git", "branch", "--list", f"worktree-{run_id}"],
        cwd=str(tmp_git_repo), capture_output=True, text=True, check=True,
    )
    assert f"worktree-{run_id}" in result.stdout

    # 清理
    remove_worktree(handle)


def test_should_use_worktree_prefix_for_branch_naming(
    tmp_git_repo: Path, worktree_base: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    """should use worktree- prefix for branch naming — branch 命名规范。"""
    monkeypatch.chdir(tmp_git_repo)

    run_id = "01HZZZ9Y5W7J4X2Q3R6M8N0P1T"  # 类 ULID 格式
    handle = create_worktree(worktree_base, run_id)

    assert handle.branch == f"worktree-{run_id}"
    assert handle.branch.startswith("worktree-")

    # 清理
    remove_worktree(handle)


def test_should_use_specified_base_ref_when_creating_worktree(
    tmp_git_repo: Path, worktree_base: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    """should use specified base_ref when creating worktree — base_ref 应写入 handle。"""
    monkeypatch.chdir(tmp_git_repo)

    run_id = "test-run-004"
    # 用 main 作为 base_ref
    handle = create_worktree(worktree_base, run_id, base_ref="main")

    assert handle.base_ref == "main"

    # 清理
    remove_worktree(handle)


def test_should_raise_when_branch_already_exists(
    tmp_git_repo: Path, worktree_base: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    """should raise CalledProcessError when branch already exists — 重复 branch 冲突。"""
    monkeypatch.chdir(tmp_git_repo)

    run_id = "test-run-005"
    handle = create_worktree(worktree_base, run_id)

    try:
        # 第二个 worktree_base2 避免 path 冲突,但 branch 已存在
        worktree_base2 = worktree_base.parent / "worktrees2"
        worktree_base2.mkdir(exist_ok=True)

        with pytest.raises(subprocess.CalledProcessError):
            create_worktree(worktree_base2, run_id)  # branch worktree-test-run-005 已存在
    finally:
        remove_worktree(handle)


# ---------------------------------------------------------------------------
# remove_worktree 测试
# ---------------------------------------------------------------------------


def test_should_remove_worktree_and_branch_when_remove_called(
    tmp_git_repo: Path, worktree_base: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    """should remove worktree and branch when remove_worktree called — 正常清理路径。"""
    monkeypatch.chdir(tmp_git_repo)

    run_id = "test-run-006"
    handle = create_worktree(worktree_base, run_id)
    assert handle.path.is_dir()

    remove_worktree(handle)

    # 目录已删除
    assert not handle.path.exists()

    # branch 已删除
    result = subprocess.run(
        ["git", "branch", "--list", f"worktree-{run_id}"],
        cwd=str(tmp_git_repo), capture_output=True, text=True, check=True,
    )
    assert result.stdout.strip() == ""


def test_should_raise_when_dirty_worktree_force_false(
    tmp_git_repo: Path, worktree_base: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    """should raise CalledProcessError when dirty worktree with force=False。"""
    monkeypatch.chdir(tmp_git_repo)

    run_id = "test-run-007"
    handle = create_worktree(worktree_base, run_id)

    # 在 worktree 里创建未跟踪文件,造成 dirty state
    (handle.path / "untracked.txt").write_text("dirty", encoding="utf-8")

    try:
        with pytest.raises(subprocess.CalledProcessError):
            remove_worktree(handle, force=False)
    finally:
        # 强制清理
        remove_worktree(handle, force=True)


def test_should_remove_dirty_worktree_when_force_true(
    tmp_git_repo: Path, worktree_base: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    """should remove dirty worktree when force=True — 熔断路径。"""
    monkeypatch.chdir(tmp_git_repo)

    run_id = "test-run-008"
    handle = create_worktree(worktree_base, run_id)

    # 创建 staged 文件,造成 dirty state
    dirty_file = handle.path / "staged.txt"
    dirty_file.write_text("staged content", encoding="utf-8")
    subprocess.run(["git", "add", "staged.txt"], cwd=str(handle.path), check=True, capture_output=True)

    # force=True 应该成功
    remove_worktree(handle, force=True)
    assert not handle.path.exists()


# ---------------------------------------------------------------------------
# list_worktrees 测试
# ---------------------------------------------------------------------------


def test_should_list_only_worktree_branches_in_list_worktrees(
    tmp_git_repo: Path, worktree_base: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    """should list only worktree-* branches in list_worktrees — 过滤正确。"""
    monkeypatch.chdir(tmp_git_repo)

    run_id_a = "test-list-run-a"
    run_id_b = "test-list-run-b"
    handle_a = create_worktree(worktree_base, run_id_a)
    handle_b = create_worktree(worktree_base, run_id_b)

    try:
        handles = list_worktrees()

        branches = {h.branch for h in handles}
        assert f"worktree-{run_id_a}" in branches
        assert f"worktree-{run_id_b}" in branches

        # 主 worktree(main branch)不应出现
        assert "main" not in branches
    finally:
        remove_worktree(handle_a)
        remove_worktree(handle_b)


def test_should_return_empty_list_when_no_worktree_branches(
    tmp_git_repo: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    """should return empty list when no worktree-* branches exist。"""
    monkeypatch.chdir(tmp_git_repo)

    handles = list_worktrees()

    # 刚初始化的 repo 没有 worktree-* 分支
    assert isinstance(handles, list)
    assert len(handles) == 0
