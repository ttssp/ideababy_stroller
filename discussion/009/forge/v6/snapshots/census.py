"""extraction/census.py — T006 · 009-pM3prime E1 · 密度 census(owns PPV P2)。

结论(先):首要 ROI 站真路径(P2)—— `python -m decision_ledger.extraction.census --collection-db <path>
  --caliber-version v1 --extractor-variant v1` → 只读真 collection.db(9,081 条 · 分层抽样)→ 提取器 →
  写 extracted_signals / extraction_rejections / trial_ledger(e1_trial)→ 产密度真数字 vs 预注册阈值 →
  verdict {meets_threshold / below_threshold_advisory}。

密度阈值语义 = **advisory 参考阈值**(HANDBACK-LOG #22 决议 2 · 2026-07-17):
  census 照常算「密度 vs 预注册阈值 30」并输出诚实判定 + 事前预期留底(防事后挪标准),**但非自动毙刀** ——
  密度 < 阈值**不**自动否决 M3'/E2。E2 go/no-go 由 operator 看**完整密度报告**(per-market 明细 + 拒绝构成)
  人工终裁(operator 权衡:30 反推自 M2 walk-forward、无实证基础,不提前拍死;advisory 保预注册纪律的诚实
  留底,又留事后分析空间)。阈值数字 30 本身仍**不可回改**(C6 · 只走 hand-back 新增 caliber_version)。

proposer(LLM 缝 · 两种真实装 · 均非 mock DB/提取器):
  - `literal_ticker_proposer`(--proposer literal · 默认自动化路径):**读真原文** · 按 record_tickers 候选在
    原文的真字面命中产 span(确定性 · 无 LLM key · 是 LLM 判断的确定性替身 · 读真语料跑真提取器写真库)。
  - `build_llm_proposer`(--proposer llm · 需 --api-key-env):温度 0 真 **DeepSeek**(OpenAI-兼容端点 · JSON mode ·
    operator 配 DEEPSEEK_API_KEY 时跑 · 同一 census 入口)。openai SDK 无缓存 → 无 cache 串号面(C1 隐患消失)。

核心红线:
  1. **collection.db 只读**(C10 · G-R1):CollectionReader URI mode=ro · 路径缺失 hard-fail。
  2. **trial_ledger 完整**(C1):每 variant×caliber×horizon 一 e1_trial 行(T012 守 · marker 不进分母)。
  3. **advisory 诚实留底**(E1-R1 · 决议 2):密度 < 阈值 → below_threshold_advisory(不静默 · 诚实输出 +
     事前预期留底 · 进完整报告供 operator 人工终裁 · **非自动毙刀**)。
  4. **无 mock**(anti-PPV):真 raw 语料 · 真 sqlite 写 · 真 extract 守门 · proposer 是 LLM 替身非 DB/提取器 mock。
  5. **凭据隔离**(C13):llm proposer 的 key 经 --api-key-env **直读值**(DEEPSEEK_API_KEY 形态 · 值只在闭包链内 ·
     不 log/不 ledger/不入 context · 有泄露前科)· literal proposer 无 key。

边界:只跑 census 写 3 表 + 产密度 verdict。**不做金标**(T007/8)· **不做 gate**(T009)· **不改采集**(OUT-8)。
"""

from __future__ import annotations

import argparse
import json
import re
import sqlite3
import sys
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any, Protocol

from pydantic import BaseModel, ConfigDict

from decision_ledger.extraction.collection_reader import (
    CollectionReader,
    derive_stratification_market,
)
from decision_ledger.extraction.extractor import ProposedSpan, extract, is_weakly_anchored
from decision_ledger.extraction.sampling import (
    build_sampling_plan,
    is_in_oos_window,
    select_source_ids,
)

# horizon 集(census 每 horizon 记一 trial · 与阈值 per-horizon 对齐)
_HORIZONS = (5, 20, 60)

# LLM proposer 温度 0(确定性 · C4 · 同文同版同输出)· 提取器版本化 prompt 模板版本。
_LLM_TEMPERATURE = 0.0
_EXTRACTION_TEMPLATE_VERSION = "extraction_v1"
# DeepSeek OpenAI-兼容端点(operator 配 DEEPSEEK_API_KEY · 复用已装 openai SDK · 不引新依赖 · 不动 Anthropic LLMClient)。
_DEEPSEEK_BASE_URL = "https://api.deepseek.com"
_DEEPSEEK_MODEL = "deepseek-v4-flash"  # operator 指定(CLI --model 可覆盖)· DeepSeek 侧真模型 ID
# max_tokens 是**输出**上限(非输入)· 真跑实测 2048 对长 qa/replay 转写会 finish_reason=length 截断(→ parse_failure
#   计数暴露)· 提到 4096 给多信号 record 留余量。真正长转写仍可能截断 → 见 runbook §chunking(operator 调 · 或抽样偏短文)。
_LLM_MAX_TOKENS = 4096
_LLM_TIMEOUT_SEC = 60.0

Proposer = Callable[..., "list[ProposedSpan]"]


