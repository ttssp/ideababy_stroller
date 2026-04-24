"""
tests/unit/test_report_schema_validator.py — report schema 校验器的单元测试。

覆盖(≥10 个用例):
1.  happy path:完整 report.md + 所有必要文件 → validate_report_schema 返回 (True, [])
2.  缺 ## 元数据 section → (False, errors 含 "missing" 信息)
3.  缺 ## 训练曲线 section → (False, errors 含 "missing training curve section" 类信息)
4.  缺 ## 分数对比 section → (False, errors 含 "score" 信息)
5.  缺 ## 失败归因 section → (False, errors 含 "失败归因" 信息)
6.  缺 ## 决策 section → (False, errors 含 "decision" 信息)
7.  训练曲线 PNG 引用的文件不存在 → (False, errors 含 PNG 路径信息)
8.  分数对比 section 缺 markdown table → (False, errors 含 "table" 信息)
9.  决策 section 缺关键词 [继续|停止|改方向] → (False, errors 含 "decision keyword" 信息)
10. 完整 report.md 路径不存在 → (False, errors 含路径信息)
11. validate_report_artifacts: scores.json 无 baseline key → errors 非空
12. validate_report_artifacts: metrics.jsonl 为空 → errors 非空
13. validate_report_artifacts: state=failed 且无 FA → errors 非空
14. validate_report_artifacts: happy path 有 scores + metrics + FA → 返回空列表
15. validate_report_artifacts: 有 scores.json 但缺 FA (state=completed) → 不报错
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from pars.report.schema_validator import validate_report_artifacts, validate_report_schema


# ---------------------------------------------------------------------------
# 辅助函数：构造合法 report.md 内容
# ---------------------------------------------------------------------------

_VALID_REPORT = """\
# Run 01JTEST00000000000000000000 · 测试实验

## 元数据
- 研究问题: 测试 LoRA 是否提升 gsm8k
- baseline: Qwen3-4B accuracy=0.45
- LoRA 配置: rank=8, alpha=16, lr=2e-4, epochs=3
- 数据集: gsm8k-100 train/test
- wall_clock: 02:30:00
- API USD: $0.50
- GPU hours: 2.5

## 训练曲线
![training curve](artifacts/training_curve.png)

| epoch | train_loss | eval_loss |
|---|---|---|
| 1 | 1.23 | 1.45 |
| 2 | 0.98 | 1.12 |
| 3 | 0.75 | 0.89 |

## 分数对比
| 模型 | held-out metric | delta vs baseline |
|---|---|---|
| baseline (frozen) | 0.45 | — |
| LoRA epoch 1 | 0.47 | +0.02 |
| LoRA final | 0.51 | +0.06 |

## 失败归因(必填,即使成功也写"无明显失败")
见 failure_attribution.md

- 假设: 预期 LoRA 会提升性能
- 观察: LoRA final accuracy=0.51, 高于 baseline 0.45
- 归因: 基本符合预期
- 下一步建议: 继续当前配置

