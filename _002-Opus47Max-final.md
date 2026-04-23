# Idea 002 · Opus · Final Position

**Timestamp**: 2026-04-23
**Author**: Opus 4.7 Max
**Idea**: Research Radar — a lab-internal, topic-scoped research surveillance
system for a solo operator leading a ~15-person AI lab.
**Moderator direction (binding)**: **A-primary** (topic-ledger-briefing) on a
**B-compatible schema**, with **D (MCP surface) exposed alongside** from v1.
**Reads (consolidating)**: every file in `discussion/002/` — PROTOCOL absent,
both S1A/S1B, S2R1 both sides, stage1-synthesis, stage2-checkpoint, moderator
notes, both S3R1 and S3R2.

---

## 1. My final recommendation (TL;DR, 5 bullets max)

1. **Build it, lab-internal, recall-first.** Ship a topic-ledger-briefing
   system for the 8 operator-supplied seed topics (`agentic-RL`,
   `agent self-evolution`, `diffusion-LLMs`, `compressing-LLM-reasoning`,
   `novel-LLM-architectures`, `on-policy-distillation`,
   `LLM-explainability`, `LLM-adapters`) with Mon/Fri Obsidian briefings and
   an MCP pull surface from day 1. Do NOT position as a product.
2. **The briefing is what you read; the inbox is the recall guarantee.**
   ~1,700 artifacts/week end up in the store; the briefing surfaces ≤15
   per topic per cycle; the rest remain queryable via MCP and are never
   silently dropped. This reconciles the operator's "更怕漏报" preference
   with human reading capacity.
3. **Framings, not scores.** Output is structured per-artifact framings
   (`claim`, `method`, `delta_from_prior`, `why_relevant`,
   `mismatch_hint`). Novelty is an *advisory hint*, never a primary rank
   key. Four S1B benchmarks (NovBench, GraphMind, Literature-Grounded
   Novelty, DeepReview) show autonomous novelty scoring is adversarially
   fragile in 2026.
4. **Append-only, auditable, one store, two surfaces.** Every framing
   immutable and versioned by `(artifact_id, prompt_version, model)`;
   every ranking decision reproducible via `ranker_version`; Obsidian
   briefing (push) and MCP tools (pull) read from the same PostgreSQL
   ledger. 7 MCP tools: `topic.briefing`, `topic.inbox`, `topic.delta`,
   `topic.contrarian_view`, `artifact.trace`, `search`, `health`.
5. **8-week solo build, gated on three explicit milestones.** Gate A
   (week 1): seed corpus + cold-start briefing + first labels. Gate B
   (week 3): mismatch = trace-level field (NOT named briefing section);
   GEPA-shaped eval set with ≥10 positives, ≥10 negatives, ≥5 controls.
   Gate C (week 5): Mon/Fri cadence live, feedback loop earns operator
   steering. Named mismatch section only if week-6 eval clears
   precision@10 ≥ 0.7.

---

## 2. Full technical proposal

### 2.1 System shape

One logical system, three observable surfaces. Same normalized
PostgreSQL store feeds all three.

```
┌─────────────────────────────────────────────────────────┐
│                    INGESTION LAYER                      │
│  arxiv · OpenAlex · Semantic Scholar · OpenReview ·     │
│  GitHub trending · curated-blog whitelist (~15 sites,   │
│  robots.txt strict, rate-limited)                       │
│  [X adapter: schema + stub only, no v1 client]          │
└──────────────────┬──────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────────────┐
│              NORMALIZATION + APPEND-ONLY STORE          │
│  artifact (source-URL unique)                           │
│  artifact_version (immutable text snapshots)            │
│  topic (candidate|active|archived)                      │
│  topic_artifact_link (state transitions = new rows)     │
│  framing (immutable, keyed by prompt_version+model)     │
│  evidence_span (field-level provenance)                 │
│  briefing_cycle / briefing_item / feedback              │
│  rank_signals (lex · sem · recency · centroid-shift)    │
│  idea_candidate / idea_candidate_member (RESERVED,      │
│     non-authoritative, operator-created only)           │
└──────────────────┬──────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────────────┐
│           TRIAGE + RANKING LAYER                        │
│  Recall-first: every artifact scored, none dropped      │
│  Triage pass: Haiku 4.5 (first-pass; GLM/MiniMax v1.5   │
│     only if cost forces)                                │
│  Second pass (top-N per topic): Haiku 4.5 + structured  │
│     framing extractor (claim, method, mismatch_hint)    │
│  Hybrid retrieval: pg_textsearch BM25 + pgvector/BGE-M3 │
│     semantic, RRF fusion; hybrid proven-then-blocking   │
│  Ranker: transparent weighted sum, no black-box score   │
└──────────────────┬──────────────────────────────────────┘
                   ↓
         ┌─────────┴─────────┬──────────────────┐
         ↓                   ↓                  ↓
  ┌──────────────┐    ┌──────────────┐   ┌──────────────┐
  │ BRIEFING     │    │ INBOX        │   │ MCP SURFACE  │
  │ Mon/Fri AM   │    │ (read-thru   │   │ (on-demand)  │
  │ Sonnet 4.6   │    │  queryable,  │   │ 7 tools, see │
  │ → Obsidian   │    │  never       │   │ §2.4         │
  │   markdown   │    │  linear)     │   │              │
  └──────────────┘    └──────────────┘   └──────────────┘
```

