# 009 投资决策闭环 · 已接受结论(局部接受 · Decision menu [C])

> **operator 于 2026-07-01 对 forge v1+v2 verdict 选择 [C] 局部接受。** 本文档固化"已采纳"
> 的结论 + M1 起点,供后续 L4 / XenoDev build session 直接对照。**不是 PRD**(PRD 待
> fork 时按 v1 draft + v2 蓝图叠加生成)。权威全文见 `forge/v1/stage-forge-009-v1.md`
> + `forge/v2/stage-forge-009-v2.md`。

## 一句话

009 = 给现有 004/008 接上"回测验证 + 复盘反馈"管道,连成一个能自转的七环节闭环。
**不建独立大壳**,用 Strangler Fig 分期,每期独立可用。**起点 = M1 PIT 价格历史层。**

## ✅ 已采纳(证据最硬 · 0 争议 · 立即生效)

### A. 目标态形态(v2 蓝图)
- **七环节闭环**:008 采集/结构化 → 回测 PIT 数据层 + [alpha 头 / calibration 头] →
  StrategyModule 独立 lane → 004 决策/纪律 → calibration 反馈回流。
- **非独立统一壳**:靠契约让各器官独立迭代 + 端到端连贯(v1 松耦合 verdict,不推翻)。
- **唯一关键新器官 = PIT 价格历史层**(004 的 `advisor_reports` 无价格结果列)。
- ASCII 目标态模块图见 `forge/v2/stage-forge-009-v2.md` §"Refactor plan"。

### B. 回测 new-first 按学术级统计纪律(v1)
- 分析师 alpha 度量 = TipRanks 三件套(Hit Ratio + 平均超额 + Z 显著性)。
- 防过拟合 = Deflated Sharpe Ratio + Probability of Backtest Overfitting(记 trial 数 + deflate)。
- 必须:point-in-time / walk-forward+OOS / 交易成本 / trial-count。

### C. 三条硬约束(可执行 · L4 build 验收 gate)
1. **回流 human-on-the-loop**:
   - 可"建议→human 确认→之后可自动套用"的**旋钮**:某 source_id 的 confidence
     multiplier/cap、alpha lane 启用/降权、devil's-advocate 触发阈值、复盘提醒频率、
     calibration 报告窗口。
   - **永远手动 / 禁止自动化**:买/卖/持有/等待动作、单笔最终决定、自动下单/调仓、
     跨源综合分、新增外部顾问/扩大采集或交易 universe、把图谱/蒸馏升为决策者。
2. **两档详略**:现建器官(PIT 数据层/alpha 头/calibration 头/四段接口契约)画定量
   契约+AC;未来插槽(图谱 lane/蒸馏 lane)只画 StrategyModule 签名+gate。
3. **回测层 contract tests**(必测):as-of 防未来数据 / 唯一价格源 / 复权+退市样例 /
   alpha 不跨源合并 / calibration 不静默改阈值 / StrategyModule source_id 唯一且 lane
   不见 registry / 004 无 winner·recommended·aggregate 字段。
   (这些把 v1 的 AC-1..AC-5 + v2 新约束全变成回测器官的可测契约。)

### D. 红线边界(v1 · 继承 004)
- 004 端**永不呈现权威综合分**(schema 已 enforce:conflict_reports 无 winner 字段)。
- alpha 再强也**不推出自动执行**(红线 #1)。
- 图谱 defer v2+;蒸馏末位,只能独立 lane 化,不替人决策。

## ⏸ 已挂起(等条件成熟再碰 · 不是拒绝)

- **M3 calibration 头**:先看 M2 alpha 头能不能出可信数字(样本量够不够 DSR 显著),
  再决定 calibration 值不值得建。
- **统一壳 gate 判据文档**:等松耦合真跑起来遇到打补丁时再写,避免过早形式化。
- **图谱 lane / 蒸馏 lane**(定性签名):等 M2/M3 证明简单信号有价值后再触发 gate
  (可能起 forge v3 定内部)。

## ❌ 无需确认拒绝的

无。v1+v2 verdict 均无 unresolved,双方完全一致。

## ▶ 起点:M1 · PIT 价格历史层

**这是 Strangler Fig 第一期,不依赖任何后续,可独立落地。**

- **目标**:唯一行情来源。范围 = 日线 bars + 拆分/分红复权 + PIT ticker/date 映射 +
  退市股感知(survivorship-free);**defer** 多市场/汇率/分钟级/tick。
- **接口契约**:`(ticker, as-of date) → 复权收盘价`;所有字段带当时可见时间戳,
  CHECK/NOT NULL 级硬约束防 look-ahead。
- **contract tests**:as-of cutoff 防未来 / 唯一价格源 / 复权样例(拆分不被当暴跌)/
  退市样例(survivorship 不泄漏)。
- **风险**:复权若 v0.1 不做 → alpha 头把拆分当暴跌,回测全错(必须 v0.1 做)。
- **预估代价**:L(核心新建 + PIT 正确性)。M1 是纯新建,代价估计比其他模块更不确定。

## ⚠ operator 落地时要盯的现实缺口(forge 自批判)

1. **分析师历史样本量可能不足以让 DSR 显著** → M2 alpha 头可能"判不出"分析师行不行。
   撞在 M2,是整个闭环的第一个价值锚,先验证这个。
2. **干净历史股价数据(含复权/退市)的获取成本** → M1 是纯新建、无现成标的对照,
   代价估计(L)是基于 SOTA 推断,可能被真实数据源成本推翻。先选定价格数据源。
3. **"beat 80-90% 同行"缺 baseline 样本池** → v0.1 可能只能给"这分析师 vs 大盘"的
   绝对超额,给不出"vs 80-90% 同行"的分位。蓝图未把"分析师样本池采集"画成器官
   (超闭环自洽射程)。
4. **双模型回声室**:v2 蓝图是两个 AI 高度收敛的产物,非真实回测数据。可能共享盲点
   (calibration↔004 schema 耦合演化未展开 / operator 判不了旋钮建议值本身的隐性
   循环依赖)。以上任一都可能在 M1/M2 推翻代价估计或器官边界。

## 下一步选项

- **推 M1**:fork PRD branch(`discussion/009/009-pForge/PRD.md`,骨架 = v1 stage doc
  的 PRD draft + 叠加本文档的 M1 契约/回流约束/contract tests)→ `/plan-start` →
  新开 XenoDev session 真开发。⚠ 建议只把 M1 放进第一个 HANDOFF,严守 Strangler Fig。
- **先选价格数据源**:M1 依赖外部价格数据(日线+复权+退市)。落地前先定用哪个源
  (成本/覆盖/复权质量),这是缺口 #2。
- **park**:若价格数据源未定 / 008 forge v4 信号 spike 未落地(009 回测上游依赖它)。
