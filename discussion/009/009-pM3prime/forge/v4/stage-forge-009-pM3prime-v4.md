---
doc_type: forge-stage
fork_id: 009-pM3prime
forge_version: v4
created: 2026-08-14
convergence: converged
open_disagreements: 0
v02_notes: 3
w_forms: [verdict-only, decision-list, refactor-plan]
synthesized_by: main-process(承 v2/v3 先例 · 未起 forge-synthesizer 子代理)
trigger: IDS /handback-review 009 第 36 条 · T015 M1=pass + 四条 obligation 在 forge:009-pM3prime:phase0 到期
reviewers: [Claude Opus (A), GPT-5.6-Sol xhigh (B)]
---

# Forge Stage · 009-pM3prime · v4 · 「机制存在,但没有绑定谁在何时做什么」

## How to read this

前三轮的审阅对象依次是:**v1** 金标标注的验收主体 · **v2** 那套验收的测量效度 · **v3** 产出信号的那台机器。
**v4 审的是这套治理机制自身** —— 条款、义务、gate 之间的传导。

触发源是四条义务在 `forge:009-pM3prime:phase0` 同时到期(这是该 gate **第一次真的开火**),
加上 T015 聚合探针交回的 **M1 = pass**。

⚠ **本文档的可信度分布不均匀,请按此读**:
**P1 阶段双方四题倾向逐条相同 —— 这是本 fork 连续第四轮 P1 零分歧收敛,应视为回声。**
**可采信的收敛来自 P2**:双方检索面**零重叠**(A:标注分歧 / ML drift / OPA / Chrome / 预注册;
B:NIST 计量学 / RFC 5848 / RFC 9162 / ModSecurity / Kubernetes KEP),且**各自推翻了自己 P1 的一部分**
(A 侧 4 条 / B 侧 3 条)。⇒ 本 verdict 的分量在 P2 与 P3,不在 P1。

---

## Verdict(W: verdict-only)

**CONCERNS · converged · 0 unresolved。**

**四条到期义务是同一个病灶的四个断面:机制存在,但没有绑定「谁在何时做什么」。**

**① M1 = pass 欠一次具名裁决(采广读)。**
依据**只**是本地三载体(forge v3 正文 :277 · decision matrix :163 · `OB-...-07` 标题)+ 已接线的消费点 +
`OB-16` 本身,**不得援引外部规范权威**。**本次裁决内容**:接受 M1 为**固定批可比性**证据;
**不作效度代理 · 不外推 · 不解锁扩样与 E2**。
rationale **必须同时载明**两项风险输入:
(i) 一致率上升**无法区分**噪声去除与**歧义抹除**;
(ii) 6 个跑的 `census_verdict` **全部** `below_threshold_advisory`。

**② 现状跨批次比较不可信。**
`OB-15` 的兑现判据 = **四前提合取**:① 预注册观察/停止边界 ② 逐 attempt exposure 可计
③ 已观察失败的结果及**精确时间/区间**留存且**删失可识别** ④ 失败批次内容身份可比。
**四者证不出则 fallback 到写穿透或等价耐久回执。** 不写死实现。

**③ 监测周期已定形,重校准间隔未定形。**
已定:每个**被消费的批次**必测必落库;身份/口径变化(模型 · `system_fingerprint` · 语料批次 ·
`caliber_version`)**立即**启动新基线;**XenoDev 产证,IDS operator-chair 接受基线与升版**。
未定:统计型重校准间隔 —— 记为**具名敞口**(非「优化项」),须带消费点。

**④ C4 convert 判据 = 过程证据 + 结果证据 + 具名批准 + 版本化回退,四者合取。不给数字。**
版本化回退语义 = **历史不可变;授权被后续 `caliber_version` supersede**
(新版本只撤销旧版的**未来消费权**,旧阈值/旧证据/当时裁决永久保留可查)。

**⑤ 停止增列例证,转向动作绑定。**

🔴 **贯穿全部四条的元条款**:**本 verdict 自己不得犯它所诊断的病。**
本轮产出的每一条 v0.2 note **必须带 `due_gate`**,且 `due_event` 语义为
**「义务登记后的下一次 firing」——正在发生的这一次 phase0 不计为履约**。
否则一条无消费点的 note 就是同一形态的第五处实例,而且是本轮亲手制造的。

