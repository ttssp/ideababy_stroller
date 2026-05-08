---
description: Cross-cutting expert-forge — two reviewers audit existing artifacts (repo / stage docs / external materials), SOTA-benchmark, converge to a single verdict + W-shaped deliverables. Stateful — re-run advances phase by phase. NOT part of L1-L4 pipeline.
argument-hint: "<idea-id-or-fork-id>  e.g. 005, 005-pA"
allowed-tools: Read, Write, Bash(mkdir:*), Bash(cp:*), Bash(echo:*), Bash(ls:*), Bash(date:*), Bash(test:*), Bash(grep:*), Bash(stat:*), Bash(find:*), Bash(cat:*), Bash(head:*), Bash(md5:*), Bash(md5sum:*), AskUserQuestion, WebSearch, WebFetch, Task, Glob, Grep
model: opus
---

# Expert Forge · stateful cross-cutting reviewer

Idea/fork **$ARGUMENTS**.

## Step 0 — locate target & detect state

### 0.1 推算 target 路径

`$ARGUMENTS` 可以是 root idea(如 `005`)或任何 fork(如 `005-pA`、`002b-stablecoin-payroll`、`004-pB`、`002g-dao-bounty`)。

**解析规则**(必须严格按这个顺序判断,允许 fork-id 任意后缀):

```bash
TARGET="$ARGUMENTS"

# Step 1: 提取 TARGET 的前导数字串作为 root candidate
#   例:002b-stablecoin-payroll → root=002
#       005 → root=005
#       005-pA → root=005
#   regex: ^([0-9]+)(.*)$  ;若整体匹配失败则报错"$ARGUMENTS 不是合法的 idea/fork id"
ROOT_NUM="<TARGET 的前导数字串>"
SUFFIX="<TARGET 减去 ROOT_NUM 后剩余>"

# Step 2: 按 SUFFIX 是否为空决定路径
if [[ -z "$SUFFIX" ]]; then
  # 纯数字 → root idea
  DISCUSSION_PATH="discussion/$TARGET"
else
  # 有后缀 → fork(后缀格式不限,可以是 -pA / b-something / g-foo / 任意)
  DISCUSSION_PATH="discussion/$ROOT_NUM/$TARGET"
fi

# Step 3: 验证目录存在
test -d "$DISCUSSION_PATH"
```

如果 `$DISCUSSION_PATH` 不存在 → **不要立即报错**,先按下面顺序判断:

1. 用 `grep -n "^## \*\*${ROOT_NUM}\*\*:" proposals/proposals.md | head -1`(其中 `${ROOT_NUM}` 是 Step 0.1 算出的前导数字串)看 proposals.md 是否有该 idea 的 entry。
2. **若 grep 命中**(`${ROOT_NUM}` 在 proposals.md 中有段落)→ 跳到 Step 0.5(它会自动 mkdir + 写 `FORGE-ORIGIN.md` + 跑 prefill)。
3. **若 grep 未命中**(proposals.md 也没这个 id)→ 才报错,提示用户:
   > "找不到 idea/fork `$ARGUMENTS`(预期路径 `<DISCUSSION_PATH>`,proposals.md 也没有 §${ROOT_NUM} 段落)。运行 `/status` 查看现有 idea/fork 列表,或先 `/propose` 创建。"

**注意**:fork-id 后缀格式由 `/fork` 命令自由决定,**不要假设固定形态**(如 `pA/pB/a/b`)— 仓库现有 fork 包括 `001-pA`、`002b-stablecoin-payroll`、`002f-payroll-er`、`002g-dao-bounty`、`003-pA`、`004-pB` 等多种命名习惯。

### 0.2 识别当前 forge version

```bash
ls -1 $DISCUSSION_PATH/forge/ 2>/dev/null | grep -E '^v[0-9]+$' | sort -V
```

- 无 `forge/` 目录或目录空 → fresh run, 起 `v1`,跳到 Step 1(Phase 0 intake)
- 有 v1...v<N>(取最新 v<N>):
  - 读 `$DISCUSSION_PATH/forge/v<N>/.forge-state.json` 的 `phase` 字段(若文件不存在,fallback 用文件存在性推断)
  - **`phase == "done"`**(stage-forge-<id>-v<N>.md 存在)→ 询问用户:[查看 v<N> 结果 / 起 v<N+1> / cancel]
  - **`phase == "aborted"`**(用户在 Step 8 选过 [C] Abort)→ **视为已结案**,自动起 v<N+1>(在 v<N+1> 目录创建 fresh state,跳到 Step 1 重做 Phase 0 intake)。可选先告知用户:"v<N> 已 aborted,自动起 v<N+1>。"
  - 其他(`phase` 是 1/2/3R1/3R2 等中间态)→ 取 v<N> 作为当前活跃 v,跳到 Step 0.3

记 `CURRENT_V=v<N>`,`FORGE_DIR=$DISCUSSION_PATH/forge/$CURRENT_V`。

### 0.3 状态检测

读 `.forge-state.json`(若不存在则用文件存在性 fallback)。按下表分支(顺序短路):

| 检测条件 | 当前状态 | 跳转 Step |
|---|---|---|
| `forge-config.md` 不存在 | Phase 0 未完成 | Step 1(intake)+ Step 2(Phase 1 Opus) |
| `P1-Opus47Max.md` 存在 ∧ outbox `<TS>-<id>-forge-v<N>-p1.md` 不存在 | Phase 1 等 Codex | Step 7(打印 cdx-run 指引,**不推进**) |
| outbox p1 含 `Verdict: BLOCK` | Codex 报错 | Step 8(error path) |
| outbox p1 齐全 ∧ `P2-Opus47Max.md` 不存在 | Phase 1→2 过渡 | Step 3(Phase 2 Opus)|
| `P2-Opus47Max.md` 存在 ∧ outbox p2 不存在 | Phase 2 等 Codex | Step 7 |
| outbox p2 含 BLOCK | Codex 报错 | Step 8 |
| outbox p2 齐全 ∧ `P3R1-Opus47Max.md` 不存在 | Phase 2→3R1 过渡 | Step 4(Phase 3R1 Opus) |
| `P3R1-Opus47Max.md` 存在 ∧ outbox p3r1 不存在 | Phase 3R1 等 Codex | Step 7 |
| outbox p3r1 含 BLOCK | Codex 报错 | Step 8 |
| outbox p3r1 齐全 ∧ `P3R2-Opus47Max.md` 不存在 | Phase 3R1→3R2 过渡 | Step 5(Phase 3R2 Opus) |
| `P3R2-Opus47Max.md` 存在 ∧ outbox p3r2 不存在 | Phase 3R2 等 Codex | Step 7 |
| outbox p3r2 含 BLOCK | Codex 报错 | Step 8 |
| outbox p3r2 齐全 ∧ `stage-forge-<id>-v<N>.md` 不存在 | Phase 4 触发 | Step 6(synthesizer) |
| stage 文档存在 | done | Step 7(打印 done 菜单) |

