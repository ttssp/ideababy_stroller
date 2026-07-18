# Forge Stage · 009 · v6 · "extraction proposer 锚定契约:引文回锚制根治字符偏移截断"

**Generated**: 2026-07-18T02:10:00Z
**Source**: forge-lite+P2 run v6 · X = 11 标的(IDS 3 直读 + XenoDev-009 快照 8), Y = 契约正确性/LLM 能力贴合 + 工程纪律/守门不变量, Z = 对标 SOTA(P2 双方各自检索), W = decision-list + refactor-plan(仅此两件)
**Convergence mode**: strong-converge
**Rounds completed**: P1 (both · Opus 4.8 Max + GPT-5.5 xHigh) · P2 (both) · P3R1 (both) · P3R2 (both)
**Searches run**: 14 across ≥6 distinct sources(Opus 4:LangExtract 博客/resolver 源码深读 + LLM-IE 文献 + RAG attribution + DeepSeek 文档;GPT 10:LangExtract README/resolver.py + DeepSeek thinking/API + AWS/HF ASR eval + 中文 ASR 模型卡)
**Moderator injections honored**: none(moderator-notes.md 不存在 · 双方 P1 均确认)
**Convergence outcome**: converged(单一 verdict · P3R2 双方 §2 均标"无 unresolved"/"CLEAN to synthesize" · 三条占位分歧全在 R2 收敛为条款细化 · GPT R1 的 BLOCK 升级条件在 R2 满足后解除)

---

## How to read this

forge 是横切层(不在 L1-L4 pipeline 内)。本文档是双专家独立审(P1)+ SOTA 对标(P2)+ 两轮
联合收敛(P3R1/R2)后的**单一 verdict**。scope = forge-lite+P2(单一契约决策 · 非全 idea
重审):只裁定 009-pM3prime E1 的 extraction proposer 输出锚定契约,不重审 009 集合体。

触发事实:KG-40 真跑(58 条中 56 条 `finish_reason=length`、0 成功 span)证明现契约让 LLM
直接产原文字符偏移(`span_start/span_end`)在长语料 + 推理型模型 JSON mode 下 ≈100% 截断,
E1 真密度读不出来 → E2/E3 门开不了。本 forge 定死修复契约。

读完你应该:
- 知道双专家最终 verdict:改为**「引文回锚制」(候选①)+ 四条契约条款**,整体形态 =
  incremental refactor with contract hardening(非 redesign)
- 逐条溯源支持每条结论的证据(§Evidence map · 每行可回原轮)
- 拿到两件可执行草案:§Decision matrix(保留/调整/删除/新增)· §Refactor plan(改哪些
  文件 + 测试栅栏 + XenoDev FU-task 边界 + runbook 影响)
- 能基于 §Decision menu 直接进下一步([A] 授权 XenoDev FU-task 改线 + 重跑真普查 /
  [B] 跑 v7 / [C] 局部接受 / [P] park / [Z] abandon)

**一句话 verdict**:让 LLM 数字符偏移是根因,业界(LangExtract)早已改为 LLM 只产逐字引文、
偏移由确定性代码回锚;009 照此改契约并配 fuzzy 审计层 / census_invalid 硬门 / 模型无关预算
公式 / variant 记账四条硬化条款,contract 定稿即可授权 XenoDev 重跑真密度。

---

## Verdict

**extraction proposer 输出锚定契约重裁为「引文回锚制」(候选①),整体形态 = incremental
refactor with contract hardening,非 redesign。** LLM 只产 `{quote(逐字引文), ticker?,
direction?, confidence}`,不产字符偏移;偏移由确定性代码分层回锚(exact → normalized →
fuzzy)生成,match tier/provenance 升为一等审计面。候选②(输出侧分块)在 SOTA 对标中无
先例、根因(LLM 数字符)未除,降级为「输入超长 record 的正交补充」,不作输出契约。

