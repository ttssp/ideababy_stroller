# L2 Explore Report · 001 · "Research Radar —— lab 的外置研究编辑部"

**Generated**: 2026-04-23T10:30:00+08:00
**Source**: 直接从 root proposal 001 进入 L2（`/explore-start 001` in root-id-direct mode；L1 的 13 条 inspired directions 被保留为灵感库，未折进本报告）
**Source rounds**: L2R1（Opus 4.7 Max + GPT-5.4 xhigh），L2R2（Opus 4.7 Max + GPT-5.4 xhigh）
**Searches run**: 12 次，跨 ≥ 10 个独立来源（Covidence / DistillerSR / Iris.ai Researcher Workspace / Readwise / Are.na / Mendeley 下线档案 / Notion-Figma 案例 / Zulip for research / ResearchRabbit 2025 revamp & Litmaps 收购 / Management Science 2024 delegation / emergency physicians keeping-up 综述 / r/MachineLearning 讨论 / r/PhD & r/Researcher workflow 讨论 / Huddersfield 2024 reference-management practices）
**Moderator injections honored**: 0（本 L2 未注入 moderator 注记，两轮自由推进）

## How to read this

这是 L2 对 001 Research Radar 的**深度展开**——不是 L1 那种"13 条浅层可能性"的菜单，而是对**一个** idea 的**一层**读法做到诚实极限。读完你应该知道：

- 这个 idea 具体是什么（不再抽象）
- 为什么它值得做 —— 以及哪些"novelty 叙事"在 R2 的搜索下被削弱、真正剩下的 novelty 是什么
- 它可以长成什么（natural extensions），以及它**不该**长成什么（natural limits —— 这些限制会在 L3 scope 时保护它）
- 在真正 scope 之前你必须回答 / 必须做 user interview 的 open questions 有哪些

L1 的菜单（`../L1/stage-L1-inspire.md`）记录了 13 条替代框架（Dissent Cartographer、Lab-Scale Shared Intelligence、Taste Twin、Permission-to-Drop 等），它们作为**灵感库**独立存在；本报告不再重述它们。如果读完本报告你觉得某条 menu direction 比原 proposal 更锋利，可以从那里 fork。

## Executive summary

- **Idea 的最锋利定位是"AI lab 的持续运转的外置研究编辑部"（lab-scoped research editor）** —— 不是 discovery tool，不是 knowledge base，而是把"发现 → 判断 → 归档 → 忽略留痕 → 回看 → 更新 SOTA 感知"折叠成**一条连续回路**的 editing & memory 系统。它的核心对象不是单篇 paper，而是**topic 的状态变化**。
- **Novelty 经 R2 搜索后被诚实降级为 "novel slice + novel execution"**，不是 novel concept。team-level literature workflow（Covidence、DistillerSR、Iris.ai Researcher Workspace）、shared library（Paperpile / Zotero / Mendeley）、taste personalization 的组件都已成熟；**真正未被占的切片是"open-ended frontier surveillance + 共享编辑判断 + 可剪枝的低价值留痕"** 这条组合。
- **用户锚点存在真实分歧 —— buyer 与 operator 需要拆分**：PI / lab lead 是**经济 buyer**，senior PhD / postdoc / staff researcher 才是**高频 operator**。这是一个 persona 分层问题，不是"PI 还是学生二选一"。
- **验证 verdict 为 Y-with-conditions** —— 有 winning pattern（Notion/Figma team wiki、Zulip 被 Stanford CS 选用）、有真实 demand（PGR reference-management 复杂度随资历上升），但有若干硬条件必须在 L3 明确（详见 §6）。
- **首页形态应为 digest-first，topology 降为 second-order explainer layer**。R2 搜索（emergency physicians 的 keeping-up 调查 + r/MachineLearning 的"全域不可能跟上"讨论）明确支持"时间是首要约束"的框架；graph view 不该作为唯一入口。

## 1. The idea, fully unpacked

**这不是一个"更勤奋的订阅器"**。原 proposal 读起来像是 "arXiv 爬虫 + LLM 解读 + 知识库"的 pipeline，但两轮深度展开后真正浮现出来的骨架是另一个东西：**一个为 AI lab 持续维护 8–15 个 topic 的"state dossier"的外置研究编辑部**。它处理的单位不是单篇 paper，而是 topic 的状态变化 —— "这周这个 topic 的 SOTA 被撼动了吗？某个 claim 被复现失败了吗？新方法合流进了哪条主线？"每条 shift 下挂 3–5 篇触发它的工作，但 shift 本身才是第一公民。

