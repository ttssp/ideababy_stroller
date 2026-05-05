# ruff: noqa: E501
"""initial_schema

Revision ID: 0001
Revises:
Create Date: 2026-04-26T00:00:00

结论: 创建决策账本所有核心 SQLite 表 + 索引，含 R2 修订 (decision_drafts / status / market)
细节:
  - 11 张核心表: decisions / decision_drafts / env_snapshots / conflict_reports /
    strategy_signals / rebuttals / advisor_reports / watchlist / notes / alerts / llm_usage
  - WAL + foreign_keys 由 env.py 的 event listener 在 connect 时设置
  - 仅用 raw SQL DDL（op.execute），不引入 SQLAlchemy ORM（tech-stack §1）
  - downgrade 完整可逆（TECH-8 要求）
  - 所有 CHECK constraints 严格对齐架构 §3.2 + §9 不变量
  - file-level noqa E501: SQL DDL 多行字符串内的中文注释允许长行 (semantic clarity > line width)
"""

from __future__ import annotations

from collections.abc import Sequence

from alembic import op

# revision identifiers
revision: str = "0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """
    结论: 创建所有核心表 + 索引。
    细节: 顺序按外键依赖排列（被依赖表先建）。
    """
    # ──────────────────────────────────────────────────────────
    # 1. env_snapshots — 决策当时不可变快照 (被 decisions / decision_drafts 引用)
    # ──────────────────────────────────────────────────────────
    op.execute("""
        CREATE TABLE env_snapshots (
            snapshot_id   TEXT PRIMARY KEY,
            price         REAL,                    -- human 录入 / Proxyman 同步; v0.1 可空
            holdings_pct  REAL,                    -- 该 ticker 占组合比例; 可空
            holdings_abs  REAL,                    -- 绝对持仓金额 (USD); 可空
            advisor_week_id TEXT,                  -- 关联当周 AdvisorReport id; 可空
            snapshot_at   TEXT NOT NULL            -- ISO 8601 datetime
        )
    """)

    # ──────────────────────────────────────────────────────────
    # 2. advisor_reports — 咨询师周报 (被 strategy_signals 引用)
    #    R8/R20 红线: source_id 字段必须存在（未来多来源支持）
    # ──────────────────────────────────────────────────────────
    op.execute("""
        CREATE TABLE advisor_reports (
            advisor_id      TEXT PRIMARY KEY,
            source_id       TEXT NOT NULL,          -- R8/R20 红线: 来源标识 e.g. "columbia_advisor_v1"
            week_id         TEXT NOT NULL,           -- e.g. "2026-W17"
            raw_text        TEXT NOT NULL,
            structured_json TEXT NOT NULL,           -- LLM 结构化输出 JSON
            ingested_at     TEXT NOT NULL            -- ISO 8601 datetime
        )
    """)
    op.execute("""
        CREATE UNIQUE INDEX idx_advisor_reports_week_source
            ON advisor_reports (week_id, source_id)
    """)

    # ──────────────────────────────────────────────────────────
    # 3. strategy_signals — StrategyModule.analyze() 输出 (被 conflict_reports 引用)
    # ──────────────────────────────────────────────────────────
    op.execute("""
        CREATE TABLE strategy_signals (
            signal_id     TEXT PRIMARY KEY,
            source_id     TEXT NOT NULL,                -- "advisor" | "placeholder_model" | "agent_synthesis"
            ticker        TEXT NOT NULL,
            direction     TEXT NOT NULL CHECK (direction IN ('long','short','neutral','wait','no_view')),
            confidence    REAL NOT NULL CHECK (confidence >= 0.0 AND confidence <= 1.0),
            rationale_plain TEXT NOT NULL CHECK (length(rationale_plain) > 0),  -- R3 红线: 必须非空
            inputs_used_json TEXT NOT NULL,            -- JSON dict {"advisor_week_id":..., "price_at":...}
            created_at    TEXT NOT NULL
        )
    """)
    op.execute("""
        CREATE INDEX idx_strategy_signals_ticker_source
            ON strategy_signals (ticker, source_id)
    """)

    # ──────────────────────────────────────────────────────────
    # 4. conflict_reports — ConflictReportAssembler 输出
    #    R10 红线: 无 priority / winner / recommended 字段
    #    不变量 #2: signals ≥ 3 (由 service 层 + pydantic 保证, DDL 记录 ref)
    # ──────────────────────────────────────────────────────────
    op.execute("""
        CREATE TABLE conflict_reports (
            report_id            TEXT PRIMARY KEY,
            divergence_root_cause TEXT NOT NULL CHECK (length(divergence_root_cause) > 0),
            has_divergence       INTEGER NOT NULL CHECK (has_divergence IN (0,1)),
            rendered_order_seed  INTEGER NOT NULL,   -- R2 D22: hash(sources+day)%N, UI 随机化三列顺序
            signals_json         TEXT NOT NULL,      -- JSON 列表存储 signal_id 引用 (≥3, service 层校验)
            created_at           TEXT NOT NULL
            -- 无 priority / winner / recommended 字段 (R10 红线)
        )
    """)

    # ──────────────────────────────────────────────────────────
    # 5. rebuttals — DevilAdvocateService 输出 (≤ 80 字反驳)
    # ──────────────────────────────────────────────────────────
    op.execute("""
        CREATE TABLE rebuttals (
            rebuttal_id   TEXT PRIMARY KEY,
            rebuttal_text TEXT NOT NULL
                CHECK (length(rebuttal_text) > 0 AND length(rebuttal_text) <= 80),
            invoked_at    TEXT NOT NULL
        )
    """)

    # ──────────────────────────────────────────────────────────
    # 6. decision_drafts — R2 新增 D13: draft 阶段临时草稿
    #    INSERT 时 refs 可空（asyncio.gather 完成后 UPDATE）
    # ──────────────────────────────────────────────────────────
    op.execute("""
        CREATE TABLE decision_drafts (
            draft_id             TEXT PRIMARY KEY,
            ticker               TEXT NOT NULL,
            intended_action      TEXT NOT NULL
                CHECK (intended_action IN ('buy','sell','hold','wait')),
            draft_reason         TEXT NOT NULL
                CHECK (length(draft_reason) > 0 AND length(draft_reason) <= 80),
            env_snapshot_json    TEXT NOT NULL,      -- JSON 序列化的 EnvSnapshot
            conflict_report_ref  TEXT,               -- INSERT 时 NULL, gather 完成后 UPDATE
            devils_rebuttal_ref  TEXT,               -- INSERT 时 NULL, gather 完成后 UPDATE
            status               TEXT NOT NULL
                CHECK (status IN ('draft','committed','abandoned'))
                DEFAULT 'draft',
            created_at           TEXT NOT NULL,
            committed_at         TEXT,               -- commit 时填
            abandoned_at         TEXT,               -- 30min GC 或 human 弃用时填
            FOREIGN KEY (conflict_report_ref) REFERENCES conflict_reports (report_id),
            FOREIGN KEY (devils_rebuttal_ref) REFERENCES rebuttals (rebuttal_id)
        )
    """)
    op.execute("""
        CREATE INDEX idx_drafts_status_created
            ON decision_drafts (status, created_at)
    """)
    # GC 任务: status='draft' AND created_at < now()-30min → status='abandoned' (不变量 #12)

    # ──────────────────────────────────────────────────────────
    # 7. decisions — 主决策档案 (R2 修订: 加 status / would_have_acted_without_agent NOT NULL)
    # ──────────────────────────────────────────────────────────
    op.execute("""
        CREATE TABLE decisions (
            trade_id                        TEXT PRIMARY KEY,
            ticker                          TEXT NOT NULL,
            action                          TEXT NOT NULL
                CHECK (action IN ('buy','sell','hold','wait')),  -- 不变量 #3: 必含 hold+wait
            reason                          TEXT NOT NULL
                CHECK (length(reason) > 0 AND length(reason) <= 80),
            pre_commit_at                   TEXT NOT NULL,
            env_snapshot_json               TEXT NOT NULL,       -- JSON 序列化的 EnvSnapshot
            conflict_report_ref             TEXT NOT NULL,       -- R2: 必填, draft 阶段生成
            devils_rebuttal_ref             TEXT NOT NULL,       -- R2: 必填, draft 阶段生成
            post_mortem_json                TEXT,                -- 可空, N 天后回填
            would_have_acted_without_agent  INTEGER NOT NULL
                CHECK (would_have_acted_without_agent IN (0,1)),  -- R2 M1: 强制 yes/no, 无默认
            status                          TEXT NOT NULL
                CHECK (status IN ('draft','committed','abandoned'))
                DEFAULT 'committed',          -- R2 D8 新增; commit 路径默认 committed
            created_at                      TEXT NOT NULL,
            updated_at                      TEXT NOT NULL,
            FOREIGN KEY (conflict_report_ref) REFERENCES conflict_reports (report_id),
            FOREIGN KEY (devils_rebuttal_ref) REFERENCES rebuttals (rebuttal_id)
        )
    """)
    op.execute("""
        CREATE INDEX idx_decisions_ticker_pre_commit
            ON decisions (ticker, pre_commit_at)
    """)
    op.execute("""
        CREATE INDEX idx_decisions_action
            ON decisions (action)
    """)
    op.execute("""
        CREATE INDEX idx_decisions_status
            ON decisions (status)
    """)

    # ──────────────────────────────────────────────────────────
    # 8. watchlist — 关注股清单 (R2 D24: 加 market 字段)
    # ──────────────────────────────────────────────────────────
    op.execute("""
        CREATE TABLE watchlist (
            ticker       TEXT PRIMARY KEY,
            market       TEXT NOT NULL
                CHECK (market IN ('US','HK','CN'))
                DEFAULT 'US',                -- R2 D24: per-market session config
            display_name TEXT               -- 可选显示名称
        )
    """)

    # ──────────────────────────────────────────────────────────
    # 9. notes — 笔记 wiki (content_hash 去重)
    # ──────────────────────────────────────────────────────────
    op.execute("""
        CREATE TABLE notes (
            note_id      TEXT PRIMARY KEY,
            title        TEXT NOT NULL,
            content      TEXT NOT NULL,
            tags_json    TEXT NOT NULL DEFAULT '[]',   -- JSON 字符串列表
            content_hash TEXT NOT NULL,                -- sha256(content), 去重 key
            created_at   TEXT NOT NULL,
            updated_at   TEXT NOT NULL
        )
    """)
    op.execute("""
        CREATE UNIQUE INDEX idx_notes_content_hash
            ON notes (content_hash)
    """)

    # ──────────────────────────────────────────────────────────
    # 10. alerts — 失败告警 (O10) + meta_decisions (B-lite 切换, 架构 §5)
    # ──────────────────────────────────────────────────────────
    op.execute("""
        CREATE TABLE alerts (
            alert_id     TEXT PRIMARY KEY,
            alert_type   TEXT NOT NULL
                CHECK (alert_type IN ('low_decision_rate','parse_failure','llm_timeout','telegram_failure')),
            severity     TEXT NOT NULL
                CHECK (severity IN ('info','warning','critical')),
            body         TEXT NOT NULL,
            created_at   TEXT NOT NULL,
            dismissed_at TEXT                          -- human 确认后填入; 可空
        )
    """)
    op.execute("""
        CREATE INDEX idx_alerts_type_created
            ON alerts (alert_type, created_at)
    """)

    # ──────────────────────────────────────────────────────────
    # 11. llm_usage — LLM API 调用成本日志 (架构 §10 M4)
    #     D21 cache 命中率监控 + R2 Q11 latency 监控
    # ──────────────────────────────────────────────────────────
    op.execute("""
        CREATE TABLE llm_usage (
            call_id                  TEXT PRIMARY KEY,
            service                  TEXT NOT NULL,    -- "ConflictReportAssembler" | "AdvisorStrategy.analyze" | ...
            model                    TEXT NOT NULL,    -- "claude-sonnet-4-6"
            prompt_template_version  TEXT NOT NULL,    -- e.g. "conflict_v1"
            prompt_tokens            INTEGER NOT NULL,
            output_tokens            INTEGER NOT NULL,
            cost_usd                 REAL NOT NULL,
            cache_hit                INTEGER NOT NULL CHECK (cache_hit IN (0,1)),  -- D21 监控
            latency_ms               INTEGER NOT NULL,                             -- R2 Q11 监控
            created_at               TEXT NOT NULL
        )
    """)
    op.execute("""
        CREATE INDEX idx_llm_usage_service_created
            ON llm_usage (service, created_at)
    """)
    op.execute("""
        CREATE INDEX idx_llm_usage_cache_hit
            ON llm_usage (cache_hit)
    """)


def downgrade() -> None:
    """
    结论: 删除所有表（顺序与 upgrade 相反，先删依赖方）。
    细节: migration 可逆（TECH-8），即使 v0.1 永远不 downgrade。
    """
    # 先删索引（SQLite 不用显式 DROP INDEX for tables，但 DROP TABLE 会同时删除）
    # 按外键依赖反向删除
    op.execute("DROP TABLE IF EXISTS llm_usage")
    op.execute("DROP TABLE IF EXISTS alerts")
    op.execute("DROP TABLE IF EXISTS notes")
    op.execute("DROP TABLE IF EXISTS watchlist")
    op.execute("DROP TABLE IF EXISTS decisions")
    op.execute("DROP TABLE IF EXISTS decision_drafts")
    op.execute("DROP TABLE IF EXISTS rebuttals")
    op.execute("DROP TABLE IF EXISTS conflict_reports")
    op.execute("DROP TABLE IF EXISTS strategy_signals")
    op.execute("DROP TABLE IF EXISTS advisor_reports")
    op.execute("DROP TABLE IF EXISTS env_snapshots")
