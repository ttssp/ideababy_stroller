# Forge intake prefill draft · 005 · v1

**Generated**: 2026-05-07T00:00:00Z
**Subagent**: forge-intake-prefill
**Proposal status**: found
**Forge target type**: root-idea

## Detected proposal section

**Title**: `005`: auto agentic coding
**proposals.md line**: 198
**Body byte count**: ~1180(粗算 UTF-8)
**Fields detected**: 想法, 我为什么想做这个, 我已经想过的角度, 我诉求
**未出现的 optional 字段**: 我已知的相邻方案/竞品, 我的初始约束, 我的倾向, 还在困扰我的问题

> 注:proposal 段落比较精简(无 Z 段、无约束/倾向段)。Z mode 若选"对标指定列表",human 需手粘对标项。K seed 主要由 4 个 ### 子节拼装。

---

## X candidates (raw)

### From proposal section(8 条 path 候选 + 1 条 proposal-text)

- [x] **proposal-text**:`005` 想法 + 我为什么 + 我诉求(全段拼装,~1180 字节)
  - type: pasted-text
  - reachable: n/a
  - default: ☑ checked(idea 本身的核心文本)
  - source_line: proposals.md:198-220

- [ ] `/Users/admin/codes/idea_gamma2`
  - type: external-path(directory)
  - reachable: ✅(EISDIR — 目录存在)
  - default: ☑ checked(idea_gamma2 是 human 的"大型项目"、L2 已多次 verbatim 引用,核心审阅标的)
  - source_line: proposals.md:211
  - ⚠ Codex 默认沙箱可能 BLOCK 该路径(在仓库外),Phase 1 可能需要 `cp -r` 拷贝到 `_forge-targets/` 或调整 Codex sandbox scope

- [ ] `/Users/admin/codes/idea_gamma2/docs/_archive/technology_roadmap.md`
  - type: external-path(file)
  - reachable: ✅(Read 第 1 行成功:"⚠️ ARCHIVED: previously under docs/")
  - default: ☑ checked(roadmap 是 idea_gamma2 的核心设计意图载体)
  - source_line: proposals.md:211
  - ⚠ Codex sandbox 同上

- [ ] `/Users/admin/codes/idea_gamma2/.claude/skills/pipeline/SKILL.md`
  - type: external-path(file)
  - reachable: ✅
  - default: ☑ checked(playbook 生成器,直接对应 K 中"framework/pipeline 共识方案"诉求)
  - source_line: proposals.md:211

- [ ] `/Users/admin/codes/idea_gamma2/.claude/skills/phase-retrospective/phase-retrospective-skill.md`
  - type: external-path(file)
  - reachable: ✅
  - default: ☑ checked(phase 回溯机制,对应"工程纪律"Y 视角)
  - source_line: proposals.md:211

- [ ] `/Users/admin/codes/idea_gamma2/.claude/agents`
  - type: external-path(directory)
  - reachable: ✅(EISDIR)
  - default: ☑ checked(per-phase 定制 subagent,架构设计审阅必看)
  - source_line: proposals.md:211

- [ ] `/Users/admin/codes/idea_gamma2/.claude/skills`
  - type: external-path(directory)
  - reachable: ✅(EISDIR)
  - default: ☑ checked(skills 库,对应 addy osmani 模式的 idea_gamma2 实现)
  - source_line: proposals.md:211

- [ ] `/Users/admin/codes/vibe-workflow/`
  - type: external-path(directory)
  - reachable: ✅(EISDIR)
  - default: ☑ checked(项目 2 — engineer team 协作模型)
  - source_line: proposals.md:213

- [ ] `/Users/admin/codes/vibe-workflow/.claude/`
  - type: external-path(directory)
  - reachable: ✅(已 glob 出 ~50 个 agents/commands/skills/rules 文件,内容丰富)
  - default: ☑ checked(vibe-workflow 核心 — agent 角色分工、commands、rules)
  - source_line: proposals.md:213

- [ ] `/Users/admin/codes/autodev_pipe`
  - type: external-path(directory)
  - reachable: ✅(EISDIR)
  - default: ☑ checked(项目 3 — addy osmani agent-skills 直接对标实现)
  - source_line: proposals.md:215

- [ ] `/Users/admin/codes/autodev_pipe/solo_ai_pipeline_v3.1.md`
  - type: external-path(file)
  - reachable: ✅(Read 第 1 行成功:"# 单人 + AI 团队产品级开发流水线 v3.1")
  - default: ☑ checked(autodev_pipe 的总设计文件,对应 K 诉求中"调研、论证、思辨、构思、设计")
  - source_line: proposals.md:215

> ⚠ "项目 4 = 当前 repo"(proposal §"我已经想过的角度" item 4)无显式路径。如果 human 想把当前 repo 也作为 X 标的,在 0.5.5.b custom 里加 `/Users/admin/codes/ideababy_stroller`(或仓库内子目录如 `.claude/`、`discussion/`)。

