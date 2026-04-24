"""
tests.unit.test_budget_estimator — budget_estimator.py 的单元测试。

结论：覆盖定价表、token 计数、cost 估算、边界、错误处理共 ≥ 10 个场景。
"""

from __future__ import annotations

import math

import pytest

# ---------------------------------------------------------------------------
# 导入目标模块（TDD：此时模块不存在，测试会 fail with ImportError）
# ---------------------------------------------------------------------------
from pars.proxy.budget_estimator import (
    PRICING,
    SAFETY_COEFFICIENT,
    Pricing,
    count_input_tokens,
    estimate_request_cost,
)


# ---------------------------------------------------------------------------
# 1. 定价表存在且有三个 tier
# ---------------------------------------------------------------------------


@pytest.mark.unit
def test_pricing_table_has_three_tiers() -> None:
    """should contain three model tiers when PRICING is imported."""
    assert "opus-4-7" in PRICING
    assert "sonnet-4-6" in PRICING
    assert "haiku-4-5" in PRICING


@pytest.mark.unit
def test_pricing_table_has_docstring_about_operator_update() -> None:
    """should reference operator update schedule in module docstring."""
    import pars.proxy.budget_estimator as m

    doc = m.__doc__ or ""
    # 必须提及 "操作员" 或 "operator" 更新流程（2026年 OR 季度）
    assert "操作员" in doc or "operator" in doc.lower(), (
        "模块 docstring 必须提及 '操作员' 或 'operator' 更新价格表流程"
    )


@pytest.mark.unit
def test_pricing_fields_are_positive() -> None:
    """should have all positive pricing values for each tier."""
    for tier, p in PRICING.items():
        assert p.input_per_mtok > 0, f"{tier}.input_per_mtok 必须 > 0"
        assert p.output_per_mtok > 0, f"{tier}.output_per_mtok 必须 > 0"
        assert p.cache_read_per_mtok > 0, f"{tier}.cache_read_per_mtok 必须 > 0"
        assert p.cache_write_per_mtok > 0, f"{tier}.cache_write_per_mtok 必须 > 0"


# ---------------------------------------------------------------------------
# 2. Opus / Sonnet / Haiku 各算一次（已知输入）
# ---------------------------------------------------------------------------


@pytest.mark.unit
def test_opus_cost_is_higher_than_sonnet() -> None:
    """should return higher cost for opus than sonnet given same request."""
    body = {
        "model": "claude-opus-4-7",
        "max_tokens": 1000,
        "messages": [{"role": "user", "content": "Hello world"}],
    }
    body_sonnet = {**body, "model": "claude-sonnet-4-6"}
    opus_cost = estimate_request_cost(body)
    sonnet_cost = estimate_request_cost(body_sonnet)
    assert opus_cost > sonnet_cost, "opus 定价高于 sonnet，估算 cost 也应更高"


@pytest.mark.unit
def test_haiku_cost_is_lowest() -> None:
    """should return lowest cost for haiku compared to other models."""
    base = {
        "max_tokens": 500,
        "messages": [{"role": "user", "content": "Short question"}],
    }
    haiku_cost = estimate_request_cost({**base, "model": "claude-haiku-4-5"})
    sonnet_cost = estimate_request_cost({**base, "model": "claude-sonnet-4-6"})
    opus_cost = estimate_request_cost({**base, "model": "claude-opus-4-7"})
    assert haiku_cost < sonnet_cost < opus_cost, "定价应满足 haiku < sonnet < opus"


@pytest.mark.unit
def test_sonnet_with_max_tokens_4096() -> None:
    """should return cost > 0 for sonnet request with max_tokens=4096."""
    body = {
        "model": "claude-sonnet-4-6",
        "max_tokens": 4096,
        "messages": [{"role": "user", "content": "Hello"}],
    }
    cost = estimate_request_cost(body)
    assert cost > 0, "max_tokens=4096 的 sonnet 请求估算 cost 必须 > 0"


# ---------------------------------------------------------------------------
# 3. input tokens 边界：1000 / 10000 / 100000
# ---------------------------------------------------------------------------


@pytest.mark.unit
def test_cost_scales_with_input_tokens_1000() -> None:
    """should return cost > 0 for 1000 input tokens."""
    # 生成约 1000 token 的文本（每 token ≈ 3.5 chars → 3500 chars ≈ 1000 tokens）
    content = "a" * 3500
    body = {"model": "claude-sonnet-4-6", "max_tokens": 100, "messages": [{"role": "user", "content": content}]}
    cost = estimate_request_cost(body)
    assert cost > 0


@pytest.mark.unit
def test_cost_scales_with_input_tokens_10000() -> None:
    """should return higher cost for 10000 tokens than 1000 tokens."""
    content_1k = "a" * 3500
    content_10k = "a" * 35000
    body_base = {"model": "claude-sonnet-4-6", "max_tokens": 100}
    cost_1k = estimate_request_cost({**body_base, "messages": [{"role": "user", "content": content_1k}]})
    cost_10k = estimate_request_cost({**body_base, "messages": [{"role": "user", "content": content_10k}]})
    assert cost_10k > cost_1k, "10k token 估算 cost 应高于 1k token"


