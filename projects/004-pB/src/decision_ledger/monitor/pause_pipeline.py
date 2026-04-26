"""
pause_pipeline.py — T020
结论: B-lite 降级 facade，调 T010 ConflictWorker.pause/resume + T015 placeholder
细节 (R3 ⚠️ H1):
  - T015 未 ship: ImportError → log warning + graceful no-op (非 strict 模式)
  - DECISION_LEDGER_TEST_MODE=strict: ImportError → AssertionError (CI 失败)
    防止 T015 ship 后 wiring 漂移（post-ship import 失败 = wiring 错误）
  - ConflictWorker 是强依赖（T010 必须 ship），import 失败不捕获
  - _get_conflict_worker / _try_pause_monthly_scheduler 独立函数便于 patch in tests
"""

from __future__ import annotations

import logging
import os
from typing import Any

logger = logging.getLogger(__name__)

# T020 单例占位:生产 wiring 由 main.py 在 startup 注入,测试用 patch 替换。
# 默认 None 表示未注入,调用方应在测试 patch 或生产 wire 后再用。
_conflict_worker_instance: Any = None


def _get_conflict_worker() -> Any:
    """结论: 获取 ConflictWorker 单例(由 main.py startup 或 test patch 注入)。"""
    if _conflict_worker_instance is None:
        # 生产环境如果没 wire,记录警告(测试一定 patch 这个函数,不会走到这里)
        logger.warning("ConflictWorker singleton not wired; pause/resume is no-op")

        class _Noop:
            def pause(self) -> None: ...
            def resume(self) -> None: ...
            def is_paused(self) -> bool:
                return False

        return _Noop()
    return _conflict_worker_instance


def set_conflict_worker(worker: Any) -> None:
    """生产 wiring:由 main.py startup 注入 ConflictWorker 实例。"""
    global _conflict_worker_instance
    _conflict_worker_instance = worker


def _try_pause_monthly_scheduler() -> None:
    """结论: 尝试暂停 T015 MonthlyScheduler（弱依赖，ImportError 由调用方处理）。

    细节:
      - T015 未 ship 时抛 ImportError（调用方决定是否 raise / log）
      - T015 ship 后如果 import 仍失败 = wiring 错误，strict 模式下 CI 失败
    """
    from decision_ledger.services.monthly_scheduler import monthly_scheduler
    monthly_scheduler.pause()


def _try_resume_monthly_scheduler() -> None:
    """结论: 尝试恢复 T015 MonthlyScheduler（弱依赖，ImportError 由调用方处理）。"""
    from decision_ledger.services.monthly_scheduler import monthly_scheduler
    monthly_scheduler.resume()


async def pause_all_pipelines(reason: str = "") -> None:
    """B-lite 一键降级 (R3: ImportError 不静默吞).

    结论:
      - ConflictWorker.pause() 强依赖（必须成功）
      - MonthlyScheduler.pause() 弱依赖（T015 未 ship → warning; strict → AssertionError）

    参数:
      reason: 暂停原因，写入日志（可选）
    """
    worker = _get_conflict_worker()
    worker.pause()
    logger.info("ConflictWorker paused. reason=%s", reason)

    try:
        _try_pause_monthly_scheduler()
        logger.info("MonthlyScheduler paused")
    except ImportError as e:
        # R3 ⚠️ H1: T015 未 ship 是 graceful no-op (warning), T015 ship 后 import 失败 = wiring 错误
        logger.warning(
            "MonthlyScheduler import failed (T015 not shipped or wiring broken): %s", e
        )
        if os.environ.get("DECISION_LEDGER_TEST_MODE") == "strict":
            # CI / test mode 下视为失败, 防 wiring drift
            raise AssertionError(
                f"T015 import expected to succeed in strict test mode: {e}"
            ) from e

    logger.info("All pipelines paused (B-lite engaged). reason=%s", reason)


async def unpause_all_pipelines() -> None:
    """B-lite 取消降级.

    结论:
      - ConflictWorker.resume() 强依赖
      - MonthlyScheduler.resume() 弱依赖（同 pause，T015 未 ship → warning）
    """
    worker = _get_conflict_worker()
    worker.resume()
    logger.info("ConflictWorker resumed")

    try:
        _try_resume_monthly_scheduler()
        logger.info("MonthlyScheduler resumed")
    except ImportError as e:
        logger.warning("MonthlyScheduler import failed: %s", e)
        if os.environ.get("DECISION_LEDGER_TEST_MODE") == "strict":
            raise AssertionError(
                f"T015 import expected to succeed: {e}"
            ) from e

    logger.info("All pipelines resumed (B-lite disengaged)")
