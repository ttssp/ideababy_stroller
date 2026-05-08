# Forge v1 · 006 · P1 · Opus47Max · 独立审阅(no search)

**Timestamp**: 2026-05-07T15:08:00Z
**Searches used**: NONE in this round.
**Visibility**: I did NOT read other reviewer's P1.
**Reviewer stance**: 审阅人 — 评判已存在物,不是 daydream。

---

## 0. 我读到的标的清单 + 阅读策略

### 0.1 K(用户判准)摘要

human 是非软件背景、能写较可靠 PRD 但缺各规模项目开发流程经验。诉求:**双方凭借专业能力 + 软件开发经验,通过调研、论证、思辨、构思、设计,达成"基于 claude code 实现*可靠*自动化开发的 framework/pipeline 共识方案"**。判准锚点:**可靠** + **自动化程度最高**。已亲历 4 个项目尝试(idea_gamma2 / vibe-workflow / autodev_pipe / 当前 repo)以摸索此 framework。本次 forge 是横切审阅(preserve-disagreement 模式,允许双轨产出)。

### 0.2 标的清单(11 项, prefill bundle: pure-idea)

**已读(11/11 全部 reachable)**:

| # | 标的 | 我读了什么 |
|---|---|---|
| 1 | proposal-text(§006:想法+我为什么+我已经想过的角度+我诉求) | 已在 forge-config + prefill draft 中 verbatim 引用 |
| 2 | `/Users/admin/codes/idea_gamma2`(顶层) | `ls` 顶层 → README + CLAUDE + CONSTITUTION |
| 3 | `idea_gamma2/docs/_archive/technology_roadmap.md` | 前 80 行(三大基石 + 通讯层架构图 + 5 设计原则 + AID 数据模型) |
| 4 | `idea_gamma2/.claude/skills/pipeline/SKILL.md` | 前 150 行(版本变更表 v0→v1.2 + 7 步执行流程 + Step 0/1/2 详细) |
| 5 | `idea_gamma2/.claude/skills/phase-retrospective/...` | 前 120 行(触发 + 5 维偏差 + §2.6 自演进维) |
| 6 | `idea_gamma2/.claude/agents/`(21 agent) | ls 全部文件名 + 抽样(je-* / arch / gatekeeper) |
| 7 | `idea_gamma2/.claude/skills/`(12 SKILL) | ls 全部 + breaking-change SKILL.md 前 40 行 |
| 8 | `/Users/admin/codes/vibe-workflow/`(顶层) | `ls` 顶层 + README 前 80 行(AlphaFlow 项目自身 = Workflow Builder/Compiler) |
| 9 | `vibe-workflow/.claude/`(10 agents + 11 commands + 7 rules + 4 skills) | ls 全部 + CLAUDE.md 前 100 行 + ai-fullstack-developer.md 前 100 行 + tech-lead.md 前 80 行 + code-reviewer.md 前 60 行 |
| 10 | `/Users/admin/codes/autodev_pipe`(顶层) | `ls` 顶层 |
| 11 | `autodev_pipe/solo_ai_pipeline_v3.1.md` | 前 270 行(v3 撤回声明 / Part 0 deep review / Part 1 三条路线 / 1.3 路线 A 详细) + STARTER_KIT.md 前 80 行 |

**跳过的**:无。Codex 沙箱可能 BLOCK 4 个外部 repo dir,但本机 Opus 全部读取成功。

### 0.3 阅读策略

按 4 个 Y 视角分配深度:**Y2 架构设计 + Y3 工程纪律**优先看 `.claude/skills/` `.claude/agents/` `.claude/commands/` 与 pipeline SKILL 的 step 结构(本轮主战场);**Y1 产品价值**优先看 README/CLAUDE.md/总设计文件;**Y4 开发质量保障/稳定性/SOTA 对标度**留给 P2 深入(本轮做"先识别已有机制 → 不评分"准备工作)。

### 0.4 X 解读关键澄清(§006 表面 vs 真实意图)

`§006 我已经想过的角度 1/2/3` 字面让"对照 idea_gamma2 / vibe-workflow / autodev_pipe 三个项目本身",但**这三个项目的本体(XenoNet protocol / AlphaFlow Workflow Builder / autodev_pipe 自身代码)与"agentic coding framework"是同源不同物**:idea_gamma2 = 协议级产品 + 用 `.claude/` 体系开发它;vibe-workflow/AlphaFlow = Workflow Builder + 用 `.claude/` 团队 agents 开发它;autodev_pipe = 把"agentic coding pipeline"当成产品来做(即 §006 "framework" 本身)。**X 真正可吃的是这 3 个项目的 `.claude/` 工作流元数据**(skills/agents/commands/rules)+ autodev_pipe `solo_ai_pipeline_v3.1.md` 设计文档。本审阅以此为基础。

