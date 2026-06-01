# Forge Stage · 006 · v5 · "多 worktree 并发上线前 · 并发安全加固 + evidence binding 时序闭合"

**Generated**: 2026-06-01T08:30:00Z
**Source**: forge run v5 with X = 12 标的, Y = [并发安全, 架构设计, 工程纪律+跨仓一致性], Z = 对标 SOTA·并发安全, W = [verdict-only, decision-list, refactor-plan, next-dev-plan]
**Convergence mode**: strong-converge
**Rounds completed**: P1 (both), P2 (both), P3R1 (both), P3R2 (both)
**Searches run**: 12 across 多个 SOTA 源(Opus 4 组 / GPT 8 组 · O_EXCL/flock man-pages、SLSA VSA、in-toto、TUF rollback-freeze、S3 Object-Lock WORM、Git content-addressed objects、git-verify-commit provenance)
**Moderator injections honored**: none(moderator-notes.md 不存在)
**Convergence outcome**: converged(单一 verdict · 零 unresolved · 6 项 backlog 档位双方逐字一致)

---

## How to read this

forge 是横切层(不是 L1-L4 pipeline 的一部分)。本文档是双专家(Opus 4.7 Max / GPT-5.5x High)审阅
12 个并发安全现场标的 + 对标并发安全 SOTA + 联合两轮收敛后的产出,**强制给出单一立场**
(strong-converge · K11 binding · 不是候选菜单 defer 给你拍板)。

读完后你应该:
- 知道双专家对「多 worktree 并发能不能上、上之前要补什么」的最终 verdict(§"Verdict")
- 知道支持每条结论的具体证据(§"Evidence map" 可逐条溯源到某轮某段)
- 拿到按 W 形态准备好的可执行草案(6 项决议清单 / 3 模块重构方案 / 2 milestone 开发计划)
- 能基于 §"Decision menu" 直接进入下一步(批准进 plan / 跑 v6 / 局部接受 / park / abandon)
- **注意一个必须你亲自拍板的 K9 决断点**(§"Decision menu" [K9] · 双方都坚持单列)

---

## Verdict

**v5 verdict = CONCERNS(可上并发,但有 3 个 P0 ship-blocker 必须先补)。**

并发可上,但先过 P0 三门:**① 堵 G3 replay**(600s freshness 必须加「bound log == 当前 latest」
或单调 review id 校验)、**② 产 R-Q7 首次真实运行证据**(`real-review/` 目录至今为空 · immutable
范式零运行证据 · 这一步顺带验 B-3 不撞库)、**③ shared-lib mirror-sha preflight**(每批并发启动前强制跑)。

**G1 / G2 / B-3 作为 P1 轻量改造**:G1 做 VSA-like 摘要(同机同信任域 P1,跨机器/跨信任域升 P0);
G2 ship evidence 强制 immutable;B-3 并入 R-Q7 唯一化 basename(不上 flock)。

6 项 backlog 全部 refactor/new(无一 cut),经 SOTA 对标 + K8 滤网全部收敛为轻量正确层 —— 重量级方案
(etcd/Redlock、完整 DSSE/in-toto 签名链、云 WORM、hash-chain ledger)双方独立判定为对单 operator
多 worktree **过度工程**,全部滤掉(直接服务 K8「可靠优先但不过度工程」)。

**⚠ 这个 verdict 含一个需你亲自确认的收紧动作**:G2/G3 会收紧 v4 已批准的「R-Q7 策略 A 两者并存」。
见 §"Decision menu" [K9]。

## Evidence map

