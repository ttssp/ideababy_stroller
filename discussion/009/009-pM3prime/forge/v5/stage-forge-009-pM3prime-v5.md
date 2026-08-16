---
doc_type: forge-stage
fork_id: 009-pM3prime
forge_version: v5
created: 2026-08-16
convergence: converged
open_disagreements: 0
v02_notes: 3
w_forms: [verdict-only, decision-list, refactor-plan]
synthesized_by: forge-synthesizer subagent
trigger: IDS /handback-review 009 第 37 条 · T016 ship + 七条 obligation 在 forge:009-pM3prime:phase0 到期(-01/-10 结账 · -04/-05/-09/-11/-12 过表并入本轮 X)
reviewers: [Claude Opus 4.7 Max (A), GPT-5.5 xHigh (B)]
moderator_injections_honored: 1
---

# Forge Stage · 009-pM3prime · v5 · 「绑定之后,到底绑在哪儿」

**Generated**: 2026-08-16T15:05:00+08:00
**Source**: forge run v5 · X = 11 标的(本仓 5 + XenoDev-009 6)· Y = 工程纪律 / 测量效度·统计方法学 / 规范工程·policy authoring · Z = 对标 SOTA(零重叠为佳)· W = verdict-only + decision-list + refactor-plan
**Convergence mode**: strong-converge
**Rounds completed**: P1(双)· P2(双)· P3R1(双)· P3R2(双)
**Searches run**: **19**(A 侧 7 / B 侧 12)覆盖 **12 个体系,零重叠**
**Moderator injections honored**: **1**(2026-08-16T04:20Z · Hard constraint · binding on both)
**Convergence outcome**: **converged · 0 unresolved**

⚠ **长度声明**:本文约 4,300 汉字,**超 synthesizer 模板 4,000 上限约 8%**。主因:W 三形态全产 +
moderator note 要求的元层专章 + 15 行 decision matrix 带两列方法论字段。**如实声明,不粉饰**(承本轮 P2/P3R1 同样处理)。

---

## How to read this

forge 是**横切层**,不是 L1-L4 pipeline 的一环。本文档是双专家审阅 + SOTA 对标 + 联合收敛的产出,
**强制给出立场**,不是候选菜单。

前四轮的审阅对象:**v1** 金标标注的验收主体 · **v2** 那套验收的测量效度 · **v3** 产出信号的那台机器 ·
**v4** 这套治理机制自身。**v5 审的是 v4 终裁的下一层:绑定落空的五种方式。**

⚠ **可信度分布(请按此读)**:
- **P1 = 弱收敛证据**。六题处置倾向几乎逐条相同(第五轮),但四条具名预测**互相落空** ⇒
  operator 裁决**不按回声处理**(见 §元层)。它只是弱证据,**不是本 verdict 的分量所在**。
- **分量在 P2 与 P3**。双方检索面**零重叠**(A:OLRC / DO-178C / NCHS / 自启动 SPC / PCI DSS / 航空 MEL /
  ISO 9001;B:FDA 522 / NRC 10 CFR 50.59 / PCAOB AS 1301 / W3C Process / BCBS 239),
  **12 个体系无一重复、无一落在本仓已有语料**,且**双方都推翻了自己的 P1**。
- **B 侧 P3R2 对 A 侧四条「硬内容」做了外推检验,三条判过度外推、一条判忠于原体系。
  本文档采用检验后的收窄版本**,而非 A 侧 P3R2 的原始表述。

---

## Verdict

**CONCERNS · converged · 0 unresolved · 定向 refactor,不 redesign。**

**五条到期义务是同一个病灶:完成全部定义在产生侧,从未走到「谁在何时读到什么、必须做什么、拿什么结账」。**

统一裁决形态 = **七问消费契约**:`normative_site`(载体**及其等级**)· `owner` · `trigger`(可达)·
`options`(**程序全定义**:known + unclassified → 具名解释者 → 留痕复审,**未分类不得自动通过**)·
`clock_or_reachable_event`(**两者皆无 ⇒ 受影响消费点 fail-closed,不伪造到期日**)·
`consumer_action` · `settlement_evidence`。

动作分类:**`-04` / `-05` / `-12` refactor · `-11` new · `-09` refactor + new。**

