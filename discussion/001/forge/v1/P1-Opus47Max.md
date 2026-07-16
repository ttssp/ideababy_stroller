# Forge v1 · 001 · P1 · Opus(Claude Code main)· 独立审阅(no search)

**Timestamp**: 2026-07-15T13:22:01Z(actual model: Opus 4.8;文件名沿协议约定)
**Searches used**: NONE in this round.
**Visibility**: I did NOT read other reviewer's P1.
**Reviewer stance**: 审阅人 — 评判已存在物,不是 daydream。

## 0. 我读到的标的清单 + 阅读策略

- 我读了(8/8,无跳过):
  - `TEXT:` proposal §001 原文 → 全 5 段(背景 seed)
  - L3 stage doc → Candidate A/B 菜单 + 信任建立机制三件套出处 + Honesty check
  - **PRD v1.2** → O4 全文 + 两节 Moderator injection response + Open questions #3
  - **触发 hand-back(20260715)** → §1/§2/§3 全文,operator 三条批评原话
  - HANDBACK-LOG → 11 条决议全序列(gate 演进脉络)
  - L3 moderator-notes → injection @07-10(77a5176)+ injection @07-13(价值重定义)
  - 首跑 FAIL hand-back(20260711)→ §2 决议链 + 诊断信号
  - XenoDev dogfood-backlog → KG-B4(:525)/ KG-B7(:588)/ KG-B8(:602)全文
- 我跳过的:无。
- **K 摘要**:本次审的不是 radar 产品本身,是 **P0.2 盲测 gate 的形态治理**。operator 三条批评(①非可靠打分器 ②要留痕可审计非盲测签字 ③要边用边迭代非一次性前置)+ 同簇裁 KG-B8/B4/B7。K 点名两个预置张力:v1.2「保留 RERUN-PASS 唯一前置」vs hand-back §3.A「彻底去二值硬前置」的线画在哪;T004-A1 十四轮硬化被 B8 推翻前提的过度投资教训。K 明言:防 V4 精神要保留、T010/T011 新解锁条件不能悬空、不看沉没成本。
- **阅读策略**:按 Y=工程纪律优先读 gate 演进链(两次 injection → v1.1 → v1.2 → 拒签)与 KG 三条;按 Y=架构设计读 PRD O4 双层结构 + DAG 前置关系;按 Y=产品价值读 UX principles 与 operator 价值重定义的咬合。

## 1. 现状摘要(按 Y 视角组织)

### 视角 A · 工程纪律

gate 的演进是一条**单调退让链**:v1.0 三要件全挡 → 首跑 FAIL(①②过,③空)→ injection 77a5176 把 gate 右调为「初始 smoke test」、长期主锚移 O2+O7 → v1.2 硬门槛收敛①②、③降级使用期校准、且认定「首跑①②实证即构成 PASS 证据」→ 07-13 重跑时 operator 填①②、拒③、**拒签形态本身**。每一步都是 operator 侧收窄、机制侧保形。纪律面守住的部分很实:首跑 FAIL→STOP 生效、T010/T011 未起、预算没烧(防 V4 铁律走通)。机制侧的强制现状:KG-B4 记明 `evaluate_gate` 是无 wiring 的纯库函数,STOP 只靠 parallel-builder 读 markdown `depends_on` 的程序纪律,「T004 已 merge ≠ gate PASS」;KG-B7 记明 codex R12-R14 三连 bypass(签字重放 / seed 爆破 / FAIL-reason oracle),已修 run-binding + 256-bit nonce + reason 泛化,根因是「确定性对答案 + answer-key 可复用 + 可无限重跑」。

### 视角 B · 架构设计

