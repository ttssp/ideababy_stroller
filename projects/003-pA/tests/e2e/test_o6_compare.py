"""
tests/e2e/test_o6_compare.py — T026 Outcome O6 E2E 测试。

结论：验证 compare() 在两个 run 之间返回正确的 "pick runX" verdict，
      并遵守 eval_score 优先 → wall_clock 次之 → usd 次之的决策顺序。

## 验证 Outcome O6

O6（architecture §9）：run 对比 —
compare(run_a, run_b) 必须返回 ComparisonResult.verdict == "pick runA" 或 "pick runB"。
决策顺序：eval_score 高者 → wall_clock 短者 → usd 少者 → runA（先入先出）。
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from pars.compare.engine import compare


# ---------------------------------------------------------------------------
# 辅助函数：创建合成 run 目录
# ---------------------------------------------------------------------------


def _make_run_dir(
    runs_root: Path,
    run_id: str,
    *,
    gsm8k_acc: float | None = None,
    wall_clock_seconds: float = 0.0,
    usd_total: float = 0.0,
) -> Path:
    """在 runs_root 下创建符合 compare() 要求的最小 run 目录结构。

    结论：
    - config.yaml 含 wall_clock_seconds / usd_total（compare 的次要决策依据）
    - metrics.jsonl 含 phase=evaluating kind=eval 的 gsm8k 记录
    """
    run_dir = runs_root / run_id
    run_dir.mkdir(parents=True)

    # config.yaml（raw dict，compare 使用 _load_config_dict 读取）
    config_content = f"wall_clock_seconds: {wall_clock_seconds}\nusd_total: {usd_total}\n"
    (run_dir / "config.yaml").write_text(config_content, encoding="utf-8")

    # metrics.jsonl — 按 compare engine 格式要求
    lines = []
    if gsm8k_acc is not None:
        metric = {
            "phase": "evaluating",
            "kind": "eval",
            "data": {
                "task_name": "gsm8k",
                "acc": gsm8k_acc,
                "acc_norm": gsm8k_acc,
            },
            "ts": "2026-01-01T00:04:00+00:00",
        }
        lines.append(json.dumps(metric))

    (run_dir / "metrics.jsonl").write_text("\n".join(lines) + "\n", encoding="utf-8")

    return run_dir


# ---------------------------------------------------------------------------
# T026-O6-TC01: eval_score 高者胜出 → verdict == "pick runA"
# ---------------------------------------------------------------------------


@pytest.mark.e2e
def test_o6_higher_eval_score_wins(tmp_runs_dir: Path) -> None:
    """should return 'pick runA' when runA has higher gsm8k accuracy.

    结论：eval_score 是第一优先级决策因子，runA=0.57 > runB=0.32 → pick runA。
    """
    _make_run_dir(tmp_runs_dir, "run-a-better", gsm8k_acc=0.57, wall_clock_seconds=300.0)
    _make_run_dir(tmp_runs_dir, "run-b-worse",  gsm8k_acc=0.32, wall_clock_seconds=200.0)

    result = compare("run-a-better", "run-b-worse", runs_root=tmp_runs_dir)

    assert result.verdict == "pick runA", (
        f"runA gsm8k=0.57 > runB gsm8k=0.32，verdict 应为 'pick runA'，"
        f"实际：{result.verdict!r}，reason={result.verdict_reason!r}"
    )


# ---------------------------------------------------------------------------
# T026-O6-TC02: eval_score 低者应输 → verdict == "pick runB"
# ---------------------------------------------------------------------------


@pytest.mark.e2e
def test_o6_lower_eval_score_loses(tmp_runs_dir: Path) -> None:
    """should return 'pick runB' when runB has higher gsm8k accuracy.

    结论：runA=0.25 < runB=0.61 → pick runB。
    """
    _make_run_dir(tmp_runs_dir, "run-a-lose", gsm8k_acc=0.25, wall_clock_seconds=200.0)
    _make_run_dir(tmp_runs_dir, "run-b-win",  gsm8k_acc=0.61, wall_clock_seconds=350.0)

    result = compare("run-a-lose", "run-b-win", runs_root=tmp_runs_dir)

    assert result.verdict == "pick runB", (
        f"runB gsm8k=0.61 > runA gsm8k=0.25，verdict 应为 'pick runB'，"
        f"实际：{result.verdict!r}，reason={result.verdict_reason!r}"
    )


# ---------------------------------------------------------------------------
# T026-O6-TC03: eval_score 相同 → wall_clock 短者胜出
# ---------------------------------------------------------------------------


@pytest.mark.e2e
def test_o6_tiebreak_wall_clock_shorter_wins(tmp_runs_dir: Path) -> None:
    """should break tie by wall_clock_seconds when eval scores are equal (shorter wins).

    结论：eval_score 相同（0.50 == 0.50），runA wall_clock=200s < runB wall_clock=400s
          → pick runA（更快）。
    """
    _make_run_dir(tmp_runs_dir, "run-a-fast", gsm8k_acc=0.50, wall_clock_seconds=200.0)
    _make_run_dir(tmp_runs_dir, "run-b-slow", gsm8k_acc=0.50, wall_clock_seconds=400.0)

    result = compare("run-a-fast", "run-b-slow", runs_root=tmp_runs_dir)

    assert result.verdict == "pick runA", (
        f"eval_score 相同时，wall_clock 200s < 400s → verdict 应为 'pick runA'，"
        f"实际：{result.verdict!r}，reason={result.verdict_reason!r}"
    )


# ---------------------------------------------------------------------------
# T026-O6-TC04: ComparisonResult 契约 — verdict / verdict_reason / metrics 字段
# ---------------------------------------------------------------------------


@pytest.mark.e2e
def test_o6_comparison_result_has_required_fields(tmp_runs_dir: Path) -> None:
    """should return ComparisonResult with verdict, verdict_reason, and metrics fields.

    结论：验证 ComparisonResult 字段契约（O6 schema 要求）。
    """
    from pars.compare.engine import ComparisonResult

    _make_run_dir(tmp_runs_dir, "run-a-fields", gsm8k_acc=0.45)
    _make_run_dir(tmp_runs_dir, "run-b-fields", gsm8k_acc=0.30)

    result = compare("run-a-fields", "run-b-fields", runs_root=tmp_runs_dir)

    # 类型契约
    assert isinstance(result, ComparisonResult), "compare() 应返回 ComparisonResult 实例"

    # verdict 字段：只能是 "pick runA" 或 "pick runB"
    assert result.verdict in {"pick runA", "pick runB"}, (
        f"verdict 应为 'pick runA' 或 'pick runB'，实际：{result.verdict!r}"
    )

    # verdict_reason：非空字符串
    assert isinstance(result.verdict_reason, str), "verdict_reason 应为字符串"
    assert len(result.verdict_reason.strip()) > 0, "verdict_reason 不得为空"

    # metrics：列表（可为空，但通常包含 eval_score / wall_clock / usd）
    assert isinstance(result.metrics, list), "metrics 应为列表"


# ---------------------------------------------------------------------------
# T026-O6-TC05: 两个 run 均无 eval_score 时抛出 ValueError
# ---------------------------------------------------------------------------


@pytest.mark.e2e
def test_o6_raises_when_both_runs_have_no_eval_score(tmp_runs_dir: Path) -> None:
    """should raise ValueError when both runs have no eval_score data.

    结论：两个 run 的 metrics.jsonl 均无 phase=evaluating kind=eval 记录时，
          compare() 无法决策，应抛出 ValueError。
    """
    _make_run_dir(tmp_runs_dir, "run-a-no-eval", gsm8k_acc=None)
    _make_run_dir(tmp_runs_dir, "run-b-no-eval", gsm8k_acc=None)

    with pytest.raises(ValueError, match="eval_score"):
        compare("run-a-no-eval", "run-b-no-eval", runs_root=tmp_runs_dir)
