# Forge v1 · 009 · P1 · GPT-5.5 xhigh · 独立审阅(no search)

**Timestamp**: 2026-07-01T01:08:34+08:00
**Searches used**: NONE in this round.
**Visibility**: I did NOT read other reviewer's P1.
**Reviewer stance**: 审阅人 — 评判已存在物,不是 daydream。

## 0. 我读到的标的清单 + 阅读策略

- 我读了:`forge-config.md`/proposal §009/004 PRD/008 PRD/008 forge v4/XenoDev 004 strategy 层/forge-protocol P1 template/`FORGE-ORIGIN.md`。X#5 真实可读,读了 `base.py`,`advisor_strategy.py`,`xgboost_model.py`,`correlation_audit.py`,`registry.py`;未用 fallback 摘录。
- 我跳过的:无。`moderator-notes.md` 不存在;我没有读取 `P1-Opus47Max.md`。
- **K(用户判准)摘要**:用户要用工程强项补投资 domain 短板。闭环灵魂已定:上游 alpha 引擎回答“该信什么”,下游 004 承诺壳保证“信了之后不乱动”;不要推翻 004 红线 #1 自动下单永不破、#9 三路信号不合并。最在乎闭环架构、004/008 干净并入、回测作为公共地基、四条新想法排期,尤其图谱是否过早。
- **我的阅读策略**:先按 004/008 的既有边界确认不可破红线,再看已 ship strategy 层能复用到什么程度,最后用 008 v4 的可靠性 gate 校准 009 上游 alpha 的落地顺序。

## 1. 现状摘要(按 Y 视角组织)

### 架构设计/集成

009 不是新单点功能,而是把 008 输入层、strategy 信号层、回测/验证层、004 承诺壳串成闭环。008 PRD 当前只负责采集、结构化、可溯源轻量包,不产投资建议;008 forge v4 进一步把出口收窄为“可溯源证据 + 置信度”契约。004 PRD 定位为下游承诺壳,三列冲突报告保留分歧,自动下单和权威综合永久 OUT。X#5 显示 strategy 层已有 `StrategyModule`/`SourceDataProvider` IDL、advisor lane、XGBoost lane、correlation audit 和 registry,但 lane 隔离、只读 provider、默认 fail-closed 都是硬约束。

### 产品价值/愿景成立性

004 解决的是“知道很多但压力下乱动”,008 解决的是“顾问内容漏、散、难复用”。009 的新增价值来自把“顾问是否可信”“我自己的信号是否独立”“执行纪律该卡多严”放到同一数据闭环里。proposal 已明确 004/008 不被替代,而是重定位为子系统。这个集合体的价值不在更大,而在回测把上游可信度和下游纪律校准连起来。

### 可行性/风险(回测+图谱)

008 v4 已把信号可靠性 spike 作为机器可信跟单的硬前置,因为 stance/conviction/action 的错标会直接变成亏损风险。004 的 correlation audit 已有 60-day window、独立模型预测、stub reject、零方差 fail-closed 等纪律,说明回测地基有一部分真实骨架。时序异质图谱目前只在 proposal 里作为设想出现,还没有与 008 字典三层、004 strategy IDL 或回测指标形成现状契约。

### 工程纪律

现有边界总体清楚:004 不自动下单、不合并三列、不把不动当失败;008 不给建议、不静默漏采、原文可回溯;strategy lane 不互读、不拿 registry、不默认产假信号。XGBoost lane 甚至默认不注册/无 provider 时 fail-closed。风险在于 009 作为集合体容易让 build runtime 把“上游 alpha 融合”静默写成 004 域内综合建议,这会穿透既有红线。

## 2. First-take 评分(按 Y 视角)

| Y 维度 | 倾向 | 理由(引用 §1 现状) |
|---|---|---|
| 架构设计/集成 | refactor | 需要重定位边界:008=证据,StrategyModule=信号 lane,回测=验证层,004=执行纪律。不是推翻现有系统,而是把接缝显式化。 |
| 产品价值/愿景成立性 | keep | 集合体有架构级价值,前提是回测真连接“顾问可信度”和“纪律校准”;否则只是 004+008 的大包装。 |
| 可行性/风险(回测+图谱) | new | 回测/alpha 验证应作为新增地基先落;图谱现在应至少降级为 later hypothesis,未见足够现状依据支撑先做。 |
| 工程纪律 | keep | 004/008/strategy 既有红线值得保留,尤其 lane 隔离、可溯源、fail-closed;009 只能在上游新域扩展,不能反向污染 004。 |

## 3. 我现在最不确定的 3 件事

1. 分析师 alpha 验证的最小可决策样本、持有周期、基准和交易成本口径是什么;P2 需要看回测/单分析师验证的标准做法。
2. 上游 alpha 层是否允许“融合信号”形成策略评分,以及这个评分怎样不被 004 UI 误读成红线 #9 禁止的权威综合。
3. 时序异质图谱是否真能补投资短板,还是只是把 008 第三层字典和图结构提前复杂化;P2 需要看金融图谱的收益与失败条件。
