"""
pars.report.charts — 实验报告图表生成器。

结论：使用 matplotlib Agg backend(无 GUI 依赖)生成训练曲线和分数对比图。
      所有函数均保存 PNG 文件，不展示 GUI 窗口。

设计约束：
1. matplotlib.use("Agg") 必须在导入 pyplot 前调用，避免 DISPLAY 依赖
2. 图表标题使用英文，防止 matplotlib 中文字体缺失乱码；内容数据无限制
3. 函数幂等：同一 out_path 可重复调用，覆写已有文件
4. 参数 None 值安全处理：eval_loss 可能为 None (baseline eval 阶段)

导出 API (T021 schema):
  - plot_eval_scores(baseline_scores, lora_scores, out_path) → None
  - plot_training_loss(loss_records, out_path) → None
"""

from __future__ import annotations

import matplotlib

# 结论：必须在 import pyplot 之前设置 Agg backend，否则在无 DISPLAY 环境下崩溃
matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
from pathlib import Path
from typing import Any


def plot_eval_scores(
    baseline_scores: dict[str, float],
    lora_scores: dict[str, float],
    out_path: Path,
) -> None:
    """生成 baseline vs LoRA 分数对比横向柱状图，保存为 PNG。

    结论：横坐标为 metric 名称，竖坐标为分数值。
          使用分组柱状图区分 baseline 和 lora。
          标题英文避免中文字体依赖。

    参数：
        baseline_scores : dict - metric 名称 → baseline 分数，如 {"accuracy": 0.45}
        lora_scores     : dict - metric 名称 → LoRA 最终分数，如 {"accuracy": 0.51}
        out_path        : Path - 输出 PNG 文件路径（父目录须已存在）

    Raises：
        ValueError : baseline_scores 或 lora_scores 为空
        OSError    : out_path 父目录不存在
    """
    if not baseline_scores:
        msg = "baseline_scores 不能为空"
        raise ValueError(msg)
    if not lora_scores:
        msg = "lora_scores 不能为空"
        raise ValueError(msg)

    # 取两个 dict 的公共 metric 键（保持顺序）
    metrics = [k for k in baseline_scores if k in lora_scores]
    if not metrics:
        # fallback：各自取 union，缺失的用 0
        all_metrics = list(dict.fromkeys(list(baseline_scores.keys()) + list(lora_scores.keys())))
        metrics = all_metrics

    baseline_vals = [baseline_scores.get(m, 0.0) for m in metrics]
    lora_vals = [lora_scores.get(m, 0.0) for m in metrics]

    n = len(metrics)
    x = list(range(n))
    width = 0.35

    fig, ax = plt.subplots(figsize=(max(6, n * 1.5), 5))

    bars_baseline = ax.bar(
        [xi - width / 2 for xi in x],
        baseline_vals,
        width,
        label="Baseline",
        color="#4C72B0",
        alpha=0.85,
    )
    bars_lora = ax.bar(
        [xi + width / 2 for xi in x],
        lora_vals,
        width,
        label="LoRA final",
        color="#DD8452",
        alpha=0.85,
    )

    ax.set_xlabel("Metric", fontsize=12)
    ax.set_ylabel("Score", fontsize=12)
    ax.set_title("Baseline vs LoRA Evaluation Scores", fontsize=14)
    ax.set_xticks(x)
    ax.set_xticklabels(metrics, rotation=15, ha="right")
    ax.legend(loc="best")
    ax.set_ylim(0, max(max(baseline_vals + lora_vals, default=1.0) * 1.2, 1.0))
    ax.grid(axis="y", alpha=0.3)

    # 添加数值标签
    for bar in bars_baseline:
        h = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2.0,
            h + 0.005,
            f"{h:.3f}",
            ha="center",
            va="bottom",
            fontsize=9,
        )
    for bar in bars_lora:
        h = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2.0,
            h + 0.005,
            f"{h:.3f}",
            ha="center",
            va="bottom",
            fontsize=9,
        )

    fig.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=120, bbox_inches="tight", format="png")
    plt.close(fig)


def plot_training_loss(
    loss_records: list[dict[str, Any]],
    out_path: Path,
) -> None:
    """生成训练损失曲线图（train_loss + eval_loss vs epoch），保存为 PNG。

    结论：双线图，蓝线为 train_loss，橙线为 eval_loss（若存在）。
          横坐标为 epoch 编号（整数），纵坐标为 loss 值。
          标题英文避免中文字体依赖。

    参数：
        loss_records : list[dict] - 训练记录列表，每条含:
                         - epoch     : int - epoch 编号
                         - train_loss: float - 训练损失
                         - eval_loss : float | None - 验证损失（可选）
        out_path     : Path - 输出 PNG 文件路径（父目录须已存在）

    Raises：
        ValueError : loss_records 为空
        OSError    : out_path 父目录不存在
    """
    if not loss_records:
        msg = "loss_records 不能为空"
        raise ValueError(msg)

    epochs = [r.get("epoch", i + 1) for i, r in enumerate(loss_records)]
    train_losses = [float(r.get("train_loss", 0.0)) for r in loss_records]

    # eval_loss 可能为 None（baseline 阶段无 eval loss）
    eval_losses_raw = [r.get("eval_loss") for r in loss_records]
    has_eval_loss = any(v is not None for v in eval_losses_raw)
    eval_losses = [float(v) if v is not None else None for v in eval_losses_raw]

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.plot(
        epochs,
        train_losses,
        marker="o",
        linewidth=2,
        markersize=5,
        color="#4C72B0",
        label="Train Loss",
    )

    if has_eval_loss:
        # 过滤掉 None 值的点（只绘制有 eval_loss 的 epoch）
        eval_x = [e for e, v in zip(epochs, eval_losses, strict=False) if v is not None]
        eval_y = [v for v in eval_losses if v is not None]
        if eval_x:
            ax.plot(
                eval_x,
                eval_y,
                marker="s",
                linewidth=2,
                markersize=5,
                color="#DD8452",
                label="Eval Loss",
                linestyle="--",
            )

    ax.set_xlabel("Epoch", fontsize=12)
    ax.set_ylabel("Loss", fontsize=12)
    ax.set_title("Training Loss Curve", fontsize=14)
    ax.set_xticks(epochs)
    ax.legend(loc="best")
    ax.grid(alpha=0.3)

    fig.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=120, bbox_inches="tight", format="png")
    plt.close(fig)
