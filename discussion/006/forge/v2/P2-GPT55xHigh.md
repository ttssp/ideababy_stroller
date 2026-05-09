# Forge v2 · 006 · P2 · GPT55xHigh · 参照系评估(with search)

**Timestamp**: 2026-05-09T12:53:13Z
**Searches run**: 8, SOTA-benchmark search only.
**Visibility**: 我已读对方 P1。

## 1. SOTA 对标

| 标的 X' | 参照项 | 它怎么做 | 我们怎么做 | gap | URL/Source |
|---|---|---|---|---|---|
| IDS / ADP-next 的 skill 层 | Claude Code Skills + Claude Agent SDK | 官方 skills 已把 commands 合并进 skill,支持个人/项目/plugin 三级、惰性加载、supporting files、invocation control;Agent SDK 提供 hooks、permissions、checkpointing、observability 等生产 agent 能力。未发现"Claude Skills SDK v2"作为独立正式名;官方现状更像"Agent SDK + Skills open standard"。 | IDS/ADP 已有 SKILL.md,但事实 SSOT 与 process skill 混在一起,V4 skill 多为历史 port。 | P1 的"V4 Component 不作起点"站住;但 XenoDev 不能只写 markdown skill,还要把 permissions/hooks/observability 纳入运行时框架。 | https://code.claude.com/docs/en/skills ; https://code.claude.com/docs/en/agent-sdk/overview |
| 跨仓与并行 build | Cursor 3.2 Multitask / Worktrees / Multi-root | Cursor 2026-04-24 官方 changelog 把 async subagents、worktrees、multi-root workspace 合在一个 agent window 中;单 session 可面向多 folder workspace 做跨 repo change。 | IDS v1.1 hand-off 用 operator 切仓 + mini-PRD;007a-pA 暴露 `working_repo` emergent 字段。 | P1 "改变物理位置让 working_repo 消失"需要修正:跨仓不是异常,而应成为一等 workspace/hand-back 模型。 | https://cursor.com/changelog/04-24-26 |
| PRD/spec/tasks 流程 | GitHub Spec Kit | 官方 repo 当前 latest release 显示 0.8.7(2026-05-07),未发现"v2"正式版;但它明确把 spec 置于中心,使用 `/speckit.constitution`、`/speckit.specify`,并强调先写 what/why 而非 tech stack。 | IDS 产 PRD,ADP/V4 产 7 元素 spec;当前 v1.1 的 IDS spec 与 ADP spec 双写冲突。 | SOTA 支持"spec 是可执行工件",但不支持 IDS 与 XenoDev 各写一份 build spec。单一 build spec 应归 XenoDev。 | https://github.com/github/spec-kit |
| agentic coding 失败研究 | MSR 2026 agentic PR studies | MSR 2026 有大量 agent-authored PR 研究,包括 33k agent PR 失败研究、被 revert 的 AI changes、测试失败、安全问题、可读性/理解性等。 | V4 有 reviewed-by 和 PPV,但无 Eval Score / risk tier;Safety Floor 仍缺凭据隔离和备份破坏检测。 | P1 的工程纪律 refactor 站住:仅靠 prompt/skill 不足,必须有统计反馈、测试失败归因、review/hand-back 数据。 | https://2026.msrconf.org/details/msr-2026-mining-challenge/19/Where-Do-AI-Coding-Agents-Fail-An-Empirical-Study-of-Failed-Agentic-Pull-Requests-in |
| 前沿 coding agent 能力 | GPT-5.4 / Codex | OpenAI 2026-03 发布称 GPT-5.4 进入 Codex,在 coding、tool use、computer use 上增强,并强调长任务中工具迭代和更少人工干预。 | K1 追求"可靠且自动化程度最高";本仓仍处在协议/文档层,运行时 agent harness 未生。 | 目标方向没错,但 gap 是 harness 产品化,不是再补一份流程文档。 | https://openai.com/index/introducing-gpt-5-4/ |

## 2. 用户外部材料消化

- **Binding 1: V4 仅参考,XenoDev 是 ADP-next** → SOTA 验证。Claude Skills 与 Agent SDK 的分层说明,以及 Spec Kit 的 extension/preset/override 机制,都支持"保留 lesson/pattern,重建运行时产品"。V4 不应被补丁式吸收。
- **Binding 2: §9 四 drift 优先** → SOTA 验证并加重。Cursor multi-root 证明跨仓 build 可做成一等能力;这反过来说明 DRIFT-4 的 `working_repo` 不是噪音,而是 schema 未显式建模的信号。
- **Binding 3: SHARED-CONTRACT v2.0 双向 hand-off** → SOTA 验证。MSR 2026 failure corpus显示 agent PR 会在测试、安全、可读性、revert 等环节失败;没有 hand-back,IDS 无法学习哪些 PRD 约束导致 build 失败。
- **Binding 4: forge 元层锁决定** → SOTA 间接验证。主流工具在增强 autonomous run,这会放大"想法变了静默停"的损害;重大转向必须保留跨模型审阅。
- **Binding 5: v2 后不重走 L1-L3,直接 B1+B2** → SOTA 支持。Spec Kit/Claude/Cursor 的重点都在把已定意图转为 spec/build/run,不是重复 upstream ideation。

## 3. 修正后的视角

- P1 判断"新建 XenoDev,不继承 V4" → **站住**。SOTA 的共同点是运行时 harness 与 workflow 绑定;V4 是历史 workflow,不是当前目标 runtime。
- P1 判断"工程纪律 refactor" → **站住并加重**。MSR 2026 failure cases 要求 XenoDev 有 Eval/risk/hand-back,不能只 port reviewed-by hook。
- P1 判断"`working_repo` 也许应通过物理位置改变而消失" → **被修正**。Cursor multi-root 表明跨 repo 是 SOTA 能力;正确方向是显式 workspace/schema,不是假装单仓。
- P1 判断"Safety Floor 先于统计层" → **部分站住**。凭据隔离/备份检测是 hard floor;但 failure corpus 说明 Eval Score 不能长期后置,至少要在 v0.1 留数据接口。
- 与 Opus P1 对齐点:Opus 主张 6 个 ADP 模块 L/P 多数保留,C 层选择性 cp;我仍同意。但 `sdd-workflow/task-decomposer` 是否 C 级直接继承,应由 XenoDev schema 决定,不能因"port-from-IDS"自动保留。