**K④ 直答:字面满足不算满足。** CN 1/0/2、HK 0/0/4 报 `not_estimable`;
**US 字面满足条件 1 不构成对 CN/HK 的重判依据**(该结论由本仓条件 1/2 量词冲突独立成立)。

**红线全守**:不解锁扩样与 E2 · 41 条盲标路 CLOSED · C6 数字不动 · 不当场改框架 schema。
🔴 **KG-42 同族未解**,双方一致签署「不解 + 具名敞口」。

---

## Evidence map

| 结论 | 来源 | 引用(≤15 words) | 反对/覆盖证据 |
|---|---|---|---|
| 五题同源:完成定义在产生侧 | P1-Opus §1 | 「没有一条写成『当某人读到某物并做了某事时,本条完成』」 | ⚠ A 侧 §3-3 自曝「我无法从内部区分确实同源与又在做同构叙事」 |
| 七问模板前五问 | P1-GPT §2 元层行 · P3R1-Opus §2 | 「`normative_site / owner / due_event / stop_or_options / obligation_path`」 | - |
| 补 `consumer_action` + `settlement_evidence` | P3R1-GPT §3 分歧 4 | 「五要件缺消费动作、结账证据」 | A 侧 P3R2 **全让**:自认「我的模板犯了它所诊断的病」 |
| `clock` → `clock_or_reachable_event` | P3R1-GPT §1 | 「本仓无自然时钟时,应写成 `clock_or_reachable_event`」 | 承 warn-registry README 局限 3(已实证无自然时钟) |
| 语义不可穷举 ≠ 程序不可全定义 | P3R1-GPT §3 分歧 2 | 「未分类默认不得自动通过」 | ⚠ A 侧 P3R1 曾主张「完备性不是目标」,P3R2 撤回并自认错 |
| `-04` 病不在「没搬进正文」 | P2-Opus §3 · P2-GPT §3 | OLRC「uncodified 是合法态」/ FDA 522「正文搬运本身不等于可消费」 | **推翻** A 侧 P1「登记顶替回写」 |
| 载体只强制「等级显式 / 可发现 / 可消费」 | P3R2-GPT §2 ① | 「OLRC 不支持本仓必须采用固定三级标签」 | 🔴 **覆盖** A 侧 P3R2 的固定三级标签(过度外推) |
| 不得要求复审主体与 owner 人员分离 | P3R2-GPT §2 ② | 「DO-178C 的独立性随安全保证目标成立」 | 🔴 **覆盖** A 侧 P3R2 该条(过度外推) |
| 低样本只要求「分市场判 + 显式状态」 | P3R2-GPT §2 ③ | 「不能直接移植精确三档或阈值」 | 🔴 **覆盖** A 侧 NCHS 三档;US≠CN/HK 依据改由本仓量词独立成立 |
| `-09` 必须新建 market 观测轴 | P2-GPT §3 · P1-Opus §1 | BCBS 239「分层可得性是汇总能力定义的一部分」 | **唯一判「忠于原体系」**;A 侧独立观察 `aggregation_probe` 零 market 轴 ⇒ 两路同结论 |
| 条件 1/2 量词不一致 ⇒ CN/HK 结构性不可满足 | P1-Opus §1 | 「条件 1 存在量词,条件 2 特定量词」 | B 侧 P1 **独立复证**(全文查 `market` 仅命中 grain 注释) |
| `-11` 消费者 = operator-chair 在 handback-review | P1-GPT §2 · P2-GPT §1 · P2-Opus §1 | PCAOB「缺接收主体、动作与完成证据」/ PCI「书面指派 + 本人正式接受」 | ⚠ B 侧 P1 §3-1 自曝:不确定该命令能否承载硬停点 |
| `-12` 加 catch-all 轴而非补第四行 | P2-Opus §1 · P2-GPT §1 | NRC/W3C「后续变化是否需重新授权,与原 decision 分开」 | A 侧 P1「补一行不够」被检索加严(补时钟维 + 授权人留痕) |
| `-05` 三态各绑方法/敞口/退出证据 | P2-Opus §3 · P2-GPT §3 | 自启动 SPC「<20–25 子组换方法而非等」;FDA Adequate/Inadequate/Revised | ⚠ **半推翻** A 侧 P1「给不产生数字的行为形态」 |
| 元层裁决 evidence_grade = `post-hoc-accepted` | P3R2-GPT §2 末 | 「解释者仍是最终 owner」 | **不得写 `independent`**(硬约束) |

