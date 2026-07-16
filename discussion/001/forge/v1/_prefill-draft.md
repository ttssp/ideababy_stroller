# Forge intake prefill draft · 001 · v1

**Generated**: 2026-07-15T00:00:00Z
**Subagent**: forge-intake-prefill
**Proposal status**: found
**Forge target type**: root-idea

> ⚠ **Forge-target-vs-proposal 语境错位提示(human 必读)**:caller 传的
> `<id>=001` / `<ROOT_NUM>=001` 是 **root-idea forge**,但本次 forge 的实际触发
> 与审阅标的**不是 root proposal §001 那句宽泛的 research-radar seed**,而是
> **已 ship 的 `001-radar-pA` build 里 P0.2 盲测 gate 的形态治理**(hand-back
> `001-radar-pA-20260715T093226Z` · KG-B8 gate 形态 + KG-B4/B7 同簇)。
> HANDBACK-LOG 末条 operator 决议明确勾了「起 forge 同簇审(/expert-forge 001)」。
> 因此:proposal §001 的 X/K 候选**只作背景 seed**(idea 的原始愿景),真正的
> forge 审阅标的在 `001-radar/` fork 子树 + handback 子树。human 组 X 时应以
> radar-fork 那一代 stage/PRD/handback 为主,root §001 与 root L1/L2/L3(旧
> "外置研究编辑部" 代)为辅。

## Detected proposal section

**Title**: Research Radar
**proposals.md line**: 99
**Body byte count**: ~1180 bytes(想法+为什么+已想角度+相邻方案+倾向 五段)
**Fields detected**: 想法, 我为什么想做这个, 我已经想过的角度, 我已知的相邻方案/竞品, 我的倾向
**Note**: §001 status 行显式声明「revived 2026-07-06 · 转向 KG-radar / Topic
Cartographer 方向(= L1 Direction 7)」,真实愿景在 `001-radar` fork,root 的
旧 fork `001-pA`(窄简报)作 valid sibling 保留。proposal 正文中**无 `@/path`
引用**(所有 `@/Users/...` 路径在 idea 005,不在 001)。

## X candidates (raw)

### From proposal section

- [x] **proposal-text**:"`Research Radar` §想法 + 我为什么想做这个 + 已想角度 + 相邻方案 + 倾向(全 5 段)"
  - type: pasted-text
  - reachable: n/a
  - default: ☑ checked(idea 本身的核心文本 · 但只作背景 seed,见顶部错位提示)
  - source_line: proposals.md:99-134

（proposal §001 内无 external-path / url,故 path 候选为 0。）

### From discussion/001/ — root 层(旧 "外置研究编辑部" 代 · 2026-04-23)

> 这一代是 root 直进 L2 的老线,fork 为 `001-pA`(窄简报,已归档为 valid
> sibling)。与本次 forge 标的(radar-fork 的 gate 形态)**关系较远**,仅作
> full-history 时的历史背景。

- [ ] `discussion/001/L1/stage-L1-inspire.md`
  - type: stage-doc
  - reachable: ✅(Read 成功 · 13 directions · Direction 7 = 本次 radar 线源头)
  - default: ☐ unchecked(仅 full-history bundle 勾)
  - source: glob L1/stage-L1-inspire*.md
- [ ] `discussion/001/L2/stage-L2-explore-001.md`
  - type: stage-doc
  - reachable: ✅(旧 "外置研究编辑部" L2)
  - default: ☐ unchecked(旧代 · 非本次标的)
  - source: glob L2/stage-L2-explore-*.md
- [ ] `discussion/001/L3/stage-L3-scope-001.md`
  - type: stage-doc
  - reachable: ✅(旧 "外置研究编辑部" L3)
  - default: ☐ unchecked(旧代 · 非本次标的)
  - source: glob L3/stage-L3-scope-*.md
- [ ] `discussion/001/L2/L2R{1}-*.md` · `discussion/001/L3/L3R{0,1,2}-*.md` · `discussion/001/L1/L1R{1,2}-*.md`
  - type: raw-round
  - reachable: ✅
  - default: ☐(advanced · full-history 也不默认勾旧代 raw rounds)

### From discussion/001/001-radar/ — radar-fork 代(2026-07-06 起 · 本次标的所在)

