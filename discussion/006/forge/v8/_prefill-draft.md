# Forge intake prefill draft · 006 · v8

**Generated**: 2026-07-13
**Subagent**: forge-intake-prefill
**Proposal status**: found
**Forge target type**: root-idea

> ⚠ **本轮 v8 的真实 X 主料不是 proposal 内文,而是 XenoDev 的 dogfood-backlog**
> (framework 缺口攒批)。proposal §006 的 external paths 全是 mac 时代路径
> (`/Users/admin/codes/...`),迁到 Ubuntu 后**全部 unreachable**(见 MEMORY
> 「mac→Ubuntu 迁移」:这类硬编码 mac 路径多是 by-design 历史文件,别改源码)。
> caller 明确本轮 X 主料 = `/home/ys/codes/XenoDev/dogfood-backlog.md`
> 的 KG-B2..B7 六条 + operator 新诉求「session-per-idea worktree 隔离」。

> ⚠ **v7 stage doc 不在标准 forge 路径下**。caller 提到「v7 结论延续上下文」,
> 但 `discussion/006/forge/v7/` 目录不存在,`stage-forge-006-v7.md` 也 glob
> 不到。标准 forge 路径下**最近可达的 prior-forge stage doc 是 v5**
> (`discussion/006/forge/v5/stage-forge-006-v5.md`)。full-history bundle 用
> v5 作为 prior-forge 锚。若 human 知道 v7 定稿另存在别处,请在 0.5.5 手加。

## Detected proposal section

**Title**: auto agentic coding
**proposals.md line**: 224
**Body byte count**: ~1250 chars(想法+我为什么+我已经想过的+我诉求 四段)
**Fields detected**: 想法, 我为什么想做这个, 我已经想过的角度, 我诉求
**未检测到**: 我已知的相邻方案/竞品(→ Z 空), 我的初始约束, 我的倾向, 还在困扰我的问题

## X candidates (raw)

### From proposal section

- [x] **proposal-text**:"`auto agentic coding` §想法 + 我为什么想做这个 + 我诉求(可靠、自动化程度最高的 claude code 自主开发 framework/pipeline 共识方案)"
  - type: pasted-text
  - reachable: n/a
  - default: ☑ checked(idea 本身的核心文本 — 但对 v8 是**背景**,主料在 dogfood-backlog)
  - source_line: proposals.md:229-246

- [ ] `/Users/admin/codes/idea_gamma2`
  - type: external-path
  - reachable: ⚠ unreachable(Read 报 File does not exist — mac 路径,已迁 Ubuntu)
  - default: ☐ unchecked(mac 历史路径,by-design stale · human 若真要可指向新路径)
  - source_line: proposals.md:237

- [ ] `/Users/admin/codes/idea_gamma2/docs/_archive/technology_roadmap.md`
  - type: external-path
  - reachable: ⚠ unreachable(Read 报 File does not exist)
  - default: ☐ unchecked
  - source_line: proposals.md:237

- [ ] `/Users/admin/codes/idea_gamma2/.claude/skills/pipeline/SKILL.md`
  - type: external-path
  - reachable: ⚠ unreachable(mac 路径)
  - default: ☐ unchecked
  - source_line: proposals.md:237

- [ ] `/Users/admin/codes/idea_gamma2/.claude/skills/phase-retrospective/phase-retrospective-skill.md`
  - type: external-path
  - reachable: ⚠ unreachable(mac 路径)
  - default: ☐ unchecked
  - source_line: proposals.md:237

- [ ] `/Users/admin/codes/idea_gamma2/.claude/agents`
  - type: external-path
  - reachable: ⚠ unreachable(mac 路径)
  - default: ☐ unchecked
  - source_line: proposals.md:237

- [ ] `/Users/admin/codes/idea_gamma2/.claude/skills`
  - type: external-path
  - reachable: ⚠ unreachable(mac 路径)
  - default: ☐ unchecked
  - source_line: proposals.md:237

- [ ] `/Users/admin/codes/vibe-workflow/`
  - type: external-path
  - reachable: ⚠ unreachable(mac 路径)
  - default: ☐ unchecked
  - source_line: proposals.md:239

- [ ] `/Users/admin/codes/vibe-workflow/.claude/`
  - type: external-path
  - reachable: ⚠ unreachable(mac 路径)
  - default: ☐ unchecked
  - source_line: proposals.md:239

- [ ] `/Users/admin/codes/autodev_pipe`
  - type: external-path
  - reachable: ⚠ unreachable(mac 路径)
  - default: ☐ unchecked
  - source_line: proposals.md:241

