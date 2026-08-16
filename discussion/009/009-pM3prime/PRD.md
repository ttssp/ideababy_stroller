# PRD · 009-pM3prime · "M3' 信号提取头 · 最小证伪链(E0+E1 期)"

**Version**: v1.2(2026-08-16 回写 **forge 009-pM3prime v5 verdict** · operator 选 Decision menu **[A] 全量落地** ·
`stage-forge-009-pM3prime-v5.md`:**审的是「绑定之后到底绑在哪儿」** —— 五条到期义务各暴露一种绑定落空方式。
**converged · 0 unresolved · CONCERNS。** 本次为 **IDS 侧收口**(refactor plan 模块 A + B),四处改动:
**① §6 条件 1/2 量词改写** —— 旧文「至少一个 per-market 读数」(存在量词)与条件 2「该市场」(特定量词)
不一致 ⇒ US 能字面满足却对 CN/HK 重判零信息;改为「**每个拟重判市场**均有可解释读数」+ 条件 2 **逐市场成立**。
**字面满足不算满足**,该判定**由本仓量词冲突独立成立,不靠外部标准背书**。
同时改写「条件 2 不可计算」的归因:不是数据缺,是**同一 pipeline 两条链分层粒度不同**
(密度链逐 market / 一致性链零 market 轴,两侧独立复证)⇒ **改措辞补不出来,必须新建 market 观测轴**。
**② §6 新增「低样本市场的显式状态」** —— 可用 / 复审 / `not_estimable` 三档 + **具名判定人**;
🔴 **只给形态不给数字**(外部统计标准的精确档位属过度外推,已被 P3R2 检验拦下)。
**③ §6 新增「跨批读数的消费契约」** —— `census_run` 表**终于有了消费者**:IDS operator-chair,
在每次 `/handback-review` 引用跨批读数**之前**枚举,命中四条停止条件任一即**停止结论与验收签署**。
**④ §7 红线 3 补两块** —— `-04` 校准监测周期**载体等级裁定 = `codified`**(此前只活在 ledger 一个
JSON 字段里,三处 grep 全零命中);`-05` 统计型重校准**三态各绑 {允许方法, 已知敞口, 退出证据}**,
**删除「历史足量后再做」静默态**。
⚠ **不变的**:扩样与 E2 **继续 blocked**;41 条盲标路**仍 CLOSED**;C6 冻结门槛**数字**未改;
CN/HK 执行态 `STOP` 与认识态 `UNKNOWN` 均不变;未改 `specs/`、未改框架 schema。
⚠ **已知未处置**:(i) **KG-42 同族未解** —— 七问的 `owner` 与复审独立性在**只有一个人的仓**里
不可同时满足,双方一致签署「不解 + 具名敞口」(`OB-...-v5-11` → `forge:006:phase0`);
(ii) `/handback-review` 能否在不改 SHARED-CONTRACT 前提下承载硬停点**未验**,证不能则消费契约降级 v0.2;
(iii) `ids:handback-review` / `xenodev:ship-gate` / `xenodev:task-review` **三个消费 gate 全未接线**
⇒ 本轮 13 条义务中 **6 条登记了也不会被消费**,`exposure` 已逐条写明。
v1.1 2026-08-14 回写 **forge 009-pM3prime v4 verdict** · operator 选 Decision menu **[B]** ·
`stage-forge-009-pM3prime-v4.md`:**审的是这套治理机制自身** —— 条款、义务、gate 之间的传导,
不是任何一个技术对象。**converged · 0 unresolved · CONCERNS。**
本轮**只做条款同步组**(refactor plan A),一处产品级改动 + 一处口径澄清:
**① §6 科学重判触发条件 1 加「未满足注记」** —— T015 产出的是**全局**跨次一致性读数
(`J_1=0.4078` / `J_agg=0.6885`),结果矩阵**零 per-market 分解**,而条件 1 要求「至少一个 per-market」;
⇒ **条件 1 仍未满足**,登记 v0.2(`due_gate: forge:009-pM3prime:phase0`)。
排除它作本轮硬产出的理由是**判据膨胀(程序性)**,不是它不重要 —— 下次 firing 仍不处置应视为拖延。
**② §7 红线 3 的 C4 `convert` 判据形态定形** —— 将来若要把 `report-only` 升为门禁,
判据 = **过程证据 + 结果证据 + 具名批准 + 版本化回退,四者合取,不给数字**
(三个独立工业先例 OPA / Chrome / Kubernetes KEP **无一给数字阈值**;Chrome 原文
「There is no threshold for which removal is necessarily safe」);
回退语义 = **历史不可变,授权被后续 `caliber_version` supersede**(只撤销旧版未来消费权,不改历史)。
⚠ **M1 = pass 的具名裁决**(本轮补上的欠账):接受为**固定批可比性**证据 ——
NIST「statistical control can only guarantee comparability among measurements」;
**不作效度代理 · 不外推 · 不解锁扩样与 E2**。两项必载风险输入:
(i) 一致率上升**无法区分**噪声去除与**歧义抹除**(「filtering non-consensus samples results in
over-optimistic results」逐字对应 M2 留存口径);(ii) 6 个跑的 `census_verdict` **全部**
`below_threshold_advisory`。
⚠ **不变的**:扩样与 E2 **继续 blocked**;41 条盲标路**仍 CLOSED**;C6 冻结门槛**数字**未改
(本轮只议其形态中的**可回退性**);未改 `specs/`。
⚠ **已知未处置**:`convert` 四要件中的「**具名批准**」在本仓只有一个人,
与 **KG-42(无合格第二源)同族**,只是断面从「标注的第二源」换成「**批准的第二源**」;
不得假装 KEP 的 PRR 形态可直接移植 —— PRR 的独立性来自组织,本仓没有组织。
v1.0 2026-08-13 回写 **forge 009-pM3prime v3 verdict** · operator 选 Decision menu **[B]** ·
`stage-forge-009-pM3prime-v3.md`:**审的是产出信号的那台机器本身**,不是金标。两处改动:
**① §7 红线 3 改形态** —— 「同文本同版本必须同输出(一致性测试)」**作废**,替换为
「强制测量 + 申报 + 落库 + 身份绑定,`pass_semantic: none`」。理由不是放松要求,是**去掉一个
原理上不可满足的要求 + 一个假绿信号**:T=0 非确定性的修复位点在推理引擎 kernel 的 batch invariance
(实测 1000 次 T=0 补全出 80 个不同结果),而 DeepSeek 官方无 `seed`、无可复现性承诺;
且该红线的契约测把 proposer 换成 `literal_ticker_proposer`(构造上确定)⇒ **命题恒真却一直给绿信号**;
实测反证 = 同日同参两跑 Jaccard **0.44**。已登记 `WARN-c4-extraction-stability-report-only`
(`temporary` · `due_event: forge:009-pM3prime:phase0` · 已接线)。
**② §6 CN/HK 改判为双态** —— **执行态 `STOP` 不变**(measurement-invalid 下的 fail-closed),
**认识态改 `UNKNOWN`**;旧「真稀疏」事实断言**作废**(建立在单次读数上,而 per-market 恰是噪声最大的一层:
CN 1/0/2 · HK 0/0/4,而总量同日方差仅 3%)。**US go 不受影响**(40/73/65 三次均 > 30,不是当初判错)。
⚠ **不变的**:扩样与 E2 **继续 blocked**(`M1=pass` 也不解锁);41 条盲标路**仍 CLOSED**;
Layer-1 四项缺角**仍未补**;红线 4(第二源资格)**不动**。
配套 12+2 条 obligations 见 `framework/obligations/ledger.jsonl`(6 条挂已接线的
`forge:009-pM3prime:phase0`,下一轮 forge intake 会被硬阻断);
Hard 契约「恒真替身」普查结论(**C4 是孤例**)见 `HARD-CONTRACT-SWEEP-20260813.md`。
v0.9 2026-08-12 回写 handback `009-pM3prime-20260811T171735Z`[FU-HB32] 决议 ·
HANDBACK-LOG 第 33 条:**🔴 41 条盲标机会的 Layer-2 金标路在 v0.1 明确关闭(不是 blocked-待前置,
是 closed)** —— 三个独立前提同时不成立:① **合格第二源**(KG-42,forge v2 撤销「operator 可自任」后
至今未解)② **盲标隔离**(IDS 侧实证:约 **19/41** 条的机器答案已经由治理文档通道泄漏,详见
§4-E1 **块 (p)**)③ **时序不变量**(`blind_annotated_at` 须早于 `machine_extracted_at`,对 2026-07-18
的历史批次结构性不可满足);且终点本就被 v0.7 冻结为「correctness gate 在 v0.1 不成立」⇒
`passed = criteria_met and _CORRECTNESS_GATE_AUTHORIZED_V0_1` 恒 False,**拆封在 v0.1 产不出可用结论**。
重开条件写在块 (p)。E1 US 密度结论、红线本体、Layer-1 结论收窄一律不动;见 §4-E1 块 (p) + §6 表 +
HANDBACK-LOG 第 33 条。
v0.8 2026-07-28 回写 handback `009-pM3prime-20260728T035015Z`[阶段 0+1+2] 决议 ·
HANDBACK-LOG 第 31 条:**🔴 撤销「两维外锚 lane」分支** —— forge v2 §134 称 timepoint 有
`published_at` 外锚系**事实错误**(frozen `SLA.md` 该行写的是「无」),该字段是**管线恒等**
(census 从 `records.published_at` 原样回填 · LLM 被结构性禁产 · 真盘 41/41 逐字节相同),
「两维」实为**一维**;且剩下那一维只核 ticker 的**合法性**不核**归属**(逐条张冠李戴到 watchlist 内
别人的 ticker → 判据 100% 通过)⇒ **lane STOP · 第 30 条据 §134 立的分支作废** ·
**Layer-1 结论收窄**:41 条盲标机会**不得用作 recall 框**(`gold ⊆ pred ⇒ span_recall ≡ 1.0`)、
**不得走 `evaluate_layer1`**,但**是目前唯一已物化的 span precision 框**(precision 无对偶退化)·
**`span_prf` 的 exact-match 形态才是 Layer-1 根因 —— 换抽样框治不了**(KG-43「数字 vs 形态」同族)·
全文红线行号锚改为**无行号锚**(KG-45:IDS 语料曾有 39 处失效行号)· 红线本体与 E1 US 密度结论不动;
见 §4-E1 **两维 lane 撤销块** + §7 + HANDBACK-LOG 第 31 条。
v0.7 2026-07-27 回写 handback `009-pM3prime-20260727T065748Z`[FU-KG43] 决议 · forge
009-pM3prime **v2** verdict · operator 选 **[C] 局部接受** · HANDBACK-LOG 第 29 条:
**🔴 撤销 v1「operator 可自任 Layer-2 第二源」推论**(范畴替换 —— 比较器领域中立 ≠ 标注劳动领域中立;
三解释维无外锚)· **KG-42 死结未真解 · 第 27 条「死结解」判定作废** · **撤销 07-25 gold 协议的 validity
地位**(同一人两版 = Krippendorff stability ≠ validity)· **全量五维 correctness gate 在 v0.1 不成立且
不因换主体/调门槛而成立** · **E2 解锁条件 ② 拆两条,②-b 回测 lane 明确 blocked** · 候选降级面
groundedness **[C] 下挂起**,待零成本效力探针证明 n≈41 具区分力后另议 · 门槛形态修正判据(数字 vs 形态)采纳 ·
红线(`gold_layer2.evaluate_layer2` 首个 guard)与 E1 US 密度结论不动;见 §4-E1 **D-7 v2 修订块** + §7 + HANDBACK-LOG 第 29 条 +
`forge/v2/stage-forge-009-pM3prime-v2.md`。
v0.6 2026-07-23 回写 handback `009-pM3prime-20260723T082127Z`[FU-KG42] 决议 · forge
009-pM3prime **v1** verdict:**§4-E1 Layer-2 金标 D-7 改写** —— 第二源资格从「领域独立真人」refactor
为「错误独立性代理(外证据锚定 + 逐维双错率证成 · 不靠品牌/领域深度)」· **frozen §2×D-7 收窄为验收级
暂不可满足 · operator 配证据协议可自任独立第二源无须外求真人** · 跨 vendor 强模型不得当 Layer-2 终审
(SOTA 无背书)· 红线(`gold_layer2.evaluate_layer2` 首个 guard)保留 · 降级口径(Layer-1 交付 + Layer-2 known-limitation);
见 §4-E1 D-7 改写块 + §7-4 + HANDBACK-LOG 第 26 条 + `forge/v1/stage-forge-009-pM3prime-v1.md`。
v0.5 2026-07-19 回写 handback `009-pM3prime-20260718T143324Z` 决议:**E1 真普查
完成**(102 records · 0 truncation = KG-40 根治实证)· strong 密度 {US: 40, CN: 1, HK: 0} ·
operator 弱锚抽查后终裁 **E2 密度前提 per-market 化:US 成立 · CN/HK STOP**;见 HANDBACK-LOG
第 25 条。
v0.4 2026-07-18:KG-40 契约阻断**已解除**——forge v6「引文回锚制」落地(XenoDev commit
76036af · 993 passed · codex 18 轮 R18 approve)· operator **授权重跑 E1 真普查**;见
HANDBACK-LOG 第 24 条。
v0.3 2026-07-17:E1 真密度普查 **blocked-by-KG-40** 状态注记 · proposer 契约裁定走 forge 009
专场;见 HANDBACK-LOG 第 23 条。
v0.2 同日:密度口径 per-market + 阈值 30/stratum 签 advisory 语义;见 HANDBACK-LOG 第 22 条)
**Created**: 2026-07-16
**Source**: forge stage-forge-009-v5.md(§Next-version PRD draft + §Decision matrix + §dev plan)+ discussion/009/forge/v5/xenodev-alpha-assets-snapshot.md
**Approved by**: human operator(2026-07-16,forge v5 Decision menu [A] · **只授权 E0+E1**)
**PRD-form**: phased
**Phases**: [E0, E1]
**Phase-current**: **E1 · 代码全 ship,但 E1 验收未达成 —— 按 §6 停止条件「停」**(2026-08-12 回填 ——
此前一直 stale 停在 `E0`,从未随进度更新)。
⚠ **「代码 ship 完」≠「phase 通过」,本字段刻意不写成 complete**:E0 + E1 两 phase 的
task(T001-T013)**全部 build-ship**(1209 passed · 无待做 task),E1 三件交付物里
**密度普查数字 ✅**(US 40 条 strong 超 advisory 阈 30 → 分市场终裁 US go / CN·HK STOP · 第 25 条)、
**`record_tickers` 判定 ✅**、但 **金标两层 ❌** —— **Layer-2 在 v0.1 CLOSED**(三前提全塌 · 见 §4-E1 块 (p) ·
HANDBACK-LOG 第 33 条)、**Layer-1 从未处置**(门槛仍空 + 四项契约缺角未补 · 见 §4-E1 块 (n))。
§6 对 E1 的停止条件原文是「**金标任一层不过 → 停,不谈回测**」⇒ 本 fork 处于**诚实停止**状态,
**E2/E3 解锁三条件在 v0.1 不会齐**。这是 forge v5「最小证伪链」预期的合法结局之一
(§6 E0 停止条件原话:「证伪链的用途就是允许诚实停止」),不是烂尾、也不是待续。

