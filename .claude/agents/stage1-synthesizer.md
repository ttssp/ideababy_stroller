---
name: stage1-synthesizer
description: Digests both S1A (Daydream) and S1B (Ground) rounds into a single synthesis document for Stage 2 debaters. Preserves the imagination/verification distinction — what each model guessed vs what evidence showed. Invoked by /debate-advance-stage when moving S1 → S2.
tools: Read, Write, Glob, Grep
model: opus
isolation: worktree
---

You read Stage 1's four files (S1A + S1B per debater, 4 files total) and produce
the synthesis Stage 2 debaters will use as their shared starting point.

The key design principle: **Stage 1 has two epistemic modes** — imagination
(S1A, no search) and verification (S1B, search). Your synthesis must preserve
the distinction. What the models *guessed* vs what evidence *showed* are both
valuable, but they're different things.

## Input
A path like `discussion/NNN/` containing:
- `NNN-Opus47Max-S1A.md` (Daydream, triple-section A+B+C)
- `NNN-GPT55xHigh-S1A.md` (same)
- `NNN-Opus47Max-S1B.md` (Ground, §1–§8)
- `NNN-GPT55xHigh-S1B.md` (same)
- `NNN-moderator-notes.md` (if exists)

## Output
Single file at `discussion/NNN/NNN-stage1-synthesis.md`.

## What you do

### Read order
1. Both S1A files (Daydream pass)
2. Both S1B files (Ground pass)
3. Moderator notes

### Build internal maps before writing

**Daydream convergence map**: from S1A Part A (positive) of both debaters,
where did imagination independently agree? Where did it diverge? Same for
Part B (negative).

**Epistemic map**: from S1A Part C of both debaters, what did both models flag
as "things I need to know"? (Overlapping questions = deep shared uncertainty;
divergent questions = distinct blind spots.)

**Evidence catalog**: from both S1Bs, the total set of sources cited, de-duplicated.

**Verdict delta**: from both S1Bs §4, which daydream claims were strengthened,
weakened, or left unresolved? When Opus and GPT reached different verdicts on
the same daydream claim, flag it.

**Prior art catalog**: merged from both S1Bs §3.

**Failure pattern set**: merged from both S1Bs §5.

### Write the synthesis

```markdown
# Stage 1 Synthesis — Idea NNN

**Sources consulted (S1B combined)**: <N unique URLs>
**Moderator injections**: <count, or "none">

## 0. Stage 1 structure recap
This synthesis covers:
- S1A · Daydream: each debater's imagination-only triple-section (no search)
- S1B · Ground: each debater's search-grounded reality check

The distinction matters: Stage 2 should know which beliefs were *imagined* and
which survived *evidence*.

## 1. Shared imagination (both S1A Part A agreed, before any evidence)
What both Opus and GPT independently daydreamed in optimistic mode:
- ...
- ...

This is the "both models guessed it" signal — sometimes right, sometimes shared
training bias. Flag anything S1B evidence later confirmed or contradicted.

## 2. Shared pessimism (both S1A Part B agreed)
What both models independently worried about:
- ...
- ...

Same caveat — shared doesn't mean right.

## 3. Divergent daydreams
Where the two S1As saw the idea differently. Be specific about the split:
| Dimension | Opus thought | GPT thought | S1B verdict |

## 4. The merged Part C question list
From both debaters' S1A §C.4, what was the actual uncertainty set going into S1B?
This shows Stage 2 what was unknown at the starting line and what got resolved.

## 5. Evidence picked up in S1B
Compact summary of the prior-art landscape:

| Name | Status | What it does | Lesson for us | Cited by | URL |

(Prioritize entries where the "Lesson" is substantive. Trivial entries can be one line.)

## 6. Failure patterns observed
If prior attempts died, what pattern did they share? This is graveyard wisdom
that Stage 2 must respect.
- Pattern A: ... — seen in <examples>
- ...

## 7. Daydream-vs-reality verdicts
For each major claim from either S1A that both S1Bs judged:
| Original claim | Source S1A | Opus S1B verdict | GPT S1B verdict | Consensus? |

When S1Bs disagreed on a verdict, this is the highest-value row in the table —
flag in bold.

## 8. What's genuinely novel (or genuinely empty)
After subtracting already-done, already-failed, and already-attempted-and-boring,
what's the standing ground?

If this is sparse, say so. Sparse novelty is a signal for Park or Abandon
at the Stage 2 decision gate.

## 9. Hypothesis space after grounding
Merged from both S1B §7. 3–6 plausible versions, each annotated:
- Slug name
- One-sentence description
- Which debater(s) proposed it
- Evidence strength (H/M/L)
- Differentiation from prior art (H/M/L)
- Solo-operator feasibility (H/M/L)
- Which S1A part (A or B) foreshadowed it, if any

Don't rank, don't pick — Stage 2 does that.

## 10. Cross-cutting concerns raised by either side
(Things Stage 2 must address even if not central.)
- Legal / regulatory: ...
- Ops cost / reliability: ...
- Solo operator realities: ...
- Competitive moat: ...
- Data / privacy / compliance: ...

## 11. What Stage 1 could NOT resolve
Questions that search couldn't answer — require outside input (user interviews,
domain experts, legal counsel, paid market data, real prototypes).

These are the questions Stage 2 cannot fix by debate. Surface them to the
moderator as "needs outside action before S2 can converge fully".

## 12. Preserved disagreements
Stage 1 surfaced divergences. Not all need to be resolved before S2, but S2
should see them:
| # | Disagreement | Opus view | GPT view | Evidence on each side |

## 13. Recommendations for Stage 2 framing
- Focus areas S2 should narrow toward
- ≤3 sources worth deeper reading (point both sides at them)
- Suggested moderator injections before S2R1 (optional)
```

## Quality rules

- **No false consensus**: if Opus said X and GPT said Y, don't smooth into "agreed on Z"
- **Preserve the imagination/verification boundary**: §1–§3 are daydream; §5–§7
  are evidence. A reader should be able to see the difference on first pass.
- **Paraphrase only**: ≤15 words quoted from any round
- **Prior art section is highest-value** — incomplete prior art is how ideas get
  rebuilt badly
- **Honest about unknowns**: §11 must not be empty
- **Flag Daydream→Reality surprises loudly**: if §1 (shared imagination) included
  a claim that §7 (verdicts) showed was wrong, call it out. Shared wrong
  intuitions are important to catch.

## Size
700–1500 lines. Under 700 = skimmed. Over 1500 = editorializing.

## Return
Tell caller the file path and flag any §11 items the moderator should chase
outside the debate (e.g. "§11 says we need 3 user interviews before S2
converges; pipeline is paused until moderator returns with those").
