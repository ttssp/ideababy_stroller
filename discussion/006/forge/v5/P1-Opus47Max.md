---
doc_type: forge-P1
forge_id: 006
forge_version: v5
side: Opus47Max
phase: 1
created: 2026-05-31T23:20:00Z
y_perspectives: [并发安全, 架构设计, 工程纪律+跨仓一致性]
convergence_mode: strong-converge
---

# Forge v5 · P1 · Opus 独立审阅(并发安全加固)

## §0 我读到的标的清单 + 阅读策略 + K 摘要

**K 摘要**:operator 决定上**多 worktree 并发构建**,触发 v4 故意推迟的 6 项并发 backlog。判准核心 = 「**可靠优先但不过度工程**」—— 单 operator 多 worktree(同机/少数机器),宁可保守真锁也不要乐观偶发撞库,但**不需要** etcd 级分布式协调,轻量正确(flock/O_EXCL/单调 id)优先(K8/K12)。v4 的 P0 决议不重审(K9),只在这 6 项收敛 verdict + 改造方案(K11 strong-converge)。

**12 标的全部本地可达**(✅×12 · 含 XenoDev 仓 `/Users/admin/codes/XenoDev/` 跨仓可读)。按 Y 主轴(并发安全)的阅读策略:优先读**真代码现场**而非协议文字 —— 因为并发 bug 藏在实装的时序里,不在 normative 描述里。重点读了 4 处真代码:
- `verify-ppv-p2.sh`(Step 0 rebind + Step 5 freshness 600s 窗 · G1 已修/G3 现场)
- `verdict-evidence-lib.sh`(consumer shallow vs producer full 的 mode 分叉 · resolve_review_log_path allowlist · G1/G2 根)
- `codex-review/SKILL.md §3.6.2`(immutable writer + noclobber · R-Q7-stress 现场)
- `parallel-builder SKILL §6` + `SHARED-CONTRACT B-1`(`ln $DRAFT $TGT` atomic + EEXIST 撞库重 gen TS · B-3 现场)

**关键实证基线(影响所有 verdict 的可信度)**:`XenoDev/.claude/skills/codex-review/real-review/` **目录尚不存在**;singleton REVIEW-LOG.md 是 2026-05-29 旧版。即 **R-Q7 immutable 范式自 P0 落地以来从未真实执行过一次** —— 全部是「协议先行」的纸面代码。这一点对 5 号 backlog(R-Q7-immutable-stress)是决定性的:它不是「压测一个已运行系统」,而是「一个零运行证据的范式」。

## §1 现状摘要(按 Y 视角组织)

### Y1 · 并发安全(v5 主轴)

读真代码后,6 项 backlog 的并发暴露面**不是均质的**,可分三类:

**A 类 · 真并发竞争(写竞争 · 跨 worker)**:只有 **B-3 dir-flock** 一项是真正的多进程写同一资源。`parallel-builder` 把 hand-back publish 到 IDS 共享 dir `discussion/006/handback/`,靠 `ln $DRAFT $TGT` 的 atomic 性 + EEXIST 撞库 hard-fail + caller 重 gen TS(SHARED-CONTRACT B-1 line 837/849)。`ln` syscall 本身**无 TOCTOU**(原子创建),所以这不是经典 race —— 但**文件名含秒级 TS**,同秒同 TID 两 worker 撞库后「重 gen TS」可能再撞同秒。当前唯一缓解是「11 round-trip 0 撞库」的经验值,**零并发实证**。

**B 类 · 时序/重放语义洞(单写 · 但语义可被并发利用)**:**G3-replay-window**。`verify_evidence_freshness`(lib line 330-352)只查「hand-back created ≥ REVIEW-LOG ts 且 diff ≤ 600s」,**不查「绑的 log 是否 == 当前 latest」**。codex 轮 3 H1 给的精确场景:10:00 A=approve,10:05 B=needs-attention,10:06 hand-back 绑 A(仍在 600s 窗内)→ gate 跟 A 忽略 B。并发下「另一 worker 捡回旧 approve」从理论变现实。这是 **R-Q7「策略 A 两者并存」的直接后果**(故意允许绑任意 immutable 记录)。

**C 类 · 跨仓信任不对称(非并发 · 但并发放大)**:**G1-consumer-binding** + **G2-singleton-audit** + **shared-lib-drift**。本质是 producer(XenoDev)能验真假、consumer(IDS)只能验语法(lib line 22-26 + 169 的 mode 分叉)。SHARED-CONTRACT line 940-941 normative 说「consumer 要验可达+rehash」,但 IDS 本地无 XenoDev REVIEW-LOG,字面实装 100% 误拒 —— **contract 内部矛盾**(handoff §2 已签字 known-gap)。并发多 worker 互传证据时,「伪造/stale 的 review_log_path/sha256 无人拦」从单点变多点。

