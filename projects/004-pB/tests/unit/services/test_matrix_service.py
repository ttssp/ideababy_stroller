"""
单元测试 — MatrixService (T011)
结论: 验证 build() 返回行数 ≥ 30，direction_score 计算正确（long=+1/short=-1/wait=0）
细节:
  - R3 简化: 无颜色、无排序（ticker 字母序）、无错位强度分层
  - 每行 dict 含: ticker / advisor_score / placeholder_score / agent_score / holding_pct
  - 测试使用 30 个 ticker 的内存 mock 数据，不依赖 SQLite
"""

from __future__ import annotations

import pytest

from decision_ledger.domain.strategy_signal import Direction, StrategySignal
from decision_ledger.services.matrix_service import MatrixService, direction_score


# ── 辅助工厂 ────────────────────────────────────────────────────────────
def _make_signal(source_id: str, ticker: str, direction: Direction) -> StrategySignal:
    """构造最小 StrategySignal 用于测试。"""
    return StrategySignal(
        source_id=source_id,
        ticker=ticker,
        direction=direction,
        confidence=0.5,
        rationale_plain=f"{source_id} test signal for {ticker}",
        inputs_used={"model_version": "test"},
    )


def _make_30_tickers() -> list[str]:
    """生成 30 个字母序 ticker，模拟 watchlist。"""
    # 混合真实 + 虚构 ticker，保证字母序
    base = [
        "AAPL", "AMZN", "BABA", "BIDU", "BYND",
        "CSCO", "DELL", "DIS",  "EA",   "EBAY",
        "FB",   "GOOG", "GRAB", "HD",   "IBM",
        "INTC", "JD",   "JPM",  "KO",   "LULU",
        "META", "MSFT", "NFLX", "NVDA", "ORCL",
        "PEP",  "QCOM", "SBUX", "SHOP", "TSLA",
    ]
    assert len(base) == 30
    return sorted(base)  # 字母序


# ── 1. direction_score 辅助函数测试 ──────────────────────────────────────
class TestDirectionScore:
    """direction_score(direction) → int 计算规则测试。"""

    def test_should_return_plus1_when_direction_is_long(self) -> None:
        """结论: long → +1."""
        assert direction_score(Direction.LONG) == 1

    def test_should_return_minus1_when_direction_is_short(self) -> None:
        """结论: short → -1."""
        assert direction_score(Direction.SHORT) == -1

    def test_should_return_0_when_direction_is_wait(self) -> None:
        """结论: wait → 0."""
        assert direction_score(Direction.WAIT) == 0

    def test_should_return_0_when_direction_is_neutral(self) -> None:
        """结论: neutral → 0."""
        assert direction_score(Direction.NEUTRAL) == 0

    def test_should_return_0_when_direction_is_no_view(self) -> None:
        """结论: no_view → 0."""
        assert direction_score(Direction.NO_VIEW) == 0


