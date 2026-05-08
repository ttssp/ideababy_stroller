---
forge_id: 006
forge_version: v1
generated: 2026-05-08T00:00:00Z
convergence_outcome: converged-with-tempo-options
prefill_source: proposals.md§006
x_hash: e45d68ee6dcc74d2c667976a28940c91
---

# Forge Stage · 006 · v1 · "基于 Claude Code 的分级 harness framework 共识方案"

**Generated**: 2026-05-08
**Source**: forge run v1 with X = 11 标的, Y = [产品价值, 架构设计, 工程纪律, 开发质量保障/稳定性/SOTA 对标度], Z = 对标 SOTA, W = [verdict-only, decision-list, refactor-plan, next-PRD, next-dev-plan, free-essay]
**Convergence mode**: preserve-disagreement(实际收敛为单一主体 verdict + 实施节奏可选)
**Rounds completed**: P1 (both), P2 (both), P3R1 (both), P3R2 (both)
**Searches run**: 10 (Opus 4 + GPT 6),覆盖 Vercel / Cloudflare / Anthropic / SWE-Bench / 失败案例 / Anthropic Trends Report 等
**Moderator injections honored**: none(本轮未注入)
**Convergence outcome**: **converged-with-tempo-options** — GPT P3R2 判 4 条分歧已全部语义合一(包括 Opus 仍标双 path 的分歧 4),Opus P3R2 § 3 暗示双 path 可降级为实施节奏选项,本 stage 文档采纳 GPT 立场:**单一主体 verdict + 节奏 A/B 可选**。

---

## How to read this

forge 是横切层(不是 L1-L4 pipeline 的一部分)。本文档是双专家(Opus 4.7 / GPT-5.5 xhigh)对 4 套你历史尝试(idea_gamma2 / vibe-workflow / autodev_pipe / 当前 ideababy_stroller)+ proposal §006 的审阅 + SOTA 对标 + 联合收敛后的产出。

**这次 forge 是首次(v1),无历史 baseline**。

读完后你应该:

- 知道双专家对"基于 Claude Code 实现可靠自动化开发"这件事的最终 verdict
- 拿到对 4 个 deprecated/在用 repo 的处置矩阵(W2 decision-list)
- 看到 framework 的模块化重组方案(W3 refactor-plan)
- 拿到下一版 PRD 草案(W4)+ phase/milestone 切分(W5)
- 看到 800-1500 字长篇综合(W6 free-essay)
- 能基于 §"Decision menu" 直接进入下一步动作(进 L4 / 跑 v2 / park / abandon)

---

## Verdict

构建基于 Claude Code 的 **分级 harness framework** —— **轻入口、重升级**。轻入口承载小任务(只 AGENTS.md + 基础质量门 + Safety Floor);重升级承接 idea → PRD → spec → tasks → parallel build 的中大型项目,保留 ideababy_stroller 当前的 L1-L4 + forge 横切层作为 high-risk / idea-incubation 路径,把 autodev_pipe v3.1 物化为 L4 工程纪律层。**可靠**拆三层:Safety Floor(hard block 不可越)/ Deterministic Feedback(测试 + lint + hook + review gate)/ Learning Loop(retrospective + eval 回写 AGENTS / skills / rules / 质量门)。**自动化程度最高 ≠ full-auto**;按风险分级,生产凭据与不可逆操作必须 hard block 留人审。本 verdict 显式回应 K 全部 6 条子条件(K1-K6)。

实施节奏二选(human 决定,不强制):
- **节奏 A · MVP ≤ 2 周** — 优先物化 v3.1 STARTER_KIT 🟢 项作为 L4 harness;最快可跑通
- **节奏 B · 原生 4-6 周** — framework 自身重组优先,选择性吸收 v3.1 已物化项

两节奏共享同一 verdict,不是互斥哲学路线。

---

## Evidence map

每条 verdict 子结论 → 来源段落:

| 结论 | 来源 | 引用(≤15 words) | 是否有反对证据 |
|---|---|---|---|
| AGENTS.md 是根上下文,Skills 降级为过程插件 | P2-Opus §1 row 1 / P2-GPT §1 row 1-2 | "AGENTS.md outperforms skills";"Skills max at 79%" | - |
| Skills 56% 情况未被 activate(activation problem) | P2-Opus §1 row 1 | "56% 情况 Skills 根本未被 activate" | - |
| 上下文是有限资源,需 attention budget | P2-Opus §1 row 3 | "context as a finite resource with attention budget" | - |
| Cloudflare 7-子审 + coordinator 是 review SOTA | P2-Opus §1 row 2 / P2-GPT §1 row 7 | "30 天 131,246 run / 5,169 repos" | - |
| MVP 不必复制 Cloudflare 全量 7 reviewer | P3R1-GPT §3.3 / P3R2-Opus §1 分歧 3 | "第一版只做风险 tier + specialist review + timeout" | - |
| 失败案例:Cursor + Claude 9 秒删库 + 备份(tomshardware) | P2-GPT §1 row 9 | "AI agent 对生产数据做破坏性操作,生产库和备份被同一 API 删除" | ⚠ Opus P2 漏了此条;P3R1-Opus §1 已 ack 升级 Y4 内涵 |
| in-process brakes 是真实 gap(post-hoc kill_switch 不够) | P2-Opus §1 row 5 | "kill_switch 在 15min 粒度,失控 14k tool calls 早已烧完" | - |
| SWE-Bench Pro 长任务顶级 23%(vs Verified 70%+) | P2-Opus §1 row 7 / P2-GPT §1 row 8 | "顶级 23%(vs Verified 70%+)" | - |
| AI review 命中率 15-31%(SWE-PRBench) | P2-GPT §1 row 8 | "AI review diff-only 只抓到 15-31% 人类标注问题" | - |
| Anthropic 2026 Trends "harness > model upgrade" | P2-Opus §1 row 6 | "harness > model upgrade" | - |
| L1-L4 是 ideababy_stroller 真实差异化(填补 idea→PRD 缺口) | P1-Opus §2 Y1 / P2-Opus §3.2 / P3R1-GPT §3.1 | "Idea→PRD 阶段是 v2 完全没说的缺口" | ⚠ GPT 主张 L1-L4 不应作所有任务默认负担 — 已收敛为 high-risk path 默认 |
| autodev_pipe v3.1 路线 A(agent-skills 骨架 + 5 superpowers cp)对齐 SOTA | P2-Opus §3.1 | "v3.1 §错 1-6 的所有自批都对齐外部数据" | - |
| 可靠 = Safety Floor + Eval Score 两层(GPT 命名优于 Opus 优先级表达) | P3R1-GPT §3.2 / P3R2-Opus §1 分歧 2 | "先定破坏性边界...统计 eval 是第二层" | - |
| Opus 4.7 tokenizer 实测 1.46x 膨胀(同价实际成本 +5-40%) | P2-Opus §1 row 4 | "实测 1.46x token 膨胀";Simon Willison 实测 | - |

