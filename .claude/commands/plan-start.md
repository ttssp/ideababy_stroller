---
description: Start L4 Plan phase for a forked PRD branch. Reads the chosen PRD.md, invokes spec-writer to produce the SDD package, runs task-decomposer, then triggers Codex adversarial review loop (up to 4 rounds). Output is a build-ready spec package.
argument-hint: "<prd-fork-id>  e.g. 001a-pA"
allowed-tools: Read, Write, Bash(mkdir:*), Bash(cp:*), Bash(echo:*), Bash(ls:*), Bash(date:*), Bash(realpath:*), Agent(spec-writer), Agent(task-decomposer), Glob, Grep
model: opus
---

# Plan · L4 entry — from PRD to spec + task DAG

PRD branch **$ARGUMENTS** (e.g. `001a-pA`).

## Step 1 — locate the PRD

The PRD was produced by `/fork ... from-L3 candidate-X as <prd-fork-id>`.
The fork's `FORK-ORIGIN.md` references the L3 stage doc and the chosen candidate.

Expected layout:
```
discussion/<root>/<parent-fork>/<prd-fork-id>/
  ├─ FORK-ORIGIN.md
  └─ PRD.md    ← generated at fork time from the L3 candidate
```

If `PRD.md` doesn't exist, construct it now from FORK-ORIGIN.md's candidate
description (fork should have extracted the full candidate). If the fork
was done before this command existed (edge case), run:

```
I notice PRD.md isn't at the expected location. I'll synthesize one from
FORK-ORIGIN.md + the L3 stage doc now. OK?
```

## Step 2 — read all context

1. `discussion/<root>/<parent-fork>/<prd-fork-id>/PRD.md` — the chosen PRD
2. `discussion/<root>/<parent-fork>/<prd-fork-id>/FORK-ORIGIN.md` — lineage
3. `discussion/<root>/<parent-fork>/L3/stage-L3-scope-<parent-fork>.md` — full menu context
4. `discussion/<root>/<parent-fork>/L2/stage-L2-explore-<parent-fork>.md` — idea context
5. `CLAUDE.md`
6. `.claude/skills/sdd-workflow/SKILL.md`

## Step 2.5 — detect PRD-form (NEW, 透传到下游)

读 PRD.md frontmatter,提取 `**PRD-form**`(缺失时默认 simple)。同时提取形态特异 frontmatter:
- phased: `**Phases**` 数组
- composite: `**Modules**`、`**Module-forms**`、`**Critical-path module**`(从 §"Critical-path module" 章节提取)
- v1-direct: `**Skip-rationale**`(全文,要校验 ≥100 字 + 含 C1/C2/C3 之一,虽然 fork-v1 已校验过,这里再 sanity check 一次)

**校验失败处理**(任一失败立即报错并停止,不调用 spec-writer):
- composite 缺 `**Modules**` 或 module 数 <2
- phased 缺 `**Phases**` 或数组长度 <2
- v1-direct 的 skip-rationale <100 字 / 缺 C1/C2/C3 / PRD §"Risk: skip-v0.1" fallback path 仍是 `<待补充>`

记录 `<PRD-FORM>` / `<PHASES>` / `<MODULES>` / `<MODULE-FORMS>` 等变量,Step 4 / 5 / 6 透传给下游。

## Step 3 — decide spec package location

```
specs/<prd-fork-id>/    e.g. specs/001a-pA/
```

Create:
```bash
mkdir -p specs/<prd-fork-id>/tasks
```

## Step 4 — invoke spec-writer

Delegate to `spec-writer` subagent:

