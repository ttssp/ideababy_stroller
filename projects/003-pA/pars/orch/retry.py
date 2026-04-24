"""
pars.orch.retry — retry run 配置派生 + 编排启动（T024 · U4）。

结论：
  - derive_retry_config: 读取 parent config → copy → 应用 hypothesis 自动建议 →
    应用 CLI explicit overrides（优先级最高）→ 新 run_id → 写 retry 元数据
  - start_retry: 调用 derive_retry_config + RunOrchestrator.start
  - config_diff: 返回 old vs new config 的差异列表（辅助诊断）

## 优先级（高 → 低）

  1. CLI 显式 override（--lr / --epochs / --lora-rank 等）
  2. hypothesis 关键词自动建议（"LR 太高" → lr /= 3 等）
  3. parent config 继承值

## hypothesis 关键词 → 自动建议 mapping

  "LR 太高"  → lr /= 3
  "LR 太低"  → lr *= 3
  "epoch 不足" → epochs += 2
  "rank 不足" → lora_rank *= 2
  其他       → 仅记录 hypothesis，不自动修改

## 退出码约定（继承自 RunOrchestrator）

  0 = completed
  2 = config 错误
  3 = stuck
  4 = budget
  5 = worker crash
"""

from __future__ import annotations

import copy
from datetime import datetime, timezone
from typing import Any

from pars.ledger import (
    DatasetConfig,
    EvalConfig,
    RunConfig,
    TrainingConfig,
    generate_ulid,
)
from pars.ledger.config_io import get_run_config_path, load_config
from pars.logging import get_logger
from pars.orch.orchestrator import RunHandle, RunOrchestrator

logger = get_logger(__name__)


# ---------------------------------------------------------------------------
# 内部：加载 parent config（可被测试 patch）
# ---------------------------------------------------------------------------

def load_parent_config(run_id: str) -> RunConfig:
    """加载 parent run 的 RunConfig。

    参数：
        run_id: parent run 的 ULID

    返回：
        RunConfig 对象

    异常：
        FileNotFoundError: run 不存在或 config.yaml 不可读
    """
    config_path = get_run_config_path(run_id)
    return load_config(config_path)


# ---------------------------------------------------------------------------
# 内部：hypothesis 关键词 → 训练参数自动建议
# ---------------------------------------------------------------------------

_HYPOTHESIS_RULES: list[tuple[str, str, Any]] = [
    # (关键词, 字段名, 操作描述)  操作通过 callable 实现
]


def _apply_hypothesis_auto_suggest(
    training: TrainingConfig,
    hypothesis: str,
) -> dict[str, Any]:
    """根据 hypothesis 关键词返回推荐的 override 字典（不直接修改 training）。

    规则（spec T024.md §Implementation plan 步骤 3）：
      "LR 太高"  → lr /= 3
      "LR 太低"  → lr *= 3
      "epoch 不足" → epochs += 2
      "rank 不足" → lora_rank *= 2
      其他       → {} (空 dict)

    返回：
        dict — 推荐的 override（字段名 → 推荐值）；空 dict 表示无建议
    """
    suggested: dict[str, Any] = {}

    if "LR 太高" in hypothesis:
        suggested["lr"] = training.lr / 3
        logger.info(
            "hypothesis 自动建议：LR 太高 → lr/=3",
            extra={"original_lr": training.lr, "suggested_lr": suggested["lr"]},
        )

    if "LR 太低" in hypothesis:
        suggested["lr"] = training.lr * 3
        logger.info(
            "hypothesis 自动建议：LR 太低 → lr*=3",
            extra={"original_lr": training.lr, "suggested_lr": suggested["lr"]},
        )

    if "epoch 不足" in hypothesis:
        suggested["epochs"] = training.epochs + 2
        logger.info(
            "hypothesis 自动建议：epoch 不足 → epochs+=2",
            extra={"original_epochs": training.epochs, "suggested_epochs": suggested["epochs"]},
        )

    if "rank 不足" in hypothesis:
        suggested["lora_rank"] = training.lora_rank * 2
        logger.info(
            "hypothesis 自动建议：rank 不足 → lora_rank*=2",
            extra={"original_rank": training.lora_rank, "suggested_rank": suggested["lora_rank"]},
        )

    return suggested


