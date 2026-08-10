# Forge Stage · 006 · v9 · 「证据完整性家族四条缺口 —— 从『门没人调』到『义务从未存在』」

**Generated**: 2026-08-10T10:35:00Z
**Source**: forge run v9,X = 7 标的(1 权威快照[首选·自足] + 1 外部 repo backlog 原文[Grep 四段] + 1 决议日志[只读第 40/41/42 条] + 1 协议 SSOT[§6 B-4-IDS] + 1 实装现场[handback-review Step 2/4.2/4.3] + 1 v8 verdict 承接 + 1 仓宪法),Y = 工程纪律(主) + 架构设计 + 安全,Z = 对标 SOTA(tamper-evident 日志 · provenance attestation · CI 强制执行门 · stale approval 失效 · code review 收敛实证),W = verdict-only + decision-list + refactor-plan
**Convergence mode**: `strong-converge`
**Rounds completed**: P1(both)· P2(both)· P3R1(both)· P3R2(both)
**Searches run**: **40**(Codex 36 queries 覆盖 Z 全五向;Opus 4 次定向 `WebFetch` —— ⚠ **非检索**,见 §underweights-1)
**Moderator injections honored**: **1**(`moderator-notes.md` @ 2026-08-10T09:58Z · Hard constraint · binding on Both · **已被双方在正文承载**)
**Convergence outcome**: **converged** —— 六条分歧全部 finalize,**无 `unresolved`**;4 条 v0.2 note;`evidence_grade` 11 行逐行定案
**Synthesizer note**: 本文档由**主 session 直接撰写**(非隔离子代理),输入全部读自主 checkout 原文;该偏离如实记录于 §underweights-7

---

## How to read this

本轮**不重开 006 大方向**,只审**证据完整性家族**四条缺口(KG-B11 / XD-41 / XD-43 / XD-44)
+ 中途正式接手的 `SHARED-CONTRACT:993` post-P0 backlog。

**读法建议**:先读 §Verdict 一段;若你只想知道「跟上一轮比,新的是什么」,直接跳 §Evidence map 的
⭐ 三行 —— 本轮的三个真发现(**原诊断被推翻** / **`absent` 态自毁** / **治理链已失败 3 次**)都在那里。
Decision matrix 的第 5 列 `evidence_grade` 与第 6 列 `obligation path` 是本轮方法论增量,**别跳**。

---

## Verdict

**采一簇总评级 `new` 的 obligation control plane,加 XD-41 / XD-44 两条校准,正式接手
`SHARED-CONTRACT:993` post-P0 (b)(c)(d),零 cut。**

核心机制:**不可绕过的权威 gate 在事件发生时预建 `pending`**;`satisfied` 必须**绑定当前内容身份**;
`skipped` **仅由预置 policy 或 operator-chair 签**,producer 只能提出、不得自批;
**到 `due_gate` 仍为 `pending` 即 fail-closed 拒绝**。控制面**逐入口**覆盖 **build 链与 forge 治理链**
(`stage verdict → 授权登记 → hand-off / 下一 intake 清偿`),
但**明确不声称自动发现未枚举入口**。既有实装件(R-Q7 双写 lib、preflight 解析器)**保留为 refactor**。

两条校准:`needs-attention` **不再等价放行**;统一四轮上限改为**按风险/复杂度分档的有界 hard-stop**,
「finding 类别重复作收敛信号」**reject**(非 defer,**不留暗门**)。

🔴 **verdict 必须具名承载的一句**:原始诊断「四条全是 execution gap」**已被 P2 的 SOTA 推翻** ——
**design gap 与 execution gap 并存,且 design gap 是共同上游**。这是「为什么这次不能只改 SKILL 措辞」
的理由链,**删掉它,本轮就退化成 K 第 1 条禁止的第三条建议**。

⭐ **本 verdict 约束 forge 自身**:v9 漏掉了 v8 给它定的 intake 义务,这件事本身就证伪了 build-only 方案。

---

## Evidence map

