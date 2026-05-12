---
doc_type: operator-playbook
scope: XenoDev 跨仓真跑(L4 hand-off → hand-back 全流程 · generic 跨 batch 模板)
generated: 2026-05-12
upstream: plan-rosy-naur v12 B 件 5 · plan v0.2-global 件 2.1
source: discussion/006/b2-2/OPERATOR-PLAYBOOK-BLOCK-D-G.md (006 batch v1 · 历史 evidence · 不删)
parameters:
  IDS_REPO: /Users/admin/codes/ideababy_stroller
  XENODEV_REPO: /Users/admin/codes/XenoDev
  BATCH_ID: <e.g. 006 / 004 / 008>           # discussion 顶层 id
  PRD_FORK_ID: <e.g. 006a-pM / 004-pB / 008a-pA>  # PRD fork id
  IDS_SNAPSHOT_COMMIT: <e.g. 423dcbd>        # 本次跑起跑时 IDS 仓 HEAD commit
related_plan: ~/.claude/plans/plan-rosy-naur.md (current sub-plan version)
ids_reference_files:
  - framework/SHARED-CONTRACT.md
  - framework/task-decomposer-derivation-guide.md
  - framework/xenodev-parallel-builder-derivation-guide.md
  - framework/xenodev-spec-writer-derivation-guide.md
  - framework/xenodev-bootstrap-kit/handback-validator/test-fixtures/README.md
---

# Operator Playbook · XenoDev 跨仓真跑(generic · 跨 batch 模板)

## §0 · 背景(scope · 与 006 v1 关系)

本 playbook 是 plan v0.2-global 件 2.1 落地 · F1 fix(B2.2 RETRO §1.1 task-review 命名 deviation) · generic 化 006 batch v1 playbook(`discussion/006/b2-2/OPERATOR-PLAYBOOK-BLOCK-D-G.md` 338 行 · 历史 evidence 不删)。

- **scope IN**:跨 batch 复用的 XenoDev session 真跑流程(Step 0-6) + 派生 skill schema + cross-model review 规则 + hand-back 闭环 + 评分决策
- **scope OUT**:不替 operator 决具体 batch 起跑节奏 · 不替具体 PRD-form 分派(由 spec-writer derivation guide 决) · 不替 model 选择阈值(由 task-decomposer derivation guide 决)

**目标**:真 PRD → 真 spec → 真 task → 真 ship → 真 hand-back → operator 评分 → 改 SHARED-CONTRACT §6 Status(若首跑) / 或继续 hand-back round-trip(后续 batch)。

**真跑判准**:用真 PRD + 真 spec(spec-writer 自动产)+ 真 task(task-decomposer 自动产)+ 真 code(parallel-builder TDD)+ 真 review(cross-model verdict ≠ BLOCK)+ 真 ship(merge XenoDev main)+ 真 hand-back(6 约束 validator PASS + 跨仓写回)。

## §1 · 当前仓状态(自填模板)

| 项 | 状态 |
|---|---|
| IDS 仓 | commit `${IDS_SNAPSHOT_COMMIT}` · `git rev-parse HEAD` 自填 |
| XenoDev 仓 | 已 bootstrap · `AGENTS.md` + `CLAUDE.md` + `HANDOFF.md` + `PRD.md` + `.claude/` + `lib/` 在位 |
| HANDOFF.md PRD | 用 `${PRD_FORK_ID}`(从 IDS `discussion/<root>/<parent-fork>/${PRD_FORK_ID}/L4/HANDOFF.md` 引) |
| 已派生 skill | XenoDev/.claude/skills/(Step 1 verify · spec-writer / task-decomposer / parallel-builder 三件套) |

## §2 · Step 0 · 起 XenoDev session(必须新 session)

```bash
cd ${XENODEV_REPO}
claude  # 启动新 Claude Code session · working dir = XenoDev
```

