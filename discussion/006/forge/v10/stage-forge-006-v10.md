# Forge Stage · 006 · v10 · 「warn 从未被分型 —— 八条『声明存在但机制不存在』的同一根」

**Generated**: 2026-08-11T07:10:00Z
**Source**: forge run v10,X = 11 标的(1 权威快照[首选·自足] + 1 攒批原文 + obligation README/ledger + handback-validator 三件 + SHARED-CONTRACT §6.3.1 + hook 治理 + CLAUDE.md:100-130 + v9 verdict + HANDBACK-LOG 第 44/45 条 + XenoDev 白名单),Y = **架构设计(唯一视角 · operator 刻意收窄)**,Z = 对标 SOTA,W = `verdict-only` + `decision-list` + `refactor-plan`
**x_hash**: `dde3abd42f0fac55f7085e1c89d882d1`(全程冻结;快照内一处事实订正未改路径清单)
**Convergence mode**: `strong-converge`
**Rounds completed**: P1(both)· P2(both)· P3R1(both)· P3R2(both)
**Searches run**: **24 queries**(Codex 单侧,覆盖 Z 方向 1/2/3/5)across **8 个独立来源**;⚠ **Opus 侧 `WebSearch` 三次同错 400,退化为定向 `WebFetch`(非检索)取 2 锚点** —— 见 §underweights-5
**Moderator injections honored**: **none**(`moderator-notes.md` 全程不存在)
**Convergence outcome**: **converged** —— 四条分歧全部 finalize,双方 P3R2 均报 `unresolved: NO`;八条评级双方全部一致;3 条 v0.2 note
**Synthesizer note**: 本文档由**隔离子代理**撰写(与 v9 由主 session 直写不同 —— v9 §underweight-7 记录过该偏袒风险)。该隔离缓解了一个方向的风险,同时引入另一个,见 §underweights-3

---

> ## ⚠ Quality-check 未通过项(2 条 · 显式留痕,不静默)
>
> 承本轮 verdict 自己的精神(声明与实际状态的落差**必须产生信号**),synthesizer 的
> quality bar 自检结果如实前置:
>
> 1. **§Verdict 超 `≤200 字` bar**(实测约 350 字)。**原因**:本轮强制要求 verdict **正文**
>    承载 Codex P3R2 的 `0/3 生效` 订正句 + 对 K 的显式回应。**处置**:保留超长、不删订正 ——
>    删掉它,本文档就会原样复现 Opus 那次被判中的实质过述。
> 2. **文档总长超 `≤4000 字` bar**(实测约 9,000+ 字)。**原因**:W 三形态(verdict-only +
>    8 行 × 6 列 decision-list + 3 模块 refactor-plan)+ 15 行 evidence map + 9 条强制自批判。
>    **建议**:若要拆分,`§Decision matrix` + `§Refactor plan` 可独立成 `AUTHORIZATION-BRIEF-v10.md`,
>    本文件保留 verdict / evidence / underweights / decision menu。
>
> 其余 quality bar 全部通过(单一 verdict · 无 unresolved · Intake recap 五节齐 · W 章节与
> forge-config 一一对应且**未产 next-dev-plan** · 自批判非空 · 决策菜单 A/B/C/P/Z 齐 ·
> 无 >15 words 逐字引用 · 无不可溯源结论 · 无越 Y 视角内容进主章节)。

---

## How to read this

forge 是横切层(不属 L1-L4 任一层)。本轮**不重开 006 大方向**,只审攒批的簇 A(治理条款
的可执行性 4 条)+ 簇 B(声明存在但机制不存在 4 条),簇 C/D 显式排除。

**读法**:先读 §Verdict 一段;若你只想知道「与 v9 比新的是什么」,直接跳 §Evidence map 的
⭐ 三行(**warn 从未被分型** / **defer 是被裁出来的而非被忘记的** / **分类执法当前 0/3 生效**)。
Decision matrix 第 5 列 `evidence_grade` 与第 6 列 `obligation path` 是承 v6/v9 的方法论字段,**别跳**。

---

## Verdict

**采一条 warn 生命周期契约,并把它的执行边做成 hard admission gate。**

任何 `warn` 在**进入系统时**必须声明 `warn_class`:**`soft advisory`**(永久 defer 合法,
但须**显式承认无升级计划**)或 **`temporary`**(必带 **owner + due event + 已接线的 consumer gate**)。
**未声明分型者由 canonical admission gate `fail-closed` 拒绝** —— 拒绝是 hard 的、**不是第四个 warn**,
这是本 verdict 与它废掉的三条「复发 ≥N 次」判据(`check-7:16` / `check-8:26` / `CLAUDE.md:114`)
之间的**全部区别**。配两条边界条款:**① 存量与新增分域**(forward gate 对新对象硬拦,历史语料只读
不追溯)· **② 例外回收工具化**(工具消费基线、自动拒新增未归类豁免并清除失效例外)。
**XD-44′ 采分层语义**:确定性终态决定能否 ship,概率风险信号只分配注意力。
**v9 obligation ledger 只作交付承载面** —— 它管「不被忘记」,定义不了 review 终态、真跑证明、路径真值归属。

