---
name: forge-protocol
description: Cross-cutting expert-forge protocol. Two reviewers audit existing artifacts (repo code / multi-stage docs / external materials) under user-declared X/Y/Z/W + K + convergence-mode, run SOTA benchmark, then jointly converge to a single verdict + W-shaped deliverables. NOT part of L1-L4 pipeline. Load when invoking /expert-forge or reading forge run artifacts.
disable-model-invocation: false
---

# Forge · Cross-cutting Expert Forge Protocol

## Path placeholder convention(重要,先读这一段)

本协议里所有路径用 **`<DISCUSSION_PATH>`** 作为 forge 工件根。它的实际值由
`/expert-forge` 命令的 Step 0.1 计算:

- **root idea** 时(`<id>` = 纯数字如 `005`):`<DISCUSSION_PATH>` = `discussion/<id>`
  - 例:`<id>=005` → `<DISCUSSION_PATH>=discussion/005`
- **fork** 时(`<id>` 含非数字后缀如 `005-pA` / `002b-stablecoin-payroll`):`<DISCUSSION_PATH>` = `discussion/<root>/<id>`(`<root>` = `<id>` 的前导数字串)
  - 例:`<id>=005-pA` → `<DISCUSSION_PATH>=discussion/005/005-pA`
  - 例:`<id>=002b-stablecoin-payroll` → `<DISCUSSION_PATH>=discussion/002/002b-stablecoin-payroll`

forge 工件**统一在 `<DISCUSSION_PATH>/forge/v<N>/` 下**(无论 root 还是 fork)。

**Codex queue id** 与路径无关,直接 = `<id>`(`$ARGUMENTS`):
- root:`.codex-inbox/queues/<id>/HEAD`(如 `.codex-inbox/queues/005/HEAD`)
- fork:`.codex-inbox/queues/<id>/HEAD`(如 `.codex-inbox/queues/005-pA/HEAD`)

参见 `.codex-inbox/README.md` v2 协议。

## What forge is for

forge 是一个**横切动作**(cross-cutting),不是 L1/L2/L3/L4 任何一层。它解决一个 pipeline 没有覆盖的工作模式:

> **双专家审阅"已经存在的东西"(repo / 多份 stage 文档 / 外部材料),做 SOTA 对标,然后强制收敛到单一 verdict + 草案产出**。

典型场景:
- 已经基于某个 idea 开发了几版 repo,想让专家拍板"redesign 还是 incremental optimize"
- 手头有一份较成熟的 idea 文档,想让专家审阅 + SOTA 对标 + 直接产出可执行 PRD
- 多个外部 repo / 历史 stage 文档需要被综合评估,产出"下一版本应该长什么样"

forge 通过 **4+1 变量(X/Y/Z/W + K)+ 收敛强度** 的通用 Phase 0 抽象,让同一命令既能审 repo 现状,也能审 idea 草稿,也能审任何成熟标的。

## What forge is NOT for

- **NOT 用于从零发散一个想法**(那是 L1 inspire 的工作)
- **NOT 用于深挖一个抽象 idea 的价值/新颖性/扩展**(那是 L2 explore 的工作)
- **NOT 用于产出候选 PRD 菜单 defer 给 human 拍板**(那是 L3 scope 的工作)
- **NOT 用于工程实现/任务拆解**(那是 L4 plan 的工作)
- **NOT 用于纯 code review**(那是 /code-review 的工作 — forge 是产品 + 架构 + 工程纪律的综合审阅)

## Forge vs L2/L3 — 关键区别

| 维度 | L2/L3 | forge |
|---|---|---|
| **输入** | 文档(proposal / stage doc) | repo 代码 + 多份 stage 文档 + 外部材料 + 用户关切 |
| **双方姿态** | 设计师(daydreamer) — 从零想象 | 审阅人(reviewer) — 评判已存在物 |
| **工作流** | 独立想 → 互读 → 收敛到候选菜单 | 读现状 → SOTA 对标 → 联合收敛到单一 verdict |
| **决策权** | defer 给 human(给菜单选) | **强制收敛**(默认 strong-converge) |
| **产出** | 候选 PRD 菜单 | 单一 verdict + W 形态可执行草案 |
| **搜索** | 价值验证 / scope-reality | SOTA 对标 / 实现路径调研 |
| **是否进 pipeline** | 是 — L1→L2→L3→L4 | 否 — 横切层,可以在 pipeline 任何位置触发 |

## 4+1 变量 + 收敛强度

每次 `/expert-forge` 启动时,Phase 0 collect 这 6 个值,持久化到 `forge-config.md`:

### X · 审阅标的(必填,free-text 粘贴)

