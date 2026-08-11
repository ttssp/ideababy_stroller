# P3R2 · Opus 4.7 Max · forge 006 v10 · finalize(strong-converge)

> 零新检索。已读:双方 P1/P2 + 双方 P3R1 + forge-config;`moderator-notes.md` 不存在。

## §1 · 我对每条分歧的最终立场

**分歧 1 · XD-44′ —— 全额接受「分层并存」。**
`approved` / `exhausted-with-open-findings` / `chair-override` 三终态由 **ship gate 确定性消费**,
决定能不能 ship;**变更风险信号只分配注意力,不得决定放行或轮数**,降为可选 v0.2 note、**不产生 obligation**。
这比我 P3R1 的「二选一」更准:我当时把「不能当 gate 判据」误当成「不能存在」。

**分歧 2 · KG-B19 —— 一致。** 评级 `refactor`,但**冲突事实必须进 rationale**:
v8 worktree 规约与 T102 精确路径白名单**在设计上曾不兼容**,归一与 ratchet 是消解手段;
不得把一个**已知的规约级冲突**写成普通实现欠债。

**分歧 3 · KG-B16 —— 已让步,锁定。** `refactor` + 完整性收据堵「单侧即落地」。

**分歧 4 · 我让步,且对方的切法比我的好。**
我原主张「v9 的 `skipped` 在形状上已是被裁出来的 defer,PEP 387 的 soft 分型可直接表达为
ledger 的一个字段」。Codex 的限定成立:**`skipped` 只能关闭「升级义务」,不能表达
advisory 本身的持续语义** —— 一个永久 soft advisory 不是「一次被签掉的义务」,
它是**一条持续有效的规则属性**。
⇒ 采其分层:**ledger 承载裁决结果,warn registry / schema 承载规则语义,两者不混成一层。**
把它们混成一层正是我 P1/P2 两次偏袒 v9 的同一根 —— **想让已有机制多扛一点**。

**自指检验 —— 接受其答案,这是本 verdict 成立的前提。**
owner = **warn 所在 SSOT 的 owner**;`forge:<id>:phase4` **hard-reject** 缺 `warn_class` 的治理行;
`xenodev:task-review` / `xenodev:ship-gate` **hard-reject** 缺分类、或 `temporary` 却 `due_gate` 未接线。
**该拒绝是 hard gate,不是第四个 warn** —— 这一句是本 verdict 与被它废掉的三条
「复发 ≥N 次」判据之间的全部区别。

## §2 · 联合 verdict(单一 · 无 unresolved)

**采一条 warn 生命周期契约,并把它的执行边做成 hard admission gate。**

任何 `warn` 在**进入系统时**必须声明 `warn_class`:
- **`soft advisory`** —— 永久 defer 合法,但必须**显式承认无升级计划**(承 PEP 387);
- **`temporary`** —— 必带 **owner + due event + 已接线的 consumer gate**。

**未声明分型者由 canonical admission gate `fail-closed` 拒绝**,拒绝是 hard 的、不是新的 warn。
本仓现存三条「复发 ≥N 次」判据(`check-7:16` / `check-8:26` / `CLAUDE.md:114`)**全部作废**,
就地改写为分型声明 —— 它们不是升级机制:**无计数者、无消费点、无执行者**。

配两条边界条款:**① 存量与新增分域** —— forward gate 对新对象硬拦,历史语料只读不追溯
(承 Sonar new-code baseline;直接解 `check-8` 的 47/100 存量包);
**② 例外回收工具化** —— 由工具消费基线、自动拒新增未归类豁免并清除失效例外
(承 Ruff `RUF100`;`KG-B19` 的「只减不增」由此获得执行者)。

**XD-44′ 采分层语义**:确定性终态决定能否 ship,概率风险信号只分配注意力。
**v9 obligation ledger 只作交付承载面** —— 它保证「该做的不被忘记」,
**定义不了** review 终态、真运行证明、路径真值归属;后者是本轮的新结构,不得并入接线计划。

## §3 · 残余分歧 → v0.2 note(三字段齐全)

- **note 1 · 🔴 本 verdict 的执行边有三分之二落在未接线的 gate 上。**
  分型的 hard-reject 依赖 `forge:<id>:phase4`(✅ 已接线)+ `xenodev:task-review`(❌ 未接线)
  + `xenodev:ship-gate`(❌ 未接线)。⇒ **IDS 治理行今天就能真拦,XenoDev build/mirror 行不能。**
  **主体 + 时点**:XenoDev gate owner,在 `xenodev:task-review` 首个接线 task 的 pre-merge 前;
  由 operator-chair 验收。**风险敞口**:在接线前,build 侧新增 warn **仍可不分型进入系统** ——
  **这正是 v9 栽过的同一个形状(verdict 下发、consumer 未接线、蒸发)**,本轮必须睁着眼睛记下来。
