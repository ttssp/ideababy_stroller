"""
pars.orch.env_snapshot — 启动时环境快照采集（T023）。

结论：collect_env_snapshot() 采集 python version / platform / CUDA / GPU / pip freeze SHA256，
      返回 EnvSnapshot Pydantic 模型。
      subprocess 失败（无 nvidia-smi 或 pip 不可用）时优雅降级为 None，不抛异常。

字段映射：
  python_version  → platform.python_version()
  platform        → platform.system().lower() + "-" + platform.machine().lower()
  gpu_name        → nvidia-smi --query-gpu=name --format=csv,noheader 第一行
  cuda_version    → nvidia-smi --query-gpu=driver_version,... + 解析 CUDA 版本
                    实际使用 nvidia-smi --version 输出中的 CUDA 行
  pip_freeze_sha256 → pip freeze | sha256sum（hexdigest）
"""

from __future__ import annotations

import hashlib
import platform
import subprocess
import sys

from pars.ledger import EnvSnapshot
from pars.logging import get_logger

logger = get_logger(__name__)


def collect_env_snapshot() -> EnvSnapshot:
    """采集当前运行环境快照，返回 EnvSnapshot 实例。

    所有 subprocess 步骤失败时优雅降级（返回 None），不传播异常。

    返回：
        EnvSnapshot 实例，各字段见 pars.ledger.config_schema.EnvSnapshot
    """
    python_ver = platform.python_version()
    plat_str = f"{platform.system().lower()}-{platform.machine().lower()}"
    gpu_name, cuda_version = _collect_gpu_info()
    pip_sha = _collect_pip_freeze_sha256()

    logger.debug(
        "collect_env_snapshot 完成",
        extra={
            "python_version": python_ver,
            "platform": plat_str,
            "gpu_name": gpu_name,
            "cuda_version": cuda_version,
            "pip_sha256_present": pip_sha is not None,
        },
    )

    return EnvSnapshot(
        python_version=python_ver,
        platform=plat_str,
        gpu_name=gpu_name,
        cuda_version=cuda_version,
        pip_freeze_sha256=pip_sha,
    )


# ---------------------------------------------------------------------------
# 内部辅助：GPU / CUDA 采集
# ---------------------------------------------------------------------------

def _collect_gpu_info() -> tuple[str | None, str | None]:
    """通过 nvidia-smi 采集 GPU 名称和 CUDA 版本。

    使用两次查询：
      1. nvidia-smi --query-gpu=name --format=csv,noheader → GPU 名称
      2. nvidia-smi --query-gpu=driver_version --format=csv,noheader → 驱动版本（CUDA 版本关联）
         注：更可靠的 CUDA 版本来自 nvidia-smi 的 "CUDA Version:" 行

    失败时（FileNotFoundError / 非零退出码）返回 (None, None)。

    返回：
        (gpu_name, cuda_version) — 失败时均为 None
    """
    try:
        result = subprocess.run(  # noqa: S603
            ["nvidia-smi", "--query-gpu=name,driver_version", "--format=csv,noheader"],
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (FileNotFoundError, OSError):
        logger.debug("_collect_gpu_info: nvidia-smi 不存在，跳过 GPU 采集")
        return None, None
    except subprocess.TimeoutExpired:
        logger.warning("_collect_gpu_info: nvidia-smi 超时")
        return None, None

    if result.returncode != 0:
        logger.debug(
            "_collect_gpu_info: nvidia-smi 返回非零",
            extra={"returncode": result.returncode},
        )
        return None, None

    # 解析输出：期望格式 "GPU Name, Driver Version\n"
    # 也兼容只有 name 一列的情况（测试 mock 可能只返回一行）
    raw = result.stdout.strip()
    if not raw:
        return None, None

    # 尝试按逗号分割（CSV 格式）
    lines = raw.splitlines()
    first_line = lines[0].strip() if lines else ""
    parts = [p.strip() for p in first_line.split(",")]

    gpu_name = parts[0] if parts and parts[0] else None

    # 第二列是驱动版本（如 "550.144.00"），不是 CUDA 版本
    # 尝试从第二列获取 CUDA 版本（部分 nvidia-smi 版本输出格式不同）
    # 回退策略：从输出中查找 CUDA 版本行
    cuda_version = _extract_cuda_version_from_smi()

    return gpu_name, cuda_version


def _extract_cuda_version_from_smi() -> str | None:
    """从 nvidia-smi 的标准输出（不带 --query-gpu）中提取 'CUDA Version: X.Y'。

    返回：
        CUDA 版本字符串（如 "12.4"）或 None
    """
    try:
        result = subprocess.run(  # noqa: S603
            ["nvidia-smi"],
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (FileNotFoundError, OSError, subprocess.TimeoutExpired):
        return None

    if result.returncode != 0:
        return None

    # 在输出中查找 "CUDA Version: X.Y" 模式
    for line in result.stdout.splitlines():
        line_lower = line.lower()
        if "cuda version:" in line_lower:
            # 提取版本号
            idx = line_lower.index("cuda version:") + len("cuda version:")
            version_part = line[idx:].strip()
            # 取第一个词（可能含空格前）
            version_token = version_part.split()[0] if version_part.split() else None
            return version_token if version_token else None

    return None


# ---------------------------------------------------------------------------
# 内部辅助：pip freeze SHA256
# ---------------------------------------------------------------------------

def _collect_pip_freeze_sha256() -> str | None:
    """执行 pip freeze 并返回输出的 SHA256 hex 摘要。

    失败时（FileNotFoundError / 非零退出码 / timeout）返回 None。

    返回：
        64-char hex 字符串（SHA256）或 None
    """
    try:
        result = subprocess.run(  # noqa: S603
            [sys.executable, "-m", "pip", "freeze"],
            capture_output=True,
            text=True,
            timeout=60,
        )
    except (FileNotFoundError, OSError) as e:
        logger.debug("_collect_pip_freeze_sha256: pip 不可用", extra={"error": str(e)})
        return None
    except subprocess.TimeoutExpired:
        logger.warning("_collect_pip_freeze_sha256: pip freeze 超时")
        return None
    except subprocess.CalledProcessError as e:
        logger.debug("_collect_pip_freeze_sha256: pip freeze 失败", extra={"error": str(e)})
        return None

    if result.returncode != 0:
        logger.debug(
            "_collect_pip_freeze_sha256: pip freeze 返回非零",
            extra={"returncode": result.returncode},
        )
        return None

    freeze_output = result.stdout
    digest = hashlib.sha256(freeze_output.encode("utf-8")).hexdigest()

    logger.debug(
        "_collect_pip_freeze_sha256: 完成",
        extra={"sha256_prefix": digest[:8]},
    )
    return digest