> "Use spec-writer to produce a complete SDD package in `specs/<prd-fork-id>/`
>  from the PRD at `discussion/.../<prd-fork-id>/PRD.md`.
>
>  **PRD-form awareness (REQUIRED)**:
>  PRD frontmatter `**PRD-form**` = `<PRD-FORM>` (one of simple / phased / composite / v1-direct).
>  - `<PHASES>` = <如 phased,数组如 [v0.1, v1.0]>
>  - `<MODULES>` = <如 composite,数组如 [m1, m2, m3]>
>  - `<MODULE-FORMS>` = <如 composite,字典>
>  - `<CRITICAL-PATH>` = <如 composite,critical-path module 的 ID>
>
>  按 spec-writer Phase 0 分支:
>  - simple    → 标准 7 文件输出
>  - phased    → SLA / risks 按 PRD `**Phases**` 数组分段;spec.md §2 Scope Boundaries 也按 phase 分子节
>  - composite → 顶层 spec.md 退化为 INDEX,**额外**为每 module 输出 spec-<m>.md;risks.md / SLA.md 加 Module 列
>  - v1-direct → SLA.md 顶部加 §'Skip rationale';risks.md 必含 R-skip-v0.1 条目
>
>  Context to read:
>  - The PRD (source of truth for outcomes, scope, constraints, form)
>  - L3 stage doc for the menu context (why this cut was chosen vs siblings)
>  - L2 stage doc for the idea texture
>  - CLAUDE.md
>  - sdd-workflow skill
>
>  Produce(按形态产文件清单 — 见 spec-writer.md Phase 0 manifest 表)。
>
>  DO NOT yet create tasks/ — that's the next step (task-decomposer).
>  DO NOT start implementation — that's parallel-builder later.
>  DO NOT modify the PRD — even if you find issues, escalate to operator."

Wait for spec-writer to complete.

## Step 5 — invoke task-decomposer

Delegate to `task-decomposer`:

> "Use task-decomposer to break spec.md into tasks/T001.md ... T<NNN>.md and
>  produce dependency-graph.mmd.
>
>  **PRD-form awareness (REQUIRED)**:
>  PRD-form = `<PRD-FORM>` (透传自 step 2.5)
>  - composite 形态:**额外**读所有 spec-<m>.md(每 module 独立分解,顶层 INDEX 协调跨 module 任务)
>  - phased 形态:每 task frontmatter 加 `phase_target: <phase-id>`;DAG 必须按 phase 分层(用 mermaid subgraph 框);v0.1 任务全完 + 通过 quality-gate 才允许进 v1.0 任务
>  - composite 形态:每 task frontmatter 加 `module: <m> | shared`;file_domain 用 module 命名空间;DAG 用 mermaid subgraph 框各 module
>
>  Source: specs/<prd-fork-id>/spec.md(composite 时还包括 spec-*.md)
>  Plus: architecture.md, tech-stack.md for file_domain decisions.
>  Target dir: specs/<prd-fork-id>/tasks/
>
>  Produce 10-30 tasks with phase labels (build phase 0/1/2/3 + PRD-level phase_target if phased + module if composite). Apply model routing heuristics from task-decomposer-skill (recommended_model per task).
>
>  Output distribution health report at end + (form-specific): 每 phase / 每 module 的 task 数分布。"

Wait for completion.

## Step 5.5 — write HANDOFF.md (NEW · v2.2,SHARED-CONTRACT §3 实装)

依据:`framework/SHARED-CONTRACT.md` §3 Hand-off 协议(contract_version 1.1.0)。

写 `specs/<prd-fork-id>/HANDOFF.md`(operator-readable 格式,跨仓切到 ADP 时使用)。HANDOFF.md 必须在 spec.md + tasks/T*.md 已生成后产出(它的 Schema 转换表引用 §5 Task Breakdown);也必须在 Codex adversarial review(Step 6)之前产出,以便 review 同时核查 hand-off 协议。

### 模板(替换 `<...>` 占位为真实值)

