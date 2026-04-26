"""
LLMClient 单元测试 — T005 TDD 先写 (红)
结论: 验证 cache hit/miss, fallback, key redact, schema error, usage 记账
细节:
  - mock anthropic SDK 不发真请求
  - 月成本 > $40 自动降级 Sonnet → Haiku
  - API key 不能出现在日志 (SEC-3)
  - tool-use schema 不匹配 → LLMSchemaError (SEC-4)
  - cache 命中跳过 API 调用
"""

from __future__ import annotations

import logging
from decimal import Decimal
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from pydantic import BaseModel

from decision_ledger.llm.client import LLMClient
from decision_ledger.llm.errors import LLMSchemaError

# ── Pydantic schema for tests ──────────────────────────────────────────────────

class _TestSchema(BaseModel):
    """测试用 schema。"""
    direction: str
    confidence: float


# ── fake LLMUsageWriter (解耦 T003) ───────────────────────────────────────────

class _FakeUsageWriter:
    """
    LLMUsageWriter 的 fake 实现 — 内存存储，测试用。
    解耦 T003: 不 import LLMUsageRepository。
    """

    def __init__(self, monthly_cost: float = 0.0) -> None:
        self.records: list[Any] = []
        self._monthly_cost = Decimal(str(monthly_cost))

    async def insert(self, usage: Any) -> None:
        self.records.append(usage)

    async def monthly_total_cost(self) -> Decimal:
        return self._monthly_cost


# ── helpers ───────────────────────────────────────────────────────────────────

def _make_tool_use_response(content: dict[str, Any]) -> MagicMock:
    """构造 anthropic SDK tool-use 响应 mock。"""
    tool_block = MagicMock()
    tool_block.type = "tool_use"
    tool_block.input = content

    response = MagicMock()
    response.content = [tool_block]
    response.usage = MagicMock()
    response.usage.input_tokens = 100
    response.usage.output_tokens = 50
    response.model = "claude-sonnet-4-6"
    return response


def _make_client(
    tmp_path: Path,
    usage_writer: _FakeUsageWriter | None = None,
    api_key: str = "sk-ant-test-key-000",
) -> LLMClient:
    """创建 LLMClient 实例。"""
    if usage_writer is None:
        usage_writer = _FakeUsageWriter()
    return LLMClient(
        api_key=api_key,
        usage_writer=usage_writer,
        cache_dir=tmp_path,
    )


# ── test: cache hit 跳过 API 调用 ─────────────────────────────────────────────

@pytest.mark.asyncio
async def test_cache_hit_skips_api_call(tmp_path: Path) -> None:
    """结论: cache 命中时不调用 anthropic SDK (D11)。"""
    client = _make_client(tmp_path)
    # 先 put 一个 cache 条目
    client._cache.put(
        advisor_week_id="2026-W17",
        ticker="TSM",
        prompt_template_version="conflict_v1",
        model="claude-sonnet-4-6",
        data={"direction": "long", "confidence": 0.8},
    )
    with patch("anthropic.Anthropic") as mock_cls:
        result = await client.call(
            prompt="test prompt",
            template_version="conflict_v1",
            cache_key_extras={"advisor_week_id": "2026-W17", "ticker": "TSM"},
            schema=_TestSchema,
            model="claude-sonnet-4-6",
        )
        # API 不应被调用
        mock_cls.assert_not_called()
    assert result.direction == "long"
    assert result.confidence == 0.8


# ── test: cache miss 时调用 API ───────────────────────────────────────────────

@pytest.mark.asyncio
async def test_cache_miss_calls_anthropic_api(tmp_path: Path) -> None:
    """结论: cache miss 时调用 anthropic SDK 并写入 cache。"""
    usage_writer = _FakeUsageWriter()
    client = _make_client(tmp_path, usage_writer=usage_writer)

    mock_response = _make_tool_use_response({"direction": "short", "confidence": 0.6})

    with patch.object(client, "_call_api", new_callable=AsyncMock) as mock_api:
        mock_api.return_value = mock_response
        result = await client.call(
            prompt="test prompt",
            template_version="conflict_v1",
            cache_key_extras={"advisor_week_id": "2026-W17", "ticker": "TSM"},
            schema=_TestSchema,
            model="claude-sonnet-4-6",
        )
        mock_api.assert_called_once()

    assert result.direction == "short"
    assert result.confidence == 0.6
    # usage 应该被记录
    assert len(usage_writer.records) == 1


