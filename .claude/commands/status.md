---
description: Show the full state tree of an idea — which layers done, which forks active, what Codex owes, what's next. Always shows the next-step menu so human knows what to do.
argument-hint: "<idea-number-or-fork-id>  e.g. 001  or  001a  (omit to see all)"
allowed-tools: Read, Bash(ls:*), Bash(find:*), Bash(cat:*), Bash(stat:*), Bash(date:*), Glob, Grep
model: sonnet
---

# Status · idea state tree

Show what's happening with idea **$ARGUMENTS** (or all ideas if no argument).

## Step 1 — figure out scope

If `$ARGUMENTS` is empty → list all ideas in `proposals/proposals.md` and show
each top-level idea's headline status (one line each).

If `$ARGUMENTS` is `NNN` (e.g. `001`) → show the full tree under `discussion/NNN/`,
including all forks.

If `$ARGUMENTS` is a fork id like `NNN-fork` → show that subtree only.

## Step 2 — gather facts

```bash
# Which ideas exist
ls discussion/ 2>/dev/null

# For target idea, walk the tree
find discussion/$ARGUMENTS -type d 2>/dev/null
find discussion/$ARGUMENTS -name "stage-*.md" 2>/dev/null
find discussion/$ARGUMENTS -name "FORK-ORIGIN.md" 2>/dev/null
```

For each layer dir (L1/, L2/, L3/, L4/) found:
- Count rounds present per side (Opus and GPT)
- Check if `stage-L<n>-*.md` synthesis exists
- Last modified timestamp

For pending Codex tasks (v2 — multi-queue):
```bash
# 列出所有队列及当前 HEAD，并标注是否已被 Codex 完成
for d in .codex-inbox/queues/*/; do
  q=$(basename "$d")
  h=$(cat "$d/HEAD" 2>/dev/null)
  [ -z "$h" ] && continue
  if [ -f ".codex-outbox/queues/$q/$h" ]; then
    echo "$q  HEAD=$h  ✅ done"
  else
    echo "$q  HEAD=$h  ⏸ pending"
  fi
done
```

每个 idea / fork 都有自己的队列，多个 idea 并行时彼此独立。
判断规则：`queues/<id>/HEAD` 指向的任务文件**不存在于** outbox 对应路径 → 该
队列有未读 Codex 任务（需要 `cdx-run <id>`）。

如果 `$ARGUMENTS` 是具体 idea / fork-id，仅看对应队列即可（其他队列对它无意义）。

## Step 3 — render the tree

Use this format (no headers, just a clean ASCII tree + status badges):

```
Idea 001 · "Real-time collab whiteboard for educators"
Status: in L2-explore (fork: 001a)

discussion/001/
├── L1 · Inspire ✅ done
│   └── stage-L1-inspire.md  (10 directions, 3 selected for fork)
│
├── 001a [forked from L1 #3, 2 days ago]
│   └── L2 · Explore ⏳ in progress
│       ├── L2R1 ✅ both done
│       └── L2R2 ⏸ Opus done · Codex pending
│
├── 001b [forked from L1 #5, 2 days ago]  ⏸ parked
│   └── L2 · Explore — only L2R1 Opus done
│
└── 001c [forked from L1 #7, 1 day ago]
    └── L2 · Explore ⏳ in progress
        └── L2R1 ⏸ both done

Last action: Opus completed L2R2 for 001a, 12 minutes ago
Pending Codex: 1 inbox task (001a-L2R2) waiting for cdx-run
```

Status badges:
- ✅ = done
- ⏳ = in progress
- ⏸ = paused / waiting
- ⛔ = blocked
- 🅿️ = parked
- ❌ = abandoned

## Step 4 — next-step menu (always show this)

Based on the most recent action and what's missing, suggest the most likely next step:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 Suggested next steps:

[1] Wait for Codex 001a-L2R2 (queue=001a is pending)
    → in your Codex terminal: cdx-run 001a

[2] Check Opus's L2R2 output in 001a
    → I'll show you discussion/001/001a/L2/L2R2-Opus47Max.md

[3] Move 001c forward (next round needed)
    → /explore-next 001c 2

[4] Fork another direction from L1 menu
    → /fork 001 from-L1 direction-X as 001d

[5] Park the entire 001 tree (preserve all artifacts)
    → /park 001

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Reply 1/2/3/4/5 or describe what you want to do.
```

The menu items are computed dynamically from what the tree state actually allows.
Don't show options that don't apply (e.g. don't show "L4 plan" if no L3 done yet).

## Style

- Output is for humans skim-reading; use tree characters and badges, not paragraphs
- Always end with the menu — never just dump status without saying what's next
- If multiple ideas have pending work, list them in order of "most recently active"
