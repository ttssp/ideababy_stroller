"""
Portfolio 域模型 — T002
结论: Watchlist (含 market enum) / Holding / HoldingsSnapshot 三个模型
细节:
  - Market enum: US/HK/CN (R2 D24 per-market session config)
  - Watchlist.market 默认 'US' (架构 §3.5 D24)
  - Holding: 单个持仓条目
  - HoldingsSnapshot: 特定时刻的完整持仓快照
"""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict


class Market(StrEnum):
    """市场枚举 — R2 D24 per-market session config 需要区分市场时区。"""

    US = "US"   # NYSE/NASDAQ: 09:30-16:00 ET
    HK = "HK"   # HKEX: 09:30-16:00 HKT
    CN = "CN"   # SSE/SZSE: 09:30-15:00 CST


class Watchlist(BaseModel):
    """关注股清单条目 — 含 market 字段 (D24)。"""

    model_config = ConfigDict(frozen=True)

    ticker: str
    market: Market = Market.US      # 默认 US (D24)
    display_name: str | None = None  # 可选的显示名称


class Holding(BaseModel):
    """单个持仓条目。"""

    model_config = ConfigDict(frozen=True)

    ticker: str
    market: Market = Market.US
    quantity: float               # 持仓数量
    avg_cost: float | None = None  # 均价成本 (USD)
    current_value: float | None = None  # 当前市值 (USD)


class HoldingsSnapshot(BaseModel):
    """特定时刻的完整持仓快照。"""

    model_config = ConfigDict(frozen=True)

    snapshot_id: str                    # UUID 字符串
    holdings: list[Holding]
    total_value: float | None = None    # 组合总市值 (USD)
    snapshot_at: datetime = datetime.now()
