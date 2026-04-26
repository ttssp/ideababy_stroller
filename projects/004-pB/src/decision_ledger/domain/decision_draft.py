"""
DecisionDraft 域模型 — T002 R2 新增
结论: draft/commit 双阶段录入的中间态模型 (R2 D8/D13)
细节:
  - DraftStatus: draft/committed/abandoned (与 DecisionStatus 语义相同，独立定义便于类型明确)
  - draft_reason: ≤ 80 char，与 Decision.reason 同等约束
  - conflict_report_ref / devils_rebuttal_ref: INSERT 时可 NULL，asyncio.gather 完成后填入
  - committed_at / abandoned_at: 状态转换时间戳
"""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, field_validator

from decision_ledger.domain.decision import Action
from decision_ledger.domain.env_snapshot import EnvSnapshot


class DraftStatus(StrEnum):
    """草稿状态枚举 — R2 D8/D13 规定。"""

    DRAFT = "draft"          # 初始状态，等待 asyncio.gather 完成
    COMMITTED = "committed"  # commit endpoint 写入后
    ABANDONED = "abandoned"  # 30min GC 或 human 主动放弃


class DecisionDraft(BaseModel):
    """Pre-commit 临时草稿 — R2 新增。

    生命周期:
      1. POST /decisions/draft → INSERT status='draft', refs=NULL
      2. asyncio.gather 完成 → UPDATE refs
      3. POST /decisions/{draft_id}/commit → status='committed'
      4. 30min 超时 GC → status='abandoned'
    """

    model_config = ConfigDict(frozen=True)

    draft_id: str                              # UUID 字符串
    ticker: str
    intended_action: Action                    # 可在 commit 时改为 final_action
    draft_reason: str                          # ≤ 80 char，可在 commit 时改
    env_snapshot: EnvSnapshot
    conflict_report_ref: str | None = None     # INSERT 时 NULL，asyncio 完成后填入
    devils_rebuttal_ref: str | None = None     # 同上
    status: DraftStatus = DraftStatus.DRAFT
    created_at: datetime = datetime.now()
    committed_at: datetime | None = None       # commit 时填入
    abandoned_at: datetime | None = None       # GC 或放弃时填入

    @field_validator("draft_reason")
    @classmethod
    def _validate_draft_reason_length(cls, v: str) -> str:
        """结论: draft_reason 不能为空且不超过 80 字符。"""
        if not v or not v.strip():
            raise ValueError("draft_reason 不能为空")
        if len(v) > 80:
            raise ValueError(f"draft_reason 不能超过 80 字符，当前 {len(v)} 字符")
        return v
