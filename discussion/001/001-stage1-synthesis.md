# Stage 1 Synthesis — Idea 001 · Research Radar

**Sources consulted (S1B combined)**: ~17 unique URLs (Opus cited 10, GPT cited 11, overlap ~4)
**Moderator injections**: none (no `001-moderator-notes.md` at time of synthesis)
**S1A posture**: Opus = POSITIVE pole, GPT = NEGATIVE pole (per PROTOCOL §S1R1)
**Synthesizer note**: both debaters wrote all three parts (A positive + B negative + C epistemic) independently within their own S1A, so the "pole assignment" is a lean rather than a hard boundary for this stage.

---

## 0. Stage 1 structure recap

This synthesis covers the four Stage 1 files:

- **S1A · Daydream** (no search, no cross-reading):
  - `001-Opus47Max-S1A.md` — long, prose-heavy, concrete numeric guesses
  - `001-GPT54xHigh-S1A.md` — shorter, more abstract, framing-oriented
- **S1B · Ground** (with search, both debaters read each other's S1A first):
  - `001-Opus47Max-S1B.md` — 7 searches, 10 URLs cited
  - `001-GPT54xHigh-S1B.md` — 5 searches, 11 URLs cited

The imagination/verification boundary matters. Stage 2 debaters should be
able to tell which beliefs were *invented from memory* (§1–§4 of this synthesis)
vs. which survived *contact with the web* (§5–§8). Shared intuitions that
turned out wrong are called out explicitly in §7.

---

## 1. Shared imagination (both S1A Part A agreed, before any evidence)

Both Opus and GPT independently daydreamed the same optimistic core, which is
a strong "both models guessed it" signal but also a shared-prior signal that
deserves scrutiny.

**1.1 The core payload is a *personal* system, not a general feed reader.**
Opus framed it as "a living model of the entire research landscape *from the
user's personal point of view*." GPT framed it as "a private scientific
intelligence system for one lab leader." Both explicitly rejected the "generic
summarizer" framing.

**1.2 Fusion of three loops that are currently fragmented.** Opus: discovery +
cross-reference + knowledge-base + delta. GPT (more crisply): "detect, compare,
connect, remember, and update" — fusing **discovery + memory + synthesis** into
one loop. GPT's three-loop naming is the cleaner articulation; Opus adopted it
in S1B §1.

**1.3 The win condition is *behavioral change*, not better dashboards.** Opus:
"the user stops reading arXiv unassisted." GPT: "the user stops 'checking arXiv'
and starts consulting a trusted radar before making research bets." Both
imagined the same success marker.

**1.4 Taste / personalization is the differentiator from incumbents.** Opus:
"the user's taste, expressed through which papers they mark as relevant or SOTA
or cooked, becomes training signal." GPT: "the user is narrow and opinionated …
high hit rate on things I would have regretted missing." Same idea, different
framings.

**1.5 The grand version becomes infrastructure, not a tool.** Opus: "prosthetic."
GPT: "compounding asset." Both used nearly identical escalation language.

**1.6 Current LLMs are good enough for the narrow version.** Both asserted this
without citation in S1A.

**Note for Stage 2**: the convergence on §1.1–§1.5 is the strongest signal from
Stage 1. If both models independently reached for the same positive framing
without reading each other, the framing is probably load-bearing. Flag §1.6 as
"shared imagination" — it was also true, but both debaters needed S1B to verify it.

---

## 2. Shared pessimism (both S1A Part B agreed)

Both debaters independently surfaced the same failure modes:

**2.1 Novelty / impact scoring is the hard part, not the plumbing.** Opus
called it "near-AGI-complete." GPT called it "tacit taste, local context, and
long-running technical memory." Same concern, different language. Opus's
version is harsher; GPT's is more actionable (taste is *learnable from actions*
even if not from text).

**2.2 Knowledge-base / ontology drift will decay the value.** Opus referenced
the "personal knowledge graph curse" (Roam / Logseq / Mem failure pattern). GPT
named the "classic knowledge-management trap" where "ontologies drift, tags
sprawl, and the knowledge base can become a graveyard of summaries nobody
trusts." Both flagged it without prompting.

**2.3 Alert fatigue / low trust when push-notifications misfire.** Opus: push
layer is "the single most dangerous surface" (though this is actually from S1B).
GPT S1A: "if it sends too many plausible-but-not-important things, trust also
drops." Shared concern.

**2.4 "I'll just read it myself" is the retention cliff.** Opus called it
out by name. GPT didn't name it as crisply but implied it ("LLMs can imitate
that voice before they truly earn it").

**2.5 The grand one-week solo MVP is probably overclaimed.** Opus: "do not
promise yourself this is the tool that will let you keep up with AI for the
next five years." GPT: "not in the grand form described, and not with a
one-week solo build target."

**Note for Stage 2**: the pessimism convergence is also strong. Five independent
failure modes surfaced in both Part Bs. None of them were fabricated — S1B
validated all five (see §7).

---

## 3. Divergent daydreams

The two S1As were not identical. Key splits:

