---
forge_version: v2
created: 2026-07-27T08:12:58Z
convergence_mode: strong-converge
x_hash: 3e134daff92fc92300a3bec84fa84054
prefill_source: manual
fork_id: 009-pM3prime
triggering_handback: 009-pM3prime-20260727T065748Z
triggering_decision: HANDBACK-LOG 第 28 条(2026-07-27T07:46:28Z · IDS commit f4802f9)
---

# Forge Config · 009-pM3prime · v2

## X · 审阅标的

（operator 与 orchestrator 协商拟定 · 全部核实可达 · 2026-07-27）

本次 forge 由 hand-back `009-pM3prime-20260727T065748Z`(FU-KG43 · drift + prd-revision-trigger · severity high)
与 operator 在 `/handback-review 009` **第 28 条决议**中的自陈**共同触发**。

**触发链**:XenoDev 按第 27 条 defer① 起 Layer-2 真跑 → 真跑前零成本可达性验证发现**冻结门槛组合数学不可达**
→ 回 IDS 决议 → operator 在决议中补充「**operator 不具备标注能力**」,澄清为「**领域判断力不足(全维)**」
→ **forge v1「operator 可自任第二源」的落地前提被本人推翻** → KG-42「无验收主体」死结**未真解**,
只是被 D-7 挪了位置 → 按宪法「重大架构转向必须 /expert-forge」起本轮。

**注**:门槛不可达(D-1/D-2/D-3)已由第 28 条决议直接裁定并交 XenoDev 落地(直改 spec/SLA),
**与本轮正交,不在 X 的审阅目的内**(标的中的 probe / gold_layer2.py 只作背景证据读,不重开该议题)。

### 解析后的标的清单

- `discussion/009/handback/20260727T065748Z-009-pM3prime-20260727T065748Z.md`
  (类型:本仓库文件 · 198L · **触发源全文** · 尤其 §1 D-1/D-2/D-3 与 §3-4 KG-43)
- `discussion/009/handback/HANDBACK-LOG.md`
  (类型:本仓库文件 · 863L · **只读第 26 / 27 / 28 条** —— 完整决议链:D-7 改写收敛 → build 落地并判
  「KG-42 死结解」→ 前提被推翻。第 28 条是本轮 forge 的直接授权书,**必读**)
- `discussion/009/009-pM3prime/forge/v1/stage-forge-009-pM3prime-v1.md`
  (类型:本仓库文件 · 304L · **v1 verdict 全文** —— 即前提被推翻的那份。重点读三分离契约
  (错误独立性 / 领域能力 / 最终仲裁权)与「operator 可自任」的论证链条,**本轮要正面复核它**)
- `discussion/009/009-pM3prime/PRD.md`
  (类型:本仓库文件 · 270L · **重点 §2 Users(frozen「单人不懂投资」)+ §4-E1 D-7 改写块 + §7-4**)
- `discussion/009/forge/v5/stage-forge-009-v5.md`
  (类型:本仓库文件 · 431L · 证伪链 E0→E1→E2→E3 原设计 · **金标两层验收的出处与理据**,
  用于判断「Layer-2 若不成立,整条证伪链还剩什么」)
- `/home/ys/codes/XenoDev-009/specs/009-pM3prime/SLA.md`
  (类型:外部 repo · 95L · **重点第 28 行**:「第二源资格从『输出一致率』refactor 为『逐维双错率 +
  abstain 覆盖率 + 外证据锚 + 盲标隔离』」+ Layer-2 逐维门槛表)
- `/home/ys/codes/XenoDev-009/specs/009-pM3prime/spec.md`
  (类型:外部 repo · 465L · **重点 §O8 / D-7 / C9 仲裁 / B5 诚实边界**)
- `/home/ys/codes/XenoDev-009/specs/009-pM3prime/risks.md`
  (类型:外部 repo · 106L · **重点 E1-R2** 双模型 echo-chamber 与 009-pForge G-R1 先例)
- `/home/ys/codes/XenoDev-009/projects/004-pB/src/decision_ledger/extraction/gold_layer2.py`
  (类型:外部 repo · 500L · **背景证据** · `:203` 第二 LLM 终审红线 / `:301` legacy 分叉 /
  `:369` passed 合取 / `mapping_agreement_rate` 与 `coverage_denominator` 语义)