### 2.2 Pinned stack (v1)

| Layer | Choice | Reason |
|---|---|---|
| Runtime | Python 3.12, `uv` | CLAUDE.md tool preference |
| Storage | PostgreSQL 16 + `pgvector` + `pg_textsearch` (or ParadeDB/VectorChord equivalent) | Hybrid retrieval in one DB; no separate vector store |
| ORM | SQLAlchemy 2.x + Alembic | Migrations matter because schema grows through B-upgrade path |
| Embedder | BGE-M3 on local 4090 (~1.5 GB VRAM) | Cost + latency; cache-per-artifact |
| PDF parse / figure VLM | InternVL or 4–8B-tier (on 4090) | Only when abstract is insufficient |
| Triage LLM (first-pass) | **Claude Haiku 4.5** | Safe default; GLM-4.6/MiniMax-M2 evaluated week 4 if Haiku cost > $50/week |
| Second-pass framing | **Claude Haiku 4.5** | Same model, different prompt for structured framing |
| Briefing synthesis | **Claude Sonnet 4.6** | Opinionated, readable, still cheap at 16 briefings/week |
| Opus | **Not used in v1** | CLAUDE.md prohibited for boilerplate |
| MCP server | Python `mcp` SDK, stdio transport | Claude Code integration |
| Scheduler | `cron` + `systemd timers` | Single-user; no Airflow |
| Ingestion | `arxiv.py`, `pyalex`, `semanticscholar`, `httpx` + `trafilatura` | Rate-limit middleware, robots.txt strict |
| Output sink | Obsidian vault, path `~/obsidian-vault/research-radar/YYYY/MM/YYYY-MM-DD-<topic>.md` | Operator already uses Obsidian |
| Feedback | Obsidian frontmatter blocks parsed by nightly cron; `radar.feedback.record` MCP tool | Meet operator where they already read |
| Tests | `pytest`, real Postgres in Docker (no mocked DB per CLAUDE.md) | CLAUDE.md iron rule |
| Lint | `ruff` | CLAUDE.md |

### 2.3 Schema (B-compatible, append-only)

Core tables, committed to memory after R2 convergence:

```sql
-- Append-only core
artifact(id, source_url UNIQUE, source_type, authors, pub_ts, fetch_ts)
artifact_version(id, artifact_id FK, fetched_at, text_ptr, sha256)
topic(id, name, status {candidate|active|archived}, seed_keywords,
      seed_artifact_ids, created_at, archived_at)
topic_artifact_link(id, topic_id, artifact_id, link_state, relevance,
                    reason, first_seen_at, ranker_version)
                    -- state transitions = new rows
framing(id, artifact_id, topic_id, prompt_version, model, created_at,
        claim, method, delta_from_prior, why_relevant,
        mismatch_hint JSONB {flag, kind, confidence, evidence_span_id},
        superseded_by FK)
evidence_span(id, framing_id, field_name, start, end, source_uri)

-- Ranking (auditable)
rank_signals(id, artifact_id, topic_id, ranker_version,
             lex_score, sem_score, recency_score, centroid_shift,
             bias_terms JSONB, confidence)

-- Cycles + feedback
briefing_cycle(id, date, cycle_kind {synthesis|delta}, ranker_version)
briefing_item(id, cycle_id, topic_id, artifact_id, rank_pos,
              section, rationale, framing_id)
feedback(id, briefing_item_id_or_artifact_id, kind
         {useful|noise|missed|wrong_frame|should_track_topic},
         note, operator_ts)

-- B upgrade path (RESERVED, non-authoritative in v1)
idea_candidate(id, label, created_by {operator|system}, state
               {draft|active|archived}, created_at)
idea_candidate_member(idea_candidate_id, artifact_id,
                      operator_confirmed bool, note, created_at)
```

Four disciplines this schema enforces:
- **Reproducibility is a DB property, not a test.** Every framing keyed
  by `(artifact_id, prompt_version, model)`; `superseded_by` FK lets
  each pair have a "current" without losing history.
- **Ranking is auditable.** `ranker_version` is a first-class string
  written into `rank_signals` and every `briefing_item`. "The Fri 5/8
  briefing was bad" becomes a reproducible query.
