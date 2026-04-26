"""
StrategyRegistry 测试 — T007
结论: register/get_all/重复 source_id 报错/FastAPI DI 风格 get_registry
细节:
  - test_register_and_get_all: 注册三个 lane 后 get_all() 返回三个实例
  - test_duplicate_source_id_raises: 同 source_id 注册两次 raise ValueError
  - test_get_by_source_id: 按 source_id 查找 lane 实例
  - test_register_custom: register_custom 扩展点可注册自定义 lane
  - test_get_registry_factory: get_registry() 工厂函数可用于 FastAPI Depends
"""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest

from decision_ledger.strategy.registry import StrategyRegistry


@pytest.fixture
def mock_llm() -> MagicMock:
    return MagicMock()


@pytest.fixture
def mock_provider() -> MagicMock:
    provider = MagicMock()
    provider.get_advisor_report = AsyncMock()
    provider.get_portfolio = AsyncMock()
    provider.get_env_snapshot = AsyncMock()
    provider.get_ticker_meta = AsyncMock(return_value={})
    return provider


@pytest.fixture
def registry(mock_llm: MagicMock, mock_provider: MagicMock) -> StrategyRegistry:
    """默认包含三个标准 lane 的 registry。"""
    return StrategyRegistry.build_default(mock_llm, mock_provider)


class TestStrategyRegistryBuildDefault:
    """build_default 工厂方法测试。"""

    def test_build_default_returns_registry(
        self, mock_llm: MagicMock, mock_provider: MagicMock
    ) -> None:
        """结论: build_default 返回 StrategyRegistry 实例。"""
        reg = StrategyRegistry.build_default(mock_llm, mock_provider)
        assert isinstance(reg, StrategyRegistry)

    def test_build_default_has_three_lanes(
        self, mock_llm: MagicMock, mock_provider: MagicMock
    ) -> None:
        """结论: build_default 包含 advisor / placeholder_model / agent_synthesis 三个 lane。"""
        reg = StrategyRegistry.build_default(mock_llm, mock_provider)
        all_lanes = reg.get_all()
        source_ids = {lane.source_id for lane in all_lanes}
        assert source_ids == {"advisor", "placeholder_model", "agent_synthesis"}, (
            f"build_default 应包含三个标准 lane，实际 source_id: {source_ids}"
        )

    def test_build_default_has_exactly_three_lanes(
        self, mock_llm: MagicMock, mock_provider: MagicMock
    ) -> None:
        """结论: build_default 恰好有三个 lane，不多不少。"""
        reg = StrategyRegistry.build_default(mock_llm, mock_provider)
        assert len(reg.get_all()) == 3


class TestStrategyRegistryGetAll:
    """get_all() 测试。"""

    def test_get_all_returns_list(self, registry: StrategyRegistry) -> None:
        """结论: get_all() 返回列表类型。"""
        result = registry.get_all()
        assert isinstance(result, list)

    def test_get_all_elements_have_source_id(self, registry: StrategyRegistry) -> None:
        """结论: get_all() 中每个元素都有 source_id 属性。"""
        for lane in registry.get_all():
            assert hasattr(lane, "source_id"), f"lane {lane} 缺少 source_id 属性"

    def test_get_all_elements_have_analyze(self, registry: StrategyRegistry) -> None:
        """结论: get_all() 中每个元素都有 analyze 方法（符合 StrategyModule 协议）。"""
        for lane in registry.get_all():
            assert callable(getattr(lane, "analyze", None)), (
                f"lane {lane.source_id} 缺少 callable analyze 方法"
            )

    def test_get_all_returns_copy(self, registry: StrategyRegistry) -> None:
        """结论: get_all() 返回副本，防止外部修改内部状态。"""
        result1 = registry.get_all()
        result1.append(MagicMock())
        result2 = registry.get_all()
        assert len(result2) == 3, "get_all() 应返回列表副本，不允许外部修改内部状态"


