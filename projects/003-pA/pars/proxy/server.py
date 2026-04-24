"""
pars.proxy.server — LiteLLM localhost proxy 启动/停止管理。

结论：
  `start_proxy` 以 subprocess 形式启动 LiteLLM CLI（litellm --host 127.0.0.1 --port <port>），
  返回 `ProxyHandle`（含 pid/port/stop）。
  `stop_proxy` 先 SIGTERM + 等待 5s，再 SIGKILL（保证子进程清理）。

安全约束（R4 / D10）：
  - 强制 --host 127.0.0.1（来自 ProxyConfig.bind_host，已在 config 层校验）
  - proxy 继承 env（持有 ANTHROPIC_API_KEY），worker 子进程 env 不得持 key
  - stderr 重定向到 runs/<id>/artifacts/proxy.err.log（防止 key 泄漏到 stdout）

健康检查：
  启动后轮询 GET http://127.0.0.1:<port>/health，最多等 5s（10 × 500ms）。
  若超时 → raise RuntimeError（调用方决定 fallback 或 abort）。

LiteLLM 配置（config.yaml）：
  临时 yaml 写入 runs/<id>/artifacts/litellm_config.yaml，格式：
    model_list:
      - model_name: claude-sonnet-4-6
        litellm_params:
          model: anthropic/claude-sonnet-4-6
          api_key: os.environ/ANTHROPIC_API_KEY
    general_settings:
      master_key: ""
      disable_request_tracking: true
"""

from __future__ import annotations

import os
import signal
import subprocess
import tempfile
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import IO, Any

import httpx

from pars.logging import get_logger
from pars.proxy.config import ProxyConfig

logger = get_logger(__name__)

# LiteLLM config YAML 模板（版本 1.50.x 兼容格式）
_LITELLM_CONFIG_TEMPLATE = """\
model_list:
  - model_name: claude-opus-4-7
    litellm_params:
      model: anthropic/claude-opus-4-7
      api_key: os.environ/ANTHROPIC_API_KEY
  - model_name: claude-sonnet-4-6
    litellm_params:
      model: anthropic/claude-sonnet-4-6
      api_key: os.environ/ANTHROPIC_API_KEY
  - model_name: claude-haiku-4-5
    litellm_params:
      model: anthropic/claude-haiku-4-5
      api_key: os.environ/ANTHROPIC_API_KEY
general_settings:
  master_key: ""
  disable_request_tracking: true
"""

_HEALTH_CHECK_RETRIES = 10
_HEALTH_CHECK_INTERVAL_S = 0.5
_STOP_SIGTERM_WAIT_S = 5.0


# ---------------------------------------------------------------------------
# Handle 数据类
# ---------------------------------------------------------------------------


@dataclass
class ProxyHandle:
    """LiteLLM proxy 进程的句柄。

    字段：
        host:       proxy 绑定地址（必须是 "127.0.0.1"）
        port:       proxy 监听端口
        pid:        subprocess PID
        _proc:      subprocess.Popen 对象（内部使用）
        _config_path: 临时 yaml 配置文件路径（stop 时清理）
    """

    host: str
    port: int
    pid: int
    _proc: subprocess.Popen[bytes] = field(repr=False)
    _config_path: Path | None = field(default=None, repr=False)

    def is_alive(self) -> bool:
        """返回 proxy 进程是否仍在运行。"""
        return self._proc.poll() is None


# ---------------------------------------------------------------------------
# 辅助：生成 LiteLLM config yaml
# ---------------------------------------------------------------------------


def _write_litellm_config(dest: Path) -> None:
    """将 LiteLLM config yaml 写入 dest 路径。"""
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(_LITELLM_CONFIG_TEMPLATE, encoding="utf-8")


# ---------------------------------------------------------------------------
# 主函数
# ---------------------------------------------------------------------------


