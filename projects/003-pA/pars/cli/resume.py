"""
pars.cli.resume — pars sft resume 子命令实现（T019 · O3 · C13 · C22）。

结论：封装 resume 逻辑的 CLI 入口，调用 pars.orch.resume 的 can_resume /
      prepare_resume / execute_resume。
      can_resume 失败 → 退出码 2 + 友好提示；
      用户确认（或 --yes）后调用 execute_resume。

命令签名：
    pars sft resume --run-id <id> [--yes]

--yes 跳过交互确认（供测试和自动化脚本使用）。
"""

from __future__ import annotations

import typer

from pars.logging import get_logger

logger = get_logger(__name__)


def run_resume(run_id: str, yes: bool = False) -> None:
    """pars sft resume 的业务逻辑入口。

    参数：
        run_id : 要续跑的 run ID
        yes    : True → 跳过交互确认（--yes flag）

    副作用：
        - can_resume 失败 → typer.Exit(2)
        - execute_resume 未实现（T023）→ typer.Exit(1)
        - 成功 resume → typer.Exit(0)
    """
    from pars.orch.resume import can_resume, execute_resume, prepare_resume

    # --- 检查是否可以 resume ---
    ok, reason = can_resume(run_id)
    if not ok:
        typer.echo(f"[ERROR] 无法 resume run {run_id!r}: {reason}", err=True)
        logger.error(
            "pars sft resume 被拒绝",
            extra={"run_id": run_id, "reason": reason},
        )
        raise typer.Exit(2)

    # --- 打印 resume 计划，等待用户确认 ---
    plan = prepare_resume(run_id)
    typer.echo("=" * 60)
    typer.echo(f"  pars sft resume — 续跑计划")
    typer.echo("=" * 60)
    typer.echo(f"  run_id       : {plan['run_id']}")
    typer.echo(f"  current_phase: {plan['current_phase']}")
    typer.echo(f"  checkpoint   : {plan['checkpoint_path']}")
    typer.echo(f"  last_epoch   : {plan['last_epoch_completed']}")
    typer.echo(f"  usd_spent    : ${plan['usd_spent']:.4f}")
    typer.echo(f"  wall_clock   : {plan['wall_clock_elapsed_s']:.1f}s")
    typer.echo("=" * 60)

    if not yes:
        confirm = typer.confirm("确认续跑？(y/N)", default=False)
        if not confirm:
            typer.echo("已取消。", err=True)
            raise typer.Exit(0)

    # --- 执行 resume ---
    typer.echo(f"[INFO] 开始 resume run {run_id!r}...")
    logger.info("pars sft resume 开始执行", extra={"run_id": run_id})

    try:
        execute_resume(run_id)
    except NotImplementedError as exc:
        # T023 尚未实现 execute_resume 的 worktree 部分 → 友好提示
        typer.echo(
            f"[WARN] execute_resume 尚未完全实现（T023 负责 worktree+worker 部分）: {exc}",
            err=True,
        )
        logger.warning(
            "execute_resume NotImplementedError（T023 尚未实现）",
            exc_info=exc,
            extra={"run_id": run_id},
        )
        raise typer.Exit(1)
