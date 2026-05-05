"""
StrategySignal 域模型 — T002
结论: 单个 Strategy 实例对一笔潜在决策的判断 (架构 §3.1 IDL)
细节:
  - Direction enum: long/short/neutral/wait/no_view
  - rationale_plain: 必填非空 (不变量 #4 R3 红线: 信号必须有白话解释，不允许黑箱)
  - confidence: 0.0-1.0，0.0 表示没意见 (no_view 时使用)
  - inputs_used: 记录使用的输入 (advisor_week_id / price_at 等)，可追溯
"""

from __future__ import annotations

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, field_validator


class Direction(StrEnum):
    """策略方向枚举 — 对应架构 §3.1 IDL direction 字段。"""

    LONG = "long"        # 看多 / 建仓
    SHORT = "short"      # 看空 / 做空
    NEUTRAL = "neutral"  # 中性 / 持有
    WAIT = "wait"        # 等待入场信号
    NO_VIEW = "no_view"  # 无观点 (PlaceholderModelStrategy 默认，confidence=0.0)


class StrategySignal(BaseModel):
    """单个 Strategy 对一笔潜在决策的判断输出 — 不可变。"""

    model_config = ConfigDict(frozen=True)

    source_id: str          # "advisor" | "placeholder_model" | "agent_synthesis" | future custom
    ticker: str
    direction: Direction
    confidence: float       # 0.0-1.0，0.0 表示没意见
    rationale_plain: str    # 白话解释，不变量 #4: 必须有，禁止黑箱
    inputs_used: dict[str, Any]  # {"advisor_week_id": ..., "price_at": ..., "model_version": ...}

    @field_validator("rationale_plain")
    @classmethod
    def _validate_rationale_plain_nonempty(cls, v: str) -> str:
        """结论: rationale_plain 必须非空 (不变量 #4 R3 红线)。"""
        if not v or not v.strip():
            raise ValueError("rationale_plain 不能为空 — 不允许信号黑箱 (不变量 #4)")
        return v

    @field_validator("confidence")
    @classmethod
    def _validate_confidence_range(cls, v: float) -> float:
        """结论: confidence 必须在 [0.0, 1.0] 区间。"""
        if v < 0.0 or v > 1.0:
            raise ValueError(f"confidence 必须在 0.0-1.0 范围，当前值: {v}")
        return v
