"""
月度 review UI Router — T015 (R3 简化版)
结论: GET /reviews/monthly 路由，4 section 静态 markdown render
细节:
  - GET /reviews/monthly[?month=YYYY-MM]  → 月报全页（Jinja2 渲染）
  - set_monthly_review_service(svc): 测试 DI 入口
  - set_templates(templates): 测试 DI 入口
  - month 参数默认当前月份 (Asia/Taipei)
  - R3: 不调 LLM; 不渲染 PNG 图表; 不含 audience 参数
  - 副作用: 模块 import 时自动向 plugin registry 注册 router
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Any

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/reviews", tags=["reviews"])

# ── 全局依赖 (测试通过 set_* DI 函数注入) ─────────────────────────────────────

_monthly_review_svc: Any = None
_templates: Any = None


def set_monthly_review_service(svc: Any) -> None:
    """测试 DI 入口: 注入 MonthlyReviewService 实例。

    结论: 模块级注入，避免 FastAPI Depends 复杂性。
    """
    global _monthly_review_svc
    _monthly_review_svc = svc


def set_templates(templates: Any) -> None:
    """测试 DI 入口: 注入 Jinja2Templates 实例。"""
    global _templates
    _templates = templates


def _get_svc() -> Any:
    """获取当前服务实例，未初始化时 raise 500。"""
    if _monthly_review_svc is None:
        raise HTTPException(status_code=500, detail="MonthlyReviewService 未初始化")
    return _monthly_review_svc


def _get_templates() -> Jinja2Templates:
    """获取当前 templates，未初始化时使用 app 全局单例。"""
    if _templates is not None:
        return _templates  # type: ignore[no-any-return]
    from decision_ledger.ui.app import templates as app_templates

    return app_templates


def _current_month_id() -> str:
    """返回当前时间的月份字符串 (YYYY-MM, Asia/Taipei 时区)。

    结论: 与 monthly_scheduler 保持一致的时区逻辑。
    """
    try:
        from zoneinfo import ZoneInfo

        tz = ZoneInfo("Asia/Taipei")
    except Exception:
        import datetime as _dt

        tz = _dt.UTC  # type: ignore[assignment]
    now = datetime.now(tz=tz)
    return now.strftime("%Y-%m")


# ── Routes ───────────────────────────────────────────────────────────────────


@router.get("/monthly", response_class=HTMLResponse)
async def monthly_review_page(
    request: Request, month: str | None = None
) -> HTMLResponse:
    """GET /reviews/monthly[?month=YYYY-MM] — 渲染月度 review 全页。

    结论: 聚合月报数据后渲染 reviews/monthly.html 模板 (R3 4 section)。
    参数:
      month: 月份字符串 (e.g. "2026-04")，默认当前月。
    """
    month_id = month or _current_month_id()
    svc = _get_svc()

    try:
        review_data = await svc.generate(month_id=month_id)
    except Exception as exc:
        logger.error("月报生成失败 | month_id=%s | error=%s", month_id, exc)
        raise HTTPException(status_code=500, detail=f"月报生成失败: {exc}") from exc

    templates = _get_templates()
    return templates.TemplateResponse(
        "reviews/monthly.html",
        {
            "request": request,
            "review": review_data,
            "month_id": month_id,
        },
    )


# ── 注册到 plugin registry (模块导入副作用) ──────────────────────────────────
from decision_ledger.plugin import register_router  # noqa: E402

register_router(router)
