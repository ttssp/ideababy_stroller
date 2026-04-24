# PRD · 001-pA · "PI Briefing Console"

**Version**: 1.0  (human-approved via fork)
**Created**: 2026-04-23T13:27:47Z
**Source**: discussion/001/L3/stage-L3-scope-001.md · Candidate A
**Approved by**: human moderator（通过 `/fork 001 from-L3 candidate-A as 001-pA` 确认）

---

## Problem / Context

AI 领域的 research 以每天数百篇 arXiv + 多家顶尖 lab blog + 大量 GitHub repo 的速度涌出，lab PI 与高频使用的 senior PhD/postdoc 都难以只凭个人阅读跟上。现有工具两头都不满足：**传统 paper list / newsletter**（Elicit、Semantic Scholar Feed）给的是论文堆叠，信号被淹没；**LLM 深搜工具**（Undermind 等）一次性给 report，但不帮助 lab 建立对一个 topic 的**持续判断**。

L2 §1 把核心买单场景收敛为 "给 AI lab PI 的外置研究编辑部"：PI 是经济 buyer（决策者 + 做 lab 方向建议的人），senior PhD/postdoc 是日常 operator（替 lab 做 triage）。L3R0 intake 确认双 persona 都必须被 serve，PI 优先。

v0.1 必须**诚实承认无法同时满足"更快 + 更独特 + 更精致"三项**，选择 **Speed + Differentiation 并存、Polish 主动放弃** 的组合 —— 把 "digest-by-state-shift" 与 "可剪枝 breadcrumb resurface" 两条 novelty bet 做对，其余留到 v0.2+。

核心 bet：当 briefing 不是按论文堆叠、而是按 **state shift**（本 topic 今天发生了什么变化）组织，并且每篇新工作都能走 4-action（read now / read later / skip / breadcrumb）留痕、低价值留痕在未来被 resurface —— 那么 PI 每天 10 分钟 Web briefing 能真正做到 "不漏看"，operator 的 triage 劳动能 compound 成 lab 的长期资产。

## Users

### 主 persona — Dr. Chen 类型 PI（经济 buyer + 决策者）

- **角色**：AI lab PI，带 5–15 人团队，lab 覆盖 8–15 个 topic（e.g. RLHF、efficient attention、multi-modal reasoning、mechanistic interp、inference-time compute…）
- **痛**：每周要给学生做方向建议；最怕"漏看一篇 next week 会被学生问住的文章"；读 Elicit / Semantic Scholar Feed 得到的是"一堆论文" —— 真正需要的是 "**本 topic 今天发生了什么变化**" 的 briefing
- **使用节奏**：每天 8:00 打开 Web briefing，10 分钟扫完 8–15 topic 的 state 摘要，确定今天要深入哪 1–2 个 shift；周会前用 breadcrumb resurface 回看过去 90 天
- **买单逻辑**：他为"省时间 + 更清楚"付钱，但**真正 compound 的价值** 需要 3–6 个月才显现（breadcrumb 累积 → day-45 之后 resurface aha）
- **重心指引**：产品设计以 PI 的使用节奏为先（digest-first、无 sidebar、一键进入今日 state shifts）

### 次 persona — Maya 类型 senior PhD / postdoc（高频 operator）

- **角色**：lab 里最勤奋的 operator；PI 把日常 paper triage 委托给 her；她替 lab 做一轮初步判断再把 "值得看" 的推给 PI
- **痛**：每天读 20–50 篇 abstract；"好像看过、之后再也找不回" 是最高频的挫败
- **账号**：**独立 login + 独立 seat**（R2 修正点：不允许"共用 login"），轻量 invite by email token，≤ 15 用户
- **权限**：全员 read+write；admin（PI）专管 topic 池 CRUD；**不做 per-topic 可见性分层**（这是 v0.1 的有意简化 —— §"Open questions" Q5 记录）
- **使用方式**：对 briefing 里每一篇论文做 4-action + 可选一句 "why I disagree"（轻量 explicit taste signal，不是闭环 agent）

### 明确次要 / 降级的用户