⚠ **边界(未触碰,不得被下游解读为松动)**:不解锁扩样与 E2 · 41 条盲标路 v0.1 CLOSED 不重开 ·
不修改 C6 冻结门槛**数字**(本轮只议其**形态**中的可回退性)· 未改 `specs/`。

---

## Evidence map

| 来源 | 侧 | 逐字引文 | 用在哪 |
|---|---|---|---|
| NIST 测量过程 | B | 统计控制「**can only guarantee comparability among measurements**」 | ①:M1=pass 只证可比性,不证准确 |
| NUTMEG(2025-07) | A | 「variation should be treated as **signal** rather than noise」 | ①④:分歧是信号 |
| Hate-speech 分歧建模(2026-06) | A | 「**filtering non-consensus samples results in over-optimistic results**」 | ①:逐字对应 M2 留存口径 |
| CrowdTruth 2.0 / Perspectivist | A | 分歧揭示**歧义**而非错误;整体转向显式建模分歧 | ① |
| NIST 有删失的失败率 | B | 前提是「**exact times of failure are recorded**」 | ②:第三前提的来源 |
| RFC 5848 / RFC 9162 | B | 缺口可检测审计存在,但**审计失败后的动作不规定** | ⑤:形态非本仓独有 |
| ModSecurity | B | 「**Every Ruleset can have false positives in new environments**」→ DetectionOnly 先行 | ④:需真实误杀审阅 |
| Kubernetes KEP | B | graduation criteria / flake-free e2e / PRR 批准 / rollback 并列必填 | ④:四者合取 |
| OPA Gatekeeper | A | dryrun→deny 三档齐备,**不给任何晋级判据**(否定性结果) | ④ |
| Chrome/Blink | A | 「**There is no threshold for which removal is necessarily safe**」,改规定过程量 | ④:不给数字 |
| ML pipeline provenance 文献 | A | **否定性结果** —— 无一定义「哪些记账须挺过回滚/崩溃」 | ②:答案只能本地推 |
| 预注册文献 | A | **反向结果** —— 收益被质疑,「may increase publication bias」 | ①:**撤回**外部支撑 |
| `census.py:728-731` docstring | A | 「跨批次比对……**不做这条,前面全是空话**」 | ②:本地唯一判据来源 |
| `SLA.md:136` | B | 目标列要求「每批产可复核的跨次一致性读数」,判据列 SQL 只验身份/attempt 行 | ⑤ 第四处 |
| `OB-...-09` 标题 vs satisfied note | B | 标题要求「定形」,satisfied 只表示「上议程」 | ⑤ 第三处 |

---

## Intake recap

**X** 10 项(本仓 6 + XenoDev-009 4)· 双方**均全部读到,零 skipped**,未触发 BLOCK。
**Y** = 工程纪律 · 架构设计 · 测量效度/统计方法学。**Z** = 对标 SOTA。
**W** = verdict-only + decision-list + refactor-plan。**收敛** = strong-converge。
**gate**:obligation gate 首查 COUNT 4 → operator 四条全裁「过表」→ 复查 0;
warn gate 首查 COUNT 1 → 三态裁决 defer(operator-chair 签署)→ 复查 0。

---

## Verdict rationale

**① 为什么采广读。**
条款歧义的载体分布是 **3:2** —— 广读在 forge v3 正文 :277、decision matrix :163(且标注「已接线」)、
`OB-...-07` **标题**;窄读只在结果矩阵表与 `OB-...-07` **note**。
**少数派口径赢了,赢的方式是它更靠近执行者** —— T015 hand-back 读的是结果矩阵表。
⇒ 单改正文而不改那张表,等于重演本次。

但**支撑理由必须换**:A 侧原打算援引预注册规范,检索后发现外部证据**不站在这边**
(有文献论证预注册收益被高估、甚至可能加剧发表偏倚),**故主动撤回该支撑**。
⇒ ① 只能靠本地机制论证。这也意味着窄读的辩护(「pass 需要的只是被记录并被看见」)
**曾被认真对待**,最终被 3:2 的载体分布 + 已接线消费点 + `OB-16` 的存在压过。

