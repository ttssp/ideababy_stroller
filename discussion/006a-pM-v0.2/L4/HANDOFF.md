---
# §6.2 workspace schema 4 字段
workspace:
  source_repo: /Users/admin/codes/ideababy_stroller
  build_repo: /Users/admin/codes/XenoDev
  working_repo: /Users/admin/codes/ideababy_stroller
  handback_target: /Users/admin/codes/ideababy_stroller/discussion/006/handback/

# §3.1 source_repo_identity 字段(IDS forward producer 填 · XenoDev hand-back producer 透传)
source_repo_identity:
  expected_remote_url: git@github.com:ttssp/ideababy_stroller.git
  repo_marker: "# Idea Incubator — Project C"
  git_common_dir_hash: 28d25bf82af4c0e2

# Hand-off metadata
prd_fork_id: 006a-pM-v0.2
discussion_id: "006"
prd_form: simple
phases: null
modules: null
module_forms: null
critical_path_module: null
skip_rationale: null

handed_off_at: 2026-05-28T03:13:19Z
prd_source: /Users/admin/codes/ideababy_stroller/discussion/006a-pM-v0.2/PRD.md
shared_contract_version_honored: 2.0

# Cross-repo split 扩展字段(IDS forward 端 v0.2 加 · SHARED-CONTRACT §6 隐含模式显式化)
cross_repo_split: true
target_repo_enum: [IDS, XenoDev]
default_target_repo: IDS
---

# Hand-off · 006a-pM-v0.2 → XenoDev (per SHARED-CONTRACT §6 v2.0)

**Handed off at**: 2026-05-28T03:13:19Z
**PRD source**: /Users/admin/codes/ideababy_stroller/discussion/006a-pM-v0.2/PRD.md
**Build repo**: /Users/admin/codes/XenoDev
**Workspace**: 见 frontmatter `workspace:` 块(§6.2 4 字段全填)
**Source repo identity**: 见 frontmatter `source_repo_identity:` 块(XenoDev 写 hand-back 前必须按 §6.2.1 约束 3 校验)
**SHARED-CONTRACT version honored**: 2.0

## §1 · 给 XenoDev operator 的指令

operator 切到 build_repo 后:

1. `cd /Users/admin/codes/XenoDev`
2. 读本 HANDOFF.md(全文)+ 引用的 PRD.md(`/Users/admin/codes/ideababy_stroller/discussion/006a-pM-v0.2/PRD.md`)+ 推荐同步读 v3 forge stage doc(`/Users/admin/codes/ideababy_stroller/discussion/006/forge/v3/stage-forge-006-v3.md` §W3 refactor-plan + §W5 dev plan 已就绪)
3. 在 XenoDev session 触发 XenoDev 自带的 spec-writer(per XenoDev AGENTS.md;**不**调 IDS 的 spec-writer subagent — XenoDev 派生自己的)
4. spec-writer 产 XenoDev 内部 spec.md(7 元素 schema · simple PRD-form 走标准 7 文件输出)
5. XenoDev task-decomposer 产 tasks/T*.md
6. parallel-builder 跑 task,quality gate 在 XenoDev 内部决议
7. 每个 task ship 后 XenoDev 产 hand-back 包(per §6.3 schema)写回 IDS `/Users/admin/codes/ideababy_stroller/discussion/006/handback/`

## §2 · PRD-form 透传(XenoDev spec-writer 分派依据)

`prd_form: simple`(详见 frontmatter)

- simple    → 标准 7 文件输出 ✅ (本 PRD 走此分支)
- phased    → SLA / risks 按 PRD `**Phases**` 数组分段
- composite → 顶层 spec.md 退化为 INDEX,**额外**为每 module 输出 spec-<m>.md
- v1-direct → SLA.md 顶部加 §'Skip rationale'

## §3 · §6.2.1 6 约束自检契约(XenoDev producer 写 hand-back 前必走)

per `framework/SHARED-CONTRACT.md` §6.2.1,XenoDev 产 hand-back 包写入 `<source_repo>/discussion/<discussion_id>/handback/` 前,必须按 6 约束自检:

1. canonical-path containment(realpath prefix 校验)
2. symlink reject(路径任一段是 symlink 即拒)
3. repo identity check(三模式:remote / no-remote / hash-only,任一 PASS 即满足)
   - remote 模式:对比 `git config remote.origin.url` 与本 HANDOFF.md `expected_remote_url`
   - no-remote 模式:`head -c 30 CLAUDE.md` 与 `repo_marker` 严格相等
   - hash-only 模式(可选):`shasum -a 256 .git/HEAD .git/config | head -c 16` 与 `git_common_dir_hash` 相等
4. id consistency check(三处 id 严格一致:`discussion_id=006` · `prd_fork_id=006a-pM-v0.2` · 路径 `discussion/006/handback/<basename>` 含 `006a-pM-v0.2`)
5. id 字符集 + filename basename + final-path containment(OWASP path traversal 防御)
6. hard-fail(任一约束失败,producer 不写 / consumer 不读)

任一失败 = `Drop`(不写文件,不创目录,只 stderr)。

## §4 · Open questions for build phase

(从 IDS PRD §"Open questions" 分流过来 · XenoDev build 自然遇到时解决 · 不污染 XenoDev spec frozen)

- **OQ-1** · C-3 case F 根因修复:选 a(`score-handback escape` 真路径修)vs 选 b(删 case F)— operator 在 XenoDev wave 1 真路径首次跑 FU-producer-1 时临门决定 · 不影响 P0 必修
- **OQ-2** · `bootstrap.sh` 升级是否需要新增 `verify-bootstrap.sh` smoke test — wave 3 起 task 时决定 · 推荐建(W3 模块 A wave 3 未列但属 K10 边界纪律延伸)
- **OQ-3** · B-4-XenoDev runtime task 在 XenoDev 仓走 plan-start 还是直接 task ship — 由 XenoDev runtime 调度决定 · IDS 不越界

## §5 · Rollback plan

如果 XenoDev build 失败:
- **(a)** 回到 IDS 修 PRD,重跑 `/plan-start 006a-pM-v0.2`
- **(b)** 改 XenoDev spec(不改 IDS PRD),用 XenoDev 自己的修订机制
- **(c)** 起 forge v4(`/expert-forge 006`)重新审 v0.2 范围
- **(d)** XenoDev 产 hand-back 包(tags: `prd-revision-trigger`)写回 IDS,operator 在 IDS 跑 `/handback-review 006` 决议

## §6 · 本 hand-off 包补充上下文(IDS-side 推荐 XenoDev 读)

per v3 forge stage doc 已就绪可消费:

- **§W3 refactor-plan**(L194-296):按模块 + 3 wave 拆解 · XenoDev spec-writer 可作为 spec module 分段输入
- **§W5 next-dev-plan**(L369-419):phase 1+2+3 IDS side + phase X XenoDev side · XenoDev task-decomposer 可作为 DAG 骨架
- **§W2 decision-list**(L163-192):11 项 backlog 一一对一 verdict(N×9 / R×6 / cut-to-note×1)· 可作为 task 验收清单
- **MANIFEST-v0.2.md 字段固定 7 项**(详见 v3 stage doc §W3 模块 A):`source_path` / `target_path` / `source_sha256` / `target_sha256` / `copy_method` / `verification_command` / `operator_decision_source` · 每 wave append 一节

**关键硬规则**(R2 已收敛 · XenoDev 不可违):
- wave 2 cp 通过 ≠ ship-ready(只有 wave 3 跑通新 idea bootstrap + verify-all SHIP-READY 才能关闭 v0.2)
- B-4 协议改入 IDS v3 commit / B-4-XenoDev runtime 实装是 XenoDev 单独 task · 不越界
- B-3 IDS dir flock 不入 v0.2 主线(仅 SHARED-CONTRACT changelog 记 v0.2-note · 触发条件已列)
- bootstrap.sh 升级归 IDS bootstrap-kit(IDS=SSOT owner · XenoDev 只消费 bootstrap 结果)

## §7 · Cross-repo split 协议(v0.2 扩展 · SHARED-CONTRACT §6 隐含模式显式化)

### §7.1 · 为什么 v0.2 是跨仓 batch ship

