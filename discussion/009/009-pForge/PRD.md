# PRD · 009-pForge · "投资决策闭环 · M1 PIT 价格历史层 + M2 alpha 头"

**Version**: v0.1
**Created**: 2026-07-01T09:04:55Z
**Source**: forge stage-forge-009-v1.md(定位 + PRD draft 骨架)+ stage-forge-009-v2.md(七环节目标态蓝图)+ discussion/009/M1-price-data-source-research.md(数据源选型 + 表 DDL)
**Approved by**: human operator(2026-07-01,forge v1+v2 Decision menu [C] 局部接受 → 推 M1+M2 进 L4)
**PRD-form**: phased
**Phases**: [M1, M2]
**Phase-current**: M1

> **本 PRD 的血缘与定位**:009 是集合体 idea(008 采集 + 回测验证 + 004 纪律 + 四条新想法),
> 经 forge v1(该不该建 / 怎么建)+ v2(目标态蓝图 / 分期路线)双轮收敛。本 fork = **进 L4 落地
> Strangler Fig 分期的前两期**:M1 PIT 价格历史层(唯一关键新器官)+ M2 alpha 头(闭环第一个
> 可验证价值锚)。权威全文见 `discussion/009/forge/v1/stage-forge-009-v1.md` +
> `discussion/009/forge/v2/stage-forge-009-v2.md` + `discussion/009/ACCEPTED.md`。

---

## 0. 定位(关键 · 防 V4)

**009-pForge 本 fork 的交付物 = 闭环回测地基的前两期(M1 数据层 + M2 alpha 头),不是一个新建的
独立统一壳。** 它以**松耦合**方式围绕已 ship 的 004(承诺壳)/ 008(采集)生长(Strangler Fig),
004/008 全程一直可用。

**⚠ 严守 Strangler Fig,不得被 build runtime 悄悄扩成大壳(K binding②)**:
- 本 PRD 只授权 M1 + M2 两期,**M3 calibration 头 / 统一壳 / 图谱 / 蒸馏全部 defer 到本 fork 之外**。
- 每期独立可用:M1 单独完成 = 有了唯一行情地基(还不出分析结论);M2 完成 = 可单独回答
  "某分析师到底行不行",不依赖 M3。
- 目标态全貌见 v2 蓝图七环节图;本 fork 只落地其中第 0 层(数据)+ 第 1 层的 alpha 头。

## 1. Problem / Context

**operator 的第一性原理(不变)**:懂算法/自动化/数据,**不懂投资**。产品本质 = 用工程强项补投资
domain 短板。具体到本 fork:**"我说某分析师去年准,但没有 ground truth 证明。"** —— 缺的不是
更多信息,是能把"分析师准不准"变成可计算数字的**干净历史股价 + 统计纪律**。

**为什么先做这两期**(forge v2 Strangler Fig):
- **M1 PIT 价格历史层是唯一关键新器官**:004 的 `advisor_reports` 无 realized-return / 价格结果列,
  004 现在只有 `env_snapshots.price` 单点(决策时点),没有连续价格序列。alpha 头要"分析师方向 vs
  之后真实股价"必须靠这层。
- **M2 alpha 头是闭环第一个可验证价值锚**:operator 最想要的 high-value 问题("分析师到底行不行"),
  M2 就能独立回答。

**L2 verdict 继承**:整个闭环的价值前提是"回测能判出 alpha";若分析师历史样本量根本不足以让 DSR
显著,这个前提会塌(见 §11 现实缺口)。所以 M2 的 success 不是"分析师一定有 alpha",而是"能产出
一份 as-of 可复现、统计上诚实(记 trial-count + deflate)的 alpha 报告,让数字自己说话"。

## 2. Users

单人自用 operator。懂算法/自动化/数据,不懂投资、无专业投资经验。需要用工程强项(回测统计纪律)
补投资 domain 短板。**自用单人,不商业化**(K binding④)。

## 3. Core user stories

- 作为不懂投资的 operator,我要**验证某个分析师到底有没有 alpha**(Hit Ratio + 平均超额 + 显著性),
  好判断能不能把他作为关键参考信号,而不是凭"年初买存储股赚过"的主观印象。
- 作为闭环搭建者,我要一个**唯一、干净、as-of 正确的历史股价来源**(日线 + 复权 + 退市感知),
  让"分析师准不准"可被计算,且回测全程可复现、不泄漏未来。
- 作为容易踩数据坑的 operator,我要系统**在拆分/退市这类边界情况上显式正确**(拆分不被当暴跌、
  退市股不被静默当"无数据"),否则 alpha 数字全错我还不知道。

## 4. Scope IN(本 fork 只授权这些)

