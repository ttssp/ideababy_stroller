---
doc_type: forge-stage
fork_id: 009-pM3prime
forge_version: v3
created: 2026-08-13
convergence: converged
open_disagreements: 0
v02_notes: 4
w_forms: [verdict-only, decision-list, refactor-plan]
synthesized_by: main-process(承 v2 先例 · 未起 forge-synthesizer 子代理)
---

# Forge Stage · 009-pM3prime · v3 · "产出信号的那台机器还能不能用"

**双专家**:Opus 5(A 侧)· GPT-5.6-sol xhigh(B 侧)
**触发**:2026-08-12 五条实跑证据(HANDBACK-LOG 第 33 条之后的 build 侧活动)
**收敛**:`converged` · 0 条未解分歧 · 4 条 v0.2 note

## How to read this

前两轮 forge(v1 / v2)审的是**金标标注**——Layer-2 的验收对象成不成立。
**本轮审的是更底层的东西:产出信号的那台机器本身。**

如果你只读一段,读 **§Verdict**。
如果你要动手,读 **§Refactor plan** 与 **§探针实验契约**——后者是本轮唯一的新执行授权,且**带硬上限**。
如果你想知道这份 verdict 哪里可能是错的,读 **§What this menu underweights**——那里有 6 条,其中 2 条是可立即执行的下一步。

⚠ **本轮没有一行 build 侧实证**。所有结论基于对既有实跑数据(PREREG §10)与代码/契约文本的审阅。
这一点在 §underweights 第 1 条被显式记账。

---

## Verdict(W: verdict-only)

**E1 提取器在 v0.1 内可继续使用,但它的单次输出即刻失去「事实」地位。扩样与 E2 继续 blocked。**

四条同时生效:

**(a) 有界语义重试** —— 在宣告一条 record 失败前补应用层重试,覆盖**空 content / 坏 JSON / `usage` 缺失**这三类(SDK 默认的传输层重试**不覆盖**它们,而它们正是两次实跑的失败类型)。这是**落实既有 SLA**「调用失败 → 重试/退避 · **连续**失败 hard-fail」,**零冻结项改动**;重试耗尽仍 hard-fail,KG-40 不动。

**(b) C4 改形态,`pass_semantic: none`** —— 「同文本同版本必同输出」在第三方 API 消费者位置上**原理上不可满足**(修复位点在推理引擎 kernel 的 batch invariance;DeepSeek 官方无 `seed`、无可复现性承诺)。改为**强制测量 + 申报 + 落库 + 身份绑定**(`system_fingerprint` / `service_tier` / 语料内容哈希)。**report-only ≠ optional**。将来若要设门禁,必须升 `caliber_version`,并在**看相关结果之前**预注册口径、阈值、适用模型与校准样本。

**(c) 一次有界预注册聚合探针** —— 仅在 (a) 落地**且**端到端唯一入口交付验收后跑**一次**。硬上限:**有效跑 ≤6 · 尝试 ≤8 · 102 条 · 单跑 ≤35 min · 总计 ≤3.5 h 且 ≤$10,总帽优先**。任一硬帽先触发、或补跑后仍不足 6 个有效结果 ⇒ 整体记 `indeterminate`,**禁止追跑,且不得解释为成功**。判据用 **record-level 配对 bootstrap 的 `Δ = J_agg − J_1`,CI 对 0 判三态**。它**只测本批**跨次信度与**候选**留存;**不得**自称测得真信号留存。`M1 = fail / indeterminate` ⇒ 触发 forge v4;`M1 = pass` **亦不代表效度成立、不能外推、不解锁扩样与 E2**。

**(d) CN/HK 双态改判** —— **执行态 `STOP` 保留**(measurement-invalid 下的 fail-closed),**认识态改 `UNKNOWN`**;旧「真稀疏」判断**作废**。ledger 双记执行态与认识态 + 记明旧理由的失效证据 + 科学重判触发条件。**理由只许来自科学效度,不得诉诸市场价值或商业优先级。**

**路线不改判** —— 但改判的触发条件已被 (c) 的 M1 判据**事前冻结**。