可包括(可多选):
- 本仓库子目录路径(如 `discussion/005/L3/`)
- 外部 repo 绝对路径(如 `/Users/admin/codes/idea_gamma2/`)
- URL(双方用 WebFetch 抓)
- 直接粘贴的文本块(用户在 intake 里贴一大段)
- 历史 stage 文档引用(如 `discussion/005/L2/stage-L2-explore-005.md`)

**沙箱约束**:Codex 默认沙箱在仓库内,读外部路径可能 BLOCK。用户负责处理沙箱(如 `cp -r` 拷贝外部 repo 到仓库内的 `_forge-targets/`),或在 Codex 端调整 scope。

### Y · 审阅视角(必填,multi-select)

合法视角(双方 P1 必须按这些视角组织观察):
- **产品价值** — 这玩意儿对真实用户是不是真有用?
- **架构设计** — 模块切分、抽象层次、可演化性
- **工程纪律** — 测试、CI、SDD/spec-driven 程度、code review 机制
- **安全** — 输入验证、密钥管理、permission boundary、attack surface
- **教学价值** — 是否能让用户在使用过程中学到东西
- **商业可行** — 是否有可持续商业模式
- **用户体验** — 易用性、onboarding、错误恢复
- **free-text** — 用户自定义视角

### Z · 参照系(必填,single-select + 可叠加用户外部材料)

三种 mode:
- **对标 SOTA** — 双方在 P2 各自检索领域 SOTA(如 addy osmani agent-skills、Spec Kit、Devin、Cursor 等)
- **对标指定列表** — 用户在 intake 里给出对标项清单,双方只对标这几个
- **不对标,纯内部审阅** — 跳过 P2 SOTA 搜索,P2 仅做"用户外部材料消化"

**外部材料叠加**:不论选哪种 mode,用户都可在 K 里贴外部材料(链接 / 文本片段 / 文件路径),双方在 P2 必须消化。

### W · 产出形态(必填,multi-select)

决定 forge-synthesizer 在 stage 文档里产出哪些章节:
- **verdict-only** — 只要 verdict + 简短 rationale(≤500 字)
- **decision-list** — 4 列矩阵(保留 / 调整 / 删除 / 新增),每行引用 evidence
- **refactor-plan** — 按模块分组(当前问题 / 目标态 / 改造步骤 / 风险)
- **next-PRD** — 下一版 PRD 草案(用 scope-protocol PRD 章节模板)
- **next-dev-plan** — 下一版 dev plan(按 phase / milestone 切,不到 spec 级)
- **free-essay** — 长篇综合(800-1500 字)

multi-select 时按上面顺序拼接,共享前置 §"Verdict" + §"Evidence map"。

### K · 用户判准(必填,free-text)

贯穿所有 phase 的"你最在乎什么"。例:
> "4 个 repo 都被 deprecate 过,需要专家拍板 redesign 还是 incremental optimize。我看重最少代码重写量、必须用上已验证的两个 novelty、v0.1 必须 polish 拿得出手。"

K 是审阅人姿态的"指南针" — P1 §0 必须引用 K,P3R1 § 与 K 的对齐性自检必须存在,P3R2 verdict 必须显式回应 K。

### 收敛强度

- **strong-converge**(默认) — P3R2 必须 finalize 单一 verdict;残余分歧降级为 v0.2 note
- **preserve-disagreement** — P3R2 允许并存 2 个 verdict,各自独立完整;synthesizer 不强行合一

## Reviewer stance vs Daydreamer stance(双方姿态)

forge 的双专家是 **审阅人**,不是 **设计师**:

| 姿态维度 | 审阅人(forge) | 设计师(L2) |
|---|---|---|
| 起点 | 已经存在的东西 | 一张白纸 |
| 第一动作 | 把现状读懂 | 凭印象想象未来 |
| 评价语言 | "这里 X 不行,因为 Y;应该 Z" | "这个 idea 的核心价值是 X" |
| 时间感 | 立足现在 → 看下一步 | 立足未来 → 描绘可能性 |
| 风险偏好 | 先看坏处再看好处 | 先看美处再看限制 |

forge 严禁退化成 daydreamer 模式 — 双方在 P1/P2 任何时候都不能凭空想象"如果有这么个东西就好了",必须从 X 标的的具体内容出发。

## 5 个 Phase

```
Phase 0 · Intake (single)         ← human 填 4+1 变量 + 收敛强度
Phase 1 · 独立审阅 (1 round)      ← 双方按 X 读标的、按 Y 视角写 first-take,无搜索
Phase 2 · 参照系评估 (1 round)    ← 双方按 Z 跑搜索 + 消化外部材料
Phase 3 · 联合收敛 (R1 + R2)      ← R1 标分歧 / R2 按收敛强度 finalize
Phase 4 · synthesizer (single)    ← 主进程 Task 调 forge-synthesizer
```

