"""
E2E app factory — T009
结论: 提供 make_e2e_app() 作为 uvicorn --factory 入口，
      构建含 decisions router 的 FastAPI app，注入缓存感知的 mock services。
细节:
  - 仅在 DECISION_LEDGER_E2E=true 时使用（subprocess E2E 测试专用）
  - 读取 DECISION_LEDGER_DB_URL / DECISION_LEDGER_LLM_CACHE_DIR env vars
  - 注入 E2ECacheMockAssembler（读 LLM cache 文件，无真实 API 调用）
  - 注入 E2EFastRebuttalMock（≤1s mock rebuttal，无真实 API 调用）
  - 通过 set_recorder() 注入 DecisionRecorder 到 decisions router
"""

from __future__ import annotations

import asyncio
import os
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from fastapi import FastAPI

# ── 常量 ─────────────────────────────────────────────────────────────────────

_DEFAULT_CACHE_DIR = Path.home() / "decision_ledger" / "llm_cache"
_DEFAULT_DB_PATH = Path.home() / "decision_ledger" / "db.sqlite"

# ConflictReport assembler 使用的 cache 参数（必须与 seed_state.py 一致）
_CONFLICT_TEMPLATE_VERSION = "conflict_assembler_v1"
_CONFLICT_MODEL = "claude-sonnet-4-6"
_ADVISOR_WEEK_ID = "advisor-2026W17"


# ── E2E Mock 服务 ─────────────────────────────────────────────────────────────


class E2ECacheMockAssembler:
    """结论: 从 LLM cache 文件读取 ConflictReport，绕过真实 API（E2E 常态命中路径）。

    细节:
      - advisor_week_id 硬编码为 seed_state.ADVISOR_WEEK_ID
      - 命中 cache → ≤1s；miss → raise RuntimeError（测试 seed 必须预热）
      - ticker 对应 cache 键由 LLMCache._make_key 算法生成
    """

    def __init__(self, cache_dir: Path) -> None:
        from decision_ledger.llm.cache import LLMCache

        self._cache = LLMCache(cache_dir=cache_dir)

    async def assemble(
        self,
        ticker: str,
        env_snapshot: Any,
    ) -> Any:
        """结论: 从 cache 读取 mock ConflictReport，命中返回，miss 抛 RuntimeError。"""
        from decision_ledger.domain.conflict_report import ConflictReport
        from decision_ledger.domain.strategy_signal import Direction, StrategySignal

        # 尝试命中 LLM cache
        cached = self._cache.get(
            advisor_week_id=_ADVISOR_WEEK_ID,
            ticker=ticker,
            prompt_template_version=_CONFLICT_TEMPLATE_VERSION,
            model=_CONFLICT_MODEL,
        )

        if cached is None:
            raise RuntimeError(
                f"E2E cache miss: ticker={ticker!r} 未被预热。"
                "请确保 seed_llm_cache() 已运行，并使用 WATCHLIST_TICKERS 中的 ticker。"
            )

        # 构造 signals
        signals_data = cached.get("signals", [])
        signals = [
            StrategySignal(
                source_id=s["source_id"],
                ticker=s["ticker"],
                direction=Direction(s["direction"]),
                confidence=float(s["confidence"]),
                rationale_plain=str(s["rationale_plain"]),
                inputs_used=s.get("inputs_used", {}),
            )
            for s in signals_data
        ]

        return ConflictReport(
            signals=signals,
            divergence_root_cause=str(
                cached.get("divergence_root_cause", "E2E mock 分歧")
            ),
            has_divergence=bool(cached.get("has_divergence", True)),
            rendered_order_seed=int(cached.get("rendered_order_seed", 0)),
        )


