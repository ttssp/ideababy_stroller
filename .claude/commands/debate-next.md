---
description: Advance Opus to the next round in its current stage. Handles pole switching (S1R2), cooperative mode (S2), and engineering mode (S3). Use search when stage requires.
argument-hint: "<idea-number> <stage> <round>  e.g. 001 1 2  or  001 2 1"
allowed-tools: Read, Write, Bash(ls:*), Bash(date:*), WebSearch, WebFetch, Glob, Grep
model: opus
---

# Debate · Next Round (Opus)

Idea **$1**. Stage **$2**. Round **$3**. Branch based on stage.

## Step 1 — Read (strict order)
```bash
ls discussion/$1/ | sort
```

Then read:
1. `proposals/proposals.md` (re-confirm idea)
2. `.claude/skills/debate-protocol/SKILL.md`
3. `discussion/$1/$1-moderator-notes.md` if exists — **any injection is binding**
4. All prior GPT rounds for current + earlier stages
5. All your own prior rounds
6. If stage == 2: **first** read `discussion/$1/$1-stage1-synthesis.md`
7. If stage == 3: **first** read `discussion/$1/$1-stage2-checkpoint.md`

## Step 2 — Branch by stage

### If $2 == 1 (Stage 1 · Explore)
Pole assignment:
- S1R1: Opus POSITIVE (already done via /debate-start)
- S1R2: Opus NEGATIVE (switch)
- S1R3: whichever pole you were weaker on in the prior round (your choice)
- S1R4: moderator-directed (check moderator notes; if silent, ask)

Mandatory: ≥5 fresh web searches. No repeats of queries from prior rounds.

Content obligations (use S1R2+ template):
- What the other side found that I missed (≥3)
- Fresh searches with URLs
- Steelman the now-assigned pole
- Where my prior pole overreached
- Updated hypothesis space (3–5 ranked versions of the idea)
- Single most-useful signal to resolve uncertainty

### If $2 == 2 (Stage 2 · Position · cooperative)
Posture is now cooperative. Fewer searches required (≥2 if useful).

Content obligations (use S2R1+ template):
- What I now believe the idea actually is (sharpened, maybe narrower)
- Honest Y/N on "should this be built"; state conditions or "instead do X"
- Candidate directions: 2–4 peers (name, paragraph, risk, target user). Do NOT pick one.
- Direction I lean toward — and why (honest, not neutral)
- Deltas since Stage 1
- Moderator injection response (if any)

### If $2 == 3 (Stage 3 · Converge · engineering)
Moderator must have chosen a direction in stage2-checkpoint (verify by reading it).
If no direction chosen, stop and tell the moderator.

Content obligations (use S3R1+ template):
- Steelman opponent's strongest point from prior S3 round (if any)
- ≤2 disagreements with testable hinges
- New ground
- ≥1 concession
- Self-critique
- Optional `<!-- READY-TO-CONCLUDE -->` + rationale

## Step 3 — Write

Target: `discussion/$1/$1-Opus47Max-S$2R$3.md`

Use the corresponding template in PROTOCOL.md. Paraphrase (≤15 words verbatim).

## Step 4 — Output confirmation

Print one line summarizing the round's moves. Example:
- "S1R2: switched to NEGATIVE pole; 6 new sources cited; hypothesis space narrowed to 3 versions."
- "S2R1: direction menu has 3 peers (A/B/C); I lean B; 1 open question for moderator."
- "S3R1: 2 disagreements with testable hinges; 1 concession; not yet READY-TO-CONCLUDE."

Tell the human: "Now run Codex's matching round in a separate terminal (see PROTOCOL.md)."
