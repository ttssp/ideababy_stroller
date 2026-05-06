---
description: Show idea pipeline status. No arg = global dashboard (4-layer matrix + waiting-on-me + dead-branch hints). <id> = single idea drill-down. --activity [days] = recent activity timeline. --include-parked expands parked/abandoned section in global view.
argument-hint: "<id> | --activity [days] | --include-parked | (no arg)  e.g. 001  or  --activity 7"
allowed-tools: Read, Bash(ls:*), Bash(find:*), Bash(cat:*), Bash(stat:*), Bash(date:*), Bash(git:*), Bash(grep:*), Bash(rg:*), Bash(awk:*), Bash(sort:*), Bash(head:*), Bash(tail:*), Bash(wc:*), Glob, Grep
model: sonnet
---

# Status · idea state · 3 视图

根据 `$ARGUMENTS` 路由到不同视图:

- **空参数** → 视图 A · 全局面板 (Step 5 实现)
- `--activity [days]` → 视图 C · 活动流 (Step 6 实现, days 缺省 7)
- `--include-parked` → 视图 A 但展开 parked/abandoned 段
- `<id>` (NNN 或 NNN-fork) → 视图 B · 单 idea drill-down (Step 2-4 实现, 现有逻辑)

## Step 1 — figure out scope

```
case "$ARGUMENTS" in
  "")                          → 视图 A (Step 5)
  --activity*)                 → 视图 C (Step 6),  天数 = 第 2 个 token 或 7
  --include-parked)            → 视图 A (Step 5) + 展开 park/abandon
  *)                           → 视图 B (Step 2-4),  $ARGUMENTS 是 idea 或 fork
esac
```

视图 B 的 scope:
- `NNN` (e.g. `001`) → 显示 `discussion/NNN/` 下完整 tree (含所有 fork)
- `NNN-fork` (e.g. `001a`) → 仅显示该 fork 子树

## Step 2 — gather facts

```bash
# Which ideas exist
ls discussion/ 2>/dev/null

# For target idea, walk the tree
find discussion/$ARGUMENTS -type d 2>/dev/null
find discussion/$ARGUMENTS -name "stage-*.md" 2>/dev/null
find discussion/$ARGUMENTS -name "FORK-ORIGIN.md" 2>/dev/null
```

For each layer dir (L1/, L2/, L3/, L4/) found:
- Count rounds present per side (Opus and GPT)
- Check if `stage-L<n>-*.md` synthesis exists
- Last modified timestamp

For pending Codex tasks (v2 — multi-queue):
```bash
# 列出所有队列及当前 HEAD，并标注是否已被 Codex 完成
for d in .codex-inbox/queues/*/; do
  q=$(basename "$d")
  h=$(cat "$d/HEAD" 2>/dev/null)
  [ -z "$h" ] && continue
  if [ -f ".codex-outbox/queues/$q/$h" ]; then
    echo "$q  HEAD=$h  ✅ done"
  else
    echo "$q  HEAD=$h  ⏸ pending"
  fi
done
```

每个 idea / fork 都有自己的队列，多个 idea 并行时彼此独立。
判断规则：`queues/<id>/HEAD` 指向的任务文件**不存在于** outbox 对应路径 → 该
队列有未读 Codex 任务（需要 `cdx-run <id>`）。

如果 `$ARGUMENTS` 是具体 idea / fork-id，仅看对应队列即可（其他队列对它无意义）。

## Step 3 — render the tree

Use this format (no headers, just a clean ASCII tree + status badges):

```
Idea 001 · "Real-time collab whiteboard for educators"
Status: in L2-explore (fork: 001a)

discussion/001/
├── L1 · Inspire ✅ done
│   └── stage-L1-inspire.md  (10 directions, 3 selected for fork)
│
├── 001a [forked from L1 #3, 2 days ago]
│   └── L2 · Explore ⏳ in progress
│       ├── L2R1 ✅ both done
│       └── L2R2 ⏸ Opus done · Codex pending
│
├── 001b [forked from L1 #5, 2 days ago]  ⏸ parked
│   └── L2 · Explore — only L2R1 Opus done
│
└── 001c [forked from L1 #7, 1 day ago]
    └── L2 · Explore ⏳ in progress
        └── L2R1 ⏸ both done

Last action: Opus completed L2R2 for 001a, 12 minutes ago
Pending Codex: 1 inbox task (001a-L2R2) waiting for cdx-run
```

