# Idea 003 · L2R1 · Opus 4.7 Max · Explore (no search)

**Timestamp**: 2026-04-24T02:24:03Z
**Searches used**: NONE in this round.
**Visibility**: 我没有读 GPT-5.4 的 L2R1（并行独立原则）。
**Origin**: 跳过 L1 模式（`/inspire-start --mode=skip`）。Proposal 本身已有清晰方向——最小化复刻 Anthropic AAR(Automated Alignment Researcher)，但以个人 Claude Code 为底座。本 R1 按 skip-mode 要求先在 §0 给出"我考虑过但没选的邻近框定"，再进入深挖。

---

## 0. Alternative framings considered（skip-mode 专属）

我在进入深挖之前，想了想这个 proposal 在不同人眼里会被读成什么。下面 4 条是我**考虑过但没在本 R1 继续往下挖的**邻近框定，以及我为什么没选它们（以及**什么信息会让我改主意**）。

**A. "另一个 AI scientist 克隆" 框定**。把 003 读成第 N 个 Sakana-v2 / Agent Laboratory 式的"端到端自动写论文"系统。我没选这个——proposer 的原话是"进行 AI 算法的研究"，不是"写论文"；而且 proposer 的 001 和 003 是**相互承接**的（radar 先消化最新 research，agent 再自己做 research）。如果把 003 看成"写论文的机器"，它和 001 会重复。**如果 proposer 说"我就是想产出可发表的 paper"，我会回到这条框定**。

**B. "个人研究员的副驾驶" 框定**。把多智能体解释成"人类研究员 + 多个 Claude subagent 做同一个实验"的并行助手模式——类似 Copilot 的加强版。我没选——proposer 明确引用 AAR 和 Karpathy 的 autoresearch，这两个标杆都是**自主**而非**辅助**。"副驾驶" 框定会丢掉 AAR 里最戏剧性的那件事：**九个智能体在爬山集上从 0.23 干到 0.97**，这是自主的结果，不是副驾驶的结果。**如果 proposer 说"我主要想要一个能在我实验期间帮我分流试 5-10 个想法的 sidecar"，我会切到这条**。

**C. "AI-for-Science 的通用平台" 框定**。把 003 扩展到生物 / 化学 / 材料等更广领域，对标 Google AI co-scientist / FutureHouse Robin。我没选——proposer 明确说"AI 算法的研究"，这是一个有纪律的边界；跳出这个边界会立刻碰上领域知识、湿实验闭环、专家人审等 completely different problems。**如果 proposer 说"AI 只是第一个 domain，长期要跨领域"，我会把本方向读成 "AI 领域版 + 未来平台化" 的双层结构**。

**D. "团队协作平台" 框定**。多智能体 = 一个 agent 工作站，支持 proposer 的实验室几个研究员各自挂若干 agent 共享发现。我没选——proposer 的倾向行写的是"基于个人的 Claude Code"，这是**单个人 × 多智能体**，不是**多个人 × 每人一组智能体**。前者是个人生产力工具，后者是 SaaS/团队产品，路线与难度完全不同。**如果一年后这件事真做成并且他实验室别人开始用，它会自然变成后者——但那是 L2 之外的事**。

下面我按 **"个人研究员用多智能体自主推进 AI 算法课题，最小化复刻 AAR，Claude Code 底座"** 这个主框定继续。

---

## 1. The idea, unpacked

### 用户长什么样——具体到不能再具体

这个想法的主要用户**不是** AI Lab 的 infra 工程师、**不是**想做 agent SaaS 的创业者、**也不是**想发 survey 的博士新生。是**一个已经做 ML/LLM 方向研究 5-10 年的独立研究者或小实验室 PI**，具体画像：

