# Codex 任务 · forge 001 v6 · Phase 1(独立审阅)

**Kickoff form**: `oneshot`(P1 是首轮,无前序上下文)
**Role**: GPT-5.4/5.6 xhigh · forge 双评审之一 · 与 Opus 独立作业(**本轮禁止读 Opus 的 P1**)
**Output**: 写 `discussion/001/forge/v6/P1-GPT55xHigh.md`,然后把同一份内容投到
`.codex-outbox/queues/001/20260803T095600-001-forge-v6-p1.md`(**文件名必须与本文件逐字一致**)

---

## 0 · 硬约束(违反即本轮作废)

- **NO web search**(SOTA 对比是 Phase 2 的事)
- 不写 PRD / dev-plan / refactor 详细方案
- 所有判断必须基于下面 X 的 9 件标的**原文**;读不到的标的**必须在 §0 显式声明「未读到」**,
  **不得**凭想象补全
- §0 必须复述 K 并说明你的阅读策略
- 篇幅:**目标 800-1500 CJK 字符**。⚠ **若超标,具名声明即可,严禁用 `sed`/截断做有损机械压缩**
  (v5 本轮踩过:GPT 用 `sed` 压缩致内容受损,已裁定「宁可超标具名声明」)

## 1 · 本轮是什么

**不是 v5 的续集,是 v5 的第一次实战回检。**

v5 裁了 12 项 → 9 项落进 `spec.md` v0.6→v0.7 → 跑了 5 轮 codex adversarial-review →
最终 verdict `needs-attention`(**未 approve**)。v6 要审的正是这个过程产出的三样东西:

1. v5 **自己降级为 v0.2 note 的那条**(池跨方向可比性),被 codex round-3/4/5 **三轮独立判 high**;
2. v5 **新造的 §0.1「判据冻结前置」**,第一次应用就判了 **v5 自己的 item 2 不具冻结资格**(自指);
3. v5 的 **fallback 分支第一次被真实触发**(「方向被证不可比 → 拆池」)。

## 2 · K · 用户判准(必须全程扣住)

> **(a) 一个「集合级判据」的分区键怎么定,才不会让「凑够数」变成「借不相干的数」?
> 若事后证明借错了,已经放行的结论要不要追溯——追溯的下游语义由谁定义?**
>
> **(b) 当评审说「不应合入」而落地方说「披露即可合」时,谁的话算数、以什么形式算数?**

**关心**:能执行的裁决(落到「改哪一行 / 哪个 task / 起不起跑」)· **回检 v5 的四列范式**
(A + 判据 + 证不出则 B + 落点)在 fallback 首次被触发时够不够可执行 · **追溯成本要正面算**
(v6 与 v5 的关键不同:v5 裁「判据怎么定」,v6 裁「已放行的结论要不要撤」,撤销有真实成本)。

**不关心 / 不重开**:gate 形态(v3 已裁)· 生效条款标的(v4 已裁)· v5 已裁的 9 项 ·
O7 节奏 · 第 6 轮 codex 何时跑(已裁 = v0.8 amendment 强制随行项)· **framework 层全归 006**
(R-Q7 / REVIEW-LOG pointer / precheck 缺席即豁免 / XD-39~43 / worktree hook)。

**Tradeoff**:门松 = 永远不再 fail(永久失去信号);门紧 = 结构性不可达。
**v5 已经选过一次「维持现状 + 事后拆池」,三轮独立证据说不够 —— 再选「维持」需要比上次更强的
理由,不能只是重复上次的理由。** 且:**「已显式披露」不得作为任何一项的判据或 fallback**。

## 3 · Y / Z / W / 收敛

- **Y(审阅视角)**:**架构设计** + **工程纪律**(仅此 2 项)
  ⚠ operator **未选**「安全」与「产品价值」。v5 §underweights 曾建议 v6 补「安全」。
  ⇒ 若你的判断触及注入防御 / 例外到期 / 「1 条判断有无决策价值」,**显式标注「本轮无该视角」**,
  不要默认已覆盖,也不要擅自展开。
- **Z**:Phase 2 才对标 SOTA。**P1 禁检索。**
- **W**:**decision-list only**(四列矩阵 · 不要 verdict-only / next-PRD / refactor-plan)
- **收敛**:`strong-converge`

