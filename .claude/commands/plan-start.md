---
description: Start L4 Plan phase for a forked PRD branch. Reads the chosen PRD.md, invokes spec-writer to produce the SDD package, runs task-decomposer, then triggers Codex adversarial review loop (up to 4 rounds). Output is a build-ready spec package.
argument-hint: "<prd-fork-id>  e.g. 001a-pA"
allowed-tools: Read, Write, Bash(mkdir:*), Bash(cp:*), Bash(ln:*), Bash(ls:*), Bash(date:*), Agent(spec-writer), Agent(task-decomposer), Glob, Grep
model: opus
---

# Plan · L4 entry — from PRD to spec + task DAG

PRD branch **$ARGUMENTS** (e.g. `001a-pA`).

## Step 1 — locate the PRD

The PRD was produced by `/fork ... from-L3 candidate-X as <prd-fork-id>`.
The fork's `FORK-ORIGIN.md` references the L3 stage doc and the chosen candidate.

Expected layout:
```
discussion/<root>/<parent-fork>/<prd-fork-id>/
  ├─ FORK-ORIGIN.md
  └─ PRD.md    ← generated at fork time from the L3 candidate
```

If `PRD.md` doesn't exist, construct it now from FORK-ORIGIN.md's candidate
description (fork should have extracted the full candidate). If the fork
was done before this command existed (edge case), run:

```
I notice PRD.md isn't at the expected location. I'll synthesize one from
FORK-ORIGIN.md + the L3 stage doc now. OK?
```

## Step 2 — read all context

1. `discussion/<root>/<parent-fork>/<prd-fork-id>/PRD.md` — the chosen PRD
2. `discussion/<root>/<parent-fork>/<prd-fork-id>/FORK-ORIGIN.md` — lineage
3. `discussion/<root>/<parent-fork>/L3/stage-L3-scope-<parent-fork>.md` — full menu context
4. `discussion/<root>/<parent-fork>/L2/stage-L2-explore-<parent-fork>.md` — idea context
5. `CLAUDE.md`
6. `.claude/skills/sdd-workflow/SKILL.md`

## Step 3 — decide spec package location

```
specs/<prd-fork-id>/    e.g. specs/001a-pA/
```

Create:
```bash
mkdir -p specs/<prd-fork-id>/tasks
```

## Step 4 — invoke spec-writer

Delegate to `spec-writer` subagent:

> "Use spec-writer to produce a complete SDD package in `specs/<prd-fork-id>/`
>  from the PRD at `discussion/.../<prd-fork-id>/PRD.md`.
>
>  Context to read:
>  - The PRD (source of truth for outcomes, scope, constraints)
>  - L3 stage doc for the menu context (why this cut was chosen vs siblings)
>  - L2 stage doc for the idea texture
>  - CLAUDE.md
>  - sdd-workflow skill
>
>  Produce:
>  - spec.md (6-element contract — use PRD outcomes as §1, PRD scope as §2,
>    PRD constraints as §3, synthesize §4 'prior decisions' from L2/L3 lineage,
>    §5 task breakdown skeleton, §6 verification criteria)
>  - architecture.md
>  - tech-stack.md (pinned versions with rationale)
>  - SLA.md (phased: v0.1 and v1.0)
>  - risks.md (technical, operational, security, commercial, bus-factor)
>  - non-goals.md (explicit from PRD scope OUT)
>  - compliance.md (if applicable — flag if PRD implies regulatory concerns)
>
>  DO NOT yet create tasks/ — that's the next step (task-decomposer).
>  DO NOT start implementation — that's parallel-builder later."

Wait for spec-writer to complete.

## Step 5 — invoke task-decomposer

Delegate to `task-decomposer`:

> "Use task-decomposer to break spec.md into tasks/T001.md ... T<NNN>.md and
>  produce dependency-graph.mmd.
>
>  Source: specs/<prd-fork-id>/spec.md
>  Plus: architecture.md, tech-stack.md for file_domain decisions.
>  Target dir: specs/<prd-fork-id>/tasks/
>
>  Produce 10-30 tasks with phase labels (Phase 0/1/2/3). Apply model routing
>  heuristics from task-decomposer-skill (recommended_model per task).
>
>  Output distribution health report at end."

Wait for completion.

## Step 6 — prepare Codex adversarial review

Write `.codex-inbox/<TS>-<prd-fork-id>-L4-adversarial-r1.md`:

