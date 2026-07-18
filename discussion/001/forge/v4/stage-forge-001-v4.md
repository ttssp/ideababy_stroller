# Forge Stage · 001 · v4 · "第五次『推演≠真跑』续裁:生效条款标的重裁 → 采 γ,以正式 amendment 落地"

**Generated**: 2026-07-18T08:40:00Z
**Source**: forge run v4 with X = 9 标的(4 本仓库文件/stage 文档 + 5 XenoDev worktree 文件), Y = 架构设计 · 工程纪律 · 产品价值, Z = 对标 SOTA(评估集污染卫生 / 生效条款绑首个真实 run / 预注册 vs 事后豁免), W = verdict-only + decision-list + next-PRD
**Convergence mode**: strong-converge
**Rounds completed**: P1 (both), P2 (both), P3R1 (both), P3R2 (both)
**Searches run**: 14 across ~14 distinct sources(Opus 3 · GPT 11;LLM benchmark 污染治理 decontamination 文献族 · scikit-learn data-leakage / Google MLCC train-test 分离 · progressive delivery(Argo Rollouts AnalysisRun 三态 / SLO-based gates)· 临床 protocol 治理(FDA waiver 明文禁止 / CONSORT / ClinicalTrials.gov amendment 留史))
**Moderator injections honored**: none(`forge/v4/moderator-notes.md` 不存在)
**Convergence outcome**: converged(双方 P3R2 §2 单一 verdict 逐点对齐,无 unresolved)

---

## How to read this

forge 是横切层(不是 L1-L4 pipeline 的一部分)。本文档是双专家(Opus 4.8 + GPT-5.5 xHigh)
审阅 + SOTA 对标 + 联合收敛后的产出,**强制给出立场**(不是候选菜单 defer 给你拍板)。

