---
forge_version: v6
idea: 009
fork: 009-pM3prime
scope: forge-lite+P2
convergence_mode: strong-converge
prefill_source: manual
x_hash: bfd6f2fc8770ccfdda7ac0c478cc696b
created: 2026-07-17T09:40:00Z
trigger: KG40 hand-back（20260717T081757Z · prd-revision-trigger · high）· E1 真密度被 proposer 字符偏移契约缺陷系统性阻断（HANDBACK-LOG 第 23 条决议 1/3）
snapshot_source: XenoDev-009 @ b51b5b2 + 15 dirty files（快照取自工作区 · 含未 commit 的 DeepSeek 接线 = 病灶现场）
---

# Forge v6 · 009-pM3prime · extraction proposer 契约:LLM 产出锚定语义重裁

## scope 说明 · forge-lite+P2（v3/v4 lite 与 v5 full 的中间档 · operator 拍板）

聚焦的**单一契约决策**,不重审 009。比 v3/v4 纯 lite 多跑一轮 P2 SOTA 检索——理由:
① 本题有真 prior-art（LLM 引文锚定 quote-then-anchor vs 字符偏移是业界已踩过的坑面）;
② 回声室预警已三连（v3 two-SELECT 原子性盲区靠 build 端 codex 兜底才抓到);
③ 当前 XenoDev 端 codex 5 次挂死（KG-38）,build 兜底正弱,forge 时多一轮外部证据校准。
流程:P1 双方独立审 → P2 双方 SOTA 检索 → 若零分歧直接 synthesizer;若实质分歧升级补 P3R1。

## X · 审阅标的（11 个 · IDS 3 + 快照 8 · 全可达）

**IDS 侧(直读)**:
1. **KG40 hand-back(核心 X)** `discussion/009/handback/20260717T081757Z-009-pM3prime-20260717T081757Z.md`
   —— 真跑事实(56/58 截断 0 span)+ 根因 + 候选①② + 守门救场记录
2. **PRD v0.3** `discussion/009/009-pM3prime/PRD.md` —— §4-E1 blocked-by-KG-40 状态 +
   §7 BLOCK 硬约束(尤其 §7-1 trial ledger / §7-2 文本 PIT / §7-3 引文锚定+提取稳定性)
3. **forge v5 stage doc** `discussion/009/forge/v5/stage-forge-009-v5.md` —— 红线 normative
   source(只需读 §BLOCK 红线 + §underweights,不重读全文)

**快照件(`discussion/009/forge/v6/snapshots/` · 源 = XenoDev-009 工作区 @ b51b5b2)**:
4. **census.py(病灶本体 · 638 行)** —— `_build_extraction_prompt` L191-246(让 LLM 产
   span_start/span_end 字符偏移 = 根因)· `build_llm_proposer` L247+(DeepSeek 接线 · JSON
   mode · max_tokens/截断处理)· 守门 L516-607(`llm_parse_failures` 计数 + 0-accepted 不可信
   判定 + STOP 语义)
5. **extractor.py(179 行)** —— C3 引文锚定消费面:span 偏移当前怎么被消费/验证
6. **caliber.py(157 行)** —— 口径 schema(ProposedSpan 形态 · 口径版本记账)
7. **gold_layer1.py(157 行)** —— 金标 Layer-1 span P/R/F1 —— **偏移语义改动的隐性消费面**
   (金标 harness 用 span 计分,契约改动必须论证此面兼容性)
8. **test_e1_citation_consistency.py(144 行)** —— C3 契约测试现编码(改契约 = 改此测试的
   断言语义,须明确)
9. **0017_add_extraction_tables.py** —— DDL 序列化面(extracted_signals 的 span 列语义)
10. **E1-real-census-runbook.md** —— 真跑操作面(重跑步骤受契约改动的影响)
11. **E2-design-inputs.md** —— 下游 E2 设计输入(extractor_variant 维度与本契约的耦合)

## Y · 审阅视角(2)

- **契约正确性 / LLM 能力贴合** —— 产出契约必须贴 LLM 真实能力(引原文子串 vs 数字符偏移);
  锚定语义在**全部消费面**(extractor 锚定 / gold_layer1 计分 / 0017 DDL / caliber schema /
  契约测试 / census 报告)一致、可审计、可复核(C3 引文锚定初心:每条疑似信号可回原文核对)
- **工程纪律 / 守门不变量** —— `llm_parse_failures` 护栏固化为 proposer 强制不变量的条款措辞;
  温度 0 / 提取器版本化 / 同文本同版本同输出红线保持;prompt 契约改 = 新提取器变体 →
  trial_ledger 记账(§7-1);重跑成本与输出预算安全性(9081 条语料长尾下不再撞截断)

## Z · 参照系

- mode: **对标 SOTA**(P2 阶段 · 双方各自检索)
- 检索面(allowed):LLM 结构化抽取/引文锚定业界实践(quote-then-anchor · fuzzy/exact
  substring 回锚 · 字符偏移失败案例)· span annotation 管线的锚定惯例(NER/IE 标注工具怎么
  处理 LLM 产出定位)· 推理型模型 JSON mode 输出截断的已知处置模式
