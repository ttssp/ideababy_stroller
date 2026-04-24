"""
test_stuck_probes.py — probes.py 单测（mock 所有外部调用）。

所有 probe 函数是纯函数（input = snapshot dict / subprocess，output = 数值），
用 monkeypatch mock 掉 subprocess.run（nvidia-smi）和 psutil。

Probe 函数约定：
- probe_gpu_util() -> float | None
- probe_process_cpu(pid, recursive=True) -> float
- probe_disk_io(prev) -> tuple[float, dict]    # 返回 MB/s + 新快照
- probe_net_io(prev) -> tuple[float, dict]      # 返回 MB/s + 新快照
"""

from __future__ import annotations

import subprocess
from unittest.mock import MagicMock, patch

import pytest

from pars.stuck.probes import (
    probe_disk_io,
    probe_gpu_util,
    probe_net_io,
    probe_process_cpu,
)


# ---------------------------------------------------------------------------
# probe_gpu_util
# ---------------------------------------------------------------------------

class TestProbeGpuUtil:
    """probe_gpu_util：调 nvidia-smi 解析 GPU 利用率。"""

    def test_should_return_float_when_nvidia_smi_succeeds(self, monkeypatch):
        """nvidia-smi 正常返回时，解析 GPU 利用率数值。"""
        fake_result = MagicMock()
        fake_result.returncode = 0
        fake_result.stdout = "42\n"

        monkeypatch.setattr(
            "pars.stuck.probes.subprocess.run",
            lambda *args, **kwargs: fake_result,
        )
        result = probe_gpu_util()
        assert result == 42.0

    def test_should_return_none_when_nvidia_smi_not_found(self, monkeypatch):
        """nvidia-smi 不存在（FileNotFoundError）时，返回 None（无 GPU 降级）。"""
        def _raise(*args, **kwargs):
            raise FileNotFoundError("nvidia-smi not found")

        monkeypatch.setattr("pars.stuck.probes.subprocess.run", _raise)
        result = probe_gpu_util()
        assert result is None

    def test_should_return_none_when_nvidia_smi_nonzero_exit(self, monkeypatch):
        """nvidia-smi 返回非零退出码时，返回 None。"""
        fake_result = MagicMock()
        fake_result.returncode = 1
        fake_result.stdout = ""

        monkeypatch.setattr(
            "pars.stuck.probes.subprocess.run",
            lambda *args, **kwargs: fake_result,
        )
        result = probe_gpu_util()
        assert result is None

    def test_should_return_none_when_nvidia_smi_output_invalid(self, monkeypatch):
        """nvidia-smi 输出无法解析为数字时，返回 None。"""
        fake_result = MagicMock()
        fake_result.returncode = 0
        fake_result.stdout = "[N/A]\n"

        monkeypatch.setattr(
            "pars.stuck.probes.subprocess.run",
            lambda *args, **kwargs: fake_result,
        )
        result = probe_gpu_util()
        assert result is None

    def test_should_return_zero_when_gpu_idle(self, monkeypatch):
        """GPU 空闲时返回 0.0。"""
        fake_result = MagicMock()
        fake_result.returncode = 0
        fake_result.stdout = "0\n"

        monkeypatch.setattr(
            "pars.stuck.probes.subprocess.run",
            lambda *args, **kwargs: fake_result,
        )
        result = probe_gpu_util()
        assert result == 0.0

    def test_should_return_none_when_called_process_error(self, monkeypatch):
        """subprocess.CalledProcessError 时，返回 None（兜底）。"""
        def _raise(*args, **kwargs):
            raise subprocess.CalledProcessError(1, "nvidia-smi")

        monkeypatch.setattr("pars.stuck.probes.subprocess.run", _raise)
        result = probe_gpu_util()
        assert result is None


# ---------------------------------------------------------------------------
# probe_process_cpu
# ---------------------------------------------------------------------------

