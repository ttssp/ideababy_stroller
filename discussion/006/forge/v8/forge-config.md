---
forge_version: v8
created: 2026-07-13T11:20:00Z
convergence_mode: strong-converge
x_hash: e9b6ed08cec4ad28da0f68a6cd08a4f4
prefill_source: proposals.md§006 + caller v8 批次(XenoDev dogfood-backlog KG-B2..B7 攒批 + operator worktree 隔离诉求 2026-07-13)
---

# Forge Config · 006 · v8

## X · 审阅标的

discussion/006/forge/v8/_x-batch-snapshot.md
/home/ys/codes/XenoDev/dogfood-backlog.md
discussion/006/forge/v7/stage-forge-006-v7.md
CLAUDE.md
/home/ys/codes/XenoDev/CLAUDE.md
TEXT:proposal-006(见 K 首四段)

### 解析后的标的清单

- `discussion/006/forge/v8/_x-batch-snapshot.md`(类型:本仓库文件 · **权威快照 · 首选阅读源** · ✅ 可达。三部分:① operator worktree 隔离诉求原话 + IDS 混线实证;② KG-B2..B7 六条 dogfood-backlog 原文全文(摘 @ XenoDev cc4edeb);③ XenoDev CLAUDE.md 工作流摘录。Codex 沙箱 BLOCK 外部路径时以本文件为准,自足)
- `/home/ys/codes/XenoDev/dogfood-backlog.md`(类型:外部 repo 文件 · ⚠ Codex 沙箱可能 BLOCK · 仅作能读时的原文核对源;若读,用 Grep 定位 KG-B 段落,**勿整读**(600 行 ~85k token))
- `discussion/006/forge/v7/stage-forge-006-v7.md`(类型:stage 文档 · ✅ 可达 · 最近 verdict(review gate 状态机 + fork-id SSOT)承接上下文;只读 verdict/decision matrix/underweights 三节即可。KG-B2 与 v7 A1 的联动关系在 v7 已预判)
- `CLAUDE.md`(类型:本仓库文件 · ✅ · IDS 宪法 —— 现行 session/分支/目录工作流的定义处;worktree 隔离议题的 IDS 侧现状基准)
- `/home/ys/codes/XenoDev/CLAUDE.md`(类型:外部 repo 文件 · ⚠ BLOCK 可跳 —— 快照 Part 3 已含工作流摘录)
- `TEXT:proposal-006`(类型:粘贴文本 · K 首四段 · 006 大方向背景,本轮不重审大方向)

## Y · 审阅视角

✅ 架构设计(框架机制缺口的主视角:KG-B2 build 基线拓扑 / KG-B4+B7 gate 强制与执行语义 / KG-B5 LlmClient 接口契约 / worktree 隔离的分支拓扑设计)
✅ 工程纪律(KG-B3 TDD 证据入仓 / KG-B6 hook 与 SKILL 范式冲突 / 流程规约的可执行性)
✅ 用户体验(operator 工作流人体工学:worktree 隔离诉求的本质是单人多线操作的心智负担;KG-B6 高频误报也是 UX 摩擦)

## Z · 参照系

mode: 对标 SOTA
**检索方向**(P2):多 agent/多 session 并行开发的 git worktree 隔离模式(业界实践,含 Claude Code 官方 worktree 用法)· LLM system/user role 分离作为 prompt-injection 防御的业界标准(OpenAI/Anthropic 官方指引)· 「人在环 + 机器对答案」gate 的单次执行/防重放先例(考试系统/CI approval gate/审计)· monorepo 多项目 .gitignore 模板模式 · pre-commit/credential hook 误报治理(fail-closed 与开发者人体工学的平衡)
**外部材料叠加**:无

## W · 产出形态

✅ verdict-only(单一 verdict + 短 rationale)
✅ decision-list(7 项批次逐条:保留现状/调整/新增机制/defer,4 列矩阵)
✅ refactor-plan(按模块分组:gate 执行语义强制(B4+B7 同簇)/ build 基线与 worktree 拓扑(B2 + operator 隔离诉求同簇)/ LlmClient role 分离(B5)/ 证据与 hook 摩擦(B3+B6)/ IDS session 隔离机制)
✅ next-dev-plan(下发排期:XenoDev 授权 brief 条目 + IDS 侧落地项,按 P0/P1/P2 分级)

## K · 用户判准

(proposal §006 四段原文,006 大方向背景:)

给定一个 PRD,claude code 可以几乎没有人工干预的情况下自主完成开发任务。我需要一个**可靠的、自动化程度最高**解决方案。