**幂等性**:同一状态被命令再次触发时,detect 到"Opus 该 phase 已写 + Codex 还没回",直接打印 next-step 菜单不重写文件。

**outbox BLOCK 检测**:每次过渡前 grep outbox 文件首 30 行有无 `Verdict: BLOCK`。命中则不推进 + 跳 Step 8 报错。

### 0.4 HEAD 占用检测(防覆盖他人任务)

按 `.codex-inbox/README.md` v2 协议:**queue id = `<id>` 本身**(root 时是 `NNN`,fork 时是 `<fork-id>` 如 `005-pA`/`002b-stablecoin-payroll`)— **每个 fork 用自己独立的 queue,不共享 root queue**。本检测就在 **forge 自己 queue**(`.codex-inbox/queues/<id>/HEAD`)上做,不去看其他 queue。

如果本 queue 已被 L 系列 / task-review 任务占用且未消费,forge 直接覆盖会让旧任务变成无声 orphan(cdx-run 看不见、/status 也忽略)。

**检测逻辑**(只在**写新 inbox 任务前**触发,即 Step 2 / 3 / 4 / 5 写 inbox 之前):

读 `.codex-inbox/queues/<id>/HEAD`(若存在,`<id>` = `$ARGUMENTS`),分类:

- **HEAD 不存在 / queue 目录不存在** → 无占用,正常推进
- **HEAD 内容是本 forge run 的任务**(文件名匹配 `-forge-<CURRENT_V>-p<n>.md`)
  - 对应 outbox 已存在 → 可以覆盖到下一个 forge 任务
  - 对应 outbox 不存在 → 跳 Step 7(等本 forge phase 的 Codex 回)
- **HEAD 内容是非本 forge 任务**(L 系列 / task-review / 上一次 forge v / 等)
  - 对应 outbox 已存在 → 旧任务已消费,可以覆盖
  - 对应 outbox 不存在 → **跳 Step 8 + HEAD 占用专用 menu**(见下)

**HEAD 占用专用 menu**:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠ Queue <id> 的 HEAD 当前指向另一个未完成任务:
  <current-head-filename>
  (类型推测:<L 系列 / task-review / 上一次 forge / 不明>)

如果直接推进 forge,这个任务会变成 orphan(cdx-run 看不见,/status 也忽略)。

📋 选项:

[A] 等当前任务先消费
    → 在 Codex 终端跑 cdx-run <id>
    → 完成后再回来 /expert-forge $ARGUMENTS

[B] 强制覆盖(我已经知道这个任务作废了 / 已经手工搬 outbox 了)
    → 我会写新 forge 任务,旧 HEAD 任务被视为 orphan 接受
    → 旧 inbox 文件保留在 .codex-inbox/queues/<id>/ 但不再被 cdx-run 访问

[C] Abort 当前 forge
    → 不写任务,我会在 $FORGE_DIR/.forge-state.json 标 aborted
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Reply A/B/C or describe.
```

**注**:本检测只在 forge 即将写新 inbox 任务时触发,不影响 Step 1(intake)和 Step 6(synthesizer 主进程内)。Phase 0 intake 不写 inbox,所以即使 HEAD 被占用,intake 仍可完成 — 直到要写 P1 inbox 时才检测。这是有意为之:让用户先填好 forge-config 再决定要不要让队列等。

## Step 0.5 — Bootstrap + Prefill(proposal-aware intake)

只在 fresh run(Step 0.3 检测 `forge-config.md` 不存在 → 决定走 Step 1)时执行。
若 forge-config 已存在(intake 已完成),跳过 Step 0.5 整段。

本步把 `proposals/proposals.md` 中的 `## **${ROOT_NUM}**:` 段落作为预填来源,
配合 `<DISCUSSION_PATH>/` 中已有的 L1/L2/L3 stage docs,产出 X/K/Z + Y/W
默认勾选的草稿,让用户在 AskUserQuestion 界面增删/编辑后拍板,**而不是** 让
用户从零粘贴(原 Step 1.2/1.3 流程)。

### 0.5.1 Detect proposal entry

```bash
ROOT_NUM="<前导数字串,见 Step 0.1>"

# 找 proposals.md 中该 root id 的 entry 行号
PROP_LINE=$(grep -n "^## \*\*${ROOT_NUM}\*\*:" proposals/proposals.md | head -1 | cut -d: -f1)
if [[ -n "$PROP_LINE" ]]; then
  PROP_FOUND=true
else
  PROP_FOUND=false
fi
```

两个 short-circuit 分支:

- **PROP_FOUND=false ∧ `$DISCUSSION_PATH` 不存在** → 实际已被 Step 0.1 拦下报错(grep 命中才会到这里),本分支不会触发。
- **PROP_FOUND=false ∧ `$DISCUSSION_PATH` 存在** → 跳过 0.5.2-0.5.5 整段,**直接进 Step 1**(legacy intake)。在 Step 1.2 prompt 顶部加一行警告:`(注:proposals.md §${ROOT_NUM} 未找到, 走手工 intake)`。

否则继续 0.5.2。

### 0.5.2 Auto-mkdir 若 proposal 存在但 `<DISCUSSION_PATH>` 不存在

