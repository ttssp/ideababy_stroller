---
forge_version: v4
idea: 009
fork: 009-pForge
scope: forge-lite
convergence_mode: strong-converge
prefill_source: manual
x_hash: 0e9b1a4d7c2f5836a21e4f90b7d6c318
created: 2026-07-06T04:15:33Z
trigger: T015 hand-back（20260706T040059Z · prd-revision-trigger）· O8 下游集成架构缺口
---

# Forge v4 · 009-pForge · O8 下游集成:alpha「非方向 evidence」怎么上台

## scope 说明 · forge-lite

这是 **forge-lite**（同 v3）—— 一个**聚焦的架构决策**,不是重审整个 009。方向已明确
（T015 揭的 O8 下游缺口）,X 标的收窄到「D-M2-1 O8 定义 + 004 三处下游 + alpha_lane 能力层」。
只 P1 双方独立审 → 若收敛直接 synthesizer;若分歧升级补 P2。**不跑 5 轮全 forge。**

## X · 审阅标的（6 个 · 全可达已验证）

1. **T015 hand-back** `discussion/009/handback/20260706T040059Z-009-pForge-20260706T040059Z.md`
   （R1→R3 全 adversarial 轨迹 · 核心 X · handback 类）
2. **assembler 缓存键**（R3-F1 病灶）:`XenoDev/projects/004-pB/src/decision_ledger/services/conflict_report_assembler.py`
   L156-174 `triplet` / `signals_hash`（代码 · 已核实:hash `{source_id}={direction.value}:{confidence_bucket}`,
   evidence_strength 在 inputs_used 未进 hash）
3. **Telegram 渲染**（R3-F2 病灶之一）:`XenoDev/.../telegram/conflict_narrative.py`
   L54 `signals[:3]` + `_THREE_PERMUTATIONS` + 3 显式 order 索引（代码 · 已核实:**真丢第四路**）
4. **UI 渲染**（R3-F2 病灶之二 · ⚠ 待验）:`XenoDev/.../ui/router_conflicts.py`
   L164-176（代码 · **已核实反例:L170/176 `return ordered_first_three + remaining` · 第四路其实透传不丢** —
   hand-back 的 R3-F2 对 UI 路径的断言不准 · forge 须复核并纠正）
5. **alpha_lane 能力层**（已稳 · NO_VIEW+evidence_strength 语义来源）:
   `XenoDev/projects/009-pForge/T015/.../strategy/alpha_lane.py`（代码 · T015 worktree 未 merge）
6. **上游 signed 证据**（为什么 alpha 只能 NO_VIEW）:`XenoDev/.../alpha/realized_return.py`
   L231 excess 已按历史信号方向 signed（代码 · R1-F1 铁证根据）

## Y · 审阅视角（2）

- **架构正确性 / 器官边界** — 「非方向 evidence」是 004 决策台的新概念,怎么进 ConflictReport +
  缓存 + 渲染而不破「恰好 3 路方向票」的现有不变量 + 不违 OUT-10（不改 004 已 ship 语义除非必要）
- **产品语义 / 用户可见性** — 分析师 alpha 质量旁证对不懂投资的 operator 该**怎么展示**才有用又不误导
  （它不是第四张方向票,不能让用户误读为「4 个信号 3 多 1 空」）

## Z · 参照系

- mode: **不对标**（forge-lite · 纯内部架构审 · 004 决策台是自有器官无外部 SOTA 可比）
- 用户外部材料: 无

## W · 产出形态

- **refactor-plan** ✅（改哪些文件 + 怎么改 + 落哪个仓 + 下游 task 边界）
- **decision-list** ✅（三个子决策 a/b/c 各自 verdict）
- verdict-only / next-PRD / next-dev-plan / free-essay 未勾

## K · 用户判准（binding）

T015 揭 D-M2-1 的 O8「alpha 平权进 conflict_reports」定义抽象,004 下游为「恰好 3 路方向票」设计,
承载不了「第四路非方向 evidence」这个新概念。XenoDev 已在 alpha_lane.py 内定死 alpha 的信号形态
（`direction=NO_VIEW · confidence=0.0 · is_directional=False · signal_kind="alpha_quality_evidence"` ·
强度进 `inputs_used["evidence_strength"]`）,但下游两处击穿需 IDS 决。

**要定死三个子决策**:
- **(a) ConflictReport 承载**:「非方向 evidence」是**扩 ConflictReport 支持一等公民**（新增 evidence 类字段/类型,
  显式区分方向票 vs 非方向 evidence）,还是**复用现有 direction 5 值**（NO_VIEW 塞进去 + 强度另放）?
- **(b) 缓存键语义**（R3-F1 silent-wrong · 必须解）:assembler 的 signals_hash 是否纳入 evidence 强度
  （evidence_strength / z_excess / signal_kind / is_directional）?否则强/弱/error alpha 全 hash 成
  `NO_VIEW:low` → 复用旧 divergence_root_cause = silent-wrong。修法:纳入 hash · 还是结构化输入前禁该路径缓存?
- **(c) 渲染**:Telegram（真丢第四路）+ UI（须复核是否真丢）从「固定 3 路方向票」改「N 路 + 方向票/非方向
  evidence 分区展示」?「非方向 evidence 怎么展示」本身是产品决策（对 operator 怎样才有用不误导）。

**binding**:
① 死守 alpha_lane 已定的 NO_VIEW 非方向语义（不重议 alpha 该不该产方向 · R1/R2 已证不能）;
② 最小冲击优先,但 **R3-F1 缓存 silent-wrong 是硬 bug 必须真解**（不能降级）;
③ 守 OUT-10 边界 —— 能不改 004 已 ship 就不改;若必须改 assembler/渲染（spine/UI）,明确这是**授权的下游集成**
   而非越界,且改动要可控（不牵动无关 task）;
④ 契约要能直接指导 XenoDev 起「下游集成」FU-task（拆新 task 还是并入 T016 · 给边界）;
⑤ **产品视角不能省** —— (c) 的展示形态要对不懂投资的 operator 真有用（K 的 O6/O8 初心:让分析师历史 edge
   质量作为旁证影响决策信心,而非当第四票混淆方向多空计数）;
⑥ 轻收尾（forge-lite · 可执行优先 · 若某子决策超出最小契约就降级 v0.2 note）。

## 候选提示（供双方 first-take · 非预设答案）

三个子决策不是孤立的 —— (a) 的选择约束 (b) 和 (c):
- 若 (a) 扩 ConflictReport 一等公民 → (b) 缓存键自然纳入新 evidence 字段 + (c) 渲染显式分区,最干净但冲击最大
- 若 (a) 复用 direction → (b) 需专门把 evidence_strength 塞进 hash（易漏）+ (c) 渲染要在 NO_VIEW 里二次判别
  是否 alpha,最省改动但语义最脆
- 中间路:(a) 轻扩（ConflictReport 加一个 `evidence_lanes` 旁路,不动 3 路方向票主结构）→ 平衡

双方独立 first-take 评这三个子决策各自的 verdict + 三者组合的最优路径。
