# Forge v3 · 001 · P3R1 · Opus47Max · 联合收敛 R1(标分歧)

**Timestamp**: 2026-07-17T06:22:00Z
**Visibility**: 我已读对方 P1 + P2。
**Searches in this round**: NONE(避免 R1 又开搜索发散)。

## 1. 整合摘要

双方 P1 独立同向确认同一结构事实:**隐依赖环**——a1 生效自证(D')→ B' 谓词 → audit.json → gate PASS → operator 盲测二值签字(被否形态)。对方措辞「a1 的可审计产物仍被旧 post-gate 形态锁住」与我方「被否形态从前门搬进了地基」是同一诊断。双方 P2 检索互补且交叉验证:我方 5 searches(SLSA 部署门 / OSCAL「证据是管线副产物非 ex-post 重建」/ sealed-exam 分流 / advisory-gate 划线 / progressive delivery),对方 24 searches(PyPI attestations「留痕随产物出生」/ SLSA verifying-artifacts 与 **VSA**(验证摘要与密封细节并存)/ HF public-private leaderboard 分面 / GitLab allow_failure·Buildkite soft_fail / Azure SDP·Argo Rollouts)。两组证据零冲突,共同指向:① 留痕验收 ≠ 去阻断,SOTA 硬门全是机器验签、人不在判定回路;② 证据生成时落盘是正解,post-gate 重生成是反模式;③ 密封是活动属性不是管线默认属性(评估面透明 / 校准面密封可并存);④ 生产期信任主锚仍带机器判据的自动 STOP。

## 2. 我的初步 verdict(草案)

**gate 形态 = 「分流 + 两层」,人肉二值签字与 RERUN-PASS 从解锁链彻底移除**。(1) **评估 run(默认形态)**:a1 per-slice source 映射**生成时落盘、始终可见**(证据是管线副产物;评估 run 无负控,无密封需求);T010/T011 解锁 = **B' 结构谓词(硬阻断 · SLSA attestation 同构)+ D' 自证(独立核验一致)**,全机器可验,叙事级信任全移 O2/O7 使用期抽查 + 治理道(g2 作最小机器前置 + g4 作信任主锚)。(2) **校准 run(operator 自发起的可选活动)**:保留盲测密封 + answer-key + 负控注入,产出零解锁语义只入 journal(v1 已裁的一致化);密封需求收窄到此。**生效自证立即可跑**:对 07-17 真跑产物(`diffusion-models-20260717T051551Z`)用既有确定性 retrieval+切窗路径生成 audit.json(不烧 key、不再要求 gate PASS 前置),跑 B'+D' 双路径核验——满足 K「真跑如何走到判定」。KG-B10 前提方向 = **收窄**:评估 run 无 post-gate 产物概念后,协议面只剩校准 run 密封完整性 + 自证记录防伪,方向为受控 writer/密码学绑定,细节留后续。关键不确定:audit 生成时落盘的 CLI 改接是否真 S 级,若 R2 评估超 S 级需重排自证序列。

## 3. 关键分歧清单

- **分歧 1:g3 的地位——独立第三层 vs 折入使用期信号**
  - 我的立场:两层足够;叙事级非阻断告警**折入** O2/O7 的 journal 信号 + 治理道 escalation,不设独立 g3 层——「a warning nobody reads is not a gate」,独立告警层无消费者就是噪音 + 过度投资。
  - 对方立场(P2 §3):"v3 不应选纯 g2 或纯 g4,而应是 g2 最小前置 + g3 smoke signal + g4 使用期后验"(三层)。
  - 我希望 R2 怎么收敛:按「g3 产物有没有独立消费者」判——若 smoke 信号的消费者就是 journal/治理道,则 g3 是 g4 的输入信号非独立层(名字之争,实质同构);若对方主张独立 smoke 产物/独立告警通道,须给出消费者与 escalation 路径,否则并入。
- **分歧 2:RERUN-PASS artifact 的处置(对方未显式表态)**
  - 我的立场:退役出解锁链(preflight 不再内部消费它);其产出机制随校准活动保留或废止,由改接代价定。hand-back 16 刚把它定为「spine 底座」,本 verdict 要显式推翻该定位,不能含糊。
  - 对方立场:P2 row2 提「应拆成产物留痕可验与谁在何时采取动作两层」,方向兼容但未落到 RERUN-PASS 的字面处置。
  - 我希望 R2 怎么收敛:对方基于 preflight/spec §5 现状给出「去 RERUN-PASS 消费」的改接代价评估,R2 定死其字面去向。
- **分歧 3(minor):校准 run 的 verification summary(VSA 同构)v0.1 建不建**
  - 我的立场:不建,journal 记录足够(别过度投资)。对方 P2:"只输出可公开 verification summary"。R2 期望:降级为 v0.2 note。

## 4. 与 K 的对齐性自检

- K-A「gate 四方向一次裁清」→ ✅ g1 废(维持 v1)/ g2 采(最小机器前置)/ g3 折入信号(分歧 1 待 R2)/ g4 主锚;四方向全有显式落点。
- K-B「a1 可见性时机一次裁清」→ ✅ 分流:评估 run 生成时落盘始终可见;校准 run 密封。
- K「T010/T011 条款落定不悬空」→ ✅ 改写为 B'+D' 全机器自证;无二值 PASS、无人肉签字。
- K「新形态必须附 07-17 真产物立即可验证的自证步骤」→ ✅ §2 自证序列;⚠ 依赖「CLI 改接 S 级」假设,R2 须核。
- K「防 V4 STOP 保留」→ ✅ 机器道(结构谓词 fail-closed + 可复现失败)+ 治理道,双道不变。
- K「a1 对错不再审」→ ✅ 未审;只裁其产物可见性。
- K「KG-B10 只裁前提方向」→ ✅ 收窄 + 方向,未深裁 spine 细节。
- K「倾向改接 A'/B'/D' 非重写」→ ✅ B'/D' 谓词逻辑原样复用;A' 只改产出时机;audit_channel 防伪面冻结。
