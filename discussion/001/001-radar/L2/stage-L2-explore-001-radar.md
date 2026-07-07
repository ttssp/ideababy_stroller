# L2 Explore Report · 001-radar · "Paper Radar：给 AI lab 负责人的研究方向位移雷达"

**Generated**: 2026-07-06T14:00:00Z
**Source**: forked from 001 · L1 Direction 7「Topic Cartographer（做地图不做流）」（起步以 moderator note 澄清的 KG-radar 愿景为准，Direction 7 原文为骨架）
**Source rounds**: L2R1（Opus + GPT，双方）、L2R2（Opus + GPT，双方）
**Searches run**: 16 次（每侧 8 次），横跨约 15 个不同来源（竞品官网、arXiv 学术工作、行业报道、dashboard 失败研究、生态动向）
**Moderator injections honored**: 1（binding · KG-radar 澄清愿景优先于 Direction 7 字面文本）

## How to read this

这是 L2 层对 001-radar 的深度剖析。不同于 L1 菜单（很多浅可能性并列），这是对**一个**想法的**一份**丰富理解。读完你应该知道：

- 这个想法具体是什么（不只是概念，是有质地的细节）
- 为什么值得考虑（或诚实地说，哪里该重新掂量）
- 它可能长成什么、以及**不该**试图变成什么
- 进 L3 scope 之前你必须回答（或需要找真实用户回答）的问题

本层严守铁律：**不谈技术/可行性/成本做决策**。当年 001-pA 的 LLM 成本教训（p95 46s / 月 $1838）只作风险背景，不在此层下结论。

## Executive summary

- **净判定：Y-with-conditions。** 双方 explorer 独立得出同一结论。需求是真的且在恶化，生态位在产品侧尚无人占据，但护城河**不在**"知识图谱"四个字本身——那层已被学术近邻逼近，消费级图工具也各占一角。
- **真正的独占组合是三者叠加**：(a) 方法级+claim 级的图语义 × (b) **位移**作为主 payload（不是新增、不是静态邻域图）× (c) 有品味、可持续校准的 agent 策展。单拿任何一样都能找到近亲；叠在一起、且服务于 lab-lead 决策语境的产品形态，目前没人做。
- **生存法则由 dashboard 失败研究给出**：位移视图必须**绑定一个反复发生的决策仪式**（组会选精读 / 季度方向复盘 / talk 备稿），而不是做一张"随时可看"的全景地图——"随时可看"在行为上约等于"从不看"。72% 的 BI dashboard 被弃用回电子表格，主因就是"与决策隔离建设"。
- **时机窗口开着但在变窄**：Papers with Code 2025-07 关停刚把方法级基础设施腾空；ResearchRabbit 2025-11 被 Litmaps 收购、后者已有时间轴+momentum（"半步位移"）；同时学界 2026 年 5-6 月连出 Eliot、MIRAI、Scientific Contribution Graph 等逼近同片区域的工作。产品侧无人占位，学界正在逼近。
- **最大的悬而未决不是"该不该做"，而是"位移的 payload 长什么样"**：可视地图 / 强观点 briefing / 前后快照 diff / 可带进组会的问题清单——这四选一可能决定整个产品骨架，且两位 explorer 都指认它是 L3 首要待决问题。默认的"以图为主容器"这个假设**值得被审**。

## 1. The idea, fully unpacked

用户不是"研究者"这个泛称，是一类很具体的人：**AI lab 的负责人**——PI、研究组 leader、创业公司的 research lead，或任何对 8~15 个 topic 负有"这个方向还值不值得下注"判断责任的 senior researcher。这个人自己动手写代码的时间趋近于零，但每周的决策全都依赖对领域现状的判断：批不批一个新课题、砍不砍一个旧方向、给哪个学生的 proposal 泼冷水、下季度算力往哪儿压。他的困境**不是**"读不完论文"——那是 PhD 的困境——而是**他脑中每个领域的 big picture 在悄悄过期**。他上一次真正吃透 RLHF 是八个月前，之后的理解靠走廊对话、X 上的碎片和组会上学生的转述拼起来。他自己知道这一点，所以每次做方向判断时心里都有一丝不确定：我脑中这张地图，还是现在的地形吗？

