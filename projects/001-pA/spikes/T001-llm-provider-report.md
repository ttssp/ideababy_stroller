# T001 LLM Provider Spike 报告

**评测日期**: 2026-04-24
**Provider**: GLM5.1 via 火山引擎 ARK (Anthropic-compatible endpoint)
**Model ID**: glm-5.1
**Fixture**: `tests/fixtures/human-labeled-20.json` (20 条 · 分布 10 shift / 6 incremental / 4 unrelated)
**Run 文件**: `projects/001-pA/spikes/runs/glm-2026-04-24T14-12-29-901Z.json`
**Harness**: `projects/001-pA/spikes/eval-harness.ts`
**权威 task 契约**: `specs/001-pA/tasks/T001.md`
**Prompt 来源**: `specs/001-pA/reference/llm-adapter-skeleton.md` §3 / §3.5 / §6 (字面拷贝 · 任何修改必须同步 bump prompt_version)

---

## 1. 指标摘要

| 指标 | 数值 | 阈值 / 备注 | 结果 |
|---|---|---|---|
| `summary_accuracy_n3_or_less` (≤3 句合规率) | 20 / 20 | 应 100% (truncateTo3Sentences 兜底) | ✅ |
| `judge_accuracy` | 14 / 20 (70.0%) | gate ≥ 14/20 = 70% (tech-stack.md §2.5) | ✅ 擦边 |
| `avg_input_tokens` | 774 | — | — |
| `avg_output_tokens` | 1914 | — | — |
| `p95_latency_ms_summarize` | 46289 ms | gate ≤ 5000 ms | ❌ 超 9.3× |
| `p95_latency_ms_judge` | 65160 ms | — (无 gate · 但已是 summarize 同量级) | ⚠️ |
| `monthly_cost_extrapolation_usd` (按 9k calls/月) | $275.78 | gate ≤ $50/月 (C11 envelope · 9k 假设下) | ❌ 超 5.5× |
| `monthly_cost_extrapolation_usd` (按 60k calls/月 · operator 真实预算) | **$1838.5** | gate ≤ $50/月 → 折算 ≤ $333/月 (60k 等比放大) | ❌ 超 5.5× |

> **两套外推假设并列说明**:
> - **9k calls 假设**: harness 默认值 · 15 topics × 20 candidate/day × 30 day = 9000 · aggregate.monthly_cost_extrapolation_usd 直接出 $275.78
> - **60k calls 假设**: operator 实际给的预算量级 · $275.78 × (60000/9000) = **$1838.5**
> - Pricing 占位: input $2.5/M · output $15/M (按 GPT-5.4 价位 · 火山 ARK GLM5.1 真实账单未到位)
> - **真实账单到位后才能定论**: 火山 ARK GLM5.1 实际单价大概率低 5–10× (国内云推理普遍便宜) · 若实际单价是 placeholder 的 1/6,$1838.5 → ~$306/月,仍**略超** $50 gate · 若实际单价是 1/40,$1838.5 → ~$46/月,**翻 ✅**
>
> **Gate 复盘**: 三 gate 中只有 judge_accuracy 14/20 擦边过,延迟和成本两条都明显超线。
> - judge_accuracy 落在 §5 模糊带 [13/20, 15/20] = 65%–75% 区间内 → 按 spec §5 触发 Codex second-opinion 复核
> - 延迟和成本超线主因: avg_output_tokens=1914 显著偏高(prompt 限定 ≤3 句却拿到平均 ~1.4k token verdict rationale),且单次 summarize p95 接近 50s 表明 GLM5.1 在长 abstract 上 thinking 时间偏长
> - 成本 gate 的最终判定依赖火山真实账单 · 延迟 gate 不依赖单价

---

## 2. Confidence 分布 (verdict.confidence)

按 **verdict.label** (模型实际打的标签) 分桶 · 20/20 records 都有 verdict (无 LLMProviderError)。

| label | count | mean confidence | min | max |
|---|---|---|---|---|
| shift | 13 | 0.892 | 0.80 | 0.95 |
| incremental | 4 | 0.863 | 0.80 | 0.90 |
| unrelated | 3 | 0.950 | 0.90 | 1.00 |

> 命令: `jq '.records[] | select(.verdict != null) | {l: .verdict.label, c: .verdict.confidence}' runs/glm-*.json`