| 结论 | 来源 | 引用(≤15 words) | 是否有反对证据 |
|---|---|---|---|
| consumer 仅 syntax-only · producer 已强 | P1-Opus §1 / P1-GPT §1 | "consumer 有语法闸 + producer 自证" | - 双方独立核查一致 |
| `real-review/` 目录不存在 · R-Q7 零运行证据 | P1-Opus §0 / P1-GPT §0 | "immutable 范式自 P0 落地从未真实执行" | - 双方独立核查一致 |
| G3 = 教科书级 missing-freshness 反模式 | P2-Opus §1 / P2-GPT §1 | "timestamp 窗 ≠ 防重放(TUF rollback/freeze)" | - SOTA 双方一致 |
| G3 → P0 · 借 TUF 单调性 | P3R2-Opus §2 / P3R2-GPT §2 | "加 latest equality 或单调 review id" | - |
| R-Q7 → P0(new · 产运行证据) | P3R2-Opus §2 / P3R2-GPT §2 | "零运行证据不能上并发" | - |
| shared-lib → P0 preflight gate | P3R1-Opus §3 / P3R2-GPT §2 | "每批并发启动前强制跑 mirror-sha gate" | ⚠ P1-Opus 初判 P2,P2/R1 让步到 P0(见 underweights) |
| G1 → P1 default + 拓扑升 P0 | P3R2-Opus §1 / P3R2-GPT §1 | "跨机器/跨信任域并发再升 P0" | ⚠ P1-GPT 初判 P0,R1/R2 收敛 P1(见 underweights) |
| G1 修法 = SLSA VSA 轻量摘要 | P2-Opus §1 / P2-GPT §1 | "consumer 验摘要而非重跑 XenoDev 私有路径" | - SOTA 双方一致 |
| G2 → P1 · ship 强制 immutable | P3R2-Opus §2 / P3R2-GPT §2 | "singleton 仅作人读 latest-pointer(WORM invariant)" | - |
| B-3 → P1 · 唯一化 basename · 不上 flock | P2-Opus §3 / P2-GPT §3 | "flock 跨平台坑(NFS/SMB 语义变)" | ⚠ P1-Opus 初判 P0,R1/R2 合并入 R-Q7 P1(见 underweights) |
| K8 滤掉 etcd/DSSE/云WORM/ledger | P2-Opus §2 / P2-GPT §2 | "对单 operator 多 worktree 全是过度工程" | - 双方独立达成 |
| G2/G3 收紧 v4 策略 A · 需 operator 确认 | P3R1-Opus §4 / P3R1-GPT §4 | "不是重审 v4 P0,是 v5 并发触发后收紧" | - 双方独立标到同一红线 |

(所有 ⚠ 行的反对证据均为「收敛前的优先级分歧」,经 P3R1/P3R2 显式收敛,非未解决冲突 · 详见 §underweights)

## Intake recap

### X · 审阅标的(12 个)
- 槽位 1 · v4 verdict baseline(继承不重审)— stage 文档
- 槽位 2 · XenoDev → IDS 交接 §4.5(并发 backlog 源头)— handoff 文档
- 槽位 3 · 协议层 SHARED-CONTRACT §6 B-4-IDS(line 940-941 producer 校验 + known-gap)— 协议
- 槽位 4-5 · R-Q6 共享 lib + consumer 实装(verdict-evidence-lib.sh / validate-verdict-evidence.sh)— 真代码
- 槽位 6 · R-Q7 immutable path + replay(verify-ppv-p2.sh Step 0 rebind + Step 5 freshness)— 真代码
- 槽位 7 · R-Q7 writer(codex-review SKILL §3.6.2 immutable writer + noclobber)— 真代码
- 槽位 8 · B-3 dir flock(SHARED-CONTRACT B-1 publish + parallel-builder SKILL §3.1)— 协议+真代码
- 槽位 9 · mirror drift 守护(test-verdict-evidence-mirror-sha.sh + MANIFEST §wave-4)— 测试+清单
- 槽位 10 · consumer 入口(handback-review.md Step 4 shallow precheck)— 命令
- 槽位 11 · 项目记忆(6 项并发 backlog 全清单)— memory
- 槽位 12 · v3 B-3 原始决议(触发条件 + 升级路径 · 不重审)— stage 文档

### Y · 审阅视角
- **Y1 并发安全**(v5 核心)— race / TOCTOU / atomic 写 / dir 锁 / evidence binding 时序 / replay 防护 / 单调时钟
- **Y2 架构设计**— 并发加固的协议层归属(normative vs 实装)· producer/consumer 职责
- **Y3 工程纪律 + 跨仓一致性**— 并发下 mirror drift 守护 · 共享 lib SSOT · 多 worktree 协调纪律

