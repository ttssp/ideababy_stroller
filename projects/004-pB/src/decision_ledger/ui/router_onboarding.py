"""
Onboarding UI Router — T021
结论: 7 步引导流程路由，首次启动检测 + 状态机推进 + 持久化到 onboarding_state 表
细节:
  - GET  /onboarding: 欢迎页 (welcome.html, 步骤 1)
  - GET  /onboarding/steps: 合并步骤页 (steps_combined.html, 步骤 2-7)
  - GET  /onboarding/done: 完成页 (done.html)
  - POST /onboarding/advance: 推进步骤 (current_step 表单字段) -> redirect
  - create_onboarding_router() 工厂函数
  - 首次启动检测: startup task 查询 onboarding_state.completed_at
    (通过 register_startup_task 注册, 不修改 main.py)
  - R2 H3: 不引用 T019 符号 (learning_check / LearningCheck)
    step 7 仅静态文案, 学习提醒走 T020 alert banner
"""

from __future__ import annotations

import logging

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse, Response

from decision_ledger.services.onboarding_service import OnboardingService
from decision_ledger.ui.app import templates

logger = logging.getLogger(__name__)

# ── 模块级 OnboardingService 实例 (内存态, 生产中持久化到 DB) ─────────────────
_svc: OnboardingService = OnboardingService()


def create_onboarding_router() -> APIRouter:
    """创建 onboarding router 实例（工厂函数，测试可直接调用）。

    结论: 使用模块级 _svc (内存态状态机); 生产环境可通过
    startup task 从 DB 恢复状态 (v0.1 简化: 仅内存态, 无跨进程持久化).
    """
    router = APIRouter(prefix="/onboarding", tags=["onboarding"])

    # ── GET /onboarding: 欢迎页 (步骤 1) ────────────────────────────────────
    @router.get("", response_class=HTMLResponse)
    @router.get("/", response_class=HTMLResponse)
    async def get_onboarding_welcome(request: Request) -> HTMLResponse:
        """展示 Onboarding 欢迎页（步骤 1 说明）。

        结论: 首次访问显示欢迎页; 已完成引导时仍可访问回顾。
        """
        return templates.TemplateResponse(
            request=request,
            name="onboarding/welcome.html",
            context={
                "active_tab": "onboarding",
                "steps": OnboardingService.STEPS,
                "current_step": _svc.current_step,
                "is_completed": _svc.is_completed(),
            },
        )

    # ── GET /onboarding/steps: 合并步骤页 (步骤 2-7) ────────────────────────
    @router.get("/steps", response_class=HTMLResponse)
    async def get_onboarding_steps(request: Request) -> HTMLResponse:
        """展示合并步骤页（步骤 2-7 single-page multi-section）。

        结论: 所有步骤在一个页面内，通过 anchor (#section-step-n) 跳转。
        """
        return templates.TemplateResponse(
            request=request,
            name="onboarding/steps_combined.html",
            context={
                "active_tab": "onboarding",
                "steps": OnboardingService.STEPS,
                "current_step": _svc.current_step,
                "is_completed": _svc.is_completed(),
            },
        )

    # ── GET /onboarding/done: 完成页 ────────────────────────────────────────
    @router.get("/done", response_class=HTMLResponse)
    async def get_onboarding_done(request: Request) -> HTMLResponse:
        """展示 Onboarding 完成确认页。

        结论: 显示耗时 + O6 pass 状态; 提供进入主界面链接。
        """
        total_s = _svc.total_duration_s()
        o6_pass = OnboardingService.check_o6_pass(total_s) if total_s is not None else False

        return templates.TemplateResponse(
            request=request,
            name="onboarding/done.html",
            context={
                "active_tab": "onboarding",
                "total_duration_s": total_s,
                "o6_pass": o6_pass,
                "is_completed": _svc.is_completed(),
            },
        )

    # ── POST /onboarding/advance: 推进步骤 ──────────────────────────────────
    @router.post("/advance", response_class=HTMLResponse)
    async def post_advance_step(
        request: Request,
        current_step: int = Form(default=1),
    ) -> Response:
        """推进 Onboarding 步骤并重定向。

        结论:
          - current_step 1 -> 2: redirect /onboarding/steps#section-step-2
          - current_step 2-6 -> n+1: redirect /onboarding/steps#section-step-{n+1}
          - current_step 7 -> done: redirect /onboarding/done
        细节:
          - 记录 leave_step(current_step) + enter_step(next_step) timestamp
          - step 7 完成后 mark_complete()
        """
        next_step = current_step + 1

        # 记录当前步骤离开
        await _svc.leave_step(current_step)

        if next_step > 7:
            # 所有步骤完成
            await _svc.mark_complete()
            logger.info(
                "Onboarding 完成: total_duration_s=%.1f, o6_pass=%s",
                _svc.total_duration_s() or 0.0,
                OnboardingService.check_o6_pass(_svc.total_duration_s() or 0.0),
            )
            return RedirectResponse(url="/onboarding/done", status_code=303)

        # 记录下一步进入
        await _svc.enter_step(next_step)

        if current_step == 1:
            # 步骤 1 完成 -> 进入 steps_combined 页
            return RedirectResponse(
                url=f"/onboarding/steps#section-step-{next_step}", status_code=303
            )
        else:
            return RedirectResponse(
                url=f"/onboarding/steps#section-step-{next_step}", status_code=303
            )

    return router


# ── 首次启动检测: startup task ───────────────────────────────────────────────

async def _onboarding_startup_check() -> None:
    """结论: app startup 时检查 onboarding_state.completed_at.

    细节:
      - 若 completed_at 为 NULL (未完成), 记录 warning 日志
        (真实 redirect 由前端 JS 或 middleware 处理, v0.1 简化)
      - 若已完成, 跳过
      - DB 查询失败时静默忽略 (onboarding 不应 block 主 app 启动)
    """
    try:
        from decision_ledger.config import load_settings
        from decision_ledger.repository.base import AsyncConnectionPool

        settings = load_settings()
        db_path = str(settings.decision_ledger_home / "data.sqlite")
        pool = AsyncConnectionPool(db_path=db_path)
        await pool.initialize()

        async with pool.connection() as conn:
            cursor = await conn.execute(
                "SELECT completed_at FROM onboarding_state WHERE id = 1 LIMIT 1"
            )
            row = await cursor.fetchone()

        if row is None or row[0] is None:
            logger.info(
                "Onboarding 未完成 — 请访问 http://localhost:8000/onboarding 完成配置引导"
            )
        else:
            logger.info("Onboarding 已完成 (completed_at=%s)", row[0])

    except Exception as exc:
        # 静默忽略: onboarding_state 表可能尚未创建 (alembic upgrade head 未跑)
        logger.debug("Onboarding startup check 忽略错误: %s", exc)


# ── 模块副作用: 注册到 plugin registry ──────────────────────────────────────

def _register_onboarding_router() -> None:
    """将 onboarding router 和 startup check 注册到全局 plugin registry。

    结论: main.py 无需修改，import decision_ledger.ui.router_onboarding 触发注册。
    """
    try:
        from decision_ledger.plugin import register_router, register_startup_task

        router = create_onboarding_router()
        register_router(router)
        register_startup_task(_onboarding_startup_check)
        logger.debug("onboarding router 已注册到 plugin registry")
    except ImportError:
        # 独立测试时跳过 plugin registry 注册
        pass
    except Exception:
        logger.warning("onboarding router 注册到 plugin registry 失败（忽略，测试时正常）")


_register_onboarding_router()
