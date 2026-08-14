# P3R2 · Opus · forge 009-pM3prime v4

**Phase 3 Round 2 · finalize · convergence_mode = strong-converge · NO new search**

---

## §1 我对每条分歧的最终立场

### 分歧 1 · `OB-15` 三前提 vs 四前提 —— **全盘让步,采对方**

对方补的第四项(「已观察失败的结果及精确时间/区间留存、删失可识别」)**正是我引了却没有落成前提的那一句**
—— 我在 P2 §1 逐字抄了 NIST 的 caveat「exact times of failure are recorded」,却在 P3R1 把它漏出了三前提之外。
**这是我这侧的引用不完整**,对方补得对。终稿采**四前提**,证不出则 fallback 到写穿透或等价耐久回执。

### 分歧 2 · 是否给 N / K 是否「部分未满足」—— **接受 ✅,但拒绝「优化」这个词**

对方的结构性拆分是对的:**监测周期**(已定形)与**重校准间隔**(未定形)是两件事,我 P3R1 把它们混在一起,
才得出「K 部分未满足」。按拆分后:K 的「有定期校准机制」在**机制层已满足** —— 每个被消费的批次必测必落库,
是真实可执行的节拍;而本仓**没有自然时钟**(warn registry README 局限 3 已实证),
**以批次为索引是唯一诚实的周期**。⇒ **§4 自检该条改判 ✅。**

**但我不接受把剩下那块叫「v0.2 优化」。** 优化是让已有能力更好;这里缺的是**一项能力**:
仅有「身份/口径变化即新基线」触发器时,**身份稳定而缓慢漂移的场景结构上无人覆盖** ——
NIST 的控制图路径存在的理由恰恰就是它。⇒ 应记为**具名敞口**,不是优化项。

🔴 **而这引出本轮我最想写进终稿的一条**:
**本 verdict 自己不得犯它所诊断的病。** 我们四题共同的病灶是「机制存在未绑定到谁在何时做什么」;
若把「重校准间隔待 control history 足量后定」写成一条**没有消费点**的 v0.2 note,
它就是同一形态的**新增第五处**,而且是我们亲手造的。
⇒ 该 note **必须带 `due_gate`**;且依本轮实测,本 fork **唯一已接线**的消费 gate 是
`forge:009-pM3prime:phase0`(它今天真的开火了),`xenodev:*` 三个 gate **均未接线**。

### 分歧 3 · 版本化回退是否违反 C6 —— **让步,采对方措辞**

路线 (b) 双方一致。**措辞我改错了**:我写「旧 gate 结论**作废**」,对方指出这可能暗示追改历史。
终稿统一为:**历史不可变;授权被后续 `caliber_version` supersede** ——
旧阈值、旧证据、当时的裁决**永久保留可查**,新版本只撤销旧版的**未来消费权**。
这样 (b) 确实不违反 C6「预注册不可回改」,也不落入 forge v2 的「移动球门」判据。

### 分歧 4 · per-market 是否列为 v4 硬输出 —— **让步,采排除**

同意排除,理由(判据膨胀 · v3 §underweights 4 的教训)成立。
⚠ 一处小更正:对方在分歧 4 引我的原句「处置重点应从『继续找』转向『动作绑定』」——
那句是我对**议题⑤**说的,不是对 per-market 说的。不影响裁定,记此以免进语料后被当成我的 per-market 立场。
**但「显式未满足说明」必须落到具体载体**:`PRD.md` §6 科学重判触发条件 1 处加注
「本条**未**因 T015 满足 —— 该读数为全局,非 per-market」。只写进 stage doc 等于没写。

---

## §2 联合 verdict(单一)

**四条到期义务是同一个病灶的四个断面:机制存在,但没有绑定「谁在何时做什么」。终裁如下。**

**① M1=pass 欠一次具名裁决**(广读)。依据**只**是本地三载体 + 已接线消费点 + `OB-16` 本身,
不得援引外部规范权威。**本次裁决内容**:接受 M1 为**固定批可比性**证据 ——
NIST「statistical control can only guarantee comparability among measurements」;
**不解锁扩样与 E2,不外推,不作效度 gate 代理**。rationale **必须同时载明**两项风险输入:
(i) 一致率上升无法区分噪声去除与**歧义抹除**(「filtering non-consensus samples results in over-optimistic results」);
(ii) 6 个跑的 `census_verdict` **全部** `below_threshold_advisory`。

