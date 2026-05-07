---
description: Redebate L2 Explore for a fork — when external knowledge changes, re-run L2 with new R1+R2+advance. Default --mode=in-place archives v1 to _archive/v1/ and produces v2 in same dir. L1 not supported (use /inspire-inject + re-run instead). Stage 1 MVP — only --mode=in-place is implemented; --mode=fork lands in Stage 3.
argument-hint: "<fork-id-or-idea-number> [--reason \"<text>\"] [--no-search]   e.g. 003-pA --reason \"native cache\""
allowed-tools: Read, Write, Edit, Bash(mkdir:*), Bash(cp:*), Bash(mv:*), Bash(echo:*), Bash(ls:*), Bash(date:*), Bash(test:*), Bash(stat:*), AskUserQuestion, Glob, Grep
model: opus
---

# Explore · L2 redebate (Opus side, R1 of new round)

Target **$ARGUMENTS**（解析见 Step 0）。

> **范围声明（Stage 1 MVP）**
> - 只支持 `--mode=in-place`。`--mode=fork` 会报"未实现，请等 Stage 3"。
> - 下游 dirty 标记在 Stage 2 才落地；本命令的 advance 完成后会留下一段
>   "TODO: Stage 2 will mark downstream"，不会自动改 spec/tasks。
> - **L1 不支持 redebate**：若需要重做 L1，使用 `/inspire-inject` + `/inspire-next`，
>   或 `/propose` 新 idea。

## Step 0 — 解析参数

`$ARGUMENTS` 形如：`<target>` 或 `<target> --reason "..."` 或 `<target> --no-search`。

提取：
- `target`（fork-id 或 root NNN，必填）
- `reason`（可选 string）
- `no_search`（bool，默认 false）
- `mode`（默认 `in-place`；若用户传 `--mode=fork`，**Stage 1 直接报错退出**：
  > "fork 模式还未实现（Stage 3 计划）。当前请用 --mode=in-place，或先用
  >  /fork <target> from-L2 ... 走传统 fork。"）

## Step 1 — 定位目标 + 状态预检

### 1.1 路径解析

| target 形态 | L2 目录 |
|---|---|
| fork-id（如 `003-pA`，含字母后缀或 `-pX` / `-r<k>`） | `discussion/<root>/<target>/L2/` |
| root NNN（如 `003`） | `discussion/<root>/L2/` |

`<root>` = target 的前缀数字（regex `^[0-9]+`）。

### 1.2 状态检测

```bash
ls discussion/.../<target>/L2/ 2>/dev/null
```

四种状态分支：

- **L2 目录不存在** → STOP，输出：
  > "L2 还未启动 — redebate 需要既有 stage doc。请先 `/explore-start <target>`。"

- **进行中（有 R1 但无 stage doc）** → STOP，输出：
  > "L2 当前在跑（检测到 L2R1-*.md，但 stage-L2-explore-<target>.md 不存在）。
  >
  > Redebate 的本质是『对**已完成层**重新辩论』，需要一个既有 baseline（stage doc）
  > 才能让新一轮在 §0 反思修订。当前没有 baseline，redebate 语义不成立。
  >
  > 请按需求选其一：
  >  - 想完成当前讨论再 redebate：跑完 `/explore-next <target>` + `/explore-advance <target>`，
  >    待 stage doc 产出后再 `/explore-redebate <target>`。
  >  - 想放弃当前 R1 重做：手工 `rm discussion/.../<target>/L2/L2R1-*.md`，再 `/explore-start <target>`。
  >  - 想给当前未完成的 R2 加约束：`/explore-inject <target>`（这才是 inject 的语义）。"

  STOP — **不**进入 Step 2。

- **已 advance（stage doc 存在）** → ✅ 主流场景，继续 Step 2。

- **已有 `_archive/v<N>/` 子目录** → 读 `_archive/v<N>/REDEBATE-MANIFEST.md` 确认上次时间。
  - 若上次 redebate < 7 天前：AskUserQuestion friction 提醒：
    ```
    Q: 上次 L2 redebate 距今仅 X 天（v<N>）。频繁 redebate 通常意味着方向不稳定。
       建议先用 /explore-inject 加约束让下一轮调整，而不是再 redebate。继续？
       [y] 继续 redebate
       [n] 取消，改用 /explore-inject
    ```
  - 若 [n] 退出。

