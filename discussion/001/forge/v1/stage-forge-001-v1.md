# Forge Stage · 001 · v1 · "P0.2 盲测 gate 形态治理:退役人肉二值签字 → 机器可判最小验收"

**Generated**: 2026-07-16T08:10:00Z
**Source**: forge run v1 with X = 8 标的(1 粘贴文本 + 6 本仓库文件/stage 文档 + 1 外部 repo 文件), Y = 工程纪律 · 架构设计 · 产品价值, Z = 对标 SOTA(验证/gate 设计先例层), W = verdict-only + decision-list + next-PRD + refactor-plan
**Convergence mode**: strong-converge
**Rounds completed**: P1 (both), P2 (both), P3R1 (both), P3R2 (both)
**Searches run**: 20 across ~15 distinct sources(Opus 4 · GPT 16;human-in-loop eval / audit-trail / LLM-judge 校准 / 后验闭环四方向)
**Moderator injections honored**: none(`forge/v1/moderator-notes.md` 不存在)
**Convergence outcome**: converged(双方 P3R2 §2 单一 verdict 逐点对齐,无 unresolved)

---

## How to read this

forge 是横切层(不是 L1-L4 pipeline 的一部分)。本文档是双专家(Opus 4.8 + GPT-5.5 xHigh)
审阅 + SOTA 对标 + 联合收敛后的产出,**强制给出立场**(不是候选菜单 defer 给你拍板)。

本次真实标的**不是** proposal §001 那句宽泛 research-radar seed,而是**已 ship 的 001-radar-pA
build 里 P0.2 盲测 gate 的形态治理**——触发源 = hand-back `001-radar-pA-20260715T093226Z`
(operator 真跑当面拒签 gate 形态)。故下文 §"Next-version PRD draft" 表述为 **PRD v1.2 → v1.3
的修订草案方向**,不是全新 PRD。

读完后你应该:
- 知道双专家对「人肉盲测二值签字 gate」去留的最终 verdict,以及 KG-B4/B7/B8 三层各自的裁决
- 知道支撑每条结论的具体证据(§"Evidence map" 可逐条溯源到 P1/P2/P3)
- 拿到按 W 形态准备好的可执行草案(4 列决策矩阵 + PRD v1.3 方向 + XenoDev 落地 refactor-plan)
- 能基于 §"Decision menu" 直接进入下一步行动(把 verdict 灌回 PRD / 跑 v2 / 局部接受 / park / abandon)

## Verdict

**P0.2「人肉盲测二值签字」gate 从 T010/T011 解锁前置中退役——采纳 KG-B8。** 新解锁前置 =
机器可自动判的最小验收三项:① trace/provenance schema 完整性;② 证据 3 击可达性(链路机器可解析、
引用可解析到原文);③ 轻量审计通道就位(留痕结构存在且命名一致)。三项秒级可跑、无人肉停机。
operator 的判断力从「一次性考官」移位为「使用期抽查者 + O7 journal 累积校准」——这是 operator
三条批评①②③(非可靠打分器 / 要留痕可审计 / 要边用边迭代)的直接落地,且 SOTA 无「人肉盲测二值
签字作阻断闸门」先例(回应 K)。**防 V4 铁律不丢**:FAIL→STOP 双道保留——机器道拦可复现失败,
治理道(prd-revision-trigger hand-back)接 operator 判断级发现(本次 forge 自身即该通道运转的实证)。
KG 级联:**B8 采纳**(形态重构)· **B7 大部消解**(签字/answer-key/反作弊面随盲测退役而退场,残余
reviewer leakage/Goodhart 归审计设计,不再投资加固)· **B4 保留但改写**(机器强制对象从「RERUN-PASS
artifact 存在」改为「三项最小验收 + 机器道 STOP 的代码级 wiring」,B4「不能靠 markdown 约定」的教训
恰恰适用于新前置)。

## Evidence map