- **No B-dependency leaks into A.** An artifact must appear in briefings,
  inbox, and MCP search *without* an `idea_candidate` assignment. Idea
  candidates are operator-created only in v1; the system never auto-
  clusters.
- **Filter-bubble mitigation at schema level.** Ranker weights are
  hand-tuned in v1, never trained from click data. Filter-bubble
  literature (S1B Q7: arxiv 2307.01221 + 2402.15013) says personalization
  narrows; the mitigation is architectural, not hopeful.

### 2.4 MCP surface (7 tools, day-1, stdio to Claude Code)

| Tool | Purpose | Recall-first guarantee |
|---|---|---|
| `radar.topic.briefing(topic, cycle?)` | Latest briefing body for a topic | — |
| `radar.topic.inbox(topic, since?, limit?=200)` | Full ranked inbox since a point | Never filters; only ranks |
| `radar.topic.delta(topic, since_cycle?)` | What changed on a topic since cycle C | Includes demotions + changed framings |
| `radar.topic.contrarian_view(topic)` | Items the default ranker deprioritized (serendipity valve) | Pattern-F mitigation |
| `radar.artifact.trace(artifact_id)` | Full framing + evidence spans + rank signals + feedback history | GEPA-case audit surface |
| `radar.search(query, topic_filter?, since?, limit=100)` | NL query across claims/methods/framings (hybrid) | Ranked, not filtered |
| `radar.health()` | Ingest backlog, last-cycle cost, per-source status | Pattern-C upstream-risk alarm |

### 2.5 Ranking algorithm (transparent, no black-box)

```
rank = 0.30·lex_score        # BM25 over (title, abstract, excerpts)
     + 0.30·sem_score        # cosine(artifact_emb, topic_centroid)
     + 0.20·recency_score    # exp(-Δdays / half_life_topic)
     + 0.20·centroid_shift   # distance from last-cycle topic centroid
     + bias_terms            # per-source / per-author priors, optional
```

- **Weights hand-tuned** against the GEPA-seeded eval set (§2.9), never
  learned from click data in v1 (filter-bubble mitigation).
- `topic_centroid` = EMA over (seed artifacts + operator-`useful`-marked
  artifacts, past 30 days); recomputed weekly.
- `half_life_topic` = 21 days default, per-topic tunable (e.g., 7 days
  for `diffusion-LLMs`, 45 for `LLM-explainability`).
- **No novelty score in `rank`.** `novelty_hint` lives on the framing
  row, labeled advisory; never a sort key.

### 2.6 Cold-start plan (week 1, non-negotiable gate)

Week 1 ends only if all five deliverables exist:
1. 8 seed topics loaded from operator's Q-M1 list.
2. 90-day topic-scoped backfill completed (~2,000–3,500 artifacts).
3. All 12 core tables live (§2.3).
4. First cold-start briefing generated against the backfill, even if
   intentionally noisy; operator labels ≥20 seed items via Obsidian or
   MCP.
5. `radar.artifact.trace(...)` works on every item in that seed briefing.

**Fallback for seed centroid**: if operator hasn't supplied 5 canonical
papers per topic by day 3, auto-seed from top-5 arxiv results for the
topic keyword. Worse centroid, non-blocking. Operator can override later.

### 2.7 Claim/method mismatch detector (GEPA-shaped; R2 gated)

The operator's concrete Q-M4 pain was the GEPA paper — "agent self-
evolution" in the headline, prompt optimization in the method. The
system must help catch these, but **earn the name first**:

| Week | State |
|---|---|
| 3 | `mismatch_hint` lives as a column on every framing row. |
| 3–5 | Briefing *body* may mention a mismatch inline only when `confidence ≥ 0.85`. No dedicated section. |
| 6 | Evaluate on GEPA-style eval set: ≥10 positives, ≥10 negatives, ≥5 "flashy-but-aligned" controls (GPT's R2 addition). |
| 6 decision | If `precision@10 ≥ 0.7` AND operator judges ≥5 of top-10 genuinely useful → week 7 promotes to named "headline/method mismatches" briefing section. Else stays trace-only, revisit v1.5. |

This is the one v1 feature where "named surface" = "earned trust". The
alternative (shipping a named section day-1) is Pattern-B-shaped
(authoritative nonsense, Galactica-class failure mode).

### 2.8 Feedback capture

**Primary**: Obsidian frontmatter blocks. Each briefing item gets:
```yaml
<!-- radar-item: briefing_item_id=... artifact_id=... ranker=v0.2 -->
<!-- radar-feedback:
#   kind: useful | noise | wrong_frame | missed | should_track | -
#   note: (optional)
-->
```
The operator edits the feedback block in-place. Nightly cron (`radar fb
sync`) scans the vault, parses edits, writes `feedback` rows, archives
processed blocks. No web form, no separate app.

**Secondary**: `radar.feedback.record(...)` MCP tool for in-flow reactions
inside Claude Code. Same table.

**Success metric (R2 refinement from GPT)**: realistic for a solo
operator — ≥8 labeled items per cycle AND ≥3 corrective labels every 2
weeks (noise/wrong_frame/missed). Not "40% of items" (too sensitive to
briefing size). If below by week 6, redesign (likely a weekly 3-prompt
questionnaire).

### 2.9 GEPA eval set harvest

Three-step, parallel to weeks 1–3 build:

- **Week 1 day 5**: synthetic mismatch-generation pass over 200
  backfill artifacts at Haiku `confidence ≥ 0.7`. Yields ~10–20
  candidates (many wrong).
- **Week 2**: operator labels each via Obsidian: `genuine |
  not_genuine | borderline`. Operator's own volunteered examples (GEPA +
  any others) enter as parallel input. Target: ≥10 genuine, ≥10
  not-genuine, ≥5 "flashy-but-aligned" controls.