> **本 PRD 的血缘与定位**:009 集合体经 forge v1-v4 收敛并 ship M1(PIT 价格层)+ M2(alpha
> 评估机器,由 fork 009-pForge 交付,743 passed)。2026-07-16 operator 亲述事实修正:该分析师
> **不产显性荐股 call**,信号只以隐性形态存在 → forge v5(full,8 rounds,converged)裁定
> **M3'(信号提取头)提前成立,以最小证伪链推进**。本 fork = 证伪链的**前两站 E0+E1**。
> 权威全文见 `discussion/009/forge/v5/stage-forge-009-v5.md` +
> `discussion/009/operator-input-2026-07-16-implicit-signals.md`。

---

## 0. 定位(关键 · 防 V4)

**009-pM3prime 本 fork 的交付物 = 证伪链前两站(E0 口径预注册 + E1 密度普查/两层金标),
不是完整提取管线,更不是蒸馏系统。**

- **只授权 E0 + E1**。**E2(历史窗先导)/ E3(forward 确证线)显式 defer 到本 fork 之外**——
  gate 在 E1 的两个真数字:密度普查结果(vs 预注册阈值)+ 金标两层验收结果。数字经 hand-back
  交回 IDS,operator 看数决定是否另行授权 E2/E3。build runtime 把 E2/E3 做进来 = 越界 = BLOCK。
- **密度 gate 判定语义 = per-market**(2026-07-19 终裁 · HANDBACK-LOG 第 25 条):「真密度
  显著」按 market 各自判定,**不要求全域齐过**——真普查读数 per-market 分化(US 超阈 ·
  CN/HK 真稀疏)证明全域单一判定会把 US 的有效密度误杀在 CN/HK 的语料结构性稀疏里。E2 若
  获授权,评估范围限于密度前提成立的 market(当前 = US);CN/HK 补语料后可另启普查再议。
- 每站独立可用:E0 完成 = 有了可审计的"疑似信号"定义与拒绝口径(即使 E1 不跑也是资产);
  E1 完成 = 知道"这条路值不值得继续投"(密度+提取器可靠性两个真数字)。
- forge v5 §underweights 明示:**整个 M3' verdict 的 ROI 锚点(语料密度)从未实测,E1 就是
  去实测它的**——本 fork 的本质是花最小代价买最关键的信息。

## 1. Problem / Context

M2 交付了"能算分析师 alpha 的机器",但 07-07 probe + 07-16 事实修正证实:机器**没有也永远
不会有**显性 (ticker, direction, date) 输入——该分析师的信号以隐性形态散落在盘前/盘中/盘后
笔记与直播转写里(只言片语甚至暗示)。评估问题因此变为"分析师隐性信息 × 提取方法"的
**联合假设**:回测差时无法区分"分析师无 alpha"与"提取方法烂"。

E0+E1 是拆开联合假设的第一步:先定义"什么算一条可评估疑似信号"(E0),再实测语料里有
多少条、提取器是否可靠(E1)。**不过这两关,任何回测都是自欺。**

## 2. Users

单人自用 operator。懂算法/自动化/数据,不懂投资。自用不商业化。
009 实际要造"学会他怎么看盘"的解读器,回测是解读器的考官(operator 原话血缘见
operator-input 文档 §1)。

## 3. Core user stories

- 作为不懂投资的 operator,我要一份**可审计的疑似信号口径**:什么样的笔记/直播片段算
  "一条可评估疑似信号"(ticker/方向/时点/出处),什么样的太模糊必须 typed rejection——
  不 best-effort 猜(CXO Guru Grades 行规:vague→exclude)。
- 作为容易自欺的 operator,我要在投入回测**之前**知道两个真数字:① 语料能提出多少条
  合格疑似信号(密度 vs 预注册阈值);② 提取器过不过金标(span 抽取 + 可交易映射两层)。
- 作为要诚实的 operator,我要普查阈值**先写下再普查**(预注册),防止看到数字后移动球门。

## 4. Scope IN(本 fork 只授权这些)

### E0 · 口径预注册(证伪链第一站)
- **疑似信号口径文档**:定义"一条可评估疑似信号"的构成要件——ticker(或可无歧义映射到
  ticker 的标的指称)/ 方向(long/short 语义)/ 时点(published_at 即权威时间基准)/
  出处引文(原文锚定)/ 置信。口径按版本管理(**口径版本 = trial ledger 记账维度之一**)。
