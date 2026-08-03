---
forge_version: v6
created: 2026-08-03T09:52:00Z
convergence_mode: strong-converge
x_hash: 5fece3ba9297e123860c376c4489b8e3
prefill_source: manual(v3/v4/v5 先例续用 — v1 已实证 proposal §001 语境错位,不走 proposal prefill)
trigger: HANDBACK-LOG 决议 40 三项路由中的第 1 项(池分区键)+ 第 (1) 条发现(needs-attention 等价放行跨层复发)· operator 选 [1]
---

# Forge Config · 001 · v6

> **本轮不是 v5 的续集,是 v5 的第一次实战回检。**
>
> v5 裁了 12 项、落了 9 项进 spec v0.7、跑了 5 轮 codex。**v6 要审的正是这个过程本身
> 产出的三样东西**:
> 1. v5 **自己降级为 v0.2 note 的那条**(池跨方向可比性),被 codex 三轮独立判 high;
> 2. v5 **新造的 §0.1 判据冻结前置**,第一次应用就判了 **v5 自己的 item 2 不具冻结资格**;
> 3. v5 的 **fallback 分支第一次被真实触发**(「方向被证不可比 → 拆池」)。
>
> ⇒ **v6 的标的不是「再修一个症状」,是「v5 那套方法论在真实压力下站不站得住」。**

## X · 审阅标的

9 件,**全部可达性已于 2026-08-03 实测验证**(`test -f` + 行数)。
⚠ **XenoDev 侧 5 件均为 worktree 副本路径**(`.claude/worktrees/001-radar-pA/`)——
**权威副本是 worktree 那份**(main checkout 的 spec 停在 v0.2)。
Codex 沙箱可能 BLOCK 外部 repo → **inbox 任务内附关键摘录兜底,BLOCK 时用摘录、不判 BLOCK**。

### 解析后的标的清单

**IDS 侧(4 件)**

1. `discussion/001/forge/v5/stage-forge-001-v5.md`(本仓库文件 · 343 行 · **本轮直接上游**)
   —— 12 项决策表(`:165` 第 2 行 = 池定义原文,**本轮争议条款的出处**)· **v0.2 note 1**
   (「累积池跨方向可比性 —— 首池达 3 条并抽样时复核」= 把本轮争议**主动降级**的那一笔)·
   §underweights 三条**本轮必须正面回应**:
   - 「item 8 应退回等 item 2 定稿后再动」(T040 起跑前提);
   - 「最可能被真跑打掉的是 **item 2 的可测性**」(**已应验** —— 见 X-6 round-2/3);
   - 「Y 未含安全独立视角…应在 v6 的 Y 里加」(**本轮 operator 明确不加,见 Y 段声明**)。
   ⚠ 另含 §"Next-version PRD draft" —— **本轮已实证该段会 stale**,见 K 理由 5。

2. `discussion/001/handback/HANDBACK-LOG.md`(本仓库文件 · 1068 行 · **40 条决议 SSOT**)
   —— **重点读第 39 条**(R5 逐条裁决 · F1-F4 全 accepted · 落地前置)与**第 40 条**(本轮触发源:
   三项路由 + 两条包外发现 + 「收敛速度不是质量指标」)。第 31/34/35/37/38 条作 lineage 背景。

3. `discussion/001/handback/20260802T162313Z-001-radar-pA-20260802T162313Z.md`(本仓库文件 · 147 行)
   —— v0.7 amendment hand-back。**重点读 §1 那张 5 轮 finding 处置表**与 §3 的 5 条 Suggested action。
   ⚠ **本包与 X-6 原始 log 之间存在转述落差,这正是 K 理由 3 的标的 —— 双方须自己比对,不要采信任一方的转述。**

4. `discussion/001/001-radar/001-radar-pA/PRD.md`(本仓库文件 · **PRD v1.7** · 215 行)
   —— O1 三个月 + 时间锚二分支 · O2 「≥3」定位澄清 · Biggest product risk 两条并列 ·
   **v1.7 response 第 1 点记录了「照抄 v5 施工单引入已被推翻写法」的完整实例**。

**XenoDev worktree 侧(5 件)**

