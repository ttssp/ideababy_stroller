# L2 Explore Report · 005 · 「PRD-to-confidence framework（不是 PRD-to-code 工厂）」

**Generated**: 2026-05-07T00:00:00Z
**Source**: 直接来自 `/inspire-start 005 --mode=skip`（root idea，未经 L1；proposal 状态 menu-ready 但 L1 目录从未真正生成）
**Source rounds**: L2R1（Opus / GPT 各一份）、L2R2（Opus / GPT 各一份）
**Searches run**: 10 次价值验证检索，跨 ~9 个独立来源（Devin/Cognition、addy osmani、Anthropic、arxiv 2502.13069、arxiv 2603.26233、Microsoft ACE、Stack Overflow 2025、METR RCT 2025、The New Stack / arxiv 2505.19443）
**Moderator injections honored**: 无（标准 advance，非 redebate）
**Skip-mode 信号**: 双方在 §0 都列了 4 个被否决的替代 framing；最强的共同信号是**两边都明确拒绝把 005 读成「human-out-of-the-loop 软件工厂」**——这是后续所有论证的基础。

---

## How to read this

这是 L2 对 idea 005「auto agentic coding」的深度展开。和 L1 菜单（多个浅层方向）不同，这是**一个想法的一种丰富理解**。看完之后你应该清楚：
- 005 真正是什么（**不是**它表面看起来的样子）
- 为什么值得做（以及哪些诚实的理由让你重新考虑）
- 它能长成什么、不该长成什么
- 进 L3 之前你必须自己回答（或先去访谈用户后才能回答）的问题是哪些

---

## Executive summary

- **005 的真正定位是 PRD-to-confidence framework，不是 PRD-to-code 工厂**。两位评审在 R2 罕见地收敛到同一个 framing：管道的产出不应该只是代码，而应是一张**「自动推进区 / 必须澄清区 / 事后可审计区 / 暂停区」的信心地图**。
- **概念层 novelty 接近零，但有两个真实空白**：(a) 把 ambiguity 检测+暴露做成**结构化 checkpoint**（学术界证实这是 SOTA 模型自己也搞不定的硬问题）；(b) 把 addy osmani 已经做到的「项目级 AGENTS.md 累积」**扩展为用户级长期 calibration profile**。其他部分（spec-driven / TDD-gate / review）都是站在 addy agent-skills + Superpowers 的肩膀上。
- **目标用户被精确定义为「强需求表达者 + 弱工业交付直觉者」**——CS PhD / ML 研究员型，能写结构化 PRD、读得懂工程原则，但缺工业肌肉记忆（TDD 习惯、code review 直觉、scope 取舍）。这必须**原话写进 L3 PRD**，不能漂成「非程序员」。
- **抗重做是硬约束**——human 已经连续 deprecate 了 4 个版本（idea_gamma2 / vibe-workflow / autodev_pipe / 当前 repo）。005 v0.1 必须**结构上能演化**，不能要求 v0.1→v1.0 推倒重来；否则它就是第 5 次。
- **验证 verdict：Y-with-conditions**。市场需求被多方证据强证实（Devin 失败模式、46% 信任缺口、vibe→agentic 转向）；但要做出差异化，必须**收紧到上面那两个 novelty 缺口上**，而不是再发一个「AI 写代码」框架。

---

## 1. The idea, fully unpacked

**005 的本质不在「让 agent 写代码」，在于让一个特定人群「敢相信 agent 写出来的代码」**。两侧 R1 都从用户画像入手，R2 收敛到一个让人耳目一新的 framing：005 是给"**会写 PRD 但缺工业交付直觉**"的单人操作者用的——不是给所有非程序员，也不是给已经能写代码的开发者，是切在中间的一类很特殊的人。human 自己就是样本：CS PhD、ML 出身，能讲清"为什么要 TDD"、"什么是 spec-driven"，但从没在大公司跟过几个版本的迭代节奏，没踩过"测试覆盖率假高真低"的坑，也不知道"灰度发布"的真实意义。这群人有钱、有时间、有品味，但缺一种深度——把一个想法跨过工程实现的鸿沟、到达可信赖软件这件事的**肌肉记忆**。

