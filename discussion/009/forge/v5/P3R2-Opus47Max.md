# P3R2 · Opus side · finalize(forge v5 · 009 · strong-converge)

**Reviewer**: Opus(主进程)
**Phase**: 3R2(已读对方 P3R1;convergence_mode = strong-converge)
**Date**: 2026-07-16

---

## §1 · 我对每条分歧的最终立场 + 让步

**分歧 1(历史窗证据地位)— 全盘接受对方精化**。采纳其验收语义词汇表:**历史窗 = 开发
证据**(合法用途:口径发现、failure case 分类、power analysis、提取器校准),**forward =
确证证据**(唯一 alpha 背书路径)。我 P2 的"假设生成"表述并入"开发证据"一词,后续所有
草案沿此词汇表。这不是我让步立场,而是对方把我的二分从"贬历史窗"修正为"给历史窗定岗"——
更对。

**分歧 2(CXO 硬币基线)— 全盘接受**。基线语义定为:operator 体感归零、从硬币/naive
baseline 起跑、叙事 = "检验一个私域分析师是否是例外";同时**禁止因公开 pundit 均值差而
提前杀死实验**(基线是起跑线不是判决书)。双向约束都写进 verdict。

**分歧 3(金标验收范围)— 全盘接受,这是 R1 最有价值的精化**。金标包拆两层:
**层 1 · span 抽取验收**(疑似信号语句有没有被找到:α≥0.667 + span P/R/F1)、
**层 2 · 可交易映射验收**(sector/ticker/方向/horizon/时点映射对不对:映射级一致率
门槛)。**两层全过才许进回测**;operator 可当标注者之一,**不单独当终审**(需第二标注源 +
分歧仲裁)。对方对我 P2 口径的这个扩展,正面回应了双方 P1 各自的第一不确定点。

对方 R1 的条件句("若 R2 无法把证据层级和金标门槛写成硬约束 → alpha claim 判 BLOCK")
——本轮 §2 verdict 即把两者写成 BLOCK 级硬约束,条件解除。

## §2 · 联合 verdict(单一 · strong-converge)

**M3'(信号提取头)提前成立,以"最小证伪链"形态推进;它是 008 语料与 M2 评估机器之间
缺失的器官,008→004 通用桥不另设,07-07 smoke path 决议正式 supersede。**

证伪链五站,每站带停止条件,fail = 诚实停止(提取头产物仍为可复用资产):
**E0 口径**(定义"一条可评估疑似信号",vague→typed rejection,预注册密度阈值)→
**E1 普查+金标**(语料密度普查;金标两层验收:span 抽取 + 可交易映射,两层全过才进回测)→
**E2 历史窗先导**(证据地位 = **开发证据**:口径/提取器校准、failure 分类、power analysis)→
**E3 forward 确证线**(采集-即提取-封存-事后对账,**唯一 alpha 确证路径**,常设化)。

**BLOCK 级硬约束(进 next-PRD)**:① trial ledger 扩到提取器变体×口径版本×horizon,
全部计入 DSR/PBO deflate;② 文本 PIT(提取只可用 published_at ≤ 信号时点的内容);
③ 引文锚定(每条疑似信号必须附原文出处)+ 提取稳定性(温度 0/版本化/同文本同输出);
④ 两级证据制与两层金标门槛按上述语义执行;⑤ M1/M2/004 零改动,蒸馏技能("学会他怎么想")
与图谱维持远期 OUT。评估叙事 = 硬币基线起跑、检验例外、不预判生死。

## §3 · 残余分歧降级 v0.2 note

- **EQM 解释质量评分**:收为可选旁支(廉价预筛 + 蒸馏远期素材),不进 M3' 主链、不作
  alpha 证据。对方 R1 未再争,若其 R2 异议则升回决策项。
- **金标两层的具体数值门槛**(α 精确值、映射一致率、P/R 下限):原则定死(有门槛+全过
  才回测),数值留 XenoDev 实现校准。
- **record_tickers 语义**(复用/校验/重建):E1 普查站顺带查明,三选一留实现。
- **密度"够/不够"的数值线**:预注册原则定死(普查前先写下阈值),具体数进 PRD 草案再由
  operator 拍。
- **cutoff 早于语料期的对照模型**:forward 线为主后降为可选加固,不作硬要求。

## §4 · W 形态产出的初步草稿建议(给 synthesizer)

- **verdict-only**:§2 全文即是,可直接收录。
- **decision-list**:保留(M1 PIT 层/M2 统计机器/O8 evidence 台面/004 纪律壳零动)·
  调整(蒸馏 M4 排期→拆分:提取头 M3' 前置、技能蒸馏留远期;评估叙事→例外检验;金标→
  两层制;历史窗→开发证据定岗)· 删除(07-07 smoke path、独立 008→004 搬运桥)·
  新增(提取头器官、证伪链 E0-E3、三条纪律红线、forward 封存线、提取层 rejection taxonomy)。
- **next-PRD**:M3' 骨架 —— PRD-form=phased,Phases=[E0+E1(口径/普查/金标),E2(历史窗
  先导),E3(forward 确证线)];IN=证伪链五站;OUT=蒸馏技能/图谱/自动交易/改 004/改 M2
  评估端语义;疑似信号 schema 要素(ticker/方向/时点/出处引文/置信/提取器版本/口径版本);
  物化路径倾向 **009 自有表**(extracted_signals + extraction_rejections + trial_ledger),
  经 adapter 进 M2 join,**不写 004 生产三表**(不污染其语义、不撞 UNIQUE(week_id,source_id));
  §8 契约测试含:文本 PIT 负例、trial ledger mutation-killer、引文锚定断言、两层金标 gate。
- **refactor-plan**:按模块 —— 008 采集面(零动,只读消费)· collection.db(E1 查明
  record_tickers)· 009 新增三表(上述)· M2 join(加第二输入源 adapter,七类拒绝契约
  不松)· 004(零动)。
- **next-dev-plan**:E0→E3 milestone 各带停止条件与验收口径;E3 常设化含"内容到达即
  提取封存"的调度钩子;先导窗口纪律(operator 记忆中的存储主线时段仅作 OOS sanity check,
  开发/调参用其他时段)。
