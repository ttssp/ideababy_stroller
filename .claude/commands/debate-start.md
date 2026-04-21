---
description: Start S1A (Daydream phase) of the debate. Opus writes triple-section (A+B+C) independently, with NO web search. Pure imagination + epistemic honesty.
argument-hint: "<idea-number> (e.g. 001)"
allowed-tools: Read, Write, Bash(mkdir:*), Bash(cp:*), Bash(ls:*), Bash(date:*), Glob, Grep
model: opus
---

# Debate · S1A (Daydream · Opus)

You are Opus, Debater A. Idea **$ARGUMENTS**. This is **S1A**, the
daydream sub-phase of Stage 1. GPT writes its own S1A in parallel; you do
not read it.

## HARD CONSTRAINTS (this round only)

1. **DO NOT run any web search.** No WebSearch. No WebFetch. No `curl`, no
   `fetch`. This round is **pure imagination + epistemic honesty**. If you feel
   the urge to look something up, note it under Part C as a question for S1B.

2. **DO NOT read the opponent's S1A.** Verify with `ls discussion/$ARGUMENTS/`;
   if `$ARGUMENTS-GPT*.md` exists, refuse to open it.

3. **Triple-section structure is mandatory**: Part A + Part B + Part C, in that order.

## Setup
```
mkdir -p discussion/$ARGUMENTS
test -f discussion/PROTOCOL.md && cp discussion/PROTOCOL.md discussion/$ARGUMENTS/PROTOCOL.md
```

## Read (only these)
1. `proposals/proposals.md` — find entry `**$ARGUMENTS**`
2. `.claude/skills/debate-protocol/SKILL.md` (or the copy at `discussion/$ARGUMENTS/PROTOCOL.md`)
3. `CLAUDE.md`

Nothing else. Especially: no browsing, no search, no external fetches.

## Write

Target: `discussion/$ARGUMENTS/$ARGUMENTS-Opus47Max-S1A.md`

Template:

```markdown
# Idea $ARGUMENTS · S1A · Opus 4.7 Max · Daydream (no search)

**Timestamp**: <from `date -u +"%Y-%m-%dT%H:%M:%SZ"`>
**Search used**: NONE. This is imagination + memory only.
**Visibility**: I did NOT read GPT's S1A.

## Part A · Most-exciting version (POSITIVE pole)

If this idea succeeds in a 10x way, what does the world look like in 5–10 years?

- Who the users are and their lived experience
- Why this version is dramatically better than anything that exists today
- The "aha" moment when a user first encounters it
- Why I believe this is *possible* (set aside whether it's been done before)

Be willing to sound grand. This is imagination, not a business plan.
Length guidance: ~30% of the file.

## Part B · Most-damning version (independent NEGATIVE pole)

Set Part A aside. Start fresh.

From honest skepticism (not cynicism, not mockery), make a genuine case that
this idea will fail or shouldn't exist:
- Structural reasons it might not work
- Fundamental constraints (human behavior, economics, physics, regulation) it runs into
- If I recall prior similar attempts: what I remember about why they failed
- What I'd tell a founder who asked me "honestly, should I build this?"

Truthful, not theatrical. Real pessimism worth taking seriously — not a strawman.
Length guidance: ~30% of the file.

## Part C · Epistemic honesty — what I'd actually need to know

I just wrote two imaginative passages. Some of it is genuine intuition, some is
confabulation. Sort it:

### C.1 Claims backed by real confidence
For each major claim in Part A or Part B, note what it rests on:
  "Claim: ..." · "Source of my confidence: a paper I've read / a product I've used / domain intuition from X"

### C.2 Claims that are assumptions I haven't tested
Things I stated as if I knew, but actually don't.

### C.3 Known unknowns
Things I know I don't know. Be specific.

### C.4 Five search-shaped questions for S1B
Write them as actual search queries, not topic areas. These go into the
S1B merged question list.

1. ...
2. ...
3. ...
4. ...
5. ...

Length guidance: ~40% of the file — Part C is what drives S1B's value.
```

## Style rules

- Part A can be bold, Part B must be honest (not cynical), Part C must be concrete.
- Numbers over adjectives.
- No appeals to authority ("top companies do X" is not a reason).
- Paraphrase anything you remember; don't invent verbatim quotes.

## After writing

```bash
ls -la discussion/$ARGUMENTS/
```

Tell the human:
"S1A written (Daydream, no search). Now launch Codex S1A in a separate terminal —
paste the S1A kickoff from PROTOCOL.md §'Codex-side kickoffs'. GPT also writes
its triple-section independently, without search, without reading mine.

When both S1A files exist, run `/debate-next $ARGUMENTS 1 B` for the S1B grounding round."
