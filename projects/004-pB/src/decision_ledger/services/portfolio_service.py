"""
PortfolioService — T012
结论: 关注股 CSV 解析 + 持仓 JSON 解析的纯函数层
细节:
  - parse_watchlist_csv: 解析 CSV 文本，返回 list[dict]，含校验 + dedupe + uppercase
  - parse_holdings_json: 解析 JSON 文本，返回 list[dict]，含校验 + dedupe + uppercase
  - PortfolioServiceError: 统一错误类型，携带用户可读的错误消息

校验规则 (spec §T012):
  - ticker 自动 uppercase
  - ticker 去重（保留第一条）
  - 关注股 / 持仓硬上限 100 条（超过抛错）
  - 关注股 50 条软上限（超过允许但不阻断，调用方可读 len 判断是否需要警告）
  - CSV BOM 头自动去除 (Excel UTF-8 BOM: U+FEFF)
  - JSON cost_basis 截断到 2 位小数
  - JSON root 必须是 array
  - 每条 holdings 必须含 ticker + qty 字段
"""

from __future__ import annotations

import csv
import io
import json


class PortfolioServiceError(Exception):
    """关注股 / 持仓录入校验错误 — 携带用户可读错误消息。"""


# ── 常量 ─────────────────────────────────────────────────────────────────

_HARD_LIMIT = 100  # 硬上限（超过抛错）
_SOFT_LIMIT = 50   # 软上限（超过允许，但调用方应发出警告）
_CSV_BOM = "﻿"  # UTF-8 BOM (Excel 导出时常见)

# 已知的 header 列名关键字（如果第一行 ticker 列完全匹配，则跳过）
_HEADER_KEYWORDS = {"ticker", "symbol", "code"}


def parse_watchlist_csv(csv_text: str) -> list[dict[str, str]]:
    """解析关注股 CSV 文本，返回已去重、已 uppercase 的 row 列表。

    结论: 纯函数，不访问数据库。
    参数 csv_text: 原始 CSV 字符串 (支持 Excel BOM 头)。
    返回: list[dict]，每条含 ticker / sector / note 三个字段 (后两者可空)。
    抛出:
      PortfolioServiceError: 超过硬上限 100 条时。
    细节:
      - BOM 头 (\\ufeff) 自动去除
      - 空行跳过
      - ticker 空白行跳过
      - ticker 自动 uppercase
      - 重复 ticker 取第一条 (case-insensitive 去重)
    """
    # 去除 BOM
    text = csv_text.lstrip(_CSV_BOM)

    reader = csv.reader(io.StringIO(text))
    rows: list[dict[str, str]] = []
    seen_tickers: set[str] = set()
    first_row = True

    for raw_row in reader:
        # 跳过完全空行
        if not any(cell.strip() for cell in raw_row):
            continue

        # 解析各列
        ticker_raw = raw_row[0].strip() if len(raw_row) > 0 else ""
        sector = raw_row[1].strip() if len(raw_row) > 1 else ""
        note = raw_row[2].strip() if len(raw_row) > 2 else ""

        # 跳过 header 行 (首行且 ticker 列是已知 header 关键字)
        if first_row and ticker_raw.lower() in _HEADER_KEYWORDS:
            first_row = False
            continue
        first_row = False

        # 跳过空 ticker
        if not ticker_raw:
            continue

        # uppercase
        ticker = ticker_raw.upper()

        # dedupe (case-insensitive，因已全部 upper，直接比较即可)
        if ticker in seen_tickers:
            continue
        seen_tickers.add(ticker)

        rows.append({"ticker": ticker, "sector": sector, "note": note})

    # 硬上限校验
    if len(rows) > _HARD_LIMIT:
        raise PortfolioServiceError(
            f"关注股数量 {len(rows)} 超过硬上限 {_HARD_LIMIT}，请减少后重试。"
        )

    return rows


def parse_holdings_json(json_text: str) -> list[dict[str, object]]:
    """解析持仓 JSON 文本，返回已去重、已 uppercase 的 holdings 列表。

    结论: 纯函数，不访问数据库。
    参数 json_text: 原始 JSON 字符串，根节点必须是 array。
    返回: list[dict]，每条含 ticker / qty / cost_basis 三个字段。
    抛出:
      PortfolioServiceError: JSON 非法 / 非 array / 缺少必要字段 / 超过硬上限时。
    细节:
      - ticker 自动 uppercase
      - 重复 ticker 取第一条 (case-insensitive 去重)
      - cost_basis 截断到 2 位小数 (None 保留为 None)
      - 超过 100 条抛 PortfolioServiceError
    """
    # 解析 JSON
    try:
        data = json.loads(json_text)
    except json.JSONDecodeError as exc:
        raise PortfolioServiceError(f"JSON 解析失败: {exc}") from exc

    # 根节点必须是 array
    if not isinstance(data, list):
        raise PortfolioServiceError("JSON 根节点必须是 array（列表），例如: [{...}, {...}]")

    result: list[dict[str, object]] = []
    seen_tickers: set[str] = set()

    for i, item in enumerate(data):
        if not isinstance(item, dict):
            raise PortfolioServiceError(f"第 {i + 1} 条 holdings 不是 JSON 对象")

        # 校验必要字段: ticker
        if "ticker" not in item:
            raise PortfolioServiceError(f"第 {i + 1} 条 holdings 缺少 ticker 字段")

        # 校验必要字段: qty
        if "qty" not in item:
            raise PortfolioServiceError(f"第 {i + 1} 条 holdings 缺少 qty 字段")

        ticker_raw = str(item["ticker"]).strip()
        if not ticker_raw:
            raise PortfolioServiceError(f"第 {i + 1} 条 holdings 的 ticker 不能为空")

        ticker = ticker_raw.upper()

        # dedupe
        if ticker in seen_tickers:
            continue
        seen_tickers.add(ticker)

        # qty
        qty_raw = item["qty"]
        try:
            qty = float(qty_raw)
        except (TypeError, ValueError) as exc:
            raise PortfolioServiceError(
                f"第 {i + 1} 条 holdings 的 qty 不是有效数字: {qty_raw}"
            ) from exc

        # cost_basis (可选，容差到 2 位小数)
        cost_basis_raw = item.get("cost_basis")
        cost_basis: float | None
        if cost_basis_raw is None:
            cost_basis = None
        else:
            try:
                cost_basis = round(float(cost_basis_raw), 2)
            except (TypeError, ValueError) as exc:
                raise PortfolioServiceError(
                    f"第 {i + 1} 条 holdings 的 cost_basis 不是有效数字: {cost_basis_raw}"
                ) from exc

        result.append({
            "ticker": ticker,
            "qty": qty,
            "cost_basis": cost_basis,
        })

    # 硬上限校验
    if len(result) > _HARD_LIMIT:
        raise PortfolioServiceError(
            f"持仓数量 {len(result)} 超过硬上限 {_HARD_LIMIT}，请减少后重试。"
        )

    return result
