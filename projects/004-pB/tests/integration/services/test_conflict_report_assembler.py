"""
ConflictReportAssembler 集成测试 — T010
结论: 验证 R10 红线（无 priority/winner/recommended）、R9 解耦、rendered_order_seed 确定性
细节:
  - test_three_signals_present: 输出永远 ≥ 3 signals
  - test_no_divergence_message: 三 signal 全 no_view → root_cause = "暂无分歧"
  - test_no_priority_winner_field: ConflictReport 序列化无 priority/winner/recommended 字段 (R10)
  - test_assembler_no_lane_state_read: assembler 不 import lane 模块 (R9)
  - test_rendered_order_seed_deterministic: 同一 source_ids + day → 同 seed；不同 day → 不同 seed
"""

from __future__ import annotations

import ast
import hashlib
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock

import pytest

from decision_ledger.domain.conflict_report import ConflictReport
from decision_ledger.domain.env_snapshot import EnvSnapshot
from decision_ledger.domain.strategy_signal import Direction, StrategySignal

# ── 测试辅助工厂 ──────────────────────────────────────────


def _make_env_snapshot(advisor_week_id: str = "2026-W17") -> EnvSnapshot:
    """构造测试用 EnvSnapshot。"""
    return EnvSnapshot(
        price=100.0,
        holdings_pct=0.05,
        holdings_abs=5000.0,
        advisor_week_id=advisor_week_id,
        snapshot_at=datetime.now(tz=UTC),
    )


def _make_signal(
    source_id: str,
    ticker: str = "AAPL",
    direction: Direction = Direction.LONG,
    confidence: float = 0.8,
) -> StrategySignal:
    """构造测试用 StrategySignal。"""
    return StrategySignal(
        source_id=source_id,
        ticker=ticker,
        direction=direction,
        confidence=confidence,
        rationale_plain=f"{source_id} 的观点：{direction.value}",
        inputs_used={"advisor_week_id": "2026-W17"},
    )


def _make_no_view_signal(source_id: str, ticker: str = "AAPL") -> StrategySignal:
    """构造 no_view 信号（confidence=0.0）。"""
    return StrategySignal(
        source_id=source_id,
        ticker=ticker,
        direction=Direction.NO_VIEW,
        confidence=0.0,
        rationale_plain=f"{source_id} 无观点",
        inputs_used={},
    )


def _make_llm_client(fake_report_data: dict[str, Any] | None = None) -> Any:
    """创建带 mock LLM 返回的 LLMClient stub。"""
    if fake_report_data is None:
        fake_report_data = {
            "signals": [
                {
                    "source_id": "advisor",
                    "ticker": "AAPL",
                    "direction": "long",
                    "confidence": 0.8,
                    "rationale_plain": "advisor 看多基本面强",
                    "inputs_used": {"advisor_week_id": "2026-W17"},
                },
                {
                    "source_id": "placeholder_model",
                    "ticker": "AAPL",
                    "direction": "neutral",
                    "confidence": 0.5,
                    "rationale_plain": "placeholder 中性观望",
                    "inputs_used": {},
                },
                {
                    "source_id": "agent_synthesis",
                    "ticker": "AAPL",
                    "direction": "wait",
                    "confidence": 0.3,
                    "rationale_plain": "agent_synthesis 建议等待",
                    "inputs_used": {"env_snapshot": "included"},
                },
            ],
            "divergence_root_cause": "advisor 看多但 agent_synthesis 建议等待",
            "has_divergence": True,
        }

    mock_client = AsyncMock()
    # LLMClient.call 返回 ConflictReportLLMOutput pydantic model
    mock_client.call = AsyncMock(return_value=fake_report_data)
    return mock_client


# ── 主测试类 ──────────────────────────────────────────────