**② 为什么是判据不是实现。**
A 侧 P1/P2 主张「finding (a) 不可 defer,落点是写穿透」;B 侧引 NIST 有删失分析指出
**写穿透不是唯一可信形态**。A 侧全盘让步 —— 这正是 memory `forge-verdict-vs-empirical-ship`
的正面解法形态「A + 判据 + 证不出则 B」,写死实现会重演 v3 §underweights 1 批评过的「没写 fallback」。
⚠ **A 侧同时承认自己引用不完整**:P2 §1 逐字抄了 NIST 的「exact times of failure are recorded」,
却在 P3R1 把它漏出三前提之外,由 B 侧补成第三前提。

**③ 为什么周期分成两半。**
K 的原始要求是「接受结果含提取器误差,前提是**有定期校准机制**」。
B 侧的结构性拆分成立:**监测周期**(每个被消费的批次)与**重校准间隔**(何时判定仪器已漂移)是两件事。
前者已定形且可执行 —— 本仓**没有自然时钟**(warn registry README 局限 3 已实证),
**以批次为索引是唯一诚实的周期**。后者定不出来:NIST 的控制图路径要求多点历史,
而本仓全部可用点只有两跑 Jaccard 0.44、本次 J_1 = 0.4078、历史密度 41/73/71 —— **控制图画不出来**。
⚠ **称谓之争的结论**:剩下那块是**具名敞口**不是「优化」——
优化是让已有能力更好,而这里缺的是**一项能力**:仅有「身份变化即新基线」触发器时,
**身份稳定而缓慢漂移的场景结构上无人覆盖**,而 NIST 控制图存在的理由正是它。

**④ 为什么四者合取、且必须能回退。**
三个独立工业先例(OPA / Chrome / KEP)**没有一个给数字阈值**;Chrome 明写
「没有一个阈值使移除必然安全」,改为规定**过程量**。⇒ K 的「给形态不给数字」不是本仓偏好,
是成熟弃用流程的共同形态。
KEP 另加一项双方 P1 都没有的:**rollback 与 convert 并列必填**。
这在本仓触发一条结构性冲突:C6「预注册不可回改」+ v2「移动球门」判据意味着
**convert 一旦升版,退回 report-only 会被自己的反自欺条款挡住** ⇒ convert 是**单向门**。
出路采 (b):**回退 = 再升一个新 `caliber_version`,撤销旧版未来消费权,历史不动。**
⚠ A 侧原措辞「旧结论**作废**」被 B 侧改正 —— 那可能暗示追改历史;终稿统一为
「历史不可变;授权被后续版本 **supersede**」。

**⑤ 为什么停止增列。**
B 侧带回 RFC 5848 / 9162:成熟标准同样提供缺口可检测审计,却**不规定审计失败后的动作**。
⇒「机制有、动作无」**非本仓独有的纪律问题**。继续找第五处、第六处的边际收益低于把已知四处**绑上动作**。

---

## Decision matrix(W: decision-list)

| # | 对象 | 判 | 内容 | obligation path(产生 gate → 消费 gate) |
|---|---|---|---|---|
| 1 | 「结果三态必须回 forge 裁决」条款 | **调整** | 广读入正文;**同步改 v3 结果矩阵表 pass 行**(不改表则歧义仍在) | `forge:...:v4:phase4 → forge:009-pM3prime:phase0`(**已接线**) |
| 2 | 本次 M1=pass 的具名裁决 | **新增** | 固定批可比性证据 · 不解锁 E2 · rationale 载明歧义抹除风险 + 6 跑密度全低 | `→ forge:009-pM3prime:phase0`(**已接线**) |
| 3 | `OB-15` 兑现语义 | **调整 + 新增** | 四前提合取 + 证不出则 fallback;**删除**「机制存在即可信」的隐含等价 | `→ xenodev:handoff-intake`(🔴 **未接线** · `exposure` 必填) |
| 4 | 校准监测周期 + 责任分离 | **新增** | 每消费批次必测落库 · 身份/口径变化即新基线 · XenoDev 产证 / IDS operator-chair 接受升版 | `→ forge:009-pM3prime:phase0`(**已接线**) |
| 5 | 统计型重校准间隔 | **登记议题** | **具名敞口**(非优化项)· 不臆定 N · 待 control history 足量后预注册方法与 N | `→ forge:009-pM3prime:phase0` · `due_event` = **登记后的下一次 firing** |
| 6 | C4 convert 判据 | **调整** | 过程 + 结果 + 具名批准 + 版本化回退,四者合取 · 不给数字 | `→ forge:006:phase0`(C4 warn 已 defer 至此 · **已接线**) |
| 7 | 版本化回退语义 | **新增** | 历史不可变;授权被后续 `caliber_version` supersede。**删除**「回退 = 改旧结论」的表述 | `→ forge:006:phase0` |
| 8 | `SLA.md:136` 判据列 | **调整** | 补「跨次一致性读数**存在性**」判据 —— 目前四个「必须」里最重要的那个**零判据** | `→ xenodev:handoff-intake`(🔴 **未接线** · `exposure` 必填) |
| 9 | per-market 跨次分解 | **登记议题** | **非** v4 硬产出(判据膨胀);但「当前未满足」**必须**落 `PRD.md` §6 条件 1 注记 | `→ forge:009-pM3prime:phase0` · 下次 firing 决定是否升义务 |
| 10 | 继续枚举第五/第六处 | **删除** | RFC 5848/9162 证明该形态非本仓独有;边际收益低于动作绑定 | `N/A(diagnosis replaced)` |

