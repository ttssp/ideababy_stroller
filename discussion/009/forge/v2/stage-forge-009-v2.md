# Forge Stage · 009 · v2 · "投资决策闭环目标态蓝图 = 七环节契约化闭环图 + Strangler Fig 分期(不推翻 v1)"

**Generated**: 2026-07-01T16:00:00+08:00
**Source**: forge run v2 with X = 5 标的(v1 stage doc 地基 + 004/008 PRD + 004 strategy 层 + ⭐004 alembic 13 migration DB schema), Y = 架构设计/目标态 / 可演化性/分期路线 / 器官边界清晰度 / 工程纪律, Z = 对标 SOTA, W = refactor-plan(目标态模块图)+ free-essay(final goal 全貌)+ next-dev-plan(Strangler Fig 分期路线)
**Convergence mode**: strong-converge
**Rounds completed**: P1 (both), P2 (both), P3R1 (both), P3R2 (both)
**Searches run**: 13 across ~11 distinct sources(量化系统标准分层 data→strategy→backtesting→execution / Strangler Fig Fowler-Azure / PIT 数据 QuantRocket+StarQube+Norgate / QuantConnect Algorithm Framework / HITL 反馈文献 arXiv+ease.ml / TOGAF 两档详略 / 自适应交易系统过拟合)
**Moderator injections honored**: none
**Convergence outcome**: converged(单一 verdict,无 unresolved,全程 0 实质分歧)

---

## How to read this

forge 是横切层(不是 L1-L4 pipeline 的一部分)。**本文档是「画目标态蓝图」专项 forge 的产出,不是重判该不该建。** v1(`discussion/009/forge/v1/stage-forge-009-v1.md`)已定 verdict(009 = 集成契约 + 共享回测地基,非独立统一壳);v2 在其上产**一张目标态架构蓝图**,解决 operator 痛点"现在 004/008/四念头各做各的、缺统一方向、架构设计不够充分彻底"。

**v2 与 v1 的关系**:v1 回答"该不该建、怎么建";v2 回答"最终形态长啥样、怎么分期走到那"。**v2 显式不推翻 v1** —— 蓝图完全建在 v1 松耦合 verdict 上。

读完后你应该:
- 拿到一张**七环节契约化闭环图**(§"Refactor plan" 目标态模块图),一眼看清哪些是已有器官(keep)、哪些要新建(new)、哪些是未来插槽(gated)
- 理解**闭环为什么是"环"不是"链"**(§"Long-form synthesis" 讲透 v1 没画透的反馈回流)
- 拿到**Strangler Fig 分期路线**(§"Next-version dev plan"),每期独立可用、防 V4
- 能基于 §"Decision menu" 直接进入下一步(进 L4 起 PRD / 跑 v3 / 局部接受 / park)

**一句话预警**:蓝图 ≠ 一次性建完的大工程(这是 operator 最怕的 V4)。目标态图指导方向,但**每一期都要能独立跑、独立有价值**。如果你读到任何地方感觉像"要一口气建完才有用",那是理解偏差,请回到 §"Verdict" 与 §"Next-version dev plan" 的"每期独立可用"。

## Verdict

**009 目标态蓝图定稿(不推翻 v1)= 一张七环节契约化闭环图,不是新建的独立统一壳。** 主链:008 采集/结构化 → 回测 PIT 数据层 + alpha 头/calibration 头 → StrategyModule 独立信号 lane → 004 决策/纪律 → calibration 反馈回流。已有器官(008 采集 / 004 承诺壳 / strategy 多 lane / 004 档案半槽含 `would_have_acted_without_agent` + `post_mortem_json`)keep;**唯一关键新器官 = PIT 价格历史层**(日线+复权+PIT ticker+退市感知,defer 多市场/汇率/tick)。分期用 **Strangler Fig**:新回测器官围绕 004/008 生长,M1 数据层→M2 alpha 头(最先出"分析师行不行"数字、最独立可用)→M3 calibration 头 + 两条回流线→M4(gated)图谱/蒸馏,每期独立可用。三条硬约束定稿:① 回流 **human-on-the-loop**(旋钮建议→human 确认后生效;动作/结构/决策权永远手动);② **两档详略**(现建器官画定量契约+AC,未来插槽只画 StrategyModule 签名+gate);③ **回测层 contract tests**。

**回应 K**:此蓝图直接服务 K 第一性原理(工程补投资短板 —— PIT 数据层+复权+DSR/PBO 把"判分析师"变可验证工程,human-on-the-loop 承认 operator 判不了过拟合、让系统建议但人拍板);用 Strangler Fig + 每期独立可用 + 两档详略**三重防 K 最怕的 V4**;严守 K binding①(human-on-the-loop = 系统不得静默改旋钮)。**明确不推翻 v1**,落地路线仍是契约先行、不先建大壳。

## Evidence map

每条 verdict 子结论 → 来源段落(v2 全程 0 实质分歧,故"反对证据"列多为 v0.2 note / 跨 v 提示,非 v2 内部对立):