（显式回应 K:①「还能不能往下走」→ 能,但要先把仪器修成可申报的;②「严格性 vs 可跑性」→ **结论出乎意料:实现比 SLA 更严,② 的解是让实现回到契约,不是放松它**;③「接受误差但要定期校准」→ 校准的**义务与形态**已定,**周期与升版责任未定**,降为 v0.2 note 2;④「每条建议一条命令可验证」→ (a)(b) 可以,**(c) 做不到零改动满足**,已写成启动前置条件而非掩饰。）

---

## Evidence map

| 结论 | 来源 | 引用(≤15 words) | `evidence_grade` | 是否有反对证据 |
|---|---|---|---|---|
| C4「同文同版同输出」contract test 只跑 `literal_ticker_proposer` ⇒ 命题恒真 | A-P1 §1 视角C · B-P1 §0 越界读 | "同文同版同输出只跑 literal proposer" | **`independent`**(双方零重叠路径各自 `rg` 到) | — |
| 且 `SLA.md` E1 段把该 **Hard 100%** 要求的**判据栏**直接写成那个测试名 | A-P2 §3 | "提取确定性 \| 同文本同版本 100% 同输出" | `post-hoc-accepted` | — |
| T=0 非确定性主因是 kernel 缺 batch invariance;1000 次补全出 80 个不同结果,修复后全同,代价 ≈2× | A-P2 §1 row1 | "batch invariance 是实际元凶" | **`SOTA-corrected`** | — |
| DeepSeek 官方 Chat schema **无 `seed`、无可复现性保证**;`system_fingerprint` 仅表后端配置 | B-P2 §1 row2 + §3-2(官方文档出处) | "没有可复现性保证" | **`SOTA-corrected`** | — (B 侧写了可证伪点:官方若新增 seed 须重审) |
| ⇒ 「同输出」对 API 消费者**原理上不可满足** ⇒ 病在**契约形态**,不在缺测试 | A-P2 §3 修正 1 | — | `SOTA-corrected` | — |
| SLA §依赖段本就写「重试/退避 · **连续**失败 hard-fail」,而实现单条失败即 `break` + 全回滚 | A-P2 §3 修正 2 → B-P2 §3-1 独立核实 | "SDK 不会重试空 content、坏 JSON、缺 usage" | **`independent`**(B 侧独立核实 SLA 作用域 + SDK 重试边界) | ⚠ B 侧收窄:**只解 ②,不解 ③** |
| trial ledger 的病是 **grain 太粗**,不是 invalid 回滚 | A-P2 §3 → B-P2 §3-3(**撤回自己 P1 的推论**) | "失败运行不入分析 trial 账并非根病" | **`independent`** | — |
| 文献不给阈值与最少 N(Atil 10 次 / NER 最多 30 次,均非普适下限) | B-P2 §3-4 | "没有给本任务最少 N 或稳定性门槛" | `SOTA-corrected` | — |
| 稀有实体在扰动下更脆、错误答案仍可高置信 ⇒ 多数票可能偏向显眼信号 | B-P2 §1 row6(arXiv 2404.05088) | "稀有实体更脆" | **`SOTA-corrected`** | — (把 A-P1 §3-2 的猜测升为有依据的风险) |
| 无独立 validity 锚时,探针**无资格**输出「真信号留存率」,只能输出**候选**留存率 | B-P3R1 §3-1 → **A-P3R2 §1 全盘让步** | "模型重复输出不能兼任预测与真值" | **`independent`**(B 侧独立发现 A 的范畴错误) | — |
| A 侧原停止规则有硬冲突:6 有效跑 + 2 补跑 ≠ N=6,且可达 4h40min | B-P3R2 §1-① | "六次有效跑加最多两次补跑不是 N=6" | `post-hoc-accepted` | — |
| N=6 只有一个 3-v-3 比较 ⇒ **不能 bootstrap run variance**;须改 record-level 配对 `Δ` | B-P3R2 §1-③ | "record bootstrap 只支持本批推断" | `post-hoc-accepted` | — |
| 同批 `J_1` 作**成对**基线**不天然循环**(A 侧自曝的担心不成立);事后改规则才构成过拟合 | B-P3R2 §1-① | "事后调规则才构成过拟合" | `post-hoc-accepted` | ⚠ **推翻 A 侧 P3R2 inbox 里提出的循环性质疑** |
| `P(6 跑全完成) ≈ 35%` 算术正确,但 iid 与 p 点估计未证实 ⇒ **只能作排程依据** | B-P3R2 §1-④ | "只能作排程依据" | `post-hoc-accepted` | ⚠ 收窄 A 侧把该数当作 (a) 必要性论据的用法 |