> ⚠ 注意:`001-radar/` 整棵子树是 **untracked / gitignored**,`Glob` 探不到,
> 靠 `Grep .`(ripgrep 遍历)+ Read 逐个证实存在。以下路径均 Read 第 1 行成功。

- [ ] `discussion/001/001-radar/L2/stage-L2-explore-001-radar.md`
  - type: stage-doc
  - reachable: ✅("Paper Radar：给 AI lab 负责人的研究方向位移雷达")
  - default: ☐ unchecked(from-L3/full-history bundle 勾)
  - source: grep 遍历命中
- [x] `discussion/001/001-radar/L3/stage-L3-scope-001-radar.md`
  - type: stage-doc
  - reachable: ✅("给 AI lab 负责人的新方向评估器" · Candidate A/B 菜单)
  - default: ☑ checked(radar-fork 最近 stage · from-L3 是默认推荐)
  - source: grep 遍历命中
- [x] `discussion/001/001-radar/001-radar-pA/PRD.md`
  - type: internal-path(PRD · v1.2)
  - reachable: ✅(含 O4 两层信任 gate + v1.1/v1.2 演进 · **正是本次 forge 要改的 PPV 结构**)
  - default: ☑ checked(gate 形态审阅的直接标的)
  - source: grep 遍历命中
- [ ] `discussion/001/001-radar/001-radar-pA/L4/HANDOFF.md`
  - type: internal-path
  - reachable: ✅
  - default: ☐ unchecked(L4 交接包 · advanced)
- [ ] `discussion/001/001-radar/L2/moderator-notes.md` · `discussion/001/001-radar/L3/moderator-notes.md`
  - type: internal-path
  - reachable: ✅(L3 moderator-notes 含 injection 77a5176 主锚移 O2+O7 · 与 gate 形态直接相关)
  - default: ☐ unchecked(advanced · 但 human 若审 gate 形态强烈建议勾 L3 moderator-notes)
- [ ] `discussion/001/001-radar/FORK-ORIGIN.md` · `.../001-radar-pA/FORK-ORIGIN.md`
  - type: internal-path
  - reachable: ✅
  - default: ☐ unchecked

### From discussion/001/handback/ — hand-back 触发链(本次 forge 的直接因)

> ⚠ 同为 untracked 子树,Grep 遍历命中。这是本次 forge 最相关的一组 X 候选。

- [x] `discussion/001/handback/20260715T093226Z-001-radar-pA-20260715T093226Z.md`
  - type: internal-path(**触发本次 forge 的 hand-back**)
  - reachable: ✅(P0.2 gate 形态被 operator 真跑拒签 · operator 三条批评原话 · §3 建议 A/B/C)
  - default: ☑ checked(**forge 的第一因 · 必读**)
  - source: grep 遍历命中(git status 亦见此 untracked 文件)
- [x] `discussion/001/handback/HANDBACK-LOG.md`
  - type: internal-path(11 条决议史 · append-only)
  - reachable: ✅(含首跑 FAIL 20260711 决议 + KG-B4/B5/B7/B8 演进链 + 末条「起 forge」决议)
  - default: ☑ checked(gate 演进史 + KG-B4/B7/B8 同簇脉络的 SSOT)
  - source: grep 遍历命中
- [ ] `discussion/001/handback/20260711T135303Z-001-radar-pA-20260711T135303Z.md`
  - type: internal-path(P0.2 首跑 FAIL hand-back · **能力层** FAIL,与本次**结构层**质疑成对照)
  - reachable: ✅
  - default: ☑ checked(理解「首跑 FAIL vs 本次形态拒签」两层区别的关键对照)
  - source: grep 遍历命中
- [ ] `discussion/001/handback/20260710T063441Z-...md`(T004 P0.2 gate ship) · `20260713T060950Z-...md`(T004-A1 要件③ operationalize / KG-B7)
  - type: internal-path
  - reachable: ✅
  - default: ☐ unchecked(advanced · gate 硬化史 · full-history 勾)
- [ ] 其余 handback 包(055546Z/063436Z/063438Z/063443Z/021320Z/072600Z/213722Z)
  - type: internal-path
  - reachable: ✅(T001-T005 + A1 系列 ship 通知)
  - default: ☐ unchecked(advanced)

### Starting-point quick-pick groups

