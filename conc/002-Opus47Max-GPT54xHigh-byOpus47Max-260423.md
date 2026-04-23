# Conclusion — Idea 002 · Research Radar (lab-internal topic-ledger radar)

**Synthesized**: 2026-04-23
**By**: Opus (synthesizer)
**Sources**: 2 S1 rounds/side (S1A + S1B, 4 files total), 1 S2R1/side, 1 moderator-notes file with 4 binding answers + direction choice, 3 Opus S3 rounds + 2 GPT S3 rounds, 1 stage-1 synthesis, 1 stage-2 checkpoint, 2 `*-final.md` consolidations. Total ≈ 15 debate artifacts.
**Anchored on direction**: **A-primary (topic-ledger-briefing) on B-compatible schema, with D (MCP surface) exposed alongside from v1.** (Moderator's explicit pick in `002-moderator-notes.md`, line 7.)

## Moderator Checkpoint

Before this conclusion drives any spec work, the human operator must confirm:

1. **Are the 8 seed topics supplied in Q-M1 still the active-topic list as of spec-writing day, or has any of them already drifted?** Drift since 2026-04-23 would change seed-paper selection and ranker half-life defaults. This is the fragile input that the whole cold-start week-1 gate depends on.
2. **Will you personally spend ~3 hours across weeks 2–3 labeling the GEPA-style mismatch eval set (≥10 genuine + ≥10 not-genuine + ≥5 flashy-but-method-aligned controls)?** If no, the `MISMATCH WATCH` section cannot ship in v1 and must move to v1.5 — this should be pre-committed, not discovered at week 3.
3. **What single sentence defines v1 success at end of week 6 after Gate C?** Proposed default: "I have opened ≥8 of 12 Mon+Fri briefings and can name ≥2 specific instances where Radar caught something I would have missed." If you refuse to pre-commit a behavioral bar, Pattern A (useful-but-niche plateau) is the default failure mode — and the finals from both debaters call this out as the dominant risk that architecture cannot defuse.

---

## 0. Stage lineage (how we got here)

**Stage 1** ruled out generic "personalized daily paper feed" as the wedge (Semantic Scholar Research Feeds already ships adaptive personalization — GPT S1B catch, preserved in synthesis §7), ruled out autonomous novelty scoring as a primary signal (four benchmarks — NovBench, GraphMind, Literature-Grounded Novelty, DeepReview — show LLM novelty judgment is adversarially fragile), defused the arxiv legal concern (bulk/commercial use explicitly permitted), validated the firehose premise (~571/day all-arxiv in 2023, super-exponential growth through 2025), and identified the un-owned territory: a **lab-specific, topic-scoped radar with idea-migration provenance + active-project awareness + auditable verdicts + a serendipity valve**. **Stage 2** assembled four peer directions (A topic-ledger-briefing, B idea-provenance-graph, C project-linked-radar, D radar-as-MCP) and — after four binding operator answers (recall > precision; 8–15 topics with yearly ±2–3 churn; X is a v2 hook only; no paywalled content) — the moderator chose **Advance** with **A-primary on a B-compatible schema, D exposed alongside**. Q-M2 closed ("no project state exists") collapsed Direction C; Q-M1 supplied 8 concrete seed topics; Q-M4 named GEPA as the pain case. **Stage 3** took that direction into engineering: both debaters converged after two rounds on a single normalized Postgres ledger, append-only artifact/framing/evidence/link-state discipline, framings-not-scores as the primary output, recall-first briefing + inbox split, Mon synthesis + Fri delta cadence with a shared Obsidian template, hybrid retrieval decided at Gate A.5 (not argued), mismatch detection gated behind precision@10 ≥ 0.7 before getting its named section, and Obsidian-first feedback capture with a nightly `radar fb sync` cron.

---

## 1. Executive Summary

The project is a **lab-internal Research Radar** for a solo operator + 15-person AI lab, organized around 8 evolving standing topics. The path is a single normalized PostgreSQL ledger behind two asymmetric surfaces (an opinionated twice-weekly Obsidian briefing; a pull-based MCP tool set callable from Claude Code) that together deliver a recall-first memory + triage substrate — explicitly not an autonomous frontier-judgment system. The first shippable deliverable is an 8-week v0.1 gated by four binary checkpoints (Gate A at week 1 = seed corpus + cold-start briefing + labeling loop; Gate A.5 at week 2 = hybrid-retrieval in-or-out decision; Gate B at week 3 = GEPA-shaped eval set live with negatives + controls; Gate C at week 5 = twice-weekly cadence live with working feedback loop). Preceded by a 3-day proof-of-concept that decides model tier + cost viability on a single topic before the 8-week plan commits.

---

## 2. Core Consensus

Each bullet is a point both `002-Opus47Max-final.md` §4 and `002-GPT54xHigh-final.md` §4 explicitly committed to (grep-verified):

- **Build as a lab-internal tool only, Y-conditionally.** Not a product category. (Opus final §4 bullet 1; GPT final §4 bullet 1.)
- **A-primary is the v1 direction.** (Opus final §4 bullet 1; GPT final §4 bullet 3.)
- **B-compatible schema is preserved from day 1 but remains strictly non-authoritative** — no artifact may require an `idea_candidate` assignment to appear in briefing, inbox, or MCP search. (Opus final §4 bullets 1–2; GPT final §4 bullets 4 + §2.8.)
- **D (MCP surface) ships from v1 against the same underlying store**, not as optional garnish. (Opus final §4 bullet 3; GPT final §4 bullet 5.)
- **Open-access only in v1.** IEEE/ACM/bioRxiv-with-login out. (Operator answer 4, adopted in both Opus final §2.11 and GPT final §2.4.)
- **X remains an adapter-boundary + schema stub**, never a v1 live dependency. (Operator answer 3; Opus final §2.11; GPT final §4.)
- **Recall-first, never filter-first.** Briefing = reading surface (≤15 items × 2/week); inbox = recall guarantee (queryable via MCP, not scanned linearly). (Operator answer 1; Opus final §4 bullet 5 and §2.5; GPT final §4 + §2.3.)
- **Framings, not scores, as the primary product object.** `claim`, `method`, `why-it-matters`, `adjacent-prior-work`, `mismatch_hint` per artifact. No "novelty: 0.87" as primary sort key. (Opus final §2.10 and §4 bullet 4; GPT final §2.10 + §4.)
- **Autonomous novelty scoring is out** as a primary ranking signal; novelty can appear only as an advisory hint. (Stage-1 evidence anchor; Opus final §1 bullet 3; GPT final §2.9.)
- **Append-only ledger discipline.** `artifact_version`, `evidence_span`, `rank_signals`, `ranker_version` as first-class tables/columns; link-state transitions are new rows, not updates. (Opus final §2.3; GPT final §2.7.)
- **Named `MISMATCH WATCH` briefing section is gated** on precision@10 ≥ 0.7 AND operator judges ≥5 of top-10 flags genuinely useful. Trace-level `mismatch_hint` until then. (Opus final §2.7; GPT final §2.11.)
- **Twice-weekly cadence, same Obsidian template, `cycle_kind` column separating Mon synthesis from Fri delta.** Resolves the only remaining S3 cadence disagreement on the data plane. (Opus final §2.5 and §4 bullet 8; GPT final §2.12 and §4.)
- **Hybrid retrieval (BM25 + pgvector + RRF) is decided by Gate A.5**, not by argument. Binary outcome, pre-committed on both sides. (Opus final §2.6 and §4 bullet 9; GPT final §2.9 + residual §1.)
- **Cold-start week-1 discipline**: week 1 is "done" only when seed corpus + cold-start briefing + operator labeling on ≥20 items all exist, not when ingestion adapters are online. (Opus final §3.2 Gate A and §4 bullet 12; GPT final Phase 0 Gate A.)
- **Obsidian-first feedback capture** via inline `<!-- radar-feedback: -->` blocks, nightly `radar fb sync` cron, plus `radar.feedback.record()` MCP tool. No separate UI. (Opus final §2.8; GPT final §2.14.)
- **8 MCP tools in v1**: `topic.briefing`, `topic.inbox`, `topic.delta`, `topic.contrarian_view`, `artifact.trace`, `search`, `health`, `feedback.record`. (Opus final §2.5; GPT final §2.13.)
- **8-week solo build, 3 named gates + Gate A.5**, cost envelope $6–$25/week LLM at observed volumes. (Opus final §3.2; GPT final Phase 1 gates.)
- **"Ship narrow or stop" is a hard discipline.** If the build does not materially change the operator's Mon/Fri workflow in the live phase, abandon — do not widen. (Opus final §5.3 and R5; GPT final §4 bullet 24 + recommendation 3.)

## 3. Key Disagreements & Adjudication

| # | Topic | Opus stance | GPT stance | Synthesizer verdict | Hinge / experiment |
|---|-------|-------------|------------|---------------------|--------------------|
| D1 | Friday briefing **semantics** (carryover re-inclusion) | Full-structured over a 4-day window; high-signal carryovers included, tagged as carryover | Delta-only by default; carryovers admitted only when materially re-framed | **Split — settled by in-build A/B**. Both R3s converged on `cycle_kind` column + shared template; the semantic question is explicitly scheduled as a 4-week Variant A vs Variant B experiment starting week 7 | Track per-briefing open rate × items-clicked-through × explicit `useful` count; keep the winning variant |
| D2 | Feedback-capture success metric | R2: ≥40% of items in last 3 briefings have non-empty feedback block | Absolute quotas: ≥8 labeled items/cycle AND ≥3 corrective labels/2 weeks | **GPT-leaning** — Opus self-critiqued the 40% as ungrounded in R2 §6, then explicitly adopted GPT's absolute-quota metric in R3 Concession #4. Finals on both sides record the quota version | Gate C measurement at week 5; if observed rate is ≥20% items/cycle without prompting, tighten the quota; if <8 labeled/cycle, redesign the capture mechanism |
| D3 | Mismatch detector as a **named briefing section** before precision gate | R1 proposed a named "headline/method mismatches this cycle" section from week 3 with the precision check only at week 6 | Store `mismatch_hint` trace-level only until promotion gate clears (precision@10 ≥ 0.7 + operator utility bar) | **GPT-leaning** — Opus R2 Concession #1 explicitly adopts GPT's gating argument, citing Pattern B (authoritative nonsense) — a named section firing noisily for 5 weeks would damage trust in *all* briefing sections. Both finals record the gated-promotion version | Eval set built at Gate B; evaluation at week 6; named section ships week 7 only if precision@10 ≥ 0.7 AND operator judges ≥5 of top-10 genuinely useful |
| D4 | Hybrid retrieval as **week-1 blocking** | R2 argued hybrid must be live end-of-week-1: recall-first promise is structurally unhonorable without semantic retrieval for cross-phrased cases like GEPA | Hybrid is in v1 but should NOT block week 1: Gate A is about giving the operator something concrete to react to, not about infra breadth | **GPT-leaning on sequencing; Opus-leaning on substance.** Collapsed into Gate A.5 at week 2: hybrid gets installed day 1 but is evaluated against Gate A's seed labels, with a binary in-or-out decision. Opus R3 Concession #1 is explicit. Both finals record Gate A.5 | Three-way lex/sem/hybrid eval at end of week 2; pass conditions: hybrid recall@20 ≥ lex-only + 10pp OR recovers ≥2 cross-phrased cases lex-only misses |
| D5 | Primary entity: paper vs. idea | S1A paper-centric; S1B §1 conceded GPT's idea-centric framing is stronger | S1A idea-centric from the start ("motion of ideas") | **GPT-leaning on framing; Opus-leaning on v1 scope**. Both finals agree the *long-term* unit is the idea (B-compatible schema reserved), but the *v1* authoritative unit is the topic + artifact. B-dependence is explicitly forbidden by the "no artifact needs an idea-candidate assignment" invariant | v1 measures whether operator-authored idea candidates accumulate usefully over 6 months; if ≥15 candidates with ≥5 artifacts each emerge, v1.5 entity-resolution experiments are justified |

### D1 — Justification

The operator's Q-M3 answer ("周一早上，周五早上") is symmetric in phrasing, which Opus reads as "equal-weight reading sessions" and GPT reads as "two reading moments with potentially different information needs." Neither side can falsify the other from the operator's one-sentence answer alone; both positions survive under the shared `cycle_kind` + same-template resolution, so the disagreement is genuinely a 50/50 empirical question that belongs in a launch experiment rather than a pre-commit. Opus final §5.1 explicitly rates his own confidence at 55/45 *toward* GPT's delta-only position, which makes this the least-adjudicated of the five disagreements.

### D2 — Justification

Opus R2 §6 explicitly self-critiqued the 40% target as an un-grounded guess — he noted he had no empirical basis for that rate of solo-operator feedback in practice. GPT's absolute quotas are better calibrated to a single-person labeling bandwidth (percentages scale sensitively with briefing item count). Opus R3 Concession #4 adopts GPT's version unambiguously. This is a clean win for GPT's framing; the in-build measurement at Gate C will calibrate the actual number upward or redesign the mechanism if the quota can't be hit.

### D3 — Justification

Opus R2 §1 explicitly steelmans GPT's gating argument: his own R1 had proposed a named mismatch section shipping from week 3 with only a week-6 precision eval to validate it, which meant weeks 1–5 would have carried a named (trust-bearing) feature whose quality was effectively unvalidated — a Galactica-shaped failure in miniature. GPT is correct that named surfaces are trust surfaces — the cost of a noisy feature firing for 5 weeks exceeds the cost of shipping it trace-only until it earns promotion. Pattern B (authoritative nonsense, synthesis §6) maps directly onto this failure mode.

### D4 — Justification

Opus R3 §1 explicitly concedes that his R2 argument was directionally right but scope-confused: the two core substantive claims (hybrid retrieval is production-ready in 2026; the recall-first promise is structurally unhonorable without semantic retrieval) both survived, but neither forces the infrastructure into week 1 as a *blocking* deliverable. The Gate A.5 framing is GPT's position (prove-before-promoting) with a concrete metric and pre-committed response. Opus's substantive claim (GEPA pain is structurally a cross-phrasing recall failure) survives as the motivation for making the gate exist; GPT's sequencing claim (don't couple infra readiness to product-feedback readiness) is what shapes where the gate lands. The merged outcome is better than either pure position.