🔴 **verdict 正文必须同时承载的一句**(Codex P3R2 反核订正,**不得沿用「1/3 已能真拦」的表述**):
**此契约只有 M1 schema 与 M2 三处 hard-reject 均落地后才是机制;此前不得宣称 build/mirror 已受保护。**
`forge:<id>:phase4` 目前**只是已有 gate 的插入点,尚无 `warn_class` schema 或拒绝逻辑**
⇒ 分类执法当前 **`0/3` 生效 · `1/3` 有插入点 · `2/3` 连 gate 也未接线**。

**对 K 的直接回应**:这是「这根」的**结构性回答**(一条契约 + 两条边界条款),不是八条个案处置清单;
且它**不新增任何 warn**,而是要求既有 warn 分型 —— 因此满足 K 的 🔴 自指约束
(「任何再加一个 warn 型 check 的方案必须给出升级边的执行者与 gate」)。

---

## Evidence map

| # | 结论 | 来源 | 引用(≤15 words) | 反对/限缩证据 |
|---|---|---|---|---|
| ⭐1 | **真正的缺陷不是「warn 没有到期」,是「warn 从未被分型」**;永久 defer 合法但须显式标 soft | P2-GPT §1 row 2(PEP 387 / K8s)· P3R1-Opus §1(1) | 「永久 `defer` 可以合法」 | ⚠ **推翻 Opus P1 自己的地基**(见 §underweights-1);**Codex 单侧检索** |
| ⭐2 | 成熟 warn 治理 = **固定节奏复审 + 具名 tracking issue + 三态裁决**;关键区分是**被裁决出来的 defer vs 被遗忘的 defer** | P2-Opus §1 ⭐1 · P2-GPT §1 row 1(RFC 1589) | 「convert to error / revert / defer」 | ⚠ 限缩:RFC 场景是单团队 + 固定发布节奏,**本仓无自然时钟**,不得直接移植 |
| ⭐3 | **分类执法当前 `0/3` 生效** —— `forge:<id>:phase4` 只是插入点,无 schema 无拒绝逻辑 | P3R2-GPT §1 | 「只是 gate 位置已接线」 | ⚠ **订正 Opus P3R2 note 1 的过述**(原写「1/3 今天已能真拦」) |
| 4 | 三条「复发 ≥N 次」判据不是升级机制:**无计数者、无消费点、无执行者** | P1-Opus §1(2) · P1-GPT §2(KG-B15 行) | 「判据在第 2 次就达成……仍复发到第 4 次」 | 双方 P1 **独立同判**;快照 3.1 有带行号现场 |
| 5 | **存量/新增分域**是成熟解:PR 只对相对 baseline 的新代码施加失败条件 ⇒ 直接解 `check-8` 的 47/100 存量包 | P2-GPT §1 row 3(Sonar) | 「旧债不被追溯阻断」 | **Codex 单侧检索** |
| 6 | **例外回收可工具化**:失效抑制可被机器识别并自动删除 ⇒ 「只减不增」有执行者 | P2-GPT §1 row 4(Ruff `RUF100`) | 「并可自动删除」 | ⚠ **直接反驳 Opus P1 对 KG-B19 的诊断**;**Codex 单侧检索** |
| 7 | **XD-44′ 分层**:三终态由 ship gate 确定性消费;风险信号只分配注意力、**不决定放行或轮数** | P1-GPT §2 · P2-GPT §1 row 5 · 双方 P3R2 §1 | 「ship gate 直接消费终态并拒绝同形放行」 | ⚠ **关键性分级假说被判证据不足**(n=2);风险研究**不支持轮数或 ship gate** |
| 8 | **v9 ledger 是交付承载面,不是语义定义面**;`skipped` 只关闭升级义务,表达不了 advisory 的持续语义 | P1-GPT §2 前言 · P3R1-GPT §3 分歧 4 · P3R2-Opus §1 | 「相似数据模型不等于相似 enforcement coverage」 | ⚠ **Opus 两次偏袒被判中后才让步**(§underweights-2) |
| 9 | **XD-52**:4 轮上限的轮次真相住在对话记忆里,无机器可查计数器 | 双方 P1 §2(XD-52 行) | 「轮次真相应持久化」 | 双方 P1 **独立同判** |
| 10 | **XD-47**:假审与真审在解析层同形,输出不携带「gate 是否真跑过」,降级方向 **fail-open** | 双方 P1 §2(XD-47 行) | 「须携带可验证的 `ran/not-run`」 | 双方 P1 **独立同判** |
| 11 | **KG-B18**:`source_repo` 是 consumer 侧持权威值的字段,producer 声明它零信息增益 | 双方 P1 §2 **独立**判 `cut` | 「纯增可失真面」 | 最终形态(**producer 观察值 ≠ consumer 权威值分域**)是 Codex 细化后 Opus 接受 ⇒ 不得升 `independent` |
| 12 | **KG-B16 需跨仓完整性收据 / KG-B17 缺的是发布 gate 上的消费点** | P1-GPT §2 两行 | 「『单侧即落地』还需完整性收据」 | ⚠ 两条均为 **Opus 让步**(原判 `keep` / `refactor`) |
| 13 | **KG-B19**:v8 worktree 规约与 T102 精确路径白名单**在设计上互不兼容**;按 checkout 根归一是 git 自己的文档指引 | 快照 Part 2 B-4 · P2-Opus §1 row 2 | 「用 `git rev-parse --git-path`」 | 该冲突在 74 天无回审期间**从未被发现** —— 冲突本身是「没有回审」的产物 |
| 14 | ⭐ **Phase 0 obligation gate 首次真阻断且拦对**(命中 `OB-006-v9-01`,74 天回审被迫做完,当场删 3 条并产出 KG-B19) | forge-config §K · `.forge-state.json` · 快照 3.3 | 「74 天没做的回审在 gate 上被迫做完」 | ⚠ **n=1**;拦的是 **forge 自己这条链**;build 侧三 gate 全未接线;判据是最简形态 |
| 15 | **Opus 撰写的权威快照本身含错**:`consumer_wired:false` 真值 **9/11** 而非 10/11 | P2-Opus §3(4) 事实订正 · **由 Codex P1 抓出** | 「真值 9/11,不是 10/11」 | 已加**可见订正块**(不静默改数);实质结论不变 |

