# Forge Stage · 006 · v8 · "七项 dogfood 缺口 + worktree 隔离诉求的四簇裁决"

**Generated**: 2026-07-13T13:00:00Z
**Source**: forge run v8 with X = 6 标的（1 权威快照[首选·自足] + 1 外部原文[可选核对·BLOCK 可跳] + 1 v7 verdict 承接 + 2 仓宪法 + 1 proposal 背景文本）, Y = 架构设计 + 工程纪律 + 用户体验, Z = 对标 SOTA（worktree 隔离模式 · LLM role 分离 · gate 单次执行/防重放 · monorepo gitignore 模板 · hook 误报治理）, W = verdict-only + decision-list + refactor-plan + next-dev-plan
**Convergence mode**: strong-converge
**Rounds completed**: P1 (both), P2 (both), P3R1 (both), P3R2 (both)
**Searches run**: 11 across ~11 distinct sources（Claude Code 原生 `-w` flag + 社区并行实践 · OpenAI Model Spec + OWASP LLM01 · ACME/AP2/OAuth nonce 一次性 + GitHub stale approvals · gitleaks/detect-secrets 集中 allowlist 治理 · stacked-branch 显式 base）
**Moderator injections honored**: none（无 `discussion/006/forge/v8/moderator-notes.md`）
**Convergence outcome**: converged（单一 verdict · 双方 P3R2 §2 逐条同案 · 四条分歧全签字收敛 · 无 unresolved · 4 条 v0.2 note）

---

## How to read this

forge 是横切层（不是 L1-L4 pipeline 的一部分）。本文档是 v8 forge run 双专家审阅 + SOTA 对标 + 联合收敛后的产物，**强制给出立场**（不是候选菜单 defer 给你拍板）。本轮**不重开 006 大方向**，专审 XenoDev dogfood-backlog 攒批的六条框架缺口（KG-B2..B7）+ operator worktree 隔离诉求，承接 v7（review gate 状态机 + fork-id SSOT）。

- W 勾了 **verdict-only + decision-list + refactor-plan + next-dev-plan** 四块，本文档就产这四块。
- verdict 是**单一收敛**（strong-converge），骨架取自双方 P3R2 §2 逐条同案的联合 verdict。
- decision-list 七行逐条标簇号 + P 级 + 证据源；refactor-plan 四模块 = 四簇，每模块含 mirror 同步顺序；next-dev-plan 双仓分道（IDS 侧 vs XenoDev 授权条目）。
- 读完你应能直接进 §"Decision menu" 选 [A] 全落 / [B] 局部先落 P0 / [C] 跑 v9 / [P] park。
- 与 v7 的关系：v7 已预判 KG-B2 是 KG-B1 下游、KG-B4 与 KG-B2 同簇为「下批料」；本轮兑现该预判并把 B4 与 B7 合簇。

## Verdict

**incremental optimize，不 redesign，零 cut。** 七项批次收敛为**四个改造簇，全部 refactor/new，既有强 gate、Safety Floor fail-closed、codex primary 地位全部不动**：① **（P0）gate 执行语义**（B4+B7 合簇）——SHARED-CONTRACT 新章定四条不变量（gate task 语义 / PASS artifact 机器查验 / 已判 run 登记一次性消费 / 新 run 作废 stale 签字），XenoDev preflight 落最轻实现（机器可读登记表），终结「防 V4 的 STOP 只是 markdown 约定」；② **（P0 规约 + P1 机制）分支拓扑显式化**（B2+worktree 诉求合簇）——session-per-idea worktree 复用原生 `-w`（零自建），main 生命周期 = proposal → idea 分支 → human checkpoint 合回 → 清理，build 基线从隐含 main 改机器可读声明，warn 型 preflight 起步；③ **（P0 契约 / P1 实施）LlmClient role 分离**（B5）——messages-style 进契约作 v2，legacy adapter 保兼容，allowlist 序列化降级保留为纵深防御；④ **（P1）证据与 hook 治理**（B3+B6）——gitignore 模板路径无关豁免 + 证据入仓机器检查，hook 白名单按模式类集中收敛 + 定期回审，明拒逐例加白。四簇均有 SOTA 直接对应物，无一处发明新轮子。

