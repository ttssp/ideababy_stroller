# L3 Scope Menu · 001-radar · "Paper Radar：给 AI lab 负责人的新方向评估器"

**Generated**: 2026-07-07
**Source**: L2 report 001-radar + L3R0 intake
**Rounds completed**: L3R1（Opus + GPT，双方）、L3R2（Opus + GPT，双方）
**Searches run**: 19 次 scope-reality 查询（Claude R2 · 4 + GPT R2 · 15）
**Moderator injections honored**: none（本 L3 未注入 moderator note）

## How to read this menu

这是 L3 对 001-radar 的输出：两份候选 PRD。每一份都是**同级 peer** —— 在你 intake 里
写死的约束下，对同一个想法的一种合法切法。你将 fork 其中一份（或多份）进入 PRD 分支跑 L4：

    /fork 001-radar from-L3 candidate-A as 001-radar-pA

fork 之后运行 `/plan-start 001-radar-pA` 开始 L4（HANDOFF → XenoDev build runtime）。

**本菜单只有两个候选**，不是三个。原因见下方「落选记录」——纯 Radar-first / 8-15 组合盘点
被双方 R2 独立判死（超预算 + 首月无价值时刻 + 冷启动仪式被边缘化），不作为 peer，只留证据。

## Intake recap — 我们honored了什么

### 硬约束（✅）—— 两个候选全部遵守
- **时间盒 2-3 月 · 周工时 15-30h · 预算约 130-360h**（两候选都落在盒内，A 有余量、B 贴上沿）
- **目标用户 = AI lab 负责人 / research lead（operator 本人）** · 非泛 researcher · 非领域新人
- **决策仪式 = 开新方向评估（冷启动）** —— v0.1 核心动作，两候选的入口动作都是它
- **payload = briefing 为主（判断+证据）+ diff/图作可展开证据层**，非"以图为主"
- **规模 = 8-15 topic + 单人版**（见下 ❓ 处理：8-15 被诚实重定为轨迹终点，非 v0.1 硬交付）
- **不追全覆盖**（选择性中心度是价值 · L2 natural limit）

### 软偏好（🤔）
- 隐含优先级：**差异化 > 广度**（红线"不追全覆盖" + L2 护城河脆弱性）
- **可验证性高**（operator 自用 · 冷启动评估的判断准不准是核心）
- 8-15 topic 是 operator 期望值，但与预算有张力 → 允许分期，显式列 tradeoff（下方矩阵）

### 红线 —— 任何候选都不许违背
- ✅ **硬红线**：不追全覆盖（operator 明确定）
- 双方 R1/R2 收敛补提（两候选全遵守）：
  - **不做问答 / 报告生成器**（briefing 限定为"结构成型度 / 是否下注"一种文体，避开 Elicit / Undermind / OpenScholar 的 synthesis 面）
  - **不做 push / 每日 feed**（一切信息 pull 时呈现；B 的"显著位移置顶"是 pull 内排序，非通知）
  - **不做真理机 / 无证据判断**（每个论断可展开到原文，做不到就标低置信，宁缺不装）
  - **不面向领域新人**（位移 / 成型度判断的前提是用户已有领域判断力）
  - **不做 lab 共享 / 团队协作**（单人版 · 私人判断外骨骼）

### ❓ items —— 本菜单如何决定

| ❓ item | Candidate A 处理 | Candidate B 处理 |
|---|---|---|
| 商业模式 | 自用起步（无账号 / 无计费，scope 最小） | 同 A |
| 平台形态 | 产品级选项：v0.1 CLI/terminal 出 markdown briefing → v0.2 本地 Web 视图（证据展开更完整）。技术留 L4 | 同 A（组合盘的展示面更受益于 Web，可提前到 v0.1，见风险） |
| 冷启动 vs 位移主次 | **公开脉络重建裁法**：冷启动时 agent 重建该方向的公开研究脉络（2-3 历史切片），位移内嵌在单次评估内 —— 张力消解，位移当场兑现 | 同 A 的公开脉络 + 额外的"自建基线积累"位移（留驻后回访 diff） |
| map-region alert | v0.1 一律 OUT | 唯一最小例外：留驻 topic 有显著位移时，下次打开置顶提示（pull 内排序，非 push） |
| 信任建立机制 | 三件全要：证据链强制（3 击到原文）+ 评估 journal（后验复核）+ 盲测校准（拿已深耕方向测 briefing） | 同 A + journal 天然扩展为"当初判断 → 后验证实"的回访对照 |

