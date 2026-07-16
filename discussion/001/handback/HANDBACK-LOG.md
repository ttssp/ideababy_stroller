---
doc_type: handback-decision-log
first_created: 2026-07-10T06:46:12Z
last_updated: 2026-07-16T13:35:18Z
total_decisions: 14
note: append-only;每条决议追加一段 ## entry;不删除 / 不修改既有 entry
---

# HANDBACK-LOG · discussion 001

per `framework/SHARED-CONTRACT.md` §6.4,本文件是 operator 在 IDS 端对 XenoDev hand-back 包的决议日志。append-only。

## 2026-07-10T05:55:46Z · 001-radar-pA-20260710T055546Z

**Reviewed at**: 2026-07-10T06:46:12Z
**Tags**: feature
**Severity**: low
**Operator decisions**:
- [ ] 修 PRD
- [ ] 修 SHARED-CONTRACT
- [ ] 修 XenoDev spec(本仓内,信息式)
- [x] 无操作(收悉)

**Operator note**: T001 ship 通知(interface-before-impl 地基,11 frozen models + 8 Protocols)。KG-B1 deferred → forge 006 v7 A1 落地后 re-fire。findings(F1 Judgment 高置信绕过 + model_copy 残留、F2 method/claim graph)均已在 XenoDev 侧闭环,teeth-proven。§2/§3 待补(gen-handback 未传 --section2/--section3,producer 侧摩擦点,XenoDev T007 amendment 已注记)。入 practice-stats。

**Follow-up commits**: pending

## 2026-07-10T06:34:36Z · 001-radar-pA-20260710T063436Z

**Reviewed at**: 2026-07-10T06:46:12Z
**Tags**: feature
**Severity**: medium
**Operator decisions**:
- [ ] 修 PRD
- [ ] 修 SHARED-CONTRACT
- [ ] 修 XenoDev spec(本仓内,信息式)
- [x] 无操作(收悉)

**Operator note**: T002 ship 通知(OpenAlex retriever,P0.1 检索骨架)。codex KG-38 hang → subagent fallback,5 findings 全闭(含真 API 集成抓到 sort 全史古董论文 real defect)。附带新框架缺口 KG-B2(parallel-builder baseline drift)/ KG-B3(.gitignore 吞 red-green-log TDD 证据)—— 已记 XenoDev dogfood-backlog,按铁律攒批走 forge 006,本包无当场动作。入 practice-stats。

**Follow-up commits**: pending

## 2026-07-10T06:34:38Z · 001-radar-pA-20260710T063438Z

**Reviewed at**: 2026-07-10T06:46:12Z
**Tags**: feature
**Severity**: medium
**Operator decisions**:
- [ ] 修 PRD
- [ ] 修 SHARED-CONTRACT
- [ ] 修 XenoDev spec(本仓内,信息式)
- [x] 无操作(收悉)

**Operator note**: T003 ship 通知(slice-reconstructor,P0.1 收尾 = T004 盲测门输入)。codex KG-38 hang(第 5 次)→ fallback;F1 RT-2 大小写泄漏已修,F2 negative_control 接口缝路由 task-decomposer(不私改 frozen 接口)、F3/F4 路由 T012 —— defer 链路清晰,XenoDev 侧闭环。入 practice-stats。

**Follow-up commits**: pending

## 2026-07-10T06:34:41Z · 001-radar-pA-20260710T063441Z

**Reviewed at**: 2026-07-10T06:46:12Z
**Tags**: feature
**Severity**: high
**Operator decisions**:
- [ ] 修 PRD
- [ ] 修 SHARED-CONTRACT
- [ ] 修 XenoDev spec(本仓内,信息式)
- [x] 无操作(收悉)

**Operator note**: T004 ship 通知(P0.2 轨迹可信度盲测门,全项目最承重 gate)。codex KG-38 hang(第 6 次)→ spine 级双 fallback(red-team + code-reviewer),F1(critical,seed 可反推)/F2/F3/F5/F7 全修 teeth-proven;双评审抓到单评审必漏的 F7(零真实切片空洞 PASS)。Deferred:F4 → T005 已补;F6 → KG-B4(gate STOP 未机器强制,框架缺口)走 dogfood-backlog → forge 006 攒批。gate 本体已修至可信,无 IDS 侧文档动作。入 practice-stats。

**Follow-up commits**: pending

## 2026-07-10T06:34:43Z · 001-radar-pA-20260710T063443Z

**Reviewed at**: 2026-07-10T06:46:12Z
**Tags**: feature
**Severity**: medium
**Operator decisions**:
- [ ] 修 PRD
- [ ] 修 SHARED-CONTRACT
- [ ] 修 XenoDev spec(本仓内,信息式)
- [x] 无操作(收悉)

