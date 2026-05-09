# ideababy_stroller — Idea→PRD framework SSOT

> **Repo role**: idea→PRD harness(L1 inspire / L2 explore / L3 scope / L4 plan + forge cross-cutting)
> **Companion repo**: `XenoDev`(PRD→code build harness — see §4 + framework/SHARED-CONTRACT.md §6 v2.0)
> **Updated**: 2026-05-08 — restructured per `discussion/006/forge/v1/stage-forge-006-v1.md` verdict
> **Constraint**: ≤ 8KB(Vercel benchmark: 8KB AGENTS.md = 100% activation; > 8KB drops)

## §1 · Safety Floor(non-overridable hard rules)

These three rules **hard block in any sandbox mode**, including `full-auto`. No prompt / config / sandbox setting disables them. SSOT here; `XenoDev` mirrors. Full spec + failure-case provenance in `framework/SHARED-CONTRACT.md` §2.

1. **Production credential isolation** — `.env.production` / `.env.prod` / `secrets/production/*` / `prod://` connection strings must NOT enter agent context. Enforced at file-system path filter, agent context loader, pre-commit hook.
2. **Irreversible command hard block** — `rm -rf /`, `DROP TABLE` (non-test prefix), `git push --force` to protected branches (`main` / `master` / `production` / `release-*`), `aws rds delete-db-*`, `aws s3 rm --recursive <prod-bucket>`, key revocation, GCP/Azure equivalents. Escape only via human escape hatch (typed declaration + 2nd confirmation).
3. **Backup destruction detection** — same credential / API must NOT have authority to delete primary AND backup storage. Detected at IAM lint + runtime API interceptor.

**Failure case prevented**: Cursor + Claude 9-second database deletion (tomshardware 2025).

## §2 · Reliability — three layers

Reliability ≠ "fewer human prompts". Three layers, priority order:

1. **Safety Floor**(§1)— non-overridable
2. **Deterministic Feedback** — tests, lint, type-check, hook gates; binary pass/fail signal
3. **Learning Loop** — retrospective + Eval Score (SWE-bench Pro micro-eval / review recall+precision); writes back to AGENTS.md / skills / rules / quality gates

K2 ("可靠的、自动化程度最高") disambiguated: Safety Floor non-negotiable; automation maximizes within deterministic feedback + learning loop boundaries.

## §3 · Light entry vs heavy upgrade — triggers

Tiered harness: light entry for small projects, heavy upgrade for idea-incubation / mid-to-large.

| Tier | Trigger(any one) | Required tooling |
|---|---|---|
| Small | no production endpoint AND no irreversible op AND PRD < 500 字 AND single file_domain | AGENTS.md + Safety Floor + basic gates |
| Medium | production endpoint OR multi-file_domain OR PRD 500-2000 字 OR data persistence | + L4 build worktree + cross-model review |
| Large | regulated data OR distributed system OR PRD > 2000 字 OR > 3 file_domain | + full L1-L4 + retrospective + forge |

When in doubt, upgrade. Downgrade only after retrospective confirms previous tier was sufficient.

## §4 · Cross-repo contract(ideababy_stroller ↔ XenoDev)

Two repos, **independent release**, no version pinning. Coordinated via `framework/SHARED-CONTRACT.md` (SSOT here, mirror in XenoDev).

- **PRD schema** (plain markdown, 8 required fields) → produced by `/plan-start`, consumed by XenoDev build runtime (per SHARED-CONTRACT §6 v2.0)
- **Hand-off** → `/plan-start` v3.0 writes `discussion/<id>/<fork>/<prd>/L4/HANDOFF.md` (workspace + source_repo_identity blocks per §6.2 / §6.5)
- **Hand-back** → XenoDev writes `discussion/<id>/handback/*.md` back to IDS per §6.3 schema; operator runs `/handback-review <id>` to decide
- **Safety Floor binding** → XenoDev AGENTS.md must reference §1 with `binding from ideababy_stroller framework/SHARED-CONTRACT.md §2`
- **Versioning** → semver on `contract_version` frontmatter; breaking change = deprecation ≥ 4 weeks + migration ≥ 4 weeks + cutover ≥ 1 week (idea_gamma2 three-stage Pattern)

