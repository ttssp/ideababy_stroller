"""
LLMClient — T005 核心
结论: 统一 LLM 调用入口，所有调用必须经此层 (架构不变量 §9.8)
细节:
  - async 接口 (D19)，内部 asyncio.to_thread 隔离 sync SDK (TECH-5)
  - call() 顺序: cache.get → (miss) retry(call_api) → schema validate → usage.record → cache.put
  - 月成本 > $40 自动降级 Sonnet → Haiku (TECH-2)
  - API key 日志 redact: sk-ant-*** (SEC-3)
  - Anthropic tool use 强制 structured output (SEC-4)
  - Sonnet 5次失败 → fallback Haiku (TECH-7)
"""

from __future__ import annotations

import asyncio
import logging
import uuid
from datetime import UTC, datetime
from decimal import Decimal
from pathlib import Path
from typing import Any, TypeVar

import anthropic
from pydantic import BaseModel, ValidationError

from decision_ledger.domain.llm_usage import LLMUsage
from decision_ledger.llm.cache import LLMCache
from decision_ledger.llm.errors import LLMSchemaError, LLMUnavailableError
from decision_ledger.llm.retry import retry_with_backoff
from decision_ledger.llm.usage import LLMUsageWriter

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)

# 成本阈值：超过此值自动降级 Sonnet → Haiku (TECH-2 mitigation)
_MONTHLY_COST_FALLBACK_THRESHOLD = Decimal("40.0")

# 模型别名（解耦具体模型 ID，方便后续升版）
_SONNET_MODEL = "claude-sonnet-4-6"
_HAIKU_MODEL = "claude-haiku-4-5"

# Sonnet → Haiku fallback 映射
_FALLBACK_MODEL: dict[str, str] = {
    _SONNET_MODEL: _HAIKU_MODEL,
}

# token 成本估算（$/1k tokens），用于 LLMUsage.cost_usd 计算
_COST_PER_1K_INPUT: dict[str, float] = {
    _SONNET_MODEL: 0.003,
    _HAIKU_MODEL: 0.00025,
}
_COST_PER_1K_OUTPUT: dict[str, float] = {
    _SONNET_MODEL: 0.015,
    _HAIKU_MODEL: 0.00125,
}


def _redact_api_key(key: str) -> str:
    """
    SEC-3: API key 日志 redact。
    输入: sk-ant-api03-xxx... → 输出: sk-ant-***
    任何 sk-ant- 前缀的字符串，只保留前缀。
    """
    if key.startswith("sk-ant-"):
        return "sk-ant-***"
    return "***"


def _estimate_cost(model: str, input_tokens: int, output_tokens: int) -> float:
    """估算 LLM 调用成本 (美元)。"""
    in_cost = _COST_PER_1K_INPUT.get(model, 0.003) * input_tokens / 1000
    out_cost = _COST_PER_1K_OUTPUT.get(model, 0.015) * output_tokens / 1000
    return round(in_cost + out_cost, 6)


