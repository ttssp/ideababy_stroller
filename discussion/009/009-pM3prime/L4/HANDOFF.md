---
# §6.2 workspace schema 4 字段
workspace:
  source_repo: /home/ys/codes/ideababy_stroller
  build_repo: /home/ys/codes/XenoDev
  working_repo: /home/ys/codes/ideababy_stroller
  handback_target: /home/ys/codes/ideababy_stroller/discussion/009/handback/

# §6.5 第 13 项 source_repo_identity 字段(由 IDS forward 产源时填入,XenoDev 验)
source_repo_identity:
  expected_remote_url: git@github.com:ttssp/ideababy_stroller.git
  repo_marker: "# Idea Incubator — Project C"
  git_common_dir_hash: 0de4fb398ede9db1

# Hand-off metadata
prd_fork_id: 009-pM3prime
discussion_id: "009"
prd_form: phased
phases: [E0, E1]

handed_off_at: 2026-07-16T13:15:00Z
prd_source: /home/ys/codes/ideababy_stroller/discussion/009/009-pM3prime/PRD.md
shared_contract_version_honored: 2.0

# Session-per-idea worktree 规约三字段(forge 006 v8 · 跨仓通道拓扑自证)
current_idea: "009"
worktree: main(IDS 治理仓 · fork 产物经 checkpoint 入 main)
baseline: forge v5 converged(stage-forge-009-v5.md)· 009-pForge fork-complete(M1+M2 · 743 passed)
---

# Hand-off · 009-pM3prime → XenoDev (per SHARED-CONTRACT §6 v2.0)

**Handed off at**: 2026-07-16T13:15:00Z
**PRD source**: /home/ys/codes/ideababy_stroller/discussion/009/009-pM3prime/PRD.md
**Build repo**: /home/ys/codes/XenoDev
**Workspace**: 见 frontmatter `workspace:` 块(§6.2 4 字段全填)
**Source repo identity**: 见 frontmatter `source_repo_identity:` 块(XenoDev 写 hand-back 前必须按 §6.2.1 约束 3 校验)
**SHARED-CONTRACT version honored**: 2.0

## §0 · 一句话定位(给 XenoDev spec-writer 定向)

本 fork = 009「投资决策闭环」M3'(信号提取头)证伪链的**前两站 E0+E1**:E0 口径预注册
(定义"一条可评估疑似信号" + rejection taxonomy + 预注册密度阈值 + 009 自有三表 DDL)、
E1 密度普查 + 两层金标(对 008 语料 collection.db 实测可提取疑似信号密度;提取器过
span 抽取 + 可交易映射两层验收;查明 record_tickers 语义)。**E2(历史窗先导回测)/
E3(forward 确证线)未授权**——gate 在 E1 真数字,经 hand-back 交回 IDS 由 operator 另裁。
build 把 E2/E3 做进来 = 越界 = BLOCK(PRD §5)。

背景材料(XenoDev 侧建议读):PRD 全文(必读)· `discussion/009/forge/v5/stage-forge-009-v5.md`
(verdict/证伪链/underweights)· `discussion/009/operator-input-2026-07-16-implicit-signals.md`
(事实修正血缘)· `discussion/009/forge/v5/xenodev-alpha-assets-snapshot.md`(M2 契约摘录 +
collection.db 实测——XenoDev 本仓资产,可直接真读源码复核)。

## §1 · 给 XenoDev operator 的指令

operator 切到 build_repo 后:

1. `cd "$BUILD_REPO"`(= frontmatter `workspace.build_repo`,本机 `/home/ys/codes/XenoDev`)
2. 读本 HANDOFF.md(全文)+ 引用的 PRD.md
3. 在 XenoDev session 触发 XenoDev 自带的 spec-writer(per XenoDev AGENTS.md;**不**调 IDS 的 spec-writer subagent — XenoDev 派生自己的)
4. spec-writer 产 XenoDev 内部 spec.md(7 元素 schema,具体格式见 XenoDev `templates/spec.template.md`)
5. XenoDev task-decomposer 产 tasks/T*.md
6. parallel-builder 跑 task,quality gate 在 XenoDev 内部决议
7. 每个 task ship 后 XenoDev 产 hand-back 包(per §6.3 schema)写回 IDS `<source_repo>/discussion/009/handback/`

## §2 · PRD-form 透传(XenoDev spec-writer 分派依据)

`prd_form: phased` · `phases: [E0, E1]`(详见 frontmatter)

- phased → SLA / risks 按 PRD `**Phases**` 数组分段(E0 / E1 各自独立可用 + 各自停止条件)
- ⚠ 特别注意:PRD §6 列出的 ~~E2/E3~~ 仅为路线完整,**不进 spec scope**(对齐 009-pForge
  先例:M3/M4 列出但 OUT,spec line 级 OUT 条款 + 越界=BLOCK)

## §3 · §6.2.1 6 约束自检契约(XenoDev producer 写 hand-back 前必走)

per `framework/SHARED-CONTRACT.md` §6.2.1,XenoDev 产 hand-back 包写入 `<source_repo>/discussion/009/handback/` 前,必须按 6 约束自检:

1. canonical-path containment(realpath prefix 校验)
2. symlink reject(路径任一段是 symlink 即拒)
3. repo identity check(三模式:remote / no-remote / hash-only,任一 PASS 即满足)
4. id consistency check(三处 id 严格一致)
5. id 字符集 + filename basename + final-path containment(OWASP path traversal 防御)
6. hard-fail(任一约束失败,producer 不写 / consumer 不读)

任一失败 = `Drop`(不写文件,不创目录,只 stderr)。

## §4 · Open questions for build phase

(从 IDS PRD §11 分流的 build 路径选择类 OQ;XenoDev build 自然遇到时解决,不污染 spec frozen)

1. **金标两层具体数值门槛**(α 精确值 / span P/R 下限 / 映射一致率):build 时**预注册**
   (先写下再跑),原则已定死(有门槛 + 两层全过才放行)。
2. **record_tickers 语义三选一**(复用/校验/重建):E1 普查站实测后判定,判定依据与结论
   进 hand-back。
3. **预注册密度阈值具体数**:E0 站推算(参照 M2 walk-forward + DSR 显著性所需样本量,
   M2 契约见快照件),推算结果经 hand-back 请 operator 拍板后钉死。
4. **E1 普查的抽样方案**(全量 9,081 条 vs 分层抽样控制 LLM 成本):build 时定,方案本身
   须预注册(PRD §9)。
5. **提取器实现选型**(模型/prompt 结构):build 自由度,但受 PRD §7 红线约束(温度 0 /
   版本化 / 每变体入 trial_ledger)。

## §5 · Rollback plan

如果 XenoDev build 失败:
- (a) 回到 IDS 修 PRD,重跑 `/plan-start 009-pM3prime`
- (b) 改 XenoDev spec(不改 IDS PRD),用 XenoDev 自己的修订机制
- (c) 起 forge v6 重新审(触发条件见 stage doc §underweights:E1 密度 < 阈值 / 提取稳定性
  推演不成立 / 对照路径需评估 / 快照件被证有误)
- (d) XenoDev 产 hand-back 包(tags: `prd-revision-trigger`)写回 IDS,operator 在 IDS 跑
  `/handback-review 009` 决议
