---
description: Start L3 Scope phase. First runs L3R0 (human intake via AskUserQuestion — permissive of "not sure" answers), then Opus writes L3R1 (2-3 candidate PRD skeletons, no search, product-level only).
argument-hint: "<fork-id-or-idea-number>  e.g. 001a"
allowed-tools: Read, Write, Bash(mkdir:*), Bash(cp:*), Bash(echo:*), Bash(ls:*), Bash(date:*), AskUserQuestion, Glob, Grep
model: opus
---

# Scope · L3R0 (intake) + L3R1 (Opus side)

Idea **$ARGUMENTS**.

## Step 1 — preconditions

Verify L2 is complete:
```bash
ls discussion/.../<target>/L2/stage-L2-explore-*.md
```

If no L2 stage doc, stop and tell human:
> "L3 requires L2 complete. Run /explore-advance <target> first, or /status to see state."

Setup L3 dir:
```bash
mkdir -p discussion/.../<target>/L3
test -f .claude/skills/scope-protocol/SKILL.md && \
  cp .claude/skills/scope-protocol/SKILL.md discussion/.../<target>/L3/PROTOCOL.md
```

## Step 2 — read context

Read to understand the idea before intake:
1. `proposals/proposals.md` (root)
2. `discussion/.../<target>/L2/stage-L2-explore-<target>.md` — understand the idea
3. `.claude/skills/scope-protocol/SKILL.md`
4. `discussion/.../<target>/FORK-ORIGIN.md` (if fork)

## Step 3 — L3R0 intake via AskUserQuestion

**Design principle**: every question allows "not sure". "Not sure" is first-class,
not a fallback. It tells L3R1 models "generate options here".

Ask in order (use AskUserQuestion tool; ≤3 questions per tool call batched
sensibly — group related blocks):

### Batch 1 — Time + hours (Block 1)

```
Questions:
Q1. How soon do you want v0.1 in users' hands?
    - 1-2 weeks (sharp/small)
    - 3-6 weeks (small SaaS / app)
    - 2-3 months (full product)
    - 3+ months (platform-level)
    - Not sure — scope first, then match time

Q2. How many hours per week can you realistically put in?
    - Under 5 (nights/weekends only)
    - 5-15 (part-time)
    - 15-30 (serious commitment)
    - 30+ (full-time)
    - Varies a lot / not sure
```

### Batch 2 — Audience (Block 2)

Based on L2 report's candidate personas, construct audience choices
DYNAMICALLY. Example if L2 §3 showed 3 scenarios with named personas:

```
Q3. Which user slice feels most interesting to target FIRST?
    - <persona 1 from L2>, e.g. "Indie iOS devs with 1-3 side apps"
    - <persona 2>
    - <persona 3>
    - None of those — I'll describe it myself (free text)
    - Not sure — show me tradeoffs
```

### Batch 3 — Business model + Platform (Blocks 3, 4)

```
Q4. Rough business model for v0.1?
    - Free forever (OSS / hobby)
    - Free now, maybe paid tier later
    - Paid from day 1
    - Not sure — show me how each shapes scope

Q5. Platform constraint?
    - Web
    - iOS
    - Android
    - Desktop (macOS/Win/Linux)
    - CLI / terminal
    - API-only
    - No strong preference — pick what fits
    (multi_select allowed for 1-2)
```

### Batch 4 — Red lines (Block 5) — free text

```
Q6. Is there anything you absolutely WON'T do in v0.1?
    - Free text (multi-line OK)
    - Or type "none" / "not sure" — models will propose 3 likely red lines
      for your review in L3R1
```

### Batch 5 — Priorities (Block 6)

```
Q7. When two of these tradeoffs collide, which matter MOST? (pick 1-2)
    - Speed to ship
    - Polish / UX quality
    - Technical simplicity
    - Low operating cost
    - Differentiation from existing products
    - Broad appeal
    - Not sure — show me how priorities shape scope
```

### Batch 6 — Freeform catch-all

```
Q8. Anything I didn't ask but you want me to know?
    - Free text (multi-line OK)
    - Optional — just reply "no" or leave blank if nothing
```

## Step 4 — Write L3R0-intake.md

Compose `discussion/.../<target>/L3/L3R0-intake.md` using the template from
scope-protocol SKILL.md. Mark each answer with:
- ✅ if human gave a definitive answer
- 🤔 if answer was qualified / ranged ("somewhere between...")
- ❓ if human chose "not sure"
- 💡 for the freeform additions and human-written red lines

Finish with the "Summary for debaters" section listing hard constraints, soft
preferences, ❓ unknowns (models must propose options), and red lines.

Show human the assembled intake and ask for confirmation:
> "Intake captured. Anything to correct or add before L3R1 starts? (reply 'go'
> to proceed, or describe edits)"

If human edits, update and re-confirm.

## Step 5 — Opus writes L3R1

