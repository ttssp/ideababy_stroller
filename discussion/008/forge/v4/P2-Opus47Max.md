# Forge v4 · 008 · P2 · Opus47Max · 参照系评估(with search)

**Timestamp**: 2026-06-30T10:10:00Z
**Searches run**: 4(对标 SOTA · 架构/提取层 · 零法律/ToS/DMCA 检索,遵 Z binding)
**Visibility**: 我已读对方 P1(P1-GPT55xHigh.md)。

## 1. SOTA 对标

| 标的维度 | 参照项(SOTA) | 它的水平 | 008 的处境 | gap / 含义 | Source |
|---|---|---|---|---|---|
| 金融文本 sentiment/stance 提取 | FinBERT / instruct-tuned LLM,在 SEntFiN/FOMC 等**干净**金融语料 | 准确率 88–97% · Macro-F1 0.88–0.96 | trader韭语料满嘴反讽+黑话,非干净新闻体 | 90% 是**clean-text 上界**,不是本语料能指望的;且这还只是最易的 sentiment 轴 | [1][4] |
| 反讽/讽刺识别(本语料的定义性难点) | GPT-4o 标注 sarcasm / 多 agent CAF-I 测 irony | sarcasm Macro-F1 **~67%** · irony SOTA **~76%** · 跨域 61–94% 剧烈波动 | trader韭核心文体就是反讽(「这票真是好啊」=看空) | **这是真天花板**:本语料 stance 判断会从 90% 向 **67–76% irony 带**塌陷 = 红队「中等易错」的**数字落地** | [2] |
| 从文本提信号→跟单 | 信号/copy-trading 实证研究 | 信号失败率 **~70%**(滑点等)· **62% 用户 3 个月内弃用** | operator 想要「机器可信跟单」 | 即便提取 100% 准,**信号→盈利**这步本身经验上高失败率 = 跟单是高 bar 产品,提取准只是必要非充分 | [3] |
| LLM 结构化输出鲁棒性(KG-25) | 生产级 JSON 提取范式 | prompt-only JSON 失败 **5–20%**;**重试解决多数偶发,但解不了确定性坏**;constrained decoding/JSON schema **100%** | KG-25 = DeepSeek 对特定正文确定性坏 JSON,连试 3 次同位置失败 | 确认我 P1 判断:**重试单独不够**;根治 = 控制字符清洗 + 鲁棒提取 + 降级,或上 constrained decoding | [5] |

paraphrase findings,verbatim quote 无(均转述)。

## 2. 用户外部材料消化

K 中无额外外部链接/文件;X 的 4 个标的(hand-back / 字典草稿 / PRD / KG)已在 P1 全部一手消化。本轮无新外部材料需处理。

补一条对方 P1 带出、我 P1 同样独立标到的事实交叉确认:GPT P1 §1A 与我 §1A **独立得出同一结论**——「现 PRD 正式价值闭环仍是采集+喂 004,operator 新倾向的机器可信信号尚未成为定义内的下游」。两个 parallel-blind 审阅人撞到同一缝,该缝是真的。

## 3. 修正后的视角

- 我 P1 判断 B「『中等易错』无分母,跟单 go/no-go 不能在没实测前拍」→ **强化站住**。SOTA 给了分母的**上下界**:clean-text sentiment 90%,但反讽轴 SOTA 仅 67–76% 且跨域剧烈波动 [2]。本语料是反讽密集 → 真实 stance/conviction 准确率**极可能落在 67–76% 甚至更低**,远不到跟单可信。spike 从「该不该做」升级为「**几乎必做**,且要测的是反讽剥离后的真实带宽,不是泛泛准确率」。

- 我 P1 判断 A「机器可信跟单本质是 004 职责回流到 008」→ **站住 + 被 SOTA 加重**。[3] 显示信号→盈利本身 ~70% 失败、62% 弃用,独立于提取质量。**含义**:即便 008 把信号提准,「跟单可信」仍是 004 层的产品赌注,不该由 008 采集层背。这进一步支持「008 只产可溯源结构化(C9 内),信号决策留 004」的边界。

- 我 P1 判断 C「字典第 1 层无悔可先落、第 2/3 层按用途取舍」→ **站住**,与 GPT P1 §2(字典 keep)独立一致。SOTA 不改这条;红队把 stance/conviction 踢出无悔层的边界收敛,被 [2] 的反讽数字**事后证明正确**(进无悔层=系统性污染)。

- 我 P1 判断 D「KG-25 重试不够,要清洗+降级+上报」→ **被 SOTA 精确证实**。[5]:重试解偶发、解不了确定性坏(KG-25 正是确定性坏)。最稳是 constrained decoding/JSON schema(100%),但 DeepSeek 是否支持需 L4 验;退而求其次 = 控制字符清洗 + 鲁棒 span 提取 + 降级标 degraded + 失败可见。KG-24 不涉 SOTA(纯状态契约 bug),P1 判断不变。

- **新浮现、P1 未充分展开的一点**:spike 的设计不能只报「总准确率 X%」。[2] 的关键教训是反讽是误差主源 → spike 必须**分层报**:① 剥离免责后 ② 在反讽 vs 非反讽子集上分别测 stance/conviction/action ③ 给出**错标率上界 + 反讽子集的召回/精确**,operator 才能据「假信号代价 > 漏信号」定**置信度门槛**(只保留 high-confidence)。这条进 P3 收敛,落到 next-dev-plan 的 spike 规格。

---
Sources:
[1] FinBERT / financial sentiment benchmarks — https://onlinelibrary.wiley.com/doi/10.1111/1911-3846.12832 · https://arxiv.org/html/2306.12659
[2] Sarcasm/irony detection SOTA — https://arxiv.org/abs/2506.08430 · https://arxiv.org/pdf/2506.00955 · https://www.researchgate.net/publication/395224302_SarcasmBench_Towards_Evaluating_Large_Language_Models_on_Sarcasm_Understanding
[3] Copy-trading signal performance — https://www.goatfundedtrader.com/blog/is-copy-trading-profitable · https://arxiv.org/pdf/2301.00170
[4] Target-based financial sentiment — https://aclanthology.org/2025.clicit-1.74.pdf
[5] LLM structured-output reliability — https://tianpan.co/blog/2025-10-29-structured-outputs-llm-production · https://arxiv.org/pdf/2601.06151
