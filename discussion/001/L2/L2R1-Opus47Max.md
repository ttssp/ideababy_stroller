# Idea 001 · L2R1 · Opus 4.7 Max · Explore (no search)

**Timestamp**: 2026-04-23T09:41:12Z
**Searches used**: NONE in this round.
**Visibility**: I did NOT read GPT's L2R1. Verified `discussion/001/L2/` contained only PROTOCOL.md before writing.
**Origin**: **Root-id direct L2（menu-aware）**。L1 Inspire 完成并产出 13 条 direction 的 menu（`stage-L1-inspire.md`），但 moderator 选择**保留 menu 作为灵感库、直接 L2 explore 原 proposal**。因此本文不加 §0 "alternative framings"——13 条替代读法已经在 menu 里独立存在，不需要折进 L2 再重复一次。L2 的对象是 **proposal 001 里 moderator 自己写的那段具体 Research Radar 构想**（自动发现 → 解析解读 → 知识库 → 时间线/同源/继承/对立检索 → SOTA 实时更新 → 品味 agent 自学 → 为 lab 的 research agent 做前置）。

---

## 1. The idea, unpacked

**用户是谁** —— 不是笼统的"AI 研究者"。具体是一个**运营着一支 8-15 个 topic 的小型研究 lab 的 PI**（5-15 人规模，国内 AGI/foundation-model 方向，既做应用也做小而精的研究），他自己的品味还在主动生长（而不是已经定型），**主动希望保持前瞻判断力**，明确知道单靠人力已经跟不上 AI research 的产出速率。副生用户：这个 lab 的核心研究员（博士生 + 资深研究员），他们共享 PI 的 topic 地图但各自在其中的某几个点上做深度工作。

**有这个东西之前，PI 的一天大致长这样**：早上翻 arXiv 日报扫到 80-200 篇，能真正读下来的 3-5 篇；Twitter/X 上的 lab blog 推送是第二流；组里博士生每周 reading club 会补充第三流。一周下来，PI 能跟上的覆盖面大约是他"希望"覆盖的 25%-40%。更痛的是——他知道自己漏掉的不是长尾，而是**明天某个学生来找他讨论时他会被问住**的那几篇。**真正的疲惫不是"读不够多"，是"不知道自己漏掉了什么"**。SOTA 的判断经常来自 post-hoc 的碎片线索，而不是结构化掌握。

**有了之后，他的一天大致长这样**：每天早上 8-15 个 topic 的结构化 digest 已就位，但**不是按论文堆叠**，而是按"过去 24-72 小时在这个 topic 发生了什么 shift" 组织——SOTA 被撼动了吗？某个 claim 被复现失败了吗？新的 method 合流进了哪条主线？每条 shift 下面挂着 3-5 篇触发它的工作。PI 快速看一眼判断今天要下沉的是哪 1-2 个 shift；剩下的知识库替他兜底——每一篇新论文都已经被归纳进 topic 的 taxonomy，他不必担心"漏"，只需要决定今天要"深入"哪里。学生下午来问"这个方法有没有人做过类似的"，PI 直接在系统里查——topic 图显示 3 条相关路径、12 篇相关工作、2 个对立的 claim。原本需要 30 分钟的回忆变成 90 秒的点击。

**第 30 秒的 "aha"**：不是看到一份精美的 daily digest——**那是常见的 newsletter 体感**。aha 时刻是他第一次输入一个当下正在思考的问题（比如 "RLHF 对长文 reasoning 的副作用到底定性了吗"），系统给出的不是搜索结果的堆叠，而是**一张 topic 子图**：当前主流立场有 A/B 两派、A 派的 3 篇代表作有 2 篇最近被 X 挑战、B 派的 SOTA 上周被新工作推前、有 1 篇冷门的 workshop paper 被系统标注"结构上和 B 派一致但没人引用它"。30 秒内 PI 得到的不是更多信息，是**经过 topology 整理的 position**——这是他自己手动做要 2 小时的事。

**6 个月后的 long-term mastery**：PI 会意识到自己的一部分"品味"已经外化在系统里了。他对某篇新论文的第一反应从"我要不要读它"变成"系统怎么标的、我同意吗"。系统标 high-novelty 的他会专门读它即便不属于热门 topic；系统标 "incremental on X" 的他会跳过。他开始**主动训练系统**——每次他对某个标注不同意，他会写一句 why，系统的品味就逼近他的一步。系统不替代他的品味，它是一个**让品味可被审视、可被辩论、可被继承**的对象。6 个月后他换了两个学生加入 lab，新学生上来就能从系统的 topic 地图里快速建立 lab 的 shared context——这在过去需要半年口头传承的事。

