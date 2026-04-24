"""
tests.unit.test_machine_fingerprint — 机器指纹采集与比对测试（T019 · C22）。

结论：先写测试（TDD Red → Green），覆盖:
1. collect_fingerprint() 返回 5 维 dict（gpu_name, cuda_version,
   python_version, os_name, os_release）
2. 派生字段 os_major 在 diff 时正确计算
3. hard_reject: gpu_name 不同 → hard_mismatch
4. hard_reject: cuda_version 不同（主次版本）→ hard_mismatch
5. hard_reject: os_major 不同 → hard_mismatch
6. warning: python_version patch 不同 → warn_mismatch, 非 hard
7. warning: os_release patch 不同（但 os_major 不变）→ warn_mismatch
8. all match → ([], []) 空 hard 空 warn
9. 无 GPU（cuda_version=None, gpu_name=None）→ 能采集, os_major 对 None 值友好
10. write_fingerprint 原子写 + read_fingerprint 读回 → 数据完整
11. read_fingerprint 文件不存在 → 返回 None（向后兼容）
12. diff_fingerprint 仅 gpu 缺失（一方 None 另一方有值）→ 算 hard_mismatch

"""
from __future__ import annotations

import json
import platform
import sys
from pathlib import Path
from unittest.mock import patch

import pytest


# ---------------------------------------------------------------------------
# 延迟 import：让测试文件在实现文件不存在时能被 collect（会在调用时才报
# ImportError，而非 collection 阶段崩溃）
# ---------------------------------------------------------------------------

def _import_mf():
    """延迟 import machine_fingerprint 模块。"""
    from pars.orch import machine_fingerprint as mf  # noqa: PLC0415
    return mf


# ---------------------------------------------------------------------------
# 辅助：构造典型指纹 dict
# ---------------------------------------------------------------------------

def _fp(
    gpu_name: str | None = "NVIDIA GeForce RTX 4090",
    cuda_version: str | None = "12.4",
    python_version: str = "3.12.4",
    os_name: str = "Darwin",
    os_release: str = "25.2.0",
) -> dict:
    return {
        "gpu_name": gpu_name,
        "cuda_version": cuda_version,
        "python_version": python_version,
        "os_name": os_name,
        "os_release": os_release,
    }


# ===========================================================================
# 测试 1：collect_fingerprint() 返回 dict，包含 5 个必填字段
# ===========================================================================

def test_collect_fingerprint_returns_five_fields():
    """should return dict with 5 keys when called on any machine."""
    mf = _import_mf()
    fp = mf.collect_fingerprint()
    assert isinstance(fp, dict)
    required_keys = {"gpu_name", "cuda_version", "python_version", "os_name", "os_release"}
    assert required_keys == set(fp.keys()), f"缺少字段: {required_keys - set(fp.keys())}"


def test_collect_fingerprint_python_version_matches_runtime():
    """should match sys.version_info when collecting python_version."""
    mf = _import_mf()
    fp = mf.collect_fingerprint()
    expected = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    assert fp["python_version"] == expected


def test_collect_fingerprint_os_name_matches_platform():
    """should match platform.system() for os_name."""
    mf = _import_mf()
    fp = mf.collect_fingerprint()
    assert fp["os_name"] == platform.system()


def test_collect_fingerprint_os_release_matches_platform():
    """should match platform.release() for os_release."""
    mf = _import_mf()
    fp = mf.collect_fingerprint()
    assert fp["os_release"] == platform.release()


def test_collect_fingerprint_no_gpu_returns_none_fields():
    """should return gpu_name=None and cuda_version=None when nvidia-smi unavailable."""
    mf = _import_mf()

    # mock nvidia-smi 不可用
    with patch("subprocess.run") as mock_run:
        mock_run.side_effect = FileNotFoundError("nvidia-smi not found")
        fp = mf.collect_fingerprint()

    assert fp["gpu_name"] is None, "无 GPU 时 gpu_name 应为 None"
    assert fp["cuda_version"] is None, "无 GPU 时 cuda_version 应为 None"
    # 其他字段仍有值
    assert fp["python_version"] is not None
    assert fp["os_name"] is not None
    assert fp["os_release"] is not None


# ===========================================================================
# 测试 2：diff_fingerprint — hard_reject: gpu_name 不同
# ===========================================================================

