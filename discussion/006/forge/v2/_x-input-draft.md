---
doc_type: forge-v2-x-input-draft
forge_id: 006
forge_target_version: v2
generated: 2026-05-09
status: ADP-next 已通过 12 问收敛(2026-05-09);operator 仍可补订
upstream:
  - discussion/006/forge/v1/forge-config.md (v1 X / Y / Z / W / K / convergence_mode 来源)
  - discussion/006/forge/v1/stage-forge-006-v1.md (v1 verdict + decision-list + refactor-plan)
  - discussion/006/forge/v1/sanity-check-v2-2026-05-08.md (v2 显式触发条件 L226-236)
  - framework/ADP-AUDIT-2026-05-08.md (§9 4 实证 drift + W0 收官 Milestone)
purpose: 在跑 /expert-forge 006(v2)前,沉淀 v1 verdict 之后的事实变更 + 隐性 K 变更 + ADP-next 角色重定义
non_purpose: 不是 forge v2 verdict / 不是 v2 forge-config.md / 不是 stage doc;是 v2 跑前的输入材料
---

# forge 006 v2 · X 输入草稿(v2 跑前的输入材料)

## §0 · 本文件用途

本文件**不是** forge 输出,**不是** v2 verdict,**不是** v2 forge-config.md,**不是** stage doc。

本文件**是** operator 在 v2 真跑前给两个 expert(Opus 4.7 / GPT-5.5 xhigh)看的"自 v1 verdict 以来发生了什么"清单,作用 3 重:

1. 给 prefill 阶段算 `x_hash` 时纳入新 X 标的(避免 v2 沿用 v1 x_hash `e45d68ee6dcc74d2c667976a28940c91`,见 v1 forge-config.md L8)
2. 给 P1 阶段两个 expert 提供"v1 verdict 之后的事实"作为审阅起点(避免 expert 重读 v1 已审过的标的)
3. 给 operator 自己作为"什么时候真跑 v2 / 跑 v2 时填什么"的判断依据

**v2 真跑路径**:operator 跑 `/expert-forge 006` → expert-forge.md Step 0.2 检测到 v1/ 已存在 → 起 v2 / 自动 mkdir v2/ / 跑 prefill。本草稿的 §1-§7 内容由 operator 在 prefill 阶段粘进 v2/forge-config.md 对应字段;本文件以 `_<purpose>-draft.md` 命名(同 v1/_prefill-draft.md 命名约定)区分于 v2 真产物。

---

## §1 · v1 verdict 仍站得住的部分(no-rerun)

依据(均见 stage-forge-006-v1.md):

- **哲学骨架**(L41-47 verdict + L125-133 三论证):"基于 Claude Code 的分级 harness framework,轻入口、重升级"+ 三层可靠(Safety Floor / Deterministic Feedback / Learning Loop)
- **§2 decision-list 的 L 级 lesson 大部分**(L182-211 + sanity-v2 印证):AGENTS.md 作为根上下文 / Skills 降级为过程插件 / 跨模型 review / Safety Floor 三件套设计原则 / SSOT 状态机 / 默认怀疑 / no-numbers-no-recommendation
- **K 子条 K1 / K2 / K3 / K4 / K6 字面 + grounding**:全部不变(见 forge-config.md L93-107 verbatim;K6"达成 framework/pipeline 共识方案"目标未变)
- **X 标的 #1-#9**:proposal text §006 / idea_gamma2 全栈 / vibe-workflow 全栈(共 9 个)状态自 v1 跑(2026-05-07)起未发生显著变化;**v2 不重审这 9 项**
- **NG-1 / NG-2 / NG-3 / NG-4 / NG-5 / NG-6**:7 NON-GOAL 中 6 条与 ADP 角色无关,sanity-v2 已实证仍对(framework/NON-GOALS.md 不动)

**v2 跑前的指令**:不要求 expert 重审上述项(节省 token / 避免摇摆 v1 已收敛结论)。expert P1 应基于 v1 stage doc + 本草稿,直接进入"自 v1 以来发生什么"的审阅。

---

## §2 · v1 X 标的的变更清单(v2 必须重审)

v1 X 共 11 标的(见 forge-config.md L25-37)。v2 需重审的只有 #10 / #11 两项(均关于 ADP):

