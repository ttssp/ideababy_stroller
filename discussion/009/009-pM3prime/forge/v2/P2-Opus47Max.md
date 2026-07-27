# P2 · Reviewer A(Claude Opus 4.8)· 009-pM3prime forge v2

**Phase**: 2(参照系评估 · Z = 对标 SOTA)
**Written**: 2026-07-27
**Searches run**: 6 次检索 + 1 次全文抓取,覆盖 6 个独立文献面
**零重叠自检**:v1 用的是 Nine Judges / Correlated Errors / AmbER / FActScore / SAFE / PoLL ——
**本轮 6 面与其零论文重叠**(K binding 要求引正交外证据破回声室)

---

## §1 SOTA 对标

| # | 外部证据 | 对本轮议题的判定 | 冲击对象 |
|---|---|---|---|
| 1 | **Krippendorff 信度三分类**:stability(稳定性)/ reproducibility(可复现性)/ accuracy(准确性)。**intra-annotator agreement 严格讲只测 stability,不测 validity(against a standard)** | **决定性**。07-25 拍板的 gold=operator 考据版 / human=operator 盲标版,**同一人两次标注 = intra-annotator agreement = 按定义只测 stability**。把它读作「验收了 machine 映射的正确性」是**测量理论上有名字的范畴错误**,不是「诚实边界」注记能补的 | 直接判定 007-25 gold 协议的性质;**升级**双方 P1 的 gold 论证 |
| 2 | **非专家 vs 专家标注**:非专家两两一致 **0.68** vs 专家 **0.83**;知识密集域(如法律文本)**专家往往不可替代**;非专家可用的**前提是多人聚合**(majority vote 过滤噪声)后才达到接近专家的质量 | **推翻我 P1 的乐观**。非专家标注在文献里成立的条件是**聚合多个非专家** —— 而 solo operator **结构上无法聚合**。「找个能力弱一点的主体 + 认真做」不是文献支持的路径 | **推翻我 P1 §1.6** 的一半 |
| 3 | **选择性预测 / abstention**:形式化为 **risk-coverage 权衡**;标准做法是报 **risk-coverage 曲线 + AURC**(曲线下面积),而非在固定 coverage 处判过否 | **确认我 P1 §1.4 并给出解**。「诚实弃权 × 固定覆盖率门槛」互斥是真的,但文献的处理方式是**报整条曲线**,不是设一个固定 coverage 阈值 —— 现 SLA 的 0.75/0.80/0.90 固定门槛是**方法学上过时的形态** | **确认并救回** P1 §1.4 |
| 4 | **弱监督性能评估 via Partial Identification**(NeurIPS 2024):把「无金标下的评估」形式化为**偏识别问题**,用 Fréchet 界给出 accuracy/precision/recall/F1 的**区间界**,**不需要任何标注数据** | **唯一真正「不需要人产真值」的候选**。但抓原文确认:输出是**界不是点估**,且未说明小样本适用性 —— **n=41 上界会宽到什么程度未知**。009 已有 `trial_ledger` 的 extractor_variant 基础设施可充当多弱标注器 | 部分回答 K 的问题 2;**需 P3 定性** |
| 5 | **distant supervision(金融 NLP)**:用外部源自动打标,**不需人参与**;但「若数据集与外部源存在差异,自动标签会有噪声」,金融文本上仍是开放问题 | 支持「外部权威源回标」方向存在,但**噪声本身需要验证** —— 会递归回到「谁验证噪声水平」。**不是免费午餐** | 削弱 K 候选方向一的即用性 |
| 6 | **Correctness is not Faithfulness in RAG Attributions**(arXiv 2412.18004)+ 归因/groundedness 度量族(Doc-F1 / Snippet-F1):**correctness(claim 是否为真)与 groundedness(引文是否真支撑该 claim)是两回事**;实测**高达 57% 的引文是事后合理化的** | **本轮最有价值的构造性发现**。它给出一条**横切五维**的新切法(见 §3.3) | **取代**我 P1 的「事实维 vs 解释维」切法 |

## §2 用户外部材料消化

K 未附外部链接或文件(全部关切已写在 K 正文)。无额外材料需消化。

按 K 的负面清单复核:本轮检索**未触碰** D-1/D-2/D-3、**未重开**第二 LLM 终审题、**未动** E1 结论。
检索全部集中在「真值从哪来 / 无金标怎么评 / 弃权怎么处理 / 非专家能不能标」四个 K 明确关心的面。

## §3 修正后的视角

### 3.1 我 P1 中**被推翻**的(K binding 要求显式报告)

**§1.6「Layer-1 能力要求更低,是最实的降级候选」—— 推翻其立论方式。**

我 P1 的推理是「Layer-1 问的是阅读理解,Layer-2 问的是领域判断,所以 Layer-1 能活」。
证据 2 显示这个推理**漏了文献里真正的成立条件**:非专家标注质量之所以能接近专家,
靠的是**多人聚合过滤噪声**(0.68 → 经 majority vote 后接近 0.83),不是靠任务简单。
**solo operator 结构上无法聚合** —— 这个补救手段对 009 不可用。

