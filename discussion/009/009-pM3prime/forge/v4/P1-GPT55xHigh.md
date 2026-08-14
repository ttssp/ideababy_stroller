# Forge v4 · 009-pM3prime · P1 · GPT-5.6-Sol xhigh · 独立审阅(no search)

**Timestamp**: 2026-08-14T03:18:12Z
**Searches used**: NONE in this round.
**Visibility**: I did NOT read other reviewer's P1.
**Reviewer stance**: 审阅人——评判已存在物,不是 daydream。

## 0. 我读到的标的清单 + 阅读策略

- **已读**:hand-back 全文;HANDBACK-LOG 第 35/36 条;forge v3 全文;ledger 中 OB-07/09/13/15/16 全部相关行;PRD §4-E1(p)、§6 三条科学重判条件、§7 红线 3 全块;warn README 三态裁决与 validator :112-118。
- **外部 XenoDev-009 亦全部可达**:T015 §5、round-9、D9;结果 JSON 全文;census.py 的 `CensusReport.attempt_log_persist_failed`、`_persist_attempt_log` docstring、主事务边界;spec §6.3 与 SLA E1 行。**跳过:无**;`moderator-notes.md` 不存在。未读对方 P1。
- **K 摘要**:本轮审的是“**治理结论写下来之后没有产生行为**”;四题必须分别回答 pass 是否欠显式裁决、无两项 provenance 前置时跨批比较是否可信、校准周期/责任人/升版触发、C4 convert 判据形态。并保持“M1=pass 不解锁扩样/E2、41 条路 CLOSED、不改 C6 数字”。
- **策略**:沿“条款→ledger→消费 gate→真实产物”追传导,再分开看跨批 provenance、信度与效度;不以 1287 全绿代答治理问题。

## 1. 现状摘要(按 Y 视角组织)

### 视角 A · 工程纪律

v3 正文与 decision matrix 写“三态必须回 forge”,结果矩阵却只令 fail/indeterminate 触发 v4;OB-07 标题与 note 重现同一分叉。hand-back 采用窄读后,第 36 条另立 OB-16 才让 pass 分支实际开火。warn README 允许具名 defer,validator 则只按 `warn_class + due_event` 找到期项,不识别“已裁决”状态。

ledger 还显示:OB-09 的标题要求定形周期/责任/升版条件,其 satisfied 行只表示“已上议程”;OB-13 标题要求在 O 表补引用,实际另表交付后按目标等价结账。

### 视角 B · 架构设计

主 census 是整 run 单原子事务,invalid/crash 全回滚;attempt log 在主连接关闭后用独立连接、run 末尾批量 commit。于是 SIGKILL 窗口可丢 attempt,而失败 run 的内容哈希随 trial ledger 回滚;attempt 表只剩 `source_id`。T015 §5 论证限定于有人值守的本批,未覆盖未来跨批比较。

结果 JSON 只在全局文字中声明语料一致;`per_run_summary` 仅有 accepted 与 verdict,没有每跑内容身份、`caliber_version`、模型/服务身份或失败率分母字段。

### 视角 C · 测量效度 / 统计方法学

M1 在固定 102 条本批为 pass:`J_1=0.4078`,`J_agg=0.6885`,CI 全大于 0;它测的是本批信度。六跑的 `census_verdict` 又全部为 `below_threshold_advisory`。PRD 的科学重判条件要求 per-market 跨次读数与噪声小于阈值裕度,而当前 JSON 未申报 per-market 一致性/裕度。

C4 文本要求每批产生跨次一致性读数并绑定身份;SLA 判据实际列出的 SQL 只验证 trial 哈希四元组与 attempt 行存在,未直接验“跨次读数”。

## 2. First-take 评分

| 维度 / 题目 | 倾向 | 理由(证据锚) |
|---|---|---|
| 工程纪律 | **refactor** | 把义务正文与消费判据合成同一可机读状态机。第三处弱化是 OB-09“定形”被 satisfied 为“上议程”;第四处是 C4“每批跨次读数”被较弱的身份行 SQL 代验。`ledger.jsonl:35,54`;`SLA.md:136`;`spec.md:380,395`。 |
| 架构设计 | **refactor** | 跨批 provenance 不能一半随 invalid 回滚、一半到 run 末才批写。`census.py:718-740,894-898,923-930`;`T015.md:449-475`。 |
| 测量效度 / 统计方法学 | **new** | 现有一次本批信度基线不足以定义校准制度或效度门。`T015-aggregation-probe-result-20260813.json:48-57`;`PRD.md:487-490`。 |
| ① M1=pass 三态裁决 | **refactor** | **pass 也欠具名裁决。当前裁决:first-take 接受其为 fixed-batch reliability evidence,但不产生授权、不外推、不解锁 E2。**“无后续授权”是裁决结果,不能替代裁决动作。`stage-forge-009-pM3prime-v3.md:163,204-210,277`;`ledger.jsonl:57`。 |
| ② OB-15 跨批可信度 | **refactor** | **没有两项前置就不可信**:失败 attempt 既可能消失,又不能证明比较的是同内容输入;本批全绿无关。`HANDBACK-LOG.md:1666-1692`;`census.py:725-740,1082-1090`。 |
| ③ OB-09 校准制度 | **new** | 初判采用“双触发”:每个将被消费的新比较批次到期一次;模型/服务/语料/口径身份变化或预注册稳定性界越界时立即升 `caliber_version`。XenoDev 测量 owner 产证,IDS operator-chair 才能裁决/升版。`stage-forge-009-pM3prime-v3.md:237-240`;`ledger.jsonl:54`。 |
| ④ C4 warn convert | **refactor** | 形态应为:先具名下游决策与可容忍错误→前瞻预注册指标/样本/阈值→独立校准证明该指标与决策错误有稳定映射→才 convert;否则维持 report-only 或 revert。不得因看见 0.4078 后设数。`PRD.md:524-536`;`framework/warn-registry/README.md:64-75`。 |

六跑全为低密度对 **M1 判据无影响**,但对下游有实质影响:它阻止把“聚合更一致”取景成“更接近 E2 解锁”;摘要必须并报。`T015-aggregation-probe-result-20260813.json:14-38`;`HANDBACK-LOG.md:1744-1756`。

## 3. 我现在最不确定的 3 件事

1. “每个消费批次”是否足够称为定期校准,还是仍需日历上限;P2 应找方法学依据。
2. C4 从信度 report 转 gate 前,什么外部效度锚能建立“稳定→决策错误”映射;v0.1 当前可能没有。
3. 六个低密度 verdict 缺 per-market 数值与裕度,因此其对 CN/HK 科学重判条件的精确强度仍不可判。