**为什么必须新 session**:
- IDS session 上下文是 ideababy_stroller 仓宪法
- XenoDev session 上下文是 XenoDev/AGENTS.md + CLAUDE.md(独立宪法)
- 跨仓 working dir 混淆 = `realpath .` 错 = hand-back 写错地方

## §3 · Step 1 · 在 XenoDev session 验现状(2 min)

复制粘贴给 XenoDev session 的第一句话:

```
我刚 cd 进 XenoDev 仓。读 AGENTS.md + CLAUDE.md + HANDOFF.md 三件套。
然后 ls .claude/skills/ 看已派生哪些 skill。
不要写代码,只汇报现状。
```

**预期回报**:
- AGENTS.md / CLAUDE.md / HANDOFF.md 全在
- `.claude/skills/` 列表(spec-writer / task-decomposer / parallel-builder · 三件套至少一个 · 也可能空)

**判断**:
- 若 spec-writer / task-decomposer / parallel-builder 全在 → 跳到 Step 2
- 若任一缺 → 跳到 Step 1.5

## §4 · Step 1.5 · 派生 skill(若缺)

复制给 XenoDev session:

```
派生三件套 skill 到 XenoDev/.claude/skills/:

1. spec-writer/SKILL.md
   - 输入:HANDOFF.md + PRD.md(prd_form 字段决定 spec 形态)
   - 输出:specs/<feature>/spec.md(7 元素 schema · 引 framework/spec-kit-evaluation.md)
   - prd_form 分派:simple / phased / composite / v1-direct(见 IDS framework/xenodev-spec-writer-derivation-guide.md)
   - 必须含 PPV(7th element)
   - cross-model review hook:产 spec.md 后必须跑 codex review · verdict ≠ BLOCK 才标 reviewed-by

2. task-decomposer/SKILL.md
   - 输入:specs/<feature>/spec.md(reviewed-by ≠ pending)
   - 输出:specs/<feature>/tasks/T<NNN>.md + dependency-graph.mmd
   - **audit checklist A1-A4 必跑**(per IDS framework/task-decomposer-derivation-guide.md §2):
     - A1 file_domain 现状 audit(build runtime src 状态 vs file_domain 假设 · D-baseline-1 模式)
     - A2 task 依赖图入度 audit(DAG 5 铁律)
     - A3 recommended_model audit(opus/sonnet 选)
     - A4 phased build 拆 task 特殊审查

3. parallel-builder/SKILL.md
   - 输入:specs/<feature>/tasks/T<NNN>.md
   - 输出:ship 到 XenoDev main(squash commit)+ hand-back 包
   - **§9 checklist [GATE]/[AUDIT] 区分**(per IDS framework/xenodev-parallel-builder-derivation-guide.md §2)
   - **events.jsonl 写入 [GATE]**(per §3 升 hard-fail · 消灭 side-effect 语义)

派生时只读引用 IDS 仓 framework/ 内三派生 guide(只读 · 不直接 cp):
- ${IDS_REPO}/framework/xenodev-spec-writer-derivation-guide.md
- ${IDS_REPO}/framework/task-decomposer-derivation-guide.md
- ${IDS_REPO}/framework/xenodev-parallel-builder-derivation-guide.md

派生完跑一次 self-test:
- 用 PRD.md 跑 spec-writer 产 specs/<feature>/spec.md
- 用产出的 spec 跑 task-decomposer 产至少 1 个 task
- 全过 → 进 Step 2;有 friction → 回报具体 friction 给 IDS session(§跨仓 communication 模板)
```

### §4.1 · F1 fix · task-review command 等价物声明(v2 加 · 关键改动)

**问题**(B2.2 RETRO §1.1 L56-61 真案例):playbook v1 L155 字面要求 `/task-review verdict ≠ BLOCK` · 但 `/task-review` slash command 在 IDS 仓 · XenoDev 仓无 `.claude/commands/` 目录 · 实际跑 codex adversarial-review(FU-001 6 轮 / T001 5 轮 / FU-002 2 轮) · **实质同效**(cross-model + verdict-gate + 失败回 fix) · 命名差异。