**核心用户不是"笼统的研究者"，也不是单一的 PI 或单一的博士生**。两轮合并后的清晰图景是 **buyer/operator 分层**：PI / lab lead 作为经济 buyer（愿意为"集体认知带宽被放大"付费、做 onboarding 决策），senior PhD / postdoc / staff researcher 作为高频 operator（每天在系统里做 triage、标注、修正）。他们共同服务于一支 5–15 人、覆盖 8–15 个 topic 的小型 AI 研究 lab —— 国内 AGI / foundation-model 方向、同时做应用与研究、品味还在主动生长。**两类用户的共同痛点不是"读不够多"，是"不知道自己漏了什么"**。覆盖广度从 arXiv 日报、顶会、顶级 lab blog、GitHub 高潜力 repo 到 X 上的碎片观点；真正的疲劳来自"明天学生来找你讨论某条路线时你会被问住"这种事后才暴露的 gap。

**有了这个系统之后的一天是怎样的**。周一早上 8 点，不是一份按论文堆叠的 daily digest（这种形态原本是 newsletter，不是 lab infra），而是 8–15 个 topic 各自的**digest-first briefing**："RL-from-preferences 本周 frontier 稳定，无 shift；Long-context reasoning 有一个 SOTA shift，触发来自某 lab 周五 release 的 preprint，系统标记与去年 Gemini 某 trick 是同路线改进版；Agentic code generation 本周有 3 篇 negative result 并列看到，系统提示 self-refine 叙事可能需要收紧。"operator 花 10–15 分钟读完 briefing，决定本周要下沉哪 1–2 个 shift；剩下的**系统替他兜底** —— 每一篇新论文都已进入 topic 的 taxonomy，他不必担心"漏"，只需决定"深入"哪里。下午博士生敲门问"contrastive method 引入 preference learning 有没有类似工作"，operator 打开系统，20 秒内看到 3 条相关路径、12 篇工作、2 个对立的 claim（其中 1 个是 lab 成员 Alice 去年读过的） —— 原本需要 30 分钟回忆的事变成 90 秒点击。

**第 30 秒的 aha 不是"信息更多"，而是"定向感"**。当 operator 第一次输入一个当下正在思考的问题（比如 "RLHF 对长文 reasoning 的副作用定性了吗"），系统的回应不是搜索结果堆叠，是**一张已经经过 editorial triage 的 position**：A/B 两派立场 + 代表作 + 最近撼动 A 派的 3 篇挑战 + 1 篇冷门 workshop paper"结构上与 B 派一致但没人引用"。这张 position 是他自己手动做要 2 小时的事；**产品的价值不在于"我知道了更多"，而在于"我知道该把注意力放在哪里"**。

**"低价值留痕"是明确的一等特性，不是 byproduct**。这是 GPT L2R1 升级的 novelty 点，值得在 §1 里单列：绝大部分推荐系统都在放大高信号、丢弃低信号；这个 idea 明确要**存储低信号**，但带 discard / quality filter / promote controls（参考 Readwise Daily Review + Are.na 的"可剪枝 breadcrumb" pattern）。当某篇当下被判定"incremental"的工作，在 3 个月后因为某条主线变化而重新变重要，系统能通过留痕把它 resurface 回来 —— 避免"当时看过但后来完全想不起"这种结构性遗忘。注意：这绝不是"无差别囤积"，而是"可逆、可剪枝、可重用的记忆管理"。

**6 个月后的 long-term compounding**。PI 会意识到自己的部分"品味"已经**外化在系统里** —— 他对某篇新论文的第一反应从"我要不要读它"变成"系统怎么标的、我同意吗"。每次不同意，他会写一句 why（这是 cold-start 期必要的 explicit signal，R2 搜索确认 hybrid 路线才稳定 —— 纯 implicit signal 在 research 场景太稀疏）。系统的 taste 逼近 lab 的品味一步。6 个月后新学生 Carol 入职，不再是拿到一份 20 篇的 must-read 静态列表，而是打开 topic 图看到 lab 的当前立场 —— "哪些 lab 已掌握、哪些 lab 仍在观望"—— 原本需要半年的口头传承被压缩成三天。**taste 不只是 session-level preference，它是 lab 的 intellectual asset，是可继承的**。

