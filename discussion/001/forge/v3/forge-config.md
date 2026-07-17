---
forge_version: v3
created: 2026-07-17T05:43:47Z
convergence_mode: strong-converge
x_hash: 4dbf529d9f5dd6a8b47e4a5a2e5124a5
prefill_source: v2-config+handback-17(proposal prefill 跳过 — v1 已实证 proposal §001 语境错位)
---

# Forge Config · 001 · v3

> **本次 forge 的真实标的**(v2 续裁):D′ 真 rerun(hand-back 17,`deepseek-v4-flash` · exit 0)
> 证明 **a1 机制内存层生效**(6/6 source_refs 真挂 TimeSlice),但暴露结构盲区——**真跑
> pipeline 无任何落盘产物能验 a1**(盲测面故意不渲染 refs / 审计面不落盘 / audit.json 要
> gate PASS 后才产),且「rerun 得 PASS/FAIL」二值预设本身被推翻(gate 形态 operator
> 2026-07-15 已当面否 + 无 CLI 判定入口 → 真跑走不到判定)= **001 主线第四次「推演≠真跑」**
> (前三:首跑 FAIL / operator 拒 gate 形态 / KG-B9 循环依赖)。触发源 = hand-back
> `001-radar-pA-20260717T052416Z`(HANDBACK-LOG 第 17 条决议勾「起 forge v3 重裁 gate
> 形态」)。这是 v2 verdict 自定义 v3 触发条件的字面适用。

## X · 审阅标的

来源:v2 forge-config X 骨架续用(去掉已消化项:proposal 文本 / T011·T021 spec / domain
源码 / 旧真跑产物)+ hand-back 17 新证据面(IDS 3 件 + XenoDev worktree 侧 A'/B'/D' 新模块
与 07-17 真跑产物 6 件)。全部 17 件可达性已验证(2026-07-17)。
**⚠ XenoDev 侧 9 件均为 worktree 副本路径**(`.claude/worktrees/001-radar-pA/`,领先 main
26+ commits,新模块只在此处;main checkout 无)。

### 解析后的标的清单

