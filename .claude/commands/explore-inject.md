---
description: Append a moderator note to L2/moderator-notes.md for binding steering before the next L2 round (or a re-run after explore-advance).
argument-hint: "<fork-id-or-idea-number>  e.g. 001a"
allowed-tools: Read, Write, Bash(mkdir:*), Bash(date:*), AskUserQuestion, Glob
model: sonnet
---

# Explore · inject moderator note (L2)

Idea **$ARGUMENTS**.

## Step 1 — verify L2 context exists

```bash
test -d discussion/.../<target>/L2/
```

If not, stop and suggest `/explore-start <target>` or `/status <target>`.

## Step 2 — ask human what to add

Use AskUserQuestion:

```
Q1: What's the steering note? (free text, multi-line OK)
    Include:
    - What dimension should debaters unpack more deeply?
    - A user persona, use case, or extension angle you want examined?
    - A limit or constraint you want them to take seriously?
    - If this is post-advance: what part of the report felt underdeveloped?

Q2: Binding on whom?
    - Both models (default)
    - Opus only
    - GPT only

Q3: Type of note?
    - Hard constraint (must honor)
    - Soft guidance (should consider; may argue against)
```

## Step 3 — append to L2/moderator-notes.md

```bash
mkdir -p discussion/.../<target>/L2
touch discussion/.../<target>/L2/moderator-notes.md
```

Append:

```markdown

## Injection @ <ISO>
**Type**: <Hard constraint | Soft guidance>
**Binding on**: <Both | Opus | GPT>
**Applies to**: next L2R2 (or re-run if advance already ran)

<human's note>

### Required response
In the next round, affected models must address this in a section titled
"## Moderator injection response".
```

## Step 4 — output next-step menu

Detect state:
- If only L2R1 exists → next is L2R2 with this injection
- If L2R2 exists and stage-L2-explore-*.md exists → re-run L2R2 + re-synthesize
- If only stage doc exists → same as above

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Injection recorded at discussion/.../<target>/L2/moderator-notes.md

📋 Next steps:

[1] Run /explore-next <target> to trigger L2R2 with injection honored
    (if L2R2 hasn't been done yet)

[2] Re-run L2R2 (if it already ran; injection needs to influence it)
    → I'll delete existing L2R2 files first, then re-run
    → previous stage-L2-explore-*.md will be overwritten after re-synthesis

[3] Just save the note; I'll decide when to trigger next round

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Reply 1/2/3 or describe.
```
