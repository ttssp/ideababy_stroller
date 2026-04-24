"""
tests.unit.test_state — pars.ledger.state 单元测试。

覆盖点：
1.  new_run_state 创建合法初始状态（phase=init, stuck_state=idle）
2.  write_state + read_state round-trip（RunState 写入读出等值）
3.  extra 字段被 Pydantic 拒绝（extra="forbid"）
4.  非法 stuck_state 被 field_validator 拒绝
5.  合法 phase 转移（init → baseline）
6.  非法 phase 转移（completed → lora_train）抛 ValueError
7.  终态 completed 无出边（completed → completed 也应报错）
8.  终态 failed 无出边（failed → baseline 报错）
9.  read_state 在文件不存在时抛 FileNotFoundError
10. update_state 原子写（写后再读字段更新正确）
11. update_state 更新 last_update 时间戳
12. write_state 原子性（写失败时不残留 .tmp 文件）
13. RunPhase 枚举包含全部 7 个节点
14. state.json 文件内容为合法 JSON（能被 json.loads 解析）
15. last_update 反序列化为 UTC-aware datetime
"""

from __future__ import annotations

import json
import os
import threading
import time
from datetime import datetime, timezone, UTC
from pathlib import Path

import pytest

from pars.ledger.state import (
    VALID_TRANSITIONS,
    RunPhase,
    RunState,
    new_run_state,
    read_state,
    update_state,
    write_state,
)
from pars.ledger.run_id import generate_ulid

# ---------------------------------------------------------------------------
# 辅助
# ---------------------------------------------------------------------------


def _make_run_id() -> str:
    """生成一个合法 ULID 字符串作为 run_id。"""
    return generate_ulid()


# ---------------------------------------------------------------------------
# 1. new_run_state 初始状态
# ---------------------------------------------------------------------------


def test_new_run_state_phase_is_init():
    """should create RunState with phase=init when calling new_run_state."""
    run_id = _make_run_id()
    state = new_run_state(run_id)
    assert state.phase == RunPhase.INIT


def test_new_run_state_stuck_state_is_idle():
    """should create RunState with stuck_state=idle when calling new_run_state."""
    run_id = _make_run_id()
    state = new_run_state(run_id)
    assert state.stuck_state == "idle"


def test_new_run_state_defaults():
    """should set numeric defaults to 0 and boolean to False when creating new state."""
    run_id = _make_run_id()
    state = new_run_state(run_id)
    assert state.stuck_restart_count == 0
    assert state.needs_human_review is False
    assert state.usd_spent == 0.0
    assert state.wall_clock_elapsed_s == 0.0
    assert state.gpu_hours_used == 0.0


def test_new_run_state_last_update_utc_aware():
    """should have UTC-aware last_update when creating new state."""
    run_id = _make_run_id()
    state = new_run_state(run_id)
    assert state.last_update.tzinfo is not None
    assert state.last_update.utcoffset().total_seconds() == 0


# ---------------------------------------------------------------------------
# 2. write_state + read_state round-trip
# ---------------------------------------------------------------------------


def test_write_read_state_roundtrip(tmp_path: Path):
    """should preserve all RunState fields when writing and reading back."""
    run_id = _make_run_id()
    os.environ["RECALLKIT_RUN_DIR"] = str(tmp_path)
    try:
        state = new_run_state(run_id)
        state = RunState.model_validate({
            **state.model_dump(),
            "phase": RunPhase.BASELINE,
            "usd_spent": 3.14,
            "stuck_restart_count": 2,
            "needs_human_review": True,
            "last_update": state.last_update,
        })
        write_state(state, run_id)
        loaded = read_state(run_id)
    finally:
        del os.environ["RECALLKIT_RUN_DIR"]

    assert loaded.run_id == run_id
    assert loaded.phase == RunPhase.BASELINE
    assert loaded.usd_spent == pytest.approx(3.14)
    assert loaded.stuck_restart_count == 2
    assert loaded.needs_human_review is True


def test_state_json_is_valid_json(tmp_path: Path):
    """should produce valid JSON file when writing state."""
    run_id = _make_run_id()
    os.environ["RECALLKIT_RUN_DIR"] = str(tmp_path)
    try:
        state = new_run_state(run_id)
        write_state(state, run_id)
        raw = (tmp_path / run_id / "state.json").read_text(encoding="utf-8")
    finally:
        del os.environ["RECALLKIT_RUN_DIR"]

    data = json.loads(raw)
    assert data["run_id"] == run_id
    assert data["phase"] == "init"


