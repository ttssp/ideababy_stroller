---
description: Inject a moderator note into an ongoing debate that both models must respond to
argument-hint: "<idea-number> <round-tag>  (e.g. 001 R2.5)"
allowed-tools: Read, Write, Edit, Bash(ls:*), Bash(date:*), AskUserQuestion
model: sonnet
---

# Moderator Injection

Idea **$1**. Inject a binding note at round **$2** that both Opus and Codex must address next round.

## Step 1 — Gather the note

Ask the human (via AskUserQuestion if short, otherwise free text):

1. "What question or constraint are you injecting?" (free text, 1–3 sentences)
2. "Which side are you more skeptical of right now?"
   - Opus
   - Codex / GPT-5.4
   - Both equally
   - Neither — this is a new consideration
3. "Is this a hard constraint or a softer nudge?"
   - Hard constraint — must be honored
   - Soft guidance — consider but can be argued against

## Step 2 — Append to moderator notes

Target: `discussion/$1/$1-moderator-notes.md`. Create the file if missing, with:

```markdown
# Moderator Notes — Idea $1

Binding guidance from the human moderator, timestamped and numbered.
Both debaters MUST address every injection in the round immediately following its insertion.
```

Then append:

```markdown

## Injection @ $2
**Timestamp**: <date -u output>
**Type**: <Hard constraint | Soft guidance>
**Skeptical of**: <Opus | Codex | Both | Neither>

<the human's note, verbatim>

### Required response
- Opus: address in R<round after $2> under `## Moderator injection response`
- Codex: address in R<round after $2> under `## Moderator injection response`
```

## Step 3 — Optional — notify the active round

Show the human:
> "Injection recorded. Now tell both Opus and Codex:
>   'Before writing R<next>, check discussion/$1/$1-moderator-notes.md — there's an
>   injection @ $2 you must respond to.'
>
> If they've already started R<next>, ask them to pause and re-read notes first."

## Good injection patterns

Encourage the human to write sharp, decision-altering injections:
- "Budget is now hard-capped at $X/month. Revise any proposal above this."
- "Team size will be 1 person (me) for at least 6 months. Adjust ops story."
- "I won't ship until SOC2 ready. Factor in from day 1."
- "User interview feedback just came in: users actually want X, not Y. Reconsider."

Discourage vague injections:
- ❌ "Think more about performance" (no decision hinge)
- ❌ "Is this the right approach?" (not a constraint)
