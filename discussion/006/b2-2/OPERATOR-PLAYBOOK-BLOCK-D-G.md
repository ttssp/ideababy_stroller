---
doc_type: operator-playbook
scope: B2.2 Block D-G(XenoDev 跨仓真跑)
generated: 2026-05-10
operator: Yashu Liu
prerequisite_state:
  ids_repo: /Users/admin/codes/ideababy_stroller (commit 423dcbd · A.7 + Round 5 决策完成)
  xenodev_repo: /Users/admin/codes/XenoDev (已 bootstrap · HANDOFF.md + PRD.md + .claude/ 在位)
  prd_in_use: 006a-pM(已 cp 到 XenoDev/PRD.md)
related_plan: ~/.claude/plans/plan-rosy-naur.md v11 Block D-G
---

# Operator Playbook · B2.2 Block D-G 跨仓真跑

> **目标**:首个真 PRD → 真 spec → 真 task → 真 ship → 真 hand-back → operator 评分 → 改 SHARED-CONTRACT §6 Status。
>
> **真跑判准**(plan v11 约束 3):用真 PRD + 真 spec(spec-writer 自动产)+ 真 task(task-decomposer 自动产)+ 真 code(parallel-builder TDD)+ 真 review(cross-model verdict ≠ BLOCK)+ 真 ship(merge XenoDev main)+ 真 hand-back(6 约束 validator PASS + 跨仓写回)。
>
> **不真跑就过不了 Block G 评分**(operator 自评示意跑 = 自欺,不能改 §6 Status: ACTIVE)。

## 当前仓状态(2026-05-10)

| 项 | 状态 |
|---|---|
| IDS 仓 | commit `423dcbd` · 34 commit ahead origin/main · A.7 + Round 5 决策完成 |
| XenoDev 仓 | 已 bootstrap · `AGENTS.md` + `CLAUDE.md` + `HANDOFF.md` + `PRD.md` + `.claude/` + `lib/` 在位 |
| HANDOFF.md PRD | 用 `006a-pM`(plan v11 假设的 `b2-2/PRD-v0/` 未生成,但 006a-pM 同样是真 PRD,可直接用) |
| 已派生 skill | XenoDev/.claude/skills/ 存在但未 verify 内容(Block D 第一步要 verify) |

## Step 0 · 起 XenoDev session(必须新 session,不要复用 IDS session)

```bash
# 在 macOS Terminal:
cd /Users/admin/codes/XenoDev
claude  # 启动新 Claude Code session,working dir = XenoDev
```

**为什么必须新 session**:
- IDS session 上下文是 ideababy_stroller 仓宪法
- XenoDev session 上下文是 XenoDev/AGENTS.md + CLAUDE.md(独立宪法)
- 跨仓 working dir 混淆 = `realpath .` 错 = hand-back 写错地方

## Step 1 · 在 XenoDev session 验现状(2 min)

复制粘贴给 XenoDev session 的第一句话:

```
我刚 cd 进 XenoDev 仓。读 AGENTS.md + CLAUDE.md + HANDOFF.md 三件套。
然后 ls .claude/skills/ 看已派生哪些 skill。
不要写代码,只汇报现状。
```

**预期回报**:
- AGENTS.md / CLAUDE.md / HANDOFF.md 全在
- `.claude/skills/` 列表(可能含 spec-writer / task-decomposer / parallel-builder 雏形,也可能空)

**判断**:
- 若 spec-writer skill 已存在 → 跳到 Step 2
- 若不存在 → 跳到 Step 1.5

## Step 1.5 · 派生 spec-writer + task-decomposer skill(若 Step 1 显示缺)

复制给 XenoDev session:

