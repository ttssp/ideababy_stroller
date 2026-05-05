"""
grade_learning 集成测试 — T019 (R3 简化版)
结论: end-to-end 模拟跑通 LearningCheckService + mock LLM 评分
细节:
  - test_start_quarter_creates_db_record: start_quarter 后 DB 有记录
  - test_save_answers_updates_db: save_answers 正确更新 DB
  - test_grade_learning_script_mock_mode: grade_learning.py 脚本 mock 模式输出总分 >= 7/10
  - test_full_flow_start_answer_score: 完整流程 start → answer → score
  - test_learning_check_script_triggers_start: learning_check.py 脚本正确触发抽题
  - test_r3_no_llm_in_service_path: service 路径（非 grade 脚本）不触发 LLM
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from collections.abc import AsyncIterator
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
import pytest_asyncio
import yaml

from decision_ledger.repository.base import AsyncConnectionPool

PROJECT_ROOT = Path(__file__).resolve().parents[3]
CHECKLIST_FILE = PROJECT_ROOT / "docs" / "learning_checklist.yaml"


# ── Fixtures ─────────────────────────────────────────────────────────────────


@pytest_asyncio.fixture
async def migrated_pool(tmp_path: Path) -> AsyncIterator[AsyncConnectionPool]:
    """提供经过 alembic upgrade head 迁移的 AsyncConnectionPool。"""
    db_path = tmp_path / "test_learning.sqlite"
    db_url = f"sqlite:///{db_path}"

    env = {
        **os.environ,
        "DECISION_LEDGER_DB_URL": db_url,
        "ANTHROPIC_API_KEY": os.environ.get("ANTHROPIC_API_KEY", "test-key-placeholder"),
        "TELEGRAM_BOT_TOKEN": os.environ.get("TELEGRAM_BOT_TOKEN", "test-token-placeholder"),
    }
    result = subprocess.run(  # noqa: S603
        [sys.executable, "-m", "alembic", "upgrade", "heads"],
        cwd=str(PROJECT_ROOT),
        env=env,
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, f"alembic upgrade 失败:\nstdout: {result.stdout}\nstderr: {result.stderr}"

    pool = AsyncConnectionPool(str(db_path))
    await pool.initialize()
    try:
        yield pool
    finally:
        await pool.close()


@pytest_asyncio.fixture
async def learning_repo(migrated_pool: AsyncConnectionPool) -> Any:
    """提供 LearningQuarterRepository 实例（注入 migrated pool）。"""
    from decision_ledger.repository.learning_quarter_repository import LearningQuarterRepository

    return LearningQuarterRepository(pool=migrated_pool)


@pytest_asyncio.fixture
async def learning_svc(learning_repo: Any) -> Any:
    """提供 LearningCheckService 实例（注入真实 repo）。"""
    from decision_ledger.services.learning_check_service import LearningCheckService

    return LearningCheckService(repo=learning_repo, checklist_path=CHECKLIST_FILE)


# ── 集成测试: DB 操作 ─────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_start_quarter_creates_db_record(learning_svc: Any, migrated_pool: AsyncConnectionPool) -> None:
    """should create a record in learning_quarters table when start_quarter is called."""
    quarter_id = "2026-Q2"
    questions = await learning_svc.start_quarter(quarter_id)

    # 验证返回 7 题
    assert len(questions) == 7

    # 验证 DB 有记录
    async with migrated_pool.connection() as conn:
        cursor = await conn.execute(
            "SELECT * FROM learning_quarters WHERE quarter_id = ?", (quarter_id,)
        )
        row = await cursor.fetchone()

    assert row is not None, "DB 中无 learning_quarters 记录"
    assert row["quarter_id"] == quarter_id
    assert row["finalized"] == 0

    # 验证 questions_json 正确存储了 7 题
    stored_questions = json.loads(row["questions_json"])
    assert len(stored_questions) == 7


@pytest.mark.asyncio
async def test_save_answers_updates_db(learning_svc: Any, migrated_pool: AsyncConnectionPool) -> None:
    """should update answers_json in DB when save_answers is called."""
    quarter_id = "2026-Q2"
    await learning_svc.start_quarter(quarter_id)

    answers = {"calibration": "校准是预测置信度与准确率的一致性", "c1": "测试答案"}
    await learning_svc.save_answers(quarter_id, answers)

    # 验证 DB 更新
    async with migrated_pool.connection() as conn:
        cursor = await conn.execute(
            "SELECT answers_json FROM learning_quarters WHERE quarter_id = ?",
            (quarter_id,),
        )
        row = await cursor.fetchone()

    assert row is not None
    stored_answers = json.loads(row["answers_json"])
    assert stored_answers["calibration"] == "校准是预测置信度与准确率的一致性"


@pytest.mark.asyncio
async def test_full_flow_start_answer_score(
    learning_svc: Any,
    migrated_pool: AsyncConnectionPool,
) -> None:
    """should complete full flow: start_quarter → save_answers → save_scores."""
    quarter_id = "2026-Q2-full"
    questions = await learning_svc.start_quarter(quarter_id)

    # 为每题构造答案
    answers = {q["id"]: f"我的答案关于 {q['concept'][:10]}" for q in questions}
    await learning_svc.save_answers(quarter_id, answers)

    # 模拟 LLM 评分 (高分通过场景)
    scores = {q["id"]: 8 for q in questions}
    avg = await learning_svc.save_scores(quarter_id, scores, finalized=True)

    # 均分 8.0 >= 7.0 应通过
    assert learning_svc.is_passing(avg) is True
    assert abs(avg - 8.0) < 0.01

    # 验证 DB finalized=1
    async with migrated_pool.connection() as conn:
        cursor = await conn.execute(
            "SELECT finalized, scores_json FROM learning_quarters WHERE quarter_id = ?",
            (quarter_id,),
        )
        row = await cursor.fetchone()

    assert row is not None
    assert row["finalized"] == 1
    stored_scores = json.loads(row["scores_json"])
    assert len(stored_scores) == 7


@pytest.mark.asyncio
async def test_get_quarter_after_start(learning_svc: Any) -> None:
    """should return quarter data when get_quarter called after start_quarter."""
    quarter_id = "2026-Q2-get"
    await learning_svc.start_quarter(quarter_id)

    result = await learning_svc.get_quarter(quarter_id)

    assert result is not None
    assert result["quarter_id"] == quarter_id


@pytest.mark.asyncio
async def test_get_quarter_returns_none_for_missing(learning_svc: Any) -> None:
    """should return None when quarter does not exist in DB."""
    result = await learning_svc.get_quarter("2099-Q9-nonexistent")
    assert result is None


# ── R3 验证: service 路径不调 LLM ────────────────────────────────────────────


@pytest.mark.asyncio
async def test_r3_no_llm_in_service_path(learning_svc: Any) -> None:
    """should not call any LLMClient during start_quarter and save_answers (R3 cut)."""
    quarter_id = "2026-Q2-r3check"

    # patch LLMClient.call 确认未调用
    with patch("decision_ledger.llm.client.LLMClient.call") as mock_call:
        await learning_svc.start_quarter(quarter_id)
        await learning_svc.save_answers(quarter_id, {"calibration": "test answer"})

    mock_call.assert_not_called()


# ── grade_learning 脚本 mock 模式验证 ────────────────────────────────────────


@pytest.mark.asyncio
async def test_grade_learning_script_mock_mode(
    learning_svc: Any,
    migrated_pool: AsyncConnectionPool,
    tmp_path: Path,
) -> None:
    """should output average score >= 7/10 when grade_learning.py runs in mock mode."""
    quarter_id = "2026-Q2-grade"
    questions = await learning_svc.start_quarter(quarter_id)

    # 为每题构造答案
    answers = {q["id"]: f"关于 {q['concept'][:10]}: 核心概念是" for q in questions}
    await learning_svc.save_answers(quarter_id, answers)

    # 直接测试 grade_learning 模块的核心函数 (不起子进程，避免环境依赖)
    # 用 mock LLM 评分: 所有题得 8 分
    mock_grade_result = MagicMock()
    mock_grade_result.score = 8
    mock_grade_result.brief_reason = "理解正确"

    mock_llm = MagicMock()
    mock_llm.call = AsyncMock(return_value=mock_grade_result)

    # 导入 grade_learning 模块并调用核心评分函数
    import importlib

    grade_module = importlib.import_module("scripts.grade_learning")

    avg = await grade_module.grade_quarter(
        quarter_id=quarter_id,
        svc=learning_svc,
        llm_client=mock_llm,
    )

    assert avg >= 7.0, f"均分 {avg} < 7.0，O4 verification 失败"


# ── learning_check 脚本触发抽题 ──────────────────────────────────────────────


@pytest.mark.asyncio
async def test_learning_check_script_triggers_start(
    learning_repo: Any,
    tmp_path: Path,
) -> None:
    """should create quarter record when learning_check script triggers start_quarter."""
    from decision_ledger.services.learning_check_service import LearningCheckService

    svc = LearningCheckService(repo=learning_repo, checklist_path=CHECKLIST_FILE)

    # 模拟 scripts/learning_check.py 的核心逻辑
    import importlib

    check_module = importlib.import_module("scripts.learning_check")

    quarter_id = "2026-Q2-script"
    questions = await check_module.run_start_quarter(
        quarter_id=quarter_id,
        svc=svc,
    )

    assert len(questions) == 7

    # 验证 DB 有记录
    result = await svc.get_quarter(quarter_id)
    assert result is not None
    assert result["quarter_id"] == quarter_id
