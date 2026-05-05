"""
Shell Router — T004
结论: 提供 GET / (首页) 和 GET /_partials/alert-banner (T020 接管前返回空) 两个端点
细节:
  - GET / 渲染 index.html，含项目说明 + 跳转决策档案链接
  - GET /_partials/alert-banner T004 阶段返回空 HTML (无激活告警)，T020 接管后返回真 banner partial
  - 不接管其他 tab 路由 (T008/T010/T011/T012/T014/T015/T016/T019/T020 各自接管)
"""

from __future__ import annotations

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from decision_ledger.ui.app import templates

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    """首页 — 项目说明 + 决策档案入口。

    结论: 渲染 index.html，nav 高亮"决策档案"（OP-6 mitigation: 主场景首页）。
    """
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "active_tab": "decisions",  # 首页默认高亮决策档案
        },
    )


@router.get("/_partials/alert-banner", response_class=HTMLResponse)
async def alert_banner_partial(request: Request) -> HTMLResponse:
    """Alert Banner Partial — T004 阶段返回空 (T020 接管后返回真 banner)。

    结论: HTMX 轮询此 endpoint (base.html 中 hx-trigger="load, every 60s")。
          T004 阶段无激活告警，返回 200 空内容。
    """
    return templates.TemplateResponse(
        request=request,
        name="_empty_alert_banner.html",
        context={},
    )
