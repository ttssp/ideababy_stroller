# PRD-base 模板(共享底座)

> **用途**:这是所有 PRD-form(simple / phased / composite / v1-direct)共享的字段与章节。各 fork 命令在生成 PRD.md 时,先复制本模板的"通用部分",再叠加各形态特异的章节。
>
> **本文件不是 PRD,不该被 fork 命令直接复制为成品**。它是模板的"基类"。

## 通用 frontmatter(所有形态都有)

```markdown
# PRD · <new-id> · "<candidate title>"

**Version**: 1.0  (human-approved via fork)
**Created**: <ISO>
**Source**: <相对路径到 stage-L3-scope-*.md> · Candidate <X>
**Approved by**: human moderator
**PRD-form**: simple | phased | composite | v1-direct      ← 必填,缺失默认 simple
```

## 形态特异 frontmatter(由 fork 命令按需添加)

```markdown
**Phases**: [v0.1, v1.0]                       # 仅 phased,数组,任意 ≥2 个命名 phase
**Modules**: [<m1>, <m2>, ...]                  # 仅 composite,数组
**Module-forms**: {<m1>: simple, <m2>: phased}  # 仅 composite,字典
**Skip-rationale**: |                           # 仅 v1-direct,≥100 字 + 必含 C1/C2/C3 之一
  <prose,详细论证为什么跳过 v0.1>
```

## 通用章节(所有形态都有)

```markdown
## Problem / Context
(从 candidate 的 v0.1 段或 v1 段抄过来,扩展 L2 上下文)

## Users
(从 candidate §"User persona" 抄过来,扩展 L2 personas)

## Core user stories
(从 candidate §"user stories" 抄过来,编号 US1/US2/...)

## Real-world constraints
(从 L3R0-intake ✅ hard constraints + candidate 的时间/平台等综合)

| # | Constraint | Source | Rigidity |
|---|------------|--------|----------|
| C1 | <time budget> | L3R0 Block 1 | Hard |
| C2 | <platform>    | L3R0 Block 4 | Hard |
| C3 | <business model> | L3R0 Block 3 | Soft |
| C4 | <red line>    | L3R0 Block 5 | Hard |

## UX principles (tradeoff stances)
(从 candidate §"UX priorities" 抄过来)

## Open questions for L4 / Operator
(任何 ❓ 项 L3 未解决的;关键项会阻塞 build)

---

## PRD Source
本 PRD 由 /fork-* 命令从 L3 candidate 自动生成。完整上下文(为何这种切法、scope-reality 判决、比较矩阵)见:

- L3 menu: <相对路径>
- L2 unpack: <相对路径>
- FORK-ORIGIN.md: 本目录

本 PRD 是 L4 spec-writer 的 **真相源**。修改 PRD 必须 operator 显式批准 — L4 agents 永不自动改 PRD。
```

## 各形态在 base 之上叠加什么(速查)

| 形态 | 新增 frontmatter | 新增主体章节 | Scope 章节怎么写 |
|---|---|---|---|
| **simple** | `**PRD-form**: simple` | (无) | `## Scope IN` 单段 + `## Scope OUT` 单段 |
| **phased** | `**Phases**: [...]` | `## Phase transition learning` | `## Scope IN` 下分 N 个 `### Scope IN — <phase-id>`;`## Scope OUT` 也分子节(永久 OUT vs 仅当前 phase OUT) |
| **composite** | `**Modules**` + `**Module-forms**` | `## Source candidates` / `## Modules`(每 module 一节) / `## Module dependency graph` / `## Critical-path module` | `## Scope IN` 在每个 `## Modules > <m>` 子节内独立写;顶层 `## Scope IN` 退化为"全部 modules 全做" |
| **v1-direct** | `**Skip-rationale**: \|<prose>` | `## Risk: skip-v0.1`(必填,2-3 段对冲) | `## Scope IN (v1)` + `## Scope OUT`,无 v0.1 段 |