单一 verdict 回应 K：**七项一项不漏**（四簇覆盖七项，映射显式）；**尊重证据权重**（B5 九轮 / B7 三轮硬证据判 new 且最高档）；**止血核心优先、防过度工程**（worktree 复用原生零自建、gate 登记表文件级、hook 校验从 warn 起步——延续 v7 D1「只落止血核心」先例）；**gate 强制性不靠程序纪律**（①簇全部机器可验）；**动冻结契约给迁移路径**（B5 legacy adapter + v1/v2 并存 + 兼容测试）。

## Evidence map

| 结论 | 来源 | 引用 | 是否有反对证据 |
|---|---|---|---|
| 七项 = 三个结构缺口 + 两类纪律摩擦，非七个孤立 bug | P1-Opus §1 + P1-GPT §1 + P3R1 双方 §1 | "并行多 idea/多 fork 的分支拓扑没有成为框架对象" | - 双方 P1 起即同判 |
| B4+B7 = 同一 gate 执行语义缺口的静态面/动态面 | P1-Opus §1(a) + snapshot KG-B4/B7 原文 + P3R1 双方分歧4 | "gate 只有判定逻辑，没有执行语义" | - 双方同判 |
| B2+worktree = 同一分支拓扑缺口在 build 侧/治理侧两症状 | P1-Opus §1(b) + P1-GPT §1 + snapshot Part1 混线实证 | "20+ commits 混在一根 009 命名分支" | - 双方同判 |
| B5 判 new（契约变更），非继续补 sanitizer | P1-Opus §2 + P2-Opus §1 row2 + P2-GPT §3 + snapshot KG-B5 | "9 轮不收敛 = 证据链完整" | ⚠ GPT P1 §2 原判 refactor，P2 搜索后自改 new |
| worktree「命令支持」档 = Claude Code 原生 `-w`，无需自建 | P2-Opus §1 row1 + P2-GPT §1 row1（本机 `claude --help` 实证） | "命令支持档原生已有" | - 双方 P2 独立核实 |
| B7 三要素（单次/一次性/stale 作废）业界各有对应，组合现成 | P2-Opus §1 row3 + P2-GPT §1 row3 | "组合现成模式即可，强制点可以很轻" | - SOTA 背书 |
| hook 白名单必须按模式类收，不按撞一次加一条 | P2-Opus §1 row4 + §3 修正3 + P2-GPT §1 row4 | "逐例加白与 KG-B1 逐例放宽 regex 同构风险" | - 双方同判（KG-B1 史佐证） |
| worktree 校验 P0 = warn 型 preflight，hook block 留 v0.2 | P3R1-GPT 分歧1 + P3R2 双方 §1.1 | "本周混线发生在无任何机器提示的环境下" | ⚠ Opus P1/P3R1 原倾向「现在就加轻 hook」，R2 让步撤回 |
| main 生命周期 = proposal→idea 分支→checkpoint 合回→清理 | P3R1-GPT 分歧3 + P3R2 双方 §1.3 | "main 是 accepted governance artifact 归档线" | - 双方 R2 收敛 |
| gate 不变量进 SHARED-CONTRACT 新章，SKILL 只落实现 | P3R1-GPT 分歧4 + P3R2 双方 §1.4 | "语义不能只在 parallel-builder SKILL" | ⚠ Opus P2「强制点可以很轻」被误读为落 SKILL，R2 澄清=实现轻非语义轻 |
| 零 cut（七项全有真实复现证据，无一推演） | P1-Opus §2 + snapshot 全部 KG-B 复现场景 | "证据质量显著好于 v5" | - 对齐 forge-verdict-vs-empirical-ship 教训 |
| B3 静默失效两个 task 才发现（T001.log 从未入 git） | P1-Opus §1 工程纪律 + snapshot KG-B3 | "T001.log 从没进 git（git ls-files 空）" | - 快照硬证据 |
| B6 hook 与 parallel-builder §6.1 明写范式直接冲突 | P1-Opus §1 + snapshot KG-B6 | "§6.1 mktemp 私有 dir 是 SKILL 明写范式" | - 快照硬证据 |

