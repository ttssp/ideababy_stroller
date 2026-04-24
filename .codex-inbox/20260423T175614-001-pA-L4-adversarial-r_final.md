# Codex Task · 001-pA · L4 Final Adversarial Review (R_final)

**Created**: 2026-04-23T17:56:14Z
**Recommended model**: gpt-5.4
**Recommended reasoning_effort**: xhigh
**Estimated tokens**: ~30-45k
**Max runtime**: ≤ 120 min
**Supersedes**: R2 kickoff (20260423T165611...) which was scoped only to B1/B2/B3 fix verification

---

## Why this is "R_final" not "R2"

After R1 BLOCK + fixes, the operator gave a 5-hour autonomy window asking to complete **all documentation** to a bar where "1 architect + 6–8 junior engineers can directly build from the spec package." The spec-writer + task-decomposer produced:

- R1 blocker fixes (B1 `paper_summaries` + B2 skip `CHECK` + B3 task contracts)
- Q1/Q2/Q4/Q5 drift closures
- **7 new reference artifacts** in `specs/001-pA/reference/` totaling ~6900 lines:
  - `schema.sql` (624 lines) — executable full DDL
  - `directory-layout.md` (794) — monorepo tree + env + configs
  - `api-contracts.md` (1119) — 18 endpoints + error catalog
  - `llm-adapter-skeleton.md` (1354) — full TS interface + 2 adapters + prompts
  - `ops-runbook.md` (1556) — deploy + backup + on-call SOP
  - `testing-strategy.md` (733) — unit + E2E catalog + fixtures
  - `error-codes-and-glossary.md` (713) — errors + extended glossary
- `DECISIONS-LOG.md` (~339 lines) — all first-principles judgments
- `README.md` (222 lines) — navigation entry point
- 5 interface-layer drift consolidations (tech-stack ↔ reference)

**Total spec package ≈ 10,000+ lines of engineering contract.** This review is the **final sanity check before Phase 0 kickoff**. Operator explicitly wants a stress-test that surfaces any remaining blocker.

---

## Your role

You are GPT-5.4 xhigh performing a comprehensive adversarial review on the **entire** spec package, with a narrow focus on three questions:

1. **Does the package actually satisfy "junior engineer can start coding"?** — i.e. are there unresolved "figure it out" gaps, missing fields, un-cross-referenced terms, spec ↔ reference drift, or CI-skipped cases that would cause a junior to block and page the architect?
2. **Are the R1 blockers actually closed end-to-end**, not just in the file that was patched but consistently across the now-expanded reference layer?
3. **Are there any NEW blockers introduced by the reference layer** (e.g. schema.sql does something the tasks don't expect; api-contracts.md uses a type not in schema; testing-strategy.md references a fixture that doesn't exist)?

You are looking for **blockers and high-severity concerns only**. This is the last adversarial pass before build; the operator explicitly wants a harder challenge, not a box-check.

---

## Read order (efficient, ~90 min budget)

### Tier 1 — Landing (10 min)
1. `specs/001-pA/README.md` — navigation
2. `specs/001-pA/DECISIONS-LOG.md` — all first-principles decisions (skim)

### Tier 2 — Spec authoritative (20 min)
3. `specs/001-pA/spec.md` — v0.2.2 six-element contract
4. `specs/001-pA/architecture.md` — v0.2 C4 + ADRs 1–7 + data model
5. `specs/001-pA/tech-stack.md` — pinned versions + LLM interface
6. `specs/001-pA/risks.md` — TECH-1..9 · OPS-1..5 · SEC-1..10 · DOGFOOD-1..3 · BUS-1..3 · COM-1..4 · LEG-1..3
7. `specs/001-pA/SLA.md` — v0.1 + v1.0
8. `specs/001-pA/non-goals.md` — 25 items
9. `specs/001-pA/compliance.md`
10. `specs/001-pA/dependency-graph.mmd` — 25 tasks, 113h, critical path 58h (note: 114h after Q1/Q2/Q4 patch, 59h critical path — header slightly stale; not a blocker per DECISIONS-LOG)

### Tier 3 — Reference (50 min)
11. `specs/001-pA/reference/schema.sql` — **check each CHECK/UNIQUE/FK**
12. `specs/001-pA/reference/directory-layout.md` — package.json + tsconfig + CI
13. `specs/001-pA/reference/api-contracts.md` — 18 endpoints with schemas
14. `specs/001-pA/reference/llm-adapter-skeleton.md` — TS code + prompts
15. `specs/001-pA/reference/ops-runbook.md` — systemd + backup + incidents
16. `specs/001-pA/reference/testing-strategy.md` — test catalog + fixtures
17. `specs/001-pA/reference/error-codes-and-glossary.md` — 50 errors + glossary

