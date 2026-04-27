"""
BLiteService — T022
结论: B-lite 降级路径核心服务 (CLI only, R3 删除 UI toggle)
细节:
  - engage(reason): 调 pause_all_pipelines + 写 meta_decisions (cooling_off_until = now+14d)
  - disengage(): 14 天 cooling-off 检查 + 调 unpause_all_pipelines
  - is_engaged(): 读 ConflictWorker.is_paused() 反映当前降级状态
  - status(): 返回 engaged / cooling_off_remaining / last_reason
  - _ensure_table(): CREATE TABLE IF NOT EXISTS meta_decisions（不依赖 alembic）
  - 必须显式 import pause_all_pipelines / unpause_all_pipelines (R2 H1)
"""

from __future__ import annotations

import logging
import uuid
from datetime import UTC, datetime, timedelta
from typing import Any

from decision_ledger.domain.alert import MetaDecision
from decision_ledger.monitor.pause_pipeline import pause_all_pipelines, unpause_all_pipelines
from decision_ledger.repository.base import AsyncConnectionPool

logger = logging.getLogger(__name__)

# 14 天 cooling-off 约束 (不可配置，硬约束)
_COOLING_OFF_DAYS = 14

_CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS meta_decisions (
    meta_id          TEXT PRIMARY KEY,
    decision_type    TEXT NOT NULL,
    reason           TEXT NOT NULL,
    created_at       TEXT NOT NULL,
    cooling_off_until TEXT
)
"""


class BLiteService:
    """B-lite 降级路径服务 (T022, R3: CLI only).

    结论: 封装 engage/disengage 状态机 + 14d cooling-off + pause facade 调用。
    细节:
      - 不依赖 alembic，通过 _ensure_table() 自建 meta_decisions 表
      - engage() / disengage() 均为 async（因调用 async pause facade）
      - is_engaged() 同步读取 ConflictWorker.is_paused() 状态
    """

    def __init__(self, pool: AsyncConnectionPool) -> None:
        """
        结论: 仅注入 pool，不建立任何连接。
        """
        self._pool = pool

    async def _ensure_table(self) -> None:
        """结论: 幂等创建 meta_decisions 表（不经 alembic）。

        细节:
          - CREATE TABLE IF NOT EXISTS 幂等，可重复调用
          - 写路径使用 write_connection()（单一 writer 不变量）
        """
        async with self._pool.write_connection() as conn:
            await conn.execute(_CREATE_TABLE_SQL)
            await conn.commit()

    async def engage(self, reason: str) -> MetaDecision:
        """触发 B-lite 降级: pause 所有 pipeline + 写 meta_decisions 记录。

        结论:
          - 调用 pause_all_pipelines(reason) (R2 H1 强依赖)
          - 写 decision_type="b_lite_engaged", cooling_off_until=now+14d
          - 返回 MetaDecision pydantic 对象

        参数:
          reason: 触发降级的原因（必填），写入档案

        返回:
          MetaDecision: 本次 engage 的元决策档案
        """
        await self._ensure_table()
        await pause_all_pipelines(reason)

        now = datetime.now(tz=UTC)
        cooling_off_until = now + timedelta(days=_COOLING_OFF_DAYS)
        meta_id = str(uuid.uuid4())

        async with self._pool.write_connection() as conn:
            await conn.execute(
                """
                INSERT INTO meta_decisions
                    (meta_id, decision_type, reason, created_at, cooling_off_until)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    meta_id,
                    "b_lite_engaged",
                    reason,
                    now.isoformat(),
                    cooling_off_until.isoformat(),
                ),
            )
            await conn.commit()

        decision = MetaDecision(
            meta_id=meta_id,
            decision_type="b_lite_engaged",
            reason=reason,
            created_at=now,
            cooling_off_until=cooling_off_until,
        )
        logger.info(
            "B-lite engaged. meta_id=%s cooling_off_until=%s reason=%s",
            meta_id,
            cooling_off_until.isoformat(),
            reason,
        )
        return decision

    async def disengage(self) -> MetaDecision:
        """解除 B-lite 降级: 检查 cooling-off + resume 所有 pipeline。

        结论:
          - 读取最近一条 b_lite_engaged 记录的 cooling_off_until
          - 若 cooling_off_until > now → 抛 ValueError("cooling-off")
          - 否则调用 unpause_all_pipelines() (R2 H1)
          - 写 decision_type="b_lite_disengaged" 记录

        返回:
          MetaDecision: 本次 disengage 的元决策档案

        抛出:
          ValueError: 若在 14 天 cooling-off 期内调用
        """
        await self._ensure_table()

        # 读取最近 engage 记录的 cooling_off_until
        async with self._pool.connection() as conn:
            cursor = await conn.execute(
                """
                SELECT cooling_off_until
                FROM meta_decisions
                WHERE decision_type = 'b_lite_engaged'
                ORDER BY created_at DESC
                LIMIT 1
                """
            )
            row = await cursor.fetchone()

        now = datetime.now(tz=UTC)

        if row is not None and row["cooling_off_until"] is not None:
            cooling_off_until = datetime.fromisoformat(row["cooling_off_until"])
            # 确保 timezone-aware 比较
            if cooling_off_until.tzinfo is None:
                cooling_off_until = cooling_off_until.replace(tzinfo=UTC)
            if now < cooling_off_until:
                remaining = cooling_off_until - now
                raise ValueError(
                    f"cooling-off 期内不可 disengage，剩余 {remaining.days} 天 "
                    f"(cooling_off_until={cooling_off_until.isoformat()})"
                )

        await unpause_all_pipelines()

        meta_id = str(uuid.uuid4())
        async with self._pool.write_connection() as conn:
            await conn.execute(
                """
                INSERT INTO meta_decisions
                    (meta_id, decision_type, reason, created_at, cooling_off_until)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    meta_id,
                    "b_lite_disengaged",
                    "manual disengage",
                    now.isoformat(),
                    None,
                ),
            )
            await conn.commit()

        decision = MetaDecision(
            meta_id=meta_id,
            decision_type="b_lite_disengaged",
            reason="manual disengage",
            created_at=now,
            cooling_off_until=None,
        )
        logger.info("B-lite disengaged. meta_id=%s", meta_id)
        return decision

    def is_engaged(self) -> bool:
        """结论: 读 ConflictWorker.is_paused() 判断当前是否处于 B-lite 降级状态。

        细节:
          - 同步方法（ConflictWorker.is_paused() 是同步的）
          - 通过 pause_pipeline 内部 _get_conflict_worker() 获取单例
          - 不查数据库（避免 async 依赖）
        """
        from decision_ledger.monitor.pause_pipeline import _get_conflict_worker
        worker = _get_conflict_worker()
        return bool(worker.is_paused())

    async def status(self) -> dict[str, Any]:
        """返回当前 B-lite 状态快照。

        结论:
          - engaged: 优先读 DB 最后一条记录判断（ConflictWorker 可能未 wire，如 CLI 场景）
            * 最后一条 meta_decisions 记录是 b_lite_engaged → True
            * 最后一条是 b_lite_disengaged 或无记录 → False
          - cooling_off_remaining: 若在 cooling-off 期内，返回剩余 timedelta；否则 None
          - last_reason: 最近 engage 的 reason；若无记录返回 None

        返回:
          dict 含 "engaged" / "cooling_off_remaining" / "last_reason"

        细节:
          - CLI 测试场景（subprocess）中 ConflictWorker 未 wire，is_paused()=False 不准确
          - 因此 status() 优先查 meta_decisions 表最后一条记录判断 engaged 状态
          - 进程内可通过 is_engaged() 读 ConflictWorker 状态（实时）
        """
        await self._ensure_table()

        # 读最后一条 meta_decisions 记录（任意 decision_type），判断当前 engaged 状态
        async with self._pool.connection() as conn:
            cursor = await conn.execute(
                """
                SELECT decision_type, reason, cooling_off_until
                FROM meta_decisions
                ORDER BY created_at DESC
                LIMIT 1
                """
            )
            last_row = await cursor.fetchone()

            # 读最近 engage 记录的 reason 和 cooling_off
            cursor2 = await conn.execute(
                """
                SELECT reason, cooling_off_until
                FROM meta_decisions
                WHERE decision_type = 'b_lite_engaged'
                ORDER BY created_at DESC
                LIMIT 1
                """
            )
            engage_row = await cursor2.fetchone()

        # engaged = 最后一条记录是 b_lite_engaged
        engaged = (
            last_row is not None
            and last_row["decision_type"] == "b_lite_engaged"
        )

        cooling_off_remaining: timedelta | None = None
        last_reason: str | None = None

        if engage_row is not None:
            last_reason = engage_row["reason"]
            if engage_row["cooling_off_until"] is not None:
                cooling_off_until = datetime.fromisoformat(engage_row["cooling_off_until"])
                if cooling_off_until.tzinfo is None:
                    cooling_off_until = cooling_off_until.replace(tzinfo=UTC)
                now = datetime.now(tz=UTC)
                if now < cooling_off_until:
                    cooling_off_remaining = cooling_off_until - now

        return {
            "engaged": engaged,
            "cooling_off_remaining": cooling_off_remaining,
            "last_reason": last_reason,
        }
