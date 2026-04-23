# Idea 001 · S1B · Opus 4.7 Max · Ground (with search)

**Timestamp**: 2026-04-22T09:40:00Z
**Search used**: 7 WebSearch queries; 30+ unique URLs surfaced; 10 cited below.
**Visibility**: I read my own S1A, GPT's S1A (all three parts), and the PROTOCOL. No moderator notes exist yet.

---

## §1 · What GPT's S1A gave me that I missed

Independent imagination, then comparison. Three real gaps:

1. **The framing "discovery + memory + synthesis are fragmented"** (GPT Part A). I treated the fragmentation as a given; GPT named it as the *core unlock*. This is cleaner than my "delta-aware summarization" framing because it names which *three* loops must be fused. I steal this: the product's core verb is **fuse discovery + memory + synthesis into a single loop**, not "summarize deltas."
2. **"Tacit taste, local context, and long-running technical memory"** (GPT Part B). GPT articulated the social/embodied nature of research judgment better than I did. My Part B.3 said "novelty detection is near-AGI-complete" — GPT's framing is more useful: *taste* is the bottleneck, and taste is *learnable from the user's actions* but not from the paper's text. That reframes the training-signal problem.
3. **The bad-equilibrium warning** (GPT Part B, penultimate paragraph): *"expensive ingestion, impressive dashboards, low behavioral change."* This is a sharper failure mode than my "graveyard of abandoned products." It predicts *how* a v1 that "works" will still fail — behaviorally — even with polished summaries. I steal this as an explicit anti-goal.

What I contributed that GPT didn't: concrete prior-art memory (Elicit, Undermind, Connected Papers, Galactica, Arxiv-sanity), specific numbers (arXiv ~400/day memory), the delta-check mechanism, LLM cost realism, and the "tool cannot solve an attention problem" epigram.

**Convergence**: both of us independently wrote the same anti-pattern — grand universal radar for everyone. Both converged on "this must be radically narrow to work." Encouraging.

## §2 · Merged question list → searches run

