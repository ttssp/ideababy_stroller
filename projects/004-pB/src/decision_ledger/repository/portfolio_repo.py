"""
PortfolioRepository — T003
结论: 关注股 watchlist + 持仓快照 CRUD
细节:
  - replace_watchlist: 事务内清空并重写（写路径，原子操作）
  - get_watchlist: 返回当前关注股列表（读路径）
  - upsert_holding_snapshot: 写入持仓快照（写路径）
  - latest_snapshot: 最新持仓快照（读路径）
"""

from __future__ import annotations

import json
from datetime import UTC, datetime

from decision_ledger.domain.portfolio import Holding, HoldingsSnapshot, Market, Watchlist
from decision_ledger.repository.base import AsyncConnectionPool


class PortfolioRepository:
    """关注股 + 持仓快照 Repository。"""

    def __init__(self, pool: AsyncConnectionPool) -> None:
        self._pool = pool

    async def replace_watchlist(self, watchlist: list[Watchlist]) -> None:
        """事务内清空并重写 watchlist（写路径，原子操作）。

        结论: 整体替换，不做 diff，保证 watchlist 与输入完全一致。
        """
        async with self._pool.write_connection() as conn:
            await conn.execute("DELETE FROM watchlist")
            for item in watchlist:
                await conn.execute(
                    """
                    INSERT INTO watchlist (ticker, market, display_name) VALUES (?, ?, ?)
                    """,
                    (item.ticker, item.market.value, item.display_name),
                )
            await conn.commit()

    async def get_watchlist(self) -> list[Watchlist]:
        """返回当前关注股列表（读路径）。"""
        async with self._pool.connection() as conn:
            cursor = await conn.execute(
                "SELECT ticker, market, display_name FROM watchlist ORDER BY ticker"
            )
            rows = await cursor.fetchall()
            return [
                Watchlist(
                    ticker=str(row["ticker"]),
                    market=Market(str(row["market"])),
                    display_name=str(row["display_name"]) if row["display_name"] else None,
                )
                for row in rows
            ]

    async def upsert_holding_snapshot(self, snapshot: HoldingsSnapshot) -> None:
        """写入持仓快照（写路径）。

        结论: 直接 INSERT，不 REPLACE（每次快照保留历史，latest_snapshot 取最新）。
        细节: holdings 序列化为 JSON 存入 env_snapshots 表（v0.1 无独立 holdings 表）。
        """
        async with self._pool.write_connection() as conn:
            await conn.execute(
                """
                INSERT INTO env_snapshots (
                    snapshot_id, price, holdings_pct, holdings_abs, advisor_week_id, snapshot_at
                ) VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    snapshot.snapshot_id,
                    snapshot.total_value,
                    None,  # holdings_pct: 快照级别不存，按 ticker 存
                    None,  # holdings_abs: 同上
                    None,  # advisor_week_id: 快照不关联
                    snapshot.snapshot_at.isoformat(),
                ),
            )
            # holdings 存为 notes 附加存储（简化实现，v0.1 合理）
            # 实际上把持仓 JSON 存在 snapshot_id 对应的 notes 表作为 raw_data
            # 为保持简洁，存在 notes 表 content 字段（note_id = snapshot_id）
            holdings_json = json.dumps(
                [h.model_dump() for h in snapshot.holdings], ensure_ascii=False
            )
            now = datetime.now(tz=UTC).isoformat()
            import hashlib
            content_hash = hashlib.sha256(holdings_json.encode()).hexdigest()
            await conn.execute(
                """
                INSERT OR REPLACE INTO notes (
                    note_id, title, content, tags_json, content_hash, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    f"holdings_snapshot_{snapshot.snapshot_id}",
                    f"Holdings Snapshot {snapshot.snapshot_id}",
                    holdings_json,
                    json.dumps(["holdings_snapshot"]),
                    content_hash,
                    now,
                    now,
                ),
            )
            await conn.commit()

    async def latest_snapshot(self) -> HoldingsSnapshot | None:
        """返回最新的持仓快照（读路径）。

        结论: 从 env_snapshots 取最新 snapshot_id，再查 notes 拿 holdings JSON。
        """
        async with self._pool.connection() as conn:
            cursor = await conn.execute(
                """
                SELECT snapshot_id, snapshot_at FROM env_snapshots
                WHERE snapshot_id LIKE 'hs_%' OR snapshot_id NOT LIKE '%draft%'
                ORDER BY snapshot_at DESC
                LIMIT 1
                """
            )
            row = await cursor.fetchone()
            if row is None:
                return None

            snapshot_id = str(row["snapshot_id"])
            snapshot_at = datetime.fromisoformat(str(row["snapshot_at"]))

            # 从 notes 查 holdings JSON
            cursor2 = await conn.execute(
                "SELECT content FROM notes WHERE note_id = ?",
                (f"holdings_snapshot_{snapshot_id}",),
            )
            row2 = await cursor2.fetchone()
            if row2 is None:
                return HoldingsSnapshot(
                    snapshot_id=snapshot_id,
                    holdings=[],
                    snapshot_at=snapshot_at,
                )

            holdings_data = json.loads(str(row2["content"]))
            holdings = [Holding(**h) for h in holdings_data]
            return HoldingsSnapshot(
                snapshot_id=snapshot_id,
                holdings=holdings,
                snapshot_at=snapshot_at,
            )
