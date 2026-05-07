---
name: explore-protocol
description: L2 Explore layer protocol — once human picks an inspired direction (or skips L1), L2 deeply unpacks that single idea's value, novelty, utility, extensions, and limits. Still NOT for tech/feasibility (those are L3/L4). Two rounds — Daydream then Cross+Validate. Load when starting, continuing, or transitioning L2.
disable-model-invocation: false
---

# L2 · Explore Protocol

## What L2 is for

L1 produced a menu of **possible directions**. Human picked one (via /fork) and
forked it into its own sub-tree (e.g. 001a). L2's job is to take that single
idea and **unpack it deeply** — what it really is, what's novel about it, what
it delivers, what it could extend into, what natural limits it has.

Think of L2 as writing **the long-form essay about this idea**. After L2,
human should have a deep, multi-faceted understanding of what they're looking at.

## What L2 is NOT for

- Still **NOT** for technical decisions (architecture, stack, cost) — those are L4
- Still **NOT** for committing to scope (that's L3)
- Not for picking the "best" version — L2 produces a rich understanding,
  L3 turns it into a concrete what-to-build

## Skip-mode special case

If human used `/inspire-start NNN --mode=skip`, L2 must include an extra
section in L2R1: **"Alternative framings I considered before settling on this one"**.
This folds L1's value into L2 — the human still benefits from the "could have
been other things" perspective even though L1 wasn't formally run.

## L2R1 template (Daydream — no search, deep unpacking)

```markdown
# Idea NNN[/fork-id] · L2R1 · <Model> · Explore (no search)

**Timestamp**: <ISO>
**Searches used**: NONE in this round.
**Visibility**: I did NOT read the other debater's L2R1.
**Origin**: <if forked, reference the L1 candidate; if skip mode, note that>

## 0. (Skip mode only) Alternative framings considered
If this comes from /inspire-start --mode=skip, write 3-4 alternative ways to
read this proposal that you considered but didn't pursue. One paragraph each.
Why didn't you pursue them? What would change your mind?

## 1. The idea, unpacked
3-5 paragraphs. Take the inspired direction (or original proposal) and walk
around it from multiple angles:
- Who exactly are the users (be specific — "indie iOS devs maintaining 1-3 apps"
  beats "developers")
- What's their daily life like before they have this
- What's their daily life like after
- What's the "aha" moment — the first 30 seconds of using it
- What does long-term mastery look like — the user 6 months in
- What does the world look like if a million people use this

Don't summarize the proposal back. **Develop it**. Add specificity. Find the
texture.

## 2. What's genuinely novel
Where does this NOT just recombine existing patterns? What's the real
"haven't seen this before" core?

If you can't find a real novelty — say so. "The novelty is in execution, not
concept" is a valid (and common) finding. So is "honestly, this isn't novel,
but it's underserved" or "the core is well-known, but the slice is new."

## 3. Utility — what can users actually DO with this?
Concrete usage scenarios. Not features — *usage*. Three examples:
- A specific user, in a specific situation, doing a specific thing.
- What did they accomplish? What problem went away?
- What do they tell their friend afterward?

## 4. Natural extensions
If v0.1 ships and works, what are the obvious next-2-years extensions?
- Adjacent features users would request
- Adjacent user segments that would notice
- Adjacent products that could coexist (a family of related tools, or a platform play)

Not aspirational ("eventually we'll be a unicorn"). Concrete ("the obvious v0.2
is X because users hitting Y will ask for it").

## 5. Natural limits
What this idea **cannot** be, or what it shouldn't try to be:
- Use cases that are tempting but a bad fit
- User segments that look adjacent but are different
- Scope creep traps
- Cultural / temporal / geographic limits

Knowing the limits sharpens the idea.

## 6. Three honest questions about this idea
Things that, if you got a clear answer, would significantly change how you
think about this. (These seed the L2R2 search.)

1. ?
2. ?
3. ?
```

**Style**:
- 700-1300 words total
- §1 and §3 are the heart — invest most words here
- Specific > abstract everywhere
- No tech / feasibility / cost / architecture talk
- Paraphrase if recalling external info; ≤15 words verbatim if quoted

## L2R2 template (Cross + value-validation search)

Same value-validation search rules as L1R2: prior art, demand signals, failure
cases. **Forbidden**: tech stack, architecture, cost, feasibility queries.

```markdown
# Idea NNN[/fork-id] · L2R2 · <Model> · Cross + Value Validation

**Timestamp**: <ISO>
**Opponent's L2R1 read**: yes
**Searches run**: <n>, value-validation only

## 1. From opponent's L2R1, what sharpened my thinking
≥3 specific things from opponent's R1 that genuinely added to your view.
Not summary — what *changed* in your understanding.

## 2. Where I'd push back on opponent's L2R1
Up to 3 specific points where you disagree. Be honest, not contrarian.

## 3. Search-based reality check
For each of the 3-6 concrete claims either side made about the idea (about
demand, about prior art, about user behavior), what does the world say?

| Claim | Source side | What I searched | What I found | Verdict |

Cite URLs.

## 4. Refined picture
Now, after R1 and search, write a sharpened version of the idea (1-2 paragraphs).
This may be:
- Narrower than R1 (focused down)
- Slightly different framing (the search revealed the real interesting cut)
- More confident (the search confirmed)
- Less confident (the search undermined; honest if so)

## 5. Open questions that L2 cannot answer
Things only L3 (real scope decision with human input) or L4 (technical reality)
can resolve. Surface them so L3 starts informed.

## 6. Three things I'd want a real user interview to ask
If we could interview 5 target users right now, what 3 questions would tell us
the most? (These often signal "we've gone as far as imagination can go — need
real-world input now".)
```

**Style**: 600-1100 words. Heavy on §3 and §4.

## explore-synthesizer output (stage-L2-explore-<fork-id>.md)

After both L2 rounds, the `explore-synthesizer` agent runs and produces
`discussion/.../<fork-id>/L2/stage-L2-explore-<fork-id>.md`.

This is the deep "essay about this idea" the human reads to decide whether
and how to proceed to L3.

Structure:

```markdown
# L2 Explore Report · <fork-id> · "<title>"

**Generated**: <ISO>
**Source**: forked from <root> L1 #<n>  OR  direct from /inspire-start --mode=skip
**Source rounds**: L2R1 (both), L2R2 (both)
**Searches run**: <n> across <k> distinct sources

## How to read this

This is the L2 layer's deep dive on idea <fork-id>. Unlike the L1 menu (which
was many shallow possibilities), this is one rich understanding. After reading,
you should know:
- What this idea genuinely is, in detail
- Why it's worth considering (or honest reasons to reconsider)
- What it could grow into and what it shouldn't try to be
- What questions you must answer (or get user input on) before scoping it in L3

## Executive summary
3-5 bullets. The synthesized essence.

## 1. The idea, fully unpacked
Synthesized from §1 of both L2R1s + refinements from L2R2 §4. 4-8 paragraphs.

## 2. Novelty assessment
What's genuinely new vs recombined-existing. Synthesizer's honest verdict, not
diplomatic. If novelty is thin, say so — and explain whether that matters
("execution-driven" can still be a great idea).

## 3. Utility — concrete usage scenarios
3-5 specific user scenarios from L2R1 §3 (both sides). Pick the most evocative
ones. Don't include weak scenarios just to fill space.

## 4. Natural extensions (the long shadow)
The 2-year possibility space if v0.1 succeeds. Synthesized from §4 of both R1s.

## 5. Natural limits (the protective fence)
What this should NOT be. From §5 of both R1s.

## 6. Validation status
What did L2R2 search find?
- Prior art landscape (table)
- Demand signals (table)
- Failure cases (table)
- Net verdict on "should this exist": <Y / Y-with-conditions / unclear / N>

## 7. Open questions for L3 / for users
Synthesized from §5 + §6 of both L2R2s. These are what L3 must address (or
what user research must answer first).

## 8. Decision menu (for the human)

### [S] Scope this idea — proceed to L3
The idea is ripe. Move to scope decisions:
```
/scope-start <fork-id>
```
(L3 will pull in your real constraints, preferences, available time/budget.)

### [F] Fork another L2 angle from this same idea
You see a sharper cut of <fork-id> after reading this report:
```
/fork <fork-id> from-L2 <new-angle> as <new-id>
```

### [B] Back to L1 menu — pick another inspired direction
This direction was OK but the menu had others worth trying:
```
/status <root>  (see the L1 menu and other forks)
```

### [R] Re-explore with new input
Inject something L2 didn't consider, run L2R3:
```
/explore-inject <fork-id> "<your input>"
/explore-next <fork-id>
```

### [P] Park this fork
Preserve all artifacts, decide later.
```
/park <fork-id>
```

### [A] Abandon this fork
Evidence in L2 says don't continue this direction (siblings still active):
```
/abandon <fork-id>
```

---

## Fork log
(updated by /fork command for any sub-forks of this L2)
```

## Codex-side kickoff prompts

### L2R1 (Daydream)
```
You are GPT-5.5 xhigh, Debater B, L2R1 on idea NNN[/fork-id].

HARD CONSTRAINTS:
- NO web search this round
- DO NOT read discussion/.../L2/L2R1-Opus47Max.md (parallel independence)
- NO tech / architecture / cost / feasibility content (those are L3/L4)

Read in order:
- proposals/proposals.md (entry NNN)
- if forked: discussion/NNN/.../FORK-ORIGIN.md and the source L1 menu's
  selected candidate
- .claude/skills/explore-protocol/SKILL.md
- AGENTS.md

Write discussion/.../L2/L2R1-GPT55xHigh.md using the L2R1 template (sections 0
[skip-mode only], 1-6). 700-1300 words. Heavy on sections 1 and 3.
```

### L2R2 (Cross + value validation)
```
You are GPT-5.5 xhigh, L2R2 on idea NNN[/fork-id].

VALUE-VALIDATION SEARCH ONLY:
  Allowed: prior art / demand signals / failure cases
  Forbidden: tech stack / architecture / cost / feasibility

Read:
- .claude/skills/explore-protocol/SKILL.md
- discussion/.../L2/moderator-notes.md (if exists; binding)
- discussion/.../L2/L2R1-Opus47Max.md (opponent — all sections)
- your own L2R1

Run ≥3 value-validation searches. Cite URLs.

Write discussion/.../L2/L2R2-GPT55xHigh.md using the L2R2 template (§1-§6).
600-1100 words. Heavy on §3 and §4.
```

## Quality bars for advancing L2 → L3

L2 is done enough to scope when:
- Both L2R1 (deep unpack, ≥700 words each)
- Both L2R2 (cross + validation, ≥3 searches each)
- explore-synthesizer produced stage-L2-explore-<fork-id>.md
- Human read it and chose to proceed (not Park or Abandon)
