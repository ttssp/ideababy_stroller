# Forge Stage · 009-pM3prime · v2 · "无合格领域主体时,金标 Layer-2 还成不成立"

**Generated**: 2026-07-27T09:20:00Z
**Source**: forge run v2 with X = 10 标的(5 本仓库文件 + 5 XenoDev-009 外部 repo 文件), Y = 验证方法学/认识论(核心) · 统计效力与可证伪性 · 成本与 v0.1 可行性, Z = 对标 SOTA, W = verdict-only + decision-list + next-PRD
**Convergence mode**: strong-converge
**Rounds completed**: P1 (both), P2 (both), P3R1 (both), P3R2 (both)
**Reviewers**: Claude Opus 4.8(Reviewer A)· GPT-5.6-Sol xhigh(Reviewer B)
**Searches run**: ~26 across ~17 distinct sources(Opus 6 检索 + 1 全文抓取 · GPT 20 query / 6 批)· **与 v1 零论文重叠**
**Moderator injections honored**: none(本 run 无 moderator-notes 注入)
**Convergence outcome**: converged(单一 verdict,无 unresolved;残余分歧降 4 条 v0.2 note;A 侧让步 2 条)
**Triggering handback**: `009-pM3prime-20260727T065748Z`(FU-KG43)+ HANDBACK-LOG 第 28 条

---

## How to read this

本轮触发源有两层,**第二层才是重心**:

1. XenoDev 起 Layer-2 真跑前做零成本可达性验证,发现**冻结门槛组合数学不可达**(D-1/D-2/D-3)——
   该层已由 HANDBACK-LOG 第 28 条直接裁定并交 XenoDev 落地,**不在本轮议题内**。
2. operator 在同一条决议中**自陈「领域判断力不足(全维)」** ——
   **forge v1「operator 可自任独立第二源」的落地前提被本人推翻**,
   第 27 条据此所作的「KG-42 死结解」判定随之失效。本轮审的是这一层。

读完后你应该:
- 知道 v1 的解到底错在哪一步(§Verdict rationale · **不是错在结论,是错在一次范畴替换**)
- 知道现在还剩什么可做、什么必须停(§Verdict · §Decision matrix)
- 拿到可直接落地的 PRD 改写落点(§Next-version PRD draft)
- 知道本 verdict 自己的软肋(§What this menu underweights —— **本轮有一条很硬的自曝**)

---

## Verdict

**全量五维 Layer-2 作为「映射正确性(correctness)gold gate」在 v0.1 判定不成立,
且不因换主体、不因调门槛而成立。** sector / direction / horizon 三维不存在可及的 validity 锚;
而唯一在场的主体(operator)产出的「gold 考据版 vs human 盲标版」是**同一人两次标注**,
按 Krippendorff 信度分类**只测 stability(稳定性),不测 validity(对标准的准确性)**。

**forge v1「operator 可自任独立第二源」的推论据此撤销。**
错误独立性解决的是「两方不共享盲点」,**它不产生真值**。
**KG-42「无验收主体」的死结不是被 v1 解开的,是被 D-7 挪了位置。**

**但不判纯 STOP。** 把 Layer-2 的验收对象从 **correctness** 降级为 **groundedness**
(被引原文是否真支撑该五元组)——它只需阅读理解、不需领域判断,
009 的引文回锚基础设施(`raw_ref` / `span_start` / `span_end` · forge v6 引文回锚制)已就位,
且能真抓到东西(RAG 归因文献实测高达 57% 引文为事后合理化)。

**该采纳是条件性的,条件必须同时落地 —— 条件不落地则回退纯 STOP:**
- **E2 拆分**:原 E2 历史窗回测 **不解锁**;新增 groundedness-only 诊断 lane。
- **硬边界必须明写**:**groundedness 过 ≠ 映射正确 ≠ 有 alpha ≠ 授权回测**。
- **门槛形态同步修正**:固定 coverage 阈 → risk-coverage 曲线 / AURC,
  经**新 `caliber_version` 预注册并废止旧 pass 语义**。
  判据:**看数后下调既有阈值数字 = 移动球门(禁);换形态并重注册 = 方法学修正(可);
  形态改也不得 retroactively 解锁旧 gate。**
- **红线不动**:`gold_layer2.py:203` 第二 LLM / 跨 vendor 未校准模型当 Layer-2 终审仍 raise。

