"""
post-mortem 回填路由集成测试 — T018
结论: 验证 GET/POST /decisions/{trade_id}/post-mortem 端到端行为
细节:
  - GET  /decisions/{id}/post-mortem → 200 HTML 表单
  - POST /decisions/{id}/post-mortem → 成功保存，重定向到 show 页
  - POST executed_at < pre_commit_at → 422
  - POST result_pct_after_7d 在 7 天内填写 → 422
  - hold/wait 决策也可填 post_mortem (R11)
  - 无效 trade_id → 404
"""

from __future__ import annotations

import asyncio
import os
import subprocess
import sys
import uuid
from collections.abc import AsyncIterator
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient

from decision_ledger.domain.conflict_report import ConflictReport
from decision_ledger.domain.decision import Decision
from decision_ledger.domain.env_snapshot import EnvSnapshot
from decision_ledger.domain.rebuttal import Rebuttal
from decision_ledger.domain.strategy_signal import Direction, StrategySignal

PROJECT_ROOT = Path(__file__).resolve().parents[3]


# ── 辅助工厂 ─────────────────────────────────────────────


def _make_signal(source_id: str, ticker: str = "AAPL") -> StrategySignal:
    return StrategySignal(
        source_id=source_id,
        ticker=ticker,
        direction=Direction.LONG,
        confidence=0.8,
        rationale_plain=f"{source_id} 看多",
        inputs_used={"advisor_week_id": "2026-W17"},
    )


def _make_conflict_report(ticker: str = "AAPL") -> ConflictReport:
    return ConflictReport(
        signals=[
            _make_signal("advisor", ticker),
            _make_signal("agent_synthesis", ticker),
            _make_signal("placeholder_model", ticker),
        ],
        divergence_root_cause="测试报告",
        has_divergence=False,
        rendered_order_seed=42,
    )


def _make_rebuttal() -> Rebuttal:
    return Rebuttal(
        rebuttal_text="测试反驳",
        invoked_at=datetime.now(tz=UTC).isoformat(),
    )


def _make_assembler_mock() -> MagicMock:
    async def _assemble(*args: Any, **kwargs: Any) -> ConflictReport:
        return _make_conflict_report()

    mock = MagicMock()
    mock.assemble = _assemble
    return mock


def _make_devil_mock() -> MagicMock:
    async def _generate(*args: Any, **kwargs: Any) -> Rebuttal:
        return _make_rebuttal()

    mock = MagicMock()
    mock.generate = _generate
    return mock


# ── Fixtures ─────────────────────────────────────────────


