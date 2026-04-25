# Codex Inbox · 001-pA · T001 LLM Spike Second-Opinion Review

**Kickoff time**: 2026-04-24T15:00:00Z
**Reviewer role**: GPT-5.4 xhigh · LLM Spike Second-Opinion Reviewer
**Mission**: 复核 T001 spike (GLM5.1) judge_accuracy=14/20 是否真的"算过 70% gate" · 给出 proceed / refine-prompt-then-rerun / fallback 的明确建议
**Recommended model**: gpt-5.4
**Recommended reasoning_effort**: xhigh
**Max runtime**: ≤ 30 min
**Output language**: 中文

---

## Context

T001 是 001-pA Phase 0 的强制 spike(spec.md §6 T001 验收) · 目的是验证 LLM-as-Judge 在 paper-shift detection 任务上是否到 commercial 阈值。

- Provider: GLM5.1 via 火山引擎 ARK
- Fixture: `tests/fixtures/human-labeled-20.json` (20 条 · 10 shift / 6 incremental / 4 unrelated · human-labeled gold)
- Run 文件: `projects/001-pA/spikes/runs/glm-2026-04-24T14-12-29-901Z.json`
- 报告: `projects/001-pA/spikes/T001-llm-provider-report.md`(operator 已填 §1/§2/§3 · §4 是 Claude 草稿 · §5 触发本 review)

按 `tech-stack.md §2.5` 三 gate:
- judge_accuracy ≥ 14/20 = 70% **→ 14/20 擦边过**
- p95_summarize ≤ 5000 ms **→ 实测 46289 ms · 超 9.3× ❌**
- monthly_cost ≤ $50/月 (60k calls 假设 + GPT-5.4 placeholder 价位) **→ $1838.5 · 超 36.8× ❌ · 但单价依赖火山真实账单未到位**

按 §5 模糊带规则 [13/20, 15/20] = 65%–75% → 触发本 review · operator 等结论再签 approved-provider。

---

## 你需要回答的三个问题

### Q1 · 14/20 命中是否"真命中"?

逐条复核 14 条人类 vs 模型一致 record · 判断**是否存在"理由错但标签蒙对"** ——
即 verdict.label 对、但 verdict.rationale 没真正抓到 anchor vs candidate 的关键区别(例如把 incremental 改进硬包装成 "shift" 但恰好 human label 也是 shift 这种伪命中)。

**输入读这些**:
- run 文件 records[0..19] 全部 verdict.rationale 字段
- `tests/fixtures/human-labeled-20.json` 每条的 `human_rationale` 或 `notes` 字段(若有)
- `specs/001-pA/reference/llm-adapter-skeleton.md` §3.5 / §6 中 prompt 的 verdict 判定标准定义

**输出**: 14 条命中分桶
- "真命中"(rationale 抓到关键差异): N 条
- "伪命中"(label 对但 rationale 离题或脑补): M 条
- 真命中率 = N / 14

### Q2 · 4 条 incremental→shift 误判是 prompt 问题还是模型问题?

误判样本: f11 (PsiPO) · f12 (Mamba-2) · f14 (DeepSeekMoE) · f15 (QLoRA) · 全部 confidence ≥ 0.85
人类标签 incremental · 模型 verdict shift。

**输入读这些**:
- run 文件 records f11/f12/f14/f15 的 verdict.rationale 全文
- 对应 fixture 4 条的 anchor abstract + candidate abstract + human notes
- prompt 中 shift vs incremental 的判别条文(`llm-adapter-skeleton.md` §3.5 / §6)

**判断**:
- 是不是 prompt 把 "对前作的实质改进" 和 "颠覆 anchor 假设" 的边界写得太模糊,导致 GLM5.1 都往 shift 推?
- 还是 GLM5.1 模型本身的判别偏差(同样 prompt 给 Claude / GPT 大概率不会都误升)?
- 收紧 prompt 边界(例如显式列举 "改进现有方法 ≠ shift" 反例)能改善吗?预估能从 4 错→几错?

**输出**: 一段 ≤ 200 字诊断 · 二选一: prompt-fixable / model-inherent

### Q3 · 整体建议: proceed / refine-prompt-then-rerun / fallback?

