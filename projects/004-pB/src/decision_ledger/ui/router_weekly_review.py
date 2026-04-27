"""
weekly review UI Router — T014
结论: 周度 review 页面路由，含维护工时填报 HTMX 端点
细节:
  - GET /reviews/weekly[?week=YYYY-WW]  → 周报全页（Jinja2 渲染）
  - POST /reviews/weekly/maintenance    → HTMX 维护工时填报（返回 partial HTML）
  - set_weekly_review_service(svc): 测试 DI 入口
  - set_templates(templates): 测试 DI 入口
  - week 参数默认当前 ISO 周 (Asia/Taipei)
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Any

from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/reviews", tags=["reviews"])

# ── 全局依赖 (测试通过 set_* DI 函数注入) ─────────────────────────────────────

_weekly_review_svc: Any = None
_templates: Any = None


def set_weekly_review_service(svc: Any) -> None:
    """测试 DI 入口: 注入 WeeklyReviewService 实例。

    结论: 模块级注入，避免 FastAPI Depends 复杂性。
    """
    global _weekly_review_svc
    _weekly_review_svc = svc


def set_templates(templates: Any) -> None:
    """测试 DI 入口: 注入 Jinja2Templates 实例。"""
    global _templates
    _templates = templates


def _get_svc() -> Any:
    """获取当前服务实例，未初始化时 raise 500。"""
    if _weekly_review_svc is None:
        raise HTTPException(status_code=500, detail="WeeklyReviewService 未初始化")
    return _weekly_review_svc


def _get_templates() -> Jinja2Templates:
    """获取当前 templates，未初始化时使用 app 全局单例。"""
    if _templates is not None:
        return _templates  # type: ignore[no-any-return]
    from decision_ledger.ui.app import templates as app_templates

    return app_templates


def _current_week_id() -> str:
    """返回当前时间的 ISO 周号字符串 (YYYY-WW, Asia/Taipei 时区)。

    结论: 使用 scheduler 模块的同名逻辑，保持一致性。
    """
    try:
        from zoneinfo import ZoneInfo

        tz = ZoneInfo("Asia/Taipei")
    except Exception:
        import datetime as _dt

        tz = _dt.UTC  # type: ignore[assignment]
    now = datetime.now(tz=tz)
    return now.strftime("%G-W%V")


# ── Routes ───────────────────────────────────────────────────────────────────


@router.get("/weekly", response_class=HTMLResponse)
async def weekly_review_page(request: Request, week: str | None = None) -> HTMLResponse:
    """GET /reviews/weekly[?week=YYYY-WW] — 渲染周度 review 全页。

    结论: 聚合周报数据后渲染 reviews/weekly.html 模板。
    参数:
      week: ISO 周号字符串 (e.g. "2026-W17")，默认当前周。
    """
    week_id = week or _current_week_id()
    svc = _get_svc()

    try:
        review_data = await svc.generate(week_id=week_id)
    except Exception as exc:
        logger.error("周报生成失败 | week_id=%s | error=%s", week_id, exc)
        raise HTTPException(status_code=500, detail=f"周报生成失败: {exc}") from exc

    templates = _get_templates()
    return templates.TemplateResponse(
        "reviews/weekly.html",
        {
            "request": request,
            "review": review_data,
            "week_id": week_id,
        },
    )


@router.post("/weekly/maintenance", response_class=HTMLResponse)
async def log_maintenance_hours(
    request: Request,
    week_id: str = Form(...),
    hours: float = Form(...),
) -> HTMLResponse:
    """POST /reviews/weekly/maintenance — HTMX 维护工时填报端点。

    结论: 接收 HTMX 表单提交，写入工时后返回 partial HTML。
    参数 (form body):
      week_id: "YYYY-WW" 格式
      hours: 维护工时 (≥ 0.0)
    返回: _weekly_maintenance_partial.html (含更新后的维护摘要)
    """
    if hours < 0.0:
        raise HTTPException(status_code=422, detail="hours 不能为负数")

    svc = _get_svc()

    try:
        await svc.log_maintenance_hours(week_id=week_id, hours=hours)
        maintenance = (await svc.generate(week_id=week_id))["maintenance"]
    except Exception as exc:
        logger.error("维护工时填报失败 | week_id=%s | hours=%s | error=%s", week_id, hours, exc)
        raise HTTPException(status_code=500, detail=f"维护工时填报失败: {exc}") from exc

    templates = _get_templates()
    return templates.TemplateResponse(
        "reviews/_weekly_maintenance_partial.html",
        {
            "request": request,
            "week_id": week_id,
            "maintenance": maintenance,
        },
    )


# ── 注册到 plugin registry (模块导入副作用) ──────────────────────────────────
from decision_ledger.plugin import register_router  # noqa: E402

register_router(router)
