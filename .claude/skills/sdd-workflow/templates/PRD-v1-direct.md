# PRD · <new-id> · "<candidate title>" (v1-direct)

**Version**: 1.0  (human-approved via fork)
**Created**: <ISO>
**Source**: <相对路径>/L3/stage-L3-scope-<source>.md · Candidate <X>
**Approved by**: human moderator
**PRD-form**: v1-direct
**Skip-rationale**: |
  <这里是 ≥100 字的 prose,必须显式提及 C1/C2/C3 中至少 1 条:
   - C1 假设已外部验证(用户研究/同质市场/已有 N 个验证赛道) — 不需要 v0.1 来验证用户是否要这个
   - C2 v0.1 没有独立可发布价值(协议/SDK/平台类,半个不能用)
   - C3 多 candidate 互补(本来就是同一产品的不同器官,砍一刀反而是负担)
   fork-v1 命令拒绝 <100 字或缺 C1/C2/C3 的 rationale。>

## Problem / Context
(从 candidate 抄过来,扩展 L2 上下文。注意:这里描述的应该是 v1 形态的产品,不是 v0.1 切片。)

## Users
(v1 的目标用户。因为不走 v0.1,这里要更具体 — 没有"先打靶看反应"的兜底。)

## Core user stories (v1)

| # | As a | I want | So that |
|---|------|--------|---------|
| US1 | ... | ... | ... |
| US2 | ... | ... | ... |

## Scope IN (v1)

直接 v1 scope,不分阶段。

- ...

## Scope OUT

- ...

## Success — observable outcomes (v1)

| # | Outcome | How measured |
|---|---------|--------------|
| O1 | ... | ... |

## Real-world constraints

| # | Constraint | Source | Rigidity |
|---|------------|--------|----------|
| C1 | <time budget for v1>  | L3R0 Block 1 | Hard |
| C2 | <platform>            | L3R0 Block 4 | Hard |
| C3 | <red line>            | L3R0 Block 5 | Hard |

## UX principles (tradeoff stances)
(从 candidate §"UX priorities" 抄过来)

## Biggest product risk
(常规产品风险)

## Risk: skip-v0.1 (必填对冲条款)

跳过 v0.1 意味着放弃"早期反馈兜底"。本节是必填的对冲条款 — 如果 v1 上线后核心假设错了,fallback path 是什么?

### 假设 A: <skip-rationale 中的核心假设>
- **如果错了的征兆**: <用户行为信号 / 客观 metric>
- **fallback 时间窗口**: <我们最多承受多久才必须切换>
- **fallback 路径**: <降级到哪 — partial pivot / 砍 scope / 重新走 L3?>

### 假设 B: ...

(2-3 段。这部分内容 spec-writer 会抄到 risks.md 的 R-skip-v0.1 条目。)

## Open questions for L4 / Operator
- ...

---

## PRD Source
本 PRD 由 `/fork-v1` 命令从 L3 fork 自动生成。skip-rationale 由 operator 在 fork 时交互式提供并通过校验(≥100 字 + 必含 C1/C2/C3 之一)。

- L3 menu: discussion/.../<source>/L3/stage-L3-scope-<source>.md
- L2 unpack: discussion/.../<source>/L2/stage-L2-explore-<source>.md
- FORK-ORIGIN.md in this directory

本 PRD 是 L4 的 **真相源**。L4 spec-writer 必须:
- SLA.md 顶部加 §"Skip rationale"(从本 PRD frontmatter 抄过来)
- risks.md 必含 R-skip-v0.1 条目(从本 PRD §"Risk: skip-v0.1" 抄过来)
- Outcomes / Scope 直接 v1,不分阶段

## 反悔通道

如果 v1-direct 决策后觉得太冒进,可以用 `/fork-phased <src> from-L3 <candidate> as <new-id-alt>` 在同一个 source 上 fork 一个 phased 版本作平行 sibling,两版同时跑(或 abandon v1-direct 走 phased)。