这里有一个比"信息过载"更精准的病灶定义（来自 GPT 侧、被 Opus 侧采纳）：真正的敌人不是论文的**数量**，而是新增的**同质化**——在 feed 里，一篇"已有路线的漂亮补丁"和一篇"把两个原本分离的方法族接起来"的工作长得一模一样，而日常工具最容易把前者（爆款热度）放大、把后者（结构性贡献）淹没。用户真正想要的恰恰是第二种判断。radar 的核心任务，就是把第二种从第一种里拎出来——这直接定义了"品味层"的工作对象。

有了它之后，用户的动作变成：**想查的时候打开那个 topic 的地图**。地图不是引用关系的可视化，而是一张**方法级**（乃至 claim 级）的知识图谱——节点既有 paper、也有更耐久的"方法/技术"单位，甚至有"claim / 问题意识"这类第三层节点；边不止"谁引用谁"，还有 derives-from / contradicts / generalizes / supersedes。这里有个语义上的精确点（GPT 侧补上、Opus 侧确认）：`contradicts` 这类边真正挂靠的对象是 **claim**，不是 paper——所以图的语义骨架应当是 paper / method / claim 三层，而非双层。而且地图是**活的**：一个 agent 在持续收集最新 SOTA、判断价值、把有价值的织进图、给价值一般的留痕防漏。

但用户看到的第一屏**不是图本身，是位移**。过去 90 天，这个领域哪些假设在退潮、哪些方向被合并、哪个新节点正在往中心挤。位移比新增更有信息量：新增是流的逻辑（今天又有 40 篇），位移是地图的逻辑（重心挪了、某条边断了）。30 秒的 aha 时刻因此很尖锐：lab lead 看到的不是"新增 23 篇论文"，而是"preference optimization 的前沿从离线 pairwise 叙事，明显向在线反馈、过程信号、可验证任务的混合区域移动；DPO 仍是中心节点，但不再是解释所有新工作的唯一坐标"。他本来**隐约感觉**到了这件事（X 上这类工作似乎变多了），但从没有人把它**画出来**给他确认。那种"我模糊的直觉被具象成一张可以指着讲的图"的瞬间，是这个产品的第一价值时刻。

L2R2 的搜索之后，这里出现了一个必须诚实点出的张力：**那句"frontier 漂移"的叙事，本质是一句 briefing，不是一张地图**。如果最有价值的 payload 是那句话，图可能只是生成那句话的中间产物——那么产品重心就该落在**叙事**而非可视化。两份 R1 同时押了"地图为主"和"一句话最尖锐"两注，却没指出两者之间的张力。这个形态问题（payload 到底是地图 / briefing / 前后快照 diff / 问题清单）因此从一个次要选项升级成了 L3 的首要待决问题，也是本报告不替 operator 拍板的地方。

六个月后的熟练用户不再把它当查询工具，而当**判断的外骨骼 / 研究判断的第二记忆**：季度方向复盘时逐张地图过位移；学生开题前先让他在地图上指出 idea 落在哪个区域；请报告嘉宾前先看对方工作在图上的邻域。更重要的是 agent 的品味在与他对齐——哪些位移值得推到眼前、哪些只是噪声，这个判断在长期交互中被校准。但这里两份 R1 都跳过了一个关键环节（Opus 侧点出）：用户凭什么从"看看"走到"依赖"？中间必经的是若干次"地图说的和我后来验证的一致"。**这个信任积累机制两份 R1 都缺席，L3 必须补**——因为 contradicts / supersedes 这类边本质是判断而非事实，一次显眼的错边就可能烧掉全部信任。

原提案里还藏着一个必须成为一等公民的动作：**冷启动一张新 topic 地图**。原提案明确要求"给一个新工作，若无对应 topic 则新建并主动搜索补齐"。而 lab 负责人真实工作里"评估一个**还没进我 8~15 个 topic** 的新方向"（正是 GPT 侧场景三）恰是高价值时刻。所以"覆盖足够窄位移才有意义"这道保护栅栏必须留一扇门——冷启动新地图不是例外，是核心动作之一。最后，如果一百万人用它，"这个领域现在怎么样"会从口口相传的软知识变成一个可打开、可指认、可争论的公共物件——survey 从半年一篇的静态快照变成活的地层图。但这是远景，不是承诺；而且 GPT 侧提醒：更可信的**初始**价值其实是 lab-local 的私有地图（不同 lab 对"重要"的定义不同，过早的公共地图反而稀释品味）。

