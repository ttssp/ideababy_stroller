"""
pars.budget — 预算追踪层（T018 · 第二道保险兜底）。

职责：
  - BudgetTracker：60s 轮询读 state.json（usd_spent 来自 T010 proxy 权威值），
    计算 wall_clock / 累计 GPU hours，写回 state。
  - BudgetMonitor：daemon Thread，每 60s tick 一次，cap 突破时发 SIGINT。

注意：
  - USD 硬帽主控制归 T010 proxy 前置拒绝（C20）。
  - 本模块仅负责 wall_clock / gpu_hours 的 60s 兜底 SIGINT。
  - USD 兜底路径（60s 轮询读到 usd_spent > cap）会触发 warning + SIGINT，
    但正常情况下不应走到这里（T010 proxy 应已前置拦截）。
"""

from pars.budget.tracker import BudgetMonitor, BudgetStatus, BudgetTracker

__all__ = ["BudgetMonitor", "BudgetStatus", "BudgetTracker"]
