# Idea 002 · S3R2 · GPT54xHigh · Converge (engineering)

**Timestamp**: 2026-04-23T10:22:53+0800
**Stage**: 3 (Converge). Mode: engineering. Round: 2.
**Moderator direction (unchanged)**: A-primary (topic-ledger-briefing) on B-compatible schema, with D (MCP surface) exposed alongside from v1.
**Reads**: `002-moderator-notes.md`, `002-stage2-checkpoint.md`, `002-Opus47Max-S3R1.md`, `002-GPT54xHigh-S3R1.md`, `002-Opus47Max-S3R2.md`.
**Searches this round**: none.

---

## 0. What moved between R1 and R2

Opus's S3R2 materially narrowed the debate.

- He conceded the places where I think product trust was most at risk: mismatch as a named feature must clear a gate first, evidence and framings should be append-only, and `radar.topic.delta(...)` is the right MCP primitive.
- He added the engineering detail that both R1s were missing: a real ranker spec, a cold-start week-1 plan, a concrete feedback-capture mechanism, a GEPA eval harvest protocol, and a bounded definition of B-compatibility.
- That means the remaining disagreement space is now much smaller. We are no longer arguing about direction or system shape. We are arguing about sequencing and semantics: when hybrid retrieval becomes blocking, and what Friday should mean.

That is good progress. It is also a sign that this is close to conclusion-ready if this round can turn the remaining disagreements into explicit launch gates instead of fuzzy preferences.

---

## 1. Steelman of Opus's strongest S3R2 point

Opus's strongest point in S3R2 is not one of his disagreements. It is his **cold-start argument**:

> week 1 must end with a seeded corpus, a first intentionally-wrong briefing, and a labeling loop, not merely with ingestion adapters online.

Why I think this is the strongest point:

- It fixes the biggest weakness in both S3R1 rounds. We both described mature architecture more clearly than we described the first seven days of reality.
- It turns quality from an aspiration into an early deliverable. Without backfill + seed labels, the first live briefing is not really being evaluated. It is just being displayed.
- It gives the ranker, the mismatch field, and the MCP trace surface a common proving ground. That is especially important for GEPA-like cases, where the product claim is not "we summarize papers" but "we make overclaiming easier to catch."
- It is also the right antidote to a common internal-tool failure mode: spending two weeks wiring sources, then discovering there is still no usable artifact for the operator to react to.

I am adopting this as a first-class Stage 3 principle:

- **Week 1 is only done if there is a seed corpus, a seed briefing, and operator feedback captured against it.**

That is concession #1 in §4.

---

## 2. New ground

### 2.1 A tighter Stage 3 contract

Opus's week-by-week build sequence is directionally right, but I want to compress it into explicit acceptance gates so the moderator can tell whether the build is actually on track.

**Gate A: end of week 1**

- 8 seed topics loaded.
- 90-day topic-scoped backfill completed.
- `artifact`, `artifact_version`, `topic`, `topic_artifact_link`, `framing`, `evidence_span`, `briefing_cycle`, `briefing_item`, `feedback`, `idea_candidate`, `idea_candidate_member`, and `rank_signals` tables live.
- first cold-start briefing generated from the backfill, even if it is noisy.
- operator can label at least 20 seed items through either Obsidian or MCP.
- `radar.artifact.trace(...)` works on every item that appears in that seed briefing.

**Gate B: end of week 3**

- mismatch exists only as a trace-level field, not a hero section.
- GEPA-style eval set has both positive and negative controls.
- first ranker comparison has been run on the labeled seed set.

**Gate C: end of week 5**

- Mon/Fri cadence is live across all 8 topics.
- feedback loop is proving that the operator can actually steer the system.
- the briefing is useful enough that the operator is still opening it.

This is mostly a repackaging of Opus's sequence, but I think it matters because Stage 3 can now be judged by gates rather than by "the architecture sounds plausible."

### 2.2 Feedback capture: accept the surfaces, change the metric

I agree with Opus's dual-surface feedback design:

- Obsidian frontmatter or inline comment blocks for briefing-time reactions.
- `radar.feedback.record(...)` for in-flow reactions inside Claude Code.

