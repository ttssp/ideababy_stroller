# Idea 002 · S3R3 · Opus 4.7 Max · Converge (engineering)

**Timestamp**: 2026-04-23
**Stage**: 3 (Converge). Mode: engineering. Round: 3.
**Moderator direction (unchanged)**: A-primary (topic-ledger-briefing) on
B-compatible schema, D (MCP surface) exposed alongside from v1.
**Reads**: `002-Opus47Max-S3R2.md` (own prior round),
`002-GPT54xHigh-S3R2.md` (opponent's round — close read),
`002-moderator-notes.md`, both S3R1s, `002-stage2-checkpoint.md`.
**Searches this round**: 0 (engineering-mode; protocol allows optional).

---

## 0. What moved between R2 and R3

GPT's S3R2 did three things that matter for this round:

1. **Reframed Gate A/B/C as explicit moderator-readable launch gates.** This
   is a better artifact than my week-by-week sequence; gates are testable,
   weeks are only descriptive. Adopted in §2.
2. **Pushed back narrowly on hybrid-retrieval sequencing** — not on whether
   we build it, but on whether it's week-1 blocking. GPT's argument (Gate A
   is about "operator has something to react to," not infra breadth) is
   correct. I move. See §1 + §5.
3. **Refined Friday semantics with `cycle_kind` on the data plane while
   keeping Monday's template on the UI plane.** This is the right resolution
   of our Disagreement 2 and closes it. Adopted in §1 + §5.

GPT marked **READY-TO-CONCLUDE** in their R2. I agree the architecture is
stable. I also agree the remaining hinges are launch-gate experiments, not
reasons to hold Stage 3 open. After this round, we have one converging pass
from each side on the R2 concessions; I mark **READY-TO-CONCLUDE** as well
(see bottom).

---

## 1. Steelman of GPT's strongest S3R2 point

GPT's strongest point in R2 is this, from §3 Disagreement 1:

> "the thing most likely to kill v1 in week 1 is not 'pgvector came one week
> later'; it is 'the operator still has nothing concrete to react to'. Making
> hybrid a hard week-1 dependency couples infra readiness to product-feedback
> readiness too early."

Why this is stronger than my R2 position:

- **My R2 argument was directionally right but scope-confused.** I argued
  that hybrid retrieval is production-ready in 2026 and that the recall
  promise is structurally unhonorable without it. Both claims are true. But
  neither claim forces the infrastructure into week 1 as a *blocking*
  deliverable. "Hybrid lands in v1" and "hybrid lands in week 1" are
  different claims; I conflated them.
- **Gate A is about the labeling-loop existing, not about every retrieval
  path being perfect.** A seed corpus ranked by lex+recency+centroid produces
  an intentionally-wrong first briefing (my R2 §2.5 said exactly this). The
  whole point of the cold-start briefing is that it surfaces items for
  labeling — not that it's well-ranked on day 7. GPT is right that adding
  "and hybrid is live" to week 1 is a false gate: it makes infra readiness
  block product-feedback readiness.
- **The evaluation-gate version is cleaner than the infra-gate version.** If
  hybrid doesn't beat lex-only on the seeded eval (GPT's day-5 test, my R2
  §2.9 harvest), we wouldn't want it in v1 anyway. The gate GPT proposes
  — "hybrid becomes blocking before first live multi-topic briefing IF it
  clears the eval" — is the thing I was trying to express. GPT's framing
  is just more honest about what the condition actually is.

**I adopt this.** Concession #1 in §4. Concrete change: the week-1 Gate A
deliverables (GPT R2 §2.1) are preserved as-is. Hybrid retrieval lands in
**week 2**, evaluated against the week-1 seed labels, and becomes a
**Gate A.5 blocker for week 3's second-pass framing** only if it clears
the eval. If it doesn't, it's not in v1 — same outcome as my R2's "rip it
out" fallback, just with a cleaner gate.

Secondary point worth adopting: GPT's **`cycle_kind` on the data plane with
template consistency on the UI plane** (R2 §2.5). My R2 argued Friday =
full-briefing over a narrow window; GPT argues Friday = delta-semantic
cycle with the same template. These are **not incompatible**. The
`cycle_kind ∈ {synthesis, delta}` column is additive — the template
renders the same sections, but `radar.topic.delta(topic, since_cycle)`
knows to compute "what changed since cycle X" differently depending on
whether cycle X was a `synthesis` or `delta` cycle. Both our R2 positions
survive under GPT's refinement. Concession #2 in §4.

---

## 2. New ground — minimal

This round is mostly convergence. Two items of genuinely new ground, both
small:

### 2.1 Gate A.5 — hybrid retrieval decision gate (week 2)

