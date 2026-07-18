---
forge_version: v4
created: 2026-07-17T17:10:00Z
convergence_mode: strong-converge
x_hash: 91d8e5078bca472cfb53bcdd7f58b004
prefill_source: v3-config+handback-19(proposal prefill 跳过 — v1 已实证 proposal §001 语境错位,v3 先例续用)
---

# Forge Config · 001 · v4

> **本次 forge 的真实标的**(v3 续裁 · 议题收窄):forge v3 落地四模块 A″/B″/C″/D″ 机制**全 DONE**
> (354 passed · codex 9 轮 adversarial approve · round-2 真生产 bug 已修),但 **D″ 生效自证真跑
> 正确 fail-closed STOP** —— v3 钦点的生效标的「07-17 真产物」本身是 **pre-split 校准/盲测产物**
> (负控 slice-3 + 同 stem answer-key),v3 自己引入的评估/校准分流禁止评估自证消费它 =
> **生效条款前提在真跑下不成立 = 第五次「推演≠真跑」**(前四:首跑 FAIL / operator 拒 gate 形态 /
> KG-B9 循环依赖 / D′ 真跑走不到判定)。operator 已决 Option A(不硬改 · 不假 PASS)。触发源 =
> hand-back `001-radar-pA-20260717T092547Z`(HANDBACK-LOG 第 19 条决议勾「起 forge v4 重裁
> 生效条款标的」)。v3 §underweights 四条监测项 ①-④ 均未命中,命中的是第五种:生效条款标的错配。

## X · 审阅标的

来源:v3 forge-config X 骨架收窄(去掉已消化项:v1/v2 stage 文档 / gate.py / unlock_preflight.py /
旧 hand-back 11·16·17)+ hand-back 19 新证据面(IDS 4 件 + XenoDev worktree 5 件)。
全部 9 件可达性已验证(2026-07-17)。
**⚠ XenoDev 侧 5 件均为 worktree 副本路径**(`.claude/worktrees/001-radar-pA/`,本批 forge v3
实装**尚未 commit**,只存在于 working tree;main checkout 无)。

### 解析后的标的清单

1. `discussion/001/forge/v3/stage-forge-001-v3.md`(类型:stage 文档 · **v3 verdict 本体 = 被续裁标的**,生效条款「对 07-17 真产物立即自证 PASS」所在 + v4 触发条件 + §underweights)
2. `discussion/001/handback/20260717T092547Z-001-radar-pA-20260717T092547Z.md`(类型:本仓库文件 · **触发 v4 的 hand-back 19 · 第一因**,D″ STOP 证据链 + α/β/γ 三选项 + codex 9 轮 adversarial 记录 + §4 v4 触发核心)
3. `discussion/001/001-radar/001-radar-pA/PRD.md`(类型:本仓库文件 · PRD v1.5,O4 生效条款现行文本 = 要改写的对象)
4. `discussion/001/handback/HANDBACK-LOG.md`(类型:本仓库文件 · 19 条决议史 SSOT,五次「推演≠真跑」lineage)
5. `/home/ys/codes/XenoDev/.claude/worktrees/001-radar-pA/projects/001-radar-pA/src/radar/credibility/selfcheck_sequence.py`(类型:外部 repo 文件 · ⚠ Codex 沙箱可能 BLOCK · D″ 自证序列实现本体,含 `_reject_if_calibration_stem` + `_require_eval_briefing_shape` 守卫 = **挡 β 的代码面**;inbox 任务内附关键摘录兜底,BLOCK 时用摘录不判 BLOCK)
6. `/home/ys/codes/XenoDev/.claude/worktrees/001-radar-pA/projects/001-radar-pA/src/radar/cli/reconstruct.py`(类型:外部 repo 文件 · ⚠ 同上 · A″/C″ 分流实现:评估 run 生成时落 audit + 校准 run 零解锁)
7. `/home/ys/codes/XenoDev/.claude/worktrees/001-radar-pA/scripts/selfcheck-07-17.sh`(类型:外部 repo 文件 · ⚠ 同上 · 生效自证 operator 手跑脚本 = STOP 的复现入口)
8. `/home/ys/codes/XenoDev/.claude/worktrees/001-radar-pA/projects/001-radar-pA/out/reconstruct/diffusion-models-20260717T051551Z.md`(类型:外部 repo 文件 · ⚠ 同上 · **07-17 真产物本体 = 标的错配的物证**(盲测 briefing,顶部有盲测说明);⚠⚠ 同 stem `_answer-key-*.json` + `*.runbinding.json` 在 `out/credibility/` **密封,双方只指认文件名不得读内容**)
9. `/home/ys/codes/XenoDev/.claude/worktrees/001-radar-pA/projects/001-radar-pA/tests/test_selfcheck_sequence_forge_v3.py`(类型:外部 repo 文件 · ⚠ 同上 · 离线序列 5 测全绿 = 机制可跑、争点只在标的的证据)

## Y · 审阅视角