- `/home/ys/codes/XenoDev-009/projects/004-pB/scripts/layer2-feasibility-probe.py`
  (类型:外部 repo · 196L · **背景证据** · 门槛不可达的可复现证明 · 当前 exit 1)

**沙箱注记**:X 含 5 个 XenoDev-009 外部 repo 路径。Codex 默认沙箱在 ideababy_stroller 内,
读 `/home/ys/codes/XenoDev-009/*` 可能 BLOCK。**v1 用同构配置跑通过(outbox 四轮无 BLOCK)**,
故本轮沿用。若 Codex 端仍 BLOCK,按 forge-protocol §"Codex sandbox edge cases" 处理
(剔标的重跑 / 调沙箱 scope / 关键内容直贴)。orchestrator 每次 phase 推进前 grep outbox 首 30 行有无 `Verdict: BLOCK`。

## Y · 审阅视角

✅ **验证方法学 / 认识论(核心)** —— 金标验收的认识论基础:**真值(gold)到底从哪里来、谁能证伪它、
   一个不具备领域判断力的主体能否产生合法真值**。D-7 的「错误独立性」论证解决的是「两方不共享盲点」,
   本轮要审的是它**是否也解决了「gold 本身是不是真值」**。这是本轮死结所在。

✅ **统计效力与可证伪性** —— n=41 的样本量、弱监督 / 无金标评测方法的统计性质、降级验收之后
   还剩多少真实证伪力。防止产出一个「跑得动但验收不了任何东西」的 harness。

✅ **成本与 v0.1 可行性** —— 每个候选方向的真实代价(外部数据购买 / 人工 / 工程量),
   以及 solo operator 在 v0.1 能不能真做。防止出一堆理论上成立、实际做不了的方案。

## Z · 参照系

**对标 SOTA**(双方各自独立检索,要求零论文重叠优先)。

本议题正落在成熟文献区,建议检索方向(非穷举、不限于此):
- 弱监督 / 无金标评测(weak supervision · Snorkel 系 · programmatic labeling)
- noisy label learning · label noise 下的评估
- distant supervision(用外部知识库自动产标注)
- 事后结果作真值(outcome-based / market-outcome labeling · 金融 NLP 中的用法)
- 无参考评测(reference-free evaluation)与其已知失效模式
- inter-annotator agreement 在**无领域专家**条件下的方法学处理
- 事实维 vs 解释维的可核验性分层(FActScore / SAFE 系「独立性来自外证据锚定」)

**binding**:v1 的皇冠自证是 **P2 双方各自跑零重叠 SOTA、各自推翻了自己的 P1**。
本轮必须重演该动作 —— 见 K 的回声室警告。

## W · 产出形态

- ✅ **verdict-only** —— 单一 verdict + 简短 rationale。本轮最关键的就是一句话:
  **金标 Layer-2 到底还成不成立、验收主体是谁**。
- ✅ **decision-list** —— 4 列矩阵(保留 / 调整 / 删除 / 新增),逐条处置 D-7 契约、三分离、
  SLA 门槛表、E2 解锁条件。
- ✅ **next-PRD** —— 下一版 PRD 草案。本轮结论很可能要改 PRD 的 **E2 解锁条件 ②** 与 **§4-E1 D-7 块**。

## K · 用户判准

本次 forge 由 hand-back `009-pM3prime-20260727T065748Z`(FU-KG43)+ operator 在 `/handback-review 009`
**第 28 条决议**中的自陈共同触发。

### 要审的核心问题

在「**operator 领域判断力不足(全维)**」这个真实约束下,证伪链 E1→E2 的「金标 Layer-2 验收」
**到底还成不成立?验收主体是谁,还是根本不存在?**

### 背景与前提塌陷

- **forge v1(2026-07-23)** 对 KG-42「无验收主体」死结的解法是:第二源资格从「领域独立真人」
  refactor 为「**错误独立性代理**」三分离契约(错误独立性 / 领域能力 / 最终仲裁权),
  结论是「**operator 可自任独立第二源(靠独立性而非领域深度)· 无须前置外求真人**」。
  HANDBACK-LOG 第 27 条据此判定「KG-42 死结解」。
