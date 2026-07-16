# Forge v5 · 009 · P2 · GPT-5.5 xHigh · 参照系评估(with search)

**Timestamp**: 2026-07-16T11:30:45Z
**Searches run**: 11 queries, SOTA-benchmark
**Visibility**: 我已读对方 P1；未读 `P2-Opus47Max.md`。

## 1. SOTA 对标

| 主题 | SOTA 发现 | 对 009 v5 的含义 |
|---|---|---|
| LLM 从新闻文本抽取交易信号 | Lopez-Lira/Tang 以新闻标题→LLM 判断→滞后一日收益检验，且把样本放在模型训练窗之后，并处理新闻可得时点；LLM 确有抽取文本信号的增量可能。Source: https://arxiv.org/abs/2304.07619 | 提取头提前站得住，但必须把 `published_at` 和交易可得性作为文本 PIT，不可只看内容相关性。009 的对象比标题更弱、更隐性，所以先验应比该论文更保守。 |
| 观点/解释可信度评分 | Karvetski 等用 55k+ forecast-rationale pairs 证明自然语言解释中的 EQM 可预测准确度，但更擅长识别低质量判断者；BTF-2 用冻结语料 pastcasting 来避免 hindsight bias。Sources: https://arxiv.org/abs/2606.30987, https://arxiv.org/abs/2604.26106 | “分析师可信度”不应只靠收益端；可先评估其解释质量/盲点/可校准性。不过 SOTA 提醒：解释质量更适合筛掉差判断，不能自动证明 alpha。 |
| 多重检验/回测污染 | Bailey/Lopez de Prado 的 PBO/DSR 明确把多次试验导致的 performance inflation 当作核心风险，DSR 校正 selection bias、multiple testing 与非正态收益。Sources: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2460551 | Opus 的“提取器变体 = trial”应升为硬红线；每个 prompt、规则、标签口径、horizon 都要进 trial ledger，否则 M2 的 DSR/PBO 会被上游自由度绕开。 |
| LLM 参数化前视偏差 | 2026 FinCAD 论文把 LLM 预训练记住历史走势命名为 parametric look-ahead bias，并给出推理期抑制记忆的缓解方向。Source: https://arxiv.org/abs/2605.24564 | 我 P1 对“美光/海力士记忆只能当 sanity check”的担心被加固。引用锚定和训练窗对照不是洁癖，而是回测有效性的前置条件。 |

## 2. 用户外部材料消化

无。

## 3. 修正后的视角

我的 P1 核心判断站住：009 v5 不是缺 008→004 搬运桥，而是缺能把隐性文本显性化的提取头；M1/M2 量尺资产应保留，但纪律必须上移到文本侧。SOTA 支持“文本可产信号”，也支持“收益回测必须防多重检验”，所以提取头提前不是路线膨胀，而是原评估机器取得输入的前置器官。

被修正的是风险排序：我原先把联合假设拆账列为第三不确定点；P2 后我会把它升到 P3 分歧候选第一。若没有独立标注样本/解释质量评分/拒绝行统计，回测失败无法区分分析师无 alpha、提取器差、样本少或 horizon 错。

与 Opus 的收敛点很强：我同意其“M1+M2 量尺资产”继续照用、同意“提取器变体 = trial”、同意“LLM 权重面 look-ahead”是方法论级威胁，也同意“提取质量独立验收”应进入红线。主要分歧/待裁不是方向，而是保守程度：Opus 倾向先谈物化路径；我认为 P3 应先裁最小证伪顺序，避免 schema 讨论掩盖“隐性信号密度是否足够”这个首要 ROI 风险。
