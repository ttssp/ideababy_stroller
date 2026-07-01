# Forge v1 · 009 · P2 · Opus47Max · 参照系评估(SOTA 对标)

**Timestamp**: 2026-07-01T (Phase 2)
**Searches used**: 6 web searches(backtest 偏差方法论 / deflated Sharpe & PBO / 时序异质图谱金融 / 决策日记+量化先例 / TipRanks 分析师 alpha 度量 / 回测框架分层架构)。
**Visibility**: 已读对方 P1-GPT55xHigh.md(refresh);自己 P1 refresh;forge-config refresh;moderator-notes 不存在。
**Reviewer stance**: 审阅人 — 用 SOTA 校准 P1 的 first-take,不引入新标的。

## 0. 本轮做了什么

读对方 P1:GPT-5.5 与我 P1 **强对齐** —— 同样 refactor 架构(显式重划 008 证据 / StrategyModule 信号 / 回测验证 / 004 纪律四层)、同样 keep 愿景(前提:回测真连"顾问可信度↔纪律校准")、同样 new-first 回测、同样图谱降级、同样 keep 红线。**唯一措辞差**:GPT 把图谱叫 "later hypothesis",我叫 "defer 到 v2+ gated" —— 实质同。GPT §3 第 2 问("融合信号评分怎样不被 UI 误读成红线 #9 禁止的权威综合")与我 §1B 的"蒸馏措辞危险"是同一条边界焦虑的两个切面 —— 这是双方共同锁定的**最高优先级待钉点**。

下面用 SOTA 把 P1 的四个倾向逐一压到证据上。

## 1. SOTA 对标

| 主题 | SOTA 现状(检索证据) | 对 009 的启示 |
|---|---|---|
| **分析师 alpha 验证** | TipRanks(Cornell 金融系合作)是成熟工业方案:对每个分析师算 ①Success Rate/Hit Ratio ②Avg Return per rec ③**Z-test 判断是技能还是运气**,且按 sector 波动率校正(防高波动板块刷分)、可换 S&P500 基准算超额。E*Trade 已集成。 | K#3"验证分析师 alpha"**不是空想,有工业先例可抄方法论**。009 回测层的分析师评估头 = TipRanks 三件套(命中率+平均超额+Z 显著性),不必重新发明指标。直接回答 GPT P2 §3 第 1 问(最小样本/持有期/基准/成本口径)。 |
| **回测过拟合防御** | Deflated Sharpe Ratio + Probability of Backtest Overfitting(Bailey & López de Prado):**少数几个策略配置就能刷出高模拟 Sharpe**,记忆效应让过拟合策略 OOS 系统性跑输。DSR 按 trial 数 + 偏度 + 峰度 deflate 显著性阈值;必须记录"试了多少次回测"才能正确 deflate。 | K#3"防过拟合/训练集污染"**有硬核统计武器**。009 回测引擎须内建:①walk-forward / OOS 分割 ②交易成本(slippage)③**trial-count 记账 + DSR**。这把 operator"用算法强项补投资短板"落到实处 —— 这正是工程能补 domain 的地方。 |
| **回测架构分层** | 标准分层:point-in-time 数据摄取层 → 向量化计算层 → 策略/风险层,各层经接口半独立。**向量化**(快·适合原型·假设次 bar 成交)vs **事件驱动**(高保真·建模 slippage/部分成交·复杂)。数据层是"唯一行情来源",信号必须只用过去信息、持仓相对数据滞后。 | 直接回答我 P1 §3 第 2 问("一个引擎两用 vs 两引擎共享数据源")。答案:**共享一个 point-in-time 数据层(枢纽),两个评估头** —— calibration 头(我的决策 vs 反事实)和 alpha 头(分析师方向 vs 真实股价)。一套数据两用 = 数据层共享,指标头分离。009 v1 用向量化够了(低频·原型),事件驱动留 later。 |
| **时序异质图谱在金融** | 学术活跃但**已知重坑**:①关系图靠 handcrafted labeling 或 NLP 抽取,"资源消耗重、准确率低",且**易被单边新闻/不准的抽取模型误导** ②>4M 边时计算复杂度**prohibitive**,要靠动态边采样才能 scale ③难捕捉风险传播的非线性多关系本质。多为机构级数据规模论文。 | **强化我 P1 的 defer 判断**,且给出可验证理由:图谱的关系边依赖 NLP 抽取 —— 而 008 forge v4 已把"提取可靠性"标为中等易错。**图谱会把 008 的抽取脆弱性二次放大**(边错→图错→信号错)。对单人自用规模,图谱是"institutional-scale 才回本"的赌注。defer 到 v2+,gated 在"回测证明信号有价值 + 简单结构撑不住"。 |
| **决策纪律 + alpha 引擎合并先例** | 行为金融文献明确推荐**组合**:Ulysses 契约(书面预承诺)+ 决策日记(识别 bias 模式)+ **隔离反思时间与执行时间** + 量化信号降低情绪偏差。"行为缺口"(基金回报 vs 投资者实际回报)2014-24 年达 1.5-3%/年。但**未检索到把这套整合成单一产品的先例** —— 各组件成熟,集成是空白。 | 直接回答我 P1 §3 第 1 问("集合体 vs 拆开做")。**004 承诺壳 = Ulysses 契约 + 决策日记的工程实现;隔离反思/执行 = 上下游分层。组合是有文献背书的正解,但市面无整合品 → 009 的架构级价值正在"集成本身"**。这不是 V4 过度设计 —— 是填一个文献认证、产品空白的缝。但"价值在集成"意味着:**若集成做不干净(边界糊),价值立刻归零**,退化成 004+008 的大包装(GPT P1 原话同此担忧)。 |

