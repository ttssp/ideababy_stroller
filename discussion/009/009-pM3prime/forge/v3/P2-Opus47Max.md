# Forge v3 · 009-pM3prime · P2 · Opus 5 · 参照系评估(with search)

**Timestamp**: 2026-08-13T05:35:00Z
**Searches run**: 5 成功(SOTA-benchmark)+ **3 失败**(DeepSeek 官方 API 文档三次 `Socket is closed`,见 §3 未决项)
**Visibility**: 我已读对方 P1(`P1-GPT55xHigh.md`)。
**Note**: 本轮 `WebSearch` 工具在本 session 持续报 `400 output_config.effort 'xhigh' ...`,全部检索改走 `WebFetch`(arXiv API + 原站)。

## 1. SOTA 对标

| 参照项 | 它怎么做 / 它测到什么 | 我们怎么做 | gap | Source |
|---|---|---|---|---|
| **Defeating Nondeterminism in LLM Inference**(Thinking Machines, 2025) | 判定 T=0 非确定性的**主因不是** GPU 并发、也不单是浮点非结合律,而是 **kernel 缺 batch invariance** —— 服务端负载变 ⇒ batch size 变 ⇒ 归约顺序变。实测:1000 次 T=0 补全出 **80 个不同结果**,首次分叉在 **第 103 个 token**;换 batch-invariant kernel 后 **1000/1000 完全相同**,代价 **≈2×**(26s→55s,优化后 42s) | 温度 0,调第三方 API,**假定** T=0 ⇒ 确定性 | 🔴 **根本 gap**:该修复必须在**推理引擎 kernel 层**做。我们是 API 消费者,**这一层不在我们手里** ⇒ 「同文本同版本必同输出」对我们**在原理上不可满足**,不是我们没做到 | https://thinkingmachines.ai/blog/defeating-nondeterminism-in-llm-inference/ |
| **Non-Determinism of "Deterministic" LLM Settings**(arXiv 2408.04667) | 5 模型 × 8 任务 × 各跑 10 次:准确率波动最高 **15%**,最好-最差差距最高 **70%**;提出 **TARr@N**(原始输出全一致率)与 **TARa@N**(解析后答案全一致率)。并记录业界咨询意见:非确定性"perhaps essential to the efficient use of compute resources via co-mingled data in input buffers" | Jaccard 0.44,**N=2** | 形态对了:我们的 Jaccard 就是 TARa 的**集合值类比**。但 **N=2 太少**,且我们从没把它当**常规指标**跑。另:该文说明这**不会消失**,是服务架构的必然产物 | https://arxiv.org/abs/2408.04667 |
| **OLAF: Towards Robust LLM-Based Annotation Framework**(arXiv 2512.15979v2, 2025-12 / 2026-01) | 主张 LLM 标注**应被当作测量活动**,而非自动化函数;构念清单 = reliability / calibration / **drift** / consensus / aggregation / transparency;明确指出现有研究**普遍缺标准化的 reliability/calibration/drift 度量**,且常略去关键配置 | 把一次读数当事实 | 我 P1 §2 的诊断("全链条把一次读数当事实")**被一篇独立论文以同样措辞给出**。但它是**概念框架,不给阈值** ⇒ **不能指望文献替我们定 τ 和 N** | https://arxiv.org/abs/2512.15979 |
| **Empirical Study of Zero-Shot NER with ChatGPT**(2023) | **两阶段多数投票**:先投最一致的 **mention**,再投最一致的 **type** | 单次抽取直接落库 | 这是现成的**集合值聚合配方**,与我们 `(ticker, direction)` 结构同构(先投 ticker,再投 direction)。⚠ **摘要层未给 P/R 代价数字** —— 我 P1 §3-2 的疑问(交集会不会滤掉真信号)**文献在此深度未答** | arXiv IE/self-consistency 检索 |
| **Self-Consistency (CoT)**(arXiv 2203.11171) | 采样多条推理路径后**边缘化**取最一致答案;GSM8K **+17.9%** / SVAMP +11.0% / AQuA +12.2% | — | ⚠ **范畴差,不可直搬**:它聚合的是**单一答案**(众数良定义),我们要聚合的是**集合**。"边缘化"在集合上不是同一个操作 | https://arxiv.org/abs/2203.11171 |
| **Let Me Speak Freely?**(arXiv 2408.02442) | 格式约束伤推理密集任务 | §10.6 已实测三臂 | 已在 PREREG §10.6 消化并**实测部分证伪其直接搬用**(我们卡的是解析成活率,不是推理质量)。**本轮不重复** | 见 PREREG §10.6 |

