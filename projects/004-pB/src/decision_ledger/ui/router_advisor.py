"""
Advisor UI Router — T006
结论: 提供咨询师 pipeline 的 3 个 Web UI 路由
细节:
  - GET /advisor/parse-failures: 列出解析失败记录 (TECH-3 fallback)
  - GET/POST /advisor/manual-structure: 手工录入结构化 JSON
  - GET /advisor/paste (R2 新增): fallback PDF 上传 UI
  - POST /advisor/paste (R2 新增): 接受 base64 PDF → 写入 inbox → 触发 watcher
  - create_advisor_router(inbox_dir) 工厂函数，供测试注入临时 inbox_dir
  - 模块副作用: 注册到 plugin registry (main.py 无需修改)
"""

from __future__ import annotations

import base64
import binascii
import logging
from pathlib import Path

from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel

from decision_ledger.ui.app import templates

logger = logging.getLogger(__name__)


class PasteRequest(BaseModel):
    """POST /advisor/paste 请求体 schema。"""

    pdf_base64: str
    filename: str = "advisor_upload.pdf"


def create_advisor_router(inbox_dir: Path | None = None) -> APIRouter:
    """
    创建 advisor router 实例（工厂函数，测试可注入临时 inbox_dir）。

    参数:
        inbox_dir: PDF 写入目标目录；None 时从 config 加载（生产路径）
    """
    router = APIRouter(prefix="/advisor", tags=["advisor"])

    def _get_inbox_dir() -> Path:
        """获取 inbox 目录：测试时用注入值，生产时从 config 读取。"""
        if inbox_dir is not None:
            return inbox_dir
        # 生产路径: 从 config.decision_ledger_home / "inbox" 读取
        from decision_ledger.config import load_settings

        try:
            settings = load_settings()
            return settings.decision_ledger_home / "inbox"
        except Exception:
            # 配置加载失败时 fallback 到默认路径
            return Path("~/decision_ledger/inbox").expanduser()

    # ── GET /advisor/parse-failures ─────────────────────────────────────
    @router.get("/parse-failures", response_class=HTMLResponse)
    async def parse_failures_page(request: Request) -> HTMLResponse:
        """
        列出 PDF 解析失败记录 (TECH-3 fallback UI)。

        结论: v0.1 从 alerts 表读取 parse_failure 记录，展示给 human 手工处理。
        细节: T006 阶段无 DB 连接注入（T003 repo 未串联到路由），先展示空列表。
              T014/T015 接管后才真正从 DB 读取。
        """
        return templates.TemplateResponse(
            request=request,
            name="advisor/parse_failures.html",
            context={
                "active_tab": "advisor",
                "failures": [],  # TODO(T014): 从 AdvisorRepository 读取
            },
        )

    # ── GET /advisor/manual-structure ────────────────────────────────────
    @router.get("/manual-structure", response_class=HTMLResponse)
    async def manual_structure_page(
        request: Request,
        failure_id: str = "",
        pdf_path: str = "",
    ) -> HTMLResponse:
        """手工录入结构化 JSON 页面 (TECH-3 fallback)。"""
        return templates.TemplateResponse(
            request=request,
            name="advisor/manual_structure.html",
            context={
                "active_tab": "advisor",
                "failure_id": failure_id,
                "pdf_path": pdf_path,
                "advisor_id": "",
                "week_id": "",
                "raw_summary": "",
                "structured_json": "",
                "error_message": "",
                "success": False,
            },
        )

    # ── POST /advisor/manual-structure ───────────────────────────────────
    @router.post("/manual-structure", response_class=HTMLResponse)
    async def manual_structure_submit(
        request: Request,
        failure_id: str = Form(default=""),
        pdf_path: str = Form(default=""),
        advisor_id: str = Form(...),
        week_id: str = Form(...),
        raw_summary: str = Form(default=""),
        structured_json: str = Form(...),
    ) -> HTMLResponse:
        """
        接受手工录入的结构化 JSON，入库。

        结论: v0.1 仅 echo 回表单（DB 写入路径由 T014 补全）。
        """
        # TODO(T014): 解析 structured_json → upsert_weekly
        return templates.TemplateResponse(
            request=request,
            name="advisor/manual_structure.html",
            context={
                "active_tab": "advisor",
                "failure_id": failure_id,
                "pdf_path": pdf_path,
                "advisor_id": advisor_id,
                "week_id": week_id,
                "raw_summary": raw_summary,
                "structured_json": structured_json,
                "error_message": "",
                "success": True,
            },
        )

    # ── GET /advisor/paste (R2 新增) ──────────────────────────────────────
    @router.get("/paste", response_class=HTMLResponse)
    async def paste_page(request: Request) -> HTMLResponse:
        """R2 新增: fallback PDF 上传 UI。"""
        return templates.TemplateResponse(
            request=request,
            name="advisor/paste.html",
            context={
                "active_tab": "advisor",
            },
        )

    # ── POST /advisor/paste (R2 新增) ─────────────────────────────────────
    @router.post("/paste")
    async def paste_pdf(payload: PasteRequest) -> JSONResponse:
        """
        R2 新增: 接受 base64 PDF → 写入 inbox → watcher 触发同 pipeline。

        结论:
          - 校验 base64 合法性 → 400 on invalid
          - 解码 → 写入 _get_inbox_dir() / filename
          - watcher 轮询检测到新文件后自动触发解析
        """
        # 校验 base64
        try:
            pdf_bytes = base64.b64decode(payload.pdf_base64, validate=True)
        except (binascii.Error, ValueError) as exc:
            logger.warning("POST /advisor/paste: 无效 base64: %s", exc)
            raise HTTPException(status_code=400, detail=f"无效的 base64 编码: {exc}") from exc

        # 安全文件名（防止路径穿越）
        safe_filename = Path(payload.filename).name
        if not safe_filename.lower().endswith(".pdf"):
            safe_filename += ".pdf"

        # 写入 inbox
        target_inbox = _get_inbox_dir()
        target_inbox.mkdir(parents=True, exist_ok=True)
        dest = target_inbox / safe_filename

        dest.write_bytes(pdf_bytes)
        logger.info("PDF 已写入 inbox: %s (%d bytes)", dest, len(pdf_bytes))

        return JSONResponse(
            status_code=202,
            content={
                "status": "accepted",
                "message": f"PDF 已写入 inbox，等待 watcher 处理: {safe_filename}",
                "path": str(dest),
            },
        )

    return router


# ── 模块副作用: 注册到 plugin registry（main.py 无需修改）──────────────────
def _register_advisor_router() -> None:
    """将 advisor router 注册到全局 plugin registry。"""
    try:
        from decision_ledger.config import load_settings
        from decision_ledger.plugin import register_router

        try:
            settings = load_settings()
            inbox = settings.decision_ledger_home / "inbox"
        except Exception:
            inbox = Path("~/decision_ledger/inbox").expanduser()

        router = create_advisor_router(inbox_dir=inbox)
        register_router(router)
    except ImportError:
        pass


_register_advisor_router()
