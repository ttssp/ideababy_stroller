"""
pars.orch — Run Orchestrator。

职责：接收 RunConfig，创建 git worktree，启动 claude -p worker 子进程，
协调 Stuck Detector 与 Budget Tracker，写 Ledger，管理 run 生命周期。

公开导出：
  T011 · worker env builder（C15/R4 API key 隔离）
  T013 · worker 生命周期 + worktree + stream parser
"""

# T011：worker subprocess env builder（C15/R4 API key 隔离）
from pars.orch.worker_env import (
    WorkerEnvConfig,
    assert_no_keys,
    build_worker_env,
    strip_key_env,
)

# T013：worker 生命周期主类
from pars.orch.worker import (
    Worker,
    WorkerConfig,
    WorkerHandle,
    cleanup,
    launch_worker,
    stop,
    wait,
)

# T013：git worktree 生命周期
from pars.orch.worktree import (
    WorktreeHandle,
    create_worktree,
    list_worktrees,
    remove_worktree,
)

# T013：claude -p stream-json 解析
from pars.orch.stream_parser import (
    ClaudeEvent,
    parse_stream,
)

__all__ = [
    # T011 · worker env
    "WorkerEnvConfig",
    "assert_no_keys",
    "build_worker_env",
    "strip_key_env",
    # T013 · worker 生命周期
    "Worker",
    "WorkerConfig",
    "WorkerHandle",
    "cleanup",
    "launch_worker",
    "stop",
    "wait",
    # T013 · worktree
    "WorktreeHandle",
    "create_worktree",
    "list_worktrees",
    "remove_worktree",
    # T013 · stream parser
    "ClaudeEvent",
    "parse_stream",
]