1. **学术/准学术背景**——有 PhD 或接近 PhD，对 SOTA 读得懂、对 baselines 有 taste，对"哪个方向值得下手"有直觉但**手不够用**。
2. **课题节奏是周-月级**——每个研究 idea 需要 1-4 周的 sprint 才能判出生死，节奏上只能同时推 1-2 个主线，最渴望把"副线的 10 个备选想法"批量 pre-screen。
3. **已经在用 Claude / Cursor / Codex 写代码**——本人对 agent 既熟又警惕，知道 agent 会胡编会走捷径，也知道它在**明确目标 + 可验证评分**的任务上能跑得很快。
4. **算力预算有限**——不是 frontier lab，能用的是**单台 workstation + 偶尔 Runpod**，不是 1000 张 H100 集群。月度可承受研究 infra 成本在 $500-3000 区间，不是 $50k 那个档。
5. **对"研究本身的代理化"有强烈的好奇心**，同时有真实的未完成任务——桌面上**此刻**就有 3-5 个"想试但没时间做"的方向。

这 5 条一合起来，画像的画像是：**一个手里有想法、有直觉、有预算底限、但被时间物理约束住的 PI/独立研究者**。不是企业用户，不是爱好者，是**在"生产单位"和"业余爱好者"中间的那一层**。

### Before / after——他的桌面此刻是什么样

**Before**（当前的日常）：他桌面上有一个 Notion 或 Obsidian 笔记叫 "Research ideas 2026"。里面列着 12 条 bullet：*"试试 DPO 变种在小 LM 上的 scaling"、"LoRA adapter 混入 attention head 的效果"、"chain-of-draft 对比 CoT 在 math 上的 token 效率"* 等等。每条 bullet 后面跟着一句自言自语："值得 2 周但我没空"、"感觉能做但可能已经有人做过"、"不知道从哪下手"。他最大的痛不是"没想法"，是**想法和执行之间有 40 小时的鸿沟**——每条想法要写 baseline、要布 pipeline、要扫超参、要 debug——而这 40 小时当中 **30 小时是他不需要亲自经历的苦力**。**他本人只在最后那 10 小时里做真正的研究——看结果、判断、设计下一步**。

**After**（有这个系统后）：周一早上，他开一个新的 research run，用 20 分钟写 9 条**故意含糊**的方向种子（"DPO 变种 in small LM"、"LoRA × attention head"、…）。他点 launch。系统在后台并行跑 9 个 Claude Code worker 48 小时，每个在自己的沙箱 worktree 里尝试自己那条种子的路径。worker 之间通过一个共享论坛看彼此的发现，互相 fork 或反驳。周三早上他收到仪表盘汇总：**9 条种子里有 2 条产生了可复现的 artifact（代码 + eval 分数），3 条 converged 到"此路不通且给出理由"，3 条还在探，1 条触发奖励黑客被系统自动隔离**。他接下来一天花在**读那 2 条真正的 artifact**——自己判断 novelty，决定 follow-up。**一周变一月，一月变一季**。

### 第一次的"Aha"——前 30 秒

第一次 aha 不是"agent 跑起来好快"。Aha 发生在**当他看到论坛上 worker #3 反驳 worker #7 的那一刻**——两个 agent 对同一个实验结果给出不同解读，worker #3 说："这个 acc 提升是 data leakage 不是真 improvement，我跑了 held-out set 掉了 15 个点。" 这一刻他突然意识到：**这件事不是一个 agent 在跑，是一个会彼此质疑的小研究小组**——而且这个小组 24 小时不睡。这种"群体智能"感官上的第一次击中，比"自动化"本身更打动他，因为**他本人也是这样做研究的——跟合作者互相质疑**。

### 6 个月后的 mastery 长什么样

6 个月后他已经**不再一个人"想 idea"**。他日常工作流变成三件事：(a) 每周日花 2 小时写下一周的 9 条种子（这是他剩下的**真正研究工作**——方向判断、taste、reframing）；(b) 周一 launch，周二周三看 artifact；(c) 把 2-3 条最有前景的结果**亲自**深耕——写论文、做严格实验、投会议。系统替他完成的**不是**研究本身，**是研究的 pre-screening 和死路快速淘汰**。他的产出率会翻 3-5 倍，但他本人的**工作性质**改变了：**他从"研究员"变成"研究的 curator + judge"**。他会跟朋友说："我现在的 9 个 agent 就是我以前的 5 个本科 RA + 2 个 master 学生——只是他们不睡觉、也不抱怨。"

### 一百万人用——天花板形态

