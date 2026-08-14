---
forge_version: v5
created: 2026-08-14T09:16:53Z
convergence_mode: strong-converge
x_hash: 2bccb33924b07cd06dc7d32bd4d2146d
prefill_source: manual
fork_id: 009-pM3prime
trigger: 2026-08-14 IDS /handback-review 009 第 37 条 · T016 ship + 七条 obligation 在 forge:009-pM3prime:phase0 到期(-01/-10 结账 · -04/-05/-09/-11/-12 进本轮 X)
---

# Forge Config · 009-pM3prime · v5

**主题**:**绑定之后,到底绑在哪儿。**

前四轮的审阅对象依次是:v1 金标标注的**验收主体**、v2 那套验收的**测量效度**、v3 产出信号的**那台机器**、
v4 **这套治理机制自身**(条款、义务、gate 之间的传导)。

v4 的终裁是「**机制存在,但没绑定谁在何时做什么**」。
**v5 审的是它的下一层:绑定落空的五种方式。**

| 到期义务 | 落空方式 | 现场证据(IDS 2026-08-14 亲验) |
|---|---|---|
| `OB-...-v4-04` 校准监测周期 | **载体缺失** | 定形内容只活在 ledger 的 `evidence` 字段;`PRD.md` / `spec.md` / `SLA.md` 三处 grep **全零命中** |
| `OB-...-v4-11` census_run 消费点 | **消费者缺失** | 表已建、每跑落一行,**今天没有任何环节读它** |
| `OB-...-v4-05` 统计型重校准间隔 | **触发条件不可达** | 控制图要多点历史;本仓全部可用点 = 两跑 Jaccard 0.44 · J_1=0.4078 · 密度 41/73/71 ⇒ **画不出来** |
| `OB-...-v4-12` codex-review SKILL §4.2 | **选项集不完备** | 条款给三选项,实际发生的是**第四种**(修复后 ship 不复核) |
| `OB-...-v4-09` per-market 跨次分解 | **自我判据到期** | 其 note 自写「下次 firing 仍不处置 = 拖延」——**今天就是那个下次** |

> **本轮 gate 处置留痕**:`forge:009-pM3prime:phase0` 首查 **COUNT 7**。
> `OB-...-v4-01`(条款同步三处载体)与 `OB-...-v4-10`(三 gate 接线复核)经 IDS 现场逐处复核判为
> **结账型**(交付物 / 复核结论已在案),其余五条**过表 = 并入本轮 X**。
> warn gate 首查 **COUNT 0**(`WARN-c4` 已于 v4 defer 至 `forge:006:phase0`)。

---

## X · 审阅标的

### 本仓(✅ 可达)

1. `framework/obligations/ledger.jsonl`(本仓库文件 · 75 行 JSONL)
   - ★ **本轮五题的原文就在这里**。重点读 `OB-009-pM3prime-v4-04` / `-05` / `-09` / `-11` / `-12` 五条的
     **最后一行**(append-only,同 id 取末行),尤其看 `title` / `evidence` / `note` 三者说的是不是同一件事
     —— v4 第⑤题的形态(义务写标题、判据写 note)在本轮五条里**是否复发**,是免费的第一手观察。
2. `discussion/009/009-pM3prime/forge/v4/stage-forge-009-pM3prime-v4.md`(本仓库文件 · 268 行)
   - **前轮裁决,对本轮有约束力**。重点:#decision-matrix **#4 / #5 / #9** 三行 + **三条 v0.2 note** +
     §Verdict 的元条款「**本 verdict 自己不得犯它所诊断的病**」+ §underweights。
3. `discussion/009/009-pM3prime/PRD.md`(本仓库文件 · 666 行 · v1.1)
   - 推荐读取范围:**§6 科学重判触发条件 1 的「未满足注记」**(`-09` 的条款载体)/ §7 红线 3(C4 convert 判据四要件)/
     头部 v1.1 段(M1=pass 具名裁决 + 两项必载风险输入)。
4. `discussion/009/handback/HANDBACK-LOG.md`(本仓库文件 · 1952 行)
   - **只读第 37 条**(不必通读)。含本轮 gate 的直接前身:IDS 九项独立复核、F1(SKILL §4.2 第四选项)完整事实链、
     F3(gap ① 表述失真)、义务拆账明细表。第 36 条可选读(F2 口径两读的先例)。
