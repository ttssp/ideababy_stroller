"""extraction/caliber.py — T001 · 009-pM3prime E0 · 疑似信号口径定义源(证伪链第一站)。

结论(先):这是证伪链 E0 的**口径预注册源**。定义三样冻结物(O1/O2/O3):
  1. `CALIBER_VERSION`:口径版本号(trial_ledger 记账维度 · immutable-hash 锚 · 改口径 = 新版本非改 v1)。
  2. `ExtractionRejectionReason`:提取层歧义拒绝原因 StrEnum(≥6 · 与口径 5 要件闭合)——
     后续 0017 `extraction_rejections` 表 CHECK 逐字节 echo 此集(T002 migration test 守一致)。
  3. `SuspectedSignal` + `Citation`:frozen pydantic model,承载"一条可评估疑似信号"5 要件 ——
     提取器 T005 与 census T006 的产物 schema。

核心红线(为什么这么设计 · 对齐 009-pForge M2 join.py 精神):
  1. **歧义默认拒绝**(C8 · D-6):方向/时点/标的任一歧义 → 各自落 typed rejection,**绝不 best-effort 猜**。
     放松口径 = 把噪声当信号,污染下游密度普查真数字。
  2. **可交易方向唯一**:direction 只收 long/short(产 signed 样本 · 对齐 M2 _TRADEABLE_DIRECTIONS);
     neutral/wait/观望不产样本 → 不进 SuspectedSignal(也非 rejection · 静默跳过)。
  3. **引文锚定必填**(C3):每条疑似信号带 source_id + raw_ref + span offset,可回查 collection.db 原文
     复核(跨 DB 存值不设 FK · 0017 注释写明)。缺引文 = 不可复核 = 拒。
  4. **PIT 时间基准唯一**:published_at 是权威时点(秒级)· 缺则 no_timepoint 拒(C2 文本 PIT 依赖它守未来不可达)。

E0 不碰 LLM(D-11):本模块**纯 schema/枚举/常量**,零 LLM 依赖(单测 test_should_not_import_llm 守此)。
首次真 LLM 提取在 E1(T005 extractor / T006 census)。

边界(本 module 只做):产口径 schema + 枚举 + 版本常量。**不建表**(T002)· **不写 preregister**(T003)·
  **不跑提取器**(T005)。密度阈值**推算方法**在 spec 附录 B 冻结,**具体数值须 operator 签字**(OQ-3 · C6)。
"""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, model_validator


# ── O1 · 口径版本(immutable-hash 锚 · trial_ledger 记账维度)────────────────────────
# 改口径规则 = 新 caliber_version(如 v2),不是改 v1 内容 —— 保证 spec 附录 A 的 caliber_hash 与
# trial_ledger caliber_preregistration marker 行一一对应可审计(O1 · T001 时刻 gate)。
CALIBER_VERSION: str = "v1"


class ExtractionRejectionReason(StrEnum):
    """提取层歧义拒绝原因枚举 —— 严格对齐 0017 extraction_rejections CHECK(rev-T002)。

    落库值必须 ∈ 此集合,否则 0017 CHECK 拒插(T002 migration test test_should_reject_*_reason 守此)。
    枚举**最终集本 module 冻结**(spec 附录 A);T002 的 CHECK 从本枚举**导出**不手抄(防漂移)。

    与口径 5 要件的闭合关系(每个要件的缺失/歧义面都有对应拒绝原因):
      - 标的(要件 1)缺/歧义 → SECTOR_ONLY / MULTI_TICKER_UNSPLITTABLE
      - 方向(要件 2)缺  → NO_DIRECTION
      - 时点(要件 3)缺  → NO_TIMEPOINT
      - 出处引文(要件 4)不可回锚 → UNANCHORABLE_CITATION(span 越界原文 · proposer 产假引文/幻觉 · G-R3 注入面)
      - 非信号语句(非可评估疑似信号)→ PURE_IDEOLOGY / IRONY_OR_QUOTING_OTHERS
    """

    SECTOR_ONLY = "sector_only"                          # 只提板块/主题 · 无具体可交易 ticker
    NO_DIRECTION = "no_direction"                        # 无 long/short 方向语义(纯陈述/中性)
    NO_TIMEPOINT = "no_timepoint"                        # 无权威 published_at 时点(PIT 基准缺)
    UNANCHORABLE_CITATION = "unanchorable_citation"      # 引文 span 越界原文 · 不可回锚(要件 4 · review 修:原误标 no_timepoint)
    MULTI_TICKER_UNSPLITTABLE = "multi_ticker_unsplittable"  # 一句涉多 ticker 且无法拆成独立信号
    PURE_IDEOLOGY = "pure_ideology"                      # 纯立场/宏观情绪表达 · 非针对标的的可评估信号
    IRONY_OR_QUOTING_OTHERS = "irony_or_quoting_others"  # 反讽/转述他人观点 · 非作者自身信号


# 可交易方向:SuspectedSignal 只收 long/short(产 signed 样本 · 对齐 M2 alpha/join.py _TRADEABLE_DIRECTIONS)。
# neutral/wait/no_view 不产疑似信号样本(既非 accepted 也非 rejection · 静默跳过)。
_TRADEABLE_DIRECTIONS = frozenset({"long", "short"})


