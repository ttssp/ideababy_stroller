"""
DevilAdvocateService — T013
结论: 独立反驳服务, draft 阶段同步生成一句话反方意见
细节:
  - R2 修订: 不是 StrategyModule lane, 不实现 source_id / analyze
  - R3 修订 B-R2-3: fast-path 配置
      model=claude-sonnet-4-6, cache 绕过 (cache_lookup=False), asyncio.wait_for timeout=3.0s
  - §9.4 不变量: rebuttal_text 非空 (由 Rebuttal pydantic validator 保证)
  - R6 合规: prompt 无红线词 (见 docs/prompts/devil_advocate_v1.md)
  - F2-T013: prompt 模板从 docs/prompts/devil_advocate_v1.md 单一来源加载
"""

from __future__ import annotations

import asyncio
import logging
import uuid
from pathlib import Path
from typing import Any, cast

from decision_ledger.domain.decision_draft import DecisionDraft
from decision_ledger.domain.env_snapshot import EnvSnapshot
from decision_ledger.domain.rebuttal import Rebuttal

logger = logging.getLogger(__name__)

# R3 fast-path 配置 (D21 + B-R2-3, 与 spec T013 第 73-80 行一致):
# - model = Sonnet 4.6, 不降 Haiku (allow_fallback=False, 质量风险禁令)
# - max_tokens = 100 (反 over-explanation, ≤ 80 字)
# - temperature = 0.3 (低随机性)
# - cache_lookup = False (Rebuttal 不可缓存)
# - timeout_seconds = 3.0 (单点硬上限, T008 5s 兜底)
_FAST_PATH_MODEL = "claude-sonnet-4-6"
_FAST_PATH_MAX_TOKENS = 100
_FAST_PATH_TEMPERATURE = 0.3
_FAST_PATH_CACHE_LOOKUP = False
_FAST_PATH_ALLOW_FALLBACK = False
_GENERATE_TIMEOUT_S = 3.0

# 用户输入字段长度上限 (反 prompt injection + 控 prompt token 数)
_MAX_DRAFT_REASON_CHARS = 200

# F2-T013: prompt 单一来源 — docs/prompts/devil_advocate_v1.md
# 不再在 Python 文件里维护 prompt 字面量, 避免 .md / .py 双向漂移导致的
# R6 红线词审计盲区。
_PROMPT_DOC_PATH = (
    Path(__file__).resolve().parents[3]
    / "docs"
    / "prompts"
    / "devil_advocate_v1.md"
)
_PROMPT_BEGIN_MARKER = "\n<!-- PROMPT_BEGIN -->\n"
_PROMPT_END_MARKER = "\n<!-- PROMPT_END -->\n"


def _load_prompt_template() -> str:
    """从 docs/prompts/devil_advocate_v1.md 提取 PROMPT_BEGIN/END 之间的模板。

    F2-T013: 模板在 .md 中维护, 与 R6 合规说明同文件. 单一来源避免漂移。
    标记必须独立成行 (前后换行), 避免散文里 inline 引用同一字符串造成误匹配。
    """
    if not _PROMPT_DOC_PATH.is_file():
        raise FileNotFoundError(
            f"devil_advocate prompt 文档缺失: {_PROMPT_DOC_PATH}"
        )
    text = _PROMPT_DOC_PATH.read_text(encoding="utf-8")
    begin = text.find(_PROMPT_BEGIN_MARKER)
    end = text.find(_PROMPT_END_MARKER)
    if begin < 0 or end < 0 or end <= begin:
        raise ValueError(
            f"devil_advocate prompt 文档缺少 BEGIN/END 行内标记: {_PROMPT_DOC_PATH}"
        )
    raw = text[begin + len(_PROMPT_BEGIN_MARKER) : end]
    return raw.strip("\n")


# import 期一次性加载, 模板不可变 (R3 fast-path 不允许运行期改 prompt)
_PROMPT_TEMPLATE = _load_prompt_template()


def _sanitize_user_text(text: str, max_chars: int = _MAX_DRAFT_REASON_CHARS) -> str:
    """清洗用户文本: 截断 + 移除可能破坏 XML tag 的字符。

    F1: 防 prompt injection — 移除 </user_input> 闭合标签,
    避免攻击者闭合 user_input 后注入 system 指令。
    """
    if not text:
        return ""
    cleaned = text.replace("</user_input>", "").replace("<user_input>", "")
    if len(cleaned) > max_chars:
        cleaned = cleaned[:max_chars] + "...(已截断)"
    return cleaned


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

        # F1: prompt injection 防御 — 用户字段截断 + tag 内化
        sanitized_reason = _sanitize_user_text(draft_reason)

        # 渲染 prompt (≤ 200 token 上下文, R3 fast-path)
        prompt = _PROMPT_TEMPLATE.format(
            ticker=effective_ticker,
            intended_action=intended_action,
            draft_reason=sanitized_reason,
            price=env_snapshot.price,
            holdings_pct=f"{env_snapshot.holdings_pct:.1%}",
        )

        # R3 fast-path: 显式传 4 个不变量 + timeout 由 LLMClient 内部 wait_for
        # 外层 asyncio.wait_for 作安全网 (slack 1s 兼容慢 retry chain cancellation)
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
                        },
                        schema=Rebuttal,
                        model=_FAST_PATH_MODEL,
                        max_tokens=_FAST_PATH_MAX_TOKENS,
                        temperature=_FAST_PATH_TEMPERATURE,
                        cache_lookup=_FAST_PATH_CACHE_LOOKUP,
                        allow_fallback=_FAST_PATH_ALLOW_FALLBACK,
                        timeout_seconds=_GENERATE_TIMEOUT_S,
                    ),
                    timeout=_GENERATE_TIMEOUT_S + 1.0,  # 安全网, 防 retry chain 拖死
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
