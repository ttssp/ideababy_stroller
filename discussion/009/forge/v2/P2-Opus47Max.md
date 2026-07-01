# Forge v2 · 009 · P2 · Opus47Max · 参照系评估(SOTA 对标 · 画蓝图专项)

**Timestamp**: 2026-07-01T05:46:53Z (Phase 2)
**Searches used**: 5 web searches(自适应系统反馈回路 auto vs human / 量化系统分层架构+反馈环 / point-in-time 价格数据层设计 / strangler-fig 增量演化 / 目标态架构蓝图详略度)。
**Visibility**: 已读对方 P1-GPT55xHigh.md(refresh);自己 v2 P1 refresh;v1 stage doc refresh;forge-config refresh;moderator-notes 不存在。
**Reviewer stance**: 审阅人 — 用 SOTA 校准 v2 蓝图 first-take,不重刷 v1 已做的回测方法论 SOTA。

## 0. 本轮做了什么

读对方 v2 P1:GPT-5.5 与我 **高度对齐**,且**独立读了 DB schema**得出同一结论(七环节闭环、非统一壳)。GPT 的 §3 三个不确定点与我 **几乎逐条相同** ——(1) 回流该自动调阈值还是 human 确认(2) 价格数据层范围(v0.1 只做关注股日线 vs 纳入多市场/复权/汇率/成本)(3) 蓝图实到字段/gate 还是服务边界(后者可能诱导 V4)。**双方独立收敛到同一批不确定性 —— 这正是 P2 SOTA 该精准打击的三个点。** GPT 还比我 sharpen 一处:`decisions.would_have_acted_without_agent` 虽在,但 calibration 仍缺"事后价格、不动基线、反事实窗口"(不是现成一等表)—— 这与我 §1A"要新建价格历史层"是同一缺口的两面。

下面用 SOTA 把这三个不确定点 + 两个核心 Y(目标态架构 / 分期)压到证据上。

## 1. SOTA 对标

| 主题 | SOTA 现状(检索证据) | 对 009 蓝图的启示 |
|---|---|---|
| **目标态架构分层** | 量化系统的规范分层 = **data → strategy → backtesting → execution**,"modular, feedback-driven, 各层 isolated 降耦合","post-trade analysis feeds back into modeling","各角色独立迭代但保持 end-to-end coherence"。 | **SOTA 直接验证了双方画的七环节形态**,且给了 operator 痛点的精确解:"各做各的"不是靠大壳解决,是靠**契约让各器官独立迭代 + 端到端连贯**(= v1 的松耦合 + 契约先行)。蓝图的器官图可直接映射这套标准分层,operator 的"缺统一方向"= 缺这张 end-to-end coherence 图,不是缺大壳。 |
| **反馈回路:自动 vs 人工**(不确定点1) | 自适应系统用 fitness function **自动**调权重/阈值,但"面临 parameter sensitivity + 计算复杂度 + 过拟合风险";解药是**惩罚项控制**(AIC 等)。"自动调参无需操作员训练"是优点,但过拟合风险仍是核心挑战。 | **直接回答不确定点1**:回流可以自动,但**过拟合风险正是 operator 判不了的(他不懂投资)**。所以蓝图应定:**v0.1 回流线 = "回测算出建议旋钮值 → human 确认后才生效"(human-on-the-loop)**;全自动回流 gated 在"回测本身已按 DSR/PBO 防过拟合 + 有惩罚项控制"之后。这也守住 K binding①(防 build runtime 静默定方向)—— 自动调阈值本质就是系统在替 operator 定"信号多强/纪律多严"。 |
| **point-in-time 价格数据层**(不确定点2) | PIT 数据基础设施必须处理 **publication lags / data revisions / survivorship bias / corporate actions(拆分/分红)/ adjusted vs unadjusted 序列**;survivorship-free 要含退市股。是"front-office 策略的 foundational requirement"。 | **回答不确定点2**:价格层**不 trivial**,但单人 v0.1 关注股场景有明确"最小可用"档:**日线 bars + 拆分/分红复权 + 退市股感知(survivorship)**;**defer** 多市场/汇率/分钟级/tick。⚠ 关键:复权处理必须 v0.1 就做(否则 alpha 头把拆分当暴跌,回测全错)。这是 v1 AC-5(as-of 不泄漏未来)的具体化 —— 复权也是一种 as-of 正确性。 |
| **增量演化 / 分期**(核心 Y) | **Strangler Fig 模式**(Martin Fowler):新系统**latch 到现有系统上、piece by piece 长起来**、逐步替换/扩展,每期独立可用、"high-value features first"、避免 big-bang rewrite。"每期允许 learning + 调整"。 | **给了蓝图分期一个 named、battle-tested 的锚**,且是 V4 的直接解药。009 新"回测器官"**strangle 进现有 004/008 周围**(不替换、只扩展):M2 alpha 头先做(operator 最想要的 high-value)→ 逐步长出 calibration + 回流。蓝图的分期章节应显式命名 Strangler Fig,强调"回测器官围绕 004 生长,004 一直可用"。 |
| **目标态蓝图详略度**(不确定点3) | TOGAF 区分 **Architecture Definition Document(定性视图)vs Architecture Requirements Specification(定量、可测 criteria)**;"多视图、varying levels of detail"。 | **精准回答不确定点3的"画多实"**:蓝图应**分两档详略** —— **现在要建的器官(M1数据层/M2 alpha头)画到定量契约级**(接口签名 + AC 可测条款,如 v1 AC-1..AC-5);**未来插槽(图谱/蒸馏)只画定性边界**(StrategyModule 接口签名 + gate 条件,不画内部字段)。这就是"充分彻底 vs 防 V4"的标准分界线 —— 不是二选一,是**按器官成熟度分详略**。 |