Status badges:
- ✅ = done
- ⏳ = in progress
- ⏸ = paused / waiting
- ⛔ = blocked
- 🅿️ = parked
- ❌ = abandoned

## Step 4 — next-step menu (always show this)

Based on the most recent action and what's missing, suggest the most likely next step:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 Suggested next steps:

[1] Wait for Codex 001a-L2R2 (queue=001a is pending)
    → in your Codex terminal: cdx-run 001a

[2] Check Opus's L2R2 output in 001a
    → I'll show you discussion/001/001a/L2/L2R2-Opus47Max.md

[3] Move 001c forward (next round needed)
    → /explore-next 001c 2

[4] Fork another direction from L1 menu
    → /fork 001 from-L1 direction-X as 001d

[5] Park the entire 001 tree (preserve all artifacts)
    → /park 001

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Reply 1/2/3/4/5 or describe what you want to do.
```

The menu items are computed dynamically from what the tree state actually allows.
Don't show options that don't apply (e.g. don't show "L4 plan" if no L3 done yet).

## Step 5 — 视图 A · 全局面板 (无参 / `--include-parked`)

视图 A 用于断点续做 — 一眼看清所有 idea/fork 在 4 层管线里的位置 + 等我处理的事。

### 5.1 收集事实(filesystem + git 反推, 无 cache)

**Shell 兼容性提醒** (这个仓库默认 zsh):
- 测试 glob 是否匹配文件用 `ls X >/dev/null 2>&1 && echo Y || echo N`,**不要**用 `ls X | head -1 >/dev/null` (管道前段失败被吞)
- zsh 默认 no-match 报错, 复杂 glob 段前 `setopt NULL_GLOB 2>/dev/null` 把空展开成空列表
- 优先用 `[ -f path ]` / `[ -d path ]` 显式判断单个文件存在


```bash
# (a) 所有 idea
ls discussion/ 2>/dev/null | grep -E '^[0-9]{3}$'