- **提取层 rejection taxonomy**:对齐 M2 join 七类拒绝的精神(歧义默认拒绝),定义提取层
  的 typed rejection 枚举(如:sector-only 无标的 / 无方向语义 / 无时点 / 纯理念-心理按摩 /
  多标的不可拆 / 反讽-引用他人观点等——具体枚举 E0 定)。
- **预注册密度阈值**:普查前先写下"多少条算够"(按**分市场**最低样本量推算,参照 M2
  walk-forward 与 DSR 显著性所需 trial 数)。写入本 PRD 附录后不得回改。
  - **口径裁定(2026-07-17 handback 决议 1)**:密度计数 = **per-market · horizon-independent**。
    一条疑似信号在提取时**结构上无 horizon**(horizon 是 E2 回测窗选择,非提取属性),按
    per (market, horizon) 计数会把 1 条信号 fan 进 3 个 horizon 桶 = 假独立证据(review HIGH#1
    已修,XenoDev 实装与本口径对齐)。
  - **已签阈值(2026-07-17 handback 决议 2)**:**每 stratum(= market)30 条**
    (threshold_hash=97c58440426f8770 · 反推自 M2 walk-forward 18/3/3 + min_trials<20)。
    **语义 = advisory 参考阈值**:普查照常输出「过/不过参考线」的诚实 verdict,留事前预期
    记录(防事后挪标准);但**非自动毙刀** —— E2 go/no-go 由 operator 依完整密度报告
    (per-market 明细/拒绝构成/密度分布)人工拍板,不由阈值机械触发。阈值数字本身仍受
    §7-5 不可回改约束。
- **疑似信号 schema 定稿**:`extracted_signals`(ticker / 方向 / 时点=published_at /
  出处引文 / 置信 / 提取器版本 / 口径版本)+ `extraction_rejections`(typed)+
  `trial_ledger`(提取器变体 × 口径版本 × horizon)三表 DDL——**009 自有表,不写 004
  生产三表**(不污染其语义、不撞 UNIQUE(week_id, source_id))。

### E1 · 密度普查 + 两层金标(证伪链第二站 · 首要 ROI 站)
- **语料密度普查**:对 collection.db(9,081 条:article 1,179 / qa 7,545 / replay 转写 357,
  published_at 秒级)按 E0 口径普查可提取疑似信号密度,产出真数字与预注册阈值对比。
  顺带**查明 record_tickers 表(777 行)语义**(采集侧弱关联/标题命中/已消歧候选三选一),
  决定提取头 ticker 解析的复用/校验/重建。
  - **⚠ 状态(2026-07-17 · blocked-by-KG-40 · handback 决议 · HANDBACK-LOG 第 23 条)**:
    首次真 LLM 密度普查(DeepSeek · 温度 0 · JSON mode · sample 200)被 proposer prompt
    契约缺陷系统性阻断——prompt 要求 LLM 产原文**字符偏移**(span_start/end),推理型模型
    在长语料下烧爆输出预算,56/58 条 finish_reason=length 截断 + 0 成功 span。**真密度读数
    不成立**(既非 below 也非 meets threshold,是工具契约缺陷;census `llm_parse_failures>0`
    守门正确拦下「截断假 0」,未误判 STOP)。两条候选修法(①改产逐字文本片段 + 下游
    `str.find` 回锚 vs ②分块喂)均动引文锚定契约(§7-3)= spine 级 → **裁定走 forge 009
    专场**(议题含 `llm_parse_failures` 守门固化为 proposer 强制不变量),契约定稿 +
    XenoDev 改线后方可重跑。**E2/E3 解锁第一条件(真密度显著)持续未满足。**
  - **✅ 解除(2026-07-18 · KG-40 阻断已解 · handback 决议 · HANDBACK-LOG 第 24 条)**:
    forge v6 verdict「引文回锚制」四条款落地(XenoDev commit 76036af):LLM 只产逐字引文
    quote(不产偏移 · 不回填 published_at),偏移由 `anchoring.py` 确定性分层回锚
    (exact→normalized→fuzzy 审计层);occurrence 消解经 R16 熔断裁决按契约「证不出用 DP」
    分支切 DP(单一归一坐标候选表 · 位置序分配)。census_invalid 硬门 + 三类失败计数
    (上条决议 3 的护栏)已固化为 typed 契约。993 passed · codex 18 轮 adversarial-review
    R18 approve。**operator 已授权重跑真普查**(重跑前确认 DEEPSEEK key 就位;读数 =
    exact+normalized 硬下界 + fuzzy 分层另报 + weak_anchor 率人工终裁)。真密度读数产出前,
    **E2/E3 解锁第一条件(真密度显著)仍未满足**——解锁判定以重跑读数为准。
  - **✅ 完成(2026-07-19 · E1 真普查读数 + operator 终裁 · HANDBACK-LOG 第 25 条)**:
    新契约重跑(sample-size 40 × 3 form · DeepSeek v4-flash · 温度 0 · prompt_v2):102
    records 处理 · **0 truncation · 三类失败计数全 0**(vs 07-17 旧契约 58/58 全截断)=
    KG-40 根治实证,census_invalid 硬门未触发,**读数有效**。**strong 密度 = {US: 40,
    CN: 1, HK: 0}** vs advisory 阈 30/stratum · verdict=below_threshold_advisory(CN/HK
    触发)但 US 超阈(+10)= per-market 分化非全域稀疏。拒绝构成:sector_only 175(语料
    特性主因)· unanchorable_citation 13 · no_direction 4;fuzzy 率 1/42 极低。IDS 侧弱锚
    抽查(29 条语义弱锚逐条切原文核验):build 自报 83% 含 5 条小写 ticker 误计
    (mu/amd/mrvl/hood/rddt 实为真锚)→ 真语义弱锚 71%;~23/29 为真隐性信号(「老黄/
    达子」→NVDA ·「美光」→MU ·「谷子」→GOOGL · ASR 转错「新一生」→300502 等)=
    **M3'「隐性信号可被口径捕捉」假设首次正面实证**;可疑过度联想仅 6 条可定位(ETF 权重
    枚举簇 ×5 + sector→name ×1),最保守全毙 US 40→34 **仍 > 30**。**终裁:「真密度显著」
    per-market 判定——US 成立 · CN/HK 不成立(真稀疏 · 分市场 STOP · 补语料后可另启普查)。**
    E2/E3 解锁三条件中**第一条件对 US 已满足**;第二条件(两层金标)仍未满足(待真人第二
    标注源,见 §4-E1 金标);E2 正式授权仍需三条件齐 + operator 另行授权,范围限 US market。
