"""
pars.report.failure_schema — FailureAttribution Pydantic v2 模型与校验器。

结论：D16 半结构化失败归因 schema 是 R3 Critical 风险的核心缓解。
      纯自由文本会让 worker 输出"可能是数据问题，可能是超参问题"（产品价值崩塌）；
      本 schema 通过必填字段 + 枚举归因 + 数字引用强制 + next_steps 关键词校验
      消除这种崩塌模式。

字段来源：
  - architecture.md §9 — failure_attribution.md 半结构化 schema 全文
  - tasks/T020.md Outputs — 字段约束细节

对外 API（T021 消费端 strict gate 使用）：
  - CauseCategory      : 归因枚举（对齐 architecture §9）
  - FailureAttribution : Pydantic v2 主模型
  - parse_markdown(md_text) -> FailureAttribution  : 解析 worker 写的 md 文件
  - validate_quality(fa) -> tuple[bool, list[str]] : 二次语义校验（Pydantic 之上）

设计约束：
  1. validate_quality 严格 gate：False 即 report schema gate 失败（spec §6 O2）
  2. 不存在"警告但不 fail"的半态语义（spec.md §6 O2 + R1 Medium #2 修复）
  3. observation 含数字：正则 r"\\b\\d+\\.?\\d*\\b" （整数和小数均可）
  4. next_steps 具体变更：至少 1 项含关键词（lr/epoch/rank/batch/data 等）或含具体数值赋值
"""

from __future__ import annotations

import json
import re
from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator


# ---------------------------------------------------------------------------
# 归因枚举：对齐 architecture §9 完整枚举
# ---------------------------------------------------------------------------


class CauseCategory(str, Enum):
    """失败归因分类枚举。

    来源：architecture.md §9 failure_attribution.md 的"归因"复选框列表。
    继承 str 使得 Pydantic JSON 序列化为字符串值（非枚举名），
    便于 T021 渲染器和 T026 schema validator 直接比较字符串。
    """

    DATA_FORMAT = "DATA_FORMAT"        # 数据格式错（具体哪条 / 哪种）
    LR_TOO_HIGH = "LR_TOO_HIGH"        # 学习率太大
    LR_TOO_LOW = "LR_TOO_LOW"          # 学习率太小
    DIST_DRIFT = "DIST_DRIFT"          # eval 集与训练集分布漂移
    BASELINE_STRONG = "BASELINE_STRONG"  # 基线本身已够强（LoRA 上限有限）
    EPOCH_NOT_ENOUGH = "EPOCH_NOT_ENOUGH"  # 训练 epoch 不足
    LORA_RANK_LOW = "LORA_RANK_LOW"    # LoRA rank 不足
    OOM = "OOM"                        # 显存 OOM 导致 batch 太小
    OTHER = "OTHER"                    # 其他（必须自由叙述）


# ---------------------------------------------------------------------------
# 主模型：FailureAttribution
# ---------------------------------------------------------------------------

# 用于 observation 含数字的正则：整数或小数（含科学计数法如 1e-4）
_NUMBER_RE = re.compile(r"\b\d+\.?\d*\b")

# 用于 next_steps 具体变更的关键词正则：
# 方案：1) 含 key=value 形式（lr=, epoch=, rank=, batch=, data= 等）
#        2) 或含关键词（lr, epoch, rank, batch, data）+ 数字
#        3) 或含明确具体动作词（模型名、数据集名、数值变更）
_NEXT_STEP_KEYWORD_RE = re.compile(
    r"(lr|epoch|rank|batch|data|model|dataset|learning[_\s]rate|lora|alpha|weight)\s*[=：:\-]?\s*\S+",
    re.IGNORECASE,
)
# 备用：next_step 含数字也算具体（"尝试 3 个 epoch" 算具体）
_NEXT_STEP_NUMBER_RE = re.compile(r"\b\d+\.?\d*[eE][+-]?\d+|\b\d+\.?\d*\b")


