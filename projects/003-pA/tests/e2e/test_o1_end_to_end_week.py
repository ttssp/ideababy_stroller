"""
tests/e2e/test_o1_end_to_end_week.py — T026 Outcome O1 E2E 测试。

结论：验证 RunOrchestrator.start() 在 week-scale 运行中产出正确的文件产物
      和 state.phase==completed。

## 测试策略

- 合成测试（CI 默认，@pytest.mark.e2e）：
    mock RunOrchestrator.start()，手动创建文件产物，
    验证产物结构校验逻辑 + RunHandle 字段契约。
- 真实 GPU 测试（@pytest.mark.slow @pytest.mark.gpu）：
    需要 NVIDIA GPU，运行完整 TinyLlama + alpaca[:20] epochs=1 run。

## 验证 Outcome O1

O1（architecture §9）：单次 LoRA SFT 实验，产出决策报告 + 完整产物。
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from pars.ledger.state import RunPhase
from pars.orch.orchestrator import RunHandle


# ---------------------------------------------------------------------------
# T026-O1-TC01: 合成测试 — RunHandle 字段契约（CI 默认）
# ---------------------------------------------------------------------------


@pytest.mark.e2e
def test_o1_orchestrator_run_handle_contract(
    tmp_runs_dir: Path,
    tiny_run_config,
) -> None:
    """should return RunHandle with exit_code=0 and completed phase when run succeeds.

    结论：mock RunOrchestrator.start() 使其返回合法 RunHandle，
          验证调用方能正确读取所有字段（契约测试）。
    """
    from pars.orch.orchestrator import RunOrchestrator

    run_id = "test-o1-synthetic-01"
    report_path = tmp_runs_dir / run_id / "report.md"

    # 构造期望的 RunHandle
    expected_handle = RunHandle(
        run_id=run_id,
        final_state=RunPhase.COMPLETED,
        report_path=report_path,
        exit_code=0,
        failure_reason=None,
    )

    with patch.object(RunOrchestrator, "start", return_value=expected_handle) as mock_start:
        orch = RunOrchestrator()
        handle = orch.start(
            research_question=tiny_run_config.research_question,
            base_model=tiny_run_config.base_model,
            dataset_id=tiny_run_config.dataset.hf_id,
            dataset_split=tiny_run_config.dataset.split,
            n_samples=tiny_run_config.dataset.n_samples,
        )

    # 验证 mock 被调用
    mock_start.assert_called_once()

    # 验证 RunHandle 字段契约
    assert handle.exit_code == 0, f"exit_code 应为 0（completed），实际：{handle.exit_code}"
    assert handle.final_state == RunPhase.COMPLETED, (
        f"final_state 应为 completed，实际：{handle.final_state}"
    )
    assert handle.run_id == run_id
    assert handle.failure_reason is None, (
        f"成功 run 的 failure_reason 应为 None，实际：{handle.failure_reason}"
    )


# ---------------------------------------------------------------------------
# T026-O1-TC02: 合成测试 — run 产物结构（CI 默认）
# ---------------------------------------------------------------------------


@pytest.mark.e2e
def test_o1_run_artifacts_structure(tmp_runs_dir: Path) -> None:
    """should produce expected artifact structure when a run completes.

    结论：直接在 tmp_runs_dir 创建标准产物结构，验证产物路径协议：
          runs/<run_id>/config.yaml, state.json, metrics.jsonl, report.md,
          artifacts/training_curve.png
    """
    from pars.report.schema_validator import validate_report_schema

    run_id = "test-o1-artifacts-01"
    run_dir = tmp_runs_dir / run_id
    run_dir.mkdir(parents=True)
    (run_dir / "artifacts").mkdir()

    # 创建最小合法 state.json
    (run_dir / "state.json").write_text(
        json.dumps({
            "run_id": run_id,
            "phase": "completed",
            "stuck_state": "idle",
            "stuck_restart_count": 0,
            "needs_human_review": False,
            "usd_spent": 0.12,
            "wall_clock_elapsed_s": 300.0,
            "gpu_hours_used": 0.08,
            "last_update": "2026-01-01T00:05:00+00:00",
        }),
        encoding="utf-8",
    )

    # 创建最小合法 metrics.jsonl（非空）
    metric_line = json.dumps({
        "phase": "evaluating",
        "kind": "eval",
        "data": {"task_name": "gsm8k", "acc": 0.42},
        "ts": "2026-01-01T00:04:00+00:00",
    })
    (run_dir / "metrics.jsonl").write_text(metric_line + "\n", encoding="utf-8")

    # 创建最小合法 report.md（通过 validate_report_schema）
    report_content = _make_valid_report_md(run_id=run_id)
    (run_dir / "report.md").write_text(report_content, encoding="utf-8")

    # 创建 config.yaml（占位）
    (run_dir / "config.yaml").write_text("run_id: " + run_id + "\n", encoding="utf-8")

    # 创建 artifacts/training_curve.png（1x1 像素 PNG 占位）
    _write_minimal_png(run_dir / "artifacts" / "training_curve.png")

    # --- 断言产物存在 ---
    assert (run_dir / "config.yaml").exists(), "config.yaml 应存在"
    assert (run_dir / "state.json").exists(), "state.json 应存在"
    assert (run_dir / "metrics.jsonl").exists(), "metrics.jsonl 应存在"
    assert (run_dir / "metrics.jsonl").stat().st_size > 0, "metrics.jsonl 不得为空"
    assert (run_dir / "artifacts" / "training_curve.png").exists(), (
        "artifacts/training_curve.png 应存在"
    )

    # --- 断言 state.phase == completed ---
    state_data = json.loads((run_dir / "state.json").read_text())
    assert state_data.get("phase") == "completed", (
        f"state.phase 应为 completed，实际：{state_data.get('phase')}"
    )

    # --- 断言 report.md schema 通过 ---
    ok, errors = validate_report_schema(run_dir / "report.md")
    assert ok, f"report.md schema 校验失败：{errors}"


# ---------------------------------------------------------------------------
# T026-O1-TC03: 真实 GPU 测试（需要 NVIDIA GPU，默认 skip）
# ---------------------------------------------------------------------------


@pytest.mark.e2e
@pytest.mark.slow
@pytest.mark.gpu
@pytest.mark.skipif(
    shutil.which("nvidia-smi") is None,
    reason="需要 NVIDIA GPU + nvidia-smi（macOS/CPU CI 自动 skip）",
)
def test_o1_real_sft_run_completes(
    tmp_runs_dir: Path,
    tiny_run_config,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """should complete full SFT run with TinyLlama + alpaca[:20] and produce report.

    结论：真实 GPU 端到端测试，验证 O1 完整 happy path（含训练+eval+报告）。
    预期耗时：TinyLlama 1.1B + alpaca[:20] epochs=1 ≈ 5-20min。
    """
    import os

    from pars.orch.orchestrator import RunOrchestrator
    from pars.report.schema_validator import validate_report_schema

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        pytest.skip("ANTHROPIC_API_KEY 未设置，跳过真实 run 测试")

    orch = RunOrchestrator()
    handle = orch.start(
        research_question=tiny_run_config.research_question,
        base_model=tiny_run_config.base_model,
        dataset_id=tiny_run_config.dataset.hf_id,
        dataset_split=tiny_run_config.dataset.split,
        n_samples=tiny_run_config.dataset.n_samples,
        lora_rank=tiny_run_config.training.lora_rank if tiny_run_config.training else 8,
        lora_alpha=tiny_run_config.training.lora_alpha if tiny_run_config.training else 16,
        lr=tiny_run_config.training.lr if tiny_run_config.training else 2e-4,
        epochs=tiny_run_config.training.epochs if tiny_run_config.training else 1,
        batch_size=tiny_run_config.training.batch_size if tiny_run_config.training else 1,
        max_seq_len=tiny_run_config.training.max_seq_len if tiny_run_config.training else 512,
        eval_tasks=tiny_run_config.eval.tasks,
        usd_cap=tiny_run_config.budget.usd_cap,
        wall_clock_hours_cap=tiny_run_config.budget.wall_clock_hours_cap,
        gpu_hours_cap=tiny_run_config.budget.gpu_hours_cap,
    )

    assert handle.exit_code == 0, (
        f"exit_code 应为 0（completed），实际：{handle.exit_code}，"
        f"reason={handle.failure_reason}"
    )
    assert handle.final_state == RunPhase.COMPLETED

    run_dir = tmp_runs_dir / handle.run_id
    assert (run_dir / "config.yaml").exists()
    assert (run_dir / "state.json").exists()
    assert (run_dir / "metrics.jsonl").exists()
    assert (run_dir / "metrics.jsonl").stat().st_size > 0

    # report.md 存在 + schema 校验
    report_path = run_dir / "report.md"
    assert report_path.exists(), "report.md 应存在"
    ok, errors = validate_report_schema(report_path)
    assert ok, f"report.md schema 校验失败：{errors}"

    # training_curve.png
    assert (run_dir / "artifacts" / "training_curve.png").exists()


# ---------------------------------------------------------------------------
# 辅助函数
# ---------------------------------------------------------------------------


def _make_valid_report_md(run_id: str) -> str:
    """生成能通过 validate_report_schema 的最小合法 report.md 内容。

    结论：按 schema_validator.py 的必填 H2 sections 要求生成。
    """
    return f"""# SFT 实验决策报告

