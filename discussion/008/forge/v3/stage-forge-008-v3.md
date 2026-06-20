# Forge Stage · 008 · v3 · "凭据隔离之下的受控自动翻页 · 分层 broker 架构"

**Generated**: 2026-06-20T03:10:00Z
**Source**: forge run v3 with X = 4 标的(IDS 本仓 2 + XenoDev 快照 2), Y = 架构设计/数据流边界 + 安全/凭据边界, Z = 对标 SOTA(架构/凭据层 · 不跑法律检索), W = verdict-only + decision-list + 协议修订草案 + next-PRD
**Convergence mode**: strong-converge
**Rounds completed**: P1 (both), P2 (both), P3R1 (both), P3R2 (both) — 共 8 份 round file
**Searches run**: 11 across 架构/凭据层多源(Opus P2 三次:credential broker/secretless · Playwright 认证会话隔离 · 分页失败模式;GPT P2 八次 / 六源可用)— **零法律/ToS/DMCA 检索**(Z binding 禁止)
**Moderator injections honored**: none(本 v 无 moderator-notes.md)
**Convergence outcome**: converged(双方 P3R2 §2 各为单一 GO verdict 且逐项同向;双方均显式标 "无 unresolved")

---

## How to read this

forge 是横切层(不是 L1-L4 pipeline 的一部分)。本文档是双专家(Opus 4.8 Max + GPT-5.5x High)
独立审阅 + 架构/凭据层 SOTA 对标 + 两轮联合收敛后的产出,**强制给出立场**(不是候选菜单 defer 给你拍板)。

读完后你应该:
- 知道双专家对「凭据隔离硬约束之下,自动翻页能力是否/如何落地」的最终 verdict(单一 GO · 分层架构)
- 能用 §"Evidence map" 把每条结论逐条溯源到具体 round file 段落
- 拿到四件套产物:§"Verdict rationale"(浓缩立场展开)、§"Decision matrix"(保留/调整/删除/新增 全景)、
  §"协议修订草案(SHARED-CONTRACT §2)"(§2 新增子条款的精确措辞)、§"Next-version PRD draft"(可回流改 PRD v1.2→v1.3 的采集架构 + C5 章节)
- 能基于 §"Decision menu" 直接进入下一步(改 §2 + 改 008-pB PRD + 回 XenoDev 起 L4 实装 / 跑 v4 / park / abandon)

> ⚠ **本 forge 审的是架构 + 凭据边界,不审【自动翻页对此顾问平台的合规性】**(operator 已拍板并担责,binding,沿用 v1/v2)。
> 全程未论证「自动翻页是否违法 / 踩 ToS / 规避访问控制 / DMCA」。**GO 不等于「合规」**——合规是 operator 的已决前提,不是 forge 的结论。
> 本 verdict 也**未审 broker/runner 的工程实装复杂度**(那是 L4/XenoDev 才能答的真风险,见 §"What this menu underweights")。

## Verdict

**GO(分层架构)** · 自动翻页能力**可在「登录态绝不进 agent context」硬约束之下落地**,形态 = **三层分离**:
**① 控制流层**:agent 只产可审计的 **declarative plan**(源 / 时间窗 / 端点集合 / 参数 schema / 最大请求预算 / 停止条件 / 落盘位置),**不持 key、不发请求**。
**② 执行基座层**:operator 一键授权后,**隔离的 capability-scoped credential broker/runner** 独占 operator 登录态(独占 userDataDir/storageState · agent 无文件读权 · 日志脱敏),**按端点/参数白名单**抓取并把内容＋分页 checkpoint 落盘 —— **绝非通用 HTTP 代理**(broker 不盲转发 agent 给的任意 URL)。
**③ 侦察兵/fallback 层**:agent 分析已落盘数据诊断列表缺口、把「盲滑」变「定向滑」。
**协议层**:SHARED-CONTRACT **§2 新增「采集会话凭据隔离」子条款**(协议级);**§1 PRD schema 不动**;**C5 OUT 侧渠道中性 keep,仅补一句 IN/OUT 边界说明**。确认粒度 = **每 bounded capture batch 一次**(六要素:源/时间窗/端点集/请求预算/停止条件/落盘位置)。**无 unresolved。**

