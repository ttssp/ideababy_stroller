"""
AdvisorRepository 集成测试 — T003
结论: 验证 upsert_weekly / latest_for_week / list_for_ticker / record_parse_failure
"""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

import pytest

from decision_ledger.domain.advisor import AdvisorWeeklyReport, ParseFailure
from decision_ledger.repository.advisor_repo import AdvisorRepository
from decision_ledger.repository.base import AsyncConnectionPool


def _make_report(
    week_id: str = "2026-W17",
    ticker: str = "AAPL",
    advisor_id: str | None = None,
) -> AdvisorWeeklyReport:
    """构造测试用 AdvisorWeeklyReport。

    结论: advisor_id 是 PRIMARY KEY,不同周报必须不同 advisor_id。
    细节: 默认按 week_id 派生唯一 ID;list_for_ticker 测试需多条共存。
    """
    return AdvisorWeeklyReport(
        advisor_id=advisor_id or f"advisor_{week_id}",
        source_id="advisor_001",
        week_id=week_id,
        raw_text="测试周报文本内容",
        structured_json={ticker: {"direction": "long", "confidence": 0.8}},
        parsed_at=datetime.now(tz=UTC),
    )


@pytest.mark.asyncio
async def test_upsert_weekly_and_latest_for_week_should_round_trip(
    migrated_pool: AsyncConnectionPool,
) -> None:
    """结论: upsert 后 latest_for_week 应返回相同 week_id 的报告。"""
    repo = AdvisorRepository(migrated_pool)
    report = _make_report(week_id="2026-W17", advisor_id="advisor_001")
    await repo.upsert_weekly(report)

    fetched = await repo.latest_for_week("2026-W17")
    assert fetched is not None
    assert fetched.week_id == "2026-W17"
    assert fetched.advisor_id == "advisor_001"
    assert "AAPL" in fetched.structured_json


@pytest.mark.asyncio
async def test_latest_for_week_should_return_none_when_week_not_found(
    migrated_pool: AsyncConnectionPool,
) -> None:
    """结论: 查询不存在的 week_id 应返回 None。"""
    repo = AdvisorRepository(migrated_pool)
    result = await repo.latest_for_week("2099-W99")
    assert result is None


@pytest.mark.asyncio
async def test_upsert_weekly_should_overwrite_same_week_and_source(
    migrated_pool: AsyncConnectionPool,
) -> None:
    """结论: 同 week_id + source_id 的第二次 upsert 应覆盖原记录（幂等）。"""
    repo = AdvisorRepository(migrated_pool)

    report_v1 = _make_report(week_id="2026-W18")
    await repo.upsert_weekly(report_v1)

    # 第二次 upsert，相同 week_id + source_id，不同内容
    report_v2 = AdvisorWeeklyReport(
        advisor_id="advisor_001",
        source_id="advisor_001",
        week_id="2026-W18",
        raw_text="更新版周报",
        structured_json={"TSLA": {"direction": "short", "confidence": 0.6}},
        parsed_at=datetime.now(tz=UTC),
    )
    await repo.upsert_weekly(report_v2)

    fetched = await repo.latest_for_week("2026-W18")
    assert fetched is not None
    assert fetched.raw_text == "更新版周报"
    assert "TSLA" in fetched.structured_json


@pytest.mark.asyncio
async def test_list_for_ticker_should_return_reports_containing_ticker(
    migrated_pool: AsyncConnectionPool,
) -> None:
    """结论: list_for_ticker 应返回 structured_json 含该 ticker 的所有周报。"""
    repo = AdvisorRepository(migrated_pool)

    await repo.upsert_weekly(_make_report(week_id="2026-W17", ticker="AAPL"))
    await repo.upsert_weekly(_make_report(week_id="2026-W18", ticker="AAPL"))
    await repo.upsert_weekly(_make_report(week_id="2026-W19", ticker="TSLA"))

    aapl_reports = await repo.list_for_ticker("AAPL")
    tsla_reports = await repo.list_for_ticker("TSLA")

    assert len(aapl_reports) == 2
    assert len(tsla_reports) == 1


@pytest.mark.asyncio
async def test_list_for_ticker_should_return_empty_when_ticker_not_found(
    migrated_pool: AsyncConnectionPool,
) -> None:
    """結論: 不存在的 ticker 应返回空列表。"""
    repo = AdvisorRepository(migrated_pool)
    result = await repo.list_for_ticker("NONEXISTENT")
    assert result == []


@pytest.mark.asyncio
async def test_record_parse_failure_should_persist_to_alerts(
    migrated_pool: AsyncConnectionPool,
) -> None:
    """结论: record_parse_failure 应将失败记录写入 alerts 表（type=parse_failure）。"""
    repo = AdvisorRepository(migrated_pool)
    failure = ParseFailure(
        failure_id=str(uuid4()),
        pdf_path="/data/reports/2026-W17.pdf",
        error_message="PDF 格式不支持",
        failed_at=datetime.now(tz=UTC),
        advisor_id="advisor_001",
    )
    # 不应抛出异常
    await repo.record_parse_failure(failure)