---

## Intake recap

### X · 审阅标的(11 个)
`_x-batch-snapshot.md`(权威快照 · 首选 · 自足)· `FORGE-006-v10-PENDING.md`(11 条攒批,簇 C/D 显式排除)·
`framework/obligations/README.md`(:60-91 schema + 接线状态)· `framework/obligations/ledger.jsonl`(11 条义务)·
`framework/xenodev-bootstrap-kit/handback-validator/`(check-7 / check-8 / `validate-handback.sh:76` 死变量)·
`framework/SHARED-CONTRACT.md`(§6.3.1 `:800-820` + Changelog `:1298`)· `framework/hook-allowlist-governance.md`(三不变量)·
`CLAUDE.md:100-130`(worktree 规约)· `discussion/006/forge/v9/stage-forge-006-v9.md`(上一轮 verdict)·
`discussion/001/handback/HANDBACK-LOG.md`(第 44/45 条)· XenoDev `.scan-credentials-ignore`(**双方均可读,无 BLOCK**)

### Y · 审阅视角
✅ **架构设计 —— 本轮唯一视角**。❌ 不选工程纪律 / 安全(operator 刻意收窄,非遗漏)

### Z · 参照系
mode: **对标 SOTA**。五方向:policy-as-code 强制边的下一层 / warn→error 升级治理 /
技术债与例外的到期 ratchet / 多 checkout 路径归一 / review 终止按关键性分级。
**外部材料叠加:无**(双方 §2 均标 `n/a`,未把检索结果冒充 operator 材料)
⚠ **方向 1/3/5 全部由 Codex 单侧覆盖**(Opus 侧 Z 执行故障 · §underweights-5)

### W · 产出形态
`verdict-only` + `decision-list`(8 行 × 6 列 · 第 6 列必填)+ `refactor-plan`(按模块 · 含 mirror 同步顺序)
🔴 **显式不产 `next-dev-plan`** —— obligation ledger 的 `due_gate` 已严格覆盖其核心功能且**有消费点**,
dev-plan 没有;同一件事两个载体、其中一个无消费点 = 给蒸发留后门(本仓已实证蒸发 3 次)

### K · 用户判准
要「这根的结构性回答,不是八个个案的处置清单」· **Y 只给架构设计是刻意的**,「执行不力 / 该有人跟进」
是**已排除项**(四次实证)· 🔴 **自指约束**:任何新增 warn 型方案必须同时给出升级边的**执行者与 gate** ·
通用机制优先但**不接受为通用性虚构抽象**;fail-closed 优先,**追溯性执法须单独论证** ·
不要 next-dev-plan,第 6 列 obligation path 必填 · **Phase 0 正面实证只有 1 个数据点,不得据此推论充分** ·
**要求 Codex 侧优先证伪而非补强**(v8 已标回声室风险高于 v7)

### 收敛模式
`strong-converge` —— 必须 finalize 单一 verdict;残余分歧降级为 v0.2 note。双方 P3R2 均报 `unresolved: NO`。
Codex 对「为何『三分之二执行边未接线』不构成 unresolved」的一句话回答:**未接线是已证实的落地前置条件,
有单一路径、具名 consumer 与可判定验收,不是两套架构主张仍冲突。**

