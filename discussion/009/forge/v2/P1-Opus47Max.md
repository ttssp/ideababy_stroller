# Forge v2 · 009 · P1 · Opus47Max · 独立审阅(no search · 画蓝图专项)

**Timestamp**: 2026-07-01T03:10:04Z
**Searches used**: NONE in this round.
**Visibility**: I did NOT read other reviewer's v2 P1.
**Reviewer stance**: 审阅人 — 基于 v1 verdict + 004/008/strategy/DB schema 现状,画目标态蓝图 first-take,不 daydream、不推翻 v1。

## 0. 我读到的标的清单 + 阅读策略

- 我读了(全部 5 个 X 标的):
  - `discussion/009/forge/v1/stage-forge-009-v1.md`(v1 单一 verdict + Evidence map + decision-list/AC-1..AC-5 + refactor-plan + PRD draft + dev plan + 自批判)—— **蓝图地基**。
  - `discussion/004/004-pB/PRD.md`(承诺壳现状 · 红线)+ `discussion/008/008-pB/PRD.md`(采集层现状 · US6 接口)。
  - `/home/ys/codes/XenoDev/.../strategy/` 10 个 .py(v1 已一手读,本轮 refresh IDL 约束)。
  - ⭐ `/home/ys/codes/XenoDev/.../alembic/versions/` **13 个 migration**(v2 新增标的)—— 一手读了 `0001_initial_schema`(11 张核心表全文)、`0002_tab_open_log`、`0010_extend_advisor_reports`、`0013_add_strategy_xgboost_metadata`。
- 我跳过的:无。XenoDev 本机可达。
- **K(用户判准)摘要**:v2 = **画目标态蓝图专项**,不重新质疑该不该建(v1 已定)。要把 009 闭环**最终形态 + 器官边界 + 分期演化路线**画彻底,解决"现在各做各的、缺统一方向"。**死守 v1 verdict 不推翻,蓝图 ≠ 一次性建完(防 V4),目标态图指导方向但每期独立可用**。射程 = 画到"闭环自洽跑起来"(采集→结构化→信号→决策→纪律执行→复盘→反馈),四念头就位不画更远。四念头位置全钉死(alpha头/回测枢纽/图谱v2+lane/蒸馏末位lane)。第一性原理 = 工程补投资短板。
- **阅读策略**:Y=目标态架构 → 把七环节逐一映射到"已有器官/要建器官/未来插槽";Y=分期路线 → 找"从现状最小切片到目标态"的依赖链;Y=器官边界 → 重点看 DB schema 里"决策档案/分析师报告/信号"三张表的现成字段,判 calibration/alpha 头接口代价;Y=工程纪律 → refresh StrategyModule IDL + v1 AC 条款。

## 1. 现状摘要(按 Y 视角组织)

### 视角 A · 架构设计/目标态

**读完 DB schema,一个改变蓝图判断的关键事实:闭环"复盘/反馈"环所需的数据字段,004 已经埋好了大半。** `decisions` 表已有:① `would_have_acted_without_agent`(NOT NULL,0/1,R2 强制无默认)—— 这**正是 calibration 头要的反事实字段**("没有承诺壳我会不会照样动");② `post_mortem_json`(可空,"N 天后回填")—— **复盘回填槽已存在**;③ `env_snapshot_json` + `env_snapshots` 表(决策时点 price/holdings 快照)—— **point-in-time 决策快照已存**。`advisor_reports` 表(source_id/week_id/structured_json + 0010 加的 transcript/key_points)= alpha 头输入源;`strategy_signals` 表(source_id/direction/confidence/inputs_used_json)= 信号 lane 输出已持久化且带 source 隔离。

**所以目标态蓝图的"器官清单"比想象的清晰**:
- **已有器官(keep)**:008 采集层 / strategy 信号层(多 lane IDL)/ 004 承诺壳(decisions+conflict_reports+rebuttals)/ 004 复盘半槽(post_mortem_json + would_have_acted 字段)。
- **要新建器官(new)**:回测层 = **共享 point-in-time 数据层 + alpha 头 + calibration 头**。⚠ 关键缺口:schema 里 `advisor_reports` **没有 realized-return / 价格结果列** —— alpha 头要"分析师方向 vs 之后真实股价",必须新建一个**价格历史表 / 时序数据层**(004 现在只有决策时点的 `env_snapshots.price` 单点,没有连续价格序列)。这是蓝图必须画出的新器官,不能靠复用 004 表糊过去。
- **未来插槽(gated)**:图谱 lane(v2+)/ 蒸馏 lane(末位)—— 都实现 StrategyModule 接口,平权进 conflict_reports。

### 视角 B · 可演化性/分期路线

