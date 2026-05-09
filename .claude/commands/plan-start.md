---
description: Start L4 Hand-off phase for a forked PRD branch. Produces a hand-off package (HANDOFF.md with workspace + source_repo_identity blocks) that XenoDev build runtime consumes. IDS itself no longer produces specs/ — that responsibility moved to XenoDev per SHARED-CONTRACT §6 v2.0.
argument-hint: "<prd-fork-id>  e.g. 001a-pA"
allowed-tools: Read, Write, Bash(mkdir:*), Bash(echo:*), Bash(ls:*), Bash(date:*), Bash(realpath:*), Bash(git config:*), Bash(git rev-parse:*), Bash(head:*), Bash(shasum:*), Glob, Grep
model: opus
---

# Plan · L4 entry — from PRD to hand-off package (v3.0)

PRD branch **$ARGUMENTS** (e.g. `001a-pA`).

> **v3.0 (M2 cutover, 2026-05-10)**:Per `framework/SHARED-CONTRACT.md` §6 v2.0,IDS 不再产 `specs/`,只产 hand-off 包(HANDOFF.md)写到 `discussion/<id>/<prd>/L4/`。spec/architecture/tasks/build/quality 全部移交 XenoDev build runtime(`/Users/admin/codes/XenoDev`)。本命令的 v2.2(产 specs/ + Codex review loop)已淘汰。

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
6. `framework/SHARED-CONTRACT.md` §6 v2.0(workspace schema 4 字段 + hand-back 通道)

## Step 2.5 — detect PRD-form (透传到 hand-off 包)

读 PRD.md frontmatter,提取 `**PRD-form**`(缺失时默认 simple)。同时提取形态特异 frontmatter:
- phased: `**Phases**` 数组
- composite: `**Modules**`、`**Module-forms**`、`**Critical-path module**`
- v1-direct: `**Skip-rationale**`(全文)

**校验失败处理**(任一失败立即报错并停止):
- composite 缺 `**Modules**` 或 module 数 <2
- phased 缺 `**Phases**` 或数组长度 <2
- v1-direct 的 skip-rationale <100 字 / 缺 C1/C2/C3 / PRD §"Risk: skip-v0.1" fallback path 仍是 `<待补充>`

记录 `<PRD-FORM>` / `<PHASES>` / `<MODULES>` / `<MODULE-FORMS>` 等变量,Step 3 透传给 hand-off 包 frontmatter(XenoDev 端 spec-writer 据此分派形态分支)。

## Step 3 — write HANDOFF.md (hand-off 包,§6.3 schema)

依据:`framework/SHARED-CONTRACT.md` §6 v2.0(contract_version 2.0)。

**目标路径**:`discussion/<root>/<parent-fork>/<prd-fork-id>/L4/HANDOFF.md`

(L4 目录不存在则 `mkdir -p`)

### 模板(替换 `<...>` 占位为真实值)

```markdown
---
# §6.2 workspace schema 4 字段
workspace:
  source_repo: <`realpath .` of IDS repo>
  build_repo: /Users/admin/codes/XenoDev
  working_repo: <`realpath .` of IDS repo (operator 当前所在仓)>
  handback_target: <`realpath .`>/discussion/<root>/handback/

# §6.5 第 13 项 source_repo_identity 字段(由 IDS forward 产源时填入,XenoDev 验)
source_repo_identity:
  expected_remote_url: <`git config remote.origin.url` 输出,无 remote 留空>
  repo_marker: <`head -c 30 CLAUDE.md`,MUST contain "Idea Incubator">
  git_common_dir_hash: <可选;`shasum -a 256 .git/HEAD .git/config | head -c 16`>

# Hand-off metadata
prd_fork_id: <prd-fork-id>
discussion_id: <root>
prd_form: <PRD-FORM>
phases: <如 phased,数组>
modules: <如 composite,数组>
module_forms: <如 composite,字典>
critical_path_module: <如 composite>
skip_rationale: <如 v1-direct,首段>

handed_off_at: <`date -u +%Y-%m-%dT%H:%M:%SZ`>
prd_source: <`realpath` of PRD.md>
shared_contract_version_honored: 2.0
---

# Hand-off · <prd-fork-id> → XenoDev (per SHARED-CONTRACT §6 v2.0)

**Handed off at**: <ISO timestamp>
**PRD source**: <`realpath discussion/<root>/<parent-fork>/<prd-fork-id>/PRD.md`>
**Build repo**: /Users/admin/codes/XenoDev
**Workspace**: 见 frontmatter `workspace:` 块(§6.2 4 字段全填)
**Source repo identity**: 见 frontmatter `source_repo_identity:` 块(XenoDev 写 hand-back 前必须按 §6.2.1 约束 3 校验)
**SHARED-CONTRACT version honored**: 2.0

## §1 · 给 XenoDev operator 的指令

operator 切到 build_repo 后:

1. `cd /Users/admin/codes/XenoDev`
2. 读本 HANDOFF.md(全文)+ 引用的 PRD.md
3. 在 XenoDev session 触发 XenoDev 自带的 spec-writer(per XenoDev AGENTS.md;**不**调 IDS 的 spec-writer subagent — XenoDev 派生自己的)
4. spec-writer 产 XenoDev 内部 spec.md(7 元素 schema,具体格式见 XenoDev `templates/spec.template.md`)
5. XenoDev task-decomposer 产 tasks/T*.md
6. parallel-builder 跑 task,quality gate 在 XenoDev 内部决议
7. 每个 task ship 后 XenoDev 产 hand-back 包(per §6.3 schema)写回 IDS `<source_repo>/discussion/<discussion_id>/handback/`

## §2 · PRD-form 透传(XenoDev spec-writer 分派依据)

`prd_form: <PRD-FORM>`(详见 frontmatter)

- simple    → 标准 7 文件输出
- phased    → SLA / risks 按 PRD `**Phases**` 数组分段
- composite → 顶层 spec.md 退化为 INDEX,**额外**为每 module 输出 spec-<m>.md
- v1-direct → SLA.md 顶部加 §'Skip rationale'

## §3 · §6.2.1 6 约束自检契约(XenoDev producer 写 hand-back 前必走)

per `framework/SHARED-CONTRACT.md` §6.2.1,XenoDev 产 hand-back 包写入 `<source_repo>/discussion/<discussion_id>/handback/` 前,必须按 6 约束自检:

1. canonical-path containment(realpath prefix 校验)
2. symlink reject(路径任一段是 symlink 即拒)
3. repo identity check(三模式:remote / no-remote / hash-only,任一 PASS 即满足)
4. id consistency check(三处 id 严格一致)
5. id 字符集 + filename basename + final-path containment(OWASP path traversal 防御)
6. hard-fail(任一约束失败,producer 不写 / consumer 不读)

任一失败 = `Drop`(不写文件,不创目录,只 stderr)。

## §4 · Open questions for build phase

(IDS PRD 中**关于 build 路径选择**的 OQ 在此承载;XenoDev build 自然遇到时再解决,不污染 XenoDev spec frozen)

(由 operator 从 IDS PRD §"Open questions" 手工分流后填入)

## §5 · Rollback plan

如果 XenoDev build 失败:
- (a) 回到 IDS 修 PRD,重跑 `/plan-start`
- (b) 改 XenoDev spec(不改 IDS PRD),用 XenoDev 自己的修订机制
- (c) 起 forge v3 重新审整个 idea
- (d) XenoDev 产 hand-back 包(tags: `prd-revision-trigger`)写回 IDS,operator 在 IDS 跑 `/handback-review <id>` 决议
```

