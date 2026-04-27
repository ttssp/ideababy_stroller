#!/usr/bin/env python
"""
toggle_b_lite.py — T022 B-lite CLI
结论: 3 个子命令 engage / disengage / status 操控 B-lite 降级路径
细节:
  - engage --reason="...": 触发降级 (写 meta_decisions + pause pipelines)
  - disengage: 解除降级 (14 天 cooling-off 检查 + resume pipelines)
  - status: 显示当前状态 (engaged / cooling_off_remaining / last_reason)
  - DECISION_LEDGER_B_LITE_SKIP_PAUSE=1: 测试逃逸，跳过真实 pause hook
  - DECISION_LEDGER_DB_URL: SQLite DB 路径 (环境变量)
"""

from __future__ import annotations

import argparse
import asyncio
import os
import sys
from pathlib import Path

# 将 src 加入 sys.path（方便 scripts/ 目录直接运行）
_project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_project_root / "src"))


def _get_db_path() -> str:
    """结论: 从环境变量读取 DB 路径（DECISION_LEDGER_DB_URL 或默认路径）。"""
    db_url = os.environ.get("DECISION_LEDGER_DB_URL", "")
    if db_url.startswith("sqlite:///"):
        return db_url[len("sqlite:///"):]
    if db_url:
        return db_url
    # 默认路径：项目根的 decision_ledger.sqlite
    return str(_project_root / "decision_ledger.sqlite")


async def _engage(reason: str) -> None:
    """执行 engage 子命令。"""
    from decision_ledger.repository.base import AsyncConnectionPool
    from decision_ledger.services.b_lite_service import BLiteService

    db_path = _get_db_path()
    pool = AsyncConnectionPool(db_path)
    await pool.initialize()

    try:
        if os.environ.get("DECISION_LEDGER_B_LITE_SKIP_PAUSE") == "1":
            # 测试逃逸: 用 mock 替换 pause facade
            from unittest.mock import MagicMock, patch

            mock_cw = MagicMock()
            mock_cw.is_paused.return_value = True
            mock_ms = MagicMock()

            with (
                patch(
                    "decision_ledger.monitor.pause_pipeline._conflict_worker_instance",
                    mock_cw,
                ),
                patch(
                    "decision_ledger.services.monthly_scheduler.monthly_scheduler",
                    mock_ms,
                ),
                patch(
                    "decision_ledger.monitor.pause_pipeline._try_pause_monthly_scheduler",
                    new_callable=lambda: lambda: None,
                ),
            ):
                svc = BLiteService(pool=pool)
                meta = await svc.engage(reason=reason)
        else:
            svc = BLiteService(pool=pool)
            meta = await svc.engage(reason=reason)

        cooling_off_str = (
            meta.cooling_off_until.isoformat() if meta.cooling_off_until else "N/A"
        )
        print("[B-lite] ENGAGED")
        print(f"  meta_id:           {meta.meta_id}")
        print(f"  reason:            {meta.reason}")
        print(f"  cooling_off_until: {cooling_off_str}")
        print("  ConflictWorker + MonthlyScheduler -> PAUSED")
    finally:
        await pool.close()


async def _disengage() -> None:
    """执行 disengage 子命令。"""
    from decision_ledger.repository.base import AsyncConnectionPool
    from decision_ledger.services.b_lite_service import BLiteService

    db_path = _get_db_path()
    pool = AsyncConnectionPool(db_path)
    await pool.initialize()

    try:
        if os.environ.get("DECISION_LEDGER_B_LITE_SKIP_PAUSE") == "1":
            from unittest.mock import MagicMock, patch

            mock_cw = MagicMock()
            mock_cw.is_paused.return_value = False
            mock_ms = MagicMock()

            with (
                patch(
                    "decision_ledger.monitor.pause_pipeline._conflict_worker_instance",
                    mock_cw,
                ),
                patch(
                    "decision_ledger.services.monthly_scheduler.monthly_scheduler",
                    mock_ms,
                ),
                patch(
                    "decision_ledger.monitor.pause_pipeline._try_resume_monthly_scheduler",
                    new_callable=lambda: lambda: None,
                ),
            ):
                svc = BLiteService(pool=pool)
                meta = await svc.disengage()
        else:
            svc = BLiteService(pool=pool)
            meta = await svc.disengage()

        print("[B-lite] DISENGAGED")
        print(f"  meta_id:  {meta.meta_id}")
        print("  ConflictWorker + MonthlyScheduler -> RESUMED")
    except ValueError as exc:
        print(f"[B-lite] ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
    finally:
        await pool.close()


async def _status() -> None:
    """执行 status 子命令。"""
    from decision_ledger.repository.base import AsyncConnectionPool
    from decision_ledger.services.b_lite_service import BLiteService

    db_path = _get_db_path()
    pool = AsyncConnectionPool(db_path)
    await pool.initialize()

    try:
        svc = BLiteService(pool=pool)
        st = await svc.status()

        engaged_str = "YES" if st["engaged"] else "NO"
        print(f"[B-lite] STATUS: {engaged_str}")
        if st["cooling_off_remaining"] is not None:
            days = st["cooling_off_remaining"].days
            print(f"  cooling_off_remaining: {days} 天")
        if st["last_reason"] is not None:
            print(f"  last_reason: {st['last_reason']}")
    finally:
        await pool.close()


def main() -> None:
    """结论: argparse 入口，解析 3 个子命令并调用对应 async 函数。"""
    parser = argparse.ArgumentParser(
        prog="toggle_b_lite",
        description="B-lite 降级路径 CLI (T022)",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # engage 子命令
    engage_parser = sub.add_parser("engage", help="触发 B-lite 降级（pause pipelines）")
    engage_parser.add_argument(
        "--reason",
        required=True,
        help='降级原因，例如 --reason="连续 2 周决策 < 2"',
    )

    # disengage 子命令
    sub.add_parser("disengage", help="解除 B-lite 降级（14 天 cooling-off 检查）")

    # status 子命令
    sub.add_parser("status", help="显示当前 B-lite 状态")

    args = parser.parse_args()

    if args.command == "engage":
        asyncio.run(_engage(args.reason))
    elif args.command == "disengage":
        asyncio.run(_disengage())
    elif args.command == "status":
        asyncio.run(_status())
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