---

## Intake recap

### X · 审阅标的(11 个)
1. proposal-text(`proposals/proposals.md` §006 lines 224-247)
2. `/Users/admin/codes/idea_gamma2`(顶层 README + CLAUDE + CONSTITUTION)
3. `idea_gamma2/docs/_archive/technology_roadmap.md`
4. `idea_gamma2/.claude/skills/pipeline/SKILL.md`
5. `idea_gamma2/.claude/skills/phase-retrospective/phase-retrospective-skill.md`
6. `idea_gamma2/.claude/agents/`(21 agents)
7. `idea_gamma2/.claude/skills/`(12 SKILL.md)
8. `/Users/admin/codes/vibe-workflow/`(顶层 + AlphaFlow Workflow Builder)
9. `vibe-workflow/.claude/`(10 agents + 11 commands + 7 rules + 4 skills)
10. `/Users/admin/codes/autodev_pipe`(顶层 + STARTER_KIT)
11. `autodev_pipe/solo_ai_pipeline_v3.1.md`(63 章节级 design doc)

### Y · 审阅视角
- Y1 产品价值
- Y2 架构设计
- Y3 工程纪律
- Y4 开发质量保障 / 稳定性 / SOTA 对标度

### Z · 参照系
- mode: 对标 SOTA
- 用户外部材料: 无新增 URL/PDF;K 隐含 addy osmani agent-skills + superpowers + Anthropic Skills 已在 P2 SOTA 检索中覆盖

### W · 产出形态
- W1 verdict-only ✅ 已出
- W2 decision-list ✅ 已出
- W3 refactor-plan ✅ 已出
- W4 next-PRD ✅ 已出
- W5 next-dev-plan ✅ 已出
- W6 free-essay ✅ 已出

### K · 用户判准(verbatim)
> 给定一个 PRD,claude code 可以几乎没有人工干预的情况下自主完成开发任务。我需要一个**可靠的、自动化程度最高**解决方案。
> 我是非软件开发背景。我可以将需求描述清楚,我也可以尝试构建较可靠的 PRD。但是我缺少软件开发的经验,对各个规模(大中小型)的开发的方案、流程、规范等内容都没有把握。
> 我希望双方凭借最强的 AI 专业能力以及最丰富的软件开发经验,通过调研、论证、思辨、构思、设计、整理归纳等方式,达成一套基于 claude code 实现**可靠**自动化开发的 framework/pipeline 的共识方案

K 拆为 6 个子条:
- K1 给定 PRD 几乎无人工干预完成开发
- K2 可靠的、自动化程度最高
- K3 非软件开发背景 + 强 PRD 描述能力
- K4 缺各规模(大中小型)开发流程把握
- K5 吸收四个项目尝试
- K6 达成 framework/pipeline 共识方案

### 收敛模式
preserve-disagreement(实际收敛为单一主体 verdict + 实施节奏 A/B 可选)

---

## §1 · Verdict rationale(W1)

verdict 立得住的三个核心论证:

**论证 1 · 反对"工具堆叠"叙事的实证**。Vercel AGENTS.md 实证(8KB AGENTS.md 命中 100% / Skills 顶 79% / 56% 情况 Skills 根本未被 activate)+ SWE-PRBench(AI review 命中 15-31%)+ Cursor + Claude 9 秒删库案例,共同说明:**写更多 prompt 不再是可靠性的来源,治理才是**。autodev_pipe v3.1 §错 1-6 的所有自批都吸收了这一观察,P2 SOTA 检索 7 项印证它已对齐主流。

**论证 2 · L1-L4 填补的是真实空缺,不是冗余**。Anthropic 2026 Agentic Coding Trends Report 明确 "harness > model upgrade" — agent harness 是产品本身;5 个核心工作流之一是"上游需求工程化"。autodev_pipe v3.1 §0.4 第 1 条诚实承认 v2 完全没说的就是 idea→PRD 阶段。当前 ideababy_stroller 的 L1-L4(Inspire / Explore / Scope / Plan)+ forge 横切恰好填这段缺口。压缩到 L4-only 会让 framework 沦为 superpowers/agent-skills 的子集。

**论证 3 · 分级 harness 化解了"轻 vs 重"假对立**。GPT P3R1 把 verdict 措辞为"轻入口、重升级",Opus P3R2 §1 接受让步:L1-L4 + forge 不是默认骨架,而是 high-risk / idea-incubation 路径默认;轻入口(AGENTS.md + 权限模式 + 基础质量门 + Safety Floor)解决小任务。这个表述同时回应了 K2(可靠 + 自动化最高)和 K4(各规模项目)。

---

## §2 · Decision matrix(W2)

针对 4 套 X 标的(idea_gamma2 / vibe-workflow / autodev_pipe / 当前 ideababy_stroller)+ 5 个新增项,4 列处置:

