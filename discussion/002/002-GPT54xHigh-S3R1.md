# Idea 002 · S3R1 · GPT54xHigh · Converge (engineering)

**Timestamp**: 2026-04-23T10:10:41+0800
**Stage**: 3 (Converge). Mode: engineering.
**Moderator choice carried in**: **ADVANCE** with **Direction A-primary (topic-ledger-briefing)** on a **B-compatible schema**, with **D (MCP surface) exposed alongside from v1**.
**Reads**: `002-stage2-checkpoint.md`, `002-moderator-notes.md`, `002-Opus47Max-S2R1.md`, `002-GPT54xHigh-S2R1.md`, `002-Opus47Max-S3R1.md`.

---

## 0. Context carried into Stage 3

The moderator answers close several Stage 2 branches and sharpen the engineering target:

- **Q-M1** gave 8 seed topics immediately. That removes "topic discovery UI" from v1. We can start with a pinned topic ledger and earn the right to build better topic-management later.
- **Q-M2** is "no project state." That matters a lot. It confirms the checkpoint's A-primary recommendation and means we should not smuggle Direction C requirements back into v1 through the side door.
- **Q-M3** says the operator reads on **Monday morning and Friday morning**, from X pushes, arXiv pushes, conference lists, blogs, and GitHub. That is enough to justify a push surface, but it does **not** automatically imply two full briefings of equal weight.
- **Q-M4** gives a named pain case: **GEPA looked like agent self-evolution but was really prompt optimization**. This is the most valuable concrete grounding we have. It says the product must help detect **claim/method mismatch**, not just rank "interesting" artifacts.
- **Q-M5** says to keep the **B-schema upgrade path from day 1**. I agree. The schema should preserve room for idea-level entities even if v1 does not yet build an authoritative idea graph.

My updated frame is:

- v1 is a **topic-ledger system with a briefing compiler and an MCP query surface**.
- The product promise is **coverage, traceability, and faster judgment**, not autonomous judgment.
- B-compatibility is a **schema discipline**, not a reason to ship B's entity-resolution problem in v1.

---

## 1. Steelman of Opus's strongest point

Opus's strongest point in S3R1 is this:

> **The inbox is not meant to be read linearly; it is the recall guarantee. The briefing is the linear reading surface.**

Why I think this is the right correction:

- It resolves the core tension in "recall-first" honestly. If we promise high recall, the raw artifact volume will be too large for a human to read directly.
- It turns the inbox from a UX liability into a product guarantee. The user is not being asked to scan 1,000+ items per week; the user is being promised that the system **saw them and can surface them on demand**.
- It keeps the product from drifting into fake precision. A tiny filtered list would feel cleaner, but it would violate the moderator's explicit preference to avoid misses.

I am adopting this framing. It changes the product language and the success metric:

- **Briefing success**: "Did this save reading time and change what I paid attention to this week?"
- **Inbox success**: "When I ask about a thing, can the system show me that it saw it, how it framed it, and why it ranked it the way it did?"

That is concession #1 in §6.

---

## 2. New ground: architecture

### 2.1 Architectural posture

I want the architecture to be opinionated in four ways:

1. **Append-only evidence first**
   Every ingest event, extracted framing, and generated briefing item should have durable provenance. We can update derived views, but we should not lose the original observation trail.

2. **Topic ledger first, idea graph later**
   v1 should organize around topics because that is what the operator can supply today. B-compatibility should live in the schema through reserved idea-level entities and trace tables, not through premature graph resolution.

3. **One store, two surfaces**
   A-primary and D-alongside only stay cheap if briefing generation and MCP answers are reading from the same normalized store.

4. **Human-legible judgment artifacts**
   The system should save structured framings such as `claim`, `method`, `why-it-matters`, `why-it-might-be-overclaimed`, and `adjacent-prior-work`, rather than opaque scores as the primary object.

### 2.2 System shape

```text
Sources
  arXiv / OpenAlex / OpenReview / GitHub / curated blogs / X-adapter stub
    ->
Ingest + Normalize
  dedupe, source metadata, raw text snapshots, artifact versions
    ->
Ledger Store
  topics, artifacts, topic-artifact links, framing records, evidence spans,
  briefing cycles, feedback, reserved idea candidates
    ->
Derivations
  ranking, delta detection, mismatch hints, briefing candidate sets
    ->
Surfaces
  1. Mon/Fri topic briefings in Obsidian markdown
  2. MCP tools for query / trace / audit / health
```

### 2.3 Schema shape (B-compatible without pretending B is shipped)

Pinned core entities:

- `topic`
  Stable identifier, display name, status (`candidate|active|archived`), seed keywords, seed artifacts, created/archived timestamps.

- `artifact`
  Canonical artifact row for paper / repo / blog / post / discussion thread, with source URL, source type, authorship fields, publication timestamp, fetch timestamp, and normalized text pointers.

