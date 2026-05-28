# Forge intake prefill draft · 006 · v3

**Generated**: 2026-05-27T00:00:00Z
**Subagent**: forge-intake-prefill
**Proposal status**: found
**Forge target type**: root-idea(006 = root idea,无独立 fork-id;006a-pM 是 v0.1 PRD fork,已 ship 封箱)

> ℹ **v3 与 v1/v2 的关系**:`proposals.md §006` 文本自 v1/v2 起未变(与 §005 内容逐字相同 — 早期压测复制痕迹),proposal-side X 与 K seed **与 v2 prefill 几乎一致**。v3 的真正差异化输入来自:
> - **v2 forge stage doc**(`discussion/006/forge/v2/stage-forge-006-v2.md`)= v2 已收敛 verdict / decision matrix / refactor plan / PRD 草案 / dev plan / free-essay 全集;v3 是在 v2 verdict 落地 ship 后(v0.1 已封箱)再开的新一轮 forge,**v2 verdict 本身是 v3 默认上下文**(不重审,但应继承)。
> - **HANDBACK-LOG.md v0.1 ship 后 17 ENTRY 决议日志**(其中 ENTRY 7-17 是 2026-05-27 batch 2 真路径 backlog 来源)= 11 项 v0.2 forge 待办的"真路径累积证据"。
> - **proposal-text + idea_gamma2 / vibe-workflow 全栈**(v1 X #1-#9)= operator 在 v2 时已显式标 no-rerun,v3 默认沿用 no-rerun(不再让 Phase 1 Opus 读外部历史 repo)。
>
> **主命令在 0.5.5 X UI 应呈现的 X 集合**:**v3 的 X 主体是 HANDBACK-LOG 提取的 11 项 backlog + v2 stage doc + 本仓 framework/SHARED-CONTRACT.md + xenodev-bootstrap-kit 的 mirror 现状 + XenoDev 真路径子树头部 file**,而非 proposal-text 历史重读。Bundle 推荐已据此设计。

## Detected proposal section

**Title**: `006`: auto agentic coding
**proposals.md line**: 224
**Body byte count**: ~1430 chars (UTF-8)
**Fields detected**: 想法, 我为什么想做这个, 我已经想过的角度, 我诉求

(注:§006 没有 §我已知的相邻方案/竞品 / §我的初始约束 / §我的倾向 / §还在困扰我的问题 — 与 v1/v2 prefill 检测一致)

## X candidates (raw)

### From proposal section(historical · operator 在 v2 已标 no-rerun · v3 默认沿用)

- [ ] **proposal-text**:"`006`: auto agentic coding §想法 + 我为什么想做这个 + 我诉求"
  - type: pasted-text
  - reachable: n/a
  - default: ☐ unchecked(v2 已吸收;K seed 仍含 verbatim;v3 主线不重读)
  - source_line: proposals.md:224-247
- [ ] `/Users/admin/codes/idea_gamma2`(+ docs/_archive/technology_roadmap.md / .claude/skills/pipeline · phase-retrospective · agents · skills 共 6 项)
  - type: external-path
  - reachable: ✅(v2 已验过)
  - default: ☐ unchecked(v1 / v2 已 no-rerun)
  - source_line: proposals.md:237
- [ ] `/Users/admin/codes/vibe-workflow/` + `.claude/`(2 项)
  - type: external-path
  - reachable: ✅
  - default: ☐ unchecked(v1 / v2 已 no-rerun)
  - source_line: proposals.md:239
- [ ] `/Users/admin/codes/autodev_pipe`(+ solo_ai_pipeline_v3.1.md)
  - type: external-path
  - reachable: ✅
  - default: ☐ unchecked(v2 verdict 已 archive V4 整仓;v3 不再回头审 ADP 仓)
  - source_line: proposals.md:241

### From discussion/006/forge/v2/(v2 已收敛产物 · v3 默认必读)

- [x] `discussion/006/forge/v2/stage-forge-006-v2.md`
  - type: stage-doc
  - reachable: ✅
  - default: ☑ checked(v3 主线锚:v2 verdict / decision matrix / W3 refactor plan / W4 PRD 草案 / W5 B1+B2 dev plan / W6 essay 全集 — Phase 1 Opus 必读,否则无法对齐 v0.2 修订 baseline)
  - source: glob discussion/006/forge/v2/stage-*.md
- [ ] `discussion/006/forge/v2/forge-config.md`
  - type: stage-doc(aux)
  - reachable: ✅
  - default: ☐ unchecked(prefill 已总结其 X/Y/Z/W/K 配置;v3 可参考但非必读)
- [ ] `discussion/006/forge/v2/moderator-notes.md` + `_x-input-draft-by-operator.md`
  - type: stage-doc(aux)
  - reachable: ✅
  - default: ☐ unchecked(advanced;若 v3 主线又出现"v2 收敛是否过早"的争议时勾)

### From discussion/006/handback/(v0.1 ship 后真路径 backlog · v3 核心 X)

- [x] `discussion/006/handback/HANDBACK-LOG.md`(17 ENTRY · 2026-05-11 batch 1 + 2026-05-27 batch 2)
  - type: stage-doc(append-only log)
  - reachable: ✅
  - default: ☑ checked(**v3 唯一最重要 X** — 11 项 backlog 全在此;ENTRY 7-17 的 §"汇总 IDS-side 行动 batch 2 · §5 backlog 总览"是 verdict 直接锚)
  - source: 直接 read

- [ ] 11 个 hand-back 包 `discussion/006/handback/2026*-006a-pM-2026*.md`
  - type: stage-doc(包体)
  - reachable: ✅(全部 reachable;batch 1 = 6 包 / batch 2 = 11 包,batch 1 已被 batch 2 摘要)
  - default: ☐ unchecked(HANDBACK-LOG 已摘要;若 v3 expert 需 cross-check 单包 §3 ship history / §4 PRD trigger / §7 设计认知 verbatim 再勾)

### From framework/(本仓协议层 · v3 4 项协议级修订标的)

- [x] `framework/SHARED-CONTRACT.md`(v2.0 现行)
  - type: internal-path
  - reachable: ✅
  - default: ☑ checked(**v3 4 项协议级修订全在此**:Cross-device publish §6 / event-schema enum 单复数统一 / IDS dir flock / `--ids-verdict-evidence` flag — HANDBACK-LOG ENTRY 11/14/15/17 触发)
- [x] `framework/xenodev-bootstrap-kit/` 整子树(22 个 .sh + README + templates)
  - type: internal-path
  - reachable: ✅(已验:eval-event-log/writer.sh + handback-validator/{validate,_yaml-helpers,check-3,check-5}.sh + safety-floor-{1,2,3} + workspace-schema 全 reachable)
  - default: ☑ checked(**mirror 现状**:v2 ENTRY 7+9+13 已 cp 5 文件 SSOT 反向同步;v3 待续 rebuild 子树范围 = skills/parallel-builder + spec-writer + codex-review + hooks/wrappers + tests/integration + handback-validator/templates + gen-handback + score-handback)

### From /Users/admin/codes/XenoDev/(SSOT 上游 · v3 mirror rebuild 标的)

- [x] `/Users/admin/codes/XenoDev/.claude/skills/parallel-builder/SKILL.md`
  - type: external-path
  - reachable: ✅
  - default: ☑ checked(ENTRY 11 真路径 SKILL §6.3 cross-device fallback 是协议级修订源;IDS mirror 现不含此子树)
- [x] `/Users/admin/codes/XenoDev/.claude/skills/spec-writer/SKILL.md`
  - type: external-path
  - reachable: ✅
  - default: ☑ checked(ENTRY 10 sort -V → gsort → python3 portability fix;IDS mirror 现不含)
- [x] `/Users/admin/codes/XenoDev/.claude/skills/codex-review/SKILL.md`
  - type: external-path
  - reachable: ✅
  - default: ☑ checked(ENTRY 7/10/13/17 §6 anti-pattern #10 + adversarial 4 轮 + ship-blocker precedent · IDS mirror 现不含)
- [x] `/Users/admin/codes/XenoDev/.claude/hooks/wrappers/dangerous-event-emit.sh`
  - type: external-path
  - reachable: ✅
  - default: ☑ checked(ENTRY 12 hooks/wrappers Safety Floor + eval-event-log wire · IDS mirror 现不含 hooks/wrappers/)
- [x] `/Users/admin/codes/XenoDev/tests/integration/`(8 个 .sh:bootstrap-verify / round-trip-006a-pM / test-negative / eval-events-count / test-T011-negative / manual-cleanup-t008 / test-verify-all-negative / verify-all-outcomes)
  - type: external-path
  - reachable: ✅
  - default: ☑ checked(ENTRY 8/14/15/17 round-trip + atomic publish + fail-closed + verify-all + --ids-verdict-confirmed 真路径 · IDS mirror 现不含 tests/integration/)
- [x] `/Users/admin/codes/XenoDev/lib/handback-validator/{templates/handback.template.md, gen-handback.sh, score-handback.sh}`
  - type: external-path
  - reachable: ✅(全部 reachable · 含 _yaml-helpers / check-1..6 / validate / score / gen / templates / test-fixtures)
  - default: ☑ checked(ENTRY 13/16 templates 三节 body + tags array + gen --section1/2/3 flag + score 3 字段 · IDS mirror handback-validator/ 子树已部分 SSOT 同步 5 文件;templates + gen + score 待并入下次 rebuild)
- [ ] `/Users/admin/codes/XenoDev/lib/eval-event-log/{writer.sh, reader.sh, event-schema.json}`
  - type: external-path
  - reachable: ✅
  - default: ☐ unchecked(writer.sh 已 batch 1 ENTRY 7 SSOT;event-schema.json 是 enum 单复数协议级修订源 · 可选并入 X · 主命令呈现时让 operator 决定 explicit add)
- [ ] `/Users/admin/codes/XenoDev/PRD.md`(v0.1 PRD · 已 ship 封箱)
  - type: external-path
  - reachable: ✅
  - default: ☐ unchecked(已 ship 不再改;若 v3 触发 v0.2 PRD draft 时 expert 需读历史 v0.1 真路径再勾)

### Starting-point quick-pick groups

主命令在 0.5.5.a AskUserQuestion 渲染。**default 推荐 = [Bundle:v0.2-protocol-bump]**(11 项 backlog 集中处理是 v3 主线使命)。

- **[Bundle:pure-idea]**(总是显示 · v3 不推荐用此)
  - X 数量:1(只 proposal-text · v1/v2 已 no-rerun proposal-side 路径)
  - pre-checked: proposal-text
  - 用途:若 operator 想从零再审 idea 本身(几乎不会发生)
- **[Bundle:from-v2-stage]**(v2 stage 存在 · 历史回顾)
  - X 数量:2
  - pre-checked: v2 stage-forge-006-v2.md + HANDBACK-LOG.md
  - 用途:expert 复盘 v2 verdict 是否仍 hold;不修订协议
- **[Bundle:v0.2-protocol-bump]**(✓ **default 推荐 · v3 主线**)
  - X 数量:8
  - pre-checked: v2 stage-forge-006-v2.md + HANDBACK-LOG.md + framework/SHARED-CONTRACT.md + framework/xenodev-bootstrap-kit/ + XenoDev/skills/{parallel-builder,spec-writer,codex-review} + XenoDev/hooks/wrappers/ + XenoDev/tests/integration/ + XenoDev/lib/handback-validator/{templates,gen,score}
  - 用途:11 项 backlog(mirror rebuild + 协议 4 项 + lib 3 bug)一次性处理
  - estimated_tokens: ~22k(2 stage doc ≈ 6k + SHARED-CONTRACT ≈ 3k + bootstrap-kit 22 .sh ≈ 5k + XenoDev 6 skill/hook/test/lib path ≈ 8k)
- **[Bundle:full-history]**(任一 stage exists)
  - X 数量:14
  - pre-checked: v0.2-protocol-bump 全部 + v1 X 9 项(proposal-text + idea_gamma2 + vibe-workflow + autodev_pipe)
  - estimated_tokens: ~40k(⚠ 超 8k 阈值 · 主命令应软警告 operator 此 bundle 重读 v2 已 no-rerun 的 9 个外部 repo 历史 X)
  - 用途:若 operator 想让 v3 expert 同时回审 framework 起源假设
- **[Bundle:custom]**(总是显示 — operator 自己挑)

## K seed (suggested, editable by user)

```
// from "想法":
给定一个PRD,claude code可以几乎没有人工干预的情况下自主完成开发任务。我需要一个**可靠的、自动化程度最高**解决方案。

// from "我为什么想做这个":
我是非软件开发背景。我可以将需求描述清楚,我也可以尝试构建较可靠的PRD。但是我缺少软件开发的经验,对各个规模(大中小型)的开发的方案、流程、规范等内容都没有把握。

// from "我已经想过的角度"(非路径文字部分):
我最近一个月做了很多尝试:
1. 第一个项目名 idea_gamma2(数字基建,phase + pipeline skill + phase-retrospective + subagent + skills)
2. 第二个项目 vibe-workflow(engineer team 协作 + 自动化开发)
3. 第三个项目 autodev_pipe(借鉴 vibe coding / agentic coding 最佳实践 + agent-skills + superpowers · 专业的自动化开发流程)
4. 第四个项目当前 repo(idea→PRD→自动开发)

// from "我诉求":
希望双方凭借最强的 AI 专业能力以及最丰富的软件开发经验,通过调研、论证、思辨、构思、设计、整理归纳等方式,达成一套基于 Claude Code 实现**可靠**自动化开发的 framework/pipeline 的共识方案

// v3 specific additions(operator append 2026-05-27,可在 0.5.5.c K editor 编辑)
K8(v3 mission · binding):v3 mission = "Bootstrap kit v0.2 反向同步、带上协议修订 + lib bug 清班"。v0.1(006a-pM)已 ship 封箱(2026-05-27);v3 不重审 idea / 不重审 v2 verdict 主线,只在 v2 verdict 落地后的 **真路径 backlog 三类** 上收敛:
  (a) **mirror rebuild 4 子树**:skills/{parallel-builder, spec-writer, codex-review} + hooks/wrappers + tests/integration + handback-validator/{templates, gen-handback, score-handback}
  (b) **协议级修订 4 项**(SHARED-CONTRACT §6 + event-schema):Cross-device publish 段 / event-schema enum 单复数统一(operator_interventions/review_failures 复 vs handback_drift 单) / IDS dir flock/fcntl / `--ids-verdict-evidence` flag
  (c) **XenoDev 本仓 lib bug 3 项**:scan-credentials exit code + 14 false positive 治理 / gen-handback `--out` 默认前缀 / FU-producer-1 case F stale(T007 ship 后 template 无 `{{RATIONALE}}` · main 14/15 fail 真 regression)

K9(v2 verdict 继承 · 不重审):v2 已收敛"IDS=idea→PRD + 治理 / XenoDev=唯一 L4 runtime / 双向 hand-off"= v3 不动这个大架构,只动落地后的协议 + lib 细节修订。

K10(operator 偏好 · 评分 #2 加分依据):Cluster A 选项 1(锁定 mirror 现有子树范围)的实证已成熟 — 单 ENTRY 7/9/13 三连 cp + 不越 mirror 边界;v3 修订 mirror 子树范围时应延续这种"边界先定、批量 SSOT、不越界"的纪律。

K11(v3 收敛模式偏好):strong-converge(operator 已对 v2 强 binding;v3 同档)— 11 项 backlog 应一一对一收敛产 verdict,不允许"双方都对"式压扁,残余分歧用 v0.2-note 旁注。
```

**Byte count**: ~2350 chars (UTF-8 · K seed 充实,proposal verbatim + K8-K11 v3 specific 共 5 段)
**Quality flag**: ≥ 80 chars · ok

## Z candidates (suggested if mode=对标指定列表)

**原文原样**(proposal §006 没有 §我已知的相邻方案/竞品 段):

```
无 — Z mode 选定列表时由 human 手粘。
```

**v3 上下文建议补**(operator 0.5.5.d Z editor 时参考 · 非 prefill 自动塞):
- Anthropic Skills / Agent SDK / Claude Code subagent(v2 P1/P2 已对标 · v3 主线协议层不重做 SOTA 调研,聚焦"已知最佳实践 transformer 复用")
- GitHub Spec Kit 0.8.7 schema(若 v3 触发 protocol §6 修订需要)
- Cursor 3 multi-root + worktrees(v2 已对标 workspace 4 字段,v3 修订 Cross-device publish 时可再核)
- v3 默认 Z mode = **不对标 / 内部收敛**(11 项 backlog 全部来自本仓真路径累积证据,无需外部 SOTA 验证就有充分 evidence)

## Y default recommendation

| Y 维度 | 默认 | 触发关键词 evidence |
|---|---|---|
| 产品价值 | ☐ | (v3 是 framework 内部协议级修订 · 不直接面向 product user · operator 可勾) |
| 架构设计 | ☑ | "framework/pipeline 的共识方案" + v2 K8 "协议级修订 4 项" + ENTRY 14/15 "协议级 corruption 风险" |
| 工程纪律 | ☑ | "工程纪律" + "可靠、自动化程度最高" + HANDBACK-LOG 17 ENTRY 全程 evidence + ENTRY 9 "spec retroactive amendment 标 OUT-of-scope" |
| 安全 | ☐ | (Safety Floor 三件套 v0.1 已 ship · v3 不在安全维度;A1 scan-credentials exit code 是 lib bug 不是安全维度) |
| 教学价值 | ☐ | (内部协议修订无 onboarding scope) |
| 商业可行 | ☐ | (operator 单人 · evidence: P3R2-GPT §4 W4 OUT-1) |
| 用户体验 | ☐ | (operator = sole user · v3 不动 UX) |
| **Y5 重做代价 / 沉没成本 / 知识保留** | ☑ | v2 已勾此自定义 Y · v3 11 项 backlog 多个涉及 mirror rebuild "现有子树范围" vs "全 cover" 的 L/P/C trade-off · ENTRY 10 Cluster A 选项 1 即此 axis;**强烈建议 v3 继续勾** |

**至少推荐 ✅ 数**:3 项(架构设计 + 工程纪律 + Y5 重做代价 — 与 v2 Y 配置完全同档,反映 v3 是 v2 落地修订而非新主题)

## W default recommendation

| W 形态 | 默认 | 理由 |
|---|---|---|
| verdict-only | ☑ | (always · v3 11 项 backlog 必须有单一收敛 verdict) |
| decision-list | ☑ | (always · v3 主线就是 11 项决议表 keep/cut/new/amend) |
| next-PRD | ☐ | (v0.1 已 ship 封箱;v3 不产 v0.2 PRD · 若 backlog 大到触发 v0.2 PRD 再说;主命令呈现时让 operator 决定 explicit add) |
| refactor-plan | ☑ | "rebuild" / "反向同步" / "mirror 子树范围" / "协议级修订" + ENTRY 10/11/12/13/14 全部含 mirror rebuild evidence |
| next-dev-plan | ☑ | "v0.2 forge backlog · skills mirror rebuild" + ENTRY 8 "全入 v0.2 forge backlog" + ENTRY 14 "协议级 Cluster B 累积" + ENTRY 17 "步骤 3 + 4 待 operator 跨仓执行" |
| free-essay | ☐ | (v3 是落地修订 · 不需要 800 字 essay 论证大架构;若 expert 觉得有跨 backlog 系统性 insight 可自行旁注) |

**至少推荐 ✅ 数**:4 项(verdict-only + decision-list + refactor-plan + next-dev-plan — 与 v2 W 配置略减 PRD/essay,反映 v3 是协议级 + lib 修订 batch 而非新主题论述)

## Reachability check on all X paths

| Path | Reachable | Type | Note |
|---|---|---|---|
| proposals.md §006 | ✅ | proposal-section | line 224-247 |
| discussion/006/forge/v2/stage-forge-006-v2.md | ✅ | stage-doc | v3 主锚 |
| discussion/006/forge/v2/{forge-config, moderator-notes, _x-input-draft-by-operator}.md | ✅ | stage-doc(aux) | |
| discussion/006/handback/HANDBACK-LOG.md | ✅ | stage-doc(append-only) | **v3 最核心 X** · 17 ENTRY |
| discussion/006/handback/20260511T*.md (5 包 batch 1) | ✅ | handback-package | HANDBACK-LOG 已摘要 |
| discussion/006/handback/20260524T*-20260525T*.md (11 包 batch 2) | ✅ | handback-package | HANDBACK-LOG ENTRY 7-17 摘要 |
| framework/SHARED-CONTRACT.md | ✅ | internal-path | 协议层 4 项修订标的 |
| framework/xenodev-bootstrap-kit/eval-event-log/{writer,reader}.sh | ✅ | internal-path | mirror 现状(writer 已 SSOT) |
| framework/xenodev-bootstrap-kit/handback-validator/{validate, _yaml-helpers, check-1..6, score-handback?}.sh | ✅ | internal-path | mirror 现状(validate + _yaml + check-3 + check-5 已 SSOT;templates/gen/score 待 rebuild) |
| framework/xenodev-bootstrap-kit/safety-floor-{1,2,3}/*.sh | ✅ | internal-path | v0.1 ship 时 cp · mirror 现状 |
| framework/xenodev-bootstrap-kit/workspace-schema/{extract,validate}.sh | ✅ | internal-path | mirror 现状 |
| /Users/admin/codes/XenoDev/.claude/skills/parallel-builder/SKILL.md | ✅ | external-path | mirror 待 rebuild |
| /Users/admin/codes/XenoDev/.claude/skills/spec-writer/SKILL.md | ✅ | external-path | mirror 待 rebuild |
| /Users/admin/codes/XenoDev/.claude/skills/codex-review/SKILL.md | ✅ | external-path | mirror 待 rebuild |
| /Users/admin/codes/XenoDev/.claude/hooks/wrappers/dangerous-event-emit.sh | ✅ | external-path | mirror 待 rebuild |
| /Users/admin/codes/XenoDev/tests/integration/*.sh(8 个) | ✅ | external-path | mirror 待 rebuild |
| /Users/admin/codes/XenoDev/lib/handback-validator/{templates/handback.template.md, gen-handback.sh, score-handback.sh} | ✅ | external-path | mirror 待 rebuild · templates 三节 + tags array + gen --section1/2/3 + score 3 字段 |
| /Users/admin/codes/XenoDev/lib/eval-event-log/event-schema.json | ✅ | external-path | enum 单复数协议级修订源 |
| /Users/admin/codes/XenoDev/PRD.md | ✅ | external-path | v0.1 已 ship · 默认不勾 |
| v1 X #2-#9(idea_gamma2 / vibe-workflow / autodev_pipe 7 path) | ✅(v2 已验) | external-path | v3 默认 no-rerun |

## Quality flags

- [x] proposal section detected:✅
- [x] ≥1 X candidate extracted:✅(主线 ≥ 8 项 v3-specific X + 历史 9 项 v1 no-rerun X · 总 17+)
- [x] K seed ≥ 80 chars:✅(~2350 chars · 含 proposal verbatim + K8-K11 v3 specific)
- [x] At least 1 Y default recommended:✅(架构设计 + 工程纪律 + Y5 = 3 项)
- [x] At least 1 W default recommended:✅(verdict-only + decision-list + refactor-plan + next-dev-plan = 4 项)

## Operator pre-input materials note

> ⚠ **prefill 子代理职责边界**:本 draft **只**基于:
> - proposals.md §006 verbatim(K seed proposal 部分)
> - discussion/006/forge/v2/stage-forge-006-v2.md(继承标记)
> - discussion/006/handback/HANDBACK-LOG.md ENTRY 1-17(11 项 backlog 提取)
> - 本仓 framework/xenodev-bootstrap-kit/ + /Users/admin/codes/XenoDev/ 子树 glob(reachability + mirror 现状 vs 待 rebuild 标定)
>
> prefill **不脑补**:
> - 11 项 backlog 的具体修订方案(那是 Phase 1 Opus / Phase 3 Codex 的事)
> - Cross-device publish §6 文本(Phase 2 ALL-FOR-A)
> - event-schema enum 应统一为单还是复(Phase 1 双 expert)
> - mirror rebuild 是 manual cp 还是 git subtree(Phase 1 双 expert)
> - lib bug 优先级排序(Phase 3 final verdict)
>
> 若 operator 在 v3 forge 之前已写过 `_x-input-draft-by-operator.md` / `moderator-notes.md`(v2 模式),主命令在 0.5.5.c K editor / 0.5.5.d Z editor 时**仍按本 draft 列出** K + Y/W 推荐,operator 在交互界面手追加。

## Prefill summary(给主命令的简要)

```
prefill_status: success
draft_file: discussion/006/forge/v3/_prefill-draft.md
x_candidates: 17 (proposal=4 group | v2-stage=3 | handback=2 | framework-internal=2 | XenoDev-external=8)
k_seed_bytes: ~2350
z_candidates_present: false (proposal §006 无 §相邻方案;v3 默认 Z mode = 不对标/内部收敛)
intermediate_products_found: [v2-stage-doc, HANDBACK-LOG, framework/xenodev-bootstrap-kit-mirror, XenoDev-ssot-tree]
y_recommended: [架构设计, 工程纪律, Y5-重做代价/沉没成本/知识保留]
w_recommended: [verdict-only, decision-list, refactor-plan, next-dev-plan]
estimated_tokens_full_history: 40k (⚠ ≥ 8k · 主命令应软警告)
estimated_tokens_default_bundle (v0.2-protocol-bump): 22k (⚠ ≥ 8k · 主命令应软警告但这是 v3 主线必读)
default_bundle: v0.2-protocol-bump
```
