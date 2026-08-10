# Forge v9 · 006 · P3R2 · Opus47Max · 联合收敛 R2(finalize)

**Timestamp**: 2026-08-10T10:20:00Z
**Visibility**: 我已读对方 P3R1。
**Convergence mode**: `strong-converge`
**Searches in this round**: NONE。

## Moderator injection response

(注入时我的 P3R1 已写完,故按 note 规定在此回应;对方已在其 P3R1 回应。)

1. **覆盖面 —— 覆盖,且这是本轮 verdict 的实质扩面。** 我原草案的 ledger 只覆盖 build 侧,
   **那是错的**:实例 2 证明「forge 已裁定 + 已下发授权条目」这条链**同样没有消费点**。
   最终形态:`stage verdict → 授权登记(obligation)→ 下一 intake / 落地清偿` 与 build 侧
   **共用同一控制面**。产生点 = forge Phase 4 定稿;消费点 = ①XenoDev hand-off intake、
   ②**下一次 `/expert-forge <id>` 的 Phase 0 intake**(未清偿的 obligation 未取得权威终态 ⇒ intake 不得完成)。
2. **归层 —— design gap 是共同上游,三例都不是「执行不力」。** 实例 2 是决定性的:
   决议、下发、留痕**全做了**,仍蒸发,因为**下游没有任何 gate 要求它清偿**。
   把它读成「人没跟进」会精确导出「再发一条提醒」——那正是 K 第 1 条禁止的第三条建议。
3. **自指处置 —— 支持,且这是本轮最便宜的一条。** v9 自己漏掉了 v8 给它定的 intake 义务
   (`hook-allowlist:82` 白名单全表回审),**这就证伪了 build-only ledger**:
   若控制面不含 forge 自身,本轮 verdict 会成为第 4 个实例。⇒ verdict 必须含一条约束 forge 自身的条款。
   ⚠ **诚实边界**:该义务本轮**仍未履行**(白名单全表没过)—— 本条不追认它已完成,
   它作为 obligation 的**第一条实测存量**进入 v0.2 note 3。

## 1 · 我对每条分歧的最终立场 + 让步

- **分歧 1 · KG-B11 / XD-43 评级** —— 对方:"同意,且把治理 gate 纳入范围,不能只接 build 三入口"。
  **我全额接受,含扩面。** 最终:**实装件保留(refactor)+ obligation 层新增(new)**,总评级 `new`。
  **让步**:范围由「build 三入口」扩到「build + forge 治理链」。
- **分歧 2 · XD-41 评级与归簇** —— 对方补:"fallback producer 无权签自己的 `skipped`"。
  **接受,这条比我原表述强。** 最终:`new`,并入簇①;补审债**从创建即为 `pending`**,不是事后标记。
  **让步**:我原写「ledger 里一条 `absent` 条目」,改为「创建即 `pending`」——见分歧 6。
- **分歧 3 · finding 类别重复信号** —— 双方均判 **`reject`**。对方补:"未来若有新实证须作为新提案重开,
  **不保留暗门**"。**接受该补充**(defer 会以「已考虑」形态留在文档里,正是本家族的病)。**无让步项。**
- **分歧 4 · 被推翻的地基是否具名** —— 双方一致:**要**,写成理由链而非悄悄换方案。**无让步项。**
- **分歧 5 · XD-44 粒度 reframe 落点** —— 对方:"反对写未经验证的固定 `N`"。
  **我让步,撤回 `≥N`。** 最终措辞:「**单 task 含多个可独立评审的跨模块契约面 ⇒ 触发拆分复核**」,
  **不称唯一根因**,展开归 task-decomposer 另案。理由:P2 实证只支持「规模/复杂度 ↔ 轮次相关」,
  **不支持任何具体阈值** —— 写 `N` 就是我自己造一个没有实证的数字,与 XD-44 建议 2 被 reject 的理由同构。
