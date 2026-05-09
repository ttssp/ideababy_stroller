# Forge v2 · 006 · P1 · Opus 4.7 Max · 独立审阅(no search)

**Timestamp**: 2026-05-09T12:30:00Z
**Searches used**: NONE in this round.
**Visibility**: I did NOT read other reviewer's P1.
**Reviewer stance**: 审阅人 — 评判已存在物,不是 daydream。
**Convergence intent**(operator binding):每个 W 都要有收敛主线 + v0.2 note 旁注;不暴力压扁分歧。

## §0. 我读到的标的清单 + 阅读策略 + K 摘要

### 我读了(9 个 X 标的,全部 reachable)

**ADP 仓 5 标的**(架构 + 工程纪律视角):
- `/Users/admin/codes/autodev_pipe`(顶层 ls:Makefile / pyproject.toml / src/ / specs/{v3.2,v3.3,v4,007a-pA,...} / .claude/{skills,hooks,agents} / docs/decisions / templates / tests / human_op*.md)
- `/Users/admin/codes/autodev_pipe/specs/v4/spec.md`(Δ-X1,V4 frozen schema 0.2 / 5 outcome / 8 in-scope / 7 out-of-scope / reviewed-by codex 4 轮闭环)
- `/Users/admin/codes/autodev_pipe/docs/decisions/0008-v4-dogfood-path.md` + `0009-v4-scope-downgrade.md`(Δ-X2,B 路径 → C Hybrid 降级 + AC4 弱化为 ≥1 真自用 + ≥1 ADP self)
- `/Users/admin/codes/autodev_pipe/.claude/skills/{sdd-workflow,task-decomposer}/SKILL.md`(Δ-X3,**两 skill 都 port from ideababy_stroller**,见 sdd-workflow L11)
- `/Users/admin/codes/autodev_pipe/.claude/hooks/block-dangerous.sh`(Δ-X4,23 条 dangerous pattern + python3 解析 + permissionDecision allow/deny)
- v1 #11 `solo_ai_pipeline_v3.1.md`(粗扫:已被 v3.2-v4 spec.md 系列接替,作为历史 archive)

**IDS 本仓 4 标的**(架构 + 工程纪律 + Y5 重做代价视角):
- `specs/007a-pA/spec.md` v0.3 + `HANDOFF.md`(Δ-X5,4 轮 R1-R4 review 全闭环 + Mini-PRD Handoff Block 结构化转写 + L138 显式建议 ADP V4 checkpoint-01 后再切仓)
- `framework/SHARED-CONTRACT.md` v1.1.0(Δ-X6,5 §:PRD schema / Safety Floor 双 SSOT / Hand-off 协议 / 版本演化 / 五元组;v1.1 audit 修订删 cli + Makefile 假设)
- `framework/NON-GOALS.md` v1(NG-1 Linux kernel + Anthropic Skills SDK 范式不内化历史 repo 代码)
- `framework/ADP-AUDIT-2026-05-08.md` §9(DRIFT-1 至 DRIFT-4 完整论证)

### 我跳过的:9 个 v1 X #1-#9(operator §1 显式 no-rerun;v1 已审且自 v1 起未变)

### K(用户判准)摘要

K1-K6 verbatim from proposal §006:**达成基于 Claude Code 实现可靠自动化开发的 framework/pipeline 共识方案**(K6),核心约束 = 可靠 + 自动化最高(K1)/ operator 非软件背景但能写 PRD(K2)/ 4 个历史尝试 idea_gamma2 + vibe-workflow + autodev_pipe + IDS(K5)。

**K7**(operator 2026-05-09 Append):**ADP-next 是 framework "待生下半边"产物,V4 是物证不是吸收对象**;K5 中"autodev_pipe 项目"实际指 ADP-next 的设计意图,而非 V4 这版具体实装。

**moderator-notes.md 5 件 binding 事实**(逐条吸收):

1. **ADP-next 角色重定义**:V4 仅参考,IDS=idea→PRD,XenoDev(ADP-next 仓名)=L4
2. **§9 4 实证 drift**(DRIFT-1 架构级 / DRIFT-2 立即阻塞 / DRIFT-3 双 source / DRIFT-4 emergent):优先于 v1 任何 verdict
3. **SHARED-CONTRACT v2.0 双向 hand-off**:正向 PRD + 反向 hand-back(drift 反馈 / PRD revision / 实践统计)
4. **强制 forge 元层锁决定**:防"想法变了→静默停"(V4 失败模式),ADP-next 重大决策必须在 IDS 仓走 /expert-forge
5. **启动路径**(Q13 第一性):forge v2 verdict → 拆 IDS 优化 + XenoDev L4,**不重走 L1-L3,不另起 idea 008 / forge 008**

