# Forge v6 · 009 · P3R1 · Opus47Max · 联合收敛 R1(标分歧)

**Timestamp**: 2026-07-18T00:20:00Z
**Visibility**: 我已读对方 P1 + P2。
**Searches in this round**: NONE(避免 R1 又开搜索发散)。

## 1. 整合摘要

双方 P1 独立收敛候选①(quote-then-anchor)为骨架,P2 各自的 SOTA 检索互相补强且无一处
推翻共识:LangExtract(Google 生产库)是同构先例——LLM 只产引文子串,resolver 代码回锚;
对方深挖到 `resolver.py` 源码,证实业界 exact 阶段**不是天真首现而是 order-preserving
occurrence DP**(重复引文按输出顺序映射到 successive occurrences),fuzzy 默认阈 0.75 且
`MATCH_FUZZY` provenance 显式;我方文献证实 exact-only 在 ASR 中文语料会系统性低估 E1 密度
(空白/标点/全半角/繁简失配是常态),对方 ASR 评测参照系(CER/归一化惯例)独立支持同一结论。
根因侧对方补了关键事实:**DeepSeek thinking 默认 enabled,reasoning tokens 属 generated
completion**——我 P2 的「4× 可见输出」还不够保守,须 non-thinking 或大上限 + usage 硬门。
护栏侧双方一致:失败计数进契约、verdict 须能表达「读数不成立」、金标 exact-match 口径不动。

## 2. 我的初步 verdict(草案)

选候选①为唯一输出契约,配四条联合条款:(1) LLM 输出 = {quote, ticker, direction,
confidence},**删 content_published_at**(census 回填)+ 每 record 限 N 条;(2) 确定性
分层回锚:exact → 确定性归一化(空白/标点/全半角)→ fuzzy(阈值化 · 确定性),重复引文按
**确定性 occurrence 顺序映射不重叠**;NOT_FOUND/ambiguous → 复用 `UNANCHORABLE_CITATION`
+ detail 细分(exact/normalized/fuzzy/not_found/ambiguous),**caliber v1 不动**;(3) 密度
按 match tier 分层报——mirror 现有 strong/all 双口径哲学,operator 读 [exact+normalized,
+fuzzy] 区间;census verdict 增「census_invalid/读数不成立」态 + CLI 非零 exit,proposer
失败计数从实现习惯升为类型契约;(4) 预算条款:non-thinking 优先,max_tokens ≥ 保守上界
公式(N × 引文上限 + 推理余量),finish_reason allowlist + usage.reasoning_tokens 硬门;
variant 身份 = proposer 类型 + prompt 模板版本,trial_ledger 记账,旧 literal/llm trial 不抹。

## 3. 关键分歧清单

- **分歧 1 · occurrence 选择的具体形态**(我让步后的残余)
  - 我的立场:接受对方方向——从「天真首现」升级为**确定性 occurrence 顺序映射**。让步理由
    不只是 SOTA 惯例:ASR 转写重复句常见,天真首现会让两条重复信号映射同一 span →
    gold_layer1 的 set 语义把它们塌缩成一条,密度与金标计数双双失真——这是正确性论证。
  - 对方立场:"SOTA 更接近 order-preserving occurrence DP + match provenance"
  - 我希望 R2 怎么收敛:条款写**行为语义**(重复引文顺序映射到不同 occurrence · 不重叠 ·
    确定性 · 全失配走 ambiguous),**不锁算法实现**(全量 DP vs 贪心 claim-set 留 build,
    LangExtract resolver 作参考实现)。对方若坚持锁 DP,请给「贪心不满足行为语义」的反例。
- **分歧 2 · fuzzy 层进契约的档位**
  - 我的立场:fuzzy 进契约且**默认开**,但密度按 tier 分层报(fuzzy 命中不混入下界口径),
    C8「不猜」由确定性+阈值+provenance+分层读数共同满足——工具失配不该记成语料歧义。
  - 对方立场:"fuzzy 不能静默当 exact,需写 match_mode/score/detail"(未表态默认开/关)
  - 我希望 R2 怎么收敛:对方明确表态默认开 vs 默认关(v2 开关)。我接受任一,只要
    (i) 阈值进契约预注册(参考 LangExtract 0.75,取保守值)(ii) 分层读数强制。
- **分歧 3 · 预算条款的强度**
  - 我的立场:non-thinking 优先 + 上界公式即可,不必绑 32K。
  - 对方立场:"建议用 non-thinking 或 32K+ 上限,并把 finish_reason/usage 变硬门"
  - 我希望 R2 怎么收敛:合并为「non-thinking 可用时必用;不可用时 max_tokens ≥ max(公式
    上界 × 4, 16K)+ usage 监控硬门」——具体数字对方定,我在意的是**模型无关的公式形态**。

## 4. 与 K 的对齐性自检

- K-① 三红线不动摇 / prompt 改 = 新变体记账 → ✅ verdict-(4) variant 身份条款直接落实;
  文本 PIT 由「删 content_published_at + census 回填」反而更强(消 LLM 篡改面)。
- K-② 输出预算安全性量化 → ✅ verdict-(4) 上界公式 + thinking 事实修正(对方 P2 证据)。
- K-③ 模型无关 → ✅ 条款全为行为语义(finish_reason/usage 是 OpenAI-兼容通用面)。
- K-④ 资产不推翻 / 金标 span 计分显式裁定 → ✅ 金标 exact-match 口径不动(双方一致),
  偏移仍是存储通货;DDL 零改(provenance 走 detail 字段,0018 加列留 build 选项)。
- K-⑤ 根治优先 → ✅ 候选①根除「LLM 数字符」;⚠ 一处诚实标注:fuzzy 阈值是新引入的
  校准点,若 E1 重跑后 fuzzy 命中占比异常高,须回头审阈值(记 v0.2 note)。
- K-⑥ 直接指导 FU-task → ✅ 四条款可直接展开 refactor-plan(census/extractor/测试/runbook)。
- K-⑦ 轻收尾 → ✅ 算法锁定、0018 加列、fuzzy 默认档等实现级取舍显式降级 build/v0.2。