## 2. Novelty assessment

**判定：Novel execution（概念组合常见，主容器有新意；护城河在"怎么做"，不在"做什么"）。**

双方独立给出同一诚实结论：**零件都不新，组合方式新**。citation graph 可视化已有成熟产品（Connected Papers / Litmaps / ResearchRabbit）；新论文 alert 是十年老功能；paper graph、reading list、survey、trend dashboard、SOTA tracker、研究简报都有相邻形态。真正可能新的，是把**"研究方向的结构位移"作为主 payload**，而不是把它当图视图的附属解释。与普通 citation graph 的差异在于：citation graph 回答"文献之间如何相连"，KG-radar 要回答"方法与问题的重心如何移动"；与 newsletter 的差异在于后者回答"今天读什么"，前者回答"为什么这篇东西改变了地图"；与 leaderboard 的差异在于后者把进展压成指标排序，前者关心一条路线是否正在替换另一条。

但 L2R2 搜索对"novelty 在哪"做了一次重要的收窄，其中最关键的是一处**部分推翻**：moderator note 和两份 R1 都隐含假设"claim 级 / contradicts-supersedes 这类边没人规模化做过"——**这条不成立**。scite.ai 早已围绕 supporting / disputing(contrasting) / mentioning 对约 **15 亿条 citation statement** 建立了 smart-citation 视角。同时 2026 年的 Scientific Contribution Graph（arXiv 2605.15011）已做 contribution 级节点 + prerequisite 边，OpenScholar / Elicit / Undermind 已把 search、report、alert、gap-finding 做到产品层。结论是清晰的：**"方法级 / claim 级节点"和"contradicts 这种边"本身都不能再当强 novelty**——它们已有学术乃至产品近邻。真正能守住的差异，只能落在三件事的**交集**上：位移（时间维度的 diff）作为主呈现 × 方法/claim 粒度的图语义 × lab-lead 决策语境下的 agent 品味校准。任何单独一条都会被现有玩家拆掉——图被 Litmaps/ResearchRabbit 拆，报告被 Elicit/Undermind 拆，claim 语义被 scite 拆。novelty 是执行驱动的、且窗口在收窄，但只要那个"位移感"真做出来，它就不再是又一张漂亮 paper map，而是研究判断的仪表盘。

## 3. Utility — 具体使用场景

**场景一 · invited talk 前夜（双方共识的最强场景）。** 一位做 RLHF / alignment 的 PI 下月要给跨领域听众讲"过去半年 preference learning 发生了什么"。他不想列 30 篇 paper，也不想临时拼 survey。他打开 KG-radar，看 topic 地图的半年位移：frontier 从离线 DPO 变体向 online / on-policy 漂移，且三篇工作在 contradicts 一个 2025 年的共识假设。这页位移图直接成为演讲里"field 往哪儿走"的关键 slide。第二天他对同行说的是："我不是补读完了所有论文，而是终于知道这半年该怎么讲——那张图不是我画的，是我的 radar 长出来的。"

**场景二 · 周一组会定精读。** 一个 12 人的 AI lab 每周只能集体深读 2~3 篇工作。以前学生各自推荐，最后常被热度、熟人转发、标题吸引。KG-radar 帮 lab lead 看见某个新方法**虽然热度不高，但连接了两个原本分离的子簇**，并让组里现有路线暴露出一个新竞争面。组会因此不再问"这篇是不是热门"，而问"它改变了我们对这个 topic 的哪条边"。问题从信息筛选升级成路线判断。这个场景同时把"不替代精读"这条 limit 翻成了正面产品语义：地图不是阅读的替代品，是**精读的选择器**——读什么、带什么问题读、读完放回哪张图。

