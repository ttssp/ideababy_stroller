"""add_extraction_tables - T002 · 009-pM3prime E0 · 7 张信号提取头 009 自有表

Revision ID: 0017
Revises: 0016
Create Date: 2026-07-16T00:00:00

结论(T002 · 009-pM3prime E0 · O4 · 证伪链第一站建表):
  建 7 张 **009 自有表** 承载"疑似信号提取 → 密度普查 → 两层金标"的产物 + 记账 + 阈值预注册:
    1. extracted_signals       —— accepted 疑似信号(5 要件 + 引文锚定值 + 版本化)
    2. extraction_rejections   —— 歧义拒绝留痕(rejection_reason CHECK ⇔ T001 枚举逐字节)
    3. trial_ledger            —— 试验记账(row_kind 两态:caliber_preregistration marker / e1_trial)
    4. density_threshold       —— 预注册密度阈值(per market×horizon · 幂等 UNIQUE · C6 不可回改)
    5. gold_layer1_result      —— 金标 Layer-1 span 验收(α/P/R/F1)
    6. gold_layer2_result      —— 金标 Layer-2 映射验收(mapping_agreement_rate · 真人第二源)
    7. record_tickers_judgment —— record_tickers 语义判定(三选一 + 复用/校验/重建)

核心红线(为什么这么设计):
  1. **只 ADD 不 alter 004 表**(C7 · OUT-7):迁移体只含 CREATE(TABLE/INDEX)· 0 处 ALTER/DROP/UPDATE/
     INSERT 命中 004 生产表(advisor_reports/strategy_signals/watchlist/price_daily/conflict_reports)·
     不撞 advisor_reports UNIQUE INDEX(week_id,source_id)。单测 test_migration_0017_adds_only_no_004_mutation 守。
  2. **跨 DB 无 FK**(C11):extracted_signals 的 citation(source_id+raw_ref+span offset)存**值**,
     **不** REFERENCES records —— records 在 collection.db **另一文件**,SQLite 跨 DB FK 不可能。存值可
     回查 collection.db 复核(T011 回锚测)。同理 record_tickers_judgment 不 FK 到 record_tickers。
  3. **rejection_reason CHECK ⇔ T001 枚举逐字节**:CHECK 值从 `ExtractionRejectionReason` **导出**(见
     `_REJECTION_REASON_CHECK`),**不手抄**(手抄易漂 · T001 冻结集变则此处自动跟随)。单测
     test_extraction_rejections_check_covers_exactly_t001_enum + test_should_accept_all_t001_rejection_reasons 守。
  4. **trial_ledger row_kind 两态 CHECK**(解 red-team R1 矛盾核心):E0 preregister 写 marker 行时 grain
     列(extractor_variant/horizon)尚不存在 → marker 行允许 NULL;E1 census 写 e1_trial 行时 grain 必须齐 →
     `row_kind='e1_trial' ⇒ extractor_variant IS NOT NULL AND horizon IS NOT NULL`。O11/C1 完整性只数
     e1_trial 行(marker 不进 DSR/PBO 分母)。
  5. **forward-only**(TECH-8):downgrade raise NotImplementedError(跟 004 0010-0016 同 pattern)。

细节(T002 file_domain 内):
  - horizon CHECK ∈ {5,20,60}(对齐 M2 SLA C16 · 未来 E2 回测复用)。
  - direction CHECK ∈ {long,short}(可交易方向 · 对齐口径 5 要件 2 · neutral/wait 不产样本)。
  - density_threshold UNIQUE(market,horizon,caliber_version)保 preregister 幂等(重跑不重复插)。
  - UPGRADE_SQL 提为模块常量 list[str]:upgrade() 经 op.execute 跑;单测按文件路径 import 复用同一份 SQL(不 mock)。
"""

from __future__ import annotations

from collections.abc import Sequence

from alembic import op

from decision_ledger.extraction.caliber import ExtractionRejectionReason

revision: str = "0017"
down_revision: str | None = "0016"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