**005 之前的日常是高认知负担 + 低确定性**。每开一个新项目都从零搭脚手架——挑 skills、挑 subagents、写 playbook、跑一段、回头改 prompt、再跑、发现 agent 偷工减料、加约束、回归测、走 loop。可以启动很多 agent，可以写越来越长的说明，但心里始终有一个问题没解决："**我现在看到的，是专业工程推进，还是一套看起来专业的文本仪式？**"于是项目变大时反复重建流程，每次失败都像在提醒"这套方法不够专业"，旧流程被归档、新流程被命名、新一轮希望开始——但**真正的判断资产没有稳定累积**。human 已经做了 4 次这种循环，005 必须打破它。

**005 之后的日常体验**不是"它替我写代码"，而是"我终于知道每个阶段该相信什么"。PRD 不再只是给 agent 的输入，而是进入一套从意图、范围、任务、验证、评审到交付信心的连续语言。aha 时刻不是看到代码生成，是在前 30 秒看到系统把需求翻译成一组清晰的承诺——**哪些是产品决定、哪些只是待澄清问题、哪些需要人类裁决、哪些可以交给自动化推进、哪些证据会让系统说"可以继续"**。这种体验让 human 第一次感到自己不是在哄模型做事，是在操作一个有纪律的交付机构。

**关键体验设计：高杠杆裁决经济学**。两位评审在 R2 用不同语言描述了同一件事——GPT 称之为"裁决经济学"（高价值决策保留 / 低价值救火外包），Opus 称之为"工程纪律硬连线"（spec/test/review/gate 从软规范变成结构上不可跳过的硬约束）。合起来就是：**最高自动化 ≠ 最少人工，而是最少低价值陪护 + 最多可审计信心**。human 的角色从 lvl-1 救火员升级为 lvl-3 裁决者；管道在 PRD 不清时**主动停下来 surface 决策**，并把"我做了哪些超出 PRD 的判断"清单留给 human 事后审计。

**6 个月后的 mastery**：human 不再是"写一份 PRD 然后被动等"，而是积累了一套**自己的项目史**——哪些 PRD 写法会导致漂移、哪些边界表述能显著减少返工、哪些"看起来聪明"的自动化其实制造幻觉、哪些人工裁决最值得保留。005 越用越像他自己的交付风格，而不是某个社区最佳实践的复制品。**这就是「用户级 calibration profile」**——它是 005 相对 addy osmani 已经做到的"项目级 AGENTS.md 自累积"的真正增量空间。

**百万人用了的世界**：变化不只是更多人能 vibe coding。更大的变化是**软件创造的门槛从"你是否有工程团队"转向"你是否能清楚表达目标 + 愿意接受纪律化澄清"**。研究者、设计师、运营者、小企业主把软件视为可迭代的工作资产而非一次性外包。会写好 PRD、能做范围取舍、能用准确验收语言的人变得比会写代码的人更值钱。005 的文化目标不是让人无脑自动化，是让**非工程操作者获得工程化表达的尊严和控制感**。

**反向定义同样关键**——R1 双方在 §0 都明确拒绝了几种诱人的替代读法：不是"永远比我懂的高级搭档"（违背 human 的"自动化优先"诉求）、不是"让 agent 替 human 写 PRD"（越界，PRD 是 human 责任区）、不是"对外卖工作流的产品"（模糊核心）、不是"四个旧项目合并版"（最终版流程本身就是陷阱）。**两边最一致的拒绝**：human-out-of-the-loop 不是 005 应该承诺的方向；可靠性来自清晰判断、边界控制和证据积累，不来自把人完全赶出流程。

---

## 2. Novelty assessment

