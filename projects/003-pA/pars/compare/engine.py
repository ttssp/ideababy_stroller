"""
pars.compare.engine — 跨 run 比较引擎 (T025 · O6 实现)

结论：实现两个层次的 compare 接口：
  1. 底层三函数 + format_markdown（T025.md spec 接口，输出三栏 markdown）
     - compare_configs(a, b)  → list[DiffRow]
     - compare_metrics(a_id, b_id, runs_root) → list[DiffRow]
     - compare_conclusions(report_a, report_b) → list[DiffRow]
     - format_markdown(config_diffs, metric_diffs, conclusion_diffs) → str

  2. 高层 compare() 函数（Prompt O6 决策 contract）
     返回 ComparisonResult，强制给出 "pick runX" verdict，
     eval_score 最高者胜，同分用 wall_clock（短）→ usd（少）作 tiebreaker。

设计原则：
  - 与 pars.paths.run_dir 解耦：接受 runs_root 参数（方便测试用 tmp_path）
  - deepdiff 7.0.1 输出结构：ValuesChanged/DictionaryItemAdded/Removed 等 key
  - metrics.jsonl 扁平化读取，phase=evaluating kind=eval 取最后一条（每 task_name）
  - report.md 缺 ## 决策 section → 返回 "(no decision section)"，log warning
"""

from __future__ import annotations

import json
import logging
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# 数据结构
# ---------------------------------------------------------------------------


@dataclass
class DiffRow:
    """单个差异行：字段名 + A 侧值 + B 侧值。

    用于 compare_configs / compare_metrics / compare_conclusions 的返回值。
    """

    field: str
    value_a: Any
    value_b: Any


@dataclass
class MetricRow:
    """compare() 返回的 ComparisonResult.metrics 中的单行。

    metric:   指标名（如 "eval_score(gsm8k)", "wall_clock_s", "usd_spent"）
    val_a:    run_a 侧的值
    val_b:    run_b 侧的值
    delta:    val_b - val_a（数值；非数值时为 0.0）
    winner:   "runA" | "runB" | "tie"
    """

    metric: str
    val_a: Any
    val_b: Any
    delta: float
    winner: str


@dataclass
class ComparisonResult:
    """高层 compare() 的完整输出（O6 决策 contract）。

    metrics:       指标行列表（eval_score / wall_clock / usd / config diff 等）
    verdict:       "pick runA" 或 "pick runB"（强制明确，无 "mixed"）
    verdict_reason 人类可读的决策理由（含 eval_score 差值 + 时间/成本说明）
    runa_id:       run_a 的 run_id
    runb_id:       run_b 的 run_id
    markdown:      完整的 markdown 差异表（三栏 format_markdown 输出）
    """

    metrics: list[MetricRow]
    verdict: str
    verdict_reason: str
    runa_id: str
    runb_id: str
    markdown: str = field(default="")


# ---------------------------------------------------------------------------
# 内部辅助：路径解析
# ---------------------------------------------------------------------------


def _resolve_run_dir(run_id: str, runs_root: Path | None) -> Path:
    """返回 run 的目录路径。

    如果提供了 runs_root（测试用临时目录），直接拼接；
    否则通过 pars.paths.run_dir 解析（生产环境路径）。
    """
    if runs_root is not None:
        return runs_root / run_id
    from pars.paths import run_dir as _run_dir  # noqa: PLC0415
    return _run_dir(run_id)


# ---------------------------------------------------------------------------
# 内部辅助：扁平化 nested dict（用于 compare_configs）
# ---------------------------------------------------------------------------


def _flatten_dict(d: dict, prefix: str = "") -> dict[str, Any]:
    """将嵌套 dict 扁平化为 {dotted.key: value} 格式。

    例: {"training": {"lora_rank": 8}} → {"training.lora_rank": 8}
    """
    result: dict[str, Any] = {}
    for key, value in d.items():
        full_key = f"{prefix}.{key}" if prefix else key
        if isinstance(value, dict):
            result.update(_flatten_dict(value, prefix=full_key))
        else:
            result[full_key] = value
    return result