### 阅读策略

按 Y 三视角分配读取深度:架构(SHARED-CONTRACT + ADP-AUDIT 全文 + ADP specs/v4 + sdd-workflow SKILL),工程纪律(block-dangerous + sdd-workflow + task-decomposer + 007a-pA 4 outbox),Y5 重做代价(ADP 顶层 ls + V4 已 frozen 模块清单 + ADR 0008/0009 sunk-cost 估值)。

## §1. 现状摘要(按 Y 三视角)

### Y1 · 架构设计

**核心事实**:ADP V4 已实装的"AI 自动开发 pipeline" = 6 个工程模块 — sdd-workflow(spec init / 7 元素契约) / task-decomposer(9 字段 frontmatter / 1-4h 原子单元) / parallel-builder(5 hard rule / file_domain 互斥) / spec_validator(schema 强制) / block-dangerous hook(23 pattern) / retrospective skill(L1+L2 / `~/.claude/lessons/` user scope)。**这 6 个模块各自有独立工程价值**,但 V4 整体架构假设(autodev_pipe-cli build 直送 / Makefile target / IDS PRD = ADP spec 同 schema)在 SHARED-CONTRACT v1.1 audit 中**已实证全错**。

**关键 drift**(`framework/ADP-AUDIT-2026-05-08.md` §9 DRIFT-1):**IDS L4 设计假设错误**。IDS CLAUDE.md L24 假设 IDS 自带完整 SDD 工具链,实证 IDS 仓 0 Makefile / 0 pyproject.toml / 0 pytest / 0 spec_validator。应然分工 = IDS(idea→PRD)+ XenoDev(PRD→spec→build→ship 一条龙)。这一条**颠覆 v1 verdict 中"L1-L4 + forge 横切 = framework 默认骨架"** 的隐性假设(v1 是基于 IDS 自带 L4 build 的)。

### Y2 · 工程纪律

**ADP 实装 ≠ 文档主张**:V4 spec.md 顶部声称 "本 spec 自身遵守 v3.3 7 元素契约,reviewed-by codex 4 轮闭环"是真的(commit 物证 + ADR 0008/0009 partial supersede 双向链接齐全),工程纪律实装在 ADP 子集上**已经达到 production-grade**。但 V4 整体目标(L3 项目级 retrospective + subagent_promote + worker-monitor + 真跨项目 lesson 反哺)被 ADR 0009 显式推 V4.2,**V4 第一版只验证"L1+L2 retrospective + lesson 能 import"**。

**IDS 这边工程纪律** = 跨仓 hand-off 协议(SHARED-CONTRACT v1.1.0 / HANDOFF.md schema / 5 元组 producer-consumer)+ specs-protection 规则 + plan-start 命令产 hand-off 包。但**实测产生 DRIFT-2/3/4**:IDS 仓缺 Python infra(立即阻塞 task verification)+ 双 source of truth(IDS specs/007a-pA + ADP 也产 13 task)+ task-decomposer subagent emergent 行为(`working_repo: ideababy_stroller` 字段)。

### Y5 · 重做代价 / 沉没成本 / 知识保留(L/P/C 分层视角)

V4 实装 6 模块的 L/P/C 价值评估(给 W2 decision-list 起点):

| 模块 | L 设计原则 | P 范式结构 | C 代码 | ADP-next 处置建议 |
|---|---|---|---|---|
| sdd-workflow(7 元素 + PPV) | ✅ | ✅ | ✅ port-from-IDS | **保留**(L+P+C 都对;XenoDev 直接继承) |
| task-decomposer(9 字段 + 1-4h) | ✅ | ✅ | ✅ port-from-IDS | **保留**(同上) |
| parallel-builder(5 hard rule) | ✅ | ✅ | ⚠ 需重审 | L+P 保;C 在 XenoDev 重写时纳入 |
| spec_validator | ✅ | ✅ | ⚠ 需重审 schema_version | L+P 保;C 看 ADP-next schema 决定 |
| block-dangerous hook(23 pattern) | ✅ | ✅ | ✅ | **直接 cp**(纯 bash + python3,无依赖) |
| retrospective skill L1+L2 + lessons/ user scope | ✅ | ✅ | ⚠ 12 周 dogfood 未跑 | L+P 保;C 等 dogfood 信号(在 V4 上跑没意义,operator 已决议不再跑;**XenoDev 起来后重做 dogfood**) |

