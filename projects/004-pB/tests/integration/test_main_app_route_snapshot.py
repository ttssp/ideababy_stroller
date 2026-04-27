"""
test_main_app_route_snapshot.py — Codex review F1 钉死现状

结论: 钉死"v0.1 production main app 路由表 = 5 条 (healthz + docs)"的现状,
让"沉默的 0% production wiring 缺失"变成可见的 nonregression gate.

为什么需要这个 test:
  - Codex review F1: from decision_ledger.main import app 后, app.routes 只有
    {/healthz, /docs, /docs/oauth2-redirect, /openapi.json, /redoc} 5 条
  - 没有任何业务路由 (decisions/conflicts/post-mortem/notes/...) 注册
  - 这是因为 main.py 不导入 router 模块, plugin registry 在 production 启动时为空
  - F2-T020 followup A1 加的 BANNER 已经把这件事标到 stderr 可见
  - 但需要一个**测试**钉死现状, 防止"未来某天接通了一半 router 又退回去"
    导致 BANNER 显示一切正常但实际只有部分 wired

为什么用 subprocess:
  - 同一 pytest 进程内, 其他 ui 测试已经 import 过各 router 模块,
    触发了 module-level register_router(...) 副作用; plugin registry 不再为空,
    apply_to_app(app) 之后 app.routes 已包含业务路由 → 同进程 import 无法
    精确反映"production 进程独立启动" 的真实状态
  - subprocess 模拟用户跑 `python -m decision_ledger.main` 的真实启动 — 全新
    Python 解释器, plugin registry 必然为空, 真实反映 v0.1 production 行为

本 test 的双重意图:
  (a) v0.1 现在: 通过 = production 路由表正是预期的 5 条 (没接通业务)
  (b) v0.2 production app factory 接通时: 此 test 会 fail, 强制 v0.2 工程师
      显式更新 EXPECTED_ROUTES, 同时确认全套业务路由都已注册

详见 docs/known-issues-v0.1.md §8.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def _import_main_app_in_subprocess() -> list[str]:
    """干净 subprocess 里 import main.app, 返回路由 path 列表。

    模拟用户跑 `python -m decision_ledger.main` 的全新进程启动状态,
    不受同 pytest 进程内其他测试 import router 模块的副作用影响。
    """
    env = {
        **os.environ,
        "ANTHROPIC_API_KEY": os.environ.get("ANTHROPIC_API_KEY", "test-key-placeholder"),
        "TELEGRAM_BOT_TOKEN": os.environ.get("TELEGRAM_BOT_TOKEN", "000:test-placeholder"),
        "DECISION_LEDGER_SUPPRESS_V01_BANNER": "1",
    }

    code = (
        "import json\n"
        "from decision_ledger.main import app\n"
        "paths = sorted(getattr(r, 'path', str(r)) for r in app.routes)\n"
        "print(json.dumps(paths))\n"
    )

    result = subprocess.run(  # noqa: S603
        [sys.executable, "-c", code],
        cwd=str(PROJECT_ROOT),
        env=env,
        capture_output=True,
        text=True,
        timeout=15,
    )
    assert result.returncode == 0, (
        f"subprocess 失败:\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
    )
    # stdout 最后一行才是 JSON (前面可能有 logging 输出)
    lines = [ln for ln in result.stdout.strip().splitlines() if ln.startswith("[")]
    assert lines, f"subprocess 输出未含 JSON 路由列表:\n{result.stdout}"
    return list(json.loads(lines[-1]))


def test_main_app_route_snapshot_in_v01_production_path() -> None:
    """F1: from decision_ledger.main import app 后路由表必须等于预期 5 条。

    任何额外路由 = v0.2 production wiring 已接通 (好), 需更新 snapshot.
    任何缺失路由 = main.py / FastAPI 默认 endpoint 配置回退 (坏).
    """
    actual_paths = _import_main_app_in_subprocess()

    expected_paths = sorted([
        "/docs",
        "/docs/oauth2-redirect",
        "/healthz",
        "/openapi.json",
        "/redoc",
    ])

    assert actual_paths == expected_paths, (
        f"F1 production wiring snapshot 变化:\n"
        f"  expected: {expected_paths}\n"
        f"  actual:   {actual_paths}\n"
        f"如果你接通了 v0.2 production app factory (好), 请更新 EXPECTED_ROUTES\n"
        f"并确认所有业务路由都已注册. 详见 docs/known-issues-v0.1.md §8."
    )


def test_main_app_business_routes_count_is_zero_in_v01() -> None:
    """F1 互补断言: 任何业务路径前缀 (decisions/conflicts/...) 必须 0 条。

    比 snapshot test 更精确: snapshot 关心精确集合, 这条关心"业务路由是否泄漏"。
    若 v0.2 接通后, 此 test 也要更新预期.
    """
    actual_paths = _import_main_app_in_subprocess()

    business_prefixes = (
        "/decisions",
        "/conflicts",
        "/post-mortem",
        "/notes",
        "/weekly-review",
        "/monthly-review",
        "/learning",
        "/matrix",
        "/settings",
        "/onboarding",
        "/advisor",
    )
    business_routes = [
        p for p in actual_paths if any(p.startswith(pre) for pre in business_prefixes)
    ]

    assert business_routes == [], (
        f"F1 v0.1: production main app 不应含业务路由 (现在有: {business_routes})\n"
        f"如果 v0.2 接通了 production wiring, 请同步更新 test_main_app_route_snapshot."
    )
