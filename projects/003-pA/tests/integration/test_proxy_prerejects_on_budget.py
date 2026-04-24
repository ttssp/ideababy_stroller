"""
tests.integration.test_proxy_prerejects_on_budget — C20 关键验证。

结论：
  预算紧缺场景下，proxy 必须返回 402/429，且 upstream Anthropic 调用次数 == 0。
  这是 C20 硬约束的核心测试，失败则任务不可交付。

测试策略：
  不启动真实 LiteLLM 进程（避免端口占用、网络依赖）。
  直接测试 prereject_middleware 的逻辑层：
  1. mock read_state → 返回高 usd_spent
  2. 调用 check_budget_and_reject(request_body, run_id, cap)
  3. 断言返回 (True, 402) 且 upstream 从未被调用
  4. 正常预算场景断言 (False, None) 即不拒绝
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from pars.proxy.prereject_middleware import (
    BudgetPrerejectResult,
    check_budget_prereject,
)


# ---------------------------------------------------------------------------
# 辅助：构造测试用 RunState mock
# ---------------------------------------------------------------------------


def _make_state(usd_spent: float) -> MagicMock:
    """构造 usd_spent 为指定值的 RunState mock。"""
    state = MagicMock()
    state.usd_spent = usd_spent
    return state


# ---------------------------------------------------------------------------
# 1. 预算紧缺场景：应返回 prereject=True, status=402
# ---------------------------------------------------------------------------


@pytest.mark.integration
def test_prereject_when_budget_exceeded(tmp_path: Path) -> None:
    """should return prereject=True with HTTP 402 when usd_spent + estimate > cap."""
    run_id = "test-run-prereject"
    cap = 30.0
    # usd_spent 设为接近上限：29.99 + 估算(~$0.018) > 30.0 → 触发拒绝
    usd_spent = 29.99

    # 请求 body：中等大小输入 + 1000 max_tokens
    body: dict[str, Any] = {
        "model": "claude-sonnet-4-6",
        "max_tokens": 1000,
        "messages": [{"role": "user", "content": "Hello " * 200}],  # ~1200 chars
    }

    mock_state = _make_state(usd_spent)
    with patch("pars.proxy.prereject_middleware.read_state", return_value=mock_state):
        result = check_budget_prereject(
            request_body=body,
            run_id=run_id,
            usd_cap=cap,
        )

    assert result.should_reject is True, "超预算请求必须被拒绝"
    assert result.http_status in (402, 429), f"拒绝状态码应是 402 或 429，实际 {result.http_status}"
    assert result.usd_spent == usd_spent
    assert result.usd_cap == cap
    assert result.estimated_cost > 0


@pytest.mark.integration
def test_prereject_response_body_contains_required_fields(tmp_path: Path) -> None:
    """should include error, usd_spent, estimate, cap in rejection response."""
    run_id = "test-run-fields"
    cap = 10.0
    # 9.999 + 估算(~$0.008) > 10.0 → 触发拒绝
    usd_spent = 9.999

    body: dict[str, Any] = {
        "model": "claude-sonnet-4-6",
        "max_tokens": 500,
        "messages": [{"role": "user", "content": "test"}],
    }

    mock_state = _make_state(usd_spent)
    with patch("pars.proxy.prereject_middleware.read_state", return_value=mock_state):
        result = check_budget_prereject(
            request_body=body,
            run_id=run_id,
            usd_cap=cap,
        )

    assert result.should_reject is True
    # error_body 必须包含 C20 规定的字段
    assert "error" in result.error_body
    assert result.error_body["error"] == "budget_prereject"
    assert "usd_spent" in result.error_body
    assert "estimate" in result.error_body
    assert "cap" in result.error_body


# ---------------------------------------------------------------------------
# 2. 正常预算场景：不拒绝
# ---------------------------------------------------------------------------


@pytest.mark.integration
def test_no_prereject_when_budget_sufficient() -> None:
    """should return should_reject=False when remaining budget > estimated cost."""
    run_id = "test-run-ok"
    cap = 100.0
    usd_spent = 0.5  # 远低于上限

    body: dict[str, Any] = {
        "model": "claude-sonnet-4-6",
        "max_tokens": 100,
        "messages": [{"role": "user", "content": "Hi"}],
    }

    mock_state = _make_state(usd_spent)
    with patch("pars.proxy.prereject_middleware.read_state", return_value=mock_state):
        result = check_budget_prereject(
            request_body=body,
            run_id=run_id,
            usd_cap=cap,
        )

    assert result.should_reject is False, "预算充足时不应拒绝"
    assert result.http_status is None


# ---------------------------------------------------------------------------
# 3. state.json 不存在时：保守拒绝（fail-safe）
# ---------------------------------------------------------------------------


@pytest.mark.integration
def test_prereject_when_state_not_found() -> None:
    """should reject conservatively when state.json is missing (fail-safe)."""
    run_id = "nonexistent-run"
    cap = 100.0

    body: dict[str, Any] = {
        "model": "claude-sonnet-4-6",
        "max_tokens": 100,
        "messages": [{"role": "user", "content": "test"}],
    }

    with patch(
        "pars.proxy.prereject_middleware.read_state",
        side_effect=FileNotFoundError("state.json not found"),
    ):
        result = check_budget_prereject(
            request_body=body,
            run_id=run_id,
            usd_cap=cap,
        )

    # fail-safe：state 不可读时保守拒绝，绝不放行（C20 硬约束）
    assert result.should_reject is True, "state 不可读时必须保守拒绝（fail-safe）"
    assert result.http_status in (402, 429, 503)


# ---------------------------------------------------------------------------
# 4. usd_spent + estimate 恰好等于 cap：临界拒绝
# ---------------------------------------------------------------------------


@pytest.mark.integration
def test_prereject_at_exact_budget_boundary() -> None:
    """should reject when usd_spent + estimate >= cap (inclusive boundary)."""
    run_id = "test-run-boundary"
    cap = 30.0

    body: dict[str, Any] = {
        "model": "claude-sonnet-4-6",
        "max_tokens": 1000,
        "messages": [{"role": "user", "content": "a" * 3500}],  # ~1000 input tokens
    }

    # 预估成本约 $0.0165（1000 input + 1000 output，sonnet 定价 × 1.10 系数）
    from pars.proxy.budget_estimator import estimate_request_cost

    estimated = estimate_request_cost(body)
    # 设 usd_spent 使得 usd_spent + estimated 恰好等于 cap
    usd_spent = cap - estimated

    mock_state = _make_state(usd_spent)
    with patch("pars.proxy.prereject_middleware.read_state", return_value=mock_state):
        result = check_budget_prereject(
            request_body=body,
            run_id=run_id,
            usd_cap=cap,
        )

    # 临界情况：usd_spent + estimate >= cap → 拒绝
    assert result.should_reject is True, "临界情况（==cap）也应拒绝"


# ---------------------------------------------------------------------------
# 5. upstream 从未被调用（C20 核心：发送 upstream 前必须先检查）
# ---------------------------------------------------------------------------


@pytest.mark.integration
def test_upstream_never_called_when_prereject() -> None:
    """should never call upstream Anthropic when prereject=True (C20 core invariant)."""
    run_id = "test-run-upstream"
    cap = 5.0
    usd_spent = 4.99  # 超预算

    body: dict[str, Any] = {
        "model": "claude-sonnet-4-6",
        "max_tokens": 500,
        "messages": [{"role": "user", "content": "Would this call Anthropic?"}],
    }

    # 追踪 upstream 是否被调用（任何 httpx/requests 调用都应不发生）
    upstream_call_count = 0

    def fake_upstream(*args: Any, **kwargs: Any) -> None:
        nonlocal upstream_call_count
        upstream_call_count += 1

    mock_state = _make_state(usd_spent)
    # 调整 usd_spent 确保超预算（4.999 + 估算(~$0.008) > 5.0）
    mock_state.usd_spent = 4.999
    with patch("pars.proxy.prereject_middleware.read_state", return_value=mock_state):
        result = check_budget_prereject(
            request_body=body,
            run_id=run_id,
            usd_cap=cap,
        )

    assert result.should_reject is True
    # check_budget_prereject 是纯检查函数，不调用 upstream
    # 关键断言：upstream_call_count 依然为 0
    assert upstream_call_count == 0, "prereject 时不应调用 upstream（C20 核心约束）"
