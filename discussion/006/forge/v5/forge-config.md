---
doc_type: forge-config
forge_id: 006
forge_version: v5
created: 2026-05-31T23:04:00Z
prefill_source: manual(并发 backlog 来自 v4 known-gap + handoff §4.5 + 项目记忆 · operator 决定上多 worktree 并发)
convergence_mode: strong-converge
x_count: 12
x_hash: 9c5e79e910cd4fd80633c6ca739d552e
y_count: 3
w_count: 4
z_mode: 对标 SOTA · 并发安全(Phase 2 跑搜索)
k_provenance: verbatim 核心诉求 + K9/K10/K11 verbatim + v5 K8 替换 + K12 新增(对标 SOTA 判准)
v5_mission: 多 worktree 并发上线前 · 并发安全加固 + evidence binding 时序闭合
inheritance: v4 verdict 不重审(6 项 backlog C 全收 · P0 原子波已 ship · contract 2.3)
---

# Forge config · idea 006 · v5

## 背景:为什么起 v5

v4 verdict(post-v0.2 协议稳态化 · 6 项 backlog)已 operator C 全收 + P0 原子波双仓 ship(IDS commit `cc7e799` + XenoDev commit `223ff46` · contract 2.2→2.3)。但 v4 **有意推迟**了一批"等并发实战再判"的 backlog —— operator 现在决定**上多 worktree 并发构建**,这批 backlog 的触发条件即将到来,必须先审。

**v5 触发**:operator 计划多 worktree 并发(2026-05-31)。并发是以下所有 backlog 的真实引爆场景:单 operator 顺序构建触发不了,并发一上全部 reachable。

**v5 审的 6 项并发 backlog**(来源:v4 known-gap + XenoDev handoff §4.5 + 项目记忆 [[project-forge-v5-trigger]]):

1. **G1-consumer-binding** · consumer shallow 验不了 evidence binding · 并发 worker 互传证据 · 伪造/stale 的 review_log_path/sha256 无人拦(SHARED-CONTRACT line 940-941 normative 说要验但 consumer 实装不了 → contract 内部矛盾)
2. **G2-singleton-audit** · 绑 singleton REVIEW-LOG 的 hand-back 下次 review 覆盖后无法复证 · 多 worker 同时审更易触发
3. **G3-replay-window** · R-Q7「策略 A 两者并存」允许绑任意 immutable 记录 · 后续出阻断 review 后旧 approve 仍能在 600s freshness 窗内被绑过 gate(并发下另一 worker 真能捡回旧 approve)
4. **B-3-dir-flock** · 多 producer 并发写 IDS `discussion/<id>/handback/` dir 撞库 · v3 起挂 v0.x-note · **并发是它的正主**(12 包顺序 round-trip 0 撞库 · 但并发未实证)· 当前靠 `ln $DRAFT $TGT` atomic + sha 复验 fail-closed
5. **R-Q7-immutable-stress** · immutable per-review path 在并发多 worker 下的真路径压测 · v4 落地是「协议先行」· 并发才是真实价值场景
6. **shared-lib-drift** · R-Q6 共享 lib SSOT 在 XenoDev · IDS mirror · 多 worktree 各自 mirror · drift 风险上升 · 当前靠 SHA dual-verify + test-verdict-evidence-mirror-sha.sh 手动守护

## X · 审阅标的(12 引用 · 并发安全现场)

### 槽位 1 · v4 verdict baseline(继承 · 不重审)
- `discussion/006/forge/v4/stage-forge-006-v4.md`(v4 verdict · 6 项 backlog C 全收 · §underweights 列了并发 backlog · 整文件)

### 槽位 2 · XenoDev → IDS 交接(并发 backlog 源头 · 最重点)
- `/Users/admin/codes/XenoDev/.work/IDS-handoff-006-forge-v4-P0.md`(§4.5 = 4 轮 codex adversarial-review F1/F2/G1/G2/H1/H2 + 3 处同根缺口 backlog 条目 · §2 known-gap · §4 R-Q7 策略 A · **整文件必读**)

### 槽位 3 · 协议层(并发安全条款现状)
- `framework/SHARED-CONTRACT.md`(§6 B-4-IDS line 867-987 · **重点** line 940-941 producer-side 校验 + known-gap 注记 + B-3 v0.x-note changelog 段 + B-1 publish atomic 段 · v2.3 现行)