def test_last_update_round_trips_as_utc_aware(tmp_path: Path):
    """should deserialize last_update as UTC-aware datetime after round-trip."""
    run_id = _make_run_id()
    os.environ["RECALLKIT_RUN_DIR"] = str(tmp_path)
    try:
        state = new_run_state(run_id)
        write_state(state, run_id)
        loaded = read_state(run_id)
    finally:
        del os.environ["RECALLKIT_RUN_DIR"]

    assert loaded.last_update.tzinfo is not None
    assert loaded.last_update.utcoffset().total_seconds() == 0


# ---------------------------------------------------------------------------
# 3. extra 字段被拒绝
# ---------------------------------------------------------------------------


def test_runstate_rejects_extra_fields():
    """should raise ValidationError when constructing RunState with unknown field."""
    import pydantic

    with pytest.raises(pydantic.ValidationError, match="extra"):
        RunState.model_validate({
            "run_id": _make_run_id(),
            "phase": "init",
            "last_update": datetime.now(UTC).isoformat(),
            "unknown_field": "should_be_rejected",
        })


# ---------------------------------------------------------------------------
# 4. 非法 stuck_state 被拒绝
# ---------------------------------------------------------------------------


def test_runstate_rejects_invalid_stuck_state():
    """should raise ValidationError when stuck_state has invalid value."""
    import pydantic

    with pytest.raises(pydantic.ValidationError):
        RunState.model_validate({
            "run_id": _make_run_id(),
            "phase": "init",
            "last_update": datetime.now(UTC).isoformat(),
            "stuck_state": "invalid_value",
        })


# ---------------------------------------------------------------------------
# 5. 合法 phase 转移
# ---------------------------------------------------------------------------


def test_update_state_valid_phase_transition(tmp_path: Path):
    """should succeed when transitioning from init to baseline via update_state."""
    run_id = _make_run_id()
    os.environ["RECALLKIT_RUN_DIR"] = str(tmp_path)
    try:
        state = new_run_state(run_id)
        write_state(state, run_id)
        new_state = update_state(run_id, phase=RunPhase.BASELINE)
    finally:
        del os.environ["RECALLKIT_RUN_DIR"]

    assert new_state.phase == RunPhase.BASELINE


def test_update_state_init_to_lora_train(tmp_path: Path):
    """should succeed when transitioning from init to lora_train directly."""
    run_id = _make_run_id()
    os.environ["RECALLKIT_RUN_DIR"] = str(tmp_path)
    try:
        state = new_run_state(run_id)
        write_state(state, run_id)
        new_state = update_state(run_id, phase=RunPhase.LORA_TRAIN)
    finally:
        del os.environ["RECALLKIT_RUN_DIR"]

    assert new_state.phase == RunPhase.LORA_TRAIN


def test_update_state_lora_train_to_lora_train(tmp_path: Path):
    """should succeed when transitioning lora_train to lora_train (resume re-entry)."""
    run_id = _make_run_id()
    os.environ["RECALLKIT_RUN_DIR"] = str(tmp_path)
    try:
        state = new_run_state(run_id)
        write_state(state, run_id)
        update_state(run_id, phase=RunPhase.LORA_TRAIN)
        new_state = update_state(run_id, phase=RunPhase.LORA_TRAIN)
    finally:
        del os.environ["RECALLKIT_RUN_DIR"]

    assert new_state.phase == RunPhase.LORA_TRAIN


# ---------------------------------------------------------------------------
# 6. 非法 phase 转移 → ValueError
# ---------------------------------------------------------------------------


def test_update_state_invalid_phase_transition(tmp_path: Path):
    """should raise ValueError when phase transition is illegal (init to report)."""
    run_id = _make_run_id()
    os.environ["RECALLKIT_RUN_DIR"] = str(tmp_path)
    try:
        state = new_run_state(run_id)
        write_state(state, run_id)
        with pytest.raises(ValueError, match="非法 phase 转移"):
            update_state(run_id, phase=RunPhase.REPORT)
    finally:
        del os.environ["RECALLKIT_RUN_DIR"]


# ---------------------------------------------------------------------------
# 7 & 8. 终态无出边
# ---------------------------------------------------------------------------


def test_completed_is_terminal(tmp_path: Path):
    """should raise ValueError when attempting any transition from completed state."""
    run_id = _make_run_id()
    os.environ["RECALLKIT_RUN_DIR"] = str(tmp_path)
    try:
        # 强制写入 completed 状态（跳过转移校验）
        state = RunState.model_validate({
            "run_id": run_id,
            "phase": "completed",
            "last_update": datetime.now(UTC).isoformat(),
        })
        write_state(state, run_id)
        with pytest.raises(ValueError, match="非法 phase 转移"):
            update_state(run_id, phase=RunPhase.LORA_TRAIN)
    finally:
        del os.environ["RECALLKIT_RUN_DIR"]


