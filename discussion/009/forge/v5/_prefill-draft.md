# Forge intake prefill draft · 009 · v5

**Generated**: 2026-07-16
**Subagent**: forge-intake-prefill
**Proposal status**: found
**Forge target type**: root-idea

> **Note (repeat-forge idea)**: 009 是 **forge-first idea**(目录有 `FORGE-ORIGIN.md`,
> 无 L1/L2/L3 stage docs)。本 idea 已跑过 forge v1-v4。本轮 v5 的"中间层产物"
> 不是 L1/L2/L3 层文档,而是 **prior forge stage docs (v1-v4) + fork PRD + HANDBACK-LOG**。
> 因此下方 Bundle 用 repeat-forge 语义(prior-forge / fork-artifacts / full-history),
> 不是标准 from-L2/from-L3。
>
> **v5 触发材料(高优先 X)**:`operator-input-2026-07-16-implicit-signals.md` —— operator
> 亲述事实修正:分析师**不荐股**、信号只以**隐性形态**存在,推翻 M2 alpha 头"存在显性
> (ticker,direction,date) 信号"的输入假设,07-07 smoke path 决议前提被 supersede。
> 这是 forge v5 的核心审阅标的,**default checked**。

## Detected proposal section

**Title**: 投资决策闭环(集合体 · 008采集 + 回测验证 + 004纪律)
**proposals.md line**: 276
**Body byte count**: ~2050 bytes(行 276-315,proposal §009 是文件最后一个 entry,到 EOF)
**Fields detected**: `### 想法`, `### 我为什么想做这个`, `### 闭环的灵魂(已定 · 关键)`, `### 我已经想过的角度(四条核心工作)`, `### 已 build 可复用资产(查实于 XenoDev projects/004-pB)`, `### 我的诉求`

> **未检出**:`### 我已知的相邻方案/竞品`(Z 段缺)、`### 我的初始约束`、`### 我的倾向`、
> `### 还在困扰我的问题` —— 这些 ### 子标题在 §009 中不存在(proposal 用了 idea 特有的
> `### 闭环的灵魂` / `### 已 build 可复用资产` 两个非标准段,已按语义映射进 K/X)。

## X candidates (raw)

### From proposal section

- [x] **proposal-text**:"`投资决策闭环(集合体)` §想法 + 我为什么想做这个 + 闭环的灵魂 + 我的诉求(全段)"
  - type: pasted-text
  - reachable: n/a
  - default: ☑ checked(idea 本身核心文本)
  - source_line: proposals.md:276
- [ ] `/home/ys/codes/XenoDev/projects/004-pB`(来自 `### 已 build 可复用资产` 段引用的
  004 已 ship 信号引擎骨架:`strategy/base.py` StrategyModule IDL / `xgboost_model.py` /
  `feature_engineering.py` / `train.py` / `correlation_audit.py` / `advisor_strategy.py` /
  `domain/advisor.py` / 13 alembic migration)
  - type: external-path
  - reachable: ✅(本 subagent Glob 命中 9238 个文件;`src/decision_ledger/`、
    `domain/advisor.py`、`alembic/versions/00xx` 均存在)
  - default: ☑ checked
  - source_line: proposals.md:303-309
  - ⚠ **Codex sandbox 注意**:该目录在 XenoDev 仓(跨仓 · `feat/009-spec` 分支上有 alpha 模块),
    Phase 1 若走 Codex 沙箱可能 BLOCK 跨仓读;Opus 直读本机路径无碍。
- [ ] `/home/ys/codes/XenoDev/out/collection.db`(008 语料,9081 条 · article 1179 /
  qa 7545 / replay 357;来自 v5 触发材料 §4 核查)
  - type: external-path
  - reachable: ⚠ 二进制 .db(存在但本 subagent 无法 Read 文本;存在性由 Glob 兜底确认 —— 文件在)
  - default: ☑ checked(v5 提取头设计的直接语料依据;Phase 1 Opus 需知其 schema/规模,
    不必真读全库)
  - source_line: operator-input-2026-07-16-implicit-signals.md:63(v5 材料引用,非 proposal 内)
  - ⚠ **Codex sandbox 注意**:同上,跨仓 + 二进制;human 若要 Phase 1 真查 schema 建议
    附一份 `.schema` 文本快照而非让沙箱读 .db。