5. `framework/warn-registry/README.md`(本仓库文件 · 119 行)
   - 只读 §「三态裁决」+ §接线状态表。**`-10` 的复核结论就绑在这张表上**:
     `xenodev:task-review` / `ship-gate` / `handoff-intake` 三条**仍全部 ❌ 未接线**。

### XenoDev-009 build repo(⚠ 外部 repo · Codex 沙箱可能 BLOCK —— 若 BLOCK 请在 §0 **显式声明**并改用下方 TEXT 块,**不要假装读过**)

6. `/home/ys/codes/XenoDev-009/specs/009-pM3prime/spec.md`(610 行)
   - `-04` **该回写而未回写**的候选载体之一。重点:§3 C4 行(convert 判据四要件已同步)· §4 **D-13**(M1=pass 裁决)·
     §6.3 Hard 契约→验收锚映射表。
7. `/home/ys/codes/XenoDev-009/specs/009-pM3prime/SLA.md`(154 行)
   - 同上,候选载体之二。重点:**E1「提取稳定性」行**(判据列现有三条 SELECT,第三条是 T016 新补的存在性判据)。
8. `/home/ys/codes/XenoDev-009/projects/004-pB/src/decision_ledger/extraction/aggregation_probe.py`(1321 行)
   - **`-09` 的落点 + `-11` 的数据面**。只看 `_run_batch` 的结果矩阵组装段 + `_persist_aggregation_probe_result` /
     `_mark_aggregation_probe_result_completed` 两阶段发布段。
9. `/home/ys/codes/XenoDev-009/projects/004-pB/alembic/versions/0023_add_census_run_and_aggregation_probe_result.py`(144 行)
   - `census_run` / `aggregation_probe_result` 两表 DDL。**`-11` 要定的「谁在何时读」,读的就是这两张表**。
10. `/home/ys/codes/XenoDev-009/.claude/skills/codex-review/SKILL.md`(548 行)
    - ★ **`-12` 的条款载体**。只读 **§4.2「4 轮上限」表格**(四行)+ 上下文。
11. `/home/ys/codes/XenoDev-009/specs/009-pM3prime/results/T015-aggregation-probe-result-20260813.json`(150 行)
    - 真实结果矩阵全文。⚠ **IDS 已实证 `grep -i market` 零命中** —— `-09` 说的「零 per-market 分解」属实。

---

### TEXT: `-04` 的载体缺失(IDS 2026-08-14 现场 grep · 沙箱 BLOCK 时的替代来源)

**ledger `OB-009-pM3prime-v4-04` 的 `evidence` 字段逐字**:

```
decision matrix #4(新增)。**已定形**:每个**被消费的批次**必测必落库;身份/口径变化
(模型 · system_fingerprint · 语料批次 · caliber_version)**立即**启动新基线;
**XenoDev 产证,IDS operator-chair 接受基线与升版**。
```

**IDS 现场核查(三处 grep 全零命中)**:

```
rg -n '监测周期|被消费的批次|必测必落库|立即启动新基线|新基线' \
   discussion/009/009-pM3prime/PRD.md                       → 0 hit
rg -n '监测周期|被消费的批次|必测必落库|新基线|v4-04' \
   XenoDev-009/specs/009-pM3prime/spec.md  SLA.md           → 0 hit
```

⇒ **一条已「定形」的周期义务,其全部正文只存在于 ledger 的一个 JSON 字段里。**
⚠ 请注意这与 v4 自己的元条款的关系:v4 裁定「本 verdict 自己不得犯它所诊断的病」,
而 `-04` 恰恰是 v4 亲手产生的、**没有条款载体**的裁决。

---

### TEXT: `-12` 的选项集缺口(条款原文 vs 实际动作 vs 相反先例)

**A · 条款原文**(`XenoDev-009:.claude/skills/codex-review/SKILL.md` §4.2 表格,逐字):

```
| 轮次      | verdict         | 处置 |
| Round 1-3 | needs-attention | 按 finding 改 impl · 重跑 |
| Round 4   | needs-attention | **hard-stop** · operator 决:接受 finding ship / 升级 forge / 退 task |
| 任意轮    | approve         | PASS · 进下游 |
| 任意轮    | fail closed     | hard-stop · operator 修 codex / SKILL |
```

**B · 实际发生的动作**(T016 hand-back §1/§2/§3 item 2):

