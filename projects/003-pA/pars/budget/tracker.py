"""
pars.budget.tracker — BudgetTracker + BudgetMonitor（T018 · 第二道保险兜底）。

结论：
  USD 硬帽主控制归 T010 proxy 前置拒绝（C20），本模块是第二道保险：
  - wall_clock 超限（60s 轮询） → SIGINT
  - GPU hours 超限（60s 轮询） → SIGINT
  - USD 超限（60s 轮询兜底，正常不触发） → warning + SIGINT

设计要点：
  - BudgetTracker.tick() 从 state.json 读 usd_spent（T010 proxy 权威值），
    不自行计算 USD（避免 race condition / 定价二义）
  - 写回 state.json 时仅更新 wall_clock_elapsed_s / gpu_hours_used，
    不覆盖 usd_spent（T010 负责写该字段）
  - GPU hours 近似计算：gpu_util > 5% 的 60s tick 数 × 60 / 3600
    可靠性不高，v0.1 接受（README 声明"近似"）
  - SIGINT 通过 os.kill(worker_pid, signal.SIGINT) 发送
  - BudgetMonitor 是 daemon Thread，60s 间隔轮询

GPU 读取策略（降级链）：
  1. 尝试 GPUtil（pip 包，轻量）
  2. 尝试 nvidia-smi subprocess 解析
  3. 两者均失败 → 返回 0.0（保守：不触发 GPU cap）

接口说明：
  - _get_gpu_util_pct()：模块级函数，供 tracker.tick() 调用，也便于测试 mock
  - _get_started_at_ts()：从 state.json 读 started_at 时间戳（兼容字段不存在的情况）
"""

from __future__ import annotations

import os
import signal
import time
from dataclasses import dataclass, field
from datetime import timezone
from threading import Event, Thread
from typing import Any

from pars.ledger.state import read_state, update_state
from pars.logging import get_logger

logger = get_logger(__name__)


# ---------------------------------------------------------------------------
# GPU 利用率读取（降级链）
# ---------------------------------------------------------------------------