**operator 二选一**:

**方案 A · 真派生 /task-review 到 XenoDev**(命名完全对齐):
```
派生 XenoDev/.claude/commands/task-review.md(参考 IDS .claude/commands/task-review.md)
工作流:agent 跑 codex 或 opus cross-model review · verdict ≠ BLOCK 才 ship
```

**方案 B · 声明 codex adversarial-review 是 /task-review 等价物**(命名差异 · 同语义):
```
在 XenoDev/AGENTS.md / SKILL.md 显式注:
"XenoDev session 内 /task-review 等价于 codex adversarial-review · cross-model + verdict-gate + 失败回 fix"
```

**默认推荐**(per RETRO operator 拍):**选 B**(已是 XenoDev 实际跑法 · 0 改动 + 加 doc 1 行) · 选 A 适合需统一 slash command 体验时。

Evidence:`discussion/006/b2-2/B2-2-RETROSPECTIVE.md` §1.1 L56-61 + §4.3 F1 L168。

### §4.2 · operator 跨仓 friction 反馈格式(回 IDS session)

```
XenoDev Block <D|E|F> friction · <具体>
- file: <XenoDev 内路径>
- error: <粘贴 stderr verbatim>
- 我猜根因:<可选>
```

我在 IDS 端会评估是否需修 plan-start v3.0 / spec-kit-evaluation / 三派生 guide。

## §5 · Step 2 · 跑 spec-writer 产真 spec(~1-2h · XenoDev 内)

复制给 XenoDev session:

```
跑 spec-writer skill · 输入 PRD.md + HANDOFF.md。
prd_form 字段在 HANDOFF.md frontmatter 里 · 按它分派。
产出 specs/<feature>/spec.md(7 元素全填 · PPV 不能空)。

产出后跑 cross-model review(per §4.1 方案 A 或 B):
- /codex:adversarial-review --wait(本仓内 · 等价 /task-review)
- 若 verdict 含 BLOCK / no-ship → 修 spec → 重跑
- verdict ≠ BLOCK → 在 spec.md frontmatter reviewed-by 字段写 "codex/<date>"

不要进 task 阶段 · 先把 spec ship 干净。
```

**完成标志**:
- `XenoDev/specs/<feature>/spec.md` 存在 + 7 元素 + PPV + reviewed-by ≠ pending
- spec.md 内容反映 PRD 真意图(operator 读一遍判断)

## §6 · Step 3 · 跑 task-decomposer 产真 task(~30min-1h)

复制给 XenoDev session:

```
跑 task-decomposer skill 输入 specs/<feature>/spec.md。
产出 specs/<feature>/tasks/T<NNN>.md + dependency-graph.mmd。

**audit checklist 必跑**(per ${IDS_REPO}/framework/task-decomposer-derivation-guide.md §2):
- A1 file_domain 现状 audit:build runtime 仓内 file_domain 路径是否已存在?src 是否在源仓只读?跨仓 mass cp 是否前置必要?
- A2 task 依赖图入度 audit:本 task 的 blockedBy 是否真在 DAG 中存在?入度 = 0 task 是否 ≥ 1?
- A3 recommended_model audit:high-risk(LOC ≥ 200 / 跨多 module)→ opus · low-risk → sonnet
- A4 phased build 拆 task 特殊审查:PRD-form = phased 时 baseline cp 是否前置 schedule?

任一 audit FAIL → 选 spec-gap recovery 路径(per task-decomposer guide §4 三选一矩阵):
- 拆 task(轻量 · operator plan-mode)
- 跨仓 mass cp(中等 · 11k LOC 量级)
- forge amendment(重 · ${IDS_REPO} `/expert-forge`)

按 dependency-graph 选首 task(T001 = 入度 0 第一个)。
```