# ── LLM 接线用类型(DeepSeek · OpenAI-兼容)────────────────────────────────────────
class ProposedSpanList(BaseModel):
    """LLM structured-output(JSON mode)的 pydantic 校验包装(单对象裹 list · 防注入)。

    结论:LLM 温度 0 抽荐股信号 → spans。extra=forbid:LLM 多余键被拒(注入防御 · 同 ProposedSpan)。
    """

    model_config = ConfigDict(extra="forbid")

    spans: list[ProposedSpan] = []


class _ChatClientProto(Protocol):
    """census 只依赖 OpenAI-兼容 client 的 `chat.completions.create`(duck-typed · 测试注 fake · 不硬绑 openai)。

    真 client = openai.OpenAI(base_url=DeepSeek, api_key=...)· .chat.completions.create(**kwargs) 返带
    .choices[0].message.content(JSON 串)· fake 同形态即可(不真调 DeepSeek · 不烧 key)。
    """

    @property
    def chat(self) -> Any: ...


ChatClientFactory = Callable[[str], _ChatClientProto]


@dataclass
class CensusReport:
    """census 产物报告(密度真数字 + verdict · 供 hand-back T013)。"""

    caliber_version: str
    extractor_variant: str
    total_records: int
    total_accepted: int
    total_rejected: int
    # 双口径密度(H1 复审 · operator 决):density_by_stratum=**下界**(仅强锚·抗幻觉)· density_all_by_stratum=**上界**(强+弱·含隐性)。
    density_by_stratum: dict[str, int] = field(default_factory=dict)      # "market" -> 强锚 accepted 数(下界 · 兼容旧名)
    density_all_by_stratum: dict[str, int] = field(default_factory=dict)  # "market" -> 全 accepted 数(上界 · 含弱锚/隐性)
    # 三态(red-team 复审):meets_threshold(强锚下界达标·最可信)/ meets_threshold_unverified(仅上界达标·全靠弱锚·须抽查)/
    #   below_threshold_advisory(连上界都不达标·advisory 非自动毙刀·决议 2)。
    verdict: str = "below_threshold_advisory"
    # ⚠ 可观测性(red-team H2 · 2026-07-17):LLM 路径的失败计数 —— 区分"真 0 密度" vs"截断/坏 JSON/API 挂
    #   掉导致的假 0 密度"。任一 > 0 = verdict 的 0-accepted **不可信**(operator 须知 · 别读成真稀疏)。
    llm_parse_failures: int = 0   # LLM 返回坏 JSON / 结构不符 / max_tokens 截断 → 该 record 静默 0 span 的次数
    llm_api_failures: int = 0     # DeepSeek API 报错 / 空 choices / 超时 → 该 record 降级 0 span 的次数
    # 引文弱锚计数(H1 · 审计非拒绝):accepted 信号里 ticker 不在 span 切片字面出现的条数。隐性信号合法弱锚,
    #   但**弱锚率高 = 引文质量存疑 / 疑幻觉**(operator 审:占 accepted 比例高 → 别轻信密度 · 抽查引文)。
    weak_anchor_accepted: int = 0


# ── proposer 实装 1:确定性真文本 proposer(读真原文 · 真字面命中 · 无 LLM)──────────────
def literal_ticker_proposer(
    text: str, *, published_at: str, record_tickers: list[str] | None = None,
    source_id: str | None = None,  # noqa: ARG001 — literal 路径不需 · 收下以兼容统一 proposer 契约
) -> list[ProposedSpan]:
    """按 record_tickers 候选在**真原文**的字面命中产 span(确定性 · LLM 判断替身 · 非 mock)。

    结论:对每个候选 ticker,在原文找首个字面命中位置 → 产一条 long span(方向用简单情绪启发:
      命中处附近有"涨/看多/多"→long,"跌/看空/空"→short,否则不产方向 → 下游 no_direction 拒)。
    细节:这是 census 自动化路径的确定性替身(读真语料 · 真 span offset · 真 published_at)· 命中不到 →
      不产 span(该 record 无 accepted · 计入密度分母语义由 census 处理)。真 LLM 路径见 llm_proposer。
    """
    tickers = record_tickers or []
    spans: list[ProposedSpan] = []
    for ticker in tickers:
        core = ticker.split(".")[0]
        if not core:
            continue
        m = re.search(r"\b" + re.escape(core) + r"\b", text, re.IGNORECASE)
        if m is None:
            continue  # 字面命不到 → 不产(候选校验:record_tickers 是弱关联 · verify · T004)
        start, end = m.start(), m.end()
        # 方向启发(命中处 ±40 字符窗内找情绪词 · 无 → direction=None → no_direction 拒)
        window = text[max(0, start - 40): min(len(text), end + 40)]
        direction: str | None = None
        if re.search(r"看多|涨|买入|加仓|做多|bull|long", window, re.IGNORECASE):
            direction = "long"
        elif re.search(r"看空|跌|卖出|减仓|做空|bear|short", window, re.IGNORECASE):
            direction = "short"
        spans.append(
            ProposedSpan(
                ticker=core, direction=direction, confidence=0.5,
                span_start=start, span_end=end, content_published_at=published_at,
            )
        )
    return spans