| 结论 | 来源 | 引用(≤15 words) | 是否有反对证据 |
|---|---|---|---|
| 七环节闭环形态,非统一壳(双方独立读 DB schema 撞同一结论) | P1-Opus §1A / P1-GPT §1A / P2-Opus §1 row 1 | "各做各的靠契约解决非靠大壳" | - |
| 004 已埋反事实字段(v1 AC-1 有 DB 背书) | P1-Opus §1A | "`would_have_acted_without_agent` NOT NULL R2 强制无默认" | - |
| conflict_reports 无 winner 字段 = "永不权威综合分"有 schema enforce | P1-Opus §1C | "数据库层面就 enforce 永不权威综合分" | - |
| 唯一关键新器官 = PIT 价格历史层(advisor_reports 无价格结果列) | P1-Opus §1A / P2-Opus §1 row 3 | "`advisor_reports` 没有 realized-return / 价格结果列" | ⚠ v0.2 note 1:不动基线/反事实窗口粒度未定 |
| 价格层 v0.1 = 日线+复权+PIT ticker+退市,defer 多市场/tick | P2-Opus §1 row 3 / P2-GPT §1 row 3 | "复权和 PIT 不能 defer,否则数字会错" | - |
| 分期 = Strangler Fig(回测器官围绕 004/008 生长) | P2-Opus §1 row 4 / P2-GPT §1 row 2 | "新回测器官 strangle 进现有 004/008 周围" | - |
| 回流 human-on-the-loop(自动回流有过拟合风险,operator 判不了) | P2-Opus §1 row 2 / P2-GPT §1 row 4 | "过拟合风险正是 operator 判不了的" | ⚠ v0.2 note 2:前 K 次是否强制逐次确认 |
| 两档详略(按器官成熟度分档,非二选一) | P2-Opus §1 row 5(TOGAF) / P2-GPT §1 row 5 | "按器官成熟度分详略,不是二选一" | - |
| 回测层需 contract tests(否则契约化器官停留在图上) | P3R1-GPT §3 待固化2 / P3R2 双方 §1 | "回测层需要 contract tests" | - |
| 回流旋钮清单 vs 永远手动清单(旋钮 vs 动作/结构) | P3R1-GPT §3 待固化1 / P3R2-Opus §1 | "旋钮=建议确认可自动;动作/结构/决策权=永远手动" | ⚠ v0.2 note 3:图谱/蒸馏 gate 走 forge v3 还是 L4 |

（v2 无 v1 式"曾是分歧后让步"的行 —— 双方 P1/P2 独立收敛,P3R1/R2 均判 0 分歧,故本表无 v2 内部对立证据;⚠ 均指向 §"What this menu underweights" 的 v0.2 note 与跨 v 提示。）

## Intake recap

### X · 审阅标的(5 个)
- `discussion/009/forge/v1/stage-forge-009-v1.md`(本仓库文件 · forge stage · 339 行)— **核心 X · 蓝图地基**。v2 基于它、不推翻它。
- `discussion/004/004-pB/PRD.md`(本仓库文件 · 237 行)— 004 承诺壳现状(下游纪律器官),红线 #1/#9/#10。
- `discussion/008/008-pB/PRD.md`(本仓库文件 · 315 行)— 008 采集/结构化现状(上游采集器官),008↔004 接口 US6。
- `/home/ys/codes/XenoDev/projects/004-pB/src/decision_ledger/strategy/`(外部 repo · 10 个 .py)— 004 已 ship strategy 层(信号器官)。**双方 v2 P1 均真实读取,无沙箱 BLOCK / 无 fallback**(P1-Opus §0 + P1-GPT §0 均确认 XenoDev 本机可达)。
- ⭐ `/home/ys/codes/XenoDev/projects/004-pB/alembic/versions/`(外部 repo · **13 个 migration** .py)— **v2 新增,补 v1 盲区**。**双方均真实读取**;Opus 一手读了 `0001_initial_schema`(11 张核心表全文)/`0002_tab_open_log`/`0010_extend_advisor_reports`/`0013_add_strategy_xgboost_metadata`,GPT 读了 5 个 migration。此标的是本轮最大信息增量。

### Y · 审阅视角
- 架构设计/目标态(核心)— 闭环最终形态、器官切分、接口契约、数据流
- 可演化性/分期路线(核心)— 分几期走、每期交付啥、gated 条件、每期独立可用
- 器官边界清晰度 — 上游 alpha 层 vs 下游 004 纪律层边界;四念头位置 + 接口 + gated
- 工程纪律 — 跨器官接口契约(复用 004 StrategyModule IDL 隔离范式 + v1 AC 条款)

### Z · 参照系
- mode: 对标 SOTA(聚焦"目标态架构 + 分期演化"层,不重刷 v1 的回测方法论 SOTA)
- 用户外部材料: 无(X 的 5 个标的即全部一手材料;双方 P2 §2 均确认无额外 URL 待叠加)

### W · 产出形态
- 架构 refactor-plan(目标态模块图)✅ → 见 §"Refactor plan"
- free-essay(final goal 全貌叙事)✅ → 见 §"Long-form synthesis"
- next-dev-plan(Strangler Fig 分期路线)✅ → 见 §"Next-version dev plan"

（verdict-only / decision-list / next-PRD **未勾** → v1 已产 decision-list + PRD draft,v2 不重复;本文档无 §"Verdict rationale" / §"Decision matrix" / §"Next-version PRD draft"。）

