"""
ConflictCacheWarmer — T010 R3 B-R2-3 (F2-H2 简化)
结论: 预热 ConflictReport 的 job 入队器,每 ticker 仅 1 个 assemble job
细节:
  - warm_for_advisor_report(advisor_report_id): 对所有 tickers 入队 1 个 assemble job
  - F2-H2: 移除 cache_warmer_analyze (死 no-op, assemble 内部已经跑 3 lanes,
    独立 analyze 既不预热缓存又永远 mark_done, 会让"95% 成功率"指标说谎)
  - B-R2-3: 不入队任何 rebuttal 相关 job (Rebuttal 依赖 draft 内容, 每次唯一, 无法预热)
  - job_id: uuid4 保证唯一性
"""

from __future__ import annotations

import uuid
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    pass


class ConflictCacheWarmer:
    """结论: 预热 ConflictReport 的 job 入队器,每 ticker 1 个 assemble job。

    细节:
      - __init__(job_queue_repo, tickers): 注入 job 队列 repo 和关注股列表
      - warm_for_advisor_report: 批量入队,每 ticker 1 个 cache_warmer_assemble job
      - B-R2-3: 只入队 ConflictReport 相关 job,不入队 Rebuttal job
    """

    def __init__(
        self,
        job_queue_repo: Any,
        tickers: list[str],
    ) -> None:
        """结论: 注入 job 队列 repo 和关注股列表。

        细节:
          - job_queue_repo: 提供 enqueue(job_id, job_type, payload) 接口
          - tickers: 关注股列表 (30-50 个), 每次 warm 都会覆盖所有 tickers
        """
        self._job_repo = job_queue_repo
        self._tickers = tickers

    async def warm_for_advisor_report(self, advisor_report_id: str) -> None:
        """结论: 对所有关注股入队 1 个 cache_warmer_assemble job (F2-H2 简化)。

        细节:
          - 每个 ticker 入队 1 个 cache_warmer_assemble job (聚合三路 signals)
          - payload 含 advisor_report_id (便于 worker 溯源) + ticker
          - F2-H2: 不再入队 cache_warmer_analyze (死 no-op, 见 module docstring)
          - B-R2-3: 不入队任何 rebuttal job (Rebuttal 输入依赖 draft 内容, 每次唯一无法预热)
        """
        for ticker in self._tickers:
            assemble_job_id = str(uuid.uuid4())
            await self._job_repo.enqueue(
                job_id=assemble_job_id,
                job_type="cache_warmer_assemble",
                payload={
                    "ticker": ticker,
                    "advisor_report_id": advisor_report_id,
                },
            )
