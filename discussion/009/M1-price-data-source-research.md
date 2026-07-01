# M1 · 历史股价数据源选型 + 接入方案(deep research 结果)

> **背景**:009 闭环第一期 M1「PIT 价格历史层」的数据源调研。用途 = 历史回测验证分析师 alpha
> (非实时);硬需求 = 复权 + 退市股(survivorship-free)+ point-in-time;三市场(美/港/A);
> 成本尽量免费。技术栈 Python + SQLite + alembic。
>
> **方法**:deep-research 工作流(5 角度 fan-out → 22 源 → 94 条 claim → 25 条 3 票对抗验证)。
> ⚠ **工作流的最终 synthesis 阶段出了 bug 返回了 test 占位符,但验证阶段完整跑通**——本报告由
> Opus 从 **19 条已验证 confirmed claim + 6 条被驳回 claim** 重建,每条结论标了验证票数。
> 被驳回的说法**不写进结论**(见末尾"验证中被否掉的说法")。

## 0. 一句话结论

**没有单一免费源能干净覆盖美/港/A 三市场 + 复权 + 退市。** 现实最优 = **分市场组合免费源先跑通 M2**,
其中 **A 股用 BaoStock(证据最硬,复权因子 + as-of 口径都对)**,**美股用 Tiingo 免费档(复权准确度
最高,近 CRSP)**,港股是最大缺口(免费源普遍差)。**Tushare 免费档基本不可用**(只给不复权)。
**yfinance 可做美股快速起步但退市股处理不可靠**,不能作回测唯一源。**若嫌组合麻烦 → EODHD 个人档
(月费个位数)是唯一"一个源覆盖三市场 + 显式保留退市股"的低价选项**,但它自己的复权也有已知误差。

## 1. 数据源对比表(每条标验证票数)

| 源 | 美股 | 港股 | A股 | 复权质量 | 退市覆盖 | PIT/as-of | 成本 | 已知坑(验证票数) |
|---|---|---|---|---|---|---|---|---|
| **BaoStock** | ✕ | ✕ | ✅ | ✅ **好**:qfq+hfq 复权因子 + 精确公式,可只存因子动态算 (3-0) | A股 | ✅ **原生 as-of**:取 ≤ 目标日最近因子 (3-0) | **免费** | 涨跌幅复权口径,无法还原参加分配的实际收益 (3-0);仅 A 股 |
| **AKShare** | △ | △ | ✅ | ✅ A股 qfq/hfq via `adjust` 参数 (3-0) | A股退市接口有(沪深+科创)(1-2,港美无专用接口) | 需自建 | **免费** | 底层爬 EastMoney/Sina/Tencent,**重复调用被封 IP**、限流风险 (3-0) |
| **Tushare 免费档** | ✕(付费~2000 CNY/yr) | ✕(付费~1000 CNY/yr) | △ | ❌ **免费档只给不复权**,复权要积分/付费 (3-0) | — | — | 免费档≈不可用 | 120 积分只够不复权日线、不能调其他接口 (3-0);港美单独付费墙 (3-0) |
| **yfinance** | ✅ | △ | △ | 一般(社区有复权抱怨,但"差 1-2%"的具体说法**被驳回**) | ❌ **退市股返回空 DataFrame 不报异常**,和"该期无数据"无法区分 (2-1 + 3-0) | 需自建 | **免费** | try/except 抓不到退市;退市信号只打 console log (2-1);"每年挂 2-4 次"具体数字**被驳回** |
| **Tiingo 免费档** | ✅ | ✕ | ✕ | ✅ **最准**:复权价近乎完全匹配 CRSP 基准 (2-1) | 一般 | 需自建 | **免费档**(有限) | 只美股,不支持国际市场 |
| **EODHD 个人档** | ✅ | ✅ | ✅(有限) | ⚠ 声称 CRSP 但**实测有偏差**(410.347 vs 410.317)(2-1) | ✅ **显式保留退市股**(2018 为界:后有基本面+分红+拆分+EOD,前只 EOD)(3-0) | 需自建 | **~月费个位数美元** | 复权自己也不完全准,要交叉验证 |
| IEX Cloud | ✅ | ✕ | ✕ | ❌ **复权方法非标/错**(股息以不可能价格再投资 + 漏 Realty Income 分拆)(2-1) | — | — | 付费 | 复权总回报序列不可靠,不推荐 |

## 2. 明确推荐(针对"单人 + 免费优先 + 先跑通 M2")