| Dimension | Opus S1A thought | GPT S1A thought | S1B verdict on the split |
|---|---|---|---|
| **Concrete mechanism for the "aha moment"** | Drag-in-PDF → auto claim-check table vs 6 prior works; names a specific demo | Generic "short brief that says what assumption weakens" | **Opus's mechanism partially broken** — SCIVER 2025 finds LLMs struggle to verify claims from scratch. The *demo* Opus described will fail loudly on adversarial papers. |
| **Volume realism** | "arXiv ~400 cs/day, ~50-100 AI-relevant" | "high enough that manual tracking doesn't scale" (no number) | **Opus's number low** — S1B revised to 500-700 cs/day, ~100-200 AI-relevant in 2026 |
| **Ontology strategy** | Implicit: let user curate a personal graph | Flagged drift as a core risk; no strategy offered | **GPT was right to flag it** — S1B confirmed ontology drift is a "silent killer" with only ~27% of org KGs in production |
| **Prior-art specificity** | Named ~10 products from memory (Elicit, Undermind, Connected Papers, Galactica, arxiv-sanity, ResearchRabbit, Scite, Consensus, etc.) | Zero products named in S1A | **Opus's memory was largely accurate** — S1B confirmed most named products exist and are positioned roughly as claimed. GPT's lack of specificity cost them. |
| **The "attention not awareness" framing** | "No tool can solve an attention problem for a person who is already over-subscribed" → suggests an *inverted* radar (reject 95%) | Did not articulate this inversion | **Opus-only framing**; survived S1B and became H5/Reject-95% in the hypothesis space. GPT's S1B did not re-derive it. |
| **Cost modeling** | "~50 full-paper LLM reads/day + 3x cross-ref reads + daily re-rank" with specific concern | Not addressed | **Opus-only framing**; still unresolved. |
| **Team-memory dimension** | Mentioned lab reading list late in Part A | "Whether the user's real need is discovery, synthesis, or team-memory preservation" — raised it as an open question | **GPT-only framing**; Stage 2 should decide whether "team" is in scope or not. |
| **User-research vs web-research question** | Flagged "how the user actually makes decisions today" as a non-web-searchable known unknown | Similar framing but less explicit | Both agreed but neither resolved. Carried to §11. |

---

## 4. The merged Part C question list (what was unknown at the starting line)

This is the combined C.4 set from both debaters, before either ran searches.

**Opus's 5 search-shaped questions (from 001-Opus47Max-S1A.md C.4):**
1. arXiv papers per day 2026, cs.CL/cs.LG/cs.AI volume
2. Best open-source PDF extraction tool 2025–26 (Nougat / Marker / GROBID comparison)
3. Elicit / Undermind / Emergent Mind 2025 feature comparison and retention
4. LLM claim extraction + contradiction detection benchmark 2025 (still research or solved?)
5. Semantic Scholar API 2026 rate limits / alternatives / OpenAlex

**GPT's 5 search-shaped questions (from 001-GPT54xHigh-S1A.md bottom):**
1. AI research radar / arXiv / blog / GitHub personalized monitoring tool for researchers
2. Why paper recommendation tools fail for researchers (alert fatigue, discovery, trust)
3. Automated novelty detection in research papers (benchmark survey, LLM scientific literature)
4. Knowledge graph for scientific literature (topic ontology maintenance failure cases)
5. Single-user research workflow (Semantic Scholar / arXiv alerts / repo tracking / notes) comparison

**Merged question set (de-duplicated) — what Stage 1 actually tried to answer:**

| # | Topic | Contributed by | Resolved in S1B? |
|---|---|---|---|
| Q1 | arXiv volume 2026 | Opus Q1 + GPT Q5 (adjacent) | Partially — corpus size resolved; AI-relevant daily rate estimated |
| Q2 | Prior art landscape (Elicit / Undermind / ResearchRabbit / SciSpace / etc.) | Opus Q3 + GPT Q1 + GPT Q5 | Yes — solid catalog produced |
| Q3 | PDF extraction toolchain | Opus Q2 | Yes — Marker is the 2026 default |
| Q4 | Claim extraction + contradiction detection maturity | Opus Q4 + GPT Q3 | Yes — still research, not solved |
| Q5 | Citation-graph backbone (OpenAlex / Semantic Scholar API) | Opus Q5 | Yes — OpenAlex favored |
| Q6 | Alert fatigue / recommender retention | GPT Q2 | Yes — named failure mode with evidence |
| Q7 | Ontology / KG drift in practice | GPT Q4 | Yes — confirmed as silent killer |
| Q8 | Galactica-class overconfidence failures | GPT-only (implicit) | Yes — Galactica withdrawal cited |

This question-set is what Stage 2 debaters should treat as "resolved at the
starting line." Anything not on this list is either unknown (§11) or assumed.

---

## 5. Evidence picked up in S1B

Merged and de-duplicated from both S1Bs. Prioritized by lesson weight for
Stage 2.

