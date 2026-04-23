# Idea 002 · S1A · Opus 4.7 Max · Daydream (no search)

**Timestamp**: 2026-04-22T14:19:55Z
**Search used**: NONE. This is imagination + memory only.
**Visibility**: I did NOT read GPT's S1A. `ls discussion/002/` returned empty at
the time of writing.

---

## Part A · Most-exciting version (POSITIVE pole)

It's late 2030. Chen, who runs a 15-person AI lab in Shanghai, starts her
morning the way she has for the past three years: she opens her Radar. Not
Twitter, not arxiv-sanity, not Semantic Scholar — the Radar. It is the thing
that knows what *she* knows, what her *lab* is working on, and what the
*field* did while she slept.

The top of the Radar is not a feed. It is a **three-paragraph morning
briefing**, written in the voice of a senior colleague who read everything
overnight. Paragraph 1: "Since yesterday, the state of the art on long-horizon
agent evaluation moved. Here is the one paper that moved it, here is why
(two-sentence claim), here is what the authors got wrong (one sentence), here
is what it means for your MoE-routing-for-agents project." Paragraph 2:
"Three papers arrived on topics you're tracking but weren't moved by.
Verdict: derivative of the Feb ICML paper you already read. Skippable unless
you want the specific benchmark they ran." Paragraph 3: "One anomaly. A
Chinese lab you've never tracked posted a repo with 2,400 stars overnight;
the code is real; the paper isn't out yet; here's what it seems to do; I've
queued a deep dive for tonight."

**The "aha" moment**: Chen realizes after one week that she hasn't opened
arxiv.org in five days and she's *more* current than she was when she read
it twice daily. Because the Radar isn't a feed — it is a **senior reviewer
who already filtered**. The 300 papers/day becomes 3, and the 3 come with
verdicts, not just abstracts.

The second "aha" is a month later. Chen's student Liu asks: "Is there
anything recent on speculative decoding for diffusion?" The Radar doesn't
just search — it replies: "You haven't asked about this before. I don't have
a mature topic for it yet. I found 14 candidate papers in the last 6 months,
clustered into 3 sub-threads. The most important is this NeurIPS 2030 paper,
but the real precursor is a 2023 ICLR workshop paper you wouldn't have
found via keyword. Should I open a topic and track going forward? Y/N."
She says yes. Two weeks later she has a topic page with a SOTA leaderboard,
a provenance graph showing which ideas beget which, and three active
researchers it's worth emailing.

Why this is dramatically better than today: today Chen's team reads papers
with three unstated questions: *is this novel?*, *is the claim real?*, *does
this matter for what I'm doing?* Each of those questions requires reading
the paper plus remembering every similar paper from the last 5 years. The
Radar makes the second and third question cheap, which means the lab spends
its reading budget on the *first* question — the genuinely novel stuff.
Conservatively that's a 3–5x multiplier on effective research throughput.

Why I believe this is *possible*. Three things, all in the last 18 months,
have crossed thresholds simultaneously:
1. Long-context models can now hold a lab's history + a paper + a knowledge
   graph in one call without retrieval games. A 1M-token context makes
   "read this paper *in the context of what this lab already did*" a single
   prompt, not a RAG pipeline.
2. Parsing + math rendering on arxiv PDFs is no longer the bottleneck.
   GROBID-class tools + VLM-based figure understanding are good enough that
   "what is the actual claim" can be extracted reliably.
3. The cost of running a model on a paper has dropped below the opportunity
   cost of a grad student reading it. If a good Haiku/GLM-class model costs
   pennies per paper, the economics of "read everything" flip.

The long-term vision is not a tool Chen uses. It is a **lab memory**. In
year 3, when Chen hires, new researchers don't "get up to speed" by reading
textbooks — they read *their Radar topic pages*, curated by 3 years of their
new lab's taste. In year 5, the Radar is writing the literature-review
section of the lab's papers and scoring the novelty of proposed experiments
against the 3-year-old decisions the lab made that the new grad student
doesn't know about yet.

---

## Part B · Most-damning version (independent NEGATIVE pole)

Setting Part A aside. Starting fresh, from honest skepticism.