Inserting between GPT's Gate A (week 1) and Gate B (week 3):

**Gate A.5 (end of week 2, blocking for week-3 framing pass)**:
- Hybrid retrieval (BM25 + pgvector + RRF fusion, via ParadeDB or
  pg_textsearch depending on operator's Postgres tier) implemented end-to-end
  against the week-1 seed corpus.
- Three-way eval run: lex-only, sem-only, hybrid — against the labeled seed
  items from Gate A + operator-confirmed cross-phrased queries.
- **Decision rule**:
  - If hybrid recall@20 ≥ lex-only + 10pp OR recovers ≥ 2 cross-phrased
    cases lex-only misses → hybrid is the default ranker signal, and the
    semantic-retrieval pipeline is frozen as v1-blocking.
  - If hybrid does not clear that bar → v1 ships with lex-only + centroid
    retrieval; pgvector stays installed but unused by the ranker;
    re-evaluated in v1.5 with more data.
- Either outcome is a successful gate. The gate's purpose is *to decide*,
  not *to force hybrid to win*.

This is the cleanest expression of GPT's R2 Disagreement 1. It converts
my R2 "hybrid from week 1" assertion and GPT's "hybrid gated on eval"
into a single explicit gate with a concrete metric and a pre-committed
response to either outcome.

### 2.2 Friday semantics — `cycle_kind` column + delta-eligibility rule

Adopting GPT's R2 §2.5 refinement. The schema change (additive):

```text
briefing_cycle
  id              uuid
  cycle_date      date
  cycle_kind      'synthesis' | 'delta'    -- NEW column
  topic_id        uuid
  ranker_version  text
  created_at      timestamptz
```

Behavioral rule for the Friday delta:
- A Friday `delta` cycle draws from `briefing_item` candidates where:
  - `first_seen_at >= prev_monday_synthesis.created_at`, OR
  - an `artifact_version` or `framing` row has been added since the
    previous Monday synthesis
- Carryover items (items that appeared in Monday and would re-rank high
  on Friday) are **tagged** in the briefing as carryover but may appear
  when `radar.topic.delta(...)` judges them materially re-framed.
- The 4-week A/B experiment GPT and I both proposed now tests
  **the delta-eligibility rule**, not the template.

This resolves our Disagreement 2 fully. The remaining question — "are
carryovers helpful or annoying on Friday?" — is the experiment itself,
not a pre-launch decision. My R2 position ("Friday = full over 4-day
window") and GPT's R2 position ("Friday = delta-semantics") both
survive as the two variants of the experiment.

### 2.3 Two additions to GPT's Gates A/B/C

GPT's §2.1 gates are the right artifact. Two extensions, small but load-
bearing:

**Gate A (week 1) additions**:
- Add: `ranker_version = "v0.1-coldstart"` committed to every
  `briefing_item` row from the seed briefing. Reason: even the wrong
  first briefing must be reproducible for later postmortems.
- Add: `cost_telemetry` surfaces real tokens + dollars for the seed
  briefing. Reason: the "GLM vs Haiku" and "does cheap triage hold
  quality?" decisions both depend on early cost observation, not
  week-5 observation.

**Gate B (week 3) addition**:
- GPT's §2.3 rule: eval set = ≥10 genuine mismatches + ≥10 not-genuine +
  ≥5 "flashy headline, method-aligned" controls. I adopt this fully —
  the negative and control categories are how we prevent the week-6
  promotion decision from being a self-fulfilling exercise. Named in
  the gate explicitly.

**Gate C (week 5) addition**:
- Make GPT's refined feedback metric the explicit gate bar:
  `≥ 8 labeled items per cycle AND ≥ 3 corrective labels (noise /
  wrong_frame / missed) per 2 weeks`. My R2's 40% target was ungrounded;
  GPT's absolute quota is more honest. Concession #4 below.

---

## 3. ≤2 disagreements with testable hinges

Both my R2 disagreements have now collapsed into explicit gates (§2.1,
§2.2). I have **no remaining disagreements** with GPT on the engineering
plan.

To honor the protocol's "≤2" constraint — which reads as "up to two," not
"at least one" — I'll note two **narrow residual uncertainties** that are
not disagreements with GPT but are worth flagging as experiments Stage 3
leaves open, not questions Stage 3 must answer:

### Residual uncertainty 1 · Triage-tier economics assumption

**Status**: not a disagreement with GPT. Both rounds of R2 converged on
"Haiku first-pass + Sonnet briefing" as v0, with GLM/MiniMax cost-
optimization deferred until the Haiku cost line is observed. My R2
Concession #4 and GPT's R2 adoption of it are the same.

**Residual uncertainty**: the cost estimate ($6/week from my R2 §2.5)
assumes 2,000 artifacts/week after topic-keyword pre-filter. If the
real post-filter number is 3,000–4,000/week (plausible — my pre-filter
estimate is cited as ±2x in R2 §6 self-critique), the Haiku second-pass
scales linearly and we hit ~$15–$25/week. Still fine for a solo operator,
but enough to trigger the GLM/MiniMax switch earlier than week 4.

**Testable hinge (already scheduled, not new)**: end-of-week-2 cost audit
(part of Gate A.5's data collection). If observed weekly run-rate exceeds
$20, switch triage to GLM-4.6 and re-run the Gate B eval with the
downgraded first-pass. Cost escalation is reversible in ~1 day.

### Residual uncertainty 2 · Feedback-capture completion rate

**Status**: not a disagreement with GPT. R2 converged on GPT's absolute
quotas replacing my percentage target.

**Residual uncertainty**: GPT's own R2 self-critique flagged this — the
new lower quota may starve the ranker. I agree with the flag. But the
experiment structure (Gate C checks quota at week 5; ranker-tuning
pass happens after Gate C) lets us revise upward if the actual completion
rate is higher than the quota demands.

No new hinge — Gate C's structure already handles it.

---

## 4. Concessions (≥1)

**Concession #1**: Adopted GPT's week-1-blocking critique of hybrid
retrieval (§1). My R2 argued hybrid-from-day-1; GPT correctly separated
"hybrid in v1" (agreed) from "hybrid blocks week 1" (disagreed). The
Gate A.5 framing (§2.1) is GPT's position with a concrete metric.

**Concession #2**: Adopted GPT's `cycle_kind` column + template-consistency
resolution (§2.2). My R2 was right about template consistency; GPT was
right about semantic distinction. Both survive under the refined schema.

**Concession #3**: Adopted GPT's ≥10+≥10+≥5 labeled-set composition rule
(§2.3 / Gate B). My R2 eval harvest only required ≥10 genuine cases; GPT's
addition of not-genuine + controls prevents the mismatch feature from
over-promoting itself in the week-6 eval.

**Concession #4**: Adopted GPT's absolute-quota feedback metric replacing
my 40%-of-items-in-last-3-briefings target (§2.3 / Gate C). My self-
critique in R2 §6 explicitly flagged the 40% number as a guess; GPT's
quotas are better-calibrated to a solo operator's realistic labeling
bandwidth.

**Concession #5**: Adopted GPT's "no artifact should need an
`idea_candidate` assignment to appear in briefing / inbox / MCP search"
boundary rule (their R2 §2.4). My R2 bounded the B-surface but didn't
make this specific invariant explicit. Without it, B-compatibility could
silently slide into B-dependence. Added to the v1 spec.

---

## 5. Self-critique

Three under-confidences I want on the record before finals:

1. **The Gate A.5 eval may not have enough cross-phrased queries to
   produce a statistically clean decision.** §2.1 says "≥ 2
   cross-phrased cases recovered" as one of the pass conditions. If the
   operator only confirms 3–4 cross-phrased queries on the seed corpus,
   +/- 1 case in the recovery count flips the decision. This is the
   same statistical-power concern I raised in R2 §6. The realistic
   mitigation is that operator-confirmed cross-phrasing *grows* over
   weeks 3–4 as he labels; we can re-run the Gate A.5 eval at week 4
   with more data before declaring hybrid dead.

2. **I've converged so much on GPT's R2 structure that I may be
   under-challenging the product frame itself.** Stage 2 §6 flagged
   that neither debater priced the "use Research Feeds for 4 weeks
   first" baseline. The operator chose Advance, which closes that
   decision — but Stage 3 R3 isn't the place to re-open it. Still:
   if v1 ships and the operator finds it marginal, the honest failure
   mode is that Research Feeds + Zotero would have served him for 90%
   of the value at 5% of the build cost. I can't make that failure
   less likely at this point, but I want the finals doc to acknowledge
   it as a known residual risk, not a surprise at month 4.

3. **No round of Stage 3 re-verified the local-4090 / VLM PDF-parsing
   assumption.** The proposal specifies 24GB VRAM on a 4090 and cheap-
   API access to GLM/MiniMax. R1/R2/R3 have all assumed these hold. If
   the operator's 4090 is actually allocated to other lab workloads
   most of the time (a detail neither debate round checked), batched
   overnight embedding jobs may compete for VRAM and delay the cold-
   start cycle. Flag for the build-phase checklist: confirm 4090
   availability window on day 1.

---

## 6. Decision questions (reduced)

R2 had 2 open questions. Remaining for moderator:

**D1**. The Obsidian briefing file layout — GPT's R2 didn't take a
position; my R2 proposed `YYYY/MM/YYYY-MM-DD-<topic>.md` (append-via-new-file)
with optional `<topic>.md` living pages generated alongside. Lean:
file-per-cycle as canonical, living-page as convenience view. **Defer to
build-phase operator preference**; it's a 1-day switch.

**D2**. `radar fb sync` daemon vs. nightly cron for feedback parsing —
my R2 lean was nightly cron for v1 (simpler, predictable). **Defer to
build-phase**; also a 1-day switch.

Neither is a Stage 3 gate. Both belong in the build phase's task
decomposition.

---

## 7. Architecture status — what finals should say

Consolidated posture across both sides:

- **A-primary** (topic-ledger-briefing), **B-compatible schema**
  (reserved, non-authoritative), **D-alongside** (MCP surface from v1).
- **One normalized PostgreSQL ledger**, append-only on artifact /
  framing / evidence / link transitions. `rank_signals` and
  `ranker_version` first-class. `cycle_kind` on briefing cycles.
- **Framings, not scores**. `mismatch_hint` on every framing; named
  "headline/method mismatch" briefing section gated behind
  precision@10 ≥ 0.7 at week 6.
- **Hybrid retrieval (BM25 + pgvector + RRF)** in v1, gated on Gate A.5
  eval at end of week 2. Binary: in or out, no half-in.
- **Twice-weekly cadence** (Mon synthesis + Fri delta) with same
  Obsidian template, `cycle_kind` separating semantics. 4-week A/B
  experiment on delta-eligibility after Gate C.
- **Recall-first architecture**: briefing = what you read; inbox =
  recall guarantee queryable via MCP.
- **7 MCP tools** (day 1): `topic.briefing`, `topic.inbox`,
  `topic.delta`, `topic.contrarian_view`, `artifact.trace`, `search`,
  `health`. Plus `feedback.record` = 8 (adding the feedback-capture
  path made explicit in R2).
- **8-week solo build**, 3 named gates (A/B/C) plus A.5 for hybrid-
  retrieval decision. Cost envelope: $6–$25/week LLM at observed
  volumes, room to downgrade to GLM/MiniMax if triage quality holds.

What's explicitly out of v1:
- No web UI (Obsidian + Claude Code surfaces only).
- No live X ingestion (schema + adapter stub only).
- No paywalled content.
- No autonomous novelty scoring or novelty-as-primary-rank-key.
- No automated idea-candidate clustering (operator-authored only).
- No fine-tuned local models.
- No cross-artifact entity resolution (v1.5+).

---

<!-- READY-TO-CONCLUDE -->

**Rationale for marking READY-TO-CONCLUDE**:
- GPT marked READY-TO-CONCLUDE in R2. I agree.
- Both R2 disagreements collapsed cleanly in this round: Disagreement 1
  (hybrid) into Gate A.5, Disagreement 2 (Friday) into `cycle_kind` +
  template-consistency.
- No remaining architectural disagreement. Two residual uncertainties
  (triage cost, feedback completion rate) are experiments scheduled
  within v1, not Stage-3 questions.
- Five concessions on my side (named-mismatch gate, append-only schema,
  `delta` tool, week-1-not-blocking hybrid, `cycle_kind` resolution,
  labeled-set composition, feedback-quota, B-non-authoritative
  invariant). GPT conceded cold-start discipline, ranker auditability,
  bounded B-surface, and Obsidian-first feedback.
- Protocol's S3 → Finals bar is met: ≥3 substantive disagreements
  resolved (mismatch-gating, hybrid-sequencing, Friday-semantics,
  cold-start, feedback-metric), ≥5 consensus points beyond the proposal
  (the architecture-status list in §7), each side named ≥2 things the
  other caught (I named append-only schema + named-mismatch gate + Gate
  A/B/C framing + absolute-quota feedback metric; GPT named cold-start
  principle + ranker auditability + bounded B-surface + `radar.topic.
  delta`).

Finals should consolidate, not re-open. The two launch-gate experiments
(hybrid decision, Friday delta-eligibility) belong in the finals doc as
explicitly scheduled, falsifiable in-build experiments — not as Stage 3
residue.

---

### One-line summary

**S3R3: 5 concessions (hybrid-not-week-1-blocking, `cycle_kind` template-
consistent resolution, ≥10+≥10+≥5 labeled-set rule, absolute-quota
feedback metric, B-non-authoritative invariant); 0 remaining
disagreements (both R2 hinges collapsed into Gates A.5 and `cycle_kind`);
2 residual uncertainties flagged as scheduled in-build experiments, not
blockers. READY-TO-CONCLUDE.**