### 方案 A(免费组合 · 推荐先走这个)
- **A 股 → BaoStock**:证据最硬。它同时给**前复权因子 + 后复权因子 + 精确公式**,还原生用"取 ≤ 目标日最近因子"
  的 as-of 口径——**正好是 M1 PIT 层要的模式**,几乎是照抄。免费。
- **美股 → Tiingo 免费档**:免费源里复权最准(近乎完全匹配 CRSP 参考值),够验证 alpha。
  - 备选 **yfinance**:起步快、无需注册,但**退市股不可靠**(空 DataFrame 混淆),只能当"现存股票"的快速原型,
    回测正式跑要么补退市名单要么换 Tiingo。
- **港股 → 最大缺口**。免费源普遍差(Tushare 付费墙、AKShare 爬取不稳)。M2 若港股标的少,**先手工/半自动补**
  或**暂缓港股**;若港股是重点 → 直接看方案 B。

### 方案 B(低价统一 · 嫌组合麻烦时)
- **EODHD 个人档(月费个位数美元)**:调研里**唯一**"一个源覆盖三市场 + 显式保留退市股(survivorship remedy)"
  的低价选项。代价:它自己的复权也有已知误差(实测偏离 CRSP),关键标的要**交叉验证**。
- 适合:港股是重点、或不想维护三套免费源接口时。

### 诚实的边界(免费能走多远)
- **免费够用**:A 股(BaoStock 完全够)+ 美股验证性回测(Tiingo/yfinance)。跑通 M2"这个分析师有没有 alpha"够了。
- **免费不够、要转付费**:① 港股要干净复权+退市 → 免费源都差,基本得 EODHD 类;② 要严格 survivorship-free
  的美股全市场回测(不只是抽几个分析师覆盖的票)→ yfinance/Tiingo 免费档的退市覆盖都不足;③ 要 point-in-time
  基本面(不只是价格)→ 免费源都没有。

## 3. M1 接入方案(能直接指导 SQLite/alembic 落地)

调研验证了几条**架构级正确做法**(都 3-0 confirmed),直接定 M1 的表设计:

### 3.1 复权:存"原始价 + 调整因子",不存预先算好的复权价 ✅ (3-0)
- **依据**:真正的 PIT 数据库要存"原始 as-reported 值 + 单独字段标记是否被 restate + restate 日期",
  不能覆盖原始值(3-0);LEAN 也把 split/复权数据存成**独立 factor 文件**而非改写原始价(3-0);
  BaoStock 直接给因子 + 公式,可只存因子动态算(3-0)。
- **M1 表设计**:
  ```
  price_daily(
    ticker TEXT, market TEXT,          -- 'US'/'HK'/'CN',与 004 watchlist.market 对齐
    trade_date TEXT,                    -- 交易日 (ISO)
    close_raw REAL NOT NULL,            -- 不复权原始收盘价(永不覆盖)
    -- 复权因子(qfq/hfq 两套,来自 BaoStock;其他源没有则算)
    adj_factor_fwd REAL,                -- 前复权因子
    adj_factor_back REAL,               -- 后复权因子
    source TEXT NOT NULL,               -- 'baostock'/'tiingo'/'yfinance'/...
    as_of TEXT NOT NULL,                -- 该行"当时可见"的时间戳(防 look-ahead)
    ingested_at TEXT NOT NULL,
    PRIMARY KEY (ticker, market, trade_date, source)
  )
  ```
- **复权价查询时动态算**:`adjusted_close = close_raw × (取 as_of ≤ 目标日 的最近 adj_factor)`。

### 3.2 as-of 防 look-ahead:取"≤ 目标日期的最近因子" ✅ (3-0)
- **依据**:BaoStock 官方口径——某交易日的复权价 = 取日期 ≤ 该日的最近复权因子 × 当日不复权价
  (浦发银行实例验证)(3-0)。这**正是 PIT 防 look-ahead 的标准模式**。
- **M1 实现**:所有价格查询函数强制带 `as_of_date` 参数,SQL 用 `WHERE trade_date <= :as_of ORDER BY trade_date DESC LIMIT 1`
  取因子。**contract test**:构造"未来因子已入库但查询 as_of 早于它"的负例,断言查不到未来因子(对应 v2 蓝图 AC-5)。
- **额外**:基本面/分析师数据的 look-ahead 更隐蔽——公司先发新闻稿(季末后 4-5 周)、再交正式报告(可能 restate,
  甚至几年后再改)(3-0)。M1 价格层先不碰基本面,但 as_of 字段的设计要为将来留位。

