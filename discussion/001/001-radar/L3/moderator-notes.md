# Moderator notes · 001-radar · L3

## Injection @ 2026-07-10T08:19:13Z
**Type**: Hard constraint
**Binding on**: Both models

**背景**:P0.2 位移可信度盲测 gate 第一次真跑(diffusion models,2026-07-10,T005 后 gate 首次 operator 可跑)暴露两个问题:
1. 一次性盲测统计功效低(3 切片 + 1 阴性对照,瞎猜也有 1/3 命中率),只能挡"明显编造"一档;
2. 要件①②的判定质量依赖 operator 对**被测窗口**的记忆浓度——产品窗口是近 12-18 月,但 operator 对 diffusion models 的深耕期在 2023 及以前,窗口错位导致判定信号失真。快速演化领域里"operator 深耕期 ≠ 产品近期窗"是常态,不是本次特例。

**operator 核心立场(hard constraint)**:质量机制必须**实事求是、结论可回溯、在使用过程中持续反馈偏差、渐进提升构建质量**——不追求一蹴而就的一次性认证。具体右调:

1. **P0.2 盲测 gate 语义右调为「初始 smoke test」**:只负责挡"地基明显烂还继续烧预算"(防 V4),PASS 解锁 Phase 1+ 的语义保留,但 PASS **不**宣称"位移重建可信性已终审证成"。
2. **长期质量主锚移到 O2 + O7**(PRD 已有,权重上升):
   - O2(EvidenceLink 三跳可回溯)= "结论可以回溯"的落地;
   - O7(JournalEntry.decision_delta 使用中偏差反馈)= "用的过程中不断反馈偏差"的落地。
   信任是使用中逐步校准出来的(O4 calibration 本义),不是 gate 一次发证。
3. **历史窗回溯验证入候选工具箱**:拿 operator 已知答案的历史窗口(如 diffusion 2021→2023)考管线,是"结论可回溯"的执行形式,信号强于近期窗盲测;需 retriever 支持 `to_publication_date` 封闭历史窗(XenoDev 侧小改造,候选任务,非本注入强制)。
4. **KG-B4(gate STOP 机器强制)按右调语义设计**:强制的是"FAIL 不降级续建"(STOP 铁律不变),而非"一次 PASS = 永久免检"。

### Required response
下一次 PRD 修订(v1.1)或下一轮 L3 相关 round,双模型必须以 "## Moderator injection response" 一节回应本注入(明确 gate 语义、O2/O7 权重、历史窗回溯的取舍)。
