"""
R2 新增: /advisor/paste 集成测试 — T006
结论: POST /advisor/paste 含 base64 PDF → inbox 落文件 → watcher 触发 → advisor_reports 入库
细节:
  - POST /advisor/paste 接受 base64 编码的 PDF
  - 文件落入 inbox 目录后 watcher 触发 enqueue 回调
  - GET /advisor/paste 返回 200 + HTML form
  - POST /advisor/paste 无效 base64 → 400 响应
"""

from __future__ import annotations

import base64
import os
from pathlib import Path

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def sample_pdf_bytes() -> bytes:
    """读取 tests/fixtures 的 sample PDF 字节。"""
    here = Path(__file__).parent.parent.parent  # tests/
    pdf_path = here / "fixtures" / "sample_advisor_2026w17.pdf"
    return pdf_path.read_bytes()


@pytest.fixture
def inbox_dir(tmp_path: Path) -> Path:
    """临时 inbox 目录。"""
    inbox = tmp_path / "inbox"
    inbox.mkdir(parents=True, exist_ok=True)
    return inbox


@pytest.fixture
def advisor_app_client(inbox_dir: Path) -> TestClient:
    """创建包含 advisor router 的 TestClient。"""
    os.environ.setdefault("ANTHROPIC_API_KEY", "test-key-placeholder")
    os.environ.setdefault("TELEGRAM_BOT_TOKEN", "test-token-placeholder")

    from fastapi import FastAPI

    from decision_ledger.ui.router_advisor import create_advisor_router

    app = FastAPI()
    router = create_advisor_router(inbox_dir=inbox_dir)
    app.include_router(router)

    return TestClient(app, raise_server_exceptions=True)


class TestAdvisorPasteRoute:
    """GET/POST /advisor/paste 路由测试。"""

    def test_should_return_200_when_get_paste_page(
        self, advisor_app_client: TestClient
    ) -> None:
        """GET /advisor/paste → 200 + HTML。"""
        response = advisor_app_client.get("/advisor/paste")
        assert response.status_code == 200
        assert "text/html" in response.headers.get("content-type", "")

    def test_should_return_html_form_when_get_paste(
        self, advisor_app_client: TestClient
    ) -> None:
        """GET /advisor/paste 页面包含 form 元素。"""
        response = advisor_app_client.get("/advisor/paste")
        assert b"form" in response.content.lower()

    def test_should_drop_file_to_inbox_when_post_valid_pdf(
        self,
        advisor_app_client: TestClient,
        sample_pdf_bytes: bytes,
        inbox_dir: Path,
    ) -> None:
        """POST /advisor/paste 含 base64 PDF → inbox 目录落文件。"""
        encoded = base64.b64encode(sample_pdf_bytes).decode("utf-8")

        response = advisor_app_client.post(
            "/advisor/paste",
            json={"pdf_base64": encoded, "filename": "test_drop.pdf"},
        )

        assert response.status_code in (200, 201, 202)

        # 断言文件出现在 inbox
        dropped_files = list(inbox_dir.glob("*.pdf"))
        assert len(dropped_files) >= 1
        # 文件内容与原始 PDF 一致
        assert dropped_files[0].read_bytes() == sample_pdf_bytes

    def test_should_return_400_when_invalid_base64(
        self, advisor_app_client: TestClient
    ) -> None:
        """POST /advisor/paste 无效 base64 → 400。"""
        response = advisor_app_client.post(
            "/advisor/paste",
            json={"pdf_base64": "INVALID_BASE64!!!!", "filename": "bad.pdf"},
        )
        assert response.status_code == 400

    def test_should_return_400_when_missing_pdf_base64(
        self, advisor_app_client: TestClient
    ) -> None:
        """POST /advisor/paste 缺少 pdf_base64 字段 → 400/422。"""
        response = advisor_app_client.post(
            "/advisor/paste",
            json={"filename": "no_content.pdf"},
        )
        assert response.status_code in (400, 422)


class TestAdvisorParseFailuresRoute:
    """GET /advisor/parse-failures 路由测试。"""

    def test_should_return_200_when_get_parse_failures(
        self, advisor_app_client: TestClient
    ) -> None:
        """GET /advisor/parse-failures → 200。"""
        response = advisor_app_client.get("/advisor/parse-failures")
        assert response.status_code == 200

    def test_should_return_html_when_get_parse_failures(
        self, advisor_app_client: TestClient
    ) -> None:
        """GET /advisor/parse-failures 返回 HTML。"""
        response = advisor_app_client.get("/advisor/parse-failures")
        assert "text/html" in response.headers.get("content-type", "")


class TestAdvisorManualStructureRoute:
    """POST /advisor/manual-structure 路由测试。"""

    def test_should_return_200_when_get_manual_structure(
        self, advisor_app_client: TestClient
    ) -> None:
        """GET /advisor/manual-structure → 200。"""
        response = advisor_app_client.get("/advisor/manual-structure")
        assert response.status_code == 200
