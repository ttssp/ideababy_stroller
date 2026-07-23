# Forge v1 · 009-pM3prime · P2 · GPT-5.6-Sol xhigh · 参照系评估(with search)

**Timestamp**: 2026-07-23T17:42:12+08:00
**Searches run**: 12, SOTA-benchmark
**Visibility**: 我已读对方 P1。

## 1. SOTA 对标

| 标的 X' | 参照项 | 它怎么做 | 我们怎么做 | gap | URL/Source |
|---|---|---|---|---|---|
| Layer-2 第二源 | Self-Preference Bias | GPT-4 显著偏好熟悉、低困惑度文本，不限是否自身生成 | 只排除 `human` 以外来源 | 来源标签既过严又未测熟悉性偏差 | https://arxiv.org/abs/2410.21819 |
| 单一异源判者 | PoLL | 六数据集上用不相交模型家族组成 panel，优于单一 GPT-4 且更贴近人判 | 一提取器加一个第二源、逐维一致即过 | 有“异源可用”先例，但先例是多判者而非一对一互认 | https://arxiv.org/abs/2404.18796 |
| “跨 vendor 即独立” | Correlated Errors | 评估 350+ LLM；两模型都错时一榜单仍有 60% 同错，强模型即使跨架构/provider 也高度相关 | 未测错误重叠，只测输出 agreement | **直接反证**：vendor/架构异源不是独立性证明 | https://arxiv.org/abs/2506.07962 |
| 事实型判定 | Extractive-QA judge | 有明确 gold answer 时，多家族 judge 与人相关最高 0.909，自偏很小；复杂答案类型仍较弱 | 五元组无现成 gold，且事实与解释维度混合 | 不能把抽取 QA 结果外推为整组可自治 | https://aclanthology.org/2026.gem-main.9/ |
| 自动事实验收 | FActScore / SAFE | 原子化后查可靠知识源；FActScore 自动估计误差低于 2%，SAFE 在分歧样本中 76% 胜 crowd | 第二源凭参数知识独立重标，无证据锚 | SOTA 的正交性来自外部证据，不只来自模型品牌 | https://aclanthology.org/2023.emnlp-main.741/ · https://arxiv.org/abs/2403.18802 |
| 冷门别名消歧 | AmbER | 多类检索器对同名冷门实体的误取概率约为热门实体两倍 | “老黄/达子/ASR 错词”正属长尾别名 | 异源模型仍可能共享流行度先验；需尾部专项金标 | https://aclanthology.org/2021.acl-long.345/ |

## 2. 对方 P1 关切消化

1. **错误相关性**：答案不是“真人或异源模型”二选一。PoLL 证明家族多样性可降偏差；350-model 研究同时证明跨 vendor 不足以建立独立性。第二源只能是候选，须在本任务盲测集上报告逐维双错率，而非由品牌预先授信。
2. **事实还是金融判断**：`ticker`/别名可由知识源核验，适合 FActScore/SAFE 式自动化；`direction/horizon/timepoint` 含语境解释，且 ASR、冷门称谓会把事实维度也变成歧义任务。因此“operator 不懂投资”并非全维阻断，但给小抄也不能自动成为终审。
3. **元层自证**：Claude×GPT 的收敛不构成独立性证据；相关错误研究说明跨谱系强模型仍可同错。本轮收敛最多生成待验假设，不能替代外部金标。
4. **keep vs refactor**：对方的“验收链骨架 keep”成立；我 P1 的架构 `refactor` 过宽。但“只改 guard”又过窄：资格层须记录证据来源、模型家族与 abstain，报告 agreement 之外的逐维错误重叠并保留分歧仲裁。结论是 **gate 骨架 keep，第二源契约与度量 refactor**。

## 3. 修正后的视角

- P1“D-7 应从 human 改写为错误正交性”→ **站住**：PoLL 与事实核验都把多样性/外证据作为有效机制。
- P1“异源强模型可充当独立第二源”→ **被推翻为有条件命题**：跨 provider 强模型仍有显著同错；不得按 vendor 自动放行。
- P1“架构应 refactor”→ **部分被推翻**：fail-closed gate 与双层链保留，只重构来源契约、校准指标和仲裁语义。
- 对方“任务主要是事实性指称消解”→ **部分站住**：ticker 可工具核验；但长尾流行度偏差及其余解释维度使纯 LLM 双标不足。
- 修正 verdict：异源 LLM 在 SOTA 有 panel/工具增强先例，却无“单一跨 vendor 模型可直接当独立 gold source”的依据。最小可接受方向是外证据锚定、尾部盲测校准、按维度双错率与人类只审歧义/分歧；否则维持 fail-closed。
