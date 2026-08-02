---
forge_version: v5
created: 2026-08-02T08:20:42Z
convergence_mode: strong-converge
x_hash: 12df995ec5063e98c41082314096a9e7
prefill_source: manual(v3/v4 先例续用 — v1 已实证 proposal §001 语境错位,不走 proposal prefill)
trigger: HANDBACK-LOG 决议 31 / 34 / 35(既定 7 项)+ 决议 37 / 38(本轮新增 5 项)· operator 裁「一场裁完」
---

# Forge Config · 001 · v5

> **本次 forge 的真实标的**:不是 12 个独立议题,而是**同一根轴的 12 次发作**。
> 本项目在 v1–v4 四轮 forge + 38 条 hand-back 决议里反复撞同一件事:
> **一条机器可判的验收判据被冻结成 gate 之后,才发现它压根判不了 / 判不稳 /
> 挂错了地方 / 有两种读法 / 指的不是同一个东西。**
> 每次都是真跑(不是评审、不是推演)把它揭出来 —— 在册**七次「推演≠真跑」**。
>
> v5 要一次性裁掉这根轴,而不是再修一个症状。

## K · 用户判准

**核心问题(双方全程扣住这一句)**:

> **一条机器可判的验收判据,在被冻结成 gate 之前,必须先证明什么、挂在哪一侧、
> 由谁写、用什么词指称?**

**为什么现在 forge 这个标的**:

1. **T040 被阻塞是硬成本**。T040 任务书原文要把 §1-O2 (a)(b)(c) 固化成 BLOCK gate
   并用 mutation 证 teeth —— 而 (c) 正是争议条款。**给待改的规则装牙 = 焊死一个还没定的判据**。
   IDS 已连续三次拦下同型动作(决议 31 拦 T040 / 决议 35 §2.4 拦 P2 契约测 / 决议 35 拦 FU-C)。
2. **在册五例已经够多了,再攒就是纵容**:KG-43(数学不可达 · 0.70 > 上界 0.69756)/
   T022 judge 无下界(结构不可达)/ unlock-preflight 吃活体 top-200(可达但不可复现)/
   §7-P2 双读法(缺唯一可读性)/ **O7 缺起算点**(新 · 时钟从未启动 ⇒ 永远无法判定)。
3. **决议 37/38 又添了两个新维度**,证明这根轴还没被理解透:
   - **挂哪一侧**(产出侧 vs 验收侧)—— 「让 judge 凑够 3 条」会正面违反 spec §1-O4「不做真理机」;
   - **词汇同一性** —— 「评估 run」一词在 forge v3/v4 语境指 `reconstruct`,在 O7 语境指 `evaluate`,
     底下是两族产物;差一点就把 evaluate 产物硬塞进一道**本来就该拒它的门**。

**关心什么**:

- **要能执行的裁决,不要正确的综述**。每条都要落到「spec-writer 下一步改哪一行 / T040 按什么建测」。
- **可达性判据本身要可达** —— 别裁出一条「判据冻结前须证 X」而 X 自己证不出来(自指陷阱)。
- **裁完 T040 能起跑**。这是本轮最实的验收:v5 结束时 T040 若仍不能起跑,这场 forge 没解决主要问题。

**不关心什么**:

- 不重开 gate 形态(v3 已裁 · g1 永久退役)、不重开生效条款标的(v4 已裁 · 采 γ 已生效)。
- 不裁 O7 节奏(已定每周 1 个新方向)、不裁是否起第 6 轮 codex(operator 成本决定)。
- 不碰 framework 层(XD-41/42/43 / KG-B4 / review_path schema / worktree hook 全归 `/expert-forge 006`)。

**看重的 tradeoff**:

- **门收太松 → 无信号**(needs-attention 事实等价于放行,已实证);
  **门收太紧 → 结构性不可达**(0.70 门槛 / 下界 3),两边都出现过,要的是**中间那条能判的线**。