```
派生两个 skill 到 XenoDev/.claude/skills/:

1. spec-writer/SKILL.md
   - 输入:HANDOFF.md + PRD.md(prd_form 字段决定 spec 形态)
   - 输出:specs/<feature>/spec.md(7 元素 schema · 引 framework/spec-kit-evaluation.md)
   - prd_form 分派:
     - simple → 标准 7 元素 spec.md
     - phased → SLA / risks 按 phases 分段
     - composite → 顶层 spec.md 退化 INDEX + 每 module 单独 spec-<m>.md
     - v1-direct → SLA.md 顶部加 "Skip rationale"
   - 必须含 PPV(7th element)— 见 IDS framework/spec-kit-evaluation.md
   - cross-model review hook:产 spec.md 后必须跑 codex review,verdict ≠ BLOCK 才标 reviewed-by

2. task-decomposer/SKILL.md
   - 输入:specs/<feature>/spec.md(reviewed-by ≠ pending)
   - 输出:specs/<feature>/tasks/T<NNN>.md(每 task 含 verification + suggested executor model)
   - 同步产 specs/<feature>/dependency-graph.mmd

派生时参考 IDS 仓的范式(只读引用):
- /Users/admin/codes/ideababy_stroller/.claude/skills/spec-writer/SKILL.md(若存在)
- /Users/admin/codes/ideababy_stroller/.claude/skills/task-decomposer/SKILL.md(若存在)

派生完跑一次 self-test:
- 用 PRD.md 跑 spec-writer 产 specs/<feature>/spec.md
- 用产出的 spec 跑 task-decomposer 产至少 1 个 task
- 全过 → 进 Step 2;有 friction → 回报具体 friction 给 IDS session
```

**operator 跨仓 friction 反馈格式**(回 IDS session):

```
XenoDev Block D friction · <具体>
- file: <XenoDev 内路径>
- error: <粘贴 stderr verbatim>
- 我猜根因:<可选>
```

我在 IDS 端会评估是否需要修 plan-start v3.0 / spec-kit-evaluation 文档。

## Step 2 · 跑 spec-writer 产真 spec(~1-2h · XenoDev 内)

复制给 XenoDev session:

```
跑 spec-writer skill,输入 PRD.md + HANDOFF.md。
prd_form 字段在 HANDOFF.md frontmatter 里,按它分派。
产出 specs/<feature>/spec.md(7 元素全填,PPV 不能空)。

产出后跑 cross-model review:
- /codex:adversarial-review --wait(本仓内)
- 若 verdict 含 BLOCK / no-ship → 修 spec → 重跑
- verdict ≠ BLOCK → 在 spec.md frontmatter reviewed-by 字段写 "codex/<date>"

不要进 task 阶段,先把 spec ship 干净。
```

**完成标志**:
- `XenoDev/specs/<feature>/spec.md` 存在 + 7 元素 + PPV + reviewed-by ≠ pending
- spec.md 内容反映 PRD 真意图(operator 读一遍判断)

## Step 3 · 跑 task-decomposer 产真 task(~30min-1h · XenoDev 内)

复制给 XenoDev session:

```
跑 task-decomposer skill 输入 specs/<feature>/spec.md。
产出 specs/<feature>/tasks/T<NNN>.md + dependency-graph.mmd。

按 dependency-graph 选首 task(T001 = 入度 0 第一个)。
不要起 parallel-builder,先把 task 列表 ship 干净。
```

**完成标志**:
- `specs/<feature>/tasks/T001.md` 至少存在
- `dependency-graph.mmd` 存在
- T001 含 verification criteria + suggested executor model

## Step 4 · 跑 parallel-builder 起首 task → ship(~半天-1天 · XenoDev 内)

复制给 XenoDev session:

```
派生 parallel-builder skill(若 .claude/skills/parallel-builder/SKILL.md 不存在),
参考 IDS .claude/commands/parallel-kickoff.md 范式。

起 T001:
1. git worktree add projects/<feature>/T001 <new-branch>
2. cd 进 worktree
3. TDD:test → red → implement → green
4. 跑 /task-review verdict ≠ BLOCK
5. merge 回 main(squash 或 rebase 自选)
6. 删 worktree

ship 标志:T001 verification criteria 全过 + cross-model review verdict ≠ BLOCK + main 含 T001 commit
```

**friction 高发点**:
- worktree 路径冲突 → 改 projects/<feature>/T001 → projects/<feature>-T001
- TDD 写不出 red test(spec 太抽象) → 回 Step 2 修 spec,不绕过
- review BLOCK → 真修代码,不放水

## Step 5 · 产 hand-back 包 + 跨仓写回 IDS(~30min · XenoDev 内 + IDS 内)

复制给 XenoDev session:

```
T001 ship 完,产 hand-back 包:

1. 准备 hand-back .md(per IDS framework/SHARED-CONTRACT.md §6.3 schema):
   - frontmatter:handback_id / source_repo_path / build_repo_path / handback_target / 三标签(drift / prd-revision-trigger / practice-stats)
   - body:T001 ship 总结 + 学到的 friction + 给 IDS PRD 的反馈

2. 跑 lib/handback-validator/validate-handback.sh <hand-back.md> /Users/admin/codes/ideababy_stroller
   - 6 约束 PASS 才能写
   - 任一 FAIL → drop + stderr,修 hand-back 再跑

3. 写到 IDS:cp <hand-back.md> /Users/admin/codes/ideababy_stroller/discussion/006/handback/<ts>-<handback_id>.md
   (validator PASS 之后才 cp)
```

**operator 回 IDS session 跑 review**:

```bash
# 在 IDS session(working dir = ideababy_stroller):
ls discussion/006/handback/  # 应看到新 hand-back 文件
/handback-review 006
```

跟着 /handback-review skill 走完决议,append 到 `discussion/006/handback/HANDBACK-LOG.md`。

**完成标志**:
- `discussion/006/handback/<ts>-<handback_id>.md` 存在
- `discussion/006/handback/HANDBACK-LOG.md` 至少 1 条 operator 决议

## Step 6 · operator 主观评分 + Status 决策(~30min · IDS 内)

回 IDS session,write `discussion/006/b2-2/B2-2-RETROSPECTIVE.md`:

```markdown
---
doc_type: b2-2-retrospective
b2_2_completion_date: <today>
operator: Yashu Liu
---

# B2.2 retrospective · 首个真 PRD ship + hand-back 闭环

## 5 维度评分(1-10)

| # | 维度 | 评分 | 备注 |
|---|---|---|---|
| 1 | hand-back 包格式可读可消费 | <X>/10 | <evidence> |
| 2 | 6 约束 validator 错误信息清楚 | <X>/10 | <evidence> |
| 3 | workspace + source_repo_identity 在跨仓 friction | <X>/10 | <evidence> |
| 4 | §6.2.1 6 约束在真数据无 false positive/negative | <X>/10 | <evidence> |
| 5 | hand-off → ship → hand-back 闭环符合预期 | <X>/10 | <evidence> |

**总分 / 平均**:<sum>/50 · <avg>/10

## 决策

- ≥ 7/10 → 起 cutover sealing commit(SHARED-CONTRACT §6 Status: ACTIVE)
- < 7/10 → 起 forge v3 plan,本 plan 标 PARTIAL

## retrospective 总结

<operator 自由写>
```

**若 ≥ 7/10**:跑下面命令(我会在 IDS session 替你执行,你只需说"评分 X/10,改 Status: ACTIVE"):

```
edit framework/SHARED-CONTRACT.md:
- §6 顶部 `Status: ACTIVE-but-not-battle-tested` → `Status: ACTIVE`
- §6 顶部 `Promotion to ACTIVE pending` 段 → `Promoted to ACTIVE: <commit hash> · <date> · operator score <avg>/10`
- frontmatter `v2_status_note` 删除
- Changelog 加 v2.0 ACTIVE entry

commit:feat(framework)!: SHARED-CONTRACT v2.0 Status: ACTIVE — B2.2 hand-back round-trip verified(score <avg>/10)
```

**若 < 7/10**:本 plan 暂停 + 标 PARTIAL,起 forge v3 plan(operator 在 IDS 跑 `/expert-forge 006`)。

## 跨仓 communication 通道(operator 与我的协议)

**XenoDev session friction → 回 IDS session 报**(粘贴模板):

```
XenoDev Block <D|E|F> friction
- step: <step 编号>
- file: <XenoDev 内路径>
- error: <粘贴 stderr verbatim>
- 我已尝试: <可选>
```

**我会做**:
- 评估是不是 IDS 端 helper 缺(改 plan-start v3.0 / spec-kit-evaluation / handback-validator)
- 不是 IDS 端问题 → 给 XenoDev 内调试建议,你 cp 进 XenoDev session
- 是 IDS 端问题 → 我修 IDS,产 fix commit,你回 XenoDev 重试

