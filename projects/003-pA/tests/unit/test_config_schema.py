"""
tests/unit/test_config_schema.py — RunConfig Pydantic schema + config.yaml IO 测试。

覆盖：
- 合法 minimal config 能加载
- 合法 full config 能加载
- 缺必填字段报 ValidationError 带字段名
- extra 字段报 ValidationError（防 typo）
- 字段范围约束拒绝（num_train_epochs=0, learning_rate=1.5, usd_hard_cap=0）
- round-trip：save → load 得到相同对象
- atomic write：写入后文件完整（不留半文件）
- update_config_field：部分字段更新后持久化
- parent_run_id 设置正确（for retry/variant 链）
- get_run_config_path 返回正确路径
- lm-eval task 列表不为空时 EvalConfig 合法
"""

from __future__ import annotations

import os
import tempfile
import threading
from pathlib import Path

import pytest

from pars.ledger.config_schema import (
    BudgetConfig,
    DatasetConfig,
    EnvSnapshot,
    EvalConfig,
    RunConfig,
    TrainingConfig,
)
from pars.ledger.config_io import (
    get_run_config_path,
    load_config,
    save_config,
    update_config_field,
)


# ---------------------------------------------------------------------------
# 测试 fixture 辅助函数
# ---------------------------------------------------------------------------

def _minimal_run_config() -> RunConfig:
    """返回最小合法 RunConfig（仅必填字段）。"""
    return RunConfig(
        run_id="01KPZSDEE8VWSDS83ZS9WHKWES",
        research_question="Qwen3-4B 在 gsm8k 上 LoRA 微调能提升准确率多少？",
        base_model="Qwen/Qwen3-4B",
        dataset=DatasetConfig(
            hf_id="gsm8k",
            split="train",
            n_samples=100,
        ),
        eval=EvalConfig(
            tasks=["gsm8k"],
            n_shot=0,
        ),
        budget=BudgetConfig(
            usd_cap=30.0,
            wall_clock_hours_cap=12.0,
            gpu_hours_cap=10.0,
        ),
    )


def _full_run_config() -> RunConfig:
    """返回完整 RunConfig（含所有可选字段）。"""
    return RunConfig(
        run_id="01KPZSDEE8VWSDS83ZS9WHKWES",
        research_question="Qwen3-4B 在 gsm8k 上 LoRA 微调能提升准确率多少？",
        base_model="Qwen/Qwen3-4B",
        dataset=DatasetConfig(
            hf_id="gsm8k",
            split="train",
            n_samples=100,
        ),
        training=TrainingConfig(
            backend="unsloth",
            lora_rank=16,
            lora_alpha=32,
            lr=2e-4,
            epochs=3,
            batch_size=4,
            max_seq_len=2048,
        ),
        eval=EvalConfig(
            tasks=["gsm8k", "arc_easy"],
            n_shot=5,
            limit=200,
        ),
        budget=BudgetConfig(
            usd_cap=30.0,
            wall_clock_hours_cap=12.0,
            gpu_hours_cap=10.0,
        ),
        env_snapshot=EnvSnapshot(
            python_version="3.12.12",
            platform="linux-x86_64",
            cuda_version="12.4",
            gpu_name="NVIDIA RTX 4090",
            pip_freeze_sha256="abc123def456",
        ),
        notes="第一次 gsm8k LoRA 实验",
        parent_run_id="01KPZSDEE8QWAR241YQN0K394G",
    )


# ---------------------------------------------------------------------------
# T1: 合法 minimal config 能加载
# ---------------------------------------------------------------------------

def test_minimal_config_loads_successfully() -> None:
    """should load successfully when given minimal required fields."""
    cfg = _minimal_run_config()
    assert cfg.run_id == "01KPZSDEE8VWSDS83ZS9WHKWES"
    assert cfg.research_question == "Qwen3-4B 在 gsm8k 上 LoRA 微调能提升准确率多少？"
    assert cfg.base_model == "Qwen/Qwen3-4B"
    assert cfg.training is None  # 可选字段
    assert cfg.env_snapshot is None  # 可选字段
    assert cfg.notes is None  # 可选字段


# ---------------------------------------------------------------------------
# T2: 合法 full config 能加载
# ---------------------------------------------------------------------------

def test_full_config_loads_successfully() -> None:
    """should load successfully when all optional fields are provided."""
    cfg = _full_run_config()
    assert cfg.training is not None
    assert cfg.training.lora_rank == 16
    assert cfg.eval.tasks == ["gsm8k", "arc_easy"]
    assert cfg.parent_run_id == "01KPZSDEE8QWAR241YQN0K394G"
    assert cfg.env_snapshot is not None
    assert cfg.env_snapshot.gpu_name == "NVIDIA RTX 4090"


