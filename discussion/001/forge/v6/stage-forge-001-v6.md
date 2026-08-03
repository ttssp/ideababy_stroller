# Forge Stage · 001 · v6 · "池分区键定生死:comparability_class 前置冻结 · block-PASS 出口关闭 · chair 条款"

**Generated**: 2026-08-03T20:40:00Z
**Source**: forge run v6 with X = 9 标的(IDS 4 件 + XenoDev worktree 5 件), Y = 架构设计 · 工程纪律, Z = 对标 SOTA, W = **decision-list only**
**Convergence mode**: strong-converge
**Rounds completed**: P1 (both · ⚠ Codex 侧重跑一次,污染轮归档 `_contaminated-p1/`), P2 (both), P3R1 (both), P3R2 (both)
**Searches run**: **5 次**(全部在 GPT 侧,覆盖 6 个独立来源:CVE FAQ / CVE schema / NVD API / Cochrane ch.10 / BMJ / RFC 7282)+ **Opus 侧 0 次有效检索** —— `WebSearch` 后端故障(400 · effort xhigh · 3 次同错),改定向 `WebFetch`,**不计检索**
**Moderator injections honored**: none(`forge/v6/moderator-notes.md` 不存在)
**Convergence outcome**: **converged**(双方 P3R2 §2 单一 verdict 对齐,GPT 明写「无 unresolved」)
**触发源**: HANDBACK-LOG 决议 40 (3) 池分区键 + (1) needs-attention 等价放行跨层复发 · operator 选 [1]
⚠ **v5 声明的既定 v6 判据(warn 候选过 `review_by` 后无证据仍被续期)本轮尚未触发** —— 触发本轮的是决议 40 的**新增触发器**,两者并列不替代。

> ⚠ **两项 synthesizer 质量栏未过 · 具名声明(非静默超标)**
> 1. **正文约 5,000 CJK 字符,超 4000 上限约 25%。** 被砍掉的会正好是 8 行 fallback 列的**三要素**
>    (谁 / 何时 / 既有结论怎么办)—— 而 v5 的 fallback 正是缺这三件才被 codex 连打三轮,
>    **它们是本轮召开的理由本身**。承 v5 v0.2 note 3 裁定(「宁可超标具名声明,禁有损机械压缩」);
>    本轮双方 P1/P2/P3R1/P3R2 四份文档亦均已具名超标。
> 2. **§"Verdict" 约 340 CJK 字符,超 200 上限**,且**按 forge-config 的 W 约束折进
>    §"Decision list" 开头作 `### Verdict`,不单列成 h2 段**(这是 operator 明确要求,不是遗漏)。
>    压到 200 会掉掉 8 项互锁裁决里的「PASS 重开前置」与「追溯二态」两组限定 —— 那正是承重条款。

---

## How to read this

forge 是横切层(不是 L1-L4 pipeline 的一部分)。本文档是双专家(Opus 4.7 Max + GPT-5.5 xHigh)
审阅 + SOTA 对标 + 两轮联合收敛的产出,**强制给出立场**。

**本轮不是 v5 的续集,是 v5 的第一次实战回检。** 审的是三样 v5 自己产出的东西:v5 主动降级为
v0.2 note 的那条(池跨方向可比性,被 codex 三轮独立判 high)· v5 新造的 §0.1 判据冻结前置
(第一次应用就判了 v5 自己的 item 2 不具冻结资格)· v5 的 fallback 分支第一次被真实触发。

**W = decision-list only**(operator 明确不要 verdict-only / next-PRD / refactor-plan)。
故**单一 verdict 折在 §"Decision list" 开头,不单列成段**;涉及 PRD / 多文件改造的裁决全部落在
「落点」列。读完后你应该能直接从 §"Decision menu" [A] 的执行顺序进入下一步动作。

---

## Evidence map

