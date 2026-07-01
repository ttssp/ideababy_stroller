---
forge_version: v2
created: 2026-07-01T03:10:04Z
convergence_mode: strong-converge
x_hash: e6abd867709d5d945e3a10b51aa52d4e
prefill_source: manual
---

# Forge Config · 009 · v2

> **009 v2 = 「画目标态蓝图」专项 forge。** v1 已定 verdict(009 = 集成契约 + 共享回测地基,非独立统一壳;回测 new-first 按 DSR/PBO 建;图谱 defer;蒸馏最后独立 lane;004 端永不权威综合分)。**v2 不推翻 v1,而是在其上产一张「闭环目标态架构蓝图」** —— 把 final goal 全貌 + 每个器官边界 + 分期演化路线画彻底,解决 operator 痛点"现在 004/008/四念头各做各的、缺统一方向、架构设计不够充分彻底"。
>
> **与 v1 的关系**:v1 回答"该不该建、怎么建";v2 回答"最终形态长啥样、怎么分期走到那"。v1 stage doc 是 v2 的地基(primary X)。

## X · 审阅标的

(operator 手工 intake · 5 项 · v2 在 v1 基础上加读 004 DB schema 补盲区)

### 解析后的标的清单

- `discussion/009/forge/v1/stage-forge-009-v1.md`(类型:本仓库文件 · forge stage · 339 行)— **核心 X · 蓝图地基**。v1 单一 verdict + Evidence map + decision-list(含 AC-1..AC-5)+ refactor-plan + PRD draft + dev plan + 自批判。v2 蓝图**基于它、不推翻它**。
- `discussion/004/004-pB/PRD.md`(类型:本仓库文件 · 237 行)— 004 承诺壳现状(**下游纪律器官**)。红线 #1/#9/#10 + §6 v1.0 roadmap。
- `discussion/008/008-pB/PRD.md`(类型:本仓库文件 · 315 行)— 008 采集/结构化现状(**上游采集器官**)。008↔004 接口 US6。
- `/home/ys/codes/XenoDev/projects/004-pB/src/decision_ledger/strategy/`(类型:外部 repo 目录 · 10 个 .py)— 004 已 ship strategy 层(**信号器官**)。StrategyModule IDL / correlation_audit / advisor+XGBoost lane / registry。⚠ Codex 沙箱 BLOCK risk(v1 双方均真实读到,无 fallback);若不可达用 v1 stage doc §Intake recap X#5 + config §X-fallback 摘录。
- ⭐ `/home/ys/codes/XenoDev/projects/004-pB/alembic/versions/`(类型:外部 repo 目录 · **13 个 migration** .py)— **v2 新增,补 v1 盲区**。v1 自批判明说"未读 004 的 13 个 alembic migration(DB schema),影响 M3 calibration 头接'004 档案'的代价估计"。蓝图要画"calibration 头↔004 档案"接口,须看 schema。关键文件:`0001_initial_schema.py`(基础表)/ `0010_extend_advisor_reports.py` + `0011_advisor_reports_composite_pk.py`(分析师报告表)/ `0013_add_strategy_xgboost_metadata.py`(strategy 元数据)/ `0002_tab_open_log.py`(决策/开仓日志 → calibration 反事实所需?)。⚠ 同 XenoDev 仓沙箱 risk;若不可达标注,用文件名清单推断表结构。

## Y · 审阅视角

(operator 勾选 4 项 · 为"画蓝图"定制)

✅ **架构设计/目标态** —— 闭环最终形态怎么画、器官怎么切分、器官之间接口契约长啥样、数据怎么流。(核心)
✅ **可演化性/分期路线** —— 从现状(004/008/四念头各自为政)到目标态,分几期走、每期交付啥、gated 在什么条件。**每期必须能独立跑,不是"全做完才有用"**(防 V4)。(核心)
✅ **器官边界清晰度** —— 上游 alpha 层 vs 下游 004 纪律层边界;四个念头(验证alpha/回测/图谱/蒸馏)各自在闭环哪个位置、接口对谁、gated 条件。
✅ **工程纪律** —— 跨器官接口契约怎么定义才能保证器官不糊边界(复用 004 StrategyModule IDL 隔离范式 + v1 的 AC 验收条款)。

