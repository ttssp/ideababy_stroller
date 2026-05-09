# Forge v2 · 006 · P3R1 · Opus 4.7 Max · 联合收敛 R1(标分歧)

**Timestamp**: 2026-05-09T13:00:00Z
**Visibility**: 我已读对方 P1 + P2。
**Searches in this round**: NONE(R1 hard constraint)。
**Convergence intent**(operator binding):每个 W 都要有收敛主线 + v0.2 note 旁注。

## §1. 整合摘要

四份 P1/P2 在**5 件 binding** 上完全对齐(V4 仅参考 / DRIFT-1 架构级 / SHARED-CONTRACT v2.0 双向 / forge 元层锁 / 不重走 L1-L3),**主结构无分歧**:新建 XenoDev,V4 archive,IDS=idea→PRD,XenoDev=L4 一条龙。SOTA(Spec Kit 0.8.7 / Cursor 3 multi-root / Anthropic Skills+Agent SDK / MSR 2026 failure corpus / GPT-5.4 Codex)全方向验证 — agentic coding 主流共识就是"运行时 harness + 4 phase + 跨仓 workspace + 可观测 + 可学习"。

GPT P2 §1 关键 headline 一针见血:**"我们 vs SOTA 的核心 gap 是 XenoDev 还没有一等运行时 harness"**(Eval/risk/hand-back/permissions/observability 都未产品化)— 这定义了 v2 verdict 的中心命题:**ADP-next 不是补一份 process 文档,而是建一个 production runtime**。两边一致认为 "**仅靠 prompt/skill 不足,必须有统计反馈、测试失败归因、review/hand-back 数据**"(GPT P2 §3 row 4,15 words)。

GPT P2 也修正了 2 个我 P1/P2 的具体错误:(a) Spec Kit 当前 latest = 0.8.7(2026-05-07)而非 v2 — 我 P2 沿用 operator binding 中"Spec Kit v2"假设没核;(b) `working_repo` emergent 字段处置:不是"通过物理位置消除"(我 P1 §3 Q3),而是"显式建模为 workspace/schema"(Cursor multi-root SOTA 支持)。这两条我接受。

## §2. 我的初步 verdict(草案)

**verdict**:**主线 = 新建 XenoDev 仓 + 直接采用 Spec Kit 0.8.7 schema + 跨仓 workspace 一等建模(吸收 `working_repo`)+ 双向 hand-off/back v2.0 + Eval/risk/hand-back 数据接口在 v0.1 留位**。V4 整体作为 archive 物证(打 git tag `v4-final`),L+P 作为 lesson 写入 XenoDev `~/.claude/lessons/`,C 仅 cp `block-dangerous.sh`(纯工业共识 23 pattern,无 ADP-next 偏好)。IDS 这边 SHARED-CONTRACT v1.1.0→v2.0 + CLAUDE.md L24 重写 + plan-start v2 改产 hand-off 包(不再产 specs/)是 B1 流;XenoDev 启动是 B2 流,B1 必须先(SOTA Spec Kit 强顺序)。

**关键不确定点**:Spec Kit 0.8.7 的 spec schema 与 V4 7 元素 schema 的兼容度如何 — 直接 fork 是否需要 wrap 一层(保留 PPV 第 7 元素的 production path 思想)。如果 R2 给不出明确答案,W4 next-PRD 中 schema 选择降级为 v0.2 note 显式留两选项。

## §3. 关键分歧清单

**分歧 1 · sdd-workflow / task-decomposer C 级处置(承袭来源)**

- 我的立场:port from IDS,XenoDev 起来时**直接从 IDS 重新 port**(IDS 是原版 source-of-truth,ADP 那边的是 port 副本)
- 对方立场(GPT P2 §3 row 5,15 words):"是否 C 级直接继承,应由 XenoDev schema 决定,不能因 port-from-IDS 自动保留"
- R2 期望收敛:**接受 GPT 立场**。XenoDev 选定 schema(Spec Kit 0.8.7 或 V4 7 元素 fork)后,sdd-workflow / task-decomposer 的 C 级形态由该 schema 重新派生,不是从 IDS 或 ADP 任一边 cp。**让步**。

**分歧 2 · `working_repo` emergent 字段处置(P1 §3 Q3)**