---

## Verdict rationale(W · verdict-only)

**为什么是「分型」而不是又一条判据。** 双方 P1 独立认定:本仓三个 warn 机制各挂一条形状相同的
「复发 ≥2 次」升级判据,而 KG-B15 的同形判据**在第 2 次就达成、达成后仍复发到第 4 次**
—— 已有直接反例证明这种判据不产生任何行为(Evidence 4)。Opus P1 由此推出「warn 应当自带到期」,
**这一步被 P2 的 SOTA 推翻**:最成熟的 warn→error 治理(rustc RFC 1589)根本不用自动到期,
且明确把 `defer` 列为三种合法结局之一;PEP 387 进一步给出 soft/hard 分型 ——
**并非所有 warn 都要升级,永久 defer 合法,但必须显式标为 soft 并承认无移除计划**。
⇒ 缺陷的正确命名从「没有到期」改为「**从未被分型**」(Evidence ⭐1/⭐2)。

**为什么它不是第四个 warn。** K 的自指约束要求:给不出升级边的执行者与 gate 就不算解法。
本 verdict 的执行边由 Codex 在 P3R1 补上并经 Opus P3R2 全额接受:
**owner = warn 所在 SSOT 的 owner;`forge:<id>:phase4` hard-reject 缺 `warn_class` 的治理行;
`xenodev:task-review` / `xenodev:ship-gate` hard-reject 缺分类、或 `temporary` 却 `due_gate` 未接线。**
拒绝是 hard gate。这一句是本 verdict 唯一有资格区别于被它废掉的三条判据的地方 ——
**因此它也是本 verdict 最脆弱的地方:三处 hard-reject 一处未落地,契约就退回声明层**(§v0.2 note 1)。

**为什么 v9 不能吃下本批。** Opus P1 的最强怀疑是「本批多数只是 v9 obligation control plane 的
未接线实例」。Codex P1 **明确反对**并在 P2 顶住了 Opus 的第二次回归:v9 能防义务蒸发、能承载
KG-B16/B17 的交付欠债,但**定义不了 review 如何终止、怎样证明真跑、谁拥有路径真值**;
把这些塞成接线计划会把「义务存在」误当成「机制语义完整」(Evidence 8)。最终切法:
**ledger 承载裁决结果,warn registry / schema 承载规则语义,两层不混。**

**追溯性执法的单独论证**(K 明确要求):不采「全库翻硬 vs 永远 warn」的二选一,
采 Sonar new-code baseline 形态 —— forward gate 对新对象硬拦,历史语料只读不追溯。
这直接给出 `check-8` 若升 hard-fail 会把 **47/100 存量包整体判 corruption** 的出路(Evidence 5)。

---

## Decision matrix(8 行 + 1 作废行 × 6 列)

> 第 5 列 `evidence_grade` 承 forge 001 v6 条款(**记录回声室,不消除它**);
> 第 6 列 `obligation path` 承 v9 —— **指不出「谁产生、谁消费」的裁决不成立**。
> ⚠ **该列是约束性证明字段,不是 gate 本身。**

| 簇/条目 | 动作 | 评级 | 关键裁决 | `evidence_grade` | `obligation path`(产生 → 消费) |
|---|---|---|---|---|---|
| **A / XD-44′** | 新增 | `new` | 三终态 `approved` / `exhausted-with-open-findings` / `chair-override` 由 ship gate 确定性消费;风险信号仅提示 | `post-hoc-accepted` | `forge:006:v10:phase4 → xenodev:ship-gate` |
| **A / XD-52** | 调整 | `refactor` | 轮次真相持久化到文件系统,每轮入口机械读取 | **`independent`** | `forge:006:v10:phase4 → xenodev:task-review` |
| **A / XD-47** | 新增 | `new` | 输出必带可验证 `ran/not-run` + 被读对象内容身份;缺运行证据判失败且不计有效轮次 | **`independent`** | `forge:006:v10:phase4 → xenodev:task-review` |
| **A / KG-B15** | 调整 | `refactor` | **先消规约歧义再硬拦**(第 4 次是被告知后显式裁决,合法 checkpoint 与混线未分型) | `SOTA-corrected` | `forge:006:v10:phase4 → xenodev:task-review` |
| **B / KG-B16** | 调整 | `refactor` | 跨仓**完整性收据**堵「单侧实装即落地」 | `post-hoc-accepted` | `forge:006:v10:phase4 → xenodev:handoff-intake` |
| **B / KG-B17** | 新增 | `new` | 发布环节**消费** fixture 通过产物;环境无关 fixture 只是必要条件 | `post-hoc-accepted` | `forge:006:v10:phase4 → xenodev:handoff-intake` |
| **B / KG-B18** | 删除/分域 | `cut` | **producer 观察值 ≠ consumer 权威值**;新包由 consumer 派生,历史字段只读兼容 | `post-hoc-accepted` | `forge:006:v10:phase4 → xenodev:handoff-intake` |
| **B / KG-B19** | 调整 | `refactor` | checkout 根归一 + 例外 ratchet;**保留「两条框架规约曾设计不兼容」的事实** | `post-hoc-accepted` | `forge:006:v10:phase4 → xenodev:ship-gate` |
| **三条「复发 ≥N 次」判据**(`check-7:16` / `check-8:26` / `CLAUDE.md:114`) | **作废** | `cut` | 就地改写为分型声明;它们不产生行为(无计数者/消费点/执行者) | `SOTA-corrected`(诊断双侧独立,**替代形态**由 PEP 387 改判) | **`N/A(rejected)`** —— 作废项不产生 obligation |