**②** 现状**跨批次比较不可信**。`OB-15` 的兑现判据 = **四前提**(预注册观察/停止边界 · 逐 attempt exposure 可计 ·
已观察失败的结果及精确时间/区间留存且删失可识别 · 失败批次内容身份可比);
**四者证不出则回退到写穿透或等价耐久回执**。不写死实现。

**③** **监测周期已定形**:每个被消费的批次必测必落库;身份/口径变化(模型 · `system_fingerprint` ·
语料批次 · `caliber_version`)**立即**启动新基线;**XenoDev 产证、IDS operator-chair 接受基线与升版**。
**统计型重校准间隔未定形**,记为具名敞口(非优化项),须带消费点。

**④** C4 convert 判据 = **过程证据 + 结果证据 + 具名批准 + 版本化回退,四者合取**,不给数字。
版本化回退语义 = **历史不可变、授权被后续 `caliber_version` supersede**。

**⑤** 停止增列例证。RFC 5848/9162 表明「机制有、动作无」非本仓独有,处置落在**动作绑定**。

**0 unresolved。**

---

## §3 残余分歧降级为 v0.2 note

1. **统计型重校准间隔的 N** —— 待 control history 达足量点数后定。
   🔴 **必须带 `due_gate`,否则本 note 自身即第五处实例**(见 §1 分歧 2)。
   建议 `due_gate = forge:009-pM3prime:phase0`(本 fork 唯一已接线且今日实证会开火的 gate)。
2. **per-market 跨次一致性分解** —— v0.2 候选,非 v4 硬产出;但**当前未满足须落 PRD §6 条件 1 注记**。
3. **`OB-15` 四前提的具体实装路线** —— 交 build 侧选,受 fallback 分支约束。
4. **`xenodev:*` 三 gate 未接线** —— 本 verdict 产出的义务若指向它们,一律 `consumer_wired: false` 且 `exposure` 必填。

---

## §4 W 形态产出的初步草稿建议

**verdict-only** —— 用 §2 全文,四题各一段,每段末尾给「回写落点」(文件 + 节)。

**decision-list(四列 + obligation path 列)** —— 建议行:
| 对象 | 判 | obligation path |
|---|---|---|
| 「三态必须回 forge 裁决」条款 | **调整**(广读入正文 + **同步改结果矩阵表 pass 行**) | `forge:...:v4:phase4 → forge:009-pM3prime:phase0` |
| `OB-15` 兑现判据 | **新增**(四前提 + fallback) | `→ xenodev:handoff-intake`(**未接线** · exposure 必填) |
| 校准监测周期 + 责任分离 | **新增** | `→ forge:009-pM3prime:phase0` |
| 重校准间隔 N | **登记议题**(v0.2 · 具名敞口) | `→ forge:009-pM3prime:phase0` |
| C4 convert 四合取判据 | **调整** | `→ forge:006:phase0`(C4 warn 已 defer 至该 gate) |
| SLA 提取稳定性行「判据」列 | **调整**(补「跨次读数存在性」判据 —— 目前四个「必须」里最重要的那个零判据) | `→ xenodev:handoff-intake`(**未接线**) |
| per-market 未满足注记 | **新增**(PRD §6 条件 1 加注) | `→ forge:009-pM3prime:phase0` |

**refactor-plan** —— 三组:
(A) **条款同步组**:v3 结果矩阵表 pass 行 + `OB-...-07` note + PRD §6 条件 1 注记(三处一起改,漏一处仍留歧义);
(B) **记账组**:`census.py` 的 attempt log 四前提落地面 + `SLA.md:136` 判据列补跨次读数存在性 SQL;
(C) **C4 三处同步 site**:IDS `PRD.md` §7 红线 3 + XenoDev `spec.md` C4 + `SLA.md` E1 行。

⚠ **给 synthesizer 的硬约束**:Step 6.5 登记义务时,凡消费点为 `xenodev:*` 者
**必须** `consumer_wired: false` + `exposure` 必填;凡本轮产出的 v0.2 note **必须**有 `due_gate`。
**这是本 verdict 自身不重蹈其诊断对象的唯一保证。**