### 实装动作

```bash
TS="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
PRD_SOURCE="$(realpath discussion/<root>/<parent-fork>/<prd-fork-id>/PRD.md)"
SOURCE_REPO="$(realpath .)"
HANDBACK_TARGET="${SOURCE_REPO}/discussion/<root>/handback/"
EXPECTED_REMOTE="$(git config remote.origin.url 2>/dev/null || echo '')"
REPO_MARKER="$(head -c 30 CLAUDE.md)"
# 然后用 Write 工具落盘上面模板的实化版本
mkdir -p discussion/<root>/<parent-fork>/<prd-fork-id>/L4/
```

### 验收

```bash
HANDOFF="discussion/<root>/<parent-fork>/<prd-fork-id>/L4/HANDOFF.md"
test -f "$HANDOFF" && \
  grep -q "shared_contract_version_honored: 2.0" "$HANDOFF" && \
  grep -q "workspace:" "$HANDOFF" && \
  grep -q "source_repo_identity:" "$HANDOFF" && \
  grep -q "/Users/admin/codes/XenoDev" "$HANDOFF" && \
  grep -q "§6.2.1" "$HANDOFF" && \
  echo "HANDOFF.md OK"
```

## Step 4 — output next-step menu

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ L4 Hand-off package generated for <prd-fork-id>.

Generated:
  discussion/<root>/<parent-fork>/<prd-fork-id>/L4/HANDOFF.md
    (workspace + source_repo_identity blocks · §6.3 schema · v2.0)

📋 Next step: switch to XenoDev build runtime

[1] (默认) 切到 XenoDev 仓继续
    → cd /Users/admin/codes/XenoDev
    → cat <abs path of HANDOFF.md>
    → 在 XenoDev session 触发 XenoDev 自己的 spec-writer
       (XenoDev 不调 IDS 的 spec-writer subagent;XenoDev 派生自己的)

[2] Show me the hand-off package
    → I'll display discussion/<root>/<parent-fork>/<prd-fork-id>/L4/HANDOFF.md

[3] Show me the PRD that was handed off
    → I'll display the PRD.md

[4] Pause — I want to read everything before switching repos
    → run /status <prd-fork-id> to see state when ready

[5] (after XenoDev runs) Review hand-back packages
    → /handback-review <discussion-id>
    (XenoDev produces hand-back packages per task ship; operator decides 下一步)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Reply 1/2/3/4/5 or describe.
```

## After XenoDev consumes hand-off

XenoDev 跑完一个或多个 task ship 后产 hand-back 包,跨仓写回 IDS `<source_repo>/discussion/<discussion_id>/handback/`(per §6.4)。

operator 在 IDS 仓运行:

```
/handback-review <discussion-id>
```

逐条决议 §6.3 三标签(drift / prd-revision-trigger / practice-stats),写入 `discussion/<id>/handback/HANDBACK-LOG.md`(append-only 决议日志)。

可选后续:
- 若有 PRD-revision-trigger → `/scope-inject` 修 PRD 后重跑本 `/plan-start` 产新 hand-off 包
- 若累积 N 条 hand-back 呈现系统性 drift → `/expert-forge <id>` 起新一轮 forge

## Notes

- 本命令是 **hand-off 包 producer**,不是 build doer。所有 spec/task/build/quality 在 XenoDev 内部完成。
- IDS 的 spec-writer / task-decomposer subagents 在 v3.0 后**不再被本命令调用**(M3 已把 4 个 fork 的 specs/ 标 DEPRECATED)。XenoDev 派生自己的 spec-writer(per stage doc §W2)。
- 跨仓 audit trail:hand-off 包的 `workspace.handback_target` 字段告诉 XenoDev 写 hand-back 写到哪;hand-back 包写回后 `/handback-review` 是 operator 在 IDS 端的入口。
- v2.2 → v3.0 breaking change 见 `framework/SHARED-CONTRACT.md` Changelog v2.0 entry。
