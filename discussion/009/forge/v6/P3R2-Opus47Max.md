# Forge v6 · 009 · P3R2 · Opus47Max · 联合收敛 R2(finalize)

**Timestamp**: 2026-07-18T01:05:00Z
**Visibility**: 我已读对方 P3R1。
**Convergence mode**: strong-converge(从 forge-config 读)

## 1. 我对每条分歧的最终立场 + 让步

- **分歧 1 · occurrence 锁行为还是锁算法**:
  - 对方在 P3R1 给的论证:"写行为条款 + 反例测试;DP 可作为推荐实现" → **完全接受**。
  - 我的最终立场:契约锁四条行为语义——按 LLM 输出顺序处理 · 确定性 · 不重叠(已占用
    occurrence 不复用)· 无法满足时落 ambiguous(不静默)。DP(LangExtract resolver)为
    推荐实现非合同唯一解;**贪心 claim-set 若要用,须先给「重叠长短引文」反例测试证明满足
    四条语义**,证不出就用 DP——对方的反例担忧成立,采纳为测试栅栏而非算法禁令。
  - 让步给对方的部分:放弃我 P1 的「天真首现」(P3R1 已让);增采「反例测试」条款。
- **分歧 2 · fuzzy 默认档位**:
  - 对方在 P3R1 给的论证:"默认开启审计性 fuzzy,默认不计入下界" + 阈值 ≥0.85 预注册 → **接受全部**。
  - 我的最终立场:fuzzy 在 v1 实装且默认开,但**只作审计层**:E1 主读数(vs 预注册阈值的
    meets/below 判定)以 exact+normalized 为硬下界;fuzzy 命中单独分层报告(与既有
    strong/all 双口径正交叠加);阈值 0.85(比 LangExtract 0.75 保守)预注册,不可事后调。
  - 让步给对方的部分:我原「密度按 tier 分层报,operator 读区间」保留,但 verdict 判定
    口径收紧为对方版(fuzzy 不进 meets/below 判定输入)——更符合 C6 预注册纪律。
- **分歧 3 · 预算写公式还是固定数**:
  - 对方在 P3R1 给的论证:"数字是实例,不是契约本体" + 三触发即 census_invalid → **接受**。
  - 我的最终立场:契约本体 = 公式 `generated_budget ≥ reasoning_headroom +
    N_max × quote_char_limit × token_factor + JSON_overhead`;non-thinking 可用时必用;
    thinking 开启时 `usage.reasoning_tokens` 纳入监控。**usage.reasoning_tokens 异常 /
    finish_reason=length / 空 content 任一触发 → 该 record 计失败,失败数 > 0 →
    census verdict = census_invalid + CLI 非零 exit**(从 stderr WARN 升为硬门)。
    32K 等具体数落 runbook/实现作实例。
  - 让步给对方的部分:无实质残余(我 P3R1 已声明数字对方定)。

## 2. 联合 verdict(单一)

**extraction proposer 输出锚定契约重裁为「引文回锚制」(候选①),整体形态 = incremental
refactor with contract hardening,非 redesign。**四条契约条款:(A) **输出契约**:LLM 只产
{quote(逐字引文), ticker?, direction?, confidence},不产偏移,不回填 content_published_at
(census 从 record 注入,消 PIT 篡改面),每 record 上限 N_max 条;(B) **回锚契约**:确定性
分层 exact → normalized(空白/标点/全半角等确定性归一)→ fuzzy(阈 0.85 · 审计层),
occurrence 按四条行为语义(顺序 · 确定性 · 不重叠 · ambiguous 显式),每 accepted 信号携
match provenance(exact/normalized/fuzzy);NOT_FOUND/ambiguous → 复用
`UNANCHORABLE_CITATION` + detail 细分,**caliber v1 与 rejection 枚举不动**(避免阈值重
预注册连锁);(C) **读数与护栏契约**:E1 密度判定输入 = exact+normalized 硬下界,fuzzy
分层另报;proposer 必须暴露 api/parse/truncation 分类计数(类型契约非习惯);任一失败
计数 > 0 → verdict = **census_invalid**(新态,表达「读数不成立」)+ CLI 非零 exit;
(D) **预算与记账契约**:模型无关预算公式(见 §1-3)+ non-thinking 优先;prompt 模板 →
extraction_v2,**variant 身份 = proposer 类型 + 模板版本**(如 llm_extraction_v2),
trial_ledger 新 variant 记账,旧 literal/llm-v1 trial 不抹。金标 Layer-1 exact-match 口径、
Citation/DDL 偏移通货、0017 schema 全部不动。契约定稿 → XenoDev FU-task 改线 → operator
授权重跑真普查。**无 unresolved。**

## 3. 残余分歧降级为 v0.2 note

- **fuzzy 阈值 0.85 的实证校准**:若 E1 重跑后 unanchored 率或 fuzzy 命中占比异常
  (>10-20% 级),回头审阈值与归一化集(何时看:E1 真密度报告出来时)。
- **normalized 层的归一化集边界**(繁简转换是否纳入):先收窄为可逆确定性字符级归一
  (空白/标点/全半角),繁简留实证数据后定——过宽的归一化会稀释「逐字引文」语义。
- **0018 加列 vs detail 字段承载 provenance**:落库形态留 build(C7 只 ADD 均合规),
  detail 起步、量大再 0018 加列。
- **贪心 vs DP**:留反例测试裁决(§1-1),不占契约。

## 4. W 形态产出的初步草稿建议

- W 含 **decision-list** → 4 列矩阵建议 row:
  - 保留:span 偏移作存储/金标/DDL 通货 · caliber v1 + rejection 枚举 · gold_layer1
    exact-match · 0017 schema · census 单原子事务 · 温度 0/finish_reason allowlist/脱敏
  - 调整:`_build_extraction_prompt` → extraction_v2(引文制 · 删 content_published_at ·
    N_max 上限)· extractor 增确定性分层回锚步(exact/normalized/fuzzy + occurrence 四语义)·
    census verdict 增 census_invalid 态 + CLI 非零 · Proposer 契约显式失败计数 ·
    variant 身份 = proposer 类型+模板版本 · runbook(重跑步骤/原子性表述矛盾修正 L82)
  - 删除:LLM 直产 span_start/span_end 的输出契约(根因)· verdict「不可信」靠 stderr
    自觉的软语义
  - 新增:match provenance(exact/normalized/fuzzy)· 密度按 match tier 分层报告 ·
    预算公式条款 · occurrence 反例测试 · ambiguous detail 值
- W 含 **refactor-plan** → 关键模块(全在 XenoDev-009 / 004-pB):
  1. `extraction/census.py`:prompt v2 + proposer 失败计数契约化 + `_decide_verdict` 增
     census_invalid + CLI exit 语义 + max_tokens 公式化(non-thinking 优先)
  2. `extraction/extractor.py`(+可能新 `anchoring.py`):分层回锚 + occurrence 语义 +
     provenance;`_classify_reject` 接 ambiguous detail
  3. 测试栅栏:契约测试扩「切片==引文」性质断言 + occurrence 反例测试 + census_invalid
     触发测试 + 变体记账测试;`test_e1_citation_consistency.py` 同步
  4. 文档:E1 runbook(命令/解读/矛盾修正)· E2-design-inputs 追加 match-tier 读数维度
- 边界:**不碰** gold_layer1 / caliber schema / 0017 migration / 004 任何已 ship 件;
  FU-task 单独可 review,完成后经 hand-back 请 operator 授权重跑真普查。