| Name | Status | What it does | Lesson for us | Cited by | URL |
|---|---|---|---|---|---|
| **Elicit** | Live, ranked #1 by 17-PhD panel (7.3/10 in 2025 eval) | Broad-source agentic literature review; does not fabricate citations | Session-based, no persistent personal KB diff. *This is the gap.* Can add our features faster than we can catch up on theirs. | Both | https://elicit.com · https://support.elicit.com/en/articles/11241729 |
| **Undermind** | Live, #2 in same eval (6.8/10) | Deep successive search (2–3 min iterative refinement); novelty/gap framing; alerts | "Successive search" is a primitive worth understanding. Still session-based. | Both | https://www.undermind.ai/ |
| **Semantic Scholar (product)** | Live | Search, library, alerts, personalized feeds on top of large corpus | Closer to a radar than the others; existing alerts infrastructure. Hard incumbent to beat on breadth. | GPT | https://www.semanticscholar.org/product |
| **ResearchRabbit** | Live, low daily-use | Visual literature maps and exploration | Graph-exploration ≠ radar. Low retention for daily research practice. | Both | https://www.researchrabbit.ai/ |
| **SciSpace** | Live | Per-paper chat + literature-review tables | Per-paper chat is easy; not a radar. | Opus | https://scispace.com |
| **arxiv-sanity / arxiv-sanity-lite** | Live, simplified | Personalized arXiv recommender | **High-signal lesson**: Karpathy pared down from full KG to simple lite version. The "full knowledge base" version didn't stick; simpler version did. | Both | https://github.com/karpathy/arxiv-sanity-preserver |
| **Semantic Sanity (Allen AI)** | Live | Personalized arXiv recommendations | Precursor pattern for the feed piece. | Opus | https://s2-sanity.apps.allenai.org/faq |
| **PaperWeaver (2024 research prototype)** | Prototype | Explicitly tackles "alert but no context" problem — generates context-grounded paper recommendations | **High-value lesson**: names the exact failure mode (titles + abstracts alone leave researchers unable to connect to own work) and measures it. Worth reading in full before Stage 2. | Opus | https://arxiv.org/html/2403.02939v2 |
| **Galactica (Meta, 2022, withdrawn)** | Dead | Science-facing LLM that confidently fabricated citations | **Cautionary anchor**: any claim-check surface will be judged against this history. Provenance + "show your work" is not optional. | Both | https://www.deeplearning.ai/the-batch/meta-released-and-quickly-withdrew-a-demo-of-its-galactica-language-model/ |
| **Marker (VikParuchuri)** | Live OSS | PDF → Markdown/JSON, ~25 pages/sec on H100, handles equations | **Pragmatic 2026 default** for a solo build on a 4090. Faster than Nougat; less brittle on math. | Both | https://pypi.org/project/marker-pdf/ · https://github.com/cuuupid/cog-marker |
| **Nougat (Meta)** | Live OSS | End-to-end neural PDF parsing | Slower than alternatives; not the first choice for solo builders. | Both | https://arxiv.org/pdf/2308.13418 |
| **GROBID** | Live OSS, mature | Classical PDF metadata/citation extraction, 10.6 PDF/s | Use for metadata/citations layer. Complements Marker. | Both | https://github.com/grobidOrg/grobid |
| **OmniDocBench (CVPR 2025)** | Benchmark | Evaluates PDF parsing across tools | Reference point for choosing the stack. Mathpix / PaddleOCR-VL lead on formulas (>9.6). | Opus | (link in Opus S1B) |
| **OpenAlex** | Live | Open scholarly corpus + API; ~100k calls/day soft limit, no hard rate limit | **Primary citation-graph backbone for 2026**. Better than Semantic Scholar for a personal radar because of quota and openness. | Both | https://developers.openalex.org/ |
| **Semantic Scholar API** | Live | Citation graph + paper data; 1000 RPS shared / 1 RPS per key on intro tier | Secondary backbone. Usable but fragile for sustained volume. | Both | https://www.semanticscholar.org/product/api |
| **arXiv public API + OAI-PMH** | Live, documented | Official endpoints for listing/harvesting | Answers the "legal path to arXiv data" question directly. | GPT | https://info.arxiv.org/help/api/index.html · https://info.arxiv.org/help/oa/index.html |
| **SCIVER (ACL 2025)** | Benchmark | Multimodal scientific claim verification | **Directly probes the "auto claim-check" promise**. Finding: LLMs can categorize weakness *when given the review* but struggle to identify them from scratch. Implication: the A.2 "drag in a paper, get a claim table" demo will work partially, not fully. | Opus | https://aclanthology.org/2025.acl-long.420.pdf |
| **TaDA (VLDB 2025)** | Benchmark/paper | Claim extraction across 80 papers, med + CS | "Valuable but limited" results on claim extraction — consistent with SCIVER. | Opus | https://www.vldb.org/2025/Workshops/VLDB-Workshops-2025/TaDA/TaDA25_16.pdf |
| **SCITAB / CliniFact / Valsci** | Benchmarks | Scientific claim verification datasets (1.2K / 1,970 / ~500 instances) | Supports *narrow* verification, not open-domain novelty/impact scoring. | GPT | https://aclanthology.org/2023.emnlp-main.483/ · https://www.nature.com/articles/s41597-025-04417-x · https://link.springer.com/article/10.1186/s12859-025-06159-4 |
| **Scholarly recommender survey (Knowledge and Information Systems, 2023)** | Review | Stresses user-satisfaction evaluation | Generic "relevance" is not enough; satisfaction is a separate axis. | GPT | https://link.springer.com/article/10.1007/s10115-023-01901-x |
| **Alert fatigue clinical study** | Empirical | Low-value alerts reduce acceptance | Evidence is from clinical systems, but the mechanism generalizes. | GPT | https://link.springer.com/article/10.1186/s12911-017-0430-8 |
| **arXiv submission records (2024–25)** | Metric | ~28k submissions/month late 2025 (up from ~24k late 2024); >3M total corpus as of April 19, 2026 | Updates volume estimate. Implies daily AI-relevant rate ~100-200, roughly 2x Opus's S1A guess. | Opus | https://blog.arxiv.org/2024/11/04/arxiv-sets-new-record-for-monthly-submissions-again/ |
| **"Ontology Drift" Medium piece (Feb 2026)** | Industry write-up | Names ontology drift as the "silent killer" of enterprise KG projects; ~27% of orgs have KGs in production | Validates GPT's S1A concern with real numbers. | Opus | https://medium.com/graph-praxis/ontology-drift-why-your-knowledge-graph-is-slowly-going-wrong-234fa238826c |
| **Ontology Learning arXiv (2511.05991)** | Research | Documents redundant/conflicting entity problem in growing KGs | Supports "let ontology emerge" strategy. | Opus | https://arxiv.org/html/2511.05991v1 |
| **Aaron Tay — Google Scholar vs AI tools** | Industry eval | 17-PhD ranking of 2025 academic AI tools | Source of the Elicit #1 / Undermind #2 finding. | Opus | https://aarontay.substack.com/p/google-scholar-vs-other-ai-search-tools |
| **SMU deep-research literature tools** | Industry eval | Comparative review of deep-research AI tools | Corroborates Aaron Tay. | Opus | https://library.smu.edu.sg/topics-insights/deep-research-literature-tools-what-are-they-and-how-are-they-different |