### Phase 0 · Intake

由 `/expert-forge` 命令编排:
1. **X** 自由文本粘贴(用户在终端贴路径列表 / URL / 文本块)
2. **K** 自由文本粘贴(用户写"我最在乎什么")
3. **Y** AskUserQuestion(multi-select)
4. **Z** AskUserQuestion(single-select + 是否叠加外部材料)
5. **W** AskUserQuestion(multi-select)
6. **收敛强度** AskUserQuestion(single-select)

收齐后写 `<DISCUSSION_PATH>/forge/v<N>/forge-config.md`(格式见下文§"forge-config.md output format")。

### Phase 1 · 独立审阅

双方各自:
- 读 X 中所有标的(本仓库 Read / 外部路径 Read / URL WebFetch / 粘贴文本直读)
- 读 forge-config.md(拿 4+1 变量)
- 读 forge-protocol/SKILL.md
- **不读对方 P1**(parallel independence)
- **不跑搜索**(那是 P2)
- 按 Y 视角组织观察,产 first-take

产出:`<DISCUSSION_PATH>/forge/v<N>/P1-<Model>.md`(模板见 §"P1 template")

### Phase 2 · 参照系评估

双方各自:
- 读对方 P1(此处不再 parallel-blind,因为 P1 已交叉)
- 读自己 P1
- 按 Z 跑搜索:
  - mode=对标 SOTA → 检索领域 SOTA(prior-art / 失败案例 / 演化路径)
  - mode=对标指定列表 → 只检索 K 里指定的对标项
  - mode=不对标 → 跳过搜索,只消化用户外部材料
- 消化用户在 K 里贴的外部材料

产出:`P2-<Model>.md`(模板见 §"P2 template")

### Phase 3 · 联合收敛(R1 + R2)

#### R1 · 标分歧

双方各自:
- 读双方 P1 + P2(整合)
- 产初步 verdict + 列 ≥1 关键分歧 + 引用对方原话

产出:`P3R1-<Model>.md`(模板见 §"P3R1 template")

#### R2 · finalize

双方各自:
- 读对方 P3R1
- 按 convergence_mode 行事:
  - **strong-converge**:必须 finalize 单一 verdict;残余分歧降级 minor;给 W 形态产出的初步草稿建议
  - **preserve-disagreement**:允许列 2 个并存 path,各自独立完整;给 synthesizer 的"保留两条 path 不强行合一"指令

产出:`P3R2-<Model>.md`(模板见 §"P3R2 template")

### Phase 4 · synthesizer

主进程通过 `Task` 工具调 `forge-synthesizer` subagent。subagent 读 forge-config + 8 个 round file,按 W 路由章节,产 `stage-forge-<id>-v<N>.md`。

详见 `.claude/agents/forge-synthesizer.md`。

## forge-config.md output format

```markdown
---
forge_version: v1
created: <ISO>
convergence_mode: strong-converge | preserve-disagreement
x_hash: <md5 of X 路径列表字符串>
---

# Forge Config · <id> · v<N>

## X · 审阅标的

<用户粘贴的原始 free-text,不做加工>

### 解析后的标的清单

- <path 1>(类型:本仓库子目录 / 外部 repo / URL / 粘贴文本 / stage 文档)
- <path 2>
- ...

## Y · 审阅视角

✅ <视角 1>
✅ <视角 2>
...

## Z · 参照系

mode: 对标 SOTA | 对标指定列表 | 不对标
**指定列表**(若 mode=指定):
- <对标项 1>
- ...
**外部材料叠加**(若用户在 K 里提到):
- <材料指针>

## W · 产出形态

✅ <形态 1>
✅ <形态 2>
...

## K · 用户判准

<用户粘贴的原始 free-text>

## 收敛强度

✅ <strong-converge | preserve-disagreement>

---

## Summary for reviewers

**审阅标的总数**: <n>
**视角维度**: <list>
**参照系**: <one line>
**预期产出**: <list>
**用户最在乎**: <one paragraph 摘要 K>
**收敛模式**: <strong-converge | preserve-disagreement>
```

## P1 template

