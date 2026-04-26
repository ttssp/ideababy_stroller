"""
ConflictWorker — T010 R2 H1
结论: ConflictReport cache warmer job 消费者，支持 pause/resume/is_paused hook
细节:
  - pause() / resume() / is_paused(): hook API，供 draft 同步路径挂载
  - run_loop(): 持续消费 cache_warmer 队列的 job
  - paused 时跳过 claim_next（不消费），直接 sleep（draft 同步路径不经过 worker）
  - R2 H1: pause 不影响 ConflictReportAssemblerService 直接调用（T008 draft 路径独立）
"""

from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from decision_ledger.services.conflict_report_assembler import ConflictReportAssemblerService


class ConflictWorker:
    """结论: cache warmer job 消费者，pause/resume 控制队列消费行为。

    细节:
      - _paused: bool 状态，pause() 设为 True, resume() 设为 False
      - is_paused(): 返回当前 _paused 值
      - run_loop(): 轮询 job_queue_repo.claim_next()，paused 时只 sleep 不消费
      - R2 H1: draft 同步路径（T008 DecisionRecorder）不走 worker，pause 不影响其路径
    """

    _POLL_INTERVAL_SEC: float = 1.0   # 正常轮询间隔（秒）
    _PAUSE_SLEEP_SEC: float = 2.0     # pause 状态下的 sleep 间隔（秒）

    def __init__(
        self,
        job_queue_repo: Any,
        assembler_service: ConflictReportAssemblerService | Any,
    ) -> None:
        """结论: 注入 job 队列 repo 和 assembler service。

        细节:
          - job_queue_repo: 提供 claim_next() / mark_done() / mark_failed()
          - assembler_service: 执行具体的 ConflictReport 组装任务
        """
        self._job_queue_repo = job_queue_repo
        self._assembler_service = assembler_service
        self._paused: bool = False

    # ── pause/resume/is_paused hook API ──────────────────────────────────────

    def pause(self) -> None:
        """结论: 暂停 worker 队列消费（幂等）。

        细节:
          - 多次调用不报错（幂等）
          - draft 同步路径不受影响（R2 H1 设计决定）
        """
        self._paused = True

    def resume(self) -> None:
        """结论: 恢复 worker 队列消费（幂等）。

        细节: 多次调用不报错（幂等）。
        """
        self._paused = False

    def is_paused(self) -> bool:
        """结论: 返回当前 pause 状态。"""
        return self._paused

    # ── run_loop ──────────────────────────────────────────────────────────────

    async def run_loop(self) -> None:
        """结论: 持续轮询 job 队列，paused 时跳过消费只 sleep。

        细节:
          - paused=True: await asyncio.sleep(PAUSE_SLEEP_SEC)，不调 claim_next
          - paused=False: claim_next() → 有 job 则执行，无 job 则 sleep(POLL_INTERVAL)
          - job 执行失败: mark_failed + 继续（不 raise 避免 worker 崩溃）
        """
        while True:
            if self._paused:
                # pause 状态: 不消费队列，只等待
                await asyncio.sleep(self._PAUSE_SLEEP_SEC)
                continue

            job = await self._job_queue_repo.claim_next()
            if job is None:
                # 队列为空，等待后重试
                await asyncio.sleep(self._POLL_INTERVAL_SEC)
                continue

            # 执行 job
            job_id: str = job.get("job_id", "unknown")
            job_type: str = job.get("job_type", "")
            payload: dict[str, Any] = job.get("payload", {})

            try:
                await self._execute_job(job_type=job_type, payload=payload)
                await self._job_queue_repo.mark_done(job_id)
            except Exception as exc:
                # 记录失败但不 raise（保持 worker 持续运行）
                await self._job_queue_repo.mark_failed(job_id, str(exc))

    async def _execute_job(self, job_type: str, payload: dict[str, Any]) -> None:
        """结论: 根据 job_type 执行对应任务。

        细节:
          - cache_warmer_analyze: 调 assembler_service.assemble 的 analyze 阶段（预热）
          - cache_warmer_assemble: 调 assembler_service.assemble 完整流程（预热）
          - 其他 job_type: raise ValueError（明确拒绝未知 job）
        """
        if job_type not in ("cache_warmer_analyze", "cache_warmer_assemble"):
            raise ValueError(f"ConflictWorker 不识别 job_type: {job_type!r}")

        ticker: str = payload.get("ticker", "")
        if not ticker:
            raise ValueError(f"job payload 缺少 ticker 字段: {payload}")

        # 注: env_snapshot 在 cache warmer 场景下可以为 None 或从 payload 重建
        # 这里简化处理：cache warmer 阶段不需要完整 env_snapshot
        # 实际 prod 实现应从 payload 反序列化 env_snapshot
        env_snapshot = payload.get("env_snapshot", None)

        if job_type == "cache_warmer_assemble" and env_snapshot is not None:
            await self._assembler_service.assemble(
                ticker=ticker,
                env_snapshot=env_snapshot,
            )
        # cache_warmer_analyze 阶段: 单路 lane analyze（未来扩展，当前 no-op for warmer）
