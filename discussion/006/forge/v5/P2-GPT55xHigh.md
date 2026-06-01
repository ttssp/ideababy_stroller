# Forge v5 · 006 · P2 · GPT55xHigh · 参照系评估(with search)

**Timestamp**: 2026-06-01T01:28:24Z
**Searches run**: 8, SOTA-benchmark search only.
**Visibility**: 我已读对方 P1。

## 1. SOTA 对标

| backlog | 参照项 | 它怎么做 | 我们怎么做 | gap + K8/K12 滤网后结论 | URL/Source |
|---|---|---|---|---|---|
| B-3 dir-flock | `O_EXCL` / lockfile / `flock` | `open(O_EXCL)` 有 NFS 条件;man-pages 建议同 FS 唯一文件 + `link(2)`。`flock` 在 NFS/SMB 语义会变。 | `ln $DRAFT $TGT` 原子发布,EEXIST hard-fail。 | P1 的"先压测再决定"偏软。借鉴唯一文件+link/`O_EXCL` 思路;过滤 etcd/Redlock。优先把 basename 加 nonce/单调 id,必要时轻量 lockfile。 | https://man7.org/linux/man-pages/man2/open.2.html · https://man7.org/linux/man-pages/man2/flock.2.html |
| G1 consumer-binding | SLSA VSA / in-toto attestation | verifier 对 subject digest、resource URI、policy 产摘要;consumer 可信 verifier 摘要,不必重跑全验证。 | IDS consumer 只 syntax-only;producer full 自证。 | P1 站住:IDS full rehash 不现实。但 SOTA 给答案:把 producer full 结果变成可消费的 VSA-like 摘要,最小字段=artifact digest+policy+verifier+log digest。过滤完整 DSSE 签名链。 | https://slsa.dev/spec/v1.2/verification_summary · https://github.com/in-toto/attestation |
| G3 replay-window | TUF rollback/freeze 防护 | 用版本单调、过期时间、snapshot hash 互相约束,旧 metadata 不能覆盖新状态。 | 600s freshness 只看时间差,不看"是否最新/单调"。 | P1 站住且更强:P0 应补单调 review id 或 latest pointer equality;只保留时间窗不够。过滤 TUF threshold signing。 | https://theupdateframework.github.io/specification/v1.0.17/ |
| G2 singleton-audit | WORM / immutable object version | WORM 模式阻止锁定版本被覆盖或删除。 | singleton 可覆盖;immutable 范式存在但 `real-review/` 尚无记录。 | P1 站住:ship evidence 不应绑 singleton。借鉴 WORM invariant,不上 S3/Object Lock。 | https://aws.amazon.com/s3/features/object-lock/ |
| R-Q7 immutable-stress | content-addressed storage | Git 以内容 hash 命名对象,hash 即定位与完整性锚。 | ts-slug 文件名 + sha 字段,但零运行样本。 | P1 站住:需真实压力证据。SOTA 还提示可用 content-addressed 文件名降低同秒碰撞和审计歧义;不必上完整 ledger。 | https://git-scm.com/book/en/v2/Git-Internals-Git-Objects.html |
| shared-lib-drift | checksum manifest + signed git provenance | Git object hash/签名提交可验证内容与提交身份。 | MANIFEST + SHA dual-verify,未自动 gate。 | P1 的 keep 站住,但优先级从 P1 偏向 P0 preflight:并发启动前必须跑 mirror SHA gate。过滤全量签名供应链,保留 git/SHA provenance。 | https://www.kernel.org/pub/software/scm/git/docs/git-verify-commit.html |

## 2. 用户外部材料消化

K 无外部链接/文件;本轮只消化 K8/K12 滤网。可吸收的是轻量正确层:唯一化原子创建、单调 review id、VSA-like 摘要、WORM-style 不可覆盖、mirror SHA preflight。会被滤掉的是 etcd/Redlock、完整 in-toto DSSE 签名链、云 WORM 存储、hash-chain ledger;它们对单 operator 同机/少数机器过重,会伤害"自动化程度最高"。

## 3. 修正后的视角

- P1 判断 "consumer 只做 syntax-only" → **站住**。SLSA VSA 支持"consumer 信 verifier 摘要",但要求摘要可验证;当前缺 producer-full result artifact。
- P1 判断 "B-3 先压测真实碰撞率" → **部分被推翻**。`open(2)` 对 lockfile 的建议说明并发写目录应先有唯一化/原子创建策略;不能等撞库后再补。
- P1 判断 "G3 600s 不证明当前有效" → **站住并加重**。TUF 的 rollback/freeze 模式说明 freshness 必须配单调版本或 latest 绑定。
- P1 判断 "ship 流程应强制 immutable" → **站住**。WORM 参照只借 invariant:证据一旦用于 ship,不可覆盖;singleton 只能作 pointer。
- P1 判断 "shared-lib-drift keep/P1" → **修正为 keep 但并发 preflight P0**。不需要自动 sync hook,但每批并发前应强制跑 SHA gate。
- 对 P1 §3 三个不确定项:full consumer binding 的答案是 VSA-like 摘要而非 IDS rehash;B-3 答案是唯一化+原子创建优先于重型 flock;G3 答案是单调 id/latest equality,单纯 nonce 不够。
