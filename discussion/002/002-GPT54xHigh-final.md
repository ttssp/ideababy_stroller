# Idea 002 · Final Position · GPT-5.4 xhigh

**Timestamp**: 2026-04-23T11:30:00+0800
**Basis**: I read every `*.md` file in `discussion/002/` and consolidated Stage 1, Stage 2, moderator answers, and all Stage 3 converge rounds.
**Standard**: no new speculation; only the strongest conclusions that survived the record.

---

## 1. Final recommendation (5 bullets)

- **Build this, conditionally, as a lab-internal tool only.** Do not frame it as a broad product category. The defensible wedge is narrow and lab-specific.
- **Ship A-primary**: a topic-ledger briefing system for the operator's 8-15 evolving topics, with **B-compatible schema** preserved from day 1 and **D (MCP surface)** exposed alongside from v1.
- **Keep v1 recall-first, audit-first, and open-access-only.** Briefing is the reading surface; inbox is the recall guarantee; all outputs must trace back to source artifacts and evidence spans.
- **Do not ship autonomous novelty scoring or live X ingestion in v1.** Novelty can exist only as an advisory hint; X remains an adapter boundary and schema stub, not a dependency.
- **Advance only with explicit launch gates and stop conditions.** If by the end of the early live phase this does not materially improve the operator's Monday/Friday workflow, the honest move is to stop widening scope.

---

## 2. Full technical proposal

### 2.1 Product definition

- The product is **not** "an AI that judges the research frontier for me."
- The product **is** a **research memory and triage substrate** that makes judgment cheaper, more traceable, and less lossy.
- Its core user is the operator first, then trusted lab members second.
- Its bounded scope is the operator's **8-15 standing topics**, with yearly churn supported explicitly.
- Its job is to:
  - ingest public research artifacts,
  - link them to tracked topics,
  - generate structured framings,
  - compile Mon/Fri briefings,
  - preserve a queryable recall trail,
  - let the operator audit, challenge, and correct the system.

### 2.2 What the system should optimize for

- **Recall over precision**, because the moderator explicitly prefers misses to be rarer even if some noise remains.
- **Traceability over rhetorical smoothness**, because Stage 1 showed that fluent science-facing AI without grounding is a trust killer.
- **Workflow change over demo quality**, because this category's most common failure mode is "useful utility that never becomes habit."
- **Schema discipline over premature graph ambition**, because idea-level provenance is valuable but too expensive to make authoritative in v1.

### 2.3 Product surfaces

- **Surface 1: Obsidian briefings**
  - Monday briefing: synthesis cycle.
  - Friday briefing: delta cycle.
  - Same visible template on both days.
  - Short, opinionated, readable.
  - Each item links to traceable evidence.

- **Surface 2: MCP query interface**
  - Pull-based surface for mid-week interrogation.
  - Reads from the same normalized store as the briefing compiler.
  - No separate web UI in v1.

- **Surface 3: Queryable inbox**
  - Not a linear reading surface.
  - Exists as the recall guarantee and audit trail.
  - Lets the operator ask "did we see this?" and "why did it rank this way?"

### 2.4 Source scope

- **In scope for v1**
  - arXiv
  - OpenAlex
  - Semantic Scholar lookup
  - OpenReview when relevant venues are live
  - GitHub trending / selected repos
  - curated public blog whitelist

- **Out of scope for v1**
  - paywalled papers
  - live X ingestion
  - broad web crawling
  - internal lab docs unless explicitly added later

### 2.5 System architecture

```text
Public sources
  -> ingest + normalize
  -> append-only ledger store
  -> ranking + framing derivations
  -> briefing compiler + MCP tools
  -> operator feedback
  -> ranker / framing improvements
```

### 2.6 Pinned stack

- **Runtime**: Python 3.12 via `uv`
- **Database**: PostgreSQL 16
- **DB features**:
  - JSONB
  - `pg_trgm`
  - `pgvector` installed and evaluated through Gate A.5
- **DB layer**: SQLAlchemy 2.x + Alembic
- **Scheduler**: cron / simple worker entrypoints
- **HTTP + ingest**: `httpx`, lightweight source clients, conservative blog fetching
- **Parsing**: lightweight text extraction only in v1
- **MCP**: Python MCP SDK over stdio
- **Tests**: `pytest`
- **Lint / format**: `ruff`
- **Output sink**: Obsidian markdown files
- **No v1 web app**
- **No separate vector database**
- **No workflow orchestrator**

### 2.7 Data model

- `topic`
  - first-class tracked subject
  - states: `candidate | active | archived`
  - lifecycle-aware

- `artifact`
  - canonical paper / repo / blog / discussion-thread record
  - source metadata lives here