# ---------------------------------------------------------------------------
# 公开 API 1: derive_retry_config
# ---------------------------------------------------------------------------

def derive_retry_config(
    parent_run_id: str,
    hypothesis: str,
    overrides: dict[str, Any],
) -> RunConfig:
    """从 parent run config 派生新的 retry RunConfig。

    优先级（高 → 低）：
      1. CLI 显式 override
      2. hypothesis 自动建议
      3. parent config 继承值

    参数：
        parent_run_id : parent run 的 ULID
        hypothesis    : 本次 retry 的假设文本（必填，不得为空字符串）
        overrides     : CLI 显式 override dict（key = 字段名，value = 新值）

    返回：
        新 RunConfig（含 parent_run_id + retry_hypothesis + 应用 overrides 后的参数）

    异常：
        FileNotFoundError : parent run 不存在
        ValueError        : hypothesis 为空字符串
    """
    # 校验 hypothesis 非空
    if not hypothesis or not hypothesis.strip():
        raise ValueError(
            "hypothesis 不得为空字符串。"
            "请使用 --hypothesis 传入本次 retry 的动机，如 '\"LR 太高，尝试降低 3 倍\"'。"
        )

    # 读取 parent config（FileNotFoundError 由此传播）
    parent = load_parent_config(parent_run_id)

    logger.info(
        "derive_retry_config: 读取 parent config 成功",
        extra={"parent_run_id": parent_run_id, "hypothesis": hypothesis},
    )

    # ------------------------------------------------------------------
    # 构建 training overrides（三层优先级）
    # ------------------------------------------------------------------

    # 1. 从 parent 继承 training 参数（dict 形式）
    parent_training = parent.training
    training_fields: dict[str, Any] = {}

    if parent_training is not None:
        training_fields = {
            "backend": parent_training.backend,
            "lora_rank": parent_training.lora_rank,
            "lora_alpha": parent_training.lora_alpha,
            "lr": parent_training.lr,
            "epochs": parent_training.epochs,
            "batch_size": parent_training.batch_size,
            "max_seq_len": parent_training.max_seq_len,
        }

    # 2. 应用 hypothesis 自动建议（优先于 parent，但低于 CLI override）
    if parent_training is not None:
        suggested = _apply_hypothesis_auto_suggest(parent_training, hypothesis)
        training_fields.update(suggested)

    # 3. 应用 CLI 显式 override（最高优先级）
    # 只处理 TrainingConfig 字段
    training_override_keys = {"lr", "epochs", "lora_rank", "lora_alpha", "batch_size", "max_seq_len"}
    top_level_override_keys = {"research_question"}

    for key, value in overrides.items():
        if key in training_override_keys:
            training_fields[key] = value
        # top-level 字段单独处理（见下方）

    # 构造最终 TrainingConfig
    final_training: TrainingConfig | None = None
    if parent_training is not None:
        final_training = TrainingConfig(**training_fields)

    # ------------------------------------------------------------------
    # 构建 top-level 字段
    # ------------------------------------------------------------------

    # research_question: override > parent
    research_question = overrides.get("research_question", parent.research_question)

    # 新 run_id（ULID）
    new_run_id = generate_ulid()

    # 构造新 RunConfig
    new_config = RunConfig(
        run_id=new_run_id,
        research_question=research_question,
        base_model=parent.base_model,
        dataset=parent.dataset.model_copy(),
        training=final_training,
        eval=parent.eval.model_copy(),
        budget=parent.budget.model_copy(),
        env_snapshot=None,  # retry run 在启动时重新采集
        created_at=datetime.now(timezone.utc),
        # retry 元数据
        parent_run_id=parent_run_id,
        retry_hypothesis=hypothesis,
    )

    logger.info(
        "derive_retry_config: 新 config 派生完成",
        extra={
            "new_run_id": new_run_id,
            "parent_run_id": parent_run_id,
            "overrides_applied": list(overrides.keys()),
        },
    )

    return new_config


# ---------------------------------------------------------------------------
# 公开 API 2: config_diff
# ---------------------------------------------------------------------------