四条契约条款:**(A) 输出契约**——删 `content_published_at`(census 回填 · 消 PIT 篡改面)、
每 record 上限 N_max 条;**(B) 回锚契约**——分层 exact→normalized→fuzzy(阈 0.85 预注册 ·
审计层)+ occurrence 四条行为语义(顺序/确定性/不重叠/ambiguous 显式),NOT_FOUND/ambiguous
复用 `UNANCHORABLE_CITATION`+detail,caliber v1 不动;**(C) 读数与护栏契约**——密度硬下界
只计 exact+normalized(fuzzy 另报)、proposer 失败计数升为类型契约、任一失败计数 > 0 →
新态 `census_invalid` + CLI 非零 exit;**(D) 预算与记账契约**——模型无关预算公式 +
non-thinking 优先 + variant 身份 = proposer 类型+模板版本(trial_ledger 记账 · 旧变体不抹)。

**回应 K**:① 三红线不动摇 + prompt 改=新变体记账 → (D) variant 身份条款直接落实,文本 PIT
因删 content_published_at 反而更强;② 输出预算安全性量化 → (D) 上界公式 + DeepSeek thinking
计入 max_tokens 的文档级修正;③ 模型无关 → 条款全为行为语义(finish_reason/usage 是
OpenAI-兼容通用面);④ 资产不推翻 → 金标 exact-match/Citation/DDL 偏移通货/0017 schema 全
不动;⑤ 根治优先 → 候选①根除「LLM 数字符」;⑥ 直接指导 FU-task → §Refactor plan 精确到文件。

## Evidence map

| 结论 | 来源 | 引用(≤15 words) | 是否有反对证据 |
|---|---|---|---|
| LLM 直产字符偏移已被真跑证伪 | forge-config 触发 + P1-GPT §1 | "58 条中 56 条 finish_reason=length,0 成功 span" | - 真跑事实 |
| 候选①(引文回锚)有生产级先例 | P2-Opus §1 row1 + P2-GPT §1 row1 | "LangExtract:LLM 只产引文子串,resolver 代码回锚" | - SOTA 双侧独立命中同一库 |
| 候选②无先例、根因未除 → 降级 | P2-Opus §3 + P1-Opus §1 | "候选②在对标中无先例;runbook 已判其破回锚" | - 双方一致 |
| exact-only 会系统性低估 E1 密度 | P2-Opus §1 row2 + P2-GPT §1 row5 | "空白/标点/全半角/繁简失配是常态非例外" | ⚠ 推翻了 P1-Opus/P1-GPT 的 exact-only 初判(见 §underweights) |
| 多处匹配走确定性 occurrence 非天真首现 | P2-GPT §1 row2 + P3R1-Opus §3 分歧1 | "order-preserving occurrence DP;首现会塌缩重复信号" | ⚠ 推翻双方 P1 的「首现锚定」(R2 已让步收敛) |
| fuzzy 进 v1 但只作审计层不计下界 | P3R1-GPT §3 分歧2 + P3R2-Opus §1 | "fuzzy 默认开 · 密度硬下界只计 exact+normalized" | - R2 双方收敛(Opus 接受 GPT 收紧版) |
| fuzzy 阈值取 0.85(比 LangExtract 0.75 保守)预注册 | P3R1-GPT §3 + P3R2 双方 §1 | "阈值宜比 0.75 更保守,至少 0.85,并预注册" | - 双方一致 |
| DeepSeek reasoning tokens 计入 max_tokens | P2-GPT §1 row4 + P2-Opus §1 row4 | "reasoning_content 与 final content 同为生成物" | - 文档级证实(修正 P1 §3 疑虑) |
| 预算写模型无关公式,固定数只是实例 | P3R1-GPT §3 分歧3 + P3R2 双方 §1 | "数字是实例,不是契约本体" | - R2 双方收敛 |
| 需新增 census_invalid 态(表达读数不成立) | P1-Opus §1 视角B + P3R2 双方 §2 | "verdict 三态无法表达『读数不成立』,靠 stderr 自觉" | - 双方一致 |
| variant 身份须编码 proposer 类型+模板版本 | P1-Opus §1 视角B + P3R2 双方 §1 | "literal 与 llm 真跑共享一个 variant id" | - 双方一致(§7-1 记账诚实性) |
| caliber v1/gold exact-match/DDL 偏移通货不动 | P1-Opus §2 (d) + P3R2 双方 §2 | "偏移仍是存储与计分通货,只是来源变" | - 双方一致 |

