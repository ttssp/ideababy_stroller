"""
pars.stuck.monitor — StuckMonitor：5s 采样循环 + 状态机集成（architecture §8.1）。

结论：StuckMonitor 是 I/O shell，把 probes（纯函数）+ StuckStateMachine（纯状态）
粘合成一个 5s 轮询 daemon Thread。

职责：
1. 每 5s 采样一次（SAMPLE_INTERVAL=5，唯一真相 = architecture §8.1）
2. 调用所有 probe 函数，构造 sample dict
3. 调用 SM.transition(sample)，获取新态
4. 更新 state.json.stuck_state（写 ledger）
5. 若新态 == truly_stuck → 发 SIGINT + CircuitBreaker.record_restart()
6. 若 CB 熔断 → record_human_review_needed() + 停止监控

非职责（out of scope）：
- 不决策重启逻辑（orchestrator T023 责任）
- 不处理 SIGINT 接收（T023 orchestrator 责任）
- 不实现 worker subprocess 启停（T013 已做）

设计：daemon=True，主线程退出时自动停止。
停止：调用 stop()，或主线程退出。
"""

from __future__ import annotations

import signal
import subprocess
import threading
import time
from typing import TYPE_CHECKING, Callable

from pars.logging import get_logger
from pars.stuck.probes import probe_disk_io, probe_gpu_util, probe_net_io, probe_process_cpu
from pars.stuck.state_machine import (
    SAMPLE_INTERVAL,
    CircuitBreaker,
    StuckState,
    StuckStateMachine,
)

if TYPE_CHECKING:
    from pars.orch.worker import WorkerHandle

logger = get_logger(__name__)