- `artifact_version`
  - immutable snapshots
  - source changes do not erase prior evidence

- `topic_artifact_link`
  - append-only topic association history
  - captures when and why an artifact entered a topic

- `framing`
  - immutable structured interpretation of an artifact in a topic context
  - includes:
    - claim
    - method
    - why it matters
    - possible overclaim
    - adjacent prior work
    - mismatch hint
    - model / prompt version

- `evidence_span`
  - field-level provenance for framing claims

- `briefing_cycle`
  - dated cycle object
  - includes `cycle_kind = synthesis | delta`

- `briefing_item`
  - what entered a briefing
  - section, rationale, rank, ranker version

- `rank_signals`
  - lex score
  - semantic score
  - recency score
  - centroid shift
  - ranker version

- `feedback`
  - `useful | noise | missed | wrong_frame | should_track_topic`
  - can come from Obsidian or MCP

- `idea_candidate`
  - reserved v1 structure for B-compatibility
  - non-authoritative
  - operator-authored only in v1

- `idea_candidate_member`
  - operator-confirmed artifact membership only

### 2.8 B-compatibility rule

- Preserve the schema needed to evolve into idea-level provenance later.
- Do **not** let that reserved structure become a hidden v1 dependency.
- No artifact should require an `idea_candidate` assignment to:
  - appear in a briefing,
  - appear in inbox results,
  - appear in MCP search.
- No automated cross-artifact clustering drives the product in v1.

### 2.9 Retrieval and ranking

- The ranker should be **transparent** and built from interpretable signals.
- Default v1 formula:

```text
rank =
  w1 * lexical_score +
  w2 * semantic_score +
  w3 * recency_score +
  w4 * centroid_shift +
  optional small bias terms
```

- Default posture:
  - no novelty score as a primary rank key
  - no click-trained taste model in v1
  - no silent filtering
  - all artifacts remain queryable

- Retrieval decision:
  - hybrid retrieval is **not** a week-1 blocker
  - hybrid retrieval **is** a v1 candidate, decided by Gate A.5
  - if hybrid materially improves recall on the labeled set, it stays
  - if it does not, v1 ships without semantic retrieval in the ranker

### 2.10 Framing over scoring

- The primary product object is a **framing**, not a scalar verdict.
- Briefings should say:
  - what the artifact claims
  - what method it actually uses
  - why it matters to the tracked topic
  - what prior work or adjacent work matters
  - whether there is a possible mismatch or overclaim

- Briefings should **not** lead with:
  - novelty score
  - impact score
  - "trust this paper" score

### 2.11 GEPA-class mismatch handling

- The debate converged that GEPA-like cases are important.
- The correct v1 posture is:
  - store `mismatch_hint` on every artifact framing
  - keep it trace-level at first
  - promote to a named briefing section **only after** it clears a precision gate

- Promotion rule:
  - precision@10 >= 0.7
  - and at least half of top flagged cases judged genuinely useful by the operator

- If it fails:
  - keep it as a trace-level field
  - do not headline it socially

### 2.12 Briefing design

- **Monday**
  - synthesis cycle
  - answer: what is the state of the topic now?

- **Friday**
  - delta cycle
  - answer: what changed since Monday that I should not miss?

- Both should:
  - use the same visible markdown template
  - read similarly to the operator
  - differ semantically in what they are allowed to include

- Friday carryovers should be treated as an experiment:
  - allowed only when materially re-framed or changed
  - evaluated after launch rather than argued in advance

### 2.13 MCP tools

- `radar.topic.briefing(topic, cycle?)`
- `radar.topic.inbox(topic, since?, limit?)`
- `radar.topic.delta(topic, since_cycle?)`
- `radar.topic.contrarian_view(topic, since?)`
- `radar.artifact.trace(artifact_id)`
- `radar.search(query, topic_filter?, since?)`
- `radar.health()`
- `radar.feedback.record(...)`

### 2.14 Feedback capture

- **Primary path**: edit lightweight feedback blocks inside Obsidian briefing items
- **Secondary path**: record feedback during MCP use in Claude Code / Codex
- No separate feedback UI in v1
- The metric should be realistic for a solo operator:
  - at least 8 labeled items per cycle
  - at least 3 corrective labels every 2 weeks

### 2.15 Trust rules

- Append-only evidence
- Versioned framings
- Ranker version on briefing items
- Evidence spans on framing statements
- No silent source failure
- `radar.health()` must expose source outages and backlog state
- Every promoted feature needs a real evaluation gate before it becomes a social claim

### 2.16 What is explicitly out of v1

