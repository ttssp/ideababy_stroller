---
description: Fork an L3 candidate into a v1-direct PRD (skip v0.1, ship v1 directly). Requires skip-rationale ≥100 chars + must explicitly cite C1/C2/C3 from synthesizer evaluation. Use only when assumptions are externally validated.
argument-hint: "<source-id> from-L3 <candidate-spec> as <new-id>  e.g. 003 from-L3 candidate-A as 003-pV1"
allowed-tools: Read, Write, Bash(mkdir:*), Bash(cp:*), Bash(ls:*), Bash(date:*), Bash(grep:*), Bash(wc:*), AskUserQuestion, Glob, Grep
model: sonnet
---

# /fork-v1 · 单 candidate 直奔 v1

> 本命令是 v1-direct 形态的 fork — 跳过 v0.1,直接做 v1。**需要严格的合理性证明**(skip-rationale)。
> 共享 /fork.md 的 Step 1-3(定位源/找候选/确认)和 Step 5-6(更新 fork log/输出菜单)。

Parse `$ARGUMENTS` as: `<source-id> from-L3 <candidate-spec> as <new-id>`

## Step 1 — locate source stage doc (shared with /fork)

按 /fork.md Step 1 同规则。**强制 from-L3**。

## Step 2 — find the candidate (shared with /fork)

按 /fork.md Step 2 同规则。

## Step 3 — confirm with human (shared with /fork,扩展)

显示同样的 confirmation 块,**额外**展示 stage doc §"Candidate relationships" §4 的 C1/C2/C3 评估结果:

```
About to fork (v1-direct):
  Source:    <path>
  Candidate: #<X> "<title>"
  New id:    <new-id>
  Path:      discussion/<root>/.../<new-id>/

Synthesizer's skip-v0.1 evaluation (from §"Candidate relationships" §4):
  C1 假设已外部验证:    ✅/❌  <evidence>
  C2 v0.1 无独立价值:   ✅/❌  <evidence>
  C3 多 candidate 互补: ✅/❌  <evidence>
  → 合理性:<推荐 / 可考虑 / 反对>

Proceed? [y/N]
```

如果 synthesizer 评估 0 条 ✅,confirmation 块 **额外加红色警告**:"Synthesizer 认为不应跳过 v0.1。继续意味着你比 synthesizer 有更多信息 — 请慎重。"

## Step 3.5 — interactive: collect skip-rationale (NEW, 强制校验)

用 AskUserQuestion 询问 operator:

**Question**: 详细说明为什么跳过 v0.1(必须 ≥100 字,必须显式提及 C1、C2、或 C3 中至少 1 条)?

operator 输入后,**做 2 个机器校验**:

```bash
# 校验 1: 长度
chars=$(echo -n "$rationale" | wc -m)
if [ "$chars" -lt 100 ]; then
  echo "❌ skip-rationale 长度 $chars 字 < 100 字。v1-direct 需要详细论证,请重新输入。"
  exit 1
fi

# 校验 2: 必须含 C1 / C2 / C3 之一(精确匹配,允许中英文上下文)
if ! echo "$rationale" | grep -qE 'C1|C2|C3'; then
  echo "❌ skip-rationale 未显式提及 C1/C2/C3 任一条件。"
  echo "   C1 = 假设已外部验证 / C2 = v0.1 无独立价值 / C3 = 多 candidate 互补"
  echo "   请在 rationale 中明确指出你依据哪一条。"
  exit 1
fi
```

任一校验失败,要求 operator 重新输入(不退出命令)。最多 3 次后给出 escape hatch:"如果你确实无法满足校验,建议用 /fork-phased 改 phased 形态作妥协。"

## Step 4 — perform the fork (v1-direct PRD generation)

### 4a. mkdir + write FORK-ORIGIN.md (shared,扩展)

建目录。FORK-ORIGIN.md 在 `Selected candidate` 节后追加:

```markdown
**PRD-form**: v1-direct
**Skip-rationale** (operator-supplied, validated ≥100 chars + cites C1/C2/C3):
<rationale prose>
```