| 结论 | 来源 | 引用(≤15 words) | 是否有反对证据 |
|---|---|---|---|
| 人肉盲测二值签字作阻断闸门无工业先例 | P2-Opus §1 row1 · P2-GPT §1 综合 | "工业界没有人肉盲测二值签字作阻断发布闸门的先例形态" | - |
| operator 非可靠打分器有文献背书,单轮 4 样本只够 smoke | P2-Opus §1 row2 · P2-GPT §1 row4 | "单轮 4 样本统计功效只够 smoke 诊断" | - |
| 砍人肉二值 ≠ 砍一切阻断;SOTA 保留自动化 gate | P2-Opus §1 row3 · P2-Opus §3 补一刀 | "SOTA 保留阻断 gate 但它是自动化的" | ⚠ P1-GPT §2 曾把非阻断 smoke「留后续裁」(见 §underweights) |
| 新前置 = 机器可判三项(trace/可达/审计通道) | P3R2-Opus §2 · P3R2-GPT §2 | "三项轻量机器前置(trace 完整、引用可达、审计通道一致)" | - |
| 识伪盲测 retire-as-gate, keep-as-calibration,零解锁语义 | P3R2-Opus §1 分歧1 · P3R2-GPT §1 分歧1 | "校准产出只入 journal,零解锁语义" | ⚠ P1-Opus §3.3:抽查功效是否只是更便宜的剧场 |
| FAIL→STOP 双道(机器道 + 治理道)保留 | P3R2-Opus §1 分歧3 · P3R2-GPT §1 分歧3 | "机器道拦可复现失败,治理道接判断级发现" | - |
| O2 3 击留痕从「产品功能」升级为「验收机制」 | P1-Opus §1 视角B · P2-Opus §1 row4 | "把 O2 从产品功能提升为验收机制" | - |
| B8 是 B4/B7 上游;裁 B8 级联改写下游 | P1-Opus §1 视角B · hand-back §2 诊断信号 | "B8(形态该不该存在)是 B4 与 B7 的上游" | - |
| B7 反作弊面随盲测退役大部消解 | P3R2-Opus §2 · P2-GPT §3 部分修正 | "answer-key、nonce、签字重放会随盲测退役大幅消解" | ⚠ P2-GPT §3:残余 reviewer leakage/样本偏差/Goodhart 仍在 |
| B4 保留但强制对象改写、要求代码级 wiring | P1-GPT §1 工程纪律 · P3R2-Opus §2 | "机器闭环应转为 trace 完整性…不能靠 markdown 纪律" | - |
| DAG 依赖结构滞后于 PPV 语义(RERUN-PASS 仍是唯一前置) | P1-GPT §1 架构设计 · PRD Open questions #3 | "DAG 解锁点还停在一次性二值 PASS" | - |

## Intake recap

### X · 审阅标的(8 个)
- `TEXT:` proposal §001「Research Radar」原文(粘贴文本 · 背景 seed,非审阅重心)
- `discussion/001/001-radar/L3/stage-L3-scope-001-radar.md`(stage 文档 · Candidate A/B + 信任三件套出处)
- `discussion/001/001-radar/001-radar-pA/PRD.md`(本仓库文件 · **PRD v1.2 · gate 形态直接标的**)
- `discussion/001/handback/20260715T093226Z-...md`(本仓库文件 · **触发本次 forge 的 hand-back · 第一因**)
- `discussion/001/handback/HANDBACK-LOG.md`(本仓库文件 · 11 条决议史 SSOT)
- `discussion/001/001-radar/L3/moderator-notes.md`(本仓库文件 · 两次 injection · 主锚移 O2+O7 + 价值重定义)
- `discussion/001/handback/20260711T135303Z-...md`(本仓库文件 · P0.2 首跑 FAIL · 能力层 vs 结构层对照)
- `/home/ys/codes/XenoDev/dogfood-backlog.md`(外部 repo 文件 · KG-B4/B7/B8 三条同簇原文)

### Y · 审阅视角
- 工程纪律 — gate/验收机制、TDD/review 流、防 V4 铁律的形态
- 架构设计 — PPV 结构、T010/T011 解锁依赖、O2/O7 信任链的可演化性
- 产品价值 — 验证范式是否贴 operator 真实工作流(边用边审计 vs 停下来考试)

### Z · 参照系
- mode: 对标 SOTA(限验证/gate 设计先例层:human-in-loop eval / audit-trail 验收 / LLM-judge 校准 / 后验闭环)
- 用户外部材料:无(K 内无额外链接)

### W · 产出形态
- verdict-only · decision-list · next-PRD · refactor-plan(下方四章节均需出现)