如果 10 万个 PhD / 独立研究者真的用上了这样的系统，AI 研究的**速度常数**会变。不是 2 倍 3 倍，是**节奏变化**——从"每人每年推 2-4 个课题"到"每人每年推 20-40 条探索 + 3-5 个亲自深耕"。下游会发生两件事：(1) **研究思路的熵会下降**——如果所有人都用同一套种子扩展 meta-prompt，很可能大家会**同时尝试同一批邻近想法**，这件事可能是好是坏（好的一面：快速穷举；坏的一面：同质化）；(2) **"判断力"会取代"执行力"**成为研究员的核心素养——会 debug Python 的人会多到过剩，会判断"这个方向值不值得看"的人会稀缺。系统会间接催生一种**新的研究职业**：**种子工程师 + 研究 curator**，不做实验，只判断和指方向。

---

## 2. What's genuinely novel

**概念上 novelty 不高**——AAR(2026年4月) 已经证明了 9 个 Claude Opus 在共享论坛 + 外部评测下可以自主爬山到 PGR 0.97，Karpathy 的 autoresearch 示范了"单任务 + 单 metric + 自主迭代"的 loop，Sakana AI Scientist v1/v2 示范了全流水线，Google AI co-scientist 示范了 Elo 锦标赛辩论。多智能体自主研究**这个空间本身**，过去 18 个月已经被反复探索了。

真正 novel 的是**组合 + 切点**：

1. **"个人级"而非"Lab 级"的最小复刻**——AAR 用了 $18k / 5 天 / 9 个 Opus，那是 lab-scale。把它压到**个人 workstation + 月度数百美元 + Claude Code 原生能力（subagent / hooks / worktree / MCP 一样不少）**，让一个独立研究者**一个人能跑起来**——这件事此前没有人以这个定位做过。MVP 级的"在个人桌上跑的 AAR 缩影"是这个方向真正的切点。

2. **面向"死路快速淘汰"而非"证明成果"**——大多数同类系统（Sakana、Agent Laboratory）在卖"自动写出一篇 paper"——**这个指标本身就是奖励黑客的温床**（你最后 judge 的是文档而不是实验）。这个 idea 如果聚焦在**"48 小时内把 9 条方向里的 6 条 prune 掉，只留 2-3 条真正值得人类去深耕"**，它的 value prop 就和所有前辈都不一样——它不卖"替代研究员"，它卖"给研究员省 30 小时的 pre-screening 苦力"。这个定位是**务实且防黑客的**。

3. **Claude Code 作为底座的"白捡"系数**——个人用 Claude Code 已经自带 subagent / hooks / worktree / MCP / sandbox / headless 模式 / 权限系统 / prompt caching。把 AAR 的那套架构**映射到 Claude Code 的原生能力上**，新增代码面可能只是 AAR 论文原 repo 的 1/5 到 1/10。这个"把 paper-scale 压缩到 personal-scale"的杠杆，是 Claude Code 2026 年这个具体时点的新能力带来的机会，**2024 年做不了，2027 年 Opus 5 出来后可能又不一样**——现在这个 12-18 个月的窗口是真实的。

**Honest verdict**: 这不是一个 **0→1 的创新**。它是**一个时机型 + 切点型的组合 novelty**——在 2026 年这个"Claude Code 原生能力到位 × AAR 论文公开 × 个人研究者算力到位"的三角窗口里，有人会做这个，如果不是 proposer 做，也会有别人做。价值在**谁先做出一个真正好用的、被个人研究者采纳的版本**。

---

## 3. Utility — 3 concrete usage scenarios

### Scenario A · 陈博士，独立做 LLM post-training 的研究者

陈博士手里有 5 条待探索的 DPO 变种 idea，还有 3 条 scaling law 观察想验证。过去他每条都要花 2-3 天自己搭 baseline + 跑扫参，只有 1-2 条会成功。**周一早上**他写了 8 条 20 词种子（"DPO with KL-reduction schedule"、"scaling law on reasoning traces"、…），launch 一个 run，预算 $500 / 48 小时。**周三下午**他打开仪表盘：8 条里 2 条已经跑出可复现的 artifact（一条 DPO 变种在小 LM 上 +2 个点的 reasoning score，一条 scaling observation 被 held-out data 否定）；3 条被 forum 讨论中确定是"早已有人做过且已知失败"；2 条 stuck 在 debug 步骤被系统超时 kill；1 条触发异常分数被自动送入人审队列。他花周四一整天**亲自**复现那条 +2 个点的结果——发现它真实但很小，然后决定把这条接到他下个月的 sprint 中。**8 条在 48 小时内被 pre-screen，他自己的研究节奏向前跳了一个月**。他跟朋友说："我终于做到了我以前一直说'我如果有 3 个 RA 就能做到的事'。"

