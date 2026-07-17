# Forge v3 · 001 · P1 · GPT55xHigh · 独立审阅(no search)

**Timestamp**: 2026-07-17T14:10:04+08:00
**Searches used**: NONE in this round.
**Visibility**: I did NOT read other reviewer's P1.
**Reviewer stance**: 审阅人 — 评判已存在物,不是 daydream。

## 0. 我读到的标的清单 + 阅读策略

- 我读了:forge-config(v3 K/Y/W/strong-converge);v3 moderator-notes 不存在;X1 v2 stage;X2 v1 stage;X3 hand-back 17;X4 hand-back 16;X5 hand-back 11;X6 HANDBACK-LOG 11-17;X7 PRD v1.4;X8 L3 moderator-notes;X9 dogfood KG-B9/B10/B11;X10 FU-D-rerun-a1-verify-blindspot;X11 dependency-graph;X12 gate.py 指定段;X13 audit_channel.py 全文;X14 unlock_preflight.py 全文;X15 rerun_selfcheck.py 全文;X16 07-17 盲测面产物;X17 被否签字模板;forge-protocol P1 template;AGENTS.md。
- 我跳过的:无 IDS 仓内标的不可达。按红线,我没有读 `P1-Opus47Max.md`,也没有读任何 `out/credibility/_answer-key-*.json`。
- **K(用户判准)摘要**:本轮必须一次裁清 A「gate 存废/形态」与 B「a1 per-slice source 映射何时可见」。K 明确说第四次「推演≠真跑」后,任何新形态都必须能用 2026-07-17 真跑现有产物说明「真跑如何走到判定/验收」,并且验证范式要贴 operator「边用边审计、留痕可回溯」,不是停下来考试。a1 机制对错不再审;T010/T011 解锁条款和 KG-B10 前提处置不能再悬空。
- **我的阅读策略**:按 Y 四视角先看事实链是否闭合。架构看 gate/audit/DAG 拓扑;工程纪律看 STOP、preflight、selfcheck 是否真能机器执行;产品价值看 PRD/O2/O7 与 operator 原话;用户体验看 operator 实际看到的盲测产物和签字模板。

## 1. 现状摘要(按 Y 视角组织)

### 架构设计

v1 已把人肉盲测二值签字从 T010/T011 前置中退役;v2 又把 ①② 退到 Phase 2/使用期,新前置改成 a1 单一谓词。当前 DAG 已接成 T003-A3 → T004-A2 → T004-A4,再双前置 T010/T011,但注释仍写 RERUN-PASS artifact 未退役,只是被 preflight 内部消费。D′ 真跑后,这个拓扑出现新的卡点:a1 的 source_refs 在内存里成立,但盲测 markdown 不渲染 refs,审计 markdown 不落盘,audit.json 又由 `generate_audit_channel_postgate` 在 gate PASS 后才产。

### 工程纪律

代码层有明显的 fail-closed 倾向:`evaluate_gate` 做 run_id/切片集合/new_evidence_chain 校验;`read_audit_channel`、`check_unlock_predicate`、`run_a1_selfcheck` 都会在结构缺失时 STOP。但 KG-B10 两面仍成立:`_verify_gate_pass_artifact` 只信 caller 传入的 PASS markdown,selfcheck journal 只信 caller 写入的布尔字段。也就是说,当前实现能挡误用和低技巧绕过,但不是不可伪造边界。

### 产品价值

PRD 的真实价值锚是 lab lead 在 30 分钟内拿到可核验方向判断,长期信任靠 O2/O7 使用中校准。operator 07-15 的三条原话已经把产品价值从「一次性盲测过关」推向「留痕可审计、边用边迭代」。07-17 真跑盲测面则再次证明,现在落盘给 operator 的仍是纯叙事,没有任何 source/ref token,与可审计价值锚断开。

### 用户体验

operator 当前体验被拆成两个相互冲突的界面:可见的是盲测散文和要求填 new_evidence_chain 的签字模板;真正能支持快速审计的 per-slice source 映射被放进受保护/后置路径。签字模板保留「真切片全可信 + 负控识伪 + 新证据链」的考试感,而 hand-back 11/17 都显示 operator 想要的是可见底料、抽查、回溯和持续修正。

## 2. First-take 评分(按 Y 视角)

| Y 维度 | 倾向 | 理由(引用 §1 现状) |
|---|---|---|
| 架构设计 | refactor | a1 链已落地但被 post-gate 可见性锁住;若 gate 改形态,DAG/RERUN-PASS/audit 时机必须一起重绑。 |
| 工程纪律 | refactor | STOP 与结构校验值得保留,但 KG-B10 说明现边界不能承担「真 PASS/真 rerun」的不可伪造语义。 |
| 产品价值 | refactor(g1 cut) | O2/O7 与留痕审计方向站得住;盲测二值签字与 operator 工作流冲突,不应继续作价值主锚。 |
| 用户体验 | new | 现有 operator 可见面不是审计面;需要新的可审计留痕操作面,否则 a1 对用户不可感知。 |

## 3. 我现在最不确定的 3 件事

1. g2「留痕可审计验收」与 g4「O2/O7 使用期后验」的边界怎么画:是前置验收只看产物留痕结构,还是干脆把信任判定主要移到使用期?
2. 若没有二值 PASS,T010/T011 的最小解锁证据应是什么:一份可见 a1 审计产物 + 可复现 smoke 记录是否足够,还是仍需某个非考试型 STOP artifact?
3. KG-B10 是否应在本轮改写为「任何 provenance/审计产物的可伪造性协议」,而不是继续围绕 post-gate PASS artifact 设计;这个范围太宽会不会重蹈 KG-B7 过度投资。