**如果 100 万高强度知识工作者都在用 —— 真正被替代的是什么**。不是 Google Scholar 或 arXiv 订阅，是 **Twitter/X 的 AI 研究 feed + 个人记忆碎片**。研究判断从依赖社交媒体热度（最吵的方向），转向依赖持续维护的脉络、边界与偏好。小 lab 开始更像"拥有一支稳定的资深研究编辑部" —— 它不替你好奇、不替你下最终结论，但它让你更少被热闹牵着走、更少因遗忘而重复劳动、更早看见一个方向到底在变硬、变薄，还是只是变吵。原 proposal 里"最终目标：lab 的研究智能体"那条线需要这一步的 topic 图 + taste asset + lab memory 作为前置 —— 这个 idea 是走通那条线的第 1 步。

**核心机制的一句话收束**：**把"发现 → 判断 → 归档 → 忽略（留痕）→ 回看 → 更新 SOTA 感知"折叠成一条连续回路**。六件事在现有工具里分散在六个产品、在用户的 workflow 里断裂成六段。这个 idea 的 product-shape 级新意就在于**把这六段压成一件事**。

## 2. Novelty assessment

**Verdict: Novel slice + Novel execution（不是 novel concept）**

诚实地说：如果停在"自动发现 + LLM 归纳 + 知识库 + taste 学习"的抽象层，这几乎完全不新 —— Elicit、Undermind、ResearchRabbit、alphaXiv、Paperpile、Zotero 都在这片地里。R2 的搜索进一步表明 team-level literature workflow 本身也不新：Covidence / DistillerSR 已经把"协作式 review + 可复用证据库 + audit trail"做成成熟产品，Iris.ai 2025 年推出了 "Researcher Workspace"。**所以 "unit-of-product 是 lab 而不是个人"本身并不是一个结构性空白** —— 这是 GPT R2 对 Opus R1 的重要削弱，Opus R2 明确接受。

真正没被占的是**这一条切片**：**"open-ended frontier surveillance + 共享编辑判断 + 可剪枝的低价值留痕 + 以 topic 状态（而非 paper）为产品核心对象"** 四点合起来作为一个统一的 editing & memory 系统。Covidence 类产品服务的是 systematic review（封闭问题 + 有截止时间），不是 open-ended frontier sensemaking；shared library 类产品停在"共享书架"，不会主动维护 topic state、不做 editorial judgment；Readwise / Are.na 的留痕 pattern 很强但不针对 research topic。把这四件事**合成一条连续回路并针对 AI research 前沿生存**，目前确实没有一个直接对位的产品。所以 novelty 落在 **slice（具体切片）+ execution（六段折叠成一段的 integration 方式）**，不在 concept。

## 3. Utility — concrete usage scenarios

### 场景 A · 周日晚的"假设是不是开始失效"
周日 22:30，做 post-training 方向的博三学生 Maya 在为周一组会准备。她原打算继续追一条已看了两周的 optimization 路线，但打开 lab radar 后，相应 topic 的 state dossier 顶部标红："一篇新工作没有提出更强结果，却拆掉了你这条路依赖的核心前提"；并串起她上个月读过、但从没意识到其实属于同一争论链条的两篇旧工作。Maya 把组会问题从"我们要不要复现这个方法"改成"这条路的假设是不是已经开始失效"。周一会后她跟 labmate 说："**它不是帮我多读了一篇，是帮我少浪费了两个星期。**"

### 场景 B · 季度选题时的"站位"而非"资讯"
lab 负责人 Dr. Chen 在为下季度选题做取舍，手上同时有 10 来个 topic。以前他靠浏览量、群聊讨论度和几篇印象深的 paper 做判断，容易追着最吵的方向跑。现在他打开每个 topic 的时间线，看到的不是"最近谁发了什么"，而是"这个 topic 过去八周发生了哪三次实质位移 / 哪条分支开始合流 / 哪条看起来热但其实没带来新的研究抓手"。他在组会上说出的不是"最近大家都在做这个"，而是"**这个方向值得继续，是因为它终于把一个旧问题变成了可推进的问题**"。radar 给他的价值不是资讯，是站位。