# ---------------------------------------------------------------------------
# 内部辅助：跳过不需要对比的字段
# ---------------------------------------------------------------------------

# 仅对比超参数相关字段，过滤时间戳/运行时填入字段/run_id
_SKIP_FIELDS = frozenset({
    "run_id",
    "created_at",
    "started_at",
    "completed_at",
    "wall_clock_seconds",
    "usd_total",
    "gpu_hours",
    "notes",
    "parent_run_id",
    "env_snapshot",
})


# ---------------------------------------------------------------------------
# 公开 API：底层三函数 + format_markdown
# ---------------------------------------------------------------------------


def compare_configs(
    cfg_a: dict[str, Any],
    cfg_b: dict[str, Any],
) -> list[DiffRow]:
    """对比两个 RunConfig dict，返回差异行列表。

    结论：扁平化嵌套 dict 后逐 key 对比，跳过时间戳/运行时字段。
         使用 deepdiff 前先扁平化，简化 deepdiff 输出处理。

    参数：
        cfg_a: run A 的 config dict（从 config.yaml load 后 model_dump()）
        cfg_b: run B 的 config dict

    返回：
        list[DiffRow]，每行 (field, value_a, value_b)；完全相同时为空列表
    """
    flat_a = _flatten_dict(cfg_a)
    flat_b = _flatten_dict(cfg_b)

    diffs: list[DiffRow] = []
    all_keys = set(flat_a) | set(flat_b)

    for key in sorted(all_keys):
        # 过滤不感兴趣的字段（run_id、时间戳等运行时字段）
        root_key = key.split(".")[0]
        if root_key in _SKIP_FIELDS or key in _SKIP_FIELDS:
            continue

        val_a = flat_a.get(key, "(missing)")
        val_b = flat_b.get(key, "(missing)")

        if val_a != val_b:
            diffs.append(DiffRow(field=key, value_a=val_a, value_b=val_b))

    return diffs


def compare_metrics(
    run_a_id: str,
    run_b_id: str,
    *,
    runs_root: Path | None = None,
) -> list[DiffRow]:
    """对比两个 run 的 eval 指标（最后一次 phase=evaluating, kind=eval 记录）。

    结论：读取 metrics.jsonl，按 task_name 分组取最后一条 eval 记录。
          对齐 task_name × metric key：
          - 两侧都有 → 比较值，如不同则入 DiffRow
          - 只有 A 有 → value_b = "(only in B)"（缺失那侧）
          - 只有 B 有 → value_a = "(only in A)"

    注意：这里的 "only in A" 语义是"该 task 只在 A 中存在"，
          value_b 显示 "(only in A)" 意味着 B 侧没有此 task。
    """
    eval_a = _load_last_eval_per_task(run_a_id, runs_root=runs_root)
    eval_b = _load_last_eval_per_task(run_b_id, runs_root=runs_root)

    diffs: list[DiffRow] = []
    all_tasks = set(eval_a) | set(eval_b)

    for task in sorted(all_tasks):
        data_a = eval_a.get(task)
        data_b = eval_b.get(task)

        if data_a is None:
            # 只有 B 有
            for metric_key, val_b in sorted(data_b.items()):  # type: ignore[union-attr]
                diffs.append(DiffRow(
                    field=f"{task}.{metric_key}",
                    value_a="(only in B)",  # A 侧缺失
                    value_b=val_b,
                ))
        elif data_b is None:
            # 只有 A 有
            for metric_key, val_a in sorted(data_a.items()):
                diffs.append(DiffRow(
                    field=f"{task}.{metric_key}",
                    value_a=val_a,
                    value_b="(only in A)",  # B 侧缺失
                ))
        else:
            # 两侧都有，逐 metric key 对比
            all_metric_keys = set(data_a) | set(data_b)
            for metric_key in sorted(all_metric_keys):
                val_a = data_a.get(metric_key, "(missing)")
                val_b = data_b.get(metric_key, "(missing)")
                if val_a != val_b:
                    diffs.append(DiffRow(
                        field=f"{task}.{metric_key}",
                        value_a=val_a,
                        value_b=val_b,
                    ))

    return diffs