### K · 用户判准
本次真实标的 = P0.2 盲测 gate 形态治理。operator 真跑拒签「人肉盲测二值签字」形态,三条批评:
①operator 非可靠打分器(单轮 3 切片 1 负控,功效低)②应留痕可审计,不应盲测签字(每条位移
判断留 source trace + 抽查 + log 回溯)③应边用边迭代,不应前置一次性闸门。同簇裁 KG-B8(形态
该不该存在)+ KG-B4(gate PASS 无机器强制)+ KG-B7(反作弊单次执行)。**必须裁的张力**:PRD v1.2
保留 RERUN-PASS 唯一前置 vs hand-back §3.A 彻底去二值硬前置——线画在哪。**我在乎**:验证范式贴
operator 真实工作流(边用边审计,不是停下来考试);给 T010/T011 新解锁条件(不能悬空);防 V4
铁律(FAIL→STOP→回流)精神保留哪怕形态变。**我不在乎**:gate 现有代码沉没成本;保住 T004-A1
那 14 轮投入的面子。

### 收敛模式
strong-converge(双方 P3R2 已 converged,无 unresolved)

---

## Verdict rationale(W · verdict-only)

裁的这条线画在 **v1.2 与 hand-back §3.A 之间、且偏向 §3.A 但补一道机器底线**:

- **比 v1.2 更进**:v1.2 虽把长期主锚移到 O2+O7、要件③降级,但仍**保留 RERUN-PASS 为 T010/T011
  唯一前置**(PRD Open questions #3 明写「它仍是 T010/T011 唯一前置」)。verdict 让人肉二值签字这个
  解锁形态整体退役——DAG 依赖结构追上 PPV 语义,不再让「一次性二值 PASS」当解锁点(P1-GPT §1 架构:
  "依赖结构滞后于 PPV 语义")。
- **比 §3.A 多一道底线**:hand-back §3.A 提「彻底改可审计留痕验收 + gate 降级为纯非阻断 smoke signal」。
  P2 双方独立检索后**共同修正**了纯非阻断路线——SOTA 三分工里 CI 自动化 gate **仍是阻断的**
  (P2-Opus §1 row3),纯告警会丢掉防 V4 的 STOP 精神(K 明言不可丢)。所以新前置不是「无 gate 直接
  放行」,而是「机器可自动判的最小验收阻断 + operator 抽查非阻断」。
- **诚实框架**:新形态不是「抽查功效更高」的剧场替换。SOTA 的诚实解是把人当**噪声传感器 + 校准集 +
  多轮累积 + 误差校正**(P2-Opus §1 row2 · P2-GPT §1 row4);v0.1 的四样本只承担 smoke 诊断,**不承担
  certification 语义**——若未来要认证,须按目标 power 反推样本量(降级为 v0.2 note)。这一点必须写穿:
  verdict 解决的是「形态错配 + 工作流错配」,不假装解决了统计功效问题。

三层 KG 的裁决顺序遵循 K「预置输入 2」的次序论(先裁 B8,别再往被拒形态加固):**B8 → B7 → B4**。
先裁 B8(形态重构)使 B7 的反作弊攻击面(answer-key/nonce/签字重放)随盲测退役大部自然消解,避免重蹈
T004-A1「花 14 轮硬化被 B8 推翻前提」的过度投资;B4(机器强制)不删除而是把强制对象改写到新前置上。

## Decision matrix(W · decision-list)

| 类别 | 项 | 来源(标的具体位置) | 理由 | 优先级 |
|---|---|---|---|---|
| **保留** | FAIL→STOP 防 V4 铁律(触发器改写,不删语义) | PRD O4 初始层 · hand-back §1 | 首跑 FAIL→STOP 已证其值钱(预算没烧);K 明言精神不可丢 | P0 |
| **保留** | O2 3 击回溯留痕 → **升级为验收机制** | PRD O2/O4 长期层 · P1-Opus §1 视角B | 满足批评②在架构上是把已有 O2「从产品功能提升为验收机制」,非新增机制 | P0 |
| **保留** | prd-revision-trigger / hand-back 通道(治理道 STOP) | hand-back frontmatter tags · P3R2-Opus §1 分歧3 | 治理道不是新机制,是既有通道显式命名;本次 forge 即其运转实证 | P0 |
| **保留** | 负控注入机制 → **降级为可选校准活动** | PRD O4 初始层 · P3R2 双方分歧1 | 首跑精准命中负控 slice-1 是实证正资产(有牙),退役太浪费;非保沉没成本 | P1 |
| **保留** | O5/O7 journal + taste 后验闭环 | PRD O4 长期层 · O5 | 长期信任主锚,operator 使用期校准的落点 | P0 |
| **调整** | T010/T011 解锁前置:RERUN-PASS → 机器可判三项 | PRD Open questions #3 · hand-back §3.B | 依赖结构追上 PPV 语义;给出「不悬空」的新解锁条件(K 在乎) | P0 |
| **调整** | O4 初始层语义:盲测 smoke → 机器 smoke(自动/秒级/阻断) | PRD O4 · P2-Opus §3 补一刀 | SOTA 保留阻断但是自动化的;人肉判断移到使用期循环 | P0 |
| **调整** | KG-B4:强制对象改写 + 要求代码级 wiring | XenoDev dogfood-backlog KG-B4 · P1-GPT §1 | B4「不能靠 markdown depends_on」的教训恰适用于新前置的机器闭环 | P0 |
| **调整** | XenoDev spec §5 重跑协议 → 改为校准活动协议 | hand-back §3.B · P3R2-Opus §4 | 去二值签字后,重跑不再是解锁前置,是可选校准 | P1 |
| **删除** | 人肉盲测二值签字的**解锁形态**(签字模板-解锁耦合) | hand-back §2 · PRD O4 | operator 真跑拒签;SOTA 无此先例;与产品 UX 原则(判断先行/边用边审计)相抵 | P0 |
| **删除** | KG-B7 反作弊面的**进一步投资**(现状冻结,不删已 ship 代码) | XenoDev KG-B7 · hand-back §2 诊断信号 | operator 无对抗动机;攻击面随盲测退役消解;别再往被拒形态加固 | P0 |
| **删除** | 四样本 certification 语义 | P2-GPT §1 row4 · P3R2-GPT §3 v0.2 note3 | 统计功效只够 smoke,不能支撑认证;避免新剧场 | P1 |
| **删除** | review queue / journal 回溯**作阻断前置** | P3R1 双方分歧2 | journal 规则全归使用期治理,不阻断——否则重造更宽的 gate,违 K「边用边迭代」 | P0 |
| **新增** | trace/provenance schema 机器校验器(阻断项①) | P3R2-Opus §4 · P2-GPT §1 row3(W3C PROV) | 机器可自动判 trace 完整性;新前置第①项 | P0 |
| **新增** | 证据可达性检查器(阻断项②:3 击链路可解析 / 引用可达) | P3R2 双方 §2 | 机器可判引用可解析到原文;新前置第②项 | P0 |
| **新增** | 轻量抽查记录通道(阻断项③:文件级结构,非 LangSmith 级) | P3R2-Opus §1 分歧2 让步 | operator 抽查留痕最小结构;**v0.1 必须轻量**,膨胀则新 gate 变旧仪式 | P0 |
| **新增** | 机器道 STOP 的代码级 wiring(B4 改写落点) | P3R2-Opus §2 · P3R2-GPT §1 分歧3 | 缺 trace/时间线断裂/引用不可达/结构不一致 → 自动 STOP 阻断下游 | P0 |
| **新增** | journal 累积校准规则(使用期治理,非阻断) | P3R2 双方 §3 v0.2 note | 边用边攒证据校准;不挡解锁 | P1 |

## Next-version PRD draft(W · next-PRD)

> **注**:本次标的是 001-radar-pA 的 gate 形态治理,**不是全新 PRD**。以下是 **PRD v1.2 → v1.3 的
> 修订草案方向**(O4/Open questions 章节重写为主),供 operator 灌回 PRD 时消费。PRD 是 L3 后 SSOT,
> 修订须 operator 显式批准。

```
# PRD 修订草案 · 001-radar-pA · v1.2 → v1.3

**Status**: Draft from forge v1, awaiting human approval(仅改 O4 + Open questions #3 + 新增 non-goal)
**Sources**: forge stage-forge-001-v1.md · hand-back 20260715T093226Z · KG-B8

## 改动点 1 · O4 重写(信任分层校准)

- 初始层 · P0.2 解锁前置(改写):从「盲测二值签字 gate」→ **机器可自动判最小验收三项**
  ① trace/provenance schema 完整性(每条位移判断/边带 source trace,机器可解析)
  ② 证据 3 击可达性(O2 三击链路机器可解析、引用可解析到原文条目)
  ③ 轻量审计通道就位(留痕可被 operator 抽查的最小文件级结构存在且命名一致)
  三项秒级机器判、无人肉停机;任一项 FAIL → 机器道 STOP(防 V4)。
- 长期层 · 信任主锚(强化):O2(3 击回溯,已升级为验收机制)+ O5/O7(journal 后验 + taste 校准)
  + operator 使用期**抽查**(非盲判);identity 保持 v1.2 长期主锚。
- 识伪盲测:明示为**可选的使用期校准活动**(operator 自发起、无签字模板、无 PASS/FAIL 裁决),
  产出**只写 journal 作校准证据,零解锁语义**(封死借尸还魂回前置)。

## 改动点 2 · Open questions #3 重写

废止「(RERUN-PASS)仍是 T010/T011 唯一前置」的表述。新表述:T010/T011 解锁前置 = 上述机器可判
三项;首跑证据用途从「重判签字」改为「校准活动的历史样本」;多轮盲测=可选校准,不挡解锁。

## Scope OUT 新增(显式 non-goal)

- **人肉盲测二值签字作解锁闸门**(evidence: SOTA 无此先例形态 · operator 真跑拒签 · KG-B8 采纳)
- **四样本 certification 语义**(evidence: 统计功效只够 smoke · P2 双方独立命中 Kim2026/Noisy-but-Valid)
- **review queue / journal 回溯作阻断前置**(evidence: 全归使用期治理 · 否则重造更宽 gate,违「边用边迭代」)
- **KG-B7 反作弊面的进一步投资**(evidence: operator 无对抗动机 · 攻击面随盲测退役消解)

## Success looks like(O4 相关补充,回应 K)

- operator 能「边用边抽查」而非「停下来考试」——每条位移判断可 3 击到原文,发现问题 agent 有 log 可回溯
- 明显不可信(trace 断链/引用不可达)机器自动 STOP,防 V4 精神以新形态保留

## Open questions(forge 也没解决的,降级 v0.2 note)
- 阻断项③「审计通道」最小 schema 具体形态(单文件 vs 目录 vs 附着 briefing)——留 XenoDev spec 层按 v0.1 自用实况定
- 校准活动的频率与统计设计(按目标功效反推样本量,Kim 2026 路线)——攒 journal 数据后再定
- 治理道 STOP 的证据标准——先复用 hand-back §6 schema,误/漏触发再收紧
```

## Refactor plan(W · refactor-plan · XenoDev 改 spec 时直接消费)

> 骨架 = 双方 P3R2 §4 草稿建议的**并集**;冲突处以双方 §1/§2 最终立场为准。代价 S/M/L 基于 §4 建议。
> 落地在 XenoDev(唯一 L4 build runtime);IDS 侧只改 PRD + 决议,不静默改代码(防 V4 · 跨仓边界)。

#### 模块 A · T010/T011 依赖结构 + 机器道 STOP wiring
- **当前问题**:DAG 硬编码 `P0.2-RERUN-PASS artifact` 为 T010/T011 唯一前置;`evaluate_gate` 是无
  wiring 的纯库函数,STOP 只靠 parallel-builder 读 markdown `depends_on`(KG-B4:「T004 已 merge ≠ gate PASS」)。
- **目标态**:前置改为机器可判三项;新增机器道 STOP 的**代码级 wiring**(缺 trace/时间线断裂/引用
  不可达/留痕结构不一致 → pipeline 内自动 STOP 阻断下游)。这是 B4 改写的落点——不能再靠 markdown 约定。
- **改造步骤**:1) spec §5/§6 + dependency-graph.mmd:T010/T011 前置文案与脚本重定义;2) 把三项验收
  接入 preflight,任一 FAIL 自动 STOP;3) 保留 prd-revision-trigger 作治理道 STOP(既有通道显式命名)。