---

## Intake recap

### X · 审阅标的(11 项 · 双方均全部读到 · **零 BLOCK,三个 TEXT fallback 块未触发**)
本仓 5:`ledger.jsonl`(五条末行)· v4 stage doc · `PRD.md` v1.1 · `HANDBACK-LOG.md` 第 37 条 ·
`warn-registry/README.md`。XenoDev-009 6:`spec.md` · `SLA.md` · `aggregation_probe.py` ·
migration `0023` · `codex-review/SKILL.md` §4.2 · T015 结果 JSON。

**五题来自五条到期义务**:`OB-009-pM3prime-v4-04`(载体缺失)· `-11`(消费者缺失)·
`-05`(触发条件不可达)· `-12`(选项集不完备)· `-09`(自我判据到期)。
**gate 留痕**:obligation gate 首查 COUNT 7 → `-01`/`-10` 判结账、五条**过表并入 X** → warn gate 首查 COUNT 0。

### Y · 审阅视角
工程纪律 · 测量效度/统计方法学 · 规范工程/policy authoring。

### Z · 参照系
对标 SOTA,**零重叠为佳**;禁复述本仓已有九面语料。实际:12 体系零重叠、零复述、零 tech-stack 深潜。

### W · 产出形态
verdict-only · decision-list(带 `obligation path` + `evidence_grade` 两列)· refactor-plan(落点到文件与节)。
**三项本文档全产**(见下三节)。

### K · 用户判准(摘要)
不重审 T016;审五条义务背后的同一件事「绑定落在哪儿」。① `-04` 该写进哪份文档的哪一节,
**且为什么 v4 当时没写(后半问更重要)**;② `-11` 定出「谁、何时、读到什么必须停」,**不要没有主体的句子**;
③ `-05` 在触发条件不可达期间**仍产生行为**,**不许看数造 N**;④ `-09` **字面满足算不算满足**;
⑤ `-12` 给能写回 §4.2 的答案 + 跨仓送达路径。**元层第⑥题**:v5 每条裁决自身须能答载体/消费者/触发/选项四问。
**不许动**:M1=pass 不解锁扩样与 E2 · 41 条 CLOSED · C6 数字 · 框架 schema。

### 收敛模式
**strong-converge** —— 残余分歧降级为 v0.2 note 且**必带 `due_gate`**。

---

## 元层第⑥题 · moderator binding 的活体标本(不占 W 配额)

**operator 裁决(已 honor)**:本轮 P1 **不按回声处理**,判为**弱收敛证据**。理由:该 binding 把
「预测都落空」与「即又是逐条相同」写成等价,而现实是 **A∧¬B**(处置倾向相同、四条具名预测互相落空)。
立法意图是防「两人没独立思考」,预测互相落空恰证明双方不知道对方会怎么判。

**⚠ 这正是本轮第⑤题(`-12`)的同构复现,且这次发生在 forge 自己的规则上** ——
条款枚举了 decision,而发生的是条款没枚举的那一格。

**两条附加约束的执行核验**:① P2 零重叠**未放松** —— 双方逐条申报检索面,12 体系零重叠、零复述本仓语料,
且 P3R1 双方各自点名了「被自己 P2 推翻的 P1 判断」(A:`-04` 成因框法、`-05` 半推翻;B:`-09` 翻为
refactor + new)。② 本 binding 的歧义**已登记为活体标本**,处置如下。

**一般化处置(写回条款)**:判定规则把判据 A 与 B 写成等价而现实给出 A∧¬B 时 ——
**落入 unclassified,默认不自动通过,由具名解释者裁决并留痕**,链路为
`unclassified → operator note → cross-model review → synthesis settlement`。

**本 note 自身的四问自检(元条款对它同样有效)**:载体 = `moderator-notes.md` ✅ ·
消费者 = 双方后续 phase ✅(P2/P3 均已回应)· 触发 = 本轮实际可达 ✅ · 选项 = ❌ **只裁个案,一般 fallback
由本轮七问补上**。
🔴 **`evidence_grade` = `post-hoc-accepted`,不得写 `independent`** —— **解释者仍是最终 owner**。

---

## Verdict rationale(W: verdict-only · 五题各一条可写回条款正文的短裁决)

