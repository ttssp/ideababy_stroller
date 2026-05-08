# Proposals

每个 idea 在这里登记。**写一句话 idea 描述就够了**——更多内容是 L1 inspire 阶段两个顶尖模型的事，不是你这阶段要操心的。

## 怎么用

每个 proposal 用 `## **NNN**: <一句话标题>` 开头（NNN 是 3 位编号）。下面用模板。

**重要**：模板里只有"标题 + 一段话想法"是必填，其他字段全部可选。不写 = 没想清楚或不想约束 = L1 阶段模型会帮你想，不会逼你补。

<!-- ---

## 极简模板（最常见用法）

```markdown

---

## **NNN**: <一句话标题>

**提出日期**: YYYY-MM-DD
**状态**: draft

### 想法 (必填)
<plain language describing what's in your head — 一两句话也行，几段也行>

```

---

## 详细模板（如果你已经想得比较深，这些字段都可以填）

下面字段**全部可选**——填了模型会重视，不填模型会自己探索：

```markdown

---

## **NNN**: <一句话标题>

**提出日期**: YYYY-MM-DD
**状态**: draft

### 想法 (必填)
<plain language>

### 我为什么想做这个
<触发这个 idea 的真实原因——你遇到的痛、你看到的机会、你的好奇心来源>

### 我已经想过的角度
<避免 L1 inspire 重复你已经想过的方向>

### 我已知的相邻方案/竞品
<如果你已经知道某些做过类似事的人/产品，写下来——L1 模型会用这做起点>

### 我的初始约束
<预算 / 时间 / 平台 / 必须用什么 / 不能用什么——这些会在 L3 scope 阶段重要，但 L1/L2 会忽略>

### 我的倾向
<如果你已经有方向偏好，说出来——但要知道 debater 会挑战你>

### 还在困扰我的问题
<你的真诚 unknown——L1 inspire 阶段的模型会优先解答这些>

```

---

## 状态字段含义

| 状态 | 意思 |
|---|---|
| draft | 刚写完,还没启动 inspire |
| inspiring | L1 进行中 |
| menu-ready | L1 完成,待 fork |
| exploring | L2 进行中（含某个 fork 在 L2 阶段） |
| scoping | L3 进行中 |
| planning | L4 进行中（spec/dev plan） |
| building | 实际开发中 |
| shipped | 上线 |
| parked | 暂搁,有复活条件 |
| abandoned | 放弃,有 lesson 文档 |
| forked | 已分支为多个子 idea，本身归档 |

---

## Ambition 等级（可选标注）

| 级别 | 意思 | 典型时长 |
|---|---|---|
| S | 脚本或一次性工具 | 0.5–3 天 |
| M | 单一用途工具或小 CLI | 1–3 周 |
| L | 完整 SaaS 产品 | 4–10 周 |
| XL | 平台级（IM、协议、完整 iOS/Android app） | 8–20+ 周 |

不强制——L1/L2 会自己估，你不必先定。 -->

---
## **001**: Research Radar

