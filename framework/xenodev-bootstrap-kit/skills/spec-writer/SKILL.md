---
name: spec-writer
description: 把 IDS 喂入的 HANDOFF.md + PRD.md 转成 XenoDev 7 元素 spec 包(IDS 6 元素 + PPV 第 7)。Load 当 operator 在 XenoDev 仓内首次拿到 hand-off、需要起 specs/<feature>/spec.md、或 PRD 修订需要重派 spec 时。**不**调 IDS 的 spec-writer subagent — 本 skill 是 XenoDev 自派生(per AGENTS.md §5 + framework/xenodev-spec-writer-derivation-guide.md)。
inspired_by: GitHub Spec Kit 0.8.7 (concept-level only, no code copied) + IDS sdd-workflow 6 元素契约(adapter 模式,per ideababy_stroller/framework/spec-kit-evaluation.md)
schema_version: 0.1
schema_extends: SK 0.8.7 7 元素 + XenoDev §7 PPV(Production Path Verification,防 mock-pass-prod-fail)
tools: Read, Write, Edit, Glob, Grep, Bash
model: opus
isolation: inline
disable-model-invocation: false
---

# spec-writer · XenoDev L4 自派生

> **结论先**:从 HANDOFF.md 读 prd_form,按 4 分支拼 7 元素 spec.md;产完跑 codex adversarial-review;verdict ≠ BLOCK 才标 reviewed-by。

## 0 · 核心契约

- **输入**:`HANDOFF.md`(workspace + source_repo_identity + prd_form)+ `PRD.md`(IDS L3 产出)
- **输出**:`specs/<feature>/spec.md` + 配套文件(architecture/SLA/risks/non-goals,按 prd_form 取舍)
- **feature naming**:`<discussion_id>` 或 `<prd_fork_id>`,直接取 HANDOFF.md frontmatter `discussion_id` / `prd_fork_id`(优先 fork_id,如 `006a-pM`)
- **硬约束**:7 元素一个不能少;PPV 必须含 ≥1 条 P_i 真路径 + 可执行验证命令
- **失败模式拒收**:不写 spec / 只写 mock-pass-prod-fail 样本 → status 不能升 frozen,后续 task-decomposer 拒输入

## 1 · Phase 0 — 读入 + 分派

### 1.1 必读

```
HANDOFF.md           # workspace 4 字段 / source_repo_identity / prd_form / discussion_id / prd_fork_id
PRD.md               # operator 从 IDS cp 进来的(本仓根)
```

### 1.2 prd_form 4 分派(强制)

读 HANDOFF.md frontmatter `prd_form` 字段,按以下分派:

| prd_form | spec.md 形态 | 配套文件 | Skip 字段 |
|---|---|---|---|
| **simple** | 标准 7 元素 spec.md(单文件)| architecture / SLA / risks / non-goals 各 1 | — |
| **phased** | 标准 7 元素,但 §SLA / §risks / §verification 按 PRD `**Phases**` 数组分段;每 phase 一节 | SLA.md / risks.md 强制按 phase 分子节 | — |
| **composite** | 顶层 spec.md **退化为 INDEX**(只列 modules + 跨 module 依赖);每 module 单独 `spec-<m>.md`(7 元素全展开,§5 §6 仅 module 范围)| 顶层 architecture.md 描述 module 间通信;每 module 一份 SLA / risks | — |
| **v1-direct** | 标准 7 元素;**SLA.md 顶部加 §"Skip rationale"**(说明为什么 v0.1 直跳 v1)| SLA.md 多 §"Skip rationale" 一节,引 PRD evidence | — |

未列 prd_form / 字段缺失 → **hard-fail**(`echo "ERR: HANDOFF.md prd_form 缺失或非法值: $val" >&2; exit 1`);不试图 default。

## 2 · Phase 1 — 7 元素 spec.md 起草

### 2.1 §1-§6(同 IDS 6 元素,直接派生 per derivation-guide §"7 元素 spec contract" 维度 1-6)

