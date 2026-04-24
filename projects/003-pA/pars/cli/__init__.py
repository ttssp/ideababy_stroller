"""
pars.cli — Typer CLI 入口层。

职责：解析命令行参数，调用 Orchestrator 启动 run，展示进度与报告路径。
具体命令（sft start / resume / status / list 等）由 T005 实现。
"""

# T005: 导出 app，使 pyproject.toml [project.scripts] `pars = "pars.cli.main:app"` 可 resolve
from pars.cli.main import app  # noqa: E402

__all__ = ["app"]
