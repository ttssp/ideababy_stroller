# Idea 001-radar · L3R1 · Claude · Scope (no search)

**Timestamp**: 2026-07-06T17:37:29Z
**Inputs read**: L2 report, L3R0-intake
**Searches used**: NONE in this round
**Visibility**: did NOT read other debater's L3R1
**Model note**: 本轮由 Claude(Fable 5)执笔,文件名沿用管线约定。

## 0. How I read the intake

operator 本人即目标用户,这让 L3 少了一层猜测,但 intake 里有一处结构性张力必须由候选来裁而不是被含混掉:**锚定的仪式是"开新方向评估(冷启动)",而 idea 的原始卖点是"位移"——刚冷启动的新方向没有旧地图可 diff**。我把三个候选设计成这个三角(冷启动深度 × 覆盖广度 × 位移完整度)上的三个真实取舍点,都尊重硬约束:2-3 月 / 15-30h 周 / briefing 为主 + diff/图作证据 / 单人版 / 不追全覆盖。8-15 topic 是 operator 期望值,与预算有张力——我在每个候选里诚实标注它到底能不能到 15,不静默砍窄。

- 尊重的硬约束:时间盒/工时、用户=lab lead 本人、仪式=冷启动评估、payload=briefing 为主、单人版、不追全覆盖
- 将为 ❓ 提选项:商业模式、平台形态、冷启动 vs 位移主次、alert 例外、信任机制
- 红线照单:不追全覆盖(硬)+ §5 补提

## 1. Candidate A · "方向评估官(Assessor-first)"

### v0.1 in one paragraph
一个**按需出动**的研究方向评估 agent:你给它一个方向(一句描述或 2-3 篇种子 paper),它冷启动一张该方向的方法级地图,然后交给你一份**强观点评估 briefing**——这方向结构上成没成型(分散爆发 vs 稳定问题簇+方法簇互连)、中心 claim 是什么、哪些已被 contradicts、建议投/观望/不投——每个判断可点开看证据(节点、边、快照)。它不常驻、不推送:你评估哪个方向,哪个方向的地图才存在。

### User persona (sharpened from L2)
operator 本人:AI lab 负责人,每月 1-3 次面临"这个新方向值不值得投一队人/一个学生"的决策,现状靠 X 碎片 + 走廊直觉,想要"结构上是否成形"的可核验判断。

### Core user stories (3-5)
- 作为 lab lead,我能给出一个方向名/种子 paper,在**一次咖啡的时间尺度内**拿到冷启动评估 briefing,让"回去想想一周"变成"当场有据讨论"。
- 作为 lab lead,我能点开 briefing 里任何一个判断,看到支撑它的节点/边/原文出处,自己核验 agent 有没有胡说。
- 作为 lab lead,我能对同一方向**re-run 评估**,拿到"距上次评估的变化"——这是本候选唯一的位移形态(评估间 diff)。
- 作为 lab lead,我能把评估结论(投/观望/不投 + 日期)留档,三个月后回看当时判断对不对。

### Scope IN
- 冷启动 pipeline:方向输入 → 检索收集 → 方法/claim 级图构建(单方向、量级小)
- 结构成型度 briefing(判断+证据链,可展开)
- 评估留档 + re-run diff(同方向二次评估的对比)
- 3-5 个真实评估跑通(operator 自用验证)

### Scope OUT (explicit non-goals)
- **常驻 8-15 topic 持续跟进**——本候选里 topic 地图是评估的副产物,不做后台持续 ingest(那是 B/C 的事)
- 跨 topic 视图、方法迁移检测、区域 alert
- 任何 push;问答/报告生成器;全覆盖

### Success looks like
- 3 个月内完成 ≥5 次真实新方向评估,其中 ≥1 次实际改变了 operator 的投入决策
- 任一 briefing 的任一判断都能在 3 次点击内到达原文证据
- 对 operator 已深耕的方向做"盲测评估",briefing 判断与 operator 自己的判断一致或给出他认可的新信息(信任校准)

### Honest time estimate under human's constraint
~8-10 周 @ 20h/周(160-200h)。信心 M——冷启动检索+图构建质量是主要不确定源。**在预算内,留有缓冲**。

