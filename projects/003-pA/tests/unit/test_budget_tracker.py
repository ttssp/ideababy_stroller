"""
tests.unit.test_budget_tracker — BudgetTracker 单元测试（T018）。

结论：
  覆盖 BudgetTracker 的核心逻辑：
  - tick() 从 state.json 读 usd_spent / 计算 wall_clock / 累计 gpu_hours
  - check_caps() 返回突破项列表（空 = OK）
  - _on_cap_exceeded() 发送 SIGINT 到 worker_pid + 写日志
  - BudgetMonitor 60s 轮询行为
  - USD 兜底路径（正常不触发）

模拟策略：
  - 时钟：monkeypatch time.time / datetime.now
  - GPU：monkeypatch _get_gpu_util 钩子
  - worker_pid：使用 os.getpid()（当前进程），通过 signal handler 捕获
  - 文件系统：tmp_runs_dir fixture
"""

from __future__ import annotations

import os
import signal
import time
from datetime import datetime, timezone, UTC
from pathlib import Path
from threading import Event
from unittest.mock import MagicMock, call, patch

import pytest

from pars.budget.tracker import BudgetMonitor, BudgetStatus, BudgetTracker
from pars.ledger.state import RunPhase, RunState, write_state


# ---------------------------------------------------------------------------
# 辅助：在 tmp_runs_dir 中写 state.json
# ---------------------------------------------------------------------------


def _make_state(
    run_id: str,
    *,
    usd_spent: float = 0.0,
    wall_clock_elapsed_s: float = 0.0,
    gpu_hours_used: float = 0.0,
    started_at_ts: float | None = None,
) -> None:
    """在 RECALLKIT_RUN_DIR/<run_id>/state.json 中写一个最小 RunState。"""
    now = datetime.now(UTC)
    state = RunState(
        run_id=run_id,
        phase=RunPhase.LORA_TRAIN,
        usd_spent=usd_spent,
        wall_clock_elapsed_s=wall_clock_elapsed_s,
        gpu_hours_used=gpu_hours_used,
        last_update=now,
    )
    write_state(state, run_id)


# ===========================================================================
# BudgetStatus 数据类
# ===========================================================================


@pytest.mark.unit
class TestBudgetStatus:
    """BudgetStatus 数据类基础校验。"""

    def test_budget_status_has_expected_fields(self) -> None:
        """should have wall_s and gpu_h fields when created with defaults."""
        status = BudgetStatus(usd_spent=1.5, wall_s=3600.0, gpu_h=0.5)
        assert status.usd_spent == 1.5
        assert status.wall_s == 3600.0
        assert status.gpu_h == 0.5

    def test_budget_status_as_dict(self) -> None:
        """should return dict with wall_s and gpu_h when calling as_dict."""
        status = BudgetStatus(usd_spent=2.0, wall_s=7200.0, gpu_h=1.0)
        d = status.as_dict()
        assert d["wall_s"] == 7200.0
        assert d["gpu_h"] == 1.0


# ===========================================================================
# BudgetTracker.tick — 基础读取
# ===========================================================================


