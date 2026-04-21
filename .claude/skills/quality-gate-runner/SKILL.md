---
name: quality-gate-runner
description: Reference for the 10 commercial-readiness quality gates, with runnable commands and pass criteria. Load when running /quality-gate, before shipping, before merging to main, or when the user asks "is this ready", "can I ship", or "ship check".
allowed-tools: Read, Bash, Grep, Glob
disable-model-invocation: false
---

# Quality Gate Runner — SOPs

Defines the 10 gates every commercial-grade release must pass. Gates 1–6 can be
automated; 7–8 delegate to Codex / adversarial-reviewer; 9–10 require human judgment.

## Philosophy

The enemy of commercial quality is **false green**. A gate that reports PASS when
something's actually wrong is worse than no gate. Every gate below has a well-defined
failure mode; if the check can't run (missing infra), that's a RED, not a SKIP.

## The ten gates

### G1 · Type check
```bash
# TypeScript projects
pnpm tsc --noEmit 2>&1 | tee /tmp/g1.log
# Python strict
uv run mypy --strict . 2>&1 | tee /tmp/g1.log
# Go
go vet ./... && go build ./...
# Swift
xcodebuild -scheme <Scheme> -sdk iphonesimulator
```
**PASS**: 0 errors. Warnings allowed.
**Common false green**: `--noEmit` skipped → no type check actually happened.

### G2 · Lint
```bash
pnpm lint 2>&1 | tee /tmp/g2.log
# or: biome check . / ruff check . / swiftlint lint
```
**PASS**: 0 errors, ≤5 warnings.
**Common false green**: lint config ignoring most of src/ → cat the config; verify coverage.

### G3 · Unit tests + coverage
```bash
pnpm test --coverage 2>&1 | tee /tmp/g3.log
# or: uv run pytest --cov=src --cov-report=term-missing
```
**PASS**: all green, lines ≥ 80%, branches ≥ 75%.
**Common false green**: tests that `expect(true).toBe(true)` → spot-check 3 random tests read nontrivially.

### G4 · Integration / E2E
```bash
pnpm e2e 2>&1 | tee /tmp/g4.log
# or: playwright test / xcuitest
```
**PASS**: all critical-path scenarios from spec.md §Verification green.
**Common false green**: flaky tests retried → check the retry count; >1 retry = flaky = RED.

### G5 · Security — static + dependency
```bash
# Secrets
rg -n "(api[_-]?key|secret|password|token|bearer)\s*[:=]\s*['\"][^'\"]{16,}" \
   --glob '!**/*.test.*' --glob '!**/*.md' --glob '!**/node_modules/**' --glob '!**/.git/**'
# Dependency vulns
pnpm audit --prod 2>&1 | tee /tmp/g5-deps.log
# or: uv pip audit / cargo audit / govulncheck ./...

# Then delegate deep review to the security-auditor subagent
```
**PASS**: 0 secrets, 0 critical, 0 high in `pnpm audit`, 0 critical from security-auditor.

### G6 · Performance baseline
Read `specs/*/SLA.md` for targets. Then run project benchmarks:
```bash
# Examples
pnpm bench
k6 run perf/smoke.js
autocannon -c 50 -d 30 http://localhost:3000/api/health
```
**PASS**:
- p95 within SLA
- No regression > 10% vs last known good baseline (store baseline in `perf/baseline.json`)

**If no perf test exists**: that's a RED for v1.0 (but OK for v0.1 MVP).

### G7 · Codex adversarial review
Run (in Claude Code with codex-plugin-cc installed):
```
/codex:adversarial-review --base main
  challenge concurrency safety, data consistency, failure recovery, security
  boundaries, and operational cost at 10x traffic. assume the author has no
  large-project experience.
```
**PASS**: 0 blockers in Codex's report. Follow-ups go to risks.md.

### G8 · Opus adversarial self-review
Delegate to the `adversarial-reviewer` subagent:
> "Use adversarial-reviewer on diff main...HEAD. All three personas. Severity-promote cross-persona findings."

**PASS**: overall score ≥ 85/100, 0 BLOCKs.

### G9 · Compliance checklist
Read `specs/*/compliance.md` if it exists. Minimum manual checklist for any commercial product:

```markdown
- [ ] Privacy policy drafted and linked from app
- [ ] Terms of service drafted and linked
- [ ] Data residency decided; implementation matches policy
- [ ] User data deletion path exists and is tested
- [ ] User data export path exists (for GDPR/PDPA portability)
- [ ] Cookie / tracking consent (if applicable to jurisdiction)
- [ ] Crash reporting has opt-out
- [ ] Analytics has opt-out
- [ ] (payments) PCI scope documented; SAQ completed
- [ ] (health data) HIPAA applicability reviewed
- [ ] (EU users) GDPR DPIA for high-risk processing
- [ ] (Taiwan users) PDPA notices prepared
- [ ] (China users) check applicable data localization
- [ ] App store policies reviewed (iOS / Android)
- [ ] Third-party licenses in LICENSE-THIRDPARTY or equivalent
```

**PASS**: operator signs each line or explicitly marks N/A with reason.

### G10 · Human acceptance
Operator walks through `spec.md §6 Verification Criteria` personally for each outcome.
No shortcut. Must be a real person using the product as a real user would.

**PASS**: operator writes `GATE10: PASS <date>` in the PR / release notes.

## Gate report format

The `/quality-gate` command produces this table. Anything that isn't explicitly ✅ is RED:

```
| Gate | Status | Detail |
|------|--------|--------|
| G1 Type check       | ✅ | 0 errors |
| G2 Lint             | ⚠ | 2 warnings — acceptable |
| G3 Unit + coverage  | ❌ | 87% lines / 71% branches — branches below 75% threshold |
| G4 E2E              | ✅ | 12/12 scenarios |
| G5 Security (SAST)  | ❌ | 1 HIGH in utils/merge.ts:44 — prototype pollution |
| G6 Performance      | ⏸ | Benchmark not implemented (acceptable for v0.1, RED for v1.0) |
| G7 Codex review     | ✅ | 0 blockers, 2 follow-ups |
| G8 Opus review      | ✅ | Score 88/100 |
| G9 Compliance       | ⏸ | Awaiting operator sign-off |
| G10 Human accept    | ⏸ | Pending |

SHIP-READY: NO (2 blockers; 3 pending)
```

## Overriding a gate

Gates are advisory for v0.1 / MVP. For commercial v1.0, each failed gate requires:
1. Written override justification
2. Risk entry in `risks.md`
3. Ticket for follow-up

An override is NOT a fix — it's a deliberate decision to ship with a known gap.
Track overrides; if you have > 3 active overrides, stop shipping and clear the backlog.

## Common false-green patterns (learn these)

1. **Ignored test files** — `jest.config` excludes tests of a whole module. Grep for `testPathIgnorePatterns`.
2. **Coverage gap in new code** — total coverage OK but changed lines uncovered. Run:
   ```bash
   pnpm test --coverage --changedSince=main
   ```
3. **Flaky E2E passing on retry** — configure runners with `retries: 0` for gates.
4. **Lint auto-fix masking** — run `pnpm lint` (not `lint --fix`) so you see what would've been changed.
5. **Adversarial review with no findings** — means the reviewer didn't dig. Re-run with explicit focus.
6. **Security scan with no output** — means the tool didn't run, not that there are no issues. Check exit code.
