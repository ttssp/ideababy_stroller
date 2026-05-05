"""
EnvSnapshot — 决策当时的不可变环境快照
结论: frozen pydantic model，记录价格/持仓/咨询师周报 ID
细节:
  - price / holdings_pct / holdings_abs 均可空 (v0.1 human 录入，Proxyman 可能未同步)
  - advisor_week_id 关联当周 AdvisorReport
  - snapshot_at 是 UTC datetime，存储为 ISO 字符串
"""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class EnvSnapshot(BaseModel):
    """决策录入时刻的环境快照，一旦创建不可变。"""

    model_config = ConfigDict(frozen=True)

    # price 可空: v0.1 human 手填, 可在 post-mortem 回填
    price: float | None
    # 该 ticker 占组合比例 (0.0-1.0 表示百分比, e.g. 0.05 = 5%)
    holdings_pct: float | None
    # 绝对持仓金额 (USD)
    holdings_abs: float | None
    # 关联到当周 AdvisorReport 的 ID (week_id 格式: "2026-W17")
    advisor_week_id: str | None
    # 快照时间 (UTC)
    snapshot_at: datetime
