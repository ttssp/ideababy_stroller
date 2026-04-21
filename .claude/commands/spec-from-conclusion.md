---
description: Convert a reviewed conclusion into a full SDD spec package
argument-hint: "<idea-number>  (e.g. 001)"
allowed-tools: Read, Write, Edit, Bash(mkdir:*), Bash(ls:*), Bash(date:*), Glob, Grep, Agent(spec-writer)
model: opus
---

# Spec-from-Conclusion

Idea **$ARGUMENTS**. Convert the human-approved conclusion into a full Spec-Driven-Development
package that downstream build agents can consume without ambiguity.

## Precondition

Verify the conclusion exists and has been human-reviewed (contains `> 人工批注` or
`> Moderator note` markers somewhere):

```bash
ls conc/$ARGUMENTS-*.md 2>/dev/null
```

If not, stop and ask the human for the approved conclusion path.

## What to build

Create directory: `specs/$ARGUMENTS-<kebab-case-project-name>/` with these files:

| File | Purpose | Owner subagent |
|---|---|---|
| `PRD.md` | Product requirements (outcomes-first) | spec-writer |
| `spec.md` | The 6-element contract (outcomes, scope, constraints, decisions, tasks, verification) | spec-writer |
| `architecture.md` | C4-level 1 and 2 diagrams + key trade-off notes | spec-writer |
| `tech-stack.md` | Pinned versions, rationale, excluded alternatives | spec-writer |
| `dependency-graph.mmd` | Mermaid DAG of tasks; no code, just IDs | task-decomposer |
| `tasks/T001.md` … | One file per task with verification criteria | task-decomposer |
| `non-goals.md` | What this project intentionally does NOT solve | spec-writer |
| `risks.md` | Risk register with mitigation + owner | spec-writer |
| `SLA.md` | Measurable production targets (p95 latency, uptime, error budget) | spec-writer |

## Delegation

Step 1 — invoke `spec-writer` subagent:
> "Use the spec-writer subagent with inputs:
>   - conclusion file: `conc/$ARGUMENTS-Opus47Max-GPT54xHigh-byOpus47Max-*.md`
>   - target directory: `specs/$ARGUMENTS-<name>/`
>   - produce all files listed above EXCEPT tasks/ and dependency-graph.mmd"

Wait for it to return a summary.

Step 2 — invoke `task-decomposer` subagent:
> "Use the task-decomposer subagent on `specs/$ARGUMENTS-<name>/spec.md`.
>   Emit dependency-graph.mmd and tasks/T001.md through TNNN.md following the
>   task template. Maximum 30 tasks for v0.1; if more needed, slice into phases."

Step 3 — adversarial review gate (MANDATORY):
Run this in-session (not a subagent, because user may need to see streaming output):
```
/codex:adversarial-review specs/$ARGUMENTS-<name>/
  challenge every unstated assumption. focus on: concurrency, data consistency,
  failure recovery, auth boundary, supply-chain security, operational cost at 10x
  scale. assume the author has no large-project experience.
```

## Post-review loop

1. Read Codex's adversarial findings.
2. Classify each finding as:
   - **BLOCK** — spec must be updated (do it immediately with Edit)
   - **FOLLOW-UP** — track in `risks.md` as a known unknown
   - **REJECT** — disagree with Codex; document why in a new `## Opus rebuttal` section of the relevant file
3. After updates, re-run `/codex:adversarial-review` once more.
4. Stop when Codex returns "no blocking issues" OR after 4 iterations (whichever first).

## Output

Print a status table:
```
| File                     | Status | LOC |
|--------------------------|--------|-----|
| PRD.md                   | ✅     | 140 |
| spec.md                  | ✅     | 280 |
...
| Adversarial review rounds: 3
| Remaining Codex concerns: 0 blockers, 2 follow-ups (in risks.md)
```

Tell the human: "Spec ready at `specs/$ARGUMENTS-<name>/`. Run `/parallel-kickoff $ARGUMENTS <task-ids>` to start implementation."