- [ ] `/Users/admin/codes/autodev_pipe/solo_ai_pipeline_v3.1.md`
  - type: external-path
  - reachable: ⚠ unreachable(mac 路径)
  - default: ☐ unchecked
  - source_line: proposals.md:241

### From caller-supplied v8 batch material(本轮真实 X 主料)

- [x] `/home/ys/codes/XenoDev/dogfood-backlog.md`
  - type: external-path(XenoDev repo · 本机绝对路径)
  - reachable: ✅(Read 第 1 行成功 · 601 lines · ~85k token 读满成本)
  - default: ☑ checked(**本轮 forge 的核心审阅标的** — framework 缺口攒批)
  - source: caller 明示 · 含 KG-B2/B3/B4/B5/B6/B7 六条框架缺口(均 medium~high,
    均标「攒批回 IDS forge」)+ operator 新诉求「session-per-idea worktree 隔离」
  - note: 全文很大;Phase 1 Opus 可只聚焦 KG-B2..B7 段(约 line 508-599)+ 相关簇。
    ⚠ 若 full-read 会吃 ~85k token,建议 Phase 1 用 Grep 定位 KG-B* 段落而非整读。

### From discussion/006/ (intermediate-layer products)

**无 L1/L2/L3 stage docs** —— 006 是 forge-only idea(L0 直接由 /expert-forge
bootstrap,从未走 L1-L3 pipeline)。故 from-L2 / from-L3 bundle **不适用**。

可选的 prior-forge stage docs(横切历史 verdict,非 pipeline stage):

- [ ] `discussion/006/forge/v5/stage-forge-006-v5.md`
  - type: stage-doc(prior-forge verdict · "多 worktree 并发安全加固 + evidence binding")
  - reachable: ✅(~252 非空行 · ~6k token)
  - default: ☑ checked(最近**可达**的 prior-forge 结论 — 给 Phase 1 做延续上下文)
  - source: glob forge/v5/stage-forge-006-v5.md

- [ ] `discussion/006/forge/v4/stage-forge-006-v4.md`
  - type: stage-doc(prior-forge verdict)
  - reachable: ✅(~282 非空行 · ~7k token)
  - default: ☐ unchecked(full-history bundle 才勾)
  - source: glob forge/v4/stage-forge-006-v4.md

- [ ] `discussion/006/forge/v3/stage-forge-006-v3.md`
  - type: stage-doc(prior-forge verdict)
  - reachable: ✅
  - default: ☐ unchecked(advanced · full-history 才勾)

- [ ] `discussion/006/forge/{v1,v2}/stage-forge-006-v{1,2}.md`
  - type: stage-doc(最早两版 forge verdict)
  - reachable: ✅
  - default: ☐ unchecked(advanced · 通常不需回溯到 v1/v2)

### Starting-point quick-pick groups

- **[Bundle:pure-idea]**(总是显示)
  - X 数量:2(proposal-text + dogfood-backlog)
  - pre-checked:
    - proposal-text(auto agentic coding 核心文本)
    - /home/ys/codes/XenoDev/dogfood-backlog.md
  - note: proposal 的 external paths 全 unreachable,不进 pure-idea 预勾;dogfood-backlog
    虽是 external,但它是本轮真实 idea 主体,归入 pure-idea。

- **[Bundle:from-L2]** —— **不适用**(006 无 L2 stage doc)

- **[Bundle:from-L3]** —— **不适用**(006 无 L3 stage doc)

- **[Bundle:with-prior-verdict]**(prior-forge stage 存在 · **default 推荐**)
  - X 数量:3
  - pre-checked: pure-idea 全部 + `discussion/006/forge/v5/stage-forge-006-v5.md`
  - note: 用最近可达 prior-forge(v5)替代常规 from-L3 default,因 006 无 pipeline stage。

- **[Bundle:full-history]**(任一 prior stage 存在时显示)
  - X 数量:7(pure-idea 2 + v1..v5 五份 prior-forge stage docs)
  - pre-checked: proposal-text + dogfood-backlog + v1/v2/v3/v4/v5 stage docs
  - estimated_tokens: ~110k(dogfood-backlog ~85k + 5 份 stage docs ~30k)
    ⚠ **≥ 8k · 主命令会软警告** —— dogfood-backlog 单独就 ~85k,若整读会吃满
    Phase 1 上下文。强烈建议改用 with-prior-verdict + Grep 定位 KG-B* 段,别 full-read。