**① `-04` 载体缺失** —— **每条 forge 裁决必须被裁定载体等级,且该等级必须显式、可发现、可消费。**
ledger 行可作合法一等载体(**「显式不入正文」是合法态**),但必须绑一条消费边:哪个 gate 在何触发下读它、
以何证据结账。**不预设三处镜像**;**不强制固定三级标签**(B 侧检验:OLRC 不支持)。
**K① 后半问(为什么 v4 没写)**:原解释「登记顶替回写」**已被 P2 推翻** ——
病不在「没搬进正文」,而在 ledger 行**没有反馈边、没有复审主体、也没被裁定载体等级**。

**② `-11` 消费者缺失** —— **消费者 = IDS operator-chair;时点 = 每次 `/handback-review` 在引用跨批失败率、
密度或一致性读数之前;停止条件 = 库不可读 / 被引用跑无对应行 / 删失未披露 / 同 caliber 下样本量变化而无预注册
选择规则 —— 命中任一即停止该结论与验收签署。** 指派须书面 + 本人正式接受,并留工作底稿。

**③ `-05` 触发条件不可达** —— **删除「历史足量后再说」这一静默态。** 每个被消费批次必须产
`insufficient_history` / `method_ready` / `recalibration_due` 之一,**每态绑 `{允许方法, 已知敞口, 退出证据}`**;
`insufficient_history` 的必载字段 = 自启动图族前 ~50 点的 **masking 敞口**。转态由预注册方法的适用前提决定,
**不看现数造 N**。(只给状态机会退化成「有状态无内容」的记账对象 —— 那正是本轮病灶本身。)

**④ `-09` 自我判据到期** —— **做 US 分解;CN/HK 报 `not_estimable` 并具名判定;PRD §6 条件 1 改为
「每个拟重判市场均有可解释的 per-market 跨次读数」,条件 2 逐市场成立。** `aggregation_probe.py` 必须
**新建 market 观测轴 —— 改措辞补不出来**(分层可得性是汇总能力定义的一部分)。
**字面满足不算满足**,此判由本仓量词冲突独立成立,**不靠外部标准背书**。

**⑤ `-12` 选项集不完备** —— **§4.2 加一条 catch-all 程序轴,而非补第四行**:未枚举动作一律 **fail-closed**,
由具名解释者签署 + 留痕复审;「修复后 ship」若被采纳,**必须携带修后强制复验**(验证轮不受名义四轮帽,
持续收敛可签续)**与授权人身份记录**。**跨仓送达**:条款载体在 XenoDev、裁决场在 IDS ⇒
**IDS 产逐字替换授权,operator 手工送达**;三 gate 未接线期间,承接义务挂 `forge:009-pM3prime:phase0` +
复核文件 hash。

**⑥ 保守失真 vs 乐观失真(K 结尾点名,不得沉默)** —— **需要不同处置强度**:两者共用
「逐字核验—更正—留 provenance」;**乐观失真可能误解锁 ⇒ 立即 fail-closed;保守失真默认纠偏 + 登记浪费,
仅当它触发不可逆/高成本动作时才阻断。** 本次 T016 的「无留痕」属后者。
⚠ **该条只有 B 侧作答,A 侧四份产出全程未表态** ⇒ 记为单侧结论(见 §underweights 2)。

---

## Decision matrix(W: decision-list · 带 `obligation path` + `evidence_grade`)