```bash
if [[ "$PROP_FOUND" == "true" && ! -d "$DISCUSSION_PATH" ]]; then
  mkdir -p "$DISCUSSION_PATH"
  TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  # 写 FORGE-ORIGIN.md(根目录;与 fork 子目录的 FORK-ORIGIN.md 形成对称)
  # 内容见下,用 Write 工具写
fi
```

`<DISCUSSION_PATH>/FORGE-ORIGIN.md` 内容(用 Write 工具,变量替换实际值):

```markdown
# Forge origin

**This directory**: $DISCUSSION_PATH
**Bootstrapped by**: /expert-forge $ARGUMENTS @ <ISO>
**Trigger**: proposals.md §${ROOT_NUM} exists; discussion/ did not.
**Source proposal**: proposals/proposals.md (line ${PROP_LINE})
**L1/L2/L3 status at bootstrap**: never run (forge-first 启动)

## Why this file exists

This idea entered the pipeline via /expert-forge directly, not via
/inspire-start → /explore-start → /scope-start. The forge run treats
the proposal section as its primary X target. If you later run L1-L4
on this idea, those layers will populate L1/, L2/, L3/ alongside
this forge/ directory normally.

This file is informational; not read by phase-1/2/3 reviewers.
```

向用户输出一行确认:

```
ℹ proposals.md §${ROOT_NUM} 找到, $DISCUSSION_PATH 不存在 → 已自动创建并写 FORGE-ORIGIN.md。
```

### 0.5.3 Pre-create FORGE_DIR

```bash
# CURRENT_V 已在 Step 0.2 算好;fresh run 默认 v1
CURRENT_V="${CURRENT_V:-v1}"
FORGE_DIR="$DISCUSSION_PATH/forge/$CURRENT_V"
mkdir -p "$FORGE_DIR"
```

(只 mkdir。`PROTOCOL.md` 拷贝和 `forge-config.md` 写入仍由 Step 1.1 / 1.9 做。)

### 0.5.4 Task 调 forge-intake-prefill 子代理

显式 Task 调用,prompt 必须把 5 个变量的实际值传给 subagent(它在 isolated worktree,不能再算 Step 0.1):

```
Task tool:
  subagent_type: forge-intake-prefill
  description: "Prefill forge intake for $ARGUMENTS"
  prompt: """
  forge-intake-prefill 启动。

  实际 <DISCUSSION_PATH> = <Step 0.1 算出的值, e.g. discussion/005 或 discussion/005/005-pA>
  实际 <id> = $ARGUMENTS
  实际 <CURRENT_V> = v1(或 Step 0.2 算出的 v<N>)
  实际 <ROOT_NUM> = <Step 0.1 算出的前导数字串>
  proposals.md 路径 = proposals/proposals.md
  proposal entry 行号 = <PROP_LINE 实际数字, 若 PROP_FOUND=false 则填 "n/a">

  读 proposals.md §<ROOT_NUM>(从行 <PROP_LINE> 开始,到下一个 ## **NNN** 或 EOF),
  glob <DISCUSSION_PATH>/L*/stage-*.md 和 L*/L*R*-*.md,按
  .claude/agents/forge-intake-prefill.md 的 §"Extraction rules" 提取
  X/K/Z 候选 + Y/W 推荐,写 <DISCUSSION_PATH>/forge/<CURRENT_V>/_prefill-draft.md,
  返回 prefill summary string。

  详见 .claude/agents/forge-intake-prefill.md。
  """
```

子代理返回 summary string 后,主命令解析其中 `prefill_status`:

- **`fallback_to_manual`** → 跳过 0.5.5,直接进 Step 1.2 legacy(在 prompt 顶部加 `(注:proposal §${ROOT_NUM} prefill 失败 — <reason>, 走手工 intake)`)
- **`success` 或 `partial`** → 继续 0.5.5

### 0.5.5 Preview + 用户确认(三个 sub-screen)

#### 0.5.5.a Bundle quick-pick

读 `$FORGE_DIR/_prefill-draft.md` §"Starting-point quick-pick groups",仅
显示该 idea 实际存在的 stage doc 对应的 bundle:

```
AskUserQuestion(single-select):
  question: "起点选哪一档?(决定 X 的初始勾选状态;后面还可以微调)"
  multi_select: false
  options(动态生成):
    [Bundle:pure-idea]    只用 proposal §${ROOT_NUM} 的文本(忽略已存在的 L2/L3)
    [Bundle:from-L2]      proposal + L2 stage doc            (只在 L2 stage 存在时显示)
    [Bundle:from-L3]      proposal + L3 stage doc            (只在 L3 stage 存在时显示;若存在则 default 推荐)
    [Bundle:full-history] proposal + 全部 L1/L2/L3 stage     (任一 stage 存在时显示)
    [Bundle:custom]       我自己挑(下一步给完整 multi-select)
```

**Bundle 选定后**,如果选 `[Bundle:full-history]` 且子代理估算的
`estimated_tokens_full_history` ≥ 8k,主命令打印**软警告**(非阻塞):

```
⚠ Full-history bundle 预计 Phase 1 Opus 读 ~<n>k tokens(<m> 个标的)。
  Codex / Opus 不会 hard-fail,但单轮可能多次工具调用。
  如果不需要全部 context,建议改 from-L3。要继续选 full-history 吗?
  [继续 / 改 from-L3]
```

回继续就继续。回"改 from-L3"重置 bundle 选择并继续。

#### 0.5.5.b X candidate 多选确认

按选定 Bundle 的 pre-checked 列表展示完整 X 候选:

```
AskUserQuestion(multi-select):
  question: "X 候选(根据 bundle:<X> 已预勾选;按需取舍。⚠ = 路径不可达,Codex 沙箱可能 BLOCK)"
  multi_select: true
  options: <逐条列 _prefill-draft.md §"X candidates (raw)" 的所有项>
    每条前缀 ✅(reachable)/ ⚠(unreachable),后缀 [pre-checked] / [unchecked-default]
```

用户最终勾选数 = 0 → 自动 fallback 到 Step 1.2 legacy(在 prompt 顶部加来源警告)。
否则记录 `X_FINAL`。

#### 0.5.5.c K editor

打印 `_prefill-draft.md` §"K seed (suggested, editable)" 的内容,然后:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
K · 用户判准 — 自动从 proposal §${ROOT_NUM} 拼装的草稿如下:

<引用 _prefill-draft.md K seed 完整内容>

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
请操作:
  [Enter]  直接接受草稿(不修改)
  [Edit]   粘贴你修改后的完整 K(替换草稿)
  [Append] 在草稿基础上 append 新段(我会拼接)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Reply Enter / Edit + 内容 / Append + 内容。
```

(K 是长 free-text,不走 AskUserQuestion;主命令解析首单词分流。)

记录 `K_FINAL` 和 `K_PROVENANCE`(`verbatim` / `edited` / `appended`)。

### 0.5.6 Merge prefill 进 Step 1

记录"已 prefill 完成"的部分:✅ X / ✅ K。Step 1 改为:

- **Step 1.1** Setup forge dir → 仍执行(`mkdir -p $FORGE_DIR` 幂等;`cp PROTOCOL.md` 仍执行)
- **Step 1.2** X intake → **跳过**;forge-config.md §"X · 审阅标的" 直接由 X_FINAL + reachability 报告填
- **Step 1.3** K intake → **跳过**;forge-config.md §"K · 用户判准" 直接由 K_FINAL 填
- **Step 1.4** Y multi-select → 走;**默认勾选项 = prefill draft 的 Y recommendation**
- **Step 1.5** Z mode → 走;若 prefill 检测到 Z 候选(`z_candidates_present: true`),"对标指定列表" 选项后加 `(推荐 — 已自动从 proposal 抓原文,请手改为一行一项)`。**用户选"对标指定列表"时**,把 prefill 的 Z 段原文原样拼进 forge-config 的 Z 字段(在 §"指定列表" 下),让用户在确认前手改
- **Step 1.6** W multi-select → 走;**默认勾选项 = prefill draft 的 W recommendation**
- **Step 1.7** 收敛模式 → 走(无 prefill)
- **Step 1.8** 预览 → 字段后加来源标注:
  ```
  X · 标的(<n> 个)[来自 prefill — proposal §<ROOT_NUM> + bundle:<X>]:
    - ...
  K · 判准(<m> 字)[来自 prefill, <verbatim|edited|appended>]:
    "<前 100 字>..."
  Y · 视角 [用户选, prefill 推荐过 <list>]: <list>
  Z · 参照系 [用户选, prefill 检测到 Z 候选: <true|false>]: <mode>
  W · 产出 [用户选, prefill 推荐过 <list>]: <list>
  ...
  ```
- **Step 1.9** 写 forge-config.md → frontmatter 加一行 `prefill_source: proposals.md§${ROOT_NUM}`(prefill 失败 fallback 时填 `manual`);`.forge-state.json` 加一行 `"prefill_used": true|false`

### 0.5.7 Fallback 路径(汇总)

任一子步骤异常都 fall through 到 Step 1.2 legacy 流程,**不阻塞 forge 进度**:

| 触发点 | 触发条件 | 行为 |
|---|---|---|
| 0.5.1 | PROP_FOUND=false ∧ DISCUSSION_PATH 存在 | 跳过 0.5.2-0.5.5,Step 1.2 顶部加来源警告 |
| 0.5.4 | 子代理返回 `prefill_status: fallback_to_manual` | 跳过 0.5.5,Step 1.2 顶部加来源警告(含 fallback reason) |
| 0.5.5.b | 用户最终勾选数 = 0 | Step 1.2 顶部加 `(注:prefill X 候选全反勾, 走手工 intake)` |
| 0.5.5.c | 用户回 Edit / Append 但提交空内容 | Step 1.3 顶部加 `(注:prefill K 提交空, 走手工 intake)` |

fallback 时 forge-config.md frontmatter 的 `prefill_source` 字段填 `manual`,
`.forge-state.json` 的 `prefill_used` 填 `false`。

## Step 1 — Phase 0 intake(仅 fresh run)

### 1.1 Setup forge dir

```bash
# Step 0.5.3 may have already mkdir'd $FORGE_DIR; mkdir -p is idempotent
mkdir -p $FORGE_DIR
mkdir -p .codex-inbox/queues/<id> .codex-outbox/queues/<id>

# 拷贝 protocol 快照
test -f .claude/skills/forge-protocol/SKILL.md && \
  cp .claude/skills/forge-protocol/SKILL.md $FORGE_DIR/PROTOCOL.md
```

### 1.2 X · 审阅标的(free-text)

**若 Step 0.5 已成功收集 X(prefill 路径)** → 跳过本步;`X_FINAL` 的内容会
在 Step 1.9 直接写进 forge-config.md §"X"。

否则(legacy / fallback 路径)向用户输出说明 + 等待回复。如果 fallback 路径
来自 0.5.7,在 prompt 顶部多加一行警告(具体内容见 0.5.7 触发点表)。

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔨 Forge v<N> · idea $ARGUMENTS · Phase 0 intake (步骤 1/6)
<若来自 fallback,这里加来源警告行,如:
 (注:proposals.md §<ROOT_NUM> 未找到, 走手工 intake)
>

X · 审阅标的(粘贴格式不限,每行一个):
  - 本仓库子目录路径(相对或绝对)
  - 外部 repo 绝对路径(注意 Codex 沙箱可能不可读)
  - URL(双方会用 WebFetch 抓)
  - 历史 stage 文档引用(如 discussion/005/L2/stage-L2-explore-005.md)
  - 直接粘贴的文本块(标 "TEXT:" 开头,后面跟内容)

请粘贴你想让双专家审阅的所有标的,然后回复:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

收到后:
1. 解析每行,标注类型:
   - 路径存在(`test -d` 或 `test -f`)→ "本仓库子目录" / "外部 repo" / "本仓库文件" / "stage 文档"
   - URL(以 http://https:// 开头)→ "URL"
   - "TEXT:" 前缀 → "粘贴文本"
   - 解析失败 → 标 ⚠ 让用户确认
2. 对外部路径做 read-only 验证(`ls $path 2>&1`),失败的标"BLOCK risk(用户处理沙箱)"
3. 给出解析后的清单让用户确认:
   ```
   解析结果(<n> 个标的):
   - ✅ /Users/admin/codes/ideababy_stroller/ (本仓库根)
   - ⚠ /Users/admin/codes/idea_gamma2/ (外部 repo,Codex 可能 BLOCK)
   - ✅ discussion/005/L2/stage-L2-explore-005.md (stage 文档)
   - ⚠ <某项> 解析失败,可能是路径打错?

   确认无误回复 'go' 进入下一步;否则告诉我哪里要改。
   ```

### 1.3 K · 用户判准(free-text)

**若 Step 0.5.5.c 已成功收集 K** → 跳过本步;`K_FINAL` 的内容会在 Step 1.9
直接写进 forge-config.md §"K"。

否则向用户输出说明 + 等待回复:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
K · 用户判准(2/6) — 你最在乎什么?
<若来自 fallback,加来源警告行,如:
 (注:prefill K 提交空, 走手工 intake)
>

请用一段话(可多行)告诉双专家:
- 你为什么要 forge 这个标的
- 关心什么、不关心什么
- 看重什么 tradeoff
- 任何贯穿审阅过程双方应记住的 context
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

收到后直接保存,不解析。

### 1.4 Y · 审阅视角(AskUserQuestion multi-select)

```
Q: 你希望双专家从哪些视角审阅?(可多选)

  □ 产品价值 — 这玩意儿对真实用户是不是真有用?
  □ 架构设计 — 模块切分、抽象层次、可演化性
  □ 工程纪律 — 测试、CI、SDD、code review 机制
  □ 安全 — 输入验证、密钥、permission boundary
  □ 教学价值 — 是否能让用户在使用过程中学到东西
  □ 商业可行 — 是否有可持续商业模式
  □ 用户体验 — 易用性、onboarding、错误恢复