- **Week 3 gate**: if ≥10 genuine → mismatch feature lives; else push
  to v1.5. Either way, `mismatch_hint` column stays populated for
  future data accumulation.

### 2.10 Topic lifecycle

- States: `candidate → active → archived`. Never `DELETE`.
- Archived topics: artifacts remain queryable via `radar.search`; no
  briefing generated; page becomes read-only.
- Hard cap: 15 active topics (operator constraint). Exceeding requires
  archiving first.
- Yearly review via `radar.topic.review()` MCP tool: per-topic
  briefing-open rate, inbox-query rate, artifact volume, last-active.
- Matches operator's expected churn: +3 new, −2 dropped per year,
  stable 8–15.

### 2.11 Out-of-scope (explicit)

- ❌ Web UI. Obsidian + Claude Code is the entire surface.
- ❌ Autonomous idea graph. `idea_candidate` tables exist but v1 does
  no auto-clustering; operator-created only.
- ❌ X ingestion. Adapter stub + schema fields only. Operator note 3:
  "留个口子, 后面再具体确定方案".
- ❌ Paywalled content (IEEE/ACM/bioRxiv-login). Operator note 4.
- ❌ Fine-tuned local models. Inference with pre-trained only.
- ❌ Personalization beyond 8 topics + explicit feedback. Filter-bubble
  literature (Pattern F, S1B Q7) supports deferral.
- ❌ Autonomous novelty *scoring*. Only *hints*, always advisory.
- ❌ Lab-memory-as-onboarding surfaces. Year-3 aspiration; not priced.
- ❌ Project-linked features (Direction C). Operator Q-M2: no project
  state exists. Collapses C's precondition.

### 2.12 Observability / cost

- Structured JSONL logs to disk.
- Per-artifact cost telemetry in Postgres (`rank_signals.bias_terms`
  holds cost; `framing` rows log model + token counts).
- `radar.health()` exposes backlog, last-cycle cost, per-source health.
- **Weekly LLM cost estimate (§2.5 R1 math)**: ~$6/week ≈ $312/year at
  Haiku-for-triage + Sonnet-for-briefing tier. If triage quality forces
  Sonnet escalation everywhere, worst case ~$50/week ≈ $2,600/year —
  still within any sane budget.

---

## 3. MVP plan

### 3.1 Phase 0 — Proof of concept (≤5 days)

Before the 8-week build starts, a 3-day spike de-risks the two
assumptions most likely to change the plan:

1. **Day 1**: 100-paper corpus from the operator's preferred arxiv
   categories. Run Haiku-triage on each, hand-label claim-span and
   method-span accuracy on 30. If <80% accurate, escalate triage
   plan to Sonnet (pre-build, before the cost line is committed).
2. **Day 2**: `pg_textsearch` + `pgvector` hybrid retrieval on the
   100 papers. Include at least 3 cross-phrased pairs (e.g.,
   "self-improvement" vs. "prompt optimization"). Verify hybrid
   recovers them; lex-only misses them.
3. **Day 3**: end-to-end one-briefing demo on one topic. Operator
   reads it; sanity-checks the voice and cadence.

Output: a go/no-go on the 8-week plan, and empirically tuned decisions
on Haiku-vs-escalate and hybrid-vs-lex.

### 3.2 Phase 1 — v0.1 shippable (8 weeks)

The 8-week build sequence, gated:

| Week | Deliverable | Gate |
|---|---|---|
| 1 | Storage schema + arxiv/OpenAlex ingestion + 8-topic backfill + cold-start labeling loop + hybrid retrieval online | **Gate A**: 90-day backfill done, 1st cold-start briefing exists, operator labeled ≥20 items, `trace` works |
| 2 | Semantic Scholar lookup + GitHub trending + blog whitelist + triage scaffolding + GEPA eval seed (synthetic gen) + ranker v0.2 with feedback-centroid | — |
| 3 | Second-pass framing (Haiku) + `mismatch_hint` column + evidence-span extraction + operator labels GEPA seed | **Gate B**: eval set has ≥10 genuine, ≥10 not-genuine, ≥5 controls; mismatch = trace-level field only |
| 4 | Briefing generator (Sonnet) → Obsidian write + first live briefing (1 topic) + feedback sync daemon | Operator feedback ≥8 labeled items/cycle |
| 5 | Scale to all 8 topics + Mon+Fri cadence live + ranker weights tuned from `feedback` | **Gate C**: Mon/Fri live across 8 topics; feedback loop proves operator can steer |
| 6 | MCP server + 7 tools + contrarian reranker + mismatch precision@10 eval | Mismatch promotion decision: named section iff `precision@10 ≥ 0.7` + operator judges ≥5/10 useful |
| 7 | Topic lifecycle commands + X adapter stub + 3-arm cadence experiment start (Mon-full-Fri-full / Mon-full-Fri-delta / Mon-only) | — |
| 8 | Hardening + backup/restore + rate-limit edges + cost audit + operator runbook in `projects/002-*/README.md` | Cadence experiment 2-week result collected |

### 3.3 Phase 2 — v1.0 commercial (months 3–6)

"Commercial" here is a misnomer — this is a personal tool. Read as
"v1.0 stable, publishable-internals-ready":

- **v1.5 upgrades** (earned, not promised):
  - Auto-clustering into `idea_candidate` (Direction B upgrade) —
    only if the operator's hand-authored idea candidates hit ≥50
    over 3 months, providing training data. Cross-artifact entity
    resolution is research-grade; ship it only after the operator
    has exercised the hand-authored flow.
  - `radar.topic.contrarian_view` matured with operator-tunable
    "disagreement aggressiveness."
  - X adapter becomes a live client behind feature flag; starts
    with ≤10 key accounts (operator whitelist).
  - Local fine-tuned models on 4090 for claim/method extraction
    — only if Haiku cost exceeds $50/week consistently.
- **Publishable-internals**: a short write-up of the
  claim/method-mismatch detector's precision/recall against the
  GEPA-shaped eval set. This is the piece that, if the system works,
  has a natural paper in it.
- **No SaaS pivot.** The standing novelty is narrow (synthesis §8);
  widening scope dilutes it fast. Iris.ai raised $8.3M building the
  enterprise version — don't play their game.

---

## 4. Consensus with GPT

Strict interpretation — "we both committed to X as the way forward,"
not "we both mentioned X." By the end of S3R2, we committed together to:

1. **Briefing = reading surface; inbox = recall guarantee.** GPT
   credited me for this framing; I credit GPT for forcing it to be
   operationally precise. The ~1,700-artifact/week inbox was never
   meant to be read linearly.
2. **Framings, not scores.** GPT's S2R1 §1 shift from "the system
   judges" to "the system makes judgment cheaper, more traceable,
   and less lossy" — I adopted in S3R1 concession #1 and that adoption
   held.
3. **Append-only evidence first.** GPT's S3R1 §2.1 principle — every
   framing immutable and versioned — I adopted in S3R2 concession #2.
   Reproducibility becomes a DB property.
4. **Named mismatch section earns its name.** GPT's S3R1 §5 D2
   precision-gate — I adopted in S3R2 concession #1. A named surface
   before the precision gate clears is Pattern B (Galactica).
5. **`radar.topic.delta` is the right primitive.** GPT's S3R1 tool —
   I adopted in S3R2 concession #3; my `what_am_i_missing` became a
   narrower `contrarian_view` sibling.
6. **Bounded B-compatibility.** Reserved tables + operator-created
   idea-candidates only; no automated clustering in v1. Agreed in
   both S3R2s.
7. **Cold-start is a week-1 deliverable, not a weeks-2-to-3
   afterthought.** GPT adopted my S3R2 cold-start plan as his S3R2
   concession #1. Week 1 is not done without seed corpus + labels.
8. **Obsidian-first feedback, not a new UI.** GPT conceded in S3R2
   concession #4; I specified the mechanism in S3R2 §2.8.
9. **Transparent ranker with `ranker_version` first-class.** GPT
   conceded `rank_signals` deserves its own table in S3R2 concession
   #2.
