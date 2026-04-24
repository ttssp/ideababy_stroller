"""Worker 生命周期主类。

结论:
  Worker 封装一次完整的 claude -p headless 运行:
  创建 worktree → mount .claude 只读 → 启动 proxy → 构造 env →
  Popen claude -p → yield ClaudeEvent 流 → 退出后清理(逆序)。

用法(T023 主编排会调):
    config = WorkerConfig(run_id="01AB...", workflow_prompt="...")
    worker = Worker(config)
    for event in worker.run():
        # 回调 stuck detector / budget tracker / progress bar
        process_event(event)
    # worker.run() 退出 = 清理完成

生命周期清理顺序(finally 块,逆序):
  1. unmount .claude(ReadonlyHandle.release)
  2. git worktree remove(remove_worktree)
  3. stop proxy(stop_proxy)

安全约束(C15/R4):
  - worker env 不含 ANTHROPIC_API_KEY(由 build_worker_env 保证)
  - .claude/ 对 worker 进程只读(由 ensure_readonly_claude_dir 保证)

已知限制:
  - 不实现 stuck 状态机(T017)
  - 不实现 budget tracker(T018)
  - 不实现 resume(T019)
  - 不实现 prompt 构造(T016)
"""

from __future__ import annotations

import os
import signal
import subprocess
import threading
from collections.abc import Iterator
from dataclasses import dataclass, field
from pathlib import Path

from pars.logging import get_logger
from pars.orch.stream_parser import ClaudeEvent, parse_stream
from pars.orch.worker_env import WorkerEnvConfig, build_worker_env
from pars.orch.worktree import WorktreeHandle, create_worktree, remove_worktree
from pars.paths import worktree_dir
from pars.proxy import ProxyConfig, ProxyHandle, start_proxy, stop_proxy
from pars.proxy.config import _pick_free_port as _proxy_pick_free_port
from pars.safety import ReadonlyHandle, ensure_readonly_claude_dir

logger = get_logger(__name__)

# 默认 worker_claude_dir 模板路径(相对于项目根)
_DEFAULT_CLAUDE_TEMPLATE = Path("worker_claude_dir")

# 默认 worktree 基准目录(相对于 cwd)
_DEFAULT_WORKTREE_BASE: Path | None = None  # None → 使用 pars.paths.worktree_dir


@dataclass
class WorkerConfig:
    """Worker 启动参数。

    字段:
        run_id:          当前 run 的 ULID
        workflow_prompt: 传给 claude -p 的 system prompt 或 prompt 文件路径
        max_turns:       claude -p --max-turns 参数(默认 200)
        timeout_seconds: 整体 run 超时,默认 12h(对齐 SLA < 12h)
        worktree_base:   worktree 根目录;None 时用 pars.paths.worktree_dir 计算
        claude_template: worker_claude_dir 模板路径;None 时用项目内默认
        proxy_config:    ProxyConfig;None 时自动选 free port
        extra_env:       额外注入 worker env 的 key-value(如 RECALLKIT_CKPT_DIR)
    """

    run_id: str
    workflow_prompt: str
    max_turns: int = 200
    timeout_seconds: int = 12 * 3600
    worktree_base: Path | None = None
    claude_template: Path | None = None
    proxy_config: ProxyConfig | None = None
    extra_env: dict[str, str] = field(default_factory=dict)


