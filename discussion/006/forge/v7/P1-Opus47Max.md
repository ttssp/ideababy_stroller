# Forge v7 · 006 · P1 · Claude · 独立审阅(no search)

**Timestamp**: 2026-07-07T11:45:00Z
**Searches used**: NONE in this round.
**Visibility**: I did NOT read other reviewer's P1.
**Reviewer stance**: 审阅人 — 评判已存在物,不是 daydream。
**Model note**: 本轮由 Claude(Fable 5)执笔,文件名沿用管线约定。

## 0. 我读到的标的清单 + 阅读策略

- 我读了:
  - `FORGE-006-v7-PENDING.md` → 全文(聚簇导航 + 两 session fresh evidence)
  - `forge/v7/_x-backlog-snapshot.md` → 全文(pending KG 权威文本:KG-12/22/23/32/33/34/35/37/38 + KG-B1 + 未编号「后台长任务存活检测」条)
  - `/home/ys/codes/XenoDev/dogfood-backlog.md` → 读了当前工作树版(发现**分支依赖**:KG-30~38 只在 feat/009-spec,KG-B1 只在 feat/001-radar-pA-spec;这本身就是一条观察,见 §1B)+ 经 `git show` 核对 009 分支原文与快照一致
  - `forge/v6/stage-forge-006-v6.md` → verdict/decision-list/underweight 三节(确认 v7 批次与 v6 的 KG-26~31 无重叠;KG-29 的"v0.3 只放宽 -p 后缀"历史直接喂给 KG-B1 分析)
- 我跳过的:无(X 全部可达)
- **K(用户判准)摘要**:双主攻——①「review gate 不能单点依赖 codex,fallback 要制度化不靠临场犹豫,挂起态要能超时检测触发 fallback」;②「KG-B1 跨仓 fork-id charset 协议漂移,正在阻塞 001-radar-pA 反向通道,裁 regex 扩展 vs IDS 铸造约定收紧」。硬约束:mirror 件改动落 IDS 三层同步,不在 XenoDev 当场改。
- **我的阅读策略**:按 Y=工程纪律优先读每条 KG 的「复现场景 + 关联 SKILL 段落」;按 Y=架构设计横向找五条簇1 KG 的共同结构与跨仓契约的所有权划分。

## 1. 现状摘要(按 Y 视角组织)

### 视角 A · 工程纪律

ship 流程把 codex review 设为 §3/§4.1 的**强 hook 原子序步骤**(无 review 不 merge),但 codex-review SKILL 本体没有任何失效分支。实战一周内 fallback 被迫发生了至少三次、三种**互不相同的失效模态**:KG-32 额度耗尽(codex 起不来)、KG-37 沙箱 bwrap loopback 禁令(codex 起得来但 review 所需只读 git/rg 全 fail)、KG-38 会话流掉线挂死(命令全跑通、读完源文件后 reasoning 流静默 7+ 分钟,status 恒 running 而 result 报 No job found)。目前的治理现状是:operator 在 KG-32 现场决议 subagent fallback 并**写进了 XenoDev CLAUDE.md「cross-model review fallback」段**(过桥版),但 SKILL 决策表没有对应分支——于是 KG-37/38 两次都靠"按铁律外推"临场判断,每次都在消耗犹豫成本。KG-38 还暴露 companion 无超时、无 fail-closed、status/result 语义自相矛盾;毗邻的未编号条目(后台长任务 ps|grep 误判 → 3 进程并行写坏 mp4)说明「长任务存活检测」是比 codex 更宽的纪律空白。

verdict 的**提取与有效性**同样脆弱:KG-35(--wait 最终 verdict 不稳定落主 stdout,靠 status --all summary 兜底,而 SKILL §4 假设主 log 可解析)、KG-23(working-tree scope 文档说含 committed-unmerged、实测不含且 intermittent → 每轮 commit 后 review 可能 vacuous approve = gate 静默失效,这是**假绿**类риск里最危险的一条)。簇3 的 KG-34 是另一处假绿(executescript 单测测不出生产 text() 的 `:字` bind-param 陷阱,靠 §2.4 真跑兜底);KG-33 是近失数据丢失(worktree remove --force 后 stash 列表消失,靠 fsck 悬空 commit 救回,SKILL §5 无守卫无告警,**根因存疑**)。簇4 KG-22:phased spec 的 per-phase review status 无 schema 表达,三个下游 consumer 只读 top-level status——增量补 phase 必撞 frozen-before-build 铁律。

### 视角 B · 架构设计

