---
name: scope-protocol
description: L3 Scope layer protocol — takes a fully-unpacked idea (post-L2) and produces a product-level PRD candidate menu. L3 starts with L3R0 (human intake), then L3R1 (independent scope candidates, no search), then L3R2 (cross + scope-reality search). Output is stage-L3-scope-<fork>.md with 2-3 candidate PRDs. Human forks one or more into PRD branches for L4.
disable-model-invocation: false
---

# L3 · Scope Protocol

## What L3 is for

L2 produced a rich understanding of one idea. L3's job: turn that understanding
into **concrete product requirements** that L4 (spec/build) can execute on.

L3 is where **human's real-world constraints enter the system**. Time, budget,
personal red lines, platform preferences — these couldn't be part of L1/L2
without poisoning the imagination. Now they come in.

L3 output is a **candidate PRD menu** — 2-3 peer PRD drafts covering the same
idea at different scope cuts. Human picks one (or forks multiple) to proceed
to L4.

## What L3 is NOT for

- **NOT spec/architecture.** No API shapes, no DB schema, no tech stack. That's L4.
- **NOT picking the technology.** Even "should this be a mobile app or web app"
  is a scope decision (product decision) — what framework, what cloud, what DB
  are L4 decisions.
- **NOT implementation estimates.** L4 generates those from tasks.

## The PRD/Spec split (important)

```
L3 output: PRD.md (product view)
  ├─ Who the user is (specific, persona-level)
  ├─ Core user stories (3-7, each executable)
  ├─ Scope IN (what this v0.1 delivers)
  ├─ Scope OUT (explicit non-goals)
  ├─ Success looks like (observable outcomes, numbered)
  ├─ Real constraints (time/budget/platform/compliance)
  └─ UX principles (tradeoffs, not wireframes)

L4 input:  PRD.md  →  L4 output: spec.md, architecture.md, ...
                                 (engineering contracts, tech picks, tasks)
```

**Key property**: a PRD should be readable by someone who has no idea what the
technology will be. A spec is readable by engineers. They're different documents
for different audiences.

## The three sub-phases

### L3R0 · Human intake (required, ~5 min)

**This is human's turn, not the models'.**

The `/scope-start` command uses `AskUserQuestion` to collect real-world
constraints. Questions are designed to be:
- Quick (2-4 choice options by default, or short free text)
- Permissive — every question accepts "not sure yet / let the model suggest"
- Free-form at the end — catches anything the fixed questions missed

Output: `L3R0-intake.md` with structured, annotated answers.

**Critical design principle**: "not sure" is a **first-class answer**, not a
fallback. A human who's honestly uncertain produces better L3R1 rounds than
a human forced to guess. Models see the "?" marks in intake and know to
proactively suggest options for those dimensions.

### L3R1 · Independent scope candidates (no search)

Both models read the L2 explore report + L3R0 intake, then each independently
proposes **2-3 candidate scopes** (candidate PRDs at skeleton level).

Each candidate includes:
- A crisp v0.1 description (1 paragraph)
- The specific user persona it targets
- 3-5 core user stories
- Explicit non-goals
- Honest time estimate given human's constraints
- What success looks like for this cut

**No technical decisions.** Only product-level: what, who, when, why.

### L3R2 · Cross + scope-reality search

Models read each other's L3R1 candidates, then run **scope-reality searches**:

**Allowed**:
- "What do products in this category typically include at v0.1?"
- "What's the minimum viable feature set users expect?"
- "What features are often cut that users don't miss?"
- "What's the typical first-6-months roadmap for products like this?"

**Still forbidden** (these are L4):
- Tech stack queries
- Architecture queries
- Specific implementation approaches

L3R2 output: refined candidate list, with scope-reality validation.

### scope-synthesizer → stage-L3-scope-<fork>.md

After both L3R2 files exist, `scope-synthesizer` produces the candidate PRD menu.

Human reads the menu and chooses:
- Select one candidate → fork into PRD branch → `/plan-start`
- Fork multiple candidates → parallel PRD branches
- Re-scope (need another round)
- Park / Abandon

## L3R0 intake question set

