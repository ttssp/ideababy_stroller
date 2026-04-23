---
description: Close L2 and produce the L2 explore report (stage-L2-explore-<fork-id>.md). Runs explore-synthesizer subagent. After this, human decides — proceed to L3 (scope), fork another L2 angle, back to L1, re-explore, park, or abandon.
argument-hint: "<fork-id-or-idea-number>  e.g. 001a"
allowed-tools: Read, Write, Bash(ls:*), Bash(date:*), Glob, Grep, Agent(explore-synthesizer)
model: opus
---

# Explore · close L2, produce report

Idea **$ARGUMENTS**.

## Step 1 — preconditions

```bash
ls discussion/.../<target>/L2/*.md
```

Required: both L2R1, both L2R2.
If any missing, stop and tell human what's pending. Optionally proceed with
explicit `--partial` flag (synthesizer will note what's missing).

## Step 2 — invoke synthesizer

Delegate to `explore-synthesizer`:

> "Use explore-synthesizer on idea <target>.
>  Read all L2 files in discussion/.../<target>/L2/.
>  Output: discussion/.../<target>/L2/stage-L2-explore-<target>.md.
>  Origin context: <fork from L1 #n / direct from skip-mode>."

Wait for return.

## Step 3 — sanity check

Read the produced file. Check:
- Executive summary present
- §1-§7 all populated
- §6 validation verdict explicit (Y / Y-with-conditions / unclear / N)
- §7 open questions for L3 non-empty
- Decision menu present

If any check fails, ask synthesizer to revise.

## Step 4 — output human-facing menu

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ L2 done. Explore report produced.

File: discussion/.../<target>/L2/stage-L2-explore-<target>.md
Validation verdict: <Y / Y-with-conditions / unclear / N>
Executive summary:
  · <bullet 1 from synthesizer's exec summary>
  · <bullet 2>
  · <bullet 3>

Top 3 open questions for L3 (or for user research):
  1. <from §7>
  2. <from §7>
  3. <from §7>

📋 Your decision:

[1] Scope this idea — proceed to L3 (recommended if verdict is Y or Y-with-conditions)
    → /scope-start <target>
    (L3 brings in your real constraints, preferences, time/budget.)

[2] Fork another L2 angle from this same idea
    → /fork <target> from-L2 <new-angle> as <new-id>
    (use this if reading the report sparked a sharper cut)

[3] Back to L1 menu — pick another inspired direction
    → /status <root>  (see all L1 directions and other forks)

[4] Re-explore — inject new input and run another L2 round
    → tell me what to add, I'll write to L2/moderator-notes.md
       and we can run /explore-next <target>

[5] Park this fork (preserve, decide later)
    → /park <target>

[6] Abandon this fork (siblings continue)
    → /abandon <target>

[V] Show me the full L2 report before deciding
    → I'll display stage-L2-explore-<target>.md

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Reply 1/2/3/4/5/6/V or describe.
```

## Notes

- If validation verdict is **N**, gently suggest options 5 (park) or 6 (abandon).
  Don't refuse to proceed to L3 — human's call — but flag the verdict prominently.
- If verdict is **unclear**, suggest option 4 (re-explore with steering) before
  option 1.
- Open questions in §7 may include "we need to interview real users" — if so,
  recommend pausing the pipeline (option 5) until that's done. L3 without user
  input is often rework.
