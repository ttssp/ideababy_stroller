"""
post-mortem 回填 UI 路由 — T018
结论: GET/POST /decisions/{trade_id}/post-mortem，支持 4 字段回填 + 时间约束校验
细节:
  - GET  /decisions/{trade_id}/post-mortem → 渲染回填表单（若已回填预填数据）
  - POST /decisions/{trade_id}/post-mortem → 校验 + 入库，成功 303 → show 页
  - _now_override 表单参数: 测试注入"现在时间"（production 永远留空）
  - 不修改 main.py，通过 register_router 注册（T018 模式）
  - R11: hold/wait 决策 executed_at 留空允许
  - R3: 无自动 nudge（v0.2+）
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Annotated, Any

from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from decision_ledger.services.post_mortem_service import (
    PostMortemService,
    PostMortemValidationError,
)
from decision_ledger.ui.app import templates

router = APIRouter(prefix="/decisions", tags=["post_mortem"])

# ── 全局 DecisionRepository（测试通过 set_decision_repo 注入）────────────────
_decision_repo: Any = None
_pm_service: PostMortemService = PostMortemService()


def set_decision_repo(repo: Any) -> None:
    """测试 DI 入口：注入 DecisionRepository 实例。

    结论: 与 T008 相同的模块级注入模式，避免 FastAPI Depends 复杂性。
    """
    global _decision_repo
    _decision_repo = repo


def _get_decision_repo() -> Any:
    """获取当前 repo，未初始化时 raise 500。"""
    if _decision_repo is None:
        raise HTTPException(status_code=500, detail="DecisionRepository 未初始化")
    return _decision_repo


# ── 路由实现 ─────────────────────────────────────────────────────────────────


@router.get("/{trade_id}/post-mortem", response_class=HTMLResponse)
async def get_post_mortem_form(request: Request, trade_id: str) -> HTMLResponse:
    """GET /decisions/{trade_id}/post-mortem — 渲染 post-mortem 回填表单。

    结论: 若已回填过，预填已有数据；若未回填，字段为空。
    """
    repo = _get_decision_repo()
    decision = await repo.get(trade_id)
    if decision is None:
        raise HTTPException(status_code=404, detail=f"决策 {trade_id!r} 不存在")

    # 预填已有 post_mortem 数据
    existing_pm = decision.post_mortem

    return templates.TemplateResponse(
        request,
        "decisions/post_mortem.html",
        {
            "decision": decision,
            "existing_pm": existing_pm,
        },
    )


@router.post("/{trade_id}/post-mortem")
async def post_post_mortem(
    request: Request,
    trade_id: str,
    executed_at: str = Form(default=""),
    result_pct_after_7d: str = Form(default=""),
    result_pct_after_30d: str = Form(default=""),
    retrospective_notes: str = Form(default=""),
    now_override: Annotated[str, Form(alias="_now_override")] = "",  # 仅测试用，注入当前时间
) -> RedirectResponse:
    """POST /decisions/{trade_id}/post-mortem — 校验 + 入库 post-mortem。

    成功: 303 → /decisions/{trade_id}
    决策不存在: 404
    校验失败: 422

    注意:
      now_override (表单字段名 _now_override) 为测试专用字段，生产场景留空则默认 datetime.now(UTC)。
    """
    repo = _get_decision_repo()
    decision = await repo.get(trade_id)
    if decision is None:
        raise HTTPException(status_code=404, detail=f"决策 {trade_id!r} 不存在")

    # 解析字段
    executed_at_dt: datetime | None = None
    if executed_at.strip():
        try:
            executed_at_dt = _parse_datetime_field(executed_at.strip())
        except ValueError:
            raise HTTPException(
                status_code=422,
                detail=f"executed_at 格式不合法: {executed_at!r}，期望 YYYY-MM-DDTHH:MM",
            ) from None

    result_7d: float | None = None
    if result_pct_after_7d.strip():
        try:
            result_7d = float(result_pct_after_7d.strip())
        except ValueError:
            raise HTTPException(
                status_code=422,
                detail=f"result_pct_after_7d 必须是数字: {result_pct_after_7d!r}",
            ) from None

    result_30d: float | None = None
    if result_pct_after_30d.strip():
        try:
            result_30d = float(result_pct_after_30d.strip())
        except ValueError:
            raise HTTPException(
                status_code=422,
                detail=f"result_pct_after_30d 必须是数字: {result_pct_after_30d!r}",
            ) from None

    notes: str | None = retrospective_notes.strip() if retrospective_notes.strip() else None

    # 解析注入时间（测试专用）
    now_dt: datetime | None = None
    if now_override.strip():
        try:
            now_dt = datetime.fromisoformat(now_override.strip())
            if now_dt.tzinfo is None:
                now_dt = now_dt.replace(tzinfo=UTC)
        except ValueError:
            pass  # 忽略无效的 override，使用真实时间

    # 校验时间约束
    try:
        _pm_service.validate(
            pre_commit_at=decision.pre_commit_at,
            executed_at=executed_at_dt,
            result_pct_after_7d=result_7d,
            result_pct_after_30d=result_30d,
            retrospective_notes=notes,
            now=now_dt,
        )
    except PostMortemValidationError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    # 构造 PostMortem 并写入 DB
    from decision_ledger.domain.decision import PostMortem

    pm = PostMortem(
        executed_at=executed_at_dt,
        result_pct_after_7d=result_7d,
        result_pct_after_30d=result_30d,
        retrospective_notes=notes,
    )

    await repo.update_post_mortem(trade_id, pm)

    return RedirectResponse(
        url=f"/decisions/{trade_id}",
        status_code=303,
    )


# ── 私有辅助 ─────────────────────────────────────────────────────────────────


def _parse_datetime_field(value: str) -> datetime:
    """解析表单中的 datetime 字段（接受 ISO 格式和 datetime-local 格式）。

    结论: HTML datetime-local input 产出格式为 YYYY-MM-DDTHH:MM，
          也接受完整 ISO 格式（含时区）。
    """
    # 先尝试完整 ISO 格式（含时区）
    try:
        dt = datetime.fromisoformat(value)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=UTC)
        return dt
    except ValueError:
        pass
    # 尝试 datetime-local 格式（无时区）
    for fmt in ("%Y-%m-%dT%H:%M", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M"):
        try:
            dt = datetime.strptime(value, fmt)
            return dt.replace(tzinfo=UTC)
        except ValueError:
            continue
    raise ValueError(f"无法解析 datetime: {value!r}")


# ── 注册到主 app（plugin registry 模式）──────────────────────────────────────
def _register() -> None:
    """将 post_mortem router 注册到全局 plugin registry。"""
    try:
        from decision_ledger.plugin import register_router

        register_router(router)
    except ImportError:
        pass


_register()