- 我的立场(P1 §3 Q3):或通过物理位置改变让其消失,或 ADP-next schema 追认,operator 待决
- 对方立场(GPT P2 §3 row 3,12 words):"正确方向是显式 workspace/schema,不是假装单仓"
- R2 期望收敛:**接受 GPT 立场**。SHARED-CONTRACT v2.0 §"workspace 字段 schema" 显式定义跨仓 workspace 模型(Cursor multi-root 范式),`working_repo` 字段进 XenoDev schema v0.1 一等公民。**让步**。

**分歧 3 · Eval Score / risk tier 在 v0.1 的形态**

- 我的立场(P2 §3 row 5):**部分站住** — Safety Floor 三件套是 hard floor 优先;Eval Score / risk tier 可推 v0.2(operator §6.5 也说 "由 v2 expert 决定 N 与 X 阈值")
- 对方立场(GPT P2 §3 row 4,18 words):"Eval Score 不能长期后置,至少要在 v0.1 留数据接口"
- R2 期望收敛:**部分接受 GPT 立场,折中** — v0.1 必须**留数据接口**(append-only event log 字段定义)但**不必实装 scoring 算法** + 不必出 risk tier verdict;v0.2 才上 scoring + verdict。**理由**:operator §6.5 明示阈值由 expert 论证 + operator §6.7 不设上限,过早 freeze 算法 = 浪费;但留接口 = 未来不用 schema-bump,符合 GPT MSR 2026 实证关切。

**分歧 4 · v1 V4 retrospective skill / lessons/ user scope 的处置**

- 我的立场(P1 §2 Y2):L+P 保留(等 XenoDev 真 dogfood 后回炉重做);P2 §3 我自我修正为"V4 dogfood 12 周 0 次跑过 = 未实证,XenoDev 不应直接继承"
- 对方立场(GPT P2 隐含):同我 P2 修正,作为 lesson 而非 component 保留
- R2 期望收敛:**双方已对齐**(P2 阶段我已自我修正向 GPT 立场靠拢)。无需 R2 处理,可 §3 标 closed。

## §4. 与 K 的对齐性自检(K1-K7 + convergence_intent + 5 binding)

- **K1** "可靠的、自动化程度最高解决方案" → ✅ verdict 主线 = 建 XenoDev 一等运行时 harness + 显式跨仓 workspace + Eval 数据接口 + Safety Floor 三件套,直接对应"可靠 + 自动化"。MSR 2026 failure corpus 给反例验证。
- **K2** "operator 非软件背景但能写 PRD" → ✅ IDS 保留 idea→PRD 阶段(SHARED-CONTRACT 8 字段 schema + L1-L3 流程不变),hand-off 后 XenoDev 接管所有 SDD 复杂度;operator 只动 PRD 不动 spec。
- **K3** "对各规模(大中小型)的开发的方案、流程、规范都没有把握" → ⚠ verdict 给出 ADP-next 是中-大型 pipeline,但**没显式回答小型项目用什么轻入口**(v1 verdict "轻入口、重升级"形态在 v2 没显式继承,需 R2 显式回应或降级 v0.2 note)。
- **K4** "我最近一个月做了 4 个尝试" → ✅ V4(尝试 3)+ idea_gamma2(尝试 1,no-rerun)+ vibe-workflow(尝试 2,no-rerun)+ IDS(尝试 4)在 verdict 中各有处置:V4=archive+lesson;尝试 1/2/4 不动。
- **K5** "吸收四个项目尝试" + **K7**(operator Append)"ADP-next 是 framework 待生下半边,V4 是物证不是吸收对象" → ✅ verdict 严格按 K7 reframe:V4 仅作 archive 物证 + L+P 作为 lesson,C 仅 cp block-dangerous;不补丁 V4 = 与 K7 完全对齐。
- **K6** "达成基于 claude code 实现可靠自动化开发的 framework/pipeline 的共识方案" → ✅ verdict 给出 framework(IDS)+ pipeline(XenoDev)的明确分工 + 双向 hand-off 让 framework/pipeline 形成闭环;符合"共识方案"原意。
- **convergence_intent** "每个 W 都要有收敛主线 + 旁注补充" → ✅ 本 R1 verdict 主线明确 + 关键不确定点标 v0.2 note 候选 + R2 残余分歧降级 = 完全对齐。
- **5 binding 事实** → 全 ✅(本 R1 §1+§2 已逐条引用并基于其推 verdict)。

**唯一 ⚠ = K3**:R2 必须显式回应"小型项目用什么轻入口"或降级为 stage 文档 v0.2 note(避免 K3 在 v2 verdict 中被悄悄丢)。
