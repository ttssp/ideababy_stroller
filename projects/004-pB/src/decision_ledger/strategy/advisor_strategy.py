"""
AdvisorStrategy — T007
结论: 咨询师观点 lane，按 structured_json 中的 ticker 决策，无观点时返回 no_view
细节:
  - source_id = "advisor"
  - 若 ticker 不在 structured_json 中，直接返回 no_view + confidence=0.0（不调 LLM）
  - 若有观点，调 _call_llm 生成 StrategySignal（LLM 可被 patch 测试）
  - rationale_plain 永远非空（不变量 #4）
  - inputs_used 含 advisor_week_id（可追溯）
  - R9 隔离: 不 import advisor_strategy / placeholder_model / agent_synthesis 其他 lane
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


class AdvisorStrategy:
    """
    结论: 咨询师观点 lane — 读取周报 structured_json 生成 StrategySignal。
    细节:
      - 有观点: 委托 _call_llm 出 StrategySignal（可 mock 测试）
      - 无观点: 直接返回 no_view，confidence=0.0，rationale_plain 说明原因
    """

    source_id: str = "advisor"

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
        结论: 按咨询师周报生成 StrategySignal。
        细节:
          - 若 ticker 不在 structured_json 中，返回 no_view（不调 LLM，节省 token）
          - 若有观点，委托 _call_llm 解析并生成 StrategySignal
          - rationale_plain 必须非空（不变量 #4）
        """
        structured = advisor_report.structured_json or {}
        if ticker not in structured:
            # 无观点直接返回，不调 LLM
            return StrategySignal(
                source_id=self.source_id,
                ticker=ticker,
                direction=Direction.NO_VIEW,
                confidence=0.0,
                rationale_plain=(
                    f"咨询师本周（{advisor_report.week_id}）对 {ticker} 无评论，"
                    "无观点不产生信号。"
                ),
                inputs_used={
                    "advisor_week_id": advisor_report.week_id,
                    "model_version": "advisor_strategy_v1",
                },
            )

        # 有观点，委托 LLM 生成
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
          - 提取 structured_json 中 ticker 的结构化数据
          - 调用 LLM client 生成 StrategySignal
          - 如 LLM 返回无效，退化为 no_view（防御性编程）
        """
        structured = advisor_report.structured_json or {}
        ticker_data = structured.get(ticker, {})
        raw_direction = ticker_data.get("direction", "no_view")
        raw_confidence = float(ticker_data.get("confidence", 0.0))
        raw_rationale = ticker_data.get("rationale", "")

        # 映射 direction 字符串到 Direction enum
        direction_map: dict[str, Direction] = {
            "long": Direction.LONG,
            "short": Direction.SHORT,
            "neutral": Direction.NEUTRAL,
            "wait": Direction.WAIT,
            "no_view": Direction.NO_VIEW,
        }
        direction = direction_map.get(raw_direction.lower(), Direction.NO_VIEW)

        # 构建 rationale_plain（不变量 #4: 永远非空）
        if raw_rationale:
            rationale_plain = (
                f"咨询师对 {ticker} 的观点: {raw_direction}（置信度 {raw_confidence:.1%}）。"
                f"理由: {raw_rationale}"
            )
        else:
            rationale_plain = (
                f"咨询师对 {ticker} 的观点: {raw_direction}（置信度 {raw_confidence:.1%}）。"
                f"本周报（{advisor_report.week_id}）无详细理由说明。"
            )

        return StrategySignal(
            source_id=self.source_id,
            ticker=ticker,
            direction=direction,
            confidence=raw_confidence,
            rationale_plain=rationale_plain,
            inputs_used={
                "advisor_week_id": advisor_report.week_id,
                "model_version": "advisor_strategy_v1",
            },
        )