(后面有 Other 可补充自定义视角)
```

multi_select=true。**默认勾选项**:
- 若 Step 0.5 prefill 跑过(success / partial)→ 用 prefill draft §"Y default recommendation" 中标 ✅ 的项作为默认勾选,并在 question description 中附 prefill evidence 引文(如"`架构设计`:命中关键词 framework / pipeline")
- 否则 → 默认推荐前 3 项(产品价值 / 架构设计 / 工程纪律)

### 1.5 Z · 参照系(AskUserQuestion single-select)

```
Q: 双专家在 Phase 2 怎么对比参照?

  ◯ 对标 SOTA — 双方各自检索领域 SOTA(prior-art / 失败案例 / 演化路径)
  ◯ 对标指定列表 — 我会在 K 里给出对标项,双方只对标这几个
  ◯ 不对标,纯内部审阅 — 跳过 Phase 2 SOTA 搜索
```

如果选"对标指定列表",再问:

```
Q: 你想对标哪些项目?(每行一个,可空)
<若 Step 0.5 prefill 检测到 Z 候选(z_candidates_present=true)→ 在 prompt 末尾
  贴出 _prefill-draft.md §"Z candidates" 的原文段,并加提示:
  "(已自动从 proposal §<ROOT_NUM> §"我已知的相邻方案/竞品" 抓原文如下;请手改为一行一项)"
>
```

如果 prefill 检测到 Z 候选 + 用户选"对标指定列表",在 forge-config.md 的
§"Z" 中先写 prefill 的原文段(标 "[来自 prefill 原文]"),用户在 Step 1.8
预览阶段可以再调整。

### 1.6 W · 产出形态(AskUserQuestion multi-select)

```
Q: 你希望最终 stage 文档包含哪些产出形态?(可多选)

  □ verdict-only — 只要 verdict + 简短 rationale(≤500 字)
  □ decision-list — 4 列矩阵(保留/调整/删除/新增)
  □ refactor-plan — 按模块分组的改造方案
  □ next-PRD — 下一版 PRD 草案(可直接进 L4 plan-start)
  □ next-dev-plan — 下一版 dev plan(按 phase/milestone 切)
  □ free-essay — 长篇综合(800-1500 字)
```

multi_select=true。强制至少选 1 项。**默认勾选项**:
- 若 Step 0.5 prefill 跑过(success / partial)→ 用 prefill draft §"W default recommendation" 中标 ✅ 的项作为默认勾选
- 否则 → 默认 verdict-only + decision-list + next-PRD(三件套适合大多数 idea)

### 1.7 收敛强度(AskUserQuestion single-select)

```
Q: 双专家最终要怎么收敛?

  ◯ strong-converge(默认)— 必须 finalize 单一 verdict;残余分歧降级为 v0.2 note
  ◯ preserve-disagreement — 允许并存 2 个 verdict,各自独立完整
