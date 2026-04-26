"""
StrategyModule IDL — T007
结论: Protocol + SourceDataProvider 接口定义，架构枢纽（architecture.md §3.1）
细节:
  - StrategyModule: 仅 source_id + analyze，**不含** conflict_resolve / devil_advocate
    （IDL 锁死，TECH-4）
  - SourceDataProvider: 只读数据接口，**不暴露** registry / 其他 lane（R3 contract-level 隔离）
  - constructor 强制仅接受 (LLMClient, SourceDataProvider)，不接受 registry（不变量 #14）
  - @runtime_checkable 支持 isinstance 检查（D7 扩展位）
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, runtime_checkable

if TYPE_CHECKING:
    from decision_ledger.domain.advisor import AdvisorWeeklyReport
    from decision_ledger.domain.env_snapshot import EnvSnapshot
    from decision_ledger.domain.portfolio import HoldingsSnapshot
    from decision_ledger.domain.strategy_signal import StrategySignal
    from decision_ledger.llm.client import LLMClient


@runtime_checkable
class SourceDataProvider(Protocol):
    """
    R3 新增: lane 唯一可读的数据来源接口（只读，不暴露其他 lane）。

    结论:
      - 所有方法均返回不可变 dataclass 或 None
      - 接口名称**不含** 'lane' / 'strategy' / 'module' / 'signal'（R3 不变量）
      - 不暴露 registry / list[StrategyModule] / 其他 lane 实例

    细节:
      - get_advisor_report: 按 advisor_week_id 查询咨询师周报
      - get_portfolio: 查询最新持仓快照
      - get_ticker_meta: 查询 ticker 元信息（如关注股列表）
      - get_env_snapshot: 查询最新环境快照
    """

    async def get_advisor_report(self, advisor_week_id: str) -> AdvisorWeeklyReport | None:
        """按 week_id 查询咨询师周报。返回 None 表示本周尚无数据。"""
        ...

    async def get_portfolio(self) -> HoldingsSnapshot | None:
        """查询最新持仓快照。返回 None 表示无持仓数据。"""
        ...

    async def get_ticker_meta(self, ticker: str) -> dict[str, str]:
        """查询 ticker 元信息（market, display_name 等）。"""
        ...

    async def get_env_snapshot(self) -> EnvSnapshot | None:
        """查询最新环境快照。返回 None 表示无快照。"""
        ...


@runtime_checkable
class StrategyModule(Protocol):
    """
    所有策略源实现此接口（R2 修订，仅 analyze）。

    结论:
      - 单一职责: (advisor_report, portfolio, ticker, env_snapshot) → StrategySignal
      - IDL 锁死: 仅 source_id + analyze，**不含** conflict_resolve / devil_advocate（TECH-4）
      - R3 contract-level 隔离: __init__ 仅接受 (LLMClient, SourceDataProvider)
        不接受 registry / 其他 lane / list[StrategyModule]

    细节:
      - source_id: lane 唯一标识符（"advisor" | "placeholder_model" | "agent_synthesis"）
      - analyze: 输入四元组 → StrategySignal，必须填充 rationale_plain（不变量 #4）
      - env_snapshot 是 analyze 签名必须参数（R2 B3 修复）
    """

    source_id: str = ""  # Protocol 约束: 每个 lane 必须提供 source_id 值

    def __init__(
        self,
        llm_client: LLMClient,
        source_data_provider: SourceDataProvider,
    ) -> None:
        """
        R3 contract-level 隔离: 仅接受 (llm_client, source_data_provider)。
        不接受 registry, 不接受其他 lane 实例, 不接受 list[StrategyModule]。
        通过 inspect.signature runtime test (T007) 验证。
        """
        ...

    async def analyze(
        self,
        advisor_report: AdvisorWeeklyReport,
        portfolio: HoldingsSnapshot | None,
        ticker: str,
        env_snapshot: EnvSnapshot,
    ) -> StrategySignal:
        """
        分析并输出 StrategySignal。

        Args:
            advisor_report: 本周咨询师周报（不可变）
            portfolio: 最新持仓快照（可为 None）
            ticker: 分析标的
            env_snapshot: 当前环境快照（R2 B3 必须参数）

        Returns:
            StrategySignal（rationale_plain 必须非空，不变量 #4）
        """
        ...


class CustomStrategyModule(StrategyModule):
    """
    v0.5+ 扩展位（D7）。

    结论: human 未来插入私有 ML 模型用。继承 IDL 接口（analyze 单一方法），实现细节由 human 自由。
    细节:
      - 仅作为 ABC 基类使用，source_id 由子类覆写
      - 接口约束同 StrategyModule（analyze + source_id）
    """

    source_id: str = "custom_v1"  # human 自定义，子类应覆写

    def __init__(
        self,
        llm_client: LLMClient,
        source_data_provider: SourceDataProvider,
    ) -> None:
        """继承 StrategyModule constructor 约束。"""
        ...

    async def analyze(
        self,
        advisor_report: AdvisorWeeklyReport,
        portfolio: HoldingsSnapshot | None,
        ticker: str,
        env_snapshot: EnvSnapshot,
    ) -> StrategySignal:
        """子类必须覆写此方法。"""
        raise NotImplementedError("CustomStrategyModule 子类必须实现 analyze()")
