"""
pars.budget — 预算追踪层。

职责：读写 runs/<id>/state.json 的 usd_spent 字段（原子 flock）；
实现 60s 轮询 BudgetMonitor 协程；为 proxy 的预估逻辑提供定价表。
由 T014 实现。
"""