### Z · 参照系
- mode: 对标 SOTA · 并发安全(Phase 2 跑搜索)
- 用户外部材料: 无(K 无外部链接/文件 · 仅 K8/K12 滤网)

### W · 产出形态
- verdict-only(单 verdict + rationale)
- decision-list(6 项 backlog 一一对一 · keep/refactor/cut/new + 档位 + SOTA 对标)
- refactor-plan(按模块 + 优先级 + 估时 + SOTA 借鉴)
- next-dev-plan(估时 + 改哪个仓 + target_repo + ship-blocker 标注)
- **不含** next-PRD / free-essay(operator 明确排除)

### K · 用户判准(摘自 forge-config.K)
- 核心诉求(verbatim · 一脉相承):"给定一个 PRD,claude code 可以几乎没有人工干预地自主完成开发任务 · 可靠的、自动化程度最高的解决方案"
- K8(v5 mission · binding):多 worktree 并发上线前 · 并发安全加固 + evidence binding 时序闭合 · 只收敛 6 项并发 backlog · 可靠优先但不过度工程(单 operator 少数机器不上 etcd 级分布式协调)
- K9(v4 verdict 继承 · 不重审):只动 v4 明确推迟到「并发实战再判」的 6 项 backlog
- K10(operator 偏好):边界先定、批量 SSOT、不越界
- K11(收敛模式):strong-converge · 6 项一一对一 · 残余分歧降 v0.4-note
- K12(对标 SOTA):每项 backlog 说清 SOTA 怎么做 / 当前 gap / 借鉴还是不适用 · 过 K8「轻量正确」滤网

### 收敛模式
strong-converge(K11 binding · 与 v2/v3/v4 同档 · 残余分歧降 v0.4-note 旁注 · 本次双方完全 converged 零 unresolved)

---

## §"Verdict rationale"(W: verdict-only)

verdict 落 CONCERNS 而非 PASS 或 BLOCK,论证如下:

**为什么不是 PASS**:三处真洞在并发下从理论变现实。① G3 是 SOTA 教科书级反模式 ——
`verify_evidence_freshness` 只查「不太旧」(diff ≤ 600s),不查「仍是当前有效 review」,codex 轮 3 H1
给的精确场景(10:00 approve → 10:05 needs-attention → 10:06 绑旧 approve 仍在窗内过 gate)在并发下
「另一 worker 捡回旧 approve」直接成立(P2-Opus §1 / P2-GPT §1 · TUF rollback/freeze 对标)。
② R-Q7 immutable 范式从 P0 落地至今**零运行证据**(`real-review/` 目录不存在 · 双方独立核查),
让一个从未真实执行的范式在并发下首跑是不可接受的风险。③ mirror drift 守护当前需手动触发,
多 worktree 各携不同时间点 mirror 时无 gate 拦截。

**为什么不是 BLOCK**:这三处都有**轻量正确**的明确修法,且 producer 侧已比 v4 初态强很多
(Step 0 rebind + allowlist + rehash + 一致性校验)。补完 P0 三门即可安全并发,不需要推倒重来。

**为什么全程轻量**:K8/K12 滤网双方独立达成共识 —— 单 operator 多 worktree(同机/少数机器)
不需要 etcd/Redlock 分布式锁、完整 in-toto DSSE 签名链、云 WORM 存储、hash-chain ledger。这些不是
不好,是「过度工程」违 K8,反而会伤害「自动化程度最高」。留下的全是轻量层:O_EXCL/唯一化、
单调 id/latest equality、VSA-like 摘要、WORM invariant、preflight gate。

**直接回应 K**:并发安全加固服务「可靠」;B-3 唯一化 basename 避免同秒撞库 hard-fail 打断无人值守,
直接服务「自动化程度最高」(撞库 hard-fail 会中断 pipeline)。verdict 全程未引入需 operator 软件
背景才能维护的重型机制 —— 服务 K「非软件背景 operator」。

## §"Decision matrix"(W: decision-list · 6 项 backlog 一一对一)