### K · 用户判准
> 我要跑 forge 009 v2,是因为 v1 出了 verdict(009 = 集成契约 + 共享回测地基,分期落地,别先建大壳)后,我意识到一个真问题:**现在 004、008、四个新念头更多是"各做各的",缺一张统一的目标态蓝图。** 我担心没有把 final goal 定清楚,会多走弯路,架构设计也不够充分彻底。所以 v2 的目的 = **把 009 闭环的最终形态 + 每个器官边界 + 分期演化路线画彻底,产一张"目标态架构蓝图"**。**这不是重新质疑该不该建(v1 已定),而是画清"怎么建、最终长啥样、怎么分期走到那"。**
>
> **最重要的 binding**:① 死守 v1 verdict 不推翻(蓝图 ≠ 一次性建完的大工程 = 最怕的 V4;每期都要能独立跑、独立有价值);② 蓝图射程 = 画到"完整闭环能自洽跑起来"为止(采集→结构化→信号→决策→纪律执行→复盘→反馈),四念头都就位,**不画**更远的(多分析师池、自动化提升、机构级扩展);③ 四念头位置全钉死(在闭环哪个位置 + 接口对谁 + gated 条件):①验证 alpha→回测层 alpha 评估头;②回测→共享 PIT 数据层 + 两头;③图谱→v2+ 信号 lane(gated);④蒸馏→最后做的独立信号 lane。
>
> **第一性原理(不变)**:我懂算法/自动化/数据,不懂投资。产品本质 = 用工程强项补投资 domain 短板。每个器官按"补哪个短板"定位。**其他 binding**:①别让子系统(尤其 build runtime)静默替我定方向(防 V4);②008 合规边界已拍板不重审;③自用单人不商业化;④投资 domain 判断给可验证依据(回测数字/SOTA),别凭感觉。
>
> **我特别想让蓝图回答**:七环节里哪些已有器官/要新建器官/未来插槽(一张图看清)?器官之间接口契约到底长啥样(尤其"008→回测→StrategyModule→004"主链)?"复盘/反馈"环怎么在架构上闭合(v1 没画透)?从现在到目标态,第一期该交付哪个最小可用切片?

### 收敛模式
strong-converge → 单一 verdict + 残余分歧降级为 v0.2 note(见 §"What this menu underweights")

---

## Refactor plan

> **W = refactor-plan 的产出 = 目标态模块图(蓝图的"结构骨架")。** 这是一张**分层 + 数据流 + 反馈回流**的闭环图,每个器官标 `keep / new / gated`,每条器官间箭头标"契约名 + 传什么"。合并双方 P3R2 §4 的最强版本。

### 目标态七环节闭环图(ASCII)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  第 0 层 · 数据 / 证据                                                          │
│                                                                               │
│   [008 采集] ──采集契约──▶ [008 结构化]                                        │
│    keep                     keep (advisor_reports + 轻量包)                    │
│                                  │                                             │
│                                  │  ⟨证据契约: source_id / week_id /           │
│                                  │   structured_json / transcript / as-of⟩     │
│                                  ▼                                             │
│                        ┌──────────────────────────────┐                       │
│                        │  ⭐ PIT 价格历史层 (new)      │  ◀── 唯一关键新器官     │
│                        │  日线 + 复权 + PIT ticker +   │                       │
│                        │  退市感知; 唯一行情来源        │                       │
│                        │  defer: 多市场/汇率/tick       │                       │
│                        └──────────────────────────────┘                       │
└──────────────────────────────────┬────────────────────────────────────────────┘
                                    │ ⟨as-of 契约: 所有字段带当时可见时间戳,防 look-ahead⟩
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  第 1 层 · 验证 / 复盘  (回测层 = new · 009 的实际枢纽)                          │
│                                                                               │
│   ┌────────────────────────┐        ┌──────────────────────────────┐          │
│   │  alpha 头 (new)         │        │  calibration 头 (new)         │          │
│   │  分析师方向 vs 真实股价   │        │  我的决策 vs 不动反事实         │          │
│   │  → hit-rate/超额/Z 显著  │        │  读 decisions.would_have_...  │          │
│   │  → DSR/PBO (v1 定)      │        │  + env_snapshots (决策快照)    │          │
│   │  输入: advisor_reports   │        │  输入: 004 档案 + PIT 价格路径 │          │
│   │       + PIT 价格         │        │                               │          │
│   └───────────┬────────────┘        └──────────────┬────────────────┘          │
│               │ 共享同一 PIT 数据层,但指标分离(两头不合并)                     │
└───────────────┼───────────────────────────────────┼────────────────────────────┘
                │ ⟨alpha 契约: 某 source_id 的得分,     │ ⟨calibration 契约: 纪律得分,
                │  不跨 source 合并 (AC-2)⟩            │  不静默改阈值⟩
                ▼                                     │
┌──────────────────────────────────────────────┐    │
│  第 2 层 · 信号  (StrategyModule 多 lane · keep IDL) │    │
│                                               │    │
│   [advisor lane] [XGBoost lane]  keep         │    │
│   [⭐alpha 得分 lane]  new (回测得分入信号)     │    │
│   [图谱 lane]  gated (v2+)                     │    │
│   [蒸馏 lane]  gated (末位)                    │    │
│   —— 各 lane 平权 / source_id 隔离 / 不合并    │    │
│      lane constructor 不见 registry           │    │
└──────────────────┬────────────────────────────┘    │
                   │ ⟨信号契约: StrategySignal              │
                   │  (direction/confidence/rationale),    │
                   │  写 strategy_signals 带 source_id⟩    │
                   ▼                                       │