**如果 100 万人在用这个**：世界会不一样。AI research 的**生命周期**被系统化地记录——哪些 idea 在被推进、哪些被证伪、哪些在合流——并且是 **lab 级别**而不是学术传媒级别的记录。每个 lab 有自己的 shared brain；当一个 lab 的 shared brain 成熟到某个程度，它开始能**主动提出研究问题**（"根据我们 lab 过去 12 个月的工作和 field 当前的 gap，下一个有价值的 question 可能是 X"）——这时原 proposal 里埋的"最终目标：研究智能体"那条线就走通了。

## 2. What's genuinely novel

**不完全是新——但具体的切片是新的**。自动论文发现、LLM 归纳、知识库构建这些 building block 已经很成熟（Elicit、Undermind、ResearchRabbit、alphaXiv 等等都在做）。真正"没见过的"是三个层的结合：

**第一层 novelty**：**从"feed 范式"到"topic topology 范式"**的产品形态切换。现有工具 95% 都是"流"（每日推送、推荐、alerts）；它们的 primary view 是时间线。这个 idea 的 primary view 是 topology——节点是工作、边是 derives-from/contradicts/generalizes/supersedes，时间是这张图的一个维度而不是组织原则。流是"被时间冲刷"，图是"可以驻足"。

**第二层 novelty**：**"lab 级 shared brain"而非"个人工具的多人授权"**。现有工具几乎 100% 是个人定位；即使支持 sharing，也是 shared shelves（shared libraries、shared tags）。这个 idea 里 lab 的集体理解是第一公民：topic 地图记录的是 **lab 的 position**（我们倾向于这个 claim、我们对这个 claim 抱持怀疑），不是 user 的。

**第三层 novelty**：**"品味是可训练、可外化的 agent 伙伴"**。不是 LLM 套个壳做 personalization（那是现在所有产品都在做的事），是显式把"taste model"当作系统的一个独立对象——它会被 PI 主动挑战、被修正、被继承给新学生。它是 lab 的 intellectual asset，不是 session 级的 preference 信号。

**诚实的说**：任何一层单拿出来都不是完全原创——"知识图谱"、"team tool"、"品味 model"都有先例。**三层合起来作为一个统一产品，目前确实没有人在做**（L1R2 的搜索证据支持这点）。所以 novelty 在 **integration + slice + unit-of-product**，不在 building block。

## 3. Utility — what can users actually DO with this?

**场景 A · 周一早上的"topic weather report"**
PI 周一 8:00 打开系统。不是一份 daily digest（他已经见过太多 newsletter），而是 8-15 个 topic 各自的"weather report"：**RL-from-preferences** 本周 frontier 稳定，无 shift；**Long-context reasoning** 有一个 SOTA shift，触发来自某 lab 周五 release 的 preprint，系统标记"与去年 Gemini 的某个 trick 是同一条路线的改进版"；**Agentic code generation** 本周有 3 篇 negative result 被并列看到，系统提示"主流的 self-refine 叙事可能需要收紧"。PI 花 12 分钟读完 weather report，决定本周 deep dive 放在 "Long-context reasoning" 的那个 shift 上。他告诉同事 Alice：**"系统这周帮我发现了一篇不然我一定会漏的文章，它就是你上周卡住的那条路上的关键补丁。"**

**场景 B · 学生问问题时的 topology 查询**
博士生 Bob 下午敲门："老师，我在想把 contrastive method 引入 preference learning，有没有类似的工作？"PI 以前要么凭记忆回答（常常漏）、要么让 Bob 自己 google（慢且浅）。现在他打开系统、输入这个问题——20 秒后一张 topic 图跳出来：3 条相关路径（contrastive RLHF、SimCSE-style preference、DPO variant with negative sampling），每条路径上 3-5 篇代表作 + 1-2 篇 lab 成员已经读过的标记（Alice 去年读过 SimCSE-style 那条）。PI 在图上圈出 2 篇给 Bob，同时告诉 Alice 这条值得你重看。Bob 回去后对同学说：**"老师的知识库是真 work 的，不是装样子的。"**

