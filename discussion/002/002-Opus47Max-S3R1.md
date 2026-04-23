# Idea 002 · S3R1 · Opus 4.7 Max · Converge (engineering)

**Timestamp**: 2026-04-22
**Stage**: 3 (Converge). Mode: engineering. Moderator chose **ADVANCE** with
**Direction A-primary (topic-ledger-briefing)** on a **B-compatible schema**,
with **D (MCP surface) exposed alongside from v1**.
**Reads**: `002-stage2-checkpoint.md` (direction + §6 honesty flags),
`002-moderator-notes.md` (Q-M1..Q-M5 answers), both S2R1s. No prior S3 round
exists (R1).

---

## 0. Context carried into Stage 3

Moderator's concrete answers to Q-M1..Q-M5 change the engineering plan
materially:

- **Q-M1 (topic list)** — 8 topics supplied: `agentic-RL`, `agent
  self-evolution`, `diffusion-LLMs`, `compressing-LLM-reasoning`,
  `novel-LLM-architectures` (looped transformers as seed), `on-policy-
  distillation`, `LLM-explainability`, `LLM-adapters`. Day-1 import task
  exists — we don't need topic-nucleation tooling in v1.
- **Q-M2 (project state)** — none. Direction C collapses as I predicted;
  the Stage 3 checkpoint's "flip to C" branch is closed. Good — it
  confirms A-primary.
- **Q-M3 (reading workflow)** — Mon AM + Fri AM, sources are X pushes +
  arxiv pushes + conf lists + blogs + GitHub. This is the exact shape of
  behavior that Direction A's weekly briefing can *absorb* (briefing + inbox
  replaces arxiv/conf manual scans) while D (MCP) becomes the in-flow query
  surface for the in-Claude-Code ad-hoc checks he'd otherwise do with X.
  Biweekly cadence (Mon + Fri) ≠ weekly. **The briefing cadence must be
  twice-weekly, not weekly** — this is a small but real delta from S2.
- **Q-M4 (pain case)** — GEPA (claimed agent self-evolution, actually prompt
  optimization) is a gift. This is the exact failure mode the auditable-
  verdict layer must defuse: an LLM summary that *parrots the authors'
  framing* ("self-evolving agent") without cross-checking method against
  claim. GEPA belongs in the v1 test set as gold-label "noisy-positive —
  flag the claim/method mismatch."
- **Q-M5 (schema)** — keep idea-entity-capable schema from day 1. Direction
  B upgrade path preserved.

Checkpoint §6 honesty flags (7 of them) — I'll address the 4 that bite
engineering: #2 inbox-size at scale, #3 lab-project-aware w/o evidence, #6
LLM cost at volume, #7 X-adapter-scope-creep. Flags #1, #4, #5 are
moderator-level decisions already made (operator picked A, didn't choose
"use Research Feeds for 4 weeks first").

---

## 1. Steelman of opponent's strongest point (prior S3)

No prior S3 round exists. Instead, I'll steelman GPT's **strongest S2R1
point** that I disagreed with or underweighted: **"the system should be
framed less as *a model that judges the frontier for me* and more as *a
research memory and triage system that makes judgment cheaper, more
traceable, and less lossy*"** (GPT S2R1 §1 final paragraph).

Why this is stronger than my framing: my S2R1 kept phrasing the output as
"auditable verdicts" — which retains the ambition of *the system issuing
verdicts at all*. GPT's framing steps back and says the system's core job
is **triage + memory + audit trail**, and the human produces the verdicts
*using* those artifacts. This is a weaker claim for the system and a
stronger product position. Stage 3 should adopt GPT's framing as the
operating definition: we build a **triage-and-memory substrate with
opinionated-but-auditable briefings**, not "an AI that judges papers."

