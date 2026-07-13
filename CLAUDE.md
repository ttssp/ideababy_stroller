# Idea Incubator — Project Constitution

This repo is a **tree** from raw idea to shipped software. Powered by a single
human operator and a team of AI agents (Claude Opus 4.7, GPT-5.4 xhigh,
Sonnet 4.6, Codex 5.3/5.4, Haiku 4.5).

## The 4-layer pipeline (each layer can fork)

```
Proposal (one-paragraph seed)
  │
  ▼
L1 · Inspire   — daydream N inspired directions, value/novelty/utility only
  │  output: stage-L1-inspire.md (menu of directions)
  │  fork: human selects 1+ directions → 001a, 001b, ...
  ▼
L2 · Explore   — deep unpack of one chosen idea, still no tech
  │  output: stage-L2-explore-<fork>.md (rich essay about the idea)
  │  fork: optional sharper cuts of the same idea
  ▼
L3 · Scope     — real requirements, what to build, what NOT to build
  │  output: PRD-v<n>.md (real product requirements with human's constraints)
  │  fork: different PRD interpretations
  ▼
L4 · Hand-off  — produce hand-off package; downstream build runtime (XenoDev) does spec/tasks/build/quality
  │  output: HANDOFF.md → XenoDev consumes (per framework/SHARED-CONTRACT.md §6 v2.0)
```

Every layer's output is **independently valuable**. An L1 inspire menu may stay
useful for years even if no fork is ever built. An L2 deep dive captures a way
of thinking that's worth keeping. Park is normal; Abandon comes with a lesson doc.

## XenoDev 跨仓(IDS = 治理 · XenoDev = 唯一 L4 build runtime)

真正的代码开发**不在本仓**。本仓(IDS)管 idea→PRD→治理(L1-L4 hand-off + forge);
`XenoDev`(本机路径见 `$XENODEV_ROOT`,当前为 `/home/ys/codes/XenoDev`)是**唯一 L4 build runtime** —— 消费 IDS 的 hand-off
包,产可 ship 的代码,跑完产 hand-back 包写回 IDS。(per forge v2 verdict + SHARED-CONTRACT §6)

- **何时从 IDS 切到 XenoDev**:L4 `/plan-start` 产出 HANDOFF.md 后 → **新开 XenoDev session** 真开发
  (`cd "$XENODEV_ROOT" && claude`,`$XENODEV_ROOT` 见 `~/.bashrc`)。spec/tasks/build/quality 全在 XenoDev。
- **何时从 XenoDev 切回 IDS**(决策入口):
  - **框架级问题**(协议 / SKILL / hand-back / mirror / 并发机制的缺陷/优化)→ XenoDev 记
    `dogfood-backlog.md` → 攒批回 IDS 起 `/expert-forge 006`(框架级变更**只**走 forge,XenoDev 不当场改)
  - **PRD 问题** → hand-back → `/handback-review` → `/scope-inject` 改 PRD
  - **重大架构转向** → 必须 `/expert-forge`(防 V4 失败模式)
- **权威边界**:详尽两仓分工 / hand-back schema / 切回决策矩阵见 `framework/SHARED-CONTRACT.md` §6
  + XenoDev `CLAUDE.md`「dogfood 铁律」+「当出问题时」决策矩阵。本段是 IDS 侧的快速指针。

## Iron rules

- **Layer discipline**: L1/L2 NEVER discuss tech/feasibility/cost. L3 brings in
  human's real constraints. L4 is engineering. Don't mix.
- **PRD is source of truth after L3**: L4 agents (spec-writer) read PRD but
  don't alter product decisions. If PRD has issues, escalate to human.
- **No code without a spec**: a task without `specs/.../tasks/T<NNN>.md` does
  not execute. (L4 only.)
- **TDD for production code** (L4): tests first, fail, then implement, then green.
- **Pre-merge review mandatory** (L4 build): every parallel-builder worktree
  MUST pass `/task-review <fork> T<NNN>` with verdict ≠ BLOCK before merging.
  Reviewer mode is operator's choice (`claude-light` / `claude-full` / `codex`
  / `mixed`). See `.claude/commands/task-review.md`.
- **Cross-model review mandatory** for v1.0 paths (L4 quality gate).
- **Specs are immutable from build workers** — only operator + spec-writer touch them.
- **Every command outputs a next-step menu** — human never has to guess what's next.
- **"Not sure" is a first-class answer in L3R0 intake** — models must offer
  options for ❓ items, not pressure human to decide.
- **Think in English, reply in Chinese** — reason internally in English, output in Chinese

## Codex inbox/outbox bus (v2 · 多队列)

Cross-agent coordination uses `.codex-inbox/queues/<id>/` 和
`.codex-outbox/queues/<id>/`，每个 idea / fork-id 一个独立队列（见
`.codex-inbox/README.md`）。human 在 Codex 终端运行：

```
cdx-run <queue-id>      # 例：cdx-run 003-pA
cdx-queues              # 看所有队列与 HEAD 状态
```

旧的单一 `latest.md` symlink 在 v2 已废弃 —— 多 idea 并行/多 worktree 不再冲突。

## Session-per-idea worktree 规约 (forge 006 v8 · 簇② · 2026-07-13)

