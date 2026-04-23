# Idea Incubator — Project Constitution

This repo is a **tree** from raw idea to shipped software. Powered by a single
human operator and a team of AI agents (Codex Opus 4.7, GPT-5.4 xhigh,
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
L4 · Plan      — spec, architecture, tasks, parallel build, quality gates
  │  output: working code + ship
```

Every layer's output is **independently valuable**. An L1 inspire menu may stay
useful for years even if no fork is ever built. An L2 deep dive captures a way
of thinking that's worth keeping. Park is normal; Abandon comes with a lesson doc.

## Iron rules

- **Layer discipline**: L1/L2 NEVER discuss tech/feasibility/cost. L3 brings in
  human's real constraints. L4 is engineering. Don't mix.
- **No code without a spec**: a task without `specs/.../tasks/T<NNN>.md` does
  not execute. (L4 only.)
- **TDD for production code** (L4): tests first, fail, then implement, then green.
- **Cross-model review mandatory** for v1.0 paths (L4 quality gate).
- **Specs are immutable from build workers** — only operator + spec-writer touch them.
- **Every command outputs a next-step menu** — human never has to guess what's next.
- output in Chinese

## Codex inbox/outbox bus

Cross-agent coordination uses `.codex-inbox/` and `.codex-outbox/` (see
`.codex-inbox/README.md`). human runs `cdx-run` in Codex terminal — no
copy-pasting kickoffs needed.

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
- `specs/NNN-<fork-id>-<prd>/` — only spec-writer + task-decomposer write
- `projects/NNN-<fork-id>/` — parallel-builder workers (scoped to task file_domain)
- `.codex-inbox/`, `.codex-outbox/` — agent coordination bus

## Prohibited

- L1/L2 emitting tech/feasibility content (re-route to L4)
- Auto-generating `AGENTS.md` or `AGENTS.md` (LLM-generated context hurts quality)
- Modifying `specs/` from a build worker
- Committing `.env*` files
- Forking >3 levels deep without strong reason

## When things feel off

1. `/status NNN` to see ground-truth state of any tree
2. `/clear` and restart from a stage doc if context feels polluted
3. If a layer keeps drifting into the wrong content (L2 doing tech), re-read the
   layer's protocol skill and consider injecting a moderator note

## Not in scope for this AGENTS.md

- Per-project details (`projects/<fork-id>/AGENTS.md`)
- Personal preferences (`~/.Codex/AGENTS.md`)
- Path-scoped rules (`.Codex/rules/*.md` with `paths:` frontmatter)
