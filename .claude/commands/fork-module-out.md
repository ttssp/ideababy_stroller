---
description: Remove a module from a composite PRD. Edits the composite PRD.md to drop one module, updates Modules/Module-forms frontmatter, and writes MODULE-OUT-LOG.md. If only 1 module remains, suggests downgrading to simple PRD-form.
argument-hint: "<prd-id> <module-id>  e.g. 005-pAll clarifier"
allowed-tools: Read, Write, Edit, Bash(date:*), Bash(grep:*), AskUserQuestion, Glob
model: sonnet
---

# /fork-module-out · composite 退路

> 本命令处理 composite PRD 的 "中途砍 module" 场景。**编辑 PRD.md** 是必要的(PRD 在 discussion/ 下不受 specs-protection 约束)。

Parse `$ARGUMENTS` as: `<prd-id> <module-id>`

例: `/fork-module-out 005-pAll clarifier`(从 005-pAll composite PRD 中移除 module `clarifier`)

## Step 1 — locate composite PRD

读 `discussion/.../<prd-id>/PRD.md`,**校验**:
- frontmatter `**PRD-form**: composite` 必须存在,否则报错"`<prd-id>` 不是 composite PRD,本命令仅适用于 composite。其他形态请用 /abandon 或 /park。"
- 找到 `**Modules**: [...]` 列表,校验 `<module-id>` 在列表里,否则报错并显示当前 modules 列表。

## Step 2 — confirm with human

```
About to remove module from composite:
  PRD:                discussion/.../<prd-id>/PRD.md
  Removing module:    <module-id>
  Modules before:     [<m1>, <module-id>, <m3>]
  Modules after:      [<m1>, <m3>]
  Critical-path:      <was/still> <m?>

This will:
  - Edit PRD.md (frontmatter Modules + Module-forms 列表 / §"Modules" 子节删除 / §"Module dependency graph" 更新 / §"Critical-path module" 重评估)
  - Append MODULE-OUT-LOG.md (新建或追加)

Reason for removing? (will be saved to MODULE-OUT-LOG.md)
[ _________________________________________________ ]

Proceed? [y/N]
```

## Step 3 — branch by remaining module count

读 PRD.md 的 `**Modules**` 字段,计算移除后剩余数量。

### 3a. 剩 ≥2 个 module(继续 composite)

执行编辑:
1. PRD.md frontmatter `**Modules**: [...]` 删除目标 module
2. PRD.md frontmatter `**Module-forms**: {...}` 删除目标 module 的 entry
3. PRD.md `## Source candidates` 表格删除对应行
4. PRD.md `## Modules > ### Module: <module-id>` 整节删除
5. PRD.md `## Module dependency graph` mermaid 图删除涉及该 module 的边和节点
6. PRD.md `## Critical-path module` 重新评估(如果被移除的 module 原本是 critical-path,提示 operator "原 critical-path 已移除,请在 PRD 中重选 critical-path",但**不自动重选** — 这是产品决策)
7. 各 §Modules 子节内引用该 module 的句子标 `~~<...>~~`(strikethrough)而不是直接删,保留可追溯性

写入 MODULE-OUT-LOG.md(新建或追加)。

### 3b. 剩 1 个 module(降级为 simple)

> **前置条件**:v3 阶段 fork-composite 已锁 module-form 为 simple,所以剩余 module 必然是 simple,降级到顶层 simple 总是无损的(无 phase / skip-rationale 等额外信息可丢)。

提示 operator:
```
After removing <module-id>, only 1 module remains: <surviving-m>.
Composite-of-1 is not meaningful.

Options:
  [A] Downgrade PRD to simple form (recommended)
      具体执行步骤(见 §"3b 降级映射规则"):
      - frontmatter:PRD-form 改为 simple;删除 **Modules** / **Module-forms**;保留 **Migrated** 字段(若有)
      - §"Modules > ### Module: <surviving-m>" 子节的内容上提:
          • 子节内 Scope IN     → 顶层 ## Scope IN(替换/合并)
          • 子节内 Scope OUT    → 顶层 ## Scope OUT(替换/合并)
          • 子节内 user stories → 顶层 ## Core user stories 表(合并;保持编号连贯)
          • 子节内 module-internal outcomes → 顶层 ## Success — observable outcomes(合并)
      - 整个 ## Modules 章节删除
      - 删除 §"Source candidates" / §"Module dependency graph" / §"Critical-path module" 三个 composite-only 章节
      - 顶层 ## Core user stories 表的 Primary module 列删除(simple 没有 module 概念)
      - 顶层 ## Real-world constraints 表的 Module scope 列删除(同理)
      - 顶层 ## Success outcomes 表的 Spans modules 列删除(同理)
      - 顶层 ## Biggest product risks 删除"composite 特有风险"小节(集成复杂度/单点/scope creep)
      - 写 MODULE-OUT-LOG.md(备注 'downgraded to simple, surviving module: <surviving-m>')
  [B] Cancel — keep composite-of-2 (don't remove <module-id> after all)
  [C] Abandon entire fork instead → /abandon <prd-id>
```