簇1 五条的共同结构:review gate 是**单通道架构**(codex companion 唯一权威),失效处理是**事后追认的惯例**而非架构组件。值得注意的是分流的雏形其实已在实践中长出来:按 task 风险分级选 fallback 强度(T016 write-boundary → red-team+code-reviewer 双跑;T017 medium test-only → code-reviewer 单跑),且 REVIEW-LOG 有「reviewed-by: subagent-fallback@date 不冒充 codex」的诚实标注惯例——**缺的不是实践,是把实践升格为 SKILL 决策表里的显式分支**(失效判据分类 × 风险分级 × 降级链 × 判死阈值)。

跨仓契约面(KG-B1)的现状:fork-id 的**铸造**在 IDS(plan-start),**校验**在 XenoDev(bootstrap-kit mirror 件 check-6 charset regex),两边没有共同的 schema 定义源。演化史已经证明了"逐例放宽 regex"这条路的形状:KG-29 v0.2→v0.3 只放宽了 `-p` 多字符,001-radar-pA 的 idea-slug 中段立刻再断,且 v0.3 修还只在 009 分支(main 停在 v0.2)——**每一种新命名习惯都会再断一次,每次修还要跨分支漂**。附带的 gen-handback「仓根 HANDOFF = 唯一活跃 fork」SSOT 假设与 operator 实际的多 fork 并行(008/009/001 同开)直接冲突。另一条架构级观察来自我读 X 的过程本身:**dogfood-backlog 也是分支依赖的**——001 分支看不到 009 分支的 KG-30~38,append-only 纪律在多分支并行下事实上被切成了多本账。

## 2. First-take 评分(按 Y 视角)

| Y 维度 | 倾向 | 理由(引用 §1 现状) |
|---|---|---|
| 工程纪律 | **keep 意图 + refactor 机制** | 「无 review 不 merge」强 hook 与 fail-closed 姿态是对的,别动;但失效分支要从 CLAUDE.md 过桥文字**制度化进 SKILL 决策表**:失效判据三分类(起不来/起得来跑不动/跑得动挂死)× 判死阈值(静默 N 分钟=挂死)× verdict 提取 fallback 链(主 log→status summary→job logFile)。KG-23 的 scope 语义要先修文档与实现不符,ship 流程内强制 branch-scope(或 lint 空 diff 拦截)。KG-34 把「migration task 必真跑 alembic upgrade head」写成硬 checklist。 |
| 架构设计 | **refactor(review 通道)+ new(fork-id 契约单点)** | 单通道+临场 fallback → 显式「review 通道抽象」:主通道 codex,降级链按风险分级,子代理 fallback 标注不冒充(实践已长出,升格即可)。KG-B1 拒绝第三次逐例放宽 regex:**new 一个跨仓 fork-id 规范单点**(SSOT 在 IDS,格式规范 + 安全字符集显式成文,XenoDev mirror 消费同一定义),或收紧 IDS 铸造——方向待 P3 裁,但"每种新命名再断一次"的现状必须终结。KG-33 根因存疑,**不该在推演里定修法**,先真复现(与 [[forge-verdict-vs-empirical-ship]] 教训一致)。 |

## 3. 我现在最不确定的 3 件事

1. **KG-B1 的修法方向**:扩 check-6 regex 接 idea-slug 中段(需严审:中段允许的字符集如何不引入 path-traversal 面?`^[0-9]{3}(-[a-z0-9]+)?-p[A-Z]\w*$` 这类形状安全吗?)vs 回 IDS 收紧铸造约定(但 001-radar-pA 已在用,改名有历史成本)vs 两头都动(IDS 定规范、XenoDev 消费)。我希望 P2 搜「跨系统共享 id/schema 契约的演化管理」先例(schema registry / 契约测试),P3 听对方对安全面的判断。
2. **挂起检测的判死逻辑放哪一层**:companion.mjs 内建超时(最彻底,但 companion 是 XenoDev 侧 runtime,修它是否越出 IDS forge 的管辖?)vs SKILL 层轮询判死约定(N 分钟静默=挂死,轻但每个调用方都要自己实现)vs 框架级「后台长任务 liveness + 单实例锁」通用约定(把未编号条目一起解决,面最大)。希望 P2 搜 watchdog/liveness 的标准做法,P3 收敛出分层答案。
3. **KG-23 的审序权衡**:候选修法①(ship 流程内一律 branch-scope)最对,但 KG-37 实测 branch-mode 恰恰是沙箱失效重灾区——两条 KG 的修法可能互相顶牛(working-tree 避沙箱但漏 committed;branch 全量但撞 bwrap)。这个交互在单条 KG 里看不见,需要 P3 把簇1 当一个系统来收敛,而不是逐条给药。
