"""
tests.unit.test_compare_engine — pars.compare.engine 单元测试 (T025 TDD 红灯阶段)

结论：覆盖 compare_configs / compare_metrics / compare_conclusions /
      format_markdown 及 ComparisonResult / compare() 接口的所有关键路径。
      共 ≥10 个测试用例，遵循 "should ... when ..." 命名约定。
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

# 被测模块（还未实现，此时会失败）
from pars.compare.engine import (
    ComparisonResult,
    DiffRow,
    compare,
    compare_configs,
    compare_conclusions,
    compare_metrics,
    format_markdown,
)


# ---------------------------------------------------------------------------
# compare_configs 测试
# ---------------------------------------------------------------------------


def test_compare_configs_should_return_empty_when_configs_are_identical():
    """两个完全相同的 config → diff 列表为空。"""
    cfg_a = {
        "run_id": "AAAA",
        "training": {"lora_rank": 8, "lora_alpha": 16, "lr": 0.0002},
    }
    cfg_b = {
        "run_id": "BBBB",
        "training": {"lora_rank": 8, "lora_alpha": 16, "lr": 0.0002},
    }
    diffs = compare_configs(cfg_a, cfg_b)
    # run_id 字段差异应被过滤掉（仅报告超参数差异）
    # 其余字段完全相同 → 空列表
    assert diffs == []


def test_compare_configs_should_surface_lora_rank_diff_when_ranks_differ():
    """lora_rank 不同 → DiffRow 中应出现该字段。"""
    cfg_a = {"training": {"lora_rank": 8}}
    cfg_b = {"training": {"lora_rank": 16}}
    diffs = compare_configs(cfg_a, cfg_b)
    fields = [row.field for row in diffs]
    assert "training.lora_rank" in fields


def test_compare_configs_should_surface_lr_diff_when_lr_differs():
    """lr 不同 → DiffRow 中应出现 training.lr。"""
    cfg_a = {"training": {"lora_rank": 8, "lr": 2e-4}}
    cfg_b = {"training": {"lora_rank": 8, "lr": 1e-4}}
    diffs = compare_configs(cfg_a, cfg_b)
    fields = [row.field for row in diffs]
    assert "training.lr" in fields


def test_compare_configs_should_include_value_a_and_value_b_in_diff_row():
    """DiffRow 的 value_a / value_b 字段应携带原始值。"""
    cfg_a = {"training": {"lora_rank": 8}}
    cfg_b = {"training": {"lora_rank": 16}}
    diffs = compare_configs(cfg_a, cfg_b)
    rank_row = next(r for r in diffs if r.field == "training.lora_rank")
    assert rank_row.value_a == 8
    assert rank_row.value_b == 16


# ---------------------------------------------------------------------------
# compare_metrics 测试
# ---------------------------------------------------------------------------


def test_compare_metrics_should_surface_eval_score_diff_when_scores_differ(tmp_path: Path):
    """两个 run 的 eval_score 不同 → metrics_diffs 应包含该 task 的条目。"""
    # 构造 run_a / run_b 的 metrics.jsonl（含 eval kind 记录）
    runa_dir = tmp_path / "run_a"
    runb_dir = tmp_path / "run_b"
    runa_dir.mkdir()
    runb_dir.mkdir()

    _write_eval_metric(runa_dir, task_name="gsm8k", acc=0.41)
    _write_eval_metric(runb_dir, task_name="gsm8k", acc=0.57)

    diffs = compare_metrics("run_a", "run_b", runs_root=tmp_path)
    fields = [row.field for row in diffs]
    assert any("gsm8k" in f for f in fields)


def test_compare_metrics_should_show_only_in_a_when_task_missing_in_b(tmp_path: Path):
    """run_a 跑了 gsm8k，run_b 没有 → 应出现 '(only in A)' 标记。"""
    runa_dir = tmp_path / "run_a"
    runb_dir = tmp_path / "run_b"
    runa_dir.mkdir()
    runb_dir.mkdir()

    _write_eval_metric(runa_dir, task_name="gsm8k", acc=0.41)
    # run_b 无 eval 记录

    diffs = compare_metrics("run_a", "run_b", runs_root=tmp_path)
    # 有 gsm8k 行，且 value_b 表示 "only in A"
    gsm_rows = [r for r in diffs if "gsm8k" in r.field]
    assert len(gsm_rows) > 0
    assert "(only in A)" in str(gsm_rows[0].value_b)


def test_compare_metrics_should_show_only_in_b_when_task_missing_in_a(tmp_path: Path):
    """run_a 没有 eval，run_b 跑了 → 应出现 '(only in B)' 标记。"""
    runa_dir = tmp_path / "run_a"
    runb_dir = tmp_path / "run_b"
    runa_dir.mkdir()
    runb_dir.mkdir()

    _write_eval_metric(runb_dir, task_name="gsm8k", acc=0.57)

    diffs = compare_metrics("run_a", "run_b", runs_root=tmp_path)
    gsm_rows = [r for r in diffs if "gsm8k" in r.field]
    assert len(gsm_rows) > 0
    assert "(only in B)" in str(gsm_rows[0].value_a)


# ---------------------------------------------------------------------------
# compare_conclusions 测试
# ---------------------------------------------------------------------------


def test_compare_conclusions_should_extract_decision_section_when_present(tmp_path: Path):
    """report.md 有 ## 决策 section → 应返回该 section 内容的 diff。"""
    report_a = tmp_path / "report_a.md"
    report_b = tmp_path / "report_b.md"
    report_a.write_text(
        "## 元数据\n一些元数据\n## 决策\n继续训练，gsm8k 有提升。\n",
        encoding="utf-8",
    )
    report_b.write_text(
        "## 元数据\n一些元数据\n## 决策\n停止，loss 上升。\n",
        encoding="utf-8",
    )

    diffs = compare_conclusions(report_a, report_b)
    assert len(diffs) > 0
    # 内容含各自的决策文字
    row = diffs[0]
    assert "继续" in str(row.value_a)
    assert "停止" in str(row.value_b)


