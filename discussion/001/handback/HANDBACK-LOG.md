---
doc_type: handback-decision-log
first_created: 2026-07-10T06:46:12Z
last_updated: 2026-08-02T14:59:40Z
total_decisions: 39
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

## 2026-07-16T17:01:53Z · 001-radar-pA-20260716T170153Z

**Reviewed at**: 2026-07-16T23:05:46Z
**Tags**: build-complete
**Severity**: medium
**Operator decisions**:
- [ ] 修 PRD
- [x] 修 SHARED-CONTRACT(**pending** · §6 spine 通用 checker 层「下游 provenance 机器强制绑上游 gate PASS」· 随 spine 裁决一并落地;框架级变更按规约只走 forge,不当场直改)
- [x] 修 XenoDev spec(跨仓 · **§5 #1 BLOCKING**:spec-writer 落 DAG 边 T003-A3→T004-A2→T004-A4 + T010/T011 `depends_on` 改绑 T004-A4 + 加测断言 DAG/frontmatter 不再有 T004A1 直连;#2 三个 amendment task doc(T003-A3/T004-A2/T004-A4)纳入 frozen spec)
- [x] 收悉四模块 build-complete(A'/B'/C'/D' 全 DONE · 318 passed · ruff clean · 13 轮 codex adversarial 全 finding 真实 · practice-stats 入库)

**Operator note**: forge v2 verdict [A] 四模块落地收悉(承接第 14/15 条)。§6 gate-spine 子协议(「下游 provenance 机器不可伪造绑上游 gate PASS」· A' 面 gate-PASS artifact 可伪造 + D' 面 selfcheck 只信 caller 布尔 = 两面同病)裁决 = **暂缓·记录待裁**:build 侧已诚实降级为「非不可伪造安全边界 · 只结构检查」+ 程序纪律,fail-closed 仍挡无意/低技巧误用;KG-B10 已入 XenoDev dogfood-backlog;forge v3 / 拆独立 task / SHARED-CONTRACT 通用层的取舍等 D' 真 rerun 自证跑完后再定,避免 KG-B7 过度投资。SHARED-CONTRACT 修订因此标 pending、随 spine 裁决一并走。当前唯一 BLOCKING = §5 #1:DAG/frontmatter 结构依赖未改前,按图调度的 parallel-builder 可绕过 preflight/selfcheck(prose 前置已改但结构依赖未改),机器道 wiring 不完整——下一步最优先。

**Follow-up commits**: pending(XenoDev 侧:spec-writer 落 §5 DAG/frontmatter 结构改;IDS 侧:SHARED-CONTRACT 修订随 spine 裁决)

## 2026-07-17T03:24:24Z · 001-radar-pA-20260717T032424Z

**Reviewed at**: 2026-07-17T04:30:44Z
**Tags**: build-complete
**Severity**: medium
**Operator decisions**:
- [ ] 修 PRD
- [ ] 修 SHARED-CONTRACT(维持 **pending** · KG-B10 spine 裁决时机不变 = 等 D' 真 rerun 出真证据后走 forge;codex 2026-07-17 re-review 提级 critical 仅作**紧迫度记录**,不改时序)
- [ ] 修 XenoDev spec(无需 —— 本包即 spec 结构改的收口报告)
- [x] 收悉 #1 BLOCKING 收口(上一包 §5 #1 = **DONE**:commit `a09d45b` · DAG 边 T003-A3→T004-A2→T004-A4 + T010/T011 `depends_on` 重绑 `[T004-A2,T004-A4]` · 机器道 wiring 结构闭合 · 纯 docs/spec 0 src · 318 passed · practice-stats 入库)

**Operator note**: 三项决议:① 收悉 #1 BLOCKING 收口,pending 列划掉「§5 #1」——调度图现强制走 preflight,prose 前置与结构依赖已对齐。② KG-B10 spine 子协议 forge 时机 = **维持暂缓,等 D' 真 rerun**(与上一条决议 + 本包 §3.2 建议一致,防 forge v5「审没真跑过的东西」教训;codex critical 提级入册为紧迫度信号)。③ D' 真 rerun = **先轮换 DEEPSEEK key 再授权跑**(该 key 有泄露前科且 008/001 共用,本包 §4 亦建议轮换;轮换后再在 XenoDev 侧跑 reconstruct 真跑,PASS + 独立核验一致方解锁 T010/T011)。KG-B11(spec-writer SKILL REVIEW-LOG 非 immutable)不单独起 IDS 侧动作——已在 XenoDev dogfood-backlog 在册,随框架批次攒批走 006 forge。当前 pending 链:key 轮换 → D' 真 rerun → PASS 解锁 T010/T011 → KG-B10/spine 裁决走 forge(KG-B11 同簇)。

**Follow-up commits**: pending(operator:轮换 DEEPSEEK key;XenoDev 侧:D' 真 rerun 自证;IDS 侧:SHARED-CONTRACT 修订仍随 spine 裁决)

## 2026-07-17T05:24:16Z · 001-radar-pA-20260717T052416Z

**Reviewed at**: 2026-07-17T05:29:55Z
**Tags**: prd-revision-trigger
**Severity**: high
**Operator decisions**:
- [ ] 修 PRD(不直接改 —— gate 形态经 forge v3 裁定后再回写 PRD/HANDOFF)
- [ ] 修 SHARED-CONTRACT(维持暂缓 · KG-B10「post-gate」时机前提取决于 gate 形态,形态先定 —— 本包 §3.2 真跑硬证据支持既有暂缓判断)
- [ ] 修 XenoDev spec(无需 —— 本包即 D′ 真 rerun 证据回流;项目内 gate/pipeline 代码保留不动,per §3.3)
- [x] **起 forge v3 重裁 gate 形态**(采纳 §3.1:裁 gate 存废/形态四方向——盲测二值签字 vs 留痕可审计验收 vs 非阻断 smoke signal vs 信任移 O7 后验——+ 新维度「a1 产物 per-slice source 映射何时/如何对 operator/审计可见」;真跑证据已齐,前三次裁决都缺的"真跑过"证据本次补上)

**Operator note**: 仅勾选「起 forge v3 重裁 gate 形态」——当前唯一关键路径,T010/T011 解锁、KG-B10、SHARED-CONTRACT 修订全 gated 在 gate 形态裁决之后。§3.2 暂缓 + §3.3 锁定为既有状态自然延续(上一条决议已在册),不需另行动作。附带入册:① a1 机制内存层验证生效(6/6 source_refs 真挂 TimeSlice + model_copy 往返保留),forge v3 不必再审 a1 对错;② 001 主线第四次「推演≠真跑」(首跑 FAIL / operator 拒 gate / KG-B9 循环依赖 / 本次真跑走不到 gate 判定);③ model 名以账号 `/models` 端点为真相源,非公开文档;④ DEEPSEEK key 轮换维持上条决议 pending 在册(本次未勾选为新 follow-up)。

**Follow-up commits**: pending(IDS 侧:`/expert-forge 001` 起 forge v3;XenoDev 侧:worktree-001-radar-pA 领先 main 含 `7d0a64c` 未 push,push 需 operator 确认)

## 2026-07-17T05:24:16Z · 001-radar-pA-20260717T052416Z · follow-up(forge v3 verdict 落地)

**Reviewed at**: 2026-07-17T07:02:01Z
**Tags**: prd-revision-trigger(follow-up)
**Severity**: high
**Operator decisions**:
- [x] 修 PRD(**DONE**:v1.4→v1.5 · O4 初始层重写为「分流 + 两层 + 机器自证」+ Scope OUT 补两条 + Open questions #3 更新 + v1.5 response;operator 经 forge v3 Decision menu [A] 显式批准)
- [ ] 修 SHARED-CONTRACT(维持暂缓 · **KG-B10 前提已收窄**至校准 run answer-key 密封完整性 + 自证记录防伪两处,方向 = 受控 writer/密码学绑定;spine 子协议细节与 SHARED-CONTRACT 通用层仍留后续)
- [x] 修 XenoDev spec(**授权下发**:dogfood-backlog 已 append「forge 001 v3 处置结果回填」段(worktree 副本 · 未 commit 留 XenoDev session 消费);四模块 A″(评估 run 生成时落 audit + 可见渲染面)/ B″(preflight 换 evidence bundle)/ C″(--calibration 分流 + 泄露面对抗验证)/ D″(07-17 真产物自证序列 + journal 字段级小改)全 S 级;audit_channel 防伪 spine 面冻结)
- [x] 收悉 forge v3 verdict(strong-converge · converged 无 unresolved:**g1 永久退役出解锁链;评估 run 证据生成时落盘始终可见;T010/T011 解锁全机器自证人不在判定回路;校准 run 只密封 answer-key 零解锁语义;g3 折入 O2/O7 信号;防 V4 双道保留**)

**Operator note**: 选 forge v3 Decision menu **[A] 全量落地**。⚠ **本决议显式覆盖第 16 条(hand-back `001-radar-pA-20260717T032424Z`)中「RERUN-PASS artifact 未退役 · 仍是 gate spine 底座 · 被 T004-A2 preflight 内部消费」的定位**——RERUN-PASS 一步退出 preflight 消费链(无双轨过渡窗口),其生成机制随校准活动保留或废止按 build 实况定,不再影响解锁链。生效条款「真 briefing rerun 自证 PASS」的 PASS 语义改写为 B′+D′ 机器谓词对真产物成立(自证对 07-17 真跑产物 diffusion-models-20260717T051551Z 立即可跑)。⚠ forge v3 §underweights 预警在案:回声室连续第三次高危;「S 级改接」「分流后校准泄露面收窄」仍是推演——D″ 立即自证是最后防线,v4 触发条件四条已列(改接超 S 级 / 泄露面未收窄 / 抽查范式失效 / KG-B10 校准面防伪方向不受控),任一命中走 prd-revision-trigger 回流。DEEPSEEK key 轮换维持 pending 在册。

**Follow-up commits**: IDS 侧 786d2a1(forge v3 全程产物 + 决议 17 入库)· ac71653(PRD v1.4→v1.5)· 本条 entry commit;XenoDev 侧 pending:四模块 A″/B″/C″/D″ 实装(dogfood-backlog 回填段随 XenoDev session 消费时一并 commit;worktree 领先 main 未 push)

## 2026-07-17T09:25:47Z · 001-radar-pA-20260717T092547Z

**Reviewed at**: 2026-07-17T16:50:59Z
**Tags**: build-complete · prd-revision-trigger
**Severity**: high
**Operator decisions**:
- [ ] 修 PRD(不直接改 —— 生效条款标的经 forge v4 裁定 α/β/γ 后再回写 PRD v1.5 O4)
- [ ] 修 SHARED-CONTRACT(维持暂缓 · KG-B10 spine 子协议在册冻结;协议面已收窄至校准 run answer-key 密封完整性 + 自证记录防伪两处,细节随 spine 裁决)
- [ ] 修 XenoDev spec(无需 —— spec amendment_3 已收口 codex@2026-07-17;四模块实装属 build 产物)
- [x] **起 forge v4 重裁生效条款标的**(采纳 §6:α 生效自证改对评估 run 新产物跑 / β 07-17 产物特批 pre-split 豁免 / γ 生效条款改「首个评估 run 产物落地即自证」+ 07-17 降为校准活动历史样本;**XenoDev 倾向 γ**;v4 触发实为「生效条款前提在真跑下不成立」= 第五次「推演≠真跑」,v3 §underweights 四条监测项 ①-④ 均未命中)

**Operator note**: 仅勾选「起 forge v4」——四模块机制采纳(354 passed · codex 9 轮 adversarial approve · round-2 真生产 bug「评估产物标题非 B′ 可解析」已修 · 有界护栏 finding 全修)与 D″ STOP 诚实定性(07-17 真产物系 pre-split 校准产物,评估自证正确 fail-closed 不假 PASS · operator 已决 Option A)一并收悉入册,不需另行动作。⚠ 投递异常记录:本包滞留 XenoDev worktree `.work/handback-forge-v3-landing.md` 未投递(producer 端漏最后一步),由 IDS 侧代跑 producer 6 约束 PASS 后补投递入库(consumer 6 约束亦 PASS)。附带在册:① XenoDev worktree-001-radar-pA 上本批 forge v3 实装(13 改 + 8 新文件)**尚未 commit**,且分支领先 main 26+ commits 未 push,待 operator 确认收编;② KG-B10 spine 子协议维持冻结在册(防 KG-B7 过度投资),随后续 forge 裁;③ pre-existing lint 债 F541×2(tests/test_reconstruct.py:658-659 · T003-A2 引入)记录在案不入本批 scope;④ DEEPSEEK key 轮换维持 pending 在册(本批 D″ 用确定性 retrieval 未烧 key)。

**Follow-up commits**: pending(IDS 侧:`/expert-forge 001` 起 forge v4 重裁生效条款标的;XenoDev 侧:forge v3 实装收编 commit + worktree push 均待 operator 确认)

## 2026-07-17T09:25:47Z · 001-radar-pA-20260717T092547Z · follow-up(forge v4 verdict 落地)

**Reviewed at**: 2026-07-18T08:55:00Z
**Tags**: build-complete · prd-revision-trigger(follow-up · 承接第 19 条决议)
**Severity**: high
**Operator decisions**:
- [x] 修 PRD(**DONE**:v1.5→v1.6 · O4 生效条件段整段替换(标的:07-17 真产物 → 首个评估 run 产物 · 同 stem · 同一验收事件 · 四态显式:同事件自证/首个 PASS 生效/FAIL 回流重试/未跑 landed-not-yet-effective)+ 07-17 处置一句(降校准活动历史样本 · exclusion 非豁免)+ Open questions #3 更新(v4 amendment lineage + v5 触发条件五条)+ v1.6 response;operator 经 forge v4 Decision menu 选 [2]=[A] 显式批准)
- [ ] 修 SHARED-CONTRACT(维持暂缓 · KG-B10 spine 冻结不变;「同一验收事件」ts 间隔机器强制与密钥治理通用化均降 v0.2 note,攒首批评估 run 实况后与 spine 同窗裁)
- [x] 修 XenoDev spec(**授权下发**:dogfood-backlog append「forge 001 v4 处置结果回填」段(worktree 副本 · 未 commit 留 XenoDev session 消费);三件事:a. **即刻收编** forge v3 worktree 实装 commit(状态命名「机制 landed」)b. selfcheck 脚本 S 级参数化(direction/ts/briefing · 只复用现有 D″ 入口/守卫 · 禁新判据/旁路/spine · 超 S 回落手工模板)c. key 轮换 → 授权 → 首个默认评估 run → 同一验收事件内同 stem 自证)
- [x] 收悉 forge v4 verdict(strong-converge · converged 无 unresolved:**采 γ · 正式 amendment 非 waiver;β cut(ML eval hygiene 零豁免先例 + 临床 protocol「waivers not permitted」跨域合围);α 收编为 γ 立即执行形态;key 轮换写入 runbook 序列不进 B′/D′ 机器谓词;护栏三道守卫 + 14 测 + KG-B10 冻结全 keep 零削弱**)

**Operator note**: 选 forge v4 Decision menu **[A] 落地**(operator 回复 [2] = 直接落地)。生效语义自此两态:**机制 landed**(XenoDev 收编 commit 即达)≠ **条款生效**(首个评估 run 自证 PASS 才达);landed-not-yet-effective 是诚实中间态,无 deadline 有判据(canary blocked-until-verified 正统)。⚠ forge v4 §underweights 预警在案:回声室连续第四次高危(双方 P1 独立同构;缓解证据 = P2 源不重叠互证 + GPT 回声室自检产出 amendment 正当性条件反向材料);「同一验收事件」现靠 runbook 纪律未机器强制(悬空风险从标的错配换位到自证时机);参数化 S 级仍是推演——**首个评估 run 的真跑自证是本 amendment 的最后防线**。⚠ 生效时点实质由 key 轮换节奏决定(轮换自决议 16 起三连 pending,持续 pending 则条款诚实停在 landed-not-yet-effective;v5 触发条件⑤在案)。v5 触发条件五条:首个评估 run 再 STOP / 参数化远超 S / 事件锚僵尸化 / 验收事件纪律被打破 / key 轮换持续 pending 阻塞生效。

**Follow-up commits**: IDS 侧 pending 本 session(forge v4 全程产物 + PRD v1.5→v1.6 + 本条 entry);XenoDev 侧 pending:a. 收编 commit(即刻)b. 脚本参数化 c. key 轮换 → 首个评估 run → 同事件自证(dogfood-backlog 回填段随 XenoDev session 消费时一并 commit;worktree 领先 main 未 push)

## 2026-07-18T13:54:00Z · 001-radar-pA-20260718T135400Z

**Reviewed at**: 2026-07-18T14:19:01Z
**Tags**: feature(语义 = build-complete 里程碑;因 gen-handback tag enum 已剔除 `build-complete` 改用合法值 `feature`,漂移本身见下)
**Severity**: medium
**Operator decisions**:
- [ ] 修 PRD(无需 —— 机制 landed 里程碑与 PRD v1.6 O4 两态语义完全一致,条款生效路径不变)
- [ ] 修 SHARED-CONTRACT(不当场改 —— KG-B5 族三项产者工具漂移未授权攒批动作,仅在册,见 note)
- [ ] 修 XenoDev spec(无需 —— §a 4 commit 收编 + §b 参数化即第 20 条决议授权 a/b 的执行结果,spec 无新缺口)
- [x] 无操作(**收悉 · 机制 landed 里程碑确认**):§a 收编 4 commit(`11e81dd` feat / `6d442af` test +55 · 354 passed 零回归 / `4c626a7` docs / `a43da36` refactor 参数化)= forge v4 verdict §a/§b 待办全落地;§c 条款生效维持 operator 门控显式 deferred(key 轮换 → 选方向 → 授权烧 key → 首个评估 run 同事件自证)

**Operator note**: 仅勾选「收悉·里程碑确认」。生效状态自此:**机制 landed = DONE**(第 20 条授权 a/b 兑现 · 参数化 S 级达标 codex adversarial approve 0 material findings · 三道守卫零削弱)· **条款生效 = landed-not-yet-effective**(诚实中间态维持 · 待 §c)。§underweights 兑现监测入册:✅ 参数化确 S 级(v5 触发条件②缓解);⏳「同一验收事件」仍 runbook 纪律(v5 触发④在案);⏳ 首个评估 run 真跑自证仍是本 amendment 最后防线(再 STOP = 第六次「推演≠真跑」= v5 触发①)。**在册未授权动作项(operator 未勾选,不视为决议)**:① KG-B5 族 ×3 产者工具漂移(仓根 HANDOFF `git_common_dir_hash` 陈旧 `11c3…`→实际 `bbf1…`,mode-1 短路不阻断 / gen-handback tag enum 剔除 `build-complete` 与已投递实践漂移 / gen-handback template 硬编码 macOS 路径无占位符 + `REPO_ROOT` 与 section-base 耦合,本包 3 字段系 producer 手工修正)—— 已由 XenoDev 记 dogfood-backlog 在册,随框架批次归 006 forge 时机由 operator 另裁;② KG-B10(校准面防伪方向)/ KG-B11(SKILL §3.2.1 协议债)维持原判在册;③ F541×2 ruff 债(tests/test_reconstruct.py:658-659 · pre-existing)未授权顺清,维持记录在案;④ 附带修复 `731b685`(仓根 stale 008-pB HANDOFF 字节 mirror 修复)收悉 —— 本包正确产 001 身份即其生效验证。⚠ 投递方式正常(producer 直投,无上次 `.work/` 滞留异常复发)。

**Follow-up commits**: pending(IDS 侧:本 hand-back 包 + 本条 entry 入库 commit;XenoDev 侧:worktree 31 commit 领先 main 未 push,收编已完成待 operator 定 push 节奏;§c 序列维持 operator 门控)

## 2026-07-18T23:16:42Z · 001-radar-pA-20260718T231642Z

**Reviewed at**: 2026-07-19T00:29:52Z
**Tags**: feature(语义 = forge v4 §c 条款生效事件里程碑;gen-handback enum 无 `clause-effectuation`,沿用第 21 条同判据,enum 漂移维持在册)
**Severity**: medium
**Operator decisions**:
- [x] 修 PRD(**DONE 本 session**:v1.6 生效状态标注三处——① header 加 Effective 行(`landed-not-yet-effective` → `landed-and-effective`)② O4 生效条件段加生效记录(标的 `diffusion-models-20260718T231343Z` · 同一验收事件 B′+D′ 自证 PASS · unlock-preflight exit 0 · 生效绑定 stem,后续评估 run 各自按①履行同事件自证义务)③ Open questions #3 加兑现注记(最后防线兑现 · v5 触发①④未触发 · 残留监测继续在案)。**条款文本零改动,版本号维持 v1.6**——生效是状态兑现非条款修订,不 bump 版本)
- [ ] 修 SHARED-CONTRACT(无需 —— 两态语义已随 v4 verdict 落 PRD,协议层无新缺口;KG-B10 spine 冻结维持)
- [ ] 修 XenoDev spec(无需 —— 本次是 runbook 纪律路径的正确执行,只复用现有 `run_selfcheck_sequence` + 三道守卫,无新增判据/旁路,spec 无新缺口)
- [ ] 无操作(不适用 —— 本条有 PRD 状态标注动作)

**Operator note**: 选「确认生效 + 修 PRD」。**两态迁移在本 discussion 收口:机制 landed = DONE(第 21 条)· 条款生效 = DONE(本条)= landed-and-effective**。第六次「推演≠真跑」判定**落生效侧**(真跑 PASS 非被推翻)——上游 forge/推演 verdict 四连被下游真跑推翻的链,在本条款以真跑 PASS 收口。真跑证据链:首个默认评估 run `diffusion-models-20260718T231343Z`(operator 三前置门逐一显式授权:key 就位確认(C8 合规 · presence/长度检查 · 值不进 stdout · C12 hook 两度 fail-closed 已尊重不绕)/ 方向 diffusion models / 授权烧 key;真 OpenAlex + 真 DeepSeek · 封闭历史窗 2021→2023 与 selfcheck 缺省窗逐字一致 · 新 ts 与 07-17 校准样本干净隔离不撞 ①b 守卫)→ 同一验收事件内一气呵成:B′ 四件全 PASS · D′ `unlock_allowed=True`/`is_fixture=False`/独立检索双路径一致 · audit_digest 入 append-only journal → unlock-preflight 四参齐 exit 0 → **T010/T011 hard-block 解除**(机器核验 · 人不在判定回路)。§underweights 兑现监测收册:✅ v5 触发①(首个评估 run 再 STOP)未触发;✅ v5 触发④(先用后证/隔日补证)未触发——一气呵成守住,但「同一验收事件」仍 runbook 纪律未机器强制,继续在案;⏳ KG-B10 provider-proof spine 未触及维持冻结(本次走的正是纪律默认路径 · 归 IDS forge 决落地时机)。**在册未授权动作项(不视为决议)**:KG-B11 / KG-B5 族(gen-handback template macOS 硬编码本次**再次触发**,本包 4 字段系 producer 手工修正为 Ubuntu canonical 值;建议 template 占位 + env 化 · REPO_ROOT 与 section-base 解耦)随框架批次归 006 forge 攒批,时机 operator 另裁。**T010/T011 后续(build 侧)**:可起跑,起跑前 parallel-builder 会再跑 unlock-preflight 作 hard-block 门;生效绑定本 evidence bundle stem,换方向/换窗需对新评估 run 重跑自证。⚠ 投递方式正常(producer 直投 · 无 `.work/` 滞留复发)。

**Follow-up commits**: pending 本 session(IDS 侧:本 hand-back 包 + PRD v1.6 生效标注 + 本条 entry 入库 commit;XenoDev 侧:worktree 33 commit 领先 main 未 push,push 节奏 operator 另定)

## 2026-07-19T01:28:21Z · 001-radar-pA-20260719T012821Z

**Reviewed at**: 2026-07-23T07:59:19Z
**Tags**: feature(T010 检索规模化强化 build-ship · Phase 1 · spec §5 P1.1)
**Severity**: low
**Operator decisions**:
- [ ] 修 PRD(无需 —— T010 `ScaledRetriever` 实现与 spec §5 P1.1 + OUT-5/C6/C9 完全一致,无 PRD/spec 缺口)
- [ ] 修 SHARED-CONTRACT(无需 —— §4.4 verifier 实证 SHARED-CONTRACT 0 改动)
- [ ] 修 XenoDev spec(无需 —— 加层非改骨架,file_domain 只 `scale.py`,不改 T002 `openalex.py` 骨架)
- [x] 无操作(**收悉 · T010 feature ship 确认**):`ScaledRetriever` compose 多 base retriever 合并去重 + 有界时序截断(`SCALE_MAX_PAPERS=1000` · OUT-5 不追全 · 超界诚实截断保时序前段)· C9 run-ephemeral 纯内存零文件写(禁 Candidate B 底座 · 有测锁)· codex review path-B(risk=low)**approve 0 finding** · 10 test cov 100% · **364 passed 零回归** · §4.4 verifier PASS(拓扑序 + diff 边界)。集成基线 = worktree 分支(非 main · 领先 33+ commit)。

**Operator note**: 仅勾选「无操作·收悉入库」+「KG-B5 dogfood 归 006」。T010 是 forge v4 §c 条款生效(第 22 条 landed-and-effective)后 unlock-preflight exit 0 解阻 T010/T011 的首个 build-ship,依赖门(depends_on T004-A2/A4)满足。**在册未授权动作项(不视为决议)**:KG-B5 族 dogfood 本次再触发 —— ① gen-handback template macOS 硬编码(producer 手工修 5 字段 + 补 baseline/worktree)② codex-review SKILL §0.1 companion 路径版本漂移(硬编码 `codex/1.0.3/` · 包称 Ubuntu 实际 `1.0.4/`)—— 随框架批次归 006 forge 攒批,时机 operator 另裁。**交叉核验补充(非包内自报)**:(a) IDS 侧 bootstrap-kit 源模板 `handback-validator/templates/handback.template.md` 已用 `{{REPO_ROOT}}`/`{{SOURCE_REPO}}` 占位符(正确);被诉硬编码的是 **XenoDev 侧** template 副本 → 属跨仓修,非 IDS 修。(b) codex `1.0.*` plugin cache 本机 `~/.claude/` 不存在,无法从 IDS 侧证实 `1.0.4`,系 XenoDev-side 观察。**⚠ validator 调用注记**:6 约束校验须传绝对路径 —— `/handback-review` 命令模板字面用相对 `"$HANDBACK_DIR/<file>.md"` 会令 check-5 path 正则(`.*/discussion/`)误判 corruption FAIL;本次改传 realpath 后两包均 exit 0 PASS(此系命令模板 latent bug,与包内容无关)。

**Follow-up commits**: pending 本 session(IDS 侧:两 hand-back 包 + 本条 entry 入库 commit;XenoDev 侧:worktree 33+ commit 领先 main 未 push,push 节奏 operator 另定)

## 2026-07-19T01:35:23Z · 001-radar-pA-20260719T013523Z

**Reviewed at**: 2026-07-23T07:59:19Z
**Tags**: feature(T011 方法/claim 级图构建 build-ship · Phase 1 · spec §5 P1.2 · 差异化根 C6 · FU-T011-edge-provenance 折入)
**Severity**: medium
**Operator decisions**:
- [ ] 修 PRD(无需 —— 节点=方法/claim 非论文级(C6 防退化)+ 边关系级 source 锚(反 OUT-8 真理机)与 PRD O2 语义一致;冻结接口改是 spec/接口结构矛盾收口,非 PRD 语义变更 —— 见 note)
- [ ] 修 SHARED-CONTRACT(无需 —— 协议层无新缺口)
- [ ] 修 XenoDev spec(无需 —— FU-T011-edge-provenance 已在 build 侧折入 T011 branch,commit `a8cd87d` + task doc `7d4c441` + 状态更新;spec 无新缺口)
- [x] 无操作 —— 但含**冻结接口改动确认**(见下,operator 已勾「确认冻结改·收悉」):
  **✅ 确认冻结 domain 改 `GraphEdge.source_ref: SourceRef | None`(operator build 侧已授权 · IDS review 确认符合 T001 契约治理)**:spec §O2 + T011 task Outputs 明写「边挂 source_ref 锚供 T021 三击」,但 `GraphEdge`(T001 **冻结** domain · `model_config=_FROZEN`)无 source 字段 + `domain/` 在 T011 file_domain(`graph/**`)外 = 真 spec/冻结接口结构矛盾。codex adversarial-review **5 轮**收口(confirm-review reviewer 反对节点-only stub —— 无边无法兑现方法关系图目标 · T012/T020 依赖边判 structural_connection)→ operator 决 T011 gated 到 FU 先做 · 合并为**一个完整方法关系图** ship(拒节点-only stub)· 授权改冻结 T001 domain 加 `source_ref`(默认 None **向后兼容** · T003 空图/现有构造不破 · **385 passed** 验)。**同 KG-B5「结构改 frozen 授权」先例 · 非语义重写**。T011 交付:节点=方法/claim + 节点/边**均带真 source 锚**(只锚真检索 ref · 幻觉关系/悬挂/无锚边 fail-closed 丢弃 · 可 O2 三击)· `GRAPH_MAX_NODES=50`/`GRAPH_MAX_EDGES=200` 有界(OUT-5)· 复用 `reconstruct` 注入防御 + `_sample_window` 采样(codex 9 轮硬化,不重造)· C9 run-ephemeral · C8 key 注入 · 31 test cov 95% · ruff clean · **385 passed 零回归**。

**Operator note**: 勾选「确认冻结改·收悉」+「KG-B5 dogfood 归 006」—— **未升级 forge**。operator 明确将 `GraphEdge.source_ref` 判为 **spec/冻结接口结构矛盾的收口**(同 KG-B5 frozen 授权先例 · 默认 None 向后兼容 385 passed 验),**不视为触及 PRD O2 语义或需 forge 追认**(handback 决议级确认即足)。**T021 依赖链就位**:边 provenance 已落地 → T021(证据链强制)现可 depends_on FU-T011-edge-provenance(O2 三击到边的物理前提满足)。**在册未授权动作项(不视为决议)**:KG-B5 族 dogfood 三项 —— gen-handback template macOS 硬编码 / codex-review SKILL codex 路径 `1.0.3` 漂移 / eval-event-log writer.sh 接口漂移(真接 JSON via stdin · 非 parallel-builder SKILL §6.4 文档的 `--type` flag)—— 随框架批次归 006 forge 攒批,时机 operator 另裁。**注**:真 LLM 集成 build(task V2)deferred 未授权烧 key(C8 · 同 `_build_real_llm` 惯例 · 单测注入 fake LLM 全覆盖逻辑)。

**Follow-up commits**: pending 本 session(IDS 侧:两 hand-back 包 + 本条 entry 入库 commit;XenoDev 侧:worktree 领先 main 未 push,FU-T011 折入 commit `a8cd87d`/`7d4c441` 在 worktree,push 节奏 operator 另定)

## 2026-07-23T09:16:35Z · 001-radar-pA-20260723T091635Z

**Reviewed at**: 2026-07-23T09:35:06Z
**Tags**: feature(T012 历史切片重建收口·图上精化 build-ship · Phase 1 · spec §5 P1.3 · 差异化根 C6 图证据)
**Severity**: medium
**Operator decisions**:
- [ ] 修 PRD(无需 —— `GraphFinalizedReconstructor` 实现与 spec §5 P1.3 + C6/OUT-5/C9/C8/RT-2 一致;位移叙事经图信号精化点出 `structural_connection`(要件③首跑 FAIL「无新证据链」那格收口方向),无 PRD 缺口)
- [ ] 修 SHARED-CONTRACT(无需 —— §4.4 verifier 实证 SHARED-CONTRACT 0 改动)
- [ ] 修 XenoDev spec(无需 —— **零冻结 domain 改动**:图锚作 finalize 副产物(finalize.py 内本地 frozen dataclass · **非 domain**)· 吸取 T011 冻结矛盾教训「能不改冻结就不改」;仅新增 finalize.py,不改 reconstructor/slicer/writer 骨架)
- [x] 无操作(**收悉 · T012 feature ship 确认**):post-gate 图上精化 —— 在 T003 时间密度切窗 + T011 方法/claim 图基础上产最终 2-3 切片位移叙事(供 Phase 2 judge),每切片挂窗内图节点/边锚(供 T021 证据链 3 击),图接合关系喂 LLM 精化 prompt 引导点出 `structural_connection`。**轻量·锚+提示形态**(operator plan-mode 批准三决策:图信号=锚+提示不改切窗算法 / 端到端集成测 deferred / 图锚作 finalize 副产物非 domain)。复用单一真相不重造(`_canonicalize_doc_ref` gate + `_serialize_untrusted_field`+`_strip_judgment_words` 注入防御+RT-2 双保险)· 边落窗由**边关系级 source_ref** 判定(跨窗结构连接不丢)· 有界 `_MAX_RELATIONS_IN_PROMPT=40`/`_NARRATIVE_MAX_CHARS=800`(OUT-5)· C9 零落盘 · grep 门 `Judgment|radar_ring|briefing` 空(未偷做 judge/简报)· **22 test cov 100%** · **419 passed 零回归**(397+22)· §4.4 verifier(拓扑序 + diff 仅 finalize.py+tests/ + SHARED-CONTRACT 0 改)。**scope 边界确认(同 T011 finding#1 决议 · 不越)**:finalize 只挂结构锚 + 图信号引导 LLM,**不**做语义证据核验(强制 3 击到真原文核对 = T021 的活),避 scope creep;T021 现可 depends_on [T011, T012](节点/边锚 + 切片图锚就位)。

**Operator note**: 勾选「无操作·收悉入库」+「KG-B12 归 006·记环境已修」。**codex review 轨迹诚实**:round-1~3 三轮真 codex review 单调收敛(全 P2 级 · finding 逐轮更窄 = 前轮修复暴露的对称遗漏 · 全修+补测钉住 · typical approaching-approve 轨迹:r1 边落窗改边关系级 ref 判定 / r2 补 `reconstruct` 入口实现 T001 Protocol 可替换 T003 双入口 / r3 叙事回灌截断+空 ref 边守卫)· **round-4(确认收尾轮)= codex 后端环境故障(非代码/非 verdict)** → operator 决接受 r1~3 收敛证据 ship(同 009 codex 额度耗尽 subagent-fallback 精神 · 不因环境故障无限阻 ship)· hand-back 诚实标 round-4 未拿 codex 确认(reviewed-by = codex r1~3 收敛 + operator-accepted)。**KG-B12 处置 = 归 006 forge · 环境层已修记录在案**:KG-B12(codex 后端强推新模型 `gpt-5.6-sol` · 本地 codex CLI `1.0.4` 太旧 → round-4 `Codex error 400 "requires a newer version of Codex"` + `Reviewer failed` + exit 1 · 重试同错非瞬时 · codex-review gate 全线不可用 · high)。**⚠ 交叉核验(consumer 端实测 · 非包内自报)**:KG-B12 报的「gate 全线不可用」是 **build 时(09:16)** 状态;**环境层根因今天 17:16 已修** —— 本机 `~/.local/bin/codex` softlink 今日重指 → `codex-cli 0.144.5`(正是 `gpt-5.6-sol` 所需 `≥0.144.5`),与 forge009 上下文 memory(codex 双版本 + 5.6-sol 版本门槛 · 又一次「推演≠真跑」· 有备份可回滚)一致。故 **KG-B12 环境层修复 = 已完成(operator 今日 forge009 已做)**;归 006 forge 的是**框架层硬化**:① SKILL §0.1 加 codex 可用性/模型兼容性 preflight(起 review 前探 · 早 fail)② §7 补「后端模型版本 gate 失败」failure mode 显式处置(=环境故障非代码 · 不消耗 §4.2 四轮上限)③ codex 全不可用时 subagent-fallback 兜底策略(同 009 先例 · medium task 是否值得待议)+ codex plugin 升级(环境层 · 已修)。**在册未授权动作项(不视为决议)**:KG-B5 族 dogfood 三项沿用(gen-handback template macOS 硬编码 · codex-review SKILL 路径 `1.0.3`→`1.0.4` 漂移(与 KG-B12 同族 · B12 更严重因后端强推新模型) · eval-event-log writer.sh 真接 JSON via stdin 非 SKILL 文档 `--type` flag),随框架批次归 006 forge 攒批。**注**:真方向端到端集成(task Verification 检索→图→切片烧 key)deferred 未授权烧 key(C8 · 同 T011)。

**Follow-up commits**: pending 本 session(IDS 侧:本 hand-back 包 + 本条 entry 入库 commit,与 #23/#24 同批;XenoDev 侧:T012 合并回 worktree 分支(T010 `9bd150c` / T011 `f11a7b6` / T012 base=f11a7b6)· worktree 领先 main 未 push · push 节奏 operator 另定)。**下一活 = 起跑 T020(judge · depends_on T012)/ T021(证据链强制 · depends_on [T011,T012])**:新开 XenoDev session `claude -w 001-radar-pA`,起跑前重跑 unlock-preflight 作 hard-block 门。

## 2026-07-23T13:29:18Z · 001-radar-pA-20260723T132918Z

**Reviewed at**: 2026-07-23T15:03:08Z
**Tags**: prd-revision-trigger(spec 内部字面契约矛盾 · T020 结构成型度判断 judge · P1 级 · codex round-10 实证)
**Severity**: high
**Operator decisions**:
- [x] 修 PRD/spec §O2:**采 A1(producer 推荐 · 最小改)** —— spec §O2 加**低置信豁口条款**「`low_confidence=True 且 evidence=()` 的判断(证据不足 · O4 诚实信号)豁免 O2 的 3 击证据链强制;O2 只对**高置信/有锚**判断生效」· 对应改 §1 in-scope + §6「每条判断 3 击」为「每条**高置信**判断 3 击」。改在 **XenoDev spec**(`specs/001-radar-pA/spec.md` · O2=line 45 / §1 in-scope=line 60 / O1 长期锚=line 40),IDS PRD 语义**不改**(O2/O4/OUT-8 语义本已自洽 · 矛盾在 spec 派生层的字面耦合,非 PRD 缺口)。
- [ ] 改 T001 冻结 Judge Protocol 返非 Judgment 状态(**否决 A2** —— 触 KG-B5 冻结 interface 改 · 授权成本高 · 下游 T022 需另路渲染 · A1 已足)
- [ ] 裁 O2 字面优先 · 稀疏不产判断(**否决 A3** —— 丢 O4「证据不足以判」诚实产品信号 · 违 PRD「诚实第一块砖」精神 · producer 亦标不推荐)
- [ ] 无操作(**否决** —— T020/T021/T022 ship 合法性会持续悬空 · Phase 2 停滞)
- [x] **A4 附带项 → 攒批回 forge**:根因 KG-25(冻结 domain 不约束字段 → 消费端无限深 patch · 与本 spec 矛盾同源)记 XenoDev `dogfood-backlog.md` + 归 forge 攒批,与 **KG-B5 族 / KG-B11 / KG-B12** 一并起 `/expert-forge`(审 domain 最小约束:`SourceRef.ref` min_length / period 格式 / 图字段 max_length)· 符合 CLAUDE.md「框架级变更只走 forge」铁律 · 不当场改。

**Operator note**: 勾选「A1 spec 加低置信豁口(推荐)」+「A4 攒批回 forge(推荐)」。**矛盾性质裁定**:operator 采 producer 判 —— 这是 **spec 派生层两条 outcome 的字面契约矛盾**(O2「任一判断 3 击」vs O4/OUT-8「无证据必标低置信但未声明豁免证据链」在 `low_confidence=True ∧ evidence=()` 稀疏格直接对撞),**非 T020 代码错**。T020 impl 诚实守 OUT-8 反真理机红线(无真锚不伪造证据链)= 正确价值排序;A1 是把「已在跑的正确行为」正式落 frontmatter,**T020 现行为即 A1 目标形态 · 零行为变更 · 零冻结改**,与 memory 记 v6/R16 正面解法「实现选择类条款写成 A+判据+fallback」同构。**红线守护确认**:A1 继续守 OUT-8(不得为满足 O2 放松反真理机 = 那才是真理机)。**consumer 端交叉核验(非包内自报 · 我已逐条比对 XenoDev spec 原文 + judge.py + round-10 review-log)**:(a) spec 原文引证属实 —— O2(spec.md:45「任一判断 ≤3 击 · source_ref 可解析」)/ §1 in-scope(:60「每条判断 3 击」)/ O4(:47「低置信显式标注不做真理机」)/ OUT-8(:76「无证据判断必须标低置信」),四条字面确如包述,OUT-8 确**未**声明「低置信→豁免 O2」、O2 确**无**「低置信除外」;(b) round-6 interim 决已写进 `judge.py:87-91/116/127/251` 注释+契约测(「T021 对 low_confidence=True 且 evidence=() 判断豁口」)但**未落 frozen spec 字面** = 包述「决议是 plan,spec 字面未改,契约合法性悬空」属实;(c) round-10 P1 finding 实证(`T020-round10.md:52`「不要让稀疏判断绕过证据链强制 · 低置信标记并未在现有契约中豁免证据链」)= codex 独立复核,非推演。**验证器注记(同 #23/#24/#25 复现)**:6 约束校验须传绝对路径 —— 命令模板字面相对 `"$HANDBACK_DIR/<file>.md"` 因 `$HANDBACK_DIR` 尾斜杠致 `handback//` 双斜杠 → check-5 path 正则误判 corruption FAIL;传 realpath 后 6 约束全 exit 0 PASS(此系命令模板 latent bug,与包内容无关 · 已多次归 006 攒批)。**在册未授权动作项(不视为决议)**:KG-B5 族 dogfood(gen-handback template macOS 硬编码 / codex-review SKILL 路径漂移 / eval-event-log writer.sh 接口漂移)+ KG-B12(codex 后端强推 gpt-5.6-sol · 环境层今日 17:16 已修软链→0.144.5 · 框架层硬化待 forge)沿用,随框架批次归 006 forge 攒批。

**Follow-up commits**: pending 本 session(IDS 侧:本 hand-back 包 + 本条 entry 入库 commit;**A1 spec 落地待跨仓** —— 需 `cd "$XENODEV_ROOT"` 改 `specs/001-radar-pA/spec.md` §O2/§1/§6 加低置信豁口条款(或经 `/scope-inject 001` 若走 IDS PRD 侧,但本裁定改在 XenoDev spec 派生层);A4 forge backlog 记 XenoDev `dogfood-backlog.md`。XenoDev 侧 T020 worktree 分支 `task/001-radar-pA-T020-judge` 保留 blocked-on-spec,spec 加豁口后解 blocked · merge · 起 T021)。**下一活 = 跨仓落 A1**:改 XenoDev spec §O2 加豁口 → 回 XenoDev session `claude -w 001-radar-pA` 解 T020 blocked · merge · 起 T021(证据链强制 · depends_on [T011,T012] · 据 A1 豁口实装:断链=ship-blocker 只对高置信判断)。

## 2026-07-27T11:36:53Z · 001-radar-pA-20260727T113653Z

**Reviewed at**: 2026-07-27T13:10:17Z
**Tags**: feature(T021 证据链强制 + source_ref 真解析 build-ship · A1 豁口 owner 实装 · depends_on [T011,T012])/ drift(①评审门来源 ≠ codex ②评审中真跑复现 KG-29 项目级 high 缺陷)
**Severity**: high
**Operator decisions**:
- [ ] 修 PRD(无需 —— 本包 §3 未提任何 PRD 缺口;T021 是第 26 条决议 A1 豁口的实装,PRD 语义未被触碰)
- [ ] 修 SHARED-CONTRACT(无需 —— 无协议层改动诉求)
- [ ] 修 XenoDev spec(本轮无需 —— 恒等映射设计决定属 §3 B「已由 operator 批准 · 供存档不需再决」)
- [x] 无操作(**收悉 · T021 feature ship 确认**):`src/radar/evidence/`(anchors/enforce/exemption)对**非豁免**判断强制「anchor 真存在 ∧ anchor 映射 ref 与自报 `source_ref` 同一文档身份 ∧ 该文档确在本次真检索语料内 ∧ 链 ≤3 击」;豁免判定两步(step A 集合级有序分支 A-1 sparse → A-2 no-provenance · canonical 校验前置;step B 逐条分类),**豁免资格从原始数据重算不读 caller 自报 flag**(反 KG-B10「caller 自报=可伪造」)。契约测 256(+1 strict xfail)· `radar.evidence` coverage 100% · 全量 716 passed · ruff clean · mutation 12/12 全杀。**诚实边界(spec-sanctioned)**:只证证据链 **provenance 身份**,不证文档内容语义支撑该判断 —— spec §6 明写语义核验仍归 operator 人审、结构锚必须真指向本 run 产物,operator 2026-07-27 已裁「语义支撑接受为已知残留」。
- [x] **框架级 3 条 → 归 006 forge 攒批**(见本轮 #28 合并勾选,不当场改 · 符 CLAUDE.md「框架级变更只走 forge」铁律)
- [x] **T022 门禁裁定 → 见本轮 #28**(本包 §3 A 提的唯一 blocking 项「T022 是否 gated 在 FU-KG29 之后」已被同批次 #28 的 FU ship 就地回答)

**Operator note**: 勾选「无操作·收悉入库」+「框架级归 006」+「T022 直接起跑」。**评审门来源诚实标注(drift ①)**:codex round-10..13 各获一次真 verdict(全 needs-attention · finding 逐条实测复现后修),对 round-14 提交 `3ffb6ce` 起复审时撞**账号级配额墙**,真实报错 `Codex error: You've hit your usage limit ... try again at Aug 2nd, 2026 7:04 AM.` → companion 返 `Codex did not return valid structured JSON` + exit 1;重置窗口 ≈6 天使「暂挂等重置」不可行 → operator 2026-07-27 **授权改独立子代理 ×2 评审并要求显式标注来源 ≠ codex**,两份(红队对抗视角 + 正确性/可维护性视角)均判 needs-attention,共 7 条 finding 全部实测复现后修。⚠ producer 明确声明**未把 commit 摘要喂给任何模型换 approve、未自评自签、不冒充 codex verdict**(KG-28 红线)—— 该诚实标注是本包可信度的承重面。**operator 补跑裁定**:08-02 配额重置后**对 T021 + FU-KG29 两 task 补跑一次 codex adversarial-review 把账做平** —— 独立子代理两轮共挖 12 条真 finding 质量不差,但**它们不是协议规定的那道门**,补跑同时也是对替代路径质量的一次真实校准数据。**KG-29 缺陷性质(drift ②)**:`graph/builder.py:90` 的 `prompt_ref_canon = {canonical: 原始ref}` 以 canonical 为唯一键、**碰撞时后者静默覆盖前者**;真跑复现(非推演)—— 语料同含 `https://repo.example/paper` 与 `.../paper/` 两篇不同文档,LLM 明确返前者、builder 实际锚到后者,无异常无日志;judge 原样复制该错 ref,enforcement 查 membership 时**它确实在语料里** → **全链无 blocker**,即 O2「3 击回溯真原文」在该链上是**假的**。越 T021 file_domain(`src/radar/evidence/**`)故按「不当场改」纪律只记不改,域内以 `xfail(strict=True, raises=AssertionError)` 钉住 + 生产链绑定测断言逐个 node/edge 锚到预期那一篇。**consumer 端交叉核验(IDS 侧实跑 · 非采信包内自报)**:(a) `enforce_evidence_chain` 生产消费点 —— `rg` 全 `projects/001-radar-pA/src/` 仅命中 `enforce.py` 定义与 `__init__.py` 再导出,**零 caller** = 包述「KG-29 属潜伏未在跑」属实,该事实是 T022 门禁裁定的关键缓解依据;(b) XenoDev worktree `worktree-001-radar-pA` 上 T021 commit `7febdde` 在册。**在册设计决定(§3 B · 存档不再决)**:文档身份 = **恒等映射(逐字)弃归一折叠** —— 折叠版连续 5 轮被 codex 证出可执行碰撞(query/fragment 被吞 → arXiv 版本与 DOI 尾斜杠被裁 → 空分隔符不可区分 → IPv6 方括号被剥 → IPvFuture 不含冒号 → port 转 int 丢词法 → `urlsplit` 静默删控制字符),根因「归一必须单射」在通用 URL 上极难成立,而同一 key 同时用于 anchor↔ref 一致性与 corpus membership,任一碰撞都让未检索资源穿过两道门;恒等映射天然单射使该证明义务整体消失。前提**机器可验非假设**(`test_verbatim_ref_identity_holds_across_the_real_production_chain` 用 fake LLM 故意返别名以证 builder 锚回原始串;上游一旦改成让 LLM 自填 ref 该测立刻转红),折叠版全部碰撞用例保留为回归网。

**Follow-up commits**: pending 本 session(IDS 侧:本 hand-back 包 + #28 包 + 两条 entry 入库 commit;XenoDev 侧 T021 `7febdde` 在 `worktree-001-radar-pA` 分支,未 push,push 节奏 operator 另定)。**下一活见 #28**。

## 2026-07-27T12:45:18Z · 001-radar-pA-20260727T124518Z

**Reviewed at**: 2026-07-27T13:10:17Z
**Tags**: spec-gap-fix(FU-KG29-canonical-collision 两层根治 build-ship · 解除 codex 判定的「阻塞 ship」项)/ drift(①评审门来源仍 ≠ codex ②§4.4 自查违规 → 重建分支)
**Severity**: high
**Operator decisions**:
- [ ] 修 PRD(无需 —— 本包 §3 未提 PRD 缺口;FU 是项目级缺陷修复,PRD 语义未触碰)
- [ ] 修 SHARED-CONTRACT(无需)
- [ ] 修 XenoDev spec(**本轮不改** —— DOI 分支 `rstrip('/')` 同类残留越权裁为「记为已知残留暂不动」,见下)
- [x] 无操作(**收悉 · FU-KG29 ship 确认 · codex 阻塞项解除**):两层根因两层修 —— ①`credibility/gate.py` canonicalizer 停止对通用 URL 做无差别 `rstrip("/")`(该函数存在理由是消 DOI/arXiv 变体假 STOP,通用 URL 尾斜杠**从来不在该理由射程内**),path 改逐字保留、DOI/arXiv 折叠不动(既有 `test_canonicalize_doc_ref_maps_variants_to_same_key` 继续绿 = 未伤初衷);②`graph/builder.py` 单层字典改 `_RefIndex`:`exact`(原串逐字集 · **优先命中不经归一**)+ `alias`(canonical→原串 · **仅收唯一对应一篇**的 · 一对多整条剔除)→ 查不到即 **fail-closed 丢锚绝不猜**。全量 730 passed · `gate.py` 97% / `builder.py` 96% · ruff clean · mutation 8/8 全杀。T021 那条 `xfail(strict=True)` 修好后自动 XPASS(strict) 报错精确提示拆标记 —— **跨 task 跟踪钉机制走通一整轮**,marker 已拆转常规回归测。
- [x] **T022 起跑:直接起(不 gated)** —— codex 在 T021 round-12 判「KG-29 落地前阻塞 ship」,本 FU 即该落地:缺陷两层收口 + mutation 8/8 证有牙 + xfail 转常规回归测永久钉住 + `enforce_evidence_chain` 至今无生产消费点(消费点在 T022)故 **KG-29 从未真正暴露**,赶在 T022 起跑前修完。→ **T022 现无 KG-29 相关阻塞,授权起跑**。
- [x] **DOI 分支 `rstrip('/')` 残留 → 记为已知残留暂不动** —— 现由 fail-closed(歧义丢锚)兜住且既有测依赖它,docstring 已如实标注;要动需单独评估,不在本轮。
- [x] **框架级 4 条 → 归 006 forge 攒批**(本轮合并勾选 · 覆盖 #27+#28 两包):**KG-29 谓词 SSOT 缺失** / **KG-20 替代评审路径档** / **方法论 8 条回流 review checklist** / **handback frontmatter 路径失真(新 · consumer 端发现)**。

**Operator note**: 勾选「无操作·收悉」+「T022 直接起跑(推荐)」+「08-02 补跑两个 task 的 codex 评审(推荐)」+「DOI 残留记为已知暂不动(推荐)」+ 框架级四条全归 006。**评审门来源(drift ①)**:与 #27 同因 —— codex 仍在账号级配额墙内(重置 2026-08-02),本 task `risk_level: high` 本应强制 path A adversarial-review,按 operator 对**同一阻塞**的裁定走独立子代理 ×2 并显式标注来源 ≠ codex,两份均判 needs-attention,**5 条 finding 全部实测复现后修**。其中 **[I1] 是 producer 自己引入的缺陷且方向与本 FU 论点相反** —— 去掉全局 `rstrip("/")` 竟**同时加宽** DOI 分支(旧码因先 rstrip 使 `https://doi.org/` 永进不了 DOI 分支;去掉后其 body 为空却铸出 `doi:` key,于是 `doi:` / `https://doi.org/` / `http://doi.org/` / `https://dx.doi.org/` 塌成同一 key = 直接构成锚伪造面),而 docstring 只写了收窄 —— 「整个 FU 的论点是不折叠规范没保证的东西,实现却在别处折叠得更多」。[I2] 空 canonical 无守卫(`doc://` 剥前缀后空壳锚),而兄弟消费点 `finalize.py` 早在 codex round-3 就为此加过守卫、重写索引时无人提醒带上 = KG-29 框架级那半的**第二次自证**。[I3] 修完 canonicalizer 后三条以 KG-29 命名的测把 `_RefIndex` 整层还原掉照样绿(已重指到仍构成真碰撞的 DOI 变体 + 加前置断言)。[I4] R1 结论对理由错(实测 P0.2 解锁路径 canonicalize 调用数 = 0 · 真因是该路径压根不经 canonicalizer)。[红队 medium] 尾斜杠不符即掉锚系有意为之(不按其主推荐恢复容差 —— 那会部分撤销本修复),但掉锚零可观测属实 → 补诊断指向真根因。⚠ 同样明确声明未喂摘要换 approve、未自评自签、不冒充 codex verdict。**§4.4 自查违规处置(drift ②)**:pre-merge verifier 抓到起跑前的 `file_domain` 修正混在第一个 `test:` commit 里(违反「`test:` commit 只许动 `tests/`」)且 task doc 不在 `file_domain` 内 = diff 越界;虽 gate 的**意图**(防生产代码藏进 test commit)未被违反(改的是文档),producer 仍**重建分支**拆出独立 `docs(task):` 提交 + 补 file_domain,重跑三项全过 —— **不给自己开例外**的处置与「给自己开例外一次,下次就没有可援引的标准」的自陈一并留档可审。**consumer 端交叉核验(IDS 侧实跑 · 非采信自报)**:(a) `pytest --collect-only -q` = **730 tests collected**,与包述 730 passed 一致;(b) `rg xfail tests/` 仅命中 `test_evidence.py:823-826` 的 docstring 历史记述,**marker 确已拆** = 「xfail 转常规回归测」属实;(c) worktree `worktree-001-radar-pA` HEAD `6a50f3a`(FU)在 T021 `7febdde` 之上,DAG 顺序与包述一致;(d) `enforce_evidence_chain` 零生产 caller(见 #27)= 「从未真正暴露」属实。**⚠ consumer 端新发现(两包均未自报 · 已入 006 攒批)**:本轮两包 frontmatter `to_source_repo` / `workspace.source_repo` 均写 **`/Users/admin/codes/ideababy_stroller`**(已死 mac 路径),而 `handback_target` 是正确的 `/home/ys/...`;同机同仓相隔 4 小时的 `20260723T091635Z` 写 `/home/ys`、`132918Z` 写 `/Users/admin` → **至少一个是错的**。`gen-handback.sh:425-438` 本身有 forge v6 KG-26 的 fail-closed 解析链(`--source-repo` → `$IDS_REPO` → sibling → fail,**不会**写死 mac 路径),故这两包该字段**不是走那条链产的**;validator 不拦是因约束 3 用 repo_marker/remote/hash 而非该字段 → **跨仓 audit trail 上的静默失真**(与 KG-B5 族 gen-handback template macOS 硬编码同族,本次是**产出物实证**而非模板阅读)。**在册未授权动作项(不视为决议)**:KG-B5 族 / KG-B11 / KG-B12(环境层软链已修) / KG-25 沿用,随框架批次归 006 forge 攒批。

**Follow-up commits**: pending 本 session(IDS 侧:#27 + #28 两 hand-back 包 + 两条 entry 入库 commit,未 push;XenoDev 侧 FU `6a50f3a` 在 `worktree-001-radar-pA`,未 push)。**下一活 = 起 T022(PPV-P2 · briefing+evaluate CLI)**:新开 XenoDev session `claude -w 001-radar-pA`,起跑前重跑 unlock-preflight 作 hard-block 门;T022 起跑时把「上游 T021/FU-KG29 评审门为替代路径、08-02 后补跑 codex」记入 task doc 作评审债显式标注。**待办(时点触发)**:2026-08-02 codex 配额重置后补跑 T021 + FU-KG29 的 adversarial-review。**待办(攒批)**:框架级四条起 `/expert-forge 006`。

## 2026-07-28T01:04:57Z · 001-radar-pA-20260728T010457Z

**Reviewed at**: 2026-07-28T16:14:13Z
**Tags**: drift(替身输出形态与真 provider 行为长期脱节)/ spec-gap-fix(收成一处共享 helper · 容错边界只容围栏)
**Severity**: high
**Operator decisions**:
- [ ] 修 PRD(无需 —— provider 行为容错属实装层,PRD 语义未触碰)
- [ ] 修 SHARED-CONTRACT(无需)
- [ ] 修 XenoDev spec(无需 —— 本 FU 未改 spec)
- [x] **无操作(收悉 · FU-KG30 ship 确认)**:两个真跑才可能暴露的 provider 行为缺陷两处收口 —— ① 真 DeepSeek 把 JSON 包在 markdown 围栏返回,builder/judge 均裸 `json.loads` → 全链第 2 环 hard-fail;② 图 JSON 撞 `max_tokens=2000` 被**随机**截断(同 prompt 一次 4729 字符完整、一次 6462 字符被截),而客户端**丢弃了** provider 给的 `finish_reason` → 「被截断」与「返回垃圾」在下游无法区分。修法按 operator 裁定收成**一处共享 helper**(`radar/llm/json_response.py::parse_llm_json`),builder 与 judge 各调一次,直接规避 KG-29 那类同一谓词多消费端各自实装。**容错边界刻意严格 —— 只容围栏,绝不从任意文本捞取**:理由是**注入面**(上游 prompt 封着不可信的论文 title/abstract,LLM 可能复述被注入素材;若实现成「捞第一个 `{...}`」则响应里任何伪造 JSON 都可能被当结果,而图与判断正是证据链源头)。7 条 finding 全部实测复现后修,**两条最严重的由两名评审各自独立命中**。
- [x] **认可 `finish_reason=='length'` 全局 hard-fail 行为变更**(§3B.1 producer 请求确认)—— `complete()` 现对**所有**消费者在截断时失败响亮,含三个只吃散文的调用点(`reconstructor.py:239`/`:296`/`finalize.py:242`),**无 opt-out**。裁定认可:半截叙事被静默当完整叙事用下去,比失败响亮危险得多;而这三处正是产给人看的审计面。
- [x] **框架级 KG-30 归 006 forge 攒批**(见第 31 条汇总)

**Operator note**: **⚠ 对 KG-30 的归因更正(consumer 端,与 producer 表述不同)**:包述强调「四个 task 全绿 ship 却第一次真跑第一环炸」,易读成「批量开发之过」。**事实是那 4 个 task(T011/T012/T020/T021)每一个都单独评审过、都过 §4.4 verifier、都有 TDD 红绿证据** —— **评审没漏,是 ship 门里压根没有「真调一次 provider」这一项**。故「减少批量」推不出来(一个一个来同样会漏),**正确修法是加门不是减批**(即包述候选 (a)/(b)/(c) 方向)。此更正影响 B1 的 build 编排决策(见第 31 条:T030/31/32 授权三路并行,但每个 merge 前保留真 provider 冒烟这道轻量门)。
**方法论 5 条收悉**(与前批一并回流 review checklist):① **诊断文案的盲区本身就是缺陷** —— 错误文案只印响应开头 200 字符而截断证据全在尾部,**白烧一次真调用**才定位;② **「宣称 ≠ 实做」栽在 producer 自己的注释上** —— 宣称「两块围栏整体不匹配(歧义 fail-closed)」,实测是匹配的,fail-closed 是下游 `json.loads` **碰巧**兜住,**安全性质不该靠别的模块的实现细节承重**;③ **验证工具自身会失牙(第二次)** —— mutation 把 `_MAX_TOKENS = 8000 → 2000` 是**等长**替换,同秒改回时 CPython `.pyc` 缓存(按 mtime **秒** + size 判定)不失效 → 跑陈旧字节码 baseline 假红,已加 `PYTHONDONTWRITEBYTECODE=1`(上一批那次是 `"1 xfailed"` 含子串 `"failed"`,同族);④ **改一个旋钮必须看它的配对旋钮** —— 上限与超时是一对,只改一半只是把失败面从「坏 JSON」平移到**更贵**(token 已计费)且**更难认**(文案不指向根因)的「超时」;⑤ **mutation 存活的两种成因处置相反** —— 空响应守卫存活 = **代码冗余** → 删码;`max_tokens` 生效路径存活 = **测选错断言对象**(断了常量值而非它进请求体)→ 补牙。
**评审门来源(drift · 连续第 3 个 task)**:codex 账号级配额墙(重置 **2026-08-02**),operator 2026-07-28 明确指定走独立子代理 ×2(红队对抗 + 正确性/回归),均判 needs-attention。⚠ 明确声明未喂 commit 摘要换 approve、未自评自签(KG-28 红线)、**不冒充 codex verdict**。本包无 `ids_verdict_evidence` 块 —— 与「非 codex verdict」自陈一致,consumer 端 verdict-evidence 语法预检按契约跳过。
**consumer 端交叉核验(IDS 侧实跑)**:三包 6 约束 validator 全 PASS(传 realpath 绝对路径 · KG-12 已知坑规避)。

**Follow-up commits**: pending 本 session(IDS 侧:3 个 hand-back 包 + 第 29/30/31 条 entry 入库 commit,**未 push**)。

## 2026-07-28T01:34:06Z · 001-radar-pA-20260728T013406Z

**Reviewed at**: 2026-07-28T16:14:13Z
**Tags**: spec-gap-fix(P2 真路径连通性已证 · PASS 判据卡上游)/ drift(首次真跑第 2 环崩 → 逼出 FU-KG30)
**Severity**: high
**Operator decisions**:
- [ ] 修 PRD(本轮不改 —— 判据形态送 forge,见下)
- [ ] 修 SHARED-CONTRACT(无需)
- [ ] 修 XenoDev spec(**本轮不改** —— §1-O2 (c) 的下界形态是 forge 议题,不在 handback 单包决议级裁)
- [x] **T022 真路径连通性事实入账(不动任何判据)**:真检索 200 篇 + 真 DeepSeek · **全链无 mock** · exit 0 · 壁钟 **31.3 秒**(O3 要求 ≤30 分钟 · 57 倍余量)· 产物**真落盘非 stdout** · **1 条判断真挂上证据链** · 计数不足成因已按 §1-O2 (c) 硬性要求查清(**非**数据稀疏[200 篇/44 可用锚]、**非** provenance 丢失、**非** `_parse_judgments` 静默丢弃[LLM 原始就只返 1 条])。`enforce_evidence_chain` 至此有**第一个生产消费点**。
- [x] **⛔ P2 判 PASS 挂起 —— 判据形态送 `/expert-forge 001`,本轮不裁**(理由见 Operator note)
- [x] **8 条 finding 收悉**,其中两条 high 属「产物能说谎」类:① `render()` **从不看 `report.ship_blocked`** → 带幻觉 ref / anchor↔ref 错配的 report 会渲染成与合法产物**毫无视觉差别**的 briefing(CLI 恰好挡了一道,但 renderer 是**公共件**)→ 新增 `BriefingBlockedError`,**fail-closed 移进产产物的那个类里**;② **dry-run 产物谎称「全链真跑」** —— 与模块自己 docstring 直接矛盾,且发生在**那份就是 P2 证据**的文件上(spec §7 反 PPV 头号罪)→ 据实换警示横幅;③ 双向控制字符(U+202E RLO)穿透 `_md_inline_safe` 直达**人审面**(spec §6 把语义核验整个交给 operator 肉眼 = 本系统唯一语义安全网)→ renderer 加一层并**复用 T021 类别判据**不另立第二套。
- [x] **框架级 KG-30 归 006**(与第 29 条同条目,不重复计)

**Operator note**: **⛔ §3A(judge 无判断数下界)本轮不裁,送 forge 001 —— 决议理由如下(含 IDS 自身归因)**:
**(1) 根因比包述更靠上一层,且源头在 IDS 自己的第 26 条决议。** consumer 端读 spec v0.6 amendment log 原文查实:「≥3 条非豁免判断」是 **IDS `/handback-review 001` 第 26 条决议 A1** 落地时加入的。链条 = T020 codex round-10 逼出 spec 内部字面矛盾(§1-O2「任一判断 3 击」无限定 vs O4/OUT-8「无证据必标低置信 · 不做真理机」在稀疏格对撞)→ IDS 决 A1「给 spec 加低置信豁口条款」→ 但光加豁口会留「全豁免 = 空过」的洞 → 故补 (c)「豁免不计抽样 + 非豁免 <3 不判 PASS」。**故「3」的原始用途是防空过的守门数字 + 人审抽样量,不是任何统计推导的产物。**
**(2) 缺口是该决议当场结构性造出来的,不是后来发现的。** 同一次修订**改到了 T022.md 的契约**(抽样域收窄),却**明写「T020 已有实装零改动」** —— 而「零代码改解 blocked」正是当初选 A1 的卖点。**即:一边加了一个只有 T020 输出才能满足的数字门槛,一边明确规定不许动 T020。那个「零改动」正是让门槛够不着的原因。** 机器核验:`judge.py:53` `JUDGE_MAX_JUDGMENTS = 12`,`:364` 仅作上限截断;**全文件零下限措辞**(`rg '至少|最少|不少于|at least|no fewer|>=3|≥3'` 空)—— 包述属实。
**(3) 为何不由本命令裁 —— 后悔值不对称 + 自我审查停摆。** 候选方向的错误信号性质相反:「改指令逼 AI 凑 3 条」= 把防作弊的门改造成逼作弊的门(与 O4/OUT-8 诚实精神正面冲突,而那两条正是当初加豁口的理由),且**污染不可逆**(账本里躺着凑数判断);「改判据放松」= **门松了就不会再 fail,错了不会有任何信号**;「挂着」= **天天可见、可逆**。在无法立即验证哪个对时(codex 停摆至 08-02),应选错了会喊的那个。⚠ **更关键**:IDS 侧本轮的推理路径(判据挡路 → 查来历 → 发现来历不硬 → 建议放松)**与 009 forge v1 同构**,而 v1 被 forge v2 判为「证据在场却被解释掉」并整体撤销推论。**本命令既是该判据的立法者(第 26 条)又在提议修法,而唯一对抗性审查(codex adversarial-review)恰好不可用** → 结构上无法与那次自欺区分,**故不由本命令定案**。
**(4) 带进 forge 的输入(作候选,非决议)**:spec 原文自述 **O2 是长期累计锚**(「**不靠 gate 一次发证,靠使用中持续校准兑现**」· v1.1 已移出 gate),而 (c) 却要求**单份产物**独自扛满 3 条 —— **与 O2 自身定位打架**;同时 P2 的活是验证「整条链通不通」,用「必须产 3 条判断」量它属**量错了对象**(1 条挂了证据链的判断已证检索→图→切片→判断→证据链强制→渲染全通)。候选拆法:**单份 ≥1(防空过)+ 累计 ≥3(O2 抽样)**。⚠ 此为 forge 输入,**不是本轮决议**。
**(5) 与 §3B(第 31 条 A 项)同族,同批裁** —— 见第 31 条「判据的用途分类」。
**§3B 非 blocking 六项收悉**:`_md_inline_safe` 缺 Cc/Cf/Cs 剥离(正确的家在该函数本身 · reconstruct 审计面**仍然**会被 RLO 欺骗 · 建议起 FU 上收)· `_md_safe_ref` 与 `resolvable_doc_key` 谓词分歧(合法 Wiley DOI 被 O2 门接受却被渲染层 disarm → 证据链认证合格而产物里三击终点**复制出来不可解析** · KG-29 同族)· `_slugify` 抹掉非 ASCII(中文方向产 `direction-<ts>.md` 且同秒撞名)· **产物计数行已是事实上的机器可读接口**(`**非豁免判断**:N 条` 被两个测文件同一 regex 解析 · **T040 契约测集也会用** → **决 OQ-A1-1 时必须知道该格式串已承重,否则决议会静默打断读回**)· T001 `render(judgments)` 承载不下所需上下文(KG-25 族 · 建议改 `render(report)` · 记录在案以免 T030/T031/T040 建于错误假设)· 评审门连续第 4 个 task 非 codex。
**评审门来源(drift · 连续第 4 个 task)**:同第 29 条 —— 独立子代理 ×2,两份均 needs-attention,8 条全部实测复现后修;⚠ 未喂摘要换 approve、未自评自签、**不冒充 codex verdict**。
**方法论 6 条收悉**,最锋利一条:**「某一环被调用」证明不了「它的输出被采用」** —— producer 自认很强的门(断言 fake LLM 收到过全部 5 类 prompt),评审一个 mutation 就穿了(把 T012 精化结果丢掉改用未精化叙事,prompt 照样都发、门照样绿)。**真正的判据是产物里有没有那一环的指纹。** 余五条:fail-closed 保证必须住在产产物的那个类里不能住在某个调用方 · 产物 provenance 声明必须随运行模式变化 · 诊断文案盲区即缺陷 · 验证工具失牙第二次(等长 mutation + 秒级 mtime → `.pyc` 陈旧)· 计数不足要查成因不能顺手归给数据稀疏(spec §1-O2 (c) 写进了这条,本轮真用上了)。

**Follow-up commits**: pending 本 session(同第 29 条 commit)。**P2 物证重建暂不授权** —— 见第 31 条 C 项。

## 2026-07-28T04:11:03Z · 001-radar-pA-20260728T041103Z

**Reviewed at**: 2026-07-28T16:14:13Z
**Tags**: prd-revision-trigger(unlock-preflight 判据形态不可复现)/ drift(①producer 漏跑 IDS 明令的门 ②P2 产物灭失 ③`to_source_repo` 死路径根因)
**Severity**: high · **零代码改动包**(3 个 `docs(dogfood):` commit · 未改 src/spec/SKILL/framework)
**Operator decisions**:
- [x] **⭐ A · `unlock-preflight` 定为「一次性验收门」,退出常驻用法(采 producer 建议 A1)**:该门只在「评估 run 产物落地的同一验收事件内」跑一次,结果绑 evidence bundle stem 写 journal;**后续 task 起跑前不重跑**,改为**校 journal 里该 stem 的 PASS 记录存在**(纯本地读 · 可复现)。**同时撤回** HANDBACK-LOG:448「起跑前重跑 unlock-preflight 作 hard-block 门」这句指令 —— **该指令是第 28 条决议的产物,错在 IDS 侧,本轮撤销**。
- [x] **⛔ B(judge 下界)不在本条裁** —— 并案送 `/expert-forge 001`,见第 30 条。
- [x] **C · 镜像漂移四项全做**(见 Operator note 的 consumer 端更正)
- [x] **P2 物证重建暂不授权** —— 判据形态未定,现在重建的是**旧判据下的产物**;等 forge 001 裁完与新跑合并,只烧一次 DEEPSEEK key。
- [x] **08-02 codex 补跑范围扩到 7 个 task**:积压 4(T021 / FU-KG29 / FU-KG30 / T022)+ 新增 3(T030 / T031 / T032)。⚠ **必须显式要求跨 task 审,不得只逐个过一遍**。
- [x] **框架级归 006 攒批**:KG-30(high)/ KG-31(high)/ KG-32(medium)/ **镜像无同步机制(high · 新 · consumer 端查出)**/ KG 编号空间对齐;存量 KG-29 谓词 SSOT / KG-20 替代评审路径档 / 方法论回流 / KG-B5 族 / KG-B10 / KG-B11 / KG-B12 / KG-25 沿用。
- [x] **B1 build 授权:T030 / T031 / T032 三路并行起跑**(T040 / T041 ⛔ 不建 · 见 Operator note)

**Operator note**: **(A) 采 A1 的三条依据**:① **账本机制已现成** —— consumer 端实读 `out/journal/a1-selfcheck.jsonl`,已记 `ts`/`run_label`/`direction`/`audit_path`/`briefing_path`/`predicate_passed`/`checks{structure,resolvable,coverage,naming}`/`independent_check_agree`,即**已按 evidence bundle 绑定记录 PASS 状态**;且 `radar.credibility.rerun_selfcheck.n()` 已实装读该 journal 并**会拒绝 fixture 记录**(测试 `test_n_requires_nonfixture_pass_with_independent_agree` + 「fixture 记录不该被 n 接受作解锁凭据」)。**A1 基本是把已在跑的机制在协议上认下来,不是新建。** ② **这是撤销 IDS 自己第 28 条加的常驻用法、回到原设计** —— hand-back `20260718T231642Z` §4 原文已写「生效**绑定本 evidence bundle stem** · **每评估 run 各自生效 · 非全局一次性**」。**撤销 ≠ 放松**,风险性质与「改判据」完全不同。③ **A3(谓词分裂:幻觉检测硬门 / 语料一致性告警)虽更治本,但现在做是错的时机** —— 记入 forge 议题。A2(快照留档)不采:快照本身成可伪造面(KG-B10 同族),引出「谁签它」的新问题。**不追溯**:T010/T011 的 07-18 exit 0 是**当时语料下合法取得**,本次 STOP 是漂移非追溯否定,T012/T020/T021/T022 ship 合法性不动摇。
**诊断属实(producer 三步实测,consumer 认可)**:audit 的 200 条 source_ref 今日命中 **199**;唯一缺的 `TrojDiff`(CVPR 2023)是**真论文**只是掉出今日 top-200;同刻连跑两次 200 条**逐字一致**(排除 API 不确定性)。机制 = `sort=relevance_score:desc` + top-200 截断,排名尾部随索引 churn,而 `resolvable` 要求**严格超集** → 任何尾部抖动即 STOP。**同一 evidence bundle,07-18 exit 0、07-28 exit 2,10 天漂 1/200。**
**(B) ⚠ consumer 端对 §D KG-33 的根因更正(producer 判错落点 · IDS 第 28 条当初也判错)**:producer 称「template 本身写死 mac 字面量 = 设计缺陷 → 每份包恒带死路径」。**IDS 侧实查:范围判错了。** ① **IDS 侧 `framework/xenodev-bootstrap-kit/handback-validator/templates/handback.template.md` 用的是 `{{SOURCE_REPO}}` 占位符**(已修);② **`gen-handback.sh:512` 的 sed 列表里有 `s|{{SOURCE_REPO}}|…|g`**,且 `:426-433` 有 fail-closed 解析链;③ 修复出处 = commit **`5ebb42f` 「fix(006): 落地 P0 · IDS 侧去 mac 硬编码路径 + 防漂移守卫(forge v6 KG-26)」**;④ **XenoDev 侧 `lib/handback-validator/templates/handback.template.md`(及 001-radar-pA worktree 副本)仍是 mac 字面量**;⑤ **最锋利的一点:该 commit 同时新增的防漂移守卫 `check-no-hardcoded-env.sh`,在 XenoDev 侧 `find` 结果为空 —— 专门用来拦这一类的守卫,自己没被镜像过去**;⑥ 两侧 `gen-handback.sh` 差 **35 行**,不止这一处。→ **真根因 = forge v6 KG-26 的 P0 修复只落 IDS、从未镜像到 XenoDev**,即 **forge v4「landed ≠ 生效两态」在跨仓镜像面复发**(修复在 IDS 是 landed,在真正跑它的 XenoDev 不生效)。IDS 第 28 条当初推断「`gen-handback.sh` 有 fail-closed 链故这两包不是走那条链产的」—— **方向对、落点也错**(链是对的,只是那份副本根本没这条链)。
**(C) 镜像四项(按优先级)**:🔴 **a · 回写更正给 XenoDev 最急** —— 不做则 XenoDev 按「template 设计缺陷」这个错根因去改自己那份,与 IDS 已修版本**第二次分叉**;🟠 **b · 同步 `lib/handback-validator/`**(template 占位符化 + `SOURCE_REPO` 解析链 + `check-no-hardcoded-env.sh` 守卫),**先看完 35 行 diff 再定范围,不盲抄**(XenoDev 侧可能有合理本地改动,如其独有的 `scan-credentials.sh`);🟡 **c · 镜像同步机制本身归 006 forge**(真问题 —— 防漏的守卫自己漏了,这是最强证据);🟡 **d · KG 编号空间对齐**(本地条加 `XD-` 前缀)—— 现「KG-32」同文件两义、「KG-29」早已两义,且 **IDS `HANDOFF.md:80` 把 template 缺陷记作 KG-31 而本包记作 KG-33**,跨仓引用已在指错条目。**⚠ 本包 frontmatter 的 `to_source_repo` 是 producer 有意留错的活样本**(对照 `HANDOFF.md:4` 正确值 `/home/ys/codes/ideababy_stroller`);约束 3 用 `source_repo_identity` 三字段判身份,不受影响。
**(D) drift ① producer 漏跑 IDS 明令的门 —— 认定「载体不对」而非 producer 之过**:该指令只以散文形式出现在 HANDBACK-LOG 第 448 行 **Follow-up commits 行行尾**,不在决议列表、不在 task frontmatter、不在 SKILL §0 preflight 清单、不在 DAG,**无任何机器可读落点**。producer 按 parallel-builder §0.1 跑了 `depends_on` 门即起跑,三处证据(`T022.md` / `tests/red-green-log/T022.log` / `.eval/events.jsonl`)均无 preflight 痕迹。**KG-B4 当初解决的正是这问题的上一层(把前置从散文改成 `depends_on` 结构依赖),本次是同一个病在新的一层复发** —— 门本身机器化了,但「什么时候必须跑它」又退回成散文。→ 归 006:凡「起跑前必跑」的门必须落到 task frontmatter 或 SKILL §0 的机器清单,散文只作解释。**本轮 A 决议采 A1 后该指令已撤回,此路径自然消解。**
**(E) 同族第三例 → 通用前置归 forge**:① 009 **KG-43** 门槛冻结后**数学不可达**(上界 0.69756 < 0.70);② 001 **T022** judge 无下界 → **结构性不可达**;③ **本条** 可达但对同一证据重复判会**翻面** → **不可复现**。operator 此前已从 KG-43 归纳「判据可达性先于判据冻结」,本例补上缺失的另一半 **可复现性**。→ 送 forge 的通用前置:**任何机器判据冻结前须零成本证 ①可达 ②对同一证据可重复判同一结果;若输入含外部活体数据则必须显式声明有效期语义。** ⚠ **更一般的根 = 判据的「用途分类」缺失** —— 目前 SKILL/spec 里没有「**一次性验收门** vs **常驻/累计门**」的概念,于是同一判据被两种时间语义的用法混着消费而无人察觉。consumer 端发现**本条与第 30 条是同一个 bug 的两次发作**:preflight 被「一次性验收 vs 常驻」混用;「≥3」被 **O2(spec 自述长期累计锚)vs P2(一次性路径验证)** 混用。**故 forge 001 须一次裁四条(用途分类 / judge 下界 / OQ-A1-1 / 通用前置),分开裁 = 四次都只治症状。**
**(F) B1 build 编排决议(consumer 端依据 DAG + task 原文定)**:剩余 DAG = `T022 ─┬ T030 ┬ T040 ─ T041`(T030/T031/T032 三路并行 → T040 收口 → T041)。**T030/T031/T032 授权并行起跑** —— 已核**无一消费争议判据**(T030 JournalStore 记结论+`decision_delta`;T031 TasteStore 记标记;T032 run-ephemeral 守卫查语料复用;三者均不引用非豁免计数/抽样下界/OQ-A1-1),forge 怎么裁都不返工。**⛔ T040 / T041 不建,等 forge 001** —— 依据 T040 任务书原文:「把 spec §6 契约固化成 contract 测集(**违任一 = BLOCK gate**)…**O2 豁口契约(spec §1-O2 (a)(b)(c) · frozen-spec 层)**…用 **mutation 证 teeth**」,**其中 `(c)` 正是争议中的「≥3 条」**。现在建 = 给一条可能被改的规则装 BLOCK 级的牙并专门证明它咬得动,forge 一改就全部拔掉重装,而 T041 已建其上。**且零成本** —— T040 本就排在 T030/31/32 之后,这几天正在建它的前置。**merge 前轻量门保留(铁律 · 不可省)**:三 worktree 并行建 → **各自过 `/task-review` verdict ≠ BLOCK 再 merge** → 08-02 再做跨 task 深审(合规);全建完全 merge 最后一次性 review(**违反铁律**)。轻量门内容 = **真 provider 冒烟**(KG-30 自己的药方 · T031/T032 不碰外部 provider 则自动跳过)+ **T032 额外要求一次 mutation**(守卫类失败模式是静默的 —— 本批已踩三次「mutation 存活」/「删掉照样绿」/「看似承重实则不通电」,拆掉守卫看测试红不红,比事后审便宜得多)。
**(G) 攒批 review 的正确定位(consumer 端分析 · 修正常见误读)**:本项目吃亏最大的两个缺陷 —— **KG-29**(同一判断规则在多消费点各自实装互相漂移)与 **KG-30**(「LLM → JSON 消费者」这条边 4 个 task 一次没对真 provider 验过)—— **都是跨 task 缺陷,单 task 评审结构上看不见**(每个 task 单看都自洽)。故 **08-02 的批量 review 对本项目最贵的那类缺陷是更强的手段,不是更弱**;但必须**显式要求跨 task 审**(找:同一谓词多处实装 / 从没对真东西验过的边 / 没通电的守卫),否则攒批唯一的收益被浪费。
**(H) 本包诚实边界(consumer 认可)**:零代码改动 · 未烧 DEEPSEEK key(补跑只用免费 OpenAlex 检索) · 未擅自「修好」那道门(按决策矩阵回 IDS 决,防 V4) · 未追溯改动已 ship task · 诊断全部实测非推断。**评审门来源**:本包零代码改动故未走代码评审门,codex 配额墙仍在。

**Follow-up commits**: pending 本 session(IDS 侧:3 个 hand-back 包 + 第 29/30/31 条 entry 入库 commit,**未 push**)。**下一活 = XenoDev session `claude -w 001-radar-pA` 起 T030/T031/T032 三路并行**(⚠ **起跑前不再重跑 unlock-preflight** —— 本条 A 决议已撤回该指令,改校 journal PASS 记录;各 worktree merge 前保留 `/task-review` 轻量门 + 真 provider 冒烟,T032 额外 mutation)。**待办(时点触发 · 2026-08-02 codex 配额重置)**:① 7 task 跨 task adversarial-review(T021/FU-KG29/FU-KG30/T022/T030/T031/T032);② 起 `/expert-forge 001` 裁判据形态四条(用途分类 / judge 下界 / OQ-A1-1 / 通用前置)—— **阻塞 T040**;forge 完 → T040 → T041。**待办(攒批 · 不阻塞)**:框架级起 `/expert-forge 006`(KG-30 / KG-31 / KG-32 / 镜像无同步机制 / KG 编号对齐 / 存量条目)。**待办(即时)**:回写 KG-33 根因更正给 XenoDev + 同步 `lib/handback-validator/` 镜像。

## 2026-07-29T02:08:08Z · 001-radar-pA-20260729T020808Z

**Reviewed at**: 2026-07-29T08:40:32Z
**Tags**: feature(T030 journal 留档 + 后验查回 · O5 + O7 decision_delta)
**Severity**: low
**Operator decisions**:
- [ ] 修 PRD
- [ ] 修 SHARED-CONTRACT
- [x] **收悉 ship · 无需 IDS 决议**(无 spec 矛盾 / 无未授权接口 / C9 · NG-1b 未触碰)
- [x] **§3.2「FU 接线 evaluate → journal(一处调用)」→ 已被第 35 条撤回**,不据此排期
- [x] **§3.3 起 FU-A** —— 收口 T004 `journal/schema.py` 的 `splitlines()` + 无保护 `read_text` 两个 bug
- [x] **§3.4 跨 task finding 回放 → 归 `/expert-forge 006`**(框架级 · 见第 35 条 forge 分派)
- [x] **§3.5 08-02 后纳入 7-task 跨 task 深审**(沿用第 31 条既定范围)

**Operator note**: **(A) 交付与缺口都认**。守域(只动 `src/radar/journal/**`)是 IDS 定的,producer 如实记「生产 journal 至今 0 行」是对的诚实,不算交付缺陷。⚠ **consumer 端实查印证**:`out/briefing/` **目录根本不存在**、`out/journal/` 只有 `a1-selfcheck.jsonl` —— evaluate 全链真跑 **0 次**、评估 journal **0 行**,与包内自述完全一致。
**(B) 两条 P1 的性质认定**:① U+2028/2029/0085 被 `splitlines()` 断行,而 fail-closed 是**文件粒度** ⇒ **同文件健康行被一起拖下水**,且报出的行号指向一条 `json.loads` 能正常解析的行(诊断跟着失真);② 多字节截断产 `UnicodeDecodeError`(`ValueError` 子类,既非 `JournalCorruptError` 也非 `OSError`)⇒ **整整一类损坏绕过 fail-closed 契约**。本项目结论/理由/快照全中文(一字 3 字节),**不需要手工编辑就能触发**。两条都只在 **O5 后验那一刻**暴露 —— 即「写得进、读不回」,而 O5 的全部价值就在那一刻。
**(C) ⭐ 裁 B 之后 FU-A 的优先级上升,不是下降**(consumer 端补充 · 不在包内):第 35 条裁「读法 B · operator 手工 record」后,journal 成为 **operator 自己的决策档案**。**briefing 能重渲染,三个月前的判断不能重放** —— journal 从「工程洁癖」变成**唯一副本**,其读回鲁棒性是 O5「三个月后回看当时判断对不对」的**单点依赖**。故 FU-A 是本轮唯一即刻授权的 FU。
**(D) 但真跑不必等 FU-A**(两件事并行 · consumer 端核过):T030 交付的 `python -m radar.journal.cli {record,list}` 走 `JsonlJournalStore`,**两个 bug 都已修**;FU-A 管的是 T004 `schema.py` 那个**另一个消费端**。故第 33/35 条授权的真跑与 FU-A 无先后依赖。
**(E) 「同一对缺陷三处三种处置」认定为活的 KG-29 漂移**:T030 两个都修 / T031 只修了一个(早一轮补了 `UnicodeDecodeError` 包装)/ T004 一个没修 —— 同一个包、同一个 `out/journal/` 目录。这是 KG-29「同一谓词多消费端各自实装 = 无声漂移」在**同一批并行 task 内部**的即时复现,不是历史存量。FU-A 收的就是这条。
**(F) 评审 provenance 认可**:4 轮 22 findings 全修,**独立子代理 · 非 codex**,producer 已显式声明未产生也未冒充 codex verdict。**连续第 5 个替代路径 task**(T021 / FU-KG29 / FU-KG30 / T022 / 本批三个),配额墙至 2026-08-02 —— 评审债在册,08-02 补。
**(G) §4 方法论四条照单收**,其中两条 consumer 端认为值得回流 006:①「**测试用错误的代码路径产出了一个正确的事实**」(`raw[:-3]` 砍的是全 ASCII 行尾,走的是既有 JSON 分支;揭发它的不是人眼是覆盖率 99%→95%);②「**断言『诊断存在』不等于断言『诊断正确』**」—— `lineno = 999999` 的 mutation 在一个**专门为抓第①条而写**的测试下**仍然存活**,因为只断言了「有个『行』字」。行号**就是**那段修复的全部价值。

**Follow-up commits**: pending 本 session

## 2026-07-29T02:08:09Z · 001-radar-pA-20260729T020809Z

**Reviewed at**: 2026-07-29T08:40:32Z
**Tags**: feature(T031 taste 反馈标记留存 + 读回 · O6)
**Severity**: low
**Operator decisions**:
- [ ] 修 PRD
- [ ] 修 SHARED-CONTRACT
- [x] **收悉 ship · 无需 IDS 决议**(无 spec 矛盾 / 无未授权接口 / C9 · NG-1b 未触碰 / **v0.1「只留存不闭环」边界未越**)
- [x] **§3.2 FU-B(渲染面消毒上收为共享谓词)→ 缓,不在本轮起**
- [x] **§3.3「denylist → 类别/allowlist」写进 framework 层通用教训 → 归 `/expert-forge 006`**
- [x] **§3.4 08-02 后 codex 重跑**(并入 7-task 深审)

**Operator note**: **(A) v0.1 边界守得对**。R1-3 明写闭环自动调参是 v0.2,producer 未越界;`TasteMark` frozen domain 只有 `judgment_claim` + `aligned`,**同 claim 多标 = 多行并存无 latest-wins**,把歧义印给 operator 自己判而不替他挑 —— 这是照 OQ-A1-1「不在 XenoDev 当场定语义」的纪律,**认可**。极性必须显式给(不给任一极当默认,免得「忘了标」静默变成「标了那一极」往 taste 库灌噪声)同理认可。
**(B) ⭐ 最有价值的一条是方法论 —— 认定为本批最强 finding**:人读面消毒最初写成**六项 denylist**,而那张表是从**存储层**那个 bug 推出来的(`json.dumps` 不转义 ∩ `splitlines()` 会断行);可它要防的是**终端渲染**被伪造 —— **两个集合几乎不相交**。评审用真 VT 模拟器实测:那三个 Unicode 分隔符**终端根本不断行**(等于白中和),而真能骗人的 **VT / FF / ESC / BS / DEL / RLO / ZWSP / BOM 一个都没拦**;其中 **ANSI 光标上移 + 清行比换行注入更坏** —— 换行只是**多印**假行,ANSI 能**擦掉真行**(实测把 CLI 自己印的表头改写成「taste 标记: (empty) 0 tiao」)。
**(C) 🔴 而本仓早为同一威胁类付过学费 —— 这才是要回流 006 的真正理由**:`reconstruct/reconstructor.py` 的 `_serialize_untrusted_field` docstring 明写「R5 denylist 打地鼠 → R7 allowlist(拒整个补集)」,R8 还因白名单宽了一类吃过 codex high。**而新代码仍然从 denylist 起步。** ⇒ 那条教训**停留在单个文件的 docstring 里,没有变成起跑时就生效的约束** —— 这是 framework 层缺陷(与 KG-B4「门机器化了但『何时必须跑它』退回散文」同构),故归 006 而非 001。
**(D) 修法认可 · 复用而非重造是对的**:改判据为 Unicode 类别(Cc/Cf/Cs/Zl/Zp + noncharacter),**复用** `evidence/anchors.py` 既有类别表(**不在本层重造 = 正面执行 KG-29 教训**),本层只加 Zl/Zp 并说明为什么(那张表管**标识符合法性**,本层管**渲染面**,正确集合本就不同)。正文(汉字/ASCII/符号/变音符/emoji)一字不动;转义分隔符自身**单射**(穷举 11110 串 · 0 碰撞)。
**(E) FU-B 缓的理由(不是不做)**:① T031 **自己那一层已经修对了**,这是**整合**不是**活缺陷** —— 与 FU-A 收的「三处三种处置」性质不同;② 它的真价值要和 (C) 那条 **006 框架级约束一起兑现** —— 先上收谓词、后定约束,很可能返工;③ 现状三处分散在册不丢:`evidence/anchors.py`(标识符合法性 Cc/Cf/Cs)、`briefing/renderer.py` `_strip_deceptive_codepoints`(T022 已记同一条建议)、本 task `_one_line`。
**(F) 两条已知取舍照单收(producer 写成断言防下次被当 bug「修」掉,做法正确)**:① **ZWJ(U+200D)属 `Cf` 会被中和** ⇒ ZWJ emoji 序列显示拆开,有意为之 —— 评审给的硬理由不是「emoji 少见」而是「**消毒只在显示层**:store 读回逐字节相等、`--json` 保留原文,operator 永远取得回原文」(ZWJ 在天城文/阿拉伯连写里承重,这个理由才立得住);② **终端折行**仍可把 claim 文字推到物理行首(40 列下实证),**任何码点规则都关不掉**,要宽度感知截断 —— 但它擦不掉真输出、表头与汇总都在、`--json` 仍权威,弱于已修的那些。
**(G) §4.1 认定为跨 task 通用教训(与第 32 条 (G) 同族)**:「**守卫的测试可以在守卫被完全关掉的情况下通过 —— 而且在同一个 task 里连发三次**」(round-1 只断言表头 / round-2 截断码点表 / round-3 比较两条**本来就不同**的 claim),**每一次都落在最新加的那道守卫上**。终判据是:把 `_one_line` 换成恒等函数 → 16 条测试红,而那条**专门测它**的测试**照样绿**。⇒ 与第 31 条 (F) 给 T032 加 mutation 门是同一个理由,已验证必要。

**Follow-up commits**: pending 本 session

## 2026-07-29T02:11:37Z · 001-radar-pA-20260729T021137Z

**Reviewed at**: 2026-07-29T08:40:32Z
**Tags**: feature(T032 C9 run-ephemeral 守卫 · 交付物是边界表非 C9 证明)
**Severity**: medium
**Operator decisions**:
- [ ] 修 PRD
- [ ] 修 SHARED-CONTRACT
- [x] **收悉 ship · 五门 + 行为门入库**;**②在三 task 合并后如期变红并报出 6 处未声明读点**(merge commit `9ae402d`)—— 那正是它被设计出来要做的事,**认定为守卫真通电的正面证据**
- [x] **🔴 §3.1 采纳 —— T040 的 BLOCK gate 判据形态并进 `/expert-forge 001`**(第 3 项议题 · 见第 35 条分派)
- [x] **§3.2.1 FU-C(传递闭包审计)⛔ 本轮明确不起** —— 等 forge 裁完 C9 gate 形态
- [x] **§3.2.2 残留 FP 记录在案**(`csv.reader(io.StringIO(s))` 被计入 · fail-closed 方向 · 一行 `DECLARED_READ_SITES` 可消)
- [x] **§3.2.3 08-02 后 codex 重跑**(并入 7-task 深审)

**Operator note**: **(A) ⭐ 采纳 producer + 评审的共同判断:「这不是运气不好,是方法本身的上限」**。四轮评审**每一轮**都跑出一条**普通重构形状**的可用绕过 —— **包括针对紧邻的上一版** —— 四轮共五条,且**第五条的修复本身又引入第六个缺陷**:① 跨次语料池放进**已分类的非评估包**(`journal/`)+ 落**已登记前缀** + 用 `Path.open` → 四门全绿,三次同方向 dry-run 累积到 18 篇;② `sqlite3.connect(...)` 直接放进 `retrieval/`(名字白名单看不见);③ 语料池落在 `out/` **之外**(`.radar-cache/`);④ `a+` **增量扩展** + 走 **reconstruct** 入口;⑤ **bytes 路径让 ⑤ 全盲**(`str(b"/p")` = `"b'/p'"`,记录**看着有、比对时没有**,而 `dbm`/`shelve` 自己就传 bytes)。⇒ **名字键控的 AST 审计器面对 `getattr` / 别名 / C 扩展 / bytes 路径不可能完备;audit hook 也只看得见自己订阅的事件、自己包住的窗口、测试真驱动到的入口。枚举出来的那张边界,就是交付物本身。** 该句已写死进模块 docstring,认可。
**(B) 🔴 最锋利的一条,IDS 单独记为通用教训**:绕过 #1 当初被判「可接受」的**理由正是「② + ⑤ 双红」**;绕过 #5 打掉了 ⑤ 这半边 ⇒ **那条判断在无人知晓的情况下已经失效**。⇒ **「靠另一道门兜底」是一种需要单独验证的论证:写下「由 X 兜底」时,必须同时验 X 在这条具体路径上真的有效。** 这条与第 31 条 (E) 的「判据用途分类」同属「判据的元性质」族,一并送 forge 001。
**(C) 三处完全没覆盖的空白(不是残留)已在册**:分类边界**不是 import 边界**(① 对经 import 到达的读**永久失明**)· dry-run 把 retriever 换成 fake(真 `OpenAlexRetriever` 里的缓存**零行为覆盖**)· ⑤ 对「只枚举目录不 open」的读法**无痕**。
**(D) 🔴 §3.1 的核心裁断(本条 severity=medium 的唯一来源)**:**T040 的 BLOCK gate,PASS 只能表示「没有已知的 C9 漂移形状」,不能表示「C9 成立」。** 若 T040 spec 要求后者 = **判据不可达**,须先裁再焊牙。**认定为判据不可达同族第 4 例**,与在册三例并列:① KG-43(009 Layer-2)**数学**不可达(0.70 > 上界 0.69756);② T022 P2 **结构**不可达(judge prompt 无判断数下界);③ unlock-preflight **可达但不可复现**(活体 top-200 · PASS 是时刻不是状态);④ **本条 方法上限**不可达。前三例教训已入 memory:**判据可达性必须先于判据冻结**;本例是其自然延伸 —— **冻结判据前,先问「这个判据能被什么东西证明?」**
**(E) ⛔ FU-C 本轮不起的理由(consumer 端主动加严 · 比 producer 建议更保守)**:FU-C 的主题(**C9 gate 能证明什么**)**正是 forge 001 要裁的那一条**。现在建 FU-C = **给未定的规则焊牙** —— 这正是本批自己反复抓出的失败模式:第 31 条 (F) 拿它拦下 T040、第 35 条 §2.4 又拿它拦下 P2 契约测,**再犯就是同一 session 内第三次复现**。且 producer 自己已写明「真修法要给现有跨包复用逐个开例外,**超出本 task**」—— 范围本就不清。已在册的具体路径不丢:`graph/builder.py` 与 `reconstruct/finalize.py` 已 import `credibility.gate`,而 `credibility/audit_channel.py` 有 3 处读上次 run 的 audit 产物 —— **今天没连起来,但门 ① 对这条路径永久失明**。
**(F) §4 方法论四条全部照单收,两条送 forge 006**:①「**修误报可以换来漏报,而漏报在守卫上贵得多**」—— 修「参数遮蔽被误报」时用了整模块 shadowed 集合,于是**另一个函数**里一句 `connect = None` 就静默关掉整份文件的检测;**FP 让人烦(还看得见),FN 让人以为干净**(改成作用域感知后两头都对);②「**测试会把 bug 固化成契约**」—— 绕过 #4 的一半根因是上一轮的测试**明写** `open(...,'a',...)` 不算读,而 C9 的文字一直写着「读**以及 append 式增量扩展**」,**实装与它自己的 docstring 矛盾了整整一轮,而测试站在错的那边**。③ 另记:「⑤ 是 API 无关的」这句被证伪后在**三个地方**残留,其中函数 docstring **正是 T040 作者会读的那一份** —— 文档措辞是交付物的一部分。

**Follow-up commits**: pending 本 session

## 2026-07-29T08:21:20Z · 001-radar-pA-20260729T082120Z

**Reviewed at**: 2026-07-29T08:40:32Z
**Tags**: spec-gap(§7-P2 journal 归属双读法 · 撤回并更正第 32 条包 §3.2 的建议)
**Severity**: medium · **零代码改动包**
**Operator decisions**:
- [ ] 修 PRD
- [ ] 修 SHARED-CONTRACT
- [x] **⭐ 裁「读法 B」· operator 手工 `record`,`journal list` 是验收读回** —— XenoDev **零代码**,T030 交付即刻可判绿
- [x] **修 XenoDev spec(跨仓 · 信息式)**:§7-P2 验证命令列补一句消歧
- [x] **撤回登记受理**:第 32 条包 §3 第 2 条**前半句「一处调用」作废**;后半句「请勿判绿」保留但**理由换成「归属没定」**;该包其余部分(§2 / §2.5 / §4 及 §3 的 1/3/4/5 条)**不受影响仍然有效**
- [x] **⭐ 授权真跑起 O7 时钟**(与 forge 解耦 · 见 (D))
- [x] **forge 议题分两仓**:001 带 3 项 / 006 攒 2 项(见 (E))
- [x] **§3.6 08-02 深审带上本条歧义作独立核查项**

**Operator note**: **(A) ⭐ 裁 B · 三条独立证据同向,读法 A 无任何正面依据**。consumer 端**逐行独立核过 producer 引用的每一处字面**,全部属实,并补一条 producer 没引用的独立佐证:
① **IDS 侧 PRD `discussion/001/001-radar/001-radar-pA/PRD.md:42`**(producer 未引用 · consumer 端补):「作为 lab lead,**我能把**评估结论(投/观望/不投 + 日期 + 理由)留档进 journal」—— **主语是 operator**,不是系统;
② **spec §1-O5**(`spec.md:92`)措辞是「**可**留档 journal」,不是「自动留档」;
③ **`decision_delta` 在类型上机器不可观测** —— spec §6 O7 验收行(`spec.md:267`)逐字「该次评估**实际改变 operator 投/观望/不投**」,这件事发生在人的决策里、不在任何产物上,evaluate **没有任何输入能观测它**;而 O7 被 spec 标为「**最强产品成功信号**」(`spec.md:94`),不是可糊过去的边角字段。
⇒ 读法 A 的**唯一**依据是「验证命令列没写 `record`」这一处**沉默**,而沉默恰恰被读法 B 更好地解释(record 是人的动作,不在自动链内)。
**(B) consumer 端对「三填三不填」的加强(不在包内)**:producer 说 `RadarRing` 四环与 `conclusion` 三值「词表差异只是表征」,方向对但仍偏弱。**实查 `domain/__init__.py`:`radar_ring: RadarRing` 挂在 `Judgment` 上(每份 briefing N 条判断各带一个),`JournalEntry.conclusion` 是整次评估一条 —— 两者是层级差,不是词表差。** ⇒ 读法 A 要发明的**不是一张映射表,而是一条聚合语义**(取众数?取最高环?按证据数加权?),而 spec 从未定义 —— 正是 OQ-A1-1 纪律所禁止的「在 XenoDev 当场定语义」。`JournalEntry` 六字段 `model_config = _FROZEN` 亦已核实。
**(C) 落地位置更正(producer §3.2 写得不准 · consumer 端更正)**:producer 建议「`/scope-inject` 在 §7-P2 补一句」—— **不对**。§7-P2 在 **XenoDev `specs/001-radar-pA/spec.md`**,不在 IDS PRD;M3 后 IDS 不产 specs/(SHARED-CONTRACT §6 v2.0)。⇒ 正确动作是**跨仓改 XenoDev spec 验证命令列**,与 009 第 28 条「直改 XenoDev spec/SLA 不碰 C6」是同一先例。**补的那句**:「`<cli> journal record` 由 operator 读完 briefing 后手工执行,**不在自动链内**;`journal list` 是验收读回」。
**(D) ⭐⭐ 授权真跑起 O7 时钟 —— 与第 31 条「P2 物证重建暂不授权」不冲突,但必须靠「用途分类」才分得开**(consumer 端主动提出 · 不在任何包内):
- **实况(consumer 端实查磁盘,非推演)**:`out/briefing/` **目录根本不存在** ⇒ evaluate 全链真跑 **0 次**;`out/journal/` 只有 `a1-selfcheck.jsonl` ⇒ 评估 journal **0 行**;`out/reconstruct/` 有 2 份真跑(07-17 校准 + 07-18 解锁)。
- **spec §1-O7 是本批唯一带墙钟的验收项**:「**3 个月内**完成 **≥5 次**真实**新方向**评估,其中 ≥1 次实际改变 operator 投入决策」。当前 **0/5**,且 spec **未定义这 3 个月从哪天起算** —— 时钟根本没起,每推一天窗口整体后移一天。
- **阻塞类型不同**:§1-O2 (c) / C9 gate 判据 / §7-P2 归属都是**决策阻塞**(一场 forge 就解);**O7 是日历 + 计数阻塞,任何 forge 决议都解不开,只有真跑能解**。
- **⚠ 与第 31 条的关系**:第 31 条「暂不授权」的是**为 P2 验收做的物证重建**,理由「等 forge 裁完与新跑合并,只烧一次 key」—— 该理由在 **P2 用途下仍然成立、继续有效**;但在 **O7 用途下不成立**:O7 本就要 ≥5 次**不同新方向**,根本合并不了,「只烧一次 key」在 O7 语义下无意义。⇒ **同一个「跑一次 evaluate」的动作,在 P2 验收用途下该等 forge,在 O5/O7 累计用途下不能等。这正是第 31 条 (E) 自己提出的「判据的用途分类缺失」根因的又一次应用 —— 这次应用在动作侧而非判据侧。**
- **决议**:授权**现在跑第 1 次真 evaluate(新方向)** + **定下节奏**(如每周 1 个新方向),而非单次一事一议。**批量补跑会把 O7 从产品信号降成刷计数** —— O7 要的是 5 次**真实**决策,不是 5 行 journal。跑完 operator 读 briefing 后手工 `journal record`,**顺带实证裁 B 的整条链路**。
- **诚实边界**:① 带 **per-run 自证义务**(PRD v1.5 ①:同一验收事件内同 stem B′+D′ 自证);② 若 forge 改了 §1-O2 (c),这次跑的 briefing 在 **P2 用途**上可能作废,但在 **O5/O7 用途**上**不作废** —— journal 行记的是 operator 决策,不依赖证据链抽样判据;③ 烧 DEEPSEEK key。
**(E) forge 议题分两仓(per CLAUDE.md 铁律「框架级只走 006」)**:
- **`/expert-forge 001`(08-02 后 · 阻塞 T040)带 3 项,一个主题「判据冻结前必须先证什么」**:① **T040 C9 BLOCK gate 判据形态**(第 34 条 §3.1 · 方法上限不可达);② **§1-O2 (c)「≥3 条非豁免判断」**(第 31 条既定 · 结构不可达);③ **「唯一可读性」补进可达性族**(本条 §2.5 · 见 (F))。⚠ 第 31 条 (E) 既定的「用途分类 / judge 下界 / OQ-A1-1 / 通用前置」四条**不被本次分派取代,仍在同一场 forge 内**;本次是**追加**第 ①③ 项并明确「必须一次裁完,分开裁 = 只治症状」。另追加第 34 条 (B)「靠另一道门兜底是需要单独验证的论证」入同一族。
- **`/expert-forge 006`(攒批 · 不阻塞)追加 2 项**:① **跨 task finding 回放机制**(第 32/33 条共同提出:N 个并行 task 共享代码形状时,任一评审的 finding 在 ship 前对其余 task 逐条回放;**补法不是共享评审者** —— 那会重新引入独立评审要打破的 monoculture;一次就能抓到 T030/T031/T004 三个实例);② **「denylist → 类别/allowlist」写成起跑时生效的约束**(第 33 条 (C):本仓已在 `_serialize_untrusted_field` 付过 R5→R7→R8 的学费,而新代码仍从 denylist 起步 —— 教训停在单文件 docstring 里没变成约束,与 KG-B4 同构)。沿用第 31 条既定 006 攒批清单(KG-30/31/32 / 镜像无同步机制 / KG 编号对齐 / 存量条目),**不替代**。
**(F) 「唯一可读性」= 判据可达性族的第三个半(本条最大的方法论增量)**:在册四例 —— ① KG-43 门槛 0.70 > 上界 0.69756(缺**可达性**);② T022「≥3 条非豁免判断」judge 无下界(缺**结构可达性**);③ unlock-preflight 活体 top-200 尾部 churn(缺**可复现性**);④ **本条 §7-P2 journal 归属双读法(缺唯一可读性)**。⇒ **一条验收行,若其「产物」列与「验证命令」列能推出两种互斥实装,那不是待办事项,是没写完的定义。** 这条**比 ①②③ 更隐蔽,因为两列各自都读得通,只有把它们并起来问「谁来写这一行」才暴露** —— consumer 端认可这个判断。
**(G) 「为什么现在提而不等 T040」认可**:T040 要给 §7-P2 建契约测,**按哪种读法建,测的东西完全相反**(按 A 建 → 测「evaluate 跑完 journal 自动多一行」→ **现在必红**且逼着改 evaluate;按 B 建 → 测「record 之后 list 读得回」→ **现在已绿**)。**归属未定时建测 = 给一条还没定的规则焊牙**,与 IDS 拦下 T040 的理由完全同构 —— 只是这条上轮没被发现,**因为它藏在两列之间而不是写在一句话里**。
**(H) 评审债显式在册**:本包**未经 cross-model review**(零代码 · 结论全部可由 spec/domain 字面逐行复核 · 按 SKILL 不触发 review 门 · 不冒充任何 codex verdict)。**consumer 端已独立复核全部引用行,结论属实,不依赖 producer 自述。** 08-02 深审须**把本条歧义作独立核查项**带上 —— 它恰好是「四轮独立评审 × 3 个 task 都没抓到」的那一类:**评审看 diff,而这条不在 diff 里**。
**(I) §4 方法论第 1 条认定为本批最高价值的一条,送 forge 006**:「**评审看的是 diff,而最贵的错误可能不在 diff 里**」—— T030 走了 4 轮评审、22 findings 全修,没有任何一轮碰到 §3 的建议,因为评审对象是**代码改动**,而「给 IDS 的下一步建议」是**散文**,不在 diff 里也没有测试能红;**它却是那份 hand-back 里唯一会让 IDS 花钱的部分**。⇒ **hand-back §3 的每一条建议,应当和代码一样被要求给出可复核的依据行号。** 本包每条论断都标了 `file:line`,是按这条自我要求写的 —— consumer 端实测**因此才能逐行复核**,机制有效,建议固化进 §6.3 schema。另收 §4.2「**估『接线』工作量前,先把被接的那个类型的每个必填字段逐个问一遍『调用方手上有没有』**」—— 六个字段三个没有,这个检查**一分钟**就能做完,而它推翻了整条建议;§4.4「**撤回要撤得比原文醒目**」—— 单独成包 + 逐字引用 + 明写哪半句撤,做法正确,**一条被安静更正的错误建议和没更正没有区别**。

**Follow-up commits**: pending 本 session

## 2026-07-30T03:44:14Z · 001-radar-pA-20260730T034414Z

**Reviewed at**: 2026-08-02T01:03:59Z
**Tags**: drift(FU-A jsonl 读回谓词三处收口 · 登记表机器强制)
**Severity**: medium
**Validator**: 6 约束 consumer 模式 **PASS**;`ids_verdict_evidence` 父键不存在 → verdict-evidence 语法预检**跳过**(本包非 codex-verdict 包,正常)
**Operator decisions**:
- [ ] 修 PRD
- [ ] 修 SHARED-CONTRACT(**但 XD-41 建议 3 会动 §6.3 schema,随 006 攒批一起裁**)
- [x] **追认 §2.4 三处越域**(不算越权)· XD-39 / XD-40 归 `/expert-forge 006` 攒批
- [x] **⭐ 要求 XenoDev 补产 R1–R5 的 hand-back 包**(通道缺口 · 见 (B))
- [x] **XD-41 / XD-42 / XD-43 全归 006 攒批**,XD-41 / XD-43 标 **high 优先**
- [x] **⭐ O7 时钟 item b 现在跑**,base 取 **post-R5 HEAD `df5ce24`**(见 (E))

**Operator note**: **(A) ⚠⚠ 本包在决议时已是 stale snapshot —— 这是 consumer 端实查发现的、包本身无从知道的事实,且它比包内任何一条都重要**。本包写于 XenoDev worktree `5399661`+`04f2e79`(2026-07-30 11:43 +08)。**其后 07-31 16:27–17:47 codex 配额提前恢复**(包 §2.5 称重置 08-02),又落 5 个 commit `78e3e8f`→`4743ccd`→`1cf10e9`→`4a4c5f5`→`df5ce24`(codex 补跑 R1–R5)。consumer 端实查 `git log --date=iso-strict` + `dogfood-backlog.md` + `review-log/backfill-e89860e-2026-07-31-round{1..5}.md`,核实:
- 补跑 scope 取**累积区间**(base `e89860e` = 最后一个真过 codex 的代码 commit),**4 轮共 21 条 finding · 11 条 high**;
- 测试数 **938 → 1006**(R4 后 998,R5 +8);
- backlog 新增 **XD-41 / XD-42 / XD-43**(两条 high)⇒ 本包 §3.1「本轮新增 2 条」**已过期**;
- **R1–R5 从未产 hand-back 包** —— IDS 侧 `discussion/001/handback/` 最新仍是本包(07-30)。

⇒ **本条决议同时覆盖本包与 R1–R5 的既成事实**,并按下面 (B) 要求补通道。**本包 §2/§2.3/§2.6 的交付与三条自我推翻仍然有效**(它们描述的是 FU-A 那次交付本身,不被后续轮次推翻);**失效的只有 §2.5 的可信度自评与 §3.1 的「新增 2 条」计数**。

**(B) ⭐ 要求补产 R1–R5 hand-back 包 —— 理由不是流程洁癖,是三条实质依赖**:
1. **XD-41 是本轮最贵的一条,而它的一手证据(21 条 finding 的分类与具体内容)只存在于 XenoDev 的 review-log + commit body 里,IDS 侧只有 backlog 散文**。forge 006 要裁「替代路径可信边界」,拿散文裁 = 又一次在没有物证的情况下定判据(与 KG-43 同型)。
2. **R5 自陈「修法未经 codex 复核」**(operator 定的 5 轮上限用尽),且 **R5 四条 high 里三条是 R4 修法自身的残留绕过** —— 这是一笔**显式在册但没有机器落点的债**,必须进 hand-back 才在 IDS 侧可见。
3. post-R5 HEAD `df5ce24` 是下面 (E) O7 真跑的 base,**IDS 侧现在没有任何包记载这个 base 的状态**。
   ⇒ 补包应含:21 条 finding 分类 · post-R5 HEAD 状态(1006 passed / mutation / ruff)· 「R5 未复核」的显式挂债 · 是否值得起第 6 轮的建议。

**(C) XD-41 认定为本批最高价值的一条,且它给「连续第 6 批替代路径」这件事结了账**。本包 §2.5 自称「不得记为 codex 门已过」—— 态度正确,但**当时无从知道欠了多少**。现在知道了:8 个 task-unit(T021 / FU-KG29 / T022 / FU-KG30 / T030 / T031 / T032 / FU-A)连续 6 批走独立子代理路径 merge,codex 一恢复 4 轮抓出 21 条 / 11 条 high,且抓出的是**「产物能说谎」**这一族:
- 非 dry-run 路径接受注入的 fake ⇒ briefing 表头照写「全链真跑 · PPV P2 终点产物」(**子代理 4 批没看出来**);
- 公共 renderer 的来源声明是**默认 False 的布尔** ⇒ **什么都不做就等于声称真跑**,连测试自己都在批量铸造这种产物;
- **`journal record` 只校验「可读 + 非空」⇒ README 能成为 O5/O7 journal 行**;
- 两个仓级 shell 门(task-preflight / unlock-record-check)**此前零测试覆盖**。
XD-41 归的三条成因 consumer 端**认可且不打折**:① **子代理与被审代码同源同上下文** —— 它读的是同一批文件与同一套注释,而那些注释正是作者的自述(本轮多条 finding 直接指出**注释与代码不符**);② **子代理不跨 task-unit 看** —— 最贵的几条恰恰是跨批次才可见;③ **「verdict ≠ BLOCK」在替代路径上偏松** —— 6 批全是 needs-attention 照样 merge,**needs-attention 事实上等价于放行**。
⇒ 这是第 35 条 (H)「评审债显式在册」的**代价实测**,也是**第七次「推演≠真跑」**的变体:这次推演的不是代码行为,是**评审强度**。三条建议(补审债标记 + 累积区间 / 替代路径下判据收紧一档 / hand-back schema 加 `review_path: codex | fallback`)全部随 006 攒批,**第 3 条动 SHARED-CONTRACT §6.3,与第 35 条 (I)「§3 每条建议须给可复核依据行号」同批落**。

**(D) XD-43(high)是 IDS 自己下的单跑成了空转,必须在 006 与 KG-B4 并案**。`scripts/task-preflight.sh` 是 IDS 第 29 条要的机器可读落点(task 起跑前置写进 frontmatter,脚本逐条真跑,任一非 0 → hard-block)。本轮把解析器从 fail-open 收到 fail-closed 用了 **R1/R2/R3 三轮**,而 **codex 每一轮都同时指出:即使解析器完全正确,也没有任何入口强制调用它** —— parallel-builder SKILL 的 preflight 清单里没有这一行 ⇒ **这道门从未被执行过**,它宣称的 hard-block 保证不成立。XenoDev 按铁律不当场改 SKILL(正确),接线归 IDS。
⇒ 与 **KG-B4「机器道 STOP 必须真 wire 成退出码」是同一条链的前后两段**:KG-B4 讲「门要真 wire」,XD-43 讲「wire 了但没人调用」。**006 上必须并案裁,分开裁 = 只治症状**(与第 35 条 (E) 对 forge 001 三项的要求同型)。另收 XD-43 建议 2:**ship 门也要验一条与当前 task/spec 内容绑定的成功执行记录**(task id + commit + 命令 + 退出码 + 内容摘要),否则「起跑时跑过」与「ship 的是同一份内容」之间仍有缝。
**XD-42(low)**随批:代码里写死的「已记 KG-34」指向的是另一件事(migration 硬 checklist),**编号撞车后旧引用没回填 ⇒「记了 backlog」这句话本身不可核验**。采纳其建议 2 的形态 —— **代码里不写编号,只写「已记 dogfood-backlog(搜:<关键词>)」**,编号会变标题不会。这是「文档声称跑在代码前面」的**变体:文档声称跑在另一份文档前面**。

**(E) ⭐ O7 时钟 item b 现在跑,base 取 post-R5 HEAD `df5ce24` —— 且 codex 补跑恰好改变了这个决定的性质**。第 35 条 (D) 已裁「O7 是日历 + 计数阻塞,任何 forge 决议都解不开,只有真跑能解」,该理由**继续有效**;本条补一层**新理由**:
- XD-41 抓出的 **「`journal record` 只校验可读 + 非空 ⇒ README 能成为 O5/O7 journal 行」**,以及 R5-F2 **「真跑横幅未绑定固定槽位 ⇒ 第 3 行明写 DRY_RUN_FAKE、正文夹带真跑横幅的自相矛盾快照照样能成为 O5/O7 的 P2 journal 行」** —— **两条打的都正是 O7 这条链**;
- ⇒ **若按 07-30 的 base 跑,会造出一条「机器无从证伪」的 O7 行**;按 `df5ce24` 跑,journal 行的来源声明才真的被校验。**codex 补跑把「现在跑」从「不得不跑」升级成了「现在跑更干净」**;
- **诚实边界(照第 35 条 (D) 原样承继)**:① 带 per-run 自证义务(PRD v1.5 ①);② 若 forge 001 改了 §1-O2 (c),这次 briefing 在 **P2 用途**上可能作废,在 **O5/O7 用途**上**不作废**;③ 烧 DEEPSEEK key;④ 跑完 operator 读 briefing 后**手工 `journal record`**,顺带实证第 35 条裁的「读法 B」整条链路。
- **⚠ 残留风险如实记**:R5 四条 high 的修法**未经 codex 复核**,而其中 F2(真跑横幅)/ F4(URL canonicalizer 折叠大小写敏感分量,影响 `graph/builder.py` 别名回退锚点)**正落在 briefing 产物可信度面上**。⇒ **本次真跑的 briefing 在 O5/O7 计数用途上有效,但若第 6 轮 codex(若起)推翻 R5 修法,该次 briefing 的 P2 用途需重判**。这是「用途分类」第三次应用(第 31 条判据侧 → 第 35 条动作侧 → 本条**产物侧**)。

**(F) 追认三处越域的理由(与本包 §3.2「不要求裁越域」的自我克制并不冲突,但 IDS 主动裁掉它)**:包 §2.4 标题写「需 operator 裁是否越权」而 §3.2 写「不要求裁越域」—— **同一份包里两处口径不一致**,虽无害但正是本仓反复踩的「两列之间读得出两种意思」形态(第 35 条 (F)「唯一可读性」)。IDS 一次裁死:**追认,不算越权**。判据:三处全为诊断/文档面 · 零判定分支改动 · 不碰 KG-B10 spine 冻结面 · 可单独 revert;且 `cli/unlock_preflight.py` 那处**不接住就等于 FU 目标只兑现一半**(新造的 typed 错在真实路径上仍以 traceback 投递),`journal/cli.py` 那处**不修则本包在 `taste/store.py` 新写的注释是假陈述**。⇒ **「不修会让本包自己的文档变成假陈述」应当作为越域的正当理由之一写进 006 攒批**,它比「范围洁癖」更该被保护。
**顺带认可包内「不采纳评审建议退 2」的裁断**:「journal 文件坏了」是**输入损坏**,退 1;「a1 谓词判 STOP」是门的**判断**,退 2。混进 2 会让 parallel-builder preflight 把「文件坏了」读成「门判了 STOP」—— 这是**退出码语义的用途分类**,与 (E) 同源。

**(G) 本包 §2.6 三条自我推翻仍然是本批方法论增量,不因 stale 而打折**:① **清空 `JSONL_FACES` → `916 passed, 5 skipped` 且 rc=0 全绿,15 个用例一个没跑** —— 根因是 pytest 把空参数化报 **skipped 而非 failed**,而 ship 门只看 `failed` 与 rc,**覆盖率、ruff、人眼全都放过它**;② **启发式判据放在「完备性」这一环上必然 fail-open**(评审真落地了一个 `journal/method_pool.py` 反例,全量 932 passed);③ **在收口 KG-29 的补丁里又犯了一次 KG-29**(自写 mode 取参把路径字面量当 mode 解析,而 `lifecycle/ephemeral.py` 逐字记过这个坑并已解决)。**三条都只有 mutation / 独立评审抓到,没有一条是自查发现的** —— 这与 (C) 里 XD-41 的结论同向:**自评估的上界由「评估者与被评者的独立性」决定,不由评估的认真程度决定**。

**(H) 通道自证与既有 commit 对齐**:本包 KG-33 第 7 次复现(`gen-handback.sh` 的 `to_source_repo` / `workspace.source_repo` 仍写死 mac 字面量,producer 已手改;6 约束 validator **producer 模式对此不报错** ⇒ 该字段无机器门)—— 归 006 既定攒批,不再重复受理。另记:**第 32/33/34/35 条已落 commit `7e9e9fe`**(其 entry 内 `Follow-up commits: pending` 因 append-only 不回改,在此登记)。

**(I) ⚠ 本次 session 的 worktree 规约 warn(不阻断)**:本次 `/handback-review 001` 在 **`main` 分支**跑,不在 `001` worktree —— 与 CLAUDE.md「Session-per-idea worktree 规约」不匹配,按 P0 **warn 型 preflight** 记录不拦截。同时工作区存在 **009 的未提交改动**(`discussion/009/009-pM3prime/PRD.md` + 009 的两个 hand-back 包 + 009 HANDBACK-LOG)—— **本条决议的 commit 严格只收 001 路径,不夹带 009**,以免复现该规约要治的混线。**这是该规约上线后第 1 次记录到的 mismatch**;升级判据(hook 硬拦)是复发 ≥2 次。

**Follow-up commits**: `543b4df`(本条决议 + 本包入库,严格只收 001 路径)· 后续 XenoDev 侧补包 / O7 真跑 commit 待回填

## 2026-08-02T01:21:27Z · 001-radar-pA-20260802T012127Z

**Reviewed at**: 2026-08-02T08:04:29Z
**Tags**: drift · practice-stats(codex 配额恢复后对累积区间 `e89860e..df5ce24` 补跑 R1–R5)
**Severity**: high
**Validator**: 6 约束 consumer 模式 **PASS**;`ids_verdict_evidence` 父键不存在 → verdict-evidence 语法预检**跳过** —— ⚠ 本包**刻意不挂**该块且给了理由,consumer 端认可(见 (B))
**Related task**: `codex-backfill-audit-R1-R5`
**Operator decisions**:
- [ ] 修 PRD
- [x] **修 SHARED-CONTRACT §6.3**:加 `review_path` 字段,但**改形状**(见 (C))· 随 006 攒批落
- [ ] 修 XenoDev spec(本批不碰 · spec amendment 攒到 forge 001 后由 spec-writer 一次性落)
- [x] **⭐ XD-41 标题数字回填 + §2.6 scope 证据入 forge 006**(见 (A))
- [x] **XD-43 归 forge 006**,与 KG-B4 并案(第 36 条 (D) 既定,本条确认)
- [x] **R4-F4 目录 fsync 守卫冲突并入 forge 001 T040**,不单开条目(见 (D))
- [x] **⭐ 第 6 轮 codex:采纳「窄 scope」,但换触发判据**(见 (E))
- [x] **XD-42 维持不修**(第 36 条既定)· **`REVIEW-LOG.md` latest pointer 过期追加进 006**(见 (F))

**Operator note**: **(0) 第 36 条第 2 项的交付已收到,通道缺口闭合。** consumer 端**不照抄包内自述**,对可机器复核的部分做了独立实算:5 份 `review-log/backfill-e89860e-2026-07-31-round{1..5}.md` 的 sha256 与 §4.4 表**逐条命中**;`grep -cE '^- \[high\]'` / `'^- \[medium\]'` 逐轮实测 = R1 5/1 · R2 4/1 · R3 3/2 · R4 3/1 · R5 4/0 ⇒ **19 high / 5 medium / 24 条**,与 §2.2 表一致;`dogfood-backlog.md` XD-41(:1486)/ XD-42(:1532)/ XD-43(:1568)三条目实存;HEAD 链 `df5ce24`→`c53b6a6`→`9444e09` 属实。**⇒ 本包的数字面可信,不是散文自述。**

**(A) ⭐ XD-41 数字更正采纳,且这条更正本身比数字更重要**。XD-41 标题原文(`dogfood-backlog.md:1486`)consumer 端实读 = 「4 轮抓出 21 条(其中 11 条 high)」;真值 **5 轮 24 条 / 19 high / 5 medium**,「21」是**闭合数**被误当 finding 数,「11 high」无任何对应口径。⇒ **回填标题**。
**为什么这条要单独记**:第 36 条 (C) 已用「21 条 / 11 high」这两个数写进 IDS 决议,forge 006 本来要拿它裁「替代路径可信边界」。**连「记录 finding 数」这件最机械的事,不做机器计数都会漂** —— 这是「文档声称跑在代码前面」在**统计口径**上的一次实例,与 XD-42(文档声称跑在另一份文档前面)同族。
**§2.6 五条一手证据全额采纳,且认可其归因方式**:包给每条「产物能说谎」都附了**「6 批子代理为什么结构上看不出来」**,成因逐条落在 **scope 定义**上 —— ① 子代理沿 task 验收条目走,而验收表本身漏了一个方向(R1-F1:验收只写「dry-run 不许声称真跑」,**反方向没人问**);② 每批独立、结构上不做「复核上一轮修法」(R2-RF1);③ 不跨 task-unit(R3-F3 要连 T022 产物一起看);④ **不在任何 task `file_domain` 里的仓级件在结构上不可见**(两个仓级 shell 此前零测试覆盖)。
⇒ **forge 006 上 XD-41 的判据必须落在 scope 定义,不是「换个更强的评审者」。** 包 §2.6 ⑤ 补的那条尤其重:同一道 fail-open 门被**连续五轮**逐层收紧,每轮都是**合法 YAML 的新写法**(flow 序列 → 引号键 → 转义键/合并键 → 整体缩进 → 注释行)⇒ **「一次评审放行」这个前提对 fail-open 类缺陷本身不成立,与评审者强弱无关。** 另收两条硬证据:`test_briefing.py` 5 处构造点**全部默认铸造「全链真跑」产物**、`test_journal_cli.py` 成功夹具就是「`# briefing` + 任意文本」—— **测试自己在铸造 / 演示那个洞,而子代理看的正是「测试是否通过」**。

**(B) 认可 §4.4「不挂 `ids_verdict_evidence`」的裁断,并把它记为通道设计的正面先例**。理由链 consumer 端复核成立:7 字段里 `codex_model` **无法诚实填写**(R1–R5 产物是 companion 原始 stdout,无 REVIEW-LOG frontmatter ⇒ 不含 model;`~/.codex/sessions/` 07-31 零 rollout;`~/.codex/config.toml` 的 `gpt-5.6-sol` 是**今天**的配置,不能证明 07-31 跑的是它 —— 与 [[codex-version-model-config]] 记的 07-23 改软链时间线一致)。而 `validate-verdict-evidence.sh:9-11` 自己明写「接受语法合法但**未经证伪**的 evidence metadata」⇒ **挂一个填不实的块正是该 validator 警告的用法**。
⇒ **「字段填不实时不挂块 + 另给可机器复核的替代证据表」应当写进 §6.3 schema 作为正当行为**,否则下一个 producer 会为了过预检而发明一个 model 名。这与本仓「needs-attention 事实等价于放行」是同型风险的反面 —— **语法门能被满足,恰恰是它最危险的时候**。

**(C) ⭐ `review_path` 采纳但改形状 —— 单枚举表达不了本包自己**。包 §3.1-4 建议 `review_path: codex | fallback`。**本包就是该形状的反例**:它覆盖 8 个 task-unit,**全部 ship 时走 fallback、事后才被 R1–R5 补审**,二值填哪个都是错的。⇒ 落 §6.3 时定成:
- `review_path: codex | fallback | fallback-backfilled`(三态)
- 外加 `review_debt: [<task ids>]` —— **哪些 unit 至今没有一手评审证据**
否则字段上线后 IDS 读到的仍是一个**压平了真实状态的值**,与现在读散文差别不大 —— 那就白改了一次 schema。本条与第 35 条 (I)「§3 每条建议须给可复核依据行号」同批落。

**(D) R4-F4 并入 T040 裁,不单开**。包 §2.5.3 把三条路各自的问题写死了,consumer 端认可**且认为这个自我否决本身是本包第二有价值的部分**:① 给 C9 门①开豁免 = **为了让自己刚写的代码过而给安全门加豁免**;② 挪 helper 到非评估模块 = **主动利用门①对 import 的已知失明去绕过它**(比 ① 更坏);③ 改门①判 `os.open` flags = 改的正是**躺在 T040 待裁清单上**的 C9 契约。
⇒ 三条路都通向「判据未定时先动判据」,**上交是唯一诚实解**。裁定前如实记:`briefing/` 产物在崩溃/掉电场景下**无持久性保证**(非 blocking)。落点已在 `src/radar/briefing/writer.py:85-97` 逐条写明,T040 裁时直接读代码即可,不必回溯本包。

**(E) ⭐ 第 6 轮:采纳「窄 scope」形态,但**触发判据从「forge 001/006 裁完之后」改为「**第一次真打算判 P2 PASS 之前**」。
包 §4.3 理由 2 说 R5-F2 / R5-F4 落在本次产物可信度面上所以有紧迫性 —— **但包自己在 §2.3 已写明:这次 briefing 的 P2 用途已因「非豁免判断 1 条 < 下界 3」独立失效**(该结论来自同日的 `20260802T073925Z` 包)。**两件事乘起来 = R5-F4 就算被推翻,对 P2 也不产生增量损失** —— 包把这两条分开写在两处,没有相乘,于是高估了第 6 轮的紧迫性。
真实顺序是:**T020 补下界 → P2 才变得可达 → 那时才需要 R5-F4 已被复核**。⇒ 钉法改成上述判据,比「forge 裁完」更准:**forge 裁完但 T020 未修时跑第 6 轮,仍然是空转。**
**采纳包 §4.3 的其余部分**:scope 只取 `4a4c5f5..df5ce24` + O7 真跑改动,focus 明写「R5 四条修法的残留绕过 + 真跑链路可信度」,**不重跑 30-commit 累积区间**。并采纳其理由 3 的自我约束 —— 在 C9 判据冻结前跑,很可能抓出一批「取决于 C9 怎么裁」的 finding = 空转(**与 009 KG-43 / T022 judge 无下界 / 07-28 gate 不可复现同族第四例**)。
**§4.2 的残留率量化(40%→20%→50%→75%)采纳为「末轮无复核」的正式挂债依据**,且认可包 §4.3 理由 1 的反向诚实:R5 四条**在性质上**与前四轮不同(把判据从「搜索」改成「定位」;R5-F4 直接把单一真相搬进 stdlib `urlsplit`)⇒ **第 6 轮预期产出低于前五轮但不为零** —— 这个自估没有往有利方向偏,记一笔。
**§4.3 理由 4 单独认可**:「5 轮上限是 operator 的成本决定,不是收敛证据」—— **不把「跑满了」说成「收敛了」**,这正是本仓要的口径。

**(F) `REVIEW-LOG.md` latest pointer 过期 —— 采纳,追加进 006(包里留给 operator 判,IDS 裁「记」)**。`.claude/skills/codex-review/REVIEW-LOG.md` 停在 **2026-07-26**,R1–R5 五轮**一条都没写进去**(补跑走的是 ad-hoc 的 `review-log/` 目录)。
**不是整洁问题**:IDS 之所以拖到 08-02 才发现「07-31 有五轮从未产 hand-back」,这个过期指针是成因之一 —— **「本仓最近一次 codex review 是什么」这个指针,恰好在最需要它的那批上失效**。与 **XD-43「门实装了但从未被调用」同构**:一个是门没接线,一个是指针没接线,两者都在「机制存在 ⇒ 机制生效」这个假设上翻车。⇒ 归 006,与 XD-43 / KG-B4 同案讨论。

**(G) 本包 §3.3「不要求 IDS 做的」全额尊重**,不误排期:不裁 R5 未复核(是 operator 节奏)· 不碰 spec(v0.6→v0.7 amendment 三条攒到 forge 001 后一次性落)· 不改 parallel-builder SKILL · 不起 T040/T041/FU-B/FU-C。**§4.6 的三条有界收口如实收悉**:RF5/R3-F4 的 jsonl 写入是**有界收口不是闭合**(事务性持久化 / 尾部恢复 / 并发安全 = 存储层重设计,已记 backlog;回滚建立在本仓明写的「单用户无并发写」假设上);R3-F2 的 C9 顺序判据是**源码文本顺序的近似不是控制流分析**,`global`/`nonlocal` 仍是已知空白(已写进 docstring,方向上更保守 = 漏报更少)。

**(H) KG-33 第 8 次复现收悉,不重复受理**(归 006 既定攒批)。本包补了一个 KG-33 **未覆盖**的口子:`--repo-root .` 会让 `from_build_repo` / `build_repo` / `working_repo` 三个字段全变成字面量 `.`(producer 已手改)。⇒ **同一张模板的第二个口子**,006 上修 KG-33 时一并收,别只修 `to_source_repo` 那两行。**6 约束 validator producer 模式对两者均不报错 ⇒ 这三个字段至今无机器门** —— 这与 (C) 的 `review_path` 是同一件事的两面:**schema 有字段 ≠ 字段可信**。

**Follow-up commits**: `282ea34`(本条决议 + 本包入库,严格只收 001 路径)

## 2026-08-02T07:39:25Z · 001-radar-pA-20260802T073925Z

**Reviewed at**: 2026-08-02T08:04:29Z
**Tags**: spec-gap · practice-stats(O7 时钟第 1 次真 evaluate)
**Severity**: medium
**Validator**: 6 约束 consumer 模式 **PASS**;`ids_verdict_evidence` 父键不存在 → 语法预检**跳过**(本 session 零代码改动 · 零 codex,正常)
**Related task**: `O7-first-real-evaluate`
**Operator decisions**:
- [ ] 修 PRD
- [ ] 修 SHARED-CONTRACT
- [x] **修 XenoDev spec(跨仓)**:O7 起算日写进 §1-O7(见 (A))· 随 forge 001 后那批 amendment 一起落
- [x] **⭐ §3.2 自证义务定义域裁 (i)**,但措辞必须同时命名两条链(见 (C))
- [x] **T020 判断数下界归 forge 001**,但**先裁定义域**,不直接派 prompt 改动(见 (B))
- [x] **KG-31/32 并案**:本次实例算进证据,不新开条目(见 (D))
- [x] **O7 节奏维持既定**:每周 1 个新方向,禁批量补跑;**不需等 T020 修完**(见 (E))
- [x] **§5.6 转义可读性起独立条目**(现在记,不现在修)—— 归 forge 001,**不得归类为渲染小 bug**(见 (F))

**Operator note**: **(0) ⭐ O7 计数 0/5 → 1/5,`decision_delta=true` 首次达成。** spec §1-O7 的「≥1 次实际改变 operator 投入决策」**这一半已满足**,剩下的只是次数。第 35 条 (D) + 第 36 条 (E) 授权的动作已交付。**§6 全文内嵌真跑产物的做法认可** —— 两个产物都被 `.gitignore:83 out/` 吃掉,不嵌就是 **R1-F5(T022 真跑无可复核物证)原样复发**,producer 主动识别并兜住了。

**(A) O7 起算日采纳原措辞**:「起算日 = **首条真实评估 journal 行的 `date`**」⇒ 本次 = **2026-08-02**,截止 **2026-11-02**。
consumer 端实读 `specs/001-radar-pA/spec.md` §1-O7 确认:原文只有「3 个月内完成 **≥5 次**」,**确无起点定义**。⇒ **不定义起点 = O7 永远无法判定通过或失败**,与判据可达性同族(第 35 条 (F) 在册四例的第五例:缺**起算点**)。
采纳该措辞还有一层理由包里没说:它是**自定义式**的 —— 起点由第一条 journal 行自己确定,以后不需要人工维护一个日期常量,也不会出现「spec 写的起点与 journal 事实不符」这种新的双读法。

**(B) ⭐ T020「补下界」归 forge 001,但必须先裁定义域 —— 包默认的修法可能正面违反 spec §1-O4**。
包 §4.1-3 写的是「T020 judge 补判断数下界」,默认成因是 **(α) judge 欠产 → 改 prompt**。但 consumer 端实读 `spec.md` §1-O4 原文:「低置信处**显式标注**不确定度(**不做真理机**)」。⇒ **强迫 judge 凑够 3 条判断,正面违反 O4。**
两种读法**修法相反**:
- **(α) judge 欠产** ⇒ 改 **prompt / 产出侧**;
- **(β)「每 run ≥3 条非豁免判断」这个假设本身不成立** ⇒ 改 **抽样验收侧**(例如允许**跨 run 累积抽样**,而不是要求单 run 自足)。
包用「200 篇不稀疏语料仍只 1 条」论证 (α),这**确实**证明了 judge 相对语料欠产,但**没有排除**「该方向真的只支撑 1 条诚实判断」。⇒ **forge 001 上这条必须改写成「先裁下界落在产出侧还是验收侧」,不要直接派 prompt 改动。** 这是包自己援引的 **KG-43「判据可达性先于判据冻结」再往下一层**:不只问「判据可达吗」,还要问「**判据该挂在哪一侧**」—— 挂错侧的可达性修复会砸掉另一条验收行。
**§2.3 的第二次独立复现全额采纳为证据**:不同方向 + 200 篇不稀疏语料 + 有可用锚,仍是 **1 条** ⇒ 排除「方向稀疏」与「偶然」两种解释,**这确实是结构缺陷不是抽样波动**。与第 31 条既定的 T022 结论同源,本包是**第二次独立复现**。

**(C) ⭐ §3.2 自证义务定义域裁 (i),但 spec 措辞必须同时命名两条链**。
**裁 (i)** —— 自证义务只覆盖 `radar.cli.reconstruct` 评估 run(a1 解锁链),O7 的 `evaluate` run **无 a1 自证义务**,现状即正确,spec 里把两个「评估 run」**改名消歧**。判据三条:① (ii) 要给 evaluate 补 audit.json 产出 + 让 `_require_eval_briefing_shape`(`selfcheck_sequence.py:174`)认第二种产物形状 = **改 C″ 分流契约**并触 **KG-B10 冻结面**,代价与收益不成比例;② 包 §3.2 的三条硬证据 consumer 端认可(`unlock_preflight` 要 `--audit` 而 `run_evaluate` 只写 briefing;`selfcheck-07-17.sh:63` 缺省派生指向 `out/reconstruct/`;正向 allowlist 逐段要求块级来源块,T022 渲染的 `### {i} · {ring}` 会匹配 heading 但**逐段来源块必然缺** ⇒ fail-closed STOP,即便绕过 B′ coverage 也会拿判断序号去对真 slice_id 再 STOP);③ **硬把 evaluate 产物塞进自证 = 撞上一道本来就该拒它的门 = 第五次「冻结不可达判据」** —— 包的这句自我识别是对的。
**⚠ 但措辞必须加一句,否则 (i) 会被误读成「evaluate run 裸奔」**:evaluate 有一条**同族但不同链**的 provenance 保障 —— `RunProvenance` 三值(`REAL_FULL_CHAIN` **只有**在「已拒绝一切注入」那条分支才传得出去 · R1-F1 + R2-RF1)+ `journal record` 的 `lines[2]` **逐字相等**绑定(R5-F2)。⇒ spec 改名消歧时**同时命名两条链**,而不只是给两个 run 改名。否则半年后有人读到 (i),会以为 evaluate 无任何来源保障,再补一次多余的自证 —— **那就是本条要避免的错误的镜像**。
**§3.1 结论 A 收悉**:`selfcheck-07-17.sh` 的 `2021-01-01→2023-12-31` 是**位置参数向后兼容缺省值**不是语义要求(`:5-8` + `:30-38`),真实约束是「**与被自证的那个 run 同窗**」⇒ **O7 用近期窗合法**。窗口本身不冲突这一结论成立。
**根因认定**:「**评估 run**」一词在 forge v3/v4 语境指 `reconstruct --calibration=False`,与 `radar.cli.evaluate` **词汇撞车**,底下是两族产物。⇒ 这是**第 35 条 (F)「唯一可读性」的第二个实例**,但形态不同:上次是**一条验收行的两列之间**能读出两种实装,这次是**一个词在两个文档语境里指两个东西**。建议 forge 001 把两者并为同一族记。

**(D) KG-31/32 并案采纳,不新开条目**。`.gitignore:83 out/` 吃掉真跑产物 = **R1-F5 的复发条件仍在**;本包用「全文内嵌 hand-back」**单次**兜住,但那是**人工纪律不是机器门** —— producer 自己标注了这一点,认可。⇒ 006 上与 KG-31/32(PPV 产物随 ship 自毁)并案时,把本次实例算进证据:建议 ship 门要求「**烧过 key 的产物必须有仓外持久落点 + sha256 绑定**」,否则烧钱买来的证据随 worktree 蒸发。

**(E) O7 节奏维持既定,且明确「不需等 T020」**。每周 1 个新方向,**禁止批量补跑**(批量会把 O7 从产品成功信号降成刷计数);5 次约需 4 周,远早于 11-02。
**consumer 端补一条包里没说的排期结论**:**O7 不依赖 P2 判据**(journal 行记的是 operator 的真实决策,不依赖证据链抽样判据)⇒ **O7 第 2 次下周就能跑,不必等 T020 下界修完、也不必等 forge**。这是「用途分类」第四次应用(判据侧第 31 条 → 动作侧第 35 条 → 产物侧第 36 条 → **排期侧本条**)。
**§2.2 环境阻断收悉,不记 dogfood**(mihomo 规则把 `deepseek.com` 踢成 DIRECT → SNI 阻断,operator 改规则后 401 = 连通)。三件如实认可:**key 未烧**(TLS 握手就断,请求未送达)· **零产物落盘**(fail-closed 正确工作 —— **这正是 R1-F1 那条修法要的行为,顺带成了它的第一次真跑实证**)· 环境问题非框架缺陷。但记一笔:**第二次**「代码全绿 ship,第一次真跑就炸在第一个真 provider 环」(上次 T022 是代码,这次是网络,成因不同)⇒ **共同印证在册 KG-30(ship 门不含真 provider 冒烟)**,不重复记条目。

**(F) ⭐ §5.6 转义可读性 —— 现在起条目,归 forge 001,不得归类为渲染小 bug**。包说「刻意不修 · 若 operator 认为影响使用则另起 task」。**IDS 裁:不修的判断对(修它等于放宽注入防御面),但「等 operator 觉得影响使用」这个触发条件太晚。**
实况(§6.1 原文):`我将聚焦于“coding LLMs”方向,精化出一段突出\*\*结构连接\*\*的位移叙事` … `从\(u+201c\)生成主导\(u+201d\)向\(u+201c\)攻防对抗主导\(u+201d\)的接合部迁移` —— 整段叙事满是 `\*\*` 与 `\(u+201c\)`。这是 T021/T022 两层安全消毒(欺骗性码点剥离 + markdown 中和)的**正确行为但副作用**。
**为什么不是小事**:**O7 要求 operator 每周真读一份这个产物并作出投入决策,连做 5 次**;PRD O1 是「**信任第一块砖**」。⇒ **读不下去的产物会直接压低 O7 的完成率**,这是**产品面风险**,不是渲染整洁问题。正规改法(渲染时反转义 / 分离展示层)确实不该当场动,但条目现在就记,别无限期挂在一条 §5.6 里。

**(G) §5.1 / §5.2 / §5.4 的诚实边界全额收悉**:① R5-F2 / R5-F4 两条修法未经 codex 复核**直接决定本次 briefing 可信度**,已**逐字写进 journal 的 `rationale`**(让三个月后的 O5 后验看得见当时判断基础有多薄)—— **这个做法是本包最好的一处**,建议固化:**产物的可信度债应当写进产物本身,而不只写进 hand-back**,因为三个月后做 O5 后验的人读的是 journal 不是 hand-back;② 唯一证据锚 `doi.org/10.1038/s41586-025-09422-z`(1 击)**未经人工语义核验**,机器只保证结构 provenance,包**不冒称已核验**;③ B′+D′ 自证未跑是裁 (a) 的结果**不是漏做**,连带 `out/journal/a1-selfcheck.jsonl` 无新增,**T010/T011 解锁状态不受影响**(早由 `diffusion-models-20260718T231343Z` 那次 PASS 解锁 · 第 22 条)。
**⚠ §5.3 评审债显式在册**:本 session **零 codex 评审**,§4 四条建议与 §3.2 的 spec 缺口判断**未经任何第二方复核** —— 按 XD-37 标注。**consumer 端已独立复核 §3.2 的三条硬证据与 §4.1-1 的 spec 原文,结论属实**;但 (B) 那条(T020 下界)正是**因为无第二方复核而偏了一层**的实例 —— 记一笔:XD-37 的教训在本包上**又应验了一次**。

**(H) ⚠ worktree 规约 mismatch 第 2 次 —— 升级判据已达成**。本次 `/handback-review 001` 仍在 **`main` 分支**跑,不在 `001` worktree;工作区同时存在 **009 的未提交改动**(`discussion/009/009-pM3prime/PRD.md` + 009 两个 hand-back 包 + 009 HANDBACK-LOG)。**本条决议的 commit 严格只收 001 路径,不夹带 009**。
第 36 条 (I) 记的是「该规约上线后**第 1 次** mismatch;升级判据(hook 硬拦)是复发 **≥2 次**」⇒ **本次是第 2 次,判据已达成**。按 CLAUDE.md「Session-per-idea worktree 规约」v0.2 条款,**warn 型 preflight 应升级为 commit-time hook 硬拦** —— 归 `/expert-forge 006` 落地。
⚠ 但一并记一条**反对意见供 forge 权衡**:两次 mismatch **都发生在 `/handback-review` 这一个命令上**,而该命令产出的正是 CLAUDE.md 自己列为「合回 main 的自然候选」的 **accepted governance artifact**。⇒ **在 main 上跑 handback-review 可能本来就是对的**,真正该硬拦的是「**工作区带着别的 idea 的脏改动**」而不是「分支名不匹配」。forge 上别把判据钉在分支名上,**钉在「commit 是否只收单一 idea 路径」更贴近这条规约要治的混线**。

**Follow-up commits**: `282ea34`(本条决议 + 本包入库,严格只收 001 路径)

## 2026-08-02T14:59:40Z · forge-001-v5-landing · R5 逐条裁决

**Reviewed at**: 2026-08-02T14:59:40Z
**Type**: ⚠ **非 hand-back 包决议** —— 这是 `/expert-forge 001` **v5 verdict 的落地前置**
(stage 文档 §Decision list「落地前置(表前 · 不可跳过)」+ Decision menu [A] 第 1 步)。
按 [A] 的执行顺序要求「写进 HANDBACK-LOG」,故入本 log。
**Source**: `discussion/001/forge/v5/stage-forge-001-v5.md`(commit `fdbbbdd`)
**Operator decision**: **[A] 接受 v5 verdict**,交 spec-writer 落 v0.6→v0.7 一次性 amendment

### (0) 为什么需要这条裁决(不是流程洁癖)

forge v5 的 **P3R2-GPT 穷尽性检查**发现一处**证据闭环缺口**,Opus 侧漏了并在 §5 接受:
**R5 四条 finding 的修法至今未经 codex 复核,IDS 也从未逐条裁决** —— 决议 37 (E) 只裁了
「**第 6 轮何时跑**」,**没裁 R5 findings 本身**。而 v5 的 12 项施工单里 **item 11 / item 2
直接建立在 R5 的两条修法之上**。⇒ 不先裁,施工单有若干条**建在未裁决的地基上**。

### (1) 本次裁决的一手证据(consumer 端实跑 · 非采信自述)

| 项 | 实测 | 结果 |
|---|---|---|
| 四条修法是否真在代码里 | 逐条读 `task-preflight.sh:151` / `journal/cli.py:172-190` / `ephemeral.py:373-381,385-391` / `gate.py:158-180` | ✅ **四条全在,且与包内描述逐字相符** |
| 是否有回归测覆盖 | `test_repo_scripts_gates.py` / `test_journal_cli.py` / `contract/test_ephemeral.py` / `test_credibility_gate.py` | ✅ 四条各有落点 |
| 套件现状 | `python -m pytest -q` 于 `9444e09` **本次真跑** | ✅ **`1006 passed in 4.57s`** |

⚠ **仍然为真的那件事**:以上证明「**修法在、有测、套件绿**」,**不证明「修法对」** ——
四条**均未经 codex 复核**(operator 定的 5 轮上限用尽),这是**在册未清偿的债**,不因本次裁决消失。

### (2) 逐条裁决 + 映射到 12 项

| R5 # | 级 | 病灶(一句话) | **裁决** | 映射到 v5 施工单 | 承重? |
|---|---|---|---|---|---|
| **F1** | high | 注释行不参与缩进结构 ⇒ block 循环在注释处 break,收了 `true` 永不执行后面的 `false`,脚本还返回成功(同一洞的**第五种写法**) | **accepted** | 与 12 项**无直接耦合**;其遗留缺口「preflight 从未被调用」= **XD-43 归 `/expert-forge 006`**,不在本轮 | 否 |
| **F2** | high | 真跑横幅只要求全文任意位置出现 ⇒ 第 3 行明写 `DRY_RUN_FAKE`、正文夹带真跑横幅的**自相矛盾**快照照样能成 P2 journal 行 | **accepted** | ⭐ **item 11** —— 该项要「**命名 evaluate 自己那条 provenance 链**(RunProvenance + journal `lines[2]`)」,**命名的正是这条修法** | ⭐ **是** |
| **F3** | high | `_SCOPE_NODES` 只列函数与 lambda ⇒ 下钻进类体/推导式把 Store 名误记成外层绑定,真读盘被跳过 | **accepted** | **item 10**(同文件 `ephemeral.py`,C9 门① 的 `COMPENSATING_CONTROLS` 表要加在这里)· **item 9**(兜底举证规则的实证来源就是 C9 双门) | 间接 |
| **F4** | high | 通用 URL canonicalizer 把第一个 `/` 前全部文本当 host 整体 lower ⇒ query / userinfo 的大小写敏感分量被折叠 | **accepted** | ⭐ **item 2** —— 该项要求「**抽样时 anchor 必须仍有效**」+「按规范化 claim + direction 去重」,**规范化身份的正确性直接由这条修法决定** | ⭐ **是** |

**无 rejected · 无 deferred。** 四条修法均已落地、有测、套件绿 ⇒ 撤销它们要付更大代价,
且没有任何证据指向它们错。

### (3) ⭐ 本裁决的真正产出:两条承重关系(这才是 GPT 让先裁的原因)

**F2 与 F4 是承重的** —— v5 的 item 11 与 item 2 **各自建立在其上**:

- **item 11 命名 `lines[2]` 绑定为「evaluate 那条 provenance 链」** ⇒ 若 F2 被第 6 轮推翻,
  **item 11 命名的是一条坏链**,spec 术语章会把一个错误保证写成规范文本。
- **item 2 要求「anchor 抽样时仍有效」+ 规范化去重** ⇒ 若 F4 被推翻,**累积池的身份判据本身漂**,
  同一篇文档可能在池里既算命中又算未命中。

⇒ **裁定(承接决议 37 (E) 并收紧)**:第 6 轮 codex 的触发判据维持
「**第一次真打算判 P2 PASS 之前**」,**并明确追加**:
> **item 11 与 item 2 在 spec 里落成规范文本可以现在做,但其保证不得被援引为 P2 PASS 的依据,
> 直到第 6 轮复核过 R5-F2 / R5-F4。**

**理由**:这两项的 spec 文本本身是**正确的方向**(命名链 / 池身份),被推翻的风险不在**要不要写**,
而在**写下的那条链当前是否可信**。⇒ 允许落文本、禁止据以判绿 —— 这是**用途分类第五次应用**
(判据侧 → 动作侧 → 产物侧 → 排期侧 → **本条:文本效力侧**)。

### (4) v5 verdict 接受与执行顺序

**接受 v5 全部 12 项,采 stage 文档 §Decision list 的最终底稿(= P3R2-GPT §1 修订版)。**
特别确认三条**不得降级**(降任一即 BLOCK):**item 2**(借池防空过)· **item 10**
(`review_by < expires_on` + **到期机器转红不可省**)· **item 12**(上下文安全展示投影 ·
**证不出安全则展示版不 ship** · 「不作证据用途」标签不能替代注入防御)。

**剩余执行顺序**(本条完成第 1 步):
1. ✅ **R5 逐条裁决**(本条)
2. ⏭ spec-writer 落 **v0.6 → v0.7 一次性 amendment**(12 项 · frontmatter `amended_at_5` +
   Amendment log + Version bump)→ **走一次 codex review**
3. ⏭ **T040 起跑**(warn + versioned baseline + 只卡新增 · 须证「存量只 warn / 新增才 block」)
4. ⏭ PRD v1.6→v1.7 三点修订(O7 时间锚 / 呈现面是 O1 风险 / 判断数量是集合验收采样)

### (5) 本轮 forge 的方法论增量(登记入库)

- ⭐ **本仓「判据可达性族」是 ISO/IEC/IEEE 29148 九特征的重新发明**:结构/数学可达 = **Feasible** ·
  可判定/可复现 = **Verifiable**(「iff 存在一个过程能证明系统满足它」)· **唯一可读性(决议 35 (F))
  = Unambiguous**(「allows only one interpretation」)· **OQ-A1-1 悬空 = Complete 违反**
  (集合级「no TBD, TBS, or TBR clauses」)。⇒ **自造术语让五个事故看起来像五次偶发,
  采用标准后它们是同一族的同一种违反。**
- ⭐ **但九特征只是分类不是牙**:自指链终止于「**有资质者评审 + 真跑证据**」= **合法终点非自动解除**
  (与 test oracle 文献「人是最后的 oracle 来源,合法」同构)。⇒ 本地化表强制四列 +
  **Feasible 栏不接受推演** = **七次「推演≠真跑」第一次被制度化收口成一条填表硬约束**。
- ⭐ **跨模型对标的第一价值是纠错不是共识**:Opus P2 记了条负结果「未检索到『gate 上线前先证
  其可满足』的先例」,**被 GPT 用 W3C / NASA / IEEE 29148 打掉,Opus 独立复核确认**。
  ⇒ **单模型 forge 会把「未检索到」当成「无先例」** —— 这条比 12 项施工单更耐用。
- **反自欺条款双向执行且真抓到东西**(本仓方法论资产):GPT 自陈未检索「强制多样本输出有效性」·
  Opus 自陈**累积规则是 post-hoc 制定**(SPIRIT 明写须 prespecified)⇒ **只对下一次评估生效、不追溯**;
  GPT 末轮又抓出 Opus 施工单**三处**:`≥5 run` **无来源魔数** / item 3 **给 Unambiguous 写了一条
  自己不 Verifiable 的判据** / item 12 **用「不作证据用途」标签解释掉注入风险**。三处 Opus 已逐条认领。
- **协议自指两连**:P1 阶段「800-1500 字」中文歧义致 GPT 用 `sed` 机械压缩、Opus 超标;
  stage 文档又超 4000 上限 30% 并具名声明。⇒ **本轮要裁的 Unambiguous 缺陷,发生在裁它的这场 forge
  自己的协议里**。归 `/expert-forge 006`(改 CJK 字符 / Latin words 双口径 + 禁有损机械压缩)。

**v6 触发判据(写死可测)**:**warn 候选过 `review_by` 后无证据仍被续期**。

**Follow-up commits**: `9d24b26`(本条裁决入库)
