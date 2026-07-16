# Forge Stage · 009 · v5 · "隐性信号事实修正:提取头提前成 M3'·最小证伪链"

**Generated**: 2026-07-16T21:30:00Z
**Source**: full forge run v5 · X = 8 标的(6 真读 + 2 跨仓靠快照件), Y = 产品价值 + 架构设计 + 工程纪律, Z = 对标 SOTA, W = verdict-only + decision-list + next-PRD + refactor-plan + next-dev-plan(五件套全勾)
**Convergence mode**: strong-converge
**Rounds completed**: P1 (both · Opus 4.8 Max + GPT-5.5 xHigh) · P2 (both) · P3R1 (both) · P3R2 (both)
**Searches run**: 15 across ≥6 distinct sources(Opus 4 + GPT 11 · 覆盖 parametric look-ahead / 文本→信号 prior art / pundit 评分先例 / gold-standard 标注 / PBO-DSR 原始文献)
**Moderator injections honored**: none
**Convergence outcome**: converged(单一 verdict · P3R2 双方 §2 对齐 · GPT §2 显式背书 Opus §2 · 无 unresolved · 无 BLOCK 残留:GPT R1 的 BLOCK 条件在 R2 已解除)

---

## How to read this

forge 是横切层(不在 L1-L4 pipeline 内)。本文档是双专家独立审(P1)+ SOTA 对标(P2)+ 两轮联合
收敛(P3R1/R2)后的**单一 verdict**(strong-converge · 不列并行 path)。它把 v5 的事实修正级触发
——"该分析师不产显性荐股 call、信号只以隐性形态存在"——落成一条可执行的路线重排。

