---
description: Run L1R2 (Opus side) — read opponent's L1R1, run value-validation searches only (NO tech/feasibility searches), produce refined direction list. Only meaningful in mode=full; mode=narrow ends after L1R1.
argument-hint: "<idea-number>  e.g. 001"
allowed-tools: Read, Write, Bash(ls:*), Bash(date:*), Bash(ln:*), WebSearch, WebFetch, Glob, Grep
model: opus
---

# Inspire · L1R2 (Opus side)

Idea **$ARGUMENTS**.

## Step 1 — preconditions

Verify both L1R1 files exist:
```bash
test -f discussion/$ARGUMENTS/L1/L1R1-Opus47Max.md
test -f discussion/$ARGUMENTS/L1/L1R1-GPT54xHigh.md
```

If either is missing, stop and tell the human:
> "Cannot run L1R2 — <which side> hasn't completed L1R1 yet. Run /status $ARGUMENTS to see what's pending."

## Step 2 — read in this order

1. `.claude/skills/inspire-protocol/SKILL.md` (L1R2 template)
2. `discussion/$ARGUMENTS/L1/L1-moderator-notes.md` (if exists; **binding injections**)
3. `discussion/$ARGUMENTS/L1/L1R1-GPT54xHigh.md` (opponent — all four parts)
4. `discussion/$ARGUMENTS/L1/L1R1-Opus47Max.md` (your own L1R1)

## Step 3 — run value-validation searches

**Allowed search categories** (cite URLs):
- "Has someone done X?" — prior art, products, projects
- "Do people want X?" — Reddit, HN, Stack Overflow complaints, surveys
- "Has X been tried & failed/succeeded?" — case studies, post-mortems, news

**FORBIDDEN search categories** (these belong to L4, not L1):
- Tech stack queries
- Architecture queries
- Cost / pricing queries
- Implementation difficulty queries

Run **≥3** value-validation searches across the most promising directions
from both sides' L1R1s. Don't search every direction — focus on the ones with
real "spark" and on directions where prior art is genuinely unclear.

## Step 4 — write Opus's L1R2

Target: `discussion/$ARGUMENTS/L1/L1R2-Opus47Max.md`

Use the L1R2 5-section template from the protocol:
1. From opponent's L1R1, directions I also find compelling (≤3)
2. From opponent's L1R1, directions I'd push back on (≤3, honest)
3. Value-validation search results (table with URLs)
4. My refined Top 3 (may differ from R1)
5. New directions sparked by reading opponent's R1 (if any)

Length: 500–900 words. Heavy on §3 and §4.

## Step 5 — write Codex inbox task

Compute timestamp `$(date -u +%Y%m%dT%H%M%S)`.

Write `.codex-inbox/<TS>-$ARGUMENTS-L1R2.md`:

```markdown
# Codex Task · idea $ARGUMENTS · L1R2

**Created**: <ISO>
**Recommended model**: gpt-5.4
**Recommended reasoning_effort**: xhigh
**Estimated tokens**: ~6-12k

## Your role
You are GPT-5.4 xhigh, Debater B, L1R2 on idea $ARGUMENTS. Read opponent's
L1R1, run value-validation searches only, produce a refined direction list.

## CONSTRAINTS
- VALUE-VALIDATION SEARCH ONLY:
    Allowed: prior art / user demand / failure cases
    Forbidden: tech stack / architecture / cost / feasibility
- Quote ≤15 words verbatim from any source

## Read in order
1. .claude/skills/inspire-protocol/SKILL.md
2. discussion/$ARGUMENTS/L1/L1-moderator-notes.md (if exists; binding)
3. discussion/$ARGUMENTS/L1/L1R1-Opus47Max.md (opponent — all four parts)
4. your own L1R1 (discussion/$ARGUMENTS/L1/L1R1-GPT54xHigh.md)

## Search
≥3 value-validation searches. Cite URLs.

## Write
discussion/$ARGUMENTS/L1/L1R2-GPT54xHigh.md using the L1R2 5-section template.
500-900 words.

## When done
Write .codex-outbox/<TS>-$ARGUMENTS-L1R2.md with:
  - Files written + word count
  - Top 3 in your refined §4
  - Any directions you abandoned (with reason)
  - Note for Claude Code if needed
```

Update symlink:
```bash
cd .codex-inbox && ln -sf <TS>-$ARGUMENTS-L1R2.md latest.md
```

## Step 6 — output next-step menu

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ L1R2 Opus side done.
File: discussion/$ARGUMENTS/L1/L1R2-Opus47Max.md (<word-count> words)
Searches run: <n> value-validation queries

Key updates this round:
  · Validated: <direction or claim that prior art supports>
  · Weakened: <direction or claim that evidence undermines>
  · New: <any direction sparked by reading opponent>

📋 Next step:

[1] Run Codex L1R2 (recommended)
    → in your Codex terminal:  cdx-run

[2] Show Codex kickoff for manual paste
    → I'll display .codex-inbox/latest.md

[3] Show me Opus's L1R2 first
    → I'll display discussion/$ARGUMENTS/L1/L1R2-Opus47Max.md

[4] Inject a moderator note before Codex runs
    → tell me what to add

[5] Skip Codex L1R2 and synthesize what we have
    → /inspire-advance $ARGUMENTS  (will note Codex L1R2 missing)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Reply 1/2/3/4/5 or describe what you want.
```