| 结论 | 来源 | 引用(≤15 words) | 是否有反对证据 |
|---|---|---|---|
| 池仅按 `epoch + rubric` 分区,方向只进去重 ⇒ 可跨不相干方向借数 | X-6 codex round-3/4/5(三轮 high)· 双方 P1 §1 | "predeclared comparability-class identifier" | - |
| `direction` 在去重键抬高计数、在分区键不限借用 = 同一字段两处反向使用 | P1-Opus §1-A1 | "direction 被用来抬高计数,却不被用来限制借用" | ⚠ GPT P2 §3「我未想到…读 spec 后认同病灶」= 事后同意,非独立复现 |
| 可比性是 pooling 的**准入前提**,不是事后修补项 | P2-Opus §1 row1(Cochrane ch.10) | "仅当被判定为充分相似才做 meta-analysis" | ⚠ 被 P2-GPT 部分修正(见下一行) |
| v5 不是全错 —— 错在把**探索性**池化的出口写成可放行 PASS | P2-GPT §1 row3(Cochrane + BMJ)→ P3R1-Opus §1-3 接受 | "retrospective subgroup 可产假设,不应指导实践" | Opus P2 原判「方向反了」**已被修正为只对 block-PASS 出口成立** |
| `needs-attention` 不是 veto;缺的是 chair 这个角色 | P2-Opus §1 row4 · P2-GPT §1 row4(RFC 7282) | "addressed, but not necessarily accommodated" | Opus P1 §1-B3 原框架(「不应合入⇒必须不合」)**已被自己 P2 推翻** |
| 「标注 + 通知」挡不住下游继续消费 ⇒ 必须消费点 fail-closed | P2-Opus §1 row5(retraction 实证) | "已标 retracted 的论文仍继续被引用" | - |
| `REJECTED`(应被过滤)与 `DISPUTED`(保留待核实)是**两态**,不是一态 | P2-GPT §1 row1/row2(CVE FAQ / schema / NVD) | "NVD 提供 `noRejected` 过滤 / `cveTag=disputed` 查询" | Opus P2 把二者压成单态 fail-closed,P3R1 §1-2 **自认过粗**并接受 |
| ⭐ 至今**零**真实 O2/P2 PASS 被旧池消费 ⇒ 迁移表实测零项 | P2-GPT §2 仓内实查 · 双方 P1 §3 各自提出 | "非豁免判断 1 条 <3,不得据以判 O2 / §7-P2 PASS" | -(本轮唯一「独立提出 + 实查证实」行) |
| 零受影响必须写成核查结果,不得靠沉默推断 | P2-GPT §2 | "不要靠沉默推断" | - |
| 当前**没有合格消费点**;最近的消费面是 `evaluate` 落盘产物与 journal snapshot | P2-GPT §2 | "当前没有合格消费点" | - |
| T041 是 phase-4 测量工具,交付物不是运行时契约 ⇒ 扩 `file_domain` 也是错配 | P1-Opus §1-B1 | "T041 `depends_on:[T040]` ⇒ 该协议被双重阻塞" | ⚠ GPT P1 只到「file_domain/owner 缺口」,P2 §3 才「认同更强表述」 |
| 三态接口 owner 与消费点 fail-closed 必须**同一个 task** | P3R1-GPT §3-D4 → P3R2-Opus §1-D4 全额接受 | "接口只是标签、消费点无输入" | - |
| §0.1 已把 O2 PASS 向定成事实 warn ⇒ T040 隔离条件**由 spec 给出**,不需另证 | P3R1-Opus §3-D2 → P3R1-GPT §3-D2 确认 | "隔离已由 spec 给出" | GPT P1 原主张「不能隔离则等 v6 后起跑」**已撤回** |
| 实查 `tests/contract/` 不存在 ⇒ T040 零进展是拖延,不是 v5 fallback 生效 | P1-Opus §1-B2 | "是拖延,不是 fallback 生效" | - |
| 「事后同意」不得与独立收敛同权,且该规则须**对双方对称适用** | P3R1-GPT §3-D3 → P3R2-Opus §1-D3 让步 | "我原来的提法是单向的、对我自己有利" | - |

---

## Intake recap

### X · 审阅标的(9 件 · 全部 2026-08-03 实测可达)
**IDS 侧 4 件**:`forge/v5/stage-forge-001-v5.md`(343 行 · 本轮直接上游)· `HANDBACK-LOG.md`
(1068 行 · 40 条决议 SSOT)· hand-back 包 `20260802T162313Z`(147 行)· `PRD.md` v1.7(215 行)。
**XenoDev worktree 侧 5 件**(权威副本在 worktree):`spec.md` v0.7 `frozen`(462 行 · 主战场)·
⭐ `review-log/001-radar-pA-spec-v07/round{1..5}-codex-raw.log`(6 文件 211 行 · v5 时不存在的新证据)·
`tasks/T021.md` · `tasks/T040.md` · `tasks/T041.md`。

### Y · 审阅视角
**架构设计**(池分区键 = 集合级判据的边界设计 · 「撤销既有 PASS」的下游语义 · `file_domain` 覆盖性)
+ **工程纪律**(「reviewer 说不合入」的约束力 · T040 起跑前提 · spec→task 移交的机器校验)。
⚠ 声明的盲区:**未选安全**(v5 §underweights 曾建议 v6 补,operator 明确不加)· **未选产品价值**
(⇒ 本轮不从产品侧重开阈值存废,只裁分区与追溯)。

### Z · 参照系
mode: **对标 SOTA**,建议面三条(累积证据池的分区/分层 · 「评审反对但仍合入」的治理先例 ·
已发布结论的撤销/版本化)。用户外部材料:**无**。
⚠ **本轮 Z 严重不对称**:GPT 侧 5 次检索可用;Opus 侧 `WebSearch` 全程故障,只能定向 `WebFetch`
⇒ **Opus 侧本轮无任何负结果有效**(承 v5 教训,Opus P2 顶部已自行封杀该类结论)。

### W · 产出形态
**decision-list**(四列矩阵 + 本轮加第 5 列 `evidence_grade`)· **唯一形态**。
交叉验证:本文档只产 §"Decision list" 一个 W 章节,**无** verdict-only / refactor-plan / next-PRD 段。

### K · 用户判准(核心两问)
> (a) 一个「集合级判据」的分区键怎么定,才不会让「凑够数」变成「借不相干的数」?若事后证明借错了,
> 已经放行的结论要不要追溯——追溯的下游语义由谁定义?
> (b) 当评审说「不应合入」而落地方说「披露即可合」时,谁的话算数、以什么形式算数?

关心:**要能执行的裁决不要正确的综述** · **回检 v5 的四列范式本身**(fallback 第一次被真实触发,
要看它写得够不够可执行)· **追溯成本正面算**(v6 裁的是「已经放行过的结论要不要撤」)。
硬约束:fallback 列必须写明**谁触发 · 什么时点 · 触发前已放行的结论怎么办**;判据列的 Feasible 栏
不接受推演;**禁止用「已显式披露」作任何一项的判据或 fallback**。