| # | 证据 | 来源 | 强度 |
|---|---|---|---|
| ⭐1 | **「四条全是 execution gap」被推翻** —— in-toto 的 owner **先签必经步骤**、GitHub requirement **由 ruleset 预置**、SLSA subject digest **先绑内容再验后生证据**:成熟体系**全都在证据之外先定义 obligation** ⇒ 本仓不是「造了门没人调」,是**从未有 obligation 层这个设计** | P2-GPT §1 第 2/4 行(in-toto · required checks) | **本轮唯一一次真正的证伪**,且推翻的是 **Opus 自己 P1 的地基**(Opus P1 曾点名请求证伪而非补强) |
| ⭐2 | **`absent` 态自毁** —— 「若 `absent` 是一个要被写下的状态,**它自己就会缺席**」⇒ 等于把「缺席即豁免」原样搬进新机制;改为 `pending` 由 gate **预建**,缺席才真正不可能(无人需要写任何东西即可触发拒绝) | P3R1-GPT §1 / §3 分歧 6 | 对 Opus 草案**最重要的一次修正**,Opus 全额让步 |
| ⭐3 | **治理链已独立失败 3 次** —— ① `SHARED-CONTRACT:993` post-P0 backlog 明写「需 forge 决议」挂 **65 天**、v5–v8 一场没接;② 🔴 `SHARED-CONTRACT:1239`(§8.5 · forge v8 · 07-13)已把「preflight 登记表 + `evaluate_gate` 接下游」**作授权条目下发**,**28 天仍 ⏳** —— **这就是 v9 在审的 XD-43 本身**;③ `hook-allowlist-governance.md:82` 明写「下次 `/expert-forge 006` 起时把白名单全表过一遍」,**v9 就是那个「下次」,没过** | ① P1-Opus §1 附加发现;②③ moderator 注入(IDS 侧独立清点) | 实例 ② **决定性**:决议、下发、留痕**全做了**仍蒸发,因**下游无任何 gate 要求清偿** ⇒ **不能归为「人没跟进」** |
| 4 | **四条的机制侧确实都已存在**:`codex-review/SKILL.md:279-317` 双写范式 + `:315` 把「只写 singleton」明文列 ❌ anti-pattern + `write_review_log_immutable` lib 真实存在;preflight 解析器已实装并收紧为 fail-closed;替代路径每批都跑了红绿日志/mutation/双子代理 | P1-Opus §1(实装现场带行号) | 双方 P1 **独立**到达 |
| 5 | **实测三态**:v0.6 双写齐全 / **v0.7 + v0.8 两者皆无** ⇒ 不是「调了错写法」,是**根本没调**;`REVIEW-LOG.md` 至今对下游显示 `approve / findings_count 0`(2026-07-26),现实是 `needs-attention` 带 2 条未复核 high | Codex P1 §0 独立真核(`git ls-files` + 目录 ls + frontmatter `ts`) | **Codex 侧独立复核属实**,非取 IDS 自述 |
| 6 | **XD-44 首次有实证**:19,177 reviews 的规模/新增行与 review changes 相关;另一研究 **70% 约 1–2 轮但精确轮次预测很差**;defect escape 与 coverage/参与度/专家度显著相关**但 100% coverage 仍有缺陷**;⚠ **未取到任何支持统一停轮阈值的研究** | P2-GPT §1 第 7/8 行(EMSE 2022 ×2 + EMSE 2016) | **单侧覆盖**(Opus 侧 `WebSearch` 故障),无跨模型交叉 —— 见 §underweights-1 |
| 7 | **三条 SOTA 限缩(反向证据)**:① **OPA 只是 decision point**,enforcement 接线必须应用自己做 ⇒「采 policy-as-code 即解决」被反证;② **SLSA 能证明「谁对哪份内容作何声明」但不能证明 review 足够**,且 producer 与证据**同信任域**;③ **WORM/Merkle 只保证已有记录不可改、不生成 obligation** | P2-GPT §1 第 5/3/1 行 · P2-Opus §1 第 5 行(SLSA 未规定缺席处置) | 双侧各自取到,**是本轮野心的边界条件** |
| 8 | **「缺席」的成熟解**:GitHub required check 必须取得 `successful` / `skipped` / `neutral` **状态**才放行,未上报保持 Pending 并阻断 ⇒ **「不适用」必须被主动申报,不能靠沉默**;Gerrit `copyCondition` 说明全量撤销会因 merge-base 漂移**误报** | P2-Opus §1 第 2/3 行 · P2-GPT §1 第 4/6 行 | **双侧独立取到同一先例**;直接给出 K 第 3 条要的「该带而未带 ≠ 未带就拒」 |

---

## Intake recap

