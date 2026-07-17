# Forge Stage · 001 · v3 · "第四次『推演≠真跑』续裁:g1 永久退役 → 按 run 类型分流 + 两层 + 信号"

**Generated**: 2026-07-17T06:45:00Z
**Source**: forge run v3 with X = 17 标的(8 本仓库文件/stage 文档 + 9 XenoDev worktree 文件), Y = 架构设计 · 工程纪律 · 产品价值 · 用户体验, Z = 对标 SOTA(非二值留痕验收 / 盲测密封 vs 审计可见张力 / advisory-vs-hard gate / 生产期抽查替代前置 gate), W = verdict-only + decision-list + next-PRD + refactor-plan
**Convergence mode**: strong-converge
**Rounds completed**: P1 (both), P2 (both), P3R1 (both), P3R2 (both)
**Searches run**: 29 across ~30 distinct sources(Opus 5 · GPT 24;SLSA/Sigstore 部署门 · OSCAL/continuous-compliance「证据是管线副产物」· sealed-exam/HF public-private leaderboard 分流 · advisory-gate 划线(GitLab allow_failure/Buildkite soft_fail)· progressive delivery(Azure SDP/Argo Rollouts)· PyPI attestations · SLSA VSA)
**Moderator injections honored**: none(`forge/v3/moderator-notes.md` 不存在)
**Convergence outcome**: converged(双方 P3R2 §2 单一 verdict 逐点对齐,无 unresolved)

---

## How to read this

forge 是横切层(不是 L1-L4 pipeline 的一部分)。本文档是双专家(Opus 4.8 + GPT-5.5 xHigh)
审阅 + SOTA 对标 + 联合收敛后的产出,**强制给出立场**(不是候选菜单 defer 给你拍板)。