### 槽位 4-5 · R-Q6 共享 lib + consumer 实装(evidence binding 现场)
- `/Users/admin/codes/XenoDev/lib/handback-validator/verdict-evidence-lib.sh`(producer full / consumer shallow 双 mode · resolve_review_log_path allowlist trust-boundary · 整文件)
- `/Users/admin/codes/XenoDev/lib/handback-validator/validate-verdict-evidence.sh`(consumer shallow wrapper · syntax-only precheck 三重标注 · 整文件)

### 槽位 6 · R-Q7 immutable path + replay 现场
- `/Users/admin/codes/XenoDev/scripts/verify-ppv-p2.sh`(Step 0 rebind 解 hand-back 绑定 review_log_path + Step 5 freshness 600s 窗 · **重点** G1 修复 + H1 replay 窗口)

### 槽位 7 · R-Q7 writer + dir 写竞争现场
- `/Users/admin/codes/XenoDev/.claude/skills/codex-review/SKILL.md`(§3.6.2 immutable real-review/ writer + noclobber + singleton latest-pointer · §3.6.4 anti-pattern)

### 槽位 8 · B-3 dir flock 现场(并发写 dir)
- `framework/SHARED-CONTRACT.md` §6 B-1 publish 段(`ln $DRAFT $TGT` atomic + EXDEV fallback · 当前并发安全假设) — 已在槽位 3 · 此处标重点子段
- `/Users/admin/codes/XenoDev/.claude/skills/parallel-builder/SKILL.md`(§3.1 ids_verdict_evidence inject + publish hand-back 到 IDS dir · 并发多 worker 写同 dir 的真路径)

### 槽位 9 · mirror drift 守护现场
- `framework/xenodev-bootstrap-kit/tests/integration/test-verdict-evidence-mirror-sha.sh`(IDS 侧 SHA dual-verify 守护 · shared-lib-drift backlog 现场)
- `framework/xenodev-bootstrap-kit/MANIFEST-v0.2.md` §wave-4(mirror provenance audit · 整 §wave-4 段)

### 槽位 10 · consumer 入口(并发下 consumer 验证路径)
- `.claude/commands/handback-review.md`(Step 4 verdict-evidence shallow precheck · 并发下多包 consumer 验证)

### 槽位 11 · 项目记忆(并发 backlog 全清单)
- `/Users/admin/.claude/projects/-Users-admin-codes-ideababy-stroller/memory/project_forge_v5_trigger.md`(6 项并发 backlog 全清单 + 为什么推迟 + 触发时机)

### 槽位 12 · v3 B-3 原始决议(dir flock 触发条件 + 升级路径)
- `discussion/006/forge/v3/stage-forge-006-v3.md` §W3 模块 B(B-3 v0.2-note 原始触发条件 + 升 P1 路径 · 不重审 v3 verdict · 只读 B-3 触发条件定义)

## Y · 审阅视角(3)

- **Y1 并发安全**(v5 核心 · 新)— race condition / TOCTOU / atomic 写 / dir 锁 / evidence binding 时序 / replay 防护 / 单调时钟 · 这是 v5 主轴
- **Y2 架构设计**(prefill · 同 v2/v3/v4)— 并发加固的协议层归属(SHARED-CONTRACT normative vs 实装)· producer/consumer 职责
- **Y3 工程纪律 + 跨仓一致性**(prefill · 同 v4 Y6 演化)— 并发下 mirror drift 守护 · 共享 lib SSOT · 多 worktree 协调纪律

## Z · 参照系

**模式**:对标 SOTA · 并发安全

理由:并发安全是**有成熟业界做法的领域**(与 v3/v4 纯内部治理不同)· 6 项 backlog 多数有 prior-art 可比对:
- B-3 dir flock → `flock(2)` / `fcntl` advisory lock / `O_EXCL` atomic create / lockfile 模式(BSD vs Linux 差异)
- G1/G3 evidence binding + replay → CAS(compare-and-swap)/ 单调 review id / nonce / 时钟防重放 / TUF-style 签名时效
- G2 singleton audit → append-only log / content-addressed storage / immutable ledger 模式
- 多 worker 协调 → 分布式锁(etcd/redlock 模式)/ optimistic concurrency / WAL
- mirror drift → checksum manifest / signed mirror / git-based provenance

**Phase 2 跑搜索**:双方各检索并发安全 SOTA + prior-art + 失败案例(eg 著名 race condition CVE / lockfile 反模式)· 比对 6 项 backlog 的当前做法。**不搜** pricing / tech-stack-deep-dive / 实施细节(per PROTOCOL §"P2 forbidden")。

