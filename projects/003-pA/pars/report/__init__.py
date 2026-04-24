"""
pars.report — 决策报告生成层。

职责：读取 runs/<id>/metrics.jsonl 与 artifacts/，按 architecture §9 的
强制 schema 渲染 report.md 和 failure_attribution.md。

T020 实现：
  - failure_schema.py  — FailureAttribution Pydantic v2 模型 + 校验器 + 解析器
  - failure_prompt.py  — 给 worker 的失败归因 prompt 模板 + 渲染函数

T021 负责：report 主渲染（消费本模块的 strict gate API）
"""

# T020: FailureAttribution schema 层
from pars.report.failure_schema import (
    CauseCategory,
    FailureAttribution,
    from_json,
    parse_markdown,
    to_json,
    validate,
    validate_quality,
)

# T020: failure prompt 模板层
from pars.report.failure_prompt import (
    FAILURE_PROMPT_TEMPLATE,
    render_failure_prompt,
)

__all__ = [  # noqa: RUF022
    # T020: schema 核心
    "CauseCategory",
    "FailureAttribution",
    # T020: 校验器 + 解析器
    "parse_markdown",
    "validate_quality",
    "validate",
    # T020: 序列化便捷函数
    "to_json",
    "from_json",
    # T020: prompt 模板
    "FAILURE_PROMPT_TEMPLATE",
    "render_failure_prompt",
]
