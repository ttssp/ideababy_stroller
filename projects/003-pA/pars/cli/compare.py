"""
pars.cli.compare — 顶层 `pars compare` 命令实现（T025 · O6）

结论：实现 `pars compare <run_a_id> <run_b_id> [--output PATH]` 命令。
      - 默认输出到 stdout（三栏 markdown diff + ## Verdict 节）
      - 若提供 --output PATH，额外写入文件（并在 stdout 打印写入确认）
      - 调用 pars.compare.engine.compare() 获取 ComparisonResult

命令行签名：
    pars compare RUN_A RUN_B [--output FILE]

退出码：
    0: 成功
    1: 内部错误（run 目录不存在 / config 损坏 / eval 缺失等）
"""

from __future__ import annotations

from pathlib import Path
from typing import Annotated, Optional

import typer

from pars.logging import get_logger

logger = get_logger(__name__)


def run_compare(
    run_a_id: Annotated[
        str,
        typer.Argument(help="第一个 run ID（runA）"),
    ],
    run_b_id: Annotated[
        str,
        typer.Argument(help="第二个 run ID（runB）"),
    ],
    output: Annotated[
        Optional[Path],
        typer.Option(
            "--output",
            "-o",
            help="将 markdown 差异表写入指定文件（默认仅打印到 stdout）",
            writable=True,
            resolve_path=False,
        ),
    ] = None,
) -> None:
    """对比两个 run 的 config / metric / 结论差异，输出 markdown 差异表。

    O6 决策合约：输出必含明确的 "pick runX" 决策（eval_score 最高者胜）。
    三栏 markdown（## Config diff / ## Metric diff / ## Conclusion diff）+ ## Verdict。
    """
    from pars.compare.engine import compare

    try:
        result = compare(run_a_id, run_b_id)
    except ValueError as exc:
        typer.echo(f"[ERROR] {exc}", err=True)
        raise typer.Exit(1) from exc
    except Exception as exc:
        logger.exception("pars compare 内部错误", exc_info=exc)
        typer.echo(f"[ERROR] compare 失败：{exc}", err=True)
        raise typer.Exit(1) from exc

    # 输出到 stdout
    typer.echo(result.markdown)

    # 若指定 --output，写入文件
    if output is not None:
        output = Path(output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(result.markdown, encoding="utf-8")
        typer.echo(f"[OK] 差异表已写入：{output}", err=True)

    logger.info(
        "pars compare 完成",
        extra={"run_a": run_a_id, "run_b": run_b_id, "verdict": result.verdict},
    )
