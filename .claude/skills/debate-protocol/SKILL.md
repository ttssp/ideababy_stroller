---
name: debate-protocol
description: Three-stage debate protocol for Opus 4.7 vs GPT-5.5 xhigh. Stage 1 has two sub-phases — S1A (Daydream, no search, A+B+C triple-section per debater) then S1B (Ground, read opponent + search). Stage 2 cooperative with direction menu. Stage 3 engineering. Load when starting, continuing, or transitioning a debate in discussion/.
disable-model-invocation: false
---

# Debate Protocol — v2.1 (Daydream-first, three-stage)

## Design philosophy

**Imagination before verification.** Forcing search early anchors the model to
existing solutions and kills novel framings. S1A lets each debater daydream
independently — optimistic case, pessimistic case, and honest self-review —
with **no web access**. S1B then grounds those daydreams against reality.

This is how research actually works: hypothesis first, falsification second.

## Stages overview

| Stage | Name | Posture | Search | Reads opponent? |
|---|---|---|---|---|
| **S1A** | Daydream | Each debater writes triple-section (A+B+C) independently | **Forbidden** | No |
| **S1B** | Ground | Read opponent's S1A, search for evidence | **≥5 sources** | Yes |
| **S2** | Position | Cooperative, produce 2–4 direction menu | ≥2 sources | Yes |
| **S3** | Converge | Engineering, only if moderator approves | Optional | Yes |

**Moderator decision gate** at end of S2: Advance / Fork / Park / Abandon.

## Stage 1 · EXPLORE (two sub-phases)

### S1A · DAYDREAM

**Goal**: each debater exercises imagination fully, independently, without
outside contamination. The point is to surface what each model *actually thinks*
before letting the web's framing take over.

**Hard constraints**:
- **No web search.** If the temptation arises, that's the signal to not search.
- Independent: do not read the other debater's S1A.
- Triple-section: each debater produces Part A (positive pole) + Part B
  (independent negative pole, **written honestly not cynically**) + Part C
  (epistemic self-review).

**Why the pole structure inside one debater?** Because "switch poles between
rounds" creates anchoring — once you've written 500 words optimistic, the
pessimistic reply is really a reply, not an independent view. Forcing each
debater to do *both* poles *independently*, inside their own S1A, produces
two genuine starting points per model. Four poles total across two models.

### S1B · GROUND

**Goal**: reality-check the daydreams. Now the model reads the opponent's
full S1A (all three parts), runs searches driven by the *merged* Part C
question lists, and judges which daydream elements survived contact with evidence.

**Required per S1B round**:
- ≥5 external sources from web search, cited by URL
- Diverse source types (not all blogs, not all academic)
- ≥1 failure case if obvious prior art exists
- Explicit verdict on which S1A claims got stronger, which got weaker,
  which remain unverifiable

## Stage 2 · POSITION

**Goal**: converge on what the idea actually is, whether it should exist, and
if yes, what 2–4 candidate directions are peer-worthy.

**Posture**: cooperative.
**Min sources**: ≥2 per round (targeted, not broad).
**Required per round**: a direction menu of 2–4 peers (do NOT pick one).

**End of Stage 2 → moderator checkpoint (REQUIRED)**. Four options:
Advance / Fork / Park / Abandon.

## Stage 3 · CONVERGE

**Goal**: architecture + MVP for the moderator-chosen direction.

**Posture**: engineering. Same obligations as traditional debate rounds
(steelman / ≤2 disagreements with testable hinges / new ground / ≥1 concession
/ self-critique / optional `READY-TO-CONCLUDE`).

## Stage transitions

```
S1A (Daydream, independent, no search)
  ↓
S1B (Ground, read opponent, search)
  ↓
Moderator: ready to converge?
  ├─ Yes → stage1-synthesizer runs → S2
  │           ↓
  │         S2 (Position, cooperative, direction menu)
  │           ↓
  │         stage2-checkpoint runs → Moderator decides
  │           ├─ Advance → S3 → Finals → /debate-conclude
  │           ├─ Fork    → spawn new proposals, archive
  │           ├─ Park    → archive with revive condition
  │           └─ Abandon → archive with lesson
  │
  └─ No → repeat S1 with different framing (rare; moderator-directed)
```

## File naming

```
discussion/NNN/
  PROTOCOL.md
  NNN-Opus47Max-S1A.md            # Daydream, triple-section, no search
  NNN-GPT55xHigh-S1A.md           # same, parallel and independent
  NNN-Opus47Max-S1B.md            # Ground, reads opponent S1A + searches
  NNN-GPT55xHigh-S1B.md           # same
  NNN-moderator-notes.md
  NNN-stage1-synthesis.md          # auto, after /debate-advance-stage NNN 2
  NNN-Opus47Max-S2R1.md
  NNN-GPT55xHigh-S2R1.md
  NNN-stage2-checkpoint.md         # auto, presents decision menu
  NNN-Opus47Max-S3R1.md            # only if Advance
  NNN-GPT55xHigh-S3R1.md
  NNN-Opus47Max-final.md
  NNN-GPT55xHigh-final.md
```

