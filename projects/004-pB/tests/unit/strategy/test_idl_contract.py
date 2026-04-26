"""
IDL contract 锁定测试 — T007
结论: 断言 StrategyModule IDL 仅含 source_id + analyze，不含任何其他方法（TECH-4）
细节:
  - test_protocol_attrs_locked: IDL 公开接口集合锁死，加方法立即失败
  - test_analyze_signature_has_env_snapshot: analyze 必须含 env_snapshot 参数（R2 B3）
  - test_no_extra_methods: 确认不含 conflict_resolve / devil_advocate（R2 D22/D23）
  - test_source_data_provider_no_lane_words: SourceDataProvider 方法名不含禁止词（R3）
"""

from __future__ import annotations

import inspect

from decision_ledger.strategy.base import SourceDataProvider, StrategyModule


class TestStrategyModuleIDLContract:
    """StrategyModule IDL 合同锁定测试。"""

    def test_protocol_attrs_locked(self) -> None:
        """结论: IDL 公开成员集合锁死为 {source_id, analyze}，任何 PR 增删立刻失败。"""
        # 获取 Protocol 定义的成员（排除 Python 内置的 dunder 方法）
        protocol_members = {
            name
            for name in dir(StrategyModule)
            if not name.startswith("_")
            and name not in {"mro", "register"}  # ABC 基础方法
        }

        # 精确锁定：IDL 必须且仅含这两个成员
        expected = {"source_id", "analyze"}
        assert (
            protocol_members == expected
        ), f"IDL 成员集合漂移！期望: {expected}，实际: {protocol_members}"

    def test_no_conflict_resolve(self) -> None:
        """结论: IDL 不含 conflict_resolve（已拆到 T010 ConflictReportAssembler）。"""
        assert not hasattr(StrategyModule, "conflict_resolve"), (
            "IDL 不应含 conflict_resolve — 它在 T010 ConflictReportAssembler，不在 lane"
        )

    def test_no_devil_advocate(self) -> None:
        """结论: IDL 不含 devil_advocate（已拆到 T013 DevilAdvocateService）。"""
        assert not hasattr(StrategyModule, "devil_advocate"), (
            "IDL 不应含 devil_advocate — 它在 T013 DevilAdvocateService，不在 lane"
        )

    def test_analyze_signature_has_env_snapshot(self) -> None:
        """结论: analyze 签名必须含 env_snapshot 参数（R2 B3 修复，IDL 自相矛盾问题）。"""
        sig = inspect.signature(StrategyModule.analyze)
        assert "env_snapshot" in sig.parameters, (
            "analyze 签名缺少 env_snapshot 参数 — R2 B3 修复要求此参数必须在 IDL 中"
        )

    def test_analyze_signature_has_advisor_report(self) -> None:
        """结论: analyze 签名含 advisor_report 参数。"""
        sig = inspect.signature(StrategyModule.analyze)
        assert "advisor_report" in sig.parameters

    def test_analyze_signature_has_portfolio(self) -> None:
        """结论: analyze 签名含 portfolio 参数。"""
        sig = inspect.signature(StrategyModule.analyze)
        assert "portfolio" in sig.parameters

    def test_analyze_signature_has_ticker(self) -> None:
        """结论: analyze 签名含 ticker 参数。"""
        sig = inspect.signature(StrategyModule.analyze)
        assert "ticker" in sig.parameters

    def test_analyze_signature_param_count(self) -> None:
        """结论: analyze 签名参数数量固定（self + 4 个业务参数）。"""
        sig = inspect.signature(StrategyModule.analyze)
        # self + advisor_report + portfolio + ticker + env_snapshot = 5
        assert len(sig.parameters) == 5, (
            f"analyze 参数数量应为 5（self+4），实际: {len(sig.parameters)}，"
            f"参数: {list(sig.parameters.keys())}"
        )


class TestSourceDataProviderContract:
    """SourceDataProvider 接口合同测试（R3 contract-level 隔离）。"""

    def test_no_lane_word_in_methods(self) -> None:
        """结论: SourceDataProvider 公开方法名不含 'lane' 字样（R3 不变量）。"""
        public_methods = [
            name for name in dir(SourceDataProvider)
            if not name.startswith("_")
            and name not in {"mro", "register"}
        ]
        lane_methods = [m for m in public_methods if "lane" in m.lower()]
        assert not lane_methods, (
            f"SourceDataProvider 方法名不得含 'lane'，违规方法: {lane_methods}"
        )

    def test_no_strategy_word_in_methods(self) -> None:
        """结论: SourceDataProvider 公开方法名不含 'strategy' 字样（R3 不变量）。"""
        public_methods = [
            name for name in dir(SourceDataProvider)
            if not name.startswith("_")
            and name not in {"mro", "register"}
        ]
        strategy_methods = [m for m in public_methods if "strategy" in m.lower()]
        assert not strategy_methods, (
            f"SourceDataProvider 方法名不得含 'strategy'，违规方法: {strategy_methods}"
        )

    def test_no_module_word_in_methods(self) -> None:
        """结论: SourceDataProvider 公开方法名不含 'module' 字样（R3 不变量）。"""
        public_methods = [
            name for name in dir(SourceDataProvider)
            if not name.startswith("_")
            and name not in {"mro", "register"}
        ]
        module_methods = [m for m in public_methods if "module" in m.lower()]
        assert not module_methods, (
            f"SourceDataProvider 方法名不得含 'module'，违规方法: {module_methods}"
        )

    def test_no_signal_word_in_methods(self) -> None:
        """结论: SourceDataProvider 公开方法名不含 'signal' 字样（R3 不变量）。"""
        public_methods = [
            name for name in dir(SourceDataProvider)
            if not name.startswith("_")
            and name not in {"mro", "register"}
        ]
        signal_methods = [m for m in public_methods if "signal" in m.lower()]
        assert not signal_methods, (
            f"SourceDataProvider 方法名不得含 'signal'，违规方法: {signal_methods}"
        )

    def test_has_get_advisor_report(self) -> None:
        """结论: SourceDataProvider 具备 get_advisor_report 方法。"""
        assert hasattr(SourceDataProvider, "get_advisor_report")

    def test_has_get_portfolio(self) -> None:
        """结论: SourceDataProvider 具备 get_portfolio 方法。"""
        assert hasattr(SourceDataProvider, "get_portfolio")

    def test_has_get_env_snapshot(self) -> None:
        """结论: SourceDataProvider 具备 get_env_snapshot 方法。"""
        assert hasattr(SourceDataProvider, "get_env_snapshot")
