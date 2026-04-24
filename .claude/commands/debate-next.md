---
description: [DEPRECATED v3.0 — use /inspire-start → /explore-start → /scope-start → /plan-start instead] Advance Opus to the next round. Branches by stage. S1 has two sub-phases (A=Daydream, B=Ground); pass sub-phase letter as third argument for S1. S2 and S3 use numeric rounds.
argument-hint: "<idea-number> <stage> <sub-phase-or-round>  e.g. 001 1 B  or  001 2 1  or  001 3 2"
allowed-tools: Read, Write, Bash(ls:*), Bash(date:*), WebSearch, WebFetch, Glob, Grep
model: opus
---

# Debate · Next Round (Opus)

Idea **$1**. Stage **$2**. Sub-phase or Round **$3**.

## Step 1 — Enumerate and read

```bash
ls discussion/$1/ | sort
```

Read (in order):
1. `proposals/proposals.md` (re-confirm idea)
2. `.claude/skills/debate-protocol/SKILL.md`
3. `discussion/$1/$1-moderator-notes.md` if exists — **any injection is binding**
4. All prior rounds (both sides) in the current and earlier stages

## Step 2 — Branch by stage

### If $2 == 1 and $3 == B (Stage 1 · Ground · S1B)

**Preconditions**:
- `$1-Opus47Max-S1A.md` exists (your own daydream)
- `$1-GPT54xHigh-S1A.md` exists (opponent's daydream)

If either is missing, stop and tell the moderator.

**Read order for this round**:
1. Your own S1A
2. Opponent's S1A (all three parts: A, B, C)
3. Moderator notes

**Mandatory actions**:
- Merge your Part C question list (C.4) with opponent's Part C questions, de-duplicate
- Run **≥5 web searches** driven by merged list, use WebSearch tool
- Source diversity: not all blogs, not all academic, include ≥1 failure case if obvious
- Cite every source by URL

**Content obligations (use S1B template)**:
1. What opponent's S1A gave me that I missed (Part A insights / Part B risks / Part C questions)
2. Merged question list → searches run (queries + findings + URLs)
3. Prior art catalog (name · status · relevance · URL)
4. Reality vs daydream verdict on my own S1A:
   - Part A claims: stronger / weaker / unknown
   - Part B concerns: validated / defused / unknown
5. Graveyard lessons (repeat failure modes if prior art died)
6. What's genuinely novel here (after subtracting done / failed / trivial)
7. Updated hypothesis space (3–5 versions, scored on demand / differentiation / solo-feasibility)
8. Moderator injection response (if any)

Write to: `discussion/$1/$1-Opus47Max-S1B.md`
Length target: 500–1000 words, heavy on §2, §4, §7.

After writing, tell the human:
"S1B written. Codex writes its S1B in its own terminal (paste S1B kickoff). When
both S1Bs exist, run `/debate-advance-stage $1 2`."

### If $2 == 1 and $3 is anything else
Stop and tell the moderator:
"Stage 1 has two sub-phases only: S1A (Daydream) and S1B (Ground).
Use `/debate-start $1` for S1A or `/debate-next $1 1 B` for S1B.
S1 does not have numeric rounds."

### If $2 == 2 (Stage 2 · Position · cooperative)

**Preconditions**:
- `$1-stage1-synthesis.md` exists (run `/debate-advance-stage $1 2` first if not)

**Read order**:
1. `$1-stage1-synthesis.md` FIRST (the Stage 1 digest)
2. PROTOCOL.md
3. All Stage 1 files (both sides' S1A and S1B) for context
4. Your own and opponent's prior S2 rounds (if any)
5. Moderator notes

**Search**: ≥2 targeted searches if useful (lower bar than S1B).

**Content obligations (use S2R1+ template)**:
1. What I now believe the idea actually is (sharpened, maybe narrower)
2. Honest Y/N on "should this be built" (conditions or "instead do X")
3. Candidate directions: 2–4 peers (name · paragraph · risk · target user · survival angle)
   — Do NOT pick one
4. Direction I lean toward and why (honest, not neutral)
5. Deltas since S1B
6. Moderator injection response (if any)

Write to: `discussion/$1/$1-Opus47Max-S2R$3.md`

### If $2 == 3 (Stage 3 · Converge · engineering)

**Preconditions**:
- `$1-stage2-checkpoint.md` exists
- Moderator's direction decision is recorded in moderator-notes.md

If either missing, stop and tell the moderator.

**Content obligations (standard converge-round template)**:
- Steelman opponent's strongest point from prior S3 round (if any)
- ≤2 disagreements with testable hinges
- New ground
- ≥1 concession
- Self-critique
- Optional `<!-- READY-TO-CONCLUDE -->` + rationale

Write to: `discussion/$1/$1-Opus47Max-S3R$3.md`

## Step 3 — Output confirmation

Print one-line summary of this round's moves. Examples:
- "S1B: 7 searches across 7 unique URLs; my Part A claim <X> weakened; Part B concern <Y> validated by prior failure of <Z>; 4 updated hypotheses."
- "S2R1: direction menu has 3 peers (A/B/C); I lean B; 1 open question for moderator."
- "S3R1: 2 disagreements with testable hinges; 1 concession; not READY-TO-CONCLUDE yet."

Tell the human what kickoff to paste for Codex's matching round.
