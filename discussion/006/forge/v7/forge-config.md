---
forge_version: v7
created: 2026-07-07T11:30:53Z
convergence_mode: strong-converge
x_hash: 024bf278a91ae3e183606b91a7d0b9c7
prefill_source: FORGE-006-v7-PENDING.md(operator 预填导航 · 2026-07-06/07 两 session 攒批)+ KG-B1 现场并入(2026-07-07 Phase 0 发现)
---

# Forge Config · 006 · v7

## X · 审阅标的

discussion/006/FORGE-006-v7-PENDING.md
discussion/006/forge/v7/_x-backlog-snapshot.md
/home/ys/codes/XenoDev/dogfood-backlog.md
discussion/006/forge/v6/stage-forge-006-v6.md

### 解析后的标的清单

- `discussion/006/FORGE-006-v7-PENDING.md`(类型:本仓库文件 · pending KG 聚簇导航 + 两 session fresh evidence · ✅ 可达。⚠ 注意它尚未含 KG-B1,以快照为准补)
- `discussion/006/forge/v7/_x-backlog-snapshot.md`(类型:本仓库文件 · **pending KG 权威全文快照** · ✅ 可达 · **首选阅读源**。backlog 原文分支依赖:KG-30~38 在 XenoDev `feat/009-spec`,KG-B1 在 `feat/001-radar-pA-spec`,两分支互不可见——快照合流了两边 + 标注 provenance,v6 有 KG29 快照先例)
- `/home/ys/codes/XenoDev/dogfood-backlog.md`(类型:外部 repo 文件 · ⚠ Codex 沙箱可能 BLOCK + **分支依赖**(当前工作树是 001 分支,无 KG-30~38)· 仅作能读时的原文核对源,不是必读)
- `discussion/006/forge/v6/stage-forge-006-v6.md`(类型:stage 文档 · v6 verdict=portability-refactor 覆盖 KG-26~31 · 承接上下文 + 确认 v7 不重叠;只读 verdict/decision-list/underweight 三节即可)

## Y · 审阅视角

✅ 工程纪律(review/CI/fallback 机制 · 核心)
✅ 架构设计(review gate 单点依赖 · fallback 分流架构)

## Z · 参照系

mode: 对标 SOTA
**检索方向**(P2):CI review gate 的容错/降级模式 · 外部服务依赖的 fallback/circuit-breaker 制度化先例 · 长时任务挂起态检测(liveness/watchdog)· 多 reviewer 分流(human/bot fallback)实践
**外部材料叠加**:无(K 中未给额外链接)

## W · 产出形态

✅ decision-list(4 列矩阵:保留/调整/删除/新增)
✅ refactor-plan(按模块分组 · SKILL/协议层改法 · 落 IDS 三层同步)

## K · 用户判准

v7 收 v6(可移植性)之后攒的一批框架级 KG,主攻【codex-review 作为 review gate 的可靠性】——
簇1 五条同根(KG-23 scope 语义 / KG-32 额度死锁 / KG-35 输出落盘 / KG-37 沙箱权限 / KG-38 会话流
静默挂起),共同根因是 review gate 把 codex 当唯一可靠通道,但它在五处都会失效。核心诉求:
**review gate 不能单点依赖 codex,fallback 要制度化不靠临场犹豫,且挂起态要能超时检测触发 fallback**。
(毗邻证据:backlog 未编号条目「后台长任务缺存活检测+单实例锁」与挂起检测同主题族,审簇1 时可一并纳入。)

**簇2 升级为第二主攻(2026-07-07 Phase 0 现场并入)**:**KG-B1(spine 级 · high · 正在阻塞)**——
hand-back validator 约束6 charset regex 不接受 IDS 铸的「带 idea-slug 中段」fork-id(001-radar-pA 三段式),
连 KG-29 v0.3 修都不接 → **001-radar-pA 这个 fork 的全部 hand-back 无法发布,反向通道断裂**(T001 已
ship 却收不了口)。附带 gen-handback 强读根 HANDOFF 的 SSOT 假设在多 fork 并行(008/009/001 同开)下
会静默用错 fork id。这与 KG-29 同族,backlog 自标「同批审 fork-id charset 协议」。**fork-id 铸造约定的
SSOT 在 IDS(plan-start),charset 校验在 XenoDev mirror 件——这是跨仓协议漂移,恰是 forge 该裁的**:
修 regex(需严审 path-traversal 安全)还是收紧 IDS 铸造约定,或两者。原簇2 papercuts(KG-12 validator
相对路径误报 · KG-31 gen-handback mac 字面路径)一并清。
簇3(build mechanics:KG-33 worktree remove 丢 stash 指针 · KG-34 executescript 与生产 execute 语义
不一致)/ 簇4(KG-22 phased spec per-phase review status 不被下游 gate 识别)顺手清。

硬约束:⚠ codex-review SKILL 是 IDS bootstrap-kit mirror 件,改动必须落 IDS 三层同步,不在 XenoDev
当场改。fresh evidence 权重:KG-38 是 2026-07-06 T017 新撞(与 KG-32 额度死锁是不同失效模态——
挂起不报错不退出更隐蔽);KG-12 连续两个 handback-review session 重现;KG-37 在 T016 撞、T016b 又
证明是间歇性。这些是活疼不是陈账。

## 收敛强度

✅ strong-converge

---

## Summary for reviewers

**审阅标的总数**: 4(1 导航 + 1 权威全文快照[首选] + 1 外部原文[可选核对 · BLOCK 可跳] + 1 v6 承接)
**视角维度**: 工程纪律 · 架构设计
**参照系**: 对标 SOTA(CI review gate 容错/降级 · fallback 制度化 · 挂起检测 · 多 reviewer 分流 · 跨系统 id/schema 契约演化)
**预期产出**: decision-list + refactor-plan(SKILL/协议层 · IDS 三层同步)
**用户最在乎**: 双主攻——① review gate 对 codex 的单点依赖在 scope 语义/额度/输出落盘/沙箱/会话流五处失效(簇1 五条同根,两条本周 fresh);要 fallback 制度化 + 挂起态超时检测,不靠临场犹豫。② KG-B1 跨仓 fork-id charset 协议漂移(spine 级 · **正在阻塞 001-radar-pA 反向通道**);要裁 regex 扩展 vs IDS 铸造约定收紧。簇3/4 顺手清。mirror 件改动落 IDS 三层同步。
**收敛模式**: strong-converge