def _get_gpu_util_pct() -> float:
    """返回当前 GPU 利用率百分比（0.0 ~ 100.0）。

    降级链：
    1. GPUtil（如已安装）
    2. nvidia-smi --query-gpu=utilization.gpu --format=csv,noheader,nounits
    3. 均失败 → 返回 0.0（保守策略：不因 GPU 读取失败而误触发 cap）

    注意：macOS 无 NVIDIA GPU，nvidia-smi 不可用时正常返回 0.0。
    """
    # 方法 1：GPUtil
    try:
        import GPUtil  # type: ignore[import-untyped]  # noqa: PLC0415

        gpus = GPUtil.getGPUs()
        if gpus:
            return float(gpus[0].load * 100.0)
    except Exception:  # noqa: BLE001, S110
        pass  # GPUtil 未安装或无 GPU，降级到下一方法

    # 方法 2：nvidia-smi
    try:
        import subprocess  # noqa: PLC0415

        result = subprocess.run(  # noqa: S603
            ["nvidia-smi", "--query-gpu=utilization.gpu", "--format=csv,noheader,nounits"],  # noqa: S607
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
        if result.returncode == 0:
            val = result.stdout.strip().splitlines()[0]
            return float(val)
    except Exception:  # noqa: BLE001, S110
        pass  # nvidia-smi 不可用（macOS 正常），降级到 0.0

    # 方法 3：降级返回 0.0
    return 0.0


def _get_started_at_ts(run_id: str) -> float:
    """从 state.json 读取 started_at 时间戳（Unix epoch float）。

    设计：T018 规格中 started_at 来自 state.json.last_update（首次写入近似值）。
    因为 RecallKit v0.1 状态机中没有独立 started_at 字段，
    我们用 state.json 的 last_update 作为最佳近似（Orchestrator 启动 run 时写入）。

    若无法读取 → 返回 time.time()（wall_clock 近似为 0，保守策略：不触发 cap）。
    """
    try:
        state = read_state(run_id)
        dt = state.last_update
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.timestamp()
    except Exception:  # noqa: BLE001
        return time.time()


# ---------------------------------------------------------------------------
# BudgetStatus 数据类
# ---------------------------------------------------------------------------


@dataclass
class BudgetStatus:
    """单次 tick() 的预算快照。

    字段：
        usd_spent : 当前累计消费 USD（从 state.json 权威读取）
        wall_s    : 已用 wall-clock 秒数
        gpu_h     : 已用 GPU 小时数
    """

    usd_spent: float
    wall_s: float
    gpu_h: float

    def as_dict(self) -> dict[str, Any]:
        """序列化为 dict（与 architecture §2 current_usage 接口对齐）。"""
        return {
            "usd_spent": self.usd_spent,
            "wall_s": self.wall_s,
            "gpu_h": self.gpu_h,
        }


# ---------------------------------------------------------------------------
# BudgetTracker
# ---------------------------------------------------------------------------


class BudgetTracker:
    """预算追踪器（第二道保险）。

    职责：
    - tick()：读 state.json + 计算 wall_clock + 累计 GPU hours → 写回 state
    - check_caps()：比较 status 与各 cap 阈值，返回突破项列表
    - current_usage()：返回当前使用量 dict（非 tick，直接读 state）
    - _on_cap_exceeded()：发 SIGINT 到 worker_pid + 记日志

    注意：
    - usd_spent 只读不写（T010 proxy 权威）
    - wall_clock 和 gpu_hours 允许写回 state（T018 负责这两字段）
    """

    # GPU 活跃阈值：利用率 > 5% 才计入 GPU hours（与 T018 spec 对齐）
    _GPU_ACTIVE_THRESHOLD_PCT: float = 5.0
    # 每次 tick 的 GPU 积分时长（秒）；60s 轮询 × 60s/tick = 1 tick
    _GPU_TICK_SECONDS: float = 60.0

    def __init__(
        self,
        run_id: str,
        *,
        wall_clock_cap_s: float,
        gpu_hours_cap: float,
        usd_cap: float,
        worker_pid: int,
    ) -> None:
        """初始化 BudgetTracker。

        Args:
            run_id          : run 唯一标识（用于定位 state.json）
            wall_clock_cap_s: wall-clock 上限（秒）
            gpu_hours_cap   : GPU 使用小时上限
            usd_cap         : USD 硬帽（第二道保险阈值，正常由 T010 proxy 前置拦截）
            worker_pid      : worker 进程 PID（SIGINT 目标）
        """
        self.run_id = run_id
        self.wall_clock_cap_s = float(wall_clock_cap_s)
        self.gpu_hours_cap = float(gpu_hours_cap)
        self.usd_cap = float(usd_cap)
        self.worker_pid = worker_pid
        # 内部 GPU hours 累加器（补充 state.gpu_hours_used）
        self._gpu_h_delta: float = 0.0

    # -----------------------------------------------------------------------
    # 主接口
    # -----------------------------------------------------------------------

    def tick(self) -> BudgetStatus:
        """执行一次预算采样，写回 state.json（仅 wall_clock + gpu_hours 字段）。

        读取：
          - state.json.usd_spent（T010 权威，不修改）
          - _get_started_at_ts() → wall_clock = now - started_at
          - _get_gpu_util_pct() → gpu 是否活跃

        写回：
          - wall_clock_elapsed_s
          - gpu_hours_used

        Returns:
            BudgetStatus — 当前预算快照
        """
        now_ts = time.time()
        started_at_ts = _get_started_at_ts(self.run_id)
        wall_s = now_ts - started_at_ts

        # 读取 GPU 利用率，决定是否积累 GPU hours
        gpu_util = _get_gpu_util_pct()
        if gpu_util > self._GPU_ACTIVE_THRESHOLD_PCT:
            self._gpu_h_delta += self._GPU_TICK_SECONDS / 3600.0

        # 读 state：获取 usd_spent（权威）和 gpu_hours_used（已积累基础）
        try:
            state = read_state(self.run_id)
            usd_spent = state.usd_spent
            # gpu_hours = state 中已有 + 本次 tick 累计增量
            gpu_h_total = state.gpu_hours_used + self._gpu_h_delta
        except Exception:  # noqa: BLE001
            # state 读失败：保守处理，用 0 值继续（不中断监控线程）
            logger.warning("state.json 读取失败，使用默认值继续监控", extra={"run_id": self.run_id})
            usd_spent = 0.0
            gpu_h_total = self._gpu_h_delta

        # 写回 state（仅 wall_clock + gpu_hours，不动 usd_spent）
        try:
            update_state(
                self.run_id,
                wall_clock_elapsed_s=wall_s,
                gpu_hours_used=gpu_h_total,
            )
        except Exception:  # noqa: BLE001
            # 写失败不中断监控（只记日志）
            logger.warning("state.json 写回失败", extra={"run_id": self.run_id})

        return BudgetStatus(usd_spent=usd_spent, wall_s=wall_s, gpu_h=gpu_h_total)

    def check_caps(self, status: BudgetStatus) -> list[str]:
        """检查各 cap 是否被突破，返回突破项名称列表。

        Args:
            status: tick() 返回的 BudgetStatus

        Returns:
            突破项列表（空 = 全部 OK）。
            项名：'wall_clock' | 'gpu_hours' | 'usd'
        """
        breaches: list[str] = []

        if status.wall_s >= self.wall_clock_cap_s:
            breaches.append("wall_clock")

        if status.gpu_h >= self.gpu_hours_cap:
            breaches.append("gpu_hours")

        if status.usd_spent >= self.usd_cap:
            breaches.append("usd")

        return breaches

    def current_usage(self) -> dict[str, Any]:
        """返回当前使用量快照（直接读 state.json，不触发写操作）。

        Returns:
            {"wall_s": float, "gpu_h": float}（spec 约定格式）
        """
        try:
            state = read_state(self.run_id)
            return {
                "wall_s": state.wall_clock_elapsed_s,
                "gpu_h": state.gpu_hours_used,
            }
        except Exception:  # noqa: BLE001
            return {"wall_s": 0.0, "gpu_h": 0.0}

    def _on_cap_exceeded(self, reason: str) -> None:
        """cap 突破响应：发 SIGINT 到 worker_pid + 写日志。

        Args:
            reason: 突破原因（'wall_clock' | 'gpu_hours' | 'usd'）

        USD 路径的特殊日志：
            若 reason == 'usd'，额外打印 WARNING 说明"proxy pre-reject may have missed"，
            表示 T010 proxy 前置拦截出现漏洞（正常不应触发此路径）。
        """
        if reason == "usd":
            logger.warning(
                "usd cap hit via 60s polling fallback, proxy pre-reject may have missed. "
                "run_id=%s usd_cap=%s — 若频繁触发请检查 T010 proxy 预估逻辑。",
                self.run_id,
                self.usd_cap,
            )
        else:
            logger.warning(
                "SIGINT due to %s cap exceeded. run_id=%s pid=%d — 发送 SIGINT 给 worker。",
                reason,
                self.run_id,
                self.worker_pid,
            )

        # 发 SIGINT 到 worker 进程
        try:
            os.kill(self.worker_pid, signal.SIGINT)
        except ProcessLookupError:
            # worker 已退出（进程不存在），忽略
            logger.info("worker pid=%d 不存在，跳过 SIGINT", self.worker_pid)
        except Exception as exc:  # noqa: BLE001
            logger.error("os.kill 失败: %s", exc)


# ---------------------------------------------------------------------------
# BudgetMonitor — 60s 轮询 daemon Thread
# ---------------------------------------------------------------------------


class BudgetMonitor(Thread):
    """60s 轮询 BudgetTracker，cap 突破时发 SIGINT（T018 第二道保险）。

    用法：
        monitor = BudgetMonitor(tracker=tracker, poll_interval_s=60.0)
        monitor.start()
        ...
        monitor.stop()
        monitor.join()

    设计：
    - daemon=True：主进程退出时自动回收，不阻塞退出
    - _stop_event：Event 控制退出，stop() 设置后下一次 sleep 结束即退出
    - poll_interval_s：可参数化（单元测试传小值加速验证）
    """

    def __init__(
        self,
        tracker: BudgetTracker,
        poll_interval_s: float = 60.0,
    ) -> None:
        super().__init__(name=f"BudgetMonitor-{tracker.run_id}", daemon=True)
        self._tracker = tracker
        self._poll_interval_s = poll_interval_s
        self._stop_event = Event()

    def run(self) -> None:
        """轮询主循环：每 poll_interval_s 秒 tick 一次，检查 cap。"""
        logger.info(
            "BudgetMonitor 启动：run_id=%s poll_interval=%ss",
            self._tracker.run_id,
            self._poll_interval_s,
        )
        while not self._stop_event.is_set():
            try:
                status = self._tracker.tick()
                breaches = self._tracker.check_caps(status)
                for reason in breaches:
                    self._tracker._on_cap_exceeded(reason)
                    # cap 突破后只发一次 SIGINT，随后退出循环等 worker 响应
                    self._stop_event.set()
                    break
            except Exception as exc:  # noqa: BLE001
                # 轮询异常不能崩溃 monitor 线程，记录后继续
                logger.error("BudgetMonitor tick 异常: %s", exc)

            time.sleep(self._poll_interval_s)

        logger.info("BudgetMonitor 退出：run_id=%s", self._tracker.run_id)

    def stop(self) -> None:
        """请求监控循环退出（非阻塞，需配合 join() 等待线程结束）。"""
        self._stop_event.set()
