---
forge_id: 006
forge_version: v2
created: 2026-05-09T12:28:43Z
last_updated: 2026-05-09T12:28:43Z
convergence_mode: strong-converge
x_hash: 65d9d65c7c17d4e2cf3241b05a469a16
prefill_source: proposals.md§006 + _x-input-draft-by-operator.md §1-§7 + moderator-notes.md §一-§六
prefill_used: true
v1_x_hash: e45d68ee6dcc74d2c667976a28940c91
v1_convergence_mode: preserve-disagreement
v1_outcome: converged-with-tempo-options
convergence_intent: |
  operator 2026-05-09 verbatim:"每个 W 都要有收敛的内容,也允许在这个 W 上有其他补充/不同的建议、想法和评价"。
  expert 应将此 strong-converge 的具体执行方式理解为:
  - 主线 verdict 必须收敛(W1 单一一句 / W2 4 列决策矩阵单一收敛 / W3 单一 refactor plan / W4 单一 PRD / W5 单一 dev plan / W6 单一长文论述)
  - 残余分歧通过协议原生 §"v0.2 note"(per SKILL.md L471)旁注式纳入,不删丢
  - **不得**因为 strong-converge 就把双方 P3R2 §3 残余意见暴力压扁丢弃
---

# Forge Config · 006 · v2

## X · 审阅标的

