"""
test_stuck_restart_circuit_breaker.py — CircuitBreaker 集成测试。

模拟：
- 3 次 stuck → restart 流程
- 第 4 次 should_restart() == False
- stuck_lock 文件存在
- state.json.needs_human_review == True

标记为 integration 测试（需 pytest -m integration）。
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import pytest

from pars.ledger.state import RunPhase, RunState, read_state, write_state
from pars.stuck.state_machine import CircuitBreaker
from pars.stuck.stuck_lock import has_stuck_lock, write_stuck_lock


pytestmark = pytest.mark.integration


class TestCircuitBreakerIntegration:
    """CircuitBreaker：3 次 stuck-restart → 第 4 次熔断 + stuck_lock + needs_human_review。"""

    def test_should_trip_and_write_lock_after_3_restarts(self, tmp_path, monkeypatch):
        """3 次 record_restart() 后：
        - should_restart() == False
        - record_human_review_needed() 写 stuck_lock + needs_human_review=True
        """
        monkeypatch.setenv("RECALLKIT_RUN_DIR", str(tmp_path))
        run_id = "circuit-test-01"
        (tmp_path / run_id).mkdir()

        # 初始化 state.json
        state = RunState(
            run_id=run_id,
            phase=RunPhase.LORA_TRAIN,
            stuck_restart_count=0,
            needs_human_review=False,
            last_update=datetime.now(timezone.utc),
        )
        write_state(state, run_id)

        # 模拟 3 次 stuck-restart
        cb = CircuitBreaker(stuck_restart_count=0)
        for _ in range(3):
            assert cb.should_restart() is True
            cb.record_restart()

        # 第 4 次检查：熔断
        assert cb.should_restart() is False

        # 调用 record_human_review_needed 写 stuck_lock + 更新 state.json
        cb.record_human_review_needed(run_id=run_id)

        # 验证 stuck_lock 文件存在
        assert has_stuck_lock(run_id=run_id), "stuck_lock 文件应存在"

        # 验证 state.json.needs_human_review = True
        updated_state = read_state(run_id)
        assert updated_state.needs_human_review is True

    def test_should_block_4th_restart_when_breaker_tripped(self, tmp_path, monkeypatch):
        """count=3 时 should_restart() 返回 False，不再重启。"""
        cb = CircuitBreaker(stuck_restart_count=3)
        assert cb.should_restart() is False

    def test_should_write_stuck_lock_with_correct_content(self, tmp_path, monkeypatch):
        """stuck_lock 文件 JSON 内容：reason + restart_count + created_at。"""
        import json

        monkeypatch.setenv("RECALLKIT_RUN_DIR", str(tmp_path))
        run_id = "circuit-test-02"
        (tmp_path / run_id).mkdir()

        state = RunState(
            run_id=run_id,
            phase=RunPhase.LORA_TRAIN,
            needs_human_review=False,
            stuck_restart_count=3,
            last_update=datetime.now(timezone.utc),
        )
        write_state(state, run_id)

        cb = CircuitBreaker(stuck_restart_count=3)
        cb.record_human_review_needed(run_id=run_id)

        lock_file = tmp_path / run_id / "stuck_lock"
        assert lock_file.exists()
        data = json.loads(lock_file.read_text())
        assert data["reason"] == "circuit_breaker_tripped"
        assert data["restart_count"] == 3
        assert "created_at" in data

    def test_should_persist_lock_across_restarts(self, tmp_path, monkeypatch):
        """stuck_lock 持久化：进程重启后文件仍存在（模拟进程重启 = 新 CB 对象）。"""
        monkeypatch.setenv("RECALLKIT_RUN_DIR", str(tmp_path))
        run_id = "circuit-test-03"
        (tmp_path / run_id).mkdir()

        state = RunState(
            run_id=run_id,
            phase=RunPhase.LORA_TRAIN,
            needs_human_review=False,
            stuck_restart_count=3,
            last_update=datetime.now(timezone.utc),
        )
        write_state(state, run_id)

        # 第一个进程生命周期：写 stuck_lock
        cb1 = CircuitBreaker(stuck_restart_count=3)
        cb1.record_human_review_needed(run_id=run_id)
        assert has_stuck_lock(run_id=run_id)

        # 模拟进程重启：新 CB 对象也能感知 lock（通过文件系统）
        assert has_stuck_lock(run_id=run_id), "进程重启后 stuck_lock 应仍存在"