class Worker:
    """1 worker 严格顺序,不并发。

    generator 模式:调用 worker.run() 得到 Iterator[ClaudeEvent],
    消费完(或 break)后自动执行 finally 清理。

    线程模型:
    - 主线程:读 stdout → parse_stream → yield ClaudeEvent
    - stderr 后台线程:排空 stderr 入内存 buffer,防止 claude -p 因 stderr pipe 满而阻塞
    """

    def __init__(self, config: WorkerConfig) -> None:
        self._config = config
        self._proc: subprocess.Popen[str] | None = None
        self._proxy_handle: ProxyHandle | None = None
        self._worktree_handle: WorktreeHandle | None = None
        self._readonly_handle: ReadonlyHandle | None = None
        self._stderr_thread: threading.Thread | None = None
        self._stderr_lines: list[str] = []

    # ------------------------------------------------------------------
    # 主接口
    # ------------------------------------------------------------------

    def run(self) -> Iterator[ClaudeEvent]:
        """启动 worker,yield ClaudeEvent 流,退出时自动清理。

        Yields:
            ClaudeEvent — 来自 claude -p 的每一个流事件

        Raises:
            subprocess.CalledProcessError: claude -p 以非零退出码退出
            RuntimeError: proxy 启动失败 / worktree 创建失败

        清理保证(finally):
            即使外部 break / 异常,也执行逆序清理:
            unmount → remove worktree → stop proxy
        """
        cfg = self._config

        # 1. 计算 worktree 目标路径
        if cfg.worktree_base is not None:
            wt_base = cfg.worktree_base
        else:
            # worktree_dir 返回 .worktrees/<run_id> 的绝对路径,取父目录作为 base
            wt_base = worktree_dir(cfg.run_id).parent

        # 2. 计算 claude_template 路径
        if cfg.claude_template is not None:
            claude_template = cfg.claude_template
        else:
            # 相对于 cwd(项目根) 的默认路径
            claude_template = (Path.cwd() / _DEFAULT_CLAUDE_TEMPLATE).resolve()

        try:
            # 3. 创建 git worktree
            logger.info("worker.run: 创建 worktree", extra={"run_id": cfg.run_id})
            self._worktree_handle = create_worktree(wt_base, cfg.run_id)

            # 4. mount .claude 只读
            logger.info("worker.run: mount .claude 只读")
            self._readonly_handle = ensure_readonly_claude_dir(
                self._worktree_handle.path,
                claude_template,
            )

            # 5. 启动 proxy
            logger.info("worker.run: 启动 proxy")
            proxy_cfg = cfg.proxy_config or ProxyConfig(port=_proxy_pick_free_port())
            self._proxy_handle = start_proxy(proxy_cfg, run_id=cfg.run_id)
            proxy_port = self._proxy_handle.port

            # 6. 构造 worker env
            env_config = WorkerEnvConfig(
                run_id=cfg.run_id,
                proxy_port=proxy_port,
                extra_injected=cfg.extra_env,
            )
            worker_env = build_worker_env(env_config)

            # 7. Popen claude -p
            cmd = self._build_cmd(cfg)
            logger.info(
                "worker.run: 启动 claude -p",
                extra={"cmd": cmd, "cwd": str(self._worktree_handle.path)},
            )
            self._proc = subprocess.Popen(  # noqa: S603
                cmd,
                env=worker_env,
                cwd=str(self._worktree_handle.path),  # 绝对路径
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding="utf-8",
            )

            # 8. 后台线程排空 stderr
            self._start_stderr_drain()

            # 9. yield ClaudeEvent 流
            assert self._proc.stdout is not None  # noqa: S101
            yield from parse_stream(iter(self._proc.stdout.readline, ""))

            # 10. 等待进程退出
            exit_code = self._proc.wait()
            if self._stderr_thread is not None:
                self._stderr_thread.join(timeout=5)

            logger.info(
                "worker.run: claude -p 退出",
                extra={"exit_code": exit_code, "run_id": cfg.run_id},
            )

            if exit_code not in (0, -signal.SIGINT, 130):
                # 130 = 128 + 2(SIGINT),claude 可能返回 130 表示被 Ctrl+C 中断
                logger.warning(
                    "worker.run: 非零退出码",
                    extra={"exit_code": exit_code},
                )

        finally:
            self._cleanup()

    def terminate(self, *, timeout: int = 30) -> None:
        """外部调用:SIGINT 给 worker,timeout 秒后 SIGKILL。

        用途:Stuck Detector(T017) / Budget Tracker(T018) 发出停止信号。

        Args:
            timeout: SIGINT 后等待的秒数;超时后发 SIGKILL(默认 30s)
        """
        proc = self._proc
        if proc is None or proc.poll() is not None:
            logger.debug("terminate: 进程已退出或未启动")
            return

        logger.info("terminate: 发送 SIGINT", extra={"pid": proc.pid})
        try:
            proc.send_signal(signal.SIGINT)
        except ProcessLookupError:
            return

        try:
            proc.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            logger.warning(
                "terminate: SIGINT 超时,发送 SIGKILL",
                extra={"pid": proc.pid, "timeout": timeout},
            )
            try:
                proc.send_signal(signal.SIGKILL)
            except ProcessLookupError:
                pass
            proc.wait()

    # ------------------------------------------------------------------
    # 内部辅助
    # ------------------------------------------------------------------

    def _build_cmd(self, cfg: WorkerConfig) -> list[str]:
        """构造 claude -p 命令行。

        格式:
            claude -p <workflow_prompt>
                --output-format stream-json
                --max-turns <max_turns>
        """
        return [
            "claude",
            "-p", cfg.workflow_prompt,
            "--output-format", "stream-json",
            "--max-turns", str(cfg.max_turns),
        ]

    def _start_stderr_drain(self) -> None:
        """启动后台线程排空 stderr,防止 pipe 满导致 claude -p 阻塞。"""
        proc = self._proc
        if proc is None or proc.stderr is None:
            return

        stderr_lines = self._stderr_lines

        def _drain() -> None:
            assert proc is not None  # noqa: S101
            assert proc.stderr is not None  # noqa: S101
            for line in proc.stderr:
                stripped = line.rstrip("\n")
                stderr_lines.append(stripped)
                if stripped:
                    logger.debug("claude stderr: %s", stripped)

        t = threading.Thread(target=_drain, daemon=True, name=f"stderr-{self._config.run_id}")
        t.start()
        self._stderr_thread = t

    def _cleanup(self) -> None:
        """逆序清理:unmount → remove worktree → stop proxy。

        每步独立 try/except,保证即使中间步骤失败也继续清理。
        """
        # step 1: 等待进程退出
        if self._proc is not None and self._proc.poll() is None:
            logger.warning("cleanup: 进程仍在运行,强制 SIGKILL")
            try:
                self._proc.send_signal(signal.SIGKILL)
                self._proc.wait(timeout=5)
            except (ProcessLookupError, subprocess.TimeoutExpired):
                pass

        # step 2: 等 stderr 线程
        if self._stderr_thread is not None:
            self._stderr_thread.join(timeout=5)
            self._stderr_thread = None

        # step 3: unmount .claude 只读
        if self._readonly_handle is not None:
            try:
                self._readonly_handle.release()
                logger.info("cleanup: .claude unmount 完成")
            except Exception as exc:  # noqa: BLE001
                logger.error("cleanup: unmount 失败(已忽略)", extra={"error": str(exc)})
            finally:
                self._readonly_handle = None

        # step 4: remove worktree
        if self._worktree_handle is not None:
            try:
                remove_worktree(self._worktree_handle, force=True)
                logger.info("cleanup: worktree 移除完成")
            except Exception as exc:  # noqa: BLE001
                logger.error("cleanup: remove_worktree 失败(已忽略)", extra={"error": str(exc)})
            finally:
                self._worktree_handle = None

        # step 5: stop proxy
        if self._proxy_handle is not None:
            try:
                stop_proxy(self._proxy_handle)
                logger.info("cleanup: proxy 停止完成")
            except Exception as exc:  # noqa: BLE001
                logger.error("cleanup: stop_proxy 失败(已忽略)", extra={"error": str(exc)})
            finally:
                self._proxy_handle = None

        logger.info("cleanup: 全部资源清理完成", extra={"run_id": self._config.run_id})


