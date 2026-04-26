# conflict_assembler_v1 — ConflictReportAssembler 提示词设计文档

**版本**: v1.0
**对应任务**: T010
**template_version**: `"conflict_assembler_v1"`
**LLM 输出 schema**: `ConflictReportLLMOutput` (divergence_root_cause + has_divergence)

---

## 核心原则

### R10 红线: 中立聚合，不选 winner

- **严禁**输出 `priority` / `winner` / `recommended` / `建议` / `推荐` / `更好` 等引导性词汇
- **目的**: 保留投资人的独立判断空间，不通过 AI 文案引导决策
- **衡量标准**: 读者读完报告后，只知道"分歧在哪"，不知道"应该怎么做"

### 不变量 #4: rationale_plain 必须有白话解释

- 每个 signal 的 `rationale_plain` 必须是可读的白话描述
- 不允许黑箱输出（如"模型判断为 LONG"）
- divergence_root_cause 同样需要白话化

---

## 提示词结构

```
分析以下三个独立视角对 {ticker} 的判断，客观评估是否存在实质性分歧。

各视角信号:
- {source_id}: 方向={direction}, 置信度={confidence}
  分析: {rationale_plain}

要求:
1. 客观描述各视角的分歧点（如有），不要选择 winner 或推荐方向
2. 不要使用 '建议' '推荐' '应该' '更好' 等引导性词汇
3. divergence_root_cause: 简洁白话描述分歧根因，无分歧时填 '暂无分歧'
4. has_divergence: 是否存在实质性分歧（方向不同 = True，相同或均 no_view = False）
```

---

## 边界案例处理

### 全 no_view 场景

- 三路 signals 均为 `no_view` 时，**直接返回** `has_divergence=False, divergence_root_cause="暂无分歧"`
- 不需要调用复杂 LLM 分析（在代码层面短路）

### 部分 no_view 场景

- 若只有部分视角为 `no_view`，仍需分析有观点的视角之间是否分歧
- `has_divergence` 取决于**有观点**的视角之间是否一致

### 高度一致场景

- 三路均 LONG / 均 NEUTRAL 等 → `has_divergence=False`
- divergence_root_cause 写："三路视角方向一致，无实质性分歧"

---

## 失败处理 (R3 #13)

- LLM 调用失败时 **raise**，不返回 placeholder stub
- 调用方 (DecisionRecorder.create_draft) 负责 catch 并返回 503

---

## 版本迭代计划

| 版本 | 变化 |
|------|------|
| v1.0 | 初始版本，基础分歧识别 |
| v1.1 | 计划: 加入时序分析（历史信号趋势）|
| v2.0 | 计划: 替换 PlaceholderModelStrategy → 真实量化模型 |