This changes one concrete engineering choice: the briefing layer should
surface LLM-generated *framings* (what the paper claims, what method it
uses, what adjacent work exists, where it might mislead) rather than
LLM-generated *scores* (novelty: H, impact: M). Framings are auditable per
sentence (each sentence carries a span-level citation). Scores are
adversarially fragile (synthesis §Pattern E, validated by 4 benchmarks).

This adoption is concession #1 in §5.

---

## 2. New ground — architecture and MVP

### 2.1 System shape

One logical system, three observable surfaces:

```
┌─────────────────────────────────────────────────────────┐
│                    INGESTION LAYER                      │
│  arxiv · OpenAlex · Semantic Scholar · OpenReview ·     │
│  GitHub trending · curated blogs (with robots.txt)      │
│  [X adapter: schema + stub only, no v1 client]          │
└──────────────────┬──────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────────────┐
│              NORMALIZATION + STORE                      │
│  Artifact store (papers/repos/blogs/posts)              │
│  Topic store (8 seed topics, lifecycle-aware)           │
│  Idea-node schema (reserved, not populated v1)          │
│  Claim-method index (per-paper: claim span + method     │
│  span — GEPA-style mismatch detection)                  │
└──────────────────┬──────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────────────┐
│           TRIAGE + RANKING LAYER                        │
│  Recall-first: every artifact scored, none dropped      │
│  Small-model triage on 4090 (GLM/MiniMax tier)          │
│  Commercial-model second-pass on top-N per topic        │
│  Rankings: topic-relevance, claim-confidence, novelty-  │
│  hint (advisory only, labeled as such)                  │
└──────────────────┬──────────────────────────────────────┘
                   ↓
         ┌─────────┴─────────┬──────────────────┐
         ↓                   ↓                  ↓
  ┌──────────────┐    ┌──────────────┐   ┌──────────────┐
  │ BRIEFING     │    │ INBOX        │   │ MCP SURFACE  │
  │ (Mon/Fri AM) │    │ (read-thru)  │   │ (on-demand)  │
  │ → Obsidian   │    │ per-topic +  │   │ 6 tools; see │
  │   markdown   │    │ global       │   │ §2.3         │
  └──────────────┘    └──────────────┘   └──────────────┘
```

### 2.2 Pinned stack (v1)

- **Runtime**: Python 3.12, `uv` for env.
- **Storage**: PostgreSQL 16 (artifact + topic + claim index + idea-node
  reserved tables; JSONB for flexible per-source metadata). Single primary,
  no replicas; backups to local disk + weekly encrypted snapshot. No vector
  DB in v1 — see §3 disagreement 2.
- **Embeddings + retrieval**: `pgvector` extension on Postgres. BGE-M3 or
  equivalent small embedder running on 4090 (≈1.5GB VRAM); embeddings
  cached per artifact, never recomputed.
- **LLM routing**:
  - *Triage pass* (every artifact): GLM-4.6 or MiniMax-M2 via cheap API.
    Short prompt, extract (claim, method, novelty-hint, mismatch-flag).
    Budget: ≤2000 input tokens + ≤400 output per artifact.
  - *Second pass* (top-N per topic per cycle): Claude Haiku 4.5 or
    equivalent. Structured framing for the briefing. Budget: ≤8000 input
    + ≤800 output per top-N item.
  - *Briefing generation*: Claude Sonnet 4.6, one pass per topic per
    cycle, assembles the top-N framings into the Mon/Fri briefing.
  - No Opus in v1 — cost discipline per CLAUDE.md "Prohibited" rules.
- **Local models on 4090** (24GB VRAM budget):
  - Embedder: BGE-M3 ≈1.5GB
  - PDF parser / figure VLM: InternVL or equivalent 4–8B tier, ~12–16GB
    VRAM
  - Leaves headroom for batched embedding jobs + ad-hoc reranker