Merged 10 raw C.4 questions (my 5 + GPT's 5) → 7 unique searches after dedup. (My Q1+GPT Q4 overlap → combined into volume search; my Q3+GPT Q1 overlap → combined into prior-art search; my Q4+GPT Q3 overlap → combined into claim-extraction search.)

**Q1. arXiv volume 2026.**
Finding: arXiv hit **~28,000 submissions/month** late 2025 (vs. ~24k late 2024), total corpus **>3M as of April 19, 2026**. Exact cs-AI-relevant daily rate still not directly broken out in public dashboards. My S1A figure "~400 cs/day" is consistent order-of-magnitude; real 2026 number is probably higher (plausibly 500-700/day across cs), with AI-relevant subset **~100-200/day** — about 2x what I estimated. This makes the scale problem *harder* than my Part A assumed.
Sources: [arXiv blog submission records](https://blog.arxiv.org/2024/11/04/arxiv-sets-new-record-for-monthly-submissions-again/), [arXiv Wikipedia](https://en.wikipedia.org/wiki/ArXiv).

**Q2. Prior-art AI research-assistant space (2025–26).**
Finding: **17-PhD evaluation** ranks **Elicit #1 (7.3/10)** and **Undermind #2 (6.8/10)**, both general-purpose academic deep-research tools. Both already **do not fabricate citations** (a risk I worried about is largely solved in this class). Undermind's differentiator is **successive search** (iteratively refines queries over 2–3 min). SciSpace does per-paper chat and literature-review tables. **None of the big 3 is positioned as a personal radar with a persistent KB diff** — they are session-based. This is both a confirmation (my "delta-aware personal KB" gap is real and unfilled) and a threat (they can add it faster than a solo dev).
Sources: [Aaron Tay — Google Scholar vs AI tools](https://aarontay.substack.com/p/google-scholar-vs-other-ai-search-tools), [SMU deep-research literature tools](https://library.smu.edu.sg/topics-insights/deep-research-literature-tools-what-are-they-and-how-are-they-different), [Undermind site](https://www.undermind.ai/).

**Q3. PDF extraction stack 2025–26.**
Finding: the field moved. **Marker** (VikParuchuri) is now the pragmatic open-source choice — **~25 pages/sec on H100**, outputs Markdown/JSON, handles equations. **Nougat** (Meta) is end-to-end neural but slower than classical Grobid (Grobid: 10.6 PDF/s). **Mathpix** (commercial) and **PaddleOCR-VL** lead the CVPR 2025 OmniDocBench at >9.6 formula-extraction score. For a 4090 + one-week build, **Marker is the right default**; Grobid for metadata/citations; fall back to a VLM only on failures. This mostly validates my S1A C.1 claim ("PDF parsing largely tractable") and also updates me: specialized math extraction is much better than I knew.
Sources: [marker-pdf PyPI](https://pypi.org/project/marker-pdf/), [Nougat paper](https://arxiv.org/pdf/2308.13418), [Meursault 12-tool eval](https://liduos.com/en/ai-develope-tools-series-2-open-source-doucment-parsing.html), [OmniDocBench CVPR 2025](https://openaccess.thecvf.com/content/CVPR2025/papers/Ouyang_OmniDocBench_Benchmarking_Diverse_PDF_Document_Parsing_with_Comprehensive_Annotations_CVPR_2025_paper.pdf).

**Q4. LLM scientific-claim extraction + contradiction detection (2025).**
Finding: this is *still an active research area*, not a solved engineering problem. 2025 VLDB paper extracts claims from 80 papers across med+CS with "valuable but limited" results; ACL 2025's **SCIVER** evaluates multimodal claim verification and finds LLMs *can predict weakness categories given the review* but **struggle significantly to verify and identify weaknesses from scratch**. This directly damages my S1A Part A.2 "aha moment" (drag in a paper, auto-get a claim-check table) — that specific demo will only partly work. It is not AGI-hard, but it will not be one-prompt and will fail loudly on adversarial cases. My Part B.3 warning is **validated**.
Sources: [VLDB 2025 TaDA claim extraction](https://www.vldb.org/2025/Workshops/VLDB-Workshops-2025/TaDA/TaDA25_16.pdf), [SCIVER ACL 2025](https://aclanthology.org/2025.acl-long.420.pdf), [LLM critiques of papers ACL 2025](https://aclanthology.org/2025.findings-emnlp.1185.pdf).

**Q5. Citation-graph backbone for 2026.**
Finding: **Semantic Scholar** public API = 1000 RPS shared unauth, **1 RPS per API key** on intro tier — usable but fragile. **OpenAlex** = **~100k calls/day soft limit, no hard rate limit**, fully open, positioned as the MAG replacement. For a personal radar, **OpenAlex is the right primary** backbone with Semantic Scholar as secondary. I did not know OpenAlex was this strong in 2026.
Sources: [OpenAlex developer docs](https://developers.openalex.org/), [OpenAlex vs Semantic Scholar vs PubMed comparison](https://intuitionlabs.ai/articles/openalex-semantic-scholar-pubmed-comparison).

**Q6. Alert fatigue / paper-recommender retention.**
Finding: CHI-adjacent 2024 work (**PaperWeaver**) confirms the exact failure mode I named: "existing alert systems only present title + abstract; researchers struggle to connect recommendations to their own research context" — which is why retention drops. Arxiv-sanity is explicitly *about* taming the flood; its author (Karpathy) ended up simplifying to "arxiv-sanity-lite" because the full KG version didn't stick. Alert fatigue is a named, measured, structural problem. My Part B and GPT's Part B both got this right.
Sources: [PaperWeaver arXiv 2024](https://arxiv.org/html/2403.02939v2), [arxiv-sanity-preserver GitHub](https://github.com/karpathy/arxiv-sanity-preserver).

**Q7. Personal KG / ontology drift in practice.**
Finding: ontology drift is a named failure mode with industry write-ups: *"the silent killer of enterprise KG projects,"* and only **~27% of organizations have KGs in production** as of late 2025 despite years of hype. Newly-added documents introduce redundant / conflicting entities requiring non-trivial merge+alignment pipelines. **GPT's Part B warning about ontology drift is strongly validated.** This is an engineering risk I had under-weighted in my Part A.
Sources: [Ontology Drift, Medium Feb 2026](https://medium.com/graph-praxis/ontology-drift-why-your-knowledge-graph-is-slowly-going-wrong-234fa238826c), [Ontology Learning arXiv 2511.05991](https://arxiv.org/html/2511.05991v1).

## §3 · Prior art catalog

| Name | Status | Relevance | URL |
|---|---|---|---|
| **Elicit** | Active, #1 in 2025 PhD eval (7.3/10) | Closest to grand vision; session-based, no personal KB diff | https://elicit.com |
| **Undermind** | Active, #2 (6.8/10) | Successive-search is the interesting idea; still session-based | https://www.undermind.ai/ |
| **SciSpace** | Active | Per-paper chat + lit-review tables; no radar layer | https://scispace.com |
| **arxiv-sanity-lite** | Active, simplified | The "full version" failure is a direct lesson: complexity got in the way | https://github.com/karpathy/arxiv-sanity-preserver |
| **PaperWeaver** | Research prototype (2024) | Explicitly tackles the "alert but no context" problem | https://arxiv.org/abs/2403.02939 |
| **Connected Papers / ResearchRabbit** | Active, low daily-use | Graph-exploration tools, not radars | (from memory) |
| **Semantic Sanity (Allen AI)** | Active | Personalized arXiv recs; precursor pattern | https://s2-sanity.apps.allenai.org/faq |
| **Galactica** | Dead (2022) | Warning about over-confident scientific claim extraction | (from memory) |

## §4 · Reality vs daydream verdict on my S1A

### My Part A claims
- **"Delta-aware summarization against personal KB is the payload"** → **stronger.** No incumbent does it. Validated gap.
- **"80% agreement on top-5 after 6 months"** → **unknown / invented.** Drop the specific number; reframe as "calibrated to the user's own post-hoc judgments."
- **"MVP fits in a week"** → **weaker.** The full-grand-radar does not fit in a week. A *scoped* MVP (1 source, 1 topic area, personal KB diff on a small index) could.
- **"Cheap inference is the unlock"** → **unchanged.** Still true, but claim-extraction is more expensive per-paper than I implied because it needs multi-pass (extract → ground → contradict).
- **"4090 sufficient for embedding index"** → **stronger** for cs-AI only subset; **unknown** for full arXiv corpus.

### My Part B concerns
- **"Novelty detection is the hard part"** → **validated** by SCIVER 2025 finding (LLMs struggle on claim verification from scratch).
- **"One-user feedback loop is thin"** → **neither validated nor refuted** by search; remains a live risk but ** taste-from-actions (GPT's framing) gives a partial answer.**
- **"Summarizers have low retention"** → **partially validated** (PaperWeaver paper cites this exact problem); measured effect sizes still unknown.
- **"YC startups pivoted to enterprise"** → **not verified.** Demote to "anecdotal memory, may be wrong."
- **"Plumbing will eat the week"** → **validated** by tool survey: picking ingestion stack + normalization across arXiv + blogs + GitHub is days, not hours.

## §5 · Graveyard lessons

Three repeated failure modes across Galactica, arxiv-sanity-full, generic summarizers, and 15-org-out-of-55 KG projects:

1. **Overconfident extraction destroys trust.** If the claim-check step in my A.2 fails on a paper the user *knows*, the whole system loses credibility. Mitigation: always show provenance and always allow an "I disagree" override that re-trains.
2. **Ontology drift poisons the KB.** Either auto-generated topics decay, or manual curation burns out. Mitigation: do **not** ship a fixed ontology; let it emerge from user tags + embedding clusters, and accept messy.
3. **Alert fatigue at ≥ few-per-day; trust loss at any false-urgent.** The push-notification layer is the single most dangerous surface. Mitigation: **default to digest-only, no push until the user explicitly whitelists a topic**.

## §6 · What is genuinely novel here (after subtraction)

Stripping away what exists or has failed:

- **Session-based research assistants** (Elicit, Undermind) exist and are good.
- **Static knowledge graphs** exist and fail on drift.
- **Alert feeds** (arxiv-sanity, Semantic Sanity) exist and suffer fatigue.
- **Per-paper chat** exists (SciSpace).

What's **not** shipped by any incumbent I can find:

1. **Delta-against-personal-KB**: when a new paper arrives, explicitly compare its claims against entries already in *your* KB and flag contradictions / supersessions. This requires the KB to be shallow-but-structured enough to diff against.
2. **Taste-from-actions learning**: the user's actions ("marked cooked," "saved," "starred for reproduction," "ignored") continuously train a personal ranker — not generic "relevance," but *this user's revealed preference*.
3. **Claim-level provenance**: instead of paper-level summaries, extract and store *individual claims* with their evidence. Makes contradiction detection tractable and makes distrust localisable.

#3 is technically risky (see SCIVER finding) but #1 and #2 are engineerable in 2026.

## §7 · Updated hypothesis space

| # | Version | Demand | Differentiation | Solo-feasibility (1 wk) |
|---|---|---|---|---|
| **H1** | **Grand Radar** — all sources, KB, delta, push, ontology. | High (personal) | Medium (Elicit can catch up) | **Low** — 3–4 weeks honest |
| **H2** | **Personal Delta-KB (narrow)** — arXiv only, 2 AI sub-areas, daily digest with "what changed vs your saved papers." | Medium-high | **High** (no incumbent does personal-KB diff) | **Medium-high** if scoped |
| **H3** | **Claim-level Reader+Diff** — drag-in-PDF → extract claims → check against local claim DB → flag contradictions. | Medium (one-use-at-a-time) | Very high | Medium — depends on how well SCIVER-class extraction works in practice |
| **H4** | **Lab-Brief Generator** — weekly 500-word brief for *a specific lab agenda*, not a radar; evidence-grounded from the week's top 50 arXiv. Low-touch. | Medium (the user gets one thing to read) | Medium | **High** — very buildable in a week |
| **H5** | **Reject-95%-Confident** — inverted radar; every morning show only the ~5 papers worth opening out of ~200, with 1-line reason each. Quiet by design. | High (solves attention, not awareness) | High | **High** |

My ranked lean: **H5 > H2 > H4 > H3 > H1.** The inversion from "surface more" to "reject more confidently" matches my Part B's attention-bottleneck argument and GPT's bad-equilibrium warning. H2 is the defensible differentiation. H1 is a 2-month trap.

## §8 · Moderator injection response

No moderator notes present at time of writing.

---

*End of S1B. Ready for stage-1 synthesis.*