# ── rejection_reason CHECK 子句从 T001 枚举导出(逐字节一致 · 防手抄漂移)──────────────
# 结论:CHECK IN (...) 的值集 == ExtractionRejectionReason 全集。T001 改枚举 → 此处自动跟随。
# red-team R3:值内单引号必须 SQL 转义(''),否则未来某枚举值含 ' 会破 DDL 语法/被重解释。
# 当前 6 值全 snake_case 无引号(dormant),但转义 = 让未来低摩擦改枚举也安全(本 module 的设计初衷)。
_REJECTION_REASON_CHECK: str = ", ".join(
    "'{}'".format(reason.value.replace("'", "''")) for reason in ExtractionRejectionReason
)


# ── DDL 常量(single source · upgrade() 与单测共用 · 不 mock)──────────────────────

# 1. extracted_signals:accepted 疑似信号(5 要件 + 引文锚定值 + 版本化维度)
# 跨 DB 无 FK(C11):citation 三段(source_id + raw_ref + span_start/span_end)存值可回查 collection.db。
_EXTRACTED_SIGNALS_SQL = """
CREATE TABLE extracted_signals (
    id                 INTEGER PRIMARY KEY AUTOINCREMENT,
    -- ── 引文锚定(C3 · 跨 DB 存值不设 FK · 可回查 collection.db 复核)──
    source_id          TEXT    NOT NULL,          -- collection.db records.source_id(存值 · 非 FK)
    raw_ref            TEXT    NOT NULL,           -- raw-* 原文引用(存值 · 非 FK)
    span_start         INTEGER NOT NULL CHECK (span_start >= 0),   -- 原文片段起始偏移(回锚切片)
    span_end           INTEGER NOT NULL CHECK (span_end >= span_start),  -- 结束偏移 ≥ 起始
    -- ── 5 要件(口径 v1 · caliber.SuspectedSignal)──
    ticker             TEXT    NOT NULL,
    direction          TEXT    NOT NULL
                       CHECK (direction IN ('long','short')),   -- 可交易方向(口径要件 2 · neutral/wait 不产样本)
    published_at       TEXT    NOT NULL,           -- 权威 PIT 时点(口径要件 3 · C2 文本 PIT 基准)
    confidence         REAL    NOT NULL
                       CHECK (confidence >= 0.0 AND confidence <= 1.0),   -- 置信 ∈ [0,1](要件 5)
    -- ── 版本化维度(每 trial 记账 · 温度 0 确定性锚 · D-9)──
    extractor_variant  TEXT    NOT NULL,           -- 提取器变体(温度 0 · 版本钉死)
    caliber_version    TEXT    NOT NULL,           -- 口径版本(对齐 trial_ledger 记账维度)
    created_at         TEXT    NOT NULL
)
"""

# 2. extraction_rejections:歧义拒绝留痕(rejection_reason CHECK ⇔ T001 枚举)
_EXTRACTION_REJECTIONS_SQL = f"""
CREATE TABLE extraction_rejections (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    source_id        TEXT    NOT NULL,             -- 被拒记录(存值 · 跨 DB 非 FK)
    raw_ref          TEXT    NOT NULL,
    rejection_reason TEXT    NOT NULL
                     CHECK (rejection_reason IN ({_REJECTION_REASON_CHECK})),   -- ⇔ T001 ExtractionRejectionReason 逐字节
    caliber_version  TEXT    NOT NULL,
    created_at       TEXT    NOT NULL
)
"""