def test_diff_fingerprint_hard_mismatch_when_gpu_name_differs():
    """should return gpu_name in hard_mismatches when GPU models differ."""
    mf = _import_mf()
    saved = _fp(gpu_name="NVIDIA GeForce RTX 4090")
    current = _fp(gpu_name="NVIDIA H200 141GB")
    hard, warn = mf.diff_fingerprint(saved, current)
    assert "gpu_name" in hard, f"gpu_name 不同应进 hard_mismatches，实际: {hard}"
    assert "gpu_name" not in warn


# ===========================================================================
# 测试 3：diff_fingerprint — hard_reject: cuda_version 主次版本不同
# ===========================================================================

def test_diff_fingerprint_hard_mismatch_when_cuda_major_minor_differs():
    """should return cuda_version in hard_mismatches when major.minor CUDA version differs."""
    mf = _import_mf()
    saved = _fp(cuda_version="12.4")
    current = _fp(cuda_version="12.6")
    hard, warn = mf.diff_fingerprint(saved, current)
    assert "cuda_version" in hard, f"cuda_version 主次版本不同应进 hard_mismatches，实际: {hard}"


def test_diff_fingerprint_hard_mismatch_when_cuda_major_differs():
    """should return cuda_version in hard_mismatches when CUDA major version differs."""
    mf = _import_mf()
    saved = _fp(cuda_version="11.8")
    current = _fp(cuda_version="12.4")
    hard, warn = mf.diff_fingerprint(saved, current)
    assert "cuda_version" in hard


# ===========================================================================
# 测试 4：diff_fingerprint — hard_reject: os_major 不同
# ===========================================================================

def test_diff_fingerprint_hard_mismatch_when_os_major_differs():
    """should return os_major in hard_mismatches when OS major version differs."""
    mf = _import_mf()
    saved = _fp(os_name="Darwin", os_release="24.0.0")   # Darwin 24 = macOS Sequoia
    current = _fp(os_name="Darwin", os_release="25.2.0")  # Darwin 25 = macOS Tahoe
    hard, warn = mf.diff_fingerprint(saved, current)
    assert "os_major" in hard, f"os_major 不同应进 hard_mismatches，实际: {hard}"


def test_diff_fingerprint_hard_mismatch_when_os_name_differs():
    """should return os_major in hard_mismatches when OS platform differs (Linux vs Darwin)."""
    mf = _import_mf()
    saved = _fp(os_name="Linux", os_release="6.1.0")
    current = _fp(os_name="Darwin", os_release="25.2.0")
    hard, warn = mf.diff_fingerprint(saved, current)
    # 不同 os_name 必然 os_major 不同
    assert "os_major" in hard


# ===========================================================================
# 测试 5：diff_fingerprint — warning: python_version patch 不同，不 hard_reject
# ===========================================================================

def test_diff_fingerprint_warn_when_python_patch_differs():
    """should return python_version in warn_mismatches (not hard) when patch version changes."""
    mf = _import_mf()
    saved = _fp(python_version="3.12.4")
    current = _fp(python_version="3.12.5")
    hard, warn = mf.diff_fingerprint(saved, current)
    assert "python_version" not in hard, "python_version patch 差异不应 hard_reject"
    assert "python_version" in warn, f"python_version patch 差异应 warn，实际: {warn}"


# ===========================================================================
# 测试 6：diff_fingerprint — warning: os_release patch 不同，os_major 不变
# ===========================================================================

def test_diff_fingerprint_warn_when_os_release_patch_differs_but_major_same():
    """should warn but not hard-reject when os_release patch changes but os_major unchanged."""
    mf = _import_mf()
    saved = _fp(os_name="Darwin", os_release="25.2.0")
    current = _fp(os_name="Darwin", os_release="25.2.1")
    hard, warn = mf.diff_fingerprint(saved, current)
    assert "os_major" not in hard, "os_major 未变，不应 hard_reject"
    assert "os_release" not in hard, "os_release patch 差异不应 hard_reject"
    assert "os_release" in warn, f"os_release patch 差异应 warn，实际: {warn}"


# ===========================================================================
# 测试 7：diff_fingerprint — all match → ([], [])
# ===========================================================================

