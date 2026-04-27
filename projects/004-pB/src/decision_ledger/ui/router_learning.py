"""
学习检查 UI 路由 — T019 (R3 简化版)
结论: GET /learning, GET /learning/{quarter_id}, POST /learning/{quarter_id}/answer
细节:
  - GET  /learning → 列表页（最近 N 季历史 + 当前季入口 + 文档自查链接）
  - GET  /learning/{quarter_id} → 季度答题页（题目列表 + 答案表单）
  - POST /learning/{quarter_id}/answer → 保存 human 答案，跳 results
  - 评分由 scripts/grade_learning.py 跑（不在 web 路径调 LLM, R3 cut）
  - 不修改 main.py, 通过 register_router 注册
"""

from __future__ import annotations

import json

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.templating import Jinja2Templates

from decision_ledger.services.learning_check_service import LearningCheckService

router = APIRouter(prefix="/learning", tags=["learning"])

_service: LearningCheckService | None = None
_templates: Jinja2Templates | None = None


def set_learning_service(service: LearningCheckService) -> None:
    """DI 入口: 注入 LearningCheckService 实例。"""
    global _service
    _service = service


def set_templates(templates: Jinja2Templates) -> None:
    """DI 入口: 注入 Jinja2Templates。"""
    global _templates
    _templates = templates


def _get_service() -> LearningCheckService:
    if _service is None:
        raise HTTPException(status_code=500, detail="LearningCheckService 未初始化")
    return _service


def _get_templates() -> Jinja2Templates:
    if _templates is None:
        from decision_ledger.ui.app import templates as default_templates

        return default_templates
    return _templates


@router.get("", response_class=HTMLResponse)
async def list_quarters(request: Request) -> Response:
    """学习检查首页: 列表 + 文档自查链接。"""
    templates = _get_templates()
    return templates.TemplateResponse(
        request,
        "learning/index.html",
        {"request": request},
    )


@router.get("/{quarter_id}", response_class=HTMLResponse)
async def show_quarter(request: Request, quarter_id: str) -> Response:
    """季度答题页: 题目列表 + 答案表单 (若已答 / 已评分则展示 results)。"""
    service = _get_service()
    templates = _get_templates()
    quarter = await service.get_quarter(quarter_id)
    if quarter is None:
        raise HTTPException(status_code=404, detail=f"季度 {quarter_id} 不存在")

    questions = json.loads(quarter.get("questions_json", "[]"))
    answers = json.loads(quarter.get("answers_json", "{}"))
    scores = json.loads(quarter.get("scores_json", "{}"))
    finalized = bool(quarter.get("finalized", 0))

    if finalized and scores:
        avg = service.compute_average_score(scores)
        return templates.TemplateResponse(
            request,
            "learning/_results.html",
            {
                "request": request,
                "quarter_id": quarter_id,
                "questions": questions,
                "answers": answers,
                "scores": scores,
                "average_score": avg,
                "passing": service.is_passing(avg),
            },
        )

    return templates.TemplateResponse(
        request,
        "learning/quarter_form.html",
        {
            "request": request,
            "quarter_id": quarter_id,
            "questions": questions,
            "answers": answers,
        },
    )


@router.post("/{quarter_id}/answer")
async def submit_answers(request: Request, quarter_id: str) -> Response:
    """保存 human 答案。表单字段名 = concept_id (yaml 里定义的 id)。"""
    service = _get_service()
    quarter = await service.get_quarter(quarter_id)
    if quarter is None:
        raise HTTPException(status_code=404, detail=f"季度 {quarter_id} 不存在")

    form = await request.form()
    answers: dict[str, str] = {
        key: str(value) for key, value in form.items() if isinstance(value, str)
    }
    await service.save_answers(quarter_id, answers)

    return RedirectResponse(url=f"/learning/{quarter_id}", status_code=303)


# ── 注册到主 app (plugin registry 模式) ──
def _register() -> None:
    try:
        from decision_ledger.plugin import register_router

        register_router(router)
    except ImportError:
        pass


_register()
