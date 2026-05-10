---
fork_kind: PRD-fork
fork_at: 2026-05-10
parent: discussion/006/forge/v2/stage-forge-006-v2.md
parent_section: §"Next-version PRD draft (W4 — XenoDev v0.1)" L228-285
fork_id: 006a-pM
prd_form: simple
operator_manual_l3: true
naming_note: "M=Mock/B2.2 路线;符合 SHARED-CONTRACT §6.2.1 约束 6 regex ^[0-9]{3}[a-z]?(-p[A-Z])?$"
---

# Fork origin · 006a-pM

## Lineage

```
proposals/proposals.md
  ↓ (L1)
discussion/006/L1/stage-L1-inspire.md(historical;L1 内容已被 forge v1/v2 覆盖)
  ↓ (forge,跳 L2-L3)
discussion/006/forge/v1/stage-forge-006-v1.md
  ↓ (forge v2)
discussion/006/forge/v2/stage-forge-006-v2.md
  ↓ §"Next-version PRD draft (W4)" L228-285 是符合 SHARED-CONTRACT §1 8 字段 schema 的完整 PRD draft
  ↓ (B2.2 Block B operator manual L3 + extract;不走 IDS 完整 L1-L3,per stage doc §"模块 B" + §"B2 流" M4)
本 fork: discussion/006a-pM/PRD.md
```

## 为什么不走 IDS L1-L3

per moderator-notes §五 第一性事实 + stage doc §"B2 流" M4:
> 在 IDS 给 forge v2 §"Next-version PRD draft" 加 §"Real constraints" + §"Open questions"(1-2h 手工 L3),不走 IDS 完整 L1-L3 流程

L1-L3 已被 forge v1 + v2 覆盖(L1 inspire / L2 explore / L3 scope 的思考全部在 stage doc verdict);再走完整 L1-L3 = 浪费 + 偏离 stage doc verdict。

## fork-id 命名(与 IDS 既有范式对齐)

`006a-pM` 平铺命名:
- `006` = discussion id(forge 006)
- `a` = sub-fork variant
- `-pM` = parent variant M(M=Mock,B2.2 路线特有;真 PRD ship 后可 fork 出 `006a-pA`)
- 完整匹配约束 6 regex `^[0-9]{3}[a-z]?(-p[A-Z])?$`(B2.2 dry-run 已实证)

与 IDS 既有 fork 范式对齐:001-pA / 003-pA / 004-pB / 007a-pA(全平铺);本 fork 加入序列。

## scope of fork

**只写 XenoDev v0.1 这一个目标**;不混 forge governance / IDS framework 改进等。任何 cross-cutting 关切 → escalate 到 IDS forge(per stage doc 强制 forge 元层锁)。

## downstream(本 fork 下一步)

per `plan-rosy-naur` v11 B2.2 sub-plan:
- ✅ Block B(本 fork 落地,operator 接受 stage doc 初稿 + 4 件 done)
- ⏭ Block C cp PRD 进 XenoDev + bootstrap → operator 跨仓自跑
- ⏭ Block D-G XenoDev L4 spec/task/build/ship + hand-back 闭环 → operator 主导
