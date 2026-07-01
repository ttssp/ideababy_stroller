# 🔀 Session Handoff · forge 009 v2

> **给新 session 的快速接手文档。** 写于 2026-07-01T07:00Z(v2 Phase 4 完成后更新为 DONE)。
> 读完这份 + `stage-forge-009-v2.md` 就能无缝接手。**不要重读整段对话历史**。

## 一句话状态

**forge 009 v2「画目标态蓝图」已完成(phase=done)。** stage 文档 `stage-forge-009-v2.md` 已产出 —— 含**目标态七环节 ASCII 闭环图 + Strangler Fig 分期路线 + 全貌叙事 + 三条硬约束**,单一 verdict、无 unresolved、全程 0 分歧。**下一步是 operator 拍板 Decision menu**(见 stage doc 末尾);synthesizer 推荐起点 = **[C] 局部接受,先推 M1 PIT 数据层**。

## 怎么接手(立即可执行)

```bash
cd /home/ys/codes/ideababy_stroller
cat discussion/009/forge/v2/stage-forge-009-v2.md   # 读目标态图 + 分期路线 + Decision menu
```

forge v2 循环**全部跑完**(P1/P2/P3R1/P3R2 双方 8 份 + synthesizer stage doc)。**不需要再 cdx-run**。

## v2 蓝图定稿(供接手者心里有数)

单一 verdict:009 目标态 = **七环节契约化闭环图(非独立统一壳,不推翻 v1)**。主链 008采集/结构化→回测PIT数据层+alpha头/calibration头→StrategyModule独立lane→004决策/纪律→calibration反馈回流。**唯一关键新器官 = PIT 价格历史层**(日线+复权+PIT ticker+退市感知)。**Strangler Fig 分期** M1数据层→M2 alpha头(最先出数字)→M3 calibration+两条回流线→M4 gated图谱/蒸馏,每期独立可用。**三条硬约束**:① 回流 human-on-the-loop(旋钮建议→human确认;动作/结构/决策权永远手动)② 两档详略(现建器官画定量契约+AC,未来插槽只画签名+gate)③ 回测层 contract tests。

⚠ **v2 未产 next-PRD**(W 未勾)—— 进 L4 须以 v1 stage doc 的 PRD draft 为骨架叠加 v2 蓝图(见 stage doc [A])。⚠ **自批判点出的最大风险** = 双模型回声室(可能共享盲点:calibration↔004 schema 耦合演化 / operator 判不了旋钮建议值的隐性循环依赖);真实价格数据成本 + 分析师样本量仍可能在 M1/M2 推翻代价估计。

## Phase 1→3R2 已收敛到哪(v2 · 蓝图已定稿)

双方全程 0 实质分歧。**单一 verdict**:009 目标态 = **七环节契约化闭环图(非统一壳)**。主链 008采集/结构化→回测PIT数据层+alpha头/calibration头→StrategyModule独立lane→004决策/纪律→calibration反馈回流。唯一关键新器官 = PIT 价格历史层(日线+复权+PIT ticker+退市感知,defer多市场/汇率/tick)。**Strangler Fig 分期**:M1数据层→M2 alpha头(最先出数字最独立)→M3 calibration+两条回流线→M4 gated图谱/蒸馏,每期独立可用。**三条硬约束定稿**:① 回流 human-on-the-loop(旋钮建议→human确认生效,动作/universe/决策权永远手动)② 两档详略(现建器官画定量契约+AC,未来插槽只画签名+gate)③ 回测层 contract tests。旋钮清单 + contract-tests 清单双方一致(见 P3R1-GPT §3 + P3R2-Opus §1)。残余仅 3 条 v0.2 note(不动基线粒度 / 自动套用解锁门槛 / gate 触发走 forge v3 还是 L4)。Opus P3R2 §4 已给 synthesizer 逐项 W 草稿。

## Phase 1+2 已收敛到哪(v2)

双方 v2 P1 **高度对齐**,且 §3 三个不确定点**几乎逐条相同**;Opus P2 用 SOTA 把这三点全给了有依据的答案:
- **不确定点1(回流自动 vs 人工)→ human-on-the-loop**:自适应系统自动回流有过拟合风险(而这正是 operator 判不了的)→ v0.1 回测算"建议旋钮值",human 确认生效,全自动 gated。
- **不确定点2(价格层范围)→ 日线+复权+退市感知**,defer 多市场/汇率/tick;复权必须 v0.1 做。
- **不确定点3(蓝图画多实)→ 按器官成熟度分两档**:现建器官(数据层/alpha头)画定量契约(接口+AC),未来插槽(图谱/蒸馏)只画定性边界(签名+gate)。调和"充分彻底 vs 防 V4"。
- SOTA 还验证:七环节形态 = 量化系统标准分层(data→strategy→backtest→execution+feedback);分期锚定 **Strangler Fig**(新回测器官围绕 004 生长,每期独立可用);"各做各的"靠契约解决非靠大壳。
P3R1 预计只需收敛 2 点:(A) 回流 human-on-the-loop 的确切边界(哪些旋钮确认后可自动)；(B) 两档详略的确切清单(现建器官 vs 未来插槽)。SOTA 全文见 `P2-Opus47Max.md` §1。

