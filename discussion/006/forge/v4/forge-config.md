---
doc_type: forge-config
forge_id: 006
forge_version: v4
created: 2026-05-29T16:39:15Z
prefill_source: manual(post-v0.2 backlog 不来自 proposals.md)
convergence_mode: strong-converge
x_count: 13
x_hash: 9ea15bafc3cbcd841d7a14398f7c132f
y_count: 3
w_count: 4
z_mode: 不对标 · 纯内部审阅
k_provenance: verbatim + v4 K8/K9 替换
v4_mission: post-v0.2-shipped 协议层稳态化 + 治理债清理
inheritance: v3 verdict 不重审(11 项 backlog 三类 batch ship 已真路径实证成功 · v0.2-shipped 关闭判据全达成)
---

# Forge config · idea 006 · v4

## 背景:为什么起 v4

v3 verdict(11 项 backlog 三类 batch ship · 3 wave 顺序)已在 v0.2 真路径 ship 完整闭环(IDS 10 commit + XenoDev 13 commit · 2026-05-30 双仓 push):

- O1-O6 全 PASS · SLA §1.3 状态 2 达成 · v0.2-shipped reached
- 11 项 backlog 全闭环(N×9 mirror + R×3 lib bug + B-1/B-2/B-4 协议改 + B-3 v0.2-note + B-4-XenoDev runtime)
- HANDBACK-LOG ENTRY 18-29 batch 3 入库 · 12/12 6 约束 validator PASS

但 v0.2 ship 过程**额外暴露 / 累积**了 5 项新 backlog,**v3 verdict 范围外**:

1. **R-Q6**(HANDBACK-LOG ENTRY 29):validate-handback.sh + handback-review.md consumer-side 升 7 字段 verify · 当前只 TX04 ship 加固 verify-ppv-p2.sh · 剩 2 consumer 未升
2. **R-Q7**(HANDBACK-LOG ENTRY 29):REVIEW-LOG immutable per-review path · 防 singleton `cat >` 覆盖 async hand-back invalidate 老 SHA
3. **contract_version 治理债**(我审计发现):SHARED-CONTRACT v0.2 wave 2 已 ship 169 行协议改(B-1 + B-4-IDS + B-3-note),但 `contract_version` 还是 `2.2` · Changelog v0.2 4 行已写但 frontmatter 未 bump · 违反 semver 纪律
4. **B-3 IDS dir flock 升级判定**(v3 v0.2-note 触发条件):v0.2 真路径跑了 12 包 hand-back round-trip 0 撞库 · 触发条件未实证 · v4 决定是否进 v0.3 主线 / 继续留 v0.4-note / 直接 cut
5. **D-precedent codify**(v0.2 多次出现 needs-attention 接受 ship 模式):D2(OQ-4 解法 A)/ D3-T203(spec vs 真路径 cp 数)/ D3-T208(mirror SHA stale)/ D4-T205(finding 不在 file_domain 内 transitional bind)/ D6-T301/T304/T306(adversarial-review 接受 ship)— 7 次 D-precedent 累积 · 是否升 SHARED-CONTRACT § normative 流程

v4 = 把这 5 项 backlog 收敛成 v0.3 ship 计划(单 wave · 不再三波 · 也可能拆 2 wave · forge 决)。

## X · 审阅标的(13 个文件 / 9 大槽位)

per v4 mission · 全 reachable ✅ · 跨仓读 #6-#11 与 v3 同范式(v3 跑通过)

### 槽位 1 · v3 verdict baseline(继承 · 不重审)

- [x] `discussion/006/forge/v3/stage-forge-006-v3.md`
  - type: stage-doc
  - 用途:v3 verdict 主线锚 — W2 decision matrix / W3 refactor plan / W4 PRD draft / W5 dev plan / W6 essay
  - 读取策略:整文件 Read(34918 字节 / ~611 行 · v4 P1 只引 verdict + W2 段)

### 槽位 2 · v3 双方 P3R2(verdict 双方收敛证据)

- [x] `discussion/006/forge/v3/P3R2-Opus47Max.md`
- [x] `discussion/006/forge/v3/P3R2-GPT55xHigh.md`
  - type: stage-doc
  - 用途:v3 strong-converge 双方 0 unresolved 实证 · K11 binding 来源 · v4 K9 不重审依据