```markdown
# Forge v<N> · <id> · P1 · <Model> · 独立审阅(no search)

**Timestamp**: <ISO>
**Searches used**: NONE in this round.
**Visibility**: I did NOT read other reviewer's P1.
**Reviewer stance**: 审阅人 — 评判已存在物,不是 daydream。

## 0. 我读到的标的清单 + 阅读策略

- 我读了:<逐条列 X 中读了的标的 + 该标的的核心读取范围>
  - 例:`/Users/admin/codes/idea_gamma2/` → 读了 README + technology_roadmap + .claude/skills/pipeline 目录
- 我跳过的:<逐条列因 BLOCK / 不可达 / 时间预算跳过的标的 + 原因>
- **K(用户判准)摘要**:<引用 K 关键句,1-2 段>
- **我的阅读策略**:<例:按 Y 视角=工程纪律 + 架构设计 优先看 .claude/skills/ 和 commands/ 结构;按 Y=产品价值 优先看 README 和 stage 文档>

## 1. 现状摘要(按 Y 视角组织)

每个 Y 视角 1-3 段。**只描述,不评价**(评价在 §2)。

### 视角 A · <Y 第 1 项>
<现状描述,引用具体文件/段落>

### 视角 B · <Y 第 2 项>
...

## 2. First-take 评分(按 Y 视角)

每个 Y 维度给 keep / refactor / cut / new 倾向 + 1-2 句理由。**这是审阅人的诚实第一反应**。

| Y 维度 | 倾向 | 理由(引用 §1 现状) |
|---|---|---|
| <Y 第 1 项> | keep / refactor / cut / new | <理由> |
| <Y 第 2 项> | ... | ... |

## 3. 我现在最不确定的 3 件事

留给 P2 搜索 / P3 协商。**不要假装确定** — forge 的价值在于把不确定性显式化。

1. <不确定点 + 我希望搜什么验证 + 或希望对方在 P3 给我什么洞见>
2. ...
3. ...
```

**Style**:
- 800-1500 字
- 每个 Y 维度都必须出现在 §1 + §2
- §0 必须引用 K
- 不允许跨入 SOTA 对比(那是 P2)
- 不允许写 PRD / dev plan / refactor 详细方案(那是 Phase 4)

## P2 template

```markdown
# Forge v<N> · <id> · P2 · <Model> · 参照系评估(with search)

**Timestamp**: <ISO>
**Searches run**: <n>, <SOTA-benchmark | 指定对标 | 仅外部材料消化>
**Visibility**: 我已读对方 P1。

## 1. SOTA 对标(或指定对标)

| 标的 X' | 参照项 | 它怎么做 | 我们怎么做 | gap | URL/Source |
|---|---|---|---|---|---|
| ideababy_stroller | addy osmani agent-skills | 20 skills + 7 commands + AGENTS.md 自累积 | 4 层 pipeline + L4 build worktrees | <gap 描述> | https://addyosmani.com/blog/agent-skills/ |
| ... | ... | ... | ... | ... | ... |

paraphrase findings,verbatim quote ≤15 words。

## 2. 用户外部材料消化

如果 K 里有外部链接 / 文本 / 文件,逐项处理:
- **材料 1**:<指针>
  - 哪些可吸收 → <list>
  - 哪些会改方向 → <list>
  - 哪些是噪音 → <list,可空>
- **材料 2**:...

## 3. 修正后的视角

P1 哪些判断站住,哪些被对标推翻。每条引用 §1 或 §2 的具体证据。

- P1 判断 A "<原话>" → **站住**(因为 SOTA <X> 也是这么做)
- P1 判断 B "<原话>" → **被推翻**(因为 SOTA <Y> 已证明 <相反结论>)
- ...
```

**Style**:
- 600-1100 字
- §1 至少 3 条对标(若 mode=对标 SOTA / 指定对标)
- §2 至少处理用户提供的所有外部材料
- §3 至少 3 条修正(站住或被推翻)
- 严禁跨入 PRD / dev plan(那是 Phase 4)

**搜索约束**:
- mode=对标 SOTA: SOTA-benchmark search only;forbidden = tech-stack-deep-dive / pricing / 实施细节
- mode=指定对标: 只搜 K 里给的对标项
- mode=不对标: 不跑 web search,§1 章节标 "n/a (mode=不对标)"

## P3R1 template

```markdown
# Forge v<N> · <id> · P3R1 · <Model> · 联合收敛 R1(标分歧)

**Timestamp**: <ISO>
**Visibility**: 我已读对方 P1 + P2。
**Searches in this round**: NONE(避免 R1 又开搜索发散)。

## 1. 整合摘要

读完双方 P1 + P2 后,我对"这件事现在的样子"的整合理解(2-3 段,引用关键证据)。

## 2. 我的初步 verdict(草案)

单段,3-5 行。**直接给立场**,不要 hedge。

例:"我倾向 incremental optimize,不 redesign。理由:(1) ...(2) ...(3) ...。
关键不确定点是 X,如果 R2 解决不了,我会改为 redesign。"

## 3. 关键分歧清单

每条:
- **分歧 N**:<一句话标题>
  - 我的立场:<原话>
  - 对方立场(引用对方 P1/P2 原句,≤15 words):"..."
  - 我希望 R2 怎么收敛:<具体方向>

至少 1 条。如果真的没分歧,写"§3 无 — 双方在 P1/P2 已高度对齐,R2 重点在 W 形态产出的草案"。

## 4. 与 K 的对齐性自检

把 K 摘出来,逐条 check 我的 verdict 是否对齐:
- K 第 1 条 "<原话>" → ✅ / ⚠ / ❌ + <说明>
- ...
```

