"""
rebuttals UI Router — T013
结论: HTMX partial GET /decisions/{trade_id}/rebuttal
细节:
  - R2 修订: 不再是 poll 路径 (draft 阶段已同步生成); 仅服务于
    draft preview 页 + success 页面 partial 渲染
  - 返回 _rebuttal_partial.html HTMX partial
  - compliance §4.3: 模板含 '反方意见仅供考虑' 免责声明
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse

from decision_ledger.ui.app import templates

router = APIRouter(prefix="/decisions", tags=["rebuttals"])

# ── 全局 repo 实例（测试通过 set_rebuttal_repo 注入）────────────────────────
_rebuttal_repo: Any = None


def set_rebuttal_repo(repo: Any) -> None:
    """测试 DI 入口: 注入 RebuttalRepository 实例。

    结论: 避免 FastAPI Depends 复杂性，直接模块级注入（测试 fixture 调用）。
    """
    global _rebuttal_repo
    _rebuttal_repo = repo


def _get_rebuttal_repo() -> Any:
    """获取当前 repo，未初始化时 raise 500。"""
    if _rebuttal_repo is None:
        raise HTTPException(status_code=500, detail="RebuttalRepository 未初始化")
    return _rebuttal_repo


# ── 路由实现 ─────────────────────────────────────────────────────────────────


@router.get("/{trade_id}/rebuttal", response_class=HTMLResponse)
async def get_rebuttal_partial(request: Request, trade_id: str) -> HTMLResponse:
    """GET /decisions/{trade_id}/rebuttal — HTMX rebuttal partial 渲染。

    R2 修订: 不再是 poll (draft 阶段已同步生成)。
    用途: draft preview 页 + decision success 页面嵌入 rebuttal 展示。
    compliance §4.3: 模板含 '反方意见仅供考虑' 免责声明。
    """
    repo = _get_rebuttal_repo()

    rebuttal = await repo.get_for_decision(trade_id)
    if rebuttal is None:
        raise HTTPException(
            status_code=404,
            detail=f"rebuttal for trade_id={trade_id!r} 不存在",
        )

    return templates.TemplateResponse(
        request,
        "decisions/_rebuttal_partial.html",
        {"rebuttal": rebuttal, "trade_id": trade_id},
    )