- **Ingestion**: `arxiv.py`, `openalex` client, `semanticscholar` client,
  `pyalex` for OpenAlex bulk, `requests` + `trafilatura` for blog HTML
  with `robots.txt` compliance via `urllib.robotparser`, `httpx` with
  rate-limit middleware. Blog list is operator-maintained whitelist, no
  discovery crawling.
- **MCP server**: `mcp` Python SDK, transport = stdio for Claude Code
  integration.
- **Scheduler**: plain `cron` + `systemd timers` on the Linux box (24GB
  4090). No Airflow/Prefect — overkill for single-user.
- **Briefing sink**: writes to `~/obsidian-vault/research-radar/YYYY/MM/
  YYYY-MM-DD-<topic>.md`. Operator already uses Obsidian per the proposal.
- **Tests**: `pytest`, real Postgres in Docker (per CLAUDE.md tool
  preferences — no mocked DB), `ruff` for lint.
- **Observability**: structured logs (JSONL) to disk; per-artifact-cost
  telemetry via Postgres row; a minimal `/stats` MCP tool for the operator
  to read current weekly cost + backlog size.

### 2.3 MCP surface (6 tools, day-1)

Exposed to Claude Code via stdio. The operator asks in-chat; results return
as tool output. Each tool honors recall-first default — no silent drops.

1. `radar.topic.briefing(topic: str, cadence: 'mon'|'fri'='latest')` —
   returns the latest Obsidian briefing body for a named topic.
2. `radar.topic.inbox(topic: str, since: date=last_cycle, limit: int=200)`
   — returns full ranked inbox for a topic since last cycle; no
   filtering beyond rank order.
3. `radar.search(query: str, topic_filter: list[str]=None, since:
   date=-30d, limit=100)` — natural-language query across
   claims + methods + framings. Recall-first: returns ranked, not
   filtered, with confidence column.
4. `radar.artifact.framing(artifact_id: str)` — returns the saved framing
   for a single artifact: claim, method, claim/method-mismatch flag,
   adjacent artifacts, source URL. This is the GEPA-case surface.
5. `radar.topic.what_am_i_missing(topic: str)` — runs the serendipity
   valve on-demand: returns the top-N items the default ranker hid
   or deprioritized, with one-line rationale for why the contrarian
   ranker promoted each. Per checkpoint §3 recommendation #5.
6. `radar.health()` — returns ingest backlog, last-cycle cost, per-source
   status (arxiv up? OpenAlex up? blog N failed ingestion?). Pattern-C
   (upstream infra risk) mitigation: fails loudly when a source is down
   so the operator notices *before* the briefing silently shrinks.

### 2.4 MVP — what ships in v1

IN (v1, 6–8 weeks solo):
- Ingestion from arxiv (daily), OpenAlex (daily), Semantic Scholar
  (paper-lookup only — no graph crawl), OpenReview (when venues open),
  GitHub trending ML (daily), operator whitelist of ~15 blogs (daily).
- Artifact store, topic store, claim-method index, idea-node reserved
  schema.
- Triage pass (all artifacts) + second pass (top-30 per topic per cycle)
  + briefing generation (Mon AM, Fri AM).
