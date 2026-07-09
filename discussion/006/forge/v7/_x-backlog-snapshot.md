# X 快照 · XenoDev dogfood-backlog pending KG 权威全文(forge v7 用)

> **为什么有这个文件**:backlog 权威文件在 XenoDev 仓且**分支依赖**——KG-30~38 在 `feat/009-spec`
> 分支,KG-B1 在 `feat/001-radar-pA-spec` 分支(当前工作树),两者互不可见。加上 Codex 沙箱可能
> 读不到外部 repo,故把 v7 pending 批次的权威全文快照进本 forge 目录(v6 有 KG29 快照先例)。
> **快照时间**:2026-07-07T11:40Z。**KG-36 不在此**(forge v4 已覆盖)。
> 双方 reviewer:本文件与 FORGE-006-v7-PENDING.md(聚簇导航)配合读;能读外部 repo 时可去原文核对。

---

## A · 来自当前工作树(feat/001-radar-pA-spec 分支)

### KG-12 · handback-validator valid fixture/README 默认命令与 producer/consumer mode 分流不一致
- 日期: 2026-06-10T12:30:11Z
- 类型: bug
- 严重度: low
- 复现场景: review 时按 `lib/handback-validator/README.md` 的“valid → exit 0”思路跑 `bash lib/handback-validator/validate-handback.sh lib/handback-validator/test-fixtures/valid/handback.md /Users/admin/codes/ideababy_stroller`,实际 exit 1:默认 `--mode=consumer`,check-5 要求物理路径包含 `/discussion/<id>/handback/` 且 filename 是 `<ISO>-<handback_id>.md`,而 fixture 在 `lib/handback-validator/test-fixtures/valid/` 下。改用 `--mode=producer` 后 PASS;另一个带 timestamp basename 的 valid fixture默认 consumer 也因路径不含 `/discussion/.../handback/` 失败。即 README 的单元测试说明停留在 mode 分流之前,且缺一个真正 consumer-mode valid fixture 或模拟路径。
- 关联: `lib/handback-validator/README.md` §单元测试 / `lib/handback-validator/validate-handback.sh` `--mode=consumer|producer` / `lib/handback-validator/check-5-id-consistency.sh` / valid fixtures
- operator 确认: <留空 · 待 operator review:README valid 示例改成 producer mode,并新增/生成 consumer-mode fixture 路径测试;框架级,回 IDS forge 定>


### KG-22 · phased spec 增量补 phase 段时,per-phase review status 不被下游 gate 识别(只读 top-level status/reviewed-by)
- 日期: 2026-06-16T00:00:00Z(008-pB v0.2 spec 补段 · codex adversarial-review R3 [high] 捕获)
- 类型: 框架缺陷 | schema-gap
- 严重度: high(直接破 frozen-before-build 铁律 · 任何 phased spec 增量补 phase 都中招)
- 复现场景: 008-pB 是 phased spec(v0.1 已 frozen+ship)。本次在既有 spec 上**补 v0.2 段**(改了 binding 契约
  C5+/C11/P4/P5/O8-O10),为标 v0.2 段独立 review 状态,加了 frontmatter `v0.2_status: review` + `v0.2_reviewed-by: pending`,
  **保留 top-level `status: frozen`**(想表达「v0.1 段仍 frozen」)。codex R3 grep 了三个 consumer 证明:
  `task-decomposer/SKILL.md:22-24`、`parallel-builder/SKILL.md:54-55`、`specs/008-pB/scripts/status-008.sh:58-61`
  **全部只 gate top-level `status`==frozen + `reviewed-by`!=pending,没有任何一个读 `v0.2_status`**。
  → 后果:留 top-level frozen 时,下游 operator/automation 会把**未 review 的 v0.2 scope 当 buildable**,
  起 T2xx decomposition/build = 破「frozen-before-build」不变量,可 ship 未审 v0.2 契约变更。
  本项目当轮 workaround:top-level status 整体降 review(已 grep 证明 gate 正确 BLOCK),v0.2 过 review 后连同复位 frozen。
  但这是**项目级 workaround,框架本身缺「phased spec 的 per-phase 可 build 状态」表达**。
- 为何是框架级(非项目级): spec-writer SKILL 的 frontmatter schema(§3.3)只有单一 `status`/`reviewed-by`,
  对 phased spec「v0.1 frozen + v0.2 review 中」这种**部分 frozen** 状态无表达;task-decomposer/parallel-builder
  的 gate 也只认单一 top-level。**任何** phased spec 增量补 phase(像 006a-pM/008-pB 这类多次 hand-off 的 fork)
  都会撞同一问题。修好后受益的是「以后所有 phased 增量开发的项目」。
