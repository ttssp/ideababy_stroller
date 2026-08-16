# XenoDev-009 启动 prompt · forge v5 落地 · 模块 C(跨仓授权)

> **用法**:在 XenoDev-009 session 的**第一条消息**里贴下面「启动 prompt」整段(或让 agent 读本文件全文)。
> 本文件是 **IDS 侧产物**(forge v5 的跨仓落地授权),XenoDev 侧**只读不改**。
> **模块 A + B(IDS 侧)已于 `6f9a9a9` 落地**;本文件只含模块 C。

---

## 启动 prompt(从这里开始复制)

你在 `XenoDev-009` build runtime,分支 `feat/009-spec`。本次任务 = 落地 **IDS forge 009-pM3prime v5 verdict**
的 **模块 C(XenoDev 跨仓部分)**。

### 本轮 verdict 的一句话(先建立框架,再看交付物)

**五条到期义务是同一个病灶:完成全部定义在产生侧,从未走到「谁在何时读到什么、必须做什么、拿什么结账」。**
统一裁决形态 = **七问消费契约**:`normative_site`(载体**及其等级**)· `owner` · `trigger`(**可达**)·
`options`(**程序全定义**:known + unclassified → 具名解释者 → 留痕复审,**未分类不得自动通过**)·
`clock_or_reachable_event`(**两者皆无 ⇒ 受影响消费点 fail-closed,不伪造到期日**)·
`consumer_action` · `settlement_evidence`。

### 授权来源(**不重开已决问题,逐条照做 —— 这是本次的合同**)

1. `/home/ys/codes/ideababy_stroller/discussion/009/009-pM3prime/forge/v5/stage-forge-009-pM3prime-v5.md`
   —— **先通读**。重点 §Verdict / §Decision matrix / §Refactor plan 模块 C / §What this menu underweights
2. `/home/ys/codes/ideababy_stroller/framework/obligations/ledger.jsonl`
   —— 读 `OB-009-pM3prime-v5-08` / `-09` / `-10` / `-13` 四行(**兑现判据写在各自 `note` 里**)
3. `/home/ys/codes/ideababy_stroller/discussion/009/009-pM3prime/PRD.md` **v1.2**
   —— §6「条件 1/2 量词改写」+「低样本市场的显式状态」+「跨批读数的消费契约」· §7 红线 3 的两块新增

⚠ **IDS 已裁决的事不要重新论证**;若你认为某条裁决有问题,**记 hand-back 交回 IDS,不要当场改**。

---

### 交付物 ① `OB-009-pM3prime-v5-10` —— per-market 观测轴(**本次最大的一项**)

**病灶(IDS 与 Codex 两侧独立复证)**:同一条 pipeline 的**两条链分层粒度不同** ——
`census.py` 的密度链**逐 market 判**(`density_by_stratum` / `density_all_by_stratum` 以 market 为键;
`meets_threshold` = 每 market 的 strong 下界 ≥ 阈值;`below_threshold_advisory` = 有 market 连上界都 < 阈值),
而 `aggregation_probe.py`(1321 行)**全文只有 `:744` 一处 `market` 注释**,`_run_batch` **零 market 轴**。

⇒ PRD §6 条件 2(per-market 噪声量级 < **该市场**的密度阈值裕度)**在当前实现下不可计算**。
🔴 **这不是数据缺** —— `derive_stratification_market` 就在 `census.py` 里;
**是两条链的分层粒度不同。改措辞补不出来。**

**依据(forge v5 十二个参照体系中唯一被判「忠于原体系」的跨界引用)**:
BCBS 239 —— **分层可得性是「汇总能力」定义的一部分**,汇总的同时必须保持按相关维度可分解,例外须解释;
而本仓 PRD §6 条件 2 已把 market 指定为**相关轴**。

**交付**:
1. `projects/004-pB/src/decision_ledger/extraction/aggregation_probe.py::_run_batch` 结果矩阵组装段
   —— **新建 market 观测轴**,产出 per-market 的跨次一致性读数;
2. **CN / HK 输出 `not_estimable`**(不是 0、不是 null、不是省略)——
   见 PRD §6「低样本市场的显式状态」三档表(可用 / 复审 / `not_estimable`);
3. `specs/009-pM3prime/SLA.md` **E1 行判据列**增一条**可 `SELECT`** 的 per-market 读数判据
   (承 `OB-...-v4-08` 的形状:目标列陈述要求而判据列验证更弱的东西 = 假绿的同一形状);
4. 相应回归测试。

🔴 **只给形态,不给数字。** **不得**在本次实现里引入任何 per-market 的样本量阈值 / 档位数字 ——
forge v5 P3R2 检验已判定:把外部统计标准(NCHS 比例呈现标准)的**精确档位或阈值直接移植属过度外推**,
可移植的只有「**分市场判 + 低样本显式状态 + 具名判定人**」这一形态。**判定人 = IDS operator-chair。**

