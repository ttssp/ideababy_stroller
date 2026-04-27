"""
Settings UI Router — T012
结论: 提供关注股 watchlist + 持仓快照 holdings 的录入 UI，4 个路由
细节:
  - GET /settings/watchlist: 展示当前关注股列表 + CSV 粘贴区
  - POST /settings/watchlist: 接受 csv_text 表单字段，解析写入 DB
  - GET /settings/holdings: 展示当前最新持仓快照 + JSON 粘贴区
  - POST /settings/holdings: 接受 json_text 表单字段，解析写入 DB
  - create_settings_router(pool=... | pool_getter=...) 工厂函数
  - 模块副作用: 注册 router (import 期) + register_startup_task (lifespan 期 init pool)
校验规则:
  - ticker 自动 uppercase + dedupe（委托 portfolio_service）
  - 硬上限 100 条（超过 400/422 响应）
  - CSV BOM 自动去除

Codex review F1 修复: 原版本在 import 期 new AsyncConnectionPool 但永不 initialize,
production 调路由时 RuntimeError 被 handler `try/except` 静默吞 → 返回 200 + 空表,
用户感受不到坏。改成: import 期只注册 router + startup task; lifespan 期真 init pool;
handler 通过 pool_getter 拿 initialized pool, 未 init 时 503 (而非 200 + 空)。
"""

from __future__ import annotations

import logging
import uuid
from collections.abc import Callable
from datetime import UTC, datetime
from pathlib import Path

from fastapi import APIRouter, Form, HTTPException, Request
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


def create_settings_router(
    pool: AsyncConnectionPool | None = None,
    *,
    pool_getter: Callable[[], AsyncConnectionPool | None] | None = None,
) -> APIRouter:
    """创建 settings router 实例 (工厂函数, 测试可注入 migrated_pool)。

    参数:
        pool: AsyncConnectionPool 实例 (测试场景, 已 initialize)
        pool_getter: 延迟获取 pool 的 callable (production 场景, lifespan
            期才 initialize); 必须返回已 initialize 的 pool 或 None (未 ready)
    返回:
        配置好 4 个路由的 APIRouter 实例
    要求:
        pool / pool_getter 至少传一个; 同时传时 pool_getter 优先 (production 路径)。
    """
    if pool is None and pool_getter is None:
        raise ValueError(
            "create_settings_router 需要 pool 或 pool_getter 至少一个"
        )

    def _get_repo() -> PortfolioRepository:
        """每个 request 拿到当前 initialized 的 PortfolioRepository。

        F1 修复关键点: 通过 pool_getter 拿 lifespan 期 init 的 pool;
        若 pool 还没 init (lifespan 未跑) → 503 而非"静默 200 + 空表"。
        """
        active_pool = pool_getter() if pool_getter is not None else pool
        if active_pool is None:
            raise HTTPException(
                status_code=503,
                detail="settings 路由 pool 未初始化 (lifespan 未启动?)",
            )
        return PortfolioRepository(active_pool)

    router = APIRouter(prefix="/settings", tags=["settings"])

    # ── GET /settings/watchlist ──────────────────────────────────────────
    @router.get("/watchlist", response_class=HTMLResponse)
    async def get_watchlist_page(request: Request) -> HTMLResponse:
        """展示当前关注股列表 + CSV 粘贴区。

        结论: 从 DB 读取 watchlist，传给模板渲染。
        """
        repo = _get_repo()  # F1: lifespan 未起会 503, 不再静默 200 + 空表
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
        repo = _get_repo()  # F1: lifespan 未起会 503
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
        repo = _get_repo()  # F1: lifespan 未起会 503
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
        repo = _get_repo()  # F1: lifespan 未起会 503
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


# ── 模块副作用: import 期注册 router + startup task ────────────────────────────
# F1 修复 (Codex review):
# 原版本在 import 期 new pool 但永不 initialize, handler 触发时 RuntimeError 被
# `try/except Exception` 静默吞 → 200 + 空表。改为 import 期只注册 router,
# pool initialization 推到 lifespan 期的 startup task。

# Module-level holder, lifespan 期 startup task 写入 initialized pool;
# create_settings_router 通过 pool_getter closure 拿到当前值。
_pool_holder: dict[str, AsyncConnectionPool | None] = {"pool": None}


def _settings_pool_getter() -> AsyncConnectionPool | None:
    """供 router handler 拿当前 initialized pool; lifespan 未起则返回 None → 503。"""
    return _pool_holder["pool"]


def _resolve_settings_db_path() -> str:
    """从 Settings 解析 DB 路径; load_settings 失败时退回默认路径。"""
    try:
        from decision_ledger.config import load_settings
        settings = load_settings()
        return str(settings.decision_ledger_home / "data.sqlite")
    except Exception:
        return str(Path("~/decision_ledger/data.sqlite").expanduser())


async def _init_settings_pool() -> None:
    """startup task: lifespan 期初始化 settings router 用的 pool。

    F1 修复关键: pool.initialize() 必须在 async 上下文里跑, 不能在 import 期。
    init 失败不抑制 — 让 lifespan 看到错误, 而不是静默 noop 让 UI 永远空表。
    """
    if _pool_holder["pool"] is not None:
        # 已 init 过 (重复 startup 防御); 不重做
        return
    db_path = _resolve_settings_db_path()
    pool = AsyncConnectionPool(db_path)
    await pool.initialize()
    _pool_holder["pool"] = pool
    logger.info("settings router pool 已初始化 (db=%s)", db_path)


def _register_settings_router() -> None:
    """import 期注册 router + startup task (生产 main.py 无需修改)。"""
    try:
        from decision_ledger.plugin import register_router, register_startup_task

        # router 用 pool_getter 拿 lifespan 期 init 的 pool;
        # 未 init 时 handler 返回 503 (而非 200 + 空表)
        router = create_settings_router(pool_getter=_settings_pool_getter)
        register_router(router)
        register_startup_task(_init_settings_pool)
    except ImportError:
        pass
    except Exception:
        # logger.exception (不是 warning) — 让真错可见
        logger.exception("settings router 注册到 plugin registry 失败")


_register_settings_router()