class FailureAttribution(BaseModel):
    """失败归因半结构化 schema（Pydantic v2）。

    结论：R3 Critical 缓解核心——必填字段强制证据，自由段允许新模式。
          所有约束来自 architecture §9 + T020.md Outputs + spec §6 O2。

    契约：
      - Pydantic 层：字段存在性 + 类型 + 长度约束
      - validate_quality 层：observation 含数字 + next_steps 具体性 + OTHER 叙述
    """

    model_config = ConfigDict(extra="forbid")

    assumption: str = Field(
        min_length=20,
        max_length=2000,
        description=(
            "原本期待发生什么（≥20 字符，≤2000 字符）。"
            "应描述具体的预期结果，如期望 metric 值或行为。"
        ),
    )
    observation: str = Field(
        min_length=30,
        description=(
            "实际发生了什么（≥30 字符，必须引用 metric 数字）。"
            "validate_quality 会用正则检验是否存在数字。"
        ),
    )
    causes: list[CauseCategory] = Field(
        min_length=1,
        description=(
            "归因分类列表（至少 1 项，枚举值见 CauseCategory）。"
            "若选 OTHER，causes_detail 必须填写（由 validate_quality 强制）。"
        ),
    )
    causes_detail: str | None = Field(
        default=None,
        description=(
            "归因补充说明（可空）。"
            "若 causes 含 CauseCategory.OTHER，此字段必须非空（validate_quality 强制）。"
        ),
    )
    next_steps: list[str] = Field(
        min_length=1,
        description=(
            "下一步建议列表（至少 1 项）。"
            "每项应含具体 hyperparam / 数据 / 模型变更。"
            "validate_quality 检验至少 1 项含具体关键词或数值。"
        ),
    )
    free_narrative: str | None = Field(
        default=None,
        description=(
            "自由叙述（可空，但鼓励）。"
            "worker 的 reasoning chain，允许描述新模式、异常发现等。"
        ),
    )

    @field_validator("assumption")
    @classmethod
    def assumption_not_whitespace_only(cls, v: str) -> str:
        """拒绝纯空白的 assumption（即使满足长度约束）。"""
        if not v.strip():
            msg = "assumption 不能为纯空白字符串"
            raise ValueError(msg)
        return v

    @field_validator("observation")
    @classmethod
    def observation_not_whitespace_only(cls, v: str) -> str:
        """拒绝纯空白的 observation（即使满足长度约束）。"""
        if not v.strip():
            msg = "observation 不能为纯空白字符串"
            raise ValueError(msg)
        return v


# ---------------------------------------------------------------------------
# 二次语义校验（Pydantic 之上的 validate_quality）
# ---------------------------------------------------------------------------


def validate_quality(fa: FailureAttribution) -> tuple[bool, list[str]]:
    """对 FailureAttribution 进行语义二次校验。

    结论：Pydantic 负责结构约束；validate_quality 负责内容语义约束。
          spec §6 O2 + R1 Medium #2 明确要求：False 即 gate 失败，无半态语义。

    校验项：
    1. observation 含数字（整数或小数）— 证明 worker 引用了可观测 metric 事实
    2. next_steps 至少 1 项含具体变更词（lr/epoch/rank/batch/data 等 + 数值）
    3. 若 causes 含 OTHER，causes_detail 不能为空

    参数：
        fa : 已通过 Pydantic 校验的 FailureAttribution 实例

    返回：
        (True, [])            — 通过，report O2 gate 通过
        (False, [str, ...])   — 失败，list 为可操作错误消息
    """
    errors: list[str] = []

    # --- 规则 1：observation 必须含数字 ---
    if not _NUMBER_RE.search(fa.observation):
        errors.append(
            "observation 中未检测到 metric 数字（整数或小数）。"
            "请在 observation 中引用具体数值，如 'accuracy=0.41'、'loss=1.23'、'epoch 3' 等。"
        )

    # --- 规则 2：next_steps 至少 1 项含具体变更词或数值 ---
    has_specific_step = any(
        _NEXT_STEP_KEYWORD_RE.search(step) or _NEXT_STEP_NUMBER_RE.search(step)
        for step in fa.next_steps
    )
    if not has_specific_step:
        errors.append(
            "next_steps 中未检测到具体变更关键词或数值（如 lr=、epoch=、rank=、data= 等）。"
            "请提供可执行的具体建议，如 '将 lr=2e-4 改为 lr=5e-5' 或 '增加 epoch=5'。"
        )

    # --- 规则 3：OTHER 归因必须有 causes_detail ---
    if CauseCategory.OTHER in fa.causes:
        if not fa.causes_detail or not fa.causes_detail.strip():
            errors.append(
                "causes 含 CauseCategory.OTHER 时，causes_detail 不能为空。"
                "请在 causes_detail 中详细说明具体原因（OTHER 要求自由叙述，防止归因为空）。"
            )

    return (len(errors) == 0, errors)


