# Forge v10 · 006 · P3R1 · GPT55xHigh · 联合收敛 R1(标分歧)

**Timestamp**: 2026-08-11T05:56:38Z
**Visibility**: 我已读双方 P1 + P2，以及对方 P3R1。
**Searches in this round**: NONE。

## 1. 整合摘要

双方已收敛到同一根因：本仓缺的不是更多提醒，而是**声明在进入系统时的语义分型与强制消费边**。RFC 1589 双侧独立取得，说明成熟 warn 治理依靠具名 owner、固定裁决 gate 与 hard/revert/defer 出口；PEP 387 又补出永久 soft advisory 的合法性。Sonar/Ruff 分别给出“新旧分域”和“失效例外机器回收”，因此现存三个“复发 ≥N 次”判据应退出。

v9 ledger 只能承载“该交付不会被忘记”：其 `skipped` 可记录具名 defer，但 9/11 obligation 无 consumer，且 ledger 不能定义 review 终态、真运行证明、权威值或路径归一。Opus 已撤回“多数只是 v9 未接线实例”及对 v9 的 SOTA 评价提升，并接受 KG-B16/B19 的 `refactor`；这些不再是实质分歧。

## 2. 我的初步 verdict（草案）

**采一条 warn 生命周期契约：新增 warn 必须声明 `soft advisory` 或 `temporary`；soft 明示无升级计划，temporary 必带 owner、due event 与已接线 consumer，未分型者由 canonical admission gate fail-closed 拒绝。**存量与新增分域，例外回收工具化；v9 ledger 只作交付承载面。XD-44′ 采用分层语义：确定性终态决定能否 ship，概率风险信号只分配注意力、不得决定放行或轮数。

## 3. 关键分歧清单

- **分歧 1 · XD-44′：终态与风险信号**
  - 我的立场：**分层并存**。`approved / exhausted-with-open-findings / chair-override` 由 ship gate 消费；风险信号仅作非阻断优先级提示。68/64 的预测能力不能承担放行，单 operator 也无本地训练依据。
  - 对方立场：“反对把风险预测模型引进本仓作 gate 判据”。我同意其 gate 边界，但保留风险提示的非规范层。
  - R2：把终态语义写进主 verdict；风险信号降为可选 v0.2 note，不产生 obligation。

- **分歧 2 · KG-B19 冲突事实**
  - 我的立场：必须保留“worktree 规约与精确路径白名单曾设计不兼容”的事实；评级仍为 `refactor`，归一与 ratchet 是消解手段。
  - 对方立场：“归一只是消解手段”。完全接受。
  - R2：事实进 evidence/rationale，不把已知冲突误写成普通实现欠债。

- **分歧 3 · KG-B16 评级**
  - 我的立场：维持 `refactor`；完整性收据堵“单侧即落地”。
  - 对方已让步：接受。R2 只需锁定 SSOT→mirror→MANIFEST 顺序与 obligation path。

- **分歧 4 · v9 定位**
  - 我的立场：接受“**形状对、覆盖不足、不得削减本轮工作量**”，但加限定：`skipped` 只能关闭“升级义务”，不能表达 advisory 本身的持续语义。
  - 对方立场：“形状对，覆盖不足”。
  - R2：ledger 承载裁决结果；warn registry/schema 承载规则语义，不混成一层。

**分型草案的自指检验**：原句“未声明分型的 warn 不得新增”若只写文档，仍会复发原病。owner 是 warn 所在 SSOT 的 owner；治理决议由 `forge:<id>:phase4` 拒绝缺 `warn_class` 的行，build/mirror 实装由 `xenodev:task-review` 与 `xenodev:ship-gate` 拒绝缺分类、或 temporary 的 `due_gate` 未接线。该拒绝为 hard gate，不是第四个 warn。

**`evidence_grade`**：保留三档；`independent` 只给交叉前独立取得的事实/结论，`SOTA-corrected` 给被外证改判者，`post-hoc-accepted` 给读对方后接受的方案。RFC 1589 这个**证据锚点**够 `independent`，但“soft/temporary 二分”整条 verdict 应标 `SOTA-corrected`；XD-44′ 三终态、KG-B16 完整性收据、KG-B18 观察值/权威值分域若标 `independent` 都会过高，应标 `post-hoc-accepted`。

**Unresolved**：无。风险模型是否落地不影响主 verdict，降 v0.2 note；字段名和具体存储属后续实现，不构成本轮架构分歧。