- **[Bundle:custom]**(总是显示 — human 自己挑 · 尤其若 v7 定稿另存别处需手加)

## K seed (suggested, editable by user)

```
// from "想法":
给定一个PRD,claude code可以几乎没有人工干预的情况下自主完成开发任务。我需要一个**可靠的、自动化程度最高**解决方案。

// from "我为什么想做这个":
我是非软件开发背景。我可以将需求描述清楚,我也可以尝试构建较可靠的PRD。但是我缺少软件开发的经验,对各个规模(大中小型)的开发的方案、流程、规范等内容都没有把握。

// from "我已经想过的角度"(非路径文字部分,保留 numbered list 结构):
我最近一个月做了很多尝试:
1. 第一个项目名idea_gamma2,是一个大型项目(人+agent共存的数字基建/通讯协议)。梳理想法+定 technology roadmap,开发分几个 phase,每 phase 用 pipeline SKILL 生成 playbook 让 claude code 实现,phase 结束用 phase-retrospective 更新 pipeline skill,每 phase 定制 subagent + 构建 skills。
2. 第二个项目 vibe-workflow,通过一个 engineer team 协作完成自动化开发。
3. 第三个项目 autodev_pipe,借鉴社区 vibe/agentic coding 最佳实践实现 agent 自动化开发 pipeline;吸收 addy osmani 的 agent-skills(把 Google 级工程体系的工程纪律迁移到 AI agent,在规格/测试/评审/验证/发布约束下产可信软件)+ superpowers 部分 skills。
4. 第四个项目为当前 repo(IDS),把 idea 转化成成型产品/软件,idea 成型(产出PRD)后进入自动开发阶段。

// from "我诉求":
我希望双方凭借最强的AI专业能力以及最丰富的软件开发经验,通过调研、论证、思辨、构思、设计、整理归纳等方式,达成一套基于claude code实现**可靠**自动化开发的framework/pipeline的共识方案。

// [v8 上下文补充 · caller 明示 · human 可保留或删]:
本轮 v8 forge 的真实审议主体不是重开 006 大方向,而是审 XenoDev dogfood-backlog
攒批的六条框架缺口(KG-B2 parallel-builder「一切 merge 回 main」假设被
blocked-handback 打破 / KG-B3 red-green-log TDD 证据被 .gitignore 吞 /
KG-B4 gate 类 task PASS 无机器强制·防 V4 gate 可绕过 / KG-B5 LlmClient 无
system/user role 分离·prompt-injection 只能 prompt 内防 / KG-B6
credential-isolation hook 对 heredoc/变量拼路径/$()误报 fail-closed /
KG-B7 盲测 gate 需框架层单次执行强制·防重放取答案),外加 operator 新诉求
「session-per-idea worktree 隔离」。收敛出 v8 verdict + 各条改造方案 →
下发 XenoDev 半边 brief。
```

**Byte count**: ~1900 chars(远超 80 门槛)
**Quality flag**: K seed 长度 >=80 chars: ok

## Z candidates (suggested if mode=对标指定列表)

**原文原样**:

```
无 —— proposal §006 没有 ### 我已知的相邻方案/竞品 段。
Z mode 若选「对标指定列表」由 human 手粘;若选「对标 SOTA」双方 P2 自行检索
(006 历史 forge 对标过 addy osmani agent-skills / Spec Kit / Devin / Cursor
等,可沿用)。本轮偏框架自审(dogfood 缺口),Z 可能选「无对标 / 仅内部一致性」。
```

## Y default recommendation

| Y 维度 | 默认 | 触发关键词 evidence |
|---|---|---|
| 产品价值 | ✅ | "达成一套基于claude code实现可靠自动化开发的framework" |
| 架构设计 | ✅ | "framework/pipeline的共识方案"(命中 framework/pipeline) |
| 工程纪律 | ✅ | "在规格、测试、评审、验证和发布约束下产出更可信的软件"(命中工程纪律/流程) |
| 安全 | ✅ | "credential-isolation hook 对 heredoc/变量拼路径误报 fail-closed"(KG-B6·命中密钥/权限)+ "prompt-injection 防御"(KG-B5) |
| 教学价值 | ☐ | (无命中) |
| 商业可行 | ☐ | (无命中) |
| 用户体验 | ☐ | (无命中) |

> note: 常规规则「framework/pipeline/工程纪律」命中 → 架构设计+工程纪律+产品价值
> 三件套 ✅。本轮 X 主料 dogfood-backlog 含 KG-B5(prompt-injection)/KG-B6
> (credential-isolation)两条安全相关,额外给**安全** ✅。