本次是 **v2 verdict 的续裁**,不是重开新议题。v2 把 ①② 退役重绑 T021/T022 + 使用期,新前置改成
a1 单一谓词,生效条款写死「真 briefing rerun 自证 PASS」。XenoDev 执行 D′ 真 rerun
(`deepseek-v4-flash` · exit 0),证明 **a1 机制内存层生效**(6/6 source_refs 真挂 TimeSlice ·
model_copy 往返保留),但暴露结构盲区——**真跑 pipeline 无任何落盘产物能验 a1**(盲测面故意不
渲染 refs / 审计面 render_markdown 不落盘 / audit.json 要 gate PASS 后才产),且「rerun 得
PASS/FAIL」二值预设本身被推翻(gate 形态 operator 2026-07-15 已当面否 + 无 CLI 判定入口 → 真跑
走不到判定)= **001 主线第四次「推演≠真跑」**(前三:首跑 FAIL / operator 拒 gate 形态 /
KG-B9 循环依赖)。触发源 = hand-back `001-radar-pA-20260717T052416Z`(HANDBACK-LOG 第 17 条勾
「起 forge v3 重裁 gate 形态」)。这是 v2 verdict 自定义 v3 触发条件的字面适用。故下文
§"Next-version PRD draft" 表述为 **PRD v1.4 → v1.5 修订草案方向**(O4 初始层 + Scope OUT +
Open questions #3 重写为主),不是全新 PRD——沿 v1/v2 stage 文档先例。

读完后你应该:
- 知道双专家对 gate 存废/形态四方向(g1-g4)+ a1 产物可见性时机的最终裁决(一次裁清)
- 知道支撑每条结论的具体证据(§"Evidence map" 可逐条溯源到 P1/P2/P3)
- 拿到按 W 形态准备好的可执行草案(4 列决策矩阵 + PRD v1.5 方向 + XenoDev 落地 refactor-plan)
- 能基于 §"Decision menu" 直接进入下一步行动(灌回 PRD / 跑 v4 / 局部接受 / park / abandon)

## Verdict

**g1(人肉盲测二值签字)永久退役出解锁链;新 gate 形态 = 按 run 类型分流 + 两层 + 信号。**
(1) **评估 run(默认)**:a1 per-slice source 映射**生成时落盘、始终可见**(证据是管线副产物,
废止评估用途的 post-gate ex-post 重生成);T010/T011 解锁 = **B′ 结构谓词(硬阻断)+ D′ 真 rerun
自证(独立核验一致)+ A1SelfCheckRecord journal 机器核验**,人不在判定回路;preflight 消费对象从
RERUN-PASS 文本一步换为 evidence bundle,无双轨过渡。(2) **校准 run(operator 自发起可选)**:保留
盲测密封 + 负控 + answer-key,**只密封 answer-key 不密封证据通道**,产出零解锁语义只入 journal。
g3 折入 O2/O7 journal 信号 + escalation 不设独立层;g4 = 叙事级信任主锚。生效条款 PASS = B′+D′
机器谓词对真产物成立,**自证步骤对 07-17 真跑产物(diffusion-models-20260717T051551Z)立即可跑**。
KG-B10 前提收窄至校准 run answer-key 密封完整性 + 自证记录防伪,spine 细节留后续。(直接回应
K「验证范式贴 operator 边用边审计」「新形态附真产物立即可验自证」「T010/T011 落定不悬空」。)

## Evidence map

| 结论 | 来源 | 引用(≤15 words) | 是否有反对证据 |
|---|---|---|---|
| 隐依赖环:a1 自证→B′→audit.json→gate PASS→被否盲测签字 | P1-Opus §1 架构 · P1-GPT §1 架构 | "能产 trace 的 audit.json 由 gate PASS 后才产" | - |
| 三条 a1 可见路径全被「保识伪难度」锁死 | P1-Opus §1 架构 | "盲测面不渲染 / render_markdown 不落盘 / audit.json post-gate" | - |
| 留痕验收 ≠ 去阻断;SOTA 硬门全机器验签、人不在判定回路 | P2-Opus §1 row1(SLSA/Sigstore) | "attestation 作硬性部署前置,人不在判定回路" | - |
| 证据应是管线副产物,post-gate 重生成是 SOTA 反模式 | P2-Opus §1 row2(OSCAL) | "evidence produced as byproduct rather than reconstructed ex-post" | - |
| 密封是活动属性非管线默认;评估透明/校准密封可分流并存 | P2-Opus §1 row3 · P2-GPT §1(HF leaderboard/VSA) | "密封只用于专门评测活动;日常靠透明 provenance" | - |
| 纯 g3 无 escalation 是已知失败模式(warning nobody reads) | P2-Opus §1 row4 · P3R1-GPT 分歧1 | "a warning nobody reads is not a gate" | - |
| g4 不是「无门」;生产期照样有机器判据自动 STOP | P2-Opus §1 row5(Argo/canary) | "canary 按 metrics 验证,不达标自动 halt/rollback" | - |
| g1 cut 不复活(维持 v1);盲测二值签字不作价值主锚 | P1-GPT §2 · P3R2 双方 §2 | "盲测二值签字与 operator 工作流冲突" | - |
| 解锁 = B′ 结构谓词 + D′ 自证 + journal,全机器可验 | P3R2-Opus §2(1) · P3R2-GPT §2 | "B'/D' 谓词逻辑原样复用,卡点只在输入时机" | ⚠ 「CLI 改接 S 级」仍推演(见 §underweights) |
| RERUN-PASS 一步退役、无双轨;hand-back 16「spine 底座」被覆盖 | P3R2-Opus §1.2 · P3R2-GPT §1.2 | "RERUN-PASS 一步退出解锁链,不设双轨过渡窗口" | ⚠ hand-back 16 曾定为 spine 底座,本 verdict 显式推翻 |
| v0.1 复用 A1SelfCheckRecord journal + 字段级小改,不新建 VSA | P3R2-Opus §1.3 · P3R2-GPT §1.3 | "复用已建成 journal,补 digest/sealed-key 指针" | ⚠ 独立 VSA summary 降 v0.2 note |
| 校准 run 只密封 answer-key 不密封证据通道 | P3R1-GPT 分歧3 · P3R2 双方 §2 | "评估 run 透明;校准 run 只密封 answer-key" | - |
| KG-B10 收窄至校准面(密封完整性+自证防伪),方向受控 writer/密码学 | P2-Opus §3 · P3R2 双方 §2(4) | "post-gate 产物概念只剩校准 run answer-key 两处" | - |
| 防 V4 双道保留:机器道 fail-closed STOP + 治理道回流 | P1-Opus §2 工程纪律 · P3R2-Opus §2(5) | "结构谓词 fail-closed + 可复现失败自动 STOP" | - |
| audit_channel 防伪 spine 面冻结(KG-B10 在册不当场修) | P1-Opus §2 工程纪律 | "KG-B10 两面诚实降级非安全边界,在册未越权修" | - |

## Intake recap

### X · 审阅标的(17 个)
- `discussion/001/forge/v2/stage-forge-001-v2.md`(stage 文档 · **v2 verdict 本体 = 被续裁标的**)
- `discussion/001/forge/v1/stage-forge-001-v1.md`(stage 文档 · v1 verdict · retire-as-gate keep-as-calibration 源头)
- `discussion/001/handback/20260717T052416Z-...md`(本仓库文件 · **触发 v3 的 hand-back 17 · 第一因**)
- `discussion/001/handback/20260717T032424Z-...md`(本仓库文件 · hand-back 16 · DAG 重绑 + KG-B10 codex critical 提级)
- `discussion/001/handback/20260715T093226Z-...md`(本仓库文件 · hand-back 11 · operator 形态拒签三条批评源头)
- `discussion/001/handback/HANDBACK-LOG.md`(本仓库文件 · 17 条决议史 SSOT)
- `discussion/001/001-radar/001-radar-pA/PRD.md`(本仓库文件 · PRD v1.4 · O4 现行解锁语义 = 被重裁对象)
- `discussion/001/001-radar/L3/moderator-notes.md`(本仓库文件 · injection 史:主锚移 O2+O7)
- XenoDev worktree 9 件(⚠ `.claude/worktrees/001-radar-pA/` 副本,领先 main 26+ commits):
  `dogfood-backlog.md`(KG-B9/B10/B11)· `followup-log.md`(FU-D-rerun-a1-verify-blindspot)·
  `dependency-graph.mmd`(a09d45b 后 DAG)· `gate.py`(被否形态本体)· `audit_channel.py`(post-gate 逻辑)·
  `unlock_preflight.py`(B′ 四件验)· `rerun_selfcheck.py`(D′ · KG-B10 另一面)·
  `out/reconstruct/diffusion-models-20260717T051551Z.md`(07-17 真跑盲测面 · answer-key 密封不读)·
  `verification/P0.2-...-diffusion-models.md`(被否签字模板)

### Y · 审阅视角
- 架构设计 — gate 形态 / a1 产物可见性时机 / audit_channel 拓扑 / T010-T011 解锁依赖
- 工程纪律 — 验收机制形态、防 V4 铁律、真跑自证步骤可执行性、A′/B′/D′ 模块改接代价
- 产品价值 — 验证范式贴 operator 真实工作流(边用边审计 vs 停下来考试)
- 用户体验 — 留痕可审计验收的 operator 操作面(审计产物怎么看、多久看一次、错误恢复)· v3 新增维度

### Z · 参照系
- mode: 对标 SOTA(v3 新方向;不重跑 v1 的 human-in-loop/盲测先例、v2 的 lineage-at-generation/staged-gating/bootstrap 方向)
- 四检索方向:非二值留痕型验收 / 盲测密封 vs 审计可见张力 / advisory-vs-hard gate 工业实证 / 生产期抽查替代前置 gate
- 用户外部材料:无(K 内无额外链接;v3「外部材料」= hand-back 17 与 XenoDev 真跑产物,P1 已消化)

### W · 产出形态
- verdict-only · decision-list · next-PRD · refactor-plan(下方四章节均需出现)

### K · 用户判准
背景:v1 裁掉人肉盲测二值签字 gate;v2 把 ①② 退役重绑 T021/T022 + 新前置 a1(生效条款 = 真
briefing rerun 自证 PASS)。D′ 真 rerun(hand-back 17)跑通:**a1 机制内存层验证生效**(6/6
source_refs 真挂 TimeSlice);但真跑暴露结构盲区——**真跑 pipeline 无任何落盘产物能验 a1**,且
「rerun 得 PASS/FAIL」二值预设本身被推翻 = **第四次「推演≠真跑」**。本次一次裁清两件:**A · gate
存废/形态四方向**(g1 盲测二值已被否 / g2 留痕可审计验收 / g3 非阻断 smoke / g4 移 O2/O7 后验)·
**B · a1 产物可见性时机**(现 post-gate 才产 vs 留痕底料该始终可见)。连带定实:T010/T011 解锁条件
最终形态(生效条款怎么改写不悬空)· KG-B10 前提处置方向(只裁 go/no-go/改写方向,spine 细节留后续)。
**我在乎**:①验证范式贴 operator 真实工作流(边用边审计、留痕可回溯,不是停下来考试;07-15 拒签
三条批评是硬约束)②第四次「推演≠真跑」后铁律:新 gate 形态必须附「用 07-17 真跑现有产物立即可
验证」的自证步骤 + 回答「真跑如何走到判定/验收」③T010/T011 落定别悬空 ④防 V4 精神保留(可复现
失败 STOP + 回流)形态可变 ⑤a1 机制对错不必再审(内存层已实证),审的是产物可见性 ⑥别过度投资
(KG-B7 教训),倾向改接已建成的 A′/B′/D′ 模块而非重写。**我不在乎**:v2 verdict 面子;gate/checker
代码沉没成本;盲测「考试感」保留与否(识伪已 retire-as-gate keep-as-calibration)。

### 收敛模式
strong-converge(双方 P3R2 已 converged,无 unresolved)

---

## Verdict rationale(W · verdict-only)

本次裁决的核心不是「gate 该不该存在」,而是 **v2 把 a1 的验证产物锁在被否形态的地基后面导致真跑
走不到判定**——用四点论证:

- **隐依赖环是结构事实,不是实现进度问题**。双方 P1 独立同向确认同一诊断:a1 生效自证(D′)需
  B′ 谓词、需 audit.json、需 gate PASS、需 operator 盲测二值签字 = **07-15 被当面否掉的那个形态**
  (P1-Opus §1 · P1-GPT §1)。三条 a1 可见路径(盲测面故意不渲染 refs / render_markdown 不落盘 /
  audit.json post-gate)全由「保识伪难度」一个设计动机锁死。RERUN-PASS 在 hand-back 16 被定为「spine
  底座」,实际是把被否形态从前门搬进地基,依然是唯一 driver——**真跑走不到判定不是 bug,是这条隐环
  的必然**。故 RERUN-PASS 必须一步退役出解锁链(不设双轨,否则违 K「条款落定不悬空」)。

- **留痕验收 ≠ 去阻断;SOTA 硬门全机器验签、人不在判定回路**。SLSA provenance + Sigstore 部署门
  (P2-Opus §1 row1)= attestation 作硬性部署前置,cosign 验签、admission webhook 拒无效产物——阻断
  但全自动,人不在判定回路。这直接给出「g2 是最小机器前置」的正统:**机器可验结构项 = 硬阻断;人判
  质量项 = 非阻断 + 使用期后验**(advisory-gate 划线判据 P2-Opus §1 row4)。于是 g2 与 g4 从「四选一」
  变成同一形态的两层。

- **证据生成时落盘是正解,post-gate 重生成是 SOTA 点名的反模式**。OSCAL/continuous-compliance 文献
  「evidence is produced as a byproduct of the pipeline rather than reconstructed ex-post」
  (P2-Opus §1 row2)——而 `generate_audit_channel_postgate` 字面就是 gate PASS 后重跑 retrieval+切窗
  的 ex-post 重建。B 议题方向明确:**评估 run 的 source 映射生成时落盘、始终可见**。PyPI attestations
  「留痕随产物出生」(P2-GPT §1)交叉验证同一方向。

- **密封是活动属性不是管线默认;评估透明 / 校准密封可分流并存**。sealed-exam 实践(SEAL/ARC-AGI/
  FrontierMath 私有题集)只用于专门评测活动(P2-Opus §1 row3);HF public/private leaderboard 分面 +
  SLSA VSA(P2-GPT §1)证明可见摘要与密封细节可并存。当前 CLI 把盲测密封当**唯一默认形态**(每次
  reconstruct 都产盲测面+answer-key+签字模板)是与 SOTA 的根本错位。故**校准 run 只密封 answer-key
  不密封证据通道**,产出零解锁语义只入 journal(与 v1 识伪裁决一致化);KG-B10 协议面因此收窄到校准
  面两处(密封完整性 + 自证记录防伪),「等 gate 形态定」的暂缓判断被再次验证。

## Decision matrix(W · decision-list)

| 类别 | 项 | 来源(标的具体位置) | 理由 | 优先级 |
|---|---|---|---|---|
| **保留** | B′/D′ 谓词逻辑原样复用 | `unlock_preflight.py` · `rerun_selfcheck.py` · P3R2 双方 §2 | 卡点只在输入产物时机,不在谓词本身;K 第 6 条改接非重写 | P0 |
| **保留** | 双道 STOP(机器道 fail-closed + 治理道回流) | v1/v2 verdict · P3R2-Opus §2(5) | 防 V4 精神不可丢;本次 forge 即治理道运转实证 | P0 |
| **保留** | 校准活动的密封 + 负控 + answer-key 机制 | v1 识伪裁决 · P3R2 双方 §2 | 密封是校准活动属性;retire-as-gate keep-as-calibration 一致化 | P0 |
| **保留** | fail-closed 纪律(read_audit_channel 严格结构校验等) | P1-Opus §2 工程纪律 · P1-GPT §2 | 空壳/sparse 陷阱都拒;结构缺失即 STOP,值得保留 | P0 |
| **保留** | audit_channel 防伪 spine 面**冻结**(KG-B10 在册) | P1-Opus §2 · P3R2-Opus §4 | 等 KG-B10 后续裁;第三次逼近 KG-B7 过度投资,须冻结 | P0 |
| **调整** | audit.json 产出时机 → 评估 run 生成时落盘 | `audit_channel.py`:198-257 · P2-Opus §1 row2 | post-gate ex-post 重生成是 SOTA 反模式;留痕应随产物出生 | P0 |
| **调整** | preflight 消费对象:RERUN-PASS 文本 → evidence bundle | `unlock_preflight.py` · P3R2 双方 §1.2 | audit.json + briefing + D′ journal 记录;一步切换无双轨 | P0 |
| **调整** | D′ 生效条款 PASS 语义 → 机器谓词(B′+D′) | PRD O4 v1.4 · P3R2-Opus §2(3) | 无二值 PASS 无人肉签字;PASS = 机器谓词对真产物成立 | P0 |
| **调整** | KG-B10 范围 → 收窄至校准面(密封完整性+自证防伪) | dogfood KG-B10 · P2-Opus §3 | 评估 run 无 post-gate 产物后协议面大幅缩小 | P0 |
| **调整** | CLI 按 run 类型分流(校准显式 flag) | P1-Opus §1 产品价值 · P3R2-Opus §4 | 现 CLI 默认走盲测三件套=误把校准当唯一形态 | P0 |
| **删除** | 人肉签字-解锁耦合(彻底字面移除) | hand-back 11 拒签 · P3R2 双方 §2 | g1 永久退役出解锁链;operator 非可靠打分器 | P0 |
| **删除** | 评估 run 的 post-gate ex-post 证据重生成路径 | `audit_channel.py` · P2-Opus §1 row2 | SOTA 点名反模式;评估用途改生成时落盘 | P0 |
| **删除** | RERUN-PASS 作 preflight 消费对象 | P3R2 双方 §1.2 | 一步退役;hand-back 16「spine 底座」定位被显式覆盖 | P0 |
| **删除** | 独立 g3 层(非阻断 smoke 单独成层) | P2-Opus §1 row4 · P3R2 双方 §1.1 | warning nobody reads;无独立消费者=噪音+过度投资 | P0 |
| **新增** | 评估 run 生成时 audit 落盘 + human-readable 审计渲染面 | P1-Opus §2 用户体验(new)· P1-GPT §2 | operator 审计操作面结构性缺失;a1 底料在而不可见 | P0 |
| **新增** | `--calibration` 分流 flag + 校准密封面维持 | P3R2-Opus §4 · P2-GPT §1(HF leaderboard) | 评估透明/校准密封分流的机器落点 | P0 |
| **新增** | 07-17 真产物立即自证序列(diffusion-models-20260717T051551Z) | K 第 2 条 · P3R2-Opus §2(3) | 第四次「推演≠真跑」后硬要求:真跑如何走到判定 | P0 |
| **新增** | journal 信号 escalation 规则(一句话级) | P2-Opus §1 row4 · P3R2-Opus §2(1) | g3 折入 O2/O7 journal 带 escalation,不独立成层 | P1 |

## Next-version PRD draft(W · next-PRD)

> **注**:本次标的是 001-radar-pA 的 gate 解锁与验收语义再改,**不是全新 PRD**。以下是 **PRD v1.4
> → v1.5 的修订草案方向**(O4 初始层 + Scope OUT + Open questions #3 重写为主),供 operator 灌回
> PRD 时消费。PRD 是 L3 后 SSOT,修订须 operator 显式批准。

```
# PRD 修订草案 · 001-radar-pA · v1.4 → v1.5

**Status**: Draft from forge v3, awaiting human approval(改 O4 初始层 + Open questions #3 + Scope OUT 补两条)
**Sources**: forge stage-forge-001-v3.md · hand-back 20260717T052416Z · KG-B10(收窄)

## 改动点 1 · O4 初始层解锁前置重写(分流 + 两层 + 机器自证)

- 「a1 生效条款 = 真 briefing rerun 自证 PASS」的 PASS 语义废止二值/人肉读法。新 T010/T011 解锁 =
  **评估 run 默认形态,全机器可验、人不在判定回路**:
  ① a1 per-slice source 映射生成时落盘、始终可见(证据是管线副产物)
  ② B′ 结构谓词(硬阻断)对真产物成立
  ③ D′ 真 rerun 自证(独立核验一致)入 A1SelfCheckRecord journal,机器核验通过
- **生效条件(写死)**:上述谓词须对 **07-17 真跑产物(diffusion-models-20260717T051551Z)立即可跑
  自证**——用既有确定性 retrieval+切窗生成 audit.json(不烧 key、不要求 gate PASS 前置)→ 跑 B′+D′
  双路径核验入 journal。(K 第 2 条:第四次「推演≠真跑」后铁律,必须回答真跑如何走到判定。)
- **run 类型分流(显式命名)**:评估 run(默认)透明留痕即解锁凭据;校准 run(operator `--calibration`
  自发起可选)保留盲测密封+负控+answer-key,**只密封 answer-key 不密封证据通道**,产出零解锁语义只入
  journal。叙事级信任主锚移 O2/O7 使用期抽查 + 治理道;非阻断信号折入 journal 带 escalation,不设独立层。

## 改动点 2 · Scope OUT 补两条(显式 non-goal)

- **人肉签字参与任何解锁判定**(evidence: operator 07-15 拒签三条批评 · SLSA 硬门人不在判定回路 · 见 §"Evidence map")
- **评估 run 的 post-gate 证据重生成**(evidence: OSCAL「证据应是管线副产物非 ex-post 重建」· 见 §"Evidence map")

## 改动点 3 · Open questions #3 再更新

废止「a1 生效条款 = 真 briefing rerun 得二值 PASS」的表述(v1.4 遗留)。新表述:T010/T011 解锁 =
B′ 结构谓词 + D′ 自证 + journal 机器核验(无签字无 RERUN-PASS);评估/校准分流;a1 产物评估 run 始终可见。

## Success looks like(O4 相关补充,回应 K)

- 解锁谓词能对 07-17 真跑现有产物立即机器自证,不再交真跑走不到判定的形态(K 第 2 条)
- operator 正常评估流中能直接看到 a1 留痕底料(human-readable 审计渲染面),不再藏在被否考试形态后面(K 第 1 条)

## Open questions(forge 也没解决的,降级 v0.2 note)
- 校准 run 独立 VSA summary 文档形态(v0.1 复用 A1SelfCheckRecord + 字段级小改;校准上量后再评估建独立 schema)
- 叙事级 smoke 信号的自动化实现(哪些叙事特征可机器提示)—— 攒 O2/O7 journal 数据后定
- O2/O7 后验的自动 STOP(canary/Argo 同构)—— 治理道现为纯人工回流,使用量上来后评估补机器后验道
- RERUN-PASS 生成机制在校准活动内长期去留 —— 按 XenoDev 改接实况定,不影响解锁链(已一步切换)
- KG-B10 绑定机制细节(受控 writer / digest 签名 / 密封 key 指针不可伪造)—— 只裁前提方向,细节留后续
```

## Refactor plan(W · refactor-plan · XenoDev 改 spec 时直接消费)

> 骨架 = 双方 P3R2 §4 草稿建议的**并集**;冲突处以双方 §1/§2 最终立场为准。代价 S/M/L 基于 §4 建议。
> 落地在 XenoDev(唯一 L4 build runtime);IDS 侧只改 PRD + 决议,不静默改代码(防 V4 · 跨仓边界)。
> **显式冻结**:audit_channel 防伪 spine 面(KG-B10 在册)本轮不动,等 KG-B10 后续裁。

#### 模块 A″ · CLI 评估 run 生成时落 audit.json + human-readable 审计渲染面
- **当前问题**:audit.json 由 `generate_audit_channel_postgate`(audit_channel.py:198-257)在 gate PASS
  后 ex-post 重生成;render_markdown(人读审计面)真跑不落盘;operator 正常评估流永远看不到 a1 底料
  (P1-Opus §1 产品价值/用户体验)。SOTA 点名 post-gate 重生成是反模式(P2-Opus §1 row2)。
- **目标态**:评估 run source 映射**生成时落盘、始终可见**(证据是管线副产物,不再 gate PASS 前置);
  新建最小 human-readable 审计渲染面(render_markdown 落盘或等价物),供 operator 抽查。
- **改造步骤**:1) 评估 run 路径下 audit.json 从生成时确定性 retrieval+切窗直接落盘(去 gate PASS 前置);
  2) render_markdown 评估 run 落盘;3) 逐面 grep 枚举 audit 消费面(preflight/序列化/渲染 · KG-36 教训)。
