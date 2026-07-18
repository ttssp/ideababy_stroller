# Forge v4 · 001 · P3R2 · Opus47Max · finalize(strong-converge)

**Timestamp**: 2026-07-18T07:45:00Z
**Visibility**: 我已读对方 P3R1。
**Convergence mode**: strong-converge

## 1. 我对每条分歧的最终立场 + 让步

- **分歧 1(同事务 vs 两步)· 收敛,双向让步**:采纳对方 R1 降级后的措辞——「**同 stem 绑定 +
  同一验收事件内完成 + 失败即 blocked**」。我放弃「两步间隔无约束」的宽松面(对方「不能隔日
  口头补证」是对的:自证与产物落地同属一个验收事件,operator 不得把产物先投入产品使用、自证
  无限期挂起);对方放弃代码级同事务(不 wire 进 `reconstruct`,防新机制)。条款语义:评估 run
  产物落地后,**在同一验收事件内**跑同 stem 自证;自证前该产物不得作解锁凭据。
- **分歧 2(收编时序)· 收敛,采对方让步后的拆分**:代码收编 commit **即刻**(9 轮 review 成果
  不悬 working tree);收编状态命名为「**机制 landed**」,与「**条款生效**」(首个评估 run 自证
  PASS)是两个显式区分的状态。我采纳对方的命名区分——这恰好给 γ 的 blocked 态一个诚实的中间
  刻度:landed-not-yet-effective。
- **分歧 3(参数化定性)· 收敛,无让步需要**:双方同判 S 级 runbook 泛化非新机制。共同边界写死:
  只复用 `run_selfcheck_sequence` 现有入口与三道守卫;**禁止**新增判据、旁路 flag、provider-proof
  spine(KG-B10 维持冻结)。若泛化实作中膨胀超 S → 回落为「按 07-17 脚本模板逐 run 手工复制改参」
  (零代码)。
- **分歧 4(key 轮换地位)· 收敛,采对方精确化**:轮换是**授权前置 / 兑现步骤**,写进条款的
  runbook 序列(轮换 → 授权 → 首个评估 run → 同事件自证),但**不进入机器 PASS 谓词**(B′+D′
  保持纯净,不混操作性条件)。我放弃「条款前置」的模糊表述,采对方「操作前置 + 不污染谓词」。

## 2. 联合 verdict(单一)

**采 γ,以正式 amendment(非 waiver)落地:生效自证标的从「07-17 真产物」改写为「首个评估 run
产物」。** PRD v1.5 O4 生效条件改写(→v1.6):① 每个评估 run 产物落地后,在**同一验收事件内**
以同 stem evidence bundle 跑 B′+D′ 自证;**首个自证 PASS 的评估 run = 条款生效事件**,T010/T011
随之机器解锁;自证 FAIL → 机器道 STOP + hand-back 回流,修复后下一评估 run 重试;未跑/未过则
维持 blocked(landed-not-yet-effective 态,诚实且无 deadline,判据预定义)。② 07-17 产物降为
**校准活动历史样本**(exclusion 非豁免:不销毁、不豁免、不作 PASS 证据;answer-key 维持密封)。
③ **β cut**(ML eval hygiene 与 clinical protocol 治理跨域明文反模式)。④ **α 不作独立选项**,
收编为条款执行 note:operator 授权 + DEEPSEEK key 轮换完成后可即刻跑首个评估 run(轮换→授权→
run→自证是条款内 runbook 序列;key 状态不进机器谓词)。⑤ 护栏三道守卫 + 14 测 + KG-B10 冻结面
全 keep 零削弱;自证脚本做 S 级参数化泛化(禁新判据/旁路/spine)。⑥ XenoDev worktree 实装
**即刻收编 commit**(机制 landed),与条款生效显式两态。无 unresolved。

## 3. 残余分歧降级为 v0.2 note

- 「同一验收事件」的机器强制(现靠 runbook 纪律 + 同 stem 绑定;是否需要产物落地 ts 与自证 ts
  的最大间隔机器校验)→ 攒首批评估 run 实况后定,与 KG-B10 spine 同窗裁。
- 首个评估 run 的方向选择是否需治理记录(operator 选自己真关心的方向即可,但若长期未发生,
  是否在 journal 记「未生效持续时长」信号)→ O2/O7 journal 数据上来后定。
- 校准活动历史样本的独立标注 schema(现用决议 log + 脚本注记;校准 corpus 上量后再评估)。

## 4. W 形态产出的初步草稿建议(逐项对应 forge-config.W)

- **verdict-only**:§2 原文可直接作 stage 文档 Verdict 段;rationale 四点:(a) 07-17 三层校准
  身份证据使 β 结构性不可行;(b) 污染治理 exclusion + protocol waiver 明文禁止的跨域合围;
  (c) canary blocked-until-verified 正统性(判据预定义、无 deadline);(d) v4 自身即 documented
  deviation → prospective amendment 的 SOTA 正路实例。
- **decision-list**:建议行——保留:三道守卫/14 测/B′+D′ 谓词纯净性/KG-B10 冻结/双道 STOP;
  调整:O4 生效条款标的(07-17→首个评估 run)/07-17 身份(生效标的→校准历史样本)/selfcheck
  脚本(硬编码→S 级参数化)/worktree 状态(未 commit→即刻收编 · landed 态命名);删除:β 路径
  (含任何豁免 flag)/α 作为独立条款;新增:landed-not-yet-effective 状态命名/条款内 runbook
  序列(轮换→授权→run→同事件自证)/FAIL 态显式文本(STOP+回流+下次重试)。
- **next-PRD**:v1.5→v1.6 改动点三处——O4 生效条件段整段替换(同事件自证 + 首个 PASS 生效 +
  FAIL 回流 + runbook 序列);O4 增补 07-17 处置一句(校准历史样本 · exclusion 非豁免);Open
  questions #3 更新(废止「对 07-17 产物立即自证」表述,记 v4 amendment lineage)。Scope OUT
  无需动(v1.5 两条已覆盖人肉签字与 post-gate 重生成,本次无新 non-goal)。