---

## 1. 现状摘要(按 Y 视角组织 — 只描述,不评价)

### 视角 Y1 · 产品价值

**human 已亲历的"用 claude code 自动化开发"3 套现实**:

- **idea_gamma2**:为 XenoNet 协议 6 层 monorepo 服务的工程化体系。**任务粒度**已细到"phase[N]-task-breakdown §〇.0 SSOT 状态机"+ je-a..h 多通道并行 worktree。CLAUDE.md §"工作流"显示成熟分工:`Opus 规范 / Codex review / GLM JE 批量实现 / Haiku 类型`,提交格式 `feat(JE-X-NN): <title>`。已迭代到 Phase 4.5(W34-W44 主线 3 + Python SDK,8-11 周)。CONSTITUTION.md 22+ 条 P0-P5 决策优先级 + Phase 实战案例反引(如 W19 F1/W18 wire-format/ADR-014)。
- **vibe-workflow/AlphaFlow**:产品本身是 Workflow Builder。`.claude/` 里把 SOTA agent role 模型固化:**10 个 agents(ai-fullstack-developer / tech-lead / code-reviewer / dev-plan-reviewer / design-review / system-reviewer / devops-engineer / llm-engineer / test-engineer / delivery-tracker)**, 每个 agent frontmatter 极详细(model/effort/tools/role/operations/allowed write paths/bootstrapping/refusal rules)。code-reviewer 支持 diff/full-repo 双模 + `--lens=testability` 信号加权。
- **autodev_pipe**:本仓库是 `solo_ai_pipeline_v3.1.md`(63 章节级 design doc)+ 物化 STARTER_KIT(35 项文件清单,标 🟢/🟡/🔵 三档物化度)。**v3.1 内容贴近 §006 诉求**:Part 0 自批 v2 6 大错(§0.2 错 1-6)+ 撤回 v3 错误论断(关于 superpowers + agent-skills 同装失效);Part 1 给三条可选路线(A: 起步 / B: 熟练后切 / C: 不推荐);把 AGENTS.md 立为根上下文 + 引用 Vercel 实测 8KB AGENTS.md 命中率 100% vs Skills ≤79%。

human 诉求"非软件背景 + 强 PRD 描述能力 → 接近无人工干预产出 production-ready 软件"在三处尝试中**都已部分兑现但未对齐为统一框架**。

### 视角 Y2 · 架构设计

三个项目的**抽象层次**显著不同:

- **idea_gamma2 = SKILL+AGENT+TASK-BREAKDOWN 三层**。SKILL 是元层执行 SOP(如 pipeline SKILL §"7 步流程");AGENT 是角色专家(arch / je-* / gatekeeper);**真正的 phase-specific 内容不写在 SKILL 里而在 task-breakdown(SSOT)**。pipeline SKILL.md §"原则:skill 不硬编码 Phase 特有内容"是关键约束,SKILL 只定义"怎么读、怎么用",Phase 特有内容全在 CONSTITUTION + task-breakdown + ADR 里。
- **vibe-workflow = AGENT 中心 + SKILL 围绕**。10 agents 是核心抽象;skills(4 个:align-architect / dev-plan-from-architecture / dev-plan-apply-review / dev-plan-review-loop)只服务 dev-plan 工作流;commands(11 个)是 user-facing slash 命令。**AGENT 自身有 bootstrapping 机制**(扫 manifest / 写 `.claude/<agent>.config.json`)— 把项目形态 detection 内化到 agent 而不是 SKILL。
- **autodev_pipe = 设计稿 + STARTER_KIT 双重身份**。layered design 在文档里(v3.1 §0-§7);代码仓库本身是物化模板(`templates/AGENTS.md / CLAUDE.md` 是带 `<TODO>` 占位的纯模板,根目录的 AGENTS.md 是开发本仓库专用版)。`.claude/skills` 含 numerical-claims-verifier(共享 skill,金融+算法项目通用)+ retrospective(三级 L1/L2/L3)。

**当前 ideababy_stroller 仓库的 4 层 Inspire→Explore→Scope→Plan + forge 横切层**是第 4 套抽象,其结构与上述 3 套不重合(idea_gamma2/vibe-workflow/autodev_pipe 都没有 L1-L4 的 idea-incubation 层,它们都假设已有 PRD 起点)。

### 视角 Y3 · 工程纪律