1. `discussion/001/forge/v2/stage-forge-001-v2.md`(类型:stage 文档 · **v2 verdict 本体 = 被续裁标的**,含 a1 单一谓词前置 + 生效条款「真 briefing rerun 自证 PASS」+ v3 触发条件 + §underweights)
2. `discussion/001/forge/v1/stage-forge-001-v1.md`(类型:stage 文档 · v1 verdict,裁掉人肉盲测二值签字的源头 + 双道 STOP 设计 + 识伪 retire-as-gate keep-as-calibration)
3. `discussion/001/handback/20260717T052416Z-001-radar-pA-20260717T052416Z.md`(类型:本仓库文件 · **触发 v3 的 hand-back 17 · 第一因**,D′ 真跑证据 + a1 可见性三条路径全堵的结构盲区 + §3 建议)
4. `discussion/001/handback/20260717T032424Z-001-radar-pA-20260717T032424Z.md`(类型:本仓库文件 · hand-back 16,DAG 重绑收口(a09d45b)+ KG-B10 两面 codex critical 提级记录)
5. `discussion/001/handback/20260715T093226Z-001-radar-pA-20260715T093226Z.md`(类型:本仓库文件 · hand-back 11,operator 形态拒签原话三条批评 = gate 四方向的源头)
6. `discussion/001/handback/HANDBACK-LOG.md`(类型:本仓库文件 · 17 条决议史 SSOT)
7. `discussion/001/001-radar/001-radar-pA/PRD.md`(类型:本仓库文件 · PRD v1.4,O4 现行解锁语义 = 被重裁对象)
8. `discussion/001/001-radar/L3/moderator-notes.md`(类型:本仓库文件 · injection 史:主锚移 O2+O7(77a5176)+ v1.2 价值重定义)
9. `/home/ys/codes/XenoDev/.claude/worktrees/001-radar-pA/dogfood-backlog.md`(类型:外部 repo 文件 · ⚠ Codex 沙箱可能 BLOCK · KG-B9/B10/B11 原文;inbox 任务内附关键摘录兜底,BLOCK 时用摘录不判 BLOCK)
10. `/home/ys/codes/XenoDev/.claude/worktrees/001-radar-pA/specs/001-radar-pA/followup-log.md`(类型:外部 repo 文件 · ⚠ 同上 · FU-D-rerun-a1-verify-blindspot 全档,commit 7d0a64c)
11. `/home/ys/codes/XenoDev/.claude/worktrees/001-radar-pA/specs/001-radar-pA/dependency-graph.mmd`(类型:外部 repo 文件 · ⚠ 同上 · 现行 DAG,a09d45b 重绑后:T003-A3→T004-A2→T004-A4 + T010/T011 depends_on)
12. `/home/ys/codes/XenoDev/.claude/worktrees/001-radar-pA/projects/001-radar-pA/src/radar/credibility/gate.py`(类型:外部 repo 文件 · ⚠ 同上 · 现行 gate 源码 = 被否形态的实现本体)
13. `/home/ys/codes/XenoDev/.claude/worktrees/001-radar-pA/projects/001-radar-pA/src/radar/credibility/audit_channel.py`(类型:外部 repo 文件 · ⚠ 同上 · audit.json **post-gate 才产**的逻辑本体(A'/C' 模块)= a1 可见性时机议题的代码面)
14. `/home/ys/codes/XenoDev/.claude/worktrees/001-radar-pA/projects/001-radar-pA/src/radar/credibility/unlock_preflight.py`(类型:外部 repo 文件 · ⚠ 同上 · B' preflight 四件验 + hard-block,机器道解锁 wiring 现状)
15. `/home/ys/codes/XenoDev/.claude/worktrees/001-radar-pA/projects/001-radar-pA/src/radar/credibility/rerun_selfcheck.py`(类型:外部 repo 文件 · ⚠ 同上 · D' selfcheck,只信 caller 布尔 = KG-B10 另一面)
16. `/home/ys/codes/XenoDev/.claude/worktrees/001-radar-pA/projects/001-radar-pA/out/reconstruct/diffusion-models-20260717T051551Z.md`(类型:外部 repo 文件 · ⚠ 同上 · **07-17 D′ 真跑盲测面产物**;⚠⚠ 同目录 answer-key 密封,**双方都不得读 key 文件**)
17. `/home/ys/codes/XenoDev/.claude/worktrees/001-radar-pA/projects/001-radar-pA/specs/001-radar-pA/verification/P0.2-trajectory-credibility-diffusion-models.md`(类型:外部 repo 文件 · ⚠ 同上 · 被否 gate 形态的签字模板,保留 run-877f1c1e 历史 FAIL 判定审计价值)

## Y · 审阅视角

✅ 架构设计 — gate 形态 / a1 产物可见性时机 / audit_channel 拓扑 / T010-T011 解锁依赖 — v3 核心议题层
✅ 工程纪律 — 验收机制形态、防 V4 铁律、真跑自证步骤可执行性、A'/B'/D' 模块改接代价
✅ 产品价值 — 验证范式是否贴 operator 真实工作流(边用边审计 vs 停下来考试)— g2/g3/g4 取舍的判据层
✅ 用户体验 — 留痕可审计验收的 operator 操作面(审计产物怎么看、多久看一次、错误恢复)— v3 新增维度

## Z · 参照系

mode: 对标 SOTA(v3 新检索方向;**不重跑** v1 已做的 human-in-loop/盲测先例、v2 已做的
lineage-at-generation/staged-gating/bootstrap 循环依赖方向)

**检索方向约束**(限定在 v3 议题层):
- 非二值/留痕型验收先例(provenance attestation 作为 release 条件 / continuous compliance / evidence-based acceptance)
- 盲测密封(answer-key sealing / holdout 保密)与审计可见性的张力如何工程化并存
- advisory gate vs hard gate 的工业实证(soft/non-blocking quality signal 何时优于阻断式,CI/CD 语境)
- 生产期抽查 / trust-after-use 替代前置 gate 的先例(progressive delivery / canary / eval-in-production)

## W · 产出形态

✅ verdict-only — gate 存废/形态四方向的核心裁决 + rationale
✅ decision-list — gate 形态 / a1 可见性时机 / T010-T011 解锁条款改写 / KG-B10 前提处置 逐条裁决(保留/调整/删除/新增)
✅ next-PRD — PRD v1.5 草案方向(O4 解锁与验收语义再改)
✅ refactor-plan — XenoDev 落地路径(A'/B'/D' 模块改接方案),build session 直接消费

## K · 用户判准

**背景链(三句话)**:forge v1 裁掉人肉盲测二值签字 gate;v2 把 ①② 退役重绑 T021/T022 +
新前置 a1(单一谓词,生效条款 = 真 briefing rerun 自证 PASS)。D′ 真 rerun(hand-back 17)
跑通:**a1 机制内存层验证生效**(6/6 source_refs 真挂 TimeSlice · model_copy 往返保留,
不必再审 a1 对错);但真跑暴露结构盲区——**真跑 pipeline 无任何落盘产物能验 a1**(盲测面
故意不渲染 refs / 审计面不落盘 / audit.json 要 gate PASS 后才产),且「rerun 得 PASS/FAIL」
二值预设本身被推翻(gate 形态 operator 已否 + 无 CLI 判定入口 → 真跑走不到判定)= **第四次
「推演≠真跑」**。

**本次要裁两件事(一次裁清,不许拆开)**:

**A · gate 存废/形态**,四方向(承接 hand-back 11 operator 拒签三条批评 + injection 77a5176):
- (g1) 盲测二值签字维持 —— operator 已当面否,列出仅为完整性
- (g2) 留痕可审计验收 —— 产物 + 审计通道即验收,非二值签字
- (g3) 降为非阻断 smoke signal —— gate 保留但不挡解锁
- (g4) 信任整体移 O2/O7 使用期后验 —— 前置 gate 退役

**B · a1 产物可见性时机**:per-slice source 映射何时/如何对 operator/审计可见。现设计 =
post-gate 才产(audit_channel.py);但若 gate 去二值化改留痕可审计,**a1 产物正是留痕的
底料,可能反该始终可见**——非 post-gate 才产。gate 形态一变,可见性时机跟着变,两者必须
一次裁清。

**连带定实(裁决必须落地到)**:
- T010/T011 解锁条件最终形态:a1 生效条款「真 rerun 自证 PASS」在新 gate 形态下如何兑现
  ——若无二值 PASS,生效条款怎么改写,不许悬空。
- KG-B10「post-gate 产物绑 gate PASS」的**前提处置方向**(go / no-go / 改写方向):gate
  形态定了,给 KG-B10 一个明确方向;spine 子协议细节(不可伪造绑定机制)**留后续,本轮不深裁**
  (operator 拍板,防 KG-B7 过度投资)。

**我在乎**:
1. 验证范式贴 operator 真实工作流(边用边审计、留痕可回溯,不是停下来考试)——07-15 拒签
   三条批评是硬约束:① operator 非可靠打分器(单轮功效低)② 要留痕可审计不要盲测签字
   ③ 要边用边迭代不要前置一次性闸门
2. **第四次「推演≠真跑」后的铁律**:v3 产出的任何 gate 形态,必须附「用 07-17 真跑现有
   产物立即可验证」的自证步骤(真产物已在:worktree out/diffusion-models-20260717T051551Z.md
   + 密封 answer-key + 恢复后的签字模板),且必须回答「真跑如何走到判定/验收」——不许再交
   一个真跑走不到的形态
3. T010/T011 解锁条件必须落定,别再悬空一轮
4. 防 V4 精神保留(可复现失败必须 STOP + 回流),形态可变
5. a1 机制对错**不必再审**(内存层已实证);审的是它的产物可见性
6. 别过度投资(KG-B7 教训,T004-A1 十四轮硬化被推翻在先):裁决要最小化「先建再推翻」,
   倾向改接已建成的 A'/B'/D' 模块而非重写

**我不在乎**:v2 verdict 的面子(v3 触发条件被正当触发,这是机制在工作);gate/checker
代码沉没成本;盲测「考试感」保留与否(识伪已 retire-as-gate keep-as-calibration)。

## 收敛强度

✅ strong-converge

---

## Summary for reviewers

**审阅标的总数**: 17(8 本仓库文件/stage 文档 + 9 XenoDev worktree 文件)
**视角维度**: 架构设计 · 工程纪律 · 产品价值 · 用户体验
**参照系**: 对标 SOTA(v3 新方向:非二值留痕型验收 / 盲测密封 vs 审计可见性张力 / advisory-vs-hard gate 实证 / 生产期抽查替代前置 gate)
**预期产出**: verdict-only + decision-list + next-PRD + refactor-plan
**用户最在乎**: 第四次「推演≠真跑」后重裁 gate 存废/形态(g1-g4)+ a1 产物可见性时机,两者
一次裁清;T010/T011 解锁条款落定不悬空;新形态必须附 07-17 真跑现有产物立即可验证的自证
步骤;KG-B10 只裁前提方向;a1 对错不再审;倾向改接 A'/B'/D' 已建成模块。
**收敛模式**: strong-converge