### From discussion/005/(intermediate-layer products)

- [ ] `discussion/005/L2/stage-L2-explore-005.md`(~14k chars / ~4.7k tokens)
  - type: stage-doc
  - reachable: ✅
  - default: ☐ unchecked(by default — Bundle 选 from-L2/full-history 时勾)
  - source: glob `L2/stage-L2-explore-*.md`

- [ ] `discussion/005/L3/stage-L3-scope-005.md`(estimated ~12k chars / ~4k tokens)
  - type: stage-doc
  - reachable: ✅
  - default: ☑ checked(by default — L3 是最近 stage,**from-L3 是默认推荐**;包含 L2 verdict + 3 个 peer PRD candidates)
  - source: glob `L3/stage-L3-scope-*.md`

- [ ] `discussion/005/L2/L2R1-Opus47Max.md`
  - type: raw-round
  - reachable: ✅
  - default: ☐(advanced — full-history Bundle 才勾)

- [ ] `discussion/005/L2/L2R1-GPT55xHigh.md`
  - type: raw-round
  - reachable: ✅
  - default: ☐(advanced)

- [ ] `discussion/005/L2/L2R2-Opus47Max.md`
  - type: raw-round
  - reachable: ✅
  - default: ☐(advanced)

- [ ] `discussion/005/L2/L2R2-GPT55xHigh.md`
  - type: raw-round
  - reachable: ✅
  - default: ☐(advanced)

- [ ] `discussion/005/L3/L3R0-intake.md`
  - type: raw-round(intake)
  - reachable: ✅
  - default: ☐(advanced — full-history 才勾;包含 human 在 L3R0 给的硬约束 verbatim)

- [ ] `discussion/005/L3/L3R1-Opus47Max.md`
  - type: raw-round
  - reachable: ✅
  - default: ☐(advanced)

- [ ] `discussion/005/L3/L3R1-GPT55xHigh.md`
  - type: raw-round
  - reachable: ✅
  - default: ☐(advanced)

- [ ] `discussion/005/L3/L3R2-Opus47Max.md`
  - type: raw-round
  - reachable: ✅
  - default: ☐(advanced)

- [ ] `discussion/005/L3/L3R2-GPT55xHigh.md`
  - type: raw-round
  - reachable: ✅
  - default: ☐(advanced)

> 无 L1 stage doc(005 走 `/inspire-start --mode=skip` 直入 L2 — 见 L2 stage doc §"Source")。
> 无 sibling fork(`discussion/005/005-*` 不存在 — 005 尚未 fork)。

### Starting-point quick-pick groups

- **[Bundle:pure-idea]**(总是显示)
  - X 数量:11(proposal-text + 10 reachable external paths)
  - pre-checked:proposal-text + 全部 8 个 idea_gamma2/vibe-workflow/autodev_pipe 路径(idea_gamma2 × 6、vibe-workflow × 2、autodev_pipe × 2)
  - 适用场景:human 想让双专家**绕开 L2/L3 imagination**,纯凭"已经存在的 4 个 repo + idea 本身"做 SOTA 对标拍板

- **[Bundle:from-L2]**(L2 stage exists)
  - X 数量:12(pure-idea 全部 + L2 stage doc)
  - pre-checked:pure-idea + `discussion/005/L2/stage-L2-explore-005.md`
  - 适用场景:human 想让 forge 在 L2 verdict(Y-with-conditions)的基础上做技术审阅,但**不想被 L3 的 3 个候选预先 anchor**

- **[Bundle:from-L3]**(L3 stage exists,**default 推荐**)
  - X 数量:12(pure-idea 全部 + L3 stage doc)
  - pre-checked:pure-idea + `discussion/005/L3/stage-L3-scope-005.md`
  - 适用场景:典型 forge 场景 — 已有 L3 candidate 菜单(A/B/C 3 个 peer PRD),需要双专家拍板"哪个最该 ship 或综合方案"。L3 stage doc 已隐含 L2 verdict 摘要,信息密度高
  - **这是 005 的推荐起点**

- **[Bundle:full-history]**(任一 stage exists)
  - X 数量:22(pure-idea + L2 + L3 stage docs + 9 raw rounds + L3R0 intake)
  - pre-checked:全部上述 + 全部 raw rounds
  - estimated_tokens: **~35-50k tokens**(L2 stage 4.7k + L3 stage 4k + 9 raw rounds × ~3k = 27k + proposal 0.3k + 4 个外部 dir Read 时按 5k 兜底 × 4 = 20k)
  - ⚠ **远超 8k 软警告阈值** — 主命令在 0.5.5.a 选此 Bundle 时会软警告