（表以最 load-bearing 的 13 条为限；标 ⚠ 的四条反对/修正证据在 §"What this menu underweights" 展开。）

## Intake recap

### X · 审阅标的（6 个）
- **权威快照[首选·自足]** · `discussion/006/forge/v8/_x-batch-snapshot.md`（本仓库文件 · operator worktree 诉求原话 + IDS 混线实证 + KG-B2..B7 六条全文 @ XenoDev cc4edeb + XenoDev CLAUDE.md 工作流摘录）
- **外部原文[可选核对·BLOCK 可跳]** · `/home/ys/codes/XenoDev/dogfood-backlog.md`（外部 repo · Codex 沙箱可能 BLOCK · 仅 Grep 核对不整读）
- **v7 承接** · `discussion/006/forge/v7/stage-forge-006-v7.md`（stage 文档 · review gate 状态机 + fork-id SSOT verdict · KG-B2/B4 已预判为下批料）
- **IDS 宪法** · `CLAUDE.md`（本仓库文件 · session/分支/目录工作流定义处 · worktree 议题 IDS 侧现状基准）
- **XenoDev 宪法** · `/home/ys/codes/XenoDev/CLAUDE.md`（外部 repo · BLOCK 可跳 · 快照 Part3 已含摘录）
- **proposal 背景** · `TEXT:proposal-006`（粘贴文本 · K 首四段 · 本轮不重审大方向）

### Y · 审阅视角
- ✅ 架构设计（框架机制缺口主视角：B2 拓扑 / B4+B7 gate 执行语义 / B5 接口契约 / worktree 分支拓扑）
- ✅ 工程纪律（B3 TDD 证据入仓 / B6 hook 与 SKILL 范式冲突 / 流程规约可执行性）
- ✅ 用户体验（operator 单人多线操作心智负担 / B6 高频误报的 UX 摩擦）

### Z · 参照系
- mode: **对标 SOTA**
- 检索方向：worktree 隔离模式（含 Claude Code 官方用法）· LLM role 分离作 prompt-injection 防御标准 · gate 单次执行/防重放先例 · monorepo gitignore 模板 · pre-commit/credential hook 误报治理
- 用户外部材料：**无**（K 未给额外链接）

### W · 产出形态
- ✅ verdict-only · ✅ decision-list（7 项）· ✅ refactor-plan（四簇分组）· ✅ next-dev-plan（双仓 P0/P1/P2）

### K · 用户判准
本轮不重开 006 大方向，审 XenoDev dogfood-backlog 六条框架缺口 + operator worktree 诉求，收敛 verdict + 各条改造方案 → 下发双仓落地 brief。七项：**KG-B2**(build 基线偏离)、**KG-B3**(TDD 证据被 gitignore 吞)、**KG-B4**(gate PASS 无机器强制)、**KG-B5**(LlmClient 无 role 分离 · 九轮硬证据)、**KG-B6**(credential hook 误报 fail-closed)、**KG-B7**(盲测 gate 试错/重放 · 三轮硬证据)、**operator worktree 隔离诉求**（session-per-idea worktree，main 只留 proposal 期）。operator 在乎：可靠 > 全面、止血核心优先防过度工程（v7 D1 先例）、gate 强制性不靠程序纪律、尊重证据权重。**硬约束**：mirror 件三层同步（SSOT 侧改 + cp 回 mirror + MANIFEST SHA · 本周刚实证 mirror 漂移 IDS bd3dd70 修复）；动 T001 冻结接口须给迁移路径。

### 收敛模式
strong-converge

---

## Decision matrix（7 项批次 × 4 列）

