"""
FastAPI 应用入口 — T001
结论: 仅做 app 实例 + /healthz + plugin registry 接入，子组件后续 Phase 通过 import 副作用注册
细节:
  - bind 127.0.0.1（架构不变量 #7，永远不接 0.0.0.0）
  - plugin registry 模式: register_router / register_startup_task / register_scheduler_job
  - lifespan: 执行所有注册的 startup_tasks
  - DECISION_LEDGER_TEST_MODE=strict 由 CI 注入 (架构不变量 #15)
    production 应当不注入此 env (留空), 让 _get_conflict_worker 走 _Noop 替身

F2-T020 followup A1: lifespan 加启动期 stderr BANNER 列出 v0.1 已知 stub
  (ConflictWorker 未 wire / FailureAlert cron 未起 / TabMetricsMiddleware 未挂 /
  register_scheduler_job 死消费), 让"v0.1 plugin registry 系统性死代码"
  显式可见, 不再"沉默的 0%"。详见 docs/known-issues-v0.1.md。
"""

from __future__ import annotations

import asyncio
import logging
import os
import sys
from collections.abc import AsyncGenerator, Coroutine
from contextlib import asynccontextmanager
from typing import Any  # needed for Coroutine[Any, Any, None]

import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from decision_ledger.config import ConfigError, load_settings
from decision_ledger.monitor.pause_pipeline import get_wiring_status
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


# ── F2-T020 followup A1: v0.1 已知 stub 启动期 BANNER ──────────────────────────
#
# 为什么用 stderr.write 而不是 logger: BANNER 必须无视 logging level filter,
# 即便 root logger 被设成 ERROR 也要打出来。这是"沉默的 0% → 可见信号" 的关键。
# 单用户 localhost 没人看 INFO log, 但每次启动 terminal 都会扫到 stderr。
_V01_BANNER_SUPPRESS_ENV = "DECISION_LEDGER_SUPPRESS_V01_BANNER"


def _build_v01_banner() -> str | None:
    """构造 v0.1 已知 stub BANNER 文本。返回 None 表示无 stub (未来全 wire 后)。

    F2-T020 followup A1: 通过 get_wiring_status() 检测 wiring,
    如果某槽位未来真 wire 了, 该行会从 banner 中自动消失。
    """
    wiring = get_wiring_status()
    stubs: list[str] = []
    if wiring.get("conflict_worker") == "noop":
        stubs.append("ConflictWorker:        not wired (B-lite engage pause = no-op)")
    # 以下 stub 是 v0.1 的设计选择, 不依赖 wiring detect (没有对应注入点);
    # 直接列出, 等 v0.2 真 wire 时手工删除对应行。
    stubs.append(
        "FailureAlert cron:     not scheduled (manual run only)"
    )
    stubs.append("TabMetricsMiddleware:  not installed (OP-6 ratio is best-effort)")
    stubs.append("register_scheduler_job: collected but never started (cron-only)")
    # 用户视角最大 stub: 12 个 router setter 在 production 永不被调,
    # 用户跑 ./start.sh 后访问 /decisions/draft 等 DB-bound 路由会 500.
    # 详见 known-issues-v0.1.md §8. v0.2 建 production app factory 修复.
    stubs.append("DB-bound routers:      500 in production (use e2e factory; §8)")

    if not stubs:
        return None

    bar = "*" * 78
    body_lines = [
        bar,
        "*** v0.1 KNOWN LIMITATIONS — see docs/known-issues-v0.1.md".ljust(74) + " ***",
    ]
    for line in stubs:
        body_lines.append("*** " + line.ljust(70) + " ***")
    body_lines.append(bar)
    return "\n".join(body_lines) + "\n"


def _print_v01_banner() -> None:
    """启动期把 v0.1 stub BANNER 打到 stderr。

    用环境变量 DECISION_LEDGER_SUPPRESS_V01_BANNER=1 关闭 (CI / 测试 / 监控对接用)。
    """
    if os.environ.get(_V01_BANNER_SUPPRESS_ENV) == "1":
        return
    banner = _build_v01_banner()
    if banner is None:
        return
    sys.stderr.write(banner)
    sys.stderr.flush()


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

    # F2-T020 followup A1: 在 ready log 之前打 v0.1 stub BANNER 到 stderr
    _print_v01_banner()

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
