# Idea Incubator

A single-operator, AI-team pipeline from raw idea to commercial-grade software.

## How it works

```
┌──────────┐   ┌─────────┐   ┌───────────┐   ┌──────┐   ┌───────┐   ┌──────┐
│ Proposal │──▶│ Debate  │──▶│Conclusion │──▶│ Spec │──▶│ Build │──▶│ Ship │
│          │   │ Opus +  │   │ synthesis │   │ SDD  │   │ //    │   │ 10   │
│ 10 min   │   │ GPT-5.4 │   │ (Opus)    │   │      │   │ work  │   │ gates│
│          │   │ 3-5 rds │   │           │   │      │   │ trees │   │      │
└──────────┘   └─────────┘   └───────────┘   └──────┘   └───────┘   └──────┘
   You           2 AIs          1 AI         1 AI       N AIs      You+AIs
```

The pipeline is defined in [PLAYBOOK.md](./PLAYBOOK.md). Don't skip that file.

## Quick start

```bash
# 1. First-time setup (once per machine) — see PLAYBOOK.md §0
npm install -g @anthropic-ai/claude-code @openai/codex
brew install ripgrep tmux gh    # macOS
claude auth login
codex auth login

# 2. Inside Claude Code in this directory
claude
> /plugin marketplace add openai/codex-plugin-cc
> /plugin install codex@openai-codex

# 3. Drop an idea
> /propose
# (interactive — captures idea into proposals/proposals.md as **NNN**)

# 4. Debate it (run these in separate terminals)
# Terminal A (Claude Code) — Opus takes POSITIVE pole in S1R1
> /debate-start 001
# Terminal B (Codex) — GPT takes NEGATIVE pole; paste S1R1 kickoff from discussion/PROTOCOL.md
codex --model gpt-5.4 -c reasoning_effort=xhigh

# 5. Round 2 — POLES SWITCH. Both sides steelman the opposite.
# Terminal A:
> /debate-next 001 1 2
# Terminal B: paste S1R2 kickoff

# 6. Advance to Stage 2 when you've seen enough
> /debate-advance-stage 001 2
# stage1-synthesizer writes a synthesis doc; both sides then run S2 rounds (cooperative)
> /debate-next 001 2 1       # Opus S2R1
# Codex: paste S2R1 kickoff

# 7. Advance to Stage 3 — MODERATOR DECISION GATE
> /debate-advance-stage 001 3
# stage2-checkpoint presents a menu: Advance (pick direction) / Fork / Park / Abandon
# Record your choice in moderator-notes. Only if you chose Advance:
> /debate-next 001 3 1       # Opus S3R1 engineering mode
# Codex: paste S3R1 kickoff

# 8. Finalize and conclude
> /debate-finalize 001
# Terminal B: paste Finals kickoff
> /debate-conclude 001

# 9. Review conclusion; if approved, generate spec
> /spec-from-conclusion 001

# 10. Parallel build
> /parallel-kickoff 001 T003,T004,T008

# 11. Before merging
> /quality-gate 001
```

## Directory map

```
idea-incubator/
├── CLAUDE.md                    # Project constitution (loaded every session)
├── AGENTS.md → CLAUDE.md        # Symlink for Codex compatibility
├── PLAYBOOK.md                  # Full operator manual
├── README.md                    # You're here
├── .claude/
│   ├── settings.json            # Project-level Claude Code config
│   ├── commands/                # Slash commands
│   ├── agents/                  # Subagent definitions
│   ├── skills/                  # Reusable skill packages
│   └── rules/                   # Path-scoped rules (lazy-loaded)
├── .codex/
│   └── config.toml              # Codex project config
├── .worktreeinclude             # Files copied into each new worktree
├── .gitignore
│
├── proposals/
│   └── proposals.md             # Every idea lives here as **NNN**
│
├── discussion/
│   ├── PROTOCOL.md              # Debate rules template
│   └── NNN/                     # One folder per idea
│       ├── NNN-Opus47Max-R1.md
│       ├── NNN-GPT54xHigh-R1.md
│       ├── ... R2, R3 ...
│       ├── NNN-moderator-notes.md
│       └── NNN-*-final.md
│
├── conc/
│   └── NNN-Opus47Max-GPT54xHigh-byOpus47Max-YYMMDD.md
│
├── specs/
│   └── NNN-<project-name>/
│       ├── PRD.md
│       ├── spec.md              # The 6-element contract
│       ├── architecture.md
│       ├── tech-stack.md
│       ├── SLA.md
│       ├── risks.md
│       ├── non-goals.md
│       ├── dependency-graph.mmd
│       └── tasks/
│           ├── T001.md … TNNN.md
│
└── projects/
    └── NNN-<project-name>/      # Real code — usually a git submodule
```

## One-page cheat sheet

| Command | Use when |
|---|---|
| `/propose` | Starting a new idea |
| `/debate-start <NNN>` | Launching Opus's S1R1 (POSITIVE pole) |
| `/debate-next <NNN> <stage> <round>` | Opus's next round. Pole auto-switches at S1R2. |
| `/debate-advance-stage <NNN> <target>` | Move from S1→S2 or S2→S3. S2→S3 is a moderator decision gate. |
| `/debate-inject <NNN> <tag>` | Inject a constraint/question both sides must address |
| `/debate-finalize <NNN>` | Opus writes its standalone final |
| `/debate-conclude <NNN>` | Synthesize the full debate |
| `/spec-from-conclusion <NNN>` | Turn conclusion into SDD package |
| `/parallel-kickoff <NNN> <task-ids>` | Prep worktrees for parallel build |
| `/quality-gate <NNN>` | Pre-ship check (10 gates) |
| `/codex:review` | Quick Codex review of diff |
| `/codex:adversarial-review` | Hostile Codex review with focus text |
| `/codex:rescue` | Hand a stuck task to Codex |

## Subagents available

| Agent | Purpose | Model |
|---|---|---|
| `stage1-synthesizer` | Digest Stage 1 rounds before S2 starts | Opus |
| `stage2-checkpoint` | Build moderator decision doc after S2 | Opus |
| `conclusion-synthesizer` | Fold full debate into conclusion doc | Opus |
| `spec-writer` | Build SDD package from conclusion | Opus |
| `task-decomposer` | Spec → task DAG | Opus |
| `parallel-builder` | Execute one task in own worktree | Sonnet |
| `security-auditor` | OWASP audit | Opus (effort: high) |
| `adversarial-reviewer` | 3-persona hostile review | Opus (effort: high) |
| `code-reviewer` | Constructive PR review | Sonnet |
| `debate-facilitator` | Meta-observer of ongoing debate | Opus |

## Philosophy

- Specs are the only thing that turns multi-model output into production software
- Two AI debaters find 3x the issues one does
- Worktrees are the only way to run 5 AIs without stepping on each other
- Commercial quality comes from adversarial review loops, not clever prompts
- The operator's time is best spent on spec review, debate moderation, and user
  research — not writing code