综合 Q1 + Q2 + 延迟 ❌ + 成本 (待真实账单) 的全图,给一个**明确建议**:

- **proceed** (签 `approved-provider: glm-5.1`)
  - 仅当: Q1 真命中率 ≥ 12/14 且 Q2 判 model-inherent (refine prompt 也救不了多少) 且 operator 接受延迟 + 成本写进 risks.md
  - 同时给出 risks.md TECH-1 应补充的具体登记内容
- **refine-prompt-then-rerun** (不签 · bump prompt_version · 重跑)
  - 仅当: Q2 判 prompt-fixable 且预估能把 judge_accuracy 推到 16/20 以上 (可清晰过 gate 不再擦边)
  - 给出 prompt 收紧的具体改写建议(原文 + 改写 diff)
- **fallback** (签 `approved-provider: FALLBACK_TO_HEURISTIC` · 关闭 LLM judge)
  - 仅当: Q1 真命中率 < 10/14 (即"真过 gate"也存疑) · 或 Q2 判 model-inherent + 同时延迟无法解决
  - 给出 fallback 后 LLM 仅 summarize 的 spec 路径调整建议(spec.md OP-Q1 flag 应翻成什么值)

---

## Rules

1. **不要重跑 spike** · 本 review 只读现有 run 数据 + spec/prompt 文件 · 不调用 GLM
2. **不要修改 spec/prompt 源文件** · 只在 outbox 给改写建议
3. **不能用 WebSearch / WebFetch** · 全部基于本仓库证据
4. **不要扩散到非 T001 范围** · 不要评论 T002/T003/T010 等其他 task · 不要重开 R_final3 已 ✅ 的 G 项
5. 如果某个证据不足以判断,标 ⚠️ 并说明缺什么数据 · 不要硬猜

---

## 完成后

写到 `.codex-outbox/20260424T150000-001-pA-T001-spike-second-opinion.md`

格式:

```markdown
# T001 Spike Second-Opinion Review

**Reviewer**: GPT-5.4 xhigh
**Completed**: <ISO>
**Runtime**: ~<N> min
**Scope**: T001 GLM5.1 spike judge_accuracy=14/20 模糊带复核

## Q1 · 14/20 真命中率

| fixture_id | human | verdict | rationale 真假 | 备注 (≤ 1 行) |
|---|---|---|---|---|
| f1 | shift | shift | 真/伪 | ... |
| f2 | shift | shift | 真/伪 | ... |
| ... 14 行 ... |

**真命中**: N / 14
**伪命中**: M / 14
**评估**: <一句话总结>

## Q2 · 4 条 incremental→shift 误判诊断

| fixture_id | 误判类型 | 关键 prompt 漏洞 (若 prompt-fixable) |
|---|---|---|
| f11 | ... | ... |
| f12 | ... | ... |
| f14 | ... | ... |
| f15 | ... | ... |

**判定**: prompt-fixable / model-inherent
**理由**: ≤ 200 字
**预估改善**: 若 prompt-fixable,改写后 judge_accuracy 预估到 X/20

## Q3 · 最终建议

**Verdict**: proceed / refine-prompt-then-rerun / fallback

**理由**: ≤ 300 字 · 必须显式说明:
- 为什么不是另两个选项
- 延迟 ❌ 这条结构性问题怎么处理
- 成本 ❌ 是否需等火山真实账单到位才能终判

**给 operator 的下一步**:
- 若 proceed: risks.md TECH-1 应补登记的内容
- 若 refine-then-rerun: prompt 改写 diff (原文 → 新版 · 行号)
- 若 fallback: spec.md OP-Q1 flag 应翻的值 + 影响的下游 task 清单

## Self-flag (可选)

<本 review 中你做了哪些假设 · 哪些证据缺失只能标 ⚠️ · operator 应当知道的边界>
```

---

## Operational constraints

- **No WebSearch, no WebFetch** · 仅本仓库证据
- **Cite file:line** for 关键判断
- **Chinese output** · 报告整体中文 · 行内技术名 / 文件路径保持英文
- **30 min hard cap** · 单个 Q 超 10 min 标 ⚠️ 移到下一个 Q
- **不能改任何源文件** · review 文件以外不写任何东西
