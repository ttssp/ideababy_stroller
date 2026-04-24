"""
pars.orch — Run Orchestrator。

职责：接收 RunConfig，创建 git worktree，启动 claude -p worker 子进程，
协调 Stuck Detector 与 Budget Tracker，写 Ledger，管理 run 生命周期。
由 T007 实现。

公开导出（T011 · worker env builder · C15/R4）：
"""

# T011：worker subprocess env builder（C15/R4 API key 隔离）
from pars.orch.worker_env import (
    WorkerEnvConfig,
    assert_no_keys,
    build_worker_env,
    strip_key_env,
)

__all__ = [
    "WorkerEnvConfig",
    "assert_no_keys",
    "build_worker_env",
    "strip_key_env",
]