# ── proposer 实装 2:真 LLM(DeepSeek · 温度 0 · 需 --api-key-env · operator 配 key 时跑)──────────
def _default_deepseek_client_factory(api_key: str) -> _ChatClientProto:
    """默认真 DeepSeek client 构造(openai SDK 指 DeepSeek base_url · 不引新依赖 · 不动 Anthropic LLMClient)。

    结论:api_key 明文经构造传入 openai.OpenAI(base_url=DeepSeek · api_key=值)· 值只在此闭包链内 · 不 log/不 ledger。
    细节:import 延迟到调用点(census literal 路径零 LLM 依赖 · 无 key 环境不触发 openai/DeepSeek 构造)。
      openai SDK 无内置缓存层 → 天然无 cache 串号面(旧 Anthropic LLMClient 的 C1 隐患在此彻底消失)。
    """
    from openai import OpenAI

    return OpenAI(base_url=_DEEPSEEK_BASE_URL, api_key=api_key, timeout=_LLM_TIMEOUT_SEC)


def _read_api_key_value(api_key_env: str) -> str:
    """从 env 变量**直读 key 值**(--api-key-env 模式 · DEEPSEEK_API_KEY 形态 · operator 拍板)。

    结论:env 直接存 key 值(非文件路径)→ os.environ 读值 · 未设/空 → fail-fast(不静默用空 key)。
    细节:与 tiingo 的 load_token_from_env_pointer(env 存**路径**)是两种凭据形态 · 本函数走"直存值"形态。
      key 值只在本调用链闭包内 · **绝不** log / 写 ledger / 入 census context 输出(C13 · 有泄露前科)。
    """
    import os

    val = os.environ.get(api_key_env)
    if not val:
        raise ValueError(
            f"env {api_key_env} 未设或为空(--api-key-env 直读值模式 · 应存 DeepSeek key 值 · C13)"
        )
    return val


def _build_extraction_prompt(text: str, *, published_at: str, record_tickers: list[str]) -> str:
    """温度 0 抽取 prompt(读中文原文语义抽疑似荐股信号 → ProposedSpan)· 提取器版本化(_EXTRACTION_TEMPLATE_VERSION)。

    结论:让 LLM 只产**候选 span**(未验收原料)· 引文锚定/PIT/歧义拒绝由下游 extract() 守门(proposer 不越权)。
    细节:span_start/span_end 是**原文字符偏移**(供 extract 回锚真原文 · C3)· content_published_at 用记录发布时点
      (PIT 守 · C2)· ticker/direction 可空(歧义 → 下游 typed rejection · 不猜)· candidate tickers 作提示不作 ground-truth。
    """
    cand = ", ".join(record_tickers) if record_tickers else "(无候选提示)"
    # ⚠ prompt 必须含 "json" 字样(DeepSeek/OpenAI response_format=json_object 硬要求 · 真调 400 实证 2026-07-17)。
    return (
        "你是投研信号抽取器。从下面这段中文投研原文里,抽取**疑似荐股信号**(隐性/显性均可),"
        "每条产一个候选 span。**严格只返回一个 JSON 对象**,形如 "
        '{"spans": [{"ticker": ..., "direction": ..., "confidence": ..., '
        '"span_start": ..., "span_end": ..., "content_published_at": ...}, ...]},不要输出任何解释文字。\n'
        "字段规则:\n"
        "1. span_start/span_end = 该信号在原文中的字符偏移(整数 · 从 0 计 · 供回锚原文)。\n"
        "2. ticker = 标的代码字符串(不确定填 null · 不猜)· direction ∈ {\"long\",\"short\"}(不明确填 null)。\n"
        "3. confidence = 0~1 浮点。\n"
        f"4. content_published_at 一律填该原文发布时点 \"{published_at}\"(PIT 守 · 不可晚于信号时点)。\n"
        '5. 无任何疑似信号 → 返回 {"spans": []}(不硬凑)。\n'
        f"候选标的提示(仅参考 · 非权威 · 可忽略):{cand}\n"
        "----- 原文开始 -----\n"
        f"{text}\n"
        "----- 原文结束 -----"
    )


def _parse_spans_json(content: str) -> tuple[ProposedSpanList, bool]:
    """LLM 返 JSON 串 → pydantic 校验为 ProposedSpanList · 返 (结果, ok)。ok=False = 解析/校验失败(计数用)。

    结论:DeepSeek JSON mode 返 `{"spans":[...]}` 串 · json.loads + model_validate · extra=forbid 拒多余键。
    细节:LLM 输出**不可信**(注入面 + max_tokens 截断面)· 解析失败/结构不符 **不崩整个 census**(该 record 无
      accepted · 降级安全)· **但返 ok=False 供上层计数**(red-team H2:区分真 0 密度 vs 截断/坏 JSON 假 0)·
      真 span 仍走下游 extract() 的引文锚定/PIT/歧义守门(BLOCK #3 不绕过 · proposer 只是候选原料)。
    """
    try:
        data = json.loads(content)
    except (json.JSONDecodeError, TypeError):
        return ProposedSpanList(spans=[]), False  # 坏 JSON(常见 = max_tokens 截断)→ 降级 + 标失败
    if not isinstance(data, dict):
        return ProposedSpanList(spans=[]), False
    try:
        return ProposedSpanList.model_validate(data), True
    except Exception:  # noqa: BLE001 — 结构不符(缺字段/多余键/越界)→ 降级 + 标失败(不崩)
        return ProposedSpanList(spans=[]), False