### 收敛模式
**strong-converge** —— 单一 verdict;残余分歧降级 v0.2 note,且**每条 note 必须带具名触发时点
与在此之前的风险敞口**(禁「首次实施时复核」这类无主体无时点措辞 —— v5 note 1 正是那样写的)。

---

## Decision list(W = decision-list only · 5 列 · 8 项)

### Verdict(单一 · strong-converge · 按 W 约束折在本节开头,不单列成段)

**池化机制保留,但它的 block-PASS 出口现在关闭,降为探索/warn 出口** —— v5 的错不在池化,
而在把一个 post-hoc 的**探索性**机制的出口写成了可放行 PASS。**PASS 出口重开的前置**:池键改为
`decision_epoch + rubric + comparability_class` 且在 epoch 开启时冻结为不可变,`direction` 进比较类
**退出去重计数**,去重身份改 stable claim identity。**追溯采二态**(CVE 先例):已证无效 →
`rejected-like`(消费点机器可拒);存疑 → `disputed-like`(保留但不得当 clean PASS 消费);
**fail-closed 落在消费点判定上,不落在通知/标注上**。**关键实测**:仓内核查确认**零**真实 O2/P2 PASS
被旧池消费 ⇒ **现在立规则最便宜**,但零受影响必须落成具名核查记录。**`needs-attention` 不是 veto**
(RFC 7282),但 override 只能由 **operator-chair** 逐条写明 concern 如何被 addressed,
**spec-writer 不得自任,无 chair 记录不得声称 clean PASS**。**T040 立即局部起跑**;
**三态接口 owner 与消费点 fail-closed 合为一个具名新 task,不塞 T041。**

⇒ 直接回应 K:**(a)** 分区键 = 预声明的 `comparability_class`,追溯二态 + 消费点 fail-closed,
下游语义由 **operator-chair** 定义;**(b)** reviewer 非 veto,chair 的**逐条书面 addressed 记录**算数,
「披露」属 noted 侧不属 addressed 侧 —— 这也是 config 禁用「已显式披露」作判据的理由。

### 8 项矩阵