**完成标志**:
- `specs/<feature>/tasks/T001.md` 至少存在
- `dependency-graph.mmd` 存在
- T001 含 verification criteria + suggested executor model + audit checklist 全 PASS
- task-decomposer guide piggy-back reference(本 sub-plan 件 2.6 · IDS commit `0d51595`)

## §7 · Step 4 · 跑 parallel-builder 起首 task → ship(~半天-1天)

复制给 XenoDev session:

```
派生 parallel-builder skill(若 .claude/skills/parallel-builder/SKILL.md 不存在)
参考 ${IDS_REPO}/framework/xenodev-parallel-builder-derivation-guide.md。

**SKILL §9 checklist [GATE]/[AUDIT] 区分**(per guide §2):
- [GATE] producer/consumer validator / tests / lint / coverage / git status / events.jsonl
- [AUDIT] merge 命令 log / verifier 机器化 log / preflight log / retro / review-log

**events.jsonl 写入 = [GATE] hard-fail**(per guide §3 · 消灭 side-effect 语义):
- SKILL §6.4:events.jsonl 写入失败 = ship 失败 · 显式 exit 1
- SKILL §4.1 atomic order:commit 前 events.jsonl 必写

起 T001:
1. git worktree add projects/<feature>/T001 <new-branch>
2. cd 进 worktree
3. TDD:test → red → implement → green
4. 跑 /task-review verdict ≠ BLOCK(per §4.1 方案 A 或 B · codex adversarial-review 等价物)
5. merge 回 main(squash 或 rebase 自选)
6. 删 worktree

ship 标志:T001 verification criteria 全过 + cross-model review verdict ≠ BLOCK + main 含 T001 commit + events.jsonl 写入 PASS
```

**friction 高发点**:
- worktree 路径冲突 → 改 `projects/<feature>/T001` → `projects/<feature>-T001`
- TDD 写不出 red test(spec 太抽象) → 回 Step 2 修 spec · 不绕过
- review BLOCK → 真修代码 · 不放水
- events.jsonl 没写 → [GATE] hard-fail · agent 撞墙 · 必写后才能 ship

parallel-builder guide piggy-back reference(本 sub-plan 件 2.4 · IDS commit `23c4db7`)。

## §8 · Step 5 · 产 hand-back 包 + 跨仓写回 IDS(~30min · XenoDev + IDS)

### §8.1 · XenoDev session 操作

复制给 XenoDev session:

```
T001 ship 完 · 产 hand-back 包(per ${IDS_REPO}/framework/SHARED-CONTRACT.md §6.3 schema):

1. 准备 hand-back .md:
   - frontmatter:handback_id / source_repo_path / build_repo_path / handback_target / source_repo_identity 块(remote / marker / hash 任选模式)/ tags(drift / prd-revision-trigger / practice-stats / feature)/ severity
   - body §1 normative:Build-side 上下文 50-500 字
   - body §2 normative:触发理由(按 tags 列条)
   - body §3 normative:operator checkbox list 4 项
   - body §3 RECOMMENDED(v2.2 加):producer-side Suggested actions 表格(5 列 # / Action / 类型 / 优先级 / 备注)
   - body §4 RECOMMENDED(v2.2 加):PRD-revision-trigger 检查段(O1-O9 / phase / D-spec / 红线 四类)
   - body §5 RECOMMENDED(v2.2 加):后续 task 建议
   - body §6 RECOMMENDED(v2.2 加):File changes(squash commit + 文件清单)
   - body §7 RECOMMENDED(v2.2 加):已知风险 / known gotchas

2. 跑 lib/handback-validator/validate-handback.sh <hand-back.md> ${IDS_REPO} --mode=producer
   - 6 约束 PASS 才能写
   - 任一 FAIL → drop + stderr · 修 hand-back 再跑
   - 真 fixture corpus 示例:${IDS_REPO}/framework/xenodev-bootstrap-kit/handback-validator/test-fixtures/(valid 1 + invalid 4 · 见 test-fixtures/README.md)

3. 写到 IDS:cp <hand-back.md> ${IDS_REPO}/discussion/${BATCH_ID}/handback/<ts>-<handback_id>.md
   (validator PASS 之后才 cp)
```

