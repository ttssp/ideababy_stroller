"""
pars.orch — Run Orchestrator。

职责：接收 RunConfig，创建 git worktree，启动 claude -p worker 子进程，
协调 Stuck Detector 与 Budget Tracker，写 Ledger，管理 run 生命周期。
由 T007 实现。
"""