**观察**:
- 模型整体自信度偏高 (所有桶 mean ≥ 0.86 · min ≥ 0.80) · 没有 ≤ 0.5 的"低自信"verdict
- shift 桶被严重偏倚: 模型在 13 条 verdict='shift' 中只有 9 条与人类标签一致 (f1–f5, f7–f10)。f11/f12/f14/f15 (人类=incremental) 都被误判为 shift, 且模型在这些误判上 confidence ≥ 0.85 — **高自信误判**, 校准差
- incremental 桶偏低自信 + 偏低召回: 6 条人类 incremental 中只有 f13/f16 被识出 (2/6 召回); 模型倾向把 incremental 升级为 shift
- unrelated 桶最稳: 4 条人类 unrelated 中 3 条 (f18/f19/f20) 一致 · 唯一漏判 f17 (Graph Attention Networks) 被打成 incremental confidence=0.8
- **结论**: confidence 数值不能直接用作下游优先级排序权重 — 高自信不等于高准确

---

## 3. Adversarial 稳健性 (单独跑 `--fixture adversarial`)

| 期望项 | 实测 | 结果 |
|---|---|---|
| 15 条 adversarial 中,被注入 verdict='shift' 的条数 | 未跑 | — |
| summary 句数 > 3 的条数 | 未跑 | — |
| rationale 含 "JAILBREAK"/"COMPROMISED"/"MALICIOUS" 字样的条数 | 未跑 | — |
| Category D (PII) 抛 LLMProviderError 的条数 | 未跑 | — |

> **本 run (`glm-2026-04-24T14-12-29-901Z.json`) 仅跑 human-labeled fixture (`_meta.fixture="human-labeled"`),adversarial 矩阵未执行。**
> Adversarial 跑批是 T001 spike 的独立子步,需另行 `pnpm spike:eval --fixture adversarial` 触发,产物落到 `runs/glm-adversarial-*.json` 后再回填本表。
>
> 旁证: human-labeled 20 条全部 `error: null`,无 `LLMProviderError` · 无 `truncated=true` 句数 > 3 (truncateTo3Sentences 兜底正常 · f4/f6 出现 `truncated=true` 是被截到 3 句以内,不是溢出 — `summary.rationale_sentences.length=3` 都成立)
> 真正的 adversarial 断言矩阵在 T004 `tests/unit/llm-adapter.test.ts`,本 spike 数据不替代单测

---

## 4. 风格偏好 (operator 主观评 · 抽样 5 条 verdict='shift' summary)

> **草稿说明**: 以下打分 / 评语由 Claude 起草 · operator 通读 5 条 summary 后**改成自己的判断**再签字。
> 抽样池(覆盖正确判 + 误判,便于评估"风格 vs 准确"两个维度):
> - **f1 (DPO)** verdict shift ✓ — 标准案例
> - **f3 (SigLIP)** verdict shift ✓ — 中英混合 abstract
> - **f4 (Mixtral)** verdict shift ✓ · summary `truncated=true` — 看截断后是否突兀
> - **f6 (ParaFold)** verdict incremental ✗ (人类=shift) — 漏判 shift,看 summary 本身写得清不清楚
> - **f11 (PsiPO)** verdict shift ✗ (人类=incremental) — 误升,看 rationale 是否过度联想

**评分 / 评语**(以下为 Claude 草稿建议 · operator 改写):

- **summary 可读性**: 4 / 5 ⭐
  - 句式工整 · 三句结构清晰 (What / How vs prior / Lab actionable) · 术语保留英文不强译
  - 扣 1 分:f4 截断在小数点中间 ("Llama 2 70B and GPT-3." / "5 across all evaluated benchmarks") · f6 截断在数字中间 ("13." / "8X average speedup") — 句号边界检测对小数点不友好,读起来割裂

- **rationale 思路接近 operator 自己判断吗**: 部分接近,但**偏激进**
  - shift 桶里 9 条命中的 rationale (f1/f2/f5/f7/f8/f9 等) 思路紧扣"anchor 假设 vs candidate 颠覆",和我自己判断接近
  - **f11/f14 这类被误升为 shift 的 rationale 显得"用力过猛"** — 把 incremental 性质的"对前作的改进 / 推广"硬包装成"颠覆 anchor 假设",过度联想
  - 模型整体偏好 shift 标签 → 在边界样本上倾向往 shift 推

- **中英文混合 abstract 处理**: 良好
  - f3 (SigLIP) abstract 含 "1M batch size"、"32k" 等数字 + 英文术语,模型 summary 全英文输出 · 数字精度保留 · 没有出现中英夹杂导致的语法乱串
  - human-labeled-20 fixture 整体以英文 abstract 为主 · 真正的中文 abstract 处理能力本 spike **未充分覆盖** · v0.2 应在 fixture 里加几条中文 paper 复测

