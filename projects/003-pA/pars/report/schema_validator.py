"""
pars.report.schema_validator — 报告 schema 校验器。

结论：O2 strict gate 实现。分两层：
  1. validate_report_schema(report_path) — 校验 report.md 内容结构
  2. validate_report_artifacts(run_dir)  — 校验 run_dir 下的 artifact 文件完整性

设计原则：
  - 校验失败即返回错误列表，调用方决定是否 raise
  - H2 section 用正则 `^## (.*)$` 匹配（MULTILINE），不依赖第三方解析库
  - strict gate：一条错误就表示校验不通过，调用方可据此 raise

validate_report_schema 断言（对齐 spec §6 O2 + architecture §9）：
  - H2 sections 存在: ## 元数据 / ## 训练曲线 / ## 分数对比 / ## 失败归因 / ## 决策
  - `![training curve]` 引用的 PNG 文件存在
  - `## 分数对比` 下有 markdown table（|.*|.*|）
  - `## 决策` 段含关键字 [继续|停止|改方向] 之一

validate_report_artifacts 规则（对齐 T021.md 任务说明）：
  - artifacts/scores.json 存在且含 "baseline" key
  - metrics.jsonl 存在且非空
  - state=failed 时 failure_attribution.md 必须存在
  - FA 存在时通过 failure_schema.parse_markdown + validate_quality 严格 gate
"""

from __future__ import annotations

import json
import re
from pathlib import Path


# ---------------------------------------------------------------------------
# 内部正则常量
# ---------------------------------------------------------------------------

# H2 section 标题匹配（MULTILINE 模式）
_H2_RE = re.compile(r"^##\s+(.+?)(?:\s*\(.*\))?\s*$", re.MULTILINE)

# 必要 H2 sections（含模糊匹配支持中文括号注释）
_REQUIRED_SECTIONS = [
    ("元数据", re.compile(r"^##\s+元数据\s*$", re.MULTILINE)),
    ("训练曲线", re.compile(r"^##\s+训练曲线\s*$", re.MULTILINE)),
    ("分数对比", re.compile(r"^##\s+分数对比\s*$", re.MULTILINE)),
    ("失败归因", re.compile(r"^##\s+失败归因", re.MULTILINE)),   # 宽松：允许括号说明
    ("决策", re.compile(r"^##\s+决策\s*$", re.MULTILINE)),
]

# 图片引用正则：匹配 ![...](path.png) 形式
_IMG_RE = re.compile(r"!\[.*?\]\(([^)]+\.png)\)", re.IGNORECASE)

# Markdown table 行正则：至少两列
_TABLE_ROW_RE = re.compile(r"^\|.+\|.+\|", re.MULTILINE)

# 决策关键词
_DECISION_KEYWORDS_RE = re.compile(r"(继续|停止|改方向)")


def validate_report_schema(report_path: Path) -> tuple[bool, list[str]]:
    """校验 report.md 的结构完整性（O2 schema gate）。

    结论：纯正则检查，不调用 LLM。检查 H2 sections、PNG 引用、table、决策关键词。
          全部通过返回 (True, [])；任一失败返回 (False, [错误消息, ...])。

    参数：
        report_path : Path - report.md 文件路径

    返回：
        (ok: bool, errors: list[str]) — ok=True 时 errors 为空列表
    """
    errors: list[str] = []

    # --- 检查文件存在 ---
    if not report_path.exists():
        return False, [f"report.md 不存在: {report_path}"]

    content = report_path.read_text(encoding="utf-8")

    # --- 检查必要 H2 sections ---
    for section_name, pattern in _REQUIRED_SECTIONS:
        if not pattern.search(content):
            errors.append(f"报告缺少必要章节 '## {section_name}'（missing {section_name} section）")

    # --- 检查 PNG 文件引用存在性 ---
    img_matches = _IMG_RE.findall(content)
    for img_rel_path in img_matches:
        # 图片路径相对于 report.md 所在目录
        img_abs = report_path.parent / img_rel_path
        if not img_abs.exists():
            errors.append(
                f"报告引用的图片文件不存在: {img_rel_path} "
                f"（期望绝对路径: {img_abs}）"
            )

    # --- 检查 ## 分数对比 下有 markdown table ---
    score_section_content = _extract_section_content(content, "分数对比")
    if score_section_content is not None:
        if not _TABLE_ROW_RE.search(score_section_content):
            errors.append(
                "## 分数对比 section 缺少 markdown table（| ... | ... | 格式）"
                "（missing score comparison table）"
            )
    # 若 section 不存在，已在上面的 H2 检查中报错，此处不重复

    # --- 检查 ## 决策 段含关键词 [继续|停止|改方向] ---
    decision_content = _extract_section_content(content, "决策")
    if decision_content is not None:
        if not _DECISION_KEYWORDS_RE.search(decision_content):
            errors.append(
                "## 决策 section 缺少关键词 [继续|停止|改方向]"
                "（missing decision keyword: 继续/停止/改方向）"
            )

    return (len(errors) == 0, errors)


