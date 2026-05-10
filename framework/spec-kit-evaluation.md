---
doc_type: framework-spec-kit-evaluation
generated: 2026-05-10
upstream: discussion/006/forge/v2/stage-forge-006-v2.md (B2.1 Block D)
purpose: 评估 GitHub Spec Kit 0.8.7 与 XenoDev v0.1 兼容度,推荐 fork 策略
v0_2_note_1_owner: 本文档为 v0.2 note 1 的预答案;首个真 PRD 起 sdd-workflow 时回看
---

# Spec Kit 0.8.7 兼容度评估 · XenoDev v0.1 视角

## TL;DR(决策)

**推荐:adapter 模式**(stage doc §"模块 B" step 5 倾向)

- 引用 Spec Kit 0.8.7 部分 skill 的概念(spec-first / 4-phase),自加 PPV 第 7 元素扩展
- **不 fork 整 repo**(Eng. cost 不值)
- v0.2 升级触发器:首个真 PRD 起 sdd-workflow 时若 adapter 不足 → 升级 fork(本文档为 v0.2 note 1 的预答案,B2.2 跑首 PRD 时回看)

---

## Context · 为什么评估

stage doc §"模块 B" step 5 + §"B2 流" M7 列出"评估 fork Spec Kit 0.8.7 现行 schema(adapter 模式优先,fork 整 repo 次选;v0.2 note 1)"。本评估为 B2.1 Block D 落地。

stage doc 关键事实(L385):
> Opus P2 原写 "Spec Kit v2 schema" 是事实错误(SOTA latest 是 0.8.7,GPT P2 §1 row 3 修正)

stage doc verdict 显式 SOTA 共同方向(L549 / L358):
> SOTA 共同方向(Anthropic Agent SDK + Skills / Cursor 3 multi-root + worktrees / **Spec Kit 0.8.7 spec-first** / MSR 2026 失败实证)全部指向 **运行时 harness + 4-phase + 跨仓 workspace + 可观测 + 可学习**

---

## 8 维度评估

### 维度 1 · spec.md schema 兼容度(SK 0.8.7 7 元素 vs XenoDev 需 PPV 第 7 元素)

| 项 | SK 0.8.7(推断) | XenoDev v0.1 需求 | 兼容? |
|---|---|---|---|
| §1 Outcomes | ✅ 同名 | ✅ 同 | YES |
| §2 Scope IN/OUT | ✅ 同名 | ✅ 同 | YES |
| §3 Constraints | ✅ 同名 | ✅ 同 | YES |
| §4 Prior Decisions | ✅ ~同名(SK 用 Decisions) | ✅ 同 | NEAR (rename ok) |
| §5 Task Breakdown | ✅ ~同名 | ✅ 同 | NEAR |
| §6 Verification Criteria | ✅ ~同名 | ✅ 同 | NEAR |
| **§7 Production Path Verification (PPV)** | ❌ **SK 0.8.7 没有** | ✅ XenoDev 必须有(per ADP V4 lessons learned) | **GAP** |

**结论**:6 元素近似兼容,**第 7 元素 PPV 是 XenoDev 自加的扩展**。adapter 模式可在 SK 7 元素之上 append PPV,无需 fork 整 repo。

> **OQ-B2.1-1**(本文档承认):SK 0.8.7 的 schema 是否有更精细的子元素(eg §3 Constraints 是否含 OQ 子节)— 需 B2.2 起 sdd-workflow 时实测。本评估基于 stage doc 引用 + 行业 spec-driven dev 通识,未 deep-dive SK 0.8.7 源码。

### 维度 2 · 4-phase 强顺序范式 vs XenoDev 现有计划

SK 0.8.7 4-phase(per stage doc §"模块 B" step 5 + §"B1 流"):**spec → plan → tasks → implement**(强顺序,不能并行)

XenoDev v0.1 计划:hand-off → spec-writer → task-decomposer → parallel-builder → ship → hand-back(同 4-phase 结构)

**结论**:**完全同构**。adapter 模式无需改 phase order,只在每 phase 内部参考 SK skill 实装。

### 维度 3 · spec→tasks 拆解 skill 兼容度