| v1 X # | 原描述(v1) | 自 v1 以来发生什么 | 来源证据 |
|---|---|---|---|
| #10 ADP 仓库顶层 `/Users/admin/codes/autodev_pipe` | v3.1 设计稿 + STARTER_KIT.md(35 项清单)| **v3.2 frozen** (2026-04-29 port stroller 五件套) → **v3.3 frozen** (2026-05-06 codex 真审) → **v4 frozen** (代码层 2026-05-06,12 周 dogfood 起点) → **ADR 0008/0009** (B 真外部 → C Hybrid 路径修正) → **next_draft §3 三方共同盲区** | sanity-check-v2-2026-05-08.md §"关键发现" L19-35 + ADP-AUDIT-2026-05-08.md §1.1 / §1.4 |
| #11 ADP `/Users/admin/codes/autodev_pipe/solo_ai_pipeline_v3.1.md` | 63 章节级总设计文档 | 已被 v3.2-v4 spec.md 系列接替;v3.1 文档仍存但作为历史 archive 使用 | 同上 |

**v2 真跑时 X 段落应增补的"v1 后增量"**:

| 增量 X 标号 | 内容 | 路径 |
|---|---|---|
| Δ-X1 | autodev_pipe v4 spec.md(冻结代码层 + 12 周 dogfood 起点) | `/Users/admin/codes/autodev_pipe/specs/v4/spec.md` |
| Δ-X2 | ADP ADR 0008/0009(V4 dogfood 路径决策) | `/Users/admin/codes/autodev_pipe/docs/decisions/0008-v4-dogfood-path.md` + `0009-v4-scope-downgrade.md` |
| Δ-X3 | ADP `.claude/skills/sdd-workflow/` + `task-decomposer/`(真实入口,非 Makefile) | `/Users/admin/codes/autodev_pipe/.claude/skills/{sdd-workflow,task-decomposer}/SKILL.md` |
| Δ-X4 | ADP `.claude/hooks/block-dangerous.sh`(Safety Floor 单层防线现状) | `/Users/admin/codes/autodev_pipe/.claude/hooks/block-dangerous.sh` |
| Δ-X5 | IDS 跨仓 hand-off 实测产物 — 007a-pA pilot | `specs/007a-pA/spec.md v0.3` + `specs/007a-pA/HANDOFF.md` + 4 轮 R1-R4 review outbox(`.codex-outbox/queues/007a-pA/`)|
| Δ-X6 | IDS framework SHARED-CONTRACT v1.1.0 + AUTODEV-PIPE-SYNC-PROPOSAL v2 + NON-GOALS 现状 | `framework/{SHARED-CONTRACT,AUTODEV-PIPE-SYNC-PROPOSAL,NON-GOALS}.md` |
| Δ-X7 | 跨仓审计 — ADP-AUDIT 2026-05-08(§1-§9 + Milestone) | `framework/ADP-AUDIT-2026-05-08.md` |

(Δ-X1 至 Δ-X7 加进 v2 X 后,v2 总 X 标的 = 11 + 7 = **18**;x_hash 必然异于 v1。)

---

## §3 · v1 K 的 grounding 变更(隐性 K 变更)

K 字面来自 forge-config.md L93-107 verbatim,拆为 6 子条 K1-K6(见 stage-forge-006-v1.md L112-118)。v1 跑期间未察觉的隐性 K 变更:

### K5 grounding 变更 — ADP 在 K 中的角色

**K5 字面**:"吸收四个项目尝试"(idea_gamma2 / vibe-workflow / autodev_pipe / 当前 ideababy_stroller)

**v1 跑时的 grounding 假设**(未显式说出但驱动了 verdict):
- ADP = framework "下半边的活产物",将持续维护并被吸收为 framework 的 build 层
- v1 stage §3 模块 1-4 + §5 dev plan 全部假设 "ADP 会被补丁 / 升级 / 物化为 L4 工程纪律层"
- sanity-v2 推荐"路径 2 在 ADP 那边补 3 真 gap" 也基于这个 grounding

**v2 应识别的真实 grounding**(operator 2026-05-09 揭示):
- ADP V4 是 operator 半年前停掉的"半成品"
- operator 决定不再用"野路子"维护 V4,**而是用 IDS L1-L4 方法重做 ADP-next**(用 ADP-next 区分之前的 ADP)
- V4 在 K 中的角色 = **物证**(operator 之前 4 个尝试之一的实物记录),**不是吸收对象**
- 真正要吸收的是"ADP-next 的设计意图"(K 中的"调研结论 / 设想 / 计划"段),不是"V4 这版具体实装"

**v2 应做的 K 操作**:

选项 A(轻):重写 K5 解释段,显式区分"V4 = 物证"vs "ADP-next = 待生的下半边产物";K1-K4 / K6 不动
选项 B(重):新增 K7 = "ADP-next 的角色显式声明:framework 待生的下半边,V4 是物证不是吸收对象,K5 中 ADP 项目实际指 ADP-next 的设计意图"
选项 C(最重):重新切 K — 把"framework K"和"ADP-next K"分开成两个独立 K(K_F + K_A),v2 verdict 可能要分两个 stage doc