读完你应该:
- 知道双专家最终 verdict:提取头**提前成立**(定名 M3'),但形态是**最小证伪链**而非一次性 build
- 逐条溯源支持每条结论的证据(§Evidence map)
- 拿到五件套可执行草案:§Decision list(保留/调整/删除/新增矩阵)· §Next-version PRD draft(M3'
  骨架 · 可直接 fork 进 L4)· §Refactor plan(哪些器官动/不动)· §Next-version dev plan(E0→E3 分期)
- 能基于 §Decision menu 直接进下一步([A] fork PRD 进 L4 / [B] 跑 v6 / [C] 局部接受 / [P] park / [Z] abandon)

**一句话 verdict**:009 实际要造的不是"给分析师打分的评分器",而是"学会他怎么看盘的解读器";
M3'(信号提取头)是 008 语料与 M2 评估机器之间缺失的**可审计器官**,以带停止条件的证伪链推进,
历史窗只算开发证据、forward 线才是 alpha 唯一确证路径。

---

## Verdict

**M3'(信号提取头)提前成立,以"最小证伪链"形态推进;它是 008 语料与 M2 评估机器之间缺失的
可审计器官,008→004 通用搬运桥不另设,07-07 smoke path 决议正式 supersede。**

证伪链五站(每站带停止条件,fail = 诚实停止,提取头产物仍为可复用资产):**E0 口径**(定义"一条
可评估疑似信号"·vague→typed rejection·预注册密度阈值)→ **E1 普查+两层金标**(语料密度普查 +
span 抽取验收 + 可交易映射验收,两层全过才进回测)→ **E2 历史窗先导**(证据地位 = 开发证据:
口径/提取器校准、failure 分类、power analysis)→ **E3 forward 确证线**(采集-即提取-封存-事后对账,
唯一 alpha 确证路径,常设化)。评估叙事 = 硬币基线起跑、检验分析师是否是例外、不因公开 pundit
均值差预判生死。M1/M2/004 零改动;蒸馏技能("学会他怎么想")与时序图谱维持远期 OUT。

**回应 K**:① "工程强项补投资短板"→提取头+证伪链+统计纪律全是工程强项的发挥面;② "两灵魂分居
上下游、004 纪律壳不动"→全部动作在上游信号层,004/M2 评估端零改动;③ 四条核心工作排期→验证分析师
现依赖提取头(联合假设已设拆账机制)、回测系统 M1/M2 照用、图谱维持 defer、蒸馏拆分为"提取头提前 +
技能蒸馏远期";④ "防 V4"→提取头钉死"只显性化他说了什么,不学他怎么想"的 OUT 条款 + 每站带停止
条件;⑤ v5 事实修正(隐性信息 × 提取方法联合假设)→升格为三条 BLOCK 级红线 + 两级证据制。

---

## Evidence map

| 结论 | 来源 | 引用(≤15 words) | 是否有反对证据 |
|---|---|---|---|
| 缺的不是搬运桥,是提取头 | P1-Opus §1 + P1-GPT §1 | "缺口位于 008 内容与 M2 join 之间,不是 004 下游展示层" | - 双方独立收敛 |
| M1/M2 量尺资产全 keep(与信号来源无关) | P1-Opus §2 + P1-GPT §2 | "量尺与信号来源无关;743 passed 的既有资产" | - 双方一致 |
| 07-07 smoke path 正式 cut(前提证伪) | P1-Opus §2 + P1-GPT §2 + forge-config 触发 | "前提(显性 call 存在)被 operator 亲述证伪" | - operator 亲述 + 双方一致 |
| 提取头 vs 蒸馏技能必须切开(防 V4) | P1-Opus §1/§2 | "提前的应该只是提取头,不是蒸馏技能" | - 双方 + P3R1 §4 唯一警示项 |
| LLM parametric look-ahead 不可识别 → 历史窗降级 | P2-Opus §1 row1 + P2-GPT §1 row4 | "若模型记住了结果,预测能力不可识别" | - SOTA 双侧背书(FinCAD 论文) |
| forward 线为 alpha 唯一确证路径 | P2-Opus §3 + P3R1-Opus §2 | "forward 评估线成为 alpha 确证的主路径" | - P3R2 双方闭合(历史窗=开发证据) |
| 提取器变体×口径×horizon 计入 trial_count | operator-input + P1 双方 + P2-GPT §1 row3 | "每个 prompt、规则、标签口径、horizon 都要进 trial ledger" | - SOTA(Bailey-LdP)加固为硬红线 |
| 文本 PIT(只用 published_at ≤ 信号时点) | operator-input + P1 双方 | "文本 published_at PIT" | - collection.db 时间戳支持 |
| 引文锚定 + 提取稳定性(温度 0/版本化) | P1-Opus §1 + P2-Opus §1 row2 | "同文本多次运行一致性检查" | - SOTA 加的第三个泄漏面 |
| 金标拆两层(span 抽取 + 可交易映射) | P3R1-GPT 分歧3 → P3R2-Opus §1 | "两层全过才许进回测" | - R2 双方全盘接受(R1 最有价值精化) |
| 公开 pundit 基线 = 硬币 · operator 体感归零 | P2-Opus §1 row3(CXO Guru Grades) | "公开 pundit 平均 = 硬币" | ⚠ P3R1-GPT 分歧2:基线是起跑线非判决书(见 §underweights) |
| vague→exclude 是行规(有直接先例) | P2-Opus §1 row3(CXO) | "太模糊无法评分的预测直接排除" | - 非我们发明 |
| 疑似信号落 009 自有表(不写 004 三表) | P1-Opus §1/§3 + P3R2-Opus §4 | "落 009 自有表倾向,不污染 004 生产表" | ⚠ Opus P1 §3 列为未量化改动量(见 §underweights) |
| EQM 解释质量评分收为可选旁支 | P3R1-Opus §3 分歧3 → P3R2 双方 §3 | "更擅长识别低质量判断者" | - GPT R1 提"可先评估",R2 未再争 |
| record_tickers 语义 E1 普查站查明 | P1 双方 §3 + P3R2 §3 | "复用、校验还是完全重建 ticker 解析" | - 双方均列为不确定,降级 v0.2 |

(15 行 · 已挑最 load-bearing;3 处 ⚠ 反对/未定证据在 §underweights 展开)

---

## Intake recap

### X · 审阅标的(8 个 · 6 真读 + 2 跨仓靠快照件)
1. **proposal §009**(proposals.md:276-EOF · proposal-section)— 双方真读
2. **v5 触发材料**(operator-input-2026-07-16-implicit-signals.md · internal ✅)— 双方真读
3. **现 PRD**(009-pForge/PRD.md · phased M1/M2 · internal ✅)— 双方真读
4. **决议日志**(HANDBACK-LOG.md · 21 决议 · internal ✅)— 双方精读 07-06 M-fork-complete + 07-07 P2-prod-precondition-gap
5. **最近 verdict 锚**(stage-forge-009-v4.md · O8 非方向 evidence · internal ✅)— 双方真读
6. ⚠ **XenoDev 004-pB 仓**(alpha 模块 feat/009-spec 分支 · external)— Opus 真读(join.py/evaluate/realized_return + alembic DDL);GPT 沙箱 BLOCK,靠快照件
7. ⚠ **008 语料库**(collection.db · 9,081 条 · external)— Opus sqlite3 实测 schema+分布;GPT 沙箱 BLOCK,靠快照件
8. **跨仓快照件**(xenodev-alpha-assets-snapshot.md · internal ✅)— 6/7 沙箱替代读物,双方均读

### Y · 审阅视角(3)
- **产品价值** — 隐性信息提取→回测→蒸馏这条链对 operator 是否真值得建;隐性信息边际价值假设怎么尽早证伪
- **架构设计** — 提取头放闭环哪个位置;和 008/M2/004 边界怎么切;M3' 与原 M3/M4 重排;疑似信号 schema 与 M2 join 对接
- **工程纪律** — 两条红线(提取器变体入 trial_count / 文本侧 PIT)+ anti-PPV 验收口径(终点是真数字/真拒绝行)

### Z · 参照系
- mode: **对标 SOTA**
- 检索方向:文本→交易信号既有做法与失败案例 / 分析师-KOL 观点可信度评估 prior art / 文本→信号的多重检验陷阱与 DSR-PBO 衔接
- 用户外部材料: 无(K 中无外部链接,P2 双方均记"无需消化项")

### W · 产出形态(5 · 全勾)
verdict-only ✅ · decision-list ✅ · next-PRD ✅ · refactor-plan ✅ · next-dev-plan ✅
(交叉验证:以下五个 W-shape 章节全部齐整出现)

### K · 用户判准(binding · prefill verbatim 摘要)
把 004/008/alpha 回测/信号蒸馏合成完整投资决策闭环(004/008 不被替代,重定位为子系统);第一性原理 =
用工程强项补投资 domain 短板;两灵魂分居上下游(alpha 引擎上游回答"该信什么"、004 承诺壳下游保证
"执行不走样",不冲突永久共存);四条核心工作(验证分析师 alpha / 完备回测系统 / 时序异质图谱待评估 /
蒸馏分析师技能);诉求 = 审定闭环整体架构、004/008 怎么并入、四条想法怎么排期、集合体是否真有架构级
价值还是又一个 V4 式过度设计。**v5 特有事实修正**:分析师不产显性荐股 call,信号只以隐性形态存在;
M2 输入假设"存在显性 (ticker,direction,date) 信号"永久不成立;GAP-1 从"缺搬运桥"升级为"缺信号
提取/蒸馏头";评估问题从"这个分析师行不行"变为"分析师隐性信息 × 提取方法"的联合假设。

### 收敛模式
strong-converge → 单一 verdict(P3R2 双方 §2 对齐 · GPT 显式背书 Opus · 无 unresolved)

---

## §Verdict rationale(W: verdict-only)

三条论证支柱,均可在 §Evidence map 溯源:

**支柱一 · 为什么提前不是路线膨胀,而是补缺失器官**。原 PRD 把"蒸馏 lane"放 M4 OUT,前提是 M2
能先吃到显性信号。该前提被 operator 亲述证伪(不产显性 call)→ M2 评估机器"没有输入"。SOTA
(Lopez-Lira/Tang,arXiv 2304.07619)证明 LLM 确能从文本抽取增量信号,前提是把 published_at 和
交易可得性作文本 PIT。所以提取头不是新愿望,是让既有 743-passed 评估机器取得输入的**前置器官**——
提前它是补缺,不是加 scope。防 V4 的关键是切开"提取头(显性化他说了什么)"与"蒸馏技能(学会他
怎么想)":前者提前进 M3',后者维持远期 OUT。

