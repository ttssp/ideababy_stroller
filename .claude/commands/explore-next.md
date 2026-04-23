---
description: Run L2R2 (Opus side) — read opponent's L2R1, run value-validation searches only, produce sharpened picture + open questions for L3.
argument-hint: "<fork-id-or-idea-number>  e.g. 001a"
allowed-tools: Read, Write, Bash(ls:*), Bash(date:*), Bash(ln:*), WebSearch, WebFetch, Glob, Grep
model: opus
---

# Explore · L2R2 (Opus side)

Idea **$ARGUMENTS**.

## Step 1 — preconditions

Verify both L2R1 files exist:
```bash
ls discussion/.../<target>/L2/L2R1-*.md
```

Need both `L2R1-Opus47Max.md` and `L2R1-GPT54xHigh.md`.
If either missing, stop and tell human (`/status <target>` to see state).

## Step 2 — read in order

1. `.claude/skills/explore-protocol/SKILL.md` (L2R2 template)
2. `discussion/.../<target>/L2/moderator-notes.md` (if exists; binding)
3. `discussion/.../<target>/L2/L2R1-GPT54xHigh.md` (opponent — all sections)
4. `discussion/.../<target>/L2/L2R1-Opus47Max.md` (your own L2R1)
5. (If forked) `discussion/<root>/L1/stage-L1-inspire.md` for L1 context

## Step 3 — value-validation searches only

**Allowed**:
- Prior art (products, services, projects)
- Demand signals (Reddit, HN, surveys, complaints)
- Failure cases (post-mortems, shutdowns, pivots)

**Forbidden** (these are L3/L4 questions):
- Tech stack queries
- Architecture decisions
- Cost / pricing models
- Implementation difficulty

Run **≥3** value-validation searches across the most concrete claims from
either side's L2R1. Don't search every claim — focus on ones where evidence
will most clarify the picture.

## Step 4 — write Opus's L2R2

Target: `discussion/.../<target>/L2/L2R2-Opus47Max.md`

Use L2R2 template:
- §1 What sharpened my thinking from opponent's L2R1 (≥3 specific things)
- §2 Where I'd push back (up to 3, honest)
- §3 Search-based reality check (table with URLs)
- §4 Refined picture (1-2 paragraphs — sharpened version of the idea)
- §5 Open questions L2 cannot answer (for L3 / user research)
- §6 Three things I'd want a real user interview to ask

Length: 600-1100 words. Heavy on §3 and §4.

## Step 5 — write Codex inbox task

Compute timestamp `$(date -u +%Y%m%dT%H%M%S)`.

Write `.codex-inbox/<TS>-<target>-L2R2.md` with the full Codex L2R2 kickoff
(template in explore-protocol SKILL.md §"L2R2 Codex kickoff").

Update `.codex-inbox/latest.md` symlink.

## Step 6 — output next-step menu

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ L2R2 Opus side done.
File: discussion/.../<target>/L2/L2R2-Opus47Max.md (<word-count> words)
Searches: <n> value-validation queries

Refined picture (§4 in 1 sentence):
"<the sharpened reading>"

Validation verdict: <Y / Y-with-conditions / unclear / N>
Top open question for L3: <from §5>

📋 Next step:

[1] Run Codex L2R2 (recommended)
    → in your Codex terminal:  cdx-run

[2] Show Codex kickoff for manual paste
    → I'll display .codex-inbox/latest.md

[3] Show me Opus L2R2 first
    → I'll display the file

[4] Inject moderator note before Codex
    → tell me what to add

[5] Skip Codex L2R2 and synthesize what we have
    → /explore-advance <target>  (will note Codex L2R2 missing)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Reply 1/2/3/4/5 or describe.
```