- **风险**:audit 生成时落盘改评估 run 时机,校准 run 密封面**不得受影响**(评估/校准分流须干净隔离,
  P1-Opus §3.1 不确定项:分流后校准 run 泄露面是否真收窄未做对抗验证)。
- **预估代价**:S

#### 模块 B″ · unlock_preflight 消费对象换 evidence bundle · 去 gate-PASS 检查(评估 run)
- **当前问题**:preflight 现查 RERUN-PASS 文本 / `_verify_gate_pass_artifact` 只信 caller 传入 PASS
  markdown(unlock_preflight.py · KG-B10 一面);评估 run 解锁被 gate PASS 前置卡住(隐依赖环)。
- **目标态**:preflight 消费对象一步换为 evidence bundle(audit.json + briefing + D′ journal 记录);
  评估 run 去 gate-PASS 检查;B′ 谓词逻辑原样复用(只换输入产物,不改谓词)。
- **改造步骤**:1) spec §5 + dependency-graph.mmd:T010/T011 前置文案改为 evidence bundle;2) preflight
  从查 PASS regex 改查 digest/source_refs/run metadata;3) 无双轨窗口——RERUN-PASS 一步退出消费链。
- **风险**:若 preflight 仍留 RERUN-PASS 旁路(双轨),违 K「条款落定不悬空」,须彻底字面移除。
- **预估代价**:S

