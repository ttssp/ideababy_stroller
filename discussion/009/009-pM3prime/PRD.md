# PRD · 009-pM3prime · "M3' 信号提取头 · 最小证伪链(E0+E1 期)"

**Version**: v0.1
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
- **预注册密度阈值**:普查前先写下"多少条算够"(含分市场/分 horizon 的最低样本量推算,
  参照 M2 walk-forward 与 DSR 显著性所需 trial 数)。写入本 PRD 附录后不得回改。
- **疑似信号 schema 定稿**:`extracted_signals`(ticker / 方向 / 时点=published_at /
  出处引文 / 置信 / 提取器版本 / 口径版本)+ `extraction_rejections`(typed)+
  `trial_ledger`(提取器变体 × 口径版本 × horizon)三表 DDL——**009 自有表,不写 004
  生产三表**(不污染其语义、不撞 UNIQUE(week_id, source_id))。

### E1 · 密度普查 + 两层金标(证伪链第二站 · 首要 ROI 站)
- **语料密度普查**:对 collection.db(9,081 条:article 1,179 / qa 7,545 / replay 转写 357,
  published_at 秒级)按 E0 口径普查可提取疑似信号密度,产出真数字与预注册阈值对比。
  顺带**查明 record_tickers 表(777 行)语义**(采集侧弱关联/标题命中/已消歧候选三选一),
  决定提取头 ticker 解析的复用/校验/重建。
- **金标两层验收**(两层全过才允许未来进回测;operator 可当标注者之一,**不单独终审**——
  需第二标注源 + 分歧仲裁):
  - **层 1 · span 抽取验收**:疑似信号语句有没有被找到(Krippendorff α + span P/R/F1,
    数值门槛实现时预注册);
  - **层 2 · 可交易映射验收**:sector/ticker/方向/horizon/时点映射对不对(映射级一致率)。
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
  停止条件:密度 < 预注册阈值 → 停(insufficient_sample 诚实路径);金标任一层不过 → 停,
  不谈回测。
- ~~E2 历史窗先导~~ / ~~E3 forward 确证线~~ —— **不在本 fork**,gate = E1 数字 + operator 另行授权。

## 7. BLOCK 级硬约束(§8 契约测试须覆盖 · forge v5 verdict 定死)

1. **trial ledger**:提取器变体 × 口径版本 × horizon 全部记账(E1 期间试过的每个 prompt/规则
   变体都算 trial,未来 DSR/PBO deflate 的分母)。漏记 = BLOCK。
2. **文本 PIT**:提取只可使用 published_at ≤ 信号时点的内容(负例测试:构造"未来内容已入库"
   场景断言提取不到)。
3. **引文锚定 + 提取稳定性**:每条疑似信号必须附原文出处(可复核);温度 0 / 提取器版本化 /
   同文本同版本必须同输出(一致性测试)。
4. **金标 gate**:未过两层金标,`extracted_signals` 不得流向任何回测消费方(mutation-killer:
   移除 gate 断言应致测试失败)。
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
3. **密度阈值具体数**:E0 推算(参照 DSR 显著性所需样本量),operator 拍板后预注册。
4. **LLM 提取器的权重面 look-ahead**(parametric look-ahead bias):E0/E1 期间影响有限
   (金标对照的是人工标注非未来收益),但 E2 授权评估时必须重新正视;cutoff 早于语料期的
   对照模型为可选加固。
5. **EQM 解释质量评分**:可选旁支(廉价预筛/蒸馏远期素材),不进主链;operator 若想升主链
   另起 forge。
