"""
tests.integration.test_resume_after_kill — resume 逻辑集成测试（T019 · O3 · C13 · C22）

结论：验证 pars sft resume 的 5 大核心路径：
1. 正常 resume：非终态 + checkpoint 非空 + 同机指纹 → can_resume() True
2. 终态拒绝：completed/failed run → can_resume() False
3. 空 checkpoint 拒绝：checkpoint 目录为空 → False
4. stuck_lock 拒绝：stuck_lock 存在 → False + 提示 pars unlock
5. 机器指纹 hard reject：GPU/CUDA/os_major 不同 → False + cross-machine 提示
6. 指纹文件缺失兜底：旧 run 无指纹文件 → warning + 允许 resume
7. warning 不阻断：python patch 升级 / os patch 升级 → True（warn 不 reject）
8. CLI：pars sft resume --run-id=<id> --yes → 退出码 2 for blocked, 0 for ready
       非存在 run → 退出码 2 + 友好提示

注意：
- 不依赖真实训练（无 GPU 依赖）
- 使用 tmp_path 隔离文件系统
- marker: integration（非 CI slow）
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from unittest.mock import patch

import pytest

from click.testing import CliRunner


# ---------------------------------------------------------------------------
# Markers
# ---------------------------------------------------------------------------

pytestmark = pytest.mark.integration


# ---------------------------------------------------------------------------
# 辅助：构建 state.json + fingerprint + checkpoint 目录
# ---------------------------------------------------------------------------

def _write_state(run_dir: Path, run_id: str, phase: str, checkpoint_path: str | None = None) -> None:
    """写 state.json 到 run_dir/<run_id>/state.json。"""
    run_dir.mkdir(parents=True, exist_ok=True)
    state_path = run_dir / "state.json"
    state_data: dict[str, Any] = {
        "run_id": run_id,
        "phase": phase,
        "current_script": None,
        "checkpoint_path": checkpoint_path,
        "last_epoch_completed": None,
        "stuck_state": "idle",
        "stuck_restart_count": 0,
        "needs_human_review": False,
        "usd_spent": 0.0,
        "wall_clock_elapsed_s": 0.0,
        "gpu_hours_used": 0.0,
        "last_update": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f+00:00"),
    }
    if checkpoint_path:
        state_data["checkpoint_path"] = checkpoint_path
    state_path.write_text(json.dumps(state_data, indent=2, ensure_ascii=False), encoding="utf-8")


def _write_fingerprint(run_dir: Path, fp: dict) -> None:
    """写 machine_fingerprint.json 到 run_dir/machine_fingerprint.json。"""
    fp_path = run_dir / "machine_fingerprint.json"
    fp_path.write_text(json.dumps(fp, indent=2, ensure_ascii=False), encoding="utf-8")


def _make_checkpoint(ckpt_run_dir: Path) -> None:
    """在 ckpt_run_dir 创建一个非空的 checkpoint 目录（模拟训练存档）。"""
    ckpt_run_dir.mkdir(parents=True, exist_ok=True)
    (ckpt_run_dir / "adapter_model.safetensors").write_bytes(b"\x00" * 16)


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


# ---------------------------------------------------------------------------
# 集成测试：can_resume() 逻辑链
# ---------------------------------------------------------------------------

class TestCanResume:
    """can_resume(run_id) -> (bool, str) 的集成验证。"""

    def test_should_allow_resume_when_state_is_lora_train_and_checkpoint_nonempty(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """should return True when run is in lora_train phase with checkpoint available."""
        run_id = "test-run-resume-ok"
        runs_dir = tmp_path / "runs"
        ckpts_dir = tmp_path / "checkpoints"
        monkeypatch.setenv("RECALLKIT_RUN_DIR", str(runs_dir))
        monkeypatch.setenv("RECALLKIT_CKPT_DIR", str(ckpts_dir))

        run_dir = runs_dir / run_id
        run_dir.mkdir(parents=True, exist_ok=True)
        ckpt_run_dir = ckpts_dir / run_id
        _make_checkpoint(ckpt_run_dir)

        _write_state(run_dir, run_id, "lora_train", checkpoint_path=str(ckpt_run_dir))
        saved_fp = _fp()
        _write_fingerprint(run_dir, saved_fp)

        from pars.orch.resume import can_resume

        # mock current machine fingerprint 与保存一致
        with patch("pars.orch.resume.collect_fingerprint", return_value=saved_fp):
            ok, reason = can_resume(run_id)

        assert ok is True, f"预期 can_resume=True，实际 reason={reason!r}"

    def test_should_allow_resume_when_phase_is_eval(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """should allow resume when run is in eval phase (training done, only eval left)."""
        run_id = "test-run-eval-phase"
        runs_dir = tmp_path / "runs"
        ckpts_dir = tmp_path / "checkpoints"
        monkeypatch.setenv("RECALLKIT_RUN_DIR", str(runs_dir))
        monkeypatch.setenv("RECALLKIT_CKPT_DIR", str(ckpts_dir))

        run_dir = runs_dir / run_id
        run_dir.mkdir(parents=True, exist_ok=True)
        ckpt_run_dir = ckpts_dir / run_id
        _make_checkpoint(ckpt_run_dir)

        _write_state(run_dir, run_id, "eval", checkpoint_path=str(ckpt_run_dir))
        saved_fp = _fp()
        _write_fingerprint(run_dir, saved_fp)

        from pars.orch.resume import can_resume

        with patch("pars.orch.resume.collect_fingerprint", return_value=saved_fp):
            ok, reason = can_resume(run_id)

        assert ok is True, f"eval phase 应允许 resume, reason={reason!r}"

    def test_should_reject_resume_when_phase_is_completed(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """should return False with 'already completed' when run is in completed phase."""
        run_id = "test-run-completed"
        runs_dir = tmp_path / "runs"
        ckpts_dir = tmp_path / "checkpoints"
        monkeypatch.setenv("RECALLKIT_RUN_DIR", str(runs_dir))
        monkeypatch.setenv("RECALLKIT_CKPT_DIR", str(ckpts_dir))

        run_dir = runs_dir / run_id
        run_dir.mkdir(parents=True, exist_ok=True)

        _write_state(run_dir, run_id, "completed")

        from pars.orch.resume import can_resume

        ok, reason = can_resume(run_id)

        assert ok is False, "已完成 run 不应允许 resume"
        assert "completed" in reason.lower() or "终态" in reason or "already" in reason.lower()

    def test_should_reject_resume_when_phase_is_failed(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """should return False when run is in failed phase."""
        run_id = "test-run-failed"
        runs_dir = tmp_path / "runs"
        ckpts_dir = tmp_path / "checkpoints"
        monkeypatch.setenv("RECALLKIT_RUN_DIR", str(runs_dir))
        monkeypatch.setenv("RECALLKIT_CKPT_DIR", str(ckpts_dir))

        run_dir = runs_dir / run_id
        run_dir.mkdir(parents=True, exist_ok=True)
        _write_state(run_dir, run_id, "failed")

        from pars.orch.resume import can_resume

        ok, reason = can_resume(run_id)

        assert ok is False, "failed run 不应允许 resume"

    def test_should_reject_resume_when_checkpoint_dir_is_empty(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """should return False when checkpoint directory exists but is empty."""
        run_id = "test-run-empty-ckpt"
        runs_dir = tmp_path / "runs"
        ckpts_dir = tmp_path / "checkpoints"
        monkeypatch.setenv("RECALLKIT_RUN_DIR", str(runs_dir))
        monkeypatch.setenv("RECALLKIT_CKPT_DIR", str(ckpts_dir))

        run_dir = runs_dir / run_id
        run_dir.mkdir(parents=True, exist_ok=True)
        # checkpoint 目录存在但为空
        (ckpts_dir / run_id).mkdir(parents=True, exist_ok=True)

        _write_state(run_dir, run_id, "lora_train")
        _write_fingerprint(run_dir, _fp())

        from pars.orch.resume import can_resume

        with patch("pars.orch.resume.collect_fingerprint", return_value=_fp()):
            ok, reason = can_resume(run_id)

        assert ok is False, "checkpoint 为空不应允许 resume"
        assert "checkpoint" in reason.lower() or "空" in reason

    def test_should_reject_resume_when_checkpoint_dir_not_exist(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """should return False when checkpoint directory does not exist."""
        run_id = "test-run-no-ckpt-dir"
        runs_dir = tmp_path / "runs"
        ckpts_dir = tmp_path / "checkpoints"
        monkeypatch.setenv("RECALLKIT_RUN_DIR", str(runs_dir))
        monkeypatch.setenv("RECALLKIT_CKPT_DIR", str(ckpts_dir))

        run_dir = runs_dir / run_id
        run_dir.mkdir(parents=True, exist_ok=True)
        # 不创建 checkpoint 目录

        _write_state(run_dir, run_id, "lora_train")
        _write_fingerprint(run_dir, _fp())

        from pars.orch.resume import can_resume

        with patch("pars.orch.resume.collect_fingerprint", return_value=_fp()):
            ok, reason = can_resume(run_id)

        assert ok is False

    def test_should_reject_resume_when_run_id_not_found(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """should return False when run_id does not exist (state.json missing)."""
        runs_dir = tmp_path / "runs"
        ckpts_dir = tmp_path / "checkpoints"
        monkeypatch.setenv("RECALLKIT_RUN_DIR", str(runs_dir))
        monkeypatch.setenv("RECALLKIT_CKPT_DIR", str(ckpts_dir))

        runs_dir.mkdir(parents=True, exist_ok=True)

        from pars.orch.resume import can_resume

        ok, reason = can_resume("nonexistent-run-id")

        assert ok is False
        assert len(reason) > 0, "应有说明性 reason 字符串"

    # --- stuck_lock 拒绝 ---

    def test_should_reject_resume_when_stuck_lock_exists(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """should return False with unlock hint when stuck_lock file is present."""
        run_id = "test-run-stuck-locked"
        runs_dir = tmp_path / "runs"
        ckpts_dir = tmp_path / "checkpoints"
        monkeypatch.setenv("RECALLKIT_RUN_DIR", str(runs_dir))
        monkeypatch.setenv("RECALLKIT_CKPT_DIR", str(ckpts_dir))

        run_dir = runs_dir / run_id
        run_dir.mkdir(parents=True, exist_ok=True)
        ckpt_run_dir = ckpts_dir / run_id
        _make_checkpoint(ckpt_run_dir)

        _write_state(run_dir, run_id, "lora_train", checkpoint_path=str(ckpt_run_dir))
        _write_fingerprint(run_dir, _fp())

        # 创建 stuck_lock 文件
        (run_dir / "stuck_lock").write_text(
            json.dumps({"reason": "truly_stuck", "timestamp": "2026-01-01T00:00:00+00:00"}),
            encoding="utf-8",
        )

        from pars.orch.resume import can_resume

        with patch("pars.orch.resume.collect_fingerprint", return_value=_fp()):
            ok, reason = can_resume(run_id)

        assert ok is False, "stuck_lock 存在应拒绝 resume"
        assert "unlock" in reason.lower() or "stuck" in reason.lower(), (
            f"应提示 pars unlock，实际 reason={reason!r}"
        )

    # --- 机器指纹 hard reject ---

    def test_should_reject_resume_when_gpu_name_differs(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """should return False with cross-machine message when gpu_name differs."""
        run_id = "test-run-gpu-mismatch"
        runs_dir = tmp_path / "runs"
        ckpts_dir = tmp_path / "checkpoints"
        monkeypatch.setenv("RECALLKIT_RUN_DIR", str(runs_dir))
        monkeypatch.setenv("RECALLKIT_CKPT_DIR", str(ckpts_dir))

        run_dir = runs_dir / run_id
        run_dir.mkdir(parents=True, exist_ok=True)
        ckpt_run_dir = ckpts_dir / run_id
        _make_checkpoint(ckpt_run_dir)

        saved_fp = _fp(gpu_name="NVIDIA GeForce RTX 4090")
        current_fp = _fp(gpu_name="NVIDIA H200 141GB")

        _write_state(run_dir, run_id, "lora_train", checkpoint_path=str(ckpt_run_dir))
        _write_fingerprint(run_dir, saved_fp)

        from pars.orch.resume import can_resume

        with patch("pars.orch.resume.collect_fingerprint", return_value=current_fp):
            ok, reason = can_resume(run_id)

        assert ok is False, "GPU 不同应 hard reject"
        assert "cross-machine" in reason.lower() or "gpu_name" in reason
        assert "h200-rsync-playbook" in reason.lower() or "mismatch" in reason.lower()

    def test_should_reject_resume_when_cuda_version_differs(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """should return False when CUDA major.minor version differs."""
        run_id = "test-run-cuda-mismatch"
        runs_dir = tmp_path / "runs"
        ckpts_dir = tmp_path / "checkpoints"
        monkeypatch.setenv("RECALLKIT_RUN_DIR", str(runs_dir))
        monkeypatch.setenv("RECALLKIT_CKPT_DIR", str(ckpts_dir))

        run_dir = runs_dir / run_id
        run_dir.mkdir(parents=True, exist_ok=True)
        ckpt_run_dir = ckpts_dir / run_id
        _make_checkpoint(ckpt_run_dir)

        saved_fp = _fp(cuda_version="12.4")
        current_fp = _fp(cuda_version="12.6")

        _write_state(run_dir, run_id, "lora_train", checkpoint_path=str(ckpt_run_dir))
        _write_fingerprint(run_dir, saved_fp)

        from pars.orch.resume import can_resume

        with patch("pars.orch.resume.collect_fingerprint", return_value=current_fp):
            ok, reason = can_resume(run_id)

        assert ok is False, "CUDA 版本不同应 hard reject"

    def test_should_reject_resume_when_os_major_differs(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """should return False when os_major (derived) differs."""
        run_id = "test-run-os-major-mismatch"
        runs_dir = tmp_path / "runs"
        ckpts_dir = tmp_path / "checkpoints"
        monkeypatch.setenv("RECALLKIT_RUN_DIR", str(runs_dir))
        monkeypatch.setenv("RECALLKIT_CKPT_DIR", str(ckpts_dir))

        run_dir = runs_dir / run_id
        run_dir.mkdir(parents=True, exist_ok=True)
        ckpt_run_dir = ckpts_dir / run_id
        _make_checkpoint(ckpt_run_dir)

        saved_fp = _fp(os_name="Darwin", os_release="24.0.0")    # Darwin 24
        current_fp = _fp(os_name="Darwin", os_release="25.2.0")  # Darwin 25

        _write_state(run_dir, run_id, "lora_train", checkpoint_path=str(ckpt_run_dir))
        _write_fingerprint(run_dir, saved_fp)

        from pars.orch.resume import can_resume

        with patch("pars.orch.resume.collect_fingerprint", return_value=current_fp):
            ok, reason = can_resume(run_id)

        assert ok is False, "os_major 不同应 hard reject"
        assert "os_major" in reason

    # --- warning 不阻断 ---

    def test_should_allow_resume_when_python_patch_version_differs(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """should allow resume (with warning) when only python patch version changed."""
        run_id = "test-run-python-patch"
        runs_dir = tmp_path / "runs"
        ckpts_dir = tmp_path / "checkpoints"
        monkeypatch.setenv("RECALLKIT_RUN_DIR", str(runs_dir))
        monkeypatch.setenv("RECALLKIT_CKPT_DIR", str(ckpts_dir))

        run_dir = runs_dir / run_id
        run_dir.mkdir(parents=True, exist_ok=True)
        ckpt_run_dir = ckpts_dir / run_id
        _make_checkpoint(ckpt_run_dir)

        saved_fp = _fp(python_version="3.12.4")
        current_fp = _fp(python_version="3.12.5")

        _write_state(run_dir, run_id, "lora_train", checkpoint_path=str(ckpt_run_dir))
        _write_fingerprint(run_dir, saved_fp)

        from pars.orch.resume import can_resume

        with patch("pars.orch.resume.collect_fingerprint", return_value=current_fp):
            ok, reason = can_resume(run_id)

        assert ok is True, f"python patch 升级不应拒绝 resume，reason={reason!r}"

    def test_should_allow_resume_when_os_patch_version_differs_but_major_same(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """should allow resume when os_release patch changes but os_major unchanged."""
        run_id = "test-run-os-patch"
        runs_dir = tmp_path / "runs"
        ckpts_dir = tmp_path / "checkpoints"
        monkeypatch.setenv("RECALLKIT_RUN_DIR", str(runs_dir))
        monkeypatch.setenv("RECALLKIT_CKPT_DIR", str(ckpts_dir))

        run_dir = runs_dir / run_id
        run_dir.mkdir(parents=True, exist_ok=True)
        ckpt_run_dir = ckpts_dir / run_id
        _make_checkpoint(ckpt_run_dir)

        saved_fp = _fp(os_name="Darwin", os_release="25.2.0")
        current_fp = _fp(os_name="Darwin", os_release="25.2.1")

        _write_state(run_dir, run_id, "lora_train", checkpoint_path=str(ckpt_run_dir))
        _write_fingerprint(run_dir, saved_fp)

        from pars.orch.resume import can_resume

        with patch("pars.orch.resume.collect_fingerprint", return_value=current_fp):
            ok, reason = can_resume(run_id)

        assert ok is True, f"os patch 升级不应拒绝 resume（os_major 未变），reason={reason!r}"

    # --- 指纹文件缺失兜底 ---

    def test_should_allow_resume_when_fingerprint_file_missing(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """should allow resume with warning when machine_fingerprint.json is missing (old run)."""
        run_id = "test-run-no-fp"
        runs_dir = tmp_path / "runs"
        ckpts_dir = tmp_path / "checkpoints"
        monkeypatch.setenv("RECALLKIT_RUN_DIR", str(runs_dir))
        monkeypatch.setenv("RECALLKIT_CKPT_DIR", str(ckpts_dir))

        run_dir = runs_dir / run_id
        run_dir.mkdir(parents=True, exist_ok=True)
        ckpt_run_dir = ckpts_dir / run_id
        _make_checkpoint(ckpt_run_dir)

        # 不写 fingerprint 文件（旧 run 兼容）
        _write_state(run_dir, run_id, "lora_train", checkpoint_path=str(ckpt_run_dir))

        from pars.orch.resume import can_resume

        with patch("pars.orch.resume.collect_fingerprint", return_value=_fp()):
            ok, reason = can_resume(run_id)

        # 向后兼容：允许 resume（reason 可能是空串或包含 warning 字样）
        assert ok is True, f"指纹文件缺失应向后兼容允许 resume，reason={reason!r}"


# ---------------------------------------------------------------------------
# 集成测试：find_latest_checkpoint()
# ---------------------------------------------------------------------------

class TestFindLatestCheckpoint:
    """find_latest_checkpoint(run_id) -> Path | None 的集成验证。"""

    def test_should_return_none_when_checkpoint_dir_not_exist(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """should return None when checkpoint directory does not exist."""
        ckpts_dir = tmp_path / "checkpoints"
        monkeypatch.setenv("RECALLKIT_CKPT_DIR", str(ckpts_dir))

        from pars.orch.resume import find_latest_checkpoint

        result = find_latest_checkpoint("no-such-run")
        assert result is None

    def test_should_return_none_when_checkpoint_dir_is_empty(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """should return None when checkpoint directory exists but is empty."""
        run_id = "test-run-empty-ckpt"
        ckpts_dir = tmp_path / "checkpoints"
        monkeypatch.setenv("RECALLKIT_CKPT_DIR", str(ckpts_dir))

        (ckpts_dir / run_id).mkdir(parents=True, exist_ok=True)

        from pars.orch.resume import find_latest_checkpoint

        result = find_latest_checkpoint(run_id)
        assert result is None

    def test_should_return_checkpoint_dir_when_nonempty(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """should return the checkpoint dir Path when it contains files."""
        run_id = "test-run-has-ckpt"
        ckpts_dir = tmp_path / "checkpoints"
        monkeypatch.setenv("RECALLKIT_CKPT_DIR", str(ckpts_dir))

        ckpt_run_dir = ckpts_dir / run_id
        _make_checkpoint(ckpt_run_dir)

        from pars.orch.resume import find_latest_checkpoint

        result = find_latest_checkpoint(run_id)
        assert result is not None
        assert result.exists()
        assert result.is_dir()


# ---------------------------------------------------------------------------
# 集成测试：CLI pars sft resume 子命令
# ---------------------------------------------------------------------------

class TestResumeCliCommand:
    """pars sft resume CLI 子命令端到端测试（使用 click.testing.CliRunner）。"""

    def _get_cli(self):
        from pars.cli.main import cli
        return cli

    def test_cli_resume_exits_2_when_run_not_found(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """should exit with code 2 and friendly message when run_id does not exist."""
        runs_dir = tmp_path / "runs"
        ckpts_dir = tmp_path / "checkpoints"
        monkeypatch.setenv("RECALLKIT_RUN_DIR", str(runs_dir))
        monkeypatch.setenv("RECALLKIT_CKPT_DIR", str(ckpts_dir))
        runs_dir.mkdir(parents=True, exist_ok=True)

        runner = CliRunner()
        result = runner.invoke(self._get_cli(), ["sft", "resume", "--run-id", "nonexistent-run", "--yes"])

        assert result.exit_code == 2, f"预期退出码 2，实际 {result.exit_code}: {result.output}"

    def test_cli_resume_exits_2_when_completed_run(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """should exit with code 2 when run is completed."""
        run_id = "cli-test-completed"
        runs_dir = tmp_path / "runs"
        ckpts_dir = tmp_path / "checkpoints"
        monkeypatch.setenv("RECALLKIT_RUN_DIR", str(runs_dir))
        monkeypatch.setenv("RECALLKIT_CKPT_DIR", str(ckpts_dir))

        run_dir = runs_dir / run_id
        run_dir.mkdir(parents=True, exist_ok=True)
        _write_state(run_dir, run_id, "completed")

        runner = CliRunner()
        result = runner.invoke(self._get_cli(), ["sft", "resume", "--run-id", run_id, "--yes"])

        assert result.exit_code == 2, f"completed run 应返回退出码 2: {result.output}"

    def test_cli_resume_exits_2_when_stuck_lock_exists(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """should exit with code 2 and unlock hint when stuck_lock is present."""
        run_id = "cli-test-stuck"
        runs_dir = tmp_path / "runs"
        ckpts_dir = tmp_path / "checkpoints"
        monkeypatch.setenv("RECALLKIT_RUN_DIR", str(runs_dir))
        monkeypatch.setenv("RECALLKIT_CKPT_DIR", str(ckpts_dir))

        run_dir = runs_dir / run_id
        run_dir.mkdir(parents=True, exist_ok=True)
        ckpt_run_dir = ckpts_dir / run_id
        _make_checkpoint(ckpt_run_dir)

        _write_state(run_dir, run_id, "lora_train", checkpoint_path=str(ckpt_run_dir))
        _write_fingerprint(run_dir, _fp())
        (run_dir / "stuck_lock").write_text(
            json.dumps({"reason": "truly_stuck", "timestamp": "2026-01-01T00:00:00+00:00"}),
            encoding="utf-8",
        )

        runner = CliRunner()
        with patch("pars.orch.resume.collect_fingerprint", return_value=_fp()):
            result = runner.invoke(self._get_cli(), ["sft", "resume", "--run-id", run_id, "--yes"])

        assert result.exit_code == 2
        assert "unlock" in result.output.lower() or "stuck" in result.output.lower()

    def test_cli_resume_exits_2_on_cross_machine_hard_reject(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """should exit 2 with cross-machine message when GPU fingerprint mismatches."""
        run_id = "cli-test-gpu-mismatch"
        runs_dir = tmp_path / "runs"
        ckpts_dir = tmp_path / "checkpoints"
        monkeypatch.setenv("RECALLKIT_RUN_DIR", str(runs_dir))
        monkeypatch.setenv("RECALLKIT_CKPT_DIR", str(ckpts_dir))

        run_dir = runs_dir / run_id
        run_dir.mkdir(parents=True, exist_ok=True)
        ckpt_run_dir = ckpts_dir / run_id
        _make_checkpoint(ckpt_run_dir)

        saved_fp = _fp(gpu_name="NVIDIA GeForce RTX 4090")
        current_fp = _fp(gpu_name="NVIDIA H200 141GB")

        _write_state(run_dir, run_id, "lora_train", checkpoint_path=str(ckpt_run_dir))
        _write_fingerprint(run_dir, saved_fp)

        runner = CliRunner()
        with patch("pars.orch.resume.collect_fingerprint", return_value=current_fp):
            result = runner.invoke(self._get_cli(), ["sft", "resume", "--run-id", run_id, "--yes"])

        assert result.exit_code == 2
        assert "cross-machine" in result.output.lower() or "mismatch" in result.output.lower()
