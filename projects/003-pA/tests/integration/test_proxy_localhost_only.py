"""
tests.integration.test_proxy_localhost_only — D10/R4 localhost bind 验证。

结论：
  ProxyConfig 的 bind_host 白名单检查覆盖了 0.0.0.0 和 LAN IP。
  实际网络 bind 测试通过 server.py start_proxy 完成（需 LiteLLM 可用）。

测试策略：
  Unit-level: config 层拒绝非 127.0.0.1
  Integration-level: mock subprocess 验证启动命令含 --host 127.0.0.1
"""

from __future__ import annotations

import subprocess
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from pars.proxy.config import ProxyConfig, _pick_free_port
from pars.proxy.server import ProxyHandle, start_proxy, stop_proxy


# ---------------------------------------------------------------------------
# 1. Config 层：非 127.0.0.1 被拒绝（R4 白名单）
# ---------------------------------------------------------------------------


@pytest.mark.integration
def test_proxy_config_rejects_all_non_localhost_hosts() -> None:
    """should reject any non-127.0.0.1 bind_host at config creation time."""
    non_local_hosts = ["0.0.0.0", "192.168.0.1", "10.0.0.1", "::1", "localhost"]
    for host in non_local_hosts:
        with pytest.raises(ValueError, match="127.0.0.1|localhost|bind"):
            ProxyConfig(bind_host=host, port=8765)


@pytest.mark.integration
def test_proxy_config_accepts_only_127_0_0_1() -> None:
    """should accept 127.0.0.1 as the only valid bind_host."""
    cfg = ProxyConfig(bind_host="127.0.0.1", port=8765)
    assert cfg.bind_host == "127.0.0.1"


# ---------------------------------------------------------------------------
# 2. start_proxy：subprocess 命令包含 --host 127.0.0.1
# ---------------------------------------------------------------------------


@pytest.mark.integration
def test_start_proxy_command_binds_to_localhost(tmp_path: Path) -> None:
    """should pass --host 127.0.0.1 to LiteLLM subprocess."""
    port = _pick_free_port()
    log_path = tmp_path / "api_log.jsonl"
    cfg = ProxyConfig(port=port, log_path=log_path)

    # mock subprocess.Popen 避免真实启动 LiteLLM
    mock_proc = MagicMock()
    mock_proc.pid = 99999
    mock_proc.poll.return_value = None  # 进程未退出

    captured_cmd: list[str] = []

    def fake_popen(cmd: list[str], **kwargs: object) -> MagicMock:
        captured_cmd.extend(cmd)
        return mock_proc

    # mock 健康检查，模拟 proxy 已就绪
    mock_response = MagicMock()
    mock_response.status_code = 200

    with (
        patch("pars.proxy.server.subprocess.Popen", side_effect=fake_popen),
        patch("pars.proxy.server.httpx.get", return_value=mock_response),
    ):
        handle = start_proxy(cfg)

    try:
        # 关键断言：命令中包含 --host 127.0.0.1
        cmd_str = " ".join(captured_cmd)
        assert "--host" in cmd_str, f"启动命令缺少 --host：{cmd_str}"
        assert "127.0.0.1" in cmd_str, f"启动命令缺少 127.0.0.1：{cmd_str}"
        assert str(port) in cmd_str, f"启动命令缺少端口 {port}：{cmd_str}"
    finally:
        with patch("pars.proxy.server.subprocess.Popen", side_effect=fake_popen):
            stop_proxy(handle)


# ---------------------------------------------------------------------------
# 3. ProxyHandle 包含正确的 host/port
# ---------------------------------------------------------------------------


@pytest.mark.integration
def test_start_proxy_returns_handle_with_correct_host_port(tmp_path: Path) -> None:
    """should return ProxyHandle with host=127.0.0.1 and the configured port."""
    port = _pick_free_port()
    cfg = ProxyConfig(port=port)

    mock_proc = MagicMock()
    mock_proc.pid = 12345
    mock_proc.poll.return_value = None

    mock_response = MagicMock()
    mock_response.status_code = 200

    with (
        patch("pars.proxy.server.subprocess.Popen", return_value=mock_proc),
        patch("pars.proxy.server.httpx.get", return_value=mock_response),
    ):
        handle = start_proxy(cfg)

    assert handle.host == "127.0.0.1"
    assert handle.port == port
    assert handle.pid == 12345

    stop_proxy(handle)
