# Idea 005 · L3R2 · GPT-5.5 xhigh

**Timestamp**: 2026-05-07T02:36:28Z
**Opponent's L3R1 read**: yes
**Searches run**: 4 scope-reality themes / 13 queries

## 1. What sharpened from Opus's L3R1

- Opus A 的强点是“单点 ambiguity map”比我的 Candidate A 更锋利：它把 v0.1 价值压到 PRD 进入开发前的一道安检，5-7 周可信。但我 push back：完全 stateless 会削弱 L2 的抗重做条件，至少要把用户裁决记录成未来可用的 calibration seed。
- Opus B 让我更确定 Web dashboard 不能做成全流程管道。范围搜索显示 observability/dashboard 赛道已经很密，005 若做 dashboard，必须避开性能、token、trace 红海，专注“单人操作者的产品裁决信心”。
- Opus C 直接把用户级 calibration day 1 做满，野心清楚；但它自己也承认赌“用户会回来读画像”。我的 C 更应保留“项目级信心日志”作为第一项目就有价值的入口，让 calibration 自动长出来，而不是先卖画像。
- Opus 的“calibration 何时入场”是关键轴；我会把它再压成更可拍板的一句话：**v0.1 到底先卖单次信心，还是先卖长期记忆**。

## 2. Scope-reality searches

| Candidate | Comparable product | What they include / shipped | What they cut or leave open | URL |
|---|---|---|---|---|
| A | GitHub Spec Kit | 已有 `/speckit.clarify`，明确推荐在计划前澄清 underspecified areas；模板要求标 `[NEEDS CLARIFICATION]`，不要猜。 | 它是 spec-driven workflow，不是给 Persona A/B 的独立 PRD 信心产品；没有用户级工程判断 calibration。 | https://github.com/github/spec-kit / https://github.com/github/spec-kit/blob/main/spec-driven.md |
| A | Keeborg PRD generator | 从 plain English 生成 AI-ready PRD，含 user stories、acceptance criteria、edge cases、dependencies。 | 它偏“代写/生成 PRD”，正撞 005 已确认红线；不是尊重用户已有 PRD 的 ambiguity policy。 | https://www.keeborg.com/generate/prd |
| B | Datadog LLM Observability | 提供 AI agent tracing、inputs/outputs、latency、token usage、errors、evaluations。 | 面向生产 LLM app 和工程团队，不回答“这个 PRD 哪些产品判断可交给 agent”。 | https://www.datadoghq.com/product/ai/llm-observability/ |
| B | Splunk AI Agent Monitoring | 监控 performance、quality、token usage；有 Agents page、service map。 | 企业 observability 语义很强，单人操作者的信心地图未被覆盖，但 dashboard 形态会被用户拿来类比。 | https://help.splunk.com/en/splunk-observability-cloud/observability-for-ai/splunk-ai-agent-monitoring |
| B | Maxim Agent Observability | 有 traces、online evaluations、human annotation、alerts。 | “human review”已存在，但服务对象是线上 agent 质量，不是 PRD→交付裁决。005 不能只做更小的 Maxim。 | https://www.getmaxim.ai/products/agent-observability |
| C | Mem0 | v1 语义是长期 memory layer，能存 user preferences、traits、action histories，并随互动更新。 | 证明 memory 空间真实，但它是通用 agent memory，不是工程判断画像；005 必须做领域化 calibration。 | https://mem0.ai/blog/introducing-mem0 |
| C | Personal AI | My AI 主张记住每次对话、学习偏好并随时间演化。 | 用户级记忆不新；差异化只在“PRD 盲点、裁决偏好、返工模式”这种工程化记忆。 | https://www.personal.ai/products |
| C | Rewind | launch 时做本地 searchable life/work memory，强调本地存储和搜索。 | 说明本地记忆产品的第一价值常是“可找回”，不是“画像”；005 C 应先做可回溯信心日志。 | https://techcrunch.com/2022/11/01/rewind-wants-to-revamp-how-you-remember-with-millions-from-a16z/ |
| A/B | GitHub Copilot coding agent | 异步做任务、开 PR、请求 review；session logs 和 PR review 让人回到 loop。 | 它服务代码任务流，不服务 PRD 入口的 ambiguity policy；也不积累用户级产品裁决偏好。 | https://docs.github.com/en/copilot/using-github-copilot/coding-agent/about-assigning-tasks-to-copilot |
| A/B | Cline | Plan/Act 分离，用户批准变更，透明、本地、非黑箱。 | 已覆盖“人批准每步变化”的开发陪跑；005 不该再做同步陪跑，而要做低打扰的裁决经济学。 | https://docs.cline.bot/getting-started/what-is-cline |
| B/C | Devin | 当前产品语义扩到工程团队、多 repo、PR、迁移、tribal knowledge。 | 进一步证明“万能 AI 工程师”方向会走向大团队/企业；005 应守住单人操作者。 | https://devin.ai/ |