### M1 · PIT 价格历史层(唯一关键新器官)
- 唯一行情来源。范围 = **日线 bars + 拆分/分红复权 + PIT ticker/date 映射 + 退市股感知(survivorship-free)**。
- **defer**(本 fork 明确不做):多市场统一/汇率/分钟级/tick。
- **接口契约**:`(ticker, as-of date) → 复权收盘价`;所有字段带当时可见时间戳(as-of),
  CHECK/NOT NULL 级硬约束防 look-ahead(继承 004 把红线写进 DDL 的范式)。
- **数据源选型**(来自 M1 调研,证据票数见 §附录 A):
  - A 股 → **BaoStock**(证据最硬:qfq+hfq 复权因子 + 精确公式 + 原生 as-of 口径,几乎照抄)。
  - 美股 → **Tiingo 免费档**(免费源里复权最准,近 CRSP);备选 yfinance(起步快,但退市股不可靠,
    只能当现存股票快速原型)。
  - 港股 → **最大缺口**,免费源普遍差。M2 若港股标的少 → 先手工/半自动补或暂缓;若港股是重点 →
    评估 EODHD 个人档(月费个位数美元,唯一低价覆盖三市场 + 显式保留退市股)。

### M2 · alpha 头(闭环第一个可验证价值锚)
- 产分析师 **Hit Ratio + 平均超额 + Z 显著性**(TipRanks 三件套)。
- **防过拟合统计纪律**(v1 定):walk-forward/OOS 分割 + 交易成本 + **trial-count 记账** +
  **Deflated Sharpe Ratio + Probability of Backtest Overfitting**(Bailey & López de Prado)。
- alpha 得分实现为**一个新 StrategyModule lane**(平权进 004 的 conflict_reports,source_id 隔离,
  不跨源合并)。

## 5. Scope OUT(显式 non-goals · 每条引证据)

> **这些是本 fork 的硬边界。build runtime 若把任何一条做进来 = 越界 = BLOCK。**

- **M3 calibration 头**(承诺壳自校准 / 反事实)—— **defer 到本 fork 之外**。先看 M2 alpha 头能不能
  出可信数字(样本量够不够 DSR 显著),再决定 calibration 值不值得建(ACCEPTED.md ⏸ 挂起项)。
- **009 独立统一壳** —— 先建大壳 = operator 最怕的 V4(forge v1/v2 双方 §2)。
- **004 权威综合分 / 跨源合并评分** —— 红线 #9;004 的 conflict_reports schema 已 enforce
  无 winner/recommended/aggregate 字段(P1-Opus §1C)。
- **自动下单 / 自动执行 / 自动调仓** —— 红线 #1(Barber-Odean 加固);alpha 再强也不推自动执行。
- **两条反馈回流线**(alpha→信号权重 / calibration→纪律阈值)—— 属 M3 期,本 fork 不做。
- **时序异质图谱 lane** —— defer v2+;NLP 关系抽取放大 008 抽取脆弱性(边错→图错→信号错)。
- **蒸馏 lane** —— 末位,只能落成独立信号 lane(不替人决策 / 不综合打分),本 fork 不做。
- **多市场统一 / 汇率 / 分钟级 / tick** —— M1 defer。
- **point-in-time 基本面数据**(非价格)—— 免费源都没有,本 fork 只做价格层;但 as_of 字段设计
  为将来留位。

## 6. Phased roadmap(committed · Strangler Fig)

> **核心纪律**:新回测器官围绕已 ship 的 004/008 生长,每期独立可用,M2 不依赖 M3。
> 本 fork 授权 M1+M2;M3/M4 列出仅为路线完整,**不在本 fork 交付范围**。

### Phase M1 · PIT 价格历史层(预估 L · 新器官 latch 点)
- **交付**:PIT 价格 schema + 单市场(先选一个)接入 + 复权处理 + 退市显式建模 + as-of 契约 + contract tests。
- milestone:
  - **M1.1** — 建 3 张表(`price_daily` / `ticker_status`,DDL 见 §7)+ as-of NOT NULL 硬约束,写 alembic migration。
  - **M1.2** — 接入第一个价格源(建议 A 股 BaoStock 或美股 Tiingo,看分析师主覆盖哪个市场)+ 拆分/分红复权(存原始价+因子,查询时动态算)。
  - **M1.3** — contract tests(as-of 防未来 / 唯一价格源 / 复权样例 / 退市样例,见 §8)。
- 依赖:008 现状(可溯源包)+ 外部价格数据源。
- 风险:复权不做 → alpha 头把拆分当暴跌,回测全错(**必须 M1 做**);免费源退市覆盖是最大不确定,
  **每个源实测**别信文档(§11 缺口①)。
- **独立可用性**:M1 单独完成 = 有了唯一行情地基,但还不出分析结论(需 M2)。

