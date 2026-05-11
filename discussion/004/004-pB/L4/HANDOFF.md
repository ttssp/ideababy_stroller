---
# §6.2 workspace schema 4 字段
workspace:
  source_repo: /Users/admin/codes/ideababy_stroller
  build_repo: /Users/admin/codes/XenoDev
  working_repo: /Users/admin/codes/ideababy_stroller
  handback_target: /Users/admin/codes/ideababy_stroller/discussion/004/handback/

# §3.1 source_repo_identity 字段(IDS forward 端填入,XenoDev hand-back producer 按 §6.2.1 约束 3 三模式比对)
source_repo_identity:
  expected_remote_url: git@github.com:ttssp/ideababy_stroller.git
  repo_marker: "# Idea Incubator — Project C"
  git_common_dir_hash: 647b0db7b4d47318

# Hand-off metadata
prd_fork_id: 004-pB
discussion_id: "004"
prd_form: phased
phases: [v0.2, v0.5, v1.0, v1.5+]
phase_current: v0.2
phase_target: v0.2
modules: null
module_forms: null
critical_path_module: null
skip_rationale: null

handed_off_at: 2026-05-10T07:12:34Z
prd_source: /Users/admin/codes/ideababy_stroller/discussion/004/004-pB/PRD.md
shared_contract_version_honored: 2.0
---

# Hand-off · 004-pB → XenoDev (per SHARED-CONTRACT §6 v2.0)

**Handed off at**: 2026-05-10T07:12:34Z
**PRD source**: `/Users/admin/codes/ideababy_stroller/discussion/004/004-pB/PRD.md`
**Build repo**: `/Users/admin/codes/XenoDev`
**Workspace**: 见 frontmatter `workspace:` 块(§6.2 4 字段全填)
**Source repo identity**: 见 frontmatter `source_repo_identity:` 块(XenoDev 写 hand-back 前必须按 §6.2.1 约束 3 三模式校验,任一 PASS 即满足)
**SHARED-CONTRACT version honored**: 2.0

---

## §1 · 给 XenoDev operator 的指令

operator 切到 build_repo 后:

1. `cd /Users/admin/codes/XenoDev`
2. 读本 HANDOFF.md(全文)+ 引用的 PRD.md
3. 在 XenoDev session 触发 XenoDev 自带的 spec-writer(per XenoDev AGENTS.md;**不**调 IDS 的 spec-writer subagent — XenoDev 派生自己的)
4. spec-writer 产 XenoDev 内部 spec.md(7 元素 schema,具体格式见 XenoDev `templates/spec.template.md`)
5. XenoDev task-decomposer 产 tasks/T*.md
6. parallel-builder 跑 task,quality gate 在 XenoDev 内部决议
7. 每个 task ship 后 XenoDev 产 hand-back 包(per §6.3 schema)写回 IDS `<source_repo>/discussion/004/handback/`

### 1.1 · 本 hand-off 的特殊性(必读)

**v0.1 已 ship,本次是 v0.2 hand-off(phased 第二阶段)**:
- v0.1 ship 时间:2026-04-27,见 IDS 仓 `projects/004-pB/docs/v0.1-ship-summary.md`
- v0.1 历史代码位于 IDS 仓内 `projects/004-pB/src/decision_ledger/...`(M2 cutover 前的产物)
- v0.2 build 在 XenoDev,**不**复用 v0.1 的 `projects/004-pB/` worktree;XenoDev spec-writer 需把 v0.1 代码视作"已有参考实现"读取,产出 XenoDev 内部新 spec
- v0.1.1 hotfix 余项:`projects/004-pB/docs/known-issues-v0.1.md`(Codex review F1/F2/F3 处置),v0.2 启动前 operator 应确认这些 hotfix 的处置状态(已修 / 留到 v0.2 / 接受为已知)

**v0.2 三个交付物**(顺序由 operator 决定,XenoDev task-decomposer 拆 DAG 时参考):
1. v0.2.1 笔记 wiki 升级(主动复盘 + 概念健康度)— 难度 L,重要度 M
2. v0.2.2 自动化咨询师监控(Proxyman 升级到自动化 pipeline)— 难度 H,重要度 H
3. v0.2.3 简单的私有模型 v1(XGBoost + 技术指标)— 难度 H,重要度 H

详细完成标准 + v0.1 已留位实测 → 见 PRD §6 Phase v0.2。

---

## §2 · PRD-form 透传(XenoDev spec-writer 分派依据)

`prd_form: phased`(详见 frontmatter)