- **Carol 类型 onboarding 场景**（刚加入 lab 的 junior，需要 tour）：v0.2+
- **lab 外部的 casual reader / newsletter subscriber**：非本产品受众
- **跨 lab federation 场景**：v0.1 不考虑

## Core user stories

1. 作为 **PI**，我每天 8:00 可以打开 Web briefing，10 分钟内看完 8–15 topic 的 state 摘要，**确定今天要深入哪 1–2 个 shift**。
2. 作为 **PI 或 operator**，我可以对 briefing 里每一篇论文做 4-action（`read now` / `read later` / `skip` / `breadcrumb`），系统记住该决策并在下次同类工作出现时体现。
3. 作为 **PI**，3 个月后我可以查 "过去 90 天我为哪些 topic 标过 breadcrumb、其中哪些现在被 resurface 了" —— 形成 "过去标过但可能要重看" 的列表。
4. 作为 **operator**，我可以对系统的 `skip` / `breadcrumb` 决策写一句 "why I disagree"（轻量 explicit taste signal，系统仅记录、不做反向影响 briefing 的闭环 agent）。
5. 作为 **PI**，我可以维护 8–15 个 topic 关注列表（关键词池 + arXiv category + 可选 seed author），任何时候 CRUD。
6. 作为 **任何 lab 成员**，我可以 JSON export 整套数据（包含 topic / paper / 我的 action 历史 / breadcrumb 记录）；数据库可自持（self-host Postgres/SQLite）。

## Scope IN (v0.1)

| # | Item | 说明 |
|---|------|------|
| IN-1 | **Topic 管理** | 8–15 topic，PI 手动 CRUD；每 topic = { 关键词池, arXiv category, 可选 seed author } |
| IN-2 | **每日 briefing（Web page）** | Digest-first；按 state shift 组织（不是论文堆叠）；每 topic 一行 state 摘要 + 至多 3 篇触发论文 |
| IN-3 | **4-action 标注** | `read now` / `read later` / `skip` / `breadcrumb`；每次可附一句自由文本 why |
| IN-4 | **Breadcrumb resurface** | 6 周 / 3 个月 / 6 个月分别重新 surface；带 "为什么现在又回来" 的上下文（系统解释触发条件）|
| IN-5 | **双 seat auth** | PI + operator 各自独立 login（email token invite，≤ 15 用户）；权限极简：全员 read+write，admin 管理 topic 池 |
| IN-6 | **Data portability** | JSON export 全量；数据库自持有（Postgres 或 SQLite；L4 早期决策）|
| IN-7 | **LLM 解读** | 仅基于 abstract + metadata 产出 ≤ 3 句 summary；不做 PDF 全文解析；summary 格式遵守红线 2（委托 triage ≠ 替代阅读）|

## Scope OUT (explicit non-goals)

| # | Item | 原因 |
|---|------|------|
| OUT-1 | **完整 Taste agent 闭环** | 只收集 explicit disagree，不做 hybrid agent 反向影响 briefing —— 延后 v0.2 |
| OUT-2 | **Topology graph / topic 关系图主视图** | digest-first 不需要它；强行做会冲淡首页价值 |
| OUT-3 | **Lab shared belief ledger / stance history** | 属 Candidate B 范畴 |
| OUT-4 | **Paper 二次分析 / novelty 自动评分 / 跨 paper 对比** | 会把产品推向 "做得不精的 Elicit"；守红线 2 |
| OUT-5 | **Mobile native / CLI / PWA** | Web only（Candidate C 才覆盖 PWA）|
| OUT-6 | **PDF 全文解析** | 仅用 abstract + metadata |
| OUT-7 | **Onboarding-focused view / Carol 场景** | 降级 v0.2 |
| OUT-8 | **公开打分 / 社区 review / 排行榜** | 硬红线 3（Paperstars 失败模式）|
| OUT-9 | **Billing / payment** | v0.1 先免费，预留 auth 不做 billing（intake Block 3）|
| OUT-10 | **Per-topic 可见性分层 / 细粒度权限** | 全员 read+write 是有意的简化；见 Open questions Q5 |
| OUT-11 | **跨 lab federation / 公开 radar** | 所有 data lab 内部 |