## 2. 用户外部材料消化

K 内无额外 URL / 文件;X 的 5 个标的(proposal §009 / 004 PRD / 008 PRD / 008 forge-v4 / 004 strategy 代码)已在 P1 一手消化完毕,本轮无新增外部材料。SOTA 证据全部来自上表 6 次检索,无 operator 私有材料待叠加。

## 3. 修正后的视角(P1 哪些站住、哪些被推翻)

**站得更稳的(SOTA 加固)**:
- **回测 new-first** —— TipRanks 证明指标可抄、DSR/PBO 证明过拟合可防;回测从"听起来对"升级为"有成熟方法论可落地的工程任务"。P1 倾向不变,信心↑。
- **图谱 defer** —— 从"我怕过度设计的直觉"升级为"有证据的判断":NLP 关系抽取放大 008 既有脆弱性 + 机构级数据才回本。P1 判断不变,理由更硬。
- **两灵魂共存 / 闭环有价值** —— 行为金融文献明确背书"承诺壳+量化信号"组合,且无整合先例。P1"非 V4"判断站住。

**需要补强/修正的**:
- **集合体 vs 拆开做(我 P1 §3 最大不确定)有了更清晰答案,但带条件**:文献支持"合"(组合有价值、市面空白),但价值**全锁在"集成质量"**上。所以我从 P1 的"倾向合但不确定"修正为:**合,但 verdict 必须把"集成边界"作为头号交付物**(否则就是松耦合演进更省)。这给 P3R1 的关键分歧埋了伏笔:009 该是"统一壳"还是"004 v1.0 加回测 lane + 008 接口"的松耦合 —— **判据 = 集成边界能否被契约化钉死**。
- **红线 #9 的边界**(GPT 最关切)从模糊变可操作:SOTA 的"信号融合"(如 ensemble 评分)在 004 语境下**必须落成"又一个独立信号 lane(alpha 回测得分),仍不合并、仍人最终拍板"**,UI 上呈现为冲突报告的新增一列而非"权威综合分"。蒸馏(proposal 第[4]条)同理 —— 落成独立 lane 则不破红线 #1/#9,落成"自主分析"则越界。这条 P3R1 必须钉成硬约束。

**给 P3R1 的收敛预告**:双方 P1+P2 已高度对齐,核心待收敛只剩 **2 条**:(A) 009 集成形态 —— 统一壳 vs 松耦合演进(判据:边界可否契约化);(B) 上游"信号融合/蒸馏"与红线 #9 的精确边界(判据:独立 lane vs 权威综合)。其余(回测先、图谱后、keep 地基、keep 纪律)已无分歧,R2 重点应放在 W 形态草案(PRD draft / refactor-plan / dev-plan / decision-list)。

---

**Sources**(本轮检索):
- [The Deflated Sharpe Ratio (Bailey & López de Prado, SSRN)](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2460551) · [Deflated Sharpe ratio — Wikipedia](https://en.wikipedia.org/wiki/Deflated_Sharpe_ratio) · [Minimum backtest length & deflated SR](https://stefan-jansen.github.io/machine-learning-for-trading/08_ml4t_workflow/01_multiple_testing/)
- [How Analysts are Ranked — TipRanks](https://www.tipranks.com/glossary/h/how-analysts-are-ranked) · [How Experts are Ranked — TipRanks](https://www.tipranks.com/experts/how-experts-ranked)
- [Temporal & Heterogeneous GNN for Financial Time Series (ACM CIKM)](https://dl.acm.org/doi/10.1145/3511808.3557089) · [Spatio-Temporal Decoupled Heterogeneous Graph for Systemic Risk (Springer)](https://link.springer.com/chapter/10.1007/978-981-95-3462-3_9)
- [Vector-Based vs Event-Based Backtesting (IBKR)](https://www.interactivebrokers.com/campus/ibkr-quant-news/a-practical-breakdown-of-vector-based-vs-event-based-backtesting/) · [Building a Robust Backtesting Framework — Event-Driven (QuantJourney)](https://quantjourney.substack.com/p/i-have-never-seen-bad-backtest-3n)
- [How Behavioral Discipline Drives Investment Returns](https://howardcmfunds.com/mind-over-markets-how-behavioral-discipline-drives-investment-returns/) · [Investment Discipline: Hidden Driver of Long-Term Performance](https://eco3min.fr/en/investment-discipline-long-term-performance/)
- [Problems in Backtesting and Biases in Data (AnalystPrep CFA)](https://analystprep.com/study-notes/cfa-level-2/problems-in-backtesting/) · [Survivorship Bias in Backtesting (LuxAlgo)](https://www.luxalgo.com/blog/survivorship-bias-in-backtesting-explained/)
