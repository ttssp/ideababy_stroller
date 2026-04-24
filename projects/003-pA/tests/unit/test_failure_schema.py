"""
tests/unit/test_failure_schema.py — FailureAttribution schema + validate_quality 测试。

覆盖（≥15 个测试用例，每条注释说明防哪种崩塌模式）：
1.  合法完整 FA → Pydantic 正常加载，validate_quality 返回 (True, [])
2.  observation 无数字 → validate_quality 返回 (False, [...])
3.  next_steps 无具体词（"继续尝试" × 2）→ validate_quality 返回 (False, [...])
4.  causes 空列表 → Pydantic ValidationError
5.  assumption 太短 (< 20 字符) → Pydantic ValidationError
6.  assumption 太长 (> 2000 字符) → Pydantic ValidationError
7.  observation 太短 (< 30 字符) → Pydantic ValidationError
8.  CauseCategory.OTHER 且 causes_detail 为空 → validate_quality 返回 (False, [...])
9.  CauseCategory.OTHER 且 causes_detail 有实质内容 → validate_quality 通过
10. from_json / to_json 双向 round-trip 测试
11. parse_markdown happy path → 正确解析各字段
12. parse_markdown 缺 ## 必填字段 section → ValueError
13. parse_markdown 缺 assumption 行 → ValueError
14. CauseCategory 枚举值合法性验证（传入枚举之外的字符串 → Pydantic error）
15. next_steps 含 lr=1e-4 → validate_quality 通过（具体 hyperparam 变更）
16. observation 含整数（"epoch 3"）→ validate_quality 通过（证明引用了可观测事实）
17. causes 含多个枚举项（合法）→ Pydantic 正常加载
18. validate_quality 对 None causes_detail + OTHER 的明确失败消息
"""

from __future__ import annotations

import json

import pytest
from pydantic import ValidationError

from pars.report.failure_schema import (
    CauseCategory,
    FailureAttribution,
    parse_markdown,
    validate_quality,
)


# ---------------------------------------------------------------------------
# 辅助函数：合法 FailureAttribution 参数
# ---------------------------------------------------------------------------


def _valid_fa_kwargs() -> dict:
    """返回最小合法 FailureAttribution 构造参数。"""
    return {
        "assumption": "预计 LoRA 微调后 gsm8k 准确率从基线 0.45 提升至 0.55 以上",
        "observation": "LoRA final epoch accuracy=0.41，低于 baseline 0.45，loss 曲线在 epoch 2 出现拐点",
        "causes": [CauseCategory.LR_TOO_HIGH],
        "causes_detail": None,
        "next_steps": ["将 lr=2e-4 降低至 lr=5e-5，重新训练 epoch=3 观察收敛"],
        "free_narrative": None,
    }


# ---------------------------------------------------------------------------
# T1: 合法完整 FA → Pydantic 正常加载 + validate_quality 通过
# 防止崩塌：基础合法路径必须通过
# ---------------------------------------------------------------------------


def test_valid_full_fa_passes_pydantic_and_validate_quality() -> None:
    """should pass Pydantic validation and validate_quality when all fields are valid."""
    fa = FailureAttribution(**_valid_fa_kwargs())
    ok, errors = validate_quality(fa)
    assert ok is True, f"期望 validate_quality 通过，但得到错误: {errors}"
    assert errors == []


# ---------------------------------------------------------------------------
# T2: observation 无数字 → validate_quality 返回 (False, [...])
# 防止崩塌：worker 写"eval 结果不好" → 没有 metric 数字 → schema gate 拒绝
# ---------------------------------------------------------------------------


def test_observation_without_number_fails_validate_quality() -> None:
    """should fail validate_quality when observation has no numeric value."""
    kwargs = _valid_fa_kwargs()
    kwargs["observation"] = "LoRA 训练完成后评测结果比预期差，基线更强，可能是数据问题"
    fa = FailureAttribution(**kwargs)
    ok, errors = validate_quality(fa)
    assert ok is False, "observation 无数字应导致 validate_quality 失败"
    assert any("observation" in e.lower() or "数字" in e or "metric" in e.lower() for e in errors)


# ---------------------------------------------------------------------------
# T3: next_steps 无具体词（全是"继续尝试"）→ validate_quality 返回 (False, [...])
# 防止崩塌：worker 写"继续尝试调超参" → 无任何具体变更 → schema gate 拒绝
# ---------------------------------------------------------------------------


def test_next_steps_all_vague_fails_validate_quality() -> None:
    """should fail validate_quality when next_steps contain no actionable keywords."""
    kwargs = _valid_fa_kwargs()
    kwargs["next_steps"] = ["继续尝试", "也许可以调整一下"]
    fa = FailureAttribution(**kwargs)
    ok, errors = validate_quality(fa)
    assert ok is False, "next_steps 无具体词应导致 validate_quality 失败"
    assert any("next_step" in e.lower() or "具体" in e or "关键词" in e for e in errors)