> **显式回应 K**:K#1(持 key 主体怎么设/信任边界划哪)→ 持 key 主体 = 隔离 broker/runner,边界 = 「agent 产意图 vs broker 持凭据并执行」二者不互穿,broker 端点白名单是防 agent 滥用持 key 进程的核心闸;K#2(3 候选向选哪/怎么混)→ 不是三选一,是 ③控制流 + ②broker 基座 + ①侦察兵 分层组合;K#3(是否触及 §1/§2 协议层措辞修订 + 改动边界)→ 触及 §2(新增采集会话凭据隔离子条款 · 协议级),§1 不动,改动边界精确到「§2件1 后加一段」(见 §"协议修订草案")。

## Evidence map

| 结论 | 来源 | 引用(≤15 words) | 是否有反对证据 |
|---|---|---|---|
| 当前半自动「被动性即隔离」是凭据安全地基 | P1-Opus §1A | "agent 物理上不经手登录态…被动性即隔离" | - |
| 自动翻页=主动发请求,必须持登录态,引入当前不存在的新主体 | P1-Opus §1A / P1-GPT §1 架构 | "翻页=主动发请求…必须持有效登录态" | - |
| §2件1 字面只到 deployment secret,不含采集会话 cookie | P1-Opus §1B / P1-GPT §1 安全 / 快照 line 169-184 | "成文 scope 是 .env.production…字面没说采集 cookie" | - |
| 三候选不是三选一,是一条管线的分层组合 | P1-GPT §2 / P2-Opus §3 / P2-GPT §3 | "同一能力的不同控制面" | ⚠ Opus P1 §2/§3 初判倾向③一次性 runner + 对②保留 → P2 被 SOTA 收回(见 underweight) |
| credential broker / secretless 是成熟工业范式(非新发明) | P2-Opus §1 row1 / P2-GPT §1 row1-2 | "agent 完成工作而从不读取底层凭据" | - |
| broker 必须 capability-scoped 端点白名单,非通用 HTTP 代理 | P2-GPT §2 / §3 / P2-Opus §1 row2 / P3R1-Opus §1 | "盲转发任意 URL=只是把 key 从 agent 挪到代理" | - |
| Playwright persistent context 是认证会话隔离候选(非强制) | P2-Opus §1 row3 / P2-GPT §1 row3 | "runner 独占 userDataDir/storageState" | - |
| 分页无内建增量,须 checkpoint 落盘(接 v0.1 C7 不静默丢) | P2-Opus §1 row4 / P2-GPT §1 row4-5 / P3R1-Opus §1 | "没有内建增量机制…checkpoint/dedup 须自己设计" | - |
| 列表截断 2025-07-21 根因未知 → 条件分支兜(主路径翻页 / 分支 detail 批量发现) | P1-Opus §3#1 / P2-Opus §3 残留 / P3R1 双方 | "分页未尽 vs API 物理截断…须实战数据" | ⚠ 全程未实测的外部未知(非 reviewer 分歧 · 见 underweight) |
| 确认粒度 = 每 bounded capture batch 一次(六要素) | P3R1-GPT §2 / P3R2 双方 §1 | "每个 bounded capture batch 一次确认,不是每页" | - |
| §2 子条款层级 = 协议级(对所有未来采集类项目生效) | P3R2-GPT §3 W3 / P3R2-Opus §3 note-4 | "适用于所有未来采集类项目" | ⚠ Opus note-4 标 operator 可改判项目级(见 underweight) |
| C5 OUT 侧渠道中性 keep,只补一句 IN/OUT 边界 | P3R1 双方 §2 / P3R2 双方 §2 | "C5 OUT 侧渠道中性 keep,只补 IN/OUT 边界说明" | - |

(上表 12 行,挑了最 load-bearing 的;其余次级结论散见各 round §1/§2/§3。)

## Intake recap