- **风险**:B4 的机器强制若仍不闭环(留在库函数),等于换汤不换药——SOTA CI gate 是真阻断的,此项必须真 wire。
- **预估代价**:M

#### 模块 B · credibility/gate.py + injector.py → 降级为校准工具
- **当前问题**:gate 机制含 KG-B7 反作弊硬化(run-binding + 256-bit nonce + reason 泛化,codex 14 轮),
  但 operator 拒此形态前提;签字模板与解锁耦合。
- **目标态**:去签字/解锁路径,保留负控注入与叙事产出;产出只入 journal,零解锁语义。KG-B7 反作弊面
  **现状冻结**(不删已 ship 代码,但不再投资加固)。
- **改造步骤**:1) 摘除签字-解锁耦合;2) 负控注入保留为可选校准活动入口(operator 自发起);3) 校准
  产出写 journal schema,不产 PASS/FAIL/RERUN-PASS artifact。
- **风险**:若解锁语义未封死,盲测可能借尸还魂回前置(P3R2-Opus §1 分歧1 显式封条)。
- **预估代价**:S(主要是解耦 + 删路径,非新建)

#### 模块 C · 新增 trace-validator(三项验收的机器实现)
- **当前问题**:O2 有 source trace,但只是产品功能,未形成验收级 provenance/audit artifact(P2-GPT §1 row3)。
- **目标态**:机器全量校验 trace/provenance schema 完整性 + 证据 3 击可达性(引用可解析到原文)+ 审计
  通道命名一致性;可对标 W3C PROV / Audit Cards 的验收级结构,但 **v0.1 保持轻量文件级**。