class LLMClient:
    """
    LLM 调用统一入口。

    使用方式:
        client = LLMClient(api_key=..., usage_writer=repo, cache_dir=Path(...))
        result: MySchema = await client.call(
            prompt="...",
            template_version="conflict_v1",
            cache_key_extras={"advisor_week_id": "2026-W17", "ticker": "TSM"},
            schema=MySchema,
        )
    """

    def __init__(
        self,
        api_key: str,
        usage_writer: LLMUsageWriter,
        cache_dir: Path | None = None,
        service_name: str = "LLMClient",
    ) -> None:
        # SEC-3: API key 不出现在日志
        logger.debug("LLMClient 初始化 (api_key=%s)", _redact_api_key(api_key))
        self._api_key = api_key
        self._usage_writer = usage_writer
        self._cache = LLMCache(cache_dir=cache_dir)
        self._service_name = service_name

    # ── 主入口 ────────────────────────────────────────────────────────────────

    async def call(
        self,
        prompt: str,
        *,
        template_version: str,
        cache_key_extras: dict[str, str],
        schema: type[T],
        model: str = _SONNET_MODEL,
    ) -> T:
        """
        统一 LLM 调用接口 (D19 async)。

        顺序:
          1. 检查月成本是否超 $40 → 自动降级 model (TECH-2)
          2. cache.get → 命中: 记 usage(cache_hit=True, cost=0) → 返回
          3. cache miss → retry(call_api) with fallback → schema validate
          4. usage.record (cache_hit=False, 真实 token)
          5. cache.put

        Args:
            prompt: 已渲染的 prompt 文本
            template_version: prompt 模板版本，如 "conflict_v1"（必须含，D11）
            cache_key_extras: 构成 cache key 的额外字段，必须含 advisor_week_id + ticker
            schema: pydantic model 类，用于 tool use schema + 结果验证 (SEC-4)
            model: 目标模型，默认 Sonnet 4.6；月成本超 $40 时自动降为 Haiku

        Returns:
            schema 实例

        Raises:
            LLMSchemaError: API 返回数据不符合 schema (SEC-4)
            LLMUnavailableError: 5 次 retry + fallback 全部失败
        """
        advisor_week_id = cache_key_extras.get("advisor_week_id", "")
        ticker = cache_key_extras.get("ticker", "")

        # 步骤 1: 月成本超 $40 → 自动降级
        effective_model = await self._resolve_model(model)

        start_ns = asyncio.get_event_loop().time()

        # 步骤 2: cache 查询
        cached = self._cache.get(
            advisor_week_id=advisor_week_id,
            ticker=ticker,
            prompt_template_version=template_version,
            model=effective_model,
        )

        if cached is not None:
            logger.debug("缓存命中: ticker=%s, version=%s", ticker, template_version)
            # cache hit: 记录 usage (cost=0, cache_hit=True)
            await self._record_usage(
                model=effective_model,
                template_version=template_version,
                input_tokens=0,
                output_tokens=0,
                cost_usd=0.0,
                cache_hit=True,
                latency_ms=self._elapsed_ms(start_ns),
            )
            try:
                return schema(**cached)
            except ValidationError as e:
                raise LLMSchemaError(
                    f"缓存数据不符合 schema {schema.__name__}: {e}",
                    raw_data=cached,
                ) from e

        # 步骤 3: cache miss → 调用 API (含 retry + fallback)
        response = await self._call_with_retry_and_fallback(
            prompt=prompt,
            schema=schema,
            model=effective_model,
        )

        # 步骤 4: 解析 tool_use block
        tool_data = self._extract_tool_data(response)

        # 步骤 5: pydantic validate (SEC-4)
        try:
            result = schema(**tool_data)
        except ValidationError as e:
            raise LLMSchemaError(
                f"API 返回数据不符合 schema {schema.__name__}: {e}",
                raw_data=tool_data,
            ) from e

        # 步骤 6: 记录 usage
        actual_model = getattr(response, "model", effective_model) or effective_model
        input_tokens = response.usage.input_tokens
        output_tokens = response.usage.output_tokens
        cost = _estimate_cost(actual_model, input_tokens, output_tokens)

        await self._record_usage(
            model=actual_model,
            template_version=template_version,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cost_usd=cost,
            cache_hit=False,
            latency_ms=self._elapsed_ms(start_ns),
        )

        # 步骤 7: cache.put (用 actual_model 的 cache key)
        self._cache.put(
            advisor_week_id=advisor_week_id,
            ticker=ticker,
            prompt_template_version=template_version,
            model=effective_model,
            data=tool_data,
        )

        return result

    # ── 内部工具 ──────────────────────────────────────────────────────────────

    async def _resolve_model(self, requested_model: str) -> str:
        """
        TECH-2: 检查月成本，超 $40 自动降级 Sonnet → Haiku。
        注意: 月成本统计在 cache 查询之前。
        """
        monthly_cost = await self._usage_writer.monthly_total_cost()
        if monthly_cost >= _MONTHLY_COST_FALLBACK_THRESHOLD:
            fallback = _FALLBACK_MODEL.get(requested_model)
            if fallback:
                logger.info(
                    "月成本 $%.2f 超阈值 $%.2f，自动降级: %s → %s",
                    monthly_cost,
                    _MONTHLY_COST_FALLBACK_THRESHOLD,
                    requested_model,
                    fallback,
                )
                return fallback
        return requested_model

    async def _call_with_retry_and_fallback(
        self,
        prompt: str,
        schema: type[T],
        model: str,
    ) -> Any:
        """
        TECH-7: 先对主模型 retry 5 次，失败后 fallback 到 Haiku 再 retry 5 次。
        双层都失败 → LLMUnavailableError。
        """
        try:
            return await retry_with_backoff(
                self._call_api,
                prompt,
                schema,
                model,
            )
        except LLMUnavailableError:
            fallback_model = _FALLBACK_MODEL.get(model)
            if fallback_model and fallback_model != model:
                logger.warning(
                    "主模型 %s 耗尽 retry，fallback 到 %s",
                    model,
                    fallback_model,
                )
                return await retry_with_backoff(
                    self._call_api,
                    prompt,
                    schema,
                    fallback_model,
                )
            raise

    async def _call_api(
        self,
        prompt: str,
        schema: type[BaseModel],
        model: str,
    ) -> Any:
        """
        封装 anthropic SDK 同步调用 → asyncio.to_thread (TECH-5)。
        使用 Anthropic tool use 强制 structured output (SEC-4)。
        API key 不出现在日志 (SEC-3)。
        """
        logger.debug(
            "调用 Anthropic API: model=%s, api_key=%s",
            model,
            _redact_api_key(self._api_key),
        )

        # 构造 tool schema (SEC-4: 强制 structured output)
        tool_def = _build_tool_schema(schema)

        def _sync_call() -> Any:
            """同步调用，在 thread 中执行。"""
            sdk_client = anthropic.Anthropic(api_key=self._api_key)
            # dict literals 与 ToolParam/ToolChoiceAnyParam TypedDict 运行时兼容，
            # 但 mypy 无法通过 overload 解析确认 → 抑制 call-overload 错误
            return sdk_client.messages.create(  # type: ignore[call-overload]
                model=model,
                max_tokens=2048,
                tools=[tool_def],
                tool_choice={"type": "any"},
                messages=[{"role": "user", "content": prompt}],
            )

        # TECH-5: asyncio.to_thread 隔离同步阻塞
        return await asyncio.to_thread(_sync_call)

    @staticmethod
    def _extract_tool_data(response: Any) -> dict[str, Any]:
        """
        从 anthropic 响应中提取 tool_use block 数据。
        SEC-4: 期望 tool_use 类型，不接受 free-form text。
        """
        for block in response.content:
            if getattr(block, "type", None) == "tool_use":
                return dict(block.input)
        # 没有 tool_use block（API 可能返回纯文本） → schema 错误
        raise LLMSchemaError(
            "API 响应缺少 tool_use block（SEC-4: 不接受 free-form 输出）",
            raw_data=response.content,
        )

    async def _record_usage(
        self,
        *,
        model: str,
        template_version: str,
        input_tokens: int,
        output_tokens: int,
        cost_usd: float,
        cache_hit: bool,
        latency_ms: int,
    ) -> None:
        """记录 LLMUsage 到持久层（架构 §10 M4 schema）。"""
        usage = LLMUsage(
            call_id=str(uuid.uuid4()),
            service=self._service_name,
            model=model,
            prompt_template_version=template_version,
            prompt_tokens=input_tokens,
            output_tokens=output_tokens,
            cost_usd=cost_usd,
            cache_hit=cache_hit,
            latency_ms=latency_ms,
            created_at=datetime.now(tz=UTC),
        )
        try:
            await self._usage_writer.insert(usage)
        except Exception as e:
            # usage 记录失败不阻断主流程，但要记日志
            logger.error("LLM usage 记录失败 (不阻断主流程): %s", e)

    @staticmethod
    def _elapsed_ms(start: float) -> int:
        """计算从 start (event_loop.time()) 到现在的毫秒数。"""
        elapsed = asyncio.get_event_loop().time() - start
        return max(0, int(elapsed * 1000))


def _build_tool_schema(schema: type[BaseModel]) -> dict[str, Any]:
    """
    从 pydantic model 生成 Anthropic tool use schema。
    SEC-4: 强制 structured output，不接受 free-form text。
    """
    json_schema = schema.model_json_schema()
    return {
        "name": schema.__name__,
        "description": schema.__doc__ or f"返回 {schema.__name__} 格式数据",
        "input_schema": json_schema,
    }
