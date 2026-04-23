# Idea 002 · S3R2 · Opus 4.7 Max · Converge (engineering)

**Timestamp**: 2026-04-23
**Stage**: 3 (Converge). Mode: engineering. Round: 2.
**Moderator direction (unchanged)**: A-primary (topic-ledger-briefing) on
B-compatible schema, D (MCP surface) exposed alongside from v1.
**Reads**: `002-Opus47Max-S3R1.md` (own prior round), `002-GPT54xHigh-S3R1.md`
(opponent's round — close read), `002-stage2-checkpoint.md`,
`002-moderator-notes.md`, both S2R1s, `002-stage1-synthesis.md`.
**Searches this round**: 2 targeted (newsletter delta-vs-full engagement
data, 2026 Postgres hybrid search state).

---

## 0. What moved between R1 and R2

GPT's S3R1 produced three things that change my engineering plan:

1. **Two sharp disagreements** with well-constructed testable hinges — Friday
   as delta-not-full-briefing, and mismatch-detector gated behind a precision
   bar before getting its own briefing section.
2. **A schema shape** that is more disciplined than mine on one axis
   (`artifact_version` for immutable snapshots; `evidence_span` as an
   explicit table). Worth adopting; see §2.2.
3. **A `radar.topic.delta(topic, since_cycle?)` MCP tool** that I missed and
   that cleanly generalizes my "what_am_i_missing" special-case. Adopted;
   see §2.4.

One honest observation before I write this round: **GPT's R1 is tighter than
mine on product discipline, but softer than mine on the week-1-through-week-8
execution path and on concrete ranking/retrieval mechanics**. This round
tries to concede the first gap and press the second.

---

## 1. Steelman of GPT's strongest S3R1 point

GPT's strongest point is **Disagreement 2 from their §5** (mismatch-detector
gating):

> "v1 should store `mismatch_hint` on every artifact framing. The briefing
> can mention a mismatch only when confidence is high. The dedicated
> 'headline/method mismatches' section should wait until the detector clears
> an evaluation threshold."

Why this is stronger than my R1 position:

- **My R1 proposal was Galactica-shaped in one specific way**: it headlined
  "claim-method mismatches this cycle" as a named briefing section on
  day-1, with the precision gate only present as a week-6 eval measurement.
  That means weeks 1–5 ship a *named* feature whose quality is unvalidated.
  Pattern B (authoritative nonsense, synthesis §Pattern B) applies exactly:
  if the section fires noisily for 5 weeks, the operator learns to distrust
  *all* briefing sections, not just that one. The damage propagates.
- **The social cost of a named feature exceeds its engineering cost.** A
  pipeline-level `mismatch_hint: bool` field with a confidence score is
  cheap (artifact-level JSONB column). A named briefing section is a
  product claim — "we flag overhyped papers" — and product claims are
  trust surfaces.
- **The testable hinge is cleaner than mine.** GPT's "precision@10 ≥ 0.7
  AND ≥ half judged useful by operator" is a bar that maps onto a concrete
  promotion decision. My "recall <60% escalates to Sonnet" tuned the
  *model* but never gated the *surface*.

**I adopt this.** Concession #1 in §5. The engineering change is small
(§2.7 rewrite) but the product-trust change is large.

Secondary point worth adopting: GPT's **append-only evidence first**
posture in §2.1. My R1 schema was mutation-friendly (framings could be
re-generated over the same row). GPT's framing — every framing row is
immutable + versioned + keyed by `(artifact_id, prompt_version, model)` —
makes reproducibility a property of the database rather than a test we
have to write. That's worth the storage cost. Concession #2 in §5.

---

## 2. New ground

### 2.1 Where GPT's R1 was silent and this round isn't

GPT's R1 shipped a product frame, a schema sketch, a pinned stack, an MVP
list, and two hinges. What it did **not** ship and what this round supplies:

- **A ranking algorithm spec**, not just "rank transparently."
- **A cold-start week-1 plan** — literally what happens on day 1 when the
  store is empty and we have zero feedback data.
- **A concrete feedback-capture mechanism** — GPT's Decision Question 2
  asked about it but didn't answer it. I propose a spec.
- **A bounded definition of "enough B-compatibility"** (GPT's Decision
  Question 3) with a specific schema freeze.
- **A protocol for harvesting the 10–20 GEPA-style eval cases** from the
  operator without blocking the week-3 mismatch-detector work.