**Style**:
- 600-1000 字
- §3 是核心,必须有具体引用
- §4 是审阅人姿态的关键 check — 不能漂离 K

## P3R2 template

```markdown
# Forge v<N> · <id> · P3R2 · <Model> · 联合收敛 R2(finalize)

**Timestamp**: <ISO>
**Visibility**: 我已读对方 P3R1。
**Convergence mode**: <strong-converge | preserve-disagreement>(从 forge-config 读)
```

### Strong-converge 模式

```markdown
## 1. 我对每条分歧的最终立场 + 让步

针对 P3R1 §3 列出的每条分歧,我的最终立场:
- **分歧 1**(原标题):
  - 对方在 P3R1 给的论证:"..." → 让步 / 反驳 / 部分接受
  - 我的最终立场:<原话>
  - 让步给对方的部分:<list 或 "无">
- **分歧 2**:...

## 2. 联合 verdict(单一)

**我和对方在 R2 后达成的单一 verdict**:<一段,200-400 字>

如果 R2 后双方仍冲突,标 §"unresolved"(synthesizer 会处理):
- **unresolved**:<分歧名> — 我的立场 vs 对方立场,各自论证

## 3. 残余分歧降级为 v0.2 note

不影响主 verdict 但值得记录的小分歧:
- v0.2 note 1:<内容 + 何时该回头看>
- ...

## 4. W 形态产出的初步草稿建议

针对 forge-config 的 W 选择,给 synthesizer 我的草稿建议:
- W 含 verdict-only → 我的 verdict 关键句:"..."
- W 含 decision-list → 我建议的 4 列矩阵 row(列前 5 条):
  - 保留:<list>
  - 调整:<list>
  - 删除:<list>
  - 新增:<list>
- W 含 next-PRD → 关键产品决策点(2-3 条):...
- W 含 next-dev-plan → 关键 milestone(2-3 条):...
- W 含 refactor-plan → 关键模块(2-3 个):...
- W 含 free-essay → 关键论点(2-3 条):...
```

### Preserve-disagreement 模式

```markdown
## 1. 已收敛点

R2 后双方已对齐的部分(按 P3R1 §3 各条分歧):
- **分歧 1** → 已收敛到 <立场>(双方都接受)
- **分歧 N** → 仍未收敛(进 §2)

## 2. 仍并存的分歧(允许 2 个 verdict)

允许列出最多 2 个并存的 verdict path,每个独立完整:

### Path A · <我的 verdict>
<verdict 单段,200-400 字 + 各自的核心论证>

### Path B · <对方的 verdict 摘要 + 我对它的诚实表述>
<verdict 单段 + 论证>

## 3. 给 synthesizer 的指令

"保留两条 path,不强行合一。Path A 适用 <场景 X>,Path B 适用 <场景 Y>。
Human 必须在两条 path 之间选,选的标准是 <K 中的某条 + 外部因素>。"
```

**Style**:
- 700-1200 字
- strong-converge 模式 §2 必须给单一 verdict 或显式标 unresolved
- preserve-disagreement 模式 §3 必须给"何时选哪条" 的指导
- §4(strong-converge)是 synthesizer 的输入材料,要具体不要抽象

## Codex inbox templates

每个 phase 的 Codex 任务文件 frontmatter 共有字段:

```
**Queue**: <id>
**Created**: <ISO>
**Recommended model**: gpt-5.5
**Recommended reasoning_effort**: xhigh
**Estimated tokens**: ~8-15k(oneshot) / ~5-10k(reuse-session)
**Kickoff form**: oneshot | reuse-session
**Forge version**: v<N>
**Phase**: P<n>
```

### P1 inbox(oneshot)