```

### 1.8 拼装预览给用户确认

每行字段后加来源标注(prefill 路径 / legacy 手工)。如果 X 或 K 来自 prefill,
显式标注 bundle 类型 + K 的 provenance(verbatim / edited / appended)。

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Phase 0 intake 收齐。预览:

X · 标的(<n> 个) [<来自 prefill — proposal §<ROOT_NUM> + bundle:<X> | 手工 intake>]:
  - <list 摘要>

Y · 视角 [用户选 <若 prefill 推荐过, 加 ", prefill 推荐过 <list>">]: <list>
Z · 参照系 [用户选 <若 prefill 检测到 Z 候选, 加 ", prefill 检测到 Z 原文段">]: <mode>
W · 产出 [用户选 <若 prefill 推荐过, 加 ", prefill 推荐过 <list>">]: <list>
K · 判准(<m> 字) [<来自 prefill, <verbatim|edited|appended> | 手工 intake>]:
  "<前 100 字...>"
收敛模式:<strong-converge | preserve-disagreement>

确认无误回复 'go';要修改告诉我哪里。
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 1.9 写 forge-config.md + state.json

确认后,计算 X 路径列表字符串的 md5 哈希。写两个文件:

**forge-config.md** 格式见 forge-protocol/SKILL.md §"forge-config.md output format"。
frontmatter 中**新增一行** `prefill_source`:
- 若 Step 0.5 走通(success / partial)→ `prefill_source: proposals.md§<ROOT_NUM>`
- 若 fallback 到 legacy intake → `prefill_source: manual`

**.forge-state.json**:
```json
{
  "version": "v<N>",
  "phase": "1",
  "convergence_mode": "strong-converge",
  "x_hash": "<md5>",
  "prefill_used": true | false,
  "created": "<ISO>",
  "last_updated": "<ISO>"
}
```

### 1.10 连跑 Phase 1 Opus

intake 完成后,**不停下来等用户**,直接进 Step 2。

## Step 2 — Phase 1 Opus side(独立审阅)

### 2.0 读前置文件(若存在)

- `$FORGE_DIR/forge-config.md`(refresh)
- `$FORGE_DIR/moderator-notes.md`(若存在,binding — 用户可能在 P1 前 inject)

### 2.1 读 X 中所有标的

按 forge-config.X 解析后的清单逐个 Read:
- 本仓库路径:Read(若是目录,先 ls 列文件,再选关键文件读)
- 外部 repo 路径:Read(若失败,记录为 "skipped due to access" 在 P1 §0)
- URL:WebFetch
- 粘贴文本:从 forge-config.md 直接读
- stage 文档:Read

读取策略(按 Y 视角):
- 视角=工程纪律 + 架构设计 → 优先看 `.claude/`、`commands/`、`skills/`、模块入口
- 视角=产品价值 → 优先看 README、stage 文档
- 视角=安全 → 优先看 auth、permission、input validation 相关代码
- 视角=用户体验 → 优先看 UI、onboarding 流程

### 2.2 写 P1-Opus47Max.md

Path: `$FORGE_DIR/P1-Opus47Max.md`

按 forge-protocol/SKILL.md §"P1 template" 结构:
- §0 我读到的标的清单 + 阅读策略 + K 摘要
- §1 现状摘要(按 Y 视角组织,每视角 1-3 段)
- §2 First-take 评分(按 Y 维度,keep/refactor/cut/new + 理由)
- §3 我现在最不确定的 3 件事

**HARD CONSTRAINTS**:
- NO web search this phase
- 不允许跨入 SOTA 对比
- 不允许写 PRD / dev plan / refactor 详细方案
- §0 必须引用 K
- 800-1500 字

### 2.3 写 Codex P1 inbox 任务

```bash
TS=$(date -u +%Y%m%dT%H%M%S)
INBOX_FILE=".codex-inbox/queues/<id>/${TS}-<id>-forge-${CURRENT_V}-p1.md"
```

写 inbox 文件,按 forge-protocol/SKILL.md §"P1 inbox(oneshot)" 模板。
**Kickoff form: oneshot**(P1 是首轮,无前序上下文)。

任务文件中 § "X 标的清单" 必须把 forge-config 解析后的清单逐条列出(让 Codex 不需要去解析),每条标:
- 路径或 URL
- 类型
- 推荐读取范围(目录列文件 / 整文件读 / WebFetch / 直读 stage)

### 2.4 更新 HEAD

```bash
echo "${TS}-<id>-forge-${CURRENT_V}-p1.md" > .codex-inbox/queues/<id>/HEAD
```

### 2.5 更新 state.json

```json
{ "phase": "1", "opus_done": true, "codex_done": false, ... }
```

### 2.6 跳 Step 7(打印 cdx-run 指引)

## Step 3 — Phase 2 Opus side(参照系评估)

### 3.1 前置

确认 outbox p1 齐全且非 BLOCK(Step 0 已检测,这里是过渡触发)。

### 3.2 读对方 P1 + 自己 P1 + moderator-notes

读:
- `$FORGE_DIR/P1-GPT55xHigh.md`(对方,新读)
- `$FORGE_DIR/P1-Opus47Max.md`(自己,refresh)
- `$FORGE_DIR/forge-config.md`(refresh)
- `$FORGE_DIR/moderator-notes.md`(若存在,binding)

### 3.3 按 Z 跑搜索

按 forge-config.Z:
- mode=对标 SOTA: 跑 ≥3 SOTA 检索(prior-art / failure cases / 演化路径)
  - allowed: 领域内已有产品 / 学术研究 / 失败案例
  - forbidden: tech-stack-deep-dive / pricing / 实施细节
- mode=对标指定列表: 只检索 K 里给的对标项,每个至少 1 次搜索
- mode=不对标: 不跑 web search

### 3.4 消化外部材料

如果 K 中提到外部链接 / 文件,逐项消化(Read / WebFetch)。

### 3.5 写 P2-Opus47Max.md

按 forge-protocol §"P2 template":
- §1 SOTA 对标(表格)
- §2 用户外部材料消化
- §3 修正后的视角(P1 哪些站住、哪些被推翻)

600-1100 字。

### 3.6 写 Codex P2 inbox(reuse-session)

模板见 forge-protocol §"P2 inbox(reuse-session)"。
**Kickoff form: reuse-session**。

Session hint 块列出:
- 已读(本轮请勿重读):forge-config / 自己的 P1 / X 中所有标的 / forge-protocol P1 部分
- 本轮新读:对方 P1 / forge-protocol P2 部分 / moderator-notes / 外部材料

### 3.7 更新 HEAD + state.json

```bash
echo "${TS}-<id>-forge-${CURRENT_V}-p2.md" > .codex-inbox/queues/<id>/HEAD
```

state.json: `{ "phase": "2", "opus_done": true, ... }`

### 3.8 跳 Step 7

## Step 4 — Phase 3R1 Opus side(联合收敛 R1)

### 4.1 前置

outbox p2 齐全且非 BLOCK。

### 4.2 读双方 P1+P2

- `$FORGE_DIR/P2-GPT55xHigh.md`(对方,新读)
- 双方 P1+P2(refresh)
- moderator-notes(若有更新)

### 4.3 写 P3R1-Opus47Max.md

按 forge-protocol §"P3R1 template":
- §1 整合摘要
- §2 我的初步 verdict(单段 3-5 行,直接给立场不要 hedge)
- §3 关键分歧清单(每条:我的立场 / 对方立场+引用句 / R2 期望收敛方向)
- §4 与 K 的对齐性自检(逐条 ✅/⚠/❌)

**HARD CONSTRAINTS**:
- NO new search this round(避免 R1 又开搜索发散)
- 必须列 ≥1 关键分歧(若真无,§3 写"§3 无 — 双方对齐,R2 重点在草案")
- 必须给初步 verdict 草案
- 引用对方原句 ≤15 words

600-1000 字。

### 4.4 写 Codex P3R1 inbox(reuse-session)

```bash
TS=$(date -u +%Y%m%dT%H%M%S)
INBOX_FILE=".codex-inbox/queues/<id>/${TS}-<id>-forge-${CURRENT_V}-p3r1.md"
```

模板见 forge-protocol §"P3R1 inbox(reuse-session)"。

### 4.5 更新 HEAD + state.json

```bash
echo "${TS}-<id>-forge-${CURRENT_V}-p3r1.md" > .codex-inbox/queues/<id>/HEAD
```

state.json: `{ "phase": "3R1", "opus_done": true, "codex_done": false, ... }`

**HEAD 一致性合同**:HEAD 内容 = inbox 文件名 = outbox 文件名(三者必须完全一致),
否则 cdx-queues 永远 pending。沿用 explore-protocol 已踩过的坑。

### 4.6 跳 Step 7

## Step 5 — Phase 3R2 Opus side(finalize)

### 5.1 前置

outbox p3r1 齐全且非 BLOCK。

### 5.2 读对方 P3R1 + refresh

- `$FORGE_DIR/P3R1-GPT55xHigh.md`(对方,新读)
- 自己 P3R1 refresh
- moderator-notes(若有更新)
- forge-config.md 的 convergence_mode

### 5.3 按 convergence_mode 写 P3R2-Opus47Max.md

按 forge-protocol §"P3R2 template" 的对应分支:

**strong-converge**:
- §1 我对每条分歧的最终立场 + 让步
- §2 联合 verdict(单一,200-400 字;若仍冲突,显式标 unresolved)
- §3 残余分歧降级为 v0.2 note
- §4 W 形态产出的初步草稿建议(逐项对应 forge-config.W)

**preserve-disagreement**:
- §1 已收敛点
- §2 仍并存的分歧(允许 2 个 verdict,各自独立完整)
- §3 给 synthesizer 的"何时选哪条 path"指导

700-1200 字。

### 5.4 写 Codex P3R2 inbox(reuse-session)

```bash
TS=$(date -u +%Y%m%dT%H%M%S)
INBOX_FILE=".codex-inbox/queues/<id>/${TS}-<id>-forge-${CURRENT_V}-p3r2.md"
```

模板见 forge-protocol §"P3R2 inbox(reuse-session)"。任务文件必须明确传 convergence_mode(从 forge-config 的 frontmatter 读)。

### 5.5 更新 HEAD + state.json

```bash
echo "${TS}-<id>-forge-${CURRENT_V}-p3r2.md" > .codex-inbox/queues/<id>/HEAD
```

state.json: `{ "phase": "3R2", "opus_done": true, "codex_done": false, ... }`

### 5.6 跳 Step 7

## Step 6 — Phase 4 synthesize

### 6.1 前置 quality bars(forge-protocol §"Convergence quality bars")

逐条 check:
- forge-config.md 完整(4+1 变量都填了)
- 8 个 round file 齐全
- 双方 P3R2 没有 BLOCK
- strong-converge 模式:双方 verdict 已对齐(或显式标 unresolved)
- preserve-disagreement 模式:双方 P3R2 都按要求列了 paths
- K 在双方 P3R2 中至少被引用 1 次(grep K 的关键词)

任意 fail → 跳 Step 8(error path),给修复选项。

### 6.2 主进程 Task 调 forge-synthesizer

prompt 必须把 `<DISCUSSION_PATH>` 的实际值显式传给 subagent(subagent 在 isolated worktree 不能再算 Step 0.1):

```
Task tool:
  subagent_type: forge-synthesizer
  description: "Synthesize forge v<N> for <id>"
  prompt: """
  forge-synthesizer 启动。

  实际 <DISCUSSION_PATH> = <Step 0.1 算出的值, e.g. discussion/005 或 discussion/005/005-pA>
  实际 <id> = $ARGUMENTS
  实际 <CURRENT_V> = v<N>

  读 <DISCUSSION_PATH>/forge/<CURRENT_V>/forge-config.md 和全部 8 个 round file,
  产出 <DISCUSSION_PATH>/forge/<CURRENT_V>/stage-forge-<id>-<CURRENT_V>.md。

  详见 .claude/agents/forge-synthesizer.md。
  """
