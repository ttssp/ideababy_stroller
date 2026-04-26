"""
E2E seed state — T009
结论: 向 tmpdir SQLite 写入 30 个关注股 + 1 份持仓快照 + 1 份 advisor_report,
      并用 LLMCache.put() 预热对应 conflict_report cache (让 draft 阶段命中常态, ≤ 1s)
细节:
  - watchlist_stocks: 30 个 ticker (US 市场为主, 覆盖常用关注股命名)
  - advisor_report: week_id="2026-W17", source_id="columbia_advisor_v1"
  - advisor_week_id: seed 时和 EnvSnapshot.advisor_week_id 保持一致
  - mock LLM cache: 用 LLMCache.put() 直接写文件 (绕过真实 API)
  - 预热 key 对应 ConflictReportAssembler._TEMPLATE_VERSION + "claude-sonnet-4-6"
  - 不预热 Rebuttal (D21/R3: Rebuttal 不可缓存, 走 fast-path)
"""

from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

# ── 种子数据常量 ──────────────────────────────────────────────────────────────

ADVISOR_WEEK_ID = "advisor-2026W17"  # 与 EnvSnapshot.advisor_week_id 对应
SEED_ADVISOR_ID = "seed-advisor-001"
SEED_SOURCE_ID = "columbia_advisor_v1"
SEED_WEEK_ID = "2026-W17"

# 30 个关注股 (US 市场为主)
WATCHLIST_TICKERS = [
    "AAPL", "MSFT", "NVDA", "GOOGL", "AMZN",
    "META", "TSLA", "BRK.B", "JPM", "V",
    "UNH", "JNJ", "WMT", "PG", "MA",
    "HD", "ORCL", "BAC", "XOM", "CVX",
    "LLY", "PFE", "ABBV", "KO", "PEP",
    "MRK", "DIS", "NFLX", "INTC", "AMD",
]

# E2E 测试用的默认 ticker (预热其 cache)
DEFAULT_E2E_TICKER = "NVDA"

# ConflictReportAssembler cache 键参数 (对应 T010 实现)
CONFLICT_ASSEMBLER_TEMPLATE_VERSION = "conflict_assembler_v1"
CONFLICT_MODEL = "claude-sonnet-4-6"

# Rebuttal 模板版本 (T013 DevilAdvocateService fast-path)
DEVIL_TEMPLATE_VERSION = "devil_advocate_v1"
DEVIL_MODEL = "claude-sonnet-4-6"

# ── mock ConflictReport 数据 (写入 cache) ────────────────────────────────────

def _make_mock_conflict_report_cache(ticker: str) -> dict[str, Any]:
    """构造 mock ConflictReport 用于写入 LLM cache。

    结论: 符合 ConflictReport 域模型 + ConflictRepository.get() 期望的 JSON 结构。
    细节: 三路 signals (advisor/placeholder_model/agent_synthesis), has_divergence=True。
    """
    return {
        "signals": [
            {
                "source_id": "advisor",
                "ticker": ticker,
                "direction": "long",
                "confidence": 0.75,
                "rationale_plain": f"{ticker} 咨询师看多: 估值合理，技术面向好",
                "inputs_used": {
                    "advisor_week_id": ADVISOR_WEEK_ID,
                    "price_at": None,
                    "model_version": "columbia_v1",
                },
            },
            {
                "source_id": "placeholder_model",
                "ticker": ticker,
                "direction": "no_view",
                "confidence": 0.0,
                "rationale_plain": "占位模型无观点 (v0.1 默认 no_view)",
                "inputs_used": {
                    "advisor_week_id": ADVISOR_WEEK_ID,
                    "price_at": None,
                    "model_version": "placeholder_v1",
                },
            },
            {
                "source_id": "agent_synthesis",
                "ticker": ticker,
                "direction": "neutral",
                "confidence": 0.5,
                "rationale_plain": f"{ticker} 综合信号: 咨询师看多但市场环境中性，建议观察",
                "inputs_used": {
                    "advisor_week_id": ADVISOR_WEEK_ID,
                    "price_at": None,
                    "model_version": "agent_v1",
                },
            },
        ],
        "divergence_root_cause": f"{ticker} 存在分歧: 咨询师看多 vs 综合信号中性",
        "has_divergence": True,
        "rendered_order_seed": abs(hash(ticker + ADVISOR_WEEK_ID)) % 6,
    }


