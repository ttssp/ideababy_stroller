"""
pars.cli.main — Typer CLI 入口（T005 骨架占位）。

结论：定义顶层 app + sft 子命令组，所有子命令均为占位（后续 task 填充实现）。
不引入任何真实业务逻辑；后续 task 直接往函数体内填肉即可。

命令结构：
    pars --version / --help
    pars sft start   (T023 实现)
    pars sft status  (T023/T024 实现)
    pars sft retry   (T024 实现)
    pars sft report  (T024 实现)
    pars sft compare (T025 实现)
    pars sft resume  (T023 实现)
    pars unlock      (T017 实现，C18 stuck_lock 清除路径)

实现注意（Typer 0.12 兼容性）：
    Typer 0.12 的 is_eager=True bool 参数在 callback 中存在类型传递 bug，
    导致 --version 无法正常工作。解决方案：
    1. app.callback() 中不定义 --version 参数
    2. 模块末尾通过 typer.main.get_command(app) 获取底层 click Group
    3. 向 click Group 直接注入 click.Option --version（绕过 Typer 参数处理）
    4. 导出 cli 变量（预构建的 click Group），供测试和 entry point 使用
"""

from __future__ import annotations

from typing import Annotated, Optional

import click
import typer
from typer.main import get_command

import pars
from pars.logging import configure_root, get_logger

# ---------------------------------------------------------------------------
# Logger（module 级）
# ---------------------------------------------------------------------------

logger = get_logger(__name__)

# ---------------------------------------------------------------------------
# Typer app 实例
# ---------------------------------------------------------------------------

app = typer.Typer(
    name="pars",
    help="RecallKit v0.1 · 单人后训练决策循环（LoRA SFT + eval + 决策报告）",
    add_completion=False,  # 避免自动注册 completion 子命令
    no_args_is_help=True,  # 无参数时打印 help
    invoke_without_command=True,  # 允许 callback 接管（处理 --version）
)

# sft 子命令组
sft = typer.Typer(
    name="sft",
    help="SFT 训练子命令（start / status / retry / report / compare / resume）",
    no_args_is_help=True,
)
app.add_typer(sft, name="sft")


# ---------------------------------------------------------------------------
# 全局 callback：启动时初始化 logger
# 注意：--version 不在此定义（见模块末尾 _build_cli 注释）
# ---------------------------------------------------------------------------

@app.callback()
def _global_callback(ctx: typer.Context) -> None:
    """RecallKit CLI 全局入口。

    初始化 logging；所有子命令均依赖此 callback 完成初始化。
    --version 由模块末尾注入到 click Group（绕过 Typer 0.12 bug）。
    """
    configure_root()


# ---------------------------------------------------------------------------
# pars sft start（T023 实现，委托给 pars.cli.start 模块）
# ---------------------------------------------------------------------------

from pars.cli.start import start as _start_impl

sft.command("start")(_start_impl)


# ---------------------------------------------------------------------------
# pars sft status
# ---------------------------------------------------------------------------

@sft.command("status")
def sft_status(
    run_id: Annotated[
        Optional[str],
        typer.Option("--run-id", "-r", help="指定 run ID（默认显示最近一个 run）"),
    ] = None,
) -> None:
    """查询 SFT run 的当前状态（训练进度 / stuck 状态 / 已用预算）。"""
    from pars.cli.status import run_status
    run_status(run_id)


# ---------------------------------------------------------------------------
# pars sft retry
# ---------------------------------------------------------------------------

@sft.command("retry")
def sft_retry(
    from_run: Annotated[
        str,
        typer.Option("--from", help="基于哪个 run ID 创建新实验（继承 config，允许覆盖）"),
    ],
    hypothesis: Annotated[
        Optional[str],
        typer.Option("--hypothesis", help="新实验假设（覆盖原 run 假设）"),
    ] = None,
) -> None:
    """基于已有 run 创建新实验（调整超参数后重跑）。

    TODO: T024 实现 retry 逻辑（fork config + new run）。
    """
    logger.warning("T024 will implement pars sft retry")
    typer.echo("T024 will implement: pars sft retry（基于已有 run 创建新实验）", err=True)
    raise typer.Exit(1)


# ---------------------------------------------------------------------------
# pars sft report
# ---------------------------------------------------------------------------

@sft.command("report")
def sft_report(
    run_id: Annotated[
        str,
        typer.Option("--run-id", "-r", help="要生成报告的 run ID"),
    ],
) -> None:
    """为指定 run 生成 markdown 决策报告（含训练曲线 + 分数对比 + 失败归因）。

    TODO: T024 实现报告渲染逻辑。
    """
    logger.warning("T024 will implement pars sft report")
    typer.echo("T024 will implement: pars sft report（生成 markdown 决策报告）", err=True)
    raise typer.Exit(1)


# ---------------------------------------------------------------------------
# pars sft compare
# ---------------------------------------------------------------------------