┌──────────────────────────────────────────────┐         │
│  第 3 层 · 决策 / 纪律  (004 承诺壳 · keep)     │         │
│                                               │         │
│   [conflict_reports]  ◀── 无 winner/recommended/         │
│         │              aggregate 字段 (R10, schema enforce)│
│         ▼                                     │         │
│   [decisions]  ◀── human 拍板 (无自动下单)     │         │
│         │                                     │         │
│         ▼                                     │         │
│   [rebuttals]  ◀── devil's advocate            │         │
└──────────────────────────────────────────────┘         │
                                                          │
╔═════════════════════════════════════════════════════════════════════════════╗
║  反馈回流 (闭环之所以是"环") —— 两条线都过 human 确认闸 (human-on-the-loop)     ║
║                                                                               ║
║  ① alpha 头得分 ──(建议)──▶ 调 [alpha 得分 lane] 的 confidence 权重           ║
║  ② calibration 头得分 ──(建议)──▶ 调 [rebuttals] 的 devil's-advocate 阈值     ║
║                                                                               ║
║  ⚠ 系统只产"建议旋钮值",human 确认后才生效;不得静默改权重/纪律阈值            ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

### 模块分组(按器官,标 keep/new/gated + 两档详略)

#### 模块 A · PIT 价格历史层(new · 唯一关键新器官 · 定量档)
- **当前问题**:004 `advisor_reports` **无 realized-return / 价格结果列**;004 现在只有 `env_snapshots.price` 单点(决策时点),没有连续价格序列(P1-Opus §1A)。alpha 头要"分析师方向 vs 之后真实股价",calibration 头要"决策后 N 天价格路径",都靠这层。
- **目标态**:唯一行情来源。范围 = **日线 bars + 拆分/分红复权 + PIT ticker/date 映射 + 退市股感知(survivorship-free)**;defer 多市场/汇率/分钟级/tick(P2-Opus §1 row 3 / P2-GPT §1 row 3)。
- **接口契约(定量)**:`(ticker, as-of date) → 复权收盘价`;所有字段带当时可见时间戳(as-of),CHECK/NOT NULL 级硬约束防 look-ahead(继承 004 把红线写进 DDL 的范式,P1-Opus §1D)。
- **contract tests**(必测):as-of cutoff 防未来数据;唯一价格源(不许第二处行情);复权样例(拆分不被当暴跌);退市样例(survivorship 不泄漏)。
- **风险**:复权若 v0.1 不做 → alpha 头把拆分当暴跌,回测全错(P2-Opus §1 row 3)。
- **预估代价**:L(核心新建 + PIT 正确性)

#### 模块 B · 回测层双评估头(new · 定量档)
- **当前问题**:004 只有 `correlation_audit.py` 的 Pearson 雏形,远不足以判 alpha(v1);calibration 缺"事后价格、不动基线、反事实窗口"(P1-GPT §1B —— `would_have_acted_without_agent` 在,但不是现成一等表)。
- **目标态**:共享 PIT 数据层,**两个指标分离的评估头**。alpha 头 = 分析师方向 vs 真实股价 → hit-rate/超额/Z 显著 + DSR/PBO(TipRanks 三件套,v1 定);calibration 头 = 读 `decisions.would_have_acted_without_agent` + `env_snapshots` 做反事实(P3R2-Opus §4)。
- **接口契约(定量)**:alpha 头对外只暴露"某 source_id 的 hit-rate/超额/DSR",**不暴露跨 source 合并结论**(v1 AC-2);两头共享数据层但**指标不合并**。
- **contract tests**(必测):alpha 不跨源合并;calibration 不静默改阈值。
- **风险**:两头数据模型/指标不同,共享 runner 可能被迫为迁就一头打补丁(v0.2 note 1 → 触发 v1 的统一壳 gate 重估)。
- **预估代价**:alpha 头 L(最先且最重)/ calibration 头 M。

#### 模块 C · StrategyModule 信号层(keep IDL / refactor 加 lane · 定量档接口 + 定性档 gated lane)
- **当前问题**:IDL 干净(source_id + analyze → StrategySignal,多 lane 不合并,constructor 不接 registry),但 alpha 回测得分尚无入口。
- **目标态**:保留 IDL 与多 lane;**新增 alpha 得分 lane**(把回测得分实现为一个平权 lane 进 conflict_reports);图谱 lane / 蒸馏 lane 作 **gated 未来插槽,只画 StrategyModule 签名 + gate,不画内部**(两档详略,P2-Opus §1 row 5)。
- **接口契约(定量)**:每个 lane `source_id` 唯一;写 `strategy_signals` 带 source_id;**lane 不得绕过 IDL 直连 DB**(P1-Opus §1D 风险)。
- **contract tests**(必测):StrategyModule source_id 唯一;lane constructor 不见 registry。
- **预估代价**:S(复用现有 IDL,新增 lane 是既定扩展点)。

