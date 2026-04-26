"""
lane runtime contract 测试 — T007 R3 ⚠️ B3 contract-level 隔离
结论: 通过 inspect.signature 验证每个 lane 的 __init__ 不接受 registry/modules/lanes 参数
细节:
  - test_lane_init_signature_no_registry: 所有 lane __init__ 签名不含禁止参数
  - test_lane_init_only_accepts_llm_and_provider: 实例化时传第三个参数 raise TypeError
  - test_lane_init_no_lane_in_provider: SourceDataProvider 方法名不含 lane 相关字样
  - test_lane_cannot_instantiate_with_registry: 传 registry 关键字参数 raise TypeError
"""

from __future__ import annotations

import inspect
from unittest.mock import AsyncMock, MagicMock

import pytest

from decision_ledger.strategy.advisor_strategy import AdvisorStrategy
from decision_ledger.strategy.agent_synthesis import AgentSynthesisStrategy
from decision_ledger.strategy.base import SourceDataProvider
from decision_ledger.strategy.placeholder_model import PlaceholderModelStrategy

# 所有 lane 类型列表（用于参数化测试）
ALL_LANES = [AdvisorStrategy, PlaceholderModelStrategy, AgentSynthesisStrategy]
ALL_LANE_IDS = ["AdvisorStrategy", "PlaceholderModelStrategy", "AgentSynthesisStrategy"]

# 禁止出现在 __init__ 签名中的参数名
FORBIDDEN_INIT_PARAMS = {"registry", "modules", "lanes", "others"}


@pytest.fixture
def mock_llm() -> MagicMock:
    """Mock LLMClient。"""
    return MagicMock()


@pytest.fixture
def mock_provider() -> MagicMock:
    """Mock SourceDataProvider。"""
    provider = MagicMock()
    provider.get_advisor_report = AsyncMock()
    provider.get_portfolio = AsyncMock()
    provider.get_env_snapshot = AsyncMock()
    provider.get_ticker_meta = AsyncMock()
    return provider


@pytest.mark.parametrize("lane_cls", ALL_LANES, ids=ALL_LANE_IDS)
class TestLaneInitSignatureNoRegistry:
    """验证所有 lane 的 __init__ 不含禁止参数（R3 contract-level 隔离）。"""

    def test_lane_init_signature_no_registry(self, lane_cls: type) -> None:
        """结论: __init__ 不含 'registry' 参数。"""
        sig = inspect.signature(lane_cls.__init__)
        params = set(sig.parameters.keys()) - {"self"}
        forbidden_found = params & FORBIDDEN_INIT_PARAMS
        assert not forbidden_found, (
            f"{lane_cls.__name__}.__init__ 签名含禁止参数: {forbidden_found}。"
            f"R3 contract-level 隔离要求 __init__ 仅接受 (llm_client, source_data_provider)"
        )

    def test_lane_init_only_two_params(self, lane_cls: type) -> None:
        """结论: __init__ 仅接受两个业务参数（llm_client + source_data_provider）。"""
        sig = inspect.signature(lane_cls.__init__)
        # 排除 self
        params = {k: v for k, v in sig.parameters.items() if k != "self"}
        assert len(params) == 2, (
            f"{lane_cls.__name__}.__init__ 应仅有 2 个参数（llm_client + source_data_provider），"
            f"实际: {list(params.keys())}"
        )

    def test_lane_init_has_llm_client(self, lane_cls: type) -> None:
        """结论: __init__ 含 llm_client 参数。"""
        sig = inspect.signature(lane_cls.__init__)
        assert "llm_client" in sig.parameters, (
            f"{lane_cls.__name__}.__init__ 缺少 llm_client 参数"
        )

    def test_lane_init_has_source_data_provider(self, lane_cls: type) -> None:
        """结论: __init__ 含 source_data_provider 参数。"""
        sig = inspect.signature(lane_cls.__init__)
        assert "source_data_provider" in sig.parameters, (
            f"{lane_cls.__name__}.__init__ 缺少 source_data_provider 参数"
        )

    def test_lane_cannot_instantiate_with_registry(
        self,
        lane_cls: type,
        mock_llm: MagicMock,
        mock_provider: MagicMock,
    ) -> None:
        """结论: 传第三个参数（registry）时 raise TypeError，不接受额外参数。"""
        fake_registry = MagicMock(name="FakeRegistry")
        with pytest.raises(TypeError):
            lane_cls(mock_llm, mock_provider, fake_registry)  # type: ignore[call-arg]

    def test_lane_init_third_kwarg_raises(
        self,
        lane_cls: type,
        mock_llm: MagicMock,
        mock_provider: MagicMock,
    ) -> None:
        """结论: 传 registry 关键字参数时 raise TypeError。"""
        with pytest.raises(TypeError):
            lane_cls(  # type: ignore[call-arg]
                mock_llm,
                mock_provider,
                registry=MagicMock(name="FakeRegistry"),
            )


class TestSourceDataProviderNoLaneExposure:
    """验证 SourceDataProvider 不暴露 lane 相关方法（R3 不变量）。"""

    def test_lane_init_no_lane_in_provider(self) -> None:
        """结论: SourceDataProvider dir() 方法名不含 lane/strategy/module/signal 字样。"""
        forbidden_words = {"lane", "strategy", "module", "signal"}
        public_attrs = [
            name for name in dir(SourceDataProvider)
            if not name.startswith("_")
            and name not in {"mro", "register"}
        ]
        violations = []
        for attr in public_attrs:
            for word in forbidden_words:
                if word in attr.lower():
                    violations.append(f"{attr} 含禁止词 '{word}'")
        assert not violations, (
            f"SourceDataProvider 接口暴露了 lane 相关方法，违规: {violations}"
        )
