"""
pars.stuck.probes — GPU/CPU/disk/net 探针（纯函数，可 100% mock 测试）。

结论：每个 probe 是独立纯函数，无副作用，读取系统状态并返回数值。
无 GPU 时 probe_gpu_util() 返回 None，上层 SM 降级处理（忽略该信号）。
pid 已死时 probe_process_cpu() 返回 0（安全降级）。

Probe 返回格式：
- probe_gpu_util()    -> float | None   0-100%
- probe_process_cpu() -> float           累加 CPU%
- probe_disk_io()     -> (float, dict)   (MB/s, 新快照)
- probe_net_io()      -> (float, dict)   (MB/s, 新快照)
"""

from __future__ import annotations

import subprocess
from typing import Any

import psutil

from pars.logging import get_logger

logger = get_logger(__name__)


# ---------------------------------------------------------------------------
# probe_gpu_util
# ---------------------------------------------------------------------------

def probe_gpu_util() -> float | None:
    """通过 nvidia-smi 读取 GPU 利用率（%）。

    无 GPU / 驱动不可用时返回 None，上层 SM 忽略该信号（降级到 CPU+IO）。

    返回：
        float : GPU 利用率 0.0-100.0
        None  : nvidia-smi 不可用 / 解析失败
    """
    try:
        result = subprocess.run(
            [
                "nvidia-smi",
                "--query-gpu=utilization.gpu",
                "--format=csv,noheader,nounits",
            ],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode != 0:
            return None
        raw = result.stdout.strip()
        return float(raw)
    except FileNotFoundError:
        # nvidia-smi 不存在（macOS 开发机等）
        return None
    except (ValueError, TypeError):
        # 输出无法解析为数字（如 "[N/A]"）
        logger.debug("probe_gpu_util: 无法解析 nvidia-smi 输出", extra={"output": result.stdout})
        return None
    except subprocess.CalledProcessError:
        return None
    except subprocess.TimeoutExpired:
        logger.warning("probe_gpu_util: nvidia-smi 超时（5s）")
        return None
    except Exception as exc:
        logger.warning("probe_gpu_util: 未知异常", exc_info=exc)
        return None


# ---------------------------------------------------------------------------
# probe_process_cpu
# ---------------------------------------------------------------------------

def probe_process_cpu(pid: int, recursive: bool = True) -> float:
    """读取指定 pid 的所有子进程 CPU% 累加值。

    pid 已死（NoSuchProcess）时返回 0（安全降级）。

    参数：
        pid       : 要监控的主进程 pid（worker 进程）
        recursive : 是否递归包含所有后代进程

    返回：
        float : 所有子进程 CPU% 的累加值（0.0 表示无活动）
    """
    try:
        proc = psutil.Process(pid)
        children = proc.children(recursive=recursive)
        total = sum(child.cpu_percent() for child in children)
        return float(total)
    except psutil.NoSuchProcess:
        logger.debug("probe_process_cpu: pid=%d 已不存在", pid)
        return 0.0
    except Exception as exc:
        logger.warning("probe_process_cpu: 异常", exc_info=exc)
        return 0.0


# ---------------------------------------------------------------------------
# probe_disk_io
# ---------------------------------------------------------------------------

def probe_disk_io(
    prev: dict[str, Any] | None,
    interval_s: float = 5.0,
) -> tuple[float, dict]:
    """读取全局磁盘 IO 增量，返回 (MB/s, 新快照)。

    首次调用（prev=None）时 delta=0.0，仅返回快照供下次计算。

    参数：
        prev       : 上次快照 {"read_bytes": int, "write_bytes": int, "timestamp": float}
                     None 表示首次调用
        interval_s : 采样间隔秒数（用于归一化 MB/s）；默认 5s 对齐 §8.1

    返回：
        (delta_mbs, new_snapshot) : 增量 MB/s + 新快照 dict
    """
    counters = psutil.disk_io_counters()
    if counters is None:
        return 0.0, {}

    new_snap = {
        "read_bytes": counters.read_bytes,
        "write_bytes": counters.write_bytes,
    }

    if prev is None or not prev:
        return 0.0, new_snap

    delta_bytes = (
        (counters.read_bytes - prev["read_bytes"])
        + (counters.write_bytes - prev["write_bytes"])
    )
    delta_mbs = max(0.0, delta_bytes) / 1_000_000 / interval_s
    return delta_mbs, new_snap


# ---------------------------------------------------------------------------
# probe_net_io
# ---------------------------------------------------------------------------

def probe_net_io(
    prev: dict[str, Any] | None,
    interval_s: float = 5.0,
) -> tuple[float, dict]:
    """读取全局网络 IO 增量，返回 (MB/s, 新快照)。

    注意：计算 recv + sent 总量，用于检测 HF 下载（下载时 recv 为主）。

    参数：
        prev       : 上次快照 {"bytes_recv": int, "bytes_sent": int}
        interval_s : 采样间隔秒数

    返回：
        (delta_mbs, new_snapshot) : 增量 MB/s + 新快照 dict
    """
    counters = psutil.net_io_counters()
    if counters is None:
        return 0.0, {}

    new_snap = {
        "bytes_recv": counters.bytes_recv,
        "bytes_sent": counters.bytes_sent,
    }

    if prev is None or not prev:
        return 0.0, new_snap

    delta_bytes = (
        (counters.bytes_recv - prev["bytes_recv"])
        + (counters.bytes_sent - prev["bytes_sent"])
    )
    delta_mbs = max(0.0, delta_bytes) / 1_000_000 / interval_s
    return delta_mbs, new_snap