| # | A(裁决) | 判据(Feasible 栏不收推演) | 证不出则 B(fallback:**谁 · 何时 · 已放行结论怎么办**) | 落点 | `evidence_grade` |
|---|---|---|---|---|---|
| 1 | **池键加 `comparability_class` 并在 epoch 开启时冻结为不可变**:键 = `decision_epoch + rubric + comparability_class`;未预声明可比较类 ⇒ **不得借池 PASS** | 历史证据:codex round-3/4/5 三轮判 high(round-3 要求预声明可比较类标识,round-4 加「使既有 PASS 失效/重评」)。SOTA:Cochrane 把充分相似设为 pooling 准入前提。**Feasible**:池化路径机器侧从未实装、零真实 PASS(P2-GPT 实查)⇒ 改键**零迁移**,可达性由实测事实支撑 | **谁**:operator(chair)。**何时**:spec-writer 提交 v0.8 amendment、请求 chair 验收的那一刻(可观察 = v0.8 的 review 请求出现在 `review-log/`)。**证不出**(给不出可判定的类标识)⇒ 该 epoch 一律只出 `INSUFFICIENT_EVIDENCE`,**不得出 PASS**,且不设自动到期重开。**已放行结论**:实测零项(见 #5);若核查发现非零 ⇒ 全部先入 `needs-revalidation`,下游按非 PASS 处理直至重验 | `spec.md` §1-O2(c)(worktree `:181-201`)+ §6 O2 行(`:393`);`T021.md` ⑤⑥ 断言。**PRD 不改**(v1.7 O2 已澄清「集合验收采样口径」)。⚠ 落地以 **v0.8 最终措辞**为准,不以本文档措辞为准(承 K 理由 5:施工单会 stale) | `independent` ⚠ 见 underweight-1 |
| 2 | **`direction` 退出去重计数、去重身份改 stable claim identity**:`direction` 进分区/比较类;同 claim 跨方向 = 同一 claim 的两次观察,**不计 2 条** | P1-Opus §1-A1:同一字段在去重键抬计数、在分区键不限借用,净效应最大化跨方向凑数。spec 自陈 claim 语义身份未定义(同义改写 / 仅换锚 / 跨 epoch 重复三攻击面)。⚠ **Feasible 诚实标**:stable claim identity 算法**尚无真跑证据** ⇒ 按 §0.1 只能 warn 侧上线(见 note-2) | **谁**:T021 owner 提交算法 + 反例测试,**operator-chair** 验收。**何时**:T021 提交并请求 chair 验收那一刻(可观察 = T021 的 review 请求)。**证不出**稳定 identity ⇒ 去重维持现状但 **PASS 向持续 warn**,不得转 block-PASS。**已放行结论**:零(同 #5);若非零按 `disputed-like` 处理 | `spec.md` §1-O2(c) 去重条 + §0.1 转正条件②;`T021.md`(`:31/:44/:60` 仍是 v0.6 单 run 阈值 + 三处已删的 `OQ-A1-1` dangling 引用) | **`post-hoc-accepted`** |
| 3 | **block-PASS 出口关闭,池化降为探索/warn 出口**;重开前置 = #1 + #2 落地 ∧ note-2 闭合 | SOTA:Cochrane 允许「sensible and honest」post-hoc 探索但须标明;BMJ:回溯性分组可产假设、不应指导实践 ⇒ 探索性池化正当,写成可放行 PASS 不正当。**Feasible**:§0.1 第一次应用已把 PASS 向判为事实 warn 态 —— 关闭出口只是把既成事实写进规范,不新增可达性负担 | **谁**:operator(chair)。**何时**:#1 + #2 落地后的首次 v0.8 amendment 验收会。**证不出**(#1 或 #2 任一被证不可达)⇒ block-PASS 出口**保持关闭且不设期限**,O2 长期停 `INSUFFICIENT_EVIDENCE`;⚠ **不得以「已显式披露」为由重开**(config 硬约束)。**已放行结论**:零项(核查记录);若非零 ⇒ `rejected-like` | `spec.md` §1-O2(c) 出口语义 + §0.1 自检条。⚠ **必须给 gate 等级的机器可读形式**(P1-Opus §1-A3:「PASS 向 warn / FAIL 向 block」目前只以散文存在,T040 无法为它建测) | **`SOTA-corrected`** |
| 4 | **追溯采二态,fail-closed 落在消费点**:已证无效 → `rejected-like`(消费点机器可拒);存疑 → `disputed-like`(记录保留、不得当 clean PASS 消费)。**不靠通知/标注** | SOTA:CVE FAQ/schema —— REJECTED 记录原则上应被忽略、留存只为告知无效;NVD 提供 `noRejected` 过滤与 `cveTag=disputed` 查询 ⇒ **二态有机器开关先例**。反面实证:已标 retracted 的论文仍继续被引 ⇒ 标注挡不住消费 | **谁**:#8 新 task 的消费点 owner(机器侧执行)+ **operator-chair** 认定状态词。**何时**:消费点 verifier **第一次读到非 clean 状态**时(机器时点,写进 verdict artifact);状态认定由 chair 在 `/handback-review` 留痕。**证不出**(消费点 task 未就位)⇒ 任何 O2/P2 PASS 声称一律不成立(fail-closed 缺省)。**已放行结论**:实测零项;若非零 ⇒ 一律先入 `disputed-like`,由 chair 逐条判 `rejected-like` 或重验 | `spec.md` §1-O2(c) 追溯语义段 + §7-P2;#8 新 task 的消费语义定义;HANDBACK-LOG 决议 40 (3) 的 follow-up 条目 | **`SOTA-corrected`** |
| 5 | ⭐ **落一份具名「零受影响 PASS 核查记录」**:实测 `out/` 仅 `coding-llms-20260802T022608Z.md` + `evaluations.jsonl` 一行,两者均明写不得据以判 PASS;`a1-selfcheck.jsonl` 的 `predicate_passed` 属 T010/T011 解锁自证 ⇒ **迁移表 = 零项**。**零受影响是核查结果,不是默认值** | 双方 P1 §3 **各自独立**提出该事实问题(Opus §3-2 / GPT §3-3),GPT P2 §2 **仓内实查证实**(worktree + 主副本 `out/` 全查)。这是本轮唯一「独立提出 + 实查证实」的结论 | **谁**:执行核查的 agent(记名)+ operator 签收。**何时**:**v0.8 amendment 提交前** —— 核查记录是 amendment 的**必带附件**,缺则 amendment 不予验收。**证不出**(核查发现**非零**旧 PASS)⇒ 立刻按 #4 二态处置(全部先入 `disputed-like`),并把迁移表写进 v0.8 **且触发 v7**(见 §underweights)。**已放行结论**:本行本身就是「触发前」的清点动作,无遗留 | 新增核查文件(建议 `<W>/review-log/001-radar-pA-spec-v08/pass-migration-audit.md`)+ HANDBACK-LOG 新决议条目引用 | **`independent`** ⭐ 本轮最强行 |
| 6 | **chair 条款**:`needs-attention` **不是 veto**;override 合法,但只能由 **operator-chair** 作出并**逐条写明 reviewer concern 如何被 addressed**;`/handback-review` 是闸点与留痕、**不是 chair 本身**;**spec-writer 不得自任**;**无 chair 记录不得声称 clean PASS** | SOTA:RFC 7282 —— rough consensus 要求 issue 被 addressed 而不必被 accommodated,须给反对者 reasoned explanation,**由 chair 认定**;addressed(实质考量)vs merely noted(承认但忽略),后者不构成 consensus。**历史证据**:round-5 原文 summary「不应合入」;v0.7 的可否 ship 由 spec-writer 自批,reasoned explanation 从未回给 codex(五轮各自独立无回路) | **谁**:operator。**何时**:每次 hand-back 入库时 `/handback-review` 决议**落笔那一刻**(逐条 override 或不 override,二选一,不得留白)。**证不出**(chair 记录缺席)⇒ 该 amendment 只保留为 **provisional spec**,可作下一版输入,**不得援引为 O2/P2 PASS 权威**。**已放行结论**:**已 commit 的 v0.7 追认为 provisional**(不撤 commit),其 O2/P2 权威性即刻悬置,直到 chair 逐条记录补齐 | v0.8 amendment frontmatter / Amendment log;HANDBACK-LOG 新决议条目。⚠ 该规则的**一般化形态**(全仓所有 idea 的 reviewer verdict 约束力)属 framework 层 ⇒ **归 `/expert-forge 006`**,本轮只在 001 落地 | **`SOTA-corrected`** |
| 7 | **T040 立即局部起跑**:6 个测文件中 **5 个非 O2 文件建 block 测**;`test_o2_exemption_contract.py` 的 (c) 条只建 **warn-only 断言 + versioned baseline**;**不得把 O2 PASS 面做成 block** | §0.1 自检已把 O2 PASS 向定成事实 warn ⇒ **隔离条件由 spec 给出,不需另证**(双方 R1/R2 确认)。**Feasible**:`depends_on:[T030,T031,T032]` 三者已 ship;实查 `tests/contract/` 不存在 ⇒ 零进展是拖延不是 fallback 生效,且 v5 item 8 自带 fallback 正好覆盖本形态 | **谁**:T040 builder(XenoDev 侧)+ operator 验收。**何时**:起跑后**首次 `pytest tests/contract/ -q` 全绿并提交 baseline** 时(可观察 = worktree 上出现该 baseline 文件)。**证不出**((c) 条连 warn-only 断言都无落点,如池无持久化对象可断言)⇒ (c) 条**只记 baseline 不建断言**,其余 5 文件照常 ship,**不阻断**。**已放行结论**:无(T040 零进展,无既有放行) | `<W>/specs/001-radar-pA/tasks/T040.md` + `tests/contract/`。⚠ **(c) 条断言形态依赖 #1/#2 的 v0.8 最终措辞** ⇒ 排期上「接受一次返工」或「(c) 排在 v0.8 之后」二选一,**别装无依赖**(同决议 40 (4) 的处置) | `independent` ⚠ 见 underweight-2 |
| 8 | **新起具名 task(不塞 T041),合并两件事**:① 三态(`PASS` / `INSUFFICIENT_EVIDENCE` / `FAIL`)的 CLI 退出码 + 产物状态字段协议;② 消费点 verifier(读 briefing + journal + pool manifest,产 O2/P2 verdict artifact,并规定 clean / `rejected-like` / `disputed-like` / insufficient / fail 的消费语义)。**必须同 task** | GPT P2 §2 实查「当前没有合格消费点」。T041 `file_domain` = `bench/**` + `tests/e2e/**` 不覆盖 CLI/journal(codex round-1/2/3/5 四次点名);P1-Opus §1-B1:T041 是 phase-4 测量工具、交付物非运行时契约 ⇒ 扩 `file_domain` 也是错配,且 `depends_on:[T040]` 造成双重阻塞。合一理由:分开则「接口只是标签、消费点无输入」 | **谁**:task-decomposer 排期 + operator 授权。**何时**:**下一批 task-decomposer 排期、写下 task 编号那一刻**(决议 40 (4) 已定「随下一批排入独立 task」;可观察 = `specs/001-radar-pA/tasks/T0xx.md` 落盘)。**证不出**(该 task 迟迟无 owner)⇒ `evaluate` 的 exit 0 + 正常落盘产物**一律不得作为 PASS 证据**,O2/P2 保持 `INSUFFICIENT_EVIDENCE`。**已放行结论**:零(实测);若非零按 #4 二态处置 | 新 task(`<W>/specs/001-radar-pA/tasks/T0xx.md`)· `src/radar/cli/evaluate.py` · `journal/cli.py` · **不改 T041**;同批收 `T021.md` 的 v0.6 残留 + dangling `OQ-A1-1`;收口 HANDBACK-LOG 决议 40 (4) | **`independent`** |

**`evidence_grade` 分布**:`independent` ×4(#1 / #5 / #7 / #8)· `SOTA-corrected` ×3(#3 / #4 / #6)·
`post-hoc-accepted` ×1(#2)。⇒ **8 行里只有 4 行够得上 independent**,详见 §underweights。

### 耦合关系(哪些必须同批落)
- **语义互锁不可拆**:#1 + #3 + #4(只改池键不关 PASS 出口 = 用新键继续放行;只关出口不定二态 = 重开时无追溯语义)。
- **#5 是全批前置**(不先清点,「零迁移」就是靠沉默推断 —— 本轮明令禁止的那件事)。
- **#6 是 v0.8 的合法性前置**(否则 v0.8 重演 v0.7 的自批)。
- **#7 可与 spec amendment 并行**(仅 (c) 条依赖 #1/#2 最终措辞)。**#8 依赖排期,不阻塞 #7**。

---

## v0.2 notes(残余分歧 · 每条带具名触发时点 + 之前的风险敞口)

**note-1 · 「≥3」阈值本身未裁**
- **为什么未裁**:Cochrane「研究数很少的分组探索,无论 timing 价值都存疑」直接打在**数字本身**上,
  但本轮 **Y 未含产品价值视角**(operator 明确不选),双方均无资格判「1 条判断对 operator 有无决策价值」。
- **触发时点(具名 · 有主体有时刻可观察)**:**池 owner 关闭首个 epoch,且 #8 的消费点 owner 首次
  观察到同一 `comparability_class` 达 ≥3 并准备抽样**的那一刻 —— **operator 必须就地书面回答**
  「这 3 条合起来是否支撑一个我敢用的判断」。**可观察事件** = 消费点 verifier 产出的 verdict artifact 里
  `pool_size >= 3` 首次为真。答「否」⇒ 阈值升级为独立议题(需补产品价值视角,见 v7 判据)。
- **在此之前的风险敞口**:即使池键修好,仍可能产出**结构合规但对决策无用的 PASS**;
  该敞口与分区键**正交**,不因 #1/#2 修复而消失。

**note-2 · stable claim identity 谁定义、何时冻结**
- **触发时点(具名)**:**T021 owner 提交 claim 规范化算法 + 反例测试,并请求 operator-chair 验收**
  的那一刻(spec v0.7 已把它列为 PASS 向转正条件②)。**可观察事件** = T021 的 review 请求出现在 `review-log/`。
- **在此之前的风险敞口**:**PASS 向持续 warn**;spec 已自陈的三个攻击面(**同义改写 / 仅换锚 /
  跨 epoch 重复**)**全程开着**。
- ⚠ **依赖关系(必须保留)**:**note-2 未闭合前,note-1 的触发时点不可能到达** —— 池达不到可信的 3。

---

## What this menu underweights(强制自批判)

**underweight-1 · P1 独立性事故 —— 本轮不是双向对称独立**
首次下发 Phase 1 时,IDS 侧(Opus)**先写完自己的 P1,再把自己的结论当作「建议关注面 / 结构事实 /
结构观察」写进给 Codex 的任务书 §6**。forge 协议里 **P1 是唯一一轮双向独立**,污染 P1 = 抽掉本协议的
主要认识论价值,且产生最危险的失真:高度一致会被下游读成「两个模型独立同意」。
**operator 裁定重跑 P1**(洁净 inbox · 全新 oneshot thread · 显式禁止 Codex 打开 Opus P1 与
`_contaminated-p1/`),被污染的一轮**原样归档不删**。
⚠ **但 Opus 的 P1 未重写** ⇒ 本轮的「独立」是 **GPT 相对 Opus 独立,不是双向对称独立**。
⇒ **矩阵第 1 行虽标 `independent`,其准确读法是:源出 X 原文(codex round-3/4/5 + v5 决策表第 2 行),
两侧各自到达但 P1 非双向对称独立 —— 禁止读作双盲独立发现。**
诚实边界如实记:污染主要作用在**「审什么」**(scope),较少作用在**「结论是什么」**;
但 v5 的教训恰恰是 scope 定义决定评审能不能看见问题,故不因此减轻。

**underweight-2 · 第 7 行的 `independent` 也需限缩**
双方 P1 **各自**提出「T040 应起跑」,但**幅度经 P3R1/R2 才收敛** —— Opus P1 主张立即走 item 8 自带
fallback;GPT P1 主张仅限不依赖新池 PASS 的面,且「不能隔离则等 v6 后起跑」。**「立即」这个强度不是
P1 独立共识,是 R2 产物。**

**underweight-3 · WebSearch 全程故障 ⇒ Opus 侧无任何负结果有效**
Opus 侧 `WebSearch` 三次同错(400 · `output_config.effort 'xhigh' is not supported when thinking is
disabled`),Z 退化为**对已知权威源的定向 `WebFetch`,不是检索**。⇒ Opus 侧**一条「未检索到 ⇒ 无先例」
型结论都不得产出**(其 P2 顶部已自行封杀),**CVE `REJECTED`/`DISPUTED` 面两次 fetch 只回到导航页,
记为「未取到」而非「不存在」,靠 GPT 侧 5 次检索补上**。⇒ **本轮 SOTA 覆盖面事实上是单侧的**,
第 4 行(CVE 二态)只有一个检索来源方,**没有跨模型交叉验证**。

**underweight-4 · 回声室在 P1 被隔离后,于 P2 以「事后同意」形式回归**
8 行里只有 4 行是 `independent`。Opus P2 逐条 `grep` 实测:它 P1 的四条主张(§0.1 责任人自批 /
T041 范畴错误 / direction 抬高计数 / 三重不追溯单调性)在 GPT 洁净 P1 中**零命中**;GPT P2 的表态是
「没想到 / 未想到 / 未命名但认同」—— **四条全是被告知后同意,无一独立复现**。GPT P3R1 补了对称约束:
Opus 接受的 v5 探索出口 / CVE 二态 / chair 映射**同样不是 P1 独立复现**,Opus P3R2 承认「我原来的提法
是单向的、对我自己有利」并全额采纳三级标注。**`evidence_grade` 这一列就是为记录它而设 —— 它不消除
回声室,只让它可见。**

**underweight-5 · Y 视角覆盖盲区(两处,均 operator 明确不选)**
- **未选安全**:v5 §underweights 曾建议 v6 补。本轮 #3 的「gate 等级机器可读表达」与 #4 的「消费点
  fail-closed」都含隐性安全面(状态可被伪造 / 消费点可被绕过),**由工程纪律代管,本轮无独立安全视角**。
- **未选产品价值**:直接后果 = note-1 挂账。Cochrane 的证据打在数字本身,本轮**无资格审它**。

**underweight-6 · K 中未充分回应的项**
K 的 tradeoff 第 1 条要求「再选一次『维持』需要比上次更强的理由」—— 本轮**没有选维持**,故该条未被
真正测试。另:K「追溯成本要正面算」得到的答案是**成本为零**(实测零迁移),这是**当下事实**而非
**方法论**:本轮**并未给出「若迁移表非零该怎么算成本」的一般方法**,只给了处置形态(#4 二态)。

**underweight-7 · X 标的覆盖局限**
`round1-codex-raw.log` 的 3 条 finding(dry-run fake 产物可解锁 [critical] / 自证只绑可变路径 [high] /
JSONL 短写回滚可截断并发记录 [medium])**base 是 `main` 不是 `9444e09`,scope 与后四轮不同**。
forge-config X-6 明令「是否已被处置、由谁处置,本轮须核」—— **双方 P1/P2/P3 均未对这 3 条给出处置结论**。
⇒ **这是本轮的一处实打实的漏审**,建议在 [A] 执行时并入 #6 的 chair 逐条裁决一起清。

**underweight-8 · convergence_mode 副作用**
strong-converge 下,双方都同意但**最可能被真跑打掉**的是:① **`comparability_class` 的可判定性** ——
「类标识」和 v5 的「方向」一样,是个**人给的标签**,谁来保证两个 run 的 class 相同不是随手填的?
本轮无人验过它的机器可判性,#1 的 Feasible 栏靠的是「零迁移成本」而**不是**「类标识本身可达」。
② **消费点 fail-closed 的实装代价**(#8 是纯新增 task,从未有人估过它的规模)。两者的 fallback 已预置。

**underweight-9 · forge versioning 提示(v5 判据顺延 + v7 新判据)**
- **v5 声明的 v6 判据本轮未触发**:「warn 候选过 `review_by` 后无证据仍被续期」—— 至今未发生,
  **原样顺延为 v7 判据之一**,不因本轮已跑而作废。
- **v7 触发判据(本轮新增,任一命中即起 v7)**:
  1. **#5 核查发现非零旧 PASS** ⇒ 迁移不再零成本,二态处置的代价面本轮从未算过。
  2. **chair 条款上线后,再出现一次 reviewer verdict ≠ approve 而无 chair 逐条记录即 ship**
     —— 承 K 理由 3 的同款判据(「两层各一次 = 判据缺失不是执行疏漏」),**第二次即证条款被绕过**。
  3. **note-1 触发时 operator 答「否」** ⇒ 阈值议题升级,**v7 的 Y 必须补产品价值视角**。
  4. ⚠ **本文档从 verdict 直接推出的可证伪点(双方 round 未显式列,如实标注来源)**:
     `comparability_class` 上线后首个 epoch 关闭时,若**类数 ≈ 判断数**(每条判断自成一类),
     则分区键把「跨方向假 PASS」换成了「PASS 永久不可达」—— 严格但等于没裁,**触发 v7**。
- **不该跑 v7 的情形**:本轮 8 项**尚未行动过**时只想「再听一遍」⇒ 应该用 `/forge-inject` 注入
  moderator note,不是起新 v。

> 自批判扫描结论:本轮**有**重大盲区(underweight-3 单侧检索 / underweight-7 漏审 round-1 三条 /
> underweight-1 非双向独立)。**forge 是双模型综合,不是真实数据** —— 本仓已有七次「推演≠真跑」先例,
> 真跑仍可能推翻本 verdict,fallback 列就是为此预置的。

---

## Decision menu(for human)

### [A] 接受 verdict,交 spec-writer 落 v0.7 → v0.8 amendment

```
执行顺序(★ = 不可颠倒):

★1. 落「零受影响 PASS 核查记录」(#5)
    —— 必须在任何追溯规则写进 spec 之前完成。否则「零迁移」就是靠沉默推断,
       而那正是本轮明令禁止的那件事。产物 = 具名核查文件 + operator 签收。

★2. chair 追认(#6):operator 对 codex round-5 的 2 条 high 逐条标
    accepted / rejected / deferred + 写明 concern 如何被 addressed;
    追认 v0.7 为 provisional(不撤 commit),其 O2/P2 权威性悬置至记录补齐;
    ⚠ 同批清 round-1 的 3 条 finding 处置(见 underweight-7,本轮漏审)。
    写进 HANDBACK-LOG 新决议。
    —— 必须先于 3,否则 v0.8 会重演 v0.7 的「spec-writer 自批」。

 3. spec-writer 落 v0.7 → v0.8 一次性 amendment:#1 / #2 / #3 / #4 条文 + #6 条款文本
    → 走一次 codex review。
    ⚠ 强制随行项:R5-F2/F4 的第 6 轮 codex 复核(决议 40 (5) 防遗忘条款 —— v0.8
      不得在未完成该复核的情况下宣称 O2/P2 可判 PASS)。

 4. (可与 3 并行)T040 起跑(#7):5 文件 block 测 + (c) 条 warn-only/baseline。
    ⚠ (c) 条依赖 3 的最终措辞 ⇒ 「接受一次返工」或「(c) 排在 3 之后」二选一。

 5. task-decomposer 排新 task(#8):三态接口 + 消费点 verifier 合一;
    同批收 T021 的 v0.6 残留(:31/:44/:60)与 dangling OQ-A1-1。

 6. PRD:本轮不改。v1.7 的 O2 定位澄清已覆盖「集合验收采样口径」。
    ⚠ 唯一可能的 PRD 面 = note-1 触发且 operator 答「否」时,O2 阈值本身要回 PRD ——
      那时才动,不预改(承 K 理由 5:不照施工单预写 PRD)。
```
⚠ **#1 / #3 / #4 语义互锁,任一被降级为「实施注记」,联合 verdict 即失效**(分别会重开
「用新键继续放行」/「探索出口当 PASS 用」/「重开时无追溯语义」)。
⚠ 本轮 **W 未含 next-PRD** ⇒ 本文档**不构成 `/plan-start` 的输入**,**不需要 fork 新 PRD branch**。

### [B] 跑 forge v7(说明需要补什么)
```
/expert-forge 001
# Phase 0 intake 时调整 X / Y / Z / W / K;v6 整目录保留作历史参考
```
适用:§underweights-9 的 4 条 v7 判据任一命中 · 或 operator 认为 `comparability_class`
的**机器可判性**必须先裁(本轮 Feasible 栏没验过它)· 或要补**产品价值 / 安全**视角进 Y。

### [C] 局部接受
- ✅ **建议优先采纳**:**#5**(零成本 + 是其余各行的前置)· **#6**(纯流程,无代码面,且是 v0.8 的
  合法性前提)· **#7 的 5 文件面**(不依赖 v0.8 措辞,今天就能跑)
- ⏸ **可挂起**:**#2**(依赖 T021 的 claim 规范化算法,见 note-2)· **#8**(依赖 task-decomposer 排期)
- ❌ **不建议拆散**:**#1 + #3 + #4**(语义互锁,拆开落会重新打开假 PASS 通道)
- ⚠ **不建议只采 #1 不采 #3**:那等于「换了个更严的键,继续用它放行」——**本轮最坏的局部接受组合**。

### [P] Park
```
/park 001
```
保留全部 forge 产物。⚠ 注意:① **O7 longstop 时钟继续走**(start 2026-08-02 → 截止 2026-11-02,
到期无 journal 行判 FAIL(0/5),这是 v5 item 4 的设计意图不是缺陷);② park 期间假 PASS 通道
**理论上开着**,但**实测机器侧跑的仍是 v0.6**(池化路径未实装)⇒ 通道**事实上不可达**
(承决议 40 (3) 的同款判断)。

### [Z] Abandon
```
/abandon 001
```
**本 verdict 不指向 abandon。** 它裁的是「集合级判据的分区与追溯」,不是「要不要继续做 radar」;
且 O7 首跑已 `decision_delta=true`,产品信号为正。仅当 operator 独立判定 radar 整体不做时才选此项。

---

## Forge log
(由 /expert-forge 命令更新;记录每次 forge run 的 v 序列 + 关键 verdict 一句话)

- **v6: 2026-08-03** — verdict: "**池化保留但 block-PASS 出口现在关闭,降为探索/warn 出口**(v5 的错不在池化,在把 post-hoc 探索机制的出口写成可放行 PASS · Cochrane/BMJ);PASS 重开前置 = 池键改 `decision_epoch + rubric + comparability_class` 且 **epoch 开启时冻结不可变** ∧ `direction` **进比较类、退出去重计数** ∧ 去重身份改 **stable claim identity**;**追溯采二态**(CVE 先例:已证无效 → `rejected-like` 消费点机器可拒 / 存疑 → `disputed-like` 保留但不得当 clean PASS 消费),**fail-closed 落在消费点判定上不落在通知标注上**(retraction 实证:标了仍被引);⭐ **仓内实查确认零真实 O2/P2 PASS 被旧池消费 ⇒ 迁移表实测零项,现在立规则最便宜,但零受影响必须落成具名核查记录不得靠沉默推断**;**`needs-attention` 不是 veto**(RFC 7282:addressed ≠ accommodated)**但 override 只能由 operator-chair 逐条写明 concern 如何被 addressed,`/handback-review` 是闸点与留痕非 chair 本身,spec-writer 不得自任,无 chair 记录不得声称 clean PASS**,已 commit 的 v0.7 追认为 provisional;**T040 立即局部起跑**(5 非 O2 文件 block + (c) 条 warn-only/baseline);**三态接口 owner 与消费点 fail-closed 合为一个具名新 task,不塞 T041**(分开则接口只是标签、消费点无输入)。**方法论产出:decision-list 新增第 5 列 `evidence_grade`(independent×4 / SOTA-corrected×3 / post-hoc-accepted×1)—— 回声室在 P1 被隔离后于 P2 以『事后同意』形式回归,这一列为记录它而设**;v5 四列范式**有效,缺的是 fallback 列的最小字段集**(谁 / 何时 / 已放行结论怎么办),本轮硬性补齐;⚠ 本轮 P1 非双向对称独立(Opus P1 未重写)+ Opus 侧 WebSearch 全程故障(无负结果有效)+ round-1 三条 finding 漏审。v7 判据:核查发现非零旧 PASS / chair 条款被绕过第二次 / note-1 时 operator 答否 / 类数≈判断数致 PASS 永久不可达;v5 既定判据(warn 候选无证据续期)顺延。"
- v5: 2026-08-02 — verdict: "采 ISO/IEC/IEEE 29148 九特征作『判据冻结前置』分类框架 + 逐项本地化为可执行牙,12 项作 spec v0.6→v0.7 一次性 amendment 施工单;(c) 从个体级门改挂集合验收侧;T040 以 warn + versioned baseline 起跑…(详见 v5 stage 文档)"
- v4: 2026-07-18 — verdict: "采 γ,以正式 amendment(非 waiver)落地:生效自证标的改写为『首个评估 run 产物』…(详见 v4 stage 文档)"
- v3: 2026-07-17 — verdict: "g1(人肉盲测二值签字)永久退役出解锁链;新 gate 形态 = 按 run 类型分流 + 两层 + 信号…(详见 v3 stage 文档)"
- v2: 2026-07-16 — verdict: "①② 从 T010/T011 解锁前置退役(采纳 KG-B9 · 循环依赖成立)…(详见 v2 stage 文档)"
- v1: 2026-07-16 — verdict: "P0.2 人肉盲测二值签字 gate 退役(采纳 KG-B8),T010/T011 改由机器可判三项解锁…(详见 v1 stage 文档)"
