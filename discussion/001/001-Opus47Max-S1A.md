# Idea 001 · S1A · Opus 4.7 Max · Daydream (no search)

**Timestamp**: 2026-04-22T09:26:34Z
**Search used**: NONE. This is imagination + memory only.
**Visibility**: I did NOT read GPT's S1A. Verified `ls discussion/001/` shows only `PROTOCOL.md` at time of writing.

---

## Part A · Most-exciting version (POSITIVE pole)

**10x vision in 5–10 years**: "Research Radar" becomes the *persistent research cortex* of the user — a single surface where an AI-lab lead can walk into their office on a Monday morning and, in 15 minutes, absorb what happened in frontier AI over the weekend at a resolution that *used to require three PhD students and a week*. It is not a "feed reader with summarization." It is a living model of the entire research landscape *from the user's personal point of view*, and that last phrase is the payload.

### A.1 Who the user is, and what their Monday morning looks like

The user runs an AI lab, supervises students and research engineers, and has to decide — every week — which three papers the group should reproduce, which are noise, and which will become the new SOTA baseline that everyone copies in 8 weeks. Today (2026) that decision is made by: (a) skimming arXiv's daily cs.CL + cs.LG lists, which emit ~400 papers/day; (b) scrolling X/BlueSky for whatever happens to be viral; (c) asking a student to "go read this and tell me." This is lossy, personality-driven, and biased toward Twitter-attention rather than substance.

In the 10x version, Monday morning looks like this: the user opens Research Radar. The first screen is not a list. It is a **map**: a 2D layout of ~30 topic clusters the user cares about (RL from human feedback, long-context architectures, multimodal grounding, agent evaluation, diffusion-language hybrids, post-training data curation, inference-time scaling, ...). Each cluster is sized by new-work-this-week. Clusters glow when they moved — a cluster "lit up" means either (1) a new paper pushed SOTA on a tracked benchmark, (2) three labs published correlated work suggesting a regime shift, or (3) a piece of work contradicted an existing entry in the user's knowledge base. The user clicks the glowing cluster. They see a **diff**: here is what the cluster looked like last week, here is what it looks like now, here are the 4 papers that caused the delta, ranked by a *personal* score (novelty × fit-to-lab-agenda × reproducibility × trustworthiness-of-authors-as-estimated-from-prior-work). Each paper has a 90-second verbal brief that the system generated from reading the paper *and cross-referencing it against the 40 related papers already in the knowledge base*. The brief isn't "what the paper says" — abstracts already do that. The brief is "what this paper *changes*": "This overturns the 2025 assumption that X scales; here are the two prior entries in your KB that are now contradicted; here is the experiment the authors *didn't* run that would settle it."

That is the magic. Not summarization. **Delta-aware summarization against the user's own evolving map.**

### A.2 The "aha" moment

The user adds a new paper — say, a colleague sends them a PDF. They drag it in. Within 60 seconds, Research Radar has: extracted the paper's claims, mapped them onto an existing topic (or spawned a new one), **identified 6 prior works the paper claims to beat**, pulled those works from its corpus, and produced a side-by-side claim-check table: "The paper claims +4.2 on benchmark X vs. baseline B, but baseline B is from a 2024 version; the current strongest public baseline on X is C, and this paper does not report against C." The user immediately knows: "this is cooked." That specific moment — where the system *catches something the user would have missed for two weeks* — is when Research Radar stops being a nice-to-have and becomes infrastructure. The first time it happens, the user tells one colleague. The tenth time, they stop reading arXiv unassisted.

### A.3 Why this is dramatically better than anything today

Today's options are: (1) generic paper-summarizer chatbots that re-describe the abstract and are forgotten by next week; (2) curated human newsletters that lag by 5–10 days and reflect the curator's taste, not yours; (3) X/BlueSky, which amplifies drama; (4) asking a student, which doesn't scale and burns relationships. All four are *stateless* — they don't remember what you already know, don't track your topics, don't cross-reference. Research Radar is stateful and personal. It is the difference between Google and a personal librarian who has worked for you for three years.