## 决策
**继续**: 测试 metric accuracy=0.51 相较基线 0.45 提升 0.06, 建议继续增加 epoch 进一步验证。
"""


def _write_report(tmp_path: Path, content: str = _VALID_REPORT) -> Path:
    """写 report.md 到 tmp_path, 返回文件路径。"""
    report_path = tmp_path / "report.md"
    report_path.write_text(content, encoding="utf-8")
    return report_path


def _write_png(tmp_path: Path) -> Path:
    """写一个假的 PNG 文件(有效 magic bytes)到 artifacts/。"""
    artifacts = tmp_path / "artifacts"
    artifacts.mkdir(exist_ok=True)
    png_path = artifacts / "training_curve.png"
    # PNG magic bytes: 8 bytes header
    png_path.write_bytes(b"\x89PNG\r\n\x1a\n" + b"\x00" * 100)
    return png_path


# ---------------------------------------------------------------------------
# 测试组 1: validate_report_schema
# ---------------------------------------------------------------------------


class TestValidateReportSchema:
    """validate_report_schema(report_path) -> tuple[bool, list[str]] 的测试。"""

    def test_happy_path_returns_true_with_empty_errors(self, tmp_path: Path) -> None:
        """正常情况: 完整 report.md + PNG 存在 → (True, [])。"""
        _write_png(tmp_path)
        report_path = _write_report(tmp_path)
        ok, errors = validate_report_schema(report_path)
        assert ok is True
        assert errors == []

    def test_missing_metadata_section(self, tmp_path: Path) -> None:
        """缺 ## 元数据 → 返回 False + 错误描述。"""
        _write_png(tmp_path)
        content = _VALID_REPORT.replace("## 元数据\n", "## REPLACED_META\n")
        report_path = _write_report(tmp_path, content)
        ok, errors = validate_report_schema(report_path)
        assert ok is False
        assert any("元数据" in e for e in errors)

    def test_missing_training_curve_section(self, tmp_path: Path) -> None:
        """缺 ## 训练曲线 → (False, errors 含 training curve 信息)。"""
        _write_png(tmp_path)
        content = _VALID_REPORT.replace("## 训练曲线\n", "## REPLACED_CURVE\n")
        report_path = _write_report(tmp_path, content)
        ok, errors = validate_report_schema(report_path)
        assert ok is False
        assert any("训练曲线" in e or "training curve" in e.lower() for e in errors)

    def test_missing_score_comparison_section(self, tmp_path: Path) -> None:
        """缺 ## 分数对比 → (False, errors 含分数对比相关信息)。"""
        _write_png(tmp_path)
        content = _VALID_REPORT.replace("## 分数对比\n", "## REPLACED_SCORE\n")
        report_path = _write_report(tmp_path, content)
        ok, errors = validate_report_schema(report_path)
        assert ok is False
        assert any("分数对比" in e or "score" in e.lower() for e in errors)

    def test_missing_failure_attribution_section(self, tmp_path: Path) -> None:
        """缺 ## 失败归因 → (False, errors 含失败归因信息)。"""
        _write_png(tmp_path)
        content = _VALID_REPORT.replace(
            "## 失败归因(必填,即使成功也写\"无明显失败\")\n",
            "## REPLACED_FA\n",
        )
        report_path = _write_report(tmp_path, content)
        ok, errors = validate_report_schema(report_path)
        assert ok is False
        assert any("失败归因" in e for e in errors)

    def test_missing_decision_section(self, tmp_path: Path) -> None:
        """缺 ## 决策 → (False, errors 含 decision/决策 信息)。"""
        _write_png(tmp_path)
        content = _VALID_REPORT.replace("## 决策\n", "## REPLACED_DECISION\n")
        report_path = _write_report(tmp_path, content)
        ok, errors = validate_report_schema(report_path)
        assert ok is False
        assert any("决策" in e or "decision" in e.lower() for e in errors)

    def test_missing_png_file_referenced_in_report(self, tmp_path: Path) -> None:
        """报告引用的 PNG 文件不存在 → (False, errors 含路径信息)。"""
        # 不写 PNG 文件
        report_path = _write_report(tmp_path)
        ok, errors = validate_report_schema(report_path)
        assert ok is False
        assert any("png" in e.lower() or "training_curve" in e for e in errors)

    def test_score_comparison_section_missing_table(self, tmp_path: Path) -> None:
        """分数对比 section 存在但没有 markdown table → (False, errors 含 table 信息)。"""
        _write_png(tmp_path)
        content = _VALID_REPORT.replace(
            "| 模型 | held-out metric | delta vs baseline |\n|---|---|---|\n| baseline (frozen) | 0.45 | — |\n| LoRA epoch 1 | 0.47 | +0.02 |\n| LoRA final | 0.51 | +0.06 |",
            "无表格内容，仅有文字说明。",
        )
        report_path = _write_report(tmp_path, content)
        ok, errors = validate_report_schema(report_path)
        assert ok is False
        assert any("table" in e.lower() or "表格" in e for e in errors)

    def test_decision_section_missing_keyword(self, tmp_path: Path) -> None:
        """决策 section 不含 [继续|停止|改方向] 关键词 → (False, errors 含 keyword 信息)。"""
        _write_png(tmp_path)
        content = _VALID_REPORT.replace(
            "**继续**: 测试 metric accuracy=0.51 相较基线 0.45 提升 0.06, 建议继续增加 epoch 进一步验证。",
            "实验结果不错，参数配置合理。",
        )
        report_path = _write_report(tmp_path, content)
        ok, errors = validate_report_schema(report_path)
        assert ok is False
        assert any("继续" in e or "停止" in e or "改方向" in e or "keyword" in e.lower() or "关键词" in e for e in errors)

    def test_report_file_not_exists(self, tmp_path: Path) -> None:
        """report.md 不存在 → (False, errors 含路径信息)。"""
        nonexistent = tmp_path / "nonexistent_report.md"
        ok, errors = validate_report_schema(nonexistent)
        assert ok is False
        assert len(errors) >= 1
        assert any("exist" in e.lower() or "not found" in e.lower() or "找不到" in e or "不存在" in e for e in errors)


# ---------------------------------------------------------------------------
# 测试组 2: validate_report_artifacts
# ---------------------------------------------------------------------------


