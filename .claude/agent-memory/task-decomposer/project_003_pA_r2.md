---
name: 003-pA task-decomposer R2 model routing
description: R11 成本缓解策略 - Opus 工时份额 ≤ 15%,仅保留 3 条 contract-heavy 安全收口任务
type: project
---

**Scope**: 仅适用于 `specs/003-pA/`。任务编号(T012/T017/T020)是 003-pA 特定的,**不要**直接复用到其他 idea。**可以借鉴**的是判据:"Opus 预算只留给改一个字节泄密 / single-source-of-truth 契约的任务,不按 risk_level=high 自动给 Opus" — 这条启发式对所有 fork 的 task-decomposer 工作通用。

---

2026-04-24 task-decomposer R2 为 spec 003-pA v0.2 做的模型路由再平衡。

**决策**:Opus 仅保留 T012(`.claude/` fail-closed)、T017(Stuck 状态机 single-truth)、T020(FailureAttribution schema)三条 contract-heavy 安全任务。

**Why**:R11 风险(首版路由 Opus 工时占比 38.4%,目标 ≤15%)+ C2 350-450h 预算 + C3 无商业预算。降 Sonnet/Codex 不降任务严苛度(只换 reviewer)。

**How to apply**:后续若再加 task,Opus 预算只留给"改一个字节泄密"或"single source of truth 契约"的任务,不按 risk_level=high 就自动给 Opus。