**operator 倾向**:在 §6 ADP-next 候选设想未填前难判断;**建议 v2 跑时让两个 expert 在 P1 自行判 A/B/C 三选一**(把 K 重切的判断权交给 expert,operator 在 stage 阶段决策)。

---

## §4 · v1 verdict 落地路径的失效证据

v1 stage 显式落地路径(见 stage-forge-006-v1.md §5 + sanity-v2 §"推荐路径修订"):
- **节奏 A**:MVP ≤ 2 周,物化 v3.1 STARTER_KIT 🟢 项作为 L4 harness
- **节奏 B**:原生 4-6 周,framework 自身重组优先
- **路径 1**(sanity-v2 提出):用真实 idea 跑通 1 个 IDS L1→L4
- **路径 2**(sanity-v2 提出 + operator 在 next-steps.md v3 选择):在 ADP 那边补 3 真 gap(prod cred / risk tier / Eval Score)

逐条评估失效证据:

### 证据 1 · 路径 2 前提失效

sanity-v2 §"3 真 gap"假设 ADP 是要被补丁的活系统(见 sanity-check-v2-2026-05-08.md L275-281)。但今天 operator 决定不再维护 V4 → 这个前提失效。补 3 个 gap 到一个**确定要被重做**的代码库,等于:
- 浪费实施成本(gap 实装会随 ADP-next 重写一并被替代)
- 污染 V4 dogfood signal(沿用 ADR 0008 D2 警告 — 见 ADP-AUDIT-2026-05-08.md §1.4 + L63 "插入新 build 工作 = 100% 概率污染最初 4 周 dogfood signal")
- 阻碍 ADP-next 干净起步(ADP-next 应从 PRD/spec 干净启动,而非接手"补到一半的 V4")

### 证据 2 · DRIFT-1 是 framework 自身错误,不是 ADP 补丁

§9 DRIFT-1(架构级,见 ADP-AUDIT-2026-05-08.md L293-345):
- **错误**:IDS CLAUDE.md L24 假设 "L4 = spec + tasks + parallel build + ship",IDS 仓自带完整 SDD 工具链
- **实证**:IDS 仓**无** Makefile / pyproject.toml / pytest / check-disjoint / spec_validator
- **应然**:IDS = idea → PRD;ADP(或 ADP-next)= PRD → spec → build → ship
- **修复路径**:重写 SHARED-CONTRACT v1.1.0 → v2.0 + 重写 IDS CLAUDE.md L24 + 重写 plan-start.md

这条修复**不是"在 ADP 补 gap"**,**是 IDS framework 自身的重写**。路径 2 的"在 ADP 补 gap"动作不解决 DRIFT-1。

### 证据 3 · 007a-pA pilot dogfood 价值已达成

specs/007a-pA/HANDOFF.md L145 期望:"实测过程会暴露 SHARED-CONTRACT 假设 vs 现实的 drift 点(若有)"。

实证(见 ADP-AUDIT-2026-05-08.md §"Milestone" L499-528):**HANDOFF step 1-6 全 ✓** + **暴露 4 实证 drift**(DRIFT-1 至 DRIFT-4)= dogfood 价值已实现。

后续 step 7(parallel-builder)+ step 8(ship)被显式决议**暂停**(理由:dogfood 价值已达成 + 继续 build 会引入更多无关 drift D-A 至 D-E 冲淡焦点 + 不污染 V4 dogfood + C8 IDS-first ship 隐含约束)。

### 失效程度小结

| v1 落地路径 | 失效程度 | 理由 |
|---|---|---|
| 节奏 A(MVP 2 周物化 v3.1 STARTER_KIT) | **完全失效** | v3.2 已 port 五件套;v3.1 STARTER_KIT 物化的诱惑前提不存在;operator 不再维护 V4 |
| 节奏 B(4-6 周 framework 重组优先) | **基本失效** | 重组方向需结合 ADP-next 角色重定义重新设计;v1 §3 模块 1-4 描述的"在 ADP 补"不再适用 |
| 路径 1(真 idea L1→L4) | **部分达成** | 007a-pA pilot 已跑 step 1-6 → dogfood 价值已实现;路径 1 未到末端但已产生 §9 4 drift 证据,功能等价 |
| 路径 2(在 ADP 补 3 真 gap) | **完全失效** | 见证据 1 + 证据 2 |

**v2 应基于"v1 落地路径基本全失效"的事实重新产 verdict**,而非在 v1 路径基础上增量调整。

---

## §5 · 跨仓 hand-off 实测产物 — 4 实证 drift 总览

依据 framework/ADP-AUDIT-2026-05-08.md §9 L281-543,4 条实证 drift 摘要(详情见原文,本节不复述):