#### 模块 D · 004 决策/纪律层(keep · 定量档边界)
- **当前问题**:无(schema 已 enforce 边界)。
- **目标态**:`conflict_reports`(无 winner/recommended/aggregate 字段,R10)→ `decisions`(human 拍板)→ `rebuttals`(devil's advocate),全 keep。
- **接口契约(定量)**:004 API/DB 响应中**任何字段都不得出现跨源合并的单一权威评分**(v1 AC-1,且 P1-Opus §1C 证明 schema 已背书)。
- **contract tests**(必测):004 无 winner/recommended/aggregate 字段。
- **预估代价**:0(纯 keep + 加 alpha 得分 lane 的消费,已在模块 C)。

#### 模块 E · 反馈回流线(new · 定量档 · 闭环的"环")
- **当前问题**:v1 没画透"复盘→反馈"如何闭合(K 特别想要)。
- **目标态**:两条回流线,**都过 human 确认闸(human-on-the-loop)**:
  - 线①:alpha 头得分 →(建议)→ 调 alpha 得分 lane 的 confidence 权重;
  - 线②:calibration 头得分 →(建议)→ 调 devil's-advocate 阈值。
- **接口契约(定量 · human-on-the-loop 硬约束)**:见下 §"回流边界硬约束清单"。
- **contract tests**(必测):calibration/alpha 回流不静默改权重/纪律阈值(必须留 human 确认记录)。
- **预估代价**:M(依赖 M2/M3 评估头先跑通才有数据回流)。

### 回流边界硬约束清单(human-on-the-loop · 继承 v1 AC 风格 · 可测)

> **区分点(干净)**:**"旋钮"(调信号/纪律的强度参数)= 建议→human 确认→之后可自动套用;"动作/结构/决策权" = 永远手动。** 来源:P3R1-GPT §3 待固化1 + P3R2 双方 §1 完全采纳。

**可"建议→human 确认→之后自动套用"的旋钮**(白名单):
- 单个 `source_id` 的 confidence multiplier / cap
- alpha lane 启用 / 降权
- devil's-advocate 触发阈值
- 复盘提醒频率
- calibration 报告窗口长度

**永远手动 / 禁止自动化的项**(黑名单):
- 任何买 / 卖 / 持有 / 等待动作
- 单笔交易最终决定
- 自动下单 / 调仓
- 跨源权威综合分
- 新增外部顾问 / 扩大采集或交易 universe
- 把图谱 / 蒸馏 lane 升为决策者

**可测**:回流动作若触及黑名单任一项 = BLOCK;白名单旋钮的"自动套用"必须能追溯到一次 human 确认记录（v0.2 note 2:前 K 次是否强制逐次确认,M3 定）。

---

## Long-form synthesis

> **W = free-essay 的产出 = final goal 全貌叙事(蓝图的"愿景全景")。** 合并双方 P3R2 §4 的论点。

**这张蓝图回答的第一个问题,是 operator 的真实焦虑:"我把 004、008、四个念头分散建了,它们到底是不是一个东西?"** v2 的答案是:它们**已经是**一个闭环的不同器官,只是缺一张图把它们连起来。SOTA(量化系统的标准分层 data → strategy → backtesting → execution,post-trade analysis feeds back into modeling)直接验证了这个形态 —— 双方两位审阅人各自独立读完 004 的 13 个 DB migration,不约而同画出了同一张七环节图。operator 感觉"各做各的、缺统一方向",本质不是缺一个大壳,而是**缺这张 end-to-end coherence 图 + 器官之间的契约**。这是本轮最重要的认知转折:**统一方向 ≠ 统一壳**。

**七环节各补哪个投资短板(第一性原理"工程补 domain 短板"的逐环节落地)**:
- **008 采集**补"投顾内容漏散、看过就忘"—— 把付费投顾的分析持久化成可查证据。
- **008 结构化 + advisor_reports**补"读了但没沉淀成可计算的东西"—— 变成带 source_id/week_id 的结构化记录。
- **⭐PIT 价格历史层(唯一新器官)**补"我说某分析师去年准,但没有 ground truth"—— 提供 as-of 正确的真实股价,让"准不准"可被计算。
- **回测 alpha 头**补"我判不了分析师有没有 alpha"—— 用 TipRanks 三件套 + DSR/PBO 把主观印象变成 hit-rate/超额/显著性数字。
- **回测 calibration 头**补"我压力下会乱动,但不知道乱动到底亏没亏"—— 用 `would_have_acted_without_agent` 反事实算"我的决策 vs 不动"。
- **StrategyModule 信号层**补"多个信号源我会不自觉合并成一个'感觉'"—— 强制多 lane 平权、source_id 隔离、不合并。
- **004 决策/纪律**补"执行走样、临场推翻计划"—— 承诺壳 + devil's advocate + human 拍板。

**为什么这是"环"不是"链"(v1 没画透、K 特别想要的答案)**:一条链是"采集→…→执行"跑完就结束;一个环的关键在于**复盘算出的东西要回流去校准上游信号强度和下游纪律强度**。具体两条回流线:alpha 头算出"某分析师历史 hit-rate 低" →(建议)→ 调低他那条 lane 的 confidence 权重(上游信号给多强);calibration 头算出"我历史上一乱动就亏" →(建议)→ 调严 devil's-advocate 触发阈值(下游纪律卡多严)。**这两条线让闭环闭合** —— 系统会随着复盘数据越来越懂"哪个信号可信、我什么时候该被拦"。

**但这里藏着 K 的核心 binding**:回流**绝不能自动**。SOTA(自适应交易系统)证明自动调参有 parameter sensitivity + 过拟合风险,而**过拟合恰恰是 operator 判不了的(他不懂投资)**。所以蓝图定死 **human-on-the-loop**:系统只产"建议旋钮值",human 确认后才生效。这不是妥协,而是第一性原理的直接推论 —— 工程补 domain 短板意味着系统负责"算得准"(把过拟合防住的统计纪律),human 负责"拍板"(承认自己判不了、但保留最终控制权)。自动回流本质就是系统在替 operator 定"信号多强/纪律多严",踩 K binding① 的红线。

**为什么不建大壳(直面 operator 最怕的 V4)**:分期锚是 **Strangler Fig**(Fowler / Azure)—— 新回测器官**latch 到已 ship 的 004/008 上、piece by piece 长起来**,不替换、只扩展,004 全程一直可用。M2 alpha 头先做(operator 最想要的 high-value:"分析师到底行不行"),它**不依赖 M3 就能独立回答问题**。这就是"每期独立可用"的工程含义:不是"全做完才有价值",而是每长出一个器官,闭环就多闭合一段、多回答一个问题。蓝图的"充分彻底"体现在**两档详略** —— 现在要建的器官(PIT 数据层/两头)画到定量契约 + AC,未来插槽(图谱/蒸馏)只画 StrategyModule 签名 + gate 条件。**"充分彻底 vs 防 V4"不是二选一,是按器官成熟度分档画**:画清方向(全貌图)但不给没验证的东西写 spec。

**未来 3-6 月可能的演化路径**:M1→M2 跑通后,operator 第一次能拿到"某分析师 vs 大盘的 as-of 可复现超额报告"—— 这是整个闭环第一个可验证的价值锚。若 M2 证明分析师确有 alpha,M3 的 calibration 头会让承诺壳从"凭感觉设阈值"变成"用我自己的反事实历史校准阈值"。图谱/蒸馏两个 gated lane 是否触发,取决于 M2/M3 是否证明"简单信号不够";即使触发,是否要先跑 forge v3 定内部,也留到 gate 触发时再判(v0.2 note 3)。**整张蓝图的射程止于"闭环自洽跑起来",不画多分析师池/自动化升级/机构级扩展 —— 那些是闭环跑通后的事,现在画等于画虚(K binding②)。**

---

## Next-version dev plan

> **W = next-dev-plan 的产出 = Strangler Fig 分期路线(蓝图的"落地路线")。** 按 milestone 切,不到 spec 级(spec 是 L4 spec-writer 的工作)。双方 P3R2 §4 milestone 完全一致,取合并版。**核心纪律:新回测器官围绕已 ship 的 004/008 生长,每期独立可用,M2 不依赖 M3。**

## Phase M1 · PIT 价格历史层(预估 L)· 新器官 latch 点
- 目标:落地 PIT 价格历史层 = 日线 + 复权 + PIT ticker/date + 退市感知 + as-of 契约,接 008 证据包 + 价格源。
- 关键 milestone:
  - M1.1: PIT 数据 schema(ticker × as-of date → 复权收盘价;退市股保留)+ as-of NOT NULL 硬约束
  - M1.2: 接入价格源(单人关注股范围)+ 拆分/分红复权处理
  - M1.3: contract tests(as-of 防未来 / 唯一价格源 / 复权样例 / 退市样例)
- 依赖:008 现状(可溯源包)+ 外部价格数据源
- 风险:复权不做 → alpha 头把拆分当暴跌,回测全错(Evidence map "价格层范围"行);不动基线/反事实窗口粒度未定(v0.2 note 1,此期开始细化)
- **独立可用性**:M1 单独完成 = 有了唯一行情地基,但还不出分析结论(需 M2)。

## Phase M2 · alpha 头(预估 L)· **最先出可验证数字 · 最独立可用**
- 目标:先做 alpha 头,产分析师 hit-rate / 平均超额 / Z 显著性 / DSR/PBO / 样本窗报告。**这是 operator 最想要的、闭环第一个可验证价值锚。**
- 关键 milestone:
  - M2.1: Hit Ratio + 平均超额 + Z 显著性(TipRanks 三件套)
  - M2.2: walk-forward/OOS + 交易成本 + trial-count 记账 + DSR/PBO deflate(v1 定的统计纪律)
  - M2.3: alpha 得分实现为一个新 StrategyModule lane(平权进 conflict_reports)+ contract tests(alpha 不跨源合并 / source_id 唯一)
- 依赖:M1 数据层
- 风险:trial-count 不记账 → DSR 无法正确 deflate(过拟合自欺);分析师历史样本量可能不足以让 DSR 显著(见 §"What this menu underweights" 跨 v 提示)
- **独立可用性**:M2 完 = **可单独回答"某分析师到底行不行",不依赖 M3**。这是 Strangler Fig 的关键期。

## Phase M3 · calibration 头 + 两条回流线(预估 M)· 闭环真正闭合
- 目标:做 calibration 头(读 004 档案反事实)+ 两条 human-on-the-loop 回流线,让闭环"环"起来。
- 关键 milestone:
  - M3.1: 反事实 calibration 数据模型(读 `decisions.would_have_acted_without_agent` + `env_snapshots` + PIT 价格路径;定"不动"基线 N 天窗口 —— v0.2 note 1 此期定死)
  - M3.2: 两条回流线(alpha 得分→信号权重建议 / calibration→纪律阈值建议),human-on-the-loop 确认闸 + 前 K 次强制逐次确认(v0.2 note 2 此期定)
  - M3.3: contract tests(calibration 不静默改阈值 / 回流动作触黑名单 = BLOCK)
- 依赖:M2(共享 runner 已跑通 + alpha 得分 lane 已在)
- 风险:两头指标不同,runner 被迫打补丁 → 触发 v1 的统一壳 gate 重估(v0.2 note 1)
- **独立可用性**:M3 完 = 闭环七环节全部闭合,反馈回流生效(human 确认制)。

## Phase M4(gated)· 图谱 lane / 蒸馏 lane
- 目标:仅在 M2/M3 证明简单信号有价值后,另起 gate 评估图谱/蒸馏。
- 门槛(gated 条件):
  - 图谱 lane:gated 在"回测证明简单信号不够 + 008 抽取脆弱性可控"
  - 蒸馏 lane:末位,只能落成独立信号 lane(不替人决策/不综合打分,v1 AC-4)
- **决策岔口**(v0.2 note 3):gate 触发后,是否先跑 **forge v3** 定内部,还是直接进 L4 —— 留到 gate 触发时再判。
- **图谱与蒸馏永不进 M1-M3。** 目标态图只给它们留 StrategyModule 签名 + gate(定性档,不画内部)。

---

## What this menu underweights(强制自批判)

诚实表述本蓝图可能 underweight 的点。v2 全程 0 实质分歧,故本节重点不是"未整合的反对证据",而是**收敛过头的风险 + 蓝图射程外的盲区 + 跨 v 触发点**。

- **convergence_mode 副作用(本轮最该警惕的)**:strong-converge + 双方**独立读 DB schema 撞到同一张七环节图** + 独立检索到同一批 SOTA(P3R1 双方均自述"两个独立审阅路径撞到同一堵墙")。证据虽硬,但**双模型同源于相似训练语料,可能共享同一盲点**。具体可疑处:(a) 双方都把"回测器官围绕 004/008 生长"当成干净的 Strangler Fig,但**都没深究"回测层直连 004 DB 读 `decisions`/`env_snapshots` 反事实"是否会让 calibration 头和 004 schema 耦合死** —— 一旦 004 改 schema,calibration 头可能连带崩(P1-Opus §1D 提了"回测层最容易和 004 表耦合死"的风险,但 verdict 只用"单向契约 + 不绕过 IDL"对冲,未展开 004 schema 演化时的兼容策略);(b) 双方都判 human-on-the-loop 是"承认 operator 判不了过拟合",但**都没质疑"operator 判得了旋钮建议值本身吗"** —— 如果系统建议"把某分析师权重从 0.8 调到 0.3",operator 凭什么判断这个建议对不对?human-on-the-loop 把最终控制权还给 operator,但 operator 的判断依据仍是系统给的回测数字,这里有一个隐性循环依赖,v2 未拆解。

- **反对证据未充分整合**:v2 内部无对立证据(§"Evidence map" 无 v2 内 ⚠ 冲突行),但 §"Evidence map" 有 3 条 ⚠ 指向 v0.2 note —— 均是**已识别但故意 defer 到 M1/M3 细化**的粒度问题(不动基线窗口 / 前 K 次确认 / 图谱 gate 走 forge v3 还是 L4),不是被忽略的分歧。

- **Y 视角覆盖盲区**:Y 未含"安全/隐私",但回测层 calibration 头要读 004 的**个人决策档案 + 持仓快照**(`decisions` / `env_snapshots`),PIT 价格层 + 008 证据也涉敏感数据。本轮未评估回测层的数据访问控制 / 存储边界,值得 L4 或 v3 补 attention。**注意:合规按 K binding② 明确不重审,此处仅指工程侧数据安全,非合规。**

- **K 中未充分回应的关切**:K 第一性原理引 v1 的"要 beat 80-90% 的一般分析师才够价值"(v1 §underweights 已挂)—— v2 蓝图给了 alpha 头的度量方法(TipRanks + DSR/PBO),但**仍没给"80-90% 分位"的 baseline 从哪来**(需要一个分析师样本池做分母)。这是 M2 落地会撞到的现实缺口:v0.1 可能只能给"这个分析师 vs 大盘/S&P500"的绝对超额,给不出"vs 80-90% 同行"的分位。**蓝图未把"分析师样本池采集"画成一个器官** —— 因为它超出 K binding② 的射程(闭环自洽即止),但 operator 应预期这个缺口。

- **X 标的覆盖局限 / 沙箱**:本轮双方**均真实读取** 004 strategy 层 + alembic 13 migration(无 fallback,补齐了 v1 未读 DB schema 的盲区)。但 X 全部指向 IDS + **单一 XenoDev 004-pB repo** —— 蓝图的"PIT 价格层接外部价格源"这一环**没有任何现成标的可对照**(004 现在无价格历史基础设施),M1 是纯新建,代价估计(L)是双方基于 SOTA 推断,非基于已有代码 —— 比其他模块的估计更不确定。

- **forge versioning 提示(什么新信息会触发 v3 并改变本蓝图)**:(1) M2 落地后发现分析师历史样本量不足以让 DSR 显著(alpha 判不出来)→ 需重估整个闭环前提,可能触发 v3;(2) calibration 头直连 004 DB 反事实被证明耦合过深 / runner 频繁打补丁 → 触发 v1 的统一壳 gate 重估(v0.2 note 1);(3) 图谱/蒸馏 gate 触发 → 按 v0.2 note 3 决定是否起 forge v3 定内部;(4) operator 决定要严格的"beat 80-90% 同行"分位 → 需评估分析师样本池采集(超当前射程的新 domain 工作)。

（本节非空。**核心提醒:v2 是双模型高度收敛的蓝图综合,不是用户访谈或真实回测数据 —— 真实的价格数据获取成本、分析师样本量、004 schema 演化摩擦,任一都可能在 M1/M2 落地时推翻本蓝图的代价估计或器官边界。**)

