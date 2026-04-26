"""
E2E pytest fixtures — T009
结论: 提供 subprocess uvicorn 服务器 + alembic 迁移 + seed 数据 + LLM cache 预热，
      让 draft 阶段常态命中 cache (≤ 1s)。
细节:
  - e2e_server_url: scope=module，subprocess 启动 uvicorn（port 18000），
    先运行 alembic upgrade head，再 seed 数据库和 LLM cache，等待就绪后 yield base URL。
  - app_client_503: scope=function，in-process FastAPI AsyncClient，注入 slow mock recorder
    用于验证 503 timeout 行为（无需真实 browser）。
  - playwright 通过 pytest.importorskip 跳过保护（CI 未装 chromium 时跳过）。
"""

from __future__ import annotations

import asyncio
import os
import socket
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock

import pytest
import pytest_asyncio

# ── 常量 ─────────────────────────────────────────────────────────────────────

_SERVER_HOST = "127.0.0.1"
_SERVER_PORT = 18001  # 18000 被 T004 用，T009 用 18001 避免冲突
_SERVER_URL = f"http://{_SERVER_HOST}:{_SERVER_PORT}"
_PROJECT_DIR = Path(__file__).parents[2]  # projects/004-pB/

# ── e2e_server_url fixture ──────────────────────────────────────────────────


@pytest.fixture(scope="module")
def e2e_tmpdir() -> Any:
    """结论: module-scope 临时目录（subprocess 服务器生命周期内共用）。

    细节: 使用 tempfile.mkdtemp()，手动清理（TemporaryDirectory scope=module 不支持）。
    """
    import shutil

    d = Path(tempfile.mkdtemp(prefix="e2e_decision_ledger_"))
    yield d
    shutil.rmtree(d, ignore_errors=True)


@pytest.fixture(scope="module")
def e2e_db_path(e2e_tmpdir: Path) -> Path:
    """结论: E2E 测试用 SQLite 路径（在 tmpdir 内）。"""
    return e2e_tmpdir / "e2e_test.sqlite"


@pytest.fixture(scope="module")
def e2e_cache_dir(e2e_tmpdir: Path) -> Path:
    """结论: E2E 测试用 LLM cache 目录（tmpdir 内，隔离）。"""
    cache_dir = e2e_tmpdir / "llm_cache"
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir


@pytest.fixture(scope="module")
def e2e_server_url(e2e_db_path: Path, e2e_cache_dir: Path) -> Any:
    """结论: 启动真实 uvicorn subprocess 服务器，yield base URL，测试后 teardown。

    步骤:
      1. alembic upgrade head (DECISION_LEDGER_DB_URL 指向 tmpdir SQLite)
      2. seed_database (30 关注股 + advisor_report)
      3. seed_llm_cache (30 ticker conflict_report mock cache)
      4. 启动 uvicorn subprocess (DECISION_LEDGER_E2E=true 激活 decisions router)
      5. socket 轮询等待就绪 (最多 15s)
      6. yield _SERVER_URL
      7. teardown: proc.terminate()
    """
    db_url = f"sqlite:///{e2e_db_path}"

    env = {
        **os.environ,
        "ANTHROPIC_API_KEY": "test-e2e-key",
        "TELEGRAM_BOT_TOKEN": "test-e2e-token",
        "DECISION_LEDGER_TEST_MODE": "strict",
        "DECISION_LEDGER_DB_URL": db_url,
        "DECISION_LEDGER_LLM_CACHE_DIR": str(e2e_cache_dir),
        "DECISION_LEDGER_E2E": "true",  # 激活 decisions router (见 _make_e2e_app)
    }

    # 1. 运行 alembic upgrade head
    result = subprocess.run(  # noqa: S603
        [
            sys.executable,
            "-m",
            "alembic",
            "-c",
            str(_PROJECT_DIR / "alembic.ini"),
            "upgrade",
            "head",
        ],
        cwd=_PROJECT_DIR,
        env=env,
        capture_output=True,
        text=True,
        timeout=30,
    )
    if result.returncode != 0:
        pytest.fail(
            f"alembic upgrade head 失败:\n{result.stdout}\n{result.stderr}"
        )

    # 2. seed 数据库（在独立事件循环中执行）
    _run_seed_db(e2e_db_path)

    # 3. 预热 LLM cache
    _run_seed_cache(e2e_cache_dir)

    # 4. 启动 uvicorn subprocess
    cmd = [
        sys.executable,
        "-m",
        "uvicorn",
        "tests.e2e.e2e_app_factory:make_e2e_app",
        "--host",
        _SERVER_HOST,
        "--port",
        str(_SERVER_PORT),
        "--factory",
        "--log-level",
        "warning",
    ]
    proc = subprocess.Popen(  # noqa: S603
        cmd,
        cwd=_PROJECT_DIR,
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    # 5. 轮询等待就绪
    deadline = time.monotonic() + 15.0
    while time.monotonic() < deadline:
        try:
            with socket.create_connection((_SERVER_HOST, _SERVER_PORT), timeout=0.5):
                break
        except OSError:
            time.sleep(0.3)
    else:
        proc.terminate()
        pytest.fail(
            f"E2E server 在 15s 内未就绪 ({_SERVER_URL})"
        )

    yield _SERVER_URL

    # teardown
    proc.terminate()
    try:
        proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        proc.kill()


# ── in-process client fixture（503 超时测试用）─────────────────────────────


@pytest_asyncio.fixture
async def app_client_slow() -> Any:
    """结论: in-process httpx.AsyncClient，注入 6s 慢 mock recorder，验证 503 行为。

    细节:
      - 不启动 subprocess，用 AsyncClient(app=...) 直接测试路由层
      - slow_assembler.assemble() sleep 6s，超过 DecisionRecorder._TIMEOUT_SEC=5s
      - 用于 test_draft_timeout_returns_503
    """
    from httpx import ASGITransport, AsyncClient

    from decision_ledger.ui.app import create_app
    from decision_ledger.ui.router_decisions import router as decisions_router
    from decision_ledger.ui.router_decisions import set_recorder

    # 构建含 decisions router 的 in-process app
    app = create_app()
    app.include_router(decisions_router)

    # mock 慢 assembler（sleep 6s，必超 5s timeout）
    slow_assembler = AsyncMock()

    async def _slow_assemble(**_: Any) -> None:
        await asyncio.sleep(6.0)  # 超过 5s timeout

    slow_assembler.assemble = _slow_assemble

    # mock 正常 devil（不影响超时方向）
    fast_devil = AsyncMock()
    fast_devil.generate = AsyncMock(return_value=_make_mock_rebuttal())

    # 构建真实 DB pool + repos (in-memory SQLite)
    recorder = _build_in_process_recorder(slow_assembler, fast_devil)
    set_recorder(recorder)

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client

    # teardown: 清除 recorder 注入
    set_recorder(None)


# ── 内部辅助 ─────────────────────────────────────────────────────────────────


def _run_seed_db(db_path: Path) -> None:
    """结论: 在独立 asyncio 事件循环中执行 seed_database(module fixture 中无法 await)。"""
    from .fixtures.seed_state import seed_database

    asyncio.run(seed_database(db_path))


def _run_seed_cache(cache_dir: Path) -> None:
    """结论: 预热 LLM cache(同步,seed_state.seed_llm_cache 本身是同步函数)。"""
    from .fixtures.seed_state import seed_llm_cache

    seed_llm_cache(cache_dir)


def _make_mock_rebuttal() -> Any:
    """结论: 构造 mock Rebuttal 对象（in-process 503 测试用）。"""
    from datetime import UTC, datetime

    from decision_ledger.domain.rebuttal import Rebuttal

    return Rebuttal(
        rebuttal_text="考虑反方: 测试用快速反驳，不代表真实风险评估。",
        invoked_at=datetime.now(tz=UTC).isoformat(),
    )


def _build_in_process_recorder(
    assembler_service: Any,
    devil_service: Any,
) -> Any:
    """结论: 构建 in-process DecisionRecorder（使用 in-memory SQLite）。

    细节:
      - pool 用 in-memory SQLite（:memory:），scope=function
      - 需要先初始化 pool + 创建表（简化 schema，仅测试所需列）
      - 返回 DecisionRecorder，不写入真实 DB
    """
    import asyncio
    import tempfile
    from pathlib import Path

    from decision_ledger.repository.base import AsyncConnectionPool
    from decision_ledger.repository.conflict_repo import ConflictRepository
    from decision_ledger.repository.decision_repo import DecisionRepository
    from decision_ledger.repository.rebuttal_repo import RebuttalRepository
    from decision_ledger.services.decision_recorder import (
        DecisionDraftRepository,
        DecisionRecorder,
    )

    # 使用 tmpfile SQLite（in-memory 不支持 WAL）
    fd, tmp_path_str = tempfile.mkstemp(suffix=".sqlite")
    os.close(fd)
    tmp = Path(tmp_path_str)

    async def _setup() -> AsyncConnectionPool:
        pool = AsyncConnectionPool(db_path=str(tmp))
        await pool.initialize()
        # 创建最小 schema（跳过 alembic，直接建表）
        async with pool.write_connection() as conn:
            await conn.executescript("""
                CREATE TABLE IF NOT EXISTS decision_drafts (
                    draft_id TEXT PRIMARY KEY,
                    ticker TEXT NOT NULL,
                    intended_action TEXT NOT NULL,
                    draft_reason TEXT NOT NULL,
                    env_snapshot_json TEXT NOT NULL,
                    conflict_report_ref TEXT,
                    devils_rebuttal_ref TEXT,
                    status TEXT NOT NULL DEFAULT 'draft',
                    created_at TEXT NOT NULL,
                    committed_at TEXT,
                    abandoned_at TEXT
                );
                CREATE TABLE IF NOT EXISTS conflict_reports (
                    report_id TEXT PRIMARY KEY,
                    ticker TEXT NOT NULL,
                    signals_json TEXT NOT NULL,
                    divergence_root_cause TEXT NOT NULL,
                    has_divergence INTEGER NOT NULL DEFAULT 0,
                    rendered_order_seed INTEGER NOT NULL DEFAULT 0,
                    created_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS rebuttals (
                    rebuttal_id TEXT PRIMARY KEY,
                    draft_id TEXT,
                    rebuttal_text TEXT NOT NULL,
                    invoked_at TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS decisions (
                    trade_id TEXT PRIMARY KEY,
                    ticker TEXT NOT NULL,
                    action TEXT NOT NULL,
                    reason TEXT NOT NULL,
                    pre_commit_at TEXT NOT NULL,
                    env_snapshot_json TEXT NOT NULL,
                    conflict_report_ref TEXT,
                    devils_rebuttal_ref TEXT,
                    would_have_acted_without_agent INTEGER,
                    status TEXT NOT NULL DEFAULT 'committed'
                );
            """)
            await conn.commit()
        return pool

    pool = asyncio.run(_setup())

    draft_repo = DecisionDraftRepository(pool)
    conflict_repo = ConflictRepository(pool)
    rebuttal_repo = RebuttalRepository(pool)
    decision_repo = DecisionRepository(pool)

    return DecisionRecorder(
        assembler_service=assembler_service,
        devil_service=devil_service,
        draft_repo=draft_repo,
        conflict_repo=conflict_repo,
        rebuttal_repo=rebuttal_repo,
        decision_repo=decision_repo,
    )