## Intake recap

### X · 审阅标的(11 个 · 全可达)
- **IDS 直读 3**:KG-40 hand-back(核心 X · 真跑事实+根因+候选①②)· PRD v0.3(§4-E1
  blocked-by-KG-40 + §7 BLOCK 红线)· forge v5 stage doc(§BLOCK normative + §underweights)
- **XenoDev-009 快照 8**(@ b51b5b2 工作区 · 含 15 dirty):census.py(病灶本体 638 行)·
  extractor.py · caliber.py · gold_layer1.py · test_e1_citation_consistency.py ·
  0017 DDL · E1-real-census-runbook.md · E2-design-inputs.md

### Y · 审阅视角(2)
- **契约正确性 / LLM 能力贴合**:产出契约必须贴 LLM 真实能力(引原文子串 vs 数字符偏移);
  锚定语义在全部消费面(extractor/gold_layer1/0017 DDL/caliber/契约测试/census 报告)一致、
  可审计、可复核
- **工程纪律 / 守门不变量**:`llm_parse_failures` 护栏固化为强制不变量;温度 0/提取器
  版本化/同文本同版本同输出红线保持;prompt 契约改=新变体→trial_ledger 记账;输出预算安全性

### Z · 参照系
- mode:**对标 SOTA**(P2 阶段 · 双方各自检索)
- 用户外部材料:**无**(K 中无外部链接/文件 · X 标的即全部材料)

### W · 产出形态
- **decision-list** ✅ + **refactor-plan** ✅
- verdict-only / next-PRD / next-dev-plan / free-essay **未勾**(双方 P3R2 §4 的 verdict-only
  关键句已并入上方 §Verdict 段落)

### K · 用户判准(binding)
E1 真密度是 M3' 的 ROI 闸门(forge v5 §underweights「密度从未实测」)+ E2/E3 解锁第一条件。
07-17 真跑证实:proposer prompt 让 LLM 产原文字符偏移,推理型模型在长语料+JSON mode 下把
4096 token 预算烧在推理/复读上 → 56/58 截断 + 0 成功 span ≈100% 失败。要定死 (a) 输出锚定
契约 / (b) 回锚失败语义 / (c) 护栏固化条款 / (d) 消费面追平清单。binding 七条:① 守 v5 三红线
+ prompt 改=新变体记账;② 输出预算安全性须量化(不许「应该够了」);③ 模型无关(不绑
deepseek-v4-flash);④ 907 passed 资产不推翻 + 金标 span 计分显式裁定;⑤ 最小冲击但根治优先;
⑥ 产出直接指导 XenoDev FU-task(refactor-plan 精确到文件+测试栅栏+runbook 影响);⑦ 轻收尾
(超出最小契约的展开降级 v0.2 note)。

### 收敛模式
**strong-converge**(P3R2 双方 §2 均标单一 verdict · 无 unresolved)

---

## Decision matrix(W · decision-list)

