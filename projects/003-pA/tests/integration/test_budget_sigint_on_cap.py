"""
tests.integration.test_budget_sigint_on_cap — BudgetMonitor SIGINT 集成测试（T018）。

结论：
  验证 BudgetMonitor 在 wall_clock / gpu_hours 超限时，真实发送 SIGINT 到 worker 进程，
  worker 进程捕获 SIGINT 后写 failure_attribution.md。

策略：
  - 启动真实 subprocess（Python 子进程，内置 SIGINT handler）
  - BudgetMonitor 在主进程监控，超限即 os.kill(worker_pid, SIGINT)
  - 子进程写 failure_attribution.md 表示收到 SIGINT
  - 验证 failure_attribution.md 存在且内容含"SIGINT"

注意：
  - USD cap 路径由 T010 test_proxy_prerejects_on_budget.py 覆盖，本文件不重复
  - 轮询间隔在集成测试中设为 0.5s（非 60s），便于快速验证
"""

from __future__ import annotations

import os
import signal
import subprocess
import sys
import textwrap
import time
from pathlib import Path

import pytest


# ---------------------------------------------------------------------------
# 子进程脚本：等待 SIGINT，收到后写 failure_attribution.md
# ---------------------------------------------------------------------------


_WORKER_SCRIPT = textwrap.dedent(
    """\
    import signal
    import sys
    import time
    from pathlib import Path

    output_file = Path(sys.argv[1])
    output_file.parent.mkdir(parents=True, exist_ok=True)

    def _on_sigint(signum, frame):
        output_file.write_text("SIGINT received\\n", encoding="utf-8")
        sys.exit(130)  # 130 = 128 + SIGINT(2)

    signal.signal(signal.SIGINT, _on_sigint)

    # 等最多 30 秒
    for _ in range(300):
        time.sleep(0.1)

    # 未收到 SIGINT，超时退出
    output_file.write_text("timeout_no_sigint\\n", encoding="utf-8")
    sys.exit(0)
    """
)


# ---------------------------------------------------------------------------
# 辅助：写最小 state.json
# ---------------------------------------------------------------------------


def _write_state(
    run_dir: Path,
    *,
    usd_spent: float = 0.0,
    gpu_hours_used: float = 0.0,
    wall_clock_elapsed_s: float = 0.0,
) -> None:
    """写最小合法 state.json（含 T018 需要的字段）。"""
    import json
    from datetime import UTC, datetime

    state_path = run_dir / "state.json"
    state_path.parent.mkdir(parents=True, exist_ok=True)
    data = {
        "run_id": run_dir.name,
        "phase": "lora_train",
        "current_script": None,
        "checkpoint_path": None,
        "last_epoch_completed": None,
        "stuck_state": "idle",
        "stuck_restart_count": 0,
        "needs_human_review": False,
        "usd_spent": usd_spent,
        "wall_clock_elapsed_s": wall_clock_elapsed_s,
        "gpu_hours_used": gpu_hours_used,
        "last_update": datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%S.%f+00:00"),
    }
    state_path.write_text(json.dumps(data, indent=2), encoding="utf-8")


# ===========================================================================
# 集成测试
# ===========================================================================


