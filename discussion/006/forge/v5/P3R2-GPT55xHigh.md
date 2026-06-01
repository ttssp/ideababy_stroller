# Forge v5 · 006 · P3R2 · GPT55xHigh · 联合收敛 R2(finalize)

**Timestamp**: 2026-06-01T08:00:15Z
**Visibility**: 我已读对方 P3R1。
**Convergence mode**: strong-converge

## 1. 我对每条分歧的最终立场 + 让步

- **分歧 1**(B-3 dir-flock 是 P0 还是 P1):
  - 对方在 P3R1 给的论证:"B-3 与 R-Q7 命名合并为同一项 P1 改动" → 让步。
  - 我的最终立场:接受该收敛。B-3 不再单列更高优先级;basename 唯一化/content-addressed 或 nonce naming 并入 R-Q7 命名 P1。R-Q7 stress 本身仍是 P0,因为它要产首次 immutable 运行证据、noclobber 同秒碰撞测试,并顺带验证 B-3 不撞库。
  - 让步给对方的部分:我放弃 P2 中对 B-3 "不能等撞库后再补"的单列 P0 倾向;保留条件是 stress 若暴露真实撞库,立刻升 P0 hotfix。

- **分歧 2**(G1 consumer-binding 是 P0 还是 P1):
  - 对方在 P3R1 给的论证:"G1 = P1 default + 部署拓扑触发升级" → 接受。
  - 我的最终立场:G1 默认 P1。当前单机/少数 worktree、同一 operator 信任域下,producer full 已存在,consumer syntax-only 已显式标注,短期 ship-blocker 是 replay 和零运行证据。若改成跨机器、跨信任域、第三方 worker,则 G1 升 P0。
  - 让步给对方的部分:不再把 G1 固定判 P0;用部署拓扑作为升级触发。

## 2. 联合 verdict(单一)

**我和对方在 R2 后达成的单一 verdict**:v5 verdict = **CONCERNS,但不是 BLOCK**。并发上线前必须先完成三个 P0 gate:第一,G3 replay-window 要堵,用 latest equality 或单调 review id 证明 bound log 仍是当前有效 review,不能只靠 600s freshness;第二,R-Q7 immutable-stress 要产首次真实运行证据,包括 immutable `real-review/` 写入、noclobber 同秒碰撞、bound-log verify,并顺带压测 B-3 命名不撞库;第三,shared-lib-drift 要把 mirror-sha 守护变成每批并发启动前 preflight。P1 是结构性轻量改造:G1 做 VSA-like producer-full 摘要 + consumer profile 分层;G2 ship evidence 强制 immutable,目前允许 singleton 的策略 A 需收紧;B-3 不上重型 flock,并入 R-Q7 naming 唯一化。P2 暂无主线代码项,只保留后续自动 sync/更强 provenance 的观察 note。

## 3. 残余分歧降级为 v0.4-note

- **v0.4-note 1 · B-3 撞库升级条件**:主 verdict 不把 B-3 实装列 P0;但若 R-Q7 stress 或首批并发出现真实 EEXIST 撞库/丢 review,立即升 P0 hotfix,不等下一轮 forge。
- **v0.4-note 2 · G1 拓扑升级条件**:当前默认 P1 仅适用于同机/少数 worktree/同信任域。若引入跨机器 runner、第三方 worker、或 operator 无法直接审计 XenoDev review artifacts,G1 立刻升 P0。
- **v0.4-note 3 · K9 策略 A 收紧**:G2/G3 会把 v4 已批准的 R-Q7「策略 A 两者并存」收紧为 ship evidence 强制 immutable + latest/单调绑定。这是 v5 并发触发后的必要收紧,但必须显式交 operator 确认。

## 4. W 形态产出的初步草稿建议

- **verdict-only**:建议关键句写成:"CONCERNS:并发可上,但先过 P0 三门:堵 replay、产 R-Q7 首次真实运行证据、mirror-sha preflight;G1/G2/B-3 作为 P1 轻量改造,并显式收紧 R-Q7 策略 A。"
- **decision-list**:
  - 保留:`shared-lib-drift` 当前 SHA/MANIFEST mirror 机制,但升级为 P0 preflight gate。
  - 调整:`G1 consumer-binding` → P1 VSA-like 摘要 + producer/consumer profile;`G2 singleton-audit` → P1 ship evidence 强制 immutable;`G3 replay-window` → P0 latest/单调绑定;`B-3 dir-flock` → P1 并入 R-Q7 naming 唯一化。
  - 删除:无。
  - 新增:`R-Q7 immutable-stress` → P0 真实运行证据 + noclobber 同秒碰撞 + bound-log verify。
- **refactor-plan**:模块 A evidence binding(profile + VSA-like 摘要 + replay 单调性);模块 B immutable review/naming(real-review、content-addressed/nonce basename、singleton latest pointer 降级为人读);模块 C concurrency preflight(mirror-sha gate + R-Q7/B-3 stress harness)。
- **next-dev-plan**:Milestone 0(P0 gate):mirror-sha preflight、R-Q7 stress、G3 latest/单调校验;Milestone 1(P1 protocol/runtime):G1 profile+summary、G2 强制 immutable、B-3 naming 合并;Milestone 2(v0.4-note watch):若撞库或跨信任域出现,按 note 升级。
- **K9 operator 决断点**:synthesizer decision menu 必须单列确认项:"是否批准 v5 将 v4 R-Q7 策略 A 两者并存收紧为 ship evidence 强制 immutable + latest/单调绑定?"
