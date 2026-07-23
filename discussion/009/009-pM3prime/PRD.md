# PRD · 009-pM3prime · "M3' 信号提取头 · 最小证伪链(E0+E1 期)"

**Version**: v0.6(2026-07-23 回写 handback `009-pM3prime-20260723T082127Z`[FU-KG42] 决议 · forge
009-pM3prime **v1** verdict:**§4-E1 Layer-2 金标 D-7 改写** —— 第二源资格从「领域独立真人」refactor
为「错误独立性代理(外证据锚定 + 逐维双错率证成 · 不靠品牌/领域深度)」· **frozen §2×D-7 收窄为验收级
暂不可满足 · operator 配证据协议可自任独立第二源无须外求真人** · 跨 vendor 强模型不得当 Layer-2 终审
(SOTA 无背书)· 红线 `gold_layer2.py:81` 保留 · 降级口径(Layer-1 交付 + Layer-2 known-limitation);
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
**Phase-current**: E0

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
  > **④ 红线保留(不动)**:第二 LLM 直接当 Layer-2 终审 = V4 失败模式;`gold_layer2.py:81`
  > (`second_source_kind != 'human' → raise`)**保留**。新增「外证据锚定辅助」仅作用 **Layer-1**(窄义 (a))。
  > 以后若任务内数据证明某种证据锚定模型达到**预注册的逐维独立性门槛**,可重审其 Layer-2 资格,但
  > **不得按 provider 品牌直接放行**。
  >
  > **⑤ 三条 v0.2 待解**(实装前解 · 见 forge stage §What this menu underweights):逐维双错率可接受阈值
  > 具体数字 · 「外证据锚定」用哪个权威知识源核验 ticker(受红线约束不引入 look-ahead)· operator 自任第二源
  > 时技术上如何保证「独立于提取器」(标注 UI/流程隔离 · 主路最脆弱技术假设)。

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
  另行授权(密度 gate **per-market**:US 已过 · CN/HK STOP,见 §4-E1 2026-07-19 注记;
  金标两层仍未过,三条件未齐)。

## 7. BLOCK 级硬约束(§8 契约测试须覆盖 · forge v5 verdict 定死)

1. **trial ledger**:提取器变体 × 口径版本 × horizon 全部记账(E1 期间试过的每个 prompt/规则
   变体都算 trial,未来 DSR/PBO deflate 的分母)。漏记 = BLOCK。
2. **文本 PIT**:提取只可使用 published_at ≤ 信号时点的内容(负例测试:构造"未来内容已入库"
   场景断言提取不到)。
3. **引文锚定 + 提取稳定性**:每条疑似信号必须附原文出处(可复核);温度 0 / 提取器版本化 /
   同文本同版本必须同输出(一致性测试)。
4. **金标 gate**:未过两层金标,`extracted_signals` 不得流向任何回测消费方(mutation-killer:
   移除 gate 断言应致测试失败)。**Layer-2 第二源资格红线(2026-07-23 · forge v1 · 见 §4-E1 D-7 改写 ④)**:
   第二 LLM 直接当 Layer-2 终审 = V4 = BLOCK;`gold_layer2.py:81`(`second_source_kind != 'human' → raise`)
   保留;外证据锚定的模型辅助仅可作用 Layer-1,越界进 Layer-2 终审 = BLOCK。
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