**`evidence_grade` 分布**:`independent` ×2 · `SOTA-corrected` ×2 · `post-hoc-accepted` ×5。
⚠ **Codex 自查明写:上述任一升 `independent` 均属过高**(承 forge 001 v6 第 8 行高估的教训);
Opus P3R2 明确**不上调**。特别地:**KG-B18 判 `cut` 虽是双方 P1 独立同判,但其最终形态
(观察值 / 权威值分域)是 Codex 细化后 Opus 接受的,故为 `post-hoc-accepted`,不得因「双方都判 cut」而升级。**

🔴 **矩阵不得被读成「路径已可用」**:第 6 列的三个消费 gate
(`xenodev:ship-gate` / `xenodev:task-review` / `xenodev:handoff-intake`)
**目前全部 `consumer_wired: false`**(`framework/obligations/README.md:81-91`)。
登记 obligation 时 `exposure` 字段必填,三 gate 全接线前不得关闭。

---

## Refactor plan(3 模块)

> Codex P3R2 **有条件接受** Opus 的三模块切分;条件 = **M2 必须包含逐入口接线与跨仓完整性收据**。

### M1 · warn registry 与 `warn_class` schema
- **当前问题**:三个 warn 机制(`check-7:13` / `check-8:23` / `CLAUDE.md:112`)**全部未声明自己是哪一类**;
  分型若无载体会退化成写在各脚本注释里的自述 —— **即今天的状态**。
- **目标态**:`warn_class ∈ {soft advisory, temporary}` 有权威载体与 schema;
  `soft` 必须显式承认无升级计划;`temporary` 必须带 owner + due event + consumer gate。
- **步骤**:① 定 registry 载体(新文件?SHARED-CONTRACT 新节?ledger 兄弟文件?—— **v0.2 note 3**)
  ② 定 schema 与必填字段 ③ 把三条现存判据就地改写为分型声明(**它们的作废是 M1 的验收物**)。
- **风险**:载体选错会与 ledger 混成一层 —— 而「想让已有机制多扛一点」正是 Opus 两次偏袒 v9 的同一根。
- **预估代价**:**S**(纯 IDS 侧 · 但**是 M2 的前置,不可并行**)

### M2 · admission / consumer gate 逐入口接线 + 跨仓完整性收据
- **当前问题**:分类执法 **`0/3` 生效 · `1/3` 有插入点 · `2/3` 连 gate 也未接线**。
- **目标态**:三处 hard-reject 全部生效 —— `forge:<id>:phase4` 拒绝缺 `warn_class` 的治理行;
  `xenodev:task-review` / `xenodev:ship-gate` 拒绝缺分类或 `temporary` 而 `due_gate` 未接线者。
- **步骤**:① `forge:<id>:phase4` 从「插入点」补成「schema + 拒绝逻辑」
  ② `xenodev:task-review` 接线(承载 XD-52 / XD-47 / KG-B15)
  ③ `xenodev:ship-gate` 接线(承载 XD-44′ 三终态 / KG-B19)
  ④ `xenodev:handoff-intake` 接线(承载 KG-B16/B17/B18)
  ⑤ 🔴 **跨仓完整性收据**:每处接线产出可被对侧独立复核的收据,堵「单侧实装被当成已落地」。
- **风险**:v9 反证已在案 —— **逐入口接线成本省不掉,枚举清单本身可能缺席**;
  且这正是 v9 栽过的形状(verdict 下发、consumer 未接线、蒸发)。
- **预估代价**:**L**(跨仓 · 四个入口 · 是本轮的承重模块)

### M3 · 新旧分域与 ratchet 工具
- **当前问题**:`check-8` 若升 hard-fail 会把 **47/100 存量包**整体判 corruption;
  「只减不增」健康度指标**没有工具**(三个模式类识别至今 ⏳ 未实装);白名单条数随 worktree 数**线性膨胀**。
- **目标态**:forward gate 对新对象硬拦 / 历史语料只读不追溯(承 Sonar);
  工具消费基线、自动拒新增未归类豁免并清除失效例外(承 Ruff `RUF100`);路径按 checkout 根归一(承 git 文档)。