class TestConflictReportAssemblerOutputs:
    """ConflictReportAssembler 核心输出测试。"""

    async def test_three_signals_present(self) -> None:
        """结论: assemble() 输出 ConflictReport.signals 始终 ≥ 3 条 (R2 D22 不变量 #2)。"""
        from decision_ledger.services.conflict_report_assembler import (
            ConflictReportAssembler,
        )

        signals = [
            _make_signal("advisor"),
            _make_signal("placeholder_model"),
            _make_signal("agent_synthesis"),
        ]
        env_snapshot = _make_env_snapshot()

        # mock LLM 返回
        mock_llm = AsyncMock()

        from decision_ledger.services.conflict_report_assembler import (
            ConflictReportLLMOutput,
        )

        fake_llm_output = ConflictReportLLMOutput(
            divergence_root_cause="advisor 看多，agent 建议等待",
            has_divergence=True,
        )
        mock_llm.call = AsyncMock(return_value=fake_llm_output)

        assembler = ConflictReportAssembler(llm_client=mock_llm)
        report = await assembler.assemble(signals=signals, env_snapshot=env_snapshot)

        assert isinstance(report, ConflictReport)
        assert len(report.signals) >= 3, f"signals 必须 ≥ 3，当前 {len(report.signals)}"
        # signals 必须是传入的 signals（不丢弃）
        assert len(report.signals) == len(signals)

    async def test_no_divergence_message(self) -> None:
        """结论: 三 signal 全 no_view → divergence_root_cause = '暂无分歧'。"""
        from decision_ledger.services.conflict_report_assembler import (
            ConflictReportAssembler,
            ConflictReportLLMOutput,
        )

        signals = [
            _make_no_view_signal("advisor"),
            _make_no_view_signal("placeholder_model"),
            _make_no_view_signal("agent_synthesis"),
        ]
        env_snapshot = _make_env_snapshot()

        mock_llm = AsyncMock()
        fake_llm_output = ConflictReportLLMOutput(
            divergence_root_cause="暂无分歧",
            has_divergence=False,
        )
        mock_llm.call = AsyncMock(return_value=fake_llm_output)

        assembler = ConflictReportAssembler(llm_client=mock_llm)
        report = await assembler.assemble(signals=signals, env_snapshot=env_snapshot)

        assert report.has_divergence is False
        # 全 no_view 时根因应含"暂无分歧"
        assert "暂无分歧" in report.divergence_root_cause

    async def test_assembler_failure_raises(self) -> None:
        """结论: R3 不变量 #13 — LLM 失败时 raise，不返回 placeholder stub。"""
        from decision_ledger.services.conflict_report_assembler import (
            ConflictReportAssembler,
        )

        signals = [
            _make_signal("advisor"),
            _make_signal("placeholder_model"),
            _make_signal("agent_synthesis"),
        ]
        env_snapshot = _make_env_snapshot()

        mock_llm = AsyncMock()
        mock_llm.call = AsyncMock(side_effect=RuntimeError("LLM 不可用"))

        assembler = ConflictReportAssembler(llm_client=mock_llm)

        # LLM 失败时必须 raise（不返回 no-divergence stub）
        with pytest.raises((RuntimeError, Exception)):
            await assembler.assemble(signals=signals, env_snapshot=env_snapshot)


class TestR10RedLine:
    """R10 红线: ConflictReport 无 priority/winner/recommended 字段。"""

    def test_no_priority_winner_field(self) -> None:
        """结论: R10 红线 — ConflictReport 序列化后无 priority/winner/recommended。

        这是架构红线，不仅仅是文档要求。
        """
        report = ConflictReport(
            signals=[
                _make_signal("advisor"),
                _make_signal("placeholder_model"),
                _make_signal("agent_synthesis"),
            ],
            divergence_root_cause="测试根因",
            has_divergence=True,
            rendered_order_seed=42,
        )

        serialized = report.model_dump()
        serialized_keys = set(serialized.keys())

        forbidden_fields = {"priority", "winner", "recommended"}
        violations = forbidden_fields & serialized_keys
        assert not violations, (
            f"R10 红线违反: ConflictReport 序列化含有禁止字段 {violations}。"
            "priority/winner/recommended 字段绝不允许出现。"
        )

    def test_no_priority_winner_field_in_json(self) -> None:
        """结论: R10 — JSON 字符串中无 priority/winner/recommended 关键词。"""
        report = ConflictReport(
            signals=[
                _make_signal("advisor"),
                _make_signal("placeholder_model"),
                _make_signal("agent_synthesis"),
            ],
            divergence_root_cause="测试根因",
            has_divergence=True,
            rendered_order_seed=42,
        )

        json_str = report.model_dump_json()

        for keyword in ("priority", "winner", "recommended"):
            assert keyword not in json_str, (
                f"R10 红线违反: JSON 输出中含 '{keyword}' 关键词。"
                f"完整 JSON: {json_str}"
            )

    def test_conflict_report_schema_no_forbidden_fields(self) -> None:
        """结论: R10 — ConflictReport JSON schema 定义中无禁止字段。

        检查 properties 字段名(不检整个 schema dict 字符串,后者会含 description)。
        """
        schema = ConflictReport.model_json_schema()
        property_names = set(schema.get("properties", {}).keys())

        for keyword in ("priority", "winner", "recommended"):
            assert keyword not in property_names, (
                f"R10 红线违反: ConflictReport.properties 含 '{keyword}' 字段"
            )


