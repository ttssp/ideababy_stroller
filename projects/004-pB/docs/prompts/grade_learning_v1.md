# grade_learning_v1 — 学习检查评分 Prompt (T019 R3)

## 版本
v1 — 仅评分，不抽题，不出题（R3 真砍：extract / generate_question prompt 已删除）

## 用途
`scripts/grade_learning.py` 调用 LLMClient 时使用此 prompt，比对 human 答案与标准答案，
给出 0-10 整数分。

## 调用时机
仅在 `scripts/grade_learning.py --quarter <quarter_id>` 时调用 LLM。
`LearningCheckService` 服务路径（抽题、答题录入）**不调用 LLM**。

---

## Prompt 模板 (Python format string)

```
你是一位学习评估专家。请评估以下投资决策系统学习检查答案的质量。

## 评分规则
- 评分范围: 0-10 整数
- 10分: 完全掌握核心概念，答案准确且有深度
- 7-9分: 基本掌握，主旨正确，细节可能不完整
- 4-6分: 部分理解，有明显缺漏或误解
- 1-3分: 极少掌握，答案偏离核心概念
- 0分: 未作答或完全错误

## 评分要求
- 主旨匹配优先：不强求逐字对照，只要核心概念准确即可得高分
- 宽容理解：允许不同的表达方式，重点是理解深度
- 只输出 JSON，不输出任何解释文字

## 待评估内容

概念: {concept}

标准答案:
{standard_answer}

Human 答案:
{human_answer}

## 输出格式 (严格 JSON)

{{
  "score": <0-10 整数>,
  "brief_reason": "<20字以内，说明扣分主因或满分原因>"
}}
```

---

## 输出 Schema

```python
class GradeResult(BaseModel):
    score: int          # 0-10
    brief_reason: str   # ≤ 20 字
```

## 注意事项
- `brief_reason` 仅供内部记录，不展示给 human（避免引导）
- 均分 ≥ 7.0 视为本季度通过 (O4 verification)
- 单次调用评估单个概念，批量评估用 `asyncio.gather`