> **根因**:并行多线的**分支拓扑从未成为框架对象**。实证:001/006/009 三 idea 20+ commits
> 混在 `forge/009-blueprint` 一根命名分支上(混线发生在**有规约意识的 operator** 身上,说明
> 光靠自觉不够)。本节把「一个 session 只 working on 一个 idea、各自独立 worktree」定为规约。

**默认命令**:每开一个 session working on 某个 idea,用 Claude Code **原生** worktree flag:

```
claude -w <idea>        # 复用原生 -w/--worktree,零自建;自动建分支 + 独立目录
```

- **命名约定**:worktree 目录名 / 分支名 = idea id(如 `001`、`006`、`009-pForge`)。
- **零自建**:复用 Claude Code 原生 `-w`(forge v8 P2 双方本机 `claude --help` 实证已有),
  不造启动器。

**main 分支生命周期**(operator 原话「只有刚开始 proposal 的时候用 main」的规约化):

```
proposal on main                          # 新 idea 起于 main(/propose 写 proposals.md)
  → idea worktree branch                  # 之后每个 session 在 idea 独立 worktree/分支
  → accepted governance artifact
    经 human checkpoint 合回 main          # 定稿的治理产物合回 main
  → branch cleanup                        # 合回后清理 idea 分支
```

- **checkpoint 复用既有决策点**,不新设仪式——自然候选:`handback-review` 决议后 /
  stage 文档定稿后 / forge verdict 落地后。合回频率由 operator 节奏定。
- **合回前 main 不得反向污染**:idea 分支上只累积**本 idea** 的内容,不夹带其它 idea。

**warn 型起步(不阻断)**:本规约 P0 只做 **warn 型 preflight**——session 的
worktree/分支名与 working idea 不匹配时**提示不拦截**。hook block(commit-time 硬拦)留 v0.2,
升级判据 = warn 上线后 mismatch 混线**仍复发 ≥2 次**(判据数据来自真跑,对齐 v7「真跑校准」先例)。

**生效范围**:本规约对 forge v8 落地后**新开的 session** 生效;**存量混线分支**
(如当前 `forge/009-blueprint` 已有的 001/006/009 交织历史)**不追溯拆分**——强拆已 push 前
的连续历史反而增乱,让它随各 idea 自然 checkpoint 合回 main 后清理即可。

**跨仓一致**:XenoDev 侧同构规约(见 XenoDev `CLAUDE.md`);hand-back / outbox 包 frontmatter
加 `current_idea` / `worktree` / `baseline` 三字段(跨仓通道自带拓扑自证 · 授权条目下发)。

**已知局限(v0.2 note)**:worktree **不隔离** DB/env/端口/运行时服务(SOTA 提醒)——XenoDev
两 session 并行跑测试的资源互斥面,出现第一次真冲突后再规约化(forge v8 §"v0.2 note" 4)。

## Tool preferences

- Search: `rg` (ripgrep), never raw `grep`
- JS/TS: `pnpm`, Node 22 LTS, TS strict, Biome
- Python: `uv` for env+install, `ruff`, `pytest`
- Go: standard toolchain, `golangci-lint`
- iOS: Xcode 16+, SwiftLint, XCTest
- Commits: Conventional Commits

## Directory ownership

- `proposals/proposals.md` — operator writes (one-paragraph seed minimum)
- `discussion/NNN/L1/` — inspire layer; only the layer's commands write here
- `discussion/NNN/<fork-id>/L2/` — explore layer per fork
- `discussion/NNN/<fork-id>/L3/` — scope layer per fork
- `discussion/NNN/<fork-id>/<prd-version>/L4/` — plan layer per PRD version
- `discussion/NNN/<fork-id>/<prd-version>/L4/HANDOFF.md` — produced by `/plan-start` (v3.0+, M2 cutover);XenoDev build runtime consumes
- `specs/NNN-<fork-id>-<prd>/` — **DEPRECATED M3** (commit d3194a0):4 fork specs/ archived as forge v2 evidence;IDS no longer produces specs/(see SHARED-CONTRACT §6 v2.0)
- `projects/NNN-<fork-id>/` — historical parallel-builder worktrees (pre-M2);new builds happen in XenoDev repo
- `.codex-inbox/`, `.codex-outbox/` — agent coordination bus

## Prohibited

- L1/L2 emitting tech/feasibility content (re-route to L4)
- Auto-generating `AGENTS.md` or `CLAUDE.md` (LLM-generated context hurts quality)
- Modifying `specs/` at all (M3 verdict 2026-05-10 commit d3194a0: 4 fork specs/ archived as forge v2 evidence;no further task additions / reviews)
- Committing `.env*` files
- Forking >3 levels deep without strong reason

## When things feel off

1. `/status NNN` to see ground-truth state of any tree
2. `/clear` and restart from a stage doc if context feels polluted
3. If a layer keeps drifting into the wrong content (L2 doing tech), re-read the
   layer's protocol skill and consider injecting a moderator note

## Not in scope for this CLAUDE.md

- Per-project details (`projects/<fork-id>/CLAUDE.md`)
- Personal preferences (`~/.claude/CLAUDE.md`)
- Path-scoped rules (`.claude/rules/*.md` with `paths:` frontmatter)