### ❓ items 仍对 operator 开放（菜单无法替你决定）
- **延迟预算是否分快慢两档**：市场证据说 5-30 分钟出带溯源报告已被驯化（Deep Research 类），
  30 分钟初判现实；但"学生开题当场讨论"场景可能需要一个更快的档。v0.1 要不要内建快慢两档，
  需要 operator 自用数据说话 —— 建议 v0.1 先单档，用起来后再定。
- **briefing 的"结构成型度"结论词表的最终形态**：候选借了 ThoughtWorks Tech Radar 四环词表
  （投入 / 试点 / 观察 / 暂缓），但研究者第一眼信任哪套词、分几级，需要拿真产出物给 3-5 个
  同行看反应 —— v0.1 中后期可用非正式验证，不阻塞开工。

> 上面两条菜单答不了。它们进入所选 PRD 的"open questions for L4 / for moderator"。
> 好消息：两条都不是 scope 的骨架决定，可以边用边定，不会引发大返工。

## The key tradeoff axis

**位移的来源 / v0.1 是工具还是系统。** 两侧 R2 §4 独立收敛到同一根轴：位移从哪里来？
A（方向评估官）用**公开脉络重建** —— 每次评估当场重建该方向过去 12-18 个月的结构变迁，
位移在单次评估内兑现，v0.1 是一把**每次用完即完整的工具**，价值第一天到手、零维护负担、
盒内有余量；但 3 个月末你手里是一叠评估档案，不是一张"活的雷达"。B（评估→留驻漏斗）在 A 之上
加**自建基线积累** —— 评估完可留驻，留驻 topic 攒快照，回访给"自基线以来位移"，v0.1 是一个
**越用越厚的系统**，朝原始梦想（8-15 张活地图）迈出真实一步；但要背上留驻机制的成本和
"组合盘会不会没人回访"的 dashboard-失败风险。GPT 的等价问法：v0.1 先证明一个**高信任方向判断**
（A），还是先兑现**组合覆盖承诺**（B 用留驻把 8-15 变成使用轨迹）。intake 的仪式选择（冷启动评估）
+ Connected Papers / Undermind 的窄切先例都指向 A；operator 对"8-15 覆盖"的期望指向 B。这是要拍的板。

---

## Candidate PRDs

### Candidate A · "方向评估官（历史位移内嵌）"

**Suggested fork id**: `001-radar-pA`
**Sources**: Claude R1-A 骨架 + GPT R1-C 公开脉络 diff + GPT B 的 taste 反馈 story + Tech Radar 词表；双方 R2 均把它列为最稳的验证 cut

**v0.1 essence**:
一个**按需出动**的研究方向评估 agent。你给它一个方向（一句描述或 2-3 篇种子 paper），它冷启动
重建该方向的公开研究脉络（含 2-3 个历史时间切片），然后交给你一份**强观点评估 briefing**：这方向
结构上成没成型（分散爆发 vs 稳定问题簇+方法簇互连）、核心 claim 是什么、"它如何从热词变成结构
（或为什么没有）"的历史位移证据、结论明确落在投入 / 试点 / 观察 / 暂缓，每条判断 3 击内到原文。
评估留档进 journal 供后验复核。它**不常驻、不推送、不做组合盘** —— 你评估哪个方向，哪个方向的
地图才存在，用完即完整。

**User persona**（具体）:
operator 本人 —— AI lab 负责人，每月 1-3 次面临"这个还没进我 topic 列表的新方向值不值得投一个
学生 / 一小队"的决策，现状靠 X 碎片 + 走廊直觉 + 心里那一丝"我脑中这张地图还是现在的地形吗"的
不确定，想要"结构上是否成形"的可核验判断。

