# Forge v6 · 009 · P1 · GPT55xHigh · 独立审阅(no search)

**Timestamp**: 2026-07-17T10:03:41Z
**Searches used**: NONE in this round.
**Visibility**: I did NOT read other reviewer's P1.
**Reviewer stance**: 审阅人 — 评判已存在物,不是 daydream。

## 0. 我读到的标的清单 + 阅读策略

- 我读了:`forge-config.md`;`moderator-notes.md` 不存在;KG-40 hand-back;PRD;forge v5 指定两段;8 个快照文件(`census.py`、`extractor.py`、`caliber.py`、`gold_layer1.py`、C3 测试、0017 DDL、runbook、E2 输入);以及 forge P1 模板。
- 我跳过的:`discussion/009/forge/v6/P1-Opus47Max.md` 按 parallel independence 禁令未读;无 web search。
- **K(用户判准)摘要**:K 的硬句是“契约不定 → 真密度产不出 → E2 门开不了”,且绑定“prompt 契约改 = 新提取器变体 → trial_ledger 必须记账”。本轮只裁 LLM proposer 锚定契约、失败护栏与 span 消费面追平。
- **我的阅读策略**:先看“LLM 产什么、系统最终信什么”,再看失败计数、trial 记账、PIT/稳定性是否守住。

## 1. 现状摘要(按 Y 视角组织)

### 契约正确性 / LLM 能力贴合

`census.py` 的 prompt 要 LLM 返回全文 `span_start/span_end`。KG-40 真跑 58 条中 56 条 `finish_reason=length`,0 成功 span;这不是“密度低”,而是让模型数字符偏移导致 JSON 截断。下游 `extractor.py`、`caliber.Citation`、0017 DDL、Layer-1 金标、C3 测试都需要最终 offset,但没有证据表明 offset 必须由 LLM 直接产出。

### 工程纪律 / 守门不变量

现有守门已救场:`llm_parse_failures/api_failures` 进入 `CensusReport`,CLI 警告失败非零时 0-accepted 不可信;PRD/hand-back 也把 E1 标为 blocked-by-KG-40。v5 红线仍是文本 PIT、引文锚定与稳定性、trial ledger、两层金标 gate。0017 的 CHECK/trigger/span 列较硬,E2 输入还记录 gate 需按 extractor_variant 加维。

## 2. First-take 评分(按 Y 视角)

| Y 维度 | 倾向 | 理由 |
|---|---|---|
| 契约正确性 / LLM 能力贴合 | refactor | 最终 span 语义 keep;“LLM 直接产字符偏移”已被真跑证伪。 |
| 工程纪律 / 守门不变量 | refactor | 红线与失败计数 keep;失败结论语义、variant 记账、消费面追平需固化。 |

**(a)** 选候选①为主:LLM 产逐字原文片段,下游确定性回锚成 offset。候选②只缓解长输入,仍让模型数偏移;可作输入侧补充,不应作输出契约。

**(b)** 多处 exact substring 和非逐字引用都不应静默首现或猜测。typed rejection 优先;最多允许空白规范化这类可解释规则,且必须计数。

**(c)** `api_failure`、`parse_failure`、`truncation/non-stop finish_reason` 应分桶;任一非零且 accepted=0 时,只能报“读数不成立/需重跑”,不得给真 0 密度 verdict。

**(d)** 消费面逐面追平:extractor 从“信 LLM offset”改为“quote 回锚后守门”;gold_layer1 仍按最终 offset exact-match;0017 DDL span 列兼容但须标明来源;caliber 保持 `Citation` 为最终锚点,候选 schema 区分 quote/citation;C3 测试覆盖回锚、歧义拒绝、确定性;census/runbook 更新失败语义与新 variant 记账;E2/gate 不得让新 variant 蹭旧金标。

## 3. 我现在最不确定的 3 件事

1. P2 需验证 quote-then-anchor 的输出预算上界:多信号长 record 是否仍截断。
2. 子串歧义分布未知:重复短句、ASR 空白/标点、全半角差异会决定 rejection 是否过严。
3. Layer-1 是否继续只看最终 offset exact-match,或另加 quote 命中诊断指标;不能借此放松 C3。