**支柱二 · 为什么必须是证伪链而非一次性 build**。评估问题变成"隐性信息 × 提取方法"的联合假设 →
回测差时无法区分"分析师无 alpha"与"提取方法烂"(P1 双方各自的第一不确定点)。唯一拆账手段是给
每一站设停止条件:E0 定不出可评估口径就停;E1 密度不足(预注册阈值)或金标不过就停,不谈回测;
E2/E3 分级证据。CXO Guru Grades(2005-2012,68 位专家 6,584 条预测)给了"vague→exclude"的行规
先例和"公开 pundit 平均 = 硬币"的基线——operator 体感归零、从硬币基线起跑,但基线是起跑线不是
判决书(不因均值差提前杀实验)。

**支柱三 · 为什么历史窗只算开发证据、forward 才是确证**。这是 v5 相对 v1-v4 的结构性新知:
parametric look-ahead bias 已是命名问题(FinCAD 2026,arXiv 2605.24564)——模型权重内嵌训练窗内
未来知识,数据管道审计不可见;"若模型记住了结果,预测能力不可识别"。009 语料 2025-06→2026-07,
尾段已在多数模型 cutoff 之后,未来增量语料天然干净 → 架构上把 forward 线设为主证据线(采集-即
提取-封存-事后对账),历史窗降为开发/校准。这条把"回测提取信号"从方法论存疑变为可执行。

---

## §Decision matrix(W: decision-list)

