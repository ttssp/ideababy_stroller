---
description: Fork an idea (or any sub-tree) into a new branch from any layer's stage document. Supports both "just-completed" forks and "historical retrospective" forks (revisit a past decision and try a different candidate).
argument-hint: "<source> from-L<n> <candidate-spec> as <new-id>  e.g. 001 from-L1 direction-3 as 001a"
allowed-tools: Read, Write, Bash(mkdir:*), Bash(cp:*), Bash(ls:*), Bash(date:*), Glob, Grep
model: sonnet
---

# Fork · branch off a candidate from any layer

Parse `$ARGUMENTS` as: `<source-id> from-L<n> <candidate-spec> as <new-id>`

Examples:
- `001 from-L1 direction-3 as 001a`  → fork 001's L1 candidate #3 into 001a
- `001 from-L1 "real-time whiteboard" as 001whiteboard`  → fork by name match
- `001a from-L3 PRD-candidate-2 as 001a-pv2`  → from a sub-tree's L3 layer
- `001 from-L1 direction-7 as 001g`  → historical retrospective (e.g. weeks later)

## Step 1 — locate the source stage document

The source layer's synthesis document must exist. Look for:
```
discussion/<source-id>/.../L<n>/stage-L<n>-*.md
```

If `<source-id>` is `001`, the path is `discussion/001/L<n>/stage-L<n>-*.md`.
If `<source-id>` is `001a`, the path is `discussion/001/001a/L<n>/stage-L<n>-*.md`.
(General rule: replace dashes/dots with `/` to walk into nested forks.)

If the stage doc doesn't exist, **stop** and tell human:
> "Cannot fork: <source-id> hasn't completed L<n> yet (no stage-L<n>-*.md found).
> Run `/status <source-id>` to see what's needed first."

## Step 2 — find the candidate inside the stage document

The candidate spec can be:
- Numeric: `direction-3` → look for the 3rd entry in the menu/candidate list
- Name match: `"real-time whiteboard"` → grep candidate titles
- ID: `PRD-candidate-2` → exact match on candidate ID

If ambiguous or not found, **stop** and show a list:
> "Candidates available in <source>'s L<n>:
>   1. <name>
>   2. <name>
>   ...
> Re-run with: /fork <source> from-L<n> <number-or-exact-name> as <new-id>"

## Step 3 — confirm with human (single Y/N)

Show what you're about to do:

```
About to fork:
  Source:    discussion/001/L1/stage-L1-inspire.md
  Candidate: #3 "Real-time collaborative whiteboard for educators"
  New id:    001a
  Path:      discussion/001/001a/

This will:
  - create discussion/001/001a/
  - write FORK-ORIGIN.md tracing back to source
  - copy proposal context from proposals/proposals.md entry 001
  - augment with the candidate description as the new starting point

Proceed? [y/N]
```

If human says no, stop.

## Step 4 — perform the fork

```bash
mkdir -p discussion/<parent-of-new-id>/<new-id>
```

Write `discussion/.../<new-id>/FORK-ORIGIN.md`:

```markdown
# Fork origin

**This fork**: <new-id>
**Forked from**: <source-id> · L<n>
**Source stage doc**: <relative path to stage-L<n>-*.md>
**Selected candidate**: <candidate name verbatim from source>
**Candidate description (extracted from source)**:

<copy the relevant section from the stage doc here, max ~300 words, as the
starting context for this fork — paraphrased, not verbatim if >15 words at a stretch>

**Forked at**: <ISO timestamp>
**Forked by**: human moderator (via /fork command)
**Rationale** (optional, human can fill in):

[ ___________________________________________________ ]

---

## What this fork is for

Now `<new-id>` is its own independent sub-tree. The next layer (L<n+1>) will
operate on the candidate above as if it were a fresh proposal. Run:

  /<next-layer-cmd>-start <new-id>

(e.g. /explore-start 001a if forking from L1, /plan-start 001a-pA if forking from L3)

## Sibling forks (for cross-reference)

<auto-list other forks from the same source's L<n>, e.g.:>
- 001a (this one) — direction #3
- 001b — direction #5 (in L2 already)
- 001c — direction #7 (parked)
```

### Special case: fork from L3 → also write PRD.md

If the source layer is **L3** (from `from-L3 ...`), also produce a full PRD.md
for the new fork by extracting the candidate section.

**重要 (历史教训)**: PRD §5 和 §6 必须分开 — §5 是 "Scope OUT (永远不做)"
红线级别非目标, §6 是 "Phased roadmap (committed, 按阶段)" 承诺序列。
两者对 v0.1 架构的影响完全相反:
- Scope OUT → v0.1 不留扩展点 (留了诱发越界)
- Phased roadmap → v0.1 必须留扩展点 (避免 v0.2+ 起步重写)

历史 idea004 fork 早期版本把 L2 §4 "Natural extensions" 压扁进 Scope OUT,
导致下游混乱。新协议强制分离, 详见 `.claude/skills/scope-protocol/SKILL.md`
"Scope OUT vs Phased roadmap — 为什么拆开" 节。

Write `discussion/.../<new-id>/PRD.md`:

```markdown
# PRD · <new-id> · "<candidate title>"

**Version**: 1.0  (human-approved via fork)
**Created**: <ISO>
**Source**: discussion/.../<source>/L3/stage-L3-scope-<source>.md · Candidate <X>
**Approved by**: human moderator

## Problem / Context
(From the candidate's v0.1-in-one-paragraph, expanded with L2 context as needed)

## Users
(From the candidate's "User persona" section, expanded with L2 personas)

## Core user stories
(From the candidate's user stories — one per story, numbered)

## Scope IN (v0.1)
(From the candidate's "Scope IN" — as-is)

## Scope OUT (永远不做 — red-line / 永久排除)
**ONLY** copy candidate's red-line non-goals here (项目身份冲突 / 永远不做的项).
**DO NOT** copy phased roadmap items here (those go to next section).
例: 自动下单 / 商业化 / 期权高杠杆 / 信息壳赛道 (跨 candidate identity).

- <hard non-goal>, because <invariant reason>
- ...

## Phased roadmap (全部 committed, 按阶段交付)

**Source**: From candidate's "Phased roadmap" section (which itself inherits
from L2 §4 "Natural extensions"). 必须保留每条的:
- 阶段归属 (v0.2 / v0.5 / v1.0 / v1.5+)
- 难度 + 重要性标签
- 对应解决的 L2 风险编号

**写作约定 (强制)**:
- **v0.2 (NEXT)**: 详细描述 (做什么 / 完成标准 / v0.1 已留位)
- **v0.5 / v1.0 / v1.5+**: 一行概要

**Maintenance hint** (添加到本节末尾):
> 每次 ship 后 PRD 维护: 把已完成阶段从 roadmap 删除, 把"下一阶段"从概要升级
> 成详细描述。这是 PRD 持续演进, 不是一次写死。

### Phase v0.2 (NEXT — 详细)

#### v0.2.1 <feature name>
[难度 L/M/H, 重要性 L/M/H] — 对应解决: L2 §4 风险 #<n>

**v0.2 做什么**: <2-4 句>
**完成标准**: <2-3 条 measurable>
**v0.1 已留位**: <接口/扩展点位置>

#### v0.2.2 ...

### Phase v0.5 (3-9 个月 — 概要)
- <feature> [难度 X, 重要性 Y] — 对应解决: L2 §4 风险 #<n>
- ... [v0.2 ship 后细化]

### Phase v1.0 (9-18 个月 — 概要)
- ...

### Phase v1.5+ (远期 — 概要)
- ...

## Success — observable outcomes
(From the candidate's "Success looks like" — as-is, numbered O1/O2/...)

## Real-world constraints
(Drawn from L3R0-intake ✅ hard constraints + the candidate's time/platform/etc.)

| # | Constraint | Source |
|---|------------|--------|
| C1 | <time budget> | L3R0 intake Block 1 |
| C2 | <platform> | L3R0 intake Block 4 |
| C3 | <business model implication> | L3R0 intake Block 3 |
| C4 | <red line> | L3R0 intake Block 5 |

## UX principles (tradeoff stances)
(From the candidate's "UX priorities" — as-is)

## Biggest product risk
(From the candidate's "Biggest risk" — as-is)

## Open questions for L4 / Operator
(Any ❓ items from L3 that survived unresolved. These block build if critical.)

---

## PRD Source
This PRD was auto-generated from L3 fork. Contents are derived from the
approved L3 candidate. For full context (why this cut vs siblings, scope-
reality verdict, comparison matrix), see:

- L3 menu: discussion/.../<source>/L3/stage-L3-scope-<source>.md
- L2 unpack: discussion/.../<source>/L2/stage-L2-explore-<source>.md
- FORK-ORIGIN.md in this directory

This PRD is the **source of truth** for L4 (spec-writer). Changes to PRD
require explicit human approval — never auto-revised by L4 agents.
```

## Step 5 — update the source stage doc

Append a marker to the source `stage-L<n>-*.md`:

```markdown

---

## Fork log
- <ISO> · candidate #3 forked as `<new-id>` (status: just-created)
```

(If a "Fork log" section already exists, append to it. This way, the source doc
serves as a directory of all spawned forks.)

## Step 6 — output the next-step menu

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Forked: <new-id> created at discussion/.../<new-id>/

Trace:
  proposals/proposals.md (entry <root>)
    → discussion/<root>/L1/stage-L1-inspire.md (candidate #3)
      → discussion/<root>/<new-id>/

📋 Next steps:

[1] Start L<n+1> for <new-id> immediately (recommended)
    → /<next-layer-cmd>-start <new-id>
       e.g. /explore-start 001a if you forked from L1

[2] Add rationale or a constraint to FORK-ORIGIN.md before starting next layer
    → tell me what to add and I'll write it

[3] Fork another candidate from same source while you're at it
    → /fork <source> from-L<n> <other-candidate> as <other-new-id>

[4] Just create the fork and stop (start next layer later)
    → done; come back anytime with /status <new-id>

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Reply 1/2/3/4 or describe what you want.
```

## Notes

- **Historical retrospective forks**: this command works the same whether the
  source layer was completed 5 minutes ago or 5 weeks ago. The stage doc is the
  source of truth.
- **Naming conventions** for `<new-id>`: free-form. Conventions that work well:
  - `<root><letter>` — 001a, 001b, 001c (default)
  - `<root>-<short-name>` — 001-whiteboard, 001-quiz
  - `<root>-pv<n>` — 001a-pv2 (different PRD versions)
- Forks preserve full lineage; you can fork forks of forks. Don't go more than
  3 levels deep without strong reason — the tree gets unmanageable.
