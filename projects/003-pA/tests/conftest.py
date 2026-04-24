"""
tests.conftest — 共享 pytest fixture。

结论：提供全局 fixture 给所有测试子套件使用。
      具体业务 fixture（训练相关、eval 相关）由各 task 的 test 文件自行定义。

Fixture 清单（T003 提供的基础层）：
- tmp_runs_dir     : 临时 runs/ 目录结构（unit/integration 测试隔离）
- mock_anthropic_key : 注入假的 ANTHROPIC_API_KEY env var（避免真实 API 调用）
- fake_gpu_snapshot  : 模拟 nvidia-smi 输出的 dict（T017 GPU 监控测试用）
"""

from __future__ import annotations

from collections.abc import Generator
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# 文件系统相关 fixture
# ---------------------------------------------------------------------------


@pytest.fixture()
def tmp_runs_dir(tmp_path: Path) -> Path:
    """返回临时 runs/ 目录（已创建，测试结束后自动清理）。

    用途：隔离文件系统副作用，避免测试污染真实 runs/ 目录。
    与 RECALLKIT_RUN_DIR env var 配合使用：
        monkeypatch.setenv("RECALLKIT_RUN_DIR", str(tmp_runs_dir))

    返回：tmp_path / "runs"（Path 对象，已 mkdir）
    """
    # 创建 runs/ 子目录结构
    runs_dir = tmp_path / "runs"
    runs_dir.mkdir(parents=True, exist_ok=True)

    # 同时创建 checkpoints/ 便于测试 ensure_run_tree
    (tmp_path / "checkpoints").mkdir(parents=True, exist_ok=True)

    return runs_dir


# ---------------------------------------------------------------------------
# API key 相关 fixture
# ---------------------------------------------------------------------------


@pytest.fixture()
def mock_anthropic_key(monkeypatch: pytest.MonkeyPatch) -> str:
    """注入假的 ANTHROPIC_API_KEY，防止测试意外调用真实 Anthropic API。

    用途：所有涉及 LiteLLM / claude 调用的 mock 测试均应使用此 fixture，
          确保即使 mock 失效也不会泄漏真实 API key 或产生费用。

    返回：注入的假 key 字符串（供测试断言用）
    """
    # 固定格式 sk-ant-test-... 便于识别
    fake_key = "sk-ant-test-00000000000000000000000000000000"
    monkeypatch.setenv("ANTHROPIC_API_KEY", fake_key)
    return fake_key


# ---------------------------------------------------------------------------
# GPU snapshot fixture（T017 GPU 监控模块用）
# ---------------------------------------------------------------------------


@pytest.fixture()
def fake_gpu_snapshot() -> dict[str, object]:
    """返回模拟的 nvidia-smi 输出 dict，供 T017 GPU 监控测试使用。

    用途：在无 GPU 的 macOS 开发机和 CI 环境中测试 GPU 监控逻辑，
          避免实际依赖 nvidia-smi 可执行文件。

    数据结构模拟单张 NVIDIA RTX 4090（24 GB VRAM）：
    {
        "index": 0,
        "name": "NVIDIA GeForce RTX 4090",
        "memory_total_mb": 24576,
        "memory_used_mb": 8192,
        "memory_free_mb": 16384,
        "utilization_gpu_pct": 45,
        "utilization_mem_pct": 33,
        "temperature_c": 62,
        "power_draw_w": 280.5,
        "power_limit_w": 450.0,
    }

    注意：字段名与 T017 GPU 监控模块约定的输出 schema 对齐，
          T017 实现时应确保与此 fixture 一致。
    """
    return {
        "index": 0,
        "name": "NVIDIA GeForce RTX 4090",
        "memory_total_mb": 24576,
        "memory_used_mb": 8192,
        "memory_free_mb": 16384,
        "utilization_gpu_pct": 45,
        "utilization_mem_pct": 33,
        "temperature_c": 62,
        "power_draw_w": 280.5,
        "power_limit_w": 450.0,
    }


# ---------------------------------------------------------------------------
# 环境隔离辅助 fixture（全局 autouse，防 env var 泄漏）
# ---------------------------------------------------------------------------


@pytest.fixture(autouse=True)
def _isolate_recallkit_env(monkeypatch: pytest.MonkeyPatch) -> Generator[None, None, None]:
    """自动 fixture：确保每个测试拿到干净的 RECALLKIT_* env var 环境。

    autouse=True → 无需在每个测试文件里手写 clean_env fixture。
    test_paths.py 里有本地的 clean_env fixture，两者互补（本地优先）。

    清理范围：RECALLKIT_RUN_DIR / RECALLKIT_CKPT_DIR / PARS_LOG_LEVEL
    （不动 ANTHROPIC_API_KEY — 由 mock_anthropic_key fixture 按需注入）
    """
    for key in ("RECALLKIT_RUN_DIR", "RECALLKIT_CKPT_DIR", "PARS_LOG_LEVEL"):
        monkeypatch.delenv(key, raising=False)
    yield