class E2EFastRebuttalMock:
    """结论: 固定返回一句话 mock rebuttal（≤100ms），无真实 API 调用（E2E 专用）。

    细节:
      - D21: rebuttal fast-path ≤ 3s（mock 直接返回，远快于要求）
      - rebuttal_text 必须 ≤ 80 字（Rebuttal validator 要求）
      - 不可缓存（D21/R3），每次 draft 独立生成
    """

    async def generate(
        self,
        ticker: str,
        env_snapshot: Any,
    ) -> Any:
        """结论: 立即返回 mock rebuttal（≤100ms）。"""
        from decision_ledger.domain.rebuttal import Rebuttal

        # 截断到 80 字保证 validator 通过
        text = f"考虑反方: {ticker} 短期超买，技术面存在回调风险，谨慎追高。"
        if len(text) > 80:
            text = text[:79]  # 截断，保留 ≤80 字

        return Rebuttal(
            rebuttal_text=text,
            invoked_at=datetime.now(tz=UTC).isoformat(),
        )


# ── DB pool + repos 初始化 ────────────────────────────────────────────────────


async def _initialize_pool_and_repos(db_path: Path) -> dict[str, Any]:
    """结论: 初始化 AsyncConnectionPool + 所有 Repository 实例。

    细节:
      - 使用 DECISION_LEDGER_DB_URL 指定的 SQLite 文件（由 conftest.py 设置）
      - 已由 alembic upgrade head 迁移完毕
    """
    from decision_ledger.repository.base import AsyncConnectionPool
    from decision_ledger.repository.conflict_repo import ConflictRepository
    from decision_ledger.repository.decision_repo import DecisionRepository
    from decision_ledger.repository.rebuttal_repo import RebuttalRepository
    from decision_ledger.services.decision_recorder import (
        DecisionDraftRepository,
    )

    pool = AsyncConnectionPool(db_path=db_path)
    await pool.initialize()

    draft_repo = DecisionDraftRepository(pool)
    conflict_repo = ConflictRepository(pool)
    rebuttal_repo = RebuttalRepository(pool)
    decision_repo = DecisionRepository(pool)

    return {
        "pool": pool,
        "draft_repo": draft_repo,
        "conflict_repo": conflict_repo,
        "rebuttal_repo": rebuttal_repo,
        "decision_repo": decision_repo,
    }


# ── App factory ───────────────────────────────────────────────────────────────


def make_e2e_app() -> FastAPI:
    """结论: uvicorn --factory 入口，构建 E2E 测试用 FastAPI app。

    细节:
      - 读取 env vars 配置 DB + cache 路径
      - 注入 E2ECacheMockAssembler + E2EFastRebuttalMock
      - 通过 set_recorder() 注入 DecisionRecorder
      - 包含 decisions router（_make_standalone_app 不含）
    """
    from decision_ledger.services.decision_recorder import DecisionRecorder
    from decision_ledger.ui.app import create_app
    from decision_ledger.ui.router_decisions import router as decisions_router
    from decision_ledger.ui.router_decisions import set_recorder

    # 读取 env 配置
    db_url = os.environ.get("DECISION_LEDGER_DB_URL", "")
    if db_url.startswith("sqlite:///"):
        db_path = Path(db_url.removeprefix("sqlite:///"))
    else:
        db_path = _DEFAULT_DB_PATH

    cache_dir_str = os.environ.get("DECISION_LEDGER_LLM_CACHE_DIR", "")
    cache_dir = Path(cache_dir_str) if cache_dir_str else _DEFAULT_CACHE_DIR

    # 构建 mock services
    assembler = E2ECacheMockAssembler(cache_dir=cache_dir)
    devil = E2EFastRebuttalMock()

    # 初始化 repos（同步运行）
    repos = asyncio.run(_initialize_pool_and_repos(db_path))

    recorder = DecisionRecorder(
        assembler_service=assembler,
        devil_service=devil,
        draft_repo=repos["draft_repo"],
        conflict_repo=repos["conflict_repo"],
        rebuttal_repo=repos["rebuttal_repo"],
        decision_repo=repos["decision_repo"],
    )

    # 注入 recorder 到 decisions router
    set_recorder(recorder)

    # 构建 app + 包含 decisions router
    app = create_app()
    app.include_router(decisions_router)

    return app
