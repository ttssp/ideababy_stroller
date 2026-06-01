# Forge v5 · 006 · P3R2 · Opus47Max · 联合收敛 R2(finalize)

**Timestamp**: 2026-06-01T00:50:00Z
**Visibility**: 我已读对方 P3R1。
**Convergence mode**: strong-converge(从 forge-config 读)

## 1. 我对每条分歧的最终立场 + 让步

- **分歧 1**(B-3 是否单列更高优先级):
  - 对方在 P3R1 给的论证:"并入 R-Q7/content-addressed 或 nonce basename 的 P1 改动,保留 P0 stress gate" → **完全接受**。
  - 我的最终立场:**B-3 命名唯一化并入 R-Q7 content-addressed naming 改动,归 P1**;R-Q7 stress 本身是 P0(产首次运行证据,含 noclobber 同秒碰撞测试)。即:**P0 的 stress gate 顺带验证 B-3 不撞库,B-3 的代码改动(唯一化 basename)在 P1**。若 stress 暴露真实同秒撞库,升 P0 hotfix。
  - 让步给对方的部分:无实质让步 —— 双方在 R1 已收敛到同一表述。

- **分歧 2**(G1 是 P0 还是 P1):
  - 对方在 P3R1 给的论证:"若跨机器/跨信任域并发再升 P0;同机/少数 worktree 保 P1" → **接受为条件分档**。
  - 我的最终立场:**G1 = P1(default) + 部署拓扑触发升级条款**。当前 operator 是单机多 worktree(同信任域),G1 的伪造风险被「同一 operator 不会自己伪造证据」压住,P1 足够。**一旦跨机器 / 跨信任域 / 引入非 operator 的第三方 worker,G1 升 P0**。这把「P0/P1 边界」从模糊收敛成「一条明确的拓扑触发线」。
  - 让步给对方的部分:接受 P1(我 P2 曾倾向上调到 P0/P1 边界)—— Codex 的「producer full 已存在 + consumer 已标 syntax-only,短期风险主要在 G3」论证站得住。

## 2. 联合 verdict(单一)

**v5 verdict = CONCERNS(可上并发,但有 3 个 P0 ship-blocker 必须先补)。**

6 项并发 backlog 全部 refactor/new(无一 cut),经 SOTA 对标 + K8 滤网,收敛为三档轻量正确改造:

**P0(并发上线 ship-blocker · 3 项)**:① **G3 堵重放窗** —— 600s freshness 必须加「bound log == 当前 latest」或单调 review id 校验(SOTA:TUF rollback/freeze;纯时间窗是教科书级 missing-freshness 反模式);② **R-Q7 产首次运行证据** —— `real-review/` 目录为空,immutable 范式零运行证据,并发前必须先产真实 immutable 写入 + noclobber 同秒碰撞 + bound-log verify 的压力样本(这一步顺带验证 B-3 不撞库);③ **shared-lib preflight gate** —— 每批并发启动前强制跑 `test-verdict-evidence-mirror-sha.sh`,挡 worktree 携旧 mirror 的静默 drift。

**P1(收敛改造 · 3 项)**:④ **G1 VSA 化** —— producer 在 hand-back 写可验证的「已验证摘要」(SLSA VSA 模式:artifact digest + policy + verifier + log digest),consumer 验摘要而非重跑 XenoDev 私有路径校验;把 SHARED-CONTRACT line 940-941 从 known-gap 升为显式 producer/consumer profile 分层;⑤ **G2 强制 immutable** —— ship 流程的 hand-back evidence 强制绑 immutable real-review 记录,singleton 仅作人读 latest-pointer;⑥ **B-3 唯一化 basename** —— 并入 R-Q7 content-addressed/nonce 命名,消除同秒碰撞根因(不上 flock,SOTA 证其跨平台坑)。

**G1 升级条款**:G1=P1 default,跨机器/跨信任域/第三方 worker 时升 P0。

