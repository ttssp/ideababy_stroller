"""
tests/integration/test_report_end_to_end.py — 报告渲染端到端集成测试。

测试策略:
1. 构造完整 run_dir fixture (baseline score / lora score / metrics / state=completed) →
   render_report → 验证输出含 "基线 vs LoRA" + PNG 路径引用 + "✅ 无失败"
2. 有 failure_attribution 的 run → render 后报告含失败归因章节
3. charts.py 生成真实 PNG 文件 (验证 header bytes 是 PNG magic \x89PNG)
"""

from __future__ import annotations

import json
import struct
from pathlib import Path

import pytest
import yaml

from pars.report.charts import plot_eval_scores, plot_training_loss
from pars.report.renderer import render_report


pytestmark = pytest.mark.integration


# ---------------------------------------------------------------------------
# Fixture: 构造完整 run_dir
# ---------------------------------------------------------------------------


def _make_run_dir(
    tmp_path: Path,
    *,
    state: str = "completed",
    include_fa: bool = False,
    fa_content: str | None = None,
) -> tuple[Path, str]:
    """构造合法 run_dir 结构,返回 (run_dir, run_id)。"""
    run_id = "01JTEST00000000000000000001"
    run_dir = tmp_path / "runs" / run_id
    artifacts = run_dir / "artifacts"
    artifacts.mkdir(parents=True, exist_ok=True)

    # config.yaml
    config = {
        "run_id": run_id,
        "question": "LoRA 是否能提升 Qwen3-4B 在 gsm8k 上的准确率？",
        "base_model": "Qwen3-4B",
        "dataset": "gsm8k-100",
        "lora": {"rank": 8, "alpha": 16, "lr": 2e-4, "epochs": 3},
        "started_at": "2026-04-24T00:00:00+00:00",
        "ended_at": "2026-04-24T02:30:00+00:00",
        "gpu_model": "NVIDIA GeForce RTX 4090",
        "cuda_version": "12.4",
        "python_version": "3.12.0",
        "wall_clock": "02:30:00",
        "usd_spent": 0.50,
        "gpu_hours": 2.5,
    }
    (run_dir / "config.yaml").write_text(yaml.dump(config, allow_unicode=True), encoding="utf-8")

    # metrics.jsonl (含 baseline + training epoch + eval 行)
    metrics_lines = [
        json.dumps({
            "ts": "2026-04-24T00:01:00+00:00",
            "phase": "baseline",
            "kind": "eval",
            "data": {"accuracy": 0.45, "metric": "accuracy"},
        }),
        json.dumps({
            "ts": "2026-04-24T00:30:00+00:00",
            "phase": "training",
            "kind": "epoch",
            "data": {"epoch": 1, "train_loss": 1.23, "eval_loss": 1.45},
        }),
        json.dumps({
            "ts": "2026-04-24T01:00:00+00:00",
            "phase": "training",
            "kind": "epoch",
            "data": {"epoch": 2, "train_loss": 0.98, "eval_loss": 1.12},
        }),
        json.dumps({
            "ts": "2026-04-24T01:30:00+00:00",
            "phase": "training",
            "kind": "epoch",
            "data": {"epoch": 3, "train_loss": 0.75, "eval_loss": 0.89},
        }),
    ]
    (run_dir / "metrics.jsonl").write_text("\n".join(metrics_lines) + "\n", encoding="utf-8")

    # artifacts/scores.json (含 baseline + lora_final)
    scores = {
        "baseline": {"accuracy": 0.45},
        "lora_epoch_1": {"accuracy": 0.47},
        "lora_final": {"accuracy": 0.51},
    }
    (artifacts / "scores.json").write_text(json.dumps(scores, indent=2), encoding="utf-8")

    # state.json
    state_data = {
        "phase": state,
        "usd_spent": 0.50,
        "gpu_hours": 2.5,
    }
    (run_dir / "state.json").write_text(json.dumps(state_data, indent=2), encoding="utf-8")

    # failure_attribution.md (可选)
    if include_fa:
        default_fa = """\
# Failure attribution · {run_id}

## 必填字段
- **假设**: 预计 LoRA 微调后 gsm8k 准确率从基线 0.45 提升至 0.55 以上，学习率 2e-4 合适
- **观察**: LoRA final epoch accuracy=0.51，高于 baseline 0.45，loss 曲线在 epoch 3 仍下降
- **归因**:
  - [x] 训练 epoch 不足
- **下一步建议**: 尝试增加 epoch=5 或调整 rank=16 进一步提升

## 自由叙述(可选,但鼓励)
整体训练过程正常，结果略低于预期，建议增加训练轮次。
""".format(run_id=run_id)
        content_to_write = fa_content if fa_content is not None else default_fa
        (run_dir / "failure_attribution.md").write_text(content_to_write, encoding="utf-8")

    return run_dir, run_id