| 类别 | 项 | 来源（标的具体位置） | 理由 | 优先级 |
|---|---|---|---|---|
| **调整** | B2 build 基线 | snapshot KG-B4 原文 §0.1/§1.2 硬编码 main | 基线从隐含常量升机器可读声明；blocked-handback fork 是 stacked 场景，SOTA 有显式 base 对应物 | P1（簇②） |
| **调整** | B3 TDD 证据入仓 | snapshot KG-B3 `!tests/**/red-green-log/*.log` 锚定错 | bootstrap-kit 模板改路径无关 `!**/red-green-log/*.log` + 加「证据已入 git」机器检查，否则修完仍是约定 | P0（簇④） |
| **新增** | B4 gate 静态强制 | snapshot KG-B4 三处独立证据（backlog/红队/code-reviewer） | `gate: true` task 语义 + 下游 preflight 查 PASS artifact；防 V4 的机器化 | P0（簇①） |
| **新增(契约变更)** | B5 role 分离 | snapshot KG-B5 九轮 review + T003-A2 硬证据 | messages-style（system=指令/user=数据）是唯一结构性解；provider 层支持 role；必须给 T001 迁移路径 | P0 契约/P1 实施（簇③） |
| **调整** | B6 hook 误报 | snapshot KG-B6 三类误报（heredoc/变量拼路径/$()） | 白名单按模式类集中 + 回审纪律；件1 non-overridable 地位不动，动的是误报面；需与 §6.1 协调 | P1（簇④） |
| **新增** | B7 gate 执行语义 | snapshot KG-B7 codex 3 轮同族 bypass | 单次执行/answer-key 一次性/签字不可变三要素进 gate 契约；与 B4 合一个模块，不拆两个半吊子 | P0（簇①） |
| **新增** | worktree 隔离诉求 | snapshot Part1 混线实证 + P2 双方 `-w` SOTA | session-per-idea worktree 规约，复用原生 `-w` 零自建；与 B2 基线声明合簇；warn 型 preflight 起步 | P0 规约/P1 机制（簇②） |

**保留不动**（既有强机制，全簇一致确认）：Safety Floor fail-closed 姿态 · 强 gate（判定逻辑本身）· codex primary 地位 · parallel-builder（保留，只升拓扑假设）。
**Cut 候选**：**无**——七项全部有真实复现证据，无一推演（对齐 forge-verdict-vs-empirical-ship 教训）。

---

## Refactor plan（四模块 = 四簇）

### 模块① · gate 执行语义强制（B4 + B7 · P0）
- **当前问题**：gate 只有判定逻辑无执行语义。B4——PASS 靠 depends_on markdown，「T004 已 merge」≠「operator 签字 PASS」，无机器查验（snapshot KG-B4 code-reviewer 佐证：nothing in shipped code gates action on evaluate_gate return）。B7——answer-key 可复用 + operator 可无限重跑，codex R12-14 三轮同族假 PASS（replay / run_id 泄露 / FAIL-reason 泄露）。
- **目标态**：SHARED-CONTRACT 新章（排在 v7 fork-id §7 邻位）写四条 gate 执行语义**不变量**——(a) gate task 语义（frontmatter `gate: true`）;(b) PASS artifact 存在性机器查验;(c) 已判 run 登记一次性消费（≈ ACME nonce list）;(d) 新 run 作废 stale 签字（≈ GitHub stale approvals）。
- **改造步骤**（顺序）：1. IDS SHARED-CONTRACT 新章定四不变量（契约层，SSOT）;2. XenoDev preflight 落最轻实现——机器可读登记表 + `evaluate_gate` 接进下游 preflight;3. task-decomposer 对 gate task 产 PASS 前置检查。
- **涉及 mirror 件与同步顺序**：SHARED-CONTRACT 是 mirror 件 → IDS SSOT 改 + cp -p 回 XenoDev mirror + 更新 MANIFEST SHA + 跑 mirror-sha 测试;双仓契约 fixture 复用 v7 A4 模式。
- **风险**：登记表并发语义（多 session 判同一 gate 竞态）v0.1 单 operator 不触发（v0.2 note 3）。
- **预估代价**：M（契约章 + preflight 实现，无重型基建）。

