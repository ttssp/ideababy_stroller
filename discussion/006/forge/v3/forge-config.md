---
doc_type: forge-config
forge_id: 006
forge_version: v3
created: 2026-05-27T12:21:47Z
prefill_source: proposals.md§006 + handback-log batch 2 + v2 stage doc
convergence_mode: strong-converge
x_count: 13
x_hash: 1504bfea63c84d916d57bd2f48a634f5
y_count: 3
w_count: 6
z_mode: 不对标 · 纯内部审阅
k_provenance: verbatim
v3_mission: Bootstrap kit v0.2 反向同步 + 协议修订 + lib bug 清班
inheritance: v2 verdict 不重审(IDS = 治理 / XenoDev = 唯一 L4 / 双向 hand-off)
---

# Forge config · idea 006 · v3

## X · 审阅标的(13 个文件 · 9 大 X 槽位)

per bundle:v0.2-protocol-bump + operator 额外加 event-schema.json。所有标的 reachable ✅。

### 槽位 1 · v2 verdict baseline(继承 · 不重审)
- [x] `discussion/006/forge/v2/stage-forge-006-v2.md`
  - type: stage-doc
  - 用途:v3 主线锚 — v2 decision matrix / W3 refactor plan / W4 PRD 草案 / W5 B1+B2 dev plan / W6 essay
  - 读取策略:整文件 Read(4583 字 / 476 行)

### 槽位 2 · v0.1 ship 后 backlog 源(v3 主输入)
- [x] `discussion/006/handback/HANDBACK-LOG.md`
  - type: stage-doc(append-only log)
  - 用途:17 ENTRY 决议 · 11 项 backlog 全在此(ENTRY 7-17 batch 2 = 2026-05-27 真路径)· §"汇总 IDS-side 行动 batch 2 §5 backlog 总览"是 verdict 直接锚
  - 读取策略:整文件 Read(~227 KB · 但实际 batch 2 部分约 30KB)

### 槽位 3 · 协议层(本仓)
- [x] `framework/SHARED-CONTRACT.md`(v2.0 现行)
  - type: internal-path
  - 用途:协议 4 项修订源 — Cross-device publish §6 / event-schema enum / IDS dir flock / `--ids-verdict-evidence` flag