def compare_conclusions(
    report_a_path: Path,
    report_b_path: Path,
) -> list[DiffRow]:
    """对比两份 report.md 的 ## 决策 section 内容。

    结论：用正则提取 ## 决策 section（到下一个 ## 或文档末尾）。
          返回一行 DiffRow，field="decision"，value_a/value_b 为各自 section 内容。
          若 section 缺失，返回 "(no decision section)"，并 log warning。

    参数：
        report_a_path: run A 的 report.md 路径
        report_b_path: run B 的 report.md 路径

    返回：
        list[DiffRow]（通常只有一行 decision），两侧内容相同时也返回（供展示用）
    """
    content_a = _extract_decision_section(report_a_path, "run_a")
    content_b = _extract_decision_section(report_b_path, "run_b")
    return [DiffRow(field="decision", value_a=content_a, value_b=content_b)]


def format_markdown(
    config_diffs: list[DiffRow],
    metric_diffs: list[DiffRow],
    conclusion_diffs: list[DiffRow],
) -> str:
    """将三组 DiffRow 格式化为三栏 markdown 差异表。

    结论：生成三个 H2 section（## Config diff / ## Metric diff / ## Conclusion diff），
          每 section 内一个 markdown table。section 无 diff 时显示 "(no differences)"。

    返回：
        完整 markdown 字符串
    """
    lines: list[str] = []

    # --- Config diff ---
    lines.append("## Config diff")
    lines.append("")
    if config_diffs:
        lines.append("| field | runA | runB |")
        lines.append("|-------|------|------|")
        for row in config_diffs:
            lines.append(f"| {row.field} | {row.value_a} | {row.value_b} |")
    else:
        lines.append("*(no differences)*")
    lines.append("")

    # --- Metric diff ---
    lines.append("## Metric diff")
    lines.append("")
    if metric_diffs:
        lines.append("| metric | runA | runB |")
        lines.append("|--------|------|------|")
        for row in metric_diffs:
            lines.append(f"| {row.field} | {row.value_a} | {row.value_b} |")
    else:
        lines.append("*(no differences)*")
    lines.append("")

    # --- Conclusion diff ---
    lines.append("## Conclusion diff")
    lines.append("")
    if conclusion_diffs:
        lines.append("| field | runA | runB |")
        lines.append("|-------|------|------|")
        for row in conclusion_diffs:
            # 决策内容可能有多行，替换换行为 <br>
            val_a = str(row.value_a).replace("\n", " ").strip()
            val_b = str(row.value_b).replace("\n", " ").strip()
            lines.append(f"| {row.field} | {val_a} | {val_b} |")
    else:
        lines.append("*(no differences)*")
    lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# 公开 API：高层 compare()（O6 决策 contract）
# ---------------------------------------------------------------------------