- **[Bundle:custom]**(总是显示)
  - 主命令进 0.5.5.b 完整多选

---

## K seed (suggested, editable by user)

```
// from "想法":
给定一个PRD,claude code可以几乎没有人工干预的情况下自主完成开发任务。我需要一个**可靠的、自动化程度最高**解决方案。

// from "我为什么想做这个":
我是非软件开发背景。我可以将需求描述清楚,我也可以尝试构建较可靠的PRD。但是我缺少软件开发的经验,对各个规模(大中小型)的开发的方案、流程、规范等内容都没有把握。

// from "我已经想过的角度"(非路径文字部分,保留 numbered list 结构):
我最近一个月做了很多尝试:
1. 第一个项目名 idea_gamma2。这个项目对我来说是一个大型项目,主要是构建一个人+agent共存的数字基建(通讯协议)。我尝试着梳理我的想法,并制定了一个 technology roadmap。我会将开发分成几个 phase 来实现。每个 phase 开发前,我会用 pipeline SKILL 生成 playbook,然后让 claude code 按照 playbook 去实现。每个 phase 结束后,会用 phase-retrospective skill 更新 pipeline skill。每个 phase 都会定制相应的 subagent,此外还构建了一部分 skills。
2. 第二个项目为 vibe-workflow。我是通过一个 engineer team 协作完成自动化开发。核心内容可以参考 .claude/。
3. 第三个项目是 autodev_pipe。该项目设计初衷是希望借鉴社区的 vibe coding/agentic coding 的最佳实践,实现一个 agent 自动化开发的 pipeline。调研的一些结论、设想和计划记录在 solo_ai_pipeline_v3.1.md。其中主要借鉴最近流行的 addy osmani 的 agent-skills,据说这套 skills 是把多年在 Google 级工程体系中沉淀出的工程纪律,迁移到 AI agent,让模型不只是更快地产出代码,而是在规格、测试、评审、验证和发布约束下产出更可信的软件。此外,本项目也吸收了 superpowers 的部分 skills。核心目的是借助这些 skills 打造"专业的自动化开发流程"。
4. 第四个项目为当前 repo。核心是为尝试将一个 idea 转化成一个成型的产品/软件。本 repo 在 idea 成型(产出 PRD)后,会进入自动开发阶段。

// from "我诉求":
我希望双方凭借最强的 AI 专业能力以及最丰富的软件开发经验,通过调研、论证、思辨、构思、设计、整理归纳等方式,达成一套基于 claude code 实现**可靠**自动化开发的 framework/pipeline 的共识方案。
```

**Byte count**: ~1850(UTF-8;中文按 3 字节/字粗算)
**Quality flag**: K seed 长度 >= 80 chars: **ok**(远超阈值)

---

## Z candidates (suggested if mode=对标指定列表)

**proposal §005 没有 `### 我已知的相邻方案/竞品` 段** — Z mode 选"对标指定列表"时由 human 手粘。

但 K seed 内文已显式提到几个对标候选(human 选 mode=对标指定列表 时可考虑):

```
// 从 K seed 内文提取的隐含对标候选(human 自行决定是否纳入 Z 列表):
- addy osmani 的 agent-skills(K 内显式 evangelize 的对标对象)
- superpowers 的 skills(K 内提到部分吸收)
- (若想用 SOTA mode,L2 stage doc §6 已列了完整 prior-art 表:Devin、Cursor、aider、claude-code、Anthropic measuring-agent-autonomy、Microsoft ACE、GitHub Spec Kit 等;直接用 L2 表更高效)
```

> 推荐 **Z mode = 对标 SOTA**(让双方在 P2 自由检索),原因:K 中 human 明确诉求"双方凭借最强的 AI 专业能力以及最丰富的软件开发经验,通过调研、论证、思辨..."—— 暗示希望开放搜索而非锁死小列表。

---

## Y default recommendation

| Y 维度 | 默认 | 触发关键词 evidence |
|---|---|---|
| 产品价值 | ✅ | (always — proposal 主诉求"可靠的自动化开发解决方案"是产品价值问题) |
| 架构设计 | ✅ | "framework/pipeline 的共识方案"(K §诉求, verbatim) |
| 工程纪律 | ✅ | "工程纪律,迁移到 AI agent"(K §我已经想过的角度 item 3, verbatim);"在规格、测试、评审、验证和发布约束下产出更可信的软件" |
| 安全 | ☐ | (无命中;proposal 未提到密钥/权限/输入验证) |
| 教学价值 | ☐ | (无显式命中;但 L2 §3 场景 E "教学模式"暗示;human 可勾上) |
| 商业可行 | ☐ | (无命中 — 005 是 personal/工作流 idea,非商业产品) |
| 用户体验 | ☐ | (proposal 未直接命中;但 L3 PRD 候选必然涉及 form factor — human 可勾上) |

