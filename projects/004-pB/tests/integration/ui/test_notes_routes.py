"""
/notes 路由集成测试 — T016
结论: 验证 CRUD + search + dedup 提示的端到端行为
细节:
  - 使用 TestClient + fake NoteService (不需要真实 DB)
  - 验证 dedup 命中时 UI 显示提示文本
  - 验证搜索 (?q=keyword) 过滤结果
  - 验证 DELETE /notes/{id} 删除成功
"""

from __future__ import annotations

import hashlib
from datetime import datetime
from typing import Any
from unittest.mock import AsyncMock, MagicMock

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.testclient import TestClient
from pathlib import Path

from decision_ledger.domain.note import Note


# ── 辅助工厂 ─────────────────────────────────────────────────


def _make_note(
    note_id: str = "note-001",
    title: str = "P/E ratio 解析",
    content: str = "P/E 是市盈率，衡量股票估值",
    tags: list[str] | None = None,
) -> Note:
    if tags is None:
        tags = ["估值"]
    normalized = content.lower().strip()
    content_hash = hashlib.sha256(normalized.encode()).hexdigest()
    return Note(
        note_id=note_id,
        title=title,
        content=content,
        tags=tags,
        content_hash=content_hash,
        created_at=datetime(2026, 4, 27, 12, 0, 0),
        updated_at=datetime(2026, 4, 27, 12, 0, 0),
    )


def _make_fake_service(
    notes: list[Note] | None = None,
    dedup_result: tuple[Note, bool] | None = None,
    search_results: list[Note] | None = None,
) -> MagicMock:
    """构造 fake NoteService。"""
    from decision_ledger.services.note_service import NoteRef

    svc = MagicMock()

    _notes = notes or []
    svc.list_notes = AsyncMock(return_value=_notes)
    svc.get_note = AsyncMock(return_value=_notes[0] if _notes else None)

    if dedup_result is None:
        note = _make_note()
        dedup_result = (note, False)
    svc.create_note = AsyncMock(return_value=dedup_result)

    svc.update_note = AsyncMock(return_value=_notes[0] if _notes else None)
    svc.delete_note = AsyncMock(return_value=None)
    svc.search = AsyncMock(return_value=search_results or [])
    svc.list_summaries_for_topics = AsyncMock(return_value=[])

    return svc


def _make_app(svc: Any) -> FastAPI:
    """构造含 notes router 的 test FastAPI app。"""
    _UI_DIR = Path(__file__).parents[3] / "src" / "decision_ledger" / "ui"
    TEMPLATES_DIR = _UI_DIR / "templates"
    STATIC_DIR = _UI_DIR / "static"

    app = FastAPI()

    if STATIC_DIR.exists():
        app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

    app_templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

    from decision_ledger.ui import router_notes

    router_notes.set_note_service(svc)
    router_notes.set_templates(app_templates)

    app.include_router(router_notes.router)

    return app


# ── 路由存在性测试 ──────────────────────────────────────────