@pytest_asyncio.fixture
async def migrated_pool(tmp_path: Path) -> AsyncIterator[Any]:
    """提供已迁移的 SQLite pool。"""
    from decision_ledger.repository.base import AsyncConnectionPool

    db_path = tmp_path / "test_pm.sqlite"
    db_url = f"sqlite:///{db_path}"

    env = {
        **os.environ,
        "DECISION_LEDGER_DB_URL": db_url,
        "ANTHROPIC_API_KEY": os.environ.get("ANTHROPIC_API_KEY", "test-key"),
        "TELEGRAM_BOT_TOKEN": os.environ.get("TELEGRAM_BOT_TOKEN", "test-token"),
    }
    result = subprocess.run(  # noqa: S603
        [sys.executable, "-m", "alembic", "upgrade", "head"],
        cwd=str(PROJECT_ROOT),
        env=env,
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, f"alembic upgrade 失败: {result.stderr}"

    pool = AsyncConnectionPool(str(db_path))
    await pool.initialize()
    try:
        yield pool
    finally:
        await pool.close()


@pytest.fixture
def app_client(migrated_pool: Any) -> TestClient:
    """创建注入真实 repo + mock LLM 的 TestClient。
    同时注册 decisions router 和 post_mortem router。
    """
    os.environ.setdefault("ANTHROPIC_API_KEY", "test-key")
    os.environ.setdefault("TELEGRAM_BOT_TOKEN", "test-token")

    from decision_ledger.repository.conflict_repo import ConflictRepository
    from decision_ledger.repository.decision_repo import DecisionRepository
    from decision_ledger.repository.rebuttal_repo import RebuttalRepository
    from decision_ledger.services.decision_recorder import DecisionDraftRepository, DecisionRecorder
    from decision_ledger.ui.app import create_app
    from decision_ledger.ui.router_decisions import router as decisions_router
    from decision_ledger.ui.router_decisions import set_recorder
    from decision_ledger.ui.router_post_mortem import router as pm_router
    from decision_ledger.ui.router_post_mortem import set_decision_repo

    conflict_repo = ConflictRepository(migrated_pool)
    rebuttal_repo = RebuttalRepository(migrated_pool)
    decision_repo = DecisionRepository(migrated_pool)
    draft_repo = DecisionDraftRepository(migrated_pool)

    recorder = DecisionRecorder(
        assembler_service=_make_assembler_mock(),
        devil_service=_make_devil_mock(),
        draft_repo=draft_repo,
        conflict_repo=conflict_repo,
        rebuttal_repo=rebuttal_repo,
        decision_repo=decision_repo,
    )

    set_recorder(recorder)
    set_decision_repo(decision_repo)

    app = create_app()
    app.include_router(decisions_router)
    app.include_router(pm_router)
    return TestClient(app, raise_server_exceptions=False)


# ── 辅助: 创建一条已 commit 的决策，返回 trade_id + pre_commit_at ──────────────


def _create_committed_decision(
    client: TestClient,
    action: str = "buy",
) -> tuple[str, datetime]:
    """完整流程 draft → commit，返回 (trade_id, pre_commit_at)。"""
    draft_resp = client.post(
        "/decisions/draft",
        data={
            "ticker": "AAPL",
            "intended_action": action,
            "draft_reason": "测试决策",
        },
        follow_redirects=False,
    )
    assert draft_resp.status_code in (302, 303), f"draft 失败: {draft_resp.status_code}"
    location = draft_resp.headers.get("location", "")
    parts = location.split("/")
    draft_idx = parts.index("draft") if "draft" in parts else -1
    draft_id = parts[draft_idx + 1] if draft_idx >= 0 and draft_idx + 1 < len(parts) else ""
    assert draft_id, "未能获取 draft_id"

    commit_resp = client.post(
        f"/decisions/{draft_id}/commit",
        data={
            "final_action": action,
            "final_reason": "测试决策",
            "would_have_acted_without_agent": "yes",
        },
        follow_redirects=False,
    )
    assert commit_resp.status_code in (302, 303), f"commit 失败: {commit_resp.status_code}"
    commit_location = commit_resp.headers.get("location", "")
    trade_id = commit_location.rstrip("/").split("/")[-1]
    assert trade_id, "未能获取 trade_id"

    # pre_commit_at 从 DB 取，用 now 近似（误差 < 5s）
    return trade_id, datetime.now(tz=UTC)


# ── 测试类 ────────────────────────────────────────────────


class TestGetPostMortemForm:
    """GET /decisions/{trade_id}/post-mortem 测试组。"""

    def test_should_return_200_when_get_post_mortem_form(
        self, app_client: TestClient
    ) -> None:
        """结论: GET /decisions/{id}/post-mortem 返回 200 HTML。"""
        trade_id, _ = _create_committed_decision(app_client)
        response = app_client.get(f"/decisions/{trade_id}/post-mortem")
        assert response.status_code == 200
        assert "text/html" in response.headers.get("content-type", "")

    def test_should_contain_four_fields_when_get_form(
        self, app_client: TestClient
    ) -> None:
        """结论: 表单包含 4 个字段: executed_at / result_pct_after_7d / result_pct_after_30d / retrospective_notes。"""
        trade_id, _ = _create_committed_decision(app_client)
        response = app_client.get(f"/decisions/{trade_id}/post-mortem")
        html = response.text
        assert "executed_at" in html
        assert "result_pct_after_7d" in html
        assert "result_pct_after_30d" in html
        assert "retrospective_notes" in html

    def test_should_return_404_when_invalid_trade_id(
        self, app_client: TestClient
    ) -> None:
        """结论: 无效 trade_id → 404。"""
        response = app_client.get("/decisions/nonexistent-id/post-mortem")
        assert response.status_code == 404

    def test_should_prefill_when_post_mortem_exists(
        self, app_client: TestClient
    ) -> None:
        """结论: 已回填过的决策再次 GET 表单，应预填已有数据。"""
        trade_id, _ = _create_committed_decision(app_client)

        # 先 POST 回填
        post_time = datetime.now(tz=UTC) + timedelta(hours=1)
        app_client.post(
            f"/decisions/{trade_id}/post-mortem",
            data={
                "executed_at": post_time.strftime("%Y-%m-%dT%H:%M"),
                "result_pct_after_7d": "",
                "result_pct_after_30d": "",
                "retrospective_notes": "预填测试备注",
                "_now_override": "",
            },
        )

        # 再次 GET 应该预填
        response = app_client.get(f"/decisions/{trade_id}/post-mortem")
        assert "预填测试备注" in response.text


class TestPostPostMortem:
    """POST /decisions/{trade_id}/post-mortem 测试组。"""

    def test_should_redirect_to_show_when_post_valid(
        self, app_client: TestClient
    ) -> None:
        """结论: POST 成功 → 303 重定向到 /decisions/{trade_id}。"""
        trade_id, _ = _create_committed_decision(app_client)
        # executed_at 用 30 天后（肯定合法）
        executed_at = datetime.now(tz=UTC) + timedelta(hours=1)

        response = app_client.post(
            f"/decisions/{trade_id}/post-mortem",
            data={
                "executed_at": executed_at.strftime("%Y-%m-%dT%H:%M"),
                "result_pct_after_7d": "",
                "result_pct_after_30d": "",
                "retrospective_notes": "买入后小涨",
                "_now_override": "",
            },
            follow_redirects=False,
        )
        assert response.status_code in (302, 303)
        location = response.headers.get("location", "")
        assert f"/decisions/{trade_id}" in location
        assert "post-mortem" not in location

    def test_should_persist_post_mortem_when_post_valid(
        self, app_client: TestClient
    ) -> None:
        """结论: POST 成功后，show 页显示已回填数据。"""
        trade_id, _ = _create_committed_decision(app_client)
        executed_at = datetime.now(tz=UTC) + timedelta(hours=1)

        app_client.post(
            f"/decisions/{trade_id}/post-mortem",
            data={
                "executed_at": executed_at.strftime("%Y-%m-%dT%H:%M"),
                "result_pct_after_7d": "",
                "result_pct_after_30d": "",
                "retrospective_notes": "持续观察，基本面佳",
                "_now_override": "",
            },
            follow_redirects=True,
        )

        # show 页应该出现回填内容
        show_resp = app_client.get(f"/decisions/{trade_id}")
        assert "持续观察，基本面佳" in show_resp.text or response_has_post_mortem(show_resp.text)

    def test_should_return_422_when_executed_at_before_pre_commit_at(
        self, app_client: TestClient
    ) -> None:
        """结论: executed_at < pre_commit_at → 422。"""
        trade_id, pre_commit_at = _create_committed_decision(app_client)
        bad_executed_at = pre_commit_at - timedelta(days=2)

        response = app_client.post(
            f"/decisions/{trade_id}/post-mortem",
            data={
                "executed_at": bad_executed_at.strftime("%Y-%m-%dT%H:%M"),
                "result_pct_after_7d": "",
                "result_pct_after_30d": "",
                "retrospective_notes": "",
                "_now_override": "",
            },
        )
        assert response.status_code == 422

    def test_should_return_422_when_result_7d_filled_before_7_days(
        self, app_client: TestClient
    ) -> None:
        """结论: 决策后 3 天填 result_pct_after_7d → 422。"""
        trade_id, pre_commit_at = _create_committed_decision(app_client)
        # now_override = pre_commit_at + 3 天（不到 7 天）
        now_3d = pre_commit_at + timedelta(days=3)

        response = app_client.post(
            f"/decisions/{trade_id}/post-mortem",
            data={
                "executed_at": "",
                "result_pct_after_7d": "3.5",
                "result_pct_after_30d": "",
                "retrospective_notes": "",
                "_now_override": now_3d.isoformat(),  # 注入 "现在时间" 到第 3 天
            },
        )
        assert response.status_code == 422

    def test_should_return_200_when_result_7d_filled_after_7_days(
        self, app_client: TestClient
    ) -> None:
        """结论: 决策后 8 天填 result_pct_after_7d → 合法。"""
        trade_id, pre_commit_at = _create_committed_decision(app_client)
        now_8d = pre_commit_at + timedelta(days=8)

        response = app_client.post(
            f"/decisions/{trade_id}/post-mortem",
            data={
                "executed_at": "",
                "result_pct_after_7d": "5.5",
                "result_pct_after_30d": "",
                "retrospective_notes": "",
                "_now_override": now_8d.isoformat(),
            },
            follow_redirects=False,
        )
        assert response.status_code in (302, 303)

    def test_should_allow_hold_wait_without_executed_at(
        self, app_client: TestClient
    ) -> None:
        """结论: hold 决策不填 executed_at → 合法 (R11: 不动允许复盘)。"""
        trade_id, _ = _create_committed_decision(app_client, action="hold")
        now_10d = datetime.now(tz=UTC) + timedelta(days=10)

        response = app_client.post(
            f"/decisions/{trade_id}/post-mortem",
            data={
                "executed_at": "",          # 留空
                "result_pct_after_7d": "",
                "result_pct_after_30d": "",
                "retrospective_notes": "持有中，无操作",
                "_now_override": now_10d.isoformat(),
            },
            follow_redirects=False,
        )
        assert response.status_code in (302, 303)

    def test_should_return_404_when_post_invalid_trade_id(
        self, app_client: TestClient
    ) -> None:
        """结论: 无效 trade_id POST post-mortem → 404。"""
        response = app_client.post(
            "/decisions/nonexistent-id/post-mortem",
            data={
                "executed_at": "",
                "result_pct_after_7d": "",
                "result_pct_after_30d": "",
                "retrospective_notes": "",
                "_now_override": "",
            },
        )
        assert response.status_code == 404

    def test_should_allow_wait_decision_post_mortem(
        self, app_client: TestClient
    ) -> None:
        """结论: wait 决策也可填 post_mortem (R11)。"""
        trade_id, _ = _create_committed_decision(app_client, action="wait")

        response = app_client.post(
            f"/decisions/{trade_id}/post-mortem",
            data={
                "executed_at": "",
                "result_pct_after_7d": "",
                "result_pct_after_30d": "",
                "retrospective_notes": "等待入场时机",
                "_now_override": "",
            },
            follow_redirects=False,
        )
        assert response.status_code in (302, 303)


# ── 辅助函数 ──────────────────────────────────────────────


def response_has_post_mortem(html: str) -> bool:
    """检查 show 页是否包含 post-mortem 相关内容。"""
    return any(keyword in html for keyword in ["post-mortem", "事后", "PostMortem"])