### Tier 4 — Tasks (spot-check 6 files, 10 min)
18. `specs/001-pA/tasks/T001.md` — LLM spike (gate)
19. `specs/001-pA/tasks/T003.md` — schema spine (Q5 closure verification)
20. `specs/001-pA/tasks/T004.md` — LLM interface
21. `specs/001-pA/tasks/T013.md` — summary persist
22. `specs/001-pA/tasks/T015.md` — /today + 4-action + skip enforcement
23. `specs/001-pA/tasks/T023.md` — export + export_log
24. `specs/001-pA/tasks/T030.md` — deploy (Q1 closure verification)

### Tier 5 — Meta (5 min)
25. `specs/001-pA/OPEN-QUESTIONS-FOR-OPERATOR.md` — Q1..Q5 resolution markers + Q3 still deferred
26. `.codex-outbox/20260423T142034-001-pA-L4-adversarial-r1.md` — your R1 output for comparison

### Tier 6 — Lineage (if time)
27. `discussion/001/001-pA/PRD.md` — for faithfulness verification (spec should still map 1:1)

---

## Specific cross-checks (MUST perform each)

### X1 — Schema integrity
- Every column referenced in `tasks/T*.md` Outputs is actually declared in `schema.sql`
- Every FK has explicit ON DELETE policy
- Every CHECK is syntactically valid Postgres 16
- `paper_summaries` sentence-cap regex handles: pure English, pure Chinese (full-width `。！？`), mixed, no-trailing-punctuation edge case
- `actions.skip_requires_why` handles empty-string btrim correctly
- Index strategy covers every `WHERE` clause in the API contracts (e.g., `/today` loader needs briefings(lab_id, for_date) index)
- `export_log` indexed for monthly audit scan

### X2 — API contract ↔ schema consistency
- Every resource type in `api-contracts.md §3` maps field-for-field to `schema.sql` (case conversion OK but no missing fields)
- Error codes in `error-codes-and-glossary.md §1` match API endpoint errors one-to-one
- curl examples parse against declared request schema
- No endpoint demands a column that schema doesn't have
- E9 `/api/today` is clearly labeled deferred in §7 (per drift-4 resolution)

### X3 — LLM adapter ↔ spec ↔ cost envelope
- `LLMProvider` interface in `llm-adapter-skeleton.md §2` matches `tech-stack.md §2.4` exactly (camelCase, per-pair judge, SummaryRecord shape)
- OpenAI $15/M output used consistently across `tech-stack.md`, `spec.md C11`, `llm-adapter-skeleton.md §4`
- T001 spike harness (`llm-adapter-skeleton.md §8`) matches `T001.md` exit criteria (≥ 70% on 20 human-labeled)
- Prompt templates contain the injection-defense instructions (untrusted-text framing + XML wrapping)
- `recordLLMCall` budget check in `llm-adapter-skeleton.md §7` covers BOTH `summarize` and `judge` purposes (R1 H8 implicit-fix)

### X4 — Tasks ↔ reference alignment
- Every task's `file_domain` paths exist in `directory-layout.md §1` tree
- Every task that modifies a co-owned file has a strict `depends_on` edge
- T003 Outputs enumerate exactly what schema.sql declares (15 tables, 2 CHECKs, UNIQUE, 5 auth cols, 3 labs/fetch cols, export_log)
- T030 grants.sql enumeration matches reference (webapp_user + worker_user permissions on paper_summaries, export_log)
- T032 E2E `schema_version >= '1.1'` (Q4 closure)
- T013 writes to `paper_summaries` not `llm_calls.response_text`
- T015 3-layer skip enforcement has specific task deliverables (`recordAction.ts`, `skip-why-input.tsx`)

### X5 — Testing catalog completeness
- Every `spec.md §6` verification hook has a corresponding test in `testing-strategy.md §2/3/4`
- Every red-line-2 enforcement layer has a test (DB CHECK + API + UI)
- `tests/fixtures/human-labeled-20.json` schema documented (needed for T001 spike to even start)
- E2E `skip-requires-why.spec.ts` covers Chinese input edge cases (2-char / 3-char rejected, 5-char accepted)

### X6 — Ops runbook completeness
- systemd units reference correct file paths (match `directory-layout.md deploy/systemd/`)
- `pg-dump.sh` + `restic-backup.sh` have sane error handling + alert paths
- Incident response (I1–I8) has concrete commands
- Secrets rotation covers all secrets declared in `.env.example`
- Caddy query-string logging explicitly disabled (H6 mitigation)

