"""
tests/unit/test_env_snapshot.py — T023 env_snapshot 单元测试。

结论：验证 collect_env_snapshot() 返回 EnvSnapshot 实例，
      字段类型正确，GPU/CUDA 字段在无 nvidia-smi 时为 None 而非抛异常。
"""

from __future__ import annotations

import subprocess
from unittest.mock import MagicMock, patch

import pytest

from pars.ledger import EnvSnapshot


# ---------------------------------------------------------------------------
# T023-ENV-TC01: 返回 EnvSnapshot 实例
# ---------------------------------------------------------------------------

def test_collect_env_snapshot_returns_instance() -> None:
    """should return EnvSnapshot instance when collect_env_snapshot is called."""
    from pars.orch.env_snapshot import collect_env_snapshot

    snap = collect_env_snapshot()
    assert isinstance(snap, EnvSnapshot), f"应返回 EnvSnapshot 实例，实际：{type(snap)}"


# ---------------------------------------------------------------------------
# T023-ENV-TC02: python_version 非空字符串
# ---------------------------------------------------------------------------

def test_python_version_is_nonempty_string() -> None:
    """should return non-empty python_version string when collect_env_snapshot is called."""
    from pars.orch.env_snapshot import collect_env_snapshot

    snap = collect_env_snapshot()
    assert isinstance(snap.python_version, str), "python_version 应为字符串"
    assert len(snap.python_version) > 0, "python_version 不得为空"
    # 验证格式：x.y.z 或 x.y
    parts = snap.python_version.split(".")
    assert len(parts) >= 2, f"python_version 应含至少 major.minor，实际：{snap.python_version}"  # noqa: PLR2004


# ---------------------------------------------------------------------------
# T023-ENV-TC03: platform 非空字符串
# ---------------------------------------------------------------------------

def test_platform_is_nonempty_string() -> None:
    """should return non-empty platform string when collect_env_snapshot is called."""
    from pars.orch.env_snapshot import collect_env_snapshot

    snap = collect_env_snapshot()
    assert isinstance(snap.platform, str), "platform 应为字符串"
    assert len(snap.platform) > 0, "platform 不得为空"


# ---------------------------------------------------------------------------
# T023-ENV-TC04: 无 nvidia-smi 时 GPU 字段为 None 而非抛异常
# ---------------------------------------------------------------------------

def test_gpu_fields_none_when_no_nvidia_smi() -> None:
    """should return None for gpu/cuda fields when nvidia-smi is unavailable."""
    from pars.orch.env_snapshot import collect_env_snapshot

    # 模拟 nvidia-smi 不存在（FileNotFoundError）
    with patch("subprocess.run") as mock_run:
        mock_run.side_effect = FileNotFoundError("nvidia-smi: not found")
        snap = collect_env_snapshot()

    assert snap.gpu_name is None, f"无 nvidia-smi 时 gpu_name 应为 None，实际：{snap.gpu_name}"
    assert snap.cuda_version is None, f"无 nvidia-smi 时 cuda_version 应为 None，实际：{snap.cuda_version}"


# ---------------------------------------------------------------------------
# T023-ENV-TC05: nvidia-smi 返回非零时 GPU 字段为 None
# ---------------------------------------------------------------------------

def test_gpu_fields_none_when_nvidia_smi_fails() -> None:
    """should return None for gpu/cuda fields when nvidia-smi exits with nonzero."""
    from pars.orch.env_snapshot import collect_env_snapshot

    mock_result = MagicMock()
    mock_result.returncode = 1
    mock_result.stdout = ""

    with patch("subprocess.run", return_value=mock_result):
        snap = collect_env_snapshot()

    assert snap.gpu_name is None
    assert snap.cuda_version is None


# ---------------------------------------------------------------------------
# T023-ENV-TC06: nvidia-smi 成功时 GPU 字段非 None
# ---------------------------------------------------------------------------