**场景三 · 季度方向复盘。** 季度会前，负责人把 12 张地图的 90 天位移各看十分钟。发现自己 lab 押注的某方向，其中心假设在这个季度被三篇独立工作 contradicts——地图上那个节点的入边红了一圈。他带着这张图进会议室，砍方向的讨论从"我感觉这条路不太行"变成"证据在这儿，大家看"。方向决策从记忆和直觉的辩论，变成对一张共享地图的核对。

**场景四 · 决定是否开一个新方向（冷启动动作）。** 一位创业公司 research lead 在考虑把一小队人投入"agent evaluation"，担心这只是短期噪声。这是一个**还没进他 topic 列表**的方向——KG-radar 现场冷启动一张新地图，展示过去几个月的变化：若相关 work 只是分散爆发、没形成稳定问题簇，这是谨慎信号；若 evaluation 方法、benchmark criticism、failure taxonomy、可复现 case study 开始互相连接，说明 topic 正从热词变成可研究对象。他完成的不是选题自动化，而是把"感觉上很热"变成"结构上是否成形"的判断。

**场景五 · 学生开题接地。** 学生兴冲冲提了个 idea。负责人打开对应 topic 的地图，两人一起找这个 idea 的落点——发现它坐在一个四个月前被 supersedes 边覆盖的区域，隔壁却有一条几乎没有节点的 frontier 边。原本要一周的"我回去想想"，变成十分钟的有据反馈加一个更好的方向。学生获得的不是否定，是**一张能看见自己位置的地图**。

## 4. Natural extensions（长阴影）

- **Topic memory（最自然的 v0.2）**：每个 topic 不只显示当前地图，还保留关键历史快照，让用户回看"我们三个月前为什么认为 A 路线更强、现在为什么改判"。服务于 lab 的长期学习，而非单次阅读。用户一旦依赖位移，必然会问"上一版地图长什么样"，这是被使用行为直接拉出来的需求。
- **Lab-shared / lab-local taste layer**：地图从负责人的私人判断外骨骼长成 lab 的共享认知底座（回应 L1 菜单里的 lab-scale 主题）；同时把同一张公共研究地图，折射成"对我们 lab 为什么重要"的私有视角。不同团队对"重要"的定义不同（理论清晰 / 可复现 / benchmark movement / 能否启发产品），taste layer 是把公共图私有化的关键。
- **区域订阅 / map-region alert**：radar 从被动查询长出主动提醒，但以**地图区域**而非关键词为订阅单位——"这个节点周边有任何位移就叫我"。这是 feed 类工具给不了的，也是把用户拉回来的候选机制（注意这与"不做每日简报"的边界存在张力，见 §5 与 §7）。
- **跨 topic 方法迁移检测**：某方法从 NLP 图漂进 RL 图，往往是好题目的前兆——radar 主动标记这种跨图迁移。
- **Research-agent 底座（终局野心）**：把持续演化的图作为 research agent 的底座——brainstorm 时 agent 在图上找空洞、找矛盾、找可迁移的边。原提案写明的终局在这里露出第一级台阶：对现有工作的深理解是想出好题目的前置条件，这张图就是那个"深理解"的物质形态。

每一级都以前一级的图质量为地基，不需要跳跃。它们不是另起炉灶的新产品，而是同一张研究地图在不同研究仪式里的出口。

## 5. Natural limits（保护栅栏）

- **不是每日简报。** 那是 001-pA 的形态（砍窄给忙人看流）。地图的价值恰在"想查时打开"的 pull 语义，混进 push 会把它拖回 feed 的重力井。（⚠️ 但这道边界不绝对——见 §7 里 GPT 对 map-region alert 的反驳：区域级位移提醒不等于退回每日新闻流。这是 L3 要裁的一刀。）
- **不适合领域新人从零学起。** 位移的前提是你脑中有旧地图可被 diff。新人需要 survey / 教科书。这个相邻用户段看着近，其实是另一个物种。主用户是"已经有方向判断责任、但被增长速度压垮的人"。
- **不该追求全覆盖。** 把 arxiv 全量塞进图是 feed 思维的残留。价值在 8~15 个 topic 上的选择性中心度；贪全会同时毁掉品味和信任、退化成浅层趋势榜。
- **不是真理机。** contradicts / supersedes 这类边本质是判断而非事实，地图必须把不确定性穿在外面。若它承诺"自动理解一切并给出正确方向"，反而失去可信度。
- **不该做问答/报告生成器。** 那片已被 Elicit / Undermind / OpenScholar 高强度占据。KG-radar 应专注 temporal structure + lab-local judgment，避免正面撞进 synthesis-agent 无人区。
- **预设 arxiv 速度的领域。** 半年位移接近零的慢领域里，这个产品的核心呈现没东西可画。
- **不能把图当目的。** 复杂图很容易显得高级，但用户要的是可行动的 big picture：该补读什么、该警惕什么、哪条路线在上升、哪个问题已变形。地图若导不出判断，只是认知装饰。

