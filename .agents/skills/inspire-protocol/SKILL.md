---
name: inspire-protocol
description: L1 Inspire layer protocol — the most upstream layer of the idea pipeline. Two top-tier models help human break out of cognitive limits by daydreaming N inspired directions adjacent/extended/reframed from the original proposal. Three modes (full/narrow/skip). Load when starting, continuing, or transitioning L1 in any discussion/.
disable-model-invocation: false
---

# L1 · Inspire Protocol

## What L1 is for

The original proposal is **a seed**. The human has cognitive limits — they can't
have read everything, can't see every adjacent angle, can't reframe their own
thinking easily. L1's job is to use two top-tier models (Opus 4.7 Max + GPT-5.4
xhigh) to **expand the idea space** around the proposal.

L1's output is an **inspired menu** — N candidate directions, each one a different
"this could be" reading of the original proposal. Human picks 1–N to fork.

## What L1 is NOT for

- **NOT for technical decisions.** No architecture talk, no stack choices, no
  cost estimates, no feasibility assessment. Those are L3/L4.
- **NOT for picking the "right" answer.** L1 produces options, human chooses.
- **NOT for committing to anything.** A direction in the L1 menu can be parked
  forever; the menu itself is valuable.

## Three modes

Human picks at start: `/inspire-start NNN [--mode=full|narrow|skip]`

### `full` (default) — proposal is vague or human wants exploration

Two rounds (L1R1 daydream + L1R2 cross & validate). Each debater produces 5–10
inspired directions in their L1R1. Final menu has 8–15 directions including the
proposal's original framing as a baseline.

### `narrow` — proposal is fairly clear, but worth checking nearby variations

Only one round. Each debater produces 3–5 close variations of the proposal.
Final menu has 4–6 entries: original + variations. Best for "I'm pretty sure
about my idea but want to see if I'm missing a better cut."

### `skip` — proposal is sharp, human wants to go straight to L2

L1 is bypassed. **But** L2's first round must include a section "Alternative
framings considered before settling on this one" — folding L1's value into L2.
This prevents tunnel vision.

## L1R1 template (Daydream — no general search; value-validation search OK in L1R2)

```markdown
# Idea NNN · L1R1 · <Model> · Inspire (no search)

**Timestamp**: <ISO>
**Mode**: full | narrow
**Search used**: NONE in this round.
**Visibility**: I did NOT read the other debater's L1R1.

## Part A · Adjacent directions
Same core impulse as the proposal, but switch a key dimension. For each:
- 1 sentence reframing
- 1 paragraph: who uses it, how, and the "aha" moment

Try at least 3 of these dimensions:
- **Audience swap**: B2C↔B2B, expert↔mass, individual↔team, ...
- **Form-factor swap**: desktop↔mobile↔CLI↔ambient, sync↔async, foreground↔background
- **Scope swap**: feature↔product↔platform, single-purpose↔suite, hyper-focused↔generic
- **Pain swap**: same audience, adjacent pain point in their life

Produce **3–5 adjacent directions** (3 if mode=narrow).

## Part B · Extended directions
Push the proposal toward extremes:
- **Maximally ambitious version**: if no constraints, what's the boldest cut?
- **Minimally focused version**: what's the smallest possible thing that still delivers?
- **Cross-domain transplant**: take the same mechanism into an unrelated field.

Produce **2–3 extended directions** (1–2 if mode=narrow).

## Part C · Reframed directions
Question the proposal's premises:
- Is the stated "problem" actually the real problem? What's the deeper pain?
- Does the implied "solution shape" have to look this way? What if it's totally different form?
- What assumptions did the human make that might not be true?

Produce **2–3 reframed directions** (1–2 if mode=narrow).

## Part D · My Top 3 with spark
From all the above (A + B + C), pick the 3 you find most genuinely interesting.
For each:
- Direction name (short, memorable)
- One paragraph: what it would feel like if it existed
- Spark point: what makes this *interesting* (not "feasible", not "profitable" —
  literally what makes it an idea worth thinking about)
- Why human probably didn't think of it themselves: what cognitive limit does
  this overcome? (e.g. "human framed as a B2C product, but a B2B
  internal-tools cut probably has 10x easier distribution")

Do NOT discuss feasibility, cost, technical difficulty, architecture, or "can
we actually build this". Only: is this interesting? Is it new? What can it do?
Who'd love it?
```

**Style mandates for L1R1**:
- 600–1200 words total
- Be bold; this is imagination, not a business plan
- Be specific; "an AI tool" is not a direction, "an AI tool that listens to
  Slack and summarizes your weekly contributions in your own voice for your
  own performance review" is
- Don't repeat the proposal's framing — Part A/B/C must each move the framing somewhere

## L1R2 template (Cross + value-validation search)

In this round, models read each other's L1R1 and may search **only for value
validation** (not for technical/implementation info).

**Allowed search categories**:
- "Has someone done this?" (prior art for value validation)
- "Do users really want this?" (Reddit, HN, surveys, complaints)
- "Has this been tried and failed/succeeded?" (case studies)

**Forbidden search categories** (these are L4 questions, not L1):
- "What stack should I use?"
- "How would I architect this?"
- "What are the technical risks?"
- "How much would this cost?"

