# Forge v6 · 009 · P3R2 · GPT55xHigh · 联合收敛 R2(finalize)

**Timestamp**: 2026-07-17T23:07:48Z
**Visibility**: 我已读对方 P3R1。
**Convergence mode**: strong-converge

## 1. 我对每条分歧的最终立场 + 让步

- **分歧 1**(occurrence 选择形态):
  - 对方在 P3R1 给的论证:"条款写行为语义" → 让步
  - 我的最终立场:合同锁行为,不锁算法。条款 wording:同一 record 内按 LLM 输出 claim 顺序回锚;每个 quote 选择确定性 occurrence;默认不复用已占用字符区间;若存在多个同等最优且无法由顺序/不重叠规则消解,标 `ambiguous` 并走 `UNANCHORABLE_CITATION` detail,不得静默首现。
  - 让步给对方的部分:DP 不写死为唯一实现;但必须有重复句、重叠长短引文、同 quote 多次出现三类反例测试。

- **分歧 2**(fuzzy 层默认档位):
  - 对方在 P3R1 给的论证:"fuzzy 进契约且默认开" → 部分接受
  - 我的最终立场:fuzzy 默认开,但只是审计层。条款 wording:回锚顺序为 exact → normalized → fuzzy → not_found;normalized 仅允许空白、标点、全半角、繁简/大小写等确定性规则;fuzzy 阈值预注册为 0.85。E1 meets/below 的硬下界只计 exact+normalized;fuzzy 命中单独报告为 upper/audit tier,不得混入下界。
  - 让步给对方的部分:不把 fuzzy 延到 v0.2;本轮纳入 v1,但用 tier 保护密度结论。

- **分歧 3**(预算与硬门):
  - 对方在 P3R1 给的论证:"non-thinking 优先 + 上界公式即可" → 让步
  - 我的最终立场:合同写模型无关公式,实现数字只是实例。条款 wording:可用 non-thinking 时必须关闭 reasoning;若 reasoning 不可关闭,`max_tokens >= max(4 * visible_output_budget, 16384)`。`visible_output_budget = N_max * quote_char_limit * token_factor + json_overhead`。任一 record 出现 `finish_reason=length`、空 content、坏 JSON、usage 缺失、`usage.reasoning_tokens > generated_budget - visible_output_budget` 时,本次 census verdict 必须为 `census_invalid`,CLI 非零。
  - 让步给对方的部分:32K+ 不写入合同;可作为 runbook 推荐默认值。

## 2. 联合 verdict(单一)

**我和对方在 R2 后达成的单一 verdict**:CLEAN to synthesize。forge v6 应选择候选①作为唯一输出契约:LLM 只产 quote/ticker/direction/confidence 等语义字段,不产字符 offset,`content_published_at` 由 census 回填;offset 由确定性分层回锚生成,并把 match tier/provenance 作为一等审计面。caliber/gold/DDL 的 offset 通货和金标 exact-match 口径保持不动;新增的是 contract hardening:occurrence 行为语义、fuzzy 审计层、预算公式、`census_invalid` 硬门、variant 身份可测试化。无 unresolved。

## 3. 残余分歧降级为 v0.2 note

- v0.2 note 1:fuzzy 阈值 0.85 是预注册起点。若 E1 重跑后 fuzzy tier 占比异常高或人工抽检误配率高,回头调阈值或改为 feature flag。
- v0.2 note 2:DP vs 贪心 claim-set 属实现选择。只要通过反例测试并满足行为语义,build 可选更简单实现。
- v0.2 note 3:provenance 落库方式可先走 detail JSON;若后续分析频繁按 tier 聚合,再加 0018 显式列。

## 4. W 形态产出的初步草稿建议

- W 含 verdict-only → 我的 verdict 关键句:"候选① CLEAN,但必须随合同硬化一起落地;候选②仅保留为输入超长 record 的正交补充。"
- W 含 decision-list → 我建议的 4 列矩阵 row(列前 5 条):
  - 保留:caliber v1 rejection enum;gold_layer1 exact-match;DDL offset 字段;现有 907 passed 资产;v5 三红线。
  - 调整:proposer schema 改 quote-first;extractor 增分层回锚;census verdict 增 `census_invalid`;runbook 改按 tier 读数;variant 身份包含 proposer 类型 + prompt 模板版本。
  - 删除:LLM 输出 `span_start/span_end`;LLM 回填 `content_published_at`;静默首现;stderr-only WARN;同一 `v1` 混记 literal/llm。
  - 新增:occurrence 反例测试;normalized/fuzzy provenance 测试;预算公式单测;finish_reason/usage 硬门测试;E1 report 的 exact+normalized/fuzzy 分层表。
- W 含 refactor-plan → 关键模块:
  - `census.py`:schema/prompt v2、variant 身份、budget guard、`census_invalid` verdict。
  - `extractor.py` 或新 resolver helper:exact/normalized/fuzzy/not_found/ambiguous 分层回锚。
  - tests/runbook:补三类 occurrence 反例、预算截断夹具、tier report 断言和重跑操作说明。
