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
