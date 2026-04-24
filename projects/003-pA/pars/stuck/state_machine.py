"""
pars.stuck.state_machine — Stuck 检测状态机（architecture §8 单一真相源实现）。

=============================================================================
4 态显式转移表（architecture §8.2 invariant）
=============================================================================

  状态          → training           → downloading        → idle               → truly_stuck
  ─────────────────────────────────────────────────────────────────────────────────────────
  idle          GPU>20% 持续 30s     net>1MB/s 持续 30s   —                    停留>15min
                (6 个 5s 样本)       (6 个 5s 样本)                            且 elapsed≥300s
  training      —                    —                    GPU<5% AND           —
                                                          CPU<10% AND
                                                          disk<1MB/s
                                                          持续 60s(12 样本)
  downloading   —                    —                    net<100KB/s AND      —
                                                          disk<1MB/s
                                                          持续 60s(12 样本)
  truly_stuck   —                    —                    —                    终态(发 SIGINT)

冷启动豁免：elapsed_since_start < 300s → 禁止 truly_stuck 转移；
           全 0 信号时记录 warning "cold_start_silence_suspected_stuck"

=============================================================================

设计原则：
- 纯 Python（无 I/O）：所有外部依赖（时钟/probe 输入）通过参数注入
- 窗口使用 collections.deque(maxlen=12)（12 × 5s = 60s）
- 每次 transition() 重算：延迟由"持续 N 秒"条件本身提供
- GPU=None 时降级：忽略 GPU 信号，仅看 CPU + disk
"""

from __future__ import annotations

import time
from collections import deque
from enum import StrEnum
from typing import Callable

from pars.logging import get_logger

logger = get_logger(__name__)

# ---------------------------------------------------------------------------
# architecture §8.1 契约常量（唯一真相）
# 任何修改必须同步更新 architecture.md §8.1 并在 commit 中说明原因
# ---------------------------------------------------------------------------

#: 采样周期（秒）— §8.1：5s
SAMPLE_INTERVAL: int = 5

#: 滚动窗口样本数 — §8.1：12 × 5s = 60s
WINDOW_SAMPLES: int = 12

#: 冷启动豁免期（秒）— §8.3：0-300s 内禁止 truly_stuck
COLD_START_SECS: int = 300

#: idle → truly_stuck 阈值（秒）— §8.2：> 15min
IDLE_STUCK_SECS: int = 900  # 15 × 60

# --- 转移阈值 ---

#: idle → training：GPU 利用率严格大于此值（%）
GPU_TRAIN_PCT: float = 20.0

#: training → idle 的 GPU 低阈值（%，严格小于 5%）
GPU_IDLE_PCT: float = 5.0

#: idle → downloading：网络速率严格大于此值（MB/s = 1 MB/s）
NET_DOWNLOAD_MBS: float = 1.0

#: downloading → idle：网络速率严格小于此值（MB/s = 100 KB/s）
NET_IDLE_KBS: float = 0.1  # 100 KB/s

#: 磁盘 IO 活跃阈值（MB/s）：>= 1MB/s 视为活跃，阻止 → idle
DISK_ACTIVE_MBS: float = 1.0

#: training → idle / downloading → idle 所需持续窗口（秒 = 12 个 5s 样本）
TRAIN_IDLE_SECS: int = 60

#: idle → training / idle → downloading 所需持续窗口样本数（30s = 6 个 5s 样本）
ACTIVE_TRIGGER_SAMPLES: int = 6  # 6 × 5s = 30s


# ---------------------------------------------------------------------------
# 状态枚举
# ---------------------------------------------------------------------------


class StuckState(StrEnum):
    """4 态状态机节点（对应 architecture §8.2 转移表的行/列）。"""

    IDLE = "idle"
    TRAINING = "training"
    DOWNLOADING = "downloading"
    TRULY_STUCK = "truly_stuck"


# ---------------------------------------------------------------------------
# StuckStateMachine
# ---------------------------------------------------------------------------