### 2.2 Schema — deltas from R1

I'm adopting GPT's shape with four specific modifications:

```text
artifact                  -- append-only on source-url uniqueness
artifact_version          -- immutable text snapshots; (artifact_id, fetch_ts)
topic                     -- candidate | active | archived (per R1)
topic_artifact_link       -- (topic_id, artifact_id, relevance, reason,
                             link_state, first_seen_at); append-only on state
                             changes — link_state transitions become new rows
framing                   -- immutable; keyed by (artifact_id, prompt_version,
                             model, created_at); superseded_by FK lets us
                             point to the "current" framing for a pair
evidence_span             -- (framing_id, field_name, start, end, source_uri)
briefing_cycle            -- date-keyed (2026-04-27-mon)
briefing_item             -- (cycle_id, topic_id, artifact_id, rank_pos,
                             section, rationale, ranker_version)
feedback                  -- (briefing_item_id OR artifact_id, kind, note,
                             operator_ts) — kind ∈ {useful, noise, missed,
                             wrong_frame, should_track_topic}
idea_candidate            -- RESERVED; see §2.6
idea_candidate_member     -- RESERVED; see §2.6
rank_signals              -- (artifact_id, topic_id, lex_score, sem_score,
                             recency_score, centroid_sim, confidence,
                             ranker_version) — replaces opaque "relevance_score"
```

Three deltas from GPT's R1 schema:

1. **`rank_signals` is first-class**, not embedded in `topic_artifact_link`.
   Reason: a new ranker version regenerates *all* signals for *all* artifacts.
   Keeping them on the link row would force either an update-in-place
   (violates append-only) or a forest of link-row duplicates. A separate
   table keyed by `ranker_version` lets the operator A/B two rankers on
   the same corpus without schema churn.
2. **`link_state` transitions are new rows, not updates.** Same reasoning.
   This gives us a link-history audit trail for free.
3. **`ranker_version` as a first-class string**, committed into every
   `briefing_item`. Reason: when the operator says "the Fri 5/8 briefing
   was bad," we need to reproduce the exact ranking decision. This costs
   one text column per briefing item.

### 2.3 Ranking algorithm spec (R1 said "rank transparently"; this is how)

The inbox ranker is a **weighted combination of 4 transparent signals**,
no black-box LLM score:

```
rank = w1·lex_score       # BM25 over (title, abstract, key excerpts)
     + w2·sem_score       # cosine(artifact_embedding, topic_centroid)
     + w3·recency_score   # exp(-Δdays / half_life_topic)
     + w4·centroid_shift  # distance from last-cycle topic centroid
     + bias_terms         # per-source prior, per-author prior (optional)
```

Concrete choices:
- `w = (0.30, 0.30, 0.20, 0.20)` as v0 defaults. Operator-tunable per topic.
  No ML learning in v1 — weights are hand-tuned against the GEPA eval
  (§2.7). Filter-bubble mitigation (Pattern F): weights never trained from
  click data in v1, because clicks produce the feedback loop GPT and I
  both worry about.
- `topic_centroid` is the EMA of (curated seed artifacts + operator-marked-
  useful artifacts from past 30 days). Re-computed weekly.
- `half_life_topic` defaults to 21 days, operator-tunable per topic —
  topics like `diffusion-LLMs` may want 7 days, `LLM-explainability` may
  want 45.
- **No "novelty score" in the rank formula.** Pattern E. `novelty_hint` is
  a display column on framings, labeled advisory, never a primary sort
  key.

Why hybrid lex+sem from day 1 (not gated behind a milestone — see §3 D1):
- BM25 alone misses GEPA-style cross-phrased cases: "self-evolution" vs.
  "self-improvement" vs. "autonomous adaptation" vs. "prompt optimization
  dressed as self-evolution." The operator's named pain case *is* a
  cross-phrasing failure.
- Semantic alone has the inverse failure: surfaces topic-adjacent items
  with no lexical anchor to the actual query. For a recall-first system,
  that's noise.
- Postgres 2026 tooling is ready (§3 D1 evidence); hybrid is not a
  "future-proofing tax" anymore.

### 2.4 MCP surface — adopting GPT's `delta`, refining the set

GPT's R1 had 6 MCP tools. Mine had 6. Where they differ:

| Opus R1 name | GPT R1 name | Keep? |
|---|---|---|
| `radar.topic.briefing` | `radar.topic.briefing` | Yes (agreed) |
| `radar.topic.inbox` | `radar.topic.inbox` | Yes (agreed) |
| `radar.search` | `radar.search` | Yes (agreed) |
| `radar.artifact.framing` | `radar.artifact.trace` | **Adopt GPT's name** — `trace` is broader: returns framing + evidence spans + rank signals + feedback history on one artifact |
| `radar.topic.what_am_i_missing` | (absent) | **Keep, rename:** `radar.topic.contrarian_view` — narrower scope (this tool specifically runs the contrarian reranker), doesn't block on `delta` |
| `radar.health` | `radar.health` | Yes (agreed) |
| (absent) | `radar.topic.delta` | **Adopt GPT's tool** — returns "what changed on topic T since cycle C": new artifacts, changed framings, promoted/demoted items, with reasons. This is the killer tool for the MCP surface. |

So 7 tools in v1, not 6. The extra is worth it — `delta` is the
MCP-native equivalent of "here's your Friday briefing experience" but
pull-driven, which partially defuses my D1 vs. GPT cadence disagreement.

### 2.5 Cold-start — week-1 operating plan (new)

Neither R1 round priced the first 7 days of deployment. This matters
because the system has no operator feedback, no topic centroid, no
`ranker_version` history, and no GEPA eval set.

**Day 1–2: corpus seed.** Backfill ingestion for each of the 8 topics from
the last 90 days. Run arxiv listing API + OpenAlex search scoped to
topic-keyword queries. Estimated volume: ~250 artifacts/day × 90 days ×
topic-scoped filter = **roughly 2,000–3,500 artifacts in the seed store**,
not 22,500. (Keyword pre-filter is essential; measured on day 1.)

**Day 2–3: seed topic centroid.** Operator supplies ≤5 canonical papers per
topic (8 topics × 5 = 40 known-relevant seeds). Centroid computed from
embeddings of those seeds. Without this, sem_score has nothing to compare
against and the ranker degrades to lex+recency only.

**Day 3: first cold-start briefing.** Generated against the 90-day
backfill, not the daily firehose. This is an intentionally wrong
briefing — its job is to surface 15 items per topic for the operator
to label (useful / noise / wrong-frame). That labeling becomes the
first feedback-weighted centroid update.

**Day 4–5: live ingestion begins.** Daily arxiv + OpenAlex + GitHub +
blogs. Briefing cron deferred until day 7.

