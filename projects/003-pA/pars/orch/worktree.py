"""Git worktree 生命周期管理。

v0.1 一个 worker 对应一个 worktree:
  - 创建:git worktree add <target_path> -b worktree-<run_id> <base_ref>
  - 清理:git worktree remove <target_path> + git branch -d <branch_name>
  - failure-safe:若进程异常退出,worktree lock 文件留存;
                 操作员可手工 `git worktree remove --force` 清理

结论:
  - create_worktree 使用 run_id 生成确定性分支名 worktree-<run_id>
  - remove_worktree force=False 时会保留 dirty worktree 并报错
  - list_worktrees 解析 `git worktree list --porcelain` 原生输出
"""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path

from pars.logging import get_logger

logger = get_logger(__name__)

# branch 前缀约定
_BRANCH_PREFIX = "worktree-"


@dataclass
class WorktreeHandle:
    """git worktree 的描述符。

    字段:
        path:      worktree 在文件系统上的绝对路径
        branch:    worktree 所在 branch 名(格式: worktree-<run_id>)
        base_ref:  创建时的基准 ref (HEAD / main / commit-sha)
    """

    path: Path
    branch: str
    base_ref: str


def create_worktree(
    base_dir: Path,
    run_id: str,
    *,
    base_ref: str = "HEAD",
) -> WorktreeHandle:
    """创建 git worktree。

    执行:
        git worktree add <base_dir>/<run_id> -b worktree-<run_id> <base_ref>

    Args:
        base_dir: worktree 根目录(如 .worktrees/)
        run_id:   run 的唯一标识(ULID)
        base_ref: 基准 git ref(默认 HEAD)

    Returns:
        WorktreeHandle

    Raises:
        subprocess.CalledProcessError: git 命令失败(如分支已存在)
        FileNotFoundError: git 不在 PATH 中
    """
    target_path = Path(base_dir).resolve() / run_id
    branch_name = f"{_BRANCH_PREFIX}{run_id}"

    target_path.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        "git", "worktree", "add",
        str(target_path),
        "-b", branch_name,
        base_ref,
    ]

    logger.info(
        "创建 git worktree",
        extra={"path": str(target_path), "branch": branch_name, "base_ref": base_ref},
    )

    try:
        subprocess.run(  # noqa: S603
            cmd,
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as exc:
        raise subprocess.CalledProcessError(
            exc.returncode,
            exc.cmd,
            exc.output,
            exc.stderr,
        ) from exc

    logger.info(
        "git worktree 创建成功",
        extra={"path": str(target_path), "branch": branch_name},
    )
    return WorktreeHandle(
        path=target_path,
        branch=branch_name,
        base_ref=base_ref,
    )


def remove_worktree(handle: WorktreeHandle, *, force: bool = False) -> None:
    """清理 git worktree。

    步骤:
    1. git worktree remove [--force] <path>
    2. git branch -d <branch>  (仅 force=False 时;force=True 时 branch-d 可能失败被忽略)

    Args:
        handle: create_worktree 返回的 WorktreeHandle
        force:  True 时忽略 dirty state(测试 / 熔断路径);
                False 时 dirty worktree 会导致 git worktree remove 失败

    Raises:
        subprocess.CalledProcessError: git 命令失败(如 dirty worktree 且 force=False)
    """
    path = handle.path
    branch = handle.branch

    # step 1: git worktree remove
    rm_cmd = ["git", "worktree", "remove"]
    if force:
        rm_cmd.append("--force")
    rm_cmd.append(str(path))

    logger.info(
        "移除 git worktree",
        extra={"path": str(path), "force": force},
    )

    subprocess.run(  # noqa: S603
        rm_cmd,
        check=True,
        capture_output=True,
        text=True,
    )

    # step 2: 删除 branch
    branch_cmd = ["git", "branch", "-d", branch]
    try:
        subprocess.run(  # noqa: S603
            branch_cmd,
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as exc:
        if force:
            # force 路径:branch 删除失败不致命(可能已被其他操作处理)
            logger.warning(
                "force 模式 git branch -d 失败(已忽略)",
                extra={"branch": branch, "stderr": exc.stderr},
            )
        else:
            raise

    logger.info("git worktree 清理完成", extra={"path": str(path), "branch": branch})


def list_worktrees() -> list[WorktreeHandle]:
    """解析 `git worktree list --porcelain` 输出，返回 WorktreeHandle 列表。

    porcelain 格式示例(每个 worktree 块以空行分隔):
        worktree /abs/path/to/main
        HEAD abc123def
        branch refs/heads/main

        worktree /abs/path/to/.worktrees/run-01
        HEAD def456abc
        branch refs/heads/worktree-run-01

    注意:
    - 主 worktree(第一块)的 branch 可能是 (HEAD detached at ...)
    - 只返回 branch 以 worktree- 前缀开头的 worktree
    - 裸仓库行以 "bare" 标记,跳过

    Returns:
        仅含 worktree-<run_id> 分支的 WorktreeHandle 列表
    """
    try:
        result = subprocess.run(  # noqa: S603
            ["git", "worktree", "list", "--porcelain"],
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as exc:
        logger.error(
            "git worktree list 失败",
            extra={"stderr": exc.stderr},
        )
        return []

    handles: list[WorktreeHandle] = []
    blocks = result.stdout.strip().split("\n\n")

    for block in blocks:
        if not block.strip():
            continue

        wt_path: str | None = None
        wt_branch: str | None = None
        wt_head: str | None = None
        is_bare = False

        for line in block.strip().splitlines():
            if line.startswith("worktree "):
                wt_path = line[len("worktree "):]
            elif line.startswith("branch "):
                # format: refs/heads/<branch_name>
                ref = line[len("branch "):]
                wt_branch = ref.replace("refs/heads/", "", 1)
            elif line.startswith("HEAD "):
                wt_head = line[len("HEAD "):]
            elif line == "bare":
                is_bare = True

        if is_bare or wt_path is None:
            continue
        if wt_branch is None or not wt_branch.startswith(_BRANCH_PREFIX):
            # 主 worktree 或非 worktree-* 分支,跳过
            continue

        handles.append(
            WorktreeHandle(
                path=Path(wt_path),
                branch=wt_branch,
                base_ref=wt_head or "HEAD",
            )
        )

    return handles