- 候选修法(回 forge 议 · 不当场改): ① spec frontmatter 加 `phase_status` map(每 phase 一个 frozen/review 状态);
  ② task-decomposer/parallel-builder gate 改为「读目标 task 的 phase → 查该 phase 的 status」而非单 top-level;
  ③ 或约定「补 phase 段期间 top-level 必须降 review」写进 SKILL(把本项目 workaround 升为框架约定 + 加 lint)。
  ②最彻底(支持 v0.1 task 仍可 build 而 v0.2 被 block 的并行态),但改动面大;③最轻(成文约定)。
- 关联: spec-writer SKILL §3.3 frontmatter schema / task-decomposer SKILL §(status gate) / parallel-builder SKILL §0.1 /
  specs/008-pB/scripts/status-008.sh:58 / 008-pB spec.md frontmatter v0.2_status / codex-v0.2-round3.log R3-F1
- operator 确认: <留空 · operator 阶段性 review 时补>


### KG-23 · codex `--scope working-tree` 看不到「已 commit 未 merge」的改动 → ship 流程每轮 commit 后 review 会 vacuous approve(空 diff)
- 日期: 2026-06-17T00:00:00Z(008-pB v0.2 T210 R3 ship review 踩到)
- 类型: 框架缺陷 | SKILL 机制(codex-review · ship 流程交互)
- 严重度: high(假 approve 风险 · ship gate 失效 · 任何「每轮修完 commit 再 review」的流程都中招)
- 复现场景: parallel-builder ship 流程 §2-§3 是「TDD commit → codex review → 改 → commit → 再 review」。
  T210 R2 修完**已 commit**(dc73508)后,跑 `codex adversarial-review --wait --scope working-tree` 做 R3 →
  codex 报「当前工作树无 staged/unstaged/untracked 变更,无可审 diff」**vacuous approve**。根因:codex
  companion 的 working-tree scope 实测只看 `git diff`(unstaged)+ 可能 staged,**不含已 commit 未 merge**。
  但 codex-review SKILL §0.2 line 67 明写 working-tree scope「worktree 内未 commit 改动 **+ 已 commit 但未
  merge 改动**」—— **文档与实现不符**。改用 `--base main --scope branch` 后得真 R3(3 个 high finding)。
  对照:T205 R2 同样 committed 后跑 working-tree 却**看到了** diff(真 review)—— 行为**不一致/intermittent**,
  更危险(有时假 approve 有时真审,无法预期)。
- 为何是框架级(非项目级): 影响 codex-review SKILL + parallel-builder ship 流程对**所有** task 的 review 有效性。
  ship 流程默认每轮 commit(§2.3/§4.4 要 commit 拓扑),然后 review —— 若 working-tree scope 漏 committed 改动,
  每个 task 的 codex gate 都可能 vacuous approve = ship gate 静默失效。修好后受益的是所有用这套 framework 的 task。
- 候选修法(回 forge 议 · 不当场改): ① codex-review SKILL §3 ship 流程内调用契约改为 `--base <merge-base>
  --scope branch`(review 已 commit 的 branch 全量),而非 working-tree;② 或 parallel-builder §3 调 review 前
  **不 commit**(review 未 commit 改动)再 commit —— 但破坏「每轮 commit 留痕」;③ 或修 companion 的 working-tree
  scope 让它真含 committed-unmerged(对齐 SKILL §0.2 line 67 文档);④ 至少 SKILL 加显式告警「ship 流程内每轮
  commit 后必须用 branch scope,不可用 working-tree」+ 加 lint(review 前检 working-tree 是否空 → 空则强制 branch scope)。
  ①最对(ship 流程本就该 review 整个未 merge branch);③修文档不符;④最轻(成文 + lint)。
- 关联: codex-review SKILL §0.2 line 67(scope 文档)+ §3.0.1 ship 调用契约 / parallel-builder SKILL §3 /
  /tmp/codex-T210-review-r3.log(vacuous approve)vs /tmp/codex-T210-review-r3b.log(branch scope 真 R3)
- operator 确认: <留空 · operator 阶段性 review 时补>


