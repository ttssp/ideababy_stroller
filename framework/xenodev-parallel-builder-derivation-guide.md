---
doc_type: xenodev-skill-derivation-guide
generated: 2026-05-12
upstream: plan-rosy-naur v12 · plan v0.2-global 件 2.4
purpose: parallel-builder SKILL 派生指引(§9 checklist GATE/AUDIT 区分 + events.jsonl hard-fail · B2.2 RETRO §4.2.1 audit-step 全漏 codify)
ids_reference_files:
  - framework/SHARED-CONTRACT.md
  - framework/xenodev-spec-writer-derivation-guide.md
  - framework/task-decomposer-derivation-guide.md
  - discussion/006/b2-2/B2-2-RETROSPECTIVE.md
---

# parallel-builder SKILL 派生指引(IDS framework feedback · 件 2.4)

## §1 背景(scope · 与其他 derivation guide 关系)

本指引是 plan v0.2-global 件 2.4 落地 · F4(B2.2 RETRO §4.3 L171)· 触发自 B2.2 batch 3 ship `.eval/events.jsonl` 全漏 + 4 项 audit step 同类 gap 的真实证。

- **与 `xenodev-spec-writer-derivation-guide.md` / `task-decomposer-derivation-guide.md` 关系**:平级 · 三件套各覆盖一个 SKILL · 本指引补 parallel-builder 端 audit step 行为约束。
- **scope IN**:SKILL §9 checklist 12 项 [GATE] / [AUDIT] 二元分类 · events.jsonl 升 [GATE] 方案 · 跨仓应用 4 步。
- **scope OUT**:不直接改 XenoDev SKILL.md(无写权限) · 不预决 producer/consumer validator 实装 · 不替 operator 决 worktree 模式。

## §2 SKILL §9 checklist GATE / AUDIT 区分(核心)

**[GATE]** = hard-fail · 漏 = ship 失败 · agent 必撞墙
**[AUDIT]** = non-blocking · 漏不阻本 task ship · 但 PHASE 末 operator 自审必 backfill

| # | §9 项 | 分类 | 漏的后果 |
|---|---|---|---|
| 1 | producer validator PASS | **[GATE]** | ship 失败 |
| 2 | consumer validator PASS(若 IDS 端跑) | **[GATE]** | ship 失败 |
| 3 | tests 全 PASS | **[GATE]** | ship 失败 |
| 4 | lint clean | **[GATE]** | ship 失败 |
| 5 | coverage ≥ 阈值 | **[GATE]** | ship 失败 |
| 6 | git status clean(commit 前) | **[GATE]** | ship 失败 |
| 7 | events.jsonl 写入 | **[GATE]** ⚠ v0.2 升 | (升 [GATE] 后)ship 失败;原 [AUDIT] 时 silent skip |
| 8 | merge 字面命令 log | **[AUDIT]** | PHASE 末 backfill |
| 9 | verifier 机器化 log | **[AUDIT]** | PHASE 末 backfill |
| 10 | preflight 显式跑 log | **[AUDIT]** | PHASE 末 backfill |
| 11 | retro 记录 | **[AUDIT]** | PHASE 末 backfill |
| 12 | review-log/ 留档 | **[AUDIT]** | PHASE 末 backfill |

**AUDIT 项守则**(对 8-12 项适用):
- "若漏 · PHASE 末 operator 自审 backfill · 不阻本 task ship · 但 backlog 必清"
- agent ship 完即提示"⚠ 本 task 漏 [AUDIT] 项 N 个,加入 PHASE-末 backfill 队列"

## §3 events.jsonl hard-fail 升级(本件核心)

v0.1 状态:`events.jsonl` 是 [AUDIT] 项 · B2.2 batch 3 ship 全漏(per §5 案例)。
v0.2 升级:**改 [GATE]** · 消灭 side-effect 语义 · 让 agent "hard-block 反馈" 撞墙。

跨仓 patch 三处:
1. **SKILL §6.4 (events 写入定义)**:加 "写入失败 = ship 失败 · 显式 exit 1 · 不允许 silent skip"
2. **SKILL §9 (第 12 项 checklist)**:由 [AUDIT] 改 [GATE]
3. **SKILL §4.1 (atomic order 表)**:把 events.jsonl 写入加到 commit 前置 — "commit 前 events.jsonl 必写"

理由(per B2.2 RETRO §4.2.1):"hard-block 反馈 vs 纯 side-effect 反馈 在 agent 行为上有质的差" · producer/consumer validator(fail-closed)0 漏 · side-effect step 全漏 · 升 [GATE] 后 events.jsonl 加入 fail-closed 阵营。

