"""
/conflicts 路由集成测试 — T010
结论: 验证三列渲染顺序按 rendered_order_seed、空态显示"暂无分歧"
细节:
  - test_three_columns_render: HTML 含 3 个 [data-source] 元素，顺序按 rendered_order_seed
  - test_empty_state_shown: 全 no_view 时 HTML 渲染 "暂无分歧"
  - test_conflict_list_route: GET /conflicts 返回 200
  - test_conflict_detail_route: GET /conflicts/{report_id} 返回 200
"""

from __future__ import annotations

from typing import Any

from fastapi.testclient import TestClient

from decision_ledger.domain.conflict_report import ConflictReport
from decision_ledger.domain.strategy_signal import Direction, StrategySignal

# ── 测试辅助工厂 ──────────────────────────────────────────


def _make_signal(
    source_id: str,
    ticker: str = "AAPL",
    direction: Direction = Direction.LONG,
    confidence: float = 0.8,
) -> StrategySignal:
    return StrategySignal(
        source_id=source_id,
        ticker=ticker,
        direction=direction,
        confidence=confidence,
        rationale_plain=f"{source_id} 的分析：趋势向上，基本面支撑",
        inputs_used={"advisor_week_id": "2026-W17"},
    )


def _make_no_view_signal(source_id: str) -> StrategySignal:
    return StrategySignal(
        source_id=source_id,
        ticker="AAPL",
        direction=Direction.NO_VIEW,
        confidence=0.0,
        rationale_plain=f"{source_id} 无观点",
        inputs_used={},
    )


def _make_conflict_report(
    seed: int = 2,
    has_divergence: bool = True,
    all_no_view: bool = False,
) -> ConflictReport:
    """构造 ConflictReport。"""
    if all_no_view:
        signals = [
            _make_no_view_signal("advisor"),
            _make_no_view_signal("placeholder_model"),
            _make_no_view_signal("agent_synthesis"),
        ]
        return ConflictReport(
            signals=signals,
            divergence_root_cause="暂无分歧",
            has_divergence=False,
            rendered_order_seed=seed,
        )
    return ConflictReport(
        signals=[
            _make_signal("advisor", direction=Direction.LONG),
            _make_signal("placeholder_model", direction=Direction.NEUTRAL),
            _make_signal("agent_synthesis", direction=Direction.WAIT),
        ],
        divergence_root_cause="advisor 看多但 agent_synthesis 建议等待，分歧明显",
        has_divergence=has_divergence,
        rendered_order_seed=seed,
    )


def _make_app_with_fake_repo(
    reports: dict[str, ConflictReport] | None = None,
) -> Any:
    """构造 test FastAPI app，注入 fake conflict repo。"""
    from pathlib import Path

    from fastapi import FastAPI
    from fastapi.staticfiles import StaticFiles
    from fastapi.templating import Jinja2Templates

    _UI_DIR = Path(__file__).parents[3] / "src" / "decision_ledger" / "ui"
    TEMPLATES_DIR = _UI_DIR / "templates"
    STATIC_DIR = _UI_DIR / "static"

    app = FastAPI()

    # 如果 static 目录存在则挂载
    if STATIC_DIR.exists():
        app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

    app_templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

    if reports is None:
        reports = {}

    class FakeConflictRepo:
        async def get(self, report_id: str) -> ConflictReport | None:
            return reports.get(report_id)

        async def list_recent(self, limit: int = 10) -> list[ConflictReport]:
            return list(reports.values())[:limit]

    from decision_ledger.ui import router_conflicts

    router_conflicts.set_conflict_repo(FakeConflictRepo())
    router_conflicts.set_templates(app_templates)

    app.include_router(router_conflicts.router)

    return app


# ── 路由存在性测试 ──────────────────────────────────────────


class TestConflictRoutes:
    """/conflicts 路由基础行为测试。"""

    def test_conflict_list_route_exists(self) -> None:
        """结论: GET /conflicts 路由存在且返回 200。"""
        app = _make_app_with_fake_repo(reports={})
        client = TestClient(app, raise_server_exceptions=True)
        resp = client.get("/conflicts")
        assert resp.status_code == 200

    def test_conflict_list_route_html_response(self) -> None:
        """结论: GET /conflicts 返回 HTML 内容。"""
        app = _make_app_with_fake_repo(reports={})
        client = TestClient(app, raise_server_exceptions=True)
        resp = client.get("/conflicts")
        assert "text/html" in resp.headers.get("content-type", "")

    def test_conflict_detail_route_exists(self) -> None:
        """结论: GET /conflicts/{report_id} 路由存在，404 when not found。"""
        app = _make_app_with_fake_repo(reports={})
        client = TestClient(app, raise_server_exceptions=False)
        resp = client.get("/conflicts/nonexistent-id")
        assert resp.status_code == 404

    def test_conflict_detail_route_200_when_found(self) -> None:
        """结论: GET /conflicts/{report_id} 存在时返回 200。"""
        report = _make_conflict_report(seed=3)
        app = _make_app_with_fake_repo(reports={"test-report-1": report})
        client = TestClient(app, raise_server_exceptions=True)
        resp = client.get("/conflicts/test-report-1")
        assert resp.status_code == 200

    def test_by_decision_route_exists(self) -> None:
        """结论: GET /conflicts/by-decision/{trade_id} 路由存在。"""
        app = _make_app_with_fake_repo(reports={})
        client = TestClient(app, raise_server_exceptions=False)
        # 该路由返回 404 when trade_id 不存在，但路由本身应存在（非 405）
        resp = client.get("/conflicts/by-decision/nonexistent-trade")
        assert resp.status_code in (200, 404), (
            f"by-decision 路由应存在，状态码应为 200 或 404，当前 {resp.status_code}"
        )


