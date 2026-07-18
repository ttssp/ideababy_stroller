"""extraction/extractor.py — T005 · 009-pM3prime E1 · 疑似信号提取器(温度0/版本化/PIT/引文/歧义)。

结论(先):从 raw 文本按 T001 口径抽疑似信号(O10 · C2/C3/C4/C8)。核心 = **确定性守门逻辑**
  (PIT/引文/schema/歧义拒绝)+ **DI proposer 缝**(真 LLM 在 T006 census · 单元层注 fake 测逻辑)。

架构(为什么这么切):
  - **proposer**(DI · LLM 缝):`(text, *, published_at) -> list[ProposedSpan]` —— 真实装是温度 0 LLM 调用,
    但 extract() 本身不 import LLM(单元层可注 fake · 真 LLM 端到端在 T006 census PPV · C13 key 经 --token-env 名)。
  - **extract()**(确定性守门):对每个 ProposedSpan 逐条守 5 要件 + PIT + 引文可锚 → accepted SuspectedSignal /
    typed Rejection。**歧义默认拒绝不猜**(C8 · echo M2 join.py 精神)。

核心红线:
  1. **PIT 守**(C2):入参强制 published_at;候选的 content_published_at > 信号时点 → drop(未来内容不可达 · T010 端到端)。
  2. **引文锚定**(C3):accepted 附 Citation(source_id+raw_ref+span offset)· span 必须落在原文范围内(越界 → 拒 · 假引文不可回锚)。
  3. **确定性**(C4):extract 本身无随机 · 同 proposals 同 version → 同输出(温度 0 假设在 proposer 层 · T011 真 LLM 一致性测)。
  4. **歧义默认拒绝**(C8):无 ticker→sector_only · 无/非交易方向→no_direction · 无时点→no_timepoint · 各落 typed Rejection。
  5. **注入防御**(G-R3):原文当**数据**非指令 · 输出 schema 只收 5 要件(ProposedSpan 字段封闭)· span 越界即拒。
  6. **凭据隔离**(C13):本模块不含明文 key · LLM key 只经 --token-env 名(真 proposer 适配器在 census 层组装)。

边界:只 build 提取器 + 守门逻辑。**不跑全量 census**(T006)· **不做金标**(T007/8)· **不建表**(T002)。
"""

from __future__ import annotations

import re
from collections.abc import Callable

from pydantic import BaseModel, ConfigDict, Field

from decision_ledger.extraction.caliber import (
    Citation,
    ExtractionRejectionReason,
    SuspectedSignal,
)
from decision_ledger.extraction.timeutil import is_at_or_before

# 可交易方向(对齐 caliber · neutral/wait/no_view 不产样本 → no_direction 拒)
_TRADEABLE_DIRECTIONS = frozenset({"long", "short"})


