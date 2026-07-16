# P1 · Opus side · 独立审阅 first-take(forge v5 · 009)

**Reviewer**: Opus(主进程)
**Phase**: 1(独立审阅 · NO search · NO SOTA)
**Date**: 2026-07-16

---

## §0 · 我读到的标的 + 阅读策略 + K 摘要

**全部 8 个 X 标的均真读**:proposal §009(proposals.md:276-315 全文)· operator-input
2026-07-16(v5 触发材料全文)· 009-pForge/PRD.md(全文,重点 §0/§4/§5/§11)·
HANDBACK-LOG.md(17 条 entry 标题全扫 + 精读 M-fork-complete 与 07-07
P2-prod-precondition-gap 两条决定性 entry)· forge v4 stage doc(全文)· XenoDev 004-pB
(真读 `feat/009-spec` 分支:join.py 全文 260 行 / evaluate `__main__.py` / realized_return.py
关键段 / alembic 0001/0010/0011 DDL)· collection.db(sqlite3 实测 schema + 分布)·
跨仓快照件(本 forge 自产,已核)。阅读策略按 Y:产品价值先读 operator-input + proposal
诉求段;架构读 join/evaluate 契约 + PRD IN/OUT 边界;工程纪律读 C16/DSR/PBO 与七类拒绝实现。

**K 摘要**:工程强项补投资短板;两灵魂分居上下游;四条核心工作;防 V4;**v5 事实修正 =
分析师不荐股、信号隐性,提取/蒸馏头从 M4 末位候选提前到关键路径,评估问题变为
"隐性信息 × 提取方法"联合假设**。

## §1 · 现状摘要(按 Y)

**产品价值**。事实修正让 009 的价值命题发生了实质迁移:原命题"这个分析师行不行"有一条
干净的证据链(显性 call → PIT 回测 → 数字);新命题在链条中间插入一个**自由度巨大的
提取层**,证据强度天然被稀释——回测差时无法区分"分析师无 alpha"与"提取方法烂"。但另一面,
修正让产品叙事更诚实:proposal 第 4 条(蒸馏技能、自给自足)本来就是 operator 的终局,
009 真正要造的是"学会他怎么看盘"的**解读器**,不是"给他打分"的评分器。M1+M2 量尺资产
(PIT 双 as_of、C16、DSR/PBO、七类拒绝)与信号来源无关,全部照用——已 build 的钱没有白花,
这点必须先钉死。语料侧地基意外地好:9,081 条、覆盖 13 个月、`published_at` 精确到秒、
replay 已转写,且 operator 体感"有用"的时段(25 年底存储主线)落在覆盖内。

**架构设计**。现状的硬 seam 在 M2 join 的输入契约:`resolve_signals` 绑死 004 三表
(advisor_reports/strategy_signals/watchlist),且**无 strategy_signals 行整条落
no_signal_date 拒**——这意味着提取头的产物必须以某种方式"物化"成这套契约能吃的形态。
两条路:(i) 伪造 004 三表兼容行(最省事,但把提取产物混进 004 生产表,污染其语义,且
UNIQUE(week_id,source_id) 是为真报告设计的);(ii) 009 自有新表(如 extracted_signals,
带 extraction_run_id / 出处引文 / 提取器版本 / 置信)+ join 层加第二输入源或 adapter。
另一个被低估的现状:collection.db 已有 `record_tickers` 表(777 行)——采集侧已存在某种
ticker 关联,提取头设计前必须先查明其语义(是标签?是提及?谁写的?),避免重复造轮子
或误信脏数据。原 M4"蒸馏 lane"的红线(只能独立 lane 化、不替人决策)依然成立——**提前的
应该只是"提取头"(显性化他说了什么),不是"蒸馏技能"(学会他怎么想)**,两者必须显式切开,
否则 M3' 会滑坡成 V4 式大工程。