class TestNotesRoutes:
    """GET /notes 路由基础行为测试。"""

    def test_should_return_200_when_getting_notes_list(self) -> None:
        """结论: GET /notes 返回 200 + HTML。"""
        svc = _make_fake_service()
        app = _make_app(svc)
        client = TestClient(app, raise_server_exceptions=True)

        resp = client.get("/notes")

        assert resp.status_code == 200
        assert "text/html" in resp.headers.get("content-type", "")

    def test_should_show_note_titles_in_list(self) -> None:
        """结论: GET /notes 列表页包含笔记标题。"""
        notes = [_make_note(title="P/E ratio 解析")]
        svc = _make_fake_service(notes=notes)
        app = _make_app(svc)
        client = TestClient(app, raise_server_exceptions=True)

        resp = client.get("/notes")

        assert "P/E ratio 解析" in resp.text

    def test_should_return_200_when_getting_new_note_form(self) -> None:
        """结论: GET /notes/new 返回 200。"""
        svc = _make_fake_service()
        app = _make_app(svc)
        client = TestClient(app, raise_server_exceptions=True)

        resp = client.get("/notes/new")

        assert resp.status_code == 200
        assert "text/html" in resp.headers.get("content-type", "")

    def test_should_redirect_after_creating_note(self) -> None:
        """结论: POST /notes 成功后 302 到 /notes。"""
        note = _make_note()
        svc = _make_fake_service(dedup_result=(note, False))
        app = _make_app(svc)
        client = TestClient(app, raise_server_exceptions=True, follow_redirects=False)

        resp = client.post(
            "/notes",
            data={"title": "P/E ratio 解析", "content": "市盈率定义", "tags": "估值"},
        )

        assert resp.status_code in (302, 303)
        assert "/notes" in resp.headers.get("location", "")

    def test_should_show_dedup_hint_when_hash_collision(self) -> None:
        """结论: POST /notes 相同 hash 命中时 UI 重定向并带 dedup 参数。"""
        existing = _make_note(note_id="existing-001")
        svc = _make_fake_service(dedup_result=(existing, True))
        app = _make_app(svc)
        client = TestClient(app, raise_server_exceptions=True, follow_redirects=False)

        resp = client.post(
            "/notes",
            data={"title": "任意标题", "content": "P/E 是市盈率，衡量股票估值", "tags": ""},
        )

        # dedup 时应重定向到列表页带 dedup_hint 参数或到已有笔记编辑页
        assert resp.status_code in (302, 303)
        location = resp.headers.get("location", "")
        assert "dedup" in location or "existing-001" in location

    def test_should_return_search_results_when_q_provided(self) -> None:
        """结论: GET /notes?q=FOMC 调用 search 并显示结果。"""
        fomc_note = _make_note(title="FOMC 分点投票", content="联邦公开市场委员会")
        svc = _make_fake_service(search_results=[fomc_note])
        app = _make_app(svc)
        client = TestClient(app, raise_server_exceptions=True)

        resp = client.get("/notes?q=FOMC")

        assert resp.status_code == 200
        assert "FOMC 分点投票" in resp.text
        svc.search.assert_called_once_with(query="FOMC")

    def test_should_return_404_when_note_not_found_for_edit(self) -> None:
        """结论: GET /notes/{id}/edit 不存在时返回 404。"""
        svc = _make_fake_service()
        svc.get_note = AsyncMock(return_value=None)
        app = _make_app(svc)
        client = TestClient(app, raise_server_exceptions=False)

        resp = client.get("/notes/nonexistent/edit")

        assert resp.status_code == 404

    def test_should_return_200_when_editing_existing_note(self) -> None:
        """结论: GET /notes/{id}/edit 存在时返回 200 + 表单。"""
        note = _make_note(note_id="note-007")
        svc = _make_fake_service(notes=[note])
        svc.get_note = AsyncMock(return_value=note)
        app = _make_app(svc)
        client = TestClient(app, raise_server_exceptions=True)

        resp = client.get("/notes/note-007/edit")

        assert resp.status_code == 200
        assert "P/E ratio 解析" in resp.text

    def test_should_redirect_after_deleting_note(self) -> None:
        """结论: DELETE /notes/{id} (via POST form) 成功后 302 到 /notes。"""
        svc = _make_fake_service()
        app = _make_app(svc)
        client = TestClient(app, raise_server_exceptions=True, follow_redirects=False)

        resp = client.delete("/notes/note-001")

        assert resp.status_code in (302, 303)
        assert "/notes" in resp.headers.get("location", "")
        svc.delete_note.assert_called_once_with("note-001")

    def test_should_not_call_llm_in_any_route(self) -> None:
        """结论: /notes 路由不调 LLM (R3 cut 验证)。"""
        from unittest.mock import patch

        note = _make_note()
        svc = _make_fake_service(dedup_result=(note, False))
        app = _make_app(svc)
        client = TestClient(app, raise_server_exceptions=True, follow_redirects=False)

        with patch("anthropic.Anthropic") as mock_cls:
            client.get("/notes")
            client.post(
                "/notes",
                data={"title": "测试", "content": "内容", "tags": ""},
            )
            mock_cls.assert_not_called()
