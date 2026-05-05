"""
decisions UI Router — T008
结论: 6 个路由实现双阶段决策录入 UI
细节:
  - GET  /decisions/new           → 草稿表单
  - POST /decisions/draft         → 创建草稿（含 LLM，5s timeout）
  - GET  /decisions/draft/{id}/preview → 预览（3列冲突报告 + commit 表单）
  - POST /decisions/{id}/commit   → 提交为正式 Decision（零 LLM）
  - GET  /decisions/{id}          → 查看已归档决策
  - GET  /decisions               → 决策列表
  - set_recorder(recorder): 测试 DI 入口
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from decision_ledger.domain.decision import Action
from decision_ledger.domain.env_snapshot import EnvSnapshot
from decision_ledger.ui.app import templates

router = APIRouter(prefix="/decisions", tags=["decisions"])

# ── 全局 DecisionRecorder 实例（测试通过 set_recorder 注入）──────────────────
_recorder: Any = None


def set_recorder(recorder: Any) -> None:
    """测试 DI 入口：注入 DecisionRecorder 实例。

    结论: 避免 FastAPI Depends 复杂性，直接模块级注入（测试 fixture 调用）。
    """
    global _recorder
    _recorder = recorder


def _get_recorder() -> Any:
    """获取当前 recorder，未初始化时 raise 500。"""
    if _recorder is None:
        raise HTTPException(status_code=500, detail="DecisionRecorder 未初始化")
    return _recorder


# ── 辅助：从环境构造 EnvSnapshot（简化版，实际由 market data 填充）────────────


def _make_env_snapshot_placeholder() -> EnvSnapshot:
    """构造测试/演示用 EnvSnapshot（实际生产中由 T010 market data 填充）。

    结论: T008 阶段使用占位值，T010 负责实际 market data 集成。
    """
    from datetime import UTC, datetime

    return EnvSnapshot(
        price=0.0,
        holdings_pct=0.0,
        holdings_abs=0.0,
        advisor_week_id="unknown",
        snapshot_at=datetime.now(tz=UTC),
    )


# ── 路由实现 ─────────────────────────────────────────────────────────────────


@router.get("/new", response_class=HTMLResponse)
async def new_form(request: Request) -> HTMLResponse:
    """GET /decisions/new — 显示草稿表单。"""
    return templates.TemplateResponse(
        request,
        "decisions/new.html",
        {
            "last_ticker": None,
            "last_action": None,
            "last_reason": None,
        },
    )


@router.post("/draft")
async def post_draft(
    request: Request,
    ticker: str = Form(...),
    intended_action: str = Form(...),
    draft_reason: str = Form(...),
) -> RedirectResponse:
    """POST /decisions/draft — 创建草稿，并行调用 LLM（5s timeout）。

    成功 → 302 到 /decisions/draft/{draft_id}/preview
    超时 → HTTPException(503)
    理由超长 → HTTPException(422)
    """
    # 校验理由长度（domain validator 也会检查，但这里提前 422）
    if len(draft_reason) > 80:
        raise HTTPException(
            status_code=422,
            detail=f"draft_reason 不能超过 80 字符，当前 {len(draft_reason)} 字符",
        )
    if not draft_reason.strip():
        raise HTTPException(status_code=422, detail="draft_reason 不能为空")

    # 校验 action
    try:
        action = Action(intended_action)
    except ValueError as err:
        raise HTTPException(
            status_code=422,
            detail=f"不合法的 intended_action: {intended_action!r}",
        ) from err

    recorder = _get_recorder()
    env_snapshot = _make_env_snapshot_placeholder()

    # create_draft 内部有 asyncio.timeout(5.0)，超时时 raise HTTPException(503)
    draft_id, _report, _rebuttal = await recorder.create_draft(
        ticker=ticker.strip().upper(),
        intended_action=action,
        draft_reason=draft_reason,
        env_snapshot=env_snapshot,
    )

    return RedirectResponse(
        url=f"/decisions/draft/{draft_id}/preview",
        status_code=303,
    )


@router.get("/draft/{draft_id}/preview", response_class=HTMLResponse)
async def preview_draft(request: Request, draft_id: str) -> HTMLResponse:
    """GET /decisions/draft/{draft_id}/preview — 三列冲突报告预览页。"""
    recorder = _get_recorder()

    # 查询 draft
    draft = await recorder._draft_repo.get(draft_id)
    if draft is None:
        raise HTTPException(status_code=404, detail=f"draft {draft_id!r} 不存在")

    # 查询 conflict_report 和 rebuttal
    if draft.conflict_report_ref is None or draft.devils_rebuttal_ref is None:
        raise HTTPException(
            status_code=422,
            detail="draft 的 refs 为 NULL，可能超时未完成",
        )

    report = await recorder._conflict_repo.get(draft.conflict_report_ref)
    rebuttal = await recorder._rebuttal_repo.get_for_decision(draft.devils_rebuttal_ref)

    if report is None or rebuttal is None:
        raise HTTPException(status_code=404, detail="冲突报告或反驳记录不存在")

    # 按 rendered_order_seed 随机化三列顺序
    signals = list(report.signals)
    seed = report.rendered_order_seed
    # 简单的确定性随机化：用 seed 做偏移
    offset = seed % len(signals)
    columns = signals[offset:] + signals[:offset]

    return templates.TemplateResponse(
        request,
        "decisions/draft_preview.html",
        {
            "draft": draft,
            "report": report,
            "rebuttal": rebuttal,
            "columns": columns,
        },
    )


@router.post("/{draft_id}/commit")
async def commit_draft(
    request: Request,
    draft_id: str,
    final_action: str = Form(...),
    final_reason: str = Form(...),
    would_have_acted_without_agent: str | None = Form(None),
) -> RedirectResponse:
    """POST /decisions/{draft_id}/commit — 零 LLM，提交为正式 Decision。

    成功 → 302 到 /decisions/{trade_id}
    缺少 would_have_acted → 422
    draft 不存在 → 404
    重复 commit → 409
    """
    # R2 M1: would_have_acted 强制 yes/no
    if would_have_acted_without_agent is None:
        raise HTTPException(
            status_code=422,
            detail="would_have_acted_without_agent 不能为空 (R2 M1)",
        )
    value_lower = would_have_acted_without_agent.strip().lower()
    if value_lower not in ("yes", "no", "true", "false", "1", "0"):
        raise HTTPException(
            status_code=422,
            detail=f"would_have_acted_without_agent 值不合法: {would_have_acted_without_agent!r}",
        )
    acted = value_lower in ("yes", "true", "1")

    # 校验 final_reason 长度
    if len(final_reason) > 80:
        raise HTTPException(
            status_code=422,
            detail=f"final_reason 不能超过 80 字符，当前 {len(final_reason)} 字符",
        )
    if not final_reason.strip():
        raise HTTPException(status_code=422, detail="final_reason 不能为空")

    # 校验 final_action
    try:
        action = Action(final_action)
    except ValueError as err:
        raise HTTPException(
            status_code=422,
            detail=f"不合法的 final_action: {final_action!r}",
        ) from err

    recorder = _get_recorder()

    # commit_draft 零 LLM（§9.1 不变量）
    trade_id = await recorder.commit_draft(
        draft_id=draft_id,
        final_action=action,
        final_reason=final_reason,
        would_have_acted_without_agent=acted,
    )

    return RedirectResponse(
        url=f"/decisions/{trade_id}",
        status_code=303,
    )


@router.get("/{trade_id}", response_class=HTMLResponse)
async def show_decision(request: Request, trade_id: str) -> HTMLResponse:
    """GET /decisions/{trade_id} — 查看已归档决策。"""
    recorder = _get_recorder()

    decision = await recorder._decision_repo.get(trade_id)
    if decision is None:
        raise HTTPException(status_code=404, detail=f"决策 {trade_id!r} 不存在")

    return templates.TemplateResponse(
        request,
        "decisions/show.html",
        {"decision": decision},
    )


@router.get("", response_class=HTMLResponse)
async def list_decisions(request: Request) -> HTMLResponse:
    """GET /decisions — 决策列表，含 hold + wait (D2/R11)。"""
    recorder = _get_recorder()

    # 聚合所有 actions（含 hold + wait）
    all_decisions: list[Any] = []
    for action in ("buy", "sell", "hold", "wait"):
        decisions = await recorder._decision_repo.list_by_action(action)
        all_decisions.extend(decisions)

    # 按时间倒序
    all_decisions.sort(key=lambda d: d.pre_commit_at, reverse=True)

    return templates.TemplateResponse(
        request,
        "decisions/list.html",
        {"decisions": all_decisions},
    )
