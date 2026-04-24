"""
test_stuck_state_machine.py — StuckStateMachine + CircuitBreaker 单测。

测试覆盖 architecture §8.2 全部转移规则 + §8.3 冷启动豁免 + §8.7 测试矩阵。
共 >=20 个测试用例，每条 transition 规则独立断言。

采样约定（对齐 architecture §8.1）：
- 采样周期 5s
- 窗口长度 12（12 × 5s = 60s）
- 转移条件以"持续 N 秒"= "连续 N/5 个样本全满足"表达

Probe sample dict 格式：
    {
        "gpu": float | None,        # GPU 利用率 0-100%；None 表示无 GPU
        "cpu": float,               # 子进程 CPU% 累加
        "disk_delta_mbs": float,    # 磁盘 IO 增量 MB/s
        "net_delta_mbs": float,     # 网络 IO 增量 MB/s
    }
"""

from __future__ import annotations

import time
from collections import deque

import pytest

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


# ---------------------------------------------------------------------------
# 工具函数：构造 probe sample
# ---------------------------------------------------------------------------

def _sample(
    gpu: float | None = 0.0,
    cpu: float = 0.0,
    disk_mbs: float = 0.0,
    net_mbs: float = 0.0,
) -> dict:
    """构造一个 probe sample dict。"""
    return {
        "gpu": gpu,
        "cpu": cpu,
        "disk_delta_mbs": disk_mbs,
        "net_delta_mbs": net_mbs,
    }


def _make_sm(state: StuckState = StuckState.IDLE, elapsed: float = 400.0) -> StuckStateMachine:
    """构造一个处于指定初始态、已过冷启动的 SM。

    elapsed=400 确保冷启动期（300s）已结束，可允许 truly_stuck 转移。
    """
    sm = StuckStateMachine(clock=lambda: elapsed)
    sm._state = state
    sm._state_entered_at = 0.0
    return sm


# ---------------------------------------------------------------------------
# 常量合理性校验（architecture §8.1 contractual values）
# ---------------------------------------------------------------------------

class TestContractConstants:
    """校验实现常量与 architecture §8 数值严格一致。"""

    def test_should_use_5s_sample_interval_when_checking_constant(self):
        assert SAMPLE_INTERVAL == 5, f"采样周期必须是 5s，got {SAMPLE_INTERVAL}"

    def test_should_have_12_window_samples_when_checking_constant(self):
        assert WINDOW_SAMPLES == 12, f"窗口样本数必须是 12，got {WINDOW_SAMPLES}"

    def test_should_have_300s_cold_start_when_checking_constant(self):
        assert COLD_START_SECS == 300

    def test_should_have_900s_idle_stuck_when_checking_constant(self):
        assert IDLE_STUCK_SECS == 900  # 15min

    def test_should_have_correct_thresholds_when_checking_constants(self):
        assert GPU_TRAIN_PCT == 20.0
        assert GPU_IDLE_PCT == 5.0
        assert NET_DOWNLOAD_MBS == 1.0
        assert NET_IDLE_KBS == 0.1  # 100 KB/s = 0.1 MB/s
        assert DISK_ACTIVE_MBS == 1.0
        assert TRAIN_IDLE_SECS == 60


# ---------------------------------------------------------------------------
# idle → training 转移（§8.2：GPU > 20% 持续 30s = 连续 6 个样本）
# ---------------------------------------------------------------------------