### §8.2 · Step 5 闭环责任分担(v2.2 加 · per SHARED-CONTRACT §6.4.1)

| 阶段 | 责任主体 | 完成判据 | 不闭环影响 |
|---|---|---|---|
| **同步段:producer 写回** | XenoDev session | producer validator PASS + 文件落到 `${IDS_REPO}/discussion/${BATCH_ID}/handback/<file>.md` | XenoDev session 不能关 |
| **异步段:consumer 决议** | IDS session(operator 任意时机) | `/handback-review ${BATCH_ID}` 跑完 + HANDBACK-LOG.md append entry + IDS commit | 决议延后不阻 XenoDev session 关闭 |

**关键**:XenoDev session 闭环责任**仅到文件写回** · 不等 IDS 决议。IDS `/handback-review` 是 operator 异步责任 · 可分钟级、天级、甚至跨 session(B+A 真并行模式下常见 · 见 §10)。

### §8.3 · operator 回 IDS session 跑 review

```bash
# 在 IDS session(working dir = ${IDS_REPO}):
ls discussion/${BATCH_ID}/handback/  # 应看到新 hand-back 文件
/handback-review ${BATCH_ID}
```

跟着 /handback-review skill 走完决议 · append 到 `discussion/${BATCH_ID}/handback/HANDBACK-LOG.md`。

**完成标志**:
- `discussion/${BATCH_ID}/handback/<ts>-<handback_id>.md` 存在
- `discussion/${BATCH_ID}/handback/HANDBACK-LOG.md` 至少 1 条 operator 决议
- SHARED-CONTRACT v2.2 piggy-back reference(本 sub-plan 件 2.5+2.2 合 · IDS commit `0e68382`)
- test-fixtures README.md piggy-back reference(本 sub-plan 件 2.3 · IDS commit `6e2628a`)

## §9 · Step 6 · 评分 + Status 决策(~30min · IDS 内)

回 IDS session · write `discussion/${BATCH_ID}/<batch-name>/<batch>-RETROSPECTIVE.md`:

```markdown
---
doc_type: <batch>-retrospective
batch_completion_date: <today>
operator: Yashu Liu
---

# <batch> retrospective

## 5 维度评分(1-10)

| # | 维度 | 评分 | 备注 |
|---|---|---|---|
| 1 | hand-back 包格式可读可消费 | <X>/10 | <evidence> |
| 2 | 6 约束 validator 错误信息清楚 | <X>/10 | <evidence> |
| 3 | workspace + source_repo_identity 在跨仓 friction | <X>/10 | <evidence> |
| 4 | §6.2.1 6 约束在真数据无 false positive/negative | <X>/10 | <evidence> |
| 5 | hand-off → ship → hand-back 闭环符合预期 | <X>/10 | <evidence> |

**总分 / 平均**:<sum>/50 · <avg>/10
```

### §9.1 · Status 决策规则

| 评分 | 行动 |
|---|---|
| **首跑 ≥ 7/10** | 起 cutover sealing commit(SHARED-CONTRACT §6 Status: ACTIVE) |
| **首跑 < 7/10** | 起 forge v3 plan · 本 batch 标 PARTIAL |
| **后续 batch ≥ 7/10** | 加入 v0.2 RETRO(同 004 v0.2-retro.md 模式 · 比较 framework dimension diff) |
| **后续 batch < 7/10** | 起 framework feedback queue(F1-FN)· 入 plan v0.2+ |

**真实参考**(本 sub-plan evidence):
- 006 batch B2.2 评分 38/50 = **7.6/10**(B2.2 cutover sealing commit `08f8104`)
- 004 batch v0.2 评分 43/50 = **8.6/10**(+1.0 vs 006 · v0.2-retro.md `b060a2e`)

