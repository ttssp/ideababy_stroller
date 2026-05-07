---
description: Fork multiple L3 candidates into ONE composite PRD with modules. Suitable when N candidates are complementary (different organs of same product), not alternatives. Use parallel /fork sibling instead if candidates are alternatives competing for the same need.
argument-hint: "<source-id> from-L3 <candidates-csv> as <new-id>  e.g. 005 from-L3 A,B,C as 005-pAll"
allowed-tools: Read, Write, Bash(mkdir:*), Bash(cp:*), Bash(ls:*), Bash(date:*), AskUserQuestion, Glob, Grep
model: sonnet
---

# /fork-composite · 多 candidate 合 1 PRD

> 本命令把多个 L3 candidate 合并成 1 份 composite PRD,各 candidate 变成 module。
> **关键判断**:仅当 candidate 间是"互补"关系时合理。如果是"替代"(同需求的不同方案),应该用 `/fork` 多次创建并行 sibling 子树而不是 composite。
> 共享 /fork.md 的 Step 1(定位源)和 Step 5-6(更新 fork log/输出菜单)。

Parse `$ARGUMENTS` as: `<source-id> from-L3 <candidates-csv> as <new-id>`

例: `005 from-L3 A,B,C as 005-pAll`(从 005 的 L3 stage doc 合并 candidate A、B、C 为新 fork 005-pAll)
例: `005 from-L3 direction-1,direction-3 as 005-pCompose`

## Step 1 — locate source stage doc (shared with /fork)

按 /fork.md Step 1 同规则。**强制 from-L3**。

## Step 2 — parse candidates CSV and verify each exists (改造 /fork Step 2)

把 `<candidates-csv>` 按逗号切分,得到 candidate spec 列表(如 `[A, B, C]`)。**逐个**在 stage doc 里验证存在,若任一缺失则报错并显示完整候选列表。

**约束**:
- candidates 数量 ≥2(若 =1 提示用 /fork 或 /fork-phased 即可)
- 数量 ≥3 时打印警告 "composite-of-N(N≥3) 演化成本高,推荐 N=2 起步;N≥3 请确认每个 module 都是必要器官"

## Step 3 — confirm with human (shared with /fork, 改造)

显示要合并的 candidates 列表 + 新 fork 路径,Y/N 确认。confirmation 块要展示 §"Candidate relationships" §1 关系矩阵的核心结论(从 stage doc 抄过来):

```
About to fork (composite):
  Source:     discussion/<root>/.../L3/stage-L3-scope-<source>.md
  Candidates: A "<title-A>", B "<title-B>", C "<title-C>"
  New id:     <new-id>
  Path:       discussion/<root>/.../<new-id>/

Relationship analysis from synthesizer:
  A↔B: <互补/替代/顺承>
  A↔C: ...
  B↔C: ...
  Synthesizer recommended PRD-form: <X>

⚠ Verify these are truly complementary (not alternatives).
  If alternatives, use parallel /fork instead.

Proceed? [y/N]
```

## Step 3.5 — interactive: name modules + declare module-forms (NEW)

用 AskUserQuestion 询问 operator:

**Question 1**(对每个 candidate): 给它起一个 module-id(默认从 candidate 名提,如 "A 'PRD Clarifier'" → 默认 `clarifier`)?

**Question 2**(对每个 module): 该 module 内部形态?
- simple(**v3 唯一选项**)— scope IN 仅 v0.1

> **TODO(phase 5)**:module-level phased / v1-direct 在 v3 阶段尚未实现 — 下游 spec-writer 和 task-decomposer 还没有相应的透传与处理逻辑(若 module 标 phased,phase gate 会丢失;若标 v1-direct,skip-rationale 校验不会触发)。
>
> 待 phase 5 补完以下能力后再开放:
> - spec-writer 处理 module-level phased(产 spec-`<m>`-v0.1.md / spec-`<m>`-v1.0.md 多文件,per-module phase gate)
> - spec-writer 处理 module-level v1-direct(per-module R-skip-v0.1 条目)
> - plan-start 把每个 module 的内部形态透传给下游
> - task-decomposer 按 per-module phase_target 切 DAG
>
> 当前命令直接默认填 `module-form: simple` 给所有 module,**不向 operator 暴露 phased/v1-direct 选项**。spec-writer 的 Phase 0 校验也会拦截非 simple 的 module-form(避免有人手工改 PRD frontmatter 跳过本约束)。

**Question 3**: 哪个 module 是 critical-path(整个 composite 的最小可发布)?

**Question 4**: 各 module 间有依赖吗?(用箭头描述,如 `m1 → m2, m1 → m3`)

记录所有答案到本地变量。所有 module 的 form 字段统一填 `simple`。

## Step 4 — perform the fork (composite PRD generation)

