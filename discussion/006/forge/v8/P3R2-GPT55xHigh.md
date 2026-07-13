# Forge v8 · 006 · P3R2 · GPT55xHigh · 联合收敛 R2(finalize)

**Timestamp**: 2026-07-13T20:16:02+08:00
**Visibility**: 我已读对方 P3R1 + P3R2。
**Convergence mode**: strong-converge

## 1. 我对每条分歧的最终立场 + 让步

- **worktree 校验轻重**:接受对方终案。P0 = 默认 `claude -w <idea>`、worktree/branch 与 idea id 对齐、warn 型 preflight;hook block 留 v0.2。我的让步是撤回 P0 轻 hook。补充:outbox/handback frontmatter 写 `current_idea` / `worktree` / `baseline`。
- **B5 迁移粒度**:接受双方案合一。messages-style 是 v2 正典;`complete(prompt)` 只作 legacy adapter;新 task 强制 v2;旧消费面在自然接触点收编。补充要求:compat test 覆盖 v1/v2 同语料双跑。
- **main 治理角色**:接受 lifecycle:proposal on main → idea worktree branch → human checkpoint 合回 main → cleanup。checkpoint 复用 handback-review、stage 定稿、forge verdict 等既有决策点。main 是 accepted governance artifact 归档线,不是日常多 idea 工作线。
- **契约 vs SKILL**:无 unresolved。SHARED-CONTRACT 写 gate 不变量(PASS 查验、单次执行、answer-key 一次性、新 run 作废 stale 签字);SKILL/preflight 写最低实现;mirror 同步作验收项。

## 2. 联合 verdict(单一)

**incremental optimize,不 redesign,零 cut。** 七项收敛为四簇:① B4+B7 = gate 执行语义(P0),契约写不变量,XenoDev 用登记表/preflight 机器查验;② B2+worktree = 分支拓扑显式化(P0/P1),默认 worktree-per-idea,main 只作 proposal 与合流线,baseline 改机器可读声明;③ B5 = LlmClient v2 契约(P0/P1),messages-style 正典,adapter 保兼容,sanitize 降级为纵深防御;④ B3+B6 = 证据与 hook 治理(P1),修 gitignore/证据入仓检查,误报用集中 allowlist/baseline/audit,fail-closed 不动。该 verdict 尊重硬证据,止血核心优先,不自建大系统。

## 3. 残余分歧降级为 v0.2 note

- warn preflight 后若 mismatch 复发 2 次,再升 commit-time block。
- B5 v1 直接消费面若 3 个月后仍残留,再裁专门迁移 task。
- gate 登记表并发先不加锁;同 gate 双 session 真实出现后再加原子写/锁。
- worktree 不隔离 DB/env/端口;第一次资源冲突后再规约互斥声明。

## 4. W 形态产出的初步草稿建议

- **verdict-only**:用 §2 首句 + 四簇名。
- **decision-list**:保留 Safety Floor、强 gate、codex primary、parallel-builder;调整 B2/B3/B6;新增 B4+B7、B5 v2、worktree 默认;defer §3 四项。
- **refactor-plan**:四模块对应四簇,每模块列问题、目标态、最小实现、验收证据、mirror 同步;gate 模块复用 v7 SSOT+mirror+fixture 纪律。
- **next-dev-plan**:P0 = gate 契约章、worktree/main 规约、B3 止血、B5 v2 契约;P1 = XenoDev preflight、baseline 消费、adapter、B6 集中治理;P2 = v0.2 notes 按真实复发升级。