⚠ **成本未实测(`OB-...-v5-13`)**:IDS 侧 P1 §3 已自曝**未读 `derive_stratification_market` 实现**;
若它需要回查 `collection.db` 字段,成本会比 IDS 预判高一档。**若实测成本显著高于预期 ⇒ 停下记 hand-back,
不要硬做**;这正是 v0.2 note 3 预留的分支。

---

### 交付物 ② `OB-009-pM3prime-v5-08` + `-09` —— `codex-review/SKILL.md` §4.2 逐字替换

🔴 **两条必须同批落,不得只落其一** —— **只删不加留真空,只加不删留两读。**

**背景**:条款给三个选项,而 T016 实际走的是**第四种(修复后 ship 不复核)**;
同时 HANDBACK-LOG **第 34 条**又确立过「持续收敛可超上限」的**相反先例**。
双方 P3 收敛于 **B 侧的二分**:**语义状态不可穷举(不可能)≠ 决策程序不可全定义(可能且必须)**。
(A 侧 P3R1 曾主张「完备性不是目标」,P3R2 **完全让步并自认错** —— 那个表述有一个危险读法 = 放弃 fail-closed。)

**替换目标**:`.claude/skills/codex-review/SKILL.md` §4.2「4 轮上限」表格。

**替换后的表格(逐字)**:

```
| 轮次       | verdict          | 处置 |
|------------|------------------|------|
| Round 1-3  | needs-attention  | 按 finding 改 impl · 重跑 |
| Round 4    | needs-attention  | **hard-stop** · operator checkpoint,见下「Round 4 的四个动作」 |
| 任意轮     | approve          | PASS · 进下游 |
| 任意轮     | fail closed      | hard-stop · operator 修 codex / SKILL |
| **任意轮** | **未落入以上任一格** | 🔴 **catch-all:fail-closed。不得自动通过。** 见下「catch-all 程序轴」 |
```

**紧随表格之后新增两段(逐字)**:

```
#### Round 4 的四个动作(operator checkpoint · 四选一)

1. **接受未改的已审 finding 后 ship**;
2. **修复后 ship** —— 合法,但**必须同时携带三件,缺一即回落 catch-all**:
   ① **授权人身份记录**(谁批准的,具名);
   ② **修后强制复验** —— 验证轮**不受名义四轮帽**约束,持续收敛可签续;
   ③ **`clock_or_reachable_event`** —— 到期时钟或可达事件;**两者皆无 ⇒ fail-closed,不得伪造到期日**;
3. **升级 forge**;
4. **退 task**。

🔴 **删除「四轮硬顶即终局」这一读法。** 它与 HANDBACK-LOG 第 34 条「持续收敛可超上限」的先例冲突,
且当时未标注这是一次口径选择 —— 两读并存本身就是缺陷。
**四轮上限约束的是 `needs-attention` 的重跑轮次,不约束修复后的验证轮。**

#### catch-all 程序轴

**语义状态不可穷举,但决策程序必须全定义。**
- 已枚举的动作 → 按上表处置;
- **未枚举的动作 → `unclassified`,默认 fail-closed,不得自动通过**;
- `unclassified` 的唯一合法出路 = ① **具名解释者签署** ② **理由留痕** ③ **事后复审**。

**为什么不是「补第四行」**:补一行只堵这一个格子。工业先例(NRC 10 CFR 50.59 的
「八类变化须实施前取许可、其余也须保存书面判断依据」· W3C Process 的「实质改动须重走条件」)
都把「**后续变化是否需要重新授权**」与**原 decision 分开成独立轴**;
ISO 9001 §8.7 要求放行不合格输出必须**记录授权人身份**、返工后须由**适当权限者 revalidation**;
航空 MEL 则给出**修复时限分档 + 时钟自发现次日零点起 + 条件式放行**。
⇒ **时钟是 IDS 与 Codex 双方 P1 都漏掉的一整维,本条补上。**
```

---

### 交付物 ③ 载体等级同步查证(**先裁级,再决定动不动 —— 不预设镜像**)

IDS 已裁定 `-04`(**校准监测周期**:每个被消费批次必测必落库 · 身份/口径变化立即启动新基线 ·
XenoDev 产证 / IDS operator-chair 接受基线与升版)的**载体等级 = `codified`**,正文落点 = IDS `PRD.md` §7 红线 3。

🔴 **本次不预设「三处镜像」** —— 该预设动作已被 forge v5 decision matrix **#10 裁掉**。
请**逐项查证并给结论**(需要同步 ⇒ 同步;不需要 ⇒ **写明理由**):

1. `specs/009-pM3prime/spec.md` **C4 行** —— 是否需要承载 `-04` 的监测周期?
2. `specs/009-pM3prime/SLA.md` **E1 行** —— 是否需要承载 `-05` 的三态
   (`insufficient_history` / `method_ready` / `recalibration_due`,**每态各绑 {允许方法, 已知敞口, 退出证据}**,
   `insufficient_history` **必载** 自启动图族前 ~50 点的 masking 敞口)?

