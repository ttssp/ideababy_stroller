# Idea 002 · S2R1 · Opus 4.7 Max · Position (cooperative)

**Timestamp**: 2026-04-22
**Stage**: 2 (Position). Posture: cooperative, not adversarial.
**Reads**: `002-stage1-synthesis.md` (first), `PROTOCOL.md`, all S1A + S1B from
both sides, `002-moderator-notes.md` (4 operator answers, binding).
**Searches this round**: 3 targeted (recall-oriented triage pattern · topic
drift in long-running knowledge bases · X/Twitter data access in 2026).

---

## 1. What I now believe the idea actually is

After Stage 1, the idea should sharpen — and narrow — from the proposal's text
in five concrete ways. This is the version I'll carry into the direction menu:

1. **Primary entity is the *idea*, not the paper.** I conceded this to GPT in
   S1B §1 and the synthesis §3 flagged it as the single biggest cross-debater
   update. An "idea" here is an addressable thing with provenance across
   artifacts (paper → repo → blog → discourse). Papers and repos become
   *manifestations* of ideas, not the unit of storage.
2. **Scope is the operator's lab, not a product category.** The synthesis §8
   is right that this is a "personal-tool-with-publishable-internals," not a
   unicorn. Framing as a SaaS for labs would collide head-on with Iris.ai
   ($8.3M) and Semantic Scholar Research Feeds (free, adaptive, shipped). As
   a lab-internal system, the competitive picture changes entirely.
3. **Output is auditable verdicts + provenance, not novelty scores.** Four
   benchmarks (NovBench, GraphMind, Literature-Grounded Novelty, DeepReview)
   agreed: LLM novelty scoring is adversarially fragile today. A surviving
   product can expose assistive signals + full citation trail; it cannot
   expose a "novelty: 0.87" number as a primary rank.
4. **Recall-biased, not precision-biased.** This is the operator's explicit
   answer (moderator-notes item 1: "更怕漏报, 可以接受小部分误报"). It flips the
   system design: the default is "show everything ranked, flag the high-noise
   tail" not "filter aggressively and show the top N." Systematic-review
   tooling (Covidence, EPPI-Reviewer) is the precedent — broad capture, ML
   ranking, human final-call. See
   [AI tools for literature review 2025 overview](https://richlyai.com/ai-tools/ai-tools-for-literature-review/)
   and [Artificial intelligence for literature reviews (Springer 2024)](https://link.springer.com/article/10.1007/s10462-024-10902-3).
5. **Open-access only, no paywalled content.** Operator answer 4: AI-domain
   closed/paid papers are "太时效性太差" and not worth pursuing. This closes
   the recall-hole question (§11.7 of the synthesis) cleanly and removes
   the IEEE/ACM ingestion scope.

What drops out of the proposal text as a result:
- "taste-learning from X + dialectical" as a core feature — demoted to a
  future **hook**, not a v1 feature (see §3 menu and operator answer 3).
- "Real-time SOTA leaderboard auto-update" — demoted to a view over
  auditable topic state, not a primary output.
- "Senior-colleague brief" framing — kept as **one** output surface option,
  not the only one.

---

## 2. Honest Y/N on "should this be built"

**Y, conditionally.** The conditions are all things Stage 1 surfaced:

- Build the lab-internal version only. Do not position this as a product
  that competes with Semantic Scholar Research Feeds or Iris.ai. The
  standing novelty is narrow; widen-to-product dilutes it fast.
- Anchor novelty on **idea-migration provenance + in-progress-project
  integration**, not on "personalized daily paper feed" (Semantic Scholar
  already ships that).
- Accept the 6–12 month timeline budget but **gate each phase** on the
  output actually changing the operator's behavior — Pattern A (useful-but-
  niche plateau) is the 10-year failure mode for this category.
- Default to local-first. Paywalled is out by operator decision. Any
  blog-scraping that extends beyond conservative ToS/robots.txt needs an
  explicit decision, not a default.

Conditions under which I'd say N: if the operator's actual current reading
workflow turns out to already be served well by Semantic Scholar Research
Feeds + Zotero + papersgpt-for-zotero + occasional Elicit runs, then the
incremental value of building this is smaller than the synthesis suggested.
This is a moderator question worth asking (§6).

---

## 3. Candidate directions (4 peers, NOT picked)

Stage 1 converged on five hypotheses but two (`weekly-briefing-cron` and
`radar-as-MCP`) are *output-surface choices* rather than product directions;
`adversarial-taste-pair` is a feature that composes onto any direction. I'm
reshaping the menu so each entry is a *direction-of-the-whole-system*, with
a default output surface and a default serendipity-valve choice baked in.

### Direction A — **Idea-Migration Radar**
**One-paragraph description.** The system's unit is an *idea* that migrates
across paper → repo → blog → discourse. The lab has 8–15 topic pages; each
topic page is a living DAG of ideas, each idea has its own provenance chain
across artifact types. New artifacts arrive, get matched to existing ideas
(or create a new idea node), and the topic page gets regenerated daily.
Output surface: weekly briefing (markdown → Obsidian-compatible) + on-demand
MCP queries for "what's moving on topic X?".

- **Biggest risk**: entity resolution across artifact types is genuinely
  hard engineering — "is this repo the implementation of that paper's
  method?" is a cross-modal semantic-match problem with no turn-key library.
  Budget risk is real; synthesis §9 rated F (feasibility) = M, not H.
- **Target user**: the lab lead *and* senior researchers in the lab. The
  idea-centric view is specifically useful when onboarding a new researcher
  to a topic, which supports the synthesis's "lab memory" vision (though
  not in year 1).