| ID | 严重 | 性质 | W1 是否阻塞 | 本质 | v2 verdict 应处理 |
|---|---|---|---|---|---|
| **DRIFT-1** IDS L4 设计假设错误 | **架构级** | 第一性推导 | 不直接阻塞(可绕) | IDS 仓没 Python infra ≠ bug,**根本错在 IDS L4 假设自带 SDD 工具链** | v2 verdict 必须显式回应"IDS 是否仍要带 L4 build 阶段";SHARED-CONTRACT v2.0 重写依据 |
| **DRIFT-2** IDS 缺 Python infra | **立即阻塞** | 实证(W1 撞墙) | 阻塞 task verification | DRIFT-1 的症状,不是独立 | v2 verdict 解决 DRIFT-1 即可;DRIFT-2 自然消失 |
| **DRIFT-3** 双 source of truth(IDS+ADP 各 13 task) | 中 | 实证 | 不阻塞(并存)| DRIFT-1 的症状 | v2 verdict 决定 spec/task 物理位置后,DRIFT-3 自然消失(IDS specs/ 标 DEPRECATED 或全删)|
| **DRIFT-4** working_repo emergent | 低/信号 | 实证(模型 emergent) | 不阻塞 | task-decomposer subagent 行为领先 ADP schema v0.2 | v2 决定 ADP-next schema 时追认或显式纳入 |

**v2 应把这 4 条作为 X 输入材料的核心证据**(对应 §2 表 Δ-X7)。

**特别提示**:DRIFT-1 是**架构级**,不只影响 ADP/ADP-next,也颠覆 IDS L4 阶段定位。v2 verdict 几乎一定要回答以下问题:
- IDS 是否仍声明自身有 L4 阶段?
- 若 IDS 没 L4,IDS pipeline 是 L1-L3?(spec-writer 如何归属?task-decomposer 如何归属?)
- ADP-next 是否完全继承 L4(spec / tasks / parallel build / ship 一条龙)?

---

## §6 · ADP-next 候选设想(operator 2026-05-09 已填,brainstorm + 第一性 12 问)

operator 与 Claude 在 2026-05-09 通过 12 轮问答(Q1-Q12 + Q13 第一性澄清)收敛出本节内容。所有结论基于第一性原理 + 事实(forge v1 verdict 物证 / §9 4 实证 drift / V4 实装现状 / forge 与 L1-L4 各自定位)。

### §6.1 · ADP-next 是什么 / 不是什么(Q1)

**operator 决议**:

> "**当前 ADP V4 只是作为一个参考,不做任何强要求强关联,一切从第一性原理出发,搭建一个可靠的 AI 自动开发 pipeline。我还是希望 IDS 负责 idea 到 PRD 的部分,ADP-next 只保障稳定、可靠、高质量、产品级的开发**。"(operator verbatim)

**展开**:
- ADP-next 是从第一性原理重建的 AI 自动开发 pipeline,**不是** V4 的延续 / 续作 / 升级版
- V4 在 ADP-next 中的角色 = **可参考的历史尝试之一**,与 idea_gamma2 / vibe-workflow / 现 IDS 同级,**没有任何强约束力**
- ADP-next **范围严格限定在 L4**:接收 IDS 产出的 PRD → 自己产 spec → build → ship。**不**做 idea / inspire / explore / scope 阶段(那是 IDS 的职责)
- 4 形容词产品定位:**稳定 + 可靠 + 高质量 + 产品级**(具体量化判准见 §6.5 Success looks like)
- 隐含决议:V4 已实装的 60-90% 模块(sdd-workflow / spec-validator / reviewed-by hook / retrospective L1+L2 / 等)**不强制保留**,ADP-next 自己 forge 论证后决定哪些借鉴 / 哪些重写 / 哪些丢

### §6.2 · 仓库形态(Q2 + Q7)

**operator 决议**:

| 决议项 | 选择 |
|---|---|
| 仓库策略 | **新建仓**(候选 a) |
| V4 处置 | 整仓 archive(打 git tag `v4-final`,不再动) |
| 仓名 | **XenoDev**(全新名字,与 V4 心智彻底切断) |
| 默认路径 | `/Users/admin/codes/XenoDev`(operator 可改) |

**理由**(基于事实):
- V4 主分支不被覆写,git history 物理保留 — 任何时候 `cd /Users/admin/codes/autodev_pipe && git log` 仍可看 V4 完整演化
- "XenoDev" 名字与 "autodev_pipe" 完全切断,避免心智上仍把 ADP-next 当 V4 的下个版本
- 与 Q3 只读 hand-off + 应然分工(IDS=idea→PRD / XenoDev=L4)一致

