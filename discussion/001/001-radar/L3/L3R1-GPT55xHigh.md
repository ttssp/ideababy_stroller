# Idea 001-radar · L3R1 · GPT-5.5 xhigh · Scope (no search)

**Timestamp**: 2026-07-06T17:44:18Z
**Inputs read**: proposals/proposals.md, L2 report, L3R0 intake, scope-protocol skill, AGENTS.md
**Searches used**: NONE in this round
**Visibility**: did NOT read the other debater's L3R1 content

## 0. How I read the intake

我读到的 v0.1 不是“研究论文阅读器”，也不是“漂亮知识图谱”，而是给 operator 这个 AI lab 负责人用的**新方向冷启动评估器**：输入一个还没进入常设 topic 列表的新方向，尽快判断它结构上是否已经成型、是否值得投入。硬约束是 2-3 个月、每周 15-30 小时、单人版、8-15 topic 目标、briefing 为主、diff/图只做证据层、不追全覆盖。真正的 scope 张力是：冷启动深度、8-15 覆盖、位移 diff 完整度三者不能同时拉满。下面三个候选是同级切法，不是主方案加备选。

## 1. Candidate A · “深冷启动裁判”

### v0.1 in one paragraph

v0.1 专注一次一个新方向的高质量冷启动评估。用户给出方向名、1-3 个种子 work 或一段直觉，系统产出一份可核验 briefing：这个方向是否形成稳定问题簇、方法簇、代表性路线和关键争议；结论明确分为“可投 / 观察 / 暂缓”，并附上证据展开。它承认 8-15 topic 在本切法里不是同时常驻覆盖，而是 2-3 个月内完成 4-6 次深冷启动，沉淀为未来 topic 组合的候选入口。

### User persona

一位 AI lab 负责人，正在判断“agent evaluation / long-horizon memory / scalable oversight”这类新方向是否值得拉一名学生或小队投入。

### Core user stories

- 作为 lab lead，我可以输入一个新方向和少量线索，获得一份结构成型度判断，避免只凭热度下注。
- 作为 lab lead，我可以看到该方向的核心问题簇、方法簇和代表 work，判断它是短期噪声还是研究对象。
- 作为 lab lead，我可以展开每条判断背后的证据，知道结论哪里确定、哪里只是推断。
- 作为 lab lead，我可以把冷启动结果保存为候选 topic，供之后继续跟踪。

### Scope IN

- 新方向 briefing：一句判断、三到五条理由、证据展开。
- 结构成型度：问题簇、方法簇、争议点、代表 work、空白区。
- 冷启动后的 topic 候选库：记录“为什么当时判可投/观察/暂缓”。
- 信任层：每条关键判断带置信度、证据来源摘要、待人工确认项。

### Scope OUT

- 不承诺 8-15 个 topic 同时活跃监控；这是深度换广度。
- 不做每日 feed，不按“今天新增论文”组织体验。
- 不做开放式问答/长报告生成器；briefing 只服务方向评估。

### Success looks like

- operator 能在 30 分钟内完成一次新方向初判。
- 至少 3 次冷启动结果能在之后人工复核时被认为“抓住了结构而非只列论文”。
- 每份 briefing 的关键判断都能追溯到可检查证据。

### Honest time estimate under human's constraint

8-10 周，约 160-260 小时。信心 M。它能落在预算内，但代价是 v0.1 不完成 8-15 topic 的完整组合覆盖。

### UX principles

- 判断先行，证据随后；不要让用户先读图。
- 宁可少做几次深评估，也不要给很多浅结论。
- 不确定性外显，不把 agent 判断包装成事实。

### Biggest risk to this cut

最大风险是它违背 operator 对 8-15 topic 的完整覆盖期待。这个切法最适合验证“冷启动方向评估是否真有价值”，但不是完整 radar。

## 2. Candidate B · “8-15 组合盘点”

### v0.1 in one paragraph

v0.1 直接围绕 operator 的 8-15 个关注 topic 建一个单人研究组合视图。每个 topic 都有轻量 briefing：当前结构、最近值得注意的位移、尚未成型的新分支、可投/观察/暂缓信号。冷启动仍是一等动作，但它的目标是把新方向快速放入这套组合坐标里，而不是对单个方向做最深审判。

### User persona

同一位 lab 负责人，但当前痛点是“我管的方向太多，需要一张每周/每月能扫过的研究组合盘”。

### Core user stories

- 作为 lab lead，我可以维护 8-15 个 topic 的当前状态，知道哪些方向需要复盘。
- 作为 lab lead，我可以把一个新方向冷启动后放进组合盘，与现有 topic 比较投入优先级。
- 作为 lab lead，我可以看到每个 topic 的简短判断，而不是被迫打开十几张复杂图。
- 作为 lab lead，我可以标记 agent 判断是否符合我的 taste，让下一轮更贴近我的标准。

### Scope IN

- 8-15 topic 的轻量状态卡：结论、理由、关键变化、下一步建议。
- 新方向冷启动入口：输出较短 briefing，并建议是否纳入组合。
- 组合层优先级视图：哪些 topic 值得投、观察、降级。
- 最小信任机制：人工确认/反驳关键判断，保留理由。

### Scope OUT

- 不对每个 topic 做深度 claim 级地图。
- 不追全 arxiv，不做泛领域覆盖。
- 不做 lab 共享协作；只服务 operator 的私人判断外骨骼。

### Success looks like

