"""
per-market session 集成测试 — D24 H4 verify
结论: 验证 US / HK / CN 三市场交易时段窗口 + 默认 US fallback
细节:
  - test_us_ticker_in_session: US ticker @ 14:00 ET → in_session=True
  - test_hk_ticker_in_session: HK ticker @ 14:00 HKT → in_session=True
  - test_cn_ticker_in_session: CN ticker @ 14:00 CST → in_session=True
  - test_us_ticker_out_of_session: US ticker @ 14:00 HKT (=02:00 ET) → in_session=False
  - test_default_us_fallback: ticker market 未填 → 默认 US 行为
  - test_cn_after_close: CN ticker @ 15:30 CST → in_session=False
"""

from __future__ import annotations

from datetime import datetime
from zoneinfo import ZoneInfo

import pytest


# ── 测试用时区 ──────────────────────────────────────────────────────────────
ET = ZoneInfo("America/New_York")
HKT = ZoneInfo("Asia/Hong_Kong")
CST = ZoneInfo("Asia/Shanghai")


def test_us_ticker_in_session() -> None:
    """should return True when US ticker is checked at 14:00 ET (trading hours)."""
    from decision_ledger.telegram.market_session import is_in_session

    now = datetime(2026, 4, 27, 14, 0, 0, tzinfo=ET)  # 14:00 ET, Monday
    assert is_in_session("US", now=now) is True


def test_hk_ticker_in_session() -> None:
    """should return True when HK ticker is checked at 14:00 HKT (trading hours)."""
    from decision_ledger.telegram.market_session import is_in_session

    now = datetime(2026, 4, 27, 14, 0, 0, tzinfo=HKT)  # 14:00 HKT, Monday
    assert is_in_session("HK", now=now) is True


def test_cn_ticker_in_session() -> None:
    """should return True when CN ticker is checked at 14:00 CST (trading hours)."""
    from decision_ledger.telegram.market_session import is_in_session

    now = datetime(2026, 4, 27, 14, 0, 0, tzinfo=CST)  # 14:00 CST, Monday
    assert is_in_session("CN", now=now) is True


def test_us_ticker_out_of_session_when_checked_at_hkt() -> None:
    """should return False when US ticker is checked at 14:00 HKT (= 02:00 ET, pre-market)."""
    from decision_ledger.telegram.market_session import is_in_session

    # 14:00 HKT = 02:00 ET (UTC+8 vs UTC-4)
    now = datetime(2026, 4, 27, 14, 0, 0, tzinfo=HKT)
    assert is_in_session("US", now=now) is False


def test_default_us_fallback_empty_string() -> None:
    """should default to US session when ticker market is empty string."""
    from decision_ledger.telegram.market_session import is_in_session

    now_in_et = datetime(2026, 4, 27, 14, 0, 0, tzinfo=ET)
    # 空字符串 → 默认 US
    assert is_in_session("", now=now_in_et) is True


def test_default_us_fallback_none_market() -> None:
    """should default to US session when ticker market is None (passed as empty)."""
    from decision_ledger.telegram.market_session import is_in_session

    now_in_et = datetime(2026, 4, 27, 14, 0, 0, tzinfo=ET)
    # None 视为未填 → 默认 US
    assert is_in_session(None, now=now_in_et) is True  # type: ignore[arg-type]


def test_cn_after_close() -> None:
    """should return False when CN ticker is checked at 15:30 CST (after 15:00 close)."""
    from decision_ledger.telegram.market_session import is_in_session

    now = datetime(2026, 4, 27, 15, 30, 0, tzinfo=CST)  # 15:30 CST, after CN close
    assert is_in_session("CN", now=now) is False


def test_us_before_open() -> None:
    """should return False when US ticker is checked at 09:00 ET (before 09:30 open)."""
    from decision_ledger.telegram.market_session import is_in_session

    now = datetime(2026, 4, 27, 9, 0, 0, tzinfo=ET)  # 09:00 ET, before open
    assert is_in_session("US", now=now) is False


def test_us_at_close_time() -> None:
    """should return False when US ticker is checked at exactly 16:00 ET (close time exclusive)."""
    from decision_ledger.telegram.market_session import is_in_session

    now = datetime(2026, 4, 27, 16, 0, 0, tzinfo=ET)  # 16:00 ET, close time
    assert is_in_session("US", now=now) is False


@pytest.mark.parametrize(
    "market,tz,hour,expected",
    [
        ("US", ET, 9, False),    # 09:00 ET — before open (09:30)
        ("US", ET, 10, True),    # 10:00 ET — in session
        ("US", ET, 16, False),   # 16:00 ET — at close (exclusive)
        ("HK", HKT, 9, False),   # 09:00 HKT — before open
        ("HK", HKT, 12, True),   # 12:00 HKT — in session
        ("HK", HKT, 16, False),  # 16:00 HKT — at close (exclusive)
        ("CN", CST, 9, False),   # 09:00 CST — before open
        ("CN", CST, 12, True),   # 12:00 CST — in session
        ("CN", CST, 15, False),  # 15:00 CST — at close (exclusive)
    ],
)
def test_parametrized_session_windows(
    market: str, tz: ZoneInfo, hour: int, expected: bool
) -> None:
    """should correctly identify in/out session for parametrized market/hour combinations."""
    from decision_ledger.telegram.market_session import is_in_session

    now = datetime(2026, 4, 27, hour, 0, 0, tzinfo=tz)
    assert is_in_session(market, now=now) is expected