**Reading priority for Stage 2 (top 3)**:

1. **PaperWeaver (arxiv 2403.02939)** — names the alert/recommendation failure
   mode with empirical grounding. Most directly relevant to the product shape.
2. **SCIVER (ACL 2025)** — defines what claim-verification LLMs can and can't do
   in 2025. Sets realistic expectations for any claim-check feature.
3. **arxiv-sanity / arxiv-sanity-lite** — the *pivot* from full KG to lite is
   exactly the scope question Stage 2 faces. Worth reading the repo README /
   post-mortem before deciding H1 vs. H4/H5.

---

## 6. Failure patterns observed in prior art

Synthesized from both S1Bs §5.

- **Pattern A · Overconfident scientific-claim extraction destroys trust.**
  Seen in: Galactica (withdrawn 2022), adjacent in SCIVER/TaDA evaluations showing
  LLMs struggle on from-scratch claim verification. *Mitigation inferred by both
  debaters*: always show provenance, never assert without the source snippet, and
  give the user a low-friction "I disagree" override.
- **Pattern B · Complexity that doesn't pay for its maintenance cost.** Seen in:
  arxiv-sanity full version → simplified to arxiv-sanity-lite; the personal-KG
  wave (Roam/Logseq/Mem) where users worked more for the graph than the graph
  worked for them; ~27% of enterprise KG projects actually reach production.
  *Mitigation inferred*: do not ship a fixed ontology; let it emerge from user
  actions + embedding clusters; tolerate messiness.
- **Pattern C · Alert fatigue at ≥ few-per-day; trust loss at any false-urgent.**
  Seen in: PaperWeaver's explicit framing of the problem; clinical alert-fatigue
  literature (generalized mechanism). *Mitigation inferred*: default to digest,
  not push; no urgency flag without user whitelisting; measure precision, not
  recall.
- **Pattern D · Survivors specialize; generalists pivot or wither.** Seen in:
  Elicit (literature review), Undermind (deep search), ResearchRabbit (maps),
  arxiv-sanity (feed). No incumbent offers the full stack. *Lesson*: the
  "research cortex" framing is the graveyard; narrow is the live path.
- **Pattern E · Graph-exploration tools become "start-of-project" tools, not
  daily practice.** Seen in: Connected Papers and ResearchRabbit (both named
  by Opus as "I look at this twice when I start a new project"). *Lesson*:
  any product relying on graph-as-primary-surface risks low retention.
- **Pattern F · Session-based tools scale through use, but don't build memory.**
  Seen in: Elicit, Undermind, SciSpace. They start fresh every time; the user
  does not feel the tool "knows" them. *Opportunity / Opus + GPT shared framing*:
  persistent, delta-aware memory is the unfilled gap.

---

## 7. Daydream-vs-reality verdicts

Major claims from either S1A mapped against both S1Bs. **Bolded rows** = S1Bs
disagreed on the verdict or the claim was a shared-imagination miss.