### X · 审阅标的(7)
`_x-batch-snapshot.md`(权威快照·自足)· XenoDev worktree `dogfood-backlog.md`(Grep KG-B11/XD-41/XD-43/XD-44 四段)·
`discussion/001/handback/HANDBACK-LOG.md`(第 40/41/42 条)· `framework/SHARED-CONTRACT.md`(§6 B-4-IDS)·
`.claude/commands/handback-review.md`(Step 2 / 4.2 / 4.3)· `discussion/006/forge/v8/stage-forge-006-v8.md` · `CLAUDE.md`
**x_hash**: `7ad1bb97a7760addddb7cd371eca3b71`(全程冻结未改,**注入不改 X / 不改 K**)

### Y · 审阅视角
工程纪律(主)· 架构设计 · 安全

### Z · 参照系
对标 SOTA:tamper-evident/append-only 审计日志 · provenance attestation(SLSA/in-toto/Sigstore)·
CI 强制执行门(required checks / branch protection / OPA)· stale approval 失效 · code review 收敛实证。
**外部材料叠加:无**(双方 §2 均标 `n/a`,未把检索结果冒充 operator 材料)

### W · 产出形态
`verdict-only` + `decision-list` + `refactor-plan`(❌ **不产 `next-dev-plan`** —— operator 显式不要)

### K · 用户判准(六条 operator 关切 + 四条硬约束)
要 enforcement 不要第三条建议 · 先判故障态再定修法 · 要「该带而未带」判据不要「未带就拒」·
不过度工程能合就合 · 尊重证据权重差异 · **显式自检本轮结论本身是否落进「缺席即豁免」**。
硬约束:框架级只走 forge · mirror 三层同步(**`SHARED-CONTRACT` SSOT 在 IDS**)· 改 §6 须 bump
`contract_version` + Changelog · **不碰批次外 KG-B8/B9/B10/B12 + XD-42**

### 收敛模式
`strong-converge` —— 必须 finalize 单一 verdict。**理由**(operator 原文):本批需要的是可执行 enforcement,
两条并存路径会让「缺席即豁免」又一次悬置。

---

## Decision matrix(11 行 × 6 列)

> 第 5 列 `evidence_grade` 承 forge 001 v6 立的条款(**记录回声室,不消除它**);
> 第 6 列 `obligation path` 为本轮新增 —— **每条裁决必须能指出「谁产生这条义务、谁消费它」,
> 指不出的条不成立**。⚠ 该列是**约束性证明字段,不是 gate 本身**(Codex P3R2 §1 修正)。

| # | 类别 | 最终裁决 | 判据 / 证据源 | `evidence_grade` | `obligation path`(产生 → 消费) |
|---|---|---|---|---|---|
| 1 | **新增** | **核心 obligation**:权威 gate 预建、内容绑定关闭、到期拒绝 | 双方 P1 **独立**到达「证据不能决定自身是否应存在」;in-toto layout `THRESHOLD` + `expected_materials` MATCH 提供同构先例(证据 1/8) | **`independent`** | lifecycle gate → row-specific `due_gate` |
| 2 | **新增** | **`pending / satisfied / skipped` 状态机 + policy / operator-chair 签署权**(producer 只能提出) | Codex P3R1 分歧 6:`absent` 若是「要被写下的状态」则自己会缺席(证据 2);签署权分层堵 Codex P1 §3-2 的「连类型一起省略」攻击面 | **`post-hoc-accepted`** ⚠ Opus 全额让步的产物 | canonical gate → 同一 gate 的终态校验 |
| 3 | **新增** | **XD-41 fallback 补审债并入同簇** —— 从 fallback merge 时即创建 `pending` | 硬证据:替代路径六批放行,codex 恢复后 4 轮抓 21 条(11 high);`needs-attention` 事实等价放行 | **`post-hoc-accepted`** ⚠ Opus P1 原判 refactor,后让步 | fallback merge gate → codex 恢复后的累积补审 gate |
| 4 | **新增** | ⭐ **forge 治理链纳入同一控制面**(`stage verdict → 授权登记 → hand-off / 下一 intake 清偿`) | moderator 注入的三实例(证据 3);实例 ② 证明完整决议+下发仍蒸发 | **`post-hoc-accepted`** ⚠ **moderator 注入后的扩面,非双侧独立到达** | Phase 4 定稿 → XenoDev hand-off intake / 下一 Phase 0 的 `due_gate` |
| 5 | **新增** | **接手 `SHARED-CONTRACT:993` post-P0 (b)(c)(d)** | 挂 65 天、明写「需 forge 决议」、(b)(c)(d) 与本批高度重叠;Codex 独立判其为**consumer 侧根** | **`independent`** | XenoDev ship gate → IDS handback-review consumer gate |
| 6 | **调整** | **`needs-attention` 不再等价放行** | RFC 7282 addressed ≠ merely noted(v6 已立条款);XD-41 真跑数据 | **`independent`** | fallback review gate → merge / ship gate |
| 7 | **调整** | **四轮上限 → 按风险/复杂度分档的有界 hard-stop** | EMSE 实证:规模/复杂度 ↔ 轮次相关;70% 约 1–2 轮但预测很差(证据 6) | **`independent`** | codex-review loop → operator hard-stop / ship gate |
| 8 | **调整** | **单 task 含多个可独立评审的跨模块契约面 ⇒ 触发拆分复核**(**不称唯一根因**,展开归 task-decomposer) | Opus P1 §3-3 reframe + Codex「支持但证据不足以判为唯一根因」;⚠ **Opus 已撤回原 `≥N` 阈值** —— 写 `N` 等于自造无实证的数字,与 #10 被 reject 的理由同构 | **`post-hoc-accepted`** | task-decomposer → task / spec review gate |
| 9 | **保留** | **R-Q7 双写 lib + preflight 解析器**作为 refactor 实装件,**不重写** | 实装现场带行号核实(证据 4):文本、判例、工具三样齐全 | **`post-hoc-accepted`** | 新 canonical entry gate → ship gate |
| 10 | **删除** | **「finding 类别重复作收敛信号」reject** —— 非 defer,**不留暗门**;未来新实证只能以**新提案**重开 | 未取到支持统一停轮阈值的研究;非结构化 finding 无可靠可执法的等价判定(证据 6) | **`SOTA-corrected`** | `N/A(rejected)` |
| 11 | **删除** | **「四条全是 execution gap」的原诊断** | 成熟体系全都在证据之外先定义 obligation(证据 1) | **`SOTA-corrected`** | `N/A(diagnosis replaced)` |