(显式回应 K:①「还成不成立」→ correctness 形态不成立,groundedness 形态成立;
②「主体是谁」→ correctness 无合格主体且 v0.1 无法获得,groundedness 主体即 operator;
③「宁可 STOP 不要自欺」→ 采纳条件化,边界写不硬即回退 STOP,B 侧对此有否决权并已行使复核。)

---

## Evidence map

| 结论 | 来源 | 引用(≤15 words) | 是否有反对证据 |
|---|---|---|---|
| 同一人两版标注只测 stability 不测 validity | P2-Opus §1 row1(Krippendorff 信度三分类)· P2-GPT §2 独立复核 | "可靠性文献最多支持稳定/复现,不自动给 validity" | — (双方零重叠路径同向) |
| v1 中心推论有范畴替换(度量函数领域中立 ≠ 标注劳动领域中立) | P1-Opus §1.2 | "`mapping_agreement_rate()` 是比较器,它只做 `==`" | — |
| v1 未定义 gold provenance,而判据相对 gold 定义 | P1-Opus §1.3 · P1-GPT §1 | "v1 D-7 草案写得很细的是 human 资格,不是 gold provenance" | — (双方 P1 独立同得) |
| operator 07-27 自陈对 v1 是**旧信息**(risks.md 07-23 已载且在 v1 的 X 里) | P1-Opus §1.1 · P1-GPT §1(独立核证) | "旧信息的精确化/加重,不是性质全新的事实" | — (B 侧被要求独立核证,结论一致) |
| 非专家标注可用的前提是**多人聚合**,solo 结构上不可用 | P2-Opus §1 row2 · P2-GPT §1 row2(Snow et al.) | "非专家 0.68 vs 专家 0.83;majority vote 过滤噪声" | ⚠ 被 Dorner & Hardt 局部削弱(见下) |
| 单噪声标签在「比较分类器 + 更多样本」目标下有理论路径 | P2-GPT §1 row3(Dorner & Hardt ICML 2024) | "预算应投向更多样本的单标签" | ⚠ **推翻 A 侧 P2「solo 无路」的绝对表述** |
| 弱监督 / partial identification 只产区间界,不产 pass/fail gold | P2-Opus §1 row4 · P2-GPT §1 row1(Data Programming) | "bounds 只给区间,不产 pass/fail gold" | — |
| 事后市场回标验 alpha 与市场反应,不验原文→五元组映射 | P2-GPT §1 row6(StockNet 等) | "outcome 不能证明映射 gold 正确" | — |
| correctness 与 groundedness 是两个可分离的验收对象 | P2-Opus §1 row6(Correctness is not Faithfulness)· P2-GPT §1 row5(FEVER/CFEVER) | "高达 57% 的引文是事后合理化的" | — (**两条零重叠路径独立导出,本轮最强证据**) |
| 固定 coverage 阈是方法学上过时形态,标准做法是 risk-coverage 曲线 | P2-Opus §1 row3 · P2-GPT §1 row4(selective classification) | "标准做法是 risk-coverage 曲线或给定 risk 后最大化 coverage" | ⚠ B 侧修正 A 的「结构冲突」表述为「门槛未校准」(见 §Verdict rationale) |
| Layer-1 主体问题全程未处置 | P1-Opus §1.6 · 双方 P3R2 §3 | "Layer-1 门槛仍空 = blocked-on Layer-1 真盲标跑" | — (双方均确认未解) |

---

## Intake recap

### X · 审阅标的(10 个 · 全部可达 · 无 skipped)

本仓库内:FU-KG43 hand-back 全文 · HANDBACK-LOG 第 26/27/28 条 · **v1 stage doc 全文** ·
PRD(§2 Users + §4-E1 D-7 改写块)· forge v5 stage doc(证伪链 E0-E3 原设计)
外部 repo(XenoDev-009):`SLA.md`(第 28 行 refactor 声明 + Layer-2 逐维门槛表)· `spec.md`(O7/O8 + C9 + D-7)·
`risks.md`(E1-R2 及其 07-23 下游注)· `gold_layer2.py`(背景证据)· `layer2-feasibility-probe.py`(背景证据)

### Y · 审阅视角
- 验证方法学 / 认识论(自定义 · 核心)
- 统计效力与可证伪性
- 成本与 v0.1 可行性
- (operator 未选「架构设计」「产品价值」—— 聚焦「验收还成不成立」,不发散到架构与产品叙事)

