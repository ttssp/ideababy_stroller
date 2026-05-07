---
description: Pre-merge review gate for L4 build worktrees. Runs reviewer(s) of operator's choice (claude / codex / mixed) on a parallel-builder task before its worktree merges. Required by repo iron rule — verdict ≠ BLOCK to merge.
argument-hint: "<fork-id> <T-id> [--reviewer=claude-light|claude-full|codex|mixed]   e.g. 004-pB T012"
allowed-tools: Read, Write, Bash(ls:*), Bash(cat:*), Bash(git:*), Bash(date:*), Bash(mkdir:*), Bash(echo:*), Bash(rg:*), AskUserQuestion, Agent(code-reviewer), Agent(adversarial-reviewer), Agent(security-auditor), Glob, Grep
model: opus
---

# Task Review · pre-merge gate

Reviews the worktree produced by `parallel-builder` for `<fork-id>` task `<T-id>`
**before** the human merges it into the project trunk. Output is a structured
verdict: `CLEAN | CONCERNS | BLOCK`. Repo iron rule (CLAUDE.md) prohibits
merging without a non-BLOCK verdict.

## Step 0 — parse args

Expected: `$ARGUMENTS = "<fork-id> <T-id> [--reviewer=mode]"`, e.g.
`004-pB T012 --reviewer=claude-full`.

If `--reviewer=` is not given, ask via AskUserQuestion (Step 1). Otherwise
skip Step 1.

## Step 1 — choose reviewer mode (if not specified)

Use AskUserQuestion (single question, 4 options):

```
Q: Which reviewer mode for <fork>-<T>?
   Options:
   - claude-light  → 仅 code-reviewer (5 维度) — 小改 / UI / 文档
   - claude-full   → code-reviewer + security-auditor + adversarial-reviewer 串行 — 业务逻辑、API、状态机、并发 (Recommended)
   - codex         → 写 inbox 让 GPT-5.5 跨模型审；catch Claude 盲点
   - mixed         → claude-full + codex 都跑、合并结果 — 高风险任务（auth / 付费 / 敏感数据）
```

Default if user just hits enter: `claude-full`.

## Step 2 — locate worktree & gather diff

```bash
FORK="<fork-id>"
T="<T-id>"

# 任务规格
SPEC_FILE="specs/$FORK/tasks/$T.md"
test -f "$SPEC_FILE" || { echo "missing spec: $SPEC_FILE"; exit 1; }

# 项目目录（可能是 worktree 路径或 projects/ 子目录）
PROJ_DIR=$(ls -d projects/$FORK 2>/dev/null | head -1)
test -d "$PROJ_DIR" || { echo "missing project dir for $FORK"; exit 1; }

# diff 范围：默认对比项目 trunk（typically main 或 fork 的基线分支）
cd "$PROJ_DIR"
BASE=$(git rev-parse --abbrev-ref --symbolic-full-name @{upstream} 2>/dev/null || echo main)
git diff --stat "$BASE...HEAD" -- .
git log "$BASE..HEAD" --oneline -- .
```

读 `$SPEC_FILE` 拿到 `file_domain`、`acceptance criteria`、`verification` 三段。

## Step 3 — run reviewers per mode

### claude-light

Delegate to **code-reviewer**:

> "Use code-reviewer to review the diff `$BASE...HEAD` in $PROJ_DIR for task $T.
>  Read $SPEC_FILE for acceptance criteria. Output 5-axis findings classified
>  by P:high / P:med / P:low. Anything P:high blocks merge."

### claude-full

依次 delegate 三个 agent（顺序串行；每个完成才下一个）：

1. **code-reviewer** — 同 claude-light
2. **security-auditor** — 审 diff（OWASP Top 10 + secrets + auth/crypto），critical/high blocks
3. **adversarial-reviewer** — 三人格 (Saboteur / New Hire / Security Auditor)，每人格至少一条；输出 0-100 score

### codex

Compute timestamp `$(date -u +%Y%m%dT%H%M%S)`. Write
`.codex-inbox/queues/$FORK/<TS>-$FORK-$T-task-review.md`:

```markdown
# Codex Task · $FORK · Task Review · $T

**Queue**: $FORK
**Created**: <ISO>
**Recommended model**: gpt-5.5
**Recommended reasoning_effort**: xhigh
**Estimated tokens**: ~10-20k
**Kickoff form**: oneshot

## Your role
You are GPT-5.5 xhigh, performing pre-merge review on a single task ($T) that
parallel-builder just finished. Your goal is to find issues a friendly Claude
reviewer might miss — concurrency, security, hidden side-effects, spec drift.

## Read
- specs/$FORK/tasks/$T.md (acceptance + file_domain)
- specs/$FORK/spec.md (broader spec context)
- $PROJ_DIR/ — diff against $BASE (use `git diff $BASE...HEAD`)

## Output
.codex-outbox/queues/$FORK/<same-filename>.md with:
- 5-axis findings (correctness / consistency / security / concurrency / spec-fit)
- Per finding: severity (blocker / high / med / low), location, fix direction
- Verdict: CLEAN | CONCERNS | BLOCK
- One section "what Claude reviewers likely won't catch"

Quote ≤15 words verbatim from any source file.
```

