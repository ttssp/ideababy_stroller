---
description: Append a moderator note to L1/moderator-notes.md for binding steering before the next L1 round (or a re-run after inspire-advance).
argument-hint: "<idea-number>  e.g. 001"
allowed-tools: Read, Write, Bash(mkdir:*), Bash(date:*), AskUserQuestion, Glob
model: sonnet
---

# Inspire · inject moderator note (L1)

Idea **$ARGUMENTS**.

## Step 1 — verify L1 context exists

```bash
test -d discussion/$ARGUMENTS/L1/
```

If not, stop and suggest `/inspire-start $ARGUMENTS` or `/status $ARGUMENTS`.

## Step 2 — ask human what to add

Use AskUserQuestion:

```
Q1: What's the steering note? (free text, multi-line OK)
    Include:
    - What angle should debaters pay more attention to?
    - Any new constraint or value dimension to consider?
    - A direction from the menu you want sharpened (if this is post-advance)?

Q2: Binding on whom?
    - Both models (default)
    - Opus only
    - GPT only

Q3: Type of note?
    - Hard constraint (must honor)
    - Soft guidance (should consider; may argue against)
```

## Step 3 — append to L1/moderator-notes.md

```bash
mkdir -p discussion/$ARGUMENTS/L1
touch discussion/$ARGUMENTS/L1/moderator-notes.md
```

Append:

```markdown

## Injection @ <ISO>
**Type**: <Hard constraint | Soft guidance>
**Binding on**: <Both | Opus | GPT>
**Applies to**: next L1R2 (or re-run of L1R2 if advance already ran)

<human's note>

### Required response
In the next round, affected models must address this in a section titled
"## Moderator injection response".
```

## Step 4 — output next-step menu

Detect state:
- If L1R1 exists but L1R2 doesn't → next natural action is L1R2 with this injection
- If L1R2 exists and stage-L1-inspire.md exists → menu is stale, re-run of L1R2 needed
- If only stage doc exists → need to re-run L1R2 then re-synthesize

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Injection recorded at discussion/$ARGUMENTS/L1/moderator-notes.md

📋 Next steps (based on current L1 state):

[1] Run /inspire-next $ARGUMENTS to trigger L1R2 with injection honored
    (if L1R2 hasn't been done yet)

[2] Re-run L1R2 (if it already ran; injection needs to influence it)
    → I'll delete existing L1R2 files first, then re-run
    → previous stage-L1-inspire.md will be overwritten after re-synthesis

[3] Just save the note; I'll decide when to trigger next round
    → no further action now

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Reply 1/2/3 or describe.
```

## Notes

- The injection is visible to debaters in subsequent rounds because both
  `/inspire-next` and the Codex kickoff templates read `moderator-notes.md`
  as binding context.
- If human already ran `/inspire-advance` (so `stage-L1-inspire.md` exists)
  and now wants re-inspiration with steering, option [2] is the right path —
  it re-runs L1R2 with the injection, then re-synthesizes the menu.