The `/scope-start` command asks these, in order. Each has a "not sure"
equivalent that the model respects.

### Block 1 — Time reality
1. **How soon do you want v0.1 in users' hands?**
   - 1-2 weeks (sharp/small)
   - 3-6 weeks (small SaaS / app)
   - 2-3 months (full product)
   - 3+ months (platform-level)
   - Not sure — scope first, then I'll match time

2. **How many hours per week can you actually put in?**
   - <5 (nights/weekends only)
   - 5-15 (part-time)
   - 15-30 (serious commitment)
   - 30+ (full-time)
   - Varies a lot / not sure

### Block 2 — Audience reach (narrowing)
3. **Which user slice is most interesting to target FIRST?**
   - Shown from the L2 report's candidate user personas
   - Plus "none of those feel right — I'll describe" (free text)
   - Plus "not sure, show me tradeoffs"

### Block 3 — Business model
4. **Rough business model for v0.1?**
   - Free forever (OSS / hobby)
   - Free with optional paid tier later
   - Paid from day 1 (one-time or subscription)
   - Not sure — show me how each shapes scope

### Block 4 — Platform preference
5. **Platform constraint, if any?**
   - Multi-choice (Web / iOS / Android / desktop / CLI / API-only / other)
   - Plus "no preference — pick whatever fits the idea best"

### Block 5 — Red lines (the hard no's)
6. **Is there anything you absolutely WON'T do in v0.1?**
   - Free text, encouraged
   - "None come to mind" is fine — models will propose 3 likely red lines for
     this idea (based on L2 report) and human can accept/reject

### Block 6 — Priorities (shapes tradeoffs)
7. **When two of these conflict, which matters more? (pick 1-2)**
   - Speed to ship
   - Polish / UX quality
   - Technical simplicity
   - Low operating cost
   - Differentiation from existing products
   - Broad appeal
   - Not sure — show me how different priorities lead to different scopes

### Block 7 — Freeform catch-all
8. **Anything I didn't ask but you want me to know?**
   - Multi-line free text
   - Completely optional

## L3R0-intake.md output format

```markdown
# L3R0 · Human Intake · <fork-id>

**Captured**: <ISO>
**Method**: AskUserQuestion interactive

## Block 1 — Time reality

### Target delivery
- ✅ Human answered: <answer>
- OR: ❓ Human not sure — models should propose time scenarios

### Weekly hours
- ✅ / ❓

## Block 2 — Audience
### First slice
- ✅ / ❓ / 💡 (free text)

## Block 3 — Business model
- ✅ / ❓

## Block 4 — Platform
- ✅ / ❓ / 💡

## Block 5 — Red lines
- ✅ Human-named: <list>
- 💡 Models should propose likely red lines based on L2 for human review in L3R1

## Block 6 — Priorities
- ✅ / ❓

## Block 7 — Freeform
<human's free text>

---

## Summary for debaters

**Hard constraints (✅)** — MUST honor in every candidate:
- <list>

**Soft preferences (✅ but negotiable)**:
- <list>

**Unknowns (❓) — models should proactively offer options in L3R1**:
- <list>

**No-go's (red lines)**:
- <list>
```

## L3R1 template (each model, independent)

