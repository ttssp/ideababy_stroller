# Forge v2 · 009-pM3prime · P1 · GPT-5.6-Sol xhigh · 独立审阅(no search)

**Timestamp**: 2026-07-27T08:29:28Z  
**Searches used**: NONE in this round.  
**Visibility**: I did NOT read other reviewer's P1.  
**Reviewer stance**: 审阅人 — 评判已存在物,不是 daydream。

## 0. 我读到的标的清单 + 阅读策略

- 我读了:`forge-config.md`;无 `moderator-notes.md`;hand-back FU-KG43 全文;`HANDBACK-LOG` 第 26/27/28 条;v1 stage 全文;PRD §2/§4-E1/§7;forge v5 stage 全文;XenoDev `SLA.md`、`spec.md`、`risks.md`、`gold_layer2.py`、`layer2-feasibility-probe.py`;以及 forge-protocol P1 template。
- 我跳过的:未读 `discussion/009/009-pM3prime/forge/v2/P1-Opus47Max.md`;无不可达标的;未联网。
- **K(用户判准)摘要**:K 的核心句是:在“operator 领域判断力不足(全维)”下,金标 Layer-2 “到底还成不成立?验收主体是谁,还是根本不存在?” K 还明确说,宁可接受长期 blocked,也不要“看起来能跑、实际上验收不了”的降级 harness。
- **阅读策略**:先复核 v1 中心推论链,再核 `risks.md` 日期证据,最后看代码里 gold/human/machine 的真实契约。D-1/D-2/D-3 只当背景,不重审。

## 1. 现状摘要(按 Y 视角组织)

### 验证方法学/认识论

v1 的链条有三环:保留双层 gate 与 fail-closed;把第二源从“领域真人”改成“错误独立性代理”;再推出 operator 可自任。前两环有标的支撑:`gold_layer2.py` 确实只算五维映射,`mapping_agreement_rate()` 不含金融理解逻辑,第二 LLM 终审也被 `second_source_kind != human` 红线挡住。但第三环把“第二源不必等同领域专家”推进成“operator 可以产合法 gold/human 输入”。这一步没有在 v1 中闭合。v1 D-7 草案写得很细的是 human/第二源资格,不是 gold provenance;而新契约的双错率是 machine 与 human 都相对 gold 算错,所以 gold 是真值锚。

`risks.md` E1-R2 的下游后果注已在 2026-07-23 写明:当前配置凑不出领域独立真人第二源,operator “自评标注质量不如 LLM · 无合格金融判断”。v1 Intake recap 明确读了 `risks.md` 的 E1-R2。因此 2026-07-27 自陈对 v1 是**旧信息的精确化/加重**,不是性质全新的信息;v2 更像裁决旧推论是否绕过了 gold 真值来源。

### 统计效力与可证伪性

现有 Layer-2 统计对象是 41 条样本的五维关系。D-1 已证明旧合取门槛在理想输入下不可达,这是 KG-43 背景;即便 D-1 修掉,逐维双错率仍只证明“相对某个 gold,两方是否同错”。若 gold=operator 考据版,而 operator 对 sector/direction/horizon/timepoint/ticker 五维都无把握,统计量不能证伪 gold 本身。弱监督或无金标评测可生成一致性/稳定性证据,但不能替代 Layer-2 终审真值。

### 成本与 v0.1 可行性

四类候选的现状是:事后市场真值有外部可证伪性,但它验证收益/方向结果,不直接验证原文到五元组映射,且更像 E2/E3;公开数据库或 watchlist 可支撑 ticker、`published_at` 可支撑 timepoint,成本低且 v0.1 可做,但只覆盖事实维,不覆盖解释维;弱监督/无金标便宜,但没有终审主体;彻底改验收范式可能诚实,但会改变 E2 解锁条件,不是 P1 可细化的改写。

## 2. First-take 评分(按 Y 视角)

| Y 维度 | 倾向 | 理由(引用 §1 现状) |
|---|---|---|
| 验证方法学/认识论 | **cut 当前形态 / new 真值来源** | 当前“五维 Layer-2 + operator 自任 gold”不成立。错误独立性只解决不共享盲点,不产生真值;需先有 gold provenance 与可证伪者。 |
| 统计效力与可证伪性 | **refactor** | keep 双错率、abstain、fail-closed 作为度量骨架;但没有合格 gold 时,统计结果只是在未验证锚上的相对数。 |
| 成本与 v0.1 可行性 | **cut 全量五维 v0.1 / keep 事实维锚** | v0.1 可诚实保留 ticker/timepoint 这类外部可核验维;全量 sector/direction/horizon Layer-2 若无外部主体应长期 blocked,E2 不解锁。 |

KG-43 的 first-take:任何冻结门槛前至少要有两种前置证明。第一是存在性证明:构造理想输入能让 `passed=1`。第二是真值证明:验收锚从哪里来、谁能独立证伪它、成本是否在本 tier 可承受。009 同时缺过这两道门。

## 3. 我现在最不确定的 3 件事

1. P2 搜索后,弱监督/无金标评测在金融 NLP 里是否能给“验收替代物”,还是只能给开发期诊断。
2. 是否存在 PIT-safe 的公开权威源能给 direction/sector/horizon 回标,且成本低到 v0.1 真能做。
3. E2 解锁条件若只保留事实维 Layer-2,统计上还剩多少证伪力;如果太低,诚实 STOP 可能是主 verdict。
