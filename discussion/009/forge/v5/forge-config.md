---
forge_version: v5
idea: 009
scope: full
convergence_mode: strong-converge
prefill_source: proposals.md§009
x_hash: ccdb41620268a187d348e72aad47e260
created: 2026-07-16T00:00:00Z
trigger: operator-input 2026-07-16 · 分析师不荐股/信号隐性 · smoke path(07-07 决议)前提被推翻 · 路线图倒转候选
---

# Forge v5 · 009 · 隐性信号事实修正后的路线重排:提取/蒸馏头该不该提前、怎么切

## scope 说明 · full forge

这**不是** forge-lite。v5 的触发是**事实修正级**的:operator 亲述该分析师不产显性荐股
call,M2 alpha 头的输入假设("存在显性 (ticker,direction,date) 信号")对该数据源永久
不成立,07-07 smoke path 决议前提作废。原 v1/v2 把"蒸馏"排 M4 最末且 gated,operator
真实需求把它提前到任何评估之前的关键路径 = 路线图倒转 = 重大架构转向 → 按宪法走全量
forge(P1 独立审 → P2 SOTA 对标 → P3 收敛)。

## X · 审阅标的(8 个)

1. **proposal §009**:`proposals/proposals.md` 行 276 起(到 EOF)—— idea 核心文本
   (想法/第一性原理/闭环灵魂/四条核心工作/已 build 资产/诉求)。[proposal-section]
2. **v5 触发材料(最高优先)**:`discussion/009/operator-input-2026-07-16-implicit-signals.md`
   —— operator 亲述事实修正 + 008 语料核查 + 给 v5 的 6 个待裁问题。[internal ✅]
3. **现 PRD**:`discussion/009/009-pForge/PRD.md`(phased M1/M2 · fork 已 complete)——
   重排 M3' 必须以其 IN/OUT 边界为基线。[internal ✅]
4. **决议日志**:`discussion/009/handback/HANDBACK-LOG.md`(21 决议 · 重点:07-07
   P2-prod-precondition-gap 被本轮 supersede 的决议 1 + M-fork-complete 收尾)。[internal ✅]
5. **最近 verdict 锚**:`discussion/009/forge/v4/stage-forge-009-v4.md`(O8 非方向
   evidence 上台)。[internal ✅]
6. ⚠ **XenoDev 004-pB 仓**:`/home/ys/codes/XenoDev/projects/004-pB`(alpha 模块在
   `feat/009-spec` 分支;main 工作树看不到 · Codex 沙箱可能 BLOCK 跨仓)。[external]
7. ⚠ **008 语料库**:`/home/ys/codes/XenoDev/out/collection.db`(9,081 条 · 二进制 ·
   跨仓)。[external]
8. **跨仓快照件(6/7 的沙箱替代读物)**:`discussion/009/forge/v5/xenodev-alpha-assets-snapshot.md`
   —— alpha 模块契约摘录(join 七类拒绝/双 as_of/evaluate CLI/三表 DDL)+ collection.db
   schema/规模实测。**Codex 读不到 6/7 时以本件为准**。[internal ✅]

## Y · 审阅视角(3)

- **产品价值** — "从隐性信息提取疑似信号→回测检验→蒸馏分析套路"这条链对 operator
  (不懂投资、想借工程强项补短板)是不是真值得建?相比"直接自建公开数据信号"的对照路径,
  分析师隐性信息的边际价值假设是什么、怎么尽早证伪?
- **架构设计** — 提取头放在闭环哪个位置、和 008(采集)/M2(评估机器)/004(纪律壳)的
  边界怎么切;M3' 与原 M3(calibration 头/回流线)/M4(图谱/蒸馏)怎么重排;
  "疑似信号"的产物 schema 与 M2 join 的对接方式。
- **工程纪律** — 两条候选红线怎么钉死:①提取规则/prompt 每个变体计入 DSR/PBO
  trial_count(防在噪声里调提取直到回测好看);②文本侧 PIT 纪律(提取只能用
  published_at 早于信号时点的内容)。以及先导实验的验收口径(anti-PPV:终点是真数字/
  真拒绝行,非"提取器跑通")。

## Z · 参照系

- mode: **对标 SOTA**
- 检索方向(binding 建议,双方各自跑 ≥3 次):
  a. LLM/NLP 从非结构化文本(新闻/研报/社交媒体/播客转写)提取交易信号的既有做法与
     失败案例(如 news sentiment alpha、event-driven 策略的 point-in-time 文本处理);
  b. "分析师/KOL 观点可信度评估"的 prior art(TipRanks 类是 v1 已知锚,v5 重点在
     **隐性观点**怎么显性化的先例);
  c. 文本→信号研究中的多重检验/数据窥探陷阱与对策(和 Bailey-LdP DSR/PBO 的衔接)。

## W · 产出形态(5)

- **verdict-only** ✅(单一 verdict + rationale)
- **decision-list** ✅(保留/调整/删除/新增矩阵 —— 至少覆盖:蒸馏头提前与否、M3' scope、
  07-07 决议处置、两条红线、008→004 桥归属、原 M3/M4 内容重排)
