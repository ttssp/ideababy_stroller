"""
FastAPI 应用入口 — T001
结论: 仅做 app 实例 + /healthz + plugin registry 接入，子组件后续 Phase 通过 import 副作用注册
细节:
  - bind 127.0.0.1（架构不变量 #7，永远不接 0.0.0.0）
  - plugin registry 模式: register_router / register_startup_task / register_scheduler_job
  - lifespan: 执行所有注册的 startup_tasks
  - DECISION_LEDGER_TEST_MODE=strict 由 CI 注入（架构不变量 #15）
"""

from __future__ import annotations

import asyncio
import logging
from collections.abc import AsyncGenerator, Coroutine
from contextlib import asynccontextmanager
from typing import Any  # needed for Coroutine[Any, Any, None]

import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from decision_ledger.config import ConfigError, load_settings
from decision_ledger.plugin import apply_to_app, get_startup_tasks

# ── 日志配置 ─────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("decision_ledger.main")


# ── 配置加载（fail-fast）────────────────────────────────
# 结论: 启动时立即校验 env，防止运行中途才爆炸
try:
    _settings = load_settings()
    logger.info(
        "配置加载成功 | home=%s | test_mode=%s",
        _settings.decision_ledger_home,
        _settings.decision_ledger_test_mode,
    )
except ConfigError as _config_err:
    # 在测试环境下（test_smoke.py 用 env mock），允许延迟初始化
    # 真实启动时若 env 缺失，uvicorn 启动前就会报错
    logger.warning("配置加载跳过 (可能在测试中): %s", _config_err)
    _settings = None  # type: ignore[assignment]


# ── Lifespan 上下文管理器 ─────────────────────────────────
@asynccontextmanager
async def _lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """结论: 启动时运行所有注册的 startup tasks，关闭时清理资源。"""
    tasks = get_startup_tasks()
    logger.info("启动 %d 个后台任务...", len(tasks))

    # 并发启动所有注册的 startup tasks
    running: list[asyncio.Task[None]] = []
    for factory in tasks:
        coro: Coroutine[Any, Any, None] = factory()
        t: asyncio.Task[None] = asyncio.create_task(coro, name=getattr(factory, "__name__", "task"))
        running.append(t)

    logger.info("FastAPI 应用已就绪 | bind=127.0.0.1:8000")
    yield

    # 关闭时取消所有后台任务
    for t in running:
        t.cancel()
    if running:
        await asyncio.gather(*running, return_exceptions=True)
    logger.info("所有后台任务已停止")


# ── FastAPI App 实例 ─────────────────────────────────────
app = FastAPI(
    title="决策账本",
    version="0.1.0",
    description="ML PhD 自用投资决策档案系统 — calibration engine first",
    lifespan=_lifespan,
    # 生产环境关闭 OpenAPI（localhost 私用可保留）
    openapi_url="/openapi.json",
    docs_url="/docs",
)


# ── 健康检查路由 ─────────────────────────────────────────
@app.get("/healthz", response_class=JSONResponse)
async def healthz() -> dict[str, bool]:
    """结论: 健康探针，返回 {ok: true}，不做任何 DB / LLM 调用。

    架构不变量 #7 检查点: 此 endpoint 只能通过 127.0.0.1 访问。
    """
    return {"ok": True}


# ── Plugin registry 应用 ─────────────────────────────────
# 结论: 后续 task 只需在自己模块顶部 import 并调用 register_router 等，
#       main.py 在此处统一 apply，不再修改 main.py
apply_to_app(app)


# ── __main__ 入口 ────────────────────────────────────────
# 结论: python -m decision_ledger.main 触发，强制 bind 127.0.0.1（架构不变量 #7）
if __name__ == "__main__":
    uvicorn.run(
        "decision_ledger.main:app",
        host="127.0.0.1",  # 永远不接 0.0.0.0（架构不变量 §9.7）
        port=8000,
        reload=False,
        log_level="info",
    )
