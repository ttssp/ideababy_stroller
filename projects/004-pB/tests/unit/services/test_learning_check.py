"""
LearningCheckService 单元测试 — T019 (R3 简化版)
结论: 覆盖抽题 / yaml 解析 / 评分计算 / R3 cut 验证（service 路径无 LLM 调用）
细节:
  - test_start_quarter_samples_7_from_checklist: start_quarter 从 yaml 抽 7 题
  - test_start_quarter_raises_when_yaml_missing: yaml 不存在时 raise FileNotFoundError
  - test_start_quarter_raises_when_too_few_concepts: yaml 少于 7 条时 raise ValueError
  - test_start_quarter_questions_are_unique: 抽出的 7 题 id 不重复
  - test_save_answers_stores_answers: save_answers 将答案写入 repo
  - test_get_quarter_returns_existing: get_quarter 返回已存在的季度
  - test_get_quarter_returns_none_for_missing: get_quarter 未找到时返回 None
  - test_compute_average_score_when_all_graded: 均分计算正确
  - test_is_passing_when_average_gte_7: 均分 >= 7 视为通过
  - test_is_passing_when_average_lt_7: 均分 < 7 视为不通过
  - test_service_has_no_llm_client_attribute: R3 cut — service 无 llm_client 属性
  - test_r3_no_llm_call_in_start_quarter: AST 验证 service 文件无 LLMClient.call 调用
"""

from __future__ import annotations

import ast
import sys
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock, MagicMock

import pytest
import yaml

# ── 测试辅助 ──────────────────────────────────────────────────────────────────

PROJECT_ROOT = Path(__file__).resolve().parents[3]
SERVICE_FILE = PROJECT_ROOT / "src" / "decision_ledger" / "services" / "learning_check_service.py"
CHECKLIST_FILE = PROJECT_ROOT / "docs" / "learning_checklist.yaml"


def _make_service(repo: Any = None, checklist_path: Path | None = None) -> Any:
    """延迟导入 LearningCheckService 并构造实例。"""
    if "decision_ledger.services.learning_check_service" in sys.modules:
        del sys.modules["decision_ledger.services.learning_check_service"]

    from decision_ledger.services.learning_check_service import LearningCheckService

    if repo is None:
        repo = MagicMock()
        repo.insert_quarter = AsyncMock()
        repo.get_quarter = AsyncMock(return_value=None)
        repo.update_answers = AsyncMock()
        repo.update_scores = AsyncMock()

    path = checklist_path or CHECKLIST_FILE
    return LearningCheckService(repo=repo, checklist_path=path)


def _make_mock_repo() -> MagicMock:
    """构造 mock LearningQuarterRepository。"""
    repo = MagicMock()
    repo.insert_quarter = AsyncMock()
    repo.get_quarter = AsyncMock(return_value=None)
    repo.update_answers = AsyncMock()
    repo.update_scores = AsyncMock()
    return repo


# ── 测试: yaml 解析 + 抽题 ───────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_start_quarter_samples_7_from_checklist(tmp_path: Path) -> None:
    """should sample exactly 7 concepts when yaml has 10 entries."""
    # 准备 10 条 yaml
    data = {
        "concepts": [
            {"id": f"c{i}", "concept": f"概念 {i}", "standard_answer": f"答案 {i}"}
            for i in range(10)
        ]
    }
    yaml_path = tmp_path / "checklist.yaml"
    yaml_path.write_text(yaml.dump(data, allow_unicode=True))

    repo = _make_mock_repo()
    svc = _make_service(repo=repo, checklist_path=yaml_path)

    questions = await svc.start_quarter("2026-Q2")

    assert len(questions) == 7


@pytest.mark.asyncio
async def test_start_quarter_raises_when_yaml_missing() -> None:
    """should raise FileNotFoundError when yaml does not exist."""
    missing_path = Path("/tmp/nonexistent_learning_checklist_xyz.yaml")
    repo = _make_mock_repo()
    svc = _make_service(repo=repo, checklist_path=missing_path)

    with pytest.raises(FileNotFoundError):
        await svc.start_quarter("2026-Q2")


@pytest.mark.asyncio
async def test_start_quarter_raises_when_too_few_concepts(tmp_path: Path) -> None:
    """should raise ValueError when yaml has fewer than 7 concepts."""
    data = {
        "concepts": [
            {"id": f"c{i}", "concept": f"概念 {i}", "standard_answer": f"答案 {i}"}
            for i in range(5)  # 只有 5 条，不够 7
        ]
    }
    yaml_path = tmp_path / "checklist.yaml"
    yaml_path.write_text(yaml.dump(data, allow_unicode=True))

    repo = _make_mock_repo()
    svc = _make_service(repo=repo, checklist_path=yaml_path)

    with pytest.raises(ValueError, match="至少需要 7 个概念"):
        await svc.start_quarter("2026-Q2")


@pytest.mark.asyncio
async def test_start_quarter_questions_are_unique(tmp_path: Path) -> None:
    """should return 7 unique concept ids when sampling."""
    data = {
        "concepts": [
            {"id": f"c{i}", "concept": f"概念 {i}", "standard_answer": f"答案 {i}"}
            for i in range(10)
        ]
    }
    yaml_path = tmp_path / "checklist.yaml"
    yaml_path.write_text(yaml.dump(data, allow_unicode=True))

    repo = _make_mock_repo()
    svc = _make_service(repo=repo, checklist_path=yaml_path)

    questions = await svc.start_quarter("2026-Q2")

    ids = [q["id"] for q in questions]
    assert len(ids) == len(set(ids)), "抽取的题目 ID 不唯一"


