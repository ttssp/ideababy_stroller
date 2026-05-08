---
forge_id: 006
forge_version: v1
doc_type: next-steps-plan
generated: 2026-05-08
upstream: stage-forge-006-v1.md
status: awaiting-execution
total_effort: ~3 工作日(纯文档,零代码)
---

# Forge 006 v1 · 下一步 5 件事(带依据溯源)

## 本文档定位

本文档是 forge stage-forge-006-v1.md verdict 落地的**第一阶段计划**。verdict 是"分级 harness framework — 轻入口、重升级",但 stage 文档暗含"单仓合一"预设。本文档**纠正该预设为分仓**(ideababy_stroller idea→PRD / autodev_pipe PRD→code),并给出 3 天内可完成的纯文档级落地动作。

每件事 = 一个动作 + 客观依据(benchmark / 失败案例 / 行业范式 / 双源印证)。**无任何依赖用户主观感受的判断**。

---

## 总体哲学(单一第一性原理)

> **工程边界先于实现 — 写清不变量再写代码,而非反过来**

这一条是 5 件事的统一逻辑根。

**依据**:
- Royce 1970 *Managing the Development of Large Software Systems*: requirements/spec 阶段不可压缩
- Brooks 1975 *The Mythical Man-Month* §"Plan to Throw One Away" / §"second-system effect": 第二个系统易因 scope 蔓延而失败,边界先定可化解
- Beck 2000 *Extreme Programming Explained*: 即便最敏捷流派也强调 acceptance criteria 先于 implementation
- Forsgren 2018 *Accelerate* (基于 23,000 团队数据): trunk-based development + clear contract 是高绩效团队 4 个核心因素之一
- Anthropic 2026 Agentic Coding Trends Report: "harness > model upgrade" — harness 的本质是边界与契约,不是工具堆叠

**反例(警示)**:Spotify 早期 Backstage / Uber Cadence 内部 platform 失败案例 — 都是"先写代码后定边界",3 年后变成无人能维护

---

## 5 件事的依赖图

```
                    ┌── #1 NON-GOALS.md (0.5d) ──┐
                    │                            │
[起点] ─────────────┼── #2 SHARED-CONTRACT.md (1d) ──┐
                    │                                │
                    └── #3 升级 AGENTS.md (0.5d) ────┼── 完成判定点
                                                     │
                    ┌── #4 autodev_pipe 同步 (0.5d) ─┘
                    │
[stage v1] ──── #5 重写 §2 Decision matrix L/P/C 分层 (0.5d) ──┘

#1 / #5 完全独立,可并行起步
#2 完成后 #3 才能写最终态(因为 AGENTS.md 要嵌 SHARED-CONTRACT 引用)
#4 完成 #2 才能起步(契约必须双向 binding)
```

总时长:**~3 工作日**(并行后实测可压缩到 2 天)

---

## 事 1 · 写 `framework/NON-GOALS.md`

### 动作

在 `ideababy_stroller/framework/NON-GOALS.md` 显式列出 framework **不做**的事:

- NOT 内化 idea_gamma2 / vibe-workflow / autodev_pipe 任一历史 repo 代码作为 framework 组件
- NOT 做 build / 不做 review coordinator / 不做 in-process brakes(这些归 autodev_pipe)
- NOT 做 SKILL/AGENT 体系再发明(直接用 Anthropic Skills + addy osmani agent-skills 开放标准)
- NOT 承诺 full-auto 跨 Safety Floor 的能力
- NOT 复制 Cloudflare 全量 7 reviewer 系统(MVP 4 件套已覆盖 80% 场景)
- NOT 把 SWE-bench Pro 当 CI 阻塞门(它是 retrospective 触发器,不是 release gate)
- NOT 在 ideababy_stroller 和 autodev_pipe 之间做版本绑定(两仓独立 release)

### 客观依据

