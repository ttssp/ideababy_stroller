# Idea Incubator · v3.0

A single-operator, AI-team pipeline from raw idea to commercial-grade software.

## Core philosophy

Your idea is a **seed**. The pipeline is a **tree** that branches at every layer.
Every branch (fork) is a sibling, not nested. Every layer's output is
independently valuable — even ideas that get parked or abandoned leave behind
exploration documents worth keeping.

## The four layers

| Layer | Discusses | Search? | Human density |
|---|---|---|---|
| **L1 Inspire** | What inspired directions does this seed grow? Value, novelty, utility — NO tech | Value-validation only (in R2) | Low (let models fly) |
| **L2 Explore** | One chosen idea, deeply: novelty, utility, extensions, limits | Value-validation only (in R2) | Medium (give signals) |
| **L3 Scope** | Real requirements, what to build, what NOT to build | Free | High (your real needs) |
| **L4 Plan** | Spec, architecture, tasks, build, ship | Free | Medium (approve key calls) |

## Quick start

```bash
# 1. Setup (once)
mkdir my-incubator && cd my-incubator
tar xzf ~/Downloads/idea-incubator-v3.0-stage1.tar.gz
bash install.sh
bash scripts/codex-inbox-init.sh

# 2. Configure Codex alias (once, in ~/.zshrc or ~/.bashrc)
alias cdx-run='codex "read .codex-inbox/latest.md and execute exactly what it says, then write a corresponding .codex-outbox/<same-filename>.md confirming what you did"'
source ~/.zshrc

# 3. Drop an idea (one paragraph minimum)
claude
> /propose

# 4. L1 Inspire — let models break your cognitive limits
> /inspire-start 001
# (you'll see a menu when Opus done; choose [1] to send Codex)
# in Codex terminal:  cdx-run
# back in Claude Code:
> /inspire-next 001
# in Codex terminal:  cdx-run
> /inspire-advance 001
# read the L1 menu; pick a direction:
> /fork 001 from-L1 direction-3 as 001a

# 5. L2 Explore — deep unpack the chosen direction
> /explore-start 001a
# in Codex terminal:  cdx-run
> /explore-next 001a
# in Codex terminal:  cdx-run
> /explore-advance 001a
# read the explore report; if good:
> /scope-start 001a       # (L3 — coming in v3.0-stage2)
```

## Anywhere in the flow

```bash
> /status                  # see all ideas + active forks
> /status 001              # see this idea's full tree
> /status 001a             # see one fork's state
> /fork 001 from-L1 direction-7 as 001b   # historical retrospective fork
> /park 001a               # preserve, decide later
```

## Command reference (v3.0-stage1)

### Pipeline commands (per layer)
| Command | When |
|---|---|
| `/propose` | Drop a one-paragraph idea seed |
| `/inspire-start <NNN> [--mode=full\|narrow\|skip]` | Start L1 R1 (Daydream, no search) |
| `/inspire-next <NNN>` | L1 R2 (cross-read + value-validation search) |
| `/inspire-advance <NNN>` | Close L1, produce inspired menu |
| `/explore-start <fork-id>` | Start L2 R1 (Daydream, no search) |
| `/explore-next <fork-id>` | L2 R2 (cross-read + value-validation search) |
| `/explore-advance <fork-id>` | Close L2, produce explore report |
| `/scope-start <fork-id>` | Start L3 (coming in v3.0-stage2) |
| `/plan-start <fork-id>` | Start L4 (coming in v3.0-stage2; uses preserved v2.1 SDD assets) |

### Tree management
| Command | When |
|---|---|
| `/fork <src> from-L<n> <candidate> as <new-id>` | Branch any layer's stage doc, anytime (incl. retrospective) |
| `/status [<id>]` | See full tree state + suggested next step |
| `/park <id>` | Preserve, set revival condition |
| `/abandon <id>` | Close out, write lesson doc (coming in v3.0-stage2) |

## Decision-menu UX

Every command ends with a numbered menu. Reply with a digit or free text.

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ <what just happened>
   <key facts in 2-4 lines>

📋 Next steps:

[1] <most likely action — usually "send Codex via inbox">
[2] <second option — usually "inject a note">
[3] <show me what was just written>
[4] <fork or branch>
[5] <park or stop>

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Reply 1-5 or describe.
```

## Codex inbox/outbox

You **never copy-paste a long prompt** between terminals. Claude Code writes a
self-contained task to `.codex-inbox/latest.md`; you run `cdx-run` in Codex;
Codex reads the file, executes, writes confirmation to `.codex-outbox/`. See
`.codex-inbox/README.md` for full details.

## Directory structure

```
my-incubator/
├── CLAUDE.md                    # constitution
├── PLAYBOOK.md                  # operator manual (full design rationale)
├── README.md                    # you're here
│
├── .claude/
│   ├── settings.json
│   ├── commands/                # slash commands (see table above)
│   ├── agents/                  # subagents (inspire-synthesizer, explore-synthesizer, ...)
│   ├── skills/                  # protocol skills (inspire-protocol, explore-protocol, ...)
│   └── rules/                   # path-scoped rules
│
├── .codex-inbox/                # Claude→Codex tasks (cdx-run reads latest.md)
├── .codex-outbox/               # Codex→Claude confirmations
├── .codex/config.toml           # Codex project config
│
├── proposals/proposals.md       # idea seeds (one-paragraph minimum)
│
└── discussion/                  # the tree
    └── 001/                     # idea root
        ├── L1/                  # Inspire layer
        │   ├── L1R1-Opus47Max.md
        │   ├── L1R1-GPT54xHigh.md
        │   ├── L1R2-*.md
        │   ├── L1-moderator-notes.md
        │   └── stage-L1-inspire.md       # the inspired menu
        │
        ├── 001a/                # forked from L1 #3
        │   ├── FORK-ORIGIN.md   # lineage
        │   └── L2/
        │       ├── L2R1-*.md
        │       ├── L2R2-*.md
        │       └── stage-L2-explore-001a.md
        │
        ├── 001b/                # forked from L1 #5 (parallel sibling)
        │   └── ...
        │
        └── 001c/                # forked retrospectively, weeks later
            └── ...
```

## What's in v3.0-stage1 vs stage2

**stage1 (this release)**:
- L1 Inspire: full + narrow + skip modes
- L2 Explore
- Tree management: status / fork / park
- Codex inbox/outbox bus
- Updated proposal template (one-paragraph minimum)

**stage2 (next release)**:
- L3 Scope (with `scope-protocol` skill, `/scope-*` commands, `scope-synthesizer`)
- L4 entry glue (connects L3 PRD output to preserved v2.1 SDD assets:
  spec-writer, task-decomposer, parallel-builder, code-reviewer,
  adversarial-reviewer, security-auditor, quality-gate)
- `/abandon` command
- Full PLAYBOOK.md rewrite for 4-layer model

If you need L3/L4 today, the v2.1 commands (`/debate-*`, `/spec-from-conclusion`,
`/parallel-kickoff`, `/quality-gate`) still work and are preserved in this package.
You can use v3.0's L1+L2 to land on a clear PRD-equivalent, then drop into
v2.1's flow for spec→build→ship until v3.0-stage2 ships proper L3+L4 commands.

## Apps that complement this workflow

- Claude Code (this repo's home)
- Codex CLI (the second-debater terminal)
- Optional: Claude Desktop (for reading long stage docs in a nice UI)
