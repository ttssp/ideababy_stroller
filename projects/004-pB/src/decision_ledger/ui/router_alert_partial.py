"""
Alert banner partial Router — T020
结论: 接管 T004 base.html 的 hx-trigger="load, every 60s" /_partials/alert-banner endpoint
细节:
  - 无 active alert → 返回空字符串(HTMX 不渲染任何内容)
  - 有 active alert → 渲染 alert_banner_partial.html(R3 M2 + B-R2-4 仅 CLI/runbook)
  - 工厂函数 create_alert_partial_router 接受 alert_repo + templates 注入
"""

from __future__ import annotations

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, Response
from fastapi.templating import Jinja2Templates

from decision_ledger.repository.alert_repo import AlertRepository


def create_alert_partial_router(
    alert_repo: AlertRepository,
    templates: Jinja2Templates,
) -> APIRouter:
    """工厂函数:创建 alert partial 路由器。

    结论: 测试与生产用同一工厂注入(repo + templates)。
    """
    router = APIRouter(tags=["monitor"])

    @router.get("/_partials/alert-banner", response_class=HTMLResponse)
    async def alert_banner(request: Request) -> Response:
        """返回 alert banner partial(空内容 if no active alert)。

        结论: R3 M2 + B-R2-4 banner 仅显示 CLI 命令 + runbook 引用,
        不再有"点击降级 link" / 不再有 /settings/b-lite UI toggle。
        """
        active_alerts = await alert_repo.latest_active()
        if not active_alerts:
            return Response(content="", media_type="text/html")
        # 取最新一条 active alert 渲染
        alert = active_alerts[0]
        return templates.TemplateResponse(
            request,
            "monitor/alert_banner_partial.html",
            {"alert": alert},
        )

    return router