### §6.3 · 跨仓接口(Q3 + Q9 + Q12)

**operator 决议**:**双向 hand-off,SHARED-CONTRACT v2.0 一开始就含双向通道**

- **正向**(IDS → XenoDev):IDS 产 PRD + 元数据(等价当前 v1.1.0 §3 已实装的 hand-off 包)
- **反向**(XenoDev → IDS):**hand-back 包**,内容包括:
  - drift 反馈(类似今天 §9 4 drift,build 过程中暴露的设计缺陷)
  - PRD 不够细的问题(L4 build 撞墙时反馈到 IDS L3 重审)
  - 实践价值评估(N 个 idea 跑完后的成功率 / 干预率统计,反哺 IDS L1 inspire 选题)
- IDS 仓预留接收路径(eg `discussion/<idea>/handback/<timestamp>.md`)
- SHARED-CONTRACT v2.0 是 **breaking change**(v1.1.0 → v2.0 major bump),内容 = 双向协议 + IDS L4 重定义(应然分工 from DRIFT-1)+ ADP/XenoDev 角色重命名

**理由**:
- 单向 hand-off 没有闭环,ADP-next 跑一次又一次,IDS 不知道哪个 PRD 是好 PRD / 哪条约束写得不够清楚 / 哪种 ADP-next build 模式跑得通 — 整个 4 项目 dogfood lesson 收敛流程断了
- 双向 hand-off 把"实践→反思→优化 PRD/IDS"这条 loop 闭合,符合 K6"达成 framework/pipeline 共识方案"原意

### §6.4 · 防"想法变了 → 静默停"(Q5 + Q6 + Q11)

**operator 决议**:**强制 forge 元层锁决定**(任何"想法变了"必须起 forge 重审,不能静默停)

**应用范围**:
- ADP-next 的所有重大决策(架构 / 重大重构 / 重大想法转向)**强制走 IDS 仓的 `/expert-forge` 命令**
- forge 在 IDS 仓起,**不在 XenoDev 仓自带 forge 机制**(XenoDev 不复制 expert-forge 命令)
- IDS = 治理仓(所有 idea / 含 ADP-next 的元层决策)+ 评判仓(forge 是 IDS 的命令)
- XenoDev = 执行仓(只负 L4 spec→build→ship,不做元层决策)

**与"V4 仅作参考"的关系**(澄清 Q5/Q6 张力):
- forge **机制本身**(双 expert + SOTA + Codex review + 收敛)= **保留并强制使用**
- forge v1 / v2 的**具体 verdict 内容**(28 项 L/P/C / §9 4 drift / 决策矩阵 / refactor plan)= **仅参考,不做硬约束**
- ADP-next 跑 forge 时(如果有需要),expert 可以独立论证,即使结论与 forge 006 v1/v2 不同也 OK

**为什么**:
- V4 的失败模式 = "做了一半,我的想法变了"(operator verbatim)+ "野路子直 spec"
- forge 元层强制 = 把"想法变了"显式化为"必须重审 verdict",而不是 operator 一个人静默停
- V4 没经历过这种强制,导致半年沉没 + ADP-AUDIT 才发现废弃事实

### §6.5 · 成功判准(Q8 + Q8.1)

**operator 决议**:**质量型 + 数量型复合**(具体 N 与阈值由 forge 006 v2 的 expert 论证决定)

骨架:

| 维度 | 表述模板 |
|---|---|
| 数量型 | "ADP-next 完成 N 个真 idea 的 L4 ship"(N 待定) |
| 质量型 | "operator 干预率 < X%"(X 待定;hands-off 计量方法待 v2 expert 定) |
| 复合 | 同时满足上述两条 |

**v2 expert 应回答的具体问题**(operator 在 forge 006 v2 prefill 时显式提)
- N = 3 / 5 / 10 / 其他?
- 干预率 X = 20% / 10% / 5% / 其他?
- "干预" 怎么计量(每条 task 阻塞次数 / 每个 idea 提问次数 / spec frozen 后的修订次数 / 等)?
- N 个 idea 是连续 N 个,还是窗口 N(滑动窗口最近 N)?
- "真 idea" 与"测试 idea" 边界(防 expert 给个低 bar 让 operator 跑 N 个 toy idea 凑数)

### §6.6 · 启动路径(Q10 + Q13 第一性结论)

**operator 决议**:**forge 006 v2 verdict 出后,直接拆 IDS 优化 + XenoDev build,不重走 L1-L3 流程,不另起 idea 008 / forge 008**

**第一性依据**(operator 2026-05-09 关键澄清):

