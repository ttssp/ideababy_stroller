# Forge Stage · 009 · v1 · "投资决策闭环 = 集成契约 + 共享回测地基,不先建统一壳"

**Generated**: 2026-07-01T12:00:00+08:00
**Source**: forge run v1 with X = 5 标的, Y = 架构集成 / 愿景成立性 / 可行性(回测+图谱) / 工程纪律, Z = 对标 SOTA, W = decision-list + next-PRD + next-dev-plan + refactor-plan
**Convergence mode**: strong-converge
**Rounds completed**: P1 (both), P2 (both), P3R1 (both), P3R2 (both)
**Searches run**: 12 across ~11 distinct sources (TipRanks / Bailey-López de Prado DSR+PBO / QuantConnect 五层 / Barber-Odean / THGNN 金融图谱 / Look-Ahead-Bench point-in-time / 事件vs向量回测 / 行为纪律缺口 / 幸存者偏差 / sell-side analyst arXiv)
**Moderator injections honored**: none
**Convergence outcome**: converged(单一 verdict,无 unresolved)

---

## How to read this

forge 是横切层(不是 L1-L4 pipeline 的一部分)。本文档是双专家(Opus 4.7 Max + GPT-5.5 xhigh)对 009 闭环 proposal + 004/008 现状 + 004 已 ship strategy 代码的独立审阅、SOTA 对标、四轮联合收敛后的产出。strong-converge 模式 → **强制给出单一 verdict**(不是候选菜单 defer 给你拍板)。

读完后你应该:
- 知道双专家对"009 是否该建、以什么形态建"的最终 verdict
- 能在 §"Evidence map" 逐条溯源每个结论到 P1/P2/P3 的具体段落 + SOTA 证据
- 拿到 4 件按 W 形态准备好的可执行草案:decision 矩阵 / 架构 refactor 方案 / 下一版 PRD 草案 / dev plan
- 能基于 §"Decision menu" 直接进入下一步(局部接受起 v0.1 PRD / park / 跑 v2)

**一句话预警**:verdict 的核心是"**不先建统一壳**" —— 这正是主动防你踩过的 V4 失败模式。如果你读到任何地方感觉像"又要建个大系统",那是理解偏差,请回到 §"Verdict"。

## Verdict

**009「投资决策闭环」的架构级价值成立,但它当前不是一个要新建的独立统一壳,而是一份"闭环集成契约规范 + 共享回测地基"。** 保留 004 已 ship 的 strategy 多 lane 地基(StrategyModule IDL / correlation_audit / advisor+XGBoost lane)与 004/008 红线纪律;把 008 forge v4 的"可溯源证据+置信度"契约作为上游输入边界。**最先落地的新增物 = 一个按 SOTA 统计纪律(point-in-time 数据 / walk-forward+OOS / 交易成本 / trial-count / DSR+PBO)建的回测层**,形态为"共享 point-in-time 数据层 + calibration 头(承诺壳自校准)+ alpha 头(验证分析师)",被 004 v1.0 回测 lane + 008 消费契约以**松耦合**方式消费。时序异质图谱 defer 到 v2+;蒸馏技能排最后且只能独立 lane 化。**"统一壳是否独立成物"降级为显式 gate**:仅当 calibration/alpha 两头需要 004/008 都不拥有的独立回测内核 + 状态模型 + 验收口径时才升级。

**回应 K**:此 verdict 直接服务 K 第一性原理(用回测统计纪律 DSR/PBO 把"判分析师可不可信"变成可验证工程任务 = 工程补 domain 短板),且用"契约先行、不先建大壳"主动防 K#2 的 V4 风险;严守 K"两灵魂共存、别推翻红线"(上游只产独立信号,下游 004 红线作边界)。

## Evidence map

