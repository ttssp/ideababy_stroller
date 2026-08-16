# Forge v5 · 009-pM3prime · P3R2 · Opus 4.7 Max · 联合收敛 R2(finalize)

**Timestamp**: 2026-08-16T14:40:00+08:00
**Visibility**: 我已读对方 P3R1。
**Convergence mode**: **strong-converge**(从 forge-config 读)

## 1. 我对每条分歧的最终立场 + 让步

- **分歧 1 · `-04` 是否预设正文镜像** —— 对方:"映射表必须有消费者在相关 gate 解析" → **全让**。
  它抓住了我方案的致命处:一张没有消费 gate 的映射表,**就是又一个产生侧目录**,与我诊断的 ledger 同病。
  **最终立场**:先裁载体等级(`codified` / `note` / `explicitly-uncodified`,取自 OLRC 两级效力),
  再做映射表,且映射表**必须绑定消费 gate + 结账证据**。让步:撤回「映射表本身即产出」的隐含主张。
- **分歧 2 · 「使选项集完备」是否错误目标** —— 对方:"事实状态不可穷举,但程序可全定义" → **完全让步,我错了**。
  我 P3R1 写的「完备性不可达、可解释性才是目标」有一个危险读法:**放弃 fail-closed**。
  对方的区分更准:**语义穷举**(不可能)≠ **程序全定义**(可能且必须)——
  `known options + unclassified → 具名解释者 → 留痕复审`,**未分类默认不得自动通过**。
  让步:撤回我的表述,采用对方的二分。
- **分歧 3 · `-05` 先方法还是先状态** —— 对方:"方法是内容,状态是可消费载体" → **让步**。
  我的「先方法后状态」是个伪排序。**最终立场**:每态绑定 `{允许方法, 已知敞口, 退出证据}` 三元组,
  不争线性先后;masking 敞口(自启动图前 ~50 点)作为 `insufficient_history` 态的**必载字段**。
- **分歧 4 · 五要件与 clock 是否充分**(对方新提)—— **全让,且这是本轮对我最重的一击**。
  我的 `normative_site / owner / trigger / options / clock` **五条全部描述义务本身,没有一条描述
  消费动作与结账证据** ⇒ **我的模板犯了它所诊断的病**,v4 元条款直接命中。
  且 `clock` 在**没有自然时钟的本仓**(`warn-registry/README.md` 局限 3 已实证)不可达。
  让步:采纳 `clock_or_reachable_event`,两者皆无 ⇒ **受影响消费点 fail-closed,不得伪造到期日**;
  并补 `consumer_action` 与 `settlement_evidence` 两问。

**净移动方向:四条分歧我三全让一让 —— 从我的五要件模板移动到对方的七问消费契约。**

## 2. 联合 verdict(单一)

**五题收敛为同一件事:义务停在「产物存在」,从未走到「谁在何时读到什么、必须做什么、拿什么结账」。**
统一裁决形态 = **七问消费契约**,五题各出一条可写回条款正文的短裁决,均按七问实例化:
`normative_site`(载体**及其等级**:codified / note / explicitly-uncodified)· `owner`(责任主体)·
`trigger`(可达触发)· `options`(**程序上全定义**:known + unclassified → 具名解释者 → 留痕复审,
**未分类不得自动通过**)· `clock_or_reachable_event`(**两者皆无 ⇒ fail-closed**)·
`consumer_action`(消费者必须做的动作)· `settlement_evidence`(结账证据)。

动作分类双方一致:**`-04` / `-05` / `-12` refactor · `-11` new · `-09` refactor + new**;
总体**定向 refactor,不 redesign**。四条来自零重叠检索的硬内容必须进正文,不得只留在本文件:
① 载体分三级、且「显式不入正文」是合法态(OLRC);② **复审主体必须与 owner 分离**(DO-178C 的
独立 safety 复审);③ 小样本三档「可用 / 复审 / 抑制」+ **具名判定人**(NCHS),据此 `-09` 的
CN/HK 报 `not_estimable`、US 的字面满足**不构成对 CN/HK 的重判依据**;④ **分层可得性是汇总能力
定义的一部分**(BCBS 239),故 `-09` 必须新建 market 观测轴,改措辞补不出来。
本 verdict **不解锁**扩样与 E2,**不重开** 41 条盲标路,**不动** C6 数字,**不当场改**框架 schema。

## 3. 残余分歧降级为 v0.2 note(均带 due_gate)

- **v0.2 note 1 · KG-42 同族未解(本轮最大敞口)**:七问的 `owner` 与「复审主体须与 owner 分离」
  在**只有一个人的仓**里不可同时满足。本轮**不解,写成具名敞口**,严禁用「已具名」冒充「已解决」。
  **due_gate**: `forge:006:phase0`(与 `OB-...-v4-06`「具名批准」同场并案)。
- **v0.2 note 2 · 可达事件源清单未定**:本仓当前可达事件仅 gate firing 与 hand-back 到达两类,
  是否覆盖五条未验;未验期间按 fail-closed。**due_gate**: `forge:009-pM3prime:phase0`(下一轮首查)。
- **v0.2 note 3 · `-09` 观测轴实现成本未实测**:我 P1 §3 已自曝未读 `derive_stratification_market`
  实现,成本可能低估一档。**due_gate**: `xenodev:task-review`(该 task 的 pre-merge)——
  ⚠ **该 gate 至今未接线,`exposure` 必填**。

## 4. W 形态产出的初步草稿建议

- **verdict-only 关键句**:「五条义务的完成全部定义在产生侧;本轮把它们改写为**七问消费契约**,
  未分类动作一律 fail-closed,无时钟则退可达事件、再无则停。」
- **decision-list(四列 + `obligation path` + `evidence_grade` 两列)**:
  - **保留**:`-11` 的 operator-chair 具名(`independent`)· 五条的 `due_gate` 机制
  - **调整**:`-04` 载体等级 + 映射表 + 消费 gate(`SOTA-corrected`)· `-05` 三态各绑方法/敞口/退出证据
    (`SOTA-corrected`)· `-12` §4.2 加 **catch-all fail-closed 轴**而非补第四行(`SOTA-corrected`)·
    PRD §6 条件 1 改「每个拟重判市场均有可解释 per-market 读数」(`SOTA-corrected`)
  - **删除**:`-05` 的「历史足量后再说」静默态 · `-12` 的「四轮硬顶即终局」读法
  - **新增**:`-09` 的 market 观测轴(`aggregation_probe.py`)· `-11` 的 handback-review 消费步 ·
    七问模板本身(框架级 ⇒ **不当场改,走 forge 006**)
- **refactor-plan 关键模块**:① `PRD.md` §6 条件 1/2 + 新增「per-market 三档与具名判定人」节;
  ② XenoDev `spec.md` C4 行 / `SLA.md` E1 行(载体等级裁定后按级同步,**不预设三处镜像**);
  ③ `codex-review/SKILL.md` §4.2 表格 + catch-all 行(跨仓:IDS 产逐字替换授权,operator 手工送达);
  ④ `aggregation_probe.py` `_run_batch` 的结果矩阵组装段(market 轴)。