- **分歧 6(对方新增)· ledger 状态与递归终点** —— 对方:"`absent` 不是应写入的状态,
  而是到期 gate 对缺少权威终态的判定"。**我全额让步,并认为这是本轮对我草案最重要的一次修正。**
  我的 `absent` 态有一个致命缺陷:**若 `absent` 是一个「要被写下」的状态,它自己就会缺席** ——
  等于把「缺席即豁免」原样搬进新机制。改为 **`pending` 由权威 gate 在事件发生时预建**、
  到期未取得终态即 fail-closed,**缺席才真正不可能**(因为没人需要写任何东西来触发拒绝)。
  最终状态机:**`pending`(gate 预建 · 初态)/ `satisfied`(须绑当前内容身份)/ `skipped`(权威签署)**;
  签署权:**producer 只能「提出」skip,确定性豁免由预置 policy 签,例外由 operator-chair 签,
  producer 不得自批**。递归**终止于不可绕过的 canonical gate**,不是 ledger 自证。

## 2 · 联合 verdict(单一)

**采一簇评级 `new` 的 obligation control plane,加 XD-41 / XD-44 两条校准,正式接手
`SHARED-CONTRACT:993` post-P0 backlog,零 cut。** 核心:由**不可绕过的 canonical gate 在事件发生时
预建 `pending` obligation**,三态 `pending / satisfied / skipped`;`satisfied` 必须绑**当前内容身份**,
`skipped` 必须由**预置 policy 或 operator-chair 签**(producer 只能提出,不得自批),
**到期仍 `pending` 即 fail-closed 拒绝**。控制面**同时覆盖 build 链与 forge 治理链**
(`stage verdict → 授权登记 → 下一 intake / 落地清偿`),KG-B11 / XD-43 / XD-41 补审债 /
post-P0 (b)(c)(d) 全部并入本簇;既有实装件(R-Q7 双写 lib、preflight 解析器)**保留为 refactor**。
校准:`needs-attention` **不再等价放行**;统一四轮改为**按风险/复杂度分档的有界 hard-stop**,
「finding 类别重复作收敛信号」**reject**(非 defer,不留暗门)。
**verdict 必须具名写明:「四条全是 execution gap」这一原始诊断已被 SOTA 推翻,design gap 与
execution gap 并存且 design gap 是共同上游** —— 这是「为什么这次不能只改 SKILL 措辞」的理由链。
**本 verdict 约束 forge 自身**(v9 漏掉 v8 的 intake 义务即证 build-only 不成立)。
**无 `unresolved`。**

## 3 · 残余分歧降级为 v0.2 note

- **note 1 · v0.7/v0.8 的精确漏调入口仍未定位(K 第 2 条未达成)。**
  **触发时点(具名主体)**:**obligation control plane 的第一个 canonical gate 上线后,
  由该 gate 的 owner 在首次捕获一条到期 `pending` 时**回答「这条是哪个入口漏调的」——
  可观察 = 第一条 fail-closed 拒绝记录落盘。
  **在此之前的风险敞口**:我们**按「未调用」处置,但从未证明它是根因**;
  若真因是「SKILL 未被 load」或「amendment 路径压根不在清单里」,
  则 gate 预建 obligation 的**触发事件本身可能选错**,机制会漏掉整类事件。
  ⚠ **不得把「未调用」冒充为已定位根因**(对方 P1 原话,双方 R1/R2 均确认)。
- **note 2 · obligation 枚举完备性是已知敞口(谁保证清单没漏一步)。**
  **触发时点(具名主体)**:**每次新增一个 canonical gate 时,由该 gate 的 owner** 在
  `/task-review` 或 forge intake 上申报「本 gate 覆盖哪些事件、明确不覆盖哪些」;
  可观察 = gate 注册项里出现覆盖面声明。
  **在此之前的风险敞口**:**未被枚举的入口 = 静默零 obligation**,
  即本家族的原病在「清单之外」原样存活。OPA 反证已证**逐入口接线的成本不可省**,
  ⇒ **verdict 不得声称「一条机制自动覆盖所有入口」**。
- **note 3 · v9 自身未履行的 intake 义务(`hook-allowlist-governance.md:82` 白名单全表回审)。**
  **触发时点(具名主体)**:**下一次 `/expert-forge 006` 的 Phase 0 intake,由 operator** 在
  intake 清单上处置该条(过表 / 明确 skip 并签署);可观察 = 该次 forge-config 的 X 或
  intake 记录里出现白名单条目。
  **在此之前的风险敞口**:hook 白名单**至今未经全表回审**;且本条是**本轮控制面的第一条实测存量**
  —— 若它在下一次 intake 又蒸发,**即证本 verdict 的治理链覆盖是纸面的**,直接触发 v10。
