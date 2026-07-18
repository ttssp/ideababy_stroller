# Forge v6 · 009 · P3R1 · GPT55xHigh · 联合收敛 R1(标分歧)

**Timestamp**: 2026-07-17T16:55:13Z
**Visibility**: 我已读对方 P1 + P2。
**Searches in this round**: NONE(避免 R1 又开搜索发散)。

## 1. 整合摘要

双方已收敛到候选①为主线:LLM 不再产 `span_start/span_end`,而是产可回锚的引文,偏移由确定性代码生成。P2 的 SOTA 参照也支持这一点:LangExtract 类路线不是相信 LLM 自报坐标,而是把 source grounding 放在 resolver 层,并把未定位、fuzzy 等状态显式暴露。

真正未收敛的是契约边界:对方 P2 更愿意把 fuzzy 纳入 v1,我更强调不能让 fuzzy 污染 E1 下界读数;对方仍保留「首现」的确定性直觉,我认为重复出现时应锁行为语义,而不是锁首现。预算面双方已经接近:reasoning tokens 必须纳入输出预算,finish_reason/usage 不能只是 WARN。

## 2. 我的初步 verdict(草案)

我倾向 **incremental refactor with contract hardening**,不是 redesign。候选①保留现有 caliber/gold/DDL 的 offset 通货,只替换 offset 来源并补 provenance,这是最小根治路径。R2 必须定三条:occurrence 选择语义、fuzzy 默认档位、预算硬门。若 R2 不能把这三条写成可测试契约,我会升级为 BLOCK。

## 3. 关键分歧清单

- **分歧 1**: occurrence 锁行为还是锁算法
  - 我的立场:契约应锁「按 claim 输出顺序、确定性、尽量不重叠、可审计 ambiguity」的行为语义;实现可用 DP,但不要把某个算法名写死。普通贪心 claim-set 可能在重叠长短引文场景牺牲全局匹配,除非证明满足这些语义。
  - 对方立场(引用对方 P2 原句,≤15 words):"多处出现默认取首现"
  - 我希望 R2 怎么收敛:写行为条款 + 反例测试;DP 可作为推荐实现,不是合同唯一解。

- **分歧 2**: fuzzy 层默认开还是默认关
  - 我的立场:v1 可实现 fuzzy,但 E1 gate 的主读数必须以 exact+normalized 为硬下界;fuzzy 单独分层报告,不得混入 meets/below 的核心密度。阈值宜比 LangExtract 0.75 更保守,至少 0.85,并预注册。
  - 对方立场(引用对方 P2 原句,≤15 words):"fuzzy 层(0.85 阈)是否进契约"
  - 我希望 R2 怎么收敛:默认开启审计性 fuzzy,默认不计入下界;NOT_FOUND 才走 typed rejection。

- **分歧 3**: 预算条款写公式还是写固定数
  - 我的立场:合同应写模型无关上界公式:visible_output_budget = N_max × quote_char_limit × token_factor + JSON overhead;generated_budget 必须覆盖 reasoning + visible。实现可设 32K+ 起步,但数字是实例,不是契约本体。
  - 对方立场(引用对方 P2 原句,≤15 words):"max_tokens ≥ 4× 预期可见输出"
  - 我希望 R2 怎么收敛:non-thinking 优先;若 thinking 开启,usage.reasoning_tokens、finish_reason=length、空 content 任一触发 census_invalid,CLI 非零。

## 4. 与 K 的对齐性自检

- K-(a)「输出锚定契约」→ ✅。候选① + deterministic grounding 正面修复 LLM 产 offset 根因。
- K-(b)「回锚失败语义」→ ✅。NOT_FOUND typed rejection; normalized/fuzzy 不伪装 exact,靠 tier/detail 表达。
- K-(c)「护栏固化条款」→ ✅。finish_reason/usage/content 进入硬门,不再只靠 stderr WARN。
- K-(d)「消费面追平清单」→ ✅。offset 仍是下游通货,新增 provenance/detail 不推翻 caliber/gold/DDL。
- v5 红线「prompt 改=新变体、预算须量化、模型无关、根治优先」→ ⚠。我的 verdict 对齐,但 R2 必须把 variant 身份和预算公式写成测试项,否则仍会漂回人工解释。
