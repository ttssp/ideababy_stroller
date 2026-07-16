# Forge Stage · 001 · v2 · "①② 循环依赖续裁:退役解锁前置 → a1 最小 lineage 前移 + ①② 重绑 Phase 2/使用期"

**Generated**: 2026-07-16T13:10:00Z
**Source**: forge run v2 with X = 14 标的(1 粘贴文本 + 6 本仓库文件/stage 文档 + 7 外部 repo 文件), Y = 架构设计 · 工程纪律 · 产品价值, Z = 对标 SOTA(lineage-at-generation / staged gating / bootstrap 循环依赖 / eval-in-production 抽查), W = verdict-only + decision-list + next-PRD + refactor-plan
**Convergence mode**: strong-converge
**Rounds completed**: P1 (both), P2 (both), P3R1 (both), P3R2 (both)
**Searches run**: 8 across ~11 distinct sources(Opus 4 · GPT 4;生成时 provenance / 编译器自举 bootstrap / 分阶段 gate / eval-in-production 抽查)
**Moderator injections honored**: none(`forge/v2/moderator-notes.md` 不存在)
**Convergence outcome**: converged(双方 P3R2 §2 单一 verdict 逐点对齐,无 unresolved)

---

## How to read this

forge 是横切层(不是 L1-L4 pipeline 的一部分)。本文档是双专家(Opus 4.8 + GPT-5.5 xHigh)
审阅 + SOTA 对标 + 联合收敛后的产出,**强制给出立场**(不是候选菜单 defer 给你拍板)。

本次是 **v1 verdict 的续裁**,不是重开新议题。v1 把 P0.2 人肉盲测二值签字 gate 退役、改机器
可判三项(① trace schema 完整 / ② 证据 3 击可达 / ③ 轻量审计通道),并自带落地硬前置「先用真
briefing 验三项秒级可判性」。XenoDev 执行该硬前置真跑(run-877f1c1e · 直接源码核验 + 独立对抗
子代理交叉,零分歧),触发 verdict 自定义 STOP:**①② 在当前拓扑下无底料可判**——根因 = **循环
依赖**(能产 trace 的 T011/T021 恰在 gate 下游)= **KG-B9**。触发源 = hand-back
`001-radar-pA-20260716T085807Z`(HANDBACK-LOG 第 13 条勾「起 forge v2 重裁」)。这是 v1 Decision
menu [B] 的字面适用,即 v1 自己定义的 STOP 出口被正当触发。故下文 §"Next-version PRD draft"
表述为 **PRD v1.3 → v1.4 修订草案方向**,不是全新 PRD。

读完后你应该:
- 知道双专家对 ①② 作解锁前置资格的最终裁决,以及 hand-back 13 §3 A/B/C 三议题 + KG-B9/B4 逐条处置
- 知道支撑每条结论的具体证据(§"Evidence map" 可逐条溯源到 P1/P2/P3)
- 拿到按 W 形态准备好的可执行草案(4 列决策矩阵 + PRD v1.4 方向 + XenoDev 落地 refactor-plan)
- 能基于 §"Decision menu" 直接进入下一步行动(灌回 PRD / 跑 v3 / 局部接受 / park / abandon)

## Verdict

**forge v1「机器可判三项」的 ①② 从 T010/T011 解锁前置中退役——采纳 KG-B9,循环依赖成立**
(能产 trace 的 T011/T021 恰在 gate 下游,checker 底料 ⊂ gate 所 gate 的范围;且 ① 的谓词对象
「判断/边」在解锁时点结构性不存在)。①② **重绑两处**:T021/T022 的 ship 验收(其验收测名字面即
①②,底料彼时天然存在)+ O2/O7 使用期抽查对象(生产 trace 抽样审计范式)。**新 T010/T011 解锁前置
(单一谓词 · 同批解锁)**= a1(per-slice source 映射最小前移:仅 slice→source refs 保留,走 P0.1
amendment 通道,不建图不做 judge,不违 RT-2)落地后机器秒级判三件:briefing 带可解析 slice→source
映射 / ③ 审计通道结构就位 / 命名一致。**生效条件写死:对真 briefing rerun 自证 PASS**(fixture 仅
回归)——直接回应 K 第 4 条「连续第二次被现实打回后,新前置必须附现有真产物立即可验证的自证步骤」。
解锁语义显式命名为一次性 stage-0 治理动作 + 自托管点条款,不承担 certification。**KG-B4 wiring
对象改绑** a1 映射 + ③ 结构 + 治理 STOP 记录(全为真实存在的文件级 artifact)。KG-B7 冻结、识伪
零解锁、FAIL→STOP 双道——v1 已裁,维持不变。

## Evidence map