- **金标两层验收**(两层全过才允许未来进回测;operator 可当标注者之一,**不单独终审**——
  需第二标注源 + 分歧仲裁):
  - **层 1 · span 抽取验收**:疑似信号语句有没有被找到(Krippendorff α + span P/R/F1,
    数值门槛实现时预注册);
  - **层 2 · 可交易映射验收**:sector/ticker/方向/horizon/时点映射对不对(映射级一致率)。

  > **⚠ D-7 改写(2026-07-23 · forge 009-pM3prime v1 verdict · HANDBACK-LOG 第 26 条)**
  > **Source**: `discussion/009/009-pM3prime/forge/v1/stage-forge-009-pM3prime-v1.md` §Next-version PRD draft
  > (Reviewer A=Claude Opus 4.8 · B=GPT-5.6-Sol xhigh · strong-converge · converged · 无 unresolved)。
  >
  > **背景**:E1 US 密度 go 后推进 Layer-2 撞 frozen PRD **§2(单人不懂投资)× 本节 Layer-2 金标(D-7 原要
  > 领域独立真人第二源)互斥** → Layer-2 无合格验收主体 → 诚实 STOP。forge 经两组零论文重叠的正交 SOTA
  > (Nine Judges 跨 vendor 错误相关 φ=0.6 · Correlated Errors 350+ 模型 60% 同错 · 人 n_eff 是 LLM 2 倍 ·
  > AmbER 长尾别名共享流行度先验 · FActScore/SAFE 独立性来自外证据锚定非品牌)收敛出下述改写。
  >
  > **① D-7 新措辞(替换「Layer-2 用真人第二标注源」的独立性理据)**:
  > > Layer-2 gold 的第二源**不得以模型家族 / provider 异源作为独立性代理**。合格第二源须**独立于提取器
  > > 盲标**(不先看提取器输出)、**以可追溯外部证据作答**、并**通过任务内校准**(含长尾/歧义样本)。独立性靠
  > > **外部证据锚定 + 任务内盲测逐维双错率**证成,**不靠来源品牌 / 领域深度**。`human`(**含 operator 本人**,
  > > 若独立于提取器且遵循证据协议)是当前可执行的独立性默认;跨 vendor 模型未经任务内校准不得替代 Layer-2
  > > 终审。**无法判断须 abstain;冲突未仲裁不得通过。**
  >
  > **② 验收铰链四条**(挂在 Layer-2 定义下):
  > 1. **外证据锚定**:每个判断绑定外部证据与来源;事实维度(ticker/交易所)由权威知识源核验。
  > 2. **盲测校准前置**:资格启用前完成含长尾/歧义样本的盲测校准集(直击 AmbER 冷门别名 2 倍误取)。
  > 3. **逐维双错率报告**:按 5 维(sector/ticker/direction/horizon/timepoint)报告双错率 + abstain +
  >    覆盖率;可接受门槛**预注册**(§4-E0 OQ-1 精神:先写下再测)。
  > 4. **人审歧义 + 仲裁留痕**:歧义/方向/时点维度必须人(operator 或加强复核者)审;冲突保留仲裁链;
  >    未闭环 fail-closed。
  >
  > **③ §2 × 本节 Layer-2 金标 关系澄清(消 handback「无验收主体」死结)**:
  > - **非产品级真互斥**:operator「不懂投资」**不阻断**独立第二源 —— 要的是**独立性,非领域深度**。
  > - 冲突仅「**当前资源下 Layer-2 全量验收暂不可满足**」→ 给降级口径:**Layer-1 span 一致性可交付 +
  >   Layer-2 标 known-limitation**;operator 过证据协议校准后解锁全量。
  > - **operator 可自任独立第二源 · 无须前置外求真人**;外部真人**不是 v0.1 前置门槛**,当 operator 尾部
  >   校准不过线 / abstain 覆盖不足 / 同类歧义持续复发时,再评估升级引入领域标注者(可选加强)。
  >
  > **④ 红线保留(不动)**:第二 LLM 直接当 Layer-2 终审 = V4 失败模式;
  > **锚(无行号 · KG-45)**:`gold_layer2.evaluate_layer2` 的**首个 guard** · 常量 `_HUMAN_SOURCE_KIND` ·
  > 回归测 `test_should_reject_when_second_source_not_human`(`second_source_kind != 'human' → raise`)**保留**。新增「外证据锚定辅助」仅作用 **Layer-1**(窄义 (a))。
  > 以后若任务内数据证明某种证据锚定模型达到**预注册的逐维独立性门槛**,可重审其 Layer-2 资格,但
  > **不得按 provider 品牌直接放行**。
  >
  > **⑤ 三条 v0.2 待解**(实装前解 · 见 forge stage §What this menu underweights):逐维双错率可接受阈值
  > 具体数字 · 「外证据锚定」用哪个权威知识源核验 ticker(受红线约束不引入 look-ahead)· operator 自任第二源
  > 时技术上如何保证「独立于提取器」(标注 UI/流程隔离 · 主路最脆弱技术假设)。

  > **🔴 D-7 v2 修订(2026-07-27 · forge 009-pM3prime v2 verdict · HANDBACK-LOG 第 29 条 · operator 选 [C] 局部接受)**
  > **Source**: `discussion/009/009-pM3prime/forge/v2/stage-forge-009-pM3prime-v2.md`
  > (Reviewer A=Claude Opus 4.8 · B=GPT-5.6-Sol xhigh · strong-converge · converged · 无 unresolved)。
  > **本块优先于上方 v1 改写块**;v1 原文保留仅供追溯,其 ①③ 的关键结论已被下述 (a)(c) 撤销。
  >
  > **背景(前提塌陷)**:2026-07-27 operator 自陈**对金融新闻 sector / direction / horizon / timepoint /
  > ticker 五维均无领域判断力**(非投入不足,是能力问题)→ v1「operator 可自任独立第二源」的落地前提由本人推翻。
  > 注:该事实**并非新信息** —— `risks.md` E1-R2 下游注(2026-07-23)已载「operator 无合格金融判断」,
  > 且该文件在 v1 的 X 清单内;v1 读过并将其重新解释掉。故本轮性质是**裁决 v1 的推论**,非处理新事实。
  >
  > **(a) 撤销 v1「operator 可自任 Layer-2 第二源」推论**。断裂点是一次**范畴替换**:v1 由
  > 「`mapping_agreement_rate()` 不含金融逻辑」推出「标注不需领域深度」—— 但该函数是**比较器**(只做 `==`),
  > 标注劳动在于**五元组怎么产生**;且 v1 用以支撑的「事实维可外证据核验」**只覆盖 ticker 与 timepoint 两维**
  > 〔**⚠ 2026-07-28 订正:这句本身是错的 —— 实为一维。见下方「两维 lane 撤销块」**〕,
  > sector / direction / horizon 三维无任何外锚。**错误独立性解决「两方不共享盲点」,不产生真值。**
  > → **KG-42「无验收主体」死结并未真解,只是被 D-7 挪了位置**;HANDBACK-LOG 第 27 条「KG-42 死结解」判定**作废**。
  >
  > **(b) 撤销 07-25 gold 协议作为 validity 依据的地位**。`gold`=operator 考据版 / `human`=operator 盲标版
  > 是**同一人两次标注**,按 Krippendorff 信度三分类(stability / reproducibility / accuracy)
  > **只测 stability,不测 validity**。该数字**在测量理论上不是对 machine 映射正确性的验收**。
  > 作为 stability 记录可保留,**不得当 validity 用**。(v1 的契约缺角:D-7 草案详写 human 资格,
  > 却从未定义 **gold provenance**,而双错率恰是相对 gold 定义的 —— 判据悬空。)
  >
  > **(c) 全量五维 Layer-2 作为「correctness gold gate」在 v0.1 判定不成立**,
  > **且不因换主体、不因调门槛而成立**。v1 ③「§2 × Layer-2 金标 **非产品级真互斥**」的判断
  > **在 correctness 维度上撤销** —— 它**就是**真互斥:产品定义(单人自用·不懂投资)与验收要求
  > (五维映射正确性)在 v0.1 不可同时满足,是**能力与 validity 锚的结构问题**,不是资源问题。
  >
  > **(d) E2 解锁条件 ② 拆为两条**(见 §7 E2/E3 解锁条件同步修订):
  > - **②-a 诊断 lane**:可产**开发证据**(口径校准 / failure 分类 / 提取器变体比较)。
  > - **②-b 回测 lane**:历史窗回测需 correctness 验收过 → **v0.1 明确 blocked(非「待跑」)**,
  >   原因是**缺 validity 锚**而非缺劳动。
  > - **⚠ 反自欺条款**:②-a 过**不得**被记作条件 ② 满足。任何文档把降级结果表述为「两层金标过」
  >   = 口径漂移,须回 hand-back。
  >
  > **(e) 候选降级面 = groundedness · 本次 [C] 决议下【挂起,不予采纳为既定验收面】**。
  > forge v2 verdict 提出把 Layer-2 验收对象由 **correctness**(映射对不对 · 需领域判断)降级为
  > **groundedness**(**被引原文是否真支撑该五元组** · 只需阅读理解),且 009 引文回锚基础设施
  > (`raw_ref`/`span_start`/`span_end`)已就位。**operator 选 [C]:该面暂不写入 PRD 作为验收面**,
  > 解锁前置 = **零成本效力探针**须先证明其在 **n≈41 上具备区分力**
  > (forge §underweights 自曝:groundedness 的统计效力**两边都没算**;correctness 侧「41 条 × 门槛 0.05
  > → 约 2 条错即翻盘」的问题换成 groundedness 后原样存在)。探针出数字后另行决议是否采纳。
  > **若采纳,硬边界必须同时写死**:groundedness 过 **≠** 映射正确 **≠** 有 alpha **≠** 授权回测。
  >
  > **(f) 门槛形态修正判据**(采纳 · 跨场景通用):**看数后下调既有阈值数字 = 移动球门(禁);
  > 换形态 + 新 `caliber_version` 预注册 + 废止旧 pass 语义 = 方法学修正(可);形态改亦不得
  > retroactively 解锁旧 gate。** 具体:Layer-2 固定逐维 coverage 阈是方法学上过时形态
  > (标准形态为 risk-coverage 曲线 / AURC)—— 但**本次不改数字**,形态重注册待 (e) 决议后一并做。
  >
  > **(g) 红线保留(不动)**:第二 LLM / 跨 vendor 未校准模型当 Layer-2 终审 → raise
  > (锚:`gold_layer2.evaluate_layer2` 首个 guard · 常量 `_HUMAN_SOURCE_KIND` · **无行号** · KG-45)。
  > gate fail-closed 骨架不动。E1 US 密度结论(第 25 条)不动。
  >
  > **(h) 未处置项(v0.2 note · 见 forge v2 stage §v0.2 notes)**:① Dorner & Hardt 变体比较路径
  > (v0.2+ · **带前置验证义务**:须先证 operator 标注噪声与真值**正相关**,该假设在三解释维未经检验且可能为假)
  > · ② partial identification 界宽在 n≈41 未验 · ③ **Layer-1 主体问题全程未处置**(门槛仍空 · 同样 blocked-on 真盲标)
  > · ④ 「operator 慢考据 gold 是否可产」方法学上无解,只能靠外锚绕开而外锚仅覆盖两维
  > 〔**⚠ 2026-07-28 订正:「两维」实为一维,且该一维对主要错误模式无齿。见下方撤销块**〕。

  > **🔴 两维外锚 lane 撤销块(2026-07-28 · handback `009-pM3prime-20260728T035015Z` · HANDBACK-LOG 第 31 条)**
  > **Source**: build 侧零成本合成探针 `two-dim-anchor-probe.py`(exit 0)+ **IDS 侧独立复跑与闭式验算**。
  > **本块优先于上方 (a)/(h)④ 中关于「外锚覆盖两维」的一切表述**;原文保留仅供追溯。
  >
  > **(i) 「两维外锚 lane」撤销 —— 前提是事实错误。** HANDBACK-LOG 第 30 条曾据 forge v2 §134
  > (「事实维可外证据核验只覆盖 ticker(watchlist 外锚)与 timepoint(`published_at`)两维」)立过一条
  > **两维 gate lane** 分支。该前提**不成立**,两条独立理由各自足以否掉它:
  > - **① `published_at` 不是外锚,是管线恒等。** 项目自己的 frozen `SLA.md` Layer-2 逐维门槛表
  >   **timepoint 行「外证据锚」列写的就是「无」** —— forge v2 与其相矛盾。链条:`published_at` 读自
  >   collection.db `records` → census 原样传入 → LLM 被 `_V2_FORBIDDEN_FIELDS` **结构性禁产**
  >   (即便带 `null` 也算 schema drift)→ 引文制强制 `content_pub = published_at` 显式忽略 LLM 值 →
  >   回填进 `extracted_signals.published_at`。**IDS 侧跨库 join 真 collection.db(9,081 条)实证:
  >   41/41 逐字节相同 · 不同 0 · 缺失 0。** 拿它核 machine 的 timepoint 是 `X == X`,**不可能失败,
  >   因此不可能发现任何提取错误**。⇒ 「两维」实为**一维**。
  > - **② 剩下那一维对主要错误模式无齿。** ticker 外锚核的是「这是不是一个合法上市符号」,**不是**
  >   「这是不是这篇文章的符号」。探针 C 组:machine 把每条 ticker 都换成 watchlist 内**别人的** ticker
  >   (相对 gold 逐条 100% 错)→ 两维判据**仍 100% 通过**(IDS 独立复跑复现)。而「张冠李戴到另一个
  >   真实标的」正是 **silent-wrong-number**,后果最重的那一类。
  >
  > **(j) 形态天花板(KG-44)** —— 即便退一步只用 ticker 一维:区间/置信下界形态 `1/(1+z²/n)` 下,
  > n=41 天花板 `0.93810` ⇒ **τ ≥ 0.94 数学不可达**;按真盘簇结构做 Kish 修正
  > (`m_A = Σm²/Σm = 189/41 = 4.6098` → `n_eff = 8.894`)天花板降至 **`0.76676`** ⇒ **连已冻结的
  > 0.90 都不可达**。点估计形态下 τ=0.90 也只容 **4 条 miss**,而单个 ticker 最大簇 = 10/41 = 24.4%
  > —— **一个 ticker 在窗内退市就能吃光全部容错预算**。(IDS 闭式独立验算全部吻合。)
  > ⚠ **本块不提任何门槛数字**;门槛预注册仍属 C6 范畴。
  >
  > **(k) 锚方向不掉转。** 现行 `_compute_ticker_anchor` 核的是 **gold** 的 ticker。`gold → machine`
  > **不是纯加严**(gold miss 而 machine 命中时覆盖率反升),且撞 frozen spec §O8 D-3 注块 ⑥ 与 SLA
  > 里「只核 gold 的 ticker」这句**实质论断** ⇒ **非 build 可自决**。若日后要保留该能力,形态应为
  > **`gold ∧ machine`**(纯加严 · 与 lane 是否采纳解耦)。
  >
  > **(l) ⚠ 明确不暗示 E2 可解锁。** 两维 lane 即便成立也**不验 direction**(交易信号最核心维);
  > 本轮结果**比该预期更差**。**桌上仍然没有任何一条路能解开 E2**;②-b 回测 lane 维持 **blocked**。
  >
  > **(m) Layer-1 结论收窄(与 build 建议不同 · 不整体采纳)。**
  > - **41 条盲标机会不得用作 recall 抽样框、不得走 `evaluate_layer1`。** 理由是**抽样框结构性错误**
  >   而非样本量:41 条 = machine **已接受**的输出,以其为 gold 框 ⇒ `gold ⊆ pred` ⇒
  >   `span_recall = |gold∩pred|/|gold| ≡ 1.0` **恒真**,与提取器漏了多少完全无关 —— 而 O7 要测的正是
  >   recall。**这与 KG-43/KG-44 同族:一个数学上不可能给出坏消息的判据。**
  > - **危害集中在「走 `evaluate_layer1`」**:该函数把 P 与 R 和**同一个** `prf_threshold` 做 AND,
  >   而 gate 只读 `passed` ⇒ recall≡1.0 那半边假数会写进审计表并让 gate 以为两项都过。
  >   ⚠ **Layer-2 有代码级硬闸(授权常量恒 False),Layer-1 没有对应硬闸 —— 它是两道门里软的那道。**
  > - **但保留其 precision 框地位**:precision **无对偶退化**(实测 `gold ⊊ pred` 时
  >   0.25/0.5/0.75/1.0 完全可证伪),且**恰恰是杀死 recall 的那个读法让 precision 成立** ——
  >   gold = 判为真的那些 machine span,逐字节同源 ⇒ exact-match 天然满足 ⇒ `precision = |真|/41`
  >   **就是接受集的假阳性率**。故 build「Layer-1 不需要那 41 条」**过宽,不采纳**;
  >   **41 条是目前唯一已物化的 span precision 框。**
  > - **build「必须重跑提取器烧 key」的成本论断不成立**:存在**零 LLM 成本的正确 recall 框** ——
  >   在**已普查的 102 条记录**上抽样标 gold,pred = **已物化的 41 个 accepted span**;14 源之外
  >   每条记录贡献 0 个 pred span,在 accepted-span 定义下这是**正确**不是缺失 ⇒ `recall ∈ (0,1)` 可证伪。
  > - 🔴 **但换框治不了根因**:`span_prf` 是 **exact-match** 口径(差 1 字符即 0 分),独立标注的 gold
  >   偏移几乎不可能逐字符命中 ⇒ recall 波动来自**边界抖动**而非漏检。**根因是判据形态,不是语料** ——
  >   须先决定放宽匹配(overlap / IoU)或改**句子级单元**。**这是 KG-43「数字 vs 形态」在 Layer-1 的同族实例。**
  >
  > **(n) Layer-1 契约缺角(冻结门槛前必解 · 治理层)**:① α 的 **unit 与 label 空间**从未定义
  > ② **`pred_spans` 的定义**从未写下(算「已接受信号的 span」还是含「已定位但被口径拒的 span」?
  >   —— 后者的偏移在 census 阶段被主动丢弃,`extraction_rejections` 无 span 列)
  > ③ `evaluate_layer1` / `krippendorff_alpha` **无任何生产调用方**(全仓仅测试触及 · `gold_layer1_result` 0 行)
  > ④ **无 frame-type 守卫**(没有任何东西阻止把一个恒真框喂进去)。
  > **在这四项写清楚之前不得冻结 Layer-1 门槛**,否则重蹈 KG-43「冻结了一个没定义清楚的门」。
  >
  > **(o) 盲标资源与泄露面(须知悉)**:41 条盲标机会**全程未拆封**。但 `blind/worksheet.txt`
  > **含 `span_start`/`span_end` 且被 git 追踪**,而 `.gitignore` 的豁免注释断言它「不含任何答案」——
  > **Layer-1 的金标就是 span**,该豁免只考虑了 Layer-2 的五元组 ⇒ **Layer-1 的 span 独立性设计上已破**
  > (KG-47)。缓解事实:该 commit **未 push 到任何 remote**,暴露面**只限本地**。
  > ⚠ 另:`blind/machine.json` **不含 span 偏移**(只有五维)⇒ 那 41 条作为已封装制品
  > **是 Layer-2 映射资源,不是 Layer-1 span 资源**。
  >
  > **(p) 🔴 41 条 Layer-2 金标路 = v0.1 CLOSED(2026-08-12 · HANDBACK-LOG 第 33 条 · 撤销块 (o)
  > 「Layer-2 映射资源完好」的隐含前提)**:块 (o) 判 Layer-1 span 独立性已破、Layer-2 五元组资源尚存。
  > **后半句现已被 IDS 侧实证推翻。** 三个独立前提同时不成立,任何一条都足以关闭该路:
  >
  > | # | 前提 | 状态 | 据 |
  > |---|---|---|---|
  > | ① | **合格第二源** | ❌ 未解 | KG-42。forge v1 的「operator 可自任」已被 forge v2 撤销(范畴替换),此后无替代主体 |
  > | ② | **盲标隔离** | ❌ **已实质失效** | 见下方泄漏账 |
  > | ③ | **时序不变量** | ❌ 结构性不可满足 | `_blind_annotated_strictly_before_machine` 是 `criteria_met` 的 AND 分量;41 条提取于 2026-07-18,D-7 协议 2026-07-27 才实装 ⇒ 诚实填 `--machine-extracted-at` 必挡。谎报即「看到数字后移动球门」 |
  >
  > **泄漏账(逐条核过 `blind/machine.json` 答案键,非推演)**:HANDBACK-LOG **第 25 条**
  > (2026-07-19 · IDS 侧弱锚抽查 · operator 读过并据此终裁 US go)把机器答案按 worksheet 的
  > **同一套标识**写进了正文——「src=60232 簇 ×5(KO/PG/PM/PEP/MO)」= worksheet id 35–39 答案集合
  > **精确命中**;「id=5 → MU」= worksheet id 5 **精确命中**;「him=Walmart → WMT」= id 40/41 命中;
  > 另有 6 条具名映射(老黄/达子→NVDA · 美光→MU · 谷子→GOOGL · coke→KO · 新一生→300502)按原文 span
  > 可回溯,5 条小写 ticker(mu/amd/mrvl/hood/rddt)字面即答案。合计 **≈19/41(46%)** 可直接或近似还原,
  > 泄漏面已扩散到 **6 份 IDS 文档**(含本 PRD 与 forge v1 三件)。
  >
  > **⚠ 泄漏通道 = 治理散文,不是 DB / 文件。** 既有红线检查(`extracted_signals` checksum · 四张 gold 表 0 行 ·
  > `blind/` 零改动)**全部只守 DB 与文件通道**,对散文通道零覆盖 —— 故泄漏在 3.5 周、跨 8 条决议里无人察觉,
  > 且每条决议都在如实报告「41 条全程未拆封」(该断言在它自己的口径内成立,口径本身漏了一个通道)。
  > 框架面归 **KG-52**(forge 006 攒批)。
  >
  > **为什么是 CLOSED 而不是 blocked**:即使三前提全部补齐,v0.7 (c) 已冻结「全量五维 Layer-2 作为
  > correctness gate 在 v0.1 判定不成立,且不因换主体、不因调门槛而成立」,代码落成
  > `_CORRECTNESS_GATE_AUTHORIZED_V0_1 = False` 恒假 ⇒ `passed = criteria_met and False`。
  > **拆封的最好结果只是一行取证记录,解锁不了任何东西。** 继续为它补前置 = 为已冻结为不成立的终点投工。
  >
  > **重开条件(三条 AND · 缺一不得重开)**:① KG-42 有真解(具名的合格第二源,不是代理指标)
  > ② 走**全新批次**且**先盲标后提取**(唯一能诚实满足时序关的顺序;当前 41 条不可复用)
  > ③ v1.0 显式授权 correctness gate(即 `_CORRECTNESS_GATE_AUTHORIZED_V0_1` 翻真的前置论证成立)。
  >
  > **不受影响(逐条声明,防过度收缩)**:E1 US 密度终裁(第 25 条)不动 —— 它是 advisory 人工终裁,
  > 不依赖金标;②-a 诊断 lane 的挂起状态不动;Layer-1 结论收窄(41 条 = 唯一已物化 precision 框)
  > 不动 —— 但注意 Layer-1 用法**不需要盲标**,不受本块关闭影响;`gate.py` fail-closed 骨架与
  > FU-HB32 的 DB 迁移 / schema 前置守卫**保留**(它们修的是「landed≠生效」,与拆封与否无关)。