- forbidden:tech-stack deep-dive / pricing / 与本契约无关的实施细节

## W · 产出形态

- **decision-list** ✅ —— 逐子决策 verdict:(a) 候选①(逐字文本片段+`str.find` 回锚)vs
  候选②(分块)vs 第三/混合方案;(b) 子串回锚歧义处置(多处出现/不完全逐字);
  (c) `llm_parse_failures` 强制不变量条款;(d) span 消费面逐面追平清单
- **refactor-plan** ✅ —— 改哪些文件 + 怎么改 + 测试栅栏 + XenoDev FU-task 边界 + 重跑
  runbook 步骤影响
- verdict-only / next-PRD / next-dev-plan / free-essay 未勾

## K · 用户判准(binding)

E1 真密度是 M3' 的 ROI 闸门(forge v5 §underweights「密度从未实测」)+ E2/E3 解锁第一条件。
07-17 真跑证实:proposer prompt 让 LLM 产原文字符偏移,推理型模型(deepseek-v4-flash)在长
语料 + JSON mode 下把 4096 token 输出预算烧在推理/复读上 → 56/58 截断 + 0 成功 span ≈100%
失败。census `llm_parse_failures` 守门救场(区分「截断假 0」vs「真没信号」),XenoDev 主动
TERM 停跑。契约不定 → 真密度产不出 → E2 门开不了。

**要定死的子决策**(对应 W decision-list):
- **(a) 输出锚定契约**:候选①「LLM 产逐字文本片段(exact substring),偏移由下游
  `str.find`/正则回锚」vs 候选②「分块喂 + 块内偏移」vs 第三/混合方案。build 侧倾向①
  (输出短 · 契约贴 LLM 能力:擅引原文不擅数字符),但**不预设答案**——双方独立评。
- **(b) 回锚失败语义**:子串在原文多处出现怎么裁(首现/全现/typed rejection)?LLM 引文
  不完全逐字(轻微改写/空白差异)怎么裁(fuzzy 容差 vs 硬拒)?必须走 typed rejection
  taxonomy(E0 口径已有的枚举精神),不允许 best-effort 静默猜。
- **(c) 护栏固化条款**:`llm_parse_failures>0 → 0-accepted 判不可信,不许静默当真 0 密度`
  固化为任何 proposer 实现的强制不变量(handback 决议 3 已定方向,forge 定条款措辞:
  api/parse/truncation 计数怎么分类、报告面怎么呈现)。
- **(d) 消费面追平清单**:span 偏移语义的全部消费面逐面裁定兼容/改动(extractor 锚定 /
  gold_layer1 span P-R-F1 计分 / 0017 DDL 列 / caliber schema / test_e1_citation_consistency
  断言 / census 报告)。**KG-36 教训:序列化面最易 silent 丢——不许只顺病灶。**

**binding**:
① 守 forge v5 三条 BLOCK 红线不动摇:文本 PIT;引文锚定 + 温度 0 / 提取器版本化 / 同文本
   同版本同输出;**prompt 契约改 = 新提取器变体 → trial_ledger 必须记账**(§7-1),旧
   literal / 旧 llm-prompt 变体的 trial 记录不可抹(多重检验分母诚实性)。
② 候选方案必须论证**输出预算安全性**:在 9081 条语料的长尾(最长 record 上界)下不再撞
   max_tokens 截断——给出量化理由,不许「应该够了」。
③ **模型无关**:契约不绑死 deepseek-v4-flash;换任何推理型/非推理型模型契约仍成立。
④ 已交付资产不推翻(907 passed:DeepSeek 接线 / 双口径密度 / 签字 threshold_hash 落库 /
   runbook / E2-design-inputs 复用),契约以最小 diff 落到现有 census.py / extractor.py;
   金标 harness(gold_layer1)的 span 计分语义若受影响,必须显式裁定而非顺带破坏。
⑤ 最小冲击但**根治优先**:宁可契约改大一点也不再来一次 61 分钟烧 key 产已知全 0 的重跑。
⑥ 产出要能直接指导 XenoDev FU-task(refactor-plan 精确到文件 + 测试栅栏 + runbook 影响),
   契约定稿后 operator 授权重跑真普查——这是本 forge 的唯一出口。
⑦ 轻收尾(单契约决策 · 可执行优先 · 超出最小契约的展开降级 v0.2 note)。

## 候选提示(供双方 first-take · 非预设答案)

(a) 的选择约束 (b) 和 (d):
- 候选① → (b) 歧义处置成为契约核心难点(多处出现 · 不完全逐字);(d) extractor 从「信任
  LLM 偏移」变「自己回锚」,gold_layer1 计分输入不变(仍是偏移,只是来源变);DDL 可能零改。
- 候选② → 偏移语义从全文变块内,(d) 全消费面都要理解「块」概念 = 契约面更宽;但 LLM 任务
  不变(仍数字符),截断风险只是被块大小缓解,根因未除。
- 混合路(如 ① + 超长 record 分块喂入)→ 输入侧分块与输出侧文本片段正交,可组合;须论证
  必要性(输入是否真会超 context)。
双方独立 first-take 评各候选 + 组合的最优路径,并各自给出消费面追平清单。