#### 模块 C″ · 校准 run 分流 flag + 密封面维持
- **当前问题**:现 CLI 默认走盲测面+answer-key+签字模板三件套,把校准形态当唯一形态(P1-Opus §1 产品价值)。
- **目标态**:`--calibration` 分流 flag;校准 run 保留盲测密封+负控+answer-key,**只密封 answer-key
  不密封证据通道**;产出零解锁语义只入 journal(与 v1 识伪裁决一致化)。
- **改造步骤**:1) CLI 加 `--calibration` flag,默认评估 run;2) 校准 run 维持密封面 + answer-key 注入;
  3) 校准产出只入 journal,零解锁语义。
- **风险**:评估/校准分流后盲测面与审计面同 ts 命名是否留可 diff 旁路(P1-Opus §3.1 不确定项,须对抗审查)。
- **预估代价**:S

#### 模块 D″ · 对 07-17 真产物跑通自证序列 + A1SelfCheckRecord 字段级小改
- **当前问题**:D′ 真 rerun 证明内存层生效,但无落盘产物能验 a1;A1SelfCheckRecord journal 字段
  (run_label/paths/checks/reason/independent_check)不含 digest / sealed-key 指针。
- **目标态**:对 07-17 真跑产物(diffusion-models-20260717T051551Z)立即跑通自证序列——生成时 audit.json
  → B′ 谓词 → D′ 双路径核验入 journal;A1SelfCheckRecord 补 digest + sealed-key 指针(字段级小改 · 须 S 级)。