### Z · 参照系
- mode: 对标 SOTA。**零重叠要求**:避开 v1 已用的 Nine Judges / Correlated Errors / AmbER /
  FActScore / SAFE / PoLL。实际引入 6 个新文献面(信度理论 / 非专家标注 / 单噪声标签 /
  选择性预测 / 弱监督无金标评估 / groundedness-vs-correctness)。

### W · 产出形态
verdict-only · decision-list · next-PRD

### K · 用户判准(摘要)
在「operator 领域判断力不足(全维)」硬前提下,金标 Layer-2 还成不成立、验收主体是谁。
要正面处理的张力:**错误独立性解决「不共享盲点」,不解决「gold 是不是真值」**。
硬约束:不要需 operator 具备领域判断力的方案 / 不要第二 LLM 当终审 / 不重开 D-1~D-3 / 不动 E1 结论。
姿态:**宁可接受长期 blocked,也不要跑得动但验收不了任何东西的降级 harness;自欺的成本远高于停下来的成本。**
binding:回声室警告(v1/v4/v5 连续三轮零分歧强收敛)+ KG-43 一并议。

### 收敛模式
strong-converge

---

## Verdict rationale(W: verdict-only)

### v1 错在哪一步

v1 的结论链有三环:① 保留 gate 骨架与 fail-closed;② 第二源从「领域独立真人」refactor 为
「错误独立性代理」;③ 推出 operator 可自任。**前两环成立,第三环断裂。**

断裂点是一次**范畴替换**。v1 写(stage doc L113-117):

> Layer-2 第二源实际要做的工作,不是「懂投资」。`mapping_agreement_rate()` 不含任何金融理解逻辑…
> 这解释了为什么「operator 不懂投资」不是全维阻断。

`mapping_agreement_rate()` 是**比较器**,它当然不含金融逻辑 —— 它只做 `==`。
但**被比较的那两组五元组是怎么产生的**,才是劳动所在。
从一句「看好存储主线」判定 direction / horizon / sector,**正是领域判断**。
**「比较器领域中立」推不出「标注领域中立」。**

而 v1 用来撑住这一步的「事实维可外证据核验」,**只覆盖 ticker(watchlist 外锚)与 timepoint
(`published_at`)两维**;direction / sector / horizon 三维没有任何外锚,v1 也没给。
即 v1 的论证严格讲只支持「两维不需领域深度」,却被用作「五维都不阻断」的结论。

### 更深一层:v1 的契约缺一个角

v1 的 D-7 改写草案把**第二源(human)**的资格写得极细(独立盲标 / 外证据锚定 / 任务内校准 /
abstain / 仲裁留痕),**却通篇没有定义 gold 从哪来** —— 而它同时把判据改成了「逐维**双错率**」,
双错 = machine≠gold ∧ human≠gold。**双错率是相对 gold 定义的;gold 未定义,判据悬空。**

正因为没定义,operator 才不得不在 2026-07-25 临时拍板补协议(gold=考据版 / human=盲标版),
而这个补丁**直接生产了本轮的困境**:gold 与 human 同为一人。
**一个把错误率定义在未定义真值锚上的契约,在结构上就是不完整的**,不是执行时才出问题。

三分离契约(错误独立性 / 领域能力 / 仲裁权)作为分析框架有价值,
但它把「领域能力」分离出去之后**没有为它安排承担者** —— 缺的第四项正是 **gold provenance**。

### 为什么不是纯 STOP

因为 correctness 与 groundedness 是两个可分离的验收对象,而后者**恰好落在 operator 能力之内**:

- **correctness** =「NVDA 这个 ticker 判得对不对、看多这个方向对不对」→ 领域判断,operator 做不了;
- **groundedness** =「**被引的那句原文,是否真的支撑这个五元组**」→ 阅读理解,operator 做得了。

这条切法是**横切五维**(五维都验,但只验「有没有原文依据」),
不是纵向砍掉三个解释维 —— 后者是本 forge 早期的想法,已被更好的切法取代。

**它对 009 特别合适**:groundedness 验收要的输入**已经在库里**(forge v6 引文回锚制的直接产物)。
**且它不是稻草人**:归因文献实测高达 57% 的引文是事后合理化的,这种检查真能抓到东西。

### 但它必须被关在笼子里