```markdown
# Codex Task · <id> · forge v<N> · P1(独立审阅)

**Queue**: <id>
**Created**: <ISO>
**Recommended model**: gpt-5.5
**Recommended reasoning_effort**: xhigh
**Estimated tokens**: ~8-15k
**Kickoff form**: oneshot
**Forge version**: v<N>
**Phase**: P1

## Your role

You are GPT-5.5 xhigh, Reviewer B, forge v<N> on idea <id> Phase 1。
**审阅人姿态** — 评判已存在物,不是 daydream。

## HARD CONSTRAINTS

- NO web search this phase(那是 P2)
- DO NOT read <DISCUSSION_PATH>/forge/v<N>/P1-Opus47Max.md(parallel independence)
- 不允许写 PRD / dev plan / refactor 详细方案(只产 first-take)
- 不允许跨入 SOTA 对比(那是 P2)
- §0 必须引用 K(用户判准)
- 按 Y 视角组织 §1 现状摘要 + §2 first-take 评分

## Read in order

1. `<DISCUSSION_PATH>/forge/v<N>/forge-config.md`(拿 X/Y/Z/W/K + 收敛强度)
2. `<DISCUSSION_PATH>/forge/v<N>/moderator-notes.md`(若存在,binding — 用户在 P1 启动前可能已 inject)
3. X 中的全部标的(逐条列在下面 § "X 标的清单")
4. `.claude/skills/forge-protocol/SKILL.md`(P1 template)
5. `AGENTS.md`(若存在)

## X 标的清单

<逐条列 forge-config 解析后的 X 路径,标注类型 + 推荐读取范围>

## Write

`<DISCUSSION_PATH>/forge/v<N>/P1-GPT55xHigh.md` using P1 template:
- §0 我读到的标的清单 + 阅读策略
- §1 现状摘要(按 Y 视角)
- §2 First-take 评分
- §3 我现在最不确定的 3 件事

800-1500 字。

## When done

Write `.codex-outbox/queues/<id>/<TS>-<id>-forge-v<N>-p1.md` with:
- **Completed**: <ISO>
- **Files written**: <list + word count>
- **Headline**: <one-line 现状一句话总结>
- **Verdict**: CLEAN | CONCERNS | BLOCK
  - BLOCK 用于沙箱拒读外部 repo / X 中标的不可达
- **First-take summary**: 每个 Y 维度的倾向(keep/refactor/cut/new)
- **Notes for Claude Code**: 任何 orchestrator 需要知道的(包括是否触发 BLOCK)

Filename **must match** the inbox file basename so HEAD pointer works:
`<TS>-<id>-forge-v<N>-p1.md`
```

### P2 inbox(reuse-session)

```markdown
# Codex Task · <id> · forge v<N> · P2(参照系评估)

[共有 frontmatter,Kickoff form = reuse-session]

## Session hint(only meaningful if Codex reuses session from P1)

你已读过(本轮请勿重读):
- `.claude/skills/forge-protocol/SKILL.md` 的 P1 部分
- `<DISCUSSION_PATH>/forge/v<N>/forge-config.md`
- 你自己的 `<DISCUSSION_PATH>/forge/v<N>/P1-GPT55xHigh.md`
- X 中所有标的

本轮**新增需读**:
- `.claude/skills/forge-protocol/SKILL.md` 的 P2 template 部分
- **`<DISCUSSION_PATH>/forge/v<N>/P1-Opus47Max.md`** ← 对方 P1
- `<DISCUSSION_PATH>/forge/v<N>/moderator-notes.md`(若存在,binding)
- 用户外部材料(K 中提到的链接 / 文件路径)

**HARD CONSTRAINT**(reuse-session only):do NOT re-read files you read in
the previous round of this Codex session unless this task explicitly lists
them above.

## Your role

forge v<N> P2 — 按 Z 跑搜索 + 消化外部材料。

## CONSTRAINTS

- 搜索约束(按 forge-config.Z):
  - 对标 SOTA: SOTA-benchmark search only;forbidden = tech-stack-deep-dive / pricing / 实施细节
  - 指定对标: 只搜 K 里给的对标项
  - 不对标: 不跑 web search,§1 章节标 "n/a (mode=不对标)"
- §1 至少 3 条对标(mode≠不对标 时)
- §2 必须处理用户提供的所有外部材料
- §3 至少 3 条修正(站住或被推翻)
- verbatim quote ≤15 words

## Write

`<DISCUSSION_PATH>/forge/v<N>/P2-GPT55xHigh.md`(template 在 forge-protocol SKILL §"P2 template")

600-1100 字。

## When done

outbox 同名文件,含:
- Verdict: CLEAN | CONCERNS | BLOCK
- Headline: SOTA 对标的一句话 verdict("我们 vs SOTA 的核心 gap 是 X")
- Searches: <n>,主要 source 列表
- 修正点(P1 哪些站住、哪些被推翻):简表
```

### P3R1 inbox(reuse-session)