# ---------------------------------------------------------------------------
# T3: 缺必填字段报 ValidationError 带字段名
# ---------------------------------------------------------------------------

def test_missing_required_field_raises_validation_error_with_field_name() -> None:
    """should raise ValidationError with field name when required field is missing."""
    from pydantic import ValidationError

    with pytest.raises(ValidationError) as exc_info:
        RunConfig(  # 缺少 research_question, base_model 等
            run_id="01KPZSDEE8VWSDS83ZS9WHKWES",
            eval=EvalConfig(tasks=["gsm8k"], n_shot=0),
            budget=BudgetConfig(
                usd_cap=30.0,
                wall_clock_hours_cap=12.0,
                gpu_hours_cap=10.0,
            ),
        )

    # 验证错误信息含缺失字段名
    error_str = str(exc_info.value)
    assert "research_question" in error_str or "base_model" in error_str


# ---------------------------------------------------------------------------
# T4: extra 字段报 ValidationError（防 typo，extra="forbid"）
# ---------------------------------------------------------------------------

def test_extra_field_raises_validation_error() -> None:
    """should raise ValidationError when unknown extra field is provided (extra=forbid)."""
    from pydantic import ValidationError

    with pytest.raises(ValidationError) as exc_info:
        RunConfig(
            run_id="01KPZSDEE8VWSDS83ZS9WHKWES",
            research_question="test?",
            base_model="Qwen/Qwen3-4B",
            dataset=DatasetConfig(hf_id="gsm8k", split="train", n_samples=100),
            eval=EvalConfig(tasks=["gsm8k"], n_shot=0),
            budget=BudgetConfig(
                usd_cap=30.0, wall_clock_hours_cap=12.0, gpu_hours_cap=10.0
            ),
            typo_field="oops",  # 不存在的字段
        )

    assert "typo_field" in str(exc_info.value) or "extra" in str(exc_info.value).lower()


# ---------------------------------------------------------------------------
# T5: TrainingConfig epochs 范围约束（ge=1）
# ---------------------------------------------------------------------------

def test_training_epochs_zero_raises_validation_error() -> None:
    """should raise ValidationError when epochs=0 (ge=1 constraint)."""
    from pydantic import ValidationError

    with pytest.raises(ValidationError) as exc_info:
        TrainingConfig(
            backend="unsloth",
            lora_rank=16,
            lora_alpha=32,
            lr=2e-4,
            epochs=0,  # 违反 ge=1
            batch_size=4,
            max_seq_len=2048,
        )

    assert "epochs" in str(exc_info.value)


# ---------------------------------------------------------------------------
# T6: TrainingConfig learning_rate=1.5 拒绝（lt=1）
# ---------------------------------------------------------------------------

def test_training_lr_exceeds_limit_raises_validation_error() -> None:
    """should raise ValidationError when lr=1.5 (must be lt=1)."""
    from pydantic import ValidationError

    with pytest.raises(ValidationError) as exc_info:
        TrainingConfig(
            backend="unsloth",
            lora_rank=16,
            lora_alpha=32,
            lr=1.5,  # 违反 lt=1
            epochs=3,
            batch_size=4,
            max_seq_len=2048,
        )

    assert "lr" in str(exc_info.value)


# ---------------------------------------------------------------------------
# T7: BudgetConfig usd_cap=0 拒绝（gt=0）
# ---------------------------------------------------------------------------

def test_budget_usd_cap_zero_raises_validation_error() -> None:
    """should raise ValidationError when usd_cap=0 (gt=0 constraint)."""
    from pydantic import ValidationError

    with pytest.raises(ValidationError) as exc_info:
        BudgetConfig(
            usd_cap=0.0,  # 违反 gt=0
            wall_clock_hours_cap=12.0,
            gpu_hours_cap=10.0,
        )

    assert "usd_cap" in str(exc_info.value)


# ---------------------------------------------------------------------------
# T8: round-trip: save → load 得到相同对象
# ---------------------------------------------------------------------------

def test_round_trip_save_load_produces_equal_config(tmp_path: Path) -> None:
    """should produce an equal config object after save → load round-trip."""
    cfg = _full_run_config()
    yaml_path = tmp_path / "config.yaml"

    save_config(cfg, yaml_path)
    loaded = load_config(yaml_path)

    assert loaded == cfg


# ---------------------------------------------------------------------------
# T9: atomic write：写入后文件完整，不留半文件
# ---------------------------------------------------------------------------

