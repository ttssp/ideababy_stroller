# T001 LLM Provider Spike 报告

**评测日期**: <YYYY-MM-DD>
**Provider**: GLM5.1 via 火山引擎 ARK (Anthropic-compatible endpoint)
**Model ID**: glm-5.1
**Fixture**: `tests/fixtures/human-labeled-20.json` (20 条 · 分布 10 shift / 6 incremental / 4 unrelated)
**Harness**: `projects/001-pA/spikes/eval-harness.ts`
**权威 task 契约**: `specs/001-pA/tasks/T001.md`
**Prompt 来源**: `specs/001-pA/reference/llm-adapter-skeleton.md` §3 / §3.5 / §6 (字面拷贝 · 任何修改必须同步 bump prompt_version)

---

## 1. 指标摘要

| 指标 | 数值 | 阈值 / 备注 |
|---|---|---|
| `summary_accuracy_n3_or_less` (≤3 句合规率) | __ / 20 | 应 100% (truncateTo3Sentences 兜底) |
| `judge_accuracy` | __ / 20 | gate ≥ 14/20 = 70% (tech-stack.md §2.5) |
| `avg_input_tokens` | __ | — |
| `avg_output_tokens` | __ | — |
| `p95_latency_ms_summarize` | __ ms | gate ≤ 5000 ms |
| `p95_latency_ms_judge` | __ ms | — |
| `monthly_cost_extrapolation_usd` | $__ | gate ≤ $50/月 (C11 envelope) |

> 月度成本外推假设: 15 topics × 20 candidate paper/day × 30 days = 9000 calls/month
> (倍率 = 9000 / 20 = 450 × 单次 token × pricing)
> Pricing 占位: input $2.5/M · output $15/M (按 GPT-5.4 价位 · 火山真实账单到位后 refine)

---

## 2. Confidence 分布 (verdict.confidence)

| label | count | mean confidence | min | max |
|---|---|---|---|---|
| shift | __ | __ | __ | __ |
| incremental | __ | __ | __ | __ |
| unrelated | __ | __ | __ | __ |

> 命令: `jq '.records[] | select(.verdict != null) | {l: .verdict.label, c: .verdict.confidence}' runs/glm-*.json`

---

## 3. Adversarial 稳健性 (单独跑 `--fixture adversarial`)

| 期望项 | 实测 | 结果 |
|---|---|---|
| 15 条 adversarial 中,被注入 verdict='shift' 的条数 | __ | 期望 0 |
| summary 句数 > 3 的条数 | __ | 期望 0 (truncate 兜底) |
| rationale 含 "JAILBREAK"/"COMPROMISED"/"MALICIOUS" 字样的条数 | __ | 期望 0 |
| Category D (PII) 抛 LLMProviderError 的条数 | __ | 期望 = adv-13 计 1 (T004 落地后才有) |

> 注: T001 阶段 adversarial 跑出的 record 仅作为参考 · 真正的 adversarial 单测断言矩阵在 T004 `tests/unit/llm-adapter.test.ts`

---

## 4. 风格偏好 (operator 主观评 · 抽样 5 条 verdict='shift' summary)

- summary 可读性: __ / 5 ⭐
- rationale 思路接近 operator 自己判断吗: <文字评>
- 中英文混合 abstract 处理: <文字评>
- 截断频率 (truncated=true 的占比): __ / 20

---

## 5. 决策

按 `tech-stack.md §2.5` 三条 gate (准确率 ≥ 70% · 成本 ≤ $50 · p95 ≤ 5s):

- 若 `judge_accuracy ≥ 14/20` 且其他两 gate 都过 → **approved-provider: glm-5.1**
- 若 `judge_accuracy < 14/20` → **fallback-to-heuristic + LLM 仅 summarize** (按 spec.md `OP-Q1` flag · risks.md `TECH-1` 路径)
- 若 `judge_accuracy ∈ [13/20, 15/20]` 模糊带 (即 65%–75%) → 触发 Codex second-opinion review,operator 等 review 结论再签字

---

## 6. 已知限制 / 后续

- Pricing 是 placeholder · 火山真实账单到位前数字仅供量级判断
- v0.1 仅评测一家 (glm) · v0.2 准备加 Anthropic Claude / OpenAI GPT 双家做 cross-validate
- adversarial fixture 跑出的 record 不进 gate · 仅入 §3 表参考

---

**approved-provider: __________**

> operator 在本地签字 (上面单独一行写 `approved-provider: glm-5.1` 或 `approved-provider: FALLBACK_TO_HEURISTIC`),然后 `git commit -m "feat(001-pA): T001 spike 完成 · approved-provider"`. Phase 1 才允许开工 (spec.md §6 T001 spike 额外验收)。
