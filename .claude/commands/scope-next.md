---
description: Run L3R2 (Opus side) — read opponent's L3R1, run scope-reality searches (what similar products include/exclude at v0.1), produce refined candidates + identify the one biggest tradeoff human must decide.
argument-hint: "<fork-id-or-idea-number>  e.g. 001a"
allowed-tools: Read, Write, Bash(ls:*), Bash(date:*), Bash(mkdir:*), Bash(echo:*), WebSearch, WebFetch, Glob, Grep
model: opus
---

# Scope · L3R2 (Opus side)

Idea **$ARGUMENTS**.

## Step 1 — preconditions

```bash
ls discussion/.../<target>/L3/L3R1-*.md
```

Need both `L3R1-Opus47Max.md` and `L3R1-GPT54xHigh.md`.
Need `L3R0-intake.md`.
If any missing, stop and tell human (`/status <target>`).

## Step 2 — read in order

1. `.claude/skills/scope-protocol/SKILL.md` (L3R2 template)
2. `discussion/.../<target>/L3/moderator-notes.md` (if exists; binding)
3. `discussion/.../<target>/L3/L3R0-intake.md` (re-check hard constraints)
4. `discussion/.../<target>/L3/L3R1-GPT54xHigh.md` (opponent, all sections)
5. `discussion/.../<target>/L3/L3R1-Opus47Max.md` (self)
6. `discussion/.../<target>/L2/stage-L2-explore-<target>.md` (context)

## Step 3 — scope-reality searches

**Allowed**:
- "What do products in [category] typically include at v0.1 / launch?"
- "What's the minimum viable feature set for [category] users?"
- "What did [similar product] ship first vs add later?"
- "What features does [similar product] NOT have and users don't miss?"

**Forbidden** (L4 territory):
- Tech stack queries
- Architecture queries
- Specific library / framework comparisons
- Pricing/cost of tools

Run **≥3** scope-reality searches. Cite URLs. ≤15 word quotes.

## Step 4 — write Opus's L3R2

Target: `discussion/.../<target>/L3/L3R2-Opus47Max.md`

Use L3R2 template:
- §1 From opponent's candidates — what sharpened my thinking
- §2 Scope-reality searches (table with URLs)
- §3 Refined candidates (2-3, each with full structure — sharpened from R1)
- §4 **The single biggest tradeoff** human must decide (name the axis)
- §5 What I'm less sure about now than in R1

Length: 600-1000 words. Heavy on §2, §3, §4.

## Step 5 — write Codex inbox task

Compute timestamp.
Queue id: `QUEUE=<target>`.

Ensure queue dirs:
```bash
mkdir -p .codex-inbox/queues/<target> .codex-outbox/queues/<target>
```

Write `.codex-inbox/queues/<target>/<TS>-<target>-L3R2.md`:

```markdown
# Codex Task · <target> · L3R2

**Queue**: <target>
**Created**: <ISO>
**Recommended model**: gpt-5.4
**Recommended reasoning_effort**: xhigh
**Estimated tokens**: ~8-14k
**Kickoff form**: reuse-session   ← 默认（R2 与 R1 上下文重叠 ~80%）

## Session hint (only meaningful if Codex reuses session from L3R1)
你已读过：scope-protocol SKILL, L3R0-intake.md, 自己的 L3R1, L2 stage doc.
本轮新增需读：
- discussion/.../<target>/L3/L3R1-Opus47Max.md  ← 对方的 R1
- discussion/.../<target>/L3/moderator-notes.md（如存在）
**HARD CONSTRAINT (reuse only)**: do NOT re-read files you read in the previous
round of this Codex session unless this task explicitly lists them above.

## Your role
You are GPT-5.4 xhigh, L3R2 on idea <target>. Read opponent's candidates,
search scope-reality, refine candidates, identify the key tradeoff axis.

## CONSTRAINTS
- SCOPE-REALITY SEARCH ONLY:
    Allowed: "what do similar products include/cut at v0.1"
    Forbidden: tech stack / architecture / specific implementations
- Quote ≤15 words verbatim

## Read in order
- .claude/skills/scope-protocol/SKILL.md
- discussion/.../<target>/L3/moderator-notes.md (if exists; binding)
- discussion/.../<target>/L3/L3R0-intake.md
- discussion/.../<target>/L3/L3R1-Opus47Max.md (opponent)
- your own L3R1
- discussion/.../<target>/L2/stage-L2-explore-<target>.md (context)

## Search
≥3 scope-reality queries. Cite URLs.

## Write
discussion/.../<target>/L3/L3R2-GPT54xHigh.md using the L3R2 template:
- §1 What sharpened from opponent
- §2 Scope-reality search (table)
- §3 Refined candidates (2-3)
- §4 Single biggest tradeoff axis
- §5 What I'm less sure about now

600-1000 words.

## When done
Write .codex-outbox/queues/<target>/<TS>-<target>-L3R2.md with:
- Files written + word count
- Each refined candidate headline
- What the key tradeoff axis is (§4)
- Notable scope-reality findings
- Anything Claude Code should know
```

Update queue HEAD pointer:
```bash
echo "<TS>-<target>-L3R2.md" > .codex-inbox/queues/<target>/HEAD
```

## Step 6 — output next-step menu

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ L3R2 Opus side done.
File: discussion/.../<target>/L3/L3R2-Opus47Max.md (<n> words)
Scope-reality searches: <n> queries across <k> sources

Opus's key tradeoff axis (§4): <one line>
Refined candidates: <count> (down from/up from L3R1)

📋 Next step (两种 kickoff 形态任选):

[1] (默认) 在已开的 Codex 终端复用 L3R1 会话 — 省 ~60% token
    → 粘贴这段进 Codex 终端：

    ```
    继续 idea <target> 的 L3R2。
    本轮只新读：
    - discussion/.../<target>/L3/L3R1-Opus47Max.md  (对方 R1)
    - discussion/.../<target>/L3/moderator-notes.md (如存在)
    然后按 .codex-inbox/queues/<target>/HEAD 指向的任务文件执行；
    把结果写到 .codex-outbox/queues/<target>/<HEAD-content>.md。
    禁止重读你已读过的其他文件。
    ```

[2] 新开 Codex 终端从零跑 (oneshot)
    → in your Codex terminal:  cdx-run <target>

[3] Show Codex kickoff for manual paste
    → cdx-peek <target>

[4] Show me Opus L3R2 first
    → I'll show the file

[5] Inject a moderator note before Codex
    → tell me what to add

[6] Skip Codex L3R2 and synthesize what we have
    → /scope-advance <target>  (will note Codex L3R2 missing)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Reply 1/2/3/4/5/6 or describe.
```
