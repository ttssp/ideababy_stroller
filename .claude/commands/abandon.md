---
description: Abandon an idea or fork with a structured lesson document. Different from park — abandon means "I've learned this shouldn't be built", with the lessons captured for future reference.
argument-hint: "<idea-or-fork-id>  e.g. 001  or  001a"
allowed-tools: Read, Write, Edit, Bash(date:*), Bash(ls:*), AskUserQuestion, Glob
model: opus
---

# Abandon · close with structured lesson

Abandon `$ARGUMENTS`. Capture what you learned so future-you doesn't repeat the
same exploration — and so lessons can inform other ideas.

## Step 1 — confirm scope + readiness

Parse `$ARGUMENTS`:
- Root idea (e.g. `001`) → abandons the entire tree (all forks within get abandoned too unless explicitly excluded)
- Fork (e.g. `001a`) → abandons just that fork; siblings continue

Use AskUserQuestion:

```
Q: Are you sure you want to abandon <target>?
   - Yes — it shouldn't be built; I've learned what I needed
   - I meant to PARK (pause, expecting return) — use /park instead
   - Cancel
```

If not "Yes", route to /park or cancel.

## Step 2 — detect which layer abandonment happens in

Look at the state of `<target>`:
- Stopped at L1 menu → didn't like any direction
- Stopped during L2 → explore revealed low value
- Stopped at L3 menu → scope revealed mismatch with constraints
- Stopped after L4 adversarial review → spec revealed too-hard / too-risky
- Stopped during build → partial implementation taught us it's not worth completing

Note the stopping layer — it shapes which lessons are available.

## Step 3 — assemble available lesson material (automatic from artifacts)

Read whatever exists in `discussion/.../<target>/`:
- L1 stage doc if present
- L2 stage doc if present
- L3 stage doc + L3R0 intake if present
- Moderator notes across layers
- Codex outbox confirmations (for anything Codex noticed)

Extract:
- **Prior art discoveries** (from L1/L2 validation searches) — what's already out there
- **Failure patterns observed** (from L1/L2 graveyard lessons)
- **Market signals noticed** (from validation searches)
- **Constraints that killed it** (from L3 intake vs required scope mismatch)
- **Technical realities that killed it** (from L4 adversarial review, if reached)
- **Assumptions that proved wrong** (from R2 "what I'm less sure about now")

## Step 4 — ask human for the personal section

Use AskUserQuestion:

```
Q1. What's the MAIN reason you're abandoning? (pick up to 2)
   - Prior art exists and is strong
   - Prior art exists and failed for a reason I now understand
   - Constraints don't match (time / budget / skills)
   - My interest in this dropped during exploration
   - Technical risk too high given my capacity
   - Market signal is weak
   - Red line conflict I didn't see coming
   - Other (free text)

Q2. What did you learn about YOURSELF from this exploration? (optional free text)
   e.g. "I realized I don't have patience for B2C"
   e.g. "I underestimated how much I dislike support work"
   Leave blank if nothing generalizable.

Q3. Under what conditions MIGHT this ever make sense? (optional free text)
   e.g. "If the incumbent X goes away / If I had a co-founder / Never"
   Leave blank if you think it's truly dead.
```

## Step 5 — produce ABANDONED.md

Write `discussion/.../<target>/ABANDONED.md`:

```markdown
# Abandonment Lesson · <target>

**Abandoned at layer**: L<n> (<stage>)
**Abandoned date**: <ISO>
**Original proposal title**: "<from proposals.md>"
**Final understanding** (from the deepest stage reached):
<one-paragraph; from L2/L3 if available, else proposal>

## Why abandoned

**Primary reasons** (from human):
1. <human's Q1 answers>
2. <>

**Reasons evident from artifacts**:
- <from L1/L2/L3 material: e.g. "L2 search §3 found 3 incumbents with >50k users">
- <from L3 intake: e.g. "human's weekly hours (10) vs scope time estimate (18 weeks) = 3.5x gap">

## What we learned about this idea / this domain

(Auto-synthesized from artifacts. Even after abandon, this is keepable.)

### Prior art (who already does this)
| Name | Status | URL | Why it matters |

### Failure modes observed in prior attempts
- ...

### Demand signals (positive or negative)
- ...

### Axis where this proposal was structurally wrong
<e.g. "assumed sync usage; market actually wants async"
 or   "assumed B2C distribution works; the math doesn't">

## What I learned about myself (from human, optional)

<human's Q2, if provided>

## Conditions that might revive this

<human's Q3, if provided. If human said "never", preserve that — important for
 future-you to see you already thought about this.>

## Recyclable material

Things from this exploration that could feed other ideas:
- <from L1 menu: "direction #5 'B2B internal tools' might apply to idea 002">
- <from L2: "the user persona 'indie iOS devs' was sharp and correct — reuse">
- <prior art references that could be useful elsewhere>

## Stage artifacts preserved

The full exploration is preserved at:
- discussion/.../<target>/
(Don't delete. Future-you may grep through lessons-learned.md to find this.)

---

## Closure

This ABANDONED.md is appended to /lessons-learned.md for long-term recall.
If conditions change, revisit by running `/status <target>` — the tree is intact.
```

## Step 6 — update proposals.md status

Find entry for root idea (`**NNN**`). Update status. If abandoning root → overall
status `abandoned`. If abandoning one fork → list forks with their statuses:

```markdown
## **001**: <title>
**状态/Status**: partially abandoned
  · 001a: abandoned (2026-04-28) — prior art too strong
  · 001b: active, in L3
  · 001c: parked
```

## Step 7 — append to lessons-learned.md

If `lessons-learned.md` doesn't exist at repo root, create it:

```markdown
# Lessons Learned

Abandonment records across all ideas, in reverse chronological order.
Scan this periodically — patterns across abandonments often reveal how you
(the operator) should adjust your idea-generation.

---
```

Append a summary entry:

```markdown
## <ISO> · <target> · "<title>" · abandoned at L<n>

**Top reason**: <human's #1 from Q1>
**Key prior art**: <top 1-2 references>
**Personal lesson**: <human's Q2 if not empty, else "—">
**Revival condition**: <human's Q3 or "none">

Full record: discussion/.../<target>/ABANDONED.md
```

## Step 8 — output final menu

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Abandoned: <target>

Written:
  discussion/.../<target>/ABANDONED.md
  proposals.md (status updated)
  lessons-learned.md (entry appended)

Recyclable material flagged:
  <list of items from ABANDONED.md "Recyclable material" section>

📋 Next steps:

[1] Check recyclable material against other ideas
    → I can show you how abandoned lessons might apply to <other active idea>

[2] Read your lessons-learned.md to see patterns across abandonments
    → I'll display it

[3] Move on to a different idea
    → /status  (see all active)  or  /propose  (drop a new one)

[4] Just done
    → close terminal; nothing lost, tree preserved

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Reply 1/2/3/4 or describe.
```

## Notes

- Abandonment is NOT failure. It's information. Log it like you'd log a
  successful launch — with the same care.
- Don't delete the discussion tree. If conditions change in 2 years, the full
  exploration is still there.
- If the human wants to abandon because of momentary fatigue ("not now, too
  tired"), route to `/park` instead. Abandon is for "after real exploration,
  this shouldn't be built".
- `lessons-learned.md` grows over time. After 10+ abandonments, read it — you
  may find 3 always-true patterns about yourself as an operator.