# ---------------------------------------------------------------------------
# Markdown 解析器：parse_markdown
# ---------------------------------------------------------------------------

# architecture §9 failure_attribution.md 的 section 标题正则
_SECTION_RE = re.compile(r"^##\s+(.+)$", re.MULTILINE)

# 必填字段行正则（支持中文冒号和英文冒号）
_ASSUMPTION_RE = re.compile(r"\*\*假设\*\*[：:]\s*(.+?)(?=\n|$)")
_OBSERVATION_RE = re.compile(r"\*\*观察\*\*[：:]\s*(.+?)(?=\n|$)")
_NEXT_STEP_RE = re.compile(r"\*\*下一步建议\*\*[：:]\s*(.+?)(?=\n##|$)", re.DOTALL)

# 归因复选框解析正则：匹配 [x] 或 [X] 标记
_CAUSE_CHECKBOX_RE = re.compile(r"\-\s*\[x\]\s*(.+?)(?=\n|$)", re.IGNORECASE)

# 归因关键词到 CauseCategory 的映射（宽松匹配，允许部分词）
_CAUSE_KEYWORD_MAP: list[tuple[str, CauseCategory]] = [
    ("数据格式", CauseCategory.DATA_FORMAT),
    ("data format", CauseCategory.DATA_FORMAT),
    ("学习率太大", CauseCategory.LR_TOO_HIGH),
    ("lr.*太大", CauseCategory.LR_TOO_HIGH),
    ("学习率太小", CauseCategory.LR_TOO_LOW),
    ("lr.*太小", CauseCategory.LR_TOO_LOW),
    ("分布漂移", CauseCategory.DIST_DRIFT),
    ("dist.*drift", CauseCategory.DIST_DRIFT),
    ("基线.*已够强", CauseCategory.BASELINE_STRONG),
    ("baseline.*strong", CauseCategory.BASELINE_STRONG),
    ("epoch.*不足", CauseCategory.EPOCH_NOT_ENOUGH),
    ("训练.*epoch", CauseCategory.EPOCH_NOT_ENOUGH),
    ("rank.*不足", CauseCategory.LORA_RANK_LOW),
    ("lora.*rank", CauseCategory.LORA_RANK_LOW),
    ("oom", CauseCategory.OOM),
    ("显存.*oom", CauseCategory.OOM),
    ("其他", CauseCategory.OTHER),
    ("other", CauseCategory.OTHER),
]


def _match_cause_category(text: str) -> CauseCategory | None:
    """从文本匹配归因枚举值（宽松匹配，不区分大小写）。"""
    text_lower = text.lower()
    for keyword, category in _CAUSE_KEYWORD_MAP:
        if re.search(keyword, text_lower):
            return category
    return None