### 场景 C · 新学生入职的 3 天 onboarding
9 月入学的硕士生 Carol 被分配到 Agentic code generation 方向。以前她会拿到一串 20 篇的 must-read 链接和一句"先把这些读了"，然后花数周建立最基础的脉络感。现在她拿到的是一个 topic dossier：骨架工作有哪些、几次关键转折发生在什么时候、哪些路线是同源延伸、哪些争论一直没定论、lab 过去为什么多次提到它但一直没真正下注。Carol 三天后就能参与一次像样的讨论。她跟前同学说："**这像接手了一个会讲人话、而且记性很好的师兄的脑子。**"

### 场景 D · Lab 成员临时求助的 90 秒 topology 查询
周三下午 Bob（博士生）敲 PI 办公室："老师，我在想把 contrastive method 引入 preference learning，有没有类似的工作？"PI 以前要么凭记忆回答（常常漏）、要么让 Bob 自己 google（慢且浅）。现在他打开系统、输入问题 —— 20 秒后一张 topic 图跳出来：3 条相关路径、每条 3–5 篇代表作、其中 2 篇被标"Alice 去年读过"。PI 在图上圈出 2 篇给 Bob，同时告诉 Alice 这条路值得你重看。Bob 回去后对同学说："**老师的知识库是真 work 的，不是装样子的。**"

### 场景 E · 半年后的 "resurfaced breadcrumb"
7 月 Dr. Chen 在系统里标过一篇"incremental on X、暂存留痕"的论文。1 月他读到另一篇新工作时，系统主动提示："这和你半年前留痕过的那篇是同一思路的互补版 —— 两者合起来可能撼动 topic Y 当前主流立场。"他点开留痕、重新评估，把两篇一起丢进下周的 journal club。他说："**这个系统最反直觉的价值，不是帮我追新东西，是让我'没被浪费的直觉'在半年后还能回来找我。**"

## 4. Natural extensions（the long shadow）

**v0.2（0–6 个月内必然被 operator 呼唤出来）**：从"我知道什么"延伸到"**我们 lab 为什么在意**"。topic 页开始带 lab 语境 —— 这件新工作与我们当前问题的关系、上次为什么忽略过它、这次为什么要改判、哪些结论只是暂存判断而不是共识。这一步从"研究雷达"长成"研究上下文的共享容器"。这是 R2 GPT 写的 v0.2，收束到原 proposal 第 2 句就已经暗示的"为什么这件事对我们重要"。

**v0.5（6–12 个月，结构性一跳）**：**post-experiment integration loop**。lab 自己的实验结果（不只是外部论文）进入 topic 图 —— 系统开始主动对比 "lab 独家发现 vs 外部主流"，标出 lab 目前在哪些 topic 上与 field 有分歧、哪些与 field 收敛。这是从"研究消费系统"走向"研究生产系统"的桥，也是走向原 proposal 最终野心（research agent）的必经一步。

**两年内相邻产品**：
- **Fed-Lab brain**：多个小 lab 的 topic 图在某 topic 上有可合并的部分，合并形成半公开的"frontier 共识图"—— 2028 年 academia infra 的雏形
- **Lab-brain-for-onboarding**：把 topic dossier 做成学生入门的 guided tour 产品（可能是独立产品线）
- **季度 topic review / 组会 briefing / 问题导向补全**：这些都是同一母产品在不同节奏下的展开（日 / 周 / 月 / 季），不是分叉

**相邻用户段**：产业研究部门（企业内部 AI research group，承受同样的 abundance 痛）、投资 AI 的 VC（用类似系统追 market 而不是 paper）。**注意这些是 2 年后的相邻路径，不是 v0.1 的扩展 —— 在 v0.1 硬化之前拓宽用户段会稀释价值密度**。

## 5. Natural limits（the protective fence）

这个产品**不该是**：

