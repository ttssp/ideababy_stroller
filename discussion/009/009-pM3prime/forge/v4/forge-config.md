---
forge_version: v4
created: 2026-08-14T03:20:00Z
convergence_mode: strong-converge
x_hash: 78ce6018a241b92450b93ce7a09a3a62
prefill_source: manual
fork_id: 009-pM3prime
trigger: 2026-08-14 IDS /handback-review 009 第 36 条 · T015 M1=pass + 四条 obligation 在 forge:009-pM3prime:phase0 到期
---

# Forge Config · 009-pM3prime · v4

**主题**:**治理结论写下来之后没有产生行为** —— 本轮不审 M1 结果对不对(数字已由 IDS 逐条实跑复证属实),
审的是**四条到期义务背后的同一个形态**。

前三轮的审阅对象依次是:v1 金标标注的**验收主体**、v2 那套验收的**测量效度**、v3 产出信号的**那台机器**。
**v4 审的是这套治理机制自身 —— 条款、义务、gate 之间的传导。**

---

## X · 审阅标的

### 本仓(✅ 可达)

1. `discussion/009/handback/20260813T155648Z-009-pM3prime-20260813T155648Z.md`(本仓库文件 · 119 行)
   - ★ **本轮触发源**。推荐读取范围:**全文**。重点 §1(M1/M2/M3 真实结果 + 硬上限)/ §2 三段(codex 9 轮 · T014 两条残留 finding 的归属主张)/ §3 四条 suggested action
2. `discussion/009/handback/HANDBACK-LOG.md`(本仓库文件 · 约 1700 行)
   - **选读第 35 条与第 36 条**(不必通读)。第 35 条 = 两条残留 finding 并入 OB-07 的原始裁决 + KG-B20/B21;
     第 36 条 = 本轮 gate 的直接前身,含 F1/F2 完整事实链与 IDS 侧独立实跑复证记录
3. `discussion/009/009-pM3prime/forge/v3/stage-forge-009-pM3prime-v3.md`(本仓库文件 · 约 320 行)
   - **前轮裁决,对本轮有约束力**。重点:§「⚠ 接受本项即同时接受」(第 277 行)/ #decision-matrix 聚合探针行(第 163 行)/
     §探针实验契约的**结果矩阵表**(第 204-210 行)/ **v0.2 note 2**(第 238 行 · 校准周期与升版责任)/ §underweights
4. `framework/obligations/ledger.jsonl`(本仓库文件 · 53 行 JSONL)
   - 读 `OB-009-pM3prime-v3-07` 的**两行**(pending 行与 2026-08-14 satisfied 行)+ `-09` / `-13` / `-15` / `-16`。
     ★ **条款歧义的另一半载体就在这里** —— 同一条义务的**标题**与 **note** 说的不是一回事
5. `discussion/009/009-pM3prime/PRD.md`(本仓库文件 · v1.0)
   - 推荐读取范围:§7 红线 3(C4 改形态 · `pass_semantic: none`)/ §6 停止条件与 E2 两 lane / §4-E1 block (p)
6. `framework/warn-registry/README.md` + `framework/warn-registry/validate-warn-class.sh`(本仓库文件)
   - ★ 只读 README §「三态裁决」与 validator 第 112-118 行。**本轮 intake 现场撞到的机制洞在这里**(见下方 TEXT 块 D)

### XenoDev-009 build repo(⚠ 外部 repo · Codex 沙箱可能 BLOCK —— 若 BLOCK 请在 §0 **显式声明**并改用下方 TEXT 块,**不要假装读过**)

7. `/home/ys/codes/XenoDev-009/specs/009-pM3prime/tasks/T015.md`
   - 重点:§「5. T014 残留 finding 处置」(defer 论证原文)/ §「codex round-9」/ §设计决策 D9 / §真实验执行
8. `/home/ys/codes/XenoDev-009/specs/009-pM3prime/results/T015-aggregation-probe-result-20260813.json`
   - 真实结果矩阵全文(机器可读)。⚠ 注意 `per_run_summary` 里 6 个跑的 `census_verdict`
9. `/home/ys/codes/XenoDev-009/projects/004-pB/src/decision_ledger/extraction/census.py`
   - 只看 `_persist_attempt_log` 与 `trial_ledger` 落库路径 + 连接管理/事务边界 —— **OB-15 的病灶面**
10. `/home/ys/codes/XenoDev-009/specs/009-pM3prime/spec.md` §6.3 映射表 + `SLA.md` E1「提取确定性」行
    - C4 三处同步 site 之二(第三处是本仓 PRD §7 红线 3)

---

### TEXT: 条款歧义的四处载体(逐字原文对照 · 沙箱 BLOCK 时的替代来源)

> 以下均为 2026-08-14 从本仓与 XenoDev-009 工作副本逐字抄出,**非转述**。

**A · forge v3 正文(stage-forge-009-pM3prime-v3.md:277)——「广读」**

```
⚠ 接受本项即同时接受:探针在五项前置未落地前**不启动**,且其结果三态**必须**回到 forge v4 裁决。
```

