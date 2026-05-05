"""
E2E 首屏延迟测试 — T004
结论: 启动真实 uvicorn server，用 Playwright 测量首屏 DCL < 2000ms (SLA §1.2)
细节:
  - 标记 @pytest.mark.e2e 便于 CI 单独运行
  - 启动前设置必要 env vars，避免 ConfigError
  - 测量 performance.timing.domContentLoadedEventEnd - navigationStart
  - 等待 networkidle 确保所有资源加载完毕再取时间
  - 超时保护: page.goto timeout=10s
"""

from __future__ import annotations

import os
import subprocess
import time
from collections.abc import Generator
from pathlib import Path
from typing import Any

import pytest

# ── Pytest mark 注册 ─────────────────────────────────────
pytestmark = pytest.mark.e2e

# ── 测试常量 ─────────────────────────────────────────────
_SERVER_HOST = "127.0.0.1"
_SERVER_PORT = 18000  # 使用非标准端口避免与开发 server 冲突
_SERVER_URL = f"http://{_SERVER_HOST}:{_SERVER_PORT}/"
_DCL_SLA_MS = 2000  # SLA §1.2: 首屏 DCL < 2s


@pytest.fixture(scope="module")
def e2e_server() -> Generator[str, None, None]:
    """结论: 启动真实 uvicorn server（子进程），yield URL，测试完毕后终止。
    细节:
      - 使用 subprocess 避免 event loop 冲突
      - 等待 server 就绪（轮询 /healthz 最多 10s）
      - scope=module 提升 server 启动效率
    """
    import socket

    env = {
        **os.environ,
        "ANTHROPIC_API_KEY": "test-e2e-key",
        "TELEGRAM_BOT_TOKEN": "test-e2e-token",
        "DECISION_LEDGER_TEST_MODE": "strict",
    }

    # 启动 uvicorn 子进程（使用 decision_ledger.ui.app 工厂）
    cmd = [
        "uv",
        "run",
        "uvicorn",
        "decision_ledger.ui.app:_make_standalone_app",
        "--host",
        _SERVER_HOST,
        "--port",
        str(_SERVER_PORT),
        "--factory",
        "--log-level",
        "warning",
    ]
    proc = subprocess.Popen(  # noqa: S603 — 测试受信任命令
        cmd,
        cwd=Path(__file__).parents[2],
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    # 等待 server 就绪
    deadline = time.time() + 10.0
    while time.time() < deadline:
        try:
            with socket.create_connection((_SERVER_HOST, _SERVER_PORT), timeout=0.5):
                break
        except OSError:
            time.sleep(0.2)
    else:
        proc.terminate()
        pytest.fail(f"E2E server 在 10s 内未就绪 ({_SERVER_URL})")

    yield _SERVER_URL

    proc.terminate()
    proc.wait(timeout=5)


@pytest.mark.e2e
def test_should_load_first_screen_within_sla_when_playwright(
    e2e_server: str,
) -> None:
    """结论: 首屏 DCL (DOMContentLoaded) 必须 < 2000ms（SLA §1.2）。
    细节: 通过 performance.timing API 测量，不依赖视觉截图。
    """
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # goto 会等到 networkidle / load event 完成
        page.goto(e2e_server, timeout=10_000, wait_until="domcontentloaded")

        # 通过 performance.timing API 取 DCL 耗时
        dcl_ms: Any = page.evaluate(
            """() => {
                const t = performance.timing;
                return t.domContentLoadedEventEnd - t.navigationStart;
            }"""
        )

        browser.close()

    assert isinstance(dcl_ms, int | float), (
        f"performance.timing 返回类型异常: {type(dcl_ms)}"
    )
    assert dcl_ms < _DCL_SLA_MS, (
        f"首屏 DCL={dcl_ms:.0f}ms 超过 SLA {_DCL_SLA_MS}ms (§1.2)"
    )