| # | 元素 | 必含字段 | 反模式 |
|---|---|---|---|
| 1 | **Outcomes** | 用户/业务可观察结果,编号 O1/O2…,带数字目标(p95 / SLA / 比例 等)| 不是 feature 列表;不是技术决策 |
| 2 | **Scope Boundaries** | §2.1 IN(v0.1 必落)/ §2.2 OUT(显式 non-goals,带 evidence)| OUT 比 IN 重要;空 OUT 直接拒 |
| 3 | **Constraints** | 表格:# / Constraint / Source / Rigidity(Hard/Soft)| 不可写"必须可扩展"等无量化形容词 |
| 4 | **Prior Decisions** | 表格:# / Decision / Source(必引 PRD/forge/conc 节号)| 不能引不可追溯;agents 不可 re-litigate |
| 5 | **Task Breakdown** | 仅 phase 名 + 跨 phase 依赖(细节给 task-decomposer)| 不是 task 列表;不写实现 |
| 6 | **Verification Criteria** | 每 Outcome 一行:可执行测试命令 / 可量化指标 / 人审 checkbox | 不可写"works end-to-end" |

### 2.2 §7 — Production Path Verification(PPV,XenoDev 自加,**不可省**)

per `framework/xenodev-spec-writer-derivation-guide.md` §"§7 PPV 最小要求" + 灵感:autodev_pipe V4 stroller idea004 12 routes 404 案例。

最小要求:
- 至少 **1 条 P_i**,描述"真路径起点 → 终点 + 必经环节 + 可执行验证命令"
- 起点 = 真实入口(CLI 命令 / HTTP route / file path / cron tick),非 mock
- 终点 = 真实持久化 / 真实写回(disk / DB / hand-back target),非 stdout
- 必经环节 = 中间所有 layer / module / hook,**逐个列出,任一被 mock 即不算 PPV**
- 验证命令 = `bash` / `pnpm test` / `curl`,operator 可直接 paste 跑

PPV 表格 schema:
```markdown
## §7 Production Path Verification

| P# | 起点(真路径)| 必经环节 | 终点(真持久化)| 验证命令 |
|----|---|---|---|---|
| P1 | `cd XenoDev && bash lib/handback-validator/validate-handback.sh fixture.md /Users/admin/codes/ideababy_stroller --mode=producer` | realpath check → symlink reject → repo identity 三模式 → id consistency → OWASP path → hard-fail | `discussion/006/handback/<ts>-006.md` 真文件存在 OR exit 1 + stderr | `bash lib/handback-validator/validate-handback.sh test-fixtures/valid/sample.md /Users/admin/codes/ideababy_stroller --mode=producer && ls /Users/admin/codes/ideababy_stroller/discussion/006/handback/<ts>-006.md` |

**反 PPV(直接拒)**:
- ❌ "通过 unit test 即算 PPV"(unit test mock 一切,不验真路径)
- ❌ "通过 mock 命令即算"(必经环节有 mock 就不算)
- ❌ "log 显示成功即算"(终点必须可观测的真持久化)
```

## 3 · Phase 2 — cross-model review(强约束 hook)

per AGENTS.md §6 + CLAUDE.md "Pre-merge review mandatory":**spec.md 产完必须跑 codex adversarial-review,verdict ≠ BLOCK 才能标 reviewed-by**。

### 3.1 跑 codex(本仓 codex 插件入口 = node mjs)

> **T005 round 2-4 amendment 2026-05-24**:不要硬编码 codex 版本号。用 `find` + `sort -V` 取语义版本最新装机版本(防 codex 升级删 1.0.3 → SKILL 路径死但 link test 还说"健康";`find | head -1` 取的是 shell glob 顺序而非 semver 顺序 · per round 3 codex P2 finding)。

```bash
cd /Users/admin/codes/XenoDev
# 按语义版本取最新(sort -V) · macOS 默认 sort 支持 -V
CODEX_MJS=$(find /Users/admin/.claude/plugins/cache/openai-codex/codex/*/scripts/codex-companion.mjs 2>/dev/null | sort -V | tail -1)
node "$CODEX_MJS" \
  adversarial-review --wait --scope working-tree \
  "review specs/<feature>/spec.md against XenoDev 7 元素契约(IDS 6 + PPV);
   重点: PPV 是否真路径 / Outcomes 是否量化 / OUT 是否覆盖 / Constraints 是否带 Rigidity / Prior Decisions 是否带 source"
```

