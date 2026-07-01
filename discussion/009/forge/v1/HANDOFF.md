# 🔀 Session Handoff · forge 009 v1

> **给新 session 的快速接手文档。** 写于 2026-07-01T03:10Z(Phase 4 完成后更新为 DONE)。
> 读完这份 + `stage-forge-009-v1.md` 就能无缝接手。**不要重读整段对话历史**,状态全在这里。

## 一句话状态

**forge 009「投资决策闭环」v1 已完成(phase=done)。** stage 文档 `stage-forge-009-v1.md` 已产出,单一 verdict、无 unresolved。**下一步是 operator 拍板 Decision menu**(见 stage doc 末尾 [A]-[Z]);synthesizer 推荐起点 = **[C] 局部接受**。

## 怎么接手(立即可执行)

```bash
cd /home/ys/codes/ideababy_stroller
cat discussion/009/forge/v1/stage-forge-009-v1.md   # 读最终 verdict + 4 件 W 产物 + Decision menu
```

forge 循环**全部跑完**(P1/P2/P3R1/P3R2 双方 8 份 + synthesizer stage doc)。**不需要再 cdx-run**。接下来是纯 operator 决策:进 L4(需手工 fork PRD branch,见 stage doc [A])/ 局部接受 [C] / park [P] / 跑 v2 [B]。

## Phase 1→3R2 已收敛到哪(供接手者心里有数)· 分歧已全部收敛

双方在 R1 已实质收敛,Opus P3R2 finalize 接受了 GPT 的松耦合 verdict。**单一 verdict**:

> **009 当前不是要新建的独立统一壳,而是"闭环集成契约规范 + 共享回测地基"**,落入 004 v1.0 回测 lane + 008 消费契约的松耦合演进。回测层最先落(point-in-time / walk-forward / OOS / 交易成本 / trial-count / DSR/PBO)。图谱 defer v2+、蒸馏最后且只能独立 lane 化。红线固化:上游只产独立信号/内部评分,**004 端永不呈现权威综合分**。**统一壳升级 = 显式 gate**(仅当 calibration/alpha 两头需 004/008 都不拥有的独立回测内核+状态模型+验收口径时才升级)。

- **(A) 集成形态** → 已收敛:**松耦合胜,统一壳 gated**(Opus 让步接受 GPT 判据)。
- **(B) 红线 #9 边界** → 已收敛:上游独立 lane/内部评分,004 端永不权威综合分,固化为硬验收条款。
残余仅 2 条 v0.2 minor note(两评估头是否长出独立内核 / 008 as-of 时间戳粒度),不影响主 verdict。Opus P3R2 §4 已给 synthesizer 逐项 W 草稿(decision-list / next-PRD / next-dev-plan / refactor-plan)。全文见 `P3R2-Opus47Max.md`。

## 009 是什么(背景 · 为什么起这个 forge)

operator 的终极目标:把**已分散建的 004 + 008 + 四条新想法**合成一个**完整投资决策闭环产品**。这不是新造,是**集成 + 补缺口**。
- **第一性原理(贯穿全程的 K 核心)**:operator 懂算法/自动化/数据,**但不懂投资**。产品本质 = **用工程强项补投资 domain 短板**。
- **闭环灵魂已定(关键,别再让专家纠结)**:"承诺壳"(004·防乱动·下游纪律)与"alpha 引擎"(验证/信号/策略·上游)**共存不冲突,分居上下游**。**已明确 binding:不推翻 004 红线 #1/#9**(它们管下游执行层,不约束上游信号/回测层)。
- 详见 `proposals/proposals.md` §009(行 266)+ 记忆 `closed-loop-investing-product-vision` + `discussion/009/FORGE-ORIGIN.md`。

## forge intake(已落盘在 forge-config.md,这里是速查)

- **X(5 标的)**:009 proposal §009 / 004 PRD / 008 PRD / 008 forge-v4 stage / **004 已 ship 的 strategy 层代码**(`/home/ys/codes/XenoDev/projects/004-pB/src/decision_ledger/strategy/`)。
  - ⚠ X#5 在 XenoDev 仓 → Codex 沙箱若不可达,用 forge-config 末尾 §"X-fallback TEXT" 摘录(已嵌入),P1 inbox 已写明铁律。