**B · forge v3 decision matrix 聚合探针行(同文件 :163)——「广读」**

```
| **聚合探针 task**(端到端唯一入口 + 配对 Δ bootstrap + 硬上限 + 结果矩阵) | 新增 | `new` |
详见 §探针实验契约;**accept-with-fixes**,五项修复未落地不得启动 | `post-hoc-accepted` |
`forge:009-pM3prime:v3:phase4 → **forge:009-pM3prime:phase0**`(结果三态须在下轮 intake 裁决 · **已接线**) |
```

**C · forge v3 结果矩阵表(同文件 :204-210)——「窄读」**

```
| 结果 | 处置 |
|---|---|
| `M1 = fail` | **触发 forge v4 议路线**;M2/M3 仍全量申报 |
| `M1 = indeterminate` | **同样触发 forge v4**(不得当作「再跑跑看」) |
| `M1 = pass` · `M2 ≥ 50%` | 只证明**本批**信度改善;**不证明效度、不外推、不解锁 E2** |
| `M1 = pass` · `M2 < 50%` | 同上,**并加注候选损失**;…… |
```

**D · `OB-009-pM3prime-v3-07` 的标题 vs note(ledger.jsonl)—— 同一条义务内部打架**

```
title: 聚合探针 task:端到端唯一入口 + record-level 配对 Δ bootstrap + 四类硬上限 + 结果矩阵;
       **结果三态必须回 forge 裁决**                        ← 广读
note:  ……**M1=fail 或 indeterminate ⇒ 触发 forge v4**;
       M1=pass 亦不代表效度成立、不外推、不解锁扩样/E2。      ← 窄读(pass 行只写"不解锁",未写"欠裁决")
```

⇒ **同一份 forge 产物 + 同一条 ledger 义务内,「三态皆欠裁决」与「仅 fail/indeterminate 欠裁决」并存。**
T015 hand-back §3 action #2 采了窄读(「M1=pass **不**自动触发任何操作」)**且未标注这是一次口径选择**。

---

### TEXT: T015 §5 的 defer 论证(逐字原文 · OB-15 的直接对象)

> **IDS 第 35 条的并入理由**(ledger `OB-...-07` 2026-08-13 追加行):

```
⇒ 两条**均为本条跨批次比对的前置**,故并入而非另起。**本条仍 pending,仍受 OB-...-12 排序在前的约束。**
```

> **T015.md §5 的 defer 理由**(XenoDev-009 · 节选逐字):

```
本 task(OB-07)自身的 6 次真跑运行时间短(硬上限 ≤3.5h,单跑 ≤35min)、由本 session 操作者全程盯着
跑(非无人值守的长期批处理),SIGKILL/OOM 中途崩溃的概率窗口极小……不阻塞 OB-07 的统计目标。
……
本 task 的 6-8 次尝试全部发生在同一 session、针对同一个只读 `collection.db` 文件……故"语料在两次尝试
之间漂移"这个风险在本 task 的操作条件下概率视为零……
……
两条 defer 均**不影响** OB-07 本身的统计设计与硬上限执行
```

⚠ **请注意两段论证的谓项**:IDS 说的是「**跨批次比对**的前置」,T015 答的是「**本批**统计正确性 / 本 task 的操作条件」。
**本轮要的是对前者的回答。**

---

### TEXT: 本轮 intake 现场撞到的机制洞(warn registry · 与议题④直接相关)

**README §「三态裁决」原文**:

```
defer    → 合法!但必须:① 具名签署 ② 写明理由 ③ 给出新的 due_event
**被遗忘的 defer 不是 defer,是缺席。** 这是本 registry 存在的全部理由。
```

**validator 实际到期判据(validate-warn-class.sh:114-115)**:

```python
hits = [r for _, r in rows
        if r.get("warn_class") == "temporary" and r.get("due_event") == due_gate]
```

⇒ 判据**不含「是否已裁决」状态**。而 fork 域 warn 唯一接线的消费 gate 就是 `forge:<id>:phase0` 本身
⇒ **把新 due_event 指回它 = 立即再次到期 = 永久阻断**;指向 `forge:<id>:v<N>:phase4` 则**永不被消费**
(那是 admission gate,Step 6.5 只跑 schema 校验)。
⇒ **对 fork 域 `temporary` warn,「给出新 due_event 的 defer」在当前机制上不可表达,只剩 convert / revert / 降 soft 三条路。**
本轮的处置是把 `WARN-c4-extraction-stability-report-only` 的 due_event 改指 `forge:006:phase0`
(沿用 README 自己对现存三条 warn 的先例),**已知代价 = 场地错配**:fork 域语义搬到框架场裁。

⚠ 这条**不是**本轮 forge 要修的东西(框架级变更走 forge 006),列在此处是因为它是议题⑤「同一形态还有没有」的**第二个现场实例**。

---

## Y · 审阅视角