- **E1 hand-back**:密度数字 + 金标两层结果 + record_tickers 判定,经 hand-back 交回 IDS,
  operator 决定 E2/E3 授权与否。

## 5. Scope OUT(显式 non-goals · build 做进来 = 越界 = BLOCK)

- **E2 历史窗先导回测** —— defer 到本 fork 之外,gate 在 E1 两个真数字。
- **E3 forward 确证线** —— 同上 defer。(两级证据制语义已由 forge v5 定死:历史窗=开发证据、
  forward=唯一 alpha 确证,E2/E3 授权时直接继承,本 fork 不实现。)
- **蒸馏技能**("学会他怎么想"/自给自足)—— 远期 OUT(防 V4;提取头只做"显性化他说了什么")。
- **时序异质图谱** —— 维持 defer。
- **自动交易 / 改 004 纪律壳** —— OUT(两灵魂分居下游,红线 #1/#9)。
- **改 M2 评估端语义 / M2 join 七类拒绝契约放松** —— OUT(量尺 keep;join adapter 属 E2 前置,
  本 fork 不做)。
- **写 004 生产三表**(advisor_reports / strategy_signals / watchlist)—— OUT(§4 schema 决议)。
- **008 采集端改动** —— OUT(只读消费 collection.db;raw 文件只读)。

## 6. Phased roadmap(committed = E0+E1 · E2/E3 列出仅为路线完整)

- **E0 · 口径预注册**(预估 S):口径文档 + rejection taxonomy + 预注册阈值 + 三表 DDL。
  停止条件:定不出可审计口径 → 停,回 IDS 重估(证伪链的用途就是允许诚实停止)。
- **E1 · 密度普查 + 两层金标**(预估 M):普查数字 + record_tickers 判定 + 金标两层 + hand-back。
  停止条件:密度 < 预注册参考阈值 → 产 STOP verdict(insufficient_sample 诚实记录)并
  hand-back,**E2 go/no-go 由 operator 依完整密度报告终裁**(阈值 advisory 语义,见 §4-E0);
  金标任一层不过 → 停,不谈回测。
- ~~E2 历史窗先导~~ / ~~E3 forward 确证线~~ —— **不在本 fork**,gate = E1 数字 + operator
  另行授权(密度 gate **per-market**:US 已过 · CN/HK STOP,见 §4-E1 2026-07-19 注记
  ⚠ **该 STOP 的理由已于 2026-08-13 改判 —— 见本节末双态块**;金标两层仍未过,三条件未齐)。

  > **🔴 E2/E3 解锁条件修订(2026-07-27 · forge v2 · HANDBACK-LOG 第 29 条 · [C])**
  > 原「解锁三条件」中的**条件 ②(两层金标过)拆为两条**,状态分别判定:
  >
  > | 条件 | 内容 | 状态(2026-07-27) |
  > |---|---|---|
  > | ① 真密度显著 | per-market | **US ✅**(第 25 条终裁)· CN/HK ❌ STOP ⚠ **2026-08-13 改判为双态,见本节末「条件 ① 的 CN/HK 改判」块** |
  > | **②-a 诊断 lane** | 产开发证据(口径校准 / failure 分类 / 变体比较) | **⏸ 待定** —— 候选降级面 groundedness 在 [C] 下**挂起**,须先过效力探针(见 §4-E1 D-7 v2 修订块 (e)) |
  > | **②-b 回测 lane** | 历史窗回测,需 **correctness 验收过** | **🔴 v0.1 明确 blocked(非「待跑」)** —— 缺 validity 锚,非缺劳动;**不因换主体或调门槛而解锁** |
  > | ③ operator 显式授权 | — | ❌ |
  >
  > **⚠ 2026-08-12 增补(第 33 条)**:②-b 所依赖的 correctness 验收,其**唯一已物化载体**
  > (41 条盲标机会)现已判 **v0.1 CLOSED**(三前提全塌 · 见 §4-E1 **块 (p)**)。即 ②-b 的状态
  > 从「blocked-待 correctness 验收」实际变为「**v0.1 内无路径可产生该验收**」。
  > **这不改变 ②-b 的结论(仍 blocked),改变的是它的性质** —— 从「等一件没做的事」变成
  > 「等一件 v0.1 内做不成的事」。**任何文档不得把「补齐拆封前置」表述为 ②-b 的解阻路径。**
  >
  > **→ E2 不授权。** E2 历史窗回测 / E3 forward 线做进 XenoDev = 越界 = **BLOCK**(不变)。
  >
  > **⚠ 反自欺条款**:②-a 过**不得**被记作条件 ② 满足;任何文档把降级验收结果表述为
  > 「两层金标过」= 口径漂移,须回 hand-back。
  >
  > **⚠ Layer-1 未处置**:Layer-1 门槛仍空、同样 blocked-on 真盲标跑,其主体问题**本轮未审**
  > (forge v2 v0.2 note ③)。不得默认 Layer-1 已解。
  >
  > **⚠ 2026-07-28 增补(第 31 条)**:Layer-1 现已**部分立案但仍未解**,状态见 §4-E1
  > **两维 lane 撤销块 (m)/(n)**。要点:41 条**不得用作 recall 框、不得走 `evaluate_layer1`**
  > (`gold ⊆ pred ⇒ recall ≡ 1.0` 恒真),但**是唯一已物化的 precision 框**;
  > **根因是 `span_prf` 的 exact-match 形态,换抽样框治不了**;
  > **α 的 unit/label 空间、`pred_spans` 定义、frame-type 守卫四项缺角未补前不得冻结 Layer-1 门槛**。
  > **Layer-1 无代码级硬闸(不同于 Layer-2 的授权常量)—— 它是两道门里软的那道。**

### 🔴 条件 ① 的 CN/HK 改判 —— 双态(2026-08-13 · forge v3 verdict (d) · `OB-009-pM3prime-v3-06`)

> **旧判「CN/HK 真稀疏」作废。执行结论不变,理由被换掉了。**

| 市场 | **执行态**(要不要投入) | **认识态**(我们知道什么) | 依据 |
|---|---|---|---|
| **US** | **go**(不变) | **已知密度足够** | 40 / 73 / 65 **三次读数均 > 阈值 30**,方向稳健 —— **不是当初判错** |
| **CN** | **`STOP`**(不变) | 🔴 **`UNKNOWN`**(原为「真稀疏」) | 三次读数 **1 / 0 / 2**;总量只差 3% 时 CN 却在 0↔2 间跳 |
| **HK** | **`STOP`**(不变) | 🔴 **`UNKNOWN`**(原为「真稀疏」) | 三次读数 **0 / 0 / 4**;总量只差 3% 时 HK 从 0 变 4 |

**为什么执行态不撤销**:`STOP` 现在的含义是 **measurement-invalid 下的 fail-closed** ——
既然读数不可信,就没有任何**正面证据**支持投入。撤销 `STOP` 会隐含「CN/HK 值得重开」,
而那需要正面证据,我们没有。**不投入的默认仍然正确,只是它的理由变了。**

**为什么认识态必须改**:原判「CN/HK 真稀疏」是一个**关于世界的事实断言**,
而它建立在**一次读数**上,且 **per-market 恰是噪声最大的那一层**
(总量读数同日方差 3%,而 per-market 读数在 0↔4 之间跳)。
⇒ 该事实断言**没有证据支持**,必须撤回。

**旧理由失效证据**:PREREG §10.5「决定性实验」三次读数对照表 + 分市场噪声一节。

**科学重判触发条件(三者需同时满足)**:
1. 提取稳定性的**申报机制已落地**(见 §7 红线 3 改形态块)且**每个拟重判市场**均产出**可解释的**
   per-market 跨次一致性读数
2. **该市场**的 per-market 读数**噪声量级**已被测出,且**小于**该市场的密度阈值裕度
   —— **逐市场成立,不得以任一市场的满足代替另一市场**
3. operator 显式授权重判 —— **不得由任何自动化流程或 agent 自行认定条件已满足**

> 🔴 **条件 1/2 量词改写(2026-08-16 · forge 009-pM3prime v5 · `OB-009-pM3prime-v5-04`)**
>
> **旧文「至少一个 per-market 读数」作废。** 旧条件 1 是**存在量词**,而条件 2 是**特定量词**
> (「**该市场**的密度阈值裕度」)⇒ 两者不一致:US(40 / 73 / 65)能满足旧条件 1,
> **却对 CN/HK 的重判零信息**,而要重判的恰是 CN/HK 的 `STOP`。
> ⇒ **字面满足不算满足。** 该判定**由本仓量词冲突独立成立,不靠任何外部标准背书**
> (forge v5 P3R2 检验:把 NCHS 比例呈现标准的精确档位直接移植属**过度外推**)。
>
> ⚠ **同时改写「条件 2 不可计算」的诊断**:它**不是数据缺**,是**同一 pipeline 的两条链分层粒度不同**
> —— `census.py` 的密度链**逐 market 判**(`meets_threshold` / `below_threshold_advisory` 以 market 为键),
> 而 `aggregation_probe.py` 的一致性链**零 market 轴**(全文仅 `:744` 一处注释,`_run_batch` 无 market 维;
> IDS 与 Codex **两侧独立复证**)。⇒ **改措辞补不出来,必须新建 market 观测轴**
> (BCBS 239:**分层可得性是汇总能力定义的一部分** —— forge v5 十二个参照体系中
> **唯一**被判「忠于原体系」的跨界引用)。承接义务 `OB-009-pM3prime-v5-10`,
> `due_gate: xenodev:task-review` ⚠ **该 gate 未接线,`exposure` 已登记**。
>
> **前身**:v4 的「条件 1 未满足注记」(T015 产出的是**全局**读数 `J_1 = 0.4078` / `J_agg = 0.6885`,
> 结果矩阵零 per-market 分解)**结论仍然成立且被本条吸收** —— 但其归因由「分解还没做」
> 改为「**两条链的分层轴不同**」。v4 当时不做的理由是**判据膨胀(程序性)**,不是它不重要;
> v5 判定该拖延**已到期**。
>
> ⚠ **不得据此松动任何执行态**:CN/HK 执行态 `STOP` 不变、认识态 `UNKNOWN` 不变;
> 扩样与 E2 **继续 blocked**;C6 冻结门槛**数字**未改;41 条盲标路**仍 CLOSED**。

⚠ **范围纪律(承 forge v3 Y 视角约束)**:本条的理由**只许来自科学效度**
(单次读数能否支撑一个 STOP 裁决)。**不得诉诸市场价值、商业优先级或「CN/HK 值不值得做」**
—— forge v3 的 Y 视角**未选产品价值**,该维度本轮未审,不得借本条夹带。

⚠ **反自欺条款**:任何文档不得把 `UNKNOWN` 表述为「CN/HK 已确认有信号」,
也不得把 `STOP` 继续表述为「CN/HK 真稀疏」。**两个方向的漂移都是漂移。**

### 低样本市场的显式状态(2026-08-16 · forge v5 · `OB-009-pM3prime-v5-04`)

per-market 读数**不足以支撑判断时,必须显式报状态** —— 不得留空,也不得用全局读数顶替。

| 状态 | 含义 | 当前落点 |
|---|---|---|
| **可用** | 该市场读数可解释,可进入条件 1/2 判定 | US(40 / 73 / 65) |
| **复审** | 读数存在但可解释性存疑 ⇒ 交**具名判定人**裁,裁决留痕 | 暂无 |
| **`not_estimable`** | 样本量不足以产出可解释读数 ⇒ **明报不可估** | CN(1 / 0 / 2)· HK(0 / 0 / 4) |

🔴 **只给形态,不给数字。** 本表**不设样本量阈值** —— forge v5 P3R2 检验判定:
把外部统计标准的精确档位/阈值直接移植属**过度外推**,可移植的只有
「**分市场判 + 低样本显式状态 + 具名判定人**」这一形态(承 forge v2「数字 vs 形态」判据)。
**判定人 = IDS operator-chair**,**不得由自动化流程或 agent 认定**(同条件 3)。
⚠ **`not_estimable` 不是 `STOP` 的新理由,也不是撤销 `STOP` 的理由** —— 它只报「测不了」,
执行态与认识态均不因本表变动。

### 🔴 跨批读数的消费契约(2026-08-16 · forge v5 · `OB-009-pM3prime-v5-06` / `-07`)

> **谁在何时读、读到什么必须停 —— 本节是 `census_run` 表的唯一消费者定义。**
> 在本节之前,该表**每跑落一行,却没有任何环节读它**。

**消费者** = **IDS operator-chair**。指派须**书面 + 本人正式接受**,并留工作底稿
(形态参照 PCI DSS 10.1.2「标准不指定职位,而要求 entity 书面指派且本人正式接受」
+ PCAOB AS 1301「具名接收主体 + 双向沟通 + 留工作底稿」)。

**时点** = 每次 `/handback-review`,**在引用任何跨批次失败率 / 密度 / 一致性读数之前**。

**动作** = 枚举相关 `census_run` 行;**命中以下任一即停止该结论与验收签署**:

1. 库不可读;
2. 被引用的那次跑**没有对应行**;
3. **删失未披露**;
4. 同 `caliber` 下 `declared_sample_size` 变化,而**无预注册的选择规则**。

⚠ **已知未验,不得静默降级**:forge v5 P1 §3 自曝**不确定** `/handback-review` 能否在
**不改 `framework/SHARED-CONTRACT.md`** 的前提下承载硬停点。若实测证不能,本节**降级为 v0.2 +
登记 exposure**,**不得当作已生效**。另:`census_run` 与被引用 batch 的**可机械关联性**
(是否只能靠 variant 文本匹配)**forge v5 未解决** —— 若不可靠,第 2 条判据不可执行。

⚠ **承接义务** `OB-009-pM3prime-v5-06` / `-07`,`due_gate: ids:handback-review`
⚠ **该 gate 不在 `framework/obligations/README.md` §接线状态表内** ⇒
**接线之前,本节只能靠 operator 每次自己记得** —— 这是敞口,不是保障。

## 7. BLOCK 级硬约束(§8 契约测试须覆盖 · forge v5 verdict 定死)

1. **trial ledger**:提取器变体 × 口径版本 × horizon 全部记账(E1 期间试过的每个 prompt/规则
   变体都算 trial,未来 DSR/PBO deflate 的分母)。漏记 = BLOCK。
2. **文本 PIT**:提取只可使用 published_at ≤ 信号时点的内容(负例测试:构造"未来内容已入库"
   场景断言提取不到)。
3. **引文锚定 + 提取稳定性**:每条疑似信号必须附原文出处(可复核);温度 0 / 提取器版本化。

   > **🔴 2026-08-13 改形态(forge v3 verdict (b) · `OB-009-pM3prime-v3-04`)—— 原文
   > 「同文本同版本必须同输出(一致性测试)」作废。**
   >
   > **作废理由(不是放松要求,是去掉一个不可满足的要求 + 一个假绿信号)**:
   > - **原理上不可满足**:T=0 非确定性的主因是推理引擎 kernel 缺 **batch invariance**
   >   (服务端负载 ⇒ batch size ⇒ 归约顺序;实测 1000 次 T=0 补全出 **80 个不同结果**,
   >   换 batch-invariant kernel 后 1000/1000 相同,代价 ≈2×)。**修复位点在推理引擎内部**,
   >   我们是第三方 API 消费者,够不着;且 **DeepSeek 官方 Chat schema 无 `seed`、无任何
   >   可复现性承诺**,`system_fingerprint` 只表示后端配置。
   > - **它此前从未被真正检验,却一直给正信号**:契约测 `test_same_text_same_version_same_output`
   >   把 proposer 换成 `literal_ticker_proposer`(构造上确定)⇒ **命题恒真**;
   >   另一半 `test_should_call_deepseek_with_temperature_zero_and_json_mode` 只断言
   >   **参数被传给 API**。⇒ **红线的两半各自被测,红线本身落在缝里,而这条缝产出的是绿。**
   > - **实测反证**:同日同参两跑,按 `(source_id, ticker, direction)` 去重后 **Jaccard 仅 0.44**。
   >
   > **替代形态(承 forge v2「数字 vs 形态」判据:这是改形态,不是挪数字)**:
   >
   > **提取稳定性 = 强制测量 + 申报 + 落库 + 身份绑定,`pass_semantic: none`。**
   > - **必须测**:每批普查须产可复核的跨次一致性读数,不得省略
   > - **必须申报**:读数进产物,不得只留在跑者的终端里
   > - **必须落库**:与该批语料同库,可 `SELECT`
   > - **必须绑身份**:`system_fingerprint` / `service_tier` / 语料内容哈希
   > - **`pass_semantic: none`** —— **不设 pass/fail 阈值**。文献不给阈值与最少 N
   >   (Atil 10 次 / NER 最多 30 次,均非普适下限),而我们**已经看过 0.44 这个数**,
   >   此刻自定 τ 落在 forge v2 判过的「看数后动门槛」阴影里。
   > - ⚠ **`report-only` ≠ `optional`** —— 上述四个「必须」是硬的,只是它们**不阻断**。
   >
   > **升级路径(唯一合法路径)**:将来若要设门禁,**必须升 `caliber_version`**,并在
   > **看相关结果之前**预注册口径、阈值、适用模型与校准样本。**升级判据不得是次数**
   > (承 forge 006 v10:「复发 ≥N 次」型判据全部作废)。
   >
   > 🔴 **`convert` 判据形态定形(2026-08-14 · forge 009-pM3prime v4 · `OB-009-pM3prime-v4-06`)**
   >
   > 上一段只说了「必须升 `caliber_version` + 看结果前预注册」,**没说凭什么判定可以升**。补齐如下 ——
   > **`report-only` → 门禁的 convert 判据 = 四者合取,缺一不可**:
   > 1. **过程证据** —— 有一段真实的观察期,且期内**审阅过真实误杀**
   >    (ModSecurity:「Every Ruleset can have false positives in new environments」,故 DetectionOnly 先行);
   > 2. **结果证据** —— per-market 噪声量级已测出且**小于该市场的密度阈值裕度**(即 §6 科学重判条件 2 的形状);
   > 3. **具名批准** —— 具名主体签署,不得由自动化流程或 agent 认定;
   > 4. **版本化回退** —— convert 前必须已具备可回退形态(见下)。
   >
   > ⚠ **只给形态,不给数字。** 三个独立工业先例(OPA Gatekeeper · Chrome/Blink · Kubernetes KEP)
   > **无一给出数字阈值**;Chrome 原文:「**There is no threshold for which removal is necessarily safe**」,
   > 改为规定过程量(最少观察期 / Deprecation Trial / 跨引擎协调)。
   > ⇒ **看完结果再定数字 = 移动球门**(承 forge v2「数字 vs 形态」判据 + 本文 §7 (f))。
   >
   > 🔴 **版本化回退语义(`OB-009-pM3prime-v4-07`)**:**历史不可变;授权被后续 `caliber_version` supersede。**
   > 回退 = 再升一个**新** `caliber_version`,**只撤销旧版的未来消费权**;
   > 旧阈值、旧证据、当时的裁决**永久保留可查**。**不得**表述为「旧结论作废」——那暗示追改历史,违反 C6。
   >
   > ⚠ **已知未处置(v4 §underweights 6)**:四要件中的「**具名批准**」在本仓**只有一个人** ——
   > operator-chair 与提出 convert 的是同一个人。前三项可机械化,**唯独批准的独立性无法靠机制保证**。
   > **这与 KG-42(无合格第二源)同族**,断面从「标注的第二源」换成「**批准的第二源**」。
   > **不得假装 Kubernetes KEP 的 PRR 批准形态可直接移植** —— PRR 的独立性来自组织,本仓没有组织。
   >
   > **本条已登记为 warn**:`framework/warn-registry/registry.jsonl` →
   > `WARN-c4-extraction-stability-report-only`(`warn_class: temporary` ·
   > **`due_event: forge:006:phase0`** · **已接线**)⇒ 下一次该 gate intake 必须三态裁决。
   > ⚠ **2026-08-14 三态裁决 = `defer`(operator-chair 签署)**,`due_event` 由
   > `forge:009-pM3prime:phase0` 改指 `forge:006:phase0`。**改指理由不是就近**,而是机制缺陷:
   > `validate-warn-class.sh` 的到期判据**不看是否已裁决**,而 fork 域唯一接线的消费 gate 就是当前 gate
   > ⇒ 指回它即刻再到期、指向 `v<N>:phase4` 则永不被消费 ⇒ **fork 域 `temporary` warn 的 defer 在当前机制上不可表达**。
   > 该缺陷已随本 warn 带进 forge 006。**已知代价 = 场地错配**:fork 域语义在框架场裁,裁决者需 009 上下文。
   >
   > 🔴 **校准监测周期 —— 载体等级裁定 = `codified`,正文落点即本节**
   > **(2026-08-16 · forge 009-pM3prime v5 · `OB-009-pM3prime-v5-02`)**
   >
   > v4 定形的内容此前**只存在于 `framework/obligations/ledger.jsonl` 的一个 `evidence` 字段里**
   > (IDS 2026-08-14 现场 grep:PRD / `spec.md` / `SLA.md` 三处**全零命中**)。v5 裁定其载体等级为
   > **`codified`**,内容如下:
   > - **每个被消费的批次**必测必落库;
   > - 身份 / 口径变化(模型 · `system_fingerprint` · 语料批次 · `caliber_version`)**立即启动新基线**;
   > - **XenoDev 产证,IDS operator-chair 接受基线与升版。**
   >
   > ⚠ **载体等级是被裁定的,不是默认的。** 三种合法取值:`codified`(入正文)/ `note`(留账本 + 挂映射)/
   > **`explicitly-uncodified`(显式裁定不入正文,仍然合法)**;三者都必须**显式、可发现、可消费**。
   > 🔴 **不预设「三处镜像」** —— 该预设动作已被 forge v5 decision matrix #10 裁掉;
   > `spec.md` / `SLA.md` 是否同步**由等级裁定结果决定**,不是默认动作。
   > 🔴 **不强制固定三级标签** —— forge v5 P3R2 检验判「必须采用固定三级标签」属**过度外推**
   > (法典编纂先例只支持「未编入正文仍可合法且保持映射」);上列三值是**本仓当前取值**,非外部强制。
   >
   > **「v4 当时为什么没写」的答案已被 forge v5 P2 推翻并改写**:原解释「义务登记动作顶替了回写动作」
   > **不成立**(适航标准:**无父需求的要求是一等公民**,只要带 rationale + 强制反馈边 + 独立复审)。
   > 真正的病 = **ledger 行没有反馈边、没有复审主体、也从未被裁定载体等级**。
   >
   > 🔴 **统计型重校准间隔 —— 三态,每态各绑方法**
   > **(2026-08-16 · forge v5 · `OB-009-pM3prime-v5-03` / `-05`)**
   >
   > **「历史足量后再做」这一静默态即日删除** —— 它在本仓已被反复证明**等于消失**。
   > 每个被消费批次必须产以下三态之一,**没有第四种沉默走法**:
   >
   > | 状态 | 允许方法 | 已知敞口 | 退出证据 |
   > |---|---|---|---|
   > | `insufficient_history` | 自启动 / 归一化图族(Q-t · Z-MR · DNOM)——**专为零历史 start-up 设计** | 🔴 **必载**:自启动图前 ~50 点有 **masking 风险**,须配 retrospective 复核 | 累积到预注册方法的适用前提成立 |
   > | `method_ready` | 预注册的方法与口径(**看结果之前**注册) | 方法自身的适用边界须随读数一并申报 | 产出可复核读数并落库 |
   > | `recalibration_due` | 同上;触发后**必须**重跑基线 | 旧基线在新基线被接受前**不得**继续背书新批次 | operator-chair 接受新基线与升版 |
   >
   > 🔴 **不看现数造 N**(承 forge v2「数字 vs 形态」判据):转态由**预注册方法的适用前提**决定,
   > **不得**在看过当前读数之后回头定样本量。文献口径是「低于 ~20–25 子组**换方法**,而不是等」
   > ⇒ **「等数据够」不是一个合法状态。**
   > ⚠ **只给状态机而不绑方法 = 退化成「有状态无内容」的记账对象 —— 那正是本轮诊断的病灶本身。**
   >
   > **同步三处,漏一处即仍有假绿源**:本条(IDS PRD)· `$XENODEV_ROOT/specs/009-pM3prime/spec.md` C4 ·
   > 同目录 `SLA.md` E1「提取确定性」行。
   > ⚠ **本行的「三处同步」是 forge v3 对红线 3 改形态的既有裁决,适用范围仅限该改形态**;
   > 它**不构成**对上方 `-04` / `-05` 两块的镜像预设(见 matrix #10)。
   >
   > 详见 `forge/v3/stage-forge-009-pM3prime-v3.md` §Verdict (b) + §Verdict rationale。
4. **金标 gate**:未过两层金标,`extracted_signals` 不得流向任何回测消费方(mutation-killer:
   移除 gate 断言应致测试失败)。**Layer-2 第二源资格红线(2026-07-23 · forge v1 · 见 §4-E1 D-7 改写 ④)**:
   第二 LLM 直接当 Layer-2 终审 = V4 = BLOCK;`second_source_kind != 'human' → raise` 保留
   (**锚:`gold_layer2.evaluate_layer2` 首个 guard · 常量 `_HUMAN_SOURCE_KIND` · 回归测
   `test_should_reject_when_second_source_not_human` · 不写行号 · KG-45**);
   外证据锚定的模型辅助仅可作用 Layer-1,越界进 Layer-2 终审 = BLOCK。
5. **预注册不可回改**:密度阈值在普查开始后修改 = BLOCK(记录在案的口径/阈值变更须走
   hand-back 决议)。

## 8. Success looks like(可观测 · anti-PPV)

- **E0**:口径文档 + rejection taxonomy + 预注册阈值入库(版本化);三表 DDL + migration 就绪;
  终点是**可 SELECT 的口径/阈值记录**,不是"文档写完了"。
- **E1**:`extracted_signals` / `extraction_rejections` / `trial_ledger` 里有**真行**(普查产出);
  密度数字 vs 预注册阈值的对比结论;金标两层的真实验收数字(α / P/R / 映射一致率);
  record_tickers 三选一判定;一份 hand-back 包把上述数字交回 IDS。
- **反 PPV**:终点是真数字/真拒绝行,不是"提取器 demo 跑通"。

## 9. Real constraints

- 单人自用不商业化;operator 不懂投资(工程强项补短板)。
- 语料:collection.db 2025-06-16 → 2026-07-07(9,081 条,capture 完整,replay 已转写;
  转写有噪声,提取需鲁棒)。只读消费。
- 跨仓:E0/E1 落 XenoDev build runtime;IDS 只产 hand-off(per SHARED-CONTRACT §6)。
- **窗口纪律**:operator 记忆中"有用"的时段(25 年底–26 年初存储主线)**保留为未来 OOS
  sanity check,E0/E1 的口径开发与金标标注避开优先使用该窗口**(防把答案抄进考卷)。
- LLM 提取涉及成本:E1 普查可先抽样分层(实现细节),但抽样方案须预注册。

## 10. UX principles

- 每条疑似信号可点开看原文出处(引文锚定,operator 可复核提取对不对)。
- 拒绝行同样可审计(为什么这条被拒、落哪个 taxonomy)。
- 评估叙事 = "检验私域分析师是否是例外":不默认 alpha,也不因公开 pundit 均值差预判死刑。

## 11. Open questions(forge v5 也没解决 · E0/E1 落地要盯)

1. **金标两层具体数值门槛**(α 精确值 / span P/R 下限 / 映射一致率):实现时**预注册**,
   原则已定死(有门槛 + 两层全过才放行)。
2. **record_tickers 语义**:E1 查明前不得当已消歧数据用。
3. ~~**密度阈值具体数**~~ → **已决(2026-07-17)**:30/stratum · per-market · advisory 语义
   (threshold_hash=97c58440426f8770),operator 经 handback 决议签字,详见 §4-E0 口径裁定。
4. **LLM 提取器的权重面 look-ahead**(parametric look-ahead bias):E0/E1 期间影响有限
   (金标对照的是人工标注非未来收益),但 E2 授权评估时必须重新正视;cutoff 早于语料期的
   对照模型为可选加固。
5. **EQM 解释质量评分**:可选旁支(廉价预筛/蒸馏远期素材),不进主链;operator 若想升主链
   另起 forge。
6. **口径 v2 迭代候选(2026-07-19 抽查产出 · 非本轮缺陷 · 不 rollback 读数)**:两类过度
   联想样本已定位——① ETF 成分权重枚举 → 逐股个股信号(src=60232 簇 ×5:枚举成分 ≠
   逐股荐买);② 板块词 → 单一 ticker(「美存储」→MU)。下轮口径版本迭代时并入 rejection
   判据(口径版本 = trial ledger 记账维度,变更须记账,§7-1/§7-5)。
