---
forge_id: 006
forge_version: v1
created: 2026-05-07T14:59:42Z
last_updated: 2026-05-07T14:59:42Z
convergence_mode: preserve-disagreement
prefill_source: proposals.md§006
x_hash: e45d68ee6dcc74d2c667976a28940c91
---

# forge-config · 006 · v1

本文件是 Phase 1-3R2 双方 reviewer 的"指南针"——X(审阅标的)、Y(视角)、Z(参照系)、W(产出形态)、K(用户判准)+ 收敛模式。

每个 phase Opus/Codex 进入时必须 refresh 本文件,确保所有产物对齐 K 的关切。

---

## X · 审阅标的(11 个)

来源:`prefill` (proposal §006 + bundle: pure-idea);全部 reachable(本工具 read-only 测试通过)。

⚠ 注意:其中 4 个 external-repo-dir(idea_gamma2 / vibe-workflow / autodev_pipe + 子目录)Codex 沙箱**可能** BLOCK;Phase 1 Opus 工作环境(本机 Claude Code)已确认全部可读;若 Codex Phase 1 BLOCK,Step 8 错误路径会接住给修复菜单。

| # | 类型 | 路径 / 引用 | 推荐读取范围 |
|---|---|---|---|
| 1 | pasted-text | proposal-text(`proposals/proposals.md` lines 224-247:§想法 + §我为什么想做这个 + §我已经想过的角度 + §我诉求) | 直读本文件即可;Opus 已在 prefill 阶段全文摘要 |
| 2 | external-repo-dir | `/Users/admin/codes/idea_gamma2` | 先 `ls` 顶层 → 选 README/CLAUDE.md/docs/ 入口读;不深读全部源码 |
| 3 | external-file | `/Users/admin/codes/idea_gamma2/docs/_archive/technology_roadmap.md` | Read 全文(roadmap 是设计意图核心载体) |
| 4 | external-file | `/Users/admin/codes/idea_gamma2/.claude/skills/pipeline/SKILL.md` | Read 全文(playbook 生成器,直接对应 K"framework/pipeline 共识方案"诉求) |
| 5 | external-file | `/Users/admin/codes/idea_gamma2/.claude/skills/phase-retrospective/phase-retrospective-skill.md` | Read 全文(phase 回溯 → 工程纪律 Y 视角必看) |
| 6 | external-repo-dir | `/Users/admin/codes/idea_gamma2/.claude/agents` (21 agents) | Glob `*.md` → 抽样读关键 agent(je-a/b/c/d/g1/g2/h/p/sre + arch + gatekeeper)了解角色分工模型 |
| 7 | external-repo-dir | `/Users/admin/codes/idea_gamma2/.claude/skills` (12 SKILL.md) | Glob `*/SKILL.md` → 选 pipeline / breaking-change / interface-contract / arch-spec / status-reporter 读;skills 体系的设计哲学 |
| 8 | external-repo-dir | `/Users/admin/codes/vibe-workflow/` | 先 `ls` 顶层 → 读 README.md / CLAUDE.md / AGENTS.md;了解 vibe-workflow 的整体姿态 |
| 9 | external-repo-dir | `/Users/admin/codes/vibe-workflow/.claude/` (10 agents + 11 commands + 7 rules + 4 skills) | Glob 后选 ai-fullstack-developer / code-reviewer / tech-lead 等核心 agent;commands 与 skills 选关键的读 |
| 10 | external-repo-dir | `/Users/admin/codes/autodev_pipe` | 先 `ls` 顶层(仓库较空,主要看 docs/ 与 solo_ai_pipeline 文件) |
| 11 | external-file | `/Users/admin/codes/autodev_pipe/solo_ai_pipeline_v3.1.md` | Read 全文(autodev_pipe 总设计文件,addy osmani agent-skills 借鉴的产物) |

---

## Y · 审阅视角(4 维度)

| # | 维度 | 解读 / 重点 |
|---|---|---|
| Y1 | 产品价值 | 这玩意儿对真实用户(human + agent 协作开发场景)是不是真有用?能不能让"非软件背景 + 强 PRD 描述能力"的 human 真的接近无人工干预完成开发? |
| Y2 | 架构设计 | 模块切分、抽象层次(skill/agent/command 三层?)、可演化性(每个 phase 跑完能更新 pipeline 自身?)、composability |
| Y3 | 工程纪律 | 测试、CI、SDD、code review、phase 回溯机制、skills 是否真的能强制"在规格、测试、评审、验证和发布约束下产出"? |
| Y4 | 开发质量保障 / 稳定性 / SOTA 对标度 | (用户自定义)forge 后的 framework 在真实项目(中大型)上能否产出**可靠、稳定、达到 SOTA 水准**的软件?和现有 SOTA(Anthropic Skills / addy osmani / superpowers / cursor / aider 等)对标的成熟度差距在哪? |

