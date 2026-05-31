# Forge Stage · 006 · v4 · "post-v0.2-shipped 协议层稳态化 + 治理债清理"

**Generated**: 2026-05-31T11:00:00+08:00
**Source**: forge run v4 with X = 13 引用 / 12 unique files / 9 槽位, Y = 架构设计 + 工程纪律 + Y6 治理债/protocol forward-evolution, Z = 不对标 · 纯内部审阅, W = verdict-only + decision-list + refactor-plan + next-dev-plan
**Convergence mode**: strong-converge
**Rounds completed**: P1 (both) · P2 (skipped · Z=不对标 + 无外部材料 · 同 v3) · P3R1 (both) · P3R2 (Opus 单侧 finalize · 因 P3R1 已 0 unresolved · operator 选项 3 省 Codex P3R2)
**Searches run**: 0(Z mode = 不对标 · 跳 Phase 2 web search)
**Moderator injections honored**: none(`moderator-notes.md` 不存在)
**Convergence outcome**: converged(P1 层 6 项 backlog 0 分歧 · P3R1 3 个实现层细节双向锁定 · 0 unresolved)

---

## How to read this

forge 是横切层(不是 L1-L4 pipeline 的一部分)。本文档是双专家审阅(Opus 4.7
Max + GPT-5.5 xhigh)在 v4 fresh intake 后,对 **v0.2-shipped 之后暴露的 6 项
post-v0.2 backlog** 的强收敛产出。**v4 mission 与 v2/v3 大架构无关**(K9 binding):
不重审 IDS=治理 / XenoDev=唯一 L4 / 双向 hand-off,也不动 v3 已实证的 11 项
backlog 三类 3 wave,只清理 v0.2 ship 后累积的协议债 + 治理债。

读完后你应该:

- 知道 6 项 backlog 一一对一的最终 verdict(keep×1 / refactor×3 / new×2 · 见 §"Decision matrix")
- 知道支持每条结论的具体证据(§"Evidence map" 可逐条溯源到 P1 / P3R1 / P3R2 段落 + HANDBACK-LOG / SHARED-CONTRACT / XenoDev 脚本现场)
- 拿到按 W 4 形态准备好的可执行草案:verdict rationale / 决策矩阵 / 3 模块 refactor plan / 2 波 next-dev-plan
- 能基于 §"Decision menu" 直接进入下一步(进 L4 plan-start / 跑 forge v5 / 局部接受 / park / abandon)

**注意本 v4 是精简 5 round file 路径**(非标准 8):P2×2 因 Z=不对标无 SOTA
对标价值跳过(同 v3);Codex P3R2 因 P3R1 已 0 unresolved 由 operator 选项 3
省去,单一 verdict 由 Opus P3R2 finalize 表达、双方 P1+P3R1 全程同向背书。详见
§"What this menu underweights"。

## Verdict

**CONCERNS · v4:不动 v3 11 项大架构,以 2 wave 清理 6 项 post-v0.2-shipped 协议债。**

v0.2 已真路径 ship(O1-O6 全 PASS · 双仓 push 完成),所以**不是 BLOCK**;但
consumer-side 7 字段缺验(R-Q6)、REVIEW-LOG singleton 可变路径(R-Q7)、
contract_version 漂移三处是协议层可见债,所以**不是 CLEAN**。6 项分两波:**P0
原子波**(R-Q6 共享 lib validator + R-Q7 immutable path + B-4-IDS 示例更新 +
contract bump 2.3 · 四件事必须同 wave 原子落地,否则"版本已 bump 示例仍鼓励
singleton"治理反债)+ **P1 波**(D-precedent codify 升 SHARED-CONTRACT §8 ·
cross_repo_split 升 §6 normative)。B-3 IDS dir flock 续 v0.3-note。