def compare(
    run_a_id: str,
    run_b_id: str,
    *,
    eval_metric: str = "gsm8k",
    runs_root: Path | None = None,
) -> ComparisonResult:
    """对比两个 run，返回 ComparisonResult，并给出明确的 "pick runX" 决策。

    决策逻辑（O6 强制明确，不返回 "mixed"）：
      1. eval_score（指定 eval_metric 的 acc）最高者胜出
      2. eval_score 相同 → wall_clock_seconds 短者胜出（shorter is better）
      3. wall_clock 也相同 → usd_total 少者胜出（cheaper is better）
      4. 三者皆相同 → 默认选 runA（先入先出）

    参数：
        run_a_id:    run A 的 ID
        run_b_id:    run B 的 ID
        eval_metric: 用于决策的 eval task 名称（默认 "gsm8k"）
        runs_root:   覆盖默认路径（测试用）

    返回：
        ComparisonResult（含 verdict / verdict_reason / metrics / markdown）

    异常：
        ValueError: 两个 run 都没有 eval_score 数据（无法决策）
    """
    run_a_dir = _resolve_run_dir(run_a_id, runs_root)
    run_b_dir = _resolve_run_dir(run_b_id, runs_root)

    # --- 读取 config ---
    cfg_a_dict = _load_config_dict(run_a_dir)
    cfg_b_dict = _load_config_dict(run_b_dir)

    # --- 读取 eval metrics ---
    eval_a = _load_last_eval_per_task(run_a_id, runs_root=runs_root)
    eval_b = _load_last_eval_per_task(run_b_id, runs_root=runs_root)

    # 提取目标 eval_metric 的 acc 值
    score_a = _extract_eval_score(eval_a, eval_metric)
    score_b = _extract_eval_score(eval_b, eval_metric)

    # 如果两侧都没有 eval_score → 无法决策
    if score_a is None and score_b is None:
        raise ValueError(
            f"run_a '{run_a_id}' 和 run_b '{run_b_id}' 均缺少 eval_score "
            f"（task={eval_metric}）。请确认 eval 阶段已完成。"
        )

    # --- 读取 wall_clock / usd ---
    wc_a = cfg_a_dict.get("wall_clock_seconds") or 0.0
    wc_b = cfg_b_dict.get("wall_clock_seconds") or 0.0
    usd_a = cfg_a_dict.get("usd_total") or 0.0
    usd_b = cfg_b_dict.get("usd_total") or 0.0

    # --- 组装 MetricRow 列表 ---
    metric_rows: list[MetricRow] = []

    # eval_score 行
    eval_score_row = _make_eval_score_row(eval_metric, score_a, score_b)
    metric_rows.append(eval_score_row)

    # wall_clock 行
    wc_delta = wc_b - wc_a
    wc_winner = "runA" if wc_a <= wc_b else "runB"  # shorter is better
    metric_rows.append(MetricRow(
        metric="wall_clock_s",
        val_a=wc_a,
        val_b=wc_b,
        delta=wc_delta,
        winner=f"{wc_winner}(shorter is better)",
    ))

    # usd 行
    usd_delta = usd_b - usd_a
    usd_winner = "runA" if usd_a <= usd_b else "runB"  # cheaper is better
    metric_rows.append(MetricRow(
        metric="usd_spent",
        val_a=usd_a,
        val_b=usd_b,
        delta=usd_delta,
        winner=usd_winner,
    ))

    # config diff 行（将 DiffRow 转换为 MetricRow 供汇总）
    config_diffs = compare_configs(cfg_a_dict, cfg_b_dict)
    for diff in config_diffs:
        metric_rows.append(MetricRow(
            metric=diff.field,
            val_a=diff.value_a,
            val_b=diff.value_b,
            delta=0.0,
            winner="(config diff)",
        ))

    # --- 决策逻辑 ---
    verdict, verdict_reason = _make_verdict(
        run_a_id=run_a_id,
        run_b_id=run_b_id,
        score_a=score_a,
        score_b=score_b,
        wc_a=wc_a,
        wc_b=wc_b,
        usd_a=usd_a,
        usd_b=usd_b,
        eval_metric=eval_metric,
    )

    # --- 生成 markdown 差异表 ---
    metric_diffs = compare_metrics(run_a_id, run_b_id, runs_root=runs_root)
    report_a_path = run_a_dir / "report.md"
    report_b_path = run_b_dir / "report.md"
    conclusion_diffs = compare_conclusions(report_a_path, report_b_path)
    markdown = format_markdown(config_diffs, metric_diffs, conclusion_diffs)

    # 在 markdown 末尾追加 verdict
    markdown += f"\n## Verdict\n\n**{verdict}**\n\n{verdict_reason}\n"

    return ComparisonResult(
        metrics=metric_rows,
        verdict=verdict,
        verdict_reason=verdict_reason,
        runa_id=run_a_id,
        runb_id=run_b_id,
        markdown=markdown,
    )


# ---------------------------------------------------------------------------
# 内部辅助：决策逻辑
# ---------------------------------------------------------------------------


