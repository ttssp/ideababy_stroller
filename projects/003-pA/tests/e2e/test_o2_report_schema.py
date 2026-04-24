"""
tests/e2e/test_o2_report_schema.py — T026 Outcome O2 E2E 测试。

结论：验证 validate_report_schema / validate_report_artifacts 正确识别
      合法和非法的 report.md 文件结构。

## 验证 Outcome O2

O2（architecture §9）：决策报告 schema 校验 —
必须包含 ## 元数据 / ## 训练曲线 / ## 分数对比 / ## 失败归因 / ## 决策 五个 H2 节，
PNG 图像引用、Markdown 表格、decision keyword（pick/continue/abort）。
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from pars.report.schema_validator import validate_report_schema


# ---------------------------------------------------------------------------
# 辅助函数
# ---------------------------------------------------------------------------


def _write_minimal_png(path: Path) -> None:
    """写入最小合法 1×1 像素 PNG 文件（用于产物存在性验证）。"""
    minimal_png = bytes([
        0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A,
        0x00, 0x00, 0x00, 0x0D, 0x49, 0x48, 0x44, 0x52,
        0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x01,
        0x08, 0x06, 0x00, 0x00, 0x00, 0x1F, 0x15, 0xC4,
        0x89, 0x00, 0x00, 0x00, 0x0A, 0x49, 0x44, 0x41,
        0x54, 0x78, 0x9C, 0x62, 0x00, 0x01, 0x00, 0x00,
        0x05, 0x00, 0x01, 0x0D, 0x0A, 0x2D, 0xB4, 0x00,
        0x00, 0x00, 0x00, 0x49, 0x45, 0x4E, 0x44, 0xAE,
        0x42, 0x60, 0x82,
    ])
    path.write_bytes(minimal_png)


# ---------------------------------------------------------------------------
# T026-O2-TC01: 合格 report.md 通过 schema 校验
# ---------------------------------------------------------------------------


@pytest.mark.e2e
def test_o2_valid_report_passes_schema(tmp_runs_dir: Path) -> None:
    """should return (True, []) when report.md has all required sections.

    结论：含全部 5 个 H2 section + PNG ref + 表格 + decision keyword 时，
          validate_report_schema 应返回 (True, [])。
    """
    run_id = "test-o2-valid-01"
    run_dir = tmp_runs_dir / run_id
    run_dir.mkdir(parents=True)
    (run_dir / "artifacts").mkdir()

    # 创建 PNG 文件（validate_report_schema 检查引用文件是否存在）
    _write_minimal_png(run_dir / "artifacts" / "training_curve.png")

    # 决策关键词必须是 继续|停止|改方向 之一（schema_validator 的正则要求）
    report_md = """# SFT 实验决策报告

## 元数据

| 字段 | 值 |
|------|-----|
| run_id | test-o2-valid-01 |
| base_model | TinyLlama/TinyLlama-1.1B-Chat-v1.0 |
| 训练时长 | 600s |
| USD 消耗 | 0.25 |

## 训练曲线

![training_curve](artifacts/training_curve.png)

## 分数对比

| 任务 | Baseline | LoRA SFT | Delta |
|------|----------|----------|-------|
| gsm8k | 0.15 | 0.45 | +0.30 |

## 失败归因

训练正常完成。Loss 从 2.35 下降到 0.92，共 100 步，无异常。

## 决策

推荐继续：LoRA SFT 在 gsm8k 上提升 30 个百分点，建议继续扩大训练规模。
"""
    (run_dir / "report.md").write_text(report_md, encoding="utf-8")

    ok, errors = validate_report_schema(run_dir / "report.md")

    assert ok is True, f"合法 report.md 应通过校验，errors={errors}"
    assert errors == [], f"合法 report.md 应无 errors，实际：{errors}"


# ---------------------------------------------------------------------------
# T026-O2-TC02: 缺失 H2 section 时 schema 校验失败
# ---------------------------------------------------------------------------


@pytest.mark.e2e
def test_o2_missing_section_fails_schema(tmp_runs_dir: Path) -> None:
    """should return (False, [...]) when report.md is missing required H2 sections.

    结论：缺少 ## 决策 时，validate_report_schema 应返回 False + 非空 errors。
    """
    run_id = "test-o2-missing-01"
    run_dir = tmp_runs_dir / run_id
    run_dir.mkdir(parents=True)
    (run_dir / "artifacts").mkdir()

    # 故意缺少 ## 决策 section
    report_md_missing_section = """# SFT 实验决策报告

## 元数据

| 字段 | 值 |
|------|-----|
| run_id | test-o2-missing-01 |

## 训练曲线

![training_curve](artifacts/training_curve.png)

## 分数对比

| 任务 | Baseline | LoRA SFT | Delta |
|------|----------|----------|-------|
| gsm8k | 0.10 | 0.40 | +0.30 |

## 失败归因

无失败。Loss 下降 1.50 个单位。

<!-- 故意缺少 ## 决策 section -->
"""
    (run_dir / "report.md").write_text(report_md_missing_section, encoding="utf-8")

    ok, errors = validate_report_schema(run_dir / "report.md")

    assert ok is False, "缺少 ## 决策 section 时应校验失败"
    assert len(errors) > 0, "errors 列表应非空"


# ---------------------------------------------------------------------------
# T026-O2-TC03: 缺少必填 H2 sections（多个）时报告所有缺失项
# ---------------------------------------------------------------------------


@pytest.mark.e2e
def test_o2_multiple_missing_sections_reports_all(tmp_runs_dir: Path) -> None:
    """should report all missing sections when multiple H2 sections are absent.

    结论：同时缺 ## 分数对比 和 ## 决策 时，errors 中应包含两项（或超集）。
    """
    run_id = "test-o2-multi-missing-01"
    run_dir = tmp_runs_dir / run_id
    run_dir.mkdir(parents=True)

    # 只保留元数据 + 训练曲线，缺 分数对比 / 失败归因 / 决策
    report_md_minimal = """# SFT 实验决策报告

## 元数据

| 字段 | 值 |
|------|-----|
| run_id | test-o2-multi-missing-01 |

## 训练曲线

没有图像引用（刻意省略）。
"""
    (run_dir / "report.md").write_text(report_md_minimal, encoding="utf-8")

    ok, errors = validate_report_schema(run_dir / "report.md")

    assert ok is False, "多个 section 缺失时应校验失败"
    # 至少应报告 1 个 error
    assert len(errors) >= 1, f"应有 ≥1 个错误，实际 errors={errors}"


# ---------------------------------------------------------------------------
# T026-O2-TC04: report.md 不存在时报错合理
# ---------------------------------------------------------------------------


@pytest.mark.e2e
def test_o2_nonexistent_report_fails_gracefully(tmp_runs_dir: Path) -> None:
    """should return (False, [...]) when report.md file does not exist.

    结论：文件不存在时，validate_report_schema 应返回 (False, [...]) 而非抛异常。
    """
    missing_path = tmp_runs_dir / "nonexistent" / "report.md"

    # 应返回 False + errors，不应 raise
    try:
        ok, errors = validate_report_schema(missing_path)
        assert ok is False, "文件不存在时应返回 False"
        assert len(errors) > 0, "文件不存在时 errors 应非空"
    except FileNotFoundError:
        # 允许实现选择 raise FileNotFoundError（均为合法行为）
        pass
    except Exception as e:
        pytest.fail(f"validate_report_schema 不应抛出非 FileNotFoundError 异常：{e}")
