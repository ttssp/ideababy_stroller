---
paths:
  - specs/**
---

# Rules for files under specs/

Loaded only when a session touches any file in `specs/`.

## Who can modify specs?

Only these agents:
- **Operator** (human) via direct edit or `/spec-from-conclusion`
- **spec-writer** subagent (invoked by `/spec-from-conclusion`)
- **task-decomposer** subagent (only for `tasks/*.md` and `dependency-graph.mmd`)

**Parallel-builder workers must NEVER modify `specs/*`.** If a build reveals that the
spec is wrong, the worker writes the blocker to its summary and stops. The operator
updates the spec, then re-dispatches.

## Before modifying spec.md

1. Read the current spec end-to-end. Summarize the change you're about to make.
2. If this spec has been adversarially reviewed by Codex, flag that the review may
   need to re-run after your change.
3. Spec changes must be paired with a commit message explaining the reason and
   the downstream impact (tasks that become invalidated, etc.).

## Versioning

`spec.md` carries a `**Version**` field in its header. Bump:
- Patch (0.1 → 0.1.1) for clarifications that don't change scope or outcomes
- Minor (0.1 → 0.2) for scope changes within the same phase
- Major (0.x → 1.0) at commercial launch milestones

Every version bump creates a git tag: `spec/NNN/v0.2`.

## Glossary discipline

Every term used in a domain-specific way must be in `spec.md §Glossary`. If you catch
yourself using a term that a new reader might misinterpret, stop and add it to the
glossary before proceeding.