### 槽位 3 · 协议层(治理债源头)

- [x] `framework/SHARED-CONTRACT.md`(v2.2 现行 · 含 v0.2 4 行 Changelog 但 frontmatter 未 bump)
  - type: internal-path
  - 用途:contract_version 治理债 P0 · §6 B-1/B-4-IDS 协议段 audit · Changelog 历史

### 槽位 4 · v0.2 ship 全 audit trail

- [x] `discussion/006/handback/HANDBACK-LOG.md`
  - type: stage-doc(append-only log · 657 行)
  - 用途:ENTRY 18-29 batch 3 = R-Q6/R-Q7 落点 / D-precedent 全集 / contract_version 漂移记录 · v4 主输入源
  - 读取策略:tail 段(ENTRY 18-29 + batch 3 汇总 = ~280 行)

### 槽位 5-6 · XenoDev SSOT spec + risks(R-Q6/R-Q7 / D-precedent 现场)

- [x] `/Users/admin/codes/XenoDev/specs/006a-pM-v0.2/spec.md`
  - 含 operator_decision_log D2-D6 + 28 task DAG + PPV 第 7 元素
- [x] `/Users/admin/codes/XenoDev/specs/006a-pM-v0.2/risks.md`
  - R-Q5(已加固)/ R-Q6 / R-Q7 / R-D2 cross_repo_split 协议消费失败

### 槽位 7-8 · XenoDev PPV 真路径脚本

- [x] `/Users/admin/codes/XenoDev/scripts/verify-ppv-p1.sh`(O1 mirror byte-equal + O2 MANIFEST 7 字段 + O5 fail-closed verify-all)
- [x] `/Users/admin/codes/XenoDev/scripts/verify-ppv-p2.sh`(B-4-XenoDev round-trip + R-Q5 freshness · TX04 已加固)
  - 用途:R-Q6 升 consumer-side 时参考已实现的 producer 脚本

### 槽位 9 · XenoDev REVIEW-LOG(R-Q7 现场)

- [x] `/Users/admin/codes/XenoDev/.claude/skills/codex-review/REVIEW-LOG.md`
  - 用途:singleton path 现状 · R-Q7 升 immutable per-review path 时改造对象

### 槽位 10 · XenoDev validator(R-Q6 现场)

- [x] `/Users/admin/codes/XenoDev/lib/handback-validator/validate-handback.sh`
  - 用途:6 约束 consumer mode validator · R-Q6 升 7 字段 verify 时改造对象

### 槽位 11 · HANDOFF §7 协议(cross_repo_split 实证)

- [x] `discussion/006a-pM-v0.2/L4/HANDOFF.md`
  - 用途:§7 cross_repo_split 扩展协议 · v4 决定是否升 SHARED-CONTRACT §6 normative

### 槽位 12 · MANIFEST 真路径 audit trail

- [x] `framework/xenodev-bootstrap-kit/MANIFEST-v0.2.md`
  - 用途:3 wave × 7 字段 audit trail · K10 边界纪律真路径实证 · v4 MANIFEST schema 是否升 SSOT

### 槽位 13 · v3 Changelog 段(治理债源头细看)

注:槽位 13 复用槽位 3 同一文件,但 P1/P2 读取焦点不同 — 槽位 3 = §6 协议段 + frontmatter;槽位 13 = Changelog 段(L1073+,看 2026-05-29 v0.2 4 行 entry 与 frontmatter 不同步细节)。同一物理文件,但 read scope 分离 · count 仍计 1 X · 实际 X count = 12 unique files。

## Y · 审阅视角(3)

- 架构设计(prefill · 同 v2/v3)
- 工程纪律(prefill · 同 v2/v3 · contract_version bump 纪律为核心 axis)
- **Y6 治理债 + protocol forward-evolution**(v4 自定义 · operator override)
  - contract_version bump 纪律(semver · Changelog 与 frontmatter 同步)
  - D-precedent codify(7 次 accept-with-followup 模式是否升 normative)
  - cross_repo_split §7 是否升 SHARED-CONTRACT §6 normative

