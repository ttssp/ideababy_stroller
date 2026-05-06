---
description: Close L2 and produce the L2 explore report (stage-L2-explore-<fork-id>.md). Runs explore-synthesizer subagent. After this, human decides — proceed to L3 (scope), fork another L2 angle, back to L1, re-explore, park, or abandon.
argument-hint: "<fork-id-or-idea-number>  e.g. 001a"
allowed-tools: Read, Write, Edit, Bash(ls:*), Bash(date:*), Bash(rm:*), Bash(stat:*), Bash(test:*), Glob, Grep, Agent(explore-synthesizer)
model: opus
---

# Explore · close L2, produce report

Idea **$ARGUMENTS**.

## Step 0 — active redebate detector（最小侵入）

```bash
test -f discussion/.../<target>/L2/.redebate-active
```

若存在，读取 `<next_v>|<start_iso>|<reason>`。本次 advance 是 **redebate ${next_v} 的收尾**：

- 把 `redebate=true / next_v / prev_v / reason / start_iso` 作为参数传给
  explore-synthesizer，让它在 stage doc header 加 Redebate-Lineage 块（见 Step 2）
- advance 完成 + sanity check 通过后，**删除** `.redebate-active`：
  ```bash
  rm discussion/.../<target>/L2/.redebate-active
  ```
- next-step menu 改为 redebate 收尾版（见 Step 4），含 [Revert] 选项
- **Stage 1 范围**：本次 advance **不**自动给下游 spec/tasks 标 dirty。
  下游 dirty 标记是 Stage 2 范围 — 现在仅在 menu 末尾输出一行
  "Stage 2 TODO: dirty 标记下游"提醒。

若文件不存在，按标准 advance 流程跑（下文不变）。

## Step 1 — preconditions

```bash
ls discussion/.../<target>/L2/*.md
```

Required: both L2R1, both L2R2.
If any missing, stop and tell human what's pending. Optionally proceed with
explicit `--partial` flag (synthesizer will note what's missing).

## Step 2 — invoke synthesizer

Delegate to `explore-synthesizer`:

> "Use explore-synthesizer on idea <target>.
>  Read all L2 files in discussion/.../<target>/L2/.
>  Output: discussion/.../<target>/L2/stage-L2-explore-<target>.md.
>  Origin context: <fork from L1 #n / direct from skip-mode>."

**Redebate only** — 在上述 prompt 后追加：

> "This is a redebate advance. Add a Redebate-Lineage header block right after the
>  document title, before the executive summary:
>
>  ```markdown
>  **Version**: ${next_v} (redebate)
>  **Previous version**: _archive/v<prev>/stage-L2-explore-<target>.md
>  **Redebate triggered at**: <start_iso>
>  **Redebate reason**: <reason>
>  **Time window scanned**: <prev stage doc Generated date> → <today>
>  **Redebate lineage**:
>    - v<prev>: <date from prev stage doc> (initial advance)
>    - ${next_v}: <today> (this) — trigger: <one-line summary of reason>
>  ```
>
>  Also: in the executive summary, add one bullet 'Top 3 deltas vs v<prev>: ...'
>  Read _archive/v<prev>/stage-L2-explore-<target>.md to compute the deltas."

Wait for return.

## Step 3 — sanity check

Read the produced file. Check:
- Executive summary present
- §1-§7 all populated
- §6 validation verdict explicit (Y / Y-with-conditions / unclear / N)
- §7 open questions for L3 non-empty
- Decision menu present

If any check fails, ask synthesizer to revise.

## Step 3.5 — Redebate cleanup（仅 redebate 路径）

若 Step 0 检测到 `.redebate-active`：

```bash
rm discussion/.../<target>/L2/.redebate-active
```

并准备 redebate 版菜单（Step 4 分叉）。

## Step 4 — output human-facing menu

### Step 4A — 标准 advance 菜单（非 redebate）

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ L2 done. Explore report produced.

File: discussion/.../<target>/L2/stage-L2-explore-<target>.md
Validation verdict: <Y / Y-with-conditions / unclear / N>
Executive summary:
  · <bullet 1 from synthesizer's exec summary>
  · <bullet 2>
  · <bullet 3>

Top 3 open questions for L3 (or for user research):
  1. <from §7>
  2. <from §7>
  3. <from §7>

📋 Your decision:

[1] Scope this idea — proceed to L3 (recommended if verdict is Y or Y-with-conditions)
    → /scope-start <target>
    (L3 brings in your real constraints, preferences, time/budget.)

[2] Fork another L2 angle from this same idea
    → /fork <target> from-L2 <new-angle> as <new-id>
    (use this if reading the report sparked a sharper cut)

[3] Back to L1 menu — pick another inspired direction
    → /status <root>  (see all L1 directions and other forks)

[4] Re-explore — inject new input and run another L2 round
    → tell me what to add, I'll write to L2/moderator-notes.md
       and we can run /explore-next <target>

[5] Park this fork (preserve, decide later)
    → /park <target>

[6] Abandon this fork (siblings continue)
    → /abandon <target>

[V] Show me the full L2 report before deciding
    → I'll display stage-L2-explore-<target>.md

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Reply 1/2/3/4/5/6/V or describe.
```

### Step 4B — Redebate 收尾菜单（仅当 .redebate-active 检测到时）

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔄 L2 redebate ${next_v} complete.

New stage doc: discussion/.../<target>/L2/stage-L2-explore-<target>.md
Archived ${prev_v}: discussion/.../<target>/L2/_archive/${prev_v}/
Redebate trigger: <reason 单行 summary>
Validation verdict: <Y / Y-with-conditions / unclear / N>

Top 3 deltas vs ${prev_v}:
  1. <from synthesizer's exec summary>
  2. <...>
  3. <...>

⚠️ Stage 2 TODO: 下游 dirty 标记尚未实现（Stage 1 MVP 范围）。
   现阶段需手工评估 L3/PRD/spec/tasks 是否仍 align ${next_v} 的新 framing。
   Stage 2 落地后将自动给下游打 Upstream-Redebated 标记。

📋 Your decision:

[1] Cascade upgrade — L3 也需要重做
    → /scope-redebate <target>  (Stage 3 后可用；当前请用 /scope-start fork)

[2] Continue building — 接受 redebate ${next_v} 后下游手工自检
    → 手工 review L3 stage doc / PRD / spec 是否需要调整

[3] Revert — 回滚到 ${prev_v}
    → 我会:
       (a) cp _archive/${prev_v}/* L2/
       (b) 把当前 ${next_v} 的工作产物（L2R1/L2R2/stage-doc）归档到
           _archive/${next_v}-rolled-back/
       (c) 删除 moderator-notes.md 中本次 Redebate-trigger 块
       需明确确认: y/n

[4] Show full stage doc (${next_v})
    → I'll display stage-L2-explore-<target>.md

[5] Show diff highlights vs ${prev_v}
    → I'll diff key sections and summarize

[6] Park / Abandon (decide redebate had no value)
    → /park <target> 或 /abandon <target>

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Reply 1/2/3/4/5/6 or describe.
```

## Notes

- If validation verdict is **N**, gently suggest options 5 (park) or 6 (abandon).
  Don't refuse to proceed to L3 — human's call — but flag the verdict prominently.
- If verdict is **unclear**, suggest option 4 (re-explore with steering) before
  option 1.
- Open questions in §7 may include "we need to interview real users" — if so,
  recommend pausing the pipeline (option 5) until that's done. L3 without user
  input is often rework.