- **note 4 · `skipped` 的 policy 签署模型与 operator-chair 例外格式未定形。**
  **触发时点(具名主体)**:**第一个 canonical gate 的实装者**在提交该 gate 的 spec /
  task 时给出签署格式,由 **operator-chair** 验收;可观察 = 该 task 的 review 请求。
  **在此之前的风险敞口**:若格式缺席,**`skipped` 会退化成 producer 自报** ——
  对方 P1 §3-2 的攻击面(「连类型一起省略」)原样返回,机制等于没做。

## 4 · W 形态产出的初步草稿建议

**W 含 `verdict-only`** → 关键句:
> 「**不是造门,是先立义务**:由不可绕过的 gate 预建 `pending`、内容绑定地关闭、权威签署地豁免、
> 到期即拒;**且这套控制面必须覆盖 forge 自己的决议,否则本 verdict 就是它自己的第 4 个实例。**」

**W 含 `decision-list`** → 建议矩阵**保留 v6 立的第 5 列 `evidence_grade`**(双方已在 R1 一致同意),
并**新增第 6 列「消费 gate」**(哪个不可绕过的 gate 消费这条,缺则本条不成立)。建议行:
- **新增**:①obligation control plane(状态机 + 签署权 + 内容绑定)· ②forge 治理链纳入同一控制面
  (`stage verdict → 授权登记 → 下一 intake 清偿`)· ③`SHARED-CONTRACT:993` post-P0 (b)(c)(d) 接手
- **调整**:④`needs-attention` 不再等价放行(XD-41)· ⑤四轮上限改风险/复杂度分档的有界 hard-stop(XD-44)
- **保留**:⑥R-Q7 双写 lib 与 preflight 解析器(实装件 refactor,不重写)
- **删除**:⑦「finding 类别重复作收敛信号」**reject 且不留暗门**
- **`evidence_grade` 建议**(采对方 R1 分级,我逐条核对后一致):
  `independent` = 核心 obligation 抽象 · `:993` 接手;
  `SOTA-corrected` = 纯 execution 地基被推翻 · XD-44 reject;
  `post-hoc-accepted` = 复合评级 · XD-41 并簇 · 粒度 reframe · **moderator 注入后的治理链扩面**
  · **`pending` 初态与签署权模型(这是对方 P3R1 的修正,我全额让步)**。
  ⚠ **请 synthesizer 不要把最后两项写成双侧独立结论。**

**W 含 `refactor-plan`** → 关键模块 3 个:
- **M1 · obligation 存储与状态机**(append-only;`satisfied` 绑内容身份;`pending` 由 gate 预建)
- **M2 · canonical gate 接线**(build 侧已知入口 + **forge Phase 0 intake / Phase 4 定稿**两处治理入口;
  逐入口,不得声称自动覆盖)
- **M3 · 签署与豁免**(policy 预置豁免 + operator-chair 例外;producer 只能提出)
⚠ **mirror 同步顺序必须标**:`SHARED-CONTRACT.md` 的 **SSOT 在 IDS**(与 bootstrap-kit 反向)⇒
**IDS 侧改 → cp 回 mirror → 更新 MANIFEST SHA**;改 **§6 B-4-IDS 须 bump `contract_version` + Changelog**。

---

**篇幅**:约 2100 CJK 字符,**具名超标声明**。超标来源:moderator 三问回应(硬要求)、
六条分歧逐条(对方 R1 新增第 6 条)、四条 v0.2 note 的「具名主体 + 触发时点 + 风险敞口」三字段
(v6 立的硬性最小字段集)。**均不可有损压缩。**

**⚠ 给 synthesizer 的两条硬提醒**:
1. 本轮**唯一一次真正的证伪**发生在 P2,推翻的是 **Opus 自己的地基**;
   P1 阶段的「双侧独立同意」当时**不构成验证**。
2. **`pending` 初态、签署权分层、治理链扩面**三项是 **Opus 让步 / moderator 注入后的产物**,
   `evidence_grade` 必须标 `post-hoc-accepted`,**不得包装成双方独立到达**。