**⚠ K9 operator 决断点**:G2(强制 immutable + 拒 singleton)+ G3(收紧绑定)**会收紧 v4 brief 已批准的「R-Q7 策略 A 两者并存」**。这不是重审 v4 P0 决议,是 v5 并发触发后对策略 A 的收紧。**需 operator 在 decision menu 显式确认**。双方独立标到同一红线。

## 3. 残余分歧降级为 v0.4-note

- **v0.4-note 1**:G1 VSA 摘要的**最小字段集**未在 v5 定死(SLSA VSA 全字段 vs 轻量 4 字段)。留 P1 实装时按「过 K8 滤网的最小可验证集」定,不在 v5 verdict 锁死。何时回头看:G1 进 plan-start 时。
- **v0.4-note 2**:B-3 命名用 **content-addressed(内容 hash)还是单调 nonce** 未定死。content-addressed 同内容同名(可能误判重复),nonce 单调但需计数器状态。留 R-Q7 stress 实测后按碰撞行为定。何时回头看:R-Q7 P0 stress 出证据后。

## 4. W 形态产出的初步草稿建议(供 synthesizer)

**W 含 verdict-only → verdict 关键句**:
"v5 = CONCERNS。6 项并发 backlog 全 refactor/new,经 SOTA+K8 滤网收敛为轻量正确三档:P0(G3 堵重放 + R-Q7 产运行证据 + shared-lib preflight)必须并发前补;P1(G1 VSA 化 + G2 强制 immutable + B-3 唯一化 basename)随后。无重量级方案(etcd/DSSE/云 WORM/ledger 全滤掉)。G2/G3 收紧 v4 策略 A,需 operator 确认。"

**W 含 decision-list → 6 项 backlog 矩阵**(keep/refactor/cut/new + 档位 + SOTA 对标):
| backlog | 决议 | 档位 | SOTA 借鉴 / 滤掉 |
|---|---|---|---|
| G3 replay-window | refactor | P0 | 借 TUF rollback/freeze 单调性 · 滤 threshold signing |
| R-Q7 immutable-stress | new | P0 | 借 Git content-addressed naming · 滤完整 ledger |
| shared-lib-drift | keep + preflight | P0 gate | 借 checksum manifest/git provenance · 滤全量签名链 |
| G1 consumer-binding | refactor | P1(跨机器升 P0) | 借 SLSA VSA 摘要 · 滤完整 DSSE 签名链 |
| G2 singleton-audit | refactor | P1 | 借 WORM invariant · 滤云 Object Lock |
| B-3 dir-flock | refactor | P1(并入 R-Q7 naming) | 借 O_EXCL/唯一化 · 滤 flock/etcd/Redlock |

**W 含 refactor-plan → 3 模块**:
- 模块 A · evidence 时序闭合(XenoDev `verify-ppv-p2.sh` + `verdict-evidence-lib.sh`):G3 加 latest/单调校验 + R-Q7 stress harness(改 freshness 函数 + 新 test)。
- 模块 B · evidence 跨仓信任(SHARED-CONTRACT §6 + hand-back schema + IDS consumer):G1 VSA 摘要字段 + line 940-941 profile 分层 + G2 ship 强制 immutable。
- 模块 C · 并发写 + mirror(codex-review SKILL writer + parallel-builder publish + IDS mirror gate):B-3 唯一化 basename + shared-lib preflight gate。

**W 含 next-dev-plan → 2 wave milestone**:
- **Wave P0(并发前必完成)**:G3 latest 校验 + R-Q7 stress 产首次运行证据(含 B-3 碰撞验证)+ shared-lib preflight gate。target_repo:主要 XenoDev,IDS 改 preflight。ship-blocker:并发上线前全绿。
- **Wave P1(并发后收敛)**:G1 VSA + G2 强制 immutable + B-3 唯一化 basename。可在并发跑起来后迭代。改 XenoDev(SKILL+lib)+ IDS(SHARED-CONTRACT profile + consumer)。
