# Forge v8 · 006 · P1 · GPT55xHigh · 独立审阅(no search)

**Timestamp**: 2026-07-13T19:38:53+08:00
**Searches used**: NONE in this round.
**Visibility**: I did NOT read other reviewer's P1.
**Reviewer stance**: 审阅人 — 评判已存在物,不是 daydream。

## 0. 我读到的标的清单 + 阅读策略

- 我读了:`discussion/006/forge/v8/forge-config.md` 全文,拿到 X/Y/Z/W/K、strong-converge、七项批次和同源簇提示。
- 我读了:`discussion/006/forge/v8/_x-batch-snapshot.md` 全文,作为权威快照:operator worktree 原话、IDS 混线实证、KG-B2..B7 原文、v7 回填、XenoDev 工作流摘录。
- 我核对了:`/home/ys/codes/XenoDev/dogfood-backlog.md`,只用 `rg` 定位 KG-B2..B7 段落行号,未整读外部长文件。
- 我读了:`discussion/006/forge/v7/stage-forge-006-v7.md` 的 Verdict / Decision matrix / What this menu underweights 三节。
- 我读了:`CLAUDE.md` 的 4-layer pipeline、XenoDev 跨仓、Codex bus、Directory ownership;读了 `/home/ys/codes/XenoDev/CLAUDE.md` 的工作流、跨仓引用、dogfood 铁律、切回矩阵;读了 `.claude/skills/forge-protocol/SKILL.md` 和 `AGENTS.md`。
- 我跳过的:`discussion/006/forge/v8/moderator-notes.md` 不存在;`discussion/006/forge/v8/P1-Opus47Max.md` 按 parallel independence 禁读;proposal §006 不另读,因 K 首四段已内嵌。

**K(用户判准)摘要**:用户要的是“可靠的、自动化程度最高”的 Claude Code framework/pipeline,但本轮不重开 006 大方向,只审 XenoDev dogfood-backlog 六条框架缺口 + operator worktree 隔离诉求。K 尾段明确要求七项不漏,尊重 KG-B5/B7 这类“攒够硬证据才动契约”的权重,同时延续 v7 “可靠、可落地、不过度工程”的止血核心原则。

**我的阅读策略**:按 Y 三视角分层看:架构设计看拓扑、契约、gate 执行语义;工程纪律看证据是否能入仓、hook 是否与 SKILL 自洽、mirror/契约纪律是否保持;用户体验看单人多 idea/多仓/session 切换的心智负担和高频误报。

## 1. 现状摘要(按 Y 视角组织)

### 架构设计

当前最清晰的结构性问题是“隐含拓扑”太多。KG-B2 说明 parallel-builder 把 main 当永远集成基线,但 blocked-handback 会把代码滞留在 feature 分支;operator 新诉求说明 IDS 侧 session/idea/worktree 也没有显式绑定,001/006/009 已混在同一命名分支历史里。两者不是独立偏好,而是并行多 idea/多 fork 的分支拓扑没有成为框架对象。

第二个结构问题是 gate 还没有稳定的执行语义。KG-B4 的 PASS 只靠 depends_on markdown 和程序纪律,KG-B7 的盲测 gate 即使项目内补了 run 绑定、nonce、FAIL reason 泛化,仍暴露“人在环 + 机器对答案”缺少单次执行约束。KG-B5 则是接口契约层问题:LlmClient 只有 `complete(prompt: str)`,不可信数据只能靠字符串边界和 sanitizer 混在同一通道里。

### 工程纪律

现有纪律并不弱:AGENTS.md 和 CLAUDE.md 都强调 Safety Floor、TDD、pre-merge review、forge 回流、XenoDev 不当场改框架;v7 也刚用契约 SSOT + mirror SHA 更新约束处理 fork-id 漂移。但 KG-B3 暴露 red-green-log 证据被 `.gitignore` 吞掉,导致“测试先红再绿”可能只在临时 worktree 文件系统里存在。KG-B6 暴露 credential-isolation hook fail-closed 与 parallel-builder 明写的 heredoc/变量路径/mktemp 范式冲突,纪律本身开始制造高频摩擦。

### 用户体验

operator 的 worktree 诉求本质不是“想多开分支”,而是想把单人多线操作的上下文隔离做成默认 ergonomics。现状中队列已按 idea 隔离,但 git 分支/worktree/session 没有跟上,所以操作者仍要靠记忆避免 001/006/009 混线。KG-B6 的 hook 误报同样是 UX 问题:安全姿态正确,但合法高频路径反复被挡,会诱导临场绕法和注意力损耗,削弱“几乎没有人工干预”的目标。

## 2. First-take 评分(七项批次逐项)

| 批次 | 倾向 | 理由 |
|---|---|---|
| KG-B2 | refactor | main-only 集成基线假设已被 blocked-handback 事实打破;应保留 parallel-builder,但把“基线”从隐含常量升为显式语义。 |
| KG-B3 | refactor | TDD 证据入仓是正确纪律,问题是路径锚定错;这不是新机制,是模板和项目布局需要对齐。 |
| KG-B4 | new | gate PASS artifact 的机器强制目前不存在;仅靠 depends_on/markdown 不能承载防 V4 的 STOP 语义。 |
| KG-B5 | refactor | 9 轮 review 已证明 sanitizer 不收敛;根治点在冻结接口契约,不是继续补字符串规则。因涉及 T001 兼容,应判 refactor 而非临时新增工具。 |
| KG-B6 | refactor | Safety Floor fail-closed 要 keep,但 hook 与 parallel-builder 范式冲突必须调和;不能靠每次手动绕过积累隐性流程债。 |
| KG-B7 | new | 盲测 gate 的单次执行/不可重放语义是缺失的框架不变量;项目内封泄露面只能降风险,不能定义执行边界。 |
| operator worktree 隔离诉求 | new | IDS 已有 queue-per-idea,但缺 session/worktree/branch-per-idea 规约;这是 KG-B2 同源的拓扑层新增对象,不应只写成个人习惯。 |

## 3. 我现在最不确定的 3 件事

1. B2 + operator worktree 的最小落点在哪里:只改 CLAUDE/AGENTS 的运行纪律是否足够,还是必须进入 SHARED-CONTRACT / 命令层才算可靠。
2. B4 + B7 的 gate 执行语义应强到什么程度:solo operator v0.1 下“防误操作”与“防有动机作弊”是否要同一套约束。
3. B5 的契约迁移边界:冻结的 `LlmClient` 接口要改,但哪些既有 task/client 必须兼容、哪些可以一次性迁移,需要后续阶段更硬的证据。
