---
description: Fork a candidate from L3 into a phased PRD (≥2 named phases like [v0.1, v1.0] or [v0.1, v0.2]). Suitable when v0.1 is a designed first slice with clear v1 vision; phase transition learning is recorded in PRD.
argument-hint: "<source-id> from-L3 <candidate-spec> as <new-id>  e.g. 003 from-L3 candidate-A as 003-pA"
allowed-tools: Read, Write, Bash(mkdir:*), Bash(cp:*), Bash(ls:*), Bash(date:*), AskUserQuestion, Glob, Grep
model: sonnet
---

# /fork-phased · 单 candidate ≥2 phase

> 本命令是 phased 形态的 fork。**from-L3 only**(其他层 fork 仍用 /fork)。
> 共享 /fork.md 的 Step 1-3(定位源/找候选/确认)和 Step 5-6(更新 fork log/输出菜单),只在 Step 4(PRD 生成)分化。

Parse `$ARGUMENTS` as: `<source-id> from-L3 <candidate-spec> as <new-id>`

## Step 1 — locate source stage doc (shared with /fork)

按 /fork.md Step 1 同样规则定位 `discussion/.../<source-id>/L3/stage-L3-scope-*.md`。
**强制 from-L3** — 如果 ARGUMENTS 不是 `from-L3`,报错并提示用 `/fork` 处理 L1/L2 fork。

## Step 2 — find the candidate (shared with /fork)

按 /fork.md Step 2 同规则,从 stage doc 里定位 candidate(支持 numeric / name match / ID)。

## Step 3 — confirm with human (shared with /fork)

显示同样的 confirmation 块(源 / 候选 / 新 ID / 路径),Y/N 确认。

## Step 3.5 — interactive: declare phases (NEW)

用 AskUserQuestion 询问 operator:

**Question 1**: 这个 PRD 有几个 phase?
- [2] v0.1 + v1.0(默认 — 一个 MVP + 一个商业化目标)
- [2'] v0.1 + v0.2(渐进迭代,无 v1.0 商业化目标)
- [3] v0.1 + v0.2 + v1.0(三阶段)
- [自定义] operator 输入数组,如 [v0.1, v0.5, v1.0]

**Question 2**(对每个 phase 重复): 该 phase 的核心范围是什么?(可选填,允许"待 v0.1 反馈后补")

记录 operator 答案到本地变量供 Step 4 使用。

## Step 4 — perform the fork (phased PRD generation)

### 4a. mkdir + write FORK-ORIGIN.md (shared with /fork)

按 /fork.md Step 4 同规则建目录、写 FORK-ORIGIN.md。FORK-ORIGIN.md `Selected candidate` 行后追加一行:`**PRD-form**: phased | Phases: [v0.1, v1.0]`(或 operator 选的)。

### 4b. write PRD.md using PRD-phased template

读 `.claude/skills/sdd-workflow/templates/PRD-phased.md` 作为骨架。**关键替换**:

- `**Phases**: [v0.1, v1.0]` → operator Step 3.5 Q1 的答案
- `**Phase-current**: v0.1` → 数组第一个 phase
- `### Scope IN — v0.1` / `### Scope IN — v1.0` → 按 phases 数组动态生成 N 个子节
  - v0.1 子节内容来自 candidate §"Scope IN" + intake hard constraints
  - v1.0(或后续 phases)子节内容初始为 candidate §"Natural extensions" 或 stage doc §"如果合体长什么样" — 如果都缺,留 `<待 v0.1 反馈后补>` 占位
- `## Scope OUT > 永久 OUT` → candidate §"Scope OUT" 抄过来
- `## Scope OUT > 当前 phase OUT` → 列 v0.1 不做但 v1.0 可能做的
- `## Phase transition learning` → 从 candidate §"Biggest risk" 和 stage doc §"Honesty check" 推断 1-3 条假设
- `## Core user stories` → 表格,Phase target 列按 candidate user stories 的 priority 分配
- `## Real-world constraints` → 表格,Phase scope 列分 v0.1/v1.0/both
- `## Success — observable outcomes` → v0.1 outcomes 来自 candidate §"Success looks like";v1.0 outcomes 留 `<subject to v0.1 learnings>`

写入 `discussion/.../<new-id>/PRD.md`。

## Step 5 — update source stage doc Fork log (shared with /fork)

追加 marker(同 /fork.md Step 5),但带 PRD-form 标签:

```markdown
## Fork log
- <ISO> · candidate #<X> forked as `<new-id>` (PRD-form: phased, phases: [v0.1, v1.0])
```

## Step 6 — output next-step menu

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Forked (phased): <new-id> created at discussion/.../<new-id>/

PRD-form: phased
Phases: [v0.1, v1.0]   ← operator declared
Phase-current: v0.1

Trace:
  proposals/proposals.md (entry <root>)
    → discussion/<root>/.../L3/stage-L3-scope-<source>.md (candidate #<X>)
      → discussion/<root>/.../<new-id>/PRD.md (phased)

📋 Next steps:

[1] Start L4 for <new-id> immediately (recommended)
    → /plan-start <new-id>
       (spec-writer will read PRD-form=phased, produce SLA.md / risks.md / spec.md
        with each declared phase as its own section.)

[2] Edit PRD.md to fill v1.0 Scope IN before plan-start
    → manually expand discussion/.../<new-id>/PRD.md §"Scope IN — v1.0"

[3] Add rationale to FORK-ORIGIN.md
    → tell me what to add and I'll write it

[4] I changed my mind — re-fork as simple instead
    → /fork <source> from-L3 <candidate> as <new-id>-alt

[5] Just stop
    → /status <new-id> anytime later

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Reply 1-5 or describe.
```

## Notes

- **phased 何时合理**:operator 已对 v1 形态有清晰想象,但选择先 ship v0.1 验证关键假设。当 phases 间假设关系强(v0.1 验证 X → v1 决定怎么做),用 phased 比 simple 优。
- **phased vs simple**:simple PRD 不预设 v1,需要时回 L3 重新 scope;phased 一开始就把 v1 写进 PRD,降低后期重 scope 的成本。代价是早期承诺更多。
- **phase 间转换**:目前是手动 — operator ship v0.1 → 跑 quality-gate → 决定启动 v1.0 build。后续可能加 `/phase-advance` 命令(本期未做)。
- **不允许 from-L1 / from-L2**:phased 需要 L3 candidate 的完整结构(user stories / scope / success)才能合理切 phase,L1/L2 的候选还没具体到这个粒度。