## 后台长任务(真跑)缺「可靠存活检测 + 单实例锁」约定 → 易误判重复起、互相写坏产物
- 日期: 2026-06-25T12:15:00Z
- 类型: 优化空间
- 严重度: medium
- 复现场景: 用 XenoDev 真跑 008-pB 回放下载(281 个 mp4 · 后台 `python3 driver --download-only &` 长跑 ~1h)。
  开发 Claude 盯进度时用 `ps -eo args | grep verify_token | grep python3 | grep -v grep` 判进程存活,
  **两次误报「已停」**(实际原始进程一直健康在跑 · 那个 grep 管道因时序/缓冲漏报),于是又起了 2 个
  并行进程 → **3 个 download-only 进程并行写同一 manifest + 同一批 run 目录** → ffmpeg 孤儿进程
  写坏 mp4(同文件被两个 ffmpeg 同时写 · 不完整)。止损:杀多余进程 + 删不完整 mp4 + ffprobe 全量校验。
  根因两层:① 开发 Claude 手搓 ps|grep 判存活不可靠(易误判);② 框架未给后台真跑提供「单实例锁
  (防重复起)+ 标准进度/存活查询」约定 → 每个用框架的人自己手搓、各自踩坑。
- 关联: parallel-builder / 后台真跑模式 · run_download_only(断点续靠「mp4 存在且非空」做 done 标记 ·
  但「不完整 mp4」也算存在 → 误跳;且无 flock 单实例锁)· 易复发于任何用本框架跑后台长采集的项目。
- 可能的框架侧解法(留 forge 议): ① 给长任务 driver 标配 flock 单实例锁(同 manifest/run-dir 只允许一个
  writer);② 落 PID 文件 + 标准「进度查询」脚本(不靠开发 Claude 手搓 ps|grep);③ 断点续 done 标记
  不只判「文件存在非空」,加完整性校验(size 匹配 Content-Length / ffprobe 可读)防「不完整即跳」。
- operator 确认: 

> ↑ 未编号条目 · 与 KG-38(挂起检测)同主题族:框架缺「后台长任务存活检测 + 单实例锁」约定 —— v7 簇1 审挂起检测时可一并纳入。

### KG-B1(001分支发现 · 与KG-29同族 · spine级 cross-repo) · hand-back validator 约束6 id-charset regex 不接受 IDS 铸的「带 idea-slug 中段」fork-id(如 001-radar-pA)→ 该 fork 全部 hand-back 无法发布
- 日期: 2026-07-07(001-radar-pA T001 ship · §4.1 hand-back producer 阶段触发)
- 类型: 框架缺陷(跨仓协议漂移 · IDS fork-id 铸造约定 vs XenoDev bootstrap-kit hand-back validator charset regex)
- 严重度: high(硬阻断:001-radar-pA 这个 fork 的**任何** hand-back 都过不了约束6 → 无法回流 IDS → task 无法完成 ship 收口。撞面 = 所有 IDS 用「带 idea-slug 中段」命名的 fork · 通用)
- 复现场景: 001-radar-pA T001(接口地基 · 代码已 ship + codex R1 两轮 + fallback 两轮全 approve)。跑 §4.1 hand-back producer(gen-handback --feature 001-radar-pA --task-id T001)。约束6 报 prd_fork_id (001-radar-pA) 不匹配 charset regex。根因:IDS plan-start 铸的 fork-id 001-radar-pA = 三段(discussion 001 + idea-slug radar + 变体 pA),**带 idea-slug 中段(radar)**;但 XenoDev validator 的 charset regex 从没预期中段 —— 只接 NNN 加可选字母加可选 -p 后缀。**关键**:即便 feat/009-spec 分支已有的 KG-29 v0.3 修(把 -p 单字符放宽成多字符 · 接 009-pForge/008-pB)**也不接受 001-radar-pA**(v0.3 只放宽 -p 后缀,没接中段 slug · 实测仍拒)。且本 001 分支 off main,连 v0.3 都没有(main 停在更窄的 v0.2)。
- 附带发现(gen-handback SSOT 坑): gen-handback 强读仓根 HANDOFF 的 prd_fork_id(防绕 SSOT · 不接受 --feature override),但 operator 同时开多 fork(008/009/001)时根 HANDOFF 只能是一个 → 为 fork B 产 hand-back 时会静默用 fork A 的 stale id(本次差点产成 008-pB)。workflow 假设「一时刻一活跃 fork」· 多 fork 并行下漏。
- 关联: lib/handback-validator/check-6 的 prd_fork_id charset 校验 · lib/handback-validator/gen-handback 强读根 HANDOFF · KG-29(009 分支 v0.3 修 -p 多字符 · **本条不同触发**:中段 idea-slug)· IDS plan-start fork-id 铸造约定(SSOT 在 IDS)
- operator 确认: <留空 · 待 operator review(框架级 · check-6/gen-handback 是 bootstrap-kit mirror 件 · 不当场改)· 建议方向:① check-6 regex 扩「idea-slug 中段」(需 IDS forge 严审 path-traversal 安全:中段只引连字符不引危险字符 · basename+realpath containment 防线仍在);② 或回 IDS 收紧 fork-id 铸造约定(去中段 slug · 也 forge);③ gen-handback 加显式指定 HANDOFF 路径 flag + 多-fork workflow 规约。**本仓不当场改 validator**(mirror 件 · 攒批回 IDS forge · 与 KG-29 同批审 fork-id charset 协议)。spine 级 cross-repo · 高优先>