> 本 idea 的 bundle 语义已被「forge 标的 = radar-fork gate 形态」重塑:传统
> pure-idea(root proposal)对本次 forge 价值有限,真正有用的是 radar-fork +
> handback 组。以下按 spec 生成,但 default 推荐偏向含 handback 的组。

- **[Bundle:pure-idea]**(总是显示)
  - X 数量:1(proposal-text;proposal 内 0 external-path)
  - pre-checked: proposal-text
  - ⚠ 对本次 forge 覆盖不足(只有宽泛 seed,不含 gate 形态标的)
- **[Bundle:from-L2]**(radar-fork L2 stage exists)
  - X 数量:2
  - pre-checked: pure-idea 全部 + `001-radar/L2/stage-L2-explore-001-radar.md`
- **[Bundle:from-L3]**(radar-fork L3 stage exists · **default 推荐**)
  - X 数量:2
  - pre-checked: pure-idea 全部 + `001-radar/L3/stage-L3-scope-001-radar.md`
- **[Bundle:forge-target]**(本子代理为本次 gate-form forge 追加的推荐组 · 非 spec 标准档)
  - X 数量:5
  - pre-checked: proposal-text + `001-radar/L3/stage-L3-scope-001-radar.md` +
    `001-radar/001-radar-pA/PRD.md` + 触发 hand-back(20260715T093226Z) +
    `handback/HANDBACK-LOG.md`
  - ✅ **本子代理最推荐**:恰好覆盖 gate 形态审阅所需最小充分集(标的 PRD +
    触发因 + 决议史 + scope 语境),不背旧代噪声
  - estimated_tokens: ~11k
- **[Bundle:full-history]**(任一 stage exists)
  - X 数量:~20+(proposal + root L1/L2/L3 stage + radar L2/L3 stage + PRD +
    全部 moderator-notes + 全部 handback + raw rounds)
  - pre-checked: 见上全部 reachable 候选
  - estimated_tokens: **~55k**(≥ 8k · 主命令在 0.5.5.a 选此档会软警告 · 含
    大量旧代 "外置研究编辑部" 噪声,对 gate 形态 forge 收益递减)
- **[Bundle:custom]**(总是显示 — human 自己挑)

## K seed (suggested, editable by user)

```
// from "想法":
我希望做一个research radar，会自动发现、跟进最新的AI领域研究工作

// from "我为什么想做这个":
近年来AI research工作呈井喷式增长，新的工作层出不穷。
单靠个人来读文章/Blog/Repo已经远远跟不上了。
我觉得读文章，跟进最新的research还是有所谓的"套路"的，加之现在的LLM能力越来越强，跟进research这种高级的"pipeline"是有极大可能实现的

// from "我已经想过的角度"(全段为文字，无路径):
我需要一个"research radar"，它能够：
1. 自动检测arxiv的文章、顶会（如nips, icml, iclr等）的文章、顶尖学术机构/巨头实验室/创业公司（deepmind, thinkingmachines, anthropic等）的blog，github 高潜力的repo等
2. 检测到的新工作（文章/blog/repo）后，会进行下载、解析、解读、分析（novelty, impact, 实用性）等操作
3. 构建我的知识库：topic标签库按由大到小多层级延伸；有价值的归纳进库、价值一般的留痕防漏；支持时间线/同源延伸对立渊源继承关系等多种检索；针对最新工作实时更新当前topic的SOTA水平；有主动搜索补齐能力
4. 上述分析解读处理可依赖大模型能力
5. 核心：radar 能发现并及时跟进新工作，跟进完有能力整理梳理总结归纳进展，为后续 brainstorm/research 提供可靠、前瞻的判断
6. 实验室覆盖广，长期聚焦 8~15 个 topic
7. research 的 preference 和 taste 可让智能体自主学习（收集 X 观点+证伪/证实+辩证讨论），也可在长期交互中调整

// from "我已知的相邻方案/竞品"(注:此段亦是 Z candidates 原文,见下 §Z):
Karpathy 的 autoresearch（给定任务/代码/metric，agent 自己实验想 idea 直到突破）+ anthropic 9-opus research 实验。最终目标想结合这些研究智能体优势，构建 lab 的 research agent。这个 idea 是第一步：只有对现有工作有很深理解才可能找到有价值课题。

// from "我的倾向":
没有特别倾向，最终希望构建研究智能体，先把前置的跟进 research、梳理研究脉络、保持高水准理解这些基础先做好。

// ── forge-context supplement(本子代理补 · 非 proposal 原文 · human 可删)──
// 本次 forge 的真实审阅标的不是上面这个宽泛 seed，而是已 ship 的 001-radar-pA
// build 里 P0.2 盲测 gate 的**形态治理**:operator 真跑时拒签"人肉盲测二值签字"
// gate，提三条批评(①operator 非可靠打分器 ②应留痕可审计非盲测签字 ③应边用边
// 迭代非前置一次性闸门)，要求改为「可审计留痕 + 边用边迭代」。同簇 KG-B8(gate
// 形态该不该存在)+ KG-B4(gate 无机器强制)+ KG-B7(反作弊单次执行)三层一并审。
// 详见触发 hand-back 20260715T093226Z §2/§3 与 HANDBACK-LOG 末条。
```

