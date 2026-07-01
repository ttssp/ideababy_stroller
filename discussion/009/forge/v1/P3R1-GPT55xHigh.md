# Forge v1 · 009 · P3R1 · GPT55xHigh · 联合收敛 R1(标分歧)

**Timestamp**: 2026-07-01T08:58:13+08:00
**Visibility**: 我已读对方 P1 + P2。
**Searches in this round**: NONE(避免 R1 又开搜索发散)。

## 1. 整合摘要

双方 P1/P2 已高度收敛:009 不是从零造系统,而是把 008 证据采集、004 StrategyModule 多 lane、回测验证层、004 承诺壳重新接成闭环。004 红线 #1/#9 仍管下游执行;008 与 008 forge v4 把上游输入收窄为可溯源证据、置信度、可靠性 spike。XenoDev strategy 代码也支持:lane 不接 registry,provider 只读,各 lane 平权输出 StrategySignal。

SOTA 对标把两件事压实。第一,回测必须 new-first,按 point-in-time 数据、walk-forward/OOS、交易成本、trial-count、DSR/PBO 建统计纪律;Pearson correlation audit 只是雏形。第二,时序异质图谱必须 defer,因为关系抽取会放大 008 v4 已标出的抽取脆弱性。红线 #9 边界也基本闭合:上游可做独立 lane 或内部评分,004 端永不呈现权威综合分。

剩下的实质分歧只在集成形态:009 是否应成为独立统一壳。Opus P2 把价值压在集成质量和一套数据两用上;我接受这个判据,但不接受它自动推出统一壳。共享 point-in-time 数据层 + calibration/alpha 两个评估头,当前更像可契约化的共享回测地基。

## 2. 我的初步 verdict(草案)

我的初步 verdict:009 当前不应先做独立统一壳,应降级为“契约化集成规范 + 共享回测地基”,落入 004 v1.0 回测 lane 与 008 消费契约的松耦合演进。接受 Opus 的“一套数据两用”判据,但按现有证据,它只证明需要共享 point-in-time 数据层和两个评估头,不足以证明需要一个 004/008 之外的新壳。R2 应把“何时升级为统一壳”写成未来 gate,而不是当前 verdict。

## 3. 关键分歧清单

- **分歧 1**:009 的交付身份是独立统一壳,还是契约化松耦合演进
  - 我的立场:当前采用松耦合。009 应产出 008→回测→StrategyModule→004 的接口契约、回测统计纪律、红线验收条款和 dev sequencing;不要让 build runtime 先建大一统应用壳。“一套数据两用”应实现为共享 point-in-time data layer + calibration head + alpha head,可被 004 v1.0 回测 lane 消费。
  - 对方立场(引用对方 P2 原句,≤15 words):“合,但 verdict 必须把'集成边界'作为头号交付物”。
  - 我希望 R2 怎么收敛:把判据写成 decision-list 硬门槛:若 calibration 头与 alpha 头只需共享数据层和回测 runner,则松耦合胜,009=契约规范;只有当二者需要 004/008 都不拥有的独立回测内核、状态模型和验收口径时,才升级为统一壳。同时固化验收:004 UI 不显示权威综合分;上游评分只能作为独立 lane 或回测内部指标;蒸馏技能只能成为独立信号源。

## 4. 与 K 的对齐性自检

- K 第 1 条“闭环架构怎么搭、004/008 怎么干净并入” → ✅ 以边界契约为主产物:008=证据层,回测=验证层,StrategyModule=信号 lane,004=纪律壳。
- K 第 2 条“集合体是否真有架构级价值,还是 V4 式过度设计” → ⚠ 价值成立在“集成契约 + 共享回测地基”,不成立在先做统一壳。R2 必须写清升级条件。
- K 第 3 条“回测系统怎么作为两灵魂公共地基先落地” → ✅ 接受“一套数据两用”作为判据,但落成 point-in-time 数据层 + calibration/alpha 两个评估头,并要求 DSR/PBO、trial-count、OOS。
- K 第 4 条“四条想法怎么排期” → ✅ 回测/分析师 alpha 验证先;008 信号可靠性依赖先;图谱 defer;蒸馏技能最后且只能独立 lane 化。
- K binding“别让 build runtime 静默替我定产品方向” → ✅ 当前 verdict 要求 R2 写成硬验收条款:009 当前是契约和 gate,不是实现侧自行创造统一壳或权威综合分。
