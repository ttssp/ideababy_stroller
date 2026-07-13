# Forge 006 v8 · Phase 2 · Opus 4.7 Max 参照系评估

**Written**: 2026-07-13T12:05:00Z
**Searches run**: 5(worktree 隔离 / role 分离 / 单次执行防重放 / secret-hook 误报治理 / 非 main 基线)
**读入**: P1-GPT55xHigh.md(对方)+ 自己 P1 refresh + forge-config refresh;moderator-notes 不存在

## §1 · SOTA 对标

| 议题 | SOTA 形状 | 对本批的含义 |
|---|---|---|
| worktree 隔离(operator 诉求) | **Claude Code 原生 `-w/--worktree` flag**:自动建分支 + `.claude/worktrees/<name>/` 目录 + session 整体 scope 到该目录([官方文档](https://code.claude.com/docs/en/worktrees));社区共识:2-3 并行 session 是可持续上限、任务须触碰不同文件、merge 后立即清 worktree、**worktree 不隔离 DB/env/运行服务**([MindStudio](https://www.mindstudio.ai/blog/claude-code-git-worktree-parallel-branches)、[Dan Does Code](https://www.dandoescode.com/blog/parallel-vibe-coding-with-git-worktrees)) | 「命令支持」档**原生已有,无需自建**——方案收窄为:规约(session 起手即 `-w` 或显式 worktree)+ 命名约定(worktree 名 = idea id)+ 清理纪律 + 运行时资源共享注意事项。过度工程风险显著下降 |
| B5 role 分离 | role-tagging(ChatML/Harmony)是「trusted 指令 vs untrusted 数据」**最接近结构性边界的现有物**;best practice:parameterized prompts、user 文本永不拼进指令、tool/检索输出一律 untrusted channel([Oligo](https://www.oligo.security/academy/prompt-injection-impact-attack-anatomy-prevention)、[Vectra](https://www.vectra.ai/topics/prompt-injection));研究前沿(Meta SecAlign、Prompt CFI)全押 channel separation | B5 的 messages-style 方向被强背书,是**采用标准形状而非发明**;同时 SOTA 明言 role 分离也非 proof(模型层仍可被骗)——B5 修完 allowlist 序列化仍应保留为 defense-in-depth,不是可删项 |
| B7 单次执行 | ACME 协议:server 维护**已签发 nonce 列表,一次性消费**;OAuth nonce 绑定单次登录;GitHub branch protection「**新 commit 到达即作废 stale approvals**」([ACME](https://ietf-wg-acme.github.io/acme/reconciliation/draft-ietf-acme-acme.html)、[Auth0](https://auth0.com/blog/demystifying-oauth-security-state-vs-nonce-vs-pkce/)) | B7 三要素(单次执行/answer-key 一次性/签字失效)在业界各有直接对应物,**组合现成模式即可**;强制点可以很轻——「已判 run 登记表」一个机器可读文件 ≈ ACME nonce list,不需要重型基建 |
| B6 hook 误报 | gitleaks 治理三原则:**集中可审计 allowlist**(拒绝 inline 散布)、**每行白名单是一个待定期回审的承诺**(防 dumping ground)、**hook + CI 双网**(hook 可被绕过,CI 兜底)([DevOps Daily](https://devops-daily.com/posts/pre-commit-hooks-security-guide)、[OneUptime](https://oneuptime.com/blog/post/2026-01-25-secret-scanning-gitleaks/view)) | B6 修法形状:白名单集中 + 回审纪律 + fail-closed 姿态不动;⚠ 「逐例加白」与 KG-29→KG-B1 的「逐例放宽 regex」是同构风险,白名单必须按**模式类**收(heredoc-commit-message 类/mktemp 类),不按撞一次加一条 |
| B2 非 main 基线 | stacked-branch 模式:底层 PR 指 main、上层以下层为 base;CI 基线 = **显式声明的 git hash/tag**,「baseline 之后的 delta」为评估对象([SmartScope gh-stack](https://smartscope.blog/en/blog/gh-stack-multi-agent-branch-strategy/)、[AutoRABIT](https://knowledgebase.autorabit.com/product-guides/arm/troubleshoot/best-practices/branching-strategy-and-ci-cd-pipeline)) | 「基线显式声明」有直接 SOTA 形状;blocked-handback fork 本质就是 stacked 场景。反面提醒:feature 分支长驻会失去与其他并行分支的集成反馈——**基线声明应带「回流截止条件」**,不鼓励长驻 |

## §2 · 用户外部材料消化

K 未给额外链接;无。

## §3 · 修正后的视角

**站住的**:三个结构性缺口诊断、七项 first-take 评分(含零 cut)全部维持;与 GPT P1 的诊断层几乎完全重合(它的「隐含拓扑/隐含 gate 执行语义太多」= 我的缺口 a+b)。

**修正 1(P1 §3.1 部分解除)**:worktree 强制层级三档中我原以为「命令支持」是需要自建的中成本档——错,Claude Code 原生 `-w` 已给。问题收窄为纯规约设计:何时起 worktree(idea 级 session 起手)、命名(= idea id)、main 只留 proposal 期、清理时机、以及 SOTA 两条注意事项(2-3 session 上限;worktree 不隔离运行时资源——XenoDev 跑测试/DB 时两 session 并行要显式声明互斥面)。剩余不确定只有一条:要不要加轻量 hook 校验「所改 discussion/NNN 与 worktree/分支名匹配」——留 P3 与对方裁。

**修正 2(回应 GPT P1 §3.2)**:「防误操作 vs 防有动机作弊要不要同一套约束」——SOTA 显示同一套机制(nonce 登记/一次性/stale 作废)同时覆盖两者,且实现代价是文件级不是系统级;**不必为 v0.1 弱化威胁模型**,但强制点选最轻实现(已判 run 登记表 + preflight 查表)。

**修正 3(P1 未见的风险)**:B6 白名单若逐例累加,会重演 KG-B1「逐例放宽」路径病;必须按模式类收敛 + 定期回审入纪律。这条把 B6 从「工程摩擦小修」升格为「需要一条治理规则」。