- **不该是通用论文推荐系统**。价值密度来自"8–15 个聚焦 topic + lab 级 shared brain"。扩到"所有研究者的通用 discovery"会稀释掉结构化判断，让它退化成 Elicit。
- **不该是 consumer-grade 的"论文社交网络"**。PubPeer / Paperstars 那条线不适合 —— 公开评分 / 社交会让 lab 的 shared brain 变成表演场所；**私密与信任是基础**。
- **不该强吃 long-tail topic**。8–15 topic 是护城河；扩到 50 个 topic 系统的 topology 深度会变浅，从"深入"退化成"扫描"。
- **不该替代第一手阅读**。系统的终点是让 operator **知道要读什么、省 60% 的 triage 时间**，不是"不读"。**明确区分"替代阅读"（bad，品味会退化）和"委托 triage"（可能 good，这是研究编辑的本分）** —— 这是 Opus R2 对 GPT R1 §5 的精确化。
- **不该是一次性的静态产品**。价值在复利 —— 用得越久、lab 的 topic 图越厚、taste model 越贴近。**没有几个月的持续使用，它看起来会平淡**。v0.1 的 demo 必须有"6 个月累积效果"的故事，否则用户只会把它理解成另一个 daily newsletter。
- **不该押宝 graph view 作为唯一首页**。R2 搜索（emergency physicians 调查 + r/ML 讨论）明确支持 digest-first、topology 做 second-order explainer。graph 有用、但不是用户第一个回来看的东西。
- **不该走纯 implicit taste learning**。hybrid（explicit 种子 + implicit 延伸）才稳定；必须为"PI 写一句 why I disagree"留一个低摩擦入口。
- **不该变成"无差别囤积"的留痕**。低价值留痕必须带 discard / quality filter / promote controls（Readwise / Are.na 模式）—— 可逆、可剪枝、可重用，否则会塌成信息垃圾场。
- **不该过快滑向"全自动 research agent"**。那是邻近野心，不是 v0.1 站稳脚跟所必需的身份。
- **不该追求跨语言 / 跨文化广度**。对话 AI 领域 90% 前沿在英语 arXiv；过早扩到中文小众期刊或专利会稀释 signal。

## 6. Validation status

### Prior art landscape

| Name | Status | What it does | Lesson for us | URL |
|---|---|---|---|---|
| Covidence | Mature / 付费 | 团队协作式 systematic review（封闭问题 + 截止时间） | team-first literature workflow 并不新 —— 我们不是"第一个做 team"，我们做的是 **open-ended frontier sensemaking** 这条切片 | https://www.covidence.org/ |
| DistillerSR | Mature / 付费 | centralized evidence repository + audit trail + cross-team reuse | 可复用证据库 + audit 在 systematic review 侧已成熟；我们的差异是 **topic state 而非 review project** | https://www.distillersr.com/ |
| Iris.ai Researcher Workspace | 新发布（2024–2025） | integrated research workspace（project / notes / papers 聚合） | "integrated workspace" 概念已被占；我们差异在 **editorial triage + 低价值留痕** | https://iris.ai/announcements/iris-ai-launches-the-researcher-workspace/ |
| ResearchRabbit / Litmaps / Connected Papers | 2025 被 Litmaps 收购整合 | citation graph 探索、discovery | graph view 有用户但赢家未定；**不押宝 graph 作为唯一形态**，用户评论多为正面但无公开留存数据 | https://aarontay.substack.com/p/researchrabbits-2025-revamp-iterative |
| Paperpile / Zotero shared library | Mature | shared library / group | 停留在"共享书架"层 —— 不是持续更新的 topic-state editor。差异化空间在此 | https://paperpile.com/h/create-shared-library/ |
| Readwise Daily Review | Mature / 付费 | highlight resurfacing + frequency tuning + discard | 低价值留痕的 winning pattern 真实存在 —— 但必须配筛选 + 丢弃 + 再组织，不是囤积 | https://docs.readwise.io/readwise/docs/faqs/reviewing-highlights |
| Are.na | Mature | weak-signal breadcrumb 归档 + 社区 | breadcrumb 归档能形成稳定付费社区，但仍靠 pruning 维持价值密度 | https://www.are.na/ |
| Elicit / Undermind | Mature | question-first systematic review / AI-assisted search | question-first 入口不稳定（BMC 2025 评估：同一 query 结果不一致）；作为**组织透镜**可以，作为**唯一进气管**不行 | https://elicit.com/ · https://www.undermind.ai/ |

### Demand signals