- **2026-07-27**,operator 自陈:**对金融新闻的 sector / direction / horizon / timepoint / ticker
  五维都没把握** —— 不是没时间(那是劳动量问题),是**没有领域判断力**(这是能力问题)。
  **v1 verdict 的落地前提被本人推翻。**

### 我要 forge 正面处理的核心张力(不要绕开)

D-7 的论证是「独立性靠**错误独立性**而非领域深度」。这个论证解决的是「**两方不共享盲点**」,
但**不解决「gold 本身是不是真值」**。

三方对比(machine / human / gold)里 **gold 是真值锚** —— human 和 machine 都对着它算错误率。
一个领域外行产出的 gold(考据版),**独立性有了,正确性没有来源**。
**v1 的三分离契约在这一点上是绕过去的,不是解决的。** 本轮请正面回答它。

### 我关心的

1. 在真实约束下,金标 Layer-2 是否还有**任何**成立的形态?
   **如果没有,请直说「不成立」**,并给出诚实 STOP 的形态(以及 E2 解锁条件该怎么重定)——
   **不要为了给个交代硬凑一个降级方案。**
2. 如果有,验收主体 / 真值来源是什么?候选方向(**不限于此,欢迎全部推翻**):
   - 外部权威数据回标(事后市场真值 / 公开数据库)
   - 弱监督 / 无金标评测方法
   - 把 Layer-2 缩到**可外部核验的单一事实维**(ticker 有 watchlist 外锚、timepoint 有 `published_at`)
   - 彻底改验收范式(换一种证明「提取器有用」的方式)
3. 每个方向必须回答四问:**真值从哪来 / 谁能证伪它 / 成本是什么 / v0.1 能不能真做**。

### 我不关心 · 明确不要

- **不要**再出任何需要 operator 具备金融领域判断力的方案。这是本轮的**硬前提**,不是可以商量的参数。
- **不要**用第二个 LLM 当 Layer-2 终审(`gold_layer2.py:203` 红线;forge v1 已用两组零重叠 SOTA
  证伪 —— Nine Judges 跨 vendor φ=0.6 / Correlated Errors 350+ 模型 60% 同错。**不要重开**)。
- **不要**重新讨论 D-1 / D-2 / D-3 门槛修复 —— 那三项 IDS 第 28 条已决、XenoDev 正在落地,与本轮正交。
- **不要**动 E1 的结论(US 密度 go 已于第 25 条终裁)。

### tradeoff 姿态

我宁可接受「**Layer-2 长期 blocked、E2 不解锁、这条证伪链在 v0.1 走不通**」这个诚实结论,
也不要一个看起来能跑、实际上验收不了任何东西的降级 harness。
**自欺的成本远高于停下来的成本。**

### ⚠ 回声室警告(binding)

本 idea 的 forge **v1 / v4 / v5 连续三轮**都是「双方零方向分歧强收敛」,项目记忆已标注
「回声室风险连续」。v1 的救赎在于:**P2 阶段双方各自跑零重叠 SOTA,各自推翻了自己的 P1。**

本轮请**重复那个动作**:
- P1 阶段的直觉收敛**不算数**;
- P2 **必须**用外部实证检验自己的 P1,并**显式报告「我的 P1 哪些被推翻」**;
- 若 P3R1 发现双方毫无分歧,请**主动构造最强反对意见**再收敛,不要把「都同意」当成质量信号。

### 元教训(与本轮同源 · 一并议)

**KG-43** —— 这套框架支持「门槛预注册 · C6 不可回改」(强治理,对),但**从不验证门槛可达**。
结果冻结了一个数学上不可能通过的组合,且该组合经 **forge v1 推演 + operator 批 plan 签字 +
build 四轮对抗审**,**全程无人验算**。

请一并议:**验收设计在冻结前应当承担什么前置证明义务**(如「存在性证明:构造理想输入证明
passed=1 可达」),以及这道门该落在框架的哪一层(spec-writer / task-decomposer SKILL / PRD 模板)。

## 收敛模式

**strong-converge** —— 必须 finalize 单一 verdict;残余分歧降级为 v0.2 note。

理由:operator 需要一个能拿去行动的答案(E2 解不解锁 / 要不要停)。
回声室风险已由 K 的 binding 警告 + Z=SOTA 对冲,不靠保留分歧来治。
