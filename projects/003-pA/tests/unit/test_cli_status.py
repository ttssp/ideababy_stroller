"""
tests/unit/test_cli_status.py — `pars sft status` CLI 单元测试（T009）。

结论：验证 status 子命令在标准路径和边界条件下的正确行为。

测试策略：
  - 使用 click.testing.CliRunner（非 typer.testing.CliRunner，见 test_cli_smoke.py 说明）
  - 使用 tmp_runs_dir fixture 隔离文件系统副作用
  - 每个测试通过 monkeypatch.setenv 设置 RECALLKIT_RUN_DIR
"""

from __future__ import annotations

from pathlib import Path

import pytest
from click.testing import CliRunner

from pars.cli.main import cli
from pars.ledger.config_schema import (
    BudgetConfig,
    DatasetConfig,
    EvalConfig,
    RunConfig,
)

runner = CliRunner(mix_stderr=False)


# ---------------------------------------------------------------------------
# 测试辅助工厂
# ---------------------------------------------------------------------------


def _make_run_config(**overrides: object) -> RunConfig:
    """构造最简合法 RunConfig，支持字段覆盖。"""
    defaults: dict[str, object] = {
        "research_question": "LoRA SFT 能否提升 Qwen3-4B 在 GSM8K 上的准确率？",
        "base_model": "Qwen/Qwen3-4B",
        "dataset": DatasetConfig(hf_id="gsm8k", split="train", n_samples=100),
        "eval": EvalConfig(tasks=["gsm8k"], n_shot=0),
        "budget": BudgetConfig(
            usd_cap=5.0,
            wall_clock_hours_cap=12.0,
            gpu_hours_cap=6.0,
        ),
    }
    defaults.update(overrides)
    return RunConfig(**defaults)  # type: ignore[arg-type]


def _create_run(tmp_runs_dir: Path, monkeypatch: pytest.MonkeyPatch) -> str:
    """在 tmp_runs_dir 中创建一个 run，返回 run_id。"""
    monkeypatch.setenv("RECALLKIT_RUN_DIR", str(tmp_runs_dir))
    from pars.ledger.ledger import create_run
    config = _make_run_config()
    return create_run(config)


# ---------------------------------------------------------------------------
# T009-CLI-TC01: pars sft status --help 不 crash
# ---------------------------------------------------------------------------


