# T001 Fixture 采集指南 · operator 自用

**用途**: 对着本清单上 arxiv.org 抓 abstract,替换 `tests/fixtures/human-labeled-20.json` 的 PLACEHOLDER 字段。
**预计耗时**: 3-6h(20 篇 paper · 平均 12-18 min/篇 · 含 LEG-2 rate limit ≥ 3s/req 的 sleep)。
**原则**:
- 每条 anchor 必须**早于** candidate 的 publishedAt(shift 定义要求)
- abstract 原文粘贴 · 不删 LaTeX · 不改字符
- `humanVerdict` 信你第一直觉;`rationale` 写 1-2 句"为什么这是 shift / incremental / unrelated"
- **采集前先做 pilot 5 篇**(f1 / f3 / f11 / f17 + 自选 1 篇)自检:有 ≥ 2 篇犹豫就暂停,回到 Claude 主会话讨论"shift 定义"再继续

---

## §1 · 10 条 shift 候选(f1-f10)

每条: candidate 是 shift 发起方 · anchor 是被颠覆的"前状态"paper。

### f1 · DPO 取代 RLHF
| 字段 | 值 |
|---|---|
| topic | id=1, name="RLHF / alignment", keywords=["RLHF","preference learning","reward model"] |
| candidate arxivId | `2305.18290` (Direct Preference Optimization, Rafailov 2023) |
| anchor arxivId | `2203.02155` (InstructGPT, Ouyang 2022) |
| anchor paperId | 1 (占位整数,T003 后换真 DB id) |
| rationale 草稿 | DPO 用闭式优化绕过 reward model + PPO 三步流程 · 颠覆 RLHF pipeline |

### f2 · Mamba 挑战 Transformer 长序列
| 字段 | 值 |
|---|---|
| topic | id=2, name="state-space-models", keywords=["SSM","Mamba","long-sequence","selective scan"] |
| candidate arxivId | `2312.00752` (Mamba, Gu & Dao 2023) |
| anchor arxivId | `1706.03762` (Attention Is All You Need, Vaswani 2017) |
| anchor paperId | 2 |
| rationale 草稿 | Mamba 在长序列以线性复杂度匹敌/超越 Transformer · 挑战 "attention is all you need" 统治 |

### f3 · CLIP → SigLIP(对比损失演化)
| 字段 | 值 |
|---|---|
| topic | id=3, name="vision-language pretraining", keywords=["CLIP","SigLIP","contrastive","sigmoid loss"] |
| candidate arxivId | `2303.15343` (SigLIP, Zhai 2023) |
| anchor arxivId | `2103.00020` (CLIP, Radford 2021) |
| anchor paperId | 3 |
| rationale 草稿 | SigLIP 用 sigmoid 替 softmax 对比损失 · 大幅省 batch-size 要求 · VLM 预训练范式改写 |

### f4 · Mixtral / MoE 取代 dense
| 字段 | 值 |
|---|---|
| topic | id=4, name="mixture-of-experts", keywords=["MoE","sparse","Mixtral","expert routing"] |
| candidate arxivId | `2401.04088` (Mixtral 8x7B, Jiang 2024) |
| anchor arxivId | `2302.13971` (LLaMA, Touvron 2023 · dense baseline) |
| anchor paperId | 4 |
| rationale 草稿 | Mixtral MoE 用 8x7B sparse 在 inference cost 持平 dense 7B 下超越 LLaMA 70B · 架构经济学改写 |

### f5 · LoRA / PEFT 取代 full finetune
| 字段 | 值 |
|---|---|
| topic | id=5, name="parameter-efficient-finetuning", keywords=["LoRA","PEFT","adapter"] |
| candidate arxivId | `2106.09685` (LoRA, Hu 2021) |
| anchor arxivId | `1810.04805` (BERT, Devlin 2018 · full finetune 范式) |
| anchor paperId | 5 |
| rationale 草稿 | LoRA 用 low-rank 分解把可训参数降 10000x · full finetune 不再是 de facto 做法 |

### f6 · AlphaFold 2 取代手工 homology modeling
| 字段 | 值 |
|---|---|
| topic | id=6, name="protein-structure-prediction", keywords=["AlphaFold","homology","protein folding"] |
| candidate arxivId | **PLACEHOLDER-alphafold2**(AlphaFold 2 是 Nature 2021 · arxiv 无正式 preprint · 你查 Nature DOI 10.1038/s41586-021-03819-2) |
| anchor arxivId | **PLACEHOLDER-homology-baseline**(可选 `1607.08220` Rosetta 或其它 pre-AF2 homology 系列) |
| anchor paperId | 6 |
| rationale 草稿 | AF2 在 CASP14 把蛋白质结构预测 GDT_TS 从 ~50 抬到 ~90 · 改写整个领域方法论 |
| **特别提示** | 这条可能需要你**替换 arxivId 为 DOI 或 PLACEHOLDER**;harness 不校验格式,但 abstract 必须真 |