**Core user stories**（3-5）:
- 作为 lab lead，我能给出一个方向名 / 种子 paper，在一次咖啡的时间尺度内拿到冷启动评估 briefing，让"回去想想一周"变成"当场有据讨论"。
- 作为 lab lead，我能看到该方向过去 12-18 个月的结构位移（公开脉络重建），判断它在成型还是退潮 —— 而不只看当前热度。
- 作为 lab lead，我能点开 briefing 里任何一个判断，看到支撑它的节点 / 边 / 原文出处，自己核验 agent 有没有胡说。
- 作为 lab lead，我能把评估结论（投 / 观望 / 不投 + 日期 + 理由）留档进 journal，三个月后回看当时判断对不对。
- 作为 lab lead，我能标记 agent 的判断是否符合我的 taste，让下一轮评估更贴近我的标准。

**Scope IN（v0.1）**:
- 冷启动 pipeline：方向输入 → 检索收集 → 方法 / claim 级图构建（单方向、量级小）+ 2-3 历史时间切片重建
- 结构成型度 briefing（判断 + 历史位移证据链，可展开）· 结论词表借 radar 环
- 证据链强制（每条判断 3 击内到原文）+ 低置信标注
- 评估 journal（后验复核）+ taste 反馈标记
- 3-5 次真实评估跑通（operator 自用验证）

**Scope OUT（explicit non-goals）**:
- **常驻 8-15 topic 持续跟进 / 留驻 / re-scan / 组合盘** —— 这是 B 的事；A 里 topic 地图是评估副产物，不做后台持续 ingest
- **watch / re-scan** —— 是 v0.2 扩展位（Undermind 把 watch 做成后加功能且没伤采用）
- 跨 topic 视图、方法迁移检测、区域 alert、任何 push
- 问答 / 报告生成器、全覆盖、lab 共享

**Success observable**:
- 3 个月内完成 ≥5 次真实新方向评估，其中 ≥1 次实际改变了 operator 的投入决策
- 任一 briefing 的任一判断都能在 3 次点击内到达原文证据
- **30 分钟内出初判**（把评估延迟当产品属性钉住）
- 对已深耕方向做盲测评估，briefing 判断与 operator 自己的判断一致，或给出他认可的新信息（信任校准）
- journal ≥1 条"当时 briefing 判断 → 后验证实"记录（信任第一块砖）

**Time estimate under your constraints**:
- 给定你的 intake（15-30h / 周，2-3 月）：约 **9-11 周 @20h（180-220h）**，**盒内有余量**。
- Confidence: **M+**。若下调：冷启动检索 + 图构建质量是主要不确定源，但单方向、量级小，风险可控。

**UX priorities**（tradeoff 立场）:
- 判断先行，证据随取；宁可 briefing 观点强 + 标不确定度，不做四平八稳综述
- 单次评估体验 > 长期库完整性；不为未来的常驻功能预留 UI 复杂度
- 宁可少做几次深评估，也不给很多浅结论

**Biggest risk**:
与 Deep Research 类通用工具的差异化，全押在**结构成型度框架 + 方法级图证据 + taste 校准**这三样的
交集上。如果 briefing 读起来像 Gemini Deep Research 生成的一份带溯源报告，产品就没了独占空间 ——
这是产品级 / 差异化风险，不是技术风险。缓解靠"结构成型度"这个独有判断文体 + 位移叙事 + 品味校准，
而不是靠把检索做得更全。