---

## Z · 参照系

**Mode**:对标 SOTA(双方在 Phase 2 各自检索领域 SOTA,prior-art / 失败案例 / 演化路径)

**Allowed in P2 search**:
- agentic coding / vibe coding 主流工具(cursor / cline / aider / windsurf / claude-code / copilot agent mode)
- Anthropic Skills(addy osmani agent-skills)
- superpowers skills 体系
- Anthropic measuring-agent-autonomy / Microsoft ACE / GitHub Spec Kit / Devin
- Karpathy autoresearch 等思想领袖立场
- 学术研究(autonomous coding / SWE-bench / SWE-agent / AgentLens 等)
- 失败案例 / 公开的 post-mortem

**Forbidden**:
- tech-stack-deep-dive(具体哪个语言哪个框架)
- pricing / 商业模式
- 实施级别的 step-by-step 教程

---

## W · 产出形态(6 项全选)

| # | 形态 | 在 stage 文档中的位置 |
|---|---|---|
| W1 | verdict-only | §1(开头,≤500 字单段;preserve-disagreement 时双 verdict 并列) |
| W2 | decision-list | §2(4 列矩阵:对 4 个 deprecated repo 逐个 keep/refactor/cut/new) |
| W3 | refactor-plan | §3(按模块分组的改造方案) |
| W4 | next-PRD | §4(下一版 PRD 草案,可直接进 L4 plan-start) |
| W5 | next-dev-plan | §5(按 phase / milestone 切分) |
| W6 | free-essay | §6(800-1500 字长篇综合;preserve-disagreement 模式下可分别给两个 verdict 写各自 free-essay) |

预计 stage 文档总字数:~3000-4500 字(全 W 形态会很长)。

---

## K · 用户判准

> 来源:prefill verbatim · proposal §006(`proposals/proposals.md` lines 224-247);K_PROVENANCE = verbatim

```
// from "想法":
给定一个PRD,claude code可以几乎没有人工干预的情况下自主完成开发任务。我需要一个**可靠的、自动化程度最高**解决方案。

// from "我为什么想做这个":
我是非软件开发背景。我可以将需求描述清楚,我也可以尝试构建较可靠的PRD。但是我缺少软件开发的经验,对各个规模(大中小型)的开发的方案、流程、规范等内容都没有把握。

// from "我已经想过的角度"(非路径文字部分):
我最近一个月做了很多尝试:
1. 第一个项目名idea_gamma2。这个项目对我来说是一个大型项目,主要是构建一个人+agent共存的数字基建(通讯协议)。我尝试着梳理我的想法,并制定了一个technology roadmap。我会将开发分成几个phase来实现。每个phase开发前,我会用 pipeline SKILL 生成 playbook,然后让claude code按照playbook去实现。每个phase结束后,会用 phase-retrospective skill 更新 pipeline skill。每个phase都会定制相应的subagent,此外还构建了一部分skills。
2. 第二个项目为vibe-workflow。我是通过一个engineer team协作完成自动化开发。核心内容可以参考其 .claude/ 目录。
3. 第三个项目是autodev_pipe。该项目设计初衷是希望借鉴社区的vibe coding/agentic coding的最佳实践,实现一个agent自动化开发的pipeline。调研的一些结论、设想和计划记录在 solo_ai_pipeline_v3.1.md。其中主要借鉴最近流行的addy osmani的agent-skills,据说这套skills是把多年在 Google 级工程体系中沉淀出的工程纪律,迁移到 AI agent,让模型不只是更快地产出代码,而是在规格、测试、评审、验证和发布约束下产出更可信的软件。此外,本项目也吸收了superpowers的部分skills。核心目的是借助这些skills打造"专业的自动化开发流程"。
4. 第四个项目为当前repo。核心是为尝试将一个idea转化成一个成型的产品/软件。本repo在idea成型(产出PRD)后,会进入自动开发阶段。

// from "我诉求":
我希望双方凭借最强的AI专业能力以及最丰富的软件开发经验,通过调研、论证、思辨、构思、设计、整理归纳等方式,达成一套基于claude code实现**可靠**自动化开发的framework/pipeline的共识方案
```

---

## 收敛模式

**preserve-disagreement** — 允许并存 2 个 verdict,各自独立完整。

P3R2 不强制 finalize 单一 verdict;synthesizer 在 stage 文档里输出双轨 path,human 看完后选边或合并。这与 K 中"通过调研、论证、思辨"的开放探索姿态一致。