- `--wait` 必加(单文件 review,前台跑,< 90s)
- `--scope working-tree` 必加(spec 是新 untracked 文件)
- focus 文本不删
- `CODEX_MJS` 用 `find | sort -V | tail -1` 取 semver 最新(per T005 round 2-3 codex P2 findings)

### 3.2 verdict 解析

codex stdout 通常含 `verdict:` / `BLOCK` / `FOLLOW-UP` / `NO BLOCKING ISSUES`:

| verdict | 处理 | spec.md frontmatter `reviewed-by` |
|---|---|---|
| **NO BLOCKING ISSUES** / 无 BLOCK 标签 | PASS | `reviewed-by: codex@<YYYY-MM-DD>` |
| **FOLLOW-UP** | 把 finding 写 `risks.md` 或 `open-questions.md`;spec 本身可标 reviewed | `reviewed-by: codex@<YYYY-MM-DD> (with-followups)` |
| **BLOCK** | **不**标 reviewed-by;按 finding 改 spec → 重跑(最多 4 轮 per IDS sdd-workflow 范式)| 留 `reviewed-by: pending` |
| 4 轮仍 BLOCK | hard-stop,operator 决策(改 PRD / 起 IDS forge / scope 缩)| 留 `reviewed-by: blocked-after-4-rounds` |

### 3.3 frontmatter 写回(spec.md 顶部)

```yaml
---
feature: 006a-pM
prd_source: PRD.md
handoff_source: HANDOFF.md
prd_form: simple
schema_version: 0.1
status: review | frozen
reviewed-by: pending | codex@2026-05-10 | codex@2026-05-10 (with-followups)
ppv_count: 1            # P_i 条数,< 1 拒 frozen
created: 2026-05-10
---
```

`status: frozen` 仅在 `reviewed-by ≠ pending` 且 `ppv_count ≥ 1` 时允许。task-decomposer 读 status,frozen 才接。

## 4 · Phase 3 — 配套文件(按 prd_form 取舍)

| 文件 | simple | phased | composite | v1-direct |
|---|---|---|---|---|
| `spec.md` | ✅ 7 元素 | ✅ 7 元素 + phase 分段 | ✅ INDEX(只列 module)| ✅ 7 元素 |
| `spec-<m>.md` per module | — | — | ✅ 每 module 一份 | — |
| `architecture.md` | ✅ C4 L1 | ✅ C4 L1,phase 分层 | ✅ module 间通信图 | ✅ C4 L1 |
| `SLA.md` | ✅ v0.1 一节 | ✅ 每 phase 一节 | ✅ 每 module 一节 | ✅ **顶部加 "Skip rationale"** + v1 节 |
| `risks.md` | ✅ 标准 6 类 | ✅ 每 phase 风险 + 全局 | ✅ 每 module 风险 + 跨 module | ✅ 标准 6 类 + skip 风险专节 |
| `non-goals.md` | ✅ | ✅ | ✅ | ✅ |
| `compliance.md` | optional | optional | optional | optional |

## 5 · Anti-patterns(直接拒)

per IDS sdd-workflow 范式 + XenoDev 加:

1. **Spec-as-docstring** — spec 写代码 docstring → 拒
2. **"我们再看看"spec** — 边界写"按需扩展"/"足够安全"→ 拒
3. **Auto-generated from repo** — LLM 全自动产 spec → 拒(per ETH 2026 研究 -0.5 ~ -2% 成功率)
4. **Frozen forever** — spec 一锁不改 → 反;但每次改必须 explicit commit + operator 审
5. **空 non-goals** — agents 默认扩张,non-goals 是唯一刹车
6. **Verification = "it works"** — 必须可跑命令 / 量化 / 签字
7. **PPV 缺**(XenoDev 加)— §7 没 P_i 或 P_i 含 mock → 拒
8. **prd_form 默认** — HANDOFF 没 prd_form 不试图 default,hard-fail
9. **review 跳过** — `reviewed-by: pending` 也提交 task-decomposer → 拒

## 6 · Templates(骨架,operator 在 spec 里展开)

### 6.1 spec.md 骨架(simple form)

