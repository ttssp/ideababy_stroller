"""
pars.cli.status — `pars sft status` 的实现。

结论：从 ledger 读取 run 信息，以 rich Table 渲染到终端。
      无 run_id 时显示最近 10 条 run 摘要列表；
      有 run_id 时显示单个 run 的详细信息。

依赖：
  - pars.ledger.ledger: list_runs, get_run_summary, run_exists
  - rich: Console, Table（彩色表格输出）
"""

from __future__ import annotations

import sys
from typing import Any

import typer
from rich.console import Console
from rich.table import Table

from pars.ledger.ledger import get_run_summary, list_runs, run_exists


# ---------------------------------------------------------------------------
# 公开入口
# ---------------------------------------------------------------------------


def run_status(run_id: str | None) -> None:
    """执行 pars sft status 命令逻辑。

    结论：
    - run_id 为 None：显示最近 10 条 run 的摘要列表表格
    - run_id 指定：显示单个 run 的详细信息表格
    - run 不存在：打印错误信息到 stderr 并退出 1

    Args:
        run_id: 指定的 run ID（ULID）；None 表示显示列表
    """
    if run_id is None:
        _print_all_runs()
    else:
        _print_run_detail(run_id)


# ---------------------------------------------------------------------------
# 内部渲染
# ---------------------------------------------------------------------------


def _print_all_runs(*, limit: int = 10) -> None:
    """渲染最近 N 条 run 的摘要列表。

    结论：
    - 无 run 时打印提示信息，退出码 0
    - 有 run 时渲染 rich Table：run_id | phase | status | usd_spent/usd_cap | research_question

    Args:
        limit: 最多显示条数（默认 10）
    """
    console = Console()
    runs = list_runs(limit=limit)

    if not runs:
        console.print("[yellow]暂无 SFT run。使用 `pars sft start` 创建第一个 run。[/yellow]")
        return

    table = Table(title=f"最近 {len(runs)} 条 Run（最新在前）", show_lines=True)
    table.add_column("run_id", style="cyan", no_wrap=True)
    table.add_column("phase", style="magenta")
    table.add_column("status", style="bold")
    table.add_column("usd_spent / cap", justify="right")
    table.add_column("research_question", max_width=50, overflow="fold")

    for rid in runs:
        try:
            summary = get_run_summary(rid)
        except FileNotFoundError:
            continue

        status_style = _status_style(summary.get("status", "unknown"))
        usd_str = "{:.4f} / {:.2f}".format(
            summary.get("usd_spent", 0.0),
            summary.get("usd_cap", 0.0),
        )
        table.add_row(
            rid,
            summary.get("phase", "unknown"),
            f"[{status_style}]{summary.get('status', 'unknown')}[/{status_style}]",
            usd_str,
            summary.get("research_question", ""),
        )

    console.print(table)


def _print_run_detail(run_id: str) -> None:
    """渲染单个 run 的详细信息表格。

    结论：
    - run 不存在：打印错误信息到 stderr，调用 raise typer.Exit(1)
    - run 存在：渲染 rich Table 显示所有关键字段

    Args:
        run_id: 26 字符 ULID
    """
    console = Console()

    if not run_exists(run_id):
        console.print(
            f"[red]错误：run {run_id!r} 不存在。[/red]",
            file=sys.stderr,
        )
        raise typer.Exit(1)

    summary = get_run_summary(run_id)

    table = Table(title=f"Run 详情: {run_id}", show_lines=True)
    table.add_column("字段", style="bold cyan", no_wrap=True)
    table.add_column("值", overflow="fold")

    # 字段顺序固定，保证输出稳定性
    fields: list[tuple[str, str]] = [
        ("run_id", "run_id"),
        ("phase", "phase"),
        ("status", "status"),
        ("research_question", "research_question"),
        ("base_model", "base_model"),
        ("usd_spent", "usd_spent"),
        ("usd_cap", "usd_cap"),
        ("wall_clock_hours_cap", "wall_clock_hours_cap"),
        ("gpu_hours_cap", "gpu_hours_cap"),
        ("created_at", "created_at"),
    ]

    for label, key in fields:
        value = summary.get(key)
        value_str = _format_value(label, value)
        table.add_row(label, value_str)

    console.print(table)


# ---------------------------------------------------------------------------
# 辅助格式化
# ---------------------------------------------------------------------------


def _status_style(status: str) -> str:
    """将 status 字符串映射到 rich 样式名称。

    结论：
    - completed → green
    - failed → red
    - running → blue
    - pending / unknown / other → yellow
    """
    _map = {
        "completed": "green",
        "failed": "red",
        "running": "blue",
        "pending": "yellow",
    }
    return _map.get(status, "yellow")


def _format_value(label: str, value: Any) -> str:
    """将字段值格式化为适合终端显示的字符串。

    结论：
    - None 显示为灰色 "[dim]—[/dim]"
    - float 类型的 usd_spent/usd_cap 保留 4 位小数
    - 其他值调用 str()
    """
    if value is None:
        return "[dim]—[/dim]"
    if label in ("usd_spent", "usd_cap") and isinstance(value, float):
        return f"{value:.4f}"
    return str(value)
