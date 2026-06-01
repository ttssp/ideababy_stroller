# Forge v5 · 006 · P3R1 · GPT55xHigh · 联合收敛 R1(标分歧)

**Timestamp**: 2026-06-01T07:54:37Z
**Visibility**: 我已读对方 P1 + P2。
**Searches in this round**: NONE(避免 R1 又开搜索发散)。

## 1. 整合摘要

双方事实层已经高度对齐:producer 侧有 Step 0 rebind、allowlist、rehash、一致性和 600s freshness;IDS consumer 仍只是 syntax-only precheck;`real-review/` 目录为空,所以 R-Q7 immutable 还是零运行证据;B-3 目前靠 `ln` 原子发布 + EEXIST hard-fail,完整性不坏但自动化会被同秒撞库打断。

SOTA 层也收敛到同一滤网:不要 etcd/Redlock、完整 DSSE/in-toto 链、云 WORM 或 hash-chain ledger;要轻量正确,即 O_EXCL/link 唯一化、单调 review id/latest equality、VSA-like 摘要、immutable evidence、mirror SHA preflight。Opus P2 对 B-3 的一句话我接受:"真修法不是加锁",而是去掉同秒碰撞根因。

## 2. 我的初步 verdict(草案)

我的 verdict 是 **CONCERNS,但不是 BLOCK**:并发上线前必须补三个 P0 gate/语义洞,其余作为 P1 收敛改造。6 项档位如下:

| backlog | verdict | 档位 | 立场 |
|---|---|---|---|
| G3 replay-window | refactor | P0 | 600s freshness 必须加单调 review id 或 latest equality;否则旧 approve 可绕新 needs-attention。 |
| R-Q7 immutable-stress | new | P0 | 先产真实 immutable 记录、noclobber 碰撞、bound-log verify 证据;零运行证据不能上并发。 |
| shared-lib-drift | keep | P0 preflight | 保留 SHA/MANIFEST 方案,但并发批次启动前强制跑 mirror-sha gate。 |
| G1 consumer-binding | refactor | P1 | 做轻量 VSA-like producer-full 摘要;IDS 不应强行 rehash XenoDev 私有路径。 |
| G2 singleton-audit | refactor | P1 | ship evidence 强制 immutable;singleton 只作 latest pointer。 |
| B-3 dir-flock | refactor | P1 | 不单上重锁;并入 R-Q7/content-addressed 或 nonce basename 唯一化,压测作改后证据。 |

## 3. 关键分歧清单

- **分歧 1**:B-3 是否单列更高优先级
  - 我的立场:我从 P2 的"不能等撞库后再补"收敛为:不能裸上并发,但也不必把 B-3 单列 P0 实装;把 basename 唯一化并入 R-Q7 命名 P1,同时用 P0 stress gate 证明不会同秒撞库。
  - 对方立场(引用对方 P2 原句,≤15 words):"B-3 压测 P0 / 实装 P1"。
  - 我希望 R2 怎么收敛:写成"R-Q7 stress P0;B-3 命名唯一化 P1,与 R-Q7 content-addressed/nonce naming 合并;若 stress 出现真实撞库,升 P0 hotfix"。

- **分歧 2**:G1 是 P0 还是 P1
  - 我的立场:我从 P2 的 P0 下调到 P1。原因是 producer full 已存在,consumer wrapper 明确标 syntax-only,短期 P0 风险主要在 G3 replay 与零运行证据。VSA-like 摘要应做,但不阻断第一批同机并发。
  - 对方立场(引用对方 P2 原句,≤15 words):"P0/P1 边界"。
  - 我希望 R2 怎么收敛:若 operator 要跨机器/跨信任域并发,升 G1 P0;若仍是同机/少数 worktree,保 P1。

## 4. 与 K 的对齐性自检

- K8 "可靠优先但不过度工程" → ✅ P0 只放 replay、真实运行证据、mirror preflight;P1 用轻量唯一化和 VSA 摘要,不上分布式锁。
- K9 "v4 verdict 继承 · 不重审" → ⚠ G2 "强制 immutable"和 G3 "latest/单调绑定"会收紧 v4 已批准的 R-Q7「策略 A 两者并存」。这不是重审 v4 P0,而是 v5 并发触发后的收紧;**需 operator 确认这是对策略 A 的收紧**。
- K10 "边界先定、批量 SSOT、不越界" → ✅ G1 归协议 profile + hand-back evidence 摘要;shared-lib 仍以 XenoDev SSOT + IDS mirror gate 处理。
- K11 "strong-converge" → ✅ 6 项都有单一 keep/refactor/new + P0/P1 档,不保留"双方都对"。
- K12 "SOTA 但不过度工程" → ✅ 只借 O_EXCL/link、单调 id、VSA 摘要、WORM invariant、SHA provenance;过滤 etcd/Redlock、完整签名链和 ledger。
