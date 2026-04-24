"""
ULID（Universally Unique Lexicographically Sortable Identifier）工具。

结论：D14 决策，run_id 用 ULID 而非 timestamp/UUID。
- 时间有序（启动顺序 = 字典序），便于 `pars status` 排列 run 列表
- 26 字符 Crockford Base32，比 UUID 短且 URL-safe
- 依赖 ulid-py==1.1.0（已在 uv.lock 中锁定）

对外 API（稳定，调用方不感知底层包）：
- generate_ulid() -> str           生成新 ULID（单调递增）
- validate_ulid(s) -> bool         格式校验（严格 Crockford 字符集）
- parse_ulid_timestamp(s) -> datetime  从 ULID 提取生成时间（UTC）

### 实现说明

使用 ulid.api.monotonic（单调 provider）而非 ulid.new()（默认 default provider）：
- default provider 在同一毫秒内随机填充 80-bit randomness，可能导致字典序倒退
- monotonic provider 在同一毫秒内递增 least-significant bit，保证严格单调

validate_ulid 不依赖 ulid-py 的 from_str（其 Crockford decode 会把 O→0、L→1、I→1
等"纠正"后接受），改用正则精确匹配合法字符集，严格拒绝 I/L/O/U。

parse_ulid_timestamp 不调用 ulid-py 的 Timestamp.datetime（其内部用 deprecated 的
utcfromtimestamp()），改为手动从毫秒整数构造 UTC datetime。
"""

from __future__ import annotations

import re
from datetime import datetime, timezone

from ulid.api import monotonic as _ulid_monotonic
from ulid.api import default as _ulid_default

# ---------------------------------------------------------------------------
# Crockford Base32 严格校验正则（不含 I/L/O/U，大小写不敏感）
# 字符集：0-9, A-H, J-N, P-T, V-Z（共 32 个，大小写均可）
# ULID = 10 字符时间戳 + 16 字符随机数 = 26 字符
# ---------------------------------------------------------------------------

# Crockford Base32 字符范围（大写）：
#   0-9          数字 10 个
#   A-H          字母 8 个（A B C D E F G H）
#   J-K          字母 2 个（J K，跳过 I）
#   M-N          字母 2 个（M N，跳过 L）
#   P-T          字母 5 个（P Q R S T，跳过 O）
#   V-Z          字母 5 个（V W X Y Z，跳过 U）
# 共 10 + 22 = 32 个符号；小写形式（0-9 无小写）同上但转小写
# 注意：不能用 J-N（包含 L）或 N-T（包含 O），必须精确区间
_ULID_RE = re.compile(r"^[0-9A-HJ-KM-NP-TV-Za-hj-km-np-tv-z]{26}$")


# ---------------------------------------------------------------------------
# 公开 API
# ---------------------------------------------------------------------------


def generate_ulid() -> str:
    """生成新 ULID（26 字符 Crockford Base32，单调递增）。

    使用 ulid-py 的 monotonic provider：同一毫秒内连续调用时，随机部分的
    最低有效位递增，保证字典序严格单调。跨毫秒时自然递增（时间戳部分更大）。

    返回：大写 26 字符 ULID 字符串，如 "01HXYZ..."
    """
    return str(_ulid_monotonic.new())


def validate_ulid(s: object) -> bool:
    """校验字符串是否为合法 ULID（严格 Crockford Base32 字符集）。

    只做格式校验（26 字符、严格 Crockford Base32），不检查是否存在于磁盘。

    严格 Crockford Base32 字符集（大小写不敏感）：
        0-9, A-H, J-N, P-T, V-Z（共 32 个符号）
    明确排除：I, L, O, U（视觉歧义，ULID 规范不允许，不做 auto-correct）

    参数：
        s : 任意对象；非 str 类型直接返回 False，不抛异常

    返回：
        True  — 合法 ULID（26 字符，严格字符集）
        False — 格式非法（含空字符串、None、长度错误、含 I/L/O/U 等）
    """
    if not isinstance(s, str):
        return False
    return bool(_ULID_RE.match(s))


def parse_ulid_timestamp(s: str) -> datetime:
    """从 ULID 提取生成时间（UTC-aware datetime）。

    实现：从 ULID 前 10 字符（Crockford Base32 编码的 48-bit 毫秒时间戳）
    手动解码为 int，再用 datetime.fromtimestamp 构造 UTC datetime。
    不调用 ulid-py 的 Timestamp.datetime（内部使用 deprecated utcfromtimestamp）。

    参数：
        s : 合法 ULID 字符串（26 字符）

    返回：
        datetime（tzinfo=timezone.utc），精度毫秒

    Raises：
        ValueError : s 不是合法 ULID（格式校验失败）
    """
    if not validate_ulid(s):
        raise ValueError(f"非合法 ULID，无法解析时间戳：{s!r}")

    try:
        u = _ulid_default.from_str(s)
    except Exception as exc:
        raise ValueError(f"非合法 ULID，无法解析时间戳：{s!r}") from exc

    # 从时间戳的毫秒整数构造 UTC datetime（避免 deprecated utcfromtimestamp）
    ts_ms: int = u.timestamp().int
    return datetime.fromtimestamp(ts_ms / 1000.0, tz=timezone.utc)