```markdown
# Hand-off · <prd-fork-id> → autodev_pipe

**Handed off at**: <ISO timestamp · `date -u +%Y-%m-%dT%H:%M:%SZ`>
**IDS spec path**: <`realpath specs/<prd-fork-id>`>
**PRD source**: <`realpath discussion/<root>/<parent-fork>/<prd-fork-id>/PRD.md`>
**ADP repo path** (operator 自填): /Users/admin/codes/autodev_pipe
**SHARED-CONTRACT version honored**: 1.1.0

## Operator manual steps(切仓后)

1. cd <ADP repo path>
2. 阅读 IDS PRD 与 IDS spec:
   - `cat <PRD source>`
   - `cat <IDS spec path>/spec.md`
3. 在 ADP 起新 feature(真实入口 = skill,不是 Makefile target):
   - 在 ADP Claude Code session 里,触发 `.claude/skills/sdd-workflow/SKILL.md`
   - **operator 必须人工转写**:把 IDS PRD §"User persona" + §"Core user stories" 提炼为 1-2 段 short feature description 作为 sdd-workflow input
4. sdd-workflow 产出 `specs/<feature>/spec.md`(7 元素骨架,schema_version: 0.2,reviewed-by: pending)后,operator 按下表强制项填入:

| IDS 来源 | ADP spec 节 | 强制? |
|---|---|---|
| IDS PRD frontmatter | spec.md frontmatter (`spec_id` / `status: draft` / `schema_version: 0.2` / `reviewed-by: pending`) | 强制 |
| IDS PRD §"User persona" + §"Core user stories" | §1 Outcomes(O1, O2, ...) | 强制 |
| IDS PRD §"Scope IN" | §2.1 Scope IN | 强制 |
| IDS PRD §"Scope OUT" | §2.2 Scope OUT | 强制 |
| IDS PRD §"Real constraints" | §3 Constraints(C1, C2, ... 数字化) | 强制 |
| IDS spec §"Prior Decisions" 或 architecture.md | §4 Prior Decisions(PD1, PD2, ... 引用源) | 强制 |
| IDS spec §"phases" 或 dependency-graph | §5 Task Breakdown(高层 phase + 依赖) | 强制 |
| IDS PRD §"Success looks like" | §6 Verification Criteria(每条 V_n 可执行 shell) | 强制 |
| **operator 须补**(IDS 不产出,见 step 4.5) | §7 Production Path Verification | **强制(v3.3 起)** |
| IDS PRD §"Open questions" 中**关于 constraint 数字**的 | ADP spec §3 Constraints 末尾 "Open" 小节(C-OQ-1 ...) | 可选 |
| IDS PRD §"Open questions" 中**关于 build 路径选择**的 | 不进 ADP spec,留在本 HANDOFF.md §"Open questions for build phase" | 可选 |

4.5. **operator 在 ADP 写 §7 Production Path Verification**(IDS 不越界产出,ADP 强制):
   - 参考样本:`<ADP repo>/specs/v3.3/spec.md` §7 真路径 P1-P4 example
   - 模板:`<ADP repo>/templates/spec.template.md` §7 骨架
   - 最小要求:列至少 1 条 P_i 描述"真路径起点 → 终点 + 必经环节 + 可执行验证命令"
   - 失败模式:不写或只写 mock-pass-prod-fail 的样本 → ADP `scripts/spec_validator.py` reject + status 无法转 frozen
   - 第一性原因:所有 mock-pass-prod-fail 都因为 mock 满足 spec 真路径不满足(灵感来源 stroller idea004 12 routes 404 失败案例)

5. 在 ADP 跑 reviewed-by:
   - frontmatter `reviewed-by: pending` → 触发 ADP `/codex:adversarial-review` 或 plugin 路径
   - review 通过 → frontmatter 改 `reviewed-by: codex`(或 gpt-5.5 / gemini)
   - status: draft → review → frozen
6. 任务分解(ADP 这边的 task-decomposer skill,不复用 IDS task DAG):
   - 在 ADP Claude Code session 触发 `.claude/skills/task-decomposer/SKILL.md`
   - 产出 `specs/<feature>/tasks/T*.md`(9 字段 frontmatter)
7. parallel-builder 跑 task(走 ADP 5 hard rule + Safety Floor)
8. ship 走 ADP 自己规则(不回 IDS)

## ADP-side prerequisites(operator 切仓前自查)

- ADP 仓库为 v3.2+(含 `.claude/skills/sdd-workflow/` + `.claude/skills/task-decomposer/` skill)
- ADP `make doctor` exit 0
- ADP `pre-commit install` 已跑(spec-validator + check-spec-review + check-constraint-references hooks 装齐)
- **operator 已读 ADP `templates/spec.template.md` §7 + `specs/v3.3/spec.md` §7 真实样本**(为 step 4.5 写 §7 PPV 做准备)
- ADP V4 dogfood 状态:**首次切仓前确认 V4 checkpoint-01 已出**(2026-06-03 ±);切仓时机过早会污染 dogfood signal(ADR 0008 D2)

## Schema 转换说明

详见 `framework/SHARED-CONTRACT.md` §3 HANDOFF.md schema(contract_version 1.1.0)。

## Open questions for ADP build phase

(IDS PRD 中**关于 build 路径选择**的 OQ 在此承载;ADP build 自然遇到时再解决,不污染 ADP spec frozen)

(由 operator 从 IDS PRD §"Open questions" 手工分流后填入)

## Rollback plan

如果 ADP build 失败:
- (a) 回到 IDS 修 PRD,重跑 `/plan-start`
- (b) 改 ADP spec(不改 IDS PRD),用 ADP 自己的 W-* 修订机制
- (c) 起 forge v2 重新审整个 idea
```

