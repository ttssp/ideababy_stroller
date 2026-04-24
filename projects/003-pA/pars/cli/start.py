"""
pars.cli.start — `pars sft start` Typer 命令实现（T023）。

结论：构造 RunConfig + 调用 RunOrchestrator.start()，映射退出码。

## 参数列表（完整，与 T023 spec 对齐）

    --question TEXT              研究假设（required）
    --base TEXT                  HuggingFace base model ID（required）
    --dataset TEXT               HuggingFace 数据集 ID（required）
    --dataset-split TEXT         数据集 split（默认 train[:100]）
    --lora-rank INT              LoRA rank（默认 16）
    --lora-alpha INT             LoRA alpha（默认 32）
    --lr FLOAT                   学习率（默认 2e-4）
    --epochs INT                 训练 epoch 数（默认 3）
    --batch-size INT             per-device batch size（默认 2）
    --max-seq-len INT            最大序列长度（默认 2048）
    --eval-tasks TEXT            lm-eval task 列表，逗号分隔（默认 gsm8k）
    --usd-cap FLOAT              USD 硬帽（默认 30.0）
    --wall-clock-hours-cap FLOAT wall-clock 时间上限（小时，默认 12.0）
    --gpu-hours-cap FLOAT        GPU 小时上限（默认 12.0）
    --name TEXT                  覆盖自动生成的 ULID（可选）

## 退出码约定

    0 = completed（RunHandle.exit_code == 0）
    2 = config 错误（ApiKeyMissingError / ReadonlyFailsClosed / Pydantic 校验失败）
    3 = stuck（RunHandle.exit_code == 3）
    4 = budget（RunHandle.exit_code == 4）
    5 = worker crash（RunHandle.exit_code == 5）
"""

from __future__ import annotations

import sys
from typing import Annotated, Optional

import typer

from pars.logging import get_logger
from pars.orch.orchestrator import ApiKeyMissingError, RunOrchestrator

logger = get_logger(__name__)

# ---------------------------------------------------------------------------
# Typer 命令函数（供 main.py 挂载到 sft_app 上）
# ---------------------------------------------------------------------------