- No web dashboard
- No paywalled source support
- No live X ingestion
- No automated idea graph
- No authoritative cross-artifact identity resolution
- No autonomous novelty scoring
- No fine-tuned local models
- No project-linked primary workflow, because project state does not exist today

---

## 3. MVP plan (Phase 0/1/2)

### Phase 0 · Foundation and cold start

**Goal**

- prove the system can ingest, trace, label, and produce a first intentionally-imperfect briefing worth reacting to

**Deliverables**

- 8 seed topics loaded from moderator answers
- 90-day topic-scoped backfill
- core tables live:
  - topic
  - artifact
  - artifact_version
  - topic_artifact_link
  - framing
  - evidence_span
  - briefing_cycle
  - briefing_item
  - feedback
  - idea_candidate
  - idea_candidate_member
  - rank_signals
- first cold-start briefing generated from backfill
- artifact trace works end-to-end
- operator can label at least 20 seed items
- ranker version and cost telemetry are stored from the start

**Gate A**

- if the operator cannot react to a real seed briefing, Phase 0 is not done

**Gate A.5**

- run lexical vs semantic vs hybrid retrieval on the seeded labeled set
- if hybrid improves recall materially, keep it
- if not, do not let it bloat v1

### Phase 1 · Live topic radar

**Goal**

- turn the cold-start substrate into a live Mon/Fri workflow across all tracked topics

**Deliverables**

- live ingestion for:
  - arXiv
  - OpenAlex
  - Semantic Scholar lookup
  - OpenReview where relevant
  - GitHub
  - curated blogs
- framing pipeline operational
- mismatch hint stored on every artifact
- first live Monday and Friday briefings
- MCP tools available from the same store
- feedback sync working from Obsidian and MCP
- labeled set for mismatch evaluation has:
  - at least 10 genuine mismatches
  - at least 10 not-genuine or borderline cases
  - at least 5 flashy-but-method-aligned controls

**Gate B**

- mismatch remains trace-level until it clears the precision gate

**Gate C**

- Mon/Fri cadence is live
- operator is still opening the briefings
- minimum feedback quotas are being met

### Phase 2 · Hardening and bounded extension

**Goal**

- harden the workflow without widening scope into a different product

**Deliverables**

- topic lifecycle commands
- contrarian view tool
- cost tuning
- backup / restore
- source health reporting
- X adapter stub present but off
- reserved B-compatible structures preserved and documented

**Permitted Phase 2 experiments**

- Friday carryover policy experiment
- cheaper triage model swap if quality holds
- operator-authored idea candidates

**Not a Phase 2 goal**

- full idea graph
- live X ingestion
- web UI
- project-linked workflow pivot

---

## 4. Consensus with Opus (strict)

- We both end at **Y, conditionally**, not unconditional enthusiasm.
- We both agree this should be built as a **lab-internal tool**, not as a general market thesis.
- We both agree the surviving v1 direction is **A-primary**.
- We both agree **B-compatible schema** should be preserved from day 1.
- We both agree **D / MCP alongside from v1** is correct.
- We both agree **project-linked radar is not v1** because project state does not currently exist.
- We both agree the system should be **open-access-only** in v1.
- We both agree **X stays a stub / adapter boundary**, not a live dependency.
- We both agree the system must be **recall-first**.
- We both agree the **briefing is the reading surface**.
- We both agree the **inbox is the recall guarantee**, not something the operator reads linearly.
- We both agree the product should ship **framings, not authoritative scores**.
- We both agree **autonomous novelty scoring is out** as a primary ranking signal.
- We both agree the store should be **append-only and auditable**.
- We both agree `artifact_version`, `evidence_span`, `ranker_version`, and rank signals should be first-class.
- We both agree **mismatch_hint** belongs in the schema.
- We both agree a named mismatch section must be **gated by evaluation** before promotion.
- We both agree the core store should feed both the briefings and the MCP tools.
- We both agree the v1 MCP surface includes briefing, inbox, search, trace, delta, health, and feedback paths.
- We both agree hybrid retrieval is a **launch experiment**, not a philosophical debate.
- We both agree Monday and Friday should share **one visible template**.
- We both agree Friday has **delta semantics** even if the template is stable.
- We both agree the build needs explicit early **gates**, not just a loose week-by-week narrative.
- We both agree the build should stop or narrow if it does not change the operator's Mon/Fri workflow quickly.

---

## 5. Residual disagreements + honest verdict

### Residual disagreement 1: hybrid retrieval timing