| 类别 | backlog | 来源(标的位置) | 理由 + SOTA 对标 | 优先级 |
|---|---|---|---|---|
| **调整(refactor)** | G3 replay-window | XenoDev verify-ppv-p2.sh Step 5 + lib line 330-352 | freshness 600s 只证「不太旧」· 加 bound log == latest 或单调 review id · **借 TUF rollback/freeze 单调性 · 滤 threshold signing** | **P0** |
| **新增(new)** | R-Q7 immutable-stress | XenoDev codex-review SKILL §3.6.2(real-review/ 目录不存在) | 产首次真实运行证据:immutable real-review/ 写入 + noclobber 同秒碰撞 + bound-log verify · 顺带验 B-3 不撞库 · **借 Git content-addressed naming · 滤完整 ledger** | **P0** |
| **保留(keep)+ 升级** | shared-lib-drift | IDS test-verdict-evidence-mirror-sha.sh + MANIFEST §wave-4 | 保留 SHA/MANIFEST 方案 · 升为每批并发启动前 mirror-sha preflight gate · **借 checksum manifest/git provenance · 滤全量签名链** | **P0 preflight** |
| **调整(refactor)** | G1 consumer-binding | XenoDev verdict-evidence-lib.sh mode 分叉 + SHARED-CONTRACT line 940-941 | producer 发可验证摘要(artifact digest+policy+verifier+log digest)· consumer profile 分层 · line 940-941 从 known-gap 升正式分层 · **借 SLSA VSA · 滤完整 DSSE 签名链** | **P1**(跨机器/跨信任域/第三方 worker 升 **P0**) |
| **调整(refactor)** | G2 singleton-audit | XenoDev codex-review SKILL §3.6.2 singleton latest-pointer | ship evidence 强制 immutable · singleton 仅作人读 latest-pointer · **借 WORM invariant · 滤云 Object Lock** | **P1** |
| **调整(refactor)** | B-3 dir-flock | SHARED-CONTRACT B-1 `ln $DRAFT $TGT` + parallel-builder SKILL §3.1 | 不上 flock(SOTA 证跨平台坑)· basename 唯一化消除同秒碰撞根因 · 并入 R-Q7 naming · **借 O_EXCL/唯一化 · 滤 flock/etcd/Redlock** | **P1**(并入 R-Q7 naming · stress 暴露真撞库升 P0 hotfix) |

每行均可在 §"Evidence map" 溯源。删除(cut)类:**无**(6 项全 refactor/new)。

## §"Refactor plan"(W: refactor-plan · 3 模块)

### 模块 A · evidence 时序闭合 / binding
**改哪里**:XenoDev `verify-ppv-p2.sh` + `verdict-evidence-lib.sh`
- **当前问题**:freshness 只查时间差不查「仍是当前 latest」(P1 现状)· consumer 无独立验证能力(line 940-941 内部矛盾)· R-Q7 范式零运行证据
- **目标态**:G3 加 latest/单调校验(TUF 借鉴)· G1 producer VSA 摘要 + profile 分层(SLSA VSA 借鉴)· R-Q7 stress harness
- **改造步骤**:
  1. `verify_evidence_freshness` 增「bound log == singleton latest_review_log」或「review id 单调 ≥ latest」校验(P0 · G3)
  2. 新增 R-Q7 stress test harness:产真实 immutable 写入 + 模拟 noclobber 同秒碰撞 + bound-log verify(P0 · R-Q7)
  3. producer-full 结果落为可验证 VSA-like 摘要块(artifact digest+policy+verifier+log digest)· consumer 验摘要(P1 · G1)
  4. SHARED-CONTRACT line 940-941 从 known-gap 升 producer-full / consumer-shallow 显式 profile 分层(P1 · G1)
- **风险**:G3 latest-only 可能误杀合法异步 hand-back(P1-GPT §3 不确定项 3)· G1 摘要字段集未定死(v0.4-note 1)
- **预估代价**:G3 校验 S · R-Q7 harness M · G1 VSA+profile M