- 8 seed topics as pinned configuration (operator's Q-M1 list).
- Briefing output → Obsidian vault markdown.
- Per-topic inbox queryable via MCP.
- 6 MCP tools listed in §2.3.
- Claim/method-mismatch flag on every artifact (GEPA-shaped).
- Serendipity valve: contrarian reranker + `what_am_i_missing` tool.
- Topic lifecycle: `create | active | archived` states; archive preserves
  all associated artifacts and past briefings.
- Cost telemetry: real dollar + token cost per artifact, per topic, per
  week.

OUT (v1, explicit non-goals):
- No web UI. Obsidian + Claude Code is the entire surface.
- No idea-entity-graph population (schema exists, but no cross-artifact
  resolution runs). Deferred to v1.5.
- No X ingestion (adapter stub + schema fields only). Deferred to v2 per
  moderator note 3.
- No paywalled content (IEEE/ACM/bioRxiv-login). Operator note 4.
- No fine-tuned local models — only inference with pre-trained ones.
- No personalization beyond the 8 topics + operator feedback on briefings.
  Filter-bubble literature (Pattern F) cited as reason to defer.
- No autonomous novelty *scoring*. Only novelty *hints*, always labeled
  advisory (§1 concession).
- No lab-memory-as-onboarding surfaces. Year-3 aspiration; not priced here.

### 2.5 Cycle-by-cycle load estimate (addresses checkpoint §6 flag #2 + #6)

This is the "recall-first inbox may be too big to scan" math the checkpoint
said nobody ran. Running it now because it changes the design.

Daily inflow estimates (synthesis §11.6 budget prompt):
- arxiv cs.* ≈ 200/day relevant to operator's 8 topics after keyword pre-
  filter (cs.AI alone is ~60/day, but the 8 topics span cs.LG, cs.CL, cs.AI,
  cs.CV partially — pre-filter by topic keywords, not full arxiv).
- OpenAlex (non-arxiv AI venues) ≈ 30/day.
- GitHub trending ML ≈ 20/day relevant.
- Blogs ≈ 5–10/day across ~15 whitelisted sources.
- **Total: ~250–300 artifacts/day pre-triage, ~1,700–2,100/week.**

This is *not* 3,000–5,000/week (checkpoint §6 flag #2's worst case) because
topic-keyword pre-filter happens at ingestion, before triage. **But it's
still 1,700+ items/week in the inbox.** That's too many to scan even if
ranked.

Design response: the inbox is queryable by MCP/Obsidian, **not read
linearly**. The briefing is the linear surface (≤15 items per briefing, 2
briefings/week = 30 items the operator actually reads). The inbox is the
*recall guarantee* — it exists so the operator can answer "did we cover X?"
in 2 seconds, not so he can scan all 1,700 items. This is a real constraint
and the product framing must be explicit: **briefing = what you read; inbox
= what the system promises it saw.**

Weekly LLM cost (rough, checkpoint §6 flag #6):
- Triage pass: 2,000 artifacts × ~2k input + 400 output tokens each.
  At GLM-4.6 pricing ≈ $0.0003/1k input + $0.0006/1k output (2026
  cheap-API tier), that's ~$0.0014/artifact × 2,000 = **~$2.8/week**.
- Second pass: 30 items/topic × 8 topics = 240 items × ~8k input + 800
  output. At Haiku 4.5 pricing ≈ $0.0008/1k in + $0.004/1k out:
  (0.0064 + 0.0032) × 240 = **~$2.3/week**.
- Briefing generation: 8 topics × 2 briefings/week × ~10k input + 2k out
  on Sonnet 4.6. At $0.003/1k in + $0.015/1k out: (0.030 + 0.030) × 16 =
  **~$1/week**.
- **Total LLM: ~$6/week ≈ $312/year.** Well within any sane budget.
  Flag #6 defused for v1.
- **Caveat**: this assumes GLM-4.6 quality on the triage pass is good
  enough. If we need to escalate more aggressively to Haiku, the triage
  line rises to ~$50/week — still fine, but changes the shape. A 1-day
  triage-quality prototype (checkpoint §6 flag #6's ask) is in §4 risks.

### 2.6 The claim-method mismatch detector (Q-M4 direct response)

GEPA is the named pain case. The design:
- Triage pass extracts `claim_span` (what the paper says it contributes)
  and `method_span` (what the method actually does, from abstract +
  method section if available).
- A small checker prompt asks: "does the method described in `method_span`
  substantially implement the novel contribution claimed in `claim_span`,
  or is there a mismatch (e.g., the claim is 'agent self-evolution' but
  the method is 'prompt optimization')?"
- Output: `mismatch: bool, mismatch_kind: str, confidence: float`.
- Mismatches appear in the briefing under a **dedicated section**:
  "headline/method mismatches this cycle." The operator gets to see every
  paper whose claim may overclaim its method — the anti-Galactica section.
- Evaluation set: operator provides 10–20 historical mismatch examples
  (GEPA is #1). We measure precision@10 and recall@20 on this set in
  v1 week 6. If recall <60%, we escalate the checker to Sonnet-tier.

This is the one v1 feature where "auditable framing" (§1 concession)
becomes a named product feature, not just a UX principle.

### 2.7 Topic lifecycle (operator answer 2)

- States: `candidate → active → archived`. No deletion.
- Yearly review (wall-clock, not calendar — triggered by operator via an
  MCP command `radar.topic.review()`): shows per-topic briefing-open rate,
  inbox-query rate, artifact volume, last-active date.
- Archiving: operator marks a topic archived; all its artifacts remain
  queryable (`radar.search(topic_filter=[...])` still returns them); the
  briefing cron skips archived topics; the topic page becomes read-only.
- New topics: `radar.topic.create(name, seed_keywords, seed_papers)` —
  creates candidate → activates after first successful ingest cycle.
- Capacity: hard limit 15 active topics (operator constraint). A candidate
  that would exceed 15 is refused until an active topic is archived.
- All historical briefings stay in Obsidian with timestamped paths, even
  for archived topics.

### 2.8 Build sequence (8-week solo plan, one architect + junior rotation)

Week 1 — storage schema + arxiv+OpenAlex ingestion + topic seed config.
   Junior task: write ingestion adapters with integration tests against
   real API (per CLAUDE.md: no mocked external deps on critical path).
Week 2 — Semantic Scholar lookup + GitHub trending + blog whitelist
   ingestion. Triage pass (GLM-4.6) scaffolding + cost telemetry.
Week 3 — second-pass framing extractor (Haiku) + claim/method-mismatch
   detector. Build eval set from operator's 10–20 historical incidents.
Week 4 — briefing generator (Sonnet) + Obsidian write. First end-to-end
   briefing for 1 topic. Operator reads, gives feedback.
Week 5 — scale to all 8 topics. Tune ranker weights from operator
   feedback. Mon+Fri cadence live.
Week 6 — MCP server + 6 tools. Serendipity valve implementation.
   Integrate into operator's Claude Code. Eval set scored (precision@10,
   recall@20 on GEPA-style cases).
Week 7 — topic lifecycle commands. X adapter stub + schema fields.
   Dashboard? No — `radar.health()` MCP tool is the status surface.
Week 8 — hardening. Backup/restore. Rate-limit edge cases. Cost audit.
   Operator-facing runbook in `projects/002-*/README.md`.

This fits the operator's "6–12 months with 1 arch + 6–7 juniors" budget
with 4–5x slack for the inevitable unknowns. The 8-week critical path
assumes one full-time architect + ~2 junior equivalents (5–8 h/day each);
the remaining juniors work on v1.5 preparation (entity resolution
experiments, X adapter implementation) in parallel.

---

## 3. ≤2 disagreements with testable hinges

### Disagreement 1 · Briefing cadence should be twice-weekly, not weekly

**What S2 assumed**: both Opus and GPT S2R1 + checkpoint §3 assumed a
**weekly** Monday briefing.

**What Q-M3 says**: operator reads Mon AM + Fri AM. Two reading sessions
per week, not one.

**My claim**: briefings must be **twice-weekly** (Mon AM covers Fri→Mon
window; Fri AM covers Mon→Fri window), not weekly.

**Counter-claim (anticipated from GPT)**: twice-weekly doubles briefing
generation cost (still cheap, ~$2/week) but may *halve per-briefing
signal density* — fewer new items per window, more noise in the "top 15."
The honest test is whether each briefing still hits the "≥3 items worth
reading" bar.

**Testable hinge**: in v1 week 4–6, track operator's per-briefing open-
and-read rate. If Fri briefing drops below 50% open OR below 1.5 items-
read-per-briefing, collapse to weekly Monday + Friday-summary-as-delta
instead of full Friday briefing. This is a 4-week decision, not a
design-time decision. Concrete metric, falsifiable.

### Disagreement 2 · Reserve pgvector/vector search until week 5, not v2

**What the checkpoint implied**: the MVP avoided "vector DB in v1" but
didn't commit either way.

**My claim**: `pgvector` on the same Postgres instance (no separate
vector DB) must be in v1 from week 1. Recall-first search across 1,700+
artifacts/week needs semantic retrieval; keyword-only search will produce
a `radar.search` tool that *misses* precisely the cross-phrased cases
(GEPA searched with "self-evolution" won't find papers phrased
"self-improvement" otherwise).

**Counter-claim (anticipated)**: pgvector adds operational complexity
(index tuning, recall/latency tradeoffs, potential pg version
constraints) and Week 1 is storage-schema week, not retrieval-
infrastructure week.

**Testable hinge**: in week 2, compare `radar.search("self-evolving
agents", semantic=True)` against `radar.search(..., semantic=False)` on
the 10–20 operator-provided historical cases. If semantic retrieval
recovers ≥2 more cases than keyword, pgvector stays. If not, rip it out
and revisit in v1.5. This is a 1-day spike, testable, reversible.

---

## 4. Top 3 risks (engineering)

1. **Blog ingestion becomes a compliance rat-hole.** Whitelist of ~15
   blogs sounds small; in practice each site has its own rate-limit and
   robots.txt posture, and at least one will challenge our crawling
   stance. Mitigation: use a conservative `User-Agent`, honor robots.txt
   strictly, cap at 1 req/5s per host, and maintain a per-blog compliance
   note in the config. Fallback: drop to RSS/Atom where available. Budget:
   1 week of operational drag over v1 lifetime.

2. **Triage-quality collapse at cheap tier.** GLM-4.6 or MiniMax-M2 on
   2000-token abstracts *may* hallucinate claim/method spans. If so, the
   claim/method mismatch detector becomes unreliable — which is worse than
   not having it, because it creates false alarms (GPT's Galactica failure
   mode inside our own pipeline). Mitigation: a 1-day spike in week 3 —
   run cheap triage on 100 known-good papers, hand-label, measure
   claim-span and method-span extraction accuracy. If <80% accuracy,
   escalate triage to Haiku 4.5 ($0.0008/1k in tier). Cost impact: +~$20/
   week, still fine.

3. **Operator never opens the Fri briefing.** Pattern A (useful-but-niche
   plateau) applies especially to twice-weekly cadence. Mitigation: track
   per-briefing open rate from week 4 onward; if Fri rate < 50% after
   week 6, cut to Mon-only + Fri-delta (see §3 Disagreement 1). Second
   mitigation: the MCP tool `radar.topic.what_am_i_missing` exists so the
   operator gets value even on briefings he skips. This is the "D alongside
   A" bet cashed out — if A's briefing fades, D's pull-surface is still
   live.

---

## 5. ≥1 concession

**Concession #1**: adopted GPT S2R1's framing that the system is a
**triage + memory + audit substrate**, NOT an "AI that issues verdicts."
My S2R1 kept the phrase "auditable verdicts," which retained product
ambition that Stage 1 evidence (Pattern E: novelty-scoring fragility)
doesn't support. Stage 3 now defines the output as **framings + advisory
hints + mismatch flags**, and the human produces verdicts using those.
This shows up in the UX: briefings never print "novelty: 0.87" — they
print "claim: X. method: Y. adjacent work: Z. possible mismatch flag:
none/claim-overstates-method/…" and the operator integrates.

**Concession #2**: the checkpoint §6 flag #2 (inbox size) was a real
issue I under-priced in S2R1. Running the math (§2.5) shows 1,700+
items/week in the inbox. Recall-first does NOT mean the operator scans
everything. The product framing must be explicit: briefing is what you
read; inbox is the recall guarantee (queryable, not linear). This is a
UX redesign, not a scope change — but it's an honest correction to my S2
framing.

---

## 6. Self-critique

Three things I'm under-confident about in this round:

- **The twice-weekly cadence call might be over-fitting to Q-M3.** Operator
  said he reads Mon + Fri AM. That might mean "I want a briefing both
  days" OR it might mean "I catch up on missed days." The testable hinge
  in §3 covers it, but I'm making a choice from one data point.
- **The 1,700 artifacts/week pre-filter estimate might be off by 2x in
  either direction.** Pre-filter by topic keyword is cheap but brittle.
  The real number could be 3,000/week (keywords too generous) or 600/week
  (keywords too strict and we miss cross-phrased work like the GEPA case).
  Week 1 of v1 has to measure this empirically and tune — which is in the
  plan, but it means the cost estimate and the inbox-ergonomics argument
  are both sensitive to this.
- **The claim/method mismatch detector is the most novel piece of v1 and
  also the least-proven.** GEPA is one data point. If the operator can't
  supply 10–20 historical examples in week 3, the eval set is too small
  to tune on — and without tuning, the mismatch section of the briefing
  will either be noisy (false alarms, undermines trust) or silent (no
  interesting flags, operator stops reading that section). This is a
  product feature that lives or dies on data the operator hasn't yet
  provided. It should be called out as a v1-gate in week 3: if ≥10
  historical cases aren't findable, *don't ship the mismatch detector
  in v1*, push it to v1.5.

---

## 7. Open decision questions for S3R2 or moderator

Three, ranked by how much they change the v1 plan:

**D1. GLM-4.6 vs. MiniMax-M2 for triage pass.** Both are cheap enough.
Which the operator's environment has already been integrated against
affects week 2 velocity. If neither is integrated, a ~1 day spike picks
the winner on the 100-paper eval (§4 risk 2). Ideally the moderator picks
so junior-team gets unblocked day 1.

**D2. Obsidian vault path + whether briefings are append-only or
replace.** Appending preserves history but pollutes the vault. Replacing
loses history but keeps search clean. My lean: write to dated paths
(`YYYY/MM/YYYY-MM-DD-<topic>.md`) — append via new file per cycle. But if
operator prefers living pages per topic (one file per topic, always
freshest content), the schema is cleaner. Operator preference decides.

**D3. Which 10–20 historical mismatch cases for the GEPA-style eval?**
Operator supplied 1 (GEPA). If operator can supply 10–20 by end of week
2, the claim/method detector ships in v1. If not, push to v1.5. This is
the one engineering-scope decision that has a calendar-hard deadline
(week 3 of v1).

---

<!-- not READY-TO-CONCLUDE -->

Rationale for not marking READY-TO-CONCLUDE: this is S3R1. There's been
no opposing engineering round yet. GPT's S3R1 will land soon and may
present alternatives on the stack (e.g., vector DB choice, scheduler,
LLM router, or — most likely — a different MVP slice prioritization).
At least one round of engineering-mode back-and-forth is needed before
finals; marking ready now would skip the opposition pass that protocol
§"Quality bars for stage advancement" requires for S3 → Finals.

---

### One-line summary

**S3R1: engineering plan for A-primary + B-schema + D-MCP-alongside.
Pinned stack (Postgres + pgvector + GLM/Haiku/Sonnet routing, no web UI).
8-week MVP with claim/method-mismatch detector targeting GEPA-style
cases. 2 testable-hinge disagreements (twice-weekly cadence, pgvector in
v1). 2 concessions (triage-not-verdicts framing from GPT; inbox-size
math). 3 open decision questions for the moderator / S3R2. Not
READY-TO-CONCLUDE — awaiting GPT S3R1.**