def test_diff_fingerprint_ok_when_all_fields_match():
    """should return empty lists when all fingerprint fields are identical."""
    mf = _import_mf()
    fp = _fp()
    hard, warn = mf.diff_fingerprint(fp, fp)
    assert hard == [], f"全匹配时 hard_mismatches 应为空，实际: {hard}"
    assert warn == [], f"全匹配时 warn_mismatches 应为空，实际: {warn}"


# ===========================================================================
# 测试 8：无 GPU 机器（gpu_name=None, cuda_version=None）能存储/比较
# ===========================================================================

def test_diff_fingerprint_no_gpu_both_none_is_ok():
    """should not mismatch when both saved and current have no GPU (None == None)."""
    mf = _import_mf()
    no_gpu = _fp(gpu_name=None, cuda_version=None)
    hard, warn = mf.diff_fingerprint(no_gpu, no_gpu)
    assert hard == []
    assert warn == []


def test_diff_fingerprint_hard_mismatch_when_gpu_transitions_none_to_real():
    """should hard_mismatch when one side has GPU and other doesn't (None vs real)."""
    mf = _import_mf()
    no_gpu = _fp(gpu_name=None, cuda_version=None)
    with_gpu = _fp(gpu_name="NVIDIA GeForce RTX 4090", cuda_version="12.4")
    hard, warn = mf.diff_fingerprint(no_gpu, with_gpu)
    # gpu_name 变了 (None → str) 算 hard_mismatch
    assert "gpu_name" in hard


# ===========================================================================
# 测试 9：write_fingerprint + read_fingerprint 往返
# ===========================================================================

def test_write_and_read_fingerprint_round_trip(tmp_path, monkeypatch):
    """should persist fingerprint to machine_fingerprint.json and read it back intact."""
    mf = _import_mf()
    monkeypatch.setenv("RECALLKIT_RUN_DIR", str(tmp_path))

    run_id = "test-run-001"
    fp = _fp()

    # 先创建 run 目录
    (tmp_path / run_id).mkdir(parents=True, exist_ok=True)

    mf.write_fingerprint(run_id, fp)

    read_back = mf.read_fingerprint(run_id)
    assert read_back is not None
    assert read_back == fp


def test_read_fingerprint_returns_none_when_file_missing(tmp_path, monkeypatch):
    """should return None when machine_fingerprint.json does not exist (backward compat)."""
    mf = _import_mf()
    monkeypatch.setenv("RECALLKIT_RUN_DIR", str(tmp_path))

    run_id = "nonexistent-run"
    result = mf.read_fingerprint(run_id)
    assert result is None, "文件不存在时应返回 None（向后兼容）"


def test_write_fingerprint_is_atomic(tmp_path, monkeypatch):
    """should write fingerprint atomically (file contains valid JSON after write)."""
    mf = _import_mf()
    monkeypatch.setenv("RECALLKIT_RUN_DIR", str(tmp_path))

    run_id = "atomic-test-run"
    (tmp_path / run_id).mkdir(parents=True, exist_ok=True)

    fp = _fp()
    mf.write_fingerprint(run_id, fp)

    # 验证文件内容是合法 JSON
    fp_file = tmp_path / run_id / "machine_fingerprint.json"
    assert fp_file.exists()
    content = json.loads(fp_file.read_text())
    assert content == fp


# ===========================================================================
# 测试 10：HARD_REJECT_FIELDS 与 WARNING_FIELDS 常量存在
# ===========================================================================

def test_hard_reject_and_warning_fields_constants_exist():
    """should expose HARD_REJECT_FIELDS and WARNING_FIELDS as module-level constants."""
    mf = _import_mf()
    assert hasattr(mf, "HARD_REJECT_FIELDS")
    assert hasattr(mf, "WARNING_FIELDS")
    # 验证字段分类正确
    assert "gpu_name" in mf.HARD_REJECT_FIELDS
    assert "cuda_version" in mf.HARD_REJECT_FIELDS
    assert "python_version" in mf.WARNING_FIELDS
    assert "os_release" in mf.WARNING_FIELDS
    # os_major 是派生字段，在 HARD_REJECT 语义上体现（不一定是显式常量key）
    # 但 gpu_name/cuda_version 不能出现在 WARNING_FIELDS
    assert "gpu_name" not in mf.WARNING_FIELDS
    assert "cuda_version" not in mf.WARNING_FIELDS
