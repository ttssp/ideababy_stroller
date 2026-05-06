# PI Briefing Console (`pi-briefing`)

> 本 worktree (`worktree-idea001`) 同时承载孵化器(根仓 `ideababy_stroller`)与
> idea 001-pA 工程交付包。pi-briefing 工程文件在根目录铺开;Idea Incubator
> 流程文档保留在本 README 下半部分。权威工程契约见
> [`specs/001-pA/README.md`](./specs/001-pA/README.md)。

## 本地启动 3 步

```bash
# 1. 装依赖(首次约 2 min)
pnpm install --frozen-lockfile

# 2. 准备 env + 本地 Postgres
cp .env.example .env       # 编辑 DATABASE_URL / SESSION_SECRET / ANTHROPIC_AUTH_TOKEN
createdb pi_briefing
psql -d pi_briefing -f specs/001-pA/reference/schema.sql

# 3. 跑起来
pnpm dev                   # → http://localhost:3000
```

## 主要脚本

| 命令 | 用途 |
|---|---|
| `pnpm dev` / `pnpm build` / `pnpm start` | Next dev / production build / start |
| `pnpm lint` / `pnpm typecheck` / `pnpm test` | Biome ci · `tsc --noEmit` · vitest run |
| `pnpm test:e2e` | Playwright (T008 后启用) |
| `pnpm worker:daily` | systemd timer 入口 (T011 后落地) |
| `pnpm db:generate` / `db:migrate` / `db:studio` | Drizzle Kit |
| `pnpm validate-env` | zod 校验 .env (T007 后落地) |

## 阅读顺序

- 新人 → `specs/001-pA/README.md` §2.2(初级工程师 1h ramp 路径)
- 架构师 → `specs/001-pA/README.md` §2.1
- operator → `specs/001-pA/README.md` §2.3

---

# Idea Incubator · v3.0

A single-operator, AI-team pipeline from raw idea to commercial-grade software.

## Core philosophy

Your idea is a **seed**. The pipeline is a **tree** that branches at every layer.
Every branch (fork) is a sibling, not nested. Every layer's output is
independently valuable — even ideas that get parked or abandoned leave behind
exploration documents worth keeping.

## The four layers

| Layer | Discusses | Search? | Human density |
|---|---|---|---|
| **L1 Inspire** | What inspired directions does this seed grow? Value, novelty, utility — NO tech | Value-validation only (in R2) | Low (let models fly) |
| **L2 Explore** | One chosen idea, deeply: novelty, utility, extensions, limits | Value-validation only (in R2) | Medium (give signals) |
| **L3 Scope** | Real requirements, what to build, what NOT to build | Free | High (your real needs) |
| **L4 Plan** | Spec, architecture, tasks, build, ship | Free | Medium (approve key calls) |

## Quick start

```bash
# 1. Setup (once)
mkdir my-incubator && cd my-incubator
tar xzf ~/Downloads/idea-incubator-v3.0-stage1.tar.gz
bash install.sh
bash scripts/codex-inbox-init.sh

# 2. Configure Codex shortcuts (once, in ~/.zshrc or ~/.bashrc)
# 见 .codex-inbox/README.md §"Codex 端推荐 alias"，把里面的
#   cdx-run() / cdx-peek() / cdx-queues()  三个函数粘贴进去
source ~/.zshrc

# 3. Drop an idea (one paragraph minimum)
claude
> /propose

# 4. L1 Inspire — let models break your cognitive limits
> /inspire-start 001
# (你看到菜单时选 [1];Codex 队列已就绪)
# in Codex terminal:  cdx-run 001
# back in Claude Code:
> /inspire-next 001
# in Codex terminal:  cdx-run 001     (默认 reuse-session,可粘菜单 [1] 段)
> /inspire-advance 001
# read the L1 menu; pick a direction:
> /fork 001 from-L1 direction-3 as 001a

# 5. L2 Explore — deep unpack the chosen direction
> /explore-start 001a
# in Codex terminal:  cdx-run 001a
> /explore-next 001a
# in Codex terminal:  cdx-run 001a    (默认 reuse-session)
> /explore-advance 001a
# read the explore report; if good:
> /scope-start 001a         # L3 starts with interactive intake
# answer 6-8 questions (each allows "not sure")
# Opus writes L3R1 (candidate PRDs); Codex 队列已就绪
# in Codex terminal:  cdx-run 001a
> /scope-next 001a
# in Codex terminal:  cdx-run 001a    (默认 reuse-session)
> /scope-advance 001a
# read the PRD menu; fork the one you like:
> /fork 001a from-L3 candidate-A as 001a-pA
# this auto-generates PRD.md in the new fork
> /plan-start 001a-pA       # L4 kicks off
# spec-writer runs, task-decomposer runs, Codex adversarial review queued
# in Codex terminal:  cdx-run 001a-pA   (adversarial R1)
# 若 BLOCK → 修后:  /plan-adversarial-next 001a-pA  (R2-R4,默认 reuse-session)
# if CLEAN → proceed to build:
> /parallel-kickoff 001a-pA T003,T004,T008
# 每个 task worktree 合并前必跑 review gate (iron rule):
> /task-review 001a-pA T003 --reviewer=claude-full
> /quality-gate 001a-pA
```

## Anywhere in the flow