PPV 把 P0.2 定为「项目最大不确定性锚点」,DAG 硬编码 RERUN-PASS artifact 为 T010/T011 唯一前置。信任架构在 v1.1 起已是**双层**:初始层(smoke gate)+ 长期层(O2 三击回溯 + O5/O7 journal 后验)。结构上值得注意的不对称:O2 留痕是 **in-band** 的——每条判断内嵌证据链,可随使用逐条核验、可机器检查完整性;盲测签字是 **out-of-band** 的——停机、人肉全读、二值裁决。operator 批评②要求的「每条边留 trace + 抽查 + log 回溯」与 O2 既有要求高度重叠:满足批评②在架构上**不是新增机制,而是把 O2 从产品功能提升为验收机制**。三条 KG 的层次关系清楚:B8(形态该不该存在)是 B4(怎么机器强制)与 B7(怎么防作弊)的上游;裁 B8 会级联改写下游两条的题面。

### 视角 C · 产品价值

operator 的价值重定义(v1.2)已明确:核心价值 = 跟踪动态、梳理 SOTA 脉络、及时同步,「不必是 operator 未知的」。产品自己的 UX 原则写着「判断先行,证据随取」「单次评估体验 > 长期库完整性」——而盲测签字仪式恰是「停下来考试」,operator 原话「费时费力、只得 local 解」。实证正资产存在:识伪机制有牙(首跑精准命中负控 slice-1,两次真跑要件①②均可判)。威胁模型与用户错配也是实证:KG-B7 自己写着「operator 是自己 · 无对抗动机」,却花 14 轮把 gate 硬化到防 operator 作弊。

## 2. First-take 评分(按 Y 视角)

| Y 维度 | 倾向 | 理由(引用 §1 现状) |
|---|---|---|
| 工程纪律 | **refactor** | FAIL→STOP 防 V4 精神必须保留(首跑已证其值钱);但强制点错位——「人肉盲测二值签字」既无机器强制(B4)又被用户拒(B8)。强制点应移到 in-band:留痕完整性可机器检查,抽查发现问题可回溯,这才是能被真正 enforce 的纪律形态。 |
| 架构设计 | **refactor** | 双层信任架构本身是对的,错在初始层用了带外仪式。砍带外签字、把 T010/T011 解锁改为机器可验的留痕验收(具体形态待 P2/P3 定);B4 在新形态上要重新定义(任何残留 FAIL→STOP 语义仍需机器强制),B7 随 answer-key/签字机制退役而大部分消解。 |
| 产品价值 | **refactor(对盲测仪式偏 cut)** | 验证范式必须贴「边用边审计」工作流(K 第一在乎项)。识伪能力是实证正资产,保留为**可选的使用期校准活动**;「签字-解锁」耦合砍掉。仪式与产品自己的 UX 原则相抵,不砍则产品哲学自相矛盾。 |

## 3. 我现在最不确定的 3 件事

1. **T010/T011 新解锁条件的具体形态,哪种有先例可循?** 候选:(a) 留痕验收——机器检查 trace 完整性 + operator 抽查 N 条通过;(b) 直接解锁 + O2 硬化为 in-band gate + O7 兜底;(c) 非阻断 smoke 告警(叙事崩坏才拦)。我希望 P2 搜 human-in-loop eval / provenance-based acceptance / production eval 后验闭环的先例,看工业界「pipeline 信任到什么程度才在其上建下游」怎么裁。
2. **去掉二值 gate 后,B4/B7 是否真消解?** 我的初步判断:B7 随签字/answer-key 机制整体退役而消解;但 B4 的本质(FAIL→STOP 的机器强制)在**任何**保留阻断语义的新形态里都还在,只是强制对象从「PASS artifact 存在」变为「留痕完整性检查通过」。希望对方 P1/P3 给出精确映射:哪个子问题随哪种形态选择而死。
3. **抽查审计的统计功效是否真优于盲测,还是只是更便宜 + 更贴工作流?** 若 briefing 错误是 subtle 的,随机抽查的功效未必高;诚实的地基可能是「O7 后验才是唯一真信号,但它慢」。K 要求实事求是——要警惕用一个新剧场替换旧剧场:如果留痕验收也给不出统计意义上的可信性证明,verdict 里必须把这一点写穿,而不是假装新形态解决了功效问题。