## Z · 参照系

mode: **对标 SOTA**

- 双方 Phase 2 各自检索,聚焦"**目标态架构 + 分期演化**"层(不同于 v1 聚焦"回测方法论"):
  - 投资/量化闭环系统的**目标态架构分层**怎么画(端到端 pipeline 的模块边界:数据→信号→决策→执行→复盘→反馈)
  - 个人投资/量化系统的**分期演化路线**先例(从 MVP 到完整闭环怎么切 milestone、每期怎么保持独立可用)
  - 多器官系统的**接口契约设计**范式(event-driven / 契约优先 / 防模块耦合)在金融系统的应用
  - "承诺壳/行为纪律层"与"alpha 信号层"在**同一闭环架构**里怎么分层共存的先例(有没有人画过这种图)
  - 复盘/反馈闭环(backtest → calibration → 纪律旋钮)怎么在架构上闭合
  - **forbidden**:tech-stack-deep-dive / pricing / 具体实施细节 / 重复 v1 已做的回测方法论 SOTA(TipRanks/DSR/PBO 已定,不重刷)
- **合规不在本轮范围**(沿用 operator 已拍板前提)。
- **外部材料叠加**:无额外 URL;X 的 5 个标的即全部一手材料。

## W · 产出形态

(operator 勾选 2 项 + Opus 建议加 1 项 · 均为"蓝图"服务)

✅ **架构 refactor-plan** —— **目标态模块图**:闭环七环节的器官切分 + 器官之间接口契约 + 数据流。这是蓝图的"结构骨架"。
✅ **free-essay** —— **final goal 全貌叙事**:完整闭环最终长啥样,七环节怎么串成自洽反馈环,每个器官补哪个短板。这是蓝图的"愿景全景"。
✅ **next-dev-plan** —— **分期演化路线**(Opus 加):从现状到目标态分几期、每期交付 + gated 条件,每期独立可用。这是蓝图的"落地路线",防"有图无路还是各做各的"。

(verdict-only / decision-list / next-PRD 未勾 —— v1 已产 decision-list + PRD draft,v2 不重复;v2 专注"目标态图 + 演化路线"。)

## K · 用户判准

我要跑 forge 009 v2,是因为 v1 出了 verdict(009 = 集成契约 + 共享回测地基,分期落地,别先建大壳)后,我意识到一个真问题:**现在 004、008、四个新念头更多是"各做各的",缺一张统一的目标态蓝图。** 我担心没有把 final goal 定清楚,会多走弯路,架构设计也不够充分彻底。所以 v2 的目的 = **把 009 闭环的最终形态 + 每个器官边界 + 分期演化路线画彻底,产一张"目标态架构蓝图"**。

**这不是重新质疑该不该建(v1 已定),而是画清"怎么建、最终长啥样、怎么分期走到那"。**

**最重要的 binding(贯穿全程,别违反)**:
1. **死守 v1 verdict 不推翻**。目标态蓝图可以画得完整,但落地路线仍必须是"契约先行、不先建独立统一壳、分期 gated"。**蓝图 ≠ 一次性建完的大工程** —— 这是我最怕的 V4 失败模式。如果你们把蓝图画成"要一口气建完才有用的大系统",就是画错了。目标态图指导方向,但每一期都要能独立跑、独立有价值。
2. **蓝图射程 = 画到"完整闭环能自洽跑起来"为止**:采集(008)→ 结构化/知识 → 信号/策略(StrategyModule)→ 决策 → 纪律执行(004)→ 复盘(回测)→ 反馈(校准旋钮)。四个新念头都在这张图里就位。**不画**更远的(多分析师池、自动化程度提升、机构级扩展)—— 那些是闭环跑通后的事,现在画=画虚。
3. **四个新念头在蓝图里的位置全部钉死**,每个标清"在闭环哪个位置 + 接口对谁 + gated 条件":
   - ① 验证分析师 alpha → 回测层的 **alpha 评估头**(接 008 证据 + 价格数据,产 hit-rate/超额/显著性)
   - ② 回测系统 → **共享 point-in-time 数据层 + 两个评估头(alpha 头 + calibration 头)**,是闭环"复盘/反馈"环节的枢纽
   - ③ 时序异质图谱 → **v2+ 的一个信号 lane(gated)**,gated 在"回测证明简单信号不够 + 008 抽取脆弱性可控";v0.1 不画细,只标位置
   - ④ 蒸馏技能 → **最后做的一个独立信号 lane**,不得替人决策/不得综合打分