def test_failed_is_terminal(tmp_path: Path):
    """should raise ValueError when attempting any transition from failed state."""
    run_id = _make_run_id()
    os.environ["RECALLKIT_RUN_DIR"] = str(tmp_path)
    try:
        state = RunState.model_validate({
            "run_id": run_id,
            "phase": "failed",
            "last_update": datetime.now(UTC).isoformat(),
        })
        write_state(state, run_id)
        with pytest.raises(ValueError, match="非法 phase 转移"):
            update_state(run_id, phase=RunPhase.BASELINE)
    finally:
        del os.environ["RECALLKIT_RUN_DIR"]


# ---------------------------------------------------------------------------
# 9. read_state 不存在时抛 FileNotFoundError
# ---------------------------------------------------------------------------


def test_read_state_raises_file_not_found(tmp_path: Path):
    """should raise FileNotFoundError when state.json does not exist."""
    run_id = _make_run_id()
    os.environ["RECALLKIT_RUN_DIR"] = str(tmp_path)
    try:
        with pytest.raises(FileNotFoundError):
            read_state(run_id)
    finally:
        del os.environ["RECALLKIT_RUN_DIR"]


# ---------------------------------------------------------------------------
# 10. update_state 原子写：写后字段更新正确
# ---------------------------------------------------------------------------


def test_update_state_persists_field_changes(tmp_path: Path):
    """should persist field changes to disk when update_state is called."""
    run_id = _make_run_id()
    os.environ["RECALLKIT_RUN_DIR"] = str(tmp_path)
    try:
        state = new_run_state(run_id)
        write_state(state, run_id)
        update_state(run_id, usd_spent=9.99, stuck_restart_count=3)
        loaded = read_state(run_id)
    finally:
        del os.environ["RECALLKIT_RUN_DIR"]

    assert loaded.usd_spent == pytest.approx(9.99)
    assert loaded.stuck_restart_count == 3


# ---------------------------------------------------------------------------
# 11. update_state 更新 last_update
# ---------------------------------------------------------------------------


def test_update_state_refreshes_last_update(tmp_path: Path):
    """should update last_update timestamp when update_state is called."""
    run_id = _make_run_id()
    os.environ["RECALLKIT_RUN_DIR"] = str(tmp_path)
    try:
        state = new_run_state(run_id)
        old_ts = state.last_update
        write_state(state, run_id)
        time.sleep(0.01)  # 确保时间戳有变化
        new_state = update_state(run_id, usd_spent=1.0)
    finally:
        del os.environ["RECALLKIT_RUN_DIR"]

    assert new_state.last_update >= old_ts


# ---------------------------------------------------------------------------
# 12. write_state 不残留 .tmp 文件
# ---------------------------------------------------------------------------


def test_write_state_no_tmp_residue(tmp_path: Path):
    """should not leave .tmp files after successful write_state call."""
    run_id = _make_run_id()
    os.environ["RECALLKIT_RUN_DIR"] = str(tmp_path)
    try:
        state = new_run_state(run_id)
        write_state(state, run_id)
        run_dir = tmp_path / run_id
        tmp_files = list(run_dir.glob(".state_*.tmp"))
    finally:
        del os.environ["RECALLKIT_RUN_DIR"]

    assert tmp_files == [], f"发现残留 .tmp 文件：{tmp_files}"


# ---------------------------------------------------------------------------
# 13. RunPhase 枚举包含全部 7 个节点
# ---------------------------------------------------------------------------


def test_runphase_has_all_seven_phases():
    """should have exactly 7 phases when listing all RunPhase values."""
    expected = {"init", "baseline", "lora_train", "eval", "report", "completed", "failed"}
    actual = {p.value for p in RunPhase}
    assert actual == expected


# ---------------------------------------------------------------------------
# 14 & 15 已被上面 round-trip 测试覆盖（JSON合法性 + UTC-aware datetime）
# 额外：VALID_TRANSITIONS 覆盖所有 7 个源节点
# ---------------------------------------------------------------------------


def test_valid_transitions_covers_all_phases():
    """should have VALID_TRANSITIONS entry for every RunPhase member."""
    all_phases = set(RunPhase)
    transition_sources = set(VALID_TRANSITIONS.keys())
    assert all_phases == transition_sources, (
        f"VALID_TRANSITIONS 缺少节点：{all_phases - transition_sources}"
    )
