# Proposals

Every idea in this incubator lives here first. Keep entries concise — 10 minutes max.
Detail emerges later, during debate and spec.

## Format

Each proposal starts with `## **NNN**: <one-line title>` where NNN is a zero-padded
3-digit number. Use the template below.

<!-- ---

## Template (copy me)

```markdown

---

## **NNN**: <one-line title>

**提出日期 / Proposed**: YYYY-MM-DD
**状态 / Status**: draft | exploring | position-checkpoint | building | shipped | parked | abandoned | forked
**初始野心等级 / Ambition**: S / M / L / XL
**成熟度 / Idea maturity**: vague | direction-clear | fully-formed

### 动机 (Why)
Why does this need to exist? What real problem does it solve? If the world already
works without it, why bother?

### 目标用户 (Who)
Specific. "Developers" is too vague; "TypeScript devs on macOS who build iOS side-projects"
is usable.

### 核心想法 (What)
One paragraph. Plain language. No jargon. If you can't describe it in a paragraph,
you don't understand it yet.

### 初始约束 (Constraints)
- 预算 / Budget:
- 平台 / Platform:
- 时间 / Timeline:
- 必须集成 / Must integrate with:

### 我知道的相邻方案 (Adjacent / prior art I already know about)
What exists today that sort of solves this? What did I see someone try and fail?
Leave blank if you don't know — Stage 1 of the debate will search for these.
- Product A — <how it relates>
- Attempt B — <what I remember about it>

### 已知未知 (Open Questions)
Minimum 3. These seed the debate. Honest here beats polished.
-
-
-

### 期望产出 (Desired outcome)
"A <thing> that <user> can use to <value>." One sentence.

### 我的倾向 (My lean — optional, debate can overturn)
If you already have a hypothesis about direction or stack, say so. The debaters
will challenge it. Skip if you genuinely don't know.
```

---

## Ambition legend

| Level | Meaning | Typical wall-clock |
|-------|---------|-------|
| S | Script or one-off utility | 0.5–3 days |
| M | Single-purpose tool or small CLI | 1–3 weeks |
| L | Full SaaS product with backend | 4–10 weeks |
| XL | Platform-scale (IM, protocol, full iOS/Android app) | 8–20+ weeks |

Be honest. Ambition inflates naturally; leave room to under-promise and over-deliver.

--- -->

<!-- Start writing your proposals below this line. -->
---

## **001**: Research Radar

**提出日期 / Proposed**: 2026-04-22
**状态 / Status**: parked on 2026-04-22, reason: pre-conditions are not clear enough
**初始野心等级 / Ambition**: M
**成熟度 / Idea maturity**: direction-clear

### 动机 (Why)
近年来AI research工作呈井喷式增长，新的工作层出不穷。
单靠个人来读文章/Blog/Repo已经远远跟不上了。
我希望做一个research radar，会自动发现、跟进最新的AI领域研究工作

### 目标用户 (Who)
我个人使用。
我现在负责一个AI实验室，带领很多学生和研究员探索新的AI技术、以及搭建SOTA的AI应用。

### 核心想法 (What)
我需要一个“research radar”，它能够：
1. 自动检测arxiv的文章、顶会（如nips, icml, iclr等）的文章、顶尖学术机构/巨头实验室/创业公司（deepmind, thinkingmachines, anthropic等）的blog，github 高潜力的repo等
2. 检测到的新工作（文章/blog/repo）后，会进行下载、解析、解读、分析（novelty, impact, 实用性）等操作
3. 构建我的知识库：
   - 知识库会维护一个topic标签库，topic会按由大到小、由广到窄延伸多个层级；
   - 新的工作如果有价值，则将其归纳总结到知识库中；如果价值一般或者没有价值，留个痕（以防遗漏关键）
   - 知识库支持多种形式的检索和查看，比如，可以考虑按一个时间线梳理，也可以不同工作的同源、延伸、对立、渊源、继承关系等等；又如，该知识库可以针对最新工作实时更新当前topic的SOTA水平/状态
   - 有主动搜索补充的能力，比如用户给一个新工作，之前如果没有相应的topic，会新建一个topic，并且主动搜索把相关的重要工作补齐
4. 重点工作会给我推送 
5. 上述的分析、解读、处理的能力可以依赖大模型

### 初始约束 (Constraints)
- 预算 / Budget: 我有一台4090的linux系统机器，可以部署一些小尺寸的本地LLM、OCR模型，也可以做一些搜索的事情。我有code plan，可以以廉价的成本接入GLM5.1，minimax2.7这些模型。开发层面，我可以用claude code（opus4.7，sonnet4.6），codex（gpt5.4）进行开发。
- 时间 / Timeline: 我希望在我一个人的情况，结合claude code和codex，以及cursor辅助，在一周内完成该产品的开发。

### 期望产出 (Desired outcome)
"一个我自己让我持续跟进前沿研究的、可长期使用的软件"



---

## **002**: Research Radar

**提出日期 / Proposed**: 2026-04-22
**状态 / Status**: draft
**初始野心等级 / Ambition**: M
**成熟度 / Idea maturity**: direction-clear

### 动机 (Why)
近年来AI research工作呈井喷式增长，新的工作层出不穷。
单靠个人来读文章/Blog/Repo已经远远跟不上了。
我希望做一个research radar，会自动发现、跟进最新的AI领域研究工作

### 目标用户 (Who)
我个人使用。
我现在负责一个AI实验室，带领很多学生和研究员探索新的AI技术、以及搭建SOTA的AI应用。

### 核心想法 (What)
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

### 初始约束 (Constraints)
- 预算 / Budget: 硬件：一台24G vram 的4090的linux系统机器，可以部署一些小尺寸的本地LLM、OCR模型，也可以做一些搜索的事情。模型token资源：可以以廉价的成本接入GLM5.1，minimax2.7这些模型。开发工具层面：可以用claude code（opus4.7，sonnet4.6），codex（gpt5.4）进行开发。工作模式及效率等价于相当于一个资深架构师带6~7名初级工程师。
- 时间 / Timeline: 以一名资深架构师+6~7名初级工程师的研发资源，可以给到半年到1年的开发时间。

### 期望产出 (Desired outcome)
"一个让AI research scientist持续跟进前沿研究的、可长期使用的软件"


---

## **003**: 每天赚100美元

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
