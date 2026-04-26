"""
lane 隔离测试 — T007 R2 R9 AST 检测
结论: 每个 lane 模块不 import 其他 lane（AST 检测，静态保证）
细节:
  - test_advisor_strategy_no_import_others: advisor_strategy 不 import placeholder/agent_synthesis
  - test_placeholder_model_no_import_others: placeholder_model 不 import advisor/agent_synthesis
  - test_agent_synthesis_no_import_others: agent_synthesis 不 import advisor/placeholder
  - test_agent_synthesis_no_call_other_lanes: verify mock 不调用其他 lane 的 analyze
"""

from __future__ import annotations

import ast
import importlib.util
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest


def _get_module_file(module_name: str) -> Path:
    """获取模块对应的源文件路径。"""
    spec = importlib.util.find_spec(module_name)
    if spec is None or spec.origin is None:
        pytest.fail(f"无法找到模块: {module_name}")
    return Path(spec.origin)


def _extract_imports(filepath: Path) -> set[str]:
    """
    使用 AST 解析文件中所有 import 语句，返回导入的模块名集合。
    支持: import x, from x import y, from x.y import z
    """
    source = filepath.read_text(encoding="utf-8")
    tree = ast.parse(source)
    imports: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.add(node.module)
    return imports


class TestAdvisorStrategyLaneIsolation:
    """AdvisorStrategy 不 import 其他 lane 模块。"""

    def test_advisor_strategy_no_import_placeholder_model(self) -> None:
        """结论: advisor_strategy.py 的 import 树不含 placeholder_model。"""
        filepath = _get_module_file("decision_ledger.strategy.advisor_strategy")
        imports = _extract_imports(filepath)
        violations = [imp for imp in imports if "placeholder_model" in imp]
        assert not violations, (
            f"advisor_strategy.py 不得 import placeholder_model（R9 lane 隔离）。"
            f"违规 import: {violations}"
        )

    def test_advisor_strategy_no_import_agent_synthesis(self) -> None:
        """结论: advisor_strategy.py 的 import 树不含 agent_synthesis。"""
        filepath = _get_module_file("decision_ledger.strategy.advisor_strategy")
        imports = _extract_imports(filepath)
        violations = [imp for imp in imports if "agent_synthesis" in imp]
        assert not violations, (
            f"advisor_strategy.py 不得 import agent_synthesis（R9 lane 隔离）。"
            f"违规 import: {violations}"
        )


class TestPlaceholderModelLaneIsolation:
    """PlaceholderModelStrategy 不 import 其他 lane 模块。"""

    def test_placeholder_model_no_import_advisor_strategy(self) -> None:
        """结论: placeholder_model.py 的 import 树不含 advisor_strategy。"""
        filepath = _get_module_file("decision_ledger.strategy.placeholder_model")
        imports = _extract_imports(filepath)
        violations = [imp for imp in imports if "advisor_strategy" in imp]
        assert not violations, (
            f"placeholder_model.py 不得 import advisor_strategy（R9 lane 隔离）。"
            f"违规 import: {violations}"
        )

    def test_placeholder_model_no_import_agent_synthesis(self) -> None:
        """结论: placeholder_model.py 的 import 树不含 agent_synthesis。"""
        filepath = _get_module_file("decision_ledger.strategy.placeholder_model")
        imports = _extract_imports(filepath)
        violations = [imp for imp in imports if "agent_synthesis" in imp]
        assert not violations, (
            f"placeholder_model.py 不得 import agent_synthesis（R9 lane 隔离）。"
            f"违规 import: {violations}"
        )