### f7 · Diffusion Transformer(DiT) 取代 U-Net
| 字段 | 值 |
|---|---|
| topic | id=7, name="diffusion-architecture", keywords=["DiT","diffusion","U-Net","transformer"] |
| candidate arxivId | `2212.09748` (DiT, Peebles & Xie 2022) |
| anchor arxivId | `2006.11239` (DDPM, Ho 2020 · U-Net 范式) |
| anchor paperId | 7 |
| rationale 草稿 | DiT 证明 transformer 主干在 diffusion 上 scaling 更好 · 后续 SD3 / Sora 都弃 U-Net |

### f8 · FlashAttention 取代 vanilla attention
| 字段 | 值 |
|---|---|
| topic | id=8, name="attention-efficiency", keywords=["FlashAttention","IO-aware","memory-efficient"] |
| candidate arxivId | `2205.14135` (FlashAttention, Dao 2022) |
| anchor arxivId | `1706.03762` (Attention Is All You Need · 与 f2 复用) |
| anchor paperId | 8 |
| rationale 草稿 | FlashAttention 通过 IO-aware tiling 把 attention memory 从 O(N²) 降到 O(N) · 事实标准 |

### f9 · Constitutional AI 绕开 RLHF
| 字段 | 值 |
|---|---|
| topic | id=9, name="alignment-non-RLHF", keywords=["Constitutional AI","RLAIF","self-critique"] |
| candidate arxivId | `2212.08073` (Constitutional AI, Bai 2022) |
| anchor arxivId | `2203.02155` (InstructGPT · 与 f1 复用 anchor) |
| anchor paperId | 9 |
| rationale 草稿 | CAI 用 AI feedback 替 human feedback 做对齐 · RLHF 的人类标注依赖被 challenge |

### f10 · GPT-4 技术报告(多模态能力涌现)
| 字段 | 值 |
|---|---|
| topic | id=1, name="RLHF / alignment"(复用 topic 1) |
| candidate arxivId | `2303.08774` (GPT-4 Technical Report, OpenAI 2023) |
| anchor arxivId | **PLACEHOLDER-gpt35-baseline**(或用 `2005.14165` GPT-3 做 anchor) |
| anchor paperId | 10 |
| rationale 草稿 | GPT-4 多模态 + reasoning benchmark 大跳 · 闭源模型能力跃迁的锚点报告 |

---

## §2 · 6 条 incremental 候选(f11-f16)

每条选"同一 topic 下的 follow-up paper" · 只是 +1-2% benchmark 或小幅方法改进 · 不改 state。

**建议清单**(你可以自选):

| id | topic 建议 | candidate 候选 | anchor 复用 | rationale 草稿 |
|---|---|---|---|---|
| f11 | RLHF | IPO (`2310.12036`, Azar 2023) | f1 anchor InstructGPT | IPO 对 DPO 做理论重构 · 但未改 "offline preference" 范式 |
| f12 | SSM | Mamba-2 (`2405.21060`, Dao 2024) | f2 anchor Attention | Mamba-2 在 Mamba 基础上改 selective scan · 不改 SSM vs Transformer 的根本选择 |
| f13 | MoE | DeepSeekMoE (`2401.06066`, DeepSeek 2024) | f4 anchor LLaMA | DeepSeekMoE 调 expert 粒度 · 但 "sparse 替 dense" 命题已由 Mixtral 奠定 |
| f14 | PEFT | QLoRA (`2305.14314`, Dettmers 2023) | f5 anchor LoRA(复用) | QLoRA 用 4-bit quantize + LoRA · 只是进一步省内存 |
| f15 | Diffusion | SD3 / Stable Diffusion 3 (`2403.03206`) | f7 anchor DDPM | SD3 是 DiT 范式的工程化 · 命题已由 DiT 奠定 |
| f16 | Attention | FlashAttention-2 (`2307.08691`, Dao 2023) | f8 anchor Attention(复用) | FA-2 对 FA-1 做 parallelization 优化 · 范式未变 |

---

## §3 · 4 条 unrelated 候选(f17-f20)