- **note 2 · 变更风险信号本轮不落地。** **主体 + 时点**:若未来 XD-44′ 终态语义上线后
  仍出现「终态正确但注意力错配」的实例,由 IDS forge-protocol owner 在下一次 `/expert-forge 006`
  Phase 0 重提。**风险敞口**:注意力分配继续无判据(现状),但**不阻断 ship**,故非 fail-open。
- **note 3 · `warn registry` 的载体与 schema 未定形。** **主体 + 时点**:M1 owner 在首个实现 task
  的 pre-merge `/task-review` 提交(是新文件?SHARED-CONTRACT 的新节?ledger 的兄弟文件?)。
  **风险敞口**:无载体时 `warn_class` 会退化为写在各脚本注释里的自述 —— 即今天的状态。

## §4 · W 形态产出建议(给 Phase 4)

- **verdict-only**:§2 全文即是,≤400 字,可直接采用。
- **decision-list**:8 行 × 6 列。**评级定案**:XD-44′ `new` · XD-52 `refactor` · XD-47 `new` ·
  KG-B15 `refactor` · KG-B16 `refactor` · KG-B17 `new` · KG-B18 `cut` · KG-B19 `refactor`
  (双方 P3R1 后**全部一致**)。
  **第 5 列 `evidence_grade` 按 Codex P3R1 的分级定案,我不上调**:
  RFC 1589 **证据锚点** = `independent`(双侧独立到达且经封存);
  **「soft/temporary 二分」整条 verdict = `SOTA-corrected`**(不是 `independent` —— 它由 PEP 387 改判);
  XD-44′ 三终态 / KG-B16 完整性收据 / KG-B18 观察值-权威值分域 = `post-hoc-accepted`
  (**若标 `independent` 都属过高**,承 forge 001 v6 第 8 行高估的教训)。
  **第 6 列 obligation path 必填**,`N/A(rejected)` 只给「复发 ≥N 次」三条作废项。
- **refactor-plan**:三模块 —— **M1 warn registry 与 `warn_class` schema** ·
  **M2 admission gate 逐入口接线**(含 note 1 的两个未接线 gate)· **M3 ratchet 工具与新旧分域**。
  ⚠ **mirror 同步顺序硬约束不可颠倒**:SSOT(IDS `framework/`)侧改 → `cp` 回 mirror →
  MANIFEST SHA 更新。KG-B16/B17/B18/B19 **全部涉及 mirror**,而 KG-B16 本身就是
  「单侧实装被当成已落地」的案例 —— 在审这个病的同一轮里再犯一次会很难看。

## §4.5 · 与 K 的最终对齐(⚠ 事后补写 · 2026-08-11T06:41Z)

> **诚实标注**:本节是 Phase 4 quality bar 自检发现「K 未在本文件被引用」后**补写**的,
> 不是与 §1-§4 同时写成。补写只把已有内容对 K 显式归位,**未新增任何实质主张**。
> 之所以标注而非静默补:本轮的病就是「声明与实际状态之间的落差不产生信号」。

- **K「要这根的结构性回答,不是八个个案清单」** → ✅ §2 是一条契约 + 两条边界条款,八条各自落位。
- **K「Y 只给架构设计,不产执行不力型结论」** → ✅ 全程未出现;四波让步全部落在结构层。
- **🔴 K 的自指约束「新增 warn 必须给出升级边」** → ✅ **本 verdict 不新增任何 warn**;
  它要求既有 warn 分型,且分型的执行边是 **hard admission gate 而非第四个 warn**(§1 末段)。
  这是本 verdict 唯一有资格区别于被它废掉的三条判据的地方。
- **K「通用机制优先,但不接受虚构抽象」** → ✅ 分型来自 PEP 387,不是我方发明。
- **K「fail-closed 优先,追溯性执法须单独论证」** → ✅ Sonar new-code baseline 即该论证。
- **K「不要 next-dev-plan」** → ✅ §4 只到模块级。
- **K「decision-list 第 6 列必填」** → ✅ §4 已明写,`N/A(rejected)` 只给三条作废判据。
- **K「gate 正面实证只有 1 个数据点,不得据此推论充分」** → ✅ 我因此撤回了 P2 对 v9 的评价提升。
- **K「优先证伪而非补强」** → ✅ 唯一真证伪来自对方且推翻我;我的两次偏袒均被判中并已记入 §5。

## §5 · 给 synthesizer 的两条硬提醒

1. **本轮唯一的真证伪在 P2,且推翻的是 Opus 自己的地基**(「warn 应自带到期」被 PEP 387 改判为
   「warn 从未被分型」)。**不得包装成双侧独立到达。**
2. 🔴 **Codex 两次判中 Opus 对 v9 的偏袒(P1 一次 · P2 一次),且第二次发生在 Opus 已因第一次
   被判中而明确自陈有偏袒动机之后。** 这不是花絮,是**本轮 evidence 可信度的直接输入** ——
   凡属「Opus 主张 v9 已覆盖某事」的结论,下游一律不得读成独立判断。请写进 underweights。
