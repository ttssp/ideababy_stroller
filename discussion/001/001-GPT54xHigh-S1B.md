# Idea 001 · S1B · Ground (search-heavy)

**Timestamp**: 2026-04-22T10:03:09Z
**Opponent's S1A read**: yes
**Searches run**: 5, across 11 distinct sources

## 1. What the opponent's S1A gave me that I missed
- Their Part A insight I didn't see: the real wedge is delta-aware briefs against a personal knowledge base.
- Their Part B risk I didn't see: the "I'll still read it myself" cliff is real.
- Their Part C question that belongs on my list too: the data-backbone question matters, especially arXiv/OpenAlex/Semantic Scholar access and cost.

## 2. Merged question list → searches run
I took my Part C questions + opponent's Part C questions, de-duplicated them into 5 searches.

- Q: What prior art already covers discovery, mapping, alerts, and synthesis? → q: `"AI research radar tools for researchers semantic scholar elicit researchrabbit undermind arxiv sanity"` → finding: the market is crowded, but specialized. [Semantic Scholar](https://www.semanticscholar.org/product) already has search, library, alerts, and research feeds; [ResearchRabbit](https://www.researchrabbit.ai/) owns visual exploration; [Undermind](https://www.undermind.ai/) frames around deep search, novelty, and alerts; [Elicit](https://support.elicit.com/en/articles/11241729) now runs broad-source agentic literature review; [arXiv-sanity](https://github.com/karpathy/arxiv-sanity-preserver) remains a focused personalized arXiv recommender.
- Q: Is PDF/full-text extraction tractable for a solo build? → q: `"GROBID Marker Nougat scientific PDF extraction comparison"` → finding: parsing looks like engineering, not fantasy. [GROBID](https://github.com/grobidOrg/grobid) is mature; [Marker](https://github.com/cuuupid/cog-marker) positions itself as faster than Nougat with lower hallucination risk.
- Q: Can the corpus and metadata backbone be built from public infrastructure? → q: `"arXiv API OAI OpenAlex Semantic Scholar API rate limits"` → finding: yes, but the plumbing is non-trivial. arXiv documents both [public API access](https://info.arxiv.org/help/api/index.html) and [OAI-PMH harvesting](https://info.arxiv.org/help/oa/index.html). [OpenAlex](https://developers.openalex.org/guides/authentication) is generous for a free key but still quota-bound. [Semantic Scholar API](https://www.semanticscholar.org/product/api) is available and their main product already sits on a huge corpus.
- Q: Is claim extraction / contradiction detection / novelty assessment actually solved? → q: `"scientific claim verification benchmark SCITAB CliniFact SciFact"` → finding: partial progress, not a solved general capability. [SCITAB](https://aclanthology.org/2023.emnlp-main.483/) has 1.2K expert-verified scientific claims; [CliniFact](https://www.nature.com/articles/s41597-025-04417-x) has 1,970 clinical instances; [Valsci](https://link.springer.com/article/10.1186/s12859-025-06159-4) still evaluates on roughly 500 benchmark claims. That supports narrow verification, not reliable open-domain novelty/impact scoring.
- Q: Do recommenders and alerts break on trust / overload? → q: `"alert fatigue user satisfaction recommender systems literature"` → finding: yes, this concern survives contact with evidence. The scholarly-recommender survey stresses user-satisfaction evaluation, and alert-fatigue literature shows repeated low-value alerts reduce acceptance, even if that evidence comes from clinical systems rather than researcher tools ([survey](https://link.springer.com/article/10.1007/s10115-023-01901-x), [alert fatigue study](https://link.springer.com/article/10.1186/s12911-017-0430-8)).
- Q: What obvious failure cases exist? → q: `"Galactica withdrawn scientific literature demo what went wrong"` → finding: the clearest adjacent failure is an overconfident science-facing generator. Meta's Galactica demo was launched and then quickly withdrawn after backlash over authoritative nonsense, which matters for any "AI judges science for you" posture ([analysis](https://www.deeplearning.ai/the-batch/meta-released-and-quickly-withdrew-a-demo-of-its-galactica-language-model/)).

## 3. Prior art catalog
| Name | Status (live/dead/pivoted) | Relevance | URL |
|---|---|---|---|
| Semantic Scholar | live | Search, library, alerts, personalized feeds | https://www.semanticscholar.org/product |
| ResearchRabbit | live | Visual literature maps and organization | https://www.researchrabbit.ai/ |
| Elicit | live | Evidence synthesis and agentic literature review | https://support.elicit.com/en/articles/11241729 |
| Undermind | live | Deep literature search, novelty/gap framing, alerts | https://www.undermind.ai/ |
| arXiv-sanity / lite | live | Personalized arXiv filtering and recommendations | https://github.com/karpathy/arxiv-sanity-preserver |
| Galactica demo | withdrawn | Adjacent cautionary failure in science-facing AI | https://www.deeplearning.ai/the-batch/meta-released-and-quickly-withdrew-a-demo-of-its-galactica-language-model/ |

## 4. Reality vs daydream verdict
- Which Part A claims got **stronger** (evidence supports): the need is real; current tools are fragmented; parsing/metadata infrastructure is good enough to build on; researchers do adopt scoped tools for feeds, maps, alerts, and reviews.
- Which Part A claims got **weaker** (evidence against): the idea is not greenfield; several incumbents already cover large parts of the stack; "novelty/impact assessment" remains much less solved than summarization or retrieval.
- Which Part B concerns got **validated** (seen in prior failures): trust and verification are central; adjacent science-AI failures get punished fast; user experience and alert quality matter at least as much as ranking accuracy.
- Which Part B concerns got **defused** (evidence shows it's not fatal): recommenders are not rejected outright. Researchers do use assistance when it is scoped, cited, and workflow-native.
- Which remain **unknown** (search couldn't resolve — moved to S2 or moderator): exact independent retention for these products, exact 2026 AI-paper/day volume in the target subset, and whether a personal ontology can stay coherent with light-touch curation.

## 5. Graveyard lessons
- Mode 1: survivors specialize. The market keeps rewarding feeds, maps, or reviews, not one giant "research OS."
- Mode 2: trust must be inspectable. Citation traces, quotes, and narrow claims survive better than confident global judgments.
- Mode 3: alerting is easy to ship and easy to ruin. Low-precision notifications train users to ignore the system.

## 6. What's genuinely novel here
After subtracting the done, the still-interesting piece is not "AI finds papers." It is a **personal, delta-aware research memory** that tells a lab lead what changed relative to their agenda.

That novelty is real only if it stays narrow. My inference is that a lab-specific weekly delta memo or claim-checking assistant could be differentiated; a universal autonomous "novelty/impact engine" still looks overclaimed.

## 7. Updated hypothesis space
- `Personal triage feed`: source monitoring + high-precision alerts + short cited briefs. Evidence of demand: H. Differentiation: L. Feasibility: H.
- `Weekly delta memo`: KB-backed update on what changed in selected topics and which assumptions weakened. Evidence of demand: M. Differentiation: M. Feasibility: M.
- `Paper claim-checker`: user drops in a paper and gets baseline comparisons, missing evaluations, and linked prior work. Evidence of demand: H. Differentiation: M. Feasibility: M.
- `Full research cortex`: unified ontology, SOTA map, repo/blog/paper ingestion, proactive backfill, impact scoring. Evidence of demand: M. Differentiation: M. Feasibility: L.

## 8. Moderator injection response (if any)
No `discussion/001/001-moderator-notes.md` file existed at the time of writing, so there was no binding moderator injection to answer.
