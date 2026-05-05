"""
Matrix UI Router — T011 (R3 简化版)
结论: GET /matrix 路由，渲染错位矩阵 HTML table（纯 Pico CSS，无颜色/无图表库）
细节:
  - GET /matrix              → 错位矩阵主页（完整 HTML）
  - MatrixService 在路由内部实例化（无状态，无 DB 依赖）
  - D16 红线: 不引用 plotly/matplotlib/d3.js/chart.js
  - R3 真砍: 不计算错位强度，不按错位排序，ticker 字母序
  - 副作用: 模块 import 时自动向 plugin registry 注册 router
  - 测试通过 patch("decision_ledger.ui.router_matrix.MatrixService") 注入 mock
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, Response
from fastapi.templating import Jinja2Templates

from decision_ledger.services.matrix_service import MatrixService

router = APIRouter(prefix="/matrix", tags=["matrix"])

# ── 全局 templates（测试通过 set_templates DI 注入）────────────────────────────
_templates: Any = None


def set_templates(templates: Any) -> None:
    """测试 DI 入口: 注入 Jinja2Templates 实例。

    结论: 测试场景注入自定义 templates；生产场景使用 app.py 全局单例。
    """
    global _templates
    _templates = templates


def _get_templates() -> Jinja2Templates:
    """获取当前 templates，未初始化时使用 app 全局单例。"""
    if _templates is not None:
        return _templates  # type: ignore[no-any-return]
    from decision_ledger.ui.app import templates as app_templates

    return app_templates


# ── 路由实现 ─────────────────────────────────────────────────────────────────


@router.get("", response_class=HTMLResponse)
async def matrix_page(request: Request) -> Response:
    """GET /matrix — 错位矩阵主页。

    结论: 展示所有 watchlist ticker 的三路 signals 方向 score 与持仓 %。
    细节:
      - R3: 无颜色 class，无错位强度排序，ticker 字母序
      - D16: 纯 HTML table，无图表库
      - MatrixService 由路由内部实例化（无 DB 依赖，外部传入数据）
      - 当前 R3 版本使用 mock watchlist（无真实 DB）；后续 task 接管数据层
    """
    tpl = _get_templates()

    # ── 数据获取（R3: 使用 mock watchlist + 空 signals + 空持仓）────────────
    # 后续 task（T015+）负责真实数据注入，T011 仅交付渲染结构
    tickers = _get_mock_watchlist()
    signals_by_ticker: dict[str, list[Any]] = {}
    holdings_pct: dict[str, float] = {}

    svc = MatrixService()
    rows = svc.build(
        tickers=tickers,
        signals_by_ticker=signals_by_ticker,
        holdings_pct=holdings_pct,
    )

    return tpl.TemplateResponse(
        request,
        "matrix/index.html",
        {
            "active_tab": "matrix",
            "rows": rows,
        },
    )


# ── 辅助函数 ─────────────────────────────────────────────────────────────────


def _get_mock_watchlist() -> list[str]:
    """结论: R3 mock watchlist，30 个 ticker 供 UI 渲染验证用。

    细节: 真实 watchlist 来源由后续 task 接管 (T015+)。
    """
    return sorted([
        "AAPL", "AMZN", "BABA", "BIDU", "BYND",
        "CSCO", "DELL", "DIS",  "EA",   "EBAY",
        "FB",   "GOOG", "GRAB", "HD",   "IBM",
        "INTC", "JD",   "JPM",  "KO",   "LULU",
        "META", "MSFT", "NFLX", "NVDA", "ORCL",
        "PEP",  "QCOM", "SBUX", "SHOP", "TSLA",
    ])


# ── 副作用: 向 plugin registry 注册 matrix router ───────────────────────────
# 结论: import decision_ledger.ui.router_matrix 触发时自动注册到主 app
def _register_to_plugin_registry() -> None:
    """将 matrix router 注册到全局 plugin registry（供 main.py apply_to_app 使用）。"""
    try:
        from decision_ledger.plugin import register_router

        register_router(router)
    except ImportError:
        # 独立测试时 (create_app 直接 include_router) 不需要 plugin registry
        pass


_register_to_plugin_registry()
