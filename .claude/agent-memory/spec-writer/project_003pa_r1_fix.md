---
name: 003-pA R1 fix pattern
description: How spec v0.2 resolved R1 adversarial review BLOCK verdict via D-OP1/D-OP2/D-OP3 operator decisions
type: project
---

003-pA spec bumped to v0.2 on 2026-04-24 to absorb R1 adversarial review (BLOCK · 3 blocker + 5 high + 4 med-low).

Why: Codex gpt-5.4 xhigh flagged contract gaps that would let builders ship a broken MVP. Operator pre-approved three key decisions before spec-writer round:
- D-OP1 USD < $30 = real hard cap → proxy pre-estimate + pre-reject (402/429), 60s polling SIGINT demoted to second line of defense
- D-OP2 `.claude/` fail-closed → MacFUSE+bindfs preferred, chflags/chattr fallback, pure chmod rejected as prod path, refuse-to-start if neither available (new OQ5)
- D-OP3 C9 cross-machine portability narrowed to "manual rsync + re-run training on remote"; cross-machine resume explicitly not supported (C22)

How to apply: When spec needs post-review fixes in this repo, look for operator pre-decisions in the review dispatch message first (operator tends to resolve ambiguous trade-offs upstream). Blocker #1 (stuck state machine) was resolved by making architecture.md §8 the single source of truth with explicit sampling period (5s), window semantics, transition table, disk_io threshold (>1 MB/s), cold-start exemption behavior, false-negative classification, and needs_human_review persistence (stuck_lock file). Model routing is NOT a spec concern — flag to task-decomposer R2 via risks.md R11 instead.