XenoDev 需要的:spec.md → tasks/T*.md(9 字段 frontmatter,per IDS task-decomposer 已实装范式)+ dependency-graph.mmd

SK 0.8.7 推断的:spec.md → tasks(具体 task schema 未深 verify)

**结论**:概念层兼容,具体 frontmatter / DAG 格式 XenoDev 自定义(不强 fork SK)。adapter 模式可参考 SK skill prompt 但不拷代码。

### 维度 4 · cross-model review 集成度

XenoDev 需要的(per IDS L4 已实装范式):/task-review verdict ≠ BLOCK + cross-model review for v1.0 paths

SK 0.8.7 是否带 review loop:**未知**(stage doc 未给细节)

**结论**:即使 SK 带 review loop,XenoDev 自带的 codex / opus / gpt cross-model review 范式(per IDS .claude/commands/task-review.md 历史实装)更熟悉,继续自带。adapter 模式不依赖 SK review loop。

### 维度 5 · parallel-builder 兼容度(Cursor 3 multi-root 范式)

stage doc verdict 共同方向:Cursor 3 multi-root + worktrees + async subagents

XenoDev 需要的:parallel-builder per task in worktree(per IDS .claude/commands/parallel-kickoff.md 已实装)

SK 0.8.7 是否带 parallel-builder:**推断:可能没有**(SK 偏 spec-driven design,parallel build 是 Cursor 范式)

**结论**:XenoDev 自带 parallel-builder + worktree(从 IDS 派生),不依赖 SK。adapter 模式无 parallel build 兼容性问题。

### 维度 6 · 8KB AGENTS.md 限制兼容度

Vercel benchmark:AGENTS.md ≤ 8KB = 100% activation;> 8KB drops。XenoDev 严守。

SK 0.8.7 是否大文件吃 context:**推断:adapter 模式只引部分,不拷整 repo,无 context bloat 风险**

**结论**:adapter 安全,fork 整 repo 风险高(SK repo 可能含许多 example / doc / template,污染 XenoDev context)。

### 维度 7 · 跨仓 hand-off / hand-back 兼容度(SHARED-CONTRACT v2.0 §3 / §6.3 / §3.1)

SK 0.8.7 的 hand-off 协议:**未知**(SK 主要单仓 spec-driven,跨仓非 SK 重点)

XenoDev 需要的:per IDS framework/SHARED-CONTRACT.md §6 v2.0 ACTIVE-but-not-battle-tested。完整 §6.2 workspace 4 字段 + §6.3 hand-back schema + §3.1 source_repo_identity + §6.2.1 6 约束。

**结论**:**SK 不替代 SHARED-CONTRACT**。XenoDev 跨仓协议层完全走自家 SHARED-CONTRACT,SK 不掺和。adapter 模式无冲突。

### 维度 8 · License + 版本演化兼容度

SK 0.8.7 license:**MIT**(行业惯例;具体待 SK repo 实证)

XenoDev license:MIT(per LICENSE.template)

**结论**:license 兼容。版本演化:adapter 模式 XenoDev 与 SK 各自演化,无 lock-in;fork 整 repo 则 XenoDev 跟 SK 主线 merge 是 maintenance burden。

---

## 决策矩阵

| 模式 | Eng. cost | 维护成本 | 解耦风险 | 自定义自由度 | 依赖 OQ |
|---|---|---|---|---|---|
| **adapter**(推荐) | 低(1-2 day,B2.2 跑首 PRD 时实装 spec-writer skill 引 SK 概念) | 低(各自演化) | 低(无 lock-in) | 高(随时改 PPV / phase) | OQ-B2.1-1 待 B2.2 验 |
| fork 整 repo | 高(1-2 周,要 cp + reorg + 削功能) | 高(要 sync SK 主线) | 高(SK breaking change → XenoDev 跟改) | 中(改了上游 fork 难合) | 同 |
| **不用 SK,纯自研** | 中(2-3 day 起 spec-writer 等 skill;但已有 IDS 历史范式可复用) | 低 | 0(无外部依赖) | 最高 | 0 |

**为什么 adapter 而非纯自研**:stage doc verdict L549 显式列 SK 0.8.7 为 SOTA 共同方向之一;若不用,等于忽略 industry validated pattern。adapter 模式取概念不取代码,SOTA 致敬 + 实装自由两全。

