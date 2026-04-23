# Stage 2 Checkpoint — Idea 002 · Research Radar

**Prepared for moderator**: decision required before Stage 3.
**Date**: 2026-04-22
**Inputs digested**: `002-stage1-synthesis.md` (320 lines), `002-moderator-notes.md` (4 binding answers), `002-Opus47Max-S2R1.md` (361 lines), `002-GPT54xHigh-S2R1.md` (136 lines), `proposals/proposals.md` entry 002.

**Debaters' honest verdicts on "build or not"**:
- **Opus**: **Y, conditionally** — only as a lab-internal tool, anchored on idea-migration provenance + in-progress-project integration; N if the operator's current workflow is already served by Semantic Scholar Research Feeds + Zotero + papersgpt.
- **GPT**: **Y, conditionally** — only if v1 is internal-tool-first, open-access-only, recall-first, auditable, topic-lifecycle-aware, and changes the operator's workflow within weeks.
- **Agreement**: **Yes, qualified**. Both are Y, both impose nearly identical conditions. Both would flip to N if the operator demands autonomous judgment or mandates X-as-v1-dependency.

---

## 1. Unified direction catalog (4 candidates)

Opus and GPT each proposed 4 directions. The naming differed but the structure maps cleanly. Opus surfaced Direction D (Project-Linked) as "new content" in S2R1; GPT had arrived at a near-identical direction independently (their Direction C · Project Watchtower). This cross-model convergence is a strong signal that the four directions below are the real option space, not an artifact of either debater.

Cross-map:
- **Unified A ↔ Opus-B (Briefing+Inbox) ↔ GPT-A (Topic Radar Ledger)** — topic-first, ranked inbox under a weekly briefing.
- **Unified B ↔ Opus-A (Idea-Migration) ↔ GPT-B (Idea Provenance Graph)** — idea-first, cross-artifact lineage.
- **Unified C ↔ Opus-D (Project-Linked Radar) ↔ GPT-C (Project Watchtower)** — active-project-first, decision-shortened loop.
- **Unified D ↔ Opus-C (Radar-as-MCP) ↔ GPT-D (Agent-Native Research Memory)** — agent-tool-first, no dedicated UI.