- **检测到 stale `.redebate-active`**（文件 mtime > 24h 前）→ AskUserQuestion 三选：
  ```
  Q: 发现未完成的 redebate session（开始于 <mtime>，next_v=<从文件解析>）。请选：
     [a] 继续上次未完成的 redebate
         → 用 .redebate-active 里记录的 next_v 接着跑（**不重新算版本号**），
           不再归档（已归档过），不再追加 trigger note（除非检测到没有），
           直接进入 Step 5/6 写新 R1（覆盖式）
     [b] 回滚到 v<max(_archive)>
         → cp _archive/v<max>/* L2/，rm .redebate-active，
           从 moderator-notes.md 末尾移除最近一条 Redebate-trigger 块
     [c] 强制完成 — Stage 1 暂未实现自动化收尾
         → 请手工：
           (1) 检查 L2/L2R1-*.md L2/L2R2-*.md 是否完整（双侧 R1+R2 共 4 文件）
           (2) 若完整：rm L2/.redebate-active 后跑 /explore-advance <target>
           (3) 若不完整：建议改选 [b] 回滚
  ```
  Step 3.1 会根据这里的选择走不同分支（normal vs resume）。

## Step 2 — 收集 trigger reason（若未通过 --reason 传入）

若 Step 0 已拿到 `reason`，跳过此步。否则用 AskUserQuestion 三连：

```
Q1: 为什么要 redebate L2？（free text，必答）
    可选模板（任选其一/组合）：
    - 上游变化：新研究/新产品/新事实出现
    - 下游反馈：L3/L4 跑出来发现 L2 假设错了
    - 时间漂移：距上次 advance >= 90 天 / 行业变化
    - 自我修正：re-read 觉得 R2 太弱

Q2: 是否允许模型先做 since-window search？
    [a] yes（默认） — 上次 stage doc date → 今天，搜本层允许的搜索类型
    [b] no — 纯思考，不搜索（敏感/离线场景，或操作员已自己做完调研）
```

把 Q2 的回答存为 `no_search`。

## Step 3 — atomic 归档旧产物到 `_archive/v<prev>/`

### 3.0 路径分叉：normal vs resume

根据 Step 1.2 的状态分支：

- **resume 路径**（stale 分支选 [a]）：从 `.redebate-active` 复用版本号，**跳过** 3.1/3.2/3.3/3.4
  ```bash
  # 读 .redebate-active 第一个字段（格式: <next_v>|<start_iso>|<reason>）
  IFS='|' read -r next_v start_iso prev_reason < discussion/.../<target>/L2/.redebate-active
  prev_num=$(($(echo $next_v | tr -d v) - 1))
  prev_v=v${prev_num}

  # 校验 _archive/v<prev>/ 必须存在（否则状态损坏）
  if [ ! -d discussion/.../<target>/L2/_archive/${prev_v} ]; then
    STOP "状态损坏：.redebate-active 指向 ${next_v}，但 _archive/${prev_v}/ 不存在。
          建议手工删除 .redebate-active 后重新 redebate。"
  fi

  # 校验 moderator-notes.md 末尾是否已有匹配 next_v 的 Redebate-trigger 块
  # 若有 → Step 4 跳过；若无 → Step 4 正常 append（极少见，通常意味着第一次启动写 trigger 前就中断）
  ```
  跳到 Step 4（trigger note，可能已存在则跳过）→ 进 Step 5/6 写新 R1（覆盖式）。

- **normal 路径**（已 advance + 首次启动 redebate）：执行下面 3.1-3.4 全套。

### 3.1 计算 prev/next 版本号（仅 normal 路径）

**不变量**：
- `prev_v` = "L2/ 当前活跃版本号"（即将被归档替换的版本）
- `next_v` = "本次 redebate 即将产出的版本"
- 已 advance 状态下，活跃版本 = max(_archive) + 1（因为活跃版本本身从未进过 archive）
- 因此：`prev_v = v(max(_archive_v_num) + 1)`；首次 redebate 无 archive，prev=v1

```bash
# detected_max = _archive 中已归档的最高版本号（可能为空字符串）
detected_max=$(ls discussion/.../<target>/L2/_archive/ 2>/dev/null \
  | grep -oE '^v[0-9]+$' \
  | sort -V \
  | tail -1 \
  | tr -d v)
archived_max=${detected_max:-0}        # 没有 archive 时为 0
prev_num=$((archived_max + 1))         # L2/ 里的活跃版本（即将被替换）
prev_v=v${prev_num}
next_num=$((prev_num + 1))
next_v=v${next_num}
```

