# Idea 002 · S1B · GPT54xHigh · Ground (search-heavy)

**Timestamp**: 2026-04-22T22:37:01+0800
**Opponent's S1A read**: yes
**Searches run**: 29, across 12 distinct sources

## 1. What the opponent's S1A gave me that I missed
- Their Part A insight I didn't see: the best first UX may be a concise morning briefing, not a giant dashboard.
- Their Part B risk I didn't see: if the system filters too aggressively, the lab's taste can atrophy instead of compound.
- Their Part C question that belongs on my list too: permissions and data rails matter almost as much as ranking quality, because this product depends on dependable ingestion.

## 2. Merged question list → searches run
- Q: Is the overload premise real? → q: `"site:info.arxiv.org annual report 2023 submissions arXiv"` → arXiv reported 208,493 new submissions in 2023, about 571/day overall, so the firehose premise is real even before adding blogs and repos. https://info.arxiv.org/about/reports/2023_arXiv_annual_report.pdf
- Q: Does the substrate already exist? → q: `"Semantic Scholar API overview"`, `"OpenAlex rate limits and authentication"`, `"OpenReview API docs"` → yes. All three expose maintained APIs, and OpenAlex even offers cached PDFs/TEI XML. Ingestion is feasible, so raw collection is not the moat. https://www.semanticscholar.org/product/api ; https://docs.openalex.org/how-to-use-the-api/rate-limits-and-authentication ; https://docs.openreview.net/getting-started/using-the-api
- Q: Do personalized paper feeds already exist? → q: `"Semantic Scholar research feeds official"` → yes. Semantic Scholar already ships adaptive daily Research Feeds trained from library folders and relevance feedback. Generic paper alerts are not novel. https://www.semanticscholar.org/faq/what-are-research-feeds
- Q: Is open-source paper-reading tooling mature? → q: `"PaperQA2 GitHub"`, `"papersgpt-for-zotero GitHub"` → yes for private-library QA, summarization, and agentic reading. The harder gap is frontier surveillance across sources over time. https://github.com/Future-House/paper-qa ; https://github.com/papersgpt/papersgpt-for-zotero
- Q: Can novelty/impact be scored reliably today? → q: `"automated novelty assessment scientific papers reliability"` → progress exists, but recent work still treats LLMs as assistive or section-sensitive, not trustworthy autonomous judges. That supports advisory scoring, not unattended ranking. https://www.sciencedirect.com/science/article/abs/pii/S0957417425004002 ; https://doi.org/10.1002/asi.70005
- Q: What prior failures or plateaus are obvious? → q: `"Microsoft Academic next steps"`, `"arxiv-sanity-preserver GitHub"`, `"Galactica demo removed"` → clear warnings exist. Microsoft Academic vanished; arXiv Sanity remained useful but operatorish; Galactica showed how fast science-facing AI fails when fluency outruns grounding. https://www.microsoft.com/en-us/research/project/academic/articles/microsoft-academic-to-expand-horizons-with-community-driven-approach/ ; https://github.com/karpathy/arxiv-sanity-preserver ; https://www.deeplearning.ai/the-batch/meta-released-and-quickly-withdrew-a-demo-of-its-galactica-language-model/
- Q: Do existing tools already help in a narrower workflow? → q: `"Elicit systematic literature reviews"`, `"Using artificial intelligence for systematic review: the example of elicit"` → yes, mainly for structured evidence synthesis. That validates bounded research automation, not reliable frontier judgment. https://elicit.com/solutions/literature-review ; https://bmcmedresmethodol.biomedcentral.com/articles/10.1186/s12874-025-02528-y

## 3. Prior art catalog
| Name | Status (live/dead/pivoted) | Relevance | URL |
|---|---|---|---|
| Semantic Scholar Research Feeds | Live | Personalized daily paper recommendations already exist | https://www.semanticscholar.org/faq/what-are-research-feeds |
| Elicit | Live | Strong literature-review and evidence-synthesis workflow | https://elicit.com/solutions/literature-review |
| arXiv Sanity Preserver | Live / longstanding niche | Closest old-school "tame the firehose" prior art | https://github.com/karpathy/arxiv-sanity-preserver |
| PapersGPT for Zotero | Live | Agentic reading and summarization inside a private library | https://github.com/papersgpt/papersgpt-for-zotero |
| PaperQA2 | Live | Grounded QA/summarization over paper collections | https://github.com/Future-House/paper-qa |
| Microsoft Academic | Dead | Important reminder that upstream scholarly infrastructure can vanish | https://www.microsoft.com/en-us/research/project/academic/articles/microsoft-academic-to-expand-horizons-with-community-driven-approach/ |

## 4. Reality vs daydream verdict
- Which Part A claims got **stronger**: the overload premise; the feasibility of building on existing APIs; the plausibility of a bounded internal tool for 8-15 topics.
- Which Part A claims got **weaker**: automatic scoring of novelty/impact/practicality as something a strong human would trust unattended; the full "chief of staff" vision as a first release.
- Which Part B concerns got **validated**: trust is the bottleneck, not retrieval; prior tools often remain utilities rather than becoming a user's whole research surface; maintenance of scholarly data plumbing is a real product risk.
- Which Part B concerns got **defused**: mass-market adoption friction is less fatal here because the operator only needs to satisfy one lab, not the whole market.
- Which remain **unknown**: daily briefing versus weekly cadence; whether papers, repos, blogs, or public discussion surface the earliest useful signal for these specific topics; how much adversarial review is needed before the system earns real trust.

## 5. Graveyard lessons
- Mode 1: upstream dependency risk. Microsoft Academic's retirement shows why depending on a single external scholarly spine is dangerous.
- Mode 2: useful-but-niche plateau. arXiv Sanity shows enduring demand, but I infer from its manual update pipeline and long-lived repo shape that "good enough for me" does not automatically become "default workflow for labs."
- Mode 3: authoritative nonsense. Galactica is the obvious failure case for science-facing AI that sounds plausible before it is trustworthy.

## 6. What's genuinely novel here
After subtracting what already exists, the defendable novelty is not "AI summarizes papers." It is a lab-specific radar that:
- fuses papers, repos, blogs, and public discussion,
- remembers 8-15 long-running topics over time,
- emits an opinionated but auditable briefing tied to the lab's actual work.

If the output is not traceable to sources and prior topic state, the novelty mostly collapses into "yet another feed."

## 7. Updated hypothesis space
- `Weekly Briefing First` — Evidence of demand: `H` ; Differentiation: `M` ; Feasibility for a solo operator with AI team: `H`.
- `Radar-as-Notebook Backbone` — Evidence of demand: `M` ; Differentiation: `M` ; Feasibility for a solo operator with AI team: `H`.
- `Idea Graph for 8-15 Topics` — Evidence of demand: `M` ; Differentiation: `H` ; Feasibility for a solo operator with AI team: `M`.
- `Autonomous Research Chief of Staff` — Evidence of demand: `L` ; Differentiation: `H` ; Feasibility for a solo operator with AI team: `L`.

My update after search: the first credible wedge is a narrow briefing workflow with audit trails, not the grand unified radar.

## 8. Moderator injection response (if any)
No `discussion/002/002-moderator-notes.md` exists, so there is no binding moderator injection to answer in this round.
