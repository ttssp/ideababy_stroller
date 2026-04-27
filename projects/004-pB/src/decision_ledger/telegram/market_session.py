"""
market_session.py — T017 R2 D24 per-market session config
结论: 提供 US/HK/CN 三市场交易时段 window，is_in_session() 判断当前时间是否在 session 内
细节:
  - MARKET_SESSIONS: 字典 market→(ZoneInfo, open_str, close_str)
  - is_in_session(): 将 now 转到市场时区后比较 [open, close) 区间
  - 默认 US fallback: ticker.market 未填或为 None 时使用 US session
  - 用 zoneinfo (PEP 615)，不用 pytz (deprecated)
  - close 时间为 exclusive（到达 close 时刻即视为关闭）
"""

from __future__ import annotations

from datetime import datetime, time
from zoneinfo import ZoneInfo

# ── 市场 session 配置 ──────────────────────────────────────────────────────────
# 结论: 三市场时区 + 开收盘时间，key = ticker.market 字段值
MARKET_SESSIONS: dict[str, tuple[ZoneInfo, str, str]] = {
    "US": (ZoneInfo("America/New_York"), "09:30", "16:00"),
    "HK": (ZoneInfo("Asia/Hong_Kong"), "09:30", "16:00"),
    "CN": (ZoneInfo("Asia/Shanghai"), "09:30", "15:00"),
}

# 默认市场（ticker.market 未填时使用）
_DEFAULT_MARKET = "US"


def is_in_session(ticker_market: str | None, now: datetime | None = None) -> bool:
    """判断当前时间是否在指定市场的交易 session 内。

    结论: 将 now 转换到市场时区，与 [open, close) 区间比较（close 为 exclusive）。

    参数:
        ticker_market: 市场代码 ("US" | "HK" | "CN")，None 或空字符串 → US fallback
        now: 参考时间，None 则使用当前 UTC 时间

    返回:
        True 若当前市场时区时间在 [open, close) 内，否则 False。
    """
    # 默认 US fallback: None 或空字符串
    market = ticker_market if ticker_market else _DEFAULT_MARKET
    if market not in MARKET_SESSIONS:
        market = _DEFAULT_MARKET

    tz, open_str, close_str = MARKET_SESSIONS[market]

    # 若 now 未提供，使用 UTC 当前时间
    if now is None:
        now = datetime.now(tz=ZoneInfo("UTC"))

    # 转换到市场时区
    local_now = now.astimezone(tz)
    current_time = local_now.time()

    # 解析开收盘时间
    open_time = _parse_time(open_str)
    close_time = _parse_time(close_str)

    # [open, close) 区间，close 为 exclusive
    return open_time <= current_time < close_time


def _parse_time(time_str: str) -> time:
    """将 "HH:MM" 格式字符串解析为 time 对象。

    结论: 用 strptime 解析，确保格式一致性。
    """
    parsed = datetime.strptime(time_str, "%H:%M")
    return parsed.time()