## Decision menu(for human)

### [A] 接受蓝图进 L4(需 fork 出 PRD branch)
```
⚠ /plan-start 要求 <prd-fork-id> + 完整 PRD 目录,不能直接吃 forge stage 文档。
⚠ 现有仓库 PRD 都是平铺布局 — discussion/<root>/<prd-fork-id>/PRD.md(无嵌套)
⚠ 本 v2 未产 next-PRD draft(W 未勾)——本蓝图是「目标态图 + 分期路线」,不是 PRD。
   若进 L4,PRD 内容须以 v1 stage doc 的 §"Next-version PRD draft"(009 v0.1)为骨架,
   再叠加本 v2 蓝图的 M1 PIT 数据层定量契约 + 回流边界硬约束清单 + contract tests 清单。
⚠ 特别注意:本蓝图核心是"七环节契约化闭环图,非独立统一壳 + Strangler Fig 每期独立可用"。
   若进 L4,不能被 build runtime 悄悄扩成大壳(K binding①)。

流程(暂时手工,等待 /fork-from-forge 命令落地):

1. 选一个 prd-fork-id:009 是 root → 如 009-pForge / 009-blueprintV2
   prd-fork-id 直接放在 discussion/009/ 下(平铺,不嵌套)

2. 创建 discussion/009/<prd-fork-id>/PRD.md
   - 骨架 = v1 stage doc 的 §"Next-version PRD draft"(009 v0.1)
   - 叠加 v2 蓝图:M1 PIT 数据层定量契约 / 回流 human-on-the-loop 边界清单 / contract tests 清单
   - 补 frontmatter:
     **PRD-form**: simple
     **Source**: forge stage-forge-009-v1.md(定位)+ stage-forge-009-v2.md(目标态图)

3. 创建 discussion/009/<prd-fork-id>/FORK-ORIGIN.md
   说明 forked-from = forge stage v1+v2,parent = 009(非 L3 candidate)

4. /plan-start <prd-fork-id>
   → 产 HANDOFF.md → 新开 XenoDev session 真开发(spec/tasks/build/quality)
   → 建议只把 M1(PIT 数据层)放进第一个 HANDOFF,M2/M3 分批,严守 Strangler Fig
```
适用:你接受这张目标态蓝图 + Strangler Fig 分期,想直接推进 M1 PIT 数据层落地。