**Day 7 (Monday): first live briefing.** At this point the system has:
cold-start-labeled backfill, 3 days of live flow, first centroids.
Briefing is honest about its cold-start state ("ranker is v0.1,
expect surprises").

Why this matters for the engineering plan: **week 1 of the build sequence
(§2.8 of my R1) has to end with "corpus seed + cold-start labeling flow"
shippable**, not "ingestion adapters." Without the seed loop, weeks 2–4
produce a ranker we can't evaluate. I'm re-ordering the week-1 deliverable
in §4.

### 2.6 B-compatibility — answering GPT's Decision Question 3

GPT asked: "is B-compat reserved tables and traceability hooks, or
tentative idea clustering immediately?" My answer: **reserved tables and
traceability hooks only; no clustering in v1**, with a specific freeze on
the surface area.

Concretely, the `idea_candidate` surface in v1 is:

```text
idea_candidate
  id             uuid
  label          text          -- free-text hypothesis, operator-authored
  created_by     'operator' | 'system' (only 'operator' in v1)
  state          'draft' | 'active' | 'archived'
  created_at     timestamptz

idea_candidate_member
  idea_candidate_id  uuid      FK
  artifact_id        uuid      FK
  operator_confirmed bool      -- v1 requires operator confirmation;
                               -- auto-clustering is v1.5+
  note               text
  created_at         timestamptz
```

What v1 doesn't have:
- No cross-artifact entity resolution (would poison the graph — synthesis
  §Pattern E)
- No LLM-generated `idea_candidate` rows (operator authors them; system
  only suggests candidates via `radar.trace`)
- No graph-edge table between ideas (one step too far; v1.5)

What v1 gives B:
- Durable history (append-only means B can reconstruct every observation)
- Artifact provenance (`artifact_version` + `evidence_span`)
- A user-sanctioned collection of "here are the artifacts I consider one
  idea" that becomes the v1.5 training data for automated clustering

This matches GPT's "reserved structure and provenance discipline" answer
in their §9. Concretely bounded.

### 2.7 Mismatch detector — rewritten around GPT's hinge

Adopting GPT's Disagreement 2. The updated plan:

- **Week 3 (unchanged)**: ship `mismatch_hint` as a framing field
  (`mismatch: {flag: bool, kind: str, confidence: float, evidence_span:
  id}`). Populated on every artifact's second-pass framing.
- **Weeks 3–5**: *no* "headline/method mismatches" section in the briefing.
  The briefing body can inline a mismatch mention only when
  `confidence >= 0.85` AND the framer flagged it spontaneously (not prompted
  to find one).
- **Week 5–6**: harvest the eval set. See §2.9.
- **Week 6 decision point**: run the eval. If `precision@10 ≥ 0.7 AND the
  operator judges ≥ 5 of the top-10 flags genuinely useful`, promote to a
  named briefing section in week 7. Otherwise, stay trace-only indefinitely
  and revisit in v1.5 with more data.
- **No Sonnet escalation until gate passes**. My R1 wanted to escalate
  triage if recall was <60%; GPT's hinge flips this — we hold off on
  *model escalation* until we have proof that the *feature* deserves
  better models. Escalate on signal, not on budget.

This is a stricter gate than I had. I think GPT is right that a named
section before it earns the name is the more dangerous failure than a
trace-only field that under-sells.

### 2.8 Feedback capture — spec (GPT's Decision Question 2)

GPT surfaced the question but didn't answer it. Answering now because v1
*depends* on this loop being alive by week 5.

**Primary mechanism: Obsidian frontmatter + sidecar CLI.**

The briefing writes each item as a markdown section with YAML frontmatter:

```markdown
## ArXiv 2604.11543 — "Self-Evolving Agents via Prompt Optimization"

<!-- radar-item: briefing_item_id=... artifact_id=... rank=3 ranker=v0.2 -->

**Claim**: Agents improve through prompt optimization, framed as
self-evolution.
**Method**: GEPA-style prompt search over trajectory evaluations.
**Why it matters**: Contested — headline and method diverge.
**Mismatch hint**: claim_overstates_method (conf=0.78) [trace]

---

<!-- radar-feedback:
#   kind: useful | noise | wrong_frame | should_track | -
#   note: (optional)
-->
```

The operator edits the `radar-feedback:` block in-place in Obsidian. A
lightweight CLI (`radar fb sync`, or a file-watcher daemon) scans the
Obsidian vault nightly, parses the edited blocks, writes `feedback` rows,
archives the comment block. No web form, no separate app, no API.

**Secondary mechanism: MCP tool `radar.feedback.record(...)`.**

For in-flow Claude Code feedback — "mark this as noise" during an in-chat
query. Same table, different surface.

**Completion-rate target (the testable hinge for this mechanism)**: after
week 4, at least 40% of items in the last 3 briefings must have a
non-empty feedback block (not necessarily useful/noise; even "-" counts).
If below 40% by week 6, the feedback mechanism is failing and we re-design
(likely a weekly 3-prompt questionnaire). Concrete falsifiable metric.

### 2.9 GEPA-shaped eval set — harvest protocol (§3 of R1 was vague)

Problem: R1 needed 10–20 historical claim/method mismatch cases by week 3
or the mismatch feature pushes to v1.5. My R1 treated this as "operator
provides." GPT's R1 said "build a small labeled set of at least 15." Neither
said *how*.

Proposal: **a 3-step harvest that runs in parallel with weeks 1–3 build**.

- **Step 1, week 1 day 5**: the system has a back-filled corpus of ~2,500
  artifacts. Run a synthetic mismatch-generation pass: prompt Haiku to
  generate candidate mismatch flags across 200 arxiv-seeded artifacts,
  confidence ≥ 0.7. Yield: ~10–20 *candidates* (many will be wrong).
- **Step 2, week 2**: operator reviews the candidates in Obsidian
  frontmatter (same mechanism as §2.8). For each, label: `genuine |
  not_genuine | borderline`. Include operator's own volunteered examples
  as a parallel input stream. Target: 12–18 genuine + 6–10 not-genuine
  = ~25-item labeled set.
- **Step 3, week 3**: if `genuine_count ≥ 10`, the mismatch feature lives;
  weeks 4–6 use this set for calibration. If `genuine_count < 10`, the
  feature moves to v1.5 — but we keep the `mismatch_hint` column
  populated so we can re-visit when more data accumulates.

This closes the "what if the operator doesn't have 10 examples?" failure
mode in my R1 self-critique. The system *helps* the operator find the
cases — it doesn't depend on pre-existing memory.

---

## 3. ≤2 disagreements with testable hinges

### Disagreement 1 · Hybrid search (BM25+pgvector) in v1 from week 1, not gated

**GPT's position (R1 §2.4)**: "install `pgvector` extension now but **gate
semantic retrieval use by milestone**. BGE-M3 on the 4090 once semantic
retrieval clears the milestone gate."

**My position**: enable hybrid lex+sem retrieval from **week 2**, not
gated behind any milestone. The gate costs more than it saves in 2026.

**Why (evidence, not assertion)**:
1. **The 2026 Postgres hybrid stack is production-ready.** pg_textsearch
   v1.0.0 (ParadeDB) is GA as of March 2026 with true BM25 + RRF fusion
   on the same database. VectorChord ships native BM25 + hybrid as one
   extension. The "operational complexity" concern from 2024 is largely
   obsolete. [pg_textsearch announcement (March 2026)](https://www.tigerdata.com/blog/introducing-pg_textsearch-true-bm25-ranking-hybrid-retrieval-postgres),
   [VectorChord hybrid guide](https://docs.vectorchord.ai/vectorchord/use-case/hybrid-search.html),
   [ParadeDB hybrid manual](https://www.paradedb.com/blog/hybrid-search-in-postgresql-the-missing-manual).
2. **The GEPA failure case *is* a cross-phrased recall failure.** The
   operator's one named concrete pain is "method was prompt optimization,
   claim was self-evolution." BM25 alone can't recover a paper searched
   under "self-evolving" that's indexed under "prompt optimization." Our
   recall-first promise is structurally unhonorable without semantic
   retrieval. Gating this behind a milestone means the recall promise
   ships broken in v1.
3. **Cost of adding vs. cost of gating.** Adding pgvector on day 1:
   extension install + 1.5 GB of BGE-M3 VRAM + embedding job (batched,
   ~2 hours for the 2,500-artifact seed). Adding it later: code churn in
   `radar.search`, re-indexing the backlog, an extra "is the gate
   cleared?" checkpoint meeting. The "add it later" option has worse
   expected cost.

**Testable hinge**: in week 2, run the GEPA eval seed (§2.9 step 1) with
three rankers — lex-only, sem-only, hybrid RRF — on the labeled subset.
If hybrid's recall@20 exceeds lex-only by ≥10 percentage points OR
captures ≥2 cross-phrased cases that lex-only misses, hybrid stays.
Otherwise we remove semantic retrieval and defer to v1.5. This is a
1-day decision, 1-command-line rollback (drop the sem_score term from
the ranker), not a gate that stalls the week-1 plan.

### Disagreement 2 · Friday is a full briefing, not a delta — scoped to "since-Monday changes"

**GPT's position (R1 §5 D1)**: Friday = delta briefing. Monday = full
synthesis. Run 4-week A/B against twice-full.

**My position**: Friday is a **full-structured briefing over a narrow
window**, not a delta. Structurally identical to Monday, content-wise
scoped to the Mon-→-Fri window only. The word "delta" smuggles in a
different product claim that the evidence doesn't support.

**Why**:
1. **The delta framing is an A/B-test convention, not an operator
   workflow.** Newsletter benchmarks literature ([newsletter KPIs 2025 -
   Admailr](https://www.admailr.com/email-advertising-tips/newsletter-kpis-2025/),
   [open rate benchmarks 2025 - MailerLite](https://www.mailerlite.com/blog/compare-your-email-performance-metrics-industry-benchmarks))
   shows structure consistency drives open-rate. A "delta surface"
   formatted differently from the Monday brief is a cognitive-cost delta
   *itself* — the operator has to re-orient each time. Twice-weekly is
   fine; two-shapes-weekly is not.
2. **The operator's Q-M3 answer doesn't say "Friday is lighter."** The
   answer is "周一早上，周五早上。" — two reading sessions, equal weight
   implied by the symmetric phrasing. GPT's delta hypothesis is a
   reasonable prior, but it's not what the operator said. Over-fitting
   the product to a generic knowledge-work pattern ("end-of-week
   scanning") when we have a direct operator statement is the wrong
   move.
3. **Content-scope ≠ surface-format.** I agree with GPT that Friday's
   *content* is a 4-day window; I disagree that the *format* should
   differ. Same sections, same ranker, same number of items, smaller
   input volume. This gets GPT's "lighter on Friday" intent naturally
   from the smaller window without a UX fork.

**Testable hinge**: same 4-week experiment GPT proposed, but three arms
not two:
- Arm A: Monday full + Friday full (same shape, 4-day window on Fri)
- Arm B: Monday full + Friday delta (GPT's proposal)
- Arm C: Monday only (baseline — is the Friday briefing even needed?)

Metric: per-briefing open rate × items-clicked-through × explicit
useful-count. Each arm runs 2 weeks (not 4) because this is a 2-arm
problem expanded to 3 for the baseline. If Arm A ≥ Arm B on combined
score, we stay with full-on-Friday. If Arm C ≥ both, we collapse to
Monday-only + an MCP-surface `delta` tool the operator pulls ad-hoc.

Note: **this hinge is not worth arguing about hard**. Both positions
converge on "run the experiment." The real disagreement is about whether
v1 week 5 ships 1 briefing format or 2.

---

## 4. Build sequence — updated from R1 §2.8

R1's sequence was 8 weeks with week 1 = storage + ingestion. The
cold-start reasoning (§2.5) and the eval-set harvest (§2.9) change the
shape. Updated:

- **Week 1** — storage schema (including `rank_signals`, `feedback`,
  `artifact_version`, `idea_candidate`); arxiv + OpenAlex ingestion;
  topic seed config; **backfill 90 days per topic**; seed centroid
  computation; cold-start labeling flow end-to-end (operator labels
  ≤50 seed items in Obsidian). **Hybrid pgvector+pg_textsearch online
  end of week 1.**
- **Week 2** — Semantic Scholar lookup; GitHub trending; blog whitelist
  (robots.txt strict); triage pass scaffolding; **GEPA eval seed (§2.9
  step 1) run against the backfill**; ranker v0.2 with feedback-weighted
  centroid update.
- **Week 3** — second-pass framing (Haiku) + `mismatch_hint` column;
  **operator labels the GEPA seed (§2.9 step 2)**; evidence-span
  extraction. Decision at end of week 3: `genuine_count ≥ 10` → feature
  lives; otherwise drop the *named section plan* entirely (still keep
  the column).
- **Week 4** — briefing generator (Sonnet) → Obsidian write; first live
  briefing for 1 topic with mismatch field inlined only on
  `confidence ≥ 0.85`. Feedback sync daemon (§2.8 spec) live.
- **Week 5** — scale to all 8 topics; briefing cadence lands (Mon+Fri,
  both full per §3 D2 until the experiment runs); ranker weights tuned
  against accumulated `feedback` rows.
- **Week 6** — MCP server + 7 tools (§2.4); contrarian reranker for
  `radar.topic.contrarian_view`; mismatch precision@10 eval. **Promotion
  decision for the named mismatch section.**
- **Week 7** — topic lifecycle commands; X adapter stub + schema fields;
  run the 3-arm cadence experiment (§3 D2) if two weeks allow.
- **Week 8** — hardening; backup/restore; cost audit; operator runbook.
  `ranker_version` audit log shipped.

The critical path is still 8 weeks; the re-ordering front-loads the
cold-start + eval loops which are the things that most threaten a silent
failure mode.

---

## 5. Concessions (≥1)

**Concession #1**: Adopted GPT's mismatch-gated-behind-precision
(§1, §2.7). My R1 shipped a named briefing section day-one on an
unvalidated feature. GPT is right that this is Pattern B-shaped.
Named surfaces are trust surfaces; earn the name.

**Concession #2**: Adopted GPT's append-only `artifact_version` +
`evidence_span` schema discipline (§2.2). My R1 treated framings as
mutable on re-generation. GPT's immutable + versioned framings make
reproducibility a database property, and the storage cost is negligible
at our volumes (2,000 framings/week × 2 KB ≈ 200 MB/year).

**Concession #3**: Adopted GPT's `radar.topic.delta` MCP tool (§2.4).
I had `what_am_i_missing` as my only delta-shaped tool, but that's a
contrarian-reranker special-case. A general `delta(topic, since_cycle)`
is the right abstraction, and `contrarian_view` becomes a narrower
sibling.

**Concession #4**: On Decision Question 1 from my R1 (GLM vs MiniMax):
this is no longer a pre-decision. The GEPA eval (§2.9) in week 2 gives
us a cheap side-by-side test on 200 labeled-by-operator candidates. Let
the data pick. My R1 wanted the moderator to pick on day 1; GPT's R1
implicitly assumed Haiku for first-pass and Sonnet for briefing, which
is the safer default. I'm moving to **Haiku first-pass + Sonnet briefing
as v0; GLM/MiniMax cost-optimization as a week-4 optional replacement
if the Haiku cost line exceeds $50/week**. Cost economics get revisited
empirically, not argued.

---

## 6. Self-critique

Three under-confidences in this round:

1. **My cold-start §2.5 assumes the operator can supply 5 seed papers
   per topic in 2 days.** If seed papers aren't handy, week-1's seed
   centroid is delayed and ranker v0 degrades further. I should have a
   fallback: use the top-5 arxiv results for the topic keyword as
   auto-seeds if the operator's list isn't ready by day 3. That's a
   worse centroid but non-blocking. (Didn't write this into §2.5 and
   should have.)
2. **The feedback-rate target of 40% in §2.8 is a guess.** I don't have
   data on what rate of feedback a solo operator actually provides in
   practice on a personal tool. If real-world rates are 10–15%, my
   ranker-tuning plan (§2.3) starves and we're back to hand-tuned
   weights forever. I've set 40% as the product's acceptance bar
   without evidence — only self-awareness that I'm guessing. The
   testable hinge structure is fine; the number may be wrong.
3. **The hybrid-retrieval Disagreement 1 gets my strongest argument but
   the narrowest test.** If the GEPA seed in week 2 has only 10–20
   mismatch-candidates, we may not have enough cross-phrased cases to
   measure a 10-percentage-point recall difference reliably. The
   hinge's statistical power is weak. If GPT pushes back on this, my
   fallback is "we fire on any concrete cross-phrased case recovery,
   not a rate," which is a weaker hinge but still falsifiable.

---

## 7. Open decision questions (for S3R3 or moderator)

Reduced from R1's 3 to 2:

**D1 (merged, was R1-D2+D3).** Obsidian briefing file layout — one
file-per-topic-per-cycle (my R1 lean) vs. one living-page-per-topic
(operator may prefer). Now that `briefing_cycle` is a first-class table,
both layouts can be generated from the same store. My lean: file-per-
cycle as v1 (timestamped history), with a separate `<topic>.md` living-
page generated alongside that is always the latest. This costs a few
extra Obsidian files but preserves both use-cases. Moderator preference
still decides the primary navigation surface.

**D2 (new).** The `radar fb sync` daemon vs. manual CLI: should feedback
parsing run on a file-watcher (auto-absorb) or a nightly cron
(predictable, but delayed by up to 24h)? Leaning nightly cron for v1 —
simpler, less to debug, aligns with the "system doesn't surprise the
operator" ethos. File-watcher is a v1.5 upgrade if the operator wants
in-session feedback latency.

---

<!-- not READY-TO-CONCLUDE -->

Rationale for not marking READY-TO-CONCLUDE: GPT's S3R2 hasn't landed yet.
I conceded 4 points, opened 2 disagreements with testable hinges
(Disagreement 2 is weaker than Disagreement 1 — probably collapsible
with one more round), and introduced significant new ground (ranking
spec, cold-start, feedback capture, eval harvest). One more round of
convergence would finalize: (a) whether GPT accepts the hybrid-from-day-1
argument, (b) whether the feedback-capture mechanism survives contact
with an engineering counter, (c) whether the cold-start seed protocol
has a better alternative I missed. After R3, finals are feasible.

---

### One-line summary

**S3R2: 4 concessions (named-section gate, append-only framings, `delta`
MCP tool, model pick deferred to data); 2 hinges (hybrid search in v1
from week 1, Friday = full briefing not delta); new ground on ranking
spec, cold-start week-1 plan, feedback capture spec, GEPA eval harvest
protocol, B-compat surface bound. Not READY-TO-CONCLUDE.**