### 实装

写文件:`specs/<prd-fork-id>/HANDOFF.md`,用上面模板。具体动作:

```bash
TS="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
IDS_SPEC_PATH="$(realpath specs/<prd-fork-id>)"
PRD_SOURCE="$(realpath discussion/<root>/<parent-fork>/<prd-fork-id>/PRD.md)"
# 然后用 Write 工具落盘上面模板的实化版本
```

### 验收

```bash
test -f specs/<prd-fork-id>/HANDOFF.md && \
  grep -q "SHARED-CONTRACT version honored: 1.1.0" specs/<prd-fork-id>/HANDOFF.md && \
  grep -q "sdd-workflow" specs/<prd-fork-id>/HANDOFF.md && \
  grep -q "task-decomposer" specs/<prd-fork-id>/HANDOFF.md && \
  echo "HANDOFF.md OK"
```

## Step 6 — prepare Codex adversarial review

Queue id: `QUEUE=<prd-fork-id>` (e.g. `001a-pA`).

Ensure queue dirs:
```bash
mkdir -p .codex-inbox/queues/<prd-fork-id> .codex-outbox/queues/<prd-fork-id>
```

Write `.codex-inbox/queues/<prd-fork-id>/<TS>-<prd-fork-id>-L4-adversarial-r1.md`:

```markdown
# Codex Task · <prd-fork-id> · L4 Adversarial Review Round 1

**Queue**: <prd-fork-id>
**Created**: <ISO>
**Recommended model**: gpt-5.5
**Recommended reasoning_effort**: xhigh
**Estimated tokens**: ~15-25k
**Kickoff form**: oneshot

## Your role
You are GPT-5.5 xhigh performing adversarial review on a just-generated spec
package. Your goal: find where this spec will fail in production.

## Read
- specs/<prd-fork-id>/spec.md  (6-element contract)
- specs/<prd-fork-id>/architecture.md
- specs/<prd-fork-id>/tech-stack.md
- specs/<prd-fork-id>/SLA.md
- specs/<prd-fork-id>/risks.md
- specs/<prd-fork-id>/non-goals.md
- specs/<prd-fork-id>/tasks/T*.md (sample 3-5)
- specs/<prd-fork-id>/dependency-graph.mmd
- discussion/.../PRD.md (to verify spec is faithful)

## Challenge these specifically
1. **Concurrency safety** — what breaks at 10x traffic?
2. **Data consistency** — where can state corrupt under concurrent writes?
3. **Failure recovery** — what happens when upstream X goes down for 30 minutes?
4. **Security boundaries** — where is trust crossed without verification?
5. **Operational cost at scale** — does the architecture stay affordable at 10x load?
6. **PRD faithfulness** — does the spec actually deliver every PRD outcome?
7. **Non-goal leakage** — does the spec accidentally include things PRD excludes?
8. **Task DAG sanity** — any cycles, unreachable tasks, or overly-wide dependencies?
9. **Solo-operator viability** — can one human with AI agents actually execute this?

## Write
.codex-outbox/queues/<prd-fork-id>/<TS>-<prd-fork-id>-L4-adversarial-r1.md with:

```markdown
# Adversarial Review · <prd-fork-id> · R1

