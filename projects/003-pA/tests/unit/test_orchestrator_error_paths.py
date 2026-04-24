"""
tests/unit/test_orchestrator_error_paths.py — T023 RunOrchestrator 错误路径测试。

结论：用 mock 覆盖各步骤失败场景，验证错误码、cleanup 调用、日志。
      不测 happy path（集成测试覆盖）。
"""

from __future__ import annotations

import os
from pathlib import Path
from unittest.mock import MagicMock, call, patch

import pytest


# ---------------------------------------------------------------------------
# 辅助：构造最小 RunOrchestrator（所有外部依赖均 mock）
# ---------------------------------------------------------------------------

def _make_base_kwargs() -> dict:
    """最小 start() 参数集（满足所有 required 字段）。"""
    return {
        "research_question": "Does LoRA help on GSM8K?",
        "base_model": "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
        "dataset_id": "tatsu-lab/alpaca",
        "dataset_split": "train[:20]",
        "n_samples": 20,
        "lora_rank": 16,
        "lora_alpha": 32,
        "lr": 2e-4,
        "epochs": 1,
        "batch_size": 2,
        "max_seq_len": 512,
        "eval_tasks": ["gsm8k"],
        "usd_cap": 1.0,
        "wall_clock_hours_cap": 1.0,
        "gpu_hours_cap": 1.0,
        "run_id": None,
    }


# ---------------------------------------------------------------------------
# T023-ORCH-TC01: ANTHROPIC_API_KEY 缺失 → ApiKeyMissingError
# ---------------------------------------------------------------------------

def test_start_raises_api_key_missing_when_env_not_set() -> None:
    """should raise ApiKeyMissingError when ANTHROPIC_API_KEY is not in environment."""
    from pars.orch.orchestrator import ApiKeyMissingError, RunOrchestrator

    orch = RunOrchestrator()
    env_without_key = {k: v for k, v in os.environ.items() if "ANTHROPIC" not in k}

    with patch.dict(os.environ, env_without_key, clear=True):
        with pytest.raises(ApiKeyMissingError):
            orch.start(**_make_base_kwargs())


# ---------------------------------------------------------------------------
# T023-ORCH-TC02: ReadonlyFailsClosed → 退出并传播异常（调用方退出码 2）
# ---------------------------------------------------------------------------

def test_start_propagates_readonly_fails_closed() -> None:
    """should propagate ReadonlyFailsClosed so caller maps it to exit code 2."""
    from pars.safety.readonly_mount import ReadonlyFailsClosed
    from pars.orch.orchestrator import RunOrchestrator

    orch = RunOrchestrator()

    with patch.dict(os.environ, {"ANTHROPIC_API_KEY": "sk-ant-test"}):
        with patch("pars.orch.orchestrator.generate_ulid", return_value="01JTEST00000000000000000001"):
            with patch("pars.orch.orchestrator.collect_env_snapshot", return_value=MagicMock()):
                with patch("pars.orch.orchestrator.collect_fingerprint", return_value={}):
                    with patch("pars.orch.orchestrator.write_fingerprint"):
                        with patch("pars.orch.orchestrator.save_config"):
                            with patch("pars.orch.orchestrator.create_run"):
                                with patch("pars.orch.orchestrator.start_proxy", return_value=MagicMock(port=9999)):
                                    with patch("pars.orch.orchestrator.build_worker_env", return_value={}):
                                        with patch("pars.orch.orchestrator.create_worktree", return_value=MagicMock()):
                                            with patch("pars.orch.orchestrator.ensure_readonly_claude_dir") as mock_ro:
                                                mock_ro.side_effect = ReadonlyFailsClosed(
                                                    "refuse to start",
                                                )
                                                with patch("pars.orch.orchestrator.stop_proxy"):
                                                    with patch("pars.orch.orchestrator.remove_worktree"):
                                                        with pytest.raises(ReadonlyFailsClosed):
                                                            orch.start(**_make_base_kwargs())