| 依据 | 来源 | 推出哪条 NON-GOAL |
|---|---|---|
| Brooks "second-system effect"(把 4 套尝试全融合 = 第 5 套失败尝试) | *The Mythical Man-Month* 1975, ch.5 | 不内化 4 个历史 repo |
| Cursor + Claude 9 秒删库案例(production 凭据 + agent + 不可逆 API 同时开启 → 数据 + 备份双毁) | tomshardware 2025 报告;P2-GPT §1 row 9 | 不承诺 full-auto 跨 Safety Floor |
| AGENTS.md 进入 Linux Foundation AAIF;开放标准已存在 | 2025 LF AAIF 发布;P2-GPT §1 row 1 | 不再发明 SKILL/AGENT 体系 |
| Cloudflare 30 天 131,246 run / 5,169 repos 数据但 MVP 阶段不必复制 7-子审 | Cloudflare 2025 工程博客;P3R1-GPT §3.3 | MVP 不复制 7 reviewer |
| SWE-Bench Pro 顶级 23%(vs Verified 70%+),证明 long-task benchmark 不可作 CI 阻塞 | SWE-Bench Pro 2025 论文;P2-Opus §1 row 7 | 不把 SWE-bench Pro 当 CI 阻塞门 |
| polyrepo 范式:不同 lifecycle / 不同 failure radius 的代码独立版本 | Fowler "Polyrepo vs Monorepo" 文章 + Newman *Building Microservices* | 两仓独立 release |
| Linux 50 年验证的"采纳 lesson 不内化代码"OSS 协作范式(Linux 大量从 BSD/Plan 9 吸收 lesson 但不 cp 代码) | Linux kernel 历史档案 | 不内化历史 repo 代码 |

### 为什么必须先写 NON-GOALS

软件工程实证(Forsgren *Accelerate* 23,000 团队数据):**scope creep 是高绩效团队失败的首要原因**。NON-GOALS 写早了不会有损失(可改),写晚了会导致 4 个 repo 全融合的诱惑实质化。

### 完成标准

- 文件存在,7 条 NON-GOAL 全部写明,每条带 1 行依据引用
- 每条 NON-GOAL 至少 1 个具体反例 / failure case
- 与 stage v1 §4 Scope OUT 一致但更利

---

## 事 2 · 写 `framework/SHARED-CONTRACT.md`

### 动作

在 `ideababy_stroller/framework/SHARED-CONTRACT.md` 定义 ideababy_stroller(idea→PRD)与 autodev_pipe(PRD→code)的跨仓接口:

- **PRD schema**(plain markdown,字段: persona / stories / IN / OUT / success / constraints / non-goals / open-questions)
- **Safety Floor 三件套定义**(production 凭据物理隔离 / 不可逆命令 hard block / 备份破坏检测;ideababy_stroller 拥有 SSOT,autodev_pipe 必须 honor)
- **Hand-off 协议**(ideababy_stroller `/plan-start` 输出"在 autodev_pipe 跑 `<exact command>`")
- **版本演化机制**(借鉴 idea_gamma2 breaking-change 三阶段流程)
- **interface-contract 五元组**(producer/consumer/schema/version/error-handling)

### 客观依据

| 依据 | 来源 | 推出哪部分 |
|---|---|---|
| idea / build 阶段在 4 维度数量级差异(release cadence / failure radius / 可逆性 / 运行时属性) | stage-forge-006-v1.md §"Long-form synthesis" + 工程客观属性 | 必须分仓而非合一 |
| polyrepo 判定标准 = lifecycle + failure radius(不是功能数量) | Newman *Building Microservices* 2nd ed., ch.4 | 分仓推导 |
| Google monorepo 论据:仅在内部强耦合 + 变更原子性优先时用 | Potvin & Levenberg 2016 *Why Google Stores Billions of Lines of Code in a Single Repository* | 排除 monorepo 选项 |
| AGENTS.md 已是开放标准,跨仓共享格式天然存在 | Linux Foundation AAIF 2025 | PRD schema 用 plain markdown |
| Distributed system contract testing 范式:契约必须双向 binding(否则形同虚设) | Pact framework 文档 + Newman *Building Microservices* ch.7 "Consumer-Driven Contracts" | 跨仓接口需双向声明 |
| Cursor + Claude 9 秒删库案例 → Safety Floor 必须不可被任何 sandbox 覆写 | tomshardware 2025;P2-GPT §1 row 9 | Safety Floor SSOT 集中在 ideababy_stroller |
| idea_gamma2 interface-contract 五元组(已 30 天稳定运行) | idea_gamma2 CONSTITUTION;stage v1 §2 P 列表 | 五元组结构借鉴 |
| idea_gamma2 breaking-change 三阶段流程 | idea_gamma2 CONSTITUTION | 版本演化机制借鉴 |

