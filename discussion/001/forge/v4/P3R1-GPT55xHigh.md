# Forge v4 · 001 · P3R1 · GPT55xHigh · 联合收敛 R1(标分歧)

**Timestamp**: 2026-07-18T07:31:05Z
**Visibility**: 我已读对方 P1 + P2。
**Searches in this round**: NONE。

## 1. 整合摘要

双方 P1/P2 的主线已高度对齐:07-17 产物是 pre-split 校准/盲测产物,不是 split 后评估 evidence bundle;β 作为 post-hoc waiver 应关死;γ 是主路径;α 只能作为 γ 的立即执行形态。对方 P2 用 contamination exclusion + protocol waiver forbidden 加强了这一点,我的 P2 用 data leakage hygiene + progressive delivery + protocol amendment 也得出同结论。

剩余问题不是“选不选 γ”,而是 γ 怎么写才不把 v3 的坑换个名字重挖。对方强调条款应锚事件语义,允许 runbook 两步,只要自证绑定同 stem 产物即可闭合;我 P2 写过“首个评估 run 必须同事务自证”。读完对方 P2 后,我认为“同事务”应降为“同 stem 绑定 + 同一验收事件内完成”,不必 wire 进生产 CLI,以免新增机制。

另一个实际分歧是 XenoDev worktree 收编。P1 时我担心收编 commit 与首次自证分离会放大风险;对方更看重 9 轮 review 成果不应悬在 working tree。我现在倾向让步:收编应先做,但不能宣称生效;自证仍作为独立生效门。

## 2. 我的初步 verdict(草案)

我倾向单一 verdict:采 γ,明确为 **amendment 非 waiver**。07-17 降为校准历史样本,不销毁、不豁免、不作 PASS 证据;β cut。首个默认评估 run 产物落地后,以同 stem evidence bundle 跑 B′+D′ 自证,通过才生效;未跑或未过则 T010/T011 保持 blocked。α 仅作为 operator 已授权且 key 轮换完成时的即时 γ,不是独立条款。

## 3. 关键分歧清单

- **分歧 1 · 同事务自证 vs runbook 两步**
  - 我的立场:同事务不必等于代码级同函数/同 CLI 事务,但必须是同一验收事件,绑定同 stem 评估产物,不能隔日口头补证。
  - 对方立场:"实现允许 runbook 两步"。
  - 我希望 R2 收敛:采用“同 stem + 同一验收事件 + 失败即 blocked”的措辞;不要求新 wire 进 `reconstruct`。

- **分歧 2 · XenoDev worktree 收编时序**
  - 我的立场:接受先收编 9 轮 review 成果,但收编状态只能叫机制 landed,不能叫条款生效。
  - 对方立场:"收编即刻"。
  - 我希望 R2 收敛:拆成两件事:代码收编可立即;生效自证独立等待首个评估 run。

- **分歧 3 · 自证脚本参数化是否新机制**
  - 我的立场:`selfcheck-07-17.sh` 硬编码 ts,γ 需要参数化方向/ts/briefing;这应算 S 级 runbook 泛化,不是新机制,前提是只复用现有 D″ 入口和守卫。
  - 对方立场:"γ 需参数化"。
  - 我希望 R2 收敛:允许最小参数化或文档化命令模板;禁止新增判据、旁路 flag、provider-proof spine。

- **分歧 4 · key 轮换的条款地位**
  - 我的立场:key 轮换不是 B′/D′ 谓词的一部分,但是真评估 run 授权前置;条款里应写为操作前置/风险注记。
  - 对方立场:"key 轮换该写成条款前置还是并行 pending"。
  - 我希望 R2 收敛:轮换→授权→首个评估 run→自证,作为兑现步骤;不把 key 状态混入机器 PASS 谓词。

## 4. 与 K 的对齐性自检

- K “新条款必须附真跑可执行的兑现步骤” → ✅ verdict 要求首个评估 run 产物 + 同 stem B′/D′ 自证 + blocked 失败态。
- K “不许把『首个评估 run』又变成悬空的未来事件” → ⚠ 事件锚仍可能长期未发生;缓解是未发生即不生效,并把 runbook/授权点预注册。
- K “T010/T011 解锁链闭合、无旁路” → ✅ β cut;未跑/未过保持 blocked;不允许特批 07-17。
- K “护栏不拆” → ✅ 三道 fail-closed 守卫全保留;参数化不得新增 bypass。
- K “防过度投资,不新建机制” → ✅ 不建 provider-proof spine,不把自证 wire 成新管线;只允许 runbook 级参数化。
- K “烧 key 与轮换时序显式裁进条款” → ✅ key 轮换作为真评估 run 授权前置,但不进入 PASS 谓词。
