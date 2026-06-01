# Forge v5 · 006 · P3R1 · Opus47Max · 联合收敛 R1(标分歧)

**Timestamp**: 2026-06-01T00:30:00Z
**Visibility**: 我已读对方 P1 + P2。
**Searches in this round**: NONE(避免 R1 又开搜索发散)。

## 1. 整合摘要

读完双方 P1+P2 后,这件事的样子已经很清楚,且**双方在事实层与方法层高度对齐**,远超我开局预期。

**事实层完全一致**(双方独立核查同一证据):producer 侧已有较强 evidence binding(`verify-ppv-p2.sh` Step 0 rebind + lib full mode rehash/consistency/freshness),consumer 侧只是 syntax-only precheck;`real-review/` 目录**不存在** —— R-Q7 immutable 范式自 P0 落地从未真实执行过一次。这三点是所有 verdict 的地基。

**方法层经 SOTA 对标后收敛**:双方各跑搜索,独立得到几乎相同的 prior-art 映射。G1 = SLSA VSA(producer 发可验证摘要,consumer 验摘要而非重跑);G3 = TUF rollback/freeze(Codex 补的,比我的「单调 id」更精确:freshness 必须配版本单调 + latest 绑定);G2 = WORM invariant(借不可覆盖语义,不上云);R-Q7 = Git content-addressed naming(Codex 补的,内容 hash 命名直接消除同秒碰撞);B-3 = O_EXCL/唯一文件优于 flock(双方都判 flock 跨平台坑不可取)。**最关键的共识 = K8 滤网双方独立达成**:共同滤掉 etcd/Redlock、完整 DSSE/in-toto 签名链、云 WORM、hash-chain ledger —— 对单 operator 多 worktree 全是过度工程。

唯一实质分歧收窄到**一项**:B-3 的优先级。

## 2. 我的初步 verdict(草案)

**verdict:6 项 backlog 全部 refactor/new(无一 cut),分三档落地。P0(并发上线前 ship-blocker)= G3 堵重放窗 + R-Q7 产首次运行证据 + shared-lib preflight gate;P1 = G1 VSA 化 + G2 强制 immutable + B-3 唯一化 basename。** 理由:(1) 事实层证明 consumer 信任链有真洞但 producer 已强,所以「补 consumer 验证能力」是有解的工程问题不是死结(SLSA VSA);(2) K8 滤网把所有重量级方案排除,留下的轻量层改动都小;(3) R-Q7 零运行证据是最隐蔽的风险 —— 一个从未执行的范式不能在并发下首跑。关键不确定点是 B-3 该不该进 P0,见 §3。

## 3. 关键分歧清单

- **分歧 1**:B-3 dir-flock 是 P0 还是 P1
  - 我的立场:P2 我已从「B-3 整体 P0」让步到「压测碰撞率 P0 / 真锁实装 P1」—— 因为 `ln` atomic 已保完整性,撞库只是 hard-fail 丢 review,不是安全洞,没真实碰撞数据前不宜把实装判 P0。
  - 对方立场(Codex P2 原句,≤15 words):"先压测再决定偏软……不能等撞库后再补"
  - 我希望 R2 怎么收敛:**我倾向接受 Codex 修正,但用 content-addressed naming 化解张力**。Codex 自己 P2 给的 R-Q7 方案(Git 内容 hash 命名)恰好让 B-3「实装」变得极轻 —— 如果 basename 用内容 hash 或单调 id,同秒碰撞根因直接消失,那就**不存在「压测 vs 实装」的二选一**:唯一化 basename 既是 R-Q7 的命名方案,又顺手解了 B-3 的碰撞,一份改动两处收益。所以 R2 应把 B-3 与 R-Q7 命名**合并为同一项 P1 改动**,而非把 B-3 单列 P0。压测则作为「改完后的验证证据」而非「改之前的前置 gate」。

- **分歧 2**(次要 · 优先级微调):shared-lib-drift 的 preflight gate 是 P0 还是 P2
  - 我的立场:P2 我判 P2(非 ship-blocker)。
  - 对方立场(Codex P2 原句):"并发 preflight 调高为 P0 gate"
  - 我希望 R2 怎么收敛:**接受 Codex**。preflight 是「每批并发启动前跑一次 mirror-sha」,成本几乎为零但能挡掉「worktree 携旧 mirror」的静默 drift。这个调高合理,我让步。归 P0(但属「运维 gate」类,不是代码改动)。

## 4. 与 K 的对齐性自检

- K8「v5 mission = 并发安全加固 + evidence binding 时序闭合 · 可靠优先但不过度工程」→ ✅ verdict 全程过 K8 滤网,所有重量级方案已排除,留轻量正确层(O_EXCL/单调 id/VSA 摘要/WORM invariant/preflight)。
- K9「v4 P0 决议不重审」→ ⚠ **需注意**:G2「强制 immutable + 拒 singleton」、G3「收紧绑定」**改动 v4 brief 已批准的「R-Q7 策略 A 两者并存」**。这不是重审 v4 verdict,但确实收紧了 v4 的设计选择。R2 必须显式向 operator 标明「这是对策略 A 的收紧,需 operator 确认」,不能默默改。
- K11「strong-converge · 6 项一一对一 · 残余分歧降 v0.4-note」→ ✅ verdict 已对 6 项一一给档,残留分歧仅 B-3 优先级,R2 收敛后无需 v0.4-note。
- K12「对标 SOTA · 每项说清借鉴/滤掉」→ ✅ §1 已逐项映射 prior-art + K8 滤网结论。
- 核心诉求「可靠的、自动化程度最高」→ ✅ 并发安全加固直接服务「可靠」;B-3 唯一化 basename 避免 hard-fail 丢 review 直接服务「自动化程度最高」(撞库 hard-fail 会打断无人值守)。