```markdown
# Idea <fork-id> · L3R1 · <Model> · Scope (no search)

**Timestamp**: <ISO>
**Inputs read**: L2 report, L3R0-intake
**Searches used**: NONE in this round
**Visibility**: did NOT read other debater's L3R1

## 0. How I read the intake

One paragraph: my reading of human's constraints and what it implies for scope.
- Hard constraints I'm respecting: <list>
- Unknowns I'll propose options for: <list>
- Red lines I'll honor: <list>

## 1. Candidate A · "<short name>"

### v0.1 in one paragraph
<what this is, in plain product language>

### User persona (sharpened from L2)
<specific: Sarah, an indie iOS dev with 3 side-apps, wants to...>

### Core user stories (3-5)
- As a <user>, I can <action> so that <outcome>.
- ...

### Scope IN
- <feature>
- ...

### Scope OUT (explicit non-goals)
- <tempting thing we're not doing, and why>
- ...

### Success looks like (observable outcomes)
- <measurable, e.g. "a returning user can accomplish X in <60s">
- ...

### Honest time estimate under human's constraint
- Given human said <hours/week> and <target weeks>: this cut takes ~<n> weeks.
- Confidence: H/M/L. If L, what's uncertain?

### UX principles (tradeoff stances, not designs)
- <e.g. "fast > feature-rich; ship without polish for v0.1 acceptable">
- ...

### Biggest risk to this cut
<one paragraph>

## 2. Candidate B · "<short name>"
(same structure)

## 3. Candidate C · "<short name>"
(same structure, optional — 2 is fine if honest)

## 4. Options for the human's ❓ items

For each unknown in the intake, offer 2 concrete paths:
- Intake said ❓ "business model" → Option 1: free-forever OSS (implies: no
  auth, no billing, simpler scope). Option 2: freemium with a $9/mo paid tier
  (implies: auth from day 1, minimum viable billing).

## 5. Red lines I'd propose (if intake left blank)
Based on the L2 report and my own read of the idea:
1. <likely red line> — because <L2 evidence>
2. ...
3. ...

## 6. Questions that need real user interviews (L3 can't answer)
Things that really do need data from real target users:
- ...
```

