---
description: Advance the debate from one stage to the next. Runs the relevant synthesizer (stage1-synthesizer or stage2-checkpoint) and presents a decision menu to the moderator.
argument-hint: "<idea-number> <target-stage>  e.g. 001 2  means advance from Stage 1 to Stage 2"
allowed-tools: Read, Write, Bash(ls:*), Glob, Grep, Agent(stage1-synthesizer), Agent(stage2-checkpoint)
model: opus
---

# Debate · Advance Stage

Idea **$1**. Advance to Stage **$2**.

## Precondition check

Enumerate what exists:
```bash
ls discussion/$1/*.md | sort
```

### If $2 == 2 (advancing from Stage 1 to Stage 2)
Verify Stage 1 quality bar (from PROTOCOL.md §"Quality bars"):
- Both debaters wrote **S1A** (daydream): `$1-Opus47Max-S1A.md` AND `$1-GPT54xHigh-S1A.md`
- Both debaters wrote **S1B** (ground): `$1-Opus47Max-S1B.md` AND `$1-GPT54xHigh-S1B.md`
- Each S1A contains all three parts (A, B, C) — grep for `## Part A`, `## Part B`, `## Part C`
- Each S1B cites ≥5 distinct URLs — grep for `http` occurrences

If any fails: **stop** and tell the moderator what's missing. Examples:
> "Cannot advance — Opus S1A missing Part C. Rerun `/debate-start $1` with the full triple-section."
> "Cannot advance — GPT S1B cites only 3 URLs (needs ≥5). Have Codex run more searches."

If all pass: invoke **`stage1-synthesizer`** subagent:
> "Use stage1-synthesizer on idea $1. Output: `discussion/$1/$1-stage1-synthesis.md`."

After it returns, print to the moderator:
> "Stage 1 synthesis complete at discussion/$1/$1-stage1-synthesis.md.
> Read it — it preserves the imagination vs evidence distinction.
> When ready for Stage 2:
>   - Opus: `/debate-next $1 2 1`
>   - Codex: paste S2R1 kickoff from PROTOCOL.md"

### If $2 == 3 (advancing from Stage 2 to Stage 3)
Verify Stage 2 quality bar:
- ≥2 S2 rounds per side OR moderator forces with `--force` flag
- Both sides' S2 rounds contain a direction menu (2–4 peers)

If any fails: stop and tell the moderator.

If passes: invoke **`stage2-checkpoint`** subagent:
> "Use stage2-checkpoint on idea $1. Output file: `discussion/$1/$1-stage2-checkpoint.md`.
> This file must present the moderator with:
>   - A unified list of direction candidates across both debaters
>   - A short comparison matrix
>   - A recommended decision with reasoning
>   - A clear decision menu: [Advance with direction X] / [Fork] / [Park] / [Abandon]"

After it returns, **STOP** and print to the moderator:
> "Stage 2 checkpoint ready at discussion/$1/$1-stage2-checkpoint.md.
> Your decision is REQUIRED before Stage 3 begins. Options:
>
>   1. Advance (choose a direction from the menu)
>      → Record your choice in moderator-notes.md, then run:
>         `/debate-next $1 3 1`
>      → Codex counterpart: paste S3R1 kickoff from PROTOCOL.md.
>
>   2. Fork (split into sub-debates)
>      → Create new entries in proposals.md (e.g. 001a, 001b) for each direction worth pursuing.
>      → Then run `/debate-start <new-id>` for each.
>      → Archive current debate with status 'forked'.
>
>   3. Park (archive for later)
>      → Add a note to proposals.md entry $1: 'Status: parked on <date>, reason: ...'
>      → This debate stops here; no Stage 3.
>
>   4. Abandon (evidence says don't build)
>      → Add a note to proposals.md entry $1: 'Status: abandoned, lesson: ...'
>      → Write a 1-page lesson to discussion/$1/$1-abandonment-lesson.md for future reference.
>      → This prevents re-proposing the same idea without engaging with what we learned."

## Notes

- This command does NOT automatically start Stage N. The moderator must explicitly
  trigger the next round after reviewing the synthesis/checkpoint.
- `--force` flag bypasses quality-bar checks. Use only if you know what you're doing
  (e.g. an S-level idea where extensive search is overkill).
- If the moderator chose "Fork", archive this debate's folder — don't delete it.
  The fork decisions reference S1/S2 findings.