## Z · 参照系

**模式**:不对标 · 纯内部审阅

理由:R-Q6/R-Q7 是内部 lib 实装细节 · contract_version 是内部 semver 纪律 · B-3 dir flock 已在 v3 决"无 SOTA 对标价值"(沿用)· D-precedent codify 是内部治理 · 全部不对外。跳 Phase 2 web search · 与 v3 一致 · 0 search。

## W · 产出形态(4)

- verdict-only(单 verdict + ≤500 字 rationale)
- decision-list(5 项 backlog 一一对一:R-Q6 / R-Q7 / contract_version bump / B-3 / D-precedent codify · 每项 keep/refactor/cut/new + 理由)
- refactor-plan(按模块 + P0/P1/P2 优先级 · 估时)
- next-dev-plan(估时 + 改哪个仓 + cross_repo_split target_repo 标 · 估 1 wave 或 2 wave)

**不要 next-PRD**(v4 不引入新 idea / 新 PRD)
**不要 free-essay**(v3 已写过 K10 系统性 insight 足)

## K · 用户判准(verbatim + v4 K8/K9 替换 · K10/K11 verbatim 不动)

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

// === v4 specific additions(operator append 2026-05-29 post-v0.2-shipped)===

K8(v4 mission · binding):v4 mission = "post-v0.2-shipped 协议层稳态化 + 治理债清理"。
v0.2(006a-pM-v0.2)已 ship 封箱(2026-05-29 · O1-O6 全 PASS · SLA §1.3 状态 2);
v4 不引入新 idea / 新 PRD / 新 fork,只在 v0.2 ship 后暴露的 **5 项 backlog** 上收敛:
  (a) **R-Q6**:validate-handback.sh + handback-review.md consumer-side 升 7 字段 verify(剩 2 consumer 未升)
  (b) **R-Q7**:REVIEW-LOG immutable per-review path(防 singleton `cat >` 覆盖 async invalidate)
  (c) **contract_version 治理债** P0:SHARED-CONTRACT v0.2 169 行协议改已 ship 但 frontmatter `contract_version: 2.2` / `status: v2.2` 未 bump · Changelog v0.2 4 行已写但版本号漂移 · 违反 semver 纪律
  (d) **B-3 IDS dir flock 升级判定**:v0.2 真路径 12 包 hand-back round-trip 0 撞库 · 触发条件未实证 · v4 决进 v0.3 主线 / 继续留 v0.4-note / 直接 cut 三选一
  (e) **D-precedent codify**:v0.2 7 次 accept-with-followup(D2/D3-T203/D3-T208/D4-T205/D6-T301/T304/T306)· 是否升 SHARED-CONTRACT § normative 流程 / 还是留 spec.md operator_decision_log 局部纪录

K9(v3 verdict 继承 · 不重审):v3 已收敛"11 项 backlog 三类 batch ship · 3 wave 顺序"在 v0.2 真路径完整闭环(O1-O6 全 PASS · 0 残余分歧 · 1 v0.2-note B-3 已在 changelog 显式 · 12/12 6 约束 validator PASS)= v4 不动 v3 大架构,只动 post-v0.2 暴露的 5 项 backlog 细节修订。
v2 verdict(IDS=治理 / XenoDev=唯一 L4 / 双向 hand-off)同样不重审(K9 binding 透传 v3→v4)。

K10(operator 偏好 · verbatim 不动):Cluster A 选项 1(锁定 mirror 现有子树范围)的实证已成熟 — 单 ENTRY 7/9/13 三连 cp + 不越 mirror 边界;v0.2 wave 1+2 mirror 19 文件实证再次延续了这种"边界先定、批量 SSOT、不越界"的纪律 · v4 修订 mirror 子树范围或协议字段时应延续。

K11(v4 收敛模式偏好 · verbatim 不动 · v0.2 → v0.3):strong-converge(operator 已对 v2/v3 强 binding;v4 同档)— 5 项 backlog 应一一对一收敛产 verdict,不允许"双方都对"式压扁,残余分歧用 v0.3-note 旁注。
```

## 收敛模式

strong-converge(K11 binding · 与 v2/v3 同档 · 残余分歧降 v0.3-note 旁注)
