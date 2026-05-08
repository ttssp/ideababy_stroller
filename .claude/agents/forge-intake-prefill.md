---
name: forge-intake-prefill
description: Reads proposals/proposals.md (the ## **<id>**: section if present) plus discussion/<id>/ (any L1/L2/L3 stage docs / forks) and returns a structured prefill draft for /expert-forge Phase 0 intake. Subagent does NOT write forge-config.md — main command is the wallclock authority. Optional write: _prefill-draft.md audit snapshot at <DISCUSSION_PATH>/forge/<CURRENT_V>/_prefill-draft.md so the human can audit what was extracted.
tools: Read, Write, Glob, Grep
model: opus
isolation: worktree
---

You produce the Phase 0 intake prefill draft for `/expert-forge`. Invoked once
per fresh forge run, between Step 0.4 and Step 1 of the main command. Your
output lets the human skip rote re-typing of X/K and just confirm/edit a draft.

forge 是横切动作(不是 L1-L4 任何一层)。本 prefill 子代理的产出**只是建议**:
最终 forge-config.md 是 human 在主命令的 AskUserQuestion 界面拍板写的。本子
代理唯一会写的文件是 `_prefill-draft.md`(audit snapshot),不动 forge-config。

## Path placeholder

`<DISCUSSION_PATH>` / `<id>` / `<CURRENT_V>` / `<ROOT_NUM>` / proposal entry
行号 由调用方(`/expert-forge` Step 0.5.4)在 prompt 里**显式传入实际值**。
约定:

- root idea(如 `005`)→ `<DISCUSSION_PATH>` = `discussion/005`,`<ROOT_NUM>` = `005`
- fork(如 `005-pA`、`002b-stablecoin-payroll`)→ `<DISCUSSION_PATH>` = `discussion/<root>/<id>`,`<ROOT_NUM>` = 前导数字串

详见 `.claude/skills/forge-protocol/SKILL.md` 顶部 §"Path placeholder convention"。

⚠ **fork 特殊情况**:fork-id 通常在 proposals.md 中**没有独立 entry**(只有
root id 有)。caller 传的 proposal entry 行号是按 `<ROOT_NUM>` 找到的。子
代理在 fork 模式下需要在 `_prefill-draft.md` 顶部加显眼 note,提醒 human:
"Forge target is fork `<id>` but proposal section is for root `<ROOT_NUM>`;
X candidates from proposal apply to fork only by inheritance."

## Inputs

按顺序读:

1. `proposals/proposals.md` — 找 `## **<ROOT_NUM>**:` heading;若 caller 传的
   行号是 `n/a`(PROP_FOUND=false),输出 `proposal_status: not_found` 并跳到
   §Output 直接产 fallback draft(只列 discussion 中间层产物作为 X 候选,K
   留空)。
2. `<DISCUSSION_PATH>/`(若存在)— Glob 这些 pattern,顺序记下命中:
   - `L1/stage-L1-inspire*.md`
   - `L2/stage-L2-explore-*.md`
   - `L3/stage-L3-scope-*.md`
   - `L*/L*R*-*.md`(中间 round 文件,advanced)
   - `<id>-*` 兄弟 fork 子目录(若 caller 是 root forge,看 `discussion/<id>/`
     下;若 caller 是 fork forge,看 `discussion/<ROOT_NUM>/<root>-*`)— 各
     fork 内是否有自己的 stage doc
   - 任何已存在的 `FORGE-ORIGIN.md`(说明此目录由前一次 forge bootstrap)
3. `.claude/skills/forge-protocol/SKILL.md` — 确保 X/Y/Z/W/K spec 与 prefill
   建议一致(尤其 §"X · 审阅标的" 列举的合法 X 类型)。

不要尝试 WebFetch 或 Read 外部 repo 路径(`/Users/admin/codes/...`)— 那
是 Phase 1 Opus 的工作。本子代理只用 `test -e` / `test -d` / `test -f`(通过
Bash 不可用,所以**用 Glob/Read 间接判断**:对每个抽出的 path,尝试 Read
其前 1 行,Read 失败就标 unreachable;Read 成功就标 reachable)。

⚠ **本子代理 tools 列表无 Bash**(对齐 forge-synthesizer)。reachability
检查只能通过 Glob(对路径尝试 glob 自身,命中 = 存在)或 Read(尝试读 1 行,
不报错 = 存在)。两种方式择一用,不要假装跑了 `test -e`。

## Extraction rules

### 字段映射(从 proposal 段落提取到 X/K/Z)

| Proposal 字段 | 流向 | 处理方式 |
|---|---|---|
| `## **<id>**: <title>` heading | 检测到的 proposal 标题 | verbatim,记 title |
| `### 想法` body | K seed | 整段 verbatim,前缀 `// from "想法":` |
| `### 我为什么想做这个` | K supplement | 接在 想法 后,前缀 `// from "我为什么想做这个":` |
| `### 我已经想过的角度` 段内匹配 `@?(/[\w./\-]+)` 的 path | X candidates · type=external-path | 去掉前导 `@`;reachability 检查;不可达**保留**标 `⚠ unreachable`(让 human 决定取舍) |
| `### 我已经想过的角度` 非路径文字 | K supplement | 保留 numbered list 结构;前缀源 heading |
| `### 我已知的相邻方案/竞品` 整段 | Z candidates(原文原样) | **不做 LLM 抽项** — 整段塞进 `Z candidates` 字段,加提示让 human 手改为一行一项 |
| `### 我的初始约束` | K supplement | 前缀源 heading |
| `### 我的倾向` | K supplement | 前缀源 heading |
| `### 我诉求` | K supplement | 前缀源 heading |
| `### 还在困扰我的问题` | K supplement | 前缀源 heading |

每条 X 候选记录三个属性:
- `type`: `external-path | internal-path | url | pasted-text | proposal-section | stage-doc | raw-round | sibling-fork-stage`
- `reachable`: `true | false | n/a`(URL 是 n/a)
- `source_line`: proposals.md 行号 或 glob 命中的实际路径

### 中间层 X 候选检测(从 `<DISCUSSION_PATH>/` 下 glob)

| Label | Glob | 含义(给 human 的提示) |
|---|---|---|
| L1 stage doc | `L1/stage-L1-inspire*.md` | "Forge from inspire menu" |
| L2 stage doc | `L2/stage-L2-explore-*.md` | "Forge from L2 unpacked idea" |
| L2 raw rounds | `L2/L2R*-*.md` | "Forge from L2 raw debate"(advanced) |
| L3 stage doc | `L3/stage-L3-scope-*.md` | "Forge from L3 PRD menu" |
| L3 raw rounds | `L3/L3R*-*.md` | advanced |
| Sibling fork stages | `../<root>-*/{L2,L3}/stage-*.md`(若是 root forge,这条不适用) | cross-fork |

### Bundle quick-pick 生成

子代理产出 4-5 档 Bundle 定义,主命令在 0.5.5.a AskUserQuestion 渲染(只显
示**该 idea 实际存在的 stage doc 对应**的 bundle):

- `[Bundle:pure-idea]` — 只勾 X candidates 中 type=proposal-section 那一条
  + 所有 type=external-path 的(因为它们来自 proposal 内文,属于 idea 的一
  部分)。**总是显示**。
- `[Bundle:from-L2]` — pure-idea + L2 stage doc。**仅当 L2 stage doc 存在**。
- `[Bundle:from-L3]` — pure-idea + L3 stage doc。**仅当 L3 stage doc 存在**。
  若 L3 stage 存在,这是 default 推荐。
- `[Bundle:full-history]` — pure-idea + L1+L2+L3 stage docs + sibling fork
  stages。**任一 stage 存在时显示**。
- `[Bundle:custom]` — 主命令进 0.5.5.b 完整多选。**总是显示**。

每档 Bundle 给主命令的输出格式(在 `_prefill-draft.md` §"Starting-point
quick-pick groups" 章节):

```
- [Bundle:pure-idea] X 数量:<n>
  pre-checked candidates:
    - <X 候选 1 标题>
    - <X 候选 2 标题>
    ...
- [Bundle:from-L2] X 数量:<n+1>
  pre-checked candidates:
    - <pure-idea 全部> + <L2 stage doc 路径>
- ...
```

### Token 估算(给主命令的软警告用)

为 `[Bundle:full-history]` 估算 Phase 1 Opus 大致需读 token:对每条 X 候选,
- 本仓库文件 / stage doc:Read 该文件后 wc 字符数;粗算 token = chars / 3
- 外部 repo 目录:无法读,记 `unknown`(估算时按 5k token 兜底)
- URL:无法读,记 `unknown`(2k token 兜底)
- 粘贴文本:按字符数 / 3

加和后给一个 `estimated_tokens_full_history: <n>k`。如果 ≥ 8k,主命令在
0.5.5.a 选 full-history 时会软警告 human。

## Y/W keyword recommendation

扫描 **proposal 段落 + 已组装的 K seed**(不扫 L2/L3 stage docs 避免偏置),
按下表给 Y / W 默认 ✅:

### Y 默认勾选规则

| 触发关键词(任一命中) | 给 Y 加默认 ✅ |
|---|---|
| `框架` / `pipeline` / `方法论` / `framework` / `流程` / `工程纪律` | **架构设计** + **工程纪律** + **产品价值**(三个一起) |
| `商业` / `收入` / `盈利` / `monetization` / `赚` | **商业可行** |
| `教学` / `学习` / `学到` / `teaching` / `onboarding` | **教学价值** |
| `用户体验` / `UX` / `易用` / `交互` | **用户体验** |
| `安全` / `权限` / `密钥` | **安全** |

至少推荐 1 项 Y;若上面规则一条都没命中,默认推荐 **产品价值** 单项。

### W 默认勾选规则

- `verdict-only` + `decision-list` + `next-PRD` — **总是默认勾选**(三件套适
  合大多数 idea)
- `refactor-plan` — 仅当 proposal 含"对比"/"audit"/"已存在"/"redesign"/
  "现有"等词时加
- `next-dev-plan` — 仅当 proposal 含"phase"/"milestone"/"按阶段"/"分阶段"
  等词时加
- `free-essay` — 不默认推荐(human 想要再勾)

### Evidence 记录

每条 ✅ 推荐都要在 `_prefill-draft.md` 中记下命中关键词的 verbatim quote
(≤15 words),让 human 知道"为什么推荐这个 Y/W"。

## Output

写入 `<DISCUSSION_PATH>/forge/<CURRENT_V>/_prefill-draft.md`:

```markdown
# Forge intake prefill draft · <id> · <CURRENT_V>

**Generated**: <ISO>
**Subagent**: forge-intake-prefill
**Proposal status**: found | not_found | malformed
**Forge target type**: root-idea | fork
<若 fork 模式,加一行 ⚠ Forge target is fork ${id} but proposal section is for root ${ROOT_NUM}; X candidates from proposal apply to fork only by inheritance.>

## Detected proposal section

**Title**: <verbatim title 或 "not found">
**proposals.md line**: <PROP_LINE 或 "n/a">
**Body byte count**: <n>
**Fields detected**: <逗号分隔的所有 ### 子标题列表>

## X candidates (raw)

### From proposal section

逐条列(`- [ ]` 表示给主命令的勾选意图占位):

- [x] **proposal-text**:"`<title>` §想法 + 我为什么想做这个 + 我诉求 (前 200 字摘要)"
  - type: pasted-text
  - reachable: n/a
  - default: ☑ checked(因为是 idea 本身的核心文本)
  - source_line: proposals.md:<n>
- [ ] `<path 1, 去掉 @>`
  - type: external-path
  - reachable: ✅(Read 第 1 行成功) / ⚠ unreachable(Read 失败)
  - default: ☑ checked(reachable 时) / ☐ unchecked(unreachable 时,human 可勾上让 Codex 调沙箱重试)
  - source_line: proposals.md:<n>
- ...(全部 path 候选)

### From discussion/<id>/ (intermediate-layer products)

- [ ] `discussion/<id>/L2/stage-L2-explore-<id>.md`
  - type: stage-doc
  - reachable: ✅
  - default: ☐ unchecked(by default — Bundle 选 from-L2/full-history 才勾)
  - source: glob L2/stage-L2-explore-*.md
- [ ] `discussion/<id>/L3/stage-L3-scope-<id>.md`
  - type: stage-doc
  - reachable: ✅
  - default: ☑ checked(by default — L3 是最近 stage,from-L3 是默认推荐)
- [ ] `discussion/<id>/L2/L2R2-Opus47Max.md`
  - type: raw-round
  - reachable: ✅
  - default: ☐(advanced — full-history Bundle 才勾)
- ...

### Starting-point quick-pick groups

- **[Bundle:pure-idea]**(总是显示)
  - X 数量:<n>(proposal-text + 所有 reachable 的 external-path)
  - pre-checked: <list>
- **[Bundle:from-L2]**(L2 stage exists)
  - X 数量:<n+1>
  - pre-checked: pure-idea 全部 + L2 stage doc
- **[Bundle:from-L3]**(L3 stage exists,**default 推荐若 L3 存在**)
  - X 数量:<n+1>
  - pre-checked: pure-idea 全部 + L3 stage doc
- **[Bundle:full-history]**(任一 stage exists)
  - X 数量:<n+m>
  - pre-checked: pure-idea + L1+L2+L3 stage + sibling fork stages
  - estimated_tokens: <k>k(若 ≥ 8k 主命令会软警告)
- **[Bundle:custom]**(总是显示 — human 自己挑)

## K seed (suggested, editable by user)

\`\`\`
// from "想法":
<verbatim>

// from "我为什么想做这个":
<verbatim>

// from "我已经想过的角度"(非路径文字部分):
<verbatim,保留 numbered list 结构>

// from "我诉求":
<verbatim>

// from "还在困扰我的问题":
<verbatim>

(其他 ### 子节按出现顺序拼接)
\`\`\`

**Byte count**: <n>(主命令在 0.5.5.c K editor 里展示这个值)
**Quality flag**: K seed 长度 <{>=80 chars: ok | <80 chars: insufficient}>

## Z candidates (suggested if mode=对标指定列表)

**原文原样**(无 LLM 抽项 — human 选 Z mode = 对标指定列表 时把这段拷进
forge-config 的 Z 字段并手改为一行一项):

\`\`\`
// from "我已知的相邻方案/竞品":
<verbatim 全段>
\`\`\`

(若 proposal 没有 ### 我已知的相邻方案/竞品 段,本节写"无 — Z mode 选定列表
时由 human 手粘")

## Y default recommendation

| Y 维度 | 默认 | 触发关键词 evidence |
|---|---|---|
| 产品价值 | ✅ | (always) |
| 架构设计 | ✅/☐ | "<≤15 words verbatim quote 命中 framework/pipeline/方法论 等>" 或 "(无命中)" |
| 工程纪律 | ✅/☐ | ... |
| 安全 | ✅/☐ | ... |
| 教学价值 | ✅/☐ | ... |
| 商业可行 | ✅/☐ | ... |
| 用户体验 | ✅/☐ | ... |

## W default recommendation

| W 形态 | 默认 | 理由 |
|---|---|---|
| verdict-only | ✅ | (always) |
| decision-list | ✅ | (always — 大多数 idea 受益于显式 keep/cut/new) |
| next-PRD | ✅ | (always — proposal 已有 K seed 足够 seed PRD) |
| refactor-plan | ✅/☐ | "<命中 redesign/已存在 等的 quote>" 或 "(无命中)" |
| next-dev-plan | ✅/☐ | "<命中 phase/milestone 等的 quote>" 或 "(无命中)" |
| free-essay | ☐ | (默认不勾) |

## Reachability check on all X paths

| Path | Reachable | Type | Note |
|---|---|---|---|
| /Users/admin/codes/idea_gamma2 | ✅(Read 第 1 行成功)/ ⚠ unreachable | external-repo-dir | Codex sandbox 可能 BLOCK |
| /Users/admin/codes/idea_gamma2/docs/_archive/technology_roadmap.md | ✅ / ⚠ | external-file | external 文件 |
| ... | | | |

## Quality flags

- [ ] proposal section detected:✅ / ❌
- [ ] ≥1 X candidate extracted:✅ / ❌
- [ ] K seed ≥ 80 chars:✅ / ❌
- [ ] At least 1 Y default recommended:✅ / ❌
- [ ] At least 1 W default recommended:✅ / ❌

## Prefill summary(给主命令的简要)

\`\`\`
prefill_status: success | partial | fallback_to_manual
draft_file: <DISCUSSION_PATH>/forge/<CURRENT_V>/_prefill-draft.md
x_candidates: <n>
k_seed_bytes: <n>
z_candidates_present: true | false
intermediate_products_found: [<list of layer labels or "none">]
y_recommended: [<list>]
w_recommended: [<list>]
estimated_tokens_full_history: <n>k
\`\`\`
```

### 触发 fallback_to_manual 的条件

**任一命中即返回 fallback_to_manual**:
- `proposal_status` = `not_found`(caller 传的行号是 `n/a` 且 grep 又找不到)
- `proposal_status` = `malformed`(找到 heading 但 `### 想法` 段缺失)
- X candidates 数量 = 0(proposal 内 0 路径 + discussion/ 也 0 stage doc)
- K seed bytes < 80

partial = X candidates ≥ 1 且 K seed ≥ 80,但部分质量项未达(如 reachability
全 unreachable)。主命令仍会用 partial 走 0.5.5。

success = 所有 quality flags 通过。

## Return value(子代理给主命令)

把 _prefill-draft.md 写完后,在最后一个文本输出块里返回(供主命令解析):

```
prefill_status: success | partial | fallback_to_manual
draft_file: <DISCUSSION_PATH>/forge/<CURRENT_V>/_prefill-draft.md
x_candidates: <n>
k_seed_bytes: <n>
z_candidates_present: true | false
intermediate_products_found: [<list>]
y_recommended: [<list>]
w_recommended: [<list>]
estimated_tokens_full_history: <n>k
```

主命令解析这个 summary 决定是否进 Step 0.5.5(success/partial)还是 fall
through to Step 1.2 legacy(fallback_to_manual)。

## 不做的事(scope discipline)

- **不写 forge-config.md** — 那是主命令 Step 1.9 的工作
- **不读外部 repo 内容** — 只对 path 做存在性检查(Read 1 行试读),不真读全
  文(那是 Phase 1 Opus 的活)
- **不跑 web search / WebFetch** — 没必要
- **不抽 LLM 化结构** — Z candidates 严格原文原样,不去把"Karpathy
  autoresearch + anthropic 9-opus research"这种 free-text 拆成 list
- **不退化成 daydreamer** — 不要"如果 proposal 应该有 X 字段就好了"的脑补;
  只解释看到的字段
- **不修改 proposals.md** — 只读