@pytest.mark.unit
def test_cost_scales_with_input_tokens_100000() -> None:
    """should return substantially higher cost for 100000 tokens."""
    content_100k = "a" * 350000
    body = {"model": "claude-sonnet-4-6", "max_tokens": 100, "messages": [{"role": "user", "content": content_100k}]}
    cost = estimate_request_cost(body)
    # 100k input tokens × sonnet input price($3/Mtok) = 0.30，×1.1 ≈ $0.33
    assert cost > 0.10, f"100k tokens 应估算 > $0.10，实际 {cost}"


# ---------------------------------------------------------------------------
# 4. safety coefficient 生效（> 1.0）
# ---------------------------------------------------------------------------


@pytest.mark.unit
def test_safety_coefficient_is_applied() -> None:
    """should apply safety coefficient > 1.0 to raw cost estimate."""
    assert SAFETY_COEFFICIENT > 1.0, "安全系数必须 > 1.0（偏高估算）"


@pytest.mark.unit
def test_cost_includes_safety_buffer() -> None:
    """should include safety coefficient in final cost vs base cost."""
    # 粗验证：估算 cost 应 > 纯 input+output 的基础 cost（没有 safety 的版本）
    body = {
        "model": "claude-sonnet-4-6",
        "max_tokens": 1000,
        "messages": [{"role": "user", "content": "Hello " * 100}],
    }
    cost = estimate_request_cost(body)
    pricing = PRICING["sonnet-4-6"]
    n_input_chars = len("Hello " * 100)
    raw_input_tokens = math.ceil(n_input_chars / 3.5)
    # 最小 base cost（无 safety）
    base_input = raw_input_tokens * pricing.input_per_mtok / 1_000_000
    base_output = 1000 * pricing.output_per_mtok / 1_000_000
    base_total = base_input + base_output
    assert cost >= base_total * SAFETY_COEFFICIENT * 0.9, (
        f"estimate ({cost:.6f}) 应 ≈ base ({base_total:.6f}) × safety_coef ({SAFETY_COEFFICIENT})"
    )


# ---------------------------------------------------------------------------
# 5. 空 messages → 最小 cost > 0
# ---------------------------------------------------------------------------


@pytest.mark.unit
def test_empty_messages_returns_positive_cost() -> None:
    """should return cost > 0 even with empty messages list."""
    body = {"model": "claude-sonnet-4-6", "max_tokens": 1, "messages": []}
    cost = estimate_request_cost(body)
    assert cost > 0, "空 messages 也应有最小 cost > 0（max_tokens 的 output cost）"


# ---------------------------------------------------------------------------
# 6. 未知 model → ValueError
# ---------------------------------------------------------------------------


@pytest.mark.unit
def test_unknown_model_raises_value_error() -> None:
    """should raise ValueError when model is not in pricing table."""
    body = {
        "model": "claude-unknown-99-9",
        "max_tokens": 100,
        "messages": [{"role": "user", "content": "test"}],
    }
    with pytest.raises(ValueError, match="unknown.*model|model.*unknown|pricing|PRICING"):
        estimate_request_cost(body)


# ---------------------------------------------------------------------------
# 7. count_input_tokens 大致合理（ceil(chars / 3.5)）
# ---------------------------------------------------------------------------


@pytest.mark.unit
def test_count_input_tokens_single_message() -> None:
    """should estimate tokens as ceil(chars / 3.5) for single message."""
    content = "a" * 350  # 350 chars → ceil(350 / 3.5) = 100 tokens
    body = {"messages": [{"role": "user", "content": content}]}
    tokens = count_input_tokens(body)
    expected = math.ceil(350 / 3.5)
    assert tokens == expected, f"期望 {expected} tokens，实际 {tokens}"


@pytest.mark.unit
def test_count_input_tokens_multiple_messages() -> None:
    """should sum all message contents for token count."""
    body = {
        "messages": [
            {"role": "user", "content": "a" * 70},  # ceil(70/3.5)=20 tokens
            {"role": "assistant", "content": "b" * 105},  # ceil(105/3.5)=30 tokens
        ]
    }
    tokens = count_input_tokens(body)
    expected = math.ceil(70 / 3.5) + math.ceil(105 / 3.5)  # 20+30=50
    assert tokens == expected, f"期望 {expected} tokens，实际 {tokens}"


# ---------------------------------------------------------------------------
# 8. 字典缺失字段 → ValueError（不默认）
# ---------------------------------------------------------------------------


@pytest.mark.unit
def test_missing_model_field_raises_value_error() -> None:
    """should raise ValueError when 'model' field is missing from request body."""
    body = {"max_tokens": 100, "messages": [{"role": "user", "content": "test"}]}
    with pytest.raises((ValueError, KeyError)):
        estimate_request_cost(body)


@pytest.mark.unit
def test_missing_max_tokens_raises_value_error() -> None:
    """should raise ValueError when 'max_tokens' field is missing from request body."""
    body = {"model": "claude-sonnet-4-6", "messages": [{"role": "user", "content": "test"}]}
    with pytest.raises((ValueError, KeyError)):
        estimate_request_cost(body)


# ---------------------------------------------------------------------------
# 9. Pricing dataclass 是 frozen（不可变）
# ---------------------------------------------------------------------------


@pytest.mark.unit
def test_pricing_dataclass_is_frozen() -> None:
    """should be immutable (frozen dataclass) so pricing cannot be accidentally modified."""
    p = PRICING["sonnet-4-6"]
    with pytest.raises((AttributeError, TypeError)):
        p.input_per_mtok = 999.0  # type: ignore[misc]