- **改造步骤**:1) 复用既有确定性 retrieval+切窗对 07-17 产物生成 audit.json(不烧 key、不要求 gate PASS);
  2) 跑 B′+D′ 核验入 journal;3) A1SelfCheckRecord 加两字段(digest/sealed-key 指针)。
- **风险**:字段级小改若牵动 journal 序列化/校验面则超 S 级 → 回头重排自证序列(P3R1-Opus §2 不确定项)。
- **预估代价**:S

---

## What this menu underweights(强制自批判)

- **回声室风险(与 v1/v2 同型 · 本次连续第三次 · 高危)**:strong-converge 下**双方 P1 即高度同构**
  ——四视角都指向「隐依赖环 → g1 退役 + 分流 + 生成时可见 + B′/D′ 机器自证」,几乎零实质对抗。这是
  双模型回声室强化的高风险信号,**与 v1(①② 退役)、v2(a1 前移)同型**。诚实标注互相修正的实证(说明
  不是纯回声):GPT P3R1 主张「三层公式」被自己收敛为「两层+信号」;Opus 原「两层」表述采纳 GPT「两层+
  信号」命名(信号显式在案不被吞掉)。但**双方都同意且可能错**:整个 verdict 是双模型综合,不是真跑数据,
  真实数据仍可能推翻(与 v1/v2 被真跑推翻同一机制)——已连续三个 v 都靠真跑打回推演。

