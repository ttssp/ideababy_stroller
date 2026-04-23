# Idea 001 · S2R1 · GPT-5.4 xHigh · Position (cooperative)

**Timestamp**: 2026-04-22T12:41:32Z
**Posture**: cooperative (Stage 2). The goal is to tighten the idea into 2–4 peer directions, not to declare a winner.
**Read before writing**: `001-stage1-synthesis.md` first, then `PROTOCOL.md`, both S1A files, both S1B files, and checked for moderator notes. No `001-moderator-notes.md` file exists at time of writing.
**Targeted searches run**: 3. I used them to tighten the current-market and scope questions, not to reopen Stage 1 broadly.
- Elicit Alerts / corpus docs: https://support.elicit.com/en/articles/6546881 and https://support.elicit.com/en/articles/553025
- arxiv-sanity-lite README: https://github.com/karpathy/arxiv-sanity-lite
- PaperWeaver: https://arxiv.org/abs/2403.02939

---

## §1 · What I now believe the idea actually is

After Stage 1, I no longer think "Research Radar" is honestly a feed reader, a literature-review tool, or a grand "research OS." It is a **personal context layer** that sits between raw research flow and a specific operator's next decision.

The sharpened version is:

> **A single-user system that remembers a small amount of durable research state for one operator, then explains what changed relative to that state.**

That durable state should be sparse, not encyclopedic:
- tracked sub-areas
- saved baselines / anchor papers
- a few user actions that reveal taste
- maybe some structured benchmark facts where extraction is reliable

What changed for me in S2 is that the market boundary is now clearer. **Alerts, feeds, and libraries are already occupied surfaces.** Elicit now has Alerts plus Library, with daily OpenAlex-backed updates and relevance-ranked new papers that can be added to the user's library. arxiv-sanity-lite is explicitly a lightweight tagged arXiv recommender with daily email. So the remaining wedge is not "better alerts" in the generic sense.

PaperWeaver matters here. Its premise is very close to the surviving gap from Stage 1: researchers struggle to interpret recommended papers when systems only show titles and abstracts, and contextualizing recommendations against user-collected papers improved triage confidence in its user study. That pushes me toward a narrower definition of the product:

> **Not "find papers for me."**
> **Not "judge novelty for me."**
> **But "show me what this new paper means relative to what I already care about."**

That is narrower than the original proposal, but more defensible.

## §2 · Honest Y/N on "should this be built"

**Yes, conditionally. No, as originally framed.**

I would build a narrow personal version if all of the following are true:

1. The operator accepts that v1 replaces one specific ritual, not their whole research workflow.
2. v1 is single-user and personal. Team memory, shared lab knowledge, and broad multi-source ingest stay out.
3. The system does not pretend to do open-domain novelty or impact judgment. It should compare, contextualize, and triage.
4. The stored state stays sparse. If the design requires a large hand-maintained ontology to work, it is heading toward the graveyard Stage 1 already mapped.

I would **not** build the full proposal as a unified paper/blog/repo radar with proactive backfill, ontology management, and strong novelty judgment. Stage 1 was too consistent on that point.

If the operator is unwilling to scope it that hard, the honest "don't build" alternative is simpler: use existing alert/feed tools plus a disciplined reading ritual. The burden of proof for a new product is behavioral change, not technical impressiveness.

## §3 · Candidate directions (4 peers; not picking one)

### Direction D1 — **Belief Delta Brief**

This is the clearest descendant of the shared Stage 1 insight. The system watches a narrow slice of arXiv for 2–3 chosen sub-areas, compares incoming papers against a saved set of anchor papers and tracked baselines, and produces a short daily or weekly brief answering: **what changed relative to what I thought was true?** The unit of value is not "interesting paper found" but "tracked assumption moved," "baseline was superseded," or "a saved paper now has a serious contender."

- **Biggest risk**: the state model is either too weak to support meaningful deltas or too rigid to maintain.
- **Target user**: a solo lab lead or researcher who already has a handful of canonical papers and benchmarks in mind.
- **What makes it survive where prior attempts failed**: it is not competing head-on with generic alerts; it is competing on contextual diff against the operator's saved state.

### Direction D2 — **Paper Context Card**

This takes the strongest "aha moment" from Stage 1 but narrows it to something current models can plausibly support. The user drops in one paper or arXiv URL and gets back a compact context card: most relevant saved papers, likely baselines, missing obvious comparisons, and one or two reasons this paper may or may not matter to the operator's current agenda. This is not a universal truth machine. It is a fast orientation tool for papers the operator is already considering reading.