---

## B · 来自 feat/009-spec 分支(git show feat/009-spec:dogfood-backlog.md)

### KG-32 · codex-review SKILL 无 fallback:codex 额度用尽/插件挂时 ship 流程 §3 review 强 hook 死锁(要么干等数小时、要么违规无 review merge)
- 日期: 2026-07-02T09:20:00Z(009-pForge T003 R2 re-review 实战触发 · codex 报 "You've hit your usage limit … try again at 7:45 PM")
- 类型: 框架缺陷(SKILL 机制 · 缺 degradation 路径)
- 严重度: medium(阻断单 task ship 推进 —— codex 是 §4.1 原子序步骤 1、gates merge;额度是账号级共享,今天 spec-rev-1 R1-R12 + T002 R1-R3 + T003 R1 共 16 轮 codex 打光额度,T003 R2 无法跑 → 整个 ship 卡在 review 门,worktree 只能干等 codex 重置)
- 复现场景: 009-pForge T003(high-risk correctness-spine · PIT 查询引擎)· §2 TDD 全绿(39 测 + 全 004 217 passed)· §3 跑 codex adversarial-review R1 找出 4 个真 [high/med] silent-wrong-number 缺陷 → 全修 + 红绿证据 → 要跑 **R2 确认闭合** 时 codex 报额度用尽(本地 19:45 才重置 · 距当时 ~2.5h)。ship 流程 §4.1 要求 codex PASS 才能 merge → 卡死。**当时的两条烂路都不可接受**:(a) 干等 2.5h(operator 不在、白烧上下文轮询)· (b) 无 review 直接 merge(违 §4.1 + C11 强 hook)。**operator 决议(2026-07-02):启用 subagent reviewer 作 fallback**(red-team-reviewer + code-reviewer 双跑逼近 codex 对抗强度)继续 review,拿 verdict 再 merge;codex 恢复后优先补跑作权威确认。**已当场落地为本仓治理**:写进 CLAUDE.md「## cross-model review fallback」段(operator 直接授权改本仓宪法)。
- 关联: `.claude/skills/codex-review/SKILL.md` §2 决策表 / §3 真路径 / §4 verdict(缺 "codex 不可用 → fallback 分流" 分支)· `.claude/skills/parallel-builder/SKILL.md` §3.0/§4.1(review 强 hook + 原子序)· CLAUDE.md「## cross-model review fallback」(本仓已落地版)· 实物:009-pForge T003 worktree R1 4-finding 修复 commit f154dd5/2a8bc60
- operator 确认: <留空 · 待 operator review(框架级 · codex-review SKILL 是 IDS bootstrap-kit mirror 件 · 本仓 CLAUDE.md 已落地过桥版但 SKILL 本体要回 IDS forge 定):建议把 fallback 分流写进 codex-review SKILL §2 决策表(加"codex 不可用"行 → red-team/code-reviewer subagent · verdict 标 subagent-fallback@date 不冒充 codex · codex 恢复补跑)+ 同步 SHARED-CONTRACT §6 若 review 门是协议层。**本仓 CLAUDE.md 已写(operator 授权),但 SKILL/协议层不当场改**(mirror 件 · 攒批回 IDS forge)>