class TestStrategyRegistryGetBySourceId:
    """get_by_source_id() 测试。"""

    def test_get_advisor_lane(self, registry: StrategyRegistry) -> None:
        """结论: 按 'advisor' 查找返回正确 lane。"""
        lane = registry.get_by_source_id("advisor")
        assert lane is not None
        assert lane.source_id == "advisor"

    def test_get_placeholder_model_lane(self, registry: StrategyRegistry) -> None:
        """结论: 按 'placeholder_model' 查找返回正确 lane。"""
        lane = registry.get_by_source_id("placeholder_model")
        assert lane is not None
        assert lane.source_id == "placeholder_model"

    def test_get_agent_synthesis_lane(self, registry: StrategyRegistry) -> None:
        """结论: 按 'agent_synthesis' 查找返回正确 lane。"""
        lane = registry.get_by_source_id("agent_synthesis")
        assert lane is not None
        assert lane.source_id == "agent_synthesis"

    def test_get_nonexistent_returns_none(self, registry: StrategyRegistry) -> None:
        """结论: 查找不存在的 source_id 返回 None（不 raise）。"""
        result = registry.get_by_source_id("nonexistent_lane_xyz")
        assert result is None


class TestStrategyRegistryDuplicateSourceId:
    """重复 source_id 注册测试（R9 唯一性约束）。"""

    def test_duplicate_source_id_raises_value_error(
        self, mock_llm: MagicMock, mock_provider: MagicMock
    ) -> None:
        """结论: 注册同名 source_id 时 raise ValueError（防止静默覆盖）。"""
        from decision_ledger.strategy.advisor_strategy import AdvisorStrategy

        reg = StrategyRegistry()
        lane1 = AdvisorStrategy(mock_llm, mock_provider)
        lane2 = AdvisorStrategy(mock_llm, mock_provider)

        reg.register(lane1)
        with pytest.raises(
            ValueError, match="source_id.*already.*registered|already.*registered|重复"
        ):
            reg.register(lane2)

    def test_first_registration_succeeds(
        self, mock_llm: MagicMock, mock_provider: MagicMock
    ) -> None:
        """结论: 首次注册不会 raise。"""
        from decision_ledger.strategy.advisor_strategy import AdvisorStrategy

        reg = StrategyRegistry()
        lane = AdvisorStrategy(mock_llm, mock_provider)
        reg.register(lane)  # Should not raise
        assert reg.get_by_source_id("advisor") is not None


class TestStrategyRegistryRegisterCustom:
    """register_custom 扩展点测试（D7 v0.5+ 位）。"""

    def test_register_custom_lane(
        self, registry: StrategyRegistry
    ) -> None:
        """结论: register_custom 可注册任意符合协议的 lane。"""
        mock_custom = MagicMock()
        mock_custom.source_id = "custom_private_v1"
        mock_custom.analyze = AsyncMock()

        registry.register_custom(mock_custom)
        found = registry.get_by_source_id("custom_private_v1")
        assert found is not None
        assert found.source_id == "custom_private_v1"

    def test_register_custom_appears_in_get_all(
        self, registry: StrategyRegistry
    ) -> None:
        """结论: register_custom 注册后出现在 get_all() 列表中。"""
        mock_custom = MagicMock()
        mock_custom.source_id = "custom_ml_v2"
        mock_custom.analyze = AsyncMock()

        registry.register_custom(mock_custom)
        all_lanes = registry.get_all()
        source_ids = {lane.source_id for lane in all_lanes}
        assert "custom_ml_v2" in source_ids

    def test_register_custom_duplicate_raises(
        self, registry: StrategyRegistry
    ) -> None:
        """结论: register_custom 也不允许重复 source_id。"""
        mock_custom1 = MagicMock()
        mock_custom1.source_id = "custom_dup_test"
        mock_custom1.analyze = AsyncMock()

        mock_custom2 = MagicMock()
        mock_custom2.source_id = "custom_dup_test"
        mock_custom2.analyze = AsyncMock()

        registry.register_custom(mock_custom1)
        with pytest.raises(ValueError):
            registry.register_custom(mock_custom2)


class TestStrategyRegistryFactoryFunction:
    """get_registry() 工厂函数测试（FastAPI Depends 风格）。"""

    def test_get_registry_factory_exists(self) -> None:
        """结论: get_registry 工厂函数存在于 registry 模块。"""
        from decision_ledger.strategy.registry import get_registry
        assert callable(get_registry)

    def test_get_registry_factory_returns_registry(
        self, mock_llm: MagicMock, mock_provider: MagicMock
    ) -> None:
        """结论: get_registry(llm, provider) 返回 StrategyRegistry 实例。"""
        from decision_ledger.strategy.registry import get_registry
        reg = get_registry(mock_llm, mock_provider)
        assert isinstance(reg, StrategyRegistry)