@pytest.mark.unit
class TestBudgetTrackerTick:
    """BudgetTracker.tick() 核心行为。"""

    def test_tick_reads_usd_spent_from_state_when_state_has_value(
        self,
        tmp_runs_dir: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """should read usd_spent=25 from state.json when state has usd_spent=25."""
        monkeypatch.setenv("RECALLKIT_RUN_DIR", str(tmp_runs_dir))
        run_id = "test-usd-read"
        _make_state(run_id, usd_spent=25.0)

        tracker = BudgetTracker(
            run_id=run_id,
            wall_clock_cap_s=43200,
            gpu_hours_cap=12.0,
            usd_cap=30.0,
            worker_pid=os.getpid(),
        )

        # mock time 让 wall_clock 不变
        with patch("pars.budget.tracker.time.time", return_value=0.0):
            with patch("pars.budget.tracker._get_started_at_ts", return_value=0.0):
                status = tracker.tick()

        assert status.usd_spent == 25.0

    def test_tick_calculates_wall_clock_from_started_at(
        self,
        tmp_runs_dir: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """should calculate wall_clock as now - started_at when ticking."""
        monkeypatch.setenv("RECALLKIT_RUN_DIR", str(tmp_runs_dir))
        run_id = "test-wall-calc"
        _make_state(run_id, usd_spent=0.0)

        tracker = BudgetTracker(
            run_id=run_id,
            wall_clock_cap_s=43200,
            gpu_hours_cap=12.0,
            usd_cap=30.0,
            worker_pid=os.getpid(),
        )

        started_ts = 1_000_000.0
        now_ts = 1_000_000.0 + 3600.0  # 已过 1 小时

        with patch("pars.budget.tracker.time.time", return_value=now_ts):
            with patch("pars.budget.tracker._get_started_at_ts", return_value=started_ts):
                with patch("pars.budget.tracker._get_gpu_util_pct", return_value=0.0):
                    status = tracker.tick()

        assert abs(status.wall_s - 3600.0) < 1.0

    def test_tick_writes_wall_clock_to_state_but_not_usd(
        self,
        tmp_runs_dir: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """should update wall_clock_elapsed_s in state.json but not overwrite usd_spent when ticking."""
        monkeypatch.setenv("RECALLKIT_RUN_DIR", str(tmp_runs_dir))
        run_id = "test-write-wall"
        _make_state(run_id, usd_spent=10.0)

        tracker = BudgetTracker(
            run_id=run_id,
            wall_clock_cap_s=43200,
            gpu_hours_cap=12.0,
            usd_cap=30.0,
            worker_pid=os.getpid(),
        )

        started_ts = 1_000_000.0
        now_ts = 1_000_000.0 + 7200.0  # 2 小时

        with patch("pars.budget.tracker.time.time", return_value=now_ts):
            with patch("pars.budget.tracker._get_started_at_ts", return_value=started_ts):
                with patch("pars.budget.tracker._get_gpu_util_pct", return_value=0.0):
                    tracker.tick()

        # 读回 state 验证
        from pars.ledger.state import read_state

        updated = read_state(run_id)
        assert abs(updated.wall_clock_elapsed_s - 7200.0) < 1.0
        # usd_spent 不被 tracker 覆盖
        assert updated.usd_spent == 10.0

    def test_tick_accumulates_gpu_hours_when_gpu_active(
        self,
        tmp_runs_dir: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """should accumulate gpu_hours by 60s tick when gpu_util > 5% and ticking."""
        monkeypatch.setenv("RECALLKIT_RUN_DIR", str(tmp_runs_dir))
        run_id = "test-gpu-accum"
        _make_state(run_id, gpu_hours_used=0.0)

        tracker = BudgetTracker(
            run_id=run_id,
            wall_clock_cap_s=43200,
            gpu_hours_cap=12.0,
            usd_cap=30.0,
            worker_pid=os.getpid(),
        )

        started_ts = 1_000_000.0
        now_ts = 1_000_000.0 + 60.0

        with patch("pars.budget.tracker.time.time", return_value=now_ts):
            with patch("pars.budget.tracker._get_started_at_ts", return_value=started_ts):
                # GPU 活跃(>5%)
                with patch("pars.budget.tracker._get_gpu_util_pct", return_value=80.0):
                    status = tracker.tick()

        # 60s / 3600 = 1/60 h
        expected_gpu_h = 60.0 / 3600.0
        assert abs(status.gpu_h - expected_gpu_h) < 1e-6

    def test_tick_does_not_accumulate_gpu_hours_when_gpu_idle(
        self,
        tmp_runs_dir: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """should not accumulate gpu_hours when gpu_util <= 5% and ticking."""
        monkeypatch.setenv("RECALLKIT_RUN_DIR", str(tmp_runs_dir))
        run_id = "test-gpu-idle"
        _make_state(run_id, gpu_hours_used=0.5)

        tracker = BudgetTracker(
            run_id=run_id,
            wall_clock_cap_s=43200,
            gpu_hours_cap=12.0,
            usd_cap=30.0,
            worker_pid=os.getpid(),
        )

        started_ts = 1_000_000.0
        now_ts = 1_000_000.0 + 60.0

        with patch("pars.budget.tracker.time.time", return_value=now_ts):
            with patch("pars.budget.tracker._get_started_at_ts", return_value=started_ts):
                # GPU 不活跃(≤5%)
                with patch("pars.budget.tracker._get_gpu_util_pct", return_value=3.0):
                    status = tracker.tick()

        # gpu_hours 不变，仍为 0.5
        assert abs(status.gpu_h - 0.5) < 1e-6


# ===========================================================================
# BudgetTracker.check_caps — cap 判断
# ===========================================================================


@pytest.mark.unit
class TestBudgetTrackerCheckCaps:
    """BudgetTracker.check_caps() 返回突破项列表。"""

    def _make_tracker(self, run_id: str) -> BudgetTracker:
        return BudgetTracker(
            run_id=run_id,
            wall_clock_cap_s=3600.0,
            gpu_hours_cap=1.0,
            usd_cap=30.0,
            worker_pid=os.getpid(),
        )

    def test_check_caps_returns_empty_when_all_below_cap(self) -> None:
        """should return empty list when all metrics are below cap."""
        tracker = self._make_tracker("chk-ok")
        status = BudgetStatus(usd_spent=5.0, wall_s=1800.0, gpu_h=0.3)
        breaches = tracker.check_caps(status)
        assert breaches == []

    def test_check_caps_returns_wall_clock_when_wall_clock_exceeds_cap(self) -> None:
        """should return ['wall_clock'] when wall_clock_elapsed > cap."""
        tracker = self._make_tracker("chk-wall")
        # wall_s = 4000 > cap 3600
        status = BudgetStatus(usd_spent=5.0, wall_s=4000.0, gpu_h=0.3)
        breaches = tracker.check_caps(status)
        assert "wall_clock" in breaches

    def test_check_caps_returns_gpu_hours_when_gpu_exceeds_cap(self) -> None:
        """should return ['gpu_hours'] when gpu_hours_used > cap."""
        tracker = self._make_tracker("chk-gpu")
        # gpu_h = 1.5 > cap 1.0
        status = BudgetStatus(usd_spent=5.0, wall_s=1800.0, gpu_h=1.5)
        breaches = tracker.check_caps(status)
        assert "gpu_hours" in breaches

    def test_check_caps_returns_usd_when_usd_exceeds_cap(self) -> None:
        """should return ['usd'] when usd_spent > usd_cap (60s fallback path)."""
        tracker = self._make_tracker("chk-usd")
        # usd_spent = 31.0 > cap 30.0
        status = BudgetStatus(usd_spent=31.0, wall_s=1800.0, gpu_h=0.3)
        breaches = tracker.check_caps(status)
        assert "usd" in breaches

    def test_check_caps_returns_multiple_when_several_caps_breached(self) -> None:
        """should return multiple breach names when more than one cap is exceeded."""
        tracker = self._make_tracker("chk-multi")
        status = BudgetStatus(usd_spent=35.0, wall_s=5000.0, gpu_h=2.0)
        breaches = tracker.check_caps(status)
        assert "wall_clock" in breaches
        assert "gpu_hours" in breaches
        assert "usd" in breaches

    def test_check_caps_at_exact_cap_boundary_triggers_breach(self) -> None:
        """should treat exact cap value as breach (>=) for wall_clock."""
        tracker = self._make_tracker("chk-boundary")
        # wall_s == cap 3600 正好触发
        status = BudgetStatus(usd_spent=5.0, wall_s=3600.0, gpu_h=0.3)
        breaches = tracker.check_caps(status)
        assert "wall_clock" in breaches


# ===========================================================================
# BudgetTracker.current_usage
# ===========================================================================


@pytest.mark.unit
class TestBudgetTrackerCurrentUsage:
    """BudgetTracker.current_usage() 接口。"""

    def test_current_usage_returns_dict_with_wall_s_and_gpu_h(
        self,
        tmp_runs_dir: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """should return dict containing wall_s and gpu_h when calling current_usage."""
        monkeypatch.setenv("RECALLKIT_RUN_DIR", str(tmp_runs_dir))
        run_id = "test-usage"
        _make_state(run_id, usd_spent=5.0, wall_clock_elapsed_s=1800.0, gpu_hours_used=0.5)

        tracker = BudgetTracker(
            run_id=run_id,
            wall_clock_cap_s=43200,
            gpu_hours_cap=12.0,
            usd_cap=30.0,
            worker_pid=os.getpid(),
        )
        result = tracker.current_usage()
        assert "wall_s" in result
        assert "gpu_h" in result


# ===========================================================================
# BudgetTracker._on_cap_exceeded — SIGINT 发送
# ===========================================================================


@pytest.mark.unit
class TestBudgetTrackerOnCapExceeded:
    """BudgetTracker._on_cap_exceeded() 发送 SIGINT 到 worker_pid。"""

    def test_on_cap_exceeded_sends_sigint_to_worker_pid(
        self,
        tmp_runs_dir: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """should call os.kill(worker_pid, SIGINT) when _on_cap_exceeded is called."""
        monkeypatch.setenv("RECALLKIT_RUN_DIR", str(tmp_runs_dir))
        run_id = "test-sigint-send"
        _make_state(run_id)

        worker_pid = 99999  # 非真实 pid，仅验证调用
        tracker = BudgetTracker(
            run_id=run_id,
            wall_clock_cap_s=3600,
            gpu_hours_cap=1.0,
            usd_cap=30.0,
            worker_pid=worker_pid,
        )

        with patch("pars.budget.tracker.os.kill") as mock_kill:
            tracker._on_cap_exceeded("wall_clock")
            mock_kill.assert_called_once_with(worker_pid, signal.SIGINT)

    def test_on_cap_exceeded_logs_reason(
        self,
        tmp_runs_dir: Path,
        monkeypatch: pytest.MonkeyPatch,
        caplog: pytest.LogCaptureFixture,
    ) -> None:
        """should log fatal message mentioning 'SIGINT due to wall_clock cap' when _on_cap_exceeded fires."""
        import logging

        monkeypatch.setenv("RECALLKIT_RUN_DIR", str(tmp_runs_dir))
        run_id = "test-sigint-log"
        _make_state(run_id)

        tracker = BudgetTracker(
            run_id=run_id,
            wall_clock_cap_s=3600,
            gpu_hours_cap=1.0,
            usd_cap=30.0,
            worker_pid=99999,
        )

        with patch("pars.budget.tracker.os.kill"):
            with caplog.at_level(logging.WARNING, logger="pars.budget.tracker"):
                tracker._on_cap_exceeded("wall_clock")

        # 验证日志中有"wall_clock"关键字
        assert any("wall_clock" in r.message for r in caplog.records)

    def test_on_cap_exceeded_usd_fallback_logs_warning(
        self,
        tmp_runs_dir: Path,
        monkeypatch: pytest.MonkeyPatch,
        caplog: pytest.LogCaptureFixture,
    ) -> None:
        """should log warning mentioning 'proxy pre-reject may have missed' when USD cap hits via 60s polling."""
        import logging

        monkeypatch.setenv("RECALLKIT_RUN_DIR", str(tmp_runs_dir))
        run_id = "test-usd-fallback-log"
        _make_state(run_id)

        tracker = BudgetTracker(
            run_id=run_id,
            wall_clock_cap_s=3600,
            gpu_hours_cap=1.0,
            usd_cap=30.0,
            worker_pid=99999,
        )

        with patch("pars.budget.tracker.os.kill"):
            with caplog.at_level(logging.WARNING, logger="pars.budget.tracker"):
                tracker._on_cap_exceeded("usd")

        # 验证包含 proxy pre-reject 警告
        assert any("proxy" in r.message.lower() for r in caplog.records)


# ===========================================================================
# BudgetTracker — wall_clock cap 触发场景
# ===========================================================================


@pytest.mark.unit
class TestBudgetTrackerWallClockCapTrigger:
    """wall_clock 超限时触发 SIGINT。"""

    def test_wall_clock_cap_triggers_sigint_when_elapsed_exceeds_cap(
        self,
        tmp_runs_dir: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """should trigger SIGINT when wall_clock_elapsed > wall_clock_cap_s."""
        monkeypatch.setenv("RECALLKIT_RUN_DIR", str(tmp_runs_dir))
        run_id = "test-wall-trigger"
        _make_state(run_id, usd_spent=0.0)

        worker_pid = 99999
        tracker = BudgetTracker(
            run_id=run_id,
            wall_clock_cap_s=60,  # 60s cap
            gpu_hours_cap=12.0,
            usd_cap=30.0,
            worker_pid=worker_pid,
        )

        started_ts = 1_000_000.0
        now_ts = 1_000_000.0 + 70.0  # 已过 70s > cap 60s

        with patch("pars.budget.tracker.os.kill") as mock_kill:
            with patch("pars.budget.tracker.time.time", return_value=now_ts):
                with patch("pars.budget.tracker._get_started_at_ts", return_value=started_ts):
                    with patch("pars.budget.tracker._get_gpu_util_pct", return_value=0.0):
                        status = tracker.tick()
                        breaches = tracker.check_caps(status)
                        if breaches:
                            for reason in breaches:
                                tracker._on_cap_exceeded(reason)

            assert "wall_clock" in breaches
            mock_kill.assert_called_with(worker_pid, signal.SIGINT)

    def test_wall_clock_below_cap_no_sigint(
        self,
        tmp_runs_dir: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """should not trigger SIGINT when wall_clock_elapsed < wall_clock_cap_s."""
        monkeypatch.setenv("RECALLKIT_RUN_DIR", str(tmp_runs_dir))
        run_id = "test-wall-safe"
        _make_state(run_id, usd_spent=0.0)

        tracker = BudgetTracker(
            run_id=run_id,
            wall_clock_cap_s=43200,  # 12h cap
            gpu_hours_cap=12.0,
            usd_cap=30.0,
            worker_pid=99999,
        )

        started_ts = 1_000_000.0
        now_ts = 1_000_000.0 + 3600.0  # 仅 1 小时

        with patch("pars.budget.tracker.os.kill") as mock_kill:
            with patch("pars.budget.tracker.time.time", return_value=now_ts):
                with patch("pars.budget.tracker._get_started_at_ts", return_value=started_ts):
                    with patch("pars.budget.tracker._get_gpu_util_pct", return_value=0.0):
                        status = tracker.tick()
                        breaches = tracker.check_caps(status)

            assert breaches == []
            mock_kill.assert_not_called()


# ===========================================================================
# BudgetTracker — GPU hours cap 触发场景
# ===========================================================================


@pytest.mark.unit
class TestBudgetTrackerGpuHoursCapTrigger:
    """gpu_hours 超限时触发 SIGINT。"""

    def test_gpu_hours_cap_triggers_sigint_when_accumulated_exceeds_cap(
        self,
        tmp_runs_dir: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """should trigger SIGINT when accumulated gpu_hours > gpu_hours_cap."""
        monkeypatch.setenv("RECALLKIT_RUN_DIR", str(tmp_runs_dir))
        run_id = "test-gpu-trigger"
        # state 中已经积累了 1.1h GPU 时间
        _make_state(run_id, gpu_hours_used=1.1)

        worker_pid = 99999
        tracker = BudgetTracker(
            run_id=run_id,
            wall_clock_cap_s=43200,
            gpu_hours_cap=1.0,  # cap = 1.0h
            usd_cap=30.0,
            worker_pid=worker_pid,
        )

        started_ts = 1_000_000.0
        now_ts = 1_000_000.0 + 60.0

        with patch("pars.budget.tracker.os.kill") as mock_kill:
            with patch("pars.budget.tracker.time.time", return_value=now_ts):
                with patch("pars.budget.tracker._get_started_at_ts", return_value=started_ts):
                    # GPU 活跃
                    with patch("pars.budget.tracker._get_gpu_util_pct", return_value=90.0):
                        status = tracker.tick()
                        breaches = tracker.check_caps(status)
                        if breaches:
                            for reason in breaches:
                                tracker._on_cap_exceeded(reason)

            assert "gpu_hours" in breaches
            mock_kill.assert_called_with(worker_pid, signal.SIGINT)

    def test_gpu_hours_below_cap_no_sigint(
        self,
        tmp_runs_dir: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """should not trigger SIGINT when gpu_hours < gpu_hours_cap."""
        monkeypatch.setenv("RECALLKIT_RUN_DIR", str(tmp_runs_dir))
        run_id = "test-gpu-safe"
        _make_state(run_id, gpu_hours_used=0.1)

        tracker = BudgetTracker(
            run_id=run_id,
            wall_clock_cap_s=43200,
            gpu_hours_cap=12.0,  # cap = 12h，远高于当前
            usd_cap=30.0,
            worker_pid=99999,
        )

        started_ts = 1_000_000.0
        now_ts = 1_000_000.0 + 60.0

        with patch("pars.budget.tracker.os.kill") as mock_kill:
            with patch("pars.budget.tracker.time.time", return_value=now_ts):
                with patch("pars.budget.tracker._get_started_at_ts", return_value=started_ts):
                    with patch("pars.budget.tracker._get_gpu_util_pct", return_value=90.0):
                        status = tracker.tick()
                        breaches = tracker.check_caps(status)

            assert breaches == []
            mock_kill.assert_not_called()


# ===========================================================================
# BudgetMonitor — 60s 轮询行为
# ===========================================================================


@pytest.mark.unit
class TestBudgetMonitorPollInterval:
    """BudgetMonitor 60s 轮询间隔验证。"""

    def test_60s_poll_interval_calls_sleep_60(
        self,
        tmp_runs_dir: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """should call time.sleep(60) between polls when BudgetMonitor is running."""
        monkeypatch.setenv("RECALLKIT_RUN_DIR", str(tmp_runs_dir))
        run_id = "test-monitor-sleep"
        _make_state(run_id)

        stop_event = Event()
        poll_count = 0

        def fake_sleep(seconds: float) -> None:
            nonlocal poll_count
            assert seconds == 60.0, f"期望 sleep(60),实际 sleep({seconds})"
            poll_count += 1
            if poll_count >= 2:
                stop_event.set()

        tracker = BudgetTracker(
            run_id=run_id,
            wall_clock_cap_s=43200,
            gpu_hours_cap=12.0,
            usd_cap=30.0,
            worker_pid=os.getpid(),
        )
        monitor = BudgetMonitor(tracker=tracker, poll_interval_s=60.0)

        with patch("pars.budget.tracker.time.sleep", side_effect=fake_sleep):
            with patch("pars.budget.tracker.time.time", return_value=1_000_000.0):
                with patch("pars.budget.tracker._get_started_at_ts", return_value=999_999_000.0):
                    with patch("pars.budget.tracker._get_gpu_util_pct", return_value=0.0):
                        monitor.start()
                        stop_event.wait(timeout=5.0)
                        monitor.stop()
                        monitor.join(timeout=3.0)

        assert poll_count >= 2, f"期望至少 2 次 sleep，实际 {poll_count} 次"

    def test_monitor_stops_when_stop_called(
        self,
        tmp_runs_dir: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """should exit poll loop when stop() is called on BudgetMonitor."""
        import threading  # noqa: PLC0415

        monkeypatch.setenv("RECALLKIT_RUN_DIR", str(tmp_runs_dir))
        run_id = "test-monitor-stop"
        _make_state(run_id)

        tracker = BudgetTracker(
            run_id=run_id,
            wall_clock_cap_s=43200,
            gpu_hours_cap=12.0,
            usd_cap=30.0,
            worker_pid=os.getpid(),
        )

        started_event = Event()
        # 用 threading.Event 替代 time.sleep 避免 mock 递归
        _blocker = threading.Event()

        def fake_sleep(seconds: float) -> None:
            started_event.set()
            # 等待最多 0.5s（不调用被 mock 的 time.sleep）
            _blocker.wait(timeout=0.5)

        monitor = BudgetMonitor(tracker=tracker, poll_interval_s=60.0)

        with patch("pars.budget.tracker.time.sleep", side_effect=fake_sleep):
            with patch("pars.budget.tracker.time.time", return_value=1_000_000.0):
                with patch("pars.budget.tracker._get_started_at_ts", return_value=999_999_000.0):
                    with patch("pars.budget.tracker._get_gpu_util_pct", return_value=0.0):
                        monitor.start()
                        started_event.wait(timeout=3.0)
                        monitor.stop()
                        _blocker.set()  # 让 fake_sleep 立即返回
                        monitor.join(timeout=3.0)

        assert not monitor.is_alive(), "BudgetMonitor 应在 stop() 后停止"