**K 对齐**:K8 稳态+治理债清理 ✅ / K9 不重审 v3 11 项 + 不回审 v0.2 七次历史
✅(D-precedent 只立准入流程)/ K10 边界先定+批量 SSOT+不越界(共享 lib +
编号避撞)✅ / K11 strong-converge 单一 verdict + B-3 降 v0.3-note ✅。**0 unresolved。**

## Evidence map

| 结论 | 来源 | 引用(≤15 words) | 反对证据 |
|---|---|---|---|
| R-Q6 = new · P0 | P1-Opus §2.A + P1-GPT §2 row1 + P3R1 双侧分歧1 | "验证链单向不对称是真 gap" | - |
| R-Q6 抽共享 lib(非复制 awk) | P1-GPT §3.1 + P3R1-GPT 分歧1 + P3R2 §1 | "必须从 verify-ppv-p2.sh 抽成共享 lib · 不复制 awk" | - |
| R-Q7 = refactor · P0 | P1-Opus §2.B + P1-GPT §2 row2 + P3R2 §2 | "REVIEW-LOG singleton → immutable per-review path" | ⚠ 时序条件较严 · 单 operator 几乎不触发(见 underweights) |
| contract bump 2.3(非 3.0) | P1-Opus §3.1 + P1-GPT §2 row3 + P3R1-Opus 不确定1 收敛 | "旧 hand-back 6 约束兼容读 · 新 7 字段 forward-only" | - |
| 四件事 P0 同 wave 原子落地 | P3R1-GPT 分歧2 + P3R2 §1/§2 | "版本已 bump 示例仍鼓励 singleton 治理反债" | - |
| B-3 IDS dir flock = keep · 续 v0.3-note | P1-Opus §2.D + P1-GPT §2 row4 + P3R2 §3 note1 | "12 包 round-trip 0 撞库 · 触发条件未实证" | - |
| D-precedent codify = new · P1 | P1-Opus §2.E + P1-GPT §2 row5 + P3R1 分歧3 | "只 codify 准入流程 · 不回审 7 次历史"(K9) | - |
| D-precedent 入 SHARED-CONTRACT §8 | P3R1-Opus 分歧3 + P3R1-GPT 分歧3 + P3R2 §1 | "§8 governance · 避撞 HANDOFF §7" | - |
| cross_repo_split 升 §6 normative = refactor · P1 | P1-Opus §2.F(新增项)+ P1-GPT §2 row6 + P3R2 §1 | "三层已消费 · 不升 SSOT 下次 idea 重抄碎片化" | - |
| verdict = CONCERNS(非 BLOCK/非 CLEAN) | P1-GPT §2 + P3R1-Opus §2 + P3R2 §2 | "v0.2 已 ship 故非 BLOCK · 三处协议债故非 CLEAN" | - |

(双方 P1 对 6 项 backlog **逐条同决策类别** · P3R1 仅剩 3 个实现层细节 · 全部 R1 双向锁定 · 故反对证据极少)

## Intake recap

### X · 审阅标的(13 引用 / 12 unique files / 9 槽位)
- 槽位1 · v3 verdict baseline(`discussion/006/forge/v3/stage-forge-006-v3.md` · 继承不重审)— stage-doc
- 槽位2 · v3 双方 P3R2(strong-converge 0 unresolved 实证)— stage-doc
- 槽位3+13 · `framework/SHARED-CONTRACT.md`(v2.2 现行 · §6 协议段 + frontmatter + Changelog · 治理债源头)— internal-path
- 槽位4 · `discussion/006/handback/HANDBACK-LOG.md`(657 行 · batch 3 ENTRY 18-29 = R-Q6/R-Q7/D-precedent 落点)— stage-doc
- 槽位5-6 · XenoDev `specs/006a-pM-v0.2/spec.md` + `risks.md`(operator_decision_log + R-Q5/Q6/Q7)— internal-path
- 槽位7-8 · XenoDev `scripts/verify-ppv-p1.sh` + `verify-ppv-p2.sh`(producer 端 7 字段 PPV 实证)— internal-path
- 槽位9 · XenoDev `.claude/skills/codex-review/REVIEW-LOG.md`(R-Q7 singleton 现场)— internal-path
- 槽位10 · XenoDev `lib/handback-validator/validate-handback.sh`(R-Q6 6 约束 consumer 现场)— internal-path
- 槽位11 · `discussion/006a-pM-v0.2/L4/HANDOFF.md`(§7 cross_repo_split 实证)— stage-doc
- 槽位12 · `framework/xenodev-bootstrap-kit/MANIFEST-v0.2.md`(3 wave × 7 字段 audit trail)— stage-doc