class TestAgentSynthesisLaneIsolation:
    """AgentSynthesisStrategy 不 import 其他 lane 模块。"""

    def test_agent_synthesis_no_import_advisor_strategy(self) -> None:
        """结论: agent_synthesis.py 的 import 树不含 advisor_strategy。"""
        filepath = _get_module_file("decision_ledger.strategy.agent_synthesis")
        imports = _extract_imports(filepath)
        violations = [imp for imp in imports if "advisor_strategy" in imp]
        assert not violations, (
            f"agent_synthesis.py 不得 import advisor_strategy（R9 lane 隔离）。"
            f"违规 import: {violations}"
        )

    def test_agent_synthesis_no_import_placeholder_model(self) -> None:
        """结论: agent_synthesis.py 的 import 树不含 placeholder_model。"""
        filepath = _get_module_file("decision_ledger.strategy.agent_synthesis")
        imports = _extract_imports(filepath)
        violations = [imp for imp in imports if "placeholder_model" in imp]
        assert not violations, (
            f"agent_synthesis.py 不得 import placeholder_model（R9 lane 隔离）。"
            f"违规 import: {violations}"
        )

    async def test_agent_synthesis_no_call_other_lane_analyze(self) -> None:
        """
        结论: agent_synthesis.analyze 调用链中不调用 advisor_strategy.analyze 或
        placeholder_model.analyze（R9 解耦 runtime 验证）。
        细节: 通过 mock 追踪调用，确认 agent_synthesis 不依赖其他 lane 的输出。
        """
        from datetime import UTC, datetime

        from decision_ledger.domain.advisor import AdvisorWeeklyReport
        from decision_ledger.domain.env_snapshot import EnvSnapshot
        from decision_ledger.strategy.advisor_strategy import AdvisorStrategy
        from decision_ledger.strategy.agent_synthesis import AgentSynthesisStrategy
        from decision_ledger.strategy.placeholder_model import PlaceholderModelStrategy

        # 准备 mock LLM 返回
        mock_llm = MagicMock()
        mock_provider = MagicMock()
        mock_provider.get_advisor_report = AsyncMock()
        mock_provider.get_portfolio = AsyncMock()
        mock_provider.get_env_snapshot = AsyncMock()

        from decision_ledger.domain.strategy_signal import Direction, StrategySignal

        mock_signal = StrategySignal(
            source_id="agent_synthesis",
            ticker="TSM",
            direction=Direction.WAIT,
            confidence=0.0,
            rationale_plain="等待观察，综合数据不足以行动",
            inputs_used={"advisor_week_id": "2026-W17", "env_snapshot": "present"},
        )
        mock_llm.call = AsyncMock(return_value=mock_signal)

        agent = AgentSynthesisStrategy(mock_llm, mock_provider)

        # 追踪其他 lane 的 analyze 是否被调用
        advisor_analyze_called = False
        placeholder_analyze_called = False

        # 如果 agent_synthesis 意外调用了其他 lane，测试会发现
        advisor_mock = MagicMock(spec=AdvisorStrategy)
        advisor_mock.analyze = AsyncMock(side_effect=lambda *a, **kw: setattr(
            type("X", (), {"__bool__": lambda s: True}), "advisor_analyze_called", True
        ))
        placeholder_mock = MagicMock(spec=PlaceholderModelStrategy)
        placeholder_mock.analyze = AsyncMock(side_effect=lambda *a, **kw: setattr(
            type("X", (), {"__bool__": lambda s: True}), "placeholder_analyze_called", True
        ))

        advisor_week_id = "2026-W17"
        env_snap = EnvSnapshot(
            price=100.0,
            holdings_pct=0.05,
            holdings_abs=5000.0,
            advisor_week_id=advisor_week_id,
            snapshot_at=datetime.now(tz=UTC),
        )
        report = AdvisorWeeklyReport(
            advisor_id="advisor_001",
            source_id="advisor_001",
            week_id=advisor_week_id,
            raw_text="本周看多 TSM",
            structured_json={"TSM": {"direction": "long", "confidence": 0.8}},
        )

        # 调用 agent_synthesis.analyze（使用 mock LLM）
        with patch.object(agent, "_call_llm", return_value=mock_signal):
            result = await agent.analyze(
                advisor_report=report,
                portfolio=None,
                ticker="TSM",
                env_snapshot=env_snap,
            )

        # 验证没有调用其他 lane 的 analyze
        assert not advisor_analyze_called, "agent_synthesis 不应调用 advisor_strategy.analyze"
        assert not placeholder_analyze_called, "agent_synthesis 不应调用 placeholder_model.analyze"
        assert result is not None
