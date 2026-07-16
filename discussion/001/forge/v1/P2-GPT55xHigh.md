# Forge v1 · 001 · P2 · GPT55xHigh · 参照系评估(with search)

**Timestamp**: 2026-07-16T03:35:25Z
**Searches run**: 16, SOTA-benchmark
**Visibility**: 我已读对方 P1。

## 1. SOTA 对标(或指定对标)

| 标的 X' | 参照项 | 它怎么做 | 我们怎么做 | gap | URL/Source |
|---|---|---|---|---|---|
| P0.2 gate | LangSmith evaluation lifecycle | 离线 dataset 跑实验,线上 production runs/threads 做实时质量退化检测,每次实验保留 outputs、scores、traces | 仍把 T010/T011 绑在一次性 RERUN-PASS | 信任证据应来自持续 run trace,不是单次签字 | https://docs.langchain.com/langsmith/evaluation-concepts |
| 人审形态 | LangSmith annotation/audit queues | 把 runs 放入单项或 pairwise queue,配置 rubric、reviewer 数、reservation,并允许人类纠正 evaluator score | operator 被要求停机填盲测表 | SOTA 是抽查/校正工作流,不是人作为二值打分器 | https://docs.langchain.com/langsmith/annotation-queues ; https://docs.langchain.com/langsmith/audit-evaluator-scores |
| provenance 验收 | W3C PROV + Audit Cards | provenance 记录 entity/activity/agent 以判断质量与可信度;audit card 要交代 scope、method、process integrity、review mechanism | O2 有 source trace,但未形成验收级 provenance/audit artifact | trace 已对,但缺机器可验结构与审计上下文 | https://www.w3.org/TR/prov-overview/ ; https://arxiv.org/abs/2504.13839 |
| judge 校准/功效 | Kim 2026 + Noisy but Valid + agreement metrics | 人类 rating 是主量,LLM judge 是辅助;抽样设计需算 human review 数;小规模人标校准 TPR/FPR;报告 coverage/confusion/abstention | 3 真切片 + 1 负控只能给 smoke 诊断 | 统计功效不足,不能支撑唯一硬前置 | https://arxiv.org/abs/2605.16354 ; https://arxiv.org/abs/2601.20913 ; https://arxiv.org/abs/2606.00093 |

综合看,SOTA 的共同形态不是“先让人盲测签字再开工”,而是:保留完整轨迹,把线上或实验 runs 推进抽样人审,用人审校准自动评审器,再把修正回流到 eval/report。OpenAI Evals 文档也把 eval 描述为“run, analyze, iterate”的循环,而非一次性发证(https://platform.openai.com/docs/guides/evals)。我们当前最接近 SOTA 的部分是 O2/O7 的 in-band trace/journal;最落后的部分是把 gate 的权威仍放在带外 PASS artifact。

## 2. 用户外部材料消化

K 无外部材料: n/a。

## 3. 修正后的视角

- P1 判断“人肉盲测二值硬前置”应 cut → **站住**。LangSmith 与 Audit Cards 都支持人审,但支持的是抽样审计、纠错、留痕解释,不是让单个 operator 做一次性签字。
- P1 不确定“统计功效也低” → **站住且加强**。Kim 2026 要求按目标 power 反推 human review 数;Noisy but Valid 还要求校准 judge 的 TPR/FPR。P0.2 的 4 个样本只能 smoke,不能 certification。
- P1 候选“可审计留痕、抽查、后验校准” → **站住**。这正是 LangSmith online eval + annotation queue 的工业形态,也与对方 P1 “把 O2 从产品功能提升为验收机制”同向。
- P1 判断“PASS 与下游解锁没有机器闭环” → **站住但换对象**。若砍 RERUN-PASS,B4 不等于消失;机器闭环应转为 trace 完整性、review queue 状态、journal 回溯是否满足最低规则。
- P1 不确定 B7 是否消解 → **部分修正**。answer-key、nonce、签字重放这些反作弊议题会随盲测退役而大幅消解;但 evaluator 校准仍要防 reviewer leakage、样本选择偏差和 Goodhart,只是问题从“防作弊考试”变成“审计设计”。
- P1 在 trace 完整性 vs 有限使用之间摇摆 → **倾向有限使用优先**。SOTA 更像先上线受控观测、用 production traces 校准,前置只验 trace schema 与最小抽样机制,不再要求产品价值先被本地盲测证明。