# 3. trial_ledger:试验记账(row_kind 两态 · 解 red-team R1 矛盾核心)
# marker 行(caliber_preregistration):extractor_variant/horizon 允许 NULL(E0 时 grain 未定)。
# e1_trial 行:extractor_variant/horizon 必须 NOT NULL(E1 census 记账 · O11/C1 完整性只数此)。
# sampled_source_ids:抽中 source_id 集(JSON · 可复现抽样 · D-12 不可改)。
_TRIAL_LEDGER_SQL = """
CREATE TABLE trial_ledger (
    id                 INTEGER PRIMARY KEY AUTOINCREMENT,
    row_kind           TEXT    NOT NULL
                       CHECK (row_kind IN ('caliber_preregistration','e1_trial')),
    caliber_version    TEXT    NOT NULL,           -- 两态都必带口径版本
    extractor_variant  TEXT,                        -- e1_trial 必填 · marker 允许 NULL(下方两态 CHECK 守)
    horizon            INTEGER
                       CHECK (horizon IS NULL OR horizon IN (5,20,60)),   -- 合约 horizon 集(M2 C16)
    market             TEXT
                       CHECK (market IS NULL OR market IN ('US','CN','HK')),  -- e1_trial 可携带 market(密度 per-market)
    sampled_source_ids TEXT,                        -- 抽中 source_id 集(JSON · 可复现 · D-12)
    caliber_hash       TEXT,                        -- marker 行钉口径正文 hash(O1 gate · 对齐附录 A)
    created_at         TEXT    NOT NULL,
    -- 两态 CHECK:e1_trial ⇒ grain 全非空(解 red-team R1 · E0 marker 无 grain 合法)
    CHECK (
        row_kind <> 'e1_trial'
        OR (extractor_variant IS NOT NULL AND horizon IS NOT NULL)
    )
)
"""

# 4. density_threshold:预注册密度阈值(per market×horizon · 幂等 · C6 不可回改)
# UNIQUE(market,horizon,caliber_version)保 preregister 幂等(重跑不重复插)。
_DENSITY_THRESHOLD_SQL = """
CREATE TABLE density_threshold (
    id                    INTEGER PRIMARY KEY AUTOINCREMENT,
    market                TEXT    NOT NULL
                          CHECK (market IN ('US','CN','HK')),   -- 对齐 004 Market enum
    horizon               INTEGER NOT NULL
                          CHECK (horizon IN (5,20,60)),          -- 合约 horizon 集(M2 C16)
    min_density_threshold INTEGER NOT NULL
                          CHECK (min_density_threshold >= 0),    -- 每 stratum 最低合格疑似信号数
    caliber_version       TEXT    NOT NULL,
    threshold_hash        TEXT,                                   -- 附录 B hash(operator 签字后钉 · O3 gate)
    created_at            TEXT    NOT NULL,
    UNIQUE (market, horizon, caliber_version)                     -- preregister 幂等键
)
"""

# density_threshold C6 不可回改 —— **DB 层强制**(red-team R1:UNIQUE 只挡重复 INSERT · 裸 UPDATE 能悄悄改)。
# 结论:预注册阈值一经写入,任何 UPDATE 都 RAISE(ABORT)· 改阈值只能新增 caliber_version(可审计)· 绝不
#   在 DB 层改行。这把 C6「普查后改阈值 = BLOCK」从「靠约定」升为「靠 schema」—— 防未来脚本/直连 DB 悄悄
#   把「密度不足」用改阈值粉饰过去(违证伪链诚实停语义)。T012 契约测断言此 UPDATE 被拒。
_DENSITY_THRESHOLD_IMMUTABLE_TRIGGER_SQL = """
CREATE TRIGGER density_threshold_no_update
BEFORE UPDATE ON density_threshold
BEGIN
    SELECT RAISE(ABORT,
        'C6: density_threshold 预注册不可回改 · 改阈值请新增 caliber_version(不在 DB 层 UPDATE)');
END
"""

# 5. gold_layer1_result:金标 Layer-1 span 验收(α/P/R/F1 · T007 写)
_GOLD_LAYER1_RESULT_SQL = """
CREATE TABLE gold_layer1_result (
    id                 INTEGER PRIMARY KEY AUTOINCREMENT,
    krippendorff_alpha REAL    NOT NULL,           -- 标注者间一致性
    span_precision     REAL    NOT NULL,
    span_recall        REAL    NOT NULL,
    span_f1            REAL    NOT NULL,
    passed             INTEGER CHECK (passed IS NULL OR passed IN (0,1)),  -- vs 预注册门槛(过=1)
    second_annotator   TEXT,                         -- 第二标注源标记(C9 · Layer-1 可 LLM+人混)
    arbitration_note   TEXT,                         -- 分歧仲裁留痕
    caliber_version    TEXT    NOT NULL,
    created_at         TEXT    NOT NULL
)
"""

