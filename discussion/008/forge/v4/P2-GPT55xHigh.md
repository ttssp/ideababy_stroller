# Forge v4 · 008 · P2 · GPT55xHigh · 参照系评估(with search)

**Timestamp**: 2026-06-30T18:05:19+08:00
**Searches run**: 7 search batches / 21 queries, SOTA-benchmark
**Visibility**: 我已读对方 P1。

## 1. SOTA 对标

| 标的维度 | 参照项 | 它的水平 | 008 处境 | gap | Source |
|---|---|---|---|---|---|
| 金融文本 sentiment/stance | FinBERT + Financial PhraseBank;2025 LLM 金融情绪评测 | FinBERT 论文强调金融语境有专门词汇、标注数据少;Financial PhraseBank 是 4845 条金融新闻句子、16 名金融/商业背景标注者。2025 评测发现 GPT-4o no-CoT 最贴近人类标签,而 CoT/推理不一定更好。 | 008 不是新闻句子,而是单作者投顾口语、反讽、黑话、免责声明和动作暗示;目标也不是泛 sentiment,而是 stance/conviction/action。 | 不能把干净金融情绪 benchmark 的表现迁移成跟单可信度;必须做本语料 spike。 | https://arxiv.org/abs/1908.10063 ; https://arxiv.org/abs/2506.04574 |
| 反讽/黑话/code-mixed | SemEval irony detection;code-mixed sarcasm papers | SemEval 顶队仍是专门 irony task;2026 code-mixed Hinglish sarcasm 研究里,微调 DistilBERT 最高约 84% accuracy,零/少样本 LLM 反而输给小模型;早期 Hinglish sarcasm 约 78% accuracy/F-score。 | trader韭的“这票真是好啊”、达子/卤馒头/谷子一类黑话,正是会反转 polarity 的场景。 | 通用 LLM 直接抽 stance/action 不够;黑话词典和人工金标样本是可靠性前置,不是锦上添花。 | https://arxiv.org/abs/1804.06659 ; https://arxiv.org/abs/2602.21933 ; https://arxiv.org/abs/2010.00310 |
| 文本信号 → copy trading | copy trading / social trading 实证 | copy trading 可带来“guided copying”收益,但研究也记录 copied trades 负收益时损失更高、复制会提高风险承担;平台层面还依赖真实交易记录和风控参数。 | 008 想从文本推顾问动作,没有顾问真实成交 ledger,还要先跨过 NLP 错标。 | “机器可信跟单”比平台 copy trading 更脆弱;应先定位成候选下游,不能直接作为 008 当前价值闭环。 | https://en.wikipedia.org/wiki/Copy_trading |
| LLM 结构化输出鲁棒性 | OpenAI Structured Outputs | 官方范式是 schema-constrained decoding / `strict:true`;OpenAI 在复杂 JSON schema eval 中报告 gpt-4o-2024-08-06 达 100%,老 JSON mode 不保证 schema。 | KG-25 仍是 `json.loads(content)` 裸跑,坏 JSON 无清洗、降级、告警。 | KG-25 的工程修复方向很明确;但 schema adherence 只保证形状,不保证 stance/action 语义正确。 | https://openai.com/index/introducing-structured-outputs-in-the-api/ |

## 2. 用户外部材料消化

K 中没有额外 URL 或外部文本需要 P2 新消化;X 的 hand-back、字典、PRD、KG-24/KG-25 已在 P1 读完。对方 P1 的新增价值是把“下游未定义”精确收窄为 **008↔004 接缝**:008 PRD 已定义采集和轻量包,但 004 侧如何消费、是否把文本结构化升级成机器信号,尚未写入产品边界。

## 3. 修正后的视角

- P1 判断“提取可靠性必须新增证据项” → **站住并加强**。§1 的金融情绪 SOTA 只覆盖更干净、更窄的 sentiment;反讽/code-mixed 结果显示专门任务也难到 78-84% 量级,不足以默认支持真金白银跟单。
- P1 判断“字典三层 keep” → **站住但顺序更明确**。§1 显示黑话/方言不是泛化风险,而是降低错误率的域适配资产;第 1 层词典、`entity_type`、`tech_side` 应继续保留,第 2 层 stance/action 等待 spike。
- P1 判断“工程纪律 refactor” → **站住**。§1 的 Structured Outputs 说明 KG-25 不是局部偶发,而是工业界已有成熟范式的缺位;但这只能修 JSON 形状,不能替代语义评测。
- P1 判断“产品用途 refactor” → **被收窄**。不是 008 完全没下游,而是 008 到 004 的消费契约未定义;copy trading 对标提示,应避免让 008 从“可溯源结构化”滑成“自动执行信号”。
- 对方 P1 的“机器可信跟单本质是 004 职责回流到 008” → **我接受为 P3 主分歧轴**。P2 证据支持:真实 copy trading依赖交易 ledger 和风险控制,而 008 目前只是文本推断,责任边界必须先钉住。
