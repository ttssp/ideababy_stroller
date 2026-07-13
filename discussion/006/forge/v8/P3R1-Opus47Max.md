# Forge 006 v8 · Phase 3R1 · Opus 4.7 Max 联合收敛 R1

**Written**: 2026-07-13T12:20:00Z
**Constraints honored**: no new search · 已读双方 P1+P2 全部四份 · moderator-notes 不存在

## §1 · 整合摘要

四份 round file 诊断层完全一致:七项批次 = 三个结构性缺口(隐含分支拓扑 / gate 缺执行语义 / 信任边界缺结构隔离)+ 两类纪律摩擦(证据入仓 / hook 误报)。P2 双方检索撞到同一组 SOTA 且方向互证:Claude Code 原生 `-w` flag(双方独立核实,GPT 还跑了本机 `claude --help` 实证)、role/authority 分离(OpenAI Model Spec + OWASP LLM01)、nonce 一次性消费 + stale 作废(ACME/AP2/GitHub approvals)、secret-scanning 集中 baseline/audit 治理、显式 base branch。P1 的三个标签分歧(B5 判级、worktree 层级、B4/B7 强度)经 P2 全部自然收敛:B5 → new(契约变更)+ 保留迁移约束;worktree → 默认命令化 + 轻 preflight;B4+B7 → 合并为「gate 执行语义」单一设计对象。

## §2 · 我的初步 verdict(草案)

七项批次收敛为**四个改造簇,全部 refactor/new、零 cut,既有强 gate/Safety Floor/codex 姿态不动**:
① **gate 执行语义**(B4+B7 合簇):`gate: true` task 语义进契约 + 下游 preflight 查 PASS artifact + 已判 run 登记表一次性消费 + 新 run 作废 stale 签字;契约章定不变量,SKILL 层落最轻实现(登记表 = 机器可读文件)。
② **分支拓扑规约**(B2+worktree 诉求合簇):session-per-idea worktree 默认命令化(复用原生 `-w`,不自建)+ 机器可读 baseline 声明(废「基线恒 = main」隐含假设)+ main 只留 proposal 期与合流点 + 带回流截止条件防长驻;双仓各落一份规约。
③ **LlmClient role 分离**(B5):new·契约变更,messages-style(system=指令/user=数据),T001 冻结接口走版本化迁移;allowlist 序列化降级保留为 defense-in-depth。
④ **证据与 hook 治理**(B3+B6 合簇):bootstrap-kit gitignore 模板改路径无关豁免 + 「证据已入 git」机器检查;hook 白名单按**模式类**集中收敛 + 定期回审(明拒「逐例加白」——KG-B1 同构路径病),fail-closed 姿态不动。

## §3 · 关键分歧清单

收敛度高,真分歧已不在判级,在**落地形状**,四条待 R2 定案:

1. **worktree 匹配校验的轻重**。我的立场:值得加一条轻 hook(校验「所改 `discussion/NNN` 与 worktree/分支名匹配」),因为本周混线恰发生在有规约意识的 operator 身上,纯自觉已实证不够;对方立场:"先用轻 preflight,不急着上重 hook"。期望收敛:定义「轻 preflight」的确切形状——建议 = 提示型(mismatch 时 warn 不 block),跑 3-5 session 后再裁要不要升 block(对齐 v7 watchdog 阈值「真跑校准」先例)。
2. **B5 迁移路径的粒度**。我的立场:契约版本化(v1 `complete` 与 v2 messages 并存过渡),因 bootstrap-kit 模板可能已扩散该形状;对方立场:"保留 T001 兼容迁移的约束"(未定粒度)。期望收敛:R2 给出迁移三步(契约章定 v2 → 新 task 强制 v2 → 旧消费面限期收编),并明确 001 项目内四个消费面是否本批迁移。
3. **main 在 IDS 治理仓的确切角色**。双方都还没深触:operator 原话「只有刚开始 proposal 用 main」,但 IDS 的治理产物(handback/HANDBACK-LOG/PRD/forge round files)当前全提交在共享分支上——idea worktree 分支何时、由谁合回 main?治理 docs 的 merge 拓扑是 ②簇 的必答题,不是可选项。期望收敛:R2 双方各给一个最小 merge 拓扑提案。
4. **契约章 vs SKILL 层的切分线**(我 P1 §3.3 的残留)。我的立场:①簇 的不变量(单次执行/一次性/stale 作废)进 SHARED-CONTRACT 新章(同 v7 fork-id §7 先例),SKILL 只落实现;对方立场:未显式表态(P2 只说「合并成 gate 执行语义」)。期望收敛:R2 确认层次切分 + 双仓 fixture 是否复用 v7 A4 模式。

## §4 · 与 K 的对齐性自检

- 七项批次全审、一项不漏 → ✅(四簇覆盖七项,映射显式)
- 止血核心优先、防过度工程 → ✅(worktree 复用原生能力零自建;gate 登记表 = 文件级;hook 校验从 warn 起步)
- gate 强制性不靠程序纪律 → ✅(①簇 全部机器可验)
- mirror 件三层同步纪律 → ⚠(方向遵守,但四簇各自涉及哪些 mirror 件、同步顺序,R2 草案必须逐簇显式列出)
- 动冻结契约须给迁移路径 → ⚠(方向已定版本化,粒度是分歧 2,R2 定案)
- 尊重证据权重(B5 九轮/B7 三轮硬证据) → ✅(两项均判 new 且优先级最高档)
