# Forge v7 · 006 · P3R2 · GPT55xHigh · 联合收敛 R2(finalize)

**Timestamp**: 2026-07-07T16:34:42Z
**Visibility**: 我已读对方 P3R1。
**Convergence mode**: strong-converge

## 1. 我对每条分歧的最终立场 + 让步

- **分歧1**:接受“执行属于拥有 job 生命周期的 companion”。最终:SKILL 先轮询,目标态 companion watchdog;XenoDev runtime 走授权。让步:companion 为最终层。
- **分歧2**:接受“scope 语义先修文档-实现一致”。最终:branch-scope 默认;沙箱失败降级 working-tree;空 diff 不 approve。让步:判定进 SKILL。
- **分歧3**:接受“最小 schema 扩展”。最终:只加 per-phase status+gate 读取规则。让步:不重构 phased spec。
- **分歧4**:接受“FULL 向后兼容”。最终:fork-id 进 SHARED-CONTRACT,FULL 接 `001-radar-pA`,path-safe。让步:无。

## 2. 联合 verdict(单一)

**refactor,不 redesign、不 cut codex;无 unresolved。** K1:review gate 状态机,codex primary,breaker+watchdog+routing+审计+half-open。K2:超时先落 SKILL 轮询,目标态 XenoDev companion watchdog。K3:fork-id 进 SHARED-CONTRACT SSOT,FULL 兼容已铸 id,双仓 fixture 契约测试。硬约束:IDS mirror 三层同步;XenoDev runtime 经 handoff/backlog。

## 3. 残余分歧降级为 v0.2 note

- v0.2 note 1:watchdog 阈值经 3-5 次 fallback 校准。
- v0.2 note 2:KG-33 先 guard+alert,复现后裁根因。
- v0.2 note 3:后台任务 liveness+单实例锁再事故则组件化。

## 4. W 形态产出的初步草稿建议

- W verdict-only:保留强 gate+codex primary,单通道 gate 改 breaker/watchdog/routing/contract-tests 状态机。
- W decision-list:保留 review gate、codex primary、fallback 不冒充、production path 真跑、fail-closed;调整 SKILL 三分类/timeout/verdict fallback/空 diff、branch-scope+沙箱降级、CODEOWNERS routing、KG-22 phase status;删除逐例 regex、仓根 HANDOFF 唯一 fork、pid liveness;新增 fork-id 章、fixture、merge-queue 重验、companion 授权、单实例锁。
- W refactor-plan:1) codex-review SKILL:breaker/watchdog/fallback matrix/空 diff/审计/half-open;2) SHARED-CONTRACT:grammar/path-safe/FULL compat/table/fixture;3) XenoDev:companion watchdog/status,gen-handback fork-id,KG-33/34 guard+checklist。
