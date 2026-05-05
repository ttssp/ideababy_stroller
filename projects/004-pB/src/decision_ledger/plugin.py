"""
Plugin Registry — T001
结论: 提供 register_router / register_startup_task / register_scheduler_job 三个 hook
      后续 task 在自己模块顶部 import 并调用，不再修改 main.py
细节:
  - _routers: 待注册 APIRouter 列表
  - _startup_tasks: 启动时并发执行的协程工厂列表
  - _scheduler_jobs: APScheduler 任务描述列表
  - apply_to_app() 由 main.py 在 app 创建后调用一次
"""

from __future__ import annotations

from collections.abc import Callable, Coroutine
from dataclasses import dataclass, field
from typing import Any

from fastapi import APIRouter


@dataclass
class SchedulerJobSpec:
    """APScheduler 任务描述容器。"""

    func: Callable[..., Any]
    trigger: str  # "cron" | "interval" | "date"
    kwargs: dict[str, Any] = field(default_factory=dict)
    job_id: str = ""


# ── 内部状态（包私有，不 export）────────────────────────
_routers: list[APIRouter] = []
_startup_tasks: list[Callable[[], Coroutine[Any, Any, None]]] = []
_scheduler_jobs: list[SchedulerJobSpec] = []


def register_router(router: APIRouter) -> None:
    """结论: 后续 task 在模块顶层调用此函数注册路由，避免修改 main.py。

    用法示例 (在 ui/routes.py 顶部):
        from decision_ledger.plugin import register_router
        router = APIRouter(prefix="/decisions")
        ...
        register_router(router)  # 副作用注册
    """
    _routers.append(router)


def register_startup_task(coro_factory: Callable[[], Coroutine[Any, Any, None]]) -> None:
    """结论: 注册一个启动时运行的异步任务工厂（每次 app startup 调用一次）。

    参数 coro_factory: 无参数可调用，返回协程（async def）
    用法示例:
        async def start_telegram_bot() -> None: ...
        register_startup_task(start_telegram_bot)
    """
    _startup_tasks.append(coro_factory)


def register_scheduler_job(
    func: Callable[..., Any],
    trigger: str,
    job_id: str = "",
    **trigger_kwargs: Any,
) -> None:
    """结论: 注册 APScheduler cron/interval/date 任务，main.py 启动时统一添加。

    用法示例:
        register_scheduler_job(
            weekly_review_cron,
            "cron",
            job_id="weekly_review",
            day_of_week="sun",
            hour=21,
        )
    """
    _scheduler_jobs.append(
        SchedulerJobSpec(
            func=func,
            trigger=trigger,
            kwargs=trigger_kwargs,
            job_id=job_id or func.__name__,
        )
    )


def apply_to_app(app: Any) -> None:  # Any 避免循环 import FastAPI
    """结论: main.py 在 app 构建完成后调用，将所有注册项附加到 app。

    细节:
      - 包含路由 include
      - 包含 startup handler 注册
      - scheduler jobs 仅返回 spec list（T005/T010 实际添加）
    注意: 此函数只应在 main.py 调用一次。
    """
    for router in _routers:
        app.include_router(router)

    # startup_tasks 封装为 FastAPI lifespan 或 on_event
    # 由 main.py 的 lifespan 函数迭代执行
    # (T001 阶段不启动真实任务，只注册)


def get_startup_tasks() -> list[Callable[[], Coroutine[Any, Any, None]]]:
    """获取已注册的 startup task 工厂列表（供 main.py lifespan 调用）。"""
    return list(_startup_tasks)


def get_scheduler_jobs() -> list[SchedulerJobSpec]:
    """获取已注册的 scheduler job spec 列表（供 T010/T015 使用）。"""
    return list(_scheduler_jobs)