- **「audit 生成时落盘改接 S 级」仍是推演未真跑**:§"Evidence map" 标 ⚠。verdict 把模块 A″/B″/D″
  全定 S 级,但这与 v1「机器可判三项秒级可跑」、v2「a1 谓词 S-M 级」同型——**那两个 S 级估计都被真跑
  推翻**。audit 生成时落盘牵动的消费面(preflight/序列化/渲染)未逐面 grep 枚举;A1SelfCheckRecord
  字段级小改若牵动序列化/校验面则超 S 级。**模块 D″ 的 07-17 真产物立即自证是最后防线**——这一次
  verdict 把自证从「建议」保持为「生效条件写死」,正是吸取前三次教训,但 S 级本身仍未真跑验证。

- **「按 run 类型分流后校准 run 泄露面收窄」的对抗验证未做**:P1-Opus §3.1 / P3R1-Opus 明确不确定——
  评估/校准分流后,负控泄露面是否真的只存在于校准 run?盲测面与审计面同 ts 命名(B′ ③ 命名一致检查)
  在分流后是否留可 diff 旁路?verdict 采「评估透明/校准密封」分流,但**这条对抗审查在 R1/R2 未被独立
  执行**——XenoDev 实装模块 C″ 时必须补分流泄露面的对抗验证,否则「密封收窄」可能是纸面收窄。