### 模块② · 分支拓扑显式化（B2 + operator worktree 诉求 · P0 规约 / P1 机制）
- **当前问题**：并行多线分支拓扑无规约。B2——parallel-builder §0.1/§1.2 硬编码 `git log main` 和 `-b task/... main`，blocked-handback fork 立刻炸 import fail + depends_on 误报。worktree 诉求——IDS 本周 001/006/009 三 idea 20+ commits 混在 forge/009-blueprint 一根分支（混线发生在有规约意识的 operator 身上）。
- **目标态**：session-per-idea worktree 默认命令化（复用原生 `claude -w <idea>`，零自建）+ 命名约定（worktree/分支名 = idea id）+ main 生命周期规约（proposal on main → idea worktree branch → accepted governance artifact 经 human checkpoint 合回 main → branch cleanup）+ build 基线从隐含 main 改机器可读声明（带回流截止条件防长驻）。
- **改造步骤**：1. IDS CLAUDE.md 写 worktree 规约 + main 生命周期（checkpoint 复用既有决策点：handback-review 决议 / stage 定稿 / forge verdict 落地，不新设仪式）;2. XenoDev CLAUDE.md 同构规约;3. warn 型 preflight（mismatch 提示不阻断）;4. outbox/handback frontmatter 加 `current_idea` / `worktree` / `baseline` 三字段（跨仓通道自带拓扑自证）;5. parallel-builder §0.1/§1.2 基线改显式声明消费。
- **涉及 mirror 件与同步顺序**：CLAUDE.md 非 mirror 件（各仓独立），但 parallel-builder 是 XenoDev 自派生 SKILL，改基线消费属授权条目;若 handback schema 触碰 SHARED-CONTRACT §6，走三层同步。
- **风险**：worktree 不隔离 DB/env/运行时资源（SOTA 提醒），XenoDev 两 session 并行跑测试需声明互斥面（v0.2 note 4）;warn 是否足够未经检验（v0.2 note 1 定升级判据）。
- **预估代价**：M（规约为主 + baseline 声明消费机制）。

### 模块③ · LlmClient role 分离（B5 · P0 契约 / P1 实施）
- **当前问题**：`complete(prompt: str)` 单字符串入口结构上无法表达「这是数据不是指令」;codex 九轮 review 证实 string-sanitize 不收敛（单字符 lookalike → 变体标签 → ASCII 转义自败 → Unicode 角括号 → letter-class → 多字符编码），残留「未知编码面」是硬 followup。
- **目标态**：SHARED-CONTRACT / T001 契约章定 messages-style（system=指令 / user=数据）为 **v2 正典**;`complete(prompt)` 降级为 **legacy adapter**（v1 包装 v2，单向依赖）;数据永不进指令通道;allowlist 序列化降级保留为 **defense-in-depth**（SOTA 明言 role 分离亦非 proof，不可删）。
- **改造步骤**（迁移三步，动冻结契约给路径）：1. 契约章定 messages-style v2 正典;2. 新 task 一律强制 v2，`complete(prompt)` 标 legacy adapter;3. 旧消费面（001 项目内 reconstructor/gate/CLI/fake 至少四处）在下一个自然接触点收编（不专开迁移 task，防过度工程）;兼容测试覆盖 v1/v2 同语料双跑。
- **涉及 mirror 件与同步顺序**：T001 契约若在 bootstrap-kit 模板扩散，迁移 = 契约版本化（v1/v2 并存过渡）非一次性替换;LlmClient Protocol 若为 mirror 件走三层同步。
- **风险**：迁移爆炸半径取决于 bootstrap-kit 模板是否内嵌 `complete(prompt)` 形状（P1-Opus §3.2 未定，落地前需 grep 消费面）;旧消费面三个月后仍残留则 v0.2 裁专开收编 task（v0.2 note 2）。
- **预估代价**：M（契约版本化 + 兼容测试 + 渐进收编，非一次性爆改）。

