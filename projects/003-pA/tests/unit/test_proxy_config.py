"""
tests.unit.test_proxy_config — ProxyConfig 单元测试。

结论：
  覆盖 bind_host 校验（非 127.0.0.1 → ValueError）、端口范围、
  allowed_endpoints 默认值、_pick_free_port 可用性共 ≥ 5 个场景。
"""

from __future__ import annotations

import socket

import pytest

from pars.proxy.config import ProxyConfig, _pick_free_port


# ---------------------------------------------------------------------------
# 1. _pick_free_port：返回可 bind 的端口
# ---------------------------------------------------------------------------


@pytest.mark.unit
def test_pick_free_port_returns_int_in_range() -> None:
    """should return an integer port in [low, high) range."""
    port = _pick_free_port(low=8000, high=9000)
    assert isinstance(port, int)
    assert 8000 <= port < 9000


@pytest.mark.unit
def test_pick_free_port_is_actually_bindable() -> None:
    """should return a port that can be immediately bound."""
    port = _pick_free_port()
    # 验证端口真的可 bind
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("127.0.0.1", port))  # 不 raise → 端口可用


# ---------------------------------------------------------------------------
# 2. ProxyConfig：bind_host 必须是 127.0.0.1
# ---------------------------------------------------------------------------


@pytest.mark.unit
def test_proxy_config_default_bind_host_is_localhost() -> None:
    """should default bind_host to 127.0.0.1."""
    cfg = ProxyConfig(port=8765)
    assert cfg.bind_host == "127.0.0.1"


@pytest.mark.unit
def test_proxy_config_rejects_non_localhost_bind_host() -> None:
    """should raise ValueError when bind_host is not 127.0.0.1."""
    with pytest.raises(ValueError, match="127.0.0.1|localhost|bind"):
        ProxyConfig(bind_host="0.0.0.0", port=8765)


@pytest.mark.unit
def test_proxy_config_rejects_lan_ip_bind_host() -> None:
    """should raise ValueError when bind_host is a LAN IP."""
    with pytest.raises(ValueError, match="127.0.0.1|localhost|bind"):
        ProxyConfig(bind_host="192.168.1.100", port=8765)


@pytest.mark.unit
def test_proxy_config_explicit_localhost_is_accepted() -> None:
    """should accept explicit 127.0.0.1 bind_host."""
    cfg = ProxyConfig(bind_host="127.0.0.1", port=8765)
    assert cfg.bind_host == "127.0.0.1"


# ---------------------------------------------------------------------------
# 3. allowed_endpoints 默认值
# ---------------------------------------------------------------------------


@pytest.mark.unit
def test_proxy_config_default_allowed_endpoints() -> None:
    """should include /v1/messages in default allowed_endpoints."""
    cfg = ProxyConfig(port=8765)
    assert "/v1/messages" in cfg.allowed_endpoints


@pytest.mark.unit
def test_proxy_config_allowed_endpoints_includes_count_tokens() -> None:
    """should include /v1/messages/count_tokens in default allowed_endpoints."""
    cfg = ProxyConfig(port=8765)
    assert "/v1/messages/count_tokens" in cfg.allowed_endpoints


# ---------------------------------------------------------------------------
# 4. ProxyConfig log_path
# ---------------------------------------------------------------------------


@pytest.mark.unit
def test_proxy_config_has_log_path(tmp_path: object) -> None:
    """should accept a log_path for audit log JSONL."""
    from pathlib import Path

    log_path = Path(str(tmp_path)) / "api_log.jsonl"  # type: ignore[arg-type]
    cfg = ProxyConfig(port=8765, log_path=log_path)
    assert cfg.log_path == log_path


# ---------------------------------------------------------------------------
# 5. ProxyConfig 是 frozen（不可变）
# ---------------------------------------------------------------------------


@pytest.mark.unit
def test_proxy_config_is_frozen() -> None:
    """should be immutable so port/host cannot be accidentally changed."""
    cfg = ProxyConfig(port=8765)
    with pytest.raises((AttributeError, TypeError)):
        cfg.port = 9999  # type: ignore[misc]