- **步骤**:① 定 baseline 与「新对象」判据 ② 实装模式类识别 ③ 路径归一后重跑白名单全表。
- **风险**:归一后 credential scan 对嵌套 checkout / 未跟踪文件 / gitignored 命中的边界**是否仍完备,
  本轮未裁**(Codex P1 §3-3,属安全视角,Y 未选)。
- **预估代价**:**M**

### ⚠ mirror 同步顺序(硬约束 · 不可颠倒)
```
IDS 侧改(SSOT · framework/)  →  cp 回 bootstrap-kit mirror  →  更新 MANIFEST SHA
```
**KG-B16 / B17 / B18 / B19 全部涉及 mirror**,而 **KG-B16 本身就是「单侧实装被当成已落地」的案例**
—— 在审这个病的同一轮里再犯一次会很难看。改 §6 须 bump `contract_version` + 写 Changelog。

### ⚠ 顺序硬约束(跨模块)
`M1 → M2`(schema 先于接线,否则 gate 无判据可拒);
`KG-B15 消歧 → hook block`(歧义未消先硬拦,会拦掉合法的 checkpoint 写入)。

---

## v0.2 notes(3 条 · 三字段齐全)

- **note 1 · 🔴 跨仓执法敞口 —— 本 verdict 的执行边当前 `0/3` 生效。**
  **主体**:M1 = IDS owner;M2 = XenoDev gate owners。**时点**:首个相关 task 的 pre-merge 前,
  由 operator-chair 验收。**风险敞口**:`forge:<id>:phase4` 只是**已有 gate 插入点,尚无
  `warn_class` schema 或拒绝逻辑**;`xenodev:task-review` / `xenodev:ship-gate` **连 gate 也未接线**
  ⇒ 接线前**新增 warn 仍可不分型进入系统**,须登记 `consumer_wired: false` + `exposure`,
  **三 gate 全接线前不得关闭**。**这正是 v9 栽过的同一形状**。

- **note 2 · 变更风险信号本轮不落地。**
  **主体**:IDS forge-protocol owner。**时点**:XD-44′ 终态语义上线后仍出现「终态正确但注意力错配」
  的实例时,在下一次 `/expert-forge 006` Phase 0 重提。**风险敞口**:注意力分配继续无判据(现状),
  但**不放宽 ship、不产生 obligation**,故非 fail-open。

- **note 3 · `warn registry` 的载体与 schema 未定形。**
  **主体**:M1 owner。**时点**:首个实现 task 的 pre-merge `/task-review`。
  **风险敞口**:无载体时 `warn_class` 会**退化为写在各脚本注释里的自述 —— 即今天的状态**。

---

## What this menu underweights(强制自批判)

**underweight-1 · 🔴 本轮唯一的真证伪在 P2,且推翻的是 Opus 自己的地基 —— 不得包装成双侧独立到达。**
Opus P1 主张「warn 应自带到期」,被 PEP 387 的 soft/hard 分型改判为「**warn 从未被分型**」。
Verdict 的**核心命名**因此是 `SOTA-corrected`,不是双侧独立到达的产物。
Ruff `RUF100` 同样**直接反驳**了 Opus 对 KG-B19「只减不增没有工具可执行」的诊断。

**underweight-2 · 🔴 Codex 三次判中 Opus:P1 一次、P2 一次(均为对 v9 机制的偏袒)、P3R2 一次(实质过述)。**
第二次发生在 **Opus 已因第一次被判中而明确自陈有偏袒动机之后**;第三次是本文档 §Verdict 里那处
`0/3` 订正(Opus 原写「IDS 治理行今天已能真拦」)。
⇒ **凡属「Opus 主张 v9 已覆盖某事」的结论,下游一律不得读成独立判断。**
同族事实:**Opus 撰写的权威快照本身含错**(`consumer_wired:false` 9/11 被写成 10/11),
由 Codex P1 抓出,已加可见订正块(Evidence 15)。

**underweight-3 · Phase 4 由隔离子代理撰写,方向与 v9 相反的局限。**
v9 由主 session 直写(其 §underweight-7 记录了撰写者即 reviewer 的偏袒风险);
本轮该风险已由隔离缓解。**但子代理未参与 P1-P3**,对各轮的语气、让步分量与「哪一句是真让步 /
哪一句是措辞退让」**只能从文本推断**,无法从过程感知。这是另一个方向的局限,如实记。

**underweight-4 · Opus P3R2 §4.5(与 K 的最终对齐)是事后补写。**
该节由 quality bar 自检发现「K 未在文件中被引用」后补写,**文件内已自我标注**,声明未新增实质主张。
本文档如实记入,**不当作原生内容**。