- **next-PRD** ✅(M3' 的 PRD 草案,可 fork 进 L4)
- **refactor-plan** ✅(哪些既有器官动/不动:008 采集面、M2 join 契约、conflict_report
  台面 —— 按模块分组)
- **next-dev-plan** ✅(分期计划:先导实验 → M3' 正式 build 的 milestone 切分)

## K · 用户判准(binding · prefill verbatim)

// from "想法":
把 004(决策账本/承诺壳)、008(投顾内容采集)、以及「验证分析师 alpha + 回测 + 信号蒸馏」四条想法,合成一个**完整投资决策闭环产品**:信息收集 → 结构化/知识 → 信号/策略构建 → 决策 → 纪律执行 → 复盘 → 反馈回信息。004/008 不是被替代,而是重定位为这个闭环的子系统/阶段。

// from "我为什么想做这个"(第一性原理):
我懂算法、自动化、数据,但**不懂投资,没有专业知识和经验**。这个产品的本质 = **用我的工程强项,补齐我的投资 domain 短板**。各器官按"补哪个短板"定位:
- 投资知识/背景/纪律 ← 外部专家(微信投顾)的内容,008 采集+结构化沉淀
- 策略能力 ← 外部信号 + 我自己内测的回测系统(用算法强项做)
- "这个分析师到底行不行" ← 回测数据说话(alpha/beta),是闭环的验证地基
- 执行不走样 ← 严格纪律执行(防我这个不懂投资的人临场乱动),004 承诺壳

// from "闭环的灵魂(已定 · 关键)":
"承诺壳"(防乱动)与"alpha 引擎"(验证/信号/策略)**不冲突,永久共存,分居上下游**:
- alpha 引擎在**上游**回答「该信什么、用什么策略」(补知识/策略短板)
- 承诺壳(004)在**下游**保证「信了之后执行不走样」(补纪律短板)
- 回测数据只是决定「上游信号给多强、下游纪律卡多严」的旋钮,不是二选一。

// from "我已经想过的角度"(四条核心工作 · 非路径文字部分):
1. **验证投资分析师的 alpha**:他的分析判断到底多准?不要求 100%,但要能 beat 80-90% 的一般分析师才够价值。我对他目前只有片面主观印象(正统从业经历 / 部分可信消息网络 / 投资 philosophy 我认同 / 按他说的年初买存储股实打实赚过)。我没有足够投资经验,所以**需要建一个回测系统**测他是否可信、是否可作为关键参考和信号。
2. **构建完备回测系统**:结合分析师的消息/判断 + 其他 signal,制定更好的策略/决策。
3. **时序异质图谱(待 forge 评估)**:股票/公司为节点,事件为异质节点,公司业务关联为边,每个时间点形成一张异质图谱,不同时间点不同图谱 —— 是否能更全面覆盖股市动态?
4. **蒸馏分析师技能**:若他大部分靠谱,下一步"蒸馏"他的技能 —— 他如何分析大盘/盘前盘后。哪些靠他**私域 source**、哪些靠公开数据/事件/财报(需更强信息监测能力)就能分析。技能层面保证**自给自足**(保底独立运转),私域消息再试图扩充渠道。

// from "已 build 可复用资产"(非路径文字部分 · 路径已转 X 候选):
004 已 ship 出"信号引擎"半个骨架(被承诺壳哲学包着、压在 v1.0 未释放):StrategyModule 协议 IDL(source_id+analyze→StrategySignal,锁死"多信号源不合并")/ 真 XGBoost 信号 lane / 信号源相关性<0.5 去重 / 分析师内容已建模成带 structured_json 的信号源 / 13 个 alembic migration。008 = 闭环输入端(图文/回放/预警采集,v0.1/v0.2 已 ship + forge v4 定了信号 spike 前置)。

// from "我的诉求":
我希望两位专家审定:① 闭环整体架构怎么搭;② 004/008 怎么并入(哪些复用、哪些重构、哲学边界怎么划清——上游 alpha 层 vs 下游 004 纪律红线 #1/#9);③ 四条想法怎么排期(尤其时序图谱该不该现在上、回测系统怎么作为两灵魂的公共地基先落地);④ 这个集合体相对"分散的 004+008"是否真有架构级价值,还是会变成又一个 V4 式的过度设计。

// [v5 特有 · from operator-input-2026-07-16-implicit-signals.md 事实修正]:
该分析师**不产显性荐股 call**;信号只以**隐性形态**存在(盘前/盘中/盘后笔记里零散关键信息披露、直播里展望/预警、只言片语甚至暗示)。M2 alpha 头输入假设"存在显性 (ticker,direction,date) 信号"对该数据源**永久不成立**。GAP-1 从"缺 008→004 backfill 搬运桥"升级为"缺**信号提取/蒸馏头**":008 内容库 → 从笔记/直播转写提取"疑似信号"并显性化(ticker/方向/时间/出处/置信)→ 才能进 M2 评估机器。原 forge v1/v2 把"蒸馏"排在 M4 最末且 gated,operator 真实需求把它**提前到任何评估之前的关键路径** = 路线图倒转 = 重大架构转向,按宪法必须走 forge 裁决。评估问题从"这个分析师行不行"变为"分析师隐性信息 × 提取方法"的联合假设 —— 009 实际要造的是"学会他怎么看盘"的解读器,回测是解读器的考官。