def _make_cache_key(
    advisor_week_id: str,
    ticker: str,
    prompt_template_version: str,
    model: str,
) -> str:
    """生成 LLMCache 键 (与 LLMCache._make_key 一致)。

    结论: 必须与 src/decision_ledger/llm/cache.py:LLMCache._make_key() 完全一致。
    """
    raw = f"{advisor_week_id}|{ticker}|{prompt_template_version}|{model}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def seed_llm_cache(cache_dir: Path, tickers: list[str] | None = None) -> None:
    """向 LLMCache 目录写入 mock conflict_report 数据 (绕过 Anthropic API)。

    结论: 用 LLMCache.put() 写入, 让 draft 阶段 ConflictReportAssembler 命中 cache (≤ 1s)。
    细节:
      - 仅预热 ConflictReport (Rebuttal 不可缓存, D21/R3)
      - 针对每个 ticker 写入一条 cache 文件
      - cache_dir 由调用方传入 (E2E tmpdir)
    """
    from decision_ledger.llm.cache import LLMCache

    cache = LLMCache(cache_dir=cache_dir)
    target_tickers = tickers or WATCHLIST_TICKERS

    for ticker in target_tickers:
        mock_data = _make_mock_conflict_report_cache(ticker)
        cache.put(
            advisor_week_id=ADVISOR_WEEK_ID,
            ticker=ticker,
            prompt_template_version=CONFLICT_ASSEMBLER_TEMPLATE_VERSION,
            model=CONFLICT_MODEL,
            data=mock_data,
        )


async def seed_database(db_path: Path) -> None:
    """向 SQLite 数据库写入种子数据 (30 关注股 + 1 advisor_report)。

    结论: 使用 aiosqlite 直接写入, 不依赖 Repository 层 (避免循环依赖)。
    细节:
      - watchlist: 30 个 ticker, 按 WATCHLIST_TICKERS 定义
      - advisor_reports: 1 份周报 (week_id=SEED_WEEK_ID), structured_json 含关注股 tickers
      - 持仓快照直接用 EnvSnapshot 占位 (price=None, holdings 无)
    """
    import aiosqlite

    async with aiosqlite.connect(str(db_path)) as conn:
        await conn.execute("PRAGMA foreign_keys=ON")
        await conn.execute("PRAGMA journal_mode=WAL")

        # 1. 写入 watchlist 关注股
        now_iso = datetime.now(tz=UTC).isoformat()
        for ticker in WATCHLIST_TICKERS:
            # 使用 INSERT OR IGNORE 避免重复插入
            await conn.execute(
                """
                INSERT OR IGNORE INTO watchlist (ticker, market, display_name)
                VALUES (?, ?, ?)
                """,
                (ticker, "US", f"E2E seed: {ticker}"),
            )

        # 2. 写入 advisor_report
        structured_json = json.dumps(
            {
                "tickers": WATCHLIST_TICKERS,
                "week_id": SEED_WEEK_ID,
                "advisor_week_id": ADVISOR_WEEK_ID,
                "summary": "E2E seed advisor report",
                "views": {
                    ticker: {"direction": "long", "confidence": 0.7}
                    for ticker in WATCHLIST_TICKERS
                },
            },
            ensure_ascii=False,
        )
        await conn.execute(
            """
            INSERT OR REPLACE INTO advisor_reports (
                advisor_id, source_id, week_id, raw_text, structured_json, ingested_at
            ) VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                SEED_ADVISOR_ID,
                SEED_SOURCE_ID,
                SEED_WEEK_ID,
                "E2E seed raw text",
                structured_json,
                now_iso,
            ),
        )

        await conn.commit()