class StuckStateMachine:
    """architecture §8 的 4 态 Stuck 状态机实现。

    职责：
    - 维护当前状态（idle/training/downloading/truly_stuck）
    - 每次 transition() 调用后根据样本窗口重算状态
    - 60s 滚动窗口用 deque(maxlen=12) 实现（12 × 5s）
    - 不引入任何 I/O，所有外部依赖通过参数注入

    注入点：
        clock : callable() -> float，返回单调时间（默认 time.monotonic）
                 测试时传入 lambda: fixed_value 实现 mock 时钟
    """

    def __init__(self, clock: Callable[[], float] | None = None) -> None:
        self._clock: Callable[[], float] = clock if clock is not None else time.monotonic
        self._start_time: float = self._clock()

        # 当前状态
        self._state: StuckState = StuckState.IDLE
        self._state_entered_at: float = self._start_time

        # 滚动样本窗口（deque(maxlen=12) = 60s @ 5s/sample）
        # 每个 slot = probe sample dict
        self._window: deque[dict] = deque(maxlen=WINDOW_SAMPLES)

        # 连续满足条件的样本计数（用于 30s 触发条件）
        self._consecutive_gpu_high: int = 0    # idle → training
        self._consecutive_net_high: int = 0    # idle → downloading
        self._consecutive_all_low: int = 0     # training/downloading → idle

        # 冷启动期警告
        self.warnings: list[str] = []

    # -- 属性 --

    @property
    def current_state(self) -> StuckState:
        """当前状态节点。"""
        return self._state

    @property
    def state_entered_at(self) -> float:
        """进入当前状态的时刻（单调时钟）。"""
        return self._state_entered_at

    def _elapsed_since_start(self) -> float:
        """从 SM 启动到现在的经过秒数（用于冷启动豁免判断）。"""
        return self._clock() - self._start_time

    def _idle_duration(self) -> float:
        """当前在 idle 态已停留的秒数。"""
        return self._clock() - self._state_entered_at

    def _enter_state(self, new_state: StuckState) -> None:
        """切换到新状态并记录进入时刻。"""
        if new_state != self._state:
            logger.info(
                "stuck state 转移",
                extra={"from": self._state.value, "to": new_state.value},
            )
            self._state = new_state
            self._state_entered_at = self._clock()
            # 切换状态时重置连续计数
            self._consecutive_gpu_high = 0
            self._consecutive_net_high = 0
            self._consecutive_all_low = 0

    # ---------------------------------------------------------------------------
    # 核心转移逻辑
    # ---------------------------------------------------------------------------

    def transition(self, sample: dict) -> StuckState:
        """处理一个 probe 样本，按 §8.2 规则更新状态。

        参数：
            sample : probe 快照 dict
                {
                    "gpu": float | None,      # GPU 利用率 0-100%；None 表示无 GPU
                    "cpu": float,             # 子进程 CPU% 累加
                    "disk_delta_mbs": float,  # 磁盘 IO 增量 MB/s
                    "net_delta_mbs": float,   # 网络 IO 增量 MB/s
                }

        返回：
            StuckState : 处理完本次 sample 后的当前状态
        """
        self._window.append(sample)

        gpu = sample.get("gpu")          # float | None
        cpu = sample.get("cpu", 0.0)
        disk = sample.get("disk_delta_mbs", 0.0)
        net = sample.get("net_delta_mbs", 0.0)

        current = self._state

        if current == StuckState.IDLE:
            self._handle_idle(gpu, cpu, disk, net)

        elif current == StuckState.TRAINING:
            self._handle_training(gpu, cpu, disk)

        elif current == StuckState.DOWNLOADING:
            self._handle_downloading(net, disk)

        elif current == StuckState.TRULY_STUCK:
            # 终态：不自行转移，等待 monitor 发 SIGINT
            pass

        return self._state

    # ---------------------------------------------------------------------------
    # 各态处理
    # ---------------------------------------------------------------------------

    def _handle_idle(
        self,
        gpu: float | None,
        cpu: float,
        disk: float,
        net: float,
    ) -> None:
        """idle 态：检查 → training / → downloading / → truly_stuck。

        §8.2 idle 行：
        - → training   : GPU > 20% 持续 30s（连续 6 个 5s 样本）
        - → downloading: net > 1 MB/s 持续 30s（连续 6 个 5s 样本）
        - → truly_stuck: 停留 idle > 15min 且 冷启动期已过（elapsed ≥ 300s）
        """
        # --- idle → training 计数 ---
        if gpu is not None and gpu > GPU_TRAIN_PCT:
            self._consecutive_gpu_high += 1
        else:
            self._consecutive_gpu_high = 0

        # --- idle → downloading 计数 ---
        if net > NET_DOWNLOAD_MBS:
            self._consecutive_net_high += 1
        else:
            self._consecutive_net_high = 0

        # --- 转移优先级：training > downloading > truly_stuck ---

        if self._consecutive_gpu_high >= ACTIVE_TRIGGER_SAMPLES:
            # §8.2：GPU > 20% 持续 30s → training
            self._enter_state(StuckState.TRAINING)
            return

        if self._consecutive_net_high >= ACTIVE_TRIGGER_SAMPLES:
            # §8.2：net > 1 MB/s 持续 30s → downloading
            self._enter_state(StuckState.DOWNLOADING)
            return

        # --- idle → truly_stuck ---
        elapsed = self._elapsed_since_start()
        idle_duration = self._idle_duration()

        if elapsed < COLD_START_SECS:
            # 冷启动豁免期：不触发 truly_stuck
            # 若全 0 信号，记录 warning
            if (
                (gpu is None or gpu == 0.0)
                and cpu == 0.0
                and disk == 0.0
                and net == 0.0
                and "cold_start_silence_suspected_stuck" not in self.warnings
            ):
                self.warnings.append("cold_start_silence_suspected_stuck")
                logger.warning(
                    "冷启动期内检测到全 0 信号，suspected stuck（豁免中）",
                    extra={"elapsed_s": elapsed},
                )
            return

        if idle_duration > IDLE_STUCK_SECS:
            # §8.2：停留 idle > 15min 且冷启动期已过 → truly_stuck
            logger.warning(
                "idle 停留超过 15min → truly_stuck",
                extra={"idle_duration_s": idle_duration, "elapsed_s": elapsed},
            )
            self._enter_state(StuckState.TRULY_STUCK)

    def _handle_training(
        self,
        gpu: float | None,
        cpu: float,
        disk: float,
    ) -> None:
        """training 态：检查 → idle（AND 条件）。

        §8.2 training 行：
        - → idle：GPU < 5% AND CPU < 10% AND disk < 1 MB/s 持续 60s（12 样本 AND 条件）

        GPU=None（无 GPU）时：忽略 GPU 信号，仅 CPU + disk 双 AND。
        """
        # --- GPU 条件 ---
        # GPU=None：降级为满足 GPU 条件（无 GPU 就不能用 GPU 信号判断活跃）
        gpu_low = (gpu is None) or (gpu < GPU_IDLE_PCT)
        cpu_low = cpu < 10.0
        disk_low = disk < DISK_ACTIVE_MBS

        if gpu_low and cpu_low and disk_low:
            self._consecutive_all_low += 1
        else:
            self._consecutive_all_low = 0

        if self._consecutive_all_low >= WINDOW_SAMPLES:
            # §8.2：所有条件持续 60s（12 个样本）→ idle
            self._enter_state(StuckState.IDLE)

    def _handle_downloading(self, net: float, disk: float) -> None:
        """downloading 态：检查 → idle（AND 条件）。

        §8.2 downloading 行：
        - → idle：net < 100 KB/s AND disk < 1 MB/s 持续 60s（12 样本）
        """
        net_low = net < NET_IDLE_KBS       # < 100 KB/s = 0.1 MB/s
        disk_low = disk < DISK_ACTIVE_MBS   # < 1 MB/s

        if net_low and disk_low:
            self._consecutive_all_low += 1
        else:
            self._consecutive_all_low = 0

        if self._consecutive_all_low >= WINDOW_SAMPLES:
            # §8.2：两个条件持续 60s → idle
            self._enter_state(StuckState.IDLE)