**phased 形态分派**:
- spec.md / SLA.md / risks.md 按 PRD `**Phases**` 数组(`[v0.2, v0.5, v1.0, v1.5+]`)分段
- 当前 hand-off 的 build 范围 = **v0.2**(phase_target);v0.5 / v1.0 / v1.5+ 不在本 hand-off 实施范围,但 spec-writer 应在 architecture / SLA 段保留扩展点引用(参见 PRD §6 各 Phase 描述)
- 红线(PRD §5 Scope OUT 永远不做项)在 spec.md 必须显式列出,**不留扩展点**(per PRD §5 协议规则)

---

## §3 · §6.2.1 6 约束自检契约(XenoDev producer 写 hand-back 前必走)

per `framework/SHARED-CONTRACT.md` §6.2.1,XenoDev 产 hand-back 包写入 `<source_repo>/discussion/004/handback/` 前,必须按 6 约束自检:

1. **canonical-path containment**:`realpath(handback_target)` 严格落在 `realpath(source_repo) + "/discussion/004/handback/"` 之下
2. **symlink reject**:`<source_repo>/discussion/004/handback/` 路径上任意一段是 symlink → reject(`source_repo` 自身可以是 symlink,从 source_repo canonicalized 后往下走)
3. **repo identity check**(三模式,任一 PASS 即满足):
   - remote 模式:`git config remote.origin.url` ∈ source_repo == `git@github.com:ttssp/ideababy_stroller.git`(strip protocol prefix + trailing `.git` 后字面相等)
   - no-remote 模式:`head -c 30 CLAUDE.md` ∈ source_repo 含子串 `# Idea Incubator — Project C`(`Idea Incubator` 必含)
   - hash-only 模式(operator 显式开启):`sha256(.git/HEAD + .git/config)` ∈ source_repo 前 16 字符 == `647b0db7b4d47318`
4. **id consistency check**:三处 id 严格一致 — 物理路径 `discussion/004/handback/` 的 `004` == 文件名 `<ts>-<handback_id>.md` 中 `handback_id` 解出的 prd_fork_id 前缀的 discussion_id 部分(`004-pB-...` → `004`)== frontmatter `discussion_id` 字段
5. **id 字符集 + filename basename + final-path containment**:
   - `discussion_id` 匹配 `^[0-9]{3}$`(`004` ✓)
   - `prd_fork_id` 匹配 `^[0-9]{3}[a-z]?(-p[A-Z])?$`(`004-pB` ✓)
   - `<ISO ts>` 匹配 `^[0-9]{8}T[0-9]{6}Z$`
   - `handback_id` 严格等于 `<prd_fork_id> + "-" + <ISO ts>` 拼接结果
   - filename basename 校验 + 写入前 final-path realpath containment 二次校验
6. **hard-fail 行为**:任一约束失败 → producer 不写 / consumer 不读,只 stderr 报具体哪条约束失败 + handback_id + exit 非 0

任一失败 = `Drop`(不写文件,不创目录,只 stderr)。

---

## §4 · Open questions for build phase

(IDS PRD 中**关于 build 路径选择**的 OQ 在此承载;XenoDev build 自然遇到时再解决,不污染 XenoDev spec frozen)

来自 PRD §11 Open(v0.2 启动前需回答):

### OQ-1 · 笔记 wiki Concept schema 设计【v0.2.1 必答】
- **背景**:PRD §6.v0.2.1 完成标准 "≥ 7 概念独立复述准确率 ≥ 70%",但 v0.1 实际只有简单 `Note` 模型,无 Concept / first_seen_at / recall_score
- **路径选择**:
  - (a) 在 Note 模型上加字段(`concept_first_seen_at` / `concept_recall_score` / `concept_id` 等)— 最小改动,风险:Note 与 Concept 语义混在
  - (b) 新建 Concept 表,Note 与 Concept 多对多 — 最干净,工程量稍大
- **决策时点**:v0.2 spec.md kickoff
- **建议决策方**:XenoDev spec-writer + operator

### OQ-2 · 多模态接口拆分粒度【v0.2.2 必答】
- **背景**:PRD §6.v0.2.2 实测显示 v0.1 的 `AdvisorParser` 是单一类,没有 source/format/fetcher 三层
- **路径选择**:
  - (a) parser.py 大重构成三层(SourceAdapter / FormatHandler / Fetcher)— 工程量最大但最干净,后续 v0.5+ 不需再重构
  - (b) 新写并行的 multimodal pipeline,老 parser 保留作 PDF 路径 — 兼容老路径,但有重复代码债
  - (c) 直接在 parser 加 `if format=='audio'` 分支 — 最快但 v0.5+ 还会再重构
- **决策时点**:v0.2 spec.md kickoff
- **建议决策方**:XenoDev spec-writer + operator
- **风险提示**:(c) 最快但累积 tech debt,v0.5 跨市场 cross-signal 时会再重构,operator 需在 (a)/(c) 间权衡 v0.2 时间预算