def _sanitize_llm_exc(exc: Exception) -> str:
    """脱敏 LLM 异常信息(C13 · red-team L)—— 只留类型名 + status_code,**绝不**回显异常原文(防 key 泄露)。

    结论:openai SDK 异常可能携 request 细节 · 不 str(exc) 回显 · 只取类型 + 有则 status_code。
    """
    status = getattr(exc, "status_code", None)
    return f"{type(exc).__name__}" + (f"(status={status})" if status is not None else "")


def build_llm_proposer(
    api_key_env: str, *, client_factory: ChatClientFactory | None = None,
    model: str = _DEEPSEEK_MODEL,
) -> Proposer:
    """温度 0 真 DeepSeek proposer(key 经 --api-key-env 直读值 · C13 · OpenAI-兼容端点)。

    结论:接 DeepSeek(openai SDK 指 base_url · 温度 0 · JSON mode · 提取器版本化)· operator 配 DEEPSEEK_API_KEY
      后经 `--proposer llm --api-key-env DEEPSEEK_API_KEY` 端到端跑真密度(读中文原文语义抽)。
    细节:
      - key 经 _read_api_key_value 直读 env 值(DEEPSEEK_API_KEY 形态 · 值只在闭包链内 · 不 log/不 ledger/不入 context · C13)。
      - client_factory 是 DI 缝(默认真构造 DeepSeek client · 测试注 fake · 使接线可单测而不烧 key)。
      - 温度 0(C4 确定性)· response_format=JSON mode(结构化输出 · pydantic 校验 · 注入防御)。
      - proposer 产的 span 是**候选原料** · 仍走下游 extract() 的引文锚定/PIT/歧义守门(BLOCK #3 不绕过)。
      - openai SDK 无内置缓存 → 无 cache 串号面(旧 Anthropic LLMClient 的 C1 隐患在此彻底消失 · 每 record 真调一次)。
      - **鲁棒性(red-team M/H2)**:单 record 的 API 报错/空 choices/坏 JSON **不炸整个 census**(降级该 record 为
        0 span + 计数)· proposer 挂 `.stats`(api_failures/parse_failures)供 run_census 读入 CensusReport(可观测)。
        计数 > 0 = verdict 的 0-accepted **不可信**(operator 须知是"挂了"非"真稀疏")。
    """
    # 直读 key 值(C13 · 值只在闭包链内 · 不 log 不写 ledger)· 构造时传入 · 不硬编
    api_key = _read_api_key_value(api_key_env)
    factory = client_factory or _default_deepseek_client_factory
    # ⚠ 构造异常也脱敏(red-team 复审 LOW):factory 构造在 _proposer 的 try 外 · 若构造异常携 key(SDK 校验器
    #   可能 raise f'invalid key: {key}')会经 _run 顶层 except 裸 print 泄露 · 故此处也脱敏 re-raise。
    try:
        client = factory(api_key)
    except Exception as exc:  # noqa: BLE001 — 脱敏后 re-raise(不带 key 原文 · C13)
        raise RuntimeError(f"LLM client 构造失败 · {_sanitize_llm_exc(exc)}") from None
    stats = {"api_failures": 0, "parse_failures": 0}  # 闭包状态 · 经 _proposer.stats 暴露给 run_census

    def _proposer(
        text: str, *, published_at: str, record_tickers: list[str] | None = None,
        source_id: str | None = None,  # noqa: ARG001 — DeepSeek 路径无缓存 · source_id 无需进 key(留参兼容统一契约)
    ) -> list[ProposedSpan]:
        prompt = _build_extraction_prompt(
            text, published_at=published_at, record_tickers=record_tickers or []
        )
        # DeepSeek chat.completions(温度 0 · JSON mode)· 每 record 真调一次(无缓存 · 无串号面)。
        # 鲁棒性(red-team M):API 报错/空 choices → 降级该 record 为 0 span + 计数(不炸全 census · 不丢已跑进度)。
        try:
            resp = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=_LLM_TEMPERATURE,   # 0.0 确定性(C4)
                max_tokens=_LLM_MAX_TOKENS,
                response_format={"type": "json_object"},  # 结构化 JSON 输出(pydantic 校验 · 注入防御)
            )
            choices = getattr(resp, "choices", None) or []
            if not choices:
                stats["api_failures"] += 1
                print(f"WARN LLM 空 choices · sid={source_id} · 降级 0 span", file=sys.stderr)
                return []
            # 非自然停检测(code-reviewer + red-team 复审):finish_reason 非 stop/tool_calls = 截断/内容过滤/异常 →
            #   输出不完整不可信 → 计 parse_failure(即便碰巧 loads 成功也是残缺 · 不可当"真 0 信号")。
            #   red-team 复审 LOW:原只查 'length' · 'content_filter' 等会漏 → 改 allowlist(只放行自然停)。
            finish_reason = getattr(choices[0], "finish_reason", None)
            content = choices[0].message.content
            if finish_reason is not None and finish_reason not in ("stop", "tool_calls"):
                stats["parse_failures"] += 1
                print(f"WARN LLM 非自然停(finish_reason={finish_reason} · 疑截断/内容过滤)· sid={source_id} · 降级 0 span", file=sys.stderr)
                return []
            if not content:  # None/空串(内容过滤/空补全)→ 计 api_failure(非"真 0 信号" · code-reviewer #4)
                stats["api_failures"] += 1
                print(f"WARN LLM 返空内容 · sid={source_id} · 降级 0 span", file=sys.stderr)
                return []
        except Exception as exc:  # noqa: BLE001 — 单 record API 失败降级(脱敏 · 不回显异常原文防 key 泄露 · C13)
            stats["api_failures"] += 1
            print(f"WARN LLM API 失败 · sid={source_id} · {_sanitize_llm_exc(exc)} · 降级 0 span", file=sys.stderr)
            return []

        parsed, ok = _parse_spans_json(content)
        if not ok:
            stats["parse_failures"] += 1
            print(f"WARN LLM 坏 JSON/结构不符(疑 max_tokens 截断)· sid={source_id} · 降级 0 span", file=sys.stderr)
        return list(parsed.spans)

    _proposer.stats = stats  # type: ignore[attr-defined]  — run_census 读:proposer 的失败计数入 CensusReport
    return _proposer


