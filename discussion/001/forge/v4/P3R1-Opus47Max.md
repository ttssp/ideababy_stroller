# Forge v4 · 001 · P3R1 · Opus47Max · 联合收敛 R1(标分歧)

**Timestamp**: 2026-07-18T06:40:00Z
**Visibility**: 我已读对方 P1 + P2。
**Searches in this round**: NONE(避免 R1 又开搜索发散)。

## 1. 整合摘要

四份 round file 收敛度极高,先诚实标注:**双方 P1 独立同构(γ+硬兑现 / β cut / α=γ 立即形态),
P2 检索方向重叠但源不重叠**(我:decontamination 文献族 + FDA waiver 明文;对方:scikit-learn/
Google MLCC leakage 定义 + Argo AnalysisRun 三态 + CONSORT/ClinicalTrials.gov 变更留史)——源独立
而结论一致,这比单源回声强,但仍是双模型综合,真跑仍可能推翻(001 lineage 五次先例在册)。

整合后的事实底座:07-17 产物三层校准身份证据(同 stem 标记 / 盲测正文 / 缺来源块),β 在两个
独立成熟治理域(ML eval hygiene / clinical protocol)均为明文反模式;γ 的 blocked-until-verified
获 canary 正统背书,但对方 P2 补了我漏的关键件:**Argo AnalysisRun 有三态(继续/pause/abort)**——
γ 条款不能只写 PASS 路径,必须写 FAIL 态与未发生态;对方 P2 回声室自检产出唯一反向材料
(amendment 正当性条件 = 公开、留史、说明理由)恰好反过来给 γ 定了程序形态:**正式 amendment,
非口头换标的**。

## 2. 我的初步 verdict(草案)

**采 γ,以正式 amendment 形态落地**:PRD v1.5 O4 生效条款改写(→v1.6)——生效自证标的从
「07-17 真产物」改为「**首个评估 run 产物**」;每次评估 run 产物落地即触发自证(B′+D′ 谓词,
判据不变);**首个自证 PASS 的评估 run = 条款生效事件**;自证 FAIL → 机器道 STOP + hand-back
(documented deviation),不解锁,修复后下一评估 run 重试(Argo abort→fix→new rollout 同构)。
07-17 产物降为校准活动历史样本(exclusion 非豁免,答案 key 维持密封)。**β cut**(跨域明文
反模式)。**α 不作独立选项**,收编为 γ 条款的执行 note:operator 授权 + key 轮换完成后可即刻跑
首个评估 run。**DEEPSEEK key 轮换写为首个评估 run 的条款内前置**(评估 run 烧 key;泄露前科
key 不再烧)。护栏三道守卫 + 14 测全 keep 零削弱。关键不确定点是「同事务自证」的实现边界
(分歧 1),若 R2 解决不了,条款语义与实现形态拆开表述。

## 3. 关键分歧清单

1. **同事务自证 vs 顺序两步**。我的立场:条款语义锚「产物落地即自证」,但实现允许 runbook 两步
   (跑评估 run → 立即跑自证脚本,自证绑定同 stem 产物),因为把自证 wire 进 run_reconstruct
   属新机制边缘,违 K 第 4 条;解锁完整性不受两步间隔影响(不自证就不解锁,无旁路)。对方立场
   (P2 §3):「首个评估 run 必须**同事务**自证;失败或未发生都不能解锁」。R2 期望收敛方向:
   条款写「落地即触发」语义 + 实现注明 runbook 两步可接受(同 stem 绑定即闭合),不 wire 进管线。
2. **XenoDev worktree 收编时序**。对方 P1 §3 提议「把收编 commit 与首次评估 run 自证绑定为同一
   验收包」;我的立场:**收编即刻、自证独立**——四模块机制已 codex 9 轮 approve,未 commit 状态
   本身是风险(working tree 丢失即丢 9 轮 review 成果),不该再 gate 在一个时间不定的评估 run 上;
   自证是条款生效事件,不是代码收编前提。R2 期望:对方确认或给出绑定的独立理由。
3. **(小)自证脚本参数化的定性**。selfcheck-07-17.sh 硬编码 07-17 的 direction/ts;γ 落地需要
   参数化(任意评估 run 的 direction/ts)。我定性为「脚本参数化 = S 级改接非新机制」,但这是
   K 第 4 条「不新建机制」的边界处,须对方 confirm 或挑战。

## 4. 与 K 的对齐性自检

- K1 真跑可执行兑现步骤,「首个评估 run」不悬空 → ✅ runbook 预注册进条款(轮换 key → 默认评估
  run → 同 stem 自证;判据 B′+D′ 预定义);blocked-until-verified 无 deadline 有判据,SOTA 正统。
- K2 T010/T011 解锁链闭合无旁路 → ✅ 不自证不解锁;RERUN-PASS 已退役;FAIL 态显式(STOP+回流)。
- K3 护栏不拆 → ✅ β cut 的首要理由即此;三道守卫 + 14 测零削弱;γ 不触任何守卫。
- K4 不新建机制 → ⚠ 诚实标注:γ 需 selfcheck 脚本参数化(S 级,分歧 3)+ PRD 条款文本改写;
  零新 schema、零新谓词、零新协议面。若 R2 判参数化超 S,回落为「按 07-17 脚本模板逐 run 手工
  复制改参」(零代码改,纯 operator 操作)。
- K5 烧 key 与轮换时序显式裁进条款 → ✅ 轮换 = 首个评估 run 的条款内前置(非并行 pending)。
- K 不再审清单(四模块机制/a1/KG-B10 spine/g1)→ ✅ 全部未触碰;KG-B10 维持冻结原文引用不改。