## Blockers (must fix before proceeding)
| # | Location | Issue | Why it blocks | Fix direction |

## High-severity concerns (should fix; ok as follow-up with owner+deadline)
| # | Location | Issue | Suggested action |

## Medium / Low findings
(brief list)

## PRD faithfulness check
- [ ] Every PRD outcome has corresponding spec verification
- [ ] No spec feature outside PRD scope IN
- [ ] No spec feature in PRD scope OUT

## Top 3 things the operator personally must verify (human judgment required)
1. ...

## Verdict
One of:
- CLEAN (no blockers, optionally minor fixes) — spec ready to build
- CONCERNS (non-blocking; operator decides whether to fix now or ship with risk log)
- BLOCK (must fix before round 2)
```

Quote ≤15 words verbatim from any file.
```

Update queue HEAD pointer:
```bash
echo "<TS>-<prd-fork-id>-L4-adversarial-r1.md" > .codex-inbox/queues/<prd-fork-id>/HEAD
```

## Step 7 — output next-step menu

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ L4 Plan started for <prd-fork-id>.

Generated:
  specs/<prd-fork-id>/
    ├─ spec.md           (6-element contract)
    ├─ architecture.md
    ├─ tech-stack.md
    ├─ SLA.md
    ├─ risks.md          (<n> entries)
    ├─ non-goals.md
    ├─ compliance.md     [if applicable]
    ├─ dependency-graph.mmd
    ├─ tasks/T001..T<NNN>.md  (<n> tasks across <k> phases)
    └─ HANDOFF.md        (跨仓切到 ADP 用,SHARED-CONTRACT v1.1.0)

Task distribution health: <from decomposer>
  Opus:   X%
  Sonnet: Y%
  Codex:  Z%
  Haiku:  W%
  (target: Opus 10-15%, Sonnet 55-70%, Codex 10-15%, Haiku 5-10%)

📋 Next step: Codex adversarial review R1

[1] (默认) 新开 Codex 终端跑 adversarial review R1 (oneshot)
    → in your Codex terminal: cdx-run <prd-fork-id>
    (Codex reviews spec + tasks, writes blockers/concerns to outbox)

[2] reuse-session 选项 (R1 通常 oneshot 即可；R2-R4 由 plan-adversarial-next
    自动走 reuse-session)

[3] Show Codex kickoff for manual paste
    → cdx-peek <prd-fork-id>

[4] Show me the spec first
    → I'll display specs/<prd-fork-id>/spec.md

[5] Show me the task list first
    → I'll display specs/<prd-fork-id>/dependency-graph.mmd

[6] Review the task distribution
    → I'll display model assignments summary

[7] Pause — I want to read everything before adversarial review
    → run /status <prd-fork-id> to see state when ready

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Reply 1/2/3/4/5/6/7 or describe.
```

## After Codex adversarial review completes

The human reads `.codex-outbox/<latest>.md`. Based on Codex's verdict:

- **CLEAN** → ready to build. Next: `/parallel-kickoff <prd-fork-id> <task-ids>`
- **CONCERNS** → human decides whether to fix or log risks. Often: fix highest
  severity, log the rest in risks.md, proceed.
- **BLOCK** → spec-writer revises, then `/plan-adversarial-next <prd-fork-id>` triggers R2.
  Max 4 rounds; after that human must decide whether to ship with open blockers
  or re-scope.

(The adversarial review loop command is `/plan-adversarial-next` — separate file.)

## Notes

- This command is a **coordinator**, not a doer. It kicks off spec-writer and
  task-decomposer (which do the real work) and primes Codex for review.
- Never call spec-writer directly without this command — it won't have the
  PRD → spec lineage context that this command arranges.
- After L4 is "CLEAN", human transitions to **parallel-kickoff** (already
  exists from v2.1) and **quality-gate** (already exists from v2.1). Those
  commands work unchanged.
