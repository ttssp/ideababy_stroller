---
description: Close L1 and produce the inspired-direction menu (stage-L1-inspire.md). Runs the inspire-synthesizer subagent. After this, human chooses which directions to fork.
argument-hint: "<idea-number>  e.g. 001"
allowed-tools: Read, Write, Bash(ls:*), Bash(date:*), Glob, Grep, Agent(inspire-synthesizer)
model: opus
---

# Inspire · close L1, produce menu

Idea **$ARGUMENTS**.

## Step 1 — preconditions

```bash
ls discussion/$ARGUMENTS/L1/*.md 2>/dev/null
```

Required: at least both L1R1s. L1R2s are required if mode=full.
Detect mode by checking the L1R1 frontmatter.

If mode=full and L1R2s missing on either side, stop:
> "Cannot synthesize — mode=full requires both L1R2s. Codex L1R2 is missing.
> Run /inspire-next or paste the L1R2 kickoff in Codex."

If mode=narrow and only L1R1s exist, that's fine, proceed.

## Step 2 — invoke the synthesizer

Delegate to `inspire-synthesizer` subagent:

> "Use inspire-synthesizer on idea $ARGUMENTS.
>  Read all files in discussion/$ARGUMENTS/L1/.
>  Output to discussion/$ARGUMENTS/L1/stage-L1-inspire.md.
>  Mode = <full|narrow> (detected from R1 frontmatter)."

Wait for it to return.

## Step 3 — sanity-check the synthesis

Read the produced `stage-L1-inspire.md`. Quick checks:
- ≥4 directions listed
- Each direction has: name, description, spark, cognitive jump, validation, suggested fork id
- Cross-reference table present
- Decision menu section present

If any check fails, ask the synthesizer to revise the file and re-check.

## Step 4 — output the human-facing menu

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ L1 done. Inspired menu produced.

File: discussion/$ARGUMENTS/L1/stage-L1-inspire.md
Total directions surfaced: <n>
Both-endorsed: <n>
Cognitive-jump highlights: <list 2-3 with shortest descriptions>

📋 Your decision:

[F1] Fork direction <best-1> as <suggested-id-1>  (most "spark")
     → /fork $ARGUMENTS from-L1 direction-<n> as <id>

[F2] Fork direction <best-2> as <suggested-id-2>
     → /fork $ARGUMENTS from-L1 direction-<n> as <id>

[F3] Fork multiple directions (in parallel — recommended for high-spark menus)
     → I'll prep multiple /fork commands; tell me which numbers

[R]  Re-inspire — menu doesn't capture what I want
     → tell me the steering, I'll add to L1-moderator-notes.md and we re-run L1R2

[S]  Skip the menu, just go to L2 with my original proposal
     → /explore-start $ARGUMENTS  (the menu stays for future reference)

[P]  Park the menu, I'll come back later
     → /park $ARGUMENTS

[V]  Show me the full menu before deciding
     → I'll cat discussion/$ARGUMENTS/L1/stage-L1-inspire.md

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Reply F1/F2/F3/R/S/P/V or describe what you want.
```

## Notes

- Don't push human toward Fork. The L1 menu has long-shelf-life value — Park
  is a perfectly valid choice; the human can come back in a month and fork.
- "Both-endorsed" directions are typically (but not always) the safest forks.
  Surface those prominently in the menu but don't hide solo-endorsed ones —
  asymmetric insights are often where the real value is.
- The `<best-1>`, `<best-2>`, `<id-1>`, `<id-2>` placeholders should be filled
  with actual direction numbers + short snake_case ids that the synthesizer
  suggested.
