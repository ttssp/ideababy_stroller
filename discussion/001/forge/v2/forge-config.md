---
forge_version: v2
created: 2026-07-16T10:53:37Z
convergence_mode: strong-converge
x_hash: e493adec62fb18864b7a14055b375970
prefill_source: v1-config+handback-13(proposal prefill 跳过 — v1 已实证 proposal §001 语境错位)
---

# Forge Config · 001 · v2

> **本次 forge 的真实标的**(v1 续裁):forge v1 verdict 的「机器可判三项」新前置被 XenoDev
> 真跑触发自定义 STOP —— ①(trace schema 完整性)②(证据 3 击可达性)在当前 pipeline 拓扑
> 下**无底料可判**,根因 = 循环依赖(能产 trace 的 T011/T021 恰在 gate 下游)= **KG-B9**。
> 触发源 = hand-back `001-radar-pA-20260716T085807Z`(HANDBACK-LOG 第 13 条决议勾「起
> forge v2 重裁」)。这是 v1 Decision menu [B] 的字面适用(「XenoDev 真跑后三项 checker
> 可判性被推翻,需重裁」),即 v1 自己定义的 STOP 出口被正当触发。

## X · 审阅标的

来源:v1 forge-config X 全集续用(去掉已消化项)+ hand-back 13 新证据面(XenoDev spec
侧 3 件 + 源码/产物 4 件)。全部 13 件可达性已验证(2026-07-16)。

### 解析后的标的清单

1. `TEXT:` proposal §001「Research Radar」原文(proposals.md:99-134)(类型:粘贴文本 · 背景 seed,非本次审阅重心;v1 config 内有摘要)
2. `discussion/001/forge/v1/stage-forge-001-v1.md`(类型:stage 文档 · **v1 verdict 本体 = 被续裁标的**,含机器可判三项定义 + Decision menu [B] STOP 出口 + §underweights 回声室预警)
3. `discussion/001/handback/20260716T085807Z-001-radar-pA-20260716T085807Z.md`(类型:本仓库文件 · **触发 v2 的 hand-back 13 · 第一因**,真跑证据 file:line 全集 + §3 A/B/C 三议题)
4. `discussion/001/001-radar/001-radar-pA/PRD.md`(类型:本仓库文件 · PRD v1.3,O4 已按 v1 verdict 重写 = 现行解锁语义)
5. `discussion/001/handback/HANDBACK-LOG.md`(类型:本仓库文件 · 13 条决议史 SSOT)
6. `discussion/001/handback/20260715T093226Z-001-radar-pA-20260715T093226Z.md`(类型:本仓库文件 · hand-back 11,operator 形态拒签原话 — 「连续两次被现实打回」的对照组)
7. `discussion/001/001-radar/L3/moderator-notes.md`(类型:本仓库文件 · injection 史:主锚移 O2+O7 + v1.2 价值重定义)
8. `/home/ys/codes/XenoDev/.claude/worktrees/001-radar-pA/dogfood-backlog.md`(类型:外部 repo 文件 · ⚠ Codex 沙箱可能 BLOCK · KG-B9(:646 · **只在此 worktree 副本,main checkout 尚未合回**)+ KG-B4(:525)/B7(:588)/B8(:602)原文;inbox 任务内附关键摘录兜底,BLOCK 时用摘录不判 BLOCK。注:specs/src 类标的已验证 worktree 与 main checkout 逐字节一致,维持 main 路径)
9. `/home/ys/codes/XenoDev/specs/001-radar-pA/tasks/T011.md`(类型:外部 repo 文件 · ⚠ 同上 · trace 底料任务:depends_on T004-A1 = gate 下游铁证)
10. `/home/ys/codes/XenoDev/specs/001-radar-pA/tasks/T021.md`(类型:外部 repo 文件 · ⚠ 同上 · 证据链任务:验收测名字面 = checker ①②)
11. `/home/ys/codes/XenoDev/specs/001-radar-pA/dependency-graph.mmd`(类型:外部 repo 文件 · ⚠ 同上 · DAG 拓扑 = 循环依赖机器可查面)
12. `/home/ys/codes/XenoDev/projects/001-radar-pA/out/reconstruct/diffusion-models-20260713T133341Z.md`(类型:外部 repo 文件 · ⚠ 同上 · 真 briefing 产物 run-877f1c1e,零 trace token 直接证据)
13. `/home/ys/codes/XenoDev/projects/001-radar-pA/src/radar/credibility/gate.py`(类型:外部 repo 文件 · ⚠ 同上 · gate 源码,:219 注释坐实无 per-slice source 映射)
14. `/home/ys/codes/XenoDev/projects/001-radar-pA/src/radar/domain/__init__.py`(类型:外部 repo 文件 · ⚠ 同上 · 冻结 domain:SourceRef/EvidenceLink 类型在、TimeSlice/DisplacementNarrative 回链不在)

## Y · 审阅视角