✅ 架构设计 — 生效自证标的与评估/校准分流的一致性 · T010/T011 解锁链闭合 · 条款改写后拓扑自洽 — v4 核心议题层
✅ 工程纪律 — 「条款落定不悬空」· 新条款真跑可执行性(第五次「推演≠真跑」后的铁律)· 护栏不拆 · 烧 key 时序
✅ 产品价值 — γ 的「首个真评估 run 即自证」是否贴 operator「边用边迭代」真实工作流(07-15 拒签三条批评的延续判据)

## Z · 参照系

mode: 对标 SOTA(v4 收窄方向;**不重跑** v1 已做的 human-in-loop/盲测先例、v2 已做的
lineage-at-generation/staged-gating/bootstrap 循环依赖、v3 已做的非二值留痕验收/advisory-vs-hard
gate/生产期抽查方向)

**检索方向约束**(限定在 v4 议题层):
- 校准/盲测产物混作评估证据的卫生边界 = ML eval 的 train/test contamination / holdout 泄漏同构先例(评估集污染治理)
- 生效条款绑「首个真实 run」的先例(canary/progressive delivery 的 activation criteria · release qualification on first production run)
- 预注册评估协议 vs 事后特批豁免(pre-registration / protocol amendment 的治理先例;β 的「豁免=旁路」是否有正当化条件)

## W · 产出形态

✅ verdict-only — α/β/γ 核心裁决 + rationale
✅ decision-list — 生效条款改写 / 07-17 产物处置 / T010-T011 解锁兑现 / 烧 key 与轮换时序 逐条裁决(保留/调整/删除/新增)
✅ next-PRD — PRD v1.5 O4 生效条款改写文本方向(→ v1.6)

## K · 用户判准

**背景链(三句话)**:forge v3 裁定评估/校准分流 + 两层 + 机器自证,生效条款写死「对 07-17
真产物立即自证 PASS」。XenoDev 落地四模块机制全 DONE(354 passed · codex 9 轮 approve ·
有界 finding 全修),但 D″ 生效自证真跑**正确 fail-closed STOP**:07-17 真产物是 pre-split
校准产物(负控 slice-3 + 同 stem answer-key),v3 自己的分流禁止评估自证消费它 = **生效条款
前提在真跑下不成立 = 第五次「推演≠真跑」**。operator 已决 Option A(不硬改 · 不假 PASS)。

**本次只裁一件事:生效条款标的重裁**,三选项:
- **α**:生效自证改对**评估 run 新产物**跑(烧 DEEPSEEK key;偏离 v3「对 07-17 产物自证」钦点;key 轮换 pending 是时序前置)
- **β**:07-17 产物特批 pre-split 豁免一次性消费(= 旁路;违「条款落定不悬空」;codex round-1 #1 守卫正挡此路——采 β 即拆自己刚建的护栏)
- **γ**:条款改写「**首个评估 run 产物落地即自证**」;07-17 降为校准活动历史样本(XenoDev 倾向;与识伪 retire-as-gate keep-as-calibration 一致化)

**我在乎**:
1. **第五次后的铁律升级**:新条款必须附真跑可执行的兑现步骤——若 γ,必须回答「首个评估 run
   何时/如何发生、谁授权、烧不烧 key」,**不许把『首个评估 run』又变成悬空的未来事件**(那是把
   v3 的坑换个名字再挖一遍)
2. 条款落定不悬空:T010/T011 解锁链在新条款下闭合、无旁路
3. **护栏不拆**:codex 9 轮建成的守卫(校准 stem 拒消费 / 形状 allowlist / fence-aware parser)
   是资产,裁决不得要求削弱
4. 防过度投资(KG-B7):三选项都不新建机制,裁选项 + 条款改写文本方向即可
5. 烧 key 代价与 key 轮换 pending 的时序要显式裁进条款

**我不在乎/不再审**:四模块机制对错(codex 9 轮已收敛)· a1 对错(内存层已实证)· KG-B10
spine(维持冻结)· g1 复活(永久退役)· v3 verdict 的面子(v4 被正当触发是机制在工作)。

**连带定实(裁决必须落地到)**:
- PRD v1.5 O4 生效条款的改写文本方向(→ v1.6)
- 07-17 产物降级(若 γ)的记录方式(journal / 校准活动历史样本标注)
- XenoDev worktree 未 commit 实装的收编时序(裁决落地时一并)

## 收敛强度

✅ strong-converge

---

## Summary for reviewers

**审阅标的总数**: 9(4 本仓库文件/stage 文档 + 5 XenoDev worktree 文件)
**视角维度**: 架构设计 · 工程纪律 · 产品价值
**参照系**: 对标 SOTA(v4 收窄方向:评估集污染卫生 / 生效条款绑首个真实 run / 预注册 vs 事后豁免)
**预期产出**: verdict-only + decision-list + next-PRD
**用户最在乎**: 第五次「推演≠真跑」后重裁生效条款标的(α/β/γ · XenoDev 倾向 γ);新条款必须
附真跑可执行的兑现步骤,「首个评估 run」不许悬空;T010/T011 解锁链闭合;护栏不拆;不新建机制;
烧 key 与轮换时序显式裁进条款;四模块机制对错与 KG-B10 spine 不再审。
**收敛模式**: strong-converge