- **截断频率 (truncated=true 的占比)**: **2 / 20** = 10%
  - 触发样本: f4 (Mixtral) · f6 (ParaFold)
  - 两条都是因 LLM 输出 4 句被 `truncateTo3Sentences` 砍到 3 句
  - 兜底正常工作 · 但截断点是按句号切的 · 小数点会被误判为句末 → **建议 T004 实现时在 truncate 前先做 "数字小数点 protect" 预处理**(把 `13.8X` 临时换成占位符再切句)

---

## 5. 决策

按 `tech-stack.md §2.5` 三条 gate (准确率 ≥ 70% · 成本 ≤ $50 · p95 ≤ 5s):

- 若 `judge_accuracy ≥ 14/20` 且其他两 gate 都过 → **approved-provider: glm-5.1**
- 若 `judge_accuracy < 14/20` → **fallback-to-heuristic + LLM 仅 summarize** (按 spec.md `OP-Q1` flag · risks.md `TECH-1` 路径)
- 若 `judge_accuracy ∈ [13/20, 15/20]` 模糊带 (即 65%–75%) → 触发 Codex second-opinion review,operator 等 review 结论再签字

---

### 本 run 决策状态: **v0.1 已 freeze · spike 整体 DEFERRED 到 Phase 2 (见 §7)**

> **原计划**: Codex second-opinion 待回 · 等 review 结论再签字。
> **实际决策 (operator 2026-04-24)**: 延迟 ❌ + 成本 ❌ 两条硬 gate 不是 prompt 工程能救的 · 整个 T001 spike 推迟到 Phase 2 在真实端到端数据上重跑 · 不再触发 Codex review · 详见 §7。

| Gate | 实测 | 阈值 | 结果 |
|---|---|---|---|
| judge_accuracy | 14/20 = 70.0% | ≥ 70% | ✅ 擦边过 · **落在 [13/20, 15/20] 模糊带** |
| p95_latency_ms_summarize | 46289 ms | ≤ 5000 ms | ❌ 超 9.3× |
| monthly_cost (60k calls · placeholder pricing) | $1838.5 | ≤ $50 | ❌ 超 36.8× (但单价依赖火山真实账单) |

**触发条件**: judge_accuracy 14/20 命中模糊带 → 按 §5 第三条规则,**触发 Codex second-opinion review**。

**Codex review 待回答的问题** (见 `.codex-inbox/T001-codex-review-request.md`):
1. judge_accuracy 14/20 中的 14 条命中是否"真命中"?是否存在"理由错但标签对"(蒙对)的情况?
2. 4 条 incremental → shift 的高自信误判 (f11/f12/f14/f15) 是 prompt 设计问题还是 GLM5.1 模型本身的判别偏差?换 prompt 能改善吗?
3. 给定延迟 ❌ + 成本(待真实账单)结构性超线 + judge_accuracy 擦边的全图,GLM5.1 是否值得继续投入(改 prompt / 换模型 size / fallback) · 给一个明确建议: **proceed / refine-prompt-then-rerun / fallback**

~~**operator 待办** (按 Codex 回执决定):~~
~~- 若 Codex 判 **proceed** → 下面签 `approved-provider: glm-5.1` · 同时把延迟和成本两条 gate 风险登记到 `risks.md TECH-1`~~
~~- 若 Codex 判 **refine-prompt-then-rerun** → 不签 · bump prompt_version · 重跑 spike · 出 `T001-llm-provider-report-v2.md`~~
~~- 若 Codex 判 **fallback** → 签 `approved-provider: FALLBACK_TO_HEURISTIC` · 关闭 LLM judge 路径 · 仅保留 LLM summarize~~

**实际待办**（0.4.0 后,见 §7）：本报告作为 v0.1 首轮记录冻结 · 不签 approved-provider · Phase 2 T001-v2 跑完后产出 `T001-llm-provider-report-v2.md` 由 operator 在 v2 报告里签字。

---

## 6. 已知限制 / 后续

- Pricing 是 placeholder · 火山真实账单到位前数字仅供量级判断 · operator 已确认月调用上限为 60k · 真实单价是决定成本 gate 通过与否的关键变量
- v0.1 仅评测一家 (glm) · v0.2 准备加 Anthropic Claude / OpenAI GPT 双家做 cross-validate
- adversarial fixture 跑出的 record 不进 gate · 仅入 §3 表参考 · 真正 adversarial 矩阵在 T004 单测
- **本报告非最终版**: judge_accuracy 14/20 触发模糊带 → 已投递 `.codex-inbox/T001-codex-review-request.md` · Codex 回执到位后才能签 approved-provider · 若 Codex 判 refine-then-rerun 则本报告标记为 v0.1 草稿,产物为 v0.2
- §4 风格段为 Claude 起草 · operator 通读后改写为自己的判断再签字
- truncate 函数对小数点不敏感 (f4/f6 在 "13.8X" 这类位置切错) · T004 实现需在切句前 protect 小数点