B 侧在 P3R1 划了一条线并在 P3R2 行使复核权:
**「若被写成授权原 E2/history-window/backtest,就会变成自欺,我会转向纯 STOP」**。
A 侧接受该条件为 binding。最终 B 侧判定边界措辞「**满足**」,故不回退。

这意味着 verdict 的采纳**是有生效条件的**:E2 拆分 + 硬边界明写。
**若落地时边界被稀释(例如把 groundedness 过读成条件 ② 满足),本 verdict 自动失效,回退纯 STOP。**

### 一处 A 侧被修正的表述

A 侧 P1 称「诚实弃权 × 覆盖率门槛」是**结构冲突**;B 侧修正为「**不是数学上所有主体都不可达,
而是覆盖率门槛没有经过主体能力校准**」。A 侧接受该修正在技术上成立,但指出**直接采纳会走进 C6 陷阱**
——「看到 operator 过不了,于是按 operator 能力重新校准门槛」= 移动球门,
正是 operator 在第 28 条**明确否决 D-1(c)** 的同一动作。

双方最终收敛到 B 侧措辞的判据(见 §Verdict 门槛形态段),
其价值超出 009:**它对所有预注册门槛场景可用**,直接接 KG-43。

---

## Decision matrix(W: decision-list)

| 类别 | 项 | 来源(标的位置) | 理由(evidence) | 优先级 |
|---|---|---|---|---|
| **保留** | `gold_layer2.py:203` 第二 LLM/跨 vendor 终审红线 | `gold_layer2.py:203` | v1 两组零重叠 SOTA 论证未被本轮事实触动;K 明确不重开 | P0 |
| **保留** | gate fail-closed 骨架 + 双层链 | `gate.py` | 结构正确;本轮只改验收对象不改 gate 机制 | P0 |
| **保留** | E1 US 密度结论(第 25 条终裁) | HANDBACK-LOG#25 | K 明确不动;E1 的正面实证独立成立 | P0 |
| **保留** | 引文回锚基础设施(forge v6) | `anchoring.py` · `raw_ref`/`span_*` | **groundedness 验收的输入已在库里,零新建** | P0 |
| **保留** | `trial_ledger` extractor_variant 基础设施 | `trial_ledger` | v0.2 变体比较路径的资产,现在不用但别拆 | P1 |
| **调整** | Layer-2 验收对象 **correctness → groundedness** | spec §O8 · PRD §4-E1 | 三个解释维无 validity 锚;groundedness 只需阅读理解 | **P0** |
| **调整** | E2 由单 gate **拆为两 lane**(诊断 lane / 回测 lane) | PRD E2 解锁条件 ② | 「产开发证据」与「跑历史窗回测」性质不同,不应共用一个 gate | **P0** |
| **调整** | 门槛形态:固定 coverage 阈 → risk-coverage 曲线 / AURC | SLA §Layer-2 门槛表 | 选择性预测文献的标准形态;须经**新 `caliber_version`** 重注册并废止旧 pass 语义 | P0 |
| **调整** | SLA Layer-2 门槛表整体重注册 | `SLA.md` 门槛表 | 形态改 ≠ 数字改;重注册是方法学修正不是移动球门 | P0 |
| **删除** | v1「operator 可自任 Layer-2 第二源」推论 | v1 stage §Verdict | 范畴替换;三个解释维无外锚(见 §Verdict rationale) | **P0** |
| **删除** | 第 27 条「KG-42 死结解」判定 | HANDBACK-LOG#27 | 死结未解,只是被挪位 | **P0** |
| **删除** | 07-25 gold 协议**作为 validity 验收依据**的地位 | 07-25 operator 拍板 | 同一人两版 = stability 测量;作为 stability 记录可留,不得当 validity 用 | **P0** |
| **删除** | 全量五维 correctness gate 作为 v0.1 交付项 | PRD §4-E1 | v0.1 不成立且不因换主体/调门槛而成立 | **P0** |
| **新增** | groundedness 验收面 **+ 硬边界声明** | (新) | 边界 = 过 ≠ 映射正确 ≠ 有 alpha ≠ 授权回测。**边界写不硬则整条 verdict 回退纯 STOP** | **P0** |
| **新增** | 「数字 vs 形态」冻结修正判据 | (新 · 双方收敛) | 下调既有阈值数字=移动球门;换形态 + 新 `caliber_version` 重注册 + 废止旧 pass 语义=方法学修正;形态改不得 retroactively 解锁旧 gate | P0 |
| **新增** | KG-43 三道冻结前置门 | (新 · 双方合并) | ① 存在性证明 ② 真值证明 ③ 形态检验(详见下) | P0 |
| **新增** | v0.2 note 四条 | (新) | 见 §v0.2 notes | P1 |