| 类别 | 项 | 来源(标的具体位置) | 理由(evidence) | 优先级 |
|---|---|---|---|---|
| **保留** | span 偏移作存储/金标/DDL 通货 | caliber.Citation · 0017 DDL span 列 · gold_layer1 | 偏移仍是通货,只是来源从「LLM 声称」变「代码回锚」;资产不推翻(K-④) | P0 |
| **保留** | gold_layer1 exact-match P/R/F1 口径 | gold_layer1.py | 金标计分语义属预注册,双方一致不动;pred 边界改由引文范围决定但计分口径不变 | P0 |
| **保留** | caliber v1 + `ExtractionRejectionReason` 枚举 | caliber.py(frozen) | 新增枚举值=新 caliber_version=阈值重预注册连锁;复用现值 + detail 区分子因保 v1 不动 | P0 |
| **保留** | 温度 0 / finish_reason allowlist / 脱敏 / census 单原子事务 | census.py 守门链 L303-348 | v5 红线保持;07-17 真跑 TERM 后全回滚无脏行,重跑干净 | P0 |
| **调整** | `_build_extraction_prompt` → extraction_v2 | census.py L191-246 | 引文制 · 删 content_published_at(census 回填) · 每 record N_max 上限 | P0 |
| **调整** | extractor 增确定性分层回锚步 | extractor.py(+可能新 anchoring.py) | exact/normalized/fuzzy + occurrence 四行为语义;守门从「验界内」升「产真值」 | P0 |
| **调整** | census verdict 增 `census_invalid` 态 + CLI 非零 exit | census.py `_decide_verdict` + CLI | 现三态无法表达「读数不成立」,靠 stderr 自觉 exit 0(P1-Opus 视角B) | P0 |
| **调整** | Proposer 契约显式失败计数(类型契约非 duck-type) | census.py `Proposer` 协议 | 现 `getattr(proposer,"stats",None)` 是实现习惯,K-(c) 要固化为不变量 | P0 |
| **调整** | variant 身份 = proposer 类型 + 模板版本 | census `--extractor-variant` + `_EXTRACTION_TEMPLATE_VERSION` | literal 与 llm 现共享 `v1`,§7-1 记账在身份层就守不住 | P0 |
| **调整** | runbook 重跑步骤 + 原子性表述矛盾修正(L82 vs 单原子) | E1-real-census-runbook.md | 同文档自相矛盾(增量 commit vs 单原子);重跑判据引用 verdict 非人读 WARN | P1 |
| **删除** | LLM 直产 `span_start/span_end` 的输出契约 | census.py L191-215(根因) | 真跑 56/58 截断证伪;LLM 擅引原文不擅数字符 | P0 |
| **删除** | LLM 回填 `content_published_at` | census.py L209 | LLM 输出携带调用方已知常量,徒增预算 + PIT 篡改面 | P0 |
| **删除** | verdict「不可信」靠 stderr WARN 的软语义 | census 守门 | 升为 census_invalid 硬门 + 非零 exit | P0 |
| **新增** | match provenance(exact/normalized/fuzzy)+ 密度按 tier 分层报 | (新 · 来自 LangExtract SpanMatch.status) | P2-Opus §1 row1:锚定方法本身带 provenance;operator 读 [exact+normalized, +fuzzy] 区间 | P0 |
| **新增** | 模型无关预算公式条款 + non-thinking 优先 | (新 · 来自 P2 DeepSeek 文档修正) | reasoning tokens 计入 max_tokens;公式 = reasoning_headroom + N_max×quote上限×token系数 + JSON | P0 |
| **新增** | occurrence 反例测试(重复句/重叠长短引文/同 quote 多次) | (新 · 来自 P3R1-GPT 分歧1) | 锁行为语义不锁算法;贪心 claim-set 须过反例证明满足四语义,证不出用 DP | P0 |
| **新增** | ambiguous detail 值 + census_invalid 触发测试 + 变体记账测试 | (新 · 契约测试扩) | 「切片==引文」性质断言比现在更强 | P0 |

每行可在 §Evidence map 溯源(新增行来源为 SOTA 对标 / K 关切,已在括号标注)。

## Refactor plan(W · refactor-plan)

