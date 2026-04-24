---
description: Append a moderator note to L3/moderator-notes.md for binding steering before the next round.
argument-hint: "<fork-id>  (then provide the note in a follow-up message)"
allowed-tools: Read, Write, Bash(mkdir:*), Bash(date:*), AskUserQuestion, Glob
model: sonnet
---

# Scope · inject moderator note

Idea **$ARGUMENTS**.

## Step 1 — verify scope exists

```bash
test -d discussion/.../<target>/L3/
```
If not, stop and suggest `/status <target>` or `/scope-start <target>`.

## Step 2 — ask human what to add

Use AskUserQuestion:

```
Q: What's the steering note? (free text, multi-line OK)
   Include:
   - What should debaters pay more attention to?
   - Any new constraint or preference?
   - Any red line to add?
```

Then:

```
Q: Binding on whom?
   - Both models (default)
   - Opus only
   - GPT only
```

Then:

```
Q: Type of note?
   - Hard constraint (must honor; overrides prior candidates)
   - Soft guidance (should consider; may argue against)
```

## Step 3 — append to moderator-notes.md

```bash
mkdir -p discussion/.../<target>/L3
touch discussion/.../<target>/L3/moderator-notes.md
```

Append:

```markdown

## Injection @ <ISO>
**Type**: <Hard constraint | Soft guidance>
**Binding on**: <Both | Opus | GPT>

<human's note>

### Required response
Next round both models (or specified) must address this in a section titled
"## Moderator injection response".
```

## Step 4 — output next-step menu

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Injection recorded at discussion/.../<target>/L3/moderator-notes.md

📋 Next steps:

[1] Run /scope-next <target> to get Opus's L3R2 (with injection honored)
[2] Restart L3R1 — the injection changes things fundamentally enough
    → I can delete existing L3R1s and re-run /scope-start
[3] Just save the note; I'll decide later when to trigger next round

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Reply 1/2/3 or describe.
```

Note: `/inspire-inject` and `/explore-inject` are analogous one-line wrappers.
This command is the canonical pattern.