| 结论 | 来源 | 引用(≤15 words) | 是否有反对证据 |
|---|---|---|---|
| ①② 在当前拓扑无可判对象(非 checker 未写) | P1-Opus §1 架构 · P1-GPT §1 架构 | "①② 不是 checker 尚未实现,而是当前拓扑下无可判对象" | - |
| 循环依赖成立:trace 底料在 gate 下游(采纳 KG-B9) | hand-back 13 §2 · P3R2-Opus §2 | "能产 trace 的 T011/T021 恰在 gate 下游" | - |
| ① 谓词对象「判断/边」在解锁时点结构性不存在 | P1-Opus §1 架构 | "检查项的谓词对象在该时点无定义" | - |
| ①② 重绑 Phase 2 出口(T021 验收测字面即 ①②) | P1-Opus §1 · T021.md:40 | "T021 验收测名字面就是 ①②" | - |
| ①② 重绑 O2/O7 使用期抽查对象 | P2-Opus §1 row4 · P2-GPT §1 OpenTelemetry | "production traces become datasets 逐字对应" | - |
| a1 是 SOTA 正解方向(生成时织入 lineage),非临时补丁 | P2-Opus §1 row1 · P2-GPT §1 SLSA/PROV | "a1(per-slice source 映射)是 SOTA 正解方向" | ⚠ P1-GPT §2「a1 不是我的首选」被 P2 修正(见 §underweights) |
| a1 不被 gate 挡,走 P0.1 amendment 通道 | P2-Opus §3 修正1 · P3R1-GPT 分歧2 | "a1 改的全是已 ship 的 P0.1 组件" | - |
| 解锁 = 一次性 stage-0 治理动作,不是 certification | P2-Opus §1 row2 · P3R2-Opus §1.2 | "打破循环的正解是显式一次性 stage-0 治理动作" | - |
| 生效条件写死:真 briefing rerun 自证 PASS(fixture 仅回归) | P3R2-Opus §1.1 · P3R2-GPT §1 | "真 briefing rerun PASS 是生效条件;fixture 只作回归" | ⚠ P2-GPT §3「或 fixture」留口子,R2 已收口 |
| T010/T011 同批解锁 · 单一谓词 | P3R2-Opus §1.3 · P3R2-GPT §1 分歧3 | "两 task 共用单一 predicate 同批解锁" | ⚠ P1-GPT §3.2「是否只限 trace 子集」存疑,交双道 STOP 兜底 |
| KG-B4 wiring 改绑真实 artifact(a1+③+治理记录) | P3R2-Opus §2 · P3R2-GPT §2 | "B4 改绑 a1 产物 + ③ 结构 + 治理 STOP 记录" | - |
| a2「先启空壳 ③」原样 cut(③ 无 trace 是空壳) | P1-Opus §2 · hand-back 13 §2 诊断信号 | "③ 无 trace 时只是通道外壳" | - |
| KG-B7 冻结 / 识伪零解锁 / 双道 STOP 维持不变 | P1-Opus §2 · P3R2 双方 §2 | "v1 已裁,本次无新证据推翻" | - |

## Intake recap

### X · 审阅标的(14 个)
- `TEXT:` proposal §001「Research Radar」原文(粘贴文本 · 背景 seed,非审阅重心)
- `discussion/001/forge/v1/stage-forge-001-v1.md`(stage 文档 · **v1 verdict 本体 = 被续裁标的**)
- `discussion/001/handback/20260716T085807Z-...md`(本仓库文件 · **触发 v2 的 hand-back 13 · 第一因**)
- `discussion/001/001-radar/001-radar-pA/PRD.md`(本仓库文件 · **PRD v1.3 · O4 现行解锁语义**)
- `discussion/001/handback/HANDBACK-LOG.md`(本仓库文件 · 13 条决议史 SSOT)
- `discussion/001/handback/20260715T093226Z-...md`(本仓库文件 · hand-back 11 · 形态拒签对照组)
- `discussion/001/001-radar/L3/moderator-notes.md`(本仓库文件 · injection:主锚移 O2+O7 + v1.2 价值重定义)
- `XenoDev .../dogfood-backlog.md`(外部 · KG-B9(:646)+ B4/B7/B8 原文)
- `XenoDev specs/001-radar-pA/tasks/T011.md`(外部 · trace 底料任务 · depends_on T004-A1 = gate 下游铁证)
- `XenoDev specs/001-radar-pA/tasks/T021.md`(外部 · 证据链任务 · 验收测名字面 = checker ①②)
- `XenoDev specs/001-radar-pA/dependency-graph.mmd`(外部 · DAG 拓扑 = 循环依赖机器可查面)
- `XenoDev .../out/reconstruct/diffusion-models-20260713T133341Z.md`(外部 · 真 briefing run-877f1c1e · 零 trace token 直接证据)
- `XenoDev .../src/radar/credibility/gate.py`(外部 · :219 注释坐实无 per-slice source 映射)
- `XenoDev .../src/radar/domain/__init__.py`(外部 · SourceRef/EvidenceLink 类型在、TimeSlice/DisplacementNarrative 回链不在)

