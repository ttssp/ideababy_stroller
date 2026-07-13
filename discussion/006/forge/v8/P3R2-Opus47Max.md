# Forge 006 v8 · Phase 3R2 · Opus 4.7 Max finalize(strong-converge)

**Written**: 2026-07-13T12:40:00Z
**读入**: P3R1-GPT55xHigh.md(新)+ 双方全部 round file refresh · convergence_mode=strong-converge · moderator-notes 不存在

## §1 · 对每条分歧的最终立场 + 让步

1. **worktree 校验轻重 → 签收对方案**:P0 = 默认 `claude -w <idea>` + 命名约定(worktree/分支名 = idea id)+ **warn 型 preflight**(mismatch 提示不阻断);hook block 留 v0.2,升级判据 = warn 后仍复发混线。我让步:撤回「现在就加 hook」倾向——本周混线发生在**无任何机器提示**的环境下,warn 是否足够未经检验,先给 warn 一个证明自己的机会(对齐 v7「真跑校准」先例)。**采纳对方增量**:outbox/handback 包 frontmatter 写入 `current_idea/worktree/baseline` 三字段,让跨仓通道自带拓扑自证。
2. **B5 迁移粒度 → 双方案合一**:契约章定 messages-style 为 v2 正典;`complete(prompt)` 降级为 **legacy adapter**(v1 包装 v2,单向依赖);≥1 个迁移窗口 + 兼容测试(v1/v2 同语料双跑);新 task 一律 v2,001 项目内四个消费面在下一个自然接触点收编(不专开迁移 task,防过度工程)。
3. **main 治理角色 → 签收对方生命周期,补一个 checkpoint 定义**:proposal on main → idea worktree branch(治理产物在 idea 分支上累积)→ **accepted governance artifact 经 human checkpoint 合回 main** → branch cleanup。我补:checkpoint 的自然候选 = 既有决策点(handback-review 决议后 / stage 文档定稿后 / forge verdict 落地后),不新设仪式;merge-back 频率由 operator 节奏定,规约只要求「合回前 main 不得反向污染 idea 分支以外的 idea 内容」。
4. **契约 vs SKILL 切分 → 无实质分歧,消除误读**:我 P2 的「强制点可以很轻」指**实现**轻(登记表 = 文件级),不是语义只落 SKILL。终案 = 对方表述:SHARED-CONTRACT 新章写 gate 执行语义不变量(PASS artifact 存在性 / 单次执行 / answer-key 一次性 / stale 签字作废),SKILL/preflight 写最低实现,mirror 同步(SSOT 侧改 + cp -p + MANIFEST SHA + fixture)列为验收项(复用 v7 A4 双仓 fixture 模式)。

## §2 · 联合 verdict(单一)

**incremental optimize,不 redesign,零 cut。** 七项批次按四簇落地:**①(P0)gate 执行语义**——B4+B7 合并,SHARED-CONTRACT 新章定四条不变量(gate task 语义 / PASS artifact 机器查验 / 已判 run 登记一次性消费 / 新 run 作废 stale 签字),XenoDev preflight 落最轻实现(机器可读登记表),终结「防 V4 的 STOP 只是 markdown 约定」;**②(P0 规约 + P1 机制)分支拓扑显式化**——session-per-idea worktree 默认命令化(复用原生 `-w`,零自建),main 生命周期 = proposal → idea 分支 → human checkpoint 合回 → 清理,build 基线从隐含 main 改机器可读声明,warn 型 preflight 起步;**③(P0 契约 / P1 实施)LlmClient role 分离**——messages-style 进契约作 v2,legacy adapter 保兼容,数据永不进指令通道,allowlist 序列化降级保留为纵深防御;**④(P1)证据与 hook 治理**——gitignore 模板路径无关豁免 + 证据入仓机器检查,hook 白名单按模式类集中收敛 + 定期回审,明拒逐例加白(KG-B1 同构路径病)。既有强 gate、Safety Floor fail-closed、codex primary 地位全部不动。四簇均有 SOTA 直接对应物(nonce 一次性/role separation/显式 baseline/集中 allowlist 治理),无一处发明新轮子。

## §3 · 残余分歧降级为 v0.2 note

1. **hook block 升级判据**:warn 型 preflight 上线后若 mismatch 混线仍复发(≥2 次),升级为 commit-time block;判据数据来自真跑。
2. **B5 旧消费面收编时限**:「下一个自然接触点收编」若三个月后仍有 v1 残留,v0.2 裁是否专开收编 task。
3. **gate 登记表并发语义**:多 session 并行判同一 gate 的竞态(登记表文件锁?)v0.1 单 operator 场景不触发,留观察。
4. **worktree 运行时资源互斥**:SOTA 提醒 worktree 不隔离 DB/env/服务;XenoDev 侧两 session 并行跑测试的互斥面声明,出现第一次真冲突再规约化。

## §4 · W 形态产出的初步草稿建议

- **verdict-only**:§2 首句可直接作 verdict 关键句。
- **decision-list**:7 行(B2/B3/B4/B5/B6/B7/worktree 诉求)× 4 列(保留/调整/新增/defer),每行标簇号 + P 级 + 证据源(全部可溯源到快照/round files)。
- **refactor-plan**:四模块 = 四簇;每模块含当前问题/目标态/改造步骤/涉及 mirror 件与同步顺序/预估代价(①M ②M ③M ④S);模块① 显式引用 v7 模块 A/B 的先例结构。
- **next-dev-plan**:双仓分道——**IDS 侧**:SHARED-CONTRACT gate 执行语义章 + fork-id §7 邻章排布、worktree 规约进 CLAUDE.md、hook 白名单治理规则;**XenoDev 侧授权条目**:preflight 登记表实现、LlmClient v2 + adapter、gitignore 模板修、baseline 声明消费、B6 hook 白名单实装;P0(①簇契约+preflight、②簇规约、④簇 gitignore)/ P1(③簇实施、②簇 baseline 机制、④簇白名单治理)/ P2(v0.2 notes 四项观察位)。