# ---------------------------------------------------------------------------
# T4: causes 空列表 → Pydantic ValidationError（防止归因为空）
# 防止崩塌：worker 不填归因枚举 → 产品价值崩塌 → Pydantic 直接拒绝
# ---------------------------------------------------------------------------


def test_empty_causes_raises_pydantic_validation_error() -> None:
    """should raise ValidationError when causes is an empty list."""
    kwargs = _valid_fa_kwargs()
    kwargs["causes"] = []
    with pytest.raises(ValidationError) as exc_info:
        FailureAttribution(**kwargs)
    assert "causes" in str(exc_info.value)


# ---------------------------------------------------------------------------
# T5: assumption 太短 (< 20 字符) → Pydantic ValidationError
# 防止崩塌：worker 随便填"数据有问题" → 不够有信息量 → Pydantic 拒绝
# ---------------------------------------------------------------------------


def test_assumption_too_short_raises_pydantic_validation_error() -> None:
    """should raise ValidationError when assumption is shorter than 20 characters."""
    kwargs = _valid_fa_kwargs()
    kwargs["assumption"] = "太短了不行"  # 仅 5 字符（远少于 20）
    with pytest.raises(ValidationError) as exc_info:
        FailureAttribution(**kwargs)
    assert "assumption" in str(exc_info.value)


# ---------------------------------------------------------------------------
# T6: assumption 太长 (> 2000 字符) → Pydantic ValidationError
# 防止崩塌：长度上界约束，防止 LLM 灌水导致 schema 无效
# ---------------------------------------------------------------------------


def test_assumption_too_long_raises_pydantic_validation_error() -> None:
    """should raise ValidationError when assumption exceeds 2000 characters."""
    kwargs = _valid_fa_kwargs()
    kwargs["assumption"] = "A" * 2001
    with pytest.raises(ValidationError) as exc_info:
        FailureAttribution(**kwargs)
    assert "assumption" in str(exc_info.value)


# ---------------------------------------------------------------------------
# T7: observation 太短 (< 30 字符) → Pydantic ValidationError
# 防止崩塌：observation 长度下界，强制 worker 提供足够信息
# ---------------------------------------------------------------------------


def test_observation_too_short_raises_pydantic_validation_error() -> None:
    """should raise ValidationError when observation is shorter than 30 characters."""
    kwargs = _valid_fa_kwargs()
    kwargs["observation"] = "结果差 0.1"  # 仅 6 字符（远少于 30）
    with pytest.raises(ValidationError) as exc_info:
        FailureAttribution(**kwargs)
    assert "observation" in str(exc_info.value)


# ---------------------------------------------------------------------------
# T8: CauseCategory.OTHER 且 causes_detail 为空 → validate_quality 返回 (False, [...])
# 防止崩塌：选 OTHER 必须自由叙述，否则等同于不填归因
# ---------------------------------------------------------------------------


def test_other_cause_without_causes_detail_fails_validate_quality() -> None:
    """should fail validate_quality when OTHER cause is selected but causes_detail is empty."""
    kwargs = _valid_fa_kwargs()
    kwargs["causes"] = [CauseCategory.OTHER]
    kwargs["causes_detail"] = None  # 未填必须叙述
    fa = FailureAttribution(**kwargs)
    ok, errors = validate_quality(fa)
    assert ok is False, "CauseCategory.OTHER 且 causes_detail=None 应失败"
    assert any("other" in e.lower() or "detail" in e.lower() or "叙述" in e for e in errors)


# ---------------------------------------------------------------------------
# T9: CauseCategory.OTHER 且 causes_detail 有实质内容 → validate_quality 通过
# 防止崩塌：OTHER + 有实质 causes_detail 是合法的边界情况
# ---------------------------------------------------------------------------


def test_other_cause_with_causes_detail_passes_validate_quality() -> None:
    """should pass validate_quality when OTHER cause has non-empty causes_detail."""
    kwargs = _valid_fa_kwargs()
    kwargs["causes"] = [CauseCategory.OTHER]
    kwargs["causes_detail"] = (
        "训练数据存在标注错误，约 15% 样本的答案格式不符合 GSM8K 标准，导致 loss 震荡"
    )
    fa = FailureAttribution(**kwargs)
    ok, errors = validate_quality(fa)
    assert ok is True, f"OTHER + 有实质 detail 应通过，但错误: {errors}"