**Byte count**: ~2400 bytes(远 > 80,proposal 5 段 + forge-context 补注)
**Quality flag**: K seed 长度 >= 80 chars → **ok**

## Z candidates (suggested if mode=对标指定列表)

**原文原样**(无 LLM 抽项 — human 选 Z mode = 对标指定列表 时把这段拷进
forge-config 的 Z 字段并手改为一行一项):

```
// from "我已知的相邻方案/竞品":
Karpathy最近的autoresearch让我印象深刻，那个项目是给定一个任务，一段代码，一个明确的metric，agent自己会实验，想idea，重复实验，直到突破；anthropic最近做了一个用9个opus做research的实验，也很有意思。就是9个opus自己讨论自己构思自己实验。
我希望**最终目标**能结合这些研究智能体的优势，构建一个我们lab的research agent。这个idea就是第一步，只有对现有的工作有很深的理解才有可能找到/想到有趣的题目有价值的课题。所以我想先从第一步开始。
```

> ⚠ 提醒:本段是 idea 的**终局愿景**(结合 autoresearch/9-opus 造 lab research
> agent),与本次 forge 的**近期标的**(gate 形态治理)不在同一层。若 forge 是
> 审 gate 形态,Z 对标列表更可能是 build 侧的验证/gate 设计先例(如
> ThoughtWorks Tech Radar 词表、Deep Research 溯源报告形态),而非 autoresearch。
> 由 human 定 Z mode 时判断。

## Y default recommendation

| Y 维度 | 默认 | 触发关键词 evidence |
|---|---|---|
| 产品价值 | ✅ | (always) + 命中「pipeline」规则(框架族三连之一) |
| 架构设计 | ✅ | "跟进research这种高级的\"pipeline\"是有极大可能实现的"(命中 `pipeline`) |
| 工程纪律 | ✅ | 同上「pipeline」命中(框架族规则:pipeline → 架构设计+工程纪律+产品价值 三连);另 forge 标的本身即 gate/PPV 结构治理,工程纪律高度相关 |
| 安全 | ☐ | (无命中 安全/权限/密钥) |
| 教学价值 | ☐ | (无命中 教学/学习/onboarding) |
| 商业可行 | ☐ | (proposal §001 无 商业/收入/盈利/赚;"每天赚100" 在 idea 002 不在 001) |
| 用户体验 | ☐ | (无命中 UX/交互/易用) |

> 说明:唯一命中的 Y 触发词是「pipeline」(line 112),按 framework 族规则拉齐
> 架构设计+工程纪律+产品价值三连。给定本次 forge 标的是 gate/验证 PPV 结构的
> 重构,工程纪律 + 架构设计的默认 ✅ 与标的高度吻合。

## W default recommendation

| W 形态 | 默认 | 理由 |
|---|---|---|
| verdict-only | ✅ | (always) |
| decision-list | ✅ | (always — 大多数 idea 受益于显式 keep/cut/new;本次尤甚:KG-B4/B7/B8 三层各需明确 keep/cut/redesign 裁决) |
| next-PRD | ✅ | (always — 且本次 forge 目标之一就是产 PRD/PPV 结构 verdict,PRD v1.2 待改) |
| refactor-plan | ☐(strict rule) / **建议 human 勾上** | proposal §001 正文**无** 对比/audit/已存在/redesign/现有 等词 → 严格规则默认 ☐;但 **forge-context 强烈指向 refactor**:触发 hand-back §3.A 明写「从"盲测二值硬前置"改成"可审计留痕验收"」= 对已 ship gate 机制的 redesign。human 审 gate 形态时**建议勾上** |
| next-dev-plan | ☐ | proposal §001 无 phase/milestone/按阶段/分阶段("分成几个phase" 在 idea 005 不在 001)→ 默认 ☐ |
| free-essay | ☐ | (默认不勾) |