class TestIdleToTraining:
    """idle → training：GPU util > 20% 持续 30s（6 个 5s 样本）。"""

    def test_should_stay_idle_when_gpu_high_only_5_samples(self):
        """5 个高 GPU 样本（29s）不触发 training。"""
        sm = _make_sm(StuckState.IDLE, elapsed=400.0)
        for _ in range(5):  # 只有 5 个样本，不满足 6 个
            state = sm.transition(_sample(gpu=30.0))
        assert state == StuckState.IDLE

    def test_should_transition_idle_to_training_when_gpu_high_6_samples(self):
        """连续 6 个高 GPU 样本（30s）触发 idle → training（§8.7 场景 6 边界）。"""
        sm = _make_sm(StuckState.IDLE, elapsed=400.0)
        for _ in range(5):
            sm.transition(_sample(gpu=30.0))
        state = sm.transition(_sample(gpu=30.0))  # 第 6 个
        assert state == StuckState.TRAINING

    def test_should_reset_idle_to_training_when_gpu_drops_below_threshold(self):
        """GPU 中途降到 20% 以下后重置计数，需重新满 6 个才触发。"""
        sm = _make_sm(StuckState.IDLE, elapsed=400.0)
        for _ in range(5):
            sm.transition(_sample(gpu=30.0))
        sm.transition(_sample(gpu=15.0))  # 中断
        for _ in range(5):
            sm.transition(_sample(gpu=30.0))
        state = sm.transition(_sample(gpu=30.0))  # 重新满 6 个
        assert state == StuckState.TRAINING

    def test_should_use_exactly_20pct_boundary_when_gpu_equals_threshold(self):
        """GPU == 20.0% 不触发 training（需严格大于 20%）。"""
        sm = _make_sm(StuckState.IDLE, elapsed=400.0)
        for _ in range(6):
            state = sm.transition(_sample(gpu=20.0))
        assert state == StuckState.IDLE

    def test_should_trigger_training_when_gpu_just_above_threshold(self):
        """GPU = 20.1% 触发 training（严格大于 20%）。"""
        sm = _make_sm(StuckState.IDLE, elapsed=400.0)
        for _ in range(6):
            state = sm.transition(_sample(gpu=20.1))
        assert state == StuckState.TRAINING


# ---------------------------------------------------------------------------
# idle → downloading 转移（§8.2：net > 1 MB/s 持续 30s = 连续 6 个样本）
# ---------------------------------------------------------------------------

class TestIdleToDownloading:
    """idle → downloading：net IO > 1 MB/s 持续 30s（6 个样本）。"""

    def test_should_stay_idle_when_net_high_only_5_samples(self):
        """5 个高网络样本不触发 downloading。"""
        sm = _make_sm(StuckState.IDLE, elapsed=400.0)
        for _ in range(5):
            state = sm.transition(_sample(net_mbs=2.0))
        assert state == StuckState.IDLE

    def test_should_transition_idle_to_downloading_when_net_high_6_samples(self):
        """6 个高网络样本触发 idle → downloading。"""
        sm = _make_sm(StuckState.IDLE, elapsed=400.0)
        for _ in range(5):
            sm.transition(_sample(net_mbs=2.0))
        state = sm.transition(_sample(net_mbs=2.0))
        assert state == StuckState.DOWNLOADING

    def test_should_use_1mbs_net_boundary_when_checking_threshold(self):
        """net == 1.0 MB/s 不触发 downloading（需严格大于 1 MB/s）。"""
        sm = _make_sm(StuckState.IDLE, elapsed=400.0)
        for _ in range(6):
            state = sm.transition(_sample(net_mbs=1.0))
        assert state == StuckState.IDLE


# ---------------------------------------------------------------------------
# training → idle 转移（§8.2：GPU<5% AND CPU<10% AND disk<1MB/s 持续 60s = 12 样本）
# ---------------------------------------------------------------------------

