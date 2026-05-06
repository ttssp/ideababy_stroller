---
description: Run L2R2 (Opus side) — read opponent's L2R1, run value-validation searches only, produce sharpened picture + open questions for L3.
argument-hint: "<fork-id-or-idea-number>  e.g. 001a"
allowed-tools: Read, Write, Bash(ls:*), Bash(date:*), Bash(mkdir:*), Bash(echo:*), Bash(test:*), Bash(stat:*), WebSearch, WebFetch, Glob, Grep
model: opus
---

# Explore · L2R2 (Opus side)

Idea **$ARGUMENTS**.

## Step 0 — active redebate detector（最小侵入）

```bash
test -f discussion/.../<target>/L2/.redebate-active
```

若存在，读取一行格式 `<next_v>|<start_iso>|<reason>` 并取出 `next_v`（如 `v2`）。
此时本轮 R2 是 **redebate v2 的 R2**：

- 行为与标准 R2 相同（读对方 R1 + 搜索 + 写自己 R2 + 写 Codex inbox）
- 但在 §3 search 之前，**先额外读** `discussion/.../<target>/L2/_archive/v<prev>/stage-L2-explore-<target>.md`
  作为 baseline 参考（仅判断 framing 是否变化，不抄袭）
- §4 "Refined picture" 必须明确写一段 "vs baseline ${prev_v}: <what shifted>"
- Codex inbox 任务的标题加 "redebate ${next_v}"，frontmatter 加
  `**Redebate**: ${next_v} (in-place)` 字段
- 若文件 stat mtime > 24h 前（stale session）→ 提示用户：
  > "检测到 stale .redebate-active（>24h）。请先 /explore-redebate <target>
  >  选择 [继续/回滚/强制完成] 之一，再跑 explore-next。"

若文件不存在，按标准 L2R2 流程跑（下文不变）。

## Step 1 — preconditions

Verify both L2R1 files exist:
```bash
ls discussion/.../<target>/L2/L2R1-*.md
```

Need both `L2R1-Opus47Max.md` and `L2R1-GPT54xHigh.md`.
If either missing, stop and tell human (`/status <target>` to see state).

> Redebate context: 如果 Step 0 检测到 active redebate，确认 L2R1 文件是
> redebate 的新版（应在 .redebate-active 写入后被 explore-redebate 覆盖产出）。
> 旧版本应在 `_archive/v<prev>/L2R1-*.md`。

## Step 2 — read in order

1. `.claude/skills/explore-protocol/SKILL.md` (L2R2 template)
2. `discussion/.../<target>/L2/moderator-notes.md` (if exists; binding)
3. `discussion/.../<target>/L2/L2R1-GPT54xHigh.md` (opponent — all sections)
4. `discussion/.../<target>/L2/L2R1-Opus47Max.md` (your own L2R1)
5. (If forked) `discussion/<root>/L1/stage-L1-inspire.md` for L1 context
6. **(Redebate only)** `_archive/v<prev>/stage-L2-explore-<target>.md` — baseline 参考

## Step 3 — value-validation searches only

**Allowed**:
- Prior art (products, services, projects)
- Demand signals (Reddit, HN, surveys, complaints)
- Failure cases (post-mortems, shutdowns, pivots)

**Forbidden** (these are L3/L4 questions):
- Tech stack queries
- Architecture decisions
- Cost / pricing models
- Implementation difficulty

Run **≥3** value-validation searches across the most concrete claims from
either side's L2R1. Don't search every claim — focus on ones where evidence
will most clarify the picture.

## Step 4 — write Opus's L2R2

Target: `discussion/.../<target>/L2/L2R2-Opus47Max.md`

Use L2R2 template:
- §1 What sharpened my thinking from opponent's L2R1 (≥3 specific things)
- §2 Where I'd push back (up to 3, honest)
- §3 Search-based reality check (table with URLs)
- §4 Refined picture (1-2 paragraphs — sharpened version of the idea)
  - **(Redebate only)** 在 §4 末尾加一段 "vs baseline ${prev_v}: <framing 是否变化、变化在哪>"
- §5 Open questions L2 cannot answer (for L3 / user research)
- §6 Three things I'd want a real user interview to ask

