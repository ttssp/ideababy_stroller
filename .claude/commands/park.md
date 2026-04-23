---
description: Park an idea or fork (preserve all artifacts, mark as paused with revival condition). Different from abandon — parking expects you'll return.
argument-hint: "<idea-or-fork-id>  e.g. 001  or  001a"
allowed-tools: Read, Write, Edit, Bash(date:*), AskUserQuestion
model: sonnet
---

# Park · pause an idea or fork (preserve, expect to return)

Park `$ARGUMENTS`. This is *not* abandon — parking is "good idea, wrong moment".

## Step 1 — confirm scope

If `$ARGUMENTS` is a root idea (`001`), parking pauses the entire tree.
If `$ARGUMENTS` is a fork (`001a`), parking pauses just that fork; siblings continue.

## Step 2 — gather revival info via AskUserQuestion

Ask the human:

1. **What's the revival condition?** (free text)
   "Park until X happens / Y becomes true / Z is feasible. Be specific so future-you
   knows when this is worth picking up again."

2. **Where to keep it visible?** (single-select)
   - Top of `proposals/proposals.md` parked section (default)
   - Specific tag/category (you'll tell me)
   - Just the FORK-ORIGIN.md / discussion folder note (no top-level reminder)

## Step 3 — write the park record

Create or update `discussion/<scope>/PARK-RECORD.md`:

```markdown
# Park record · <id>

**Parked at**: <ISO>
**Status before parking**: <e.g. "in L2-explore, both L2R1 done">
**Reason for parking**: <human's free text>
**Revival condition**: <human's text>
**Revival check date**: <suggest 30/60/90 days; ask human>

## What we have so far
- L1 inspire menu: <link or "n/a">
- L2 explore report: <link or "n/a">
- L3 scope decision: <link or "n/a">
- Code: <link or "n/a">

## Lessons captured during the live phase
(optional — anything worth remembering even if this never resumes)

---

To resume: run `/status <id>` and the system will load all artifacts back.
```

## Step 4 — update proposals.md

Find the entry for the root idea (e.g. `**001**`) and update its `**状态/Status**`
field. If parking a fork, list the fork separately:

```markdown
## **001**: <title>
**状态/Status**: parked (since 2026-04-23)
  · 001a: parked (revival: when iOS 19 ships APNs v2)
  · 001b: parked (revival: when I have 3 weeks free)
  · 001c: still in L2-explore
```

## Step 5 — output next-step menu

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🅿️  Parked: <id>

Park record: discussion/<scope>/PARK-RECORD.md
proposals.md updated.

📋 Next steps:

[1] Resume next time you /status <id>
    → all artifacts preserved; nothing lost

[2] Start a different idea now
    → /propose

[3] Continue with a sibling fork (if any)
    → /status <root> to see what else is active

[4] Look at other parked ideas (maybe one revival condition is now met)
    → I'll list them for you

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Reply 1/2/3/4 or just close the terminal.
```