### D5 — Justification

This disagreement was substantively resolved during Stage 1 itself (Opus S1B §1 explicitly credited GPT's idea-centric framing as stronger than his paper-centric starting point) and then relitigated at the Stage 2 direction level, where the moderator's choice (A-primary on B-compatible schema) captured both sides: v1 organizes around topics + artifacts as authoritative units, with idea-candidate reserved structures preserved for v1.5 promotion. GPT's R2 invariant — phrased as the rule that no artifact must depend on an idea-candidate assignment to reach the briefing, the inbox, or MCP search — is the hard rule that keeps B-compatibility from silently becoming B-dependence. Both finals record this as binding.

## 4. Independent Insights Worth Carrying Forward

### 4.1 From Opus only

- **Cold-start week-1 deliverable protocol.** (Opus S3R2 §2.5 → Opus final §3.2 Gate A.) Day 1–2 backfill → Day 2–3 seed centroid from ≤5 operator-supplied canonical papers per topic → Day 3 cold-start briefing (intentionally wrong, its job is to surface items for labeling) → Day 4–5 live ingestion begins → Day 7 first live briefing. Without this protocol, weeks 2–4 produce a ranker with no evaluation signal. GPT adopted this as their R2 Concession #1.
- **Ranking algorithm spec with explicit 4-signal transparent formula.** (Opus S3R2 §2.3 → Opus final §2.4.) `rank = w1·lex_score + w2·sem_score + w3·recency_score + w4·centroid_shift + bias_terms` with defaults `w = (0.30, 0.30, 0.20, 0.20)` per-topic tunable; `half_life_topic` default 21 days; `topic_centroid` is EMA over curated seeds + operator-marked-useful in last 30 days, recomputed weekly; explicit decision to **never** train weights from click data (filter-bubble mitigation, synthesis Pattern F). This converts "rank transparently" from a promise into a schema + code decision.
- **Cost envelope math for inbox scale.** (Opus S3R2 §2.5 → Opus final §2.2.) ~250–300 artifacts/day pre-triage × 7 = 1,700–2,100/week after topic-keyword pre-filter (not 3,000–5,000). Triage at cheap tier ≈ $2.8/week; second-pass at Haiku ≈ $2.3/week; Sonnet briefing ≈ $1/week. Total ≈ $6/week, room to grow to $25/week before cost-optimization kicks in.
- **GEPA-shaped eval-set harvest protocol** that doesn't depend on the operator remembering 10–20 cases. (Opus S3R2 §2.9 → Opus final §3.2 Gate B.) Step 1: Haiku generates ~30 candidate mismatches from the backfill. Step 2: operator labels genuine/not/borderline + volunteers own cases. Step 3: decision point at week 3 — if genuine_count ≥ 10, feature lives; otherwise push to v1.5. Closes the "what if the operator can't supply 10 examples?" failure mode.

### 4.2 From GPT only

- **Gate A/B/C as moderator-readable launch gates.** (GPT S3R2 §2.1 → GPT final Phase 1.) Binary pass/fail deliverables that make "is this build on track?" a readable-from-outside question rather than requiring the moderator to parse week-by-week narrative. Opus R3 §2 adopted this and extended it with Gate A.5.
- **"Triage + memory + audit substrate, NOT an AI that issues verdicts."** (GPT S2R1 §1 → GPT final §2.1.) Opus S3R1 Concession #1 explicitly adopts this reframe, which stepped the whole product back from "auditable verdicts" (retains system-issues-verdicts ambition) to "framings + advisory hints + mismatch flags," with the human producing verdicts *using* those artifacts.
- **"Preference prison" as the sharp framing of filter-bubble risk.** (GPT S1A Part B → synthesis §2.) Opus S1B §1 credited this label as sharper than his own taste-atrophy framing; it survived into synthesis Pattern F and drove the "never train ranker weights from click data" decision in v1.
- **Semantic Scholar Research Feeds as ready-made prior art.** (GPT S1B §2 → synthesis §7.) This catch collapsed any "AI-personalized daily paper feed" direction into "what does OUR version do that Research Feeds doesn't?", which is what forced the Stage 2 novelty claim to anchor on lab-project-awareness + idea-migration rather than personalization per se.
- **Negative-control discipline on the eval set.** (GPT S3R2 §2.3 → Opus R3 Concession #3.) The Gate-B eval set must include ≥5 "flashy headline, method-aligned" controls, not just ≥10 genuine + ≥10 not-genuine. Otherwise the detector can look good by only learning to flag anything that sounds ambitious.
- **`radar.topic.delta(topic, since_cycle?)` as a general MCP primitive** (GPT S3R1 §2.5 → Opus R2 Concession #3.) Cleanly generalizes Opus's `what_am_i_missing` special-case into a broader "what changed on topic T since cycle C: new artifacts, re-framings, promotions/demotions" tool that becomes the MCP-native equivalent of the Friday briefing experience.

## 5. Proposed Architecture (Consensus Version)

### Stack (pinned major versions)

- **Runtime**: Python 3.12, `uv` for env + deps.
- **Storage**: PostgreSQL 16, with `pg_trgm` + full-text search + JSONB + `pgvector` extension (installed day 1, used by ranker only if Gate A.5 passes). Single primary; nightly backup to local disk + weekly encrypted offsite snapshot. **No separate vector DB, no web app, no workflow orchestrator.**
- **ORM**: SQLAlchemy 2.x + Alembic for migrations.
- **Embeddings**: local BGE-M3 on operator's 24 GB 4090 (~1.5 GB VRAM), batched; embeddings cached per `artifact_version`, never recomputed.
- **LLM routing** (v0 defaults, not pre-decided — 3-day PoC resolves):
  - Triage pass (every artifact): Claude Haiku 4.5 — extracts `claim_span`, `method_span`, `novelty_hint`, `mismatch_hint`. Budget: ≤2k input + ≤400 output per artifact.
  - Second pass (top-N per topic per cycle): Haiku 4.5 with richer framing schema + evidence_span extraction. Budget: ≤8k input + ≤800 output.
  - Briefing synthesis: Claude Sonnet 4.6, one pass per topic per cycle. Budget: ≤10k input + ≤2k output.
  - **No Opus in v1** (cost discipline per project CLAUDE.md "Prohibited" rules).
  - GLM-4.6 / MiniMax-M2 held as cost-optimization fallback if observed Haiku weekly run-rate exceeds ~$20/week.
- **Scheduler**: plain `cron` + `systemd timers`. No Airflow/Prefect.
- **Ingestion HTTP**: `httpx`; `trafilatura` for blog HTML extraction; `urllib.robotparser` for strict robots.txt compliance; per-host 1 req / 5 s cap; RSS/Atom fallback where offered.
- **MCP server**: Python MCP SDK, stdio transport (started by Claude Code).
- **Output sink**: Obsidian vault at `~/obsidian-vault/research-radar/YYYY/MM/YYYY-MM-DD-<topic>.md` (file-per-cycle canonical) + `<topic>.md` living-page convenience view regenerated each cycle.
- **Tests**: `pytest` against real Postgres in Docker (per project CLAUDE.md — no mocked DB on critical path).
- **Lint/format**: `ruff`.
- **Observability**: structured JSONL logs; per-artifact cost telemetry rows; `radar.health()` MCP tool as live status surface (fails loudly when a source goes down — Pattern C upstream-infra-risk mitigation).

### Key modules

1. **Ingestion layer** — arxiv, OpenAlex, Semantic Scholar lookup, OpenReview, GitHub trending (ML), operator-whitelisted public blog list. X adapter interface + schema fields exist; no client implemented in v1.
2. **Normalization + ledger store** — 12 canonical tables (Opus final §2.3 / GPT final §2.7): `artifact`, `artifact_version`, `topic`, `topic_artifact_link`, `framing`, `evidence_span`, `rank_signals`, `briefing_cycle` (with `cycle_kind ∈ {synthesis, delta}`), `briefing_item`, `feedback`, `idea_candidate` (reserved, operator-authored only in v1), `idea_candidate_member` (operator-confirmed only).
3. **Triage + ranking layer** — every artifact scored (recall-first, none dropped). Transparent 4-signal weighted rank (see §4.1 Opus-only). Per-artifact `mismatch_hint` populated from week 3.
4. **Briefing compiler** — Mon synthesis + Fri delta, same Obsidian template, `cycle_kind` separating semantics. Per-topic ≤15 items per briefing; sections: `NEW & MOVING`, `CARRYOVER (materially reframed)`, `POSSIBLY OVERHYPED`, `POSSIBLY UNDERRATED`, `MISMATCH WATCH` (gated — empty before Gate-C-adjacent promotion).
5. **MCP server (8 tools)** — `topic.briefing`, `topic.inbox`, `topic.delta`, `topic.contrarian_view`, `artifact.trace`, `search`, `health`, `feedback.record`.
6. **Feedback sync daemon** — nightly `radar fb sync` cron scans Obsidian vault for edited `<!-- radar-feedback: -->` blocks, writes `feedback` rows, archives the comment.

### Critical cross-cutting concerns

- **Append-only discipline.** No updates-in-place on `artifact`, `artifact_version`, `framing`, `evidence_span`, `topic_artifact_link` state transitions, or `briefing_item`. Every regeneration creates new rows; `superseded_by` FK points to the current row. Reproducibility is a database property, not a test-suite concern.
- **Recall-first contract.** Briefing ≤15 items × 2/week = ~30 items read; inbox is ~1,700–2,100 items/week, queryable via MCP, never scanned linearly. The contract is explicit: "briefing = what you read; inbox = what the system promises it saw."
- **B-compatibility without B-dependence.** Hard invariant: no artifact may require an `idea_candidate` assignment to appear in briefing, inbox, or MCP search. `idea_candidate` rows are operator-authored only in v1 — no LLM auto-clustering.
- **Filter-bubble mitigation.** Ranker weights are never trained from click data in v1. Explicit serendipity valve: `radar.topic.contrarian_view` tool runs a contrarian reranker; briefing includes `POSSIBLY OVERHYPED` and `POSSIBLY UNDERRATED` sections.
- **Upstream-infra-risk mitigation (Pattern C).** Multi-source ingestion from day 1; `radar.health()` fails loudly on source outages so the operator notices *before* the briefing silently shrinks.
- **Cost discipline.** Per-artifact cost telemetry from Gate A. $20/week run-rate on Haiku triggers automatic cost-audit and GLM/MiniMax-tier switch eval.
- **Named surfaces are trust surfaces.** Mismatch detection is trace-level until it clears precision@10 ≥ 0.7 on a ≥10 genuine + ≥10 not-genuine + ≥5 flashy-method-aligned-controls labeled set (Pattern B mitigation).

## 6. MVP Scope

### 6.1 Phase 0 — Proof of concept (3 days)

**Goal**: prove the triage + framing loop is cost-viable and quality-viable on one topic before committing to the 8-week plan.

- **Day 1**: ingest 90-day backfill for `agentic-RL` (1 topic) from arxiv + OpenAlex. Stand up minimal `artifact` + `framing` tables. Run Haiku triage + framing on ~500 artifacts.
- **Day 2**: hand-grade a 30-paper sample for claim-span accuracy, method-span accuracy, mismatch-hint precision. Measure cost per framing.
- **Day 3**: commit model-tier decision in writing (Haiku default, or cost-escalate to Sonnet-small, or downshift to GLM/MiniMax).

**Acceptance bar**: claim + method spans correct on ≥80% of sample; cost ≤ $0.01 per framed artifact; mismatch-hint precision ≥ 0.5 (noisy but directionally useful).

**If fails**: stop and re-estimate before committing to the 8-week plan. Better to discover at day 3 than at week 4.

### 6.2 Phase 1 — v0.1 shippable (8 weeks from PoC completion)

Four binary gates. Each is moderator-readable.

**Gate A · end of week 1** — 8 seed topics loaded; 90-day topic-scoped backfill completed; all 12 canonical tables live; first cold-start briefing generated from backfill (intentionally wrong); operator labels ≥20 seed items in Obsidian or via MCP; `radar.artifact.trace(...)` works on every seed-briefing item; `ranker_version = "v0.1-coldstart"` committed on every `briefing_item` row; cost telemetry surfaces tokens + dollars.

**Gate A.5 · end of week 2** — three-way retrieval eval (lex-only / sem-only / hybrid) run against week-1 seed labels + ≥5 operator-confirmed cross-phrased queries. Decision committed in writing: hybrid is `blocking-v1` or `deferred-v1.5`. Week-2 cost audit triggers GLM/MiniMax switch eval if Haiku run-rate exceeds $20/week.

**Gate B · end of week 3** — second-pass framing pipeline (Haiku 4.5) live; `mismatch_hint` populated on every framing; GEPA-shaped eval set complete (≥10 genuine + ≥10 not-genuine + ≥5 flashy-method-aligned controls); first ranker comparison run on labeled seed set. Mismatch stays trace-level.

**Gate C · end of week 5** — Mon synthesis + Fri delta cadence live across all 8 topics; feedback loop proving the ranker can be steered (≥8 labeled items/cycle AND ≥3 corrective labels per 2 weeks); briefing useful enough that operator still opens it.

**Week 6** — MCP server + 8 tools; `contrarian_view` implementation; mismatch precision@10 eval on the Gate-B labeled set. Promotion decision for the named `MISMATCH WATCH` section.

**Week 7** — If promotion passed: ship the named section. Topic lifecycle MCP commands. X adapter stub + schema fields. Begin the 4-week A/B experiment on Friday delta-eligibility (carryovers vs. delta-only).

**Week 8** — Hardening. Backup/restore drill. Rate-limit edge cases. Cost audit. Operator runbook committed. `ranker_version` audit log shipped.

### 6.3 Phase 2 — v1.0 durable internal tool (weeks 9–24)

"v1.0" here = commercial-grade *as an internal tool*, not SaaS. Synthesis §8 framing: personal-tool-with-publishable-internals.

Priorities in order (each one is gated on Phase-1 having shipped the preceding capability):

1. **Hybrid retrieval calibration** (if Gate A.5 passed) — re-eval at weeks 10 and 14 as more labeled cross-phrased queries accumulate. Expected outcome: 3–5 percentage points additional recall@20 as the centroid stabilizes.
2. **Friday delta-eligibility decision** — the 4-week A/B from week 7 completes; commit to one variant (full over 4-day window with tagged carryovers, or delta-only). Variant wins if combined `open_rate × useful_count` exceeds the other by ≥15%.
3. **Mismatch section maturation** (if promoted at Gate C-adjacent) — expand eval set to 50+ labeled cases; tune detector on real-world performance. Retire the named section if precision@10 drops below 0.6 for 3 consecutive weeks.
4. **Operator-authored idea-candidate surfacing** (cautious v1.5 entry) — once ~15–30 candidates accumulate, show *suggested* memberships in `radar.trace` but require operator confirmation. No auto-population. This is the first hint of Direction-B feature life.
5. **X adapter v1** — implement actual client behind feature flag; operator defines ≤50 accounts-to-watch; X posts become a new artifact type subject to all the same framing/ranking. Gated on operator writing a `config/x-accounts.toml` and confirming API pricing is acceptable (xpoz/Apify/scrapfly tier per Stage-2 search).
6. **Second-researcher access** (if operator extends) — read-only MCP surface with per-user feedback namespacing. Only expose `topic.briefing`, `topic.inbox`, `artifact.trace`, `search` — feedback-write and topic-create remain operator-only.
7. **Cost & ops hardening** — API key rotation via vault; alerting on `radar.health()` regressions; cost dashboard (Grafana against Postgres cost-telemetry rows).

**Explicitly out of scope even at month 6**: no web UI; no auto-clustering of idea candidates; no cross-lab sharing; no fine-tuned local models; no paywalled content; no chief-of-staff auto-decision surfaces.

## 7. Risk Register

| ID | Risk | Likelihood | Impact | Mitigation | Owner |
|----|------|------------|--------|------------|-------|
| R1 | **Pattern A — useful-but-niche plateau**: operator opens briefings for 2–3 weeks, then quietly stops. Ten-year failure mode for this entire tool category | High | High | Pre-commit week-6 behavioral test (≥8 of 12 briefings opened + ≥2 named catches); pre-commit abandon conditions now; `radar.topic.contrarian_view` as pull-surface value when briefing fades | Operator (behavioral); architect (instrumentation at Gate C) |
| R2 | **Duplication risk** — v1 turns out to replicate 80% of Semantic Scholar Research Feeds + Zotero + papersgpt-for-zotero at 5% of the build cost. Both finals flag this explicitly (Opus final §5.3) | Medium | High | Write down the concrete gap list *before* build starts — what does v1 do that Research Feeds + Zotero can't? If no concrete list: park the build for 4–6 weeks, use existing stack first | Operator (gap list); architect (baseline comparison at Gate C) |
| R3 | **GEPA eval set fails to reach ≥10 genuine cases by week 3** — operator can't supply enough historical incidents; Haiku-generated candidates are too noisy | Medium | Medium | Phase-0 day-2 hand-grade calibrates mismatch-hint precision; Opus-only harvest protocol (3-step: synthetic + operator-labeled) reduces dependency on operator memory; if still <10 genuine at week 3, feature pushes to v1.5 cleanly (schema stays populated) | Architect (harvest protocol); operator (week 2–3 labeling block) |
| R4 | **Feedback-loop starvation** — operator provides <8 labels/cycle, ranker-tuning starves, filter stays at hand-tuned weights indefinitely | Medium | Medium | Gate C measures the real rate; redesign to weekly 3-prompt questionnaire if mechanism fails; `radar.feedback.record()` MCP path is the low-friction alternative | Architect (Gate C measurement); operator (tolerance for weekly quota) |
| R5 | **Hybrid retrieval statistical power at Gate A.5** — seed corpus may not have enough cross-phrased queries for a clean in/out decision at week 2. Opus R3 §5 flagged this | Medium | Low | Re-run Gate A.5 at week 4 with accumulated operator feedback before declaring hybrid dead; default-safe fallback is lex+centroid+recency — gate failure is not v1 failure | Architect |
| R6 | **24 GB 4090 VRAM contention** — 4090 may be allocated to other lab workloads; batched BGE-M3 embedding job competes for ~2 hours of VRAM, slipping Gate A by 3–5 days | Medium | Medium | **Pre-condition**: operator writes one-sentence availability window on day 1 of build. Fallback: CPU embedding (slower) or smaller embedder | Operator (availability declaration); architect (fallback paths) |
| R7 | **Pattern C — upstream infrastructure disappears** (Microsoft Academic 2021 precedent): arxiv/OpenAlex/Semantic Scholar/OpenReview API deprecation or pricing shift | Low | High | Multi-source ingestion from day 1; `radar.health()` fails loudly on source outage; per-source adapter interface permits replacement without re-plumbing | Architect |
| R8 | **Blog compliance rat-hole** — each whitelisted blog has its own robots.txt posture; at least one will challenge our crawling stance | Medium | Low | Strict robots.txt via `urllib.robotparser`; conservative User-Agent; per-host 1 req / 5 s cap; RSS/Atom fallback where offered; operator whitelist is narrow (~15 sources) | Architect |
| R9 | **Triage-tier hallucination** — GLM/MiniMax or even Haiku hallucinates claim/method spans on 2k-token abstracts. Pattern B applies — false mismatch flags undermine briefing trust | Medium | Medium | Phase-0 day-2 sample-grade (30 papers, acceptance ≥80% span accuracy) catches this before 8-week plan commits; in-flight escalation path documented (switch triage to richer model, cost +~$20/week) | Architect (day-2 grading) |
| R10 | **Preference prison (Pattern F)** — personalization narrows curiosity instead of expanding it | Medium | Medium | Ranker weights never trained from click data in v1; `POSSIBLY OVERHYPED` + `POSSIBLY UNDERRATED` briefing sections are *always* populated; `radar.topic.contrarian_view` tool available; operator-configured "stretch topics" permitted in topic lifecycle | Architect |

## 8. Explicit Non-Goals (what we are NOT building)

- No web UI, no dashboard, no separate frontend. Obsidian + Claude Code are the entire surface.
- No autonomous novelty scoring as a primary ranking signal. Novelty-hint is advisory, labeled as such.
- No automated cross-artifact entity resolution. `idea_candidate` rows are operator-authored only in v1.
- No live X ingestion. Schema + adapter stub only.
- No paywalled content ingestion (IEEE, ACM, bioRxiv-with-login, journal portals). Operator explicit exclusion.
- No fine-tuned local models. Inference only against pre-trained ones.
- No personalization from click/dwell data. Filter-bubble mitigation is binding.
- No "chief of staff" auto-decision-making surfaces. The system is a triage + memory + audit substrate, not a judgment engine.
- No lab-memory-as-new-hire-onboarding surfaces. Year-3 aspiration; not priced or scoped.
- No SaaS framing, no multi-lab support, no commercial distribution. Personal-tool-with-publishable-internals.
- No separate vector database, no workflow orchestrator, no queueing platform. Single Postgres + cron + systemd.
- No real-time anything. Daily ingestion + twice-weekly briefing cycle is the latency target.

## 9. Actionable Next Steps

Each with a concrete verb + file path or command.

- [ ] Human: confirm the three moderator checkpoint questions above (seed-topic stability, GEPA labeling commitment, week-6 behavioral-success sentence). Write answers to `discussion/002/002-moderator-notes.md` as a new appended section.
- [ ] Human: supply ≤5 canonical seed arxiv IDs per topic — append to `discussion/002/002-moderator-notes.md` under a "Q-M6: seed papers per topic" heading. Format: `{topic_slug}: [arxiv_id_1, arxiv_id_2, ...]`.
- [ ] Human: write a one-sentence 4090 availability window for ingestion jobs — append to the same moderator-notes file as "Q-M7: 4090 availability".
- [ ] Operator: pre-commit abandon conditions in writing — append to `discussion/002/002-moderator-notes.md` under "Abandon Conditions". Proposed default: (a) Gate A slips >1 week, (b) Gate C feedback rate <8 labels/cycle across 3 cycles, (c) week-6 behavioral test missed.
- [ ] Synthesizer/operator: run `mkdir -p specs/002-research-radar/` to create the spec directory.
- [ ] Run `/spec-from-conclusion 002` against `conc/002-Opus47Max-GPT54xHigh-byOpus47Max-260423.md` to generate `specs/002-research-radar/spec.md`.
- [ ] Spec-writer: encode Gates A / A.5 / B / C as binary acceptance criteria in `specs/002-research-radar/spec.md`. Do not let Stage-3 decisions become a vague implementation wishlist (GPT final recommendation 2).
- [ ] Spec-writer: encode the trust non-negotiables as spec invariants (no novelty score as primary rank key; no live X dependency; no named `MISMATCH WATCH` section before it earns one; no artifact requires idea-candidate assignment; ranker weights never trained from click data). Write them into a `specs/002-research-radar/invariants.md` file that the task-decomposer must not violate.
- [ ] Spec-writer: encode the 3-day PoC (Phase 0) as its own milestone with a written stop-condition. Output file: `specs/002-research-radar/phase-0-poc.md`.
- [ ] Task-decomposer: produce `specs/002-research-radar/tasks/T001.md` through `specs/002-research-radar/tasks/T0NN.md` mapped to the week-by-week build sequence (Opus final §3.2 + GPT final Phase 1).
- [ ] Architect: schedule a 30-minute external human engineering review of the spec before any build worktree is created. The architectural risk (R2 duplication risk vs existing commodity stack) is the kind of thing that benefits from a second human. Target reviewer: someone who has deployed an internal research-tools system before; Linear/Slack/email whichever channel the operator prefers.
- [ ] Architect: on day 1 of build, confirm Postgres 16 + pgvector extension + BGE-M3 weights are available on the target Linux box — add a pre-flight check script to `projects/002-research-radar/scripts/preflight.sh`.
- [ ] Architect: set up a `projects/002-research-radar/cost-telemetry.md` running log from Phase-0 day 1; every LLM call's token count + dollar cost gets logged. Review at Gate A.5 cost audit.

## 10. Meta — synthesis honesty notes

- **Standardized vocabulary**: both debaters used "briefing" interchangeably with "digest" in earlier rounds; I standardized on "briefing" throughout, consistent with both finals. Both used "triage" sometimes for "first-pass LLM extraction" and sometimes for "broader ingestion-time filtering"; I standardized on "triage pass" for the LLM extraction step specifically. "Framing" is load-bearing — it is the primary product object per both finals, explicitly opposed to "score" or "verdict."
- **Close-call disagreements**: **D1 (Friday semantics)** is genuinely 55/45 toward GPT by Opus's own admission (Opus final §5.1); I recorded it as Split-settled-by-A/B rather than adjudicating. **D4 (hybrid week-1 blocking)** was a clean win for GPT on sequencing but Opus's substantive claim (GEPA pain is structurally a cross-phrasing recall failure) was load-bearing and I credited it as the motivation for Gate A.5's existence. **D5 (paper vs idea)** was substantively conceded back in Stage 1 and I could have omitted it as a "disagreement" — but the v1 scope question (is the primary authoritative unit really the topic, or is it already the idea?) was still live enough in Stage 3 to warrant listing.
- **Concerns I could not fully resolve**: GPT S3R2 §5 self-critique flagged that "a low absolute quota is easier for the operator, but it may also starve the ranker of enough corrective signal to improve quickly." Opus R3 §5 flagged a mirroring concern. This is a real tension: the feedback metric was adjudicated GPT-leaning in D2, but the failure mode both sides anticipate (starved ranker → hand-tuned weights indefinitely) has no pre-committed fix. Gate C measurement will surface the actual rate, but the redesign path (weekly 3-prompt questionnaire?) is not specified.
- **Honest residual risk that architecture cannot defuse**: the R2 duplication risk in §7 — "v1 replicates 80% of Research Feeds + Zotero + papersgpt at 5% of the build cost." Both finals flag this; both admit it is not reducible architecturally; both delegate the mitigation to the operator's pre-build gap-list exercise. The synthesizer's honest view: this is the single biggest reason the moderator checkpoint question #3 (week-6 behavioral-success sentence) matters more than any engineering gate.
- **Where the debate under-weighted something**: neither round of Stage 3 re-verified the 24 GB 4090 VRAM budget assumption against realistic concurrent-lab-workload scenarios. I surfaced this as R6 and as a Phase-0 prerequisite, but the debate treated it as a proposal given, not a risk to measure. If the 4090 is actually saturated by other lab jobs, ingestion falls over silently at week 1.
- **Disagreement D1 is the most consequential unresolved item.** Not because it's large — it's 55/45 — but because it maps onto the one product-level choice that can't be pre-committed from one operator sentence and that directly affects how week-7 engineering time gets spent. Flagged for the moderator's attention before spec-writing.