- **改造步骤**:1) 定义 trace schema;2) 实现完整性 + 可达性 checker;3) 接入模块 A 的机器道 STOP。
- **风险**:若任一项无法秒级机器判,回头重审该项资格(v0.2 note 1)——不得让新 gate 膨胀成 LangSmith 级基础设施。
- **预估代价**:M

#### 模块 D · journal / 抽查记录最小 schema(使用期治理)
- **当前问题**:O7 journal 已有后验闭环意图,但抽查记录/校准证据的最小结构未定。
- **目标态**:轻量文件级抽查记录 schema(阻断项③的载体)+ journal 累积校准规则(使用期,非阻断)。
- **改造步骤**:1) 定抽查记录 schema(briefing 留痕 + 抽查记录);2) journal 累积校准规则文档化(不挡解锁)。
- **风险**:文件级若无法支撑 operator 快速复盘,再升级 queue(v0.2 note 2)——v0.1 不提前加 gate。
- **预估代价**:S

---

## What this menu underweights(强制自批判)

- **反对证据未充分整合 · 抽查是否只是更便宜的剧场**:§"Evidence map" 标 ⚠ 的 P1-Opus §3.3 提出诚实
  质疑——若 briefing 错误 subtle,随机抽查的统计功效未必高于盲测。主 verdict 坚持退役的理由**不是**「抽查
  功效更高」,而是「形态无先例 + 工作流错配 + 二值单轮本就功效低」;verdict 已把「不承担 certification
  语义」写穿。但请注意:**这意味着新形态也没解决统计功效问题**,只是把它诚实降级为 v0.2 note(需要真正
  可信性证明时,按目标 power 反推样本量)。别误读成「换个机器 gate 就统计可信了」。
- **B7 残余风险未清零**:§"Evidence map" 标 ⚠ 的 P2-GPT §3——answer-key/签字重放大部消解,但 reviewer
  leakage / 样本选择偏差 / Goodhart 仍在,只是从「防作弊考试」变成「审计设计」问题。verdict 把它冻结/归类
  而非解决;一旦校准活动上量,这些审计设计问题会回来。
- **Y 视角覆盖盲区**:Y 未含「安全」。P1/P2 均未展开 attack surface(operator 自用无对抗动机),但机器道
  STOP wiring 落地时的 trace 可篡改性(audit-trail 规范要求「防篡改」)值得 XenoDev spec 层后续 attention。
- **K 中未充分回应的关切**:K 全部关切均已显式覆盖(线画在哪 ✅ / T010/T011 新条件 ✅ / 防 V4 保留 ✅ /
  边用边审计 ✅ / 不看沉没成本 ✅)。无遗漏项。
- **convergence_mode 副作用(回声室风险)**:strong-converge 下双方 P1 即高度同构(三视角都 refactor),
  P2 检索又互相咬合,P3 几乎无实质对抗——**这是双模型回声室强化的高风险信号**。双方都同意但可能错的判断:
  ①「机器可判三项秒级可跑」是**推演**,未在 XenoDev 真跑验证——trace 完整性/引用可达性的机器判定在真实
  briefing 上可能比想象的难(参考历史教训:forge 理论决议屡漏实证盲区,DB 引擎语义/并发/原子性靠真跑才现形)。
  ②「B7 攻击面自然消解」是级联推断,未逐条验证残余面。**建议**:verdict 落地前在 XenoDev 用一次真 briefing
  验证三项 checker 的秒级可判性,而非直接信推演。
