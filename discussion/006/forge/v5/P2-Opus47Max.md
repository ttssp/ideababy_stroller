---
doc_type: forge-P2
forge_id: 006
forge_version: v5
side: Opus47Max
phase: 2
created: 2026-06-01T00:20:00Z
z_mode: 对标 SOTA · 并发安全
searches_used: 4
convergence_mode: strong-converge
---

# Forge v5 · P2 · Opus 参照系评估(对标并发安全 SOTA)

## §1 SOTA 对标(6 项 backlog × prior-art × K8 滤网)

跑了 4 组 SOTA 检索:(a) 原子文件创建 O_EXCL vs flock 跨平台;(b) TOCTOU/replay 防护 nonce vs timestamp 窗;(c) append-only/content-addressed 不可变审计;(d) 跨信任域验证 SLSA VSA / in-toto。每项过 K8/K12 滤网(可靠优先但不过度工程 · 单 operator 少数机器不上分布式协调)。

| backlog | SOTA 怎么做 | 我们当前做法 | gap | 借鉴 or 不适用(K8 滤网后) |
|---|---|---|---|---|
| **B-3-dir-flock** | `O_EXCL`/`link()` 创建锁文件 = **portable + simple 跨语言跨平台**;flock 在 NFS/SMB 上语义会变(byte-range 模拟、变非 advisory)· 反模式:跨文件系统用 flock | `ln $DRAFT $TGT` atomic + EEXIST hard-fail + 重 gen TS(秒级) | 无 dir-level 协调 · 同秒同 basename 撞库 hard-fail(不损坏但丢 review) | **借鉴 O_EXCL 思路**;**不用 flock**(SOTA 明确跨平台坑)· 真修法不是加锁,是**去掉同秒碰撞根因 = TS 改单调/唯一后缀(nonce)** · 这比 flock 更轻且更正确 |
| **G3-replay-window** | **学术明确:timestamp 窗 ≠ 防重放**(`timestamp-based nonces alone do not prevent immediate replay within the acceptance window`)· 需 nonce 或单调计数器证明「仍是当前有效」 | freshness 600s 窗(只证「不太旧」) | 600s 窗内旧 approve 可绕新 needs-attention(codex H1)· **这是教科书级 missing-freshness 反模式** | **借鉴单调性**:校验 bound log == 当前 latest(singleton `latest_review_log` 指向它),或拒早于 latest 的 log · 轻量(无需 nonce 表) |
| **G2-singleton-audit** | WORM/append-only + **hash chaining**(每条含前一条 hash)+ 只存 pointer+digest、payload 经 secure reference 取 | 策略 A:singleton 可覆盖 + immutable 记录不可覆盖(但二者并存 · 可绑任一) | 绑 singleton 的包下次 review 覆盖后不可复证 · 无 hash chain | **借鉴 WORM**:ship 流程**强制绑 immutable**,singleton 仅作人读 latest-pointer · hash chain 对单 operator **过度**(K8 滤掉 · 不上链) |
| **G1-consumer-binding** | **SLSA VSA(Verification Summary Attestation)** = 对本问题的教科书解:`consumers make a decision without needing access to all attestations` · producer 发已验证摘要,consumer 验摘要而非重跑 | consumer shallow(只验 7 字段语法)· producer full(rehash/consistency/freshness) | consumer 无法独立验真假 · SHARED-CONTRACT line 940-941 内部矛盾 | **借鉴 VSA 模式**(轻量版):producer 在 hand-back 写一个「我验过 + 结果 + 签名/摘要」的自证块,consumer 验该摘要完整性而非 XenoDev 文件 · 把 line 940-941 从 known-gap 升为**显式 producer/consumer profile 分层** |
| **R-Q7-immutable-stress** | (无直接 prior-art · 是实证空缺)SOTA 的 immutable 范式都假设已运行;我们的连一条记录都没产 | real-review/ 目录不存在 · 纸面范式 | **零运行证据** | 不是 SOTA gap,是**实证 gap**:并发前必须先产真实 immutable 写入 + noclobber 碰撞 + bound-log verify 的运行样本 |
| **shared-lib-drift** | checksum manifest / signed mirror / git provenance(轻量正确,适合单 operator) | SHA dual-verify + MANIFEST §wave-4 + mirror-sha test(手动触发) | 无自动 gate · 多 worktree 携不同 mirror 时间点 | **当前已是 SOTA 轻量正确**;只需把 mirror-sha 升为**并发启动前 preflight gate** · 不上自动 sync hook(过度) |

## §2 用户外部材料消化

K 无外部链接/文件需消化。但 K8/K12 给了关键滤网:operator 非软件背景 + 单 operator 多 worktree(同机/少数机器)。这把所有重量级 SOTA(etcd/redlock 分布式锁、hash-chain ledger、完整 in-toto DSSE 签名链)**明确滤掉** —— 不是因为不好,是因为「过度工程」违 K8。留下的全是**轻量正确**层:O_EXCL、单调 id、VSA 摘要思路、WORM 强制 immutable、preflight gate。

## §3 修正后的视角(P1 哪些站住、哪些被 SOTA 推翻)

**被 SOTA 强化(P1 站住)**:
- 我 P1 对 **B-3 用最轻锁(单调 nonce 去同秒根因)而非 flock** 的倾向 —— SOTA 直接证实 flock 跨平台坑(NFS/SMB 语义变),O_EXCL/唯一后缀更对。**我 P1 的 §3 不确定项 1 现在有答案了:不用 flock。**
- **G3 是教科书级反模式** —— SOTA 把「timestamp 窗 ≠ 防重放」说死了。这强化「G3 必须堵」,且修法明确(单调/latest-only)。

**被 SOTA 修正(我 P1 的判断要调)**:
- **G1 优先级我 P1 判 P1 偏低了**。SLSA VSA 证明「跨信任域 consumer 验证」是**有标准解的成熟问题**,不是「只能留 known-gap」。既然有轻量解(producer 自证摘要 + consumer 验摘要),G1 就从「new·P1·留 gap」上调为「refactor·可做·P0/P1 边界」—— 这把我和 Codex 的分歧(我 P1/它 P0)往它那边拉。
- **B-3 我 P1 判 P0、Codex 判 P1**:SOTA 让我**部分让步**。`ln` atomic 已保完整性(不损坏),撞库只是 hard-fail 丢 review,**不是安全洞**。Codex P1 §3「没并发碰撞数据前不愿判 P0」有道理。修法虽轻(单调 nonce),但**「先压测真实碰撞率」应是 P0,真锁实装可 P1**。我从「B-3 整体 P0」退到「B-3 压测 P0 / 实装 P1」。

**收敛预判**:双方事实层完全一致(producer 强/consumer shallow/real-review 空),分歧只在优先级。SOTA 把分歧收窄了 —— G1 有 VSA 标准解(上调),B-3 完整性已保(下调)。R3 的收敛核心应是:**P0 = G3 堵重放窗 + R-Q7 产首次运行证据 + B-3 碰撞率压测;P1 = G1 VSA 化 + G2 强制 immutable + B-3 真锁;P2 = shared-lib preflight gate**。
