"""
pars.report.renderer — 实验报告渲染器。

结论：ReadKit T021 的主入口。读取 run_dir 下的所有 artifact，
      调用 charts.py 生成 PNG，用 Jinja2 渲染 report.md.j2，
      输出最终 report.md。

设计约束：
1. render_report(run_dir) 接受 Path 对象，返回 report.md 的 Path
2. 模板搜索路径：优先 run_dir 同级别 templates/，再 pars.report 包目录同级 templates/
3. PNG 文件写到 run_dir/artifacts/ 下，相对路径写入模板变量
4. 失败归因：run_dir/failure_attribution.md 存在则嵌入，不存在则写"无失败"模板文本
5. 幂等：同一 run_dir 可重复调用，覆写已有 report.md

导出 API (T021 schema):
  - render_report(run_dir: Path) -> Path
"""

from __future__ import annotations

import json
import re
from datetime import timedelta
from pathlib import Path
from typing import Any

import yaml


# ---------------------------------------------------------------------------
# 内部工具
# ---------------------------------------------------------------------------


def _load_config(run_dir: Path) -> dict[str, Any]:
    """读取 run_dir/config.yaml，返回 dict。

    结论：config.yaml 是 run 的元数据来源，包含 lora 配置、数据集、时间戳等。
          文件不存在则返回空 dict（后续渲染步骤会用默认值兜底）。
    """
    config_path = run_dir / "config.yaml"
    if not config_path.exists():
        return {}
    with open(config_path, encoding="utf-8") as f:  # noqa: PTH123
        return yaml.safe_load(f) or {}


def _load_scores(run_dir: Path) -> dict[str, Any]:
    """读取 run_dir/artifacts/scores.json，返回 dict。

    结论：scores.json 含 baseline + lora_epoch_N + lora_final 等 key。
          文件不存在则返回空 dict。
    """
    scores_path = run_dir / "artifacts" / "scores.json"
    if not scores_path.exists():
        return {}
    try:
        return json.loads(scores_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}


def _load_metrics_jsonl(run_dir: Path) -> list[dict[str, Any]]:
    """流式读 run_dir/metrics.jsonl，返回所有合法 JSON 对象列表。

    结论：不依赖 MetricRecord dataclass，直接解析为 dict，
          解析失败的行跳过（不 raise）。
    """
    metrics_path = run_dir / "metrics.jsonl"
    if not metrics_path.exists():
        return []

    records: list[dict[str, Any]] = []
    with open(metrics_path, encoding="utf-8") as f:  # noqa: PTH123
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError:
                pass  # 跳过损坏行
    return records