### KG-33 · parallel-builder §5 `git worktree remove --force` 会静默丢弃 main worktree 的 stash 列表指针(内容悬空可救但列表消失·无守卫无告警)
- 日期: 2026-07-03T00:35:00Z(009-pForge T006 ship §5 删 worktree 实战触发)
- 类型: 框架缺陷(parallel-builder SKILL §5 机制 · 缺 stash 保全守卫 + 数据丢失静默)
- 严重度: medium(近失数据丢失 · 内容因 git 未 gc 尚可从悬空 commit 救回,但 SKILL 无任何守卫/告警 —— 若 operator 不懂 git 内部/或已跑过 gc,4 个文件真丢;stash-based park 是本框架起 task 的标准前置动作,撞面广)
- 复现场景: 009-pForge T006 · 起 task 前按范式 `git stash push --include-untracked -- <4 个 008-era 无关文件>` 保持 main worktree 干净(§0.1 硬约束要求干净树)· stash 成功(list 显示 stash@{0})→ 建 T006 worktree(基于 feat/009-spec HEAD)→ TDD+impl+review+merge 全过 → §5 `git worktree remove projects/009-pForge/T006` 报"包含未跟踪文件"(worktree 内 linter 改了 CLAUDE.md + 出现那两个 untracked 文件的副本)→ 改用 `git worktree remove --force` 删成功。**删完发现:main worktree 的 `git stash list` 变空、`git reflog show stash` 空、4 个 008 文件从 main worktree 消失**(CLAUDE.md line1 回退成旧版 · docs/scripts untracked 文件不见)。**救回过程**:`git fsck --lost-found` 找到 8 个悬空 commit → 逐个 `git show --name-only` 匹配 008 文件名 → 定位 stash merge-commit `71b05897`(subject "On feat/009-spec: 008-era files parked for T006 ship" · 3 parents:base/index/untracked)→ `git stash apply 71b05897` 完整恢复 4 文件(含 untracked 第三 parent)。**未丢**,但纯靠"git 没 gc + 我懂 fsck 悬空 commit"才救回。
- 关联: `.claude/skills/parallel-builder/SKILL.md` §5(删 worktree + branch · 只讲 `git worktree remove` + `git branch -D`,无 stash 保全 / 无删前快照校验 / 无"worktree 内有未追踪文件"的处理指引)· §0.1(要求 working tree 干净 → 逼出 stash-park 前置动作 → 与 §5 的 --force 删除形成隐性冲突)· 备份破坏检测件 3(`.claude/safety-floor/backup-detection/` · 但那是防"同凭据删主存+备份",没覆盖"worktree 操作误伤 stash"这类 git 内部数据丢失)· 实物:悬空 stash commit 71b058970e1516d9711a26f46e2181efbd2182fa(本次可复现证据)
- operator 确认: <留空 · 待 operator review(框架级 · parallel-builder SKILL 是 XenoDev 自派生但 §5 worktree 生命周期是通用机制)· 建议方向:① §5 删 worktree 前显式 `git stash list` 快照 + 删后比对(变化则告警"worktree remove 可能影响 stash · 检查悬空 commit");② 或 §0 park 前置动作改用「commit 到临时分支」而非 stash(commit 有 reflog 保护 · stash 悬空更脆);③ 或 §5 明确"worktree 内出现未追踪文件时先查来源再 --force,别盲删"的指引 + 附 fsck 悬空 commit 救援步骤。**根因存疑**:worktree remove --force 理论上不该动 main worktree 的 stash ref —— 可能是 stash-park 的 4 文件同时以某种形式存在于两个 worktree(linter 在 T006 worktree 也改了 CLAUDE.md)导致的交互 · 需 IDS forge 时深查 git worktree + stash 交互真因。**本仓不当场改 SKILL**(攒批回 IDS forge)>

### KG-34 · 迁移单测 executescript 与生产 op.execute(SQLAlchemy text)行为不一致:DDL 内 ':字' bind-param 陷阱单测测不出
- 日期: 2026-07-03T03:10:00Z(009-pForge T010 · M2 analyst_alpha 两表 migration 实战触发)
- 类型: 框架缺陷(迁移测试范式盲区 · test/生产行为分叉 → 假绿)
- 严重度: medium(单测全绿但真 alembic upgrade 直接炸 · 撞面 = 所有含中文/带冒号注释的 DDL migration task · 本框架 migration task 都用这套 executescript 单测范式,盲区通用)
- 复现场景: 009-pForge T010 建 analyst_alpha_eval/rejections 两表(alembic 0015)。迁移单测范式(照 test_migration_0014 派生)用 `conn.executescript(stmt)` 跑 DDL —— sqlite3 原生 executescript **不解析 `:param`**,10 个单测全绿。但生产 `upgrade()` 用 `op.execute(stmt)`,alembic/SQLAlchemy 走 `text()` **会把 DDL 字符串里的 `:字` 解析成 bind parameter**。本 task DDL 内 `--` 注释有中文"去重键含 market(rev-1)冒号同 (...)" → SQLAlchemy 把冒号后的"同"当绑定参数 → 真 `alembic upgrade head` 报 `sqlalchemy.exc.InvalidRequestError: A value is required for bind parameter '同'`,upgrade 卡在 0014 上不去 0015。**单测测不出**(executescript 路径不解析),只有 §2.4 verification 真跑 `alembic upgrade head` 才暴露。修法:DDL 内注释去 ':字' 模式(冒号后加空格或改标点)。0014 侥幸没踩(它的 ':字' 都在模块级 `#`/docstring 注释,不在 DDL 字符串内 · 但这是巧合非防线)。
- 关联: `.claude/skills/parallel-builder/SKILL.md` §2 TDD(迁移单测范式)· `alembic/versions/0014_add_price_daily_ticker_status.py`(被照抄的范式源 · executescript 单测)· 实物证据:009-pForge T010 worktree · 错误 `A value is required for bind parameter '同'` · commit 27383c8(修 3 处 ':字' 注释)
- operator 确认: <留空 · 待 operator review(框架级 · 迁移测试范式通用盲区)· 建议方向:① 迁移单测范式改用 `op.execute` 等价路径(或额外加一条"真 alembic upgrade head 到本迁移"的单测/CI 步骤,覆盖 executescript 测不到的 text() 解析)· ② 或在 parallel-builder §2.4 verification 强制"migration task 必真跑 alembic upgrade head"(本 task 是靠这步才抓到 · 但应写成硬 checklist 不靠自觉)· ③ 或 DDL 生成加 lint 禁 ':字' 模式在 op.execute 字符串内。**本仓不当场改 SKILL**(bootstrap-kit mirror · 攒批回 IDS forge)>