## 4 · X · 审阅标的(9 件 · 逐条给了推荐读取范围)

⚠ **XenoDev 侧 5 件是外部 repo 绝对路径**。若你的沙箱读不到 → **用本文件 §5 的摘录兜底,
在 §0 声明「XenoDev 侧经摘录读取」,不要判 BLOCK、不要中止本轮**。

**IDS 侧(本仓库相对路径 · 应可直读)**

1. `discussion/001/forge/v5/stage-forge-001-v5.md`(343 行)— **本轮直接上游**。
   重点:**决策表 12 项**(尤其**第 2 行 = 池定义原文**)· **v0.2 note 1**(把本轮争议主动降级的那笔)·
   **§underweights** 三条(「item 8 应退回等 item 2 定稿」/「最可能被真跑打掉的是 item 2 可测性」/
   「Y 未含安全…应在 v6 加」)· §"Next-version PRD draft"(**已实证会 stale,见 §6 观察 5**)
2. `discussion/001/handback/HANDBACK-LOG.md`(1068 行)— **只读第 39 条与第 40 条**(文件末尾约 200 行),
   其余作背景。第 40 条是本轮触发源。
3. `discussion/001/handback/20260802T162313Z-001-radar-pA-20260802T162313Z.md`(147 行)— 全读。
   ⚠ **本包与标的 6 的原始 log 存在转述落差,这正是 K(b) 的标的 —— 请自己比对,不要采信任一方转述。**
4. `discussion/001/001-radar/001-radar-pA/PRD.md`(215 行)— 读 Success O1/O2 + Biggest product risk
   + v1.7 response(记录了「照抄 v5 施工单引入已被推翻写法」的完整实例)

**XenoDev worktree 侧(绝对路径 · 沙箱可能 BLOCK → 用 §5 摘录)**
基址 `W = /home/ys/codes/XenoDev/.claude/worktrees/001-radar-pA`
(⚠ **权威副本是 worktree 这份**,XenoDev main checkout 的 spec 停在 v0.2,**不要读 main**)

5. `$W/specs/001-radar-pA/spec.md`(v0.7 · frozen · 462 行)— 重点 `:181-199`(§1-O2 (c) 池定义五条 +
   三处 ⚠ 声明)· `:200-216`(O7 二分支)· `:393`(§6 O2 行)
6. ⭐ `$W/review-log/001-radar-pA-spec-v07/round{1,2,3,4,5}-codex-raw.log` + `round1-rescoped-…`
   (6 文件 211 行)— **本轮最关键标的 · 必须读原文** · **v5 时不存在的新证据**
7. `$W/specs/001-radar-pA/tasks/T021.md`(97 行)
8. `$W/specs/001-radar-pA/tasks/T040.md`(59 行)
9. `$W/specs/001-radar-pA/tasks/T041.md`(52 行)

## 5 · 关键摘录兜底(沙箱 BLOCK 时用这些,不判 BLOCK)

### 5.1 spec v0.7 §1-O2 (c) 池定义五条(`spec.md:181-190` 要点)

- **池范围**:跨多次 `evaluate` run 累积的非豁免判断,**仅限同一 decision epoch 与同一 rubric**
- **epoch 边界**:`closes_on` 在 epoch 开始时**预先固定,不得事后延长**
- **去重**:按「**规范化 claim + direction**」去重(同一规范化 claim 出现新 anchor 时合并)
- **anchor 时效**:抽样核验时 `source_ref` anchor 必须**仍可解析**
- **借池条件**:当前 run **至少 1 条非豁免且带证据**的判断才可借历史池凑满 ≥3 判 PASS;
  当前全豁免 / 零有效判断 → **一律 `INSUFFICIENT_EVIDENCE`,旧池不得替它空过**

### 5.2 spec v0.7 三处 ⚠ 声明(要点)

- **post-hoc 声明**:累积规则是看到「1 < 3」**之后**才定的,**只对 v0.7 生效后的 run 生效,不追溯**
- **fallback**:同池多方向被证不可比 → **拆池**(非退回强迫单 run 产 3 条);
  「证明不可比」操作化 = 首次抽样核验时 **operator 就地判定**,判不可比即时拆池,
  **不追溯**已判的 PASS/INSUFFICIENT_EVIDENCE/FAIL