### From discussion/009/ (repeat-forge products — 非 L1/L2/L3)

- [ ] `discussion/009/operator-input-2026-07-16-implicit-signals.md`
  - type: proposal-section(v5 触发材料 · 事实修正)
  - reachable: ✅
  - default: ☑ checked(**v5 核心 X · 高优先** —— 推翻既有路线图输入假设)
  - source: glob 命中(~4.9k chars ≈ 1.6k tok)
- [ ] `discussion/009/009-pForge/PRD.md`(phased M1/M2 · fork 已 complete)
  - type: stage-doc(fork PRD · 现状态 SSOT)
  - reachable: ✅(~13k chars ≈ 4.4k tok)
  - default: ☑ checked(v5 要重排 M3'/蒸馏头,必须以现 PRD 的 M1/M2/OUT 边界为基线)
  - source: glob discussion/009/009-pForge/PRD.md
- [ ] `discussion/009/handback/HANDBACK-LOG.md`(21+ 决议 · append-only)
  - type: stage-doc(决议日志)
  - reachable: ✅(total_decisions=21;含 07-07 P2-prod-precondition-gap · smoke path 决议)
  - default: ☑ checked(v5 直接 supersede 其中 07-07 决议,专家需读原决议上下文)
  - source: glob discussion/009/handback/HANDBACK-LOG.md
- [ ] `discussion/009/forge/v4/stage-forge-009-v4.md`(O8 下游集成:非方向 evidence 上台)
  - type: stage-doc(prior forge verdict · 最近一版)
  - reachable: ✅
  - default: ☑ checked(v4 是最近 forge verdict,是"从哪继续"的锚)
  - source: glob discussion/009/forge/v4/stage-forge-009-v4.md
- [ ] `discussion/009/forge/v3/stage-forge-009-v3.md`(provider 双 as_of 轴契约)
  - type: stage-doc(prior forge verdict)
  - reachable: ✅
  - default: ☐ unchecked(advanced — full-history Bundle 才勾)
  - source: glob discussion/009/forge/v3/stage-forge-009-v3.md
- [ ] `discussion/009/forge/v2/stage-forge-009-v2.md`(七环节目标态蓝图 + Strangler Fig 分期)
  - type: stage-doc(prior forge verdict · 目标态蓝图)
  - reachable: ✅
  - default: ☐ unchecked(蓝图 · full-history 才勾;若 v5 要重排闭环环节次序建议手勾)
  - source: glob discussion/009/forge/v2/stage-forge-009-v2.md
- [ ] `discussion/009/forge/v1/stage-forge-009-v1.md`(该不该建 / 怎么建 · 集成契约 + 共享回测地基)
  - type: stage-doc(prior forge verdict · 奠基)
  - reachable: ✅
  - default: ☐ unchecked(奠基 verdict · full-history 才勾)
  - source: glob discussion/009/forge/v1/stage-forge-009-v1.md
- [ ] `discussion/009/M1-price-data-source-research.md`(数据源选型 + 表 DDL 调研)
  - type: stage-doc(专题调研 · M1 已消化进 PRD 附录 A)
  - reachable: ✅
  - default: ☐ unchecked(M1 数据层已定,v5 焦点在提取头/信号形态,非价格源 —— 通常不需)
  - source: glob discussion/009/M1-price-data-source-research.md
- [ ] `discussion/009/ACCEPTED.md`(forge v1+v2 接受记录 + ⏸ 挂起项)
  - type: stage-doc(接受/挂起记录)
  - reachable: ✅
  - default: ☐ unchecked(挂起项索引 · full-history 才勾)
  - source: glob discussion/009/ACCEPTED.md

### Starting-point quick-pick groups

> repeat-forge 语义:pure-idea = proposal + 外部资产;from-prior-forge = + 最近 verdict(v4)
> + 现 PRD + 决议日志(v5 default 推荐,因为 v5 是在已收敛 v1-v4 基础上做事实修正);
> full-history = 全部 prior forge stage + 挂起 + 调研。

- **[Bundle:pure-idea]**(总是显示)
  - X 数量:4
  - pre-checked:
    - proposal-text(§想法+我为什么+闭环的灵魂+我的诉求)
    - /home/ys/codes/XenoDev/projects/004-pB(⚠ Codex 沙箱慎选)
    - /home/ys/codes/XenoDev/out/collection.db(⚠ 二进制/跨仓)
    - operator-input-2026-07-16-implicit-signals.md(v5 触发材料 —— 属"当前 idea 的一部分")
- **[Bundle:from-prior-forge]**(prior forge stage exists · **default 推荐**)
  - X 数量:7
  - pre-checked: pure-idea 全部 + `forge/v4/stage-forge-009-v4.md` + `009-pForge/PRD.md`
    + `handback/HANDBACK-LOG.md`
  - 理由:v5 是在 v1-v4 已收敛 + M1/M2 已 build 的现状上做**事实修正+路线重排**,
    专家必须看 v4 最近 verdict + 现 PRD 边界 + 07-07 被 supersede 的决议才能收敛。
- **[Bundle:full-history]**(任一 prior stage exists)
  - X 数量:12
  - pre-checked: from-prior-forge 全部 + `forge/v3` + `forge/v2` + `forge/v1` stage docs
    + `ACCEPTED.md` + `M1-price-data-source-research.md`
  - estimated_tokens: ~30k(≥ 8k → 主命令会软警告 · 见下方估算)
- **[Bundle:custom]**(总是显示 — human 自己挑)

## K seed (suggested, editable by user)

```
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
```

**Byte count**: ~3600 bytes(含 v5 事实修正段)
**Quality flag**: K seed 长度 >= 80 chars: ok(远超阈值)

## Z candidates (suggested if mode=对标指定列表)

无 —— proposal §009 **没有** `### 我已知的相邻方案/竞品` 段。Z mode 选"对标指定列表"时
由 human 手粘。

> 提示(仅供 human 参考,不代替 human 选定):若 v5 走 SOTA 对标,天然候选方向是
> "从非结构化文本/直播转写做**隐性信号提取/事件抽取**"的既有做法 + 回测端反过拟合纪律
> (DSR/PBO)—— 但这些**不是** proposal 明写的竞品,故不放进 Z candidates 字段,留白由
> human 决定。

## Y default recommendation

| Y 维度 | 默认 | 触发关键词 evidence |
|---|---|---|
| 产品价值 | ✅ | (always) |
| 架构设计 | ✅ | "闭环整体架构怎么搭 …… 四条想法怎么排期"(诉求 ① ③) |
| 工程纪律 | ✅ | "回测系统怎么作为两灵魂的公共地基先落地"(诉求 ③) |
| 安全 | ☐ | (无命中 —— proposal 无 安全/权限/密钥 词) |
| 教学价值 | ☐ | (无命中) |
| 商业可行 | ☐ | (无命中 —— proposal K 明确"自用单人,不商业化",反向排除) |
| 用户体验 | ☐ | (无命中) |

> **触发说明**:诉求 ① "闭环整体架构怎么搭" + ③ "回测系统作为公共地基先落地" 命中
> `框架/pipeline/方法论/流程/工程纪律` 类语义(架构+地基+排期=方法论/流程),按规则加
> **架构设计 + 工程纪律 + 产品价值** 三项。商业维度被 K binding④"不商业化"反向排除,不推荐。

## W default recommendation

| W 形态 | 默认 | 理由 |
|---|---|---|
| verdict-only | ✅ | (always) |
| decision-list | ✅ | (always — v5 有大量 keep/cut/new 待判:蒸馏头提前/M3' 重排/07-07 决议作废/两条红线) |
| next-PRD | ✅ | (always — K seed 足够 seed;且现 PRD 需按 v5 事实修正重排,天然产 next-PRD) |
| refactor-plan | ✅ | "各器官按补哪个短板重定位 …… 哪些复用、哪些重构"(诉求 ②,命中 重构/redesign 语义) |
| next-dev-plan | ✅ | "四条想法怎么排期 …… M3'/M4"(命中 phase/milestone/分阶段 —— PRD 是 phased M1/M2,v5 重排 M3') |
| free-essay | ☐ | (默认不勾) |

> **触发说明**:refactor-plan 命中诉求 ②"哪些复用、哪些重构"+"004/008 重定位";
> next-dev-plan 命中"四条想法怎么排期"+ 现 PRD phased(M1/M2)+ v5 要新增 M3'。

## Reachability check on all X paths

| Path | Reachable | Type | Note |
|---|---|---|---|
| /home/ys/codes/XenoDev/projects/004-pB | ✅(Glob 命中 9238 文件) | external-repo-dir | 跨仓 · `feat/009-spec` 分支 alpha 模块;Codex sandbox 可能 BLOCK 跨仓读 |
| /home/ys/codes/XenoDev/out/collection.db | ⚠ 存在但二进制(Read 拒 · Glob/存在性确认在) | external-file(binary) | 008 语料 9081 条;跨仓;建议附 .schema 文本快照供 Phase 1,不让沙箱读 .db |
| discussion/009/operator-input-2026-07-16-implicit-signals.md | ✅ | internal-file | v5 触发材料 · 高优先 |
| discussion/009/009-pForge/PRD.md | ✅ | internal-file | fork PRD · phased M1/M2 · complete |
| discussion/009/handback/HANDBACK-LOG.md | ✅ | internal-file | 21 决议 · 含 07-07 被 supersede 决议 |
| discussion/009/forge/v4/stage-forge-009-v4.md | ✅ | internal-file | prior verdict · 最近 |
| discussion/009/forge/v3/stage-forge-009-v3.md | ✅ | internal-file | prior verdict |
| discussion/009/forge/v2/stage-forge-009-v2.md | ✅ | internal-file | prior verdict · 蓝图 |
| discussion/009/forge/v1/stage-forge-009-v1.md | ✅ | internal-file | prior verdict · 奠基 |
| discussion/009/M1-price-data-source-research.md | ✅ | internal-file | 专题调研(已进 PRD 附录 A) |
| discussion/009/ACCEPTED.md | ✅ | internal-file | 接受/挂起记录 |

## Token estimate (for full-history soft-warning)

| X 候选 | chars | ≈ tokens |
|---|---|---|
| proposal-text | ~2050 | ~0.7k |
| 004-pB(external-repo-dir) | unknown | 5k(兜底) |
| collection.db(external-binary) | unknown | 2k(兜底 · schema/规模元数据,不真读全库) |
| operator-input v5 材料 | ~4900 | ~1.6k |
| 009-pForge/PRD.md | ~13000 | ~4.4k |
| HANDBACK-LOG.md(21 决议) | ~估 ≥ 20000 | ~7k(兜底估) |
| forge/v4 stage | ~估 4000 | ~1.3k |
| forge/v3 stage | ~估 3000 | ~1k |
| forge/v2 stage | ~估 8000 | ~2.7k |
| forge/v1 stage | ~估 8000 | ~2.7k |
| ACCEPTED.md | ~估 3000 | ~1k |
| M1-research.md | ~估 4000 | ~1.3k |

**estimated_tokens_full_history: ~30k**(远 ≥ 8k → 主命令在 full-history 会软警告)

> ⚠ full-history 含 21 决议 HANDBACK-LOG + 4 版 prior forge stage + 2 个 external 跨仓资产,
> 体量大且部分需沙箱慎读。**推荐 default = from-prior-forge(~19k 含外部兜底)**;若不含
> 外部资产的 from-prior-forge 内文约 ~11k,仍偏重但可接受。human 若只想聚焦 v5 事实修正,
> 可用 custom 只勾:operator-input(v5) + PRD + v4 stage + HANDBACK 的 07-07 决议段。

## Quality flags

- [x] proposal section detected:✅
- [x] ≥1 X candidate extracted:✅(11 条:2 external + 9 internal + proposal-text)
- [x] K seed ≥ 80 chars:✅(~3600 bytes)
- [x] At least 1 Y default recommended:✅(产品价值/架构设计/工程纪律)
- [x] At least 1 W default recommended:✅(verdict-only/decision-list/next-PRD/refactor-plan/next-dev-plan)

## Prefill summary(给主命令的简要)

```
prefill_status: success
draft_file: discussion/009/forge/v5/_prefill-draft.md
x_candidates: 11
k_seed_bytes: 3600
z_candidates_present: false
intermediate_products_found: [v5-trigger-doc, fork-PRD, HANDBACK-LOG, prior-forge-stage-v1, prior-forge-stage-v2, prior-forge-stage-v3, prior-forge-stage-v4, ACCEPTED, M1-research]
y_recommended: [产品价值, 架构设计, 工程纪律]
w_recommended: [verdict-only, decision-list, next-PRD, refactor-plan, next-dev-plan]
estimated_tokens_full_history: 30k
```