## Success — observable outcomes

| # | Outcome | 测量方式 / 窗口 |
|---|---------|-----------------|
| O1 | **PI 日活 ≥ 25/30** | 连续使用 30 天 —— 证明 briefing 成为 ritual 而非 newsletter |
| O2 | **PI 每月 ≥ 5 次 breadcrumb resurface 被实际点开** | 低价值留痕的价值被用户自己验证 |
| O3 | **Operator 每周 ≥ 2 次独立登入 briefing** | 第 4 周起测量 —— 独立 seat 不会死 |
| O4 | **PI 可以说出 ≥ 2 个 "没这工具会漏看" 的真实案例** | 30 天访谈 + day-60 breadcrumb aha window 访谈 |
| O5 | **Day-45–60 breadcrumb resurface 出现 aha** | 定性访谈；本项是决定 A→B 升级的 gate |

**Kill-window**: **60 天**（不是 30 天）。如果 60 天后 O1/O2/O5 均未达成，证明 "digest-by-state-shift + breadcrumb resurface" 这一对 core bet 错了 —— 回 L2 重新思考（不是 pivot 到 B；B 的前提假设已被 A 证伪则更不成立）。

## Real-world constraints

| # | Constraint | Source |
|---|------------|--------|
| C1 | **时间预算 ~20h/周，目标 v0.1 ~5 周（总 ~100h）** | L3R0 intake Block 1；Opus+GPT R2 合并中值 |
| C2 | **Platform = Web only**（无 mobile native、PWA、CLI） | L3R0 intake Block 4（软偏好）+ Candidate A 明确取舍 |
| C3 | **先免费，预留 auth 不做 billing** | L3R0 intake Block 3 |
| C4 | **双 persona 必须被 serve，但 PI 优先** | L3R0 intake Block 2 硬约束 |
| C5 | **Red line 1: 不扩成通用论文发现器** | L3R0 intake Block 5；守 8–15 topic 护城河 |
| C6 | **Red line 2: 不替代第一手阅读** | 同上；summary ≤ 3 句、skip 决策可追溯 |
| C7 | **Red line 3: v0.1 不做公开打分 / 社区 review** | 同上；所有数据 lab 内部 |
| C8 | **Data portability 是 v0.1 承诺** | L2 §6 的 6 条 conditions 之一（Mendeley 下线的教训）|
| C9 | **≤ 15 用户**（lab 边界） | Candidate A Scope IN 明确 |

## UX principles (tradeoff stances)

1. **Speed > Polish**：UI 粗糙可接受（表格 + 纯文本 briefing）；绝不为"好看"延后发布。
2. **Differentiation > Polish**：digest-by-state-shift + breadcrumb resurface 两条 core bet 必须做对；这两项失分比 UI 粗糙严重得多。
3. **PI 优先，operator 独立可用**：两 seat 都必须能登；但重心和 UI 节奏偏 PI 的 8:00 10 分钟 ritual。
4. **一个视图解决一件事**：首页 = digest；无 sidebar、无 modal；其他功能通过 URL 进入（`/topics`、`/breadcrumbs`、`/export`）。
5. **解释要可追溯**：每条 state 摘要必须能点进去看"这个 shift 是基于哪 3 篇论文"；每个 skip 可以看"我当时为什么 skip"。

## Biggest product risk

**PI 把 briefing 当成 newsletter 读一周然后放弃**。

Why：v0.1 没有完整 taste agent（operator 的 disagree 不会反向影响 briefing）、breadcrumb 第一个月还没累积足够信号可供 resurface、topology 这个 "wow moment" 也不存在。因此前 30 天 PI 得到的主要是"更好组织的 daily feed"，但**真正的 aha 要到 day-45–60 才来**。如果 PI 心理预期是 "30 天判定"，他会在 aha 之前放弃。

**Mitigation（写入 L4 计划）**：

