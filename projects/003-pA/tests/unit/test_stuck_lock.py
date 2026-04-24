"""
test_stuck_lock.py — stuck_lock 读写 + pars unlock 命令单测。

测试覆盖：
- write_stuck_lock 原子写（tempfile + rename）
- has_stuck_lock 存在性检查
- clear_stuck_lock 删除
- pars unlock CLI 命令（清除 stuck_lock 文件）
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from pars.stuck.stuck_lock import (
    StuckLockData,
    clear_stuck_lock,
    has_stuck_lock,
    read_stuck_lock,
    write_stuck_lock,
)


# ---------------------------------------------------------------------------
# write_stuck_lock + has_stuck_lock
# ---------------------------------------------------------------------------

class TestWriteAndHasStuckLock:
    """写入 stuck_lock + 检查是否存在。"""

    def test_should_create_lock_file_when_write_called(self, tmp_path, monkeypatch):
        """write_stuck_lock 创建 runs/<id>/stuck_lock 文件。"""
        monkeypatch.setenv("RECALLKIT_RUN_DIR", str(tmp_path))
        run_id = "test-run-01"
        (tmp_path / run_id).mkdir()

        write_stuck_lock(run_id=run_id, reason="circuit_breaker_tripped", restart_count=3)
        lock_file = tmp_path / run_id / "stuck_lock"
        assert lock_file.exists()

    def test_should_return_true_when_lock_file_exists(self, tmp_path, monkeypatch):
        """has_stuck_lock 在文件存在时返回 True。"""
        monkeypatch.setenv("RECALLKIT_RUN_DIR", str(tmp_path))
        run_id = "test-run-02"
        (tmp_path / run_id).mkdir()
        (tmp_path / run_id / "stuck_lock").write_text("{}")

        assert has_stuck_lock(run_id=run_id) is True

    def test_should_return_false_when_lock_file_absent(self, tmp_path, monkeypatch):
        """has_stuck_lock 在文件不存在时返回 False。"""
        monkeypatch.setenv("RECALLKIT_RUN_DIR", str(tmp_path))
        run_id = "test-run-03"
        (tmp_path / run_id).mkdir()

        assert has_stuck_lock(run_id=run_id) is False

    def test_should_write_valid_json_when_lock_created(self, tmp_path, monkeypatch):
        """stuck_lock 文件内容是合法 JSON，含 reason + restart_count + created_at。"""
        monkeypatch.setenv("RECALLKIT_RUN_DIR", str(tmp_path))
        run_id = "test-run-04"
        (tmp_path / run_id).mkdir()

        write_stuck_lock(run_id=run_id, reason="circuit_breaker_tripped", restart_count=3)
        lock_file = tmp_path / run_id / "stuck_lock"
        data = json.loads(lock_file.read_text())
        assert data["reason"] == "circuit_breaker_tripped"
        assert data["restart_count"] == 3
        assert "created_at" in data

    def test_should_be_atomic_when_writing(self, tmp_path, monkeypatch):
        """写入应使用 tempfile + rename 保证原子性（文件最终路径正确）。"""
        monkeypatch.setenv("RECALLKIT_RUN_DIR", str(tmp_path))
        run_id = "test-run-05"
        (tmp_path / run_id).mkdir()

        write_stuck_lock(run_id=run_id, reason="test", restart_count=1)
        # 目标文件存在，无 .tmp 残留
        assert (tmp_path / run_id / "stuck_lock").exists()
        tmp_files = list((tmp_path / run_id).glob("*.tmp"))
        assert len(tmp_files) == 0


# ---------------------------------------------------------------------------
# read_stuck_lock
# ---------------------------------------------------------------------------

class TestReadStuckLock:
    """read_stuck_lock：反序列化 StuckLockData。"""

    def test_should_return_lock_data_when_file_exists(self, tmp_path, monkeypatch):
        """read_stuck_lock 返回 StuckLockData 对象。"""
        monkeypatch.setenv("RECALLKIT_RUN_DIR", str(tmp_path))
        run_id = "test-run-06"
        (tmp_path / run_id).mkdir()

        write_stuck_lock(run_id=run_id, reason="circuit_breaker_tripped", restart_count=3)
        lock_data = read_stuck_lock(run_id=run_id)
        assert isinstance(lock_data, StuckLockData)
        assert lock_data.reason == "circuit_breaker_tripped"
        assert lock_data.restart_count == 3

    def test_should_raise_file_not_found_when_no_lock(self, tmp_path, monkeypatch):
        """lock 文件不存在时，read_stuck_lock 抛 FileNotFoundError。"""
        monkeypatch.setenv("RECALLKIT_RUN_DIR", str(tmp_path))
        run_id = "test-run-07"
        (tmp_path / run_id).mkdir()

        with pytest.raises(FileNotFoundError):
            read_stuck_lock(run_id=run_id)


# ---------------------------------------------------------------------------
# clear_stuck_lock
# ---------------------------------------------------------------------------

class TestClearStuckLock:
    """clear_stuck_lock：删除 stuck_lock 文件。"""

    def test_should_remove_lock_file_when_clear_called(self, tmp_path, monkeypatch):
        """clear_stuck_lock 删除文件后 has_stuck_lock 返回 False。"""
        monkeypatch.setenv("RECALLKIT_RUN_DIR", str(tmp_path))
        run_id = "test-run-08"
        (tmp_path / run_id).mkdir()

        write_stuck_lock(run_id=run_id, reason="test", restart_count=1)
        assert has_stuck_lock(run_id=run_id) is True

        clear_stuck_lock(run_id=run_id)
        assert has_stuck_lock(run_id=run_id) is False

    def test_should_be_idempotent_when_clear_called_on_absent_lock(self, tmp_path, monkeypatch):
        """文件不存在时，clear_stuck_lock 不抛异常（幂等）。"""
        monkeypatch.setenv("RECALLKIT_RUN_DIR", str(tmp_path))
        run_id = "test-run-09"
        (tmp_path / run_id).mkdir()

        # 不应抛异常
        clear_stuck_lock(run_id=run_id)


# ---------------------------------------------------------------------------
# pars unlock CLI 命令
# ---------------------------------------------------------------------------

class TestParsUnlockCommand:
    """pars unlock <run-id> CLI 命令：清除 stuck_lock + 更新 state.json。"""

    def test_should_clear_lock_and_exit_0_when_lock_exists(self, tmp_path, monkeypatch):
        """lock 文件存在时，pars unlock 清除并返回 0。"""
        from click.testing import CliRunner
        from pars.cli.main import cli
        from pars.ledger.state import RunPhase, RunState, write_state
        from datetime import datetime, timezone

        monkeypatch.setenv("RECALLKIT_RUN_DIR", str(tmp_path))
        run_id = "test-unlock-01"
        (tmp_path / run_id).mkdir()

        # 创建 state.json
        state = RunState(
            run_id=run_id,
            phase=RunPhase.LORA_TRAIN,
            needs_human_review=True,
            stuck_restart_count=3,
            last_update=datetime.now(timezone.utc),
        )
        write_state(state, run_id)

        # 创建 stuck_lock 文件
        write_stuck_lock(run_id=run_id, reason="test", restart_count=3)
        assert has_stuck_lock(run_id=run_id) is True

        runner = CliRunner()
        result = runner.invoke(cli, ["unlock", "--run-id", run_id])
        assert result.exit_code == 0
        assert not has_stuck_lock(run_id=run_id)

    def test_should_exit_nonzero_when_no_lock_file_exists(self, tmp_path, monkeypatch):
        """lock 文件不存在时，pars unlock 报告并返回非零（无 lock 可清）。"""
        from click.testing import CliRunner
        from pars.cli.main import cli
        from pars.ledger.state import RunPhase, RunState, write_state
        from datetime import datetime, timezone

        monkeypatch.setenv("RECALLKIT_RUN_DIR", str(tmp_path))
        run_id = "test-unlock-02"
        (tmp_path / run_id).mkdir()

        state = RunState(
            run_id=run_id,
            phase=RunPhase.LORA_TRAIN,
            last_update=datetime.now(timezone.utc),
        )
        write_state(state, run_id)

        runner = CliRunner()
        result = runner.invoke(cli, ["unlock", "--run-id", run_id])
        assert result.exit_code != 0
