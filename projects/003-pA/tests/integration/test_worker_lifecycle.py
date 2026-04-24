"""tests.integration.test_worker_lifecycle — Worker 子进程生命周期集成测试。

结论:
  使用 mock claude 二进制(bash 脚本)替代真正的 claude -p,
  验证完整的 worktree 创建 → env 隔离 → 进程启动 → 事件流 → 清理生命周期。

测试矩阵(>=5):
  1. should complete run and yield events when mock claude exits zero
  2. should not contain ANTHROPIC_API_KEY in worker env
  3. should create and remove worktree during worker run
  4. should handle SIGINT termination within timeout
  5. should clean up worktree on error when mock claude exits nonzero
  6. should parse all event types from stream

关键设计:
  - 用 tmp git repo 作为 cwd(Worker.run() 需要在 git repo 内执行)
  - mock claude binary 写入 worktree_base 父目录的 bin/ 并前置到 PATH
  - RECALLKIT_ALLOW_UNSAFE_CHMOD=1 确保 ensure_readonly_claude_dir 使用 UNSAFE_CHMOD
  - 每个测试独立的 tmp_path 避免状态污染
"""

from __future__ import annotations

import json
import os
import signal
import stat
import subprocess
import threading
import time
from pathlib import Path
from collections.abc import Generator

import pytest

from pars.orch.stream_parser import ClaudeEvent, parse_stream
from pars.orch.worker import Worker, WorkerConfig
from pars.orch.worktree import WorktreeHandle, create_worktree, list_worktrees, remove_worktree
from pars.proxy import ProxyConfig

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def tmp_git_repo(tmp_path: Path) -> Generator[Path, None, None]:
    """创建带初始 commit 的临时 git 仓库,供 Worker 集成测试使用。"""
    repo = tmp_path / "repo"
    repo.mkdir()

    subprocess.run(["git", "init", "-b", "main"], cwd=str(repo), check=True, capture_output=True)
    subprocess.run(
        ["git", "config", "user.email", "test@example.com"],
        cwd=str(repo), check=True, capture_output=True,
    )
    subprocess.run(
        ["git", "config", "user.name", "Test"],
        cwd=str(repo), check=True, capture_output=True,
    )

    readme = repo / "README.md"
    readme.write_text("# test\n", encoding="utf-8")
    subprocess.run(["git", "add", "."], cwd=str(repo), check=True, capture_output=True)
    subprocess.run(
        ["git", "commit", "-m", "init"],
        cwd=str(repo), check=True, capture_output=True,
    )
    yield repo


@pytest.fixture()
def mock_claude_bin(tmp_path: Path) -> Generator[Path, None, None]:
    """创建 mock claude 二进制目录。

    返回 bin/ 目录路径,调用方把该目录插到 PATH 前面。
    """
    bin_dir = tmp_path / "mock_bin"
    bin_dir.mkdir()
    yield bin_dir


def _write_mock_claude(bin_dir: Path, script_body: str) -> Path:
    """在 bin_dir 写入名为 'claude' 的 bash 脚本。"""
    claude = bin_dir / "claude"
    # 脚本前缀:输出 ndjson 事件后退出
    script = f"#!/usr/bin/env bash\n{script_body}\n"
    claude.write_text(script, encoding="utf-8")
    claude.chmod(claude.stat().st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)
    return claude


@pytest.fixture()
def worker_claude_template(tmp_path: Path) -> Path:
    """创建最小化的 worker_claude_dir 模板,供 ensure_readonly_claude_dir 使用。"""
    template = tmp_path / "worker_claude_dir"
    template.mkdir()
    (template / "settings.json").write_text('{"version":"0.1"}', encoding="utf-8")
    (template / "CLAUDE.md").write_text("# Worker", encoding="utf-8")
    return template


# ---------------------------------------------------------------------------
# 辅助函数
# ---------------------------------------------------------------------------


def _run_worker_collect(
    worker: Worker,
    timeout: float = 10.0,
) -> list[ClaudeEvent]:
    """在子线程中跑 Worker.run(),收集所有事件,防止测试主线程永久阻塞。

    Args:
        worker:  配置好的 Worker
        timeout: 最长等待时间(秒)

    Returns:
        收集到的 ClaudeEvent 列表

    Raises:
        TimeoutError: worker 超过 timeout 未完成
    """
    events: list[ClaudeEvent] = []
    exc_holder: list[BaseException] = []

    def _target() -> None:
        try:
            for evt in worker.run():
                events.append(evt)
        except Exception as exc:  # noqa: BLE001
            exc_holder.append(exc)

    t = threading.Thread(target=_target, daemon=True)
    t.start()
    t.join(timeout=timeout)

    if t.is_alive():
        # 超时 → 终止 worker,等待线程结束
        try:
            worker.terminate(timeout=5)
        except Exception:  # noqa: BLE001, S110
            pass  # 超时时已尽力终止,忽略清理异常
        t.join(timeout=5)
        raise TimeoutError(f"Worker 未在 {timeout}s 内完成")

    if exc_holder:
        raise exc_holder[0]  # type: ignore[misc]

    return events