**verdict：Novel slice（不新概念，新的切法）**

诚实地说：005 的概念层 novelty 接近零。Cursor / aider / claude-code / Devin / Sweep / addy osmani agent-skills / Superpowers——市场上"agent 写代码"的人很多。R2 检索证实，addy osmani 已经发布 20 skills + 7 commands + AGENTS.md 自累积机制 + how-to-write-good-spec 完整指南，是 production-grade 的工程纪律迁移方案。

**但有两个真实的、可被验证的市场空白**，正是 005 的差异化必须落在的地方：

1. **结构化 ambiguity-surfacing checkpoint**。arxiv 2502.13069（Stanford+CMU）直接证明 LLMs 默认 non-interactive、搞不清 underspecified vs well-specified；强制 interaction 后性能 +74%，但仍只达 full-spec 的 80%。Anthropic 公开承认正在训练 Claude 主动问 clarifying question——但**没人把"什么时候该问、什么时候该合理推断+暴露"做成产品级的结构化机制**。Devin 的失败模式正是"碰到 ambiguity 时硬推而不停下"。这是 005 真正的产品级 novelty。

2. **用户级长期 calibration profile**。addy 的 AGENTS.md 累积是**项目级**（per-codebase 的 lore）。GPT R1 强调的"个人工程风格画像"——跨项目记住"这个 human 的 PRD 盲点 / 范围偏好 / 决策延迟模式"——**addy 没走到这一步**。这是第二个真实空白。

005 真正的赌注：**在 (a) ambiguity policy + (b) 用户级 calibration 这两点上做对**。其他部分（spec-driven / TDD-gate / review-mandatory）全部承认站在 addy 的肩膀上、不重新发明。**不在这两点上的 effort 都是浪费**——这是 R2 双方收敛出的最重要的 design boundary。

---

## 3. Utility — 具体使用场景

**场景 A · 周末把脑子里的小工具变出来**
某周六下午，human 想做一个"自动整理我桌面截图、按内容打 tag 的 Mac 小工具"。他花 90 分钟写一份 PRD（功能清单、非功能要求、UI 草图），把它丢进管道，去做别的事。傍晚 6 点回来，桌面上有一个能跑的 dmg 包，附带 README、test report，以及最关键的一份"**我做了哪些超出 PRD 的判断**"清单（"你没说要支持 HEIC，我加了；你没说图标要不要点击有动效，我做了静态版本，TODO 标了"）。**他向朋友讲的是**："我写了 90 分钟需求，赚了一个工具。"——重点不是 AI，是**产出可信**。

**场景 B · 给 5 万行老项目加 SSO**
human 接手一个开源项目要加 SSO 登录。他写一份 PRD（要支持 Google/GitHub/SAML、要兼容老用户、要有迁移脚本），丢进管道。**这次的关键不是产出代码，是产出过程**——管道先输出一份"现有代码地图"（读了 codebase 后画的依赖图）、一份"风险评估"（"现有 session 系统在 7 个地方耦合 password 字段，建议 mock 出来分两阶段重构"）、一份"建议 PRD 改动"（"你说要兼容老用户，但没说密码迁移路径，请补充——我提供 3 个方案"）。**human 体会到的不是写代码省力，是「拿到了一个真懂这个 codebase 的资深工程师该有的产物」**。

**场景 C · 独立创业者从 demo 跨到产品**
一个独立创业者已经让 agent 做过几个 demo，但 demo 到正式产品之间总是散掉。她使用 005 后不再把 PRD 直接丢给模型期待奇迹，而是先得到一张关于范围、风险、验收、暂停条件的清晰地图。她可以决定哪些体验必须保留、哪些先不碰、哪些问题还不值得进入开发。完成的不是"看起来能跑"到"我知道为什么它可以继续"的心智转变。**她会说**："以前我是在催模型交东西，现在我是在管理一个会留下证据的交付过程。"