### Direction A — topic-ledger-briefing
**Surfaced by**: Opus-B (named "Weekly Briefing Service + Read-Through Inbox") + GPT-A ("Topic Radar Ledger"). Both arrived independently; Opus leaned this direction explicitly.
**Primary entity**: Topic (8–15 standing, with yearly churn).
**User**: Operator first, senior lab members second.
**Value prop**: A weekly briefing per standing topic, delivered as Obsidian-compatible markdown, backed by a read-through inbox of every ingested artifact. Recall-safety-net built in — nothing dropped, everything ranked.
**How it differs from prior art**: Competitive with Semantic Scholar Research Feeds + Zotero + papersgpt-for-zotero at the artifact layer. Defensibility rests entirely on the **lab-project-aware** ranking layer — does the briefing know what the lab is currently building? If yes, differentiated; if not, re-skin.
**What has to be true for this to work**: (a) Monday-morning briefing is a format the operator actually reads (synthesis §11.1, unresolved). (b) The inbox remains genuinely useful on days the briefing is skipped. (c) Light project-awareness hooks can be bolted on without committing to full Direction C.
**Biggest risk**: "useful-but-niche plateau" (synthesis Pattern A) — the briefing becomes a Monday ritual that slowly stops changing behavior; without the project-awareness hook it collapses into an arxiv-sanity + research-feed hybrid.
**Serendipity valve**: "possibly-overhyped" + "possibly-underrated" sections in every briefing, both LLM-flagged with citations.
**X-hook posture (operator answer 3)**: Pluggable adapter behind feature flag; off in v1; can power the "overhyped/underrated" sections later.
**Evidence grounding (S1B)**: Medium. Systematic-review screening literature (GPT's S2R1 sources) supports recall-first-plus-ranked. Weekly-over-daily cadence is evidence-poor — debater intuition only.
**Imagination vs evidence**: Inbox-backed-briefing UX shape is **hypothesis**. Recall-biased architecture is **evidence-supported**. Lab-project-aware differentiation is **hypothesis** until the operator's project-state discipline is known.

### Direction B — idea-provenance-graph
**Surfaced by**: Opus-A ("Idea-Migration Radar") + GPT-B ("Idea Provenance Graph"). GPT framed it first in S1A ("motion of ideas"); Opus conceded in S1B §1 that this framing is stronger than his original paper-centric one.
**Primary entity**: Idea (an addressable thing with provenance across paper → repo → blog → discourse).
**User**: Lab lead and advanced researchers who care about lineage, novelty framing, onboarding into a subfield.
**Value prop**: Each idea is a first-class node with a provenance chain; topic pages are views over an idea graph. The system answers "has this idea been done? where did it migrate? what contradicts it?"
**How it differs from prior art**: This is the single most-defendable novelty claim in the prior-art catalog (synthesis §8). arxiv-sanity, papersgpt, Research Feeds, Elicit/Consensus/Scite are all paper-centric or library-centric. Nothing in the graveyard tracks idea-provenance across artifact types. Scite tracks *citation context*; that is adjacent, not the same thing.
**What has to be true for this to work**: (a) Cross-artifact entity resolution works reliably enough that false merges/splits don't poison the graph. (b) The operator tolerates a slow start — idea nodes accumulate value over months, not days. (c) Provenance claims are auditable (every edge in the DAG traces back to extractable evidence).
**Biggest risk**: Entity resolution across artifact types (paper ↔ repo ↔ blog ↔ discourse) is research-grade engineering, not turn-key. Synthesis §9 scored feasibility = M (Opus's estimate). False merges quietly poison the graph and are hard to audit at scale. Pattern E (novelty-scoring fragility) applies here too — any "lineage" edge that requires LLM judgment inherits adversarial fragility.
**Serendipity valve**: Cross-topic forcing function — pick one idea adjacent to a different lab's topic once/week and surface the bridge.
**X-hook posture**: Discourse is a first-class artifact type in the idea graph; X becomes one source of discourse nodes. Still pluggable — can ingest from Bluesky/Mastodon/Discord + public blogs in v1, add X later.
**Evidence grounding (S1B)**: Medium. Novelty-scoring fragility literature (NovBench, GraphMind, Literature-Grounded Novelty, DeepReview) argues against using LLMs for autonomous idea-lineage judgments. Counter-evidence: nothing in prior art does this, so the territory is genuinely open.
**Imagination vs evidence**: The *existence* of un-owned territory is **evidence-supported** (synthesis §8 derivation). The *feasibility* of solo-team implementation in 6–12 months is **hypothesis**. The claim that operators will value it enough to use it weekly is **hypothesis**.

### Direction C — project-linked-radar
**Surfaced by**: Opus-D ("Project-Linked Radar" — new in S2R1) + GPT-C ("Project Watchtower"). Both arrived independently; neither was central in S1.
**Primary entity**: Active project in the lab (not topic, not idea, not paper).
**User**: Lab lead for project-level decisions; students/researchers attached to live project threads.
**Value prop**: "What changed that matters for project Y since we last looked?" Each active project has a live "related work since you started" page; standing topics are background. Shortens the loop from external signal to internal decision.
**How it differs from prior art**: Nothing in the prior-art catalog does this *at all*. Research Feeds trains off library folders; Elicit serves one-shot queries; Iris.ai is enterprise workspace. None integrate with "what is this lab actively building right now?" Synthesis §8 explicitly named this as part of the un-owned territory.
**What has to be true for this to work**: (a) The operator (and lab) maintain a reasonably current machine-readable or structured-text view of active projects. (b) Projects are stable enough over weeks/months that "related work since you started" is well-defined. (c) Bootstrap friction — "we're working on X, Y, Z this quarter" — is a cost the operator will pay.
**Biggest risk**: Depends on disciplined project-state capture that may not exist. Projects come and go faster than topics. If the lab doesn't maintain a current project view, the system has nothing to anchor to — and building the project-tracking UX is itself a sub-product. This is a **pre-condition-heavy** direction: fail the pre-condition and the whole direction collapses.
**Serendipity valve**: "Adjacent-project" feed — literature one step away from the active project, including negative results that would argue against continuing.
**X-hook posture**: X signal is likely most valuable for *project* surveillance specifically (a debate breaking around a technique your team is building matters more than the same debate on a dormant topic). But still v2 — operator answer 3 is binding.
**Evidence grounding (S1B)**: Low-to-medium. S1 did not search for project-linked-research-tools literature because the direction didn't exist yet. The prior-art-gap claim is evidence-supported (catalog is empty for this). The pre-condition claim (project-state discipline) is **not evidenced** — it's debater inference about the operator.
**Imagination vs evidence**: The *differentiation* is **evidence-supported** by absence in prior art. The *pre-condition* (operator maintains structured project state) is **unverified**. This is the moderator question that collapses C into "great direction" or "bootstrap-friction death" depending on the answer (see §5, Q-M2 unresolved).

### Direction D — radar-as-mcp
**Surfaced by**: Opus-C ("Radar-as-MCP") + GPT-D ("Agent-Native Research Memory"). Both arrived independently.
**Primary entity**: Not fixed — the system exposes whatever underlying model (topics / ideas / projects) is chosen through MCP tool calls.
**User**: The operator specifically, because his daily surface is already Claude Code (proposal constraint).
**Value prop**: No new UI. No briefing cron. The lab's knowledge store, prior-art database, and "what's new" queries are all exposed as MCP tools callable from Claude Code / Cursor / Codex. A nightly ingestion daemon maintains the store; queries happen on demand.
**How it differs from prior art**: Lowest UI-maintenance load. Directly mitigates synthesis Pattern D (manual-pipeline decay) because there's almost nothing to maintain in the UX layer. Naturally agent-first — fits the operator's "Claude Code is my surface" constraint.
**What has to be true for this to work**: (a) Operator's daily workflow is actually agent-first enough that he remembers to ask. (b) Cold-start value exists — i.e., the tools are useful even before the operator builds habits around them. (c) "If I don't ask, nothing surfaces" is acceptable to the operator.
**Biggest risk**: Too low-surface. If the operator doesn't query the agent about research often enough, the system sees no usage and cold-start value is zero. GPT's Pattern-A test ("narrow weekly workflow a real researcher would miss if gone") is *harder* to pass when there's no proactive surface — you can't miss what never pinged you. This is the mirror-image risk of Direction A's "ritual that stops changing behavior."
**Serendipity valve**: Explicit `research.what_am_i_missing(topic)` tool that returns adversarial-taste-pair output ("here's what the default ranker would have hidden").
**X-hook posture**: Queried on demand rather than polled — if operator asks "what is X saying about RAG this week?", an adapter fetches then; otherwise X stays dark. Lowest compliance surface of all four directions.
**Evidence grounding (S1B)**: Low. S1B did not search for MCP-as-research-surface adoption data. Opus's S2R1 claim that "the operator already lives in Claude Code" is from the proposal itself; moderator should confirm whether that includes *research-question-asking* or just *code-writing*.
**Imagination vs evidence**: UI-maintenance reduction is **evidence-supported** (Pattern D logic). Cold-start risk is **evidence-supported** (Pattern A logic). Operator-fit is **hypothesis** — depends on moderator answer to Q-M3 (Monday reading workflow).

---

## 2. Comparison matrix

Columns per the request: primary entity, differentiation vs prior art (specifically Research Feeds / papersgpt / Elicit-Consensus-Scite / arxiv-sanity), engineering risk (1 architect + 6–7 juniors × 6–12 months), recall-bias fit, topic-churn fit, serendipity-valve default, X-hook handling, biggest open question.

| Direction | Primary entity | Diff vs prior art | Eng risk | Recall fit | Topic churn fit | Serendipity valve | X-hook | Biggest open Q |
|---|---|---|---|---|---|---|---|---|
| **A · topic-ledger-briefing** | Topic | Med — overlaps Research Feeds + papersgpt unless lab-project-aware | **Low-Med** | **High** — inbox is the recall guarantee | **High** — topic lifecycle is native | Over/underrated sections in briefing | Pluggable v2 adapter | Does operator actually open a Monday briefing? |
| **B · idea-provenance-graph** | Idea | **High** — no prior art does idea-migration across artifact types | **Med-High** — cross-artifact entity resolution is research-grade | Med — graph is recall-ambiguous unless low-confidence edges stay visible | Med — topics become views over graph, churn is easier here | Cross-topic forcing function | Discourse as first-class artifact; X is one source | Can false-merge rate stay below poison threshold? |
| **C · project-linked-radar** | Active project | **High** — nothing in prior art project-links research | **Med** (iff project state exists) / **High** (iff it must be built) | High — project-scoped recall is clean | Med — topics are background, projects dominate | Adjacent-project feed, including negatives | Most useful here, but still v2 | Does the operator maintain structured project state? |
| **D · radar-as-mcp** | Flexible (topic or idea) | Med — lowest UI risk but lowest surface too | **Low** — minimal UX layer | Med — no filtering, but no push either | Med — whatever underlying schema supports | `research.what_am_i_missing(topic)` tool | On-demand fetch; lowest compliance surface | Is operator's Claude Code usage research-heavy enough to trigger queries? |

Score legend: Low / Med / High. "Engineering risk" folds in both complexity and pre-condition fragility. "Eng risk" for C is bimodal — depends entirely on Q-M2 answer.

### Secondary matrix — mapping to synthesis §8 standing-novelty components

Synthesis §8 listed six components of the defendable novelty. Directions score differently on each:

| Novelty component | A | B | C | D |
|---|---|---|---|---|
| Lab-specific | Yes | Yes | **Yes (primary)** | Yes |
| Topic-scoped (8–15) | **Yes (primary)** | Derivative | Background only | Configurable |
| Idea-migration aware | Hypothesis (v1.5 upgrade) | **Yes (primary)** | Partial | Configurable |
| Auditable verdicts | Yes | Yes (graph edges must be) | Yes | Yes |
| Serendipity valve | Section | Cross-topic | Adjacent-project | Explicit tool |
| Narrow daily/weekly workflow | **Yes (weekly)** | Weekly via topic views | Project-checkpoint cadence | Pull only, no cadence |

> **Reading the matrix**: A covers 4/6 primaries; B covers 1/6 primary + is the unique home of idea-migration; C covers 1/6 primary + is the unique home of project-linking; D covers 0/6 primaries but is the cheapest shell. None covers all six. A composition of A + B's schema (Opus's lean) covers 5/6 at the cost of v1 scope.

---

## 3. Synthesizer recommendation

### **Advance with Direction A, built on Direction-B-compatible schema, with Direction-D exposed alongside from day one.**

This is **Opus's explicit lean** from S2R1 §4 and is consistent with GPT's framing (GPT did not pick in S2R1 per protocol, but their Direction A description is the same shape; their analysis of B's risk matches Opus's "2x engineering risk" assessment; their Direction D framing is structurally compatible with "MCP exposed alongside").

Reasoning, honest:

1. **A is the falsifiable-within-6-weeks direction.** The weekly briefing is a behavioral product — if the operator isn't opening it Monday morning after six weeks, the direction is dead and we know fast. B and C have value that compounds over months and are correspondingly slower to falsify. D has the opposite problem: it's falsifiable only by absence-of-queries, which operators tend to rationalize away.

2. **A is the right recall-biased architecture.** Operator answer 1 (`更怕漏报, 可以接受小部分误报`) is binding. A's inbox-under-briefing is the most honest implementation: nothing dropped, everything ranked, briefing is opinionated but ground truth is always visible. B, C, D can each be made recall-biased but require more design care. A's recall guarantee falls out of the architecture naturally.

3. **B's defensibility is real but priced too high for v1.** Synthesis §8 correctly identified idea-migration provenance as the narrowest defendable novelty. But cross-artifact entity resolution (paper ↔ repo ↔ blog ↔ discourse) is research-grade work. For a solo-operator + 6–7-junior team on a 6–12 month budget, betting the first release on a research problem is risky. **Compromise**: design A's storage schema to permit promoting artifacts to idea-nodes later (Opus's Q-M5 proposal). This costs a small v1 tax but keeps B open as a v1.5 upgrade rather than a v2 rewrite.

4. **C is attractive but pre-condition-dependent.** If the operator already maintains structured project state (a shared doc, a Linear project list, a running quarterly plan), C is arguably the best direction because it has the cleanest no-prior-art claim and the cleanest "shortens a real decision loop" story. If he does not, C is bootstrap-friction-heavy and the project-tracking UX becomes a sub-product. **This is why Q-M2 must be answered before direction-lock**. If Q-M2 comes back "yes, I maintain project state," the recommendation should flip to C-primary with A's briefing as the output surface for project-scoped digests.

5. **D as UI-surface alongside A is near-free.** If A's topic-store and artifact-store are first-class services, exposing them as MCP tools is a day-3 task, not a month-3 task. The operator gets both the push (Monday briefing) and pull (in-chat query) surfaces with one underlying store. This is the synthesis §9 "not mutually exclusive" note cashed out.

### Honest caveats

- **The standing novelty is narrow.** Synthesis §8 said this plainly. If the operator comes into Stage 3 expecting a category-creating product, the recommendation is wrong. This is a personal-tool-with-publishable-internals, not a SaaS wedge.
- **"A + B schema + D alongside" is more scope than pure A.** Stage 3 engineering-mode needs to explicitly bound v1 to the pure-A product (briefing + inbox + topic lifecycle + recall-first ranking) and defer B's entity resolution and D's MCP server to v1.5. If Stage 3 tries to ship all three at once, we're back in the full-chief-of-staff failure mode.
- **A's differentiation against Research Feeds collapses if lab-project-awareness doesn't land.** This is non-negotiable — the briefing layer MUST know something about what the lab is actively building, otherwise it's a re-skin of commodity tools. Even in A-primary, some lightweight project-awareness must ship in v1.
- **The "flip to C" path is real.** If Q-M2 comes back positive, and Q-M1 comes back "topic list is hazy," that's strong evidence C-primary is better than A-primary. Do not lock direction until those two questions are answered.

---

## 4. Moderator decision menu

The moderator (human operator) must choose ONE of these four paths. This document stops here — the decision belongs to a human, not to me.

### Option 1 · ADVANCE

Choose a direction from §1. Then run Stage 3 kickoff.

**Recommended advance**: **Direction A (topic-ledger-briefing) built on B-compatible schema, with D exposed alongside from v1 for the operator's Claude Code workflow.** See §3 for reasoning.

If moderator advances, the Stage 3 protocol requires:
```
/debate-next 002 3 1        # Opus S3R1 in engineering mode
```
Codex counterpart: paste the S3R1 kickoff from `discussion/PROTOCOL.md`.

**Moderator records** (fill in before advancing):
- Direction chosen: ____________________
- Deviation from recommendation (if any): ____________________
- Rationale (1–3 sentences): ____________________
- Answers to Q-M1 through Q-M5 (see §5) before Stage 3 starts, or explicit "will answer during S3R1 review" note: ____________________

### Option 2 · FORK

Pursue multiple directions as separate proposals. Useful if moderator sees A and C as peer-valuable and doesn't want to pick.

Concrete fork suggestions:
- **002a · Topic Briefing Tool** — Direction A as a personal-tool-scoped proposal. Scope = briefing + inbox + topic lifecycle. Timeline = 3 months. Ambition = M.
- **002b · Idea-Provenance Prototype** — Direction B as a research prototype (publishable-internals framing). Scope = idea-migration entity resolution + graph viewer. Timeline = 6 months. Ambition = L. This is explicitly a research project first, a product second.
- **002c · Project-Linked Radar** — Direction C as a lab-workflow proposal, **gated on** moderator confirming project-state discipline exists (Q-M2). If Q-M2 is "no," 002c should not fork yet.
- **002d · Research MCP Surface** — Direction D as a minimal agent-tool proposal, possibly worth doing *after* 002a to expose 002a's store via MCP. Timeline = 2–3 weeks on top of 002a.

Fork process:
1. Add new entries to `proposals/proposals.md` (002a, 002b, 002c, 002d as chosen).
2. For each, run `/debate-start <new-id>`.
3. Archive `discussion/002/` as "forked; see 002a/002b/…".

**Honest note on fork**: forking now means 2–4 parallel debates and 2–4 parallel builds. For a solo-operator + 6–7-junior team on a 6–12 month total budget, fork is probably the wrong call unless the operator specifically wants 002b as a research side-track separate from the main build. Direction A and its B-compatible schema already capture most of what's defendable; forking A and B burns budget to maintain two codebases for marginal defendability gain.

### Option 3 · PARK

Interesting but not now. Revival conditions:
- **Revive when**: (a) The operator has answered Q-M1 through Q-M4 with specific content, AND (b) The operator has used Semantic Scholar Research Feeds + Zotero + papersgpt-for-zotero as his primary workflow for 4–6 weeks and can describe specifically what's still missing.
- **Do not revive if**: The existing stack turns out to be sufficient. That's itself a valuable finding.

Park process:
1. Update `proposals/proposals.md` entry 002: Status = parked, reason = "pre-conditions (Q-M1 through Q-M4) not yet answered; operator has not trialled existing stack."
2. Archive `discussion/002/` as-is; it's valuable reference for whoever picks this up later.
3. Add calendar reminder: 6 weeks out, check "did existing-stack trial produce a concrete gap list?"

**Honest note on park**: The most likely park trigger is Q-M3 coming back "I don't actually have a Monday reading workflow, I mostly catch up when I can." If that's the answer, we don't know what the product replaces — and without that, any direction is guessing. Park is legitimate here.

### Option 4 · ABANDON

Evidence says don't build this.

**Abandonment lesson distilled from Stage 1 + Stage 2**: "The defendable wedge in AI-research-surveillance space is narrow (idea-migration + project-linking). The commodity layers (retrieval, summarization, citation-context, personalized-feed, private-library-QA) are already shipped and free or cheap. Before building, a solo-operator should spend 4–6 weeks using Research Feeds + Zotero + papersgpt-for-zotero as their primary workflow and generate a concrete missing-capability list. If no concrete list emerges, that is strong evidence the standing novelty — while real — is not worth 6–12 person-months of build."

Abandon process:
1. Update `proposals/proposals.md` entry 002: Status = abandoned.
2. Write `discussion/002/002-abandonment-lesson.md` with:
   - The idea (Research Radar as originally proposed).
   - Why it seemed good (AI-firehose premise is real; bounded lab scope is unusually favorable for an internal tool).
   - What killed it: commodity layers already cover 80% of the value; the defendable wedge (idea-migration / project-linking) is narrow and research-grade; the operator may not have the pre-conditions (written topic list, project state discipline, agent-first research workflow) that several directions depend on.
   - What to do with the freed time: 4–6 weeks with existing-stack + a short written "gap list." If the gap list is specific and painful, revive as 002-v2 with a direction locked by the actual gap.
3. Archive `discussion/002/`.

**Honest note on abandon**: Abandon is a legitimate option given synthesis §8's "personal-tool-with-publishable-internals, not a unicorn" framing, and given the unanswered Q-M1 through Q-M5. I am not recommending abandon — but I would not call it wrong. If the moderator senses they're building-to-build rather than building-to-use, abandon now is cheaper than abandon in month 4.

---

## 5. Unresolved questions carried forward

If moderator chooses ADVANCE, the five questions Opus surfaced in S2R1 §6 are still open and Stage 3 must address them. Ranked by how much they change the engineering plan:

**Q-M1 · Does a written list of 8–15 topics already exist?** (synthesis §11.4)
- Why it matters: Direction A's topic-ledger is the first-class surface. If the list exists, A can start from it. If it doesn't, v1 needs to *help build* the list, which is a different product shape.
- If answered "yes, here's the list": advance Direction A with topic-list-import as a day-1 task.
- If answered "not yet, will emerge": advance Direction A with topic-nucleation tools as part of v1 scope.
- If answered "I don't think in standing topics, I think in active problems": advance Direction C, not A.

**Q-M2 · Does a written list of active projects exist, and is project state reasonably current?** (surfaced in Opus S2R1; not in original synthesis)
- Why it matters: Direction C depends on this. If yes, C is the strongest direction (clean no-prior-art, clean decision-loop story). If no, C is bootstrap-friction-heavy.
- If answered "yes, we maintain project state in X": **strongly consider flipping recommendation to C-primary with A as the briefing output surface.**
- If answered "no, projects are informal": confirm A-primary; C becomes v2 conditional on project-tracking discipline developing.

**Q-M3 · What's the operator's current Monday-morning reading workflow?** (synthesis §11.1)
- Why it matters: Direction A ships a Monday briefing. If no Monday ritual exists, A is creating a new habit, not serving an existing one — much higher failure probability.
- If answered "I start in Claude Code and don't really read papers on a fixed cadence": shift toward Direction D (MCP) as primary, A as secondary.
- If answered "I have a rhythm but it's ad-hoc": A stays primary; briefing fits an existing-but-unstructured pattern.
- If answered "I already have a structured reading routine": document it; A's briefing should match it in shape.

**Q-M4 · Recent concrete incidents where the wrong paper got missed, or a student re-derived something the lab already knew?** (new; sharpens Directions A & B)
- Why it matters: These incidents are the best seed test cases for idea-migration provenance (Direction B) and for the lab-project-aware ranking layer (Direction A).
- If concrete incidents exist: they go into the Stage 3 test set and drive the recall-first ranker calibration.
- If no concrete incidents: A's lab-project-aware differentiation becomes abstract; consider weakening the recommendation.

**Q-M5 · v1 schema: idea-entity-capable from day 1, or simpler v1 that closes off Direction B permanently?** (Opus S2R1 design question)
- Why it matters: This is a small Stage-3 engineering-scope question that deserves an explicit call. Keeping idea-entity-capability in the v1 schema is a small ongoing tax; removing it closes off the B upgrade path.
- Default recommendation: keep it. Tax is small; option value is large.

If moderator chooses FORK / PARK / ABANDON, these questions are irrelevant — they came with the not-chosen paths. (Though Q-M1 through Q-M4 are still useful before a future revive.)

---

## 6. Honesty check

Things I noticed that the debate might have under-weighted. §6 is mandatory per protocol.

1. **Neither debater priced the cost of *not* using Semantic Scholar Research Feeds as a baseline.** Both conceded Research Feeds is ready-made prior art; neither asked whether the operator should simply *use* Research Feeds for 4 weeks and see what's actually missing. That would be the cheapest possible Stage 3. The recommendation in §3 assumes the operator won't do this; if they would, "use Research Feeds for 4 weeks then decide" is a better next step than any Stage 3 direction.

2. **"Recall-first with everything visible in an inbox" is not free.** Operator answer 1 (`更怕漏报`) sounds unambiguous, but recall-first at AI-research volume (≈60+ cs.AI papers/day × 8–15 topics = 500–900 artifacts/day pre-filter) means the inbox has 3,000–5,000 items/week. Ranking is not filtering; the operator still has to *look at* or trust-the-ranker-on *all* of them at some level. "Small inbox the operator actually reads" is a product constraint that neither debater sized. This risks A shipping an honest recall-first architecture that the operator then silently ignores because the inbox is too big to scan — which is itself a Pattern A outcome.

3. **The "lab-project-aware" layer in Direction A is doing heavy lifting but has almost no evidence behind it.** In §3 I wrote that A's differentiation against Research Feeds "rests entirely on" lab-project-awareness. This is true, and it's largely a hypothesis. Neither debater searched for evidence that "personalized paper ranking becomes more useful when the ranker knows about the reader's active projects." It's plausible, but it's not evidenced. Stage 3 should plan a cheap A/B within v1 to verify.

4. **Direction B's "research-grade engineering" framing may be underselling LLM progress.** Both debaters scored B's entity resolution at Med-High risk based on 2024–2025 evidence. By mid-2026 some of that evidence is stale — cross-artifact matching may be a tractable prompt-chain on Claude/GPT-tier models with careful evaluation. Synthesis §7 did not re-verify this for 2026. If cross-artifact matching is actually Med risk (not Med-High), Direction B's engineering-risk penalty in §2 is too harsh, and B becomes more competitive with A.

5. **Direction C's pre-condition (project state discipline) may be easier to build than the debate assumes.** Both debaters treated "lab maintains structured project state" as a hard pre-condition — if it doesn't exist, C collapses. But a lightweight project-capture UX (weekly 5-minute "what are you working on?" prompt per researcher) is ~1 week of engineering. If the operator is willing to pay the people-cost (asking researchers to answer weekly), C's pre-condition becomes a feature, not a collapse condition. Neither debater proposed this.

6. **Nobody priced GPU/local-model assumptions.** The proposal specifies a 24 GB 4090 + GLM/MiniMax for cheap inference. Opus S1B §10 noted this was assumed-not-verified. At 3,000–5,000 artifacts/week × ~10k-token triage per artifact, even cheap models add up. Budget check: 4,000 artifacts × 10k tokens × $0.00005/1k tokens ≈ $2/week on MiniMax-tier pricing — fine. But LLM-generated *weekly briefings* (thousands of tokens of output per topic × 8–15 topics × 52 weeks) and LLM-graded *lab-project-aware ranking* (expensive reasoning, not just classification) could be 10–50× that. The "cheap LLM economics" assumption deserves a 1-day prototype before Stage 3 direction-locks. This was the synthesis §11.6 action item and it remains undone.

7. **The moderator's four answers are unambiguous but one of them is a latent scope expander.** Operator answer 3 on X (`留个口子`) was framed by both debaters as "v2, pluggable adapter." That's correct for v1. But "留个口子" implies architecting for X ingestion in v1 — schema fields, adapter interface, rate-limiting plumbing. That's scope that could silently grow if Stage 3 doesn't explicitly size it. Keep the adapter interface + schema stubs; defer the actual X client to v2; make this explicit in Stage 3 task decomposition.

---

**End of Stage 2 Checkpoint.**

**Moderator action required before Stage 3. Pipeline is paused.**