### KG-35 · codex-review companion `--wait` 的最终结构化 verdict/findings 不稳定落 stdout log,需靠 `status --all` job summary 兜底
- 日期: 2026-07-03T03:30:00Z(009-pForge T010 · codex 恢复后多轮 spine migration 审实战触发)
- 类型: 框架缺陷(codex-review verdict 提取脆弱性 · SKILL §4 verdict 解析依赖不稳定输出)
- 严重度: medium(不影响 review 本身正确性,但影响 ship 流程自动化可靠性:若只读 log 会漏 verdict/findings → 可能误判"无 finding 可 merge",实际有 blocking · KG-32 fallback 分流 + codex-review SKILL §4 verdict 解析都假设能从输出拿到结构化 verdict)
- 复现场景: 009-pForge T010(M2 analyst_alpha migration)· codex 恢复后连跑 5 轮 adversarial-review(R1-R5)。`node companion.mjs adversarial-review --wait --scope branch > log 2>&1` —— **R1 的最终 `Verdict:`/`Findings:` block 完整落 log**,但 **R2/R3/R4/R5 的最终结构化 verdict/findings 没落 log**(log 停在 `[codex] Command completed` 工具调用序,最终 assistant report 丢失)。中途的 `{"verdict":"needs-attention",...}` assistant message captured 有落,但那是分析过程非最终结论。**靠 `node companion.mjs status --all --json` 的 `latestFinished.summary` 兜底**才拿到真 verdict(如 R2="eval 表的价格 provenance 仍可写成不可复现的假引用" · R4="已计算 eval 行可以带结果、却让 provenance 全空落库")—— summary 字段稳定含结论,但 findings 细节要读 job 独立 logFile(`~/.claude/plugins/data/codex-openai-codex/state/<task>/jobs/<jobid>.log`)。若 SKILL §4 verdict 解析只 grep 主 stdout log,会在这些轮次拿不到 verdict → 误判。另注:`result --json` 子命令返回的字段结构与 status 不同(verdict/summary 为 None),不可靠。
- 关联: `.claude/skills/codex-review/SKILL.md` §4(verdict 解析 + fail-closed · 假设从输出拿结构化 verdict)· §3(companion 调用契约)· KG-32(fallback 分流也依赖 verdict 提取)· 实物证据:009-pForge T010 · R2 job `review-mr4cwqbh-rsfd6k` summary vs 主 log 截断 · R4 job `review-mr4ddhg3-bgjo95`
- operator 确认: <留空 · 待 operator review(框架级 · codex-review SKILL 是 bootstrap-kit mirror 件)· 建议方向:① SKILL §4 verdict 解析改为**优先** `status --all --json` 的 `latestFinished.summary` + job 独立 logFile(findings),不只依赖主 stdout log · ② 或调 companion 时加显式结构化输出 flag(若 companion 支持 `--json`/`--output <file>`)· ③ 或 verdict 提取加 fallback 链(主 log → status summary → job logFile),任一拿到即用 · ④ 复现根因:companion `--wait` 的 stdout 缓冲/最终 report 落盘时序问题,需 IDS forge 时深查 companion.mjs 输出机制。**本仓不当场改 SKILL**(bootstrap-kit mirror · 攒批回 IDS forge)>

