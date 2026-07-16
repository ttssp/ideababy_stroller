# XenoDev 跨仓资产快照(forge v5 X 附件 · 2026-07-16 实测)

> **为什么有这个文件**:X 中两个标的在 XenoDev 仓(Codex 沙箱可能 BLOCK 跨仓读),
> 且 alpha 模块在 `feat/009-spec` 分支上(main 工作树看不到)、collection.db 是二进制。
> 本文件把两者的**关键契约/统计**摘录成 IDS 仓内可读文本,供双方 Phase 1 使用。
> 摘录均为 2026-07-16 由主进程真读实测,非转述。

---

## A. 004-pB alpha 模块(M2 评估机器 · branch `feat/009-spec`)

**文件清单**(`git ls-tree feat/009-spec`,均已 merge):
`alembic/versions/0015_add_analyst_alpha_tables.py` · `src/decision_ledger/alpha/{__init__,__main__,deflate,evaluate,join,metrics,realized_return}.py` · `src/decision_ledger/strategy/alpha_lane.py` + 6 个对应测试文件。

### A.1 join.py(T011 · 唯一 join 路径 · 歧义默认拒绝)

- 把"分析师信号 → (ticker, market, direction, signal_published_at)"解析成唯一无歧义
  ResolvedSignal;**任何歧义一律落 `analyst_alpha_rejections` 不猜**(D-M2-2 · M2-R4)。
- **七类拒绝 enum**:`multi_ticker` / `no_signal_date` / `duplicate_signal` /
  `multi_direction` / `sector_only` / `source_conflict` / `unknown_market`。
- **数据源(真读 004 · 不 mock)**:`advisor_reports.structured_json`({ticker:{direction,confidence}},
  **每报告恰好 1 个 ticker key,多则拒**)· `strategy_signals`(消歧 + **权威时间基准**,经
  `inputs_used_json.advisor_week_id` 绑定报告周;**无 strategy_signal 行则整条落
  `no_signal_date` 拒——不能只靠 structured_json 通过**)· `watchlist`(ticker→market
  权威查表,**严禁从 ticker 字符串启发式猜 market**)。
- 方向仅 `long`/`short` 产样本(neutral/wait/no_view 静默跳过非拒绝)。
- 已知边界:v0.1 **单 advisor 假设**(strategy_signals 无 advisor 定位键,多 advisor 会双重
  归因;07-07 决议 defer 键)。

### A.2 realized_return.py(T012 · SLA C16 固化)

- entry/exit 交易日规则防前视:盘后/无时刻发布 → entry=下一交易日;exit=entry+horizon 交易日。
- **双 as_of 轴**(forge v3 verdict):factor 轴统一用 exit_date 当日末;close 轴 entry/exit 各锚
  当日末——防拆股/修订污染(2:1 拆股实际 +10% 会被算成 -60% 的教训)。
- **benchmark per market**:US=`^GSPC` · CN=`000300.SH` · **HK 故意缺 → benchmark_unsupported
  typed skip(defer)**。标的+benchmark 都用对数收益;成本项 `2×ln(1−0.001)`。
- 取价**要求精确命中目标交易日**,非精确命中 = typed skip(gap/stale),绝不回看更早价
  (silent-wrong 防线)。

### A.3 evaluate CLI(T016 · P2 PPV 真路径入口)

- `python -m decision_ledger.alpha.evaluate --advisor <id> [--db <sqlite路径>]`
- **显式 `--db` 时不走 `load_settings()`**(不需要 ANTHROPIC_API_KEY 等无关凭据)。
- horizon 集合固化 `{5, 20, 60}` 交易日,每 (signal × horizon) 落 `analyst_alpha_eval` 一行;
  hit/excess 逐行,DSR/PBO/trial_count 填该 horizon 聚合值。
- 退出码:0 成功(accepted_rows 可为 0 但 WARN)/ 2 入参错 / 1 内部错。
- ingest 侧同构:`python -m decision_ledger.price.ingest --source {tiingo|baostock|hk} --ticker
  --market --start --end [--db] [--token-env]`(`--token-env` 传环境变量**名**,凭据隔离)。

### A.4 004 三表 DDL 要点(alembic 0001/0010/0011)

- `advisor_reports`:PK **(advisor_id, source_id, week_id)**(0011 复合化)+ UNIQUE
  (week_id, source_id);列含 raw_text / structured_json / ingested_at + T020 四个 nullable
  多模态列(content_format/transcript/key_points/transcription_provider)。
- `strategy_signals`:signal_id PK;direction CHECK ∈ {long,short,neutral,wait,no_view};
  confidence ∈ [0,1];rationale_plain 非空;inputs_used_json free-form TEXT(无 CHECK)。
- `watchlist`:ticker PK;market CHECK ∈ {US,HK,CN}。
- `conflict_reports`:**无 winner/recommended/priority 字段**(R10 红线,M2 契约测试 T017 守)。

### A.5 M2 交付终态(M-fork-complete · 2026-07-06)

M1=T001-T008,M2=T010-T017+T016b;004 全套 **743 passed** 无回归;PPV 双终点真路径无 mock。
M3(calibration 头/统一壳/图谱/蒸馏 lane/回流线)显式 OUT OF SCOPE(spec line 23 ·
OUT-1/2/5/6/7 · 越界=BLOCK)。

---

## B. 008 语料库(collection.db · 提取头的直接原料)

**路径**:`/home/ys/codes/XenoDev/out/collection.db`(raw 文件同目录 raw-articles/ raw-qa/ raw-replays/)

### B.1 schema(实测 `.schema`)

```sql
CREATE TABLE records (
    source_id            TEXT PRIMARY KEY,
    published_at         TEXT NOT NULL,   -- 精确到秒,+08:00 —— 文本侧 PIT 纪律的时间戳基础
    pub_date             TEXT NOT NULL,
    captured_at          TEXT NOT NULL,
    form                 TEXT NOT NULL,   -- article | qa | replay
    raw_ref              TEXT NOT NULL,   -- 指向 out/raw-*/ 下的文本文件
    capture_status       TEXT NOT NULL,
    source_url_canonical TEXT NOT NULL,
    title TEXT, tags TEXT, author TEXT
);
-- 另有 record_tickers 表(777 行)—— 采集侧已存在某种 ticker 关联,提取头设计前应查明其语义
```

### B.2 规模与覆盖(实测 2026-07-16)

| form | 条数 | pub_date 覆盖 | raw 文件 |
|---|---|---|---|
| article(盘前/中/后笔记) | 1,179 | 2025-06-16 → 2026-07-07 | raw-articles/ 3,536 个 |
| qa(问答) | 7,545 | 2025-06-17 → 2026-07-07 | raw-qa/ 15,751 个 |
| replay(直播回放 · **已转写为文本**) | 357 | 2025-06-19 → 2026-07-01 | raw-replays/ 710 个 |

- capture_status:9,079/9,081 captured(2 条 uncertain)。
- **operator 记忆中"有用"的时段(25 年底–26 年初 · 存储主线/美光/海力士)落在覆盖范围内**
  ——天然先导实验候选窗口。
- replay 转写质量注意:抽查开头有直播杂音/中英混杂段(如调试摄像头的闲聊),提取头需
  对转写噪声鲁棒。
