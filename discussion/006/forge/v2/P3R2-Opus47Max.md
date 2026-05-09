# Forge v2 · 006 · P3R2 · Opus 4.7 Max · 联合收敛 R2(finalize)

**Timestamp**: 2026-05-09T13:08:00Z
**Visibility**: 我已读对方 P3R1。
**Convergence mode**: strong-converge
**Convergence intent**(operator binding):每个 W 都要有收敛主线 + v0.2 note 旁注,不暴力压扁分歧。

## §1. 我对每条分歧的最终立场 + 让步

**分歧 1 · Spec Kit "v2" 事实表述**(GPT P3R1 §3 row 1)
- 对方在 P3R1 给的论证(quote ≤15 words):"不要把'v2 已发布'写成事实;我 P2 未验证到官方 v2"
- **我的最终立场**:**完全接受 GPT 立场**。把"直接采用 Spec Kit v2 schema"全句改写为"对齐/可评估 fork Spec Kit 现行 schema(0.8.7,2026-05-07);XenoDev 自己保留 PPV/Safety Floor 扩展"
- 让步给对方:全部。我 P2 沿用 operator binding 中的"v2 已发"假设而未核,这是事实错误。

**分歧 2 · sdd-workflow / task-decomposer C 级处置**(GPT P3R1 §3 row 2)
- 对方立场已与我 P3R1 §3 一致(双方在 P3R1 已合一)
- **最终**:CLOSED — XenoDev 选定 schema 后,skills 物理 source-of-truth 迁 XenoDev,IDS 同名 skills DEPRECATED;不因 port-from-IDS 自动 cp。

**分歧 3 · `working_repo` workspace schema**(GPT P3R1 §3 row 3)
- GPT 加新具体内容(quote ≤15 words):"必须含 workspace root / build repo / source PRD repo / hand-back target 四字段"
- **我的最终立场**:**完全接受 + 纳入主线**。SHARED-CONTRACT v2.0 §"workspace schema" 必须显式定义这 4 字段,作为跨仓 build 的一等公民。

**分歧 4 · Eval Score / risk tier v0.1 形态**(GPT P3R1 §3 row 4)
- 对方立场已与我 P3R1 一致(留接口 / 不实装算法)
- **最终**:CLOSED + GPT 加细化(quote ≤15 words):"v0.1 记录 review failures、operator interventions、hand-back drift 三类 event"。**我接受这具体 event schema**。

**分歧 5 · K3 小型项目轻入口**(GPT P3R1 §3 row 5)— **R2 finalize 必处理硬分歧**
- 对方立场(quote ≤15 words):"不同意降级为 v0.2 note...W1/W2 必须显式保留'轻入口、重升级'"
- **我的最终立场**:**完全接受 GPT 立场,纳入主线 verdict**。理由:(a) v1 verdict §1 "轻入口、重升级"是 K3 在 v1 收敛时回应 K3 的核心机制 + AGENTS §3 已实装 Small/Medium/Large tier — 这是仍站住的 v1 lesson(per moderator-notes §四 "v1 verdict 仅参考但 lesson 可吸收");(b) 把 K3 唯一回应降级 v0.2 = 实质丢 K3,违反 operator §6.1 "可靠+稳定+高质量+产品级"覆盖各规模初衷;(c) 不写 K3 入口形态会让 operator 在 v2 之后又起 v3 forge 补 K3 — 浪费一轮。**让步全部给对方**,主线 W1/W2 显式继承"轻入口、重升级"分级。

## §2. 联合 verdict(单一)

