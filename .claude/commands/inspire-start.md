---
description: Start L1 Inspire phase. Opus writes L1R1 (daydream, no search, four-section). Three modes — full (default, deep exploration), narrow (1-round only, close variations), or skip (bypass L1, go straight to L2 with proposal as direction).
argument-hint: "<idea-number> [--mode=full|narrow|skip]  e.g. 001  or  001 --mode=narrow"
allowed-tools: Read, Write, Bash(mkdir:*), Bash(cp:*), Bash(mv:*), Bash(ls:*), Bash(date:*), Bash(echo:*), AskUserQuestion, Glob, Grep
model: opus
---

# Inspire · L1R1 (Opus side)

Idea **$ARGUMENTS** (parse for `--mode=` flag; default `full`).

## Step 1 — parse args & verify proposal exists

If proposal `**NNN**` does not exist in `proposals/proposals.md`, stop and tell
human to `/propose` first.

## Step 2 — confirm mode if not specified

If human didn't pass `--mode=`, use AskUserQuestion to decide:

```
Question: How much exploration do you want at L1?
Options:
  - full   → 2 rounds, 8-15 inspired directions (default if proposal is vague)
  - narrow → 1 round, 4-6 close variations (proposal is fairly clear)
  - skip   → bypass L1, go straight to L2 (proposal is sharp; L2 will fold L1's
            value in by including "alternative framings considered")
```

## Step 3 — branch by mode

### If `--mode=skip`
Don't run L1. Output a brief explanation and tell human:
```
[A] Run /explore-start NNN now (L2 will include alternative-framings section)
[B] Cancel — actually I want some L1 exploration; re-run with --mode=narrow
```
Stop here.

### Else (full or narrow):

## Step 4 — setup

```bash
mkdir -p discussion/$NNN/L1
test -f .claude/skills/inspire-protocol/SKILL.md && cp .claude/skills/inspire-protocol/SKILL.md discussion/$NNN/L1/PROTOCOL.md
```

(The PROTOCOL.md copy is a local snapshot for the debaters and for human readability.)

## Step 5 — write Opus's L1R1

**HARD CONSTRAINTS**:
1. **NO web search this round.** No WebSearch, no WebFetch. Pure imagination + memory.
2. **DO NOT read GPT-5.5's L1R1.** Verify with `ls discussion/$NNN/L1/`.
3. **No technical/feasibility content.** Just value/novelty/utility.

Read:
- `proposals/proposals.md` entry NNN
- `.claude/skills/inspire-protocol/SKILL.md` (or local PROTOCOL.md)
- `CLAUDE.md`

Write `discussion/$NNN/L1/L1R1-Opus47Max.md` using the L1R1 four-section template
(A adjacent / B extended / C reframed / D top 3 with spark).

Counts based on mode:
- `full`: 3-5 adjacent, 2-3 extended, 2-3 reframed, top 3 in Part D
- `narrow`: 3 adjacent, 1-2 extended, 1-2 reframed, top 2-3 in Part D

Length: 600-1200 words (full) or 400-700 words (narrow).

## Step 6 — write Codex inbox task

Compute timestamp: `$(date -u +%Y%m%dT%H%M%S)`
Queue id: `QUEUE=$NNN` (L1 always lives at idea root, never on a fork).

Ensure queue dir exists:
```bash
mkdir -p .codex-inbox/queues/$NNN
```

Write `.codex-inbox/queues/$NNN/<TS>-$NNN-L1R1.md`:

```markdown
# Codex Task · idea $NNN · L1R1 (Inspire R1)

**Queue**: $NNN
**Created**: <ISO>
**Mode**: <full|narrow>
**Recommended model**: gpt-5.5
**Recommended reasoning_effort**: xhigh
**Estimated tokens**: ~5-10k
**Kickoff form**: oneshot

## Your role
You are GPT-5.5 xhigh, Debater B in a two-model debate on idea $NNN at the
L1 Inspire layer. Your job is to expand the idea space — produce inspired
directions adjacent to, extended from, or reframed from the proposal.

## HARD CONSTRAINTS
- NO web search this round (no WebSearch, no WebFetch)
- DO NOT read discussion/$NNN/L1/L1R1-Opus47Max.md (parallel independence)
- NO technical/feasibility content (no architecture, no stack, no cost talk)

## Read (only these)
- proposals/proposals.md — find entry **$NNN**
- .claude/skills/inspire-protocol/SKILL.md (or discussion/$NNN/L1/PROTOCOL.md)
- AGENTS.md

## Write
discussion/$NNN/L1/L1R1-GPT55xHigh.md using the L1R1 four-section template
from the protocol.

Mode = <full|narrow>:
- <if full>:  3-5 adjacent · 2-3 extended · 2-3 reframed · top 3 in Part D · 600-1200 words
- <if narrow>: 3 adjacent · 1-2 extended · 1-2 reframed · top 2-3 in Part D · 400-700 words

## When done
Write `.codex-outbox/queues/$NNN/<TS>-$NNN-L1R1.md` confirming:
  - Files written and word count
  - Top 3 directions you put in Part D (one line each)
  - Anything Claude Code should know about
```

Update queue HEAD pointer:
```bash
mkdir -p .codex-outbox/queues/$NNN
echo "<TS>-$NNN-L1R1.md" > .codex-inbox/queues/$NNN/HEAD
```

## Step 7 — output next-step menu

Display:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ L1R1 Opus side done.
File: discussion/$NNN/L1/L1R1-Opus47Max.md (<word-count> words)
Mode: <full|narrow>

Top 3 directions I put in Part D:
1. <name> — <one line>
2. <name> — <one line>
3. <name> — <one line>

📋 Next step: get Codex's L1R1 (queue=$NNN is ready).

[1] (默认) 新开 Codex 终端跑 (oneshot — idea 第一次接触)
    → in your Codex terminal:  cdx-run $NNN

[2] 在已开的 Codex 终端粘贴自包含 prompt (reuse-session — 收益有限，
    仅当你已经在用同一 Codex 会话连贯讨论这个 idea 时才有意义)
    → cdx-peek $NNN  看到任务全文后粘贴

[3] I want to inject a steering note before Codex starts
    → tell me what to add and I'll write it to L1-moderator-notes.md

[4] Show me the full Codex kickoff so I can paste manually
    → cdx-peek $NNN

[5] Show me Opus's L1R1 first
    → I'll show discussion/$NNN/L1/L1R1-Opus47Max.md

[6] Cancel — I want to revise the proposal first
    → /propose or edit proposals.md directly

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Reply 1/2/3/4/5/6 or describe what you want.
```

## Notes for the Opus orchestrator (you, while running this command)

- This is L1, not L4. If you find yourself drafting tech architecture or
  feasibility analysis, **stop and rewrite** — that content belongs in L4.
- Be willing to sound bold. The point of L1R1 is to show the human possibilities
  they didn't see, not to be defensible.
- Your Part D entries should each include "why human probably didn't think of
  this themselves" — this is the inspirational core.