所以「换个更容易的层」这条路,**在 solo 约束下没有文献支持**。
我 P1 §2 里把 Layer-1 排在候选首位(`new P1`),这个排序**应当降级**。
Layer-1 也许仍值得做,但理由不能是「更容易所以 operator 能担」。

**「事实维 vs 解释维」的二分 —— 被更好的切法取代。** 见 3.3。

### 3.2 我 P1 中**站住并被升级**的

**§1.3「gold 未定义 = 结构性空洞」站住,且被证据 1 升级为有名字的诊断。**
我 P1 只能说「gold 与 human 同为一人,共享盲点」—— 这是描述。
Krippendorff 的三分类给了**定性**:那是 **stability 测量**,按定义**不承载 validity**。
即 07-25 协议下的 sector/horizon/direction 双错率,测的是 operator 自己前后一致不一致,
**在测量理论上根本不是对 machine 正确性的验收** —— 与 D-3 想补的「诚实边界」注记不是同一量级的问题:
不是「这个验收较弱」,是「**这个数字不是那个东西的验收**」。

**§1.4「诚实弃权 × 覆盖率互斥」站住(证据 3),且找到了处理方式。**
文献不在固定 coverage 处判过否,而是报 **risk-coverage 曲线 + AURC**。
这意味着 SLA 冻结的固定覆盖率门槛(0.75/0.80/0.90)不只是「数字定高了」,
而是**门槛形态本身与该问题的标准处理方式不符**。这条对 KG-43 也有直接含义(见 3.4)。

### 3.3 检索带来的、双方 P1 都没有的构造性方向

**把 Layer-2 从「correctness 验收」重定为「groundedness 验收」。**

证据 6 的核心区分:
- **correctness** = 「NVDA 这个 ticker 判得对不对、看多这个方向对不对」→ **需要领域判断**,operator 做不了;
- **groundedness / faithfulness** = 「**被引的那句原文,是否真的支撑这个五元组**」→ **阅读理解**,operator 做得了。

这条切法的性质与我 P1 的「事实维 vs 解释维」不同:后者是**按维度纵切**(保 ticker/timepoint,弃三个解释维),
前者是**横切五维**(五维都验,但只验「有没有原文依据」,不验「判断对不对」)。

**为什么它对 009 特别合适**:009 **已经有整套引文锚定基础设施** —— forge v6 的「引文回锚制」
(LLM 只产逐字 quote → `anchoring.py` 确定性回锚 exact→normalized→fuzzy)、
`extracted_signals` 的 `raw_ref` / `span_start` / `span_end`。groundedness 验收要的输入**已经在库里**。

**且它不是稻草人验收**:证据 6 实测「高达 57% 的引文是事后合理化的」——
即模型先给答案再找引文。groundedness 检查**能真抓到东西**,不是走过场。

**它的诚实边界必须同时写明**:groundedness 过 ≠ 信号有 alpha,甚至 ≠ 映射正确。
它验的是「提取器没有无中生有」,不验「提取器判得准」。
**但这恰好是 E1 要拆的联合假设里 operator 真正能担保的那一半** ——
而 E2 的证据地位本就是「开发证据」,不是 alpha 确证(E3 才是)。

### 3.4 对 KG-43 的修正

我 P1 说 KG-43 是「冻结前应有可达性证明」。证据 3 让我认为这**说小了**。
Codex P1 提的两道门(存在性证明 + 真值证明)比我准确。我现在再加第三条:

**门槛的形态本身要经过方法学检验** —— 009 冻结的是「固定 coverage 阈值 + 合取判过否」,
而该问题的标准形态是 risk-coverage 曲线。**冻结一个方法学上不合适的形态,比冻结一个错的数字更难救**:
数字可以改(受 C6 约束),形态错了整套预注册都要重来。

---

**字数**:约 1,050 字(不含表格)
**Hard constraints 自检**:✅ 已读对方 P1 · ✅ 按 Z 跑 ≥3 SOTA 检索(实跑 6 面)· ✅ 与 v1 零论文重叠 ·
✅ 显式报告 P1 被推翻项(§3.1)· ✅ 未写 PRD/实装方案(留 P3R2/Phase 4)

## Sources

- [How Reliable are Annotations via Crowdsourcing?](https://oro.open.ac.uk/25874/1/mir354s-nowak.pdf)
- [Know Your Limits: A Survey of Abstention in Large Language Models](https://arxiv.org/html/2407.18418v3)
- [Weak Supervision Performance Evaluation via Partial Identification (NeurIPS 2024)](https://arxiv.org/abs/2312.04601)
- [Correctness is not Faithfulness in RAG Attributions](https://arxiv.org/pdf/2412.18004)
- [Intrarater Reliability — overview](https://www.sciencedirect.com/topics/nursing-and-health-professions/intrarater-reliability)
- [Aligning Intraobserver Agreement by Transitivity](https://arxiv.org/pdf/2009.13905)
- [Counting on Consensus: Selecting the Right Inter-annotator Agreement Metric](https://arxiv.org/pdf/2603.06865)
- [Data-centric Artificial Intelligence: A Survey (distant supervision)](https://arxiv.org/pdf/2303.10158)