def _make_verdict(
    *,
    run_a_id: str,
    run_b_id: str,
    score_a: float | None,
    score_b: float | None,
    wc_a: float,
    wc_b: float,
    usd_a: float,
    usd_b: float,
    eval_metric: str,
) -> tuple[str, str]:
    """计算 verdict 字符串和 verdict_reason。

    返回: (verdict, verdict_reason)
    """
    # 处理一侧缺失的边缘情况
    if score_a is None:
        # 只有 B 有 eval score
        winner_id = run_b_id
        winner_label = "runB"
        reason = (
            f"{winner_label} 有 {eval_metric} eval_score（{score_b:.4f}），"
            f"runA 缺少 eval 数据。"
        )
        return f"pick {winner_label}", reason

    if score_b is None:
        winner_id = run_a_id
        winner_label = "runA"
        reason = (
            f"{winner_label} 有 {eval_metric} eval_score（{score_a:.4f}），"
            f"runB 缺少 eval 数据。"
        )
        return f"pick {winner_label}", reason

    # 两侧都有 eval score
    score_delta = score_b - score_a

    if abs(score_delta) > 1e-9:
        # eval_score 有明显差异，直接选高分者
        if score_b > score_a:
            winner_label = "runB"
            reason = (
                f"runB 的 {eval_metric} 显著高于 runA（"
                f"+{score_delta:+.4f}：{score_a:.4f} → {score_b:.4f}），"
                f"虽然多跑了 {(wc_b - wc_a) / 60:.0f}min / ${usd_b - usd_a:.2f}。"
            )
        else:
            winner_label = "runA"
            reason = (
                f"runA 的 {eval_metric} 显著高于 runB（"
                f"{score_delta:+.4f}：{score_a:.4f} → {score_b:.4f}），"
                f"且 wall_clock / usd {'也更优' if wc_a <= wc_b else '略高'}。"
            )
        return f"pick {winner_label}", reason

    # eval_score 相同，tiebreaker: wall_clock（短）
    wc_delta = wc_b - wc_a
    if abs(wc_delta) > 1.0:  # 超过 1 秒的差异才算不同
        winner_label = "runA" if wc_a < wc_b else "runB"
        reason = (
            f"eval_score 相同（{score_a:.4f}），"
            f"按 wall_clock tiebreaker：{winner_label} 用时更短（"
            f"runA={wc_a:.0f}s vs runB={wc_b:.0f}s）。"
        )
        return f"pick {winner_label}", reason

    # wall_clock 也相同，tiebreaker: usd（少）
    usd_delta = usd_b - usd_a
    if abs(usd_delta) > 0.001:
        winner_label = "runA" if usd_a < usd_b else "runB"
        reason = (
            f"eval_score 和 wall_clock 均相同，"
            f"按 usd tiebreaker：{winner_label} 成本更低（"
            f"runA=${usd_a:.2f} vs runB=${usd_b:.2f}）。"
        )
        return f"pick {winner_label}", reason

    # 三者皆同 → 默认 runA
    reason = "eval_score / wall_clock / usd 三者完全相同，默认选 runA（先入先出）。"
    return "pick runA", reason


def _make_eval_score_row(eval_metric: str, score_a: float | None, score_b: float | None) -> MetricRow:
    """构造 eval_score MetricRow。"""
    if score_a is None:
        score_a_display: Any = "(missing)"
    else:
        score_a_display = score_a

    if score_b is None:
        score_b_display: Any = "(missing)"
    else:
        score_b_display = score_b

    # delta：仅在两侧都有数值时计算
    if isinstance(score_a_display, float) and isinstance(score_b_display, float):
        delta = score_b_display - score_a_display
        # 决策：eval_score 高者胜
        if abs(delta) < 1e-9:
            winner = "tie"
        elif delta > 0:
            winner = "runB"
        else:
            winner = "runA"
    else:
        delta = 0.0
        winner = "runB" if score_a_display == "(missing)" else "runA"

    return MetricRow(
        metric=f"eval_score({eval_metric})",
        val_a=score_a_display,
        val_b=score_b_display,
        delta=delta,
        winner=winner,
    )


# ---------------------------------------------------------------------------
# 内部辅助：metrics.jsonl 读取
# ---------------------------------------------------------------------------


