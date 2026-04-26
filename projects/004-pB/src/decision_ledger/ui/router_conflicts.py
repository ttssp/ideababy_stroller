"""
conflicts UI Router — T010
结论: 三列冲突报告 UI，中立显示三路信号（R10 红线: 无 winner/priority/recommended）
细节:
  - GET /conflicts                   → 冲突报告列表
  - GET /conflicts/{report_id}       → 冲突报告详情（三列布局）
  - GET /conflicts/by-decision/{trade_id} → 按决策查找冲突报告
  - set_conflict_repo(repo): 测试 DI 入口（模仿 router_decisions.py 模式）
  - set_templates(templates): 测试 DI 入口（允许测试注入自定义模板引擎）
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse, Response
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/conflicts", tags=["conflicts"])

# ── 全局依赖（测试通过 set_* DI 函数注入）────────────────────────────────────

_conflict_repo: Any = None
_templates: Any = None


def set_conflict_repo(repo: Any) -> None:
    """测试 DI 入口: 注入 ConflictRepository 实例。

    结论: 避免 FastAPI Depends 复杂性，直接模块级注入（测试 fixture 调用）。
    """
    global _conflict_repo
    _conflict_repo = repo


def set_templates(templates: Any) -> None:
    """测试 DI 入口: 注入 Jinja2Templates 实例。

    结论: 测试场景可注入自定义 templates，生产场景使用 app.py 全局单例。
    """
    global _templates
    _templates = templates


def _get_conflict_repo() -> Any:
    """获取当前 repo，未初始化时 raise 500。"""
    if _conflict_repo is None:
        # 尝试使用生产 repo（测试中应通过 set_conflict_repo 设置）
        raise HTTPException(status_code=500, detail="ConflictRepository 未初始化")
    return _conflict_repo


def _get_templates() -> Jinja2Templates:
    """获取当前 templates,未初始化时使用 app 全局单例。"""
    if _templates is not None:
        return _templates  # type: ignore[no-any-return]
    from decision_ledger.ui.app import templates as app_templates
    return app_templates


# ── 路由实现 ─────────────────────────────────────────────────────────────────


@router.get("", response_class=HTMLResponse)
async def list_conflicts(request: Request) -> Response:
    """GET /conflicts — 冲突报告列表页。

    结论: 展示最近的 ConflictReport，无 winner 偏向（R10 红线）。
    """
    repo = _get_conflict_repo()
    tpl = _get_templates()

    reports = await repo.list_recent(limit=20)

    return tpl.TemplateResponse(
        request,
        "conflicts/index.html",
        {
            "reports": reports,
        },
    )


@router.get("/by-decision/{trade_id}", response_class=HTMLResponse)
async def conflict_by_decision(request: Request, trade_id: str) -> Response:
    """GET /conflicts/by-decision/{trade_id} — 按决策 ID 查找冲突报告。

    结论: HTMX partial，供 decisions 详情页嵌入使用。
    细节: 注意此路由必须在 /conflicts/{report_id} 之前注册，否则 'by-decision' 会被当作 report_id。
    """
    repo = _get_conflict_repo()
    tpl = _get_templates()

    # 通过 trade_id 查找关联的 conflict report
    # 注: 当前 ConflictRepository 未实现 get_by_decision，返回 404 当 trade_id 不存在
    # 后续 T014+ 可扩展 repo 支持 decision → conflict_report 关联查询
    report = None
    if hasattr(repo, "get_by_decision"):
        report = await repo.get_by_decision(trade_id)

    if report is None:
        raise HTTPException(
            status_code=404,
            detail=f"未找到决策 '{trade_id}' 关联的冲突报告",
        )

    return tpl.TemplateResponse(
        request,
        "conflicts/detail.html",
        {
            "report": report,
            "report_id": trade_id,
        },
    )


@router.get("/{report_id}", response_class=HTMLResponse)
async def conflict_detail(request: Request, report_id: str) -> Response:
    """GET /conflicts/{report_id} — 冲突报告详情页（三列布局）。

    结论: 渲染三列信号视图，无 winner/priority/recommended（R10 红线）。
    细节:
      - rendered_order_seed 决定三列显示顺序
      - has_divergence=False 时渲染空态 _empty_state.html
    """
    repo = _get_conflict_repo()
    tpl = _get_templates()

    report = await repo.get(report_id)
    if report is None:
        raise HTTPException(
            status_code=404,
            detail=f"冲突报告 '{report_id}' 不存在",
        )

    # 按 rendered_order_seed 排列 signals 顺序（R2 D22）
    ordered_signals = _order_signals_by_seed(report)

    return tpl.TemplateResponse(
        request,
        "conflicts/detail.html",
        {
            "report": report,
            "report_id": report_id,
            "ordered_signals": ordered_signals,
        },
    )


# ── 辅助函数 ─────────────────────────────────────────────────────────────────


def _order_signals_by_seed(report: Any) -> list[Any]:
    """结论: 根据 rendered_order_seed 对 signals 排序（R2 D22 UI 随机化）。

    细节:
      - seed % 6 对应 3! = 6 种排列
      - 使用 itertools.permutations 生成全部排列，取 seed 对应的那个
      - 若 signals 少于 3 条则直接返回原序（不应发生，不变量 #2）
    """
    from itertools import permutations

    signals = list(report.signals)
    if len(signals) < 3:
        return signals

    # 只取前 3 个（不变量 #2 保证 ≥ 3）
    first_three = signals[:3]
    remaining = signals[3:]

    all_perms = list(permutations(first_three))
    perm_index = report.rendered_order_seed % len(all_perms)
    ordered_first_three = list(all_perms[perm_index])

    return ordered_first_three + remaining