- My earlier position: hybrid belongs in v1, but should not block week 1.
- Opus's earlier position: hybrid should land immediately because recall-first without it risks breaking on cross-phrased cases.
- Honest verdict:
  - the merged answer is better than either pure position
  - Opus was right that semantic retrieval is probably necessary for the long-run promise
  - I was right that it should be decided by a seed-corpus eval, not forced into week-1 blocking scope
  - final answer: decide it through Gate A.5, then commit

### Residual disagreement 2: Friday semantics

- My earlier position: Friday should be treated as a delta cycle
- Opus's earlier position: Friday should keep the same visible structure and not become a different product shape
- Honest verdict:
  - both positions survived
  - I was more right on the data-plane semantics
  - Opus was more right on the UX consistency
  - final answer: same template, delta semantics, carryover policy tested after launch

### Residual disagreement 3: none at architectural level

- By the end of Stage 3, there is no meaningful architectural disagreement left between us.
- What remains are **scheduled launch experiments**, not unresolved identity questions.

### Honest overall verdict

- The merged plan is worth advancing.
- It is also narrower than the original dream and should stay narrow.
- If the operator is secretly hoping for a full research chief-of-staff in v1, this plan is too conservative.
- If the operator wants a reliable internal radar that earns trust step by step, this plan is the right one.

---

## 6. Where Opus was stronger than me (≥2)

- **Cold-start execution discipline**
  - Opus got to the operational truth faster: week 1 must end with a seeded corpus, a seed briefing, and labeling, not merely "ingestion exists."

- **Concrete ranking and retrieval mechanics**
  - Opus pushed harder on rank signals, ranker versioning, and why pure lexical retrieval would likely miss GEPA-class cross-phrased cases.

- **Math on inbox scale and cost**
  - Opus forced the volume and cost estimate into the record earlier and more concretely than I did.

- **Build-sequence realism**
  - Opus was better at decomposing the debate into an actual week-by-week engineering path before I translated it into gates.

- **Defending the operator's existing rhythm**
  - Opus was quicker to take the moderator's Mon/Fri reading cadence literally and design around it rather than abstracting it into a generic workflow pattern.

---

## 7. Where I was stronger than Opus (≥2)

- **Product trust boundaries**
  - I was more disciplined early about reframing the product as memory + triage + audit, rather than an AI that issues frontier verdicts.

- **Mismatch feature restraint**
  - I was more right to insist that GEPA-style mismatch detection must stay trace-level until it clears a promotion gate.

- **Gate framing**
  - I improved the Stage 3 artifact by turning architecture talk into moderator-readable launch gates rather than only week-by-week narrative.

- **Semantic distinction for Friday**
  - I was more precise about why Friday should differ semantically even if it keeps the same visible template.

- **Keeping B-compatible from becoming B-dependent**
  - I pushed more explicitly on the invariant that no artifact should require idea-candidate assignment to enter briefing, inbox, or search.

---

## 8. Top 5 actionable recommendations for moderator

1. **Advance exactly this scoped direction, not a broader one.**
   A-primary, B-compatible, D-alongside, internal-only, open-access-only.

2. **Require the spec to encode Gates A, A.5, B, and C explicitly.**
   Do not let Stage 3 conclusions become a vague implementation wishlist.

3. **Define the kill criteria now.**
   If the operator is not still opening and correcting Mon/Fri briefings by the live phase, stop widening scope.

4. **Require the build to compare itself against the real current workflow.**
   The honest baseline is not "nothing"; it is the operator's current Mon/Fri process plus existing public tools.

5. **Keep the debate's trust constraints in the spec as non-negotiables.**
   No novelty score as primary rank key.
   No live X dependency.
   No named mismatch section before it earns one.

---

## 9. Open questions moderator must answer

These are not debate blockers, but they should be answered in spec/build planning rather than left implicit.

- **What is the canonical Obsidian output shape?**
  - file-per-cycle
  - living page per topic
  - or both, with one canonical and one convenience view

- **How should feedback sync run in v1?**
  - nightly cron
  - or live file-watcher

- **Can the operator provide 5 seed papers per topic quickly, or should the build assume automatic bootstrap seeds?**

- **Can the operator review and confirm the mismatch eval set by week 3?**
  - if not, the named mismatch feature should be deferred explicitly

- **What exact workflow change counts as success by Gate C?**
  - fewer manual source scans
  - better recall of relevant work
  - faster "is this actually what it claims?" judgments
  - all three should be made concrete in the spec

- **What 4090 availability window is actually guaranteed?**
  - the debate assumed local embedding / retrieval support without challenging lab resource contention

---

## 10. Sign-off

**Ready for SDD**

Reason:

- the architecture is converged,
- the remaining uncertainties are explicit experiments inside the build,
- the scope is narrow enough to spec honestly,
- and the trust boundaries are now clear enough to survive implementation.