# (b) 每个 idea 下的 fork — 用 FORK-ORIGIN.md 作为真实标识 (排除 par-review 等归档目录)
for nnn in $(ls discussion/ 2>/dev/null | grep -E '^[0-9]{3}$'); do
  for d in discussion/$nnn/*/; do
    [ -d "$d" ] || continue
    fork=$(basename "$d")
    case "$fork" in L1|L2|L3|L4) continue;; esac
    [ -f "discussion/$nnn/$fork/FORK-ORIGIN.md" ] && echo "$nnn  $fork"
  done
done

# (c) 每个 (idea, fork) 的 layer 完成度
# 顶层 (idea root):
ls discussion/$nnn/L1/stage-L1-inspire.md 2>/dev/null     # L1 done
ls discussion/$nnn/L2/stage-L2-explore-*.md 2>/dev/null   # L2 done (idea 级)
ls discussion/$nnn/L3/stage-L3-scope-*.md 2>/dev/null     # L3 done (idea 级)
# fork 内 (003 这种 skip-L1 直接 fork 的):
ls discussion/$nnn/$fork/L2/stage-L2-explore-*.md 2>/dev/null
ls discussion/$nnn/$fork/L3/stage-L3-scope-*.md 2>/dev/null

# (d) L4 完成度: PRD.md 存在 + specs/<fork>/ 存在 + tag 存在
ls discussion/$nnn/$fork/PRD.md 2>/dev/null              # PRD ready (L3 收敛点)
ls specs/$fork/spec.md 2>/dev/null                        # spec 已写
ls specs/$fork/tasks/T*.md 2>/dev/null | wc -l            # task 数量
git tag -l "spec/$fork/v*" "v0.*_idea${nnn}*" 2>/dev/null # 发布 milestone

# (e) Codex pending — 看 inbox 里的 .md 是否有 outbox 同名/柔性匹配的对应文件
# 注意:HEAD 文件不可靠(归档历史不写 HEAD), 必须遍历每个 inbox .md
setopt NULL_GLOB 2>/dev/null  # zsh: 让 no-match 不报错
for d in .codex-inbox/queues/*/; do
  q=$(basename "$d")
  for inf in "$d"*.md; do
    [ -f "$inf" ] || continue
    fname=$(basename "$inf")
    # 严格同名匹配?
    [ -f ".codex-outbox/queues/$q/$fname" ] && continue
    # 柔性匹配(时间戳错位): 比较 "时间戳-之后" 部分
    base=${fname#[0-9]*-}
    found=
    for o in .codex-outbox/queues/$q/*${base}; do
      [ -f "$o" ] && found=Y && break
    done
    [ -z "$found" ] && echo "PENDING  $q  $fname"
  done
done
# 注意!! 上面的 PENDING 是"原始信号", 渲染前必须做"产物兜底过滤"。
# 关键原则:**只有当所有应有产物齐全时才能视为完成**, 单边产物 = 真未完成。
#
#   - 如果 inbox 任务是 codex (gpt-5.4) 派工 → 检查的不是单边而是 GPT 侧 outbox。
#     · L1R1/L1R2/L2R1/L2R2/L3R1/L3R2 codex 任务 → 产物 = discussion/<id>/Lx/LxRy-GPT54xHigh.md
#       该文件存在 = 完成; 不存在 = 真 PENDING (即使 Opus47Max.md 已写)
#     · 反例(必须避免): 002b-stablecoin-payroll L3R2 inbox 还在但只有 L3R2-Opus47Max.md
#       缺 GPT 侧 → 这是真未完成, 不能因为"看到一个 round 文件"就过滤掉
#   - L4 adversarial review: 看 outbox 里同一 fork 的 r1/r2/r_final/r_final2/r_final3 序列
#     · 如果某 inbox 是 r2 但 outbox 已有更高 round (r_final / r_final2) → 当已完成
#     · (Codex 在 r2 那次决定一并响应给 r_final, 跳过中间 round)
#   - 如果 inbox 文件名含 DEFERRED → 单独标 "🟡 已搁置" 而非 "🔴 待跑"
#
# 当对"是否真完成"有疑问时 → 优先报告 PENDING, 让 human 看到原始信号自己判断,
# 而不是过度过滤把真 PENDING 隐藏掉。

# (f) Park / Abandon 标记 — 注意: 可能在 idea root 或 fork 内,两层都要检测
#  · idea root parked: discussion/NNN/PARK-RECORD.md      → 整个 idea 树暂停 (含所有 fork)
#  · fork parked:      discussion/NNN/<fork>/PARK-RECORD.md → 仅该 fork 暂停, 其它 fork 继续
# 当前仓库示例: discussion/001/PARK-RECORD.md 是 idea-root 级
find discussion -maxdepth 2 -name "PARK-RECORD.md" -o -name "ABANDONED.md" 2>/dev/null    # idea root
find discussion -maxdepth 3 -name "PARK-RECORD.md" -o -name "ABANDONED.md" 2>/dev/null    # 含 fork 内

# (g) 死 worktree 分支 (有 worktree-* 分支但 worktree list 中无对应)
git branch -a 2>/dev/null | grep -oE 'worktree-[a-zA-Z0-9_-]+' | sort -u
git worktree list 2>/dev/null
```

### 5.2 4-Layer 矩阵渲染

**重要语义判断 (脚本拿不到, 模型必须自己做)**:

- fork 的 L1/L2/L3 完成度: 通常**继承自 idea root**, 不要重复显示 ─
  - 例: idea 003 顶层 L2/L3 都 ✅, fork 003-pA 是从 L3 fork 出来的 PRD,
    它本身就站在 L2/L3 完成的基础上。Fork 行 L2/L3 应该显示 ─ (N/A 不是缺失)
- "skip-mode" idea: 003 跳过 L1 直接进 L2, 顶层 L1 ─ 是正常的, 不是缺失
- 半完成检测: discussion/<id>/Lx/ 目录里有 LxR1-Opus 但缺 LxR1-GPT 或缺 stage-Lx-*.md
  → 该层应显示 ⛔ (而非 ✅ 或 ─)
- L3R2 单边缺失: 002b-stablecoin-payroll 有 L3R2-Opus 缺 L3R2-GPT → L3 应 ⛔
- L4 状态多 fork 滚动: 一个 idea 多 fork 时, L4 应取**最高进度**(任一 fork ship → ✅)

每个 idea 一行(顶层) + 每个 fork 一行(缩进)。状态列含义:

| Symbol | 意思 |
|---|---|
| ✅ | 该层已完成 (stage-Lx-*.md 存在 / spec ship / tag 打了) |
| ⏳ | 该层进行中 (有部分 round 但 stage doc 缺) |
| ⏸ | 该层等外部 (codex 队列 pending / 等 human 决策) |
| ⛔ | 该层有缺失需补 (如 L3R2 GPT 缺) |
| 🅿️ | parked |
| ❌ | abandoned |
| → | 该层完成,数据流向下一层 |
| ─ | 该层未触及(N/A 或还没到) |

模板:
```
                          L1   L2   L3   L4    Status
─────────────────────────────────────────────────────
001 <一句话标题截断>      ✅    →    ─    ─     L2 in progress · 1 fork active
  └ 001a                  ─    ⏳   ─    ─     L2R2 pending Codex
  └ 001c                  ─    ⏳   ─    ─     L2R1 both done

002 <一句话标题>          ✅    →    ─    ─     L1 done · 3 forks pending L2
  └ 002b-stablecoin-...   ─    ✅   ⛔   ─     L3R2 GPT 缺失 (sundvil, 无 PRD)
  └ 002f-payroll-er       ─    ⏳   ─    ─     L2R1 both done
  └ 002g-dao-bounty       ─    ⏳   ─    ─     L2R1 only Opus done

003 <一句话标题>          ─    ✅   ✅   ⏳    L4 build phase · v0.1 shipped
  └ 003-pA                ─    ─    ─    ⏳    v0.1 ✅ (tag v0.1.0_idea003) · v0.2 fleet ⛔ R1

004 <一句话标题>          ✅   ✅   ✅   ✅    shipped
  └ 004-pB                ─    ─    ─    ✅    R1-R4.1 CLEAN · merged
```

排序: 距离 ship 越近越上 (L4 ✅ > L4 ⏳ > L3 ✅ > L3 ⏳ > L2 ✅ > L2 ⏳ > L1 ✅ > L1 ⏳)。

### 5.3 折叠 Park / Abandon

**parked 单位有两层** (5.1(f) 已说明):
- idea-root 级 (`discussion/NNN/PARK-RECORD.md`) → 整个 idea 与其所有 fork 都暂停
  矩阵渲染: idea 行 Status 列标 🅿️ + 折叠所有子 fork
- fork 级 (`discussion/NNN/<fork>/PARK-RECORD.md`) → 该 fork 单独暂停, 同 idea 其它 fork 继续
  矩阵渲染: 仅该 fork 行 Status 列标 🅿️

默认输出 (无 `--include-parked` 时):

```
🅿️ Parked (折叠 N): 001 (idea-root) · 002b-foo (fork) · ...
   复活条件 (一行各): 001: <revival-condition 截断 60 字>
                       002b-foo: <revival-condition>
❌ Abandoned (折叠 N): <id-list>
```

`复活条件` 从对应 PARK-RECORD.md 的"复活条件" / "revival" 段提取。

如果 `$ARGUMENTS == --include-parked`, 把 parked/abandoned 的 idea/fork 当 active 一样画进矩阵, 标 🅿️/❌ 在 Status 列。idea-root 级 parked 时其所有子 fork 也展开但都标 🅿️。

### 5.4 "Waiting on me" 段 (痛点 3)

5 类聚合, 每条带可执行的下一步:

```
🔴 Waiting on me (N):
  · <queue>: codex pending → cdx-run <queue>
  · <fork>: L3 PRD 未 fork → /fork <id> from-L3 candidate-X as <new-fork>
  · <fork>: L4 task BLOCK → 见 specs/<fork>/STATUS.md §修补建议
  · <branch>: 死 worktree 分支 → git branch -D <branch>
  · <fork>: park 复活检查到期 (<日期>) → 重新评估 PARK-RECORD.md 复活条件
```

每类的检测规则:

| 类型 | 规则 |
|---|---|
| Codex pending | 5.1(e) 输出非空 |
| L3 PRD 未 fork | `discussion/<id>/L3/stage-L3-scope-<id>.md` 存在 但 `discussion/<id>/<some-fork>/PRD.md` 全部不存在 |
| L4 task BLOCK | `rg -l 'verdict.*BLOCK' specs/*/STATUS.md` |
| 死 worktree 分支 | 5.1(g) 中 `git branch -a` 列出但 `git worktree list` 无对应 |
| Park 复活到期 | `rg -l '复活检查日期.*<= today>' discussion/*/PARK-RECORD.md` (若存在该格式) |

### 5.5 Next-step menu (动态计算)

按 Waiting on me 优先级 + 自然推进点排:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 Suggested next steps:

[1] /status <最有进展的 fork>     # 深入看进度
[2] cdx-run <最老的 pending queue> # 推进卡最久的 codex 任务
[3] /status --activity 7          # 看过去 7 天活动流
[4] /status --include-parked      # 展开看 park 段
[5] /propose                      # 没事就提新 idea

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
回复数字或描述你想做的事。
```

---

## Step 6 — 视图 C · 活动流 (`--activity [days]`)

视图 C 用于看过去 N 天每个 idea 都发生了什么。

### 6.1 解析参数

```bash
# $ARGUMENTS 形如: "--activity" 或 "--activity 7" 或 "--activity 30"
days=$(echo "$ARGUMENTS" | awk '{print $2}')
days=${days:-7}
```

### 6.2 收集 commit 数据 (按 idea 分桶)

**重要 macOS 兼容**: 默认 `/usr/bin/awk` 是 BSD awk, 不支持 gawk 三参 `match($0, /re/, m)`。
统一用 POSIX `match() + RSTART + RLENGTH + substr()` 形式。

**T-task commit 归属的真实约束** (重要, 不要试图绕过):

仓库里大量 commit 是 `fix(T020)` / `feat(T013)` 这种纯 task 编号格式
(typically L4 build 阶段). **`T<NNN>` 在每个 fork 内独立计数** — 即
`specs/001-pA/tasks/T020.md`、`specs/003-pA/tasks/T020.md`、`specs/004-pB/tasks/T020.md`
全都存在但是不同任务。所以**不能**用 task→fork 反查 (会得到错误的归属)。

**唯一可靠的归属信息是 commit 所在分支** — 但 commit 一旦 merge 到 main, 分支信息丢失。
`git branch --contains <sha>` 能查到的是 "包含此 commit 的所有分支", 包括 main, 不能
唯一锁定原始 worktree。

**解决方式**: T-task commits 全部归到一个 **`L4-build` 桶**, 不再细分 idea。
理由:
- 真相就是这个: 一旦 merge, 归属信息就丢了
- 用户来跑 `--activity` 时主要是看"哪个 idea 在动 / 哪个沉默", L4-build 桶的存在恰好告诉
  用户 "有 L4 build 工作正在发生但具体哪个 fork 看不到" — 这是诚实的状态信号

```bash
# macOS BSD awk 兼容: 用 POSIX match() + RSTART/RLENGTH/substr(),  不用 gawk 三参 match()
days=${days:-7}
git log --all --since="${days}.days.ago" --pretty=format:'%h%x09%ai%x09%s' \
  | awk -F'\t' '
      {
        s = $3
        # 1) (NNN-fork) 显式归属 → 取 fork 名
        if (match(s, /\([0-9]{3}[a-zA-Z0-9-]*\)/)) {
          idea = substr(s, RSTART+1, RLENGTH-2)
        }
        # 2) (T<NNN>) → 归到 "L4-build" 桶 (无法可靠反查到 idea, 见上面说明)
        else if (match(s, /\(T[0-9]+\)/)) {
          idea = "L4-build"
        }
        # 3) Merge branch worktree-<id> → 归到对应 idea
        # branch 命名约定: "worktree-idea<NNN>" (历史) 或 "worktree-<NNN-fork>" 都可能
        else if (match(s, /Merge branch .worktree-[a-zA-Z0-9-]+./)) {
          chunk = substr(s, RSTART, RLENGTH)
          if (match(chunk, /worktree-idea([0-9]{3}[a-zA-Z0-9-]*)/)) {
            # worktree-idea001 → 归到 001
            idea = substr(chunk, RSTART+13, RLENGTH-13)
          }
          else if (match(chunk, /worktree-([0-9]{3}[a-zA-Z0-9-]*)/)) {
            # worktree-001-pA → 归到 001-pA
            idea = substr(chunk, RSTART+9, RLENGTH-9)
          }
          else { idea = "其他" }
        }
        # 4) 标准 conventional commit type(...) 但括号里不是 idea/T-id → 基础设施
        else if (match(s, /^(spec|chore|docs|build|test|review|refactor|feat|fix)\(/)) {
          idea = "基础设施"
        }
        else {
          idea = "其他"
        }
        count[idea]++
        if (!(idea in last_subj)) { last_subj[idea] = s; last_ts[idea] = $2 }
      }
      END {
        for (i in count) printf "%s\t%d\t%s\t%s\n", i, count[i], last_ts[i], last_subj[i]
      }' \
  | LC_ALL=C sort -k2 -nr
```

**macOS 注意**:
- `sort -t$'\t'` 在 macOS 默认 locale 下会因多字节字符报 `Illegal byte sequence`,
  解决: 加 `LC_ALL=C` 前缀 (上方已加)
- 默认 `/usr/bin/awk` 是 BSD awk, 不支持 gawk 三参 `match($0, /re/, m)`,
  上方代码全部用 POSIX `match() + RSTART + RLENGTH + substr()` 形式

### 6.3 渲染横向 bar chart

```
过去 N 天 (<起始日> → <今日>):

<idea>  <bar>  N commits · 主要: <最近一条 subject 截断>
...
<沉默 idea>  ░░░░░░░  0 commits · 沉默 X 天 ⚠️
```

bar 计算: 每 commit 一个 ▍, 上限 8 格(超出用 `+N`)。

### 6.4 沉默 idea 检测

active 但在 N 天内 0 commits 的 idea 单独标 ⚠️ — 数据来自:
- `proposals/proposals.md` 中 status 不是 parked/abandoned 的 idea
- 减去本期 commit 桶里出现的 idea

### 6.5 Next-step menu

```
📋 [1] 看 <最忙 idea> 详情      /status <id>
   [2] 唤醒 <沉默最久 idea>      /status <id>
   [3] 推进 <第二忙 idea>        /status <id>
```

---

## Style

- Output is for humans skim-reading; use tree characters and badges, not paragraphs
- Always end with the menu — never just dump status without saying what's next
- If multiple ideas have pending work, list them in order of "most recently active"
- 视图 A 优先**广度**(所有 idea 一目了然), 视图 B 优先**深度**(单 idea 完整 tree), 视图 C 优先**时间维度**(看节奏)
- 不要让单个 idea 的标题超过 30 字符,超出截断加 `…`
