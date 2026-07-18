# Forge v4 · 001 · P3R2 · GPT55xHigh · 联合收敛 R2(finalize)

**Timestamp**: 2026-07-18T08:16:04Z
**Visibility**: 我已读对方 P3R1。
**Convergence mode**: strong-converge

## 1. 我对每条分歧的最终立场 + 让步

- **分歧 1 · 同事务自证 vs runbook 两步**
  - 对方论证“实现允许 runbook 两步” → 让步。
  - 我的最终立场:条款语义写“产物落地即触发自证”,实现收敛为 **同 stem 绑定 + 同一验收事件内完成 + 失败即 blocked**;不 wire 进 `run_reconstruct`,避免新增机制。
  - 让步给对方的部分:放弃“必须代码级同事务”;保留“不能隔日口头补证”。

- **分歧 2 · XenoDev worktree 收编时序**
  - 对方论证“收编即刻、自证独立” → 让步。
  - 我的最终立场:即刻收编 9 轮 review 成果,但状态只叫 **机制 landed**;条款生效必须等首个评估 run 自证 PASS。
  - 让步给对方的部分:不把收编 commit 与首次评估 run 绑成同一验收包。

- **分歧 3 · 自证脚本参数化是否新机制**
  - 对方论证“脚本参数化 = S 级改接非新机制” → 接受。
  - 我的最终立场:允许最小参数化 direction/ts/briefing,或文档化命令模板;禁止新判据、旁路 flag、KG-B10 spine。
  - 让步给对方的部分:若参数化超 S,回落手工模板,不阻塞主 verdict。

- **分歧 4 · key 轮换的条款地位**
  - 对方论证“轮换 = 首个评估 run 的条款内前置” → 部分接受。
  - 我的最终立场:key 轮换写入兑现步骤:轮换 → operator 授权 → 首个默认评估 run → 同事件自证;但不进入 B′/D′ 机器 PASS 谓词。
  - 让步给对方的部分:从“并行 pending”上调为授权前置/兑现步骤。

## 2. 联合 verdict(单一)

**我和对方在 R2 后达成的单一 verdict**:采 **γ,以正式 amendment 形态落地,不是 waiver**。PRD v1.5 O4 的生效自证标的从“07-17 真产物”改为“首个默认评估 run 产物”;07-17 降为校准活动历史样本,不销毁、不豁免、不作 PASS 证据,answer-key/run-binding 维持密封记录。首个评估 run 产物落地后,按同 stem evidence bundle 在同一验收事件内跑 B′+D′ 自证;PASS 才让 T010/T011 生效,未发生/FAIL 则保持 blocked 并走 hand-back/documented deviation。β cut,因为它是 post-hoc waiver 且会拆护栏。α 不作独立选项,只作为 operator 完成 key 轮换与授权后立即执行 γ 的形态。K 的“真跑可执行”“不悬空”“护栏不拆”“不新建机制”“烧 key 与轮换时序”均由上述步骤承载;KG-B10 spine 继续冻结。

## 3. 残余分歧降级为 v0.2 note

- v0.2 note 1:事件锚可能长期未发生。只要 blocked 态诚实保留即可;若 30 天仍无评估 run,operator 可选择继续 blocked 或授权一次真实评估 run。
- v0.2 note 2:脚本参数化若牵动超过 S 级,立即回落手工模板,不扩展成 provider-proof 或新协议面。
- v0.2 note 3:key 轮换是操作安全前置,不是评估可信性谓词;后续若密钥治理通用化,另走安全/SHARED-CONTRACT 层。

## 4. W 形态产出的初步草稿建议

- W 含 verdict-only → 关键句:采 γ;07-17 降校准历史样本;首个默认评估 run 同 stem 自证 PASS 后生效;β cut;α 只是即时 γ。
- W 含 decision-list:
  - 保留:评估/校准分流;B′/D′ 谓词;三道 fail-closed 守卫;KG-B10 冻结;07-17 校准记录。
  - 调整:PRD O4 生效标的;selfcheck 脚本参数化/命令模板;key 轮换写入兑现步骤;XenoDev 收编状态命名。
  - 删除:07-17 作 PASS 标的;β waiver;任何绕过 stem/body/shape 守卫的特批。
  - 新增:机制 landed vs 条款生效两态;同 stem/同验收事件自证;FAIL→blocked+hand-back 处置。
- W 含 next-PRD:
  - O4 改写为正式 amendment,生效条件锚首个默认评估 run 产物。
  - 07-17 记录为 pre-split 校准历史样本,零解锁语义。
  - 兑现步骤写明 key 轮换、operator 授权、评估 run、自证 PASS/FAIL/未发生三态。