## 2. 用户外部材料消化

K 内无额外 URL/文件;X 的 5 个标的(v1 stage doc / 004 PRD / 008 PRD / 004 strategy 代码 / 004 DB schema)已在 P1 一手消化。本轮无新增外部材料,SOTA 证据全部来自上表 5 次检索。

## 3. 修正后的视角(P1 哪些站住、哪些被推翻)

**站得更稳的(SOTA 加固)**:
- **七环节器官图** —— SOTA 的 data→strategy→backtesting→execution + feedback 标准分层直接验证双方画的形态。P1 判断不变,信心↑,且拿到"各做各的靠契约解决非靠大壳"的 SOTA 背书。
- **价格历史层是关键新器官** —— PIT 数据 SOTA 证明它 foundational 且不 trivial(要复权/survivorship),P1 "唯一关键新器官"判断站住,且范围划清(日线+复权+退市感知,defer 多市场)。
- **蓝图 ≠ 一次性建完** —— Strangler Fig 给了 named 模式背书,P1 的"每期独立可用"从原则升级为标准工程模式。

**被 SOTA 明确化/修正的(原 P1 §3 不确定 → 现在有答案)**:
- **不确定点1(回流自动 vs 人工)→ 定为 human-on-the-loop(v0.1)**:SOTA 证明自动回流有过拟合风险,而这恰是 operator 判不了的。修正为:v0.1 回流线产"建议旋钮值",human 确认生效;全自动 gated。**这条 P3R1 应固化为蓝图硬约束**(它同时是 K binding① 的落地)。
- **不确定点2(价格层范围)→ 定为"日线+复权+退市感知,defer 多市场/汇率/tick"**:从"不确定"变为有 SOTA 依据的范围线。
- **不确定点3(蓝图画多实)→ 定为"按器官成熟度分两档详略"**:现建器官画定量契约(接口+AC),未来插槽画定性边界(签名+gate)。**这直接调和了 operator "充分彻底" vs "防 V4" 的张力** —— 不是画多实的问题,是分档画。

**给 P3R1 的收敛预告**:双方 v2 P1 已高度对齐,SOTA 又把三个不确定点全给了有依据的答案。核心待收敛已很少,预计 P3R1 只需确认 **2 点**:(A) 回流线 human-on-the-loop 的确切边界(哪些旋钮允许"确认后自动"、哪些永远手动)；(B) 蓝图两档详略的分界确认(现建器官 vs 未来插槽的清单)。其余(七环节图、价格层范围、Strangler Fig 分期)已可直接进 W 形态草案(refactor-plan 目标态图 / free-essay 全貌 / dev-plan 分期路线)。

---

**Sources**(本轮检索):
- [Modular Architecture for Systematic Quantitative Trading Systems (Medium)](https://hiya31.medium.com/a-modular-architecture-for-systematic-quantitative-trading-systems-2a8d46463570) · [Quantitative Trading System Architecture: A Layered Design (Xu'Blog)](https://xuquant.com/posts/quant-system-overview/) · [Quant Trading Systems: Architecture & Infrastructure (Brenndoerfer)](https://mbrenndoerfer.com/writing/quant-trading-system-architecture-infrastructure)
- [An automated adaptive trading system (Financial Innovation, Springer)](https://link.springer.com/article/10.1186/s40854-025-00754-3)
- [Point-in-Time Data: Critical for Investment Decisions (StarQube)](https://starqube.com/point-in-time-data/) · [Norgate Data — survivorship-free systematic trading data](https://enlightenedstocktrading.com/norgate-data/)
- [Strangler Fig Pattern — Azure Architecture Center (Microsoft Learn)](https://learn.microsoft.com/en-us/azure/architecture/patterns/strangler-fig) · [Embracing the Strangler Fig pattern (Thoughtworks)](https://www.thoughtworks.com/en-us/insights/articles/embracing-strangler-fig-pattern-legacy-modernization-part-one)
- [Target Architecture — TOGAF Standard 9.2, Architecture Deliverables (Open Group)](https://pubs.opengroup.org/architecture/togaf9-doc/arch/chap32.html)