def validate_report_artifacts(run_dir: Path) -> list[str]:
    """校验 run_dir 下 artifact 文件的完整性（O2 strict gate 前置校验）。

    结论：校验 scores.json / metrics.jsonl / failure_attribution.md 的存在与内容。
          任何一条违反即返回该错误；调用方可据此决定是否 raise。

    规则（对齐 T021.md）：
    1. artifacts/scores.json 存在
    2. scores.json 含 "baseline" key
    3. metrics.jsonl 存在且非空（至少 1 行有效 JSON）
    4. state=failed → failure_attribution.md 必须存在
    5. failure_attribution.md 存在 → 必须通过 parse_markdown + validate_quality

    参数：
        run_dir : Path - run 数据目录（含 config.yaml / metrics.jsonl / artifacts/）

    返回：
        list[str] — 错误消息列表（空列表表示全通过）
    """
    errors: list[str] = []

    # --- 1. scores.json 存在检查 ---
    scores_path = run_dir / "artifacts" / "scores.json"
    if not scores_path.exists():
        errors.append(f"artifacts/scores.json 不存在: {scores_path}")
    else:
        # --- 2. scores.json 含 baseline key ---
        try:
            scores = json.loads(scores_path.read_text(encoding="utf-8"))
            if "baseline" not in scores:
                errors.append(
                    f"artifacts/scores.json 缺少 'baseline' key（当前 keys: {list(scores.keys())}）"
                )
        except (json.JSONDecodeError, OSError) as e:
            errors.append(f"artifacts/scores.json 读取/解析失败: {e}")

    # --- 3. metrics.jsonl 存在且非空 ---
    metrics_path = run_dir / "metrics.jsonl"
    if not metrics_path.exists():
        errors.append(f"metrics.jsonl 不存在: {metrics_path}")
    else:
        content = metrics_path.read_text(encoding="utf-8").strip()
        if not content:
            errors.append("metrics.jsonl 为空（empty metrics.jsonl），至少需要 1 条记录")
        else:
            # 至少有 1 行能解析为合法 JSON
            valid_lines = 0
            for line in content.splitlines():
                line = line.strip()
                if not line:
                    continue
                try:
                    json.loads(line)
                    valid_lines += 1
                except json.JSONDecodeError:
                    pass
            if valid_lines == 0:
                errors.append("metrics.jsonl 中没有有效 JSON 记录（所有行均解析失败）")

    # --- 4. state=failed → FA 必须存在 ---
    state_path = run_dir / "state.json"
    state_is_failed = False
    if state_path.exists():
        try:
            state = json.loads(state_path.read_text(encoding="utf-8"))
            if state.get("phase") == "failed":
                state_is_failed = True
        except (json.JSONDecodeError, OSError):
            pass  # state.json 解析失败不阻止其他校验

    fa_path = run_dir / "failure_attribution.md"
    if state_is_failed and not fa_path.exists():
        errors.append(
            "state=failed 但 failure_attribution.md 不存在"
            "（失败归因是 state=failed 时的必要文件）"
        )

    # --- 5. FA 存在 → 通过 parse_markdown + validate_quality strict gate ---
    if fa_path.exists():
        _validate_fa_quality(fa_path, errors)

    return errors


def _validate_fa_quality(fa_path: Path, errors: list[str]) -> None:
    """内部辅助：校验 failure_attribution.md 的质量。

    结论：严格调用 T020 的 parse_markdown + validate_quality；
          任何解析失败或质量不达标均追加到 errors 列表。
          不 raise — 错误信息追加给调用方聚合。
    """
    # 延迟导入，避免循环引用风险
    from pars.report.failure_schema import parse_markdown, validate_quality  # noqa: PLC0415

    try:
        fa_text = fa_path.read_text(encoding="utf-8")
        fa = parse_markdown(fa_text)
    except (ValueError, OSError) as e:
        errors.append(f"failure_attribution.md 解析失败: {e}")
        return

    ok, quality_errors = validate_quality(fa)
    if not ok:
        for qe in quality_errors:
            errors.append(f"failure_attribution.md 质量校验失败: {qe}")


def _extract_section_content(md_content: str, section_name: str) -> str | None:
    """提取指定 H2 section 的内容（不含标题行本身）。

    结论：以下一个 H2 或文档末尾为 section 结束边界。
          section_name 用于前缀匹配（支持 "失败归因(必填...)" 格式）。

    参数：
        md_content   : str - 完整 markdown 文本
        section_name : str - 目标 section 名称（前缀匹配）

    返回：
        section 内容字符串（不含标题行）；若 section 不存在返回 None
    """
    # 按行分割，找到目标 section 起始行
    lines = md_content.split("\n")
    start_idx: int | None = None

    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("## ") and section_name in stripped:
            start_idx = i
            break

    if start_idx is None:
        return None

    # 找到 section 结束（下一个 ## 标题或文档末尾）
    end_idx = len(lines)
    for i in range(start_idx + 1, len(lines)):
        if lines[i].strip().startswith("## "):
            end_idx = i
            break

    return "\n".join(lines[start_idx + 1 : end_idx])
