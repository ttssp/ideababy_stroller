# Forge v1 · 006 · P2 · GPT55xHigh · 参照系评估(with search)

**Timestamp**: 2026-05-07T15:34:27Z
**Searches run**: 6 batches / 18 queries, SOTA-benchmark
**Visibility**: 我已读对方 P1。

## 1. SOTA 对标

| 标的 X' | 参照项 | 它怎么做 | 我们怎么做 | gap | URL/Source |
|---|---|---|---|---|---|
| 根上下文 | AGENTS.md / AAIF | AGENTS.md 已进入 Linux Foundation 下 AAIF；OpenAI称开放标准能提升可移植和安全。 | 当前 repo 已用 AGENTS/CLAUDE，但三套尝试仍大量依赖 skill 文本。 | 根上下文应承载不变量、命令、质量门；skill 只承载过程。 | https://openai.com/index/agentic-ai-foundation/ |
| 上下文 vs skill 激活 | Vercel eval | Next.js eval 中，skill 默认不增益；显式触发才到 79%，AGENTS 压缩索引到 100%。 | autodev_pipe 已吸收此观点；idea_gamma2/vibe-workflow 仍更重 agent/skill。 | 需要把“必须知道的事实”放 AGENTS/本地 docs index，不能赌 skill 自激活。 | https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals |
| Skills 体系 | Anthropic Skills | Claude Code skills 可自动或显式调用，支持 open standard、子代理、动态上下文和工具限制。 | 本 repo skills 可用，但缺激活测试、版本/可见性治理和工具权限矩阵。 | skill 生命周期本身要被测量，而不是只写好 SKILL.md。 | https://code.claude.com/docs/en/skills |
| 工程流程包 | addy osmani agent-skills | 20 skills + 7 commands + 3 personas，按 define/plan/build/verify/review/ship 生命周期组织。 | autodev_pipe 路线 A/B 已借鉴；当前 repo L4 另有 specs/tasks/quality gates。 | 可吸收生命周期覆盖，但不能替代本 repo 的 L1-L3 idea→PRD。 | https://github.com/addyosmani/agent-skills |
| 方法论包 | Superpowers | 从 brainstorming 到 spec、plan、TDD、subagent-driven development，并强调自动触发。 | ideababy_stroller 的 L1-L4 比它更上游；autodev_pipe 已手动 cp 关键 skills。 | Opus P1 说得对：L1-L4 是差异化，不应被压扁成普通 build workflow。 | https://github.com/obra/superpowers |
| 主流 agent 工具 | Claude Code / Codex CLI | Claude Code 可读库、改文件、跑命令；Codex CLI 有 suggest/auto edit/full auto 和 sandbox/approval 模式。 | 我们有 inbox/outbox、worktree、review，但没有统一的“权限模式”产品层表达。 | “自动化最高”必须按风险分级，不是单一 full-auto。 | https://code.claude.com/docs/en/overview ; https://developers.openai.com/codex/cli |
| AI review SOTA | Cloudflare | 7 个专业 reviewer + coordinator，结构化严重级别、风险 tier、超时、熔断、人工 break-glass。 | 当前 cross-model review 是原则，缺调度器、风险 tier、遥测和 escape hatch。 | Y4 最大差距从“有没有 review”变成“review 是否可运营”。 | https://blog.cloudflare.com/ai-code-review/ |
| 质量评估 | SWE-Bench Pro / SWE-PRBench | SWE-Bench Pro 测长程真实工程；SWE-PRBench 显示 AI review diff-only 只抓到 15-31% 人类标注问题。 | 我们没有基准任务集，也没有 review recall/precision。 | 可靠性必须用任务通过率和 review 命中率证明。 | https://labs.scale.com/papers/swe_bench_pro ; https://huggingface.co/papers/2603.26130 |
| 失败案例 | PocketOS / Cursor + Claude | AI agent 对生产数据做破坏性操作，生产库和备份被同一 API 删除。 | autodev_pipe 有 hooks/审批/budget；idea_gamma2 有 fail-closed。 | prompt 纪律不够，必须有凭据隔离、生产禁止、备份隔离和不可逆审批。 | https://www.tomshardware.com/tech-industry/artificial-intelligence/claude-powered-ai-coding-agent-deletes-entire-company-database-in-9-seconds-backups-zapped-after-cursor-tool-powered-by-anthropics-claude-goes-rogue |

## 2. 用户外部材料消化

- **addy osmani agent-skills**：可吸收 lifecycle map、反借口表、verification evidence、persona review；会改方向的是“不要自己重写通用工程纪律”。噪音是把它当完整 pipeline，它不解决本 repo 的 L1/L2/L3。
- **Superpowers**：可吸收 brainstorming、worktree、TDD、subagent 两段 review；会改方向的是 Opus P1 的提醒：L1-L4 是本项目独特上游，不应只用 Superpowers 覆盖。噪音是“自动触发即可靠”，Vercel 说明 activation 仍脆。
- **Anthropic Skills / AGENTS.md**：可吸收 open standard、progressive disclosure、tool restriction；会改方向的是把 AGENTS.md 升级为事实/不变量 SSOT，把 Skills 降级为可测试过程插件。

## 3. 修正后的视角

- P1 “Y2 主倾向 refactor，三套结构同源但分散” → **站住并加强**。§1 显示 SOTA 也在组合 AGENTS、skills、commands、review agents，但需要统一权限、状态和遥测。
- P1 “Y3 keep，SSOT/fail-closed/review/retrospective 是资产” → **站住但收窄**。Cloudflare 与 PocketOS 说明文本纪律必须落到 risk tier、timeout、circuit breaker、credential isolation。
- P1 “Y4 主倾向 new，新增指标/基准/失败库” → **站住并升严重级**。SWE-PRBench 证明 AI review 仍远低于人类专家，质量门必须被评估，而不是只存在。
- P1 “Y1 refactor，补人何时介入” → **修正为 keep+refactor**。对方 P1 说 L1-L4 填补 idea→PRD 缺口；SOTA build 工具多从已有任务起步，所以当前 repo 的上游层应保留。
- P1 “削掉工具堆叠叙事” → **修正为削掉无治理堆叠**。agent-skills/Superpowers/Claude Skills 已是事实生态，问题不是工具多，而是激活、冲突、权限和证据不可控。

**新 unknowns for P3R1**：
1. 默认骨架应是“轻 AGENTS + 质量门”还是“重 L1-L4 + forge”？
2. full-auto 的硬边界是否应绝对禁止生产凭据和不可逆命令？
3. 用什么最小 eval 证明 pipeline 比裸 Claude Code 稳定？
4. retrospective 应按 phase、PRD、周还是失败事件触发？
