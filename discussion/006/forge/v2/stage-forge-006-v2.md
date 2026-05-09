---
forge_id: 006
forge_version: v2
generated: 2026-05-09T13:20:00Z
convergence_outcome: converged
prefill_source: proposals.md§006 + _x-input-draft-by-operator.md + moderator-notes.md
x_hash: 65d9d65c7c17d4e2cf3241b05a469a16
v1_x_hash: e45d68ee6dcc74d2c667976a28940c91
v1_outcome: converged-with-tempo-options
---

# Forge Stage · 006 · v2 · "新建 XenoDev 运行时 harness,V4 archive,IDS 退回 idea→PRD + 治理"

**Generated**: 2026-05-09T13:20:00Z
**Source**: forge run v2 with X = 9 标的(v1#10 + v1#11 + Δ-X1 至 Δ-X7), Y = [架构设计, 工程纪律, Y5 重做代价/沉没成本/知识保留], Z = 对标 SOTA, W = [verdict-only, decision-list, refactor-plan, next-PRD, next-dev-plan, free-essay] 全选
**Convergence mode**: strong-converge(operator binding via moderator-notes §六)
**Rounds completed**: P1 (both), P2 (both), P3R1 (both), P3R2 (both)
**Searches run**: 12(Opus 4 + GPT 8;覆盖 Anthropic Skills/Agent SDK / Cursor 3 multi-root / GitHub Spec Kit 0.8.7 / MSR 2026 agentic PR failure corpus / GPT-5.4 Codex / agentic coding abandonment 实证)
**Moderator injections honored**: 5 件 binding(全部吸收并在 verdict 中显式回应)
**Convergence outcome**: **converged**(双方 P3R2 §2 单一 verdict 完全合一;5 条 R1 分歧在 R2 全部 closed/accepted;5 条 v0.2 note 旁注式纳入,符合 operator §六 "主线收敛 + 旁注补充" intent)
**v1 → v2 framing 变化**:v1 verdict 是 "framework 整体 + L1-L4 + forge 横切 + 分级 harness"(隐性假设 IDS 自带 L4 build);v2 verdict 是 "IDS=idea→PRD+治理 / XenoDev=唯一 L4 runtime / 双向 hand-off",**v1 28 项 L/P/C 矩阵不再绑定**(per moderator §四)。v1 "轻入口、重升级"哲学骨架在 v2 K3 处理时显式继承(GPT P3R1 §3 row 5 强约束 + Opus P3R2 §1 分歧 5 全盘接受)。

---

## How to read this

forge 是横切层(不是 L1-L4 pipeline 的一部分)。本文档是双专家(Opus 4.7 Max / GPT-5.5 xhigh)对 9 个 v2 标的(ADP V4 / IDS framework 协议 / 007a-pA pilot / ADP-AUDIT §9 4 drift)审阅 + SOTA 对标 + 联合收敛后的产出。

**v2 与 v1 的关系**:v1 已跑(2026-05-08,verdict = "分级 harness framework"),v2 因 X 严重变化(ADP V4 已停止维护 + ADP-AUDIT §9 4 实证 drift 产生 + 007a-pA pilot 4 轮 review 闭环)+ K7 reframe(V4 是物证不是吸收对象)+ operator 主动选择 strong-converge 而重跑。v1 verdict **仅参考、不绑定**(operator §四决议)。

读完后你应该:

- 知道双专家对 "ADP-next 应不应该继承 V4 / 应在哪里建 / IDS 角色变化" 的最终单一 verdict
- 拿到 V4 6 模块 + IDS 协议层的 4 列处置矩阵(W2 decision-list)
- 看到 IDS / XenoDev / 跨仓 hand-back 三模块的重构方案(W3 refactor-plan)
- 拿到 XenoDev v0.1 PRD 草案(W4)+ B1/B2 双流 milestone(W5)
- 看到 800+ 字综合长文(W6 free-essay)
- 能基于 §"Decision menu" 直接进入下一步(进 L4 / park / abandon / 跑 v3)

---

## Verdict

**新建 `XenoDev` 仓作为 ADP-next 的运行时 harness;V4 整体 archive(`v4-final` git tag);IDS 退回 idea→PRD + governance/forge + SHARED-CONTRACT v2.0 双向 hand-off,不再产 specs/;XenoDev 承担唯一 PRD→spec→build→ship 一条龙**。**保留 v1 "轻入口、重升级"分级**:Small 走 AGENTS.md + Safety Floor 轻入口(operator 直驱 Claude Code,不走 forge/L1-L4),Medium/Large 走 IDS+XenoDev 双仓全链(回应 K3)。XenoDev v0.1 必落 5 件:Safety Floor 三件套 / 单一 build spec source(对齐评估 fork Spec Kit 0.8.7 现行 schema + PPV 扩展) / workspace schema 4 字段(`source_repo` / `build_repo` / `working_repo` / `handback_target`) / hand-back 包结构化(drift / PRD-revision-trigger / 实践统计三类标签) / Eval/risk 数据接口(append-only event log,记 review failures / operator interventions / hand-back drift 三类 event,**不实装 scoring 算法**)。**强制 forge 元层锁**:任何重大架构转向必须在 IDS 走 `/expert-forge`,XenoDev 不复制 forge 机制。**v2 后启动**:不重走 L1-L3,operator 直接拆 B1(IDS 优化)+ B2(XenoDev L4)双流;**B1 必须先**(SOTA Spec Kit 强顺序),B2 才能跑首 PRD hand-off。

本 verdict 显式回应 K1 / K2 / K3 / K5+K7 / K6;K4 通过 V4=archive、idea_gamma2 / vibe-workflow / IDS=各按角色处置覆盖。

---

## Evidence map

每条 verdict 子结论 → 来源段落(verbatim quote ≤15 words,反对证据见 §"What this menu underweights"):

| 结论 | 来源 | 引用 | 反对证据 |
|---|---|---|---|
| V4 整体 archive,不作 ADP-next 继承对象 | P1-GPT §2 row 1 / P2-Opus §1 row 4 | "60% 无 AI-ready data 的项目会在 2026 被放弃" | - |
| IDS L4 设计假设错(IDS 仓无 Python infra/pyproject/pytest) | P1-Opus §1 Y1 + ADP-AUDIT §9 DRIFT-1 | "IDS 仓 0 Makefile / 0 pyproject.toml / 0 pytest" | - |
| ADP-next 不是补 process 文档,是建 production runtime | P2-GPT §1 row 5 + P3R1-Opus §1 | "目标方向没错,但 gap 是 harness 产品化" | - |
| XenoDev 直接对齐评估 fork Spec Kit 0.8.7 现行 schema | P2-GPT §1 row 3(修 Opus P2 "v2" 错) | "未发现 Spec Kit v2 正式版;latest 是 0.8.7" | ⚠ Opus P2 §1 row 1 原误写 "v2 已发布",P3R2 §1 分歧 1 已 closed |
| workspace 4 字段 schema 显式建模(working_repo 一等公民) | P2-GPT §1 row 2 / P3R2-GPT §1 分歧 3 | "正确方向是显式 workspace/schema,不是假装单仓" | ⚠ Opus P1 §3 Q3 原"通过物理位置消除",P3R2 §1 分歧 2 全让步 |
| reviewed-by 4 轮 → 1-2 轮 + Evaluator role | P2-Opus §3 row 1 | "4 轮 codex review 是过度收敛风险" | - |
| Eval Score / risk tier v0.1 留接口 + 不实装算法 | P3R2-Opus §1 分歧 4 + P3R2-GPT §1 分歧 4 | "v0.1 必落 append-only event schema,记三类事件" | - |
| 保留 "轻入口、重升级" 分级(K3 回应) | P3R1-GPT §3 row 5 + P3R2-Opus §1 分歧 5 | "W1/W2 必须显式保留'轻入口、重升级'" | ⚠ Opus P3R1 原倾向降级 v0.2,P3R2 全盘接受 GPT |
| Safety Floor 三件套(凭据隔离 + 不可逆 + 备份破坏检测) | P1-GPT §1 Y2 + P2-GPT §1 row 4 | "凭据隔离/备份检测是 hard floor" | - |
| sdd-workflow / task-decomposer 由 XenoDev schema 重新派生 | P2-GPT §3 row 5 + P3R2 双方分歧 2 | "C 不从 IDS 或 V4 自动 cp" | - |
| SHARED-CONTRACT v1.1.0→v2.0 双向(hand-off + hand-back) | moderator §三 + P3R1-GPT §3 row 3 | "必须含 workspace root / build repo / source PRD repo / hand-back target 四字段" | - |
| IDS specs/007a-pA 标 DEPRECATED 或物证(双 source 解决) | ADP-AUDIT §9 DRIFT-3 + P3R2-GPT §4 W3 模块 2 | "V4 tag v4-final,IDS specs/007a-pA 标物证或 deprecated" | - |
| 强制 forge 元层锁(防"想法变了→静默停") | moderator §四 + P3R1-Opus §4 K6 | "重大转向必须保留跨模型审阅" | - |
| B1 必须先 → B2(SOTA Spec Kit 强顺序) | P2-Opus §3 row 4 + P3R2-Opus §2 | "Spec Kit 4 phase 是强顺序,不能并行" | - |

---

## Intake recap

### X · 审阅标的(9 个,全部 reachable)

**ADP 仓 5 标的**(Δ-X1 至 Δ-X4 + v1#11 archive):
- `/Users/admin/codes/autodev_pipe`(顶层)
- `/Users/admin/codes/autodev_pipe/specs/v4/spec.md`(V4 frozen 7 元素 + reviewed-by 4 轮闭环)
- `docs/decisions/0008-v4-dogfood-path.md` + `0009-v4-scope-downgrade.md`(B 路径降级 C Hybrid)
- `.claude/skills/{sdd-workflow,task-decomposer}/SKILL.md`(port from IDS,L11 显式声明)
- `.claude/hooks/block-dangerous.sh`(23 pattern + python3 解析)

**IDS 本仓 4 标的**(Δ-X5 至 Δ-X7):
- `specs/007a-pA/{spec.md v0.3, HANDOFF.md}` + `.codex-outbox/queues/007a-pA/`(4 轮 R1-R4 review 闭环)
- `framework/SHARED-CONTRACT.md` v1.1.0 + `AUTODEV-PIPE-SYNC-PROPOSAL.md` v2 + `NON-GOALS.md`
- `framework/ADP-AUDIT-2026-05-08.md` §9 DRIFT-1 至 DRIFT-4 完整论证

**v1 X #1-#9 no-rerun**(operator §1 显式标定;expert 不读)

### Y · 审阅视角(3 项)
- 架构设计 — 模块切分、抽象层次、可演化性
- 工程纪律 — 测试、CI、SDD、code review、hook 机制
- Y5 重做代价 / 沉没成本 / 知识保留(L/P/C 分层)

(产品价值未勾。)

### Z · 参照系
- mode: 对标 SOTA
- 实际检索覆盖: Anthropic Skills/Agent SDK / Cursor 3 multi-root + worktrees / GitHub Spec Kit 0.8.7 / MSR 2026 agentic PR failure corpus / GPT-5.4 Codex / agentic coding abandonment 实证
- 外部材料叠加: moderator-notes.md(binding,P1+ 自动读)+ _x-input-draft-by-operator.md

### W · 产出形态(全选 6 项)
W1 verdict-only / W2 decision-list / W3 refactor-plan / W4 next-PRD(聚焦 XenoDev v0.1) / W5 next-dev-plan(B1+B2 双流) / W6 free-essay

### K · 用户判准(K1-K7)

K1-K6 verbatim from proposal §006:**给定 PRD,Claude Code 几乎无人工干预可靠完成开发**(K1)/ operator 非软件背景但能写 PRD(K2)/ 对各规模(大中小)开发没把握(K3)/ 4 个历史尝试(K4-K5)/ 达成基于 Claude Code 实现可靠自动化开发的 framework/pipeline 共识方案(K6)。

**K7**(operator Append 2026-05-09):ADP-next 是 framework "待生下半边"产物,V4 是物证(operator 半年前停掉的"半成品")**不是吸收对象**;K5 中"ADP 项目"实际指 ADP-next 的设计意图,而非 V4 这版具体实装。

### 收敛模式
**strong-converge**(operator 选择 + binding via moderator-notes §六);convergence_intent = "每个 W 都要有收敛主线 + v0.2 note 旁注,不暴力压扁分歧"。

---

## Verdict rationale(W1)

verdict 中心命题来自 GPT P2 §1 row 5 headline:**"目标方向没错,但 gap 是 harness 产品化,不是再补一份流程文档"**。SOTA 共同方向(Anthropic Agent SDK + Skills / Cursor 3 multi-root + worktrees / Spec Kit 0.8.7 spec-first / MSR 2026 失败实证)全部指向 **运行时 harness + 4-phase + 跨仓 workspace + 可观测 + 可学习**,而非更多 process 文档。

V4 archive 不是 sunk cost lose-it-all:V4 6 模块的 L(设计原则)+ P(范式结构)全保留作为 lesson(写入 XenoDev `~/.claude/lessons/`),C(代码)仅 cp `block-dangerous.sh`(纯工业共识 23 pattern,无 ADP-next 偏好);其他 sdd-workflow / task-decomposer 由 XenoDev 选定 schema 后重新派生,不从 IDS 或 V4 自动 cp(避免双 source-of-truth 陷阱,P2-GPT §3 row 5)。

DRIFT-1 是架构级证据,**颠覆 v1 隐性假设**(IDS 自带 L4 build):IDS 仓实证 0 Python infra,意味着 v1 verdict 的 "L1-L4 + forge 横切" 默认骨架失效。v2 重新画线 = IDS 只做 idea→PRD + 治理(forge / SHARED-CONTRACT / hand-back 接收),XenoDev 是唯一 L4 runtime — 这与 SOTA Spec Kit 4-phase 模式同构,与 Anthropic Planner/Generator/Evaluator 三角架构对齐(忌讳 shared context,artifact 间 hand-off)。

K3 "对各规模没把握" 的回应 = 显式继承 v1 "轻入口、重升级":Small 项目 operator 直驱 Claude Code 走 AGENTS.md + Safety Floor 轻入口,不强制 IDS forge / L1-L4 / XenoDev L4 全套;Medium/Large 才升级到 IDS+XenoDev 双仓全链。**这是 v1 仍站住的核心 lesson**(per moderator §四 "v1 verdict 仅参考但 lesson 可吸收"),不可丢。

---

## Decision matrix(W2)

针对 9 个 X 标的的 4 列处置矩阵(每行可在 §"Evidence map" 溯源):

| 类别 | 项 | 来源(X 标的具体位置) | 理由 | 优先级 |
|---|---|---|---|---|
| **保留** | v1 "轻入口、重升级" 分级哲学(Small/Medium/Large tier policy) | v1 stage doc + AGENTS §3 已实装 | K3 回应核心 lesson | P0 |
| **保留** | Safety Floor 三件套(凭据隔离 + 不可逆命令 + 备份破坏检测) | ADP `block-dangerous.sh` + P1-GPT §1 Y2 | hard floor 不可越,SOTA(MSR 2026)实证支持 | P0 |
| **保留** | sdd-workflow 7 元素 / PPV 思想(L+P 抽象,非 C) | ADP `specs/v4/spec.md` + sdd-workflow SKILL | L 设计原则 + P 范式结构有客观工程价值 | P0 |
| **保留** | forge 机制本身(双 expert + SOTA + Codex review + 收敛) | IDS `.claude/commands/expert-forge.md` + 现 v2 跑物证 | 防"想法变了→静默停"的元层锁 | P0 |
| **保留** | task-decomposer 9 字段思想 / file_domain 互斥 / 1-4h 原子单元 | ADP task-decomposer SKILL | L+P 同上 | P1 |
| **保留** | block-dangerous.sh 23 pattern(直接 cp 进 XenoDev) | ADP `.claude/hooks/block-dangerous.sh` | 纯 bash + python3 + 23 pattern 工业共识 | P0 |
| **调整** | SHARED-CONTRACT v1.1.0 → v2.0(双向 + workspace 4 字段) | `framework/SHARED-CONTRACT.md` | DRIFT-3/4 + Cursor multi-root SOTA + hand-back 闭环需要 | P0 |
| **调整** | IDS CLAUDE.md L24 "L4 = spec + tasks + parallel build + ship" 重写 | IDS `CLAUDE.md` | DRIFT-1 架构级修复 — IDS pipeline 改为 L1-L3 + 治理 | P0 |
| **调整** | plan-start v2 改产 hand-off 包(不再产 specs/) | IDS `.claude/commands/plan-start.md` | 与 SHARED-CONTRACT v2.0 + DRIFT-3 解决配套 | P0 |
| **调整** | reviewed-by 4 轮 → 1-2 轮 + Evaluator role | ADP `specs/v4/spec.md` reviewed-by | SOTA(Anthropic Evaluator pattern)推翻 4 轮过度收敛 | P1 |
| **调整** | retrospective skill / lessons/ user scope 不直接继承,XenoDev 真 dogfood 后回炉 | ADP retrospective skill | V4 dogfood 12 周 0 次跑过 = 未实证 | P2 |
| **删除** | V4 整体作为 ADP-next 继承对象(打 `v4-final` archive,不再维护) | `/Users/admin/codes/autodev_pipe` 全仓 | K7 显式 reframe + operator 已停止维护 | P0 |
| **删除** | IDS `specs/007a-pA/` 作为 build spec source(标物证或 deprecated) | IDS `specs/007a-pA/` | DRIFT-3 双 source-of-truth 解决 | P0 |
| **删除** | "Spec Kit v2 已发布" 假设(改为 0.8.7 现行版) | (无 — 修正 Opus P2 事实错) | GPT P2 §1 row 3 验证 latest 是 0.8.7 | P0 |
| **删除** | autodev_pipe-cli build / Makefile target 假设(IDS 端) | IDS `AGENTS.md` §4/§5 | SHARED-CONTRACT v1.1 audit 已实证全错 | P0 |
| **删除** | "L1-L4 + forge 横切 = framework 默认骨架" 隐性假设 | v1 verdict 隐性假设 | DRIFT-1 颠覆;IDS 不带 L4 build | P0 |
| **删除** | V4 12 周 dogfood 作为前置条件 | ADR 0008/0009 | V4 已 archive,checkpoint 03 永不出 | P0 |
| **新增** | XenoDev 仓(`/Users/admin/codes/XenoDev`,git init) | (新建) | ADP-next 物理载体 | P0 |
| **新增** | 反向 hand-back 通道(XenoDev → IDS;`discussion/<id>/handback/<ts>.md`) | moderator §三 + P2-GPT §1 row 4 | 闭环 = 可靠自动化 K1 必要条件 | P0 |
| **新增** | workspace schema 4 字段(`source_repo` / `build_repo` / `working_repo` / `handback_target`) | DRIFT-4 + Cursor multi-root SOTA | 跨仓建模一等公民 | P0 |
| **新增** | Eval/risk 数据接口(append-only event log;3 类 event) | P3R2 双方分歧 4 折中 | 可学习闭环;不实装算法 | P0 |
| **新增** | 强制 forge 元层锁(IDS = 治理 + 评判仓;XenoDev = 执行仓不复制 forge) | moderator §四 | 防"想法变了→静默停"V4 失败模式 | P0 |
| **新增** | hand-back 包三标签结构(drift / PRD-revision-trigger / 实践统计) | moderator §三 + Cursor 异步 subagent return 同构 | 结构化反馈,非 free-text | P1 |

---

## Refactor plan(W3)

按模块分组(模块来自 IDS 协议层 + ADP 物证库 + 跨仓接口):

### 模块 A · IDS framework 协议层(B1 流)

- **当前问题**:
  - DRIFT-1 架构级:IDS CLAUDE.md L24 假设有完整 SDD 工具链,实证 0 Python infra(P1-Opus §1 Y1)
  - DRIFT-3 双 source:IDS specs/007a-pA + ADP 也产 13 task(P1-GPT §1 视角 A)
  - SHARED-CONTRACT v1.1.0 缺反向 hand-back 通道(operator Q9 否决单向方案)
- **目标态**:
  - IDS 角色 = idea→PRD(L1-L3) + governance/forge + 双向 hand-off/hand-back 接收方
  - SHARED-CONTRACT v2.0(major bump,breaking change):正向 PRD 包 + 反向 hand-back 包(drift / PRD revision / 实践统计三类) + workspace 4 字段
  - plan-start v2 不再产 `specs/`,只产 hand-off 包给 XenoDev
- **改造步骤**(顺序):
  1. 写 SHARED-CONTRACT v2.0 草稿(workspace 4 字段 + hand-back 三标签 schema)
  2. 改 IDS CLAUDE.md L24 "L4 = ..."  → "L4 委托给 XenoDev,IDS 仅产 hand-off 包"
  3. 重写 plan-start.md 命令(产 `discussion/<id>/<prd>/L4/HANDOFF.md` 而非 `specs/`)
  4. 改 AGENTS.md §4/§5 旧 `autodev_pipe-cli build` / Makefile 引用
  5. specs/007a-pA 标 DEPRECATED(物证保留,不删但禁新写)
  6. 加 hand-back 接收路径:`discussion/<id>/handback/<ts>.md` + 模板
- **风险**:
  - 现有 plan-start 输出格式被 007a-pA pilot 实测过,改后需重测 hand-off 链路(R 风险中)
  - SHARED-CONTRACT major bump 影响所有未来 idea(R 风险高,但必做 — DRIFT-1 不可逆)
- **预估代价**:M(1-2 周;operator §6.7 不设上限,此为节奏参考)

### 模块 B · XenoDev 启动(B2 流)

- **当前问题**:不存在(XenoDev 是新建仓)
- **目标态**:
  - 新仓 `/Users/admin/codes/XenoDev`,git init,定位 = "ADP-next 的运行时 harness"
  - 单一 L4 build runtime(PRD → spec → task → parallel build → ship)
  - v0.1 落 5 件:Safety Floor 三件套 / 单一 build spec source / workspace schema / hand-back 包 / Eval 数据接口
  - 不复制 IDS forge 机制(由 IDS 治理仓集中管)
- **改造步骤**(顺序;B1 模块 A 完后才能跑):
  1. git init + AGENTS.md(参考 IDS 但聚焦 L4)+ CLAUDE.md(项目 constitution)
  2. cp `block-dangerous.sh` from V4(纯工业共识,无定制)
  3. 加 Safety Floor 第 2 件:凭据隔离(`.env` + secrets 物理隔离 + 检测)
  4. 加 Safety Floor 第 3 件:备份破坏检测(snapshot + diff 模式,SOTA Cursor + Claude 9 秒删库案例反例)
  5. 评估 fork Spec Kit 0.8.7 现行 schema(adapter 模式优先,fork 整 repo 次选;v0.2 note 1)
  6. 实装 workspace schema 4 字段(`source_repo` / `build_repo` / `working_repo` / `handback_target`)
  7. 实装 spec/task skill(由 XenoDev schema 重新派生,不从 IDS port)
  8. 实装 Eval append-only event log(3 类 event:review failures / operator interventions / hand-back drift)
- **风险**:
  - Spec Kit 0.8.7 与 PPV 第 7 元素兼容度未知(v0.2 note 1 标记)
  - 新仓 bootstrap 工程量被低估(SOTA 多次实证 abandonment 风险)
- **预估代价**:L(2-4 周到 v0.1 ship,operator §6.7 不设上限)

### 模块 C · 跨仓双向 hand-back 协议(B1/B2 共用)

- **当前问题**:
  - 当前只有正向 hand-off(IDS → ADP);operator Q9 否决单向方案(无闭环)
  - DRIFT-4 emergent `working_repo` 字段未显式建模
- **目标态**:
  - SHARED-CONTRACT v2.0 § "workspace schema" 显式 4 字段(Cursor multi-root 范式)
  - hand-back 包 3 标签:drift(类似 §9 4 drift 反馈) / PRD-revision-trigger(L3 PRD 不够细的问题) / 实践统计(N idea ship 后的成功率/干预率)
  - IDS 接收路径:`discussion/<id>/handback/<ts>.md`
- **改造步骤**:
  1. 设计 hand-back 包 schema(YAML frontmatter + Markdown body + 必填字段)
  2. XenoDev 端写 hand-back 生成器(每个 task ship 后自动产)
  3. IDS 端写 hand-back 消费器(写入 `discussion/<id>/handback/`)
  4. operator manual 验证 round-trip(B1 + B2 完成后)
- **风险**:hand-back 包 schema 在第一次真 ship 后可能需 v0.2 调整(标记 v0.2 note 4)
- **预估代价**:S(嵌入 B1 + B2,无独立工时)

---

## Next-version PRD draft(W4 — XenoDev v0.1)

**注**:此 PRD 草案来自 forge 已验证事实(双方 P3R2 §4 W4 草稿合一),非 daydream。operator 在 B2.1 阶段需手补 §"Real constraints" + §"Open questions"(1-2h)再进 XenoDev L4。

```
# PRD · XenoDev v0.1

**Status**: Draft from forge 006 v2, awaiting operator approval + Real constraints append
**Sources**: forge stage-forge-006-v2.md + moderator-notes §一/§三/§五

## User persona
能写 PRD 但**非软件背景**的 operator(Yashu Liu)。痛点:对各规模(大中小型)开发的方案、流程、规范没有把握(K2+K3)。
不熟悉:spec/task 拆解、parallel build 编排、跨仓 hand-off 协议细节。
熟悉:idea 描述、PRD 写作、读 stage 文档、做拍板决策。

## Core user stories
- US-1:operator 在 IDS 完成 PRD 后,触发 hand-off 进 XenoDev,**几乎不需要手工转写**(K1)
- US-2:XenoDev 自动拆 spec → tasks → parallel build → ship,operator 仅在 hand-back / 重大决策时介入
- US-3:Small 项目可绕过 XenoDev 完整 L4(直驱 Claude Code + AGENTS.md + Safety Floor 轻入口),Medium/Large 才走全链(K3)
- US-4:每次 build 完产 hand-back 包,operator 在 IDS 看到反馈(drift / PRD gap / 统计)
- US-5:任何高风险破坏性操作被 Safety Floor 阻断,留人审

## Scope IN(v0.1 必落 5 件)
- IN-1:Safety Floor 三件套(凭据隔离 + 不可逆命令 block-dangerous.sh + 备份破坏检测)
- IN-2:单一 build spec source(在 XenoDev,对齐评估 fork Spec Kit 0.8.7 现行 schema + 自带 PPV 扩展)
- IN-3:workspace schema 4 字段一等建模(`source_repo` / `build_repo` / `working_repo` / `handback_target`)
- IN-4:hand-back 包结构化(drift / PRD-revision-trigger / 实践统计三类标签)
- IN-5:Eval/risk 数据接口(append-only event log,记 review failures / operator interventions / hand-back drift)

## Scope OUT(显式 non-goals)
- OUT-1:**不**做 SaaS / 多用户(operator 单人;evidence: P3R2-GPT §4 W4)
- OUT-2:**不**做完整 Eval scoring 算法 / risk tier verdict / 阈值数字(v0.2 note 2)
- OUT-3:**不**继承 V4 repo 任何 code(L+P 作为 lesson,C 仅 cp block-dangerous.sh)
- OUT-4:**不**复制 forge 机制(forge 在 IDS 治理仓集中管;moderator §四)
- OUT-5:**不**支持 Small 项目走完整 L4 全链(Small 走轻入口;K3 + W2 tier policy)

## Success looks like
- 跑通 ≥1 真实 PRD 的 small/medium task build → ship → hand-back 完整 round-trip
- 所有高风险破坏性操作被 Safety Floor 阻断(0 漏)
- operator 干预率 < X%(具体 X 由 v0.2 note 2 定;v0.1 仅记录原始 event,不算阈值)
- hand-back 包格式 operator 可读可消费(主观评分 ≥ 7/10)

## Real constraints(operator 手补,1-2h L3)
- 时间:operator §6.7 不设上限,但 v0.1 ship 节奏参考 = 2-4 周(B2 全部 milestone)
- 预算:operator 单人 + Claude Code subscription(无云成本预算)
- 平台:macOS / git / Claude Code CLI
- 合规:无外部用户 → 隐私合规 N/A;但凭据隔离仍是 Safety Floor 必备

## UX principles
- operator 主动介入越少越好(K1)
- 失败时 hand-back 必显式说明 root cause + 建议(不让 operator 猜)
- 高风险时显式拒绝(hard block)而非提示(防 9 秒删库)

## Open questions(forge 也没解决的)
- OQ-1:成功指标 N(连续 idea 数)和干预率 X 的具体阈值 — 需 XenoDev 跑 ≥3 真 idea / 30 task 后回看(v0.2 note 2)
- OQ-2:Spec Kit 0.8.7 schema 与 PPV 第 7 元素兼容度 — XenoDev 第一个真 PRD 起 sdd-workflow 时回看(v0.2 note 1)
- OQ-3:Small → Medium 升级触发器精确判准(代码行 / 工时 / 跨仓需求 / 等) — XenoDev 跑过 ≥1 Medium 项目后回看(v0.2 note 5)
```

---

## Next-version dev plan(W5 · B1 + B2 双流)

按 phase / milestone 切。**B1 必须先完成才能跑 B2**(SOTA Spec Kit 4-phase 强顺序,P2-Opus §3 row 4)。**不到 spec 级**(spec 是 XenoDev L4 spec-writer 的工作)。

### B1 流 · IDS framework 优化(预估 1-2 周)

- **目标**:IDS 退回 idea→PRD + governance + hand-off/hand-back;停止产 build spec
- **Milestone M1**:SHARED-CONTRACT v2.0 ship
  - 写 v2.0 草稿 + workspace 4 字段 schema + hand-back 3 标签 schema
  - 与 v1.1.0 的 breaking change 标注完整
- **Milestone M2**:IDS CLAUDE.md L24 + AGENTS §4/§5 + plan-start v2 ship
  - CLAUDE.md L24 "L4 = ..." 改为 "L4 委托 XenoDev"
  - AGENTS §4/§5 删 `autodev_pipe-cli build` / Makefile 引用
  - plan-start v2 改产 `discussion/<id>/<prd>/L4/HANDOFF.md`,不再产 `specs/`
- **Milestone M3**:specs/007a-pA 标 DEPRECATED + hand-back 接收路径就位
  - specs/007a-pA/README.md 加 DEPRECATED 标记(物证保留)
  - `discussion/<id>/handback/` 目录模板就位
- **依赖**:无(可立即启动)
- **风险**:plan-start v2 改后 007a-pA pilot 链路需重测(中)
- **B1 完成 = M1 + M2 + M3 全 ship**

### B2 流 · XenoDev L4 启动(预估 2-4 周;B1 完后才能跑)

- **目标**:XenoDev v0.1 ship,跑通首个真 PRD 的 hand-off → first task → hand-back 完整 round-trip
- **Milestone M4 (B2.1)**:operator 手补 PRD Real constraints
  - 在 IDS 给 forge v2 §"Next-version PRD draft" 加 §"Real constraints" + §"Open questions"
  - 1-2h 手工 L3,不走 IDS 完整 L1-L3 流程(per moderator §五 第一性事实)
- **Milestone M5 (B2.2)**:XenoDev 仓 bootstrap
  - git init `/Users/admin/codes/XenoDev`
  - cp PRD 进 `XenoDev/PRD.md`
  - 加 AGENTS.md + CLAUDE.md(参考 IDS 但聚焦 L4)
  - cp `block-dangerous.sh` from V4(纯工业共识)
- **Milestone M6 (B2.3)**:Safety Floor 三件套 + workspace schema 实装
  - 凭据隔离机制(`.env` 物理隔离 + 检测脚本)
  - 备份破坏检测(snapshot + diff)
  - workspace schema 4 字段实装(JSON schema + 校验)
- **Milestone M7 (B2.4)**:单一 build spec source(对齐评估 fork Spec Kit 0.8.7)
  - 评估 fork 整 repo vs adapter 模式(v0.2 note 1)
  - spec/task skill 由 XenoDev schema 重新派生(不从 IDS port)
- **Milestone M8 (B2.5)**:Eval append-only event log + 第一个真 PRD task ship
  - event log schema(3 类 event)+ append-only API
  - 跑通首个 task build → ship
- **Milestone M9 (B2.6)**:hand-back 闭环验证
  - XenoDev 第 1 个 task ship 后产 hand-back 包返 IDS
  - operator 验证 hand-back 可读可消费(主观评分)
- **依赖**:B1 全完成(SHARED-CONTRACT v2.0 + plan-start v2)
- **风险**:Spec Kit fork 边界(v0.2 note 1)/ Eval scoring 算法未定(v0.2 note 2)/ 升级触发器未定(v0.2 note 5)— 这些都标 v0.2 note,v0.1 不阻塞
- **B2 完成 = M4 + M5 + M6 + M7 + M8 + M9 全 ship**

### v0.2 note(残余分歧旁注,不阻塞 B1+B2)

- **v0.2 note 1**:Spec Kit fork 精确边界(adapter vs fork 整 repo)— XenoDev 第一个真 PRD 起 sdd-workflow 时决
- **v0.2 note 2**:Eval Score scoring 算法 + N + 干预率 X 阈值 — 累计 3 个真 idea 或 30 个 task 后定
- **v0.2 note 3**:risk tier 与 PPV 关系(独立第 8 元素 vs 嵌 PPV)— 出现第一次 High-risk hand-back 时定
- **v0.2 note 4**:retrospective/lessons 机制处置 — XenoDev 完成第一轮 ship retrospective 后定
- **v0.2 note 5**:Small → Medium 升级触发器精确判准 — XenoDev 跑过 ≥1 Medium 项目后定

---

## Long-form synthesis(W6,800-1500 字)

### 论点一 · V4 失败不是代码失败,是元层转向无锁导致的沉没

ADP V4 自 2026-04-29 起约 1 周工程量,reviewed-by 4 轮闭环 + ADR 0008/0009 双向链接齐全 — **代码层面工程纪律没问题**。V4 失败的真因是 operator 半年前"想法变了 → 静默停 → 沉没",且没有任何机制把这次"想法转向"显式锁住(没有 forge / 没有 cross-model review / 没有 retrospective 强制 trigger)。这与 SOTA 实证(2026 "60% 无 AI-ready data 项目会被放弃")完全吻合 — 不是工程问题,是治理问题。

v2 verdict 的核心治理机制是 **强制 forge 元层锁**:任何重大架构转向(架构级 / 重大重构 / 重大想法转向)必须在 IDS 仓走 `/expert-forge`,XenoDev 不复制此机制。这把 IDS 重新定义为 **治理 + 评判仓**,XenoDev 是 **执行仓**。这个分工解决了 V4 失败模式 — 下一次 operator 想法转向时,先跑 forge,不再静默停。

### 论点二 · SOTA 共同方向是运行时 harness,不是更多 prompt

12 次 SOTA 检索(Anthropic Skills/Agent SDK / Cursor 3 multi-root + worktrees / Spec Kit 0.8.7 / MSR 2026 失败实证 / GPT-5.4 Codex / agentic abandonment 实证)全部指向同一方向:**运行时 harness + 4-phase + 跨仓 workspace + 可观测 + 可学习**。Anthropic 4 月公布 Planner/Generator/Evaluator 三角架构(structured artifact 而非 shared context)是 production-validated pattern;Cursor 3 的 multi-root + worktrees + async subagent 把跨仓 build 做成一等能力;Spec Kit 0.8.7 spec-first 范式 + 4 phase 强顺序 = 已成主流共识。

V4 sdd-workflow + reviewed-by + PPV 在抽象层面与 SOTA 同构(L+P 全保留),但 V4 没有运行时 harness 这个核心壳层 — operator 当时也没意识到这是核心 gap。GPT P2 §1 row 5 一针见血:**"目标方向没错,但 gap 是 harness 产品化,不是再补一份流程文档"**。这是 v2 verdict "新建 XenoDev 仓而非补 V4" 的根本理由。

XenoDev v0.1 必落的 5 件(Safety Floor / 单一 build spec / workspace schema / hand-back / Eval 接口)中,**前 4 件都是 harness 层**;只有最后一件 Eval 接口是数据层(且 v0.1 只留接口不实装算法)。这个权重分配明确表达 v2 verdict 的优先级:harness 第一,统计第二。

### 论点三 · 可靠自动化要靠双向学习闭环,所以 hand-back 是 ADP-next 的核心产品特性

K1 verbatim "**可靠的、自动化程度最高解决方案**" 中的 "可靠" 是头条优先级;"自动化程度最高" ≠ full-auto。MSR 2026 agentic PR 失败实证(33k agent PR 失败研究 / 被 revert 的 AI changes / 测试失败 / 安全问题 / 可读性 / 理解性)给出的统一启示是:**没有 hand-back 闭环,agent 自动化做得越快越危险**。

v2 verdict 的 hand-back 通道(XenoDev → IDS,3 标签:drift / PRD-revision-trigger / 实践统计)不是工程附属功能,而是 **产品级核心特性**:operator 在 IDS 看到 build 反馈,IDS L3 PRD 阶段下次写 PRD 时知道该补什么 / 哪些约束被 build 阶段证伪 / 哪些 idea 类型成功率低不该再起。这形成 idea→PRD→build→ship→hand-back→idea 的闭环 — 也是 v1 verdict "Learning Loop"(retrospective + eval 回写)在 v2 的具体物化。

operator §6.1 verbatim "**ADP-next 只保障稳定、可靠、高质量、产品级的开发**" 的 4 个形容词都指向 hand-back 闭环 — 没有反馈,稳定 / 可靠 / 质量都是断言不是事实。Cursor 3 异步 subagent 的 "主进程汇总" pattern 给了同构参考(主线 = IDS 治理 + 汇总 / 各 subagent = XenoDev L4 任务),Anthropic Evaluator agent role 给了 "独立质量评估" 同构参考。这些 SOTA 模式都指向同一答案:**hand-back 是闭环可靠性的硬条件,不是可选 feature**。

### 综合

v2 与 v1 的 framing 区别可以浓缩为一句:**v1 是设计 framework,v2 是建 production runtime**。v1 verdict "分级 harness framework" 是哲学骨架,v2 verdict "新建 XenoDev + IDS 退回治理 + 双向 hand-back" 是落地物化。v1 的 "轻入口、重升级" 在 v2 K3 处理时显式继承(GPT P3R1 §3 row 5 强约束 + Opus P3R2 §1 分歧 5 全盘接受),证明 v1 的哲学骨架仍站住。但 v1 28 项 L/P/C 矩阵被 §9 4 实证 drift + K7 reframe 颠覆,**v2 重新画线** = IDS 角色变窄(idea→PRD + 治理),XenoDev 角色生成(唯一 L4),跨仓接口升级(SHARED-CONTRACT v2.0 双向)。

未来 3-6 月可能的演化路径:B1 (1-2 周) → B2 (2-4 周) → 第一个 hand-back 闭环验证(operator 主观评分)→ 跑 ≥3 真 idea / 30 task → v0.2 决定 Eval scoring 算法 + N/X 阈值 + Spec Kit fork 精确边界 + Small→Medium 升级触发器 + retrospective/lessons 机制处置(5 条 v0.2 note 全部回头看时机)。如果 hand-back 闭环数据 6 个月后显示 IDS PRD 质量未提升 / operator 干预率未下降,**触发 v3 forge** 重审 verdict。

---

## What this menu underweights(强制自批判)

诚实表述本 stage 文档可能 underweight 的点:

- **反对证据未充分整合**:
  - Opus P2 原写 "Spec Kit v2 schema" 是事实错误(SOTA latest 是 0.8.7,GPT P2 §1 row 3 修正);P3R2 §1 分歧 1 已 closed 但残余风险 = stage 文档其他位置如还有"Spec Kit v2"残留措辞需 grep 校验
  - Opus P1 §3 Q3 原立场"通过物理位置消除 working_repo"已被 GPT P2/P3R1 推翻并在 P3R2 §1 分歧 2 全盘让步 — 主 verdict 采纳 GPT 立场是正确的,但 Opus 原立场代表"减少跨仓复杂度"的合理担忧,XenoDev v0.1 实装 workspace schema 时如出现实施复杂度爆炸,需回看
  - Opus P3R1 原倾向把 K3 "轻入口、重升级" 降级 v0.2 note,P3R2 §1 分歧 5 全盘接受 GPT — 主 verdict 显式继承是正确的,但 Opus 原担忧 = "K3 与 W4/W5 聚焦 XenoDev 冲突",需在 B1+B2 实施时确认 W2 tier policy 不被实施细节稀释
- **Y 视角覆盖盲区**:
  - **产品价值视角未选**(operator 三屏多选时未勾)— 但 K1 verbatim 是产品诉求("可靠的、自动化程度最高解决方案");verdict 隐式回应了产品价值(hand-back = 产品核心特性)但未做完整产品价值对标(如:对其他单人 operator 可移植性 / 学习曲线 / 文档负担)
  - **安全视角未独立选**,但 Safety Floor 三件套通过 Y2 工程纪律间接覆盖 — 凭据隔离 / 不可逆命令 / 备份破坏检测的具体实装细节(如凭据隔离的 OS-level vs application-level)未深挖
  - **教学价值视角未选**,但 K2+K3(operator 非软件背景 + 对各规模没把握)实质是教学诉求 — verdict 回应了 K2/K3(IDS 接 PRD + 轻入口)但未深挖"operator 在使用 XenoDev 过程中能学到什么"
- **K 中未充分回应的关切**:
  - K2 "operator 非软件背景但能写 PRD" 在 verdict 中通过 "IDS 接 PRD + XenoDev 接管 SDD 复杂度" 回应,但**XenoDev hand-back 包结构如何让非软件背景 operator 可读可消费** = v0.1 ship 后才能验证,目前是断言
  - K6 "共识方案" 在 verdict 中通过 IDS+XenoDev+contract+forge 4 件套形成,但**这是双 expert + operator 三方的共识,与"软件开发 community 的共识"不是同一个东西** — SOTA 对标可作为社区共识代理,但 12 次搜索仍是有偏 sample
- **convergence_mode 副作用**:
  - strong-converge 让双方在 P3R2 主动收敛,P3R1 §3 5 条分歧全部 closed/accepted 看起来"完美" — 但回声室强化错误的风险存在,以下是双方都同意但可能错的判断:
    - **"XenoDev 仓建在 `/Users/admin/codes/XenoDev`"** = 双方默认 operator 接受新建一仓的工程开销(B2 至少 2-4 周),但未充分论证 "改造 V4 + rebrand 为 XenoDev" 是否更省工时(operator §四已显式排除该选项,但选项本身值得 v0.2 留 note 验证)
    - **"hand-back 包 3 标签结构"** = 双方默认结构化优于 free-text,但 operator 第一次读 hand-back 包时可能反馈"过度结构化伤可读性",需 M9 milestone 真验证
- **X 标的覆盖局限**:
  - 未读 ADP V4 的 12 周 dogfood 实际跑过的部分(operator 决议不再跑;但 V4 已跑的部分若有 retrospective 数据会推翻 "V4 dogfood 12 周 0 次跑过 = 未实证" 这条)
  - 未读 Cursor 3 的实际 multi-root 实施细节(只读了 changelog),workspace schema 4 字段是否真能映射 Cursor 范式未深验
  - 未读 IDS 当前所有 commands 的完整链路(只读了 plan-start.md),改 plan-start v2 后是否有其他命令链路被破坏未全扫
- **forge versioning 提示**:以下信息进入会触发 v3:
  - B1+B2 ship 后第一次 hand-back 闭环验证失败(operator 主观评分 < 7/10)
  - XenoDev 跑 ≥3 真 idea 后 operator 干预率 > 50%(意味着自动化失败)
  - SOTA 出现新主流方向(如 Anthropic 发布 Skills SDK v2 真版本 / Spec Kit v2 真发布 / 新 agentic harness 范式)
  - operator 想法发生重大转向(per moderator §四 元层锁触发条件)

---

## Decision menu(for human)

### [A] 接受 verdict,拆 B1+B2 双流推进(operator §五 第一性结论的标准路径)

```
注:本 verdict 不直接进 IDS L4(IDS 无 L4 build,DRIFT-1 已证实)。
正确流程:
1. operator 拆 B1(IDS 优化)+ B2(XenoDev L4)双流
2. B1 必须先(SOTA 强顺序):按 §"Refactor plan 模块 A" + §"Next-version dev plan B1 流" M1-M3
3. B2 在 B1 完成后启动:按 §"模块 B" + §"B2 流" M4-M9
4. B2.1 (M4) 时 operator 手补 §"Next-version PRD draft" 的 §"Real constraints" + §"Open questions"(1-2h)
5. cp PRD 进 `XenoDev/PRD.md`,XenoDev 走自己的 L4
6. 第一个 task ship 后 hand-back 反馈回 IDS(SHARED-CONTRACT v2.0 反向通道)
```

⚠ **不**走 `/plan-start <prd-fork-id>`(那个命令产 IDS L4 spec/task,与 v2 verdict 冲突)。
⚠ **不**重走 IDS L1-L3(冗余,L1-L2 已被 forge 覆盖,per moderator §五)。
⚠ **不**另起 idea 008 / forge 008(forge 006 v2 已是 ADP-next 的 forge)。

### [B] 跑 forge v3(说明需要补什么)

```
/expert-forge 006
# Phase 0 intake 时调整 X / Y / Z / W / K
# v2 整目录保留作历史参考
```

适用:
- 读完后觉得 verdict 对 K2/K6 回应不够(产品价值视角未补)
- 觉得 W4 PRD 草案不够细(operator 还想要更多 PRD 子节)
- 觉得 SOTA 12 次检索 sample 太小(想加 X 标的:更多 agentic coding 工具 / 真实 dogfood 数据)
- 想在 v3 加入 "改造 V4 + rebrand 为 XenoDev" 路径作为对照(operator §四已排除,但 v0.2 留 note)

### [C] 局部接受

列出哪几条采纳、哪几条挂起:
- ✅ 采纳:V4 archive + IDS 退回 idea→PRD + 强制 forge 元层锁 + 保留 "轻入口、重升级"(这 4 条是 v2 共识硬底)
- ⏸ 挂起:XenoDev 仓物理位置(`/Users/admin/codes/XenoDev` vs 其他路径) / Spec Kit fork 精确边界(等 v0.2 note 1) / Eval scoring 算法(等 v0.2 note 2)
- ❌ 拒绝:暂无(双方 P3R2 主线无显式拒绝项;若有 = 需触发 v3)

### [P] Park

```
/park 006
```

保留所有 forge 产物 + v2 verdict,标记暂停。复活时不重做 forge,从 §"Next-version dev plan" B1+B2 直接开始。
适用:operator 接下来 1-2 周专注其他 idea,XenoDev 启动延后。

### [Z] Abandon

```
/abandon 006
```

forge verdict 显示 ADP-next 不该继续做。归档 lesson 文档。
**注**:本 verdict 不支持 abandon(双方 P3R2 主线明确给 redesign by new repo;abandon = 实际放弃 K1/K6 共识方案);若 operator 选 [Z],需在 lesson 文档显式记录"为何放弃达成 K6 共识方案"。

---

## Forge log

由 `/expert-forge` 命令更新;记录每次 forge run 的 v 序列 + 关键 verdict 一句话。

- **v2** (2026-05-09): verdict = "新建 XenoDev 仓作为 ADP-next 运行时 harness;V4 archive;IDS 退回 idea→PRD + governance/forge + SHARED-CONTRACT v2.0 双向 hand-off;保留 v1 '轻入口、重升级' 分级"。Convergence: converged(strong-converge,双方 P3R2 完全合一,5 R1 分歧全 closed/accepted,5 v0.2 note 旁注)。
- **v1** (2026-05-08): verdict = "构建基于 Claude Code 的分级 harness framework — 轻入口、重升级"。Convergence: converged-with-tempo-options(实际单一 verdict + 节奏 A/B 旁注)。**v2 verdict 颠覆 v1 隐性假设(IDS 自带 L4 build),但继承 v1 哲学骨架(轻入口、重升级)**。
