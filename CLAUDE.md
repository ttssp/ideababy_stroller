# Idea Incubator — Project Constitution

This repo is a pipeline from *idea* to *production-grade software*, powered by a
single human operator and a team of AI agents (Claude Opus 4.7, GPT-5.4,
Sonnet 4.6, Codex 5.4, Haiku 4.5).

## Pipeline (6 phases, debate has 3 internal stages)
1. **Proposal** — idea captured in `proposals/proposals.md` as `**NNN**`
2. **Debate** — three stages in `discussion/NNN/`:
   - S1 Explore (opposing poles, ≥5 search sources/round, poles switch R2)
   - S2 Position (cooperative, produce 2–4 direction menu)
   - S3 Converge (engineering, only after moderator approves)
   - **Moderator decision gate at end of S2**: Advance / Fork / Park / Abandon
3. **Conclusion** — synthesizer produces `conc/NNN-*.md`
4. **Spec** — human-approved conclusion becomes `specs/NNN-*/`
5. **Build** — parallel workers in worktrees under `projects/NNN-*/`
6. **Ship** — 10-gate quality check before merge

Not every idea reaches Phase 3+. The Stage-2 gate is where we say "don't build" with evidence.

## Iron rules
- **No code without a spec.** A task without `specs/NNN-*/tasks/T<NNN>.md` does not execute.
- **Plan before change.** Any edit > 50 LOC starts in plan mode.
- **TDD for production code.** Tests first, fail, then implement, then green.
- **Small commits.** Conventional Commits. One logical change per commit.
- **Cross-model review is mandatory** for v1.0 paths: `/codex:review` then
  `/codex:adversarial-review` then `adversarial-reviewer` subagent.
- **Never modify `specs/`** files from a build worker. Only the operator + spec-writer touch specs.

## Tool preferences
- Search: `rg` (ripgrep), never raw `grep`
- JS/TS: `pnpm`, Node 22 LTS, TS strict mode, Biome for lint/format
- Python: `uv` for env + install, `ruff` for lint, `pytest` for test
- Go: standard toolchain, `golangci-lint`
- iOS: Xcode 16+, SwiftLint, XCTest
- Commits: Conventional Commits (feat / fix / chore / docs / refactor / test)
- CI: GitHub Actions; every PR runs G1–G5 automatically

## Directory ownership
- `proposals/` — operator writes, everyone else reads
- `discussion/NNN/` — only the assigned debater writes their rounds; moderator writes notes
- `conc/` — only `conclusion-synthesizer` writes; operator reviews
- `specs/NNN-*/` — only `spec-writer` and `task-decomposer` write
- `projects/NNN-*/` — `parallel-builder` workers (scoped to their task's `file_domain`)

## Prohibited
- Auto-generating `AGENTS.md` or `CLAUDE.md`
- Modifying `specs/` from a build worker
- Editing multiple tasks' `file_domain` in one worktree
- Committing `.env*` files (even if they look fake)
- Using `opus` model for boilerplate tasks (cost discipline)

## When things feel off
1. Ask the `debate-facilitator` subagent if a debate seems stuck
2. Run `/quality-gate NNN` to get a ground-truth status
3. `/clear` and restart from `specs/NNN-*/spec.md` if context feels polluted
4. If a task is blocked, write the blocker to the task file and stop — don't improvise

## Not in scope for this CLAUDE.md
- Per-project details (live in `projects/NNN-*/CLAUDE.md`)
- Personal preferences (live in `~/.claude/CLAUDE.md`)
- Path-scoped rules (live in `.claude/rules/*.md` with `paths:` frontmatter)