# ---------------------------------------------------------------------------
# CircuitBreaker
# ---------------------------------------------------------------------------


class CircuitBreaker:
    """连续 stuck-restart 熔断器（architecture §8.5）。

    跟踪 stuck_restart_count，连续 3 次后熔断：
    - should_restart() 返回 False
    - record_human_review_needed() 写 stuck_lock + state.json.needs_human_review=True
    """

    def __init__(self, stuck_restart_count: int = 0) -> None:
        self.stuck_restart_count: int = stuck_restart_count

    def should_restart(self) -> bool:
        """返回是否允许再次重启（count < 3 时允许）。"""
        return self.stuck_restart_count < 3

    def record_restart(self) -> None:
        """记录一次 stuck-restart（count +1）。"""
        self.stuck_restart_count += 1
        logger.info(
            "stuck-restart 记录",
            extra={"count": self.stuck_restart_count},
        )

    def record_human_review_needed(self, run_id: str) -> None:
        """熔断后写 stuck_lock 文件 + 更新 state.json.needs_human_review=True。

        architecture §8.5：
        - 写 runs/<id>/stuck_lock（存在即 locked）
        - 写 state.json.needs_human_review=True
        """
        from pars.stuck.stuck_lock import write_stuck_lock
        from pars.ledger.state import update_state

        # 写 stuck_lock 文件（atomic）
        write_stuck_lock(
            run_id=run_id,
            reason="circuit_breaker_tripped",
            restart_count=self.stuck_restart_count,
        )

        # 更新 state.json
        try:
            update_state(run_id, needs_human_review=True)
        except Exception as exc:
            logger.error(
                "record_human_review_needed: 更新 state.json 失败",
                exc_info=exc,
                extra={"run_id": run_id},
            )

        logger.warning(
            "circuit breaker 熔断，需人工干预",
            extra={"run_id": run_id, "restart_count": self.stuck_restart_count},
        )
