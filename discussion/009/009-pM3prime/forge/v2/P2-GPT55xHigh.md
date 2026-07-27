# Forge v2 · 009-pM3prime · P2 · GPT-5.6-Sol xhigh · 参照系评估(with search)

**Timestamp**: 2026-07-27T08:53:36Z  
**Searches run**: 20 query strings / 6 batches, SOTA-benchmark.  
**Visibility**: 我已读对方 P1。

## 1. SOTA 对标

| 标的 X' | 参照项 | 它怎么做 | 009 怎么做 | gap | Source |
|---|---|---|---|---|---|
| 无 gold 评测 | Data Programming / Snorkel | 多个 noisy labeling functions,从重叠/冲突中估计噪声模型,产 probabilistic labels;目标是训练数据 | 只有 operator 一人两版标注,n≈41,且目标是验收 gate | 弱监督可做开发诊断,不能替代终审 gold;缺多个独立 source 与大样本 | https://papers.neurips.cc/paper_files/paper/2016/hash/6709e8d64a5f47269ed5cea9f625f7ab-Abstract.html |
| 非专家标注 | Snow et al. EMNLP 2008 + content-analysis reliability | 非专家可用通常靠多人聚合/校准;内容分析要求 independent coders 的 reliability | 单个非专家,不能 majority vote,也没有专家校准 | 文献没有支持“单个无领域非专家=gold”;只能测稳定性/可复现性 | https://aclanthology.org/D08-1027/ · https://link.springer.com/article/10.3758/s13428-016-0838-6 |
| 单噪声标签 | Dorner & Hardt ICML 2024 | 若目标是比较两个二分类器,预算应投向更多样本的单标签,不一定重复标同一样本 | 009 要逐条五维验收和 E2 放行,不是只比较两个二分类器 | 这是对我 P1 的局部反证:单标签不必总是无效;但 n=41 与绝对 gate 不满足适用形态 | https://proceedings.mlr.press/v235/dorner24a.html |
| abstention | Selective classification / risk-coverage | 标准做法是 risk-coverage 曲线或给定 risk 后最大化 coverage | 009 固定每维 min coverage,又要求“不会就 abstain” | A 侧 §1.4 部分成立:对低能力主体,诚实弃权会撞硬 coverage;门槛应先校准可达覆盖 | https://www.alphaxiv.org/abs/1705.08500 |
| groundedness vs correctness | FEVER / CFEVER | 标注 claim 是否被 evidence 支持/反驳,并记录证据句;CFEVER 五人一致性 κ=0.7934 | 009 已有 raw_ref/span 引文锚,但 Layer-2 问五维投资映射是否真 | 构造性出路:可把“引文是否支撑候选五元组”拆为 Layer-1/1.5;它不等于金融正确性 | https://aclanthology.org/N18-1074/ · https://ojs.aaai.org/index.php/AAAI/article/view/29825 |
| 事后市场回标 | StockNet / high-frequency news reaction | 用价格移动、收益、波动等 outcome 检验文本信号是否有预测力或市场反应 | 009 希望先验收“原文→五元组映射”再进回测 | outcome 可验证 alpha/方向结果,不能证明映射 gold 正确;它是 E2/E3 证据,不是 Layer-2 替代 | https://aclanthology.org/P18-1183/ · https://ucrisportal.univie.ac.at/en/publications/when-machines-read-the-news-using-automated-text-analytics-to-qua/ |

## 2. 对方 P1 消化

A 侧 §1.4 “诚实弃权 × 覆盖率门槛互斥”:我判 **部分成立**。选择性预测文献支持 risk-coverage 是一条曲线,不是拍脑袋固定 coverage。若主体在 sector/horizon/direction 上确实无能力,诚实 abstain 必然压低覆盖率;但这不是数学上所有主体都不可达,而是说明当前 coverage 门槛没有经过主体能力校准。

A 侧 §1.6 Layer-1 候选:外部证据增强它。FEVER/CFEVER 把“证据句是否支撑 claim”作为可标注对象,这更接近阅读理解与证据匹配,不等同于投资判断。009 的引文回锚基础设施让 Layer-1 或 Layer-1.5 成为比全量 Layer-2 更现实的幸存面。

A 侧 §3 三个不确定点:第一,“慢考据 gold 是否可产”仍未被文献救活;可靠性文献最多支持稳定/复现,不自动给 validity。第二,“无需真值范式”存在,但弱监督需要多个 noisy sources,partial/bounds 只给区间,不产 pass/fail gold。第三,“Layer-2 STOP 的代价”被我下调:FEVER 路径说明可保留 groundedness 资产,不是 E1 ROI 归零。

## 3. 修正后的视角

- P1 判断“弱监督...不能替代 Layer-2 终审真值” → **站住**。Data Programming 能无 hand-labeled data 估噪声,但依赖多个 LF/大样本,009 不满足。
- P1 判断“全量五维 v0.1 cut” → **站住但更精确**。不是因为所有评测都死,而是 sector/direction/horizon 三维缺 validity 锚;事实维与 groundedness 可拆出。
- P1 判断“v0.1 可诚实保留 ticker/timepoint” → **被削弱/扩展**。FEVER/CFEVER 说明除事实维外,还可验“引文支撑候选五元组”的 groundedness;这可能是比我 P1 更好的中间层。
- P1 未覆盖 A §1.4 → **新增修正**。固定 coverage 门槛与 abstain 是 risk-coverage 设计问题;对低能力 operator,它会重建 blocked。
- P1 对“单个非专家无路”的直觉 → **被 Dorner/Hardt 局部削弱**。若目标改成比较二分类器且扩大样本,单噪声标签可有理论路径;但它不支持 009 当前逐条五维 gold gate。

结论变化:主立场未被推翻,但从“只剩事实维或 STOP”修正为“全量 Layer-2 STOP;可另保留 groundedness/Layer-1.5 作为非金融真值验收面”。