10. **Hybrid retrieval lands in v1, early.** We disagreed narrowly
    on whether it's week-1 blocking (my position) or week-2 at the
    latest (GPT's position), but not on inclusion.

That is 10 concrete commitments. The architecture is converged.

---

## 5. Residual disagreements

Two remain, both now "launch experiments" rather than architectural
doubt. GPT marked READY-TO-CONCLUDE in S3R2; I did not, because I
wanted one more round on these. Now that we're writing finals, I'll
state the honest verdict on each.

### 5.1 Hybrid retrieval: week-1 blocking vs. week-2 gate

- **What GPT thinks**: install pgvector/pg_textsearch early, but don't
  block the first live briefing on hybrid retrieval being wired in.
  Week 1 success is "operator has something concrete to react to,"
  not "hybrid is live." If a day-5 eval shows hybrid recovers ≥2
  cross-phrased misses, it becomes blocking before the first
  multi-topic briefing; otherwise it lands week 2.
- **What I think**: hybrid from week 1, not gated. The operator's
  stated Q-M4 pain (GEPA = cross-phrased failure) is structurally
  un-addressable by lex-only retrieval. Shipping week 1 without
  hybrid means shipping the recall promise broken. The 2026 Postgres
  hybrid tooling (pg_textsearch, ParadeDB, VectorChord) is GA; the
  "operational complexity" argument from 2024 is stale.
- **My honest view on who's right**: **GPT is slightly more right
  about risk management; I'm slightly more right about the
  technical argument.** If I had to decide unilaterally, I'd still
  ship hybrid in week 1 — the tooling cost is small and the upside
  (honest recall from day 1) is the whole product promise. But
  GPT's reading — that week 1 should be blocked on "operator has
  something to react to," not on "hybrid is wired" — is the safer
  project-management stance. A solo operator running 1–2 junior
  equivalents can't afford week-1 scope creep.
- **What would settle it**: the Phase 0 day-2 spike (§3.1) resolves
  this for free. If hybrid installs in half a day and the recall
  difference on the 100-paper toy set is obvious, GPT's concern is
  moot. If installation is painful or the recall difference is
  marginal, GPT was right to gate it.
- **Recommended resolution**: run the Phase 0 day-2 spike. If clean,
  week-1 block on hybrid (my position). If rough, week-2 gate with
  lex-only briefing acceptable for week 1 (GPT's position).

### 5.2 Friday: full over short window vs. delta-semantics-with-same-template

- **What GPT thinks**: same markdown template both days
  (operator-facing consistency), but Friday is semantically a
  **delta cycle** (`cycle_kind = delta` on the `briefing_cycle`
  row). Friday allows carryovers to be suppressed unless they've
  materially changed; Monday re-synthesizes from the current state.
  The semantic distinction affects ranking, `radar.topic.delta`
  meaning, and how we evaluate usefulness.
- **What I think**: same template AND same semantics — Friday is a
  full briefing over a 4-day window, structurally identical to
  Monday. Q-M3's operator phrasing is symmetric ("周一早上，周五早上");
  the "end-of-week scanning is lighter" intuition is a generic
  knowledge-work prior, not this operator's stated behavior.
- **My honest view on who's right**: **We actually agreed by the end
  of S3R2 more than either of us realized.** GPT conceded visible
  template consistency; I conceded that Friday's content window is
  narrower. The remaining disagreement is whether `cycle_kind`
  differs on the DB row. GPT's right that it's cheap to distinguish
  and enables different evaluation; I'm right that the operator
  shouldn't *experience* them differently. **Both are true.** Store
  `cycle_kind`, render identical markdown. That's the resolution.
- **What would settle it**: the 3-arm cadence experiment
  (Mon-full-Fri-full / Mon-full-Fri-delta-semantics /
  Mon-only-baseline) that both of us proposed. 2 weeks per arm, 6
  weeks total. Per-briefing open rate + useful-count + `trace`/`delta`
  MCP usage per Fri item = the metric.
- **Recommended resolution**: store `cycle_kind` (GPT's preference,
  cheap); render the same markdown template (my preference); run
  the 3-arm experiment in weeks 9–14.

---

## 6. Where GPT was stronger than me

Intellectual honesty. GPT's framings were better than mine in at least
four places:

1. **"Motion of ideas" over paper-centric (S1A → S1B §1 concession)**.
   My S1A was paper-centric with repos as "anomalies." GPT's S1A
   named the right mental model — ideas migrating across paper →
   repo → blog → discourse — from the start. I conceded in S1B §1
   and it carried into the B-compatible schema. This was the single
   biggest cross-model update in the debate.
2. **"Preference prison" (S1A Part B)**. I gestured at taste-
   training-on-its-own-priors. GPT named it crisply in one phrase
   that survived into the stage-1 synthesis and into Pattern F's
   mitigation design. Good framings are force multipliers.
3. **"Which failure hurts more — missed work or false positives?"
   (S1A Part C).** GPT asked the core product-tradeoff question in
   S1A. I did not. The operator's answer ("更怕漏报") became binding
   in S2 and shaped every direction's recall-first architecture. I
   would have gotten to it eventually; GPT got there first.
4. **Precision-gate on the mismatch section (S3R1 §5 D2).** My S3R1
   headlined "claim-method mismatches this cycle" as a named briefing
   section from day 1. This was Galactica-shaped — Pattern B in the
   synthesis — and I'd convinced myself it wasn't. GPT caught it,
   built a clean precision-gate hinge, and I conceded in S3R2. A
   *named* feature is a *trust* surface; earn the name. I should
   have seen this, and didn't.

Bonus (arguably a 5th): **GPT's S2R1 was shorter and tighter than
mine**. My S2R1 was 361 lines; theirs was 136. Both passed protocol
bars. Mine had more content but also more surface area to defend. In
S3, GPT's product frame (triage + memory + audit, not "AI that judges")
became the frame I adopted.

## 7. Where I was stronger than GPT

Calibrated confidence, same criterion:

1. **Specific prior-art catalog (S1A).** I named 10+ existing tools
   from memory (arxiv-sanity, Connected Papers, Semantic Scholar,
   Elicit, Scite, Consensus, Scholarcy, Mem, Rewind, Augmend). GPT
   named categories. My specificity generated more falsifiable
   claims — some of which got falsified ("the graveyard is deep" was
   wrong; the tools fragmented into a stack). But falsifiable claims
   drive better debate than abstract ones, and the specifics gave
   S1B real landmarks to evaluate against. GPT's own S1B catalog was
   thinner because of this asymmetry.
2. **Quantitative engineering specs in S3R2.** GPT's S3R1 said "rank
   transparently"; I shipped a 4-signal ranker spec with defaults,
   half-life tunables, and a filter-bubble-safe training constraint.
   GPT's S3R1 said "feedback mechanism"; I specified Obsidian
   frontmatter blocks + nightly parse + MCP tool + a completion-rate
   target. GPT's S3R1 said "small labeled set"; I wrote a 3-step
   harvest protocol that works whether the operator has 10 examples
   or zero. GPT acknowledged this directly in his S3R2 §0: "Opus's
   S3R2 materially narrowed the debate... added the engineering
   detail that both R1s were missing."
3. **Cold-start reasoning (S3R2 §2.5)**. Neither of us priced the
   first 7 days of operation in R1. I did it in R2 and GPT adopted
   it as his R2 concession #1. "Week 1 must end with a seeded
   corpus, a first intentionally-wrong briefing, and a labeling
   loop, not merely with ingestion adapters online." This is the
   anti-pattern that would have silently killed this build.
4. **Legal surface instinct (S1A Part B → S1B)**. GPT did not raise
   the legal/ethical surface at all. I flagged blog-scraping as a
   gray zone in S1A; S1B defused arxiv concerns (permissive ToS)
   and confirmed blog ambiguity; my instinct was directionally
   right and shaped the "curated blog whitelist with robots.txt
   strict" posture the final spec carries.

Bonus 5th: **Willingness to withdraw my own claims**. My S1A had a
"3–5x throughput multiplier" that was confabulated; I withdrew it in
S1B §4. GPT never made a number that concrete, so had nothing to
withdraw. That's a methodological difference, not a victory — but the
willingness to say "I said this and had no basis" is a skill I want to
keep practicing.

---

## 8. Top 5 actionable recommendations for the moderator (operator)

Prioritized, each with recommendation / why / effort / risk-if-skipped.

### Recommendation 1 — Run Phase 0 (3 days) before committing the 8-week build
- **Why**: de-risks the two assumptions most likely to change the plan
  (Haiku triage quality, hybrid retrieval install cost). Also resolves
  residual disagreement 5.1 for free.
- **Effort**: 3 days, 1 architect + 1 junior.
- **Risk if skipped**: commit to an 8-week plan whose cost model and
  week-1 gate depend on unverified assumptions. Worst case: week 4
  discovery that triage quality is below bar, forcing mid-build
  Sonnet escalation that doubles the LLM line and triggers a scope
  conversation under time pressure.

### Recommendation 2 — Treat the GEPA case as gold and collect ≥10 historical mismatch cases by end of week 2
- **Why**: the mismatch detector is the most novel v1 feature and the
  most dependent on operator-provided ground truth. Q-M4 supplied
  one case (GEPA); the detector needs ≥10 positives + ≥10 negatives
  + ≥5 controls to earn its named section.
- **Effort**: 2–4 hours of the operator's time over 2 weeks, or the
  synthetic-generation harvest (§2.9) does the heavy lifting and
  operator reviews.
- **Risk if skipped**: mismatch detector ships noisy or doesn't ship
  at all; the v1 feature most likely to change operator behavior
  becomes a trace-level column nobody surfaces.

### Recommendation 3 — Commit to 8-week build-to-green-then-stop; do NOT widen scope during the build
- **Why**: synthesis §8's "personal-tool-with-publishable-internals,
  not a unicorn" framing. Every widening (multi-user, web UI, idea
  graph now, X as v1 dependency, enterprise pivot) dilutes the
  narrow defendable wedge. The discipline of saying no is the
  product's survival condition.
- **Effort**: 0; it's a governance commitment.
- **Risk if skipped**: week-4 or week-6 "wouldn't it be great if..."
  conversations add scope; the 8-week plan becomes 16 weeks;
  operator loses patience before shipping; tool joins Pattern A
  (useful-but-niche plateau) with no recovery.

### Recommendation 4 — After 4 weeks of live use, do the 3-arm cadence experiment and the "have I stopped using Semantic Scholar Research Feeds?" check
- **Why**: the cadence experiment resolves residual disagreement 5.2.
  The Research-Feeds check is the honest "would I actually still
  build this?" retrospective. If after 4 weeks the operator is
  still reading Research Feeds + Zotero + papersgpt-for-zotero as
  his primary surface, the system has failed its success criterion
  and should either pivot hard or be retired.
- **Effort**: 6 weeks passive observation + 1 hour of introspection.
- **Risk if skipped**: no falsification discipline. The system lives
  because "it's there," not because "it works." Pattern A.

### Recommendation 5 — Pre-commit to v1.5 scope bounds; specifically, idea-graph auto-clustering requires ≥50 hand-authored idea candidates first
- **Why**: keeping Direction B's upgrade path viable is worth a
  small v1 tax; acting on it before there's training data is
  Pattern E (novelty-scoring fragility) applied to idea-lineage
  claims. The bar "operator has hand-authored 50+ idea candidates
  over 3 months" is the data-availability gate that keeps the
  upgrade honest.
- **Effort**: 5 minutes to write the gate into `projects/002-*/README.md`.
- **Risk if skipped**: v1.5 enthusiasm ships auto-clustering prematurely,
  false merges poison the graph, operator trust in the whole system
  drops.

---

## 9. What I would want to know before shipping

5 open questions the moderator must still answer (interviews,
prototypes, retrospective discipline):

1. **(Prototype) Phase 0 day-1 result**: what's Haiku triage accuracy
   on 100 papers' claim/method spans? If <80%, the cost model
   changes before build. (Reco 1.)
2. **(Operator time budget) Can the operator actually provide ≥10
   historical mismatch examples by end of week 2?** If not, the
   synthetic harvest (§2.9 step 1) carries the load, but precision
   gate is harder to pass. (Reco 2.)
3. **(Operator preference) One-file-per-briefing-cycle vs.
   living-page-per-topic in Obsidian?** Both are generable from the
   schema; operator primary-navigation preference decides. Small
   decision, but affects how the vault grows over 2 years.
4. **(Metric calibration) After 4 weeks, has the operator actually
   stopped opening Semantic Scholar Research Feeds?** Hardest
   question to answer honestly; most important. If Research Feeds
   is still the default surface, we built the wrong product.
   (Reco 4.)
5. **(Legal posture) For any AI-lab blog the operator wants to add
   to the whitelist (Anthropic / OpenAI / DeepMind /
   ThinkingMachines), what's the robots.txt + reasonable-crawler
   posture?** S1B defused arxiv; blogs remained ambiguous. One
   mis-step here is a reputational surface, not a legal one, and
   reputational surfaces propagate.

Three questions I would previously have asked but the moderator has
already answered (don't re-ask):
- ~~Written topic list?~~ Q-M1: 8 topics supplied.
- ~~Project state discipline?~~ Q-M2: no.
- ~~X dependency?~~ Q-M3 + operator note 3: no, v2 hook.

---

## 10. Signing off

**I believe this proposal is ready for SDD conversion.**

The architecture converged; 10 concrete commitments between Opus and
GPT (§4); 2 residual disagreements that are launch experiments, not
architectural doubt (§5); a gated 8-week build plan with 3 explicit
milestones; a Phase 0 spike to de-risk the two remaining assumptions;
top-5 recommendations the moderator can execute.

One honest caveat I will not bury: this is a **personal tool with
publishable internals**, not a category-creating product. If the
moderator ships it expecting a unicorn, the recommendation is
miscalibrated. If the moderator ships it expecting a tool that makes
one specific lab's research surveillance 2–3x more reliable and 3–5x
more traceable, while also producing a defensible claim/method-
mismatch detector on AI-research-specific data that could be written
up as a short paper — that is the product this plan actually builds.
The standing novelty (synthesis §8) is narrow but non-empty, and the
build plan respects that narrowness.

Proceed to `/debate-conclude 002` when GPT's final lands.

---

### One-line summary

**Final: A-primary topic-ledger-briefing on B-compatible append-only
schema with D (7 MCP tools) from day 1; 8-week gated build with Phase 0
spike; briefing = reading surface / inbox = recall guarantee; framings
not scores; mismatch detector earns its named section via precision
gate; 2 residual disagreements are launch experiments not architecture;
READY FOR SDD CONVERSION.**
