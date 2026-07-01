# Forge v1 · 009 · P2 · GPT-5.5 xhigh · 参照系评估(with search)

**Timestamp**: 2026-07-01T01:25:20+08:00
**Searches run**: 6, SOTA-benchmark
**Visibility**: 我已读对方 P1。

## 1. SOTA 对标

| 标的 X' | 参照项 | 它怎么做 | 我们怎么做 | gap | URL/Source |
|---|---|---|---|---|---|
| 闭环架构 | QuantConnect Algorithm Framework | 把 Universe/Alpha/Portfolio/Risk/Execution 分层,模块按顺序流动,且强调 separation of concerns。 | 004 已有 StrategyModule lane,008 是证据层,004 是执行纪律层。 | P1 的四层判断站住;但 009 不该先做“大统一壳”,应先把层间契约钉死。 | https://www.quantconnect.com/docs/v2/writing-algorithms/algorithm-framework/overview |
| 回测/alpha 验证 | PBO + Deflated Sharpe Ratio | PBO 用 CSCV 估计回测过拟合概率;DSR 校正多次试验、选择偏差和非正态收益。 | 004 只有 Pearson correlation audit 雏形。 | Pearson 不足以判 alpha;必须记录 trial 数、样本窗、基准、交易成本、选择偏差。 | https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253 / https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2460551 |
| 分析师 alpha | Sell-side analyst report 文本研究 | 2025 arXiv 用 1.2M 份报告和 LLM/ML 发现文本叙事可带来增量预测信息。 | 009 要验证单一投顾,008 已能沉淀文本证据。 | 方向站住:分析师文本值得测;但不能凭主观信任进入跟单,要逐条 point-in-time 回测。 | https://arxiv.org/abs/2502.20489 |
| 承诺壳/纪律 | Barber-Odean 个人投资者研究 | 高交易频率散户净收益显著差,过度交易解释了损失。 | 004 用承诺壳约束冲动,且不自动下单。 | 004 红线不但站住,还应作为 009 下游边界;alpha 强也不推出自动执行。 | https://faculty.haas.berkeley.edu/odean/papers%20current%20versions/individual_investor_performance_final.pdf |
| 时序异质图谱 | THGNN 金融图谱论文 | 图谱可能提升预测,但关系图若靠人工/NLP 构建,资源重、准确率低、关系动态变化。 | 009 图谱仍是 proposal 设想,008 提取可靠性刚被 v4 标为前置风险。 | P1 的 defer 判断站住:现在上会放大 008 抽取脆弱性;只能 gated 在回测证明简单信号不够之后。 | https://arxiv.org/abs/2305.08740 |
| 防 look-ahead | Look-Ahead-Bench | 金融 LLM 评估必须区分真实预测能力和记忆/未来信息泄漏。 | 009 会用 LLM 解析投顾内容并回测。 | 回测层必须 point-in-time;任何摘要、结构化、价格数据都要按当时可见时间戳入库。 | https://arxiv.org/abs/2601.13770 |

## 2. 用户外部材料消化

本轮 K 内无新增外部 URL/文件;X 的 5 个标的就是全部一手材料。本节无额外材料可吸收,也无外部材料改方向。

## 3. 修正后的视角

- P1 判断“回测/alpha 验证应作为新增地基先落” → **站住并加强**。PBO/DSR 与 look-ahead SOTA 说明,回测不是普通报表,而是防自欺的统计纪律层。
- P1 判断“图谱先降级为 later hypothesis” → **站住**。THGNN 证明图谱有潜力,但也明确关系构建重且易错;009 现在缺的是可靠 alpha 验证,不是更复杂结构。
- P1 判断“集合体有架构级价值” → **部分修正**。价值成立,但形态更像契约化松耦合演进,不应先追统一壳;这也回应 Opus 分歧 A。
- P1 第 2 个不确定点“信号融合怎样不破 #9” → **被压实为边界**。上游可做独立 lane/评分供回测,但落到 004 只能显示为可溯源独立信号,不能变权威综合分;这回应 Opus 分歧 B。