---

## 7. v0.1 Freeze 段（0.4.0 · 2026-04-24）

**本报告作为 v0.1 首轮 spike 记录冻结。** 整个 T001 spike 已 defer 到 Phase 2,作为 validation milestone 而非 Phase 0 强制 gate。

**Defer 决策的第一性论证**（详见 `specs/001-pA/DECISIONS-LOG.md` G11）：
1. **判 LLM 准确率需要真实端到端语境** — 单看 fixture 20 条 abstract 的判准,模型对它"过度自信"是必然。要看模型在真实 arxiv crawl + topic anchor 链路下的实际表现,等 T010/T011/T012/T013 跑通有真数据之后再评最准。
2. **延迟 ❌ + 成本 ❌ 这俩硬 gate 现在调不动** — 延迟 46s 是 GLM5.1 长 thinking 的架构特性,prompt 工程救不了;成本 gate 依赖火山真实账单到位才能终判。继续 prompt 工程救不了真正卡住的两条 gate。
3. **Phase 1 全程默认 fallback heuristic 的代价小** — 系统设计本来就允许这条降级路径(risks.md TECH-1 mitigation 已写得很清楚)· spec 改 13 个文件 / ~130 行 edit / ~70 min 工时即可完成下游同步。

**Phase 2 T001-v2 改进点**：
- fixture 不再是 20 条人工标注的 abstract,而是从 `papers` 表里抽样过去 30 天系统真实抓取的 candidate paper(按 topic anchor 自然成对)· 反映真实链路
- 退出条件加上**生产 SLA latency**(异步 worker 单 paper 处理 ≤ 60s · 不阻塞 user 交互),与 spike 上限 5s 区分
- 真实账单单价到位(火山 ARK GLM5.1 实际 input/output $/M)· 替换 GPT-5.4 placeholder 价位重算月度成本
- Phase 2 候选池开放:除 GLM5.1 外,也可重测 Anthropic Claude Sonnet 4.6 / OpenAI GPT-5.4(详见 `tech-stack.md` §2 0.2.0)
- 报告产物:`T001-llm-provider-report-v2.md`(本 v0.1 报告作为参考保留)

**Codex second-opinion 命运**：已起草的 inbox 文件 `.codex-inbox/20260424T150000-001-pA-T001-spike-second-opinion-DEFERRED.md` 加 `-DEFERRED` 后缀保留 · Phase 2 T001-v2 跑完后参考 · 不在 Phase 0 阶段触发。

**spec 联动**：
- `specs/001-pA/spec.md` 0.3.1 → **0.4.0**(§5 Phase 0 / Phase 2 / §6 T001 验收 / §6 OP-Q1 全部修订)
- `specs/001-pA/tasks/T001.md` phase 0→2 · depends_on []→[T010,T011,T012,T013]
- `specs/001-pA/tasks/T004.md` 加 stub 实现范围段(Phase 0/1 默认 `LLM_*_ENABLED=false`)
- `specs/001-pA/tasks/T010.md` / T012.md depends_on / 默认 flag 同步
- `specs/001-pA/risks.md` TECH-1 0.3.1 → 0.4.0(mitigation 改写 + v0.1 status 行)
- `specs/001-pA/tech-stack.md` §2 / §2.5(标题改 T001-v2 + Phase 2 决策树)
- `specs/001-pA/PHASE-0-KICKOFF-CHECKLIST.md` §1/§2/§3/§4/§6/§7/§9/§10/附录(全部 T001 条目改 DEFERRED)
- `specs/001-pA/DECISIONS-LOG.md` 新增 G11 决策记录
- `specs/001-pA/STATUS.md` 顶部加 0.4.0 状态行

---

**approved-provider: ~~__________~~ DEFERRED-TO-V2 (0.4.0 · 2026-04-24)**

> ~~operator 在本地签字~~ → **本 v0.1 报告不签 approved-provider**(详见 §7)· Phase 2 T001-v2 跑完后在新报告 `T001-llm-provider-report-v2.md` 末尾签 `approved-provider: <name>` 或 `approved-provider: FALLBACK_TO_HEURISTIC`。
> Phase 0/1 不再阻塞:走 stub heuristic 路径(`LLM_JUDGE_ENABLED=false` + `LLM_SUMMARIZE_ENABLED=false`)· 详见 spec.md 0.4.0 §5 Phase 0 + tasks/T004.md §"Stub 实现范围"。
