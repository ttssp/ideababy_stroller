# Forge v4 · 008 · P3R2 · GPT55xHigh · 联合收敛 R2(finalize)

**Timestamp**: 2026-06-30T18:32:42+08:00
**Visibility**: 我已读对方 P3R1。
**Convergence mode**: strong-converge

## 1. 我对每条分歧的最终立场 + 让步

- **分歧 1 · 用途定义颗粒度**
  - 对方在 P3R1 给的论证:“无悔下游 now + 跟单 gated” → 让步/接受。
  - 我的最终立场:采用两层用途定义。第一层 now = 自己回看检索 + 给 004 的可溯源结构化证据契约;第二层候选 = 机器可信跟单,只能在 spike 过门后进入后续 PRD,不能让 build runtime 据此自行实现信号产品。
  - 让步给对方的部分:用“无悔下游 now”明确解决 K#1,不再只说“008↔004 接缝未定义”。

- **分歧 2 · spike 通过门槛**
  - 对方在 P3R1 给的论证:“门槛由 operator 据代价不对称定” → 部分接受。
  - 我的最终立场:forge 不拍固定百分比;P3R2 只定义 pass 条件的形态:spike 必须产出 decision-grade evidence,至少分层报告 stance/conviction/action × 反讽/非反讽 × high-confidence 子集,并把 false-positive signal 作为一等风险。operator 再据这些数字决定是否开启跟单。
  - 让步给对方的部分:不在 forge 阶段写死准确率阈值;但要求 W 里给出可执行指标结构,防止 spike 变成泛泛抽查。

- **分歧 3 · KG-24/KG-25 权重**
  - 对方在 P3R1 给的论证:“列入 decision-list + 标候选解” → 接受。
  - 我的最终立场:KG-24/25 进入最终 W,但定位为框架可靠性附带必修,不抢 v4 主判题。KG-24 归状态契约统一;KG-25 归结构化输出约束、降级和可见告警。实装细节留 XenoDev。
  - 让步给对方的部分:不把 KG 写进 next-PRD 主目标,只写成支撑 spike/结构化链路可信的工程纪律项。

## 2. 联合 verdict(单一)

**单一 verdict:GO · gated refactor。** 008 v4 应推进,但推进方向不是“直接做机器跟单”,而是把产品边界补实:先在 PRD 中定义 008↔004 消费契约,把 008 的当前下游定为“回看检索 + 可溯源结构化证据包”,并明确 008 不产自动执行信号;“机器可信跟单”只能作为候选目标,由信号可靠性 spike 过门后再决定是否升级。字典第 1 层无悔字段现在可做,第 2/3 层字段必须受用途和 spike 结果约束。KG-24/KG-25 作为框架可靠性附带必修进入 W,用于防止结构化链路静默漏数或坏 JSON 假失败。**无 unresolved。**

## 3. 残余分歧降级为 v0.2 note

- v0.2 note:若 spike 显示 high-confidence 子集足够稳定,可回头讨论是否把“信号候选”从 004 消费契约升级为 004 的正式跟单输入。
- v0.2 note:若 operator 明确接受较高漏信号率但不能接受假信号,后续门槛应偏 precision / false-positive 上界,而不是总准确率。
- v0.2 note:若 DeepSeek 或当前模型栈不支持 constrained decoding,KG-25 可先用清洗 + 鲁棒解析 + degraded 降级 + 可见告警兜底。

## 4. W 形态产出的初步草稿建议

### next-PRD draft · 关键产品决策点

- 新增“008↔004 消费契约”:008 输出可溯源结构化证据包,字段包括原文回链、实体/主题、可选置信度和降级标记;004 决定是否形成投资信号。
- 新增“信号候选目标 gated”:stance/conviction/action 仅作为 spike 验证字段,未过门前不得写成自动跟单能力。
- 保留 Scope OUT 红线:008 不产买卖信号、仓位建议、收益判断;任何信号化消费必须在 004 或后续 PRD 中承接。

### decision-list · 4 列矩阵建议

- 保留:第 1 层无悔字段 `entity_type`、`tech_side` 三值、黑话词典、`asker`/双时间戳;C6/C9 可溯源约束;008 不直接给建议的红线。
- 调整:US6 从“轻量包喂给 004”升级为“可溯源结构化证据契约”;KG-24 抽单一 manifest ready 状态契约;KG-25 增加结构化输出鲁棒层和可见失败。
- 删除/冻结:未验证前冻结第 2 层 stance/conviction/action 的全量重提;冻结第 3 层 sections/relations/cross_refs 全量图谱化;不做“跟单信号产品”。
- 新增:信号可靠性 spike;分层评测报告;high-confidence 子集策略;false-positive signal 统计;`degraded`/parse-failure 可见状态。

### next-dev-plan · milestone 建议

- M1 PRD patch:写清 008↔004 消费契约、gated 跟单表述、Scope OUT 澄清、字典三层取舍。
- M2 spike package:抽 100-200 条样本,覆盖反讽/非反讽、黑话、免责声明、问答/图文;人工金标 stance/conviction/action;输出分层 precision/recall/FP-signal 报告。
- M3 无悔层落地:实现 `entity_type`、`tech_side`、黑话词典、问答元数据修复,保留 source_ref 回链。
- M4 工程纪律:修 KG-24 状态契约;修 KG-25 结构化输出鲁棒性、降级和告警;保证 spike/重提失败不静默。