- **Y**:架构集成 / 愿景成立性 / 可行性(回测+图谱) / 工程纪律。
- **Z**:对标 SOTA(量化平台·回测框架·多信号融合·投顾量化验证·时序图谱在金融·防过拟合)。
- **W**:next-PRD draft + 架构 refactor-plan + next-dev-plan + decision-list(四件全要)。
- **收敛**:strong-converge。

## Opus P1 已给的关键 first-take(供你心里有数 · 全文见 P1-Opus47Max.md)

**最重要的发现**:**004 已经 ship 了闭环"信号层"的实质骨架,比 proposal 说的还多** —— 不只 StrategyModule IDL,还有真 XGBoost lane + `advisor_strategy`(分析师建模成信号源)+ **`correlation_audit.py` 已在做"模型预测 vs 分析师"的 Pearson 相关性 audit**(这是 backtest-adjacent 原型!)。所以 009 是"集成+补缺口(回测/图谱)+划边界",**不是从零造**。

Opus 的 first-take 倾向:
- 架构:refactor(集成)+ keep(004 strategy 地基) —— 不是 new。
- 愿景:keep(两灵魂共存架构上真成立,004 IDL 本就多信号不合并)+ refactor(第[4]条"蒸馏成自主分析"措辞危险,须钉成"独立信号 lane"防越界红线 #1/#9)。
- 可行性:**回测 new 且最先**(接 008 forge-v4 spike 的依赖链:回测可信 ⊂ 提取可信)；**时序图谱 defer 到 v2+**(现在上=过度设计,operator 怕的 V4)。
- 工程:keep 004 的 lane 隔离 IDL + correlation strict 范式。

Opus §3 三个最不确定点(留给 Codex/P2/P3):① 集合体 vs 拆开做(009 统一壳 vs "004 v1.0+008 接口"松耦合演进就够?)② 回测"一套数据两用"是一个引擎还是两个共享数据源 ③ 图谱 defer 判断有多少把握。

## ⚠ 接手注意事项

1. **git 全未提交**。本 session 产出大量未跟踪文件:`proposals/proposals.md`(加了 §009)、`discussion/009/` 整个目录、`.codex-inbox|outbox/queues/009/`、以及**更早的** 008 forge v4 全套 + handback-review commit(`17557a8` 已 commit)+ `~/.bashrc`(cdx 函数,在你 home 不在 repo)。建议 forge 009 跑完一个完整 verdict 后再统一 commit,或现在就把 009 bootstrap 单独 commit。**operator 偏好:push/commit 前需他确认。**
2. **cdx-run 是 oneshot**(每次新 codex session)。P2/P3 任务标的是 reuse-session(省 token),但 cdx-run 不自动 reuse —— 想省 token 要手工在旧 Codex 终端粘贴(见 forge 各 phase 菜单),否则 cdx-run 也对(只是全 token)。
3. **operator 几轮前刚换机**(Mac `/Users/admin` → Linux `/home/ys`)。008 的旧 handback 包改过前缀;009 全是新机产,无此问题。
4. **AskUserQuestion 长 payload 容易坏 JSON**(本 session 多次踩),问 operator 时拆短、少转义。

## 这一串决策是怎么来的(压缩版,防你误判方向)

operator 这次 session 从 `/handback-review 008` 起步 → 决议起 008 forge v4(信号 spike verdict)→ operator 抛出四条想法(验证 alpha/回测/图谱/蒸馏)→ 发现这四条主体属 004 不属 008 → 深读 004 发现它是"承诺壳"哲学、跟四条相反 → operator 澄清"我要的是完整闭环集合体,004/008 都要" → 定灵魂 (c) 两灵魂共存(分居上下游,因为 operator 不懂投资既要 alpha 引擎补知识又要承诺壳补纪律)→ 决定起统领新 idea 009 + 起 forge 审闭环架构 → 写 009 proposal → 起 forge 009 → 推进到 Phase 1 等 Codex(当前)。