> "当前既然 forge 了,为什么要再走一遍 L1-L4。那些不是用于 idea 到 PRD 的生成吗?我理解 006 v2 forge 完的结果会直接拿去 优化当前 IDS + build XenoDev 吧?"(operator verbatim)

**事实分析**:

| 阶段 | 干什么 | forge 是否覆盖? |
|---|---|---|
| L1 Inspire | 对 raw idea 发散 N 方向(value/novelty/utility) | **forge SOTA 对标 + decision-list + free-essay 等价覆盖**(P2 SOTA 检索 = 比 L1 更广的方向探索) |
| L2 Explore | 选一方向深挖(non-tech) | **forge P3R1/P3R2 双 expert 收敛 = 比 L2 单一深挖更稳健** |
| L3 Scope | 加 operator 真约束写 PRD | **forge W4 next-PRD 自动产 PRD,但**不带 operator 真约束(forge 不问 operator 时间/失败接受度/最小切片)|
| L4 Plan | spec / task / build | XenoDev 自己的 L4 |

forge **替代了 L1-L2 大部分功能**(发散+深挖),**没替代 L3 的"operator 真约束注入"**。

**正确启动路径**:

```
Step A · forge 006 v2 跑(在 IDS 仓)
  ├─ /expert-forge 006 → 自动检测到 v1 已存在 → 起 v2
  ├─ prefill / forge-config(operator 把本草稿 §1-§7 粘进)
  ├─ P1 (Opus + GPT) / P2 (双方 + SOTA 检索) / P3R1 / P3R2
  └─ stage-forge-006-v2.md 出(verdict + W2 decision + W3 refactor + W4 next-PRD + W5 next-dev-plan + W6 free-essay)

Step B · operator 拆 v2 verdict 为 2 流(在 IDS 仓)
  │
  ├─ B1 · IDS 优化(verdict 中关于 IDS 改动的部分)
  │   ├─ 重写 SHARED-CONTRACT v1.1.0 → v2.0(双向 hand-off)
  │   ├─ 重写 IDS CLAUDE.md L24(L4 重定义为 "PRD 完工 + hand-off 包")
  │   ├─ 重写 .claude/commands/plan-start.md(产 hand-off 包,提示 operator 切到 XenoDev)
  │   ├─ DRIFT-3 处置(IDS specs/007a-pA/ 标 DEPRECATED 或全删)
  │   └─ 走标准 plan-start 推进
  │
  └─ B2 · ADP-next(XenoDev)启动
      ├─ B2.1 · operator 在 IDS 仓花 1-2h 给 v2 §4 next-PRD draft 加一节 "Real constraints (operator-specific)" + "Open questions"
      │        └─ 把 L3 会问但 forge 没问的几个问题答了:operator 时间 / 技能 / 失败接受度 / 最小切片
      ├─ B2.2 · git init /Users/admin/codes/XenoDev / cp 完整 PRD 进 XenoDev/PRD.md
      ├─ B2.3 · cd XenoDev,走 XenoDev 自己的 L4(spec-writer / task-decomposer / parallel-builder)
      └─ B2.4 · XenoDev 第一个 task 跑通后 → hand-back 包返 IDS(SHARED-CONTRACT v2.0 反向通道)
```

**不做的事**(明确排除):
- ❌ 不重走 L1 inspire(forge 已覆盖等价或更强)
- ❌ 不重走 L2 explore(同上)
- ❌ 不另起 idea 008 走 IDS L1→L4(冗余)
- ❌ 不另起 forge 008 专门论证 ADP-next(forge 006 v2 已经是了)
- ❌ 不走"forge v2 + L3 重跑"(L3 的 operator 真约束由手补完成,1-2h 即可,无须正式 L3 流程)

**风险接受**:
- forge 006 v2 §4 next-PRD 是双 expert 推出的 PRD,可能仍有不完美之处;operator 手补 L3 那一节后接受残留风险,在 XenoDev L4 build 撞墙时通过 SHARED-CONTRACT v2.0 hand-back 通道反馈回 IDS,触发 PRD revision(而非起 forge v3)

### §6.7 · 时间预算(Q4)

**operator 决议**:**不设上限,做到我满意为止**

**含义**:
- ADP-next 形态完全由质量决定(§6.5 Success looks like 满足 = 算成功),**不**由时间倒推
- 任何 expert / agent 给出的"X 周完成"建议都是参考,不是硬约束
- forge 006 v2 verdict 中的 "next-dev-plan(W5)" 时间表节奏 A/B/C 应被理解为**节奏参考**而非**硬截止**
- 不强制 dogfood 周期(避免重蹈 V4 12 周 dogfood 强制窗口的覆辙)

### §6.8 · 决议矩阵汇总(operator 12 问 Q1-Q13 一表)