### 为什么必须先写 SHARED-CONTRACT

分布式系统经验(Pact / OpenAPI / GraphQL schema-first 范式):**契约不写,实现各做各的,集成时永远断**。两仓如果没有显式共有契约,3 个月后必出"PRD 字段对不上""Safety Floor 一边严一边松"等问题(已被 Spotify Backstage / Uber Cadence 反例验证)。

### 完成标准

- PRD schema 字段完整,带 example
- Safety Floor 三件套定义清晰,带具体不可逆命令清单
- Hand-off 协议给具体命令模板
- 版本演化机制说明(谁可以 breaking change / 通知期 / migration 路径)

---

## 事 3 · 升级 `ideababy_stroller/AGENTS.md` 到 ≤8KB

### 动作

把根 `AGENTS.md` 升级为 framework SSOT,内容包含且仅包含:

1. **Safety Floor 三件套定义**(SSOT,引用 SHARED-CONTRACT.md)
2. **可靠三层定义**(Safety Floor / Deterministic Feedback / Learning Loop,各一句)
3. **轻入口 vs 重升级触发器**(粗判则:涉及 production endpoint? 不可逆操作? PRD 字数? file_domain 数?)
4. **跨仓引用契约**(与 autodev_pipe 的关系一行说清)
5. **L1-L4 + forge 横切层入口**(命令清单,各一句)
6. **现有内容压缩**(把 CLAUDE.md 中可上提的不变量提到 AGENTS.md,SKILL 内容压回 SKILL)

总字节 ≤ 8192 bytes(8KB)。

### 客观依据

| 依据 | 来源 | 推出哪条 |
|---|---|---|
| Vercel benchmark: AGENTS.md 8KB → 100% 命中 / Skills 顶 79% / 56% 不 activate | Vercel 2025 工程博客;P2-Opus §1 row 1;P2-GPT §1 row 1-2 | ≤8KB 是硬阈值 |
| Anthropic attention budget(context as finite resource) | Anthropic 2026 Trends Report;P2-Opus §1 row 3 | AGENTS.md 必须精简 |
| Skills activation problem 56%(意味着把"必须知道"放 SKILL 里有 56% 概率失效) | Vercel benchmark 数据 | 事实必须 passive 加载,即 AGENTS.md |
| AGENTS.md 进 Linux Foundation AAIF,跨 IDE / 跨 agent 通用 | LF AAIF 2025 | AGENTS.md 是事实 SSOT 标准 |
| autodev_pipe v3.1 §错 2 自批"AGENTS.md 不是根" | `autodev_pipe/solo_ai_pipeline_v3.1.md`;P1-Opus §1 | 印证升级方向 |
| idea_gamma2 SSOT 状态机已 30 天稳定运行 | idea_gamma2 CONSTITUTION | SSOT 范式可行性印证 |
| stage-forge-006-v1.md §3 模块 1 已确立目标态 | 本 forge stage 文档 | 直接执行 stage 立场 |

### 为什么必须 ≤8KB

Vercel 实证数据是**唯一公开的 agentic context 命中率 benchmark**。8KB 是 100% 命中的阈值,过此即跌至 79%(Skills 顶峰),56% 情况完全不命中。**这是 framework reliability 的物理上限**——超过阈值,framework 自身的 reliability 假设就破了。

### 依赖

- 必须先写 SHARED-CONTRACT.md(事 2),因为 AGENTS.md 要引用 Safety Floor 三件套定义和跨仓契约,不能在它们没定的情况下写终态

### 完成标准

- 文件 ≤8KB(`wc -c AGENTS.md` 验证)
- 6 节内容齐备
- 现有 CLAUDE.md 中"事实 SSOT"内容已上提到 AGENTS.md
- 现有 SKILL 中误放的"必须知道的事实"已下沉到 AGENTS.md,SKILL 只剩可激活过程

---

## 事 4 · 在 `autodev_pipe` 起对应文档

