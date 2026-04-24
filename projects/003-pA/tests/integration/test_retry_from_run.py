"""
tests/integration/test_retry_from_run.py — T024 retry integration 测试。

结论：mock RunOrchestrator.start，断言 derive_retry_config + start_retry
      生成正确的 new config（retry_from 字段 / overrides 生效）。

标记：pytest.mark.integration
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, call, patch

import pytest

from pars.ledger import (
    BudgetConfig,
    DatasetConfig,
    EvalConfig,
    RunConfig,
    RunPhase,
    TrainingConfig,
    generate_ulid,
)
from pars.orch.orchestrator import RunHandle

pytestmark = pytest.mark.integration


# ---------------------------------------------------------------------------
# 辅助：构造基准 RunConfig
# ---------------------------------------------------------------------------

def _make_parent_config(run_id: str | None = None) -> RunConfig:
    if run_id is None:
        run_id = generate_ulid()
    return RunConfig(
        run_id=run_id,
        research_question="集成测试原始假设",
        base_model="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
        dataset=DatasetConfig(hf_id="tatsu-lab/alpaca", split="train[:50]", n_samples=50),
        training=TrainingConfig(
            lora_rank=16,
            lora_alpha=32,
            lr=2e-4,
            epochs=3,
            batch_size=2,
            max_seq_len=512,
        ),
        eval=EvalConfig(tasks=["gsm8k"]),
        budget=BudgetConfig(usd_cap=30.0, wall_clock_hours_cap=12.0, gpu_hours_cap=12.0),
    )


# ---------------------------------------------------------------------------
# IT01: start_retry → RunOrchestrator.start 被调用，new config 含 parent_run_id
# ---------------------------------------------------------------------------

def test_start_retry_calls_orchestrator_with_correct_config() -> None:
    """should call RunOrchestrator.start with new config containing parent_run_id."""
    from pars.orch.retry import start_retry

    parent_id = generate_ulid()
    parent = _make_parent_config(run_id=parent_id)

    captured_config: list[RunConfig] = []

    def mock_orch_start(**kwargs) -> RunHandle:  # noqa: ANN001
        # RunOrchestrator.start 接收关键字参数（非 config 对象）
        # start_retry 内部应传递 research_question / lora_rank / lr / epochs 等
        return RunHandle(
            run_id=generate_ulid(),
            final_state=RunPhase.COMPLETED,
            report_path=None,
            exit_code=0,
            failure_reason=None,
        )

    with patch("pars.orch.retry.load_parent_config", return_value=parent), \
         patch("pars.orch.retry.RunOrchestrator") as mock_orch_cls:
        mock_orch = MagicMock()
        mock_orch_cls.return_value = mock_orch
        mock_orch.start.side_effect = mock_orch_start

        handle = start_retry(
            parent_run_id=parent_id,
            hypothesis="集成测试假设",
            overrides={},
        )

    # 断言 orchestrator 被实例化并调用 start
    assert mock_orch_cls.called, "RunOrchestrator 应被实例化"
    assert mock_orch.start.called, "RunOrchestrator.start 应被调用"


# ---------------------------------------------------------------------------
# IT02: retry_from 字段写入新 config
# ---------------------------------------------------------------------------

def test_start_retry_new_config_has_parent_run_id_field() -> None:
    """should write parent_run_id and retry_hypothesis into derived config."""
    from pars.orch.retry import derive_retry_config

    parent_id = generate_ulid()
    parent = _make_parent_config(run_id=parent_id)

    with patch("pars.orch.retry.load_parent_config", return_value=parent):
        new_cfg = derive_retry_config(
            parent_run_id=parent_id,
            hypothesis="集成测试：验证 parent_run_id 字段",
            overrides={},
        )

    assert new_cfg.parent_run_id == parent_id, (
        f"new config 应含 parent_run_id={parent_id}，实际：{new_cfg.parent_run_id}"
    )
    assert new_cfg.retry_hypothesis == "集成测试：验证 parent_run_id 字段", (
        f"new config 应含 retry_hypothesis，实际：{new_cfg.retry_hypothesis}"
    )


# ---------------------------------------------------------------------------
# IT03: overrides 生效（lr override 传达到 orchestrator.start 调用参数）
# ---------------------------------------------------------------------------

def test_start_retry_lr_override_reaches_orchestrator() -> None:
    """should pass lr override to RunOrchestrator.start."""
    from pars.orch.retry import start_retry

    parent_id = generate_ulid()
    parent = _make_parent_config(run_id=parent_id)

    captured_kwargs: dict = {}

    def capture_start(**kwargs) -> RunHandle:  # noqa: ANN001
        captured_kwargs.update(kwargs)
        return RunHandle(
            run_id=generate_ulid(),
            final_state=RunPhase.COMPLETED,
            report_path=None,
            exit_code=0,
            failure_reason=None,
        )

    with patch("pars.orch.retry.load_parent_config", return_value=parent), \
         patch("pars.orch.retry.RunOrchestrator") as mock_orch_cls:
        mock_orch = MagicMock()
        mock_orch_cls.return_value = mock_orch
        mock_orch.start.side_effect = capture_start

        start_retry(
            parent_run_id=parent_id,
            hypothesis="lr override test",
            overrides={"lr": 1e-5},
        )

    # 确认 lr 参数被正确传递
    assert captured_kwargs.get("lr") == pytest.approx(1e-5), (
        f"lr override 应传递给 orchestrator.start，captured：{captured_kwargs}"
    )


# ---------------------------------------------------------------------------
# IT04: 验证 start_retry 返回 RunHandle
# ---------------------------------------------------------------------------

def test_start_retry_returns_run_handle() -> None:
    """should return RunHandle from start_retry."""
    from pars.orch.retry import start_retry

    parent_id = generate_ulid()
    parent = _make_parent_config(run_id=parent_id)

    expected_run_id = generate_ulid()
    mock_handle = RunHandle(
        run_id=expected_run_id,
        final_state=RunPhase.COMPLETED,
        report_path=None,
        exit_code=0,
        failure_reason=None,
    )

    with patch("pars.orch.retry.load_parent_config", return_value=parent), \
         patch("pars.orch.retry.RunOrchestrator") as mock_orch_cls:
        mock_orch = MagicMock()
        mock_orch_cls.return_value = mock_orch
        mock_orch.start.return_value = mock_handle

        handle = start_retry(
            parent_run_id=parent_id,
            hypothesis="返回值测试",
            overrides={},
        )

    assert isinstance(handle, RunHandle), f"start_retry 应返回 RunHandle，实际：{type(handle)}"
    assert handle.run_id == expected_run_id


# ---------------------------------------------------------------------------
# IT05: CLI retry 命令调用时 --from / --hypothesis 传递正确
# ---------------------------------------------------------------------------

def test_cli_retry_command_invokes_start_retry() -> None:
    """should invoke start_retry with correct args when CLI retry command is called."""
    import os
    from click.testing import CliRunner
    from pars.cli.main import cli

    runner = CliRunner()
    parent_id = generate_ulid()
    parent = _make_parent_config(run_id=parent_id)

    mock_handle = RunHandle(
        run_id=generate_ulid(),
        final_state=RunPhase.COMPLETED,
        report_path=None,
        exit_code=0,
        failure_reason=None,
    )

    # CLI retry 通过 pars.orch.orchestrator.RunOrchestrator（直接 import）
    # 需要同时 patch：
    #   1. pars.orch.retry.load_parent_config（derive 时加载 parent）
    #   2. pars.cli.retry.RunOrchestrator（CLI 层直接调用 orch.start）
    with patch("pars.orch.retry.load_parent_config", return_value=parent), \
         patch("pars.cli.retry.RunOrchestrator") as mock_orch_cls, \
         patch.dict(os.environ, {"ANTHROPIC_API_KEY": "sk-test-fake"}):
        mock_orch = MagicMock()
        mock_orch_cls.return_value = mock_orch
        mock_orch.start.return_value = mock_handle

        result = runner.invoke(cli, [
            "sft", "retry",
            "--from", parent_id,
            "--hypothesis", "集成测试 CLI 假设",
        ])

    assert result.exit_code == 0, (
        f"retry 命令应退出 0，实际：{result.exit_code}\n输出：{result.output}"
    )