class TestTrainingToIdle:
    """training → idle：3 个 AND 条件持续 60s（12 个样本）。"""

    def test_should_stay_training_when_all_low_only_11_samples(self):
        """11 个全低样本（55s）不触发 training→idle（§8.7 场景 7 变体）。"""
        sm = _make_sm(StuckState.TRAINING, elapsed=400.0)
        for _ in range(11):
            state = sm.transition(_sample(gpu=2.0, cpu=5.0, disk_mbs=0.5))
        assert state == StuckState.TRAINING

    def test_should_transition_training_to_idle_when_all_low_12_samples(self):
        """12 个全低样本（60s）触发 training → idle。"""
        sm = _make_sm(StuckState.TRAINING, elapsed=400.0)
        for _ in range(11):
            sm.transition(_sample(gpu=2.0, cpu=5.0, disk_mbs=0.5))
        state = sm.transition(_sample(gpu=2.0, cpu=5.0, disk_mbs=0.5))
        assert state == StuckState.IDLE

    def test_should_block_training_to_idle_when_gpu_still_high(self):
        """GPU >= 5% 阻止 training → idle（§8.7 场景 8 变体）。"""
        sm = _make_sm(StuckState.TRAINING, elapsed=400.0)
        for _ in range(12):
            state = sm.transition(_sample(gpu=5.0, cpu=5.0, disk_mbs=0.5))
        assert state == StuckState.TRAINING

    def test_should_block_training_to_idle_when_cpu_still_high(self):
        """CPU >= 10% 阻止 training → idle。"""
        sm = _make_sm(StuckState.TRAINING, elapsed=400.0)
        for _ in range(12):
            state = sm.transition(_sample(gpu=2.0, cpu=10.0, disk_mbs=0.5))
        assert state == StuckState.TRAINING

    def test_should_block_training_to_idle_when_disk_io_active(self):
        """disk IO >= 1 MB/s 阻止 training → idle（§8.7 场景 8）。"""
        sm = _make_sm(StuckState.TRAINING, elapsed=400.0)
        for _ in range(12):
            state = sm.transition(_sample(gpu=0.0, cpu=5.0, disk_mbs=1.0))
        assert state == StuckState.TRAINING

    def test_should_reset_training_idle_counter_when_condition_broken(self):
        """11个低样本后 disk_io 突然高，计数重置，需要重新 12 个。"""
        sm = _make_sm(StuckState.TRAINING, elapsed=400.0)
        for _ in range(11):
            sm.transition(_sample(gpu=2.0, cpu=5.0, disk_mbs=0.5))
        sm.transition(_sample(gpu=2.0, cpu=5.0, disk_mbs=5.0))  # disk 突然高
        for _ in range(11):
            sm.transition(_sample(gpu=2.0, cpu=5.0, disk_mbs=0.5))
        state = sm.transition(_sample(gpu=2.0, cpu=5.0, disk_mbs=0.5))
        assert state == StuckState.IDLE

    def test_should_handle_none_gpu_when_no_nvidia_smi(self):
        """GPU=None（无 GPU/驱动失败）时，仅看 CPU + disk，GPU 信号忽略。"""
        sm = _make_sm(StuckState.TRAINING, elapsed=400.0)
        for _ in range(11):
            sm.transition(_sample(gpu=None, cpu=5.0, disk_mbs=0.5))
        state = sm.transition(_sample(gpu=None, cpu=5.0, disk_mbs=0.5))
        # GPU=None 降级为忽略 GPU 信号，CPU + disk 均低 → 可以转 idle
        assert state == StuckState.IDLE


# ---------------------------------------------------------------------------
# downloading → idle 转移（§8.2：net<100KB/s AND disk<1MB/s 持续 60s）
# ---------------------------------------------------------------------------

class TestDownloadingToIdle:
    """downloading → idle：net<100KB/s AND disk<1MB/s 持续 60s（12 样本）。"""

    def test_should_stay_downloading_when_low_only_11_samples(self):
        """11 个样本不触发 downloading→idle。"""
        sm = _make_sm(StuckState.DOWNLOADING, elapsed=400.0)
        for _ in range(11):
            state = sm.transition(_sample(net_mbs=0.05, disk_mbs=0.5))
        assert state == StuckState.DOWNLOADING

    def test_should_transition_downloading_to_idle_when_all_low_12_samples(self):
        """12 个全低样本触发 downloading → idle。"""
        sm = _make_sm(StuckState.DOWNLOADING, elapsed=400.0)
        for _ in range(11):
            sm.transition(_sample(net_mbs=0.05, disk_mbs=0.5))
        state = sm.transition(_sample(net_mbs=0.05, disk_mbs=0.5))
        assert state == StuckState.IDLE

    def test_should_block_downloading_to_idle_when_net_above_100kbs(self):
        """net >= 100 KB/s (0.1 MB/s) 阻止 downloading→idle。"""
        sm = _make_sm(StuckState.DOWNLOADING, elapsed=400.0)
        for _ in range(12):
            state = sm.transition(_sample(net_mbs=0.1, disk_mbs=0.0))
        assert state == StuckState.DOWNLOADING