| Source | Signal | Strength (H/M/L) | URL |
|---|---|---|---|
| r/MachineLearning "how do you keep up" 讨论 | "全域不可能跟上，只能依赖 conference / trusted curators / aggressive filtering" 反复出现 | H | https://www.reddit.com/r/MachineLearning/comments/1ren2m5/d_how_do_yall_stay_up_to_date_with_papers/ |
| Huddersfield 2024 reference-management practices | workflow 复杂度随资历显著上升（taught students → PGR → staff），多套系统混用 | H | https://www.sciencedirect.com/science/article/pii/S0099133324000405 |
| Emergency physicians keeping-up 调研 | 最大 barrier 是 time；偏好 mediated resources（podcasts / conference / subscription），**不偏好原始论文流** | H | https://pmc.ncbi.nlm.nih.gov/articles/PMC9178355/ |
| r/Researcher / r/PhD 文献管理讨论 | "知道读过但想不起是哪篇、为回找信息要在多套系统里翻" 反复出现 | H | https://www.reddit.com/r/PhD/comments/1r48pw3/how_do_you_document_papers/ |
| Zulip for research（Stanford CS 博士生投票切换） | 小 lab 主动选 topic-based 通讯工具 —— 证明 topic 作为组织维度的 demand | M | https://zulip.com/for/research/ |
| Notion Figma "The Figmanual" 案例 | team knowledge base 可长期 work + "grows with them without rebuild" | M（类比而非同构） | https://www.notion.com/customers/figma |
| Management Science 2024 "willingness to delegate to AI" | **loss aversion 显著降低 delegation 意愿**（漏看关键论文 = loss） | M（风险信号） | https://pubsonline.informs.org/doi/10.1287/mnsc.2024.05585 |

### Failure cases

| Name | Status | Why it died | Avoidance for us | URL |
|---|---|---|---|---|
| Mendeley public groups | 2020-12 **整体下线** | (1) passive sharing 塌回个人（2/3 group 只剩 1 人）；(2) 平台单方面下线 + 无预警数据流失 | **明确承诺 data portability / export / open format**；lab 数据不能被平台绑架 | https://www.researchgate.net/post/Groups_disappeared_from_Mendeley_What_can_I_do |
| Paperstars / 公开 review 社区 | 低活跃、review 密度稀薄 | sustained trusted participation 比发明 format 更难 | 起点是**小而受信任的 lab**，不是通用公共 marketplace | （L1R2 引用） |
| Field weather / map-of-AI dashboards | 漂亮但无人基于它做决策 | "sense the weather" 是氛围不是 decision | 每个 view 都必须对应**今天 / 这周该做什么** 的具体动作 | （L1R2 引用） |

### Net verdict

**Should this exist? Y-with-conditions**

两轮双方独立收敛到"外置研究编辑部 / lab-scoped research editor"这个 sharp version，且 6 + 6 次搜索 net 支持（winning pattern 存在、真实 demand 广泛、failure cases 都可以前置设计对冲）。这不是一个"是否值得做"的问题，而是一个"怎么做不会塌"的问题 —— 所以是 Y-with-conditions，不是 unclear。

**Conditions（必须在 L3 明确承诺的硬条件）**：

1. **数据可移植性承诺** —— 防止重演 Mendeley：self-host option、export、open format 三选至少一
2. **首页 digest-first、topology 为 second-order explainer layer** —— 不押宝 graph 作为唯一入口
3. **taste learning 必须是 hybrid（explicit 种子 + implicit 延伸）**—— 每次 operator 对系统标注不同意时写一句 why 是产品必需品，不是可选 feature
4. **低价值留痕必须带 discard / quality filter / promote controls**（Readwise / Are.na 模式），严禁无差别囤积
5. **buyer / operator 分层明确** —— PI 是经济 buyer，senior PhD / postdoc 是高频 operator；两个 persona 必须同时被服务，但可能有不同的 entry points
6. **"用户愿意委托过滤判断"是 L3 必须用 user interview 解的未解假设** —— Management Science 2024 说 loss aversion 显著压低 delegation，研究者漏看关键论文 = loss，这条假设没有直接 survey 证据；**在 scope L3 之前应先做一轮真实用户访谈**

## 7. Open questions for L3 / for user research

| # | Question | Best answered by | Why it matters |
|---|---|---|---|
| 1 | **v0.1 先优化 buyer（PI / lab lead）还是 operator（senior PhD / postdoc）？** | user interview（访谈 3–5 支 AI lab） | briefing 形态、权限、协作 ritual 完全不同；这是 product-shape 级决策，不是 feature 级 |
| 2 | 首页形态：digest-first 还是 map-first？ | user interview + A/B 小型 mockup 测试 | 搜索支持 digest-first，但差异化叙事可能依赖 topology；必须做真实取舍 |
| 3 | **研究者真的愿意把 "low-priority 不推 / 自动 skip" 委托出去吗？还是只接受 summary、不接受 filter？** | user interview（测 loss-aversion 临界点） | 如果只接受 summary 不接受 filter，idea 的上限会低很多；这是产品天花板问题 |
| 4 | 低价值留痕的归档层是个人层、topic 层、还是 lab 共享层？ | user interview（涉及信任与治理，非 L2 可推断） | 决定 lab 内部数据模型 + 权限 + 编辑规则 |
| 5 | data portability 的具体承诺形态：self-host / export / open format？ | L3 decision（user constraints + 产品定位） | 防止重演 Mendeley 的硬条件，直接影响早期架构决策（部分进入 L4） |
| 6 | Cold-start 期 PI / operator 愿意写 "why I disagree" 的最低频率？太低系统学不会，太高用户放弃 | user interview + 小型 diary study | taste agent 是否能 work 的必要条件 |
| 7 | 从多少个活跃 lab 开始，topic 图 + taste agent 的复利效果显著？一个 lab 自己用是否足够？ | empirical（v0.1 上线后数据），但 L3 需要对 "早期是不是要 bootstrap 多支 lab" 有假设 | 决定 go-to-market 节奏 |