- **后悔值不对称**:「判据挂着不解」天天可见、可逆;「判据放松了」错了就**再也不会 fail = 永久失去信号**。
  ⇒ 存疑时偏向**不放松**,但必须给出「那到底怎么才能判 PASS」的可达路径 —— 只挂着不给路径 = 没裁。

### ⚠ 强制产出形态(本轮特有 · 基于本项目自身实证)

**每条裁决必须写成「A + 判据 + 证不出则 B」的 fallback 分支,不接受单点结论。**

依据:这是**第 5 次回声室高危**(v3/v4 §underweights 已连续预警),而 v1 / v2 / v3 的裁决
**没有一条是被「保留分歧」推翻的 —— 全是被真跑推翻的**(v1 三项判据无底料 / v2 a1 端到端验不了 /
v3 生效标的错配)。⇒ 缓解手段不是并列两个 verdict(那是 defer 不是裁),而是
**把实现选择类条款写成带触发判据的 fallback 分支 + build 侧预置同轴熔断**,
实证触发时切换 = 契约执行,零治理开销。此形态在 009 forge v6 / R16 已验证有效。

### ⚠ 反自欺条款(承 009 forge v2 先例)

009 forge v1 曾发生「**证据在场却被解释掉**」:关键事实已写在 risks.md 且在 v1 的输入里,
v1 读过并解释掉了。本轮双方**须显式回答**:
「X 里有没有哪条证据是我读到了、但用一句话绕过去的?」不回答此问的 P3R2 视为未完成。

## X · 审阅标的

12 件,**全部可达性已于 2026-08-02 实测验证**(`test -f` + 行数)。
⚠ **XenoDev 侧 8 件均为 worktree 副本路径**(`.claude/worktrees/001-radar-pA/`)——
worktree 分支领先 main **70 commits**,**权威副本是 worktree 那份**(main checkout 的 spec 停在 v0.2)。
Codex 沙箱可能 BLOCK 外部 repo → **inbox 任务内附关键摘录兜底,BLOCK 时用摘录、不判 BLOCK**。

### 解析后的标的清单

**IDS 侧(4 件)**

1. `discussion/001/handback/HANDBACK-LOG.md`(本仓库文件 · 793 行 · **38 条决议 SSOT**)
   —— 七次「推演≠真跑」lineage + 五例可达性缺陷 + 用途分类四次应用的全部一手记录。
   **重点读**:决议 31(判据形态四条送 forge)· 34(C9 交付物是边界表)· 35(唯一可读性 + 用途分类动作侧)·
   37(scope 定义 / 第 6 轮触发判据)· 38(挂哪一侧 / 词汇撞车 / O7 起算点)。
2. `discussion/001/handback/20260802T012127Z-001-radar-pA-20260802T012127Z.md`(本仓库文件 · **决议 37 源包**)
   —— codex 补跑 R1–R5 全记录:24 条 finding 逐条 · §2.6「产物能说谎」五条附「子代理为什么结构上看不出来」·
   **§2.5.3 R4-F4 两道自家守卫的真实冲突** · §4.2 残留率 40→20→50→**75%**。
3. `discussion/001/handback/20260802T073925Z-001-radar-pA-20260802T073925Z.md`(本仓库文件 · **决议 38 源包**)
   —— O7 首跑实况 · **§2.3「非豁免判断 1 条 < 下界 3」第二次独立复现**(200 篇不稀疏语料)·
   **§3.2 evaluate/reconstruct 词汇撞车三条硬证据** · §6 真跑产物全文(含 §5.6 转义受损实样)。
4. `discussion/001/001-radar/001-radar-pA/PRD.md`(本仓库文件 · **PRD v1.6** · 187 行)
   —— O1「信任第一块砖」· O2 三击 · O5 journal 后验 · O7 决策改变;**v1.5 ① per-run 自证义务**原文。

**XenoDev worktree 侧(8 件)**

