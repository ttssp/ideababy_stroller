"""
MatrixService — T011 (R3 简化版)
结论: build() 将 watchlist tickers + 三路 signals + 持仓 % 汇总为二维表格 dict 列表
细节:
  - R3 真砍: 不计算错位强度，不按错位排序，默认 ticker 字母序
  - R3 真砍: 不做颜色着色，由 Pico 默认表格样式渲染
  - 方向 score: long=+1 / short=-1 / wait/neutral/no_view=0
  - 每行 dict: {ticker, advisor_score, placeholder_score, agent_score, holding_pct}
  - source_id 映射: "advisor" → advisor_score; "placeholder_model" → placeholder_score;
                    "agent_synthesis" → agent_score
"""

from __future__ import annotations

from decision_ledger.domain.strategy_signal import Direction, StrategySignal

# ── source_id → 列名 映射（锁定三路 lane ID，架构 D7/D22）────────────────
_SOURCE_TO_COL: dict[str, str] = {
    "advisor": "advisor_score",
    "placeholder_model": "placeholder_score",
    "agent_synthesis": "agent_score",
}


def direction_score(direction: Direction) -> int:
    """结论: 方向映射为数值 score (long=+1 / short=-1 / 其他=0)。

    细节:
      - long=+1 (看多建仓)
      - short=-1 (看空)
      - wait/neutral/no_view=0 (中性/等待/无观点)
    """
    if direction == Direction.LONG:
        return 1
    if direction == Direction.SHORT:
        return -1
    # wait / neutral / no_view → 0
    return 0


class MatrixService:
    """错位矩阵服务 — R3 简化版 (无颜色、无排序)。

    结论:
      - build() 是唯一公开方法，返回按 ticker 字母序排列的行列表
      - 每行含 4 个语义列: ticker / advisor_score / placeholder_score / agent_score / holding_pct
      - 设计为无状态纯函数（无 DB 依赖），由 router 负责数据拉取并传入

    细节 (R3 边界):
      - 不计算 direction_diff / 错位强度
      - 不按错位强度排序（默认 ticker 字母序）
      - 不输出颜色 class（CSS 颜色 v0.2+ polish 可加回）
    """

    def build(
        self,
        tickers: list[str],
        signals_by_ticker: dict[str, list[StrategySignal]],
        holdings_pct: dict[str, float],
    ) -> list[dict[str, int | float | str]]:
        """
        构造二维表格（行 = ticker，列 = 三方向 score + 持仓 %）。

        Args:
            tickers: 关注股 ticker 列表（可任意顺序，build 内部重新排字母序）
            signals_by_ticker: {ticker: [StrategySignal, ...]} 三路 signals 缓存
            holdings_pct: {ticker: float} 当前持仓百分比，缺失时默认 0.0

        Returns:
            按 ticker 字母序的行列表，每行为 dict:
            {
                "ticker": str,
                "advisor_score": int,       # +1/0/-1
                "placeholder_score": int,   # +1/0/-1
                "agent_score": int,         # +1/0/-1
                "holding_pct": float,       # 持仓百分比（0.0 表示未持仓）
            }
        """
        # R3: ticker 字母序
        sorted_tickers = sorted(tickers)

        rows: list[dict[str, int | float | str]] = []
        for ticker in sorted_tickers:
            # 初始化三列为 0（无 signal 或缺失时默认中性）
            col_scores: dict[str, int] = {
                "advisor_score": 0,
                "placeholder_score": 0,
                "agent_score": 0,
            }

            # 按 source_id 映射到对应列
            signals = signals_by_ticker.get(ticker, [])
            for sig in signals:
                col_name = _SOURCE_TO_COL.get(sig.source_id)
                if col_name is not None:
                    col_scores[col_name] = direction_score(sig.direction)

            row: dict[str, int | float | str] = {
                "ticker": ticker,
                "advisor_score": col_scores["advisor_score"],
                "placeholder_score": col_scores["placeholder_score"],
                "agent_score": col_scores["agent_score"],
                "holding_pct": holdings_pct.get(ticker, 0.0),
            }
            rows.append(row)

        return rows