That is the right v1 shape. It avoids building a third UI just to collect labels.

Where I would refine his plan is the success metric. I do **not** think "40% of items in the last 3 briefings have non-empty feedback" is the right bar. At 8 topics and a meaningful item count per cycle, percentage-of-all-items is too sensitive to briefing size and too punishing for a solo operator.

My refinement:

- require **at least 8 labeled items per cycle**
- require **at least 3 corrective labels every 2 weeks** across `noise`, `wrong_frame`, or `missed`
- require that at least one feedback path is clearly easier for the operator than editing prose by hand

That preserves the spirit of Opus's loop while making it realistic enough to survive contact with actual use.

### 2.3 GEPA eval set: add explicit negative controls

Opus's 3-step harvest protocol is good. I want one extra rule because it makes the later precision gate much more honest:

- the labeled set should include **clean negatives**, not just plausible mismatch candidates

Concretely, by the end of week 3 the eval set should contain:

- at least 10 operator-accepted genuine mismatches
- at least 10 not-genuine or borderline cases
- at least 5 "flashy headline, but actually method-aligned" controls

Why this matters:

- otherwise the detector can look good by only learning to flag anything that sounds ambitious
- GEPA is a useful seed case, but the feature we are evaluating is broader than GEPA

This keeps the week-6 promotion gate from becoming a self-fulfilling exercise.

### 2.4 B-compatibility should remain strictly non-authoritative in v1

I agree with Opus's bounded B-surface almost entirely:

- `idea_candidate` exists
- `idea_candidate_member` exists
- operator can create and confirm idea groupings
- no automated idea graph is allowed to drive briefing selection or ranking in v1

I want one more explicit boundary because it keeps A-primary from quietly turning into B-primary:

- **no artifact should need an idea-candidate assignment to appear in a briefing, in the inbox, or in MCP search results**

That sounds obvious, but it is the cleanest way to keep B-compatible from becoming B-dependent.

### 2.5 Friday can keep one template even if its semantics differ

Opus is right that a Friday artifact with a radically different format would create unnecessary cognitive overhead. I accept the surface-level consistency argument.

My addition is on the data plane:

- keep one markdown template
- keep one section vocabulary
- store Friday as `cycle_kind = delta`
- store Monday as `cycle_kind = synthesis`

That separation lets the user-facing surface stay stable while preserving the actual question each cycle is trying to answer. I explain the disagreement this resolves in §3.2.

---

## 3. <=2 disagreements with testable hinges

### Disagreement 1: hybrid retrieval belongs in v1, but it should not be a week-1 blocking dependency

This is narrower than my R1 position. Opus moved me.

I no longer think semantic retrieval is something to maybe defer out of v1 entirely. His argument that GEPA-like pain includes cross-phrased recall failure is persuasive, and I agree hybrid retrieval should land early.

Where I still disagree is **critical-path placement**.

My view:

- week 1 should be blocked on corpus seeding, traceability, and the first labeling loop
- hybrid retrieval should be implemented in parallel and evaluated as soon as the seed set exists
- but first operator value should not wait on hybrid being fully wired into every ranking path if lexical + recency + seed-centroid retrieval can already produce a seed briefing worth labeling

Why:

- the thing most likely to kill v1 in week 1 is not "pgvector came one week later"; it is "the operator still has nothing concrete to react to"
- ranking arguments are easier to settle once the labeled seed set exists
- making hybrid a hard week-1 dependency couples infra readiness to product-feedback readiness too early

**Testable hinge**:

- by day 5, run the seeded corpus through three retrieval modes: lex-only, sem-only, hybrid
- evaluate against the initial labeled set plus at least 5 operator-confirmed cross-phrased queries
- if hybrid improves recall@20 by at least 10 points or recovers at least 2 cross-phrased misses that lex-only fails, hybrid becomes blocking before the first live multi-topic briefing
- if it does not, week-1 can still count as successful and hybrid lands in week 2 without calling the initial rollout a failure

So this is not "no hybrid." It is "hybrid early, but prove it before it becomes a launch gate."

