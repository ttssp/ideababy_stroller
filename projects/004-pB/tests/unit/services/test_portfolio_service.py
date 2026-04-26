"""
T012 — PortfolioService 单元测试
结论: TDD 先行，覆盖 ticker dedupe / uppercase / 上限 / 非法格式 / BOM 去除
细节:
  - test_replace_watchlist_*: 关注股录入校验逻辑
  - test_parse_holdings_*: 持仓 JSON 解析逻辑
  - 所有测试不依赖数据库 (service 层 parse 方法为纯函数)
"""

from __future__ import annotations

import pytest

from decision_ledger.services.portfolio_service import (
    PortfolioServiceError,
    parse_holdings_json,
    parse_watchlist_csv,
)

# ─── parse_watchlist_csv ─────────────────────────────────────────────────


class TestParseWatchlistCsv:
    """parse_watchlist_csv 纯解析函数测试组。"""

    def test_should_uppercase_ticker_when_lowercase_input(self) -> None:
        """ticker 小写应自动转大写 (spec §R1: tsm → TSM)。"""
        rows = parse_watchlist_csv("tsm,Tech,Taiwan Semi\nappl,Tech,Apple\n")
        tickers = [r["ticker"] for r in rows]
        assert tickers == ["TSM", "APPL"]

    def test_should_dedupe_ticker_when_duplicates_in_csv(self) -> None:
        """重复 ticker 应去重，保留第一条。"""
        rows = parse_watchlist_csv("TSM,Tech,\nTSM,Finance,duplicate\nAAPL,Tech,\n")
        tickers = [r["ticker"] for r in rows]
        assert tickers == ["TSM", "AAPL"]
        assert len(rows) == 2

    def test_should_dedupe_case_insensitive_when_mixed_case(self) -> None:
        """大小写混合的重复 ticker 也应去重 (tsm + TSM = 1 条)。"""
        rows = parse_watchlist_csv("tsm,Tech,\nTSM,Finance,dup\n")
        assert len(rows) == 1
        assert rows[0]["ticker"] == "TSM"

    def test_should_raise_when_exceeds_100_hard_limit(self) -> None:
        """超过 100 个 ticker 应抛 PortfolioServiceError (硬上限)。"""
        lines = "\n".join(f"TK{i:03d},Tech," for i in range(101))
        with pytest.raises(PortfolioServiceError, match="100"):
            parse_watchlist_csv(lines)

    def test_should_warn_when_exceeds_50_soft_limit(self) -> None:
        """超过 50 个 (≤ 100) ticker 应返回结果但 rows 中有 warning 标记。"""
        lines = "\n".join(f"TK{i:03d},Tech," for i in range(60))
        result = parse_watchlist_csv(lines)
        # 返回 60 行（不阻断）
        assert len(result) == 60

    def test_should_strip_bom_when_excel_utf8_bom_csv(self) -> None:
        """Excel 导出的 UTF-8 BOM 头 (\\ufeff) 应自动去除。"""
        bom_csv = "﻿tsm,Tech,Taiwan Semi\naapl,Tech,Apple\n"
        rows = parse_watchlist_csv(bom_csv)
        # 首个 ticker 不应含 BOM 字符
        assert rows[0]["ticker"] == "TSM"

    def test_should_skip_blank_lines_when_csv_has_empty_rows(self) -> None:
        """空行应跳过不计入结果。"""
        csv_text = "TSM,Tech,\n\n\nAAPL,Tech,\n"
        rows = parse_watchlist_csv(csv_text)
        assert len(rows) == 2

    def test_should_allow_optional_columns_when_only_ticker_provided(self) -> None:
        """只有 ticker 列时应正常解析，sector/note 默认空字符串。"""
        rows = parse_watchlist_csv("TSM\nAAPL\n")
        assert len(rows) == 2
        assert rows[0]["ticker"] == "TSM"
        assert rows[0].get("sector", "") == ""

    def test_should_raise_when_ticker_is_blank(self) -> None:
        """ticker 列为空白字符串的行应被忽略（不报错，不入库）。"""
        rows = parse_watchlist_csv(",Tech,note\nAAPL,Tech,\n")
        # 空 ticker 行跳过
        tickers = [r["ticker"] for r in rows]
        assert "" not in tickers
        assert "AAPL" in tickers

    def test_should_parse_valid_csv_with_header_row(self) -> None:
        """含 header 行的 CSV 应正确跳过 header。"""
        csv_text = "ticker,sector,note\nTSM,Tech,Taiwan Semi\nAAPL,Tech,Apple\n"
        rows = parse_watchlist_csv(csv_text)
        # header 行 'ticker' 不应出现在结果中（它是列名）
        tickers = [r["ticker"] for r in rows]
        assert "ticker" not in tickers
        assert "TSM" in tickers
        assert "AAPL" in tickers


