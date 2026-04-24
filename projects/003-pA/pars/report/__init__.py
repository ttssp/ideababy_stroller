"""
pars.report — 决策报告生成层。

职责：读取 runs/<id>/metrics.jsonl 与 artifacts/，按 architecture §9 的
强制 schema 渲染 report.md 和 failure_attribution.md。
由 T010 实现。
"""