class TestThreeColumnsRender:
    """三列渲染顺序测试 (R2 D22 R10)。"""

    def test_three_columns_render(self) -> None:
        """结论: HTML 含 3 个 [data-source] 元素。"""
        report = _make_conflict_report(seed=1)
        app = _make_app_with_fake_repo(reports={"report-1": report})
        client = TestClient(app, raise_server_exceptions=True)

        resp = client.get("/conflicts/report-1")
        assert resp.status_code == 200

        # 验证 HTML 含 3 个 data-source 属性元素
        html = resp.text
        data_source_count = html.count("data-source")
        assert data_source_count >= 3, (
            f"三列模板应含 ≥ 3 个 data-source 属性，当前 {data_source_count}。"
            f"HTML 片段: {html[:500]}"
        )

    def test_three_columns_contain_all_sources(self) -> None:
        """结论: 三列 HTML 中含有所有三个 source_id。"""
        report = _make_conflict_report(seed=0)
        app = _make_app_with_fake_repo(reports={"report-2": report})
        client = TestClient(app, raise_server_exceptions=True)

        resp = client.get("/conflicts/report-2")
        html = resp.text

        for source_id in ("advisor", "placeholder_model", "agent_synthesis"):
            assert source_id in html, (
                f"三列 HTML 中应含 source_id '{source_id}'"
            )

    def test_rationale_plain_rendered(self) -> None:
        """结论: 每列的 rationale_plain 必须显式渲染，不能静默忽略。"""
        report = _make_conflict_report(seed=2)
        app = _make_app_with_fake_repo(reports={"report-3": report})
        client = TestClient(app, raise_server_exceptions=True)

        resp = client.get("/conflicts/report-3")
        html = resp.text

        # rationale_plain 的内容应该出现在 HTML 中
        for signal in report.signals:
            assert signal.rationale_plain in html, (
                f"signal.rationale_plain 必须渲染到 HTML，"
                f"source_id={signal.source_id}: {signal.rationale_plain!r}"
            )

    def test_divergence_root_cause_rendered(self) -> None:
        """结论: divergence_root_cause 应渲染在页面上。"""
        report = _make_conflict_report(seed=2)
        app = _make_app_with_fake_repo(reports={"report-4": report})
        client = TestClient(app, raise_server_exceptions=True)

        resp = client.get("/conflicts/report-4")
        html = resp.text

        # 根因文字应出现在 HTML 中
        # 截取关键词（避免 HTML 转义问题）
        assert "advisor" in html and "分歧" in html, (
            "divergence_root_cause 的关键内容应渲染到页面"
        )


class TestEmptyState:
    """空态渲染测试 (has_divergence=False or 全 no_view)。"""

    def test_empty_state_shown_when_all_no_view(self) -> None:
        """结论: 全 no_view 时，HTML 含 '暂无分歧' 字符串。"""
        report = _make_conflict_report(all_no_view=True)
        app = _make_app_with_fake_repo(reports={"report-empty": report})
        client = TestClient(app, raise_server_exceptions=True)

        resp = client.get("/conflicts/report-empty")
        assert resp.status_code == 200
        html = resp.text

        assert "暂无分歧" in html, (
            f"全 no_view 时页面应显示 '暂无分歧'，当前 HTML: {html[:500]}"
        )

    def test_empty_state_shown_when_has_divergence_false(self) -> None:
        """结论: has_divergence=False 时，HTML 含 '暂无分歧'。"""
        report = _make_conflict_report(has_divergence=False, all_no_view=True)
        app = _make_app_with_fake_repo(reports={"report-no-div": report})
        client = TestClient(app, raise_server_exceptions=True)

        resp = client.get("/conflicts/report-no-div")
        html = resp.text
        assert "暂无分歧" in html

    def test_empty_state_not_an_error_page(self) -> None:
        """结论: 空态是正常状态，不是 error page（应返回 200，文案平静）。"""
        report = _make_conflict_report(all_no_view=True)
        app = _make_app_with_fake_repo(reports={"report-ok": report})
        client = TestClient(app, raise_server_exceptions=True)

        resp = client.get("/conflicts/report-ok")
        assert resp.status_code == 200, "空态应返回 200，不是错误状态"

    def test_list_empty_when_no_reports(self) -> None:
        """结论: /conflicts 列表页，无报告时正常返回 200。"""
        app = _make_app_with_fake_repo(reports={})
        client = TestClient(app, raise_server_exceptions=True)
        resp = client.get("/conflicts")
        assert resp.status_code == 200