### 模块 B · immutable review + naming
**改哪里**:XenoDev `codex-review` SKILL writer(§3.6.2)
- **当前问题**:策略 A 允许绑 singleton · 下次 review 覆盖后不可复证(G2)· basename 含秒级 TS 同秒可撞(B-3)
- **目标态**:ship evidence 强制绑 immutable real-review 记录(WORM invariant)· content-addressed/nonce basename · singleton 降级为人读 latest-pointer
- **改造步骤**:
  1. ship 流程 hand-back evidence 强制绑 immutable(拒 singleton)· singleton 仅人读 latest-pointer(P1 · G2)
  2. real-review/ basename 改 content-addressed(内容 hash)或单调 nonce · 消除同秒碰撞根因(P1 · B-3 · 与 R-Q7 命名同一份改动)
- **风险**:content-addressed 同内容同名可能误判重复(v0.4-note 2)· **依赖 K9 决断点批准收紧策略 A**
- **预估代价**:G2 强制 immutable S · B-3 naming S(并入 R-Q7,边际成本≈0)

### 模块 C · concurrency preflight + mirror
**改哪里**:XenoDev `parallel-builder` publish(§3.1)+ IDS mirror gate
- **当前问题**:mirror-sha 守护需手动触发 · 多 worktree 携旧 mirror 无 gate 拦(shared-lib-drift)
- **目标态**:每批并发启动前强制 mirror-sha preflight gate(不上自动 sync hook · 过度)
- **改造步骤**:
  1. 把 `test-verdict-evidence-mirror-sha.sh` 升为并发批次启动前 preflight gate · 未绿不启动(P0 · shared-lib-drift)
  2. B-3 唯一化 basename 在 publish 路径生效(承接模块 B 命名 · P1)
- **风险**:preflight 漏跑则 drift 静默(运维纪律,非代码)
- **预估代价**:preflight 升级 S(测试已存在,只需挂为启动前 gate)

## §"Next-version dev plan"(W: next-dev-plan · 2 milestone + watch)

### Milestone 0 · P0 gate(并发前必完成 · ship-blocker)
- 目标:补齐 3 个 P0 ship-blocker · 全绿才能上并发
- 关键 milestone:
  - M0-1: **shared-lib mirror-sha preflight gate** 上线 · 每批并发启动前强制跑(target_repo: 主要 IDS 改 preflight 挂载)
  - M0-2: **R-Q7 stress** 产首次真实运行证据(immutable real-review/ 写入 + noclobber 同秒碰撞 + bound-log verify · 含 B-3 碰撞验证)(target_repo: XenoDev)
  - M0-3: **G3 latest/单调校验** 上线 · freshness 加 bound log == latest 或单调 review id(target_repo: XenoDev)
- 依赖:M0-2 的 stress 结果决定 B-3 命名用 content-addressed 还是 nonce(v0.4-note 2)
- 风险:R-Q7 零运行证据是最大不确定性 —— 若首次运行暴露 immutable writer 行为与纸面不符,可能反推 G1/G3 修法(见 §underweights)
- **状态:ship-blocker · 并发上线前全绿**

### Milestone 1 · P1 收敛(并发后迭代)
- 目标:结构性轻量改造 · 可在并发跑起来后迭代
- 关键 milestone:
  - M1-1: **G1 VSA-like 摘要 + consumer profile 分层** + SHARED-CONTRACT line 940-941 升正式分层(target_repo: XenoDev SKILL+lib · IDS SHARED-CONTRACT profile + consumer)
  - M1-2: **G2 ship evidence 强制 immutable** · singleton 降级人读 pointer(target_repo: XenoDev codex-review SKILL)
  - M1-3: **B-3 唯一化 basename** 并入 R-Q7 content-addressed/nonce naming(target_repo: XenoDev)
- 依赖:M1-1/M1-2 依赖 K9 决断点批准收紧策略 A
- 风险:G1 摘要最小字段集 plan 时再定(v0.4-note 1)

### Milestone 2 · v0.4-note watch(条件触发)
- 目标:监测 v0.4-note 升级条件 · 触发时按 note 升级,不等下一轮 forge
- 触发条件:
  - 撞库:R-Q7 stress 或首批并发出现真实 EEXIST 撞库/丢 review → B-3 升 P0 hotfix(v0.4-note 1)
  - 拓扑:引入跨机器 runner / 第三方 worker / operator 无法直接审计 XenoDev artifacts → G1 升 P0(v0.4-note 2)

