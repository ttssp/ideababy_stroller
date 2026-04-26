"""
集成测试 — GET /matrix 路由 (T011)
结论: 验证 /matrix 返回 200 + HTML table + ≥ 30 行 (R3: 无颜色断言)
细节:
  - 使用 FastAPI TestClient + seed 30 个 mock tickers
  - R3 简化: 不断言颜色 class，仅断言 <table>、<tr> 计数、<th> 4 列
  - MatrixService 通过依赖注入 mock（不触 DB）
  - D16: grep 确认无 plotly/matplotlib/d3/chart.js
"""

from __future__ import annotations

import os
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

# ── 30 个测试 ticker ─────────────────────────────────────────────────────
MOCK_TICKERS = sorted([
    "AAPL", "AMZN", "BABA", "BIDU", "BYND",
    "CSCO", "DELL", "DIS",  "EA",   "EBAY",
    "FB",   "GOOG", "GRAB", "HD",   "IBM",
    "INTC", "JD",   "JPM",  "KO",   "LULU",
    "META", "MSFT", "NFLX", "NVDA", "ORCL",
    "PEP",  "QCOM", "SBUX", "SHOP", "TSLA",
])

assert len(MOCK_TICKERS) == 30


def _make_mock_rows(tickers: list[str]) -> list[dict]:
    """构造 MatrixService.build() 的 mock 返回值（30 行）。"""
    rows = []
    for i, ticker in enumerate(tickers):
        score_cycle = [1, -1, 0, 1, -1]
        rows.append({
            "ticker": ticker,
            "advisor_score": score_cycle[i % 5],
            "placeholder_score": score_cycle[(i + 1) % 5],
            "agent_score": score_cycle[(i + 2) % 5],
            "holding_pct": float(i % 10) * 2.5,
        })
    return rows


# ── Fixture ──────────────────────────────────────────────────────────────
@pytest.fixture
def app_client() -> TestClient:
    """创建带 mock MatrixService 的 TestClient。"""
    os.environ.setdefault("ANTHROPIC_API_KEY", "test-key-placeholder")
    os.environ.setdefault("TELEGRAM_BOT_TOKEN", "test-token-placeholder")

    from decision_ledger.ui.app import create_app

    test_app = create_app()

    # 包含 matrix router
    from decision_ledger.ui import router_matrix
    test_app.include_router(router_matrix.router)

    return TestClient(test_app, raise_server_exceptions=True)


@pytest.fixture
def mocked_matrix_app_client() -> TestClient:
    """创建 TestClient，MatrixService.build() 被 mock 返回 30 行固定数据。"""
    os.environ.setdefault("ANTHROPIC_API_KEY", "test-key-placeholder")
    os.environ.setdefault("TELEGRAM_BOT_TOKEN", "test-token-placeholder")

    mock_rows = _make_mock_rows(MOCK_TICKERS)

    with patch(
        "decision_ledger.ui.router_matrix.MatrixService"
    ) as MockMatrixService:
        mock_svc = MagicMock()
        mock_svc.build.return_value = mock_rows
        MockMatrixService.return_value = mock_svc

        from decision_ledger.ui import router_matrix
        from decision_ledger.ui.app import create_app

        test_app = create_app()
        test_app.include_router(router_matrix.router)

        yield TestClient(test_app, raise_server_exceptions=True)