## 6. Validation status

L2R2 双方各跑 8 次搜索，证据高度一致。

### 现有工具地形（Prior art）
| 名称 | 状态 | 它做什么 | 对我们的教训 | URL |
|---|---|---|---|---|
| Litmaps | 活跃，2025-11 收购了 ResearchRabbit，转 freemium | citation/reference-based 搜索 + 可视化 + 监控新文章；已有时间轴 + momentum 指标 | **半步位移竞品**——差异化必须踩在方法级 + diff 叙事上，不能只靠"图 + 监控" | [effortlessacademic 对比](https://effortlessacademic.com/litmaps-vs-researchrabbit-vs-connected-papers-the-best-literature-review-tool-in-2025/) · [Litmaps features](https://www.litmaps.com/features) |
| ResearchRabbit | 被 Litmaps 收购 | 可视 map 看 papers/authors/concepts 互联、ideas evolve over time | 单位仍是 paper；"随时间演化"是营销词而非位移 payload | [RR features](https://www.researchrabbit.ai/features) |
| scite.ai | 活跃 | 对约 15 亿条 citation statement 分 supporting/disputing/contrasting | **部分推翻我们的假设**：claim 级边已规模化；我们的差异只能落在位移+方法粒度+决策语境 | [scite 相关论文](https://arxiv.org/abs/2104.08087) · [biorxiv PDF](https://www.biorxiv.org/content/10.1101/2021.03.15.435418.full.pdf) |
| Elicit | 活跃，自称 5M+ researchers | reports + alerts + Research Agent + sentence-level citations | 报告/问答面已被占；避免做 synthesis 器 | [elicit.com](https://elicit.com/) |
| Undermind / OpenScholar | 活跃 / 学术 | novelty、gaps、emerging trends、cross-disciplinary（OpenScholar 覆盖 45M open-access，citation-backed）| synthesis-agent 竞争压力高；专注 temporal structure 才能避开 | [undermind.ai](https://undermind.ai/) · [OpenScholar arXiv](https://arxiv.org/abs/2411.14199) |
| Papers with Code | **2025-07 被 Meta 关停** | 众包方法分类 + leaderboard | **时机变量**：方法级基础设施的空洞 12 个月内刚被腾空，社区在呼吁替代品 | [关停报道](https://hyper.ai/en/news/42900) · [社区呼替代](https://www.researchgate.net/post/Can_someone_replace_papers_with_code) |
| ORKG | 活跃 | 结构化方法级对比 | 人工策展**不可扩展**——证明 agent 自动策展是必经之路 | [orkg.org](https://orkg.org/) |
| Scientific Contribution Graph（学术，2026）| 论文 | contribution 节点 + prerequisite 边；指出 paper-level citation 与 sentence-triple 间的表征鸿沟 | 方法/贡献级图已有学术近邻，不能当独占 novelty | [arXiv 2605.15011](https://arxiv.org/abs/2605.15011) |
| Zeta Alpha | **已转向企业 RAG/搜索**（客户 Festo/BASF/Deloitte）| 曾做研究趋势/neural search | 产品侧生态位空出来了 | [zeta-alpha.com](https://www.zeta-alpha.com/) |
| Eliot / MIRAI（学术，2026-05/06）| 论文 | 交互式文献趋势探索 / 高影响力研究预测 | **窗口在变窄**：学界正逼近同一片区域 | [Eliot 2605.27610](https://arxiv.org/pdf/2605.27610) · [MIRAI 2606.05443](https://arxiv.org/pdf/2606.05443) |

### 需求信号（Demand signals）
| 来源 | 信号 | 强度 | URL |
|---|---|---|---|
| Berkeley/Haas | LLM 采纳者产出 bioRxiv +50% / arXiv +1/3；"区分有价值工作"成系统性危机 | **H** | [Haas newsroom](https://newsroom.haas.berkeley.edu/how-ai-is-transforming-research-more-papers-less-quality-and-a-strained-review-system/) |
| Guardian 2025 | indexed papers 2015→2024 从 1.71M 涨到 2.53M；researchers/peer review 被淹 | **H** | [Guardian](https://www.theguardian.com/science/2025/jul/13/quality-of-scientific-papers-questioned-as-academics-overwhelmed-by-the-millions-published) |
| NeurIPS 2025 position paper | 把 AI-generated surveys 称为对社区的 DDoS，主张 dynamic live surveys | **H**（几乎是本产品的正面背书）| [arXiv 2510.09686](https://arxiv.org/abs/2510.09686) |
| Elicit 用户规模 | 自称 5M+ researchers | **M**（证明痛点有大市场，但市场已拥挤）| [elicit.com](https://elicit.com/) |

### 失败案例（Failure cases）
| 名称 | 状态 | 为什么会死 | 我们的规避 | URL |
|---|---|---|---|---|
| BI dashboard 通病 | 长期 | 72% 用户弃 dashboard 回电子表格；主因=与决策隔离建设 + 认知过载 | **绑定一个反复发生的决策仪式**——这是生存法则，不是可选项 | [Medium: stop building dashboards](https://medium.com/@bhumikaavula90/stop-building-dashboards-nobody-uses-why-most-analytics-deliverables-fail-and-how-to-design-for-b5d751a36ad3) |
| Dashboard literacy 错配 | 学术 | 用户 literacy 与 dashboard 所需 literacy 不匹配，需求还会移动 | payload 必须导出判断，不能要求用户"学会读图" | [arXiv 2209.06363](https://arxiv.org/abs/2209.06363) |
| Mixed-initiative viz 失败评估 | 学术 | interface 设计 + 对用户预期的错误建模 | 形态问题（§7 Q2）必须靠真用户验证，不能靠想象定 | [arXiv 2009.06019](https://arxiv.org/abs/2009.06019) |
| Papers with Code | 已关停 | 众包策展 + 平台被大厂放弃 | agent 自动策展替代众包；不依赖单一平台施舍 | [hyper.ai](https://hyper.ai/en/news/42900) |

### 净判定
**Should this exist? Y-with-conditions**

需求证据强且在恶化（论文洪水 + "筛出结构性工作"正是本产品的刀刃），产品侧生态位当前无人占据，且 Papers with Code 之死刚腾出方法级基础设施的空洞。两位 explorer 独立得出 Y-with-conditions。但护城河脆弱——图、边、报告、claim 语义分别已被 Litmaps / scite / Elicit / Undermind / 学术近邻占了一角，且学界正在逼近。因此**必须带条件**：

- **条件一（payload）**：核心交付物必须是**绑定 lab 决策仪式的、持续的时间维度位移**，而不是一张通用的 paper 图。位移感做不出来，它就退化成又一个漂亮 paper map，被现有工具正面碾过。
- **条件二（novelty 落点）**：不要把"方法级 KG"当护城河——2026 已有近邻。差异必须落在"持续位移叙事 × 方法/claim 粒度 × lab-lead 决策语境 × agent 品味校准"的**交集**上。
- **条件三（用户 + 仪式绑定）**：目标用户必须是有方向判断责任的 lab lead / research lead（不是泛 researcher），且每张图都要导向一个具体 decision ritual（该读什么 / 该停什么 / 该补什么 / 哪个假设变弱 / 哪个 frontier 变强）。没有 ritual，dashboard 失败研究预言它会被弃用。

## 7. Open questions for L3 / for user research

⚠️ **本 fork 的最大风险是形态问题（Q2）在想象里定不下来。** 两位 explorer 都指认它需要真实用户（或 operator 自用）验证。L3 若在没有用户输入的情况下硬拍 payload 形态，极可能产生返工。**建议 L3 前或 L3R0 intake 中，operator 以自身即目标用户的身份先回答 Q1–Q3。**

| # | 问题 | 最适合谁回答 | 为什么重要 |
|---|---|---|---|
| 1 | **v0.1 锚定哪个决策仪式**：组会精读选择 / 季度方向复盘 / talk 备稿 / 开新方向评估？三者频次与痛感不同 | operator（本人即目标用户）| 决定生存法则里那个"反复发生的仪式"是谁；错锚 = dashboard 命运 |
| 2 | **位移 payload 的形态**：可视地图 / 强观点 briefing / 前后快照 diff / 可带进组会的问题清单？| 真用户试用 + operator 自用 | **可能决定整个产品骨架**；R1 的"以图为主"默认值必须被审 |
| 3 | **信任预算与建立机制**：边错到什么程度用户弃用？第一个月需要几次"地图说对了"才建立依赖？| 真用户 / operator 自用 | contradicts/supersedes 是判断非事实，一次显眼错边可烧掉全部信任；R1 都跳过了这段 |
| 4 | **首发 topic 数**：8~15 是终态还是起点？v0.1 也许 3 个 topic 就够验证位移价值 | operator | 影响 v0.1 的可验证性与工作量边界 |
| 5 | **单人版 vs lab 共享版起步**：先做私有判断外骨骼，还是先做 lab 共享底座？| operator | L4 之前必须定，影响所有 scope 与 taste-layer 设计 |
| 6 | **冷启动新 topic 地图是否列为一等公民动作**：Opus 指出"评估还没进列表的新方向"是高价值时刻（场景四）| operator | 决定"覆盖窄"这道栅栏要不要留门；影响核心动作清单 |
| 7 | **是否需要 map-region alert 把用户拉回**：GPT 反驳"硬性不做 feed"的边界——区域级位移提醒 ≠ 每日新闻流 | 真用户（留存行为）| pull-only 的地图会不会因"想不起来打开"而低留存？这是 §5 边界要裁的一刀 |

**建议的真实用户访谈三问**（若能采访 5 位 lab lead）：
1. 回忆最近一次砍掉或新开一个研究方向——当时你实际看了什么证据？若当时有一张"该方向 90 天位移图"，它会改变过程还是只是装饰？
2. 你现在感觉哪个 topic 上自己的理解最过期？为补上它，你上次花了多少时间、用了什么工具、停在哪一步？
3. （给他看一张 mock 位移图）你愿意把这张图原样放进你下周组会的 slide 吗？不愿意的话，缺什么才敢放？

## 8. Decision menu（for the human）

### [S] Scope this idea — proceed to L3
```
/scope-start 001-radar
```
推荐：净判定为 Y-with-conditions，需求与时机证据都变强。若 operator 愿意先以"自身即目标用户"的身份回答 §7 的 Q1–Q3（尤其形态问题），L3 会更稳、返工更少。L3 会拉入你的真实约束与偏好。

### [F] Fork another L2 angle from this same idea
```
/fork 001-radar from-L2 <new-angle> as <new-id>
```
若读完这份报告激发了更锐的切法——例如"直接把 payload 定为 briefing 而非地图"或"只做单一仪式（组会精读选择器）的极窄版"——可从本 L2 再分叉一个角度。

### [B] Back to L1 menu
```
/status 001
```
回看 001 的 L1 菜单与其他 fork（含 valid sibling 001-pA），也许某条方向在本报告映衬下更合适。

### [R] Re-explore with new input
```
/explore-inject 001-radar "<your input>"
/explore-next 001-radar
```
若觉得某处缺失（例如想补一轮专门审"payload 形态"的对撞），注入 moderator note 再跑一轮 L2。

### [P] Park
```
/park 001-radar
```
保留全部 artifact。若你想先和几位潜在用户（其他 lab lead）聊过形态问题再 scope，Park 是好选择——本报告的形态风险恰恰指向"先要用户输入"。

### [A] Abandon
```
/abandon 001-radar
```
本方向不推荐 Abandon（判定为 Y-with-conditions，非 N）。若确要放弃，sibling fork（001-pA）独立继续。

---

## Fork log
（由 /fork 命令在本 L2 有子分叉时更新）