---

## Intake recap

**X · 9 个标的 · 全部可达 · 无 skipped · 未走 TEXT 兜底**
本仓:`PREREG-census-scaleup.md`(全文)· `PRD.md` v0.9 · v2 stage doc · HANDBACK-LOG 第 28/29/33 条
XenoDev-009:`census.py` · `sampling.py` · `gold_layer2.py` · `specs/009-pM3prime/spec.md` · `SLA.md`
**双方均越界读了** `tests/contract/test_e1_citation_consistency.py`(B 侧另读 `tests/integration/test_census_cli.py`;A 侧另读 `tests/unit/test_llm_proposer_wiring.py`)——**本轮最关键的证据就来自这次越界**。

**Y** · 科学效度(测量工具 · operator 自定义)/ 架构设计 / 工程纪律 —— **未选产品价值**(故 CN/HK 只在科学效度下判)
**Z** · 对标 SOTA(A 侧 5 次成功检索 + 3 次失败;B 侧 12 次)
**W** · verdict-only + decision-list + refactor-plan(**未选 next-PRD**)
**收敛模式** · strong-converge

⚠ **工具故障留痕**:A 侧 `WebSearch` 本 session 全程报 `400 output_config.effort 'xhigh' ...`,5 次检索全部改走 `WebFetch`;
另有 3 次 `WebFetch` DeepSeek 官方文档报 `Socket is closed` —— **该未决事实由 B 侧在 P2 查到并给出官方出处**。
这是一次**工具失败被跨侧兜住**的实例,记账在此。

---

## Verdict rationale

### 病灶不是「测量不准」,是「一个 Hard 契约的验收物是恒真的」

`spec.md` C4 / `SLA.md` E1 / `PRD.md` §7 红线 3 三处写着同一件事:**同文本同版本必同输出(Hard · 100%)**。
它有测试、测试常绿、`SLA` 的**判据栏直接写着那个测试的名字**。

而那个测试把 proposer 换成了 `literal_ticker_proposer`(正则、构造上确定),docstring 自陈「literal proposer 确定性」。
另一侧 `test_llm_proposer_wiring.py` 覆盖了 LLM 路径 20+ 个失败分类分支,其中关于确定性的那条断言的是 **`temperature=0` 被传给了 API**。

⇒ **红线的两半各自被测,红线本身落在两半之间的缝里。** 而这条缝产出的是**正信号**——一条绿的 contract test,挂在一条 BLOCK 级红线下面。
比「从未被检验」更糟一档:**它被检验了,但检验对象被换成了必然通过的那个。**

### 而这条红线本身写错了形态

外部证据把这件事从「我们没做到」改判为「**做不到**」:
T=0 的非确定性主因是推理引擎 kernel 缺 batch invariance(服务端负载 ⇒ batch size ⇒ 归约顺序),
实测 1000 次 T=0 补全出 **80 个不同结果**,换 batch-invariant kernel 后 1000/1000 相同,代价 ≈2×。
**修复位点在推理引擎内部。** 而 DeepSeek 官方 Chat schema **无 `seed`、无任何可复现性承诺**。

⇒ 我们作为 API 消费者,**永远无法满足这条 Hard 契约**。继续挂着它,就是继续生产假绿。
承 v2「数字 vs 形态」判据:把「必须同输出」换成「**在声明边界内测得并申报的稳定性**」是**改形态**(可),不是**挪数字**(禁)。

### 「严格性 vs 可跑性」的答案与直觉相反

operator 在 K 里把核心矛盾定为:放松 fail-closed 会踩 KG-40,不放松则 n=1364 跑不通(P≈1.5%)。

