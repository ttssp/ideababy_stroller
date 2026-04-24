"""
pars.paths — 路径可移植层（D18 / R10 / C9 缓解）。

结论：所有路径均通过 env var 解析，绝不硬编码绝对路径，确保 H200 等远端机器可用。

设计原则：
1. 所有 accessor 函数是纯函数（pure function），每次调用读 os.environ
2. 不在 import time 创建目录（lazy — 由调用方或 ensure_run_tree 负责 mkdir）
3. 所有返回值均为绝对路径（Path.resolve()），防止 cwd 漂移导致路径失效
4. worktree_dir 无 env override（worktree 必须本地，见 architecture §2）

Env vars 一览：
- RECALLKIT_RUN_DIR   : run 数据目录根（默认 <cwd>/runs）
- RECALLKIT_CKPT_DIR  : checkpoint 目录根（默认 <cwd>/checkpoints）
- HF_HOME            : HuggingFace cache 目录（默认 ~/.cache/huggingface）
"""

from __future__ import annotations

import os
import subprocess
from pathlib import Path


# ---------------------------------------------------------------------------
# 内部辅助
# ---------------------------------------------------------------------------

def _base_runs() -> Path:
    """返回 run 数据目录根（绝对路径）。

    优先读 RECALLKIT_RUN_DIR，否则 <cwd>/runs。
    """
    env_val = os.environ.get("RECALLKIT_RUN_DIR")
    if env_val:
        return Path(env_val).resolve()
    return (Path.cwd() / "runs").resolve()


def _base_ckpts() -> Path:
    """返回 checkpoint 目录根（绝对路径）。

    优先读 RECALLKIT_CKPT_DIR，否则 <cwd>/checkpoints。
    """
    env_val = os.environ.get("RECALLKIT_CKPT_DIR")
    if env_val:
        return Path(env_val).resolve()
    return (Path.cwd() / "checkpoints").resolve()


# ---------------------------------------------------------------------------
# 公开 accessor — 均为纯函数，不创建目录
# ---------------------------------------------------------------------------

def run_dir(run_id: str) -> Path:
    """返回指定 run 的数据目录路径（绝对）。

    路径：$RECALLKIT_RUN_DIR/<run_id>  或  <cwd>/runs/<run_id>

    注意：只返回路径对象，不创建目录。需要创建目录请调用 ensure_run_tree()。
    """
    return _base_runs() / run_id


def ckpt_dir(run_id: str) -> Path:
    """返回指定 run 的 checkpoint 目录路径（绝对，worktree 外）。

    checkpoint 故意写在 worktree 外，防止 worktree 异常退出时 checkpoint 丢失。
    路径：$RECALLKIT_CKPT_DIR/<run_id>  或  <cwd>/checkpoints/<run_id>

    注意：只返回路径对象，不创建目录。
    """
    return _base_ckpts() / run_id


def worktree_dir(run_id: str) -> Path:
    """返回指定 run 的 git worktree 工作目录路径（绝对，无 env override）。

    worktree 必须本地（不支持跨机器），因此不提供 env 覆盖。
    路径：<cwd>/.worktrees/<run_id>

    注意：只返回路径对象，不创建目录。
    """
    return (Path.cwd() / ".worktrees" / run_id).resolve()


def hf_home() -> Path:
    """返回 HuggingFace cache 目录路径（绝对）。

    路径：$HF_HOME  或  ~/.cache/huggingface
    """
    env_val = os.environ.get("HF_HOME")
    if env_val:
        return Path(env_val).resolve()
    return (Path.home() / ".cache" / "huggingface").resolve()


def repo_root() -> Path:
    """返回当前 git 仓库根目录路径（通过 git rev-parse --show-toplevel）。

    若不在 git 仓库内，抛出 subprocess.CalledProcessError。
    """
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        capture_output=True,
        text=True,
        check=True,
    )
    return Path(result.stdout.strip()).resolve()


# ---------------------------------------------------------------------------
# 目录创建辅助（调用方主动调用，非 import 时自动执行）
# ---------------------------------------------------------------------------

def ensure_run_tree(run_id: str) -> None:
    """创建 run 所需的所有子目录（run_dir + ckpt_dir + run_dir/artifacts）。

    幂等（mkdir -p 语义），可重复调用。
    调用时机：Orchestrator 在 run 启动前调用一次。
    """
    # run 数据目录及子目录
    rd = run_dir(run_id)
    rd.mkdir(parents=True, exist_ok=True)
    (rd / "artifacts").mkdir(parents=True, exist_ok=True)

    # checkpoint 目录（worktree 外）
    ckpt_dir(run_id).mkdir(parents=True, exist_ok=True)
