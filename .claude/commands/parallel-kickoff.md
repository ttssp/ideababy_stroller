---
description: Launch N parallel Claude Code worktrees, one per task, for a given idea
argument-hint: "<idea-number> <comma-separated-task-ids>  e.g. 001 T003,T004,T008"
allowed-tools: Read, Bash(git worktree:*), Bash(ls:*), Bash(cat:*), Bash(mkdir:*), Glob, Grep
model: opus
---

# Parallel Kickoff

Idea **$1**. Launch parallel worktrees for tasks: **$2**.

This command does **not** spawn Claude Code instances for you (that's a human action
in separate terminals). It prepares the worktrees, sanity-checks task independence,
and outputs copy-pasteable launch instructions.

## Step 1 — Read and validate tasks

Identify the project directory:
```bash
ls specs/$1-*/ | head -1
```

For each task ID in `$2`:
1. Read `specs/$1-*/tasks/<ID>.md`.
2. Extract the **file domain** (files/directories the task will touch).
3. Extract the **dependencies** field.

## Step 2 — Independence check (mandatory)

Produce a conflict matrix:

```
        T003 T004 T008
T003    —   ?    ?
T004    ?   —    ?
T008    ?   ?    —
```

For each pair, mark:
- ✅ if file domains disjoint
- ❌ if they overlap
- ⚠ if ambiguous (e.g. shared package.json)

**Stop and refuse to launch** if any cell is ❌. Tell the human:
"Task T00X and T00Y share file domain <path>. Split them further in spec before parallelizing,
or run them sequentially."

## Step 3 — Dependency check

For each task, verify that all its dependencies are either:
- ✅ Merged to `main` (check `git log --oneline main | grep "feat(<task-id>)"`)
- ✅ Another task being launched in this batch AND already listed before it

If any dependency is unmet, stop and tell the human which tasks to finish first.

## Step 4 — Prepare worktrees

For each task (in dependency order):

```bash
# From inside the project dir (cd into specs/$1-*/../projects/$1-*/ first)
claude --worktree task-<task-id>-<short-name>
```

**Do NOT** spawn them yourself. Instead, print a copy-pasteable block for the human:

```markdown
## Terminals to launch (in order)

### Terminal 1 — T003
cd projects/$1-*/
claude --worktree T003-<short-name>

### First message to paste inside Terminal 1's Claude Code:
Read @specs/$1-*/tasks/T003.md and enter plan mode.
Propose the implementation plan. Wait for my approval before executing.

### Terminal 2 — T004
...

### Terminal 3 — T008
...
```

## Step 5 — Offer Codex parallel option

Check if any tasks are tagged `recommended-model: codex-5.4` in their frontmatter.
If so, additionally print:

```markdown
## Codex-assigned tasks

### Terminal N — T007 (Codex)
cd projects/$1-*/
git worktree add ../T007-worktree -b T007-<short-name> main
cd ../T007-worktree
codex
# Paste:
Read AGENTS.md and specs/$1-*/tasks/T007.md. Enter plan mode.
```

## Step 6 — Produce launch summary

Print:
```
Parallel kickoff prepared for idea $1.
Tasks: T003 (Sonnet), T004 (Codex 5.4), T008 (Sonnet)
File domains verified disjoint.
Dependencies OK.

Open 3 terminals, paste the blocks above. I'll be waiting in this session as
the orchestrator — ping me when any worker needs synthesis.
```

## Notes
- Never exceed 5 concurrent worktrees. Merge overhead becomes the bottleneck.
- If you are on a Max 20x plan, 3 concurrent Claude sessions is comfortable; 5 pushes the rate limit.
- If a task exceeds 200 LOC estimate, split it before parallelizing.