# ── 测试组 ───────────────────────────────────────────────────────────────
class TestMatrixRoute:
    """GET /matrix 路由集成测试。"""

    def test_should_return_200_when_get_matrix(
        self, mocked_matrix_app_client: TestClient
    ) -> None:
        """结论: GET /matrix 必须返回 200。"""
        response = mocked_matrix_app_client.get("/matrix")
        assert response.status_code == 200

    def test_should_return_html_content_type_when_get_matrix(
        self, mocked_matrix_app_client: TestClient
    ) -> None:
        """结论: Content-Type 必须是 text/html。"""
        response = mocked_matrix_app_client.get("/matrix")
        assert "text/html" in response.headers.get("content-type", "")

    def test_should_contain_html_table_when_get_matrix(
        self, mocked_matrix_app_client: TestClient
    ) -> None:
        """结论: 响应 HTML 必须包含 <table> 标签 (D16: 纯 HTML table)。"""
        response = mocked_matrix_app_client.get("/matrix")
        assert "<table" in response.text, "响应中缺少 <table> 标签"

    def test_should_contain_at_least_30_table_rows_when_get_matrix(
        self, mocked_matrix_app_client: TestClient
    ) -> None:
        """结论: tbody 中至少有 30 个 <tr> 行（对应 30 个 ticker）。"""
        response = mocked_matrix_app_client.get("/matrix")
        # 计算 <tr> 数量（包含 thead 的 1 行，实际数据行 ≥ 30）
        tr_count = response.text.count("<tr")
        # thead 有 1 行, tbody 有 30 行, 合计 ≥ 31
        assert tr_count >= 31, f"<tr> 总数不足 31 (1 header + 30 data)，实际: {tr_count}"

    def test_should_contain_4_column_headers_when_get_matrix(
        self, mocked_matrix_app_client: TestClient
    ) -> None:
        """结论: thead 必须包含 4 列表头 (ticker/三方向/持仓%)。"""
        response = mocked_matrix_app_client.get("/matrix")
        html = response.text
        # 必含 4 个 <th>
        th_count = html.count("<th")
        assert th_count >= 4, f"表头 <th> 不足 4，实际: {th_count}"

    def test_should_show_ticker_names_in_table_when_get_matrix(
        self, mocked_matrix_app_client: TestClient
    ) -> None:
        """结论: 表格中必须出现 AAPL、MSFT 等 ticker 名称。"""
        response = mocked_matrix_app_client.get("/matrix")
        html = response.text
        for ticker in ["AAPL", "MSFT", "TSLA"]:
            assert ticker in html, f"表格中缺少 ticker: {ticker}"

    def test_should_not_contain_chart_libraries_when_get_matrix(
        self, mocked_matrix_app_client: TestClient
    ) -> None:
        """结论: D16 红线 — 响应 HTML 不得含图表库引用。"""
        response = mocked_matrix_app_client.get("/matrix")
        html = response.text
        for lib in ["plotly", "matplotlib", "d3.js", "chart.js", "Chart.js"]:
            assert lib not in html, f"D16 违反: 响应 HTML 包含图表库引用: {lib}"

    def test_should_not_contain_colored_cell_class_when_get_matrix(
        self, mocked_matrix_app_client: TestClient
    ) -> None:
        """结论: R3 简化 — 不含颜色 class (matrix-red / matrix-yellow / matrix-green 等)。"""
        response = mocked_matrix_app_client.get("/matrix")
        html = response.text
        color_classes = ["matrix-red", "matrix-yellow", "matrix-green", "cell-red", "cell-yellow"]
        for color_class in color_classes:
            assert color_class not in html, f"R3: 不应含颜色 class: {color_class}"

    def test_should_have_matrix_as_active_nav_when_get_matrix(
        self, mocked_matrix_app_client: TestClient
    ) -> None:
        """结论: /matrix 页面中错位矩阵 tab 应被高亮 (aria-current)。"""
        response = mocked_matrix_app_client.get("/matrix")
        html = response.text
        # 检查 aria-current="page" 和 /matrix 出现在附近
        assert 'aria-current="page"' in html, "错位矩阵 tab 应有 aria-current 高亮"

    def test_should_contain_nav_with_matrix_third_when_get_matrix(
        self, mocked_matrix_app_client: TestClient
    ) -> None:
        """结论: OP-6 验证 — 错位矩阵仍在 nav 第三位（nav 由 T004 _nav.html 提供）。"""
        response = mocked_matrix_app_client.get("/matrix")
        html = response.text
        pos_conflicts = html.find("冲突报告")
        pos_matrix = html.find("错位矩阵")
        pos_notes = html.find("笔记")
        assert pos_conflicts > 0, "nav 中缺少冲突报告"
        assert pos_matrix > 0, "nav 中缺少错位矩阵"
        assert pos_notes > 0, "nav 中缺少笔记"
        assert pos_conflicts < pos_matrix < pos_notes, (
            "OP-6: 错位矩阵必须排在冲突报告之后、笔记之前"
        )