def start(
    question: Annotated[
        str,
        typer.Option("--question", help="研究假设文本（写入 run ledger 和报告）"),
    ],
    base: Annotated[
        str,
        typer.Option("--base", help="HuggingFace base model ID（如 TinyLlama/TinyLlama-1.1B-Chat-v1.0）"),
    ],
    dataset: Annotated[
        str,
        typer.Option("--dataset", help="HuggingFace 数据集 ID（如 tatsu-lab/alpaca）"),
    ],
    dataset_split: Annotated[
        str,
        typer.Option("--dataset-split", help="数据集 split（默认 train[:100]）"),
    ] = "train[:100]",
    lora_rank: Annotated[
        int,
        typer.Option("--lora-rank", help="LoRA rank（默认 16）"),
    ] = 16,
    lora_alpha: Annotated[
        int,
        typer.Option("--lora-alpha", help="LoRA alpha（默认 32）"),
    ] = 32,
    lr: Annotated[
        float,
        typer.Option("--lr", help="学习率（默认 2e-4）"),
    ] = 2e-4,
    epochs: Annotated[
        int,
        typer.Option("--epochs", help="训练 epoch 数（默认 3）"),
    ] = 3,
    batch_size: Annotated[
        int,
        typer.Option("--batch-size", help="per-device batch size（默认 2）"),
    ] = 2,
    max_seq_len: Annotated[
        int,
        typer.Option("--max-seq-len", help="最大序列长度（默认 2048）"),
    ] = 2048,
    eval_tasks: Annotated[
        str,
        typer.Option("--eval-tasks", help="lm-eval task 列表，逗号分隔（默认 gsm8k）"),
    ] = "gsm8k",
    usd_cap: Annotated[
        float,
        typer.Option("--usd-cap", help="USD 硬帽（默认 30.0）"),
    ] = 30.0,
    wall_clock_hours_cap: Annotated[
        float,
        typer.Option("--wall-clock-hours-cap", help="wall-clock 时间上限（小时，默认 12.0）"),
    ] = 12.0,
    gpu_hours_cap: Annotated[
        float,
        typer.Option("--gpu-hours-cap", help="GPU 小时上限（默认 12.0）"),
    ] = 12.0,
    name: Annotated[
        Optional[str],
        typer.Option("--name", help="覆盖自动生成的 ULID（可选，供测试和复现）"),
    ] = None,
) -> None:
    """启动新的 SFT 训练 run（baseline + LoRA + eval + 决策报告完整循环）。

    典型用法：
        pars sft start \\
            --question "Does LoRA improve GSM8K accuracy?" \\
            --base TinyLlama/TinyLlama-1.1B-Chat-v1.0 \\
            --dataset tatsu-lab/alpaca
    """
    # 解析 eval_tasks（逗号分隔 → list）
    eval_task_list = [t.strip() for t in eval_tasks.split(",") if t.strip()]
    if not eval_task_list:
        eval_task_list = ["gsm8k"]

    logger.info(
        "pars sft start 启动",
        extra={
            "question": question,
            "base_model": base,
            "dataset": dataset,
            "run_name": name,
        },
    )

    # 实例化编排器并执行
    orch = RunOrchestrator()
    try:
        handle = orch.start(
            research_question=question,
            base_model=base,
            dataset_id=dataset,
            dataset_split=dataset_split,
            lora_rank=lora_rank,
            lora_alpha=lora_alpha,
            lr=lr,
            epochs=epochs,
            batch_size=batch_size,
            max_seq_len=max_seq_len,
            eval_tasks=eval_task_list,
            usd_cap=usd_cap,
            wall_clock_hours_cap=wall_clock_hours_cap,
            gpu_hours_cap=gpu_hours_cap,
            run_id=name,
        )
    except ApiKeyMissingError as exc:
        # ANTHROPIC_API_KEY 缺失 → 退出码 2
        typer.echo(f"[ERROR] API key 缺失：{exc}", err=True)
        typer.echo(
            "请先设置环境变量：export ANTHROPIC_API_KEY=sk-ant-...",
            err=True,
        )
        raise typer.Exit(2) from exc
    except Exception as exc:
        # 其他 fail-fast 错误（ReadonlyFailsClosed / Pydantic 校验失败等）
        # 检查是否为 ReadonlyFailsClosed（避免循环 import）
        exc_type = type(exc).__name__
        if exc_type == "ReadonlyFailsClosed":
            typer.echo(
                f"[ERROR] .claude/ fail-closed 保护触发（C21）：{exc}",
                err=True,
            )
            typer.echo(
                "OQ5：工作目录 .claude/ 无法以只读模式挂载，拒绝启动。"
                "请检查文件权限或联系管理员。",
                err=True,
            )
            raise typer.Exit(2) from exc
        # 其他未预期异常：传播，显示完整错误
        logger.error("pars sft start 未预期异常", exc_info=exc)
        typer.echo(f"[ERROR] 未预期错误：{exc}", err=True)
        raise typer.Exit(5) from exc

    # 打印运行结果
    _print_handle_result(handle)

    # 映射退出码
    raise typer.Exit(handle.exit_code)


def _print_handle_result(handle) -> None:  # noqa: ANN001
    """打印 RunHandle 结果摘要（rich 若可用，否则纯文本 fallback）。

    结论：避免 CI 环境 rich.Table 乱行，统一用 typer.echo 纯文本输出。
    """
    import os

    use_plain = os.environ.get("PARS_NO_COLOR") or not sys.stdout.isatty()

    if use_plain:
        typer.echo(f"[OK] run_id={handle.run_id}")
        typer.echo(f"     final_state={handle.final_state}")
        typer.echo(f"     exit_code={handle.exit_code}")
        if handle.report_path:
            typer.echo(f"     report={handle.report_path}")
        if handle.failure_reason:
            typer.echo(f"     reason={handle.failure_reason}")
        return

    try:
        from rich import print as rprint
        from rich.panel import Panel

        status_emoji = {0: "完成", 3: "超时(stuck)", 4: "预算超限", 5: "worker crash"}.get(
            handle.exit_code, "未知"
        )
        lines = [
            f"[bold]run_id[/bold]      : {handle.run_id}",
            f"[bold]final_state[/bold] : {handle.final_state}",
            f"[bold]exit_code[/bold]   : {handle.exit_code} ({status_emoji})",
        ]
        if handle.report_path:
            lines.append(f"[bold]report[/bold]      : {handle.report_path}")
        if handle.failure_reason:
            lines.append(f"[bold]reason[/bold]      : {handle.failure_reason}")

        rprint(Panel("\n".join(lines), title="pars sft start 结果", expand=False))
    except ImportError:
        # rich 不可用时 fallback 纯文本
        typer.echo(f"run_id={handle.run_id} exit_code={handle.exit_code}")