- **工程纪律** —— 义务 / 判据 / gate 机制、条款歧义、评审与记账链的传导
- **架构设计** —— OB-15 的跨批次比对基础设施(写穿透 vs 单原子事务哲学、内容哈希绑定的粒度矛盾)
- **测量效度 / 统计方法学**(自定义)—— 校准周期的方法学依据、report-only → gate 的升级判据形态、信度 vs 效度的边界

## Z · 参照系

**对标 SOTA** —— 双方各自检索,零重叠为佳。可检索面(非穷举,不必逐条照做):

- 多数票 / k-of-n 聚合对标注信度与**效度**的分别影响,及其边界
- 标注器 / 抽取器**校准周期**的方法学依据(多久重标、什么触发重标、责任归属)
- `report-only` → **强制门**的升级判据形态(本仓语料已有 PEP 387 / RFC 1589 两个先例,**不要只复述它们**)
- 跨批次比对所需的 **provenance 记账**最小充分集(崩溃窗口审计 / 语料内容身份绑定)

⚠ **禁**:tech-stack 深潜 / pricing / 实施细节。

## W · 产出形态

- **verdict-only** —— 四题各一个**可写回条款正文**的短裁决 + rationale
- **decision-list** —— 四列矩阵(保留/调整/删除/新增)+ **obligation path 列**(直接喂 Step 6.5 的义务登记)
- **refactor-plan** —— 按模块分组:OB-15 的写穿透/哈希绑定落点、校准周期的落地面、C4 三处同步 site

## 收敛模式

**strong-converge** —— 必须 finalize 单一 verdict;残余分歧降级为 v0.2 note。
理由:四条义务需要**可执行终态**,两条并存的裁决等于没裁。

---

## K · 用户判准

本轮不是重审 M1 结果对不对(数字已由 IDS 逐条实跑复证属实:1287 passed 逐字一致、结果矩阵内部算术自洽、
`review_log_sha256` 精确匹配、预注册在实验前定稿零改动)。审的是**四条到期义务背后的同一个形态:
治理结论写下来之后没有产生行为。**

具体四题:

**① M1=pass 的三态裁决 —— pass 到底欠不欠一次显式裁决?**
forge v3 正文 + decision matrix + ledger 标题说「三态必须回 forge」;note + 结果矩阵表只写
「fail/indeterminate ⇒ 触发 v4」。我要一个**能写回条款正文的答案**,不要「两种读法都有道理」。
顺带把这次的 M1=pass 真裁了 —— 三态裁决本身也是这轮欠的动作。

**② OB-15 —— 没有那两条,跨批次比对是否可信?**
T014 两条残留 finding(进程崩溃窗口丢审计 [high] / 失败批次无法绑定语料内容身份 [medium])。
问题是:**在没有它们的前提下,未来任何跨批次(41 / 73 / 71 ↔ 聚合语料)的失败率比对是否可信。**
这是 IDS 第 35 条并入时的原题;T015 §5 答的是「本批统计正确性」—— **别再答那一题**。

**③ OB-09 —— 校准周期 + 责任人 + 升 `caliber_version` 的触发条件。**
这是我的原始要求(「接受结果含一部分提取器误差,**前提是有定期校准机制**」),v3 只定了测量的**义务与形态**,
周期与责任未定,双方 §4 自检当时均判 ⚠。M1 刚好给出第一个真实噪声基线:单跑两两 Jaccard **J_1 = 0.4078**。

**④ C4 warn 的 convert 判据形态。**
`WARN-c4-extraction-stability-report-only` 已于本轮 defer 到 `forge:006:phase0`。
下一场要用一个**判据形态**来裁它 —— **给形态,不要给数字**(看完结果再定数字 = 移动球门,PRD §7 (f) 已有判据)。

**不许动的**:
- M1=pass **不解锁扩样与 E2**(forge v3 §237 红线 + 本 hand-back §1 自陈一致)
- 41 条盲标路 v0.1 **CLOSED 不重开**(第 33 条三前提全塌;重开须 KG-42 真解 + 全新批次先盲标后提取 + v1.0 显式授权)
- 不改 C6 冻结门槛**数字**(形态可议,数字不动)

**我要你们特别盯的元层(第⑤题,不占 W 配额,写进 verdict rationale 即可)**:
**「义务写在标题、判据写在 note,两者不一致时被执行的永远是更弱的那一方」这个形态,在 009 的其它条款里还有没有。**
今天已经现形两处:(a) `OB-...-07` 标题 vs note;(b) warn registry README 说 defer 合法而机制不可表达。
**我要的是第三处、第四处,不是对这两处的复述。**

**回声室警告(binding)**:本 fork 的 forge v1 / v2 / v3 **连续三轮零分歧强收敛**,v2 是靠 P2 双方零重叠检索
各自推翻自己 P1 才破的。P1 若又同姿态收敛,**请当成警报而不是信号**;P2 的检索面务必各走各的。

**另**:hand-back §1 通篇未提「6 个跑的 `census_verdict` **全部** `below_threshold_advisory`」(字段在结果 JSON 里)。
我已记为取景遗漏。如果你们认为这对下游有实质影响(密度是 E2 的闸门变量),在 verdict 里说;
如果认为无实质影响,也明说 —— **不要沉默带过**。