> (KG-36 略 · forge v4 已覆盖)

### KG-37 · codex-review companion branch-mode 在 sandbox 下跑不了只读 git/rg(bwrap loopback 失败)→ §3 review 强 hook 环境性失效
- 日期: 2026-07-06T09:20:00Z(009-pForge T016 evaluate CLI ship · §3 codex adversarial-review 实战触发)
- 类型: 框架缺陷(codex-review SKILL / companion runtime 在受限沙箱下的可用性 · 影响 ship 流程 §3 强 hook)
- 严重度: medium-high(不是 codex 额度问题(KG-32),是 codex **能起但跑不了 review 所需只读命令** → branch-mode review 拿不到 diff → fail-closed needs-attention「无法完成审查」· 若无 fallback 就卡死 ship;撞面 = 所有在此机器/沙箱配置下跑 codex branch-mode review 的 spine/write-boundary task · 通用)
- 复现场景: 009-pForge T016(M2 evaluate CLI · write-boundary/PPV-spine · 该走 adversarial-review)。T016 改动已 commit(working tree 干净),先跑 `node companion.mjs adversarial-review --wait --scope working-tree` → codex 报「未发现可审查的 working tree diff」(commit 后 working-tree 空 · 预期)。改跑 branch-mode `--base feat/009-spec --scope branch` → codex thread 起得来、turn 起得来,但其**只读 git/rg 命令全部** `bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted` 失败(沙箱禁 network namespace loopback setup)→ codex 拿不到 branch diff → fail-closed verdict=needs-attention「No-ship:无法完成必须的分支 diff 审查 · 当前证据不足」(**非代码 finding · 是工具环境失效**)。job `review-mr90cku0-4gnnjy`。→ 按 CLAUDE.md 「codex 额度用尽/插件不可用 → subagent fallback」铁律外推(此处是「插件跑不动」非「额度尽」· 同类维持 review 门场景)走 `red-team-reviewer` + `code-reviewer` 双跑(write-boundary → 双跑档),三轮 red-team 收敛 approve(F1 idempotency ship-blocker 抓到并修 · 见 T016 REVIEW-LOG)。**fallback 救了场 · 但 codex 这条主审路在本环境对 branch-mode 直接不可用**。
- 关联: `.claude/skills/codex-review/SKILL.md` §3(companion 调用契约 · §3.1/§3.2 真路径)· `.claude/skills/parallel-builder/SKILL.md` §3(ship 流程 §3 强 hook)· CLAUDE.md「cross-model review fallback」段(判据「插件不可用」已含此情形 · 但只说「额度尽/companion 不可用」· 没明说「companion 起得来但沙箱禁 review 命令」这一子类)· KG-32(codex 额度用尽 fallback · 本条是**不同触发**:能起但跑不动)· 实物证据:T016 worktree · working-tree job `review-mr9063oi-ycf12x`(空 diff)· branch job `review-mr90cku0-4gnnjy`(bwrap loopback 失败 · needs-attention 非代码 finding)
- operator 确认: <留空 · 待 operator review(框架级 · codex-review SKILL 是 bootstrap-kit mirror 件 · 不当场改)· 建议方向:① codex-review SKILL 的 fallback 判据**明确加一子类**:codex 起得来但 review 命令因沙箱失败(bwrap/network/权限)→ 同「插件不可用」走 subagent fallback(现 CLAUDE.md 文字勉强覆盖但不显式 · 易犹豫);② 排查 companion/codex 沙箱能否放行只读 git/rg(review 只需读不需网 · loopback 权限是过度限制?)· 或给 companion 一个「diff 从 stdin/文件喂入」的非沙箱模式(operator 侧先 `git diff` 好喂进去 · 绕开 codex 自己收集 context 需要的命令执行);③ branch-mode review 前**优先** working-tree scope(commit 前审 · 避开 branch diff 需要跑 git 的问题)—— 但这与 §4.1 原子序(review 在 verifier 后 merge 前 · 此时已 commit)冲突,需 forge 权衡审序;④ 复现根因需 IDS forge 深查 companion.mjs 的 codex-exec 沙箱配置(bwrap network namespace 为何禁 loopback)。**本仓不当场改 SKILL**(bootstrap-kit mirror · 攒批回 IDS forge)>

