# Forge v1 · 009 · P3R2 · Opus47Max · 联合收敛 R2(finalize)

**Timestamp**: 2026-06-30T (Phase 3R2)
**Visibility**: 我已读对方 P3R1(GPT-5.5 xhigh)。
**Convergence mode**: strong-converge(从 forge-config 读)。

## 1. 我对每条分歧的最终立场 + 让步

- **分歧 1**(009 交付身份:独立统一壳 vs 契约化松耦合演进):
  - 对方在 P3R1 给的论证:"共享 point-in-time 数据层 + calibration/alpha 两个评估头,当前更像可契约化的共享回测地基" → **接受**。GPT 接受了我的"一套数据两用"判据,但正确地指出:该判据**当前只证明需要共享数据层 + 两个评估头,不足以证明需要 004/008 之外的新壳**。这个反驳是对的 —— 我 P3R1 自己也把统一壳设成"gated 在契约钉死后仍有不可替代跨层价值",而证据还没到那个门槛。
  - 我的最终立场:**009 当前 = "闭环集成契约规范 + 共享回测地基",落入 004 v1.0 回测 lane + 008 消费契约的松耦合演进;不先建独立统一壳。** 统一壳降级为**未来 gate**,不是当前 verdict。
  - 让步给对方的部分:放弃"009 现在就该是统一容器"的倾向;接受"默认松耦合、统一壳 gated"。这也更贴合 K#2(防 V4)—— 先建大壳正是 operator 最怕的过度设计。
  - **我加的一条(双方都会同意)**:gate 判据要写成**可验收的硬门槛**,不能含糊。门槛 = 当且仅当 calibration 头与 alpha 头需要"004/008 都不拥有的独立回测内核 + 独立状态模型 + 独立验收口径"时,才升级统一壳。在此之前,009 就是一份契约 + 一个共享回测 runner。

- **分歧 2**(上游"信号融合/蒸馏"与红线 #9 边界 —— P3R1 已基本闭合,此处固化):
  - 对方立场(P3R1,≤15 words):"上游可做独立 lane 或内部评分,004 端永不呈现权威综合分"。
  - 我的最终立场:**完全一致,固化为硬约束**。上游 alpha 融合/评分只能存在于两处 —— 独立信号 lane(平权,进 004 冲突报告新增列)或回测层内部指标;蒸馏(proposal 第[4]条)只能落成独立信号源。**004 UI 永不显示"权威综合分"**。
  - 让步:无(本就同向)。转为 decision-list 硬条款 + 可执行验收(防 build runtime 静默越界,对应 K binding②)。

## 2. 联合 verdict(单一)

**009「投资决策闭环」的价值成立,但它当前不是一个要新建的独立统一壳,而是一份"闭环集成契约规范 + 共享回测地基"。** 双方 R2 后一致:保留 004 已 ship 的 strategy 多 lane 地基(StrategyModule IDL / correlation_audit / advisor+XGBoost lane)与 004/008 红线纪律;把 008 forge v4 的"可溯源证据+置信度"契约作为上游输入边界;**最先落地的新增物 = 一个按 SOTA 统计纪律(point-in-time 数据、walk-forward/OOS、交易成本、trial-count、DSR/PBO)建的回测层**,它以"共享 point-in-time 数据层 + calibration 头(承诺壳自校准)+ alpha 头(验证分析师)"的形态,被 004 v1.0 的回测 lane + 008 消费契约以松耦合方式消费。时序异质图谱 defer 到 v2+(gated 在回测证明简单信号不够,且不再受 008 抽取脆弱性放大);蒸馏技能排最后且只能独立 lane 化。**"统一壳是否独立成物"降级为一个显式 gate**:仅当 calibration/alpha 两头需要 004/008 都不拥有的独立回测内核 + 状态模型 + 验收口径时才升级。红线边界固化为硬验收:上游只产独立信号/内部评分,004 端永不呈现权威综合分,alpha 再强也不推出自动执行。**这个 verdict 直接服务 K 的第一性原理(工程补 domain 短板)且主动防 V4(不先建大壳)。**

(无 unresolved。)

## 3. 残余分歧降级为 v0.2 note

- v0.2 note 1:**"一套数据两用"的两个评估头是否最终会长出独立回测内核** —— 当前判松耦合够用,但 calibration(反事实:我的决策 vs 不动)与 alpha(分析师方向 vs 真实股价)的数据模型/评估指标确实不同。回头看的时机:回测层落地、两个头都跑起来后,若发现共享 runner 频繁为迁就另一头而打补丁,即触发 gate 重估。
- v0.2 note 2:**008↔回测的时间戳契约粒度** —— point-in-time 要求"摘要/结构化/价格都按当时可见时间戳入库"(GPT 引 Look-Ahead-Bench)。008 现有的可溯源包是否已带足够细的 as-of 时间戳,还是回测层要自己补一层 as-of 索引,留待 dev plan M1 细化时确认。

## 4. W 形态产出的初步草稿建议(给 synthesizer)

- **W 含 decision-list** → 我建议的 4 列矩阵(前 5 条):
  - **保留(keep)**:① 004 StrategyModule IDL(多 lane 不合并·红线 #9)② correlation_audit strict anti-stub 范式 ③ 004 红线 #1/#9/#10(下游执行边界)④ 008 采集/结构化 + forge v4 "可溯源证据+置信度"消费契约 ⑤ advisor lane + XGBoost lane(现成第二/第三信号源)。
  - **调整(refactor)**:① correlation_audit 雏形 → 升级为 point-in-time 回测统计纪律(+DSR/PBO/trial-count/OOS/交易成本)② 008↔004 接口 → 显式化为"008→回测→StrategyModule→004"四段契约 ③ proposal 第[4]条"自主分析/自给自足"措辞 → 改为"独立蒸馏信号 lane"。
  - **删除(cut)**:无硬删除;proposal 第[4]条越界语义作废(降级为独立 lane)。
  - **新增(new)**:① 共享 point-in-time 数据层 ② calibration 评估头 ③ alpha 评估头 ④ 红线可执行验收条款(004 UI 无权威综合分 / 上游只产独立信号) ⑤ "统一壳升级 gate" 判据文档。
- **W 含 next-PRD** → 关键产品决策点:① 009 v0.1 的交付物 = 契约规范 + 共享回测地基(**不是**独立应用)② 用户故事围绕"验证某分析师有没有 alpha"(TipRanks 式 Hit Ratio+超额+显著性)+"用回测校准我自己的承诺壳"③ IN/OUT 明确:OUT = 统一壳、权威综合分、自动执行、图谱、蒸馏自主分析。
- **W 含 next-dev-plan** → 关键 milestone:**M1** 共享 point-in-time 数据层 + as-of 时间戳契约(接 008 包);**M2** alpha 评估头(分析师验证·DSR/PBO)—— 最先出可验证数字;**M3** calibration 评估头(承诺壳自校准)+ 004 v1.0 回测 lane 消费;**M4(gated)** 图谱/蒸馏,仅在 M2/M3 证明价值后。图谱与蒸馏永不进 v0.1。
- **W 含 refactor-plan** → 关键模块:① 回测层(new·核心枢纽,内建统计纪律)② 004 strategy 层(keep IDL,加"分析师 alpha 得分"独立 lane)③ 008↔回测契约层(refactor·as-of 时间戳)。改造顺序严格 = 数据层 → alpha 头 → calibration 头 → 004 lane 接入。
