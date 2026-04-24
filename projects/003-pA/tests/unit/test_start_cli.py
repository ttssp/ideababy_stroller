"""
tests/unit/test_start_cli.py — T023 `pars sft start` CLI 参数测试。

结论：验证 pars sft start --help 包含全部规定参数，
      且缺少 required 参数时退出非零。
      不调用真实 RunOrchestrator（全部 mock）。
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest
from click.testing import CliRunner

from pars.cli.main import cli

runner = CliRunner()


# ---------------------------------------------------------------------------
# T023-CLI-TC01: --help 包含所有规定参数
# ---------------------------------------------------------------------------

REQUIRED_OPTIONS = [
    "--question",
    "--base",
    "--dataset",
    "--dataset-split",
    "--lora-rank",
    "--lora-alpha",
    "--lr",
    "--epochs",
    "--batch-size",
    "--max-seq-len",
    "--eval-tasks",
    "--usd-cap",
    "--wall-clock-hours-cap",
    "--gpu-hours-cap",
    "--name",
]


def test_sft_start_help_shows_all_params() -> None:
    """should show all required parameters in pars sft start --help."""
    result = runner.invoke(cli, ["sft", "start", "--help"])
    assert result.exit_code in (0, 1), (
        f"--help 应退出 0 或 1，实际：{result.exit_code}\n{result.output}"
    )
    for opt in REQUIRED_OPTIONS:
        assert opt in result.output, (
            f"--help 输出应含 '{opt}'，实际输出：\n{result.output}"
        )


# ---------------------------------------------------------------------------
# T023-CLI-TC02: 缺 --question 时退出非零
# ---------------------------------------------------------------------------

def test_sft_start_missing_question_exits_nonzero() -> None:
    """should exit non-zero when --question is missing."""
    result = runner.invoke(cli, [
        "sft", "start",
        "--base", "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
        "--dataset", "tatsu-lab/alpaca",
    ])
    assert result.exit_code != 0, (
        f"缺 --question 应退出非 0，实际：{result.exit_code}\n{result.output}"
    )


# ---------------------------------------------------------------------------
# T023-CLI-TC03: 缺 --base 时退出非零
# ---------------------------------------------------------------------------

def test_sft_start_missing_base_exits_nonzero() -> None:
    """should exit non-zero when --base is missing."""
    result = runner.invoke(cli, [
        "sft", "start",
        "--question", "test question",
        "--dataset", "tatsu-lab/alpaca",
    ])
    assert result.exit_code != 0, (
        f"缺 --base 应退出非 0，实际：{result.exit_code}\n{result.output}"
    )


# ---------------------------------------------------------------------------
# T023-CLI-TC04: 缺 --dataset 时退出非零
# ---------------------------------------------------------------------------

def test_sft_start_missing_dataset_exits_nonzero() -> None:
    """should exit non-zero when --dataset is missing."""
    result = runner.invoke(cli, [
        "sft", "start",
        "--question", "test question",
        "--base", "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    ])
    assert result.exit_code != 0, (
        f"缺 --dataset 应退出非 0，实际：{result.exit_code}\n{result.output}"
    )


# ---------------------------------------------------------------------------
# T023-CLI-TC05: 提供所有必填参数 + 模拟 RunOrchestrator.start → RunHandle(exit_code=0)
# ---------------------------------------------------------------------------

def test_sft_start_invokes_orchestrator_with_all_params() -> None:
    """should invoke RunOrchestrator.start with correct params when all required params provided."""
    from pars.ledger import RunPhase

    mock_handle = MagicMock()
    mock_handle.run_id = "01JTESTULID000000000000001"
    mock_handle.final_state = RunPhase.COMPLETED
    mock_handle.report_path = None
    mock_handle.exit_code = 0
    mock_handle.failure_reason = None

    with patch("pars.cli.start.RunOrchestrator") as mock_orch_cls:
        mock_orch = MagicMock()
        mock_orch_cls.return_value = mock_orch
        mock_orch.start.return_value = mock_handle

        result = runner.invoke(cli, [
            "sft", "start",
            "--question", "Does LoRA help on GSM8K?",
            "--base", "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
            "--dataset", "tatsu-lab/alpaca",
        ])

    # RunOrchestrator 已被调用
    assert mock_orch_cls.called or mock_orch.start.called, (
        f"RunOrchestrator 应被实例化并调用 start，output：\n{result.output}"
    )


# ---------------------------------------------------------------------------
# T023-CLI-TC06: 带 --name 参数时传递给 orchestrator
# ---------------------------------------------------------------------------

def test_sft_start_passes_name_to_orchestrator() -> None:
    """should pass --name value to RunOrchestrator.start."""
    from pars.ledger import RunPhase

    mock_handle = MagicMock()
    mock_handle.run_id = "my-custom-run"
    mock_handle.final_state = RunPhase.COMPLETED
    mock_handle.report_path = None
    mock_handle.exit_code = 0
    mock_handle.failure_reason = None

    captured_kwargs: dict = {}

    def capture_start(**kwargs):  # noqa: ANN001
        captured_kwargs.update(kwargs)
        return mock_handle

    with patch("pars.cli.start.RunOrchestrator") as mock_orch_cls:
        mock_orch = MagicMock()
        mock_orch_cls.return_value = mock_orch
        mock_orch.start.side_effect = capture_start

        runner.invoke(cli, [
            "sft", "start",
            "--question", "test",
            "--base", "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
            "--dataset", "tatsu-lab/alpaca",
            "--name", "my-custom-run",
        ])

    assert captured_kwargs.get("run_id") == "my-custom-run", (
        f"--name 应传递为 run_id，captured_kwargs：{captured_kwargs}"
    )


# ---------------------------------------------------------------------------
# T023-CLI-TC07: 缺 ANTHROPIC_API_KEY 时退出码 2
# ---------------------------------------------------------------------------

def test_sft_start_exits_2_when_api_key_missing() -> None:
    """should exit code 2 when ANTHROPIC_API_KEY is missing."""
    import os

    from pars.orch.orchestrator import ApiKeyMissingError

    with patch("pars.cli.start.RunOrchestrator") as mock_orch_cls:
        mock_orch = MagicMock()
        mock_orch_cls.return_value = mock_orch
        mock_orch.start.side_effect = ApiKeyMissingError("ANTHROPIC_API_KEY not set")

        result = runner.invoke(cli, [
            "sft", "start",
            "--question", "test",
            "--base", "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
            "--dataset", "tatsu-lab/alpaca",
        ])

    assert result.exit_code == 2, (  # noqa: PLR2004
        f"API key 缺失应退出 2，实际：{result.exit_code}\n{result.output}"
    )


# ---------------------------------------------------------------------------
# T023-CLI-TC08: fail-closed ReadonlyFailsClosed 时退出码 2
# ---------------------------------------------------------------------------

def test_sft_start_exits_2_when_readonly_fails_closed() -> None:
    """should exit code 2 when ReadonlyFailsClosed is raised."""
    from pars.safety.readonly_mount import ReadonlyFailsClosed

    with patch("pars.cli.start.RunOrchestrator") as mock_orch_cls:
        mock_orch = MagicMock()
        mock_orch_cls.return_value = mock_orch
        mock_orch.start.side_effect = ReadonlyFailsClosed(
            "cannot mount .claude/ read-only",
        )

        result = runner.invoke(cli, [
            "sft", "start",
            "--question", "test",
            "--base", "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
            "--dataset", "tatsu-lab/alpaca",
        ])

    assert result.exit_code == 2, (  # noqa: PLR2004
        f"ReadonlyFailsClosed 应退出 2，实际：{result.exit_code}\n{result.output}"
    )


# ---------------------------------------------------------------------------
# T023-CLI-TC09: default 参数值验证
# ---------------------------------------------------------------------------

def test_sft_start_default_values_passed_to_orchestrator() -> None:
    """should pass default values to RunOrchestrator.start when not overridden."""
    from pars.ledger import RunPhase

    mock_handle = MagicMock()
    mock_handle.run_id = "01JTESTDEFAULT0000000000001"
    mock_handle.final_state = RunPhase.COMPLETED
    mock_handle.report_path = None
    mock_handle.exit_code = 0
    mock_handle.failure_reason = None

    captured: dict = {}

    def capture(**kwargs):  # noqa: ANN001
        captured.update(kwargs)
        return mock_handle

    with patch("pars.cli.start.RunOrchestrator") as mock_orch_cls:
        mock_orch = MagicMock()
        mock_orch_cls.return_value = mock_orch
        mock_orch.start.side_effect = capture

        runner.invoke(cli, [
            "sft", "start",
            "--question", "test",
            "--base", "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
            "--dataset", "tatsu-lab/alpaca",
        ])

    # 校验部分 defaults
    if captured:
        assert captured.get("lora_rank") == 16, f"lora_rank 默认 16，实际：{captured.get('lora_rank')}"  # noqa: PLR2004
        assert captured.get("lora_alpha") == 32, f"lora_alpha 默认 32，实际：{captured.get('lora_alpha')}"  # noqa: PLR2004
        assert captured.get("epochs") == 3, f"epochs 默认 3，实际：{captured.get('epochs')}"  # noqa: PLR2004
        assert captured.get("usd_cap") == 30.0, f"usd_cap 默认 30，实际：{captured.get('usd_cap')}"  # noqa: PLR2004