### [B] 跑 forge v3(说明需要补什么)
```
/expert-forge 009
# 在 Phase 0 intake 时调整 X / Y / Z / W / K
# 旧 v1/v2 整目录保留作历史参考
```
适用:
- 想把 §"underweights" 的盲点纳入(回测层↔004 schema 耦合的兼容策略 / 数据安全视角 / 分析师样本池够不够 DSR 显著)
- 图谱/蒸馏 gate 触发,要定内部(v0.2 note 3)
- K 关切发生变化(例如决定要严格的"beat 80-90% 同行"分位)

### [C] 局部接受(蓝图已高度收敛,可分批采纳)
- ✅ 建议先采纳:七环节目标态图(§"Refactor plan")+ 回流 human-on-the-loop 边界硬约束清单 + contract tests 清单(这三条证据最硬、争议最小、可直接指导 M1)
- ✅ 建议先采纳:Strangler Fig 分期 M1→M2→M3→M4(gated),先推 M1 PIT 数据层
- ⏸ 可挂起:M3 calibration 头 —— 先看 M2 alpha 头能不能出可信数字(样本量够不够 DSR 显著),再决定 calibration 值不值得建
- ⏸ 可挂起:图谱/蒸馏两个 gated lane 的定性签名 —— 等 M2/M3 证明简单信号价值后再触发
- ❌ 需你确认拒绝的:无(verdict 无 unresolved,双方 R2 完全一致)

