"""
Alert / MetaDecision 域模型 — T002
结论: 失败告警审计记录 + B-lite 切换决策档案
细节:
  - Alert: O10 监控触发时写入，含 severity / dismissed_at
  - MetaDecision: 元决策档案，记录 B-lite 切换，14 天 cooling-off (审计用)
  - AlertType / AlertSeverity: StrEnum，避免硬编码字符串
"""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict


class AlertType(StrEnum):
    """告警类型枚举。"""

    LOW_DECISION_RATE = "low_decision_rate"   # O10: 2 周内 committed < 2 条
    PARSE_FAILURE = "parse_failure"           # PDF 解析失败
    LLM_TIMEOUT = "llm_timeout"               # LLM 调用超时 (draft 阶段 > 5s)
    TELEGRAM_FAILURE = "telegram_failure"     # Telegram push 连续失败


class AlertSeverity(StrEnum):
    """告警严重度枚举。"""

    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


class Alert(BaseModel):
    """失败告警条目 — O10 监控触发时写入。"""

    model_config = ConfigDict(frozen=True)

    alert_id: str                         # UUID 字符串
    alert_type: AlertType
    severity: AlertSeverity
    body: str                             # 告警详情文本
    created_at: datetime = datetime.now()
    dismissed_at: datetime | None = None  # human 确认后填入


class MetaDecision(BaseModel):
    """元决策档案 — B-lite 切换记录，14 天 cooling-off (审计用)。"""

    model_config = ConfigDict(frozen=True)

    meta_id: str              # UUID 字符串
    decision_type: str        # "engage_b_lite" | "exit_b_lite" | "custom"
    reason: str               # 切换原因
    created_at: datetime = datetime.now()
    cooling_off_until: datetime | None = None  # 14 天 cooling-off 截止时间