```markdown
# Codex Task · <prd-fork-id> · L4 Adversarial Review Round 1

**Created**: <ISO>
**Recommended model**: gpt-5.4
**Recommended reasoning_effort**: xhigh
**Estimated tokens**: ~15-25k

## Your role
You are GPT-5.4 xhigh performing adversarial review on a just-generated spec
package. Your goal: find where this spec will fail in production.

## Read
- specs/<prd-fork-id>/spec.md  (6-element contract)
- specs/<prd-fork-id>/architecture.md
- specs/<prd-fork-id>/tech-stack.md
- specs/<prd-fork-id>/SLA.md
- specs/<prd-fork-id>/risks.md
- specs/<prd-fork-id>/non-goals.md
- specs/<prd-fork-id>/tasks/T*.md (sample 3-5)
- specs/<prd-fork-id>/dependency-graph.mmd
- discussion/.../PRD.md (to verify spec is faithful)

## Challenge these specifically
1. **Concurrency safety** — what breaks at 10x traffic?
2. **Data consistency** — where can state corrupt under concurrent writes?
3. **Failure recovery** — what happens when upstream X goes down for 30 minutes?
4. **Security boundaries** — where is trust crossed without verification?
5. **Operational cost at scale** — does the architecture stay affordable at 10x load?
6. **PRD faithfulness** — does the spec actually deliver every PRD outcome?
7. **Non-goal leakage** — does the spec accidentally include things PRD excludes?
8. **Task DAG sanity** — any cycles, unreachable tasks, or overly-wide dependencies?
9. **Solo-operator viability** — can one human with AI agents actually execute this?

## Write
.codex-outbox/<TS>-<prd-fork-id>-L4-adversarial-r1.md with:

```markdown
# Adversarial Review · <prd-fork-id> · R1

## Blockers (must fix before proceeding)
| # | Location | Issue | Why it blocks | Fix direction |

## High-severity concerns (should fix; ok as follow-up with owner+deadline)
| # | Location | Issue | Suggested action |

## Medium / Low findings
(brief list)

## PRD faithfulness check
- [ ] Every PRD outcome has corresponding spec verification
- [ ] No spec feature outside PRD scope IN
- [ ] No spec feature in PRD scope OUT

## Top 3 things the operator personally must verify (human judgment required)
1. ...

## Verdict
One of:
- CLEAN (no blockers, optionally minor fixes) — spec ready to build
- CONCERNS (non-blocking; operator decides whether to fix now or ship with risk log)
- BLOCK (must fix before round 2)
```

Quote ≤15 words verbatim from any file.
```

Update symlink:
```bash
cd .codex-inbox && ln -sf <TS>-<prd-fork-id>-L4-adversarial-r1.md latest.md
```

## Step 7 — output next-step menu

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ L4 Plan started for <prd-fork-id>.

Generated:
  specs/<prd-fork-id>/
    ├─ spec.md           (6-element contract)
    ├─ architecture.md
    ├─ tech-stack.md
    ├─ SLA.md
    ├─ risks.md          (<n> entries)
    ├─ non-goals.md
    ├─ compliance.md     [if applicable]
    ├─ dependency-graph.mmd
    └─ tasks/T001..T<NNN>.md  (<n> tasks across <k> phases)

Task distribution health: <from decomposer>
  Opus:   X%
  Sonnet: Y%
  Codex:  Z%
  Haiku:  W%
  (target: Opus 10-15%, Sonnet 55-70%, Codex 10-15%, Haiku 5-10%)

📋 Next step: Codex adversarial review R1

[1] Run Codex adversarial review (recommended)
    → in your Codex terminal: cdx-run
    (Codex reviews spec + tasks, writes blockers/concerns to outbox)

[2] Show Codex kickoff for manual paste
    → I'll display .codex-inbox/latest.md

[3] Show me the spec first
    → I'll display specs/<prd-fork-id>/spec.md

[4] Show me the task list first
    → I'll display specs/<prd-fork-id>/dependency-graph.mmd

[5] Review the task distribution
    → I'll display model assignments summary

[6] Pause — I want to read everything before adversarial review
    → run /status <prd-fork-id> to see state when ready

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Reply 1/2/3/4/5/6 or describe.
```

## After Codex adversarial review completes

The human reads `.codex-outbox/<latest>.md`. Based on Codex's verdict:

- **CLEAN** → ready to build. Next: `/parallel-kickoff <prd-fork-id> <task-ids>`
- **CONCERNS** → human decides whether to fix or log risks. Often: fix highest
  severity, log the rest in risks.md, proceed.
- **BLOCK** → spec-writer revises, then `/plan-adversarial-next <prd-fork-id>` triggers R2.
  Max 4 rounds; after that human must decide whether to ship with open blockers
  or re-scope.

(The adversarial review loop command is `/plan-adversarial-next` — separate file.)

## Notes

- This command is a **coordinator**, not a doer. It kicks off spec-writer and
  task-decomposer (which do the real work) and primes Codex for review.
- Never call spec-writer directly without this command — it won't have the
  PRD → spec lineage context that this command arranges.
- After L4 is "CLEAN", human transitions to **parallel-kickoff** (already
  exists from v2.1) and **quality-gate** (already exists from v2.1). Those
  commands work unchanged.