def start_proxy(cfg: ProxyConfig, run_id: str | None = None) -> ProxyHandle:
    """启动 LiteLLM proxy subprocess，返回 ProxyHandle。

    步骤：
    1. 生成临时 litellm config.yaml
    2. 构造命令：litellm --host 127.0.0.1 --port <port> --config <yaml>
    3. subprocess.Popen 启动（继承 env 持有 ANTHROPIC_API_KEY）
    4. 健康检查：轮询 /health，最多 5s

    Args:
        cfg:    ProxyConfig（bind_host 必须是 127.0.0.1，已在 config 层校验）
        run_id: 可选 run 标识（用于确定 artifacts 目录位置）

    Returns:
        ProxyHandle

    Raises:
        RuntimeError: LiteLLM 启动后 5s 内健康检查失败
        FileNotFoundError: litellm 命令不在 PATH 中
    """
    # 确定 config yaml 路径
    if run_id is not None:
        from pars.paths import run_dir as _run_dir

        artifacts_dir = _run_dir(run_id) / "artifacts"
    else:
        artifacts_dir = Path(tempfile.mkdtemp(prefix="pars_proxy_"))

    config_path = artifacts_dir / "litellm_config.yaml"
    _write_litellm_config(config_path)

    # 确定 stderr 日志路径（防止 key 泄漏到 stdout）
    err_log_path = artifacts_dir / "proxy.err.log"
    err_log_path.parent.mkdir(parents=True, exist_ok=True)

    # 构造命令（强制 --host 127.0.0.1）
    cmd = [
        "litellm",
        "--host", cfg.bind_host,  # 必须是 127.0.0.1（已在 config 层校验）
        "--port", str(cfg.port),
        "--config", str(config_path),
        "--quiet",
    ]

    logger.info(
        "启动 LiteLLM proxy",
        extra={"host": cfg.bind_host, "port": cfg.port, "config": str(config_path)},
    )

    # 打开 stderr log 文件
    err_fd: IO[bytes] = open(str(err_log_path), "wb")  # noqa: PTH123, SIM115

    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.DEVNULL,
        stderr=err_fd,
        env=os.environ.copy(),  # proxy 持有 ANTHROPIC_API_KEY
    )

    # 关闭父进程侧的 fd（子进程继承后父进程不需要持有）
    err_fd.close()

    handle = ProxyHandle(
        host=cfg.bind_host,
        port=cfg.port,
        pid=proc.pid,
        _proc=proc,
        _config_path=config_path,
    )

    # 健康检查轮询
    _wait_for_health(handle)

    return handle


def _wait_for_health(handle: ProxyHandle) -> None:
    """轮询 /health 端点，最多等 5s。

    Raises:
        RuntimeError: 超时（代理未就绪或启动失败）
    """
    url = f"http://{handle.host}:{handle.port}/health"
    for attempt in range(_HEALTH_CHECK_RETRIES):
        # 检查进程是否已崩溃
        if handle._proc.poll() is not None:
            raise RuntimeError(
                f"LiteLLM proxy 进程已退出（returncode={handle._proc.returncode}），"
                f"请检查 proxy.err.log"
            )
        try:
            resp = httpx.get(url, timeout=1.0)
            if resp.status_code == 200:
                logger.info(
                    "LiteLLM proxy 健康检查通过",
                    extra={"url": url, "attempt": attempt + 1},
                )
                return
        except (httpx.ConnectError, httpx.TimeoutException):
            pass

        time.sleep(_HEALTH_CHECK_INTERVAL_S)

    raise RuntimeError(
        f"LiteLLM proxy 健康检查超时（{_HEALTH_CHECK_RETRIES}次 × "
        f"{_HEALTH_CHECK_INTERVAL_S}s = "
        f"{_HEALTH_CHECK_RETRIES * _HEALTH_CHECK_INTERVAL_S}s）。"
        f"端口：{handle.port}，URL：{url}"
    )


def stop_proxy(handle: ProxyHandle) -> None:
    """停止 LiteLLM proxy subprocess。

    步骤：
    1. SIGTERM → 等最多 5s
    2. 若仍在运行 → SIGKILL（强制终止）
    3. 清理临时 config yaml（若存在）

    Args:
        handle: start_proxy 返回的 ProxyHandle
    """
    proc = handle._proc

    if proc.poll() is not None:
        # 进程已退出
        logger.debug("stop_proxy: 进程已退出，无需信号", extra={"pid": handle.pid})
        return

    # SIGTERM
    logger.info("发送 SIGTERM 到 proxy", extra={"pid": handle.pid})
    try:
        proc.send_signal(signal.SIGTERM)
    except ProcessLookupError:
        return

    # 等待最多 5s
    try:
        proc.wait(timeout=_STOP_SIGTERM_WAIT_S)
    except subprocess.TimeoutExpired:
        logger.warning("SIGTERM 超时，发送 SIGKILL", extra={"pid": handle.pid})
        try:
            proc.send_signal(signal.SIGKILL)
        except ProcessLookupError:
            pass
        proc.wait()

    # 清理临时 config yaml
    if handle._config_path is not None and handle._config_path.exists():
        try:
            handle._config_path.unlink()
        except OSError:
            pass

    logger.info("LiteLLM proxy 已停止", extra={"pid": handle.pid})