- `artifact_version`
  Immutable content snapshots so regenerated framings stay auditable if the source changes.

- `topic_artifact_link`
  Many-to-many link with `relevance_score`, `relevance_reason`, `link_state`, and `first_seen_at`.

- `framing`
  Structured output for an artifact in a topic context:
  `claim`, `method`, `delta_from_prior`, `why_relevant`, `mismatch_hint`, `confidence`, `model`, `prompt_version`.

- `evidence_span`
  Optional source spans or field-level provenance used to support a framing sentence.

- `briefing_cycle`
  A dated cycle record, probably keyed by `2026-04-27-mon` or `2026-05-01-fri`.

- `briefing_item`
  The ranked artifacts selected for a topic's briefing in a given cycle, plus section placement and rationale.

- `feedback`
  Operator judgments like `useful`, `missed`, `noise`, `wrong-framing`, `should-track-topic`.

- `idea_candidate`
  Reserved upgrade entity for B. It can store tentative clustering and cross-artifact relations, but in v1 it should be explicitly marked **non-authoritative** and non-blocking.

This gives us a real B-compatible substrate without forcing v1 to solve cross-artifact identity resolution.

### 2.4 Pinned stack

- **Language/runtime**: Python 3.12, `uv`
- **Application structure**: small Python service + worker processes, not a web app
- **Database**: PostgreSQL 16 with `pg_trgm`, full-text search, JSONB; install `pgvector` extension now but gate semantic retrieval use by milestone
- **ORM / DB layer**: SQLAlchemy 2.x + Alembic
- **Scheduler**: `cron` plus a single worker entrypoint; no workflow orchestrator in v1
- **HTTP / ingestion**: `httpx`, `trafilatura`, source-specific lightweight clients
- **Parsing**: `pypdf` for text extraction where needed; avoid heavyweight document pipelines in v1
- **Models**:
  - first-pass extraction/framing: `Claude Haiku 4.5`
  - briefing synthesis: `Claude Sonnet 4.6`
  - embeddings: local `BGE-M3` on the 4090 once semantic retrieval clears the milestone gate
- **MCP surface**: Python MCP SDK over stdio
- **Testing**: `pytest`
- **Lint/format**: `ruff`
- **Output sink**: Obsidian markdown files with dated paths, plus MCP responses

Pinned product choices:

- no dedicated web UI
- no separate vector database
- no queueing platform
- no autonomous scoring as a primary output

### 2.5 Surface design

The two v1 surfaces should be intentionally asymmetric:

- **Briefing surface**
  Push-oriented, readable, opinionated, short.

- **MCP surface**
  Pull-oriented, traceable, longer, queryable.

I would expose these MCP tools in v1:

1. `radar.topic.briefing(topic, cycle?)`
2. `radar.topic.inbox(topic, since?, limit?)`
3. `radar.search(query, topic_filter?, since?)`
4. `radar.artifact.trace(artifact_id)`
5. `radar.topic.delta(topic, since_cycle?)`
6. `radar.health()`

I would treat `what_am_i_missing` as valuable but second-tier. It can be present in v1 if it is cheap to add after baseline ranking is stable; it should not delay shipping the core query and trace surfaces.

---

## 3. MVP

### 3.1 IN

What I think belongs in v1:

- 8 seed topics from Q-M1 as pinned configuration
- ingest from arXiv, OpenAlex, OpenReview when relevant, GitHub, and a curated blog list
- X represented as a schema and adapter boundary only, not a live ingestion path
- append-only artifact capture with durable source metadata
- topic-artifact linking with transparent relevance reasons
- structured framings per artifact:
  `claim`, `method`, `why this matters`, `possible overclaim`, `related prior work`
- Mon/Fri briefing generation into Obsidian
- MCP tools for briefing retrieval, inbox/query, trace, delta, and health
- operator feedback capture on briefing items and artifact framings
- topic lifecycle states: `candidate`, `active`, `archived`
- B-compatible reserved schema for `idea_candidate` and relation traces
- lightweight mismatch hinting for GEPA-like cases as an artifact-level field

### 3.2 OUT

What should stay out of v1:

- full idea graph population
- authoritative cross-artifact entity resolution
- any dedicated dashboard or web frontend
- X ingestion as a dependency
- paywalled content
- project-linked workflows that assume formal project state
- personalized taste learning beyond explicit topic configuration and simple feedback
- heavy claim that the system can score novelty or importance robustly
- making the mismatch detector a hero feature before it clears an evaluation bar

---

## 4. Top 3 risks

1. **Topic breadth swamps trust**
   The 8 seed topics are broad and partially overlapping. If the first few cycles feel noisy, the operator may conclude the product is a fancy collector rather than a useful radar.