```

(synthesizer 是 read/write isolated worktree;用 Task 工具直接调,不走 Codex queue)

### 6.3 等 synthesizer 返回

synthesizer 会返回:
- Output file path
- Convergence outcome
- Verdict 关键句
- W 形态实际产出
- 文档总字数
- Quality check 结果

### 6.4 更新 state.json → done

```json
{ "phase": "done", "stage_doc": "stage-forge-<id>-v<N>.md", ... }
```

### 6.5 跳 Step 7(done 菜单)

## Step 7 — print next-step menu

按当前 phase 打印对应菜单:

### 7.1 Phase 0 完成 + Phase 1 Opus done(等 Codex P1)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Phase 0 intake captured. Phase 1 Opus side done.

Forge v<N> · idea <id>
File: $FORGE_DIR/P1-Opus47Max.md (<word-count> words)

X · <n> 标的;Y · <list>;Z · <mode>;W · <list>
K(摘要):"<前 80 字>..."
收敛模式:<mode>

📋 Next step:run Codex P1.

[1] (默认) 新开 Codex 终端跑 (oneshot)
    → in your Codex terminal:  cdx-run <id>

[2] Show Codex kickoff for manual paste
    → cdx-peek <id>

[3] Show me Opus's P1 first
    → I'll display the file

[4] Inject moderator note before Codex
    → /forge-inject <id>

[5] Abort current v
    → I'll archive v<N> and you can start fresh
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Reply 1/2/3/4/5 or describe.
```

### 7.2 Phase X 等 Codex(X = 1/2/3R1/3R2)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⏳ Forge v<N> · idea <id> · Phase <X> 等 Codex 返回

Opus 已写:$FORGE_DIR/<P-file>.md (<word-count> words)
HEAD: ${TS}-<id>-forge-<v>-p<x>.md