- **What makes it survive where prior attempts failed**: nobody in the
  prior-art catalog (§5 of synthesis) tracks idea-migration. arxiv-sanity,
  papersgpt-for-zotero, Semantic Scholar Research Feeds are all
  paper-centric. This is the defendable novelty claim from §8.
- **Serendipity-valve default**: cross-topic forcing-function — once/week,
  the system picks one artifact from a *different* lab's topic adjacent to
  one of ours and surfaces it as "you don't track this but here's a
  possible bridge." Mitigates filter-bubble (§Pattern F).
- **Recall-biased output shape**: every matched artifact shows up in the
  topic DAG with a confidence flag; low-confidence matches are *not hidden*,
  they're labeled "tentative — you decide."

### Direction B — **Weekly Briefing Service + Read-Through Inbox**
**One-paragraph description.** The system's primary output is a **weekly**
(not daily) briefing per standing topic, delivered as markdown files into
Obsidian. Underneath, the system maintains a "read-through inbox" — every
ingested artifact is classified to a topic, tagged with an LLM verdict +
confidence, and made queryable. The briefing is the daily-visible surface;
the inbox is the recall-safety-net the operator can scan when they suspect
something was missed. Primary entity is *papers/artifacts*, secondary
entity is topics.

- **Biggest risk**: this is competitively close to what
  papersgpt-for-zotero + Semantic Scholar Research Feeds + a cron job can
  already approximate. Defensibility rests on the **lab-project-aware**
  layer — does the briefing know what the lab is currently building? If
  yes, it's differentiated; if not, it's a re-skin of existing tools.