def test_gpu_fields_populated_when_nvidia_smi_succeeds() -> None:
    """should populate gpu_name and cuda_version when nvidia-smi reports them."""
    from pars.orch.env_snapshot import collect_env_snapshot

    # 第一次调用：--query-gpu=name,driver_version → 返回 GPU 名称
    mock_query_result = MagicMock()
    mock_query_result.returncode = 0
    mock_query_result.stdout = "NVIDIA RTX 4090, 550.144.00\n"

    # 第二次调用：nvidia-smi（无参数）→ 返回含 "CUDA Version:" 的输出
    mock_smi_result = MagicMock()
    mock_smi_result.returncode = 0
    mock_smi_result.stdout = (
        "+------------------------------------------------------------------------------+\n"
        "| NVIDIA-SMI 550.144.00    Driver Version: 550.144.00    CUDA Version: 12.4    |\n"
        "+------------------------------------------------------------------------------+\n"
    )

    # pip freeze 调用
    mock_pip_result = MagicMock()
    mock_pip_result.returncode = 0
    mock_pip_result.stdout = "numpy==1.26.0\n"

    side_effects = [mock_query_result, mock_smi_result, mock_pip_result]

    with patch("subprocess.run", side_effect=side_effects):
        snap = collect_env_snapshot()

    assert snap.gpu_name == "NVIDIA RTX 4090", f"gpu_name 不符，实际：{snap.gpu_name!r}"
    assert snap.cuda_version == "12.4", f"cuda_version 不符，实际：{snap.cuda_version!r}"


# ---------------------------------------------------------------------------
# T023-ENV-TC07: pip_freeze_sha256 为 None 或 64-char hex 字符串
# ---------------------------------------------------------------------------

def test_pip_freeze_sha256_is_none_or_hex64() -> None:
    """should return None or 64-char hex string for pip_freeze_sha256."""
    from pars.orch.env_snapshot import collect_env_snapshot

    # 不 mock subprocess，让 pip freeze 真实运行（可能很慢但可靠）
    snap = collect_env_snapshot()

    if snap.pip_freeze_sha256 is not None:
        assert isinstance(snap.pip_freeze_sha256, str), "pip_freeze_sha256 应为字符串"
        assert len(snap.pip_freeze_sha256) == 64, (  # noqa: PLR2004
            f"SHA256 应为 64 位 hex，实际长度：{len(snap.pip_freeze_sha256)}"
        )
        assert all(c in "0123456789abcdef" for c in snap.pip_freeze_sha256), (
            f"SHA256 应仅含 hex 字符，实际：{snap.pip_freeze_sha256!r}"
        )


# ---------------------------------------------------------------------------
# T023-ENV-TC08: pip freeze 失败时 pip_freeze_sha256 为 None
# ---------------------------------------------------------------------------

def test_pip_freeze_sha256_none_when_pip_fails() -> None:
    """should return None for pip_freeze_sha256 when pip subprocess fails."""
    from pars.orch.env_snapshot import collect_env_snapshot

    def side_effect(args, **kwargs):  # noqa: ANN001
        # nvidia-smi → FileNotFoundError；pip → CalledProcessError
        if "nvidia-smi" in args[0]:
            raise FileNotFoundError("no nvidia-smi")
        raise subprocess.CalledProcessError(1, args)

    with patch("subprocess.run", side_effect=side_effect):
        snap = collect_env_snapshot()

    assert snap.pip_freeze_sha256 is None, (
        f"pip 失败时 pip_freeze_sha256 应为 None，实际：{snap.pip_freeze_sha256!r}"
    )


# ---------------------------------------------------------------------------
# T023-ENV-TC09: EnvSnapshot 可成功序列化为 dict（Pydantic 契约）
# ---------------------------------------------------------------------------

def test_env_snapshot_serializable() -> None:
    """should be serializable to dict without errors."""
    from pars.orch.env_snapshot import collect_env_snapshot

    with patch("subprocess.run") as mock_run:
        mock_run.side_effect = FileNotFoundError("no gpu")
        snap = collect_env_snapshot()

    d = snap.model_dump()
    assert "python_version" in d
    assert "platform" in d
    assert "gpu_name" in d
    assert "cuda_version" in d
    assert "pip_freeze_sha256" in d
