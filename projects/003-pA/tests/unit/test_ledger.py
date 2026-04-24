"""
tests/unit/test_ledger.py — Run Ledger 高层 API 单元测试（T009）。

结论：验证 create_run / list_runs / get_run_summary / run_exists 四个高层函数
      在标准路径和边界条件下的正确行为。

测试使用 tmp_runs_dir fixture（conftest 已提供）隔离文件系统副作用。
"""

from __future__ import annotations

from pathlib import Path

import pytest

from pars.ledger.config_schema import (
    BudgetConfig,
    DatasetConfig,
    EvalConfig,
    RunConfig,
)


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


# ---------------------------------------------------------------------------
# T009-TC01: create_run 返回合法 ULID
# ---------------------------------------------------------------------------


def test_create_run_returns_valid_ulid(
    tmp_runs_dir: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """should return a valid 26-char ULID when creating a run."""
    monkeypatch.setenv("RECALLKIT_RUN_DIR", str(tmp_runs_dir))

    from pars.ledger.ledger import create_run
    from pars.ledger.run_id import validate_ulid

    config = _make_run_config()
    run_id = create_run(config)

    assert validate_ulid(run_id), f"create_run 应返回合法 ULID，实际：{run_id!r}"
    assert len(run_id) == 26, f"ULID 应为 26 字符，实际：{len(run_id)}"


# ---------------------------------------------------------------------------
# T009-TC02: create_run 写入 config.yaml
# ---------------------------------------------------------------------------


def test_create_run_writes_config_yaml(
    tmp_runs_dir: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """should write config.yaml under runs/<run_id>/ after create_run."""
    monkeypatch.setenv("RECALLKIT_RUN_DIR", str(tmp_runs_dir))

    from pars.ledger.ledger import create_run
    from pars.ledger.config_io import load_config

    config = _make_run_config()
    run_id = create_run(config)

    config_path = tmp_runs_dir / run_id / "config.yaml"
    assert config_path.exists(), f"config.yaml 应存在于 {config_path}"

    loaded = load_config(config_path)
    assert loaded.research_question == config.research_question
    assert loaded.base_model == config.base_model
    assert loaded.run_id == run_id


# ---------------------------------------------------------------------------
# T009-TC03: create_run 初始化 state.json 为 init phase
# ---------------------------------------------------------------------------


def test_create_run_initializes_state_as_pending(
    tmp_runs_dir: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """should write state.json with phase=init after create_run."""
    monkeypatch.setenv("RECALLKIT_RUN_DIR", str(tmp_runs_dir))

    from pars.ledger.ledger import create_run
    from pars.ledger.state import read_state, RunPhase

    config = _make_run_config()
    run_id = create_run(config)

    state = read_state(run_id)
    assert state.run_id == run_id
    assert state.phase == RunPhase.INIT


# ---------------------------------------------------------------------------
# T009-TC04: create_run 创建完整目录树
# ---------------------------------------------------------------------------


def test_create_run_creates_directory_tree(
    tmp_runs_dir: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """should create runs/<run_id>/ and artifacts/ subdirectory after create_run."""
    monkeypatch.setenv("RECALLKIT_RUN_DIR", str(tmp_runs_dir))

    from pars.ledger.ledger import create_run

    config = _make_run_config()
    run_id = create_run(config)

    run_path = tmp_runs_dir / run_id
    assert run_path.is_dir(), f"run 目录应存在：{run_path}"
    assert (run_path / "artifacts").is_dir(), "artifacts 子目录应存在"


# ---------------------------------------------------------------------------
# T009-TC05: list_runs 空目录返回空列表
# ---------------------------------------------------------------------------


def test_list_runs_empty_dir_returns_empty(
    tmp_runs_dir: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """should return empty list when runs directory is empty."""
    monkeypatch.setenv("RECALLKIT_RUN_DIR", str(tmp_runs_dir))

    from pars.ledger.ledger import list_runs

    result = list_runs()
    assert result == [], f"空目录应返回 []，实际：{result}"


# ---------------------------------------------------------------------------
# T009-TC06: list_runs 按时间倒序排列
# ---------------------------------------------------------------------------


def test_list_runs_ordered_newest_first(
    tmp_runs_dir: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """should return run IDs in newest-first order based on ULID timestamp."""
    monkeypatch.setenv("RECALLKIT_RUN_DIR", str(tmp_runs_dir))

    from pars.ledger.ledger import create_run, list_runs

    config = _make_run_config()
    id1 = create_run(config)
    _id2 = create_run(config)
    id3 = create_run(config)

    runs = list_runs()
    # ULID 是单调递增的，id3 > id2 > id1（字典序），最新在前
    assert runs[0] == id3, f"最新 run 应在首位，实际：{runs}"
    assert runs[-1] == id1, f"最早 run 应在末位，实际：{runs}"


# ---------------------------------------------------------------------------
# T009-TC07: list_runs 忽略非法 ULID 目录名
# ---------------------------------------------------------------------------


def test_list_runs_ignores_invalid_ulid_dirs(
    tmp_runs_dir: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """should ignore directories with names that are not valid ULIDs."""
    monkeypatch.setenv("RECALLKIT_RUN_DIR", str(tmp_runs_dir))

    from pars.ledger.ledger import create_run, list_runs

    # 创建 1 个合法 run
    config = _make_run_config()
    valid_id = create_run(config)

    # 手动创建非法目录名
    (tmp_runs_dir / "not_a_ulid").mkdir()
    (tmp_runs_dir / "INVALID-NAME-123").mkdir()
    (tmp_runs_dir / ".hidden").mkdir()

    runs = list_runs()
    assert valid_id in runs, f"合法 run_id 应在列表中，实际：{runs}"
    assert "not_a_ulid" not in runs
    assert "INVALID-NAME-123" not in runs
    assert ".hidden" not in runs


# ---------------------------------------------------------------------------
# T009-TC08: list_runs 支持 limit 参数
# ---------------------------------------------------------------------------


def test_list_runs_with_limit(
    tmp_runs_dir: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """should return at most limit runs when limit is specified."""
    monkeypatch.setenv("RECALLKIT_RUN_DIR", str(tmp_runs_dir))

    from pars.ledger.ledger import create_run, list_runs

    config = _make_run_config()
    for _ in range(5):
        create_run(config)

    runs = list_runs(limit=3)
    assert len(runs) == 3, f"limit=3 应返回 3 条，实际：{len(runs)}"


# ---------------------------------------------------------------------------
# T009-TC09: get_run_summary 包含必要字段
# ---------------------------------------------------------------------------


def test_get_run_summary_contains_required_fields(
    tmp_runs_dir: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """should return summary dict with name/hypothesis/status/phase keys."""
    monkeypatch.setenv("RECALLKIT_RUN_DIR", str(tmp_runs_dir))

    from pars.ledger.ledger import create_run, get_run_summary

    config = _make_run_config()
    run_id = create_run(config)

    summary = get_run_summary(run_id)

    assert "run_id" in summary, "摘要应含 run_id 字段"
    assert "research_question" in summary, "摘要应含 research_question 字段"
    assert "phase" in summary, "摘要应含 phase 字段"
    assert "status" in summary, "摘要应含 status 字段"
    assert "base_model" in summary, "摘要应含 base_model 字段"
    assert summary["run_id"] == run_id


# ---------------------------------------------------------------------------
# T009-TC10: get_run_summary run 不存在报 FileNotFoundError
# ---------------------------------------------------------------------------


def test_get_run_summary_nonexistent_raises_file_not_found(
    tmp_runs_dir: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """should raise FileNotFoundError when run_id does not exist."""
    monkeypatch.setenv("RECALLKIT_RUN_DIR", str(tmp_runs_dir))

    from pars.ledger.ledger import get_run_summary

    with pytest.raises(FileNotFoundError):
        get_run_summary("01HRRRRRRRRRRRRRRRRRRRRRRRR")


# ---------------------------------------------------------------------------
# T009-TC11: run_exists 存在时返回 True
# ---------------------------------------------------------------------------


def test_run_exists_returns_true_for_existing_run(
    tmp_runs_dir: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """should return True when run_id exists on disk."""
    monkeypatch.setenv("RECALLKIT_RUN_DIR", str(tmp_runs_dir))

    from pars.ledger.ledger import create_run, run_exists

    config = _make_run_config()
    run_id = create_run(config)

    assert run_exists(run_id) is True, "已创建的 run 应存在"


# ---------------------------------------------------------------------------
# T009-TC12: run_exists 不存在时返回 False
# ---------------------------------------------------------------------------


def test_run_exists_returns_false_for_missing_run(
    tmp_runs_dir: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """should return False when run_id does not exist on disk."""
    monkeypatch.setenv("RECALLKIT_RUN_DIR", str(tmp_runs_dir))

    from pars.ledger.ledger import run_exists

    assert run_exists("01HRRRRRRRRRRRRRRRRRRRRRRRR") is False, "不存在的 run 应返回 False"


# ---------------------------------------------------------------------------
# T009-TC13: get_run_summary 包含 budget 使用情况
# ---------------------------------------------------------------------------


def test_get_run_summary_contains_budget_fields(
    tmp_runs_dir: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """should include budget cap and spent fields in run summary."""
    monkeypatch.setenv("RECALLKIT_RUN_DIR", str(tmp_runs_dir))

    from pars.ledger.ledger import create_run, get_run_summary

    config = _make_run_config()
    run_id = create_run(config)

    summary = get_run_summary(run_id)
    # 应含预算上限
    assert "usd_cap" in summary, "摘要应含 usd_cap 字段"
    # 应含已花费
    assert "usd_spent" in summary, "摘要应含 usd_spent 字段"


# ---------------------------------------------------------------------------
# T009-TC14: create_run 写入 run_id 到 config.yaml
# ---------------------------------------------------------------------------


def test_create_run_fills_run_id_in_config(
    tmp_runs_dir: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """should fill run_id in saved config.yaml matching the returned ULID."""
    monkeypatch.setenv("RECALLKIT_RUN_DIR", str(tmp_runs_dir))

    from pars.ledger.ledger import create_run
    from pars.ledger.config_io import load_config

    config = _make_run_config()
    run_id = create_run(config)

    loaded = load_config(tmp_runs_dir / run_id / "config.yaml")
    assert loaded.run_id == run_id, f"config.yaml 内 run_id 应与返回值一致，实际：{loaded.run_id!r}"