operator 与 Claude 在 Step 0.5 prefill + Step 0.5.5 三屏 multi-select 收敛出本节内容。X 总数 = **9 个**(v1 #10 + v1 #11 + Δ-X1 至 Δ-X7);v1 #1-#9 在 §1 标 no-rerun(下节列出但 expert 不读)。

### 解析后的标的清单(9 个,expert 必读)

**自 v1 重审的 2 项**(ADP 仓严重变更):
- `/Users/admin/codes/autodev_pipe`(v1 #10,类型:外部 repo dir)— 推荐范围:`.claude/`、`specs/v4/`、`docs/decisions/`,**避免** `.git/` 历史
- `/Users/admin/codes/autodev_pipe/solo_ai_pipeline_v3.1.md`(v1 #11,类型:外部 file)— 推荐范围:整文件读

**v1 之后增量 7 项**(Δ-X1 至 Δ-X7):
- `/Users/admin/codes/autodev_pipe/specs/v4/spec.md`(Δ-X1,类型:外部 file)— V4 frozen 代码层 + 12 周 dogfood 起点
- `/Users/admin/codes/autodev_pipe/docs/decisions/0008-v4-dogfood-path.md`(Δ-X2 a,类型:外部 file)
- `/Users/admin/codes/autodev_pipe/docs/decisions/0009-v4-scope-downgrade.md`(Δ-X2 b,类型:外部 file)
- `/Users/admin/codes/autodev_pipe/.claude/skills/sdd-workflow/SKILL.md`(Δ-X3 a,类型:外部 file)— ADP 真实入口(非 Makefile)
- `/Users/admin/codes/autodev_pipe/.claude/skills/task-decomposer/SKILL.md`(Δ-X3 b,类型:外部 file)
- `/Users/admin/codes/autodev_pipe/.claude/hooks/block-dangerous.sh`(Δ-X4,类型:外部 file)— Safety Floor 单层防线现状
- `specs/007a-pA/spec.md` v0.3(Δ-X5 a,类型:本仓库 file)— IDS 跨仓 hand-off pilot 主 spec
- `specs/007a-pA/HANDOFF.md`(Δ-X5 b,类型:本仓库 file)— hand-off 包契约 + step 1-6 实测
- `.codex-outbox/queues/007a-pA/`(Δ-X5 c,类型:本仓库 dir)— 4 轮 R1-R4 adversarial review outbox
- `framework/SHARED-CONTRACT.md` v1.1.0(Δ-X6 a,类型:本仓库 file)— IDS↔ADP 当前协议
- `framework/AUTODEV-PIPE-SYNC-PROPOSAL.md` v2(Δ-X6 b,类型:本仓库 file)
- `framework/NON-GOALS.md`(Δ-X6 c,类型:本仓库 file)
- `framework/ADP-AUDIT-2026-05-08.md`(Δ-X7,类型:本仓库 file)— **架构级 §9 4 实证 drift 完整论证**(优先于 v1 任何 verdict)

### v1 X no-rerun 清单(9 项,expert 不读但应知存在)

operator §1(`_x-input-draft-by-operator.md`)显式标定:v1 #1-#9 自 v1 跑(2026-05-07)起未发生显著变化,v2 不重审,**节省 Phase 1 token**。

- v1 #1 proposal-text:proposals.md §006 verbatim(已 prefill 到 K seed)
- v1 #2 `/Users/admin/codes/idea_gamma2`(repo dir)
- v1 #3 `/Users/admin/codes/idea_gamma2/docs/_archive/technology_roadmap.md`
- v1 #4 `/Users/admin/codes/idea_gamma2/.claude/skills/pipeline/SKILL.md`
- v1 #5 `/Users/admin/codes/idea_gamma2/.claude/skills/phase-retrospective/phase-retrospective-skill.md`
- v1 #6 `/Users/admin/codes/idea_gamma2/.claude/agents`
- v1 #7 `/Users/admin/codes/idea_gamma2/.claude/skills`
- v1 #8 `/Users/admin/codes/vibe-workflow/`
- v1 #9 `/Users/admin/codes/vibe-workflow/.claude/`

**对 expert 的指令**:本 9 项 v1 已审,本轮**不要重读、不要重新评分**;若需要参考 v1 对它们的判定,Read `discussion/006/forge/v1/stage-forge-006-v1.md` §1-§3。

## Y · 审阅视角

operator UI 三选(产品价值未勾):

✅ 架构设计 — 模块切分、抽象层次、可演化性
✅ 工程纪律 — 测试、CI、SDD、code review、hook 机制、SDD-workflow 形态
✅ Y5 重做代价 / 沉没成本 / 知识保留 — L/P/C 分层视角:V4 实装哪些 L 可保留 / P 可借鉴 / C 必须丢(operator binding 增,见 moderator-notes §六)

(产品价值未勾。expert 不需要从用户使用价值视角评 X。)

## Z · 参照系

**mode**: 对标 SOTA

**预期 SOTA 检索方向**(operator + prefill 推荐,Phase 2 expert 自行验证):
- Anthropic Claude Skills SDK v2(若 2026-05 已发布)
- Cursor Composer 跨仓 build 模式
- Codex CLI 5.4(若已 release)
- GitHub Spec Kit v2
- addy osmani agent-skills 体系
- superpowers skills 集合
- Cursor / Cline / Aider 等 agent-coding 主流工具的 workflow 设计
- Karpathy 等思想领袖关于 autonomous coding 的最新立场

**外部材料叠加**:
- moderator-notes.md(binding,P1+ 自动读)
- _x-input-draft-by-operator.md(operator 完整上下文,P1 自由参考)

## W · 产出形态

operator UI 全选 6 项(`moderator-notes.md §六` 已 binding):

✅ W1 verdict-only — 单一一句 verdict + ≤500 字 rationale
✅ W2 decision-list — 4 列矩阵(保留/调整/删除/新增)
✅ W3 refactor-plan — 按模块分组的改造方案
✅ W4 next-PRD — **聚焦 ADP-next/XenoDev 的 PRD**(非 framework 整体 PRD,per moderator-notes §五)
✅ W5 next-dev-plan — **拆 2 流**:B1 IDS 优化(SHARED-CONTRACT v2.0 + IDS CLAUDE.md L24 + plan-start 重写)+ B2 XenoDev L4 启动(per moderator-notes §五)
✅ W6 free-essay — 800-1500 字综合长文

## K · 用户判准

K 来源 = K1-K6 verbatim from proposal §006 + K7 (operator Append)。K_PROVENANCE = `appended`。

### K1-K6 verbatim from proposal §006

```
// from "想法":
给定一个PRD,claude code可以几乎没有人工干预的情况下自主完成开发任务。我需要一个**可靠的、自动化程度最高**解决方案。

// from "我为什么想做这个":
我是非软件开发背景。我可以将需求描述清楚,我也可以尝试构建较可靠的PRD。但是我缺少软件开发的经验,对各个规模(大中小型)的开发的方案、流程、规范等内容都没有把握。

// from "我已经想过的角度":
我最近一个月做了很多尝试:
1. 第一个项目名idea_gamma2。这个项目对我来说是一个大型项目,主要是构建一个人+agent共存的数字基建(通讯协议)。我尝试着梳理我的想法,并制定了一个technology roadmap。我会将开发分成几个phase来实现。每个phase开发前,我会用 pipeline SKILL 生成 playbook,然后让claude code按照playbook去实现。每个phase结束后,会用 phase-retrospective skill 更新 pipeline skill。每个phase都会定制相应的subagent,此外还构建了一部分skills。

2. 第二个项目为vibe-workflow。我是通过一个engineer team协作完成自动化开发。核心内容可以参考其 .claude/ 目录。

3. 第三个项目是autodev_pipe。该项目设计初衷是希望借鉴社区的vibe coding/agentic coding的最佳实践,实现一个agent自动化开发的pipeline。调研的一些结论、设想和计划记录在 solo_ai_pipeline_v3.1.md。其中主要借鉴最近流行的addy osmani的agent-skills,据说这套skills是把多年在 Google 级工程体系中沉淀出的工程纪律,迁移到 AI agent,让模型不只是更快地产出代码,而是在规格、测试、评审、验证和发布约束下产出更可信的软件。此外,本项目也吸收了superpowers的部分skills。核心目的是借助这些skills打造"专业的自动化开发流程"。

4. 第四个项目为当前repo。核心是为尝试将一个idea转化成一个成型的产品/软件。本repo在idea成型(产出PRD)后,会进入自动开发阶段。

// from "我诉求":
我希望双方凭借最强的AI专业能力以及最丰富的软件开发经验,通过调研、论证、思辨、构思、设计、整理归纳等方式,达成一套基于claude code实现**可靠**自动化开发的framework/pipeline的共识方案
```

### K7 · ADP-next 角色显式声明(operator Append,2026-05-09)

> **K7**:ADP-next 是 framework 的"待生下半边"产物;V4(`/Users/admin/codes/autodev_pipe`)是物证(operator 半年前停掉的"半成品"),**不是吸收对象**。K5("吸收四个项目尝试")中"ADP 项目"实际指 ADP-next 的设计意图(尚未生),而非 V4 这版具体实装。
>
> expert 不应把"V4 怎么做"当作 ADP-next 的设计起点;而应把 V4 视为参考之一(同 idea_gamma2 / vibe-workflow / 现 IDS 同级)。**ADP-next 的真实 grounding 详见 moderator-notes.md §一**。

(K_PROVENANCE: K1-K6 verbatim,K7 appended by operator 2026-05-09)

## 收敛强度

✅ **strong-converge**(operator 选择,operator binding via moderator-notes.md §六)

---

## convergence_intent · operator 备注(expert 必读)

> operator 2026-05-09 verbatim:"**每个 W 都要有收敛的内容,也允许在这个 W 上有其他补充/不同的建议、想法和评价**"

**expert 应将此 strong-converge 的具体执行方式理解为**:
- 主线 verdict **必须**收敛(W1 单一一句 / W2 4 列决策矩阵单一收敛 / W3 单一 refactor plan / W4 单一 PRD / W5 单一 dev plan / W6 单一长文论述)
- 残余分歧通过协议原生 **§"v0.2 note" 机制**(per SKILL.md L471)旁注式纳入,**不删丢**
- **不得**因为 strong-converge 就把双方 P3R2 §3 残余意见暴力压扁丢弃
- 双方 P3R2 应主动用 §"v0.2 note" 段落把次要建议 / 不同视角 / 警告挂上来,synthesizer 在 stage 文档保留这一段
- v1 跑出来 "converged-with-tempo-options" 形态(单一 verdict + 节奏 A/B 旁注)是本 intent 的近似实现 — 可参考但不限于此形态

---

## Summary for reviewers

**审阅标的总数**: 9(v1 #10 #11 + Δ-X1 至 Δ-X7);9 项 v1 #1-#9 标 no-rerun
**视角维度**: 架构设计 / 工程纪律 / Y5 重做代价
**参照系**: 对标 SOTA(Anthropic Skills SDK v2 / Cursor Composer / Codex CLI 5.4 / GitHub Spec Kit v2 / addy osmani / superpowers / Cursor / Cline / Aider / Karpathy 等)
**预期产出**: W1-W6 全选(W4 聚焦 ADP-next/XenoDev PRD;W5 拆 B1 IDS 优化 + B2 XenoDev L4)
**用户最在乎**(摘 K):达成基于 Claude Code 实现**可靠**自动化开发的 framework/pipeline 共识方案;K7 ADP-next 是 framework 待生下半边产物,V4 是物证不是吸收对象
**收敛模式**: strong-converge(operator intent: 主线收敛 + v0.2 note 旁注,不暴力压扁分歧)

**Binding 必读**(P1/P2/P3R1/P3R2 各 phase 自动 read):
- `discussion/006/forge/v2/moderator-notes.md`(126 行,5 件 binding 事实)
- `discussion/006/forge/v2/_x-input-draft-by-operator.md`(437 行,operator 完整上下文)
- v1 verdict 仅参考,**不绑定本轮 verdict**(per moderator-notes §四 + operator §四 决议)
