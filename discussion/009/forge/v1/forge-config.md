---
forge_version: v1
created: 2026-06-30T16:56:58Z
convergence_mode: strong-converge
x_hash: a6d5fa654522c47682e431c8b055d6df
prefill_source: manual
---

# Forge Config · 009 · v1

> **009 = 统领性集合体 idea**「投资决策闭环」。把已分散建的 004(决策账本/承诺壳)+ 008(投顾采集)+ operator 四条新想法(验证分析师 alpha / 回测 / 时序异质图谱 / 蒸馏技能)合成完整闭环:信息收集 → 结构化/知识 → 信号/策略 → 决策 → 纪律执行 → 复盘 → 反馈。forge v1 核心任务 = 审定闭环架构 + 004/008 如何并入 + 哲学边界(上游 alpha 引擎 vs 下游 004 纪律红线)+ 四条排期。
>
> **forge-first 启动**:009 无 L1/L2/L3(见 FORGE-ORIGIN.md)。proposal §009 是 primary X。

## X · 审阅标的

(operator 经 AskUserQuestion 勾选 4 项 · manual intake)

### 解析后的标的清单

- `proposals/proposals.md` §009 段(类型:本仓库文件 · proposal · 行 266 起到 EOF)— **核心 X**。四条想法 + 第一性原理 + 复用清单 + forge 该审的四个问题全在此段。Codex 读时定位 `## **009**` 段。
- `discussion/004/004-pB/PRD.md`(类型:本仓库文件 · 237 行)— 004「决策账本/承诺壳」现状。重点:§1 Problem(约束>信息·Barber-Odean)、§5 Scope OUT 红线(#1 自动下单永不破 / #9 信号永不合并成权威综合)、§6 Phased roadmap(v1.0 已规划"私有模型 backtest+实盘对比"+"模型 tutor")。**判哲学边界的必读**。
- `discussion/008/008-pB/PRD.md`(类型:本仓库文件 · 315 行)— 008 采集/结构化层现状(phased · v0.1/v0.2 已 ship)。008↔004 接口现状(US6 给 004 轻量包)。
- `discussion/008/forge/v4/stage-forge-008-v4.md`(类型:本仓库文件 · forge stage)— 008 刚出的 forge v4 verdict(信号可靠性 spike 硬前置 / 008↔004 消费契约 / 字典三层)。**与 009 回测层直接衔接**。
- `/home/ys/codes/XenoDev/projects/004-pB/src/decision_ledger/strategy/`(类型:**外部 repo 目录** · 10 个 .py)— 004 已 ship 的"信号引擎半个骨架"。⚠ **Codex 沙箱 BLOCK risk**(在 XenoDev 仓)。关键文件:`base.py`(StrategyModule 协议 IDL:source_id+analyze→StrategySignal,锁死"多信号源不合并")/ `xgboost_model.py`+`feature_engineering.py`+`train.py`(真 XGBoost lane)/ `correlation_audit.py`(信号源相关性<0.5 去重)/ `advisor_strategy.py`(分析师内容建模成信号源)/ `registry.py` / `agent_synthesis.py`。Opus 端已读 base.py;Codex 若沙箱不可达 → P1 §0 标 "skipped due to access",用本 config §"X-fallback TEXT" 摘录评价,**不 fake-read**。

## Y · 审阅视角

(operator 勾选 4 项)

✅ **架构设计/集成** —— 闭环怎么搭、004/008 怎么并入、哪些复用哪些重构、模块边界。(核心)
✅ **产品价值/愿景成立性** —— 集合体相对分散的 004+008 是否真有架构级价值?还是 V4 式过度设计?闭环哲学(两灵魂共存)立不立得住?(核心)
✅ **可行性/风险(回测+图谱)** —— 回测系统怎么验证分析师 alpha(防过拟合/训练集污染)、时序异质图谱该不该现在上(还是过度设计)。
✅ **工程纪律** —— 跨模块契约/接口隔离/渐进交付;004 的 StrategyModule IDL 复用时怎么保接口约束。

## Z · 参照系

mode: **对标 SOTA**

- 双方 Phase 2 各自检索领域 SOTA,聚焦闭环/投资系统层:
  - 量化平台/回测框架(QuantConnect / Backtrader / zipline / vectorbt)的架构与已知坑
  - 多信号融合 / signal ensemble / 投顾观点量化验证的方法与失败案例
  - 决策日记 / 行为纪律工具 与 alpha 引擎结合的先例(有没有人这么合过)
  - 时序异质图谱(temporal heterogeneous graph)在金融的应用与失败案例(是否值得现在上)
  - 单分析师 alpha 验证 / 信号回测 防过拟合-训练集污染的标准做法
  - **forbidden**:tech-stack-deep-dive / pricing / 具体实施细节
- **合规不在本轮范围**(008 的付费自用/有效登录态/不传播是 operator 已拍板前提,沿用)。
- **外部材料叠加**:无额外 URL;X 的 5 个标的即全部一手材料。

## W · 产出形态

(operator 勾选 4 项)

✅ **next-PRD draft** —— 009 闭环的下一版 PRD 草案(可回流起 009 的 L4 / 或指导 004/008 怎么改)。
✅ **架构 refactor-plan** —— 按模块分组的闭环集成方案:004/008/回测层/图谱层怎么拼,复用 vs 重构清单。
✅ **next-dev-plan** —— 按 phase/milestone 切的开发计划(四条怎么排期,哪个先做哪个 gated)。
✅ **decision-list 矩阵** —— 004/008/四条 各组件的 保留/调整/删除/新增 4 列矩阵。

## K · 用户判准

我要 forge 009 这个**投资决策闭环集合体**,是因为我已经分散建了 004(决策账本/承诺壳)和 008(投顾采集),还有四条新想法(验证分析师 alpha / 回测 / 时序异质图谱 / 蒸馏技能),现在想把它们合成一个完整闭环:信息收集 → 结构化/知识 → 信号/策略 → 决策 → 纪律执行 → 复盘 → 反馈。

**第一性原理(最重要的 context,贯穿全程)**:我懂算法、自动化、数据,但**不懂投资,没有专业知识和经验**。这个产品的本质 = **用我的工程强项补齐我的投资 domain 短板**。所以每个器官按"补哪个短板"定位:投资知识/纪律靠外部专家(008 采集投顾内容)、策略能力靠外部信号+我自己内测的回测系统、"这个分析师到底行不行"靠回测数据说话、执行不走样靠 004 的纪律承诺壳。

**闭环的灵魂我已经定了(关键,别再纠结二选一)**:"承诺壳"(防我乱动)和"alpha 引擎"(验证/信号/策略)**不冲突、永久共存、分居上下游**——alpha 引擎在上游回答"该信什么、用什么策略",承诺壳(004)在下游保证"信了之后执行不走样"。回测数据只是决定"上游信号给多强、下游纪律卡多严"的旋钮。**所以请不要建议我把 004 的红线推翻**(#1 自动下单永不破 / #9 信号不合并),那些红线管的是**下游执行层**(004 域内仍成立),不约束**上游信号/回测层**(新域)。

**我最在乎、要你们替我盯死的几件事**(按重要性):
1. **闭环架构怎么搭、004/008 怎么干净并入**:哪些复用 004 已 build 的 strategy 层(StrategyModule IDL / XGBoost / correlation_audit / 分析师建模 / DB schema,这些是真金白银已 ship 的,别浪费)、哪些要重构、上游 alpha 层和下游 004 纪律层的边界怎么划清。
2. **这个集合体相对"分散的 004+008"是否真有架构级价值**——还是会变成又一个 V4 式的过度设计(我踩过 V4 失败模式,很怕重蹈)。如果你们判断它该拆开做、不该合,请直说。
3. **回测系统怎么作为两灵魂的公共地基先落地**:它既要训练我自己(承诺壳的 calibration),又要验证分析师有没有 alpha。这个"一套数据两用"是闭环的关键枢纽,怎么设计才不偏废。回测要防过拟合/训练集污染(我懂算法,这条我能听懂技术细节)。
4. **四条想法怎么排期**:尤其**时序异质图谱该不该现在上**——我直觉它能更全面覆盖股市动态,但也可能是过度设计。回测/验证是不是该最先落地(因为它是"判断分析师可不可信"的地基,不验证清楚后面全是空中楼阁)。蒸馏技能是不是最后做。

**贯穿全程的 binding**:① 我不懂投资,所以涉及投资 domain 的判断请给我**可验证的依据**(回测数字、SOTA 证据),别让我凭感觉拍;② 别让任何一个子系统(尤其 build runtime)**静默替我定产品方向**(防 V4);③ 008 的合规边界(付费自用、有效登录态、不传播)是 operator 已拍板的前提,不在本轮重审;④ 这是自用单人产品,不商业化。

---

## X-fallback TEXT(供 Codex 沙箱不可达 XenoDev 仓时使用)

> X#5(`/home/ys/codes/XenoDev/projects/004-pB/src/decision_ledger/strategy/`)在 XenoDev 仓。Opus 端已读 base.py 全文。Codex 若沙箱不可达 → 用以下摘录评价 + §0 标注,不 fake-read。能直接读则以原文件为准。

### X#5 摘录 · 004 已 ship 的 strategy 层(信号引擎半个骨架)

10 个文件:`base.py` / `advisor_strategy.py` / `xgboost_model.py` / `feature_engineering.py` / `train.py` / `correlation_audit.py` / `placeholder_model.py` / `registry.py` / `agent_synthesis.py` / `__init__.py`。

**`base.py` — StrategyModule 协议 IDL(架构枢纽 · architecture.md §3.1)**:
- `StrategyModule` Protocol:仅 `source_id` + `analyze()`,**不含** conflict_resolve / devil_advocate(IDL 锁死)。
- `SourceDataProvider` Protocol:lane 唯一可读数据来源(只读,不暴露 registry / 其他 lane)。方法:`get_advisor_report(advisor_week_id)` / `get_portfolio()` / `get_ticker_meta(ticker)` / `get_env_snapshot()`,全返回不可变 dataclass 或 None。
- constructor 强制仅接受 `(LLMClient, SourceDataProvider)`,不接受 registry(不变量 #14 · contract-level lane 隔离)。
- `@runtime_checkable`。
- **架构意图**:多个信号源(分析师 / XGBoost / LLM)各自实现 StrategyModule,**互不合并、各自独立产 StrategySignal**(对应 004 红线 #9"信号永不合并成权威综合")。

**`StrategySignal` 域模型**(domain/strategy_signal.py):含 `direction` / `confidence` / `rationale_plain`。

**已实装的信号 lane**:
- `xgboost_model.py` + `feature_engineering.py` + `train.py`:真 XGBoost 私有模型(004 v0.2.3 ship),技术指标特征(RSI/MACD/量价)+ 训练流水线。
- `advisor_strategy.py`:把分析师周报(`AdvisorWeeklyReport`,含 `structured_json: {ticker:{direction,confidence}}`)建模成一个信号源 lane。
- `correlation_audit.py`:信号源之间相关系数<0.5 才有冲突价值的审计(去重)。
- `placeholder_model.py`:占位信号(v0.1)。
- `registry.py`:信号源注册表。
- `agent_synthesis.py`:agent 综合(004 冲突报告的 C 列,但**不合并**三列)。

**对 009 的意义**:这是闭环"信号/策略层"的现成地基。009 要做的"多信号回测 + 分析师 alpha 验证",StrategyModule IDL + correlation_audit + advisor 建模可直接复用;XGBoost lane 是现成的第二信号源。**关键张力**:这套接口是在 004"承诺壳·不合并信号"哲学下设计的,009 上游 alpha 层若要"融合信号出可信策略",与红线 #9 的边界须 forge 划清(K#1)。
