---
doc_type: framework-xenodev-spec-writer-derivation-guide
generated: 2026-05-10
upstream: plan-rosy-naur v11 Block D + stage-forge-006-v2.md §"模块 B" step 7
purpose: 引导 operator 在 XenoDev session 派生 spec-writer / task-decomposer / parallel-builder skill,跑首 PRD 产 spec.md + tasks/
ids_reference_files:
  - .claude/agents/spec-writer.md (IDS 历史 spec-writer subagent;参考概念,不直接 cp)
  - .claude/skills/sdd-workflow/SKILL.md (IDS 6 元素 contract;XenoDev 加 PPV 第 7 = 7 元素)
  - .claude/skills/sdd-workflow/templates/PRD-base.md (IDS PRD 模板;参考)
  - specs/004-pB/spec.md (IDS ship 过的 7+1 元素 spec.md 实证;参考)
---

# XenoDev L4 Skill 派生指南(B2.2 Block D)

## 背景

per stage-forge-006-v2.md §"模块 B" step 7 + §W2:
> spec/task skill 由 **XenoDev schema 重新派生,不从 IDS port**

但概念可参考 IDS 历史范式。本文档列 reference + 派生原则 + checklist,operator 在 XenoDev session 用。

## scope OUT(本指南不做)

- ❌ 不直接给 XenoDev SKILL.md 内容(那是 XenoDev 仓内的事;operator 在 XenoDev session 自写)
- ❌ 不替 operator 决定 spec-writer subagent 是 isolation: worktree 还是 inline(operator dev workflow 偏好)
- ❌ 不 fork Spec Kit 0.8.7 整 repo(per `framework/spec-kit-evaluation.md` 推荐 adapter 模式)

## XenoDev 7 元素 spec contract(IDS 6 + PPV)

per `framework/spec-kit-evaluation.md` 维度 1:

| # | 元素 | IDS 范式 | XenoDev 加 / 改 |
|---|---|---|---|
| 1 | Outcomes | ✅ 同 IDS sdd-workflow §"1. Outcomes" | 直接派生 |
| 2 | Scope Boundaries(IN/OUT) | ✅ 同 IDS §"2. Scope Boundaries" | 直接派生 |
| 3 | Constraints | ✅ 同 IDS §"3. Constraints" | 直接派生 |
| 4 | Prior Decisions | ✅ 同 IDS §"4. Prior Decisions" | 直接派生 |
| 5 | Task Breakdown | ✅ 同 IDS §"5. Task Breakdown" | 直接派生 |
| 6 | Verification Criteria | ✅ 同 IDS §"6. Verification Criteria" | 直接派生 |
| **7** | **Production Path Verification (PPV)** | ❌ IDS 无(M3 已 archived) | **XenoDev 必加** — 防 mock-pass-prod-fail(灵感:autodev_pipe V4 stroller idea004 12 routes 404 案例) |

§7 PPV 最小要求(per IDS plan-start v2.2 历史 Step 4.5,但 v3.0 已删 — 本指南保留供 XenoDev 参考):
- 列至少 1 条 P_i 描述"真路径起点 → 终点 + 必经环节 + 可执行验证命令"
- 失败模式覆盖:不写 / 只写 mock-pass-prod-fail 样本 → XenoDev `scripts/spec_validator.py` reject + status 不能 frozen

## XenoDev L4 skill 三件套 派生原则

### 1. spec-writer(参考 `.claude/agents/spec-writer.md`)

operator 在 XenoDev session 起 `XenoDev/.claude/skills/spec-writer/SKILL.md` 时,**自决** frontmatter 是否同 IDS:

```yaml
---
name: spec-writer
description: Convert XenoDev PRD into 7-element spec contract package (per ideababy_stroller framework/SHARED-CONTRACT.md §1 + framework/spec-kit-evaluation.md adapter 模式)
inspired_by: GitHub Spec Kit 0.8.7 (concept-level only, no code copied) + IDS sdd-workflow (6 元素 + PPV 扩展)
schema_version: 0.1
tools: Read, Write, Edit, Glob, Grep
model: opus
isolation: worktree  # operator 决定:worktree vs inline
---
```

body 关键节(参考 IDS spec-writer.md):
- **Phase 0 · Detect PRD-form**:simple / phased / composite / v1-direct(本 PRD 是 simple)
- **Phase 1 · 7 元素 spec.md** 起草(用 §1-§6 同 IDS,加 §7 PPV)
- **Phase 2 · cross-model review**(operator 决定:codex / gpt / opus 哪些参与;reviewed-by 完成后 status 升 frozen)
- **Phase 3 · 出 7+1 文件**(spec.md + architecture.md + tech-stack.md + SLA.md + risks.md + non-goals.md + compliance.md;PPV 嵌 spec.md §7)

### 2. task-decomposer(参考 `.claude/skills/task-decomposer/SKILL.md`)