示例：
- 首次 redebate：archive 为空 → archived_max=0 → prev_v=v1, next_v=v2 ✓
- 第 2 次：_archive/v1/ 存在 → archived_max=1 → prev_v=v2, next_v=v3 ✓
- 第 3 次：_archive/v1/, v2/ 存在 → archived_max=2 → prev_v=v3, next_v=v4 ✓

### 3.2 atomic 归档（先 cp 后 mv，避免中断破坏）

```bash
ARCHIVE_DIR=discussion/.../<target>/L2/_archive/${prev_v}
mkdir -p "$ARCHIVE_DIR"

# 拷贝（不删原文件，保留供 re-run 时被同名覆盖）
cp discussion/.../<target>/L2/L2R1-Opus47Max.md   "$ARCHIVE_DIR/" 2>/dev/null
cp discussion/.../<target>/L2/L2R1-GPT55xHigh.md  "$ARCHIVE_DIR/" 2>/dev/null
cp discussion/.../<target>/L2/L2R2-Opus47Max.md   "$ARCHIVE_DIR/" 2>/dev/null
cp discussion/.../<target>/L2/L2R2-GPT55xHigh.md  "$ARCHIVE_DIR/" 2>/dev/null
cp discussion/.../<target>/L2/stage-L2-explore-<target>.md "$ARCHIVE_DIR/" 2>/dev/null
```

### 3.3 写 REDEBATE-MANIFEST.md（归档元数据）

`$ARCHIVE_DIR/REDEBATE-MANIFEST.md`：

```markdown
# Redebate manifest · L2 · <target> · ${prev_v} → ${next_v}

**Archived at**: <ISO>
**Replaced by**: redebate ${next_v} (in progress)
**Trigger reason**: <reason 原文>
**Time-window scanned**: <prev stage doc 顶部 Generated 字段或文件 mtime> → <today>
**Mode**: in-place
**Triggered by**: /explore-redebate <target>

## Files in this archive

- L2R1-Opus47Max.md
- L2R1-GPT55xHigh.md
- L2R2-Opus47Max.md
- L2R2-GPT55xHigh.md
- stage-L2-explore-<target>.md

## How to revert

If you want to roll back ${next_v} and restore this version as current:
1. Delete the post-redebate files in the parent dir
2. `cp` files from this archive back to the parent dir
3. Manually remove the redebate-trigger note from moderator-notes.md
4. Or use the [4] Revert option in the explore-advance menu
```

### 3.4 触发 `.redebate-active` 信号文件

```bash
echo "${next_v}|<ISO>|<reason 单行 escaped>" > discussion/.../<target>/L2/.redebate-active
```

格式：`<next_v>|<start_iso>|<reason>`，单行。被 `/explore-next` 和 `/explore-advance` 检测。

## Step 4 — 写 redebate-trigger moderator note

**Resume 路径**：先用 grep 检测 moderator-notes.md 是否已有匹配 `${next_v}` 的
Redebate-trigger 块（搜索模板：`type=Redebate-trigger.*new round, ${next_v}`）。
若已存在 → **跳过**本步，直接进 Step 5。仅在 grep 未命中时才 append（极少见，
意味着之前的启动在写 trigger 之前就中断了）。

**Normal 路径**：直接 append 到 `discussion/.../<target>/L2/moderator-notes.md`（若不存在则 touch）：

```markdown

## Injection @ <ISO> · type=Redebate-trigger
**Type**: Hard constraint
**Binding on**: Both
**Applies to**: redebate L2 R1+R2 (new round, ${next_v})
**Mode**: in-place
**Trigger reason**: <reason 原文，多行 OK>
**Since-last-debate window**: <prev stage doc date> → <today>
**Archived previous version**: _archive/${prev_v}/

### Required response
新一轮 R1（双方）必须在 §0 增加一节 "Redebate response"，包含：
1. trigger reason 是否改变了你对这个 idea 的先前 framing？为什么？
2. (若允许 search) 哪些新公开数据点支持或反驳触发原因？
3. 上一版 stage doc（_archive/${prev_v}/stage-L2-explore-<target>.md）哪一部分你
   现在认为应该被修订？

注：本 redebate 是 in-place 模式 — 旧 R1/R2 已归档到 _archive/${prev_v}/，
新 R1/R2 将以同名文件落在 L2/ 下，覆盖式产出。
```

## Step 5 — Since-window search 规则（Opus 内化，不动手）

> 重要：此步**不**实际跑搜索 —— 而是把"允许的搜索范围"作为 Step 6 写新 R1 时的硬约束。

**L2 redebate 允许的搜索类型**（与 explore-next 一致 + 加时间窗）：

