"""
Settings UI Router — T012
结论: 提供关注股 watchlist + 持仓快照 holdings 的录入 UI，4 个路由
细节:
  - GET /settings/watchlist: 展示当前关注股列表 + CSV 粘贴区
  - POST /settings/watchlist: 接受 csv_text 表单字段，解析写入 DB
  - GET /settings/holdings: 展示当前最新持仓快照 + JSON 粘贴区
  - POST /settings/holdings: 接受 json_text 表单字段，解析写入 DB
  - create_settings_router(pool) 工厂函数，测试注入 migrated_pool
  - 模块副作用: 注册到 plugin registry
校验规则:
  - ticker 自动 uppercase + dedupe（委托 portfolio_service）
  - 硬上限 100 条（超过 400/422 响应）
  - CSV BOM 自动去除
"""

from __future__ import annotations

import logging
import uuid
from datetime import UTC, datetime
from pathlib import Path

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse, Response

from decision_ledger.domain.portfolio import Holding, HoldingsSnapshot, Market, Watchlist
from decision_ledger.repository.base import AsyncConnectionPool
from decision_ledger.repository.portfolio_repo import PortfolioRepository
from decision_ledger.services.portfolio_service import (
    PortfolioServiceError,
    parse_holdings_json,
    parse_watchlist_csv,
)
from decision_ledger.ui.app import templates

logger = logging.getLogger(__name__)