def _decide_verdict(
    density_strong: dict[str, int],
    density_all: dict[str, int],
    market_threshold: dict[str, int],
) -> str:
    """三态密度 verdict(纯函数 · 可单测 · red-team 复审):verdict 字段本身携可信度,不靠 operator 看 stderr 侧栏。

    - meets_threshold:**每 market 的 strong(强锚下界)都 ≥ 阈值** = 有真实强锚证据支撑(最可信)。
    - meets_threshold_unverified:strong 不全达标但 **每 market 的 all(上界)都 ≥ 阈值** = 达标全靠弱锚
      (隐性 or 幻觉 offset)· 未验证 · 须抽查引文(防 H1 幻觉冒充密度 · 别当 meets 直接放行 E2)。
    - below_threshold_advisory:连 all(上界)都有 market < 阈值 = 确凿低(advisory · 非自动毙刀 · 决议 2)。
    """
    # 空 market_threshold 保守闭合(red-team 复审 LOW):`all()` 空集真空为 True → 会误返 meets_threshold(零证据放行)。
    #   现调用点 run_census 已上游挡空 thresholds · 但本纯函数自守 fail-closed · 防未来复用绕过上游 guard。
    if not market_threshold:
        return "below_threshold_advisory"
    strong_meets = all(density_strong.get(m, 0) >= thr for m, thr in market_threshold.items())
    all_meets = all(density_all.get(m, 0) >= thr for m, thr in market_threshold.items())
    if strong_meets:
        return "meets_threshold"
    if all_meets:
        return "meets_threshold_unverified"
    return "below_threshold_advisory"


