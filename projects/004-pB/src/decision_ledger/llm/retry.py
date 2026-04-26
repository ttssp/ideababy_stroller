"""
LLM 指数退避 retry — T005
结论: 5 次 retry + jitter，失败抛 LLMUnavailableError (TECH-7)
细节:
  - 不使用 tenacity（避免依赖，标准库 asyncio 实现）
  - 指数退避: base_delay * 2^attempt + jitter (0~1s)
  - retry 条件: anthropic.APIStatusError / RateLimitError / APIConnectionError
  - 非重试异常（如 AuthenticationError）立即 raise
  - max_attempts=5，base_delay=1.0s
"""

from __future__ import annotations

import asyncio
import logging
import random
from collections.abc import Awaitable, Callable
from typing import Any, TypeVar

import anthropic

from decision_ledger.llm.errors import LLMUnavailableError

logger = logging.getLogger(__name__)

T = TypeVar("T")

# 触发 retry 的异常类型
_RETRYABLE_EXCEPTIONS = (
    anthropic.APIStatusError,
    anthropic.RateLimitError,
    anthropic.APIConnectionError,
    anthropic.APITimeoutError,
)

_MAX_ATTEMPTS = 5
_BASE_DELAY = 1.0    # 秒
_MAX_DELAY = 30.0    # 秒上限，防止超长等待


async def retry_with_backoff(
    fn: Callable[..., Awaitable[T]],
    *args: Any,
    max_attempts: int = _MAX_ATTEMPTS,
    base_delay: float = _BASE_DELAY,
    **kwargs: Any,
) -> T:
    """
    对 async 函数执行指数退避重试。
    成功返回结果；max_attempts 次全失败抛 LLMUnavailableError。

    退避公式: min(base_delay * 2^attempt, max_delay) + uniform(0, 1) jitter
    """
    last_exc: Exception | None = None

    for attempt in range(max_attempts):
        try:
            return await fn(*args, **kwargs)
        except _RETRYABLE_EXCEPTIONS as exc:
            last_exc = exc
            if attempt < max_attempts - 1:
                delay = min(_BASE_DELAY * (2 ** attempt), _MAX_DELAY)
                jitter = random.uniform(0, 1.0)  # noqa: S311 — 非密码学用途
                total_delay = delay + jitter
                logger.warning(
                    "LLM API 调用失败 (attempt %d/%d): %s — 等待 %.2fs 后重试",
                    attempt + 1,
                    max_attempts,
                    exc,
                    total_delay,
                )
                await asyncio.sleep(total_delay)
            else:
                logger.error(
                    "LLM API 调用 %d 次全部失败: %s",
                    max_attempts,
                    exc,
                )
        except Exception:
            # 非重试异常（如 AuthenticationError / ValidationError）直接 raise
            raise

    raise LLMUnavailableError(
        f"LLM API {max_attempts} 次重试全部失败",
        attempts=max_attempts,
    ) from last_exc