- operator 能在一次固定复盘中扫过 8-15 个 topic，并挑出 2-3 个需要行动的方向。
- 新方向能被明确放入“纳入/观察/不纳入”之一。
- 至少 70% 的 topic 状态卡被 operator 认为“足够支持下一步判断”。

### Honest time estimate under human's constraint

10-12 周，约 260-360 小时。信心 L-M。它勉强贴住预算上沿；若每周低于 25 小时，质量会明显牺牲。

### UX principles

- 广度优先，但每个结论必须可追溯。
- 状态卡比全图重要；图/diff 是核验层。
- 允许不同 topic 深浅不一，明示覆盖质量。

### Biggest risk to this cut

最大风险是“广而浅”：为了满足 8-15 topic，briefing 可能退化成摘要卡，无法产生 L2 期待的结构位移洞察。

## 3. Candidate C · “位移证据优先”

### v0.1 in one paragraph

v0.1 把冷启动和位移的矛盾裁成：新方向没有用户旧地图，但可以重建该方向在公开研究脉络中的前后快照。每次冷启动不是只问“现在是什么”，而是问“过去一段时间它如何从热词变成结构，或为什么没有变成结构”。briefing 仍是首屏，但最核心证据是时间切片 diff。

### User persona

一位已经对某个新方向有兴趣、但担心被短期 hype 误导的 research lead，需要判断“这个方向是否正在形成可下注的结构性趋势”。

### Core user stories

- 作为 lab lead，我可以看到新方向在两个时间切片中的结构变化，而不是只看当前热度。
- 作为 lab lead，我可以判断新 work 是分散爆发，还是正在形成稳定问题簇和方法簇。
- 作为 lab lead，我可以把 diff 中的关键变化带进开题/组会讨论。
- 作为 lab lead，我可以保留一版基线，供之后判断 agent 当初是否看对。

### Scope IN

- 冷启动 briefing：结构成型度 + 是否值得投入。
- 前后快照 diff：问题簇、方法簇、中心 work、争议点的变化。
- “为什么不是 hype”的证据清单。
- 基线保存：后续复核当初判断。

### Scope OUT

- v0.1 不追求 8-15 topic 全量覆盖；优先 3-5 个高价值冷启动案例。
- 不做实时 alert；没有基线前不推送。
- 不做完整 survey；只产出方向决策需要的证据。

### Success looks like

- operator 能用 diff 解释一个方向“正在成型/尚未成型”的原因。
- 至少 3 个案例保留基线，并能在 30-60 天后复核判断质量。
- briefing 中的主结论和 diff 证据一致，不靠空泛判断支撑。

### Honest time estimate under human's constraint

9-11 周，约 210-320 小时。信心 M。它牺牲 topic 广度，但最正面保留原 idea 的“位移”差异化。

### UX principles

- diff 是证据，不是主界面；用户先读判断，再查变化。
- 时间感必须服务决策：哪里变了、为什么重要、该不该投。
- 不做没有可复核基线的强提醒。

### Biggest risk to this cut

最大风险是冷启动速度变慢。为了产出可信 diff，它比 Candidate A 更重，可能不适合需要当天快速拍板的场景。

## 4. Options for the human's ❓ items

- 商业模式：Option 1 自用工具，scope 最干净，不做商业包装；Option 2 免费自用/开源雏形，保留可分享 artifact；Option 3 小 SaaS 以后再想，v0.1 不应被它牵引。
- 平台形态：Option 1 terminal/agent 工作流，适合 operator 自用和批处理；Option 2 web 工作台，适合 briefing、证据展开和组合盘；Option 3 artifact-first，每次产出可保存的方向 dossier，界面先弱化。
- 优先级排序：若要验证价值，选 A；若要满足 8-15 覆盖，选 B；若要守住“位移”差异化，选 C。
- 冷启动 vs 位移：A 裁为冷启动主、位移弱；B 裁为组合覆盖主、位移轻量；C 裁为冷启动必须带公开脉络 diff。
- map-region alert：我建议 v0.1 默认不做；只有 B 可允许“人工订阅的高阈值区域提醒”作为例外，且不形成每日 feed。
- 信任机制：最低限度要有证据展开、置信度、人工确认/反驳、基线复核。没有这些，briefing 的强判断会消耗信任。

## 5. Red lines

1. 确认硬红线：不追全覆盖。选择性中心度是价值，不是限制。
2. 修订：不做“开放式问答/报告生成器”，但允许方向评估 briefing；briefing 必须有明确决策语境。
3. 修订：不做每日简报/feed；map-region alert 只能作为人工订阅、高阈值、非日更的例外。
4. 确认：不做真理机。所有 contradicts/supersedes/成型度判断都要外显不确定性。
5. 确认：不面向领域新人；v0.1 服务有判断责任的人。
6. 补提：不做 lab 共享版，不做团队权限、评论流、协作工作台。

## 6. Questions needing real user interviews

- 除 operator 外的 lab lead 会更信“强结论 briefing”还是“证据先行 dossier”？
- 他们愿意为一次新方向冷启动等待多久，30 分钟、半天、还是一两天？
- 什么样的错判会让他们立刻弃用：漏掉关键 work、错判路线关系，还是过度自信？
- 8-15 topic 对其他 lab lead 是常态需求，还是 operator 的个人覆盖面更宽？
- alert 的容忍线在哪里：只要高价值变化就欢迎，还是任何 push 都会让产品退化成噪声？