The second dimension of "dramatically better": **it closes loops the human can't**. When a new paper arrives, a human reads it linearly. The system reads it *against the graph*. When paper X cites paper Y, the system checks whether Y's claims survived since publication (did someone refute Y? Did Y's code repo see a concerning issue?). When a benchmark is referenced, the system knows whether that benchmark is still considered honest or has been deprecated. No human has time to do this for every paper. The system does it by default.

### A.4 Why I believe this is possible (in 2026)

- **Paper ingestion is now tractable.** GROBID-class parsers plus LLM re-read handles ~95% of arXiv PDFs cleanly. The OCR-only problem is largely solved; the structure problem is largely solved.
- **LLMs in 2026 can read a 40-page paper and answer specific factual questions reliably** (Claude 4.7 / GPT-5.4 class). The user stated they have access to these as well as GLM5.1 and Minimax 2.7 via a code plan — *cheap inference is the unlock*.
- **Embedding-based retrieval over ~500k papers fits on a single 4090 with quantized index.** The knowledge base isn't that big.
- **The "delta" operation** — comparing new claims against an evolving KB — is a well-posed LLM task if you structure it: extract claims into a schema, store them, run contradiction detection at insert time. It's not a research problem; it's careful engineering.
- **Personal scale is the friendly case.** One user. No multi-tenant auth, no scaling, no moderation. The MVP fits in a week because the hard part (generalized information retrieval) has been solved enough to stand on.

### A.5 Why the grand version is more than a tool

If it works, it's not a tool — it's a prosthetic. The user's taste, expressed through which papers they mark as "relevant" or "SOTA" or "cooked," becomes training signal for the system's ranking. After six months, the system's top-5 each week matches the user's post-hoc "actually important" list 80% of the time. After a year, the user trusts it enough to route *their lab's* reading list through it. That is the win condition: the radar is not replacing judgment, it is amplifying the one scarce resource — the user's attention — by 10–20x.

---

## Part B · Most-damning version (independent NEGATIVE pole)

Setting aside Part A entirely. Starting fresh.

**The honest take**: this idea has been attempted, in various forms, continuously since ~2018. Arxiv-sanity, Semantic Scholar, Elicit, Undermind, Consensus, Scite, ResearchRabbit, Connected Papers, Emergent Mind, Paperwithcode, Rosebud, Galactica's ill-fated retraction, at least a dozen AI-paper-summarizer YC projects, and countless personal side-projects by researchers who thought "I'll just build it myself in a weekend." Most are either (a) still alive but marginal, (b) pivoted away, or (c) quietly abandoned. The graveyard is large and the survivors are niche. That pattern isn't random. Before building, the founder should take that pattern seriously.

### B.1 Structural reason #1 — the "I'll just read it myself" cliff

The target user is *the kind of person who reads papers*. That's an unusual user. The act of skimming abstracts is, for this population, partly a social and intellectual ritual, not just information transfer. They are suspicious of summarization (rightly — summaries lose nuance, and in research, nuance is often the point). So the product must overcome a deep-seated instinct: "I'd rather read the paper myself and form my own view." Every AI-paper-summarizer I remember has eventually had the user say "it's fine but I still read the paper." If the user still reads the paper, the summarizer isn't infrastructure; it's a triage assistant. Triage assistants have low retention because the cost of using them barely beats the cost of skimming arXiv titles.

### B.2 Structural reason #2 — the "personal knowledge graph" curse

Personal knowledge graphs — Roam, Logseq, Obsidian + smart plugins, Mem, Reflect, Heptabase, etc. — have a consistent failure mode: the *graph doesn't pay for its maintenance cost*. Users spend more time organizing than the organization saves them. Research Radar as described is essentially "personal knowledge graph + auto-ingest + LLM analysis." The auto-ingest helps, but the *personalization* part is where users must invest — marking topics, correcting the system's ontology, resolving conflicts. Without that, the system drifts from what the user cares about. With it, the user is working for the system. There is no free lunch on the taxonomy.

### B.3 Structural reason #3 — "novelty detection" is a near-AGI-complete problem

Part A casually said "novelty, impact, 实用性 scored by the LLM." Let's be honest: *novelty detection in research requires deep domain understanding*. A reviewer at NeurIPS sometimes gets it wrong after reading the paper three times. An LLM one-shot scoring "is this novel?" is going to be dominated by surface similarity — it will score papers novel that use new words and score papers non-novel that have genuinely new ideas in familiar clothing. The user will catch it being wrong 3–4 times in the first week, lose trust, and either stop using the ranking or treat it as a random prior. This is not a fixable bug in one week; this is "the hard part of the problem."

### B.4 Structural reason #4 — the source list problem

"arXiv + top conferences + top labs + GitHub" sounds like a bounded set. It is not. arXiv alone has ~400 cs papers/day; filtering to "AI lab relevant" still leaves ~50–100 papers/day. Top-lab blogs are low-volume but structurally inconsistent (DeepMind blog ≠ Anthropic blog ≠ Thinking Machines blog in format, in claim style, in tone). GitHub "high-potential repos" is the hardest: star-growth is gamed, signal-to-noise is worse than arXiv, and *most* "promising" repos in week 1 are abandoned by week 8. Every one of these sources has its own failure modes; the scraping, normalization, and de-duplication alone is a significant chunk of the claimed one-week timeline. If the user underestimates this, they will spend 4 days on plumbing and have 3 days left for the actual value proposition.

### B.5 Structural reason #5 — LLM cost and latency in a continuous loop

"Detect, download, parse, analyze, cross-reference" for ~50 papers/day means ~50 full-paper LLM reads per day, plus cross-reference reads (call it 3x per new paper), plus daily re-ranking. Even at GLM5.1 / Minimax2.7 pricing, that's non-trivial for a side project — but *more importantly*, the latency means the system's insights lag arXiv by hours, not minutes. If you're doing this to be ahead of the curve, and your pipeline takes 6 hours to produce its daily digest, Twitter scooped you. This kills the "get the drop on everyone else" value prop.

### B.6 Structural reason #6 — the user is one person

One-user systems have a specific failure mode: they never get the feedback loop that would make them good. A SaaS with 10,000 users gets signal on what's valuable. A solo system gets signal on what one specific person wants on one specific Wednesday. Research Radar depends heavily on the user's taste signal to improve, and a single user produces a narrow, noisy, small dataset. The ranking model will never really fit.

### B.7 Prior-art memory — what I remember going wrong

- **Arxiv-sanity** (Karpathy-era): survived as a public utility, but most users use it once a week as a filtered feed, not as a knowledge base. The "knowledge base" layer was never added, despite obvious demand, and I suspect that's because it's much harder than it looks and the incremental value over "sorted list" is smaller than it seems.
- **Galactica**: overconfident extraction of scientific claims blew up publicly because the model was willing to assert things that weren't in the source. Research Radar's "claim check" risks the same failure mode.
- **Various YC AI-paper-summarizer startups**: I remember a pattern where they launched with impressive demos, achieved ~500 users, and then either pivoted to enterprise legal-document or research-tools-for-biopharma (where willingness to pay is much higher). None scaled into "the researcher's tool." The researcher population is small and doesn't pay.
- **Connected Papers** / **ResearchRabbit**: both reasonable products. Neither, to my memory, became central to any researcher's daily practice. They are "I look at this twice when I start a new project" tools.
- **Elicit**: the closest to Part A's vision in spirit. Has a real user base. Has *also* been iterated on by a team of 15+ people for 3+ years. A one-week solo MVP will not out-execute them on the parts they've already built.

### B.8 What I'd tell the founder

Honestly? "You will learn a great deal building this. But do not promise yourself this is the tool that will let you 'keep up with AI' for the next five years. It is more likely a useful 2-month tool that you will then partially abandon, reuse the ingestion for something else, and rediscover that *reading papers is the work*. Build it if the journey is worth it, not because you believe the end state. And if you build it: cut the scope to what matters *only to you in the next 30 days*, not a general radar."

The harshest version: **the bottleneck on staying current with AI research is not a tool problem. It is an attention problem. No tool can solve an attention problem for a person who is already over-subscribed.** A more honest product might be a *reading reduction* tool (reject 95% of papers confidently) rather than an *awareness amplification* tool (surface more papers more efficiently).

---

## Part C · Epistemic honesty — what I'd actually need to know

I just wrote two imaginative passages. Real separation time.

### C.1 Claims backed by real confidence

- **Claim**: "arXiv emits ~400 cs papers/day; cs.CL + cs.LG alone are ~50–100/day AI-relevant."
  **Source of confidence**: direct memory from using arXiv's daily listings in 2023–2025 range. The rough order-of-magnitude (hundreds/day) I'm confident on. Exact current 2026 rate I'd want to verify — could easily have grown.

- **Claim**: "GROBID and similar PDF parsers extract structure from arXiv PDFs with ~95%-ish success on well-formed papers."
  **Source of confidence**: I've seen parsing pipelines in production and heard this number in roughly this range. Precise figure is a guess; qualitative claim (PDF extraction is largely tractable) is solid.

- **Claim**: "LLMs in 2026 can answer factual questions about a 40-page paper reliably if the context fits."
  **Source of confidence**: my own experience with Claude 4.x and knowledge of 2025 benchmark progression. Long-context faithfulness isn't perfect (I remember ~85-95% factual accuracy on well-designed paper-QA benchmarks), but it's good enough for the use case.

- **Claim**: "Personal knowledge graph tools have a 'maintenance-cost > value' failure mode."
  **Source of confidence**: I've watched multiple waves of these tools (Roam → Obsidian → Mem → Reflect) and read enough post-mortems from former power-users to believe the pattern is robust.

- **Claim**: "Elicit has been iterated on for 3+ years by 15+ people."
  **Source of confidence**: rough memory of their team size from 2023–2024 coverage. Order of magnitude I trust; exact numbers I'd want to check.

- **Claim**: "Novelty detection is hard even for human reviewers."
  **Source of confidence**: widely-discussed NeurIPS/ICLR reviewer-disagreement studies. I'm confident the phenomenon is real; specific statistics (e.g., the ~40% reviewer disagreement rate I half-remember) I'd want to re-verify.

- **Claim**: "GitHub star-growth is gamed and noisy."
  **Source of confidence**: domain intuition from watching many repos. Very confident qualitatively.

- **Claim**: "Arxiv-sanity exists, Connected Papers exists, ResearchRabbit exists, Elicit exists, Undermind exists."
  **Source of confidence**: direct memory of having seen or used these. High.

### C.2 Claims that are assumptions I haven't tested

- That the user's stated 1-week timeline is achievable. I wrote "the MVP fits in a week" in Part A; in Part B I suggested the plumbing alone consumes most of that. I don't actually know which is true — it depends heavily on scope cut and tooling maturity.
- That "80% agreement between system top-5 and user post-hoc top-5 after 6 months" is a reasonable target. I made that number up. It sounds good. I have no calibration for it.
- That GLM5.1 and Minimax2.7 pricing is "cheap enough" to run ~50-150 full-paper reads per day continuously. I don't know their 2026 per-token pricing.
- That the user's 4090 is sufficient for the embedding index. Depends entirely on corpus size, which I assumed was ~500k papers; could be 2M if we include all cs.* since 2015.
- That claim-extraction + contradiction-detection is "careful engineering, not research." Said this confidently in Part A. On reflection, I'm maybe 60/40 on this — it might be substantially harder than I implied.
- That one-person systems don't get enough feedback signal to improve. This is a folk belief of mine; I have not actually tested it against counterexamples (a lot of personal tools do improve for their single user, via direct user edits).
- That "most YC AI-summarizer startups pivoted to enterprise legal/biopharma." I said this as if I knew a pattern. It's more like "I vaguely recall this" — the pattern might be weaker or non-existent.
- That paper-summary bots have "low retention." Asserted in Part B, but I actually don't have retention numbers for any of them.

### C.3 Known unknowns — things I know I don't know

1. The current 2026 per-day volume on arXiv cs.* and AI-relevant subset. Probably grew from 2024 baseline, unclear by how much.
2. Whether any existing product (Elicit, Undermind, Emergent Mind, Paperguide, etc.) has added a *delta-aware* or *personal-KB-aware* layer in the last ~6 months. The space moves fast.
3. Whether arXiv has an official API or if scraping is the realistic path. I half-remember an OAI-PMH endpoint but don't know its terms.
4. Whether Semantic Scholar's API is still generous enough to be the citation-graph backbone, or if it's been restricted.
5. What the actual cost envelope looks like at GLM5.1 / Minimax2.7 2026 prices per 100k tokens.
6. What PDF-extraction tools currently lead in open-source (nougat? marker? GROBID? something newer?).
7. Whether there is a standard "paper → claims schema" extraction prompt/tool that already works well, or if this is a non-trivial research problem in 2026.
8. Benchmark trackers (paperswithcode) — are they still maintained and usable as a SOTA-tracking backbone, or have they decayed?
9. How the user actually makes decisions today — concrete workflow details that would change MVP priorities. (This is a user-research question, not a web-search question, but it's the biggest unknown.)
10. Whether the user will actually use it daily, or whether it will be a 2-week novelty that fades — I have no prior with this specific user.
11. Legal / ToS question: can a personal tool legally ingest, cache, and summarize papers at scale? arXiv license is permissive-ish; top-lab blogs often aren't.
12. Whether GitHub "trending repo" signal can be meaningfully filtered to AI-research relevance without enormous noise.

### C.4 Five search-shaped questions for S1B

1. `arxiv papers per day 2026 cs.CL cs.LG cs.AI current volume`
2. `best open source PDF paper extraction tool 2025 2026 nougat marker grobid comparison` (looking for what a one-person builder would actually use)
3. `Elicit Undermind Emergent Mind research paper tools 2025 feature comparison retention` (what have the incumbents built — especially personal-KB or delta-aware features)
4. `LLM claim extraction scientific paper contradiction detection benchmark 2025` (is the "claim-check" step in A.2 actually a solved problem, or is it still research?)
5. `Semantic Scholar API 2026 rate limits pricing alternatives OpenAlex` (what's the citation-graph backbone for 2026?)

---

*End of S1A Daydream. Proceeding to list the directory and notify human.*