关键模块全在 XenoDev-009 build runtime(路径以快照为准,实装以工作区最新为准)。以 FU-task
形态改线,单独可 `/task-review`,完成后经 hand-back 请 operator 授权重跑真普查。

#### 模块 A · `extraction/census.py`(prompt + 护栏 + 预算 + 记账)
- **当前问题**:`_build_extraction_prompt`(L191-246)让 LLM 产字符偏移(根因);verdict
  三态无「读数不成立」;proposer 失败计数是 duck-type 可选;max_tokens=4096 固定;literal/llm
  共享 variant `v1`(P1-Opus §1 视角B)
- **目标态**:extraction_v2 引文制契约(LangExtract 同构 · P2 双方 row1)+ census_invalid
  硬门 + 模型无关预算公式(non-thinking 优先)+ variant 身份编码
- **改造步骤**(顺序):
  1. `ProposedSpan` schema 加 `quote` 载体、删 `span_start/span_end/content_published_at`
     的 LLM 产出要求(census 回填 published_at)
  2. `_build_extraction_prompt` → v2:要求逐字引文 + 每 record N_max 条上限
  3. `Proposer` 协议显式声明 api/parse/truncation 分类计数(类型契约)
  4. `_decide_verdict` 增 `census_invalid`:任一失败计数 > 0(finish_reason=length / 空
     content / 坏 JSON / usage 缺失 / `reasoning_tokens > generated_budget − visible_budget`)
     → census_invalid + CLI 非零 exit
  5. max_tokens 公式化:`generated_budget ≥ reasoning_headroom + N_max×quote_char_limit×
     token_factor + JSON_overhead`;non-thinking 可用必用,否则 `≥ max(4×visible, 16384)`
  6. variant 身份 = proposer 类型 + 模板版本(如 `llm_extraction_v2`),接 trial_ledger
- **风险**:reasoning_tokens 若某端点不回 usage → 须当 census_invalid(P2-GPT §1 row4 警示
  usage 缺失面);⚠ 预算公式的 token_factor/N_max 具体值在 build-time 真跑前是推演
- **预估代价**:S(prompt/schema/verdict 均局部改 · 双方 P3R2 §4 一致判 incremental)

#### 模块 B · `extraction/extractor.py`(+ 可能新 `anchoring.py`)
- **当前问题**:`_classify_reject`(L149-156)只验「界内 + 非空白」,不验切片内容与信号
  语义对应——LLM 给个界内乱偏移也能过守门(P1-Opus §1 视角A)
- **目标态**:确定性分层回锚 exact → normalized(空白/标点/全半角)→ fuzzy(0.85 审计层)
  → not_found;occurrence 四行为语义(顺序/确定性/不重叠/ambiguous);每 accepted 信号携
  match provenance
- **改造步骤**:
  1. 新回锚步:LLM `quote` → `str.find`/归一化/difflib fuzzy 分层产偏移(锚定即验证)
  2. occurrence 顺序映射不重叠(DP 参考 LangExtract resolver · 贪心须过反例测试)
  3. NOT_FOUND/ambiguous → 复用 `UNANCHORABLE_CITATION` + detail 细分
     (exact/normalized/fuzzy/not_found/ambiguous)
  4. `_classify_reject` 接 ambiguous detail
- **风险**:fuzzy 阈值 0.85 无本语料实证(v0.2 note);normalized 归一集边界(繁简是否纳入)
  过宽会稀释「逐字引文」语义 → 起步仅可逆确定性字符级
- **预估代价**:S-M(回锚层是本契约 diff 中心 · 可能拆新 anchoring.py)

#### 模块 C · 测试栅栏(tests/)
- **当前问题**:`test_e1_citation_consistency.py` 断言 `text[start:end]==命中片段`,未覆盖
  回锚/歧义/确定性
- **改造步骤**:扩「切片==引文逐字」性质断言 + occurrence 三类反例测试(重复句/重叠长短
  引文/同 quote 多次)+ census_invalid 触发测试 + 变体记账测试 + normalized/fuzzy provenance
  测试 + 预算公式单测 + finish_reason/usage 硬门夹具
