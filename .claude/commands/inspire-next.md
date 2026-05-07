---
description: Run L1R2 (Opus side) — read opponent's L1R1, run value-validation searches only (NO tech/feasibility searches), produce refined direction list. Only meaningful in mode=full; mode=narrow ends after L1R1.
argument-hint: "<idea-number>  e.g. 001"
allowed-tools: Read, Write, Bash(ls:*), Bash(date:*), Bash(mkdir:*), Bash(echo:*), WebSearch, WebFetch, Glob, Grep
model: opus
---

# Inspire · L1R2 (Opus side)

Idea **$ARGUMENTS**.

## Step 1 — preconditions

Verify both L1R1 files exist:
```bash
test -f discussion/$ARGUMENTS/L1/L1R1-Opus47Max.md
test -f discussion/$ARGUMENTS/L1/L1R1-GPT55xHigh.md
```

If either is missing, stop and tell the human:
> "Cannot run L1R2 — <which side> hasn't completed L1R1 yet. Run /status $ARGUMENTS to see what's pending."

## Step 2 — read in this order

1. `.claude/skills/inspire-protocol/SKILL.md` (L1R2 template)
2. `discussion/$ARGUMENTS/L1/L1-moderator-notes.md` (if exists; **binding injections**)
3. `discussion/$ARGUMENTS/L1/L1R1-GPT55xHigh.md` (opponent — all four parts)
4. `discussion/$ARGUMENTS/L1/L1R1-Opus47Max.md` (your own L1R1)

## Step 3 — run value-validation searches

**Allowed search categories** (cite URLs):
- "Has someone done X?" — prior art, products, projects
- "Do people want X?" — Reddit, HN, Stack Overflow complaints, surveys
- "Has X been tried & failed/succeeded?" — case studies, post-mortems, news

**FORBIDDEN search categories** (these belong to L4, not L1):
- Tech stack queries
- Architecture queries
- Cost / pricing queries
- Implementation difficulty queries

Run **≥3** value-validation searches across the most promising directions
from both sides' L1R1s. Don't search every direction — focus on the ones with
real "spark" and on directions where prior art is genuinely unclear.

## Step 4 — write Opus's L1R2

Target: `discussion/$ARGUMENTS/L1/L1R2-Opus47Max.md`

Use the L1R2 5-section template from the protocol:
1. From opponent's L1R1, directions I also find compelling (≤3)
2. From opponent's L1R1, directions I'd push back on (≤3, honest)
3. Value-validation search results (table with URLs)
4. My refined Top 3 (may differ from R1)
5. New directions sparked by reading opponent's R1 (if any)

Length: 500–900 words. Heavy on §3 and §4.

## Step 5 — write Codex inbox task

Compute timestamp `$(date -u +%Y%m%dT%H%M%S)`.
Queue id: `QUEUE=$ARGUMENTS` (L1 lives at idea root).

Ensure queue dirs:
```bash
mkdir -p .codex-inbox/queues/$ARGUMENTS .codex-outbox/queues/$ARGUMENTS
```

Write `.codex-inbox/queues/$ARGUMENTS/<TS>-$ARGUMENTS-L1R2.md`:

```markdown
# Codex Task · idea $ARGUMENTS · L1R2

**Queue**: $ARGUMENTS
**Created**: <ISO>
**Recommended model**: gpt-5.5
**Recommended reasoning_effort**: xhigh
**Estimated tokens**: ~6-12k
**Kickoff form**: reuse-session   ← 默认（R2 与 R1 上下文重叠 ~80%；oneshot 也能跑）

## Session hint (only meaningful if Codex reuses session from L1R1)
你已读过：proposals/$ARGUMENTS, .claude/skills/inspire-protocol/SKILL.md,
discussion/$ARGUMENTS/L1/L1R1-GPT55xHigh.md（自己的 R1）。
本轮新增需读：
- discussion/$ARGUMENTS/L1/L1R1-Opus47Max.md  ← 对方的 R1
- discussion/$ARGUMENTS/L1/L1-moderator-notes.md（如存在）
**HARD CONSTRAINT (reuse only)**: do NOT re-read files you read in the previous
round of this Codex session unless this task explicitly lists them above.

## Your role
You are GPT-5.5 xhigh, Debater B, L1R2 on idea $ARGUMENTS. Read opponent's
L1R1, run value-validation searches only, produce a refined direction list.

## CONSTRAINTS
- VALUE-VALIDATION SEARCH ONLY:
    Allowed: prior art / user demand / failure cases
    Forbidden: tech stack / architecture / cost / feasibility
- Quote ≤15 words verbatim from any source

## Read in order
1. .claude/skills/inspire-protocol/SKILL.md
2. discussion/$ARGUMENTS/L1/L1-moderator-notes.md (if exists; binding)
3. discussion/$ARGUMENTS/L1/L1R1-Opus47Max.md (opponent — all four parts)
4. your own L1R1 (discussion/$ARGUMENTS/L1/L1R1-GPT55xHigh.md)

## Search
≥3 value-validation searches. Cite URLs.

## Write
discussion/$ARGUMENTS/L1/L1R2-GPT55xHigh.md using the L1R2 5-section template.
500-900 words.

## When done
Write .codex-outbox/queues/$ARGUMENTS/<TS>-$ARGUMENTS-L1R2.md with:
  - Files written + word count
  - Top 3 in your refined §4
  - Any directions you abandoned (with reason)
  - Note for Claude Code if needed
```

Update queue HEAD pointer:
```bash
echo "<TS>-$ARGUMENTS-L1R2.md" > .codex-inbox/queues/$ARGUMENTS/HEAD
```

## Step 6 — output next-step menu

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ L1R2 Opus side done.
File: discussion/$ARGUMENTS/L1/L1R2-Opus47Max.md (<word-count> words)
Searches run: <n> value-validation queries

Key updates this round:
  · Validated: <direction or claim that prior art supports>
  · Weakened: <direction or claim that evidence undermines>
  · New: <any direction sparked by reading opponent>

📋 Next step (两种 kickoff 形态任选):

[1] (默认) 在已开的 Codex 终端复用 L1R1 会话 — 省 ~60% token
    → 粘贴这段进 Codex 终端：

    ```
    继续 idea $ARGUMENTS 的 L1R2。
    本轮只新读：
    - discussion/$ARGUMENTS/L1/L1R1-Opus47Max.md
    - discussion/$ARGUMENTS/L1/L1-moderator-notes.md (如存在)
    然后按 .codex-inbox/queues/$ARGUMENTS/HEAD 指向的任务文件执行；
    把结果写到 .codex-outbox/queues/$ARGUMENTS/<HEAD-content>.md。
    禁止重读你已读过的其他文件。
    ```

[2] 新开 Codex 终端从零跑 (oneshot, 适合 R1 跑完很久 / 已退出)
    → in your Codex terminal:  cdx-run $ARGUMENTS

[3] Show Codex kickoff for manual paste
    → cdx-peek $ARGUMENTS

[4] Show me Opus's L1R2 first
    → I'll display discussion/$ARGUMENTS/L1/L1R2-Opus47Max.md

[5] Inject a moderator note before Codex runs
    → tell me what to add

[6] Skip Codex L1R2 and synthesize what we have
    → /inspire-advance $ARGUMENTS  (will note Codex L1R2 missing)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Reply 1/2/3/4/5/6 or describe what you want.
```