---

## What this menu underweights(强制自批判)

- **R-Q7 immutable 范式零运行证据 = 本 verdict 最大不确定性来源**:`real-review/` 目录不存在
  (双方独立核查确认 · P1-Opus §0 / P1-GPT §0)。整个 evidence binding 链的 P0/P1 改造
  (G3 latest 校验 / G1 VSA 摘要 / G2 强制 immutable)**都建立在一个从未真实执行过的范式上**。
  如果 immutable writer 的 noclobber 逻辑在并发同秒下的真实行为与纸面不符(P1-Opus §3 不确定项 3),
  那 G3 的「绑 immutable log」前提就不稳。这是为什么 M0-2(R-Q7 产运行证据)被列为 P0 且必须**先**跑 ——
  它实质上是其余所有改造的实证地基。

- **反对证据(收敛前的优先级分歧 · 已解决但记录)**:§"Evidence map" 标 ⚠ 的 3 行均为收敛前分歧,
  非未解决冲突。① B-3:P1-Opus 初判 P0,经 SOTA(flock 跨平台坑)+ content-addressed naming 让 B-3
  实装变极轻,R1/R2 合并入 R-Q7 P1。② G1:P1-GPT 初判 P0,因 producer full 已存在 + consumer 已标
  syntax-only,R1/R2 收敛 P1 + 拓扑触发升级。③ shared-lib:P1-Opus 初判 P2,因 preflight 成本≈0
  能挡静默 drift,让步到 P0。三处主 verdict 均坚持收敛后档位,但 v0.4-note 1/2 保留了升级回路。

- **Y 视角覆盖盲区**:Y 未单列「数据完整性/损坏」视角。`ln` atomic + SHA 复验已保完整性(撞库只
  hard-fail 不损坏),所以不损坏不是焦点;但若未来 publish 路径改动,完整性需重新审。另:P1-Opus §1
  提到真代码注释被「真路径...真路径」乱码污染(verify-ppv-p2.sh / SKILL §3.6.3-3.6.4 / parallel-builder §3.1),
  这是工程债但 K10「不越界清理」划在 scope 外,v5 不顺手改 —— 留作独立工程债条目,值得后续 attention。

- **K 中未充分回应的关切**:K 核心诉求「几乎没有人工干预」与 §"Decision menu" [K9] 需 operator 亲自
  拍板存在张力 —— v5 收紧策略 A 必须人工确认,这是无人值守的一次必要中断。verdict 认为这是合理的
  一次性人工 gate(策略变更需 operator 知情),不是常态干预。

- **convergence_mode 副作用(strong-converge 回声室风险)**:双方在 R1 即「高度对齐远超开局预期」,
  SOTA 对标也独立得到几乎相同的 prior-art 映射。这种快速一致**可能是真共识,也可能是两模型读同一批
  证据后的回声室强化**。最该警惕的「双方都同意但可能错」的判断:**「B-3 不上 flock,唯一化 basename
  足够」** —— 双方都基于「11 round-trip 0 撞库」经验值 + SOTA flock 反模式,但都承认零并发实证。
  M0-2 stress 是验证这个共识假设的唯一手段;若 stress 暴露真撞库,v0.4-note 1 立即生效。

- **X 标的覆盖局限 + SOTA 对标深度**:SOTA 对标双方各跑 4-8 次搜索,但都是 **benchmark 级**
  (SLSA VSA / TUF / WORM / Git objects / O_EXCL man-pages),**未深入任一 prior-art 的实装细节**
  (per K12「对标但不过度」· 这是设计选择不是疏漏)。意味着「借 VSA 模式」「借 TUF 单调性」是
  方向性借鉴,落地时(plan-start)可能发现实装细节需再调。

