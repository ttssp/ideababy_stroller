# Idea 004 · L3R2 · GPT-5.4 xhigh · Scope (cross + scope-reality search)

**Timestamp**: 2026-04-24T21:59:10+08:00
**Opponent's L3R1 + L3R2 read**: yes
**Searches run**: 5 组 scope-reality queries（AI research terminal / hybrid advice / Chinese paid combo / event research / AI stock intelligence）
**Inputs read**: L3R0 intake（含 🧭 原则）, L2 report, Opus L3R1, Opus L3R2, my L3R1, scope-protocol

## 1. From opponent's L3R1 + L3R2 — what sharpened my thinking

Opus 本轮最有价值的推进有三点。第一，他把我在 R1 里提出的“平台主次 + 记录深度”真的吃进 refined candidates，说明 A/B/C 不该只在 shell 宽度上变化，这让我确认候选必须更明确地区分“研究入口”与“决策入口”。第二，他对 Candidate C 的修正是对的：如果事件数据层大量借公共源，C 的成本比 R1 想象低，不再天然超时。第三，他给 B 加了一个很诚实的 `B-lite` 退路，这个动作本身说明他也意识到 log-heavy 壳的真正风险不是功能不对，而是 upkeep 过重。

我对 Opus 的 refined candidates 整体评价是：**候选本身已经够强，但他的 §4 axis 仍然偏“第二层决定”**。我不同意把最大 tradeoff 定义成“周报 / 动手前 / event 前，哪个 calibration 场景是 primary”。在做这个选择前，human 先要决定一件更根本的事：**v0.1 是先做一个更会看市场的壳，还是先做一个更能约束自己的壳**。

## 2. Scope-reality search results