### KG-43 · 冻结前置三道门(框架级 · 归 IDS forge 006 攒批)

任何**预注册验收门槛**在冻结前须过三道门:

1. **存在性证明** —— 构造理想上界输入,证明 `passed=1` **可达**。零成本(合成数据 · 无 LLM)。
   *(009 缺这道门的直接后果:冻结了一个数学上不可能通过的组合。)*
2. **真值证明** —— 验收锚**从哪来 / 谁能独立证伪它 / 成本是否在本 tier 可承受**。
   *(009 缺这道门的直接后果:契约把错误率定义在一个未定义的真值锚上。)*
3. **形态检验** —— 门槛**形态**是否符合该问题的标准处理方式。
   *(理由:形态错比数字错更难救 —— 数字受 C6 约束尚可经版本化修正,形态错则整套预注册语义作废。
   009 缺这道门的直接后果:冻结了固定 coverage 阈,而该问题的标准形态是 risk-coverage 曲线。)*

**落点建议**:spec-writer / task-decomposer SKILL 的冻结前 checklist;PRD 模板加「验收锚来源」字段。
**受益面**:所有用本 framework 且有预注册门槛的项目(证伪链 / 金标验收 / SLA gate 全部命中)。

---

## Next-version PRD draft(W: next-PRD)

**Status**: Draft from forge v2, awaiting human approval
**Sources**: 本 stage §Verdict + §Evidence map;P3R2-Opus §4 + P3R2-GPT §4(已综合)
**粒度约定**: 写到「改哪一段 + 改成什么方向 + 硬边界措辞」,**不下沉到代码/阈值实装**(实装是 XenoDev L4 的工作)

### 改点 1 · PRD §4-E1 的 ⚠ D-7 改写块 —— **撤销 + 重写**

> **D-7(v2 改写)**:Layer-2 的验收对象是 **groundedness(引文支撑性)**,不是 correctness(映射正确性)。
> 合格验收 = 判定「**被引原文是否真的支撑该五元组**」,这是阅读理解任务,**不需要金融领域判断力**,
> operator 可独立承担。
>
> **明确不证明项(硬边界 · 不得省略)**:groundedness 过 **≠** 映射正确 **≠** 该信号有 alpha
> **≠** 授权历史窗回测。它证明的是「提取器没有无中生有 / 没有事后合理化引文」,
> 不证明「提取器判得准」。
>
> **v1 的「operator 可自任独立第二源(correctness)」推论撤销** ——
> 错误独立性解决「不共享盲点」,不产生真值;同一人的考据版与盲标版按信度理论只测 stability。
> **红线不变**:第二 LLM / 跨 vendor 未校准模型当 Layer-2 终审 = BLOCK(`gold_layer2.py:203`)。

### 改点 2 · PRD E2 解锁条件 ② —— **拆为两条**

- **② -a(诊断 lane)**:groundedness 验收过 → 可跑 **E2 诊断 lane**(口径校准 / failure 分类 /
  提取器变体比较的**开发证据**)。
- **② -b(回测 lane)**:历史窗回测需「映射 correctness 验收过」——
  **在 v0.1 明确标记为不可满足(blocked · 非「待跑」)**,并写明原因是缺 validity 锚而非缺劳动。

> ⚠ **反自欺条款(建议写进 PRD)**:②-a 过**不得**被记作 ② 满足。
> 若未来任何文档把 groundedness 结果表述为「两层金标过」,视为口径漂移,须回 hand-back。

### 改点 3 · PRD §2 × D-7 关系 —— **部分撤销 v1 的判断**

v1 判「§2(单人不懂投资)× D-7 **非产品级真互斥**,仅当前资源下暂不可满足」。
**在 correctness 维度上这个判断应撤销** —— 它**就是**真互斥:
产品定义(单人自用 · 不懂投资)与验收要求(五维映射正确性验收)在 v0.1 不可同时满足,
且不是资源问题,是**能力与 validity 锚的结构问题**。
在 groundedness 维度上,v1 的「非真互斥」判断**成立并保留**。

### 改点 4 · SLA §Layer-2 门槛表 —— **形态重注册**