**Style**:
- 800-1500 words
- Each candidate must be a genuine **peer** — not a "main + alternatives"
- Time estimates are honest even if painful (don't flatter the human's weekly-hours
  number if the scope doesn't fit)
- No tech/architecture/stack talk

## L3R2 template (cross + scope-reality search)

```markdown
# Idea <fork-id> · L3R2 · <Model>

**Timestamp**: <ISO>
**Opponent's L3R1 read**: yes
**Searches run**: <n>, scope-reality category only

## 1. From opponent's candidates — what sharpened my thinking
- Their candidate X's <aspect> is better than mine because <reason>
- Their candidate Y's <aspect> I'd push back on because <reason>

## 2. Scope-reality searches

For each candidate that survived, what do similar products actually include/exclude?

| Candidate | Comparable product | What they include v0.1 | What they cut | URL |

Paraphrase findings. Cite URLs. ≤15 word quotes.

## 3. Refined candidates

Take the best of both sides' R1 + search verdicts. Produce 2-3 refined candidates.
Each follows the L3R1 candidate format (user / stories / IN / OUT / success /
time / UX / risk) — sharpened.

## 4. The single biggest tradeoff human must decide

Across these candidates, what's the one axis where they really differ? This is
what the human is actually choosing between. Name it clearly.

Example: "Candidates A and B both ship a whiteboard. A prioritizes real-time
collaboration (requires websocket + presence infra, ~2 weeks extra). B ships
async-first and adds real-time in v0.2. The axis is: collaboration model.
Human's priority on 'speed to ship' pushes toward B."

## 5. What I'm less sure about now than I was in R1

Honest concessions. This is not performative humility — genuine updates.
```

**Style**: 600-1000 words, heavy on §2, §3, §4.

## Codex-side kickoff (for inbox)

### L3R1
```
You are GPT-5.4 xhigh, Debater B, L3R1 on idea <target>.

HARD CONSTRAINTS:
- NO web search this round
- DO NOT read discussion/.../L3/L3R1-Opus47Max.md (parallel independence)
- NO tech/architecture/stack content — PRODUCT-level scope only
- Every candidate must be a peer (not "main + alternatives")

Read:
- proposals/proposals.md (root idea)
- discussion/.../<target>/L2/stage-L2-explore-<target>.md
- discussion/.../<target>/L3/L3R0-intake.md  (human's constraints)
- .claude/skills/scope-protocol/SKILL.md
- AGENTS.md

Write discussion/.../<target>/L3/L3R1-GPT54xHigh.md using the L3R1 template.
Produce 2-3 candidate scopes (peers), honest time estimates, proposals for ❓ items,
and candidate red lines if intake didn't name any.
800-1500 words.
```

### L3R2
```
You are GPT-5.4 xhigh, L3R2 on idea <target>.

SCOPE-REALITY SEARCH ONLY:
  Allowed: "what do similar products include/cut at v0.1"
  Forbidden: tech stack, architecture, specific implementations

Read:
- .claude/skills/scope-protocol/SKILL.md
- discussion/.../<target>/L3/moderator-notes.md (if exists; binding)
- discussion/.../<target>/L3/L3R1-Opus47Max.md (opponent)
- your own L3R1
- L3R0-intake (re-check hard constraints)
- L2 report (context)

Run ≥3 scope-reality searches. Cite URLs. ≤15 word quotes.

Write discussion/.../<target>/L3/L3R2-GPT54xHigh.md using the L3R2 template.
Focus on §2, §3, §4.
600-1000 words.
```

## scope-synthesizer output

Structure of `stage-L3-scope-<fork-id>.md`:

```markdown
# L3 Scope Menu · <fork-id> · "<title>"

**Generated**: <ISO>
**Source**: L2 report <fork-id> + L3R0 intake
**Rounds**: L3R1 (both), L3R2 (both)
**Searches**: <n> scope-reality queries

## How to read this menu

This is L3's output: candidate PRDs for <fork-id>. Each is a **peer** — a
different legitimate cut of the idea under your stated constraints. You'll
fork one (or more) into PRD branches for L4:

    /fork <fork-id> from-L3 candidate-X as <fork-id>-<prd-id>

## Intake recap (what we honored)

**Hard constraints**: <list>
**Red lines**: <list>
**❓ items resolved by this menu**: <list — how did candidates handle them>
**❓ items still unresolved**: <list — human must decide>

## The key tradeoff (from L3R2 §4)

<one paragraph: the axis these candidates differ on>

---

## Candidate PRDs

### Candidate A · "<name>" (suggested id: <fork-id>-pA)

**v0.1 essence**: <one paragraph>

**User persona**: <specific>

**Core user stories**:
- ...

**Scope IN**: <list>
**Scope OUT**: <list>
**Success observable**: <measurable>

**Time estimate under your constraints**: <n> weeks
**UX priorities**: <tradeoff stances>
**Biggest risk**: <paragraph>

**Scope-reality verdict (from search)**:
- Comparable: <product at URL>
- What typical v0.1 includes: <paraphrased>
- What this candidate cuts vs norm: <list>
- Net read: <healthy / ambitious / undershooting>

**Best fit for human who**:
<one-paragraph profile of which human would choose this>

### Candidate B · ...

### Candidate C · ... (optional)

---

## Comparison matrix

| Dim | A | B | C |
|---|---|---|---|
| v0.1 weeks | 3 | 6 | 4 |
| User slice | indie dev | team lead | mass |
| Dominant priority | speed | polish | differentiation |
| Biggest risk | <one line> | ... | ... |
| Scope-reality fit | ✅ typical | ⚠ ambitious | ✅ typical |

## Synthesizer recommendation

One of:
- "**Candidate A** most fits the constraints you stated. If you're uncertain,
   pick A; it's recoverable."
- "**Fork both A and B**. They serve different users; parallel PRDs let you
   see which develops better."
- "**Pause** — intake had too many ❓ and the menu feels speculative. Consider
   doing user interviews (per L2 §7) before committing."

## Decision menu (for human)

### [F] Fork one or more candidates into PRD branches
  /fork <fork-id> from-L3 candidate-A as <fork-id>-pA
  # Then: /plan-start <fork-id>-pA (L4 begins)

### [R] Re-scope with new input
  /scope-inject <fork-id> "<steering>"
  /scope-next <fork-id>

### [B] Back to L2 — rethink the idea itself
  /status <fork-id>

### [P] Park
  /park <fork-id>

### [A] Abandon
  /abandon <fork-id>

---

## Fork log
(empty initially; updated by /fork)
```

## Quality bars for advancing L3 → L4

L3 is done enough to hand to L4 when:
- L3R0 intake completed (all 8 blocks, with ❓ allowed)
- Both L3R1 (each proposing 2-3 peer candidates)
- Both L3R2 (with scope-reality search)
- scope-synthesizer produced stage-L3-scope-<fork>.md with ≥2 candidates
- Human picked (via /fork) at least one candidate → PRD branch created