- **陪跑 ≥ 10 次现场使用校准** —— day-30 必须亲自坐在 PI 旁边看他用 briefing 至少 10 次，校准 LLM 解读 / state shift 判定
- **Kill-window 显式设为 60 天**（不是 30）—— 在任何 progress check 文档里明确这一点，防止提前宣告失败
- **Day-45 访谈模板** —— 预先设计问题："过去 45 天有哪篇 paper 是因为 breadcrumb 才被你重新点开的？" 用事实回答决定升级 / kill

**次级 risk**：LLM 对 AI 前沿论文的 novelty / impact 判断质量不足以支撑 "briefing 不退化成 paper-list"。Mitigation：L4 早期做 2–3 天 LLM prompt spike，用 20 篇已人工标注过的 arXiv paper 做 blind 测试。

## Open questions for L4 / Operator

以下 ❓ 项来自 L3，未在 PRD 层面 resolve，需要在 L4 早期（spec 阶段前）确认：

| Q | 内容 | 建议默认 / 建议阶段 |
|---|------|---------------------|
| Q1 | **Data portability 的具体形态**（self-host / JSON export / open format 三选至少一） | 建议默认 "JSON export + 自持 Postgres/SQLite 二选一"（最轻量）；L4 spec 阶段定 |
| Q2 | **LLM provider 与 prompt 形态** | 建议 L4 早期 2–3 天 spike；用 20 篇人工标注过的 paper blind 测试；confidence 指标 ≥ 70% 才继续 |
| Q3 | **State shift 的判定规则**（什么算 shift vs. incremental） | L4 spec 阶段定义；建议最小启发式："过去 7 天内同 topic 出现 ≥ 2 篇引用同一早期工作且结论不同" |
| Q4 | **Breadcrumb resurface 的触发条件** | PRD 约定 6 周 / 3 个月 / 6 个月；但"某 topic 新工作引用了你曾 breadcrumb 过的论文"也应触发 —— L4 决定 |
| Q5 | **Per-topic 权限是否需要**（PI 不想某些 operator 看到某些 topic 的场景） | v0.1 默认"全员 read+write"；若实际 lab 出现政治摩擦，Scope-out 升级为 v0.2 需求；L4 不做 |
| Q6 | **获客 / dogfood 渠道** | PRD 假设至少 1 个 PI + 2 operator 可持续陪跑；如果真实 lab < 3 人或外部 lab 不参与，validation loop degenerate 为"自用" —— operator 在接 L4 前必须给出"陪跑名单（姓名 / 角色 / 时间承诺）" |

**Blocker 判定**：Q2 与 Q6 不解决则 L4 不启动 —— Q2 决定产品是否可能成立，Q6 决定验证循环是否可能闭合。

---

## PRD Source

This PRD was auto-generated from L3 fork. Contents are derived from the approved L3 candidate A. 完整 lineage 与跨候选对比：

- L3 menu: [discussion/001/L3/stage-L3-scope-001.md](../L3/stage-L3-scope-001.md)
- L3R0 intake（含硬约束原文）: [discussion/001/L3/L3R0-intake.md](../L3/L3R0-intake.md)
- L2 unpack（idea 的深度）: [discussion/001/L2/stage-L2-explore-001.md](../L2/stage-L2-explore-001.md)
- L1 menu（13 条灵感保留）: [discussion/001/L1/stage-L1-inspire.md](../L1/stage-L1-inspire.md)
- FORK-ORIGIN.md in this directory

This PRD is the **source of truth** for L4 (spec-writer). 任何改动必须由 operator 显式授权，L4 agents 不得私自重写产品决策。若 spec-writer 在 L4 早期发现 PRD 有**产品层面**缺陷，应停下来 escalate 到 operator，不得自行修订。

### A → B 升级路径（非 v0.1 承诺，仅记录）

若 60 天后：✅ PI 持续使用 + ✅ breadcrumb resurface 出现 aha + ✅ operator 愿意写 disagree ≥ 2 次/周 —— 此时操作员可 `/fork 001 from-L3 candidate-B as 001-pB` 并把本 PRD 的 scope 作为 B 的起点（~40–60% 可复用）。**此路径不在 v0.1 范围内**，此处仅为避免将来误判为"从 0 重建"。