class TestValidateReportArtifacts:
    """validate_report_artifacts(run_dir) -> list[str] 的测试。"""

    def _make_valid_run_dir(self, tmp_path: Path, state: str = "completed") -> Path:
        """构造一个合法的 run_dir 结构。"""
        run_dir = tmp_path / "run_01JTEST"

        # 创建 artifacts/ 子目录
        artifacts = run_dir / "artifacts"
        artifacts.mkdir(parents=True, exist_ok=True)

        # 写 scores.json (含 baseline key)
        scores = {
            "baseline": {"accuracy": 0.45},
            "lora_final": {"accuracy": 0.51},
        }
        (artifacts / "scores.json").write_text(json.dumps(scores), encoding="utf-8")

        # 写 metrics.jsonl (至少一行)
        metrics_line = json.dumps({
            "ts": "2026-04-24T00:00:00+00:00",
            "phase": "training",
            "kind": "epoch",
            "data": {"epoch": 1, "train_loss": 1.23},
        })
        (run_dir / "metrics.jsonl").write_text(metrics_line + "\n", encoding="utf-8")

        # 写 state.json
        state_data = {"phase": state, "usd_spent": 0.5}
        (run_dir / "state.json").write_text(json.dumps(state_data), encoding="utf-8")

        # 写 failure_attribution.md (合法格式)
        fa_content = """\
# Failure attribution · 01JTEST

## 必填字段
- **假设**: 预计 LoRA 微调后 gsm8k 准确率从基线 0.45 提升至 0.55 以上
- **观察**: LoRA final epoch accuracy=0.51，高于 baseline 0.45，loss 曲线平稳
- **归因**:
  - [x] 基线本身已够强
- **下一步建议**: 尝试增加 epoch=5 或 rank=16 进一步提升

## 自由叙述(可选,但鼓励)
整体训练过程正常，结果符合预期。
"""
        (run_dir / "failure_attribution.md").write_text(fa_content, encoding="utf-8")

        return run_dir

    def test_happy_path_returns_empty_list(self, tmp_path: Path) -> None:
        """完整 run_dir (baseline score + lora score + metrics + FA) → 返回 []。"""
        run_dir = self._make_valid_run_dir(tmp_path)
        errors = validate_report_artifacts(run_dir)
        assert errors == []

    def test_scores_json_missing_baseline_key(self, tmp_path: Path) -> None:
        """scores.json 无 baseline key → errors 非空。"""
        run_dir = self._make_valid_run_dir(tmp_path)
        # 覆写 scores.json 删掉 baseline key
        bad_scores = {"lora_final": {"accuracy": 0.51}}
        (run_dir / "artifacts" / "scores.json").write_text(
            json.dumps(bad_scores), encoding="utf-8"
        )
        errors = validate_report_artifacts(run_dir)
        assert len(errors) >= 1
        assert any("baseline" in e.lower() for e in errors)

    def test_metrics_jsonl_empty(self, tmp_path: Path) -> None:
        """metrics.jsonl 为空 → errors 非空。"""
        run_dir = self._make_valid_run_dir(tmp_path)
        (run_dir / "metrics.jsonl").write_text("", encoding="utf-8")
        errors = validate_report_artifacts(run_dir)
        assert len(errors) >= 1
        assert any("metrics" in e.lower() or "empty" in e.lower() or "空" in e for e in errors)

    def test_state_failed_without_failure_attribution(self, tmp_path: Path) -> None:
        """state=failed 且无 failure_attribution.md → errors 非空。"""
        run_dir = self._make_valid_run_dir(tmp_path, state="failed")
        # 删除 failure_attribution.md
        (run_dir / "failure_attribution.md").unlink()
        errors = validate_report_artifacts(run_dir)
        assert len(errors) >= 1
        assert any("failure_attribution" in e.lower() or "失败归因" in e for e in errors)

    def test_scores_json_not_exists(self, tmp_path: Path) -> None:
        """scores.json 不存在 → errors 非空。"""
        run_dir = self._make_valid_run_dir(tmp_path)
        (run_dir / "artifacts" / "scores.json").unlink()
        errors = validate_report_artifacts(run_dir)
        assert len(errors) >= 1
        assert any("scores" in e.lower() for e in errors)

    def test_state_completed_without_failure_attribution_is_ok(self, tmp_path: Path) -> None:
        """state=completed 且无 FA → 不报错(FA 非必需,除非 state=failed)。"""
        run_dir = self._make_valid_run_dir(tmp_path, state="completed")
        # 删除 failure_attribution.md
        (run_dir / "failure_attribution.md").unlink()
        errors = validate_report_artifacts(run_dir)
        # 没有 FA 相关错误
        fa_errors = [e for e in errors if "failure_attribution" in e.lower() or "失败归因" in e]
        assert fa_errors == []

    def test_failure_attribution_fails_validate_quality(self, tmp_path: Path) -> None:
        """FA 存在但 validate_quality 失败 (observation 无数字) → errors 非空。"""
        run_dir = self._make_valid_run_dir(tmp_path, state="failed")
        # 覆写一个 observation 无数字的 FA
        bad_fa = """\
# Failure attribution · 01JTEST

## 必填字段
- **假设**: 预计 LoRA 微调后 gsm8k 准确率能得到显著改善，超过基线测试指标
- **观察**: 训练完成后模型性能表现低于预期，评测分数不够理想
- **归因**:
  - [x] 学习率太大
- **下一步建议**: 尝试降低 lr=1e-5 重新训练

## 自由叙述(可选,但鼓励)
结果不理想。
"""
        (run_dir / "failure_attribution.md").write_text(bad_fa, encoding="utf-8")
        errors = validate_report_artifacts(run_dir)
        assert len(errors) >= 1
        assert any("observation" in e.lower() or "数字" in e or "quality" in e.lower() for e in errors)