---

## Refactor plan(W: refactor-plan · 三组 · **组内顺序是硬的**)

### A · 条款同步组(**三处必须一起改,漏一处仍留歧义**)

1. forge v3 stage doc 的**结果矩阵表 pass 行** —— 补「pass 亦欠具名裁决」;
2. `framework/obligations/ledger.jsonl` 中 `OB-...-07` 的 note 口径(append 新行,不改历史行);
3. `discussion/009/009-pM3prime/PRD.md` §6 条件 1 —— 加注「本条**未**因 T015 满足:该读数为全局,非 per-market」。

### B · 记账组(可观测性)

1. `XenoDev-009:projects/004-pB/src/decision_ledger/extraction/census.py` —— attempt log 覆盖四前提
   (或证不出则改写穿透/等价耐久回执);
2. `XenoDev-009:specs/009-pM3prime/SLA.md:136` —— 判据列补「跨次一致性读数存在性」SQL。

⚠ 两项均落在 `xenodev:*`(**未接线**)⇒ 登记义务时 `consumer_wired: false` + `exposure` 必填。

### C · C4 三处同步组(**三个 site 缺一即仍剩一个假绿源**)

1. IDS `PRD.md` §7 红线 3;
2. `XenoDev-009:specs/009-pM3prime/spec.md` C4;
3. `XenoDev-009:specs/009-pM3prime/SLA.md` E1「提取确定性」行。
三处采用**同一套**四合取 convert 判据 + 同一套版本化回退语义。

---

## v0.2 notes(残余分歧降级 · 双方一致 · **每条必带 due_gate**)

1. **统计型重校准间隔** —— 具名敞口;待 control history 足量后**预注册**方法与 N(不得看数后造 N)。
   `due_gate: forge:009-pM3prime:phase0` · `due_event: 义务登记后的下一次 firing`。
2. **per-market 跨次分解** —— 非 v4 硬产出;当前未满足先落 `PRD.md` §6 条件 1。
   `due_gate: forge:009-pM3prime:phase0` · 下次 firing 决定是否升为义务。
3. **`xenodev:*` 三 gate 接线** —— 接线前相关义务一律 `consumer_wired: false` + `exposure` 必填。
   `due_gate: forge:009-pM3prime:phase0` · 下次 firing 复核接线状态。

---

## What this menu underweights(强制自批判)

**1 · 🔴 A 侧检索能力本轮是残的,零重叠保证由 B 侧单边承担。**
A 侧 `WebSearch` 环境层故障(后端 400),只剩 arXiv 结构化 API + 对已知 URL 的定向抓取 ——
**「我只找到我已经猜到它存在的东西」本身就是回声室形态,只是换了入口**。
B 侧 15 条开放网检索确实补上了发现能力,**但若 B 侧检索面存在系统性盲区,双方会一起错,而本轮无从发现**。
⇒ 本轮 SOTA 对标判为**不降级**,但它的正交性依赖单边。