class TestProbeProcessCpu:
    """probe_process_cpu：psutil 读取子进程 CPU% 累加。"""

    def test_should_return_sum_of_children_cpu_when_processes_exist(self, monkeypatch):
        """有 2 个子进程时，返回 CPU% 累加值。"""
        import psutil

        mock_child1 = MagicMock()
        mock_child1.cpu_percent.return_value = 30.0
        mock_child2 = MagicMock()
        mock_child2.cpu_percent.return_value = 20.0

        mock_proc = MagicMock()
        mock_proc.children.return_value = [mock_child1, mock_child2]

        monkeypatch.setattr("pars.stuck.probes.psutil.Process", lambda pid: mock_proc)
        result = probe_process_cpu(pid=1234)
        assert result == 50.0

    def test_should_return_zero_when_pid_not_found(self, monkeypatch):
        """pid 不存在（NoSuchProcess）时，返回 0（防护父进程已死）。"""
        import psutil

        def _raise(pid):
            raise psutil.NoSuchProcess(pid)

        monkeypatch.setattr("pars.stuck.probes.psutil.Process", _raise)
        result = probe_process_cpu(pid=9999)
        assert result == 0.0

    def test_should_return_zero_when_no_children(self, monkeypatch):
        """进程无子进程时，返回 0.0。"""
        mock_proc = MagicMock()
        mock_proc.children.return_value = []

        monkeypatch.setattr("pars.stuck.probes.psutil.Process", lambda pid: mock_proc)
        result = probe_process_cpu(pid=1234)
        assert result == 0.0

    def test_should_include_recursive_children_when_recursive_true(self, monkeypatch):
        """recursive=True 时，调用 proc.children(recursive=True)。"""
        mock_child = MagicMock()
        mock_child.cpu_percent.return_value = 15.0
        mock_proc = MagicMock()
        mock_proc.children.return_value = [mock_child]

        monkeypatch.setattr("pars.stuck.probes.psutil.Process", lambda pid: mock_proc)
        result = probe_process_cpu(pid=1234, recursive=True)
        mock_proc.children.assert_called_once_with(recursive=True)
        assert result == 15.0


# ---------------------------------------------------------------------------
# probe_disk_io
# ---------------------------------------------------------------------------

class TestProbeDiskIo:
    """probe_disk_io：psutil.disk_io_counters 增量 MB/s + 新快照。"""

    def test_should_return_zero_mbs_when_prev_is_none(self, monkeypatch):
        """prev=None（首次调用）时，返回 delta=0.0 + 新快照。"""
        mock_counters = MagicMock()
        mock_counters.read_bytes = 1000
        mock_counters.write_bytes = 2000

        monkeypatch.setattr(
            "pars.stuck.probes.psutil.disk_io_counters",
            lambda: mock_counters,
        )
        delta_mbs, snapshot = probe_disk_io(prev=None)
        assert delta_mbs == 0.0
        assert snapshot["read_bytes"] == 1000
        assert snapshot["write_bytes"] == 2000

    def test_should_compute_correct_delta_when_prev_provided(self, monkeypatch):
        """有 prev 时，返回增量 MB/s（elapsed 假设 5s）。"""
        mock_counters = MagicMock()
        mock_counters.read_bytes = 1_000_000 + 10_000_000  # +10MB
        mock_counters.write_bytes = 2_000_000 + 15_000_000  # +15MB

        monkeypatch.setattr(
            "pars.stuck.probes.psutil.disk_io_counters",
            lambda: mock_counters,
        )
        prev = {
            "read_bytes": 1_000_000,
            "write_bytes": 2_000_000,
            "timestamp": 0.0,
        }
        # 5 秒后，delta = (10+15)MB / 5s = 5.0 MB/s
        delta_mbs, snapshot = probe_disk_io(prev=prev, interval_s=5.0)
        assert abs(delta_mbs - 5.0) < 0.01

    def test_should_return_zero_when_no_disk_io_counters(self, monkeypatch):
        """psutil.disk_io_counters() 返回 None（无磁盘）时，返回 0.0。"""
        monkeypatch.setattr(
            "pars.stuck.probes.psutil.disk_io_counters",
            lambda: None,
        )
        delta_mbs, snapshot = probe_disk_io(prev=None)
        assert delta_mbs == 0.0
        assert snapshot == {}


# ---------------------------------------------------------------------------
# probe_net_io
# ---------------------------------------------------------------------------

class TestProbeNetIo:
    """probe_net_io：psutil.net_io_counters 增量 MB/s + 新快照。"""

    def test_should_return_zero_mbs_when_prev_is_none(self, monkeypatch):
        """prev=None 时，返回 0.0 + 新快照。"""
        mock_counters = MagicMock()
        mock_counters.bytes_recv = 5000
        mock_counters.bytes_sent = 1000

        monkeypatch.setattr(
            "pars.stuck.probes.psutil.net_io_counters",
            lambda: mock_counters,
        )
        delta_mbs, snapshot = probe_net_io(prev=None)
        assert delta_mbs == 0.0
        assert snapshot["bytes_recv"] == 5000

    def test_should_compute_correct_net_delta_when_prev_provided(self, monkeypatch):
        """有 prev 时，计算网络增量 MB/s（主要看 bytes_recv 用于下载检测）。"""
        mock_counters = MagicMock()
        mock_counters.bytes_recv = 0 + 20_000_000  # +20MB
        mock_counters.bytes_sent = 0 + 2_000_000    # +2MB

        monkeypatch.setattr(
            "pars.stuck.probes.psutil.net_io_counters",
            lambda: mock_counters,
        )
        prev = {
            "bytes_recv": 0,
            "bytes_sent": 0,
            "timestamp": 0.0,
        }
        # 5s, recv=20MB, sent=2MB, total=(20+2)/5 = 4.4 MB/s
        delta_mbs, snapshot = probe_net_io(prev=prev, interval_s=5.0)
        assert abs(delta_mbs - 4.4) < 0.01
