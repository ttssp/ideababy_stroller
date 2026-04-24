"""
tests.integration.test_tinyllama_smoke — TinyLlama 端到端冒烟测试（T016）

结论：
  用 TinyLlama 1.1B + alpaca 子集(100 条)跑完整工作流：
    baseline eval → 1 epoch LoRA SFT → eval
  断言 metrics.jsonl 含三类事件：
    - phase=baseline 的 eval_scores
    - event=train_epoch 的训练记录（>=1 条）
    - event=eval_scores 的 eval 记录（>=1 条）

  由于 Unsloth 依赖 CUDA + Linux，本测试在 macOS / 无 GPU 环境自动 skip。
  CI skip 条件：torch.cuda.is_available() == False 或 sys_platform == darwin

标记：
  @pytest.mark.slow         — 耗时 > 10s
  @pytest.mark.integration  — 需要文件系统 + 真实模型下载

验证规格：specs/003-pA/tasks/T016.md ## Verification
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest


# ---------------------------------------------------------------------------
# Skip 条件：macOS 或无 CUDA GPU → 跳过（CI 上无 GPU 跳过）
# ---------------------------------------------------------------------------

def _has_cuda() -> bool:
    """检查是否有 CUDA 可用 GPU。"""
    try:
        import torch
        return torch.cuda.is_available()
    except ImportError:
        return False


_SKIP_REASON = (
    "TinyLlama 冒烟测试需要 CUDA GPU + Linux（Unsloth 依赖），"
    "macOS / 无 GPU 环境自动跳过。"
    "在 Linux + RTX 4090 环境下用 `pytest -m 'integration and slow'` 运行。"
)

requires_cuda_linux = pytest.mark.skipif(
    not _has_cuda() or sys.platform == "darwin",
    reason=_SKIP_REASON,
)


# ---------------------------------------------------------------------------
# TinyLlama 冒烟测试参数（极小，保证快速 + 可跑通）
# ---------------------------------------------------------------------------

TINYLLAMA_MODEL = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
ALPACA_DATASET = "tatsu-lab/alpaca"
N_SAMPLES = 100  # baseline eval 样本数
LORA_RANK = 4
LORA_ALPHA = 8
LR = 2e-4
EPOCHS = 1
BATCH_SIZE = 2
MAX_SEQ_LEN = 256
EVAL_TASKS = "hellaswag"  # 快速评测任务
EVAL_LIMIT = 20  # smoke test 只跑 20 条 eval


# ---------------------------------------------------------------------------
# 辅助函数
# ---------------------------------------------------------------------------

def _load_metrics(metrics_path: Path) -> list[dict]:
    """读取 metrics.jsonl，返回所有记录 list。"""
    records = []
    with open(metrics_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
    return records


def _run_script(script_path: Path, env: dict) -> subprocess.CompletedProcess:
    """运行渲染好的 Python 脚本，返回 CompletedProcess。"""
    result = subprocess.run(
        [sys.executable, str(script_path)],
        env={**os.environ, **env},
        capture_output=False,  # 显示训练日志，便于调试
        timeout=1800,  # 30 分钟超时（wall-clock < 30min 要求）
    )
    return result


# ---------------------------------------------------------------------------
# 主冒烟测试
# ---------------------------------------------------------------------------

@pytest.mark.slow
@pytest.mark.integration
@requires_cuda_linux
def test_tinyllama_full_workflow_smoke(tmp_path: Path):
    """
    TinyLlama 1.1B + alpaca-100 完整工作流冒烟测试。

    步骤：
      1. 渲染 3 个脚本（baseline / lora / eval）到 artifacts/
      2. 运行 baseline_script.py → 验证 metrics.jsonl 有 baseline 记录
      3. 运行 lora_script.py → 验证 metrics.jsonl 有 train_epoch 记录
      4. 运行 eval_script.py → 验证 metrics.jsonl 有 eval_scores 记录
      5. 断言 scores.json 存在

    断言：
      - metrics.jsonl 含 phase=baseline 的 eval_scores（baseline 评测完成）
      - metrics.jsonl 含 event=train_epoch 的记录（训练至少 1 epoch）
      - metrics.jsonl 含 event=eval_scores 的记录（eval 完成）
      - artifacts/scores.json 存在

    wall-clock 上限：30 分钟（T016 规格）
    """
    from pars.workflow.render import render_template, write_rendered_script

    # ------------------------------------------------------------------
    # 构造临时 run 环境
    # ------------------------------------------------------------------
    run_id = "01TINYLLAMA_SMOKE_TEST000"  # 固定 ID，便于 debug
    run_dir = tmp_path / "runs" / run_id
    ckpt_dir = tmp_path / "checkpoints" / run_id
    hf_home = tmp_path / "hf_cache"

    run_dir.mkdir(parents=True)
    ckpt_dir.mkdir(parents=True)
    hf_home.mkdir(parents=True)
    (run_dir / "artifacts").mkdir(parents=True)

    env_vars = {
        "RECALLKIT_RUN_DIR": str(run_dir),
        "RECALLKIT_CKPT_DIR": str(ckpt_dir),
        "HF_HOME": str(hf_home),
    }

    # ------------------------------------------------------------------
    # 步骤 1：渲染脚本
    # ------------------------------------------------------------------
    # 直接设置 env var 让 write_rendered_script 使用正确路径
    old_run_dir = os.environ.get("RECALLKIT_RUN_DIR")
    old_ckpt_dir = os.environ.get("RECALLKIT_CKPT_DIR")
    old_hf_home = os.environ.get("HF_HOME")

    try:
        os.environ["RECALLKIT_RUN_DIR"] = str(run_dir)
        os.environ["RECALLKIT_CKPT_DIR"] = str(ckpt_dir)
        os.environ["HF_HOME"] = str(hf_home)

        baseline_ctx = {
            "base_model": TINYLLAMA_MODEL,
            "dataset_id": ALPACA_DATASET,
            "dataset_split": "train",
            "n_samples": N_SAMPLES,
            "eval_tasks": EVAL_TASKS,
        }
        lora_ctx = {
            "base_model": TINYLLAMA_MODEL,
            "dataset_id": ALPACA_DATASET,
            "lora_rank": LORA_RANK,
            "lora_alpha": LORA_ALPHA,
            "lr": LR,
            "epochs": EPOCHS,
            "batch_size": BATCH_SIZE,
            "max_seq_len": MAX_SEQ_LEN,
        }
        eval_ctx = {
            "base_model": TINYLLAMA_MODEL,
            "lora_ckpt_dir": str(ckpt_dir / "last"),
            "eval_tasks": EVAL_TASKS,
            "n_shot": 0,
            "limit": EVAL_LIMIT,
        }

        baseline_script = write_rendered_script(run_id, "baseline_script.py.j2", baseline_ctx)
        lora_script = write_rendered_script(run_id, "lora_script.py.j2", lora_ctx)
        eval_script = write_rendered_script(run_id, "eval_script.py.j2", eval_ctx)

    finally:
        # 恢复 env
        if old_run_dir is None:
            os.environ.pop("RECALLKIT_RUN_DIR", None)
        else:
            os.environ["RECALLKIT_RUN_DIR"] = old_run_dir
        if old_ckpt_dir is None:
            os.environ.pop("RECALLKIT_CKPT_DIR", None)
        else:
            os.environ["RECALLKIT_CKPT_DIR"] = old_ckpt_dir
        if old_hf_home is None:
            os.environ.pop("HF_HOME", None)
        else:
            os.environ["HF_HOME"] = old_hf_home

    assert baseline_script.exists(), "baseline_script.py 未生成"
    assert lora_script.exists(), "lora_script.py 未生成"
    assert eval_script.exists(), "eval_script.py 未生成"

    metrics_path = run_dir / "metrics.jsonl"

    # ------------------------------------------------------------------
    # 步骤 2：运行 baseline 评测
    # ------------------------------------------------------------------
    print(f"\n[smoke] 运行 baseline 评测：{baseline_script}")
    result = _run_script(baseline_script, env_vars)
    assert result.returncode == 0, (
        f"baseline_script.py 非零退出（{result.returncode}），"
        f"请检查 {metrics_path} 的错误行"
    )

    # 验证 baseline metrics
    assert metrics_path.exists(), "metrics.jsonl 未生成"
    records = _load_metrics(metrics_path)
    baseline_records = [
        r for r in records
        if r.get("phase") == "baseline" or r.get("event") == "eval_scores"
    ]
    assert len(baseline_records) >= 1, (
        f"metrics.jsonl 缺少 baseline 记录，当前记录：{records}"
    )

    # ------------------------------------------------------------------
    # 步骤 3：运行 LoRA 训练
    # ------------------------------------------------------------------
    print(f"\n[smoke] 运行 LoRA 训练：{lora_script}")
    result = _run_script(lora_script, env_vars)
    assert result.returncode == 0, (
        f"lora_script.py 非零退出（{result.returncode}），"
        f"请检查 {metrics_path} 的错误行"
    )

    # 验证 train_epoch metrics
    records = _load_metrics(metrics_path)
    train_epoch_records = [
        r for r in records if r.get("event") == "train_epoch"
    ]
    assert len(train_epoch_records) >= 1, (
        f"metrics.jsonl 缺少 train_epoch 记录（期望 >= {EPOCHS} 条），"
        f"当前记录：{records}"
    )

    # ------------------------------------------------------------------
    # 步骤 4：运行 eval 评测
    # ------------------------------------------------------------------
    print(f"\n[smoke] 运行 eval 评测：{eval_script}")
    result = _run_script(eval_script, env_vars)
    assert result.returncode == 0, (
        f"eval_script.py 非零退出（{result.returncode}），"
        f"请检查 {metrics_path} 的错误行"
    )

    # ------------------------------------------------------------------
    # 步骤 5：最终断言（三类事件 + scores.json）
    # ------------------------------------------------------------------
    records = _load_metrics(metrics_path)

    # 5a. baseline eval_scores
    baseline_eval = [
        r for r in records
        if r.get("event") == "eval_scores" and r.get("phase") == "baseline"
    ]
    assert len(baseline_eval) >= 1, (
        f"metrics.jsonl 缺少 phase=baseline 的 eval_scores 事件。"
        f"所有记录：{[r.get('event') for r in records]}"
    )

    # 5b. train_epoch（>= 1 条）
    train_epoch_records = [r for r in records if r.get("event") == "train_epoch"]
    assert len(train_epoch_records) >= 1, (
        f"metrics.jsonl 缺少 train_epoch 事件（期望 >= 1）。"
        f"所有记录事件：{[r.get('event') for r in records]}"
    )

    # 5c. eval_scores（来自 eval_script，phase=evaluating）
    eval_scores_records = [
        r for r in records if r.get("event") == "eval_scores"
    ]
    assert len(eval_scores_records) >= 1, (
        f"metrics.jsonl 缺少 eval_scores 事件（来自 eval_script）。"
        f"所有记录事件：{[r.get('event') for r in records]}"
    )

    # 5d. scores.json 存在
    scores_json = run_dir / "artifacts" / "scores.json"
    assert scores_json.exists(), (
        f"artifacts/scores.json 未生成。"
        f"artifacts/ 内容：{list((run_dir / 'artifacts').iterdir())}"
    )

    print(f"\n[smoke] 冒烟测试通过！")
    print(f"  - baseline eval_scores: {len(baseline_eval)} 条")
    print(f"  - train_epoch: {len(train_epoch_records)} 条")
    print(f"  - eval_scores（eval 阶段）: {len(eval_scores_records)} 条")
    print(f"  - scores.json: {scores_json}")