- **已知残留(spec 自陈)**:池**默认按 epoch + rubric 分区、不按评估方向分区**(方向仅作去重维度),
  理论上单 run 可借跨不相干方向历史判断凑满 ≥3 判 PASS,须等「被证不可比」才**事后**拆池;
  spec-writer 本轮**无权**改分区键(属架构转向)⇒ **留 v6 裁决**
- **§0.1 自检**:池化判据**分方向自我分类** —— `INSUFFICIENT_EVIDENCE`/`FAIL` 方向(fail-closed)
  满足 block gate 资格 ⇒ 现即生效;**`PASS` 方向**因证据栏依赖**尚未复核的 R5-F4** ⇒
  **不满足冻结资格,按 §0.1 fallback 应为 shadow/warn**。转正条件是**合取**:
  ① 第 6 轮 codex 复核过 R5-F2/F4 ∧ ② claim 规范化算法已在 T021 定义落地 + 三类负向测齐
- **诚实残留**:「规范化 claim + direction」去重**依赖的算法(claim 规范化函数 / 稳定 claim identity)
  本条不定义**;R5-F4 只处理 **anchor** 身份,**不处理 claim 语义身份**。
  已知攻击面 = 同义改写 / 仅换锚 / 跨 epoch 重复

### 5.3 codex 五轮 verdict 与要害 finding(逐轮 · 原文要点)

| 轮 | base | verdict | 要害 |
|---|---|---|---|
| 1 | **`main`**(scope 与后四轮不同) | needs-attention | **[critical]** dry-run fake 产物被发布成可解锁的评估证据 · **[high]** 解锁自证只绑可变路径,产物覆盖后旧 PASS 仍有效 · **[medium]** JSONL 短写回滚可截断并发 writer 已成功追加的记录 |
| 2 | `9444e09` | needs-attention | **[high]** `INSUFFICIENT_EVIDENCE` 判定条件自相矛盾(主句 OR / 本行 AND)· **[high]** v0.7 语义**无 task owner**,现有 DAG 仍会实现 v0.6 · **[medium]** **新池化门违反同一 amendment 新增的冻结前置**(§0.1) |
| 3 | `9444e09` | needs-attention | **[high]** 结果分类重叠,违约可被报成证据不足(须定序)· **[high]** **池范围允许不相干方向互相满足**(建议 keyed by "predeclared comparability-class identifier")· **[high]** 规范行为无可执行 owner |
| 4 | `9444e09` | needs-attention | **[high]** claim 去重未定义时 PASS 门却可转正 · **[high]** **池分区允许不相干方向互相满足**(建议加 direction 进**不可变**池键 ∧ **"invalidate/re-evaluate prior PASS"**)· **[high]** O7 有两个互斥失败日期 |
| 5 | `9444e09` | **needs-attention** | 仅剩 2 条:**池未按方向分区** · **CLI/journal 结果值接口协议无 owner**。summary 原文:**「不应合入:新池化规则允许跨方向假 PASS,且新增结果状态仍没有机器可观察的接口契约。」** next steps 原文:**「冻结并实现三态结果的 CLI/产物协议**后再合入** v0.7。」** |

⚠ **round-1 的 base 是 `main`,与后四轮(`9444e09`)不同,打的是完全不同的一批问题。
其 3 条 finding 是否已被处置、由谁处置 —— 本轮须核。**

### 5.4 hand-back 对 round-5 的转述(K(b) 的标的)

hand-back §1 原文:最终 verdict `needs-attention`(非 approve),但收敛到的 2 条残留
**「均已被识别为需要 operator/IDS 决策的架构 / task-assignment 问题,而非本轮可自行收口的缺陷」**,
显式披露入 spec 正文即视作完成。**v0.7 随即 commit 落地。**

### 5.5 task 三件的硬事实