- **Y 含用户体验但 operator 审计操作面的具体形态仍空**:v3 新增 Y=用户体验维度,双方都判「需新建
  human-readable 审计留痕面」(P1-Opus/P1-GPT §2 都标 new),但**具体形态(审计产物怎么看、多久看
  一次、错误恢复)在 verdict 仍是方向级**——render_markdown 落盘只是载体,「抽查频率/条件」「错误
  恢复通道」PRD 仍只有 v0.2 open question。用户体验维度**被裁到了「该有一个面」但没裁到「面长什么样」**。

- **K 中未充分回应的关切**:K 全部关切均已显式覆盖(①边用边审计 ✅ 评估 run 生成时可见+O2/O7 后验 /
  ②真产物立即自证 ✅ 模块 D″ 对 07-17 产物 / ③T010/T011 落定 ✅ B′+D′+journal / ④防 V4 ✅ 双道不变 /
  ⑤a1 对错不再审 ✅ 只裁可见性 / ⑥别过度投资 ✅ 改接 A′/B′/D′ 非重写 · 独立 VSA 降 v0.2 · KG-B10 收窄)。
  无遗漏项;残余风险已落到上面四条 underweight 与 v0.2 note。

- **X 标的覆盖局限**:X 含 XenoDev 源码(audit_channel/unlock_preflight/rerun_selfcheck/gate/DAG/07-17
  真产物),refactor-plan 边界基于源码实况。残余局限:⚠ XenoDev 9 件均 worktree 副本(领先 main 26+
  commits),main checkout 无——若 worktree 与最终 merge 态有偏离,模块边界需以 merge 后源码复核;
  answer-key 密封文件双方均未读(红线),校准 run 泄露面对抗验证因此也无法在 forge 内完成。

- **forge versioning 提示(触发 v4 的条件)**:以下新信息进入会触发 v4 并可能改变本 verdict——
  ① 模块 A″/B″/D″ 真跑后发现改接**远超 S 级**(audit 生成时落盘/journal 字段小改膨胀成架构改 · 与
  v1/v2 S 级被推翻同型 · 第五次「推演≠真跑」);② XenoDev 补分流对抗验证发现**校准 run 泄露面未收窄**
  (评估/校准同 ts 命名留可 diff 旁路,「密封收窄」是纸面收窄);③ operator 使用 human-readable 审计面
  后发现**抽查范式失效**(留痕在但没人抽查 · 动机问题);④ KG-B10 收窄后校准面防伪仍被 codex 提级
  critical 且**方向不受控**(受控 writer/密码学绑定不足以兜住 answer-key 密封完整性)。

自批判扫描后主要盲区 = **回声室(连续第三次 · 本次高危)+ S 级改接仍未真跑验证 + 分流泄露面对抗
验证缺席**。本 verdict 把「机器可判性/改接代价」假设从 gate 边界(v1)、a1 边界(v2)进一步平移到
audit 落盘时机与 journal 字段(v3)——平移合拓扑,但「S 级」在新位置仍是推演。**模块 D″ 对 07-17
真产物立即自证是最后防线**;forge 是双模型综合,不是真跑数据,真实数据仍可能推翻本 verdict(这已是
连续第四个 v 由真跑打回推演的同一机制)。

## Decision menu(for human)

