# PRD · <new-id> · "<composite title>" (composite)

**Version**: 1.0  (human-approved via fork)
**Created**: <ISO>
**Source**: <相对路径>/L3/stage-L3-scope-<source>.md · Candidates <X1, X2, ...>
**Approved by**: human moderator
**PRD-form**: composite
**Modules**: [<m1>, <m2>, <m3>]                  ← module-id 列表(从 fork-composite 命令交互得出)
**Module-forms**: {<m1>: simple, <m2>: simple, <m3>: simple}   ← 每个 module 内部的形态。**v3 阶段所有 module 锁定为 simple**;module-level phased / v1-direct 待 phase 5 加入(见 fork-composite.md Step 3.5 TODO)

## Problem / Context
(描述合成产品 — 不是单一 candidate,而是 N candidate 合体后的产品形态。从 scope-synthesizer §"如果合体长什么样"抄过来作为起点,然后扩展。)

## Users
(合成产品的最终目标用户。可能 N candidate 服务同一用户的不同需求,也可能服务多 persona。显式说明。)

## Core user stories
(顶层视角,跨模块的 user journey。具体 story 在每个 §Modules > <m> 子节里详细。)

| # | As a | I want | So that | Primary module |
|---|------|--------|---------|----------------|
| US1 | ... | ... | ... | m1 |
| US2 | ... | ... | ... | m1, m2 |

## Source candidates

合体来源(从 L3 stage doc 哪几个 candidate 合并):

| Module | Source candidate | 关键贡献 |
|--------|------------------|----------|
| m1 | Candidate A | <一句话> |
| m2 | Candidate B | <一句话> |
| m3 | Candidate C | <一句话> |

## Modules

每个 module 一节,内含独立 user stories / scope IN / scope OUT。

### Module: m1 (form: simple)

**Description**: ...
**User stories**: US1, US2 (顶层定义)
**Scope IN**:
- ...
**Scope OUT**:
- ...
**Module-internal outcomes**:
- O-m1-1: ...

### Module: m2 (form: simple)

**Description**: ...
**Scope IN**: ...
**Scope OUT**: ...

### Module: m3 (form: simple)

**Description**: ...
**Scope IN**: ...
**Scope OUT**: ...

<!--
v3 阶段所有 module form 锁定为 simple。下面这种 module-level phased 形态待 phase 5 实现后再启用:

### Module: m3 (form: phased)

**Description**: ...
**Phases**: [v0.1, v0.2]   ← 该 module 内部 phased,顶层依然是 composite
**Scope IN — v0.1**: ...
**Scope IN — v0.2**: ...
**Scope OUT**: ...
-->

<!-- v1-direct module 形态同样待 phase 5 -->


## Module dependency graph

```mermaid
graph LR
  m1[Module m1: <name>] --> m2[Module m2: <name>]
  m1 --> m3[Module m3: <name>]
  m2 --> m3
```

依赖说明:
- m1 → m2: m2 需要 m1 的 <output>
- m1 → m3: m3 需要 m1 的 <output>
- m2 → m3: m3 在用户流程上紧跟 m2

## Critical-path module

哪个 module 是 v1 的最小可发布(Minimum Viable Composite)?其他 module 缺失时产品仍可用吗?

- **关键路径**: <m1> — 没有它整个 composite 没意义
- **可延后**: <m3> — 即便 m3 未完成,m1+m2 已能交付一个粗糙但可用的产品
- **优先级理由**: ...

## Scope OUT (composite-level, 永久不做)

(顶层 OUT — 任何 module 都不该做。各 module 的 OUT 在 §Modules 内已写。)

- ...

## Success — observable outcomes (composite-level)

| # | Outcome | How measured | Spans modules |
|---|---------|--------------|---------------|
| O1 | ... | ... | m1, m2 |
| O2 | ... | ... | m3 |

(单 module outcome 在 §Modules 内已写。)

## Real-world constraints

| # | Constraint | Source | Rigidity | Module scope |
|---|------------|--------|----------|--------------|
| C1 | <time budget total>  | L3R0 Block 1 | Hard | all |
| C2 | <platform>           | L3R0 Block 4 | Hard | all |
| C3 | <red line>           | L3R0 Block 5 | Hard | all |
| C4 | <module-specific>    | candidate B | Soft | m2 |

## UX principles (tradeoff stances)

顶层 UX 立场(跨 module)。具体某个 module 可能有自己的 UX 调整,在 §Modules 内单独写。

## Biggest product risks

composite 特有的风险:
1. **集成复杂度风险**: N module 合作时的 join point 是否清晰?
2. **关键模块单点风险**: 关键路径 module(<m1>) 失败时整个 composite 价值归零
3. **scope creep 风险**: 中途想加 module 还是减 module?(用 /fork-module-out 处理)

## Open questions for L4 / Operator
- ...

---

## PRD Source
本 PRD 由 `/fork-composite` 命令从 L3 fork 自动生成,合并来自 candidates [<X1>, <X2>, ...]。

- L3 menu: discussion/.../<source>/L3/stage-L3-scope-<source>.md
- L2 unpack: discussion/.../<source>/L2/stage-L2-explore-<source>.md
- FORK-ORIGIN.md in this directory

本 PRD 是 L4 的 **真相源**。L4 spec-writer 必须为每个 module 产独立 spec-<module-id>.md(共 N 份),顶层 spec.md 退化为 index 列出 modules + 共享 architecture。

## Module 退路

如果中途要砍掉某个 module:`/fork-module-out <prd-id> <module-id>`。该命令会编辑本 PRD 并写 MODULE-OUT-LOG.md。