```markdown
# Codex Task · <id> · forge v<N> · P3R1(联合收敛 R1)

[共有 frontmatter,Kickoff form = reuse-session]

## Session hint

新读:
- `.claude/skills/forge-protocol/SKILL.md` 的 P3R1 template
- **`<DISCUSSION_PATH>/forge/v<N>/P2-Opus47Max.md`** ← 对方 P2(对方 P1 已在 P2 读过)
- `<DISCUSSION_PATH>/forge/v<N>/moderator-notes.md`(更新版,若存在)

## Your role

forge v<N> P3R1 — 标分歧、给初步 verdict。

## CONSTRAINTS

- **NO new search this round**(避免 R1 又开搜索发散)
- 必须列 ≥1 关键分歧(若真无,在 §3 显式说"§3 无 — 双方对齐,R2 重点在草案")
- 必须给初步 verdict 草案(§2,直接给立场不要 hedge)
- §4 与 K 的对齐性自检必须存在
- 引用对方原句 ≤15 words

## Write

`<DISCUSSION_PATH>/forge/v<N>/P3R1-GPT55xHigh.md`(template 见 SKILL §"P3R1 template")

600-1000 字。

## When done

outbox 同名文件,含:
- Verdict: CLEAN | CONCERNS | BLOCK
- Headline: 我的初步 verdict(一句话)
- 分歧数: <n>
- 与 K 对齐性: ✅ / ⚠ / ❌ + 简短说明
```

### P3R2 inbox(reuse-session)

```markdown
# Codex Task · <id> · forge v<N> · P3R2(finalize)

[共有 frontmatter,Kickoff form = reuse-session]

## Session hint

新读:
- `.claude/skills/forge-protocol/SKILL.md` 的 P3R2 template
- **`<DISCUSSION_PATH>/forge/v<N>/P3R1-Opus47Max.md`** ← 对方 P3R1
- `<DISCUSSION_PATH>/forge/v<N>/moderator-notes.md`(更新版,若存在)

## Your role

forge v<N> P3R2 — 按 convergence_mode finalize:
- strong-converge → 单一 verdict;残余分歧降级 minor
- preserve-disagreement → 允许 2 个并存 path

(从 forge-config.md frontmatter 的 convergence_mode 读)

## CONSTRAINTS

- 严格按 convergence_mode 行事,不允许混用两种模式
- strong-converge 时若 R2 后仍冲突,§2 显式标 "unresolved"(synthesizer 会处理)
- §4(strong-converge)给 synthesizer 的草稿建议必须具体到可执行
- preserve-disagreement 时 §3 必须给"何时选哪条 path"的指导

## Write

`<DISCUSSION_PATH>/forge/v<N>/P3R2-GPT55xHigh.md`(template 见 SKILL §"P3R2 template")

700-1200 字。

## When done

outbox 同名文件,含:
- Verdict: CLEAN | CONCERNS | BLOCK
- Convergence: converged | preserved-2-paths | unresolved
- Final verdict 关键句(strong-converge)/ 两条 path 标题(preserve-disagreement)
- 给 synthesizer 的草稿建议是否齐全(W 形态对应)
```

## forge-synthesizer output structure

stage 文档 `stage-forge-<id>-v<N>.md` 的结构:

### 强制章节(无论 W)

1. 标题块:`# Forge Stage · <id> · v<N> · "<title from K 摘要>"`
2. metadata:Generated / Source / Rounds completed / Searches run / Convergence mode / Moderator injections honored
3. **§ How to read this** — 一段话讲清这是什么 + 它和 L1-L4 的关系(强调横切层)
4. **§ Verdict**(≤200 字)— 单一 verdict(strong-converge)或两条 path 的并列(preserve-disagreement)
5. **§ Evidence map** — 每条结论必须能回引到 P1/P2 的具体段落
6. **§ Intake recap** — 摘要 X / Y / Z / W / K(回应"用户在乎什么、我们怎么响应")
7. **§ What this menu underweights**(强制自批判,对标 scope-synthesizer §"Honesty check")
8. **§ Decision menu**(forge 专属):
   - `[A]` 接受 verdict 进 L4 plan-start
   - `[B]` 跑 forge v2(说明需要补什么)
   - `[C]` 局部接受(列哪几条采纳,哪几条挂起)
   - `[P]` park
   - `[Z]` abandon

### 按 W 路由的可选章节

- W 含 `verdict-only` → 增 §"Verdict rationale"(扩 200-500 字)
- W 含 `decision-list` → 增 §"Decision matrix"(4 列:保留 / 调整 / 删除 / 新增,每行引用 evidence)
- W 含 `refactor-plan` → 增 §"Refactor plan"(按模块分组:当前问题 / 目标态 / 改造步骤 / 风险)
- W 含 `next-PRD` → 增 §"Next-version PRD draft"(用 scope-protocol PRD 章节模板,但内容来自 forge 已验证事实)
- W 含 `next-dev-plan` → 增 §"Next-version dev plan"(按 phase / milestone 切,不到 spec 级)
- W 含 `free-essay` → 增 §"Long-form synthesis"(800-1500 字)