@pytest.mark.asyncio
async def test_start_quarter_inserts_to_repo(tmp_path: Path) -> None:
    """should call repo.insert_quarter once when starting a new quarter."""
    data = {
        "concepts": [
            {"id": f"c{i}", "concept": f"概念 {i}", "standard_answer": f"答案 {i}"}
            for i in range(10)
        ]
    }
    yaml_path = tmp_path / "checklist.yaml"
    yaml_path.write_text(yaml.dump(data, allow_unicode=True))

    repo = _make_mock_repo()
    svc = _make_service(repo=repo, checklist_path=yaml_path)

    await svc.start_quarter("2026-Q2")

    repo.insert_quarter.assert_awaited_once()


# ── 测试: 答案管理 ──────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_save_answers_calls_repo_update() -> None:
    """should call repo.update_answers when saving answers."""
    repo = _make_mock_repo()
    svc = _make_service(repo=repo)

    answers = {"calibration": "我的答案", "c1": "另一个答案"}
    await svc.save_answers("2026-Q2", answers)

    repo.update_answers.assert_awaited_once_with("2026-Q2", answers)


@pytest.mark.asyncio
async def test_get_quarter_returns_none_for_missing() -> None:
    """should return None when quarter does not exist."""
    repo = _make_mock_repo()
    repo.get_quarter = AsyncMock(return_value=None)
    svc = _make_service(repo=repo)

    result = await svc.get_quarter("2099-Q4")

    assert result is None


@pytest.mark.asyncio
async def test_get_quarter_returns_existing() -> None:
    """should return quarter data when it exists."""
    quarter_data = {
        "quarter_id": "2026-Q2",
        "generated_at": "2026-04-01T00:00:00Z",
        "questions_json": "[]",
        "answers_json": "{}",
        "scores_json": "{}",
        "finalized": 0,
    }
    repo = _make_mock_repo()
    repo.get_quarter = AsyncMock(return_value=quarter_data)
    svc = _make_service(repo=repo)

    result = await svc.get_quarter("2026-Q2")

    assert result is not None
    assert result["quarter_id"] == "2026-Q2"


# ── 测试: 评分计算 ───────────────────────────────────────────────────────────


def test_compute_average_score_when_all_graded() -> None:
    """should compute correct average when all 7 concepts are graded."""
    svc = _make_service()
    scores = {"c0": 8, "c1": 9, "c2": 7, "c3": 6, "c4": 8, "c5": 7, "c6": 9}
    avg = svc.compute_average_score(scores)
    # (8+9+7+6+8+7+9) / 7 = 54/7 ≈ 7.71
    assert abs(avg - 54 / 7) < 0.01


def test_compute_average_score_when_empty() -> None:
    """should return 0.0 when scores dict is empty."""
    svc = _make_service()
    assert svc.compute_average_score({}) == 0.0


def test_is_passing_when_average_gte_7() -> None:
    """should return True when average score >= 7.0."""
    svc = _make_service()
    # 均分恰好 7.0
    assert svc.is_passing(7.0) is True
    assert svc.is_passing(8.5) is True
    assert svc.is_passing(10.0) is True


def test_is_passing_when_average_lt_7() -> None:
    """should return False when average score < 7.0."""
    svc = _make_service()
    assert svc.is_passing(6.9) is False
    assert svc.is_passing(0.0) is False


# ── R3 cut 验证: service 路径无 LLM 调用 ─────────────────────────────────────


def test_service_has_no_llm_client_attribute() -> None:
    """should not have llm_client attribute (R3 cut — service 路径不调 LLM)."""
    svc = _make_service()
    assert not hasattr(svc, "_llm_client"), "R3 违规: service 含 _llm_client 属性"
    assert not hasattr(svc, "llm_client"), "R3 违规: service 含 llm_client 属性"


def test_r3_no_llm_call_in_service_ast() -> None:
    """should have no LLMClient.call() in service file (AST static check, R3 cut)."""
    assert SERVICE_FILE.exists(), f"service 文件不存在: {SERVICE_FILE}"

    source = SERVICE_FILE.read_text()
    tree = ast.parse(source)

    violations: list[str] = []
    for node in ast.walk(tree):
        # 检测 xxx.call(...) 模式
        if isinstance(node, ast.Call):
            func = node.func
            if isinstance(func, ast.Attribute) and func.attr == "call":
                # 检查是否调用了 llm_client 或 LLMClient 的 call
                if isinstance(func.value, ast.Attribute):
                    if "llm" in func.value.attr.lower():
                        violations.append(
                            f"line {node.lineno}: {ast.unparse(node)[:80]}"
                        )
                elif isinstance(func.value, ast.Name):
                    if "llm" in func.value.id.lower():
                        violations.append(
                            f"line {node.lineno}: {ast.unparse(node)[:80]}"
                        )

    assert not violations, (
        f"R3 违规: LearningCheckService 路径含 LLM call:\n"
        + "\n".join(violations)
    )


def test_r3_checklist_yaml_exists_and_parseable() -> None:
    """should have docs/learning_checklist.yaml that is valid yaml with concepts list."""
    assert CHECKLIST_FILE.exists(), f"checklist yaml 不存在: {CHECKLIST_FILE}"

    with CHECKLIST_FILE.open() as f:
        data = yaml.safe_load(f)

    assert isinstance(data, dict), "yaml 根节点应为 dict"
    assert "concepts" in data, "yaml 应含 'concepts' key"
    assert isinstance(data["concepts"], list), "concepts 应为 list"
    assert len(data["concepts"]) >= 7, f"concepts 至少需要 7 条，实际: {len(data['concepts'])}"

    for item in data["concepts"]:
        assert "id" in item, f"每个 concept 需要 id 字段: {item}"
        assert "concept" in item, f"每个 concept 需要 concept 字段: {item}"
        assert "standard_answer" in item, f"每个 concept 需要 standard_answer 字段: {item}"