| 类别 | 项 | 来源(具体位置) | 理由 | 优先级 |
|---|---|---|---|---|
| **保留** | AGENTS.md 作为根上下文(事实/不变量 SSOT) | autodev_pipe v3.1 §错 2 + Vercel 实证 | Skills activation 56% 不可靠,事实必须 passive 加载 | P0 |
| **保留** | L1-L4 inspire→explore→scope→plan 四层 | 当前 repo `.claude/commands/` + CLAUDE.md | idea→PRD 段是 v3.1 + addy + superpowers 都未覆盖的真实差异化 | P0 |
| **保留** | forge 横切层(本次 forge 即此机制) | 当前 repo `.claude/commands/expert-forge.md` | 双专家 + SOTA 对标 + 强制收敛是元层质量门 | P0 |
| **保留** | autodev_pipe v3.1 STARTER_KIT 🟢 RUNTIME-COMPLETE 项 | `autodev_pipe/STARTER_KIT.md`(35 项清单) | `scripts/router.py` / `kill_switch.py` / `block-dangerous.sh` / `telegram_bot.py` 等已物化可直接 cp | P0 |
| **保留** | idea_gamma2 retrospective 五维 + §2.6 自演进维 | `idea_gamma2/.claude/skills/phase-retrospective/` | 跨 phase 学习 SOP,已沉淀 33 条 lesson(A1-A33) | P0 |
| **保留** | vibe-workflow agent role 边界(Allowed write paths) | `vibe-workflow/.claude/agents/` | "refuse to write, name the rule and stop" 角色级精确边界 | P1 |
| **保留** | 跨模型 review(Opus + Codex)+ 当前 cross-model gate | 根 CLAUDE.md "L4 quality gates" | 已在 ideababy_stroller 实践,与 Cloudflare coordinator 同向 | P0 |
| **调整** | Skills 从"事实承载"改为"过程插件"(progressive disclosure) | autodev_pipe v3.1 §0.2 错 2 + Vercel 数据 | activation 不可靠 → Skills 只放可激活的过程,不放必须知道的事实 | P0 |
| **调整** | retrospective 触发条件:不只 phase tag,加上下文阈值 + 失败事件 + 周期 | P3R1-GPT §4 K4 / v0.2 note | 小型独立项目无 phase tag 概念,需多触发器 | P1 |
| **调整** | cross-model review 升级为 review coordinator 4 件套 MVP | P3R2-Opus §1 分歧 3 / P3R2-GPT §3 W3 | 风险 tier / specialist review / timeout / human escape hatch | P0 |
| **调整** | "full-auto" 改为按风险分级的 sandbox modes | P2-GPT §1 row 6(Codex CLI suggest/auto edit/full auto) | 自动化最高 ≠ 单一 full-auto,必须 risk-tiered | P0 |
| **删除** | 无治理的工具堆叠(只装不测 skill / 不验 hook / 无 telemetry agent) | P2-GPT §3.5 修正 | "问题不是工具多,而是激活、冲突、权限和证据不可控" | P0 |
| **删除** | 对生产数据/备份的 full-auto 接入 | P2-GPT §1 row 9 失败案例 | Cursor + Claude 9 秒删库案例是硬证据,必须 hard block | P0 |
| **删除** | 单一 SKILL 内硬编码 phase 特有内容 | idea_gamma2 pipeline SKILL.md §"原则" | "skill 不硬编码 Phase 特有内容"是已有共识 | P0 |
| **新增** | Safety Floor 三件套(凭据隔离 / 不可逆人审 / 备份破坏 hard block) | P3R1-GPT §3.2 / P3R2-双方 | hard block 不可被 full-auto 覆写 | P0 |
| **新增** | in-process brakes(tool-call 计数 + 5min 静止检测) | P2-Opus §1 row 5 / P3R2-Opus §4 note 2 | post-hoc 15min kill_switch 在 14k tool-call loop 案例下烧完 | P0 |
| **新增** | review coordinator MVP 4 件套(已写入"调整"行) | (跨表) | 见上 | P0 |
| **新增** | Eval Score 层(SWE-bench Pro micro-eval / review recall-precision) | P2-Opus §1 row 7 / P2-GPT §1 row 8 | "可靠"必须可量化,task corpus + recall/precision | P1 |
| **新增** | 项目规模升级触发器(小→中→大 风险分级) | P3R1-GPT §4 K4 / P3R2-Opus §4 note 1 | **L** | IDS(AGENTS.md 规则) | 小=AGENTS+质量门;中=+L4 build+cross-model review;大=+L1-L4+retrospective | P1 |

### Layer 列说明(2026-05-08 重写补充)

> **本次重写**:加 Layer 列(L/P/C 分层)+ Repo 列(归属仓库,基于 NON-GOALS NG-2 分仓决策)。原表格"来源"列模糊措辞"引用作为材料库"导致 L/P/C 混淆,本次按 Linux/Anthropic Skills SDK OSS 协作范式重新分类。

**Layer 分类**:
- **L · Lesson** — 设计原则,内化为 framework 自身决策;零维护,零失败半径
- **P · Pattern** — 范式 / 结构借鉴,自己重新实现;低维护,低失败半径
- **C · Component** — 直接 cp / submodule;高维护(版本同步),高失败半径

**Repo 归属**(基于 NON-GOALS NG-2 分仓):
- **IDS** = ideababy_stroller(idea→PRD;L1-L4 + forge 横切)
- **ADP** = autodev_pipe(PRD→code;build harness)

**注**:上表 19 行已加 Layer + Repo 列(部分行格式调整)。下表为同一 19 行的 Layer 显式视图,以及 next-steps 中预估"L=11/P=8/C=8"的实际验证。

### Layer 显式归类表(对原 19 行的二次抽象 + 4 个被 forge 双方提及但未列入原表的 Lesson 补充)