| # | 类别 | 项 | 落点 | obligation path(产生 gate → 消费 gate) | evidence_grade | P |
|---|---|---|---|---|---|---|
| 1 | **保留** | `-11` 消费者具名 = IDS operator-chair | PRD 规范句 + handback-review | `forge:...:v5:phase4 → ids:handback-review`(⚠ 未在 registry 接线表登记 · exposure 必填) | `independent` | P0 |
| 2 | **保留** | 五条的 `due_gate` 机制 + v4 元条款「本 verdict 不得犯它所诊断的病」 | `ledger.jsonl` · v4 stage §Verdict | `→ forge:009-pM3prime:phase0`(**已接线**) | `independent` | P0 |
| 3 | **调整** | `-04` 载体等级裁定 + 映射表**绑消费 gate 与结账证据**(等级显式/可发现/可消费,**不固定三级标签**) | `ledger.jsonl` + 相关正文 | `forge:...:v5:phase4 → forge:009-pM3prime:phase0`(已接线) | `SOTA-corrected` | P0 |
| 4 | **调整** | `-05` 三态 × {允许方法, 已知敞口, 退出证据} | `warn-registry/README.md` 状态表 + `SLA.md` E1 | `→ forge:009-pM3prime:phase0`(已接线) | `SOTA-corrected` | P0 |
| 5 | **调整** | PRD §6 条件 1 量词「至少一个」→「每个拟重判市场」;条件 2 逐市场成立 | `PRD.md` §6 | `→ forge:009-pM3prime:phase0`(已接线) | `independent`(量词冲突本仓自证) | P0 |
| 6 | **调整** | `-12` §4.2 加 catch-all 程序轴 + 授权人留痕 + 修后强制复验 | `codex-review/SKILL.md` §4.2 | `forge:...:v5:phase4 → xenodev:ship-gate`(🔴 **未接线** · exposure 必填 · 过渡期挂 phase0 + 文件 hash) | `SOTA-corrected` | P0 |
| 7 | **调整** | 失真处置分级:乐观 → fail-closed;保守 → 纠偏 + 登记浪费 | HANDBACK-LOG 处置口径 | `→ ids:handback-review` | `post-hoc-accepted`(单侧提出) | P1 |
| 8 | **删除** | `-05` 的「历史足量后再说」静默态 | `ledger` `-05` note | `→ forge:009-pM3prime:phase0` | `SOTA-corrected` | P0 |
| 9 | **删除** | `-12` 的「四轮硬顶即终局」读法(与 LOG 第 34 条先例冲突,且未标注这是口径选择) | SKILL §4.2 | `→ xenodev:ship-gate`(未接线 · exposure) | `SOTA-corrected` | P0 |
| 10 | **删除** | 「必须三处镜像」这一预设动作 | — | `N/A(预设被裁掉)` | `SOTA-corrected` | P1 |
| 11 | **删除** | 「把选项集语义补全」作为目标(改为程序全定义) | — | `N/A(diagnosis replaced)` | `independent`(双方对辩产生) | P0 |
| 12 | **新增** | `-09` market 观测轴 + CN/HK `not_estimable` 输出 | `aggregation_probe.py::_run_batch` 结果矩阵组装段 · `SLA.md` E1 | `→ xenodev:task-review`(🔴 **未接线** · exposure 必填) | `SOTA-corrected`(唯一「忠于原体系」项) | P0 |
| 13 | **新增** | `-11` handback-review 消费步(读 `census_run` + 四条停止条件 + 留底稿) | `/handback-review` 流程 + PRD | `census_run 写入 → ids:handback-review` | `independent` | P0 |
| 14 | **新增** | 七问消费契约模板本身 | 框架级(PROTOCOL / ledger schema) | **不当场改 ⇒ `→ forge:006:phase0`** | `SOTA-corrected` | P1 |
| 15 | **新增** | 元层 unclassified 处置链 `unclassified→operator note→cross-model review→synthesis settlement` | forge PROTOCOL / moderator-notes 机制 | `→ forge:006:phase0` | **`post-hoc-accepted`** | P1 |

---

## Refactor plan(W: refactor-plan · 三模块 · 落点到文件与节)

### 模块 A · IDS 正文与条款(`discussion/009/009-pM3prime/PRD.md`)
- **当前问题**:`-04` 定形内容三处 grep 全零命中;§6 条件 1 量词过弱;`-11` 无规范句。
- **目标态**:PRD 成为被裁定等级后**应当** codified 的那部分裁决的正文载体。
- **步骤**:1) §6 条件 1 量词改写 + 条件 2 逐市场;2) §6 增「低样本显式状态 + 具名判定人」小节
  (**不写数字档**);3) 增 `-11` 消费契约规范句(主体/时点/四条停止条件);4) `-04` 定形内容按等级裁定结果
  决定是否入 §6/§7 邻位。
- **风险**:模块 A **不得**膨胀成「三处同步」—— 该预设已被裁掉(matrix #10)。**代价 S。**

### 模块 B · IDS 治理机制载体
- **当前问题**:`census_run` 零消费者;`-05` 三态无载体;七问模板无处安放。
- **步骤**:1) `framework/obligations/ledger.jsonl` —— 只 append 本轮裁决 + obligation path,
  **不改 schema**;2) `framework/warn-registry/README.md` 状态表 —— 绑 `-05` 三态的方法/敞口/退出证据;
  3) `/handback-review` 命令流程 —— 增读 `census_run` 的消费步与硬停点。