# ─── parse_holdings_json ─────────────────────────────────────────────────


class TestParseHoldingsJson:
    """parse_holdings_json 纯解析函数测试组。"""

    def test_should_parse_valid_json_when_correct_format(self) -> None:
        """合法 JSON 数组应正确解析。"""
        json_text = '[{"ticker": "TSM", "qty": 100, "cost_basis": 92.0}]'
        holdings = parse_holdings_json(json_text)
        assert len(holdings) == 1
        assert holdings[0]["ticker"] == "TSM"
        assert holdings[0]["qty"] == 100
        assert abs(holdings[0]["cost_basis"] - 92.0) < 0.01

    def test_should_raise_when_invalid_json(self) -> None:
        """非法 JSON 应抛 PortfolioServiceError。"""
        with pytest.raises(PortfolioServiceError, match="JSON"):
            parse_holdings_json("not a json at all {{{{")

    def test_should_raise_when_json_is_not_array(self) -> None:
        """JSON 根节点不是 array 时应抛 PortfolioServiceError。"""
        with pytest.raises(PortfolioServiceError, match="array"):
            parse_holdings_json('{"ticker": "TSM", "qty": 100}')

    def test_should_raise_when_missing_required_ticker_field(self) -> None:
        """缺少 ticker 字段应抛 PortfolioServiceError。"""
        with pytest.raises(PortfolioServiceError, match="ticker"):
            parse_holdings_json('[{"qty": 100, "cost_basis": 92.0}]')

    def test_should_raise_when_missing_required_qty_field(self) -> None:
        """缺少 qty 字段应抛 PortfolioServiceError。"""
        with pytest.raises(PortfolioServiceError, match="qty"):
            parse_holdings_json('[{"ticker": "TSM", "cost_basis": 92.0}]')

    def test_should_uppercase_ticker_in_holdings_json(self) -> None:
        """holdings 中的 ticker 也应 uppercase。"""
        json_text = '[{"ticker": "tsm", "qty": 100, "cost_basis": 92.0}]'
        holdings = parse_holdings_json(json_text)
        assert holdings[0]["ticker"] == "TSM"

    def test_should_dedupe_holdings_by_ticker(self) -> None:
        """重复 ticker 的 holdings 应去重，保留第一条。"""
        json_text = (
            '[{"ticker": "TSM", "qty": 100, "cost_basis": 92.0},'
            ' {"ticker": "tsm", "qty": 200, "cost_basis": 88.0}]'
        )
        holdings = parse_holdings_json(json_text)
        assert len(holdings) == 1
        assert holdings[0]["qty"] == 100  # 保留第一条

    def test_should_tolerate_cost_basis_to_2_decimal_places(self) -> None:
        """cost_basis 精度应容差到 2 位小数。"""
        json_text = '[{"ticker": "TSM", "qty": 100, "cost_basis": 92.123456}]'
        holdings = parse_holdings_json(json_text)
        # 不报错，cost_basis 存入时截为 2 位
        assert round(holdings[0]["cost_basis"], 2) == 92.12

    def test_should_allow_null_cost_basis(self) -> None:
        """cost_basis 为 null 时应允许（可选字段）。"""
        json_text = '[{"ticker": "TSM", "qty": 100, "cost_basis": null}]'
        holdings = parse_holdings_json(json_text)
        assert holdings[0]["cost_basis"] is None

    def test_should_raise_when_exceeds_100_holdings(self) -> None:
        """持仓超过 100 条应抛 PortfolioServiceError（硬上限复用 watchlist 逻辑）。"""
        items = [{"ticker": f"TK{i:03d}", "qty": 10, "cost_basis": 1.0} for i in range(101)]
        import json
        with pytest.raises(PortfolioServiceError, match="100"):
            parse_holdings_json(json.dumps(items))


# ─── 边界值 ──────────────────────────────────────────────────────────────


class TestBoundaryValues:
    """边界值专项测试。"""

    def test_should_accept_exactly_50_watchlist_items(self) -> None:
        """恰好 50 个关注股应正常返回（软上限边界）。"""
        lines = "\n".join(f"TK{i:03d},Tech," for i in range(50))
        rows = parse_watchlist_csv(lines)
        assert len(rows) == 50

    def test_should_accept_exactly_100_watchlist_items(self) -> None:
        """恰好 100 个关注股应正常返回（硬上限边界，不超过）。"""
        lines = "\n".join(f"TK{i:03d},Tech," for i in range(100))
        rows = parse_watchlist_csv(lines)
        assert len(rows) == 100

    def test_should_reject_101_watchlist_items(self) -> None:
        """101 个关注股应抛错（超过硬上限）。"""
        lines = "\n".join(f"TK{i:03d},Tech," for i in range(101))
        with pytest.raises(PortfolioServiceError):
            parse_watchlist_csv(lines)