候选 paper 与 anchor **keyword 重叠但 claim 无关** · 测 LLM 识别"表面相关/实质不相关"。

**建议清单**:

| id | 表面重叠 | candidate 候选 | anchor 复用 | rationale 草稿 |
|---|---|---|---|---|
| f17 | "attention" 关键词重叠 | graph attention network 领域某篇 · 如 `1710.10903` (GAT) | f2 / f8 anchor Attention | GAT 的 attention 机制与 Transformer attention 名同实异 · 领域完全不同 |
| f18 | "preference" 关键词 | recommender preference learning 某篇 · 如 `1205.2618` (BPR) | f1 anchor InstructGPT | BPR 的 preference 是推荐系统协同过滤 · 不是 RLHF 语境 |
| f19 | "diffusion" 关键词 | diffusion on graph 某篇 · 如 `1805.07045` (GCN diffusion) | f7 anchor DDPM | graph diffusion 是图卷积范畴 · 与 generative diffusion 无 claim 重叠 |
| f20 | "protein" 关键词 | protein-protein interaction 非折叠某篇 · 如 `1802.00543` (任一 PPI prediction) | f6 anchor AF2 | PPI 预测与结构预测目标完全不同 · 仅共享 "protein" 关键词 |

---

## §4 · 采集纪律(必读)

1. **arxiv 速率**: 两次 API 请求之间 sleep ≥ 3s(LEG-2 · arXiv ToS)
2. **abstract 原文**: 不改 · 不删 LaTeX · 不翻译
3. **publish time 倒序检查**: 对每条 shift,确认 candidate publishedAt > anchor publishedAt
4. **humanVerdict 独立判断**: 即使本清单草稿写 "shift",你读完 abstract 后如果**不信** → 标成 "incremental" 并在 rationale 解释你的 disagreement。**T001 测的就是"你 vs LLM"的对齐**,不是测 LLM vs 这份清单
5. **rationale 写不出来就改 humanVerdict**: 如果你对某条写不出 1 句具体理由(而不是空泛"这是 state shift") → 把它标成 incremental 或 unrelated,不要凑数

---

## §5 · 跑 pilot 5 篇 · 定义体检 SOP

**做完 §1-§3 清单阅读后**,**不要**直接采 20 篇。先按顺序采 5 条 pilot:

1. f1 (DPO · shift 典型) · 采 abstract + 标注 humanVerdict + 写 rationale
2. f3 (SigLIP · shift 典型) · 同上
3. f11 (IPO · incremental 典型) · 同上
4. f17 (GAT · unrelated 典型) · 同上
5. 自选 1 条你**最犹豫**的(可从 f6 AlphaFold / f10 GPT-4 挑)

**体检标准**: 5 条里有 **< 2 条**让你犹豫 → 继续采剩 15 条;有 **≥ 2 条**让你犹豫(例如 "这算 shift 吗"想了 > 3 min) → **STOP**,回 Claude 主会话报告:
- 哪几条让你犹豫
- 犹豫的根因(anchor 选得不对? "shift" 定义不清楚? 你对该领域知识不够?)

主会话讨论后再决定:收紧定义 / 换 anchor / 删条目 / 补训练数据。

---

## §6 · 采集流程

```
1. 打开本清单(本文件) + tests/fixtures/human-labeled-20.json
2. 对每条 f1-f20:
   a. 打开 arxiv.org/abs/<arxivId>(或 PLACEHOLDER 时自查)
   b. 复制 abstract(不改)
   c. 在 human-labeled-20.json 里找同名 id · 替换 candidate.abstract + anchor.abstract
   d. 确认 topic / humanVerdict / rationale 对齐(或改成你的判断)
   e. sleep 3s 再采下一条(别触发 arxiv rate limit)
3. 20 条全采完 → 保存 JSON
4. 跑 harness: pnpm tsx projects/001-pA/spikes/eval-harness.ts --provider glm --fixture human-labeled
5. 把 runs/glm-<ts>.json 路径发给 Claude 主会话 · 让它帮你写报告初稿
```

---

## §7 · 此清单 ≠ fixture 本身

- 本清单是**脚手架** · 帮你选题 · 节省"该选哪 10 篇"的决策时间
- 真正的 judgment(这条到底是 shift 还是 incremental)**由你**在替换 JSON 时决定
- 若你和清单草稿不同意 → 以你为准 · 把 rationale 改成你的理由
- T001 gate 的含义是 "LLM 是否能像 operator 一样判断" · 所以 operator 的标注才是 ground truth