## §10 · 跨仓 communication 通道

### §10.1 · operator friction 报告模板

XenoDev session friction → 回 IDS session 报:

```
XenoDev Block <D|E|F> friction
- step: <step 编号>
- file: <XenoDev 内路径>
- error: <粘贴 stderr verbatim>
- 我已尝试: <可选>
```

我会做:
- 评估是不是 IDS 端 helper 缺(改 plan-start v3.0 / spec-kit-evaluation / 三派生 guide)
- 不是 IDS 端问题 → 给 XenoDev 内调试建议 · operator cp 进 XenoDev session
- 是 IDS 端问题 → 我修 IDS · 产 fix commit · operator 回 XenoDev 重试

我不做:
- 不直接读 / 写 XenoDev 仓内文件(权限边界 · operator 跨仓自跑)
- 不替 operator 决"这个 friction 该不该修"(operator 决 · 我评估)

### §10.2 · B+A 真并行模式(v2 加 · 本 sub-plan 实证)

**模式定义**:operator 切 XenoDev session 跑 A 通道(继续 ship 业务 task) · 同时 IDS session 跑 B 通道(framework feedback 落地) · 两通道 IDS 触达点不重叠。

**真实证**(plan-rosy-naur v12 · 2026-05-12):
- B 通道在 IDS 内 ship:件 2.6 (`0d51595`) → 件 2.5+2.2 合 (`0e68382`) → 件 2.4 (`23c4db7`) → 件 2.3 (`6e2628a`) → 件 2.1 (本 commit)
- A 通道 operator 在 XenoDev 自跑:W1 FU-notes-fix(squash `7eb8626` · 10:51:03 UTC)+ W2 FU-weekly-fix(squash `09f6cc1` · 11:01:41 UTC)
- **真并行节点**:W1 写回时间(10:51)与 IDS B 件 2.4 ship(`23c4db7` ≈ 11:00)同一段 · 三 ship 真并行 · 跨仓 0 冲突
- A 通道写回 IDS 后 IDS git status 探到 untracked · 即时 `/handback-review ${BATCH_ID}` 决议 · 不阻 B 节奏