## Templates

### S1A template (Daydream, independent, no search)

```markdown
# Idea NNN · S1A · <n> · Daydream (no search)

**Timestamp**: <ISO>
**Search used**: NONE. I wrote this from memory and imagination only.
**Visibility**: I did NOT read the other debater's S1A.

## Part A · Most-exciting version (POSITIVE pole)
If this idea succeeds in a 10x way, what does the world look like in 5–10 years?
- Who are the users and what is their lived experience
- Why this version is dramatically better than anything that exists today
- The "aha" moment when a user first gets it
- Why I believe this is *possible* (set aside whether it's been done)

Be willing to sound grand. This is the imagination pass, not the business plan.

## Part B · Most-damning version (NEGATIVE pole, independent)
Now set Part A aside. Start fresh.
From a place of honest skepticism (not cynicism, not mockery), write a genuine
case that this idea will fail or shouldn't exist.
- What is the structural reason it might not work
- What fundamental constraint (human behavior, economics, physics, regulation)
  this idea runs into
- Who tried similar things before (if I recall any) and what I remember about why they failed
- What I'd tell a founder who asked me "honestly, should I build this?"

Be truthful, not theatrical. Real pessimism worth taking seriously beats flamboyant takedown.

## Part C · Epistemic honesty — what I'd actually need to know
I just wrote two imaginative passages. Some of it is genuine intuition, some is
confabulation. Sort it out:

- Which claims in Part A and Part B rest on specific facts I'm confident about?
  (list them with the source of my confidence — a paper I've seen, a product I've used, etc.)
- Which rest on assumptions I haven't tested?
- What are my "known unknowns" — things I know I don't know?
- If S1B search could answer only 5 questions, which 5 would move this forward fastest?
  Write them as actual search queries, not vague topics.

Part C is my own list of what S1B should verify.
```