---

## W default recommendation

| W 形态 | 默认 | 理由 |
|---|---|---|
| verdict-only | ✅ | (always — human 诉求"达成共识方案",需要锐利单一 verdict) |
| decision-list | ✅ | (always — 4 个项目历史让 keep/cut/new 矩阵价值很高:idea_gamma2 的 pipeline+phase-retro 哪些保留、autodev_pipe 的 addy osmani 借鉴哪些保留、vibe-workflow 的 engineer team 哪些保留) |
| next-PRD | ✅ | (always — L3 已有 3 个 peer PRD candidates,forge verdict 自然引向"下一版收敛 PRD";K seed 也包含 framework 共识诉求) |
| refactor-plan | ✅ | "4 个 repo 都被 deprecate 过"(L2 §6 condition 4 verbatim,human 处于 redesign vs incremental optimize 的真实抉择中) |
| next-dev-plan | ☐ | (proposal 未提 phase/milestone,虽然 idea_gamma2 用 phase 分发;forge 的 W 在 dev-plan 上不如 next-PRD 强;若 human 想要 phase 切分可手勾) |
| free-essay | ☐ | (默认不勾) |

---

## Reachability check on all X paths

| Path | Reachable | Type | Note |
|---|---|---|---|
| `/Users/admin/codes/idea_gamma2` | ✅(EISDIR) | external-repo-dir | Codex sandbox 可能 BLOCK;P1 启动前考虑 `cp -r` 到 `_forge-targets/` 或调 Codex scope |
| `/Users/admin/codes/idea_gamma2/docs/_archive/technology_roadmap.md` | ✅ | external-file | Read 1 行成功 |
| `/Users/admin/codes/idea_gamma2/.claude/skills/pipeline/SKILL.md` | ✅ | external-file | Read 1 行成功 |
| `/Users/admin/codes/idea_gamma2/.claude/skills/phase-retrospective/phase-retrospective-skill.md` | ✅ | external-file | Read 1 行成功 |
| `/Users/admin/codes/idea_gamma2/.claude/agents` | ✅(EISDIR) | external-dir | 目录存在 |
| `/Users/admin/codes/idea_gamma2/.claude/skills` | ✅(EISDIR) | external-dir | 目录存在 |
| `/Users/admin/codes/vibe-workflow/` | ✅(EISDIR) | external-repo-dir | Codex sandbox 可能 BLOCK |
| `/Users/admin/codes/vibe-workflow/.claude/` | ✅(EISDIR) | external-dir | Glob 列出 ~50 个文件 |
| `/Users/admin/codes/autodev_pipe` | ✅(EISDIR) | external-repo-dir | Codex sandbox 可能 BLOCK |
| `/Users/admin/codes/autodev_pipe/solo_ai_pipeline_v3.1.md` | ✅ | external-file | Read 1 行成功:"# 单人 + AI 团队产品级开发流水线 v3.1" |
| `discussion/005/L2/stage-L2-explore-005.md` | ✅ | stage-doc | 仓库内 |
| `discussion/005/L3/stage-L3-scope-005.md` | ✅ | stage-doc | 仓库内 |
| `discussion/005/L2/L2R{1,2}-{Opus47Max,GPT55xHigh}.md` | ✅ × 4 | raw-round | 仓库内 |
| `discussion/005/L3/L3R0-intake.md` | ✅ | raw-round | 仓库内 |
| `discussion/005/L3/L3R{1,2}-{Opus47Max,GPT55xHigh}.md` | ✅ × 4 | raw-round | 仓库内 |

> 共 10 个外部路径全部 reachable(本工具),但 Codex 沙箱跑 P1 时可能 BLOCK 4 个外部 dir;file 类(roadmap.md / SKILL.md / phase-retro skill / solo_ai_pipeline_v3.1.md)较小且明确,Codex BLOCK 概率低。

---

## Quality flags

- [x] proposal section detected:✅
- [x] >=1 X candidate extracted:✅(11 reachable + 11 stage/raw)
- [x] K seed >= 80 chars:✅(~1850 字节)
- [x] At least 1 Y default recommended:✅(产品价值 + 架构设计 + 工程纪律)
- [x] At least 1 W default recommended:✅(verdict-only + decision-list + next-PRD + refactor-plan)

---

## Prefill summary(给主命令的简要)

```
prefill_status: success
draft_file: discussion/005/forge/v1/_prefill-draft.md
x_candidates: 22
k_seed_bytes: 1850
z_candidates_present: false
intermediate_products_found: [L2-stage, L3-stage, L2-raw-rounds-x4, L3-raw-rounds-x4, L3R0-intake]
y_recommended: [产品价值, 架构设计, 工程纪律]
w_recommended: [verdict-only, decision-list, next-PRD, refactor-plan]
estimated_tokens_full_history: 45k
```