| Q | 决议 | 落实在 |
|---|---|---|
| Q1 ADP-next 差异 | V4 仅参考,第一性重建,IDS=idea→PRD,XenoDev=L4 | §6.1 |
| Q2 仓库形态 | 新建仓(候选 a)| §6.2 |
| Q3 跨仓接口 | 只读 hand-off 包(SHARED-CONTRACT v2.0)| §6.3(实际为双向)|
| Q4 时间预算 | 不设上限 | §6.7 |
| Q5 V4 仅参考粒度 | forge v1 全是参考,ADP-next forge 可全重启论证 SOTA | §6.4 |
| Q6 防"想法变了→停" | 强制 forge 元层锁决定 | §6.4 |
| Q7 仓名 | XenoDev | §6.2 |
| Q8 成功判准类型 | 质量型 + 数量型复合 | §6.5 |
| Q8.1 N + 阈值 | 由 v2 expert 论证决定 | §6.5 |
| Q9 跨仓 dogfood 双向 | 必须反馈(双向 hand-off)| §6.3 |
| Q10 ADP-next 启动路径 | 由 v2 决定(实际由 Q13 第一性结论提前确定)| §6.6 |
| Q11 forge 归属 | 全部在 IDS 起 forge(IDS=治理仓 / XenoDev=执行仓) | §6.4 |
| Q12 双向 hand-off 时机 | v2.0 直接实现双向(不分两步)| §6.3 |
| Q13 ADP-next PRD 来源 | forge 006 v2 §4 next-PRD + operator 手补 L3 真约束 1-2h | §6.6 |

---

## §7 · v2 跑的建议参数

| 参数 | v1 实际 | v2 建议 | 理由 |
|---|---|---|---|
| **W**(产出形态)| W1-W6 全选(v1 forge-config.md L72-81)| W1-W6 全选 | 同 v1;但 next-PRD(W4)应聚焦 ADP-next 的 PRD,而不是 framework 整体 PRD |
| **convergence_mode** | preserve-disagreement(v1 forge-config.md L113)→ 实际 converged-with-tempo-options | **strong-converge**(若分歧大可降级 preserve-disagreement)| v2 X 输入比 v1 厚很多 + operator 心中已有方向感(K5 grounding 已对齐)→ 收敛到单一 verdict 价值更大 |
| **Z 参照系** | 对标 SOTA(forge-config.md L52-68)| 同 v1 + 增补 | 增补:Anthropic Claude Skills SDK v2(若 2026-05 已发布)+ Cursor Composer 跨仓 build 模式 + Codex CLI 5.4(若已 release)+ GitHub Spec Kit v2 |
| **Y 视角** | Y1-Y4(产品价值 / 架构 / 工程纪律 / SOTA)| 同 v1 + 增补 Y5 | Y5 = "重做的代价 / 沉没成本 / 知识保留" — operator 决定 ADP-next 时要面对 V4 半年来的实装是否能保留(L/P/C 分层视角下哪些是 L 可保留 / P 可借鉴 / C 必须丢)|
| **Codex 阶段** | gpt-5.5 xhigh(P1-P3R2 全用)| 同 v1 | 不变 |
| **Opus 阶段** | Opus 4.7 max | Opus 4.7 max | 不变(若 Opus 4.8 已发布可考虑;但 4.7 在 v1 表现稳定)|
| **forbidden in P2 search** | tech-stack 深挖 / pricing(forge-config.md L65-68)| 同 v1 | 不变 |
| **prefill source** | proposals.md §006(verbatim)| proposals.md §006 + 本草稿 §1-§7 | 增补本草稿作为 prefill 输入 |
| **expected stage 总字数** | 3000-4500 字(v1)| 4500-6500 字 | v2 X 多 7 项,讨论面更广;但 §1 no-rerun 区会节省一部分 |

---

## §8 · v2 跑的命令

operator 在 IDS 仓库根目录跑:

```bash
/expert-forge 006
```

`expert-forge.md` Step 0.2(L40-46)的 v<N> 自动检测会:
1. `ls discussion/006/forge/` → 看到 v1 已存在
2. 取最新 v<N> = v1
3. 起 v2 / 自动 mkdir v2/ 已建好(本草稿落底前已 mkdir,v2 跑时 expert-forge 会复用)
4. 跑 prefill(forge-intake-prefill subagent,产出 v2/_prefill-draft.md)
5. operator 在 prefill 后人工编辑 v2/forge-config.md(粘进本草稿 §1-§7 + §6 自填部分)
6. expert-forge 进入 P1 阶段(双 expert 并发跑)