审阅发现**这个矛盾的前提不成立**:`SLA.md` §依赖 SLA 原文写的是
「LLM API 可用性不在本 fork 控制:**调用失败 → 重试/退避 · 连续失败 hard-fail 留错**」。
而实现是**单条失败即 `break` + 全回滚**,per-record 应用层重试为 **0**;
SDK 默认重试只覆盖连接错 / 408 / 409 / 429 / ≥500,**不覆盖**我们实测的空 content、坏 JSON、`usage` 缺失。

⇒ **实现比 SLA 更严,而严的方向恰好制造了「不可跑」。**「**连续**失败 hard-fail」这个措辞本身就预设了「单次失败不 hard-fail」。
**议题 ② 的解是让实现回到既有契约,不需要动任何冻结项,也不触碰 KG-40。**

⚠ B 侧的两处收窄已采纳:(1) 它**只解 ②,不解 ③**(重试治不了 Jaccard 0.44);
(2) `P(6 跑全完成)≈35%` 的算术正确但 iid 与 p 点估计未证实,**只能作排程依据**——
重试义务的正当性来自 **SLA 条文 + 已观察到的瞬态失败**(PREREG §10.4 问题 1:同一条记录重试 3 次一次都没复现),不来自那个概率。

### 关于第三条:只剩一条路,而那条路能不能走本轮答不了

DeepSeek 无 `seed` 已被官方文档坐实 ⇒ **多次采样 + 聚合是仅剩的杠杆**,没有第三个选项可比选。
但外部证据同时给了一个反向风险:**稀有实体在扰动下更脆**,多数票会偏向显眼信号,
**而本项目要找的恰恰是隐性、长尾的那些**。⇒ 聚合可能用「丢掉我们真正想要的东西」换来稳定。

这就是为什么 (c) 是**一次有界探针**而不是一个方案:它要同时量**信度**与**候选留存**,让代价可见。
⚠ 而它**测不了效度** —— 41 条盲标路已 CLOSED,v0.1 内不存在真值锚。任何把 `M1 = pass` 表述为「效度已验」的文档都是口径漂移。

---

## Decision matrix(W: decision-list)

> 第 5 列 `evidence_grade` 承 forge 001 v6(**记录回声室,不消除它**);
> 第 6 列 `obligation path` 承 forge 006 v9 —— **指不出「谁产生、谁消费」的裁决不成立**。
> ⚠ 该列是约束性证明字段,**不是 gate 本身**。

