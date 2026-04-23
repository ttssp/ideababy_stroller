# Stage 2 Checkpoint — Idea 001 · Research Radar

**Prepared for moderator**: decision required before Stage 3.
**Debate status**: mature — 2 S2 rounds per side, menu stable across rounds, debaters converged.
**Debaters' honest verdicts on "build or not"**:
- **Opus**: Conditional Yes — build iff scope stays narrow (≤1 week, H2/H4/H5 class, never H1), v1 replaces one ritual, and operator provides current-workflow + sub-areas before spec.
- **GPT**: Conditional Yes — build iff one ritual replaced, single-user, sparse state, no open-domain novelty, behavioral test by month 2–3; otherwise use existing alerts + disciplined reading.
- **Agreement**: yes, strong. Both say "Yes, conditionally" and "No, as originally framed." Both name the same conditions, same hard kill (Grand Radar H1 = graveyard), same anti-goal ("impressive dashboards, low behavioral change").

---

## 0. OPERATOR-INPUT BLOCKER — read first

Both debaters independently flagged, in both S2R1 **and** S2R2, the same two
non-web-searchable questions as the real tiebreaker between D1/D2/D3/D4. Opus
S2R2 stated it plainly: the checkpoint decision turns on "one question that
neither debater can answer." These are **inputs to the decision in §4**, not
side-notes:

**Q-A · Which existing ritual does v1 replace?** (pick one)

| Answer | Maps to direction |
|---|---|
| Morning arXiv skim | **D1** (or **D4** if you also buy the attention-bottleneck thesis) |
| Forwarded-paper orientation (student/collaborator sends a PDF) | **D2** |
| Monday lab review / weekly reading ritual | **D3** |
| "I want volume reduction, not awareness amplification" | **D4** |

**Q-B · Which 2–3 AI sub-areas should v1 cover?** (e.g. long-context LLMs +
agentic tool-use; or diffusion-video + robot policies; etc.)

Both sub-areas are required regardless of which direction is picked — they
scope the ingest, the tracked-baselines list, and the anchor-paper seed set.
Without them, "v1" has no corpus.

**Moderator action**: answer Q-A and Q-B in `001-moderator-notes.md` before
(or concurrent with) choosing §4. The Advance options are conditional on Q-A;
any Advance option requires Q-B to start Stage 3.

---

## 1. Unified direction catalog (4 pure + 1 hybrid)

Both debaters **converged on the same 4-direction menu across two rounds**.
Wordings differ; shape is identical. I unify the slugs below and cite the
naming from both sides. No new directions added (per instruction); no direction
dropped.

### Direction D1 — Belief Delta Brief

