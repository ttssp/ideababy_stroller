# L1 Inspire Menu · Idea 001 · "Research Radar"

**Mode**: full
**Generated**: 2026-04-23T17:30:00+08:00
**Total directions surfaced**: 13
**Both-endorsed**: 5
**Source rounds**: L1R1 (both), L1R2 (both)

## How to read this menu

这是 L1 层的产出：由你原始提案激发的一组方向。每一条都是**一种可能性**，不是推荐。你会 fork 你觉得有意思的那几条：

  /fork 001 from-L1 direction-<n> as <suggested-id>

你也可以把整份菜单 park 起来，以后再回来看。即便你从来没有 build 其中任何一个方向，这份菜单本身仍然有长期价值——半年后再读，也许某个方向的时机到了。

## Your original proposal (baseline)

> 你希望做一个 Research Radar：自动发现并跟进 AI 领域最新的 research 工作（arXiv 论文、顶会、顶级实验室 blog、GitHub repo），下载解析、评估 novelty/impact/实用性，沉淀为一个多层级 topic 知识库，支持时间线 / 同源 / 继承 / 对立等维度的检索，能主动补全相关工作、实时更新 SOTA 状态。实验室覆盖广，希望长期聚焦 8–15 个 topic。研究品味希望交由 agent 去自主学习（吸收 X 上的观点 + 在长期交互中调优）。最终野心是结合 Karpathy autoresearch、Anthropic 9-Opus 讨论这类研究智能体思路，构建一个 lab 的 research agent——这个 radar 是第一步。

---

## Inspired directions

### Direction 1 · "Dissent Cartographer / Counter-Radar"
**Suggested fork id**: 001a
**Sources**: Opus L1R1 A3 + Opus L1R2 R2-Top-1 · GPT L1R1 A3 + GPT L1R2 §4 Top-1（both endorsed，两轮都 Top 3）
**Description**:
不做"放大 mainstream 信号"的 radar，而做它的反面——专门捕捉 anti-mainstream 信号：负结果、reproducibility 问题、appendix 里被轻描淡写的 disclaimer、对火热 claim 的有效质疑、被埋没但结构正确的工作。用户打开这个 radar 不是去"跟上大家在看什么"，而是看"大家没在看 / 没在讨论，但可能正在崩塌或正在萌芽的东西"。在一个 lab 里，它扮演的是"免疫系统"的角色。

**Spark**（为什么这个方向有意思）：
所有现存 radar（Semantic Scholar、Papers with Code、alphaXiv、ResearchRabbit）的 incentive 都是放大已经在被讨论的信号——越火越被推。Counter-Radar 在方向上完全相反，它是一种**结构性的 contrarian**。这种"反向 alpha"在投资里早已是一整个流派，在科研里几乎完全空白。它让 lab 不容易被 herd，不容易把"流行"误读为"坚实"——这种品质比"早一周知道新论文"有更长的 shelf life。

**Cognitive jump from proposal**:
原提案把"高潜力"与"顶会 / 巨头 blog / 被讨论度"几乎等同。这是一个典型的 mainstream bias——真正重要的工作中有相当比例在被发现前是冷门的，而且 high-confidence claim 里往往隐藏着 appendix 级别的 caveat。让人主动设计一个**专门反自己直觉**的系统，需要一次显式的 reframe——人在自己的信息回音室里很难自己迈出这一步。