operator 起 `XenoDev/.claude/skills/task-decomposer/SKILL.md` 时:
- 9 字段 frontmatter 同 IDS task-decomposer 范式(eg `id` / `title` / `file_domain` / `recommended_model` / `dependencies` 等)
- DAG 用 `dependency-graph.mmd`(mermaid)
- 10-30 task per spec(同 IDS 范式)

### 3. parallel-builder(参考 `.claude/agents/parallel-builder.md` 若有,否则 IDS .claude/commands/parallel-kickoff.md)

operator 起 `XenoDev/.claude/skills/parallel-builder/SKILL.md`:
- 每 task 独立 worktree(per Cursor 3 multi-root 范式)
- TDD:test → red → implement → green
- /task-review verdict ≠ BLOCK 才 merge

## operator 在 XenoDev 跑 Block D 的 checklist

```bash
cd /Users/admin/codes/XenoDev

# 1. 确认 bootstrap 已落
test -f AGENTS.md && test -f CLAUDE.md && test -f PRD.md && test -f HANDOFF.md
test -d lib/handback-validator && test -x .claude/hooks/block-dangerous.sh

# 2. 起 spec-writer skill(operator 自写,参考 IDS .claude/agents/spec-writer.md)
mkdir -p .claude/skills/spec-writer
# 编辑 .claude/skills/spec-writer/SKILL.md
# 参考 /Users/admin/codes/ideababy_stroller/framework/xenodev-spec-writer-derivation-guide.md(本文件)

# 3. 跑 spec-writer 产 spec.md(7 元素 + PPV)
mkdir -p specs/006a-pM
# operator 在 Claude Code session 触发 spec-writer skill,input = PRD.md + HANDOFF.md
# output = specs/006a-pM/{spec,architecture,tech-stack,SLA,risks,non-goals}.md

# 4. cross-model review 跑过(verdict ≠ BLOCK)→ frontmatter `reviewed-by: codex` 等
# (operator 在 XenoDev session 调 codex/gpt/opus review)

# 5. status: draft → review → frozen

# 6. 起 task-decomposer skill(同模式)
mkdir -p .claude/skills/task-decomposer
# 编辑 SKILL.md;input = specs/006a-pM/spec.md;output = specs/006a-pM/tasks/T*.md + dependency-graph.mmd

# 7. 跑 task-decomposer
# 期望:10-30 task,每 task 9 字段 frontmatter

# 8. 起 parallel-builder skill(同模式;Block E 才用)
```

## OQ(本指南承认不解决)

- **OQ-derive-1**:XenoDev spec-writer 是否复用 IDS sdd-workflow `templates/`(PRD-base.md / PRD-simple.md 等)?per stage doc §W2 "schema 重新派生" → 推荐**不直接 cp**,operator 重写;但概念可参考。Block D 实跑时 operator 决。
- **OQ-derive-2**:XenoDev cross-model review 用哪 model 组合?per IDS .claude/commands/task-review.md 范式有 claude-light / claude-full / codex / mixed 4 选项;XenoDev 默认推荐 mixed(codex + claude-full)。Block D 跑 spec review 时 operator 决。
- **OQ-derive-3**:XenoDev `templates/spec.template.md`(7 元素骨架 + PPV)operator 是否手写还是 cp IDS templates 改?推荐手写(stage doc 强约束);若 cp 改 → 加 attribution 注 "concepts inspired by IDS sdd-workflow templates"。

## Block D 完成标志

- [ ] XenoDev `.claude/skills/{spec-writer,task-decomposer}/SKILL.md` 存在
- [ ] XenoDev `specs/006a-pM/spec.md` 存在(7 元素 + PPV)
- [ ] spec.md frontmatter `reviewed-by: <codex|gpt|opus|...>`(≠ pending)
- [ ] XenoDev `specs/006a-pM/tasks/T*.md` ≥ 1 个 task + `dependency-graph.mmd`
- [ ] (XenoDev 端)git log 至少 2 commit(skill 起步 + spec ship + tasks ship)

## 失败模式 + escalation

- **operator 起 spec-writer skill 卡**:重读本指南 §"XenoDev 7 元素 spec contract" + IDS `.claude/agents/spec-writer.md`;若仍卡 → 报 IDS Block D friction,我加 IDS 端 helper commit
- **Spec Kit 0.8.7 schema 兼容度暴露问题**(OQ-B2.1-1):报我,我更新 `framework/spec-kit-evaluation.md` 标 v0.2 fork trigger 触发
- **cross-model review BLOCK** → 在 XenoDev session 修 spec / 重派 task,本 plan 不在 IDS 端 fix

## 与 plan-rosy-naur v11 关系

本指南是 Block D IDS 端 helper(plan v11 标的"我可读 IDS 历史 spec-writer 范式作 reference,产 Markdown 指引")。

Block D 的真实跑由 operator 在 XenoDev session 自主导;本指南只提供:
- IDS 端 reference 文件路径清单(operator 可 cat 参考)
- 7 元素 vs 6 元素 schema 差异(adapter 模式落地形态)
- checklist + 完成标志
- OQ + 失败模式 + escalation 路径