**场景 D · ML 研究员把研究脚本变成实验室内部工具**
一位 ML 博士想把实验室里反复使用的研究脚本变成小团队可用的内部工具。他能写清楚"谁用、用来做什么、成功是什么样"，但不确定开发过程该如何分阶段。005 帮他把 PRD 变成一组可被反复确认的交付承诺，并在每个关键点提醒他**只回答产品层面的选择**。完成的是从研究想法到可用软件的转化，**消失的是"我是不是漏了专业流程"的持续焦虑**。他对朋友说："它不是替我思考，是让我**只在真正需要我判断的地方思考**。"

**场景 E · 学习放大器（教学模式）**
human 让管道做一个 idea，但开了"教学模式"——管道每做一个非显然决策，会在 changelog 里多写一段"我这里在 trade-off X 和 Y，我选 X 因为...你以后想换 Y 的话改 Z 处"。半年后 human 回看自己 30 个项目的 changelog，发现自己**在没写过代码的情况下，建立了对工程权衡的真实直觉**。**他向朋友讲的是**："我没学会写代码，但我学会了软件工程的思考方式。"

---

## 4. Natural extensions（长尾的可能形态）

- **个人工程风格画像**（最有潜力的扩展）。当用户运行多个项目后，005 逐渐总结他的 PRD 盲点、范围偏好、验收松紧、决策延迟模式，让下一次探索更贴近他的真实习惯。这是把"用户级 calibration profile"从一个产品功能变成一个长期画像产品的自然路径。
- **项目类型手册族**。研究工具、内容产品、内部运营工具、面向消费者的小应用，虽然都从 PRD 出发，但需要的取舍语言不同。v0.1 成立后，用户会要求 005 识别项目气质、给出不同的澄清重点。
- **PRD-quality linter**（独立产品）。在 human 写 PRD 时实时反馈"你这条会让管道困惑、需要补 X"。是 005 的前置工具，可以单独使用。
- **多人轻协作**。单人操作者邀请一个设计朋友 / 一个领域专家 / 一个真实用户参与少数节点。005 成为他们之间的共同语言——参与者**只在自己有判断力的地方发声**，不被完整开发流程吞没。
- **管道自我演进环路**。每个项目结束后自动生成"这个项目我们犯了什么错、应该怎么改进 skills"，并把改进**自动 PR 回 skills 库**。autodev_pipe 已经有 phase-retrospective 雏形，005 把它从手动变成自动反馈环。**注意**：Microsoft ACE 提醒 brevity bias / context collapse 风险，自我演进资产必须可整理、可裁剪。

---

## 5. Natural limits（保护性围栏）

- **不是「自然语言一句话生成完整 app」**。那是 v0 prompt 工程的浪漫，市场已证伪。005 的核心前提是 PRD 是 human 写的且高质量。PRD 烂时 005 能 surface 烂的地方，不能替你想清楚。**护栏：管道在 PRD 不够清晰时必须停下来要 clarification，绝不靠 hallucinate 补全**。
- **不是「替 human 写 PRD 的工具」**。R1 §0(C) 已明确拒绝——human 自己说"我可以将需求描述清楚、可以构建较可靠的 PRD"，PRD 是他的责任区。把 PRD 也吃掉就是不尊重他的现有能力分工，且把不确定性堆在最危险的需求侧。
- **不是「为大型多人协作团队的开发系统」**。005 的天花板是"一个 human + N 个 agent"的单元生产力。多个这种单元之间怎么协作（governance / 冲突解决 / 责任归属）是另一个 idea 的领地。
- **不是「面向已有大团队 / 强监管行业的工具」**。如果一个公司已经有 50 人工程团队、自己的 CI/CD、自己的 code style，005 进去会冲突。005 的甜蜜带是"原本没有团队、但需要团队级产出"的个人或两三人创业。
- **不是「实时协作工具」**。Cursor 风格的 sub-100ms 同屏 ping-pong 是另一个产品族。005 是异步的——human 提交 PRD 后离开屏幕。两种协作模式从根上不同，混用会两边都做不好。
- **不是「万能 AI 工程公司」**。一旦 005 同时追项目管理、团队协作、代码生成、知识库、教育、外包，它的核心会变糊。最该守住的是：**帮一个会表达需求的人，以最少但最高价值的人类裁决，获得对自动化开发过程的可解释信心**。
- **文化/语言张力**：写 PRD/RFC/ADR 是西方工程文化产物；中文场景下"用文档驱动开发"的文化薄弱（更习惯口头沟通+不断改）。005 在中文母语用户里可能遇到"懒得写 PRD"的阻力——这是真实的、需要面对的张力。