允许：
- prior art（同/邻域产品、项目）— 限定时间窗 `<prev stage doc date>` 之后
- demand signals（reddit / HN / 调研 / 抱怨）— 同窗
- failure cases（post-mortem / 关停 / pivot）— 同窗

**禁止**（这些是 L3/L4 的搜索类型，redebate 不破坏层级纪律）：
- tech stack 查询
- 架构决策
- 成本 / 定价模型
- 实施难度

若 `no_search=true`，新 R1 的 §0 写 "Time-window scan: SKIPPED per operator
request. All claims rest on prior knowledge + trigger reason."

## Step 6 — 写新一轮 Opus 的 L2R1（覆盖旧文件）

**HARD CONSTRAINTS**:
1. 这是 redebate 的新一轮 R1，旧 R1 已在 `_archive/${prev_v}/`，本次产出落到
   `discussion/.../<target>/L2/L2R1-Opus47Max.md`（**覆盖旧文件**，不读旧文件）
2. **可读** `_archive/${prev_v}/stage-L2-explore-<target>.md` 作为 baseline 参考
   （仅用来判断"哪些 framing 已变"，不抄袭其结构）
3. **不读** `_archive/${prev_v}/L2R1-GPT55xHigh.md`（保持 R1 独立）
4. 若 `no_search=false`：本轮可做 since-window search（≥3 次）
5. 若 `no_search=true`：no web search this round
6. NO tech / architecture / cost / feasibility content（L2 层级纪律）

读：
- `proposals/proposals.md` 该 idea 条目
- 若 fork：`discussion/<root>/<fork-id>/FORK-ORIGIN.md`
- `discussion/.../<target>/L2/moderator-notes.md`（含新写的 Redebate-trigger）
- `_archive/${prev_v}/stage-L2-explore-<target>.md`（baseline 参考）
- `.claude/skills/explore-protocol/SKILL.md`
- `CLAUDE.md`

写 `discussion/.../<target>/L2/L2R1-Opus47Max.md`（覆盖式），用 L2R1 模板 + redebate 增量节：

```
# L2R1 · <target> · ${next_v} (redebate)

**Round**: L2R1 (redebate ${next_v})
**Previous version**: _archive/${prev_v}/L2R1-Opus47Max.md
**Trigger**: <reason 单行 summary>

## §0 Redebate response (REQUIRED, redebate-only section)
### §0.1 Time-window scan (or "SKIPPED" if no_search=true)
| query | URL | ≤15-word quote | relevance to prior stage doc |
|...|...|...|...|

### §0.2 Has trigger reason changed my framing?
（1-2 段直接回答）

### §0.3 What part of v${prev_v} stage doc do I now believe should be revised?
（具体段落引用 + 我的修订意见）

## §1 The idea, unpacked (4-8 paragraphs — 同标准 L2R1 模板)
...
## §2 Novelty
## §3 Utility (3 concrete scenarios)
## §4 Natural extensions
## §5 Natural limits
## §6 Three honest questions
```

总长：800-1500 词（比标准 L2R1 多 §0 redebate 节）。

## Step 7 — 写 Codex inbox 任务（GPT 侧 R1 of redebate）

Compute timestamp `$(date -u +%Y%m%dT%H%M%S)`. Queue id: `QUEUE=<target>`.

```bash
mkdir -p .codex-inbox/queues/<target> .codex-outbox/queues/<target>
```

Write `.codex-inbox/queues/<target>/<TS>-<target>-L2R1-redebate-${next_v}.md`：