**载体等级三值**(本仓当前取值,**非外部强制**):`codified`(入正文)/ `note`(留账本 + 挂映射)/
**`explicitly-uncodified`(显式裁定不入正文,仍然合法)**。三者都必须**显式、可发现、可消费**。
🔴 **不强制固定三级标签** —— forge v5 P3R2 判「必须采用固定三级标签」属**过度外推**。

---

### 冻结项(**不许动**)

- 扩样与 **E2 继续 blocked**;`M1 = pass` **不解锁**
- **41 条盲标路 v0.1 CLOSED**,不重开
- **C6 冻结门槛数字**不动 · `caliber_hash` / `threshold_hash` / `density_threshold` 不动
- **CN/HK 执行态 `STOP` 与认识态 `UNKNOWN` 均不变** —— `not_estimable` **既不是 `STOP` 的新理由,
  也不是撤销 `STOP` 的理由**,它只报「测不了」
- 红线 4(第二源资格)不动 · `gold_layer2.py` 的 `second_source_kind != 'human'` 硬挡不动
- **不改 producer / validator / `framework/SHARED-CONTRACT.md` schema**(框架级变更走 forge 006)
- **不改 IDS 仓任何文件**(有意见走 hand-back)

### 验收

- `cd projects/004-pB && uv run pytest` —— 全量回归绿,**0 回归**
  ⚠ **基线请先自行实跑确认**:IDS 最近一次复证是 **1304 passed**(2026-08-14 · HANDBACK-LOG 第 37 条 · T016),
  **不要直接照抄这个数字当基线** —— 先跑一次拿到当前真值再开工
- `uv run ruff check <改动文件>` —— clean
- 四项交付物各自的兑现判据(见 ledger 各行 `note`)逐条可 `SELECT` 或可 `pytest` 验证
- codex adversarial-review(`risk_level: high`);**真路径**,非 fallback

### hand-back 要求

1. 🔴 **frontmatter 必须含拓扑自证三字段** `current_idea` / `worktree` / `baseline`
   (KG-B21:producer `gen-handback.sh` 未修,**请手工补齐**;缺失会让 validator 的 check-7 静默 skip 并输出假陈述)
2. 🔴 **`ids_verdict_evidence` 父键必须产出**,且 `review_log_path` / `review_log_sha256` 与
   `.claude/skills/codex-review/REVIEW-LOG.md` singleton 及 immutable `real-review/` 记录**三处一致**(KG-B20)
3. §3 建议里分别标注:哪几条**要 IDS 决议**、哪几条是**信息式收悉**
4. 🔴 **本次特有**:若交付物 ① 的实测成本显著高于 IDS 预判(见 `OB-...-v5-13`),
   **在 hand-back 里明写实测数字**;若因此未做完,**明写未做完而不是降级表述**

### 已知陷阱

- 真实验若涉及 LLM:`env -u ALL_PROXY -u all_proxy`(runbook 记录的 SOCKS 代理坑)
- validator 必须传**绝对路径**(相对路径会误判 corruption)
- 本次**不需要**跑真实验;三项交付物都是代码 / 契约 / 文档层

### 🔴 本轮 verdict 自己承认的敞口(**你不需要解决,但不许在 hand-back 里说它已解**)

1. **KG-42 同族未解** —— 七问的 `owner` 与「复审的独立性」在**只有一个人的仓**里不可同时满足。
   双方一致签署「**不解 + 具名敞口**」。跨模型 / 跨会话时间分离 / operator 独立签收
   **只算功能性缓解,不满足人员独立**。⚠ 同时:「复审主体必须与 owner 人员分离」本身
   **已被判过度外推**(适航标准的独立性随安全保证目标成立)⇒ **也不得反过来把它当硬要求倒逼**。
2. **三个 `xenodev:*` gate 仍全部未接线** ⇒ 本轮交付物 ①②③ 对应的义务
   (`due_gate` = `xenodev:task-review` / `xenodev:ship-gate`)**登记了也不会被任何机制消费** ——
   `exposure` 已在 ledger 逐条写明。**本次交付不改变这一事实。**
3. **零 build 侧实证(连续第三轮)** —— market 轴、catch-all 行能否实装,IDS 侧**全是推演**,
   且本轮**未预置同轴熔断**(不像 v4 的「证不出则 fallback」)。⇒ **你这一侧的实证是最后防线;
   证否比证成更有价值。**

## 启动 prompt(到这里结束)

---

## Operator 执行命令

```bash
cd /home/ys/codes/XenoDev-009 && claude
```

首条消息:

```
读 /home/ys/codes/ideababy_stroller/discussion/009/009-pM3prime/forge/v5/XENODEV-startup-v5-C.md
的「启动 prompt」整段,按它执行。
```

⚠ **worktree 规约**:`XenoDev-009` 已是 009 专用 checkout(分支 `feat/009-spec`),
**不需要**再 `claude -w`;直提交到 `feat/009-spec` 是本 fork 既有惯例(非 worktree+squash 流程)。