**IDS commit boundary 守则**(严格):
- B 件 commit 只 stage B 改动(framework/*.md / SHARED-CONTRACT)· A 包 untracked
- A 包 commit 独立(`docs(discussion): <batch>-<fork-id> ... hand-back 包入库 + HANDBACK-LOG 决议`)
- 两通道**不打包**(per CLAUDE.md ground rule)· per plan-rosy-naur v12 ground rule 2

**OQ-playbook-5**(本 v2 加):B+A 真并行能否扩 3+ 通道(多 batch 同时跑)?本 playbook 不预决 · 等 v0.3+ 多 batch 实战暴露。

## §11 · 失败回滚路径

| Block | 失败 | 回滚 |
|---|---|---|
| D spec-writer 派生卡 | XenoDev 内修 / 起 forge v3 | XenoDev 仓决 · IDS 不动 |
| D spec-writer 跑卡 | 修 spec / 重跑 | XenoDev 内 |
| E task-decomposer audit FAIL | per task-decomposer guide §4 三选一(拆 task / 跨仓 cp / forge amendment) | operator plan-mode 决 |
| E parallel-builder 跑不通 review | 修 spec → 重派 task | XenoDev 内 |
| E events.jsonl 漏写 [GATE] FAIL | 补写 events.jsonl · 重跑 ship · 不允许 silent skip | XenoDev 内 |
| F 6 约束 validator 真数据 false positive/negative | 改 IDS validator | IDS fix commit |
| F hand-back schema §3-§7 不齐 | 补 RECOMMENDED 字段(per SHARED-CONTRACT v2.2 §6.3) | XenoDev 内 |
| G 评分 < 7/10(首跑) | 起 forge v3 · 本 plan PARTIAL | IDS RETRO.md |
| G 评分 < 7/10(后续 batch) | 入 F1-FN feedback queue · 不停 ship | IDS plan v0.X+1 |
| 整 batch 失败 | revert IDS batch commit;XenoDev 自决保留/删 | 历史 evidence 全保留 |

## §12 · 估时合计(generic)

| Step | 简单 batch | 中等 | 复杂 |
|---|---|---|---|
| Step 0-1.5 起 XenoDev + 派生 skill | 1-2 h | 2-3 h | 3-4 h |
| Step 2 spec | 1-2 h | 2-4 h | 4-8 h |
| Step 3 task | 30 min - 1 h | 1-2 h | 2-4 h |
| Step 4 ship (单 task) | 4-8 h | 半天-1天 | 1-2 天 |
| Step 5 hand-back | 30 min | 30 min | 1 h |
| Step 6 评分 | 30 min | 30 min | 1 h |
| **合计** | **1-2 天** | **2-3 天** | **3-5 天** |

后续 batch 复用 skill / framework v2.2 schema · 起跑成本降(skip Step 1.5 · 直接 Step 2)。

## §13 · 关键文件清单(参数化)

### IDS 仓内必读(只读引用)

| 文件 | 用途 |
|---|---|
| `${IDS_REPO}/framework/SHARED-CONTRACT.md` §6 v2.2 | 协议 SSOT(v2.2 含 §6.3 RECOMMENDED + §6.4.1 闭环责任) |
| `${IDS_REPO}/framework/SHARED-CONTRACT.md` §6.3 | hand-back schema(3 节 normative + 4 节 RECOMMENDED) |
| `${IDS_REPO}/framework/SHARED-CONTRACT.md` §6.2.1 | 6 约束定义 |
| `${IDS_REPO}/framework/SHARED-CONTRACT.md` §6.4.1 | Step 5 闭环责任分担(v2.2 加) |
| `${IDS_REPO}/framework/spec-kit-evaluation.md` | 7 元素 spec schema 引证 |
| `${IDS_REPO}/framework/xenodev-bootstrap-kit/CLAUDE.md` | XenoDev 三件硬约束 |
| `${IDS_REPO}/framework/xenodev-spec-writer-derivation-guide.md` | spec-writer 派生指引 |
| `${IDS_REPO}/framework/task-decomposer-derivation-guide.md` | task-decomposer 派生 + audit checklist(件 2.6 · `0d51595`) |
| `${IDS_REPO}/framework/xenodev-parallel-builder-derivation-guide.md` | parallel-builder 派生 + GATE/AUDIT + events.jsonl GATE(件 2.4 · `23c4db7`) |
| `${IDS_REPO}/framework/xenodev-bootstrap-kit/handback-validator/test-fixtures/README.md` | validator 真 fixture corpus(件 2.3 · `6e2628a`) |
| `${IDS_REPO}/discussion/<root>/<parent-fork>/${PRD_FORK_ID}/PRD.md` | 真 PRD 源 |
| `${IDS_REPO}/discussion/<root>/<parent-fork>/${PRD_FORK_ID}/L4/HANDOFF.md` | 真 hand-off 源 |

### XenoDev 仓内会产生

| 文件 | Step |
|---|---|
| `${XENODEV_REPO}/.claude/skills/spec-writer/SKILL.md` | 1.5 |
| `${XENODEV_REPO}/.claude/skills/task-decomposer/SKILL.md` | 1.5 |
| `${XENODEV_REPO}/.claude/skills/parallel-builder/SKILL.md` | 1.5 |
| `${XENODEV_REPO}/.claude/commands/task-review.md`(可选 · §4.1 方案 A) | 1.5 |
| `${XENODEV_REPO}/specs/<feature>/spec.md` | 2 |
| `${XENODEV_REPO}/specs/<feature>/tasks/T*.md` | 3 |
| `${XENODEV_REPO}/specs/<feature>/dependency-graph.mmd` | 3 |
| `${XENODEV_REPO}/projects/<feature>/T<NNN>/` | 4(merge 后删 worktree) |
| `${XENODEV_REPO}/.eval/events.jsonl` | 4(每 ship 一行 · GATE) |

### IDS 仓内会产生

| 文件 | Step |
|---|---|
| `${IDS_REPO}/discussion/${BATCH_ID}/handback/<ts>-<handback_id>.md` | 5 |
| `${IDS_REPO}/discussion/${BATCH_ID}/handback/HANDBACK-LOG.md` | 5 |
| `${IDS_REPO}/discussion/${BATCH_ID}/<batch-name>/<batch>-RETROSPECTIVE.md` | 6 |
| `${IDS_REPO}/framework/SHARED-CONTRACT.md`(§6 Status 改 · 仅首跑) | 6(若 ≥ 7/10) |

## §14 · OQ(本 playbook 不解决)

- **OQ-playbook-1**(从 v1 沿用):XenoDev session 派生的 skill SKILL.md 字段 schema 应该多严?(operator 决 · 跑 spec-writer 时若 friction 暴露再说)
- **OQ-playbook-2**(从 v1 沿用):T<NNN> 选哪个具体 task — operator 按 dependency-graph 第一个可执行(入度 0)
- **OQ-playbook-3**(从 v1 沿用):cross-model review 用哪 model 组合 — operator 按 IDS .claude/commands/task-review.md 范式(或 §4.1 方案 B 用 codex adversarial-review)
- **OQ-playbook-4**(从 v1 沿用):1 个 task ship 是否够"真" — operator 主观决 · 本 playbook 默认 1 task ship 后可起 hand-back · multi-task ship 也合规
- **OQ-playbook-5**(v2 加):B+A 真并行能否扩 3+ 通道(多 batch 同时跑)? · 本 playbook 不预决 · 等 v0.3+ 多 batch 实战暴露

## §15 · 与 plan-rosy-naur v12 关系

本 playbook 是 plan-rosy-naur v12 B 件 5(2026-05-12 ship)产物 · plan v0.2-global 件 2.1 落地。**B 通道 5 件全 done**(2.6 / 2.5+2.2 合 / 2.4 / 2.3 / 2.1)。

- **不动**:006 v1 playbook(`discussion/006/b2-2/OPERATOR-PLAYBOOK-BLOCK-D-G.md` · 历史 evidence) · 三派生 guide · SHARED-CONTRACT · test-fixtures
- **piggy-back 引**:本 sub-plan B 通道前 4 件 + A 通道 W1+W2(共 5 commit · `0d51595` / `0e68382` / `23c4db7` / `6e2628a` / `9e8fba3`)
- **可 amend**:本 §4.1 task-review 等价物方案(A/B 二选一) · §10.2 B+A 真并行扩展规则 · §14 OQ-playbook-5
- **下游**:operator 跨 batch session 跑本 playbook · 替换 ${...} 参数 · 即可起跑

## §16 · Changelog

- **2026-05-12 v1.0**: 起新 generic 模板 · 基于 006 v1(338 行)generic 化 · §4.1 加 F1 fix(task-review 等价物 A/B 二选一) · §10.2 加 B+A 真并行模式实证 · piggy-back 5 commit(件 2.6 / v2.2 / 件 2.4 / 件 2.3 + A 通道)· batch-specific token 全参数化(${IDS_REPO} / ${XENODEV_REPO} / ${BATCH_ID} / ${PRD_FORK_ID} / ${IDS_SNAPSHOT_COMMIT})· 16 节 · ~330 行
- **2026-05-10 v1**(`discussion/006/b2-2/OPERATOR-PLAYBOOK-BLOCK-D-G.md` 338 行 · 历史 evidence · 不动):initial · 整合 plan v11 Block D-G + framework/b2.1-dry-run-validation.md + xenodev-bootstrap-kit/CLAUDE.md + Round 5 决策日志后的状态