**"复盘/反馈"环怎么闭合,是蓝图 v1 没画透、v2 必须补的核心。** 闭环之所以是"环",在于回测算出的东西要**回流调旋钮**。基于 schema 我能画出这个回流:alpha 头产"某分析师 hit-rate/超额" → 回流去调**该分析师信号 lane 的 confidence 权重**(上游信号给多强);calibration 头产"我的反事实纪律得分"(用 `would_have_acted_without_agent` × 后续 `post_mortem_json` 结果)→ 回流去调**承诺壳的纪律强度**(下游卡多严,如 devil's advocate 触发阈值)。**这两条回流线就是闭环的"反馈"环**,目标态图必须画出,且它们**依赖 M2/M3 评估头先跑通**才有数据回流 —— 天然的分期依赖链。

分期最小切片:**M1 价格历史/as-of 数据层 → M2 alpha 头(先出"某分析师行不行"的数字,这是 operator 最想要的、也最独立可用)→ M3 calibration 头 + 两条回流线 → M4(gated)图谱/蒸馏**。每期独立可用:M2 完就能单独回答"分析师有没有 alpha"(不依赖 M3);M3 完闭环才真正闭合。

### 视角 C · 器官边界清晰度

**四念头位置(K 要求全钉死)+ schema 佐证**:
- **① 验证 alpha → 回测层 alpha 头**:输入 = `advisor_reports`(已有)+ 新价格历史表(缺,要建);输出 = hit-rate/超额/Z 显著(v1 定的 TipRanks+DSR/PBO)。**边界**:只产"某 source_id 的得分",不跨 source 合并(v1 AC-2)。
- **② 回测 → 共享数据层 + 两头**:是"复盘/反馈"环的枢纽。**边界**:数据层是唯一行情来源(point-in-time),两头共享它但指标分离。
- **③ 图谱 → v2+ 信号 lane(gated)**:实现 StrategyModule,平权进 conflict_reports。**gated 条件**:回测证明简单信号不够 + 008 抽取脆弱性可控。v0.1 只在图上标插槽位置,不画内部。
- **④ 蒸馏 → 末位独立 lane**:同样 StrategyModule。**边界**:AC-4,只增强单 lane 能力,不替人决策、不综合打分。

**上下游边界(schema 层面已清晰)**:上游(008 采集 + 回测 + 信号 lane)只写 `strategy_signals`(带 source_id);下游(004 承诺壳)读 `conflict_reports`(R10 红线:无 priority/winner/recommended 字段)—— **数据库层面就 enforce 了"永不权威综合分"**(v1 AC-1 有 schema 背书!)。

### 视角 D · 工程纪律

004 的 schema 本身就是纪律范式:`conflict_reports` DDL 注释明写"无 priority/winner/recommended 字段(R10 红线)"、`strategy_signals.rationale_plain` CHECK 非空(R3)、`would_have_acted_without_agent` 无默认强制填。**蓝图的接口契约应继承这套"约束写进 schema/DDL"的范式** —— 新建的价格数据层 + 两个评估头的接口,也该有 CHECK/NOT NULL 级的硬约束(如 as-of 时间戳 NOT NULL 防 look-ahead,对应 v1 AC-5)。**风险**:回测层是新器官,最容易和 004 表耦合死(比如 alpha 头直接写 `strategy_signals` 而不走 StrategyModule IDL)—— 蓝图必须画清"回测层→信号 lane→strategy_signals"的单向契约,不让回测层绕过 IDL 直连 DB。

## 2. First-take 评分(按 Y 视角)

| Y 维度 | 倾向 | 理由(引用 §1 现状) |
|---|---|---|
| 架构设计/目标态 | **refactor(器官图)+ 1 个关键 new** | §1A:七环节器官大半已有(含 004 复盘半槽),蓝图=把它们画成一张图 + 补 1 个真缺口(价格历史/时序数据层,`advisor_reports` 无价格结果列)。 |
| 可演化性/分期路线 | **new(反馈环 + 分期链)** | §1B:v1 没画透的"复盘→反馈"回流(alpha得分→信号权重 / calibration→纪律强度)是闭环闭合关键,须新画;分期 M1数据层→M2 alpha头→M3 calibration+回流→M4 gated。 |
| 器官边界清晰度 | **keep(边界已清)+ 钉死四念头** | §1C:上下游边界 schema 已 enforce(conflict_reports 无 winner 字段 = AC-1 有 DB 背书);四念头位置按 K 全钉死。 |
| 工程纪律 | **keep(约束写进 schema 范式)** | §1D:004 把红线写进 DDL CHECK 的范式该继承;风险是回测层绕过 IDL 直连 DB,蓝图须画单向契约。 |

## 3. 我现在最不确定的 3 件事

1. **"复盘/反馈"环的两条回流线,该做成"自动调旋钮"还是"给人看的建议"?** 我 §1B 画的回流(alpha 得分→信号 confidence 权重 / calibration→纪律阈值)—— 如果"自动调",会不会滑向"系统自动决定信号多强"从而软性触碰"别让子系统静默定方向"(K binding①)?还是应该做成"回测给出建议旋钮值,人确认后才生效"?这关系到闭环是"全自动反馈环"还是"人在环上的半自动"。希望 P2 看 SOTA(量化系统的 calibration 回流通常自动还是人工)+ P3 帮我判边界。

2. **价格历史/时序数据层这个新器官,范围划到哪?** alpha 头要"分析师方向 vs 之后真实股价",最小要一个"ticker × 日期 → 收盘价"表。但 calibration 头要"我的决策 vs 不动反事实",可能还要"决策时点之后 N 天的价格路径"。这两个的价格数据需求**是不是同一张表**(v1 说"共享数据层"),还是 alpha 要日频序列、calibration 要事件驱动路径,其实是两种粒度?这直接决定 M1 数据层的形态。希望 P2 看回测数据层 SOTA 怎么分层。

3. **蓝图该画到多"实"?** K 说射程到"闭环自洽",四念头就位。但我不确定:图谱/蒸馏这两个"未来插槽",在目标态图里该只画一个"插槽位置 + 接口签名"(StrategyModule),还是要画出它们和其他器官的数据依赖?画太实怕变成 V4(为没验证的东西设计),画太虚怕蓝图不够"充分彻底"(operator 的诉求)。希望 P3 帮我定这个"目标态完整性 vs 防过度设计"的平衡点。
