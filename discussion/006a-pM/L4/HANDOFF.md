---
# §6.2 workspace schema 4 字段
workspace:
  source_repo: /Users/admin/codes/ideababy_stroller
  build_repo: /Users/admin/codes/XenoDev
  working_repo: /Users/admin/codes/ideababy_stroller
  handback_target: /Users/admin/codes/ideababy_stroller/discussion/006/handback/

# §3.1 source_repo_identity 字段(IDS forward 端填入,XenoDev hand-back producer 按 §6.2.1 约束 3 三模式比对)
source_repo_identity:
  expected_remote_url: git@github.com:ttssp/ideababy_stroller.git
  repo_marker: "# Idea Incubator — Project C"
  git_common_dir_hash: 647b0db7b4d47318

# Hand-off metadata
prd_fork_id: 006a-pM
discussion_id: "006"
prd_form: simple
phases: null
modules: null
module_forms: null
critical_path_module: null
skip_rationale: null

handed_off_at: 2026-05-10T08:04:37Z
prd_source: /Users/admin/codes/ideababy_stroller/discussion/006a-pM/PRD.md
shared_contract_version_honored: 2.0
---

# Hand-off · 006a-pM → XenoDev (per SHARED-CONTRACT §6 v2.0)

**Handed off at**: 2026-05-10T08:04:37Z
**PRD source**: /Users/admin/codes/ideababy_stroller/discussion/006a-pM/PRD.md
**Build repo**: /Users/admin/codes/XenoDev
**Workspace**: 见 frontmatter `workspace:` 块(§6.2 4 字段全填)
**Source repo identity**: 见 frontmatter `source_repo_identity:` 块(XenoDev 写 hand-back 前必须按 §6.2.1 约束 3 校验)
**SHARED-CONTRACT version honored**: 2.0

## §1 · 给 XenoDev operator 的指令

operator 切到 build_repo 后:

1. `cd /Users/admin/codes/XenoDev`
2. 读本 HANDOFF.md(全文)+ 引用的 PRD.md(`/Users/admin/codes/ideababy_stroller/discussion/006a-pM/PRD.md`)
3. 在 XenoDev session 触发 XenoDev 自带的 spec-writer(per XenoDev AGENTS.md;**不**调 IDS 的 spec-writer subagent — XenoDev 派生自己的)
4. spec-writer 产 XenoDev 内部 spec.md(7 元素 schema + PPV 第 7 元素;具体格式见 XenoDev `templates/spec.template.md`,Block D 起跑时实装)
5. XenoDev task-decomposer 产 tasks/T*.md
6. parallel-builder 跑 task,quality gate 在 XenoDev 内部决议
7. 每个 task ship 后 XenoDev 产 hand-back 包(per §6.3 schema)写回 IDS `/Users/admin/codes/ideababy_stroller/discussion/006/handback/`

## §2 · PRD-form 透传(XenoDev spec-writer 分派依据)

`prd_form: simple`(详见 frontmatter)

- ✅ **simple** → 标准 7 文件输出(本 PRD 走此分支)
- phased → SLA / risks 按 PRD `**Phases**` 数组分段
- composite → 顶层 spec.md 退化为 INDEX,**额外**为每 module 输出 spec-<m>.md
- v1-direct → SLA.md 顶部加 §'Skip rationale'

## §3 · §6.2.1 6 约束自检契约(XenoDev producer 写 hand-back 前必走)

per `framework/SHARED-CONTRACT.md` §6.2.1,XenoDev 产 hand-back 包写入 `/Users/admin/codes/ideababy_stroller/discussion/006/handback/` 前,必须按 6 约束自检:

1. **canonical-path containment**(realpath prefix 校验)
2. **symlink reject**(路径任一段是 symlink 即拒)
3. **repo identity check**(三模式:remote / no-remote / hash-only,任一 PASS 即满足;**本 hand-off 包 source_repo_identity 已填三字段全套**,producer 按优先级跑)
4. **id consistency check**(三处 id 严格一致)
5. **id 字符集 + filename basename + final-path containment**(OWASP path traversal 防御)
6. **hard-fail**(任一约束失败,producer 不写 / consumer 不读)

任一失败 = `Drop`(不写文件,不创目录,只 stderr)。

**实装位置**(B2.1 已落):`framework/xenodev-bootstrap-kit/handback-validator/validate-handback.sh`(operator 跑 bootstrap.sh 后会 cp 到 XenoDev `lib/handback-validator/`)。XenoDev producer 端调用范式:

```bash
bash lib/handback-validator/validate-handback.sh "$DRAFT_HANDBACK" "/Users/admin/codes/ideababy_stroller" --mode=producer
# exit 0 → cp 到 handback_target;exit 1 → drop + stderr
```

## §4 · Open questions for build phase

(IDS PRD `discussion/006a-pM/PRD.md` 中**关于 build 路径选择**的 OQ 在此承载;XenoDev build 自然遇到时再解决,不污染 XenoDev spec frozen)

- **OQ-1**(IDS PRD §Open questions OQ-1):成功指标 N(连续 idea 数)和干预率 X 的具体阈值 — 需 XenoDev 跑 ≥3 真 idea / 30 task 后回看(v0.2 note 2)
- **OQ-2**(IDS PRD §Open questions OQ-2):Spec Kit 0.8.7 schema 与 PPV 第 7 元素兼容度 — XenoDev 第一个真 PRD(本 PRD)起 sdd-workflow 时回看(v0.2 note 1;`framework/spec-kit-evaluation.md` 已预答 adapter 模式)
- **OQ-3**(IDS PRD §Open questions OQ-3):Small → Medium 升级触发器精确判准 — XenoDev 跑过 ≥1 Medium 项目后回看(v0.2 note 5)

## §5 · Rollback plan

如果 XenoDev build 失败:
- (a) 回到 IDS 修 PRD(`discussion/006a-pM/PRD.md`),重跑 `/plan-start 006a-pM`
- (b) 改 XenoDev spec(不改 IDS PRD),用 XenoDev 自己的修订机制
- (c) 起 forge v3 重新审整个 idea(IDS 仓 `/expert-forge 006`)
- (d) XenoDev 产 hand-back 包(tags: `prd-revision-trigger`)写回 IDS,operator 在 IDS 跑 `/handback-review 006` 决议