**The structural reason this fails**: the binding constraint in research is
not *finding* interesting work. It is *judgment about what matters*. A tool
that ranks papers by "novelty × impact × utility" is automating the one
thing humans still get paid for. And the automation will be mediocre for a
long time. So the user ends up with a filter that is 70% as good as their
own taste, and the cost of disagreeing with it — re-checking what it dropped
— wipes out the savings. You end up running two filters (yours + the tool's)
instead of one, and you stop trusting either.

**The more damning version**: the user *does* trust it. Which means the user
stops reading skipped papers. Which means the user's taste stops developing.
Which means in 2 years the user is a worse researcher, not a better one,
because the tool has been training them on its own priors. The researchers
who don't use the tool have read 2,000 papers the tool-user hasn't. Some of
those 2,000 are the field-defining weird ones that a summarizer would have
flagged "low impact."

**The economic case against**. Let's be concrete. A grad student earns
$40k/year; a senior researcher $200k. Reading a paper takes 20 minutes for
abstract-level triage, 2 hours for a serious read. A lab reads maybe 200
serious papers a year, call it 400 hours, or $10k of senior time — cheap
relative to everything else the lab spends money on. The Radar has to be
cheaper *and* better to be worth the integration cost. Integration cost is
not trivial: it needs the lab's private notes, their in-progress work, their
taste. That's the kind of integration everyone says yes to in a demo and no
to in production because of data-exit risk. (Example the operator might
remember: Mem, Rewind, Augmend — tools that required "give me all your
context" hit slower-than-expected adoption curves for a reason.)

**Prior-art pattern match, from memory**:
- *arxiv-sanity* (Karpathy, ~2015): personal feed ranker. Still around. Still
  niche. The 10-year lesson: people want the tool to exist but don't want
  it *as their primary reading surface* — they want it as one of five tabs.
  That's a hobby project outcome, not a venture-scale one.
- *Connected Papers*: beautiful, used once per paper, never opened again.
  Demo-great, daily-use poor.
- *Semantic Scholar*: has the data, has the semantic layer, has institutional
  funding. What they haven't built in eight years is the "daily briefing"
  layer. Why? Because that layer is about *personalization*, and
  personalization requires trust that's hard to earn and easy to lose.
- *Elicit, Scite, Consensus, Scholarcy*: all exist, all are useful, none
  ate research. The pattern is: a tool that's "pretty useful" is a
  subscription that gets canceled in year 2 unless there's a forcing function.
- Internal lab wikis / Obsidian-with-plugins: the closest thing most labs
  actually have. Every single one I've heard described has the property that
  the person who set it up maintains it and nobody else contributes. The
  Radar is that, with a more ambitious UI and the same social problem.

**The thing I'd tell a founder**: Build it for yourself for 3 months without
showing it to anyone. If you still open it daily at week 12, you have
something. If you don't — and you won't, because *you* know your taste
better than any model does — then the honest version is a personal research
tool, not a product. Personal research tools are great to build and they
don't need a debate.

**The regulatory/ethical edge**. Downloading, parsing, and storing every
arxiv paper is fine. Downloading, parsing, and storing every major lab's
blog — especially summarizing it in ways that don't preserve attribution —
is a gray zone that gets grayer as AI labs get more protective of their
outputs. The Anthropic/OpenAI/DeepMind blogs are increasingly written as
publishable statements with implicit "don't paraphrase me incorrectly"
clauses. A tool that paraphrases them at scale has a legal exposure that
scales with success. GitHub repos: fine. Blogs: ambiguous. Slack / internal
docs / Twitter threads of researchers: absolutely not.

**The taste problem, stated bluntly**. "An agent that learns my research
preferences from my X activity + my chats + dialectical arguing" sounds
great. It's also exactly the feature every *failed* personalization product
has promised. The reason it fails: taste isn't a function of observed
behavior, it's a function of *deliberated rejections* that are never logged.
You don't tell your tool "this paper is not interesting because I decided
8 months ago that diffusion-for-protein-folding isn't our comparative
advantage." You just don't click. The tool can't distinguish "didn't see"
from "saw and rejected" from "saw and wanted to read but forgot." And
without that signal, the personalization plateaus.

---

## Part C · Epistemic honesty — what I'd actually need to know

I just wrote two imaginative passages. Some of it is intuition that tracks
things I've actually encountered; some is confabulation that sounds good.
Sorting it out honestly:

### C.1 Claims backed by real confidence

- **Claim**: Long-context models can hold a paper + a lab's history in one
  call. **Source**: direct. I am a long-context model; I know the regime. Not
  speculative.
- **Claim**: Cost per LLM read of a paper is <$0.10 on small/cheap models.
  **Source**: Direct domain intuition from pricing I've encountered. Order
  of magnitude confident; exact numbers will drift.
- **Claim**: arxiv-sanity exists, is niche, is still around. **Source**:
  I've seen it referenced repeatedly. High confidence it exists and is
  niche; low confidence on whether it's actively maintained in 2026.
- **Claim**: Connected Papers is demo-great, daily-use poor. **Source**:
  personal intuition from having encountered descriptions of it plus the
  general pattern for graph-viz tools. Medium confidence.
- **Claim**: Research labs do have ad-hoc Obsidian/Notion setups that
  decay. **Source**: domain intuition — this is a well-documented
  organizational pattern. High confidence in the pattern, but I can't cite
  a specific study.
- **Claim**: Semantic Scholar has institutional funding and data but
  hasn't built a personalized daily briefing layer. **Source**: general
  awareness. Reasonable confidence on the data/funding part; I am less
  sure what SemScholar's product roadmap actually looks like today.

### C.2 Claims that are assumptions I haven't tested

- **Assumption**: A 3–5x research throughput multiplier is achievable. I
  wrote this confidently but it's made up — I have no benchmark, no study,
  no shipped product data. It's a plausible number, nothing more.
- **Assumption**: "Daily briefing" format outperforms feed format for
  researchers. I believe this but it's aesthetic intuition, not evidence.
- **Assumption**: 300 papers/day on arxiv. The real number as of now is
  almost certainly in that order of magnitude but I should verify.
- **Assumption**: Mem/Rewind/Augmend hit adoption friction due to data-exit
  concerns. I may be pattern-matching rather than recalling specific facts.
  Could be misremembering which tool had which problem.
- **Assumption**: Anthropic/OpenAI/DeepMind blogs have increasingly
  restrictive implicit usage norms. This is a feeling, not a verified claim.
- **Assumption**: A 24GB 4090 machine can meaningfully participate in the
  inference pipeline (ingesting, OCR, small-model triage). Directionally
  yes, but the specific model sizes that fit and are useful need checking.
- **Assumption**: The user's stated timeline ("半年到1年 with 1 architect +
  6-7 junior engineers") is compatible with the scope. This is their self-
  estimate; I have no basis to confirm or deny it.

### C.3 Known unknowns

- **How many papers/day arxiv CS actually sees in 2026**, after the AI-
  generated-paper wave and the publisher pushback.
- **What moderate-quality paper parsers cost** in 2026 — specifically, is
  LaTeX-source parsing available (arxiv offers source), and does that make
  the figure/math extraction problem easy or still hard?
- **What the state of open-source "paper-read-by-LLM" tooling is in 2026** —
  specifically, projects like paperqa, paper-qa, arXiv-sanity-lite, zotero
  plugins that use LLMs. Have any matured?
- **Whether the user's "8-15 topics" scope is the right unit**. Most research
  tools try to be topic-agnostic; pinning to 15 topics is either a clever
  simplification or a premature commitment.
- **Ground-truth usage patterns** — does a senior researcher actually want a
  3-paragraph morning briefing, or do they want a raw ranked feed? I don't
  know. This is a product question I can't answer from first principles.
- **What happens when the tool encounters paywalled content** (blogs with
  logins, bioRxiv/medRxiv, IEEE conferences). Is the recall on open-access
  sources enough, or does the 20% of closed content contain 80% of the
  value?
- **The X/Twitter-based taste-learning idea** — is X still where researchers
  post in 2026, or has the field migrated to Bluesky, Mastodon, or
  Discord? If the signal source moved, the taste-learning approach needs a
  different data spine.
- **The graveyard of AI-news / research-aggregator tools** — I'd want the
  full list of what's been tried and died since 2020, not just the ones I
  happen to remember.

### C.4 Five search-shaped questions for S1B

1. `"arxiv daily paper count 2025 site:arxiv.org OR site:github.com"`
   (goal: ground-truth the volume. Is it 300/day or 800/day in CS? Is it
   growing? Has the rate shift from AI-generated submissions affected it?)

2. `"research paper recommendation tool shutdown OR acquired" 2022..2026`
   (goal: graveyard. Which tools like Scholarcy, Iris.ai, Yewno, Scinapse,
   Meta's Galactica retrieval layer, arxiv-sanity-lite, paperswithcode's
   trending feature, etc. have died or pivoted? Why?)

3. `paperqa OR "paper-qa" OR openreview API OR zotero LLM plugin 2026`
   (goal: state of open-source LLM-on-papers in 2026. If there's a mature
   extraction pipeline I can stand on, scope shrinks enormously.)

4. `"research radar" OR "lab knowledge base" personalized recommendation
   case study adoption`
   (goal: find any published case study — academic or industry — of a lab
   actually deploying something like this and measuring time saved or
   research throughput. Any evidence that "3-5x throughput" has any
   empirical footing.)

5. `arxiv OR "scholarly publisher" scraping terms of service 2025 AI
   agent crawling`
   (goal: the legal/ethical surface. What does arxiv allow? What do
   SemScholar and OpenAlex allow? What are major AI-lab blogs' recent
   statements about automated summarization?)