### 模块④ · 证据与 hook 治理（B3 + B6 · P0 gitignore / P1 白名单）
- **当前问题**：B3——red-green-log 豁免 `!tests/**/red-green-log/*.log` 锚定仓根 tests/，但 XenoDev 项目在 `projects/<feature>/tests/`，豁免失效，`*.log` 兜底吞掉，T001.log 从未入 git（静默失效两 task）。B6——credential hook 对 heredoc/变量拼路径/$() 误报 fail-closed，与 parallel-builder §6.1 明写 mktemp 范式直接冲突，每个 ship 都可能撞。
- **目标态**：B3——bootstrap-kit gitignore 模板改路径无关 `!**/red-green-log/*.log` + 加「证据已入 git」机器检查（否则修完 pattern 仍是约定）。B6——白名单按**模式类**集中收敛（heredoc-commit-message 类 / mktemp 类 / 变量路径类），非撞一次加一条;定期回审入纪律（每行白名单是待回审承诺）;fail-closed 姿态 + 件1 non-overridable 地位不动;与 §6.1 协调（SKILL 与 hook 二者必改其一）。
- **改造步骤**：1. bootstrap-kit gitignore 模板改豁免 pattern（P0，止血）;2. 加证据入仓机器检查（parallel-builder §4.4 收口查 git ls-files）;3. hook 白名单按模式类实装 + 回审纪律进治理规则;4. §6.1 与 hook 冲突协调（固定 scratchpad 路径 或 hook 放行 mktemp）。
- **涉及 mirror 件与同步顺序**：bootstrap-kit gitignore 模板改动是模板层;credential-isolation hook 是 Safety Floor 件1（non-overridable），改误报面走 IDS 三层同步。
- **风险**：白名单逐例累加会重演 KG-B1「逐例放宽」路径病——必须按模式类收 + 回审（P2-Opus §3 修正3 明确升格为治理规则）。
- **预估代价**：S（gitignore 一行修 + 白名单模式类整理 + 一条治理规则）。

---

## Next-version dev plan（双仓分道 · P0/P1/P2）

### IDS 侧落地项（治理仓 · 契约/规约层）
- **P0** · SHARED-CONTRACT gate 执行语义新章（四不变量，排 fork-id §7 邻位）— 簇①
- **P0** · worktree 规约 + main 生命周期进 IDS CLAUDE.md（checkpoint 复用既有决策点）— 簇②
- **P0** · bootstrap-kit gitignore 模板改路径无关豁免 — 簇④
- **P1** · hook 白名单治理规则（模式类收敛 + 回审）进治理层 — 簇④
- **P1** · LlmClient messages-style v2 契约章 + legacy adapter 定义（若在 SHARED-CONTRACT/bootstrap-kit 扩散）— 簇③
- **硬约束**：所有 mirror 件改动 = SSOT 侧改 + cp -p 回 mirror + MANIFEST SHA 更新 + mirror-sha 测试;双仓契约 fixture 复用 v7 A4 模式

### XenoDev 侧授权条目（build runtime · 不当场改框架，经 hand-off/backlog 授权）
- **P0** · preflight 登记表实现 + `evaluate_gate` 接进下游 preflight — 簇①
- **P0** · warn 型 worktree preflight + outbox/handback frontmatter 加拓扑三字段 — 簇②
- **P0** · 项目内 gitignore 豁免已修，框架模板改后随 bootstrap 生效 + 证据入仓机器检查 — 簇④
- **P1** · LlmClient v2 + legacy adapter 实装 + 兼容测试（v1/v2 同语料双跑）— 簇③
- **P1** · parallel-builder §0.1/§1.2 基线改机器可读声明消费 — 簇②
- **P1** · B6 hook 白名单按模式类实装 + §6.1 冲突协调 — 簇④

### P2 · v0.2 note（观察位 · 真实复发后升级，不预先建）
- warn preflight 后若 mismatch 混线复发 ≥2 次 → 升 commit-time block（判据数据来自真跑）
- B5 v1 直接消费面三个月后仍残留 → 裁是否专开收编 task
- gate 登记表并发：多 session 判同一 gate 竞态，v0.1 单 operator 不触发，真冲突后再加原子写/锁
- worktree 运行时资源互斥：DB/env/端口不隔离，第一次资源冲突后再规约互斥声明