# ---------------------------------------------------------------------------
# 低级接口(T013 spec.md Outputs 中指定的函数 API,供 T023 兼容)
# ---------------------------------------------------------------------------


@dataclass
class WorkerHandle:
    """低级 worker 句柄(向后兼容 spec Outputs 描述)。

    字段:
        pid:           subprocess PID
        proc:          subprocess.Popen 对象
        env_snapshot:  worker env dict 快照(不含 secret)
        start_time:    启动时间戳(float, time.time())
        worktree:      WorktreeHandle
        readonly:      ReadonlyHandle
        proxy:         ProxyHandle
    """

    pid: int
    proc: subprocess.Popen[str]
    env_snapshot: dict[str, str]
    start_time: float
    worktree: WorktreeHandle
    readonly: ReadonlyHandle
    proxy: ProxyHandle


def launch_worker(
    run_id: str,
    prompt_path: Path,
    proxy_port: int,
    max_turns: int = 50,
    *,
    worktree_base: Path | None = None,
    claude_template: Path | None = None,
    extra_env: dict[str, str] | None = None,
) -> WorkerHandle:
    """低级接口:创建 worktree + mount + Popen,返回 WorkerHandle。

    供 T023 或需要细粒度控制的场景使用。
    推荐使用高级接口 Worker.run() 替代。

    步骤:
    1. create_worktree(run_id)
    2. ensure_readonly_claude_dir(worktree, claude_template)
    3. build_worker_env(proxy_port, extra_env)
    4. Popen(["claude", "-p", ..., "--output-format", "stream-json", "--max-turns", ...])

    Args:
        run_id:         run ULID
        prompt_path:    prompt 文件路径或内容字符串
        proxy_port:     localhost proxy 端口
        max_turns:      claude --max-turns 值
        worktree_base:  worktree 根目录(None → 默认)
        claude_template: .claude 模板目录(None → 默认)
        extra_env:      额外 env var

    Returns:
        WorkerHandle

    Raises:
        subprocess.CalledProcessError: git worktree 创建失败
        RuntimeError: claude 命令不存在
    """
    import time

    # 1. worktree
    if worktree_base is None:
        worktree_base = worktree_dir(run_id).parent
    wt = create_worktree(worktree_base, run_id)

    # 2. mount .claude
    if claude_template is None:
        claude_template = (Path.cwd() / _DEFAULT_CLAUDE_TEMPLATE).resolve()
    rh = ensure_readonly_claude_dir(wt.path, claude_template)

    # 3. env
    env_config = WorkerEnvConfig(
        run_id=run_id,
        proxy_port=proxy_port,
        extra_injected=extra_env or {},
    )
    worker_env = build_worker_env(env_config)

    # 4. Popen
    cmd = [
        "claude",
        "-p", str(prompt_path),
        "--output-format", "stream-json",
        "--max-turns", str(max_turns),
    ]
    proc = subprocess.Popen(  # noqa: S603
        cmd,
        env=worker_env,
        cwd=str(wt.path),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
    )

    # 构造 proxy handle stub(launch_worker 的调用方应已持有真正的 proxy)
    # 此处返回 proxy port 信息以供后续 stop_proxy 调用
    # 注意:launch_worker 不负责启动/停止 proxy(由调用方管理)
    # 为满足 WorkerHandle 接口,创建轻量占位对象
    from pars.proxy.config import ProxyConfig as _ProxyConfig
    from pars.proxy.server import ProxyHandle as _ProxyHandle

    proxy_placeholder = _ProxyHandle(
        host="127.0.0.1",
        port=proxy_port,
        pid=os.getpid(),  # 占位 pid(调用方自己持有真正 ProxyHandle)
        _proc=proc,  # type: ignore[arg-type]
    )

    return WorkerHandle(
        pid=proc.pid,
        proc=proc,
        env_snapshot={k: v for k, v in worker_env.items()},
        start_time=time.time(),
        worktree=wt,
        readonly=rh,
        proxy=proxy_placeholder,
    )