**提出日期 / Proposed**: 2026-04-22
**状态 / Status**: exploring (L2 进行中，基于原 proposal；L1 menu 的 13 条 directions 保留作为灵感库，以后可随时 `/fork` 任意一条。历史 park 记录见 [PARK-RECORD](../discussion/001/PARK-RECORD.md)）
**初始野心等级 / Ambition**: M
**成熟度 / Idea maturity**: direction-clear

### 想法 (必填)
我希望做一个research radar，会自动发现、跟进最新的AI领域研究工作

### 我为什么想做这个
近年来AI research工作呈井喷式增长，新的工作层出不穷。
单靠个人来读文章/Blog/Repo已经远远跟不上了。
我觉得读文章，跟进最新的research还是有所谓的“套路”的，加之现在的LLM能力越来越强，跟进research这种高级的“pipeline”是有极大可能实现的

### 我已经想过的角度
我需要一个“research radar”，它能够：
1. 自动检测arxiv的文章、顶会（如nips, icml, iclr等）的文章、顶尖学术机构/巨头实验室/创业公司（deepmind, thinkingmachines, anthropic等）的blog，github 高潜力的repo等
2. 检测到的新工作（文章/blog/repo）后，会进行下载、解析、解读、分析（novelty, impact, 实用性）等操作
3. 构建我的知识库：
   - 知识库会维护一个topic标签库，topic会按由大到小、由广到窄延伸多个层级；
   - 新的工作如果有价值，则将其归纳总结到知识库中；如果价值一般或者没有价值，留个痕（以防遗漏关键）
   - 知识库支持多种形式的检索和查看，比如，可以考虑按一个时间线梳理，也可以不同工作的同源、延伸、对立、渊源、继承关系等等；又如，该知识库可以针对最新工作实时更新当前topic的SOTA水平/状态
   - 有主动搜索补充的能力，比如用户给一个新工作，之前如果没有相应的topic，会新建一个topic，并且主动搜索把相关的重要工作补齐
4. 上述的分析、解读、处理的能力可以依赖大模型能力
5. 核心是：该radar能够发现并及时跟进新工作，跟进完工作有能力整理、梳理、总结归纳这些进展，为后续的brainstorm / research 提供**可靠、前瞻**的判断
6. 我们实验室覆盖的内容比较广，我希望长期可以聚焦在8~15个topic
7. research的preference和taste可以考虑让一个智能体去自主学习（收集X上的观点+证伪/证实+辩证的讨论），也可以考虑在和我的长期交互中调整学习

### 我已知的相邻方案/竞品
Karpathy最近的autoresearch让我印象深刻，那个项目是给定一个任务，一段代码，一个明确的metric，agent自己会实验，想idea，重复实验，直到突破；anthropic最近做了一个用9个opus做research的实验，也很有意思。就是9个opus自己讨论自己构思自己实验。
我希望**最终目标**能结合这些研究智能体的优势，构建一个我们lab的research agent。这个idea就是第一步，只有对现有的工作有很深的理解才有可能找到/想到有趣的题目有价值的课题。所以我想先从第一步开始。

### 我的倾向
没有特别的倾向，最终是希望构建一个研究智能体，我希望先把前置的跟进research，梳理研究脉络，保持高水准的理解这些基础先做好。


---

## **002**: 每天赚100美元

**提出日期**: 2026-04-23
**状态**: L1 done · 3 forks in L2 pending
**初始野心等级**: M
**成熟度**: vague
**L1 菜单**: [stage-L1-inspire.md](../discussion/002/L1/stage-L1-inspire.md)(crypto pivot 版 · 非-crypto 版已归档)

### 想法
不贪多，有什么办法可以让我每天赚100美元。前提，依靠电脑作为生产工具。

### Active forks(已从 L1 菜单分叉,待进 L2)
- **002b-stablecoin-payroll** — 稳定币发薪管家(routine 服务)
- **002f-payroll-er** — 发薪事故急诊室(acute 伴生)
- **002g-dao-bounty** — DAO bounty 技能市场(skill fallback · 启动期现金流兜底)


---
## **003**: PARS · 并行自动化研究智能体系统

**提出日期**: 2026-04-24
**状态**: L3-scoping-existing-design

### 想法
已有成熟 L4 级设计(discussion/003/L2/stage-L2-explore-003.md)。对抗审
已完成(discussion/003/L3/moderator-notes.md)。现在通过 L3 Scope 层,让模型独立产出 scope candidates,和现有设计对比,
看是否漏了别的切法。独立产出后，审视当前"14 周 × 6 人 × 这个范围"是不是最好切法,产出候选 scope 菜单对比现有设计。

### 我已知的相邻方案/竞品
Karpathy的autoresearch

---

## **004**: 个人投资顾问+投资助手智能体

**提出日期**: 2026-04-24
**状态**: draft

### 想法 (必填)
做一个我个人的智能投资顾问+投资助手

### 我为什么想做这个
人到中年，以前只想着安心上班赚工资，忽略了投资理财这个保值增值的部分。现在世界变化太快，没有所谓的铁饭碗。尤其是经济大环境下行，人口下降，世界秩序日渐混乱，我需要为整个家庭的生活质量负责。

### 我已经想过的角度
不求发大财，可以承受20%的风险，希望可以合理配置仓位，获得相对稳健的收益率
我有machine learning方向的cs PhD，对“预测”模型，ai模型都很熟悉。
我微信上付费订阅了一个投资顾问的账号，他会每周给一些周度策略，盘前盘后的技术分析，以及一些业内“共识”或“看法”，这个人哥大毕业，曾在美国的专业机构任职很多年。近几年回国了。
我初步的想法是，获得多个数据源，技术分析，结合该投资顾问的消息，做一个我个人的投资分析智能体，辅助我做出争取的投资决策。我知道个人做不了量化，我想的是可以尝试赚点小量的beta也可以。如果有好的策略吃波动我就很知足。
我现在可以买美股港股和a股。


### 我已知的相邻方案/竞品
我知道github上有很多类似的idea，应该都没法直接实战。这些repo的有价值的想法也请你多调研下

### 我的初始约束
我愿意为数据付费每年500美金，其他的数据尽量能自己搞定。每个股市集中看30～50只股票

---

## **005**: auto agentic coding

**提出日期**: 2026-05-06
**状态**: menu-ready

### 想法 (必填)
给定一个PRD，claude code可以几乎没有人工干预的情况下自主完成开发任务。我需要一个**可靠的、自动化程度最高**解决方案。

### 我为什么想做这个
我是非软件开发背景。我可以将需求描述清楚，我也可以尝试构建较可靠的PRD。但是我缺少软件开发的经验，对各个规模（大中小型）的开发的方案、流程、规范等内容都没有把握。

### 我已经想过的角度
我最近一个月做了很多尝试：
1. 第一个项目名idea_gamma2, @/Users/admin/codes/idea_gamma2 . 这个项目对我来说是一个大型项目，主要是构建一个人+agent共存的数字基建（通讯协议）。我尝试着梳理我的想法，并制定了一个technology roadmap @/Users/admin/codes/idea_gamma2/docs/_archive/technology_roadmap.md . 我会将开发分成几个phase来实现。每个phase开发前，我会用 @/Users/admin/codes/idea_gamma2/.claude/skills/pipeline/SKILL.md 生成 playbook，然后让claude code按照playbook去实现。每个phase结束后，会用 @/Users/admin/codes/idea_gamma2/.claude/skills/phase-retrospective/phase-retrospective-skill.md 更新 pipeline skill. 每个phase都会定制相应的subagent @/Users/admin/codes/idea_gamma2/.claude/agents，此外还构建了一部分skills @/Users/admin/codes/idea_gamma2/.claude/skills 

2. 第二个项目为vibe-workflow @/Users/admin/codes/vibe-workflow/。我是通过一个engineer team协作完成自动化开发。核心内容可以参考 @/Users/admin/codes/vibe-workflow/.claude/ 

3. 第三个项目是autodev_pipe @/Users/admin/codes/autodev_pipe 。该项目设计初衷是希望借鉴社区的vibe coding/agentic coding的最佳实践，实现一个agent自动化开发的piepline。 调研的一些结论、设想和计划记录在 @/Users/admin/codes/autodev_pipe/solo_ai_pipeline_v3.1.md 。其中主要借鉴最近流行的addy osmani的agent-skills，据说这套skills是把多年在 Google 级工程体系中沉淀出的工程纪律，迁移到 AI agent，让模型不只是更快地产出代码，而是在规格、测试、评审、验证和发布约束下产出更可信的软件。此外，本项目也吸收了superpowers的部分skills。核心目的是借助这些skills打造”专业的自动化开发流程“
   
4. 第四个项目为当前repo。核心是为尝试将一个idea转化成一个成型的产品/软件。本repo在idea成型（产出PRD）后，会进入自动开发阶段。

### 我诉求
我希望双方凭借最强的AI专业能力以及最丰富的软件开发经验，通过调研、论证、思辨、构思、设计、整理归纳等方式，达成一套基于claude code实现**可靠**自动化开发的framework/pipeline的共识方案

--- 

## **006**: auto agentic coding

**提出日期**: 2026-05-06
**状态**: menu-ready

### 想法 (必填)
给定一个PRD，claude code可以几乎没有人工干预的情况下自主完成开发任务。我需要一个**可靠的、自动化程度最高**解决方案。

### 我为什么想做这个
我是非软件开发背景。我可以将需求描述清楚，我也可以尝试构建较可靠的PRD。但是我缺少软件开发的经验，对各个规模（大中小型）的开发的方案、流程、规范等内容都没有把握。

### 我已经想过的角度
我最近一个月做了很多尝试：
1. 第一个项目名idea_gamma2, @/Users/admin/codes/idea_gamma2 . 这个项目对我来说是一个大型项目，主要是构建一个人+agent共存的数字基建（通讯协议）。我尝试着梳理我的想法，并制定了一个technology roadmap @/Users/admin/codes/idea_gamma2/docs/_archive/technology_roadmap.md . 我会将开发分成几个phase来实现。每个phase开发前，我会用 @/Users/admin/codes/idea_gamma2/.claude/skills/pipeline/SKILL.md 生成 playbook，然后让claude code按照playbook去实现。每个phase结束后，会用 @/Users/admin/codes/idea_gamma2/.claude/skills/phase-retrospective/phase-retrospective-skill.md 更新 pipeline skill. 每个phase都会定制相应的subagent @/Users/admin/codes/idea_gamma2/.claude/agents，此外还构建了一部分skills @/Users/admin/codes/idea_gamma2/.claude/skills 

2. 第二个项目为vibe-workflow @/Users/admin/codes/vibe-workflow/。我是通过一个engineer team协作完成自动化开发。核心内容可以参考 @/Users/admin/codes/vibe-workflow/.claude/ 

3. 第三个项目是autodev_pipe @/Users/admin/codes/autodev_pipe 。该项目设计初衷是希望借鉴社区的vibe coding/agentic coding的最佳实践，实现一个agent自动化开发的piepline。 调研的一些结论、设想和计划记录在 @/Users/admin/codes/autodev_pipe/solo_ai_pipeline_v3.1.md 。其中主要借鉴最近流行的addy osmani的agent-skills，据说这套skills是把多年在 Google 级工程体系中沉淀出的工程纪律，迁移到 AI agent，让模型不只是更快地产出代码，而是在规格、测试、评审、验证和发布约束下产出更可信的软件。此外，本项目也吸收了superpowers的部分skills。核心目的是借助这些skills打造”专业的自动化开发流程“
   
4. 第四个项目为当前repo。核心是为尝试将一个idea转化成一个成型的产品/软件。本repo在idea成型（产出PRD）后，会进入自动开发阶段。

### 我诉求
我希望双方凭借最强的AI专业能力以及最丰富的软件开发经验，通过调研、论证、思辨、构思、设计、整理归纳等方式，达成一套基于claude code实现**可靠**自动化开发的framework/pipeline的共识方案

---

## **007**: friction-tap · 摩擦点速记 CLI

**提出日期**: 2026-05-08
**状态**: draft

### 想法 (必填)
一个超薄 CLI:`friction <message>` 自动把 `<UTC ISO timestamp> - <message>` append 到当前仓库的 `docs/dogfood/v4-friction-log.md`(若不存在就创建)。目标是**让 V4 dogfood 阶段记录工具链摩擦点的成本降到零** — 当下不记 = 后面再也想不起来;记需要 5 步 = 也不会真记。

### 我为什么想做这个
forge 006 路径 2 的 4 周 playbook 在 W2 step 4 明确要求"每次 V4 retrospective skill 跑得不顺畅就 jot 一笔到 friction-log"。但当前没有 ergonomic 工具,operator 必须 (1) 切到 docs/dogfood/ (2) 找 v4-friction-log.md (3) 算 ISO timestamp (4) append (5) 保存。这 5 步在"刚被工具坑了一下"的当下 90% 概率会被跳过 → friction-log 长期空 → checkpoint-01 没素材 → V4 dogfood 信号被稀释。

### 我已经想过的角度
- **不要做成跨仓自动检测最近 friction-log** — 太复杂;先做"显式指定路径或当前 cwd 找最近的"两条规则就够
- **不要做 GUI / TUI** — 摩擦记录工具自己有摩擦就废了,纯 CLI 一行命令最好
- **不要做云同步** — friction-log 是仓库内文档,跟 git 走

### 我已知的相邻方案/竞品
- `dlog` / `note` 类 CLI 太多,但都是通用 note tool,不专门挂 friction-log 语义
- shell alias `frictlog` 自己一行 echo + redirect 也能做,但容易写错路径 / timestamp 格式

### 我的初始约束
- 实现:Python 单文件 + `~/bin/friction` 软链(或直接用 bash)
- 时间:1 周内 L1 → L4 → ship v0.1
- 平台:macOS 本机(operator 工作环境)
- 必须用 UTC ISO 8601 timestamp(跟 v4-friction-log.md 既有格式一致)

### 我的倾向
Python(可读性)优于 bash;单文件 ≤ 100 行;无第三方依赖(stdlib only)。

### 还在困扰我的问题
- "找最近的 friction-log"在仓库 / 不在仓库两种情况怎么处理?`cwd 不在 git 仓库就 fallback 到 ~/.claude/global-friction-log.md` 还是 `直接报错让 operator 显式 -f`?
- 是否要加 `friction --tail N` 看最近 N 条?(可能超出 v0.1 scope)

---