2. **B-compatible schema quietly grows into B-scope**
   The upgrade path is worth preserving, but it is easy to burn weeks building generic graph plumbing that v1 does not actually use. That would be the classic "future-proofing became present-day drag" failure mode.

3. **Mismatch detection overpromises early**
   GEPA is a strong motivating example, but one named example is not a validated feature class. If we headline mismatch detection too early and it fires noisily, we will damage trust in the entire briefing layer.

---

## 5. <=2 disagreements with testable hinges

### Disagreement 1: Monday should be the full briefing; Friday should start as a delta briefing

Opus argues for two full briefings because the operator reads Monday and Friday morning.

My view:

- Monday is the natural synthesis moment.
- Friday is better treated as a **delta surface** first: what changed, what spiked, what might change Monday's frame if you ignore it until next week.
- This preserves the operator's twice-weekly touchpoint without forcing symmetry that the workflow may not support.

Why I think this matters:

- Two full briefings risk duplicate structure and diluted significance.
- A Friday delta is cognitively lighter and may fit better with how people do end-of-week scanning.

**Testable hinge**:

- Run a 4-week experiment after v1 basic stability:
  - Variant A: Monday full + Friday full
  - Variant B: Monday full + Friday delta
- Track `open rate`, `items clicked/queried later`, and `explicit useful/noise feedback`.
- Keep the variant that wins on combined open rate and "useful" feedback.

### Disagreement 2: Do not elevate the GEPA-style mismatch detector to a named briefing section until it clears a precision gate

Opus wants claim/method mismatch to appear as a dedicated section early because it is the clearest pain case.

I agree it belongs in the architecture, but I would be more conservative in the product surface:

- v1 should store `mismatch_hint` on every artifact framing.
- The briefing can mention a mismatch only when confidence is high.
- The dedicated "headline/method mismatches" section should wait until the detector clears an evaluation threshold.

Why I think this matters:

- A noisy mismatch section will feel like the product is editorializing unreliably.
- The artifact trace surface is a safer place to accumulate evidence before we promote the feature socially inside the briefing.

**Testable hinge**:

- Build a small labeled set of at least 15 historical examples by week 3.
- Promote mismatch to a named briefing section only if precision@10 is at least 0.7 and at least half the top-10 flags are judged genuinely useful by the operator.
- If it misses that bar, keep it as a trace-level field in v1 and revisit in v1.5.

---

## 6. >=1 concession

### Concession 1

I am explicitly adopting Opus's framing that:

- the **briefing is the reading surface**
- the **inbox is the recall guarantee**

That is a better framing than my Stage 2 language, which still risked implying that the operator might directly browse the whole backlog as a normal workflow.

### Concession 2

I also concede that exposing **D alongside A from day 1** is worth doing, as long as it is genuinely thin and reads from the same store. The MCP surface is not optional garnish here; it is part of how the operator will actually interrogate the ledger during the week.

---

## 7. Self-critique

Three ways I may still be wrong:

- I may be underestimating how much semantic retrieval matters immediately. My instinct is to gate it behind evidence, but that could be too cautious for a domain with lots of cross-phrased terminology.
- My preference for a Friday delta may be overfitting to a generic knowledge-work pattern rather than this operator's actual reading habit.
- I am pushing fairly hard on append-only provenance because I think auditability is the product's spine, but there is a real chance that I am over-designing the storage layer for a v1 that mainly needs to feel useful quickly.

---

## 8. Three decision questions

1. **What is Friday, exactly?**
   Should Friday be treated as a second full synthesis pass, or as a lighter delta checkpoint meant to prevent Monday surprise?

2. **What is the minimum weekly feedback loop the operator will reliably do?**
   A v1 that captures `useful / noise / missed / wrong-frame` once or twice a week will improve much faster than one that waits for passive behavior alone.

3. **How much B-compatibility is enough for day 1?**
   Is the expectation merely reserved tables and traceability hooks, or is there a stronger desire to start tentative idea clustering immediately even if it is labeled experimental?

---

## 9. Bottom line

I support the moderator's direction:

- **A-primary** is the right v1 surface because the operator has topics but not formal project state.
- **B-compatible schema** is worth paying for, but only as reserved structure and provenance discipline.
- **D from v1** is correct because the operator's working surface is already agent-heavy.

My recommended product shape is:

- one normalized ledger store
- one push briefing surface
- one pull MCP surface
- transparent framings instead of fake-confidence verdicts
- cautious promotion of the GEPA-style mismatch feature until it proves itself

<!-- not READY-TO-CONCLUDE -->

Rationale for not marking READY-TO-CONCLUDE:
there is already good convergence on the primary direction, but two product hinges still deserve one more pass in engineering mode: briefing cadence and whether mismatch detection is a v1 headline feature or a v1 trace-level feature.