### 3.3 退市股:显式建模,不能静默丢 ✅ (3-0)
- **依据**:survivorship-free 要保留退市/破产/并购公司——Russell 3000 中 1986 年的 3000 只到后来只剩 565 只存活,
  必须留下那 2435 只(3-0);LEAN 把退市当**一等事件**(发 Delisting 对象并移除)而非静默丢(3-0)。
  **yfinance 恰恰是反面教材**:退市返回空 DataFrame 不报异常,和"该期无数据"无法区分(2-1)。
- **M1 表设计**:加一张 `ticker_status`:
  ```
  ticker_status(
    ticker TEXT, market TEXT,
    status TEXT CHECK(status IN ('active','delisted','suspended')),
    delist_date TEXT,                   -- 退市日,可空
    last_trade_date TEXT,
    PRIMARY KEY (ticker, market)
  )
  ```
- **contract test**:回测取某退市股在其退市日之后应"无价格但状态=delisted",不能是"静默空"。
- ⚠ **免费源的退市覆盖是最大风险**:yfinance/Tiingo 免费档退市覆盖都不足;A 股 AKShare 有退市接口(1-2 验证,
  仅 A 股),BaoStock 覆盖历史 A 股;港/美退市要么 EODHD 要么手工补。**M1 落地时这块要单独核查每个源实测**。

### 3.4 多源并存:PK 带 source,同一票可存多源交叉验证
- 因为免费源复权质量参差(Tiingo 准、EODHD/IEX 有误差,都 2-1 验证),M1 的 PK 含 `source`,
  **允许同一 (ticker, date) 存多个源**,回测时可对关键标的做"多源复权价一致性"抽查(把 v1 的
  correlation_audit strict 范式用到数据层)。

## 4. 建议的 M1 落地顺序

1. **先选定第一个源接一个市场**:建议 **A 股 BaoStock**(证据最硬、复权+as-of 现成)或 **美股 Tiingo**
   (看你分析师主要覆盖哪个市场)。
2. 建上面 3 张表(`price_daily` / `ticker_status`),写 alembic migration。
3. 写"取 ≤ as_of 最近因子"的复权查询 + 3 条 contract test(as-of 防未来 / 退市显式 / 复权动态算)。
4. **港股暂缓或走 EODHD**:除非港股是 M2 重点,否则先不为它卡住 M1。
5. M2 alpha 头接上后,若发现分析师覆盖的退市股多 → 再评估是否上 EODHD 补 survivorship。

## 5. 关键结论的可信度标注

| 结论 | 验证 | 可信度 |
|---|---|---|
| BaoStock A 股复权因子 + as-of 口径正确,可照抄 M1 | 3-0 | **高**(官方文档 primary) |
| Tushare 免费档只给不复权,港美付费墙 | 3-0 | **高**(官方文档) |
| yfinance 退市股返回空 DataFrame 不可靠 | 2-1 + 3-0 | **中高**(GitHub issue primary) |
| Tiingo 免费档复权最准(近 CRSP) | 2-1 | **中**(第三方 blog 实测) |
| EODHD 显式保留退市股(2018 为界) | 3-0 | **中高**(EODHD 官方 primary) |
| EODHD/IEX 复权有已知误差 | 2-1 | **中**(第三方实测) |
| PIT 要存原始值+因子、as-of 取最近因子、退市显式建模 | 3-0 ×4 | **高**(LEAN 官方 + 多源一致) |
| AKShare 爬取有限流/封 IP 风险 | 3-0 | **中高**(官方文档承认) |

## 6. 验证中被否掉的说法(不采信 · 防你被误导)

这些 claim 被 3 票对抗验证**驳回**(0-3 或 1-2),**不写进结论**:
- ❌ "yfinance 每年挂 2-4 次、限流 ~2000 请求/小时"(0-3)——挂是真的,但**这些具体数字无据**,别引用。
- ❌ "yfinance 复权价在拆分附近差 1-2%"(0-3)——有复权抱怨是真,但**"1-2%"这个具体幅度无据**。
- ❌ "所有三个免费源(yfinance/AlphaVantage/Polygon)都有 survivorship bias"(0-3)——作为**绝对断言**站不住,分源看。
- ❌ "没有任何单一免费源覆盖三市场"(0-3)——作为**绝对断言**被驳(EODHD 虽付费但接近);表述改为"没有免费源干净覆盖三市场"。
- ❌ AKShare 退市接口只覆盖 A 股(1-2)——**弱驳**,港美可能有非专用途径,别当死结论。

---
*源:22 个(BaoStock/Tushare/AKShare/EODHD 官方 primary + yfinance GitHub issues + QuantConnect LEAN docs + 若干实测 blog)。完整源清单见 deep-research 工作流 output。*
