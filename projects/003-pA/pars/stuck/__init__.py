"""
pars.stuck — Stuck Detector 状态机（architecture §8 实现）。

职责：5s 周期采样 GPU/CPU/disk/net 指标；实现 architecture §8 的
4 态状态机（idle / training / downloading / truly_stuck）；
冷启动 300s 豁免；连续 3 次 stuck-restart 熔断 + stuck_lock 持久化。

公开 API：
    StuckState           — 4 态枚举（用于类型检查）
    StuckStateMachine    — 状态机（纯函数，无 I/O）
    CircuitBreaker       — 熔断器（count < 3 允许重启）
    StuckMonitor         — 5s 采样 Thread（I/O shell）
    has_stuck_lock       — 检查 stuck_lock 文件是否存在（T019 can_resume() 使用）
    write_stuck_lock     — 写 stuck_lock 文件（原子）
    clear_stuck_lock     — 删除 stuck_lock 文件（pars unlock）
    read_stuck_lock      — 读取 stuck_lock 内容
"""

from pars.stuck.state_machine import (
    COLD_START_SECS,
    DISK_ACTIVE_MBS,
    GPU_IDLE_PCT,
    GPU_TRAIN_PCT,
    IDLE_STUCK_SECS,
    NET_DOWNLOAD_MBS,
    NET_IDLE_KBS,
    SAMPLE_INTERVAL,
    TRAIN_IDLE_SECS,
    WINDOW_SAMPLES,
    CircuitBreaker,
    StuckState,
    StuckStateMachine,
)
from pars.stuck.stuck_lock import (
    StuckLockData,
    clear_stuck_lock,
    has_stuck_lock,
    read_stuck_lock,
    write_stuck_lock,
)
from pars.stuck.monitor import StuckMonitor

__all__ = [
    # 状态机
    "StuckState",
    "StuckStateMachine",
    "CircuitBreaker",
    "StuckMonitor",
    # 契约常量
    "SAMPLE_INTERVAL",
    "WINDOW_SAMPLES",
    "COLD_START_SECS",
    "IDLE_STUCK_SECS",
    "GPU_TRAIN_PCT",
    "GPU_IDLE_PCT",
    "NET_DOWNLOAD_MBS",
    "NET_IDLE_KBS",
    "DISK_ACTIVE_MBS",
    "TRAIN_IDLE_SECS",
    # stuck_lock API
    "StuckLockData",
    "has_stuck_lock",
    "write_stuck_lock",
    "clear_stuck_lock",
    "read_stuck_lock",
]