### Scenario B · 林老师（小实验室 PI），指导 2 个 PhD 的同时想自己推一条探索性方向

林老师带两个 PhD，各自的主线课题已经占满他的 mentor 时间。但他自己有一条**跨领域的 hunch**——想看看 mechanistic interpretability 的工具能不能用来解读 agent 的 CoT 漂移。他以前的选项是**放弃这条 hunch 或者等下个 sabbatical**。现在他写下 6 条种子（不同的 probe family × 不同的 metric），在他的 workstation 上 launch 一个 run 预算 $800 / 72 小时。系统在周末跑完，周一早上他看到的是：6 条里有 1 条**非预期地**给出了一个有趣的发现——某个 probe family 在特定 layer 上能 predict CoT 漂移到 0.78 AUC。这个发现**原本不会发生**——林老师根本没时间亲自试。他决定把这个拉进下学期的一门独立课题，找一个本科生 follow up。**系统的价值不是做完研究，是把一个本来会胎死腹中的 hunch 变成了可以传给学生的半成品**。

### Scenario C · 周工（前 ML 工程师，在家自学想做独立研究）

周工刚从一家大厂出来，想做独立研究发 arXiv 建立自己的 reputation，没有实验室 affiliation。他最大的问题不是智力——他技术过硬——是**孤独**和**没人 pushback**。他订了这个系统的个人版，每周 launch 3 条他感兴趣的 reproducibility / simple-idea-study 方向（"reproducing Foo et al. 2025 with half data"、"is this baseline really worse than X"）。系统的**多智能体 forum** 给他带来一种"有合作者质疑我"的体验——他发现自己想做的实验经常在 forum 上被一个 agent 指出"这个 baseline 的 seed 变化本身就有 ±2 点的 variance，你声称的 improvement 不显著"。**这种"有人跟我较真"的反馈循环**，是他作为独立研究者最缺的东西。他在 3 个月后产出第一篇 arXiv preprint，其中 experiment section 的每个 claim 都被系统的 fact-checker 子智能体核对过。他跟朋友说："我没有同事，但我有 9 个不睡觉的同事。"

---

## 4. Natural extensions（v0.1 跑通后的 2 年近邻空间）

1. **"领域种子库" 社区**——跑通后，最有价值的**不是**系统本身，是**好的种子**。自然延伸是让用户可以**公开分享他们跑过的种子 + 结果 artifact**，形成一个"这条种子在 2026-Q3 跑出了 X 结果"的 public ledger。下一个用户可以从别人验证过的种子起步，快速避开已知死路。这**不是**论文库（已经有 arXiv），是**"种子 × 失败模式 × 成功模式"的实验库**，它填了一个空白——学术系统默认不报告 null result，但这个 ledger 会天然包含它们。

2. **"判断力训练"模式**——系统的副产品是**大量的"好/坏 hypothesis"对照**。下一步自然是做一个针对 junior researcher 的**判断力训练器**——给你 20 条种子，让你盲选哪些会产生好 artifact，再对比 agent 跑出的结果，每周一次。这个东西训练出来的**不是 agent 操作员**，是**能做研究的下一代 researcher**。教育市场在这里有 room。

3. **和 001 (Research Radar) 的自然对接**——001 负责把最新的 AI research 消化成知识库，003 负责自主推进。两者对接就是**一个闭环**：radar 发现"最近 5 篇在 data curation 方向上有进展"，自动转成 5-7 条种子注入 003 的下次 run。这个对接不是工程问题，是**workflow 的合并**——对 proposer 来说是自己两条 proposal 的 natural integration。