```markdown
# Codex Task · <target> · L2R1 redebate (${next_v})

**Queue**: <target>
**Created**: <ISO>
**Recommended model**: gpt-5.5
**Recommended reasoning_effort**: xhigh
**Estimated tokens**: ~7-13k（比标准 L2R1 多 redebate §0）
**Kickoff form**: oneshot（**不**复用 session — redebate 强调对 baseline 的新审视，需新会话避免上文偏置）

## Your role
You are GPT-5.5 xhigh, Debater B, L2R1 redebate ${next_v} on idea <target>.
This is a re-debate triggered by operator. Re-deeply unpack the idea —
its value, novelty, utility, extensions, limits — under the new trigger reason.

## HARD CONSTRAINTS
- Output file: discussion/.../<target>/L2/L2R1-GPT55xHigh.md（**覆盖旧文件**）
- 旧 R1 在 _archive/${prev_v}/，可读旧 stage-L2-explore-<target>.md 作 baseline 参考
- **不读** _archive/${prev_v}/L2R1-Opus47Max.md（独立思考）
- **不读** discussion/.../<target>/L2/L2R1-Opus47Max.md（同轮独立）
- {{IF no_search=false:}} 本轮允许做 since-window search（≥3 次，时间窗 <prev date> → today）
  允许类型：prior art / demand signals / failure cases
  禁止：tech / architecture / cost / feasibility
- {{IF no_search=true:}} NO web search — 纯思考
- NO tech/architecture/cost/feasibility content（L2 层级纪律）

## Read in order
- proposals/proposals.md（idea 条目）
- 若 fork：discussion/<root>/<fork-id>/FORK-ORIGIN.md
- discussion/.../<target>/L2/moderator-notes.md（含 Redebate-trigger 块）
- _archive/${prev_v}/stage-L2-explore-<target>.md（baseline 参考）
- .claude/skills/explore-protocol/SKILL.md
- AGENTS.md

## Write
discussion/.../<target>/L2/L2R1-GPT55xHigh.md（覆盖），结构：
- §0 Redebate response（§0.1 Time-window scan / §0.2 framing change / §0.3 stage doc revision）
- §1-§6 标准 L2R1 模板（unpacked / novelty / utility / extensions / limits / three questions）

800-1500 词。

## When done
Write .codex-outbox/queues/<target>/<TS>-<target>-L2R1-redebate-${next_v}.md 含：
- Files written + word count
- Headline: redebate 后的 sharpened reading
- 与 baseline 相比最大的 framing shift
- Top novelty + top limit (post-redebate)
```

更新 HEAD 指针：

```bash
echo "<TS>-<target>-L2R1-redebate-${next_v}.md" > .codex-inbox/queues/<target>/HEAD
```

## Step 8 — 输出 next-step menu

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔄 L2 redebate started: ${prev_v} → ${next_v} (in-place mode)

Archived: discussion/.../<target>/L2/_archive/${prev_v}/ (5 files + MANIFEST)
New R1 written: discussion/.../<target>/L2/L2R1-Opus47Max.md (<wc> words)
  · §0 Redebate response: <one-line summary>
  · §1 sharpened reading: "<one sentence>"
Trigger note: discussion/.../<target>/L2/moderator-notes.md (appended)
Active session signal: discussion/.../<target>/L2/.redebate-active

📋 Next step: Codex 侧 R1 of redebate ${next_v}.

[1] (默认) 在 Codex 终端跑：cdx-run <target>
    （会读 HEAD → 跑 redebate L2R1）

[2] 我想先看 Opus 的新 §0 redebate response
    → 我会显示 §0

[3] Show full Codex kickoff
    → cdx-peek <target>

[4] 取消 redebate — 从 _archive 恢复 ${prev_v}
    → 我会复制 _archive/${prev_v}/* 回 L2/，删除 .redebate-active
       和 moderator-notes.md 中刚加的 Redebate-trigger 块

[5] 已经跑过 Codex 侧 — 直接进 R2
    → /explore-next <target>（会识别 .redebate-active 走 redebate 路径）

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Reply 1/2/3/4/5 or describe.
```

## Notes（实施提醒）

- `<root>` 通过 target 的数字前缀 regex 提取（`^([0-9]+)`），fork-id 形如
  `003-pA` / `003-pA-r1` / `001a` 都能命中。若 target 不含数字前缀（应该不会发生），
  STOP 并提示。
- atomic 归档：所有 cp/mv 顺序为 "先 mkdir → cp → 写 MANIFEST → echo .redebate-active"，
  任何一步失败可手工从 `_archive/${prev_v}/` 恢复（MANIFEST 里有恢复指引）。
- `.redebate-active` 文件**不被 git 追踪**（Stage 1 暂不动 .gitignore；Stage 2 加）。
  实践中它在每次 redebate 周期开始/结束之间存活，不应跨 commit。
- `_archive/` 目录**应进 git**（保留历史），但 `.redebate-active` 不应。
- 若新 R1 写完后 operator 反悔，使用 [4] Revert 路径或手工：
  ```
  cp -f _archive/${prev_v}/* L2/
  rm L2/.redebate-active
  # 然后从 moderator-notes.md 删除最近那个 Redebate-trigger 块
  ```
- L1 redebate 的拒绝消息：
  > "L1 inspire layer 不支持 redebate。要重新开 L1，请 (a) `/inspire-inject <id>`
  >  + `/inspire-next <id>` 在原 L1 上重做某轮，或 (b) `/propose` 新 idea。"