def test_atomic_write_leaves_no_temp_file(tmp_path: Path) -> None:
    """should leave no .tmp file after save completes (atomic write)."""
    cfg = _minimal_run_config()
    yaml_path = tmp_path / "config.yaml"

    save_config(cfg, yaml_path)

    # 目标文件存在
    assert yaml_path.exists()
    # 没有遗留的 .tmp 文件
    tmp_files = list(tmp_path.glob("*.tmp"))
    assert len(tmp_files) == 0, f"残留 .tmp 文件: {tmp_files}"


# ---------------------------------------------------------------------------
# T10: update_config_field：部分字段更新后持久化
# ---------------------------------------------------------------------------

def test_update_config_field_persists_change(tmp_path: Path) -> None:
    """should persist field update when update_config_field is called."""
    cfg = _minimal_run_config()
    yaml_path = tmp_path / "config.yaml"
    save_config(cfg, yaml_path)

    # 更新 notes 字段
    update_config_field(yaml_path, "notes", "更新后的备注")

    reloaded = load_config(yaml_path)
    assert reloaded.notes == "更新后的备注"


# ---------------------------------------------------------------------------
# T11: parent_run_id 设置正确（for retry/variant 链）
# ---------------------------------------------------------------------------

def test_parent_run_id_is_preserved_in_round_trip(tmp_path: Path) -> None:
    """should preserve parent_run_id after save → load for retry/variant chain."""
    parent_id = "01KPZSDEE8QWAR241YQN0K394G"
    cfg = RunConfig(
        run_id="01KPZSDEE8VWSDS83ZS9WHKWES",
        research_question="retry 实验？",
        base_model="Qwen/Qwen3-4B",
        dataset=DatasetConfig(hf_id="gsm8k", split="train", n_samples=100),
        eval=EvalConfig(tasks=["gsm8k"], n_shot=0),
        budget=BudgetConfig(
            usd_cap=30.0, wall_clock_hours_cap=12.0, gpu_hours_cap=10.0
        ),
        parent_run_id=parent_id,
    )

    yaml_path = tmp_path / "config.yaml"
    save_config(cfg, yaml_path)
    loaded = load_config(yaml_path)

    assert loaded.parent_run_id == parent_id


# ---------------------------------------------------------------------------
# T12: get_run_config_path 返回正确路径
# ---------------------------------------------------------------------------

def test_get_run_config_path_returns_correct_path(tmp_path: Path) -> None:
    """should return <run_dir>/config.yaml as the standard config path."""
    run_id = "01KPZSDEE8VWSDS83ZS9WHKWES"
    # 设置环境变量指向 tmp_path，避免影响真实文件系统
    original = os.environ.get("RECALLKIT_RUN_DIR")
    try:
        os.environ["RECALLKIT_RUN_DIR"] = str(tmp_path)
        config_path = get_run_config_path(run_id)
        assert config_path == tmp_path / run_id / "config.yaml"
    finally:
        if original is None:
            os.environ.pop("RECALLKIT_RUN_DIR", None)
        else:
            os.environ["RECALLKIT_RUN_DIR"] = original


# ---------------------------------------------------------------------------
# T13: load_config 对不存在的文件抛 FileNotFoundError
# ---------------------------------------------------------------------------

def test_load_config_raises_file_not_found_when_missing(tmp_path: Path) -> None:
    """should raise FileNotFoundError when config.yaml does not exist."""
    missing_path = tmp_path / "nonexistent" / "config.yaml"

    with pytest.raises(FileNotFoundError):
        load_config(missing_path)


# ---------------------------------------------------------------------------
# T14: concurrent update_config_field 不导致数据丢失（fcntl.flock 互斥）
# ---------------------------------------------------------------------------

def test_concurrent_update_config_field_no_data_loss(tmp_path: Path) -> None:
    """should not lose data when update_config_field is called concurrently (flock)."""
    cfg = _minimal_run_config()
    yaml_path = tmp_path / "config.yaml"
    save_config(cfg, yaml_path)

    errors: list[Exception] = []

    def worker(note: str) -> None:
        try:
            update_config_field(yaml_path, "notes", note)
        except Exception as e:  # noqa: BLE001
            errors.append(e)

    threads = [threading.Thread(target=worker, args=(f"note_{i}",)) for i in range(5)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    # 无异常
    assert len(errors) == 0, f"并发更新出现错误: {errors}"
    # 文件仍然可读且合法
    final = load_config(yaml_path)
    assert final.notes is not None
    assert final.notes.startswith("note_")