```markdown
# Idea NNN · L1R2 · <Model> · Cross + Value Validation

**Timestamp**: <ISO>
**Mode**: full | narrow
**Searches run**: <n>, all in value-validation category
**Opponent's L1R1 read**: yes

## 1. From opponent's L1R1, directions I also find compelling
Pick up to 3 directions from opponent's Part D (or A/B/C) that you also like.
For each, one sentence on what makes it good — in your words, not theirs.

## 2. From opponent's L1R1, directions I'd push back on
Pick up to 3 you think are weaker. Why?
(Honest, not contrarian. If everything's great, say so and explain.)

## 3. Value-validation search results
For the most promising 3–5 directions across both R1s, what does the world say?

| Direction | Prior art status | Demand signal | Failure cases | Verdict |

Cite URLs.

## 4. My refined Top 3
After cross-reading and validation, my updated top 3 (may differ from R1):
- Direction name
- Why it survived validation (or: validation made it more interesting)
- "Aha" framing in one sentence

## 5. New directions sparked by reading opponent's R1
Sometimes the best ideas come from the gap between two views. Anything
new you can produce now that neither of you said in R1?
```

## inspire-synthesizer output (stage-L1-inspire.md)

After both L1R2s exist (or L1R1s in narrow mode), the `inspire-synthesizer`
agent runs and produces `discussion/NNN/L1/stage-L1-inspire.md`.

This document is what human reads and decides forks from. Structure:

```markdown
# L1 Inspire Menu · Idea NNN · "<title>"

**Mode**: full | narrow
**Generated**: <ISO>
**Total directions surfaced**: <n>

## How to read this

This menu is the L1 layer's output: directions inspired by your original proposal.
Each entry is a *possibility*, not a recommendation. You'll fork the ones that
feel interesting using:  /fork NNN from-L1 direction-<n> as <new-id>

You can also park this whole menu and revisit later. It has long-shelf-life value
even if you never build any of these — coming back in 6 months may surface a
direction whose moment has come.

## Your original proposal (baseline)
<one-paragraph from proposals.md>

## Inspired directions

### Direction 1 · "<short name>"
**Source**: Opus L1R1 Part A · GPT L1R2 §4 (both endorsed)
**Description**: <one paragraph>
**Spark**: <what makes this interesting>
**Cognitive jump from proposal**: <what human probably wouldn't have thought of>
**Value validation evidence**: <prior art, demand signals, failure cases — paraphrased + URLs>
**Suggested fork id**: 001a

### Direction 2 · ...
(repeat for all 4–15 directions)

---

## Cross-reference: who proposed what

| Direction | Opus surfaced | GPT surfaced | Both endorsed |
|---|---|---|---|

## Themes I notice across the menu

(synthesizer's editorial: are there clusters? does the menu lean one way?)

## Decision menu (this is for human)

### [F] Fork one or more directions
For each direction you want to develop, run:
  /fork NNN from-L1 direction-<n> as <new-id>

### [R] Reset and re-inspire with my input
If the menu doesn't capture what you actually want, add a steering note:
  /inspire-inject NNN "<your steering>"
Then re-run L1R2.

### [P] Park the whole menu, come back later
  /park NNN

### [S] Skip directly to L2 with the original proposal
If after seeing this menu you still prefer the original framing, just go:
  /explore-start NNN

(All forks created from this menu reference back to this document. Future
forks can be made even months from now using the same /fork command.)
```

## Codex-side kickoff prompts

Embedded in inbox files automatically. Also reproduced here for manual paste
fallback:

### L1R1 (mode=full)
```
You are GPT-5.4 xhigh, Debater B, L1R1 on idea NNN, mode=full.

HARD CONSTRAINT: NO web search this round. No WebSearch, no WebFetch.
DO NOT read discussion/NNN/L1/L1R1-Opus47Max.md (parallel independence).

Read: proposals/proposals.md (NNN), .Codex/skills/inspire-protocol/SKILL.md, AGENTS.md

Write discussion/NNN/L1/L1R1-GPT54xHigh.md using the L1R1 four-section template
(A · adjacent · 3-5, B · extended · 2-3, C · reframed · 2-3, D · top 3 with spark).

600-1200 words. Bold and specific.
```

### L1R1 (mode=narrow)
Same as above but tell model "mode=narrow → produce 3 adjacent, 1-2 extended,
1-2 reframed, total ~4-7 directions in Part D".

### L1R2
```
You are GPT-5.4 xhigh, L1R2 on idea NNN.

VALUE-VALIDATION SEARCH ONLY. Allowed: prior art, user demand, failure cases.
Forbidden: tech stack, architecture, cost, feasibility (those are L4).

Read in order:
  .Codex/skills/inspire-protocol/SKILL.md
  discussion/NNN/L1/L1-moderator-notes.md (if exists; binding)
  discussion/NNN/L1/L1R1-Opus47Max.md (opponent's R1, all four parts)
  your own L1R1

Run ≥3 value-validation searches. Cite URLs.
Write discussion/NNN/L1/L1R2-GPT54xHigh.md using the L1R2 5-section template.
```

## Quality bars for advancing L1 → fork → L2

L1 is "done enough to fork" when:
- Both debaters wrote L1R1 (in full or narrow mode)
- (full mode) Both wrote L1R2
- inspire-synthesizer produced stage-L1-inspire.md with ≥4 directions
- Human read the menu and selected ≥1 direction to fork
