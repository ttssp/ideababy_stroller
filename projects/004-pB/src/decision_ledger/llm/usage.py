"""
LLM 用量记账 Protocol — T005
结论: 定义 LLMUsageWriter Protocol，解耦 T003 (LLMUsageRepository 还未合并)
细节:
  - Protocol 方法: insert(LLMUsage) / monthly_total_cost() -> Decimal
  - 运行时由调用方注入真实 repo (T020 wire)
  - 测试用 fake 实现此 Protocol 即可
  - monthly_cost_usd(): 暴露当前月累积成本，用于 $40 fallback 判断 (TECH-2)
"""

from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING, Protocol, runtime_checkable

if TYPE_CHECKING:
    from decision_ledger.domain.llm_usage import LLMUsage


@runtime_checkable
class LLMUsageWriter(Protocol):
    """
    LLM 用量写入接口 — 与 T003 LLMUsageRepository 解耦。
    T020 注入真实 repo，测试中用 fake 实现。
    """

    async def insert(self, usage: LLMUsage) -> None:
        """写入一条 LLM 调用记录到持久层。"""
        ...

    async def monthly_total_cost(self) -> Decimal:
        """
        返回当前自然月（UTC）的 LLM 累积成本 (美元)。
        用于 TECH-2 mitigation: > $40 自动降级 Sonnet → Haiku。
        """
        ...
