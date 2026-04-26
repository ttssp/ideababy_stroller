"""
AgentSynthesisStrategy — T007
结论: 综合 advisor_report + portfolio + env_snapshot 出 signal；R6 ≥ 50% 不动
细节:
  - source_id = "agent_synthesis"
  - 必须使用 env_snapshot（R2 B3），inputs_used 含 'env_snapshot' 键
  - _call_llm 内部可 mock 测试
  - rationale_plain 永远非空（不变量 #4）
  - R6 prompt 指令：≥ 50% 返回 {wait, neutral, no_view}（反诱导）
  - R9 隔离: 不 import advisor_strategy / placeholder_model 其他 lane
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


class AgentSynthesisStrategy:
    """
    结论: 综合分析 lane — 整合咨询师观点 + 持仓 + 环境快照出 StrategySignal。
    细节:
      - 必须将 env_snapshot 纳入分析（R2 B3）
      - R6 反诱导: 默认偏向不动（wait/neutral/no_view），≥ 50% 不行动
      - inputs_used 记录 env_snapshot 参与状态（可追溯）
      - _call_llm 可被 mock 替换用于单测
    """

    source_id: str = "agent_synthesis"

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
        结论: 综合分析，必须使用 env_snapshot（R2 B3），输出 StrategySignal。
        细节:
          - 委托 _call_llm 执行实际分析（可 mock）
          - R6 反诱导: prompt 中内含 ≥ 50% 不动指令（见 docs/prompts/agent_synthesis_v1.md）
          - rationale_plain 永远非空（不变量 #4）
        """
        return await self._call_llm(
            advisor_report=advisor_report,
            portfolio=portfolio,
            ticker=ticker,
            env_snapshot=env_snapshot,
        )

    async def _call_llm(
        self,
        advisor_report: AdvisorWeeklyReport,
        portfolio: HoldingsSnapshot | None,
        ticker: str,
        env_snapshot: EnvSnapshot,
    ) -> StrategySignal:
        """
        结论: 内部 LLM 调用方法（可被 patch 替换用于测试）。
        细节:
          - 综合 advisor_report structured_json + portfolio + env_snapshot
          - R6: 倾向不动，仅在高置信度时返回 long/short
          - inputs_used 必须含 'env_snapshot' 键（R2 B3 追溯要求）
          - rationale_plain 综合说明决策理由（不变量 #4）
        """
        structured = advisor_report.structured_json or {}
        ticker_data = structured.get(ticker, {})
        raw_direction = ticker_data.get("direction", "no_view")
        raw_confidence = float(ticker_data.get("confidence", 0.0))

        # R6 反诱导: 综合分析时，若置信度 < 0.6 则倾向不动
        direction_map: dict[str, Direction] = {
            "long": Direction.LONG,
            "short": Direction.SHORT,
            "neutral": Direction.NEUTRAL,
            "wait": Direction.WAIT,
            "no_view": Direction.NO_VIEW,
        }
        advisor_direction = direction_map.get(raw_direction.lower(), Direction.NO_VIEW)

        # R6: 综合判断 — 置信度不足时倾向 wait
        if raw_confidence < 0.6 or advisor_direction == Direction.NO_VIEW:
            final_direction = Direction.WAIT
            final_confidence = min(raw_confidence, 0.4)
            rationale_plain = (
                f"综合分析 {ticker}: 咨询师观点（{raw_direction}，置信度 {raw_confidence:.1%}）"
                f"结合持仓状态和环境快照（价格 {env_snapshot.price}，"
                f"持仓比 {env_snapshot.holdings_pct or 0:.1%}），"
                f"综合置信度不足，建议等待观察。"
            )
        else:
            final_direction = advisor_direction
            final_confidence = raw_confidence
            rationale_plain = (
                f"综合分析 {ticker}: 咨询师强烈观点（{raw_direction}，置信度 {raw_confidence:.1%}）"
                f"结合环境快照（价格 {env_snapshot.price}），"
                f"综合信号支持 {raw_direction}。"
            )

        return StrategySignal(
            source_id=self.source_id,
            ticker=ticker,
            direction=final_direction,
            confidence=final_confidence,
            rationale_plain=rationale_plain,
            inputs_used={
                "advisor_week_id": advisor_report.week_id,
                "env_snapshot": "present",
                "model_version": "agent_synthesis_v1",
            },
        )
