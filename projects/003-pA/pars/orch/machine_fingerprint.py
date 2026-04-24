"""
pars.orch.machine_fingerprint — 机器指纹采集与比对（C22 · T019）。

结论：resume 前检测机器指纹，防止跨机器 resume 引起训练不一致。
      hard_reject 字段不一致时阻断 resume；warning 字段不一致时仅记录警告。

### 指纹字段分类（architecture.md §10 · T019 · C22）

| 字段          | 来源                            | 类型     | 说明                          |
|---------------|---------------------------------|----------|-------------------------------|
| gpu_name      | nvidia-smi --query-gpu=name     | str|None | GPU 型号；无 GPU → None       |
| cuda_version  | nvidia-smi --query-gpu=driver_model.current + nvcc | str|None | 主次版本，如 "12.4"           |
| python_version| sys.version_info                | str      | 完整版本，如 "3.12.4"         |
| os_name       | platform.system()               | str      | "Darwin" / "Linux" / ...      |
| os_release    | platform.release()              | str      | 完整小版本，如 "25.2.0"       |

派生字段（不存储，仅用于 diff）：
    os_major = f"{os_name} {os_release.split('.')[0]}"
    例: "Darwin 25" / "Linux 6"

### hard_reject_fields（不一致 → 阻断 resume）

- gpu_name      (e.g. "NVIDIA GeForce RTX 4090")
- cuda_version  (主次版本, e.g. "12.4"；patch 不比较)
- os_major      (派生, e.g. "Darwin 25" / "Linux 6")

### warning_fields（不一致 → 仅警告、不阻断）

- python_version (任何 Python patch 升级，例 3.12.4 → 3.12.5)
- os_release     (精确小版本变化，os_major 不变时)

### 文件路径

runs/<run_id>/machine_fingerprint.json （独立文件，便于 rsync 审计）
"""

from __future__ import annotations

import json
import platform
import subprocess
import sys
import tempfile
from pathlib import Path

from pars.logging import get_logger
from pars.paths import run_dir

logger = get_logger(__name__)


# ---------------------------------------------------------------------------
# 常量：字段分类
# ---------------------------------------------------------------------------

#: hard_reject_fields: 不一致时阻断 resume
HARD_REJECT_FIELDS: frozenset[str] = frozenset({"gpu_name", "cuda_version"})
# os_major 是派生字段，不直接存在指纹 dict 中，在 diff_fingerprint 中单独处理

#: warning_fields: 不一致时仅警告，不阻断
WARNING_FIELDS: frozenset[str] = frozenset({"python_version", "os_release"})


# ---------------------------------------------------------------------------
# 内部辅助：GPU / CUDA 探测
# ---------------------------------------------------------------------------

