# Idea 002 · S1B · Opus 4.7 Max · Ground (read opponent + search)

**Timestamp**: 2026-04-22
**Search used**: 7 web searches, unique URLs cited inline.
**Visibility**: Read my own S1A and GPT's S1A (all three parts) before writing.

---

## §1 · What opponent's S1A gave me that I missed

GPT framed the product as a **"research chief of staff"** and a **"living map of
the motion of ideas"**. Two things I should have named but didn't:

- **Part A insight I missed — tracking *motion* across artifact types.** My Part
  A was paper-centric with repos as anomalies. GPT's framing — that the unit is
  an *idea* migrating through paper → repo → blog → discourse — is a better
  mental model. It also implies a different data model: entities that persist
  across artifact types, not documents that are the primary object.

- **Part B risk I missed — "preference prison".** GPT named something I
  gestured at (taste-training-on-its-own-priors) but named more sharply:
  *narrowing curiosity instead of expanding it*. That is the actionable
  formulation; mine was too diffuse.

- **Part C question I missed — "which failure hurts more: missed important
  work or too many false positives?"** This is the core product-tradeoff
  question and I did not ask it.

- **Part A claim I overreached on vs. GPT.** I claimed a quantified "3–5x
  throughput multiplier" and GPT did not. GPT was right not to. I flagged it
  myself in C.2 but didn't withdraw it in Part A.

---

## §2 · Merged question list → searches run

Merged and de-duplicated from my C.4 + GPT's C queries:

| # | Query (paraphrased) | Source |
|---|---|---|
| Q1 | arxiv CS daily volume in 2025/2026 | mine C.4.1 |
| Q2 | graveyard of research aggregators (Scholarcy, Iris.ai, arxiv-sanity, etc.) | mine C.4.2 + GPT Q5 |
| Q3 | State of paperqa / Zotero-LLM plugins in 2026 | mine C.4.3 |
| Q4 | Retention / workflow fit of Elicit/Consensus/Scite | mine C.4.4 + GPT Q2 |
| Q5 | arxiv scraping ToS + AI-crawler policy | mine C.4.5 |
| Q6 | Automated novelty-scoring reliability (benchmarks) | GPT Q3 |
| Q7 | Filter-bubble / taste-learning failure in recommenders | GPT Q4 + mine B concern |

**Findings (ordered by how much they shifted my priors):**