### Y2 · 架构设计

并发加固的**协议层归属**是核心架构问题。当前 SHARED-CONTRACT line 940-941 把「可达+rehash」写成无条件 normative,但实装把它降级为 producer-only —— **契约与实装语义分叉**。这不是 bug,是 contract 缺少「producer-full vs consumer-shallow」的**显式分层建模**。G1 的真修法不是「让 consumer 也能 rehash」(跨仓不可达),而是**在协议层把验证深度建模成 producer/consumer 两个 profile**,各自 normative 自洽。`resolve_review_log_path` 的 allowlist(lib line 223-250)是好的 trust-boundary 雏形,但只防路径遍历,不防「合法路径但 stale binding」。

### Y3 · 工程纪律 + 跨仓一致性

**shared-lib-drift**:R-Q6 共享 lib SSOT 在 XenoDev,IDS mirror,靠 SHA dual-verify + `test-verdict-evidence-mirror-sha.sh` 手动守护。多 worktree 各自 mirror → drift 面上升。当前守护是「测试存在但需手动跑」,无 CI gate。另外,**真代码注释被「真路径...真路径」乱码严重污染**(verify-ppv-p2.sh line 152-157 / codex-review SKILL §3.6.3-3.6.4 / parallel-builder §3.1 几乎每条注释)—— 这是 Y3 的工程纪律硬伤,但 K10 划在「不越界清理」内,v5 不应顺手改(留作独立工程债条目标注)。

## §2 First-take 评分(按 6 项 backlog · keep/refactor/cut/new)

| backlog | first-take | 优先级直觉 | 理由 |
|---|---|---|---|
| **B-3-dir-flock** | **refactor → new(轻量真锁)** | **P0 ship-blocker** | 唯一真写竞争 · 并发正主 · 当前 EEXIST+重 gen TS 在同秒撞库下不收敛 · K8「可靠优先」要求真锁(O_EXCL/flock 轻量)· **上并发前必补** |
| **G3-replay-window** | **refactor(收紧绑定)** | **P0/P1 边界** | 语义洞已被 codex H1 证 · 修法明确(校验 bound log == latest 或单调 id)· 改动小但改「策略 A」已批准设计 · 需 forge 拍板是否扩 scope |
| **G1-consumer-binding** | **new(协议分层建模)** | **P1** | 非并发引爆但并发放大 · 真修法是协议层 producer/consumer profile 显式建模 · 非 P0(consumer 已标 syntax-only precheck 防误用) |
| **G2-singleton-audit** | **refactor(强制 immutable)** | **P1**(与 G3 同根) | 「强制 immutable + 拒 singleton」改「策略 A 两者并存」· G1 修复后 audit 弱点仅存「刻意绑 singleton」· 与 G3 合并处置最自然 |
| **R-Q7-immutable-stress** | **keep + 补实证** | **P1** | **零运行证据**(real-review/ 目录都不存在)· 不是压测已运行系统而是验范式 · 修 B-3 时顺带产首次真路径运行证据 |
| **shared-lib-drift** | **refactor(CI gate 化)** | **P2** | 当前手动 SHA 守护 · 并发下 mirror 面扩 · 升级路径 = CI gate / pre-commit hook · 非 ship-blocker |

## §3 我现在最不确定的 3 件事

1. **B-3 该用哪级锁,K8「不过度工程」的边界在哪**:`flock(2)` 文件锁 vs `O_EXCL` atomic create vs 仅修「重 gen TS 用单调 nonce 而非秒级 TS」。三者复杂度递增。我倾向最轻(单调 nonce 去掉同秒碰撞根因),但不确定 BSD/Linux flock 的跨平台坑是否值得为「正确性兜底」付出 —— 这要 Phase 2 对标 SOTA 的 lockfile 反模式才能定。

2. **G3/G2 是否该合并扩进 P0**:它们改「策略 A 两者并存」(brief 已批准)。收紧成「只绑 latest/单调 id」逻辑上更安全,但 v4 brief 故意选了「两者并存」。这是「推翻已批准设计 vs 上并发前堵洞」的张力 —— strong-converge 下必须给单一 verdict,但我不确定 operator 愿不愿在 v5 重开 v4 已拍的设计。

3. **R-Q7 零运行证据是否动摇整个 evidence binding 链的可信度**:real-review/ 从未生成过。如果 immutable writer 的 noclobber 逻辑(SKILL line 309-315)在并发同秒下的真实行为与纸面不符,那 G1 的 Step 0 rebind「绑 immutable log」的前提就不稳。我不确定该把「先产真运行证据」作为所有 P0/P1 修复的**前置 gate**,还是并行做。
