"""
pars.cli.retry — `pars sft retry` Typer 命令实现（T024 · U4）。

结论：薄 wrapper，解析 CLI 参数后委托给 pars.orch.retry.start_retry。

命令签名：
    pars sft retry \\
        --from <run_id>        （必填，parent run ID）
        --hypothesis "..."     （必填，retry 动机）
        [--lr FLOAT]           （可选 override）
        [--epochs INT]         （可选 override）
        [--lora-rank INT]      （可选 override）
        [--lora-alpha INT]     （可选 override）
        [--batch-size INT]     （可选 override）
        [--max-seq-len INT]    （可选 override）
        [--question TEXT]      （可选 override research_question）
        [--name TEXT]          （可选：覆盖新 run_id，替换自动 ULID）

退出码约定（继承 RunOrchestrator）：
    0 = completed
    2 = config 错误（parent 不存在 / hypothesis 空 / ApiKeyMissingError）
    3 = stuck
    4 = budget
    5 = worker crash
"""

from __future__ import annotations

import sys
from typing import Annotated, Optional

import typer

from pars.logging import get_logger
from pars.orch.orchestrator import ApiKeyMissingError, RunOrchestrator

logger = get_logger(__name__)


def run_retry(
    from_run: Annotated[
        str,
        typer.Option("--from", help="基于哪个 run ID 创建新实验（继承 config，允许覆盖）"),
    ],
    hypothesis: Annotated[
        str,
        typer.Option("--hypothesis", help="本次 retry 的假设文本（必填，如 'LR 太高，尝试降低 3 倍'）"),
    ],
    lr: Annotated[
        Optional[float],
        typer.Option("--lr", help="学习率 override（不指定则继承 parent 或 hypothesis 建议值）"),
    ] = None,
    epochs: Annotated[
        Optional[int],
        typer.Option("--epochs", help="训练 epoch 数 override"),
    ] = None,
    lora_rank: Annotated[
        Optional[int],
        typer.Option("--lora-rank", help="LoRA rank override"),
    ] = None,
    lora_alpha: Annotated[
        Optional[int],
        typer.Option("--lora-alpha", help="LoRA alpha override"),
    ] = None,
    batch_size: Annotated[
        Optional[int],
        typer.Option("--batch-size", help="per-device batch size override"),
    ] = None,
    max_seq_len: Annotated[
        Optional[int],
        typer.Option("--max-seq-len", help="最大序列长度 override"),
    ] = None,
    question: Annotated[
        Optional[str],
        typer.Option("--question", help="研究假设文本 override（替换 parent 的 research_question）"),
    ] = None,
    name: Annotated[
        Optional[str],
        typer.Option("--name", help="覆盖自动生成的新 ULID（可选，供测试和复现）"),
    ] = None,
) -> None:
    """基于已有 run 创建新实验（调整超参数后重跑）。

    仅覆盖显式传入的参数，其余字段继承 parent run config。
    --hypothesis 为必填项，记录本次 retry 的动机（用于决策报告）。

    典型用法：
        # 继承全部参数，仅修改 lr（根据假设自动建议）
        pars sft retry --from <run_id> --hypothesis "LR 太高"

        # 显式指定 lr override（赢过自动建议）
        pars sft retry --from <run_id> --hypothesis "LR 太高" --lr 1e-5

        # 修改多个字段
        pars sft retry --from <run_id> --hypothesis "epoch 不足" --epochs 8 --lora-rank 32
    """
    from pars.orch.retry import start_retry, config_diff, derive_retry_config, load_parent_config

    logger.info(
        "pars sft retry 启动",
        extra={
            "from_run": from_run,
            "hypothesis": hypothesis,
        },
    )

    # 收集 CLI 显式 override（只放非 None 的参数）
    overrides: dict = {}
    if lr is not None:
        overrides["lr"] = lr
    if epochs is not None:
        overrides["epochs"] = epochs
    if lora_rank is not None:
        overrides["lora_rank"] = lora_rank
    if lora_alpha is not None:
        overrides["lora_alpha"] = lora_alpha
    if batch_size is not None:
        overrides["batch_size"] = batch_size
    if max_seq_len is not None:
        overrides["max_seq_len"] = max_seq_len
    if question is not None:
        overrides["research_question"] = question

    # 若 --name 指定，注入到 overrides（start_retry 会通过 run_id 参数传给 orchestrator）
    # 实际上 name 需要直接注入到 derive_retry_config 产生的 new_config.run_id
    # 这里在 start_retry 调用前先 derive，若指定 --name 则替换 run_id
    try:
        # 先 derive 得到新 config，用于打印 diff
        new_config = derive_retry_config(
            parent_run_id=from_run,
            hypothesis=hypothesis,
            overrides=overrides,
        )
    except FileNotFoundError as exc:
        typer.echo(f"[ERROR] parent run 不存在：{exc}", err=True)
        typer.echo(f"请确认 run ID '{from_run}' 存在且 config.yaml 可读。", err=True)
        raise typer.Exit(2) from exc
    except ValueError as exc:
        typer.echo(f"[ERROR] 参数校验失败：{exc}", err=True)
        raise typer.Exit(2) from exc

    # 若指定 --name，替换 new_config 的 run_id
    if name is not None:
        new_config = new_config.model_copy(update={"run_id": name})

    # 打印派生信息（diff）
    try:
        parent = load_parent_config(from_run)
        diffs = config_diff(parent, new_config)
        typer.echo("=" * 60)
        typer.echo("  pars sft retry — 新 run 配置")
        typer.echo("=" * 60)
        typer.echo(f"  from         : {from_run}")
        typer.echo(f"  new_run_id   : {new_config.run_id}")
        typer.echo(f"  hypothesis   : {hypothesis}")
        if diffs:
            typer.echo(f"  变更字段（{len(diffs)} 项）：")
            for diff in diffs:
                typer.echo(f"    {diff['field']}: {diff['old']} → {diff['new']}")
        else:
            typer.echo("  变更字段：（无显式 override，仅 hypothesis 建议或全继承）")
        typer.echo("=" * 60)
    except Exception as exc:  # noqa: BLE001
        # diff 打印失败不应阻断 retry
        logger.warning("retry diff 打印失败（已忽略）", exc_info=exc)

    # 调用 start_retry 实际启动（使用已 derive 的 config 参数）
    orch = RunOrchestrator()
    training = new_config.training
    try:
        handle = orch.start(
            research_question=new_config.research_question,
            base_model=new_config.base_model,
            dataset_id=new_config.dataset.hf_id,
            dataset_split=new_config.dataset.split,
            n_samples=new_config.dataset.n_samples,
            lora_rank=training.lora_rank if training else 16,
            lora_alpha=training.lora_alpha if training else 32,
            lr=training.lr if training else 2e-4,
            epochs=training.epochs if training else 3,
            batch_size=training.batch_size if training else 2,
            max_seq_len=training.max_seq_len if training else 2048,
            eval_tasks=new_config.eval.tasks,
            usd_cap=new_config.budget.usd_cap,
            wall_clock_hours_cap=new_config.budget.wall_clock_hours_cap,
            gpu_hours_cap=new_config.budget.gpu_hours_cap,
            run_id=new_config.run_id,
        )
    except ApiKeyMissingError as exc:
        typer.echo(f"[ERROR] API key 缺失：{exc}", err=True)
        typer.echo("请先设置环境变量：export ANTHROPIC_API_KEY=sk-ant-...", err=True)
        raise typer.Exit(2) from exc
    except Exception as exc:
        exc_type = type(exc).__name__
        if exc_type == "ReadonlyFailsClosed":
            typer.echo(f"[ERROR] .claude/ fail-closed 保护触发（C21）：{exc}", err=True)
            raise typer.Exit(2) from exc
        logger.error("pars sft retry 未预期异常", exc_info=exc)
        typer.echo(f"[ERROR] 未预期错误：{exc}", err=True)
        raise typer.Exit(5) from exc

    # 打印运行结果
    _print_handle_result(handle)
    raise typer.Exit(handle.exit_code)


def _print_handle_result(handle) -> None:  # noqa: ANN001
    """打印 RunHandle 结果摘要。"""
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

        status_map = {0: "完成", 3: "超时(stuck)", 4: "预算超限", 5: "worker crash"}
        status = status_map.get(handle.exit_code, "未知")
        lines = [
            f"[bold]run_id[/bold]      : {handle.run_id}",
            f"[bold]final_state[/bold] : {handle.final_state}",
            f"[bold]exit_code[/bold]   : {handle.exit_code} ({status})",
        ]
        if handle.report_path:
            lines.append(f"[bold]report[/bold]      : {handle.report_path}")
        if handle.failure_reason:
            lines.append(f"[bold]reason[/bold]      : {handle.failure_reason}")

        rprint(Panel("\n".join(lines), title="pars sft retry 结果", expand=False))
    except ImportError:
        typer.echo(f"run_id={handle.run_id} exit_code={handle.exit_code}")