```
round-4(1 high)修复后未再补跑第 5 轮(命中 SKILL §4.2 4 轮硬顶,operator 授权跳过)
…… 这是 XenoDev 侧 codex-review 治理内部的过程性决定 …… 不是审查门被绕开,
是 operator 在门内做出的显式决定
```

⇒ 走的是**「修复 finding 后 ship 且不复核」**,不在 A 的三选项内。
**区别是实质的**:「接受 finding ship」交付的是**已审代码 + 已知缺陷**;
本次交付的是**codex 从未看过的代码 + 缺陷据称已修**。四种走法里**只有这一种交付未审代码**。

**C · 相反先例**(`discussion/009/handback/HANDBACK-LOG.md` 第 34 条,逐字):

```
codex 超 SKILL §4.2 名义 4 轮上限属**持续收敛**(round 1-4 各修一个真问题)非卡死重复,可接受
```

⇒ 第 34 条把上限读成**名义**且可超;本次读成**硬顶**。而 T016 自陈「**单调收敛**,每轮暴露的缺口范围逐轮收窄」
——**正是 C 覆盖的情形**,却采了硬顶读,**且未标注这是一次口径选择**。

---

### TEXT: `-09` 的陷阱(成本近零 ≠ 结果有意义)

**PRD §6 科学重判触发条件 1 的要求**:产出**至少一个 per-market** 的跨次一致性读数。

**可用样本的真实分布**(PRD v1.0 §6 记载的三次密度普查,per-market):

```
US  40 / 73 / 65     ← 三次均 > 30
CN   1 /  0 /  2
HK   0 /  0 /  4
```

⇒ 分解成本确实近零(`trial_ledger` 本就是 `market×horizon` 9 行 grain,数据在库),
但 **US 一个市场分解出来大概能用,CN / HK 分解出来是不可解释的读数**。
而条件 1 的字面要求「**至少一个**」——**US 一个就字面满足了**。

⚠ **本轮真问题不是「做不做分解」,是「字面满足算不算满足」**;若算,条件 1 本身是个弱判据。

---

## Y · 审阅视角

- **工程纪律** —— 义务 / 判据 / gate 的传导链;裁决从 stage doc 到条款正文的落地路径;记账与消费的分工
- **测量效度 / 统计方法学**(自定义)—— 低样本量下的重校准间隔形态;分层 vs 汇总读数何时必须分解;
  「字面满足」与「统计有意义」的边界
- **规范工程 / policy authoring**(自定义)—— 条款**选项集完备性**(实际动作落在选项之外时怎么办)、
  审计数据的**消费者设计**(谁读、何时读、不读的后果)、具名敞口在触发条件不可达期间的存活形态

## Z · 参照系

**对标 SOTA** —— 双方各自检索,**零重叠为佳**。可检索面(非穷举,不必逐条照做):

- 决议 → **normative text** 的落地机制:RFC / PEP / Kubernetes KEP 怎么保证「会上定的」进入规范正文,
  以及它们对「决议已作出但正文未改」这一状态有没有名字与处理流程
- **分层 vs 汇总**指标:什么时候 pooled 读数必须分解到 stratum 才可用;stratum 样本量过小时的公认处理
- **低样本量下控制图的替代**:多点历史不足时,过程监控的其它形态(以及「什么时候不该用控制图」)
- **审计日志的消费者设计**:log-as-evidence vs log-as-exhaust;谁被规定必须读、读到什么必须停
- **未收敛评审的 escape hatch**:轮次硬顶 / 时间盒类机制在工业界如何处理「到顶但仍在收敛」

⚠ **禁**:tech-stack 深潜 / pricing / 实施细节。
⚠ 本仓语料已有 PEP 387 / RFC 1589 / NIST / OPA Gatekeeper / Chrome-Blink / KEP / ModSecurity /
RFC 5848 / RFC 9162 —— **不要只复述它们**;复述旧先例不计入本轮检索面。

## W · 产出形态

- **verdict-only** —— 五题各一个**可直接写回条款正文**的短裁决 + rationale(不要「建议考虑」式句子)
- **decision-list** —— 四列矩阵(保留 / 调整 / 删除 / 新增)+ **`obligation path` 列**(产生 gate → 消费 gate ·
  直接喂 Step 6.5 的义务登记)