### [P] Park
```
/park 009
```
保留所有 forge 产物,标记为暂停。复活时不重做 forge 层。
适用:M1 依赖的外部价格数据源尚未选定,或 008 forge v4 的信号 spike 还没落地(009 回测上游依赖它)。

### [Z] Abandon
```
/abandon 009
```
forge verdict **不支持** abandon —— 双方判"闭环形态成立、目标态图清晰、非 V4"。仅当你后续发现分析师样本量根本判不出 alpha(闭环第一个价值锚 M2 塌了)才考虑,归档 lesson 文档。

---

## Forge log
(由 /expert-forge 命令更新;记录每次 forge run 的 v 序列 + 关键 verdict 一句话)

- v2: 2026-07-01 — verdict: "009 目标态蓝图 = 七环节契约化闭环图(非独立统一壳,不推翻 v1);唯一关键新器官 = PIT 价格历史层(日线+复权+PIT+退市);Strangler Fig 分期 M1 数据层→M2 alpha 头→M3 calibration+回流→M4 gated;三条硬约束 = 回流 human-on-the-loop / 两档详略 / 回测层 contract tests。"
- v1: 2026-07-01 — verdict: "009 = 闭环集成契约规范 + 共享回测地基(非独立统一壳);回测 new-first 按 DSR/PBO 建,图谱 defer v2+,蒸馏最后且独立 lane 化,004 端永不呈现权威综合分。"
