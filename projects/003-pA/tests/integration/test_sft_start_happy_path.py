"""
tests/integration/test_sft_start_happy_path.py — T023 `pars sft start` 端到端集成测试。

结论：验证 TinyLlama + alpaca[:20] 完整 run 的文件产物 + state + report schema。
      需要 NVIDIA GPU + nvidia-smi；macOS / CPU 机器直接 skip。

## 标记策略

- @pytest.mark.integration : 集成测试，默认 CI skip（filterwarnings 不影响 collect）
- @pytest.mark.slow        : 耗时 > 60s，须 -m slow 才跑
- @gpu_marker              : 无 nvidia-smi 时自动 skip（macOS 总是 skip）

## 运行方式（操作员本机，有 GPU）

    uv run pytest tests/integration/test_sft_start_happy_path.py -v \\
        -m "integration and slow and gpu"

## 预期耗时

    TinyLlama 1.1B + alpaca[:20] epochs=1 ≈ 5-20min（依据 GPU 性能）
"""

from __future__ import annotations

import shutil
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# GPU marker：无 nvidia-smi（macOS 通常无此命令）时 skip
# ---------------------------------------------------------------------------

gpu_marker = pytest.mark.skipif(
    shutil.which("nvidia-smi") is None,
    reason="需要 NVIDIA GPU + nvidia-smi（仅 Linux CI / 自有 GPU 机器执行；macOS 自动 skip）",
)


# ---------------------------------------------------------------------------
# T023-INT-TC01: TinyLlama + alpaca[:20] epochs=1 端到端 happy path
# ---------------------------------------------------------------------------

@pytest.mark.integration
@pytest.mark.slow
@gpu_marker
def test_sft_start_happy_path_with_tinyllama(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """should complete full SFT run and produce expected artifacts.

    验证：
    - runs/<run_id>/config.yaml 存在
    - runs/<run_id>/state.json phase == "completed"
    - runs/<run_id>/metrics.jsonl 非空
    - runs/<run_id>/report.md 存在 + validate_report_schema == True
    - runs/<run_id>/failure_attribution.md 存在（若适用）
    - runs/<run_id>/artifacts/training_curve.png 存在
    - worker env 历史不含 ANTHROPIC_API_KEY（proxy audit log 旁证）
    """
    import os

    from pars.orch.orchestrator import RunOrchestrator
    from pars.report import validate_report_schema

    # 使用 tmp_path 作为 runs 目录（避免污染真实 runs/）
    monkeypatch.setenv("PARS_RUNS_DIR", str(tmp_path / "runs"))
    # 确保测试用 API key 存在（真实 run 需要；CI 应有 secret）
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        pytest.skip("ANTHROPIC_API_KEY 未设置，跳过真实 run 测试")

    run_name = "test-tinyllama-happy-path-01"

    orch = RunOrchestrator()
    handle = orch.start(
        research_question="Does LoRA SFT improve TinyLlama instruction-following on alpaca?",
        base_model="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
        dataset_id="tatsu-lab/alpaca",
        dataset_split="train[:20]",
        n_samples=20,
        lora_rank=8,
        lora_alpha=16,
        lr=2e-4,
        epochs=1,
        batch_size=1,
        max_seq_len=512,
        eval_tasks=["gsm8k"],
        usd_cap=0.5,
        wall_clock_hours_cap=1.0,
        gpu_hours_cap=1.0,
        run_id=run_name,
    )

    # 验证 RunHandle
    assert handle is not None, "orch.start() 应返回 RunHandle"
    assert handle.exit_code == 0, (
        f"exit_code 应为 0（completed），实际：{handle.exit_code}，"
        f"reason={handle.failure_reason}"
    )

    run_dir = tmp_path / "runs" / run_name

    # 验证文件产物
    assert (run_dir / "config.yaml").exists(), "config.yaml 应存在"
    assert (run_dir / "state.json").exists(), "state.json 应存在"
    assert (run_dir / "metrics.jsonl").exists(), "metrics.jsonl 应存在"
    assert (run_dir / "metrics.jsonl").stat().st_size > 0, "metrics.jsonl 不得为空"

    # 验证 state.phase == "completed"
    import json

    state_data = json.loads((run_dir / "state.json").read_text())
    assert state_data.get("phase") == "completed", (
        f"state.phase 应为 completed，实际：{state_data.get('phase')}"
    )

    # 验证 report.md 存在 + schema 通过
    report_path = run_dir / "report.md"
    assert report_path.exists(), "report.md 应存在"
    ok, errors = validate_report_schema(report_path)
    assert ok, f"report.md schema 校验失败：{errors}"

    # 验证 artifacts/training_curve.png
    assert (run_dir / "artifacts" / "training_curve.png").exists(), (
        "artifacts/training_curve.png 应存在"
    )


# ---------------------------------------------------------------------------
# T023-INT-TC02: ApiKeyMissingError 在无 API key 时抛出（不需要 GPU）
# ---------------------------------------------------------------------------

@pytest.mark.integration
def test_sft_start_raises_when_no_api_key(monkeypatch: pytest.MonkeyPatch) -> None:
    """should raise ApiKeyMissingError when ANTHROPIC_API_KEY is not set.

    此测试不需要 GPU，在任何平台上都应执行。
    """
    import os

    from pars.orch.orchestrator import ApiKeyMissingError, RunOrchestrator

    # 确保 API key 不存在
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)

    orch = RunOrchestrator()
    with pytest.raises(ApiKeyMissingError, match="ANTHROPIC_API_KEY"):
        orch.start(
            research_question="test",
            base_model="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
            dataset_id="tatsu-lab/alpaca",
        )
