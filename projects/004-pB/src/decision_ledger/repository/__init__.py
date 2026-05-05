"""
Decision Ledger Repository 层 — T003
结论: 封装 SQLite 异步访问，暴露各 domain 的 Repository 类
细节:
  - 全部使用 aiosqlite 异步驱动
  - 写路径通过 WriterLock (asyncio.Lock) 保护（单一 writer 不变量）
  - 读路径不加锁（WAL 模式 reader 不阻塞 writer）
  - 全部 SQL 用 ? parametrized placeholder（SEC-5）
"""

from __future__ import annotations

from decision_ledger.repository.advisor_repo import AdvisorRepository
from decision_ledger.repository.alert_repo import AlertRepository
from decision_ledger.repository.base import AsyncConnectionPool
from decision_ledger.repository.conflict_repo import ConflictRepository
from decision_ledger.repository.decision_repo import DecisionRepository
from decision_ledger.repository.job_queue_repo import JobQueueRepository
from decision_ledger.repository.llm_usage_repo import LLMUsageRepository
from decision_ledger.repository.note_repo import NoteRepository
from decision_ledger.repository.portfolio_repo import PortfolioRepository
from decision_ledger.repository.rebuttal_repo import RebuttalRepository

__all__ = [
    "AdvisorRepository",
    "AlertRepository",
    "AsyncConnectionPool",
    "ConflictRepository",
    "DecisionRepository",
    "JobQueueRepository",
    "LLMUsageRepository",
    "NoteRepository",
    "PortfolioRepository",
    "RebuttalRepository",
]
