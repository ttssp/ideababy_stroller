# P3R1 · GPT55xHigh · forge 001 v6

> 硬约束自证:本轮零新检索;未读 `_contaminated-p1/`;引用对方原句均短于 15 words。篇幅略超 1000 CJK 字符,未做有损压缩。

## §1 整合摘要

双方已经收敛到四个核心:第一,旧池到目前未产生真实 O2/P2 PASS,追溯迁移表实测为零项,这是本轮最强的独立事实增量。第二,v5 的池化思路不废除,但只能保留为探索/warn;block-PASS 出口必须等可比较类在 epoch 开启时预注册并进不可变池键。第三,CVE 二态比单一 fail-closed 更准:`REJECTED` 类是消费点机器可拒,`DISPUTED` 类是保留但不得当 clean PASS 消费。第四,chair = operator;`/handback-review` 是 chair 认定的闸点和记录,不是 chair 本身;spec-writer 不能自任。

## §2 我的初步 verdict

池化机制保留但 PASS 出口现在关闭;v0.8 前置键为 `decision_epoch + rubric + comparability_class`,去重身份为稳定 claim identity,`direction` 进分区/比较类,退出去重计数。追溯采 CVE 二态:已证无效走 rejected-like、存疑走 disputed-like,且本轮落一份“零受影响 PASS”核查记录。`needs-attention` 不是 veto,但 override 必须由 operator-chair 逐条写明 addressed;无 chair 记录不得 clean PASS。T040 立即局部起跑:5 个非 O2 文件 block,O2 PASS 面只建 warn/baseline。三态接口 owner 与消费点 fail-closed 是同一个新 task。

## §3 关键分歧清单

**D-1 · direction 去重键**  
我的立场:同意 Opus,`direction` 应双向处置:进分区/比较类,退出去重计数;否则同一语义 claim 跨方向或同义改写仍可膨胀。对方立场+引用:Opus 主张“进分区键 ∧ 退出去重键”。R2 期望:标为已收敛;剩余只裁 stable claim identity 谁定义、何时冻结。

**D-2 · T040 起跑幅度**  
我的立场:确认 Opus 修正。§0.1 已把 O2 PASS 向定成 warn,隔离条件足够;不必等 v6 全部收敛才写非 O2 contract。对方立场+引用:Opus 说“隔离已由 spec 给出”。R2 期望:写入最终裁决:立即起跑,5 文件 block + O2 warn/baseline,不得把 O2 PASS 误做 block。

**D-3 · 认识论强度分级**  
我的立场:同意“事后同意”不得与独立收敛同权,但这条要对双方适用。Opus 接受我的 v5 探索出口、CVE 二态、chair 映射,也不是 P1 独立复现,应列为“P2 外部材料修正后收敛”,低于“零旧 PASS”这类双向独立 + 仓内核查。对方立场+引用:Opus 警告“回声室在 P1 被隔离后”。R2 期望:最终 decision-list 每行加 evidence_grade:independent / SOTA-corrected / post-hoc-accepted。

**D-4 · 消费点 task 边界**  
我的立场:三态接口 owner 与消费点 fail-closed 必须是同一个 task,否则接口只是标签、消费点无输入。task 边界:读取 briefing + journal + pool manifest,产出 O2/P2 verdict artifact,并规定 clean/rejected-like/disputed-like/insufficient/fail 的消费语义。对方立场+引用:Opus 说“消费点」目前不存在”。R2 期望:给具名新 task,不要塞 T041。

## §4 与 K 的对齐性自检

| K 条目 | 状态 | 自检 |
|---|---|---|
| (a) 分区键 | ✅ | `comparability_class` 前置冻结进池键;direction 不再抬高去重计数 |
| (a) 借错是否追溯 | ✅ | rejected-like/disputed-like 二态;本轮实测零旧 PASS |
| (a) 下游语义谁定义 | ✅ | operator-chair 定义,`/handback-review` 留痕 |
| (b) 谁的话算数 | ✅ | reviewer 非 veto;chair 可 override,但必须 addressed 记录 |
| 可执行裁决 | ⚠ | 消费点 task 未存在;P3R2 必须命名并给边界 |
| v5 四列范式回检 | ✅ | 范式有效;fallback 列需强制三要素 |
| 追溯成本 | ✅ | 当前零迁移成本,现在立规则最便宜 |
| ≥3 阈值 | ⚠ | 本轮无产品价值视角,只挂账不裁 |