def test_sft_status_help_not_crash(
    tmp_runs_dir: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """should show help without crashing when running pars sft status --help."""
    monkeypatch.setenv("RECALLKIT_RUN_DIR", str(tmp_runs_dir))

    result = runner.invoke(cli, ["sft", "status", "--help"])
    assert result.exit_code in (0, 1), (
        f"sft status --help 应退出 0 或 1，实际：{result.exit_code}\n{result.output}"
    )
    # help 输出应含 --run-id 参数说明
    assert "--run-id" in result.output or "run-id" in result.output, (
        f"help 输出应含 '--run-id'，实际：\n{result.output}"
    )


# ---------------------------------------------------------------------------
# T009-CLI-TC02: 无 run 时显示"暂无"提示，退出 0
# ---------------------------------------------------------------------------


def test_sft_status_no_runs_shows_empty_message(
    tmp_runs_dir: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """should print no-run message and exit 0 when there are no runs."""
    monkeypatch.setenv("RECALLKIT_RUN_DIR", str(tmp_runs_dir))

    result = runner.invoke(cli, ["sft", "status"])
    assert result.exit_code == 0, (
        f"无 run 时应退出 0，实际：{result.exit_code}\n{result.output}"
    )
    # 应提示用户没有 run
    combined = result.output + (result.stderr or "")
    assert "暂无" in combined or "no" in combined.lower() or "pars sft start" in combined, (
        f"无 run 时应显示提示信息，实际：\n{combined}"
    )


# ---------------------------------------------------------------------------
# T009-CLI-TC03: 有 run 时列表包含 run_id
# ---------------------------------------------------------------------------


def test_sft_status_list_contains_run_id(
    tmp_runs_dir: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """should display run_id in the table when a run exists."""
    run_id = _create_run(tmp_runs_dir, monkeypatch)

    result = runner.invoke(cli, ["sft", "status"])
    assert result.exit_code == 0, (
        f"有 run 时 status 应退出 0，实际：{result.exit_code}\n{result.output}"
    )
    assert run_id in result.output, (
        f"输出应含 run_id {run_id!r}，实际：\n{result.output}"
    )


# ---------------------------------------------------------------------------
# T009-CLI-TC04: --run-id 指定存在的 run 显示详情并退出 0
# ---------------------------------------------------------------------------


def test_sft_status_run_id_detail_exits_zero(
    tmp_runs_dir: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """should exit 0 and display run detail when --run-id exists."""
    run_id = _create_run(tmp_runs_dir, monkeypatch)

    result = runner.invoke(cli, ["sft", "status", "--run-id", run_id])
    assert result.exit_code == 0, (
        f"--run-id 存在时应退出 0，实际：{result.exit_code}\n{result.output}"
    )
    assert run_id in result.output, (
        f"详情输出应含 run_id {run_id!r}，实际：\n{result.output}"
    )


# ---------------------------------------------------------------------------
# T009-CLI-TC05: --run-id 指定不存在的 run 退出 1
# ---------------------------------------------------------------------------


def test_sft_status_nonexistent_run_id_exits_one(
    tmp_runs_dir: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """should exit 1 when --run-id points to a non-existent run."""
    monkeypatch.setenv("RECALLKIT_RUN_DIR", str(tmp_runs_dir))

    result = runner.invoke(cli, ["sft", "status", "--run-id", "01HRRRRRRRRRRRRRRRRRRRRRRRR"])
    assert result.exit_code == 1, (
        f"不存在的 run_id 应退出 1，实际：{result.exit_code}\n{result.output}"
    )


# ---------------------------------------------------------------------------
# T009-CLI-TC06: 详情输出包含 research_question 和 base_model
# ---------------------------------------------------------------------------


def test_sft_status_detail_contains_key_fields(
    tmp_runs_dir: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """should include research_question and base_model in detail output."""
    run_id = _create_run(tmp_runs_dir, monkeypatch)

    result = runner.invoke(cli, ["sft", "status", "--run-id", run_id])
    assert result.exit_code == 0, (
        f"详情查询应退出 0，实际：{result.exit_code}\n{result.output}"
    )
    assert "Qwen/Qwen3-4B" in result.output, (
        f"详情应含 base_model，实际：\n{result.output}"
    )
    assert "GSM8K" in result.output or "gsm8k" in result.output.lower(), (
        f"详情应含 research_question 关键词，实际：\n{result.output}"
    )


# ---------------------------------------------------------------------------
# T009-CLI-TC07: 列表中最新 run 排在最前
# ---------------------------------------------------------------------------


def test_sft_status_list_ordered_newest_first(
    tmp_runs_dir: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """should show newest run first in the list output."""
    monkeypatch.setenv("RECALLKIT_RUN_DIR", str(tmp_runs_dir))
    from pars.ledger.ledger import create_run

    config = _make_run_config()
    id1 = create_run(config)
    _id2 = create_run(config)
    id3 = create_run(config)

    result = runner.invoke(cli, ["sft", "status"])
    assert result.exit_code == 0, (
        f"status 列表应退出 0，实际：{result.exit_code}\n{result.output}"
    )
    output = result.output
    # 最新的 run_id（id3）应在最旧的（id1）之前出现
    pos1 = output.find(id1)
    pos3 = output.find(id3)
    assert pos1 != -1, f"id1 {id1!r} 应在输出中"
    assert pos3 != -1, f"id3 {id3!r} 应在输出中"
    assert pos3 < pos1, (
        f"最新 run（id3）应在最旧 run（id1）之前，pos3={pos3}, pos1={pos1}"
    )