Length: 600-1100 words（redebate 时 700-1200，多出来部分给 §4 vs-baseline）。Heavy on §3 and §4.

## Step 5 — write Codex inbox task

Compute timestamp `$(date -u +%Y%m%dT%H%M%S)`.
Queue id: `QUEUE=<target>`.

Ensure queue dirs:
```bash
mkdir -p .codex-inbox/queues/<target> .codex-outbox/queues/<target>
```

Write `.codex-inbox/queues/<target>/<TS>-<target>-L2R2.md` with the full Codex
L2R2 kickoff (template in explore-protocol SKILL.md §"L2R2 Codex kickoff").
Frontmatter must include:
```
**Queue**: <target>
**Kickoff form**: reuse-session   ← 默认（R2 与 R1 上下文重叠 ~80%）
```

**Redebate only**：filename 改为 `<TS>-<target>-L2R2-redebate-${next_v}.md`。
Frontmatter 额外加：
```
**Redebate**: ${next_v} (in-place)
**Baseline reference**: _archive/v<prev>/stage-L2-explore-<target>.md
**Kickoff form**: oneshot   ← 覆盖默认；redebate R2 强调对 baseline 的新审视
```
Session hint 列表必须包含 `_archive/v<prev>/stage-L2-explore-<target>.md`
作为 baseline 参考；并写明 "§4 必须包含 vs-baseline 段"。

And a `## Session hint` block listing only the new files vs L2R1 (typically:
opponent's L2R1 + moderator-notes.md if any) plus the HARD CONSTRAINT:
"Do NOT re-read files you read in the previous round of this Codex session
unless this task explicitly lists them under Session hint."

Tell Codex to write its outbox confirmation to
`.codex-outbox/queues/<target>/<TS>-<target>-L2R2.md`
（**Redebate**: 同名 → `<TS>-<target>-L2R2-redebate-${next_v}.md`，**与 inbox 文件名、HEAD 内容三者一致**；status/cdx-run 凭 HEAD 文件名匹配 outbox 同名文件来判断完成，**任何不一致都会让队列永远 pending**）。

Update queue HEAD pointer（redebate 时文件名带 `-redebate-${next_v}` 后缀，**HEAD 内容必须和 inbox/outbox 文件名完全一致**）：
```bash
echo "<TS>-<target>-L2R2[-redebate-${next_v}].md" > .codex-inbox/queues/<target>/HEAD
```

## Step 6 — output next-step menu

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ L2R2 Opus side done. <若 redebate: "(redebate ${next_v})">
File: discussion/.../<target>/L2/L2R2-Opus47Max.md (<word-count> words)
Searches: <n> value-validation queries
<若 redebate: "vs baseline ${prev_v}: <framing shift one-line>">

Refined picture (§4 in 1 sentence):
"<the sharpened reading>"

Validation verdict: <Y / Y-with-conditions / unclear / N>
Top open question for L3: <from §5>

📋 Next step (两种 kickoff 形态任选):

[1] (默认) 在已开的 Codex 终端复用 L2R1 会话 — 省 ~60% token
    → 粘贴这段进 Codex 终端：

    ```
    继续 idea <target> 的 L2R2。
    本轮只新读：
    - discussion/.../<target>/L2/L2R1-Opus47Max.md  (对方 R1)
    - discussion/.../<target>/L2/moderator-notes.md (如存在)
    然后按 .codex-inbox/queues/<target>/HEAD 指向的任务文件执行；
    把结果写到 .codex-outbox/queues/<target>/<HEAD-content>.md。
    禁止重读你已读过的其他文件。
    ```

[2] 新开 Codex 终端从零跑 (oneshot)
    → in your Codex terminal:  cdx-run <target>

[3] Show Codex kickoff for manual paste
    → cdx-peek <target>

[4] Show me Opus L2R2 first
    → I'll display the file

[5] Inject moderator note before Codex
    → tell me what to add

[6] Skip Codex L2R2 and synthesize what we have
    → /explore-advance <target>  (will note Codex L2R2 missing)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Reply 1/2/3/4/5/6 or describe.
```
