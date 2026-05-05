"""
ConflictReport 域模型 — T002
结论: 三路 signals 聚合后的冲突报告，由 ConflictReportAssembler 中立产出
细节:
  - signals: 至少 3 条 (不变量 #2，即使有 confidence=0.0 的 no_view 也计入)
  - 严禁含 priority / winner / recommended 字段 (R10 红线，不变量 #9)
  - rendered_order_seed: hash(sources + day) % N，UI 据此随机化三列顺序 (R2 D22)
  - divergence_root_cause: 白话根因，必须非空 (无分歧时写 "暂无分歧")
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, field_validator

from decision_ledger.domain.strategy_signal import StrategySignal


class ConflictReport(BaseModel):
    """三路 signals 聚合后的冲突报告 — 由 ConflictReportAssembler 中立产出。

    R10 红线: 永远无 priority / winner / recommended 字段。
    不变量 #2: signals 始终 ≥ 3 条。
    R2 D22: rendered_order_seed 驱动 UI 三列随机顺序。
    """

    model_config = ConfigDict(frozen=True)

    signals: list[StrategySignal]   # 至少 3 条 (不变量 #2)
    divergence_root_cause: str      # 白话根因，"暂无分歧" 也必须写
    has_divergence: bool
    rendered_order_seed: int        # hash(sources + day) % N，R2 D22

    # 注意: 不能有 priority / winner / recommended 字段 (R10 红线)

    @field_validator("signals")
    @classmethod
    def _validate_signals_minimum(cls, v: list[StrategySignal]) -> list[StrategySignal]:
        """结论: signals 必须至少 3 条 (不变量 #2 架构红线)。"""
        if len(v) < 3:
            raise ValueError(
                f"ConflictReport.signals 必须至少 3 条，当前 {len(v)} 条 (不变量 #2)"
            )
        return v

    @field_validator("divergence_root_cause")
    @classmethod
    def _validate_divergence_root_cause_nonempty(cls, v: str) -> str:
        """结论: divergence_root_cause 必须非空 (无分歧时写 '暂无分歧')。"""
        if not v or not v.strip():
            raise ValueError("divergence_root_cause 不能为空，无分歧时请填 '暂无分歧'")
        return v
