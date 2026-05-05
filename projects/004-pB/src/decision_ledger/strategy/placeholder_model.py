"""
PlaceholderModelStrategy — T007
结论: 占位 lane，永远返回 no_view + confidence=0.0，反对假精度（Q6）
细节:
  - source_id = "placeholder_model"
  - analyze 永远返回 Direction.NO_VIEW, confidence=0.0
  - rationale_plain 解释为何 no_view（透明度，含"占位"字样）
  - inputs_used 含 model_version（可追溯）
  - v0.5+ 替换为真实 ML 模型（D7 扩展位）
  - R9 隔离: 不 import advisor_strategy / agent_synthesis 其他 lane
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from decision_ledger.domain.strategy_signal import Direction, StrategySignal

if TYPE_CHECKING:
    from decision_ledger.domain.advisor import AdvisorWeeklyReport
    from decision_ledger.domain.env_snapshot import EnvSnapshot
    from decision_ledger.domain.portfolio import HoldingsSnapshot
    from decision_ledger.llm.client import LLMClient
    from decision_ledger.strategy.base import SourceDataProvider


class PlaceholderModelStrategy:
    """
    结论: 占位 lane — 永远 no_view，反对假精度（Q6 设计意图）。
    细节:
      - 不调 LLM，不读市场数据，保守默认假设
      - v0.5+ 由真实 ML 模型替换（D7 扩展位预留）
      - rationale_plain 明确说明这是占位实现（透明度）
    """

    source_id: str = "placeholder_model"

    def __init__(
        self,
        llm_client: LLMClient,
        source_data_provider: SourceDataProvider,
    ) -> None:
        """
        R3 contract-level 隔离: 仅接受 (llm_client, source_data_provider)。
        不接受 registry, 不接受其他 lane 实例。
        """
        self._llm = llm_client
        self._provider = source_data_provider

    async def analyze(
        self,
        advisor_report: AdvisorWeeklyReport,
        portfolio: HoldingsSnapshot | None,
        ticker: str,
        env_snapshot: EnvSnapshot,
    ) -> StrategySignal:
        """
        结论: 永远返回 no_view + confidence=0.0（Q6 反对假精度）。
        细节:
          - 不调 LLM，直接返回保守默认信号
          - rationale_plain 说明占位原因（透明度，不变量 #4）
          - v0.5+ 替换为真实 ML 模型时，此方法整体替换
        """
        return StrategySignal(
            source_id=self.source_id,
            ticker=ticker,
            direction=Direction.NO_VIEW,
            confidence=0.0,
            rationale_plain=(
                f"占位模型（placeholder_model）对 {ticker} 无观点。"
                "保守默认假设: 当前 v0.4 版本不产生 long/short 信号，"
                "真实模型将在 v0.5+ 替换此占位实现。"
            ),
            inputs_used={
                "model_version": "placeholder_model_v0",
                "ticker": ticker,
            },
        )
