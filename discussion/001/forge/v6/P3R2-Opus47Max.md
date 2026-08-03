# P3R2 · Opus 4.7 Max · forge 001 v6 · Finalize(strong-converge)

> `convergence_mode = strong-converge` · 本轮零新检索。

## §1 我对每条分歧的最终立场 + 让步

**D-1 · direction 去重键 → 已收敛(对方同意我的双向处置)**
对方 P3R1 明确同意 `direction` 进分区/比较类、**退出去重计数**,并把去重身份改为
**stable claim identity**。⇒ 收敛。**残余**只剩「stable claim identity 谁定义、何时冻结」,
降 v0.2 note(见 §3)。

**D-2 · T040 起跑幅度 → 已收敛(对方确认我的判断)**
对方确认 §0.1 已把 O2 PASS 向定成 warn ⇒ **隔离条件由 spec 给出,不需另证**;
立即局部起跑,5 个非 O2 文件建 block 测,O2 面只建 warn/baseline。

**D-3 · 认识论强度分级 → 我让步,采对方的对称版本**
我原本只把**我的四条**标为「事后同意」。对方指出**这条必须对双方适用**,并具体点名:
我接受的 **v5 探索出口 / CVE 二态 / chair 映射**「也不是 P1 独立复现」,应归
「P2 外部材料修正后收敛」。**这是对的,我原来的提法是单向的、对我自己有利。**
⇒ 我**完全采纳**对方提出的三级标注:`independent` / `SOTA-corrected` / `post-hoc-accepted`,
逐行打在最终 decision-list 上。**这条从我提的一条分歧,变成了本轮的一件产出。**

**D-4 · 消费点 task 边界 → 已收敛(采对方的合一方案)**
三态接口 owner 与消费点 fail-closed **必须是同一个 task** —— 对方的理由我接受且认为决定性:
**分开则「接口只是标签、消费点无输入」**。边界采对方版本。

## §2 联合 verdict(单一)

**池化机制保留,但其 block-PASS 出口现在关闭,降为探索/warn 出口** —— v5 的错不在池化本身,
而在**把一个 post-hoc 的探索性机制的出口写成了可放行 PASS**(Cochrane/BMJ:标明的 post-hoc 探索
正当,但至多产假设、不指导实践)。**PASS 出口重开的前置是**:池键改为
`decision_epoch + rubric + comparability_class` 且 **在 epoch 开启时冻结为不可变**;
`direction` **进比较类、退出去重计数**;去重身份改为 **stable claim identity**。

**追溯采二态而非单态**(CVE 先例):**已证无效 → `rejected-like`,消费点机器可拒**;
**存疑 → `disputed-like`,记录保留但不得当 clean PASS 消费**。**关键实测事实**:仓内核查确认
**至今零真实 O2/P2 PASS 被旧池消费,迁移表为零项** ⇒ **现在立追溯规则的成本最低**,
但**零受影响必须落成具名核查记录,不得靠沉默推断**。

**`needs-attention` 不是 veto**(RFC 7282:issue 须被 addressed,不必被 accommodated),
**但 override 必须由 operator-chair 作出并逐条写明 reviewer concern 如何被 addressed**;
**chair = operator,`/handback-review` 是闸点与留痕、不是 chair 本身,spec-writer 不得自任**;
**无 chair 记录不得声称 clean PASS**。

**T040 立即局部起跑**(5 个非 O2 文件建 block,O2 面 warn/baseline)。
**三态接口 owner 与消费点 fail-closed 合为一个具名新 task,不塞 T041。**

## §3 残余分歧 → v0.2 note

> ⚠ 按 v6 forge-config 硬约束:每条须写明**回头看的触发时点**与**在此之前的风险敞口**;
> **禁止**「首次实施时复核」这类无主体无时点措辞(v5 note 1 正是这样写的,那就是本轮的口子)。