- **风险**:⚠ C″ 须补泄露面对抗验证(引 MEMORY 教训:此前 census verdict/two-SELECT 靠
  build-time 真跑才抓到推演盲区)
- **预估代价**:S-M

#### 模块 D · 文档(runbook / E2-design-inputs)
- **改造步骤**:E1 runbook 改按 tier 读数 + 修正 L82 原子性表述矛盾 + 重跑判据引用 verdict;
  E2-design-inputs 追加 match-tier 读数维度
- **预估代价**:S

**边界(不碰)**:gold_layer1 / caliber schema / 0017 migration / 004 任何已 ship 件 /
907 passed 资产。FU-task 完成 → hand-back → operator 授权重跑真普查(本 forge 唯一出口)。

---

## What this menu underweights(强制自批判)

- **⚠ 本 verdict 大量条款在 build-time 真跑前仍是推演**:引 MEMORY 教训
  `forge-verdict-vs-empirical-ship` 的先例——009 一周期内 F6 幻影 bug + two-SELECT 原子性
  两次都是 forge/handback 理论决议漏了 DB 引擎语义/并发/原子性盲区,靠 XenoDev build-time
  复现测才杀掉。本 verdict 的预算公式 token_factor/N_max 取值、census_invalid 触发链、fuzzy
  分层回锚在真语料上的行为,都必须以 XenoDev 真跑为最后防线,不可据本文档即认定已解。
- **⚠ 快照与真码漂移风险**:X 标的的 8 个快照件取自 XenoDev-009 未 commit 工作区 @ b51b5b2
  +15 dirty(病灶现场),行号(census L191-246 等)与 refactor-plan 步骤须以 build 时工作区
  最新码为准校对,漂移可能使某步骤定位失准。
- **⚠ fuzzy 阈值 0.85 无本语料实证**:0.85 是「比 LangExtract 0.75 保守」的推理取值,非
  本中文 ASR 语料实测。若 E1 重跑后 fuzzy tier 占比异常高(>10-20% 级)或人工抽检误配率高,
  须回头审阈值(已列 v0.2 note),但这意味着一次「先跑再校准」而非本 forge 一次定死。
- **反对证据的整合**:两条 ⚠ 反对证据(exact-only 系统性低估密度 / 首现塌缩重复信号)实际
  **推翻了双方 P1 的初判**——这不是主 verdict 的隐患,恰是 P2 SOTA 检索纠偏的正面成果,
  主 verdict 采纳了纠偏后的版本(分层锚定 + 确定性 occurrence)。
- **Y 视角覆盖盲区**:Y 只含契约正确性 + 工程纪律两视角,未含「金标口径公平性」——P1-Opus
  §3-3 提出「pred 边界今后由 LLM 引文范围决定,exact-match P/R/F1 会否把『找对句子但边界差
  3 字』计全错」,本 verdict 保金标口径不动(双方一致),但**边界容差是否该进金标口径**这个
  问题被 defer 且未在契约内解决,值得 E1 重跑读数时 attention。
- **convergence_mode 副作用**:strong-converge + 回声室三连预警(MEMORY:001/006/009 forge
  回声室风险持续高)。双方独立命中同一库(LangExtract)是强信号,但也意味着若 LangExtract 的
  occurrence-DP/fuzzy-0.75 设计本身有本场景不适配处,两模型会同向强化。反证据:P2 双方从
  **不同检索路径**(Opus 博客+文献 / GPT resolver 源码+ASR 模型卡)独立到达,降低了纯回声率。
- **X 标的覆盖局限**:未读 004-pB / M2 侧任何码(契约边界声明不碰),若回锚层的 provenance
  落库形态实际影响下游 004 消费面(理论上不该),本 forge 不覆盖——detail 起步、0018 加列
  留 build 的选择已把此风险最小化。
