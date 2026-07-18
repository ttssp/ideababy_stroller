# Forge v6 · 009 · P1 · Opus47Max · 独立审阅(no search)

**Timestamp**: 2026-07-17T10:05:00Z
**Searches used**: NONE in this round.
**Visibility**: I did NOT read other reviewer's P1.
**Reviewer stance**: 审阅人 — 评判已存在物,不是 daydream。

## 0. 我读到的标的清单 + 阅读策略

- 我读了(11/11 全读 · 无跳过):
  - KG40 hand-back(`20260717T081757Z`)全文 —— 真跑事实 + 根因 + 候选①②
  - PRD v0.3 §4-E1 状态注记 + §7 五条 BLOCK + §11 OQ
  - forge v5 stage doc §BLOCK 红线 + §underweights(只读 normative 段)
  - 快照 8 件全文:census.py(病灶 `_build_extraction_prompt` L191-215 · 接线 L247-323 ·
    守门 L326-348/L558-628)· extractor.py · caliber.py · gold_layer1.py ·
    test_e1_citation_consistency.py · 0017 DDL · E1 runbook · E2-design-inputs
- **K 摘要**:E1 真密度是 M3' ROI 闸门 + E2/E3 第一解锁条件;裁定 (a) 输出锚定契约
  (b) 回锚失败语义 (c) 护栏固化条款 (d) 消费面追平清单;binding = v5 三红线不动摇
  (prompt 改 = 新变体记账)· 输出预算安全性须量化 · 模型无关 · 907 passed 资产不推翻 ·
  根治优先 · 直接指导 FU-task。
- **阅读策略**:先病灶(prompt 函数 + 失败计数链)再顺 span 偏移的每个消费面走一遍
  (extractor 守门 → caliber schema → DDL 列 → gold 计分 → 契约测试切片 → census 弱锚审计
  → runbook 操作面),对齐 K-(d) 的「不许只顺病灶」要求。

## 1. 现状摘要(按 Y 视角组织)

### 视角 A · 契约正确性 / LLM 能力贴合

现契约(census L191-215):LLM 被要求产 `span_start/span_end` = **原文字符偏移**(整数,
从 0 计),外加 ticker/direction/confidence/content_published_at,JSON object 单层封闭
(`ProposedSpanList` extra=forbid)。offsets 是唯一锚定载体:extractor `_classify_reject`
只验「界内 + 非空白切片」(L149-156),**不验切片内容与信号语义对应**——即现契约下 LLM
给个界内乱偏移也能过守门(弱锚审计 L161-179 只记不拒)。消费面全景:caliber `Citation`
存偏移(frozen)→ 0017 `extracted_signals.span_start/end` 列(CHECK ≥0/≥start)→
gold_layer1 `Span=(source_id,start,end)` **exact-match** 计 P/R/F1 → 契约测试断言
`text[start:end] == 命中片段` → census `is_weakly_anchored` 用切片做弱锚审计 → runbook §3
已显式记录「不自动 chunk(切分会破 span 偏移的原文回锚)」。**值得注意:build 侧 runbook
已先行判过候选②的核心代价**(块偏移破坏回锚语义),与 hand-back §2 候选②自述的代价一致。
`content_published_at` 由 census 注入 prompt 又要求 LLM 原样回填(L209)——LLM 输出携带一个
调用方本来就知道的常量,徒增输出预算与 PIT 篡改面(extract L98 靠它做 PIT drop)。

### 视角 B · 工程纪律 / 守门不变量

失败计数链已相当完备:finish_reason allowlist(L303)· 空 content(L307)· 坏 JSON(L317)
分类计数,`.stats` 挂 proposer 供 census 读入 report,CLI 醒目 WARN。**但有三个纪律缺口**:
① `verdict` 三态(meets / meets_unverified / below_advisory)**无法表达「读数不成立」**——
07-17 真跑实际产的是 `below_threshold_advisory` + stderr WARN,「不可信」全靠 operator 读
stderr 的自觉,CLI 仍 exit 0。hand-back 说「既非 below 也非 meets,是工具缺陷」,但代码里
**没有这个状态**。② proposer 契约(`Proposer = Callable`)对失败计数是 duck-typed 可选
(`getattr(proposer,"stats",None)`),K-(c) 要固化的不变量现在只是实现习惯,不是类型契约。
③ **trial 身份缺口**:literal 真跑与 llm 真跑都用 `--extractor-variant v1`(runbook §2),
`_EXTRACTION_TEMPLATE_VERSION="extraction_v1"` 常量存在但**未接进** variant 身份与
trial_ledger——两个不同提取器共享一个 variant id,§7-1「每个 prompt 变体都算 trial」在
身份编码层面就守不住,C4「同文本同版本同输出」跨 proposer 也不成立。另:runbook L82 说
「每 record 增量 commit」而 census L378-382 与 runbook §4 说「单原子事务末尾 commit」——
同文档自相矛盾(以代码为准:单原子,TERM 后全回滚,07-17 真跑无脏行,重跑干净)。