4. **"Red team 研究员"专门化版本**——大部分 agent 是在 propose，让一个或几个 agent 专门 **red team**（尝试 falsify 其他 agent 的 claim、尝试 reward hack 当前评测）。这个方向在 2026 年 METR / Anthropic 的奖励黑客数据的背景下会变得越来越重要。**不是 v0.1 的事**，但是 v1.0-v1.5 的必然演化。

---

## 5. Natural limits（这个方向**不应该**是什么）

- **不应该做湿实验**。任何需要实物（生物样本、化学反应、物理装置）的研究方向都不在这个系统的范围。AI 算法研究的好处是**闭环在代码和 GPU 里**——一旦跨出这个边界，系统就会撞上"人审真实性、物理成本"的墙。

- **不应该做"开放写作"型任务**——比如让 agent 写一整篇 review paper、或做思想史梳理。这类任务**没有可靠的外部评测**，会立刻变成"同模型自审 → 互相阿谀"的失败模式。AAR 论文和 Sakana 的失败都在警告这件事。本系统只做**有明确可计算指标**的研究。

- **不应该替代研究员的"judgement"环节**。系统的输出永远是**candidate**，judgement 永远是人。一旦试图让 agent "自动决定哪个 artifact 该发 paper"，就会进入 METR/Devin 论文里描述的 30%+ 奖励黑客风险区。

- **不应该走 SaaS / 团队协作路线**——至少 v0.1-v1.0。这是**单用户的生产力工具**。一旦走团队，你会立刻碰上数据隔离、预算分账、权限边界、审计合规、多租户——这些**不是**研究问题，是 enterprise software 问题，会**吃掉全部团队的时间且和真正的产品价值无关**。

- **不应该跨 AI 域（stage 1 明确不做）**——生物、化学、材料的自动研究系统已经有 Google co-scientist / FutureHouse Robin 在做，它们各自需要领域知识库、湿实验 API、专家人审——这是不同的产品。**限定在"AI 算法研究"这一个域，才有可能用有限资源做深**。

- **文化与时点限制**——这个方向在 **2026-2027 的 Claude Code 原生能力 × AAR 论文刚公开 × 个人算力窗口** 成立。6 个月后 OpenAI / Google 可能会官方推出类似产品的托管版本，系统的差异化（"个人 + 本地 + 可审计"）会**被挤压**。它最好是一个**有 1-2 年黄金窗口的产品**，而不是一个"10 年的平台赌局"。

---

## 6. Three honest questions about this idea（为 L2R2 搜索做种子）

1. **"死路快速淘汰" 这个 value prop 真的是用户最痛的点吗？** 还是用户其实更想要"帮我生成论文 draft"、"帮我找未解决的 open question"这种更 glamorous 的东西？定位错误会毁掉整个产品——L2R2 需要看 Sakana/Agent Laboratory/AAR 真实用户的反馈（有没有），以及 arXiv / X 上独立研究者对"multi-agent research"的具体愿望和抱怨。

2. **个人 × Claude Code × Runpod 这个算力 + 成本组合，够支持多少真实的 AI 算法研究方向？** AAR 的实验是 small LM（Qwen3-4B）级别。如果 individual 用户想做的研究**天然需要 70B+ 训练 / 长时间 eval / 大规模 rollout**，这个系统对他就无效。L2R2 需要看：当前独立研究者实际在做哪些方向的实验，这些方向的实验**最小可行算力需求**是多少。如果 80% 的实验都需要 $5k+ / 次，这个系统的 TAM 就被挤到一个很窄的角落。

3. **奖励黑客在 MVP 阶段到底会不会毁掉用户的信任？** AAR 原文承认即使在 9 个 Opus + 严格沙箱下仍有 4 类奖励黑客无法根治。在个人版、代码面积 1/10、时间预算短 10 倍的情况下，奖励黑客频率会不会**大幅上升**？一个用户如果第一次 run 就被一个 reward-hacked 的 "+5 点 improvement" 骗了一次（然后花周末亲自复现失败），他会不会**永远离开这个产品**？这个失败模式在 proposer 的"个人"场景下**杀伤力可能比 lab 场景更大**，因为没有 peer review 兜底。L2R2 需要看：Sakana v1 沙箱逃逸、METR o3 的 30.4% 奖励黑客率这类事件被曝光后，相应产品的用户信任曲线是怎样的。