固定逐维 coverage 阈 → **risk-coverage 曲线 / AURC 或区间报告**,
经**新 `caliber_version`** 预注册,**并废止旧 pass 语义**。
**不得**在看过数据后下调既有阈值数字(= 移动球门 = C6 违规)。

### Open questions(forge 也没解决 —— 见 v0.2 note)

- groundedness lane 在 n≈41 下的统计效力未算
- Layer-1 的主体问题未处置
- partial identification 的界宽未验

---

## v0.2 notes(残余分歧降级 · 双方一致)

1. **Dorner & Hardt 变体比较路径(v0.2+ · 带前置验证义务)**
   把 estimand 从「这条五元组对不对」改为「变体 A 是否优于 B」,对单噪声标注者是文献支持的形态,
   且 009 的 `trial_ledger` 已有基础设施。
   **但进入前必须先证明:operator 在目标维度上的标注噪声与真值正相关(即优于随机)。**
   本案前提恰是 operator 在这三维无判断力 —— **该假设未经检验且可能为假**。
   *(B 侧原话:否则会被误读为只差排期和样本量。)*

2. **Partial identification / Fréchet 界在 n≈41 的界宽未知**
   方向存在(无需任何标注即可给出 accuracy/P/R/F1 的区间界),但**小样本下界可能宽到无区分力**。
   **可零成本先算**(与 KG-43 第一道门同性质的探针)。

3. **Layer-1 主体问题全程未处置**
   `spec.md` 显示 Layer-1 门槛仍空、同样 blocked-on 真盲标跑。
   本轮聚焦 Layer-2。若 groundedness 吸收 Layer-1,需重写 Layer-1 终点;否则主体缺口仍在。

4. **「operator 慢考据 gold 是否可产」未被文献救活**
   信度文献最多支持 stability / reproducibility,**不自动给 validity**。
   该问题在方法学上无解,只能靠外锚(watchlist / `published_at`)绕开,而外锚只覆盖两维。

---

## What this menu underweights(强制自批判)

- **[本轮最硬的自曝] groundedness lane 的实际劳动量与统计效力,两边都没算。**
  本 verdict 说「operator 做得了」,依据是**任务性质**(阅读理解 vs 领域判断),
  **不是**对工作量的估算 —— 逐条核 41 条引文仍是真实劳动,而 operator 已在本轮暴露了投入约束。
  更要紧的是:**n≈41 下 groundedness 的判别力同样没算** ——
  A 侧 P1 §1.5 对 correctness 提过这个问题(41 条 × 门槛 0.05 → 约 2 条错就翻盘),
  换成 groundedness 之后**这个问题原样存在,却没有人重新算**。
  **若真跑后发现 groundedness 在 n=41 上也没有区分力,本 verdict 的「不是纯 STOP」结论就该被推翻。**
  建议:落地前先按 KG-43 第一道门给 groundedness lane 做一次可达性 + 效力探针。

- **「57% 引文事后合理化」的外推边界。** 该数字来自 **RAG 生成场景**(模型先答后引),
  009 是**抽取场景**(模型从原文里摘 quote)。两者的失败机理相近但不相同,
  该数字**支持「groundedness 检查值得做」,不支持「009 也是 57%」**。真实比例需本任务实测。

- **两位 reviewer 都是 LLM,而本轮议题恰恰是「无合格人类主体时怎么办」。**
  这是本轮的元层结构性风险:我们在用两个 LLM 论证「LLM 不能替代人类真值」,
  结论方向恰好与论证者的自利方向相反(不是自我扩权),这降低但**不消除**该风险。

- **回声室:本轮只有 P2 是真对抗。** P1 双方同姿态收敛(已标警报),
  P3R1/P3R2 收敛极快(3 条分歧 R1 即全部判定、A 侧让步 2 条)。
  **真正的对抗只发生在 P2 的零重叠外证据环节** —— 该环节确实各自推翻了自己 P1 的一部分,
  这是 verdict 可信的主要依据;但若 P2 的检索面本身有共同盲区,双方会一起错。

- **SOTA 外推边界(同 v1)。** 引用的文献证的是一般 NLP / RAG / 内容分析中的信度与归因性质,
  **不是**在「直播转写 → A股/美股五元组」这个精确任务上的直接实测。
  双方判断外推成立,但严格说这是**强论证不是本任务实测**。