## v2 是什么(和 v1 的区别 · 关键)

- **v1(已完成 · phase=done)**:回答"009 该不该建、怎么建"。verdict = 009 = 闭环集成契约规范 + 共享回测地基(非独立统一壳),回测 new-first 按 DSR/PBO,图谱 defer,蒸馏末位独立 lane,004 端永不权威综合分。
- **v2(本轮)= 画目标态蓝图专项**。operator 痛点:v1 出 verdict 后,004/008/四念头还是"各做各的、缺统一方向、架构不够充分彻底"。v2 产一张**闭环目标态架构蓝图**:final goal 全貌 + 器官边界 + 分期演化路线。**死守 v1 verdict 不推翻,蓝图 ≠ 一次性建完(防 V4)。**

## 怎么接手(立即可执行)

```bash
cd /home/ys/codes/ideababy_stroller
cat discussion/009/forge/v2/.forge-state.json   # 确认 phase=1, opus_done=true, codex_done=false
cdx-run 009                                      # 跑 Codex v2 P1(oneshot)
# 跑完后:
/expert-forge 009                                # 推进到 v2 Phase 2(自动 detect)
```

之后标准 forge 循环:P2(SOTA:目标态架构分层 + 分期演化 SOTA)→ 3R1 → 3R2 → Phase 4(synthesizer 产 stage-forge-009-v2.md)。**共还需 4 次 cdx-run。**

## v2 intake(速查 · 全文见 forge-config.md)

- **X(5 标的)**:v1 stage doc(蓝图地基)+ 004 PRD + 008 PRD + 004 strategy 代码 + ⭐**004 的 13 个 alembic migration**(v2 新增,补 v1 没读 DB schema 的盲区)。
- **Y(4 视角 · 为画蓝图定制)**:架构设计/目标态 · 可演化性/分期路线 · 器官边界清晰度 · 工程纪律。
- **Z**:对标 SOTA —— 投资闭环**目标态架构分层** + **分期演化路线** + 接口契约范式(**不重刷 v1 已做的回测方法论 SOTA**)。
- **W(3 件)**:refactor-plan(目标态模块图)+ free-essay(final goal 全貌)+ next-dev-plan(分期演化路线)。
- **收敛**:strong-converge(单一蓝图)。

## Opus v2 P1 关键发现(供你心里有数 · 全文见 P1-Opus47Max.md)

**读 004 DB schema 后的改变判断的发现:闭环"复盘/反馈"环所需字段,004 已埋好大半。** `decisions` 表已有 `would_have_acted_without_agent`(反事实字段 = calibration 头要的!)+ `post_mortem_json`(复盘回填槽)+ `env_snapshot_json`(决策时点快照)。`advisor_reports` = alpha 头输入源。`conflict_reports` DDL 明写"无 priority/winner/recommended 字段(R10)"= **v1 AC-1"永不权威综合分"有 DB 层背书**。

**但一个真缺口**:`advisor_reports` 没有 realized-return/价格结果列 —— alpha 头要"分析师方向 vs 之后真实股价",**必须新建一个价格历史/时序数据层**(004 只有决策时点单点价格,无连续序列)。这是蓝图必须画的**唯一关键新器官**。

**Opus first-take 蓝图骨架**:
- 器官清单:已有(008采集/strategy信号/004承诺壳/004复盘半槽)+ 新建(回测层=共享数据层+alpha头+calibration头,含新价格历史表)+ 未来插槽(图谱lane v2+/蒸馏lane末位)。
- 分期:M1 价格/as-of 数据层 → M2 alpha头(最先出"分析师行不行"数字·最独立可用)→ M3 calibration头 + 两条回流线 → M4(gated)图谱/蒸馏。
- **复盘/反馈环怎么闭合(v1 没画透)**:alpha 得分→回流调该分析师信号 lane 的 confidence 权重;calibration 得分→回流调承诺壳纪律阈值。这两条回流线 = 闭环的"反馈"环。

**Opus §3 三个最不确定点(留给 Codex/P2/P3)**:① 回流线该"自动调旋钮"还是"人确认后生效"(防 build runtime 静默定方向)?② 价格数据层范围(alpha 要日频序列 vs calibration 要事件驱动路径,是否同一张表)?③ 图谱/蒸馏插槽在目标态图里画多实才不 V4?

## ⚠ 接手注意事项

1. **git 全未提交**:009 整个目录(v1 全套 + v2 bootstrap)+ 008 forge v4 全套都未 commit。**operator 偏好 push/commit 前需他确认。**
2. **v1 已 done 并存档**:v2 不动 v1 目录,v1 stage doc 是 v2 的 X#1。
3. **cdx-run 是 oneshot**;P2/P3 任务标 reuse-session 省 token,但 cdx-run 不自动 reuse。
4. **X#4/#5 在 XenoDev 仓**:Opus 端已读 strategy + 关键 migration;Codex 沙箱不可达则用 forge-config §X-fallback 摘录,不 fake-read。
