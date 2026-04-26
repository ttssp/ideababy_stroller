"""
DevilAdvocateService — T013
结论: 独立反驳服务, draft 阶段同步生成一句话反方意见
细节:
  - R2 修订: 不是 StrategyModule lane, 不实现 source_id / analyze
  - R3 修订 B-R2-3: fast-path 配置
      model=claude-sonnet-4-6, cache 绕过 (nonce), asyncio.wait_for timeout=3.0s
  - §9.4 不变量: rebuttal_text 非空 (由 Rebuttal pydantic validator 保证)
  - R6 合规: prompt 无红线词 (见 docs/prompts/devil_advocate_v1.md)
"""

from __future__ import annotations

import asyncio
import logging
import uuid
from typing import Any, cast

from decision_ledger.domain.decision_draft import DecisionDraft
from decision_ledger.domain.env_snapshot import EnvSnapshot
from decision_ledger.domain.rebuttal import Rebuttal

logger = logging.getLogger(__name__)

# R3 fast-path: Rebuttal 不可缓存 (输入唯一 every draft) → 每次唯一 nonce
# R3 fast-path: model = Sonnet 4.6, 不降 Haiku (质量风险)
_FAST_PATH_MODEL = "claude-sonnet-4-6"

# R3 D21: rebuttal 单点超时 3s → TimeoutError, 由 T008 整体 5s timeout 兜底
_GENERATE_TIMEOUT_S = 3.0

# T013 prompt 模板 (≤ 200 token 上下文, 无 few-shot, R3 fast-path)
# 完整文档: docs/prompts/devil_advocate_v1.md
_PROMPT_TEMPLATE = "\n".join([
    "你是一位严格的风险审查员。请对以下投资意向给出一句话反方意见（<=80字），",
    "开头必须包含'考虑反方'四字。",
    "",
    "标的: {ticker}",
    "当前意向: {intended_action}",
    "理由摘要: {draft_reason}",
    "市场背景: 价格 {price}，持仓比例 {holdings_pct}",
    "",
    "要求:",
    "- 仅输出反驳，不加前缀",
    "- <=80字",
    "- 考虑反方的视角出发，指出潜在风险或盲点",
    "- 不评价对错，不做裁判",
])


class DevilAdvocateService:
    """
    独立反驳服务 (R2 D23). 不是 StrategyModule. 不读 lane 状态.
    R3 修订: fast-path 配置 (B-R2-3, Rebuttal 不可缓存).

    职责: 在 draft 阶段 (asyncio.gather 并发) 同步生成一句话反方意见.
    调用方: T008 DecisionRecorder.create_draft (asyncio.gather 并发).
    """

    # 注意: 没有 source_id, 没有 analyze() — R2 修订不是 StrategyModule

    def __init__(self, llm_client: Any, rebuttal_repo: Any) -> None:
        """
        Args:
            llm_client: T005 LLMClient 实例 (或 mock)
            rebuttal_repo: T003 RebuttalRepository 实例 (或 mock)
        """
        self._llm_client = llm_client
        self._rebuttal_repo = rebuttal_repo

    async def generate(
        self,
        *,
        decision_draft: DecisionDraft | None = None,
        ticker: str | None = None,
        env_snapshot: EnvSnapshot,
    ) -> Rebuttal:
        """
        生成一句话反方意见, 写入 RebuttalRepository.

        R3 fast-path 配置 (B-R2-3):
          - model: claude-sonnet-4-6 (不降 Haiku)
          - nonce in cache_key_extras: 保证每次 cache miss (等价 cache_lookup=False)
          - asyncio.wait_for timeout=3.0s: 单点 ≤ 3s 上限

        支持两种调用方式 (T008 兼容):
          - generate(ticker="TSM", env_snapshot=...)  — T008 风格
          - generate(decision_draft=draft, env_snapshot=...)  — T013 spec 风格

        Returns:
            Rebuttal 对象 (rebuttal_text 非空 ≤ 80 字, §9.4 不变量)

        Raises:
            TimeoutError: LLM 调用超过 3s (asyncio.wait_for)
            LLMSchemaError: LLM 返回数据不符合 Rebuttal schema (SEC-4)
            ValueError: rebuttal_text 为空或超 80 字 (§9.4)
        """
        # 提取 ticker — 从 decision_draft 或直接参数
        if decision_draft is not None:
            effective_ticker = decision_draft.ticker
            draft_reason = decision_draft.draft_reason
            intended_action = decision_draft.intended_action.value
        elif ticker is not None:
            effective_ticker = ticker
            draft_reason = "—"
            intended_action = "—"
        else:
            raise ValueError("generate() 必须提供 ticker 或 decision_draft 之一")

        # 渲染 prompt (≤ 200 token 上下文, R3 fast-path)
        prompt = _PROMPT_TEMPLATE.format(
            ticker=effective_ticker,
            intended_action=intended_action,
            draft_reason=draft_reason,
            price=env_snapshot.price,
            holdings_pct=f"{env_snapshot.holdings_pct:.1%}",
        )

        # R3 B-R2-3: 每次唯一 nonce → 保证 cache miss (等价 cache_lookup=False)
        nonce = str(uuid.uuid4())

        # R3 D21: asyncio.wait_for 强制 3s timeout
        try:
            rebuttal = cast(
                Rebuttal,
                await asyncio.wait_for(
                    self._llm_client.call(
                        prompt=prompt,
                        template_version="devil_advocate_v1",
                        cache_key_extras={
                            "ticker": effective_ticker,
                            "advisor_week_id": env_snapshot.advisor_week_id,
                            "nonce": nonce,  # R3: cache bypass
                        },
                        schema=Rebuttal,
                        model=_FAST_PATH_MODEL,  # R3: claude-sonnet-4-6
                    ),
                    timeout=_GENERATE_TIMEOUT_S,
                ),
            )
        except TimeoutError as e:
            logger.warning(
                "DevilAdvocateService.generate timeout (>%.1fs): ticker=%s",
                _GENERATE_TIMEOUT_S,
                effective_ticker,
            )
            raise TimeoutError(
                f"rebuttal 生成超时 (>{_GENERATE_TIMEOUT_S}s): ticker={effective_ticker}"
            ) from e

        # §9.4 不变量: rebuttal_text 非空 + ≤ 80 字 (Rebuttal pydantic validator 已保证)
        # 此处 LLMClient.call 已通过 schema=Rebuttal 做了 tool use + pydantic validate
        # 若 validator 失败 → LLMSchemaError 上抛 (不在此 catch)

        # 写入 RebuttalRepository
        rebuttal_id = str(uuid.uuid4())
        await self._rebuttal_repo.insert(rebuttal_id, rebuttal)
        logger.debug(
            "DevilAdvocateService: rebuttal 已写入 repo (id=%s, ticker=%s)",
            rebuttal_id,
            effective_ticker,
        )

        return rebuttal