class TestR9Decoupling:
    """R9 解耦: assembler 源码不 import lane 模块。"""

    def test_assembler_no_lane_state_read(self) -> None:
        """结论: R9 — assembler 不 import lane 模块(advisor/placeholder/agent_synthesis)。

        方法: 静态 AST 分析源码文件，检查 import 语句。
        """
        src_path = (
            Path(__file__).parents[3]  # 向上 3 级到 004-pB
            / "src" / "decision_ledger" / "services" / "conflict_report_assembler.py"
        )

        assert src_path.exists(), f"assembler 源文件不存在: {src_path}"

        source_code = src_path.read_text(encoding="utf-8")

        forbidden_modules = {
            "advisor_strategy",
            "placeholder_model",
            "agent_synthesis",
        }

        # AST 分析 import 语句(只查 import,不查 docstring/注释字符串)
        tree = ast.parse(source_code)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    for forbidden in forbidden_modules:
                        assert forbidden not in alias.name, (
                            f"R9 AST 违反: import {alias.name} 含禁止模块 '{forbidden}'"
                        )
            elif isinstance(node, ast.ImportFrom):
                module_name = node.module or ""
                for forbidden in forbidden_modules:
                    assert forbidden not in module_name, (
                        f"R9 AST 违反: from {module_name} import ... 含禁止模块 '{forbidden}'"
                    )


class TestRenderedOrderSeed:
    """rendered_order_seed 确定性测试 (R2 D22)。"""

    def test_rendered_order_seed_deterministic_same_day(self) -> None:
        """结论: 同一组 source_ids + 同一天 → 相同 seed (可复测)。"""
        from decision_ledger.services.conflict_report_assembler import (
            compute_rendered_order_seed,
        )

        source_ids = ["advisor", "placeholder_model", "agent_synthesis"]
        day_str = "2026-04-26"

        seed1 = compute_rendered_order_seed(source_ids, day_str)
        seed2 = compute_rendered_order_seed(source_ids, day_str)

        assert seed1 == seed2, "同一天同一组 source_ids 必须产生相同 seed（确定性）"
        assert 0 <= seed1 < 6, f"seed 必须在 [0, 5] 范围内，当前 {seed1}"

    def test_rendered_order_seed_different_days(self) -> None:
        """结论: 相同 source_ids，不同天 → seed 可能不同（随机化效果）。

        注意: 不要求一定不同（极低概率相同），但应该验证公式正确。
        """
        from decision_ledger.services.conflict_report_assembler import (
            compute_rendered_order_seed,
        )

        source_ids = ["advisor", "placeholder_model", "agent_synthesis"]

        # 验证公式: hash(",".join(sorted(source_ids)) + day_str) % 6
        for day_str in ("2026-04-26", "2026-04-27", "2026-04-28"):
            seed = compute_rendered_order_seed(source_ids, day_str)
            assert 0 <= seed < 6, f"seed 必须在 [0, 5]，day={day_str}, seed={seed}"

        # 验证公式实现与预期一致
        day_str = "2026-04-26"
        expected_input = ",".join(sorted(source_ids)) + day_str
        expected_digest = hashlib.md5(
            expected_input.encode(), usedforsecurity=False
        ).hexdigest()
        expected_seed = int(expected_digest, 16) % 6
        actual_seed = compute_rendered_order_seed(source_ids, day_str)
        assert actual_seed == expected_seed, (
            f"seed 公式不匹配: expected {expected_seed}, got {actual_seed}"
        )

    def test_rendered_order_seed_source_id_order_invariant(self) -> None:
        """结论: source_ids 顺序不影响 seed（因为内部 sorted）。"""
        from decision_ledger.services.conflict_report_assembler import (
            compute_rendered_order_seed,
        )

        source_ids_a = ["advisor", "placeholder_model", "agent_synthesis"]
        source_ids_b = ["agent_synthesis", "advisor", "placeholder_model"]
        day_str = "2026-04-26"

        seed_a = compute_rendered_order_seed(source_ids_a, day_str)
        seed_b = compute_rendered_order_seed(source_ids_b, day_str)

        assert seed_a == seed_b, "source_id 顺序不影响 seed（sorted 后计算）"