**Operator note**: T005 ship 通知(DeepSeek LlmClient wire,补 T004-F4,盲测门 operator 可跑)。C8 双审计(security-auditor + code-reviewer)通过,key 零泄漏,F1-F3 全修。codex KG-38 hang 第 7 次(连续 4 task)—— KG-38 复发频率已系统化,属 forge 006 v7 review gate 状态机范围,等 XenoDev check-6 落地。下一步是 operator 亲跑盲测 sign-off(export DEEPSEEK_API_KEY → reconstruct → evaluate_gate),非文档动作。入 practice-stats。

**Follow-up commits**: pending

## 2026-07-11T13:53:03Z · 001-radar-pA-20260711T135303Z

**Reviewed at**: 2026-07-11T14:04:49Z
**Tags**: prd-revision-trigger
**Severity**: high
**Operator decisions**:
- [x] 修 PRD(→ v1.1)
- [ ] 修 SHARED-CONTRACT
- [ ] 修 XenoDev spec(本仓内,信息式)
- [ ] 无操作(收悉)

**Operator note**: P0.2 盲测门首次真判 FAIL(diffusion models · 封闭历史窗 2021→2023)。接受 trigger。三要件:①slice-2/3 可信 ②识伪精准命中 slice-1(反橡皮图章机制有牙)③新洞察为空 → FAIL 原因 = pipeline 当前配置只产领域常识综述。STOP 生效,T010/T011 未起,T002-A1 ship 留后 —— 边界纪律全部守住。

