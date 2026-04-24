---
description: Close L3 and produce the candidate PRD menu (stage-L3-scope-<fork>.md). Runs scope-synthesizer. After this, human forks one or more candidates into PRD branches for L4, or re-scopes/parks/abandons.
argument-hint: "<fork-id-or-idea-number>  e.g. 001a"
allowed-tools: Read, Write, Bash(ls:*), Bash(date:*), Glob, Grep, Agent(scope-synthesizer)
model: opus
---

# Scope · close L3, produce PRD menu

Idea **$ARGUMENTS**.

## Step 1 — preconditions

```bash
ls discussion/.../<target>/L3/*.md
```

Required:
- L3R0-intake.md
- Both L3R1 files
- Both L3R2 files

If any missing, stop and tell human what's pending. `--partial` flag allowed
if human explicitly wants to synthesize with gaps (synthesizer will note it).

## Step 2 — invoke synthesizer

Delegate to `scope-synthesizer`:

> "Use scope-synthesizer on idea <target>.
>  Read: L3R0-intake, both L3R1, both L3R2, L2 stage doc (context), FORK-ORIGIN (if fork).
>  Output: discussion/.../<target>/L3/stage-L3-scope-<target>.md.
>  Produce ≥2 peer PRD candidates with comparison matrix, recap of honored
>  intake constraints, the key tradeoff axis, and synthesizer recommendation."

Wait for return.

## Step 3 — sanity check

Read the produced file. Check:
- Intake recap section present (hard constraints, red lines, ❓ resolved, ❓ still open)
- ≥2 candidate PRDs with all mandatory subsections
- Comparison matrix present
- Key tradeoff axis named
- Synthesizer recommendation explicit
- Decision menu present

If any check fails, ask synthesizer to revise.

## Step 4 — output human-facing menu

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ L3 done. Candidate PRD menu produced.

File: discussion/.../<target>/L3/stage-L3-scope-<target>.md
Candidates: <n> peer PRDs
Intake constraints honored: <count hard, count soft>
❓ items resolved by menu: <count>
❓ items still open for you: <count — list them briefly>

Key tradeoff axis: <from synthesizer §"The key tradeoff">

Synthesizer recommendation:
<quote or paraphrase the one-line recommendation>

📋 Your decision:

[1] Fork the recommended candidate into a PRD branch (if single recommendation)
    → /fork <target> from-L3 candidate-<X> as <target>-p<X>
    → then: /plan-start <target>-p<X>

[2] Fork MULTIPLE candidates in parallel (serve different users or validate both)
    → tell me which numbers; I'll prep /fork commands

[3] Re-scope — inject new input and run another L3 round
    → tell me what to add (goes to L3/moderator-notes.md)

[4] Back to L2 — the menu reveals I should rethink the idea itself
    → /status <target>

[5] Park — I need time to think (or interview real users first)
    → /park <target>

[6] Abandon — the menu makes it clear this shouldn't be built
    → /abandon <target>

[V] Show me the full menu before deciding
    → I'll display stage-L3-scope-<target>.md

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Reply 1/2/3/4/5/6/V or describe.
```

## Notes for the Opus orchestrator

- If synthesizer recommendation is "pause — too many ❓", lean toward option [5]
  (park) in the menu framing. Don't push human toward Fork when uncertainty is high.
- If one candidate is clearly stronger (from comparison matrix), make that
  prominent in option [1]. If candidates are genuine peers serving different
  users, emphasize option [2].
- "❓ items still open for you" is important — these are scope decisions that
  even the model couldn't resolve. Make them visible so human doesn't skip past.
