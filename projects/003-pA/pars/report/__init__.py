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

# T021: schema 校验层（不引入 matplotlib 依赖，安全前置加载）
from pars.report.schema_validator import (
    validate_report_artifacts,
    validate_report_schema,
)

# T021: 报告渲染层 + 图表生成层（延迟导入，避免 matplotlib 在 import time 加载）
# 调用方可直接 from pars.report.renderer import render_report
# 或 from pars.report.charts import plot_eval_scores, plot_training_loss
def render_report(run_dir):  # noqa: ANN001, ANN201
    """延迟导入 renderer.render_report，避免 matplotlib Agg 在 import time 加载。"""
    from pars.report.renderer import render_report as _render_report  # noqa: PLC0415
    return _render_report(run_dir)


def plot_eval_scores(baseline_scores, lora_scores, out_path):  # noqa: ANN001, ANN201
    """延迟导入 charts.plot_eval_scores。"""
    from pars.report.charts import plot_eval_scores as _fn  # noqa: PLC0415
    return _fn(baseline_scores, lora_scores, out_path)


def plot_training_loss(loss_records, out_path):  # noqa: ANN001, ANN201
    """延迟导入 charts.plot_training_loss。"""
    from pars.report.charts import plot_training_loss as _fn  # noqa: PLC0415
    return _fn(loss_records, out_path)


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
    # T021: 报告渲染
    "render_report",
    # T021: schema 校验
    "validate_report_schema",
    "validate_report_artifacts",
    # T021: 图表生成
    "plot_eval_scores",
    "plot_training_loss",
]
