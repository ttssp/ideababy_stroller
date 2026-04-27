"""
pause_pipeline.py — T020
结论: B-lite 降级 facade, 调 T010 ConflictWorker.pause/resume + T015 placeholder
细节 (R3 ⚠️ H1):
  - T015 未 ship: ImportError → log warning + graceful no-op (非 strict 模式)
  - DECISION_LEDGER_TEST_MODE=strict: ImportError → AssertionError (CI 失败)
    防止 T015 ship 后 wiring 漂移 (post-ship import 失败 = wiring 错误)
  - ConflictWorker 是强依赖 (T010 必须 ship), import 失败不捕获
  - _get_conflict_worker / _try_pause_monthly_scheduler 独立函数便于 patch in tests

F2-T020 H7 (followup A1 修订):
  - 生产模式未注入 → 默认 _Noop + WARNING + counter 自增 (不再 raise)
    理由: v0.1 plugin registry 系统性死代码, ConflictWorker 在 production
    本就不启动 (见 docs/known-issues-v0.1.md)。raise 反而把 R8 panic stop
    路径变成定时炸弹。改 noop + counter + 启动期 BANNER 让"未生效"显式可见。
  - DECISION_LEDGER_TEST_MODE=strict 维持 raise (CI gate 抓 wiring drift)
  - DECISION_LEDGER_TEST_MODE=allow-noop 维持返回 _Noop (显式 fixture 用)
F2-T020 H8: pause/resume 是同步方法, 用 asyncio.Lock 串行化避免并发 race
  (例如 O10 alert 与人工 panic stop 并发触发 pause_all)。
F2-T020 H9: 提供 reset_conflict_worker() helper, 测试 fixture 用以避免
  跨测试 wiring 污染。
"""

from __future__ import annotations

import asyncio
import logging
import os
from typing import Any

logger = logging.getLogger(__name__)

# T020 单例占位: 生产 wiring 由 main.py 在 startup 注入, 测试用 patch 替换。
# 默认 None 表示未注入。
_conflict_worker_instance: Any = None

# F2-T020 H8: pause/resume 同步方法 + asyncio.Lock 串行化, 防 O10 alert 与
# 人工 panic stop 并发触发导致 worker._paused 状态颠倒。
_pause_lock: asyncio.Lock = asyncio.Lock()

# F2-T020 H7: noop 模式开关; 仅特定测试 fixture 显式打开
_TEST_MODE_NOOP = "allow-noop"
# F2-T020 H7 (followup A1): strict 模式仍 raise (CI gate 抓 wiring drift)
_TEST_MODE_STRICT = "strict"

# F2-T020 H7 (followup A1): 未 wire 时 _get_conflict_worker 调用计数,
# 给 R8 panic stop 路径"已知未生效"提供可观测信号。
# 启动期 BANNER 通过 get_wiring_status() 读 _conflict_worker_instance is None,
# 运行期 panic stop 失效次数通过 pause_hook_noop_call_count() 读这个 counter。
_pause_hook_noop_calls: int = 0


class _Noop:
    """ConflictWorker 同步 noop 替身, 仅 fixture 用 (F2-T020 H7/H8/H9)。"""

    def pause(self) -> None: ...
    def resume(self) -> None: ...
    def is_paused(self) -> bool:
        return False


def _get_conflict_worker() -> Any:
    """获取 ConflictWorker 单例 (由 main.py startup 或 test patch 注入)。

    F2-T020 H7 (followup A1): 行为分三档:
      1. 已注入 (`set_conflict_worker(worker)` 调用过) → 返回真实 worker
      2. 未注入且 TEST_MODE=strict → raise (CI gate 抓 wiring drift)
      3. 其他 (包括 production 默认 / TEST_MODE=allow-noop / 未设)
         → 返回 _Noop + WARNING + counter 自增

    为什么 production 默认 noop 而非 raise: v0.1 plugin registry 是系统性死代码,
    ConflictWorker 不在 production 启动 (见 docs/known-issues-v0.1.md)。
    raise 把 R8 panic stop 路径变成定时炸弹反而更糟。改用 counter +
    启动期 BANNER 让"未生效"显式可见。
    """
    if _conflict_worker_instance is not None:
        return _conflict_worker_instance

    test_mode = os.environ.get("DECISION_LEDGER_TEST_MODE", "")

    if test_mode == _TEST_MODE_STRICT:
        raise RuntimeError(
            "ConflictWorker singleton not wired (strict mode). "
            "在 main.py startup 调 set_conflict_worker(worker), "
            "或临时设置 DECISION_LEDGER_TEST_MODE=allow-noop。"
        )

    # production 默认 + allow-noop 都走这里: noop + WARNING + counter
    global _pause_hook_noop_calls
    _pause_hook_noop_calls += 1
    logger.warning(
        "pause_pipeline: ConflictWorker 未 wire, 走 _Noop 替身 "
        "(R8 panic stop 在此调用上不生效; 累计 %d 次; v0.1 已知, "
        "见 docs/known-issues-v0.1.md)",
        _pause_hook_noop_calls,
    )
    return _Noop()


