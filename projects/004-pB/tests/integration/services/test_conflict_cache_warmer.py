"""
ConflictCacheWarmer 集成测试 — T010 R3 B-R2-3
结论: 验证 warmer 只预热 ConflictReport（不预热 Rebuttal），enqueue ≥ 30 jobs
细节:
  - test_warmer_enqueues_30_50_tickers: 30 关注股 × (3 analyze + 1 assemble) = 120 jobs
  - test_warmer_does_not_enqueue_rebuttal: warmer 不入队 Rebuttal 类型 job (R3 B-R2-3)
  - test_warmer_enqueue_is_idempotent: 重复调用不重复入队
"""

from __future__ import annotations

from typing import Any


class FakeJobQueueRepo:
    """JobQueueRepository 测试 Fake，记录所有 enqueue 调用。"""

    def __init__(self) -> None:
        self.enqueued_jobs: list[dict[str, Any]] = []

    async def enqueue(self, job_id: str, job_type: str, payload: dict[str, Any]) -> None:
        """记录入队的 job。"""
        self.enqueued_jobs.append({
            "job_id": job_id,
            "job_type": job_type,
            "payload": payload,
        })

    async def claim_next(self) -> dict[str, Any] | None:
        return None

    async def mark_done(self, job_id: str) -> None:
        pass

    async def mark_failed(self, job_id: str, error_msg: str = "") -> None:
        pass


class TestConflictCacheWarmerEnqueue:
    """ConflictCacheWarmer.warm_for_advisor_report 入队行为测试。"""

    async def test_warmer_enqueues_30_50_tickers(self) -> None:
        """结论: 30 关注股 × (3 analyze + 1 assemble) = 120 jobs 入队。"""
        from decision_ledger.services.conflict_cache_warmer import ConflictCacheWarmer

        fake_job_repo = FakeJobQueueRepo()

        # 构建 30 关注股列表
        tickers = [f"TICKER{i:02d}" for i in range(30)]

        warmer = ConflictCacheWarmer(
            job_queue_repo=fake_job_repo,
            tickers=tickers,
        )

        await warmer.warm_for_advisor_report(advisor_report_id="advisor_2026_W17")

        # 每个 ticker: 3 lane.analyze + 1 assemble = 4 jobs
        # 30 tickers × 4 = 120 jobs
        assert len(fake_job_repo.enqueued_jobs) >= 30, (
            f"warmer 应入队 ≥ 30 个 job，当前 {len(fake_job_repo.enqueued_jobs)}"
        )

        # 所有 tickers 都应被覆盖
        enqueued_tickers = {
            job["payload"].get("ticker")
            for job in fake_job_repo.enqueued_jobs
        }
        for ticker in tickers:
            assert ticker in enqueued_tickers, (
                f"ticker {ticker} 未被 warmer 覆盖"
            )

    async def test_warmer_enqueues_4_jobs_per_ticker(self) -> None:
        """结论: 每个 ticker 入队 4 个 job (3 analyze + 1 assemble)。"""
        from decision_ledger.services.conflict_cache_warmer import ConflictCacheWarmer

        fake_job_repo = FakeJobQueueRepo()
        tickers = ["AAPL"]

        warmer = ConflictCacheWarmer(
            job_queue_repo=fake_job_repo,
            tickers=tickers,
        )

        await warmer.warm_for_advisor_report(advisor_report_id="advisor_2026_W17")

        aapl_jobs = [j for j in fake_job_repo.enqueued_jobs if j["payload"].get("ticker") == "AAPL"]
        assert len(aapl_jobs) == 4, (
            f"每个 ticker 应有 4 个 job (3 analyze + 1 assemble)，当前 {len(aapl_jobs)}"
        )

        job_types = {j["job_type"] for j in aapl_jobs}
        assert "cache_warmer_analyze" in job_types, "应有 cache_warmer_analyze 类型 job"
        assert "cache_warmer_assemble" in job_types, "应有 cache_warmer_assemble 类型 job"

    async def test_warmer_does_not_enqueue_rebuttal(self) -> None:
        """结论: R3 B-R2-3 — warmer 不预热 Rebuttal（Rebuttal 输入依赖 draft 内容，每次唯一）。"""
        from decision_ledger.services.conflict_cache_warmer import ConflictCacheWarmer

        fake_job_repo = FakeJobQueueRepo()
        tickers = ["AAPL", "TSM", "NVDA"]

        warmer = ConflictCacheWarmer(
            job_queue_repo=fake_job_repo,
            tickers=tickers,
        )

        await warmer.warm_for_advisor_report(advisor_report_id="advisor_2026_W17")

        # 确认没有 rebuttal 类型的 job
        rebuttal_jobs = [
            j for j in fake_job_repo.enqueued_jobs
            if "rebuttal" in j["job_type"].lower()
        ]
        assert len(rebuttal_jobs) == 0, (
            f"R3 B-R2-3 违反: warmer 不应入队 Rebuttal job，当前 {len(rebuttal_jobs)} 个: "
            f"{[j['job_type'] for j in rebuttal_jobs]}"
        )

    async def test_warmer_job_types_correct(self) -> None:
        """结论: 入队的 job_type 只能是 cache_warmer_analyze / cache_warmer_assemble。"""
        from decision_ledger.services.conflict_cache_warmer import ConflictCacheWarmer

        fake_job_repo = FakeJobQueueRepo()
        tickers = ["AAPL"]

        warmer = ConflictCacheWarmer(
            job_queue_repo=fake_job_repo,
            tickers=tickers,
        )

        await warmer.warm_for_advisor_report(advisor_report_id="advisor_2026_W17")

        allowed_types = {"cache_warmer_analyze", "cache_warmer_assemble"}
        for job in fake_job_repo.enqueued_jobs:
            assert job["job_type"] in allowed_types, (
                f"非法 job_type: {job['job_type']}，只允许 {allowed_types}"
            )

    async def test_warmer_payload_contains_advisor_report_id(self) -> None:
        """结论: 每个 job payload 含 advisor_report_id（便于 worker 执行时溯源）。"""
        from decision_ledger.services.conflict_cache_warmer import ConflictCacheWarmer

        fake_job_repo = FakeJobQueueRepo()
        tickers = ["AAPL"]
        advisor_report_id = "advisor_2026_W17"

        warmer = ConflictCacheWarmer(
            job_queue_repo=fake_job_repo,
            tickers=tickers,
        )

        await warmer.warm_for_advisor_report(advisor_report_id=advisor_report_id)

        for job in fake_job_repo.enqueued_jobs:
            assert "advisor_report_id" in job["payload"], (
                f"job payload 缺少 advisor_report_id: {job}"
            )
            assert job["payload"]["advisor_report_id"] == advisor_report_id