### X · 审阅标的(4 个)
**IDS 本仓(✅ 可达):**
- `discussion/008/008-pB/PRD.md` —— 现行 PRD **v1.2**(C5:166 渠道中性 / 采集架构 / v0.1 半自动被动监听落点)。类型:本仓库文件。⚠ operator intake 写「v1.1」,实际基线是 forge v2 已 bump 的 **v1.2**。
- `discussion/008/forge/v2/stage-forge-008-v2.md` —— forge v2 verdict(C5 渠道中性原则定基线 · OUT 侧)。类型:stage 文档。

**XenoDev 快照(✅ 已拷进 `_external/`,两审阅人读同一份):**
- `_external/XENODEV-dogfood-backlog-autopage-entry.md` —— 议题主源(实战边界硬证据:列表止于 2025-07-21 / 2026 仅 detail 可达 + 3 候选决议向)。
- `_external/XENODEV-SHARED-CONTRACT-s1-s2.md` —— SHARED-CONTRACT §1(PRD schema)+ §2(Safety Floor 三件套 · 被本议题挑战的硬约束源)。

### Y · 审阅视角
- ✅ **架构设计 / 数据流边界**(本轮主轴)—— 持 operator 登录态发请求的主体怎么设、信任边界划哪;daemon↔agent 落盘接口怎么定;自动化程度 vs 信任边界清晰度的取舍。
- ✅ **安全 / 凭据边界**(本轮主轴)—— 「登录态绝不进 agent context」在自动翻页下怎么保;agent 不持 key/不直接发请求的可验证保证;持 key 主体的最小权限边界。
- ⚠ **binding**:自动翻页的【合规性】由 operator 拍板担责,**非本轮审议对象**;只审架构与凭据边界。

### Z · 参照系
- mode: **对标 SOTA**(架构 / 凭据边界层)
- 用户外部材料:已快照的两份 XenoDev 文档(议题主源 backlog + SHARED-CONTRACT §1+§2)
- Phase 2 检索受控采集 / 凭据隔离架构 prior-art:credential broker / secretless · 浏览器自动化认证会话隔离 · 自动翻页失败模式。**不跑法律检索**(执行一致:双方 P2 零法律/ToS/DMCA 检索)

