"""
tests.integration.test_compare_two_runs — pars compare 集成测试 (T025 O6)

结论：构造两个完整 run 目录（config + metrics + report.md），
      通过 CLI 调用 `pars compare runA runB`，验证：
      1. stdout 含三个 H2（## Config diff / ## Metric diff / ## Conclusion diff）
      2. lora_rank 出现在 Config diff 表中
      3. verdict 含 "pick run[AB]"

标记：pytest.mark.integration（CI 可选跳过）
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml

# ---------------------------------------------------------------------------
# Pytest 标记（与 conftest.ini 对齐，允许 -m integration 过滤）
# ---------------------------------------------------------------------------

pytestmark = pytest.mark.integration


# ---------------------------------------------------------------------------
# 辅助：构造完整 run 目录
# ---------------------------------------------------------------------------


def _make_run(
    runs_root: Path,
    run_id: str,
    *,
    lora_rank: int,
    eval_score: float,
    wall_clock_s: float = 7200.0,
    usd: float = 12.5,
) -> Path:
    """构造一个完整的 run 目录（config.yaml + metrics.jsonl + report.md）。"""
    run_dir = runs_root / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    # config.yaml
    cfg = {
        "run_id": run_id,
        "research_question": "Does higher lora_rank improve gsm8k accuracy?",
        "base_model": "Qwen/Qwen3-4B",
        "dataset": {"hf_id": "gsm8k", "split": "test", "n_samples": 100},
        "training": {
            "backend": "unsloth",
            "lora_rank": lora_rank,
            "lora_alpha": lora_rank * 2,
            "lr": 0.0002,
            "epochs": 3,
            "batch_size": 4,
            "max_seq_len": 2048,
        },
        "eval": {"backend": "lm-eval", "tasks": ["gsm8k"], "n_shot": 0},
        "budget": {"usd_cap": 30.0, "wall_clock_hours_cap": 12.0, "gpu_hours_cap": 12.0},
        "wall_clock_seconds": wall_clock_s,
        "usd_total": usd,
    }
    (run_dir / "config.yaml").write_text(
        yaml.safe_dump(cfg, allow_unicode=True), encoding="utf-8"
    )

    # metrics.jsonl（含 eval 记录）
    eval_record = {
        "ts": "2026-04-24T00:00:00+00:00",
        "phase": "evaluating",
        "kind": "eval",
        "data": {"task_name": "gsm8k", "acc": eval_score},
    }
    (run_dir / "metrics.jsonl").write_text(
        json.dumps(eval_record) + "\n", encoding="utf-8"
    )

    # report.md（含 ## 决策 section，模拟 T021 输出）
    decision_text = "继续" if eval_score >= 0.5 else "停止"
    report_content = f"""## 元数据

run_id: {run_id}
lora_rank: {lora_rank}

## 训练曲线

训练 loss 稳步下降。

## 分数对比

| metric | baseline | sft | delta |
|--------|----------|-----|-------|
| gsm8k  | 0.35     | {eval_score:.2f} | {eval_score - 0.35:+.2f} |

## 失败归因

无明显失败。

## 决策

{decision_text}训练。gsm8k acc = {eval_score:.2f}。
"""
    (run_dir / "report.md").write_text(report_content, encoding="utf-8")

    return run_dir


# ---------------------------------------------------------------------------
# 集成测试：CLI 输出验证
# ---------------------------------------------------------------------------


def test_compare_two_runs_should_output_three_h2_sections(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """pars compare runA runB → stdout 应含三个 H2 section。"""
    from click.testing import CliRunner
    from pars.cli.main import cli

    runs_root = tmp_path / "runs"
    _make_run(runs_root, "runA", lora_rank=8, eval_score=0.41)
    _make_run(runs_root, "runB", lora_rank=16, eval_score=0.57)

    monkeypatch.setenv("RECALLKIT_RUN_DIR", str(runs_root))

    runner = CliRunner(mix_stderr=False)
    result = runner.invoke(cli, ["compare", "runA", "runB"])

    assert result.exit_code == 0, f"CLI 退出非 0：\n{result.output}\n{result.exception}"
    assert "## Config diff" in result.output
    assert "## Metric diff" in result.output
    assert "## Conclusion diff" in result.output


def test_compare_two_runs_should_show_lora_rank_in_config_diff(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Config diff 表应包含 lora_rank 行（两个 run 的 lora_rank 不同）。"""
    from click.testing import CliRunner
    from pars.cli.main import cli

    runs_root = tmp_path / "runs"
    _make_run(runs_root, "runA", lora_rank=8, eval_score=0.41)
    _make_run(runs_root, "runB", lora_rank=16, eval_score=0.57)

    monkeypatch.setenv("RECALLKIT_RUN_DIR", str(runs_root))

    runner = CliRunner(mix_stderr=False)
    result = runner.invoke(cli, ["compare", "runA", "runB"])

    assert result.exit_code == 0
    assert "lora_rank" in result.output


def test_compare_two_runs_should_contain_pick_verdict(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """CLI 输出应明确含 'pick runA' 或 'pick runB' 决策字符串。"""
    from click.testing import CliRunner
    from pars.cli.main import cli

    runs_root = tmp_path / "runs"
    _make_run(runs_root, "runA", lora_rank=8, eval_score=0.41)
    _make_run(runs_root, "runB", lora_rank=16, eval_score=0.57, wall_clock_s=9000.0, usd=18.0)

    monkeypatch.setenv("RECALLKIT_RUN_DIR", str(runs_root))

    runner = CliRunner(mix_stderr=False)
    result = runner.invoke(cli, ["compare", "runA", "runB"])

    assert result.exit_code == 0
    # O6 强制要求明确决策，不允许 "results are mixed"
    assert "pick runA" in result.output or "pick runB" in result.output


def test_compare_two_runs_should_pick_higher_eval_score(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """eval_score 高的 run 应被选中（runB acc=0.57 > runA acc=0.41）。"""
    from click.testing import CliRunner
    from pars.cli.main import cli

    runs_root = tmp_path / "runs"
    _make_run(runs_root, "runA", lora_rank=8, eval_score=0.41)
    _make_run(runs_root, "runB", lora_rank=16, eval_score=0.57)

    monkeypatch.setenv("RECALLKIT_RUN_DIR", str(runs_root))

    runner = CliRunner(mix_stderr=False)
    result = runner.invoke(cli, ["compare", "runA", "runB"])

    assert result.exit_code == 0
    assert "pick runB" in result.output


def test_compare_two_runs_write_to_file_when_output_flag_given(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """--output 路径参数存在时，结果应写入文件而非仅打印。"""
    from click.testing import CliRunner
    from pars.cli.main import cli

    runs_root = tmp_path / "runs"
    _make_run(runs_root, "runA", lora_rank=8, eval_score=0.41)
    _make_run(runs_root, "runB", lora_rank=16, eval_score=0.57)
    out_file = tmp_path / "compare_output.md"

    monkeypatch.setenv("RECALLKIT_RUN_DIR", str(runs_root))

    runner = CliRunner(mix_stderr=False)
    result = runner.invoke(cli, ["compare", "runA", "runB", "--output", str(out_file)])

    assert result.exit_code == 0
    assert out_file.exists()
    content = out_file.read_text(encoding="utf-8")
    assert "## Config diff" in content