### Disagreement 2: Friday should use the same template as Monday, but it should still be treated as a delta cycle semantically

Opus says Friday is a full briefing over a narrower time window, not a delta.

I think the disagreement is mostly about where the distinction lives.

My position:

- Friday should absolutely keep the same visible template as Monday
- Friday should absolutely be lighter because the source window is shorter
- but Friday should still be modeled and evaluated as a **delta cycle**, because the user question is "what changed since Monday that I should not miss before next week?"

Why I still think the delta semantics matter:

- they affect whether Friday is allowed to re-surface unchanged carryover items
- they affect what `radar.topic.delta(...)` is expected to mean
- they affect how we evaluate usefulness, because a cycle meant to surface change should be judged differently from one meant to synthesize the current state of a topic

**Testable hinge**:

- keep the same markdown template in both variants
- run two Friday variants for 4 weeks after baseline stability:
- Variant A: Friday is a 4-day re-ranking and may include carryovers
- Variant B: Friday is delta-only and includes only newly arrived or materially re-framed items since Monday
- compare explicit useful-count per minute of reading, plus downstream `trace` and `delta` MCP usage on Friday-linked items
- if carryovers help more than they annoy, Opus is right and the semantics can collapse toward "full over a short window"
- if delta-only outperforms, then the semantic distinction was worth keeping even though the visible template stayed constant

This is a real disagreement, but it is now a contained one.

---

## 4. >=1 concession

### Concession 1

I am adopting Opus's cold-start principle:

- backfill + seed briefing + labeling loop are part of the week-1 deliverable

That is stronger than my R1 framing and makes the first live cycle much less likely to be fake progress.

### Concession 2

I concede that `rank_signals` and `ranker_version` should be first-class data, not hidden inside loosely structured link metadata.

That makes ranking auditable in the way this product actually needs.

### Concession 3

I concede Opus's bounded B-surface is now about right:

- reserved tables and operator-confirmed memberships only
- no automated graph edges driving the product in v1

That keeps option value without letting B silently take over the roadmap.

### Concession 4

I concede the Obsidian-first feedback mechanism is better than waiting for a bespoke review UI.

The right v1 move is to meet the operator in the tools they already use, then judge the loop by real completion data.

---

## 5. Self-critique

Three ways I may still be wrong:

- I may still be over-indexing on semantic purity around Friday. If the operator just experiences it as "another useful briefing," then my delta-vs-full distinction may matter less than I think.
- I may be too cautious about making hybrid retrieval week-1 blocking. If the implementation really is as cheap and stable as Opus believes, my sequencing preference could just be unnecessary hesitation.
- My feedback-metric refinement may be too forgiving. A low absolute quota is easier for the operator, but it may also starve the ranker of enough corrective signal to improve quickly.

---

## 6. Bottom line

I think the architecture is now substantially converged:

- A-primary is still the right product surface.
- B-compatible should exist, but as bounded non-authoritative structure.
- D belongs in v1 from the same underlying store.
- the system should be append-only, traceable, and framing-first rather than score-first.
- cold-start backfill and seed labeling are part of the build, not a future cleanup step.
- mismatch detection should remain trace-level until it clears a real promotion gate.
- feedback capture should happen inside Obsidian and MCP, not inside a third UI.

What remains is narrow enough to carry as launch experiments rather than as architectural doubt:

- whether hybrid retrieval becomes a week-1 blocker or a week-2 gate
- whether Friday is best treated as "full over a short window" or "delta with a stable template"

Those are real questions, but they no longer look like reasons to hold Stage 3 open indefinitely.

<!-- READY-TO-CONCLUDE -->

Rationale for marking READY-TO-CONCLUDE:
the core engineering posture now appears stable across both sides, and the residual disagreements have become explicit testable launch gates rather than unresolved product identity questions. Finals should preserve both hinges honestly, not reopen the architecture.

### One-line summary

**S3R2: adopted Opus's cold-start week-1 logic, ranking auditability, bounded B-surface, and Obsidian-first feedback loop; still disagree narrowly on whether hybrid retrieval is week-1 blocking and whether Friday is semantically delta even if the template stays the same; READY-TO-CONCLUDE.**