**纪律密度**对比:

- **idea_gamma2**:5 个 P 级铁律(P0 使命 / P1 安全 / P2 SSOT / P3 breaking 流程 / P4 通道 / P5 灰色地带)+ G1-G14 灰色地带协议;pipeline SKILL.md v1.2 已沉淀 33 条 retrospective lessons(A1-A33);phase-retrospective SKILL §2.6 "pipeline skill 自身演进偏差"维补五维盲区。**核心机制**:Phase 验收 → retrospective 五维分析 → 候选教训 → 回写 SKILL/CONSTITUTION,有强制条款"沉默跳过的反馈条目下个 Phase 一定原样重蹈"。
- **vibe-workflow**:每 agent frontmatter 显式声明 "Allowed write paths"(write freely / 需 explicit confirmation / refuse to write,name the rule and stop);code-reviewer 默认 "skepticism on every line";tech-lead "first principles loop:restate → decompose → quantify → name dominant constraint → enumerate 2-3 options → recommend with falsifying test"。`.claude/rules/` 7 条独立规则文件(change-safety / data-modeling / error-handling / llm-integration / python-style / security / testing)。
- **autodev_pipe v3.1**:把质量重心从"规范约束层"转移到"确定性反馈层"(`pre-commit + property-based testing + spec-validator + check-spec-review + check-constraint-references` 三件套);hooks 100% 可靠 vs prompts 80%;cost control 三层(`caching → routing → 熔断`);`.github/workflows/budget.yml` 每 15 分钟跑 kill_switch.py。

### 视角 Y4 · 开发质量保障 / 稳定性 / SOTA 对标度

(本轮独立审阅,**不跑搜索**;本节仅识别 X 内已有的"reliability/stability"机制,SOTA 对标留给 P2)

X 内已存在的"可靠性"机制清单:

- **idea_gamma2**:`fail-closed 默认`(P1.1)/ `wire-format = canonicalized JSON`(P1.3)/ `ledger 追加写不可篡改`(P1.4)/ Codex 对抗审查 cap 监控(retrospective A27-A28)/ acceptance script CI 真跑(A26)/ fetch mock 漂移检测(A33)/ partial-acceptance verdict + tag 后缀规则(A30-A31)。
- **vibe-workflow**:`tech-lead.first-principles-loop` 强制 "no numbers → no recommendation"(quantify 步)/ design-reviewer 做 doc-vs-code claim verification / code-reviewer 默认怀疑 every line / dev-plan-reviewer + dev-plan-apply-review 双层 review。
- **autodev_pipe v3.1**:Stage 0 强制 prompt caching `cache_control` 断点(96% 命中观测) / 双 plugin SessionStart 冲突 → 路线 A 单 hook + 5 个手动 cp 5 superpowers skill(预测可控)/ "300-400K token = 上下文腐化阈值,40% 利用率进入愚蠢区间"显式约束 / "49 个 sub-agent / $8k-15k 单次 / 23 sub-agent 3 天烧 $47k 失败案例"作为成本上限警示 / Cloudflare 协调者+子审查者分层(7 子审 + Opus/GPT 协调)。

---

## 2. First-take 评分(按 Y 视角)