def run_census(
    collection_db: str,
    *,
    caliber_version: str,
    extractor_variant: str,
    db_path: str,
    proposer: Proposer,
    sample_size: int = 40,
) -> CensusReport:
    """census 主编排:抽样 → 提取 → 写 3 表 → 密度比对 → verdict(advisory 诚实留底 · 非自动毙刀)。"""
    plan = build_sampling_plan(caliber_version)

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        # 读阈值(preregister 已写 density_threshold · 未就位则 advisory 判定无参照 → 报错)
        threshold_rows = conn.execute(
            "SELECT market, horizon, min_density_threshold FROM density_threshold "
            "WHERE caliber_version=?",
            (caliber_version,),
        ).fetchall()
        if not threshold_rows:
            raise ValueError(
                "density_threshold 未预注册(先跑 preregister · C6 先注册后普查)· census 无阈值参照"
            )
        thresholds = {(r["market"], r["horizon"]): r["min_density_threshold"] for r in threshold_rows}

        # ⚠ 原子性(red-team 复审 3 · 2026-07-17):**单次末尾 commit**(全 run 一个事务)· 不做 per-record commit
        #   也不做起手 DELETE。理由:per-record commit + 起手 DELETE 曾引两 bug —— (a) rejections 无 variant 列 ·
        #   按 caliber 清会**误删别的 variant** 审计行;(b) 无并发锁 · 两 run 交错 DELETE/commit 损坏表。单原子事务
        #   天然规避:失败 → 全回滚(无部分写)· 重跑 → 干净新事务(不双插)· 并发 → sqlite 事务隔离(后者等锁或失败,
        #   不产混合态)。代价:中途失败丢整 run 进度 —— 但 census 是可重跑的只读普查(丢了重跑即可 · 可接受)。
        total_records = 0
        total_accepted = 0
        total_rejected = 0
        weak_anchor_accepted = 0  # H1 审计:accepted 里 ticker 不在 span 切片字面出现的条数
        # ⚠ review HIGH#1 修:密度按 **market** 计(**非** per-horizon)。
        #   SuspectedSignal 无 horizon 维(horizon 是 E2 回测窗概念 · 提取时不产生)· 原实现把一条信号 fan
        #   进 3 个 horizon 桶 → 三桶恒等 = 一个 market 数复制三份 = 假的 per-horizon 独立证据。诚实做法:
        #   密度是 **per-market horizon-independent** 数字 · verdict 比 per-market 阈值(每 horizon 阈值相同 30 · 取一次)。
        # 双口径(H1 复审):density_all=强+弱(上界·含隐性含幻觉)· density_strong=仅强锚(下界·抗幻觉·漏隐性)。
        density_all_by_market: dict[str, int] = {}
        density_strong_by_market: dict[str, int] = {}

        with CollectionReader(collection_db) as reader:
            # 分层抽样:每 form 抽 N(简化:按 form 抽 · market/horizon 在 record 内派生)
            sampled_sids: list[str] = []
            for form in plan.forms:
                pool = reader.source_ids_by_form(form)
                picked = select_source_ids(
                    pool, n=min(sample_size, len(pool)), seed_key=f"{caliber_version}:{form}"
                )
                sampled_sids.extend(picked)

            now = conn.execute("SELECT strftime('%Y-%m-%dT%H:%M:%SZ','now')").fetchone()[0]

            for sid in sampled_sids:
                rec = reader.load_record(sid)
                if rec is None or not rec.text:
                    continue
                # C12:OOS 窗内 record 不参与密度(保留作 OOS · 防抄考卷)· review MED#3:按真实 UTC 日判(混时区)
                if is_in_oos_window(rec.published_at):
                    continue
                total_records += 1
                cand_tickers = reader.record_tickers(sid)

                signals, rejections = extract(
                    rec.text,
                    published_at=rec.published_at,
                    caliber_version=caliber_version,
                    extractor_version=extractor_variant,  # census 的 variant 即 extractor 的 version 维度
                    source_id=rec.source_id,
                    raw_ref=rec.raw_ref,
                    # source_id 传给 proposer:统一 proposer 契约(literal 不用 · DeepSeek 路径无缓存也不用作 key ·
                    #   仅留参兼容 · code-reviewer:此处曾有"防缓存串号"注释 · DeepSeek 无缓存已删)。
                    proposer=lambda t, *, published_at, _ct=cand_tickers, _sid=rec.source_id: proposer(
                        t, published_at=published_at, record_tickers=_ct, source_id=_sid
                    ),
                )

                # 写 accepted → extracted_signals(带引文 + 版本)
                for s in signals:
                    market = derive_stratification_market(s.ticker)
                    conn.execute(
                        "INSERT INTO extracted_signals "
                        "(source_id,raw_ref,span_start,span_end,ticker,direction,published_at,"
                        "confidence,extractor_variant,caliber_version,created_at) "
                        "VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                        (
                            s.citation.source_id, s.citation.raw_ref, s.citation.span_start,
                            s.citation.span_end, s.ticker, s.direction, s.published_at,
                            s.confidence, extractor_variant, caliber_version, now,
                        ),
                    )
                    total_accepted += 1
                    # 弱锚审计(H1 · red-team 复审):ticker 不在 span 切片字面出现 → 弱锚(word-boundary 判 · 见 is_weakly_anchored)。
                    weak = is_weakly_anchored(s.ticker, s.citation.span_start, s.citation.span_end, rec.text)
                    if weak:
                        weak_anchor_accepted += 1
                    # ⚠ 双口径密度(operator 决 · 2026-07-17 · red-team H1 复审):都报,不预设哪个对。
                    #   density_all = 强+弱全算(含隐性信号 · **上界** · 但含幻觉水分)· density_strong = 仅强锚
                    #   (**下界** · 对幻觉 offset 落真实无关文本鲁棒 · 但会漏真隐性信号)。operator 看 [strong, all] 区间人工终裁。
                    density_all_by_market[market] = density_all_by_market.get(market, 0) + 1
                    if not weak:
                        density_strong_by_market[market] = density_strong_by_market.get(market, 0) + 1

                # 写 rejected → extraction_rejections(typed · 不猜)
                for rej in rejections:
                    conn.execute(
                        "INSERT INTO extraction_rejections "
                        "(source_id,raw_ref,rejection_reason,caliber_version,created_at) "
                        "VALUES (?,?,?,?,?)",
                        (rej.source_id, rej.raw_ref, rej.rejection_reason.value, caliber_version, now),
                    )
                    total_rejected += 1

            # trial_ledger e1_trial 行:每 (extractor_variant × caliber × horizon × market) 一行(C1 完整性)。
            #   horizon 维在此保留 —— schema/C1 要求按 horizon 记账供未来 E2(E2 才真按 horizon 算 realized-return)·
            #   但**密度数字本身是 per-market horizon-independent**(见上方 density_by_market)· 两者不矛盾:
            #   trial_ledger 是"未来 E2 会在这些 (market,horizon) 上试"的记账 · 密度是"现在有多少信号可试"的计数。
            #   review 建议:记真实抽样规模而非硬 fallback —— markets 用阈值表声明的全集(census 覆盖意图),
            #   sampled_source_ids 存全集(不截断 · 可复现 D-12)。
            all_markets = {m for (m, _h) in thresholds}
            sampled_csv = ",".join(sampled_sids)
            for market in all_markets:
                for hz in _HORIZONS:
                    conn.execute(
                        "INSERT INTO trial_ledger "
                        "(row_kind,caliber_version,extractor_variant,horizon,market,"
                        "sampled_source_ids,created_at) "
                        "VALUES ('e1_trial',?,?,?,?,?,?)",
                        (caliber_version, extractor_variant, hz, market, sampled_csv, now),
                    )

        # 密度 verdict:per-market 密度 < 该 market 阈值 → below_threshold_advisory(诚实留底 · 非自动毙刀 · 决议 2)。
        #   review HIGH#1 修:比 **per-market**(非 per-horizon 假三桶)· 每 market 的阈值跨 horizon 相同(取 min 保守)。
        #   决议 2 语义:verdict 是 **advisory 参考判定**(照常算「vs 30 过/不过」+ 留事前预期)· operator 看
        #   完整报告人工终裁 go/no-go —— 判定逻辑与阈值比较**不变**,仅"低于阈值"不再等价"自动否决"。
        # 三态 verdict(operator 决 · 2026-07-17 · red-team 复审):verdict 字段本身携可信度 · 不靠 operator 看 stderr 侧栏。
        #   - meets_threshold:**strong(下界)** 每 market 都 ≥ 阈值 = 有真实强锚证据支撑(最可信)。
        #   - meets_threshold_unverified:strong < 阈值但 **all(上界)** ≥ 阈值 = 达标全靠弱锚(隐性 or 幻觉)· 未验证 ·
        #     须抽查引文(防 H1 幻觉 offset 冒充密度 · 别当 meets 直接放行)。
        #   - below_threshold_advisory:连 all(上界)都 < 阈值 = 确凿低(advisory · 非自动毙刀 · 决议 2)。
        #   review HIGH#1:比 **per-market**(非 per-horizon 假三桶)· 每 market 阈值跨 horizon 相同(取 min 保守)。
        market_threshold: dict[str, int] = {}
        for (market, _hz), thr in thresholds.items():
            # 同 market 跨 horizon 阈值取最严(min)· 保守门槛(当前候选各 horizon 均 30 · min 即 30)
            market_threshold[market] = min(market_threshold.get(market, thr), thr)
        density_by_stratum = {m: density_strong_by_market.get(m, 0) for m in market_threshold}   # 下界(仅强锚)· 兼容旧名
        density_all_by_stratum = {m: density_all_by_market.get(m, 0) for m in market_threshold}  # 上界(强+弱)
        verdict = _decide_verdict(density_by_stratum, density_all_by_stratum, market_threshold)

        conn.commit()
    finally:
        conn.close()

    # LLM 失败计数(red-team H2):proposer 挂 .stats 则读入(literal 无 .stats → 0)· 供 report 可观测。
    proposer_stats = getattr(proposer, "stats", None) or {}
    return CensusReport(
        caliber_version=caliber_version,
        extractor_variant=extractor_variant,
        total_records=total_records,
        total_accepted=total_accepted,
        total_rejected=total_rejected,
        density_by_stratum=density_by_stratum,
        density_all_by_stratum=density_all_by_stratum,
        verdict=verdict,
        llm_parse_failures=int(proposer_stats.get("parse_failures", 0)),
        llm_api_failures=int(proposer_stats.get("api_failures", 0)),
        weak_anchor_accepted=weak_anchor_accepted,
    )