If XenoDev unavailable, PRD + hand-off package are themselves deliverables; build can proceed in any harness honoring the schema.

## §5 · Pipeline & forge entry points

```
proposal → /inspire-start → L1 stage doc → fork
                          → /explore-start → L2 stage doc → fork
                          → /scope-start → L3 PRD → fork
                          → /plan-start → discussion/<id>/<prd>/L4/HANDOFF.md (v3.0)
                                          ↓
                                          XenoDev build runtime (per SHARED-CONTRACT §6 v2.0)
                                          ↓
                                          discussion/<id>/handback/*.md → /handback-review <id>

(orthogonal) /expert-forge <id> → cross-cutting audit + SOTA benchmark + forced convergence
                                → discussion/<id>/forge/v<n>/stage-forge-<id>-v<n>.md
```

- **Layer discipline**: L1/L2 NEVER discuss tech/feasibility/cost. L3 brings real constraints. L4 is engineering.
- **PRD source-of-truth** after L3: immutable from L4 spec-writer. Issues escalate to operator.
- **Forge product** lives forever; verdict triggers next decision (advance / fork / park / abandon).

## §6 · Iron rules + defaults

**Operator-level**:
- Output in Chinese (this file is English so it functions as cross-agent SSOT; user-facing dialog is Chinese)
- No code without a hand-off package (L4 produces hand-off; XenoDev produces spec/tasks/code)
- TDD for production code (L4): test → red → implement → green
- Pre-merge review mandatory (L4): `/task-review <fork> T<NNN>` verdict ≠ BLOCK
- Cross-model review mandatory for v1.0 paths
- Specs immutable: M3 (commit d3194a0, 2026-05-10) archived 4 fork specs/ as forge v2 evidence; no further task additions / reviews (XenoDev produces its own specs going forward)
- "Not sure" is a first-class L3R0 answer
- Every command outputs a next-step menu

**Tools**: `rg` (never raw `grep`); JS/TS: `pnpm` + Node 22 LTS + TS strict + Biome; Python: `uv` + `ruff` + `pytest`; Go: standard + `golangci-lint`; iOS: Xcode 16+ + SwiftLint + XCTest; Commits: Conventional Commits.

**Directory ownership**:
- `proposals/proposals.md` — operator writes (one-paragraph seed)
- `discussion/NNN/{L1, <fork>/L2/L3/<prd>/L4, forge/v<n>}/` — per-layer
- `specs/NNN-<fork>-<prd>/` — only spec-writer + task-decomposer
- `projects/NNN-<fork>/` — parallel-builder workers (scoped to file_domain)
- `.codex-inbox/queues/<id>/` + `.codex-outbox/queues/<id>/` — coordination bus (v2 multi-queue)
- `framework/` — framework SSOT documents

**Prohibitions**: L1/L2 emitting tech content; ad-hoc LLM auto-generation of AGENTS.md / CLAUDE.md (updates require plan + operator approval); modifying `specs/` at all (M3 archived); committing `.env*`; forking > 3 levels deep without reason; Skills as fact SSOT (facts go HERE; Skills = activatable processes only).

**When things feel off**:
1. `/status NNN` for tree state
2. `/clear` and restart from a stage doc if context polluted
3. If a layer drifts (L2 doing tech), re-read its protocol skill + consider moderator note
4. `/expert-forge <id>` for dual-expert audit when stage product feels mis-converged

## §7 · References & scope

**Read for full provenance**:
- `framework/NON-GOALS.md` — 7 explicit non-goals with failure cases
- `framework/SHARED-CONTRACT.md` — full cross-repo contract
- `framework/AUTODEV-PIPE-SYNC-PROPOSAL.md` — historical (pre-M2 cutover); XenoDev coordination per §6 v2.0 supersedes
- `CLAUDE.md` — Claude-Code-specific working notes (Chinese, overlaps but adds operational details)
- `discussion/006/forge/v1/stage-forge-006-v1.md` — dual-expert verdict that produced this restructure
- `discussion/006/forge/v1/next-steps.md` — 5-document plan provenance

**Out of scope here**:
- Per-project: `projects/<fork>/AGENTS.md`
- Personal: `~/.claude/CLAUDE.md`
- Path-scoped: `.claude/rules/*.md`
- Build harness internals: `XenoDev` repo