### W · 产出形态(交叉验证下方 W-shape 章节齐整)
- ✅ **verdict-only**(浓缩 verdict + 简短 rationale ≤500 字)
- ✅ **decision-list**(4 列矩阵:保留/调整/删除/新增)
- ✅ **协议修订草案**(对应 K#3:SHARED-CONTRACT §2 新增子条款的精确措辞 + 层级选择 + §1 不改理由)
- ✅ **next-PRD**(采集架构 + C5 章节的下一版草案,可回流改 008-pB PRD v1.2→v1.3)

### K · 用户判准
> **核心问题**:实战采集「2026 起全历史库」暴露 —— 列表接口止于 2025-07-21,2026 内容仅逐篇点 detail 可达,operator 手动找历史入口成本高。operator 要求引入「自动翻页」补齐历史。**在不违反凭据隔离(登录态绝不进 agent context · non-overridable)的前提下,这个能力是否/如何落地?**
>
> **binding 前提(双专家不得审议)**:① 自动翻页【合规性】由 operator 拍板并担责(不审是否违法/踩 ToS/规避访问控制);② 凭据隔离 non-overridable,不论证放宽,只论「在它之下怎么做」;③ v0.1/v0.2 已 ship 不重审。
>
> **operator 最在乎的(架构/数据流层)**:1. 持 key 主体怎么设、信任边界划哪;2. 3 候选架构向(①半自动+侦察兵 / ②独立 daemon 持 key / ③agent 出计划+一键确认+持 key 进程执行)选哪个/怎么混;3. 是否触及 SHARED-CONTRACT §1+§2 协议层措辞修订,改动边界是什么。

### 收敛模式
**strong-converge** —— 必须 finalize 单一 verdict。残余分歧降级为 note。沿用 v1/v2 收敛强度。

---

## §"Verdict rationale"(W: verdict-only)

展开 §"Verdict" 的论证,逐条引 evidence:

**为什么不是三选一,而是分层组合。** P1 双盲两轮后在结构层完全收敛:GPT P1 §2 把三候选框成「同一能力的不同控制面」(侦察兵发现缺口 / 计划层给最小请求集 / 持 key 层实际抓取 / 落盘层供只读消费);Opus P2 §3 在 SOTA 印证下**收回了 P1 对②常驻 daemon 的保留**,承认「②和③不是对立选项,是一条管线的不同层」。最终形态 = ③控制流 + ②broker 基座 + ①侦察兵,三者各司一层。

**为什么持 key 主体可以是独立程序而非「人」。** SOTA 给出工业范式名字:CyberArk Secretless Broker / HashiCorp Vault Agent sidecar / Infisical AI-agent credential brokering 把「常驻持 key 进程」做成**标准安全姿态**(localhost-only、最小 scope、短期凭据),证明「持 key 主体独立、agent 永不见 key」不是新发明(P2-Opus §1 row1 / P2-GPT §1 row1-2)。把「被动性即隔离」从「operator 手动浏览」平移到「runner 持隔离会话翻页」,隔离性质可保留,但信任主体从人变成程序——这是质变,须协议层兜(P1-Opus §2)。

**核心安全闸:broker 不是通用 HTTP 代理。** GPT P2 §2 的 load-bearing 反驳:「broker/sidecar 并不天然安全——若只是把 agent 给的任意 URL 加 cookie 转发,那只是把 key 从 agent context 移到一个可被 agent 滥用的代理里」。这直接接上双方 P1 §3 的共同担忧「agent 不持 key 易,agent 不能滥用持 key 进程难」。SOTA 答案(Secretless connector / Vault Agent / MCP capability control,P2-GPT §1 row6)= broker 对**端点/参数白名单**校验,agent 的意图须落在预定义端点集。**这是协议修订草案必须钉的核心机制。**

**为什么 checkpoint 落盘是硬要求。** 分页 SOTA 铁律:「没有内建增量机制,checkpoint/dedup 须自己设计;offset 在数据变动时会漏会重」(P2-Opus §1 row4 / P2-GPT §1 row4-5)。分页须落盘 cursor/页边界/重试来源供 agent 只读审计,否则 silent drift——这恰好对齐 v0.1 既有护栏 **C7「不静默丢」**(P3R1-Opus §1),把抽象凭据边界接回 v0.1 既有护栏。

## §"Decision matrix"(W: decision-list)

针对 008 采集架构现状,4 列矩阵。每行可在 §"Evidence map" 溯源。

| 类别 | 项 | 来源(标的具体位置) | 理由 | 优先级 |
|---|---|---|---|---|
| **保留** | 半自动被动监听采集架构(默认路径) | 008-pB PRD §采集架构 + L4 既有 `src/capture/addon.py` | 「被动性即隔离」是凭据安全地基,已可达内容仍走它(P1-Opus §1A) | P0 |
| **保留** | ①侦察兵/fallback 层 | 候选① | agent 分析落盘指方向、把盲滑变定向滑;列表 API 够得到时降 operator 成本(P1-Opus §2) | P1 |
| **保留** | C5 OUT 侧渠道中性原则 | PRD C5:166 / v2 stage | IN 侧采集手段扩展不松动 OUT 侧任何约束(P1-Opus §1C) | P0 |
| **保留** | SHARED-CONTRACT §1 PRD schema | 快照 §1 | 不需新增字段(P3R1 双方 / 快照 §1) | P0 |
| **保留** | v0.1 三护栏(C7 不静默丢等) | PRD C7:168 | checkpoint 落盘对齐 C7,接它而不改它(P3R1-Opus §1) | P0 |
| **调整** | 候选② 从「daemon 自动翻页」重述为「capability-scoped 白名单 broker/runner」 | 候选② / P2-GPT §3 | ②不是「全自动常驻产品形态」,是受控持 key 执行基座(P2-Opus §3) | P0 |
| **调整** | 候选③ 从「单次脚本」重述为「bounded-batch 控制流」 | 候选③ / P3R2-GPT §4 | agent 出 declarative plan,每 batch 一次授权(P3R1-GPT §2) | P0 |
| **调整** | C5 补一句 IN/OUT 边界说明 | PRD C5:166 | 钉死「IN 侧采集手段扩展 vs OUT 侧传播」是两件正交事(P1-Opus §1C) | P1 |
| **删除** | ② 作「无确认全自动常驻翻页产品形态」出局 | 候选② 全自动解读 | 全自动会把确认/限速/scope/审计后移成隐患(P1-GPT §2) | P0 |
| **删除** | broker 作通用 HTTP 代理 / 盲转发任意 URL 的任何形态出局 | P2-GPT §2 | 盲转发=只是把 key 挪到可被 agent 滥用的代理(P2-GPT §2) | P0 |
| **删除** | agent 持 key / 直接发请求 / 凭据 session 文件进 agent 可读路径 | K binding | 违反「登录态绝不进 agent context」硬约束(K binding) | P0 |
| **删除** | 无预算/无停止条件的开放式翻页 | P3R2-GPT §4 | 必须有最大请求预算 + 停止条件(P2-GPT §1 row6) | P0 |
| **新增** | §2「采集会话凭据隔离」子条款(协议级) | (新建议) | 把隐式/外推约束显式成文,给自动翻页成文依据(P1-Opus §1B + SOTA) | P0 |
| **新增** | broker 端点/参数白名单闸 | (新建议) | 防 agent 滥用持 key 进程的核心机制(P2-GPT §3) | P0 |
| **新增** | 分页 checkpoint 落盘(cursor/页边界/重试来源,接 C7) | (新建议) | 防 silent drift,对齐 v0.1 C7(P2-Opus §1 row4 / P3R1-Opus §1) | P0 |
| **新增** | bounded-capture-batch 六要素确认判准 | (新建议) | 每批确认一次,可量化 operator 介入,不破 O5b(P3R2 双方 §1) | P0 |
| **新增** | 定时任务须 operator 预授权固定 schedule/budget/kill-switch | (新建议) | agent 不得临时扩大授权(P3R1-GPT §2) | P1 |
| **新增/L4** | 速率/源白名单的具体数值 | (新建议) | 结构要求本轮定(plan 须含最大请求预算+停止条件),数值属 L4+operator 调参(P3R2-Opus note-3) | P2 |

---

## §"协议修订草案(SHARED-CONTRACT §2)"(W: 协议修订草案 · 对应 K#3)

### 当前缺口
SHARED-CONTRACT §2件1(Production credential 物理隔离)成文 scope 是 `.env.production` / `secrets/production/*` / `prod://` 连接串 / KMS 注入的运行时凭据(快照 line 169-184 原文实读),针对**部署/生产密钥**,防的是「Cursor 9 秒删库」那类把 prod 凭据喂进 agent 的事故。**它字面不含「顾问平台采集会话登录态 cookie/token/storageState」**(P1-Opus §1B / P1-GPT §1 安全 / 快照 ORCHESTRATOR NOTE 自陈)。K 里「登录态绝不进 agent context」是 §2件1 在采集域的**合理外推**,但**不是被一条现成条款挡住的**。自动翻页引入「持 operator 登录态主动发请求」的新主体后,这道 written-constraint 空白须显式化为成文条款。

### 层级选择:协议级(SHARED-CONTRACT)· 推荐
双方 P3R2 一致建议写进 SHARED-CONTRACT §2(对所有未来 XenoDev 采集类项目生效),理由 = 该边界适用于所有未来采集类项目(P3R2-GPT §3 W3 / P3R2-Opus note-4)。**operator 决策点**:若只想要项目级(仅 008-pB PRD/spec),退为 PRD 约束——下次别的采集项目撞同样问题须再补(P1-Opus §3#3 / P3R2-Opus note-4)。⚠ 见 §"What this menu underweights":升协议级是基于单一采集样本的外推。

### 新增子条款措辞草案(建议加在 §2件1 之后)
> **采集会话凭据隔离(件1 子条款)**:任何代表 operator 已认证会话发起采集请求的 cookie / token / storageState / userDataDir 等**运行时采集凭据,不得进入 agent context**。若需主动采集(如自动翻页),持凭据主体必须是**独立 broker/runner**,与 agent **物理隔离**(独占凭据/会话目录,agent 无文件读权,日志默认脱敏);**agent 只能提交 declarative plan**(源 / 端点集合 / 参数 schema / 请求预算 / 停止条件 / 落盘位置),**不持 key、不直接发请求**。broker/runner 必须是 **capability-scoped 连接器**:执行**端点/参数白名单**、请求预算、停止条件,**不得作为通用 HTTP 代理盲转发** agent 给的任意 URL。抓取须 **checkpoint 落盘可审计**(cursor / 页边界 / 重试来源,对齐 C7 不静默丢)。operator 授权粒度 = **每 bounded capture batch 一次**(六要素:源/时间窗/端点集/请求预算/停止条件/落盘位置);定时任务须 operator 预授权的固定 schedule/budget/kill-switch,**agent 不得临时扩大**。

(整合自:GPT P3R2 line 42-44 完整子条款文字 + Opus P3R2 §4 W3 五项覆盖清单 (a)-(e)。)

### §1 不改 + 理由
**§1 PRD schema 不动**:本轮变更不引入新 PRD 字段(采集架构变更落 PRD body + Scope IN/OUT,不改 schema 的 8 字段结构),且 §1 是 PRD↔spec 转换的字段约定,与运行时凭据边界正交(P3R1 双方 / 快照 §1)。

---

## §"Next-version PRD draft"(W: next-PRD · 回流改 008-pB PRD v1.2→v1.3)

> ⚠ **回流定位**:008-pB 早过 L3(PRD 已 v1.2),本轮**不是 fork 新 PRD branch**,而是像 v1.1/v1.2 那样**由 forge verdict 驱动现行 PRD 小幅修订**(采集架构 + C5 章节),非走 `/scope-inject`。以下是建议增补/改写的章节草案,可直接落回 `discussion/008/008-pB/PRD.md`。

**Status**: Draft from forge v3, awaiting human approval
**Sources**: forge stage-forge-008-v3.md + SHARED-CONTRACT §2 修订草案

### 改 1 · Scope IN(新增 v0.2+ 受控自动翻页)
建议在 `Scope IN — v0.2` 增补一段:
> **受控自动翻页(补齐历史库 · 分层采集架构)**:采集面从「半自动被动监听」扩到「受控自动翻页」,补齐 addon 被动监听够不到的历史列表页(实战暴露:列表接口止于 2025-07-21,2026 内容仅逐篇 detail 可达)。形态 = **分层架构**:agent 生成 bounded capture batch plan(源 / 时间窗/目标范围 / 端点集 / 参数 schema / 请求预算 / 停止条件 / 落盘位置)→ operator 确认 → 隔离 broker/runner 用 operator 登录态执行 → agent **不持 key、不发请求、只读落盘结果与脱敏 checkpoint**。半自动被动监听对已可达内容**仍保留为默认路径**。

### 改 2 · Scope OUT(v0.2 OUT 增补)
建议在 `v0.2 OUT 增补` 加三条:
> - ❌ **agent 直接持登录态 / 发请求 / 读 broker 的会话凭据文件**(红线 —— 登录态只在隔离 broker/runner,见 §2 采集会话凭据隔离子条款)。
> - ❌ **broker 作通用 HTTP 代理 / 盲转发 agent 给的任意 URL**(红线 —— broker 必须 capability-scoped 端点白名单)。
> - ❌ **无请求预算 / 无停止条件的开放式翻页 · agent 临时扩大定时任务授权**(红线 —— 定时任务须 operator 预授权固定 schedule/budget/kill-switch)。

### 改 3 · C5 追加一句 IN/OUT 边界(C5 原义不改)
建议在 C5 渠道中性原则块追加:
> C5 渠道中性约束管的是采集**后**的 OUT 侧传播/同步;**自动翻页属 IN 侧采集手段**,仅限 operator 有权访问内容,且采集会话凭据不得进入 agent context。IN 侧采集面扩展**不松动** OUT 侧任何约束(原文/转录/视频/签名 URL 仍永久 OUT)。

### 改 4 · 新增 v0.2 outcome(可选 · 对齐分层架构验收)
建议加 O11:
> | O11 | (forge v3) 自动翻页全程 **agent 无 key/无直接请求**:broker 独占会话目录 agent 无读权 · 抓取仅命中端点白名单 · checkpoint 可审计无 silent drift | 抽查 agent 进程无凭据访问;broker 日志命中白名单端点;制造一次漏页确认可检出(对齐 C7) |

### Open questions(forge 也没解决的)
- 列表截断 2025-07-21 根因(分页未尽 vs API 物理截断)须 L4 实装前一次实测确认(看响应有无 `has_more`/`next_cursor`、offset 越界返回空 vs 报错)→ 决定主路径(翻页)vs 条件分支(detail 入口批量发现)。
- broker/runner 的认证会话隔离实装手段(Playwright persistent context 等)是 L4 选型,本 forge 只给候选未定。
- 请求预算/速率上限的具体数值属 L4 + operator 调参。

---

## What this menu underweights(强制自批判)

诚实表述本 stage 文档可能 underweight 的点。这是质量栏,不能跳过。

- **反对证据未充分整合 ①(②的定位反转)**:Opus P1 §2/§3 初判倾向「③一次性 runner 为主、②常驻 daemon 持保留」,认为常驻持 key 进程攻击面/生命周期/被诱导发请求是更重负担。该立场在 P2 被 SOTA(credential broker/sidecar 把常驻持 key 进程做成标准安全姿态)**部分推翻**并收敛为分层组合。主 verdict 采纳收敛结果,但 Opus 原始担忧「broker 生命周期管理 + 被诱导执行」**并未消失**,只是被「capability 白名单闸」回应——若 L4 白名单实装不严,这条担忧会重新成立。

- **外部未知未实测(列表截断根因 · load-bearing)**:列表止于 2025-07-21 的根因(分页 cursor 未续 vs 列表 API 服务端物理不返回 2026)是 verdict **全程未实测的外部未知**,双方一致用条件分支兜(主路径翻页 / 分支 detail 批量发现,凭据边界不变仅换端点白名单)。**但若实测发现第三种情况**(如需登录态轮换 / 风控验证码 / 反爬挑战),现有二分条件分支**可能不够**,须回 forge 重评 broker connector 设计。

- **broker/runner 认证会话隔离实装复杂度未评估**:Playwright persistent context / storageState / 独立 userDataDir 是 SOTA 给的**候选**(非强制,P3R2-Opus note-2),本 forge 只给候选未定。「runner 独占会话目录 + agent 无文件读权 + 日志脱敏」在目标机器上**能否可验证落地**(而非流程承诺)是 GPT P1 §3#1 标的开放问题,实装复杂度未评估——这是 L4/XenoDev 的真风险。

- **§2 协议级子条款基于单一样本外推**:把「采集会话凭据隔离」写进 SHARED-CONTRACT §2(协议级硬约束)会对**所有未来 XenoDev 采集类项目**生效,但本 forge 的 X 标的只有 008 一个采集场景。双方都倾向协议级(收益:以后所有采集项目受益),但这是**基于单一采集样本把约束升为协议级硬约束**的外推。若 operator 担心过早固化,可选项目级(仅 008-pB),代价是下次别的采集项目须再补——这是 operator attention 点,见 §"协议修订草案"层级选择。

- **convergence_mode 副作用(双模型回声室)**:strong-converge + 双方 P1 双盲即高度同向(都独立落③控制流),P2/P3 几乎无分歧消解过程。好处是 verdict 锐利,但**双盲一致也可能是两模型共享同一盲区**——例如「declarative plan 模式真能完全杜绝 agent 通过构造 plan 间接影响 broker 行为」这一假设,双方都接受了「白名单闸足够」,无人从对立面压力测试。真实红队/实装可能暴露 plan 注入面。

- **forge versioning 提示(什么新信息触发 v4)**:① 实测列表根因发现条件分支不足(出现第三种截断情况);② L4 实装发现分层 broker 在 operator 单人本地场景**过重**(over-engineering 信号 —— 单人自用是否真需要工业级 broker,还是一个受限脚本足矣);③ §2 协议级子条款被别的 XenoDev 采集项目实践证否(发现该约束不普适)。

## Decision menu(for human)

### [A] 接受 verdict · 三处回流(协议层 + PRD + 回 XenoDev 起 L4)
本 verdict 回流的是**协议层(SHARED-CONTRACT §2)+ 008-pB PRD 采集架构/C5 小幅修订**,不是 fork 新 PRD branch(008-pB 早过 L3,PRD 已 v1.2)。像 v1.1/v1.2 那样 **forge verdict 驱动 PRD 修订**,而非走 `/scope-inject`。三步:
```
① 改 SHARED-CONTRACT §2(跨仓 · XenoDev 仓):
   - 把本 stage §"协议修订草案" 的「采集会话凭据隔离」子条款加到
     /Users/admin/codes/XenoDev/framework/SHARED-CONTRACT.md §2件1 之后
   - 层级 = 协议级(双方推荐);若 operator 改判项目级则跳过此步,只做 ②
   - ⚠ SHARED-CONTRACT 物理在 XenoDev 仓,改它须在 XenoDev session 做

② 改 008-pB PRD v1.2 → v1.3(本仓 · IDS):
   - 把本 stage §"Next-version PRD draft" 的改 1~改 4 落回
     discussion/008/008-pB/PRD.md(Scope IN/OUT + C5 + O11)
   - frontmatter bump v1.2→v1.3 + 加 forge v3 修订记录块(仿 v1.1/v1.2 体例)

③ 回 XenoDev 按分层架构起 L4 实装:
   - 新开 XenoDev session(cd /Users/admin/codes/XenoDev && claude)
   - 按 ③控制流 + ②broker 基座 + ①侦察兵 拆 spec/task
   - L4 实装前先做一次列表截断根因实测(定主路径 vs detail 分支)
```
⚠ 本选项**不走** `/plan-start` 新 fork 流程(008-pB 已有 L4 路径)。

### [B] 跑 forge v4(说明需要补什么)
```
/expert-forge 008
# 在 Phase 0 intake 时调整 X / Y / Z / W / K
# 旧 v3 整目录保留作历史参考
```
适用:三种新信息进入时——① 实测列表根因发现条件分支不足(第三种截断情况);② L4 实装发现分层 broker 在单人本地场景过重(over-engineering 信号);③ §2 协议级子条款被别的采集项目实践证否。

### [C] 局部接受
列出哪几条采纳、哪几条挂起:
- ✅ 采纳(建议):①控制流 + ②broker 基座 + ①侦察兵分层架构 / broker 端点白名单闸 / checkpoint 落盘 / bounded-batch 六要素确认
- ⏸ 挂起(等条件):§2 子条款**层级**(协议级 vs 项目级)——若 operator 暂不确定是否普适,可先落项目级(只改 008-pB PRD),待第二个采集项目出现再升协议级
- ❌ 拒绝(理由):如认为分层 broker 对单人本地过重 → 退到「仅 ①侦察兵 + 维持半自动」,但须接受「列表截断的 2026 历史补不齐」(侦察兵够不到列表 API 物理截断的内容)

### [P] Park
```
/park 008
```
保留所有 forge 产物,标记为暂停。复活时不重做这一层。

### [Z] Abandon
```
/abandon 008
```
forge verdict 显示该议题不该继续做。归档 lesson 文档。(注:本 verdict = GO,abandon 仅在 operator 重新评估「自动翻页诉求本身」时适用。)

---

## Forge log
(由 /expert-forge 命令更新;记录每次 forge run 的 v 序列 + 关键 verdict 一句话)

- v3: 2026-06-20 — verdict: "GO(分层架构)· agent 出可审计 declarative plan → operator bounded-batch 授权 → 隔离 capability-scoped broker/runner 按端点白名单抓取并 checkpoint 落盘 → agent 只读结果;§2 补采集会话凭据隔离子条款(协议级),§1/C5 不动"
- v2: 2026-06-16 — verdict: "GO · Obsidian 作 US8 载体 + 库→vault 单向 exporter + C5 渠道中性边界"
- v1: 2026-06-05 — verdict: "refactor-and-reset · C5 措辞重写 + 回放 scope 复位 + 探针判准改向自动化稳定性"