---

## 6. Validation status

**双方共 10 次价值验证检索**。证据库异常丰富，verdict 一致。

### Prior art landscape

| 名称 | 状态 | 它做了什么 | 对 005 的启示 | URL |
|---|---|---|---|---|
| addy osmani agent-skills | production-grade | 20 skills + 7 commands + AGENTS.md 项目级自累积 + how-to-write-good-spec | 概念层全覆盖；005 必须诚实承认"概念 novelty 接近 0"，差异化只能在它没做的「**用户级** calibration」 | https://addyosmani.com/blog/agent-skills/ ; https://addyosmani.com/blog/self-improving-agents/ |
| Superpowers (Claude plugin) | production | brainstorming / TDD / debugging / subagent review 等纪律化流程 | 工程纪律工具集已成熟；005 不要再做一遍 | https://claude.com/plugins/superpowers |
| Devin (Cognition) | production，公开度高 | 端到端 autonomous coding agent | 反例参考——纯无人化路线 1.5 年后仍 1/3 PR 需大改 | （见下表） |
| Cursor / aider / claude-code | mainstream | human-in-the-loop 高频陪护 | 是 005 的"反向锚点"——005 是异步、低打扰，不抢这个生态位 | — |
| Anthropic measuring-agent-autonomy | research | 训练 Claude 主动问 clarifying question | 模型层方向同向；产品层"何时问、何时合理推断"仍是空白 | https://www.anthropic.com/research/measuring-agent-autonomy |
| Microsoft ACE | research | 上下文作为可演化 playbook 累积 | 抗重做方向有学术支持；同时警告 brevity bias / context collapse | https://www.microsoft.com/en-us/research/publication/agentic-context-engineering-evolving-contexts-for-self-improving-language-models/ |

### Demand signals

| 来源 | 信号 | 强度 | URL |
|---|---|---|---|
| Stack Overflow 2025 Developer Survey | 46% 不信任 AI 输出准确性、45% 抱怨调试 AI 代码耗时、77% 表示 vibe coding 不是专业工作的一部分 | **H**——直接证实"信任缺口"是市场主诉求 | https://stackoverflow.co/company/press/archive/stack-overflow-2025-developer-survey/ |
| The New Stack / arxiv 2505.19443 | "vibe coding fails when code moves from prototype to production"；产业共识转向 agentic engineering | **H**——005 是 2026 主流路径，不是逆潮流 | https://thenewstack.io/vibe-coding-agentic-engineering/ ; https://arxiv.org/html/2505.19443v1 |
| arxiv 2502.13069 (Stanford+CMU) | LLMs 默认 non-interactive；强制 interaction 后 +74% 性能（但仍只到 full-spec 的 80%） | **H**——直接证实 ambiguity policy 是真实研究空白 | https://arxiv.org/html/2502.13069v1 |
| arxiv 2603.26233 | uncertainty-aware multi-agent 在 underspecified SWE-bench 上 69.4% vs 标准 61.2% | **H**——ambiguity 处理是可验证能力，不是哲学问题 | https://arxiv.org/abs/2603.26233 |
| Amazon Q3 2025 90-day deployment freeze | 因 AI coding assistant 事故停止部署 90 天 | **M**——大公司侧的真实事故，反向印证可信赖路径的需求 | （见 The New Stack） |