def _load_last_eval_per_task(
    run_id: str,
    *,
    runs_root: Path | None = None,
) -> dict[str, dict[str, Any]]:
    """读取 metrics.jsonl，返回每个 task_name 的最后一条 eval 记录的 data dict。

    结论：只看 phase=evaluating, kind=eval 的记录；
          同一 task_name 可能有多条（多次 eval），只取最后一条。

    返回：
        {task_name: {metric_key: value, ...}}
        例：{"gsm8k": {"acc": 0.57, "acc_norm": 0.56}}
    """
    run_dir_path = _resolve_run_dir(run_id, runs_root)
    metrics_path = run_dir_path / "metrics.jsonl"

    if not metrics_path.exists():
        return {}

    last_eval: dict[str, dict[str, Any]] = {}

    with metrics_path.open(encoding="utf-8") as f:
        for line_no, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                logger.warning("metrics.jsonl 第 %d 行 JSON 解析失败，跳过", line_no)
                continue

            if obj.get("phase") != "evaluating" or obj.get("kind") != "eval":
                continue

            data = obj.get("data", {})
            task_name = data.get("task_name")
            if not task_name:
                logger.warning("metrics.jsonl 第 %d 行 eval 记录缺少 task_name，跳过", line_no)
                continue

            # 取该 task_name 除 task_name 外的所有 metric key
            task_data = {k: v for k, v in data.items() if k != "task_name"}
            last_eval[task_name] = task_data

    return last_eval


def _extract_eval_score(
    eval_data: dict[str, dict[str, Any]],
    eval_metric: str,
) -> float | None:
    """从 eval_data 中提取指定 task 的 acc 值。

    结论：优先找 task_name == eval_metric，取 "acc" 字段。
          如果 "acc" 不存在，尝试第一个 float 值。
          如果 task 不存在，返回 None。
    """
    task_data = eval_data.get(eval_metric)
    if task_data is None:
        return None

    # 优先 acc 字段
    if "acc" in task_data:
        val = task_data["acc"]
        if isinstance(val, (int, float)):
            return float(val)

    # 退而求其次，取第一个数值字段
    for val in task_data.values():
        if isinstance(val, (int, float)):
            return float(val)

    return None


# ---------------------------------------------------------------------------
# 内部辅助：config 读取
# ---------------------------------------------------------------------------


def _load_config_dict(run_dir_path: Path) -> dict[str, Any]:
    """读取 run_dir/config.yaml，返回原始 dict（不做 Pydantic 校验）。

    config.yaml 可能不完整（test fixture），用 raw dict 更灵活。
    """
    import yaml  # noqa: PLC0415

    config_path = run_dir_path / "config.yaml"
    if not config_path.exists():
        logger.warning("config.yaml 不存在：%s", config_path)
        return {}

    try:
        data = yaml.safe_load(config_path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except Exception as e:
        logger.warning("config.yaml 读取失败：%s，error=%s", config_path, e)
        return {}


# ---------------------------------------------------------------------------
# 内部辅助：report.md 决策 section 提取
# ---------------------------------------------------------------------------

_DECISION_RE = re.compile(r"^##\s+决策\s*$", re.MULTILINE)


def _extract_decision_section(report_path: Path, run_label: str) -> str:
    """提取 report.md 的 ## 决策 section 内容。

    返回：
        section 内容字符串（去除首尾空白）；
        section 缺失时返回 "(no decision section)"，并 log warning。
    """
    if not report_path.exists():
        logger.warning("report.md 不存在，run=%s，path=%s", run_label, report_path)
        return "(no decision section)"

    content = report_path.read_text(encoding="utf-8")
    lines = content.split("\n")
    start_idx: int | None = None

    for i, line in enumerate(lines):
        if _DECISION_RE.match(line.strip()):
            start_idx = i
            break

    if start_idx is None:
        logger.warning(
            "report.md 缺少 ## 决策 section，run=%s，path=%s",
            run_label, report_path,
        )
        return "(no decision section)"

    # 找到 section 结束（下一个 ## 或文档末尾）
    end_idx = len(lines)
    for i in range(start_idx + 1, len(lines)):
        if lines[i].strip().startswith("## "):
            end_idx = i
            break

    section_content = "\n".join(lines[start_idx + 1 : end_idx]).strip()
    return section_content if section_content else "(empty decision section)"
