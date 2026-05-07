# PRD · <new-id> · "<candidate title>" (phased)

**Version**: 1.0  (human-approved via fork)
**Created**: <ISO>
**Source**: <相对路径>/L3/stage-L3-scope-<source>.md · Candidate <X>
**Approved by**: human moderator
**PRD-form**: phased
**Phases**: [v0.1, v1.0]                  ← 任意 ≥2 个命名 phase。fork-phased 命令交互问 operator 决定。例:[v0.1, v0.2] / [v0.1, v0.2, v1.0] / [v0.1, v1.0]
**Phase-current**: v0.1                   ← 当前正在做的 phase

## Problem / Context
(从 candidate 抄过来,扩展 L2 上下文。phased 的 Problem 通常涵盖最终 phase 的视野,但 v0.1 只切一刀。)

## Users
(从 candidate §"User persona" 抄过来。各 phase 的 user 可以重叠或扩展。)

## Core user stories
(用 phase 标签分组。某些 story 跨 phase。)

| # | As a | I want | So that | Phase target |
|---|------|--------|---------|--------------|
| US1 | ... | ... | ... | v0.1 |
| US2 | ... | ... | ... | v0.1 |
| US3 | ... | ... | ... | v1.0 |

## Scope IN

### Scope IN — v0.1
(从 candidate §"Scope IN" 抄过来作为 v0.1 起点)

### Scope IN — v1.0
(对 candidate 的延伸,加入"v0.1 后再做"的部分。这部分允许 ❓ 占位"待 v0.1 反馈后补",但应该至少有 3-5 条候选条目让方向清晰。)

## Scope OUT

### 永久 OUT(任何 phase 都不做)
- ...

### 当前 phase OUT(本 phase 不做但未来 phase 可能做)
- v0.1 不做但 v1.0 会做: ...

## Phase transition learning

显式列出 1-3 条**v0.1 上线后必须验证的假设**,这些假设的回答决定 v1.0 的具体内容:

1. **假设**: v0.1 用户最常用的 user story 是 US? — 如果不是 US1,v1.0 要重排优先级
2. **假设**: 用户对 <核心 outcome> 的反应符合预期(success metric ≥ 阈值) — 如果不符,v1.0 scope IN 第 2 条要重写
3. **假设**: ...

phase 转换的触发由 operator 显式决定(ship v0.1 → 跑 quality-gate → 收集反馈 → 决定启动 v1.0 build)。

## Success — observable outcomes

按 phase 分组,每条带可度量定义。

### v0.1 outcomes
| # | Outcome | How measured |
|---|---------|--------------|
| O1 | ... | ... |
| O2 | ... | ... |

### v1.0 outcomes (subject to v0.1 learnings)
| # | Outcome | How measured |
|---|---------|--------------|
| O3 | ... | ... |

## Real-world constraints

| # | Constraint | Source | Rigidity | Phase scope |
|---|------------|--------|----------|-------------|
| C1 | <time budget v0.1>   | L3R0 Block 1 | Hard | v0.1 |
| C2 | <time budget v1.0>   | operator | Soft | v1.0 |
| C3 | <platform>           | L3R0 Block 4 | Hard | both |
| C4 | <red line>           | L3R0 Block 5 | Hard | both |

## UX principles (tradeoff stances)
(从 candidate §"UX priorities" 抄过来。注意 phased 项目的 UX 立场可能随 phase 演进 — 如 v0.1 重速度、v1.0 重精致 — 显式标注。)

## Biggest product risk
(主要产品风险。phased 项目额外加一条:phase 间用户流失风险 — v0.1 → v1.0 期间用户为什么不离开?)

## Open questions for L4 / Operator
- 关键项(阻塞 v0.1 build):
- v1.0 待定项(允许暂时 ❓):

---

## PRD Source
本 PRD 由 `/fork-phased` 命令从 L3 fork 自动生成。phases 由 operator 在 fork 时交互式声明。

- L3 menu: discussion/.../<source>/L3/stage-L3-scope-<source>.md
- L2 unpack: discussion/.../<source>/L2/stage-L2-explore-<source>.md
- FORK-ORIGIN.md in this directory

本 PRD 是 L4 的 **真相源**。L4 spec-writer 必须按 PRD 声明的 phases 产 SLA.md / risks.md / spec.md 各 phase 分段。