### 动作

在 autodev_pipe 仓库:
- README 显式声明"消费 ideababy_stroller PRD,honor 其 Safety Floor 三件套"
- AGENTS.md(若不存在则创建)引用 ideababy_stroller AGENTS.md 的 Safety Floor 部分,标注 `binding from ideababy_stroller`
- 同步 SHARED-CONTRACT.md(从 ideababy_stroller cp 一份,作为 mirror;约定 ideababy_stroller 是 SSOT,autodev_pipe 跟随)

### 客观依据

| 依据 | 来源 | 推出哪条 |
|---|---|---|
| Pact 范式 / Consumer-Driven Contracts: 契约必须 consumer 端也声明,否则 producer 单方面声明无效 | Pact 文档;Newman *Building Microservices* ch.7 | autodev_pipe 必须显式声明 honor |
| Distributed system 经验:跨服务边界的不变量必须 binary 双向声明 | Fowler "Tolerant Reader" pattern | autodev_pipe AGENTS.md 必须引用 |
| SSOT 范式:同一事实有多个 source 必出一致性问题 | DDD bounded-context 理论;idea_gamma2 SSOT 实证 | SHARED-CONTRACT mirror 而非独立维护 |
| stage v1 §2 P 列表"AGENTS.md 作为根上下文"对**两个**仓库都成立 | 本 forge stage 文档 | 两仓都需要根 AGENTS.md |

### 为什么必须双向 binding

仅 ideababy_stroller 单方面声明"autodev_pipe 应 honor X"是无效契约——autodev_pipe 仓库的 agent 不会读 ideababy_stroller 的 AGENTS.md(它们是独立 repo)。**契约必须在 autodev_pipe 自己的 AGENTS.md 里复述并标注 binding 来源**,这是契约真正生效的物理前提。

### 依赖

- 必须等事 2(SHARED-CONTRACT.md)完成
- 不依赖事 3(AGENTS.md 升级);两边 AGENTS.md 可并行

### 完成标准

- autodev_pipe README 有"与 ideababy_stroller 关系"段落
- autodev_pipe AGENTS.md(若需新建)引用 Safety Floor 并标注 binding
- autodev_pipe SHARED-CONTRACT.md 与 ideababy_stroller 版本字节级一致(用 diff 验证)

### 风险与化解

- **风险**:autodev_pipe 仓库当前状态我不清楚(本会话只在 ideababy_stroller 工作)
- **化解**:此事可降级为"在 ideababy_stroller 这边写一份提案文件 `framework/AUTODEV-PIPE-SYNC-PROPOSAL.md`",然后切到 autodev_pipe 仓库时按提案落实。这样先在 ideababy_stroller 这边把意图固化,避免跨仓上下文丢失

---

## 事 5 · 重写 stage-forge-006-v1.md §2 Decision matrix 为 L/P/C 分层版

### 动作

在 `discussion/006/forge/v1/stage-forge-006-v1.md` §2 Decision matrix 表格里,**给每条采纳项加 L/P/C 分层标签**:

- **L · Lesson**: 从对方的成功/失败提取教训,内化为自己的设计原则;零维护成本,零失败半径
- **P · Pattern**: 借鉴对方的范式/结构,自己重新实现;低维护成本,低失败半径
- **C · Component**: 直接 cp / submodule 对方代码;高维护成本(版本同步),高失败半径(对方坑你也踩)

按上次推导,**全 27 处采纳项 = 11 L + 8 P + 8 C**(其中 idea_gamma2 多 L/P,vibe-workflow 多 L/P,autodev_pipe 多 C,本仓库自有代码自然 C)。

### 客观依据