**新建 `XenoDev` 仓作为 ADP-next 的运行时 harness**,V4 整体 archive(打 git tag `v4-final`)。IDS 仓退回 idea→PRD + governance/forge + 双向 hand-off/back v2.0,**不再产 specs/**;XenoDev 承担 PRD→spec→build→ship 一条龙。**保留 v1 "分级 harness、轻入口、重升级"哲学骨架**:Small 项目走 AGENTS.md + Safety Floor + 基础质量门轻入口(operator 直驱 Claude Code,不走 forge/L1-L4);Medium/Large 升级到 IDS 完整 idea→PRD + XenoDev L4 build + 双向 hand-back。XenoDev v0.1 必须先落:(a) Safety Floor 三件套(凭据隔离 + 不可逆命令 + 备份破坏检测);(b) 单一 build spec source(在 XenoDev,对齐/可评估 fork Spec Kit 0.8.7 现行 schema + 自带 PPV 扩展);(c) workspace schema 四字段(workspace root / build repo / source PRD repo / hand-back target);(d) hand-back 包结构化(drift / PRD-revision-trigger / 实践统计三类标签);(e) Eval/risk 数据接口(append-only event log,记录 review failures / operator interventions / hand-back drift,**不实装 scoring 算法**)。**强制 forge 元层锁决定**:任何重大架构转向必须在 IDS 走 `/expert-forge`,XenoDev 不复制 forge 机制。**v2 后启动路径**:不重走 L1-L3,operator 直接拆 B1(IDS 优化:SHARED-CONTRACT v1.1.0→v2.0 + CLAUDE.md L24 + plan-start v2)+ B2(XenoDev L4 启动)双流;B1 必须先(SOTA Spec Kit 强顺序),B2 才能跑首个 PRD 的 hand-off。

## §3. 残余分歧降级为 v0.2 note

- **v0.2 note 1**:Spec Kit fork 的精确边界 — 是 fork 整 repo 还是只对齐 schema 概念?XenoDev 起来时才决,看 Spec Kit 0.8.7 实际 spec 模板与 V4 7 元素 schema 的兼容度。**何时回头看**:XenoDev 第一个真 PRD 起 sdd-workflow 时。
- **v0.2 note 2**:Eval Score scoring 算法 — operator §6.5 明示由"v2 expert 论证决定"但我们 v2 没给精确数字。**保留为 W4 next-PRD 的 Open question OQ1**;**何时回头看**:XenoDev 跑完 N=2-3 个真 PRD 后回看,有真数据再决 N+干预率阈值。
- **v0.2 note 3**:risk tier 在 PPV 中的位置 — V4 PPV 第 7 元素已含 "production path";risk tier 是否拆为独立第 8 元素?**何时回头看**:XenoDev v0.2 spec schema bump 时。
- **v0.2 note 4**:小项目轻入口的"升级触发器"精确定义 — 项目从 Small 升 Medium 的判准(代码行数 / 工时 / 跨仓需求 / 等)v1 的 OQ1 在 v2 仍未给数字。**何时回头看**:XenoDev 跑过 ≥1 个 Medium 项目后,回看实际触发条件。

## §4. W 形态产出的初步草稿建议(给 synthesizer)

- **W1 verdict-only**:"**新建 XenoDev 作为 ADP-next 运行时 harness;V4 archive;IDS 退回 idea→PRD+governance;保留'轻入口、重升级'分级,Small 走 AGENTS.md 轻入口、Medium/Large 走 IDS+XenoDev 双仓全链;v0.1 必落 Safety Floor + workspace schema + hand-back + Eval 数据接口**"(80 字内单段)
- **W2 decision-list 4 列矩阵**:
  - **保留**:v1"轻入口、重升级"分级 / Safety Floor 三件套 / sdd-workflow 7 元素思想 / forge 机制
  - **调整**:SHARED-CONTRACT v1.1.0→v2.0(双向+workspace schema 4 字段)/ IDS CLAUDE.md L24 / plan-start v2 / reviewed-by 4 轮→1-2 轮+Evaluator role
  - **删除**:V4 整体作为继承对象 / IDS specs/ 双 source / "Spec Kit v2"假设(改 0.8.7)
  - **新增**:XenoDev 仓 / 反向 hand-back 通道 / workspace 4 字段 schema / Eval 数据接口(3 类 event)/ 强制 forge 元层锁
- **W3 refactor-plan 关键模块**(2-3):
  - 模块 A · IDS framework(B1):SHARED-CONTRACT v2.0 重写 + CLAUDE.md L24 + plan-start v2 + specs-protection 调整
  - 模块 B · XenoDev 启动(B2):git init + Spec Kit 0.8.7 schema 评估 + Safety Floor port from V4 block-dangerous + workspace schema 实装
  - 模块 C · 双向 hand-back 协议:hand-back 包结构 + IDS 接收路径(`discussion/<id>/handback/`)+ Eval event log 格式
- **W4 next-PRD 关键产品决策点**(2-3):
  - 用户 = operator 单人;Small 走轻入口、Medium/Large 走 IDS+XenoDev 全链;关键 success metric = N+X(具体数字 OQ1)
  - hand-back 通道是产品功能(operator 在 IDS 看到 build 反馈)而非纯工程
- **W5 next-dev-plan 关键 milestone**(2-3):
  - M1 (B1) IDS 改造完成 = SHARED-CONTRACT v2.0 + CLAUDE.md + plan-start v2 ship(operator 不设上限,但建议 1-2 周)
  - M2 (B2) XenoDev v0.1 = git init + Safety Floor + Spec Kit fork + workspace schema + 跑通首个真 PRD 第 1 个 task ship
  - M3 hand-back 闭环 = XenoDev 第 1 个 task ship 后产 hand-back 包返 IDS,operator 验证可读可消费
- **W6 free-essay 关键论点**(2-3):
  - "ADP-next 不是补 V4 的 process 文档,而是建一个 production runtime"(GPT P2 headline)
  - "K7 reframe 是 sunk cost 健康止损,SOTA 60% abandonment 实证支持"
  - "保留 v1 '轻入口、重升级' 是 K3 在 v2 仍站住的核心 lesson,不可丢"
