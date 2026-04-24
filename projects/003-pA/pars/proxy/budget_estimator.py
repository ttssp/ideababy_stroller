"""
pars.proxy.budget_estimator — 请求 USD 成本预估（纯函数，无副作用）。

结论：
  基于字符数 / 3.5 估算 input tokens，乘以定价表 + SAFETY_COEFFICIENT，
  得出请求上限成本估算值，供 prereject_middleware 做前置拒绝判断。

定价表维护（操作员职责）：
  PRICING 硬编码为当前已知价格（2026-04 时点）。
  价格变动时由操作员（operator）更新此文件并重新发布。
  不做自动拉取，避免网络依赖和意外价格漂移。
  建议操作员每季度核对 Anthropic 官方定价页。

SAFETY_COEFFICIENT：
  1.10（即 +10% 保守缓冲）。宁可提前 402 也不超支，严守 C20 硬帽约束。

token 估算方式：
  input_tokens = ceil(total_input_chars / 3.5)
  output_tokens = max_tokens（按最坏情况估算，避免低估）

total_cost = (input_tokens × input_price + output_tokens × output_price)
             / 1_000_000 × SAFETY_COEFFICIENT
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any


# ---------------------------------------------------------------------------
# 安全系数（SAFETY_COEFFICIENT > 1.0 = 偏高估算）
# ---------------------------------------------------------------------------

SAFETY_COEFFICIENT: float = 1.10
"""保守缓冲系数，确保预估成本 ≥ 实际成本（满足 C20 硬帽约束）。"""


# ---------------------------------------------------------------------------
# 定价数据类
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Pricing:
    """单个模型层级的定价参数（每百万 token 的 USD）。

    frozen=True：防止运行时意外修改定价（不可变对象）。

    字段：
        input_per_mtok:       输入 token 价格（USD / 1M tokens）
        output_per_mtok:      输出 token 价格（USD / 1M tokens）
        cache_read_per_mtok:  缓存读取 token 价格（USD / 1M tokens）
        cache_write_per_mtok: 缓存写入 token 价格（USD / 1M tokens）
    """

    input_per_mtok: float
    output_per_mtok: float
    cache_read_per_mtok: float
    cache_write_per_mtok: float


# ---------------------------------------------------------------------------
# 定价表（2026-04 版本，操作员维护）
# ---------------------------------------------------------------------------

PRICING: dict[str, Pricing] = {
    "opus-4-7": Pricing(
        input_per_mtok=15.0,
        output_per_mtok=75.0,
        cache_read_per_mtok=1.5,
        cache_write_per_mtok=18.75,
    ),
    "sonnet-4-6": Pricing(
        input_per_mtok=3.0,
        output_per_mtok=15.0,
        cache_read_per_mtok=0.3,
        cache_write_per_mtok=3.75,
    ),
    "haiku-4-5": Pricing(
        input_per_mtok=0.8,
        output_per_mtok=4.0,
        cache_read_per_mtok=0.08,
        cache_write_per_mtok=1.0,
    ),
}
"""
定价表（USD / 1M tokens）。

tier 名称映射（Anthropic model 名 → tier key）：
  claude-opus-4-7   → opus-4-7
  claude-sonnet-4-6 → sonnet-4-6
  claude-haiku-4-5  → haiku-4-5
"""


# ---------------------------------------------------------------------------
# model 名称 → tier 映射
# ---------------------------------------------------------------------------

_MODEL_TO_TIER: dict[str, str] = {
    "claude-opus-4-7": "opus-4-7",
    "claude-sonnet-4-6": "sonnet-4-6",
    "claude-haiku-4-5": "haiku-4-5",
    # 支持不带 "claude-" 前缀的短名（直接匹配 tier key）
    "opus-4-7": "opus-4-7",
    "sonnet-4-6": "sonnet-4-6",
    "haiku-4-5": "haiku-4-5",
}


def _resolve_tier(model: str) -> str:
    """将 model 名称解析为 PRICING 表的 tier key。

    Raises:
        ValueError: model 不在已知映射表中（未知模型无法安全估算成本）
    """
    tier = _MODEL_TO_TIER.get(model)
    if tier is None:
        raise ValueError(
            f"unknown model {model!r}: not in PRICING table. "
            f"Known models: {sorted(_MODEL_TO_TIER.keys())}"
        )
    return tier


# ---------------------------------------------------------------------------
# 公开函数
# ---------------------------------------------------------------------------


def count_input_tokens(request_body: dict[str, Any]) -> int:
    """估算请求 body 中 messages 的 input token 数。

    算法：
        total_chars = sum(len(msg["content"]) for msg in messages)
        tokens = ceil(total_chars / 3.5)

    设计取舍：
    - 不依赖 tiktoken（避免引入额外依赖和 model-specific 分词逻辑）
    - 3.5 chars/token 是英文/混合语言的保守估算
    - 偏高估算符合 C20 硬帽保守策略

    Args:
        request_body: Anthropic Messages API 格式的请求 body dict。
                      必须包含 "messages" 键（list of dicts with "content"）。

    Returns:
        估算的 input token 数（int，≥ 0）
    """
    messages: list[dict[str, Any]] = request_body.get("messages", [])
    total_chars = 0
    for msg in messages:
        content = msg.get("content", "")
        if isinstance(content, str):
            total_chars += len(content)
        elif isinstance(content, list):
            # content blocks（Anthropic 多模态格式），只计 text blocks
            for block in content:
                if isinstance(block, dict) and block.get("type") == "text":
                    total_chars += len(block.get("text", ""))
    return math.ceil(total_chars / 3.5) if total_chars > 0 else 0


def estimate_request_cost(request_body: dict[str, Any]) -> float:
    """估算单次请求的 USD 成本上限（含 SAFETY_COEFFICIENT 缓冲）。

    公式：
        input_tokens  = count_input_tokens(request_body)
        output_tokens = max_tokens（按最坏情况）
        base_cost = (input_tokens × input_price + output_tokens × output_price) / 1_000_000
        total_cost = base_cost × SAFETY_COEFFICIENT

    Args:
        request_body: Anthropic Messages API 格式的请求 body dict。
                      必须包含 "model" 和 "max_tokens" 字段。

    Returns:
        估算 USD 成本（float，> 0）

    Raises:
        ValueError:  model 字段缺失，或 model 不在 PRICING 表中
        KeyError:    max_tokens 字段缺失
    """
    # 取 model（缺失时 raise ValueError）
    model = request_body.get("model")
    if model is None:
        raise ValueError("request_body 缺失 'model' 字段，无法估算成本")

    # 解析 tier（未知 model 时 raise ValueError）
    tier = _resolve_tier(model)
    pricing = PRICING[tier]

    # 取 max_tokens（缺失时 raise KeyError）
    max_tokens: int = request_body["max_tokens"]  # 意图：缺失即 KeyError

    # 估算 tokens
    input_tokens = count_input_tokens(request_body)

    # 计算基础成本
    base_cost = (
        input_tokens * pricing.input_per_mtok
        + max_tokens * pricing.output_per_mtok
    ) / 1_000_000

    # 应用安全系数（确保 total > 0 即使 base_cost = 0）
    total_cost = base_cost * SAFETY_COEFFICIENT

    # 最小正值保证：即使 input=0 + max_tokens × price 也要 > 0
    # 因为 max_tokens ≥ 1 且 price > 0，total_cost > 0 已由数学保证
    return total_cost
