# Forge v5 · 009-pM3prime · P1 · GPT-5.6-Sol xhigh · 独立审阅(no search)

**Timestamp**: 2026-08-16T00:05:17+08:00  
**Searches used**: NONE in this round.  
**Visibility**: I did NOT read other reviewer's P1.  
**Reviewer stance**: 审阅人——评判已存在物，不是 daydream。

## 0. 我读到的标的清单 + 阅读策略

1. ✅ `ledger.jsonl`：五条末行及 `-01/-10` 结账行。
2. ✅ v4 stage：矩阵 #4/#5/#9、三条 note、元条款与 underweights。
3. ✅ `PRD.md`：v1.1 头部、§6 三条件与未满足注记、§7 红线 3。
4. ✅ `HANDBACK-LOG.md`：第 37 条（并回看相反先例第 34 条引文）。
5. ✅ warn README：三态裁决与五个 gate 的接线表。
6. ✅ XenoDev `spec.md`：C4、D-13、§6.3。
7. ✅ XenoDev `SLA.md`：E1 提取稳定性行。
8. ✅ `aggregation_probe.py`：结果组装、两阶段发布；独立全文查 `market` 仅命中 grain 注释。
9. ✅ migration `0023`：两表 DDL。
10. ✅ `codex-review/SKILL.md`：§4.2 表及上下文。
11. ✅ T015 JSON：全文；六跑 verdict 全低，零 per-market。

**K 摘要**：五题分别要补载体、消费者、可达触发、完整选项与到期处置；每条答案还须自证“载体、消费者、触发可达、选项完备”。不得松动 M1/E2、盲标路、C6 数字，也不得当场改框架 schema。  
**阅读策略**：先核对“标题—证据—note—真实消费边”，再区分统计上可计算、可解释与可用于重判。

## 1. 现状摘要（按 Y 三视角）

### 工程纪律

v4 矩阵 #4 已写周期与责任，却未进入 A/B/C 任一 refactor 组；Step 6.5 只把它搬进 ledger。最新五条又以 `satisfied` 表示“已上议程”，`consumer_wired:true` 表示本地 forge gate 可消费账目，不等于正文或业务消费者存在。标题、状态与 evidence 再次承载不同语义。

### 测量效度 / 统计方法学

现有历史不足以画控制图；T015 只有全局 Jaccard。US 三次 40/73/65 尚可形成分层读数，CN 1/0/2、HK 0/0/4 只能报告不可估，不能把计算出的数当解释。PRD §6 位于“CN/HK 改判”语境，却允许“至少一个市场”，因此 US 可字面解锁与它无关的 CN/HK。

### 规范工程 / policy authoring

`census_run` 在读 record 前写声明窗口，`started` 留删失；`aggregation_probe_result` 以 pending→completed 发布，但当前没有审阅 gate 读取。§4.2 把第四轮写成三选一，实际既有“持续收敛继续审”先例，也发生“修后不复核”，开放世界动作超出封闭表格。

## 2. First-take 评分（五题 + 元层）

| 题 | 倾向 | first-take 与理由 |
|---|---|---|
| `-04` | **refactor** | 权威正文落 `PRD §7 红线3`，镜像到 `spec C4` 与 `SLA E1`；每个被消费批次由 XenoDev 产证，身份变化时 IDS operator-chair 只能“接受新基线 / 拒绝消费”。v4 漏写不是抄送疏忽，而是矩阵 #4 没有到 refactor plan 的全量映射。 |
| `-11` | **new** | 消费者定为 IDS operator-chair；每次 `/handback-review` 在引用跨批失败率、密度或一致性前读取相关 `census_run`。库不可读、引用跑无行、删失未披露、同 caliber 样本量变化却无预注册选择规则，均停止该结论与验收签署。载体应是 PRD 规范句 + handback-review gate。 |
| `-05` | **refactor** | 删除“历史足量后再做”的静默形态；每个被消费批次必须产 `insufficient_history / method_ready / recalibration_due` 之一并由 IDS 签收。数据不足时仍累积同口径历史、禁止宣称稳定；何时转态由预注册方法的适用前提决定，不看现数造 N。 |
| `-09` | **refactor** | 做 US 分解，但不得据此满足 CN/HK 重判条件；CN/HK 明报 `not_estimable`。§6 条件 1 改为“每个拟重判市场均有可解释的 per-market 跨次读数”，条件 2 同市场逐一成立，operator 才可进入第三项。 |
| `-12` | **refactor** | 不把“修后 ship 不复核”合法化。第四轮是 operator checkpoint：接受**未改的已审 finding**、修复后强制验证（验证轮不受名义四轮帽；持续收敛可签续）、升级 forge、退 task；其余动作 fail-closed。IDS 产逐字替换授权，operator 手工送 XenoDev；在三 gate 未接线期间，承接义务挂可达的 `forge:009-pM3prime:phase0` 复核文件 hash。 |
| 元层 | **new** | v5 每行必须同时写 `normative_site / owner / due_event / stop_or_options / obligation_path`；缺一不进 verdict。这样消费者可达、选项含兜底，且不会再用“上议程=satisfied”冒充落地。 |

**具名预测**：我判 `-12` 必须禁止“修复后 ship 不复核”，但我预期 A 侧会因本包已被接受、且它是该义务创立者，而把第四态合法化并附补偿性回归/后续复核。另我判 `-04` 的根因是 stage 产物缺少 decision→refactor 的全映射；我预期 A 侧会判为一次三文档同步遗漏。

保守失真与乐观失真应共用“逐字核验—更正—留 provenance”，但处置强度不同：乐观失真可能误解锁，立即 fail-closed；保守失真默认纠偏并登记浪费，只有它触发不可逆/高成本动作时才阻断。本次“无留痕”属后者，不能与过去乐观漏报等量处罚。

## 3. 我现在最不确定的 3 件事

1. `handback-review` 现有步骤能否在不改 SHARED-CONTRACT 的前提下承载硬停点。
2. 哪类低历史方法能给出适用前提而不把已见数据偷渡成 N，留 P2 查证。
3. `census_run` 与被引用 aggregation batch 是否有足够稳定的可机械关联；若只能靠 variant 文本，对 `-11` 的“引用跑无行”判据可能不可执行。