### OQ-3 · v0.1 成功机制 proxy 是否够强【ship 后第 8 周回看】
- **背景**:PRD §11 — spec.md C11 已把 O3 (≥ 3 次阻止冲动) 写为 acceptance,但 ship 后 8 周回看时,human 是否真的接受 "≥ 3 次档案中 `would_have_acted_without_agent=yes` 但 final action ≠ acted" 算"机制起作用"的证据?或需要更强 proxy(例如 outcome 字段事后回填)?
- **决策时点**:ship 后第 8 周(2026-06-22 前后)
- **本 hand-off 的关系**:**不影响** v0.2 build 启动;若 8 周回看判定需更强 proxy → operator 跑 `/scope-inject` 修 PRD §7 O3 + 起 v0.2 spec.md amendment
- **建议决策方**:operator 单决

### OQ-4 · 配偶可见度 schema【v1.0 启动远期】
- **背景**:PRD §6 v1.0 配偶可见度从"难度 L"修正到"难度 M"(因 v0.1 visibility/share 字段未留)
- **路径选择**:
  - (a) decision_archive 表加 visibility 字段
  - (b) 独立 share_link 表
- **决策时点**:v1.0 启动(远期,9-18 个月)
- **本 hand-off 的关系**:**不影响** v0.2 build;归档参考,XenoDev v0.2 spec.md 不需为此预留 schema

---

## §5 · Rollback plan

如果 XenoDev build 失败:

- **(a) 回到 IDS 修 PRD,重跑 `/plan-start`**
  - 适用场景:v0.2.1/v0.2.2/v0.2.3 任一完成标准不可达 + 不是单 task 局部问题,而是 PRD 阶段约束本身有问题
  - 操作:`/scope-inject 004-pB` 修 PRD,产新 PRD 版本号 → 重跑 `/plan-start 004-pB` 产新 hand-off 包
- **(b) 改 XenoDev spec(不改 IDS PRD),用 XenoDev 自己的修订机制**
  - 适用场景:实装层面的细节(eg OQ-1 选 (a) 后 Note 模型加字段位置)与 PRD 不冲突,只是 XenoDev spec 内部技术决策需调
  - 操作:在 XenoDev 仓走 XenoDev 的 spec amendment 流程,不需 IDS 介入
- **(c) 起 forge v3 重新审整个 idea**
  - 适用场景:多个 hand-back 包累积呈现系统性 drift(eg "30 秒 SLA 在多模态接入后不可达"+ "决策档案 8 周 ≥ 15 条未达")
  - 操作:`/expert-forge 004-pB` 起 forge v3,两 reviewer 审整个 PRD + spec + ship 数据
- **(d) XenoDev 产 hand-back 包(tags: `prd-revision-trigger` / `drift` / `practice-stats`)写回 IDS,operator 在 IDS 跑 `/handback-review 004` 决议**
  - 适用场景:任一 task ship / spec violation / 跑完一批 task 的 stats,XenoDev 端常规反馈
  - 操作:XenoDev producer 按 §6.3 schema + §3 6 约束自检 → 写 `<source_repo>/discussion/004/handback/<ISO>-<handback_id>.md` → operator 在 IDS 仓 `cd /Users/admin/codes/ideababy_stroller && /handback-review 004`

---

## §6 · 引用资源(XenoDev spec-writer 必读)

按读取顺序:

1. **本 HANDOFF.md**(全文)
2. **PRD**:`/Users/admin/codes/ideababy_stroller/discussion/004/004-pB/PRD.md`(权威 source of truth)
3. **L3 stage doc**:`/Users/admin/codes/ideababy_stroller/discussion/004/L3/stage-L3-scope-004.md`(menu 全集 + Candidate B 完整背景)
4. **L2 unpack**:`/Users/admin/codes/ideababy_stroller/discussion/004/L2/stage-L2-explore-004.md`(尤其 §4 Natural extensions,是 PRD §6 Phased roadmap 的权威来源)
5. **FORK-ORIGIN.md**:`/Users/admin/codes/ideababy_stroller/discussion/004/004-pB/FORK-ORIGIN.md`(本 fork 的来历 + 红线)
6. **v0.1 ship summary**:`/Users/admin/codes/ideababy_stroller/projects/004-pB/docs/v0.1-ship-summary.md`(已 ship 的 v0.1 实际状态)
7. **v0.1 known issues**:`/Users/admin/codes/ideababy_stroller/projects/004-pB/docs/known-issues-v0.1.md`(v0.1.1 hotfix 余项)
8. **PRD v01 与 v2.0 对比**:`/Users/admin/codes/ideababy_stroller/discussion/004/004-pB/COMPARE-v01-vs-v02.md`(协议演进上下文)
9. **SHARED-CONTRACT §6 v2.0**:`/Users/admin/codes/ideababy_stroller/framework/SHARED-CONTRACT.md` §6(workspace schema + hand-back 通道 normative spec)