# ── test: cache miss 后 API 结果写入 cache ───────────────────────────────────

@pytest.mark.asyncio
async def test_cache_miss_result_is_stored_in_cache(tmp_path: Path) -> None:
    """结论: API 调用成功后，结果写入 cache，下次 get 可命中。"""
    client = _make_client(tmp_path)
    mock_response = _make_tool_use_response({"direction": "long", "confidence": 0.9})

    with patch.object(client, "_call_api", new_callable=AsyncMock) as mock_api:
        mock_api.return_value = mock_response
        await client.call(
            prompt="test prompt",
            template_version="conflict_v1",
            cache_key_extras={"advisor_week_id": "2026-W17", "ticker": "TSM"},
            schema=_TestSchema,
            model="claude-sonnet-4-6",
        )

    # 第二次 call 应命中 cache，不再调用 API
    with patch.object(client, "_call_api", new_callable=AsyncMock) as mock_api2:
        result2 = await client.call(
            prompt="test prompt",
            template_version="conflict_v1",
            cache_key_extras={"advisor_week_id": "2026-W17", "ticker": "TSM"},
            schema=_TestSchema,
            model="claude-sonnet-4-6",
        )
        mock_api2.assert_not_called()

    assert result2.confidence == 0.9


# ── test: 月成本 > $40 自动 fallback Sonnet → Haiku ─────────────────────────

@pytest.mark.asyncio
async def test_monthly_cost_over_40_fallback_to_haiku(tmp_path: Path) -> None:
    """结论: monthly_total_cost > $40 时，即使 model='sonnet'，实际使用 Haiku (TECH-2)。"""
    usage_writer = _FakeUsageWriter(monthly_cost=41.0)
    client = _make_client(tmp_path, usage_writer=usage_writer)

    mock_response = _make_tool_use_response({"direction": "neutral", "confidence": 0.5})
    mock_response.model = "claude-haiku-4-5"

    actual_model_used: list[str] = []

    async def fake_call_api(prompt: str, schema: type, model: str) -> Any:
        actual_model_used.append(model)
        return mock_response

    with patch.object(client, "_call_api", new_callable=AsyncMock, side_effect=fake_call_api):
        result = await client.call(
            prompt="test prompt",
            template_version="conflict_v1",
            cache_key_extras={"advisor_week_id": "2026-W17", "ticker": "TSM"},
            schema=_TestSchema,
            model="claude-sonnet-4-6",  # 请求 Sonnet
        )

    # 实际应降级到 Haiku
    assert actual_model_used[0] == "claude-haiku-4-5"
    assert result.direction == "neutral"


# ── test: usage 记录 model 字段在 fallback 后是 Haiku ─────────────────────────

@pytest.mark.asyncio
async def test_usage_records_haiku_model_when_fallback(tmp_path: Path) -> None:
    """结论: fallback 后 llm_usage.model 字段应为 'claude-haiku-4-5' (TECH-2 mitigation)。"""
    usage_writer = _FakeUsageWriter(monthly_cost=45.0)
    client = _make_client(tmp_path, usage_writer=usage_writer)

    mock_response = _make_tool_use_response({"direction": "long", "confidence": 0.7})
    mock_response.model = "claude-haiku-4-5"

    with patch.object(client, "_call_api", new_callable=AsyncMock) as mock_api:
        mock_api.return_value = mock_response
        await client.call(
            prompt="prompt",
            template_version="conflict_v1",
            cache_key_extras={"advisor_week_id": "2026-W17", "ticker": "TSM"},
            schema=_TestSchema,
            model="claude-sonnet-4-6",
        )

    assert len(usage_writer.records) == 1
    assert usage_writer.records[0].model == "claude-haiku-4-5"