### UX principles
- 判断先行,证据随取;宁可 briefing 观点强+标不确定度,不做四平八稳综述
- 单次评估体验 > 长期库完整性;不为未来的常驻功能预留 UI 复杂度

### Biggest risk to this cut
它放弃了"radar 持续性"——如果 briefing 质量不够一锤定音,产品退化成"一次性文献调研工具",与 Undermind/Elicit 的 report 面撞车(L2 明确要避开的)。差异化全押在**结构成型度这个独有判断框架**上。

## 2. Candidate B · "全幅雷达(Radar-first)"

### v0.1 in one paragraph
operator 期望的字面版:一次性登记 8-15 个 lab topic,agent **持续**收集新工作、织进每张 topic 地图,每张地图积累时间快照;打开任一 topic 得到"90 天位移 briefing"(哪些假设退潮/哪些簇合并/哪个新节点挤向中心 + 证据展开)。冷启动新方向作为"新增第 N 个 topic"的入口存在,但评估 briefing 是简化版(成型度判断的深度让位于覆盖广度)。

### User persona
同上,但使用姿态是**周检视**:每周打开 2-3 张地图看位移,季度复盘时逐张过。

### Core user stories
- 作为 lab lead,我登记 8-15 个 topic 后,系统持续保持每张地图不过期(新 SOTA 自动织入)。
- 作为 lab lead,我打开任一 topic 能看到 90 天位移 briefing + 可展开的快照 diff。
- 作为 lab lead,我能新增一个 topic,冷启动地图在一天尺度内就绪(简化评估)。
- 作为 lab lead,季度复盘时我能逐张导出位移摘要带进会议。

### Scope IN
- 持续 ingest pipeline(8-15 topic 并行)· 快照机制 · 位移 briefing 生成 · 简化冷启动

### Scope OUT
- 深度成型度评估(降为简化版)· lab 共享 · alert · 问答器 · 全覆盖

### Success looks like
- 12-15 张地图运行 ≥6 周不过期;≥2 次位移 briefing 给出 operator 事先没意识到的漂移;季度复盘真的用了它

### Honest time estimate under human's constraint
**~12-14 周 @ 25-30h/周(300-400h),超预算上沿**。信心 L:8-15 topic 并行的持续 ingest + 品味过滤 + 快照 + briefing,四个都是首次建设。**诚实结论:这个 cut 在 2-3 月盒子里只有 30h/周全勤才勉强塞下,且首月没有任何一张图有"位移"可看(快照还没积累)——价值兑现最晚**。若 operator 坚持此形态,现实做法是砍到 5-6 topic 起步,但那就不再是这个候选的卖点了。

### UX principles
- 覆盖完整性 > 单点深度;位移可信 > 位移酷炫

### Biggest risk to this cut
双重风险:预算超限 + **冷启动仪式被边缘化**(operator 自己选的最痛仪式在这个 cut 里只是"添加 topic"的入口)。且位移价值要等快照积累 4-6 周后才首次兑现,正撞 dashboard 失败研究说的"第一个月没有价值时刻"死亡区。

## 3. Candidate C · "评估→驻留漏斗(Funnel)"

### v0.1 in one paragraph
把 A 和 B 接成一条产品逻辑:**冷启动评估是 topic 进入雷达的唯一入口**。每次评估产出的地图+briefing 自动成为该方向的**基线快照**;评估后你选"留下跟踪"或"归档"。留下的 topic 进入轻量持续跟进(周级 re-scan),下次打开时给"自基线以来的位移 briefing"。覆盖面从 0 开始,随真实评估行为长到 8-15——**位移 = 相邻两次评估/扫描的 diff**,冷启动与位移不再打架,前者是后者的第一帧。

### User persona
同上;使用姿态 = 事件驱动(有新方向要评估)+ 周级回访(看留驻 topic 的位移)。

### Core user stories
- 作为 lab lead,我评估一个新方向,得到 A 级深度的成型度 briefing(同 A 故事 1-2)。
- 作为 lab lead,评估完我可一键"留驻",该方向进入持续跟踪,地图不再过期。
- 作为 lab lead,回访留驻 topic 时,我看到"自上次看以来"的位移 briefing + diff 证据。
- 作为 lab lead,我能看到自己的评估决策留档随时间的对错(信任机制内建:briefing 当时说成型,后来真成型了吗)。