### Y · 审阅视角
- 架构设计 — pipeline 拓扑 / trace 前移动 DAG 的代价与 RT-2 边界 / T010-T011 解锁依赖
- 工程纪律 — gate/验收机制形态、防 V4 铁律、机器道 STOP wiring(KG-B4 改写落点)
- 产品价值 — 验证范式是否贴 operator 真实工作流(边用边抽查 vs 前置考试)

### Z · 参照系
- mode: 对标 SOTA(v2 新方向:lineage-at-generation vs post-hoc / staged gating / checker 底料循环依赖 bootstrap 解法 / eval-in-production 抽查;不重跑 v1 已做的 human-in-loop/盲测先例)
- 用户外部材料:无(K 内无额外链接)

### W · 产出形态
- verdict-only · decision-list · next-PRD · refactor-plan(下方四章节均需出现)

### K · 用户判准
背景:v1 已裁掉人肉盲测二值签字 gate,新解锁前置 = 机器可判三项,并自带落地硬前置「先用真
briefing 验三项秒级可判性」。XenoDev 真跑触发 verdict 自定义 STOP:**①② 无底料可判**(真 briefing
零引用 token,根因循环依赖 = KG-B9)。本次裁三件事:**A · ①② 资格重裁**(a1 trace 前移 / a2 分阶段
前置 / a3 改使用期抽查对象)· **B · T010/T011 解锁前置定实**(不能悬空)· **C · KG-B9 与 B4 合并
处置**。**我在乎**:①验证范式贴 operator 真实工作流(边用边审计,不是停下来考试)②T010/T011 解锁
条件必须落定别再悬空 ③防 V4 精神(FAIL→STOP→回流)保留形态可变 ④**这是「前置 gate 形态」连续
第二次被现实打回**——新前置必须附「用现有真产物立即可验证」的自证步骤,不许再交纯推演可行的前置
⑤别过度投资:裁决要最小化「先建再推翻」风险。**我不在乎**:v1 verdict 的面子(它自己的 STOP 出口被
正当触发,这是机制在工作);gate/checker 代码沉没成本。

### 收敛模式
strong-converge(双方 P3R2 已 converged,无 unresolved)

---

## Verdict rationale(W · verdict-only)

本次裁决的核心不是「①② 该不该存在」,而是 **v1 把它们放成解锁前置导致的拓扑错位**——用四点论证:

- **循环依赖是结构事实,不是实现进度问题**。双方 P1 独立同向确认:①② 在 T010/T011 解锁时点没有
  可判对象。gate 消费的 `TimeSlice`/`DisplacementNarrative` 无 source 回链(domain L89-210),
  真 briefing grep 引用类 token = 0(hand-back 13 §2 证据 1)。Opus P1 更深挖一层:① 原文「每条
  位移判断/边带 source trace」,但「判断」是 T020 产物、「边」是 T011 产物,在解锁边界上**谓词对象
  结构性不存在**。这不是「checker 稍调就过」,而是「机器判 trace」前提在当前拓扑下整体不成立。