```markdown
---
feature: <id>
prd_source: PRD.md
handoff_source: HANDOFF.md
prd_form: simple
schema_version: 0.1
status: review
reviewed-by: pending
ppv_count: 0
created: <ISO-date>
---

# Spec — <feature> · <title>

**Version**: 0.1  **Updated**: <ISO>  **Source**: PRD.md + HANDOFF.md

## §1 Outcomes
- O1 ...(带数字)
- O2 ...

## §2 Scope Boundaries
### §2.1 In scope for v0.1
### §2.2 Explicitly OUT of scope(带 evidence)

## §3 Constraints
| # | Constraint | Source | Rigidity |
|---|---|---|---|

## §4 Prior Decisions
| # | Decision | Source(PRD §x / forge §y / conc §z) |
|---|---|---|

## §5 Task Breakdown(phase only)
- Phase 0: Foundation
- Phase 1: Core
- Phase 2: Integration
- Phase 3: Polish

## §6 Verification Criteria
| Outcome | Verification(可跑命令 / 量化 / 签字) |
|---|---|

## §7 Production Path Verification(PPV)
| P# | 起点 | 必经环节 | 终点 | 验证命令 |
|---|---|---|---|---|

## Glossary
## Open Questions for Operator
```

### 6.2 spec.md 骨架(phased / composite / v1-direct)

- **phased**:§5 §6 §SLA-emb 加子节 `### v0.1` / `### v0.2` / ...
- **composite**:删 §1-§7 详情,只留 `## Modules` 列表 + `## Cross-module dependencies` 图;每 module 一份 `spec-<m>.md`(用 simple 骨架填)
- **v1-direct**:同 simple 骨架;但 SLA.md 必须有 §"Skip rationale"(为什么 v0.1 直跳 v1,引 PRD evidence)

## 7 · 完成 checklist(operator 自审)

- [ ] HANDOFF.md `prd_form` 已读,分派分支已选
- [ ] §1-§6 全部填写,无 placeholder
- [ ] §7 PPV ≥ 1 条 P_i,起点/必经/终点/验证 4 列齐
- [ ] 配套文件按 prd_form 表落齐
- [ ] codex adversarial-review 跑过,stdout 已存(可附 `review-log/` 或贴 PR 描述)
- [ ] verdict ≠ BLOCK,frontmatter `reviewed-by` 标了 `codex@<date>`
- [ ] `status: frozen` 写入 frontmatter
- [ ] git status 干净 / 文件已 stage(不主动 commit,等 operator)

## 8 · Failure mode + escalation

| 症状 | 处理 |
|---|---|
| HANDOFF.md prd_form 缺 | hard-fail,echo stderr,不试图猜 |
| codex 4 轮仍 BLOCK | 留 `reviewed-by: blocked-after-4-rounds`,operator 决策(改 PRD / 起 IDS forge) |
| codex 不可用(node 报错 / 插件 missing)| stderr 真粘报错;不静默 mark reviewed |
| spec.md 写完发现 PRD 自相矛盾 | 不试图 patch,产 hand-back 包标 `prd-revision-trigger`(Block E 的事) |
| 7 元素任一缺 | 拒 frozen;status 留 `review` |

## 9 · 与上下游的关系

- **上游**:IDS `/plan-start` v3.0 → `discussion/<id>/<prd>/L4/HANDOFF.md`(per SHARED-CONTRACT §6 v2.0)
- **下游**:`task-decomposer` skill 读 frozen spec 产 tasks/T*.md(本 skill 完成 = 它的输入就绪)
- **跨仓**:本 skill **不**写回 IDS;hand-back 是 ship 后的事,由 parallel-builder 收尾产

---

**Provenance**:
- `inspired_by` GitHub Spec Kit 0.8.7(adapter 模式,per `ideababy_stroller/framework/spec-kit-evaluation.md`)
- 6 元素契约骨架参考 `ideababy_stroller/.claude/skills/sdd-workflow/SKILL.md`
- §7 PPV 来自 `ideababy_stroller/framework/xenodev-spec-writer-derivation-guide.md`
- prd_form 4 分派 schema 来自 `ideababy_stroller/framework/SHARED-CONTRACT.md` §6 + IDS `templates/PRD-{simple,phased,composite,v1-direct}.md` 4 模板
