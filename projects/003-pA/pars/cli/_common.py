"""
pars.cli._common — CLI 层共享工具函数（T005）。

结论：封装 logging 初始化、错误格式化、强制退出三个 helper，
供所有子命令复用，避免重复代码。

设计原则：
- 纯函数（无全局状态），方便测试 mock
- 不依赖具体命令逻辑（保持横切关注点分离）
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import typer

from pars.logging import configure_root


# ---------------------------------------------------------------------------
# setup_logging
# ---------------------------------------------------------------------------

def setup_logging(verbose: bool = False) -> None:
    """包装 T004 configure_root，供子命令在需要时显式初始化。

    参数：
        verbose : 若 True，以 DEBUG 级别配置 logger；否则默认 INFO。

    注意：
        通常不需手动调用，因为 app.callback()（main.py）已在启动时调用
        configure_root()。仅在独立脚本或测试中需要显式初始化时使用。
    """
    level = "DEBUG" if verbose else None  # None 时 configure_root 读 PARS_LOG_LEVEL
    configure_root(level=level, force=True)


# ---------------------------------------------------------------------------
# format_error
# ---------------------------------------------------------------------------

def format_error(e: Exception) -> str:
    """将异常转换为用户友好的 CLI 错误消息。

    格式：[ERROR] <ExceptionType>: <message>
    不暴露 traceback（防止技术信息吓到用户）；
    traceback 已由 logger.exception() 写入 stderr JSON 日志。

    参数：
        e : 要格式化的异常对象

    返回：
        可直接传给 typer.echo() / die() 的字符串
    """
    return f"[ERROR] {type(e).__name__}: {e}"


# ---------------------------------------------------------------------------
# validate_run_id
# ---------------------------------------------------------------------------

def validate_run_id(ulid_str: str) -> str:
    """校验 run ID 格式（ULID：26 位大写字母/数字，D14 约定）。

    参数：
        ulid_str : 待校验的字符串

    返回：
        有效时返回原始字符串（便于链式调用）

    抛出：
        typer.BadParameter : 格式不合法时
    """
    # ULID 格式：26 位，字符集 0-9A-HJKMNP-TV-Z（Crockford Base32 子集）
    # 简化校验：长度 + 全大写字母数字（不区分 Crockford 字符集，避免过度严格）
    clean = ulid_str.strip()
    if not clean:
        raise typer.BadParameter("run ID 不能为空")
    if len(clean) != 26:
        raise typer.BadParameter(
            f"run ID 应为 26 位 ULID，当前长度 {len(clean)}：{clean!r}"
        )
    if not clean.isalnum() or not clean.isupper():
        # 允许全大写字母数字（ULID 字符集子集）
        if not all(c in "0123456789ABCDEFGHJKMNPQRSTVWXYZ" for c in clean):
            raise typer.BadParameter(
                f"run ID 包含非法字符（ULID 格式要求大写 Crockford Base32）：{clean!r}"
            )
    return clean


# ---------------------------------------------------------------------------
# print_run_dir
# ---------------------------------------------------------------------------

def print_run_dir(path: Path) -> None:
    """向 stdout 打印 run 目录路径（供子命令成功后提示用户）。

    参数：
        path : run 目录路径（绝对）
    """
    typer.echo(f"run 目录：{path}")


# ---------------------------------------------------------------------------
# rich_table_for_config
# ---------------------------------------------------------------------------

def rich_table_for_config(d: dict[str, Any]) -> None:
    """将配置字典以 rich 表格形式打印到 stdout。

    参数：
        d : 要展示的配置字典（一级展开）

    注意：
        仅打印，不返回值。后续若需返回 rich.Table 对象再重构。
    """
    try:
        from rich.console import Console
        from rich.table import Table

        console = Console()
        table = Table(title="Config", show_header=True, header_style="bold cyan")
        table.add_column("Key", style="dim")
        table.add_column("Value")
        for key, value in d.items():
            table.add_row(str(key), str(value))
        console.print(table)
    except ImportError:
        # fallback：rich 未安装时降级为普通输出
        for key, value in d.items():
            typer.echo(f"  {key}: {value}")


# ---------------------------------------------------------------------------
# die
# ---------------------------------------------------------------------------

def die(msg: str, code: int = 1) -> None:
    """打印错误消息到 stderr 并以指定退出码退出进程。

    参数：
        msg  : 要显示的错误消息
        code : 退出码（默认 1）

    注意：
        此函数**不返回**（调用 raise typer.Exit），后续代码不会执行。
        在 CLI 命令中使用，而非在库函数中使用（库应抛出异常而非退出）。
    """
    typer.echo(msg, err=True)
    raise typer.Exit(code)
