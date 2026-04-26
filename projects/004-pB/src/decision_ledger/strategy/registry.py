"""
StrategyRegistry — T007
结论: lane 注册中心，build_default 工厂方法 + FastAPI Depends-style get_registry
细节:
  - register(): 注册 lane，重复 source_id raise ValueError（R9 唯一性约束）
  - get_all(): 返回列表副本（防外部修改内部状态）
  - get_by_source_id(): 按 source_id 查找，未找到返回 None
  - register_custom(): D7 扩展位，注册自定义 lane
  - build_default(): 工厂方法，包含三个标准 lane（advisor / placeholder_model / agent_synthesis）
  - get_registry(): FastAPI Depends-style 工厂函数
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from decision_ledger.llm.client import LLMClient
    from decision_ledger.strategy.base import SourceDataProvider, StrategyModule


class StrategyRegistry:
    """
    结论: lane 注册中心，维护所有激活的 StrategyModule 实例。
    细节:
      - R3 contract-level 隔离: registry 不传给 lane（lane 的 __init__ 不接受 registry）
      - R9 唯一性约束: 相同 source_id 的 lane 不允许重复注册
      - get_all() 返回副本，防止外部修改内部状态（防御性设计）
    """

    def __init__(self) -> None:
        """初始化空 registry。"""
        self._lanes: dict[str, StrategyModule] = {}

    def register(self, lane: StrategyModule) -> None:
        """
        结论: 注册 lane，重复 source_id raise ValueError。
        细节: R9 唯一性约束，防止静默覆盖导致不一致状态。
        """
        source_id = lane.source_id
        if source_id in self._lanes:
            raise ValueError(
                f"source_id '{source_id}' already registered in StrategyRegistry. "
                f"重复注册同一 lane 可能导致不一致状态（R9 唯一性约束）。"
            )
        self._lanes[source_id] = lane

    def register_custom(self, lane: Any) -> None:
        """
        结论: D7 扩展位 — 注册自定义 lane（v0.5+ human 私有 ML 模型）。
        细节: 同样不允许重复 source_id（复用 register 逻辑）。
        """
        self.register(lane)

    def get_all(self) -> list[StrategyModule]:
        """
        结论: 返回所有注册 lane 的列表副本。
        细节: 返回副本防止外部修改影响内部状态（防御性设计）。
        """
        return list(self._lanes.values())

    def get_by_source_id(self, source_id: str) -> StrategyModule | None:
        """
        结论: 按 source_id 查找 lane，未找到返回 None（不 raise）。
        细节: 调用方负责处理 None 情况（上游 pipeline 逻辑）。
        """
        return self._lanes.get(source_id)

    @classmethod
    def build_default(
        cls,
        llm_client: LLMClient,
        source_data_provider: SourceDataProvider,
    ) -> StrategyRegistry:
        """
        结论: 工厂方法，构建包含三个标准 lane 的 registry。
        细节:
          - advisor: 咨询师观点 lane
          - placeholder_model: 占位 lane（v0.4，v0.5+ 替换）
          - agent_synthesis: 综合分析 lane（R6 反诱导）
          - R3 contract-level 隔离: lane 初始化时不传 registry
        """
        from decision_ledger.strategy.advisor_strategy import AdvisorStrategy
        from decision_ledger.strategy.agent_synthesis import AgentSynthesisStrategy
        from decision_ledger.strategy.placeholder_model import PlaceholderModelStrategy

        registry = cls()
        registry.register(AdvisorStrategy(llm_client, source_data_provider))
        registry.register(PlaceholderModelStrategy(llm_client, source_data_provider))
        registry.register(AgentSynthesisStrategy(llm_client, source_data_provider))
        return registry


def get_registry(
    llm_client: LLMClient,
    source_data_provider: SourceDataProvider,
) -> StrategyRegistry:
    """
    结论: FastAPI Depends-style 工厂函数，返回默认 StrategyRegistry。
    细节:
      - 与 build_default 等价，提供函数式接口（FastAPI DI 友好）
      - 调用方可通过 Depends(get_registry_factory()) 注入
    """
    return StrategyRegistry.build_default(llm_client, source_data_provider)