**underweight-5 · 🔴 Z 执行故障第三次复发 ⇒ 本轮 SOTA 覆盖事实上大部分单侧。**
Opus 侧 `WebSearch` 三次同错 400(`effort 'xhigh' not supported when thinking disabled`),
**与 forge 001 v6、forge 006 v9 完全相同的后端故障,第三次**。Opus 侧 Z 退化为定向 `WebFetch`(**非检索**),
**Z 方向 1/3/5 全部由 Codex 单侧覆盖**。⇒ Evidence ⭐1/5/6/7 的实证基础**没有跨模型交叉验证**;
与 v9 `underweight-1` 同形。**该故障已连续三轮降级 forge 的 Z 证据质量,本身应成为独立议题。**

**underweight-6 · 矩阵第 6 列的 obligation path 目前全部指向不可消费的 gate。**
三个 `xenodev:*` 消费 gate **全部 `consumer_wired: false`**。八条裁决登记后**登记了但不会被消费**,
唯一真实的消费点仍是 `forge:006:phase0`(即 forge 自己这条链)。

**underweight-7 · Y 单视角的两处已知盲区(operator 刻意收窄,非遗漏)。**
① **安全**:归一后 credential scan 对嵌套 checkout / 未跟踪文件 / gitignored 命中的边界是否完备
(Codex P1 §3-3 提出,本轮未裁);② **工程纪律**:`check-8` 追溯性执法的存量语料处置只给了架构形态,
未评估真实迁移成本。两者均值得后续 attention,但**不得据此把本轮结论读成已覆盖**。

**underweight-8 · `strong-converge` 的副作用 —— 双方都同意、但最可能被真跑打掉的三条。**
① **`warn_class` 的枚举完备性**:「什么算一条 warn」从未定义 ⇒ 与 v9 的枚举完备性敞口同形,
未被枚举的 warn 在契约之外原样存活;② **自然时钟仍无解**:`temporary` 的 due event 若永不发生,
该 warn 与今天的 `pending` 无异 —— RFC 1589 的 6 周 cycle 正是本仓没有的那个东西,双方均承认未解;
③ **簇 C(KG-B13/B14)/ 簇 D(XD-45/KG-49)是否被一般条款自然覆盖,双方 P3R2 都没回答** ——
快照 Part 5.5 明确要求「若覆盖请明说」,**这个问题在四轮里被静默掠过**。

**underweight-9 · Phase 0 正面实证的边界(K 明令)。**
gate 首次真阻断且拦对,但:① **只有 1 个数据点**;② 拦下的是 **forge 自己这条链**;
③ build 侧三个消费 gate 至今全部未接线;④ 判据是「同一 gate 名 + pending」这种**最简形态**,
尚未经历 `due_gate` 语义歧义 / 跨 gate / 到期判定的真实考验。**不得据此推论机制已充分。**

---

## Forge versioning 提示(v11 触发判据)

**任一命中即起 v11**:
1. 🔴 **M2 三处 hard-reject 未全部落地,而 build 侧又新增了未分型的 warn** ⇒ 本 verdict 停在声明层,
   与它审的病同形(**本轮最强判据**)。
2. **`warn_class` 的枚举清单上线后,发现清单外仍有 warn 在产生** ⇒ 分型的完备性敞口成真。
3. **`temporary` 的 due event 长期不发生**(自然时钟问题)⇒ 分型退化为 `soft` 的同义词。
4. **KG-B15 规约歧义消解后,混线仍复发** ⇒ 硬拦方向本身需重裁。
5. **`WebSearch` 400 第四次复发** ⇒ Z 证据质量连续四轮单侧,应作独立议题起 forge。

**已知待审(v11 候选)**:簇 C(KG-B13 `cdx-run` 静默重放 / KG-B14 `reuse-session` 静默降级)·
簇 D(XD-45 / KG-49 SKILL 与 `file_domain` 结构冲突)· IDS 现存 7 条 ⏳ 授权条目 ·
Codex 沙箱对 XenoDev 数字的独立复核能力。

**不该跑 v11 的情形**:本轮 9 项裁决**尚未行动过**时只想「再听一遍」⇒ 用 `/forge-inject`,不是起新 v。

---

## Decision menu(for human)

### [A] 接受 verdict,全量落地(推荐)
```
执行顺序(★ = 不可颠倒):

★1. M1 先定 registry 载体与 warn_class schema(v0.2 note 3)
    —— 它是三处 hard-reject 的判据来源;没定就接线 = gate 无可拒之物。

★2. M2 先补 forge:<id>:phase4 的 schema + 拒绝逻辑(把「插入点」变成「生效」)
    —— 成本最低、在 IDS 内、可作首个真跑样本;随后按
       xenodev:task-review → ship-gate → handoff-intake 逐入口接线,每处出跨仓完整性收据。

★3. KG-B15 先消规约歧义,再谈 hook block(否则硬拦会拦掉合法 checkpoint 写入)。

 4. M3 ratchet 工具与新旧分域;白名单在路径归一后重跑全表。

 5. XenoDev 侧按 AUTHORIZATION-BRIEF 下发(不当场改);
    mirror 件严格走 IDS SSOT 改 → cp → MANIFEST SHA 更新。
```
⚠ **本轮 W 未含 `next-PRD`**,故模板意义上的「fork 出 PRD branch + `/plan-start`」**不可用** ——
006 是框架治理 idea,落地路径是 IDS `framework/` 直改 + XenoDev 授权条目,不是 L4 PRD fork。
若确需走 PRD fork,选 [B] 起 v11 并在 intake 时加 `next-PRD` 形态。