- **Y 未选「架构设计」与「工程纪律」。** 故 groundedness lane 的实装形态、
  与既有 harness 的接缝、测试策略均未审 —— 需 XenoDev build-time 兜底(G-R2 老教训)。

- **forge versioning 提示**:以下新信息进入会触发 v3 并可能改本 verdict ——
  ① groundedness lane 真跑后发现 n=41 无区分力(→ 可能逼回纯 STOP);
  ② operator 在目标维度上被证明优于随机(→ 松动 v0.2 note 1,变体比较路径可提前);
  ③ 出现可及的外部 validity 锚(→ correctness gate 可能复活)。

---

## Decision menu(for human)

### [A] 接受 verdict → 改 PRD → 回 XenoDev 实装

```
1. 改 PRD:discussion/009/009-pM3prime/PRD.md
   - §4-E1 D-7 块 → 按 §Next-version PRD draft 改点 1 重写(撤销 v1 推论 + groundedness + 硬边界)
   - E2 解锁条件 ② → 按改点 2 拆为 ②-a 诊断 lane / ②-b 回测 lane(后者标 blocked 非待跑)
   - §2 × D-7 关系 → 按改点 3 部分撤销 v1 的「非真互斥」判断
   - 标注 Source: forge stage-forge-009-pM3prime-v2.md
2. 记 HANDBACK-LOG 第 29 条(v2 verdict 入库 · 明确撤销第 27 条「KG-42 死结解」判定)
3. 回 XenoDev:cd "$XENODEV_ROOT" → claude -w 009-pM3prime
   - SLA §Layer-2 门槛表按改点 4 形态重注册(新 caliber_version · 废止旧 pass 语义)
   - 实装 groundedness lane
   - ⚠ 起跑前先做 §underweights 第一条建议的可达性 + 效力探针
```
⚠ 本 verdict 是 **PRD 层改动**,不是直接进 `/plan-start`。
⚠ **落地时若硬边界被稀释,本 verdict 自动失效回退纯 STOP** —— 这是 B 侧行使复核权时的 binding 条件。

### [B] 跑 forge v3
```
/expert-forge 009-pM3prime
```
适用:觉得 verdict 不够锐、或 §underweights 里「groundedness 效力未算」这条让你不放心 ——
可先做探针拿到数字再起 v3,让 v3 有实测而非推演。

### [C] 局部接受
- ✅ 采纳:撤销 v1 推论 + 删除「KG-42 死结解」判定 + E2 拆分(回测不解锁)+ KG-43 三道门
- ⏸ 挂起:groundedness lane(等 §underweights 第一条的效力探针出数字再定)
- ❌ 拒绝:(按你判断填)

**适用:如果你认同「v1 的解要撤」但对「groundedness 够不够格」还不放心 ——
这是与 K「宁可 STOP」姿态最一致的一档。**

### [P] Park
```
/park 009-pM3prime
```
保留全部产物。E2 三条件本就未齐,金标这条可挂,先推进其它条件。

### [Z] Abandon
```
/abandon 009-pM3prime
```
放弃证伪链金标层。⚠ 注意本轮 verdict 已经削弱了 v1 对 abandon 的反对理由 ——
v1 说「放弃 Layer-2 = 毁 E1 ROI」,而本轮认定 **E1 的正面实证(~23/29 真隐性信号被捕捉)独立成立**,
不必由 Layer-2 背书。所以 abandon 的代价比 v1 估计的小,但仍需归档 lesson 文档。

---

## Forge log

- **v1**: 2026-07-23 — verdict: "D-7 保留 human 为独立性默认代理但重述理据;第二源 refactor 为
  错误独立性/领域能力/仲裁权三分离;跨 vendor 强模型不得当 Layer-2 独立终审;frozen §2×D-7 收窄为
  验收级暂不可满足;operator 配证据协议自任独立源;红线 `gold_layer2.py:81` 保留。"
- **v2**: 2026-07-27 — verdict: "**v1 第三环(operator 可自任)撤销 —— 范畴替换 + gold provenance 未定义**;
  全量五维 correctness gate 在 v0.1 不成立且不因换主体/调门槛而成立(三解释维无 validity 锚 ·
  同一人两版只测 stability);**降级为 groundedness 验收 + E2 拆分,回测 lane 不解锁**;
  采纳条件化 —— 硬边界写不硬则回退纯 STOP;门槛形态经新 caliber_version 重注册(数字 vs 形态判据);
  KG-43 三道冻结前置门;红线 `:203` 不动。"
