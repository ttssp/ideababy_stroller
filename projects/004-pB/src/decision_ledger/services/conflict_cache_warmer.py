"""
ConflictCacheWarmer — T010 R3 B-R2-3
结论: 预热 ConflictReport 的 job 入队器，严禁入队 Rebuttal 类型 job
细节:
  - warm_for_advisor_report(advisor_report_id): 对所有 tickers 入队 analyze + assemble jobs
  - 每个 ticker: 3 个 cache_warmer_analyze + 1 个 cache_warmer_assemble = 4 jobs
  - B-R2-3: 不入队任何 rebuttal 相关 job（Rebuttal 依赖 draft 内容，每次唯一，无法预热）
  - job_id: uuid4 保证唯一性
"""

from __future__ import annotations

import uuid
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    pass


# ── 常量 ─────────────────────────────────────────────────────────────────────

_ANALYZE_LANES = ("advisor", "placeholder_model", "agent_synthesis")
"""三个标准 lane 的 source_id（cache_warmer_analyze job 对应）。"""


class ConflictCacheWarmer:
    """结论: 预热 ConflictReport 的 job 入队器。

    细节:
      - __init__(job_queue_repo, tickers): 注入 job 队列 repo 和关注股列表
      - warm_for_advisor_report: 批量入队，每 ticker 4 个 job
      - B-R2-3: 只入队 ConflictReport 相关 job，不入队 Rebuttal job
    """

    def __init__(
        self,
        job_queue_repo: Any,
        tickers: list[str],
    ) -> None:
        """结论: 注入 job 队列 repo 和关注股列表。

        细节:
          - job_queue_repo: 提供 enqueue(job_id, job_type, payload) 接口
          - tickers: 关注股列表（30-50 个），每次 warm 都会覆盖所有 tickers
        """
        self._job_repo = job_queue_repo
        self._tickers = tickers

    async def warm_for_advisor_report(self, advisor_report_id: str) -> None:
        """结论: 对所有关注股入队 analyze + assemble jobs（不含 Rebuttal）。

        细节:
          - 每个 ticker 入队:
            * 3 个 cache_warmer_analyze job（对应 advisor / placeholder_model / agent_synthesis）
            * 1 个 cache_warmer_assemble job（聚合全部 signals）
          - payload 含 advisor_report_id（便于 worker 溯源）、ticker、lane_source_id（analyze 用）
          - B-R2-3: 不入队任何 rebuttal job（Rebuttal 输入依赖 draft 内容，每次唯一无法预热）
        """
        for ticker in self._tickers:
            # 3 个 analyze jobs（对应三个 lane）
            for source_id in _ANALYZE_LANES:
                job_id = str(uuid.uuid4())
                await self._job_repo.enqueue(
                    job_id=job_id,
                    job_type="cache_warmer_analyze",
                    payload={
                        "ticker": ticker,
                        "advisor_report_id": advisor_report_id,
                        "lane_source_id": source_id,
                    },
                )

            # 1 个 assemble job（聚合三路 signals）
            assemble_job_id = str(uuid.uuid4())
            await self._job_repo.enqueue(
                job_id=assemble_job_id,
                job_type="cache_warmer_assemble",
                payload={
                    "ticker": ticker,
                    "advisor_report_id": advisor_report_id,
                },
            )