## W · 产出形态(4)

- verdict-only(单 verdict + ≤500 字 rationale · 并发安全总判)
- decision-list(6 项并发 backlog 一一对一:G1/G2/G3/B-3/R-Q7-stress/shared-lib-drift · 每项 keep/refactor/cut/new + P0/P1/P2 + SOTA 对标结论)
- refactor-plan(按模块 + 优先级 + 估时 · 标 SOTA 借鉴了什么)
- next-dev-plan(估时 + 改哪个仓 + target_repo + 上并发前哪些是 ship-blocker)

**不要 next-PRD**(v5 不引入新 idea / 新 PRD · 同 v4)
**不要 free-essay**(decision-list + refactor-plan 已足)

## K · 用户判准(verbatim 核心诉求 + K9/K10/K11 verbatim + v5 K8 替换 + K12 新增)

```
// from "想法"(verbatim · 一脉相承):
给定一个PRD,claude code可以几乎没有人工干预的情况下自主完成开发任务。
我需要一个**可靠的、自动化程度最高**解决方案。

// from "我为什么想做这个"(verbatim):
我是非软件开发背景。我可以将需求描述清楚,我也可以尝试构建较可靠的PRD。
但是我缺少软件开发的经验,对各个规模(大中小型)的开发的方案、流程、规范等内容都没有把握。

// from "我诉求"(verbatim):
希望双方凭借最强的 AI 专业能力以及最丰富的软件开发经验,通过调研、论证、思辨、构思、设计、整理归纳等方式,达成一套基于 Claude Code 实现**可靠**自动化开发的 framework/pipeline 的共识方案

// === v5 specific additions(operator append 2026-05-31 · 决定上多 worktree 并发)===

K8(v5 mission · binding · 替换 v4 K8):v5 mission = "多 worktree 并发上线前 · 并发安全加固 + evidence binding 时序闭合"。
operator 决定上多 worktree 并发构建 · 触发 v4 推迟的 6 项并发 backlog(G1 consumer-binding / G2 singleton-audit / G3 replay-window / B-3 dir-flock / R-Q7-immutable-stress / shared-lib-drift)。
v5 不引入新 idea / 新 PRD / 新 fork,只在这 6 项并发 backlog 上收敛 verdict + 改造方案 · 目标:并发上线前把 ship-blocker 级的并发安全洞补掉。
operator 是非软件背景 → 并发安全方案必须「可靠优先」· 宁可保守(eg 真锁)也不要「乐观但偶发撞库」· 但也不要过度工程(eg 单 operator 几台机器不需要 etcd 级分布式协调)。

K9(v4 verdict 继承 · 不重审):v4 已收敛"6 项 backlog C 全收 · P0 原子波 ship · contract 2.3"。
v5 不重审 v4 的 P0 决议(R-Q6 共享 lib / R-Q7 immutable 范式 / contract bump / D-precedent / cross_repo_split 升 §6)· 也不重审 v3(11 项 backlog)/ v2(IDS=治理 / XenoDev=唯一 L4)。
v5 只动 v4 明确推迟到「并发实战再判」的 6 项 backlog。

K10(operator 偏好 · verbatim 不动):边界先定、批量 SSOT、不越界 · v5 并发加固若动 mirror 子树 / 协议字段应延续。

K11(收敛模式偏好 · verbatim 不动):strong-converge(operator 对 v2/v3/v4 强 binding;v5 同档)— 6 项并发 backlog 一一对一收敛产 verdict · 不允许"双方都对"压扁 · 残余分歧用 v0.4-note 旁注。

K12(v5 新增 · 对标 SOTA 判准):Z=对标 SOTA。并发安全有成熟业界做法 · 双方 Phase 2 必须比对 prior-art(flock/CAS/nonce/append-only ledger/分布式锁)· 每项 backlog 的 verdict 要说清「SOTA 怎么做 · 我们当前做法的 gap · 借鉴还是不适用」。但 SOTA 借鉴要过 K8「可靠优先但不过度工程」滤网 — 单 operator 多 worktree(同机/少数机器)不需要重量级分布式协调 · 轻量正确(flock/O_EXCL/单调 id)优先。
```

## 收敛模式

strong-converge(K11 binding · 与 v2/v3/v4 同档 · 残余分歧降 v0.4-note 旁注)
