# Idea 001 · S2R1 · Opus 4.7 Max · Position (cooperative)

**Timestamp**: 2026-04-22T12:18:00Z
**Posture**: cooperative (Stage 2). Goal is a direction menu of 2–4 mutually non-dominant peers, not a winner pick.
**Read before writing**: `001-stage1-synthesis.md` (primary), PROTOCOL.md, both S1A + both S1B, no moderator notes (none exist). Ran 2 targeted searches to tighten two questions left open by synthesis §11 (arxiv-sanity-lite's pivot nature, Elicit/Undermind's current alert/library surface).

---

## §1 · What I now believe the idea actually is

After Stage 1, the "Research Radar" as proposed is three separable products wearing one name. The synthesis §8 made this concrete: the crowded ground is done (literature search, visual maps, personalized arXiv feeds, per-paper chat, alerts with library), the failed ground is marked (personal-KG maintenance, overconfident science-LLMs, "universal" aggregators), and only narrow gaps remain. The idea is most honestly described as:

> **"A single-user, persistent, delta-aware assistant that — over time — builds a sparse model of *what this specific lab lead believes*, then shows them what changed this week relative to that model."**

Key words: **single-user** (not team), **persistent** (not session-based like Elicit/Undermind), **delta-aware** (changes-vs-held-beliefs, not fresh relevance rankings), **sparse model of beliefs** (not a full ontology that drifts), **shows what changed** (not ranks everything).

Two newly-grounded adjustments to the S1B framing:

