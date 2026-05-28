---
fork_kind: PRD-fork
fork_at: 2026-05-28
parent: discussion/006/forge/v3/stage-forge-006-v3.md
parent_section: §W4 "Next-version PRD draft(v0.2 PRD · 可直接进 plan-start)" L298-365
parent_prd: discussion/006a-pM/PRD.md(v0.1 · ship 封箱)
fork_id: 006a-pM-v0.2
prd_form: simple
operator_manual_l3: true
naming_note: "v0.2 后缀显式表达 006a-pM 的 v0.2 演进;父 fork 006a-pM 已 ship · 本 fork 不重做 L1-L3,直接以 forge v3 verdict 为 PRD draft"
---

# Fork origin · 006a-pM-v0.2

## Lineage

```
proposals/proposals.md §006
  ↓ (forge v1)
discussion/006/forge/v1/stage-forge-006-v1.md
  ↓ (forge v2)
discussion/006/forge/v2/stage-forge-006-v2.md
  ↓ B2.2 Block B operator manual L3 fork
discussion/006a-pM/PRD.md(v0.1 · XenoDev v0.1 SHIP 封箱 2026-05-25)
  ↓ HANDBACK batch 2(ENTRY 7-17 · 11 项 backlog 累积)
discussion/006/forge/v3/stage-forge-006-v3.md(v3 verdict converged · 0 unresolved)
  ↓ §W4 "Next-version PRD draft" L298-365 是符合 simple PRD 形态完整 draft
  ↓ operator 接受 [A] decision menu(2026-05-28)
本 fork: discussion/006a-pM-v0.2/PRD.md
```

## 为什么不走 IDS L1-L3

per forge v3 stage doc §W4 + 父 fork 006a-pM FORK-ORIGIN.md §"为什么不走 IDS L1-L3":

- v3 stage doc §W4 已是符合 simple PRD 形态的完整 draft(IN/OUT/Success/Constraints/UX/OQ 全章)
- 父 fork 006a-pM 已 ship v0.1 · v0.2 是 backlog-driven 增量 · 不是新 idea
- v3 forge 已 converged(strong-converge · 0 unresolved · 3/3 分歧 closed · 1 v0.2-note)
- 重走 L1-L3 = 浪费 + 偏离 v3 verdict(K9 binding)

## fork-id 命名

`006a-pM-v0.2` 平铺命名:
- `006a-pM` = 父 fork id(v0.1 ship 封箱)
- `-v0.2` = 显式 v0.2 演进版本号
- 不严格匹配 SHARED-CONTRACT §6.2.1 约束 6 regex `^[0-9]{3}[a-z]?(-p[A-Z])?$`,但与父 fork
  006a-pM 的 `naming_note` 一致 · 既有仓库 004-pB 也存在 v0.2/v0.3 sub-plan 范式

与 IDS 既有 fork 范式对齐:001-pA / 003-pA / 004-pB / 006a-pM / 007a-pA(全平铺 · 平级 discussion/)

## scope of fork

**只覆盖 v3 forge stage doc 11 项 backlog 三类**(mirror rebuild × 4 + protocol revision × 4 + xenodev lib bug × 3);不再重审 v2 verdict 大架构(IDS=治理 / XenoDev=唯一 L4 / 双向 hand-off · K9 binding)。

任何 cross-cutting 关切 → escalate 到新 forge v4(参 forge v3 stage doc §"Decision menu [B]")。

## downstream(本 fork 下一步)

- ✅ /plan-start 006a-pM-v0.2 → 产 discussion/006a-pM-v0.2/L4/HANDOFF.md
- ⏭ XenoDev build runtime 消费 HANDOFF · 按 W5 dev plan phase 1/2/3 + phase X 真路径 ship
- ⏭ wave 1 + 2 + 3 各产 1 IDS commit(per W5 dev plan)+ XenoDev 单独 task ship B-4-XenoDev runtime
- ⏭ wave 3 verify-all-outcomes.sh SHIP-READY 关闭 v0.2(per success criterion)
