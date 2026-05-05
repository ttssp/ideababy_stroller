"""
笔记 wiki UI Router — T016 (R3 简化版, 零 LLM)
结论: 6 个路由实现笔记 CRUD + 全文搜索 + dedup 提示
细节:
  - GET  /notes              → 笔记列表 (支持 ?q= 全文搜索)
  - GET  /notes/new          → 新建表单
  - POST /notes              → 创建笔记 (content_hash dedup 提示)
  - GET  /notes/{id}/edit    → 编辑表单
  - POST /notes/{id}/edit    → 更新笔记
  - DELETE /notes/{id}       → 删除笔记
  - set_note_service(svc): 测试 DI 入口
  - set_templates(tpl): 测试 DI 入口
  - R3: 路由内零 LLM 调用
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

# ── 注册到 plugin registry (不修改 main.py) ────────────────────────────────────
from decision_ledger.plugin import register_router

router = APIRouter(prefix="/notes", tags=["notes"])

# ── 全局 NoteService + Templates (测试通过 set_xxx 注入) ─────────────────────────
_note_service: Any = None
_templates: Jinja2Templates | None = None


def set_note_service(svc: Any) -> None:
    """测试 DI 入口: 注入 NoteService 实例。"""
    global _note_service
    _note_service = svc


def set_templates(tpl: Jinja2Templates) -> None:
    """测试 DI 入口: 注入 Jinja2Templates 实例。"""
    global _templates
    _templates = tpl


def _get_service() -> Any:
    """获取当前 NoteService, 未初始化时 raise 500。"""
    if _note_service is None:
        raise HTTPException(status_code=500, detail="NoteService 未初始化")
    return _note_service


def _get_templates() -> Jinja2Templates:
    """获取 Jinja2Templates, 优先用注入的, 否则用 app 模块默认。"""
    if _templates is not None:
        return _templates
    from decision_ledger.ui.app import templates

    return templates


# ── 路由实现 ──────────────────────────────────────────────────────────────────


@router.get("", response_class=HTMLResponse)
async def list_notes(
    request: Request,
    q: str | None = None,
) -> HTMLResponse:
    """GET /notes — 笔记列表 (支持 ?q= 全文搜索).

    结论: q 参数存在时调用 search(), 否则 list_notes(); 零 LLM.
    """
    svc = _get_service()
    tpl = _get_templates()

    if q:
        notes = await svc.search(query=q)
    else:
        notes = await svc.list_notes()

    return tpl.TemplateResponse(
        request,
        "notes/index.html",
        {
            "active_tab": "notes",
            "notes": notes,
            "query": q or "",
        },
    )


@router.get("/new", response_class=HTMLResponse)
async def new_note_form(request: Request) -> HTMLResponse:
    """GET /notes/new — 新建笔记表单。"""
    tpl = _get_templates()
    return tpl.TemplateResponse(
        request,
        "notes/edit.html",
        {
            "active_tab": "notes",
            "note": None,
            "is_new": True,
            "dedup_hint": False,
        },
    )


@router.post("")
async def create_note(
    request: Request,
    title: str = Form(...),
    content: str = Form(...),
    tags: str = Form(""),
) -> RedirectResponse:
    """POST /notes — 创建笔记, content_hash dedup 检查.

    结论:
      - dedup=False: 302 到 /notes
      - dedup=True: 302 到 /notes?dedup=1 或已有笔记编辑页
    R3: 零 LLM.
    """
    # 校验
    if not title.strip():
        raise HTTPException(status_code=422, detail="title 不能为空")
    if not content.strip():
        raise HTTPException(status_code=422, detail="content 不能为空")

    svc = _get_service()
    tag_list = [t.strip() for t in tags.split(",") if t.strip()]

    note, dedup = await svc.create_note(
        title=title.strip(),
        content=content,
        tags=tag_list,
    )

    if dedup:
        # R3: 仅 hash 命中提示, 重定向到已有笔记编辑页 + dedup 参数
        return RedirectResponse(
            url=f"/notes/{note.note_id}/edit?dedup=1",
            status_code=303,
        )

    return RedirectResponse(url="/notes", status_code=303)


@router.get("/{note_id}/edit", response_class=HTMLResponse)
async def edit_note_form(
    request: Request,
    note_id: str,
    dedup: str | None = None,
) -> HTMLResponse:
    """GET /notes/{id}/edit — 编辑表单.

    结论: dedup=1 时在表单顶部显示 hash 命中提示.
    """
    svc = _get_service()
    tpl = _get_templates()

    note = await svc.get_note(note_id)
    if note is None:
        raise HTTPException(status_code=404, detail=f"笔记 {note_id!r} 不存在")

    return tpl.TemplateResponse(
        request,
        "notes/edit.html",
        {
            "active_tab": "notes",
            "note": note,
            "is_new": False,
            "dedup_hint": dedup == "1",
        },
    )


@router.post("/{note_id}/edit")
async def update_note(
    request: Request,
    note_id: str,
    title: str = Form(...),
    content: str = Form(...),
    tags: str = Form(""),
) -> RedirectResponse:
    """POST /notes/{id}/edit — 更新笔记.

    结论: 更新成功后 302 到 /notes; 不存在时 404.
    """
    if not title.strip():
        raise HTTPException(status_code=422, detail="title 不能为空")
    if not content.strip():
        raise HTTPException(status_code=422, detail="content 不能为空")

    svc = _get_service()
    tag_list = [t.strip() for t in tags.split(",") if t.strip()]

    updated = await svc.update_note(
        note_id=note_id,
        title=title.strip(),
        content=content,
        tags=tag_list,
    )
    if updated is None:
        raise HTTPException(status_code=404, detail=f"笔记 {note_id!r} 不存在")

    return RedirectResponse(url="/notes", status_code=303)


@router.delete("/{note_id}")
async def delete_note(
    request: Request,
    note_id: str,
) -> RedirectResponse:
    """DELETE /notes/{id} — 删除笔记.

    结论: 删除后 302 到 /notes; R3 零 LLM.
    """
    svc = _get_service()
    await svc.delete_note(note_id)
    return RedirectResponse(url="/notes", status_code=303)


# ── 副作用: 注册 router 到 plugin registry (照搬 T010/T012 模式) ──────────────────
register_router(router)