class ProposedSpan(BaseModel):
    """proposer(LLM 缝)产出的候选 span —— extract() 守门前的原料(未验收)。

    封闭 schema(注入防御 G-R3):只收这些字段 · LLM 输出多余键被 pydantic 拒 · 原文指令性内容进不来。
    ticker/direction 可 None(歧义 → 下游 typed rejection)· content_published_at 用于 PIT 守。
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    ticker: str | None = None
    direction: str | None = None
    confidence: float = Field(ge=0.0, le=1.0, default=0.0)
    span_start: int = Field(ge=0)
    span_end: int = Field(ge=0)
    content_published_at: str  # 该 span 所据内容的发布时点(PIT 守 · ≤ 信号时点才可用)


class Rejection(BaseModel):
    """歧义/不合格候选的 typed 拒绝(落 extraction_rejections · 不猜)。"""

    model_config = ConfigDict(frozen=True)

    rejection_reason: ExtractionRejectionReason
    source_id: str
    raw_ref: str
    detail: str = ""  # 拒绝细节(可空 · 审计用)


# proposer 类型:LLM 缝(真实装温度 0 · 单元层注 fake)
Proposer = Callable[..., "list[ProposedSpan]"]


def extract(
    text: str,
    *,
    published_at: str,
    caliber_version: str,
    extractor_version: str,
    source_id: str,
    raw_ref: str,
    proposer: Proposer,
) -> tuple[list[SuspectedSignal], list[Rejection]]:
    """从 raw 文本抽疑似信号(确定性守门 · 歧义默认拒绝 · PIT/引文守)。

    结论:proposer 产候选 span → 逐条守 5 要件 + PIT + 引文可锚 → (accepted signals, typed rejections)。
    细节:published_at 是权威信号时点(PIT 基准)· span 必须落原文范围内 · 无随机(C4 确定性)。
    """
    proposals: list[ProposedSpan] = proposer(text, published_at=published_at)
    text_len = len(text)

    signals: list[SuspectedSignal] = []
    rejections: list[Rejection] = []

    for sp in proposals:
        # 1. PIT 守(C2):内容时点晚于信号时点 = 未来内容泄漏(提取侧缺陷,非语料歧义)→ **静默 drop**
        #    (不落 extraction_rejections · rejection 表是语料侧歧义留痕 · PIT 泄漏是提取器该自己堵的 bug 面)。
        # ⚠ review HIGH#2 修:真实 UTC 时刻比较(**非**裸字符串 · 混时区 +08:00/Z 下字典序 ≠ 时间序)。
        if not is_at_or_before(sp.content_published_at, published_at):
            continue

        reason = _classify_reject(sp, text=text, text_len=text_len)
        if reason is not None:
            rejections.append(
                Rejection(
                    rejection_reason=reason, source_id=source_id, raw_ref=raw_ref,
                    detail=f"ticker={sp.ticker} direction={sp.direction} span={sp.span_start}:{sp.span_end}",
                )
            )
            continue

        # accepted:引文锚定 + 版本化(此时 ticker/direction 已确保非 None/可交易 · span 已在界内)
        assert sp.ticker is not None and sp.direction is not None  # _classify_reject 已守
        signals.append(
            SuspectedSignal(
                ticker=sp.ticker,
                direction=sp.direction,
                published_at=published_at,
                citation=Citation(
                    source_id=source_id, raw_ref=raw_ref,
                    span_start=sp.span_start, span_end=sp.span_end,
                ),
                confidence=sp.confidence,
                extractor_version=extractor_version,
                caliber_version=caliber_version,
            )
        )
    return signals, rejections


def _classify_reject(
    sp: ProposedSpan, *, text: str, text_len: int
) -> ExtractionRejectionReason | None:
    """守门:候选不合格 → 返 typed 拒绝原因(落 extraction_rejections);合格 → None。歧义默认拒绝(C8 · 不猜)。

    注:PIT 泄漏在 extract() 内先短路(不进此函数)· 此处只处理**语料侧歧义/引文完整性**。
    """
    # 语义要件先判(语料侧信号质量 · 口径 5 要件 1-2):
    #   标的(要件 1)缺 → sector_only
    if not sp.ticker:
        return ExtractionRejectionReason.SECTOR_ONLY

    #   方向(要件 2)缺/非可交易 → no_direction
    if sp.direction is None or sp.direction not in _TRADEABLE_DIRECTIONS:
        return ExtractionRejectionReason.NO_DIRECTION

    # 引文可锚后判(提取器侧质量 · 要件 4):span 越界原文 = 假引文不可回锚 → 拒。
    #   ⚠ review IMPORTANT 修:原误标 no_timepoint(污染 rejection breakdown · 藏了幻觉/注入这个独立失败面)。
    #   现用专门 UNANCHORABLE_CITATION —— proposer 产不可锚 span 是注入/幻觉面(G-R3)· 宁拒不产假引文信号。
    if sp.span_start < 0 or sp.span_end > text_len or sp.span_end < sp.span_start:
        return ExtractionRejectionReason.UNANCHORABLE_CITATION

    # ⚠ 空白 span 硬拒(red-team + code-reviewer H1 · 2026-07-17):真 LLM 幻觉 offset 时 span 切片可能落在空
    #   /纯空白处(定义上不可锚 · 是幻觉铁证)→ 拒。**但不强要求 ticker 字面出现在 span 内**——M3' 的前提是
    #   隐性信号(分析师不显说 ticker),强字面匹配会误毙真隐性信号(operator 决:只拒空白 · 弱锚记 report 供审)。
    if not text[sp.span_start: sp.span_end].strip():
        return ExtractionRejectionReason.UNANCHORABLE_CITATION

    return None


def is_weakly_anchored(ticker: str, span_start: int, span_end: int, text: str) -> bool:
    """弱锚判定(审计用 · 非拒绝门 · H1 · operator 决:记 report 不毙):ticker core 不在 span 切片字面出现。

    结论:True = 引文 span 里字面找不到 ticker(可能是隐性信号 · 也可能是幻觉)· 供 operator 审引文质量率 ·
      **不**据此拒绝(隐性信号合法无字面 ticker)。census 汇总此计数入 report(弱锚率高 = 引文质量存疑)。
    细节:入参用裸 (ticker, span_start, span_end)· 不绑 ProposedSpan/SuspectedSignal 具体 model(两处都可调)。
    ⚠ 已知残留(red-team 复审 LOW · 接受):core 若与常见英文词撞(如 'ALL'/'ON'/'NOW')· 词界匹配仍会把无关文本里
      该词当强锚 → 弱锚率略低估。因 operator 决"不硬要求字面 ticker"(保隐性信号召回)· 此为刻意权衡的已知盲区 ·
      不加 stoplist(过度工程)· operator 抽查引文时留意此类 core。
    """
    if not ticker:
        return False
    core = ticker.split(".")[0]
    if not core:
        return False
    slice_text = text[span_start:span_end]
    # ⚠ word-boundary 匹配(red-team 复审 MEDIUM · 2026-07-17):裸子串会误判(如 core='A' 命中 'A股' → 假强锚)。
    #   用 \b 词界(同 literal_ticker_proposer 范式)· 短/常见 core 不再蹭无关文本的意外内嵌 → 弱锚计数更准。
    return re.search(r"\b" + re.escape(core) + r"\b", slice_text, re.IGNORECASE) is None