**为什么 adapter 而非 fork 整 repo**:fork 整 repo 工程量级别更高(1-2 周 vs 1-2 day),且 v0.1 没有具体 SK feature dependency,fork 收益不明确。stage doc §"模块 B" step 5 显式 "adapter 模式优先,fork 整 repo 次选"。

---

## 实装建议(B2.2 起跑时落)

### XenoDev spec-writer skill 设计(adapter 模式具体形态)

```
.claude/skills/spec-writer/SKILL.md  (XenoDev 内,B2.2 起跑时实装)

frontmatter:
  inspired_by: GitHub Spec Kit 0.8.7 (concept-level only, no code copied)
  schema_extends: SK 7 elements + XenoDev §7 PPV
  license: MIT (XenoDev 自家)

body:
  Phase 0 · 读 PRD.md(由 IDS hand-off 提供)
  Phase 1 · 起 spec.md 7 元素(同 SK)
    §1 Outcomes
    §2 Scope IN/OUT
    §3 Constraints
    §4 Prior Decisions
    §5 Task Breakdown
    §6 Verification Criteria
  Phase 2 · 起 §7 Production Path Verification(XenoDev 扩展)
    - 真路径起点 → 终点 + 必经环节 + 可执行验证命令
    - 防 mock-pass-prod-fail(灵感:stroller idea004 12 routes 404 案例)
  Phase 3 · 跑 cross-model review(自带 codex / gpt / opus,不依赖 SK review loop)
```

### v0.2 升级 fork 整 repo 的 trigger

以下任一发生 → operator 重审 fork 决策(可能升级):
1. **B2.2 跑首 PRD 时发现 SK 7 元素子结构与 XenoDev 自定义冲突**(eg SK §3 含 XenoDev 没考虑的子节)
2. **SK 0.8.7 发布主流 plug-in / template,fork 后能直接复用,工程量 < adapter 自研**
3. **XenoDev 跑 ≥ 5 真 PRD 后回看,adapter 模式累计自研代码 > fork 维护工时**

第 3 条 trigger 与 stage doc v0.2 note 2(累计 3 idea / 30 task)对齐。

---

## 与 stage doc 的对齐

stage doc 引用本评估的位置(B2.2 起跑时回看):
- §"模块 B" step 5(L200):"评估 fork Spec Kit 0.8.7 现行 schema(adapter 模式优先)"
- §"Open questions"(L283):"OQ-2:Spec Kit 0.8.7 schema 与 PPV 第 7 元素兼容度 — XenoDev 第一个真 PRD 起 sdd-workflow 时回看(v0.2 note 1)"
- §"v0.2 note 1"(L340):"Spec Kit fork 精确边界(adapter vs fork 整 repo)— XenoDev 第一个真 PRD 起 sdd-workflow 时决"

**本评估的角色**:为 v0.2 note 1 提供**预答案**(adapter),让 XenoDev v0.1 起跑就有方向;v0.2 决策点是 fork 升级 trigger(上节列 3 条),不是从零开始决定。

---

## OQ(本评估承认不解决的)

- **OQ-eval-1**:SK 0.8.7 真实 spec.md schema 子结构(§3 是否含 OQ 子节、§4 Prior Decisions 是否含 reference 字段、etc) — 本评估基于 stage doc 引用 + 行业通识,未 deep-dive SK 源码。**B2.2 起 sdd-workflow 时实测**
- **OQ-eval-2**:SK 0.8.7 license 精确版本(MIT vs Apache 2.0 vs other) — 实测时确认
- **OQ-eval-3**:SK 0.8.7 是否有 official PPV 同等扩展 plug-in(若有,XenoDev 不需自造) — 实测时确认
- **OQ-eval-4**:adapter 模式的"SOTA 致敬"语义是否需要在 XenoDev spec-writer skill 文档显式标 attribution(eg "concepts inspired by GitHub Spec Kit 0.8.7")— 推荐显式标,符合行业惯例

---

## Changelog

- 2026-05-10 v1(B2.1 Block D):初稿,8 维度评估 + adapter 决策 + 4 OQ