📋 Next step:

[1] (默认) <oneshot 或 reuse-session 提示,按 phase 不同>
    → cdx-run <id>(oneshot)
    或 → 见 cdx-peek <id> 输出后粘贴(reuse-session,省 ~60% token)

[2] Show me Opus's <P-file> first

[3] Inject moderator note(用于下一 phase)
    → /forge-inject <id>

[4] Abort current v
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Reply 1/2/3/4 or describe.
```

### 7.3 Phase X→X+1 过渡 done(Opus 跑完下一 phase)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Phase <X> 双方齐全 → Phase <X+1> Opus side done.

[摘要 outbox 关键信息 + 本轮 Opus 产物关键信息]

📋 Next step:run Codex P<X+1>.

[1] (默认) reuse-session 粘贴(省 token)/ oneshot 新开
    → ...

[同上其他选项]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 7.4 Phase 4 done(stage 文档已生成)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Forge v<N> · idea <id> · 完成!

stage 文档:$FORGE_DIR/stage-forge-<id>-<v>.md (<word-count> words)
Convergence outcome: <converged | preserved-2-paths | unresolved>
Verdict 关键句:"<一句话>"
W 形态实际产出:<list>

Quality check:<all pass | <n> warning>

📋 Next step:

[1] 看完 stage 文档,选 Decision menu 中的一项 [A/B/C/P/Z]
    → I'll show the stage doc first

[2] 起 forge v<N+1>(说明需要补什么)
    → /expert-forge <id>

[3] 进 L4 — 需要先把 next-PRD draft fork 出 PRD branch
    ⚠ /plan-start 不能直接吃 forge stage 文档,它要求 <prd-fork-id> + 完整 PRD 目录
    ⚠ 现有仓库 PRD 都是**平铺布局** — discussion/<root>/<prd-fork-id>/PRD.md
       (无嵌套,如 discussion/001/001-pA/PRD.md、discussion/003/003-pA/PRD.md)
    流程:
      a. 选一个 prd-fork-id(命名建议:
         - 若 <id> 是 root(如 005)→ <id>-pForge 或 <id>-forgeV<N>(如 005-pForge)
         - 若 <id> 已是 fork(如 005-pA)→ <id>-pForge 或派生名(如 005-pA-pForge)
         无论哪种,prd-fork-id 都直接放在 discussion/<root>/ 下)
      b. 创建 discussion/<root>/<prd-fork-id>/PRD.md
         - 把 stage 文档中的 §"Next-version PRD draft" 章节抽出来
         - 补 frontmatter:**PRD-form**: simple, **Source**: forge stage-forge-<id>-v<N>.md
      c. 创建 discussion/<root>/<prd-fork-id>/FORK-ORIGIN.md
         (说明 forked-from = forge stage,parent = <id>,而非 L3 candidate)
      d. /plan-start <prd-fork-id>
    ⚠ 注意:`/fork` 命令目前的 from-* 来源是 L1/L2/L3 stage 文档,**还没支持
    from-forge** — 上面 a-c 步暂时需要手工创建。MVP 后会考虑加 /fork-from-forge。

[4] Park
    → /park <id>

[5] Abandon
    → /abandon <id>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Reply 1/2/3/4/5 or describe.
```

## Step 8 — error path

任何 BLOCK / state 矛盾 / quality bar fail → 打印诊断 + 给三选一:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠ Forge v<N> · idea <id> · 遇到问题

错误类型:<BLOCK | state-conflict | quality-fail>
诊断:<具体描述,引用 outbox 报错 / state 文件 / 缺失文件>

📋 修复选项:

[A] 调整 X(剔除读不到的标的)→ 起 v<N+1> 重跑
    → /expert-forge <id>(Phase 0 时调整 X)

[B] 调整 Codex 沙箱 scope 后 cdx-run 重试当前 phase
    → 调整完毕回 [B] 我重新检测状态

[C] Abort 当前 v
    → 我会把 $FORGE_DIR/.forge-state.json 的 phase 标记为 "aborted"
    → 旧 v 整目录保留(便于事后查看)
    → 下次 /expert-forge $ARGUMENTS 会被 Step 0.2 检测到 aborted,
      **自动起 v<N+1>**(fresh Phase 0 intake)
    → 旧 HEAD 任务也建议手工 cdx-run 消费掉或忽略(orphan),否则下次 Step 0.4
      会触发 HEAD 占用警告
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Reply A/B/C or describe.
```

## Notes for the Opus orchestrator

### forge 是横切层

forge 不进 L1-L4 pipeline。HEAD 在 forge 期间被占用,用户必须把当前 phase
的 cdx-run 跑完才能切回 L 系列任务。如果 HEAD 已被 L 任务占用,Step 0 应该
警告 + 让用户决定。

### Reviewer stance,不是 daydreamer

Opus 在 P1/P2 任何时候都不能凭空想象 X 标的"如果有 Y 就好了"。所有评价
必须基于 X 的具体内容。如果 X 中标的不可读(BLOCK / 跳过),P1 §0 必须显式
说明,不能假装读了。

### 对 K 的尊重

K 是审阅人姿态的"指南针"。每个 phase Opus 都要 refresh forge-config 拿
到完整 K,确保所有产物对齐 K 的关切。P3R1 §4(与 K 的对齐性自检)是关键
quality bar — 不能跳过。

### Quality 优先于速度

如果 8 个 round file 中任何一份产物质量不达模板要求(章节缺失 / 字数过
短 / 无 evidence),Step 6 的 quality bars 会 fail,跳 Step 8。这时不要
prompt synthesizer 强行产出,而是建议用户跑 v<N+1>。

### Forge 与 forge-inject 的协作

`/forge-inject <id>` 在任意 phase 间(P1→P2,P2→P3R1,P3R1→P3R2)允许
用户注入 moderator note,写到 `$FORGE_DIR/moderator-notes.md`。下一 phase
的 inbox 任务和 Opus prompt 必须读这份文件并响应。

注入后,Opus 不会自动重跑当前 phase — 用户在 next-step 菜单选 inject 后,
仍然需要回来再跑 `/expert-forge <id>` 才推进。