## 2. First-take 评分(按 Y 视角)

| Y 维度 | 倾向 | 理由(引用 §1 现状) |
|---|---|---|
| 契约正确性 / LLM 能力贴合 | **refactor → 候选①为骨架** | offsets 是唯一锚定载体但 LLM 不擅产它且守门验不了它;①把「锚定真值」从 LLM 手里收回到确定性代码(`str.find` 回锚 = 锚定即验证),输出预算随信号数而非文本长度伸缩;②让全消费面理解「块」概念且根因(LLM 数字符)未除,runbook 已判其破回锚。 |
| 工程纪律 / 守门不变量 | **refactor(三缺口都补)** | (c) 不变量固化须连带补 verdict 表达力(加「读数不成立」态或非零 exit);proposer 契约显式要求失败计数;variant 身份编码 proposer 类型+模板版本(§7-1 记账诚实性)。 |

**逐子决策 first-take**:
- **(a) 候选①,且做两个收紧**:(i) LLM 输出**删除** `content_published_at`(census 回填,
  少一个字段 + 消 PIT 篡改面);(ii) prompt 限定每 record 最多 N 条 span(输出上界可算:
  N × 引文长度上限 × token 系数 + JSON 骨架,对 4096 甚至更低都能给出量化安全论证——
  K-② 要的「不许应该够了」由此可满足)。候选②降级为「输入侧超长 record 的正交补充」,
  仅当实测有 record 超输入 context 才考虑,不做输出侧方案。
- **(b) 首现锚定 + typed rejection,复用现枚举**:`str.find` 首现 = 确定性(C4)且审计有效
  (引文是证据本体,同字面多处出现时任一处都证明「他说过这句」;span 是引用坐标非身份)。
  回锚失败(LLM 引文非逐字)→ 拒,**复用 `UNANCHORABLE_CITATION`**(语义吻合:引文不可回锚)
  ——**关键成本发现**:`ExtractionRejectionReason` 是 caliber v1 冻结物,0017 CHECK 从枚举
  导出,**新增枚举值 = 新 caliber_version = 重新预注册阈值连锁**(threshold 按 caliber 键)。
  复用现值 + `detail` 字段区分子因,可保 caliber v1 不动。是否加一层确定性空白归一(全角/
  空白差异)再 find,留 P2 找业界证据。
- **(c) 固化为三层**:proposer 契约层(任何 LLM-backed proposer 必须暴露 api/parse/截断
  分类计数)+ census 层(失败数 > 0 → verdict 必须能表达「census_invalid/读数不成立」,
  且 CLI 非零 exit,不再依赖 stderr 自觉)+ runbook 层(重跑判据引用 verdict 而非人读 WARN)。
- **(d) 追平清单(first-take)**:caliber `Citation`/0017 DDL/gold_layer1 **零改**(偏移仍是
  存储与计分通货,只是来源从「LLM 声称」变「代码回锚」);extractor 增确定性回锚步(守门
  从「验界内」升「产真值」);`ProposedSpan` 加 quote 载体(schema 改 = 本契约 diff 中心);
  census prompt 模板 → v2 + variant 身份重编;契约测试新增「切片 == 引文逐字」性质断言
  (比现在更强);runbook 重跑步骤 + 变体命名段同步改。

## 3. 我现在最不确定的 3 件事

1. **真实中文 ASR 语料上 LLM 逐字引文的保真率**:轻微改写/标点/全角半角差异会让 exact
   `str.find` 失配多少?P2 希望找到 LLM quote-then-anchor 的业界失配率数据与归一化分层
   惯例(exact → 归一化 → 拒,各层是否仍确定性)。
2. **推理型模型的输出预算语义**:DeepSeek OpenAI-兼容端点下 reasoning tokens 是否计入
   `max_tokens`?若是,候选①「答案短」不必然免截断(56/58 的烧法是「推理/复读」)——
   契约是否须同时要求「非推理模型或显式 reasoning 预算」+ 大幅上调 max_tokens(上限不产生
   成本,只防截断)?P2 查文档/社区实证。
3. **金标 Layer-1 exact-match 边界公平性**:pred span 边界今后由 LLM 引文范围决定,
   人工金标边界习惯未必逐字符对齐,exact-match P/R/F1 会不会把「找对了句子但边界差 3 字」
   计为全错?这不动本契约(计分语义属金标预注册),但门槛预注册时须知情——希望对方 P3
   给我「边界容差是否该进金标口径」的判断。
