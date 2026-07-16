# Forge v2 · 001 · P1 · GPT55xHigh · 独立审阅(no search)

**Timestamp**: 2026-07-16T19:13:53+08:00
**Searches used**: NONE in this round.
**Visibility**: I did NOT read other reviewer's P1.
**Reviewer stance**: 审阅人 — 评判已存在物,不是 daydream。

## 0. 我读到的标的清单 + 阅读策略

- 我读了:`forge-config.md`;`forge/v1/stage-forge-001-v1.md`;hand-back 13;PRD v1.3;`HANDBACK-LOG.md`;hand-back 11;L3 moderator notes;XenoDev `dogfood-backlog.md` 中 KG-B4/B7/B8/B9 与 v1 回填;T011/T021;dependency graph;真 briefing;`gate.py`;`domain/__init__.py`;forge-protocol P1 template;`AGENTS.md`。
- 我跳过的:proposal 原文按任务要求只用 forge-config 的背景摘要;`forge/v2/moderator-notes.md` 不存在;外部 repo 标的均可读,未使用摘录兜底。
- **K(用户判准)摘要**:本轮要裁的是 hand-back 13 的 A/B/C:①② 资格重裁、T010/T011 解锁前置定实、KG-B9 与 B4 合并处置。K 明确说用户在乎“边用边审计,不是停下来考试”,“T010/T011 解锁条件必须落定”,“防 V4 精神保留”,且任何新前置必须能用现有真产物立即自证,不再交纯推演可行的前置。
- 我的阅读策略:先按架构拓扑确认 ①② 是否有输入底料,再看工程纪律里的 STOP/wiring 是否有可 wire 的对象,最后用 operator 原话和 O2/O7 注入判断验证范式是否贴真实工作流。

## 1. 现状摘要(按 Y 视角组织)

### 架构设计

v1 verdict 把人肉盲测二值签字退役,改成三项机器前置;PRD v1.3 O4 与 Open questions #3 已照此落地,并保留“真 briefing 验不可判则重审”的出口。XenoDev 真跑正好触发这个出口:真实 briefing 只有位移叙事和三段 slice 文本,没有 URL/DOI/arxiv/source/node/slice 引用 token。

DAG 结构是 T004-A1 → T010/T011 → T012 → T020 → T021。T011 才产图侧 source 锚,T021 才产 3 击 evidence 链;二者都在 gate 下游。domain 里 SourceRef/EvidenceLink/MethodClaimNode.source_ref/Judgment.evidence 类型齐全,但 gate 前消费的 TimeSlice/DisplacementNarrative 无 source 回链。也就是说 ①② 不是“checker 尚未实现”,而是当前拓扑下无可判对象。

### 工程纪律

工程纪律里最强的正资产是 STOP 确实工作了:v1 自批判要求真跑自证,hand-back 13 没有硬改,而是回 IDS 重裁。gate.py 的注释也诚实承认重跑模式拒 doc/node 锚,因为 per-slice source 映射不存在、graph 未建。

问题在 B4 的新 wiring 对象。v1 把 B4 从 RERUN-PASS 改写到“三项验收 + 机器道 STOP”,但 ①② 当前不可产。若继续要求代码级 wire 到三项,会变成把强制性接到一个不存在的 artifact,重演 KG-B4 的同型错误。③ 审计通道结构可独立存在,但没有 trace 时只是通道外壳。

### 产品价值

operator 在 hand-back 11 的原话已经把产品价值锚定到“留痕可审计、快速抽查、发现问题后按 log 回溯调整”,而不是一次性考试。L3 两次 injection 也把长期信任主锚移到 O2+O7。v1 已把识伪盲测降成零解锁语义的校准活动;现在 ①② 的处境很相似:它们更像使用期抽查对象,而不是 gate 前考试题。

## 2. First-take 评分(按 Y 视角)

| Y 维度 | 倾向 | 理由 |
|---|---|---|
| 架构设计 | refactor | a1(trace 最小子集前移)是可审的架构选项,但不是我的首选:它动 Phase 边界,且必须证明不偷建 Phase 1。a2(分阶段前置)比 v1 诚实,但若只剩③作前置,会把空通道当门。a3(重估范式)最贴现状:①②应从 T010/T011 解锁前置改为使用期抽查/验收对象。 |
| 工程纪律 | refactor | 防 V4 的 FAIL→STOP 要 keep,但 B4 必须先改 wiring 对象:只能 wire 到现有真产物和治理道,不能 wire 到当前拓扑产不出的 ①②。③可 keep 为轻量审计通道,但不能伪装成 trace 已存在的证明。 |
| 产品价值 | cut/new | cut 的是“①②作为解锁前置”的资格;new 的是把 ①②作为 O2/O7 使用期审计对象来积累信任。T010/T011 解锁我倾向“直接解锁 trace-producing tasks + O2/O7/治理道兜底”,至少先解除循环依赖;等 trace 能力产出后再评价 trace,不要用尚未产出的 trace 卡住产 trace 的任务。 |

覆盖 A/B/C 的第一反应:①② 资格选 a3 为主,a2 作为过渡语言,a1 仅保留为需额外证明的架构转向;T010/T011 不应继续等三项齐备,否则循环不破;KG-B4 要与 B9 合并,先定可 wire 的真实对象;③保留,但只保留为轻量审计/治理通道,不当信任证明。

## 3. 我现在最不确定的 3 件事

1. P0.1 是否能低成本生成“per-slice source map”的最小底料而不偷建 T011?这决定 a1 是真实架构选项还是又一轮过度投资。
2. “直接解锁 T010/T011”是否应只限 trace-producing 子集,还是连 T010 规模化也一并放行?边界若画错,可能把防 V4 从过紧改成过松。
3. ③ 在 trace 尚不存在前到底能审计什么?如果只能证明目录/命名存在,它不应承担任何解锁语义;如果能记录治理事件和抽查入口,它还有保留价值。