## Reachability check on all X paths

| Path | Reachable | Type | Note |
|---|---|---|---|
| discussion/001/L1/stage-L1-inspire.md | ✅(Read 第 1 行成功) | stage-doc | root 旧代 · Direction 7 = radar 线源头 |
| discussion/001/L2/stage-L2-explore-001.md | ✅ | stage-doc | root 旧代("外置研究编辑部") |
| discussion/001/L3/stage-L3-scope-001.md | ✅ | stage-doc | root 旧代 |
| discussion/001/001-radar/L2/stage-L2-explore-001-radar.md | ✅ | stage-doc | radar-fork L2(位移雷达) |
| discussion/001/001-radar/L3/stage-L3-scope-001-radar.md | ✅ | stage-doc | radar-fork L3(Candidate A/B) |
| discussion/001/001-radar/001-radar-pA/PRD.md | ✅ | internal-file | **gate 形态标的 · PRD v1.2** |
| discussion/001/001-radar/001-radar-pA/L4/HANDOFF.md | ✅ | internal-file | L4 交接包 |
| discussion/001/001-radar/L3/moderator-notes.md | ✅ | internal-file | injection 主锚移 O2+O7 · 与 gate 直接相关 |
| discussion/001/001-radar/L2/moderator-notes.md | ✅ | internal-file | KG-radar 澄清愿景 |
| discussion/001/001-radar/FORK-ORIGIN.md | ✅ | internal-file | |
| discussion/001/001-radar/001-radar-pA/FORK-ORIGIN.md | ✅ | internal-file | |
| discussion/001/handback/20260715T093226Z-...md | ✅ | internal-file | **触发本次 forge** |
| discussion/001/handback/HANDBACK-LOG.md | ✅ | internal-file | 11 条决议史 SSOT |
| discussion/001/handback/20260711T135303Z-...md | ✅ | internal-file | P0.2 首跑 FAIL(能力层对照) |
| discussion/001/handback/(其余 8 个 handback 包) | ✅ | internal-file | T001-T005 + A1 系列 |
| discussion/001/L{1,2,3}/L*R*-*.md(root raw rounds) | ✅ | raw-round | advanced |
| discussion/001/001-radar/L{2,3}/L*R*-*.md(radar raw rounds) | ✅ | raw-round | advanced |

> reachability 方法:`001-radar/` 与 `handback/` 子树是 untracked/gitignored,
> `Glob` 探不到(返回 No files found),改用 `Grep "."`(ripgrep 遍历目录)+
> Read 第 1 行逐个证实。**无 external-repo / URL 型 X 路径**(proposal §001 无
> `@/path`),故 Codex sandbox BLOCK 风险为 0。

## Quality flags

- [x] proposal section detected:✅
- [x] ≥1 X candidate extracted:✅(1 proposal-text + 20+ discussion/handback 候选)
- [x] K seed ≥ 80 chars:✅(~2400 bytes)
- [x] At least 1 Y default recommended:✅(产品价值+架构设计+工程纪律)
- [x] At least 1 W default recommended:✅(verdict-only+decision-list+next-PRD)

## Prefill summary(给主命令的简要)

```
prefill_status: success
draft_file: discussion/001/forge/v1/_prefill-draft.md
x_candidates: 22
k_seed_bytes: 2400
z_candidates_present: true
intermediate_products_found: [root-L1-stage, root-L2-stage, root-L3-stage, radar-L2-stage, radar-L3-stage, radar-pA-PRD, radar-moderator-notes, handback-trigger, HANDBACK-LOG, handback-history]
y_recommended: [产品价值, 架构设计, 工程纪律]
w_recommended: [verdict-only, decision-list, next-PRD]
estimated_tokens_full_history: 55k
```