# ---------------------------------------------------------------------------
# T10: from_json / to_json 双向 round-trip 测试
# 防止崩塌：schema 序列化反序列化必须幂等，防止 T021 消费端数据丢失
# ---------------------------------------------------------------------------


def test_json_round_trip_produces_equal_object() -> None:
    """should produce equal object after to_json → from_json round-trip."""
    fa = FailureAttribution(**_valid_fa_kwargs())
    json_str = fa.model_dump_json()

    # 反序列化
    data = json.loads(json_str)
    fa2 = FailureAttribution.model_validate(data)

    assert fa == fa2
    assert fa2.causes == [CauseCategory.LR_TOO_HIGH]


# ---------------------------------------------------------------------------
# T11: parse_markdown happy path → 正确解析各字段
# 防止崩塌：worker 写的 failure_attribution.md 能被机器解析，防止人工复制粘贴错误
# ---------------------------------------------------------------------------

_VALID_MARKDOWN = """\
# Failure attribution · 01KPZSDEE8VWSDS83ZS9WHKWES

## 必填字段
- **假设**：预计 LoRA 微调后 gsm8k 准确率从基线 0.45 提升至 0.55 以上
- **观察**：LoRA final epoch accuracy=0.41，低于 baseline 0.45，loss 曲线在 epoch 2 出现拐点
- **归因**：
  - [x] 学习率太大 / 太小（原 lr=, 建议 lr=）
- **下一步建议**：将 lr=2e-4 降低至 lr=5e-5，重新训练 epoch=3 观察收敛

## 自由叙述（可选，但鼓励）
loss 在 epoch2 发生拐点是因为 lr 过高导致梯度爆炸，建议降低 lr 并监控 grad_norm。
"""


def test_parse_markdown_happy_path_extracts_fields() -> None:
    """should correctly extract all fields from well-formed failure_attribution.md."""
    fa = parse_markdown(_VALID_MARKDOWN)
    assert "0.45" in fa.assumption or "提升" in fa.assumption
    assert "0.41" in fa.observation
    assert CauseCategory.LR_TOO_HIGH in fa.causes or len(fa.causes) >= 1
    assert len(fa.next_steps) >= 1
    assert "lr" in fa.next_steps[0].lower() or "5e-5" in fa.next_steps[0]


# ---------------------------------------------------------------------------
# T12: parse_markdown 缺 ## 必填字段 section → ValueError
# 防止崩塌：worker 少写 section 导致静默解析错误
# ---------------------------------------------------------------------------

_MISSING_SECTION_MARKDOWN = """\
# Failure attribution · 01KPZSDEE8VWSDS83ZS9WHKWES

## 自由叙述（可选，但鼓励）
没有必填字段 section 的 markdown。
"""


def test_parse_markdown_missing_required_section_raises_value_error() -> None:
    """should raise ValueError when ## 必填字段 section is missing from markdown."""
    with pytest.raises(ValueError, match="必填字段"):
        parse_markdown(_MISSING_SECTION_MARKDOWN)


# ---------------------------------------------------------------------------
# T13: parse_markdown 缺 assumption 行 → ValueError
# 防止崩塌：必填字段 section 存在但 assumption 行缺失 → 静默错误变显式错误
# ---------------------------------------------------------------------------

_MISSING_ASSUMPTION_MARKDOWN = """\
# Failure attribution · 01KPZSDEE8VWSDS83ZS9WHKWES

## 必填字段
- **观察**：LoRA final epoch accuracy=0.41，低于 baseline 0.45，发现数字偏低
- **归因**：
  - [x] 学习率太大 / 太小（原 lr=, 建议 lr=）
- **下一步建议**：将 lr=2e-4 降低至 lr=5e-5，重新训练

"""


def test_parse_markdown_missing_assumption_raises_value_error() -> None:
    """should raise ValueError when assumption line is missing in required section."""
    with pytest.raises(ValueError, match="假设"):
        parse_markdown(_MISSING_ASSUMPTION_MARKDOWN)


# ---------------------------------------------------------------------------
# T14: CauseCategory 枚举值合法性验证（传入枚举之外的字符串 → Pydantic error）
# 防止崩塌：worker 乱填枚举值（如 "unknown"）导致数据污染
# ---------------------------------------------------------------------------


def test_invalid_cause_category_raises_pydantic_validation_error() -> None:
    """should raise ValidationError when causes contains an invalid enum value."""
    kwargs = _valid_fa_kwargs()
    kwargs["causes"] = ["INVALID_CATEGORY"]  # 非法枚举值
    with pytest.raises(ValidationError) as exc_info:
        FailureAttribution(**kwargs)
    assert "causes" in str(exc_info.value) or "invalid" in str(exc_info.value).lower()