- **风险**:🔴 B 侧 P1 §3-1 自曝**不确定** handback-review 能否在不改 SHARED-CONTRACT 前提下承载硬停点;
  若不能,该步降级为 v0.2 + exposure,**不得静默降级**。**代价 M。**

### 模块 C · XenoDev-009(跨仓 · IDS 只能产授权,不能直接改)
- **步骤**:1) `specs/009-pM3prime/spec.md` C4 行 / `SLA.md` E1 行 —— 按载体等级裁定结果同步
  (**不预设镜像**),E1 增 per-market 读数判据;2) `projects/004-pB/src/decision_ledger/extraction/aggregation_probe.py::_run_batch`
  结果矩阵组装段 —— 新建 market 轴,CN/HK 输出 `not_estimable`;
  3) `.claude/skills/codex-review/SKILL.md` §4.2 表格 —— 加 catch-all 行 + 授权人字段 + 修后强制复验。
- **送达**:IDS 产**逐字替换授权**,operator 手工送达。
- **风险**:三 gate 全未接线 ⇒ 相关义务一律 `consumer_wired: false` + `exposure` 必填;
  `-09` 实现成本未实测(A 侧 P1 §3-2 自曝未读 `derive_stratification_market`)。**代价 M–L。**

---

## v0.2 notes(3 条 · 双方一致 · 各带 `due_gate` + `exposure`)

1. **🔴 KG-42 同族未解(本轮最大敞口)** —— 七问的 `owner` 与「复审的独立性」在只有一个人的仓里
   不可同时满足。**跨模型、跨会话时间分离、operator 独立签收只算功能性缓解,不满足人员独立。**
   严禁用「已具名」冒充「已解决」。⚠ 同时:B 侧检验已判「复审主体须与 owner 人员分离」**属过度外推**
   ⇒ 也不得把它当硬要求倒逼。`due_gate`: `forge:006:phase0` · `exposure`: 同一 authority 自审,无组织隔离。
2. **可达事件源清单未验全** —— 本仓当前可达事件仅 gate firing 与 hand-back 到达两类,是否覆盖五条未验;
   未验期间按 fail-closed。`due_gate`: `forge:009-pM3prime:phase0`(下一轮首查)·
   `exposure`: 若无事件,fail-closed 可能**永久悬置**。
3. **`-09` 观测轴实现成本未实测** —— `due_gate`: `xenodev:task-review` ·
   `exposure`: 🔴 **该 gate 至今未接线**,成本与义务均可能不被复核。

---

## What this menu underweights(强制自批判)

