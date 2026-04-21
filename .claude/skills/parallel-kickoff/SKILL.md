---
name: parallel-kickoff
description: Orchestration patterns for running multiple Claude Code and Codex sessions in parallel via git worktrees. Load when planning or executing parallel task dispatch, when the user asks to "parallelize", "kick off workers", "fan out tasks", or "use worktrees".
allowed-tools: Read, Bash(git worktree:*), Bash(ls:*), Glob, Grep
disable-model-invocation: false
---

# Parallel Kickoff — SOPs

How to actually run 3–5 AI workers at once without creating a merge nightmare.

## When to parallelize (decision rule)

Parallelize task T and T' only when **ALL** are true:
1. `depends_on(T) ∩ depends_on(T') = ∅` (no hidden shared dep)
2. `file_domain(T) ∩ file_domain(T') = ∅` (strict, no "but package.json is shared")
3. Neither generates code the other must import (use interface stubs if needed)
4. Both can verify themselves independently (no shared integration test they race on)

If any is false → sequentialize.

## The "shared file" problem

Most parallel-kickoff failures come from ignored shared files:
- `package.json` / `pnpm-lock.yaml`
- `tsconfig.json`
- `.env.example`
- `prisma/schema.prisma` (if shared ORM)
- `src/index.ts` (monorepo entry point)
- CI config (`.github/workflows/*.yml`)

**Rule**: changes to shared files go into dedicated "infrastructure" tasks in Phase 0
that other tasks depend on. No parallel worker edits shared files.

## Disjointness verification script

Before launching, run:

```bash
# ./scripts/check-disjoint.sh T003 T004 T008
#!/usr/bin/env bash
set -euo pipefail

for id in "$@"; do
  task_file="specs/*/tasks/${id}.md"
  # Extract file_domain lines (simple yaml-ish parsing)
  rg -N "^\s+-\s+(.+)$" -r '$1' $task_file -A 20 | head -20
done | sort | uniq -c | sort -rn | awk '$1 > 1 {print}'

# Any output = collision. No output = safe to parallelize.
```

## Worktree hygiene

### Create one worktree per task
```bash
# From the project dir
claude --worktree T003-auth-service
# In parallel terminal:
claude --worktree T004-chat-service
# Codex side:
git worktree add ../T007-notify -b T007-notify main
cd ../T007-notify && codex
```

### .worktreeinclude (copy .env etc. into each worktree)
Create at project root:
```
.env
.env.local
*.secrets
config/master.key
```

### .gitignore
```
.claude/worktrees/
```

### Clean up when done
Claude Code auto-cleans empty worktrees. For manual management:
```bash
git worktree list
git worktree remove ../T003-auth-service
git branch -d T003-auth-service
```

### Abandoned worktree recovery
```bash
# See orphans
find .claude/worktrees -maxdepth 1 -mindepth 1 -type d

# If Claude crashed mid-session, worktrees with uncommitted changes persist.
# Claude Code auto-cleans safe (clean, older than cleanupPeriodDays) ones at startup.
```

## Recommended concurrency by plan

| Subscription | Safe concurrent Claude Code sessions | Notes |
|---|---|---|
| Pro | 1 | 5-hr limit hits fast |
| Max 5x | 2–3 | Watch `/cost` |
| Max 20x | 3–5 | Sweet spot for this workflow |
| API-only | Limited by rate limit, not subscription | |
| Codex (ChatGPT Pro) | 2–3 additional on top | |

**Practical recommendation**: 3 Claude + 1 Codex + 1 Spark for mini-tasks = 5 total
workers, which is about the max a solo operator can orchestrate anyway.

## Merge strategy (after workers finish)

Merge in **dependency order**, not completion order:

```bash
# Suppose T003 was phase-0-foundation, T004 and T008 are phase-1
git checkout main
git merge T003-auth-service --no-ff           # foundational first
git merge T004-chat-service --no-ff
git merge T008-notifications --no-ff

# At each step, if conflicts:
#   STOP. Don't paper over.
#   The conflict means file_domain disjointness was violated.
#   Fix the spec; rerun those tasks.
```

## Status dashboard pattern

Create `.agent-status/` in the main worktree. Each worker writes a JSON:

```json
// .agent-status/T003.json
{
  "status": "in-progress|complete|blocked",
  "started": "2026-04-21T10:00:00Z",
  "updated": "2026-04-21T11:15:00Z",
  "files_changed": ["src/auth/token.ts", "tests/auth/token.test.ts"],
  "verification_passed": false,
  "blockers": []
}
```

Main orchestrator session reads these to know when to synthesize.

## Inter-task communication

Workers **do not** talk to each other. If coordination is needed:
1. Define the interface in Phase 0 (e.g. a TypeScript type file shared via the main worktree)
2. Each worker imports from the interface, never from another worker's code
3. Merge in dependency order so imports resolve by the time integration happens

## When parallelism is the wrong tool

- Task count < 3 → just do it sequentially, less overhead
- Single-file feature → no benefit
- Tight integration with moving parts → worktrees don't help, agent teams might (experimental)
- You are still learning the codebase → parallelism amplifies mistakes

## Debugging "workers drifting out of scope"

Symptoms: a worker starts editing files outside its `file_domain`.
Cause: task spec was ambiguous OR worker got confused mid-session.

Fix:
1. Stop the worker immediately
2. Re-check the task spec — does it clearly state file_domain?
3. If task spec is clear, restart the worker with an explicit prompt:
   ```
   Re-read tasks/T003.md. Your file_domain is STRICTLY [list].
   If your current plan requires editing outside this list, STOP and report
   instead of editing.
   ```
4. If the worker was right to need those files, the task was under-specified;
   update spec.md and task file before resuming.
