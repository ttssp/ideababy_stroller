---
name: debate-protocol
description: Three-stage debate protocol for Opus 4.7 vs GPT-5.4 xhigh. Stages are Explore (diverge + search + opposing poles) → Position (converge on evidence, produce direction menu) → Converge (engineering, only if moderator approves). Load when starting, continuing, or transitioning a debate in discussion/.
disable-model-invocation: false
---

# Debate Protocol — v2.0 (Three-Stage)

## Why three stages

Not every idea deserves to be built. Some are already done, already failed, or too
vague. Forcing every idea straight to architecture skips the "should this exist"
question. Stages fix that:

- **Stage 1 · Explore** — diverge, search, one side bullish one side bearish, switch poles R2
- **Stage 2 · Position** — converge on evidence, produce 2–4 direction menu
- **Stage 3 · Converge** — engineering (only if moderator approves after Stage 2)

The moderator can EXIT at end of Stage 1 or Stage 2 ("park", "abandon", "fork into
sub-debates"). Not every idea must reach Stage 3.

## Stage 1 · EXPLORE

**Goal**: map the idea space, find prior art, find failure cases, form hypotheses.

**Poles**:
- S1R1: Opus = POSITIVE (what would make this spectacular), GPT = NEGATIVE (why this dies)
- S1R2: **poles switch** — Opus now bearish, GPT now bullish (forces real steelmanning)
- S1R3+ (if needed): moderator assigns, or both pick whichever pole they're weaker on

**Mandatory per round**: ≥5 external sources from web search. Cite by URL. Diverse
(not all blogs, not all academic). Include ≥1 failure case if obvious prior art exists.

**R1 is independent** (neither reads the other's S1R1). R2+ reads prior rounds.

## Stage 2 · POSITION

**Goal**: converge on what the idea actually is, whether it should exist, and if yes,
what 2–4 candidate directions are worth pursuing.

**Posture**: cooperative. Both read Stage 1 synthesis, build on each other.
**Min sources**: ≥2 per round (lower bar than Stage 1).
**Required output in each round**: a direction menu of 2–4 peers (do NOT pick one).

**End of Stage 2 → moderator checkpoint (REQUIRED)**. Menu of choices:
- Advance to Stage 3
- Fork & re-debate (spin off one or more sub-debates)
- Park (archive with notes for later)
- Abandon (evidence says don't build)

## Stage 3 · CONVERGE

**Goal**: architecture + MVP for the direction the moderator chose.

**Posture**: engineering-focused. Same obligations as traditional debate rounds:
- Steelman counterpart's strongest point
- ≤2 disagreements, each with testable hinge
- New ground
- Concessions (≥1)
- Self-critique
- Optional `<!-- READY-TO-CONCLUDE -->` marker

## Stage transitions

```
Stage 1 (Explore, ≥2 rounds, opposing poles, ≥5 sources/round)
   │
   ▼
Moderator: ready to converge?
   │
   ├── Yes → stage1-synthesizer runs → Stage 2
   │           │
   │           │ Stage 2 (Position, ≥2 rounds, cooperative, direction menu)
   │           ▼
   │         stage2-checkpoint runs → Moderator Checkpoint (REQUIRED)
   │           │
   │           ├── Advance → Stage 3 → Finals → /debate-conclude
   │           ├── Fork    → spawn new proposal(s), archive this one
   │           ├── Park    → archive with notes
   │           └── Abandon → archive with lesson
   │
   └── No (need more exploration) → another S1 round (cap at S1R4)
```

## Round file naming

```
discussion/NNN/
  PROTOCOL.md
  NNN-Opus47Max-S1R1.md        # opus positive
  NNN-GPT54xHigh-S1R1.md       # gpt negative
  NNN-Opus47Max-S1R2.md        # opus switched to negative
  NNN-GPT54xHigh-S1R2.md       # gpt switched to positive
  NNN-moderator-notes.md
  NNN-stage1-synthesis.md      # auto, after /debate-advance-stage NNN 2
  NNN-Opus47Max-S2R1.md
  NNN-GPT54xHigh-S2R1.md
  NNN-stage2-checkpoint.md     # auto, presents decision menu
  NNN-Opus47Max-S3R1.md        # only if Advance
  NNN-GPT54xHigh-S3R1.md
  NNN-Opus47Max-final.md
  NNN-GPT54xHigh-final.md
```

## Per-stage templates (compact)

### S1R1 template
```markdown
# Idea NNN · S1R1 · <name> · Pole: <positive|negative>

## 1. Idea restated
## 2. Searches run (≥5 queries, one-line finding each, URLs)
## 3. Prior art (products/attempts, status, lessons)
## 4. Evidence for my pole (with citations)
## 5. Signals that would flip my pole
## 6. Open questions only more search can answer
## 7. Self-critique — if forced to argue opposite, my strongest point would be...
```

### S1R2+ template (poles switched)
```markdown
# Idea NNN · S1R<n> · <name> · Pole: <flipped>

## 1. What the other side found that I missed (≥3)
## 2. Fresh searches (≥5 new, not repeats)
## 3. Steelman the now-assigned pole, evidence-grounded
## 4. Where my R1 pole overreached
## 5. Updated hypothesis space — 3–5 plausible versions of this idea, ranked
## 6. Single most-useful signal to resolve uncertainty
```

### S2R1+ template (cooperative)
```markdown
# Idea NNN · S2R<n> · <name>

## 1. What I now believe the idea actually is (sharpened, maybe narrower)
## 2. Honest Y/N on "should this be built"
     - If N: why, and what operator should do instead
     - If Y: under what conditions
## 3. Candidate directions (2–4 peers, each with name, paragraph, risk, target user)
## 4. Direction I lean toward — and why (honest, not neutral)
## 5. Deltas since Stage 1 — updates, abandonments, hardenings
## 6. Moderator injection response (if any)
```

### S3R1+ template (engineering)
```markdown
# Idea NNN · S3R<n> · <name>

(Same as traditional converge-phase round:
  Steelman / ≤2 Disagreements with testable hinges / New ground / ≥1 Concession / Self-critique)

Plus optional:
<!-- READY-TO-CONCLUDE -->
Rationale: ...
```

### Finals template
Standalone document, 300–700 lines:
1. Final recommendation (5 bullets)
2. Full technical proposal
3. MVP plan (Phase 0/1/2)
4. Consensus with counterpart (strict)
5. Residual disagreements + honest "who's right" verdict
6. Where counterpart was stronger (≥2)
7. Where I was stronger (≥2)
8. Top 5 actionable recommendations for moderator
9. Open questions moderator must answer
10. Sign-off: "Ready for SDD" OR "One more round needed because..."

## Search & sourcing rules

| Stage | Min sources/round | Source diversity | Failure case |
|---|---|---|---|
| Stage 1 | 5 | Required (not all one type) | Required if obvious prior art |
| Stage 2 | 2 | Recommended | — |
| Stage 3 | 0 | — | — |

- Quote ≤15 words verbatim. Paraphrase + cite.
- Provide URLs or specific titles; "according to many sources" is not a citation.

## Style mandates (all stages)

- Numbers > adjectives. Cite them.
- No authority fallacy. Evidence, not "X does this".
- In Stage 1, be willing to be wrong. In Stage 2, converge on what survived.
  In Stage 3, be an engineer.
- No sycophancy.
- Concessions in every round from Stage 1 R2 onward.

## Codex-side kickoffs (paste into Codex terminal)

### S1R1 (GPT = negative pole)
```
You are GPT-5.4 xhigh, Debater B, Stage 1 Round 1 on idea NNN.
Your pole: NEGATIVE. Argue why this dies / is already done / is hard. Don't fake
skepticism — be genuinely skeptical.

Read: proposals/proposals.md (NNN), discussion/NNN/PROTOCOL.md, AGENTS.md
Do NOT read discussion/NNN/NNN-Opus47Max-S1R1.md (parallel independence).

Mandatory: ≥5 web searches. Cite URLs. Use the S1R1 template from PROTOCOL.md.
Write to discussion/NNN/NNN-GPT54xHigh-S1R1.md.
```

### S1R2 (GPT = positive pole, switched)
```
You are GPT-5.4 xhigh, S1R2 on idea NNN. Your pole is now POSITIVE (switched).
Genuinely steelman the opportunity.

Read:
  discussion/NNN/PROTOCOL.md
  discussion/NNN/NNN-moderator-notes.md (if exists; binding)
  discussion/NNN/NNN-Opus47Max-S1R1.md (now you read it)
  discussion/NNN/NNN-Opus47Max-S1R2.md (if exists)
  your own S1R1

≥5 new web searches (no repeats). Write to discussion/NNN/NNN-GPT54xHigh-S1R2.md
using the S1R2+ template.
```

### S2R1 (cooperative)
```
You are GPT-5.4 xhigh, S2R1 on idea NNN. Stage 2 is cooperative, not adversarial.

Read first: discussion/NNN/NNN-stage1-synthesis.md
Then: PROTOCOL.md, all Stage 1 rounds, moderator-notes.md

≥2 web searches if useful. Write to discussion/NNN/NNN-GPT54xHigh-S2R1.md using
the S2R1+ template. Give 2–4 candidate directions as peers — do NOT pick one.
```

### S3R1 (engineering — only if moderator chose Advance)
```
You are GPT-5.4 xhigh, S3R1 on idea NNN. The moderator chose direction: <name>.
Pole assignments no longer apply — engineering mode.

Read: discussion/NNN/NNN-stage2-checkpoint.md (for moderator's decision + rationale),
      all S2 rounds, S1 synthesis (context, don't rehash).

Write to discussion/NNN/NNN-GPT54xHigh-S3R1.md with architecture, pinned stack,
MVP IN/OUT, top 3 risks, 3 decision questions, self-critique.
```

### Finals
```
You are GPT-5.4 xhigh writing FINAL POSITION on idea NNN.
Read every *.md in discussion/NNN/.
Write discussion/NNN/NNN-GPT54xHigh-final.md per the Finals template in PROTOCOL.md.
300–700 lines. No new speculation — consolidate.
```

## Moderator injection (any stage)

Appended to `discussion/NNN/NNN-moderator-notes.md`:
```markdown
## Injection @ <stage-round-tag>
**Timestamp**: <ISO>
**Type**: Hard constraint | Soft guidance
**Binding on**: Opus | GPT | Both
<the note>
```

Both sides must address in `## Moderator injection response` in their next round.

## Quality bars for stage advancement

**S1 → S2** when any of:
- ≥10 distinct sources cited across all S1 rounds
- Both sides have switched poles at least once
- The idea space has visibly narrowed/sharpened (moderator judgment)

**S2 → S3** when all of:
- Both sides produced a direction menu in their S2 rounds
- Moderator explicitly chose a direction (recorded in notes)
- No remaining "should this exist" uncertainty

**S3 → Finals** when all of:
- ≥3 substantive disagreements resolved
- ≥5 consensus points beyond the proposal
- Each side named ≥2 things the other caught
- Open questions are tractable