## 2. 用户外部材料消化

K 中**没有**外部链接或粘贴材料 —— 本节 N/A。K 的全部内容是判准与五条议题本身,已在 P1 §0 摘要。

## 3. 修正后的视角

### 站住的

- **P1 §2 跨维度判断("五条议题 = 同一形态错误的五个投影")站住,并被外部独立支持**。OLAF(2025-12)以"annotation as **measurement**"给出同一诊断,构念清单里 drift / reliability / aggregation 正好覆盖我们的 ①③。这不再是我自造的框架。
- **C4 恒真测试站住,且比 P1 说的更硬**。对方 P1 **零重叠路径独立发现同一条**(他自己 `rg` 了那个测试)。而我 P2 读 `SLA.md` E1 段查到更紧的一层:**该 Hard 100% 要求的"判据"栏直接写的就是那个测试名** —— `提取确定性 | 同文本同版本 100% 同输出(温度 0) | test_same_text_same_version_same_output(O10 · C4)`。⇒ **一条 Hard 100% SLA 的验收判据,是一个构造上恒真的测试。**

### 被推翻 / 必须修正的(两条,都是我自己的)

**🔴 修正 1 · 我 P1 把工程纪律的处方定小了。**
我写的是"cut 那条测试 + new 校准面"。但 Thinking Machines 的结果表明:**「同文本同版本必同输出」对第三方 API 消费者在原理上不可满足** —— 修复位点在 kernel 的 batch invariance,我们够不着。⇒ 问题**不是**"我们没测",而是 **这条 Hard 契约(spec C4 / SLA E1 / PRD §7 红线 3)本身写错了形态**。
承 v2 判据:把"必须同输出"换成"**在声明边界内测得的稳定性**"是**改形态**(可),不是**挪数字**(禁)。改测试不够。

**🔴 修正 2 · 我 P1 默认议题 ② 必须"放松已冻结契约"—— 这个前提是错的。**
`SLA.md` §依赖 SLA 原文:「LLM API 可用性不在本 fork 控制:**调用失败 → 重试/退避 · 连续失败 hard-fail 留错**。」
而实现是:单条失败 `stats +1` → 立即 `break`(census.py:611-624 · codex R10 早停)→ 全回滚。per-record 重试为 **0**(OpenAI SDK 的默认传输层重试只覆盖连接错/429/5xx,**不覆盖**空 content、坏 JSON、`usage` 缺失 —— 而这三类正是我们两次实跑的失败类型)。
⇒ **实现比 SLA 严,而严的方向恰好制造了"不可跑"。**「**连续**失败 hard-fail」这个措辞本身就预设了「单次失败不 hard-fail」。
**这直接化解 K 的核心 tradeoff**:② 的正解可能是**让实现回到既有 SLA**,不需要动任何冻结项,也不触碰 KG-40(重试后仍失败 ⇒ 照旧 census_invalid)。

### 对对方 P1 的一处不同意

对方 §1 工程纪律段说「invalid 又回滚 E1 trial 行,因此失败尝试不进入该账」。**回滚是事实,但推论我不同意**:ledger 的 grain 是 `variant × caliber × horizon`(spec C1/O11),同一 variant 重跑本就不新增行,故在该 grain 下"漏记"不成立。
**真正该被指出的是 grain 本身**:同一个 `variant × caliber × horizon` 名下,7-18 / 8-12 跑1 / 8-12 跑2 产出了**三份不同语料**,而 ledger 无法区分它们 ⇒ DSR/PBO 分母的语义确实是虚的,**但根因是 grain 太粗(且身份不含模型),不是回滚**。这个区别有实际后果:按"回滚"去修会改 fail-closed,按"grain"去修只加记账维度。

### 新的未决项(**可查事实,非推演 —— 不得靠猜**)

**DeepSeek API 是否提供 `seed` 参数或任何可复现性保证?** 我三次 `WebFetch` 官方文档均 `Socket is closed`,**没查到**。
这条**直接决定 ③ 的处方**:若有 seed 且真起作用,轮内非确定性可能大幅收窄;若无,则只剩"多次采样 + 聚合"一条路。
**这是一条 5 分钟可验证的事实**(读文档 / 传一个 `seed` 参数看是否被拒),**不得在 P3 靠推演补上**。
