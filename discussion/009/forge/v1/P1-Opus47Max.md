# Forge v1 · 009 · P1 · Opus47Max · 独立审阅(no search)

**Timestamp**: 2026-06-30T16:56:58Z
**Searches used**: NONE in this round.
**Visibility**: I did NOT read other reviewer's P1.
**Reviewer stance**: 审阅人 — 评判已存在物(004/008 现状 + 已 ship strategy 代码 + 闭环 proposal),不是 daydream。

## 0. 我读到的标的清单 + 阅读策略

- 我读了(全部 5 个 X 标的):
  - `proposals/proposals.md` §009(闭环 proposal:四条想法 + 第一性原理 + 复用清单 + forge 该审的四问)。
  - `discussion/004/004-pB/PRD.md`(全文 · 决策账本/承诺壳 · 红线 #1/#9 · §6 v1.0 已规划 backtest)。
  - `discussion/008/008-pB/PRD.md`(采集层现状 · 008↔004 接口 US6)+ `discussion/008/forge/v4/stage-forge-008-v4.md`(信号 spike 硬前置 verdict)。
  - `/home/ys/codes/XenoDev/projects/004-pB/src/decision_ledger/strategy/` 10 个 .py(base.py IDL / advisor_strategy / xgboost_model / correlation_audit / registry / feature_engineering 等,一手读)。
- 我跳过的:无。XenoDev 在本机可达。
- **K(用户判准)摘要**:operator 要把分散的 004/008 + 四条新想法合成**投资决策闭环**。第一性原理 = **用工程强项补投资 domain 短板**(他懂算法不懂投资)。闭环灵魂已定 = 承诺壳(下游纪律)与 alpha 引擎(上游信号)**共存不冲突**,**别建议推翻 004 红线**(它们管下游执行层)。最在乎:① 闭环架构+004/008 怎么干净并入(复用已 ship 的 strategy 层)② 集合体是否真有架构级价值 or V4 式过度设计 ③ 回测怎么作两灵魂公共地基先落地 ④ 四条排期(图谱该不该现在上)。binding:投资 domain 判断要可验证依据 / 防 build runtime 静默定方向 / 合规不审 / 自用单人。
- **我的阅读策略**:Y=架构集成 → 优先把 004 strategy 层(实际 ship 了什么)与 proposal 的四条逐一对齐,找"已有地基 vs 要新建"的接缝;Y=愿景成立性 → 把 004 红线哲学与 alpha 引擎方向对照,验证"两灵魂共存"在架构上是否真成立;Y=可行性 → 重点看 correlation_audit/xgboost 这两个 backtest-adjacent 件;Y=工程纪律 → 看 StrategyModule IDL 的隔离约束。

## 1. 现状摘要(按 Y 视角组织)

### 视角 A · 架构设计/集成

**关键事实(改变整个判断):004 已经 ship 了闭环"信号层"的实质骨架,而且比 proposal 说的还多。** 不只是 StrategyModule 协议 IDL(`base.py`:source_id+analyze→StrategySignal,多 lane 各自独立),还有:① `xgboost_model.py`+`feature_engineering.py`+`train.py` 真 XGBoost lane(RSI/MACD/量价);② `advisor_strategy.py` 把分析师周报建模成一个信号 lane(读 `structured_json:{ticker:{direction,confidence}}`);③ **`correlation_audit.py` 已经在做"模型预测 vs 分析师"的 Pearson 相关性 audit(O9),含 strict anti-stub 校验 + 60-day window**;④ `registry.py` 注册四个 lane(advisor/placeholder/agent_synthesis/xgboost)。

**所以 009 的"信号/策略层"和"回测验证层"不是从零——004 已有可复用地基。** proposal 第[1][2]条(验证分析师 alpha + 多信号策略)正好压在这套已 ship 的多 lane + correlation_audit 之上。008 这边 forge v4 刚定了"信号可靠性 spike 硬前置 + 008↔004 消费契约(可溯源证据+置信度)",与 009 回测层是同一条缝的两段。**闭环的物理骨架其实大半已存在,009 的真问题是"集成 + 补缺口(回测/图谱)+ 划边界",不是重造。**

### 视角 B · 产品价值/愿景成立性

**"两灵魂共存"在架构上确实成立,而且 004 自己的设计就预留了。** operator 的洞察(alpha 引擎在上游"该信什么"、承诺壳在下游"执行不走样")不是事后弥合——004 的 StrategyModule IDL **本来就是"多信号源各自独立、不合并"**(红线 #9),冲突报告把"分析师/模型/agent 综合"摆成三列让人看分歧。这套架构**天然容得下"上游多信号"**:再加一个"分析师 alpha 回测得分"信号 lane、一个"图谱衍生信号"lane,都不破红线 #9——因为它们仍是独立列,不合并成权威综合。

**真正的张力(也是 V4 风险所在)**:proposal 第[4]条"**蒸馏分析师技能成自给自足的自主分析**"——这个若做成"系统自动产出权威综合判断/自动跟单",会撞红线 #1(自动下单)+ #9(不合并)。但若做成"多一个蒸馏出来的信号 lane(仍独立、仍人最终拍板)",则不破。**边界全在"蒸馏出的东西是独立信号还是权威决策"。** operator 说"别推翻红线"——好,那蒸馏就必须落成"上游又一个独立信号源",而非"替代人决策的自主引擎"。这条 K 已经隐含,但 proposal 第[4]条的措辞("自给自足""自主分析")危险地滑向越界侧,需在 verdict 里钉死。

### 视角 C · 可行性/风险(回测+图谱)

**回测作"两灵魂公共地基"是 K#3 的核心,且 004 已有半个原型。** `correlation_audit.py` 已经证明:这套架构能算"信号源之间的统计关系"、能 strict-reject 假数据。把它扩成"**用历史发布的分析师判断 + 之后真实股价,回测他的方向准确率/alpha**"是自然延伸——但有 operator 自己懂的硬坑:**look-ahead bias / 训练集污染 / 幸存者偏差 / 样本量**(008 的语料只到某时间点、单一分析师、反讽黑话已被 008 forge v4 标为"提取中等易错")。回测的输入质量受限于 008 提取可靠性——**这把 008 forge v4 的 spike 和 009 的回测连成一条依赖链:回测可信 ⊂ 提取可信**。

**时序异质图谱(第[3]条)——我的第一反应是 NOT NOW。** 它是个大数据架构赌注(股票/公司/事件异质节点 + 时间切片),价值锁在"图谱级查询能带来 alpha"这个**未验证假设**上。在分析师 alpha 都还没回测出数字、提取可靠性都还没实测前就上图谱,是典型的"为没验证的用途过度设计"(正是 operator 怕的 V4)。图谱更像 v2+ 的事,gated 在"回测证明信号有价值 + 简单结构撑不住了"。

### 视角 D · 工程纪律

004 的 StrategyModule IDL 隔离约束很干净(constructor 只接 LLMClient+SourceDataProvider 不接 registry、lane 之间不互 import、R9 唯一性)。**009 复用时必须保这套约束**——否则"集成"会退化成把 004/008 的代码搅成一团。correlation_audit 的 strict anti-stub + 真路径 enforce 是好范式(防回测用假数据自欺)。008 那边 forge v4 的"可溯源证据+置信度契约 + 防 V4 条款"也是 009 该继承的纪律。**风险**:009 是"集合体",最容易犯的工程错是边界糊掉——把上游 alpha 层和下游 004 纪律层的代码/数据耦合死,导致改一个动全身。

## 2. First-take 评分(按 Y 视角)

| Y 维度 | 倾向 | 理由(引用 §1 现状) |
|---|---|---|
| 架构设计/集成 | **refactor(集成)+ keep(地基)** | §1A:004 已 ship 的 strategy 多 lane + correlation_audit 是现成地基,keep;009 = 在其上集成 008 采集 + 新建回测/图谱接口 + 划边界,是 refactor 不是 new。 |
| 产品价值/愿景成立性 | **keep(闭环)+ refactor(蒸馏措辞)** | §1B:两灵魂共存架构上真成立(004 IDL 本就多信号不合并),闭环有价值非 V4;但第[4]条"自主分析"措辞危险,须 refactor 成"独立信号 lane"防越界红线。 |
| 可行性/风险(回测+图谱) | **new(回测先)+ defer(图谱)** | §1C:回测是公共地基须最先 new(且接 008 spike 的依赖链);时序图谱 defer 到 v2+,现在上=过度设计。 |
| 工程纪律 | **keep(IDL 约束)** | §1D:004 的 lane 隔离 IDL + correlation strict 范式 + 008 v4 防 V4 条款都该 keep 进 009,守住集成不糊边界。 |

## 3. 我现在最不确定的 3 件事

1. **集合体 vs 拆开做——架构级价值到底够不够撑"合"?** 我倾向"合"(因为 004 已有信号地基、008 已有采集、合起来闭环自洽),但不确定是否值得现在就建统一架构,还是"008 继续供数 → 004 v1.0 加回测 lane"这种**松耦合演进**就够了(不需要 009 这个统一壳)。希望 P2 用 SOTA(有没有人把决策纪律工具+alpha回测合成过、成败如何)+ P3 帮我判:009 是真集成架构,还是其实只需要"004 v1.0 + 008 接口"两个已有 idea 各自演进。

2. **回测"一套数据两用"(训练自己 + 验证分析师)具体怎么落?** K#3 说它是枢纽,但我不确定这两用是不是真能共享一套回测引擎,还是其实是两个不同的东西(calibration 用的是"我的决策 vs 不动的反事实",alpha 验证用的是"分析师方向 vs 真实股价")——它们的数据模型和评估指标可能根本不同。希望 P2 看 SOTA 的回测框架怎么分层、P3 帮我判这是"一个引擎两用"还是"两个引擎共享数据源"。

3. **时序异质图谱的 defer 判断我有多少把握?** 我 first-take 判 NOT NOW,但 operator 直觉它有价值,我不想仅凭"怕过度设计"就否掉。希望 P2 检索:时序异质图谱在金融(尤其个人/小规模)的真实应用与失败案例——它是不是只在机构级数据规模才回本?有没有轻量版能先验证价值?P3 给"图谱该不该现在上 / 什么条件下上"的收敛判断。
