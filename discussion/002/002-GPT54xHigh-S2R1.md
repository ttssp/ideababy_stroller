# Idea 002 · S2R1 · GPT54xHigh · Position (cooperative)

**Timestamp**: 2026-04-22T23:17:34+0800
**Stage**: 2 (Position). Cooperative, not adversarial.
**Read first**: `002-stage1-synthesis.md`
**Also read**: `discussion/PROTOCOL.md`, all S1A + S1B rounds, `002-moderator-notes.md`, proposal `002`
**Searches this round**: 3 targeted, not broad

---

## 1. What I now believe the idea actually is (sharpened)

After Stage 1, I think the idea is narrower, more operational, and more defensible than the original proposal text implied:

- It is **not** a general "AI research recommender" product.
- It **is** a lab-internal, open-access-only, recall-first research surveillance system for a single operator and his lab.
- Its job is not to output confident autonomous verdicts on "novelty / impact / utility" as if those were solved labels. Its job is to **capture broadly, rank transparently, preserve traces, and help a human make forward-looking judgments with receipts**.
- The stable unit of work is probably **8-15 evolving topics**, but the deeper unit of memory may be either **ideas** or **active projects** depending on which direction we choose.
- The system must treat "low value" artifacts as **visible but deprioritized**, not silently dropped. That is now a binding consequence of the operator's note that false negatives hurt more than some false positives.
- X is a **future ingress hook**, not a core dependency. Official X docs now describe pay-per-use pricing and endpoint-specific limits, which is workable but not something I would put on the critical path of v1.  
  Sources: [X pricing](https://docs.x.com/x-api/getting-started/pricing), [X rate limits](https://docs.x.com/x-api/fundamentals/rate-limits)

The most important mental shift for me since S1 is this: the product should be framed less as "a model that judges the frontier for me" and more as **a research memory and triage system that makes judgment cheaper, more traceable, and less lossy**.

---

## 2. Honest Y/N on "should this be built"

**Y, conditionally.**

I think it should be built if, and only if, the first version accepts all of these constraints:

- **Internal tool first**. The wedge is lab-specific workflow, not a broad market claim.
- **Open-access only**. The operator has already made this explicit, and it usefully removes a lot of ingestion/compliance drag.
- **Recall-first architecture**. Use ranking, confidence, and stop rules; do not pretend aggressive filtering is safe.
- **Auditable outputs**. Every summary or verdict should link back to source artifacts and prior topic state.
- **Topic lifecycle support**. Topics will change over time, so the system needs create / active / archived states rather than a frozen taxonomy.
- **Narrow usage test early**. Within a few weeks, it should noticeably change the operator's Monday or weekly reading workflow. If it does not, the honest move is to stop widening the scope.

Why I am still on "Y" after the Stage 1 skepticism:

- The overload premise is real.
- The prior-art catalog shows many useful slices, but not the exact "lab-specific memory + surveillance + audit trail" combination.
- The operator's constraints are unusually favorable for an internal tool: bounded users, bounded topics, high personal need, tolerance for an opinionated workflow.

What would flip me toward "N":

- If the operator actually wants fully automated judgment rather than assisted judgment.
- If the system must depend on X/social ingestion from day one.
- If the workflow cannot tolerate a ranked inbox or ledger and instead demands a tiny filtered list with near-zero misses.

If those become non-negotiable, I would recommend stitching together existing tools rather than building a custom system.

---

## 3. Candidate directions (4 peers, intentionally not picked)

These are real peers. I am not ranking them, and I am not picking one in this round.

### Direction A — Topic Radar Ledger

This version makes the **8-15 standing topics** the first-class object. Each topic has a continuously updated ledger: new papers, repos, blogs, and selected public discussion enter the ledger; each item gets an auditable summary, relevance judgment, and relationship to prior topic state; low-value items remain visible as "seen, probably not important." The outward surface is a weekly briefing plus a browsable backlog. This direction is the cleanest match to the operator's existing mental model because the proposal itself is organized around long-lived topic coverage rather than one-off queries.

**Biggest risk**: differentiation may be thinner than it first appears if the topic pages are just a polished wrapper over existing paper-feed and summarization tools.

**Target user**: the operator first, then senior lab members who need a stable per-topic memory.

**What makes it survive**: it aligns directly with the operator's stated recall preference and with evidence from ML-assisted screening, where ranking and workload reduction are valuable but stopping criteria still need explicit uncertainty handling rather than blind trust.  
Sources: [screening prioritization study](https://link.springer.com/article/10.1186/s13643-023-02257-7), [stopping criteria paper](https://link.springer.com/article/10.1186/s13643-024-02699-7)

### Direction B — Idea Provenance Graph

This version makes the **idea** the primary entity rather than the topic or artifact. A paper, repo, blog post, benchmark result, and public debate are treated as manifestations of an idea moving through the field. The system's core job becomes linking those manifestations: what is inherited, what is contradicted, what is derivative, what is implementation-only, what is hype without technical movement. Topic pages still exist, but mostly as views over an idea graph. This is the most intellectually ambitious direction and the one that most directly cashes out the Stage 1 shift from paper-centric to idea-centric thinking.

**Biggest risk**: cross-artifact entity resolution is genuinely hard. False merges and false splits could quietly poison the graph.

**Target user**: the lab lead and advanced researchers who care about lineage, novelty framing, and onboarding into a subfield.

**What makes it survive**: this is the narrowest defensible novelty claim left after subtracting prior art. Existing tools mostly organize around documents, libraries, or queries; very few try to maintain persistent idea lineage across artifact types.

### Direction C — Project Watchtower

This version makes the lab's **active projects** the organizing unit. Instead of asking "what changed in topic X," the system asks "what changed that matters for project Y since we last looked?" Standing topics remain in the background, but the main briefing is project-scoped: new relevant work, threats to assumptions, adjacent techniques, and overlooked negatives. This direction is less about building a research encyclopedia and more about shortening the loop from external signal to internal decision.

**Biggest risk**: it depends on disciplined project-state capture. If the lab does not maintain a reasonably current view of what it is actually building, the system has nothing reliable to anchor to.

**Target user**: the operator as lab lead, plus students or researchers attached to live project threads.

**What makes it survive**: it ties the radar directly to decisions the lab already has to make, which may be the best defense against becoming another useful-but-optional reading utility.

### Direction D — Agent-Native Research Memory

This version treats the radar primarily as an **agent-accessible memory layer** exposed through MCP-style tools, with optional scheduled briefs as a secondary surface. The operator queries it through Claude Code / Codex rather than through a dedicated dashboard. The system still ingests and organizes artifacts, but the core interaction becomes: "what changed on topic T," "what are we missing on project P," "show me conflicting evidence," "trace this repo back to the papers and blog posts that matter." This direction optimizes for low UI maintenance and for fitting naturally into the operator's existing AI-assisted workflow.

**Biggest risk**: if the system is too pull-based, it may under-serve the "keep me current even when I do not ask" use case that motivated the proposal.

**Target user**: the operator specifically, especially if the day-to-day working surface is already agent-first.

**What makes it survive**: lowest interface burden, easiest to evolve incrementally, and naturally compatible with keeping X as a later adapter instead of a v1 dependency.

---

## 4. Moderator injection response

**Operator note 1: more afraid of misses than some false positives.**  
Adopted. All four directions assume a recall-first design where artifacts are ranked and labeled, not silently discarded.

**Operator note 2: 8-15 topics, with yearly churn.**  
Adopted. The system should support topic creation, active use, retirement, and archive. The search I ran on dynamic topic modelling reinforced that evolving topic labels over time are normal, not an edge case.  
Source: [dynamic topic modelling for scientific literature](https://link.springer.com/article/10.1007/s41060-024-00610-0)

**Operator note 3: X is mainly a hook for key accounts and discussions; details later.**  
Adopted. X should be a pluggable ingress adapter behind a feature flag. Official docs show workable API access, but metered pricing plus endpoint-specific limits make it a poor candidate for the critical path of v1.  
Sources: [X pricing](https://docs.x.com/x-api/getting-started/pricing), [X rate limits](https://docs.x.com/x-api/fundamentals/rate-limits)

**Operator note 4: ignore closed / paid papers.**  
Adopted. This simplifies v1 materially and keeps the problem focused on timely, public AI research signal.

---

## 5. What this round's targeted search changed

1. I am more confident that **recall-first plus ranked review** is the right posture. The systematic-review literature is not the same domain, but it is a good analogy for "missing relevant items is costly." It supports prioritization, not magical filtering.
2. I am less interested in making **X a pillar of the architecture**. The official docs show X access is possible, but it is clearly an adapter to manage, not a free ambient data source.
3. I am more convinced that **topic evolution must be explicit in the schema**. If topics drift over time, the right behavior is archive and relabel, not overwrite history.

---

## Sources consulted this round

- [Performance of active learning models for screening prioritization in systematic reviews](https://link.springer.com/article/10.1186/s13643-023-02257-7)
- [Computer-assisted screening in systematic evidence synthesis requires robust and well-evaluated stopping criteria](https://link.springer.com/article/10.1186/s13643-024-02699-7)
- [X API pricing](https://docs.x.com/x-api/getting-started/pricing)
- [X API rate limits](https://docs.x.com/x-api/fundamentals/rate-limits)
- [Dynamic topic modelling for exploring the scientific literature on coronavirus](https://link.springer.com/article/10.1007/s41060-024-00610-0)
