"""
tests.unit.test_run_id — pars.ledger.run_id 单元测试。

覆盖点：
1. generate_ulid 返回 26 字符
2. 10 000 次生成无碰撞
3. 连续生成单调递增（字典序）
4. parse_ulid_timestamp 解出 datetime 接近生成时间
5. 非法 ULID validate_ulid 返回 False
6. Crockford Base32 字符集（无 I/L/O/U）
7. ULID 大小写不敏感（ULID spec 允许小写输入）
8. 空字符串 / None 不崩溃
9. parse_ulid_timestamp 对非法 ULID 抛 ValueError
10. validate_ulid 对正确 ULID 返回 True
"""

from __future__ import annotations

import time
from datetime import datetime, timedelta, timezone, UTC

import pytest

from pars.ledger.run_id import generate_ulid, parse_ulid_timestamp, validate_ulid

# ---------------------------------------------------------------------------
# 1. 基本属性
# ---------------------------------------------------------------------------


def test_generate_ulid_length_is_26():
    """should return 26-character string when generating ULID."""
    result = generate_ulid()
    assert len(result) == 26, f"期望 26 字符，实际 {len(result)!r}：{result!r}"


def test_generate_ulid_returns_string():
    """should return str type when generating ULID."""
    result = generate_ulid()
    assert isinstance(result, str)


# ---------------------------------------------------------------------------
# 2. 唯一性（10000 次无碰撞）
# ---------------------------------------------------------------------------


def test_generate_ulid_no_collision_10000():
    """should produce 10000 unique values when generating in batch."""
    ids = [generate_ulid() for _ in range(10_000)]
    assert len(set(ids)) == 10_000, "10000 次生成中出现碰撞"


# ---------------------------------------------------------------------------
# 3. 单调递增
# ---------------------------------------------------------------------------


def test_generate_ulid_monotonic_within_millisecond():
    """should be lexicographically monotonic when called in rapid succession."""
    ids = [generate_ulid() for _ in range(100)]
    for i in range(1, len(ids)):
        assert ids[i - 1] <= ids[i], (
            f"单调性破坏：ids[{i-1}]={ids[i-1]!r} > ids[{i}]={ids[i]!r}"
        )


# ---------------------------------------------------------------------------
# 4. 时间戳解析
# ---------------------------------------------------------------------------


def test_parse_ulid_timestamp_close_to_now():
    """should extract datetime within 2 seconds of generation time when parsing ULID."""
    before = datetime.now(UTC)
    uid = generate_ulid()
    after = datetime.now(UTC)

    parsed = parse_ulid_timestamp(uid)
    assert parsed.tzinfo is not None, "parse_ulid_timestamp 应返回 UTC-aware datetime"
    assert before - timedelta(seconds=1) <= parsed <= after + timedelta(seconds=1), (
        f"解析时间 {parsed} 超出生成时间范围 [{before}, {after}]"
    )


def test_parse_ulid_timestamp_returns_utc_aware():
    """should return UTC-aware datetime when parsing ULID timestamp."""
    uid = generate_ulid()
    parsed = parse_ulid_timestamp(uid)
    assert parsed.tzinfo is not None
    assert parsed.tzinfo == UTC or parsed.utcoffset().total_seconds() == 0


# ---------------------------------------------------------------------------
# 5. 非法 ULID → validate_ulid 返回 False
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "invalid",
    [
        "",  # 空字符串
        "tooshort",  # 太短
        "A" * 27,  # 太长
        "AAAAAAAAAAAAAAAAAAAAAAAAI",  # 含非 Crockford 字符 I（25 chars 但含 I）
        "000000000000000000000000oo",  # 含 O / o（非 Crockford）
        "00000000000000000000000U00",  # 含 U
        "00000000000000000000000L00",  # 含 L
        "!@#$%^&*()",  # 完全非法
    ],
)
def test_validate_ulid_returns_false_for_invalid(invalid: str):
    """should return False when validating invalid ULID string."""
    assert validate_ulid(invalid) is False, f"期望 False，但 {invalid!r} 通过了校验"


# ---------------------------------------------------------------------------
# 6. Crockford Base32 字符集（排除 I/L/O/U）
# ---------------------------------------------------------------------------


def test_generated_ulid_uses_crockford_base32_charset():
    """should use Crockford Base32 charset (no I/L/O/U) when generating ULID."""
    excluded = set("ILOUilou")
    for _ in range(1000):
        uid = generate_ulid()
        bad_chars = set(uid) & excluded
        assert not bad_chars, (
            f"ULID {uid!r} 包含非 Crockford Base32 字符：{bad_chars!r}"
        )


# ---------------------------------------------------------------------------
# 7. 大小写不敏感（ULID 规范允许小写输入）
# ---------------------------------------------------------------------------


def test_validate_ulid_case_insensitive():
    """should accept lowercase ULID when validating (ULID spec allows it)."""
    uid_upper = generate_ulid()
    uid_lower = uid_upper.lower()
    assert validate_ulid(uid_upper) is True
    assert validate_ulid(uid_lower) is True


# ---------------------------------------------------------------------------
# 8. None / 非字符串不崩溃
# ---------------------------------------------------------------------------


def test_validate_ulid_none_returns_false():
    """should return False (not raise) when None is passed to validate_ulid."""
    assert validate_ulid(None) is False  # type: ignore[arg-type]


def test_validate_ulid_non_string_returns_false():
    """should return False (not raise) when non-string types are passed."""
    assert validate_ulid(12345) is False  # type: ignore[arg-type]
    assert validate_ulid([]) is False  # type: ignore[arg-type]
    assert validate_ulid(object()) is False  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# 9. parse_ulid_timestamp 对非法 ULID 抛 ValueError
# ---------------------------------------------------------------------------


def test_parse_ulid_timestamp_raises_for_invalid():
    """should raise ValueError when parse_ulid_timestamp receives invalid ULID."""
    with pytest.raises(ValueError, match="非合法 ULID"):
        parse_ulid_timestamp("not-a-ulid")


def test_parse_ulid_timestamp_raises_for_empty_string():
    """should raise ValueError when parse_ulid_timestamp receives empty string."""
    with pytest.raises(ValueError):
        parse_ulid_timestamp("")


# ---------------------------------------------------------------------------
# 10. validate_ulid 对正确 ULID 返回 True
# ---------------------------------------------------------------------------


def test_validate_ulid_returns_true_for_valid():
    """should return True when validating freshly generated ULID."""
    for _ in range(10):
        uid = generate_ulid()
        assert validate_ulid(uid) is True, f"合法 ULID {uid!r} 未通过校验"