- **对称解法优选「检查项后移 + 底料最小前移」而非「底料全量前移」**。SOTA 三重背书:分阶段 gate
  (P2-Opus #3 / P2-GPT Flagger)= 各阶段配各自可判的 gate,①② 是 Phase 2 形状的检查应放 Phase 2
  出口;eval-in-production(P2-Opus #4 / P2-GPT OpenTelemetry)= production traces 作抽样审计对象,
  贴 operator「边用边抽查」的真实工作流(hand-back 11 + O2/O7 injection)。故 ①② 重绑 T021/T022
  ship 验收(它们的验收测名字面就是 ①②)+ 使用期抽查,**不再作解锁前置**——与 v1 已裁的「识伪盲测
  零解锁语义」同构。

- **新解锁谓词用「a1 最小 lineage 前移」而非「纯治理签放」**。这是双方 P1/P2 的唯一实质分歧,R2
  已收敛到 a1:generation-time provenance(P2-Opus #1 / P2-GPT SLSA+W3C PROV)证明 a1 是 SOTA 正解
  方向(生成时织入 lineage),gate.py:219 注释自证 per-slice source 映射是管线缺件——a1 不是 forge
  外加发明。关键拓扑修正:a1 改的 slicer/reconstructor/writer 全是**已 ship 的 P0.1 组件**,走 P0.1
  amendment 通道**不被 gate 挡**(gate blocked 期间已 ship 过三次同款 amendment)。所以「解除循环」
  与「解锁谓词可秒级机器判」不冲突——a1 的 trace 不由被卡的 T010/T011 产出。这直接满足 K 第 4 条:
  纯治理解锁没有可跑的自证物,a1 谓词能对 rerun 的真 briefing 当场验。

- **bootstrap 循环的正解是显式 stage-0 动作,不是让系统先产出只有解锁后才产得出的自证物**
  (P2-Opus #2 编译器自举 stage-0 种子 / P2-GPT DDC)。故解锁语义显式命名为**一次性 stage-0 治理
  动作 + 自托管点条款**:机器道只验「该边界真能判的最小集」,信任的完整机器验证在 Phase 2 出口
  (①② 重绑处)自托管,并用独立路径交叉核验(DDC 同构 · 项目内 hand-back 13 已用独立子代理双路径)。
  这防止新前置第三次被误读为 certification。

## Decision matrix(W · decision-list)

| 类别 | 项 | 来源(标的具体位置) | 理由 | 优先级 |
|---|---|---|---|---|
| **保留** | T021/T022 ship 验收(①② 迁入原位) | XenoDev T021.md:40 · P3R2 双方 §2 | 验收测名字面即 ①②,底料彼时天然存在;checker 迁此不重写 | P0 |
| **保留** | O2/O7 使用期抽查(①② 主落点) | PRD O2 长期层 · P2 双方 §1 抽查 row | operator 真实工作流「边用边抽查」;SOTA eval-in-production 背书 | P0 |
| **保留** | FAIL→STOP 防 V4 双道(机器道 + 治理道) | v1 verdict · P3R2 双方 §2 | K 第 3 条精神不可丢;本次 forge 即治理道运转的实证 | P0 |
| **保留** | KG-B7 冻结 / 识伪零解锁语义 | v1 verdict · P1-Opus §2 | v1 已裁,本次无新证据推翻;别再往被拒形态加固 | P0 |
| **保留** | ③ 轻量审计通道(配 a1 后非空壳) | P1-Opus §2 · hand-back 13 诊断信号 | a1 后通道里有 slice 源映射可查,不再是空壳 | P0 |
| **调整** | ①② 绑定位置:T010/T011 解锁前置 → Phase 2 出口 + 使用期(资格改写非删除) | P3R2 双方 §2 · P1-Opus §2 | 谓词对象在 Phase 2 出口天然存在;贴使用期抽查范式 | P0 |
| **调整** | KG-B4 wiring 对象:「三项」→ a1 映射 + ③ 结构 + 治理 STOP 记录 | 本 hand-back §3 C · P3R2 双方 §2 | 先 B9 定底料位置,B4 绑真实存在的文件级 artifact(避免重蹈 wire 到产不出的 artifact) | P0 |
| **调整** | O4 初始层解锁谓词:机器可判三项 → a1 三件 + stage-0 语义 | P3R2-Opus §4 · PRD O4 v1.3 | 循环依赖推翻原三项;新谓词秒级可判且解除循环 | P0 |
| **删除** | ①② **作解锁前置的资格**(前置门形态,非 ①② 本身) | hand-back 13 §3 A · P3R2 双方 §2 | 无可判底料;继续前置只造空壳 gate,违 K 第 4 条 | P0 |
| **删除** | a2「先启空壳 ③」原样(③ 无 trace 是空壳门) | P1-Opus §2 · P1-GPT §1 | hand-back 自证 ③ 无 trace 只是通道外壳;a2 仅作 a1 排序表述有意义 | P0 |
| **删除** | 「机器可判三项」并列表述(①② 与 ③ 不再同层) | P3R2-Opus §4 · PRD Open questions #3 | ③ 是使用期抽查载体,①② 是 Phase 2 验收;混为解锁三项是拓扑错位 | P1 |
| **删除** | fixture 可替代生效自证(「或 fixture」口子) | P3R2 双方 §1 分歧1 | K 第 4 条要求「现有真产物」;fixture 仅回归,不得替代生效自证 | P0 |
| **新增** | a1 per-slice source 映射最小前移(窄授权 + RT-2 边界条款) | P2-Opus §1 row1 · P2-GPT SLSA/PROV | 仅 slice→source refs 保留,不建图不做 judge;SOTA 生成时织入正解 | P0 |
| **新增** | 单一 unlock predicate(a1 映射可解析 + ③ 结构 + 命名一致 · 同批解锁) | P3R2 双方 §1 分歧3 | 谓词只依赖 a1 amendment 产物;避免半解锁状态机 | P0 |
| **新增** | 真 briefing rerun 自证 PASS 生效条款(K 第 4 条落地) | P3R2 双方 §1 分歧1 | 谓词生效前须对真产物 rerun PASS;不许再交纯推演前置 | P0 |
| **新增** | stage-0 + 自托管点语义入 PRD/handoff | P2-Opus §1 row2 · P3R2-Opus §1.2 | 防止新前置第三次被误读为 certification | P0 |
| **新增** | unlock-preflight checker(B4 落点 · a1 谓词机器实现) | P3R2-Opus §4 · P3R2-GPT §4 | 机器道 STOP wire 到 a1 真实 artifact;S 级实现 | P0 |

## Next-version PRD draft(W · next-PRD)

> **注**:本次标的是 001-radar-pA 的 gate 解锁语义再改,**不是全新 PRD**。以下是 **PRD v1.3 → v1.4
> 的修订草案方向**(O4 初始层 + Open questions #3 重写为主),供 operator 灌回 PRD 时消费。PRD 是
> L3 后 SSOT,修订须 operator 显式批准。

```
# PRD 修订草案 · 001-radar-pA · v1.3 → v1.4

**Status**: Draft from forge v2, awaiting human approval(仅改 O4 初始层 + Open questions #3 + Scope OUT 补一条)
**Sources**: forge stage-forge-001-v2.md · hand-back 20260716T085807Z · KG-B9

## 改动点 1 · O4 初始层解锁前置重写(a1 谓词 + stage-0 语义)

- P0.2「机器可判三项」表述废止(①② 无底料 · 循环依赖 KG-B9)。新 T010/T011 解锁前置 =
  **单一谓词 · 同批解锁**,机器秒级判三件:
  ① briefing 带 per-slice source 映射且逐项可解析到检索语料(a1 最小前移产物)
  ② ③ 轻量审计通道结构就位(a1 后非空壳,里面有 slice 源映射可查)
  ③ 产物命名一致
- **生效条件(写死)**:上述谓词须在**现有真 briefing rerun 上自证 PASS** 方可生效;合成 fixture
  仅作回归测试,不得替代生效自证。(K 第 4 条:连续第二次被现实打回后的硬要求。)
- **解锁语义(显式命名)**:这是**一次性 stage-0 治理动作 + 最小机器谓词**,不承担 certification。
  **自托管点条款**:Phase 2 出口(T021/T022)①② 生效后,机器验收面从 a1 谓词升级为完整 trace 验收。

## 改动点 2 · ①② 迁移(退役出解锁前置)

①(trace/provenance schema 完整性)与 ②(证据 3 击可达性)**退出 T010/T011 解锁前置**,重绑两处:
- **T021/T022 ship 验收**:其验收测名字面即 ①②
  (`should_link_each_judgment_to_source_within_3_hops` / `should_resolve_source_ref_to_real_retrieved_document`),
  底料彼时天然存在。
- **O2/O7 使用期抽查对象**:生产 trace 抽样审计范式,贴 operator「边用边抽查」工作流。

## 改动点 3 · Open questions #3 再更新

废止「机器可判三项作 T010/T011 解锁前置」的表述(v1.3 已废「RERUN-PASS 唯一前置」,本次废三项并列)。
新表述:T010/T011 解锁前置 = a1 谓词单一门(改动点 1);①② 迁 Phase 2 出口 + 使用期抽查。

## Scope OUT 补一条(显式 non-goal)

- **①② 作 T010/T011 解锁前置**(evidence: 循环依赖 KG-B9 · 底料在 gate 下游 · 真 briefing 零 trace token · 见 §"Evidence map")

## Success looks like(O4 相关补充,回应 K)

- 解锁谓词能对现有真 briefing 秒级机器自证 PASS,不再交纯推演可行的前置(K 第 4 条)
- 循环依赖解除:产 trace 的任务不再被「尚未产出的 trace」卡住(K 第 2 条落定)

## Open questions(forge 也没解决的,降级 v0.2 note)
- ①② 在 Phase 2 出口的「秒级可判」仍是推演,T021/T022 落地时须对第一份真判断 briefing 复用同款自证协议
- a1 动冻结 `TimeSlice` 的消费面枚举(slicer/reconstructor/writer/gate/injector/序列化)—— forge-lite 教训:序列化面最易 silent 丢
- 使用期抽查频率/条件(固定比例 vs tail-sampling 式条件抽样)—— 攒 journal 数据后定
- 若 T021 长期不落地,机器验收面长期停在 a1 谓词 —— 治理道兜底,v0.2 检视是否需中间验收点
```

## Refactor plan(W · refactor-plan · XenoDev 改 spec 时直接消费)

> 骨架 = 双方 P3R2 §4 草稿建议的**并集**;冲突处以双方 §1/§2 最终立场为准。代价 S/M/L 基于 §4 建议。
> 落地在 XenoDev(唯一 L4 build runtime);IDS 侧只改 PRD + 决议,不静默改代码(防 V4 · 跨仓边界)。
> **v1 refactor plan 的模块 B(gate.py 降级校准工具)、D(journal schema)继续有效不变;模块 A/C
> 被本次 A'/C' 替换**(v1 A/C 依赖的 ①② 底料前提已被真跑推翻)。

#### 模块 A' · a1 amendment(per-slice source 映射最小前移)
- **当前问题**:管线丢弃 paper→slice 映射——papers 有可解析 ref(`Paper.source_ref`),但
  slicer→reconstructor 只保留时间窗 metadata + LLM 提炼的 structural_state(reconstructor.py:241
  model_copy 只回写 structural_state);`TimeSlice`/`DisplacementNarrative` 无 source 回链
  (domain L89-210)。gate.py:219 注释自证缺件。
- **目标态**:slicer/reconstructor/writer 生成时保留 paper→slice 映射(仅 slice→source refs,不建图
  不做 judge);`TimeSlice` 契约变更须 forge 授权(同 KG-B5 先例)+ 确认不违 RT-2「P0.1 不偷建 Phase 1」。
- **改造步骤**:1) `TimeSlice` domain 加 source refs 字段(冻结契约变更 · 授权后);2) reconstructor
  保留论文映射不丢;3) writer 把 slice→source 映射织入 briefing 产物;4) **逐面 grep 枚举消费面**
  (slicer/reconstructor/writer/gate/injector/序列化 · forge-lite 教训 KG-36 序列化面最易 silent 丢)。
- **风险**:动冻结 `TimeSlice` 的连锁面若未逐一枚举,序列化面可能 silent 丢(v0.2 note 2);RT-2
  边界若 spec 原文写死「P0.1 产物不得含图侧锚」则 a1 需更窄化(P1-Opus §3.1 不确定项)。
- **预估代价**:S-M(走已 ship P0.1 组件 amendment 通道,不被 gate 挡;主要代价 = 一个 amendment 周期)

#### 模块 B' · unlock-preflight checker + 机器道 STOP wiring(KG-B4 落点)
- **当前问题**:DAG 硬编码「P0.2-RERUN-PASS artifact」为 T010/T011 前置(v1.3 已废),但 KG-B4 的
  机器道 STOP wiring 对象「机器判三项」有一半(①②)不存在——重演 wire 到产不出 artifact 的同型错。
- **目标态**:单一 unlock predicate 机器实现——验 a1 映射可解析 + ③ 结构就位 + 命名一致;任一 FAIL
  自动 STOP;wiring 对象全为真实存在的文件级 artifact(a1 映射 / ③ 结构 / 治理 STOP 记录)。
- **改造步骤**:1) spec §5 + dependency-graph.mmd:T010/T011 前置文案改为 a1 单一谓词;2) preflight
  接入三件检查,任一 FAIL 自动 STOP;3) 保留 prd-revision-trigger 作治理道 STOP(既有通道显式命名)。
