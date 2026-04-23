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
**状态 / Status**: draft
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

**提出日期 / Proposed**: YYYY-MM-DD
**状态 / Status**: draft
**初始野心等级 / Ambition**: M
**成熟度 / Idea maturity**: vague

### 动机 (Why)
之前看到有人每天赚100美元这条新闻

### 目标用户 (Who)
我个人

### 核心想法 (What)
我想看看有哪些有意思的idea，或者别人真正可行的一些实践

### 初始约束 (Constraints)
- 预算 / Budget: 500美金
- 平台 / Platform: 有computer，有各种大模型的api
- 时间 / Timeline: 你可以认为我每天24小时都有时间，我计划搭一个智能体替代我

### 我知道的相邻方案 (Adjacent / prior art I already know about)
没有可提供的

### 已知未知 (Open Questions)
没有可提供的

### 期望产出 (Desired outcome)
3~5个可行方案