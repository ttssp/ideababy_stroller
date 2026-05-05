"""
failure_alert.py — T020
结论: O10 失败告警监控 — 14 天内 committed decisions < 2 触发双通道告警
细节:
  - FailureAlertMonitor.check(): SQL count WHERE status='committed' (R2 规则)
  - < 2 时: 写入 alerts 表 + 调 Telegram bot.send_alert() (mock 直到 T017 ship)
  - 注册 APScheduler cron 0 9 * * * (每天 09:00 检查)
  - bot=None 时 graceful (T017 未 ship 前)
"""

from __future__ import annotations

import logging
import uuid
from datetime import UTC, datetime
from typing import Any

from decision_ledger.domain.alert import Alert, AlertSeverity, AlertType
from decision_ledger.repository.alert_repo import AlertRepository
from decision_ledger.repository.decision_repo import DecisionRepository

logger = logging.getLogger(__name__)

# O10: 14 天内 committed decisions 最低阈值
_LOW_DECISION_THRESHOLD = 2
_LOOKBACK_DAYS = 14


class FailureAlertMonitor:
    """O10 失败告警监控器。

    结论: 每天检查 14 天内 committed decisions 数，< 2 触发双通道告警。
    细节:
      - bot=None 时 Telegram 通道 graceful no-op (T017 ship 前)
      - 已有未 dismiss 的同类告警时，不重复写入（防 spam）
    """

    def __init__(
        self,
        decision_repo: DecisionRepository,
        alert_repo: AlertRepository,
        bot: Any | None = None,
    ) -> None:
        self._decision_repo = decision_repo
        self._alert_repo = alert_repo
        self._bot = bot

    async def check(self) -> None:
        """结论: 检查 14d 内 committed decisions，< 2 触发告警写入 + Telegram push。

        细节:
          - 幂等：已有 active LOW_DECISION_RATE 告警时不重复写入
          - bot.send_alert mock/real 均可（Duck typing）
        """
        count = await self._decision_repo.count_since(days=_LOOKBACK_DAYS)

        if count >= _LOW_DECISION_THRESHOLD:
            logger.info(
                "O10 check passed: %d committed decisions in %d days", count, _LOOKBACK_DAYS
            )
            return

        logger.warning(
            "O10 ALERT: only %d committed decisions in last %d days (threshold=%d)",
            count,
            _LOOKBACK_DAYS,
            _LOW_DECISION_THRESHOLD,
        )

        # 幂等检查：已有同类 active 告警时跳过
        active = await self._alert_repo.latest_active(limit=20)
        for existing in active:
            if existing.alert_type == AlertType.LOW_DECISION_RATE:
                logger.info("O10: active LOW_DECISION_RATE alert already exists, skipping insert")
                return

        body = (
            f"连续 2 周决策档案 < 2 条 = 红色告警。"
            f"当前 {_LOOKBACK_DAYS} 天内仅 {count} 条 committed 决策。"
            f"运行 `scripts/toggle_b_lite.py engage` 进入 B-lite 降级，"
            f"或参考 docs/runbooks/b_lite.md"
        )
        alert = Alert(
            alert_id=str(uuid.uuid4()),
            alert_type=AlertType.LOW_DECISION_RATE,
            severity=AlertSeverity.CRITICAL,
            body=body,
            created_at=datetime.now(tz=UTC),
        )

        # 写入 alerts 表（通道 1: DB）
        await self._alert_repo.insert(alert)
        logger.info("O10: alert written to DB, alert_id=%s", alert.alert_id)

        # 通道 2: Telegram push（T017 ship 前 mock，ship 后自动 wire）
        if self._bot is not None:
            try:
                await self._bot.send_alert(alert)
                logger.info("O10: Telegram alert sent")
            except Exception:
                logger.exception("O10: Telegram send_alert failed (non-fatal)")
        else:
            logger.warning("O10: bot not configured, Telegram channel skipped")