### X7 — Junior-engineer readiness
Pick 3 tasks at random (T010, T015, T021 recommended). For each, answer:
- Could a TypeScript engineer with no prior project context, given only the spec package, write the code?
- What's missing that would force them to ask the architect?

### X8 — Spec versioning integrity
- `spec.md` Version field shows 0.2.1 or 0.2.2 after the latest patch
- Changelog at file footer (if present) has all 4 bumps: 0.1 → 0.2 → 0.2.1 → 0.2.2
- All cross-references to `spec.md §<section>` still resolve (e.g. after D15 / D16 added, do old references break?)

### X9 — New blockers introduced by reference layer
Look specifically for:
- Reference doc demands a feature task doesn't deliver
- Reference doc declares an invariant that schema doesn't enforce
- Reference doc's code example wouldn't compile under the pinned TS 5.6 strict config
- Reference doc's curl example would fail against the stated endpoint
- `ops-runbook.md` references a file that `directory-layout.md` doesn't list

### X10 — Bus-factor stress
If the operator disappeared for 14 days **right after Phase 0 kickoff**:
- Can another engineer pick up T001 solely from the spec package?
- Is `runbook/operator-absent.md` (mentioned in ops-runbook.md §9 I4) actually prescribed?
- Are secrets rotation / invite management reachable without operator's memory?

---

## Your output

Write to: `.codex-outbox/20260423T175614-001-pA-L4-adversarial-r_final.md`

### Required structure

```markdown
# Adversarial Review · 001-pA · R_final

**Reviewer**: GPT-5.4 xhigh
**Completed**: <ISO>
**Runtime**: ~<NN> min
**Prior rounds**: R1 BLOCK (3 blockers); R_final verifies fixes + reviews expanded reference layer

## Executive summary (≤ 5 sentences)
<is this package buildable by 1 architect + 6-8 juniors? Y/N/Y-with-caveats>

## Cross-check results (X1–X10)

| Check | Pass | Key findings |
|---|---|---|
| X1 Schema integrity | ✅/⚠️/❌ | ... |
| X2 API ↔ schema | ... | ... |
| X3 LLM ↔ spec ↔ cost | ... | ... |
| X4 Tasks ↔ reference | ... | ... |
| X5 Testing catalog | ... | ... |
| X6 Ops runbook | ... | ... |
| X7 Junior readiness | ... | ... |
| X8 Spec versioning | ... | ... |
| X9 New blockers | ... | ... |
| X10 Bus-factor | ... | ... |

## Blockers (must fix before Phase 0)
(empty if none)

## High-severity concerns
(1-line per item, ≤ 10 items)

## Pleasant surprises / things done well
(optional, ≤ 5 items — specifically flag things that exceeded expectations for junior-build readiness)

## Junior-engineer stress test (X7 detail)
For T010, T015, T021:
- What a junior could do from the spec alone
- What would require architect consultation
- Estimated time to first-commit under ideal conditions

## Remaining R1 H1–H10 status
Operator deferred them. List which ones the expanded reference layer incidentally addressed:
- H5 (export CI grep) — addressed? by what? (look in `.github/workflows/` references)
- H6 (invite GET) — retained with documented risk (SEC-10 in risks.md; drift 5 in DECISIONS-LOG)
- others...

## Final verdict
One of:
- **CLEAN** — no blockers; spec package ready for Phase 0 kickoff; junior-engineer bar met
- **CLEAN-WITH-NOTES** — no blockers; 1-5 high-severity concerns operator should log in risks.md before kickoff
- **CONCERNS** — ≥ 6 high-severity concerns OR 1 high-priority concern needs spec-writer touch before kickoff
- **BLOCK** — ≥ 1 blocker or a fundamental junior-readiness gap

Justify in ≤ 3 sentences.

## Operator's personal action list
Top 3 things operator must verify themselves, in order:
1. ...
2. ...
3. ...
```

---

## Constraints on your output

- Max 4000 lines
- Quote ≤ 15 words verbatim per file
- Cite section anchors exhaustively (the operator should be able to jump to each finding)
- NEW drifts are more important than re-raising R1 deferred items
- Be terse but specific. "spec.md §6 line 41" > "the verification section"
- If spec is genuinely ready, say CLEAN and stop — don't invent concerns for show

## Escape hatch

If your review shows the spec is comprehensively ready (CLEAN), say so plainly with justification. If it's 90% ready but has 1 blocker, say BLOCK with a single-line B1 + fix suggestion. The operator has an explicit "ship or patch" decision waiting on your verdict.

Write to `.codex-outbox/20260423T175614-001-pA-L4-adversarial-r_final.md`. Begin.