def create_settings_router(pool: AsyncConnectionPool) -> APIRouter:
    """创建 settings router 实例（工厂函数，测试可注入 migrated_pool）。

    参数:
        pool: AsyncConnectionPool 实例（真实 DB 或测试 DB 均可）
    返回:
        配置好 4 个路由的 APIRouter 实例
    """
    router = APIRouter(prefix="/settings", tags=["settings"])
    repo = PortfolioRepository(pool)

    # ── GET /settings/watchlist ──────────────────────────────────────────
    @router.get("/watchlist", response_class=HTMLResponse)
    async def get_watchlist_page(request: Request) -> HTMLResponse:
        """展示当前关注股列表 + CSV 粘贴区。

        结论: 从 DB 读取 watchlist，传给模板渲染。
        """
        try:
            watchlist = await repo.get_watchlist()
        except Exception:
            logger.exception("读取 watchlist 失败")
            watchlist = []

        return templates.TemplateResponse(
            request=request,
            name="settings/watchlist.html",
            context={
                "active_tab": "settings",
                "watchlist": watchlist,
                "error_message": "",
                "success": False,
            },
        )

    # ── POST /settings/watchlist ─────────────────────────────────────────
    @router.post("/watchlist", response_class=HTMLResponse)
    async def post_watchlist(
        request: Request,
        csv_text: str = Form(default=""),
    ) -> Response:
        """接受 CSV 文本，解析写入 watchlist 表。

        结论:
          - csv_text 字段含 ticker,sector,note 三列（sector/note 可省）
          - 硬上限 100 → 400 响应
          - 写入成功后重定向回 GET（PRG 模式）
        细节:
          - ticker → DB Watchlist.market 默认 US（CSV 无 market 列，v0.1 简化）
          - sector 存为 display_name 前缀（v0.1 简化，不单独存 sector 列）
        """
        # 解析 CSV
        try:
            rows = parse_watchlist_csv(csv_text)
        except PortfolioServiceError as exc:
            logger.warning("watchlist CSV 解析失败: %s", exc)
            # 重新渲染带错误提示的页面（不重定向）
            try:
                watchlist = await repo.get_watchlist()
            except Exception:
                watchlist = []
            return templates.TemplateResponse(
                request=request,
                name="settings/watchlist.html",
                context={
                    "active_tab": "settings",
                    "watchlist": watchlist,
                    "error_message": str(exc),
                    "success": False,
                },
                status_code=400,
            )

        # 构造 Watchlist 域模型列表
        watchlist_items = [
            Watchlist(
                ticker=row["ticker"],
                market=Market.US,  # v0.1: 默认 US，CSV 无 market 列
                display_name=row.get("sector") or None,
            )
            for row in rows
        ]

        # 写入 DB（原子替换）
        try:
            await repo.replace_watchlist(watchlist_items)
        except Exception as exc:
            logger.exception("写入 watchlist 失败: %s", exc)
            try:
                watchlist = await repo.get_watchlist()
            except Exception:
                watchlist = []
            return templates.TemplateResponse(
                request=request,
                name="settings/watchlist.html",
                context={
                    "active_tab": "settings",
                    "watchlist": watchlist,
                    "error_message": f"数据库写入失败: {exc}",
                    "success": False,
                },
                status_code=500,
            )

        logger.info("watchlist 已更新，共 %d 条", len(watchlist_items))
        # PRG: Post-Redirect-Get
        return RedirectResponse(url="/settings/watchlist", status_code=303)

    # ── GET /settings/holdings ───────────────────────────────────────────
    @router.get("/holdings", response_class=HTMLResponse)
    async def get_holdings_page(request: Request) -> HTMLResponse:
        """展示当前最新持仓快照 + JSON 粘贴区。

        结论: 从 DB 读取最新 snapshot，传给模板渲染。
        """
        try:
            snapshot = await repo.latest_snapshot()
        except Exception:
            logger.exception("读取持仓快照失败")
            snapshot = None

        return templates.TemplateResponse(
            request=request,
            name="settings/holdings.html",
            context={
                "active_tab": "settings",
                "snapshot": snapshot,
                "error_message": "",
                "success": False,
            },
        )

    # ── POST /settings/holdings ──────────────────────────────────────────
    @router.post("/holdings", response_class=HTMLResponse)
    async def post_holdings(
        request: Request,
        json_text: str = Form(default=""),
    ) -> Response:
        """接受 JSON 文本，解析写入 holdings snapshot。

        结论:
          - json_text 字段含 [{ticker, qty, cost_basis?},...] 格式
          - 硬上限 100 → 400 响应
          - 写入成功后重定向回 GET（PRG 模式）
        细节:
          - qty → Holding.quantity
          - cost_basis → Holding.avg_cost (均价成本, v0.1 简化)
        """
        # 解析 JSON
        try:
            holdings_data = parse_holdings_json(json_text)
        except PortfolioServiceError as exc:
            logger.warning("holdings JSON 解析失败: %s", exc)
            try:
                snapshot = await repo.latest_snapshot()
            except Exception:
                snapshot = None
            return templates.TemplateResponse(
                request=request,
                name="settings/holdings.html",
                context={
                    "active_tab": "settings",
                    "snapshot": snapshot,
                    "error_message": str(exc),
                    "success": False,
                },
                status_code=400,
            )

        # 构造 Holding 域模型列表
        holdings = [
            Holding(
                ticker=item["ticker"],  # type: ignore[arg-type]
                market=Market.US,       # v0.1: 默认 US
                quantity=float(item["qty"]),  # type: ignore[arg-type]
                avg_cost=float(item["cost_basis"]) if item.get("cost_basis") is not None else None,  # type: ignore[arg-type]
            )
            for item in holdings_data
        ]

        # 构造 HoldingsSnapshot
        snapshot = HoldingsSnapshot(
            snapshot_id=f"hs_{uuid.uuid4().hex[:12]}",
            holdings=holdings,
            snapshot_at=datetime.now(tz=UTC),
        )

        # 写入 DB
        try:
            await repo.upsert_holding_snapshot(snapshot)
        except Exception as exc:
            logger.exception("写入持仓快照失败: %s", exc)
            try:
                latest = await repo.latest_snapshot()
            except Exception:
                latest = None
            return templates.TemplateResponse(
                request=request,
                name="settings/holdings.html",
                context={
                    "active_tab": "settings",
                    "snapshot": latest,
                    "error_message": f"数据库写入失败: {exc}",
                    "success": False,
                },
                status_code=500,
            )

        logger.info("持仓快照已写入，共 %d 条持仓", len(holdings))
        # PRG: Post-Redirect-Get
        return RedirectResponse(url="/settings/holdings", status_code=303)

    return router


# ── 模块副作用: 注册到 plugin registry ──────────────────────────────────────
def _register_settings_router() -> None:
    """将 settings router 注册到全局 plugin registry（生产 main.py 无需修改）。"""
    try:
        from decision_ledger.config import load_settings
        from decision_ledger.plugin import register_router
        from decision_ledger.repository.base import AsyncConnectionPool

        try:
            settings = load_settings()
            db_path = str(settings.decision_ledger_home / "data.sqlite")
        except Exception:
            db_path = str(Path("~/decision_ledger/data.sqlite").expanduser())

        pool = AsyncConnectionPool(db_path)
        router = create_settings_router(pool=pool)
        register_router(router)
    except ImportError:
        pass
    except Exception:
        logger.warning("settings router 注册到 plugin registry 失败（忽略，测试时正常）")


_register_settings_router()