### [B] 只落 M1 + `forge:<id>:phase4` 一段(止血核心 · 延续 v7 D1 / v8 / v9 先例)
只做分型 schema + IDS 治理行的 hard-reject,**build 侧三 gate 全部延后**。
**代价**:build/mirror 侧敞口继续开着(即 v0.2 note 1 的全部内容);
**收益**:一两周内可验证「分型 + hard-reject 是否真的拒得动」,失败会立刻暴露。
⚠ 选 [B] 必须同时接受:**此期间不得宣称 build/mirror 已受保护。**

### [C] 局部接受
逐行挑 9 行矩阵。⚠ **三条「复发 ≥N 次」判据的作废行不可不选** —— 不作废它们,
落地会自动退回「再记一条判据」,即 K 明令排除的那种交差。
⚠ **M1 与 XD-44′/XD-52/XD-47 可拆**(前者是通用契约,后三者是 review gate 的具体语义),
但 **M1 与 M2 不可拆**(schema 无接线 = 声明层,正是本轮在审的病)。

### [P] Park
```
/park 006
```
保留全部 v10 产物,不落地。**代价**:三个 warn 机制继续无分型;KG-B15 大概率出现第 5 次;
白名单条数随 worktree 数线性膨胀,同时违反不变量 1 与不变量 3。

### [Z] Abandon
```
/abandon 006
```
放弃本批。**需写 lesson 文档**说明为什么「声明存在但机制不存在」这一族不值得治理 ——
⚠ 该结论会同时作废 v9 的 obligation control plane(本批八条中四条以其为承载面)。

---

## Forge log

- **v10: 2026-08-11** — verdict: "**采一条 warn 生命周期契约,并把执行边做成 hard admission gate** ——
  任何 warn 进入系统时必须声明 `warn_class`(`soft advisory` = 永久 defer 合法但须显式承认无升级计划 /
  `temporary` = 必带 owner + due event + 已接线 consumer gate),**未分型者 fail-closed 拒绝,
  拒绝是 hard 的、不是第四个 warn**;三条「复发 ≥N 次」判据全部作废;两条边界条款 =
  存量与新增分域(承 Sonar new-code baseline · 解 check-8 的 47/100)+ 例外回收工具化(承 Ruff `RUF100`);
  XD-44′ 分层(确定性终态管 ship,风险信号只管注意力);**v9 ledger 只作交付承载面,
  定义不了 review 终态 / 真跑证明 / 路径真值归属**。
  🔴 **此契约只有 M1 schema 与 M2 三处 hard-reject 均落地后才是机制;此前不得宣称 build/mirror 已受保护**
  —— 分类执法当前 **0/3 生效 · 1/3 有插入点 · 2/3 连 gate 也未接线**(Codex 反核订正 Opus 的过述)。
  ⭐ **本轮唯一真证伪在 P2,推翻的是 Opus 自己的地基**(「warn 应自带到期」→「warn 从未被分型」,PEP 387);
  🔴 **Codex 三次判中 Opus**(P1/P2 对 v9 的偏袒 + P3R2 的实质过述),且第二次发生在自陈偏袒动机之后;
  Opus 撰写的权威快照本身含错(9/11 被写成 10/11),由对方抓出。
  ⭐ **Phase 0 obligation gate 首次真阻断且拦对**(命中 v9 自标的『最强判据』OB-006-v9-01,
  74 天回审被迫做完,删 3 条失效条目并产出 KG-B19)—— **但 n=1,拦的是 forge 自己这条链**。
  ⚠ **Opus 侧 `WebSearch` 400 第三次复发**,Z 方向 1/3/5 全部 Codex 单侧。
  `evidence_grade`:`independent` ×2 / `SOTA-corrected` ×2 / `post-hoc-accepted` ×5。"
- **v9: 2026-08-10** — obligation control plane(gate 预建 `pending` / `satisfied` 绑内容身份 /
  `skipped` 权威签署 / 到期 fail-closed);原诊断「四条全是 execution gap」被 SOTA 推翻。
- **v8: 2026-07-13** — 七项 dogfood 缺口 → 四簇裁决(gate 执行语义 / 分支拓扑含 worktree-per-idea /
  LlmClient v2 / 证据 hook 治理)。
- **v7: 2026-07-06** — review gate 状态机(不 cut codex)+ fork-id 进 SHARED-CONTRACT §7 作 SSOT。