### 4b. write PRD.md using PRD-v1-direct template

读 `.claude/skills/sdd-workflow/templates/PRD-v1-direct.md` 作为骨架。**关键替换**:

- frontmatter `**PRD-form**: v1-direct`
- frontmatter `**Skip-rationale**: |<rationale>` (operator 输入抄进来)
- `## Scope IN (v1)` 内容来自 candidate §"Scope IN" + candidate §"Natural extensions"(把 candidate 的 v0.1 scope 和延伸合并为 v1 scope)
- `## Scope OUT` 来自 candidate §"Scope OUT"
- `## Success — observable outcomes (v1)` 来自 candidate §"Success looks like"
- `## Risk: skip-v0.1` 必填,2-3 段:
  - **假设 A**: 从 skip-rationale 提取核心假设
  - **如果错了的征兆**: 列 1-2 个 metric/用户行为信号
  - **fallback 时间窗口**: operator 在 Step 3.5 没显式说,默认填 `<待 operator 在 plan-start 前补充>`
  - **fallback 路径**: `<待补充>` 占位

写入 `discussion/.../<new-id>/PRD.md`。

## Step 5 — update source stage doc Fork log (shared)

```markdown
## Fork log
- <ISO> · candidate #<X> forked as `<new-id>` (PRD-form: v1-direct, skip-rationale validated)
```

## Step 6 — output next-step menu

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Forked (v1-direct): <new-id> created at discussion/.../<new-id>/

PRD-form:        v1-direct
Skip-rationale:  ✓ validated (≥100 chars, cites C<X>)
Scope:           直奔 v1, 无 v0.1 兜底

⚠ 你已经放弃"早期反馈"这层兜底。请确保 PRD §"Risk: skip-v0.1" 的 fallback 路径足够具体。

📋 Next steps:

[1] Start L4 for <new-id> (recommended only after补充 fallback path)
    → /plan-start <new-id>
       (spec-writer will read PRD-form=v1-direct, SLA.md 顶部加 skip-rationale,
        risks.md 必含 R-skip-v0.1 条目。)

[2] Edit PRD.md to fill fallback path before plan-start (强烈推荐)
    → manually expand discussion/.../<new-id>/PRD.md §"Risk: skip-v0.1"
       特别 fallback 时间窗口 + fallback 路径

[3] I changed my mind — re-fork as phased instead
    → /fork-phased <source> from-L3 <candidate> as <new-id>-alt
    (推荐如果你心里其实还想 v0.1 兜底)

[4] Add cross-reference to FORK-ORIGIN.md
    → tell me what to add and I'll write it

[5] Just stop
    → /status <new-id> anytime later

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Reply 1-5 or describe.
```

## Notes

- **v1-direct 何时合理**:必须满足以下至少一条(已通过 §3.5 校验):
  - **C1**: 假设已外部验证 — 同质市场 / 已有用户研究 / 已有 N 个验证赛道
  - **C2**: v0.1 无独立可发布价值 — 协议 / SDK / 平台类,半个不能用
  - **C3**: 多 candidate 互补 — 本来就是同一产品的不同器官,但本命令针对单 candidate;"多 candidate 互补"实际上更适合 /fork-composite。**所以 C3 在 /fork-v1 里很少成立**,通常是 C1 或 C2。
- **机器校验只能挡住"明显应付"**:rationale 写得严丝合缝但其实是空话,机器拦不住 — 这是 calculated risk,operator 仍是最终决策者。synthesizer §4 的 C1/C2/C3 评估提供决策依据。
- **fallback path 必须填**:本命令产物 PRD §"Risk: skip-v0.1" 的 fallback 时间窗口/路径**初始为占位**,operator 在 plan-start 前必须补全。spec-writer 在 Phase 0 检测到 v1-direct 且 fallback 仍是占位,会停下并 escalate。
- **反悔通道**:next-step menu [3] 总是给一个 /fork-phased 的退路,让 operator 容易回退。
- **不允许 from-L1 / from-L2**:v1-direct 需要 L3 candidate 的完整结构。