@sft.command("compare")
def sft_compare(
    run_id_a: Annotated[
        str,
        typer.Argument(help="第一个 run ID"),
    ],
    run_id_b: Annotated[
        str,
        typer.Argument(help="第二个 run ID"),
    ],
) -> None:
    """对比两个 run 的 config / metric / 结论差异，输出 markdown 差异表。

    TODO: T025 实现 compare 逻辑（O6 验证目标）。
    """
    logger.warning("T025 will implement pars sft compare")
    typer.echo("T025 will implement: pars sft compare（跨 run 差异对比）", err=True)
    raise typer.Exit(1)


# ---------------------------------------------------------------------------
# pars sft resume
# ---------------------------------------------------------------------------

@sft.command("resume")
def sft_resume(
    run_id: Annotated[
        str,
        typer.Option("--run-id", "-r", help="要续跑的 run ID"),
    ],
    yes: Annotated[
        bool,
        typer.Option("--yes", "-y", help="跳过交互确认（供测试和自动化脚本使用）"),
    ] = False,
) -> None:
    """从 checkpoint 续跑中断的 SFT run（仅限同机重启，C22）。

    检查流程：
    1. 确认 run 未完成（非 completed/failed 终态）
    2. 确认 checkpoint 目录非空
    3. 确认 stuck_lock 不存在（否则提示 pars unlock）
    4. 机器指纹比对（C22）：GPU/CUDA/os_major hard reject；python/os patch 仅 warning
    """
    from pars.cli.resume import run_resume
    run_resume(run_id=run_id, yes=yes)


# ---------------------------------------------------------------------------
# pars unlock（顶层命令，C18 stuck_lock 清除路径）
# ---------------------------------------------------------------------------

@app.command("unlock")
def cmd_unlock(
    run_id: Annotated[
        str,
        typer.Option("--run-id", "-r", help="要解锁的 run ID（清除 stuck_lock 文件）"),
    ],
) -> None:
    """手动清除指定 run 的 stuck_lock 文件（适用于 stuck 状态机误判场景）。

    C18：人工干预路径 — 确认不是真 stuck 后，执行 pars unlock 解除熔断锁。
    流程：
    1. 检查 stuck_lock 是否存在；若不存在，报告并退出非零（无锁可清）
    2. 清除 stuck_lock 文件
    3. 重置 state.json.needs_human_review=False
    4. 打印确认信息，退出 0
    """
    from pars.stuck.stuck_lock import clear_stuck_lock, has_stuck_lock
    from pars.ledger.state import update_state

    if not has_stuck_lock(run_id=run_id):
        typer.echo(
            f"[ERROR] run={run_id} 无 stuck_lock 文件（已解锁或 run_id 有误）",
            err=True,
        )
        raise typer.Exit(2)

    # 清除 stuck_lock 文件
    clear_stuck_lock(run_id=run_id)

    # 重置 state.json.needs_human_review = False
    try:
        update_state(run_id, needs_human_review=False, stuck_restart_count=0)
    except Exception as exc:
        logger.warning(
            "cmd_unlock: 更新 state.json 失败（stuck_lock 已清除）",
            exc_info=exc,
            extra={"run_id": run_id},
        )

    typer.echo(f"[OK] run={run_id} stuck_lock 已清除，可重新提交任务。")
    logger.info("pars unlock 成功", extra={"run_id": run_id})


# ---------------------------------------------------------------------------
# 预构建 click Group（绕过 Typer 0.12 is_eager bool 参数 bug）
#
# 原因：Typer 0.12 中 is_eager=True 的 bool Option 在 callback 函数体中接收到
# 的值为字符串 'False' 或 None，而非 bool。直接操作底层 click.Group.params
# 注入 click.Option 可绕过 Typer 的参数处理层，确保 --version 行为正确。
#
# 注意：typer.testing.CliRunner.invoke() 每次重新调用 _get_command(app)，
# 导致此处注入无效。测试应使用 click.testing.CliRunner 调用 cli 变量。
# ---------------------------------------------------------------------------

def _version_callback(ctx: click.Context, param: click.Parameter, value: bool) -> None:
    """--version click 回调：打印版本号后退出。"""
    if value:
        click.echo(f"pars {pars.__version__}")
        ctx.exit(0)


def _build_cli() -> click.Group:
    """将 Typer app 转换为 click Group，并注入 --version option。

    返回：
        注入了 --version 参数的 click.Group 实例
    """
    grp = get_command(app)
    grp.params.insert(
        0,
        click.Option(
            ["--version", "-V"],
            is_flag=True,
            is_eager=True,
            expose_value=False,
            callback=_version_callback,
            help="显示版本号后退出",
        ),
    )
    return grp  # type: ignore[return-value]


# cli：预构建的 click Group，供测试和 entry point 使用
cli: click.Group = _build_cli()


# ---------------------------------------------------------------------------
# CLI 独立运行入口
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    cli()