| 结论 | 来源 | 引用 | 是否有反对证据 |
|---|---|---|---|
| 009 不从零造,004 已 ship 信号层实质骨架(多 lane + correlation_audit) | P1-Opus §1A / config X#5 摘录 | "004 已经 ship 了闭环信号层的实质骨架" | - |
| 闭环有架构级价值,非 V4(文献背书组合 + 市面无整合先例) | P2-Opus §1 row 5(行为金融) | "组合有文献背书,但市面无整合品→价值在集成本身" | ⚠ 价值全锁在集成质量,边界糊则归零(见下) |
| 但当前不该先建统一壳 → 降级为契约规范 + 共享回测地基 | P3R2-Opus §2 / P3R2-GPT §2 | "当前只证明需要共享数据层+两个评估头,不足以证明需要新壳" | ⚠ 曾是分歧 1(Opus 初倾向"合",R2 让步) |
| 回测 new-first 且是"防自欺统计纪律层"(非普通报表) | P2-GPT §1 row 2 / P2-Opus §1 row 2 | "PBO/DSR 说明回测是防自欺的统计纪律层" | - |
| 分析师 alpha 验证指标可抄 TipRanks 三件套(命中率+超额+Z显著) | P2-Opus §1 row 1 | "TipRanks 三件套,不必重新发明指标" | - |
| 回测须内建 point-in-time / walk-forward+OOS / 交易成本 / trial-count / DSR+PBO | P2-Opus §1 row 2+3 / P2-GPT §1 row 2+6 | "trial-count 记账+DSR;数据层是唯一行情来源" | - |
| "一套数据两用" = 共享 point-in-time 数据层 + calibration 头 + alpha 头 | P2-Opus §1 row 3 | "共享一个 point-in-time 数据层,两个评估头" | v0.2 note 1:两头指标模型不同,或逼出独立内核 |
| 时序异质图谱 defer 到 v2+(NLP 关系抽取放大 008 抽取脆弱性) | P2-Opus §1 row 4 / P2-GPT §1 row 5 | "图谱会把 008 的抽取脆弱性二次放大(边错→图错→信号错)" | - |
| 红线 #9 边界:上游只产独立信号 lane / 内部评分,004 UI 永不呈现权威综合分 | P3R2-Opus §1 分歧2 / P3R2-GPT §1 边界固化 | "004 UI 永不显示权威综合分" | - |
| alpha 再强也不推出自动执行(红线 #1) | P2-GPT §1 row 4(Barber-Odean) | "004 红线不但站住,还应作为 009 下游边界" | - |
| 蒸馏(proposal 第[4]条)只能落成独立信号 lane,"自主分析"措辞越界作废 | P1-Opus §1B / P3R2-GPT §3 note 3 | "边界全在蒸馏出的东西是独立信号还是权威决策" | - |
| 统一壳升级 = 显式 gate(仅当两头需 004/008 都无的独立回测内核+状态模型+验收口径) | P3R2-Opus §1 分歧1 / P3R2-GPT §2 | "只有当二者需要 004/008 都不拥有的独立回测内核...才升级" | - |

## Intake recap

### X · 审阅标的(5 个)
- `proposals/proposals.md` §009 段(proposal · 行 266 起)— 核心 X,四条想法 + 第一性原理 + 复用清单
- `discussion/004/004-pB/PRD.md`(PRD · 237 行)— 004 决策账本/承诺壳现状 + 红线 #1/#9
- `discussion/008/008-pB/PRD.md`(PRD · 315 行)— 008 采集/结构化层现状 + 008↔004 接口
- `discussion/008/forge/v4/stage-forge-008-v4.md`(forge stage)— 008 forge v4 verdict(信号 spike 硬前置 + 消费契约)
- `/home/ys/codes/XenoDev/projects/004-pB/src/decision_ledger/strategy/`(外部 repo · 10 个 .py)— 004 已 ship strategy 层。**双方均真实读取,无 fallback / 无沙箱 BLOCK**(P1-Opus §0 + P1-GPT §0 均确认 XenoDev 本机可达)

### Y · 审阅视角
- 架构设计/集成(核心)
- 产品价值/愿景成立性(核心)
- 可行性/风险(回测 + 图谱)
- 工程纪律

### Z · 参照系
- mode: 对标 SOTA
- 用户外部材料: 无(X 的 5 个标的即全部一手材料,双方 P2 §2 均确认无额外 URL 待叠加)

### W · 产出形态
- next-PRD draft ✅
- 架构 refactor-plan ✅
- next-dev-plan ✅
- decision-list 矩阵 ✅

(verdict-only / free-essay 未勾选 → 本文档无 §"Verdict rationale" / §"Long-form synthesis")

### K · 用户判准
> 我要 forge 009 这个投资决策闭环集合体,是因为我已分散建了 004(决策账本/承诺壳)和 008(投顾采集),还有四条新想法(验证分析师 alpha / 回测 / 时序异质图谱 / 蒸馏技能),现在想把它们合成一个完整闭环。
>
> **第一性原理**:我懂算法、自动化、数据,但**不懂投资**。产品本质 = 用工程强项补投资 domain 短板。投资知识/纪律靠外部专家(008 采集投顾)、策略能力靠外部信号+自己内测的回测、"分析师行不行"靠回测数据说话、执行不走样靠 004 纪律承诺壳。
>
> **闭环灵魂已定**:"承诺壳"(防乱动)和"alpha 引擎"(验证/信号/策略)不冲突、永久共存、分居上下游。**别建议推翻 004 红线**(#1 自动下单永不破 / #9 信号不合并)——它们管下游执行层,不约束上游信号/回测层。
>
> **要你们盯死的(按重要性)**:① 闭环架构怎么搭、004/008 怎么干净并入(复用已 ship strategy 层)② 集合体是否真有架构级价值 or V4 式过度设计 ③ 回测怎么作两灵魂公共地基先落地(一套数据两用,防过拟合/训练集污染)④ 四条排期(图谱该不该现在上、蒸馏是不是最后)。
>
> **binding**:① 投资 domain 判断给可验证依据(回测数字/SOTA)② 别让任何子系统(尤其 build runtime)静默替我定方向(防 V4)③ 008 合规边界不重审 ④ 自用单人不商业化。

### 收敛模式
strong-converge → 单一 verdict + 残余分歧降级为 v0.2 note(见 §"What this menu underweights")

---

## Decision matrix

针对 004/008/四条想法各组件的现状,4 列决策矩阵。每行可在 §"Evidence map" 溯源。

| 类别 | 项 | 来源(标的的具体位置) | 理由 | 优先级 |
|---|---|---|---|---|
| **保留** | StrategyModule IDL(source_id+analyze→StrategySignal,多 lane 不合并) | 004 `strategy/base.py` | 红线 #9 的架构实现,天然容下"上游多信号"(P1-Opus §1B) | P0 |
| **保留** | lane 隔离 + 只读 SourceDataProvider + fail-closed | 004 `strategy/base.py` 不变量 #14 | 集成不能糊边界的硬约束(P1-GPT §1 工程纪律) | P0 |
| **保留** | advisor lane + XGBoost lane(+feature_engineering+train) | 004 `advisor_strategy.py` / `xgboost_model.py` | 现成第二/第三信号源,真金白银已 ship,别浪费(K#1) | P0 |
| **保留** | 004 红线 #1(自动下单永不破)/ #9(信号不合并)/ #10(不把不动当失败) | 004 PRD §5 Scope OUT | 下游执行层边界,Barber-Odean 加固(P2-GPT §1 row 4) | P0 |
| **保留** | 008 采集/结构化 + forge v4 "可溯源证据+置信度"消费契约 | 008 PRD US6 + 008 forge v4 stage | 上游输入边界,回测输入质量的上限(P1-Opus §1C 依赖链) | P0 |
| **调整** | correlation_audit 雏形(Pearson<0.5 去重) → 完整回测统计纪律 | 004 `correlation_audit.py` | Pearson 远不足以判 alpha,须升级 DSR/PBO/trial-count/OOS/交易成本(P2-GPT §1 row 2) | P0 |
| **调整** | 008↔004 粗包接口 → 显式化"008→回测→StrategyModule→004"四段契约 | 008 PRD US6 接口 | 集成边界必须契约化钉死,否则价值归零(P2-Opus §1 row 5) | P0 |
| **调整** | proposal 第[4]条"自主分析/自给自足"措辞 → "蒸馏独立信号 lane" | proposal §009 想法4 | 措辞危险滑向越界红线 #1/#9,须钉死(P1-Opus §1B) | P1 |
| **删除** | 009 独立统一壳(当前不建) | proposal §009 隐含"统一闭环产品" | 先建大壳正是 operator 最怕的 V4(P3R2 双方 §2) | P0 |
| **删除** | 004 权威综合分 / 自动执行(v0.1 及以后均不做) | — | 红线硬边界(见下"可执行验收条款") | P0 |
| **删除** | v0.1 图谱 / 蒸馏自主决策 | proposal §009 想法3/4 | 图谱放大 008 抽取脆弱性;蒸馏越界(P2-Opus §1 row 4) | P0 |
| **新增** | 共享 point-in-time 数据层(唯一行情来源,只用过去信息) | (无 — 新建议) | SOTA 回测分层的枢纽(P2-Opus §1 row 3) | P0 |
| **新增** | alpha 评估头(分析师方向 vs 真实股价,TipRanks 三件套) | (无 — 新建议) | 最先出可验证数字,直接答"分析师行不行"(K#1 想法1) | P0 |
| **新增** | calibration 评估头(我的决策 vs 不动反事实,服务承诺壳) | (无 — 新建议) | 一套数据两用的第二头(K#3) | P1 |
| **新增** | 红线可执行验收条款(见下) | (无 — 新建议) | 防 build runtime 静默越界(K binding②) | P0 |
| **新增** | "统一壳升级 gate" 判据文档 | (无 — 新建议) | 把 V4 防御写成显式门槛(P3R2 双方 §1) | P0 |

### 红线可执行验收条款(对应 K binding② · 防 build runtime 静默越界)

以下条款必须写进 009 v0.1 契约规范,并作为 L4 build 的**验收 gate**(任意一条违反 = BLOCK):

- **AC-1(无权威综合分)**:004 前端 / API 响应中,任何字段都**不得**出现"跨信号源合并后的单一权威评分/推荐"。上游多信号只能以**独立列**呈现在冲突报告中(每列标 source_id),永不出现"综合分"。
  - 可测:grep 契约 schema 无 `aggregate_score` / `authoritative_signal` / `merged_recommendation` 类字段;冲突报告渲染至少保留 N 个独立 source 列。
- **AC-2(上游只产独立信号)**:回测层的 alpha 评分只能存在于**两处** —— (a) 独立信号 lane(实现 StrategyModule,平权进 004 冲突报告),或 (b) 回测层内部指标(不出回测层)。不得有第三种"融合评分"出口。
  - 可测:StrategyModule registry 中每个 lane 的 `source_id` 唯一;回测层对外接口只暴露"某 source 的 hit-rate/超额/DSR",不暴露"跨 source 合并结论"。
- **AC-3(不推自动执行)**:alpha 再强,系统**不得**产生任何自动下单 / 自动调仓动作。所有执行动作必须经人显式确认(004 红线 #1)。
  - 可测:代码中无 broker/order-submit 调用路径;所有 action 走人工确认闸。
- **AC-4(蒸馏仅独立 lane)**:proposal 第[4]条蒸馏能力,只能实现为**一个独立信号 lane 的能力增强**,不得实现为"替人决策"或"跨源综合打分"。
  - 可测:蒸馏产物注册为一个 `source_id`,输出仍是 StrategySignal(direction/confidence/rationale),不写权威结论字段。
- **AC-5(point-in-time 不泄漏未来)**:回测所用的原文/摘要/结构化字段/价格数据,全部按**当时可见时间戳(as-of)**入库;任何信号计算不得读取信号时点之后的信息。
  - 可测:回测 runner 有 as-of cutoff 参数;单测覆盖"未来数据泄漏"负例(Look-Ahead-Bench 式)。

---

## Refactor plan

按模块分组。**改造顺序严格 = 数据层 → alpha 头 → calibration 头 → 004 lane 接入**(双方 P3R2 §4 一致)。

#### 模块 A · 回测层(new · 009 的实际枢纽)
- **当前问题**:004 只有 `correlation_audit.py` 的 Pearson 相关性雏形(60-day window + strict anti-stub),**远不足以判 alpha**(P2-GPT §1 row 2)。缺 point-in-time、OOS、交易成本、trial-count、DSR/PBO。
- **目标态**:一个"防自欺的统计纪律层"。分层 = 共享 point-in-time 数据层(唯一行情来源)→ 向量化计算层(v0.1 低频原型够用,事件驱动留 later)→ 两个评估头。指标头分离:calibration 头 vs alpha 头(P2-Opus §1 row 3)。
- **改造步骤(顺序)**:
  1. 建共享 point-in-time 数据层 + as-of 时间戳契约(接 008 证据包 + 价格数据)
  2. 建 alpha 评估头:分析师方向 vs 真实股价 → Hit Ratio + 平均超额 + Z 显著性 + DSR/PBO + 样本窗报告(TipRanks 三件套 + Bailey/López de Prado)
  3. 建 calibration 评估头:我的决策 / 不动反事实 / 004 档案接入同一 runner
- **风险**:calibration 头与 alpha 头数据模型/指标不同,共享 runner 可能被迫为迁就一头打补丁(v0.2 note 1 → 触发统一壳 gate 重估)。
- **预估代价**:L(核心新建 + 统计纪律实现,双方 P3R2 §4 均列为最先且最重)

#### 模块 B · 004 strategy 层(keep IDL / refactor 加 lane)
- **当前问题**:StrategyModule IDL 干净,但 alpha 回测得分尚无入口。
- **目标态**:保留 IDL 与多 lane 架构;新增"分析师 alpha 得分 / 蒸馏信号"独立 lane;**禁止综合分**(P3R2-GPT §4)。
- **改造步骤**:
  1. 回测层的 alpha 得分实现为一个新 StrategyModule lane(平权进冲突报告)
  2. 蒸馏产物(later)同样注册为独立 lane
- **风险**:build runtime 静默把"上游 alpha 融合"写成 004 域内综合建议,穿透红线(P1-GPT §1 工程纪律)→ 由 AC-1/AC-2 验收条款守住。
- **预估代价**:S(复用现有 IDL,新增 lane 是既定扩展点)

#### 模块 C · 008↔回测契约层(refactor)
- **当前问题**:008 现有可溯源轻量包的 as-of 时间戳粒度未知,是否够回测 point-in-time 待确认(v0.2 note 2)。
- **目标态**:补 as-of 时间戳 + source_ref + 置信度 + degraded 状态,保证回测可复现且不误认 008 在给建议(P3R2-GPT §4)。
- **改造步骤**:
  1. 审 008 轻量包是否带足够细 as-of 时间戳
  2. 不足则回测层自补一层 as-of 索引
- **风险**:时间戳粒度不足 → 回测隐性泄漏未来(违反 AC-5)。
- **预估代价**:M(依赖 008 现状核查结果,M1 细化时确定)

---

## Next-version PRD draft

```
# PRD · 009 · v0.1

**Status**: Draft from forge v1, awaiting human approval
**PRD-form**: simple
**Source**: forge stage-forge-009-v1.md
**Sources**: proposal §009 + 004 strategy 层(已 ship)+ 008 forge v4 消费契约 + SOTA(TipRanks/DSR-PBO/QuantConnect)

## 定位(关键 · 防 V4)
009 v0.1 的交付物 = **闭环集成契约规范 + 共享回测地基**,**不是**一个新建的独立应用壳。
它落入 004 v1.0 回测 lane + 008 消费契约的松耦合演进。

## User persona
单人自用 operator。懂算法/自动化/数据,不懂投资、无专业投资经验(K 第一性原理)。
需要用工程强项(回测统计纪律)补投资 domain 短板。

## Core user stories
- 作为不懂投资的 operator,我要**验证某个分析师到底有没有 alpha**(Hit Ratio + 平均超额 + 显著性),
  好判断能不能把他作为关键参考信号,而不是凭"年初买存储股赚过"的主观印象。
- 作为容易临场乱动的 operator,我要**用回测校准我自己承诺壳的纪律强度**(我的决策 vs 不动反事实)。
- 作为闭环搭建者,我要让 008 采集的证据包**能被回测消费、也能被 004 消费**,且全程 as-of 可复现。

## Scope IN
- 共享 point-in-time 数据层(as-of 时间戳契约,接 008 证据包 + 价格数据)
- alpha 评估头(分析师验证:命中率/超额/Z 显著性/DSR/PBO/样本窗)
- calibration 评估头(承诺壳自校准)
- "008→回测→StrategyModule→004"四段契约规范
- 红线可执行验收条款 AC-1..AC-5
- "统一壳升级 gate" 判据文档

## Scope OUT(显式 non-goals · 每条引 Evidence map)
- **009 独立统一壳**(先建大壳 = V4;P3R2 双方 §2)
- **004 权威综合分**(红线 #9;Evidence map "红线 #9 边界"行)
- **自动下单/自动执行**(红线 #1;Evidence map "alpha 再强也不推自动执行"行)
- **时序异质图谱**(defer v2+;Evidence map "图谱 defer"行 —— NLP 抽取放大 008 脆弱性)
- **蒸馏自主决策**(只能独立 lane;Evidence map "蒸馏只能落独立 lane"行)

## Success looks like
- 能对目标分析师产出一份 as-of 可复现的 alpha 报告(命中率+超额+DSR/PBO+样本窗),
  数字能回答"他能不能 beat 一般分析师"(K 想法1 的"beat 80-90%"是判据,非 v0.1 硬门槛)。
- 回测层通过 AC-5 泄漏负例测试(不读未来信息)。
- 004 端渲染时无任何"综合分"字段(通过 AC-1)。

## Real constraints
- 自用单人,不商业化(K binding④)
- 008 合规(付费自用/有效登录态/不传播)是既定前提,不重审(K binding③)
- 回测输入质量 ⊂ 008 提取可靠性(008 forge v4 spike 是上游依赖)

## UX principles
- 上游多信号永远以独立列呈现,人最终拍板(不给"权威结论")
- 投资 domain 判断永远附可验证依据(回测数字),不让 operator 凭感觉(K binding①)

## Open questions(forge 也没解决的)
- 008 现有轻量包 as-of 时间戳粒度是否够 point-in-time?(v0.2 note 2,M1 定)
- calibration 头与 alpha 头最终会不会长出独立回测内核 → 触发统一壳 gate?(v0.2 note 1)
```

---

## Next-version dev plan

按 milestone 切(不到 spec 级 — spec 是 L4 的工作)。双方 P3R2 §4 milestone 一致,取合并版。

## M1 · point-in-time / as-of 数据契约(预估 M)
- 目标:落地共享数据层 + as-of 时间戳契约,接入 008 证据包与价格数据。
- 关键 milestone:
  - M1.1: 定义 as-of 契约(原文/摘要/结构化字段/价格全带当时可见时间戳)
  - M1.2: 核查 008 轻量包时间戳粒度;不足则补 as-of 索引层
- 依赖:008 现状(可溯源包) + 价格数据源接入
- 风险:时间戳粒度不足 → 隐性泄漏未来(AC-5 守)

## M2 · alpha 评估头(预估 L)· **最先出可验证数字**
- 目标:先做 alpha 头,产分析师 hit rate / 超额收益 / 显著性 / DSR/PBO / 样本窗报告。
- 关键 milestone:
  - M2.1: Hit Ratio + 平均超额 + Z 显著性(TipRanks 三件套)
  - M2.2: walk-forward/OOS 分割 + 交易成本 + trial-count 记账 + DSR/PBO deflate
- 依赖:M1 数据层
- 风险:trial-count 不记账 → DSR 无法正确 deflate(过拟合自欺,P2-Opus §1 row 2)

## M3 · calibration 评估头(预估 M)
- 目标:做 calibration 头,把我的决策 / 不动反事实 / 004 档案接入同一 runner。
- 关键 milestone:
  - M3.1: 反事实 calibration 数据模型
  - M3.2: 004 v1.0 回测 lane 消费(alpha 得分 + calibration 结果)
- 依赖:M2(共享 runner 已跑通)
- 风险:两头指标不同,runner 被迫打补丁 → 触发统一壳 gate 重估(v0.2 note 1)

## M4(gated)· 图谱 / 蒸馏
- 目标:仅在 M2/M3 证明简单信号有价值后,另起 gate 评估。
- 门槛:图谱 gated 在"回测证明简单信号不够 + 008 抽取脆弱性可控";蒸馏落成独立 lane。
- **图谱与蒸馏永不进 v0.1。**

---

## What this menu underweights(强制自批判)

- **反对证据未充分整合**:§"Evidence map" 中标 ⚠ 的两条 ——(a)"闭环价值全锁在集成质量,边界糊则归零"(P2-Opus §1 row 5 + P1-GPT 同担忧):verdict 用"契约先行 + AC 验收条款"对冲,但**若 build runtime 集成时把契约做松了,verdict 的价值前提就塌了**,这是最大单点风险;(b) 分歧 1 是 Opus 让步的结果(初倾向"合"),不是天然共识 —— 若未来发现松耦合频繁打补丁,verdict 可能反转为统一壳(已写成 v0.2 note 1 gate)。

- **Y 视角覆盖盲区**:Y 未含"安全/隐私",但 008 采集的是付费投顾私域内容 + 回测涉及个人决策档案,数据敏感度高。本轮未评估存储/访问控制,值得 L4 或 v2 补 attention。**注意:合规按 K binding③ 明确不重审,此处仅指工程侧数据安全,非合规。**

- **K 中未充分回应的关切**:K 想法1 提"要 beat 80-90% 的一般分析师才够价值" —— verdict 给了度量方法(TipRanks 三件套 + DSR/PBO),但**没给"80-90% 分位"的 baseline 数据从哪来**(需要一个分析师样本池做分母)。这是 M2 落地时会撞到的现实缺口,PRD Open questions 已挂,但值得 operator 预期:v0.1 可能只能给"这个分析师 vs 大盘/S&P500"的绝对超额,给不出"vs 80-90% 同行"的分位。

- **convergence_mode 副作用**:strong-converge 让两模型高度对齐(P3R1 双方均自述"收敛度异常高")。**回声室风险**:双方都判"图谱 defer"、都判"回测 new-first",证据虽硬(THGNN 抽取重坑 + DSR/PBO 有先例),但**双模型同源于相似训练语料,可能共享同一盲点** —— 例如都低估了"分析师 alpha 回测所需的干净历史数据获取成本"(008 语料只到某时间点、单一分析师、样本量可能不足以 DSR 显著)。这条 P1-Opus §1C 已隐约提及但未在 verdict 展开。

- **X 标的覆盖局限**:双方读了 004 strategy 层 10 个 .py,但**未读 004 的 13 个 alembic migration(DB schema 全貌)**(proposal §009 提到但不在 X 清单)。回测层的 calibration 头要接"004 档案",DB schema 是否已有反事实所需字段未核实 → 可能影响 M3 代价估计。

- **forge versioning 提示**:以下新信息进入会触发 v2 跑并可能改变 verdict ——(1) M2 落地后发现分析师历史样本量不足以让 DSR 显著(alpha 判不出来)→ 需重估整个闭环前提;(2) 松耦合 runner 频繁打补丁 → 触发统一壳 gate(v0.2 note 1);(3) operator 决定要"beat 80-90% 同行"的严格分位 → 需评估分析师样本池采集(新 domain 工作)。

## Decision menu(for human)

### [A] 接受 verdict 进 L4(需 fork 出 PRD branch)
```
⚠ /plan-start 要求 <prd-fork-id> + 完整 PRD 目录,不能直接吃 forge stage 文档。
⚠ 现有仓库 PRD 都是平铺布局 — discussion/<root>/<prd-fork-id>/PRD.md(无嵌套)
⚠ 特别注意:本 verdict 的核心是"009 v0.1 不是独立应用壳,而是契约规范 + 共享回测地基"。
   若进 L4,PRD 必须严守这个定位,不能被 build runtime 悄悄扩成大壳(K binding②)。

流程(暂时手工,等待 /fork-from-forge 命令落地):

1. 选一个 prd-fork-id:009 是 root → 如 009-pForge / 009-forgeV1
   prd-fork-id 直接放在 discussion/009/ 下(平铺,不嵌套)

2. 创建 discussion/009/<prd-fork-id>/PRD.md
   - 把本 stage 中的 §"Next-version PRD draft" 抽出
   - 补 frontmatter:
     **PRD-form**: simple
     **Source**: forge stage-forge-009-v1.md

3. 创建 discussion/009/<prd-fork-id>/FORK-ORIGIN.md
   说明 forked-from = forge stage,parent = 009(非 L3 candidate)

4. /plan-start <prd-fork-id>
   → 产 HANDOFF.md → 新开 XenoDev session 真开发(spec/tasks/build/quality)
```
适用:你接受"契约 + 共享回测地基"定位,想直接推进 M1 数据层落地。

### [B] 跑 forge v2(说明需要补什么)
```
/expert-forge 009
# 在 Phase 0 intake 时调整 X / Y / Z / W / K
# 旧 v1 整目录保留作历史参考
```
适用:
- 想把 §"underweights" 的盲点纳入(补读 004 alembic schema / 评估分析师样本量够不够 DSR 显著 / 数据安全视角)
- K 关切发生变化(例如决定要严格的"beat 80-90% 同行"分位)

### [C] 局部接受(推荐起点)
verdict 已高度收敛,但你可能想分批采纳:
- ✅ 建议先采纳:回测 new-first 定位 + 红线 AC-1..AC-5 验收条款 + 图谱/蒸馏 defer(这三条证据最硬、争议最小)
- ⏸ 可挂起:calibration 头(M3)—— 先看 M2 alpha 头能不能出可信数字,再决定 calibration 值不值得建
- ⏸ 可挂起:统一壳 gate 判据文档 —— 等松耦合真跑起来遇到打补丁时再写,避免过早形式化
- ❌ 需你确认拒绝的:无(verdict 无 unresolved,双方 R2 一致)

### [P] Park
```
/park 009
```
保留所有 forge 产物,标记为暂停。复活时不重做 forge 层。
适用:M2 依赖的分析师历史数据尚未就绪,或 008 forge v4 的信号 spike 还没落地(009 回测上游依赖它)。

### [Z] Abandon
```
/abandon 009
```
forge verdict **不支持** abandon —— 双方判"闭环价值成立、非 V4"。仅当你后续发现分析师样本量根本判不出 alpha(闭环前提塌了)才考虑,归档 lesson 文档。

---

## Forge log
(由 /expert-forge 命令更新;记录每次 forge run 的 v 序列 + 关键 verdict 一句话)

- v1: 2026-07-01 — verdict: "009 = 闭环集成契约规范 + 共享回测地基(非独立统一壳);回测 new-first 按 DSR/PBO 建,图谱 defer v2+,蒸馏最后且独立 lane 化,004 端永不呈现权威综合分。"