Update queue HEAD:
```bash
mkdir -p .codex-outbox/queues/$FORK
echo "<TS>-$FORK-$T-task-review.md" > .codex-inbox/queues/$FORK/HEAD
```

Tell human: "Codex task ready. Run `cdx-run $FORK` then re-invoke
`/task-review $FORK $T --reviewer=consume-codex` to consume." (consume-codex
is a thin variant — see Step 5.)

### mixed

Run claude-full first (it's fast-ish), then write codex inbox per above.
Final verdict waits until both come back; while waiting, write a partial
verdict file noting `codex pending`.

## Step 4 — compose verdict

Verdict file: `projects/$FORK/.review/$T-r<n>.md` (auto-increment `n`).

```bash
mkdir -p projects/$FORK/.review
N=$(ls projects/$FORK/.review/$T-r*.md 2>/dev/null | wc -l)
N=$((N+1))
OUT="projects/$FORK/.review/$T-r$N.md"
```

Write structure:

```markdown
# Task Review · $FORK · $T · r$N
**Reviewer mode**: <mode>
**Run at**: <ISO>
**Diff**: $BASE...HEAD (<files> files, +<add>/-<del>)
**Reviewed by**: <code-reviewer | security-auditor | adversarial-reviewer | codex>

## Findings (按 reviewer 分组)

### code-reviewer (5-axis)
| Sev | Axis | Location | Issue | Fix direction |
|-----|------|----------|-------|----------------|
...

### security-auditor (OWASP Top 10)
| Sev | Category | Location | Issue | Fix |
|-----|----------|----------|-------|------|
...

### adversarial-reviewer (3 personas)
- 🔪 Saboteur:        <issue>
- 🆕 New Hire:        <issue>
- 🛡 Security Auditor: <issue>
- Score: <X>/100

### codex (if mode=codex|mixed)
<codex outbox 摘要>

## Acceptance check (spec faithfulness)
- [ ] T<NNN>.md 的每条 verification 已被 diff 覆盖
- [ ] file_domain 未越界
- [ ] TDD 顺序合规（先 test 后 impl 的 commit 序列）

## Verdict
- **CLEAN**     → 可合并
- **CONCERNS**  → 列哪几条建议修，哪几条进 risks.md
- **BLOCK**     → 必修后再 /task-review $FORK $T 生成 r$((N+1))

## Top fixes ranked
1. ...
2. ...
3. ...
```

判定规则：
- 任一 reviewer 报 **blocker / critical / P:high** 且**未在 spec/risks 中已记录** → BLOCK
- adversarial-reviewer score < 70 → BLOCK
- 仅 P:med / 低风险 finding → CONCERNS（人类决定）
- 无 finding 或仅 nit → CLEAN

## Step 5 — output next-step menu

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Task Review · $FORK · $T · r$N
Verdict: <CLEAN | CONCERNS | BLOCK>
Reviewer mode: <mode>
Findings: <total> (B:<n> C:<n> H:<n> M:<n> L:<n>)

📋 Next step:

[1] (CLEAN) Merge worktree
    → cd $PROJ_DIR && git checkout main && git merge <task-branch>

[2] (CONCERNS) Edit code, accept risks, then merge
    → I'll list the high-priority fixes and ask which to defer

[3] (BLOCK) Send back to parallel-builder for fix
    → tell me what scope of fix; I'll spawn Agent(parallel-builder)

[4] Re-run review with stricter mode
    → /task-review $FORK $T --reviewer=mixed

[5] Show full verdict file
    → I'll display projects/$FORK/.review/$T-r$N.md

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Reply 1/2/3/4/5 or describe what you want.
```

## Notes for the orchestrator (you)

- **You don't review yourself.** Always delegate to the reviewer agents.
  Your job is: locate worktree → run agents → compose verdict.
- **Don't merge.** Even on CLEAN, the operator does the merge — your output
  stops at the verdict file + menu.
- **Don't write to specs/.** Only `projects/$FORK/.review/` and inbox/outbox.
- **iron rule**: verdict ≠ BLOCK is mandatory before merging any worktree
  (CLAUDE.md). If operator skips, you should remind once.
- For `consume-codex` mode (re-invocation after Codex outbox arrives), parse
  outbox, append its findings to the existing `r$N.md` file, recompute verdict.