operator 选 [A]:执行降级,按上述映射规则编辑 PRD。选 [B]:撤销 step 3a 计划。选 [C]:本命令退出,提示运行 /abandon。

#### 3b 降级映射规则(精确版)

**保留**:Problem / Users / Constraints / UX principles / Open questions / PRD Source(这些章节顶层就有,内容继承自 surviving module 或合并 composite 顶层)

**删除**:Source candidates / Modules / Module dependency graph / Critical-path module(composite-only 章节)

**合并提取**(从 ### Module: <surviving-m> 子节 → 顶层各对应章节):

| Module 子节字段 | 顶层目标章节 |
|---|---|
| Description | 已并入顶层 Problem,无需迁移 |
| Scope IN | `## Scope IN`(替换或合并) |
| Scope OUT | `## Scope OUT`(替换或合并) |
| User stories(若 module 内列了细化版) | `## Core user stories` 表(合并去重,保持 US 编号连贯) |
| Module-internal outcomes | `## Success — observable outcomes` 表(合并,outcome 编号连贯) |
| Module-specific UX | `## UX principles`(合并) |
| Module-specific risks | `## Biggest product risks`(合并) |

**列删除**(顶层表格):
- `## Core user stories` 表删 `Primary module` 列
- `## Real-world constraints` 表删 `Module scope` 列
- `## Success outcomes` 表删 `Spans modules` 列
- `## Biggest product risks` 章节删除"composite 特有风险"小节

**留意**:**未来如果开放 module-level phased/v1-direct**,本步骤需要扩展处理形态保留逻辑(剩余 module 是 phased 时,降级目标应是 phased 而不是 simple;同理 v1-direct → v1-direct)。当前因 v3 锁 simple,统一降级到 simple 即可。

### 3c. 剩 0 个 module(全删)

报错:"不能从 composite 中删除最后一个 module。请改用 /abandon <prd-id> 关掉整个 fork。"

## Step 4 — write MODULE-OUT-LOG.md

新建或追加到 `discussion/.../<prd-id>/MODULE-OUT-LOG.md`:

```markdown
# Module Removal Log · <prd-id>

记录从 composite PRD 中移除 module 的历史。**编辑 PRD 是受控操作**,本日志提供完全可追溯。

---

## <ISO timestamp>

**Module removed**: <module-id>
**Source candidate (when forked)**: <从原 FORK-ORIGIN.md 提取>
**Reason** (operator-provided):
<reason from Step 2>

**State change**:
- Modules before: [<m1>, <module-id>, <m3>]
- Modules after:  [<m1>, <m3>]
- Module-forms before: {...}
- Module-forms after:  {...}
- Critical-path before: <m?>
- Critical-path after:  <m?> (or `<待 operator 重选>`)
- PRD downgraded: yes (to simple) | no (still composite)

**Operator signature**: <git config user.name 输出>

---
```

## Step 5 — output next-step menu

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Module <module-id> removed from <prd-id>

PRD-form:           composite (still) | simple (downgraded)
Modules now:        [<m1>, <m3>] | (none, simple)
Critical-path:      <m?> | <待 operator 重选>
MODULE-OUT-LOG.md:  appended

📋 Next steps:

[1] Re-run /plan-start to refresh spec package (recommended if spec already exists)
    → /plan-start <prd-id>
       (spec-writer will detect PRD change, regenerate or patch spec.md / spec-<module>.md;
        existing module spec files for the removed module become orphaned — operator decides
        whether to git rm them.)

[2] If critical-path was removed, manually edit PRD §"Critical-path module" first
    → cat discussion/.../<prd-id>/PRD.md | grep -A 5 "Critical-path"

[3] Done — continue with build (if spec already up to date)
    → /status <prd-id>

[4] Reverted decision — restore module
    → 手动 git revert PRD edit + 删除最新 MODULE-OUT-LOG entry
    (本命令不提供 auto-undo,因为 PRD 编辑是产品决策,需 operator 显式确认)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Reply 1-4 or describe.
```

## Notes

- **本命令编辑 PRD.md** — 这是少数允许 LLM 改 PRD 的场景之一(operator 显式批准 + 完整可追溯)。任何其他场景改 PRD 仍需 operator 直接编辑或 /scope-* 命令。
- **编辑不是删除**:被移除 module 在 §Modules 内的内容用 strikethrough 保留,模块依赖图也只删边不删历史 — 给 operator 留 audit trail。
- **MODULE-OUT-LOG.md 必写**:即使是降级到 simple,日志也要写完整状态 diff。
- **L4 已经跑过 spec-writer 之后再 fork-out**:spec-writer 会在下次调用时检测 PRD 变化,产 spec patch(可能是 git rm 某个 spec-<module>.md + 修改 spec.md index)。具体行为由 spec-writer Phase 0 处理。
- **不可一次砍多 module**:每次只移除 1 个,要砍多个连续运行命令。这是有意为之 — 强制 operator 一次只做一个决策。