## Convergence quality bars(Phase 4 触发前检查)

forge-synthesizer 启动前,主命令必须确认:

- [ ] forge-config.md 存在且完整(4+1 变量都填了)
- [ ] 8 个 round file 齐全(P1×2 + P2×2 + P3R1×2 + P3R2×2)
- [ ] 双方 P3R2 没有 BLOCK
- [ ] strong-converge 模式下,双方 verdict 已对齐(或显式标 unresolved)
- [ ] preserve-disagreement 模式下,双方 P3R2 都按要求列了 paths(**每方最多 1 条 path**;synthesizer 综合后 stage 文档最多 2 条 path)
- [ ] K 在双方 P3R2 中至少被引用 1 次(可通过 grep 验证)

任意 fail → Phase 4 不触发,打印 diagnostic + 给修复选项。

**Path 数硬约束**:preserve-disagreement 模式下,无论双方分歧多大,stage 文档最多并列 2 条 path。如果双方实际立场跨度超出 2 路能容纳,synthesizer 在 §"What this menu underweights" 显式说明"分歧域宽度超出 2-path 容量,某些子立场未表达"。这是产品语言的硬约束 — 给用户超过 2 条选择会让 Decision menu 失配(用户读完无法决策)。

## Forge versioning rules

forge 是横切层,允许同一 idea 反复 forge:

- **v1**:首次 `/expert-forge <id>`,产物在 `<DISCUSSION_PATH>/forge/v1/`
- **v2**:v1 done 后再次 `/expert-forge <id>`,新建 `<DISCUSSION_PATH>/forge/v2/` 子目录;v1 整目录保留不动
- **v<N>**:同上

**何时建议跑 v<N+1>**:
- X 标的发生变化(repo 演化、新外部材料加入)
- 上一版 verdict 被实证推翻(用户基于 v<N> verdict 行动后发现走偏)
- 用户判准(K)发生重大变化

**何时不该跑新版**:
- 仅是想"再听一遍"双方意见(那应该是 /forge-inject 注入 moderator note)
- 上一版 verdict 还没行动过

## Codex sandbox edge cases

X 中包含外部 repo 路径时,Codex 默认沙箱可能 BLOCK:

- **检测**:每次 Phase 推进前,主命令 grep outbox 文件首 30 行有无 `Verdict: BLOCK`
- **命中 BLOCK**:不写下一阶段 inbox + 摘录理由 + 给三选一:
  - `[A]` 调整 X(剔除读不到的标的)→ 起 v<N+1> 重跑
  - `[B]` 调整 Codex 沙箱 scope 后 cdx-run 重试当前 phase
  - `[C]` abort 当前 v
- **预防**:Phase 0 intake 完成后,主命令可选地 `ls` 验证 X 中所有路径存在(read-only check),不可达的提示用户预先 `cp -r` 拷贝到 `_forge-targets/` 子目录或用 free-text 直接粘贴关键内容

## Forge 与 L1-L4 的关系

forge 不进 L 系列 pipeline,但可以在 pipeline 任何位置触发:

- **可在 L0 触发**(idea 还没正式跑过 L1):forge 一份纯 idea 文档 + 外部材料,直接产出 PRD
- **可在 L2 后触发**:用 L2 stage 文档作 X 的一部分,forge 决定是否进 L3
- **可在 L3 后触发**(典型):用 L3 候选 + repo 现状作 X,forge 收敛到下一版 PRD(005 首跑场景)
- **可在 L4 中途触发**:repo 已开发数版,forge 拍板 redesign vs incremental optimize(005 场景)
- **可在 L4 后触发**:产品已 ship,forge 评估"下一阶段 roadmap"

forge 产出 ≠ 直接进 L4 — 用户读 stage 文档后,通过 Decision menu `[A]` 可以"接受 verdict 进 L4 plan-start",但这是单独的动作,不是 forge 自动衔接。

## Quality bars for advancing forge → L4 / next action

forge 是 done enough 当:
- 所有 4 个 phase 完成(8 个 round file 齐全)
- forge-synthesizer 产出 stage-forge-<id>-v<N>.md
- stage 文档包含强制章节(verdict + evidence + intake recap + 自批判 + decision menu)
- W 形态对应的可选章节齐全
- 用户读完后能基于 verdict 做下一步动作(进 L4 / 跑 v2 / park / abandon)

如果用户读完仍觉得"verdict 不够锐利,无法行动",**说明双专家收敛机制有问题**(可能是 K 不够强、convergence_mode 选错、Y 视角设错),需要改 protocol 或跑 v<N+1>。