### Phase M2 · alpha 头(预估 L · 最先出可验证数字 · 最独立可用)
- **交付**:分析师 alpha 报告(hit-rate / 平均超额 / Z 显著性 / DSR/PBO / 样本窗)+ alpha 得分 lane。
- milestone:
  - **M2.1** — Hit Ratio + 平均超额 + Z 显著性(TipRanks 三件套)。
  - **M2.2** — walk-forward/OOS + 交易成本 + trial-count 记账 + DSR/PBO deflate。
  - **M2.3** — alpha 得分实现为一个新 StrategyModule lane(平权进 conflict_reports)+ contract tests
    (alpha 不跨源合并 / source_id 唯一)。
- 依赖:M1 数据层。
- 风险:trial-count 不记账 → DSR 无法正确 deflate(过拟合自欺);分析师历史样本量可能不足以让
  DSR 显著 → alpha 判不出来(§11 缺口②,是整个闭环第一个价值锚,先验证这个)。
- **独立可用性**:M2 完 = 可单独回答"某分析师到底行不行",不依赖 M3。**这是 Strangler Fig 的关键期。**

### Phase M3(defer · 不在本 fork)· calibration 头 + 两条回流线
- 承诺壳自校准 + human-on-the-loop 反馈回流。**等 M2 证明能出可信数字后,另起 fork/HANDOFF 评估。**

### Phase M4(gated · 不在本 fork)· 图谱 lane / 蒸馏 lane
- 仅在 M2/M3 证明简单信号有价值后,另起 gate(可能先跑 forge v3 定内部)。**永不进 M1-M3。**

## 7. M1 表设计(来自 M1 调研 · 全 3-0 验证的正确做法)

> **依据**:真正的 PIT 数据库存"原始 as-reported 值 + 单独因子",不覆盖原始值(LEAN 把 split/复权
> 存成独立 factor 文件;BaoStock 直接给因子+公式)。全 3-0 confirmed。

### 7.1 复权:存"原始价 + 调整因子",不存预算好的复权价
```sql
price_daily(
  ticker TEXT, market TEXT,          -- 'US'/'HK'/'CN',与 004 watchlist.market 对齐
  trade_date TEXT,                    -- 交易日 (ISO)
  close_raw REAL NOT NULL,            -- 不复权原始收盘价(永不覆盖)
  adj_factor_fwd REAL,               -- 前复权因子(qfq,来自 BaoStock;其他源没有则算)
  adj_factor_back REAL,              -- 后复权因子(hfq)
  source TEXT NOT NULL,               -- 'baostock'/'tiingo'/'yfinance'/...
  as_of TEXT NOT NULL,                -- 该行"当时可见"的时间戳(防 look-ahead)
  ingested_at TEXT NOT NULL,
  PRIMARY KEY (ticker, market, trade_date, source)  -- 含 source,允许同票多源交叉验证
)
```
- **复权价查询时动态算**:`adjusted_close = close_raw × (取 as_of ≤ 目标日 的最近 adj_factor)`。

### 7.2 退市股:显式建模,不静默丢
```sql
ticker_status(
  ticker TEXT, market TEXT,
  status TEXT CHECK(status IN ('active','delisted','suspended')),
  delist_date TEXT,                   -- 退市日,可空
  last_trade_date TEXT,
  PRIMARY KEY (ticker, market)
)
```
- **依据**:survivorship-free 要保留退市/破产/并购公司(Russell 3000 中 1986 的 3000 只到后来
  只剩 565 只存活);LEAN 把退市当一等事件。yfinance 是反面教材(退市返回空 DataFrame 不报异常)。

### 7.3 多源并存
- PK 含 `source`,允许同一 (ticker, date) 存多个源,回测时可对关键标的做"多源复权价一致性"抽查
  (把 v1 的 correlation_audit strict 范式用到数据层)。

## 8. Contract tests(必测 · 回测层可测契约 · 对应 v1 AC / v2 硬约束)

> build runtime 违反任一条 = BLOCK gate。这些把 v1 的 AC-1..AC-5 + v2 新约束变成回测器官的可测契约。

**M1 层**:
1. **as-of 防未来**:构造"未来因子已入库但查询 as_of 早于它"的负例,断言查不到未来因子。
   实现 = 价格查询强制带 `as_of_date` 参数,SQL `WHERE trade_date <= :as_of ORDER BY trade_date DESC LIMIT 1`(对应 v2 AC-5)。
2. **唯一价格源**:不许第二处行情来源;回测只从 PIT 层取价。
3. **复权样例**:拆分不被当暴跌(动态算复权价正确)。
4. **退市样例**:某退市股在其退市日之后应"无价格但状态=delisted",不能是"静默空"(survivorship 不泄漏)。

**M2 层**:
5. **alpha 不跨源合并(AC-2)**:alpha 头对外只暴露"某 source_id 的 hit-rate/超额/DSR",不暴露
   跨 source 合并结论。