- **X 标的覆盖局限**:未直接读 XenoDev 的 `credibility/gate.py` / `injector.py` / `dependency-graph.mmd`
  源码(X 只含 dogfood-backlog 的 KG 摘录),refactor-plan 的模块划分基于 hand-back/KG 描述而非源码实况;
  XenoDev 侧实装前应以源码校准模块边界。
- **forge versioning 提示**:以下新信息进入会触发 v2 并可能改变本 verdict——① XenoDev 真跑发现三项 checker
  无法秒级机器判(推翻「机器 smoke gate」可行性);② 校准活动上量后统计功效数据显示抽查确实是剧场(可能
  需回到多轮累积的更重设计);③ operator 使用中发现「零解锁语义的校准」反而让人不做校准(动机问题)。

自批判扫描后主要盲区 = **回声室 + 未真跑验证**。请注意 forge 是双模型综合,不是真跑数据——XenoDev
build-time 复现测才是最后防线,真实数据仍可能推翻本 verdict。

## Decision menu(for human)

### [A] 接受 verdict → 灌回 PRD v1.3 + 派 XenoDev 落地(本 idea 语境的「进 L4」)
```
⚠ 本标的是已 ship build 的 gate 形态治理,不是新 PRD fork——不走 /plan-start 新建 branch,
   而是走「改 PRD → hand-back review 决议 → XenoDev 按新形态改 spec」的既有回流通道。
流程:
1. 把本 stage §"Next-version PRD draft" 的 O4/Open questions #3 改动灌回
   discussion/001/001-radar/001-radar-pA/PRD.md(v1.2 → v1.3),operator 显式批准。
2. 在 HANDBACK-LOG.md 追加对 hand-back 20260715T093226Z 的决议 entry(采纳 KG-B8 + B4 改写 + B7 冻结)。
3. 通过 hand-back / outbox 通道把新形态 + §"Refactor plan" 四模块下发 XenoDev(唯一 L4 build runtime)。
4. XenoDev 按新形态改 spec §5/§6 + dependency-graph + 实装 trace-validator(参 §"Refactor plan")。
⚠ 落地前建议先在 XenoDev 用一次真 briefing 验证三项 checker 秒级可判性(见 §underweights 回声室预警)。
```

### [B] 跑 forge v2(说明需要补什么)
```
/expert-forge 001
# Phase 0 intake 时调整 X / Y / Z / W / K;旧 v1 整目录保留作历史参考
```
适用:担心回声室(§underweights 已预警)想引入更强对抗;或想把 XenoDev 源码
(gate.py/injector.py/dependency-graph.mmd)加进 X 让 refactor-plan 校准到源码实况;
或 XenoDev 真跑后三项 checker 可判性被推翻,需重裁。

### [C] 局部接受
- ✅ 采纳:B8 形态重构(人肉二值签字退役)· 三项机器验收作新前置 · 双道 FAIL→STOP · B7 冻结
- ⏸ 挂起:识伪盲测「零解锁语义校准」的具体协议(等 XenoDev 真跑验证三项可判性后再定死)· 阻断项③
  审计通道最小 schema(留 spec 层)
- ❌ 拒绝:(无 — verdict 无明显应拒项;若拒 B8 采纳则整个 verdict 不成立,应改选 [B])

### [P] Park
```
/park 001
```
保留所有 forge 产物,标记暂停。复活时不重做这一层。适用:operator 暂不推进 radar,gate 形态治理挂起。

### [Z] Abandon
```
/abandon 001
```
forge verdict 显示该 idea 不该继续做。归档 lesson 文档。**本 verdict 不指向 abandon**——它是「怎么继续」
的裁决,不是「要不要继续」。仅当 operator 独立判定 radar 整体不做时才选此项。

---

## Forge log
(由 /expert-forge 命令更新;记录每次 forge run 的 v 序列 + 关键 verdict 一句话)

- v1: 2026-07-16 — verdict: "P0.2 人肉盲测二值签字 gate 退役(采纳 KG-B8),T010/T011 改由机器可判三项(trace 完整/引用可达/审计通道就位)解锁;operator 移位为抽查者+journal 校准;FAIL→STOP 双道保留;B7 大部消解、B4 改写为新前置机器闭环。"
