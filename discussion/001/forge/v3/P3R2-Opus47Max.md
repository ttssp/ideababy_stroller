# Forge v3 · 001 · P3R2 · Opus47Max · 联合收敛 R2(finalize)

**Timestamp**: 2026-07-17T06:33:00Z
**Visibility**: 我已读对方 P3R1。
**Convergence mode**: strong-converge(从 forge-config 读)

## 1. 我对每条分歧的最终立场 + 让步

- **分歧 1(g3 地位)**:
  - 对方在 P3R1 给的论证:"g3 不进 v0.1 独立层;只有被 O2/O7 journal 读取并触发 escalation 才有意义" → **对方已让步至我方立场**,收敛完成。
  - 我的最终立场:两层 + 信号——叙事级非阻断信号折入 O2/O7 journal,带 escalation 到治理道;不设独立 g3 层。
  - 让步给对方的部分:采纳其「两层 + 信号」命名(比我方原「两层」表述更准确,信号显式在案不被吞掉)。
- **分歧 2(RERUN-PASS 字面处置)**:
  - 对方在 P3R1 给的论证:"退役代价中等可控…preflight 从查 PASS 改为查 digest/source_refs/run metadata" + 改接量 = 1 spec delta + 1 preflight delta + DAG 文案更新 → **接受其代价评估**。
  - 我的最终立场:RERUN-PASS **一步退役出解锁链**(preflight 消费对象直接换为 evidence bundle:audit.json + briefing + D' journal 记录;无「过渡期内 RERUN-PASS 仍可解锁」的双轨窗口);其**生成机制**随校准活动保留(gate 对答案仍产记录、零解锁语义入 journal,与 v1 识伪裁决一致化)。
  - 让步给对方的部分:接受「spine 过渡底座」表述**仅指校准活动内机制保留**这一读法;若对方原意含「过渡期仍具解锁语义」,该部分不让(双轨窗口 = 新旧两套解锁判据并存,违 K「条款落定不悬空」)。
- **分歧 3(校准 run VSA summary v0.1 建不建)**:
  - 对方在 P3R1 给的论证:最小 schema(run id / digest / source_refs 覆盖 / sealed key 指针 / review note / STOP 状态)→ **部分接受**。
  - 我的最终立场:v0.1 的 verification 记录**复用已建成的 A1SelfCheckRecord journal**(D' 产物,字段已覆盖 run_label/paths/checks/reason/independent_check),允许**字段级小改**(补 digest 与 sealed-key 指针,XenoDev 评估须 S 级);**不新建独立 VSA schema 文档**——K 第 6 条「改接已建成模块而非重写」。独立 summary 文档形态降 v0.2 note。
  - 让步给对方的部分:采纳「评估 run 透明;校准 run 只密封 answer-key,**不密封证据通道**」全句进联合 verdict;承认机器可验 verification 记录是 v0.1 必备(非 v0.2)。

## 2. 联合 verdict(单一)

**g1(人肉盲测二值签字)永久退役出解锁链;新 gate 形态 = 按 run 类型分流 + 两层 + 信号。**
(1) **评估 run(默认形态)**:a1 per-slice source 映射**生成时落盘、始终可见**——证据是管线副产物,废止评估用途的 post-gate ex-post 重生成(SOTA 反模式);T010/T011 解锁 = **B' 结构谓词(硬阻断)+ D' 真 rerun 自证(独立核验一致)**,全机器可验、人不在判定回路(SLSA attestation 同构);preflight 消费对象从 RERUN-PASS 文本换为 evidence bundle(audit.json + briefing + D' journal 记录),一步切换无双轨。叙事级信任全归 **O2/O7 使用期抽查 + 治理道**;非阻断信号折入 journal 带 escalation,不设独立 g3 层。(2) **校准 run(operator 自发起可选活动)**:保留盲测密封 + 负控注入 + answer-key,**只密封 answer-key,不密封证据通道**;产出零解锁语义、只入 journal(v1 识伪裁决一致化)。(3) **生效条款改写**:「真 briefing rerun 自证 PASS」的 PASS = B'+D' 机器谓词对真产物成立,无人肉判定;**自证步骤对 07-17 真跑产物(diffusion-models-20260717T051551Z)立即可跑**——用既有确定性 retrieval+切窗生成 audit.json(不烧 key、不要求 gate PASS 前置)→ 跑 B' 谓词 + D' 双路径核验入 journal。(4) **KG-B10 前提处置方向 = 收窄**:评估 run 无 post-gate 产物概念后,协议面只剩校准 run answer-key 密封完整性 + 自证记录防伪;解法方向 = 受控 writer / 密码学绑定(cosign 同构);spine 细节留后续,本轮不深裁。(5) **防 V4 双道保留**:机器道 = 结构谓词 fail-closed + 可复现失败自动 STOP;治理道 = prd-revision-trigger 回流。

无 unresolved。

## 3. 残余分歧降级为 v0.2 note

- **v0.2 note 1**:校准 run 独立 VSA summary 文档形态(v0.1 复用 A1SelfCheckRecord + 字段级小改;若校准活动上量、journal 记录不足以支撑复盘,再建独立 schema)。
- **v0.2 note 2**:叙事级 smoke 信号的自动化实现(哪些叙事特征可机器提示)——攒 O2/O7 journal 数据后定,v0.1 只留 escalation 规则一句话。
- **v0.2 note 3**:O2/O7 后验的自动 STOP(canary/Argo 同构、metric-driven)——治理道现为纯人工回流,使用量上来后评估是否补机器后验道。
- **v0.2 note 4**:RERUN-PASS 生成机制在校准活动内长期去留——按 XenoDev 改接实况定,不影响解锁链(已一步切换)。

## 4. W 形态产出的初步草稿建议

- **W 含 verdict-only** → 关键句:"g1 永久退役出解锁链;评估 run 证据生成时可见 + B'/D' 全机器自证解锁,校准 run 密封收窄到 answer-key;自证对 07-17 真产物立即可跑;KG-B10 收窄至校准面。"
- **W 含 decision-list** → 建议 rows(前 5):
  - 保留:B'/D' 谓词逻辑原样复用 · 双道 STOP · 校准活动的密封+负控+answer-key 机制 · fail-closed 纪律 · audit_channel 防伪 spine 面冻结(KG-B10 在册)
  - 调整:audit.json 产出时机(评估 run 生成时落盘)· preflight 消费对象(RERUN-PASS→evidence bundle)· D' 生效条款 PASS 语义(机器谓词)· KG-B10 范围(收窄校准面)· CLI 按 run 类型分流(校准显式 flag)
  - 删除:人肉签字-解锁耦合(彻底字面移除)· 评估 run 的 post-gate ex-post 重生成路径 · RERUN-PASS 作 preflight 消费对象 · 独立 g3 层
  - 新增:评估 run 生成时 audit 落盘 + human-readable 审计渲染面 · `--calibration` 分流 flag · 07-17 真产物立即自证序列 · journal 信号 escalation 规则(一句话级)
- **W 含 next-PRD** → 关键产品决策点:① O4 初始层重写:解锁 = B'+D' 机器自证(无签字无 RERUN-PASS),评估/校准分流,a1 产物始终可见条款;② Scope OUT 补:「人肉签字参与任何解锁判定」「评估 run 的 post-gate 证据重生成」;③ Open questions #3 更新:生效条款 PASS 语义改写。
- **W 含 refactor-plan** → 关键模块:A″(CLI 评估 run 生成时落 audit.json + 可见渲染面 · S)/ B″(preflight 消费对象换 evidence bundle · 去 gate-PASS 检查(评估 run)· S)/ D″(对 07-17 真产物跑通自证序列 + journal · S)/ C″(校准 run 分流 flag + 密封面维持 · S);显式冻结项:audit_channel 防伪 spine(等 KG-B10 后续)。