6. **source_id 唯一 + lane 不见 registry**:StrategyModule 每个 lane 的 `source_id` 唯一;
   lane constructor 不接 registry(继承 004 IDL 隔离范式)。
7. **004 端无权威综合分(AC-1)**:004 API/DB 响应中任何字段都不得出现跨源合并的单一权威评分
   (P1-Opus §1C 证明 schema 已背书)。

## 9. Success looks like

- **M1**:能对目标市场的一只股票产出 as-of 正确的复权收盘价序列;拆分样例复权正确;退市样例
  显式标记(非静默空);通过 §8 M1 四条 contract test。
- **M2**:能对目标分析师产出一份 as-of 可复现的 alpha 报告(命中率 + 超额 + DSR/PBO + 样本窗),
  数字能回答"他能不能 beat 一般分析师"(注:"beat 80-90% 同行"是判据方向,非 M2 硬门槛 —— 见 §11 缺口③);
  通过 §8 M2 三条 contract test;alpha 得分作为独立 lane 平权进 004 conflict_reports,无综合分字段。

## 10. Real constraints

- 自用单人,不商业化(K binding④)。
- 008 合规(付费自用 / 有效登录态 / 不传播)是既定前提,**不重审**(K binding③)。
- 回测输入质量 ⊂ 008 提取可靠性(008 forge v4 信号 spike 是上游依赖)。
- **成本尽量免费**:A 股 + 美股验证性回测免费够用(BaoStock/Tiingo);港股干净数据 / 严格
  survivorship-free 美股全市场 / PIT 基本面 → 免费源不行,需评估付费(EODHD 类)。

## 11. Open questions / 现实缺口(forge 也没解决 · operator 落地要盯)

> 这些是 forge v1+v2 自批判点出的现实缺口。**M1/M2 落地时任一都可能推翻代价估计或器官边界。**

1. **免费源退市覆盖是最大风险**(M1 缺口):所有免费源退市这块都弱。M1 真开工时,**每个源的退市
   覆盖要单独实测,别信文档**。yfinance/Tiingo 免费档退市覆盖都不足;A 股 BaoStock 覆盖历史 A 股;
   港/美退市要么 EODHD 要么手工补。
2. **分析师历史样本量可能不足以让 DSR 显著**(M2 缺口,最关键):M2 alpha 头可能"判不出"分析师
   行不行。这是整个闭环第一个价值锚,**先验证这个**。若样本量根本判不出 → 需重估整个闭环前提。
3. **"beat 80-90% 同行"缺 baseline 样本池**:M2 v0.1 可能只能给"这个分析师 vs 大盘/S&P500"的
   绝对超额,给不出"vs 80-90% 同行"的分位(需要一个分析师样本池做分母 —— 蓝图未把它画成器官,
   超闭环自洽射程)。
4. **港股缺口**:免费源港股复权/退市普遍差。若港股是 M2 重点 → 需评估 EODHD;否则先暂缓港股,
   别为它卡住 M1。
5. **双模型回声室**:v1+v2 蓝图是两个 AI 高度收敛的产物,非真实回测数据。可能共享盲点(如低估
   干净历史数据获取成本 / calibration↔004 schema 耦合演化未展开 —— 但后者属 M3,不在本 fork)。

## 12. UX principles

- 上游多信号永远以独立列呈现,人最终拍板(不给"权威结论")。
- 投资 domain 判断永远附可验证依据(回测数字),不让 operator 凭感觉(K binding①)。

---

## 附录 A · 数据源选型证据票数(来自 M1 调研 3 票对抗验证)

| 源 | 结论 | 验证票数 | 可信度 |
|---|---|---|---|
| BaoStock A 股复权因子 + as-of 口径正确,可照抄 M1 | 3-0 | 高(官方文档 primary) |
| Tushare 免费档只给不复权,港美付费墙 → 基本不可用 | 3-0 | 高(官方文档) |
| yfinance 退市股返回空 DataFrame 不可靠 | 2-1 + 3-0 | 中高(GitHub issue primary) |
| Tiingo 免费档复权最准(近 CRSP) | 2-1 | 中(第三方 blog 实测) |
| EODHD 显式保留退市股(2018 为界),覆盖三市场,但复权自己有误差 | 3-0 / 2-1 | 中高 / 中 |
| PIT 要存原始值+因子、as-of 取最近因子、退市显式建模 | 3-0 ×4 | 高(LEAN 官方 + 多源一致) |
| AKShare A 股复权可以但爬取有限流/封 IP 风险 | 3-0 | 中高(官方文档承认) |

**被驳回、不采信的说法**(防误导):yfinance"每年挂 2-4 次"具体数字(0-3)、yfinance"复权差 1-2%"
具体幅度(0-3)、"所有免费源都有 survivorship bias"绝对断言(0-3)。完整调研见
`discussion/009/M1-price-data-source-research.md`。