**第一性原理(不变)**:我懂算法/自动化/数据,不懂投资。产品本质 = 用工程强项补投资 domain 短板。每个器官按"补哪个短板"定位。

**其他 binding**:① 别让任何子系统(尤其 build runtime)静默替我定产品方向(防 V4);② 008 合规边界(付费自用/有效登录态/不传播)已拍板,不重审;③ 自用单人产品,不商业化;④ 投资 domain 判断给可验证依据(接 v1 的 SOTA + 回测数字),别让我凭感觉。

**我特别想让蓝图回答的几个问题**:
- 闭环七环节里,哪些是"已有器官"(004/008/strategy)、哪些是"要新建器官"(回测层)、哪些是"未来插槽"(图谱/蒸馏)?一张图看清。
- 器官之间的接口契约到底长啥样?尤其"008→回测→StrategyModule→004"这条主链,数据怎么流、每段契约传什么。
- "复盘/反馈"这个环怎么在架构上闭合?回测算出的东西(分析师 alpha 得分、我的纪律校准)怎么回流去调"上游信号给多强、下游纪律卡多严"?这是闭环之所以是"环"的关键,v1 没画透。
- 从现在到目标态,第一期该交付哪个最小可用切片?

---

## X-fallback TEXT(供 Codex 沙箱不可达 XenoDev 仓时使用)

> X#4(strategy 目录)+ X#5(alembic 目录)在 XenoDev 仓。v1 双方均真实读到 strategy 层。Codex 若沙箱不可达 → 用以下摘录 + §0 标注,不 fake-read。

### X#4 摘录 · 004 strategy 层(见 v1 stage doc §Intake recap 更详)

10 个文件:`base.py`(StrategyModule IDL:source_id+analyze→StrategySignal,多 lane 不合并;SourceDataProvider 只读;constructor 只接 LLMClient+SourceDataProvider 不接 registry)/ `advisor_strategy.py`(分析师周报建模成信号 lane)/ `xgboost_model.py`+`feature_engineering.py`+`train.py`(真 XGBoost lane)/ `correlation_audit.py`(信号源相关<0.5 去重 + strict anti-stub + 60-day window)/ `registry.py` / `agent_synthesis.py`(C 列综合但不合并三列)/ `placeholder_model.py`。

### X#5 摘录 · 004 alembic 13 个 migration(DB schema · v2 新增标的)

文件名清单(推断表结构):
- `0001_initial_schema.py` — 基础表(portfolio / positions / decisions?)
- `0002_tab_open_log.py` — 开仓/标签页日志(**calibration 反事实可能所需**:我的决策 vs 不动)
- `0003_notes_fts.py` — 笔记全文检索
- `0004_weekly_maintenance.py` — 周维护
- `0005_telegram_pushes.py` — Telegram 推送
- `0006_learning_quarters.py` — 学习季度
- `0007_onboarding_state.py` — onboarding 状态
- `0008_add_concept_tables.py` — 概念表
- `0009_add_concept_explain_log.py` — 概念解释日志
- `0010_extend_advisor_reports.py` — **分析师报告表扩展**(alpha 头输入源)
- `0011_advisor_reports_composite_pk.py` — 分析师报告复合主键
- `0012_alerts_alert_type_check_extend.py` — 告警类型
- `0013_add_strategy_xgboost_metadata.py` — **strategy XGBoost 元数据**(信号 lane 元数据)

**对蓝图的意义**:calibration 头要接"004 档案"做反事实(我的决策 vs 不动),需确认 `0001`/`0002` 是否已有"决策时点 + 持仓快照 + 不动基线"字段;alpha 头要接 `0010`/`0011` 的分析师报告表。若这些字段已存在 → M3 calibration 头代价低;若缺 → 需新 migration。Codex 若可读则以原文 migration 的 `op.create_table`/`op.add_column` 为准。