**工程纪律**。M2 的统计纪律机器是现成的,但三个新泄漏面是提取层特有的:① **提取器变体 =
trial**——每个 prompt/规则版本都是一次多重检验,trial_count 记账必须从"信号"扩到
"提取器变体 × 信号集",否则 DSR deflate 失真;② **文本 PIT**——提取只能读
published_at ≤ t 的内容,collection.db 时间戳支持这一点;③ **LLM 权重面 look-ahead**
(我认为被 operator-input 低估的最大效度威胁):若提取器是 LLM,模型训练数据里"知道"
2026 年存储股涨了,提取时会被先验污染——"暗示"被解读成信号可能只是模型后见之明。缓解
方向:引文锚定硬约束(每条疑似信号必须附原文出处)、提取 prompt 禁用内容外知识、
理想情况用训练截止早于语料期的模型做对照。此外先导实验需要**窗口纪律**:operator 记得
有用的存储主线窗口只能当 out-of-sample sanity check,开发/调参必须用其他时段。

## §2 · First-take 评分(keep / refactor / cut / new)

| 对象 | 判 | 理由 |
|---|---|---|
| M1 PIT 层 + M2 统计机器(realized/DSR/PBO) | **keep** | 量尺与信号来源无关;743 passed 的既有资产 |
| M2 join"歧义一律拒绝"哲学 | **keep** | 评估端严格性不因上游模糊而放松;提取头负责显性化,join 负责把关 |
| 07-07 smoke path 决议(手工回忆显性 call) | **cut** | 前提(显性 call 存在)被 operator 亲述证伪,正式作废 |
| "蒸馏排 M4 末位"的原排期 | **refactor** | 拆开:**提取头**(显性化)提前为 M3' 关键路径;**蒸馏技能**(方法学习/自给自足)仍留远期 gated |
| M3 原内容(calibration 头/回流线) | **keep(defer)** | 与提取头正交;其 gate 条件("M2 出可信数字")现在传导为依赖 M3' |
| 提取头(008 语料→疑似信号显性化) | **new(M3' 核心)** | 产物 schema 建议:ticker/方向/时点(published_at)/出处引文/置信/提取器版本;落 009 自有表倾向 (ii),不污染 004 生产表 |
| 提取层 rejection taxonomy | **new** | 对齐 join 七类拒绝精神:提取不出/无 ticker/无方向/多义 → typed rejection,不 best-effort 猜 |
| 提取质量独立验收(gold-standard 人工标注小样本) | **new(第三条红线候选)** | 分离联合假设的唯一手段:提取器 precision/recall 先过门槛,再谈信号回测;否则"提取器烂"伪装成"分析师无 alpha" |
| trial_count 扩到提取器变体 + 文本 PIT | **new(红线)** | operator-input 已提,我背书并具体化(§1 工程纪律 ①②) |
| 008→004 通用桥(07-07 留白) | **cut(合并)** | 提取头即是桥的正确形态;不再另设机械搬运层 |

## §3 · 我现在最不确定的 3 件事

1. **语料中"疑似信号"的密度与可锚定性**:1,179 篇笔记 + 357 场直播覆盖 13 个月,能提取出
   多少条带 (ticker, 方向, 时点) 的疑似信号?几百条则 M2 统计够用,几十条则回到
   insufficient_sample。我未读语料正文,纯未知——这个数字决定 M3' 的 ROI,先导实验应
   最先回答它(先做密度普查,再做提取器)。
2. **LLM 权重面 look-ahead 的可缓解程度**:引文锚定+prompt 约束是否足以让"提取的信号"
   不被模型后见之明污染?这是方法论级威胁,若不可缓解,整个"回测提取信号"的效度存疑。
   期待 P2 SOTA 检索找先例(新闻情绪 alpha / 文本回测领域必然踩过)。
3. **疑似信号的物化路径**:(i) 伪 004 三表行 vs (ii) 009 自有表+join 适配,我倾向 (ii),
   但没有验证 join/evaluate 的改动量与 OUT-10 边界的精确归属(join.py 是 009 fork 自有物
   可改,但 evaluate 读 004 表的语义假设有多深未量化)。