- **风险**:若 predicate 仍留在无 wiring 的库函数(KG-B4 原教训「T004 已 merge ≠ gate PASS」),等于
  换汤不换药——此项必须真 wire。
- **预估代价**:S(谓词对象是文件级存在性/可解析性,秒级可判)

#### 模块 C' · ③ 审计通道最小文件结构(配 a1 后非空壳)
- **当前问题**:③ 轻量审计通道结构未定;无 a1 前它是空壳通道(抽查无物可查 · hand-back 13 诊断信号)。
- **目标态**:轻量文件级审计通道结构(承载 a1 后的 slice 源映射,供 operator 抽查);命名一致。
- **改造步骤**:1) 定审计通道最小结构(单文件 vs 目录 · 附着 briefing);2) 接入模块 B' 的 preflight
  命名一致检查。
- **风险**:结构膨胀则新 gate 变旧仪式——v0.1 保持轻量文件级。
- **预估代价**:S

#### 模块 D' · 真 briefing rerun 自证协议(生效条件落地)
- **当前问题**:v1 verdict 的「自证步骤」只是 §underweights 建议;真跑证明推演不可信,须结构强制。
- **目标态**:解锁谓词生效前对现有真 briefing rerun 一次(既有产物 + a1 后一次轻量 rerun · 成本有界,
  不重跑烧 key),结果入 journal;PASS 方生效,fixture 仅回归。
