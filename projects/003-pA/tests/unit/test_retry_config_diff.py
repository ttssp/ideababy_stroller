"""
tests/unit/test_retry_config_diff.py — T024 retry config 派生逻辑单元测试。

结论：覆盖 derive_retry_config 的全部核心路径：
  - 无 override → 继承所有字段 + retry_from / hypothesis 写入
  - 单字段 override（lr）→ 只 lr 变
  - 多字段 override → 全部生效
  - old_run_id 不存在 → 抛 FileNotFoundError
  - hypothesis 空字符串 → 抛 ValueError
  - hypothesis 关键词自动建议（"LR 太高" → lr /= 3）
  - hypothesis 关键词自动建议（"LR 太低" → lr *= 3）
  - CLI 显式 override 赢过自动建议（优先级最高）
  - diff 辅助函数验证
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest

from pars.ledger import (
    BudgetConfig,
    DatasetConfig,
    EvalConfig,
    RunConfig,
    TrainingConfig,
    generate_ulid,
)


# ---------------------------------------------------------------------------
# 辅助：构造基准 RunConfig（不需要真实磁盘）
# ---------------------------------------------------------------------------

def _make_parent_config(run_id: str | None = None) -> RunConfig:
    """构造一个完整的 parent RunConfig（不写入磁盘）。"""
    if run_id is None:
        run_id = generate_ulid()
    return RunConfig(
        run_id=run_id,
        research_question="原始假设：LoRA rank=16 是否有效？",
        base_model="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
        dataset=DatasetConfig(hf_id="tatsu-lab/alpaca", split="train[:100]", n_samples=100),
        training=TrainingConfig(
            lora_rank=16,
            lora_alpha=32,
            lr=2e-4,
            epochs=3,
            batch_size=2,
            max_seq_len=512,
        ),
        eval=EvalConfig(tasks=["gsm8k"]),
        budget=BudgetConfig(usd_cap=30.0, wall_clock_hours_cap=12.0, gpu_hours_cap=12.0),
    )


# ---------------------------------------------------------------------------
# TC01: 无 override → 完全继承 parent + retry_from/hypothesis 字段
# ---------------------------------------------------------------------------

def test_derive_retry_config_inherits_all_fields_when_no_override(tmp_path: Path) -> None:
    """should inherit all parent fields unchanged when no overrides provided."""
    from pars.orch.retry import derive_retry_config

    parent_id = generate_ulid()
    parent = _make_parent_config(run_id=parent_id)

    with patch("pars.orch.retry.load_parent_config", return_value=parent):
        new_cfg = derive_retry_config(
            parent_run_id=parent_id,
            hypothesis="任意假设",
            overrides={},
        )

    # 新 run_id 与 parent 不同
    assert new_cfg.run_id != parent_id

    # 核心超参继承
    assert new_cfg.training is not None
    assert new_cfg.training.lora_rank == 16  # noqa: PLR2004
    assert new_cfg.training.lora_alpha == 32  # noqa: PLR2004
    assert new_cfg.training.epochs == 3  # noqa: PLR2004
    assert new_cfg.training.batch_size == 2  # noqa: PLR2004

    # retry 元数据写入
    assert new_cfg.parent_run_id == parent_id
    assert new_cfg.retry_hypothesis == "任意假设"

    # 其他字段继承
    assert new_cfg.base_model == parent.base_model
    assert new_cfg.dataset.hf_id == parent.dataset.hf_id
    assert new_cfg.research_question == parent.research_question


# ---------------------------------------------------------------------------
# TC02: lr override → 只 lr 变，其它继承
# ---------------------------------------------------------------------------

def test_derive_retry_config_applies_lr_override(tmp_path: Path) -> None:
    """should apply only lr override, keeping all other fields from parent."""
    from pars.orch.retry import derive_retry_config

    parent_id = generate_ulid()
    parent = _make_parent_config(run_id=parent_id)

    with patch("pars.orch.retry.load_parent_config", return_value=parent):
        new_cfg = derive_retry_config(
            parent_run_id=parent_id,
            hypothesis="测试 lr override",
            overrides={"lr": 1e-5},
        )

    assert new_cfg.training is not None
    assert abs(new_cfg.training.lr - 1e-5) < 1e-10, f"lr 应为 1e-5，实际：{new_cfg.training.lr}"
    # 其它字段不变
    assert new_cfg.training.lora_rank == 16  # noqa: PLR2004
    assert new_cfg.training.epochs == 3  # noqa: PLR2004


# ---------------------------------------------------------------------------
# TC03: 多字段 override → 全部生效
# ---------------------------------------------------------------------------

def test_derive_retry_config_applies_multiple_overrides(tmp_path: Path) -> None:
    """should apply multiple overrides simultaneously."""
    from pars.orch.retry import derive_retry_config

    parent_id = generate_ulid()
    parent = _make_parent_config(run_id=parent_id)

    with patch("pars.orch.retry.load_parent_config", return_value=parent):
        new_cfg = derive_retry_config(
            parent_run_id=parent_id,
            hypothesis="多字段测试",
            overrides={"lr": 5e-5, "epochs": 7, "lora_rank": 32},
        )

    assert new_cfg.training is not None
    assert abs(new_cfg.training.lr - 5e-5) < 1e-10
    assert new_cfg.training.epochs == 7  # noqa: PLR2004
    assert new_cfg.training.lora_rank == 32  # noqa: PLR2004


# ---------------------------------------------------------------------------
# TC04: parent run 不存在 → 抛 FileNotFoundError
# ---------------------------------------------------------------------------

def test_derive_retry_config_raises_when_parent_not_found() -> None:
    """should raise FileNotFoundError when old_run_id does not exist."""
    from pars.orch.retry import derive_retry_config

    fake_id = generate_ulid()

    def raise_not_found(_run_id: str) -> None:
        raise FileNotFoundError(f"run {_run_id} 不存在")

    with patch("pars.orch.retry.load_parent_config", side_effect=raise_not_found):
        with pytest.raises(FileNotFoundError):
            derive_retry_config(
                parent_run_id=fake_id,
                hypothesis="假设",
                overrides={},
            )


# ---------------------------------------------------------------------------
# TC05: hypothesis 空字符串 → 拒绝（必填）
# ---------------------------------------------------------------------------

def test_derive_retry_config_rejects_empty_hypothesis() -> None:
    """should raise ValueError when hypothesis is empty string."""
    from pars.orch.retry import derive_retry_config

    parent_id = generate_ulid()
    parent = _make_parent_config(run_id=parent_id)

    with patch("pars.orch.retry.load_parent_config", return_value=parent):
        with pytest.raises(ValueError, match="hypothesis"):
            derive_retry_config(
                parent_run_id=parent_id,
                hypothesis="",
                overrides={},
            )


# ---------------------------------------------------------------------------
# TC06: hypothesis "LR 太高" → 自动建议 lr /= 3（无显式 lr override 时生效）
# ---------------------------------------------------------------------------

def test_derive_retry_config_auto_suggest_lr_too_high() -> None:
    """should automatically suggest lr /= 3 when hypothesis contains 'LR 太高'."""
    from pars.orch.retry import derive_retry_config

    parent_id = generate_ulid()
    parent = _make_parent_config(run_id=parent_id)
    original_lr = parent.training.lr  # 2e-4

    with patch("pars.orch.retry.load_parent_config", return_value=parent):
        new_cfg = derive_retry_config(
            parent_run_id=parent_id,
            hypothesis="LR 太高，导致 loss 振荡",
            overrides={},
        )

    assert new_cfg.training is not None
    expected_lr = original_lr / 3
    assert abs(new_cfg.training.lr - expected_lr) < 1e-12, (
        f"'LR 太高' 应触发 lr/=3，期望 {expected_lr}，实际 {new_cfg.training.lr}"
    )


# ---------------------------------------------------------------------------
# TC07: hypothesis "LR 太低" → 自动建议 lr *= 3
# ---------------------------------------------------------------------------

def test_derive_retry_config_auto_suggest_lr_too_low() -> None:
    """should automatically suggest lr *= 3 when hypothesis contains 'LR 太低'."""
    from pars.orch.retry import derive_retry_config

    parent_id = generate_ulid()
    parent = _make_parent_config(run_id=parent_id)
    original_lr = parent.training.lr  # 2e-4

    with patch("pars.orch.retry.load_parent_config", return_value=parent):
        new_cfg = derive_retry_config(
            parent_run_id=parent_id,
            hypothesis="LR 太低，loss 下降太慢",
            overrides={},
        )

    assert new_cfg.training is not None
    expected_lr = original_lr * 3
    assert abs(new_cfg.training.lr - expected_lr) < 1e-12, (
        f"'LR 太低' 应触发 lr*=3，期望 {expected_lr}，实际 {new_cfg.training.lr}"
    )


# ---------------------------------------------------------------------------
# TC08: CLI 显式 override 赢过 hypothesis 自动建议（优先级最高）
# ---------------------------------------------------------------------------

def test_derive_retry_config_explicit_override_wins_over_auto_suggest() -> None:
    """should use explicit CLI override instead of hypothesis auto-suggestion."""
    from pars.orch.retry import derive_retry_config

    parent_id = generate_ulid()
    parent = _make_parent_config(run_id=parent_id)

    explicit_lr = 1e-5  # 显式指定，不是 parent.lr / 3

    with patch("pars.orch.retry.load_parent_config", return_value=parent):
        new_cfg = derive_retry_config(
            parent_run_id=parent_id,
            hypothesis="LR 太高",  # 自动建议 lr/=3，但被显式 override 盖掉
            overrides={"lr": explicit_lr},
        )

    assert new_cfg.training is not None
    assert abs(new_cfg.training.lr - explicit_lr) < 1e-12, (
        f"显式 override 应赢得优先级，期望 {explicit_lr}，实际 {new_cfg.training.lr}"
    )


# ---------------------------------------------------------------------------
# TC09: diff_configs 辅助：old vs new 差异列表正确
# ---------------------------------------------------------------------------

def test_config_diff_helper_detects_changed_fields() -> None:
    """should return diff list correctly for changed fields between old and new config."""
    from pars.orch.retry import config_diff

    parent_id = generate_ulid()
    child_id = generate_ulid()

    old_cfg = _make_parent_config(run_id=parent_id)

    # 构造 new config：lr 和 epochs 变化
    new_training = TrainingConfig(
        lora_rank=16,
        lora_alpha=32,
        lr=1e-5,      # 变化
        epochs=5,      # 变化
        batch_size=2,
        max_seq_len=512,
    )
    new_cfg = old_cfg.model_copy(
        update={
            "run_id": child_id,
            "training": new_training,
            "parent_run_id": parent_id,
            "retry_hypothesis": "测试 diff",
        }
    )

    diff = config_diff(old_cfg, new_cfg)

    # diff 应该是一个 list，包含 lr 和 epochs 变化
    changed_keys = {item["field"] for item in diff}
    assert "training.lr" in changed_keys, f"diff 应含 training.lr，实际：{changed_keys}"
    assert "training.epochs" in changed_keys, f"diff 应含 training.epochs，实际：{changed_keys}"


# ---------------------------------------------------------------------------
# TC10: "epoch 不足" → 自动建议 epochs += 2
# ---------------------------------------------------------------------------

def test_derive_retry_config_auto_suggest_epoch_insufficient() -> None:
    """should automatically suggest epochs += 2 when hypothesis contains 'epoch 不足'."""
    from pars.orch.retry import derive_retry_config

    parent_id = generate_ulid()
    parent = _make_parent_config(run_id=parent_id)
    original_epochs = parent.training.epochs  # 3

    with patch("pars.orch.retry.load_parent_config", return_value=parent):
        new_cfg = derive_retry_config(
            parent_run_id=parent_id,
            hypothesis="epoch 不足，验证集还未收敛",
            overrides={},
        )

    assert new_cfg.training is not None
    expected_epochs = original_epochs + 2
    assert new_cfg.training.epochs == expected_epochs, (
        f"'epoch 不足' 应触发 epochs+=2，期望 {expected_epochs}，实际 {new_cfg.training.epochs}"
    )


# ---------------------------------------------------------------------------
# TC11: "rank 不足" → 自动建议 lora_rank *= 2
# ---------------------------------------------------------------------------

def test_derive_retry_config_auto_suggest_rank_insufficient() -> None:
    """should automatically suggest lora_rank *= 2 when hypothesis contains 'rank 不足'."""
    from pars.orch.retry import derive_retry_config

    parent_id = generate_ulid()
    parent = _make_parent_config(run_id=parent_id)
    original_rank = parent.training.lora_rank  # 16

    with patch("pars.orch.retry.load_parent_config", return_value=parent):
        new_cfg = derive_retry_config(
            parent_run_id=parent_id,
            hypothesis="rank 不足，模型容量不够",
            overrides={},
        )

    assert new_cfg.training is not None
    expected_rank = original_rank * 2
    assert new_cfg.training.lora_rank == expected_rank, (
        f"'rank 不足' 应触发 lora_rank*=2，期望 {expected_rank}，实际 {new_cfg.training.lora_rank}"
    )


# ---------------------------------------------------------------------------
# TC12: research_question 通过 --question override 替换
# ---------------------------------------------------------------------------

def test_derive_retry_config_applies_question_override() -> None:
    """should replace research_question when question override is provided."""
    from pars.orch.retry import derive_retry_config

    parent_id = generate_ulid()
    parent = _make_parent_config(run_id=parent_id)

    new_question = "新的研究假设：rank=32 能否提升 GSM8K？"

    with patch("pars.orch.retry.load_parent_config", return_value=parent):
        new_cfg = derive_retry_config(
            parent_run_id=parent_id,
            hypothesis="测试 question override",
            overrides={"research_question": new_question},
        )

    assert new_cfg.research_question == new_question
