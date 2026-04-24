"""
pars.proxy.config — ProxyConfig 数据类 + 端口选取工具。

结论：
  ProxyConfig 是 frozen dataclass，强制 bind_host=127.0.0.1（R4 + D10）。
  _pick_free_port 用 SO_REUSEADDR + getsockname 找可用端口，
  避免 TOCTOU 只有 socket bind 测试后立即释放的窗口（v0.1 接受低概率冲突）。

安全约束：
  bind_host 白名单仅 "127.0.0.1"；传入任何其他值立即 raise ValueError。
  这是唯一的 bind 检查点，不允许运行时绕过。
"""

from __future__ import annotations

import socket
from dataclasses import dataclass, field
from pathlib import Path


# ---------------------------------------------------------------------------
# 端口选取
# ---------------------------------------------------------------------------


def _pick_free_port(low: int = 8000, high: int = 9000) -> int:
    """找一个在 [low, high) 范围内可 bind 的空闲 TCP 端口。

    算法：
      对 low..high 逐一尝试 bind(AF_INET, SOCK_STREAM)；
      第一个成功的端口立即关闭 socket 并返回端口号。

    TOCTOU 注意：
      bind 测试到实际 listen 之间有短暂窗口，极低概率被抢占。
      v0.1 接受此风险（单机单 worker 场景）。

    Raises:
        RuntimeError: [low, high) 范围内无空闲端口（罕见，端口耗尽场景）
    """
    for port in range(low, high):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.bind(("127.0.0.1", port))
                return port
        except OSError:
            continue
    raise RuntimeError(f"[{low}, {high}) 范围内无可用端口")


# ---------------------------------------------------------------------------
# 白名单
# ---------------------------------------------------------------------------

_ALLOWED_BIND_HOSTS: frozenset[str] = frozenset({"127.0.0.1"})
"""仅允许本地回环地址（R4 安全约束）。"""

_DEFAULT_ENDPOINTS: list[str] = ["/v1/messages", "/v1/messages/count_tokens"]
"""Proxy 放行的 Anthropic API 端点白名单（v0.1 最小集）。"""


# ---------------------------------------------------------------------------
# ProxyConfig
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ProxyConfig:
    """localhost proxy 配置。

    frozen=True：防止运行时修改 host/port 等安全关键字段。

    字段：
        bind_host:         proxy 绑定地址，必须是 "127.0.0.1"（R4 约束）
        port:              proxy 监听端口（由调用方传入或 _pick_free_port 获取）
        allowed_endpoints: 放行的端点路径列表（默认 /v1/messages 等）
        log_path:          audit log JSONL 路径（None = 不写 audit log）
    """

    port: int
    bind_host: str = "127.0.0.1"
    allowed_endpoints: list[str] = field(default_factory=lambda: list(_DEFAULT_ENDPOINTS))
    log_path: Path | None = None

    def __post_init__(self) -> None:
        """校验 bind_host 白名单约束（post-init 因 frozen=True 无法在 __init__ 之后改）。"""
        if self.bind_host not in _ALLOWED_BIND_HOSTS:
            raise ValueError(
                f"bind_host 必须是 127.0.0.1，拒绝 {self.bind_host!r}。"
                f"R4 约束：proxy 只允许 localhost bind，禁止 LAN 暴露。"
            )