def test_compare_conclusions_should_return_no_decision_section_when_missing(tmp_path: Path):
    """report.md 缺少 ## 决策 section → 应返回 '(no decision section)' 标记。"""
    report_a = tmp_path / "report_a.md"
    report_b = tmp_path / "report_b.md"
    report_a.write_text("## 元数据\n只有元数据，没有决策。\n", encoding="utf-8")
    report_b.write_text("## 决策\n停止。\n", encoding="utf-8")

    diffs = compare_conclusions(report_a, report_b)
    row = diffs[0]
    assert "(no decision section)" in str(row.value_a)


# ---------------------------------------------------------------------------
# format_markdown 测试
# ---------------------------------------------------------------------------


def test_format_markdown_should_contain_three_h2_sections_when_all_diffs_provided():
    """format_markdown 的输出应包含 ## Config diff / ## Metric diff / ## Conclusion diff 三个 H2。"""
    config_diffs = [DiffRow("training.lora_rank", 8, 16)]
    metric_diffs = [DiffRow("gsm8k.acc", 0.41, 0.57)]
    conclusion_diffs = [DiffRow("decision", "继续", "停止")]

    md = format_markdown(config_diffs, metric_diffs, conclusion_diffs)
    assert "## Config diff" in md
    assert "## Metric diff" in md
    assert "## Conclusion diff" in md


def test_format_markdown_should_include_lora_rank_in_config_table_when_rank_differs():
    """Config diff section 应包含 lora_rank 字段。"""
    config_diffs = [DiffRow("training.lora_rank", 8, 16)]
    md = format_markdown(config_diffs, [], [])
    assert "lora_rank" in md


# ---------------------------------------------------------------------------
# compare() / ComparisonResult 接口测试（Prompt 追加的 O6 决策 contract）
# ---------------------------------------------------------------------------


def test_compare_should_pick_run_b_when_b_has_higher_eval_score(tmp_path: Path):
    """runB 的 eval_score 高 → verdict 应为 'pick runB'。"""
    _make_full_run(tmp_path, "run_a", eval_score=0.41, wall_clock_s=7200.0, usd=12.5)
    _make_full_run(tmp_path, "run_b", eval_score=0.57, wall_clock_s=9000.0, usd=18.0)

    result = compare("run_a", "run_b", runs_root=tmp_path)
    assert isinstance(result, ComparisonResult)
    assert result.verdict == "pick runB"
    assert "runB" in result.verdict_reason


def test_compare_should_pick_run_a_when_a_has_higher_eval_score(tmp_path: Path):
    """runA 的 eval_score 高 → verdict 应为 'pick runA'。"""
    _make_full_run(tmp_path, "run_a", eval_score=0.70, wall_clock_s=7200.0, usd=12.5)
    _make_full_run(tmp_path, "run_b", eval_score=0.57, wall_clock_s=9000.0, usd=18.0)

    result = compare("run_a", "run_b", runs_root=tmp_path)
    assert result.verdict == "pick runA"
    assert "runA" in result.verdict_reason


def test_compare_should_use_wall_clock_as_tiebreaker_when_eval_scores_equal(tmp_path: Path):
    """eval_score 相同时，wall_clock 短的胜出（tiebreaker）。"""
    _make_full_run(tmp_path, "run_a", eval_score=0.57, wall_clock_s=6000.0, usd=12.5)
    _make_full_run(tmp_path, "run_b", eval_score=0.57, wall_clock_s=9000.0, usd=18.0)

    result = compare("run_a", "run_b", runs_root=tmp_path)
    # run_a wall_clock 更短，应胜出
    assert result.verdict == "pick runA"