- **Target user**: the operator first, senior researchers second.
- **What makes it survive where prior attempts failed**: weekly cadence
  (not daily) matches how humans actually consume synthesis (operator's
  own reading discipline, also echoed in GPT's S1A "Monday morning does
  not begin with forty tabs"); and the read-through inbox defuses Pattern
  A's "daily-use poor" trap — the tool remains useful even on days the
  operator skips the briefing.
- **Serendipity-valve default**: the briefing always includes a "possibly-
  overhyped" and a "possibly-underrated" section, both LLM-flagged with
  citations, each containing at least one item.
- **Recall-biased output shape**: the inbox IS the recall guarantee —
  nothing gets dropped, just ranked; the briefing is explicit about "from
  142 artifacts this week, these 7 moved topic X."

### Direction C — **Radar-as-MCP** (tool, not surface)
**One-paragraph description.** The system ships as an MCP server that
Claude Code, Cursor, and Codex can call. No new UI, no briefing cron. The
lab's topic graph, prior-art database, and "what's new this week" queries
are all exposed as MCP tools. The operator lives in Claude Code already
(directly relevant to the lab's build tooling) and gets the radar as a
natural extension of that surface. A nightly ingestion daemon maintains the
store; queries happen on demand.

- **Biggest risk**: it's *too* low-surface — if the operator doesn't ask
  the agent about research topics often enough, the system sees no usage,
  and cold-start value is zero. GPT's "if you cannot win with a narrow
  weekly workflow that a real researcher would miss when it is gone" test
  is actually harder to pass when there's no proactive surface.
- **Target user**: the operator specifically, because his daily surface is
  already Claude Code (constraint stated in proposal).
- **What makes it survive where prior attempts failed**: lowest UI
  maintenance load; directly mitigates Pattern D (manual-pipeline decay)
  because there's almost nothing to maintain in the UX layer. Solo-operator
  friendly.
- **Serendipity-valve default**: a `research.what_am_i_missing(topic)`
  tool that explicitly returns the **adversarial-taste-pair**'s output —
  "here's what the default ranker would have hidden."
- **Recall-biased output shape**: no filtering — the tool returns full
  ranked lists; the operator (or Claude) does the final selection in-chat.

### Direction D — **Project-Linked Radar** (new — composed reading of S1 evidence)
**One-paragraph description.** The system treats the *lab's in-progress
projects* as the organizing unit rather than the 8–15 standing topics.
Each active project has a live "related work since you started" page that
updates as the project proceeds. Standing topics exist as background
context; the *active* surface is always "what changed in the literature
relevant to what you're currently building?" The briefing is
project-scoped, not topic-scoped.

- **Biggest risk**: projects come and go faster than topics; the operator
  doesn't have a written-down list of active projects either. Bootstrap
  requires the operator to say "we're working on X, Y, Z this quarter" —
  that's friction on the operator that the topic version doesn't have.
- **Target user**: the lab lead for project-level decisions; students/
  researchers for "what came out this week relevant to my thesis."
- **What makes it survive where prior attempts failed**: this is the piece
  nothing in the prior-art catalog does at all. Semantic Scholar Research
  Feeds trains off your library folders; Elicit/Consensus serve a query;
  none integrate with "what is this lab actively building?" The synthesis
  §8 standing-ground explicitly called out "ties to lab's active in-
  progress projects" and this direction makes that primary.
- **Serendipity-valve default**: "adjacent-project" feed — surfaces
  literature one step away from the active project, including negative
  results that would argue against continuing.
- **Recall-biased output shape**: project-scoped recall guarantee — every
  artifact plausibly relevant to project P must be visible in P's feed
  even if ranked low.

---

## 4. Direction I lean toward — and why (honest, not neutral)

I lean **B (Weekly Briefing + Read-Through Inbox)**, with **A's
idea-migration provenance as a v1.5 upgrade** and **C (MCP tool surface)
added alongside from day one for the operator's Claude-Code workflow**.

Honest reasoning, numbered:
1. **B has the clearest "operator changes behavior" test.** The weekly
   briefing is a falsifiable product — if after 6 weeks the operator isn't
   opening it Monday morning, it doesn't work and we know quickly. A and D
   are structurally harder to test this way because their value compounds.
2. **B is the right recall-biased shape.** The inbox-under-the-briefing is
   the most honest recall architecture: nothing is dropped, the briefing
   is opinionated but the ground truth is always visible. This maps
   directly onto the operator's stated preference (recall > precision)
   without needing to tune filter thresholds delicately.
3. **A is more differentiated but has 2x the engineering risk.** Entity
   resolution across artifact types (paper ↔ repo ↔ blog) is genuinely
   unsolved for AI-research specifically; it's a research problem as much
   as an engineering one. If I were writing a paper, A would be the better
   choice. For 6–12 months of solo-operator-team build, B is more likely to
   reach the end state.
4. **C bolts onto B cheaply.** If we build B and its storage/topic layer
   as first-class, exposing them as MCP tools is straightforward. We get
   both the "pull" daily surface (MCP via Claude Code) and the "push"
   weekly surface (briefing file into Obsidian) with one underlying store.
   That's the "they're not mutually exclusive" note the synthesis §9 made.
5. **D is compelling but depends on operator project discipline I can't
   verify.** If the operator already maintains a list of active projects
   with "what are we trying to learn," D is a great lead. If not, the
   bootstrap cost pushes it to v2. This is a moderator question (§6).
6. **A's idea-migration graph is still the right north star for year 2.**
   Starting with B's artifact-centric store but designing the schema so
   *ideas* can be promoted to first-class entities later is the
   compromise. Direction B can evolve into Direction A; the reverse is
   harder.

I am not picking — per protocol, this is my lean, the moderator's direction
decision happens at stage2-checkpoint.

---

## 5. Deltas since S1B

- **Hypothesis-space structure revised.** My S1B §7 treated five hypotheses
  as peers, but two of them (`weekly-briefing-cron`, `radar-as-MCP`) were
  surface choices, not directions. The Stage 2 menu is more honest as four
  *directions* with output-surface defaults baked in.
- **"Full chief-of-staff vision" (H5) dropped from the active menu.**
  Synthesis §9 already flagged it as "don't do this yet"; the operator's
  timeline (6–12 months solo) makes it infeasible. Kept as year-3 aspiration
  in D's direction description, not as a standalone option.
- **Adversarial-taste-pair demoted from hypothesis to feature.** It
  composes into every direction as a serendipity-valve default. Putting it
  on the direction menu as a peer was a category error — confirmed by
  synthesis §9 cross-cutting note.
- **New direction (D, Project-Linked Radar) introduced.** This isn't
  strictly new content — synthesis §8 already identified "ties to the
  lab's own active projects" as part of the standing novelty. But S1B's
  hypothesis list didn't surface a direction organized *primarily* around
  this. It deserves to be on the menu because it's the one wedge with no
  prior art at all.
- **Confirmed: X/Twitter as a data source is a v2 hook, not v1.** The
  operator's answer ("留个口子, 后面再具体确定方案") aligns with what search
  confirmed: X's API posture in 2026 is hostile — free tier is write-only;
  paid is $0.00015/call via third parties like xpoz, Apify, or scrapfly;
  the 2023 API apocalypse persists. See
  [Every Way to Access Twitter/X Data in 2026](https://www.xpoz.ai/blog/comparisons/twitter-x-data-access-options-compared-2026/)
  and [Scraping Twitter in 2025 developer guide](https://dev.to/sivarampg/scraping-twitter-in-2025-a-developers-guide-to-surviving-the-api-apocalypse-5bbd).
  All four directions should architect X ingestion as a pluggable adapter
  behind a feature flag, and leave it off in v1.
- **Confirmed: topic drift is a solvable sub-problem.** Operator's answer
  2 (8–15 topics churn: +3 new, −2 dropped per year, rolling) is within
  the scope of the dynamic-topic-model literature (Dynamic Topic Model,
  Dynamic Embedded Topic Model, BERTopic for yearly evolution). See
  [Dynamic topic modelling literature 2024](https://link.springer.com/article/10.1007/s41060-024-00610-0)
  and [The Evolution of Topic Modeling — ACM 2022](https://dl.acm.org/doi/10.1145/3507900).
  I don't think we need to *run* dynamic topic models; the operator
  manages the topic list by hand. But we need a schema that permits topic
  retirement without losing prior topic state (for lab memory). Archive,
  don't delete.

---

## 6. Moderator injection response (if any)

Moderator notes item 1 (recall > precision) — **adopted** as first-class
constraint. All four directions now have recall-biased output shape
defaults; the filter threshold is never the knob that hides artifacts
from view.

Moderator notes item 2 (8–15 topics, yearly churn ±2–3) — **adopted**.
The schema for all directions must support topic lifecycle: create,
active, archived. Archived topics retain their artifacts + prior
verdicts; they're just not surfaced in daily/weekly outputs.

Moderator notes item 3 (X hook only, not v1) — **adopted**. X is a
pluggable adapter in all directions, off by default. If we pick a
direction that needs "what are top researchers saying today," we revisit;
for v1, repos + blogs + arxiv + OpenReview carry the signal.

Moderator notes item 4 (no paywalled content) — **adopted**. Removes
IEEE/ACM/bioRxiv-with-login from scope. The ingestion spine is
arxiv + OpenAlex + Semantic Scholar + OpenReview + selected public
blogs + GitHub. This is a simplification — one less compliance surface.

### Open questions for the moderator (help sharpen S2R2 / direction pick)

Q-M1. **Does a written list of 8–15 topics already exist?** Synthesis
§11.4 flagged this. If the operator can share the current draft list, it
materially changes whether Direction A (idea-migration over fixed topics)
is feasible on day 1, or whether we should start with Direction B's more
flexible "topic-as-tag" model. If no list exists yet, the early system
should help *build* the list, not assume it.

Q-M2. **Does a written list of active projects exist?** Synthesis §11
didn't ask this because D didn't exist yet. If projects are tracked (even
lightly), Direction D goes from "bootstrap-friction-heavy" to "cheap start
from existing data." If not, D shifts to v2.

Q-M3. **What's the operator's current reading workflow on a Monday
morning?** Synthesis §11.1 flagged this as the single question most
worth asking before Stage 2 converges. A short free-form description from
the operator — what apps, what cadence, what he starts with — is the
cheapest piece of evidence I can use to choose between briefing-first
(Direction B) and MCP-first (Direction C).

Q-M4. **Does the operator have specific in-lab pain right now where the
wrong paper got missed, or where a student re-derived something the lab
already knew?** If yes, those concrete incidents are the best seed for
idea-migration provenance (Direction A) — they're the first ground-truth
test cases. If no specific incidents, A's value proposition stays
abstract and I'd lean harder on B.

Q-M5. **Feature flag for "Direction A schema day 1 even under
Direction B"?** I'm proposing B as v1 with an idea-entity-capable schema
from the start, so we can promote artifacts to idea-nodes later without
a migration. This is a small v1 cost; I want to confirm it's worth it, or
whether the moderator wants a simpler v1 that closes off A permanently.

---

### One-line summary

**S2R1: 4 peer directions — A Idea-Migration / B Briefing+Inbox /
C Radar-as-MCP / D Project-Linked; I lean B with A's schema baked in and
C exposed alongside; all four architected recall-biased with
adversarial-taste-pair as serendipity default; X demoted to v2 adapter;
no paywalled; 5 open questions for the moderator before direction pick.**

---

**Sources consulted this round** (3 targeted searches):
- [AI tools for literature review 2025 — richlyai.com](https://richlyai.com/ai-tools/ai-tools-for-literature-review/)
- [Artificial intelligence for literature reviews — Springer 2024](https://link.springer.com/article/10.1007/s10462-024-10902-3)
- [Dynamic topic modelling for scientific literature — Springer 2024](https://link.springer.com/article/10.1007/s41060-024-00610-0)
- [The Evolution of Topic Modeling — ACM Computing Surveys 2022](https://dl.acm.org/doi/10.1145/3507900)
- [Every Way to Access Twitter/X Data in 2026 — xpoz.ai](https://www.xpoz.ai/blog/comparisons/twitter-x-data-access-options-compared-2026/)
- [Scraping Twitter in 2025 developer guide — dev.to](https://dev.to/sivarampg/scraping-twitter-in-2025-a-developers-guide-to-surviving-the-api-apocalypse-5bbd)