| Claim | Source | What I searched | What I found | Verdict |
|---|---|---|---|---|
| AI 投研终端的 starter scope 主要是 watchlist / dashboard / transcripts / alerts，不是个人决策留痕 | [Fiscal.ai 首页](https://fiscal.ai/) · [Fiscal.ai Pricing](https://fiscal.ai/pricing/) · [Koyfin Pricing](https://www.koyfin.com/pricing/) | "AI investing assistant pricing", "stock research terminal starter tier" | 截至 2026-04-24，Fiscal.ai 的 Free/Pro 主打 dashboards、notifications、portfolio stats、AI summaries、IR content、earnings calendar；Koyfin Free/Plus 主打 portfolios、watchlists、dashboards、screener、transcripts。 | **A/C 不该靠“再多一点 generic research 功能”取胜。** 这层已经很拥挤；真正空白更像 B 的个人决策壳。 |
| Event-first 产品把价值定义成“更快研究”，不是“更好 pre-commit” | [Aiera Platform](https://aiera.com/platform/) · [Aiera Dashboard](https://aiera.com/integrations/dashboards-mobile-app/) | "earnings research assistant alerts transcripts watchlists" | Aiera 的核心是 live events、实时转录、AI 摘要、搜索告警、watchlists、plug-and-play dashboard；产品语言一直是 research speed / compliance / monitoring。 | **C 若成立，必须非常窄。** 只做“事件→持仓→建议/不建议→事后记录”，不要长成完整事件研究台。 |
| Hybrid advice 的 baseline 是 questionnaire→portfolio→auto-rebalance→advisor/planning，不是 ticker-level conflict report | [Schwab Intelligent Portfolios](https://www.schwab.com/intelligent-portfolios) · [Vanguard PAS 说明](https://corporate.vanguard.com/content/corporatesite/us/en/corp/who-we-are/pressroom/Press-Release-Advice-Improves-Portfolio-Diversification-For-9-In-10-Investors-02112020.html/1000) | "hybrid advice official features questionnaire auto rebalance advisor" | Schwab 官方把短问卷、目标、分散化 ETF 组合、自动再平衡放在前面；Vanguard 对 PAS 的官方描述也是 personalized plan、ongoing rebalancing、tax-efficient management、advisor relationship。 | **不要把 v0.1 做成 mini robo-advisor。** 可借的是低频节奏和 behavioral coaching，不是全套规划壳。 |
| 华语付费组合层卖的是持仓/调仓可见性与跟单便利，不是 personalized reasoning | [雪球购买协议](https://xueqiu.com/law/buycube) · [雪球 FAQ/组合](https://xueqiu.com/about/faq/4/0) | "雪球 付费组合 功能 官方", "中国 投资组合 持仓提醒 官方" | 雪球付费核心是详细仓位、净值、收益走势、历史调仓记录与提醒；FAQ 进一步显示它支持组合调仓、仓位分析、以及一篮子下单。且官方明确：主理人的额外报告/群聊不属于核心服务。 | **这强化了一个判断**：`咨询师内容/组合观点 → 你的持仓映射` 并不稀缺；稀缺的是“把你自己的决定与结果沉淀下来”。 |
| AI 股票智能产品现在比的是覆盖广度与推荐可解释性，不是自我校准闭环 | [Bridgewise StockWise](https://bridgewise.com/stockwise/) | "AI stock intelligence official multilingual recommendation" | StockWise 直接主打 global coverage、multilingual recommendations、buy/sell recommendations、news/transcript/earnings summaries。 | **v0.1 不该在“覆盖更多标的/更多信号”上求胜。** 这条赛道现成供给很多，human 真缺的是 personal shell。 |

## 3. Refined candidates

### Refined A · "研究收件箱"

**Essence**: 周报与咨询师 PDF/文本导入后，系统把观点映射到你的关注股与当前持仓，输出一份 Telegram-first 的周报收件箱；Web 只做错位矩阵、历史周报和术语笔记查看。  
**Persona**: 你的主要痛点是“我其实有内容，但没法快速落到自己的组合”。  
**Stories**: 每周 1 次把外部观点转成自己可读的组合视图；在 Telegram 里得到 `做 / 不做 / watch`；第一次出现的新术语被白话解释并存档。  
**IN**: PDF/文本导入、结构化摘要、关注股/持仓映射、错位矩阵、轻量冲突卡、笔记 wiki。  
**OUT**: 深度决策档案、完整事件值班台、自动抓取、音视频实解析。  
**Success / Time / UX / Risk**: 3-4 周；连续 4 周收件箱闭环；Telegram 五条消息内看完重点；最大风险是它会变成“更好的研究终端”，而不是“更好的决策系统”。  

### Refined B · "决策账本"

**Essence**: Web-first。周报和 event 卡都只是入口，真正的核心是把每次 `动 / 不动 / 等待` 都记成一条决策账本：咨询师观点、占位模型、agent 综合、分歧根因、human 最终决定、1 行理由、事后结果。  
**Persona**: 你真正想解决的是“我在压力里不稳定”，不是“我没看到足够多信息”。  
**Stories**: 动手前先过一次冲突报告；`不动` 是正式输出；周度/月度回看看到自己究竟在哪些情境最容易乱动。  
**IN**: 决策档案、冲突报告、轻量 devil's advocate、周/月 review、术语学习记录。  
**OUT**: 广谱 research terminal、全市场事件覆盖、私有模型深实现、自动执行。  
**Success / Time / UX / Risk**: 5-6 周；8 周内 ≥15 条账本、≥3 次 agent 阻止冲动动作；单次录入必须 <30 秒；最大风险是 upkeep 负担，如果录入不像“福利”而像“作业”，它会死得最快。  

### Refined C · "事件卡台"

**Essence**: 周报保留，但第一性体验变成重大事件前后的准备卡。系统只盯与你持仓相关的财报/FOMC/重大异动，在 event 前给一张卡，event 后补一张回看卡。  
**Persona**: 你平时不焦虑，但一到关键事件窗最容易被情绪带偏。  
**Stories**: event 前 24h 看见受影响持仓、三路分歧和建议的不动作；event 后把结果自动挂回时间线。  
**IN**: 事件卡、受影响持仓映射、轻量时间线、事前/事后记录。  
**OUT**: 完整事件研究台、全量宏观日历、深度决策账本、日常高频提醒。  
**Success / Time / UX / Risk**: 4-5 周；build 窗口内覆盖 2-4 次真实 event；通知严格维持“每周 + event”；最大风险是样本稀疏，做对了也可能暂时证据不厚。  

## 4. The single biggest tradeoff human must decide

我**不同意** Opus 把最大 axis 定义成“哪种 calibration 场景最优先”。更基本的 axis 是：

**`信息壳` vs `承诺壳`**

- **信息壳**: 先把外部观点、事件、研究材料更好地映射到你的组合里，减少“看了但没落地”。Refined A/C 更靠这边。
- **承诺壳**: 先把你每次动作前后的理由、分歧与结果沉淀下来，减少“其实知道很多，但临场还是乱动”。Refined B 更靠这边。

我这样判断不是抽象偏好，而是 search 直接推出来的：研究终端、事件研究、hybrid advice、华语付费组合、AI stock intelligence 这些现成产品，几乎都已经把“更多信息、更快摘要、更多提醒、更多推荐”做得很充分了；**它们共同缺的，是一个把 `你自己的决定` 当核心对象的 personal shell**。所以“周报 vs event vs 动手前”是第二层；第一层是 **你到底缺的是更多可见性，还是更强的自我约束**。

如果 human 回看最近两个月，最常见的遗憾是“明明看过咨询师内容，却没转成组合动作”，选 A。若最常见的遗憾是“知道很多，但还是在焦虑里乱动”，选 B。若最常见的遗憾集中在财报/FOMC 这些窗口，选 C。

## 5. What I'm less sure about now than in R1

第一，我在 R1 里偏向把 B 当默认优选；现在我仍认为 B 最有独特性，但没有 `录入 <30 秒` 这个 UX 前提，B 不成立。第二，我之前低估了 C 的可行性；event 数据层比我想象更现成，所以 C 现在是真候选，不再只是“想法对但超时”。第三，我对 A 的看法变复杂了：它不是最独特的壳，但如果 human 的真实痛点只是“外部观点落不到自己的 30-50 只股票上”，A 反而是最诚实的 v0.1。