def config_diff(
    old_cfg: RunConfig,
    new_cfg: RunConfig,
) -> list[dict[str, Any]]:
    """返回 old vs new RunConfig 的差异列表。

    结论：扁平化比对，仅报告实际变化的字段（使用点分路径标识嵌套字段）。

    参数：
        old_cfg : 原始 config
        new_cfg : 新 config

    返回：
        list[dict] — 每条记录：{"field": "训练.lr", "old": 2e-4, "new": 1e-5}
    """
    diffs: list[dict[str, Any]] = []

    # 比较 training 子模型
    if old_cfg.training is not None and new_cfg.training is not None:
        old_t = old_cfg.training.model_dump()
        new_t = new_cfg.training.model_dump()
        for key in old_t:
            if old_t[key] != new_t.get(key):
                diffs.append({
                    "field": f"training.{key}",
                    "old": old_t[key],
                    "new": new_t.get(key),
                })

    # 比较顶层字段（排除 run_id / created_at / parent_run_id / retry_hypothesis）
    skip_fields = {
        "run_id", "created_at", "started_at", "completed_at",
        "parent_run_id", "retry_hypothesis", "training",
        "wall_clock_seconds", "usd_total", "gpu_hours",
        "env_snapshot",
    }

    old_top = old_cfg.model_dump(exclude=skip_fields)
    new_top = new_cfg.model_dump(exclude=skip_fields)

    for key in old_top:
        if old_top[key] != new_top.get(key):
            diffs.append({
                "field": key,
                "old": old_top[key],
                "new": new_top.get(key),
            })

    return diffs


# ---------------------------------------------------------------------------
# 公开 API 3: start_retry
# ---------------------------------------------------------------------------

def start_retry(
    parent_run_id: str,
    hypothesis: str,
    overrides: dict[str, Any],
) -> RunHandle:
    """基于 parent run 派生新 config 并启动 retry run。

    逻辑：
      1. derive_retry_config → 得到 new_config
      2. 将 new_config 展开为 RunOrchestrator.start 的关键字参数
      3. 调用 RunOrchestrator.start(...)
      4. 返回 RunHandle

    参数：
        parent_run_id : parent run 的 ULID
        hypothesis    : retry 假设（非空）
        overrides     : CLI 显式 override dict

    返回：
        RunHandle（继承自 RunOrchestrator.start 契约）
    """
    new_config = derive_retry_config(
        parent_run_id=parent_run_id,
        hypothesis=hypothesis,
        overrides=overrides,
    )

    logger.info(
        "start_retry: 开始启动 retry run",
        extra={
            "parent_run_id": parent_run_id,
            "new_run_id": new_config.run_id,
            "hypothesis": hypothesis,
        },
    )

    # 将 RunConfig 展开为 RunOrchestrator.start 参数
    orch = RunOrchestrator()

    training = new_config.training
    lr = training.lr if training else 2e-4
    epochs = training.epochs if training else 3
    lora_rank = training.lora_rank if training else 16
    lora_alpha = training.lora_alpha if training else 32
    batch_size = training.batch_size if training else 2
    max_seq_len = training.max_seq_len if training else 2048

    handle = orch.start(
        research_question=new_config.research_question,
        base_model=new_config.base_model,
        dataset_id=new_config.dataset.hf_id,
        dataset_split=new_config.dataset.split,
        n_samples=new_config.dataset.n_samples,
        lora_rank=lora_rank,
        lora_alpha=lora_alpha,
        lr=lr,
        epochs=epochs,
        batch_size=batch_size,
        max_seq_len=max_seq_len,
        eval_tasks=new_config.eval.tasks,
        usd_cap=new_config.budget.usd_cap,
        wall_clock_hours_cap=new_config.budget.wall_clock_hours_cap,
        gpu_hours_cap=new_config.budget.gpu_hours_cap,
        run_id=new_config.run_id,
    )

    logger.info(
        "start_retry: retry run 完成",
        extra={
            "parent_run_id": parent_run_id,
            "new_run_id": handle.run_id,
            "exit_code": handle.exit_code,
        },
    )

    return handle