def get_wiring_status() -> dict[str, str]:
    """F2-T020 H7 (followup A1): 暴露当前 wiring 状态,给 main.py 启动期 BANNER 自检。

    返回各 wiring 槽位的状态: "wired" 表示已注入真实实例, "noop" 表示走替身。
    新加 wiring 时应在此处增加键, 让 BANNER 自动检测。
    """
    return {
        "conflict_worker": "wired" if _conflict_worker_instance is not None else "noop",
    }


def pause_hook_noop_call_count() -> int:
    """F2-T020 H7 (followup A1): 读取累计的 noop 调用次数。

    用途:
      - smoke / 自检脚本: 触发一次 panic stop, 看 counter 是否自增
      - 测试: 断言未注入路径走了 noop 分支
    """
    return _pause_hook_noop_calls


def set_conflict_worker(worker: Any) -> None:
    """生产 wiring: 由 main.py startup 注入 ConflictWorker 实例。

    F2-T020 H7: 真的 wire 进来不许给假货 (None / 缺 pause/resume 方法 / async 方法
    都视为 wiring 错误)。
    """
    if worker is None:
        raise ValueError("set_conflict_worker(None) 非法; 用 reset_conflict_worker() 清空")
    for attr in ("pause", "resume", "is_paused"):
        if not callable(getattr(worker, attr, None)):
            raise TypeError(
                f"ConflictWorker wiring 错误: 缺少同步方法 {attr!r}"
            )
        if asyncio.iscoroutinefunction(getattr(worker, attr)):
            raise TypeError(
                f"ConflictWorker.{attr} 必须是同步方法, 收到 async (F2-T020 H8)"
            )
    global _conflict_worker_instance
    _conflict_worker_instance = worker


def reset_conflict_worker() -> None:
    """F2-T020 H9: 清空注入实例 (测试 fixture 专用, 防跨测试 wiring 污染)。

    F2-T020 H7 (followup A1): 同时重置 noop counter, 让每个测试的断言独立。
    """
    global _conflict_worker_instance, _pause_hook_noop_calls
    _conflict_worker_instance = None
    _pause_hook_noop_calls = 0


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
    """B-lite 一键降级 (R3: ImportError 不静默吞)。

    结论:
      - ConflictWorker.pause() 强依赖 (必须成功)
      - MonthlyScheduler.pause() 弱依赖 (T015 未 ship → warning; strict → AssertionError)
      - F2-T020 H8: 全过程持 _pause_lock, 串行化并发 pause/resume

    参数:
      reason: 暂停原因, 写入日志 (可选)
    """
    async with _pause_lock:
        worker = _get_conflict_worker()
        worker.pause()
        logger.info("ConflictWorker paused. reason=%s", reason)

        try:
            _try_pause_monthly_scheduler()
            logger.info("MonthlyScheduler paused")
        except ImportError as e:
            # R3 ⚠️ H1: T015 未 ship → graceful no-op (warning),
            # ship 后再 import 失败 = wiring 错误 (strict mode 下 raise)
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
    """B-lite 取消降级 (F2-T020 H8: 锁串行化)。

    结论:
      - ConflictWorker.resume() 强依赖
      - MonthlyScheduler.resume() 弱依赖 (同 pause, T015 未 ship → warning)
    """
    async with _pause_lock:
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