---

## What this menu underweights（强制自批判）

- **⚠ 双模型回声室风险（本轮高于 v7，需重点点名）**：本轮双方**从 P1 起就高度同向**——P3R1-GPT §1 原话「双方 P1/P2 已高度收敛」，Opus P3R1 §1「四份 round file 诊断层完全一致」。四条分歧全落在**落地形状**（校验轻重/迁移粒度/main 角色/切分线），**没有一条是方向之争**。这意味着若「七项应 incremental optimize 不 redesign」这个大前提本身有盲区，两模型不会互相纠错。**具体未被任一方质疑的共识判断**：(a)「零 cut」——七项全保留，但没有任一方追问「B3/B6 这类纪律摩擦是否值得进 forge 而非项目内直接修」;(b)「worktree 复用原生 `-w` 就够」——双方都停在规约层，无人压测「多 idea worktree + 运行时资源共享」在 XenoDev 真跑时是否够用。**建议**：落地前对簇②③在 XenoDev 真跑一轮，用实证兜 forge 推演盲区（对齐 forge-verdict-vs-empirical-ship 教训——理论决议会漏 DB 引擎语义/并发/原子性，build-time 复现是最后防线）。
- **反对/修正证据的整合**：Evidence map 标 ⚠ 的四条——B5 判级（GPT P1 refactor → P2 自改 new）、worktree 校验轻重（Opus 让步撤回轻 hook）、gate 切分线（Opus「强制点轻」被误读，R2 澄清）、B5 反对——**均在 R2 收敛且让步方给了明确理由**，非强行压平。主 verdict 仍坚持是因四条都指向「实现轻但语义/契约不降级」的一致原则。
- **Y 视角覆盖**：三视角（架构/纪律/UX）齐全，无泄漏 out-of-scope。但**安全深度**——B5/B7 是 AI-security 议题，本轮按「架构设计」视角处理（role 分离作结构隔离），未单开安全红队视角对 messages-style **落地后**是否引入新注入面做审查（SOTA 明言 role 分离亦非 proof）。allowlist 保留为 defense-in-depth 是对冲，但 v2 上线后应补一轮注入回归。
- **K 中未充分回应的项**：K 硬约束「mirror 件三层同步」——本文档四模块**逐簇标了涉及哪些 mirror 件 + 同步顺序**（回应了 v7 underweight 与 P3R1 §4 的 ⚠），但**同步的具体 SHA/顺序清单未逐条列到 commit 级**（这是落地 brief 的活，不是 stage 文档职责）。选 [A]/[B] 时需在 AUTHORIZATION-BRIEF 里补齐。
- **X 标的覆盖局限**：XenoDev `dogfood-backlog.md` 外部原文 Codex 沙箱可能 BLOCK，本轮以 `_x-batch-snapshot.md` 权威快照为准（自足）。若快照与外部原文有漂移（快照摘于 @ cc4edeb），verdict 可能偏。落地前建议 operator 在 XenoDev 侧 `rg` 核对 KG-B 段落无新增变体。
- **forge versioning 提示（触发 v9 的新信息）**：(a) warn preflight 真跑后 mismatch 仍复发 → 需裁 hook block 形状;(b) B5 v2 上线后出现 role 分离**也**挡不住的新注入面 → role 分离方向本身要重估;(c) gate 登记表在多 session 真出并发竞态 → 需补并发语义设计;(d) worktree 运行时资源冲突真实发生 → 互斥声明规约化。这四项恰是 §"v0.2 note" 的观察位，任一触发即 v9 料。

## Decision menu（for human）