**2 · P1 阶段对本 fork 已连续四轮不产生分歧。**
本轮靠 P2 破,但这意味着「双方独立 P1」这一机制在本 fork 上的边际价值应被重估 ——
它连续四次只产出了回声。**该不该继续为它花一轮,是 forge 协议层的问题,不是本 fork 的。**

**3 · 🔴 本轮最大的自造风险敞口:四条义务已在 ledger 里显示为 `satisfied`。**
它们的 `satisfied` 语义是「已被本轮 forge 消费(上议程)」,每行 note 都写死了兑现判据。
**但账面上它们已经是 satisfied。** 若本 verdict 不落地,`forge:009-pM3prime:phase0` 下次开火时
**不会再拦住它们** —— 账面已清、实质未做。
⇒ **本 verdict 的落地不是可选项,它是那四条义务唯一的真实兑现路径。**

**4 · 本轮零 build 侧实证(同 v3 §underweights 1)。**
四前提能否在 `census.py` 现有连接管理下实装、`SLA.md` 的跨次读数存在性 SQL 具体怎么写 ——
**全是推演**。memory `forge-verdict-vs-empirical-ship` 的教训在此原样适用;
fallback 分支(证不出则写穿透)是本轮预置的熔断,**但它有没有被真正触发过,只有 build 侧知道**。

**5 · per-market 的排除理由是程序性的,不是实质性的。**
排除它是为防判据膨胀(v3 §underweights 4 的教训),**不是因为它不重要** ——
它同时是 `PRD.md` §6 科学重判条件 1 未满足的载体,而分解成本近零(`trial_ledger` 本就是 `market×horizon` grain)。
**下次 firing 若仍不处置,应视为拖延而非节制。**

**6 · 🔴 ④ 的「具名批准」在本仓只有一个人。**
过程证据、结果证据、版本化回退三项都可机械化;唯独**「具名批准」的独立性无法靠机制保证** ——
本仓的 operator-chair 与提出 convert 的人是同一个人。
**这与 KG-42(无合格第二源)同族**,只是换了个断面:v1-v2 争的是标注的第二源,这里是**批准的第二源**。
本轮**没有处理它**,也不应假装 KEP 的 PRR 批准形态能直接移植 —— PRR 的独立性来自组织,本仓没有组织。

---

## Decision menu(for human)

**[A] 全量落地** —— 三组 refactor plan 全做 + 按 decision matrix 登记义务。
最贵,但唯一能让四条 `satisfied` 义务真正兑现的路径(见 §underweights 3)。

**[B] 只做 A 组(条款同步)+ 登记义务** —— 先消歧义、先接动作,把 B/C 两组交下一轮 build。
成本最低且直击本轮病灶;代价:`SLA.md` 判据缺口与 C4 三处同步继续挂着。

**[C] 局部接受** —— 指定采纳哪几行 decision matrix,其余登记议题。

**[P] Park** —— 本轮 verdict 入库不落地。⚠ **选此需知**:四条义务账面已 `satisfied`,
park 意味着它们**既不会被兑现、也不会再被 gate 拦住**。

---

## Forge log

| Phase | A 侧(Opus) | B 侧(GPT-5.6-Sol xhigh) | 结果 |
|---|---|---|---|
| P1 | 1694 汉字 · CONCERNS | 1040 汉字 · CONCERNS | 🔴 四题倾向**逐条相同** = 连续第四轮回声 |
| P2 | 1539 汉字 · 6 条检索(**WebSearch 故障**,4 arXiv API + 2 定向) | 788 汉字 · **15 条开放网检索** | **零重叠** · 双方各自自我推翻(A 4 条 / B 3 条) |
| P3R1 | 1427 汉字 · 提 3 条分歧 | 867 汉字 · 三条全裁 + 自提分歧 4 | 4 条分歧全部进入 R2 |
| P3R2 | 1524 汉字 · **三让一守** | 749 汉字 · 采纳守住项 | **converged · 0 unresolved** |

**总计 9,628 汉字。**
**A 侧让步 3 条**(四前提 · 回退措辞 · per-market 排除),其中一条附自承引用不完整;
**B 侧让步 2 条**(具名敞口称谓 · v0.2 note 必带 due_gate),并补一条 A 侧未想到的限定:
**`due_event` 必须是「登记后的下一次 firing」,正在发生的这次 phase0 不计为履约。**