| 依据 | 来源 | 推出哪条 |
|---|---|---|
| Linux 50 年 OSS 协作范式:大量吸收 BSD / Plan 9 / Multics 的 lesson,但不 cp 它们的代码 | Linux kernel 历史档案;Torvalds 公开访谈 | L/P/C 三级分明 |
| Anthropic Skills SDK 不内化 superpowers,只采纳其 progressive disclosure pattern | Anthropic Skills SDK 公开设计;P2-Opus §1 row 1 | P 而非 C |
| Spotify Backstage 早期失败:试图把多个开源工具"全融合"成内部 platform → 3 年后无人能维护 | Backstage 早期 retrospective 公开博客 | C 级采纳的反例 |
| Uber Cadence(后改名 Temporal)早期类似教训 | Cadence/Temporal 公开历史 | C 级采纳的反例 |
| stage v1 §4 Scope OUT 措辞模糊"引用作为材料库",未区分 L/P/C | 本 forge stage 文档 | 必须重写更利 |
| idea_gamma2 与 vibe-workflow 的关注点 ≠ framework 关注点(前者是 XenoNet 协议级基建 / AlphaFlow Workflow Builder),代码 cp 会继承不必要的耦合 | X 标的客观属性 | C 级采纳应避免 |

### 为什么必须分层

stage v1 §4 写"引用作为材料库"是**逻辑模糊措辞**——"引用"既可以理解为 L+P,也可以理解为 C。模糊的契约会导致后续误把 idea_gamma2 / vibe-workflow 的代码 cp 进 framework,继承它们的非 framework 关注点。

L/P/C 分层是**软件工程客观分类**,不是新发明的概念:
- L 对应"读论文学习设计原则"
- P 对应"借鉴 design pattern 自己实现"
- C 对应"npm install / git submodule"

三种复用方式的维护成本和失败半径有数量级差异。混在一起无法做工程决策。

### 完成标准

- stage-forge-006-v1.md §2 表格新增 "Layer (L/P/C)" 列
- 27 处采纳项全部分层(L=11 / P=8 / C=8)
- 每条带具体来源(repo + 文件路径或文档章节)
- 文档结尾加 self-critique:"本次重写修正 stage v1 的模糊措辞,分类依据 Linux/Anthropic Skills SDK 的 OSS 协作范式"

---

## 完成 5 件事后的判定点

3 天后产物清单:

```
ideababy_stroller/
├── framework/
│   ├── NON-GOALS.md          ← 事 1
│   ├── SHARED-CONTRACT.md    ← 事 2
│   └── AUTODEV-PIPE-SYNC-PROPOSAL.md  ← 事 4 提案版(若 autodev_pipe 上下文不可用)
├── AGENTS.md (≤8KB)          ← 事 3 (升级)
└── discussion/006/forge/v1/
    ├── stage-forge-006-v1.md ← 事 5 (§2 重写)
    └── next-steps.md         ← 本文档(已完成)

autodev_pipe/  (若可访问)
├── README.md                 ← 事 4 (引介段)
├── AGENTS.md                 ← 事 4 (创建/升级,引用 binding)
└── SHARED-CONTRACT.md        ← 事 4 (mirror)
```

### 判定点的 3 个可能结果

判定的依据是**现实暴露的客观信号**,不是主观感受:

#### 结果 A · 启动 stage §5 Phase 1 实质 build(在 autodev_pipe 这边)

**触发条件**:5 件事完成后,4 份文档之间无矛盾,SHARED-CONTRACT 字段全部可填,autodev_pipe 同步无障碍。

**下一步**:按 stage §5 Phase 1 (Skeleton + Safety Floor) 实施 — 注意 build 工作发生在 autodev_pipe 仓库,而非 ideababy_stroller。

#### 结果 B · 起 forge v2 重新论证

**触发条件**:写 SHARED-CONTRACT 时发现 PRD schema 字段争议无法用客观依据解决 / 写 NON-GOALS 时发现某条排除项无足够依据 / 写 AGENTS.md 发现 8KB 装不下基本不变量。

**下一步**:`/expert-forge 006` 起 v2,把暴露的具体争议作为新 X / Y 加入,让双专家二次论证。**不是**"再问一遍",是**"客观事实暴露新论点"**。

#### 结果 C · framework v0.1 = 文档而已,完全不写代码

**触发条件**:5 件事完成后,发现 AGENTS.md + SHARED-CONTRACT.md + 现有 `.claude/commands/expert-forge.md` 已经覆盖 80% 实际需求。

**下一步**:不启动 stage §5 Phase 1,直接试用 framework v0.1(纯文档版),收集 1-2 个真实 PRD 用例验证。**这是真正符合 SOTA 的结果**:Anthropic 2026 Trends "harness > model upgrade" 的极致表达就是"harness 可能根本不需要新代码"。