v1.1 优先方向(operator 定):
- **A1 要件③重 operationalize**:「新洞察」改为可达目标(如新证据链组合),长期主锚按 injection 移 O2(三跳回溯)+ O7(使用中偏差反馈)
- **A2 语义切窗上调**:T012 按语义/事件切窗替代按数量切(本次 slice-2/3 挤 2023 半年粒度稀释信息密度)
- **A3 分层阅读原则**:v1.1 全量喂 abstract(新洞察的物质基础,成本可忽略);全文不做全量 —— 仅对「位移锚点论文」或 O2 证据链回溯核验时选择性深读(operator 提出的分层阅读架构,与「结论可回溯」哲学咬合)
- 细节取舍留给 v1.1 修订过程论证(injection 已要求下轮以「## Moderator injection response」回应)

gate 语义确认(§3-B):维持「FAIL → prd-revision-trigger STOP」铁律;PASS = smoke test 过,非终审发证(KG-B4 按此语义设计)。

**Follow-up commits**: a3a5f57(决议入库)· 6024159(PRD v1.0→v1.1 落地)

## 2026-07-12T02:13:20Z · 001-radar-pA-20260712T021320Z

**Reviewed at**: 2026-07-13T09:54:36Z
**Tags**: feature
**Severity**: low
**Operator decisions**:
- [ ] 修 PRD
- [ ] 修 SHARED-CONTRACT
- [ ] 修 XenoDev spec(本仓内,信息式)
- [x] 无操作(收悉)

**Operator note**: T002-A1 ship(封闭历史窗 --from/--to-date,v1.1 hand-off 解除留后后走完 review→ship)。codex approve 0 findings,默认近期窗字节级回归守卫。§2/§3 已填(--section2/--section3 修复生效)。入 practice-stats。

**Follow-up commits**: pending

## 2026-07-12T07:26:00Z · 001-radar-pA-20260712T072600Z

**Reviewed at**: 2026-07-13T09:54:36Z
**Tags**: feature
**Severity**: medium
**Operator decisions**:
- [ ] 修 PRD
- [ ] 修 SHARED-CONTRACT
- [ ] 修 XenoDev spec(本仓内,信息式)
- [x] 无操作(收悉)

**Operator note**: T003-A1 ship(语义切窗 = PRD v1.1 A2,P0.2 首跑 FAIL 根因收口)。gap-based significance-gated 切窗,切片数自适应;codex adversarial 4 轮 3 real findings 全闭 → approve。入 practice-stats。

**Follow-up commits**: pending

## 2026-07-12T21:37:22Z · 001-radar-pA-20260712T213722Z

**Reviewed at**: 2026-07-13T09:54:36Z
**Tags**: feature
**Severity**: medium
**Operator decisions**:
- [ ] 修 PRD
- [ ] 修 SHARED-CONTRACT
- [ ] 修 XenoDev spec(本仓内,信息式)
- [x] 无操作(收悉)

**Operator note**: T003-A2 ship(abstract 输入 = PRD v1.1 A3 分层阅读)。prompt-injection 防御 codex 10 轮收口(decode→NFKC→allowlist→json)。**KG-B5** 架构级 followup(string 消毒不可证完备,真根治 = LlmClient system/user role 分离 = 动 T001 冻结接口)——XenoDev 守铁律未当场改,已记 dogfood-backlog 攒批走 forge 006;v0.1 自用风险可控。入 practice-stats。

**Follow-up commits**: pending

## 2026-07-13T06:09:50Z · 001-radar-pA-20260713T060950Z

**Reviewed at**: 2026-07-13T09:54:36Z
**Tags**: feature
**Severity**: high
**Operator decisions**:
- [ ] 修 PRD
- [ ] 修 SHARED-CONTRACT
- [ ] 修 XenoDev spec(本仓内,信息式)
- [x] 无操作(收悉)

**Operator note**: T004-A1 ship(要件③ operationalize = PRD v1.1 A1,gate spine)。new_evidence_chain schema(type/statement/o2_traceable_ref)与 PRD v1.1「新证据链」定义精确对齐;RERUN-PASS artifact 为 T010/T011 唯一前置;codex adversarial 14 轮轮轮真 finding(2 critical:run-binding 防 replay、FAIL reason 防 oracle)。**KG-B7** followup(trial-error/replay 泄露族系统性根治 = 框架层单次执行强制,同 KG-B4 族)→ dogfood-backlog 走 forge。**gate 现可 operator 重跑 P0.2**(换方向/换窗多轮)。入 practice-stats。

**Follow-up commits**: pending

## 2026-07-15T09:32:26Z · 001-radar-pA-20260715T093226Z

**Reviewed at**: 2026-07-15T10:25:36Z
**Tags**: prd-revision-trigger
**Severity**: high
**Operator decisions**:
- [ ] 修 PRD
- [ ] 修 SHARED-CONTRACT
- [ ] 修 XenoDev spec(本仓内,信息式)
- [ ] 无操作(收悉)
- [x] 起 forge 同簇审(/expert-forge 001 · KG-B8 gate 形态 + KG-B4/B7 同簇)

**Operator note**: P0.2 盲测 gate **形态本身**被 operator 真跑拒签(填①②、拒③),升级为治理层质疑——非首跑那种能力层 FAIL。operator 三条批评:①operator 非可靠打分器(单轮统计功效低)②应留痕可审计而非盲测签字 ③应边用边迭代而非前置一次性闸门。与 injection 77a5176(主锚移 O2+O7)同向且更进一步。决议走 §3.C 路线:**不直接改 PRD**,起 forge 把 KG-B8(gate 形态该不该存在)+ KG-B4(gate 无机器强制)+ KG-B7(反作弊单次执行)同族三层一簇审,产 PPV 结构 verdict 后再动 PRD/spec——避免重蹈 T004-A1「先花 14 轮硬化 B7、再被 B8 推翻前提」的过度投资教训。gate 未 PASS,T010/T011 维持 blocked 至 forge 决议落地。

**Follow-up commits**: pending(待 /expert-forge 001)

## 2026-07-16T07:57:27Z · 001-radar-pA-20260715T093226Z · follow-up(forge v1 verdict 落地)

**Reviewed at**: 2026-07-16T07:57:27Z
**Tags**: prd-revision-trigger(follow-up · 承接第 11 条决议)
**Severity**: high
**Operator decisions**:
- [x] 修 PRD §"O4 / Open questions #3 / Scope OUT"(v1.2 → v1.3)
- [ ] 修 SHARED-CONTRACT
- [x] 修 XenoDev spec(跨仓 · 待 XenoDev session 按 refactor-plan 四模块落地)
- [ ] 无操作

**Operator note**: forge 001 v1 收敛(strong-converge · 无 unresolved · stage-forge-001-v1.md)。verdict:人肉盲测二值签字 gate 从 T010/T011 前置退役(KG-B8 采纳);新前置 = 机器可判三项(trace schema 完整 / 证据 3 击可达 / 轻量文件级审计通道);识伪 retire-as-gate keep-as-calibration(产出只入 journal,零解锁语义);FAIL→STOP 双道(机器道代码级 wiring = KG-B4 改写落点 · 治理道 = prd-revision-trigger 通道);KG-B7 反作弊面现状冻结不再投资。operator 选 stage 文档 Decision menu [A] 落地。⚠ 落地前置警告:三项 checker「秒级可判」是推演,XenoDev 实装前先用真 briefing 验一次(forge §underweights 回声室预警)。**T010/T011 解锁语义自本决议起按 PRD v1.3 O4 执行**。

**Follow-up commits**: ddbd14c(forge v1 产物 + 第 11 条决议入库)· 3e34ba7(PRD v1.2→v1.3 落地)· XenoDev 侧 pending(spec §5/§6 + DAG + gate.py 降级 + trace-validator,待 build session)

## 2026-07-16T08:58:07Z · 001-radar-pA-20260716T085807Z

**Reviewed at**: 2026-07-16T10:16:54Z
**Tags**: prd-revision-trigger
**Severity**: high
**Operator decisions**:
- [ ] 修 PRD
- [ ] 修 SHARED-CONTRACT
- [ ] 修 XenoDev spec(本仓内,信息式)
- [ ] 无操作(收悉)
- [x] 起 forge v2 重裁(/expert-forge 001 · 「机器可判三项」①② 资格 + T010/T011 解锁前置 + KG-B9/B4 同簇)

**Operator note**: forge v1 verdict 自带的落地硬前置(§underweights:实装前用真 briefing 验三项 checker 秒级可判性)被 XenoDev 真跑触发 STOP:三项里 ①(trace/provenance schema 完整性)② (证据 3 击可达性)在当前 pipeline 拓扑下**无底料可判**——真 briefing(run-877f1c1e)零引用类 token;TimeSlice/DisplacementNarrative 无 source 回链;CLI 空传图;paper→slice 映射在 LLM 调用后被丢。根因 = **循环依赖**:能产出机器可解析 trace 的环节(T011 图+source 锚 / T021 证据链)恰是 gate 下游、被同一 gate 所 gate;checker 底料 ⊂ gate 所 gate 的范围。独立对抗子代理交叉核验零分歧。这是 forge v1 Decision menu [B] 的字面适用条件(「XenoDev 真跑后三项 checker 可判性被推翻,需重裁」),走 verdict 自定义 STOP 出口起 v2,**不直接改 PRD**(①② 资格重裁属治理层,绕过 forge = 重蹈 V4)。v2 议题:①② 资格重裁(trace 前移 / 分阶段前置 / 重估「机器判 trace」是否该作解锁前置还是 O2/O7 使用期抽查对象)+ T010/T011 解锁前置再定义 + KG-B9(checker 底料循环依赖)与 B4 同簇处置(B4 wiring 对象一半不存在)。XenoDev 侧 gate/pipeline 代码保留不动,gate 未 PASS,T010/T011 维持 blocked。连续第三次同型教训:forge 推演决议 ≠ 真跑可行(v1 预警自兑现,真跑前置挡下了「先建 checker 再发现无底料」的过度投资)。

**Follow-up commits**: pending(待 /expert-forge 001 v2)

## 2026-07-16T13:35:18Z · 001-radar-pA-20260716T085807Z · follow-up(forge v2 verdict 落地)

**Reviewed at**: 2026-07-16T13:35:18Z
**Tags**: prd-revision-trigger(follow-up · 承接第 13 条决议)
**Severity**: high
**Operator decisions**:
- [x] 修 PRD §"O4 / Open questions #3 / Scope OUT"(v1.3 → v1.4)
- [ ] 修 SHARED-CONTRACT
- [x] 修 XenoDev spec(跨仓 · 待 XenoDev session 按 refactor-plan A'/B'/C'/D' 四模块落地)
- [ ] 无操作

**Operator note**: forge 001 v2 收敛(strong-converge · converged 无 unresolved · stage-forge-001-v2.md · 当天走完 P0→P4)。verdict:①②(trace schema 完整性 / 证据 3 击可达性)从 T010/T011 解锁前置**退役**(采纳 KG-B9 循环依赖;深层病灶 = ① 谓词对象「判断/边」在解锁时点结构性不存在),重绑 T021/T022 ship 验收(验收测名字面即此两项)+ O2/O7 使用期抽查;**新解锁前置 = a1 单一谓词**(per-slice source 映射最小前移,走 P0.1 amendment 通道不被 gate 挡,T010/T011 同批解锁);**生效条件写死「真 briefing rerun 自证 PASS」**(v1「建议真跑」升级为硬条款 = 本轮最重要机制强化);解锁语义显式 stage-0 + 自托管点;KG-B4 wiring 改绑 a1 映射+审计通道结构+治理记录;B7 冻结/识伪零解锁/双道 STOP 维持。operator 选 stage 文档 Decision menu [A] 落地。⚠ 落地警告(§underweights):「a1 谓词秒级可判」仍是推演(与 v1 被推翻假设同型,故生效条款硬门兜底);a1 动冻结 TimeSlice,实装前逐面枚举消费面。**T010/T011 解锁语义自本决议起按 PRD v1.4 O4 执行**。v3 触发条件:a1 真跑仍不可判 / T021 落地时 ①② 在 Phase 2 出口不可判 / 使用期抽查范式失效 / TimeSlice 消费面代价远超 S-M。

**Follow-up commits**: f7e2f32(forge v2 产物 + 第 13 条决议入库)· dc8f4b4(PRD v1.3→v1.4 落地)· XenoDev 侧 pending(dogfood-backlog 回填段本次已 append 未 commit,spec §5 + DAG + a1 amendment + unlock-preflight checker 待 build session)