class Citation(BaseModel):
    """引文锚定(C3)—— 疑似信号回查 collection.db 原文的坐标。

    跨 DB 存**值**不设 FK(records 在 collection.db 另一文件 · 0017 注释写明):
      - source_id + raw_ref 定位原文记录 · span_start/span_end 定位原文内片段偏移。
    T011 回锚测据此把 citation 切回 raw 原文比对(span_end ≥ span_start · offset 非负)。
    """

    model_config = ConfigDict(frozen=True)

    source_id: str = Field(min_length=1)      # collection.db records.source_id(定位原文记录)
    raw_ref: str = Field(min_length=1)        # raw-* 文件/字段引用(定位原文体)
    span_start: int = Field(ge=0)             # 原文内片段起始偏移(非负)
    span_end: int = Field(ge=0)               # 原文内片段结束偏移(非负)

    @model_validator(mode="after")
    def _validate_span_order(self) -> Citation:
        """span_end ≥ span_start(回锚切片有效 · 空 span 允许 start==end 表零长锚点)。"""
        if self.span_end < self.span_start:
            raise ValueError(
                f"引文 span 非法:span_end({self.span_end}) < span_start({self.span_start})"
            )
        return self


class SuspectedSignal(BaseModel):
    """一条可评估疑似信号 —— 提取器 T005 / census T006 的产物 schema(5 要件 + 版本化维度)。

    5 构成要件(spec 附录 A · T001 冻结):
      1. ticker    —— 显式或可无歧义映射的可交易标的(歧义 → sector_only/multi_ticker_unsplittable 拒)。
      2. direction —— long/short(无方向 → no_direction 拒 · neutral/观望不产样本)。
      3. published_at —— 权威时点(秒级 · 缺 → no_timepoint 拒 · PIT 基准)。
      4. citation  —— 引文锚定(C3 · 可回查 collection.db)。
      5. confidence —— 提取器置信度(schema 字段 · 不作硬门槛)。
    版本化维度:extractor_version + caliber_version(每 trial 记账 · 温度 0 确定性锚 · D-9)。

    frozen:产物一经产出不可篡改(对齐 join.ResolvedSignal · 防 census 途中被改)。
    """

    model_config = ConfigDict(frozen=True)

    ticker: str = Field(min_length=1)
    direction: str                            # long/short(可交易方向 · 下方 validator 守)
    published_at: str = Field(min_length=1)   # ISO-8601 秒级 · 权威 PIT 时点
    citation: Citation                        # 引文锚定(C3 · 必填)
    confidence: float = Field(ge=0.0, le=1.0)
    extractor_version: str = Field(min_length=1)
    caliber_version: str = Field(min_length=1)

    @model_validator(mode="after")
    def _validate_tradeable_direction(self) -> SuspectedSignal:
        """方向只收 long/short(可交易 · neutral/wait/no_view 不产样本 · 对齐 M2)。"""
        if self.direction not in _TRADEABLE_DIRECTIONS:
            raise ValueError(
                f"direction 非可交易方向:{self.direction!r}(只收 {sorted(_TRADEABLE_DIRECTIONS)})· "
                "neutral/wait/观望不产疑似信号样本"
            )
        return self


# ── 口径 5 要件判定规则的结构化文档串(供 spec 附录 A 引用 · 人可读 · 版本化)──────────────
# 结论:这是"一条可评估疑似信号"的**判定口径正文**,冻结进 spec 附录 A 并计算 caliber_hash。
# 改任一条 = 新 caliber_version(可审计),不是改 v1。
CALIBER_DOC: str = """\
疑似信号口径 v1(caliber_version=v1)· 一条可评估疑似信号须同时满足 5 要件:

要件 1 · 标的(ticker):
  - 显式 ticker,或可无歧义映射到单一可交易 ticker 的标的指称。
  - 只提板块/主题(无具体 ticker)→ sector_only 拒。
  - 一句涉多个 ticker 且无法拆成各自独立信号 → multi_ticker_unsplittable 拒。
  - 标的映射权威源见 T004 record_tickers 语义判定(倾向 verify 非直接 reuse)。

要件 2 · 方向(direction):
  - 明确 long / short 语义(看多建仓 / 看空做空)。
  - 无方向语义(纯陈述/中性/观望)→ no_direction 拒。
  - neutral / wait / 观望**不产样本**(既非 accepted 也非 rejection · 静默跳过)。

要件 3 · 时点(published_at):
  - 权威 published_at(ISO-8601 秒级)· 提取只可用 ≤ 此时点的内容(C2 文本 PIT)。
  - 缺权威时点 → no_timepoint 拒。

要件 4 · 出处引文(citation):
  - 原文锚定 = source_id + raw_ref + span offset · 可回查 collection.db 复核(C3)。
  - 跨 DB 存值不设 FK(records 在 collection.db 另一文件)。

要件 5 · 置信(confidence):
  - 提取器给出的置信度 ∈ [0,1](schema 字段 · 不作硬门槛 · 供下游分析)。

歧义默认拒绝(C8):任一要件歧义 → 落对应 typed rejection,绝不 best-effort 猜。
非信号语句:纯立场/宏观情绪 → pure_ideology;反讽/转述他人 → irony_or_quoting_others。
"""