我是非软件开发背景。我可以将需求描述清楚,我也可以尝试构建较可靠的 PRD。但是我缺少软件开发的经验,对各个规模(大中小型)的开发的方案、流程、规范等内容都没有把握。

我最近一个月做了很多尝试:idea_gamma2(大型项目,phase 制 + pipeline SKILL 生成 playbook + phase-retrospective)、vibe-workflow(engineer team 协作自动化开发)、autodev_pipe(借鉴社区 agentic coding 最佳实践,addy osmani agent-skills + superpowers)、当前 repo(IDS,idea → PRD → 自动开发)。

我希望双方凭借最强的 AI 专业能力以及最丰富的软件开发经验,通过调研、论证、思辨、构思、设计、整理归纳等方式,达成一套基于 claude code 实现**可靠**自动化开发的 framework/pipeline 的共识方案。

**[v8 本轮判准 · 真实审议主体]**:本轮**不重开 006 大方向**,而是审 XenoDev dogfood-backlog 攒批的六条框架缺口 + operator 新诉求,收敛 verdict + 各条改造方案 → 下发双仓落地 brief:

- **KG-B2**(medium):parallel-builder 隐含「一切 merge 回 main」,blocked-handback fork 留 feature 分支 → build 基线偏离(v7 已预判为下批料,与 KG-B4 同簇)
- **KG-B3**(medium):red-green-log TDD 证据被根 .gitignore 吞,豁免 pattern 路径锚定假设错(项目内已修,框架模板缺口待根治)
- **KG-B4**(medium-high):gate 类 task PASS 无机器强制,STOP 可绕过——防 V4 核心机制只靠程序纪律
- **KG-B5**(high · 硬证据):LlmClient 无 system/user role 分离,prompt-injection 防御 9 轮 review 证实 string-sanitize 不收敛;真根治 = role 分离(动 T001 冻结接口 = 契约变更)
- **KG-B6**(高频):credential-isolation hook 对 heredoc/变量拼路径/$() 误报 fail-closed,与 parallel-builder §6.1 明写范式直接冲突
- **KG-B7**(高优先):盲测 gate 试错/重放取答案威胁族,codex 3 轮同族 bypass 硬证据;真根治 = 框架层单次执行强制(同 KG-B4 族)
- **operator worktree 隔离诉求(2026-07-13 原话)**:「每开一个 session,就在自己独立的 worktree 下,working on 一个 idea,不相互干扰。XenoDev 也一样。只有在刚开始 proposal 的时候用 main 分支。」实证:IDS 本周 001/006/009 三 idea 20+ commits 混在 forge/009-blueprint 一根分支上。**注意与 KG-B2 的深层同源性:都是「并行多 idea/多 fork 的分支拓扑无显式规约」**。

**operator 在乎**:方案要可靠、可落地、不过度工程(v7 报告点名过 watchdog 过度工程风险,D1 只落止血核心的先例要延续);gate 类机制与防 V4 强相关,强制性不该只靠程序纪律;KG-B5/B7 是「攒够硬证据才动契约」的正面示范——裁决时尊重证据权重。**硬约束**:mirror 件(bootstrap-kit)改动必须 SSOT 侧改 + cp 回 mirror + MANIFEST SHA 更新(本周刚实证过 mirror 漂移:首跳 cp 自提交前中间态,IDS commit bd3dd70 修复);动 T001 冻结接口是契约变更,须给迁移路径。

## 收敛强度

✅ strong-converge

---

## Summary for reviewers

**审阅标的总数**: 6(1 权威快照[首选·自足] + 1 外部原文[可选核对·BLOCK 可跳·勿整读] + 1 v7 verdict 承接 + 2 仓宪法 + 1 proposal 背景文本)
**视角维度**: 架构设计 · 工程纪律 · 用户体验
**参照系**: 对标 SOTA(worktree 隔离模式 · LLM role 分离 · gate 单次执行/防重放 · monorepo gitignore 模板 · hook 误报治理)
**预期产出**: verdict-only + decision-list(7 项) + refactor-plan(按簇分组) + next-dev-plan(双仓 P0/P1/P2)
**用户最在乎**: 七项批次的**簇化裁决**——B2+worktree 诉求(分支拓扑规约)、B4+B7(gate 执行语义强制)、B5(接口契约变更,硬证据齐)、B3+B6(证据/hook 摩擦)。可靠 > 全面;止血核心优先,防过度工程;mirror 件三层同步纪律;动冻结契约须给迁移路径。
**收敛模式**: strong-converge