## W default recommendation

| W 形态 | 默认 | 理由 |
|---|---|---|
| verdict-only | ✅ | (always) |
| decision-list | ✅ | (always · 六条 KG-B 缺口天然适合逐条 keep/cut/new/defer 决策表) |
| next-PRD | ✅ | (always · K seed 足够 · 但本轮更可能落 refactor-plan 而非新 PRD) |
| refactor-plan | ✅ | "credential-isolation hook 误报 fail-closed"+"red-green-log 豁免失效"(命中「现有」缺陷改造·已存在机制) |
| next-dev-plan | ✅ | "开发分几个 phase 来实现"(命中 phase)+ 六条 KG-B 需排期下发 XenoDev |
| free-essay | ☐ | (默认不勾) |

## Reachability check on all X paths

| Path | Reachable | Type | Note |
|---|---|---|---|
| /home/ys/codes/XenoDev/dogfood-backlog.md | ✅(Read 第 1 行成功) | external-file(XenoDev) | 本轮核心标的 · ~85k token 整读 · 建议 Grep KG-B* 定位 |
| /Users/admin/codes/idea_gamma2 | ⚠ unreachable | external-repo-dir | mac 历史路径(已迁 Ubuntu · by-design stale) |
| /Users/admin/codes/idea_gamma2/docs/_archive/technology_roadmap.md | ⚠ unreachable | external-file | mac 路径 |
| /Users/admin/codes/idea_gamma2/.claude/skills/pipeline/SKILL.md | ⚠ unreachable | external-file | mac 路径 |
| /Users/admin/codes/idea_gamma2/.claude/skills/phase-retrospective/phase-retrospective-skill.md | ⚠ unreachable | external-file | mac 路径 |
| /Users/admin/codes/idea_gamma2/.claude/agents | ⚠ unreachable | external-dir | mac 路径 |
| /Users/admin/codes/idea_gamma2/.claude/skills | ⚠ unreachable | external-dir | mac 路径 |
| /Users/admin/codes/vibe-workflow/ | ⚠ unreachable | external-repo-dir | mac 路径 |
| /Users/admin/codes/vibe-workflow/.claude/ | ⚠ unreachable | external-dir | mac 路径 |
| /Users/admin/codes/autodev_pipe | ⚠ unreachable | external-repo-dir | mac 路径 |
| /Users/admin/codes/autodev_pipe/solo_ai_pipeline_v3.1.md | ⚠ unreachable | external-file | mac 路径 |
| discussion/006/forge/v5/stage-forge-006-v5.md | ✅ | stage-doc(prior-forge) | 最近可达 verdict · ~6k token |
| discussion/006/forge/v4/stage-forge-006-v4.md | ✅ | stage-doc(prior-forge) | ~7k token |
| discussion/006/forge/v3/stage-forge-006-v3.md | ✅ | stage-doc(prior-forge) | |
| discussion/006/forge/v2/stage-forge-006-v2.md | ✅ | stage-doc(prior-forge) | |
| discussion/006/forge/v1/stage-forge-006-v1.md | ✅ | stage-doc(prior-forge) | |
| discussion/006/forge/v7/stage-forge-006-v7.md | ⚠ unreachable | stage-doc | **v7 定稿不在标准路径** · caller 提及但 glob 无命中 · human 若知在别处请手加 |

## Quality flags

- [x] proposal section detected:✅
- [x] ≥1 X candidate extracted:✅(dogfood-backlog reachable + proposal-text + 5 份 prior-forge stage doc reachable)
- [x] K seed ≥ 80 chars:✅(~1900 chars)
- [x] At least 1 Y default recommended:✅(产品价值/架构设计/工程纪律/安全 四项)
- [x] At least 1 W default recommended:✅(verdict-only/decision-list/next-PRD/refactor-plan/next-dev-plan 五项)

## Prefill summary(给主命令的简要)

```
prefill_status: success
draft_file: discussion/006/forge/v8/_prefill-draft.md
x_candidates: 7 reachable(proposal-text + dogfood-backlog + v1..v5 stage docs);11 unreachable mac 路径已列但默认不勾
k_seed_bytes: 1900
z_candidates_present: false
intermediate_products_found: [none — 006 无 L1/L2/L3;仅 prior-forge stage docs v1..v5]
y_recommended: [产品价值, 架构设计, 工程纪律, 安全]
w_recommended: [verdict-only, decision-list, next-PRD, refactor-plan, next-dev-plan]
estimated_tokens_full_history: 110k
```