# ---------------------------------------------------------------------------
# Test 1: mock claude 正常退出 → 收到事件
# ---------------------------------------------------------------------------


@pytest.mark.integration
def test_should_complete_run_and_yield_events_when_mock_claude_exits_zero(
    tmp_git_repo: Path,
    mock_claude_bin: Path,
    worker_claude_template: Path,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """should complete run and yield events when mock claude exits zero."""
    monkeypatch.chdir(tmp_git_repo)
    monkeypatch.setenv("RECALLKIT_ALLOW_UNSAFE_CHMOD", "1")
    # 将 mock claude 插入 PATH 最前面
    monkeypatch.setenv("PATH", f"{mock_claude_bin}:{os.environ.get('PATH', '')}")

    # mock claude:输出 2 个 NDJSON 事件后 exit 0
    assistant_event = json.dumps({
        "type": "assistant",
        "message": {
            "id": "msg_001",
            "role": "assistant",
            "content": [{"type": "text", "text": "done"}],
            "usage": {"input_tokens": 10, "output_tokens": 5},
        },
    })
    result_event = json.dumps({"type": "result", "subtype": "success", "cost_usd": 0.0})
    _write_mock_claude(
        mock_claude_bin,
        f'echo \'{assistant_event}\'\necho \'{result_event}\'\nexit 0',
    )

    worktree_base = tmp_path / "worktrees"
    worktree_base.mkdir()

    config = WorkerConfig(
        run_id="integration-001",
        workflow_prompt="test prompt",
        worktree_base=worktree_base,
        claude_template=worker_claude_template,
        proxy_config=None,  # 无代理(mock claude 不需要)
    )

    worker = Worker(config)

    # 无代理模式:patch start_proxy / stop_proxy
    from unittest.mock import MagicMock, patch
    mock_proxy = MagicMock()
    mock_proxy.port = 9999

    with (
        patch("pars.orch.worker.start_proxy", return_value=mock_proxy),
        patch("pars.orch.worker.stop_proxy"),
    ):
        events = _run_worker_collect(worker, timeout=15.0)

    # 必须收到至少 2 个事件
    assert len(events) >= 2
    event_types = {e.event_type for e in events}
    assert "assistant" in event_types
    assert "result" in event_types

    # 验证 assistant 事件的 usage
    assistant_events = [e for e in events if e.event_type == "assistant"]
    assert len(assistant_events) == 1
    usage = assistant_events[0].usage
    assert usage is not None
    assert usage["input_tokens"] == 10
    assert usage["output_tokens"] == 5


# ---------------------------------------------------------------------------
# Test 2: worker env 不含 ANTHROPIC_API_KEY
# ---------------------------------------------------------------------------


@pytest.mark.integration
def test_should_not_contain_api_key_in_worker_env(
    tmp_git_repo: Path,
    mock_claude_bin: Path,
    worker_claude_template: Path,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """should not contain ANTHROPIC_API_KEY in worker env."""
    monkeypatch.chdir(tmp_git_repo)
    monkeypatch.setenv("RECALLKIT_ALLOW_UNSAFE_CHMOD", "1")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant-test-secret-key")  # 设置后应被剥离
    monkeypatch.setenv("PATH", f"{mock_claude_bin}:{os.environ.get('PATH', '')}")

    # mock claude:把 env 中的 ANTHROPIC_API_KEY dump 到 stdout(若存在则输出特殊标记)
    script = (
        'if [ -n "$ANTHROPIC_API_KEY" ]; then\n'
        '    echo \'{"type":"error","error":"KEY_LEAK"}\'\n'
        'else\n'
        '    echo \'{"type":"result","subtype":"success","cost_usd":0}\'\n'
        'fi\n'
        'exit 0'
    )
    _write_mock_claude(mock_claude_bin, script)

    worktree_base = tmp_path / "worktrees"
    worktree_base.mkdir()

    config = WorkerConfig(
        run_id="integration-002",
        workflow_prompt="test prompt",
        worktree_base=worktree_base,
        claude_template=worker_claude_template,
    )

    worker = Worker(config)

    from unittest.mock import MagicMock, patch
    mock_proxy = MagicMock()
    mock_proxy.port = 9998

    with (
        patch("pars.orch.worker.start_proxy", return_value=mock_proxy),
        patch("pars.orch.worker.stop_proxy"),
    ):
        events = _run_worker_collect(worker, timeout=15.0)

    # 确认没有 KEY_LEAK 事件
    error_events = [e for e in events if e.event_type == "error"]
    for e in error_events:
        assert e.raw.get("error") != "KEY_LEAK", (
            "ANTHROPIC_API_KEY 泄漏到 worker env!"
        )

    # 确认有 result 事件
    result_events = [e for e in events if e.event_type == "result"]
    assert len(result_events) >= 1, "应有 success result 事件"


# ---------------------------------------------------------------------------
# Test 3: Worker.run() 结束后 worktree 被清理
# ---------------------------------------------------------------------------


@pytest.mark.integration
def test_should_remove_worktree_after_worker_run_completes(
    tmp_git_repo: Path,
    mock_claude_bin: Path,
    worker_claude_template: Path,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """should create and remove worktree during worker run."""
    monkeypatch.chdir(tmp_git_repo)
    monkeypatch.setenv("RECALLKIT_ALLOW_UNSAFE_CHMOD", "1")
    monkeypatch.setenv("PATH", f"{mock_claude_bin}:{os.environ.get('PATH', '')}")

    result_event = json.dumps({"type": "result", "subtype": "success", "cost_usd": 0})
    _write_mock_claude(mock_claude_bin, f"echo '{result_event}'\nexit 0")

    worktree_base = tmp_path / "worktrees"
    worktree_base.mkdir()

    run_id = "integration-003"
    config = WorkerConfig(
        run_id=run_id,
        workflow_prompt="test",
        worktree_base=worktree_base,
        claude_template=worker_claude_template,
    )

    expected_worktree_path = worktree_base / run_id

    worker = Worker(config)

    from unittest.mock import MagicMock, patch
    mock_proxy = MagicMock()
    mock_proxy.port = 9997

    with (
        patch("pars.orch.worker.start_proxy", return_value=mock_proxy),
        patch("pars.orch.worker.stop_proxy"),
    ):
        # 在 run 期间 worktree 应存在;run 结束后应已清理
        worktree_existed_during_run: list[bool] = []

        original_run = worker.run

        def _monitored_run():
            for evt in original_run():
                # run 过程中 worktree 目录应存在
                worktree_existed_during_run.append(expected_worktree_path.is_dir())
                yield evt

        worker.run = _monitored_run  # type: ignore[method-assign]
        _run_worker_collect(worker, timeout=15.0)

    # run 后 worktree 目录应已删除
    assert not expected_worktree_path.exists(), (
        f"Worker 结束后 worktree 应被删除: {expected_worktree_path}"
    )

    # run 期间至少有一次 worktree 存在
    assert any(worktree_existed_during_run), "run 期间 worktree 目录应存在"


# ---------------------------------------------------------------------------
# Test 4: Worker.terminate() SIGINT → 在超时内退出
# ---------------------------------------------------------------------------


@pytest.mark.integration
def test_should_handle_sigint_termination_within_timeout(
    tmp_git_repo: Path,
    mock_claude_bin: Path,
    worker_claude_template: Path,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """should handle SIGINT termination within timeout."""
    monkeypatch.chdir(tmp_git_repo)
    monkeypatch.setenv("RECALLKIT_ALLOW_UNSAFE_CHMOD", "1")
    monkeypatch.setenv("PATH", f"{mock_claude_bin}:{os.environ.get('PATH', '')}")

    # mock claude:持续 sleep,直到被 SIGINT 停止
    # exec sleep 使 sleep 成为主进程,直接响应 SIGKILL
    _write_mock_claude(mock_claude_bin, "exec sleep 60")

    worktree_base = tmp_path / "worktrees"
    worktree_base.mkdir()

    config = WorkerConfig(
        run_id="integration-004",
        workflow_prompt="test",
        worktree_base=worktree_base,
        claude_template=worker_claude_template,
    )

    worker = Worker(config)
    start = time.monotonic()

    from unittest.mock import MagicMock, patch
    mock_proxy = MagicMock()
    mock_proxy.port = 9996

    finish_event = threading.Event()

    def _run_in_thread() -> None:
        with (
            patch("pars.orch.worker.start_proxy", return_value=mock_proxy),
            patch("pars.orch.worker.stop_proxy"),
        ):
            try:
                for _evt in worker.run():
                    pass
            except Exception:  # noqa: BLE001, S110
                pass  # worker 被 terminate 时可能抛异常,已预期
        finish_event.set()

    t = threading.Thread(target=_run_in_thread, daemon=True)
    t.start()

    # 等一小段时间让 worker 启动
    time.sleep(0.5)

    # 发送 SIGINT(3s 内若没响应则 SIGKILL)
    worker.terminate(timeout=3)

    # 等待线程完成(3s SIGKILL 宽限 + 5s cleanup → 最多 10s)
    finished = finish_event.wait(timeout=20)
    elapsed = time.monotonic() - start

    assert finished, f"Worker 未在 20s 内响应 SIGINT/SIGKILL(已过 {elapsed:.1f}s)"
    # 整体时间远小于 60s(sleep mock claude 的时长)
    assert elapsed < 30.0, f"Worker terminate 花了太久: {elapsed:.1f}s"


# ---------------------------------------------------------------------------
# Test 5: mock claude 非零退出 → worktree 仍被清理
# ---------------------------------------------------------------------------


@pytest.mark.integration
def test_should_cleanup_worktree_on_nonzero_exit(
    tmp_git_repo: Path,
    mock_claude_bin: Path,
    worker_claude_template: Path,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """should clean up worktree on error when mock claude exits nonzero."""
    monkeypatch.chdir(tmp_git_repo)
    monkeypatch.setenv("RECALLKIT_ALLOW_UNSAFE_CHMOD", "1")
    monkeypatch.setenv("PATH", f"{mock_claude_bin}:{os.environ.get('PATH', '')}")

    # mock claude:输出一个 error 事件后 exit 1
    error_event = json.dumps({"type": "error", "error": {"type": "api_error", "message": "fail"}})
    _write_mock_claude(mock_claude_bin, f"echo '{error_event}'\nexit 1")

    worktree_base = tmp_path / "worktrees"
    worktree_base.mkdir()

    run_id = "integration-005"
    config = WorkerConfig(
        run_id=run_id,
        workflow_prompt="test",
        worktree_base=worktree_base,
        claude_template=worker_claude_template,
    )

    expected_worktree_path = worktree_base / run_id
    worker = Worker(config)

    from unittest.mock import MagicMock, patch
    mock_proxy = MagicMock()
    mock_proxy.port = 9995

    with (
        patch("pars.orch.worker.start_proxy", return_value=mock_proxy),
        patch("pars.orch.worker.stop_proxy"),
    ):
        events = _run_worker_collect(worker, timeout=15.0)

    # worktree 即使在 exit 1 后也应被清理
    assert not expected_worktree_path.exists(), (
        f"非零退出后 worktree 应被清理: {expected_worktree_path}"
    )

    # 应该收到 error 事件
    error_events = [e for e in events if e.event_type == "error"]
    assert len(error_events) >= 1, "应收到 error 事件"
    # error_info property 应有效
    assert error_events[0].error_info is not None


# ---------------------------------------------------------------------------
# Test 6: parse_stream 能正确分类所有事件类型
# ---------------------------------------------------------------------------


@pytest.mark.integration
def test_should_parse_all_event_types_from_stream() -> None:
    """should parse all event types from stream."""
    lines = [
        json.dumps({"type": "system", "subtype": "init", "session_id": "s001"}),
        json.dumps({"type": "assistant", "message": {
            "id": "m001", "role": "assistant",
            "content": [{"type": "text", "text": "Hello"}],
            "usage": {"input_tokens": 5, "output_tokens": 3},
        }}),
        json.dumps({"type": "tool_use", "id": "t001", "name": "Bash", "input": {"command": "ls"}}),
        json.dumps({"type": "tool_result", "tool_use_id": "t001", "content": "file.txt"}),
        json.dumps({"type": "result", "subtype": "success", "cost_usd": 0.001}),
        # 损坏行 → 应跳过
        "NOT_JSON_AT_ALL",
        "",  # 空行 → 应跳过
        # 缺少 type 字段 → 应跳过
        json.dumps({"no_type": "here"}),
    ]

    events = list(parse_stream(iter(lines)))

    # 5 个合法事件
    assert len(events) == 5

    types = [e.event_type for e in events]
    assert types == ["system", "assistant", "tool_use", "tool_result", "result"]

    # assistant 事件 usage
    assistant_evt = next(e for e in events if e.event_type == "assistant")
    assert assistant_evt.usage == {"input_tokens": 5, "output_tokens": 3}

    # tool_use 事件 tool_name
    tool_evt = next(e for e in events if e.event_type == "tool_use")
    assert tool_evt.tool_name == "Bash"

    # result 事件 is_success_result
    result_evt = next(e for e in events if e.event_type == "result")
    assert result_evt.is_success_result is True