### 4a. mkdir + write FORK-ORIGIN.md (shared,扩展)

建目录 `discussion/.../<new-id>/`。FORK-ORIGIN.md 在 `Selected candidate` 一节:

```markdown
**Selected candidates** (composite,N=<count>):
- <module-id-1>: from candidate A "<title>"
- <module-id-2>: from candidate B "<title>"
- <module-id-3>: from candidate C "<title>"

**PRD-form**: composite
**Modules**: [<m1>, <m2>, <m3>]
**Module-forms**: {<m1>: simple, <m2>: simple, <m3>: phased}
**Critical-path module**: <m1>
```

### 4b. write PRD.md using PRD-composite template

读 `.claude/skills/sdd-workflow/templates/PRD-composite.md` 作为骨架。**关键替换**:

- frontmatter `**Modules**` / `**Module-forms**` 按 Step 3.5 答案填
- `## Source candidates` 表格按 Step 3.5 Q1 答案填
- `## Modules` 下每个 module 一节,内容来自对应 candidate 的 user stories / scope IN / scope OUT(从 stage doc 抄)
  - module 内部形态 = simple → 直接抄 candidate scope
  - module 内部形态 = phased → 拓展为 `### Scope IN — v0.1` / `### Scope IN — v0.2`(同 PRD-phased 模板生成逻辑)
  - module 内部形态 = v1-direct → 该 module 起 `**Skip-rationale**: |<prose>` + `### Risk: skip-v0.1 (module-level)`
- `## Module dependency graph` mermaid 图按 Step 3.5 Q4 答案画
- `## Critical-path module` 按 Step 3.5 Q3 答案
- `## Core user stories` 表格 — 顶层视角,Primary module 列指向各 module
- `## Success — observable outcomes` 表格 — 跨 module 的 outcomes 在顶层,单 module outcomes 在 §Modules 内

写入 `discussion/.../<new-id>/PRD.md`。

## Step 5 — update source stage doc Fork log (shared)

```markdown
## Fork log
- <ISO> · candidates #<X1>+#<X2>+#<X3> forked as `<new-id>` (PRD-form: composite, modules: [m1,m2,m3])
```

## Step 6 — output next-step menu

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Forked (composite): <new-id> created at discussion/.../<new-id>/

PRD-form:           composite
Modules:            [<m1>, <m2>, <m3>]
Module-forms:       {<m1>: simple, <m2>: simple, <m3>: phased}
Critical-path:      <m1>
Module dependencies: m1 → m2, m1 → m3

Trace:
  proposals/proposals.md (entry <root>)
    → discussion/<root>/.../L3/stage-L3-scope-<source>.md (candidates #<X1>+#<X2>+#<X3>)
      → discussion/<root>/.../<new-id>/PRD.md (composite)

📋 Next steps:

[1] Start L4 for <new-id> immediately (recommended)
    → /plan-start <new-id>
       (spec-writer will produce one spec.md as INDEX + spec-<module>.md per module
        + risks.md / SLA.md with Module column.)

[2] Review/edit PRD.md before plan-start
    → cat discussion/.../<new-id>/PRD.md
       特别检查:每个 module 的 Scope IN/OUT 是否对的、依赖图是否合理

[3] Re-think — drop a module before plan-start
    → /fork-module-out <new-id> <module-id>
       (会编辑 PRD,如果剩 1 module 会提示降级为 simple)

[4] I changed my mind — re-fork as parallel siblings instead
    → /fork <source> from-L3 <candidate-A> as <new-id>-pA
    → /fork <source> from-L3 <candidate-B> as <new-id>-pB
    (然后可以 /abandon 这个 composite fork)

[5] Just stop
    → /status <new-id> anytime later

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Reply 1-5 or describe.
```

## Notes

- **composite 何时合理**:多 candidate 设计为同一产品的不同器官,合体后整体 > 各部分之和。例:idea 001 research radar 的"采集 / 解析 / 知识库 / 主动补齐 / 时间线"5 块本来就是一个产品。
- **composite vs parallel forking**:如果 candidate 间是"替代"(竞争同一需求),用多次 /fork 创建 sibling 子树更优 — sibling 允许 abandon 任何一个,composite 一旦下注就要全做(或用 /fork-module-out 退路)。
- **N=2 vs N≥3**:N=2 推荐起步,N≥3 演化成本高(集成复杂度、scope creep 风险)。
- **module 共享代码**:utils/、shared types 等跨 module 共享代码归属在 task-decomposer 阶段决定,用 `module: shared` 命名空间。
- **退路**:`/fork-module-out` 命令可砍 module。**不能删到只剩 0 个** — 应改用 `/abandon`。
- **不允许 from-L1 / from-L2**:composite 需要 L3 candidate 的完整结构。