### 三条两边 R2 收敛的 user-interview 问题（强烈建议 L3 前做）

两轮对手评审最后独立汇合到同一组诊断性问题上。这是一个明确信号：**L2 的想象力到这里为止，必须要真实用户输入才能继续**。

1. **当你说"我最近跟不上了"，先坏掉的是哪一层：发现新东西、记住旧东西、还是判断什么值得看？** 这三者哪个是核心会直接改变产品形状（digest vs memory vs editor）
2. **过去一个月里，你在文献相关工作上最浪费时间的具体瞬间是什么**：找新 paper、补回上下文、还是找回自己已经看过的东西？
3. **如果系统对你说"这 7 篇先别读，这 2 篇今天读，这 5 篇只留痕"**，你会信任哪一部分、又觉得哪一部分越界？—— 这一条同时测 delegation 边界 + loss aversion 临界点

**Moderator 强烈建议**：在 `/scope-start 001` 之前，先找 3–5 位真实 AI lab 成员（最好至少 1 位 PI、2 位 senior PhD / postdoc）做半小时访谈，用上面三个问题开场。L3 without user input often produces rework —— 这一条在本 idea 尤其成立，因为 §6 的 condition 6（delegation 假设）和 §7 的 Q1（buyer / operator 锚点）是**产品形状级**决策，不是 feature 级。

## 8. Decision menu（for the human）

### [S] Scope this idea — proceed to L3
```
/scope-start 001
```
推荐前提：你已完成至少一次真实用户访谈（§7 的三条诊断性问题），对 Q1（buyer / operator）和 Q3（委托边界）有初步判断。此时 L3 能把 §6 的 6 条 condition 和你的真实约束（预算、时间、平台、必须用 / 不能用什么）合成 PRD-v1。

### [F] Fork another L2 angle from this same idea
```
/fork 001 from-L2 <new-angle> as <new-id>
```
如果读完本报告你觉得某个更锋利的切口浮现了（例如：只做 v0.1 = digest-first briefing + 低价值留痕，砍掉 taste agent；或者反向：只做 taste agent + 辩论陪练 —— 接近 Taste Twin 但以 lab 为 unit），可以 fork。

### [B] Back to L1 menu
```
/status 001
```
L1 的 13 条 inspired directions 仍然完整保留。本报告收束到的 sharp version（lab-scoped research editor）在 spirit 上最接近 L1 的 **Direction 2 "Lab-Scale Shared Intelligence"**，但本 L2 是以 **原 proposal** 为对象 —— 如果你读完觉得某条 L1 direction（例如 Dissent Cartographer / Permission-to-Drop / Question→Dissent Belief Router）比当前 sharp version 更锋利，可以从那里 fork 并行展开。

### [R] Re-explore with new input
如果上面任何 open question（尤其是 §7 Q1 / Q3）让你有新的引导想法，或者访谈后发现新的 persona / pain point，可以：
```
/explore-inject 001 "<你的 steering>"
```
然后再跑一轮 L2R3。

### [P] Park
```
/park 001
```
保留所有 artifact。**如果你此刻没法做用户访谈、而又不想在无访谈的情况下 scope 出 PRD**，这是诚实的选择。访谈条件 ready 时 `/status 001` 随时复活。

### [A] Abandon
```
/abandon 001
```
**不推荐** —— verdict 是 Y-with-conditions，不是 N。除非你确认不再关心 AI research 跟进这个问题域。

---

## Fork log
（初始为空；每次 `/fork` 命令执行后由它更新）
