---
name: sdd-workflow
description: Spec-Driven Development workflow for turning human-approved conclusions into production-grade spec packages. Load when writing, reviewing, or updating spec.md, PRD.md, architecture.md, or any file under specs/. Contains the 6-element spec contract, file templates, adversarial review loop, and the common failure modes to avoid.
disable-model-invocation: false
---

# Spec-Driven Development Workflow

Specs are the ONLY artifact that turns multi-model brainstorming into
production-grade software. Without one, agents guess. Guessing compounds.

## Core theorem

A spec is a **contract** between the human operator and the AI agents:
- Agents are bound to the scope
- Operator is bound to writing one before agents start

## The 6-element spec contract (every `spec.md` must have these six)

### 1. Outcomes
User- or business-observable results. Not features. Not technical decisions.

❌ "Implement JWT authentication"
✅ "A returning user can access their dashboard in ≤1.5s p95, without re-entering credentials, for 14 days after last login"

### 2. Scope Boundaries
Explicit IN and explicit OUT. The OUT list is usually more important than the IN list
because it prevents agents from over-reaching.

### 3. Constraints
Performance, budget, compliance, team size, platform. Numbers, not adjectives.

❌ "Must be scalable"
✅ "Must handle 5k concurrent users with p95 < 500ms on a single $40/mo VM until 50k paying users, at which point a re-architecture is acceptable"

### 4. Prior Decisions
Things already decided (from the debate conclusion). Agents must not re-litigate.
Each decision cites the source: `(Conclusion §5.2)`.

### 5. Task Breakdown
High-level. The `task-decomposer` agent fills in the details. Here just give phase-level
names and dependencies.

### 6. Verification Criteria
For every outcome, "done" is defined as: a specific test passing, a specific metric
hitting a number, or a specific human sign-off. No vague "works end-to-end".

## File manifest for every spec package

```
specs/NNN-<kebab-name>/
├── PRD.md                 # product-level, for humans
├── spec.md                # 6-element contract, for agents
├── architecture.md        # C4 L1/L2, tradeoffs
├── tech-stack.md          # pinned versions, excluded alternatives
├── non-goals.md           # tempting things we're NOT doing
├── risks.md               # risk register with owner
├── SLA.md                 # measurable targets
├── compliance.md          # if commercial/regulated
├── dependency-graph.mmd   # Mermaid DAG of tasks
├── tasks/
│   ├── T001.md
│   ├── T002.md
│   └── ...
└── open-questions.md      # anything awaiting moderator decision
```

## The adversarial review loop (MANDATORY for L/XL ideas)

```
spec-writer writes v0 ──► /codex:adversarial-review ──► N findings
                                                            │
                  ┌────────────────┬──────────────────┐     │
                  │                │                  │     │
              BLOCK (fix)   FOLLOW-UP (risks.md)   REJECT (document why)
                  │                                  │
                  └──────────► spec-writer v1 ◄─────┘
                                 │
                                 ▼
                  /codex:adversarial-review (round 2)
                                 │
                                 ▼
                  ... (up to 4 rounds) ...
                                 │
                                 ▼
                  STOP: Codex returns "no blocking issues"
                        OR 4 rounds reached (human decides)
```

## Anti-patterns (seen in real repos — don't do these)

### Anti-pattern 1: Spec-as-docstring
Writing 200-line docstrings inside `spec.md` describing the code.
Specs describe *behavior and contracts*, not implementation.

### Anti-pattern 2: The "we'll figure it out" spec
Scope boundaries like "scale as needed" or "secure enough". These are not constraints.

### Anti-pattern 3: Auto-generated spec from repo
ETH 2026 research: LLM-generated context files *lower* success rate by 0.5–2% and
raise cost 20%+. A spec must have a human in the loop; it's the whole point.

### Anti-pattern 4: Frozen spec
Specs don't ship once. They evolve with the code. Updating spec.md is a normal part
of implementation, not a sign of failure — but the update must be an explicit commit
that the operator reviews.

### Anti-pattern 5: Missing non-goals
A spec with empty `non-goals.md` is incomplete. Agents expand scope by default;
explicit non-goals are the only reliable brake.

