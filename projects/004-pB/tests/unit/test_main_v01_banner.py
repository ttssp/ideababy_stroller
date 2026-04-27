"""
test_main_v01_banner.py — F2-T020 followup A1
结论: lifespan 启动期 stderr BANNER 列出 v0.1 已知 stub
细节:
  - 默认输出 ConflictWorker / FailureAlert cron / TabMetrics / scheduler_jobs 4 条 stub
  - DECISION_LEDGER_SUPPRESS_V01_BANNER=1 时 stderr 干净
  - 当 conflict_worker wired 时, 该行从 banner 中消失
"""

from __future__ import annotations

import os
from unittest.mock import patch

import pytest


@pytest.fixture(autouse=True)
def reset_pause_pipeline() -> None:
    """每个测试前后清空 pause_pipeline wiring + counter, 防跨测试污染。"""
    from decision_ledger.monitor.pause_pipeline import reset_conflict_worker

    reset_conflict_worker()
    yield
    reset_conflict_worker()


def test_build_banner_lists_v01_stubs_when_unwired() -> None:
    """followup A1: 默认 (未 wire) 时 BANNER 应列出 4 条 v0.1 stub。"""
    from decision_ledger.main import _build_v01_banner

    banner = _build_v01_banner()
    assert banner is not None
    assert "v0.1 KNOWN LIMITATIONS" in banner
    assert "docs/known-issues-v0.1.md" in banner
    assert "ConflictWorker:" in banner
    assert "not wired" in banner
    assert "FailureAlert cron:" in banner
    assert "TabMetricsMiddleware:" in banner
    assert "register_scheduler_job:" in banner


def test_build_banner_omits_conflict_worker_when_wired() -> None:
    """followup A1: 当 conflict_worker wired 时, 该行从 banner 中消失。"""
    from decision_ledger.main import _build_v01_banner

    fake_status = {"conflict_worker": "wired"}
    with patch("decision_ledger.main.get_wiring_status", return_value=fake_status):
        banner = _build_v01_banner()

    assert banner is not None
    assert "ConflictWorker:" not in banner
    # 其他 v0.1 stub 仍在
    assert "FailureAlert cron:" in banner


def test_print_banner_writes_to_stderr(capsys: pytest.CaptureFixture[str]) -> None:
    """followup A1: _print_v01_banner 必须写到 stderr (不是 stdout)。"""
    from decision_ledger.main import _print_v01_banner

    _print_v01_banner()
    captured = capsys.readouterr()
    assert "v0.1 KNOWN LIMITATIONS" in captured.err
    assert "v0.1 KNOWN LIMITATIONS" not in captured.out, (
        "BANNER 必须写 stderr 而非 stdout, 避免污染 healthz/JSON 响应管道"
    )


def test_print_banner_suppressed_by_env(capsys: pytest.CaptureFixture[str]) -> None:
    """followup A1: DECISION_LEDGER_SUPPRESS_V01_BANNER=1 时 stderr 干净。"""
    from decision_ledger.main import _print_v01_banner

    with patch.dict(os.environ, {"DECISION_LEDGER_SUPPRESS_V01_BANNER": "1"}):
        _print_v01_banner()

    captured = capsys.readouterr()
    assert captured.err == ""
    assert captured.out == ""


def test_print_banner_not_suppressed_by_other_value(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """followup A1: 仅 '1' 抑制 BANNER, 其他值 (空 / '0' / 'false') 都不抑制。"""
    from decision_ledger.main import _print_v01_banner

    for value in ("", "0", "false", "no"):
        with patch.dict(
            os.environ, {"DECISION_LEDGER_SUPPRESS_V01_BANNER": value}, clear=False
        ):
            _print_v01_banner()
        captured = capsys.readouterr()
        assert "v0.1 KNOWN LIMITATIONS" in captured.err, (
            f"value={value!r} 不应抑制 banner, 仅 '1' 抑制"
        )


@pytest.mark.asyncio
async def test_lifespan_prints_banner(capsys: pytest.CaptureFixture[str]) -> None:
    """followup A1: lifespan 启动后 stderr 含 BANNER 文本。"""
    from decision_ledger.main import app

    # ensure not suppressed
    with patch.dict(os.environ, {"DECISION_LEDGER_SUPPRESS_V01_BANNER": ""}, clear=False):
        async with app.router.lifespan_context(app):
            pass

    captured = capsys.readouterr()
    assert "v0.1 KNOWN LIMITATIONS" in captured.err
    assert "ConflictWorker:" in captured.err
