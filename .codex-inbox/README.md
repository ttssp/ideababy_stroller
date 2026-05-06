# Codex Inbox / Outbox 机制 (v2 · 多队列)

## 这是什么

为了避免 human 在 Claude Code 和 Codex 终端之间反复"复制 kickoff、粘贴、记
住下一步、找文件"，本仓库使用 **文件总线** 在两个智能体之间传递任务。

- `.codex-inbox/queues/<queue-id>/` —— Claude Code 写、Codex 读。每个 .md = 一个待执行任务
- `.codex-outbox/queues/<queue-id>/` —— Codex 写、Claude Code 读。每个 .md = Codex 完成确认
- `<queue>/HEAD` —— 普通文本文件，单行 = 当前队列待执行任务的文件名
- `archive/` —— 历史任务文件（v1 时代的 flat 文件已搬入此处）

human 在 Codex 终端只需要敲：

```
cdx-run <queue-id>            # 例：cdx-run 003-pA
```

## 为什么改成多队列（vs v1 单 latest.md）

v1 用一个 `latest.md` symlink 指向"最新待执行任务"。多 idea 并行时（典型：003、
004 同时在等 Codex review）只能串行；多 git worktree 合并时 symlink 必冲突
（指向哪个文件无法 auto-merge）。

v2 以 **队列** 为隔离单位 —— 一个队列对应一个工作流通道（典型 = 一个 idea，分叉
后 = 一个 fork-id）。各队列各有 `HEAD` 文件互不干扰；HEAD 是普通文本，git 合并
冲突时是常规文本冲突，能正常处理。

## Queue ID 约定

```
未分叉:    queue = NNN          e.g. 001, 002, 004
分叉后:    queue = <fork-id>    e.g. 001a, 003-pA, 004-pB
```

各命令在写 inbox 时按以下规则推算 queue：
- `inspire-*`（L1）：`queue = $NNN`（L1 永远在 idea 根）
- `explore-*`（L2）/`scope-*`（L3）/`plan-*`（L4）：`queue = $ARGUMENTS`

## 目录结构

```
.codex-inbox/
  queues/
    003-pA/
      20260506T120000-003-pA-L4-adversarial-r2.md   ← 任务文件
      HEAD                                          ← 普通文件，单行 = 任务文件名
    004-pB/
      20260506T130000-004-pB-L4-adversarial-r4.md
      HEAD
  archive/                                           ← v1 flat 历史，已迁入
  README.md
```

`.codex-outbox/` 结构对称（Codex 写到对应 `queues/<id>/<同名>.md`）。

## 任务文件长什么样

每个任务文件自包含，Codex 读了就能执行：

```markdown
# Codex Task · idea 003-pA · L4 Adversarial R2

**Queue**: 003-pA
**Created**: 2026-05-06T12:00:00Z
**Created by**: Claude Code (Opus 4.7 Max acting as orchestrator)
**Recommended model**: gpt-5.4
**Recommended reasoning_effort**: xhigh
**Estimated tokens**: ~10-15k
**Kickoff form**: oneshot       ← 见下方 §"两种 kickoff 形态"

## 你需要做什么

[完整、自包含的任务描述：读哪些文件、不读哪些、写到哪、模板、约束]

## 完成后

把以下内容写到 `.codex-outbox/queues/003-pA/<同样的文件名>.md`：

```markdown
# Codex Done · 003-pA · L4 Adversarial R2
**Completed**: <ISO>
**Files written**: <list>
**Verdict**: CLEAN | CONCERNS | BLOCK
**Self-flag**: <anything Claude should know about>
```
```

## Codex 端推荐 alias

在 `~/.bashrc` / `~/.zshrc` 加（以下函数版本，老 alias 会失效，请整段替换）：