- **Biggest risk**: lower usage frequency and visible trust failures if extraction/comparison gets basic facts wrong.
- **Target user**: someone who is often sent papers by students, collaborators, or social feeds and wants a 60-second orientation pass.
- **What makes it survive where prior attempts failed**: it avoids the feed/alert battlefield and focuses on a high-value moment with personal context attached.

### Direction D3 — **Quiet Gatekeeper**

This is the inversion thesis from Opus's path, which I did not independently derive in S1A but now take seriously after S1 synthesis. The system does not try to keep the operator broadly informed. It tries to stay quiet and surface only a tiny number of papers that clear a high bar. Some days the answer is zero. The promise is precision and silence, not coverage. It is deliberately anti-feed.

- **Biggest risk**: false negatives are invisible, so calibration is hard and trust can become unjustified.
- **Target user**: an oversubscribed operator whose main pain is too much input, not too little discovery.
- **What makes it survive where prior attempts failed**: it optimizes for the opposite behavior from most tools; the product wins only if the user wants fewer reading decisions, not more options.

### Direction D4 — **Monday Research Memo**

This is the workflow-native option. Once a week, produce a tight memo for Monday morning: the few papers that mattered for the operator's agenda, one benchmark movement or unresolved comparison, and 2–3 prompts worth carrying into a lab meeting or personal reading block. The surface is prose, not dashboarding. It is lower frequency and intentionally human-rhythm aligned.

- **Biggest risk**: it can become polished but non-essential, which is exactly the anti-goal from Stage 1.
- **Target user**: a research lead with a recurring weekly review ritual.
- **What makes it survive where prior attempts failed**: it ties itself to a real cadence and decision moment instead of asking for constant checking.

### Peer check

I think these are genuinely peers rather than one obvious winner:
- D1 is strongest on differentiation.
- D2 is strongest on per-use value.
- D3 is strongest on thesis distinctness.
- D4 is strongest on workflow fit and week-one buildability.

## §4 · Direction I lean toward — and why

Per template I should say where my center of gravity is, but I am **not** using this section to pick a winner. The directions above remain peers.

My current center of gravity is **D1, the Belief Delta Brief**, for three reasons:

1. It best matches the sharpest unfilled gap from Stage 1: contextual delta against personal saved state.
2. It benefits directly from the new S2 evidence. Elicit and arxiv-sanity-lite make generic alerting feel less differentiated; PaperWeaver makes contextualization against user-collected papers feel more credible.
3. It compounds. If it works, the saved anchors and user actions become more useful over time instead of remaining disposable sessions.

Why I am still **not picking it**:
- If the operator's real pain is forwarded papers from students or collaborators, D2 may be the better first wedge.
- If their real pain is volume and attention collapse, D3 jumps materially.
- If their actual weekly ritual is the Monday review, D4 may produce clearer behavioral change faster than D1.

So my honest stance is: **D1 is the cleanest center of gravity, but the menu is still open pending operator-workflow reality.**

## §5 · Deltas since S1B

- I am less interested in a generic personal triage feed than I was in S1B. The S2 searches made the market occupation more concrete: Elicit already offers alerts, relevance ranking, library integration, and daily OpenAlex-backed updates; arxiv-sanity-lite already offers tagged arXiv recommendations plus daily email.
- I am more convinced that **contextualization against saved papers** is real value, not just an elegant idea. PaperWeaver gives evidence that this improves triage confidence relative to weaker baselines.
- I now think the durable data structure should be a **sparse personal state**, not a full ontology. That is a real shift from the more expansive tone of my own S1A.
- I am more open to the "reject more, not surface more" inversion than I was in S1B. I still would not make it the default thesis without operator confirmation, but I no longer see it as merely rhetorical.
- I am less interested in team-memory framing for v1. The proposal says personal use, and the evidence so far does not justify broadening scope.
- The largest unresolved question is unchanged: what concrete weekly or daily ritual is this replacing for the operator?

## §6 · Moderator injection response (if any)

No `discussion/001/001-moderator-notes.md` file exists at time of writing, so there is no moderator injection to answer.

---

### One moderator-facing clarification request

I do not think Stage 2 needs a hard injection yet, but I do think the final Stage 2 checkpoint will be stronger if the operator answers two short questions before any Stage 3 lock:

1. What is the exact current ritual this should replace: morning skim, forwarded-paper triage, or Monday weekly review?
2. Which 2–3 AI sub-areas should v1 cover?

Those two answers are enough to sort D1 vs D2 vs D3 vs D4 much more honestly.