**我不做**:
- 不直接读 / 写 XenoDev 仓内文件(权限边界 · operator 跨仓自跑)
- 不替你决定"这个 friction 该不该修"(operator 决,我评估)

## 失败回滚路径(plan v11 §"失败回滚路径")

| Block | 失败 | 回滚 |
|---|---|---|
| D spec-writer 派生卡 | XenoDev 内修 / 起 forge v3 | XenoDev 仓决,IDS 不动 |
| D spec-writer 跑卡 | 修 spec / 重跑 | XenoDev 内 |
| E parallel-builder 跑不通 review | 修 spec → 重派 task | XenoDev 内 |
| F 6 约束 validator 真数据 false positive/negative | 改 IDS validator | IDS fix commit |
| G 评分 < 7/10 | 起 forge v3,本 plan PARTIAL | IDS B2-2-RETROSPECTIVE.md |
| 整 B2.2 失败 | revert IDS B2.2 commit;XenoDev 自决保留/删 | A.5/A.6/A.7/Round5 全保留 |

## 估时合计

| Step | 时长 | 累计 |
|---|---|---|
| Step 0-1.5 起 XenoDev + 派生 skill | 1-2 h | 1-2 h |
| Step 2 spec | 1-2 h | 2-4 h |
| Step 3 task | 30 min - 1 h | 3-5 h |
| Step 4 ship | 半天 - 1 天 | 1-2 天 |
| Step 5 hand-back | 30 min | 1-2 天 |
| Step 6 评分 | 30 min | **1-2 天合计** |

operator 实际节奏可能拉长(skill 设计 / spec review loop / TDD),不强约束。

## 关键文件清单

### IDS 仓内必读(只读引用)

| 文件 | 用途 |
|---|---|
| `framework/SHARED-CONTRACT.md` §6 v2.0 | 协议 SSOT |
| `framework/SHARED-CONTRACT.md` §6.3 | hand-back schema |
| `framework/SHARED-CONTRACT.md` §6.2.1 | 6 约束定义 |
| `framework/spec-kit-evaluation.md` | 7 元素 spec schema 引证 |
| `framework/xenodev-bootstrap-kit/CLAUDE.md` | XenoDev 三件硬约束 |
| `discussion/006a-pM/PRD.md` | 真 PRD 源 |
| `discussion/006a-pM/L4/HANDOFF.md` | 真 hand-off 源 |

### XenoDev 仓内会产生

| 文件 | Step |
|---|---|
| `XenoDev/.claude/skills/spec-writer/SKILL.md` | 1.5 |
| `XenoDev/.claude/skills/task-decomposer/SKILL.md` | 1.5 |
| `XenoDev/.claude/skills/parallel-builder/SKILL.md` | 4 |
| `XenoDev/specs/<feature>/spec.md` | 2 |
| `XenoDev/specs/<feature>/tasks/T*.md` | 3 |
| `XenoDev/specs/<feature>/dependency-graph.mmd` | 3 |
| `XenoDev/projects/<feature>/T001/` | 4(merge 后删) |

### IDS 仓内会产生

| 文件 | Step |
|---|---|
| `discussion/006/handback/<ts>-<handback_id>.md` | 5 |
| `discussion/006/handback/HANDBACK-LOG.md` | 5 |
| `discussion/006/b2-2/B2-2-RETROSPECTIVE.md` | 6 |
| `framework/SHARED-CONTRACT.md`(§6 Status 改) | 6(若 ≥ 7/10) |

## OQ(本 playbook 不解决)

- **OQ-playbook-1**:XenoDev session 派生的 skill SKILL.md 字段 schema 应该多严?(operator 决 · 跑 spec-writer 时若 friction 暴露再说)
- **OQ-playbook-2**:T001 选哪个具体 task — operator 按 dependency-graph 第一个可执行
- **OQ-playbook-3**:cross-model review 用哪 model 组合 — operator 按 IDS .claude/commands/task-review.md 范式
- **OQ-playbook-4**:1 个 task ship 是否够"真" — operator 主观决,本 playbook 默认 1 task

## Changelog

- 2026-05-10 v1:initial · 整合 plan v11 Block D-G + framework/b2.1-dry-run-validation.md + xenodev-bootstrap-kit/CLAUDE.md + Round 5 决策日志后的状态