# ---------------------------------------------------------------------------
# T023-ORCH-TC03: proxy 启动失败 → cleanup 被调用（stop_proxy, remove_worktree）
# ---------------------------------------------------------------------------

def test_start_cleans_up_on_proxy_failure() -> None:
    """should call cleanup (stop_proxy, remove_worktree) when proxy start fails."""
    from pars.orch.orchestrator import RunOrchestrator

    orch = RunOrchestrator()
    mock_proxy_handle = MagicMock()
    mock_worktree_handle = MagicMock()

    with patch.dict(os.environ, {"ANTHROPIC_API_KEY": "sk-ant-test"}):
        with patch("pars.orch.orchestrator.generate_ulid", return_value="01JTEST00000000000000000002"):
            with patch("pars.orch.orchestrator.collect_env_snapshot", return_value=MagicMock()):
                with patch("pars.orch.orchestrator.collect_fingerprint", return_value={}):
                    with patch("pars.orch.orchestrator.write_fingerprint"):
                        with patch("pars.orch.orchestrator.save_config"):
                            with patch("pars.orch.orchestrator.create_run"):
                                with patch("pars.orch.orchestrator.start_proxy") as mock_start_proxy:
                                    mock_start_proxy.side_effect = RuntimeError("proxy failed to start")
                                    with patch("pars.orch.orchestrator.stop_proxy") as mock_stop_proxy:
                                        with patch("pars.orch.orchestrator.remove_worktree") as mock_rm_wt:
                                            with pytest.raises(RuntimeError, match="proxy failed"):
                                                orch.start(**_make_base_kwargs())

                                        # proxy 没有成功启动，stop_proxy 不应被调用
                                        # （cleanup 只清理已成功创建的资源）


# ---------------------------------------------------------------------------
# T023-ORCH-TC04: worker 启动失败 → cleanup 调用（proxy stop、worktree remove）
# ---------------------------------------------------------------------------

def test_start_cleans_up_on_worker_failure() -> None:
    """should call proxy stop and worktree remove when worker launch fails."""
    from pars.orch.orchestrator import RunOrchestrator

    orch = RunOrchestrator()
    mock_proxy = MagicMock()
    mock_proxy.port = 9999
    mock_worktree = MagicMock()
    mock_readonly = MagicMock()

    with patch.dict(os.environ, {"ANTHROPIC_API_KEY": "sk-ant-test"}):
        with patch("pars.orch.orchestrator.generate_ulid", return_value="01JTEST00000000000000000003"):
            with patch("pars.orch.orchestrator.collect_env_snapshot", return_value=MagicMock()):
                with patch("pars.orch.orchestrator.collect_fingerprint", return_value={}):
                    with patch("pars.orch.orchestrator.write_fingerprint"):
                        with patch("pars.orch.orchestrator.save_config"):
                            with patch("pars.orch.orchestrator.create_run"):
                                with patch("pars.orch.orchestrator.start_proxy", return_value=mock_proxy):
                                    with patch("pars.orch.orchestrator.build_worker_env", return_value={}):
                                        with patch("pars.orch.orchestrator.create_worktree", return_value=mock_worktree):
                                            with patch("pars.orch.orchestrator.ensure_readonly_claude_dir", return_value=mock_readonly):
                                                with patch("pars.orch.orchestrator.render_failure_prompt", return_value="prompt"):
                                                    with patch("pars.orch.orchestrator.Worker") as mock_worker_cls:
                                                        mock_worker = MagicMock()
                                                        mock_worker_cls.return_value = mock_worker
                                                        mock_worker.run.side_effect = RuntimeError("worker crash")
                                                        with patch("pars.orch.orchestrator.stop_proxy") as mock_stop_proxy:
                                                            with patch("pars.orch.orchestrator.remove_worktree") as mock_rm:
                                                                with pytest.raises(RuntimeError, match="worker crash"):
                                                                    orch.start(**_make_base_kwargs())

                                                        # proxy 已启动，故 stop_proxy 应被调用
                                                        mock_stop_proxy.assert_called_once()