def _extract_training_epochs(metrics: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """从 metrics 列表中提取 training/epoch 类型记录。

    结论：每条 epoch 记录对应模板 eval_table_rows 的一行：
          {epoch, train_loss, eval_loss(可选)}。

    返回按 epoch 排序的列表。
    """
    epoch_records: list[dict[str, Any]] = []
    for rec in metrics:
        if rec.get("phase") == "training" and rec.get("kind") == "epoch":
            data = rec.get("data", {})
            epoch_records.append({
                "epoch": data.get("epoch", len(epoch_records) + 1),
                "train_loss": float(data.get("train_loss", 0.0)),
                "eval_loss": (
                    float(data["eval_loss"]) if data.get("eval_loss") is not None else None
                ),
            })

    # 按 epoch 排序（防止乱序写入）
    epoch_records.sort(key=lambda r: r["epoch"])
    return epoch_records


def _extract_baseline_score(
    scores: dict[str, Any],
    metrics: list[dict[str, Any]],
) -> float | None:
    """提取 baseline 评测分数（取第一个数值 metric 作为代表分数）。

    结论：优先从 artifacts/scores.json["baseline"] 提取，
          fallback 到 metrics.jsonl 中 phase=baseline/kind=eval 的 data 字段。

    返回单一 float（代表分数）或 None。
    """
    # 优先 scores.json
    baseline_data = scores.get("baseline")
    if isinstance(baseline_data, dict) and baseline_data:
        # 取第一个 float 值
        first_val = next((v for v in baseline_data.values() if isinstance(v, (int, float))), None)
        if first_val is not None:
            return float(first_val)
    elif isinstance(baseline_data, (int, float)):
        return float(baseline_data)

    # fallback：metrics.jsonl baseline eval 记录
    for rec in metrics:
        if rec.get("phase") == "baseline" and rec.get("kind") == "eval":
            data = rec.get("data", {})
            for v in data.values():
                if isinstance(v, (int, float)):
                    return float(v)

    return None


def _build_lora_scores_table(
    scores: dict[str, Any],
    baseline_score: float | None,
) -> list[dict[str, Any]]:
    """构建 lora_scores 列表，用于模板 ## 分数对比 表格。

    结论：遍历 scores.json 中非 baseline 的 key，每个作为一行。
          label 为 key 名称；score 取第一个数值；delta vs baseline 计算。

    返回格式：[{label, score, delta}]，delta=None 若无 baseline 参照。
    """
    rows: list[dict[str, Any]] = []
    for key, val in scores.items():
        if key == "baseline":
            continue
        score: float | None = None
        if isinstance(val, dict):
            score = next(
                (float(v) for v in val.values() if isinstance(v, (int, float))),
                None,
            )
        elif isinstance(val, (int, float)):
            score = float(val)

        if score is None:
            continue

        delta: float | None = None
        if baseline_score is not None:
            delta = score - baseline_score

        rows.append({"label": key, "score": score, "delta": delta})

    return rows


def _build_baseline_scores_dict(scores: dict[str, Any]) -> dict[str, float]:
    """提取 baseline metric 字典，用于 plot_eval_scores。

    结论：从 scores["baseline"] 提取所有数值 metric，返回 {metric_name: float}。
    """
    baseline_data = scores.get("baseline", {})
    if not isinstance(baseline_data, dict):
        return {"score": float(baseline_data)} if isinstance(baseline_data, (int, float)) else {}
    return {k: float(v) for k, v in baseline_data.items() if isinstance(v, (int, float))}


def _build_lora_final_scores_dict(scores: dict[str, Any]) -> dict[str, float]:
    """提取 lora_final metric 字典，用于 plot_eval_scores。

    结论：优先取 "lora_final"，否则取最后一个非 baseline key。
    """
    if "lora_final" in scores:
        val = scores["lora_final"]
        if isinstance(val, dict):
            return {k: float(v) for k, v in val.items() if isinstance(v, (int, float))}

    # fallback：取最后一个非 baseline entry
    for key in reversed(list(scores.keys())):
        if key == "baseline":
            continue
        val = scores[key]
        if isinstance(val, dict):
            return {k: float(v) for k, v in val.items() if isinstance(v, (int, float))}

    return {}


def _format_wall_clock(config: dict[str, Any]) -> str:
    """格式化 wall_clock 字符串。

    结论：优先使用 config["wall_clock"]；
          若不存在，则从 started_at/ended_at 计算差值；
          fallback 返回 "00:00:00"。
    """
    if "wall_clock" in config:
        return str(config["wall_clock"])

    started_at = config.get("started_at")
    ended_at = config.get("ended_at")
    if started_at and ended_at:
        try:
            from datetime import datetime, timezone  # noqa: PLC0415
            start = datetime.fromisoformat(str(started_at))
            end = datetime.fromisoformat(str(ended_at))
            diff: timedelta = end - start
            total_secs = int(diff.total_seconds())
            hours, remainder = divmod(total_secs, 3600)
            minutes, seconds = divmod(remainder, 60)
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        except (ValueError, TypeError):
            pass

    return "00:00:00"


def _find_template_dir(run_dir: Path) -> Path:
    """定位 templates/ 目录，按优先级搜索。

    搜索顺序：
    1. 项目根 (run_dir 向上找直到 pyproject.toml) / templates/
    2. pars/report 包目录向上两层的 templates/
    3. 当前工作目录的 templates/

    结论：优先项目级模板，保证测试与生产使用同一套模板。
    """
    # 从 pars/report/renderer.py 推导项目根（向上找 pyproject.toml）
    renderer_path = Path(__file__).resolve()
    candidate = renderer_path.parent
    for _ in range(8):  # 最多向上 8 层
        if (candidate / "pyproject.toml").exists():
            templates_dir = candidate / "templates"
            if templates_dir.is_dir():
                return templates_dir
        candidate = candidate.parent

    # fallback：pars/report 同级 templates
    fallback = renderer_path.parent.parent.parent / "templates"
    if fallback.is_dir():
        return fallback

    # 最后 fallback：cwd/templates
    return (Path.cwd() / "templates").resolve()


def _infer_decision_text(
    scores: dict[str, Any],
    baseline_score: float | None,
) -> str:
    """根据评测结果自动推断决策文字。

    结论：决策文字必须含 [继续|停止|改方向] 之一（schema gate 要求）。
          简单规则：有 baseline 且 lora 有改善 → 继续；无改善 → 改方向；无法评估 → 停止。
    """
    lora_final = _build_lora_final_scores_dict(scores)

    if not lora_final or baseline_score is None:
        return "停止：缺少足够数据支撑决策，建议检查训练流程后重新评估。"

    lora_score_val = next(iter(lora_final.values()), None)
    if lora_score_val is None:
        return "停止：LoRA 分数数据异常，无法做出可靠决策。"

    delta = lora_score_val - baseline_score
    if delta > 0.01:
        return (
            f"继续：LoRA 微调后分数从 {baseline_score:.4f} 提升至 {lora_score_val:.4f}"
            f"（delta={delta:+.4f}），建议继续增加训练轮次或调整超参。"
        )
    elif delta < -0.01:
        return (
            f"改方向：LoRA 微调后分数从 {baseline_score:.4f} 下降至 {lora_score_val:.4f}"
            f"（delta={delta:+.4f}），建议调整学习率、rank 或数据集。"
        )
    else:
        return (
            f"继续：LoRA 微调后分数 {lora_score_val:.4f} 与 baseline {baseline_score:.4f}"
            f" 相当（delta={delta:+.4f}），可尝试更多 epoch 或更大 rank。"
        )


# ---------------------------------------------------------------------------
# 主入口
# ---------------------------------------------------------------------------


def render_report(run_dir: Path) -> Path:
    """渲染实验报告，输出 run_dir/report.md。

    结论：综合读取 config.yaml / metrics.jsonl / artifacts/scores.json /
          failure_attribution.md，生成 PNG 图表，使用 Jinja2 模板渲染最终报告。
          返回 report.md 文件路径。

    步骤：
    1. 读取 config.yaml / scores.json / metrics.jsonl
    2. 提取 baseline 分数 + epoch 记录 + LoRA 分数
    3. 生成训练曲线 PNG (training_curve.png) + 分数对比 PNG (eval_scores.png)
    4. 读取 failure_attribution.md（若存在）
    5. 渲染 report.md.j2 → run_dir/report.md

    参数：
        run_dir : Path - run 数据目录（含 config.yaml / metrics.jsonl / artifacts/）

    返回：
        Path — run_dir/report.md 的绝对路径

    Raises:
        FileNotFoundError : templates/report.md.j2 模板文件不存在
        jinja2.TemplateError : Jinja2 渲染错误
    """
    from pars.report.charts import plot_eval_scores, plot_training_loss  # noqa: PLC0415
    import jinja2  # noqa: PLC0415

    run_dir = run_dir.resolve()
    artifacts_dir = run_dir / "artifacts"
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    # --- 1. 读取数据源 ---
    config = _load_config(run_dir)
    scores = _load_scores(run_dir)
    metrics = _load_metrics_jsonl(run_dir)

    # --- 2. 提取关键数据 ---
    run_id = config.get("run_id", run_dir.name)
    baseline_score = _extract_baseline_score(scores, metrics)
    epoch_records = _extract_training_epochs(metrics)
    lora_scores_table = _build_lora_scores_table(scores, baseline_score)

    # --- 3. 生成 PNG 图表 ---
    loss_curve_png_path = artifacts_dir / "training_curve.png"
    eval_scores_png_path = artifacts_dir / "eval_scores.png"

    # 训练曲线 PNG
    if epoch_records:
        plot_training_loss(epoch_records, loss_curve_png_path)
    else:
        # 无训练数据时，生成占位图（空记录会 raise ValueError，用 placeholder）
        plot_training_loss(
            [{"epoch": 1, "train_loss": 0.0, "eval_loss": None}],
            loss_curve_png_path,
        )

    # 分数对比 PNG
    baseline_scores_dict = _build_baseline_scores_dict(scores)
    lora_final_dict = _build_lora_final_scores_dict(scores)

    if baseline_scores_dict and lora_final_dict:
        plot_eval_scores(baseline_scores_dict, lora_final_dict, eval_scores_png_path)
    elif baseline_score is not None:
        # fallback：单 metric 情况
        plot_eval_scores(
            {"score": baseline_score},
            {"score": baseline_score},  # 无 LoRA 数据时 baseline 重复
            eval_scores_png_path,
        )
    else:
        plot_eval_scores({"score": 0.0}, {"score": 0.0}, eval_scores_png_path)

    # --- 4. 失败归因 ---
    fa_path = run_dir / "failure_attribution.md"
    failure_exists = fa_path.exists()
    failure_attribution_md = ""
    if failure_exists:
        failure_attribution_md = fa_path.read_text(encoding="utf-8")

    # --- 5. 构建模板变量 ---
    lora_cfg = config.get("lora", {})
    if not isinstance(lora_cfg, dict):
        lora_cfg = {}

    # lora_config 提供 rank/alpha/lr/epochs（含默认值）
    lora_config = {
        "rank": lora_cfg.get("rank", 8),
        "alpha": lora_cfg.get("alpha", 16),
        "lr": lora_cfg.get("lr", 2e-4),
        "epochs": lora_cfg.get("epochs", 3),
    }

    # config_yaml 块（隐藏大字段）
    config_yaml_block = yaml.dump(config, allow_unicode=True, default_flow_style=False)

    # PNG 相对路径（相对于 report.md 所在目录，即 run_dir）
    loss_curve_rel = "artifacts/training_curve.png"
    eval_scores_rel = "artifacts/eval_scores.png"

    # 决策文字
    decision_text = config.get("decision_text") or _infer_decision_text(scores, baseline_score)

    template_vars = {
        "run_id": run_id,
        "question": config.get("question", "（未指定研究问题）"),
        "base_model": config.get("base_model", "（未知模型）"),
        "lora_config": lora_config,
        "dataset": config.get("dataset", "（未知数据集）"),
        "wall_clock": _format_wall_clock(config),
        "usd_spent": float(config.get("usd_spent", 0.0)),
        "gpu_hours": float(config.get("gpu_hours", 0.0)),
        "started_at": config.get("started_at", "N/A"),
        "ended_at": config.get("ended_at", "N/A"),
        "gpu_model": config.get("gpu_model", "Unknown GPU"),
        "cuda_version": config.get("cuda_version", "N/A"),
        "python_version": config.get("python_version", "N/A"),
        "baseline_score": baseline_score,
        "lora_scores": lora_scores_table,
        "eval_table_rows": epoch_records,
        "failure_exists": failure_exists,
        "failure_attribution_md": failure_attribution_md,
        "config_yaml_block": config_yaml_block,
        "eval_scores_png": eval_scores_rel,
        "loss_curve_png": loss_curve_rel,
        "decision_text": decision_text,
    }

    # --- 6. Jinja2 渲染 ---
    template_dir = _find_template_dir(run_dir)
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(str(template_dir)),
        undefined=jinja2.StrictUndefined,
        autoescape=False,  # Markdown 不需要 HTML 转义
        trim_blocks=True,
        lstrip_blocks=False,
    )
    template = env.get_template("report.md.j2")
    rendered_md = template.render(**template_vars)

    # --- 7. 写入 report.md ---
    report_path = run_dir / "report.md"
    report_path.write_text(rendered_md, encoding="utf-8")

    return report_path