| 项 | 动作 | 评级 | 关键裁决 | `evidence_grade` | `obligation path`(产生 → 消费) |
|---|---|---|---|---|---|
| KG-40 fail-closed **意图** | 保留 | `keep` | 失败不得被解释为真稀疏;重试耗尽仍 hard-fail | `independent` | **`N/A(维持原状)`** |
| 扩样 / E2 历史窗回测 | 保留 | `keep` | 继续 blocked;**`M1=pass` 也不解锁** | `independent` | **`N/A(维持原状)`** |
| 41 条盲标路 v0.1 CLOSED | 保留 | `keep` | 本轮全程未涉;不得作为效度锚复活 | `post-hoc-accepted` | **`N/A(维持原状)`** |
| E1 的 **US go 方向** | 保留 | `keep` | 40 / 73 / 65 三次均 > 30;**不是当初判错** | `independent` | **`N/A(维持原状)`** |
| 引文回锚基础设施 | 保留 | `keep` | 与本轮无关,别拆 | `post-hoc-accepted` | **`N/A(维持原状)`** |
| `census.py` **应用层语义重试** | 新增 | `new` | 覆盖空 content / 坏 JSON / `usage` 缺失;**落实既有 SLA,零冻结项改动** | **`independent`** | `forge:009-pM3prime:v3:phase4 → xenodev:task-review` |
| `system_fingerprint` / `service_tier` **落库** | 新增 | `new` | API 已返回、`resp` 已在手却从不读 ⇒ 漂移无法回溯 | `independent` | `forge:009-pM3prime:v3:phase4 → xenodev:task-review` |
| **语料内容身份哈希**落库 | 新增 | `new` | ledger 只记 source_id 集,不记内容 ⇒ 两批语料不可区分 | `post-hoc-accepted` | `forge:009-pM3prime:v3:phase4 → xenodev:task-review` |
| spec C4 / SLA E1 / PRD §7 红线 3 「100% 同输出」 | **调整** | `refactor` | **改形态**为强制测量 + 申报 + 落库 + 身份绑定;`pass_semantic: none`;**report-only ≠ optional** | **`SOTA-corrected`** | `forge:009-pM3prime:v3:phase4 → **forge:009-pM3prime:phase0**`(warn 三态裁决 · **已接线**) |
| 「100% 同输出」作为**门禁语义** | **删除** | `cut` | 对 API 消费者原理上不可满足;继续挂着 = 持续产假绿 | `SOTA-corrected` | **`N/A(rejected)`** —— 作废项不产生 obligation |
| `test_same_text_same_version_same_output` | **调整** | `refactor` | 现为**净负资产**(对红线给正信号却不承载证据);改为申报型断言或显式标失效 | **`independent`** | `forge:009-pM3prime:v3:phase4 → xenodev:task-review` |
| CN/HK「**真稀疏**」判断 | **删除** | `cut` | 建立在单次读数上,而 per-market 恰是噪声最大的一层(总量差 3% 时 HK 0→4、CN 0→2) | `independent` | **`N/A(rejected)`** |
| PRD §6 CN/HK 结论 | **调整** | `refactor` | 执行态 `STOP` 保留 + 认识态改 `UNKNOWN`;ledger 双记 + 记明旧理由失效证据与科学重判触发条件 | `post-hoc-accepted` | `forge:009-pM3prime:v3:phase4 → ids:prd-edit`(本轮 operator 直接落) |
| **聚合探针 task**(端到端唯一入口 + 配对 Δ bootstrap + 硬上限 + 结果矩阵) | 新增 | `new` | 详见 §探针实验契约;**accept-with-fixes**,五项修复未落地不得启动 | `post-hoc-accepted` | `forge:009-pM3prime:v3:phase4 → **forge:009-pM3prime:phase0**`(结果三态须在下轮 intake 裁决 · **已接线**) |
| `trial_ledger` **grain**(execution/run identity + 模型身份 + 语料身份) | **登记议题** | `refactor` | 病因双方同意,**但新 grain 形态本轮未设计**;会改 DSR/PBO 分母语义,**不宜顺手改** | `independent` | `forge:009-pM3prime:v3:phase4 → xenodev:handoff-intake`(v0.2 note 2) |
| `_N_MAX = 12` 顶满 | **登记议题** | `refactor` | 是内容不稳定的候选机制之一,**因果本轮未测**;可作 (c) 顺带观测,**不得成为判据** | `post-hoc-accepted` | `forge:009-pM3prime:v3:phase4 → xenodev:handoff-intake`(v0.2 note 3) |

---

## 探针实验契约(finalized · B 侧 `accept-with-fixes` 的五项修复已并入)

**启动前置(全部满足才准跑,缺一即不跑)**

1. **(a) 有界语义重试已落地并通过 review**
2. **端到端唯一入口已交付并验收**(含验收测试)—— B 侧裁定「将来由新脚本计算」**不满足**唯一命令要求
3. 本契约的四类上限、三态判据、结果矩阵**逐项写进 task 卡**

**硬上限(总帽优先 · 任一先触发即停)**

| 上限 | 值 |
|---|---|
| **有效跑** | **≤ 6**(拆成两个**不相交**的 3 次子集,用于比较「聚合 vs 单次」) |
| **尝试次数** | **≤ 8**(有效跑 + 补跑合计) |
| 记录数 | **102 条**(= `--sample-size 40` + 原始 `collection.db` + `caliber_version=v1` 的确定性抽样结果,与已有三次读数**同一批**) |
| 单跑墙钟 | **≤ 35 min**(超时即 abort 该跑) |
| **总墙钟 / 总花费** | **≤ 3.5 h** / **≤ $10** —— **覆盖补跑,且优先于跑数上限** |

⚠ **102 条只作 fixed-batch 校准。禁止外推到扩样语料;`M1 = pass` 也不解锁扩样 / E2。**
⚠ 任一硬帽先触发、或补跑后仍不足 6 个有效结果 ⇒ **整体记 `indeterminate`,禁止追跑,不得解释为成功。**