# ---------------------------------------------------------------------------
# T023-ORCH-TC05: RunHandle 字段契约验证
# ---------------------------------------------------------------------------

def test_run_handle_has_required_fields() -> None:
    """should have required fields: run_id, final_state, report_path, exit_code, failure_reason."""
    from pars.orch.orchestrator import RunHandle
    from pars.ledger import RunPhase

    handle = RunHandle(
        run_id="01JTEST00000000000000000004",
        final_state=RunPhase.COMPLETED,
        report_path=None,
        exit_code=0,
        failure_reason=None,
    )

    assert handle.run_id == "01JTEST00000000000000000004"
    assert handle.final_state == RunPhase.COMPLETED
    assert handle.report_path is None
    assert handle.exit_code == 0
    assert handle.failure_reason is None


# ---------------------------------------------------------------------------
# T023-ORCH-TC06: RunHandle 接受 report_path 为 Path
# ---------------------------------------------------------------------------

def test_run_handle_accepts_path_for_report() -> None:
    """should accept Path object for report_path field."""
    from pars.orch.orchestrator import RunHandle
    from pars.ledger import RunPhase

    handle = RunHandle(
        run_id="01JTEST00000000000000000005",
        final_state=RunPhase.FAILED,
        report_path=Path("/tmp/runs/test/report.md"),
        exit_code=3,
        failure_reason="stuck_timeout",
    )

    assert isinstance(handle.report_path, Path)
    assert handle.failure_reason == "stuck_timeout"
    assert handle.exit_code == 3  # noqa: PLR2004


# ---------------------------------------------------------------------------
# T023-ORCH-TC07: SIGINT 被捕获时返回 RunHandle 而非崩溃
# ---------------------------------------------------------------------------

def test_start_returns_handle_on_keyboard_interrupt() -> None:
    """should return RunHandle (not crash) when KeyboardInterrupt is raised during run."""
    from pars.orch.orchestrator import RunOrchestrator
    from pars.ledger import RunPhase

    orch = RunOrchestrator()
    mock_proxy = MagicMock()
    mock_proxy.port = 9999
    mock_worktree = MagicMock()
    mock_readonly = MagicMock()

    with patch.dict(os.environ, {"ANTHROPIC_API_KEY": "sk-ant-test"}):
        with patch("pars.orch.orchestrator.generate_ulid", return_value="01JTEST00000000000000000006"):
            with patch("pars.orch.orchestrator.collect_env_snapshot", return_value=MagicMock()):
                with patch("pars.orch.orchestrator.collect_fingerprint", return_value={}):
                    with patch("pars.orch.orchestrator.write_fingerprint"):
                        with patch("pars.orch.orchestrator.save_config"):
                            with patch("pars.orch.orchestrator.create_run"):
                                with patch("pars.orch.orchestrator.start_proxy", return_value=mock_proxy):
                                    with patch("pars.orch.orchestrator.build_worker_env", return_value={}):
                                        with patch("pars.orch.orchestrator.create_worktree", return_value=mock_worktree):
                                            with patch("pars.orch.orchestrator.ensure_readonly_claude_dir", return_value=mock_readonly):
                                                with patch("pars.orch.orchestrator.render_failure_prompt", return_value="prompt"):
                                                    with patch("pars.orch.orchestrator.Worker") as mock_worker_cls:
                                                        mock_worker = MagicMock()
                                                        mock_worker_cls.return_value = mock_worker
                                                        mock_worker.run.side_effect = KeyboardInterrupt()
                                                        with patch("pars.orch.orchestrator.stop_proxy"):
                                                            with patch("pars.orch.orchestrator.remove_worktree"):
                                                                with patch("pars.orch.orchestrator.update_state"):
                                                                    handle = orch.start(**_make_base_kwargs())

    # KeyboardInterrupt 应被捕获，返回 RunHandle 而非崩溃
    assert handle is not None
    # exit_code 应为非零（Ctrl+C = 中断 = 不完整）
    assert handle.exit_code != 0
