"""
strategy 包 — T007
结论: StrategyModule IDL + 三个 lane 实现 + StrategyRegistry
细节:
  - 仅暴露 IDL 公开接口（base.py Protocol）
  - 三个 lane 平权，互不依赖（R9 解耦）
  - registry 用于 DI 注入，不传给 lane（R3 contract-level 隔离）
"""

from decision_ledger.strategy.base import (
    CustomStrategyModule,
    SourceDataProvider,
    StrategyModule,
)
from decision_ledger.strategy.registry import StrategyRegistry

__all__ = [
    "CustomStrategyModule",
    "SourceDataProvider",
    "StrategyModule",
    "StrategyRegistry",
]