### Anti-pattern 6: Verification = "it works"
"Verification: the feature works" is no verification. It must be a runnable command,
a metric with a number, or a checkbox the human signs.

## Lean patterns (do these)

### Pattern 1: One spec, many tasks
Never write a spec per task. Tasks derive from the spec. Updating the spec updates
all derived tasks' context automatically.

### Pattern 2: Number every non-functional requirement
Every latency, throughput, availability, durability target gets a number. Even if
the number is a guess, a guess is debatable. No number is not debatable.

### Pattern 3: Risks list has bus-factor-of-1 entry
Since you are a solo operator + AI team, add a mandatory risk: "operator unavailable
for >7 days → who or what takes over?". Mitigation might be "nobody, this risk is
accepted"; that's still better than silent.

### Pattern 4: Prior Decisions are quotes (paraphrased) from the conclusion
Every Prior Decision cites `conc/NNN-*.md` section. If you can't cite it, it's not
a prior decision — it's a new decision and belongs in spec.md explicitly.

### Pattern 5: SLAs differ by phase
v0.1 SLA ≠ v1.0 SLA. v0.1 might be "uptime best-effort, no SLA". v1.0 might be
"99.9% monthly with incident SLA of 1h response / 4h resolution". Specifying both
prevents premature over-engineering.

## Templates (copy into empty files)

### `spec.md` skeleton
```markdown
# Spec — Idea NNN · <title>

**Version**: 0.1  **Updated**: <ISO>  **Source**: conc/NNN-*.md

## 1. Outcomes
<observable results, numbered O1, O2, ...>

## 2. Scope Boundaries
### 2.1 In scope for v0.1
### 2.2 Explicitly out of scope for v0.1

## 3. Constraints
| # | Constraint | Source | Rigidity |
|---|------------|--------|----------|
| C1 | p95 < 500ms | SLA.md | Hard |
| C2 | Budget < $500/mo | Moderator note | Hard |

## 4. Prior Decisions (inherited from conclusion)
| # | Decision | Source |
|---|----------|--------|
| D1 | Backend in Go | conc §5.2 |
| D2 | Postgres for primary store, Redis for cache | conc §5.3 |

## 5. Task Breakdown (phases only; details in tasks/)
- Phase 0: Foundation (T001–T005)
- Phase 1: Core services (T010–T018)
- Phase 2: Integration (T020–T024)
- Phase 3: Polish (T030–T033)

## 6. Verification Criteria
| Outcome | Verification |
|---------|--------------|
| O1 | `pnpm test e2e/login.spec.ts` green AND p95 in Grafana dashboard < 1.5s |
| O2 | ... |

## Glossary
| Term | Meaning in this project |
|------|------------------------|
| "User" | <definition unique to this project> |

## Open Questions for Operator
(empty if none; otherwise list)
```

### `risks.md` skeleton
```markdown
# Risk Register — NNN

Format: each row has ID · Category · Likelihood · Impact · Trigger · Mitigation · Owner

## Technical
| ID | Risk | L | I | Trigger | Mitigation | Owner |
|----|------|---|---|---------|------------|-------|
| TECH-1 | DB lock contention at 2k writes/s | M | H | Write latency > 200ms | Shard by tenant | operator |

## Operational

## Security

## Commercial

## Legal / compliance

## Personnel (bus-factor)
| BUS-1 | Solo operator unavailable > 7 days | M | H | Operator absent | Document runbook; auto-scale off; email auto-reply | operator |
```

### `SLA.md` skeleton
```markdown
# SLA — NNN

## v0.1 (MVP, friends & family)
- Availability: best-effort
- p95 latency: < 2s for main flows
- Error rate: < 5%
- Support: informal
- No formal incident SLA

## v1.0 (commercial launch)
- Availability: 99.5% monthly (≤ 3.6h downtime/month)
- p95 latency: < 500ms for top 3 flows
- p99 latency: < 1.2s
- Error rate: < 0.5%
- Support SLA: 1h response / 4h resolution for P1
- Error budget policy: if exceeded, freeze features for 1 sprint

## How we measure
- Uptime: <monitoring tool + URL>
- Latency: <APM tool + dashboards>
- Error rate: <log query>
```