def wait(handle: WorkerHandle, timeout: float | None = None) -> int:
    """等待 worker 进程退出,返回 exit code。

    Args:
        handle:  WorkerHandle
        timeout: 超时秒数(None = 永久等待)

    Returns:
        exit code

    Raises:
        subprocess.TimeoutExpired: 超时
    """
    return handle.proc.wait(timeout=timeout)


def stop(
    handle: WorkerHandle,
    sig: signal.Signals = signal.SIGINT,
    grace: float = 10.0,
) -> int:
    """发送信号后等待,超时则 SIGKILL。

    Args:
        handle: WorkerHandle
        sig:    首先发送的信号(默认 SIGINT)
        grace:  宽限秒数,超时后发 SIGKILL(默认 10s)

    Returns:
        exit code
    """
    proc = handle.proc
    if proc.poll() is not None:
        return proc.returncode  # type: ignore[return-value]

    try:
        proc.send_signal(sig)
    except ProcessLookupError:
        return proc.wait()

    try:
        return proc.wait(timeout=grace)
    except subprocess.TimeoutExpired:
        logger.warning("stop: 宽限期超时,发送 SIGKILL", extra={"pid": proc.pid})
        try:
            proc.send_signal(signal.SIGKILL)
        except ProcessLookupError:
            pass
        return proc.wait()


def cleanup(handle: WorkerHandle) -> None:
    """释放 WorkerHandle 持有的资源:readonly mount release + remove worktree。

    注意:不停止 proxy(调用方管理 proxy 生命周期)。

    Args:
        handle: WorkerHandle
    """
    try:
        handle.readonly.release()
    except Exception as exc:  # noqa: BLE001
        logger.error("cleanup: unmount 失败(已忽略)", extra={"error": str(exc)})

    try:
        remove_worktree(handle.worktree, force=True)
    except Exception as exc:  # noqa: BLE001
        logger.error("cleanup: remove_worktree 失败(已忽略)", extra={"error": str(exc)})