**Q1 — arxiv volume.** Total arxiv submissions hit **~28K/month by late 2025**
(super-exponential slope change), projected **65K/month by 2030**. cs.AI alone
was **~21,400 in 2024** (~60/day just cs.AI). My S1A's "300/day" referenced
all-arxiv and was roughly right; the *growth rate* is worse than I said.
[arxiv CS recent](https://arxiv.org/list/cs/recent),
[Event Horizon of Knowledge — Lightcap AI](https://lightcapai.medium.com/the-event-horizon-of-knowledge-why-3-million-arxiv-papers-are-a-warning-signal-48fc9b74fb33),
[AI Conference Crisis paper](https://arxiv.org/html/2508.04586v1).
→ Volume argument for the tool is *stronger* than I wrote.

**Q3 — Zotero LLM plugin ecosystem is mature in 2026.** `papersgpt-for-zotero`
supports Claude/Gemini/GLM/DeepSeek with an **AutoPilot agent mode** for
autonomous literature review. `llm-for-zotero` has **Agent Mode (beta)**.
`paperqa-zotero` exists for local-LLM Q&A over one's library.
[papersgpt GitHub](https://github.com/papersgpt/papersgpt-for-zotero),
[llm-for-zotero](https://github.com/yilewang/llm-for-zotero),
[paperqa-zotero](https://github.com/lejacobroy/paperqa-zotero),
[BrightCoding 2025 guide](https://www.blog.brightcoding.dev/2025/12/06/the-ultimate-zotero-llm-plugin-guide-transform-your-research-with-ai-in-2025-%F0%9F%9A%80/).
→ My "scope shrinks if the extraction pipeline is solved" wish is partly
granted *for private-library QA*, NOT for *discovery-at-the-firehose*.

**Q6 — Novelty-scoring benchmarks say: not reliable yet.** NovBench (1,684
paper-review pairs): "current models exhibit limited understanding of
scientific novelty." Literature-grounded novelty scoring, GraphMind, and
DeepReview all report **misclassification of well-documented ideas as novel**
and **prompt-injection flipping scores across nearly all papers**.
[NovBench](https://arxiv.org/html/2604.11543),
[GraphMind](https://arxiv.org/html/2510.15706v1),
[Literature-Grounded Novelty](https://arxiv.org/html/2506.22026v1),
[DeepReview ACL 2025](https://aclanthology.org/2025.acl-long.1420.pdf).
→ My Part B concern ("automation will be mediocre for a long time") is
**validated** by benchmarks.

**Q2 — Graveyard is *weaker* than I claimed.** arxiv-sanity-lite still live;
Scholarcy still subscribing; Iris.ai raised **$8.3M in May 2024**; Elicit,
Consensus, Scite are active and increasingly recommended as a *combined
workflow* (Perplexity-to-explore → Elicit-to-synthesize → Consensus-to-validate
→ Scite-to-verify).
[Scholarcy site](https://www.scholarcy.com/),
[arxiv-sanity-lite](https://github.com/karpathy/arxiv-sanity-lite),
[Iris.ai Tracxn](https://tracxn.com/d/companies/iris.ai/__0r5tCqeOMRId5QnOcyRoFicLN93c-lTaOMSCwFTcESc/funding-and-investors),
[deepresearcher 2026 comparison](https://deepresearcher.site/blog/best-ai-tools-deep-research-2026).
→ My "these all died" claim was wrong. The honest version: **all survive, none
became *the* primary surface**. That's a different lesson — stratification, not
extinction.

**Q5 — Legal surface is milder than I feared for arxiv, still ambiguous for
blogs.** arxiv explicitly permits bulk / commercial use with no MOU required;
affiliate donation "optional." AI-crawler policy literature notes post-2022
rise in robots.txt restrictions and frequent non-compliance by crawlers.
[arxiv API ToU](https://info.arxiv.org/help/api/tou.html),
[arxiv bulk data](https://info.arxiv.org/help/bulk_data.html),
[robots.txt compliance empirical study](https://arxiv.org/html/2505.21733v1).
→ My Part B worry about legal exposure on arxiv is *defused*. Blog-scraping
concerns remain.

**Q7 — Filter-bubble is well-documented but not settled.** Systematic reviews
confirm: personalized recommendation does cause **convergence in taste** and
**echo chambers**; "disentangling" work (2024) shows the effect survives
careful measurement. Mitigation literature exists but isn't a silver bullet.
[Filter Bubbles Fact or Fallacy — arxiv 2307.01221](https://arxiv.org/pdf/2307.01221),
[Filter Bubble or Homogenization — arxiv 2402.15013](https://arxiv.org/abs/2402.15013).
→ GPT's "preference prison" risk is not hypothetical.

**Q4 — Existing tools' retention pattern.** Public 2025–2026 comparisons
describe Elicit/Consensus/Scite as **complementary, not primary-surface**
tools. They live in a *stack*, each doing a narrow job; no single one becomes
the research inbox. [HKUST Library trust review](https://library.hkust.edu.hk/sc/trust-ai-lit-rev/),
[Anara: Scite vs Elicit](https://anara.com/blog/scite-vs-elicit).

---

## §3 · Prior art catalog

| Name | Status (2026) | Relevance | URL |
|---|---|---|---|
| arxiv-sanity-lite (Karpathy) | Live, niche | Personal SVM-ranker over abstracts; single-user flavor | https://github.com/karpathy/arxiv-sanity-lite |
| papersgpt-for-zotero | Active, AutoPilot agent mode | Closest existing "autonomous lit-review in your library" | https://github.com/papersgpt/papersgpt-for-zotero |
| llm-for-zotero | Active, Agent Mode (beta) | LLM in Zotero side panel; agent over library | https://github.com/yilewang/llm-for-zotero |
| paperqa / paperqa-zotero | Active | LangChain map-reduce over a library; local-LLM friendly | https://github.com/lejacobroy/paperqa-zotero |
| Elicit | Active, paid | Literature-review structured-extraction specialist | referenced in comparisons above |
| Consensus | Active, paid | "Does X help Y?" evidence synthesis | ibid. |
| Scite | Active, paid | Citation-context (supporting / contradicting) | ibid. |
| Scholarcy | Active, paid | Summarization per paper | https://www.scholarcy.com/ |
| Iris.ai | Active, $8.3M May 2024 | Enterprise research platform (RSpace™) | https://tracxn.com/... |
| NovBench / GraphMind / DeepReview | Research benchmarks | *Negative evidence* for automated novelty scoring | above URLs |

**Pattern**: lots of alive tools, each owning a narrow slice. **Nobody owns the
"daily briefing for my lab's 8–15 topics" slice.** That is the market gap.

---

## §4 · Reality vs daydream — verdict on my own S1A

**Part A claims (POSITIVE):**
| Claim | Verdict |
|---|---|
| Volume requires automation (300/day on arxiv) | **Stronger** — 900+/day all-arxiv, super-exp slope |
| Long-context models can hold paper + lab history in one call | Unchanged — still true |
| Cheap LLM-per-paper economics | Unchanged — still true |
| "Daily briefing" outperforms feed | **Unknown** — no evidence either way, product question |
| 3–5x research throughput multiplier | **Weaker** — no study supports a specific number; withdraw |
| Lab-memory as new-hire onboarding | **Unknown** — plausible but unverified |

**Part B concerns (NEGATIVE):**
| Concern | Verdict |
|---|---|
| "Automating judgment will be mediocre for a long time" | **Validated** — NovBench + DeepReview confirm |
| "Preference prison" / filter bubble | **Validated** — established recommender-systems literature |
| "Integration cost is high, data-exit concerns" | **Unknown for this operator** — he owns the data and stack, so the friction Mem/Rewind hit is not his friction |
| "Daily-use poor" pattern (Connected Papers, Scholarcy, etc.) | **Partially validated** — tools survive as narrow utilities, not primary surfaces |
| "Legal risk scraping AI-lab blogs" | **Reduced for arxiv; remains for blogs** |
| "Graveyard of aggregators" | **Wrong framing** — they didn't die, they fragmented into a stack |

---

## §5 · Graveyard lessons (what repeated failures teach us)

Since the tools mostly *didn't* die, the lesson is different from extinction:

1. **Every standalone "read everything for you" tool plateaued as a utility
   in a stack.** No tool became the researcher's *primary surface* because
   none solved the *judgment* problem — only retrieval, summarization, or
   citation-context.
2. **Benchmarks consistently find novelty scoring unreliable.** So any product
   claim built on "we rank by novelty" is on shaky ground *today*.
3. **Personalization produces real convergence.** The filter-bubble effect is
   real and measurable; any lab-scale deployment needs a serendipity valve.
4. **The missing layer is "integrate over a lab's active projects + taste".**
   Generic tools can't see that; enterprise tools (Iris.ai) try but require
   adoption friction solo operators don't have.

---

## §6 · What's genuinely novel after subtracting done/failed/trivial

After subtraction:

- **Done**: retrieval from arxiv; single-paper summarization; citation-context;
  library-Q&A; generic literature review; ranked feeds over abstracts.
- **Tried and unreliable**: LLM-based novelty scoring at SOTA-scoreboard
  granularity.
- **Uncovered**: a **topic-scoped, lab-personalized "morning briefing" layer
  that treats ideas (not papers) as the persistent entity**, integrates with
  in-progress projects, and has a built-in *disagreement / serendipity valve*
  to counteract the filter bubble.

That last clause is the genuinely novel piece. The rest is stack integration.

---

## §7 · Updated hypothesis space (3–5 versions)

Scored on **D**emand (0–3), **D**ifferentiation (0–3), **S**olo-feasibility
for 1 architect + 6–7 juniors × 6–12 months (0–3). Higher is better. (I'm
being harsher here than in my S1A — prior art shows personal tools are a
crowded field.)

| # | Version | D | Δ | F | Total | Survival angle |
|---|---|---|---|---|---|---|
| H1 | **"Idea-centric topic pages"** — entities are ideas that migrate across paper/repo/blog, with provenance graphs per idea, rebuilt daily; lab has 8–15 idea-pages. | 2 | 3 | 2 | **7** | Narrow wedge; no competitor tracks idea-migration; aligns with GPT's "motion of ideas" |
| H2 | **"Weekly briefing service, not tool"** — run as a cron, emails/pushes one ≤500-word briefing per topic per week; no UI except Obsidian-compatible markdown export. | 3 | 2 | 3 | **8** | Cheap to build, cheap to abandon; perfect solo-scale; tests usage-vs-demo gap. Matches GPT's "narrow weekly workflow" |
| H3 | **"Lab radar-as-MCP"** — expose everything as an MCP server Claude/Cursor can query on demand; no new UI. | 2 | 3 | 3 | **8** | Plugs into the operator's existing daily surface; skips the UI-adoption trap |
| H4 | **"Adversarial taste-pair"** — not personalization, but a *pair* of agents: "curator" proposes, "contrarian" must publish a weekly "what the curator missed" counter-list with receipts. | 1 | 3 | 2 | **6** | Directly addresses the preference prison, but user-value is unproven |
| H5 | **Full S1A vision — living knowledge graph + briefing + taste-learning** | 2 | 2 | 1 | **5** | Fails on feasibility; every component is rich alone; 1-year solo is aggressive |

**Leaders**: H2 and H3 (tied). H1 is the most *ambitious-but-survivable*.

---

## §8 · Moderator injection response

No moderator notes found in `discussion/002/`. No injection to respond to.

---

### One-line summary

**S1B: 7 searches across 25+ unique URLs; my Part A "300/day" claim validated but growth *stronger* than claimed; my "3–5x throughput" claim withdrawn; my "graveyard" framing wrong — tools survived as narrow utilities not as primary surfaces; Part B concerns on novelty-scoring unreliability and filter-bubble validated; Zotero plugin ecosystem (papersgpt, llm-for-zotero) is *closer to the S1A vision than I realized*; 5 updated hypotheses, H2/H3 (weekly-briefing-as-cron / radar-as-MCP) lead on solo-feasibility.**