class StuckMonitor(threading.Thread):
    """5s 采样循环：probes → SM.transition → state.json 更新 → truly_stuck 处理。

    architecture §8.1 合规：
    - 采样周期 = SAMPLE_INTERVAL（5s）
    - 窗口样本数 = WINDOW_SAMPLES（12 × 5s = 60s）
    - 所有转移规则代理给 StuckStateMachine

    参数：
        worker       : WorkerHandle，提供 pid / proc（用于发 SIGINT）
        run_id       : 当前 run ID（写 state.json + stuck_lock 时需要）
        cb           : CircuitBreaker 实例（含初始 stuck_restart_count）
        sm           : StuckStateMachine 实例（可注入用于测试）
        on_truly_stuck : 额外回调（truly_stuck 时调用，供 orchestrator 挂钩）
    """

    daemon = True  # 主线程退出时自动停止

    def __init__(
        self,
        worker: "WorkerHandle",
        run_id: str,
        cb: CircuitBreaker | None = None,
        sm: StuckStateMachine | None = None,
        on_truly_stuck: Callable[[], None] | None = None,
    ) -> None:
        super().__init__(name=f"StuckMonitor-{run_id}", daemon=True)
        self._worker = worker
        self._run_id = run_id
        self._cb = cb if cb is not None else CircuitBreaker()
        self._sm = sm if sm is not None else StuckStateMachine()
        self._on_truly_stuck = on_truly_stuck

        # IO 快照（用于增量计算）
        self._disk_snap: dict | None = None
        self._net_snap: dict | None = None

        # 停止标志
        self._stop_event = threading.Event()

        logger.info(
            "StuckMonitor 初始化",
            extra={"run_id": run_id, "restart_count": self._cb.stuck_restart_count},
        )

    # ---------------------------------------------------------------------------
    # 外部 API
    # ---------------------------------------------------------------------------

    def stop(self) -> None:
        """请求 monitor 停止（设置停止标志，Thread 在下次 sleep 结束后退出）。"""
        self._stop_event.set()

    # ---------------------------------------------------------------------------
    # Thread 主循环
    # ---------------------------------------------------------------------------

    def run(self) -> None:
        """5s 采样循环（daemon Thread 主体）。"""
        logger.info("StuckMonitor 启动", extra={"run_id": self._run_id})

        while not self._stop_event.is_set():
            try:
                self._tick()
            except Exception as exc:
                logger.error(
                    "StuckMonitor._tick 未捕获异常",
                    exc_info=exc,
                    extra={"run_id": self._run_id},
                )
            # 等待下次采样（interruptible：_stop_event.wait 替代 sleep）
            self._stop_event.wait(timeout=SAMPLE_INTERVAL)

        logger.info("StuckMonitor 已停止", extra={"run_id": self._run_id})

    # ---------------------------------------------------------------------------
    # 单次采样 tick
    # ---------------------------------------------------------------------------

    def _tick(self) -> None:
        """单次 probe → SM.transition → state.json → 副作用处理。"""
        pid = self._worker.pid

        # -- 采样 --
        gpu = probe_gpu_util()
        cpu = probe_process_cpu(pid=pid)
        disk_delta_mbs, new_disk_snap = probe_disk_io(prev=self._disk_snap)
        net_delta_mbs, new_net_snap = probe_net_io(prev=self._net_snap)

        # 更新快照（供下次增量）
        self._disk_snap = new_disk_snap or None
        self._net_snap = new_net_snap or None

        sample = {
            "gpu": gpu,
            "cpu": cpu,
            "disk_delta_mbs": disk_delta_mbs,
            "net_delta_mbs": net_delta_mbs,
        }

        logger.debug(
            "StuckMonitor sample",
            extra={
                "pid": pid,
                "gpu": gpu,
                "cpu": cpu,
                "disk_mbs": round(disk_delta_mbs, 3),
                "net_mbs": round(net_delta_mbs, 3),
            },
        )

        # -- 状态机转移 --
        new_state = self._sm.transition(sample)

        # -- 写 state.json --
        self._write_stuck_state(new_state)

        # -- truly_stuck 处理 --
        if new_state == StuckState.TRULY_STUCK:
            self._handle_truly_stuck()

    def _write_stuck_state(self, state: StuckState) -> None:
        """将当前 stuck_state 写入 state.json（architecture §8 契约）。"""
        try:
            from pars.ledger.state import update_state
            update_state(self._run_id, stuck_state=state.value)
        except Exception as exc:
            logger.error(
                "StuckMonitor: 写 state.json 失败",
                exc_info=exc,
                extra={"run_id": self._run_id},
            )

    def _handle_truly_stuck(self) -> None:
        """truly_stuck 处理：发 SIGINT + CircuitBreaker 计数 + 熔断检查。

        architecture §8.5：
        1. 发 SIGINT 给 worker
        2. record_restart()
        3. 若 CB 熔断 → record_human_review_needed() + 停止 monitor
        """
        logger.warning(
            "truly_stuck 触发 → 发 SIGINT",
            extra={"run_id": self._run_id, "pid": self._worker.pid},
        )

        # 发 SIGINT 给 worker 进程
        try:
            self._worker.proc.send_signal(signal.SIGINT)
        except (ProcessLookupError, OSError) as exc:
            logger.warning(
                "_handle_truly_stuck: 发 SIGINT 失败（进程已死？）",
                exc_info=exc,
                extra={"run_id": self._run_id},
            )

        # 通知外部回调（orchestrator 可监听）
        if self._on_truly_stuck is not None:
            try:
                self._on_truly_stuck()
            except Exception as exc:
                logger.error(
                    "_handle_truly_stuck: on_truly_stuck 回调异常",
                    exc_info=exc,
                )

        # 记录本次 restart
        self._cb.record_restart()

        # 检查熔断
        if not self._cb.should_restart():
            logger.error(
                "CircuitBreaker 熔断，需人工干预",
                extra={"run_id": self._run_id, "count": self._cb.stuck_restart_count},
            )
            self._cb.record_human_review_needed(run_id=self._run_id)
            # 停止 monitor（不再继续循环，等人工 pars unlock）
            self.stop()