**1 · 🔴 本轮亲手复现 `-04` 的形态。** 七问模板是**框架级对象**,其真正载体在 forge PROTOCOL / ledger schema,
而红线禁止当场改 ⇒ **模板现在只活在这份 stage doc 里**,与 `-04`「只活在一个 JSON 字段里」同形。
缓解仅为已登记 `→ forge:006:phase0`(matrix #14);**在 006 消费之前,它与 `-04` 同病。** 这是元条款对本轮的实打实命中。

**2 · 保守/乐观失真那条是单侧结论。** K 明确要求「不要沉默带过」,**A 侧四份产出全程未表态**,
verdict ⑥ 全部来自 B 侧 P1 一段。它未经零重叠检索、未经对辩 ⇒ `evidence_grade` 只能 `post-hoc-accepted`。

**3 · 12 个体系全部来自受监管行业**(航空 / 核 / 医疗 / 审计 / 银行 / 支付 / 法典编纂),
其独立性与强制力**来自组织与法律,本仓两者皆无** ⇒ 移植的是**形态,不是效力**。
证据:B 侧检验把 A 侧四条硬内容中的**三条判为过度外推** —— **移植失真在本轮真实发生过**,
这次被检验拦下;**没被交叉检验的那些呢?**(A 侧未对 B 侧的 FDA / NRC / PCAOB / W3C 做同等外推检验。)

**4 · 零 build 侧实证(连续第三轮)。** market 轴、`census_run` 消费步、catch-all 行能否实装,
**全是推演**;memory `forge-verdict-vs-empirical-ship` 的教训原样适用,且本轮**未预置同轴熔断**
(不像 v4 的「证不出则 fallback」)。

**5 · P1 不按回声处理这一裁决本身未被独立检验。** 它由 operator 单方解释,而 operator 同时是本轮
五条义务的产生者与最终消费者。**若该裁决判错,本轮 P1 的六题同姿态就是第五轮回声,而无人会发现。**

**6 · Y 视角未含成本/安全。** `-09` 与 catch-all 的代价只有 S/M/L 粗估,零一手数据;
`census_run` 与被引用 batch 的可机械关联性(B 侧 P1 §3-3)**本轮未被任何一方解决**。

**7 · forge versioning 提示** —— 任一发生即应跑 **v6**:(a) handback-review 被证不能承载硬停点;
(b) market 轴实测成本高一档;(c) forge 006 拒收七问模板或 unclassified 处置链;
(d) 三 gate 接线状态发生变化。

---

## Decision menu(for human)

### [A] 全量落地(推荐)
三模块 refactor plan 全做 + 按 decision matrix 的 `obligation path` 列执行 Step 6.5 义务登记
(15 行中 P0 共 10 行)。
⚠ **本轮 W 未含 `next-PRD` ⇒ 没有可直接喂 `/plan-start` 的 PRD 草案**;且本轮裁决是**治理层条款**而非产品需求,
**不需要 fork 出 PRD branch**。落地面 = IDS 条款正文 + `ledger` append + XenoDev **逐字替换授权**(手工送达)。
若确需进 L4 产品线,选 [B] 起 v6 并把 `next-PRD` 加进 W。

### [B] 跑 forge v6
```
/expert-forge 009-pM3prime     # Phase 0 重设 X / Y / Z / W / K
```
适用:§underweights 7 的四个触发之一发生;或需要把**七问模板**送去 `forge 006`(框架层)而非本 fork 再议。

### [C] 局部接受
- ✅ 建议采纳:matrix #1–#6、#8、#9、#11–#13(P0 全集 · 直接消化五条到期义务)
- ⏸ 建议挂起:#14 / #15(框架级,须走 006)· #7(单侧结论,等 A 侧或下一轮检索背书)
- ❌ 建议拒绝:任何把「跨模型 + 时间分离 + operator 签收」当作 KG-42 已解的表述

### [P] Park
```
/park 009-pM3prime
```
⚠ **选此需知**:五条义务在本轮 gate 已判**「过表 = 并入本轮 X」**,即它们的兑现路径**就是本 verdict**。
park 意味着五条**既不会被兑现,也不再有下一次被同一理由拦住的机制** ——
这与 v4 §underweights 3 记录的形态完全相同。

### [Z] Abandon
```
/abandon 009-pM3prime
```
**本轮证据不支持 abandon**:五题全部是可执行的条款级缺陷(refactor / new),无一指向 idea 本身不成立。
仅在 operator 决定整条 009-pM3prime 线下线时使用。

---

## Forge log

| Phase | A 侧(Opus 4.7 Max) | B 侧(GPT-5.5 xHigh) | 结果 |
|---|---|---|---|
| P1 | 六题倾向 · 3 条具名预测 | 六题倾向 · 2 条具名预测 | 六题几乎逐条同,**四条预测互相落空** ⇒ operator 裁**弱收敛证据**,不按回声处理 |
| P2 | **7 次检索 / 7 体系**(超模板 21%,已声明) | **12 次检索 / 5 体系** | **零重叠 · 12 体系 · 零复述本仓语料** · **双方都推翻自己的 P1** = 连续四轮回声后**第一次真破** |
| P3R1 | 提 3 条分歧(超模板 26%,已声明) | 三条全裁 + 自提分歧 4 | 4 条分歧全部进 R2 |
| P3R2 | **三全让一让**(五要件 → 七问) | 收敛 + **对 A 侧四条硬内容做外推检验**(3 过度外推 / 1 忠于原体系) | **converged · 0 unresolved** |

- **v5**(2026-08-16)—— verdict:「五条义务的完成全部定义在产生侧;改写为**七问消费契约**,
  未分类动作一律 fail-closed,无时钟则退可达事件、再无则停。」
- **v4**(2026-08-14)—— verdict:「机制存在,但没绑定谁在何时做什么。」
- **v3 / v2 / v1** —— 审阅对象依次为:产出信号的那台机器 / 那套验收的测量效度 / 金标标注的验收主体。