# ── 2. MatrixService.build() 行数测试 ────────────────────────────────────
class TestMatrixServiceBuild:
    """MatrixService.build() 返回结构验证。"""

    @pytest.fixture
    def service(self) -> MatrixService:
        """创建 MatrixService 实例，无需真实 DB。"""
        return MatrixService()

    def _make_signals_for_tickers(
        self, tickers: list[str]
    ) -> dict[str, list[StrategySignal]]:
        """为每个 ticker 生成三路 mock signals。"""
        result: dict[str, list[StrategySignal]] = {}
        directions = [
            Direction.LONG, Direction.SHORT, Direction.WAIT,
            Direction.NEUTRAL, Direction.NO_VIEW,
        ]
        for i, ticker in enumerate(tickers):
            d = directions[i % len(directions)]
            result[ticker] = [
                _make_signal("advisor", ticker, d),
                _make_signal("placeholder_model", ticker, Direction.NEUTRAL),
                _make_signal("agent_synthesis", ticker, Direction.WAIT),
            ]
        return result

    def test_should_return_at_least_30_rows_when_build_with_30_tickers(
        self, service: MatrixService
    ) -> None:
        """结论: 30 个 ticker 时 build() 返回 ≥ 30 行。"""
        tickers = _make_30_tickers()
        signals_by_ticker = self._make_signals_for_tickers(tickers)
        holdings = {t: 3.0 for t in tickers[:10]}  # 前 10 个有持仓

        rows = service.build(
            tickers=tickers,
            signals_by_ticker=signals_by_ticker,
            holdings_pct=holdings,
        )

        assert len(rows) >= 30, f"行数不足 30，实际: {len(rows)}"

    def test_should_return_ticker_in_each_row_when_build(
        self, service: MatrixService
    ) -> None:
        """结论: 每行 dict 必须含 'ticker' 字段。"""
        tickers = _make_30_tickers()
        signals_by_ticker = self._make_signals_for_tickers(tickers)

        rows = service.build(
            tickers=tickers,
            signals_by_ticker=signals_by_ticker,
            holdings_pct={},
        )

        for row in rows:
            assert "ticker" in row, f"行缺少 'ticker' 字段: {row}"

    def test_should_return_4_columns_per_row_when_build(
        self, service: MatrixService
    ) -> None:
        """结论: 每行 dict 含 4 个必要列: ticker/advisor_score/placeholder_score/agent_score/(holding_pct)."""  # noqa: E501
        tickers = _make_30_tickers()[:5]
        signals_by_ticker = self._make_signals_for_tickers(tickers)

        rows = service.build(
            tickers=tickers,
            signals_by_ticker=signals_by_ticker,
            holdings_pct={},
        )

        for row in rows:
            assert "ticker" in row
            assert "advisor_score" in row
            assert "placeholder_score" in row
            assert "agent_score" in row
            assert "holding_pct" in row

    def test_should_return_tickers_in_alphabetical_order_when_build(
        self, service: MatrixService
    ) -> None:
        """结论: R3 简化 — ticker 按字母序排列，不按错位强度排序。"""
        tickers = _make_30_tickers()
        # 故意打乱顺序传入
        import random
        shuffled = tickers[:]
        random.shuffle(shuffled)
        signals_by_ticker = self._make_signals_for_tickers(shuffled)

        rows = service.build(
            tickers=shuffled,
            signals_by_ticker=signals_by_ticker,
            holdings_pct={},
        )

        result_tickers = [row["ticker"] for row in rows]
        assert result_tickers == sorted(result_tickers), (
            "R3: ticker 应按字母序排列，不应按错位强度排序"
        )

    def test_should_map_long_to_score_plus1_when_build(
        self, service: MatrixService
    ) -> None:
        """结论: long 方向在 advisor_score 中映射为 +1。"""
        tickers = ["AAPL"]
        signals = {
            "AAPL": [
                _make_signal("advisor", "AAPL", Direction.LONG),
                _make_signal("placeholder_model", "AAPL", Direction.NEUTRAL),
                _make_signal("agent_synthesis", "AAPL", Direction.SHORT),
            ]
        }

        rows = service.build(
            tickers=tickers,
            signals_by_ticker=signals,
            holdings_pct={},
        )

        assert len(rows) == 1
        row = rows[0]
        assert row["advisor_score"] == 1, f"long → +1，实际: {row['advisor_score']}"
        assert row["placeholder_score"] == 0, f"neutral → 0，实际: {row['placeholder_score']}"
        assert row["agent_score"] == -1, f"short → -1，实际: {row['agent_score']}"

    def test_should_use_holding_pct_when_ticker_in_holdings(
        self, service: MatrixService
    ) -> None:
        """结论: holding_pct 字段从传入的 holdings_pct 读取，精度保留小数。"""
        tickers = ["AAPL"]
        signals = {
            "AAPL": [
                _make_signal("advisor", "AAPL", Direction.LONG),
                _make_signal("placeholder_model", "AAPL", Direction.NEUTRAL),
                _make_signal("agent_synthesis", "AAPL", Direction.WAIT),
            ]
        }
        holdings = {"AAPL": 12.5}

        rows = service.build(
            tickers=tickers,
            signals_by_ticker=signals,
            holdings_pct=holdings,
        )

        assert rows[0]["holding_pct"] == pytest.approx(12.5)

    def test_should_use_0_holding_when_ticker_not_in_holdings(
        self, service: MatrixService
    ) -> None:
        """结论: 不在 holdings 的 ticker holding_pct = 0.0。"""
        tickers = ["AAPL"]
        signals = {
            "AAPL": [
                _make_signal("advisor", "AAPL", Direction.SHORT),
                _make_signal("placeholder_model", "AAPL", Direction.SHORT),
                _make_signal("agent_synthesis", "AAPL", Direction.SHORT),
            ]
        }

        rows = service.build(
            tickers=tickers,
            signals_by_ticker=signals,
            holdings_pct={},
        )

        assert rows[0]["holding_pct"] == pytest.approx(0.0)

    def test_should_handle_missing_signals_gracefully_when_ticker_has_no_signals(
        self, service: MatrixService
    ) -> None:
        """结论: ticker 在 signals_by_ticker 中缺失时，各 score=0，不抛异常。"""
        tickers = ["AAPL", "MSFT"]
        # MSFT 没有 signals
        signals = {
            "AAPL": [
                _make_signal("advisor", "AAPL", Direction.LONG),
                _make_signal("placeholder_model", "AAPL", Direction.NEUTRAL),
                _make_signal("agent_synthesis", "AAPL", Direction.WAIT),
            ]
        }

        rows = service.build(
            tickers=tickers,
            signals_by_ticker=signals,
            holdings_pct={},
        )

        assert len(rows) == 2
        msft_row = next(r for r in rows if r["ticker"] == "MSFT")
        assert msft_row["advisor_score"] == 0
        assert msft_row["placeholder_score"] == 0
        assert msft_row["agent_score"] == 0