### Failure cases

| 名称 | 状态 | 为什么死/失灵 | 对 005 的规避意义 | URL |
|---|---|---|---|---|
| Devin（无人化路线） | 仍在运营但口碑分裂 | Answer.AI 测得 15% 成功率；Cognition 自报 PR merge rate 34→67%（仍 1/3 需大改）；典型失败模式："碰到 ambiguity 时硬推而不停下" | **不能复制 Devin 的路径** —— 005 的 ambiguity policy 必须**结构上**不允许"硬推" | https://www.theregister.com/2025/01/23/ai_developer_devin_poor_reviews/ ; https://futurism.com/first-ai-software-engineer-devin-bungling-tasks ; https://agentmarketcap.ai/blog/2026/04/07/devin-67-percent-pr-merge-rate-autonomous-coding-agent-performance |
| METR RCT 2025（16 名资深开源开发者） | 真实任务 | 允许 AI 时**慢 19%**，但参与者主观仍以为加速；高质量项目的隐性要求放大验证负担 | **不能用主观顺滑感当可靠性指标**——005 必须有客观的"信任证据" | https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/ |
| human 自己的前 4 次尝试 | 全部 deprecate | idea_gamma2 / vibe-workflow / autodev_pipe / 当前 repo——每次都要从零搭脚手架，retro 沦为死档案 | **抗重做是硬约束**——005 v0.1 必须结构上能演化，不能要求 v0.1→v1.0 推倒重来 | （proposal 内部记录） |

### Net verdict

**Should this exist? Y-with-conditions**

理由：市场需求被 Stack Overflow 2025（46% 信任缺口）+ vibe→agentic 转向 + Devin 失败模式 + Amazon 真实事故四方证据强证实；学术界（arxiv 2502.13069、2603.26233）也证明 005 想攻的两个空白是真的研究空白。但**概念 novelty 接近零**——addy osmani agent-skills + Superpowers 已经把工程纪律迁移做完了。所以不是"该不该做"，是"**做之前必须接受的条件**"。

**条件（L3 必须把这些写成 PRD 硬约束）**：

1. **scope 必须收紧到两个 novelty 缺口**：(a) 结构化 ambiguity-surfacing checkpoint；(b) 用户级长期 calibration profile。其他工程纪律全部复用 addy osmani agent-skills，不重做。
2. **ambiguity policy 必须是产品核心语言，不是隐含行为**。"什么时候必须问、什么时候允许合理推断+暴露+TODO 标"必须在 L3 PRD 里枚举到决策类型粒度。
3. **必须 human-on-the-loop（不是 human-out-of-the-loop）**。"几乎没有人工干预"在 L3 必须重写为"几乎没有低价值人工陪护，但保留高杠杆裁决"。
4. **抗重做是结构约束**。v0.1 必须能演化到 v1.0，不能要求推倒重来；retro 资产必须是"可被自动调用的沉淀"，不是死档案。
5. **可信赖输出的硬标准必须在 L3 定义**。不能等 L4 再补——这是产品语言不是工程语言。

---

## 7. Open questions（L3 / 用户访谈必须回答）