# 6. gold_layer2_result:金标 Layer-2 映射验收(mapping_agreement_rate · 真人第二源 · T008 写)
_GOLD_LAYER2_RESULT_SQL = """
CREATE TABLE gold_layer2_result (
    id                     INTEGER PRIMARY KEY AUTOINCREMENT,
    mapping_agreement_rate REAL    NOT NULL,         -- sector/ticker/方向/horizon/时点映射一致率
    passed                 INTEGER CHECK (passed IS NULL OR passed IN (0,1)),
    human_second_source    TEXT,                      -- 真人第二标注源标记(D-7 · 非 LLM · C9)
    arbitration_note       TEXT,                      -- 分歧仲裁留痕
    caliber_version        TEXT    NOT NULL,
    created_at             TEXT    NOT NULL
)
"""

# 7. record_tickers_judgment:record_tickers 语义判定(三选一 + 复用/校验/重建 · T004 写)
_RECORD_TICKERS_JUDGMENT_SQL = """
CREATE TABLE record_tickers_judgment (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    semantic_label      TEXT    NOT NULL
                        CHECK (semantic_label IN
                            ('weak_association','title_match','disambiguated_candidate')),
    resolution_decision TEXT    NOT NULL
                        CHECK (resolution_decision IN ('reuse','verify','rebuild')),
    evidence_query      TEXT    NOT NULL,            -- 复现证据 SQL 串(可回跑核对判定)
    sample_size         INTEGER CHECK (sample_size IS NULL OR sample_size >= 0),  -- 抽样比对样本量
    caliber_version     TEXT    NOT NULL,
    created_at          TEXT    NOT NULL
)
"""

# 查询索引(009 自有表内 · 不撞 004)
_EXTRACTED_SIGNALS_SOURCE_IDX_SQL = """
CREATE INDEX idx_extracted_signals_source ON extracted_signals (source_id, caliber_version)
"""
_TRIAL_LEDGER_GRAIN_IDX_SQL = """
CREATE INDEX idx_trial_ledger_grain
    ON trial_ledger (row_kind, extractor_variant, caliber_version, horizon)
"""


# 单测复用:每个元素是一条可 executescript 的 DDL(顺序执行)
UPGRADE_SQL: list[str] = [
    _EXTRACTED_SIGNALS_SQL,
    _EXTRACTION_REJECTIONS_SQL,
    _TRIAL_LEDGER_SQL,
    _DENSITY_THRESHOLD_SQL,
    _DENSITY_THRESHOLD_IMMUTABLE_TRIGGER_SQL,  # red-team R1:C6 不可回改 DB 层强制(裸 UPDATE 被拒)
    _GOLD_LAYER1_RESULT_SQL,
    _GOLD_LAYER2_RESULT_SQL,
    _RECORD_TICKERS_JUDGMENT_SQL,
    _EXTRACTED_SIGNALS_SOURCE_IDX_SQL,
    _TRIAL_LEDGER_GRAIN_IDX_SQL,
]


def upgrade() -> None:
    """建 7 张 009-pM3prime 信号提取头自有表(O4 · 只 ADD 不动 004)。

    结论:证伪链 E0 建表 —— extracted_signals/extraction_rejections/trial_ledger/density_threshold/
    gold_layer1_result/gold_layer2_result/record_tickers_judgment。
    细节:只新增 7 表 + 2 索引,不动 004 已 ship 表(C7 · OUT-7)· 跨 DB 无 FK(C11)· rejection_reason
    CHECK 从 T001 枚举导出(逐字节 · 防漂移)· trial_ledger row_kind 两态(解 red-team R1)。
    """
    for stmt in UPGRADE_SQL:
        op.execute(stmt)


def downgrade() -> None:
    """v0.1 TECH-8 forward-only(跟 004 0010-0016 同 pattern)。"""
    raise NotImplementedError(
        "alembic 0017 不可 downgrade · v0.1 设计 TECH-8 forward-only · "
        "7 张 009 信号提取头表建表是 forward-only schema 演进(跟 0010-0016 同)"
    )