| 类别 | 项 | 来源(标的的具体位置) | 理由 | 优先级 |
|---|---|---|---|---|
| **保留** | M1 PIT 层 + M2 统计机器(realized/DSR/PBO) | 009-pForge/PRD §M1/M2 · XenoDev alpha 模块 | 量尺与信号来源无关 · 743 passed | P0 |
| **保留** | M2 join"歧义一律拒绝"哲学 + 七类拒绝 | join.py(feat/009-spec) | 评估端严格性不因上游模糊放松 | P0 |
| **保留** | O8 非方向 evidence 台面(forge v4 verdict) | stage-forge-009-v4.md | 与提取头正交 · 已定契约不动 | P0 |
| **保留** | 004 承诺壳 / 纪律红线 #1/#9 | XenoDev 004-pB | 两灵魂分居下游 · 零改动 | P0 |
| **保留** | 008 采集面(records / published_at / raw_ref) | collection.db | 只读消费 · 采集端零动 | P0 |
| **调整** | 原 M4 蒸馏排期 → 拆:提取头提前 M3'、技能蒸馏留远期 | 现 PRD M4 OUT | 提取头是前置器官 · 蒸馏技能防 V4 留 OUT | P0 |
| **调整** | 评估叙事 → "检验私域分析师是否是例外" | K + CXO 基线(P2-Opus) | 体感归零 · 硬币基线起跑 · 不预判生死 | P1 |
| **调整** | 金标验收 → 两层制(span 抽取 + 可交易映射) | P3R2-Opus §1 | 单层 span 漏映射误差(sector/ticker/方向/horizon) | P0 |
| **调整** | 历史窗证据地位 → "开发证据"定岗 | P2-Opus §3 + P3R2 双方 | parametric look-ahead 不可识别 | P0 |
| **删除** | 07-07 smoke path 决议(手工回忆显性 call) | HANDBACK-LOG 07-07 · forge-config 触发 | 前提(显性 call)被 operator 亲述证伪 | P0 |
| **删除** | 独立 008→004 通用搬运桥(07-07 留白) | operator-input GAP-1 | 提取头即是桥的正确形态 · 不另设机械搬运层 | P0 |
| **新增** | 提取头器官(008 语料→疑似信号显性化) | (无 · M3' 核心) | operator 真需求的入口 | P0 |
| **新增** | 证伪链 E0-E3(每站带停止条件) | (无 · P3R1/R2 收敛) | 唯一联合假设拆账手段 | P0 |
| **新增** | 三条 BLOCK 级红线(trial ledger 扩 / 文本 PIT / 引文锚定+稳定性) | operator-input + SOTA 加固 | 防噪声调参 / 防 look-ahead / 防聚合不稳定 | P0 |
| **新增** | forward 采集-封存-对账线(常设化) | P2-Opus §3(不可识别性) | alpha 唯一确证路径 | P0 |
| **新增** | 提取层 rejection taxonomy(对齐 join 七类) | P1 双方独立提出 + CXO 行规 | vague→typed rejection 不 best-effort 猜 | P0 |
| **新增** | 提取质量金标验收(两层) | P1-Opus §2 + P2-Opus §1 row4 | 分离联合假设唯一机制 | P0 |

每行可在 §Evidence map 溯源。组合逻辑:E0-E3 证伪链把"新增"的提取头器官串成带停止条件的最小路径,
三条红线是每站的硬约束,历史窗/forward 两级证据制决定每站产出的证据地位。

---

## §Refactor plan(W: refactor-plan · 哪些器官动/不动)

### 模块 A · 008 采集面(collection.db records)
- **当前问题**:无(采集端完整)。records 有 published_at/captured_at/raw_ref/form,replay 已转写。
- **目标态**:只读消费源,采集端零改动。
- **改造步骤**:(无写操作)提取头以只读方式消费 records;published_at 成为文本侧 PIT 轴。
- **风险**:采集若未来改 schema 需通知提取头(松耦合契约面)。
- **预估代价**:S(只读适配 · 不改采集代码)

### 模块 B · collection.db record_tickers 语义查明
- **当前问题**:record_tickers 表(777 行 · 快照件实测)语义未裁——采集侧弱关联 / 标题命中 / 已消歧候选?(P1 双方 §3 共同不确定点)
- **目标态**:E1 普查站顺带查明,据此定提取头 ticker 解析的复用/校验/重建三选一。
- **改造步骤**:E1 站抽样审 record_tickers 与原文对应关系 → 判定语义 → 决定是否复用。
- **风险**:误信脏数据(若是弱关联却当已消歧用)。
- **预估代价**:S(查明属 E1 普查一部分 · 三选一结果留实现)

### 模块 C · 009 新增三表(提取头自有物化面)
- **当前问题**:疑似信号无落脚表;若伪造 004 三表兼容行会污染其语义、撞 UNIQUE(week_id,source_id)(P1-Opus §1)。
- **目标态**:009 自有表,不写 004 生产三表。
- **改造步骤**:建 `extracted_signals`(ticker/方向/时点=published_at/出处引文/置信/提取器版本/口径版本)+ `extraction_rejections`(typed rejection · 对齐 join 七类精神)+ `trial_ledger`(提取器变体×口径×horizon)。
- **风险**:schema 要素若漏"口径版本"→ trial 记账数不清(与红线①冲突)。
- **预估代价**:M(三表 DDL + adapter · 属 M3' 核心)

### 模块 D · M2 join(加第二输入源 adapter)
- **当前问题**:resolve_signals 绑死 004 三表;无 strategy_signals 行整条落 no_signal_date 拒(P1-Opus §1)。
- **目标态**:经 adapter 接入提取头产物,七类拒绝契约不松。
- **改造步骤**:join 层加第二输入源 adapter(读 extracted_signals)· 疑似信号走 adapter 物化成 join 能吃的形态 · 七类拒绝精神延伸到提取层。
- **风险**:evaluate 读 004 表的语义假设深度未量化(Opus P1 §3 未验改动量)→ adapter 改动量须先 grep 界定。
- **预估代价**:M(adapter + 契约测试 · join.py 是 009 fork 自有物可改)

### 模块 E · 004 承诺壳
- **当前问题**:无。
- **目标态**:零改动(两灵魂分居下游 · K binding②)。
- **改造步骤**:(无)
- **风险**:无(全部动作在上游信号层)
- **预估代价**:零

---

## §Next-version PRD draft(W: next-PRD · 可 fork 进 L4 的骨架)

```
# PRD · <009-pForge-M3prime · 待 operator 定 fork-id> · "M3' 信号提取头 · 最小证伪链"

**Status**: Draft from forge v5, awaiting human approval
**PRD-form**: phased
**Phases**: [E0+E1(口径/普查/金标), E2(历史窗先导), E3(forward 确证线)]
**Phase-current**: E0
**Source**: forge stage-forge-009-v5.md + xenodev-alpha-assets-snapshot.md

## User persona
单人自用 operator(引用 K):懂算法/自动化/数据,不懂投资、无专业投资经验。009 实际要造
"学会他怎么看盘"的解读器,回测是解读器的考官。

## Core user stories
- 作为不懂投资的 operator,我要把分析师笔记/直播里的隐性信息**显性化成可评估疑似信号**
  (ticker/方向/时点/出处/置信),否则我的评估机器没有输入。
- 作为容易自欺的 operator,我要提取器**先过金标验收再谈回测**,这样回测差时能区分是"分析师
  无 alpha"还是"提取方法烂"。
- 作为要诚实的 operator,我要 alpha 确证走 **forward 线**(内容到达即提取封存事后对账),不被
  LLM 权重里的后见之明骗。

## Scope IN
- E0 口径:定义"一条可评估疑似信号" · vague→typed rejection · 预注册密度阈值
- E1 普查+两层金标:语料密度普查 + span 抽取验收 + 可交易映射验收(两层全过才进回测)
- E2 历史窗先导:证据地位=开发证据(口径/提取器校准、failure 分类、power analysis)
- E3 forward 确证线:采集-即提取-封存-事后对账(唯一 alpha 确证路径)· 常设化
- 疑似信号 schema 要素:ticker / 方向 / 时点(published_at)/ 出处引文 / 置信 / 提取器版本 / 口径版本
- 物化路径:009 自有表(extracted_signals + extraction_rejections + trial_ledger)· 经 adapter 进 M2 join
- 提取层 rejection taxonomy(对齐 join 七类拒绝精神)

## Scope OUT(显式 non-goals · 每条引用 §Evidence map)
- 蒸馏技能("学会他怎么想")→ 远期 OUT(防 V4 · 见 §Evidence map "提取头 vs 蒸馏技能必须切开")
- 时序异质图谱 → 维持 defer(K 四条工作③ · 待评估)
- 自动交易 / 改 004 纪律壳 → OUT(两灵魂分居下游 · K binding②)
- 改 M2 评估端语义 → OUT(量尺 keep · 见 §Evidence map "M1/M2 量尺资产全 keep")
- 写 004 生产三表 → OUT(不污染语义 / 不撞 UNIQUE · 见 §Refactor plan 模块 C)

## Success looks like(可观测 · 引用 K)
- E1 出真数字:语料能提出的带 (ticker,方向,时点) 疑似信号密度 ≥ 预注册阈值 且金标两层全过
- 终点是真接受/拒绝行 + 真回测数字(anti-PPV),不是"提取器跑通"
- alpha 数字诚实:记 trial-count + DSR/PBO deflate + 硬币基线对照

## Real constraints(从 K 摘)
- 单人自用不商业化 · operator 不懂投资(需工程强项补短板)
- 语料 2025-06→2026-07(9,081 条 · 尾段已在多数模型 cutoff 后)
- 跨仓:M3' 落 XenoDev build runtime · IDS 只产 hand-off

## UX principles
- 疑似信号必须附原文出处(引文锚定 · operator 可复核)
- 评估叙事="检验私域分析师是否是例外" · 不默认 alpha 也不因均值差杀实验

## BLOCK 级硬约束(§8 契约测试须覆盖)
- ① trial ledger 扩到提取器变体×口径版本×horizon · 全部进 DSR/PBO deflate
- ② 文本 PIT:提取只可用 published_at ≤ 信号时点的内容(负例测试)
- ③ 引文锚定断言 + 提取稳定性(温度 0 / 版本化 / 同文本同输出)
- ④ 两级证据制 + 两层金标 gate(未过金标不得进回测 · mutation-killer)

## Open questions(forge 也没解决的 · 见 §残余降级 v0.2 note)
- 金标两层具体数值门槛(α 精确值 / 映射一致率 / P/R 下限)
- record_tickers 语义(复用/校验/重建三选一)
- 密度"够/不够"的数值线(预注册原则定死 · 具体数 operator 拍)
- EQM 解释质量评分是否升为主链(当前定可选旁支)
```

---

## §Next-version dev plan(W: next-dev-plan · E0→E3 分期)

### Phase E0 · 口径预注册(预估 S · 1 站)
- 目标:定义"一条可评估疑似信号"的粗口径 + 预注册密度阈值
- 关键 milestone:
  - M1: 口径文档(什么算 ticker/方向/horizon/时点 · vague→typed rejection 规则)
  - M2: 预注册密度阈值(普查前先写下"多少条算够")+ rejection taxonomy 草案
- 依赖:无(链起点)
- 停止条件:定不出可审计口径 → 停,回 L2 重估闭环前提
- 风险:同一句"看好主线"落 sector vs ticker vs 方向 vs 置信区间会改回测结论(P1-GPT §3.1)

### Phase E1 · 密度普查 + 两层金标(预估 M · 首要 ROI 站)
- 目标:普查语料密度 + 提取器过两层金标才放行回测
- 关键 milestone:
  - M1: 语料密度普查数字(能提多少条候选 · 与 E0 阈值比)· 顺带查明 record_tickers 语义
  - M2: 层 1 span 抽取验收(α≥0.667 + span P/R/F1)
  - M3: 层 2 可交易映射验收(sector/ticker/方向/horizon/时点映射一致率)
  - M4: 两层全过 gate(operator 参与标注但不单独终审 · 需第二标注源+分歧仲裁)
- 依赖:E0 口径
- 停止条件:密度 < 预注册阈值 → 停(回 insufficient_sample);金标任一层不过 → 停,不谈回测
- 风险:联合假设拆账(回测差可能来自分析师/提取器/样本/噪声/horizon)→ 金标是拆账机制(P1-GPT §3.3)

### Phase E2 · 历史窗先导(预估 M · 证据地位=开发证据)
- 目标:历史窗做口径/提取器校准、failure case 分类、power analysis
- 关键 milestone:
  - M1: 历史窗先导回测(证据地位=开发证据 · 不背书 alpha)
  - M2: failure case 分类 + power analysis(样本量够不够让 DSR 显著)
- 依赖:E1 金标过关
- 停止条件:power analysis 显示样本永远不足以显著 → 回 L2 重估
- 风险:operator 记忆中的存储主线窗口仅作 OOS sanity check,开发/调参用其他时段(P1-Opus §1)

### Phase E3 · forward 确证线常设化(预估 L · 唯一 alpha 确证路径)
- 目标:采集-即提取-封存-事后对账机制常设化
- 关键 milestone:
  - M1: "内容到达即提取封存"调度钩子(零权重泄漏)
  - M2: 事后对答案对账线 + trial ledger 汇入 DSR/PBO deflate
  - M3: 硬币基线对照 → 检验分析师是否是例外(不预判生死)
- 依赖:E2 校准过的提取器
- 停止条件:forward 累积够样本后 DSR/PBO 不显著 → 诚实结论"该分析师非例外"(提取头仍为资产)
- 风险:forward 需时间累积样本(慢证据) · look-ahead 已被 forward 结构性消除

**注**:E0-E3 全在 XenoDev build runtime 落地(跨仓 · IDS 只产 hand-off)。不到 spec 级——spec 是 L4 spec-writer 的工作。

---

## §残余降级 v0.2 note(双方 §3 高度一致 · 超出最小契约)

以下降级为实现细节 / 预注册项(双方 P3R2 §3 逐条对齐):

- **EQM 解释质量评分**:收为可选旁支(廉价预筛 + 蒸馏远期素材)· 不进 M3' 主链 · 不作 alpha 证据。
  (GPT R1 提"可先评估其解释质量",R2 未再争 → 若未来 operator 想升主链再起 forge)
- **金标两层具体数值门槛**:原则定死(有门槛 + 两层全过才回测)· α 精确值 / 映射一致率 / P/R 下限
  留 XenoDev 实现**预注册**(先写下再跑)。
- **record_tickers 语义**(复用/校验/重建三选一):E1 普查站顺带查明 · 三选一留实现。
- **密度"够/不够"的数值线**:预注册原则定死(普查前先写下阈值)· 具体数进 PRD 草案由 operator 拍。
- **cutoff 早于语料期的对照模型**:forward 线为主后降为可选加固 · 不作硬要求。

---

## What this menu underweights(强制自批判)

诚实标注本 stage doc 可能 underweight 的点。这是质量栏,不跳过。

- **双模型再次强收敛的回声室风险(最大 underweight)**:v5 全程**零方向分歧**——P1 双方独立收敛、
  P2 SOTA 无一处推翻共识只做加固、P3 三条分歧全是"侧重/保守程度"非方向。这与 v1-v4 **同一模式**
  (四轮 forge 每次都强收敛)。两个模型可能共享同一套 SOTA 直觉(look-ahead / DSR-PBO / 金标),
  在"提取头该提前"这个大方向上互相加强却没人扮真正的反方(如"隐性信号根本提不出足够密度、整个
  M3' 是伪需求、应直接 abandon 转自建公开数据信号")。Y 视角本要求的"相比直接自建公开数据信号的
  对照路径"——双方都默认走提取头,**没认真论证对照路径可能更优**。这条对照假设未被对抗验证。
- **语料密度未实测(E1 前全是推演)**:整个 verdict 的 ROI 锚点是"语料能提出足够多带 (ticker,方向,
  时点) 的疑似信号"——但**没人真读语料正文**(Opus P1 §3.1 明确"我未读语料正文,纯未知")。
  1,179 篇笔记 + 357 场直播能提几百条(M2 统计够用)还是几十条(回 insufficient_sample)是**纯未知**。
  E1 普查数字出来前,"提取头提前成立"这个结论悬在一个未验证的密度假设上。若密度实测很低,verdict
  的 ROI 前提直接塌 → 这是 v6 最可能的触发点。
- **外部标的 6/7 GPT 侧未真读(靠快照件)**:X 标的 6(XenoDev 004-pB)和 7(collection.db)GPT 侧
  被沙箱 BLOCK,只读了 Opus 自产的 xenodev-alpha-assets-snapshot.md。若快照件本身有误(如 join 契约
  摘录不全 / collection.db schema 实测有偏),GPT 的判断建在可能失真的二手材料上。**join.py 改动量、
  evaluate 读 004 表的语义假设深度**(Opus P1 §3.3 明确"未量化")——只有 Opus 真读了源码,GPT 无法
  独立复核,削弱了这部分的双人对抗强度。
- **forge 理论决议 vs build 实证的历史教训**:MEMORY 明确记载——forge/handback-review 的理论技术决议
  **会漏实证盲区**(DB 引擎语义/并发/原子性别信推演要真跑)。009 一周期内已有 **F6 幻影 bug** 和
  **forge two-SELECT 原子性两次被 build-time 杀**的先例。本 verdict 里大量是推演:"金标两层全过就能拆
  联合假设"、"forward 线就能消除 look-ahead"、"trial ledger 扩到提取器变体就防住噪声调参"——这些在
  build-time 真跑前都是假说。**XenoDev 复现测是最后防线**(尤其:提取稳定性"同文本同输出"在真 LLM 上
  是否真成立 / trial 记账在真管线里是否真数得清)。别只信本 doc 推演。
- **Y 视角覆盖盲区**:Y 未含安全/成本。forward 线常设化的**运行成本**(持续 LLM 提取调用)未量化;
  提取 prompt 喂入分析师原文的**注入面**未审(与 v4 §underweights 同类盲区)。
- **K 中未充分回应的关切**:K 诉求④"集合体相对分散的 004+008 是否真有架构级价值,还是又一个 V4"——
  verdict 用"证伪链每站带停止条件 + 提取头/蒸馏切开"防 V4,但**没正面回答"架构级价值"的度量**:
  如果 E1 就停,009 集合体相对"004+008 各自跑"的净增值是什么?这个价值命题在密度实测前无法证实。
- **forge versioning 提示 · 什么会触发 v6**:(a) E1 语料密度普查数字出来且 < 预注册阈值 → verdict 的
  ROI 前提塌;(b) build-time 复现测发现"提取稳定性/trial 记账"推演不成立;(c) operator 决定认真评估
  "直接自建公开数据信号"对照路径;(d) 快照件被证有误。任一 → 记 dogfood-backlog 攒批回起 v6。

---

## Decision menu(for human)

### [A] 接受 verdict 进 L4(需 fork 出 PRD branch)
```
⚠ /plan-start 要求 <prd-fork-id> + 完整 PRD 目录,不能直接吃 forge stage 文档。
⚠ 现有仓库 PRD 都是平铺布局 — discussion/009/<prd-fork-id>/PRD.md(无嵌套)
流程(暂时手工,等待 /fork-from-forge 命令落地):

1. 选一个 prd-fork-id:
   009 现有 fork 是 009-pForge(root=009)→ 建议派生名如 009-pForge-M3prime 或 009-pM3prime
   无论哪种,prd-fork-id 都直接放在 discussion/009/ 下(平铺,不嵌套)

2. 创建 discussion/009/<prd-fork-id>/PRD.md
   - 把本 stage 的 §"Next-version PRD draft" 抽出(已是 phased 骨架 · IN/OUT/BLOCK 约束齐全)
   - 补 frontmatter:PRD-form: phased · Source: forge stage-forge-009-v5.md

3. 创建 discussion/009/<prd-fork-id>/FORK-ORIGIN.md
   说明 forked-from = forge stage v5 · parent = 009-pForge(非 L3 candidate)

4. /plan-start <prd-fork-id> → 产 HANDOFF.md → 新开 XenoDev session 真 build(E0-E3 落 XenoDev)
```
✅ 本 forge W 勾了 next-PRD → §"Next-version PRD draft" 已就绪,可直接抽出 fork。
⚠ 但见 §underweights:E1 语料密度未实测 · 建议 fork 后 E0/E1 先行,把"密度普查"当第一站真跑,
   再决定是否投 E2/E3(证伪链本就是这个用途)。

### [B] 跑 forge v6(说明需要补什么)
```
/expert-forge 009
# 在 Phase 0 intake 时调整 X / Y / Z / W / K
# 旧 v5 整目录保留作历史参考
```
适用:若你要先证伪"对照路径(直接自建公开数据信号)可能更优"这条被双方默认跳过的假设
(§underweights 第一条);或 E1 普查真跑后密度 < 阈值,需重估整个 M3' 前提;或想加安全/成本视角。

### [C] 局部接受
- ✅ 采纳:提取头提前成 M3' · 证伪链 E0-E3 框架 · 三条 BLOCK 红线 · 两级证据制 · 07-07 supersede · M1/M2/004 零动
- ⏸ 挂起:E2/E3 投入(等 E1 密度普查数字 · 见 §underweights)· 金标具体数值门槛(实现预注册)· EQM 是否升主链
- ❌ 拒绝:(留空 · 无建议拒绝项 · 若你认为对照路径更优则走 [B])

### [P] Park
```
/park 009
```
保留所有 forge 产物,标记暂停。复活时不重做这一层。

### [Z] Abandon
```
/abandon 009
```
（不适用 · M3' 提取头是 009 闭环蓝图的兑现项 · 事实修正把它从远期候选提前到关键路径,
非该放弃的方向。列出仅为菜单完整。若 E1 密度实测证明伪需求,那是走 [B] 重估而非直接 abandon。)

---

## Forge log
- v5: 2026-07-16 — verdict: "隐性信号事实修正 → 提取头提前成 M3'(信号提取头)· 最小证伪链 E0(口径)→E1(密度普查+两层金标)→E2(历史窗=开发证据)→E3(forward=唯一 alpha 确证)· 三条 BLOCK 红线(trial ledger 扩/文本 PIT/引文锚定+稳定性)· 07-07 smoke path supersede · 008→004 桥不另设 · M1/M2/004 零动 · 蒸馏技能与图谱留远期 OUT"
- v4: 2026-07-06 — verdict: "O8 下游非方向 evidence:轻扩一等公民(evidence_lanes 旁路)+ 缓存纳 evidence 指纹(R3-F1 硬解)+ Telegram 真改/UI 加分区 · OUT-10 判为授权下游集成 · 拆新 FU-task"
- v3: 2026-07-03 — verdict: "provider 分离双 as_of 轴契约(factor_as_of 分离双轴)· entry 价执行时可见 PIT 严格 · 解 T012 R6 BLOCK"
- v2: — verdict: "七环节闭环蓝图 · PIT 层唯一新器官 · Strangler M1-M4"(已接受 · M1 已 ship)
- v1: — verdict: "集成契约 + 共享回测地基"(已接受)