**operator prefill 后的检查点**:
- v2/forge-config.md 的 K 段 — 是否反映 §3 K5 grounding 变更
- v2/forge-config.md 的 X 段 — 是否包含 §2 Δ-X1 至 Δ-X7 共 7 个新增 X
- v2/forge-config.md 的 convergence_mode — 是否设为 strong-converge
- v2/forge-config.md 的 x_hash — 应**异于** v1 hash `e45d68ee6dcc74d2c667976a28940c91`

---

## §A · 引用 — operator 2026-05-09 verbatim(隐性 K 变更物证)

operator 2026-05-09 对话原话摘录(关键 4 句,作为 §3 K5 grounding 变更的第一手证据):

> "ADP现在已经没有在做了"

> "我之前有个做了一半 ADP 罢了"

> "我决定用 IDS 的方法给 ADP 这个项目上个双保险"

> "006 的产物就是要做一个 ADP,只不过我之前有个做了一半 ADP 罢了"(operator 在追问中明确:idea 006 产出的是 ADP-next,V4 是更早的尝试)

(完整对话见 `/Users/admin/.claude/projects/-Users-admin-codes-ideababy-stroller/9fa04ce4-25e8-448e-97dd-1c1530ddf787.jsonl` —— 私人 session 记录,本仓库不存。)

---

## §B · 引用 — sanity-v2 §"何时起 v2"原文(命中状态标注)

依据 sanity-check-v2-2026-05-08.md L226-236,verbatim:

> **何时起 v2**:
>
> 1. 用真实 idea 走完 1 个 IDS L1→L4 → PRD 流程,然后**实际去 ADP 那边消费 PRD**;此时暴露的接口缺陷(SHARED-CONTRACT §3 假设的 cli 不存在)是 v2 forge 的 X 输入
> 2. 或:autodev_pipe v4 12 周 dogfood 完成 + ship checkpoint 03 后,新事实可作为 forge v2 X 输入
> 3. 或:出现新 SOTA(如 Anthropic Claude Skills SDK 升级到 v2)需重审 NG-3
>
> **何时不起 v2**:
>
> - 仅"想再问一遍"
> - 没有新 X 输入
> - 现有 framework 文档 7-8 成够用

**命中状态(2026-05-09)**:

| 触发条件 | 命中? | 证据 |
|---|---|---|
| (1) 真 idea L1→L4 后 ADP 消费暴露接口缺陷 | **✓ 命中** | 007a-pA pilot 跨仓 hand-off step 1-6 实测产生 §9 4 drift(详 §5);DRIFT-1 显式暴露"SHARED-CONTRACT 假设 cli 不存在" |
| (2) V4 12 周 dogfood 完成 + checkpoint 03 | **✗ 未命中,且永不会命中** | operator 2026-05-09 决议不再维护 V4 → checkpoint 03 不会产出;此触发条件已失效 |
| (3) 新 SOTA 重审 NG-3 | **△ 部分命中(隐性)**| 不是新 SOTA,而是 operator 对 ADP 的 SOTA 态度变了:从"野路子 build" → "用 IDS 方法重做",这是 K 内部对 SOTA 的重新解读 |

**反向"何时不起 v2"对照**:

| 反向条件 | 是否成立? |
|---|---|
| 仅"想再问一遍" | ✗ 不成立(有真 X 增量,见 §2 Δ-X1 至 Δ-X7)|
| 没有新 X 输入 | ✗ 不成立(7 个新 X)|
| 现有 framework 文档 7-8 成够用 | ✗ 不成立(DRIFT-1 是架构级错误,framework 文档不够)|

**结论**:正向触发条件命中 1 全 + 1 半;反向"不起 v2"条件全部不成立 → **起 v2 是合规的**。

---

## Changelog

- 2026-05-09 v1 (this draft): 初稿。基于 operator 2026-05-09 决议起 forge 006 v2,沉淀 v1 verdict 之后的事实变更(7 个新 X 标的)+ K5 grounding 隐性变更 + §9 4 实证 drift + ADP-next 角色重定义。**§6 ADP-next 候选设想留 placeholder,operator 在 v2 真跑前自行填写**。
- 2026-05-09 v2: §6 全面重写。operator 通过与 Claude 12 问问答(Q1-Q13)收敛 ADP-next 候选设想,含:V4 仅作参考第一性重建 / 仓名 XenoDev 新建仓 / SHARED-CONTRACT v2.0 双向 hand-off / 强制 forge 元层锁决定 / 质量+数量复合成功判准 / 启动路径 = forge v2 verdict 拆 IDS 优化 + XenoDev L4 不重走 L1-L3(forge 已替代 L1-L2 大部分,L3 真约束由 operator 手补 1-2h)/ 不设时间上限。§6 含 8 子节 + 12 问决议矩阵汇总。