**判据(全部为比较型 · 不含事前拍的绝对阈值)**

| 指标 | pass | fail | indeterminate |
|---|---|---|---|
| **M1 · 聚合是否提高本批可复现性**<br>对**同一 record** resample,计算配对差值 `Δ = J_agg − J_1` 的 bootstrap CI | CI **全部 > 0** | CI **全部 ≤ 0** | CI **跨 0** ⇒ **无区分力** |
| **M2 · 候选留存率**<br>k-of-3 多数票后候选数 / 单次候选数中位数 | — | — | **无 pass 语义,全量申报** |
| **M3 · 留存的分层结构**<br>候选按「出现在几次跑里」分层的分布 | — | — | **无 pass 语义,只申报**;若留存几乎全是高频候选 ⇒ 按 arXiv 2404.05088 预期**显式记录该风险** |

> `J_1` = 单次读数两两 Jaccard;`J_agg` = 两个 3 次聚合结果间的 Jaccard。
> ⚠ **同批 `J_1` 作成对基线不天然循环**(B 侧裁定);**事后调规则才构成过拟合**。
> ⚠ N=6 只有**一个** 3-v-3 比较 ⇒ **不能 bootstrap run variance**;record-level bootstrap **只支持本批推断**。

**预先承诺的结果矩阵(反 p-hacking · 事后不得改)**

| 结果 | 处置 |
|---|---|
| `M1 = fail` | **触发 forge v4 议路线**;M2/M3 仍全量申报 |
| `M1 = indeterminate` | **同样触发 forge v4**(不得当作「再跑跑看」) |
| `M1 = pass` · `M2 ≥ 50%` | 只证明**本批**信度改善;**不证明效度、不外推、不解锁 E2** |
| `M1 = pass` · `M2 < 50%` | 同上,**并加注候选损失**;若 E2 将来消费聚合语料,其密度读数**不得与历史 41 / 73 / 71 直接比较**(不同测量对象) |