def parse_markdown(md_text: str) -> FailureAttribution:
    """解析 worker 写的 failure_attribution.md 文本，返回 FailureAttribution 实例。

    结论：半结构化解析——按 H2 section 切分，用正则抓取必填字段行。
          解析失败时抛 ValueError（明确指出缺少哪个字段），便于操作员诊断。

    architecture §9 定义的 failure_attribution.md 格式：
    ```
    # Failure attribution · <ULID>

    ## 必填字段
    - **假设**：<...>
    - **观察**：<...>（贴 metric 数字）
    - **归因**：
      - [x] <归因选项>
    - **下一步建议**：<...>

    ## 自由叙述（可选，但鼓励）
    <reasoning chain>
    ```

    参数：
        md_text : failure_attribution.md 全文内容

    返回：
        FailureAttribution 实例（已通过 Pydantic 校验）

    Raises：
        ValueError : 缺少必要 section 或必填字段行
    """
    # --- 步骤 1：提取各 section 内容 ---
    sections = _extract_sections(md_text)

    required_section_key = "必填字段"
    if required_section_key not in sections:
        msg = f"failure_attribution.md 缺少 '## {required_section_key}' section。请按 architecture §9 格式填写。"
        raise ValueError(msg)

    required_text = sections[required_section_key]
    free_text = sections.get("自由叙述（可选，但鼓励）") or sections.get("自由叙述") or ""

    # --- 步骤 2：提取 assumption ---
    assumption_match = _ASSUMPTION_RE.search(required_text)
    if not assumption_match:
        msg = "## 必填字段 section 中缺少 '- **假设**：...' 行。"
        raise ValueError(msg)
    assumption = assumption_match.group(1).strip()

    # --- 步骤 3：提取 observation ---
    observation_match = _OBSERVATION_RE.search(required_text)
    if not observation_match:
        msg = "## 必填字段 section 中缺少 '- **观察**：...' 行。"
        raise ValueError(msg)
    observation = observation_match.group(1).strip()

    # --- 步骤 4：提取归因（复选框）---
    causes: list[CauseCategory] = []
    causes_detail: str | None = None

    checkbox_matches = _CAUSE_CHECKBOX_RE.findall(required_text)
    for matched_text in checkbox_matches:
        category = _match_cause_category(matched_text)
        if category is not None and category not in causes:
            causes.append(category)

    # 若没有匹配到任何归因复选框，使用 OTHER 并标记需要说明
    if not causes:
        causes = [CauseCategory.OTHER]
        causes_detail = "（parse_markdown 未能从 markdown 中识别归因复选框，请手动确认）"

    # --- 步骤 5：提取 next_steps ---
    next_step_match = _NEXT_STEP_RE.search(required_text)
    if not next_step_match:
        msg = "## 必填字段 section 中缺少 '- **下一步建议**：...' 行。"
        raise ValueError(msg)

    next_step_raw = next_step_match.group(1).strip()
    # 支持多行 next_steps（每行以 - 开头）
    if "\n" in next_step_raw:
        next_steps = [
            line.lstrip("-• ").strip()
            for line in next_step_raw.splitlines()
            if line.strip() and line.strip() not in ("-", "•")
        ]
    else:
        next_steps = [next_step_raw] if next_step_raw else []

    if not next_steps:
        msg = "## 必填字段 section 中 '- **下一步建议**：' 内容为空。"
        raise ValueError(msg)

    # --- 步骤 6：构造 FailureAttribution（Pydantic 二次校验）---
    return FailureAttribution(
        assumption=assumption,
        observation=observation,
        causes=causes,
        causes_detail=causes_detail,
        next_steps=next_steps,
        free_narrative=free_text.strip() if free_text.strip() else None,
    )


def _extract_sections(md_text: str) -> dict[str, str]:
    """将 markdown 按 H2 (##) 切分为 section 字典。

    返回：{section_title: section_body_text}
    section_body_text 不含 H2 标题行本身。
    """
    result: dict[str, str] = {}
    sections = _SECTION_RE.split(md_text)
    # split 结果：[before_first_h2, title1, body1, title2, body2, ...]
    # 索引从 1 开始，奇数为标题，偶数为内容
    i = 1
    while i + 1 < len(sections):
        title = sections[i].strip()
        body = sections[i + 1]
        result[title] = body
        i += 2
    return result


# ---------------------------------------------------------------------------
# 便捷 validate 入口（T021 消费端 strict gate 使用）
# ---------------------------------------------------------------------------


def validate(data: dict[str, Any]) -> FailureAttribution:
    """从字典构造 FailureAttribution 并通过 validate_quality 严格 gate。

    结论：T021 渲染器调用的统一入口。先 Pydantic 校验，再 validate_quality 语义校验。
          任一校验失败均抛 ValueError，包含可操作错误信息。

    参数：
        data : 来自 failure_attribution.md parse 或 JSON 加载的字典

    返回：
        FailureAttribution（已通过 Pydantic + validate_quality 双重校验）

    Raises：
        pydantic.ValidationError : Pydantic 结构校验失败（缺字段/类型错误/枚举非法）
        ValueError                : validate_quality 语义校验失败（无数字/无具体 next_steps 等）
    """
    fa = FailureAttribution.model_validate(data)
    ok, errors = validate_quality(fa)
    if not ok:
        joined = "\n".join(f"  - {e}" for e in errors)
        msg = f"FailureAttribution 语义校验失败（report O2 gate 拒绝）：\n{joined}"
        raise ValueError(msg)
    return fa


def to_json(fa: FailureAttribution) -> str:
    """将 FailureAttribution 序列化为 JSON 字符串。

    便捷包装 model_dump_json()，供 T021 渲染器直接使用。
    """
    return fa.model_dump_json(indent=2)


def from_json(json_str: str) -> FailureAttribution:
    """从 JSON 字符串反序列化 FailureAttribution。

    便捷包装 model_validate_json()，不经过 validate_quality（保留原始数据）。
    如需严格 gate，在反序列化后调用 validate_quality()。
    """
    data = json.loads(json_str)
    return FailureAttribution.model_validate(data)