### KG-38 · codex-review companion `review` 后台 job 会话流中途掉线挂死(status 恒 running · 不产 verdict · result 报 No job found)→ §3 review 强 hook 静默卡死
- 日期: 2026-07-06T13:05:00Z(009-pForge T017 M2 contract tests ship · §3 codex review 实战触发)
- 类型: 框架缺陷(codex-review companion runtime job 生命周期 · 会话流断线无恢复无超时 · 影响 ship 流程 §3 强 hook)
- 严重度: medium-high(不同于 KG-37 的 bwrap loopback 环境失效 · 也不同于 KG-32 额度尽:这里 codex **job 起得来、只读 git 命令全 exit 0 跑通、把 5 个不变量源文件全读完**,然后 reasoning/verdict 流**掉线后完全静默 7+ 分钟不产任何 verdict** · 而 `status` 一直报 `running`(pid 活着)· `result <job>` 却报 `No job found` · 无自动超时 / 无掉线重试成功 / 无 fail-closed → **若开发 agent 傻等就无限卡死 ship**;撞面 = 所有跑 codex 后台 review 且遇会话流不稳的 task · 通用)
- 复现场景: 009-pForge T017(M2 contract tests · medium test-only → 该走 codex `review` 档)。3 测已 commit(working tree 干净)· 跑 `node companion.mjs review --background --base feat/009-spec --scope branch`。前台 launch 命令自身 2min 超时(即使 `--background`)· 但 `status` 显示 job `review-mr987xty-4f9oyg` 确实注册且 running。查 job log:12:58:56 thread 起 → **12:59:15/20 报 `Codex error: Reconnecting... 2/5, 3/5`(会话流早期掉线)** → 掉线后仍跑通一串只读 git(`git diff` / `git show HEAD:<各源文件>` 全 exit 0)· 13:00:37 读完最后一个源文件 `registry.py` → **之后完全静默**。轮询到 5m12s 时 `status` 仍 `running`(pid 1446409 活)· log 自 13:00:37 起 7+ 分钟零新行 · `result <job>` 报 `No job found`(与 status 矛盾)。判定挂死 → `cancel <job>`(成功 · 转 cancelled)→ 按 CLAUDE.md fallback 铁律(此处是「会话掉线挂死」· 归入「插件不可用」子类)· medium 单层 test-only → `code-reviewer` 单跑 → approve(0 blocking + 3 non-blocking 完备性 nuance · 独立复跑 assemble + 5 源交叉核对 · 见 T017 REVIEW-LOG)。**fallback 救了场 · 但 codex 会话掉线后既不恢复也不超时也不报错退出,是个静默卡死陷阱**。
- 关联: `.claude/skills/codex-review/SKILL.md` §3/§4(companion 调用契约 + verdict 解析 · 无「job 挂死/超时」处理路径)· `.claude/skills/parallel-builder/SKILL.md` §3(ship 流程强 hook)· CLAUDE.md「cross-model review fallback」段(判据含「插件不可用」· 但同 KG-37 一样没显式列「job 起得来但会话流掉线后挂死不产 verdict」这一子类)· KG-37(bwrap loopback env 失效 · **本条不同触发**:命令跑通了、是会话流/reasoning 流掉线)· KG-32(额度尽 · 又不同)· 实物证据:job `review-mr987xty-4f9oyg` · log `state/T017-284b34a936abb9dd/jobs/review-mr987xty-4f9oyg.log`(末行 13:00:37 · Reconnecting 2/5 3/5 在 12:59)· json status=running 与 result=No-job-found 矛盾
- operator 确认: <留空 · 待 operator review(框架级 · codex-review SKILL 是 bootstrap-kit mirror 件 · 不当场改)· 建议方向:① companion job 加**掉线/静默超时**:job log 在 `Reconnecting... N/5` 用尽或末次活动后 X 秒无新行 → 自动转 `failed`(而非永远 `running`)· 让轮询侧能确定性判死 · 不靠人肉数分钟;② `status` 报 running 但 `result <job>` 报 No-job-found 的**状态不一致**要修(至少 result 该回「job 仍 running · 无结果」而非「不存在」· 现语义误导);③ codex-review SKILL 的 fallback 判据显式补一子类(同 KG-37 建议①的合并):codex job **会话流掉线/挂死超时** → 同「插件不可用」走 subagent fallback · 并给一个**明确的判死阈值**(如末次 log 活动 > N 分钟静默 = 挂死)· 免得开发 agent 犹豫要等多久;④ 排查 companion.mjs 的 codex thread 断线重连逻辑(`Reconnecting 2/5 3/5` 后为何不再续 4/5、5/5 而是静默)。**本仓不当场改 SKILL**(bootstrap-kit mirror · 攒批回 IDS forge)>
