---
description: Run the full quality gate suite before shipping a feature or merging to main
argument-hint: "<idea-number>  (e.g. 001)"
allowed-tools: Read, Bash, Grep, Glob, Agent(security-auditor), Agent(adversarial-reviewer), Agent(code-reviewer)
model: opus
---

# Quality Gate — Commercial-Grade Readiness Check

Idea **$ARGUMENTS**. Runs the 10 gates defined in the Playbook. **Any failure blocks ship.**

Report as a checklist; do **not** mark anything ✅ unless you've actually run the check.

## Context gathering (no manual effort)

Read the project:
- !`cd projects/$ARGUMENTS-* && git status --short`
- !`cd projects/$ARGUMENTS-* && git log --oneline -10`
- !`cd projects/$ARGUMENTS-* && cat package.json 2>/dev/null | head -40`

## Gates (run in order; stop at first hard-block if critical)

### G1 — Type check
```bash
cd projects/$ARGUMENTS-*
# JS/TS:
pnpm tsc --noEmit 2>&1 | tail -20
# Python:
# uv run mypy --strict . 2>&1 | tail -20
```
PASS criteria: 0 errors.

### G2 — Lint
```bash
pnpm lint 2>&1 | tail -20
```
PASS: 0 errors, ≤5 warnings.

### G3 — Unit tests + coverage
```bash
pnpm test --coverage 2>&1 | tail -30
```
PASS: all green + coverage ≥ 80% lines / ≥ 75% branches.

### G4 — Integration / E2E
```bash
pnpm e2e 2>&1 | tail -20
```
PASS: all critical user paths green.

### G5 — Security static analysis
```bash
# Secrets
rg -n "(api[_-]?key|secret|password|token)\s*[:=]\s*['\"][^'\"]+['\"]" --glob '!**/*.test.*' --glob '!**/*.md'
# Dependencies
pnpm audit --prod 2>&1 | tail -20
```
Then delegate to the **security-auditor** subagent:
> "Use security-auditor to review src/ and report OWASP Top 10 findings."

PASS: 0 critical / 0 high findings; no secrets in code; pnpm audit clean.

### G6 — Performance baseline
Read `specs/$ARGUMENTS-*/SLA.md` for targets, then run the project's benchmark suite
(typically `pnpm bench` or `k6 run perf/smoke.js`).

PASS: p95 within SLA, no regression >10% vs previous main.

### G7 — Codex adversarial review
```
/codex:adversarial-review --base main
  challenge concurrency safety, data consistency, failure recovery, security boundaries,
  and operational cost at 10x traffic.
```
PASS: 0 blockers in Codex's report.

### G8 — Opus adversarial self-review
Delegate to **adversarial-reviewer** subagent:
> "Use adversarial-reviewer on the diff between main and HEAD. Three personas:
> saboteur, new-hire, security-auditor. Each MUST find at least one issue."

PASS: overall score ≥ 85 / 100.

### G9 — Compliance checklist
Read `specs/$ARGUMENTS-*/compliance.md` if it exists. For a consumer product typically:
- [ ] Privacy policy and ToS drafted
- [ ] Data residency decided & implemented
- [ ] GDPR / CCPA / Taiwan PDPA basics covered (deletion, export, consent)
- [ ] Crash / analytics opt-out path exists
- [ ] If handling payments: PCI scope documented

This is a manual review — print the checklist and ask the human to confirm each item.

### G10 — Human acceptance
Ask the human to run through `specs/$ARGUMENTS-*/spec.md` §Verification criteria
manually. Block on their explicit `GATE10: PASS`.

## Output format

```
# 🚦 Quality Gate Report — Idea $ARGUMENTS
**Timestamp**: <now>
**Diff**: main...HEAD (<N> commits, <M> files, +<add>/-<del>)

| Gate | Status  | Detail |
|------|---------|--------|
| G1 Type check         | ✅ | 0 errors |
| G2 Lint               | ✅ | 2 warnings (non-blocking) |
| G3 Unit + coverage    | ⚠ | 87% lines / 71% branches (below 75% threshold on src/queue/) |
| G4 E2E                | ✅ | 12/12 scenarios |
| G5 Security (SAST)    | ❌ | 1 HIGH: prototype pollution in utils/merge.ts:44 |
...

## 🟥 Blockers (must fix before ship)
1. [G5] prototype pollution — <file>:<line> — <brief fix>
2. [G3] branch coverage — write tests for src/queue/retry.ts error paths

## 🟨 Follow-ups (track in risks.md, not blocking)
...

## 🟩 Ready for ship?
NO — 2 blockers above.

OR:

YES — all 10 gates passed. Proceed to: `gh pr create --fill`.
```