- **forge versioning 提示**:以下新信息进入会触发 v7:① E1 重跑后 fuzzy tier 占比 / unanchored
  率异常 → 审阈值与归一化集;② build-time 真跑发现预算公式或 census_invalid 触发链有推演盲区
  (概率非零,见第一条 ⚠);③ 金标边界容差问题若实测显著影响 P/R/F1 → 须重开金标口径讨论;
  ④ 换非 DeepSeek 模型后契约有不成立处(K-③ 模型无关性被实证挑战)。

## Decision menu(for human)

### [A] 接受 verdict → 授权 XenoDev FU-task 改线 + 重跑真普查(本 forge 唯一出口)
```
本 verdict 是对现有 009-pM3prime E1 实装的**契约修复**,不产新 PRD branch
(W 未勾 next-PRD · 本就无需新 fork)。出口 = XenoDev FU-task,不是 /plan-start。

流程:
1. 把本 stage 的 §Decision matrix + §Refactor plan 作为 FU-task 输入,
   在 XenoDev-009 起改线(census.py / extractor.py / tests / runbook)
   - 每模块单独 /task-review <fork> T<NNN>,verdict ≠ BLOCK 方可 merge
   - ⚠ 模块 C″ 测试栅栏须补泄露面对抗验证(反推演盲区 · 见 §underweights)
   - ⚠ refactor-plan 行号以 build 时工作区最新码为准校对(快照漂移风险)
2. prompt 契约改 = 新提取器变体 → trial_ledger 记 llm_extraction_v2,
   旧 literal/llm-v1 trial 记录不抹(K-① · §7-1 记账诚实性)
3. FU-task 完成 → hand-back 交回 IDS → operator 看契约落地证据,
   授权重跑真普查(避免再来一次 61 分钟烧 key 产已知全 0 · K-⑤)
4. E1 真密度数字产出后 → 回 009-pM3prime PRD 的 E1 gate,
   数字 vs 预注册阈值决定是否另行授权 E2/E3
```
适用:verdict converged 且四条款可直接展开 · operator 已知病灶现场。

### [B] 跑 forge v7(说明需要补什么)
```
/expert-forge 009
# 在 Phase 0 intake 时调整 X / Y / Z / W / K
# 旧 v6 整目录保留作历史参考
```
适用:build-time 真跑发现契约有推演盲区(§underweights 第一条 ⚠ 概率非零)· fuzzy 阈值
实证异常 · 金标边界容差问题浮现 · 换模型后 K-③ 模型无关性被挑战。

### [C] 局部接受
- ✅ 采纳:<列本 stage 中确定采纳的条款,如 (A) 输出契约 + (C) census_invalid 硬门>
- ⏸ 挂起:<如 (B) fuzzy 层——先只上 exact+normalized 两层,fuzzy 待 E1 首轮读数后定>
- ❌ 拒绝:<如某条 · 理由>

### [P] Park
```
/park 009
```
保留所有 forge v6 产物,标记暂停。复活时不重做本契约层。

### [Z] Abandon
```
/abandon 009
```
仅当 operator 判定 E1 密度路径整体不该继续(超出本契约 scope · 属 v5 层决策)。

---

## Forge log

- v6: 2026-07-18 — verdict: "extraction proposer 改『引文回锚制』(候选①)+ 四条硬化条款
  (输出契约/分层回锚 fuzzy0.85 审计层/census_invalid 硬门/模型无关预算公式+variant 记账);
  converged · 出口 = XenoDev FU-task 改线后授权重跑真密度"
- v5: 2026-07-16 — verdict: "M3'(信号提取头)提前成立,以最小证伪链推进(E0→E1→E2→E3);
  008→004 通用搬运桥不设 · M1/M2/004 零改"
- v1-v4: 见各 v 目录(009 集合体 gate 演进 · M1/M2 ship)