| Y 维度 | 倾向 | 理由(引用 §1 现状) |
|---|---|---|
| Y1 产品价值 | **refactor + new** | 三个项目部分兑现"非软件背景 → production-ready"诉求(autodev_pipe v3.1 最贴),但**没有任何一个**完整覆盖 idea→PRD 阶段 + 各规模项目的差异化 patch。当前 ideababy_stroller 的 L1-L4 框架填了 idea→PRD 缺口(autodev_pipe v3.1 §0.4 第 1 条明列"v2 完全没说的:Idea→PRD 阶段")— 这是真实价值。**refactor**:把 autodev_pipe 的 STARTER_KIT 物化思路 + idea_gamma2 的 task-breakdown SSOT + vibe-workflow 的 agent 角色专精度,合并成一套。**new**:L1-L4 四层 + forge 横切是新颖切法,需在 framework 中保留。 |
| Y2 架构设计 | **refactor**(强烈) | 三套抽象不重合 — idea_gamma2 SKILL+AGENT+TASK-BREAKDOWN 三层 / vibe-workflow AGENT-中心 + agent 自 bootstrap / autodev_pipe 设计稿+STARTER_KIT 双重身份。但**核心抽象单元在三套里都收敛到 agent + skill + slash command + rules + AGENTS.md/CLAUDE.md**。共识方案应明确:(a) AGENTS.md 是根上下文(autodev_pipe v3.1 §错 2 + Vercel 实测);(b) skill ≠ task-breakdown,skill 不硬编码 phase 内容(idea_gamma2 pipeline SKILL.md 原则);(c) agent 应有 bootstrap + persist config 机制(vibe-workflow 模式)。**reliability 机制**(fail-closed / SSOT / breaking-change 流程)不能是 idea_gamma2 一家的私有约定,必须是 framework 内置。 |
| Y3 工程纪律 | **keep + refactor** | 三套都有强纪律但**风格冲突**:idea_gamma2 = 论证密集型(每条 P 都引 ADR/Phase 实战案例);vibe-workflow = 角色级精确边界(agent 显式 refuse list);autodev_pipe = 反馈层优先(hooks 100% 可靠 > prompts 80%)。共识 framework 应:(a) **keep** 三套各自核心 — pipeline SOP + agent role 边界 + 反馈层 hooks;(b) **refactor** 元层"如何让纪律不被忘记":idea_gamma2 retrospective + 候选教训沉淀机制是 SOTA 候选(回写 SKILL.md 强制 + 沉默条目下 Phase 重蹈),应在 framework 中标准化。 |
| Y4 开发质量保障/稳定性/SOTA 对标度 | **暂判 refactor + 留 P2 SOTA 验证** | 三套已有的可靠性机制(fail-closed / property testing / cost kill switch / 上下文腐化阈值 / 协调者+子审查者分层)是合理基线,但是否达到当下 SOTA 需要 P2 检索 cursor / aider / claude-code agentic / SWE-agent / Anthropic skills 验证。**当前 ideababy_stroller 的 L4 build worktree + cross-model review 机制**(根 CLAUDE.md "L4 quality gates")是另一类候选机制,需 P2 与 SOTA 对照。**初步立场**:refactor — 不要从零设计可靠性,refactor autodev_pipe v3.1 的"反馈层 + 路线 A"作为基线,叠加 idea_gamma2 retrospective + vibe-workflow agent 边界 + ideababy_stroller L4 cross-model review。 |

---

## 3. 我现在最不确定的 3 件事(留给 P2 / P3)

1. **autodev_pipe v3.1 三条路线(A/B/C)的 SOTA 对标度** — v3.1 §1.1 给出 A(agent-skills + 5 个 cp)/ B(双 plugin)/ C(spec-kit + cc-spex 桥接)三选一;但 cc-spex 76 stars 单一维护者、addy osmani agent-skills 在 GitHub 高速演进中、superpowers 与 GSD 冲突 v3 误读后 v3.1 撤回。**P2 我希望搜索**:2026-Q1/Q2 后 cursor/aider/claude-code/cline/copilot agent mode/Anthropic skills 在实际项目落地中是否真有"路线 A 优于 B/C"的实战支持;Vercel "8KB AGENTS.md 命中率 100% vs Skills ≤79%" 数据是否在 SWE-bench / aider polyglot benchmark 重现。

2. **idea_gamma2 retrospective 机制是否可移植** — pipeline SKILL.md 已 v1.2 + 33 条 lesson;phase-retrospective SKILL 的"5 维 + §2.6 自演进维"看起来强但**需要 phase-accepted tag + acceptance-report.md** 这种重型基础设施。对 §006 诉求的"非软件背景独立开发者",这种重度纪律可能反而是阻力。**P2 我希望对方告诉我**:在没有"phase 验收"概念的小型/中型独立项目里,retrospective 机制要降级成什么形态(每周?每个 PRD?)?如果按 autodev_pipe v3.1 §3.9 引"上下文腐化阈值 300-400K token"作为触发,而非"phase tag",可行性如何?

3. **L1-L4 + forge 横切层的"严肃性 vs 易用性"权衡** — 当前 ideababy_stroller 的 L1-L4 已成型(L1 Inspire daydream, L2 Explore deep unpack, L3 Scope real-PRD, L4 Plan→spec→tasks→build);forge 横切允许双专家审 X(本次 forge 即此);但**对非软件背景 human**,L1-L4 是不是过重?能不能压缩到 L1+L3+L4 三层,L2 并入 L1 末段?或反方向:L1-L4 是 framework 的关键差异化,**应保留并完整 documented in README**(autodev_pipe v3.1 §0.4 第 1 条恰好认证 idea→PRD 阶段是"v2 完全没说的"缺口)。**P3 期望**:对方对 L1-L4 是否值得作为 framework 默认骨架给出立场。

---

**字数统计**:正文 ~1380 字(扣表格、code block、heading)。符合 800-1500 边界。
