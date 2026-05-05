"""
冒烟测试 — T001
结论: 验证 FastAPI app 实例存在 + /healthz 路由正确注册
细节: 不启动真实 server, 仅检查路由表
"""

from __future__ import annotations

import os


def test_app_is_not_none_when_env_set() -> None:
    """should create app instance when required env vars are set"""
    os.environ.setdefault("ANTHROPIC_API_KEY", "sk-test-placeholder")
    os.environ.setdefault("TELEGRAM_BOT_TOKEN", "123:test-placeholder")
    os.environ.setdefault("DECISION_LEDGER_TEST_MODE", "strict")

    from decision_ledger.main import app  # 延迟 import，env 先设

    assert app is not None


def test_app_has_healthz_route() -> None:
    """should register /healthz route that returns {ok: true}"""
    os.environ.setdefault("ANTHROPIC_API_KEY", "sk-test-placeholder")
    os.environ.setdefault("TELEGRAM_BOT_TOKEN", "123:test-placeholder")
    os.environ.setdefault("DECISION_LEDGER_TEST_MODE", "strict")

    from fastapi.testclient import TestClient

    from decision_ledger.main import app

    client = TestClient(app)
    response = client.get("/healthz")
    assert response.status_code == 200
    data = response.json()
    assert data == {"ok": True}


def test_app_routes_contain_healthz() -> None:
    """should include /healthz in app.routes list"""
    os.environ.setdefault("ANTHROPIC_API_KEY", "sk-test-placeholder")
    os.environ.setdefault("TELEGRAM_BOT_TOKEN", "123:test-placeholder")
    os.environ.setdefault("DECISION_LEDGER_TEST_MODE", "strict")

    from decision_ledger.main import app

    paths = [getattr(r, "path", None) for r in app.routes]
    assert "/healthz" in paths