**风险**:hard-fail 可能阻 ship 节奏 · 但 producer validator 阻已是常态 · events.jsonl hard-fail 同类。**备选**(若 hard-fail 争议):保留 [AUDIT] + 加 SKILL §6.4 显式 reminder + PHASE 末 backfill 强制(本指引 plan 默认主路径 = [GATE])。

## §4 跨仓应用步骤(IDS guide → XenoDev SKILL.md)

```
Step 1: operator 在 IDS 仓读本 guide 全文(本文件)
Step 2: cd /Users/admin/codes/XenoDev
Step 3: patch `.claude/skills/parallel-builder/SKILL.md`:
        - §9 checklist 12 项加 [GATE]/[AUDIT] 前缀(本 §2 表)
        - §9 第 12 项 events.jsonl 由 [AUDIT] 改 [GATE]
        - §6.4 加 "写入失败 = ship 失败 · 显式 exit 1"
        - §4.1 atomic order 加 events.jsonl 至 commit 前置
Step 4: XenoDev 内 commit(operator 自审 + 自跑 XenoDev review loop · IDS 不预决)
```

**注**:IDS 不直接改 XenoDev SKILL.md(events.jsonl 在 XenoDev `.eval/` · SKILL 本体在 XenoDev repo · IDS 端无写权限)。Operator 跨仓人工 cp 是当前正常路径(同 spec-writer / task-decomposer guide 模式)。

## §5 案例引用(B2.2 真发生 · verbatim · 不删)

verbatim 摘自 `discussion/006/b2-2/B2-2-RETROSPECTIVE.md`:

**§1.2 三 ship 全漏(L63-69)**:

> ### 1.2 deviation: parallel-builder SKILL §6.4 `.eval/events.jsonl` 三个 ship 全没写
>
> - SKILL §6.4 + §9 checklist 第 12 项要求每 task ship 写一行 event
> - 3 个 ship 全跳了 — events.jsonl 是纯 side-effect(不阻 ship gate)
> - producer/consumer validate 是 fail-closed → 都 PASS;side-effect step → 全漏 → **agent 默认轻视 audit step**
> - **严重度**:中-高 — 影响 spec O3 outcome(append-only event log)实证
> - **RETRO 决议**:PHASE 1 起跑前 backfill 这 3 条;PHASE 1-3 所有 task ship 必跑 §6.4

**§4.2.1 4 项 audit step 全漏 根因(L159)**:

> - **non-blocking audit step 易被 agent 忽略** — events.jsonl / merge 字面命令 / verifier 机器化 / preflight 显式跑 4 项全漏。producer/consumer validate(fail-closed)0 漏;side-effect step 全漏。**hard-block 反馈 vs 纯 side-effect 反馈** 在 agent 行为上有质的差

**§4.3 F4 完整定义(L171)**:

> - **F4**(parallel-builder SKILL §9 in scope · v0.2):checklist 区分 [GATE] / [AUDIT] 前缀,AUDIT 项注明"若漏,PHASE 末 operator 自审必 backfill",或把 events.jsonl 写入失败设为 hard-fail

## §6 失败模式 + 备选路径

| 路径 | 强度 | 何时选 |
|---|---|---|
| **主路径**:events.jsonl 升 [GATE](本指引默认) | hard-fail | events.jsonl 是 spec O3 outcome 实证 · 必须落 · 防 agent silent skip |
| **备选**:保留 [AUDIT] + 显式 reminder + PHASE 末 backfill 强制 | soft + 提醒 | hard-fail 阻 ship 节奏争议时 · 退守方案 |

风险:hard-fail 改完后 · 历史 task ship pipeline 若有人手跑(不是 SKILL 自动写)将撞墙 · operator 决跨仓 patch 前 audit 一次现有 XenoDev pipeline。

## §7 与 plan-rosy-naur v12 关系

本指引是 plan-rosy-naur v12 B 件 3(2026-05-12 ship)产物 · plan v0.2-global 件 2.4 落地。

- **不动**:spec-writer guide / task-decomposer guide / SHARED-CONTRACT
- **可 amend**:本 §2 GATE/AUDIT 表(12 项以外新 audit step 出现时加行)/ §3 events.jsonl 升级实装细节(SKILL §6.4 / §9 / §4.1 三处 patch 优先级 / 文案)
- **下游**:operator 跨仓 cp 进 XenoDev SKILL.md · XenoDev review loop 自跑

## §8 Changelog

- **2026-05-12 v1.0**: 起新 file · §2 SKILL §9 12 项 [GATE]/[AUDIT] 全分类落地 · §3 events.jsonl 升 [GATE] 三处 patch 方案 · §4 跨仓应用 4 步 · §5 B2.2 RETRO §1.2 + §4.2.1 + §4.3 三段 verbatim 锚 · 上游:plan-rosy-naur v12 B 件 3 / plan v0.2-global 件 2.4 / F4 / B2.2 RETRO §4.2.1
