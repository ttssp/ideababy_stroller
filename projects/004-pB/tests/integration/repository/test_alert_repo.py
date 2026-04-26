"""
AlertRepository 集成测试 — T003
结论: 验证 insert / latest_active / dismiss
"""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

import pytest

from decision_ledger.domain.alert import Alert, AlertSeverity, AlertType
from decision_ledger.repository.alert_repo import AlertRepository
from decision_ledger.repository.base import AsyncConnectionPool


def _make_alert(
    alert_type: AlertType = AlertType.LOW_DECISION_RATE,
    severity: AlertSeverity = AlertSeverity.WARNING,
) -> Alert:
    """构造测试用 Alert。"""
    return Alert(
        alert_id=str(uuid4()),
        alert_type=alert_type,
        severity=severity,
        body="测试告警内容",
        created_at=datetime.now(tz=UTC),
    )


@pytest.mark.asyncio
async def test_insert_and_latest_active_should_return_active_alerts(
    migrated_pool: AsyncConnectionPool,
) -> None:
    """结论: insert 后 latest_active 应返回 dismissed_at=None 的告警。"""
    repo = AlertRepository(migrated_pool)
    alert = _make_alert()
    await repo.insert(alert)

    active = await repo.latest_active()
    assert len(active) >= 1
    ids = {a.alert_id for a in active}
    assert alert.alert_id in ids


@pytest.mark.asyncio
async def test_latest_active_should_return_empty_when_no_alerts(
    migrated_pool: AsyncConnectionPool,
) -> None:
    """结论: 无告警时 latest_active 应返回空列表。"""
    repo = AlertRepository(migrated_pool)
    result = await repo.latest_active()
    assert result == []


@pytest.mark.asyncio
async def test_dismiss_should_remove_alert_from_active(
    migrated_pool: AsyncConnectionPool,
) -> None:
    """结论: dismiss 后 latest_active 不应再包含该告警。"""
    repo = AlertRepository(migrated_pool)
    alert = _make_alert()
    await repo.insert(alert)

    await repo.dismiss(alert.alert_id)

    active = await repo.latest_active()
    ids = {a.alert_id for a in active}
    assert alert.alert_id not in ids


@pytest.mark.asyncio
async def test_dismiss_on_nonexistent_should_not_raise(
    migrated_pool: AsyncConnectionPool,
) -> None:
    """结论: dismiss 不存在的 alert_id 应静默（不抛出异常）。"""
    repo = AlertRepository(migrated_pool)
    # 不应抛出
    await repo.dismiss("nonexistent-alert-id")


@pytest.mark.asyncio
async def test_insert_alert_with_parse_failure_type_should_work(
    migrated_pool: AsyncConnectionPool,
) -> None:
    """结论: parse_failure 类型告警应正常入库（CHECK 约束验证）。"""
    repo = AlertRepository(migrated_pool)
    alert = _make_alert(alert_type=AlertType.PARSE_FAILURE, severity=AlertSeverity.WARNING)
    await repo.insert(alert)

    active = await repo.latest_active()
    ids = {a.alert_id for a in active}
    assert alert.alert_id in ids