# ── test: API key 不出现在日志 (SEC-3) ───────────────────────────────────────

def test_api_key_not_leaked_in_logs(tmp_path: Path, caplog: pytest.LogCaptureFixture) -> None:
    """结论: API key 不应出现在日志输出中 (SEC-3 redact sk-ant-***)。"""
    api_key = "sk-ant-api03-supersecretkey12345"
    _make_client(tmp_path, api_key=api_key)

    with caplog.at_level(logging.DEBUG):
        # 触发 key 相关的初始化日志
        client = LLMClient(
            api_key=api_key,
            usage_writer=_FakeUsageWriter(),
            cache_dir=tmp_path,
        )
        _ = client  # suppress unused warning

    # 验证日志中无明文 key
    full_log = caplog.text
    assert "sk-ant-api03-supersecretkey12345" not in full_log


# ── test: tool-use schema 不匹配 → LLMSchemaError (SEC-4) ────────────────────

@pytest.mark.asyncio
async def test_schema_mismatch_raises_llm_schema_error(tmp_path: Path) -> None:
    """结论: API 返回数据不符合 pydantic schema 时，raise LLMSchemaError (SEC-4)。"""
    client = _make_client(tmp_path)

    # API 返回缺少必填字段的数据
    mock_response = _make_tool_use_response({"wrong_field": "value"})  # 缺少 direction/confidence

    with patch.object(client, "_call_api", new_callable=AsyncMock) as mock_api:
        mock_api.return_value = mock_response
        with pytest.raises(LLMSchemaError):
            await client.call(
                prompt="test prompt",
                template_version="conflict_v1",
                cache_key_extras={"advisor_week_id": "2026-W17", "ticker": "TSM"},
                schema=_TestSchema,
                model="claude-sonnet-4-6",
            )


# ── test: cache hit 也记录 usage (cache_hit=True, cost=0) ────────────────────

@pytest.mark.asyncio
async def test_cache_hit_records_usage_with_zero_cost(tmp_path: Path) -> None:
    """结论: cache 命中时也写 usage 记录，但 cost_usd=0, cache_hit=True (D11 监控)。"""
    usage_writer = _FakeUsageWriter()
    client = _make_client(tmp_path, usage_writer=usage_writer)

    # 先写入 cache
    client._cache.put(
        advisor_week_id="2026-W17",
        ticker="TSM",
        prompt_template_version="conflict_v1",
        model="claude-sonnet-4-6",
        data={"direction": "long", "confidence": 0.8},
    )

    await client.call(
        prompt="test prompt",
        template_version="conflict_v1",
        cache_key_extras={"advisor_week_id": "2026-W17", "ticker": "TSM"},
        schema=_TestSchema,
        model="claude-sonnet-4-6",
    )

    assert len(usage_writer.records) == 1
    assert usage_writer.records[0].cache_hit is True
    assert usage_writer.records[0].cost_usd == 0.0


# ── test: usage 记录 prompt_template_version ─────────────────────────────────

@pytest.mark.asyncio
async def test_usage_records_template_version(tmp_path: Path) -> None:
    """结论: LLMUsage 记录含 prompt_template_version 字段 (架构 §10 M4)。"""
    usage_writer = _FakeUsageWriter()
    client = _make_client(tmp_path, usage_writer=usage_writer)

    client._cache.put(
        advisor_week_id="2026-W17",
        ticker="TSM",
        prompt_template_version="advisor_v2",
        model="claude-sonnet-4-6",
        data={"direction": "long", "confidence": 0.8},
    )

    await client.call(
        prompt="test",
        template_version="advisor_v2",
        cache_key_extras={"advisor_week_id": "2026-W17", "ticker": "TSM"},
        schema=_TestSchema,
        model="claude-sonnet-4-6",
    )

    assert usage_writer.records[0].prompt_template_version == "advisor_v2"