def test_compare_should_use_usd_as_second_tiebreaker_when_eval_and_time_equal(tmp_path: Path):
    """eval_score 和 wall_clock 都相同时，usd 少的胜出（第二 tiebreaker）。"""
    _make_full_run(tmp_path, "run_a", eval_score=0.57, wall_clock_s=7200.0, usd=10.0)
    _make_full_run(tmp_path, "run_b", eval_score=0.57, wall_clock_s=7200.0, usd=18.0)

    result = compare("run_a", "run_b", runs_root=tmp_path)
    # run_a usd 更少，应胜出
    assert result.verdict == "pick runA"


def test_compare_should_raise_when_eval_score_missing(tmp_path: Path):
    """缺少 eval_score 数据时，compare() 应 raise ValueError。"""
    # 造两个没有 eval 记录的 run
    runa_dir = tmp_path / "run_a"
    runb_dir = tmp_path / "run_b"
    runa_dir.mkdir(parents=True)
    runb_dir.mkdir(parents=True)
    # 只写 config，不写 eval metrics
    _write_config(runa_dir, "run_a", wall_clock_s=7200.0, usd=12.5)
    _write_config(runb_dir, "run_b", wall_clock_s=9000.0, usd=18.0)

    with pytest.raises(ValueError, match="eval_score"):
        compare("run_a", "run_b", runs_root=tmp_path)


def test_compare_should_surface_config_diff_in_result_when_configs_differ(tmp_path: Path):
    """config 不同时，ComparisonResult.metrics 中应包含 config diff 信息。"""
    _make_full_run(tmp_path, "run_a", eval_score=0.57, lora_rank=8)
    _make_full_run(tmp_path, "run_b", eval_score=0.60, lora_rank=16)

    result = compare("run_a", "run_b", runs_root=tmp_path)
    # result.metrics 中应有 training.lora_rank 行
    metric_names = [m.metric for m in result.metrics]
    assert any("lora_rank" in n for n in metric_names)


def test_compare_result_should_have_correct_run_ids(tmp_path: Path):
    """ComparisonResult.runa_id / runb_id 应与传入的 run_id 一致。"""
    _make_full_run(tmp_path, "run_a", eval_score=0.41)
    _make_full_run(tmp_path, "run_b", eval_score=0.57)

    result = compare("run_a", "run_b", runs_root=tmp_path)
    assert result.runa_id == "run_a"
    assert result.runb_id == "run_b"


def test_compare_wall_clock_and_usd_delta_should_be_correct(tmp_path: Path):
    """MetricRow 中的 delta 计算（value_b - value_a）应正确。"""
    _make_full_run(tmp_path, "run_a", eval_score=0.41, wall_clock_s=7200.0, usd=12.5)
    _make_full_run(tmp_path, "run_b", eval_score=0.57, wall_clock_s=9000.0, usd=18.0)

    result = compare("run_a", "run_b", runs_root=tmp_path)
    metric_map = {m.metric: m for m in result.metrics}

    # wall_clock delta = 9000 - 7200 = 1800
    if "wall_clock_s" in metric_map:
        assert abs(metric_map["wall_clock_s"].delta - 1800.0) < 1.0

    # usd delta = 18.0 - 12.5 = 5.5
    if "usd_spent" in metric_map:
        assert abs(metric_map["usd_spent"].delta - 5.5) < 0.01


# ---------------------------------------------------------------------------
# 内部辅助函数（测试工厂）
# ---------------------------------------------------------------------------


def _write_eval_metric(run_dir: Path, task_name: str, acc: float) -> None:
    """向 run_dir/metrics.jsonl 写入一条 eval 记录。"""
    metrics_path = run_dir / "metrics.jsonl"
    record = {
        "ts": "2026-04-24T00:00:00+00:00",
        "phase": "evaluating",
        "kind": "eval",
        "data": {"task_name": task_name, "acc": acc},
    }
    with metrics_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")


def _write_config(run_dir: Path, run_id: str, wall_clock_s: float | None = None,
                   usd: float | None = None, lora_rank: int = 16) -> None:
    """向 run_dir/config.yaml 写入简化的 RunConfig。"""
    import yaml
    cfg = {
        "run_id": run_id,
        "research_question": "test question",
        "base_model": "Qwen/Qwen3-4B",
        "dataset": {"hf_id": "gsm8k", "split": "test", "n_samples": 100},
        "training": {
            "backend": "unsloth",
            "lora_rank": lora_rank,
            "lora_alpha": 32,
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
    config_path = run_dir / "config.yaml"
    config_path.write_text(yaml.safe_dump(cfg, allow_unicode=True), encoding="utf-8")


def _make_full_run(
    tmp_path: Path,
    run_id: str,
    *,
    eval_score: float,
    wall_clock_s: float = 7200.0,
    usd: float = 12.5,
    lora_rank: int = 16,
) -> None:
    """构造一个完整的 run 目录（config + eval metrics）。"""
    run_dir_path = tmp_path / run_id
    run_dir_path.mkdir(parents=True, exist_ok=True)
    _write_config(run_dir_path, run_id, wall_clock_s=wall_clock_s, usd=usd, lora_rank=lora_rank)
    _write_eval_metric(run_dir_path, "gsm8k", eval_score)