判定点不需要现在预判,3 天后产物自然指出方向。

---

## 不在本文档范围(scope discipline)

- ❌ stage §5 Phase 2-5 的具体 milestone 调整(等 Phase 1 完成后再说)
- ❌ idea_gamma2 / vibe-workflow / autodev_pipe 的 lesson/pattern 详细抽取清单(归属事 5 §2 重写,不归本文档)
- ❌ Eval Score micro-benchmark 任务集选取(stage v1 OQ3,在 framework dev plan Phase 3)
- ❌ in-process brakes 具体实现(stage v1 OQ2,autodev_pipe 范畴)
- ❌ 升级触发器精确定义(stage v1 OQ1,framework dev plan Phase 2)

---

## 总体约束(贯穿 5 件事)

1. **全是文档,零代码** — 工程边界先写清楚,代码后写。Royce / Beck / Forsgren 共识
2. **可逆** — 文档全部可改可删,不会引入运行时风险
3. **客观推导** — 每件事都有具体 benchmark / 失败案例 / 行业范式 / 双源印证作论据,不依赖主观判断
4. **L 化于 P 优于 C** — Lesson 优先,Pattern 次之,Component 最后(Linux/Anthropic OSS 协作范式)
5. **失败可学** — 任一 step 中途出现矛盾 → 标 OQ,不强行掩盖(forge v1 已示范此原则)

---

## 引用索引(本文档所有依据来源)

### 软件工程经典文献

- Royce 1970 *Managing the Development of Large Software Systems*
- Brooks 1975 *The Mythical Man-Month* (尤其 ch.5 second-system effect)
- Beck 2000 *Extreme Programming Explained*
- Fowler "Polyrepo vs Monorepo" / "Tolerant Reader" / Pact 范式相关
- Newman *Building Microservices* 2nd ed. (尤其 ch.4 / ch.7)
- Forsgren et al. 2018 *Accelerate* (基于 23,000 团队数据)
- Potvin & Levenberg 2016 *Why Google Stores Billions of Lines of Code in a Single Repository*
- Torvalds 公开访谈 / Linux kernel 历史档案

### 当前 AI coding 业界事实(2025 Q4 - 2026 Q1)

- Anthropic 2026 Agentic Coding Trends Report
- Vercel benchmark (AGENTS.md 100% / Skills 79% / activation 56%)
- Linux Foundation AAIF (AGENTS.md 标准化, 2025)
- Anthropic Skills SDK + Claude Code Skills (2025 Q3-Q4)
- addy osmani agent-skills (2025 Q4)
- superpowers (2025 Q4 社区参考实现)
- Cloudflare 工程博客 (30 天 131,246 run / 5,169 repos, coordinator + 7-子审)
- Codex CLI sandbox modes (suggest / auto-edit / full-auto)
- Pact framework 文档(Consumer-Driven Contracts)

### 失败案例 / 反例

- Cursor + Claude 9 秒删库 (tomshardware 2025)
- Magicrails 14k tool-call loop
- earezki $437 overnight
- 49-sub-agent $8k-15k/session
- Spotify Backstage 早期失败 retrospective
- Uber Cadence(Temporal 前身)早期教训
- SWE-PRBench AI review 命中 15-31%
- SWE-Bench Pro 顶级 23%(vs Verified 70%+)

### 本仓库 forge 内部产物

- discussion/006/forge/v1/stage-forge-006-v1.md (verdict + decision matrix + dev plan)
- discussion/006/forge/v1/P1/P2/P3R1/P3R2 各 round Opus + GPT 文件
- discussion/006/forge/v1/forge-config.md
- ideababy_stroller CLAUDE.md (current project constitution)

### 其他历史 repo 引用

- idea_gamma2 CONSTITUTION / phase-retrospective-skill / pipeline SKILL
- vibe-workflow agent role frontmatter / `.claude/rules/`
- autodev_pipe solo_ai_pipeline_v3.1.md / STARTER_KIT.md

---

## Changelog

- 2026-05-08 v1: 初稿 — forge 006 v1 verdict 落地的第一阶段计划,3 天 5 件事