**Scope-reality verdict**:
- 同类产品 v0.1 通常包含：发现、保存、图、报告、提醒、引用透明（Litmaps / ResearchRabbit / Elicit / Undermind 的主面）
- 这个候选相对 norm 砍掉：持续监控、library、team、billing、全覆盖 —— 收束到"新方向是否成型、是否下注"的窄仪式
- Net read：**healthy / typical** —— 品类里"一个动作做深"的 v0.1 有直接成功先例
- Cited comparables：
  - [Connected Papers](https://medium.com/connectedpapers/connected-papers-post-launch-community-update-64d952423d56)（2020 side project · launch 只有单种子图一个动作 · [premium 后加](https://medium.com/connectedpapers/announcing-premium-accounts-multi-origin-graphs-and-more-92e8dbd66848)）
  - [Undermind](https://www.undermind.ai/)（launch 即单一动作 · agent 深检索 3-5 分钟 · [watch 是后加](https://www.ycombinator.com/companies/undermind)）
  - [Gemini Deep Research](https://gemini.google/overview/deep-research/)（5-30 分钟出带溯源报告已被用户驯化，"评估要等几分钟"不是采用障碍）
  - [ThoughtWorks Tech Radar](https://www.thoughtworks.com/en-us/radar/faq)（四环 adopt/trial/assess/hold 词表 20 年验证 · [build your own](https://www.thoughtworks.com/insights/blog/build-your-own-technology-radar)）

**Best fit for 一个 human who**:
第一优先级是**验证差异化与信任**、想尽快亲手用上、不愿在 v0.1 就背长期维护负担的 operator。
如果你更想"先证明冷启动方向判断这件事真有价值，再决定要不要长成雷达"，A 是那个可回收、
盒内有余量、价值第一天兑现的起点 —— 而且 journal 的使用数据会直接告诉你要不要走向 B。

---

### Candidate B · "评估→留驻漏斗（组合盘）"

**Suggested fork id**: `001-radar-pB`
**Sources**: Claude R1-C 漏斗骨架 + GPT R1-B / R2-B 的状态卡组合盘；GPT R2 称 B 为**最稳的 product thesis**

**v0.1 essence**:
A 的全部（冷启动评估 + 历史位移内嵌 briefing）+ **留驻机制**。评估完你可"留驻"该方向 —— 留驻
topic 保存第一帧基线，形成一张**状态卡组合盘**（每卡带结论 / 关键变化 / 覆盖质量标注，深浅允许
不一并明示），周级轻量 re-scan，回访时给"自基线以来位移"briefing。覆盖面从 0 开始，随真实评估
行为长到 3 个月末的 5-10 卡 —— **8-15 是轨迹终点，不是 v0.1 交付物**。位移在这里有两个来源：
单次评估内的公开脉络重建（同 A）+ 留驻后回访的自建基线 diff。这是"雷达"的第一级台阶。

**User persona**（具体）:
同 A 的 operator，但使用姿态多一层：既要评估新方向（事件驱动），也希望少数已认可的方向不再从
脑内悄悄过期（周级回访）—— 想朝"8-15 张活地图"的原始梦想迈一步，愿意为此在 v0.1 就背上留驻成本。

**Core user stories**（3-5）:
- 作为 lab lead，我评估一个新方向，得到 A 级深度的成型度 briefing（继承 A 的全部评估故事）。
- 作为 lab lead，评估完我可一键"留驻"，该方向进入组合盘、保存基线快照，地图不再从脑内过期。
- 作为 lab lead，我回访留驻 topic 时，看到"自上次看以来"的位移 briefing + diff 证据；显著位移在打开时置顶（pull 内排序，非通知）。
- 作为 lab lead，我能在组合盘一眼扫过所有留驻方向的状态卡（结论 / 关键变化 / 覆盖质量），挑出需要行动的 2-3 个。
- 作为 lab lead，我能看到评估决策 journal 随时间的对错（当时说成型 → 后来真成型了吗），这是信任机制内建。

**Scope IN（v0.1）**:
- A 的完整冷启动评估（含公开脉络重建 briefing + 证据链 + journal + taste 反馈）
- 留驻 / 归档机制 + 基线快照保存
- 状态卡组合盘（结论 / 关键变化 / 覆盖质量标注 · 深浅不一并明示）
- 留驻 topic 的轻量周级 re-scan + 基线-现状位移 briefing
- pull 内显著位移置顶
- 3 个月末预期 5-10 个留驻卡

**Scope OUT（explicit non-goals）**:
- **一次性批量导入 15 topic** —— 覆盖靠用长出来，不做批量登记
- push 通知、跨 topic 方法迁移检测、alert（v0.2 候选）
- lab 共享 / 团队协作、问答器、全覆盖

**Success observable**:
- 3 个月末：≥5 次评估、≥4 个留驻 topic 有 ≥2 帧快照、≥1 次"回访位移"给出 operator 没意识到的变化
- journal 里 ≥1 条"当时 briefing 判断 → 后验证实"记录
- 每个 briefing 判断 3 击内到原文证据
- 一次组合盘复盘能产出明确行动清单（挑出 2-3 个需行动方向）

**Time estimate under your constraints**:
- 给定你的 intake：约 **11-13 周 @22-28h（250-330h）**，**贴预算上沿**。
- Confidence: **M-**。若下调：v0.1 里塞两层机制（评估 + 组合盘），首月交付压力大。
- **退化路线（已设计好）**：若第 8 周发现超支，把"周级 re-scan"降为"手动 re-run"，回到 A + journal，不伤主线。

**UX priorities**（tradeoff 立场）:
- 评估体验优先（它是"对自己获客"的价值时刻）；位移是回访奖赏，不是首屏义务
- 每个 briefing 判断携带证据链 + 不确定度标注（真理机红线的正面实现）
- 组合盘允许不同 topic 深浅不一，但把覆盖质量明示（诚实呈现"8-15 期望 vs 预算"张力）

**Biggest risk**:
v0.1 里塞了两套机制（评估 + 组合盘），撞第一个月的交付压力。更深的风险是**组合盘可能没人回访** ——
如果留驻 topic 的回访频次低于预期，整个留驻机制就成了死重，正撞 dashboard 失败研究说的
"与决策隔离建设 + 第一个月没有价值时刻"死亡区（72% BI dashboard 被弃用的主因）。这是产品级 /
采用风险，不是技术风险。

**Scope-reality verdict**:
- 同类产品里图 + 监控**已是常规能力**（Litmaps / ResearchRabbit 已经拥有），所以 briefing 必须保持窄 —— 一旦泛化就撞车
- 状态卡组合盘**没有直接先例**（Undermind 的 watch 是单方向 keep-tabs，不是多方向状态卡组合视图）
- Net read：**ambitious**（相对 A 更重，留驻层无直接先例）
- Cited comparables：
  - [Litmaps features](https://www.litmaps.com/features)（搜索大论文库 + 引用关系找相关工作 + 可视化 + 监控新文章邮件 · 图和监控是中心，非"结构成型度判断"）
  - [ResearchRabbit features](https://www.researchrabbit.ai/features)（个性化推荐 + collection 组织 + 互动地图 · 不把"该不该投一个方向"绑定 lab lead 决策仪式）
  - [Undermind](https://www.undermind.ai/)（watch / 更新提醒是单方向后加功能，非多方向组合盘）
  - [2026 evaluation paper](https://arxiv.org/abs/2605.10125)（AI 文献工具信任底线变高：不能只给强判断，每个判断必须带可核验证据）
  - [Scientific Contribution Graph](https://arxiv.org/abs/2605.15011)（方法 / 贡献级图语义不能单独当护城河 · v0.1 要卖判断仪式不卖图谱本身）

**Best fit for 一个 human who**:
第一优先级是**尽快朝"8-15 张活地图"的原始愿景迈实质一步**、愿意在 v0.1 就接受留驻机制成本和
贴预算上沿风险的 operator。如果你确信自己评估完新方向后会**反复回访**它们、看它们随时间的位移，
B 值得一博 —— 但只有当你对"回访行为真会发生"有信心时才选它（否则组合盘会成死重）。

---

## Comparison matrix

| Dimension | Candidate A（方向评估官） | Candidate B（评估→留驻漏斗） |
|---|---|---|
| v0.1 weeks | 9-11 周（180-220h） | 11-13 周（250-330h） |
| 价值首次兑现时点 | **第一天**（单次评估当场完整） | 评估当天有；位移价值需 ≥2 帧后回访兑现 |
| 位移来源 | 公开脉络重建（单次评估内） | 公开脉络重建 + 自建基线积累（留驻回访） |
| 覆盖面 @3个月 | 一叠评估档案（无常驻活地图） | 5-10 张留驻状态卡（8-15 为轨迹终点） |
| Dominant priority | 差异化 / 快价值 / 可验证 | 覆盖轨迹 / 组合复盘 / 朝原愿景 |
| Biggest risk | briefing 读起来像通用 Deep Research 报告 | 塞两层机制 + 组合盘可能没人回访（dashboard 死法） |
| Scope-reality fit | ✅ healthy / typical（窄切有直接先例） | ⚠ ambitious（留驻层无直接先例） |
| Fits your time budget | ✅ 盒内有余量 | ⚠ 贴上沿（有退化路线兜底） |
| Respects all red lines | ✅ | ✅ |

## Candidate relationships

> 本章分析 A 与 B 到底是替代 / 互补 / 顺承,从而帮你决定用哪种 fork 命令。
> **4 种 PRD 形态**:simple / phased / composite / v1-direct。

### 1. Pairwise relationship matrix

只有 A、B 两个候选,故只有一对关系（A→B）。

| 关系维度 | A→B |
|---|---|
| **替代 / 互补 / 顺承**（选一） | **顺承** —— B ⊇ A（B 的 IN 完整包含 A 的冷启动评估核心），B 在 A 之上加留驻层。A 是 B 的前置：没有 A 的评估产出（基线快照）B 的留驻 / 回访无从启动 |
| **共享产物?** | 是,且是包含关系。A 的冷启动 pipeline + briefing + journal + 证据链,是 B 的整个下半身。B 复用 A 的全部,再叠留驻 / 组合盘 / re-scan |
| **时间依赖?** | 是。A 必须先于 B 才有意义 —— 留驻机制的输入是"一次评估产出的基线",评估能力不成立则留驻是空壳。B 的退化路线也正是"退回 A" |

**关系定义**（参照本项目 fork 语义）:
- **替代**:做了 A 就不该做 B。
- **互补**:A 和 B 服务同一产品的不同器官,合体价值 > 单独。
- **顺承**:A 是 B 的前置(没有 A 的产出 B 无法启动)。

### 2. 如果合体,产品长什么样?

A 与 B 无法"合体成第三个东西",因为 **B 已经是 A 的超集** —— B = A + 留驻层。所谓"合体"就是 B 本身。
换句话说,这不是两个平行器官拼在一起,而是同一产品的**两个成熟度阶段**:A 是"评估官"这一个器官,
B 是"评估官 + 让评估结果驻留成活地图"的下一步。产品形态非常自然、无别扭感 —— 恰恰因为它们不是
两个独立候选,而是一条产品线上的相邻两帧。这一点排除了 composite(见 §5),指向 phased 或
"先 A 后按数据决定 B"。

### 3. PRD-form 推荐

**推荐**: **simple(fork A 作单 v0.1)**,并把 B 作为"数据驱动的自然 v0.2"显式记录在菜单里。
次优等价形态: **phased(A = v0.1,B 的留驻层 = v0.2,在同一 PRD 里声明两 phase)**。

**理由**（引用 §1 结论）:
A→B 是**顺承**关系(§1),B ⊇ A。既然 B 完整包含 A,最稳的走法是**先把 A 这个前置做扎实、
拿 journal 使用数据验证"回访需求真不真"**,再决定要不要展开 B 的留驻层。intake 的仪式选择
(冷启动评估)+ Connected Papers / Undermind 的窄切先例 + A 盒内有余量而 B 贴上沿 —— 三条证据
都压向"先 simple A"。B 不是被拒的 sibling,它是**同一产品晚一个 phase 的样子**(GPT 称 B 为
最稳 product thesis,这个判断被 honor:B 是终局形态,只是不该在 v0.1 就全建)。

**不推荐**:
- **composite** —— A、B 是顺承 / 超集关系,不是互补的不同器官(§2 已验证合体就是 B 本身),
  composite 会误用(见 §5)。
- **v1-direct** —— §4 评估 C1/C2/C3 全 ❌,跳过 v0.1 无依据。
- **一上来就 fork B** —— 贴预算上沿 + 组合盘"可能没人回访"的 dashboard 风险未经验证,
  在 A 的 journal 数据出来前下注 B 是拿预算赌一个未验证的行为假设。

### 4. 跳过 v0.1 的合理性评估

| 条件 | ✅/❌ | 证据 |
|---|---|---|
| **C1**:核心假设是否已外部验证? | ❌ | L2 净判定是 **Y-with-conditions** 而非 Y;护城河脆弱、形态问题(payload)L2 明确标为"想象里定不下来、需自用验证";"回访行为真会发生"这一 B 的核心假设完全未验证 |
| **C2**:v0.1 是否有独立可发布价值? | ❌(此处答案对 v1-direct 不利,但对本产品是好事) | A 本身就是完整可用的 v0.1(每次评估用完即完整),不存在"v0.1 无独立价值必须直奔 v1"的协议 / SDK / 平台型情形。恰因 A 独立有价值,更没理由跳过它 |
| **C3**:多 candidate 是否互补? | ❌ | A、B 是顺承 / 超集(§1),非互补的不同器官。不满足 composite / v1-direct 的互补前提 |

**判断**: **0 条 ✅ → 必须走 v0.1(simple 或 phased)。v1-direct 无依据。** 这与 §3 推荐一致。

### 5. composite vs parallel forking 区分（防误用）

- **composite 不适用**:它仅适用于 N 个候选是同一产品的**不同器官、合体才完整**。本菜单 A→B 是
  **顺承 / 超集**(§1),B 就是 A 的下一阶段 —— 合体后产品形态(§2)= B 本身,没有"多器官拼装"的
  语义。强行 composite 会把"一个产品的两个 phase"错当"两个模块",且 composite 一旦下注就要全做,
  正好背上 B 那份未验证的留驻风险。**禁止推荐 composite。**
- **parallel forking 也不必要**:parallel(001-radar-pA + 001-radar-pB 各自独立跑 L4)适用于
  "同时试多个真正的 peer 看哪个赢"。但 A、B 不是竞争的 peer —— B 含 A,并行跑等于把 A 的工作做两遍。
  更省的走法是先 fork A,用数据决定要不要接 B。
- **结论**:本菜单关系是"顺承"(非"替代"),故不触发"禁止 composite 时强制 parallel"的规则;
  正解是 **simple A → 数据驱动的 v0.2 B**。

---

## Synthesizer recommendation

**Fork A（`001-radar-pA`），把 B 的留驻层显式框定为"数据驱动的自然 v0.2"。**

三条证据一致压向 A:(1) 你 intake 亲自选的仪式是**冷启动评估**——A 正是这个仪式的纯净兑现,
B 在它之上加的留驻层不是仪式本身;(2) 品类里"一个动作做深"的窄切 v0.1 有 Connected Papers /
Undermind 的直接成功先例,而 B 的状态卡组合盘无直接先例;(3) A 盒内有余量(180-220h)、价值第一天
兑现、零维护负担,B 贴预算上沿且首月位移无价值时刻(撞 dashboard 死法)。**关键**:A 的评估 journal
会直接产出你需要的那个数据 —— "我评估完新方向后,到底会不会反复回访它们?" 这正是 B 的核心假设。
先用 A 三个月,journal 数据说"我一直想回看那几个留驻方向",就顺承 fork B(留驻层);数据说"评估完
就归档、从不回访",那 B 的整套留驻机制本就该省掉。

**关于 GPT 称 B 为"最稳 product thesis"** —— 这个判断被 honor,不被驳回。B 确实是这条产品线的
**终局形态**(评估 → 留驻 → 活雷达 → 8-15 覆盖),它不是一个被拒的 sibling,而是**同一产品晚一个
phase 的样子**。区别只在时机:B 的最大风险("组合盘没人回访")恰恰是 A 的 journal 能便宜验证的东西,
所以先 A 后 B 是把 B 的赌注推迟到有数据之后,而不是否定 B。

**可选等价框法**:若你想把 phase 关系写进同一份 PRD 而非分两次 fork,用 phased 形态
(`/fork-phased 001-radar from-L3 candidate-A as 001-radar-pA`,声明 phases = [v0.1 评估官, v0.2 留驻层])。
两种走法产品内容相同,只是治理颗粒度不同 —— simple 让你在 phase 之间有一个明确的"看 journal 数据
再决定"的决策闸口,我略偏好 simple。

**不 fence-sit 的一句话**:先 fork A;B 的 PRD 骨架已在本菜单里成形,三个月后若数据支持,
可直接 `/fork 001-radar from-L3 candidate-B as 001-radar-pB` 而无需重跑 L3。

## Honesty check — 菜单可能低估了什么

- **两候选都假设"公开脉络重建"能真做出可信的历史位移证据。** 这是 A/B 差异化的地基,但它本身在
  L3 层没被 scope-reality 之外的证据检验过 —— 它到底能不能从公开数据重建出"如何从热词变成结构"的
  可信叙事,是 L4 / 自用才知道的事。如果重建质量不行,A 退化成一次性调研报告的风险(A 的 biggest risk)
  会提前引爆。这是两个候选共享的、菜单无法在此层消解的地基风险。
- **两候选的时间估算都假设 briefing 的"结构成型度"文体一次做对。** 但结论词表的最终形态是仍开放的
  ❓,如果词表反复调整(拿同行反应校准),会吃掉 A 的盒内余量、把 B 推出预算盒。时间估算里没有为
  "词表返工"留缓冲。
- **两候选都未处理"慢领域"边界。** L2 natural limit 指出半年位移接近零的慢领域里产品核心呈现没东西
  可画。intake 没问 operator 的 8-15 topic 是否全是快领域;若其中有慢领域,那几个方向的评估 briefing
  会显得空。菜单默认了"operator 的方向都是 arxiv 速度的",这个假设没被 intake 确认。
- **B 的"回访行为"是纯假设,无任何数据。** 这是推荐"先 A"的核心理由,但也要诚实说:如果 operator
  已经很确定自己会回访(比如他现在就有反复翻看某几个方向的习惯),那"先 A 验证回访"这一步对他就是
  多余的谨慎,直接 phased / B 更省。菜单基于"回访未验证"给建议,operator 若有反例可推翻。

## Decision menu（for the human）

> PRD-form 决定用哪个 fork 命令。本菜单推荐 **[F] simple A**(§Synthesizer recommendation);
> phased 是等价次优。composite / v1-direct 已被 §Candidate relationships 排除。

### [F] Fork one candidate（simple form,single v0.1）— **推荐**
  /fork 001-radar from-L3 candidate-A as 001-radar-pA
  /plan-start 001-radar-pA

### [FP] Fork with phased planning（A = v0.1,B 留驻层 = v0.2,同一 PRD）— 等价次优
  /fork-phased 001-radar from-L3 candidate-A as 001-radar-pA
  （interactive：声明 phases = [v0.1 方向评估官, v0.2 评估→留驻漏斗]）

### [MF] Fork both in parallel（不推荐 —— B ⊇ A,并行等于把 A 做两遍）
  /fork 001-radar from-L3 candidate-A as 001-radar-pA
  /fork 001-radar from-L3 candidate-B as 001-radar-pB
  ⚠ 仅当你确信要同时下注两条独立 L4 时用;本菜单关系是顺承,不建议

### [R] Re-scope with new input
  /scope-inject 001-radar "<steering>"
  /scope-next 001-radar

### [B] Back to L2 — rethink the idea
  /status 001-radar

### [P] Park
  /park 001-radar

### [A] Abandon
  /abandon 001-radar

---

## 落选记录 · 纯 Radar-first / 8-15 组合盘点为什么不在菜单里

Claude R1-B「全幅雷达」= GPT R1-B/R2-C「8-15 组合盘点」这一类"一次性登记 8-15 topic + 持续 ingest
保持每张地图不过期"的候选,被**双方 R2 独立判死**,故不作为 peer,只在此留证据:

1. **超预算**：~12-14 周 @25-30h（300-400h），只有 30h/周全勤才勉强塞进 2-3 月盒子（信心 L）。
2. **首月无价值时刻**：位移要等快照积累 4-6 周后才首次兑现，正撞 dashboard 失败研究说的
   "第一个月没有价值时刻"死亡区（72% BI dashboard 被弃用的主因）。
3. **冷启动仪式被边缘化**：operator 亲自选的最痛仪式（冷启动评估），在这个 cut 里退化成
   "添加第 N 个 topic"的入口，主次颠倒。

B（评估→留驻漏斗）保留了"朝 8-15 活地图迈步"的价值内核，但用**"覆盖靠用长出来"**替代了
"一次性登记 15 个"，规避了上述三条死因 —— 所以进了菜单，纯 Radar-first 没进。

---

## Fork log
- 2026-07-07T02:58:21Z · Candidate A「方向评估官（历史位移内嵌）」forked as `001-radar-pA`（status: just-created · PRD.md 已产 · simple 形态 · 下一步 /plan-start 001-radar-pA）· Candidate B 留菜单作数据驱动 v0.2 候选,未 fork