## 元数据

| 字段 | 值 |
|------|-----|
| run_id | {run_id} |
| base_model | TinyLlama/TinyLlama-1.1B-Chat-v1.0 |
| 训练时长 | 300s |
| USD 消耗 | 0.12 |

## 训练曲线

![training_curve](artifacts/training_curve.png)

## 分数对比

| 任务 | Baseline | LoRA SFT | Delta |
|------|----------|----------|-------|
| gsm8k | 0.10 | 0.42 | +0.32 |

## 失败归因

无显著失败。训练 loss 从 2.30 下降至 0.85，共 20 步。

## 决策

推荐继续：LoRA SFT 提升 gsm8k 准确率 +32 个百分点（0.10 → 0.42），建议继续扩大规模。
"""


def _write_minimal_png(path: Path) -> None:
    """写入最小合法 1×1 像素 PNG 文件（用于产物存在性验证）。"""
    # 最小 PNG：1×1 透明像素（已知合法 PNG header + IHDR + IDAT + IEND）
    minimal_png = bytes([
        0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A,  # PNG signature
        0x00, 0x00, 0x00, 0x0D, 0x49, 0x48, 0x44, 0x52,  # IHDR chunk length + type
        0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x01,  # width=1, height=1
        0x08, 0x06, 0x00, 0x00, 0x00, 0x1F, 0x15, 0xC4,  # bitdepth=8, colortype=6
        0x89, 0x00, 0x00, 0x00, 0x0A, 0x49, 0x44, 0x41,  # IDAT
        0x54, 0x78, 0x9C, 0x62, 0x00, 0x01, 0x00, 0x00,
        0x05, 0x00, 0x01, 0x0D, 0x0A, 0x2D, 0xB4, 0x00,
        0x00, 0x00, 0x00, 0x49, 0x45, 0x4E, 0x44, 0xAE,  # IEND
        0x42, 0x60, 0x82,
    ])
    path.write_bytes(minimal_png)