# ---------------------------------------------------------------------------
# idle → truly_stuck 转移（§8.2：停留 idle > 15min 且冷启动期已过）
# ---------------------------------------------------------------------------

class TestIdleToTrulyStuck:
    """idle → truly_stuck：停留 idle > 15min（900s）且 elapsed >= 300s。"""

    def test_should_transition_to_truly_stuck_when_idle_exceeds_15min(self):
        """模拟时钟推进到 idle 停留超过 900s 后触发 truly_stuck。"""
        # 使用可控时钟：SM 在 t=400 进入 idle（冷启动已过）
        clock_val = [0.0]
        sm = StuckStateMachine(clock=lambda: clock_val[0])
        sm._state = StuckState.IDLE
        sm._start_time = 0.0   # SM 在 t=0 启动

        # 在 t=400 进入 idle（elapsed_since_start=400 > COLD_START_SECS=300）
        clock_val[0] = 400.0
        sm._state_entered_at = 400.0  # 在 t=400 进入 idle

        # idle 停留 899s（不足 15min）：clock=400+899=1299，idle_duration=899 < 900
        clock_val[0] = 400.0 + 899.0
        state = sm.transition(_sample())
        assert state == StuckState.IDLE

        # idle 停留 901s（超过 15min）：clock=400+901=1301，idle_duration=901 > 900
        clock_val[0] = 400.0 + 901.0
        state = sm.transition(_sample())
        assert state == StuckState.TRULY_STUCK

    def test_should_not_transition_to_truly_stuck_during_cold_start(self):
        """冷启动期（elapsed < 300s）内，即使全 0 信号也不触发 truly_stuck（§8.7 场景 4）。"""
        clock_val = [0.0]
        sm = StuckStateMachine(clock=lambda: clock_val[0])
        sm._state = StuckState.IDLE
        sm._state_entered_at = 0.0
        sm._start_time = 0.0  # elapsed_since_start = clock - start_time

        # 在冷启动期内推进（elapsed < 300s）
        clock_val[0] = 200.0  # 仅 200s，在冷启动豁免期内
        state = sm.transition(_sample())
        assert state == StuckState.IDLE
        # 且应记录 warning
        assert len(sm.warnings) > 0

    def test_should_record_warning_during_cold_start_silence(self):
        """冷启动期内全 0 信号时，应记录 cold_start_silence_suspected_stuck 警告。"""
        clock_val = [0.0]
        sm = StuckStateMachine(clock=lambda: clock_val[0])
        sm._state = StuckState.IDLE
        sm._state_entered_at = 0.0
        sm._start_time = 0.0

        clock_val[0] = 100.0
        sm.transition(_sample())  # 冷启动期，全 0 信号
        assert "cold_start_silence_suspected_stuck" in sm.warnings


# ---------------------------------------------------------------------------
# §8.7 场景矩阵中的关键边界测试
# ---------------------------------------------------------------------------

class TestBoundaryScenarios:
    """§8.7 测试矩阵关键场景单测。"""

    def test_should_not_trigger_training_when_gpu_high_29s(self):
        """§8.7 场景 5：GPU=25% 持续 29s（5 个样本），不触发 idle→training。"""
        sm = _make_sm(StuckState.IDLE, elapsed=400.0)
        for _ in range(5):  # 5 个 = 25s，不满足 30s（6 个）
            state = sm.transition(_sample(gpu=25.0))
        assert state == StuckState.IDLE

    def test_should_trigger_training_when_gpu_high_30s(self):
        """§8.7 场景 6：GPU=25% 持续 30s（6 个样本），触发 idle→training。"""
        sm = _make_sm(StuckState.IDLE, elapsed=400.0)
        for _ in range(6):
            state = sm.transition(_sample(gpu=25.0))
        assert state == StuckState.TRAINING

    def test_should_not_trigger_training_to_idle_at_59s(self):
        """§8.7 场景 7：GPU<5%+CPU<10%+disk<1MB/s 持续 59s（11 个样本），不触发 training→idle。"""
        sm = _make_sm(StuckState.TRAINING, elapsed=400.0)
        for _ in range(11):  # 11 个 = 55s < 60s
            state = sm.transition(_sample(gpu=2.0, cpu=5.0, disk_mbs=0.5))
        assert state == StuckState.TRAINING

    def test_should_suppress_idle_when_disk_active(self):
        """§8.7 场景 8：GPU=0 但 disk=5MB/s（写 checkpoint），保持 training 不误判。"""
        sm = _make_sm(StuckState.TRAINING, elapsed=400.0)
        for _ in range(12):
            state = sm.transition(_sample(gpu=0.0, cpu=0.0, disk_mbs=5.0))
        assert state == StuckState.TRAINING  # disk 抑制了 training→idle


