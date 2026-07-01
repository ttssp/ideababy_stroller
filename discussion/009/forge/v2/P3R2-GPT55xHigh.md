# Forge v2 · 009 · P3R2 · GPT55xHigh · 联合收敛 R2(finalize)

**Timestamp**: 2026-07-01T15:12:05+08:00
**Visibility**: 我已读对方 P3R2。
**Convergence mode**: strong-converge。

## 1. 我对每条分歧的最终立场 + 让步

双方 P3R1 均判 0 实质分歧。Opus P3R2 已完整采纳我 P3R1 的两条待固化清单,我也采纳 Opus 的最终表述,让步:无。

- **待固化 1 · 回流 human-on-the-loop**:定稿为“旋钮可建议→human 确认→之后自动套用;动作/结构/决策权永远手动”。可确认后套用:单个 `source_id` confidence multiplier/cap、alpha lane 启用/降权、devil's advocate 阈值、复盘提醒频率、calibration 报告窗口。永远手动/禁止:买卖持有等待动作、单笔最终决定、自动下单/调仓、跨源综合分、新增顾问/扩大 universe、图谱/蒸馏升为决策者。
- **待固化 2 · 两档详略 + contract tests**:定量档=PIT 价格数据层、alpha 头、calibration 头、008→回测→StrategyModule→004 契约;定性档=图谱/蒸馏 lane,只画签名+gate。contract tests 覆盖 as-of 防未来、唯一价格源、复权/退市、alpha 不跨源合并、calibration 不静默改阈值、StrategyModule source_id 唯一且 lane 不见 registry、004 无 winner/recommended/aggregate 字段。

## 2. 联合 verdict(单一)

009 目标态蓝图 = 一张七环节契约化闭环图,不是独立统一壳。主链为 008 采集/结构化 → 回测 PIT 数据层 + alpha/calibration 两头 → StrategyModule 独立 lane → 004 决策/纪律 → calibration 反馈回流。已有器官 keep;关键新器官是 PIT 价格历史层(日线+复权+PIT ticker+退市感知,defer 多市场/汇率/tick)。分期采用 Strangler Fig:M1 数据层→M2 alpha 头→M3 calibration+两条回流线→M4 gated 图谱/蒸馏,每期独立可用。三条硬约束:human-on-the-loop、两档详略、回测层 contract tests。无 unresolved。

## 3. 残余分歧降级为 v0.2 note

- v0.2 note 1:calibration 的“不动基线/反事实窗口”粒度留 M1/M3 细化,包括 N 天窗口、日频还是事件驱动。
- v0.2 note 2:“确认后自动套用”是否需前 K 次逐次确认再解锁自动,留 M3 防静默漂移。
- v0.2 note 3:图谱/蒸馏 gate 触发后是否先跑 forge v3,留 gate 触发时决定。

## 4. W 形态产出的初步草稿建议

- **refactor-plan**:画目标态模块图。第 0 层=008 证据/结构化 + 新 PIT 价格历史层;第 1 层=回测层(alpha 头、calibration 头);第 2 层=StrategyModule 多 lane(advisor/XGBoost/alpha 得分/gated 图谱/gated 蒸馏);第 3 层=004 conflict_reports→decisions→rebuttals。箭头标契约名、传输字段、keep/new/gated;反馈线标“建议→human 确认”。
- **free-essay**:写 final goal 全貌。论点:七环节各补一个投资短板;闭环之所以是环,在于 alpha 得分回调信号强度、calibration 回调纪律强度;不建大壳是因为回测器官围绕已 ship 的 004/008 生长;human-on-the-loop 是工程补 domain 短板而非让系统静默定方向。
- **next-dev-plan**:按 Strangler 切 M1-M4。M1=PIT 数据层(日线+复权+退市+as-of);M2=alpha 头,先出“分析师行不行”的独立数字;M3=calibration 头+两条回流线;M4(gated)=图谱/蒸馏 lane。每期交付可单独使用,M2 不依赖 M3。