# ---------------------------------------------------------------------------
# T15: next_steps 含 lr=1e-4 → validate_quality 通过
# 防止崩塌：有具体 hyperparam 变更（lr=）的 next_steps 必须被接受
# ---------------------------------------------------------------------------


def test_next_steps_with_lr_assignment_passes_validate_quality() -> None:
    """should pass validate_quality when next_steps contain specific lr= assignment."""
    kwargs = _valid_fa_kwargs()
    kwargs["next_steps"] = ["将 lr=1e-4 改为 lr=5e-5，同时将 epoch=5 以充分收敛"]
    fa = FailureAttribution(**kwargs)
    ok, errors = validate_quality(fa)
    assert ok is True, f"含 lr= 的 next_steps 应通过，但错误: {errors}"


# ---------------------------------------------------------------------------
# T16: observation 含整数（"epoch 3"）→ validate_quality 通过
# 防止崩塌："epoch 3" 也算引用可观测事实，不应误判为"无数字"
# ---------------------------------------------------------------------------


def test_observation_with_integer_epoch_passes_validate_quality() -> None:
    """should pass validate_quality when observation contains integer epoch number."""
    kwargs = _valid_fa_kwargs()
    kwargs["observation"] = (
        "在 epoch 3 之后 train_loss=0.8 不再下降，eval 准确率停留在 baseline 水平"
    )
    fa = FailureAttribution(**kwargs)
    ok, errors = validate_quality(fa)
    assert ok is True, f"含整数 epoch 的 observation 应通过，但错误: {errors}"


# ---------------------------------------------------------------------------
# T17: causes 含多个枚举项（合法）→ Pydantic 正常加载
# 防止崩塌：多归因场景（同时有 LR 和 DATA 问题）必须被支持
# ---------------------------------------------------------------------------


def test_multiple_causes_passes_pydantic_validation() -> None:
    """should pass Pydantic validation when causes contains multiple valid enum values."""
    kwargs = _valid_fa_kwargs()
    kwargs["causes"] = [CauseCategory.LR_TOO_HIGH, CauseCategory.DATA_FORMAT]
    fa = FailureAttribution(**kwargs)
    assert CauseCategory.LR_TOO_HIGH in fa.causes
    assert CauseCategory.DATA_FORMAT in fa.causes
    assert len(fa.causes) == 2


# ---------------------------------------------------------------------------
# T18: validate_quality 对 OTHER + None detail 返回明确错误消息（消息可读性）
# 防止崩塌：错误消息模糊导致操作员不知道如何修复
# ---------------------------------------------------------------------------


def test_other_cause_none_detail_error_message_is_actionable() -> None:
    """should return actionable error message when OTHER cause has no causes_detail."""
    kwargs = _valid_fa_kwargs()
    kwargs["causes"] = [CauseCategory.OTHER]
    kwargs["causes_detail"] = None
    fa = FailureAttribution(**kwargs)
    ok, errors = validate_quality(fa)
    assert ok is False
    # 错误消息应包含"OTHER"或"causes_detail"或中文提示，让操作员明白如何修复
    combined = " ".join(errors).lower()
    assert "other" in combined or "detail" in combined or "other" in combined or "叙述" in combined


# ---------------------------------------------------------------------------
# T19: CauseCategory 枚举覆盖 architecture §9 全部值
# 防止崩塌：枚举漏项会导致 worker 选不到正确归因
# ---------------------------------------------------------------------------


def test_all_cause_categories_defined_per_architecture_spec() -> None:
    """should define all CauseCategory values specified in architecture §9."""
    expected_categories = {
        "DATA_FORMAT",
        "LR_TOO_HIGH",
        "LR_TOO_LOW",
        "DIST_DRIFT",
        "BASELINE_STRONG",
        "EPOCH_NOT_ENOUGH",
        "LORA_RANK_LOW",
        "OOM",
        "OTHER",
    }
    actual_categories = {c.name for c in CauseCategory}
    assert expected_categories == actual_categories, (
        f"枚举值不匹配。缺少: {expected_categories - actual_categories}; "
        f"多余: {actual_categories - expected_categories}"
    )


# ---------------------------------------------------------------------------
# T20: 空 next_steps 列表 → Pydantic ValidationError
# 防止崩塌：next_steps 空列表和 causes 空列表一样是禁止状态
# ---------------------------------------------------------------------------


def test_empty_next_steps_raises_pydantic_validation_error() -> None:
    """should raise ValidationError when next_steps is an empty list."""
    kwargs = _valid_fa_kwargs()
    kwargs["next_steps"] = []
    with pytest.raises(ValidationError) as exc_info:
        FailureAttribution(**kwargs)
    assert "next_steps" in str(exc_info.value)
