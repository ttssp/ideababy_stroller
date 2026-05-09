# Idea Incubator — Project Constitution

This repo is a **tree** from raw idea to shipped software. Powered by a single
human operator and a team of AI agents (Claude Opus 4.7, GPT-5.4 xhigh,
Sonnet 4.6, Codex 5.3/5.4, Haiku 4.5).

## The 4-layer pipeline (each layer can fork)

```
Proposal (one-paragraph seed)
  │
  ▼
L1 · Inspire   — daydream N inspired directions, value/novelty/utility only
  │  output: stage-L1-inspire.md (menu of directions)
  │  fork: human selects 1+ directions → 001a, 001b, ...
  ▼
L2 · Explore   — deep unpack of one chosen idea, still no tech
  │  output: stage-L2-explore-<fork>.md (rich essay about the idea)
  │  fork: optional sharper cuts of the same idea
  ▼
L3 · Scope     — real requirements, what to build, what NOT to build
  │  output: PRD-v<n>.md (real product requirements with human's constraints)
  │  fork: different PRD interpretations
  ▼
L4 · Hand-off  — produce hand-off package; downstream build runtime (XenoDev) does spec/tasks/build/quality
  │  output: HANDOFF.md → XenoDev consumes (per framework/SHARED-CONTRACT.md §6 v2.0)
```

Every layer's output is **independently valuable**. An L1 inspire menu may stay
useful for years even if no fork is ever built. An L2 deep dive captures a way
of thinking that's worth keeping. Park is normal; Abandon comes with a lesson doc.

## Iron rules

- **Layer discipline**: L1/L2 NEVER discuss tech/feasibility/cost. L3 brings in
  human's real constraints. L4 is engineering. Don't mix.
- **PRD is source of truth after L3**: L4 agents (spec-writer) read PRD but
  don't alter product decisions. If PRD has issues, escalate to human.
- **No code without a spec**: a task without `specs/.../tasks/T<NNN>.md` does
  not execute. (L4 only.)
- **TDD for production code** (L4): tests first, fail, then implement, then green.
- **Pre-merge review mandatory** (L4 build): every parallel-builder worktree
  MUST pass `/task-review <fork> T<NNN>` with verdict ≠ BLOCK before merging.
  Reviewer mode is operator's choice (`claude-light` / `claude-full` / `codex`
  / `mixed`). See `.claude/commands/task-review.md`.
- **Cross-model review mandatory** for v1.0 paths (L4 quality gate).
- **Specs are immutable from build workers** — only operator + spec-writer touch them.
- **Every command outputs a next-step menu** — human never has to guess what's next.
- **"Not sure" is a first-class answer in L3R0 intake** — models must offer
  options for ❓ items, not pressure human to decide.
- output in Chinese

## Codex inbox/outbox bus (v2 · 多队列)

Cross-agent coordination uses `.codex-inbox/queues/<id>/` 和
`.codex-outbox/queues/<id>/`，每个 idea / fork-id 一个独立队列（见
`.codex-inbox/README.md`）。human 在 Codex 终端运行：

```
cdx-run <queue-id>      # 例：cdx-run 003-pA
cdx-queues              # 看所有队列与 HEAD 状态
```

旧的单一 `latest.md` symlink 在 v2 已废弃 —— 多 idea 并行/多 worktree 不再冲突。

## Tool preferences

- Search: `rg` (ripgrep), never raw `grep`
- JS/TS: `pnpm`, Node 22 LTS, TS strict, Biome
- Python: `uv` for env+install, `ruff`, `pytest`
- Go: standard toolchain, `golangci-lint`
- iOS: Xcode 16+, SwiftLint, XCTest
- Commits: Conventional Commits

## Directory ownership

- `proposals/proposals.md` — operator writes (one-paragraph seed minimum)
- `discussion/NNN/L1/` — inspire layer; only the layer's commands write here
- `discussion/NNN/<fork-id>/L2/` — explore layer per fork
- `discussion/NNN/<fork-id>/L3/` — scope layer per fork
- `discussion/NNN/<fork-id>/<prd-version>/L4/` — plan layer per PRD version
- `discussion/NNN/<fork-id>/<prd-version>/L4/HANDOFF.md` — produced by `/plan-start` (v3.0+, M2 cutover);XenoDev build runtime consumes
- `specs/NNN-<fork-id>-<prd>/` — **DEPRECATED M3** (commit d3194a0):4 fork specs/ archived as forge v2 evidence;IDS no longer produces specs/(see SHARED-CONTRACT §6 v2.0)
- `projects/NNN-<fork-id>/` — historical parallel-builder worktrees (pre-M2);new builds happen in XenoDev repo
- `.codex-inbox/`, `.codex-outbox/` — agent coordination bus

## Prohibited

- L1/L2 emitting tech/feasibility content (re-route to L4)
- Auto-generating `AGENTS.md` or `CLAUDE.md` (LLM-generated context hurts quality)
- Modifying `specs/` at all (M3 verdict 2026-05-10 commit d3194a0: 4 fork specs/ archived as forge v2 evidence;no further task additions / reviews)
- Committing `.env*` files
- Forking >3 levels deep without strong reason

## When things feel off

1. `/status NNN` to see ground-truth state of any tree
2. `/clear` and restart from a stage doc if context feels polluted
3. If a layer keeps drifting into the wrong content (L2 doing tech), re-read the
   layer's protocol skill and consider injecting a moderator note

## Not in scope for this CLAUDE.md

- Per-project details (`projects/<fork-id>/CLAUDE.md`)
- Personal preferences (`~/.claude/CLAUDE.md`)
- Path-scoped rules (`.claude/rules/*.md` with `paths:` frontmatter)