**note-1 · 「≥3」阈值本身未裁**
- **为什么未裁**:Cochrane「研究数很少的分组探索,无论 timing 价值都存疑」直接打在数字上,
  但本轮 **Y 未含产品价值视角**(operator 明确不选),双方均无资格判「1 条判断对 operator 有无决策价值」。
- **触发时点(具名)**:**首个 epoch 关闭且池首次达 ≥3 并进入抽样**的那一刻,由 **operator** 就地回答
  「这 3 条合起来是否真的支撑了一个我敢用的判断」。若答否 → 阈值问题升级为独立议题(需补产品价值视角)。
- **在此之前的风险敞口**:即使池键修好,仍可能产出**结构合规但对决策无用的 PASS**;
  该敞口**不因分区键修复而消失**,两者正交。

**note-2 · stable claim identity 谁定义、何时冻结**
- **触发时点(具名)**:**T021 落地 claim 规范化算法**时(spec v0.7 已把它列为 PASS 向转正条件②)。
- **在此之前的风险敞口**:PASS 向**持续 warn**;spec 已自陈的攻击面(**同义改写 / 仅换锚 /
  跨 epoch 重复**)全程开着。⇒ **note-2 未闭合前,note-1 的触发时点不可能到达**(池达不到可信的 3)。

## §4 W 形态产出草稿建议(W = decision-list only)

建议 synthesizer 出 **8 行四列矩阵**,每行按对方 P3R1 提议**加第 5 列 `evidence_grade`**:

| # | A(裁决) | fallback 三要素齐 | evidence_grade |
|---|---|---|---|
| 1 | 池键加 `comparability_class` + epoch 开启冻结 | ✔ | `independent`(双方 P1 各自到达 · 源出 codex round-3 原文) |
| 2 | `direction` 退出去重计数、去重改 stable claim identity | ✔ | **`post-hoc-accepted`**(Opus 单方 → GPT 事后同意) |
| 3 | block-PASS 出口关闭,池化降探索/warn | ✔ | **`SOTA-corrected`**(Cochrane/BMJ · GPT 修正 Opus 原判) |
| 4 | 追溯二态 `rejected-like` / `disputed-like` | ✔ | **`SOTA-corrected`**(CVE · GPT 提出,Opus 事后接受) |
| 5 | 零受影响**核查记录**(不靠沉默推断) | ✔ | **`independent`**(双方 P1 各自提出 **+ GPT 仓内实查证实**)⭐ 本轮最强 |
| 6 | chair 条款(chair=operator · override 须逐条 addressed · spec-writer 不得自任) | ✔ | **`SOTA-corrected`**(RFC 7282 推翻 Opus 原框架) |
| 7 | T040 立即局部起跑(5 block + O2 warn/baseline) | ✔ | `independent`(双方 P1 各自提出,幅度分歧已收敛) |
| 8 | 新 task:三态接口 owner + 消费点 fail-closed **合一** | ✔ | `independent`(GPT 实查「当前无合格消费点」+ 合一理由) |

**⚠ 请 synthesizer 务必保留进 underweights 的三条**:
1. **P1 独立性事故**:首次下发被 Opus 的结论污染,已重跑;**但 Opus P1 未重写** ⇒
   本轮是「**GPT 相对 Opus 独立**」,**非双向对称独立**。
2. **`WebSearch` 全程故障**(Opus 侧)⇒ Opus 的 Z 是定向 fetch 非检索,**本轮无任何负结果有效**;
   CVE 面靠 GPT 补上(GPT 侧 5 次检索可用)。
3. **8 行里只有 4 行是 `independent`** —— 其余 4 行是 SOTA 修正或事后同意。
   **回声室在 P1 被隔离后于 P2 以「事后同意」形式回归**,`evidence_grade` 这一列就是为记录它而设。

---

**篇幅**:约 1,320 CJK 字符(目标 700-1200),**具名超标声明**,不做有损压缩。