> 🔴 **AMENDMENT · 本表两行 `M1 = pass` 的处置被 forge v4 supersede(2026-08-14)**
>
> **上表原文一字未改**(承 v4 ④ 裁决:历史不可变,授权被后续版本 supersede,不得追改)。
> 本块只声明:自 2026-08-14 起,读本表 `pass` 两行时**必须**连同本块一起读。
>
> **被 supersede 的内容**:上表 `pass` 行只写了「不证明效度、不外推、不解锁 E2」,
> **未写 pass 是否仍欠一次裁决动作**。⇒ T015 hand-back(`009-pM3prime-20260813T155648Z` §3 action #2)
> 据此读成「M1=pass **不**自动触发任何操作」,**且未标注这是一次口径选择**。
>
> **v4 终裁(采广读)**:**`M1 = pass` 同样欠一次具名裁决。**
> 依据是载体分布 **3:2** —— 广读在本文档**正文**(「结果三态**必须**回到 forge v4 裁决」)、
> 本文档 **#decision-matrix 聚合探针行**(「结果三态须在下轮 intake 裁决 · **已接线**」)、
> `OB-009-pM3prime-v3-07` **标题**;窄读只在**本表**与该义务的 **note**。
> **少数派口径此前赢了,赢的方式是它更靠近执行者。**
>
> **pass 分支的裁决动作**(v4 已代为执行一次):接受为**固定批可比性**证据 ·
> 不作效度代理 · 不外推 · 不解锁扩样与 E2;rationale **必须**载明两项风险输入 ——
> (i) 一致率上升无法区分噪声去除与**歧义抹除**;(ii) 6 跑 `census_verdict` **全部** `below_threshold_advisory`。
>
> **Source**: `discussion/009/009-pM3prime/forge/v4/stage-forge-009-pM3prime-v4.md`(verdict ① · decision matrix #1)

**停止规则**:6 个有效结果或任一硬帽,先到先停。**不因结果难看加跑。**

---

## Refactor plan(W: refactor-plan · **顺序是硬的**)

**① `census.py` · 重试 + 身份落库**(解议题 ② 与 ①)
- 应用层语义重试:空 content / 坏 JSON / `usage` 缺失,有界次数 + 退避;耗尽仍 hard-fail
- `system_fingerprint` / `service_tier` 落库
- 语料内容身份哈希落库
- ⚠ **不动** R10 早停的**意图**(重试耗尽后仍走原路径)

**② 契约文本同步改形态**(解 C4 假绿 · **可与 ① 并行**)
- `spec.md` C4 / `SLA.md` E1「提取确定性」行 / `PRD.md` §7 红线 3 —— 三处同步,`pass_semantic: none`
- `test_same_text_same_version_same_output` 改为申报型断言或显式标失效
- `PRD.md` §6 CN/HK 双态 + ledger 双记
- ⚠ **三处必须一起改**,漏一处就还剩一个假绿源

**③ 聚合探针 task**(**依赖 ①** · 交付端到端唯一入口 + 配对 Δ bootstrap + 硬上限 + 结果矩阵,验收后**跑一次**)

**③ 完成前不得扩样。** `trial_ledger` grain 与 `_N_MAX` 归 v0.2 note,**不进本次 refactor**。

---

## v0.2 notes(残余分歧降级 · 双方一致)

1. **validity 无真值锚,公开未解。** 41 条盲标路 CLOSED ⇒ v0.1 内不存在效度锚。聚合能不能保住构念效度,**v0.1 内无法回答**。**任何文档不得把 `M1 = pass` 改写为「效度已验」。**
2. **校准周期、升版责任、`trial_ledger` 新 grain 待单独设计。** 测量**义务**已定形(b),但「多久跑一次 / 谁负责 / 变到什么程度触发升版」未定;新 grain 会改 DSR/PBO 分母语义,**避免顺手改**。
3. **`_N_MAX = 12` 顶满的因果未测。** 零成本可证伪(放宽上限看提案数分布是否仍顶满),可作 (c) 顺带观测,**不得成为本探针判据**。
4. **A 侧「三次被证据推翻」作为 forge 机制的过程注记纳入**(B 侧裁定 `include`):它说明**交叉裁决捕获了一次单侧自检遗漏**(第三次是 B 侧发现的,前两次是 A 侧自查)。**不得写进技术结论,也不得由单例泛化。**

---

## What this menu underweights(强制自批判)

**1 · 本轮零 build 侧实证。** memory `forge-verdict-vs-empirical-ship` 明写:forge 的理论技术决议会漏实证盲区,且给了正面解法——**实现选择类条款应写成「A + 判据 + 证不出则 B」的 fallback 分支 + build 侧预置同轴熔断**。
🔴 **本 verdict 的 (a) 没写 fallback**:重试几次?退避形态?若重试后失败率不降(说明失败不是瞬态)怎么办?
**这是本轮最像 v1 失败模式的一处。**

**2 · 只查了 C4,没查其它 Hard 契约。** 我们发现 C4 的验收物是恒真的,**是因为证据把我们指到了那里**。
`spec.md` 还有 C1 / C2 / C3 / C5 / C7 / C13 等多条 Hard 契约,**它们的「判据」栏是否也写着一个恒真或近恒真的测试,本轮没查。**
⇒ **这是一条零成本、可立即执行的下一步**(逐条比对 Hard 契约的判据测试是否用了 mock / literal / 构造上必然通过的替身)。

**3 · 探针可能什么都测不出。** B 侧自己判:record-level bootstrap **只支持本批推断**,N=6 只有一个 3-v-3 比较。
3.5 小时可能买到的是「本批上聚合有改善,但不能外推」——**这在决策上接近于零**。
结果矩阵已把 `indeterminate` 与 `fail` 同等对待(都触发 forge v4),这是防线,但**不改变可能白花 3.5 小时的事实**。

**4 · `_N_MAX` 被排在探针后面,可能顺序错了。** 它是**唯一零成本可证伪**的机制假说。
若它就是主因,我们会先花 3.5 小时测聚合,回头才发现**改一个常量能解决大半**。
把它排除在判据外是对的(防判据膨胀),但**排在执行顺序后面未必对**。

**5 · (d) 只改了标签,没改机制。** CN/HK 从「真稀疏」改成 `UNKNOWN` 是诚实的,
但**没有任何机制防止下一次又用单次读数下 per-market 结论**。(b) 的申报义务是 corpus 级的,不是 per-market 级的。

**6 · 回声室。** 双方都是 LLM,读同一批文档。B 侧确实带回独立证据(官方文档 / arXiv 2404.05088)并**三次推翻 A 侧**,这是真实的独立性。
但**框架是 A 侧 P1 定的**(「把一次读数当事实」),B 侧此后都在这个框架内做修正。
**没有人提出根本不同的框架**——例如「散文→可回测信号这条路本身该换成规则抽取 + 人工确认」。
K 里 operator 问的正是这个,而**双方都选择了「不改判」**。这个共识**可能是对的,也可能只是同一类模型的共同盲区**。

---

## Decision menu(for human)

### [A] 接受 verdict → 改 PRD/spec/SLA → 回 XenoDev 实装(推荐)

顺序:② 契约文本(IDS 侧 PRD + XenoDev 侧 spec/SLA)→ ① `census.py` → ③ 探针 task。
⚠ 接受本项即同时接受:探针在五项前置未落地前**不启动**,且其结果三态**必须**回到 forge v4 裁决。

### [B] 接受 verdict 但**先做 §underweights 第 2 条**(零成本,可能改变优先级)

先逐条比对 `spec.md` 其余 Hard 契约的判据测试是否用了构造上必然通过的替身。
若发现 C4 不是孤例 ⇒ **问题从「一条红线写错」升级为「验收体系性失效」**,那时 (b) 的范围要重划。
**成本:一次 `rg` + 人读。**

### [C] 局部接受:只做 (a)(b)(d),**探针 (c) 押后**

理由:§underweights 第 3 + 4 条 —— 探针可能白花 3.5 h,而 `_N_MAX` 零成本假说还没测。
改为:先做 (a)(b)(d) + `_N_MAX` 顺带观测,**据其结果再决定要不要探针**。
⚠ 代价:「路线改判判据」会失去它的触发器(M1),需另立。

### [P] Park —— 全部照现状冻结,不做任何改动

⚠ 后果必须写明:**假绿的 C4 contract test 继续常绿**,下一个读到它的人(或 agent)会继续相信那条红线有覆盖。

### [Z] Abandon —— 判定「散文 → 可回测信号」路线不可行

本轮**双方都不建议**,但 §underweights 第 6 条指出这可能是共同盲区。
若选此项,应先起一场**换框架**的 forge(明确指定「反对 LLM 抽取」为一侧立场),而不是直接 abandon。

---

## Forge log

| Phase | A 侧(Opus 5) | B 侧(GPT-5.6-sol xhigh) | 结果 |
|---|---|---|---|
| **P1** | 越界读 `test_llm_proposer_wiring.py`,发现红线两半各自被测 | 越界读 `test_census_cli.py`,独立发现 C4 只跑 literal proposer | 双方 `CONCERNS` · **零重叠路径同得** · 三视角倾向一致 |
| **P2** | 5 次成功检索(WebSearch 工具故障,全走 WebFetch);**推翻自己 P1 两条** | 12 次检索;**查到 DeepSeek 无 seed 的官方出处**;**撤回自己 P1 一条** | 双方 `CONCERNS` · 各自撤回 · A 的未决事实被 B 兜住 |
| **P3R1** | 标 3 条分歧;**§4 自检自曝「(c) 就是一个实验」的债务** | 3 条全表态(2 条 A 采 B 措辞);**新提分歧 4**;立准入条件「缺一即反对」 | 分歧 3→4 · A 欠债 |
| **P3R2** | **分歧 4 全盘让步**(范畴错误);偿付四类上限 + 三态判据 + 停止规则 | **验收而非称赞**:`accept-with-fixes` 五项;修停止规则硬冲突;修 bootstrap 形态;**推翻 A 自己提的循环性质疑** | **`converged`** · 0 未解 · 4 条 v0.2 note |

**A 侧本轮被推翻 3 次**:P2 两次(自查)· P3R2 一次(**B 侧发现**)。
**B 侧本轮撤回 1 次**(trial ledger 病因)。
—— 记账在此,不作技术结论(v0.2 note 4)。