**Value validation evidence** (from L1R2):
- Prior art：PubPeer 做的是**人工**、post-publication scrutiny 的社区（[PubPeer](https://pubpeer.org/static/about)）；Retraction Watch 是新闻+人工编辑（[Retraction Watch 2025/11 LLM-ID retracted papers study](https://retractionwatch.com/2025/11/19/ai-unreliable-identifying-retracted-research-papers-study/)）；Papers with Code 的 reproducibility tag 是被动的；post-publication peer review 作为学科有正面证据（[PMC PPPR review](https://pmc.ncbi.nlm.nih.gov/articles/PMC4472664/)）。
- Demand signal：Publication bias against null/negative results 在学术圈和 ML 社区都是活跃抱怨（[AskAcademia 负结果线程](https://www.reddit.com/r/AskAcademia/comments/z467d7/how_common_is_it_for_people_not_to_publish_academ/)、[r/MachineLearning 负结果讨论](https://www.reddit.com/r/MachineLearning/comments/1aikp5f/publishing_negative_results/)）。
- Failure cases：PPPR 文献警告，匿名 + gotcha dynamics 会让文化滑向"无差别负能量"而非"平衡判断"，这是这个产品最大的 cultural risk。
- Net verdict：**5 个主方向里唯一没有直接 structured 竞品的空间**。双方 R2 都独立把它放在 Top 1 / Top 3——结构性空白 + 真实 demand + 有明确的 cultural failure mode 可以提前设计对冲。强烈候选。

---

### Direction 2 · "Lab-Scale Shared Intelligence"（融合 Lab Radar + Boundary Object Maker）
**Suggested fork id**: 001b
**Sources**: Opus L1R1 A2 + Opus L1R2 R2-Top-2 · GPT L1R1 A1 (Lab Memory Theater) + GPT L1R1 C3 (Boundary Object Maker) + GPT L1R2 §4 Top-3（both endorsed）
**Description**:
产品的 unit 不是"个人"，是"lab"。系统记得每个成员的 reading list、project 进展、当前卡点；它既做 personalized routing（"Alice 应该看这篇 / Bob 应该看那篇 / 因为……"），又主动制造**跨 topic 的共享概念 handle**——当 lab 同时跑 8–15 个 topic 时，帮不同方向的人用共同的 metaphor / axis / comparison frame 来讨论。周一 lab meeting 前，每人收到自己的 digest，同时看到一张共享视图："这周你们集体该关心 X，因为 Alice 和 Carol 的 project 都在撞它"。半年后 lab 的讨论会出现显著的 cross-pollination——它是从个人工具升级成 **lab infra**。

**Spark**：
个人版 radar 的天花板是"我一个人读得快一点"，封顶是线性的。lab 版的天花板是"我们 lab 的**集体认知带宽**被放大 3×"，而且是 compounding——人越多、运行越久，数据越厚，routing 越准，lab 的集体记忆越深。这不是多人版个人工具，这是一个新物种：它把"研究消化"从信息问题重新定义成**社会认知设计问题**。

**Cognitive jump from proposal**:
原提案隐含"这是给我个人用的"——虽然提到"实验室覆盖 8–15 个 topic"，信号其实指向团队版，但很容易被"先做个人版再说"的本能带偏。**从 individual tool 到 lab infra 是一个 product shape 的跃迁**，不是功能延伸；同时"让跨 topic 的人听懂彼此"是一个比"分发论文"更深的目标——这一层人很难自己跳出来。

**Value validation evidence** (from L1R2):
- Prior art：主流 literature review 工具（Paperguide, Elicit, ResearchRabbit, Scite, Consensus, SciSpace）几乎 100% 是 individual-user 定位（[Cypris 2026 Top 11 榜单](https://www.cypris.ai/insights/11-best-ai-tools-for-scientific-literature-review-in-2026)）。ResearchRabbit 有 shared collections（[RR shared collections docs](https://learn.researchrabbit.ai/en/articles/13192798-how-to-share-papers-and-collections)），Mendeley 做过 collaborative public groups（[Mendeley collaborative groups 2010](https://blog.mendeley.com/2010/10/11/mendeley-is-now-more-social-featuring-collaborative-groups-in-app-tutorial-updated-citation-styles/)）——但都停在"共享书架"层。
- Demand signal：阅读列表的痛点本质是社会性的，研究者同时要管 project papers / future-useful papers / 跟其他 lab 的工作（[AskAcademia reading-list 管理](https://www.reddit.com/r/AskAcademia/comments/1pdpxe2/how_to_manage_your_reading_list_of_research_papers/)）。HN 的研究文献痛点线程里，大量用户在手动构建"团队知识图谱"（[HN 研究文献 pain points](https://news.ycombinator.com/item?id=41041678)）。
- Failure cases：Mendeley 自己的分析发现接近三分之二的 public group 只剩一个 member（[Mendeley public groups 研究](https://blog.mendeley.com/2015/04/27/an-exploratory-study-of-paper-sharing-in-mendeleys-public-groups/)）——**被动共享会退化回个人收藏**。winning 的版本必须有主动 routing + rituals，不只是 shared shelves。
- Net verdict：结构性空白（产品定位层）+ 真实 demand + 有明确的 "passive sharing 会塌" 教训。**双方 R2 都独立把它放进 Top 3**。候选力度强，但产品设计上必须主动制造节奏/仪式。

---

### Direction 3 · "Question→Dissent Belief Router"（Question-First Scout × Dissent Cartographer × Taste Twin）
**Suggested fork id**: 001c
**Sources**: GPT L1R1 C2 (Question-First Scout) + GPT L1R2 §5 (Belief Router) · Opus L1R2 §5 N1 (Question→Dissent Loop) · partial overlap with Opus Taste Twin（跨 R2 新萌生、双方都识别出的融合方向）
**Description**:
信息流转 180 度。系统不从"新论文流入"开始，而从 **lab 的 live questions / 当前 belief / 活跃 doubt** 开始。外部新工作要**挣到**进入 lab 视野的资格——只有当它 sharpens / weakens / redirects 一个 lab 正在追的问题，才被 surface；而且它不是按 topic tag 分发，而是按"它会撼动哪条 belief、该撼动通知到谁"来 route。系统同时维护一本 **belief ledger**（我们 lab 当前相信什么、怀疑什么、搁置什么）。新论文像子弹打向这本账本，账本的变化本身就是 lab 的 thinking timeline。

**Spark**：
这一条把 Question-First Scout（起点反转）、Dissent Cartographer（优先撞裂缝）、Taste Twin（陪练品味）三种 spark 融成一个产品骨架。它从"世界发生了什么"翻转成"**我们在尝试理解什么、外部工作如何作用于这些理解**"——让同样的 paper 流忽然变得**主动**而不是被动；让 lab 的 agenda 拥有物理存在感。它比 public scorecard（如 Research Stock Market）更安静、更私密；比 knowledge base 更活；它是研究版的 **personal OS for conviction**。

**Cognitive jump from proposal**:
原提案从"世界的 firehose"起手——这本身制造了一个 **intake-first bias**。人在"被信息淹没"的体感里，思路自然滑向"更快 / 更全 / 更结构化地摄入"。Question-First 要求先承认：**relevance 不是论文的属性，是外部工作和 lab 内部 curiosity 的关系**。要让人自己做到这个翻转很难——它需要一个 lateral jump。

**Value validation evidence** (from L1R2):
- Prior art：Elicit 的工作流是"先细化研究问题 → 在问题周围做 semantic search + screening"（[Elicit systematic review](https://elicit.com/solutions/systematic-review)）——与"问题起手"的核心已经对齐。Undermind 明确做"ask follow-up questions → understand exactly what you need → keeps tabs on your areas of interest"，非常接近**个人版** Question-First（[Undermind](https://www.undermind.ai/)）。
- Demand signal：研究者明确抱怨"当你还不知道这个领域的 magic words 时，keyword search 会完全失灵"（[AskAcademia 找论文线程](https://www.reddit.com/r/AskAcademia/comments/1b5os86/how_do_you_find_not_just_access_research_papers/)）——这就是 keyword-first 范式的结构性痛点。
- Failure cases：2025 BMC 对 Elicit 的评估显示 question-first 很有用但**结果不稳定**（同一 query 多次跑结果不一致，而且仍会漏掉人工综述里相当比例的论文）——这说明 question-first 不能是唯一入口，应该是 radar 的**组织透镜**而非**唯一进气管**（[BMC Elicit evaluation 2025](https://bmcmedresmethodol.biomedcentral.com/articles/10.1186/s12874-025-02528-y)）。
- Net verdict：个人版 Question-First 已经有人做得不错；**lab 级（team live-questions 作为中心 agenda）+ belief ledger + 与 dissent 优先原则融合** 是空白且可占的差异化。两个 R2 都从不同起点合流到这个方向，信号强。

---

### Direction 4 · "Taste Twin / 研究品味分身"
**Suggested fork id**: 001d
**Sources**: Opus L1R1 A1 + Opus L1R1 Part D #1 + Opus L1R2 R2-Top-3 · GPT L1R1 A2 (Taste Apprenticeship) · GPT L1R1 C1 (Conviction Coach) · GPT L1R2 §1（both endorsed）
**Description**:
不是"抓取 + 归纳"的 pipeline，是一个**长期学习你品味的"学术分身"**。你要对一篇论文下结论之前（impactful / forgettable / overhyped），Twin 先独立给出它的判断，然后交叉 / 辩论 / 修正；它记得你去年夸过谁、踩过哪些坑，并会主动抛出"这和你去年夸过的 X 是同一路数，但作者没引用，metric 还避开了 X 的弱点——你可能会被说服，但我觉得是话术"。三年后你意识到，你的决断力不是因为读得多，是因为**被挑战得多**。在 junior 研究者身上它更像"品味的学徒场"（Taste Apprenticeship）；在资深研究者身上它更像"陪你练十年的 sparring partner"。

**Spark**：
把"radar"从**信息工具**重新定义成**品味训练系统**——目标函数从"吞吐量"换成"判断力"。信息已经 commodity，judgement 才是稀缺。这是一个可以陪你十年、越来越懂你的对象——任何 RSS / 订阅 / search 工具都无法提供。它把"读论文"的时间压缩，但把"和 Twin 辩论某篇论文"的时间放大——后者才是真正让品味生长的时间。

**Cognitive jump from proposal**:
原提案把痛点定位在"跟不上信息"。但**真正限制 PI 水平上限的不是信息摄入，是判断力的形成**。身处"被淹没"的体感里很难看到这一层。此外"radar 是陪练不是送餐"的 product shape 与原提案的 pipeline 想象完全不同——需要显式跳出"输入→处理→输出"的心智模型。

**Value validation evidence** (from L1R2):
- Prior art：ResearchRabbit 的 "following your curiosity" 接近但不完整——仍然是 discovery 工具（[ResearchRabbit](https://www.researchrabbit.ai)）。Paperstars 在尝试基于 quality 的社区评分（[Paperstars](https://paperstars.org/)）。R Discovery 做 personalized recommendation；但 Cypris 2026 榜单的 11 个主流产品没有一个**明确定位"陪你练品味 / 长期 sparring"**（[Cypris 2026 榜单](https://www.cypris.ai/insights/11-best-ai-tools-for-scientific-literature-review-in-2026)）——所有人都在优化 consumption 端。
- Demand signal：研究者明确在要求基于"real human signal"而非 citation / hype 的 discovery（[r/learnmachinelearning 如何挑 AI 论文](https://www.reddit.com/r/learnmachinelearning/comments/1ruzjq5/how_do_you_actually_decide_which_ai_papers_are/)）；"personalization as deep as colleague"被反复提到。
- Failure cases：Paperstars 面临的问题是"review 密度稀薄"——**sustain trusted participation 比发明 format 更难**。这提示起点应该是小而受信任的社区层，而不是通用公共 marketplace。
- Net verdict：定位真空 + 真实 demand + 明确的冷启动 / 信任失败模式。R2 两边都保留或独立识别了它。高度候选，但产品形态应从小圈子起手。

---

### Direction 5 · "Key Mind Tracking（听懂少数关键的人）"
**Suggested fork id**: 001e
**Sources**: Opus L1R1 C3（single-surfaced, Opus only）
**Description**:
放弃"覆盖越广越好"的假设。历史上前瞻判断往往来自对 10–30 个 key mind 的深度追踪——选 15 个你认定的"信号源"（特定学者、匿名博客主、某些小圈子的内部讨论、某几支 lab 的 group meeting slides），把他们在所有渠道的输出（paper + blog + talk + tweet + slides）聚合成一条"他们怎么想"的流。在此之上用 LLM 做**二阶洞察**——不是"X 发了新论文"，而是"X 的 focus 过去 3 个月从 A 漂到 B；他最近一次 talk 的措辞不再为 A 辩护"。

**Spark**：
前瞻性可能不是广度函数，是**深度函数**。把雷达的对象从"整个 field"换成"一组 key mind 的思想漂移"是一个从量向质的重新定位。当你能实时看到"Ilya 的关注在往哪儿倾"的时候，你看到的是**生成信号的源头**，不是被信号冲刷的下游。

**Cognitive jump from proposal**:
原提案里 "coverage ≈ quality" 的假设非常隐性。要让人自己问"我是不是应该只盯 20 个人而不是 20 万篇论文"需要一次反直觉的切换。

**Value validation evidence** (from L1R2):
- Prior art：Semantic Scholar 支持 per-author alerts（[Semantic Scholar FAQ 管理订阅](https://www.semanticscholar.org/faq/manage-alerts)），alphaXiv 做 explore（[alphaXiv](https://www.alphaxiv.org/)），Benty Fields 等早期产品做过（[Benty Fields 综合](https://saasnik.com/ai-tools-for-researchers-in-2026/)）；但全部停在 **1.0 的 new-paper notification**，没做二阶洞察。
- Demand signal：这类产品存在 5+ 年，仍然存在用户——demand 被验证，但止步于 1.0。
- Failure cases：10 年没出现二阶洞察产品——要么做起来难（tacit + 数据稀疏），要么 PMF 不够硬——需要警惕。
- Net verdict：1.0 需求已饱和；**2.0（focus shift detection）是空白但风险偏高**。适合作为 Top 3 之外的有力候选。

---

### Direction 6 · "Reading Companion（阅读时刻的增强）"
**Suggested fork id**: 001f
**Sources**: Opus L1R1 A4（Opus only）
**Description**:
不做 push/pipeline，只做 **pull-时刻的增强**。你在浏览器或 PDF 里打开一篇论文，companion 实时呈现：这篇引用了哪些前置工作？你已经读过哪些？lab 里谁熟？同行怎么评价？作者过往轨迹里哪篇与这篇关联最紧？它不打扰你的 reading list，但在你已经决定读的那一刻，把一篇 45 分钟的论文读成 15 分钟 + 更深的理解。"aha"时刻：你读到第 3 节卡住，companion 说"这里的 trick 其实是 2023 年 Chen et al. 的 reweighting，只是术语换了——你当时读过，叫它 soft-gating"。你瞬间解锁。

**Spark**：
所有 radar 工具都假设入口是"新论文推给用户"。Reading Companion 做反向——**接受"你已经决定读这篇"这一事实**，然后优化的是那一刻的认知带宽。它是"pull 时刻的智能浸入"，不与推荐系统争门户，门槛低、每次 value 清晰可感。

**Cognitive jump from proposal**:
原提案把 value 压在"决定读什么"环节。Reading Companion 把 value 转到"决定读之后"的环节——这个环节 largely invisible，但每次都真实发生。跳出 pipeline 范式才能看见它。

**Value validation evidence**：L1R2 未专门搜索该方向；但 Reading Companion 的最大近邻（Scite、Connected Papers 的 in-reader surface、各类 AI 插件）已经非常拥挤。建议 fork 之前单独补一轮 validation。

---

### Direction 7 · "Topic Cartographer（做地图不做流）"
**Suggested fork id**: 001g
**Sources**: Opus L1R1 A5（Opus only）
**Description**:
放弃"信息流"范式，做**持续更新的研究地图**。每个 topic 是一张图，节点是工作，边是 derives-from / contradicts / generalizes / supersedes。你不是被每天/每周通知，你是在想查某个 topic 时打开地图，看这个领域最近六个月发生了什么位移——哪些方向被证伪、哪些被合并、哪些新节点挤到中心。准备 invited talk 前一晚，你打开 RL-from-preferences 的图，看到 frontier 从 DPO 往 online 方向漂了 40 度——这成为你演讲的一张关键 slide。

**Spark**：
流是**时间**的 organizing principle，地图是**结构**的 organizing principle。对研究来说"位移"比"新增"更有信息量——哪些假设在退潮、哪些合并、哪些被证伪。把产品容器从 feed 换成 cartography 是一次元素级换向。

**Cognitive jump from proposal**:
原提案里 "timeline / 同源 / 继承 / 对立" 全都存在，但它们在字面上仍被想象为知识库的**索引维度**而不是产品的**主形态**。把结构从次要维度升级成主容器需要一次反转。

**Value validation evidence**：近邻有 Connected Papers、Litmaps、ResearchRabbit 的图视图等——L1R2 未专门做 validation。如要 fork，应该先辨析清楚"比现有 citation graph 多给了什么"。

---

### Direction 8 · "Field Simulator（field weather）"
**Suggested fork id**: 001h
**Sources**: GPT L1R1 B1（GPT only；Opus L1R2 pushed back）
**Description**:
最有野心的版本：系统维护一张"field 未来形状"的活地图——每一篇新工作都轻微 tilt 这幅地图。哪些下注在增强、哪些假设在衰退、哪些问题变得新可问。使用者说的不是"我读了文献"，而是"我能感受 frontier 的天气"。

**Spark**：
把 radar 的对象从"发生了什么"升级成"field 认为自己在往哪里去"。"future-shape of a field"是一个 frontier-level 的认知容器，想象力很大。

**Cognitive jump from proposal**:
原提案假设 radar 的对象是 works；这里要求对象是"field 的未来形状"——一次非常深的范畴跃迁。

**Value validation evidence**：Opus L1R2 做出警告——"sense the weather" 是**气氛**不是 **decision**，很容易退化成漂亮但无人基于它做决策的 dashboard（对照：Meta AI research trends dashboard、VC map-of-AI 系列产品都踩过这个坑）。若 fork，必须先回答"基于这张图，用户今天 / 这周应该做 X" 的具体场景。Net verdict：高野心，但 L1R2 给出了明确 caution。

---

### Direction 9 · "The 15-Minute Morning / One Good Page"
**Suggested fork id**: 001i
**Sources**: Opus L1R1 B2（15-Minute Morning）· GPT L1R1 B2（One Good Page）—— 同一方向两个切口，最小可行形态
**Description**:
只做一件事：每天早上 7:00 一份 **15 分钟内读完**的 digest，覆盖你关注的 8–15 个 topic；每个 topic 一行摘要 + 当天至多一篇"如果今天只读一篇就读它"。三个月后 digest 开始自动出现"上周你没读这篇，但它现在可能改变 topic X，强烈建议回补"。极度克制，追求的是"每天 15 分钟、坚持十年"的复利。GPT 的切口 One Good Page 是它的邻居——每 topic 每周一张"brutally curated"的 ritual object：什么重要、什么不重要、什么值得再花一小时。

**Spark**：
在所有高野心方向之间，这条押的是**克制本身**——compression is the moat。一张每天都被真的打开的 page，胜过一个被 star 但没被用的 dashboard。它是成为仪式的那类产品。

**Cognitive jump from proposal**:
原提案的野心会自然把产品撑大。要求自己**主动舍弃 feature** 是反本能的决定。

**Value validation evidence**：Opus L1R2 的 pushback：这种形态成功靠"品味"而非"系统"，更像 newsletter 产品。建议把它定位成 MVP / ritual object 形态，而非目标形态。

---

### Direction 10 · "Clinical Research Radar（临床医学 transplant）"
**Suggested fork id**: 001j
**Sources**: Opus L1R1 B3（Opus only）
**Description**:
把同一套 radar 机制搬到**临床医学研究**——文献更多、时间更紧（新疗法可能救命）、医生更没时间读。一个"临床研究雷达"为某专科医生监控新 trial 结果、meta-analysis、FDA 动向，并告诉他"你上周给 patient 用的方案，基于周二一篇新 RCT，可能需要调整"。同一套 pipeline，换掉领域、换掉受众，价值数量级可能更大。

**Spark**：
transplant 的对象选择决定了这条方向的活力。医学领域的 stakes 把"跟进延迟"直接换算成患者后果；"你上周开的方案现在有新证据"是一个**极强的 trigger word**——在 AI research 里最多是"我漏看了一篇论文"。

**Cognitive jump from proposal**:
假设 AI research = 唯一目标受众的默认假设要被质疑——机制是 domain-agnostic 的，某些 domain 的 value 密度可能远高于 AI research。

**Value validation evidence**：Opus L1R2 自己对比 Studio Radar 后认为 Clinical transplant 比 Studio transplant 更 ground（AI research 对 LLM 的 signal digest 友好，临床研究有强结构化先例，创意领域 tacit knowledge 太多）。建议 fork 之前补一轮临床 specific 的 prior art 与 demand 搜索。

---

### Direction 11 · "Studio Radar（创意 transplant）"
**Suggested fork id**: 001k
**Sources**: GPT L1R1 B3（GPT only；Opus L1R2 pushed back）
**Description**:
把同样机制搬到创意领域——游戏工作室、时装屋、电影 collective 使用同一模式，在成千上万的 weak signal 里追踪 emerging motifs 和 visual moves。价值不是原始发现，而是一张**活的 taste map**，帮团队知道什么是 derivative、什么正在成熟、什么已经拥挤。

**Spark**：
揭示了一个深层命题：原提案的核心机制不是"paper tracking"，而是"**abundance 下的 frontier sensemaking**"。这个机制天然可以流向任何有 abundance + taste judgment 的领域。

**Cognitive jump from proposal**:
让人自己识别"我真正在做的是 frontier sensemaking 这个抽象机制"需要一次 abstraction jump。

**Value validation evidence**：Opus L1R2 明确 pushback——创意研究的 signal 更主观 / 更难被 LLM 可靠 digest，aesthetic frontier 评估需要大量 tacit knowledge，落点选得不够 ground。建议优先考虑 Clinical（Direction 10）等结构化更强的 domain。

---

### Direction 12 · "放弃的许可（Permission-to-Drop）"
**Suggested fork id**: 001l
**Sources**: Opus L1R1 C1（Opus only）
**Description**:
研究者真正的痛可能不是"信息太多我读不完"，而是"我不敢说某些 topic 我不再追"。文献焦虑的本质是 FOMO。这个方向做的不是 radar，是**"许可你不读"的系统**——它告诉你"你可以放心不看 topic X 了，基于你过去 12 个月的工作重心和 topic X 近 6 个月的进展速率，放弃它的机会成本是 0.3%"。给你**放弃的勇气**。

**Spark**：
它是一个完全反转的 value proposition——同类产品都在证明"多摄入"，只有这一条在证明"少摄入是安全的"。这在情绪上稀缺，在现有市场里几乎没人占。

**Cognitive jump from proposal**:
原提案的 value prop 是"跟上"；这一条把 value prop 翻转成"允许不跟"。要求人自己意识到"FOMO 才是痛点而不是 information overload"需要对自己的焦虑做一次诚实的 reframe。

**Value validation evidence**：L1R2 未专门搜索该方向。如要 fork，建议先验证"FOMO 是否比 information overload 更靠近真实痛点"——可能需要做一些 user interview 层的假设检验。

---

### Direction 13 · "Research Stock Market（公开品味市场）"
**Suggested fork id**: 001m
**Sources**: Opus L1R1 B1（Opus only；GPT L1R2 pushed back）
**Description**:
每篇论文是一支"研究股票"，价格由 LLM 代理池基于 novelty、impact、reproducibility、method-soundness 实时竞价——不是预测引用数，而是预测"这个 idea 在 18 个月后还会站得住吗"。人类研究者像操盘手，可以建仓、做空；持仓被未来的真实进展验证，历史命中率成为研究者的 public taste score。一个在 Twitter 被嘲笑的冷门 take 三个月后被证实，发帖者的 taste score 冲进 top 10，他的下一个 take 被 10 万人认真看——**品味变成可计量、可积累的资产**。

**Spark**：
它把"品味"这个至今高度私人、高度主观的东西，变成**一个可计量、可公开 compound 的 asset**。这是一个制度设计层面的方向。

**Cognitive jump from proposal**:
原提案里 judgment 是私人的 / 不可见的。把它变成公开可交易的 asset 要求一次"把私人品质公共化"的制度跃迁。

**Value validation evidence**：GPT L1R2 的 pushback——把**公开计分**放到 center of gravity，可能挤掉更有价值的"**私人 conviction formation**"；公开打分机制有把社区文化推向表演的风险。Net verdict：想法鲜活，但 center of gravity 风险需要先解决（可能需要一个 private-by-default 的变体）。

---

## Cross-reference: who proposed what

| # | Direction | Opus | GPT | Round(s) | Both endorsed |
|---|---|---|---|---|---|
| 1 | Dissent Cartographer / Counter-Radar | Y | Y | R1 + R2 | yes（两轮 Top 3） |
| 2 | Lab-Scale Shared Intelligence | Y | Y | R1 + R2 | yes（两轮 Top 3） |
| 3 | Question→Dissent Belief Router | Y (R2 N1) | Y (R1 C2 + R2 §5) | R1 + R2 | yes（两边 R2 都推） |
| 4 | Taste Twin | Y | Y | R1 + R2 | yes（Opus R1/R2 Top，GPT R2 §1 明确点赞） |
| 5 | Key Mind Tracking | Y | — | R1 | no (Opus only) |
| 6 | Reading Companion | Y | — | R1 | no (Opus only) |
| 7 | Topic Cartographer | Y | — | R1 | no (Opus only) |
| 8 | Field Simulator | — | Y | R1 | no (GPT only; Opus R2 pushback) |
| 9 | 15-Minute Morning / One Good Page | Y | Y | R1 | yes（两边都提，但定位为 MVP） |
| 10 | Clinical Research Radar | Y | — | R1 | no (Opus only) |
| 11 | Studio Radar | — | Y | R1 | no (GPT only; Opus R2 pushback) |
| 12 | Permission-to-Drop | Y | — | R1 | no (Opus only) |
| 13 | Research Stock Market | Y | — | R1 | no (Opus only; GPT R2 pushback) |

**Both-endorsed count**: 5（Directions 1、2、3、4、9）——其中 1/2/3/4 是强收敛，9 被双方识别为 MVP 形态而非目标形态。

## Themes I notice across the menu

我注意到三个主题在菜单里反复浮现。第一，**"value 从信息摄入迁移到判断形成"**——Taste Twin、Conviction Coach、Belief Router、Dissent Cartographer、Permission-to-Drop 都在往这个方向滑动，暗示整份菜单隐含的共识是：原提案真正锚定的痛点是 judgement 而非 throughput。第二，**"个人 vs lab 的 unit 选择是产品骨架级的决策"**——从 Lab Radar、Boundary Object Maker、Lab Memory Theater、lab 级 Belief Router、Key Mind Tracking 的团队版本，到 Taste Twin 的 lab 版本，两边都多次把 unit 从个人切换到 lab，这个维度比"加多少 feature"更决定产品物种。第三，**方向按"反 mainstream 的程度"呈现一条连续谱**——从原提案的 mainstream radar，经过 Counter-Radar / Dissent Cartographer，一直到 Permission-to-Drop（不读的许可），反向程度越强的方向空白越大。

## What's notably missing from this menu

有几个维度两边都未充分探索，moderator 如果感兴趣可以考虑 re-inspire：

- **时间尺度的极端版本**。菜单里大部分方向是"现在 + 最近 6 个月"的时间尺度。没有人提出**"10 年文献考古"类的 radar**（把冷门的历史工作重新映射到当前 frontier，做 dead-idea revival），也没有人提出**"实时 live"的 radar**（比如盯住 ICLR rebuttal 期间 reviewer 的观点流动、学者 tweet 的即时反应）。
- **针对 research 的 human-in-the-loop 形态未被触碰**。两边都没提出 **"radar + 周会 / reading group / journal club 这类高频社会场景"的绑定产品**——Boundary Object Maker 是最接近的，但它仍是 infra 而非仪式。
- **对 non-AI research domain 的覆盖极度单薄**。只有 Clinical 和 Studio 两个 transplant，且 Studio 被否。Legal、Biology wet lab、materials science、policy research 等高 abundance + 高 stakes 的领域都未被探索。
- **"雷达对抗 AI 伪造内容 / AI 生成灌水论文"的视角缺席**。在 2026 年的现实里这是显性 risk，但整份菜单未将其作为 first-class problem，仅 Dissent Cartographer 擦过。
- **商业 / 开源 / 社区治理的组织形态未被讨论**（合规范围内——这仍然是 L1 可以触碰的 value 层面，比如"这个产品是 closed lab tool 还是 open federation"会显著改变它的 value shape）。

如果以上任何一条让 moderator 觉得"对，这是我真正在乎的方向"，建议用 `/inspire-inject 001 "..."` 注入 steering 后再跑一轮 L1R2。

## Decision menu (for the human)

### [F] Fork one or more directions
为每一个你想展开的方向运行：
```
/fork 001 from-L1 direction-<n> as <suggested-id>
```

可以并行 fork 多个方向，每一个成为独立的 L2 子树。

### [R] Re-inspire with steering
菜单没捕捉到你真正想要的？加一条 steering：
```
/inspire-inject 001 "<你的引导——下一轮 L1R2 应该重点在哪>"
```
然后重跑 /inspire-next 001。

### [S] Skip the menu, go to L2 with original proposal
```
/explore-start 001
```
菜单会保留——未来任何时候都可以从它 fork。

### [P] Park
```
/park 001
```
所有 artifact 保留，`/status 001` 随时复活。

### [A] Abandon
```
/abandon 001
```
关闭这个 idea，附一份 lesson 文档。

---

## Fork log
（初始为空；每次 /fork 命令执行后由它更新）