### Y · 审阅视角
- 架构设计(prefill · 同 v2/v3)
- 工程纪律(prefill · contract_version bump 纪律为核心 axis)
- Y6 治理债 + protocol forward-evolution(v4 自定义 · operator override · 含 contract bump 纪律 / D-precedent codify / cross_repo_split 升 normative)

### Z · 参照系
- mode: 不对标 · 纯内部审阅(R-Q6/R-Q7 = 内部 lib 细节 · contract_version = 内部 semver · D-precedent = 内部治理 · 全不对外)
- 用户外部材料: 无
- Phase 2 web search: 跳过 · 0 search(同 v3)

### W · 产出形态(4)
- verdict-only(单 verdict + ≤500 字 rationale)→ §"Verdict rationale"
- decision-list(6 项 backlog 一一对一)→ §"Decision matrix"
- refactor-plan(按模块 + P0/P1 优先级 + 估时)→ §"Refactor plan"
- next-dev-plan(2 波 + target_repo 标 + 估时)→ §"Next-version dev plan"
- **不含 next-PRD**(v4 不引入新 idea / 新 PRD)
- **不含 free-essay**(v3 已写过 K10 系统性 insight)

### K · 用户判准(v4 specific · 摘要)
- **K8**(v4 mission · binding):post-v0.2-shipped 协议层稳态化 + 治理债清理 · v0.2 已封箱 · 不引入新 idea/PRD/fork · 只收敛 5 项 backlog(R-Q6/R-Q7/contract_version/B-3/D-precedent)
- **K9**(v3 verdict 继承 · 不重审):v3 11 项 backlog 三类 3 wave 已真路径完整闭环 · 不动 v3 大架构 · v2 verdict(IDS=治理/XenoDev=唯一 L4/双向 hand-off)同样不重审
- **K10**(operator 偏好):边界先定 · 批量 SSOT · 不越界 · v4 修订 mirror 子树范围或协议字段时应延续
- **K11**(v4 收敛模式):strong-converge(对 v2/v3 强 binding · v4 同档)· 5 项 backlog 一一对一收敛 · 不允许"双方都对"压扁 · 残余降 v0.3-note 旁注

### 收敛模式
strong-converge(K11 binding · 残余分歧降 v0.3-note 旁注)

---

## Verdict rationale

为什么是 **CONCERNS** 而非 BLOCK 或 CLEAN,且 6 项分两波 2 wave:

**不是 BLOCK**:v0.2(006a-pM-v0.2)已沿真路径完整 ship — O1-O6 全 PASS、SLA
§1.3 状态 2 达成、IDS 10 commit + XenoDev 13 commit 双仓 push 完成、HANDBACK-LOG
ENTRY 18-29 batch 3 入库、12/12 6 约束 validator PASS。pipeline 当前可用,没有
阻断性缺陷(P1-GPT §2 + P3R2 §2)。

