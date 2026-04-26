"""
共享 pytest fixture — T001 占位
结论: 提供 tmpdir 数据库路径 + mock anthropic client 两个基础 fixture
细节: 后续 task (T003/T005) 会扩充真实 Repository / LLMClient fixture
"""

from __future__ import annotations

import os
from collections.abc import Generator
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest


@pytest.fixture
def tmp_db_path(tmp_path: Path) -> Path:
    """返回临时 SQLite db 路径，测试结束后自动清理。"""
    return tmp_path / "test_db.sqlite"


@pytest.fixture
def mock_anthropic_client() -> Generator[MagicMock, None, None]:
    """mock anthropic.Anthropic client — 阻止真实 API 调用。"""
    with patch("anthropic.Anthropic") as mock_cls:
        mock_instance = MagicMock()
        mock_cls.return_value = mock_instance
        yield mock_instance


@pytest.fixture(autouse=True)
def _clear_env_overrides() -> Generator[None, None, None]:
    """确保每个测试从干净的环境变量状态开始。"""
    original: dict[str, str] = {}
    keys_to_remove: list[str] = []
    yield
    # 恢复（若有任何 test 修改了 env）
    for k, v in original.items():
        os.environ[k] = v
    for k in keys_to_remove:
        os.environ.pop(k, None)