**Surfaced by**: both, S1B onward (synthesis H2).
- Opus naming: "Personal Delta Memo" (S2R1) → "Belief Delta Brief" (S2R2, adopting GPT's phrasing).
- GPT naming: "Belief Delta Brief" in both S2R1 and S2R2.
- Consensus: **strong** — both debaters name it as their center of gravity in both rounds.

**User**: the operator specifically — a lab lead with a pre-existing sense of "which baselines I care about" and willingness to seed a small KB with ~10–50 anchor papers.

**Value prop (one line)**: Daily digest that answers "what changed in the 2–3 sub-areas I track, relative to what I already believe?" — not "what new papers were published."

**Core mechanism**: Ingest day's arXiv cs.AI-subset for scoped sub-areas → compare against sparse state (anchor papers + tracked benchmarks + user-action log) → surface only papers that create a delta (new SOTA on tracked benchmark / contradicts saved entry / supersedes saved baseline). Output: 3–7 items/day with one-line "why this matters vs what you saved" + 3-button interface (in-KB / noise / read-later).

**How it differs from prior art**: Not "filter against saved query" (Elicit Alerts does that in 2026). **"Diff vs believed-state"** — the comparator is the user's held KB, not a topic filter. No incumbent ships this layer.

**What must be true for this to work**:
- Extraction precision ≥90% on `(benchmark, baseline, headline metric)` from abstract + intro + experiments table. Narrow claim-ontology, not open-domain.
- Operator seeds and tends the KB enough to give the diff something to compare against. ~20 anchor papers to start.
- Operator accepts "delta" as the surface of value, not "coverage."

**Biggest remaining risk**: extraction precision. If <90% on the narrow benchmark-structure task, false-positive "supersessions" accumulate and trust-breakage is terminal (the user's trust *is* the moat). Mitigation: keep extraction narrow (numeric headline + named baselines only, never open claim extraction); ship with on-by-default "flagged as delta — confirm?" verification for first 4 weeks.

### Direction D2 — Paper Context Card

**Surfaced by**: both, S1B onward (synthesis H3, narrowed from "Claim-Checker" per V11).
- Opus naming: "Claim-Check on Drag-In" (S2R1) → "Paper Context Card" (S2R2, adopting GPT's phrasing).
- GPT naming: "Paper Context Card" in both S2R1 and S2R2.
- Consensus: **strong** on shape; both explicitly narrowed scope away from S1A's "auto claim-check table" (overclaimed per SCIVER 2025).

**User**: the operator when a paper arrives from a student / collaborator / social feed and they need a 60-second orientation before deciding whether to read.

**Value prop (one line)**: "Drag in one paper, get a compact card: most-related saved papers, likely baselines, whether those baselines are still strongest, obvious missing comparisons."

**Core mechanism**: PDF/URL → extract (Marker) → ground against user KB + OpenAlex → 60s report with (a) baselines this paper reports against, (b) whether those baselines are current strongest, (c) 5–10 most-related saved entries with "how they relate," (d) flag if headline claim is within noise of older result. **Explicitly excludes** open-domain novelty judgment and impact prediction.

**How it differs from prior art**: SciSpace offers per-paper chat; Elicit offers literature review. Neither compares the dropped-in paper against the user's personal saved state. Context is personal, not generic.

**What must be true for this to work**:
- Same narrow extraction precision as D1 plus robust KB-neighbor search.
- Lab lead actually receives 2–5 forwardable papers/week (if 0–1, D2 starves).

**Biggest remaining risk**: usage frequency. 2–5 invocations/week is the ceiling for a lab lead; month-6 retention is ambiguous if D2 is the only touchpoint (user forgets the tool between uses).

### Direction D3 — Monday Lab-Brief

**Surfaced by**: both, S1B onward (synthesis H4 originally Opus-only, GPT adopted in S2R1).
- Opus naming: "Monday Lab-Brief" in both S2 rounds.
- GPT naming: "Monday Research Memo" in both S2 rounds.
- Consensus: **strong** on shape and cadence.

**User**: the operator in "running a lab" mode, not "reading papers for myself" mode.

**Value prop (one line)**: A 500–800 word prose brief delivered Monday 8am, built on the prior week's arXiv activity in scoped sub-areas — intentionally low-frequency, intentionally prose, intentionally short.

**Core mechanism**: Sunday-night job reads week's arXiv + KB activity → structured brief: (1) 3 papers that mattered this week for your agenda + 2-sentence why each, (2) benchmark that moved (or "nothing moved"), (3) thread worth pulling (open question / emerging disagreement, ~15 min reading), (4) 3 lab-meeting prompts. No dashboards.

**How it differs from prior art**: Closest analog is a good curated human newsletter (Alphasignal, Jack Clark's Import AI). D3's differentiation is *personal scope* (your 2–3 sub-areas, your saved papers, your benchmarks) and *prompts for your team* (lab-meeting questions you can drop in). Prose artifact, not dashboard.

**What must be true for this to work**:
- Prose quality stays high on week 3, 10, 25. A bad brief kills trust faster than a bad alert.
- Operator has a weekly ritual worth aligning to (Monday review, lab meeting).

**Biggest remaining risk**: differentiation is the weakest of the four — curated human newsletters exist and are good. The product must beat them on personal scope, not just match them on format. And "polished but non-essential" is exactly the anti-goal from S1B.

### Direction D4 — Quiet Gatekeeper (Reject-95%)

**Surfaced by**: Opus in S1B (H5, inversion thesis; synthesis §12 D1 noted this was Opus-only); GPT adopted in S2R1 ("take seriously after S1 synthesis").
- Opus naming: "Reject-95%-Quiet-Radar" (S2R1) → "Quiet Gatekeeper / Reject-95%" (S2R2).
- GPT naming: "Quiet Gatekeeper" in both S2 rounds.
- Consensus: **qualified yes** — both keep it in the menu as a thesis fork, not a debate tiebreaker. Neither will choose it over D1 without operator confirmation of the attention-bottleneck thesis.

**User**: an operator who agrees that their pain is **too much input, not too little discovery**. Thesis bet.

**Value prop (one line)**: Morning job reads 100–200 papers, returns only 0–5 that clear a high-precision bar; "zero today" is a valid output. UX promises *low volume*, never high volume.

**Core mechanism**: Same ingest + narrow-extraction stack as D1, but the default is *reject* unless conditions A + B + C all hold (matches tracked topic + beats saved baseline OR contradicts saved entry + passes calibration threshold). User feedback ("not useful" / "exactly right") tunes the threshold. Quarterly audit required: 20 random rejected papers shown to operator labeled "rejected — any of these important?" to recalibrate.

**How it differs from prior art**: Every incumbent solves "too little" with better filtering. D4 reframes the problem as "too much" and wins on precision + silence. Uniquely positioned *if the thesis holds*; dead weight if the operator wants "more, not less."

**What must be true for this to work**:
- Operator genuinely agrees with the attention-bottleneck framing (synthesis §12 D1 notes this is Opus-derived, not independently re-derived by GPT in Stage 1 — it's a live thesis question).
- Threshold calibration is robust; quarterly false-negative audits are non-negotiable.

**Biggest remaining risk**: false-negative invisibility. If we reject a paper the operator would have wanted, we never learn organically. Without the audit loop, overconfidence compounds.

### Direction D1 + D2 Hybrid — Belief Delta + Context Card (composable bundle)

**Surfaced by**: Opus S2R2 only (§3 hybrid note, §5 deltas). GPT did not surface the hybrid explicitly, though GPT S2R2 §4 describes its center of gravity as "the contextualized-state family ... D1 and D2 together as a product logic" — functionally equivalent framing, different articulation.

**Why it composes**: D1 and D2 share the same state-model and the same extraction stack (narrow benchmark-structure extraction + KB-neighbor search). D1 uses them in a daily batch job; D2 uses them in an on-demand single-paper invocation. Incremental complexity of adding D2 to a D1 system is meaningfully less than building D2 standalone. D3 and D4 are **not** composable this way.

**Phasing**: D1 as v1 (1 week), D2 as v1.5 (additional ~2–3 days once D1 stack is shipped).

**When this is the right pick**: operator's dominant ritual is morning skim (Q-A = morning) **and** they also routinely receive forwarded papers (Q-A-secondary present). This is a superset of D1's user profile.

**When this is not the right pick**: any of D3/D4/D2-only rituals dominate. Blending more than this courts the Grand-Radar trap.

---

## 2. Comparison matrix

Scoring: L / M / H (honest, not diplomatic). Cost numbers from Opus S2R2 search
(MiniMax M2 @ $0.255/M input, $1.00/M output; GLM-4.5 @ $0.60/M input, $2.20/M
output — 2026 pricing).

| Direction | Debater consensus | User | Diff vs prior art | 1-wk solo feasibility | Tech complexity | Month-6 behavioral KPI | Biggest remaining risk | Monthly LLM cost (single user) |
|---|---|---|---|---|---|---|---|---|
| **D1 Belief Delta Brief** | Strong (both center of gravity, both rounds) | Morning-skim operator | H (PaperWeaver-validated mechanism; no incumbent) | M–H if narrowly scoped | M (extraction + diff is non-trivial) | Brief-open-rate ≥3 days/wk wk 18–24; replaces one ritual | Extraction precision <90% on benchmark-structure; false "supersessions" break trust | ~$23/mo (MiniMax M2, 150 papers/day extract+compare) + ~$6 polish = **<$30** |
| **D2 Paper Context Card** | Strong (both agree on shape + narrowed scope) | Forwarded-paper-triage operator | H (per-invocation personal context; no incumbent) | H (stateless per-invocation; same stack as D1 minus cron) | M (same as D1) | Confident pass-without-reading ~30% of invocations | Usage frequency (2–5/wk ceiling); user forgets tool between uses | ~$0.01–0.03/invocation × 2–5/wk = **<$1/mo** |
| **D3 Monday Lab-Brief** | Strong (both chose same cadence + structure) | Lab-lead-running-Monday-meeting | M (vs good curated newsletters, weaker than D1) | **H** (highest 1-wk feasibility; weekly job, prose only, no daily pipeline) | L–M (weekly synthesis pass; no ranker needed) | Lab-meeting prompt used ≥50% of weeks | Prose quality floor + "polished but non-essential" anti-goal | ~$5–10/mo (one weekly pass + reading of top ~50 papers) |
| **D4 Quiet Gatekeeper** | Qualified (both keep in menu; Opus advocates, GPT takes seriously post-S1) | Oversubscribed/volume-reduction operator | H *if thesis holds*; not differentiated if operator wants more | H (smaller output surface than D1; same ingest) | M (threshold calibration + audit loop) | Operator stops current morning-scan habit entirely (binary) | False-negative invisibility; audit loop is non-negotiable | ~$20/mo (same ingest as D1; cheaper output side) |
| **D1+D2 Hybrid** | Opus S2R2 explicit; GPT S2R2 implicit ("D1+D2 as product logic") | Morning-skim + forwarded-paper (superset) | H (both wedges, shared stack) | M (D1 in week 1; D2 as v1.5 in +2–3 days) | M+ (one extra surface on shared stack) | D1's KPI primary; D2's KPI as secondary | D1's extraction risk dominates; scope creep temptation | **<$30/mo** (D1 dominates cost; D2's marginal cost is negligible) |

**Non-dominance check (carried forward from Opus S2R2)**: no direction strictly
dominates another. D1 vs D3 = "daily compounding vs weekly low-risk." D2 vs D1
= "per-use depth vs persistent memory." D4 vs all = thesis fork. The hybrid
dominates D1 and D2 alone *only if* the operator's workflow covers both
rituals; otherwise it adds incremental scope without matching user need.

---

## 3. Key evidence points (load-bearing only)

The checkpoint rests on five load-bearing findings. Each either *validates* a
direction, *narrows* it, or *resolves* a prior concern. Listed in order of
decision-weight.

**E1 · PaperWeaver CHI 2024 — +0.74 triage-confidence lift, p=0.0124 (n=15)**
Source: Opus S2R2 §1. A CHI 2024 user study measured mean triage confidence
6.07 vs 5.33 when paper recommendations were contextualized against the user's
collected papers vs shown with bare related-work sections. **Statistically
significant on the exact axis D1 bets on.** Mechanism (diff-against-saved-state)
is no longer hopeful speculation — the closest-available cognate has been
measured. This is the single strongest evidence point in the debate and the
primary reason both debaters lean D1. D2's mechanism also leans on this.
URL: https://arxiv.org/abs/2403.02939 · https://dl.acm.org/doi/10.1145/3613904.3642196

**E2 · Elicit Alerts + Library shipped in 2026 — eliminates "generic triage feed"**
Sources: both debaters' S2 searches. Elicit now ships Alerts (topic monitoring
with daily OpenAlex-backed updates) plus Library (persistent saved-paper
state) on Pro/Team/Enterprise. Undermind ships topic-monitoring alerts.
**Consequence**: H6 (Personal Triage Feed) is marked out as low-differentiation
(Opus dropped it in S2R1 §5; GPT dropped it implicitly). Any direction
advanced must compete on something other than "persistent saved alerts" —
which is why D1's wedge is *"diff vs believed-state"* (not "filter against
saved query"), not merely "persistence."
URLs: https://support.elicit.com/en/articles/6546881 · https://elicit.com/blog/introducing-elicit-alerts

**E3 · arxiv-sanity-lite = strategic narrowing, not reluctant fallback**
Source: Opus S2R1 §1 adjustment (and GPT S2R1 §1). Karpathy's framing of the
lite version was "core value prop, less likely to go down, scales better" —
i.e. a *chosen* narrowing, not a retreat from a failed full version.
**Consequence**: the narrow directions (D1/D3/D4) are deliberate-scope
strategies, not compromises. This matters for operator motivation on month 3
("I chose this shape" vs "I gave up on the grand version"). It's also
cautionary evidence against reopening H1.
URL: https://github.com/karpathy/arxiv-sanity-lite

**E4 · MiniMax M2 pricing resolves the cost concern**
Source: Opus S2R2 §1 search. MiniMax M2 at $0.255/M input + $1.00/M output
(2026). A daily pipeline of 150 full-paper reads (12k input / 2k output each,
extract + ground + compare) = ~$0.76/day raw = ~$23/month. Final-polish pass
on ~5 delta papers/day on Claude/GPT-class = <$0.20/day. **Full single-user
pipeline < $30/month for any of D1–D4.** Synthesis D5 (Opus-raised cost/latency
concern) resolves: cost is no longer a first-order blocker for any direction.
URL: https://pricepertoken.com/pricing-page/model/minimax-minimax-m2

**E5 · SCIVER 2025 — open-domain claim verification is partial, not solved**
Source: Stage 1 synthesis §5 + §7 V11. SCIVER (ACL 2025) finds LLMs can
categorize weakness when given a review but struggle to identify weaknesses
from scratch. TaDA (VLDB 2025) corroborates: "valuable but limited" on claim
extraction. **Consequence**: D2's scope *must* stay at narrow benchmark-
structure extraction (reported baseline + headline metric + benchmark name —
extractable from the experiments table), not at open-domain novelty/impact
judgment. S1A's "drag in a paper, get a full auto claim-check table" is
overclaimed; the narrowed D2 ("Paper Context Card" with explicit exclusions)
is what survives. D1 and D4 inherit this scoping constraint for the same
extraction stack.
URL: https://aclanthology.org/2025.acl-long.420.pdf

---

## 4. Synthesizer recommendation

**Advance with D1 (Belief Delta Brief), conditional on operator's Q-A answer
in §0. Keep D1+D2 hybrid on the table as the "phased" variant.**

Reasoning (kept tight):

1. **D1 is the only direction both debaters independently derived in S1B, held through S2R1, and strengthened in S2R2.** Synthesis §9 already noted D1 is the only hypothesis with (both-model convergence) × (high differentiation) × (solo feasibility) all true. Both S2 rounds from both sides confirmed without drift.
2. **PaperWeaver (E1) is directly on D1's mechanism and measured it.** +0.74 triage-confidence lift, p=0.0124. No other direction has external validation at this specificity. D2/D3/D4 do not have equivalent measurement.
3. **E2 + E3 + E4 all push toward D1.** E2 kills the generic-feed alternative; E3 validates the narrow-shape-as-feature story; E4 removes cost as a blocker. D1 sits where all three vectors point.
4. **D1 is non-dominant on exactly one axis: extraction-precision risk.** The mitigation (narrow benchmark-structure extraction + on-by-default verification in first 4 weeks) is concrete and ships in a week.
5. **D1+D2 hybrid is strictly additive** if the operator's ritual-set includes both morning skim and forwarded papers. It shares D1's stack and risks.

**When each alternative becomes correct (from §0 Q-A mapping)**:
- **D2 alone becomes correct** if Q-A = "forwarded papers" is the dominant ritual *and* morning skim is not a regular habit. Then D1's daily cadence is the wrong shape.
- **D3 alone becomes correct** if Q-A = "Monday review" is the dominant ritual. D3 has the highest 1-week feasibility and the cleanest anti-dashboard posture; it loses to D1 only on differentiation.
- **D4 alone becomes correct** if Q-A = "volume reduction" is the honest pain and the operator actively endorses the attention-bottleneck thesis. D4 is a thesis bet and should not be picked unless the operator owns the thesis.
- **D1+D2 hybrid becomes correct** if morning skim is primary but forwarded-paper triage is also a live ritual (operator-confirmed). Ship D1 in week 1; add D2 as v1.5.

**Caveat owed to the moderator**: this recommendation weights E1 heavily.
PaperWeaver's n=15 study is small, and its setup differs from D1's exact
surface (it contextualized *recommendations*, not *deltas against held
beliefs*). The mechanism maps cleanly, but the lift number shouldn't be
treated as a product-level guarantee. Treat +0.74 as "mechanism works" not
"D1 will work."

---

## 5. Moderator decision menu

The moderator (human operator) must choose one of the paths below. This
document stops here — the decision belongs to a human.

### Option 1 · ADVANCE

Pick one of the five sub-options (four pure directions + the hybrid).
Answer Q-A and Q-B from §0 first; the Q-A answer determines which sub-option
is consistent with operator workflow reality.

- **1a · Advance with D1 (Belief Delta Brief)** — synthesizer recommendation. Requires Q-A = morning skim + Q-B sub-areas.
- **1b · Advance with D2 (Paper Context Card)** — requires Q-A = forwarded papers + Q-B sub-areas.
- **1c · Advance with D3 (Monday Lab-Brief)** — requires Q-A = Monday review + Q-B sub-areas. Highest 1-week feasibility.
- **1d · Advance with D4 (Quiet Gatekeeper)** — requires Q-A = volume reduction *and* explicit operator endorsement of the attention-bottleneck thesis + Q-B sub-areas.
- **1e · Advance with D1+D2 hybrid (phased)** — D1 in week 1, D2 in v1.5. Requires Q-A = morning skim with forwarded-paper triage as real secondary ritual + Q-B sub-areas.

**Moderator records in `001-moderator-notes.md`**:
```
## Decision @ S2 checkpoint
Option: 1a | 1b | 1c | 1d | 1e
Direction chosen: ____
Q-A answer: ____ (morning-skim / forwarded-papers / Monday-review / volume-reduction)
Q-B answer: ____ (2–3 AI sub-areas, concrete names)
Rationale: ____
```

Then run: `/debate-next 001 3 1` (Opus S3R1 in engineering mode). Codex
counterpart: paste the S3R1 kickoff from PROTOCOL.md §"Codex-side kickoffs".

### Option 2 · FORK

Pursue two directions as separate ideas (e.g. 001a = D1, 001b = D4 if the
moderator genuinely wants to explore both the "diff vs beliefs" and "reject
95%" theses in parallel).

1. Add new entries to `proposals/proposals.md`: `**001a**` (name + link to
   this checkpoint), `**001b**` (same). Mark 001 as Status = forked in
   `proposals/proposals.md`.
2. For each, run `/debate-start <new-id>`. Stage 1 of the new debate will
   inherit this discussion as context but re-explore poles against the
   narrowed direction.
3. Archive this discussion folder as-is; it's the reference for both forks.

**When fork makes sense here**: if the operator cannot honestly pick Q-A
(both morning skim *and* volume reduction feel equally true, and the
operator wants to learn which product wins). Note: fork costs a second week
of build; most operators should just pick one and iterate.

### Option 3 · PARK

Interesting but not now (e.g. operator's week is committed elsewhere, or
operator wants to run the "3 newsletters + 1 hour Monday" null alternative
for a month before building).

1. Update `proposals/proposals.md` entry 001: `Status: parked`, revisit
   condition (e.g. "after 4 weeks of null-alternative experiment" or "when I
   have a clear Q-A answer").
2. Archive this discussion folder as-is — it's a valuable reference.
3. Optional: write one paragraph in `001-moderator-notes.md` on why parked
   and what triggers a revisit.

**When park makes sense here**: if Q-A can't be answered without a small
self-experiment; or if the operator's week-of-build window closes.

### Option 4 · ABANDON

Evidence says don't build this. Relevant only if the operator concludes that
(a) the null alternative (newsletters + disciplined reading) actually works,
or (b) Elicit Alerts + arxiv-sanity-lite together are close enough that the
delta layer isn't worth a week.

1. Update `proposals/proposals.md` entry 001: `Status: abandoned`, reason.
2. Write `discussion/001/001-abandonment-lesson.md` — one page:
   - The idea
   - Why it initially seemed good (shared imagination from S1; PaperWeaver validation)
   - What we learned that killed it (e.g. null alternative + Elicit coverage is sufficient; operator doesn't buy behavioral-change framing; Q-A couldn't be answered)
   - What the operator should do with the freed time
3. Archive.

**When abandon makes sense here**: honestly, only if the operator runs the
null-alternative experiment and confirms no behavioral need. The debate
itself did not produce abandon-grade evidence — both sides said "conditional
yes."

---

## 6. Unresolved questions carried forward (if Advance)

If the moderator chooses **Advance**, these questions remain open for Stage 3
to address. Scoped by which direction is chosen.

**Applies to any Advance option**:
- **U1 · Extraction precision floor**: what actual precision does MiniMax M2 / GLM-4.5 achieve on `(benchmark, baseline, headline metric)` extraction from 2026 arXiv cs.AI papers? S1 §11 #9 flagged; still unresolved. Stage 3 must prototype-measure this, not assume it. This is the largest technical risk across D1/D2/D4.
- **U2 · One-user ranker feasibility**: can a per-user ranker be trained from a single user's actions (in-KB / noise / read-later) without collapsing to the user's prior beliefs? S1 §11 #4 + synthesis V13. Stage 3 should pick a conservative default (light personalization only, heavy defaults from anchor-paper embeddings) until ≥6 weeks of clicks exist.
- **U3 · Arxiv-to-dissemination latency**: how stale can the pipeline be before "Twitter scoops us"? Daily at 6am should be fine per Opus S2R2, but Stage 3 spec must state the tolerance explicitly.

**Applies to D1 / D1+D2 specifically**:
- **U4 · Anchor-paper seed flow**: how does the operator seed the KB in week 1? Bulk-import BibTeX / Zotero? Manual? Seeded from existing Elicit Library? Stage 3 must design this; it's the cold-start bottleneck.
- **U5 · Evaluation harness at week 8**: Opus S2R2 §2 proposed PaperWeaver-style rating of ~30 deltas on 1–7 scale vs a baseline. Stage 3 spec must include this measurement plan; the anti-goal isn't kept honest without it.

**Applies to D2 specifically**:
- **U6 · Invocation frequency floor**: if usage drops below 2/week after month 3, is the tool worth maintaining? Stage 3 should pre-commit to a retention-kill threshold.

**Applies to D3 specifically**:
- **U7 · Differentiation vs human newsletters**: Stage 3 must articulate what exactly makes the brief better than Import AI + 30 min of manual scope-trimming. Without a defensible answer, D3 is the "polished but non-essential" anti-goal.

**Applies to D4 specifically**:
- **U8 · False-negative audit design**: quarterly 20-paper spot-check is the synth note; Stage 3 must operationalize the sampling method so the audit isn't gamed by the calibration it's auditing.
- **U9 · Thesis-ownership check**: at spec time, the operator re-endorses the attention-bottleneck thesis in writing. If they waver, convert to D1.

**Not applicable if Fork / Park / Abandon** — these questions come with the
paths not chosen.

---

## 7. Honesty check

Things I noticed the debate might have under-weighted. Surfacing these because
convergent S2 debates tend to smooth away residual dissent and the moderator
should see what was smoothed.

**H-1 · The "shared imagination" convergence was strong, and that cuts two ways.**
Synthesis §1 noted both debaters independently reached the same optimistic
core in S1A before seeing each other's work. This is the strongest "both
models guessed it" signal but also a shared-prior-from-training signal. The
S2 convergence on D1 may be partly because both models pattern-matched the
same "persistent personalization" frame from their training data, not because
D1 is genuinely the best shape. Mitigation: the PaperWeaver evidence (E1) is
external to both models and goes in D1's direction — but PaperWeaver's lift
is +0.74 on a 1–7 scale at n=15, which is modest. Don't over-index.

**H-2 · Neither debater pressure-tested D3 against curated human newsletters.**
D3's biggest risk (§1.D3) is that Import AI / Alphasignal / Ahead of AI / Jack
Clark's Import AI / The Sequence / etc. already do 80% of what D3 offers,
with a human's taste in the loop. The Stage 1 synthesis §5 didn't catalog
these the way it cataloged research-tool incumbents, and neither S2 round
ran a price/quality benchmark. If Q-A = Monday review, the moderator should
explicitly ask: "do I already subscribe to 2+ good newsletters? do I read
them?" before picking D3.

**H-3 · The "1-week solo build" ceiling is stated but not audited.**
Opus S1B already weakened V3 ("MVP fits in a week") to "only a scoped MVP
fits in a week." Both S2 rounds reaffirmed scope discipline. But the debate
never produced a concrete week-1 task breakdown. D1's "extract + diff +
deliver" has non-trivial ingest plumbing (Marker + GROBID + OpenAlex + cron
+ KB store + extraction prompts + ranker + delivery UI). The week is tight
even if everything goes right. Stage 3 must treat "what ships in week 1 vs
what ships in week 2–3 implicitly" as a first-class decision, not hand-wave.

**H-4 · GPT's "team-memory" dimension was killed cleanly, but the operator's proposal mentions "我带领很多学生和研究员."** The proposal (re-checked) says
"我个人使用" — personal use — which was the dispositive phrase. Both debaters
closed team-memory out. But the operator is a lab lead; "prompts for your
students" is in D3, and "orientation on forwarded papers from students" is in
D2. Team is tangent-adjacent in three of the four directions. Worth the
moderator flagging: if team utility starts creeping into the D1 KPI ("did my
students benefit?"), scope has silently expanded and Opus S2R2's evaluation
anti-goal check won't catch it.

**H-5 · Opus's "inversion thesis" (D4) got one round of adoption from GPT and stopped there.** Synthesis §12 D1 flagged this as genuinely divergent (Opus-only
in Stage 1). GPT S2R1 "takes it seriously after S1 synthesis" and GPT S2R2
keeps D4 in the peer set. But neither GPT round independently argued *for*
D4 — GPT's lean is D1 in both rounds. The thesis is in the menu by Opus's
conviction plus GPT's cooperative non-objection. If the moderator is drawn
to D4, they should ask themselves whether they're buying Opus's thesis or
buying a debate-cooperative artifact. The Stage 1 synthesis §12 already
pre-warned this; keeping the warning alive here.

**H-6 · "Current LLMs are good enough" shared-imagination assumption from S1A §1.6 was never hard-verified.** Synthesis §1.6 notes both debaters asserted
this without citation in S1A. S1B cited SCIVER and Galactica as reasons for
narrowing. S2 rounds cited MiniMax M2 pricing for cost. But nobody ran a
precision measurement on "does the narrow extraction actually hit 90% on 2026
arXiv cs.AI papers?" at any point in S1 or S2. **This is U1 above, re-flagged
as an honesty-check item**: the debate has reasoned *around* extraction
precision; it has not *measured* it. Stage 3 must prototype-measure this
before anything else locks.

---

*End of Stage 2 checkpoint. Moderator action required before Stage 3. Pipeline is paused.*