- **refactor-plan** —— 按模块分组,落点具体到**文件与节**(哪份文档的哪一节 / 哪个文件的哪个函数)

## 收敛模式

**strong-converge** —— 必须 finalize 单一 verdict;残余分歧降级为 v0.2 note(**且必带 `due_gate`**,承 v4 元条款)。
理由:五条义务需要**可执行终态**,两条并存的裁决等于没裁。

---

## K · 用户判准

本轮**不重审 T016** —— 交付物已由 IDS 逐条实跑复证(全量 1304 passed 与自报逐字一致 ·
`review_log_sha256` 重算精确匹配 · SLA 新判据列与 DDL 逐列对得上 · round-4 修复的回归测试有齿)。
审的是**五条到期义务背后的同一件事:绑定落在哪儿。**

**① `-04`:定形了却没有条款载体。**
「每个被消费批次必测必落库 / 身份口径变化立即新基线 / XenoDev 产证、IDS 接受基线与升版」这套东西,
今天**只存在于 ledger 的一个 JSON 字段里**。我要的答案是:它该写进哪份文档的哪一节,
以及**为什么 v4 当时没写** —— **后半问比前半问重要。**

**② `-11`:审计表建好了,谁读?**
定出「**谁、在什么时点、读到什么就必须停下**」。
不要给我「建议在分析时参考」这种**没有主体**的句子。

**③ `-05`:触发条件不可达时,具名敞口该怎么活着。**
控制图画不出来是事实,**不许看数造 N**(承 forge v2「数字 vs 形态」判据)。
但「等数据够了再说」在本仓已被反复证明**等于消失**。
我要一个**在数据不足期间仍然产生行为**的形态。

**④ `-09`:per-market 分解,做还是不做。**
⚠ **陷阱先说破**:成本近零 ≠ 结果有意义。US 三次 40/73/65 分解出来大概能用;
**CN 1/0/2、HK 0/0/4 分解出来是不可解释的读数**。而 PRD §6 条件 1 字面只要求「至少一个 per-market」
——**US 一个就字面满足了**。
所以真问题是:**字面满足算不算满足?** 算,则条件 1 本身是个弱判据,该改;不算,则条件 1 该写成什么。

**⑤ `-12`:条款的选项集不覆盖实际发生的动作。**
SKILL §4.2 给三选项,实际走了第四种(修复后 ship 不复核);而本仓 HANDBACK-LOG 第 34 条
又确立过「持续收敛可超上限」的**相反先例**。
给一个**能写回 §4.2 表格**的答案,并说明**跨仓怎么送过去**(条款载体在 XenoDev,裁决场在 IDS)。

**不许动的**:
- M1=pass **不解锁扩样与 E2**(forge v3 §237 红线 + v4 D-13 一致)
- 41 条盲标路 v0.1 **CLOSED 不重开**
- 不改 C6 冻结门槛**数字**(形态可议,数字不动)
- **不当场改** producer / validator / SHARED-CONTRACT schema(框架级变更走 forge 006)

**元层(第⑥题 · 不占 W 配额 · 写进 verdict rationale)**:
v4 已认定「**本 verdict 自己不得犯它所诊断的病**」。
**本轮请对 v5 自己的产出做同样的检查** —— 你们给出的每一条裁决:
**载体是什么 · 消费者是谁 · 触发条件可不可达 · 选项集全不全。做不到就别写那条。**

🔴 **回声室警告(binding · 第五轮)**:
本 fork 的 P1 已**连续四轮**逐条同姿态收敛(v2 / v4 都是靠 P2 零重叠检索才破的)。
本轮要求:**P1 §2 每人必须给出至少一条「我判 X,但我预期对方会判 Y」的具名预测。**
P1 交换后若两人的预测**都落空**(即又是逐条相同),**本轮 P1 直接按回声处理,不得作为收敛证据**。

⚠ **另**:T016 hand-back 把 `-04` 相关的 gap 说成「无拦截**或留痕**」,而留痕恰是它**自己交付的**
(`census_run.declared_sample_size`,读任何 record 之前写入 · 见 HANDBACK-LOG 第 37 条 F3)。
**这是本 fork 第一例保守方向的失真**(此前六轮的失真几乎全在乐观方向)。
如果你们认为**保守方向的失真与乐观方向的失真需要不同的治理动作**,在 verdict 里说;
认为一样,也明说 —— **不要沉默带过。**