```bash
# 跑某队列下当前 HEAD 任务
cdx-run() {
  local q="$1"
  if [ -z "$q" ]; then
    echo "用法: cdx-run <queue-id>   例: cdx-run 003-pA"
    echo "可用队列:"
    cdx-queues
    return 1
  fi
  local headfile=".codex-inbox/queues/$q/HEAD"
  if [ ! -f "$headfile" ]; then
    echo "队列 $q 不存在或无 HEAD: $headfile"
    return 1
  fi
  local task_filename
  task_filename=$(cat "$headfile")
  local task_path=".codex-inbox/queues/$q/$task_filename"
  if [ ! -f "$task_path" ]; then
    echo "HEAD 指向不存在的任务文件: $task_path"
    return 1
  fi
  codex --model gpt-5.4 -c reasoning_effort=xhigh \
    "read $task_path and execute exactly what it says, then write the corresponding .codex-outbox/queues/$q/$task_filename confirming what you did"
}

# 偷看某队列下一步要干嘛
cdx-peek() {
  local q="$1"
  if [ -z "$q" ]; then echo "用法: cdx-peek <queue-id>"; return 1; fi
  local h=".codex-inbox/queues/$q/HEAD"
  [ -f "$h" ] || { echo "队列 $q 无 HEAD"; return 1; }
  echo "HEAD: $(cat "$h")"; echo '---'
  cat ".codex-inbox/queues/$q/$(cat "$h")" | head -60
}

# 列所有队列与各自 HEAD（看哪些 idea 在等 Codex）
cdx-queues() {
  for d in .codex-inbox/queues/*/; do
    [ -d "$d" ] || continue
    local q
    q=$(basename "$d")
    local h
    h=$(cat "$d/HEAD" 2>/dev/null || echo "(empty)")
    # 检查 outbox 对应文件是否已存在 → 表示 Codex 已跑过
    if [ -f ".codex-outbox/queues/$q/$h" ]; then
      echo "$q  →  $h  ✅ done"
    else
      echo "$q  →  $h  ⏸ pending"
    fi
  done
}
```

之后每次 Claude Code 提示 "Codex 任务已就绪 (queue=XXX)"，你只要：

```
cdx-run XXX
```

## 模型 / effort 覆盖

任务 frontmatter 含 `Recommended model` 与 `Recommended reasoning_effort`。
高质量发散（L1/L2）用 `gpt-5.4 + xhigh`，执行性任务可降。手动覆盖：

```bash
codex --model gpt-5.4 -c reasoning_effort=high
```

之后再 `cdx-run <queue>`。

## 两种 kickoff 形态

每个 inbox 任务的 frontmatter 都含 `**Kickoff form**: oneshot | reuse-session`。
两种形态对应两种 Codex 启动方式：

### 形态 1 — oneshot（每次新会话）

```bash
cdx-run <queue>     # 等价于 codex --model gpt-5.4 -c reasoning_effort=xhigh "..."
```

**适用**：
- 任意 `*-start`（idea / fork 第一次接触，无可复用上下文）
- 跨 idea 切换
- 上一轮 Codex 会话已退出 / 时间过久

**特点**：每次重新读 SKILL/proposal/前轮文件，prompt cache 全部 miss；适合
独立轮次但贵。

### 形态 2 — reuse-session（同一终端连贯派工）

人类在已开的 Codex 终端中**直接粘贴** Claude 在 next-step 菜单里给的短 prompt。
Codex 沿用上一轮的会话上下文，**只读 diff**。

任务文件里会有一段 `## Session hint`：
```markdown
## Session hint (only meaningful if Codex reuses session from R<n-1>)
你已读过：<列表>
本轮新增需读：<diff list>
**HARD CONSTRAINT (reuse only)**: do NOT re-read files you read in the
previous round of this Codex session unless this task explicitly lists them.
```

**适用**（默认 reuse-session 的命令）：
- `inspire-next` / `explore-next` / `scope-next`：R2 与 R1 ~80% 上下文重叠
- `plan-adversarial-next`（R2-R4）：~85% 重叠 ← 收益最大

**预计省 token**：50-70%（取决于 spec 包大小与重叠率）

### 命令默认形态对照表

| 命令 | 默认 | 备选 |
|---|---|---|
| `inspire-start` | oneshot | reuse（罕见） |
| `inspire-next` | reuse | oneshot |
| `explore-start` | oneshot | reuse（罕见） |
| `explore-next` | reuse | oneshot |
| `scope-start` | oneshot | reuse（罕见） |
| `scope-next` | reuse | oneshot |
| `plan-start` | oneshot | reuse（罕见） |
| `plan-adversarial-next` | reuse | oneshot |
| `task-review` (mode=codex) | oneshot | reuse |

### 为什么有两种形态

跨模型 debate 需要大量上下文，oneshot 每轮全部重读太贵；但 reuse-session 又
不能让人类机器人式连开终端。把选择权交给人类：默认走最省 token 的形态，菜单
里同时给"新开 oneshot"备选，避免会话断了人类没法回退。

## /status 怎么扫

`/status` 命令现在扫的是：
- `ls .codex-inbox/queues/*/HEAD` 找出所有未完成队列
- 对每个队列，比对 `outbox/queues/<q>/<HEAD-file>` 是否存在 → ✅ 已完成 vs ⏸ 待跑

## 不用 inbox 行不行？

可以。每个命令的"下一步菜单"里都会打印自包含 kickoff 文本（包括复用会话版本），
human 可以传统粘贴。inbox 只是 **可选的快捷路径**。