5. `<W>/specs/001-radar-pA/spec.md`(外部 repo · **v0.7 · `status: frozen` · 462 行 · 主战场**)
   —— **重点行**:`:181-201` §1-O2 (c) 池定义 + 结果值语义 + **§0.1 自检条**(池化判据**分方向自我分类**:
   `INSUFFICIENT_EVIDENCE`/`FAIL` 方向够 block 资格,**`PASS` 方向事实上处于 warn 态**)+ 转正条件合取化 ·
   `:199` **spec-task 同步缺口条** · `:200-216` O7 二分支 · `:393` §6 O2 行(⑤⑥ pytest + 三条 ⚠ 诚实标注)。

6. ⭐ `<W>/review-log/001-radar-pA-spec-v07/round{1..5}-codex-raw.log`(外部 repo · 6 文件 211 行 ·
   **v5 时不存在的新证据 · 本轮最关键标的**)
   —— **必须读原文不读转述**。要害:
   - **round-2 [medium]**:「新池化门**违反同一 amendment 新增的冻结前置**」——§0.1 第一次应用就判 item 2
     不具冻结资格(post-hoc 制定 · 无真跑证据 · R5-F4 未复核)。**这是自指陷阱的实例,v5 的 K 明文警告过。**
   - **round-3 / round-4 [high] 各一条**:池分区键(措辞递进 —— round-3 要求 "predeclared comparability-class
     identifier",round-4 加 "invalidate/re-evaluate prior PASS")。
   - **round-5**:verdict `needs-attention` · summary **「不应合入」** · next steps **「…后再合入 v0.7」**。
   - ⚠ **round-1 打的是完全不同的一批**(dry-run fake 产物可解锁 [critical] / 自证只绑可变路径 [high] /
     JSONL 短写回滚可截断并发记录 [medium])—— **base 是 `main` 不是 `9444e09`,scope 与后四轮不同**,
     其 3 条 finding **是否已被处置、由谁处置,本轮须核**(`round1-rescoped` 是重跑的窄 scope 版)。

7. `<W>/specs/001-radar-pA/tasks/T021.md`(外部 repo · 97 行)—— `:31/:44/:60` 仍是 **v0.6 单 run 阈值**
   + 三处引用**已删的 `OQ-A1-1`**;`:68` ⑤ 测名仍写「非豁免 0/1/2 → 不得判 PASS · 恰 3 → 可 PASS」。
8. `<W>/specs/001-radar-pA/tasks/T040.md`(外部 repo · 59 行 · **v5 裁「立即起跑」而至今未起**)
   —— `depends_on: [T030,T031,T032]`(三者已 ship)· `file_domain: tests/contract/**`
   —— ⚠ **T040 的 6 个交付文件逐一实查全部缺失 ⇒ T040 零进展**。本轮须裁:这是拖延,还是 v5 §underweights 那条 fallback 已生效?
   🔴 **证据订正(2026-08-03)**:本条原写「实查该目录不存在」**为误**(从 worktree 根跑相对路径 `ls tests/contract/`,cwd 错)。该目录**存在**且已有 3 个文件(T032 / FU-A / codex 补跑 R1 的产物),**但无一属 T040 交付**。**结论不变,证据改正** —— 详见 stage 文档 §underweight-10。
9. `<W>/specs/001-radar-pA/tasks/T041.md`(外部 repo · 52 行)—— `file_domain` = `bench/**` + `tests/e2e/**`,
   **不覆盖 CLI/journal** ⇒ v5 item 7 把结果值协议「留 T041」**指向了一个不接的收件人**。

### 本轮明确不在 X 内(防 scope 蔓延)

- **framework 层全部**:R-Q7 immutable REVIEW-LOG 被绕过 / latest-pointer stale / consumer precheck
  「缺席即豁免」/ XD-39~43 / `review_path` schema / worktree hook → **全归 `/expert-forge 006`**。
- v5 已裁的 9 项(§0.1 框架本身 / 用途分类 / judge 下界 / OQ-A1-1 语义 / 术语章 / 兜底举证 /
  O7 起算点 / Unambiguous 更名 / 词汇限定)—— **除非本轮证据直接推翻,否则不重开**。
  ⚠ 例外:**§0.1 的自指后果**在 X 内(round-2 [medium]),但审的是「§0.1 判了 item 2 之后怎么办」,
  不是「§0.1 该不该存在」。

## K · 用户判准

**核心问题(双方全程扣住这两句)**:

> **(a) 一个「集合级判据」的分区键怎么定,才不会让「凑够数」变成「借不相干的数」?
> 若事后证明借错了,已经放行的结论要不要追溯——追溯的下游语义由谁定义?**
>
> **(b) 当评审说「不应合入」而落地方说「披露即可合」时,谁的话算数、以什么形式算数?**

**为什么现在 forge 这个标的**(五条,后两条是本轮核实才浮出来的):

1. **池分区键是 v5 自己降级的那条,现在有了三轮独立反对证据。**
   v5 item 2 明文「按规范化 claim + direction 去重…方向被证不可比 → 拆池,而非退回强迫单 run 产 3 条」,
   v0.2 note 1 把它降为「首池达 3 条并抽样时复核」。codex round-3/4/5 **三轮持续判 high**:
   池仅按 `epoch + rubric` 分区,**方向只用于去重不用于分区**;当前 run 只需 1 条有效判断即可借两条
   不相干方向的历史判断达 ≥3;**拆池不追溯** ⇒ 跨方向假 PASS 可被永久保留。
   ⇒ **这不是新问题,是 v5 主动记进 v0.2 note 的已知遗留,被三轮独立证据顶了回来。**

2. ⭐ **§0.1 第一次应用就判了 v5 自己的 item 2 不具冻结资格 —— 自指陷阱兑现。**
   v5 的 K 明文警告过:「别裁出一条『判据冻结前须证 X』而 X 自己证不出来」。
   codex round-2 [medium] 正是这条:池化规则 **post-hoc 制定 · 无真跑可达性证据 · R5-F4 未复核**
   ⇒ 按 §0.1 自身规则只能 shadow/warn。amendment 的处置是**把 PASS 方向标为事实 warn 态 + 合取转正条件**。
   **本轮要裁的是:这个处置到底是「§0.1 正常工作」还是「用 warn 标签把不合格判据放进了 frozen spec」?**
   两种读法导向完全相反的结论,而目前没有判据能分开它们。

3. **「needs-attention 事实等价于放行」跨层复发 —— 两层各一次 = 判据缺失不是执行疏漏。**
   XD-41 在 **code 层**(六批替代路径评审,全 needs-attention 照样 merge);本次在 **spec 层**
   (codex round-5 原文「不应合入」+「…后再合入 v0.7」→ hand-back 转述为「需 operator 决策而非本轮
   可自行收口的缺陷」→ v0.7 已 commit)。
   ⚠ **内容判断没错**(两条残留确实超 spec-writer 授权,「不自行改」是对的);**错在「不自行改」被
   等价成「所以可以合」,且这个落差没写进 hand-back §3 交给 operator。**
   ⇒ **本仓从未定义「reviewer 说不合入」对落地方的约束力**。这是本轮要造的判据。

4. **v5 的移交指向了一个不接的收件人。**
   item 7 把 `INSUFFICIENT_EVIDENCE` 的 CLI 退出码 / 产物状态字段协议「留 T041」,而 T041 的
   `file_domain` = `bench/**` + `tests/e2e/**` **不覆盖 CLI/journal**。codex round-2/3/5 三次点名。
   后果:**`evaluate` 命中样本不足时机器侧仍可能 exit 0 且正常落盘,下游自动化分不出「成功」与「非 PASS」。**
   ⇒ 一般化问题:**spec 把一件事「留给某 task」时,有没有机器门校验那个 task 的 `file_domain` 真覆盖它?**

5. **forge 施工单会 stale,而它是 PRD 修订的输入 —— 本轮已实证一次。**
   v5 §"Next-version PRD draft" 的 O7 起算写法(`start = min(...)` 单公式 + 独立 fallback)
   **在 amendment 的 codex round-4 被判 [high] 并改写为显式二分支**(单公式容纳两种互斥读法)。
   但 v5 stage doc **冻结在 forge 结束那一刻,从未随 round-4 更新**;IDS 照该施工单写 PRD v1.7 时
   **原样搬进了已被推翻的写法**,经复核拦下并已修(commit `133bba6`)。
   ⇒ **forge 施工单 ↔ 最终 spec 之间无同步机制**,这是一条真实的漂移通道,不是假想。

**关心什么**:

- **要能执行的裁决,不要正确的综述**。每条落到「spec-writer 改哪一行 / 哪个 task 收哪个 file_domain /
  T040 现在起不起跑」。
- **本轮特有 —— 回检 v5 的方法论本身**:「A + 判据 + 证不出则 B」这个四列范式,fallback 第一次被
  真实触发。**要看 fallback 本身写得够不够可执行**(v5 的 fallback 是「方向被证不可比 → 拆池」,
  而 codex 三轮都在问「谁来证、什么时候证、证之前放行的怎么办」——**fallback 缺了触发主体与追溯语义**)。
- **追溯成本要正面算**。本轮与 v5 的关键不同:v5 裁的是「判据怎么定」,**v6 要裁的是「已经放行过的
  结论要不要撤」**。撤销有真实成本(通知下游 / PASS 结论版本化),不能只喊更严格。

**不关心什么**:

- 不重开 gate 形态(v3 已裁)、不重开生效条款标的(v4 已裁)、不重开 v5 已裁的 9 项(见 X §"不在 X 内")。
- 不裁 O7 节奏(已定每周 1 新方向)、不裁第 6 轮 codex 何时跑(**决议 40 已裁 = v0.8 amendment 强制随行项**)。
- 不碰 framework 层(全归 006)。

**看重的 tradeoff**:

- **分区键**:加方向进强制分区键 = 更严,但必须同时定义「撤销既有 PASS」的下游语义(通知谁 /
  结论是否版本化 / 谁执行);维持现状 = 假 PASS 通道理论上开着。**v5 已经选过一次「维持 + 事后拆池」,
  三轮独立证据说不够 —— 再选一次「维持」需要比上次更强的理由,不能只是重复上次的理由。**
- **后悔值(承 v5)**:门松了就永远不会 fail = 永久失去信号;门挂着天天可见、可逆。存疑偏向不放松,
  **但必须给出「那到底怎么才能判 PASS」的可达路径 —— 只挂着不给路径 = 没裁。**
- **本轮新增一层**:**「诚实披露」与「放行」的边界**。把风险写进 spec 正文是好实践,但**披露不等于
  授权** —— 本轮要划出这条线,否则「显式披露」会变成万能放行券。

### ⚠ 强制产出形态(承 v5 · 本轮加一列判据)

W = **decision-list only**(operator 明确只要四列矩阵,不要 verdict-only / next-PRD / refactor-plan)。
每项必须四列齐全:**A(裁决)· 判据 · 证不出则 B(fallback)· 落点**。

**本轮对「判据」列与「fallback」列的额外硬要求**(直接来自 K 理由 1 与「关心什么」第 2 条):

- **fallback 列必须写明三件事**:**谁**触发(主体)· **什么时点**触发 · **触发前已放行的结论怎么办**。
  ⇒ v5 的 fallback「方向被证不可比 → 拆池」正是缺这三件才被 codex 连打三轮。**本轮不得重犯。**
- **判据列的 Feasible 栏承 §0.1 不接受推演**:须给真跑证据或历史证据。
- ⚠ **禁止用「已显式披露」作为任何一项的判据或 fallback**(K tradeoff 第 3 条)。

## Y · 审阅视角

**架构设计** + **工程纪律**(operator 选定 · 2 项)

- **架构设计**:池分区键是集合级判据的边界设计;「撤销既有 PASS」是下游语义设计;
  `file_domain` 覆盖性是 task 契约的结构问题。
- **工程纪律**:「reviewer 说不合入」的约束力;T040 起跑前提;spec→task 移交的机器校验。

⚠ **本轮声明的盲区(如实记 · 不追问)**:
- **未选「安全」独立视角** —— 而 v5 §underweights **明文建议 v6 补**(item 12 注入防御 / item 10
  compensating control 均为安全面判断,由工程纪律代管)。⇒ **本轮安全面仍由工程纪律代管,
  若 v6 触及注入/例外到期面,双方须显式标注「本轮无独立安全视角」而不是默认已覆盖。**
- **未选「产品价值」** —— 而 v5 §underweights 自认没回答「**1 条判断对 operator 到底还有没有决策
  价值**」,该问题直接决定池阈值该不该存在。⇒ **本轮不从产品侧重开阈值存废,只裁分区与追溯。**
  若双方认为不回答该问题就无法裁分区键,**须在 P3R1 §3 显式提出**,由 operator 决定是否补 Y。

## Z · 参照系

**对标 SOTA**(双方各自检索,≥3 次)

建议检索面(不限于此):
1. **累积证据池的分区/分层设计** —— 临床 meta-analysis 的 subgroup / pooling 合法性判据、
   系统性综述的 heterogeneity 检验(何时不允许 pool)。
2. **「评审反对但仍合入」的治理先例** —— Linux/Chromium/Kubernetes 的 NACK / blocking review
   语义、IETF rough consensus 中「反对意见如何被 overrule 且留痕」。
3. **已发布结论的撤销/版本化机制** —— 学术 retraction/erratum 流程、
   CVE 的 REJECT/DISPUTED 状态、标准的 withdrawn/superseded 语义。

⭐ **v5 实证:跨模型检索的第一价值是纠错不是共识**(Opus 的「未检索到 ⇒ 无先例」负结果被 GPT 用
W3C/NASA/IEEE 29148 打掉)。**本轮双方若得出负结果,必须显式标注「未检索到」而不是写成「无先例」。**

## W · 产出形态

**decision-list**(四列矩阵 · **唯一形态**)

operator 明确**不要** verdict-only / next-PRD / refactor-plan:
- **不要 next-PRD** —— PRD 刚进 v1.7,本轮未必产生 PRD 面变更,选了会空转。
  ⚠ 若本轮裁决**确实**需要改 PRD,在 decision-list 的「落点」列直接写明,不另起 PRD draft 段
  (**并吸取 K 理由 5:施工单会 stale,落点写行号 + 写清依赖哪条 spec 措辞的最终版**)。
- **不要 refactor-plan** —— 若裁定涉及池持久化/版本化的多文件改动,同样落在「落点」列。
- **不要 verdict-only** —— 但 **strong-converge 仍要求 P3R2 产单一 verdict**(协议要求,与 W 无关);
  该 verdict 由 synthesizer 折进 decision-list 的开头,不单列成段。

## ⚠ 本轮已发生的协议事故(如实记 · 供 synthesizer 写进 underweights)

**P1 独立性污染 + 重跑(2026-08-03)**

- **事故**:首次下发 Phase 1 时,IDS 侧(Opus)**先写完自己的 P1,再把自己的结论当作
  「建议关注面 / 结构事实 / 结构观察」写进给 Codex 的任务书 §6**。Codex 据此产出的 P1
  与 Opus P1 高度一致 —— 但**这个一致是被制造的**。
- **为什么是事故不是瑕疵**:forge 协议里 **P1 是唯一一轮双向独立**(P2 起双方互读)。
  污染 P1 = 抽掉本协议的主要认识论价值,且产生**最危险的那种失真** —— 高度一致会被
  下游读成「两个模型独立同意」。与本仓 v5 §underweights「回声室风险第 6 次连续预警」
  及 XD-41「子代理与被审代码同源同上下文」同型。
- **诚实边界**:污染主要作用在**「审什么」**(scope),较少作用在**「结论是什么」** ——
  被污染的那份在 IDS 未给答案的列(fallback / 落点)确有独立产出(如「无法枚举依赖者
  时冻结新 PASS,旧 PASS 不得作为 clean PASS 下传」、「owner 未定则保留治理阻塞项」)。
  但 v5 的教训恰恰是**scope 定义决定评审能不能看见问题**,故不因此减轻。
- **operator 裁定**:**重跑 P1**(洁净 inbox · 全新 oneshot thread)。
- **证据保全**:被污染的 Codex P1 与那份 inbox 原样归档在 `_contaminated-p1/`,**不删**;
  Opus P1 **不重写**(operator 选项为「重跑 P1 · 洁净 inbox」而非「双方都重写」)⇒
  ⚠ **残留偏置如实记**:Opus P1 仍是先于任务书写成的那一份,本轮的「独立」是
  **Codex 相对 Opus 独立**,不是双向对称独立。synthesizer 须在 underweights 保留此条。
- **洁净 inbox 的处置**:移除全部「建议关注面 / 结构观察」与定性标注(如「本轮争议条款的
  出处」「最关键标的」),只留标的位置 + 行段 + K + Y/Z/W + 硬约束 + 模板;
  显式禁止 Codex 打开 `P1-Opus47Max.md` 与 `_contaminated-p1/`。

## 收敛模式

**strong-converge** —— 必须 finalize 单一 verdict;残余分歧降级为 v0.2 note。

⚠ **本轮对 v0.2 note 的额外约束(直接来自本轮教训)**:
**v5 正是把池分区键降级为 v0.2 note 1,才留下本轮这个口子。**
⇒ 本轮任何拟降级为 v0.2 note 的项,**必须同时写明「回头看的触发时点」与「在此之前的风险敞口」**;
**禁止**出现「首次实施时复核」这类**无主体、无时点**的降级措辞(v0.2 note 1 的原话正是如此)。
