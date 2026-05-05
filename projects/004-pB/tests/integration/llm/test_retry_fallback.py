"""
LLM retry/fallback 集成测试 — T005 TDD 先写 (红)
结论: 验证 5 次指数退避 retry + Sonnet→Haiku fallback 行为
细节:
  - mock httpx/anthropic SDK 模拟 5xx → 200 序列
  - retry 耗尽 5 次后 raise LLMUnavailableError (TECH-7)
  - 主模型失败后 fallback 到 Haiku 成功
  - retry 间隔指数增长 (jitter 版本，验证至少 retry 了 N 次)
"""

from __future__ import annotations

from decimal import Decimal
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from pydantic import BaseModel

from decision_ledger.llm.client import LLMClient
from decision_ledger.llm.errors import LLMUnavailableError

# ── test schema ───────────────────────────────────────────────────────────────

class _Signal(BaseModel):
    direction: str
    confidence: float


# ── fixture: 跳过 asyncio.sleep 避免测试等待实际延迟 ─────────────────────────

@pytest.fixture(autouse=True)
def patch_sleep(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    patch asyncio.sleep 为 no-op，避免 retry 延迟让测试超时。
    retry 逻辑本身仍被验证（重试次数、异常类型），只跳过等待时间。
    """
    async def _instant_sleep(_: float) -> None:
        pass

    monkeypatch.setattr("asyncio.sleep", _instant_sleep)


# ── fake usage writer ─────────────────────────────────────────────────────────

class _FakeUsageWriter:
    def __init__(self, monthly_cost: float = 0.0) -> None:
        self.records: list[Any] = []
        self._monthly_cost = Decimal(str(monthly_cost))

    async def insert(self, usage: Any) -> None:
        self.records.append(usage)

    async def monthly_total_cost(self) -> Decimal:
        return self._monthly_cost


def _make_client(tmp_path: Path, usage_writer: _FakeUsageWriter | None = None) -> LLMClient:
    if usage_writer is None:
        usage_writer = _FakeUsageWriter()
    return LLMClient(
        api_key="sk-ant-test-key",
        usage_writer=usage_writer,
        cache_dir=tmp_path,
    )


def _make_ok_response(data: dict[str, Any], model: str = "claude-sonnet-4-6") -> MagicMock:
    """构造成功的 tool-use 响应。"""
    block = MagicMock()
    block.type = "tool_use"
    block.input = data
    resp = MagicMock()
    resp.content = [block]
    resp.usage = MagicMock()
    resp.usage.input_tokens = 200
    resp.usage.output_tokens = 80
    resp.model = model
    return resp


# ── test: 一次 5xx 后第二次成功 (retry 成功) ──────────────────────────────────

@pytest.mark.asyncio
async def test_retry_succeeds_after_one_api_error(tmp_path: Path) -> None:
    """结论: 第 1 次 API 调用失败，第 2 次成功，retry 透明处理 (TECH-7)。"""
    import anthropic

    client = _make_client(tmp_path)
    ok_response = _make_ok_response({"direction": "long", "confidence": 0.75})

    call_count = 0

    async def api_side_effect(
        prompt: str, schema: type, model: str, *args: Any, **kwargs: Any
    ) -> Any:
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            raise anthropic.APIStatusError(
                message="Internal Server Error",
                response=MagicMock(status_code=500),
                body={"error": {"type": "internal_server_error"}},
            )
        return ok_response

    with patch.object(client, "_call_api", new_callable=AsyncMock, side_effect=api_side_effect):
        result = await client.call(
            prompt="test",
            template_version="conflict_v1",
            cache_key_extras={"advisor_week_id": "2026-W17", "ticker": "TSM"},
            schema=_Signal,
            model="claude-sonnet-4-6",
        )

    assert result.direction == "long"
    assert call_count == 2  # 1 次失败 + 1 次成功


# ── test: 连续 5 次失败 → LLMUnavailableError ─────────────────────────────────

@pytest.mark.asyncio
async def test_retry_exhausted_raises_llm_unavailable(tmp_path: Path) -> None:
    """
    结论: Sonnet 5 次 + Haiku fallback 5 次全失败后 raise LLMUnavailableError (TECH-7)。
    细节: Sonnet 耗尽 → 自动 fallback Haiku → Haiku 也耗尽 → raise。
          总调用次数 = 5 (Sonnet) + 5 (Haiku) = 10。
    """
    import anthropic

    client = _make_client(tmp_path)
    call_count = 0

    async def always_fail(
        prompt: str, schema: type, model: str, *args: Any, **kwargs: Any
    ) -> Any:
        nonlocal call_count
        call_count += 1
        raise anthropic.APIStatusError(
            message="Internal Server Error",
            response=MagicMock(status_code=500),
            body={"error": {"type": "internal_server_error"}},
        )

    with patch.object(client, "_call_api", new_callable=AsyncMock, side_effect=always_fail):
        with pytest.raises(LLMUnavailableError):
            await client.call(
                prompt="test",
                template_version="conflict_v1",
                cache_key_extras={"advisor_week_id": "2026-W17", "ticker": "TSM"},
                schema=_Signal,
                model="claude-sonnet-4-6",
            )

    # TECH-7: Sonnet 5次 + Haiku fallback 5次 = 10次全部失败才 raise
    assert call_count == 10


# ── test: Sonnet retry 失败 → fallback Haiku 成功 ─────────────────────────────

@pytest.mark.asyncio
async def test_sonnet_exhausted_fallback_to_haiku_succeeds(tmp_path: Path) -> None:
    """结论: Sonnet 5 次失败后，fallback 到 Haiku 成功返回 (TECH-7 + TECH-2 combined)。"""
    import anthropic

    usage_writer = _FakeUsageWriter()
    client = _make_client(tmp_path, usage_writer=usage_writer)

    haiku_response = _make_ok_response(
        {"direction": "neutral", "confidence": 0.5},
        model="claude-haiku-4-5",
    )

    sonnet_call_count = 0
    haiku_call_count = 0

    async def model_dependent(
        prompt: str, schema: type, model: str, *args: Any, **kwargs: Any
    ) -> Any:
        nonlocal sonnet_call_count, haiku_call_count
        if "sonnet" in model:
            sonnet_call_count += 1
            raise anthropic.APIStatusError(
                message="Internal Server Error",
                response=MagicMock(status_code=500),
                body={"error": {"type": "internal_server_error"}},
            )
        else:
            haiku_call_count += 1
            return haiku_response

    with patch.object(client, "_call_api", new_callable=AsyncMock, side_effect=model_dependent):
        result = await client.call(
            prompt="test",
            template_version="conflict_v1",
            cache_key_extras={"advisor_week_id": "2026-W17", "ticker": "TSM"},
            schema=_Signal,
            model="claude-sonnet-4-6",
        )

    # Sonnet 耗尽 5 次，Haiku 成功 1 次
    assert sonnet_call_count == 5
    assert haiku_call_count == 1
    assert result.direction == "neutral"
    # usage 应记录 Haiku model
    assert len(usage_writer.records) == 1
    assert usage_writer.records[0].model == "claude-haiku-4-5"


# ── test: fallback 后 LLMUnavailableError (Haiku 也全失败) ───────────────────

@pytest.mark.asyncio
async def test_haiku_fallback_also_exhausted_raises(tmp_path: Path) -> None:
    """结论: Haiku fallback 也全失败时最终 raise LLMUnavailableError。"""
    import anthropic

    client = _make_client(tmp_path)

    async def always_fail(
        prompt: str, schema: type, model: str, *args: Any, **kwargs: Any
    ) -> Any:
        raise anthropic.APIStatusError(
            message="Service Unavailable",
            response=MagicMock(status_code=503),
            body={"error": {"type": "overloaded_error"}},
        )

    with patch.object(client, "_call_api", new_callable=AsyncMock, side_effect=always_fail):
        with pytest.raises(LLMUnavailableError):
            await client.call(
                prompt="test",
                template_version="conflict_v1",
                cache_key_extras={"advisor_week_id": "2026-W17", "ticker": "TSM"},
                schema=_Signal,
                model="claude-sonnet-4-6",
            )


# ── test: rate limit error (429) 也触发 retry ────────────────────────────────

@pytest.mark.asyncio
async def test_rate_limit_error_triggers_retry(tmp_path: Path) -> None:
    """结论: 429 rate limit 错误也应触发 retry 而非立即失败 (TECH-7)。"""
    import anthropic

    client = _make_client(tmp_path)
    ok_response = _make_ok_response({"direction": "short", "confidence": 0.6})

    call_count = 0

    async def rate_limit_then_ok(
        prompt: str, schema: type, model: str, *args: Any, **kwargs: Any
    ) -> Any:
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            raise anthropic.RateLimitError(
                message="rate limit exceeded",
                response=MagicMock(status_code=429),
                body={},
            )
        return ok_response

    with patch.object(client, "_call_api", new_callable=AsyncMock, side_effect=rate_limit_then_ok):
        result = await client.call(
            prompt="test",
            template_version="conflict_v1",
            cache_key_extras={"advisor_week_id": "2026-W17", "ticker": "TSM"},
            schema=_Signal,
            model="claude-sonnet-4-6",
        )

    assert result.direction == "short"
    assert call_count == 3