### [A] 接受 verdict 全落（四簇 P0/P1 一并落地）
```
按 §"Refactor plan" 四模块 + §"Next-version dev plan" 双仓分道落地：
1. IDS 侧先落契约/规约层（SHARED-CONTRACT gate 章 + worktree 规约 + gitignore 模板）
2. mirror 件三层同步（SSOT 改 + cp -p + MANIFEST SHA + mirror-sha 测试）
3. 产 AUTHORIZATION-BRIEF-v8.md（授权条目全文 + 落地顺序 + 逐条双仓 commit SHA 位）
4. XenoDev 侧经 hand-off/backlog 消费授权条目（不当场改框架）
```
⚠ 框架级变更只走本 forge 决议后落地，不在 XenoDev 当场另改（K5 硬约束）。
⚠ 簇①③④ 触碰 mirror 件（SHARED-CONTRACT / bootstrap-kit / Safety Floor 件1）· 必须 IDS 三层同步。
⚠ 本轮**未产 next-PRD**（W 未勾）——本 verdict 是框架加固非产品 idea，不进 L4 plan-start。

### [B] 局部先落 P0（止血核心优先 · 延续 v7 D1 先例）
```
最小止血集（先落这些 P0）：
  - 簇① SHARED-CONTRACT gate 执行语义章 + XenoDev preflight 登记表（防 V4 机器化，最高优先）
  - 簇② worktree 规约 + main 生命周期进双仓 CLAUDE.md + warn preflight（拓扑显式化止血）
  - 簇④ bootstrap-kit gitignore 模板修（B3 证据入仓止血，一行改）
  P1 项（簇③ B5 v2 契约实施、簇② baseline 机制、簇④ B6 白名单治理）后续批次
```
适用：gate 强制与拓扑混线是当前最痛点，B5 契约变更代价大可缓一拍;对齐 operator「止血核心优先、防过度工程」。

### [C] 局部接受
- ✅ 采纳：<operator 勾选四簇中哪几簇>
- ⏸ 挂起：<等什么条件再决定，如 B5 迁移等 bootstrap-kit 消费面 grep 清点后>
- ❌ 拒绝：<理由>

### [P] Park
```
/park 006
```
保留所有 v8 forge 产物，标记暂停。复活时不重做本层收敛。

### [Z] Abandon
不适用——本轮是框架加固（非产品 idea 存废判断），无 abandon 语义。七项是已 ship 框架的可靠性债 / 跨仓协议债 / operator 工作流债，只有「修 / 缓修」，无「放弃这个 idea」。

---

## Forge log
- v8: 2026-07-13 — verdict: "incremental optimize，不 redesign，零 cut。七项 dogfood 缺口 + worktree 诉求收敛四簇:①gate 执行语义(B4+B7)进 SHARED-CONTRACT 新章四不变量 + XenoDev 登记表 preflight;②分支拓扑显式化(B2+worktree)复用原生 `-w` 零自建 + main 生命周期 + baseline 机器声明 + warn preflight;③LlmClient role 分离(B5)messages-style v2 + legacy adapter + 兼容测试;④证据与 hook 治理(B3+B6)gitignore 路径无关豁免 + 证据入仓检查 + 白名单模式类收敛拒逐例加白。强 gate/Safety Floor/codex primary 不动;四簇均有 SOTA 对应物无发明新轮子"
- v7: 2026-07-08 — verdict: "review gate 单点依赖 = 同根 5 失效切面;codex 保 primary + review 通道状态机(circuit breaker 四要素);KG-B1 拒第三次逐例放宽 regex,fork-id 语法进 SHARED-CONTRACT 作 SSOT + FULL 兼容 001-radar-pA + 双仓 fixture 契约测试"
- v6: 2026-07-02 — verdict: "5 条同根 = mac 环境形态硬编码成 constant;按 6 类性质分层外置 + 防漂移守卫"
- v5: 并发安全 · CONCERNS(KG-1 approve-over-approve / KG-2 同秒碰撞 · 已 ship 留 dogfood 观测)
- v4: hand-back/mirror 机制固化(攒批真问题再 forge 模式)
- v3/v2/v1: XenoDev 跨仓分工 + build runtime 边界确立(forge v2 = IDS 治理 · XenoDev 唯一 L4 build runtime)