✅ 架构设计 — pipeline 拓扑 / trace 前移动 DAG 的代价与 RT-2 边界 / T010-T011 解锁依赖 — v2 核心议题所在层
✅ 工程纪律 — gate/验收机制形态、防 V4 铁律、机器道 STOP wiring(KG-B4 改写落点)
✅ 产品价值 — 验证范式是否贴 operator 真实工作流(边用边抽查 vs 前置考试)— ③候选方向的判据层

## Z · 参照系

mode: 对标 SOTA(v2 新检索方向,不重跑 v1 已做过的 human-in-loop/盲测先例)

**检索方向约束**(限定在 v2 议题层):
- provenance/lineage **在生成时采集 vs 事后补锅**的工程先例(data lineage at generation time)
- staged / progressive gating(分阶段解锁、能力就绪后才启用检查项的先例)
- checker 底料循环依赖(bootstrap 问题)的标准解法(如何验证一个「验证能力本身被 gate」的系统)
- eval-in-production / 使用期抽查范式(trace 作抽查对象而非前置门的先例)

## W · 产出形态

✅ verdict-only — ①② 资格去留的核心裁决 + rationale
✅ decision-list — hand-back 13 §3 A/B/C 三议题 + KG-B9/B4 逐条裁决(保留/调整/删除/新增)
✅ next-PRD — PRD v1.4 草案方向(O4 解锁语义再改)
✅ refactor-plan — XenoDev 落地路径(spec §5/DAG/trace 前移模块切分),build session 直接消费

## K · 用户判准

**背景链(两句话)**:forge v1 已裁掉人肉盲测二值签字 gate,新解锁前置 = 机器可判三项
(① trace schema 完整 / ② 证据 3 击可达 / ③ 轻量审计通道),并自带落地硬前置「先用真
briefing 验三项秒级可判性」。XenoDev 真跑(run-877f1c1e,直接源码核验 + 独立对抗子代理
交叉,零分歧)触发了 verdict 自定义 STOP:**①② 无底料可判**——真 briefing 零引用 token,
根因 = **循环依赖**(能产 trace 的 T011/T021 恰在 gate 下游,checker 底料 ⊂ gate 所 gate
的范围)= KG-B9。

**本次要裁三件事(hand-back 13 §3 A/B/C)**:

**A · ①② 资格重裁**,三候选方向:
- (a1) trace 最小子集前移到 P0.1(动 DAG 拓扑 = 架构转向,须审是否违反 RT-2「P0.1 不偷建 Phase 1」原意)
- (a2) 分阶段前置——诚实承认当前拓扑下 ①② 无底料,先只启 ③+治理道 STOP,trace 前移落地后再补 ①②
- (a3) 重估范式——operator 立场本就是「边用边抽查 trace」(O2+O7 使用期治理),①② 也许根本不该作解锁前置,而该作使用期抽查对象(对齐识伪已降为零解锁语义的同一逻辑)

**B · T010/T011 解锁前置定实**(不能悬空):仅 ③+治理道先解锁 / trace 前移后三项齐备再
解锁 / 直接解锁 + O2/O7 使用期兜底——三选一或给出更好的。

**C · KG-B9 与 B4 合并处置**:B4 改写(机器道 STOP wire 到三项)的 wiring 对象一半不存在;
先定 trace 底料位置(B9),再定 B4 wire 到什么,否则重蹈「wire 到产不出的 artifact」同型错。

**我在乎**:
1. 验证范式贴 operator 真实工作流(边用边审计,不是停下来考试)
2. T010/T011 解锁条件必须落定,别再悬空一轮
3. 防 V4 精神(FAIL→STOP→回流)保留,形态可变
4. **这是「前置 gate 形态」连续第二次被现实打回**(07-15 operator 拒签形态、07-16 真跑拒
   底料)——v2 产出的任何新前置,必须附「用现有真产物立即可验证」的自证步骤,不许再交一个
   纯推演可行的前置
5. 别过度投资:T004-A1 十四轮硬化被推翻在先,checker 未建被真跑挡下在后——裁决要最小化
   「先建再推翻」风险

**我不在乎**:v1 verdict 的面子(它自己定义的 STOP 出口被正当触发,这是机制在工作);
gate/checker 代码沉没成本。

## 收敛强度

✅ strong-converge

---

## Summary for reviewers

**审阅标的总数**: 14(1 粘贴文本 + 6 本仓库文件/stage 文档 + 7 外部 repo 文件)
**视角维度**: 架构设计 · 工程纪律 · 产品价值
**参照系**: 对标 SOTA(v2 新方向:lineage-at-generation vs post-hoc / staged gating / checker 底料循环依赖 bootstrap 解法 / eval-in-production 抽查)
**预期产出**: verdict-only + decision-list + next-PRD + refactor-plan
**用户最在乎**: v1「机器可判三项」①② 被真跑推翻(循环依赖 KG-B9)后,裁 ①② 资格(trace
前移 / 分阶段前置 / 改使用期抽查对象)+ T010/T011 解锁前置定实 + B9/B4 合并处置;新前置
必须附现有产物立即可验证的自证步骤;防 V4 精神保留;不看沉没成本。
**收敛模式**: strong-converge