| # | Original claim | Source | Opus S1B verdict | GPT S1B verdict | Consensus? |
|---|---|---|---|---|---|
| V1 | "Delta-aware summarization against personal KB is the payload" | Opus A (and GPT A in different words) | Stronger — no incumbent fills this | Stronger — "personal, delta-aware research memory" is the real novelty | Yes, both strengthened |
| V2 | "80% agreement between system top-5 and user post-hoc top-5 after 6 months" | Opus A | Unknown / invented — drop the number | Not addressed | Agreement to drop specific number; keep calibration framing |
| V3 | "MVP fits in a week" | Opus A | Weaker — only a *scoped* MVP fits in a week; grand version is 3–4 weeks honest | Weaker implicit — called out "grand form with 1-week target" as unlikely | Yes, both weakened |
| V4 | "Cheap inference is the unlock" | Opus A | Unchanged — still true but claim-extraction is multi-pass so per-paper cost is higher than implied | Not directly addressed | Partial — Opus refined, GPT silent |
| V5 | "Novelty/impact scoring is the hard part" | Both B | Validated by SCIVER 2025 | Validated — "novelty/impact assessment much less solved than summarization/retrieval" | Strong consensus: validated |
| V6 | "Ontology drift will poison the KB" | GPT B (Opus implied in B.2) | Strongly validated — ~27% KG production rate, "silent killer" industry framing | Not explicitly verified but implicit in "narrow stays coherent" recommendation | Consensus: validated |
| V7 | "Alert fatigue / trust loss is structural" | Both B | Validated — PaperWeaver names it, measured | Validated — scholarly recommender survey + clinical alert literature | Strong consensus: validated |
| V8 | "YC AI-summarizer startups pivoted to enterprise legal/biopharma" | Opus B | **Not verified — demote to anecdotal memory, may be wrong** | Not addressed | **Opus self-demoted; treat as unverified** |
| V9 | "arXiv ~400 cs/day, ~50-100 AI-relevant/day" | Opus A | Weaker — revised upward to 500-700 cs/day, ~100-200 AI-relevant | Not directly addressed | Partial — Opus refined; GPT's "high enough" non-quantified claim is trivially consistent |
| V10 | "PDF extraction is largely tractable" | Opus A | Stronger — Marker + GROBID stack works on a 4090 | Stronger — "parsing looks like engineering, not fantasy" | Strong consensus: validated |
| V11 | "The 'aha moment' is drag-in-PDF → auto claim-check table against the user's KB" | Opus A.2 | **Weaker — SCIVER 2025 shows LLMs struggle on from-scratch claim verification; the demo will work partially, not fully** | Partially weakened — "narrow verification supported, open-domain novelty/impact scoring overclaimed" | **Consensus: the *specific demo* Opus described is overclaimed.** Stage 2 must decide whether to keep this feature scope or narrow it. |
| V12 | "Semantic Scholar API is the citation-graph backbone" | Opus C | Updated — **OpenAlex is the right primary; S2 is secondary** | Consistent — both named and usable | Consensus with a refinement: OpenAlex primary |
| V13 | "One-user feedback loop is too thin to train a ranker" | Opus B.6 | Neither validated nor refuted — remains live risk. GPT's "taste from actions" framing gives partial answer | Not directly addressed | Unresolved; carry to Stage 2 |
| V14 | "Discovery + memory + synthesis are fragmented; fusing them is the unlock" | GPT A | Validated implicitly — no incumbent fuses all three; survivors specialize | Confirmed — "survivors specialize" finding | Strong consensus: validated |
| V15 | "Existing products are session-based, not persistent" | Opus B (and GPT A implicitly) | Validated — Elicit, Undermind, SciSpace all session-based | Not directly tested, but prior-art table is consistent | Consensus: validated |
| V16 | "The attention bottleneck is what actually needs solving, not awareness" | Opus B (epigram) | Carried forward into H5 "Reject-95%-Confident" | Not derived in GPT's path | **Opus-only framing**; Stage 2 should decide whether to adopt it. GPT did not independently re-derive the inversion. |
| V17 | "Tacit taste, local context, long-running technical memory" is what LLMs can't fake | GPT B | Adopted by Opus S1B §1 ("taste is learnable from actions") | Consistent with own S1B | Consensus: validated framing |
| V18 | "Plumbing will eat the week" | Opus B.4 | Validated — tool survey shows ingestion + normalization is days not hours | Implicit consensus — "plumbing is non-trivial" in Q3 finding | Consensus: validated |

**Flagged rows for Stage 2**:

- **V11** is the single largest daydream → reality correction. Opus's S1A
  described a concrete demo ("drag in a PDF, auto-get a claim-check table
  comparing against 6 prior works"). S1B shows this demo only partly works in
  2026 with current claim-verification research. Any Stage 2 direction that
  leans on this demo must either (a) narrow the claim-check scope, (b) accept
  adversarial failures loudly, or (c) be downgraded.
- **V8** is a fabricated pattern Opus self-demoted on reflection. Stage 2 should
  not assume the "startups pivoted to enterprise" pattern without real data.
- **V16** is genuinely divergent — only Opus reached the inversion. Stage 2
  should explicitly decide whether to weight "reject more" vs "surface more" as
  the product thesis.

---

## 8. What's genuinely novel (or genuinely empty)

After subtracting done-and-shipped and already-failed:

- **Done and shipped** (stay away): broad literature search (Elicit), deep
  iterative search (Undermind), visual lit maps (ResearchRabbit), personalized
  arXiv recommendations (arxiv-sanity-lite, Semantic Sanity), per-paper chat
  (SciSpace), lit-review tables (SciSpace, Elicit).
- **Tried and failed (or decayed)**: full personal-KG tools (Roam/Mem/Reflect
  failure pattern), static auto-generated ontologies (27% production rate),
  generic alert feeds (alert fatigue), overconfident science-LLMs (Galactica).
- **Standing ground — genuinely unfilled gap**:
  1. **Delta-against-personal-KB** — when a new paper arrives, compare its
     claims explicitly against the user's saved / flagged entries and surface
     contradictions or supersessions. No incumbent does this. Both S1Bs
     independently identified this as the novelty.
  2. **Taste-from-actions personalization** — the user's actions ("marked
     cooked," "saved," "starred for reproduction") train a per-user ranker, not
     a generic relevance model. Underserved in incumbents.
  3. **Claim-level provenance storage** — extract individual claims with their
     source spans, so contradiction detection has something to diff against
     and distrust is localizable. *Technically risky* per V11/SCIVER, but
     structurally unfilled.
  4. **Inverted framing — reject 95% confidently instead of surfacing 5%** —
     this was Opus-only; GPT did not re-derive it. Standing-ground *if* the
     operator buys the attention-bottleneck thesis.

**Verdict**: novelty is sparse but not empty. The space is crowded; the
unfilled gaps are narrow and specific. Two of the four (§8.1, §8.2) are
engineerable in 2026; one (§8.3) is technically risky; one (§8.4) is a thesis
choice.

This is *not* a Park / Abandon signal on its face — but it is a narrow-scope
signal. Any Stage 2 direction menu that re-expands to the grand "Research
Cortex" (H1 / Full Research Cortex in the hypothesis table) is reopening the
graveyard.

---

## 9. Hypothesis space after grounding

Merged from Opus S1B §7 (H1–H5) and GPT S1B §7 (4 named hypotheses).
De-duplicated and cross-referenced.

Mapping:
- Opus H1 "Grand Radar" ≈ GPT "Full research cortex" → merged as **H1**
- Opus H2 "Personal Delta-KB (narrow)" ≈ GPT "Weekly delta memo" → merged as **H2**
- Opus H3 "Claim-level Reader+Diff" ≈ GPT "Paper claim-checker" → merged as **H3**
- Opus H4 "Lab-Brief Generator" → **H4** (Opus-only)
- Opus H5 "Reject-95%-Confident" → **H5** (Opus-only)
- GPT "Personal triage feed" → **H6** (GPT-only, distinct from H5 inversion)

| # | Slug | One-line description | Proposed by | Evidence strength | Differentiation vs prior art | Solo 1-week feasibility | S1A foreshadowing |
|---|---|---|---|---|---|---|---|
| **H1** | Grand Radar / Full Cortex | All sources + unified ontology + SOTA map + push + proactive backfill + impact scoring | Both (Opus H1, GPT "Full research cortex") | Demand M, but failure patterns well-documented | M (Elicit can close parts of the gap) | **L** — Opus says 3–4 weeks honest; GPT says feasibility L | Both S1A Part A described this |
| **H2** | Personal Delta-KB (narrow) / Weekly Delta Memo | arXiv-only, 2 AI sub-areas, daily/weekly digest: "what changed vs your saved papers" | Both (Opus H2, GPT "Weekly delta memo") | Demand M–H | **H** — no incumbent ships personal-KB diff | **M–H** if scoped | Directly foreshadowed by Opus A (delta against personal KB) and GPT A (what changed against topic graph) |
| **H3** | Claim-level Reader + Diff / Paper Claim-Checker | Drag-in-PDF → extract claims → check against local claim DB → flag contradictions / missing baselines | Both (Opus H3, GPT "Paper claim-checker") | Demand M–H (one-use-at-a-time) | H (mechanism) but V11 says execution risk is high | **M** — depends on how well SCIVER-class extraction works in practice | Opus A.2 is the explicit "aha moment" demo |
| **H4** | Lab-Brief Generator | Weekly 500-word brief for *a specific lab agenda*, evidence-grounded from the week's top 50 arXiv; low-touch | Opus only | Demand M | M | **H** — very buildable in a week | Opus A.1 (Monday-morning-in-15-minutes) leans on this |
| **H5** | Reject-95%-Confident | Inverted radar: each morning show only the ~5 papers worth opening out of ~200, one-line reason each. Quiet by design. | Opus only | Demand H (if attention-bottleneck thesis buys) | H | **H** | Opus B.8 epigram — "tool cannot solve an attention problem" |
| **H6** | Personal Triage Feed | Source monitoring + high-precision alerts + short cited briefs (no KB diff layer) | GPT only | Demand H | L (closest to arxiv-sanity-lite + alerts) | **H** | GPT A general framing (compounding asset, trusted radar) |

**Self-reported rankings from the debaters** (recorded; Stage 2 does its own
ranking):

- **Opus S1B lean**: H5 > H2 > H4 > H3 > H1. Reason: inversion matches the
  attention-bottleneck thesis; H2 has defensible differentiation; H1 is "a
  2-month trap."
- **GPT S1B lean**: did not rank explicitly; implicit preference for narrow
  (triage feed / weekly delta / claim-checker) over Full Cortex. The GPT
  hypothesis table uses the same demand/differentiation/feasibility axes
  but doesn't pick a winner.

**Note for Stage 2**: H2 is the only option where both debaters independently
derived the same answer AND it has high differentiation AND it is
solo-feasible with scoping. H5 is the most philosophically distinct (the
inversion). H1 is the graveyard.

---

## 10. Cross-cutting concerns raised by either side

Surface-level coverage for Stage 2. Not all central, but Stage 2 must address.

- **Legal / ToS / licensing**: Opus C.3 #11 flagged arXiv ingestion licensing
  (permissive) vs top-lab blog ToS (often not). GPT's S1B confirmed arXiv has
  official API and OAI-PMH endpoints; blog scraping remains unaddressed.
  Stage 2 must decide whether blogs are in scope, and if so, how to handle
  ToS.
- **Ops cost / reliability**: Opus B.5 — ~50 full-paper reads/day + 3x cross-ref
  reads + daily re-rank. GLM5.1/Minimax2.7 pricing per-token unverified. Stage 2
  must back-of-envelope this with 2026 prices; claim-extraction is multi-pass
  so cost is higher than single-pass summarization.
- **Solo operator reality**: both S1Bs explicitly weakened the "1-week grand
  build" claim. Stage 2 must pick a scope the operator can actually ship in
  a week *without* implicit dependency on a "part 2" that never ships.
- **Competitive moat**: None inherent for H1. H2's moat is *the user's own
  KB* (switching cost = re-importing history). H5's moat is the *trust built
  by high-precision rejection* (hard to copy without user data). Stage 2
  should note: Elicit and Undermind can add a "personal KB diff" feature
  faster than a solo dev can build the base product.
- **Data / privacy / compliance**: one-user system, so low risk surface.
  Unaddressed: if the user starts feeding internal lab papers or unpublished
  drafts into the KB, that becomes sensitive. Stage 2 might want to decide
  whether local-only is the default.
- **Hardware realism**: 4090 + claimed GLM5.1/Minimax2.7 code-plan access.
  Opus S1A C.2 flagged "4090 is sufficient" as an unverified assumption.
  Stage 2 should not assume every embedding index fits.
- **Team vs solo use**: GPT S1A raised "discovery vs synthesis vs team-memory
  preservation" as distinct possible framings. Operator proposal says "我个人
  使用" (personal use). Stage 2 should confirm team-memory is *out* of scope
  for v1, even if tempting.
- **Inference-latency vs Twitter-speed**: Opus B.5 — if the pipeline lags
  arXiv by hours, social media scoops the product. Unresolved in S1B. Stage 2
  should decide whether real-time is a requirement (argues against H3 / full
  pipeline) or daily digest is sufficient (argues for H2 / H4 / H5).

---

## 11. What Stage 1 could NOT resolve

Questions that web search could not answer. These require outside action
(user interviews, prototypes, real pricing data, legal counsel).

1. **How the user actually makes research decisions today** (workflow details,
   cadence, decision triggers, failure modes in their current process).
   Opus C.3 #9 and GPT C "Whether the user's real need is discovery, synthesis,
   or team-memory preservation." — same unknown, different framings. **This is
   the largest unresolved question and is not web-searchable.**
2. **Exact 2026 per-token pricing** for GLM5.1 and Minimax2.7 via the operator's
   code plan. Cost envelope for continuous ~50-200 paper reads/day is unknown.
3. **Actual retention numbers** for Elicit / Undermind / SciSpace / arxiv-sanity
   — the 17-PhD rating gives quality, not retention. Useful but doesn't tell
   us "do researchers use this daily after month 3?"
4. **Whether a one-user ranker can be trained from a single user's actions**
   without collapsing to the user's prior beliefs. Folk theory on both sides,
   no empirical grounding.
5. **What the operator's AI lab is actually working on** (topics, baselines
   being tracked, which papers they'd historically have regretted missing).
   Required to scope H2 / H4 / H5 to 2 specific sub-areas.
6. **Whether GitHub trending signal can be filtered to AI-research relevance**
   without overwhelming noise. Operator proposal includes GitHub repos as a
   source; neither S1B tested this.
7. **Whether arXiv-sanity-lite's simplification was a *strategic narrowing*
   that worked, or a *reluctant fallback* from a failed full version**. Reading
   the repo README / Karpathy's post would help but wasn't done in S1B.
8. **Ontology coherence with light-touch curation at one-user scale** — the
   "27% KG production" number is enterprise-scale; no evidence on whether
   solo + narrow stays coherent.
9. **Exact claim-verification accuracy** a modern LLM achieves on 2026
   AI-research papers with a well-designed multi-pass prompt. SCIVER and TaDA
   are benchmarks, not production numbers on the operator's corpus.
10. **Whether the operator will actually use it daily** — Opus C.3 #10 flagged
    this as an unknown. No prior with this specific user. Only a real prototype
    answers it.

**Moderator-facing flag**: items #1 and #5 are the blockers. Stage 2 can debate
direction menus *without* these, but any direction it picks is provisional
until the operator provides (a) a short description of their current research
workflow and (b) names of 2–3 AI sub-areas they'd scope v1 to. Items #2, #3,
#9, #10 only get resolved after a prototype exists. Items #6, #7, #8 can be
debated but not settled in Stage 2.

---

## 12. Preserved disagreements

Explicit divergences between the two debaters that Stage 2 should see, not
smooth over.

| # | Disagreement | Opus view | GPT view | Evidence on each side |
|---|---|---|---|---|
| D1 | **"Reject 95%" inversion as a product thesis** | Opus advocates (H5) — the attention bottleneck is the real constraint, awareness amplification is the wrong frame | GPT did not derive this inversion; implicitly remained in the "surface useful things" frame | Opus has the epigram and the logical chain. GPT has no counter-argument, just didn't re-derive. Stage 2 must decide whether the inversion is a thesis or a lens. |
| D2 | **Whether personal ontology can stay coherent with light-touch curation** | Opus hopeful in S1A, updated skeptical in S1B ("let it emerge from user tags + embedding clusters, accept messy") | GPT skeptical from S1A Part B onward, not resolved in S1B | Both now lean skeptical, but neither has positive evidence for the light-touch path. |
| D3 | **Claim-level storage as the right data unit** | Opus advocates (H3); acknowledges SCIVER risk but keeps it in the hypothesis space | GPT more cautious; "open-domain novelty/impact scoring still looks overclaimed" but keeps claim-checker as a hypothesis | Not a hard disagreement — both keep H3 alive — but the confidence levels differ. |
| D4 | **Prior-art recall precision** | Opus named ~10 products from memory, mostly verified accurate | GPT named zero products from memory in S1A; caught up in S1B | Not a substantive disagreement but a reminder that imagination-phase recall differed sharply. Useful context for how much to weight each debater's "I remember X exists" claims. |
| D5 | **Cost / latency as a first-order concern** | Opus raised it (B.5), unresolved | GPT did not address it | Stage 2 should adjudicate — is hourly-scale latency a product killer, or is daily digest fine? |
| D6 | **Team-memory / lab-reading-list dimension** | Opus mentioned it late in A.5 (lab reading list becomes a routed product), then dropped it | GPT raised it as an explicit open question (discovery vs synthesis vs team-memory) | Stage 2 should decide whether team scope is in or out of v1. Operator proposal says personal; both debaters partially strayed. |

---

## 13. Recommendations for Stage 2 framing

**Focus areas Stage 2 should narrow toward**:

1. **Start the direction menu from H2 and H5, not H1.** H2 has the strongest
   consensus on differentiation; H5 is the most thesis-distinct. Both are
   1-week solo feasible when scoped. H1 (Grand Radar) is the graveyard and
   should be explicitly excluded from the direction menu unless S2 finds new
   evidence.
2. **Decide early whether H3 (claim-checker) is in the direction menu.** V11
   says the specific demo is overclaimed; SCIVER evidence says the capability
   is partial in 2026. If H3 is kept, the scope should be narrower than
   Opus A.2 described (e.g., "extract numeric claims + baselines, flag
   outdated baselines" rather than "full contradiction detection").
3. **Treat §11 items #1 and #5 (user workflow + scoping sub-areas) as inputs
   the operator must provide before S2 can fully converge.** Stage 2 can
   produce a conditional direction menu; the final direction requires operator
   answers.
4. **Explicitly confirm scope: single-user, personal, no team-memory in v1.**
   GPT's raised option deserves to be killed (or kept) on record.
5. **Adopt the "fuse discovery + memory + synthesis" framing (GPT A) as the
   positive anti-goal for evaluating directions.** Any direction that only
   covers one loop has to justify why the other two are not needed.
6. **Adopt "expensive ingestion, impressive dashboards, low behavioral change"
   (GPT B) as the named anti-goal.** Stage 2 should reject any direction where
   a year-in reviewer could accuse the product of it.

**≤3 sources worth deeper reading for both S2 debaters**:

1. **PaperWeaver (arxiv 2403.02939)** — names the alert/context failure mode
   empirically. Most directly relevant to the product-shape decision.
2. **SCIVER (ACL 2025)** — defines the 2025 state of LLM claim verification.
   Required context for any H3-adjacent direction.
3. **arxiv-sanity-lite (GitHub repo + Karpathy's history)** — the actual pivot
   from full KG to lite is the scope question Stage 2 is being asked to
   answer. Read it as a case study before ranking H1 vs H2/H4/H5.

**Suggested moderator injections before S2R1 (optional)**:

1. **Operator to provide**: 2–3 sentences on current Monday-morning research
   workflow (what they actually do today) and 2–3 AI sub-areas they would
   scope v1 to. This resolves §11 #1 and #5 and unblocks H2/H4/H5 scoping.
2. **Hard constraint reminder**: one-week solo build is the ceiling. Any
   direction that requires "week 1 is just plumbing" is out of scope
   regardless of how attractive week-4 looks.
3. **Framing nudge (optional)**: instruct Stage 2 to produce 2–4 directions
   that are *mutually non-dominant* on (demand × differentiation × feasibility),
   not a ranked list. The operator picks at the decision gate.

---

*End of Stage 1 synthesis. Stage 2 debaters should read §1–§4 to understand
the imagination baseline, §5–§8 to understand what evidence changed, and
§9–§13 to see the hypothesis space and open questions they are expected to
narrow.*