- **Adjustment 1 (from S2 search, tightens §11 #7)**: arxiv-sanity-lite's simplification was *strategic narrowing* — Karpathy's own framing was "core value prop, less likely to go down, scales better." This is evidence for a narrowing-as-feature strategy, not evidence that the full version was abandoned in despair. We should frame H2/H4/H5 as *deliberately narrow*, not *narrow because we can't do the grand version*. Different story the operator tells themselves; matters for motivation on month 3.
- **Adjustment 2 (from S2 search, tightens synthesis Pattern F)**: **Elicit now ships "Alerts + Library"** on Pro/Team/Enterprise. Saved papers, unread flags, relevance-ranked feed. Undermind ships topic-monitoring alerts. The **"session-based vs persistent"** framing from S1B is partly out-of-date: they have the *containers* (library, alerts), they don't have the **delta-vs-your-beliefs layer**. This sharpens the gap: our novelty is not "we save papers and alert you" (that's Elicit Alerts in 2026). Our novelty is "we compute and show the *diff between this week and your held KB state*." That is the surface no incumbent has.
  Sources: [Elicit Alerts blog](https://elicit.com/blog/introducing-elicit-alerts), [Elicit Alerts support](https://support.elicit.com/en/articles/6546881), [Undermind](https://www.undermind.ai/).

## §2 · Honest Y/N on "should this be built"

**Conditional Yes.** Build it if and only if:

1. Scope is ≤1 week of actual work and stays at a *narrow* cut from the start (H2 / H4 / H5 class, never H1).
2. The operator accepts that v1 replaces roughly **one weekly ritual**, not an entire "how I keep up with AI" workflow.
3. The operator can provide, before spec: (a) 2–3 sentences on current Monday-morning workflow (synthesis §11 #1), and (b) 2–3 scoped AI sub-areas (synthesis §11 #5). Without these the direction is a guess.
4. The anti-goal from GPT S1A is adopted as a hard kill-switch: *if a year-in reviewer could call this "expensive ingestion, impressive dashboards, low behavioral change," we abandoned too early.* Every direction below must have a plausible month-6 behavioral KPI.

**Don't build as-proposed.** The proposal's Grand Radar (H1) is the graveyard per synthesis §6 Pattern D; this S2R1 treats H1 as out of scope.

**"Instead do X" alternative** (documented, not recommended): if the operator actually wants to keep up with AI research rather than build a tool, the honest option is "subscribe to 3 curated newsletters + 1 hour of focused arXiv reading Monday morning + accept losing some signal." This is the null hypothesis; any direction below must beat it on month-6 behavioral change.

## §3 · Candidate directions (2–4 mutually non-dominant peers; not picking)

Constructed to be **non-dominant**: each is best on at least one axis and nobody is strictly better than another. I pruned H1 (graveyard), H6 (Personal Triage Feed = Elicit Alerts in 2026, differentiation L per synthesis), and folded H4 into D3 as a lower-ambition variant.

### Direction D1 — **"Personal Delta Memo"** (was H2 + lite framing)

**One-paragraph description**: A **daily** job (not push; a digest at a fixed time) that ingests the day's arXiv cs.AI-subset papers *for the 2–3 scoped sub-areas only*, compares them against a small personal KB of papers the user has flagged as "this matters to me" / "this is the current baseline I track," and surfaces **only the ~3–7 papers that create a delta**: new SOTA on a tracked benchmark, a claim that *contradicts* something in the saved KB, or a paper that *supersedes* a saved entry. Each delta carries a one-line explanation ("paper X claims +4.2 over baseline Y which is a 2024 result; current strongest on your tracked benchmark is Z"). The user has a 3-button interface: **"now in my KB"** / **"noise"** / **"read fully later."** Their clicks train the per-user ranker over weeks.

**Risk**: the delta computation is only as good as the KB's structure. If we store papers as blobs the diff is weak; if we try to extract fine-grained claims we hit SCIVER-class failure (synthesis V11). **Mitigation**: store at *claim-subset* granularity — numeric benchmarks, method-type tags, stated comparison baselines. These are extractable with high precision from abstract + intro + experiments table (no need for from-scratch open-domain novelty detection). Narrow the claim-ontology; accept that impact scoring is out of scope.

**Target user**: the operator specifically. A lab lead with an existing sense of "what I care about" and willingness to seed the KB with ~20 papers.

**Survival angle**: incumbent gap is real and confirmed by both debaters. The switching cost *is* the user's accumulating personal KB — it grows into a moat for the product over months. Elicit Alerts + Library is adjacent, not equivalent: they show "new papers matching your saved query," not "diff vs your believed-state."

**Month-6 behavioral KPI**: user replaces one existing behavior (arXiv-skim Monday, or "ask student to tell me about X," or Twitter scrolling for papers) with the Delta Memo. Measured as "did they read the memo ≥3 days/week on weeks 18–24?"

### Direction D2 — **"Claim-Check on Drag-In"** (was H3, narrowed per synthesis V11)

**One-paragraph description**: Not a radar at all. A **single-action tool** — operator drops in a new paper (PDF or arXiv URL), and within ~60 seconds the system returns a **checklist report**: (a) the baselines this paper reports against, (b) whether those baselines are the current strongest on the relevant benchmark (pulled from papers-with-code-style tracked tables + OpenAlex citation recency), (c) the 5–10 most-related saved papers in the user's KB with 1-line "how they relate" annotations, (d) a flag if the paper's headline numeric claim is within noise of an older result (configurable threshold). Scope **explicitly excludes** open-domain novelty judgment (unsolved per SCIVER 2025) and impact prediction.

**Risk**: cost per invocation is the highest of any direction (extract + ground + compare). Also: the drag-in-a-paper action happens maybe 2–5 times/week for a lab lead — lower usage frequency than the other directions, so month-6 retention looks different.

**Target user**: the operator when they receive a paper from a colleague / student and need a fast orientation. Single-purpose but high-value-per-invocation.

**Survival angle**: highest per-use value. Most directly addresses the V11 "aha moment" from S1A once narrowed. No incumbent offers "check this paper against my saved baselines." SciSpace does per-paper chat, not cross-reference-against-user-KB. Elicit does literature review, not "validate this specific paper against my tracked state."

**Month-6 behavioral KPI**: user trusts the report enough to decide *not to read* a paper ~30% of the time (i.e. the report becomes load-bearing for a pass/fail decision).

### Direction D3 — **"Monday Lab-Brief"** (was H4, slightly upleveled)

**One-paragraph description**: A **weekly** 500–800 word brief generated Sunday night and delivered Monday 8am. Inputs: the week's arXiv activity in the 2–3 scoped sub-areas + any saved-paper activity in user's KB. Output: a structured doc — (1) "the 3 papers that mattered this week for your agenda" with 2-sentence why-it-matters each, (2) "the benchmark that moved" (one line if nothing moved), (3) "the thread you should pull" (an open question or emerging disagreement worth 15 minutes of reading), (4) a **questions-for-your-students** section (3 prompts derived from the week's deltas that the operator can drop into a lab meeting). Intentionally low-frequency, intentionally prose, intentionally short. No dashboards.

**Risk**: prose-brief quality is floor-limited by the LLM's synthesis ability + the quality of the tracked benchmark data. A bad brief in week 3 kills trust more than a bad alert (higher stakes per delivery).

**Target user**: the operator in "running a lab" mode, not "reading papers" mode. The brief is *team-facing utility* (lab meeting prompts) without being a team product — it gives the operator material to use with students.

**Survival angle**: closest to "behavioral change > dashboard" anti-goal. The brief either changes what the operator says at Monday lab meeting or it doesn't; the test is crisp. Also highest solo-1-week feasibility per S1B rankings.

**Month-6 behavioral KPI**: operator uses one or more of the brief's lab-meeting prompts ≥50% of weeks.

### Direction D4 — **"Reject-95%-Quiet-Radar"** (was H5, kept)

**One-paragraph description**: Inversion thesis. Every morning at 6am, the system reads ~100–200 new cs.AI-subset papers and shows *only the ~5 that pass a high-precision filter* — one line each, one reason each ("matches your tracked topic X + beats saved-baseline Y" / "contradicts your saved entry Z"). If zero papers pass, it says "zero today" and sends nothing. **The UX's central promise is low volume, never high volume.** User interactions — "no this wasn't useful" / "this was exactly right" — adjust the per-user threshold over weeks.

**Risk**: the philosophical distinctness of "reject more" is a thesis bet; if the operator *actually* wants "surface more" (some people do — they like the flood), D4 is wrong for them. Also, false-negative cost is invisible (user doesn't know what they missed), so calibration requires explicit spot-check audits (e.g., every 4 weeks, show the user 20 random rejected papers and ask "any of these important?").

**Target user**: specifically an operator who agrees with the attention-bottleneck thesis from my S1B §5 / Opus S1A Part B.8. Not for everyone; a thesis bet.

**Survival angle**: the only direction that reframes the problem as *too much, not too little*. Every incumbent is solving the "too little" problem with better filtering. This solves "too much" by ratcheting precision, not recall. Uniquely positioned if the thesis is right, dead weight if it's wrong.

**Month-6 behavioral KPI**: operator stops doing their current morning-arXiv-scan habit entirely and relies on D4 alone. Binary test.

---

### Non-dominance check

| Direction | Strongest on axis | Weakest on axis |
|---|---|---|
| D1 Personal Delta Memo | Differentiation (no incumbent delta-vs-belief) | Cost / claim extraction complexity |
| D2 Claim-Check on Drag-In | Per-use value; single-purpose clarity | Usage frequency (low; month-6 retention uncertain) |
| D3 Monday Lab-Brief | 1-week solo feasibility; behavioral-change clarity | Differentiation vs Elicit + human curation |
| D4 Reject-95%-Quiet-Radar | Thesis distinctness; moat on calibration trust | Thesis bet — wrong if operator wants "more not less" |

No direction strictly dominates another. D1 vs D3 is "effort vs ambition"; D2 vs D1 is "per-use depth vs per-day persistence"; D4 vs all is a thesis fork.

---

## §4 · Direction I lean toward and why (honest, not neutral)

**D1 (Personal Delta Memo), leaning strongly.** Subject to the operator's answers to synthesis §11 #1 and #5.

Why:

1. **Consensus strength from S1**: D1 is the only direction where both debaters independently derived the same answer AND synthesis §9 table shows it as the cell with high differentiation AND 1-week feasibility-with-scoping.
2. **Addresses the largest unfilled gap**: synthesis §8.1 names "delta-against-personal-KB" as the single sharpest unfilled novelty. Elicit Alerts is adjacent, not equivalent — the S2 search confirmed this. D2, D3, D4 either lean on weaker novelty (D3 adjacent to Elicit + newsletters) or on a thesis bet (D4) or have a lower-frequency surface (D2).
3. **Compounds into a moat**: the user's personal KB becomes the switching cost. D2 and D3 don't accumulate this way (D2 is stateless per-drag; D3 is a fresh weekly brief).
4. **Best test of the GPT anti-goal**: "did behavior change?" is testable month-6 — did they replace Monday-arXiv-skim or not. D1 forces this test more directly than D3 (which can become "nice to read" without changing behavior) or D2 (which may be a 3x/week tool rather than a daily one).

What makes me **not** pick it outright (why I lean, not declare):

- The claim-extraction-at-benchmark-granularity assumption in D1's mitigation is plausible but I don't have 2026 precision numbers for "extract reported baseline + headline metric + benchmark name" on real arXiv cs.AI papers. If that extraction is <90% precision, the delta computation will misfire visibly, and user trust is the moat — so breakage here breaks the whole thing.
- D4 is my *philosophical* preference per S1B §7. If the operator buys the attention-bottleneck thesis, D4 > D1. Synthesis D1 disagreement (Opus-only inversion) is unresolved and the operator is the tiebreaker.

**Honest ranking**: D1 > D4 > D3 > D2. D2 lowest because daily persistence beats per-use for this operator's stated need ("持续跟进前沿研究"). D4 second-highest *only if* the operator validates the thesis.

## §5 · Deltas since S1B

- **Dropped H6 entirely** (Personal Triage Feed): the S2 search confirmed Elicit Alerts shipped precisely this shape; no differentiation survives.
- **Downgraded H1** (Grand Radar): synthesis §8 failure patterns + Pattern D ("survivors specialize, generalists pivot or wither") make it a soft-abandon in S2R1. Not killed — if the operator insists, the debate can carry it, but I now treat it as dominated by D1+D3 together.
- **Reframed arxiv-sanity-lite**: from "reluctant fallback" to "strategic narrowing" (from the S2 search). This is evidence *in favor of* D1/D3/D4 all, as deliberate-narrow-ship strategies rather than compromises.
- **Sharpened D1's novelty**: not "persistent vs session" (Elicit already persistent via Library + Alerts), but *"diff vs believed state" vs "filter against saved query"*. This is a narrower and more defensible claim.
- **Added explicit month-6 behavioral KPIs** for each direction, per GPT anti-goal. These were implicit in S1B §3.

## §6 · Moderator injection response (if any)

No `001-moderator-notes.md` exists at time of writing.

---

### One open question for the moderator

Synthesis §11 flags items #1 and #5 as non-web-searchable and blocking for a final direction pick. Concretely:

> **Operator: in 2–3 sentences each, (a) what do you do on Monday morning today to stay current (tools, URLs, cadence, what triggers a "I should read this" decision)? and (b) name the 2–3 AI sub-areas that v1 should cover.**

Without these, S2R2 can refine the menu but any S3 direction lock is guess-work. Noting this so the moderator can decide whether to inject or let S2R2 converge the menu first.

---

*End of S2R1. Menu has 4 non-dominant peers (D1–D4); I lean D1 conditional on operator workflow input; 1 open question for moderator.*