- **改造步骤**:1) 建 rerun harness(复用既有 run-877f1c1e 产物路径);2) rerun 结果作 stage-0 自证
  证据入 journal;3) 独立路径交叉核验(DDC 同构 · 反回声室)。
- **风险**:若 a1 后 rerun 仍不达标 → 按双道回流(v0.2 检视);不达标不许硬开。
- **预估代价**:S

---

## What this menu underweights(强制自批判)

- **反对证据未充分整合 · a1 消费面代价可能不止 S 级**:§"Evidence map" 标 ⚠ 的 P1-Opus §3.2 —— 动
  冻结 `TimeSlice`(频改面:slicer/reconstructor/writer/gate/injector 全消费它)的连锁面**未逐一
  枚举**。verdict 定 a1 为 S-M 级,但 forge-lite 教训(KG-36:序列化面最易 silent 丢)提示真实代价
  可能更高。主 verdict 仍选 a1 的理由:它是 SOTA 正解方向 + 走已 ship amendment 通道不被 gate 挡;但
  **XenoDev 实装前必须逐面 grep 枚举消费面**,若序列化面代价超预期,回头重审 a1 窄度(v0.2 note 2)。

- **反对证据 · 「直接解锁」被自我推翻但过松风险仍在**:§"Evidence map" 标 ⚠ 的 P1-GPT §3.2 ——
  GPT P1 原主张「直接解锁 trace-producing tasks」,被自己 P2 的 DDC 检索部分推翻(bootstrap 要独立
  可比路径 · 不能纯治理签放)。收敛到 a1 谓词后,「T010/T011 同批解锁是否过松」的担忧仍在(P1-GPT
  §3.2)——verdict 把这条明确交给保留的双道 STOP(briefing 明显崩坏走治理道)兜底,但这是**推演级
  兜底**,未在真跑验证「过松」边界。