# ---------------------------------------------------------------------------
# 测试 1: 完整 run (无 FA) → 输出含关键内容
# ---------------------------------------------------------------------------


@pytest.mark.integration
def test_render_report_completed_run_no_fa(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """构造 completed run (无 FA) → render → 含 '基线 vs LoRA' + PNG 引用 + '无失败' 标识。"""
    monkeypatch.setenv("RECALLKIT_RUN_DIR", str(tmp_path / "runs"))
    run_dir, run_id = _make_run_dir(tmp_path, state="completed", include_fa=False)

    report_path = render_report(run_dir)

    assert report_path.exists(), f"report.md 应已生成,实际路径: {report_path}"

    content = report_path.read_text(encoding="utf-8")

    # 核心章节检查
    assert "基线" in content or "Baseline" in content, "应含基线对比内容"
    assert "LoRA" in content, "应含 LoRA 字段"
    # 训练曲线图片引用
    assert "training_curve.png" in content or "eval_scores.png" in content, "应含图片引用"
    # 无失败标识
    assert "无失败" in content or "✅" in content, "completed run 应含无失败字样"


# ---------------------------------------------------------------------------
# 测试 2: 有 FA 的 run → 报告含失败归因章节
# ---------------------------------------------------------------------------


@pytest.mark.integration
def test_render_report_with_failure_attribution(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """有 FA 的 run → render 后报告含失败归因内容(非'✅ 无失败')。"""
    monkeypatch.setenv("RECALLKIT_RUN_DIR", str(tmp_path / "runs"))
    run_dir, run_id = _make_run_dir(tmp_path, state="completed", include_fa=True)

    report_path = render_report(run_dir)
    content = report_path.read_text(encoding="utf-8")

    # 报告应包含失败归因章节标题
    assert "失败归因" in content, "应含失败归因章节"
    # 应含 FA 内容摘要(而非简单的无失败提示)
    # FA 内容: 假设/观察/建议等
    assert "假设" in content or "观察" in content or "epoch" in content.lower(), (
        "应嵌入 FA 内容摘要"
    )


# ---------------------------------------------------------------------------
# 测试 3: charts.py 生成真实 PNG 文件 (magic bytes 验证)
# ---------------------------------------------------------------------------


@pytest.mark.integration
def test_charts_generate_real_png_files(tmp_path: Path) -> None:
    """plot_eval_scores 和 plot_training_loss 生成真实 PNG (验证 magic bytes)。"""
    artifacts = tmp_path / "artifacts"
    artifacts.mkdir()

    # 测试 plot_eval_scores
    baseline_scores = {"accuracy": 0.45, "f1": 0.42}
    lora_scores = {"accuracy": 0.51, "f1": 0.49}
    eval_png = artifacts / "eval_scores.png"

    plot_eval_scores(baseline_scores, lora_scores, eval_png)

    assert eval_png.exists(), "eval_scores.png 应已生成"
    header = eval_png.read_bytes()[:8]
    assert header == b"\x89PNG\r\n\x1a\n", f"eval_scores.png 应是有效 PNG,实际 header: {header.hex()}"

    # 测试 plot_training_loss
    loss_records = [
        {"epoch": 1, "train_loss": 1.23, "eval_loss": 1.45},
        {"epoch": 2, "train_loss": 0.98, "eval_loss": 1.12},
        {"epoch": 3, "train_loss": 0.75, "eval_loss": 0.89},
    ]
    loss_png = artifacts / "loss_curve.png"

    plot_training_loss(loss_records, loss_png)

    assert loss_png.exists(), "loss_curve.png 应已生成"
    header = loss_png.read_bytes()[:8]
    assert header == b"\x89PNG\r\n\x1a\n", f"loss_curve.png 应是有效 PNG,实际 header: {header.hex()}"


# ---------------------------------------------------------------------------
# 测试 4: render_report 生成的 PNG 文件合法
# ---------------------------------------------------------------------------


@pytest.mark.integration
def test_render_report_creates_png_artifacts(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """render_report 应在 artifacts/ 下生成 PNG 图表文件。"""
    monkeypatch.setenv("RECALLKIT_RUN_DIR", str(tmp_path / "runs"))
    run_dir, run_id = _make_run_dir(tmp_path, state="completed", include_fa=False)

    render_report(run_dir)

    artifacts = run_dir / "artifacts"
    png_files = list(artifacts.glob("*.png"))
    assert len(png_files) >= 1, f"artifacts/ 下应有至少 1 个 PNG 文件,实际: {[f.name for f in png_files]}"

    # 检查每个 PNG 文件的 magic bytes
    for png_file in png_files:
        header = png_file.read_bytes()[:8]
        assert header == b"\x89PNG\r\n\x1a\n", (
            f"{png_file.name} 应是有效 PNG,实际 header: {header.hex()}"
        )