# ── CLI ─────────────────────────────────────────────────────────────────────────
def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m decision_ledger.extraction.census",
        description="密度 census(读 collection.db 只读 → 写信号 3 表 → 密度 verdict · P2 PPV 真路径入口)。",
    )
    parser.add_argument("--collection-db", required=True, help="collection.db 路径(只读 · C10)")
    parser.add_argument("--caliber-version", required=True, help="口径版本(如 v1)")
    parser.add_argument("--extractor-variant", required=True, help="提取器变体(温度 0 · 版本钉死)")
    parser.add_argument("--db", default=None, help="data.sqlite 路径(缺省回落 config.db_path)")
    parser.add_argument("--sample-size", type=int, default=40, help="每 form 抽样数(默认 40)")
    parser.add_argument(
        "--proposer", choices=("literal", "llm"), default="literal",
        help="literal=确定性真文本替身(无 key)· llm=温度 0 真 DeepSeek(需 --api-key-env)",
    )
    parser.add_argument(
        "--api-key-env", default=None,
        help="LLM key 的 env 变量名(直读值 · 如 DEEPSEEK_API_KEY · --proposer llm 时必需 · C13)",
    )
    parser.add_argument(
        "--model", default=_DEEPSEEK_MODEL,
        help=f"DeepSeek 模型 ID(默认 {_DEEPSEEK_MODEL} · --proposer llm 时用)",
    )
    return parser


