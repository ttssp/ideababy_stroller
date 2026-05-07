---
description: Run next round of L4 adversarial review (R2-R4) on a PRD fork's spec package. Uses reuse-session kickoff form by default — Codex stays in the same terminal session, only reads the diff vs previous round, saves ~60% context tokens. Stops at R4 max.
argument-hint: "<prd-fork-id>  e.g. 001a-pA  (round number is auto-detected)"
allowed-tools: Read, Write, Bash(ls:*), Bash(cat:*), Bash(date:*), Bash(mkdir:*), Bash(echo:*), Bash(git:*), Agent(spec-writer), Glob, Grep
model: opus
---

# Plan · Adversarial Review · Next Round (R2-R4)

PRD branch **$ARGUMENTS** (e.g. `001a-pA`).

## Step 1 — detect current round

```bash
FORK="$ARGUMENTS"
QDIR=".codex-inbox/queues/$FORK"
test -d "$QDIR" || { echo "no queue for $FORK — run /plan-start $FORK first"; exit 1; }
ls "$QDIR" | grep -E "L4-adversarial-r[0-9]+\.md" | sort
```

Determine `LAST_R = max round number on inbox`. The round we'll create is
`NEXT_R = LAST_R + 1`. **Hard cap**: `NEXT_R ≤ 4`. If the user invokes after
R4, stop and tell:

> "R4 is the maximum. After R4 you must either:
>  - accept open blockers and ship with risks.md updated, OR
>  - re-scope the PRD (back to L3) — the spec is fundamentally off."

## Step 2 — read the LAST_R outbox (Codex's previous verdict)

```bash
LAST_OUT=".codex-outbox/queues/$FORK/<TS>-$FORK-L4-adversarial-r${LAST_R}.md"
test -f "$LAST_OUT" || { echo "Codex hasn't returned R${LAST_R} yet — run cdx-run $FORK first"; exit 1; }
```

Parse:
- Verdict (CLEAN | CONCERNS | BLOCK)
- Top blockers / high concerns
- PRD-faithfulness check status

If verdict is `CLEAN` and no open blockers → tell human "no need for R${NEXT_R};
spec is ready to build". Stop.

## Step 3 — invoke spec-writer to address blockers (if any)

If the previous round had blockers / high concerns:

> "Use spec-writer to revise specs/$FORK/ to address the blockers from
>  $LAST_OUT. Read the outbox file first, then update spec.md / architecture.md
>  / risks.md / tasks/T*.md as needed. Do NOT alter PRD.md (it's source of truth)
>  — if a blocker requires PRD change, escalate to human."

Wait for spec-writer. Note which files changed (`git status -- specs/$FORK/`).

## Step 4 — write next-round Codex inbox task (reuse-session by default)

Compute timestamp `$(date -u +%Y%m%dT%H%M%S)`.

Write `.codex-inbox/queues/$FORK/<TS>-$FORK-L4-adversarial-r${NEXT_R}.md`:

```markdown
# Codex Task · $FORK · L4 Adversarial Review Round ${NEXT_R}

**Queue**: $FORK
**Created**: <ISO>
**Recommended model**: gpt-5.5
**Recommended reasoning_effort**: xhigh
**Estimated tokens**: ~5-10k (reuse-session 缩减自 R1 的 15-25k)
**Kickoff form**: reuse-session   ← 默认 (R${NEXT_R} 与 R${LAST_R} 上下文重叠 ~85%)

## Session hint (only meaningful if Codex reuses session from R${LAST_R})
You already read the full spec package in R${LAST_R}. This round, only
re-read the **changed files** since R${LAST_R}:

<list of changed files from `git diff --name-only HEAD~1..HEAD -- specs/$FORK/`,
 each with the line range that changed if reasonable>

**HARD CONSTRAINT (reuse only)**: Do NOT re-read files you read in R${LAST_R}
unless this list explicitly includes them.

## Your role this round
Verify whether the blockers / high concerns you raised in R${LAST_R} are now
fixed. If new issues are introduced by the changes, raise them. Re-evaluate
the verdict.

## Read this round (incremental diff)
<file list with brief change summary>

## Re-check (cross-reference R${LAST_R})
For each blocker from R${LAST_R}:
- Is it fixed? (point to the line/file that fixes it)
- If "fixed in concept" but tests / verification missing, that's still BLOCK
- If a fix introduces a new concern, raise it under §New issues

## Write
.codex-outbox/queues/$FORK/<TS>-$FORK-L4-adversarial-r${NEXT_R}.md with:

```markdown
# Adversarial Review · $FORK · R${NEXT_R}

## Status of R${LAST_R} blockers
| # | R${LAST_R} blocker | Fixed? | Evidence (file:line) |

## New issues this round
| # | Severity | Location | Issue | Fix direction |

## PRD faithfulness re-check
- [ ] No regression on PRD outcomes
- [ ] No scope creep beyond PRD scope IN
- [ ] No leakage into PRD scope OUT

## Verdict R${NEXT_R}
- CLEAN (all R${LAST_R} blockers fixed, no new blockers) — spec ready to build
- CONCERNS (some fixed, some deferred to risks.md by operator decision)
- BLOCK (new blockers or unfixed prior blockers — needs R${NEXT_R + 1})
```

Quote ≤15 words verbatim from any source.
```

Update queue HEAD pointer:
```bash
echo "<TS>-$FORK-L4-adversarial-r${NEXT_R}.md" > .codex-inbox/queues/$FORK/HEAD
```

## Step 5 — output next-step menu

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Adversarial review R${NEXT_R} primed for $FORK
Spec changes since R${LAST_R}: <n> files updated
Estimated round budget: <n> remaining (R4 max)

📋 Next step (两种 kickoff 形态任选，强烈推荐 [1]):

[1] (默认) 在已开的 Codex 终端复用 R${LAST_R} 会话 — 省 ~70% token
    → 粘贴这段进 Codex 终端：

    ```
    继续 $FORK 的 L4 adversarial review R${NEXT_R}。
    本轮只新读以下 diff 文件：
    <changed files list>
    然后按 .codex-inbox/queues/$FORK/HEAD 指向的任务文件 §"Re-check" 执行；
    把结果写到 .codex-outbox/queues/$FORK/<HEAD-content>.md。
    禁止重读 R${LAST_R} 已读过的文件。
    ```

[2] 新开 Codex 终端从零跑 (oneshot, 适合 R${LAST_R} 跑完很久 / 已退出)
    → in your Codex terminal:  cdx-run $FORK

[3] Show Codex kickoff for manual paste
    → cdx-peek $FORK

[4] Show changes since R${LAST_R}
    → I'll display git diff main..HEAD -- specs/$FORK/

[5] Skip this round — accept R${LAST_R} verdict and move on
    → /quality-gate $FORK  (or merge spec and proceed to /parallel-kickoff)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Reply 1/2/3/4/5 or describe.
```

## Notes

- **Why reuse-session by default here**: this is the highest-value reuse case
  in the whole pipeline. R2-R4 of adversarial review reads the same large spec
  package each round; reusing the session saves ~70% tokens vs oneshot.
- **R4 hard cap**: if R4 still has blockers, the spec is fundamentally off.
  Don't loop forever. Escalate to operator: re-scope PRD or ship with risks.
- **No PRD edits**: this command never touches PRD.md. If a blocker requires
  PRD change, surface it to operator and stop.