# ---------------------------------------------------------------------------
# truly_stuck 是终态（不应自行转移）
# ---------------------------------------------------------------------------

class TestTrulyStuckTerminal:
    """truly_stuck 进入后不自行转移，等待 monitor 发 SIGINT。"""

    def test_should_stay_truly_stuck_once_entered(self):
        """truly_stuck 态：无论 probe 输入如何，保持 truly_stuck。"""
        sm = _make_sm(StuckState.TRULY_STUCK, elapsed=999.0)
        state = sm.transition(_sample(gpu=50.0, cpu=80.0, disk_mbs=10.0))
        assert state == StuckState.TRULY_STUCK


# ---------------------------------------------------------------------------
# CircuitBreaker
# ---------------------------------------------------------------------------

class TestCircuitBreaker:
    """CircuitBreaker：连续 3 次 stuck-restart → 熔断 + needs_human_review。"""

    def test_should_allow_restart_when_count_below_3(self):
        """count < 3 时 should_restart() 返回 True。"""
        cb = CircuitBreaker(stuck_restart_count=0)
        assert cb.should_restart() is True

    def test_should_block_restart_when_count_reaches_3(self):
        """count == 3 时 should_restart() 返回 False（熔断）。"""
        cb = CircuitBreaker(stuck_restart_count=3)
        assert cb.should_restart() is False

    def test_should_increment_count_when_record_restart(self):
        """record_restart() 使 count +1。"""
        cb = CircuitBreaker(stuck_restart_count=0)
        cb.record_restart()
        assert cb.stuck_restart_count == 1

    def test_should_trip_breaker_after_3_restarts(self):
        """3 次 record_restart() 后熔断。"""
        cb = CircuitBreaker(stuck_restart_count=0)
        for _ in range(3):
            cb.record_restart()
        assert cb.should_restart() is False

    def test_should_still_allow_restart_at_count_2(self):
        """count=2 时仍允许第 3 次 restart（count < 3）。"""
        cb = CircuitBreaker(stuck_restart_count=2)
        assert cb.should_restart() is True


# ---------------------------------------------------------------------------
# StuckStateMachine 状态属性访问
# ---------------------------------------------------------------------------

class TestStateMachineProperties:
    """状态机属性：current_state / enter_time / warnings 等。"""

    def test_should_start_in_idle_state_when_initialized(self):
        """初始态为 idle。"""
        sm = StuckStateMachine()
        assert sm.current_state == StuckState.IDLE

    def test_should_expose_warnings_list(self):
        """warnings 属性初始为空列表。"""
        sm = StuckStateMachine()
        assert sm.warnings == []

    def test_should_track_state_entry_time_when_state_changes(self):
        """转入新态时更新 state_entered_at（通过 clock）。"""
        clock_val = [0.0]
        sm = StuckStateMachine(clock=lambda: clock_val[0])
        sm._state = StuckState.IDLE
        sm._start_time = 0.0
        sm._state_entered_at = 0.0

        clock_val[0] = 400.0
        # 推进 6 个高 GPU 样本触发 idle → training
        for _ in range(6):
            sm.transition(_sample(gpu=30.0))

        assert sm.current_state == StuckState.TRAINING
        assert sm.state_entered_at == 400.0  # 应在 clock=400 时记录入 training
