"""
tests/e2e/test_o3_resume.py — T026 Outcome O3 E2E 测试。

结论：验证 can_resume() 的正向路径（有 checkpoint + 非终态）和
      负向路径（stuck_lock 存在 / 终态 / 无 checkpoint）的行为正确性。

## 验证 Outcome O3

O3（architecture §4）：中断后可 resume —
can_resume() 必须在有 checkpoint + 非终态 + 无 stuck_lock + 指纹匹配时返回 (True, "")，
在任一前置条件不满足时返回 (False, <reason>)。
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import pytest

from pars.ledger.state import RunPhase, write_state, new_run_state
from pars.orch.resume import can_resume
from pars.stuck.stuck_lock import write_stuck_lock


# ---------------------------------------------------------------------------
# T026-O3-TC01: 合成正向 — 有 checkpoint + lora_train phase → can_resume True
# ---------------------------------------------------------------------------


@pytest.mark.e2e
def test_o3_can_resume_returns_true_with_valid_checkpoint(
    tmp_runs_dir: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """should return (True, '') when checkpoint exists and phase is non-terminal.

    结论：构造 lora_train phase + 非空 checkpoint 目录 + 无 stuck_lock + 无指纹文件，
          can_resume() 应返回 (True, "")（无指纹文件按向后兼容放行）。
    """
    run_id = "test-o3-resume-ok-01"

    # 创建 run 目录结构
    run_dir = tmp_runs_dir / run_id
    run_dir.mkdir(parents=True)

    # 写入 state.json（phase=lora_train，非终态）
    state = new_run_state(run_id)
    # 手动写 JSON，因为 update_state 需要从 init 转移（state machine 验证）
    state_data = {
        "run_id": run_id,
        "phase": "lora_train",
        "stuck_state": "idle",
        "stuck_restart_count": 0,
        "needs_human_review": False,
        "usd_spent": 0.05,
        "wall_clock_elapsed_s": 120.0,
        "gpu_hours_used": 0.03,
        "last_update": datetime.now(tz=timezone.utc).isoformat(),
    }
    (run_dir / "state.json").write_text(json.dumps(state_data), encoding="utf-8")

    # 创建非空 checkpoint 目录
    # can_resume 通过 ckpt_dir(run_id) 查找，需要设置 RECALLKIT_CKPT_DIR
    ckpt_root = tmp_runs_dir.parent / "checkpoints"
    ckpt_root.mkdir(parents=True, exist_ok=True)
    monkeypatch.setenv("RECALLKIT_CKPT_DIR", str(ckpt_root))

    ckpt_dir = ckpt_root / run_id
    ckpt_dir.mkdir(parents=True)
    (ckpt_dir / "adapter_model.bin").write_bytes(b"fake_checkpoint_data")

    # 不创建 machine_fingerprint.json → 向后兼容放行
    # 不创建 stuck_lock → 无锁

    ok, reason = can_resume(run_id)

    assert ok is True, f"有 checkpoint + 非终态时 can_resume 应返回 True，reason={reason!r}"
    assert reason == "" or reason.strip() == "", (
        f"成功时 reason 应为空串，实际：{reason!r}"
    )


# ---------------------------------------------------------------------------
# T026-O3-TC02: 合成负向 — stuck_lock 存在时 can_resume False
# ---------------------------------------------------------------------------


@pytest.mark.e2e
def test_o3_can_resume_returns_false_when_stuck_lock_exists(
    tmp_runs_dir: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """should return (False, msg) when stuck_lock file is present.

    结论：has_stuck_lock() 检测到锁文件时，can_resume 应拒绝并在 reason 中提示解锁。
    """
    run_id = "test-o3-stuck-lock-01"
    run_dir = tmp_runs_dir / run_id
    run_dir.mkdir(parents=True)

    # 写入非终态 state.json
    state_data = {
        "run_id": run_id,
        "phase": "lora_train",
        "stuck_state": "truly_stuck",
        "stuck_restart_count": 3,
        "needs_human_review": True,
        "usd_spent": 0.10,
        "wall_clock_elapsed_s": 600.0,
        "gpu_hours_used": 0.10,
        "last_update": datetime.now(tz=timezone.utc).isoformat(),
    }
    (run_dir / "state.json").write_text(json.dumps(state_data), encoding="utf-8")

    # 创建非空 checkpoint（绕过检查 2）
    ckpt_root = tmp_runs_dir.parent / "checkpoints"
    ckpt_root.mkdir(parents=True, exist_ok=True)
    monkeypatch.setenv("RECALLKIT_CKPT_DIR", str(ckpt_root))
    ckpt_dir_path = ckpt_root / run_id
    ckpt_dir_path.mkdir(parents=True)
    (ckpt_dir_path / "adapter_model.bin").write_bytes(b"fake")

    # 写入 stuck_lock（触发检查 3 失败）
    write_stuck_lock(run_id=run_id, reason="truly_stuck after 3 restarts", restart_count=3)

    ok, reason = can_resume(run_id)

    assert ok is False, "stuck_lock 存在时 can_resume 应返回 False"
    # reason 应含 stuck_lock 相关关键词
    assert "stuck_lock" in reason.lower() or "unlock" in reason.lower(), (
        f"reason 应提及 stuck_lock 或 unlock，实际：{reason!r}"
    )


# ---------------------------------------------------------------------------
# T026-O3-TC03: 合成负向 — 终态 phase 时 can_resume False
# ---------------------------------------------------------------------------


@pytest.mark.e2e
def test_o3_can_resume_returns_false_when_phase_is_completed(
    tmp_runs_dir: Path,
) -> None:
    """should return (False, msg) when run phase is terminal (completed).

    结论：completed 为终态，can_resume 应立即返回 False（在检查 checkpoint 之前）。
    """
    run_id = "test-o3-terminal-01"
    run_dir = tmp_runs_dir / run_id
    run_dir.mkdir(parents=True)

    # 写入终态 state.json
    state_data = {
        "run_id": run_id,
        "phase": "completed",
        "stuck_state": "idle",
        "stuck_restart_count": 0,
        "needs_human_review": False,
        "usd_spent": 0.25,
        "wall_clock_elapsed_s": 1800.0,
        "gpu_hours_used": 0.50,
        "last_update": datetime.now(tz=timezone.utc).isoformat(),
    }
    (run_dir / "state.json").write_text(json.dumps(state_data), encoding="utf-8")

    ok, reason = can_resume(run_id)

    assert ok is False, "completed 终态时 can_resume 应返回 False"
    # reason 应提示终态
    assert "completed" in reason.lower() or "终态" in reason, (
        f"reason 应提及 completed 或终态，实际：{reason!r}"
    )


# ---------------------------------------------------------------------------
# T026-O3-TC04: 合成负向 — 无 checkpoint 时 can_resume False
# ---------------------------------------------------------------------------


@pytest.mark.e2e
def test_o3_can_resume_returns_false_when_no_checkpoint(
    tmp_runs_dir: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """should return (False, msg) when checkpoint directory is missing or empty.

    结论：checkpoint 目录不存在时，can_resume 应在检查 2 拒绝。
    """
    run_id = "test-o3-no-ckpt-01"
    run_dir = tmp_runs_dir / run_id
    run_dir.mkdir(parents=True)

    # 写入非终态 state.json
    state_data = {
        "run_id": run_id,
        "phase": "lora_train",
        "stuck_state": "idle",
        "stuck_restart_count": 0,
        "needs_human_review": False,
        "usd_spent": 0.02,
        "wall_clock_elapsed_s": 60.0,
        "gpu_hours_used": 0.01,
        "last_update": datetime.now(tz=timezone.utc).isoformat(),
    }
    (run_dir / "state.json").write_text(json.dumps(state_data), encoding="utf-8")

    # 设置 checkpoint 根目录（但不创建 run_id 子目录）
    ckpt_root = tmp_runs_dir.parent / "checkpoints_empty"
    ckpt_root.mkdir(parents=True, exist_ok=True)
    monkeypatch.setenv("RECALLKIT_CKPT_DIR", str(ckpt_root))
    # 不创建 ckpt_root / run_id

    ok, reason = can_resume(run_id)

    assert ok is False, "无 checkpoint 时 can_resume 应返回 False"
    assert len(reason) > 0, "reason 应非空"