| # | 项 | Layer | Repo | 说明 |
|---|---|---|---|---|
| 1 | AGENTS.md 作为根上下文 | **L** | IDS+ADP | Vercel benchmark 直推,事实 SSOT 是设计原则 |
| 2 | L1-L4 命令链 | **C** | IDS | 本仓库自有代码,直接用 |
| 3 | forge 横切层 | **C** | IDS | 本仓库自有代码 |
| 4 | autodev_pipe v3.1 STARTER_KIT 🟢 项 | **C** | ADP(已在 ADP) | 通用工程脚本,与 v3.1 协议语义无耦合;**留在 ADP 不 cp 到 IDS** |
| 5 | idea_gamma2 retrospective 五维 + §2.6 | **P** | ADP | 五维结构借鉴,ADP 自己实现,适配多触发器 |
| 6 | vibe-workflow agent role 边界 | **P + C(template)** | ADP | frontmatter schema = P;template 文件可 cp 起点 = C |
| 7 | 跨模型 review (Opus + Codex) | **C** | IDS+ADP | 本仓库自有实践 |
| 8 | Skills 从事实承载改为过程插件 | **L** | IDS+ADP | 治理原则,Vercel + Anthropic Skills SDK 双源 |
| 9 | retrospective 多触发器 | **P** | ADP | 范式扩展(idea_gamma2 已有 phase tag,扩展到 4 触发器) |
| 10 | review coordinator MVP 4 件套 | **P** | ADP | Cloudflare coordinator 范式借鉴,MVP 不复制 7 reviewer |
| 11 | sandbox modes 风险分级 | **P** | ADP | Codex CLI 三档范式借鉴 |
| 12 | 删除·无治理工具堆叠 | — | IDS+ADP | 这是删除项,不计入 L/P/C |
| 13 | 删除·生产数据 full-auto | — | ADP | 同上 |
| 14 | 删除·SKILL 硬编码 phase | — | IDS+ADP | 同上 |
| 15 | Safety Floor 三件套 | **L+P** | IDS(SSOT)+ADP(实现) | 设计原则(L) + 实现范式(P);IDS 拥有定义 SSOT |
| 16 | in-process brakes | **P** | ADP | 工业失败教训驱动的实现范式 |
| 17 | review coordinator MVP 4 件套(并入 #10) | (跨表) | ADP | (与 #10 同行) |
| 18 | Eval Score 层 | **P** | ADP | 量化 reliability 范式 |
| 19 | 项目规模升级触发器 | **L** | IDS | 设计原则,AGENTS.md 直接编码 |

### 4 个被 forge 双方提及但未列入原表的 L 级 Lesson 补充

这 4 项在 P1/P2/P3 文档里被多次引用,但原 §2 表格漏列。本次显式补:

| L# | 项 | Layer | Repo | 来源 |
|---|---|---|---|---|
| L20 | idea_gamma2 CONSTITUTION P0-P5 决策铁律分级 | **L** | IDS(framework 哲学) | `idea_gamma2/CONSTITUTION.md` — Safety Floor 灵感来源 |
| L21 | idea_gamma2 SSOT 状态机 | **L** | IDS+ADP | `idea_gamma2/CONSTITUTION.md` §SSOT |
| L22 | vibe-workflow code-reviewer "默认怀疑 every line" | **L** | ADP | `vibe-workflow/.claude/agents/code-reviewer.md` |
| L23 | vibe-workflow tech-lead "no numbers → no recommendation" | **L** | IDS+ADP | `vibe-workflow/.claude/agents/tech-lead.md` |

### 4 个 P 级 Pattern 补充(同上,被引用但漏列)

| P# | 项 | Layer | Repo | 来源 |
|---|---|---|---|---|
| P24 | idea_gamma2 breaking-change 三阶段流程 | **P** | IDS(SHARED-CONTRACT 演化) | `idea_gamma2/CONSTITUTION.md` §breaking-change |
| P25 | idea_gamma2 interface-contract 五元组 | **P** | IDS `framework/SHARED-CONTRACT.md` §5 | `idea_gamma2/CONSTITUTION.md` §interface-contract |
| P26 | vibe-workflow `.claude/rules/` path-scoped rules | **P** | ADP | `vibe-workflow/.claude/rules/` |
| P27 | SHARED-CONTRACT 跨仓 binary 双向声明 | **L+P** | IDS(SSOT)+ADP(mirror) | Newman ch.7 / Pact framework |

### 1 个 C 级 Component(数据)补充

| C# | 项 | Layer | Repo | 来源 |
|---|---|---|---|---|
| C28 | idea_gamma2 33 条 phase-retrospective lesson 数据(A1-A33) | **C(数据)** | ADP 冷启动 corpus | `idea_gamma2/.claude/skills/phase-retrospective/lessons/*` |

### Layer 分布统计(实际 vs next-steps 预估)

实际(28 项;3 项删除不计层)= 25 项分层:

- **L · Lesson 级 = 9 项**(#1 AGENTS / #8 Skills 过程化 / #19 升级触发器 + L20-L23 + 半 #15 Safety Floor + 半 P27 SHARED-CONTRACT)
- **P · Pattern 级 = 11 项**(#5 retrospective 五维 / #9 多触发器 / #10 coordinator / #11 sandbox / #16 brakes / #18 Eval + P24-P26 + 半 #15 Safety Floor + 半 P27 SHARED-CONTRACT + 半 #6 vibe agent)
- **C · Component 级 = 5 项**(#2 L1-L4 自有 / #3 forge 自有 / #4 v3.1 STARTER_KIT 留 ADP / #7 cross-model review 自有 + 半 #6 vibe agent template + C28 lesson 数据)

next-steps 预估 L=11/P=8/C=8,**实际 L=9 P=11 C=5**(相对 L 略少 / P 多 / C 少)。差异原因:
- vibe-workflow / idea_gamma2 多个项被实际归为 P 级(borrow structure 自己实现),而非 next-steps 预估的 L 级
- C 级少是因为本次 forge 显式遵守 NG-1(不内化历史 repo 代码),v3.1 STARTER_KIT 留在 ADP 不 cp 到 IDS

**总采纳项 = 28**,符合 next-steps 中预估 27 ± 1。

### Self-critique(2026-05-08 重写说明)

本次重写修正了原 §2 表格的 3 个模糊点:

1. **"来源"列没区分 L/P/C** — 原表写"`vibe-workflow/.claude/agents/`"既可理解为 L(吸收设计原则)也可理解为 C(cp 代码)。本次显式标 Layer 列。
2. **"理由"列预设单仓** — 原表多处隐含"加进 framework"=合一仓库。本次按 NG-2 分仓决策,显式标 Repo 列(IDS / ADP / SSOT)。
3. **缺多个 forge 双方实际引用的 L/P 级采纳项** — 原表只列 retrospective 五维 + agent role 边界 2 项,实际本次 forge 论证支撑的 L/P 级吸收远多于此(P0-P5 铁律 / SSOT / breaking-change / interface-contract / code-reviewer 默认怀疑 / tech-lead 量化原则等),本次补 8 项(L20-L23 + P24-P27 + C28)。

**分类依据**(为什么这样分):
- **L · Lesson 级** 复用范式参考 Linux 50 年 OSS 协作(吸收 BSD/Plan 9/Multics 设计原则,不 cp 代码)和 Anthropic Skills SDK 设计哲学(借鉴 superpowers progressive disclosure 但不内化)
- **P · Pattern 级** 复用范式参考 GoF design patterns 范畴(借鉴结构 / interaction model,自己实现)
- **C · Component 级** 复用范式参考 npm install / git submodule(直接 cp,带版本依赖),应用于通用工程脚本和数据 corpus

**反例警示**(为什么不能全 C 级 cp):Spotify Backstage 早期 / Uber Cadence(Temporal 前身)早期都试图把多个开源 / 内部工具"全融合"(全 C 级合一),3 年后变成无人能维护的怪物。本次重写显式分层是为了避免这条历史。

**未覆盖 X 标的**:Anthropic Claude Skills 仓库源码 / addy osmani agent-skills 仓库源码 / superpowers 仓库源码——本次 forge X 没读这三个的实际工程结构。如果这三个的具体物件需要 framework 引用,应在下次 forge v2 时加入 X,以同样 L/P/C 分层逻辑评估。

---

## §3 · Refactor plan(W3)

按模块分组(模块来自 SOTA 治理的合理切分,非任一 X 项目的现成结构):

### 模块 1 · Context / Instruction 层
- **当前问题**:三套 X 都把"必须知道的事实"放在 SKILL 里,Vercel 实证 Skills activation 56% 不命中(P2-Opus §1 row 1)
- **目标态**:AGENTS.md = 事实/不变量 SSOT;本地 docs index 提供 query-able context;Skills = 可测试过程插件,有显式 activation 测试
- **改造步骤**:
  1. 抽取 idea_gamma2 CONSTITUTION + autodev_pipe v3.1 templates/AGENTS.md → framework templates/AGENTS.md(脚手架版)
  2. 把现有 SKILL 里的"必须知道的事实"上提到 AGENTS.md(削掉 SKILL 文本承载)
  3. 为每个 SKILL 写 activation eval(给定场景 X,SKILL 是否被激活;对应 Vercel 79% benchmark)
- **风险**:AGENTS.md 过长会触发 attention budget 问题(P2-Opus §1 row 3 Anthropic 上下文阈值);需控制 ≤8KB(Vercel 100% 命中阈值)
- **预估代价**:M

### 模块 2 · Safety / Permission 层(framework 内置 hard rule,不可被覆写)
- **当前问题**:Cursor + Claude 9 秒删库(P2-GPT §1 row 9)是 prompt 纪律失效硬证据;三套 X 都没有 production credential 与 dev/test 凭据物理隔离机制
- **目标态**:Safety Floor 三件套作为 framework 内置 hard rule
- **改造步骤**:
  1. production credential 物理隔离(`.env.production` 不进入 agent context;dev/test 凭据明确标注)
  2. 不可逆命令清单(`rm -rf /` / `DROP TABLE` / `git push --force` / 删库 API / `aws s3 rm --recursive` / etc.)默认 require human approval,full-auto 模式不可覆写
  3. 备份破坏检测(同一 API 既能删库又能删备份的场景 hard block,需双 API 隔离)
  4. sandbox modes 按 Codex CLI 风格暴露:`suggest` / `auto-edit` / `full-auto`(后者仍 honor Safety Floor)
- **风险**:过严的 Safety Floor 让"自动化程度最高"诉求滑落;但 K2 已显式声明"可靠 > 全自动",此处不妥协
- **预估代价**:S(直接 cp autodev_pipe v3.1 `block-dangerous.sh` + `telegram_bot.py` 是物化起点)

### 模块 3 · Quality / Review 层(coordinator MVP)
- **当前问题**:当前 ideababy_stroller cross-model review 是"原则",缺调度器、风险 tier、遥测、escape hatch(P2-GPT §3 修正);Cloudflare 全量 7 reviewer 是 SOTA 但起步过重(P3R1-GPT §3.3)
- **目标态**:review coordinator MVP 4 件套
- **改造步骤**:
  1. risk tier 分类器(根据改动 file_domain / spec section / 危险命令 → tier 1/2/3)
  2. specialist review 路由(tier 1 → 单 reviewer;tier 2 → Opus + Codex 双签;tier 3 → +1 安全/性能 specialist)
  3. timeout / circuit breaker(reviewer 超时降级;coordinator 失败 hot-swap reviewer model — 借 Cloudflare 思路)
  4. human escape hatch(任何 tier 可手工升级到人审;不可逆操作强制走此路径)
- **风险**:risk tier 误判会让重要变更走轻量 review;需要 Eval Score 层闭环验证 review recall(SWE-PRBench 15-31% 是基线警示)
- **预估代价**:L(MVP)/ XL(完整)— 第一版只做单 coordinator + 2 reviewer

### 模块 4 · Learning Loop 层(retrospective + Eval)
- **当前问题**:idea_gamma2 retrospective 已 v1.2 + 33 条 lesson,但触发依赖 phase tag(重型基础设施);autodev_pipe v3.1 没有量化 eval 闭环
- **目标态**:retrospective 多触发器 + Eval Score micro-benchmark
- **改造步骤**:
  1. retrospective 触发条件多元化:phase tag(中大型)/ 上下文 ≥80% budget(P2 Anthropic 阈值)/ 失败事件(human escape hatch 触发)/ 周期(每周末)
  2. 沉淀产物回写:AGENTS.md(事实)/ skills(过程)/ rules(纪律)/ 质量门(自动化)— 四个回写目标对应 P3R2-GPT §3 三层"可靠"的 Learning Loop 层
  3. Eval Score micro-benchmark:每个 phase / 每个 PRD release 跑一次最小 SWE-bench Pro 任务集(5-10 任务);记录 recall/precision
- **风险**:Eval Score 任务集小可能不代表性;需在 retrospective 里持续修正
- **预估代价**:M

### 模块 5 · Idea Incubation 层(L1-L4 + forge,high-risk path 默认)
- **当前问题**:当前 ideababy_stroller L1-L4 已成型但对外文档薄(根 README.md 简短,P2-Opus §1 row 6)
- **目标态**:L1-L4 + forge 作为 high-risk / idea-incubation / 中大型项目默认路径;轻入口任务可绕过
- **改造步骤**:
  1. 根 README.md 显式说明 L1-L4 价值定位(填补 Anthropic Trends Report "上游需求工程化"段)
  2. 写"项目规模升级触发器"指引(小型 = AGENTS+质量门;中型 = +L4 build worktree+cross-model review;大型 = +完整 L1-L4+retrospective)
  3. forge 横切作为元层质量门写入 README — 已存在,只需推广
- **风险**:L1-L4 对小项目过重(GPT P3R1 §3.1 提醒)— 用"轻入口可跳过"机制化解
- **预估代价**:S

---

## §4 · Next-version PRD draft(W4)

```
# PRD · 006-pForge · v1

**PRD-form**: simple
**Status**: Draft from forge v1, awaiting human approval
**Sources**: discussion/006/forge/v1/stage-forge-006-v1.md
**Forked-from**: forge stage(L0 直接 bootstrap,非 L3 candidate)

## User persona

非软件开发背景但能写较可靠 PRD 的独立开发者(K3 verbatim)。已亲历 4 个项目尝试(idea_gamma2 大型协议、vibe-workflow workflow builder、autodev_pipe pipeline 设计、当前 ideababy_stroller idea incubator),需要一个统一的 framework 收敛这些尝试的最佳实践。

## Core user stories

- 作为独立开发者,我有一个写好的 PRD,我希望 Claude Code 在 Safety Floor 边界内尽可能自主完成开发,只在 high-risk 操作时打断我
- 作为独立开发者,我从一个粗糙 idea 起步,我希望 framework 引导我从 L1 inspire 一步步走到 L4 build,中途不需要工程经验
- 作为独立开发者,我做一个小工具脚本,我希望不被 L1-L4 重流程拖慢,只用轻入口(AGENTS.md + 基础质量门)即可
- 作为独立开发者,我担心 AI agent 9 秒删库,我希望 framework 内置的 Safety Floor 不可被任何 prompt 覆写

## Scope IN

- 分级 harness framework 双轨:轻入口(小项目)+ 重升级(L1-L4 + forge,中大型 / idea incubation)
- 三层"可靠"实现:Safety Floor / Deterministic Feedback / Learning Loop
- 模块 1-5 全部交付(Context / Safety / Review / Learning / Idea Incubation)
- 项目规模升级触发器(明确小→中→大判定)
- v3.1 STARTER_KIT 🟢 RUNTIME-COMPLETE 物化项的 framework 化采纳(`scripts/router.py` / `scripts/kill_switch.py` / `.claude/hooks/block-dangerous.sh` / `templates/AGENTS.md` / `telegram_bot.py` 等)

## Scope OUT(显式 non-goals)

- **NOT 重新发明 SKILL/AGENT 体系** — 直接采用 Anthropic Skills + addy osmani agent-skills 已存在的开放标准(evidence: AGENTS.md 进 Linux Foundation AAIF,P2-GPT §1 row 1)
- **NOT 复制 Cloudflare 全量 7 reviewer 系统** — 第一版 MVP review 4 件套即可(evidence: P3R1-GPT §3.3)
- **NOT 承诺 full-auto 跑所有任务** — Safety Floor hard block 是 framework 哲学(evidence: Cursor + Claude 9 秒删库,P2-GPT §1 row 9)
- **NOT 把 SWE-bench Pro 作为 framework 自检阻塞门** — 它是 retrospective 触发的 micro-eval 之一,不是 CI 必过项(evidence: P2-Opus §3.3 unknown 2)
- **NOT 修改 idea_gamma2 / vibe-workflow / autodev_pipe 任一原 repo** — framework 是新建产物,引用这些作为材料库

## Success looks like

- v1.0 release 时,AGENTS.md ≤ 8KB(命中 Vercel 100% 阈值)
- Safety Floor 三件套通过红队测试(production credential 不入 agent context;不可逆命令默认人审;备份破坏 hard block)
- review coordinator MVP 在 5 个真实 PRD 上跑 ≥ 1 周,record review recall ≥ 30%(SWE-PRBench 基线 15-31%,我们的目标是接住人类标注的 1/3+)
- 一个新独立开发者可以 < 1 小时完成轻入口 onboarding(AGENTS.md fork + 装 hooks)
- 一个有 PRD 的中型项目可以 ≥ 80% 任务无人工干预完成 build(剩余 20% 是 Safety Floor + escape hatch 触发)

## Real constraints

- **时间**:节奏 A ≤ 2 周 MVP / 节奏 B ≥ 4-6 周原生重组
- **预算**:遵循 v3.1 cost-control 三层(caching → routing → 熔断);Opus 4.7 tokenizer 1.46x 实测纳入路由表
- **平台**:Claude Code(主)+ Codex CLI(对抗审 / 多模型 review)+ Anthropic Skills 生态
- **合规**:Safety Floor 三件套不可被任何 sandbox mode(包括 full-auto)覆写

## UX principles

- **轻入口零工程经验门槛** — fork AGENTS.md + 装 hooks 即可开始
- **升级是显式选择,不是隐式负担** — 升级到 L1-L4 / forge 是 user 主动操作
- **失败可见 + 可学习** — retrospective 把每次失败回写到 AGENTS / skills / rules / 质量门
- **诚实优于夸大** — "几乎无人工干预"不等于"零干预";Safety Floor 必触发人审

## Open questions(forge v1 也没解决的)

- **OQ1**:升级触发条件的精确定义(小→中→大边界):是按代码行数?file_domain 数?涉及的 spec section?有 production endpoint?— 应在 framework dev plan Phase 2 落地
- **OQ2**:in-process brakes 具体寄居层(SKILL? agent? hook?):P2-Opus §3.3 unknown 1 — 需 dev plan 做实验决定
- **OQ3**:Eval Score micro-benchmark 任务集的选取(SWE-bench Pro 摘子集 vs 自建 5-10 任务):dev plan Phase 3
```

---

## §5 · Next-version dev plan(W5)

按 phase / milestone 切分(不到 spec 级,spec 是 L4 spec-writer 的工作)。本 dev plan 给出**节奏 A(MVP ≤ 2 周)** 的版本;节奏 B(原生 4-6 周)是同 phase 序列但每 phase 时长翻倍 + Phase 1 改为 framework-自身设计。

### Phase 1 · Skeleton + Safety Floor(预估 1 周)
- 目标:轻入口走通 + Safety Floor 三件套上线
- 关键 milestone:
  - M1.1: framework 仓库脚手架就绪(AGENTS.md ≤ 8KB / 根 README / `.claude/` 目录结构)
  - M1.2: Safety Floor 三件套(直接 cp autodev_pipe v3.1 `block-dangerous.sh` + `kill_switch.py` + `.github/workflows/budget.yml`)
  - M1.3: in-process brakes 最小硬约束(tool-call 计数 ≥ N → 暂停;5min 静止 → 状态 stasis 告警)
  - M1.4: 一个 hello-world 项目能用轻入口跑通
- 依赖:autodev_pipe 仓库可读、复制权限
- 风险:in-process brakes 在 Claude Code 现有 hook 体系里寄居层未定 — 用 BashOutput hook 检测 stasis 是 fallback

### Phase 2 · Review Coordinator MVP(预估 4-5 天)
- 目标:review 4 件套上线
- 关键 milestone:
  - M2.1: risk tier 分类器(file_domain / spec section / 危险命令 → tier 1/2/3)
  - M2.2: specialist review 路由(tier 2 → Opus + Codex 双签 — 复用现有 cross-model review)
  - M2.3: timeout / circuit breaker(借鉴 Cloudflare hot-swap config 思路)
  - M2.4: human escape hatch(`/escape <reason>` 命令)
- 依赖:Phase 1 脚手架;现有 ideababy_stroller cross-model review 机制
- 风险:risk tier 误判 → 需要 Phase 3 Eval Score 闭环验证

### Phase 3 · Learning Loop(retrospective + Eval Score)(预估 3-4 天)
- 目标:学习闭环跑通
- 关键 milestone:
  - M3.1: retrospective 多触发器(phase / 上下文阈值 / 失败事件 / 周期)
  - M3.2: 回写四目标(AGENTS / skills / rules / 质量门)— 借 idea_gamma2 retrospective 五维 + §2.6 自演进维
  - M3.3: Eval Score micro-benchmark(SWE-bench Pro 5-10 任务子集);review recall/precision metric
- 依赖:Phase 1 + 2 完成
- 风险:eval 任务集代表性差 → 用 retrospective 持续修正

### Phase 4 · L1-L4 重升级路径打磨(预估 2-3 天)
- 目标:high-risk path 文档化 + 项目规模升级触发器
- 关键 milestone:
  - M4.1: 升级触发器规则文档(README + AGENTS.md 嵌入)
  - M4.2: L1-L4 命令链验证(从轻入口可一键升级到 L1 inspire)
  - M4.3: forge 横切层 README 引介(本次 forge 即此机制的成功样例)
- 依赖:当前 ideababy_stroller L1-L4 + forge 已存在
- 风险:对外文档不足导致用户不知道何时升级 — 用 README + tutorial 化解

### Phase 5 · v1.0 polish + Eval pass(预估 1 周,节奏 A)
- 目标:发布前打磨 + 红队测试 Safety Floor
- 关键 milestone:
  - M5.1: Safety Floor 红队测试通过(尝试 9 秒删库式攻击 hard block)
  - M5.2: 5 个真实 PRD 试跑 1 周;review recall ≥ 30%
  - M5.3: 80% 中型项目任务无人工干预完成 build(K1 量化)
- 依赖:Phase 1-4 全部完成
- 风险:发现 Safety Floor 漏洞需回炉 — 留 2-3 天 buffer

---

## §6 · Long-form synthesis(W6)

### 故事线:四套尝试 → SOTA 对照 → 分级 harness 收敛

human 在过去一个月里建了四个项目,本质都在回答同一个问题:**怎么让一个非软件开发背景但能写 PRD 的 human,通过 Claude Code 把 idea 跑成可靠的软件?**

idea_gamma2 是 human 第一次大规模尝试,也是 4 个里"工程纪律最重"的——CONSTITUTION 22+ 条 P0-P5 决策铁律 / SSOT 状态机 / breaking-change 三阶段流程 / interface-contract 五元组 / pipeline SKILL.md 已 v1.2 沉淀 33 条 lesson / phase-retrospective 五维 + §2.6 自演进维。这套体系在 XenoNet 协议这种"协议级数字基建"里非常合适——P 级铁律和 ADR 反引让每个决定都可追溯。但同样的密度直接搬到一个独立开发者的小工具,会变成枷锁。

vibe-workflow 走相反方向:**角色化的精确边界**。10 个 agent 各有清晰的 frontmatter("Allowed write paths" / "refusal rules" / "first principles loop")。code-reviewer 默认怀疑 every line,tech-lead 强制 "no numbers → no recommendation"。这种风格对 already-have-PRD 的中型项目高效,但**对没 PRD 的早期 idea 完全没回答**。

autodev_pipe v3.1 是 human 离 K 诉求最近的一次。Part 0 Deep review 自批 v2 6 大错(AGENTS.md 不是根 / superpowers + agent-skills 同装失效 / cc-spex 桥接成本 / 上下文阈值 / Opus 4.7 tokenizer / Cloudflare 协调者 + 子审分层),撤回 v3 错误论断,Part 1 给三条可选路线 A/B/C 并明确推 A。STARTER_KIT 35 项物化清单标 🟢/🟡/🔵 三档物化度。**P2 SOTA 对标 7 项全部印证 v3.1 §错 1-6 的自批是对的**——Vercel 实证 AGENTS.md 100% / Skills 79% / 56% 不 activate,Anthropic attention budget,Cloudflare 7-子审 + coordinator 30 天 131,246 run,Opus 4.7 tokenizer 1.46x 实测,失败案例 earezki $437 overnight / Magicrails 14k tool-call loop / "$8k-15k per session w/ 49 sub-agents"。**v3.1 已是对齐 SOTA 的设计稿**。

但 v3.1 不是终点。**两件事 v3.1 没说**:第一,idea→PRD 上游(它自己 §0.4 第 1 条诚实承认);第二,**已设计 ≠ 已物化可靠**(GPT 在 P3R1 §3.4 拎出的真分歧)。SWE-PRBench 数据(AI review diff-only 命中 15-31%)+ Cursor + Claude 9 秒删库 + 备份(tomshardware 引证)说明:**设计文档对齐 SOTA 不等于跑起来不出事故**。

当前 ideababy_stroller 的 L1-L4 + forge 横切恰好填这两个缺口。L1-L4 是 idea→PRD 上游(Inspire / Explore / Scope / Plan);forge(本次正在跑的就是它)是元层质量门——双专家审现有产物 + SOTA 对标 + 强制收敛。Anthropic 2026 Trends Report 说 "harness > model upgrade",L1-L4 + forge 正是 harness 工程化的上游延伸。

### 转折点:GPT 的"分级 harness"措辞

P3R1 双方还在"轻 vs 重"的二分里相持。Opus 主张 L1-L4 是默认骨架(填补真实差异化);GPT 主张轻入口优先(让非软件背景用户先跑起来)。如果停在 P3R1,会出双 verdict path。

GPT P3R1 §2 把 verdict 措辞为"**分级 harness framework:轻入口、重升级**"——一个词化解了对立。L1-L4 + forge 不是默认负担,而是 high-risk / idea-incubation / 中大型项目的默认路径;轻入口承载小任务。**Opus P3R2 §1 接受让步**,从"L1-L4 是默认骨架"改为"L1-L4 是 high-risk path 默认"。

GPT P3R2 §1 进一步把分歧 4(autodev_pipe v3.1 = 核心 vs 材料库)做语义合一:**v3.1 是 L4 工程自动化核心资产,不是整个 framework 的本体**;全 framework 本体 = L1-L4 + forge + L4 harness;v3.1 负责提供 L4 的 AGENTS / skills / hooks / approval / cost / review 原料。同时保留 Opus 的"已对齐 SOTA"判断和 GPT 的"已设计 ≠ 已物化可靠"区分。

### 给 human 的总体评估

你的 4 套尝试不是失败 —— 是 4 次正确方向的局部尝试。它们各自缺的不一样:

- **idea_gamma2**:工程纪律完整,但缺轻入口、缺 Safety Floor 显式化、缺 Eval Score 闭环
- **vibe-workflow**:角色边界精确,但缺 idea→PRD 上游、缺 retrospective 学习层
- **autodev_pipe v3.1**:已对齐 SOTA 的 L4 工程纪律设计,但缺物化可靠验证、缺 idea→PRD 上游
- **ideababy_stroller**:L1-L4 + forge 是真差异化,但 L4 build 阶段还薄、Safety Floor 未显式化、cross-model review 未升级到 coordinator

**分级 harness framework 的合一价值**:把 4 次尝试的最佳实践收敛到同一个产物,补齐各自的缺,显式化"什么时候必须人审、什么时候可以全自动"的边界。

### 未来 3-6 月可能的演化路径

- **3 个月**:framework v1.0 ship;1-2 个新独立开发者用轻入口;1 个中型项目用 L1-L4 跑通
- **6 个月**:Eval Score 数据足够沉淀 retrospective lesson;升级触发器自动化(不只是文档,是 framework 检测后建议升级);Safety Floor 红队 case 累积成可发布的 case study
- **9-12 个月**:framework 与 Anthropic Skills / addy osmani agent-skills 生态互通;成为"非软件背景独立开发者"的事实选择之一

---

## What this menu underweights(自批判)

- **反对证据未充分整合**:Cursor + Claude 9 秒删库案例 Opus P2 漏了,GPT 在 P2 §1 row 9 拎出。本 stage 文档已纳入 §"Evidence map" 并升级为 Safety Floor P0 项;但**Opus 漏看本身说明 SOTA 检索深度不一致 — 下次 forge 应在 P2 启动前注入"必查失败案例库"moderator note**
- **Y 视角覆盖盲区**:Y 只选了"产品价值/架构/工程纪律/质量",**未选"安全"**。但 P2-GPT §1 row 9 自然带出 Safety Floor 议题。如果 v2 forge 显式选"安全"视角,会有更系统的安全审计(如:供应链 / 第三方依赖审查 / SBOM / 模型 prompt injection 攻防)
- **K 中未充分回应的关切**:K4 "缺各规模(大中小型)开发流程把握" 在本 verdict 中被收口为"项目规模升级触发器",但**触发器精确定义未给**(仍是 OQ1)。这意味着 human 仍要靠经验判断当前项目属于哪一档
- **convergence_mode 副作用**:preserve-disagreement 模式实际收敛为单一 verdict + 节奏选项,**没有真正出现两条互斥 path** — 这可能是双方都过度妥协的结果。**值得警惕的是**:如果 framework 落地后发现"轻入口 + 重升级"是错的(比如轻入口用户从不升级,实际上是两个分裂的产品),应触发 v2 forge 重新 K
- **X 标的覆盖局限**:本次 X 是 4 个 repo + 1 个 design doc,**未读** Anthropic Claude Skills 仓库源码 / addy osmani agent-skills 仓库源码 / superpowers 仓库源码 — 这三个的实际工程结构如果与文档描述偏差大,本 verdict 会有误判。下次 forge 可加这三个为 X
- **forge versioning 提示**:触发 v2 forge 的信号包括:(a) Phase 1 落地后发现 Safety Floor 三件套有漏洞;(b) Phase 3 Eval Score 数据显示 review recall 长期 < 15%(说明 coordinator MVP 不够);(c) human 实际试用后发现"轻入口"和"重升级"的边界判断比预期难(意味着 OQ1 升级触发器需重做)

---

## Decision menu(for human)

### [A] 接受 verdict 进 L4(需 fork 出 PRD branch)

```
⚠ /plan-start 要求 <prd-fork-id> + 完整 PRD 目录,不能直接吃 forge stage 文档。
⚠ 现有仓库 PRD 都是平铺布局 — discussion/<root>/<prd-fork-id>/PRD.md
   (无嵌套,如 discussion/001/001-pA/PRD.md)
流程(暂时手工,等待 /fork-from-forge 命令落地):

1. 选一个 prd-fork-id(建议:006-pForge 或 006-forgeV1)
   - 由于 006 是 root idea,prd-fork-id 直接放在 discussion/006/ 下(平铺,不嵌套)

2. 创建 discussion/006/006-pForge/PRD.md
   - 把本 stage 中的 §4 "Next-version PRD draft" 抽出
   - 补 frontmatter:
     **PRD-form**: simple
     **Source**: forge stage-forge-006-v1.md

3. 创建 discussion/006/006-pForge/FORK-ORIGIN.md
   说明 forked-from = forge stage,parent = 006(非 L3 candidate)

4. /plan-start 006-pForge
```

⚠ 此选项**进 L4 之前**还需要 human 选**实施节奏 A 或 B**(节奏 A = MVP ≤ 2 周直接 cp v3.1 STARTER_KIT 🟢 项;节奏 B = ≥ 4-6 周 framework 原生重组)。两节奏共享同一 verdict,但 dev plan 节奏不同。

### [B] 跑 forge v2(说明需要补什么)

```
/expert-forge 006
# 在 Phase 0 intake 时调整 X / Y / Z / W / K
# 旧 v1 整目录保留作历史参考
```

适用场景:
- 想加"安全"视角(本次 Y 漏了)
- 想把 Anthropic Claude Skills / addy osmani agent-skills / superpowers 三个仓库源码加入 X
- 想让升级触发器精确定义(OQ1)在 forge 阶段就解决
- 节奏 A 跑了 1 周后发现 v3.1 STARTER_KIT 物化项有缺陷

### [C] 局部接受

- ✅ **采纳**:分级 harness verdict、Safety Floor 三件套(P0)、review coordinator MVP、AGENTS.md 根上下文、L1-L4 + forge 保留
- ⏸ **挂起**:Eval Score micro-benchmark(P1 — 等节奏 A Phase 3 决定 task corpus)、retrospective 多触发器细节(等 idea_gamma2 retrospective 移植路径明确)
- ❌ **拒绝**:(空 — 本 verdict 没有强烈拒绝项;若 human 有,可在此处覆盖)

### [P] Park

```
/park 006
```

保留所有 forge v1 产物,标记暂停。复活时不重做这一层。适用:human 决定先把 idea_gamma2 Phase 5 跑完再回来做 framework。

### [Z] Abandon

```
/abandon 006
```

forge verdict 显示该 idea 不该继续做。归档 lesson 文档。**不建议本次** — verdict 锐利且 K 全 6 子条已对齐;abandon 会丢掉 4 套尝试的合一价值。

---

## Forge log

- v1: 2026-05-08 — verdict: "构建基于 Claude Code 的分级 harness framework — 轻入口、重升级;可靠 = Safety Floor + Deterministic Feedback + Learning Loop 三层"
