---
description: Append a moderator note to a forge run's moderator-notes.md for binding steering before the next phase. Works on any forge phase transition (P1→P2, P2→P3R1, P3R1→P3R2, or before Phase 4 synthesizer).
argument-hint: "<idea-id-or-fork-id>  e.g. 005, 005-pA"
allowed-tools: Read, Write, Bash(mkdir:*), Bash(date:*), Bash(ls:*), Bash(test:*), AskUserQuestion, Glob
model: sonnet
---

# Forge · inject moderator note

Idea/fork **$ARGUMENTS**.

## Step 1 — locate active forge run

### 1.1 解析 target 路径(同 expert-forge.md Step 0.1)

`$ARGUMENTS` 可以是 root idea(如 `005`)或任何 fork(如 `005-pA`、`002b-stablecoin-payroll`)。

**解析规则**:

```bash
TARGET="$ARGUMENTS"
# regex: ^([0-9]+)(.*)$
ROOT_NUM="<前导数字串>"
SUFFIX="<剩余部分>"

if [[ -z "$SUFFIX" ]]; then
  DISCUSSION_PATH="discussion/$TARGET"
else
  DISCUSSION_PATH="discussion/$ROOT_NUM/$TARGET"
fi

test -d "$DISCUSSION_PATH"
```

如果 `$DISCUSSION_PATH` 不存在 → 停止并提示:
> "找不到 idea/fork `$ARGUMENTS`。运行 `/status $ARGUMENTS` 查看,或先 `/propose` 创建。"

**注意**:fork-id 后缀格式由 `/fork` 命令自由决定,不要假设固定形态。

### 1.2 找最新 forge v 目录

```bash
ls -1 $DISCUSSION_PATH/forge/ 2>/dev/null | grep -E '^v[0-9]+$' | sort -V | tail -1
```

若 `$DISCUSSION_PATH/forge/` 不存在或为空 → 停止并提示:
> "$ARGUMENTS 没有活跃的 forge run。先 `/expert-forge $ARGUMENTS` 启动 Phase 0 intake,或运行 `/status $ARGUMENTS` 查看现状。"

记 `FORGE_DIR=$DISCUSSION_PATH/forge/<v>`。

## Step 2 — 检测当前阶段

按 expert-forge.md Step 0.3 同样的状态检测,识别注入点:
- 当前在 Phase 0(forge-config 还没写)→ 警告"intake 还没完成,inject 没意义",建议先 `/expert-forge`
- 当前在 Phase 1 等 Codex / Phase 2 等 Codex / Phase 3R1 等 Codex / Phase 3R2 等 Codex / Phase 4 触发前 → 注入有效
- 已 done(stage 文档存在)→ 警告"v<N> 已完成,inject 无效;若想再来一轮,跑 `/expert-forge $ARGUMENTS` 起 v<N+1>"

注入点确认后,告诉用户:
> "当前 forge v<N> 处于 <phase> 阶段。注入的 moderator note 会在下一 phase Opus 写入和 Codex inbox 任务中被双方 honored。"

## Step 3 — ask human what to add

使用 AskUserQuestion(多步):

### Q1 · 注入内容(free text)

```
Q: 你要加什么 steering 到本次 forge run?(free text,多行 OK)

可选切入角度(任选其一/多):
  - 双方在审阅时应额外关注什么?
  - 有什么新约束 / 新偏好需要 binding?
  - K(用户判准)有没有补充 / 修正?
  - 有什么要补的红线 / 反对方向?
  - 想让某一边(Opus 或 GPT)特别 push back 的方向?
```

### Q2 · 绑定对象

```
Q: 这个 note 对谁 binding?
  - Both reviewers(默认)
  - Opus only
  - GPT only
```

### Q3 · 注入类型

```
Q: 是 hard constraint 还是 soft guidance?
  - Hard constraint(must honor; overrides prior)
  - Soft guidance(should consider; may argue against)
```

### Q4(可选)· 是否影响 K?

```
Q: 这个 note 是否要更新 forge-config.md 的 K(用户判准)?
  - 否(只作为下一 phase 的 moderator note,K 不变)
  - 是(同时 append 到 K,贯穿后续所有 phase)

(如果选"是"会修改 forge-config.md 并触发 X-hash 重算 — 若 X 未变,
 hash 仍稳定;若 K 长度大幅变,记录在 forge-config 的 changelog 段)
```

## Step 4 — 写 moderator-notes.md

```bash
mkdir -p $FORGE_DIR
touch $FORGE_DIR/moderator-notes.md
```

Append:

```markdown

## Injection @ <ISO>

**Type**: <Hard constraint | Soft guidance>
**Binding on**: <Both | Opus | GPT>
**Phase context**: 注入时 forge 处于 <phase> 阶段,本 note 在下一 phase 起作用
**Affects K**: <yes / no>

<human's note>

### Required response

Next phase, the binding reviewer(s) MUST address this note in a section
titled "## Moderator injection response" near the start of their phase
output (P1 §0、P2 §1、P3R1 §1、P3R2 §1 都可以加这个章节)。

If the note conflicts with prior judgments in P1/P2/P3R1, the reviewer
must explicitly call out the conflict and resolve it according to the
note's Type:
- Hard constraint → adjust prior judgment to honor the note
- Soft guidance → argue for/against and decide
```

## Step 5 — (若 Q4=yes)更新 forge-config.md K 段

读 `$FORGE_DIR/forge-config.md`,找 `## K · 用户判准` 章节,append:

```markdown

### Update @ <ISO>(via /forge-inject)

<human's note 的 K 相关部分>
```

frontmatter 不动(X 没变,hash 仍稳定)。

## Step 6 — output next-step menu

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Injection recorded at $FORGE_DIR/moderator-notes.md

注入摘要:
  Type: <Hard | Soft>
  Binding: <Both | Opus | GPT>
  当前 forge 阶段:<phase>
  下一 phase 双方都会读这份 note

📋 Next steps:

[1] (默认) 跑 /expert-forge $ARGUMENTS 推进下一 phase
    → Opus 会读 moderator-notes 并产出对应 phase 文件 + Codex inbox 任务

[2] 仅保存 note,稍后再决定何时触发下一 phase
    → 直接退出 inject

[3] 看注入后的 moderator-notes.md
    → I'll display the file
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Reply 1/2/3 or describe.
```

## Notes for the orchestrator

- inject 是 **steering 下一 phase** 的工具,不是"重写已经 round 过的内容"
- inject 不能改已生成的 Opus 文件(P1/P2/P3R1/P3R2),只在**下一 phase** 起作用
- 如果用户对当前 phase 的 Opus 产物不满意,**正确做法是 abort 当前 v 并起 v<N+1>**
  (在 /expert-forge 下次启动时会自动起 v<N+1>,Step 0.2 会处理 aborted 状态)。
  原因:重写当前 phase 涉及清理 HEAD + 备份旧 inbox + 防 outbox 错位,多状态
  耦合;abort + v<N+1> 是干净路径,所有产物在新目录隔离。
- 多次 inject 会按时间戳 append 到同一 moderator-notes.md;后续 phase
  Opus 读时会看到完整历史
- `forge-protocol/SKILL.md` 已规定每个 phase Opus prompt 必须读
  moderator-notes.md(若存在),所以 inject 后下一 phase 自动生效