**不是 CLEAN**:v0.2 ship 过程额外暴露 3 处协议层可见债。(1) **R-Q6 验证链单向
不对称** — producer 端 `verify-ppv-p2.sh` 已实装完整 7 字段 verify + R-Q5
freshness,但 IDS consumer 链路 `validate-handback.sh` / `handback-review.md`
Step 4 仍只跑 6 约束,含 `ids_verdict_evidence` 7 字段的 hand-back 进 IDS 后无法
被验(P1-Opus §1.Y2 + P1-GPT §1.Y2)。(2) **R-Q7 REVIEW-LOG singleton** —
新一轮 codex review `cat >` 覆盖 singleton 后,老 hand-back 的 `review_log_sha256`
对不上当前文件 SHA,7 字段 immutable binding 失效(P1-Opus §1.Y2 + P1-GPT §1.Y2)。
(3) **contract_version 漂移** — v0.2 wave 2 已合 169 行协议改且 Changelog v0.2 4
entry 已写,但 frontmatter `contract_version: 2.2` / `status: v2.2` 未 bump,违反
semver 纪律(P1-Opus §1.Y6 + P1-GPT §1.Y6)。

**为什么 2.3 不是 3.0**:B-4-IDS 段在 consumer-side 默认 fallback(老 hand-back 无
`ids_verdict_evidence` 字段则跳过 7 字段 check 只跑 6 约束),不 break 旧 hand-back
→ non-BREAKING → 小版本 bump。Opus P3R1 不确定1 在此被 Codex 论证锁死("旧
hand-back 6 约束兼容读、新 7 字段 forward-only" · P1-GPT §2 row3)。

**为什么 P0 四件事必须原子**:contract bump、R-Q7 immutable path、B-4-IDS 示例
`review_log_path` 更新、R-Q6 validator 互相耦合 —— 若 contract bump 单独先 ship,
版本号已是 2.3 但 SHARED-CONTRACT 示例仍写 singleton path,就出现"版本已 bump
示例仍鼓励 singleton"的治理反债(P3R1-GPT 分歧2 + P3R2 §1/§2)。这是把"绑定"
升级为"原子波"的根因。

**为什么 D-precedent 只 codify 不回审**:K9 binding — v0.2 ship 关闭判据已达成
即 7 次 D-precedent 在路径层有效,codify normative 流程(下次同样模式怎么走)与
追认历史 7 次决议可解耦(P1-GPT §2 row5 收窄 + P3R1-Opus 不确定3 解开)。只立准入
条件 / owner / 期限 / 验证门。

## Decision matrix

| 类别 | 项 | 来源(标的现场) | 理由 | 优先级 |
|---|---|---|---|---|
| **保留** | B-3 IDS dir flock(续 v0.3-note) | XenoDev/IDS bootstrap-kit dir 锁 · v3 v0.2-note | 12 包 round-trip 0 撞库 · 触发条件(并发 hand-back 撞库)未实证 · cut 会失去未来升级路径 | P2 → note |
| **调整** | R-Q7 REVIEW-LOG path | XenoDev `.claude/skills/codex-review/REVIEW-LOG.md` singleton | 升 `real-review/<task>-round<N>-REVIEW-LOG.md` immutable per-review · 防 `cat >` 覆盖 invalidate 老 SHA | **P0** |
| **调整** | contract_version bump | `framework/SHARED-CONTRACT.md` frontmatter L3-4 | `2.2→2.3` + `status` + `last_updated` · 非 BREAKING · 旧 hand-back 6 约束兼容 · Changelog v0.2 4 entry 已等版本号 | **P0** |
| **调整** | cross_repo_split 升 SSOT | `discussion/006a-pM-v0.2/L4/HANDOFF.md` §7(per-instance 扩展) | 升 SHARED-CONTRACT **§6 normative** · 三层(spec-writer/task-decomposer/parallel-builder)已消费 · 不升下次 idea 007 重抄碎片化 | P1 |
| **删除** | (无) | — | 6 项无任何 cut · v0.2 暴露的都是协议债待清,无废弃项 | — |
| **新增** | R-Q6 consumer-side 7 字段 verify | XenoDev `lib/handback-validator/` + IDS `/handback-review` Step 4 | 抽共享 shell lib(非复制 awk)· SSOT=XenoDev `lib/handback-validator/` · IDS bootstrap-kit mirror · 补全验证链对称 | **P0** |
| **新增** | D-precedent codify | `framework/SHARED-CONTRACT.md` 新 **§8** | accept-with-followup 准入流程(owner/期限/验证门)· 只立 normative · 不回审 v0.2 七次历史(K9) | P1 |

**编号锁定**:cross_repo_split → SHARED-CONTRACT **§6** normative · D-precedent →
SHARED-CONTRACT **§8** governance(避撞 HANDOFF §7 cross_repo_split 语境 · §7 留白)。

## Refactor plan

按模块分组(3 组 · 模块来自 X 标的现有结构)。

### 模块 A · handback-validator(XenoDev `lib/handback-validator/` · SSOT)
- **当前问题**:consumer mode 只跑 6 约束(check-1~6 · path-safety + schema 层)· 7 字段 verdict-evidence 无验证 · `verify-ppv-p2.sh:231-303` 的 7 字段解析/rehash/freshness 逻辑是 producer 端独有(P1-Opus §2.A + P1-GPT §2 row1)
- **目标态**:抽 `verdict-evidence-lib.sh` 共享 shell lib · producer(`verify-ppv-p2.sh`)+ consumer(新 `validate-verdict-evidence.sh` wrapper)都 source 同一 lib · IDS bootstrap-kit mirror 同一文件(SHA dual-verify)
- **改造步骤**(顺序):
  1. 从 `verify-ppv-p2.sh:231-303` 抽 7 字段解析/rehash/freshness 函数到 `lib/handback-validator/verdict-evidence-lib.sh`
  2. `verify-ppv-p2.sh` 改为 source lib(producer 端不再自带逻辑)
  3. 新建 consumer wrapper `validate-verdict-evidence.sh`(source 同一 lib)
  4. IDS `/handback-review` Step 4 调 wrapper(consumer 链路补 7 字段)
  5. bootstrap-kit mirror 共享 lib + SHA dual-verify
- **风险**:抽 lib 时改坏 producer 端已 ship 的 PPV → 必须 producer 端回归测试(v0.2 已 PASS 的 case 重跑 · P3R2 §4 模块1 风险)
- **预估代价**:M

### 模块 B · REVIEW-LOG path(XenoDev `.claude/skills/codex-review/`)
- **当前问题**:singleton `REVIEW-LOG.md` · 新 review `cat >` 覆盖 · hand-back `review_log_sha256` 绑定失效风险(P1-Opus §2.B + P1-GPT §1.Y2)
- **目标态**:`real-review/<task>-round<N>-REVIEW-LOG.md` immutable per-review · singleton 可留 latest pointer · hand-back 绑定必须指 immutable path
- **改造步骤**(顺序):
  1. 改 codex-review writer path 范式(immutable per-review)
  2. hand-back gen 绑 immutable path(不再绑 singleton)
  3. SHARED-CONTRACT B-4-IDS 示例 `review_log_path` 同步改(与 contract bump 同 commit · 见 §next-dev-plan P0 原子波)
  4. 不 cleanup 老 immutable 文件
- **风险**:已存在的 v0.2 hand-back 绑的是 singleton path → forward-only · 老的不动 · 确认历史 hand-back 不被破坏(P3R2 §4 模块2 风险)
- **预估代价**:S

### 模块 C · SHARED-CONTRACT 治理(IDS `framework/SHARED-CONTRACT.md`)
- **当前问题**:contract_version 漂移 · cross_repo_split 无 normative · D-precedent 无流程(P1-Opus §1.Y6 三债 + P1-GPT §1.Y6)
- **目标态**:frontmatter 2.3 · §6 加 cross_repo_split normative · §8 加 D-precedent governance
- **改造步骤**(顺序):
  1. frontmatter bump 2.3 + status + last_updated(**与 P0 波同 commit** · 见 §next-dev-plan)
  2. §6 收编 HANDOFF §7 六子节为 normative(P1 波)
  3. 新 §8 写 D-precedent 准入(owner/期限/验证门 · 不回审 7 次历史 · P1 波)
  4. Changelog v0.3 entry
- **风险**:§6 收编后 HANDOFF §7 与 SHARED-CONTRACT §6 的"谁是 SSOT"要写清(HANDOFF §7 引用 §6 · 不再自带完整协议 · P3R2 §4 模块3 风险)
- **预估代价**:S(frontmatter bump)+ M(§6 收编 + §8 新写)

## Next-version dev plan

按 2 波切(milestone 级 · 不到 spec 级 · spec 是 L4 spec-writer 的工作)。

### Wave 1 · P0 原子波(预估 0.5-1 天)
- 目标:补全验证链对称 + 锁死 evidence binding immutable + 清 semver 漂移 —— **四件事同一原子 commit/wave**
- target_repo:
  - **XenoDev**:R-Q6 共享 lib + consumer validator wrapper · R-Q7 immutable writer path
  - **IDS**:SHARED-CONTRACT B-4-IDS 示例 `review_log_path` 更新 + `contract_version 2.2→2.3` + status + last_updated · bootstrap-kit mirror 共享 lib
- 关键 milestone:
  - M1: R-Q6 consumer 端能 verify producer 写的 7 字段(rehash + freshness + 父键绑定)
  - M2: R-Q7 immutable per-review path 落地 · hand-back 绑 immutable
  - M3: contract 2.3 + B-4-IDS 示例同步改(`review_log_path` 不再写 singleton)
  - M4: 四件事原子落地(一个 commit/wave · 否则"版本已 bump 示例仍鼓励 singleton"治理反债)
- 依赖:无前置(可立即起)
- 风险:抽共享 lib 改坏 producer PPV → producer 回归测试 v0.2 PASS case(模块 A 风险)

### Wave 2 · P1 波(预估 0.5 天 · 纯 IDS SHARED-CONTRACT)
- 目标:把已成熟的 per-instance 扩展 + accept-with-followup 模式升 normative
- target_repo:**IDS**(`framework/SHARED-CONTRACT.md`)
- 关键 milestone:
  - M1: §6 收编 cross_repo_split HANDOFF §7 六子节为 normative(HANDOFF §7 改引用 §6)
  - M2: 新 §8 D-precedent governance(准入条件/owner/期限/验证门 · 不回审 7 次历史)
  - M3: Changelog v0.3 entry
- 依赖:Wave 1 contract bump 已落地(版本号基线)
- 风险:§6 收编后 SSOT 归属要写清(模块 C 风险)
- **待 operator 定**:P1 波是否独立再 bump 到 2.4 — Opus P3R2 倾向 P1 波合进 2.3 同一次发布不单独 2.4(两波间隔短 · P3R2 §4 next-dev-plan)· 建议采纳该倾向,Wave 2 作为 2.3 发布内的第二个 commit,不单起 2.4

### B-3 · 不进 dev-plan
续 v0.3-note(触发条件不变 · 等真路径并发实证)。

### v0.3-note(3 条残余 · K11 残余降 note)
- **note 1 · B-3 IDS dir flock**:沿用 v3 v0.2-note · 触发条件(并发 hand-back round-trip 撞库)v0.2 12 包未触发 · 等多 worktree ship 实证再判升级 · 触发条件不变
- **note 2 · R-Q7 多 worktree 真路径压测**:immutable path 本 wave 落地是"协议先行" · 真实价值场景(async hand-back + 并发 review 覆盖)要多 worktree 模式才大规模触发 · v0.3 回头看 immutable path 是否够
- **note 3 · 共享 lib 跨仓 drift 监控**:R-Q6 共享 lib SSOT 在 XenoDev · IDS mirror · 当前靠 SHA dual-verify · 若未来 lib 频繁改需考虑自动 mirror-sync hook(现在不上 · 手动 cp + SHA 够 · 12 包实证)

---

## What this menu underweights(强制自批判)

诚实表述本 stage 文档可能 underweight 的点。这是质量栏,不能跳过。

- **Codex P3R2 未单独跑(关键局限)**:标准 forge P3R2 双侧各 finalize 一次。本
  v4 由 operator 选项 3 决定**只写 Opus 单侧 P3R2 finalize**,理由是 P3R1 后已
  **0 unresolved**(Codex 在 P3R1 逐条确认 Opus 方向且在分歧 1 主动收紧)。因此单一
  verdict 主要由 **Opus P3R2 finalize 表达、双方 P1+P3R1 全程同向背书**,而非双侧
  各自独立 finalize 后对齐。风险:若存在某个只有 Codex 会在 P3R2 提出的边界反驳,
  本文档无法捕获。缓解:P3R1-GPT §3 三条实现层立场已与 Opus 完全同向(分歧 1 Codex
  甚至比 Opus 更硬),P3R2 确认性极低 —— 但这是"推断的确认性低",非"实测的双侧
  finalize 对齐"。

- **P2 SOTA 对标轮缺席**:Z=不对标 + 无外部材料 → P2×2 跳过(同 v3)。6 项 backlog
  全是内部 lib / 内部 semver / 内部治理,无对外 SOTA 比对。风险:R-Q6 共享 lib 设计
  /R-Q7 immutable path 范式 / D-precedent §8 governance 模板若有业界更成熟做法
  (eg 现成的 evidence-binding 工具链 / 决议治理框架),本 run 不会发现。这是 Z 选择
  的已知 trade-off,operator 显式接受。

- **R-Q7 反对证据未完全消解**:Opus P1 §3 不确定2 自己提出"R-Q7 攻击场景时序条件
  较严 · 单 operator workflow 几乎不会发生"。最终 verdict 仍判 P0 现做(协议先行),
  理由是 evidence binding 可变路径已是协议层 gap、未来多 worktree 并发会真路径触发。
  但这意味着 **R-Q7 是为尚未到来的并发场景预付的工程成本** —— 已在 v0.3-note 2
  显式标记"等多 worktree 压测回头看是否够"。若多 worktree 模式迟迟不落地,R-Q7
  的 ROI 短期偏低。

- **Y 视角未含安全 / 性能**:Y = 架构 + 工程纪律 + Y6 治理债,未含安全审计与性能。
  共享 lib 抽取(模块 A)涉及跨仓 source 执行 shell lib,未从供应链安全角度审(eg
  mirror 文件被篡改的信任边界)。当前靠 SHA dual-verify 兜底,但这是数据完整性而非
  执行安全。值得 v0.3 或后续 forge 关注。

- **convergence_mode 副作用(回声室风险)**:strong-converge + 双方 P1 几乎逐条同
  决策类别(Codex "逐条接受"),意味着两模型高度共识。高共识在收敛上是优点,但也
  可能是回声室 —— 双方都没质疑的根本前提是"v0.2 ship 关闭判据达成 = 7 次 D-precedent
  在路径层有效"(K9 binding)。若该前提本身有偏(eg 某次 accept-with-followup 实际
  埋了未爆雷),D-precedent codify 会把一个不完美的模式固化成 normative §8。本 run
  按 K9 不回审历史,故无法发现此类问题。

