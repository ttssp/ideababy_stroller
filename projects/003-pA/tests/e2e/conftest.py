"""
tests/e2e/conftest.py — E2E 测试套共享 fixture（T026）。

结论：提供 tmp_runs_dir / tiny_run_config / has_gpu 三个核心 fixture，
      供 test_o1..test_o7 共用。

环境变量说明：
  - RECALLKIT_RUN_DIR : run 数据目录根，由 pars.paths.runs_root() 读取
  - 每个测试通过 monkeypatch 设置，避免污染真实 runs/ 目录
"""

from __future__ import annotations

import shutil
from pathlib import Path
from typing import Generator

import pytest
import yaml

from pars.ledger.config_schema import RunConfig


# ---------------------------------------------------------------------------
# fixture: tmp_runs_dir
# ---------------------------------------------------------------------------


@pytest.fixture()
def tmp_runs_dir(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> Generator[Path, None, None]:
    """临时 runs 根目录，自动通过 RECALLKIT_RUN_DIR 注入 pars.paths。

    结论：每个测试获得独立隔离的 runs 目录，测试结束后自动清理。
    """
    runs_root = tmp_path / "runs"
    runs_root.mkdir(parents=True, exist_ok=True)
    monkeypatch.setenv("RECALLKIT_RUN_DIR", str(runs_root))
    yield runs_root


# ---------------------------------------------------------------------------
# fixture: tiny_run_config
# ---------------------------------------------------------------------------


@pytest.fixture()
def tiny_run_config() -> RunConfig:
    """从 fixtures/tiny_run_config.yaml 加载并验证 RunConfig。

    结论：TinyLlama + alpaca[:20] 最小配置，GPU 真实 run 可在 20min 内完成。
    验证：Pydantic v2 extra="forbid" 确保字段合规。
    """
    fixture_path = Path(__file__).parent / "fixtures" / "tiny_run_config.yaml"
    raw: dict = yaml.safe_load(fixture_path.read_text(encoding="utf-8"))
    # Pydantic v2 验证；schema 错误直接在 fixture 加载阶段报错，方便定位
    return RunConfig.model_validate(raw)


# ---------------------------------------------------------------------------
# fixture: has_gpu
# ---------------------------------------------------------------------------


@pytest.fixture()
def has_gpu() -> bool:
    """检测当前机器是否有 NVIDIA GPU（通过 nvidia-smi 探测）。

    结论：返回 bool，供测试按需 skip：
        if not has_gpu:
            pytest.skip("需要 GPU")
    不自动 skip，保持 fixture 的通用性。
    """
    return shutil.which("nvidia-smi") is not None