@pytest.mark.integration
class TestBudgetMonitorSigintOnWallClock:
    """wall_clock 超限 → BudgetMonitor 向 worker 发 SIGINT。"""

    def test_wall_clock_cap_triggers_sigint_to_real_subprocess(
        self,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """should send SIGINT to worker subprocess when wall_clock exceeds cap."""
        from unittest.mock import patch

        from pars.budget.tracker import BudgetMonitor, BudgetTracker

        # 准备文件系统
        runs_dir = tmp_path / "runs"
        run_id = "integ-wall-sigint"
        run_dir = runs_dir / run_id
        run_dir.mkdir(parents=True, exist_ok=True)
        monkeypatch.setenv("RECALLKIT_RUN_DIR", str(runs_dir))

        # 写 state：wall_clock 已经 70s
        _write_state(run_dir, wall_clock_elapsed_s=0.0)

        # 启动 worker 子进程
        attr_file = run_dir / "failure_attribution.md"
        worker = subprocess.Popen(
            [sys.executable, "-c", _WORKER_SCRIPT, str(attr_file)],
            start_new_session=False,
        )
        worker_pid = worker.pid

        try:
            # BudgetTracker：wall_clock_cap = 1s（极小值，立即超限）
            tracker = BudgetTracker(
                run_id=run_id,
                wall_clock_cap_s=1,  # 极小 cap，保证超限
                gpu_hours_cap=12.0,
                usd_cap=30.0,
                worker_pid=worker_pid,
            )

            # mock started_at 为 100s 前，使 wall_clock = 100s > cap 1s
            started_ts = time.time() - 100.0

            # mock GPU 无活跃（避免 gpu_hours 也触发）
            with patch("pars.budget.tracker._get_started_at_ts", return_value=started_ts):
                with patch("pars.budget.tracker._get_gpu_util_pct", return_value=0.0):
                    monitor = BudgetMonitor(tracker=tracker, poll_interval_s=0.5)
                    # 等待子进程安装 SIGINT handler（避免 SIGINT 在 handler 装好前到达）
                    time.sleep(0.3)
                    monitor.start()
                    # 等待 worker 收到 SIGINT（最多 5s）
                    worker.wait(timeout=5.0)
                    monitor.stop()
                    monitor.join(timeout=3.0)

        finally:
            # 清理：若 worker 仍活着，强制终止
            if worker.poll() is None:
                worker.kill()
                worker.wait()

        # 断言：worker 收到 SIGINT 并退出
        # - returncode 130：自定义 handler 运行 sys.exit(130)（shell 惯例 128+SIGINT）
        # - returncode -2 ：Popen 检测到进程被 SIGINT 终止（POSIX 原始信号 -signal.SIGINT）
        _sigint_exit_codes = (130, -signal.SIGINT)
        assert worker.returncode in _sigint_exit_codes, (
            f"期望退出码为 130 或 {-signal.SIGINT}（SIGINT），实际 {worker.returncode}"
        )
        # 断言：failure_attribution.md 存在且内容含 SIGINT（仅 handler 正常运行时）
        # 若 returncode == -signal.SIGINT，说明 SIGINT 在 handler 前到达 → 文件可能不存在
        if worker.returncode == 130:
            assert attr_file.exists(), "failure_attribution.md 应该被 worker handler 创建"
            content = attr_file.read_text(encoding="utf-8")
            assert "SIGINT" in content


@pytest.mark.integration
class TestBudgetMonitorSigintOnGpuHours:
    """gpu_hours 超限 → BudgetMonitor 向 worker 发 SIGINT。"""

    def test_gpu_hours_cap_triggers_sigint_to_real_subprocess(
        self,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """should send SIGINT to worker subprocess when gpu_hours exceeds cap."""
        from unittest.mock import patch

        from pars.budget.tracker import BudgetMonitor, BudgetTracker

        # 准备文件系统
        runs_dir = tmp_path / "runs"
        run_id = "integ-gpu-sigint"
        run_dir = runs_dir / run_id
        run_dir.mkdir(parents=True, exist_ok=True)
        monkeypatch.setenv("RECALLKIT_RUN_DIR", str(runs_dir))

        # state 中 GPU hours 已经 1.5h > cap 1.0h
        _write_state(run_dir, gpu_hours_used=1.5)

        # 启动 worker 子进程
        attr_file = run_dir / "failure_attribution.md"
        worker = subprocess.Popen(
            [sys.executable, "-c", _WORKER_SCRIPT, str(attr_file)],
            start_new_session=False,
        )
        worker_pid = worker.pid

        try:
            # BudgetTracker：gpu_hours_cap = 1.0（state 已超 1.5h）
            tracker = BudgetTracker(
                run_id=run_id,
                wall_clock_cap_s=43200,  # 12h，不触发
                gpu_hours_cap=1.0,  # cap，已被超
                usd_cap=30.0,
                worker_pid=worker_pid,
            )

            started_ts = time.time() - 60.0  # 仅 60s wall_clock，不超 12h cap

            # GPU 活跃，但 state 里已积累 1.5h
            with patch("pars.budget.tracker._get_started_at_ts", return_value=started_ts):
                with patch("pars.budget.tracker._get_gpu_util_pct", return_value=80.0):
                    monitor = BudgetMonitor(tracker=tracker, poll_interval_s=0.5)
                    # 等待子进程安装 SIGINT handler（避免 SIGINT 在 handler 装好前到达）
                    time.sleep(0.3)
                    monitor.start()
                    worker.wait(timeout=5.0)
                    monitor.stop()
                    monitor.join(timeout=3.0)

        finally:
            if worker.poll() is None:
                worker.kill()
                worker.wait()

        # 断言：worker 收到 SIGINT 并退出
        # - returncode 130：自定义 handler 运行 sys.exit(130)
        # - returncode -2 ：Popen 检测到进程被 SIGINT 终止（POSIX 原始信号）
        _sigint_exit_codes = (130, -signal.SIGINT)
        assert worker.returncode in _sigint_exit_codes, (
            f"期望退出码为 130 或 {-signal.SIGINT}（SIGINT），实际 {worker.returncode}"
        )
        if worker.returncode == 130:
            assert attr_file.exists(), "failure_attribution.md 应该被 worker handler 创建"
            content = attr_file.read_text(encoding="utf-8")
            assert "SIGINT" in content


@pytest.mark.integration
class TestBudgetMonitorNoSigintWhenBelowCap:
    """全部指标低于 cap → BudgetMonitor 不发 SIGINT。"""

    def test_below_cap_no_sigint_sent_to_subprocess(
        self,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """should not send SIGINT when all metrics are below cap."""
        from unittest.mock import patch

        from pars.budget.tracker import BudgetMonitor, BudgetTracker

        runs_dir = tmp_path / "runs"
        run_id = "integ-safe"
        run_dir = runs_dir / run_id
        run_dir.mkdir(parents=True, exist_ok=True)
        monkeypatch.setenv("RECALLKIT_RUN_DIR", str(runs_dir))

        _write_state(run_dir, usd_spent=5.0, gpu_hours_used=0.5)

        attr_file = run_dir / "failure_attribution.md"
        worker = subprocess.Popen(
            [sys.executable, "-c", _WORKER_SCRIPT, str(attr_file)],
            start_new_session=False,
        )
        worker_pid = worker.pid

        try:
            tracker = BudgetTracker(
                run_id=run_id,
                wall_clock_cap_s=43200,  # 12h cap
                gpu_hours_cap=12.0,  # 12h cap
                usd_cap=30.0,
                worker_pid=worker_pid,
            )

            # wall_clock = 60s，远低于 cap
            started_ts = time.time() - 60.0

            with patch("pars.budget.tracker._get_started_at_ts", return_value=started_ts):
                with patch("pars.budget.tracker._get_gpu_util_pct", return_value=50.0):
                    monitor = BudgetMonitor(tracker=tracker, poll_interval_s=0.5)
                    monitor.start()
                    # 等 2s，观察 worker 是否被干扰
                    time.sleep(2.0)
                    monitor.stop()
                    monitor.join(timeout=3.0)

        finally:
            # 正常终止 worker（不是 SIGINT）
            if worker.poll() is None:
                worker.terminate()
                worker.wait(timeout=3.0)
            if worker.poll() is None:
                worker.kill()
                worker.wait()

        # worker 不应以 130 退出（SIGINT）
        assert worker.returncode != 130, (
            f"worker 不应收到 SIGINT，但退出码是 {worker.returncode}"
        )
        # failure_attribution.md 不含 SIGINT（要么不存在，要么是 timeout）
        if attr_file.exists():
            content = attr_file.read_text(encoding="utf-8")
            assert "SIGINT" not in content
