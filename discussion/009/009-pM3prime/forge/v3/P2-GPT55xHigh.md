# Forge v3 · 009-pM3prime · P2 · GPT55xHigh · 参照系评估(with search)

**Timestamp**: 2026-08-13T05:51:53Z  
**Searches run**: 12, SOTA-benchmark  
**Visibility**: 我已读对方 P1；未读对方 P2。

## 1. SOTA 对标

| 标的 X' | 参照项 | 它怎么做 | 我们怎么做 | gap | URL/Source |
|---|---|---|---|---|---|
| fail-closed / retry | OpenAI Python SDK | 默认重试 2 次；仅连接错误、408/409/429、≥500，带退避 | client 未覆盖 `max_retries`；census 对首次空 content、坏 JSON、缺 `usage` 立即累计失败并整轮 invalid | 传输失败已有 SDK 重试；HTTP 200 的语义/契约失败没有 per-record 重试 | [官方 SDK · Retries](https://github.com/openai/openai-python#retries) |
| 模型身份/确定性 | DeepSeek Chat API | 当前请求 schema 列出 temperature/top_p 等但无 `seed`；返回 `system_fingerprint` | 温度 0；既不读 fingerprint，也无 seed 可传 | 官方仅称低温更 focused/deterministic；**没有可复现性保证**。fingerprint 只表示后端配置，不等于输出承诺 | [DeepSeek 官方 Chat API](https://api-docs.deepseek.com/api/create-chat-completion) |
| 重复性度量 | Atil et al. | 对 5 模型×8 任务跑 10 次；用 TARr@N（原输出）/TARa@N（解析答案）度量全一致 | 用两跑 Jaccard、总量差和分市场差诊断 | 论文证明“确定性设置”仍会变，但 TAR 是全一致率，未直接解决集合元素的部分重叠，也不给通用 pass 阈值 | [arXiv:2408.04667](https://arxiv.org/abs/2408.04667) |
| 集合型 IE 聚合 | Xie et al. zero-shot NER | 多次采样后先对 mention、再对 type 做两阶段多数票；七个中英 benchmark 改善，实验最多采 30 次 | 一次生成 `(source,ticker,direction)` 集合，直接进密度/market 判据 | 可借“元素→属性”两阶段统计形态；论文显示样本越多通常越好，但没给本任务最少 N 或稳定性门槛 | [EMNLP 2023 论文](https://aclanthology.org/2023.emnlp-main.493/) |
| 标注作为测量 | OLAF | 把 LLM annotation 定义成测量过程，要求同时报告 reliability、calibration、drift、consensus、aggregation、transparency | 有失败计数与 trial ledger，但单次 accepted 集仍被当事实 | P1 的“新增校准证据面”方向站住；OLAF 是框架性 position paper，不提供阈值 | [arXiv:2512.15979](https://arxiv.org/abs/2512.15979) |
| 边界/稀有项 | Mondal & Sancheti | 在 NER 输入扰动下测预测、置信与解释；稀有实体更脆，错误答案仍可高置信 | 目标恰含隐性、边界、长尾 ticker；多数票可能偏向显眼信号 | 聚合能增稳定，不自动保证构念效度；“会不会滤掉真边界信号”仍须本任务真标定 | [arXiv:2404.05088](https://arxiv.org/abs/2404.05088) |

## 2. 用户外部材料消化

**N/A**：K 未提供外部链接、文本或文件；本节只使用 §1 所列独立检索材料。

## 3. 修正后的视角

1. **任务 A／我的 P1 架构判断被收窄，A 侧修正 2 成立。** SLA 的“调用失败→重试/退避；连续失败 hard-fail”位于 E1 依赖 SLA，作用域覆盖 census。`census.py` 没有应用层 retry loop；SDK 虽默认重试传输类错误，却不会重试实测的空 content、坏 JSON、缺 `usage`。因此在宣告 record 失败前加有界语义重试可视为落实既有冻结契约，不必先改 SLA；但重试耗尽后仍须 hard-fail，且它不处理 Jaccard 0.44，故只化解议题②，不化解③。
2. **任务 B／我的 P1“模型身份缺失”站住。** DeepSeek 当前官方 Chat schema 查不到 `seed`，也没有 determinism/reproducibility 保证；`system_fingerprint` 的官方语义仅是运行模型的后端配置。可证伪点：若 DeepSeek 后续官方 schema 新增 seed 与重复性承诺，本结论须重审；当前不能靠未文档参数推演。
3. **任务 C／我撤回 P1 的病因推论，同意 A 侧。** invalid 回滚 E1 trial 行是事实，但 C1/O11 的 grain 本来就是 `variant×caliber×horizon`，不是 execution-attempt。失败运行不入这个分析 trial 账并非根病；真正缺口是同一 grain 下多次运行、不同 fingerprint/语料身份/输出集合无法区分。按“回滚”修会误碰 fail-closed，按“grain/测量身份”审才对。
4. **任务 D／我的 P1“测量对象应从点读数改判”站住，但指标问题只解了一半。** TARr/TARa、集合 Jaccard、元素入选频率与 mention→type 多数票都可描述信度；文献没有给适用于散文荐股抽取的成熟阈值或最少 N。NER 论文最多采 30 次，Atil 用 10 次，都不是普适下限。结论是：**N 与阈值须由本任务标定后预注册，不能移植数字。**
5. **我的 P1“多数聚合是否牺牲边界真信号”站住。** 稀有实体扰动研究表明长尾项更脆，故稳定交集可能只剩显眼信号；是否发生只能用本任务 recall/selection-frequency 联合证伪，不能用稳定性单指标解释掉。
6. **我的 P1“路线是否改判”仍未确定。** 搜索支持把不稳定纳入测量与聚合，但没有证明它在 009 上保留构念效度；P3 应把“聚合后信度”和“对边界真信号的效度”作为两个独立铰链，而非先拍一个 Jaccard τ。