- **forge versioning 提示(什么触发 v6)**:① R-Q7 stress 暴露 immutable writer 真实行为与纸面严重
  不符 → 可能需 v6 重审 evidence binding 链;② operator 决定上**跨机器/跨信任域**并发(G1 升 P0
  后发现 VSA-like 摘要不足以防跨信任域伪造)→ v6 审跨信任域信任模型;③ 真实并发跑出本 verdict
  未预见的 race 类别。常规升级走 v0.4-note 不需 v6。

## Decision menu(for human)

### ⚠ [K9] 必须先决断:是否批准收紧 v4 策略 A

```
双方独立标到同一红线,且都要求 synthesizer 单列此项 ——

问题:是否批准 v5 将 v4 R-Q7「策略 A 两者并存」收紧为
      "ship evidence 强制 immutable + latest/单调绑定"?

说明:
- 这不是重审 v4 verdict(K9 边界 · v4 P0 决议不动)
- 这是 v5 并发触发后,对策略 A(允许绑 singleton 或任意 immutable)的收紧
- G2(强制 immutable)与 G3(latest/单调绑定)的 P0/P1 改造都依赖这个收紧
- 不批准 → G2/G3 改造方案需重设计,M0-3 + M1-2 受阻

→ 在选择下面 [A]/[B]/[C] 前,请先对此给出 yes/no。
```

### [A] 接受 verdict · 进入 P0 改造(进 plan 而非 plan-start)
```
⚠ 本 verdict 的 W 形态不含 next-PRD(operator 明确排除)· 所以**不能直接 /plan-start**
   —— 没有 PRD draft 可吃。本 verdict 产出的是「对现有跨仓系统的改造方案」,不是新 idea/新 PRD。

推荐流程(改造现有 XenoDev + IDS · 非新 fork):
1. 先回答 [K9] 决断点(yes/no)
2. 把 §"Refactor plan" 3 模块 + §"Next-version dev plan" Milestone 0 抽为改造任务清单
3. P0 三门(M0-1/M0-2/M0-3)在 XenoDev + IDS 直接落地(主战场 XenoDev · IDS 只改 preflight)
4. M0-2(R-Q7 stress 产运行证据)是地基 · 建议最先做
5. P0 全绿 → 上并发 → 并发后迭代 Milestone 1(P1)
```
⚠ 此选项不走 L4 plan-start(无 PRD)· 是横切层改造直接落地。

### [B] 跑 forge v6(说明需要补什么)
```
/expert-forge 006
# 在 Phase 0 intake 时调整 X / Y / Z / W / K
# 旧 v5 整目录保留作历史参考
```
适用:① R-Q7 stress 暴露 immutable writer 行为与纸面严重不符;② operator 决定上跨机器/跨信任域
并发,需审跨信任域信任模型;③ 真实并发跑出本 verdict 未预见的 race 类别。
（常规升级走 v0.4-note 不需 v6。）

### [C] 局部接受
- ✅ 采纳:<勾选要落地的项 · 如「P0 三门全收 · P1 延后」>
- ⏸ 挂起:<如「G1 VSA 等确定要上跨机器并发再做」>
- ❌ 拒绝:<如「不批准收紧策略 A · 见 [K9]」· 需注明 G2/G3 替代方案>

### [P] Park
```
/park 006
```
保留所有 forge v5 产物,标记暂停。复活时不重做这一层。
（注意:park 意味着推迟并发 —— 当前 P0 洞未补,不应在 park 期间裸上并发。）

### [Z] Abandon
```
/abandon 006
```
（不预期 · v5 verdict 是「可上并发」而非「不该做」· 仅列为标准选项。）

---

## Forge log
(由 /expert-forge 命令更新;记录每次 forge run 的 v 序列 + 关键 verdict 一句话)

- v5: 2026-06-01 — verdict: "CONCERNS · 并发可上但先过 P0 三门(堵 G3 replay + 产 R-Q7 运行证据 + shared-lib mirror-sha preflight)· G1/G2/B-3 P1 轻量改造 · K8 滤掉全部重量级方案 · G2/G3 收紧 v4 策略 A 需 operator 确认"
- v4: — verdict: "post-v0.2 协议稳态化 · 6 项 backlog C 全收 · P0 原子波双仓 ship · contract 2.3 · 并发 backlog 推迟到并发实战再判(本 v5 即兑现)"