v0.2 的 11 项 backlog 三类(mirror rebuild × 4 + protocol revision × 4 + lib bug × 3)按物理改动归属拆开,**至少 50% 的 task 改 IDS 仓而非 XenoDev 仓**:

- **IDS-only 改动**:protocol amendments(`framework/SHARED-CONTRACT.md` § 6 加 B-1 EXDEV + B-4-IDS verdict-evidence 协议语义)+ SSOT mirror(`framework/xenodev-bootstrap-kit/` 4 子树 + handback-validator/{templates,gen,score})+ `bootstrap.sh` 升级 + `MANIFEST-v0.2.md` append
- **XenoDev-only 改动**:lib bug 真路径修(`lib/handback-validator/scan-credentials.sh` C-1 / `gen-handback.sh` C-2 / `score-handback.sh` C-3 case F)+ B-4-XenoDev runtime 实装(`--ids-verdict-evidence` flag + REVIEW-LOG.md schema + verify-all consumption)
- **两仓都改**:B-2 event-schema enum 全复数(`event-schema.json` 在 XenoDev SSOT,IDS mirror 跟进 cp)

`workspace.working_repo` = IDS 仅描述 plan-start cwd · 不暗示所有 task 改 IDS。本扩展协议是 v0.2 forward HANDOFF 端显式化这个事实。

### §7.2 · target_repo 字段 enum

每条 spec task 在 frontmatter 必含 `target_repo: IDS | XenoDev`(枚举 2 值):

- `target_repo: IDS` — task 工作树在 IDS 仓 · 改动在 `/Users/admin/codes/ideababy_stroller/`
- `target_repo: XenoDev` — task 工作树在 XenoDev 仓 · 改动在 `/Users/admin/codes/XenoDev/`

跨仓 task(eg B-2 enum 5 文件 grep 一致)拆成 2 条 task,每条 `target_repo` 单值,不允许 hybrid。

### §7.3 · spec-writer 分派规则

spec-writer 拿到本 HANDOFF.md(`cross_repo_split: true`)后:

1. 按 v3 stage doc §W3 refactor-plan + §W5 dev plan 拆 wave 1/2/3 + phase X
2. 每条 task 显式标 `target_repo`(参见 §7.2 enum)
3. **default_target_repo: IDS** — 如某 task 归属歧义,默认 IDS;XenoDev-only 改动必须 spec 显式标
4. cross-repo task(eg mirror cp 涉及 source=XenoDev path / target=IDS path)的工作树在 IDS 仓(IDS=SSOT owner of mirror)· source path 是只读消费 · 不在 XenoDev 仓改

### §7.4 · task-decomposer 分派规则

task-decomposer 产 tasks/T*.md 时:

1. 每个 T*.md frontmatter 透传 `target_repo`(从 spec.md 该 task 段读)
2. 跨 wave 依赖关系按 §W5 dev plan(wave 1 → wave 2 → wave 3 顺序硬依赖)
3. phase X(XenoDev B-4-XenoDev runtime)可与 wave 2 并行(SHARED-CONTRACT §6 协议先 ship,实装后 hand-back 验证)

### §7.5 · parallel-builder worktree 路由

parallel-builder 读 task `target_repo`:

- `target_repo: IDS` → 在 IDS 仓 `projects/006-006a-pM-v0.2/<task-id>/` 起 worktree
- `target_repo: XenoDev` → 在 XenoDev 仓自己的 worktree dir 起 worktree

ship 后 hand-back 包统一写回 IDS `handback_target`(frontmatter `workspace.handback_target` · 双向 hand-off 通道不变)。

### §7.6 · Fallback(若 XenoDev spec-writer 不认得本扩展)

若 XenoDev spec-writer 解析 `cross_repo_split` 失败,fallback 行为:
- 退化为 `default_target_repo: IDS`(所有 task 默认 IDS · 不丢任务)
- spec.md 中 XenoDev-only 改动应该被 surface 为"⚠ 需 operator 决定 target_repo"标签 · 让 operator 临门拍板
- 不阻塞 spec 产出 · 但需在 spec §"Assumptions" 显式记录"fallback 触发原因"