def _query_nvidia_smi() -> tuple[str | None, str | None]:
    """通过 nvidia-smi 查询 GPU 名称和 CUDA 版本。

    返回：
        (gpu_name, cuda_version_major_minor) —— 无 GPU 时均为 None。
        cuda_version 只保留 "major.minor"，如 "12.4"（丢弃 patch）。

    实现细节：
    - nvidia-smi --query-gpu=name,driver_version --format=csv,noheader,nounits
      在有 GPU 机器返回：NVIDIA GeForce RTX 4090, 535.54.03
    - CUDA 版本从 nvidia-smi 中的 CUDA Version 行解析，而非 driver_version
      使用 nvidia-smi 的 -q 模式更可靠
    """
    try:
        # 方法1：从 nvidia-smi --query-gpu 获取 GPU 名称 + CUDA version
        result = subprocess.run(
            ["nvidia-smi", "--query-gpu=name", "--format=csv,noheader,nounits"],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
        if result.returncode != 0:
            return None, None

        gpu_name = result.stdout.strip().splitlines()[0].strip()
        if not gpu_name:
            return None, None

        # 方法2：从 nvidia-smi -q 的头部解析 CUDA Version
        cuda_result = subprocess.run(
            ["nvidia-smi", "-q"],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
        cuda_version: str | None = None
        if cuda_result.returncode == 0:
            for line in cuda_result.stdout.splitlines():
                line = line.strip()
                if line.startswith("CUDA Version"):
                    # 格式：CUDA Version                      : 12.4
                    parts = line.split(":")
                    if len(parts) >= 2:
                        raw = parts[1].strip()
                        # 只保留 "major.minor"（丢弃 patch 若有）
                        ver_parts = raw.split(".")
                        if len(ver_parts) >= 2:
                            cuda_version = f"{ver_parts[0]}.{ver_parts[1]}"
                        elif ver_parts:
                            cuda_version = ver_parts[0]
                    break

        return gpu_name, cuda_version

    except (FileNotFoundError, subprocess.TimeoutExpired, OSError) as exc:
        logger.debug(
            "nvidia-smi 不可用（无 GPU 机器）",
            extra={"reason": str(exc)},
        )
        return None, None


def _derive_os_major(os_name: str, os_release: str) -> str:
    """从 os_name 和 os_release 派生 os_major 标识。

    用于 hard_reject 比对：只取大版本号。

    示例：
        _derive_os_major("Darwin", "25.2.0")  → "Darwin 25"
        _derive_os_major("Linux", "6.1.0-18-amd64")  → "Linux 6"

    边缘情况：release 无法 split 时取完整字符串（健壮性）。
    """
    try:
        major = os_release.split(".")[0]
    except (AttributeError, IndexError):
        major = os_release or "unknown"
    return f"{os_name} {major}"


# ---------------------------------------------------------------------------
# 公开 API
# ---------------------------------------------------------------------------

def collect_fingerprint() -> dict:
    """采集当前机器的 5 维指纹。

    返回：
        dict with keys:
        - gpu_name:       str | None  — GPU 型号（无 GPU → None）
        - cuda_version:   str | None  — "major.minor"（无 GPU → None）
        - python_version: str         — "x.y.z"（完整，含 patch）
        - os_name:        str         — platform.system()
        - os_release:     str         — platform.release()

    不抛异常：GPU 探测失败时降级为 None，其他字段均有值。
    """
    gpu_name, cuda_version = _query_nvidia_smi()

    python_version = (
        f"{sys.version_info.major}"
        f".{sys.version_info.minor}"
        f".{sys.version_info.micro}"
    )

    return {
        "gpu_name": gpu_name,
        "cuda_version": cuda_version,
        "python_version": python_version,
        "os_name": platform.system(),
        "os_release": platform.release(),
    }


def _fp_file_path(run_id: str) -> Path:
    """返回 runs/<run_id>/machine_fingerprint.json 路径（不创建）。"""
    return run_dir(run_id) / "machine_fingerprint.json"


def write_fingerprint(run_id: str, fp: dict) -> None:
    """原子写 runs/<run_id>/machine_fingerprint.json。

    原子性：先写 .tmp，再 os.rename 覆盖目标（POSIX 原子操作）。
    runs/<run_id>/ 目录必须存在（由调用方 ensure_run_tree 保证）。

    参数：
        run_id : run 标识符
        fp     : collect_fingerprint() 返回的 dict
    """
    target = _fp_file_path(run_id)
    target.parent.mkdir(parents=True, exist_ok=True)

    payload = json.dumps(fp, ensure_ascii=False, indent=2)

    # 先写 .tmp，同目录保证 rename 在同一文件系统（POSIX 原子）
    fd, tmp_path_str = tempfile.mkstemp(
        dir=target.parent,
        prefix=".machine_fp_",
        suffix=".tmp",
    )
    tmp_path = Path(tmp_path_str)
    try:
        import os
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(payload)
        tmp_path.rename(target)
        logger.info(
            "machine_fingerprint 写入成功",
            extra={"run_id": run_id, "path": str(target)},
        )
    except Exception:
        try:
            tmp_path.unlink(missing_ok=True)
        except OSError:
            pass
        raise


def read_fingerprint(run_id: str) -> dict | None:
    """读取 runs/<run_id>/machine_fingerprint.json。

    文件不存在时返回 None（向后兼容 v0.1 早期 run）。

    返回：
        dict  : 指纹数据
        None  : 文件不存在（旧 run，兼容处理）

    Raises：
        json.JSONDecodeError : 文件内容不是合法 JSON（文件损坏）
    """
    path = _fp_file_path(run_id)
    if not path.exists():
        logger.debug(
            "machine_fingerprint.json 不存在（旧 run 或首次 resume 前）",
            extra={"run_id": run_id, "path": str(path)},
        )
        return None

    raw = path.read_text(encoding="utf-8")
    return json.loads(raw)


def diff_fingerprint(
    saved: dict,
    current: dict,
) -> tuple[list[str], list[str]]:
    """比较保存的指纹与当前机器指纹的差异。

    按 C22 规则分类：
    - hard_mismatches : 不一致的 hard_reject 字段名列表（非空 → 不允许 resume）
    - warn_mismatches : 不一致的 warning 字段名列表（非空 → 打印 warning，允许 resume）

    注意 os_major 是 派生 字段（不存储在 dict 中），此处动态计算比较。
    cuda_version 比较时只取 "major.minor"（忽略 patch；None == None 算匹配）。

    参数：
        saved   : 历史保存的指纹（write_fingerprint 写入的 dict）
        current : 当前机器采集的指纹（collect_fingerprint 返回的 dict）

    返回：
        (hard_mismatches, warn_mismatches) — 均为 list[str]
    """
    hard: list[str] = []
    warn: list[str] = []

    # --- hard_reject: gpu_name ---
    if saved.get("gpu_name") != current.get("gpu_name"):
        hard.append("gpu_name")

    # --- hard_reject: cuda_version（主次版本比较，patch 忽略）---
    s_cuda = _normalize_cuda(saved.get("cuda_version"))
    c_cuda = _normalize_cuda(current.get("cuda_version"))
    if s_cuda != c_cuda:
        hard.append("cuda_version")

    # --- hard_reject: os_major（派生）---
    s_os_major = _derive_os_major(
        saved.get("os_name", ""),
        saved.get("os_release", ""),
    )
    c_os_major = _derive_os_major(
        current.get("os_name", ""),
        current.get("os_release", ""),
    )
    if s_os_major != c_os_major:
        hard.append("os_major")

    # --- warning: python_version ---
    if saved.get("python_version") != current.get("python_version"):
        warn.append("python_version")

    # --- warning: os_release（精确小版本）---
    # 注意：只有当 os_major 相同时，os_release 差异才是 warning；
    # 若 os_major 已经不同，os_release 已进了 hard（通过 os_major 判断），不重复 warn。
    if saved.get("os_release") != current.get("os_release") and "os_major" not in hard:
        warn.append("os_release")

    return hard, warn


def _normalize_cuda(version: str | None) -> str | None:
    """将 cuda_version 归一化为 "major.minor"。

    None → None（无 GPU 机器）。
    "12.4.0" → "12.4"（只保留主次版本）。
    "12.4" → "12.4"（已是主次版本，不变）。
    """
    if version is None:
        return None
    parts = str(version).split(".")
    if len(parts) >= 2:
        return f"{parts[0]}.{parts[1]}"
    return parts[0] if parts else None