### 槽位 4 · IDS mirror 现状(rebuild 目标 = 此 + 缺失子树)
- [x] `framework/xenodev-bootstrap-kit/`(整子树)
  - type: internal-path
  - 22 个 .sh + README + templates
  - 已 SSOT 同步 5 文件(本 session 2026-05-27 ENTRY 7+9+13 cp)
  - 待 rebuild 子树:skills/* + hooks/wrappers/ + tests/integration/ + handback-validator/{templates,gen,score}

### 槽位 5-7 · XenoDev SSOT skills(mirror rebuild 4 个子树之一)
- [x] `/Users/admin/codes/XenoDev/.claude/skills/parallel-builder/SKILL.md`(ENTRY 11 cross-device fallback §6.3)
- [x] `/Users/admin/codes/XenoDev/.claude/skills/spec-writer/SKILL.md`(ENTRY 10 portability fallback §3.1)
- [x] `/Users/admin/codes/XenoDev/.claude/skills/codex-review/SKILL.md`(ENTRY 7/10/13/17 §6 anti-pattern + 4 轮 + ship-blocker precedent)

### 槽位 8 · XenoDev SSOT hooks(mirror rebuild 4 个子树之二)
- [x] `/Users/admin/codes/XenoDev/.claude/hooks/wrappers/dangerous-event-emit.sh`(ENTRY 12 Safety Floor + eval-event-log wire)

### 槽位 9 · XenoDev SSOT tests(mirror rebuild 4 个子树之三)
- [x] `/Users/admin/codes/XenoDev/tests/integration/`(8 .sh:bootstrap-verify / round-trip / negative / events-count / cleanup / verify-all / --ids-verdict-confirmed)

### 槽位 10-12 · XenoDev SSOT handback-validator 子树(mirror rebuild 4 个子树之四)
- [x] `/Users/admin/codes/XenoDev/lib/handback-validator/templates/handback.template.md`(ENTRY 13 §1/§2/§3 三节固定 body)
- [x] `/Users/admin/codes/XenoDev/lib/handback-validator/gen-handback.sh`(ENTRY 16 + ENTRY 8 A4 `--out` 前缀 bug)
- [x] `/Users/admin/codes/XenoDev/lib/handback-validator/score-handback.sh`(ENTRY 16 case F regression + escape)

### 槽位 13 · 额外加(operator override · 协议 B2 原文)
- [x] `/Users/admin/codes/XenoDev/lib/eval-event-log/event-schema.json`(enum 单复数统一 = ENTRY 15/16 B2 原文)

## Y · 审阅视角(3)

- 架构设计(prefill 推荐 · v2 也用)
- 工程纪律(prefill 推荐 · v2 也用 · case F stale 重点)
- **Y5 重做代价 / 沉没成本 / 知识保留**(operator 自定义 · v2 同档 · Cluster A 边界纪律的核心 axis)

## Z · 参照系

**模式**:不对标 · 纯内部审阅(prefill 默认 · v3 是落地协议 + lib 修订 batch · SOTA 对标价值低 · 跳 Phase 2 web search)

## W · 产出形态(6 · 全)

- verdict-only(单 verdict + ≤500 字 rationale)
- decision-list(4 列矩阵 keep/cut/new/amend · 11 backlog 一一对一)
- refactor-plan(mirror rebuild SOP · 按 4 子树 + 协议 4 项分组)
- next-dev-plan(v0.2 dev plan · 按 phase/milestone 切)
- next-PRD(v0.2 PRD draft · 可直接进 plan-start)
- free-essay(800-1500 字跨 backlog 系统性 insight)

## K · 用户判准(verbatim)

```
// from "想法":
给定一个PRD,claude code可以几乎没有人工干预的情况下自主完成开发任务。
我需要一个**可靠的、自动化程度最高**解决方案。

// from "我为什么想做这个":
我是非软件开发背景。我可以将需求描述清楚,我也可以尝试构建较可靠的PRD。
但是我缺少软件开发的经验,对各个规模(大中小型)的开发的方案、流程、规范等内容都没有把握。

// from "我已经想过的角度"(非路径文字部分):
我最近一个月做了很多尝试:
1. 第一个项目名 idea_gamma2(数字基建,phase + pipeline skill + phase-retrospective + subagent + skills)
2. 第二个项目 vibe-workflow(engineer team 协作 + 自动化开发)
3. 第三个项目 autodev_pipe(借鉴 vibe coding / agentic coding 最佳实践 + agent-skills + superpowers · 专业的自动化开发流程)
4. 第四个项目当前 repo(idea→PRD→自动开发)

// from "我诉求":
希望双方凭借最强的 AI 专业能力以及最丰富的软件开发经验,通过调研、论证、思辨、构思、设计、整理归纳等方式,达成一套基于 Claude Code 实现**可靠**自动化开发的 framework/pipeline 的共识方案

// === v3 specific additions(operator append 2026-05-27)===

K8(v3 mission · binding):v3 mission = "Bootstrap kit v0.2 反向同步、带上协议修订 + lib bug 清班"。
v0.1(006a-pM)已 ship 封箱(2026-05-27);v3 不重审 idea / 不重审 v2 verdict 主线,只在 v2 verdict 落地后的 **真路径 backlog 三类** 上收敛:
  (a) **mirror rebuild 4 子树**:skills/{parallel-builder, spec-writer, codex-review} + hooks/wrappers + tests/integration + handback-validator/{templates, gen-handback, score-handback}
  (b) **协议级修订 4 项**(SHARED-CONTRACT §6 + event-schema):Cross-device publish 段 / event-schema enum 单复数统一(operator_interventions/review_failures 复 vs handback_drift 单) / IDS dir flock/fcntl / `--ids-verdict-evidence` flag
  (c) **XenoDev 本仓 lib bug 3 项**:scan-credentials exit code + 14 false positive 治理 / gen-handback `--out` 默认前缀 / FU-producer-1 case F stale(T007 ship 后 template 无 `{{RATIONALE}}` · main 14/15 fail 真 regression)

K9(v2 verdict 继承 · 不重审):v2 已收敛"IDS=idea→PRD + 治理 / XenoDev=唯一 L4 runtime / 双向 hand-off"= v3 不动这个大架构,只动落地后的协议 + lib 细节修订。

K10(operator 偏好 · 评分 #2 加分依据):Cluster A 选项 1(锁定 mirror 现有子树范围)的实证已成熟 — 单 ENTRY 7/9/13 三连 cp + 不越 mirror 边界;v3 修订 mirror 子树范围时应延续这种"边界先定、批量 SSOT、不越界"的纪律。

K11(v3 收敛模式偏好):strong-converge(operator 已对 v2 强 binding;v3 同档)— 11 项 backlog 应一一对一收敛产 verdict,不允许"双方都对"式压扁,残余分歧用 v0.2-note 旁注。
```

## 收敛模式

strong-converge(K11 binding · 与 v2 同档)