本次是 **v3 verdict 的续裁 · 议题极窄**,不是重开新议题。v3 裁定评估/校准分流 + 两层 + 机器自证,
生效条款写死「对 **07-17 真产物立即自证 PASS**」。XenoDev 落地四模块 A″/B″/C″/D″ 机制**全 DONE**
(354 passed · codex 9 轮 adversarial approve · round-2 真生产 bug 已修),但 **D″ 生效自证真跑
正确 fail-closed STOP**:07-17 真产物本体是 **pre-split 校准/盲测产物**(负控 slice-3 + 同 stem
answer-key),v3 自己引入的评估/校准分流禁止评估自证消费它 = **生效条款前提在真跑下不成立 =
第五次「推演≠真跑」**(前四:首跑 FAIL / operator 拒 gate 形态 / KG-B9 循环依赖 / D′ 真跑走不到
判定)。operator 已决 Option A(不硬改 · 不假 PASS)。触发源 = hand-back `001-radar-pA-20260717T092547Z`
(HANDBACK-LOG 第 19 条勾「起 forge v4 重裁生效条款标的」)。本次**只裁一件事:生效条款标的重裁**
(α 对评估 run 新产物 / β 07-17 特批豁免 / γ 条款改写「首个评估 run 产物落地即自证」)。故下文
§"Next-version PRD draft" 表述为 **PRD v1.5 → v1.6 的修订草案方向**(O4 生效条件段替换 + 07-17
处置 + Open questions #3 更新为主),不是全新 PRD——沿 v1/v2/v3 stage 文档先例。

读完后你应该:
- 知道双专家对 α/β/γ 三选项的最终裁决(采 γ · β cut · α 非独立选项)
- 知道支撑每条结论的具体证据(§"Evidence map" 可逐条溯源到 P1/P2/P3)
- 拿到按 W 形态准备好的可执行草案(3 列决策矩阵 + PRD v1.6 方向 · 均含真跑可执行兑现步骤)
- 能基于 §"Decision menu" 直接进入下一步行动(改 PRD v1.6 + 决议 + 下发 XenoDev / 跑 v5 / 局部接受 / park / abandon)

## Verdict

**采 γ,以正式 amendment(非 waiver)落地:生效自证标的从「07-17 真产物」改写为「首个评估 run
产物」。** 每个评估 run 产物落地后,在**同一验收事件内**以同 stem evidence bundle 跑 B′+D′ 自证;
**首个自证 PASS 的评估 run = 条款生效事件**,T010/T011 随之机器解锁;自证 FAIL → 机器道 STOP +
hand-back 回流(documented deviation),修复后下一评估 run 重试;未跑/未过维持 blocked
(**landed-not-yet-effective** 态,诚实且无 deadline,判据 B′+D′ 预定义)。**07-17 产物降为校准
活动历史样本**(exclusion 非豁免:不销毁、不豁免、不作 PASS 证据;answer-key 维持密封)。**β cut**
(ML eval hygiene 与 clinical protocol 治理跨域明文反模式)。**α 不作独立选项**,收编为条款执行 note:
operator 授权 + DEEPSEEK key 轮换完成后可即刻跑首个评估 run。护栏三道守卫 + 14 测 + KG-B10 冻结面
全 keep 零削弱;自证脚本做 S 级参数化泛化(禁新判据/旁路/spine)。XenoDev worktree 实装**即刻收编
commit**(机制 landed),与条款生效显式两态。(直接回应 K①「首个评估 run 不悬空」= runbook 序列
预注册进条款 + blocked 无 deadline 有判据;K②「解锁链闭合无旁路」= β cut + 不自证不解锁;K③
「护栏不拆」= β cut 首要理由 + 三守卫零削弱;K④「不新建机制」= 仅脚本 S 级参数化;K⑤「烧 key
与轮换时序」= 轮换写入 runbook 序列但不进机器谓词。)

## Evidence map

| 结论 | 来源 | 引用(≤15 words) | 是否有反对证据 |
|---|---|---|---|
| 07-17 产物三层校准身份证据,β 结构性不可行非仅不可取 | P1-Opus §1-A · P1-GPT §1-A | "三层校准身份证据:同 stem 标记 / 盲测正文 / 缺来源块" | - |
| β 在 ML eval 污染治理文献族零 grandfather 豁免先例 | P2-Opus §1 row1 · P2-GPT §1 row1 | "被污染样本不获豁免,只获移除或保留为非评估用途" | - |
| β 在临床 protocol 治理被明文禁止(waivers not permitted) | P2-Opus §1 row3 · P2-GPT §1 row3 | "Protocol waivers or exemptions are not permitted" | - |
| γ 的 blocked-until-verified 获 canary 正统背书(无 deadline 有判据) | P2-Opus §1 row2 · P2-GPT §1 row2 | "未通过验证的 release 诚实停在未晋级态,无 deadline" | - |
| γ 条款须写 FAIL 态与未发生态(非只 PASS 路径) | P2-GPT §1 row2 · P3R1-Opus §1 | "Argo AnalysisRun 三态:继续 / pause / abort" | - |
| v4 自身即 documented deviation → prospective amendment 的 SOTA 正路 | P2-Opus §3 新增视角 · P2-GPT §1 row3 | "STOP → hand-back → forge v4 → 改 PRD = 教科书走法" | - |
| 07-17 降校准历史样本 = exclusion 非豁免,不销毁不豁免 | P2-Opus §3 · P3R2 双方 §2 | "exclusion + documented deviation:降级 + 如实记录 pre-split 身份" | - |
| α 非独立选项,收编为 γ 的立即执行形态 | P1-Opus §2 · P1-GPT §2 · P3R2 双方 §2 | "SOTA 无仪式性验证 run 类别;验证一律绑真实工作负载" | ⚠ 双方 P1 独立同构(见 §underweights 回声室) |
| 同事件自证:同 stem 绑定 + 同一验收事件 + 失败即 blocked | P3R1-GPT 分歧1 · P3R2 双方 §1(分歧1) | "同 stem 绑定 + 同一验收事件内完成 + 失败即 blocked" | - |
| 收编即刻(机制 landed)与条款生效显式两态 | P3R1-Opus 分歧2 · P3R2 双方 §1(分歧2) | "landed-not-yet-effective:诚实的中间刻度" | - |
| key 轮换 = 授权前置/兑现步骤,不进机器 PASS 谓词 | P3R1-GPT 分歧4 · P3R2 双方 §1(分歧4) | "轮换→授权→run→自证是 runbook 序列;不污染谓词" | - |
| 自证脚本参数化 = S 级 runbook 泛化非新机制 | P3R1 双方 分歧3 · P3R2 双方 §1(分歧3) | "只复用现有 D″ 入口和守卫;禁新判据/旁路/spine" | ⚠ 参数化 S 级仍推演(见 §underweights) |
| 护栏三道守卫 + 14 测全 keep 零削弱 | P1-Opus §2-B · P1-GPT §1-B · K3 | "三道守卫是本轮最大资产;γ 不触任何守卫" | - |

## Intake recap

### X · 审阅标的(9 个)
- `discussion/001/forge/v3/stage-forge-001-v3.md`(stage 文档 · **v3 verdict 本体 = 被续裁标的**,生效条款所在)
- `discussion/001/handback/20260717T092547Z-...md`(本仓库文件 · **触发 v4 的 hand-back 19 · 第一因**,D″ STOP 证据链 + α/β/γ)
- `discussion/001/001-radar/001-radar-pA/PRD.md`(本仓库文件 · PRD v1.5 · O4 生效条款现行文本 = 要改写对象)
- `discussion/001/handback/HANDBACK-LOG.md`(本仓库文件 · 19 条决议史 SSOT · 五次「推演≠真跑」lineage)
- XenoDev worktree 5 件(⚠ `.claude/worktrees/001-radar-pA/` 副本,forge v3 实装尚未 commit,main checkout 无):
  `selfcheck_sequence.py`(D″ 自证序列 · 三道守卫 = 挡 β 的代码面)· `cli/reconstruct.py`(A″/C″ 分流)·
  `scripts/selfcheck-07-17.sh`(生效自证入口 = STOP 复现)· `out/reconstruct/diffusion-models-20260717T051551Z.md`
  (07-17 真产物 · 标的错配物证 · 同 stem answer-key 密封只指认不读)· `test_selfcheck_sequence_forge_v3.py`(离线 5 测全绿)

### Y · 审阅视角
- 架构设计 — 生效自证标的与评估/校准分流的一致性 · T010/T011 解锁链闭合 · 条款改写后拓扑自洽
- 工程纪律 — 「条款落定不悬空」· 新条款真跑可执行性 · 护栏不拆 · 烧 key 时序
- 产品价值 — γ 的「首个真评估 run 即自证」是否贴 operator「边用边迭代」真实工作流

### Z · 参照系
- mode: 对标 SOTA(v4 收窄方向;不重跑 v1/v2/v3 已做方向)
- 三检索方向:评估集污染卫生(train/test contamination · holdout 泄漏)/ 生效条款绑首个真实 run
  (canary/progressive delivery activation criteria)/ 预注册 vs 事后特批豁免(pre-registration / protocol amendment)
- 用户外部材料:无(K 内无额外链接;v4「外部材料」= hand-back 19 与 XenoDev worktree 真产物,P1 已消化)

### W · 产出形态
- verdict-only · decision-list · next-PRD(下方三章节均需出现;本次**无 refactor-plan**,与 v3 不同——机制已全 DONE 不重出改造方案)

### K · 用户判准
背景链:v3 裁评估/校准分流 + 两层 + 机器自证,生效条款写死「对 07-17 真产物立即自证 PASS」。XenoDev
落地四模块机制全 DONE(354 passed · codex 9 轮 approve · 有界 finding 全修),但 D″ 生效自证真跑**正确
fail-closed STOP**:07-17 产物是 pre-split 校准产物(负控 slice-3 + 同 stem answer-key),v3 分流禁止
评估自证消费它 = **第五次「推演≠真跑」**。operator 已决 Option A。本次**只裁一件事:生效条款标的重裁**
(α 对评估 run 新产物 / β 07-17 特批豁免 / γ 条款改写「首个评估 run 产物落地即自证」)。
**我在乎**:①第五次后铁律升级——新条款必须附真跑可执行兑现步骤;若 γ 必须回答「首个评估 run 何时/
如何/谁授权/烧不烧 key」,**不许把『首个评估 run』又变成悬空未来事件** ②条款落定不悬空:T010/T011
解锁链在新条款下闭合、无旁路 ③**护栏不拆**:codex 9 轮建成的守卫(校准 stem 拒消费 / 形状 allowlist /
fence-aware parser)是资产,裁决不得削弱 ④防过度投资(KG-B7):不新建机制,裁选项 + 条款改写文本方向
即可 ⑤烧 key 代价与 key 轮换 pending 的时序要显式裁进条款。
**我不在乎/不再审**:四模块机制对错(codex 9 轮已收敛)· a1 对错(内存层已实证)· KG-B10 spine
(维持冻结)· g1 复活(永久退役)· v3 verdict 的面子(v4 被正当触发是机制在工作)。

### 收敛模式
strong-converge(双方 P3R2 已 converged,无 unresolved)

---

## Verdict rationale(W · verdict-only)

本次裁决的核心不是「三选项哪个更优」,而是 **β 结构性不可行 + γ 与 SOTA 标准处置同构 + v4 自身即
SOTA 正路运行实例**——用四点论证:

- **07-17 产物三层校准身份证据使 β 结构性不可行,非仅不可取**。双方 P1 独立通读 07-17 产物本体后
  同向确认(P1-Opus §1-A · P1-GPT §1-A):标题含「位移重建(盲测)」、正文有盲测说明 + 阴性对照提示、
  slice 段全部缺评估面来源块,同 stem answer-key/runbinding 在 sibling 目录物理存在(指认未读)。守卫链
  是三道独立防线(`_reject_if_calibration_stem` / 正文 denylist / 形状 allowlist),STOP 不是单一守卫的
  偶然命中,是**产物身份的结构事实**。β 要放行它须同时穿过三道守卫——任何「豁免」实现要么加旁路 flag
  要么删守卫,都字面违反 K③「护栏不拆」。

- **污染治理 exclusion + 临床 protocol「waivers not permitted」的跨域合围**。两条独立成熟治理域给
  β 判死刑:ML benchmark 污染治理文献族的标准处置 = 识别并移出评估集,**无 grandfather 豁免先例**
  (P2-Opus §1 row1 · P2-GPT §1 row1);FDA/临床 protocol 治理明文「Protocol waivers or exemptions are
  not permitted」,变更两条正路是 prospective amendment(事前审批)或 documented deviation(事后如实
  记录,不追认合规)(P2-Opus §1 row3 · P2-GPT §1 row3 CONSORT/ClinicalTrials.gov)。β 在最成熟的
  预注册治理体系被明文禁止——不是权衡后放弃,是**跨域一致的反模式**,可干净关死。

- **γ 的 blocked-until-verified 是 canary 正统,不是治理逃避**。progressive delivery(Argo Rollouts
  AnalysisRun)的晋级语义正是「判据预定义、验证绑真实流量、未验证就停在未晋级态、没有 deadline 只有
  判据」(P2-Opus §1 row2 · P2-GPT §1 row2)。K① 点名的悬空担忧的正解**不是给 γ 加期限**,而是把判据
  与兑现步骤(runbook 级:轮换→授权→评估 run→同事件自证 · 判据 B′+D′ 预定义)预注册进条款——「预定义
  success criteria」恰是 canary 第一步。关键补件:AnalysisRun **有三态**(继续/pause/abort),γ 条款
  不能只写 PASS 路径,必须写 FAIL 态(STOP+回流+下次重试)与未发生态(landed-not-yet-effective)。

- **v4 自身即 documented deviation → prospective amendment 的 SOTA 正路运行实例**。07-17 STOP(deviation
  如实记录)→ hand-back 19(上报)→ forge v4(prospective amendment 审批)→ 改 PRD(批准后生效),这条
  链恰是治理教科书走法(P2-Opus §3 新增视角)。裁决措辞显式采「amendment 非 waiver」框架:γ 是对条款
  的**事前修订**,经治理通道批准后才执行,条款改写文本里预注册全部兑现步骤,任何再偏离都须再走
  deviation→amendment 循环——这让「不许悬空」有了程序语义。

## Decision matrix(W · decision-list)

> 议题极窄(只裁生效条款标的),故本矩阵聚焦条款/产物/脚本/状态四个具体面,不重列已 DONE 的四模块机制。
> 每行可在 §"Evidence map" 溯源。落地在 IDS 改 PRD + 决议,再下发 XenoDev(唯一 L4 build runtime)。

| 类别 | 项 | 来源(标的具体位置) | 理由 | 优先级 |
|---|---|---|---|---|
| **保留** | 三道 fail-closed 守卫(stem 拒消费 / 形状 allowlist / fence-aware parser) | `selfcheck_sequence.py` · K3 | codex 9 轮建成资产;γ 不触任何守卫;β cut 首要理由即护它 | P0 |
| **保留** | 14 测(5 主测 + 9 旁路回归)+ B′/D′ 谓词纯净性 | `test_selfcheck_sequence_forge_v3.py` · P3R2 双方 §1(分歧4) | key 轮换等操作性条件不混入机器 PASS 谓词 | P0 |
| **保留** | KG-B10 spine 面冻结 | K 不再审清单 · P3R2 双方 §2 | 维持冻结原文不改;γ 参数化禁碰 spine | P0 |
| **保留** | 双道 STOP(机器道 fail-closed + 治理道回流) | v3 verdict · P3R2 双方 §2 | 防 V4 精神不丢;本次 07-17 STOP→hand-back→v4 即治理道运转实证 | P0 |
| **保留** | 07-17 产物本体(降级不销毁) | K 连带定实 · P2-Opus §3 exclusion 语义 | exclusion 非销毁;保留为校准/识伪证据;answer-key 维持密封 | P0 |
| **调整** | O4 生效条款标的:07-17 真产物 → 首个评估 run 产物 | PRD v1.5 O4:73 · P3R2 双方 §2 | 标的错配是第五次「推演≠真跑」根因;改绑首个真实 run | P0 |
| **调整** | 07-17 身份:生效自证标的 → 校准活动历史样本 | K 连带定实 · P2 双方 §1 污染治理 exclusion | retire-as-gate keep-as-calibration 一致化;记 pre-split 身份 | P0 |
| **调整** | `selfcheck-07-17.sh`:硬编码 07-17 direction/ts → S 级参数化(direction/ts/briefing) | `scripts/selfcheck-07-17.sh` · P3R2 双方 §1(分歧3) | 泛化到任意评估 run;只复用现有入口/守卫;超 S 则回落手工模板 | P0 |
| **调整** | XenoDev worktree 状态:未 commit → 即刻收编 commit(命名「机制 landed」) | P3R2 双方 §1(分歧2) | 9 轮 review 成果不悬 working tree;与「条款生效」显式两态 | P0 |
| **删除** | β 路径(含任何 pre-split 豁免 flag / 绕守卫特批) | K 三选项 β · P2 双方 §1 | ML eval hygiene + clinical protocol 跨域明文反模式;零先例 | P0 |
| **删除** | α 作为独立条款选项 | P1 双方 §2 · P3R2 双方 §2 | SOTA 无仪式性验证 run 类别;收编为 γ 的立即执行形态 | P0 |
| **新增** | 「机制 landed」vs「条款生效」两态命名(landed-not-yet-effective 中间刻度) | P3R2 双方 §1(分歧2) | 给 γ 的 blocked 态诚实刻度;无 deadline 有判据 | P0 |
| **新增** | 条款内 runbook 序列(轮换 → operator 授权 → 首个评估 run → 同事件自证) | K5 · P3R2 双方 §1(分歧4) | 兑现步骤预注册;K① 不悬空的程序语义;key 状态不进谓词 | P0 |
| **新增** | 同事件自证措辞 + FAIL/未发生三态显式文本 | P3R1-GPT 分歧1 · P2 双方 §1 canary 三态 | 同 stem 绑定 + 同一验收事件 + 失败即 blocked;FAIL→STOP+回流+重试 | P0 |

## Next-version PRD draft(W · next-PRD)

> **注**:本次标的是 001-radar-pA 的生效条款**标的**重裁,**不是全新 PRD**。以下是 **PRD v1.5 → v1.6
> 的修订草案方向**(O4 生效条件段替换 + 07-17 处置 + Open questions #3 更新为主),供 operator 灌回
> PRD 时消费。PRD 是 L3 后 SSOT,修订须 operator 显式批准。v3 落地的评估/校准分流 + 两层 + 机器自证
> **本体不动**——只改「生效自证对准哪个产物」这一件。

```
# PRD 修订草案 · 001-radar-pA · v1.5 → v1.6

**Status**: Draft from forge v4, awaiting human approval(改 O4 生效条件段 + 07-17 处置一句 + Open questions #3)
**Sources**: forge stage-forge-001-v4.md · hand-back 20260717T092547Z(第 19 条)· SOTA(污染 exclusion / canary activation / protocol amendment)

## 改动点 1 · O4 生效条件段整段替换(标的:07-17 真产物 → 首个评估 run 产物)

- 废止 v1.5「生效条件(写死):上述谓词须对 07-17 真跑产物(diffusion-models-20260717T051551Z)
  立即可跑自证」(PRD v1.5 O4 第 73 行)——该标的是 pre-split 校准产物,评估/校准分流禁止评估自证
  消费它,真跑正确 STOP = 第五次「推演≠真跑」。
- 新生效条件(amendment · 非 waiver):
  ① **每个评估 run 产物落地后,在同一验收事件内**以同 stem evidence bundle(audit.json + briefing +
     D′ journal 记录)跑 B′+D′ 自证;自证前该产物不得作解锁凭据(不得先投入产品使用、自证无限期挂起)。
  ② **首个自证 PASS 的评估 run = 条款生效事件**,T010/T011 随之机器解锁。
  ③ 自证 **FAIL** → 机器道 STOP + hand-back 回流(documented deviation),修复后**下一评估 run 重试**
     (Argo abort→fix→new rollout 同构)。
  ④ **未跑/未过** → 维持 blocked = `landed-not-yet-effective` 态(诚实且**无 deadline**,判据 B′+D′
     预定义;不是悬空承诺——不跑评估 run 就永远不解锁,阻塞是自我施压的)。
- **条款内 runbook 兑现序列(预注册,防悬空)**:DEEPSEEK key 轮换 → operator 授权 → 首个默认评估 run
  (烧 key;自证序列本身不烧 key)→ 同一验收事件内跑同 stem 自证。**key 轮换是操作/授权前置,不进入
  B′/D′ 机器 PASS 谓词**(谓词保持纯净,不混操作性条件)。

## 改动点 2 · 07-17 产物处置(增补一句)

- 07-17 真产物(diffusion-models-20260717T051551Z)降为**校准活动历史样本**:exclusion 非豁免——
  不销毁、不豁免、不作 PASS 证据;answer-key/run-binding 维持密封记录;在决议 log / 脚本注记如实记录
  其 pre-split 身份。(与 v1「retire-as-gate keep-as-calibration」裁决一致化 · 污染治理 exclusion 背书。)

## 改动点 3 · Open questions #3 更新(记 v4 amendment lineage)

- 废止 v1.5「T010/T011 解锁 = B′+D′+journal 机器核验;自证对 07-17 产物立即可跑」中「对 07-17 产物」
  的标的表述。新表述:生效自证标的 = **首个评估 run 产物**(同 stem · 同一验收事件);07-17 降校准历史样本。
- 记 v4 amendment lineage:第五次「推演≠真跑」=生效条款标的错配;γ 经 forge v4 prospective amendment
  批准;任何再偏离须再走 deviation→amendment 循环。
- ⚠ 新落地前置警告(forge v4 §underweights):自证脚本参数化「S 级」+「同一验收事件靠 runbook 纪律未
  机器强制」仍是推演;首个评估 run 的**真跑自证**是本 amendment 的最后防线。

## Scope OUT(本次无需新增)
- v1.5 两条 non-goal(人肉签字参与解锁 · 评估 run post-gate 证据重生成)已覆盖;β cut 属既有
  「人肉签字/旁路」精神延伸,无需新列 non-goal。

## Success looks like(O4 相关补充,回应 K)
- 生效自证标的锚**首个真实评估 run**(operator 边用边迭代的自然副产物),不再交真跑走不到判定/
  标的错配的形态(K①)。
- 「首个评估 run」有预注册的 runbook 兑现序列 + blocked 无 deadline 有判据,不再是悬空未来事件(K①)。
- T010/T011 解锁链在新条款下闭合无旁路:不自证不解锁 · FAIL→STOP · β 已 cut(K②)。

## Open questions(forge 也没解决的,降级 v0.2 note)
- 「同一验收事件」的机器强制(现靠 runbook 纪律 + 同 stem 绑定;是否需产物落地 ts 与自证 ts 的最大
  间隔机器校验)—— 攒首批评估 run 实况后定,与 KG-B10 spine 同窗裁。
- 事件锚长期未发生的信号(若 30 天仍无评估 run,是否在 journal 记「未生效持续时长」)—— O2/O7 journal
  数据上来后定。
- 校准活动历史样本的独立标注 schema(现用决议 log + 脚本注记;校准 corpus 上量后再评估)。
```

---

## What this menu underweights(强制自批判)

- **回声室风险(与 v1/v2/v3 同型 · 本次连续第四次 · 高危)**:strong-converge 下**双方 P1 即独立
  同构**——γ+硬兑现 / β cut / α=γ 立即形态三点几乎零实质对抗(§"Evidence map" 标 ⚠ 的「α 非独立
  选项」正是此点)。这是双模型回声室强化的高风险信号,**与 v1(①② 退役)、v2(a1 前移)、v3(g1
  退役)同型**。诚实标注不是纯回声的实证:双方 P2 **检索方向重叠但源不重叠**——Opus 用 decontamination
  文献族 + FDA waiver 明文,GPT 用 scikit-learn/Google MLCC leakage + Argo AnalysisRun 三态 +
  CONSORT/ClinicalTrials.gov;源独立而结论一致,这比单源回声强。且互相修正在案:GPT P2 回声室自检
  产出唯一反向材料(protocol amendment 正当性条件 = 公开/留史/说明理由),反过来把 γ 定为「正式
  amendment 非口头换标的」;Opus 漏的 Argo 三态被 GPT 补入,直接改变了 γ 条款形态(必须写 FAIL/未
  发生态)。但**双方都同意且可能错**:整个 verdict 是双模型综合,不是真跑数据。

- **「同一验收事件」靠 runbook 纪律未机器强制**:verdict 用「同 stem 绑定 + 同一验收事件内完成 +
  失败即 blocked」措辞,但这是**流程纪律**而非机器约束——现无机器校验产物落地 ts 与自证 ts 的最大
  间隔。若 operator 把评估 run 产物先投入产品使用、自证隔日补(甚至无限期挂起),条款语义上违反但
  机器不拦。P3R2 双方已把此点降为 v0.2 note(攒首批评估 run 实况后定是否需 ts 间隔机器校验),但在
  首批真跑积累前,「同一验收事件」的执行完全靠 operator 自律——**这是把 v3 的坑换个位置埋的残余风险**
  (不是标的悬空,而是自证时机悬空)。

- **自证脚本参数化「S 级」仍是推演,未真跑验证**:verdict 把 `selfcheck-07-17.sh` 参数化定 S 级
  runbook 泛化,但这与 v1「机器可判三项秒级」、v2「a1 谓词 S-M 级」、v3「四模块 A″/B″/C″/D″ 全 S 级」
  同型——**前几次 S 级估计屡被真跑校准**(v3 四模块虽最终 DONE,但正是 D″ 真跑才暴露标的错配)。参数化
  牵动的 direction/ts/briefing 传参面若膨胀超 S,回落手工模板(零代码)是兜底,但「S 级」在新位置仍
  未真跑验证。**首个评估 run 的真跑自证是本 verdict 的最后防线**——这一次条款把自证从悬空标的改绑
  真实 run,正是吸取第五次教训,但真跑本身尚未发生。

- **烧 key 与 key 轮换 pending 的真实代价未完全定量**:verdict 把 key 轮换写入 runbook 序列(轮换→
  授权→run→自证),但 key 轮换自 hand-back 16 起三连 pending(见 MEMORY),DEEPSEEK key 泄露前科在册。
  「首个评估 run 烧 key」的实际执行**卡在 key 轮换先完成**——若轮换持续 pending,条款状态就诚实持续
  landed-not-yet-effective。这不是条款缺陷(blocked 态诚实),但意味着**生效时点实质由 key 轮换节奏
  决定**,而轮换节奏不在本 verdict 裁决范围内(后续若密钥治理通用化另走安全/SHARED-CONTRACT 层)。

- **Y 视角覆盖盲区**:Y 未含「安全」维度,但 07-17 产物的 answer-key 密封 + DEEPSEEK key 泄露前科都
  触及安全面。双方遵守红线未读密封 answer-key 内容,校准 run 泄露面对抗验证因此也无法在 forge 内完成
  (v3 §underweights 已列此项,v4 议题窄未重跑)。key 轮换的安全代价值得后续 attention,但不在本次
  裁决范围。

- **K 中未充分回应的关切**:K 全部关切均已显式覆盖(①不悬空 ✅ runbook 序列 + blocked 无 deadline /
  ②解锁链闭合 ✅ β cut + 不自证不解锁 + FAIL→STOP / ③护栏不拆 ✅ 三守卫零削弱 · β cut 首要理由 /
  ④不新建机制 ✅ 仅脚本 S 级参数化 · 禁新判据/旁路/spine / ⑤烧 key 与轮换时序 ✅ 写入 runbook 序列
  但不进谓词)。无遗漏项;残余风险已落到上面四条 underweight 与 v0.2 note。

- **X 标的覆盖局限**:X 含 XenoDev 5 件 worktree 副本(领先 main),refactor 边界基于 worktree 实况。
  残余局限:⚠ 5 件均 worktree 副本,forge v3 实装未 commit,main checkout 无——若 worktree 与最终
  merge 态偏离,脚本参数化边界须以 merge 后源码复核;answer-key 密封文件双方均未读(红线)。

- **forge versioning 提示(触发 v5 的条件)**:以下新信息进入会触发 v5 并可能改变本 verdict——
  ① 首个评估 run 真跑自证**再次 STOP**(新标的又有隐含前提不成立 · 第六次「推演≠真跑」);
  ② 自证脚本参数化真跑后发现**远超 S 级**(传参面膨胀成架构改);③ operator 长期不跑评估 run,条款
  永久停在 landed-not-yet-effective(事件锚僵尸化 · 「blocked until first use」演化成永远 blocked);
  ④ 「同一验收事件」纪律在真跑中被打破(产物先用后证 / 自证隔日补),暴露需机器强制 ts 间隔;⑤ key
  轮换持续 pending 导致条款无限期无法生效,需把 key 治理正式纳入议题。

自批判扫描后主要盲区 = **回声室(连续第四次 · 本次高危)+ 「同一验收事件」仅 runbook 纪律未机器强制
+ 参数化 S 级仍未真跑验证**。本 verdict 把「悬空风险」从标的错配(v3 的坑)平移到自证时机(runbook
纪律面),平移合治理逻辑且获 SOTA(canary/amendment)背书,但「不悬空」在新位置的机器强制仍是空的。
**首个评估 run 的真跑自证是最后防线**;forge 是双模型综合,不是真跑数据,真实数据仍可能推翻本 verdict
(这已是连续第五个议题由真跑打回推演的同一机制)。

## Decision menu(for human)

### [A] 接受 verdict → 改 PRD v1.6 + 决议入库 + 下发 XenoDev(本 idea 语境的「进 L4」)
```
⚠ 本标的是生效条款 amendment(不是新 PRD fork,也不是新 build——四模块机制已 DONE)——不走
   /plan-start,而是走「改 PRD v1.6 → HANDBACK-LOG 决议 entry → 下发 XenoDev(收编 commit + 脚本
   参数化 + 等首个评估 run)」的既有回流通道(沿 v1/v2/v3 先例)。
流程:
1. 把本 stage §"Next-version PRD draft" 的 O4 生效条件段替换 + 07-17 处置一句 + Open questions #3
   更新灌回 discussion/001/001-radar/001-radar-pA/PRD.md(v1.5 → v1.6),operator 显式批准。
2. 在 HANDBACK-LOG.md 追加对 hand-back 20260717T092547Z(第 19 条)的决议 entry
   (采 γ · amendment 非 waiver · 07-17 降校准历史样本 · β cut · α 非独立 · 同事件自证 · 机制 landed
   vs 条款生效两态 · key 轮换写入 runbook 序列不进谓词 · 脚本 S 级参数化)。
3. 通过 hand-back / outbox 通道下发 XenoDev(唯一 L4 build runtime):
   a. **即刻收编** forge v3 worktree 实装 commit(9 轮 review 成果 · 状态命名「机制 landed」);
   b. `selfcheck-07-17.sh` 做 S 级参数化(direction/ts/briefing · 只复用现有 D″ 入口/守卫 · 禁新判据/
      旁路/spine;超 S 回落手工模板);
   c. 完成 DEEPSEEK key 轮换 → operator 授权 → 跑首个默认评估 run → **同一验收事件内**跑同 stem 自证。
4. 首个自证 PASS = 条款生效事件 → T010/T011 机器解锁;FAIL → STOP + hand-back 回流 → 下一评估 run
   重试;未跑维持 landed-not-yet-effective(诚实无 deadline)。
⚠ 生效前提写死:B′+D′ 机器谓词须对**首个真实评估 run 产物**(非 07-17)在同一验收事件内成立
   (见 §underweights 回声室 + S 级预警 + 「同一验收事件」仅 runbook 纪律未机器强制——第五次「推演≠
   真跑」后,首个评估 run 的真跑自证是最后防线,key 轮换先完成是时序前置)。
```

### [B] 跑 forge v5(说明需要补什么)
```
/expert-forge 001
# Phase 0 intake 时调整 X / Y / Z / W / K;旧 v4 整目录保留作历史参考
```
适用:担心回声室(§underweights 已预警本次连续第四次高危)想引入更强对抗;或想把「同一验收事件机器
强制(ts 间隔校验)」纳入 forge 议题;或首个评估 run 真跑自证再次 STOP / 参数化远超 S 级 / 事件锚僵尸化
/ 同一验收事件纪律被打破 / key 轮换持续 pending 阻塞生效(见 §underweights v5 触发条件)。

### [C] 局部接受
- ✅ 采纳:采 γ(生效标的 07-17 → 首个评估 run 产物)· 07-17 降校准历史样本 · β cut · α 非独立选项 ·
  同事件自证(同 stem + 同一验收事件 + 失败即 blocked)· 机制 landed vs 条款生效两态 · key 轮换写入
  runbook 序列不进谓词 · 三守卫/14 测/KG-B10 冻结全 keep
- ⏸ 挂起:「同一验收事件」的机器强制(ts 间隔校验 · 攒首批评估 run 实况后定)· 自证脚本参数化真实
  代价(等 XenoDev 传参面实测后定死 S/超 S)· 事件锚长期未发生的 journal 信号(O2/O7 数据上来后定)·
  校准活动历史样本独立标注 schema(校准 corpus 上量后定)
- ❌ 拒绝:(无 — verdict 无明显应拒项;若拒「采 γ」则须在 α/β 间另选,但 β 跨域明文反模式、α 已被
  证是 γ 的立即形态,应改选 [B] 重裁)

### [P] Park
```
/park 001
```
保留所有 forge 产物,标记暂停。复活时不重做这一层。适用:operator 暂不推进 radar,生效条款治理挂起
(注:blocked 态本就诚实无 deadline,park 与 landed-not-yet-effective 可并存)。

### [Z] Abandon
```
/abandon 001
```
forge verdict 显示该 idea 不该继续做。归档 lesson 文档。**本 verdict 不指向 abandon**——它是「生效
条款对准哪个产物」的裁决,不是「要不要继续」;且真跑前置连续五次成功挡下推演/标的错配,证明机制在
正常工作。仅当 operator 独立判定 radar 整体不做时才选此项。

---

## Forge log
(由 /expert-forge 命令更新;记录每次 forge run 的 v 序列 + 关键 verdict 一句话)

- v4: 2026-07-18 — verdict: "采 γ,以正式 amendment(非 waiver)落地:生效自证标的从『07-17 真产物』改写为『首个评估 run 产物』;每个评估 run 产物落地后在同一验收事件内以同 stem evidence bundle 跑 B′+D′ 自证,首个自证 PASS 的评估 run = 条款生效事件,T010/T011 随之机器解锁,FAIL→STOP+hand-back 回流下次重试,未跑/未过维持 landed-not-yet-effective(无 deadline 有判据);07-17 降校准活动历史样本(exclusion 非豁免不销毁不豁免不作 PASS 证据);β cut(ML eval hygiene + clinical protocol 跨域明文反模式);α 非独立选项收编为 γ 立即执行形态;key 轮换写入条款内 runbook 序列(轮换→授权→run→同事件自证)但不进机器 PASS 谓词;三道守卫 + 14 测 + KG-B10 冻结全 keep 零削弱,自证脚本 S 级参数化(禁新判据/旁路/spine);XenoDev worktree 即刻收编 commit(机制 landed)与条款生效显式两态。第五次『推演≠真跑』=生效条款标的错配。"
- v3: 2026-07-17 — verdict: "g1(人肉盲测二值签字)永久退役出解锁链;新 gate 形态 = 按 run 类型分流 + 两层 + 信号。评估 run(默认):a1 per-slice source 映射生成时落盘始终可见(废止 post-gate ex-post 重生成),T010/T011 解锁 = B′ 结构谓词 + D′ 真 rerun 自证 + A1SelfCheckRecord journal 机器核验,preflight 消费对象一步换 evidence bundle 无双轨;校准 run(可选)只密封 answer-key 不密封证据通道、零解锁语义只入 journal;g3 折入 O2/O7 信号+escalation 不独立成层、g4 为叙事级信任主锚;生效条款 PASS=B′+D′ 机器谓词,自证对 07-17 真产物(diffusion-models-20260717T051551Z)立即可跑;KG-B10 收窄至校准面(密封完整性+自证防伪)方向受控 writer/密码学;防 V4 双道保留;hand-back 16『RERUN-PASS=spine 底座』被显式覆盖。"
- v2: 2026-07-16 — verdict: "①② 从 T010/T011 解锁前置退役(采纳 KG-B9 · 循环依赖成立),重绑 T021/T022 ship 验收 + O2/O7 使用期抽查;新解锁前置 = a1 per-slice source 映射最小前移(走 P0.1 amendment 通道不被 gate 挡)单一谓词同批解锁,生效条件写死『真 briefing rerun 自证 PASS』;解锁语义显式为一次性 stage-0 治理动作;KG-B4 wiring 改绑 a1 映射+③+治理记录;B7 冻结、双道 STOP 维持。"
- v1: 2026-07-16 — verdict: "P0.2 人肉盲测二值签字 gate 退役(采纳 KG-B8),T010/T011 改由机器可判三项(trace 完整/引用可达/审计通道就位)解锁;operator 移位为抽查者+journal 校准;FAIL→STOP 双道保留;B7 大部消解、B4 改写为新前置机器闭环。"