- **T021**(97 行):`:31/:44/:60` 仍是 **v0.6 单 run 阈值**(非豁免 0/1/2 → 不判 PASS · 恰 3 → 可 PASS),
  三处引用**已从 spec 整条删除的 `OQ-A1-1``;`:68` ⑤ 测名仍是旧语义
- **T040**(59 行):`depends_on: [T030,T031,T032]`(三者**已 ship**)· `file_domain: tests/contract/**`
  · v5 item 8 裁「**立即起跑**」· **实查 `tests/contract/` 目录不存在 ⇒ 零进展**
  · item 8 **自带 fallback**:「item 2 累积语义被证不可测 → 该条降 **warn-only 断言 + 记 baseline**,
  **不阻断**其余 5 文件 ship」
- **T041**(52 行):`file_domain` = `bench/**` + `tests/e2e/**`(**不覆盖 CLI/journal**)·
  `depends_on: [T040]` · title = 「O3 延迟计时 harness + 真实评估验证脚手架」·
  交付物是**测量工具**(bench/e2e),不是运行时契约

## 6 · 请你独立回答的问题(不要看 Opus 的 P1)

按 P1 模板产出 **§0 标的清单 + 阅读策略 + K 摘要 / §1 现状摘要(按 Y 两视角)/
§2 First-take 评分(keep / refactor / cut / new + 理由)/ §3 你现在最不确定的 3 件事**。

以下是**建议关注面,不是答案,也不要求逐条回应** —— 你应当独立判断,**尤其欢迎指出这些面本身问的不对**:

1. **分区键**:direction 该不该进强制池键?进了之后「拆池 → 撤销既有 PASS」的下游语义谁定义?
   ⚠ 注意一个结构事实:**direction 目前在去重键里(抬高计数),却不在分区键里(不限制借用)**。
2. **单调性**:spec §1-O2 (c) 中「不追溯」出现三次(post-hoc / 拆池 / 结果值语义),各自有理由。
   叠加后系统是否具有「一次 PASS 永久 PASS」的单调性?若是,该在哪一层打断?
3. **§0.1 自指**:§0.1 第一次应用就判 v5 自己的 item 2(PASS 向)不合格。
   现在的处置(PASS 向标 warn + 合取转正条件)是「§0.1 正常工作」还是「用 warn 标签把不合格判据
   放进了 frozen spec」?**这两种读法导向相反结论,目前没有判据能分开它们。**
   附:该「按方向拆 gate 等级」目前**只以散文存在**,`usage:` 标签体系不表达它 ⇒ T040 怎么为它建测?
4. **owner**:结果值协议「留 T041」是覆盖缺口还是范畴错误(T041 交付测量工具而非运行时契约)?
   一般化:**spec 把一件事「留给某 task」时,有没有机器门校验那个 task 的 `file_domain` 真覆盖它?**
5. **T040 起跑**:现在起跑,还是等 v6 收敛?
   (注意 item 8 自带 fallback 且 §0.1 已把 PASS 向定成 warn —— 这是否正好落进该 fallback 射程?)
6. **K(b) 的判据**:amendment 在 codex verdict ≠ approve 时能不能 ship?谁批?
   ⚠ 一个结构观察供你证伪:**§0.1 要求 gate 的「责任人」不得是 spec-writer 自批,
   但安装 §0.1 的这次 amendment,其「可否 ship」恰恰由 spec-writer 自批。**
7. **回检 v5 范式**:四列里的 **fallback 列**,最小必需字段是什么?
   (v5 的 fallback 写了动作没写主体/时点/既有结论处置;amendment 补了主体与时点,
   既有结论处置补出来的是「不追溯」。)
8. **边界质疑(欢迎推翻)**:「amendment ship 前谁批」与「forge 施工单会 stale」——
   这两条该归本轮(001)还是归 framework(006)?operator 已把前者路由给 001,后者尚未路由。

## 7 · 投递

写完后:

```bash
cp discussion/001/forge/v6/P1-GPT55xHigh.md \
   .codex-outbox/queues/001/20260803T095600-001-forge-v6-p1.md
```

⚠ **HEAD 一致性合同**:HEAD 内容 = inbox 文件名 = outbox 文件名,**三者必须逐字一致**,
否则 `cdx-queues` 永远 pending。

若任一标的读不到导致你无法作业 → 在 outbox 文件**首 30 行内**写 `Verdict: BLOCK` + 具体原因。
⚠ **但 XenoDev 侧读不到不算 BLOCK**(用 §5 摘录兜底即可)。