- **X 标的覆盖**:13 引用全 reachable、跨仓读通(v3 同范式已验证),无遗漏 repo /
  文件。但 HANDBACK-LOG 657 行只 tail batch 3(~280 行),ENTRY 1-17 未重读 —— 若早期
  ENTRY 藏有与 R-Q6/R-Q7 相关的 precedent,本 run 未覆盖。判断这是低风险(batch 3
  是 R-Q6/R-Q7/D-precedent 的直接落点)。

- **forge versioning 提示**:以下新信息进入会触发 v5 跑并可能改变 verdict —— (1)
  多 worktree 并发 ship 真路径上线后,B-3 dir flock 撞库 / R-Q7 immutable path 实测
  数据(可能推翻"协议先行够用"或"B-3 续 note");(2) 共享 lib 跨仓 drift 实际发生
  (可能触发 mirror-sync hook 从 note 升主线);(3) idea 007 启动且复用 cross_repo_split
  (验证 §6 normative 是否真的免去重抄)。

## Decision menu(for human)

### [A] 接受 verdict 进 L4(本 verdict 不产 PRD · 此选项受限)
```
⚠ 本 v4 W 不含 next-PRD(K8:v4 不引入新 idea/新 PRD/新 fork) ——
   §"W-shape 章节" 无 §"Next-version PRD draft",故 [A] 标准路径(fork PRD branch
   → /plan-start)在本 v4 不直接适用。

v4 verdict 是"对现有协议层的 2 wave 清理草案",不是新产品 PRD。落地路径是:
   1. 直接按 §"Refactor plan"(3 模块)+ §"Next-version dev plan"(2 波)执行,
      改 XenoDev + IDS 现有协议/lib/脚本 —— 这是工程改动,非新 PRD/新 fork
   2. P0 原子波四件事同 commit;P1 波纯 IDS SHARED-CONTRACT
   3. 改动归 v0.3(SHARED-CONTRACT contract_version 2.3)

若 operator 希望把 v0.3 清理也走正式 L4 plan-start 流程,选 [B] 起 v5 加
next-dev-plan 细化到 spec 级,或直接由 operator 手工驱动 2 wave(改动面小 · 6 项
中 4 项单仓小改)。
```