5. `<W>/specs/001-radar-pA/spec.md`(外部 repo · **spec v0.6 · `status: frozen` · 327 行 · 本轮多数改动的落点**)
   —— ⚠ 改一句 = 一次完整 amendment(frontmatter `amended_at_N` + Amendment log + Version bump,
   前 4 轮 3 轮走 codex review,第 4 轮 12 轮才收敛)。**重点行**:`:84-88` O2 低置信豁口 + **OQ-A1-1** ·
   `:90` O3 · `:94` **O7(「3 个月内 ≥5 次」· 无起算点)** · `:277` §7-P2(同时引 §1-O2 (c) 与 OQ-A1-1)·
   §1-O4「低置信显式标注 · **不做真理机**」。
6. `<W>/specs/001-radar-pA/tasks/T040.md`(外部 repo · 59 行 · **被阻塞的那个 task**)
   —— `depends_on: [T030,T031,T032]`(三者已 ship ⇒ **唯一阻塞就是判据未定**);
   任务书要把 §6 verification 固化成 gate + mutation 证 teeth。
7. `<W>/projects/001-radar-pA/src/radar/lifecycle/ephemeral.py`(外部 repo · 699 行 · **C9 双门本体**)
   —— `:135 DECLARED_READ_SITES` · `:624` 门①(评估链路读点,**对 `os.open` 保守计入且无逐文件豁免**)·
   `:636` 门②(未声明读点,**有**豁免机制)。R1-F3 / R2-RF2 / R3-F2 / R4-F3 / R5-F3 五轮收紧史全在此文件。
8. `<W>/projects/001-radar-pA/src/radar/briefing/writer.py`(外部 repo · 102 行 · **R4-F4 冲突已写死在代码里**)
   —— `:85-97` 逐条写明三条路各自的问题(开豁免 = 门被人为关掉的经典前戏 / 挪模块 = 利用门①对 import 的失明 /
   改门① = 改的正是待裁的 C9 契约)。**双方直接读这段,不要从散文转述。**
9. `<W>/projects/001-radar-pA/src/radar/judge/judge.py`(外部 repo · 423 行 · **下界议题的代码面**)
   —— `:53 JUDGE_MAX_JUDGMENTS=12` 仅**上限**截断,**全文件零下限措辞**(机器核验过)。
   争点:下界该加在这里(产出侧),还是加在验收侧(跨 run 累积抽样)。
10. `<W>/projects/001-radar-pA/src/radar/credibility/selfcheck_sequence.py`(外部 repo · 314 行 · **词汇撞车的门**)
    —— `:174 _require_eval_briefing_shape` 是**正向 allowlist**,逐段要求块级来源块 ⇒
    evaluate 产物进来必然 fail-closed STOP。这是「(i) vs (ii)」定义域之争的代码面。
11. `<W>/projects/001-radar-pA/src/radar/cli/evaluate.py`(外部 repo · 213 行)
    —— `:84-90` 生产模式拒绝一切注入(R1-F1 修法)· `:145-165 run_evaluate` **只写 briefing 不产 audit.json**
    (§3.2 硬证据 1)。evaluate 那条 provenance 链的起点。
12. `<W>/projects/001-radar-pA/src/radar/journal/cli.py`(外部 repo · 321 行)
    —— `:172-187` R5-F2 修法:真跑横幅绑定 `lines[2]` **逐字相等**。evaluate provenance 链的终点,
    也是 O7 journal 行「快照确为真跑产物」这一保证的落点。**⚠ 该修法未经 codex 复核。**

## Y · 审阅视角

✅ **架构设计** — 判据挂产出侧 vs 验收侧的拓扑后果 · C9 双门的职责边界与互证关系 ·
   evaluate / reconstruct 两族产物与两条 provenance 链的结构自洽 —— v5 核心议题层