**场景 C · lab 入职的 shared context 启动**
新学生 Carol 9 月入学，分配到 Agentic code generation 方向。以前 Carol 第一周要做的是读一份 PI 发的 "must-read" 列表（20 篇左右，静态），然后自己摸索该怎么把它们串起来。现在 Carol 打开系统的 Agentic code generation topic 图——4 条子路径、每条路径 lab 的当前立场、每条上标了"lab 已掌握"vs"lab 仍在观望"。她花了一周读完"lab 已掌握"那条最核心的子路径，第二周开始自己往 topic 图贡献标注。Carol 半年后跟前同学说：**"这个 lab 最值钱的不是 GPU，是他们集体知识的那张图。"**

## 4. Natural extensions

**v0.2** — 加入 **active hypothesis probing**：从系统当前的 topic topology 出发，让 LLM agent 主动生成"lab 应该去验证的 3 个猜想"（基于 gap 或 contradiction）。不是 open-ended research ideation，是 topology-informed 的聚焦 probing。

**v0.5** — 扩展到 **post-experiment integration loop**：lab 自己的实验结果（不只是外部论文）也进入 topic 图，topology 开始记录"lab 的独家发现 vs 外部主流",自动对比。

**两年后，相邻产品** —— 可以想见三个：
- **lab 之间的联邦共享**（Fed-Lab brain）：多个小 lab 的 topic 图在某个 topic 上有可合并的部分，合并后形成半公开的"frontier 共识图"。这是 2028 年的 academia infra 雏形。
- **教学产品**（Lab Brain for onboarding）：把 lab 图做成学生入门 topic 的 guided tour。
- **Research agent**（原 proposal 里的最终目标）：topic 图 + taste agent + experiment loop = 一个能 autonomously propose & test hypothesis 的 lab-level 研究 agent。

**相邻用户段** —— 拓展到**产业研究部门**（企业内部的 AI research group，受同样的 abundance 痛苦）、**投资 AI 的 VC**（用类似系统追 market 而不是 paper）。

## 5. Natural limits

**这不该是什么**：
- **不该是通用论文推荐系统**。它的价值密度来自"8-15 个聚焦 topic + lab 级 shared brain"。扩展到"所有研究者的通用 discovery"会稀释掉它的结构化判断——它会变回 Elicit。
- **不该是 consumer-grade 的"论文社交网络"**。PubPeer / Paperstars 那条线不适合这个 shape——公开评分/社交会让 lab 的 shared brain 变成表演场所，私密与信任是它的基础。
- **不该强吃 long tail topic**。如果 lab 从 8-15 topic 扩到 50 个 topic，系统的 topology 深度会变浅，从"深入"退化成"扫描"。8-15 是护城河。
- **不该替代 reading**。系统的终点是让 PI **知道要读什么、省 60% 的 triage 时间**，不是"不读"。如果 PI 开始完全信任系统的摘要不再回去读原文，品味会退化。
- **不该追求跨语言 / 跨文化广度**。对话 AI 领域 90% 的前沿工作在英语 arXiv；过早扩到中文小众期刊或专利全文会稀释 signal。
- **不该是一次性的静态产品**。它的价值在 **复利**——用得越久、lab 的 topic 图越厚、taste model 越贴近——没有几个月的持续使用，它看起来会平淡。

## 6. Three honest questions about this idea

这些是如果有清晰答案会显著改变我看这个 idea 的角度：

1. **"lab 级 shared brain"是否真的比"5 个个人工具的松散集合"更有价值 —— 有没有历史证据？** 具体说：过去 10 年有哪些"小团队 knowledge infra"产品真正 work 了（例：Notion 对 team wiki、Figma 对 design collaboration），哪些失败了（Mendeley public groups 三分之二塌回单人就是个反例）？winning case 的共同特征是什么？

2. **"taste 可外化"是否过度乐观 —— PI 会真的愿意把自己的判断标准 articulate 出来并训练系统吗？** 还是说这对 PI 的"元认知负担"其实太高，实际中 taste 只能通过 implicit signal（点击、阅读时长、保存）被推断，而这些 signal 在 research 场景太稀疏？

3. **topic topology 这一产品形态有没有 real user traction 的先例 —— 还是说它是一个"看起来美 / 用起来没人坚持"的 visualization trap？** 具体说：Connected Papers / Litmaps / ResearchRabbit 的 graph view 的留存数据如何？"图范式"在信息工具里是真需求还是审美幻觉？

---

**Word count**: ~1700 中英混合词等价值（对应英文 950-1050 词范围，符合 700-1300 字节）。§1 和 §3 密度最高（约 60% 字数），§2/§4/§5 中等，§6 精简。严格未触及 tech/architecture/cost/feasibility——novelty 在产品形态和 unit-of-product 层，不在实现层。