| # | 问题 | 谁能答 | 为什么重要 |
|---|---|---|---|
| 1 | **ambiguity policy** 的具体形态是什么？每个 PRD 不清的点都要 human 拍板（自动化承诺破灭），还是允许"暴露+合理推断+TODO 标"？如果允许后者，**在哪些类型决策上允许、在哪些类型不允许**？ | L3 PRD + 用户访谈 | 这是 005 体验形状的**单点决定**——选错了就退化为 Devin 或 Cursor，没有差异化空间 |
| 2 | 在 human 自己的 4 次尝试里，**真正让你不满意的是产物质量、流程难复用、还是失败时不知道为什么失败**？| **只有 human 能答** | 决定可靠性的主指标和 005 的成功标准；L2 imagination 给不了答案 |
| 3 | "可信赖输出"的硬标准是什么？passing tests？coverage > 80%？code review pass？human 抽查 10%？METR 数据已经证明"主观顺滑感不可靠" | L3 PRD（产品决策） | 太低退化为 Devin，太高没人用得起 |
| 4 | "用户级 calibration profile" 是 v0.1 必含还是 v0.2 加？它需要 ≥5 个项目才有 signal——v0.1 必须包含吗？ | L3 scope 决定 | 直接决定 v0.1 的 ambition 边界 |
| 5 | 资源现实：human 能花多少时间在这个上？周末项目 vs 4 个月专注项目 → v0.1 scope 完全不同 | **只有 human 能答** | 是 L3 的硬约束输入 |
| 6 | "强需求表达者 + 弱工业交付直觉者" 这个画像在真实世界里**有多大群体**？是只服务 human 自己，还是一类人？| **必须用户访谈** | 决定 005 是 personal tool 还是 product；两者在 L3 之后路径完全不同 |
| 7 | 目标用户读 retro / changelog / decision log 的真实概率？如果他们不读、也没委托 agent 读，"用户级 calibration" 就是死档案 | **必须用户访谈** | 直接决定 §4 最有潜力的扩展是否成立 |

**强烈建议**：第 1、2、6、7 题里有 **3 道 L3 之前应该先做用户访谈**才能负责任作答（GPT R2 §6 + Opus R2 §6 都建议访谈 ≥5 位"会写 PRD 但没工程肌肉"的目标用户）。如果直接进 L3，scope 决定要靠 human 单方面 imagination——很可能产生 v0.1 ship 后才发现需要返工。

---

## 8. Decision menu（操作者来选）

### **[S] Scope this idea — 进入 L3（推荐路径之一）**

```
/scope-start 005
```

verdict 是 Y-with-conditions，且条件已经清晰到可以 scope。L3 会拉入 human 的真实约束（时间、预算、对前 4 次失败的真实复盘、用户群体定义）。**前提**：你在 L3 启动时心里要带着 §6 的 5 条 conditions，不能让它们在 L3 过程中变软。

### **[R] Re-explore with new input —— 用户访谈后再进 L3（推荐路径之二）**

如果你判断 §7 第 6、7 题的答案对 v0.1 scope 是决定性的（且你目前没有把握靠 imagination 答好），**正确做法是先做用户访谈再回 L3**，而不是直接 scope：

```
/explore-inject 005 "<访谈 5 位目标用户后总结的关键发现>"
/explore-next 005
```

L2R3 会把访谈数据变成更紧的 framing，再进 L3 时 scope 决策会扎实很多。**这条路径推荐给愿意多花 1–2 周做用户研究的你**——它能极大减少 L3/L4 返工。

### [F] Fork another L2 angle from 005

读完报告后如果你看到了一个更尖的切法（例如"我其实想做的是 PRD-quality linter 单点产品，不是完整管道"），可以另起一支：

```
/fork 005 from-L2 <new-angle> as 005a
```

### [B] Back to global view

```
/status 005
```

### [P] Park

```
/park 005
```

如果你看完报告后**对 §7 的开放问题感到压力**、需要时间想清楚，park 是体面的选择。所有 artifacts 保留，复活时不重做这一层。

### [A] Abandon

**不推荐**——verdict 是 Y-with-conditions 不是 N，证据基础充分，没有 abandon 的合理理由。

---

**操作者推荐**：在 [S] 和 [R] 之间二选一。如果你有把握自己作为唯一目标用户（"005 v0.1 就是给我自己用"），直接 [S]。如果你想让 005 有机会服务一类人而不是只服务你，**[R] + 用户访谈是更负责任的路径**。

---

## Fork log
（由 /fork 命令更新；目前无 sub-fork）