### Scope IN
- A 的完整冷启动评估 + 留驻机制 + 留驻 topic 的轻量周级 re-scan + 基线-现状位移 briefing
- 评估决策 journal(信任回溯)

### Scope OUT
- 一次性登记 15 topic 的批量导入(覆盖靠用长出来,3 个月末预期 5-10 个留驻)· alert(v0.2 候选)· lab 共享 · 问答器 · 全覆盖

### Success looks like
- 3 个月末:≥5 次评估、≥4 个留驻 topic 有 ≥2 帧快照、≥1 次"回访位移"给出 operator 没意识到的变化
- journal 里 ≥1 条"当时 briefing 判断 → 后验证实"记录(信任第一块砖)

### Honest time estimate under human's constraint
~10-12 周 @ 20-25h/周(220-290h)。信心 M-。比 A 多出留驻/re-scan/快照机制;**贴着预算上沿但在盒内**。风险缓冲:若第 8 周发现超,可把"周级 re-scan"降为"手动 re-run"(退化成 A+留档)而不伤主线。

### UX principles
- 评估体验优先(它是获客时刻——对自己获客);位移是回访奖赏不是首屏义务
- 每个 briefing 判断携带证据链 + 不确定度标注(真理机红线的正面实现)

### Biggest risk to this cut
机制比 A 多一层,首月交付压力大;且"覆盖靠用长出来"意味着 3 个月末只有 5-10 topic——**operator 选的"8-15"在 v0.1 内不完全兑现**,要 operator 接受"期望值是轨迹终点不是 v0.1 交付物"。

## 4. Options for the human's ❓ items

- **商业模式**:① 纯自用(无账号/无计费,scope 最小,推荐 v0.1)② 自用+开源(多文档/可复现成本,+1-2 周)③ 预留 SaaS(auth 从 day1,+2-3 周,不推荐)。
- **平台形态(产品级)**:① 终端/CLI 出 markdown briefing(最贴 operator 工作流,证据展开靠链接)② 本地 Web 视图(briefing+可点开 diff/图,证据展开体验完整,+2-3 周)。C 的"证据展开"体验偏向 ②;可 v0.1 ①→v0.2 ②。
- **冷启动 vs 位移主次**:三个候选就是三个答案——A=冷启动独占;B=位移独占;C=冷启动为入口、位移为回访。
- **map-region alert**:v0.1 一律 OUT;唯一可接受的最小例外是 C 里"留驻 topic 有显著位移时,下次打开时置顶提示"(pull 内的排序,不是 push)。
- **信任机制**:① 证据链强制(每判断 3 击内到原文)② 评估 journal + 后验回看(C 内建)③ 盲测校准(拿 operator 已深耕方向测 briefing,A/C 的 success 都含)。建议三者全要,成本低价值高。

## 5. Red lines I'd propose (确认 + 补提)

1. **不追全覆盖**(operator 硬红线,三候选全部遵守)
2. **不做问答/报告生成器**——briefing 是"结构成型度判断"这一种文体,不接开放问题(否则撞 Elicit/Undermind 正面)
3. **不做 push**——一切信息在打开时呈现;C 的置顶提示是 pull 内排序,不发通知
4. **不做无证据判断**——briefing 每个论断必须可展开到证据,做不到就标"低置信",宁缺不装(真理机红线的执行形态)

## 6. Questions that need real user interviews (L3 can't answer)

operator 即用户,多数问题转化为**自用验证**(候选 success 里已内建)。仍需真实外部输入的:
1. 若未来走开源/给其他 lab lead 用:别的 lab 对"成型度"的判断框架是否与 operator 一致?(v0.1 不答,记入 v0.2 前提)
2. briefing 的"结构成型度"分级(成型/趋于成型/分散/退潮?)用什么词表让研究者第一眼信任——这需要 3-5 个同行看 mock 的反应,可在 v0.1 中后期用真产出物做非正式验证。