- **Y 视角覆盖盲区**:Y 未含「安全」。a1 织入的 source 映射的可篡改性(audit-trail 规范要求防篡改)、
  以及 slice→source 映射被 LLM 幻觉污染的可能,P1/P2 均未展开(operator 自用无对抗动机),值得
  XenoDev spec 层后续 attention。

- **K 中未充分回应的关切**:K 全部关切均已显式覆盖(①边用边审计 ✅ 主落使用期抽查 / ②T010/T011
  条件落定 ✅ a1 单一谓词 / ③防 V4 保留 ✅ 双道不变 / ④自证步骤硬要求 ✅ 真 rerun 写死 / ⑤别过度
  投资 ✅ 只做 a1 最小 amendment · ①② full checker 迁 T021 原位不先建)。无遗漏项。

- **convergence_mode 副作用(回声室风险 · 本次高危)**:strong-converge 下**双方 P1 即高度同构**
  ——三视角都指向「①② 退役 + a1 前移 + Phase 2 重绑」,几乎零实质对抗。**这是双模型回声室强化的高
  风险信号,与 v1 同型**。诚实标注两条互相修正的实证(说明不是纯回声):GPT 从「直接解锁」被自己
  P2 的 DDC 检索推翻;Opus 从「等 a1 落地后再解锁」被拓扑事实修正为「a1 走 amendment 不被 gate 挡 ·
  快与可判兼得」。但**双方都同意且可能错的判断**:①「a1 谓词秒级可判 + a1 走 amendment 通道 S-M
  级」再次是**推演**(与 v1「机器可判三项秒级可跑」同型 · 而那个正是被真跑推翻的),`TimeSlice`
  契约变更的真实代价与序列化面 silent 丢风险未真跑验证;②「①② 在 Phase 2 出口秒级可判」是把同一个
  被推翻的假设**平移到下游**——T021/T022 落地时可能发现同样不可秒级判(v0.2 note 1 已埋伏笔)。
  **建议**:a1 amendment 落地后**必须**对真 briefing rerun 自证(模块 D' 已结构强制),而非直接信推演
  ——这一次 verdict 把自证从「建议」升级为「生效条件写死」,正是吸取 v1 教训。

- **X 标的覆盖局限**:本次 X 已含 XenoDev 源码(gate.py/domain/T011/T021/DAG/真 briefing),比 v1 只
  含 KG 摘录已大幅改善——refactor-plan 模块边界基于源码实况。残余局限:RT-2 原文(spec.md §5)不在
  X 中,a1「provenance 保留 ≠ 偷建图」论证依赖其确切措辞(P1-Opus §3.1);XenoDev 实装前应以 spec
  原文校准 a1 窄度。

- **forge versioning 提示(触发 v3 的条件)**:以下新信息进入会触发 v3 并可能改变本 verdict——
  ① a1 amendment 真跑后发现 per-slice 映射**仍不可秒级判**(推翻 a1 谓词可行性 · 与 v1 同型 STOP);
  ② T021/T022 落地时 ①② 在 Phase 2 出口**仍不可秒级判**(把被推翻假设平移下游的兜底失效);
  ③ operator 使用期发现**抽查范式失效**(如「零解锁语义的使用期抽查」反而让人不做抽查 · 动机问题);
  ④ `TimeSlice` 消费面枚举发现代价远超 S-M(a1 从「最小前移」膨胀成架构大改 · 需重估 RT-2 边界)。

自批判扫描后主要盲区 = **回声室(与 v1 同型 · 本次尤重)+ 关键谓词可判性仍未真跑验证**。请注意:
本 verdict 把「机器可判性」假设从 gate 边界平移到了 a1 边界(解锁)和 Phase 2 出口(验收)——平移
本身合拓扑,但「可秒级判」在这两个新位置仍是推演。**模块 D' 的真 rerun 自证是最后防线**;forge 是
双模型综合,不是真跑数据,真实数据仍可能推翻本 verdict(与 v1 被真跑推翻同一机制)。

## Decision menu(for human)

### [A] 接受 verdict → 灌回 PRD v1.4 + 派 XenoDev 落地(本 idea 语境的「进 L4」)
```
⚠ 本标的是已 ship build 的 gate 解锁语义再改,不是新 PRD fork——不走 /plan-start 新建 branch,
   而是走「改 PRD → hand-back review 决议 → XenoDev 按新形态改 spec」的既有回流通道(沿 v1 先例)。
流程:
1. 把本 stage §"Next-version PRD draft" 的 O4 初始层 + Open questions #3 改动灌回
   discussion/001/001-radar/001-radar-pA/PRD.md(v1.3 → v1.4),operator 显式批准。
2. 在 HANDBACK-LOG.md 追加对 hand-back 20260716T085807Z 的决议 entry
   (采纳 KG-B9 + ①② 退役重绑 + a1 单一谓词 + B4 wiring 改绑 + 真 rerun 生效条款)。
3. 通过 hand-back / outbox 通道把新解锁形态 + §"Refactor plan" 四模块(A'/B'/C'/D')下发 XenoDev
   (唯一 L4 build runtime);注明 v1 模块 B/D 继续有效、A/C 被 A'/C' 替换。
4. XenoDev 按新形态改 spec §5 + dependency-graph + 实装 a1 amendment + unlock-preflight checker
   (参 §"Refactor plan")。a1 落地后**必须**对真 briefing rerun 自证 PASS 方可解锁(模块 D')。
⚠ 生效条件写死:a1 谓词须在现有真 briefing rerun 上自证 PASS(见 §underweights 回声室预警——
   这一次把自证从建议升级为硬门,正是吸取 v1「信推演被真跑推翻」的教训)。
```

### [B] 跑 forge v3(说明需要补什么)
```
/expert-forge 001
# Phase 0 intake 时调整 X / Y / Z / W / K;旧 v2 整目录保留作历史参考
```
适用:担心回声室(§underweights 已预警本次尤重)想引入更强对抗;或想把 RT-2 spec 原文
(spec.md §5)加进 X 让 a1 窄度校准到 spec 实况;或 a1 amendment 真跑后 per-slice 映射仍不可秒级判 /
T021 落地时 ①② 在 Phase 2 出口仍不可判 / operator 使用期发现抽查范式失效(见 §underweights v3 触发条件)。

### [C] 局部接受
- ✅ 采纳:①② 退役出解锁前置(采纳 KG-B9)· ①② 重绑 Phase 2 出口 + O2/O7 使用期抽查 · a1 单一
  谓词 + 真 rerun 生效条款 · KG-B4 wiring 改绑真实 artifact · 双道 STOP + B7 冻结维持
- ⏸ 挂起:a1 的 `TimeSlice` 消费面代价与窄度(等 XenoDev 逐面 grep 枚举后定死)· ③ 审计通道最小
  schema(留 spec 层)· 使用期抽查频率/条件(攒 journal 数据后定)
- ❌ 拒绝:(无 — verdict 无明显应拒项;若拒「①② 退役」则整个 verdict 不成立,应改选 [B])

### [P] Park
```
/park 001
```
保留所有 forge 产物,标记暂停。复活时不重做这一层。适用:operator 暂不推进 radar,解锁语义治理挂起。

### [Z] Abandon
```
/abandon 001
```
forge verdict 显示该 idea 不该继续做。归档 lesson 文档。**本 verdict 不指向 abandon**——它是「怎么
继续」的裁决,不是「要不要继续」;且真跑前置连续两次成功挡下过度投资,证明机制在正常工作。仅当
operator 独立判定 radar 整体不做时才选此项。

---

## Forge log
(由 /expert-forge 命令更新;记录每次 forge run 的 v 序列 + 关键 verdict 一句话)

- v2: 2026-07-16 — verdict: "①② 从 T010/T011 解锁前置退役(采纳 KG-B9 · 循环依赖成立),重绑 T021/T022 ship 验收 + O2/O7 使用期抽查;新解锁前置 = a1 per-slice source 映射最小前移(走 P0.1 amendment 通道不被 gate 挡)单一谓词同批解锁,生效条件写死『真 briefing rerun 自证 PASS』;解锁语义显式为一次性 stage-0 治理动作;KG-B4 wiring 改绑 a1 映射+③+治理记录;B7 冻结、双道 STOP 维持。"
- v1: 2026-07-16 — verdict: "P0.2 人肉盲测二值签字 gate 退役(采纳 KG-B8),T010/T011 改由机器可判三项(trace 完整/引用可达/审计通道就位)解锁;operator 移位为抽查者+journal 校准;FAIL→STOP 双道保留;B7 大部消解、B4 改写为新前置机器闭环。"