### [A] 接受 verdict → 灌回 PRD v1.5 + 派 XenoDev 落地(本 idea 语境的「进 L4」)
```
⚠ 本标的是已 ship build 的 gate 解锁与验收语义再改,不是新 PRD fork——不走 /plan-start 新建 branch,
   而是走「改 PRD → hand-back review 决议 → XenoDev 按新形态改 spec」的既有回流通道(沿 v1/v2 先例)。
流程:
1. 把本 stage §"Next-version PRD draft" 的 O4 初始层 + Scope OUT + Open questions #3 改动灌回
   discussion/001/001-radar/001-radar-pA/PRD.md(v1.4 → v1.5),operator 显式批准。
2. 在 HANDBACK-LOG.md 追加对 hand-back 20260717T052416Z 的决议 entry
   (g1 永久退役 + 分流+两层+信号 + B′/D′/journal 机器自证 + preflight 消费对象换 evidence bundle +
   KG-B10 收窄校准面 + 07-17 真产物立即自证)。
3. 通过 hand-back / outbox 通道把新形态 + §"Refactor plan" 四模块(A″/B″/C″/D″)下发 XenoDev
   (唯一 L4 build runtime);注明 audit_channel 防伪 spine 面冻结(KG-B10 后续裁)。
4. XenoDev 按新形态改 spec §5 + dependency-graph + 实装分流 + evidence bundle preflight
   (参 §"Refactor plan")。落地后**必须**对 07-17 真产物(diffusion-models-20260717T051551Z)跑通
   自证序列(模块 D″)——这是「真跑如何走到判定」的兑现,不许再交真跑走不到判定的形态。
⚠ 生效条件写死:B′+D′ 机器谓词须对 07-17 真产物立即可跑成立(见 §underweights 回声室 + S 级预警——
   连续第四次「推演≠真跑」,S 级改接本身仍未真跑验证,XenoDev 实装前须逐面 grep 枚举消费面)。
```

### [B] 跑 forge v4(说明需要补什么)
```
/expert-forge 001
# Phase 0 intake 时调整 X / Y / Z / W / K;旧 v3 整目录保留作历史参考
```
适用:担心回声室(§underweights 已预警本次连续第三次尤重)想引入更强对抗;或想把校准 run 泄露面
对抗验证纳入 forge 议题;或 XenoDev 实装后发现模块 A″/B″/D″ 远超 S 级 / 分流后校准泄露面未收窄 /
operator 使用审计面后抽查范式失效 / KG-B10 收窄后校准面防伪方向不受控(见 §underweights v4 触发条件)。

### [C] 局部接受
- ✅ 采纳:g1 永久退役出解锁链 · 评估 run 生成时可见 + B′/D′/journal 机器自证 · preflight 消费对象换
  evidence bundle(一步无双轨)· 校准 run 只密封 answer-key · g3 折入 O2/O7 信号 · KG-B10 收窄校准面 ·
  双道 STOP 维持 · audit_channel 防伪 spine 冻结
- ⏸ 挂起:模块 A″/B″/D″ 真实改接代价与消费面枚举(等 XenoDev 逐面 grep 后定死)· 校准 run 泄露面
  对抗验证(XenoDev 实装 C″ 时补)· human-readable 审计面具体形态(抽查频率/错误恢复 · 留 spec 层)·
  独立 VSA summary(降 v0.2 note)· KG-B10 spine 绑定机制细节(留后续)
- ❌ 拒绝:(无 — verdict 无明显应拒项;若拒「g1 退役」则整个 verdict 不成立,应改选 [B])

### [P] Park
```
/park 001
```
保留所有 forge 产物,标记暂停。复活时不重做这一层。适用:operator 暂不推进 radar,解锁语义治理挂起。

### [Z] Abandon
```
/abandon 001
```
forge verdict 显示该 idea 不该继续做。归档 lesson 文档。**本 verdict 不指向 abandon**——它是「怎么
继续」的裁决,不是「要不要继续」;且真跑前置连续四次成功挡下推演/过度投资,证明机制在正常工作。仅当
operator 独立判定 radar 整体不做时才选此项。

---

## Forge log
(由 /expert-forge 命令更新;记录每次 forge run 的 v 序列 + 关键 verdict 一句话)

- v3: 2026-07-17 — verdict: "g1(人肉盲测二值签字)永久退役出解锁链;新 gate 形态 = 按 run 类型分流 + 两层 + 信号。评估 run(默认):a1 per-slice source 映射生成时落盘始终可见(废止 post-gate ex-post 重生成),T010/T011 解锁 = B′ 结构谓词 + D′ 真 rerun 自证 + A1SelfCheckRecord journal 机器核验,preflight 消费对象一步换 evidence bundle 无双轨;校准 run(可选)只密封 answer-key 不密封证据通道、零解锁语义只入 journal;g3 折入 O2/O7 信号+escalation 不独立成层、g4 为叙事级信任主锚;生效条款 PASS=B′+D′ 机器谓词,自证对 07-17 真产物(diffusion-models-20260717T051551Z)立即可跑;KG-B10 收窄至校准面(密封完整性+自证防伪)方向受控 writer/密码学;防 V4 双道保留;hand-back 16『RERUN-PASS=spine 底座』被显式覆盖。"
- v2: 2026-07-16 — verdict: "①② 从 T010/T011 解锁前置退役(采纳 KG-B9 · 循环依赖成立),重绑 T021/T022 ship 验收 + O2/O7 使用期抽查;新解锁前置 = a1 per-slice source 映射最小前移(走 P0.1 amendment 通道不被 gate 挡)单一谓词同批解锁,生效条件写死『真 briefing rerun 自证 PASS』;解锁语义显式为一次性 stage-0 治理动作;KG-B4 wiring 改绑 a1 映射+③+治理记录;B7 冻结、双道 STOP 维持。"
- v1: 2026-07-16 — verdict: "P0.2 人肉盲测二值签字 gate 退役(采纳 KG-B8),T010/T011 改由机器可判三项(trace 完整/引用可达/审计通道就位)解锁;operator 移位为抽查者+journal 校准;FAIL→STOP 双道保留;B7 大部消解、B4 改写为新前置机器闭环。"