**HARD CONSTRAINTS**:
1. NO web search
2. DO NOT read GPT's L3R1
3. NO tech / architecture / stack / API content — PRODUCT-level scope only
4. Each candidate must be a **peer** (not "main + alternatives")
5. Proactively propose options for every ❓ in intake
6. If intake has no named red lines, propose 3 likely ones based on L2

Read:
- L3R0-intake.md (just written)
- L2 explore report
- scope-protocol SKILL.md
- L3-moderator-notes.md (if any)

Write `discussion/.../<target>/L3/L3R1-Opus47Max.md` with:
- §0 Reading of intake (what I'm honoring / where I'll propose options)
- §1-3 Candidates A, B, (C) — each with full structure from template
- §4 Options for ❓ items
- §5 Red lines I'd propose (if intake didn't name any)
- §6 Questions that need real user interviews

Length: 800-1500 words. 2-3 candidates. Honest time estimates.

## Step 6 — write Codex inbox task

Compute timestamp.
Queue id: `QUEUE=<target>`.

Ensure queue dirs:
```bash
mkdir -p .codex-inbox/queues/<target> .codex-outbox/queues/<target>
```

Write `.codex-inbox/queues/<target>/<TS>-<target>-L3R1.md`:

```markdown
# Codex Task · <target> · L3R1 (Scope R1)

**Queue**: <target>
**Created**: <ISO>
**Recommended model**: gpt-5.5
**Recommended reasoning_effort**: xhigh
**Estimated tokens**: ~8-14k
**Kickoff form**: oneshot

## Your role
You are GPT-5.5 xhigh, Debater B, L3R1 on idea <target>. Propose 2-3 peer
candidate scopes (PRD-skeleton level) under human's constraints from L3R0 intake.

## HARD CONSTRAINTS
- NO web search this round
- DO NOT read discussion/.../L3/L3R1-Opus47Max.md (parallel independence)
- NO tech / architecture / stack / API content — product-level only
- Each candidate is a peer (not "main + alternatives")
- Propose options for every ❓ in intake
- If intake has no red lines, propose 3 likely ones based on L2

## Read in order
- proposals/proposals.md (root)
- discussion/.../<target>/L2/stage-L2-explore-<target>.md
- discussion/.../<target>/L3/L3R0-intake.md  (human constraints + unknowns)
- .claude/skills/scope-protocol/SKILL.md
- AGENTS.md

## Write
discussion/.../<target>/L3/L3R1-GPT55xHigh.md using the L3R1 template:
- §0 Reading of intake
- §1-3 Candidates (2-3 peers, each with user/stories/IN/OUT/success/time/UX/risk)
- §4 Options for ❓ items
- §5 Proposed red lines (if needed)
- §6 Questions needing user interviews

800-1500 words.

## When done
Write .codex-outbox/queues/<target>/<TS>-<target>-L3R1.md with:
- Files written + word count
- Headline: one-line description of each candidate
- Which ❓ items you proposed options for
- Key tradeoff axis across candidates
- Anything Claude Code should know
```

Update queue HEAD pointer:
```bash
echo "<TS>-<target>-L3R1.md" > .codex-inbox/queues/<target>/HEAD
```

## Step 7 — output next-step menu

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ L3R0 intake captured + L3R1 Opus side done.

Intake summary:
  ✅ Hard constraints: <count>
  🤔 Soft preferences: <count>
  ❓ Unknowns (models will propose options): <count>
  💡 Freeform additions: <count or "none">

Opus L3R1 wrote <n> candidate scopes:
  A. <one-line>
  B. <one-line>
  [C. <one-line>]

Key tradeoff axis across candidates: <what differs>

📋 Next step: get Codex's L3R1.

[1] (默认) 新开 Codex 终端跑 (oneshot)
    → in your Codex terminal:  cdx-run <target>

[2] reuse-session 选项 (仅当你已在 Codex 终端连贯讨论这个 idea 时有意义)
    → 见 cdx-peek <target> 输出后粘贴；通常 L3R1 直接 oneshot 即可

[3] Show Codex kickoff for manual paste
    → cdx-peek <target>

[4] Show me Opus's L3R1 first
    → I'll show the file

[5] Inject a moderator note before Codex starts
    → tell me what to add (goes to L3/moderator-notes.md)

[6] Revise my intake answers
    → tell me what to change; I'll update L3R0-intake.md and we continue

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Reply 1/2/3/4/5/6 or describe.
```

## Notes for the Opus orchestrator

- When intake has many ❓, that's not a bad signal — it means the human is
  honest about uncertainty. Your §4 "options for ❓ items" is where you add
  real value: turn uncertainty into choosable concrete options.
- Red lines matter. If human didn't name any, propose 3 likely ones (pulled
  from L2's "natural limits" section). Human reads these in the menu and can
  accept/reject at fork time.
- Time estimates: honest > flattering. If the scope doesn't fit human's
  weekly-hours × target-weeks, say so. Don't silently shrink the scope to
  make the time work — that's what Candidate B/C are for.
