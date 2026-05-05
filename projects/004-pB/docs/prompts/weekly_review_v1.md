# weekly_review_v1 — T014 周报摘要 Prompt

结论: 注入周报数据，要求 LLM 生成 ≤200 字中文摘要，强调不动/等待是纪律。
细节:
  - prompt_template_version: "weekly_review_v1" (与 WeeklyReviewService 代码对应)
  - schema: WeeklySummaryOutput.summary (str)
  - 模板变量由 `_build_summary_prompt()` 动态注入，此文档记录模板设计意图

## 模板骨架（参考）

```
周报数据 ({week_id}):
- 总决策: {total_decisions} 条
- 按动作: {breakdown_str}
- 不动占比 (hold+wait): {inactive_ratio:.1%}

请生成 ≤200 字的中文周度 calibration 摘要，
重点: 不动/等待是好事 (R6 反诱导高频交易)，
强调纪律性而非短期活跃度。
```

## 设计约束

- 输出 ≤ 200 字（中文字数，含标点）
- 不得包含投资建议或对特定股票的判断
- R6: 正向强化 hold/wait 行为（反诱导高频交易）
- 输出通过 WeeklySummaryOutput.summary 字段返回

## 版本历史

| 版本 | 变更 | 日期 |
|------|------|------|
| v1   | 初始版本，含 R6 约束 | 2026-04-27 |