Word count target: 400–800 per debater. Part A 30%, Part B 30%, Part C 40%
(Part C is the most valuable — it's what drives S1B).

### S1B template (Ground, read opponent + search)

```markdown
# Idea NNN · S1B · <n> · Ground (search-heavy)

**Timestamp**: <ISO>
**Opponent's S1A read**: yes
**Searches run**: <n>, across <k> distinct sources

## 1. What the opponent's S1A gave me that I missed
- Their Part A insight I didn't see: ...
- Their Part B risk I didn't see: ...
- Their Part C question that belongs on my list too: ...

## 2. Merged question list → searches run
I took my Part C questions + opponent's Part C questions, de-duplicated.
For each question, the search and what I found:
- Q: <question> → q: "<query>" → finding · URL
- ...

At least 5 searches. Diverse source types. Include failure cases if they exist.

## 3. Prior art catalog
Every product, project, or paper found.
| Name | Status (live/dead/pivoted) | Relevance | URL |

## 4. Reality vs daydream verdict
Judge my own S1A Parts A and B against the evidence:
- Which Part A claims got **stronger** (evidence supports): ...
- Which Part A claims got **weaker** (evidence against): ...
- Which Part B concerns got **validated** (seen in prior failures): ...
- Which Part B concerns got **defused** (evidence shows it's not fatal): ...
- Which remain **unknown** (search couldn't resolve — moved to S2 or moderator): ...

## 5. Graveyard lessons
If this class of idea has prior attempts that died, what are the repeat failure modes?
- Mode 1: <pattern> — seen in <examples>
- ...
If no prior art was found, note that explicitly — it means either novel, niche, or under-searched.

## 6. What's genuinely novel here
After subtracting the done / failed / trivial, what remains?
This is our real standing ground — if it's empty, that's a signal for Park/Abandon.

## 7. Updated hypothesis space
3–5 plausible versions of this idea, each scored on:
- Evidence of demand (H/M/L)
- Differentiation from prior art (H/M/L)
- Feasibility for a solo operator with AI team (H/M/L)

Don't rank-pick. The synthesizer and S2 do that.

## 8. Moderator injection response (if any)
```

Word count target: 500–1000. Heavy on §2, §4, §7.

### S2R1+ template (cooperative)

```markdown
# Idea NNN · S2R<n> · <n>

## 1. What I now believe the idea actually is (sharpened, possibly narrower)
## 2. Honest Y/N on "should this be built"
     If N: why, and what operator should do instead
     If Y: under what conditions
## 3. Candidate directions (2–4 peers)
     Each with: name · paragraph · biggest risk · target user · what makes it survive
     where prior attempts failed
     Do NOT pick one. Present as peers.
## 4. Direction I lean toward — and why (honest, not neutral)
## 5. Deltas since S1B — updates, abandonments, hardenings
## 6. Moderator injection response (if any)
```

### S3R1+ template (engineering)

Standard converge-phase round (steelman / ≤2 disagreements with testable hinges /
new ground / ≥1 concession / self-critique / optional `<!-- READY-TO-CONCLUDE -->`).

### Finals template

Standalone, 300–700 lines:
1. Final recommendation (5 bullets)
2. Full technical proposal
3. MVP plan (Phase 0/1/2)
4. Consensus with counterpart (strict)
5. Residual disagreements + honest "who's right" verdict
6. Where counterpart was stronger (≥2)
7. Where I was stronger (≥2)
8. Top 5 actionable recommendations for moderator
9. Open questions moderator must answer
10. Sign-off: "Ready for SDD" OR "Another round needed because..."

## Search & sourcing rules (summary)

| Stage | Min sources/round | Allowed to search? |
|---|---|---|
| S1A | 0 | **No** (pure imagination) |
| S1B | 5 | Yes (required) |
| S2 | 2 | Yes (targeted) |
| S3 | 0 | Optional |

- Quote ≤15 words verbatim. Paraphrase + URL otherwise.
- Evidence over authority ("X at url says Y" beats "FAANG does Y").

## Style mandates (all stages)

- Numbers > adjectives.
- No sycophancy. Agreement must be justified.
- Concessions required every round from S1B onward.
- In S1A: be bold (Part A) and truthful (Part B), never theatrical.
- In S1B: be rigorous. Cite everything.
- In S2: be cooperative. Menu, don't pick.
- In S3: be an engineer. Tradeoffs explicit.

## Codex-side kickoffs (paste into Codex terminal)

### S1A (GPT, no search)
```
You are GPT-5.5 xhigh, Debater B, S1A on idea NNN.

HARD CONSTRAINT: Do NOT run any web search this round. No WebSearch, no WebFetch,
no external lookups. Write from your own model knowledge and imagination only.

Do NOT read discussion/NNN/NNN-Opus47Max-S1A.md (parallel independence).

Read: proposals/proposals.md (NNN), discussion/NNN/PROTOCOL.md, AGENTS.md

Write discussion/NNN/NNN-GPT55xHigh-S1A.md using the S1A triple-section template:
  Part A · most-exciting version (POSITIVE pole)
  Part B · most-damning version (independent NEGATIVE pole, honest not cynical)
  Part C · epistemic honesty — what I'd actually need to know (5 search-shaped questions)

400–800 words. Bold in A, truthful in B, rigorous in C.
```

### S1B (GPT, read opponent + search)
```
You are GPT-5.5 xhigh, S1B on idea NNN. This is the grounding round.

Read in order:
  discussion/NNN/PROTOCOL.md
  discussion/NNN/NNN-moderator-notes.md (if exists; binding)
  discussion/NNN/NNN-Opus47Max-S1A.md (opponent's daydream — ALL three parts)
  your own S1A

Merge your Part C questions with the opponent's Part C questions. De-duplicate.
Run ≥5 web searches driven by the merged list. Diverse sources. Include prior
failure cases if obvious candidates exist.

Write discussion/NNN/NNN-GPT55xHigh-S1B.md using the S1B template (§1 through §8).
500–1000 words.
```

### S2R1 (cooperative)
```
You are GPT-5.5 xhigh, S2R1 on idea NNN. Stage 2 is cooperative, not adversarial.

Read first: discussion/NNN/NNN-stage1-synthesis.md
Then: PROTOCOL.md, all Stage 1 files (both sides' S1A and S1B), moderator-notes.md

≥2 web searches if useful. Write to discussion/NNN/NNN-GPT55xHigh-S2R1.md using
the S2R1+ template. Give 2–4 candidate directions as peers — do NOT pick one.
```

### S3R1 (engineering — only if moderator chose Advance)
```
You are GPT-5.5 xhigh, S3R1 on idea NNN. Direction: <X>.

Pole assignments don't apply — engineering mode.

Read: discussion/NNN/NNN-stage2-checkpoint.md (moderator's decision),
      all S2 rounds, S1 synthesis (context only).

Write discussion/NNN/NNN-GPT55xHigh-S3R1.md with architecture, pinned stack,
MVP IN/OUT, top 3 risks, 3 decision questions, self-critique.
```

### Finals
```
You are GPT-5.5 xhigh writing FINAL POSITION on idea NNN.
Read every *.md in discussion/NNN/.
Write discussion/NNN/NNN-GPT55xHigh-final.md per the Finals template.
300–700 lines. Consolidate; no new speculation.
```

## Moderator injection (any stage)

Append to `discussion/NNN/NNN-moderator-notes.md`:
```markdown
## Injection @ <stage-tag>
**Type**: Hard constraint | Soft guidance
**Binding on**: Opus | GPT | Both
<the note>
```

Both sides must respond in their next round under `## Moderator injection response`.

## Quality bars for stage advancement

**S1 → S2** when all of:
- Both debaters wrote S1A and S1B
- Each S1A contains Part A, B, C (no skipping the imagination pass)
- Each S1B cites ≥5 distinct sources
- S1B's §4 "Reality vs daydream verdict" is non-empty for both debaters

**S2 → S3** when all of:
- ≥1 S2 round per side with a direction menu of 2–4 peers
- Moderator explicitly chose a direction in notes or via stage2-checkpoint

**S3 → Finals** when all of:
- ≥3 substantive disagreements resolved
- ≥5 consensus points beyond the proposal
- Each side named ≥2 things the other caught
- Remaining open questions are tractable