✅ **工程纪律** — 「判据冻结前须证什么」写成可执行前置 · T040 按什么形态建测才不是给未定规则焊牙 ·
   守卫冲突时的正当处置流程(什么情况下允许给安全门开豁免、由谁批) · 反自欺条款执行

✅ **产品价值** — O7 完成率是本轮唯一带墙钟的产品成功信号:§5.6 消毒转义致 briefing 可读性受损,
   而 O7 要 operator **每周真读一份、连做 5 次**,PRD O1 是「信任第一块砖」⇒
   可读性在此不是整洁问题而是**产品面风险**;以及「1 条判断」的产物对 operator 到底还有没有决策价值

## Z · 参照系

mode: **对标 SOTA**(v5 收窄方向)

**⚠ 不重跑**以下已做过的检索族:v1(human-in-loop / 盲测先例)· v2(lineage-at-generation /
staged-gating / bootstrap 循环依赖)· v3(非二值留痕验收 / advisory-vs-hard gate / 生产期抽查)·
v4(评估集污染卫生 / 生效条款绑首个真实 run / 预注册 vs 事后豁免)。

**本轮检索方向约束**:

1. **判据可达性 / 可判定性前置** — test oracle problem(测试预言难题)· mutation testing 的
   equivalent mutant 判定 · SLO error budget 的可达性与测量窗定义 · 形式化验收标准的 satisfiability 检查。
   → 有没有工程先例要求「gate 上线前先证它能被满足」?
2. **判据该挂产出侧还是验收侧** — Goodhart's law / 指标可操纵性 · 「优化产出以满足验收」的反模式 ·
   pre-registration 里 outcome definition 与 analysis plan 的分离 · sampling adequacy 不足时的既定处置
   (accumulate vs abort vs report-insufficient)。→ 直接对应「让 judge 凑 3 条 vs 跨 run 累积抽样」。
3. **安全控制的例外流程** — security control exception / risk acceptance 的正当化条件与审批分离原则 ·
   defense-in-depth 中两个 control 冲突时的裁决先例。→ 直接对应 R4-F4「能不能给门①开豁免、谁有资格批」。
4. **术语同一性** — DDD ubiquitous language / bounded context · 规范文档里同名不同义的治理先例
   (RFC 的 terminology section / 受控词表)。→ 直接对应「评估 run」撞车。
5. **测量窗起算点定义** — SLA/SLO 的 measurement window 起算约定 · 「N 个月内 ≥M 次」类条款在
   合同/合规文本里怎么定义起点才不留悬空。→ 直接对应 O7。

## W · 产出形态

✅ **verdict-only** — 核心轴的单一裁决 + rationale(「判据冻结前必须先证什么、挂哪侧、谁写、什么词」)

✅ **decision-list** — **12 项逐条裁**(保留 / 调整 / 删除 / 新增),每条须给:
   - 落点(哪个文件哪一行 / 哪条 spec 条款)
   - **fallback 分支**(A + 判据 + 证不出则 B)—— 见上文强制产出形态
   - 与其余 11 项的耦合关系(哪些必须同批落、哪些可独立)
   ⇒ 该清单直接作为 **spec v0.6→v0.7 一次性 amendment 的施工单**(spec-writer 消费,走一次 codex review)

✅ **next-PRD** — PRD v1.6→v1.7 修订草案方向(仅当裁决触及 PRD 层;否则显式写「PRD 零改动」)

**额外交付要求(不算独立 W,但必须在 decision-list 里体现)**:
**T040 起跑条件** —— v5 结束时必须能回答「T040 现在能不能起跑;若能,按什么形态建测;若不能,还差什么」。
这是本轮最实的验收。

## 收敛模式

**strong-converge** —— 必须 finalize 单一 verdict;残余分歧降级为 v0.2 note。
但 **每条裁决须带 fallback 分支**(见 K §强制产出形态)—— 这不是保留分歧,
而是把「实证可能推翻」这件事**预先写进契约**,由判据触发切换而非再起一轮 forge。
