"""
Decision 域模型 — T002
结论: pydantic v2 模型，含 Action / DecisionStatus StrEnum + 关键 validators
细节:
  - Action: buy/sell/hold/wait (架构不变量 #3，永远含 hold+wait)
  - DecisionStatus: draft/committed/abandoned (R2 D8)
  - reason: ≤ 80 char check (T002 schema constraint)
  - would_have_acted_without_agent: bool, NOT NULL 无默认 (R2 M1)
  - PostMortem: 子模型，v0.1 可空，post-mortem 回填用
"""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, field_validator

from decision_ledger.domain.env_snapshot import EnvSnapshot


class Action(StrEnum):
    """决策动作枚举 — 不变量 #3: 永远含 hold + wait。"""

    BUY = "buy"
    SELL = "sell"
    HOLD = "hold"   # 已持有 → 继续持有
    WAIT = "wait"   # 未持有 → 等待入场/观望


class DecisionStatus(StrEnum):
    """决策状态枚举 — R2 D8 新增。"""

    DRAFT = "draft"          # pre-commit 中间态
    COMMITTED = "committed"  # 已提交入档
    ABANDONED = "abandoned"  # 30min 未提交 GC 或 human 弃用


class PostMortem(BaseModel):
    """决策后回顾子模型 — v0.1 可为空，N 天后回填。"""

    executed_at: datetime | None = None
    result_pct_after_7d: float | None = None
    result_pct_after_30d: float | None = None
    retrospective_notes: str | None = None


class Decision(BaseModel):
    """决策档案单条条目 — 核心域对象。

    R2 修订:
      - status 字段 (DecisionStatus)
      - would_have_acted_without_agent: bool NOT NULL (M1)
      - conflict_report_ref / devils_rebuttal_ref 必填 (draft 阶段即生成)
    """

    model_config = ConfigDict(frozen=True)

    trade_id: str                          # UUID 字符串
    ticker: str
    action: Action
    reason: str                            # ≤ 80 char，UI + schema 双重校验
    pre_commit_at: datetime
    env_snapshot: EnvSnapshot
    conflict_report_ref: str               # R2: 必填
    devils_rebuttal_ref: str               # R2: 必填
    post_mortem: PostMortem | None = None
    would_have_acted_without_agent: bool   # R2 M1: NOT NULL 无默认
    status: DecisionStatus = DecisionStatus.COMMITTED

    @field_validator("reason")
    @classmethod
    def _validate_reason_length(cls, v: str) -> str:
        """结论: reason 不能为空且不超过 80 字符 (T002 schema check constraint)。"""
        if not v or not v.strip():
            raise ValueError("reason 不能为空")
        if len(v) > 80:
            raise ValueError(f"reason 不能超过 80 字符，当前 {len(v)} 字符")
        return v