```bash
> /status                  # see all ideas + active forks
> /status 001              # see this idea's full tree
> /status 001a             # see one fork's state
> /fork 001 from-L1 direction-7 as 001b   # historical retrospective fork
> /park 001a               # preserve, decide later
```

## Command reference (v3.0-stage1)

### Pipeline commands (per layer)
| Command | When |
|---|---|
| `/propose` | Drop a one-paragraph idea seed |
| `/inspire-start <NNN> [--mode=full\|narrow\|skip]` | Start L1 R1 (Daydream, no search) |
| `/inspire-next <NNN>` | L1 R2 (cross-read + value-validation search) |
| `/inspire-advance <NNN>` | Close L1, produce inspired menu |
| `/explore-start <fork-id>` | Start L2 R1 (Daydream, no search) |
| `/explore-next <fork-id>` | L2 R2 (cross-read + value-validation search) |
| `/explore-advance <fork-id>` | Close L2, produce explore report |
| `/scope-start <fork-id>` | Start L3 (R0 intake + R1 candidate PRDs) |
| `/scope-next <fork-id>` | L3 R2 (cross + scope-reality search) |
| `/scope-advance <fork-id>` | Close L3, produce PRD menu |
| `/scope-inject <fork-id>` | Add a moderator steering note at L3 |
| `/plan-start <prd-fork-id>` | Start L4 (spec + task DAG + Codex adversarial review prep) |
| `/parallel-kickoff <prd-fork-id> <task-ids>` | Launch parallel build workers (v2.1, preserved) |
| `/quality-gate <prd-fork-id>` | 10-gate pre-ship check (v2.1, preserved) |

### Tree management
| Command | When |
|---|---|
| `/fork <src> from-L<n> <candidate> as <new-id>` | Branch any layer's stage doc, anytime (incl. retrospective); from L3 auto-generates PRD.md |
| `/status [<id>]` | See full tree state + suggested next step |
| `/park <id>` | Preserve, set revival condition |
| `/abandon <id>` | Close out with structured lesson doc (appended to lessons-learned.md) |

### Deprecated (kept as escape hatch)
The v2.1 commands (`/debate-*`, `/spec-from-conclusion`) still work if you ever
need to bypass L1-L3 and drop straight into a debate→spec flow. Marked
DEPRECATED in their descriptions to avoid confusion.

## Decision-menu UX

Every command ends with a numbered menu. Reply with a digit or free text.

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ <what just happened>
   <key facts in 2-4 lines>

📋 Next steps:

[1] <most likely action — usually "send Codex via inbox">
[2] <second option — usually "inject a note">
[3] <show me what was just written>
[4] <fork or branch>
[5] <park or stop>

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Reply 1-5 or describe.
```

## Codex inbox/outbox (v2 · multi-queue)

You **never copy-paste a long prompt** between terminals. Claude Code writes a
self-contained task to `.codex-inbox/queues/<id>/<TS>-...md` and updates that
queue's `HEAD`. You run `cdx-run <id>` in Codex; Codex reads the HEAD-pointed
file, executes, writes confirmation to `.codex-outbox/queues/<id>/`.

每个 idea / fork 一个独立队列(`<id>` = idea 编号或 fork-id)。多 idea 并行不
冲突;`cdx-queues` 一行看完所有队列状态。两种 kickoff 形态(oneshot 与
reuse-session)详见 `.codex-inbox/README.md`。

## Directory structure

```
my-incubator/
├── CLAUDE.md                    # constitution
├── PLAYBOOK.md                  # operator manual (full design rationale)
├── README.md                    # you're here
│
├── .claude/
│   ├── settings.json
│   ├── commands/                # slash commands (see table above)
│   ├── agents/                  # subagents (inspire-synthesizer, explore-synthesizer, ...)
│   ├── skills/                  # protocol skills (inspire-protocol, explore-protocol, ...)
│   └── rules/                   # path-scoped rules
│
├── .codex-inbox/                # Claude→Codex tasks
│   ├── queues/<id>/HEAD         #   每队列指针(普通文件,非 symlink)
│   ├── queues/<id>/<TS>-*.md    #   每条任务自包含
│   └── archive/                 #   v1 历史(latest.md 时代)
├── .codex-outbox/               # Codex→Claude confirmations (queues/<id>/)
├── .codex/config.toml           # Codex project config
│
├── proposals/proposals.md       # idea seeds (one-paragraph minimum)
│
└── discussion/                  # the tree
    └── 001/                     # idea root
        ├── L1/                  # Inspire layer
        │   ├── L1R1-Opus47Max.md
        │   ├── L1R1-GPT54xHigh.md
        │   ├── L1R2-*.md
        │   ├── L1-moderator-notes.md
        │   └── stage-L1-inspire.md       # the inspired menu
        │
        ├── 001a/                # forked from L1 #3
        │   ├── FORK-ORIGIN.md   # lineage
        │   └── L2/
        │       ├── L2R1-*.md
        │       ├── L2R2-*.md
        │       └── stage-L2-explore-001a.md
        │
        ├── 001b/                # forked from L1 #5 (parallel sibling)
        │   └── ...
        │
        └── 001c/                # forked retrospectively, weeks later
            └── ...
```

## Apps that complement this workflow

- Claude Code (this repo's home)
- Codex CLI (the second-debater terminal)
- Optional: Claude Desktop (for reading long stage docs in a nice UI)