def _resolve_proposer(args: argparse.Namespace) -> Proposer:
    if args.proposer == "llm":
        if not args.api_key_env:
            raise ValueError("--proposer llm 需 --api-key-env(LLM key env 变量名 · 直读值 · C13)")
        return build_llm_proposer(args.api_key_env, model=args.model)
    return literal_ticker_proposer


def _run(args: argparse.Namespace) -> int:
    db_path = args.db
    if db_path is None:
        from decision_ledger.config import load_settings

        db_path = str(load_settings().db_path)
    try:
        proposer = _resolve_proposer(args)
        report = run_census(
            args.collection_db,
            caliber_version=args.caliber_version,
            extractor_variant=args.extractor_variant,
            db_path=db_path,
            proposer=proposer,
            sample_size=args.sample_size,
        )
    except (ValueError, FileNotFoundError) as exc:
        print(f"ERR: 入参/配置非法 · {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2
    except Exception as exc:  # noqa: BLE001
        print(f"ERR: 未预期失败 · {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1

    print(
        f"OK census caliber={report.caliber_version} variant={report.extractor_variant} "
        f"records={report.total_records} accepted={report.total_accepted} "
        f"rejected={report.total_rejected} verdict={report.verdict} "
        f"llm_api_failures={report.llm_api_failures} llm_parse_failures={report.llm_parse_failures} "
        f"weak_anchor_accepted={report.weak_anchor_accepted}"
    )
    # 双口径密度(H1 复审 · operator 决):区间 [strong 下界, all 上界] 都报 · operator 人工终裁。
    print(
        f"密度双口径 · strong(仅强锚·抗幻觉·下界)={report.density_by_stratum} · "
        f"all(强+弱·含隐性含幻觉·上界)={report.density_all_by_stratum}",
        file=sys.stderr,
    )
    # 弱锚审计提示(H1):accepted 里高比例弱锚 = 引文质量存疑(疑幻觉 offset)· operator 抽查引文。
    if report.total_accepted > 0 and report.weak_anchor_accepted > 0:
        rate = report.weak_anchor_accepted / report.total_accepted
        print(
            f"ℹ 引文弱锚:{report.weak_anchor_accepted}/{report.total_accepted}(={rate:.0%})accepted 信号 "
            "ticker 不在 span 切片字面出现 · 隐性信号合法弱锚,但高率疑幻觉 offset · 建议抽查引文质量。",
            file=sys.stderr,
        )
    # ⚠ 可观测性(red-team H2):LLM 失败 > 0 → 0-accepted **不可信**(是"挂了"非"真稀疏")· 醒目警告。
    llm_failures = report.llm_api_failures + report.llm_parse_failures
    if llm_failures > 0:
        print(
            f"⚠ WARN: {llm_failures} 条 record LLM 失败(api={report.llm_api_failures} · "
            f"parse/截断={report.llm_parse_failures})→ 这些 record 被降级为 0 span · "
            "密度 verdict 的 0-accepted **不可信**(是 LLM 挂了非真稀疏)· "
            "须查根因(max_tokens 截断 / API 限流 / 网络)后重跑,别据此下密度结论。",
            file=sys.stderr,
        )
    if report.verdict == "meets_threshold_unverified":
        print(
            "⚠ MEETS_UNVERIFIED(达标全靠弱锚 · red-team H1): strong(强锚下界)< 阈值但 all(上界)≥ 阈值 · "
            f"strong={report.density_by_stratum} · all={report.density_all_by_stratum} · "
            "达标证据全是弱锚(隐性信号 or 幻觉 offset)· **须抽查 extracted_signals 引文** 判是真隐性还是幻觉 · "
            "别当 meets 直接放行 E2。",
            file=sys.stderr,
        )
    elif report.verdict == "below_threshold_advisory":
        print(
            "ADVISORY(诚实留底 · 非自动毙刀 · 决议 2): 密度(上界)< 预注册参考阈值 30 · "
            f"strong={report.density_by_stratum} · all={report.density_all_by_stratum} · 事前预期已留底(防事后挪标准)· "
            "E2 go/no-go 由 operator 看完整密度报告(per-market 明细 + 拒绝构成)人工终裁 · "
            "→ 进 hand-back(tag prd-revision-trigger)",
            file=sys.stderr,
        )
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = _build_arg_parser()
    args = parser.parse_args(argv)
    return _run(args)


if __name__ == "__main__":
    sys.exit(main())