**沉没成本估算**:V4 自 2026-04-29 起约 1 周工程量,核心模块均有真审 reviewed-by 痕迹;**完全丢弃 ≠ 零保留**:6 模块的 L+P 全保留(有客观工程价值),C 在 XenoDev 起来时部分 cp(block-dangerous)+ 部分参考重写(其他)。**真丢弃的是 V4 整体架构假设**(autodev_pipe-cli build / Makefile target / IDS PRD = ADP spec 同 schema)。

## §2. First-take 评分

| Y 维度 | keep | refactor | cut | new |
|---|---|---|---|---|
| 架构设计 | sdd-workflow + task-decomposer 7/9 元素契约 / SHARED-CONTRACT 五元组 producer-consumer 模型 | SHARED-CONTRACT v1.1.0 → v2.0(双向 hand-off + DRIFT-1 应然分工 + 新仓名 XenoDev) / IDS CLAUDE.md L24 / plan-start 重写 | "L1-L4 + forge 横切 = framework 默认骨架"(v1 verdict 隐性假设;IDS 不带 L4 build)/ V4 整体架构假设(`autodev_pipe-cli build` / Makefile target / 双 spec) | XenoDev 仓(ADP-next 新建,V4 archive 打 git tag `v4-final`)/ 反向 hand-back 通道(XenoDev → IDS,drift 反馈 + PRD revision + 实践统计)/ 强制 forge 元层锁决定(IDS = 治理 + 评判仓,XenoDev = 执行仓) |
| 工程纪律 | block-dangerous 23 pattern / spec_validator + reviewed-by 4 轮闭环 / parallel-builder 5 hard rule + file_domain 互斥 / specs-protection rule | retrospective skill(等 XenoDev 起来后重新 dogfood) / lessons/ user scope cp 机制 | V4 12 周 dogfood / V4 4 周 checkpoint 01/02/03 / "≥ 1 真自用候选 4 周内确认" 降级条款 | XenoDev L4 build chain(spec / task / parallel / ship)+ XenoDev 自己的 dogfood / 跨仓双向 commit 引用机制 |
| Y5 重做代价 | 6 ADP 模块的 L+P 全保留(有客观工程价值,见 §1 表) / 4 历史尝试的 lesson(K5 verbatim) | block-dangerous → 直接 cp 进 XenoDev / sdd-workflow + task-decomposer → port-from-IDS-pattern + 在 XenoDev 重写细节 | V4 整体架构假设 / V4 dogfood 信号(因不再维护已失效) / 决策账本 v0.1(已暂停) | "L/P/C 分层 cp/port/重写"成为 ADP-next 的明确 onboarding 路径 |

**Binding 声明**(per moderator-notes §四 + operator §四):**v1 verdict 28 项 L/P/C 决策矩阵 + 5 模块 refactor plan + §4 next-PRD 仅作参考,不绑定本轮 v2 verdict**。本 P1 §2 评分基于 v1 verdict 之后的事实变更(7 Δ-X + §9 4 drift + K7 grounding 修订),独立于 v1 决策矩阵。

## §3. 我现在最不确定的 3 件事

1. **DRIFT-1 应然分工的具体边界**:IDS 是否完全不写任何 specs/?那 IDS L4 命令链(plan-start / spec-from-conclusion)如何重定义?spec-writer 子代理留 IDS 还是迁 XenoDev?— 这条直接影响 W3 refactor-plan 中 IDS 改造规模(轻 = 改 SHARED-CONTRACT + plan-start;重 = 整个 IDS L4 命令链 retire);Phase 2 SOTA 检索时应优先看 GitHub Spec Kit v2 / Cursor Composer 是否有"上游产 PRD,下游产 spec/build"的清晰边界范例。

2. **XenoDev 启动顺序与 IDS 重写顺序的耦合度**:operator 决议"先跑 v2 verdict → 拆 B1 IDS 优化 + B2 XenoDev L4"。但 B1(SHARED-CONTRACT v2.0)与 B2(XenoDev 第一个 PRD ship)是否可并行?或必须 B1 先 → B2 才能 hand-off?这直接影响 W5 next-dev-plan 节奏拆分。

3. **6 ADP 模块 C 级 cp 边界**:`block-dangerous.sh` 显然可 cp(纯 bash + python3 + 23 pattern 是工业共识);但 `sdd-workflow` / `task-decomposer` SKILL.md 顶部已声明 "port from ideababy_stroller" — 现在 IDS 这边已有原版,XenoDev 起来时是 cp ADP 的 port 版还是直接从 IDS 重新 port?这决定 IDS skills/ 与 XenoDev skills/ 的物理 source-of-truth 归属。