**`evidence_grade` 最终分布**:`independent` ×4(#1/#5/#6/#7)· `SOTA-corrected` ×2(#10/#11)·
`post-hoc-accepted` ×5(#2/#3/#4/#8/#9)。
⇒ **11 行里只有 4 行够得上 `independent`**。⚠ Codex P3R2 §4 明写:**刻意不把含它 P3R1 修正的
状态机整行标高**,以免复现 forge 001 v6 第 8 行「发现独立、裁决却是单方方案」仍被高估的错误。

---

## Refactor plan(3 模块)

### M1 · obligation 存储 / 状态机 / 内容身份
- append-only 存储;`satisfied` 必须携带**当前内容身份**(不是「某文件未变」的 SHA —— 证据 7②:
  SHA 只证文件未变,不证本次跑过且审的是当前内容)
- 状态机 `pending → satisfied | skipped`;**`pending` 只能由 gate 预建**,任何角色不得直接写 `absent`
- `due_gate` 为**每条义务**的属性 ⇒ 未到期义务**不阻断无关 intake**;已到 `due_gate` 而无权威终态**即阻断**
  (Codex P3R2 §1 修正:避免任意未清偿项冻结所有 forge)

### M2 · canonical gate 注册与逐入口接线
- build 侧已知入口 + **forge 侧两处治理入口**:**Phase 4 定稿**(产生)/ **Phase 0 intake**(消费)
- ⚠ **逐入口接线,不得声称自动覆盖**(证据 7①:OPA 明确只是 decision point)
- 每个 gate 注册时须登记「**覆盖 / 不覆盖哪些事件 + `due_gate`**」⇒ 对应 v0.2 note 2

### M3 · policy 与 operator-chair 签署 / consumer 终态验证
- 确定性豁免走**预置 policy 签**;例外走 **operator-chair 签**;**producer 只能提出,不得自批**
- consumer 侧独立验证终态(承 Rekor inclusion proof 的形态:**第三方可独立复证**,不靠 producer 自述)

### ⚠ mirror 同步顺序(硬约束,不可颠倒)
```
IDS 侧改(SSOT)  →  cp 回 bootstrap-kit mirror  →  更新 MANIFEST SHA
```
`SHARED-CONTRACT.md` 的 **SSOT 在 IDS,不在 MANIFEST**(与 bootstrap-kit mirror 反向)。
改 **§6 B-4-IDS 必须 bump `contract_version` + 写 Changelog entry**(属 spine · risk=high)。

---

## v0.2 notes(4 条 · 三字段齐全)

- **note 1 · v0.7/v0.8 的精确漏调入口仍未定位(K 第 2 条未达成)**
  **主体 + 时点**:**M2 canonical gate 接线的 XenoDev 实装 owner**,在**首个接线 task 进入 pre-merge
  `/task-review` 前**提交 v0.7/v0.8 调用路径复盘,由 **operator-chair** 验收。
  **此前风险敞口**:若真因是「SKILL 未被 load」或「amendment 路径未枚举」,则 **obligation 的创建事件
  会选错**,整类事件继续静默缺席。⚠ **不得把「未调用」冒充为已定位根因**(双方 P1/R1/R2 均确认)。

- **note 2 · obligation 枚举完备性敞口**
  **主体 + 时点**:每个 build gate 由 **XenoDev gate owner**、每个 forge gate 由 **IDS forge-protocol owner**,
  在**该 gate 的 pre-merge review 前**登记「覆盖/不覆盖事件 + `due_gate`」。
  **此前风险敞口**:**清单外入口产生零 obligation**,原病在控制面之外原样存活;
  **不得宣称一条机制自动覆盖所有入口**。

- **note 3 · ⭐ v9 自身未履行的白名单全表回审(控制面的第一条实测存量)**
  **主体 + 时点**:**operator**,在**下一次 `/expert-forge 006` 的 Phase 0 intake** 明确「过表」或**签署 skip**;
  可观察 = 该次 `forge-config` 的 X 或 intake 记录里出现白名单条目。
  **此前风险敞口**:hook 白名单**至今未经全表回审**;
  🔴 **若该存量在下一次 intake 又蒸发,即证明本 verdict 的治理链覆盖是纸面的,直接触发 v10。**

- **note 4 · `skipped` 的签署格式未定形**
  **主体 + 时点**:**M1 状态机 owner** 在**首个实现 task 的 pre-merge `/task-review`** 提交 policy 签署格式,
  由 **operator-chair** 验收例外格式。
  **此前风险敞口**:无格式时 **`skipped` 会退化为 producer 自报** —— Codex P1 §3-2 的
  「连包类型一起省略」攻击面原样返回,机制等于没做。

---

## What this menu underweights(强制自批判)

**underweight-1 · 🔴 Opus 侧 Z 执行故障,第二次复发 ⇒ 本轮 SOTA 覆盖事实上部分单侧**
Opus 侧 `WebSearch` 三次同错 400(`output_config.effort 'xhigh' is not supported when thinking is
disabled`),**与 forge 001 v6 完全相同的后端故障**。Z 退化为对已知权威源的**定向 `WebFetch`(不是检索)**。
⇒ Opus 侧**未产出任何「未检索到 ⇒ 无先例」型结论**(其 P2 §0 已自行封杀);
但 **Z 第 5 条方向(code review 轮次实证)Opus 侧完全未取到**,
**决策矩阵 #7 与 #10 的实证基础 100% 来自 Codex 单侧检索,没有跨模型交叉验证**。
⇒ 若该三篇 EMSE 研究被误读或不适用,#7/#10 **没有第二道防线**。

**underweight-2 · K 第 2 条(先判故障态再定修法)本轮未达成**
漏调入口至今未定位,**双方 P1 §3 第 1 条都是它,P2 的 SOTA 不可能替我们定位**。
本轮是**在承认该空白的前提下**选择了「用 gate 预建 obligation 绕过根因定位」的路线 ——
这是**合理的工程折中,不是问题已解决**。已入 note 1,但必须在此重复:
**verdict 的有效性依赖于「创建事件选对了」,而这一点未被验证。**

**underweight-3 · moderator 注入产生了一次记录在案的不对称**
注入发生在 Opus P3R1 **写完之后**、Codex P3R1 **跑之前** ⇒ **Codex 在 P3R1 就回应,Opus 推迟到 P3R2**。
该不对称**对 Codex 有利**(它拿到更多输入),已如实写入 `moderator-notes.md` 与本节。
⇒ 矩阵 #4(治理链扩面)标 `post-hoc-accepted` **正是因为它是注入后的产物**,不是双侧独立到达。

**underweight-4 · 11 行里只有 4 行 `independent`,且回声室在本轮的形态与 v6 不同**
v6 的教训是「回声室在 P1 被隔离后于 P2 以『事后同意』形式回归」。本轮**不同**:
双方 P1 **确实独立**到达同一核心诊断(Codex 未读 Opus P1),**但那不构成验证** ——
Opus P1 已预警「整齐本身是危险信号」并请求证伪,**真正的证伪直到 P2 才发生,且推翻的是 Opus 自己的地基**。
⇒ **本轮最健康的信号,同时反证 P1 阶段的「双侧同意」当时确实不该被当作验证。**
`post-hoc-accepted` ×5 里,#2/#4 是 Opus 让步或注入产物,**下游不得读成双侧独立复现**。

**underweight-5 · 本轮显式不裁的两批,不是遗漏**
① **批次外 5 条**:KG-B8 / KG-B9 / KG-B10 / KG-B12 / XD-42(operator 在 intake 时显式排除);
② **IDS 现存 8 条 ⏳ 授权条目**(`SHARED-CONTRACT :634/:1170/:1173/:1175/:1239/:1242` +
`hook-allowlist-governance :79/:82`)—— moderator note 只把它们作为**证据**引用,
**明令不得借注入扩裁**。⚠ 但这意味着:**除 note 3 的白名单外,其余 7 条 ⏳ 至今仍无消费点**,
本 verdict 落地前它们**继续暴露在同一失败模式下**。

**underweight-6 · 安全视角的两处未展开**
① `satisfied` 的「内容身份」具体取什么(文件 SHA?diff?spec 版本?)**本轮未裁** ——
证据 7② 已证 SHA 不足,但替代物未定,留给 M1;
② **控制面自身的可用性即阻断面**:gate 预建 `pending` 后若 ledger 不可用,
**fail-closed 会阻断一切** —— 该 tradeoff 双方均未讨论,是 `strong-converge` 下被压掉的一面。

**underweight-7 · Phase 4 由主 session 撰写,非隔离子代理**
按会话约束,本 stage 文档由主 session 直接写成,**未起 `forge-synthesizer` 子代理**。
⇒ **少了一层上下文隔离**:撰写者同时是 Opus 侧 reviewer,**对自己的让步与措辞有天然偏袒风险**。
缓解措施:矩阵第 5 列逐行标注、`post-hoc-accepted` ×5 中 **#2/#4 均为撰写者本人让步/注入产物且已标低**;
但**该偏袒风险无法由撰写者自证消除**,如实记于此。

**underweight-8 · `strong-converge` 的副作用**
双方都同意、但**最可能被真跑打掉**的两条:① **`due_gate` 的可判定性** —— 「什么时候算到期」
在本仓的异步节奏里(operator 单人、跨仓、批次间隔以周计)**没有自然时钟**;
② **逐入口接线的真实规模** —— OPA 反证说成本不可省,但**没有人估过本仓有多少入口**。
两者的 fallback 未预置,是本轮相对 v6 的一处退步。

---

## Forge versioning 提示(v10 触发判据)

**任一命中即起 v10**:
1. 🔴 **note 3 的白名单存量在下一次 `/expert-forge 006` Phase 0 intake 又蒸发** ——
   即证治理链覆盖是纸面的(**本轮最强判据**)。
2. **note 1 复盘发现真因不是「未调用」** ⇒ obligation 的创建事件选错,矩阵 #1/#2 需重裁。
3. **note 2 的枚举清单上线后,发现清单外入口仍在产生放行** ⇒ 「逐入口」策略不足。
4. **`due_gate` 无法给出可判定的到期语义**(underweight-8①)⇒ 整个 fail-closed 语义悬空。
5. **v9 verdict 落地后 XD-41 形态复发**(替代路径再次事实放行)。

**已攒批待审(v10 候选)**:`discussion/006/FORGE-006-v10-PENDING.md` 现有 **KG-B13**(`cdx-run` 静默重放覆盖)·
**KG-B14**(`reuse-session` 被静默降级为冷 session)· **KG-B15**(worktree 规约 warn 已复发 2 次,
hook block 升级判据达成);**新增候选**:`WebSearch` 400 第二次复发(underweight-1 · 直接降级 forge 的 Z 证据质量)。
⚠ **起 v10 前先读本轮 verdict** —— KG-B13/B14 与本轮的「声明层 vs 执行层无校验」高度同题,
可能是本条款的**实例**而非独立议题。

**不该跑 v10 的情形**:本轮 11 项**尚未行动过**时只想「再听一遍」⇒ 应该用 `/forge-inject`,不是起新 v。

---

## Decision menu(for human)

### [A] 接受 verdict,全量落地(推荐)

```
执行顺序(★ = 不可颠倒):

★1. 先定 M1 的「内容身份」取什么(underweight-6①)
    —— 它是 satisfied 的承重字段;没定就接线,等于用 SHA 假装绑定(证据 7② 已否)。

★2. M2 先接 forge 侧两个治理入口(Phase 4 产生 / Phase 0 消费)
    —— 理由:这两个在 IDS 内、成本最低,且 note 3 的白名单存量正好是第一条待清偿义务,
       可作为控制面的首个真跑样本。build 侧入口随后接。

 3. M3 签署格式(note 4)随 M1 首个实现 task 一并提交 /task-review。

 4. XenoDev 侧按授权条目下发(不当场改),mirror 件走 IDS SSOT → cp → MANIFEST SHA。
```

### [B] 只落 forge 治理链一段(止血核心 · 延续 v7 D1 / v8 先例)
只做 M2 的两个 forge 入口 + note 3 白名单清偿,**build 侧全部延后**。
**代价**:XD-41/XD-43 的 build 侧敞口继续开着;**收益**:一周内可验证「控制面是否真的挡得住」,
且用的是**本轮自己欠的那条债**作样本 —— 失败会立刻暴露,不会拖到下个季度。

### [C] 局部接受
逐行挑 11 行矩阵。⚠ **#1/#2 不可拆**(状态机是核心 obligation 的承重件);
**#11(删除原诊断)不可不选** —— 不删它,落地会自动退回「改 SKILL 措辞」。

### [P] Park
保留全部产物,不落地。**代价**:三条治理链实例继续累积,下一个 hand-back 极可能是第 4 次。

### [Z] Abandon
放弃本批。**需写 lesson 文档**说明为什么「机制存在但无消费点」这一族不值得治理。

---

## Forge log

- **v9: 2026-08-10** — verdict: "**采一簇总评级 `new` 的 obligation control plane** —— 不可绕过的权威 gate
  在事件发生时**预建 `pending`**、`satisfied` **绑当前内容身份**、`skipped` **仅由预置 policy 或
  operator-chair 签**(producer 只能提出)、**到 `due_gate` 仍 `pending` 即 fail-closed**;
  控制面**逐入口**覆盖 **build 链与 forge 治理链**,**不声称自动发现未枚举入口**;
  实装件(R-Q7 双写 lib / preflight 解析器)**保留为 refactor**;`needs-attention` **不再等价放行**;
  四轮上限改**风险/复杂度分档的有界 hard-stop**;「finding 类别重复作收敛信号」**reject 不留暗门**;
  正式接手 `SHARED-CONTRACT:993` post-P0 (b)(c)(d);**本 verdict 约束 forge 自身**。
  🔴 **原诊断『四条全是 execution gap』被 P2 SOTA 推翻 —— design gap 与 execution gap 并存,
  design gap 是共同上游**(唯一一次真证伪,推翻的是 Opus 自己的地基,且是 Opus P1 主动请求的)。
  ⭐ **方法论产出**:decision-list 在 v6 的 `evidence_grade` 之外**新增第 6 列 `obligation path`
  (产生 gate → 消费 gate)—— 指不出路径的裁决不成立**;`evidence_grade` 11 行逐行定案
  (`independent` ×4 / `SOTA-corrected` ×2 / `post-hoc-accepted` ×5)。
  ⚠ 本轮 **Opus 侧 `WebSearch` 后端故障第二次复发** ⇒ #7/#10 的实证 100% 单侧;
  **K 第 2 条(先判故障态)未达成**;**moderator 注入造成一次记录在案的不对称**;
  **Phase 4 由主 session 撰写非隔离子代理**。
  v10 判据:note 3 白名单存量再次蒸发 / note 1 复盘推翻「未调用」/ 清单外入口仍在放行 /
  `due_gate` 无可判定到期语义 / XD-41 形态复发。"
- **v8: 2026-07-13** — 七项 dogfood 缺口 + worktree 隔离诉求,四簇裁决(gate 执行语义 / 分支拓扑 /
  LlmClient v2 / 证据 hook 治理),incremental optimize 零 cut。
- **v7: 2026-07-06** — review gate 状态机(不 cut codex)+ fork-id 进 SHARED-CONTRACT §7 作 SSOT。