Net read：A 的相邻竞品最危险，因为 Spec Kit 已经把 clarification 做进 workflow；B 的 dashboard 形态最容易误入 observability 红海；C 的 memory 概念最不新，但“个人工程裁决 calibration”仍有空白。

## 3. Refined candidates

### Candidate A · “PRD Clarifier + 信心报告”

v0.1 是 PRD 进入 agentic build 前的澄清入口：用户带自己写好的 PRD，得到 ambiguity map、必须裁决问题、允许推断清单和一页信心报告。Scope IN：PRD 歧义分类、三态裁决、报告导出、裁决记录作为 calibration seed。Scope OUT：不代写 PRD、不跑完整开发、不做 dashboard、不做成熟画像。成功标准：5 位 A/B 用户中 4 位认为它能阻止明显返工；一次预检 <=45 分钟。时间：**6-8 周**。风险：会被看成 Spec Kit clarify 的独立包装，所以必须把“用户裁决记录”和“信心报告”做得比普通 clarify 更产品化。

### Candidate B · “Solo Confidence Map”

v0.1 是可视化信心地图，但严格不做 LLM observability：它展示 PRD 经过澄清后的自动推进区、必须裁决区、推断审计区、暂停区，并把每个状态绑定用户下一步动作。Scope IN：项目级信心地图、高杠杆裁决队列、审计摘要、demo→产品化检查、薄层 calibration 提醒。Scope OUT：不做 token/trace/performance monitoring、不做团队 dashboard、不做实时协作。成功标准：用户 90 秒内说清“能继续什么、要裁决什么、为什么暂停”。时间：**9-12 周**。风险：polish 成本高，且 dashboard 市场语义会让用户误解成 observability。

### Candidate C · “Confidence Journal”

v0.1 是本地/个人项目日志：每个项目从 PRD、歧义、裁决、推断、暂停、复盘形成可回溯账本；跨 2-3 个项目后自动生成用户级 calibration。Scope IN：项目日志、裁决历史、复盘摘要、新项目启动时的历史提醒。Scope OUT：不监听一切、不做通用个人 memory、不要求用户先跑 5 个项目才有价值。成功标准：第一个项目能回溯关键裁决；第三个项目能提出 3 条历史相关提醒。时间：**9-13 周**。风险：长期价值强，但首项目价值必须足够硬，否则会像死档案。

## 4. The single biggest tradeoff axis human must decide

**核心拍板轴：v0.1 先卖“单次项目的可信推进感”，还是先卖“跨项目的个人工程判断记忆”。**

A/B 偏前者：更快得到用户反馈，也更贴近 demo→产品化焦虑；但 calibration 只能薄做。C 偏后者：更符合 L2 的长期差异化和抗重做，但用户行为假设更重，回报更慢。我的建议是 synthesizer 不要把 A 和 C 对立成“短期 vs 长期”，而是判断：A 是否要强制留下 calibration seed；B 是否是 A 的可视化层；C 是否应作为 v0.2 路线而非 v0.1 主承诺。

## 5. What I'm less sure about now than in R1

- 我比 R1 更担心 Candidate A 的差异化，因为 Spec Kit 已经公开把 clarification 作为正式步骤；A 必须产品化“裁决经济学”，不能只是 PRD lint。
- 我比 R1 更不愿推荐完整 Web dashboard。Datadog/Splunk/Maxim 证明 dashboard 语义已经被 observability 占据，005 的 B 必须非常克制。
- 我仍认为我的 C 方向比 Opus C 更稳，但现在更确信 C 不该以“画像”为第一屏。第一屏应是“这个项目为什么可信/不可信”的日志，画像只是随使用浮现。