### [B] 跑 forge v5(说明需要补什么)
```
/expert-forge 006
# 在 Phase 0 intake 时调整 X / Y / Z / W / K
# 旧 v4 整目录保留作历史参考
```
适用:
- 多 worktree 并发真路径上线后,需重判 B-3 dir flock / R-Q7 immutable path ROI(见 v0.3-note 1/2)
- idea 007 启动需验证 cross_repo_split §6 normative 是否免重抄
- 想补 P2 SOTA 对标(eg evidence-binding 工具链 / 决议治理框架业界做法)→ 改 Z=对标
- 想补 Codex P3R2 双侧 finalize(若 operator 对单侧 finalize 不放心)

### [C] 局部接受
- ✅ 采纳(强收敛 · 0 unresolved · 建议全收):
  - P0 原子波四件事(R-Q6 共享 lib + R-Q7 immutable path + B-4 示例 + contract 2.3)
  - P1 波(D-precedent §8 + cross_repo_split §6 normative)
  - B-3 续 v0.3-note
- ⏸ 可挂起(若 ROI 存疑 · 等条件):
  - R-Q7 immutable path —— 若多 worktree 模式短期不上线,可降 P1 等并发实证(见 underweights · 但会破坏 P0 原子波,需重新评估示例/contract 绑定)
  - P1 波 cross_repo_split §6 升 normative —— 若 idea 007 不确定启动,可挂起到 007 立项时再升
- ❌ 拒绝:无(6 项 0 cut)

### [P] Park
```
/park 006
```
保留所有 forge v4 产物,标记暂停。复活时不重做本层。适用:v0.2 已封箱,operator
暂无精力起 v0.3 协议清理 —— 6 项 backlog 已锁定决策,随时可复活直接执行。

### [Z] Abandon
```
/abandon 006
```
v4 verdict 不支持 abandon —— 6 项都是 v0.2 ship 已暴露的真实协议债,清理有明确
价值。仅在 operator 决定整个 006 idea 线停止时才用。

---

## Forge log
(由 /expert-forge 命令更新;记录每次 forge run 的 v 序列 + 关键 verdict 一句话)

- v4: 2026-05-31 — verdict: "不动 v3 11 项大架构,2 wave 清理 6 项 post-v0.2 协议债;P0 原子波(R-Q6 共享 lib + R-Q7 immutable path + B-4 示例 + contract 2.3)+ P1 波(D-precedent §8 + cross_repo_split §6);B-3 续 v0.3-note;0 unresolved。"
- v3: 2026-05-27 — verdict: "v0.2 = 11 项 backlog 三类 batch ship · 3 wave 顺序 · 每 wave 1 IDS commit + MANIFEST-v0.2.md append。"
