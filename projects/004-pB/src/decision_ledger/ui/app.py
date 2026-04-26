"""
Web UI App 工厂 — T004
结论: create_app(config=None) 工厂函数，挂载 StaticFiles + Jinja2，
      通过 plugin registry 注册 shell router
细节:
  - StaticFiles 挂载到 /static
  - Jinja2Templates 指向 ui/templates/
  - 通过 register_router 注入 shell router (不修改 main.py)
  - 此模块 import 时产生副作用: 注册 shell router 到 plugin registry
"""

from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# ── 路径常量 ──────────────────────────────────────────────
_UI_DIR = Path(__file__).parent
TEMPLATES_DIR = _UI_DIR / "templates"
STATIC_DIR = _UI_DIR / "static"

# ── Jinja2 模板引擎（模块级单例，供 router 共享）────────────
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


def create_app(config: object = None) -> FastAPI:
    """创建并配置 FastAPI app（工厂函数，测试与生产共用）。

    结论: 挂载静态资源 + 注册 shell router，不修改 main.py。
    参数:
      config: 预留给后续 task 注入配置，T004 阶段不使用
    """
    from decision_ledger.ui.router_shell import router as shell_router

    app = FastAPI(
        title="决策账本",
        version="0.1.0",
        description="ML PhD 自用投资决策档案系统 — calibration engine first",
        # 生产/测试共用同一 OpenAPI schema
        openapi_url="/openapi.json",
        docs_url="/docs",
    )

    # ── 挂载静态文件 ──────────────────────────────────────
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

    # ── 注册 shell router ─────────────────────────────────
    app.include_router(shell_router)

    return app


# ── 副作用: 通过 plugin registry 注册 shell router 到主 app ──
# 结论: main.py 无需修改，import decision_ledger.ui 触发时自动注册
def _register_to_main_app() -> None:
    """将 shell router 注册到全局 plugin registry（供 main.py apply_to_app 使用）。"""
    try:
        from decision_ledger.plugin import register_router
        from decision_ledger.ui.router_shell import router as shell_router

        register_router(shell_router)
    except ImportError:
        # 独立测试时 (create_app 直接用) 不需要 plugin registry
        pass


_register_to_main_app()


def _make_standalone_app() -> FastAPI:
    """uvicorn --factory 入口: 创建独立 UI app（E2E 测试用，不走主 app lifespan）。

    结论: 等同于 create_app()，但语义上明确是 standalone 启动（非集成进 main.py）。
    """
    return create_app()
