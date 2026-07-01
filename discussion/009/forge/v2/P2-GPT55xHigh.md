# Forge v2 · 009 · P2 · GPT55xHigh · 参照系评估(with search)

**Timestamp**: 2026-07-01T14:17:21+08:00
**Searches run**: 8 queries, SOTA-benchmark
**Visibility**: 我已读对方 P1。

## 1. SOTA 对标

| 标的 X' | 参照项 | 它怎么做 | 我们怎么做 | gap | URL/Source |
|---|---|---|---|---|---|
| 009 七环节蓝图 | QuantConnect Algorithm Framework | Alpha / Portfolio / Risk / Execution 等模型隔离;文档强调模型“不应通信”,可隔离时用 framework。 | 008→回测→StrategyModule→004,同样靠 lane/contract 隔离。 | SOTA 支持“契约化多器官”,不支持统一壳;009 还缺回测层的标准 contract tests。 | QC Algorithm Framework |
| 009 分期演化 | Fowler / Azure Strangler Fig | 用新功能逐块包裹旧系统,渐进迁移,避免一次性替换。 | 新回测器官 latch 到 004/008,先数据层+alpha,再 calibration,未来 lane gated。 | P1 的分期站住;蓝图必须标“每期可用”,不能画成全量重建。 | Fowler + Azure |
| 价格数据层范围 | QuantRocket PIT data + QuantConnect corporate actions | PIT ticker/date 映射、delisted 覆盖、复权/公司行动处理是历史回测地基。 | P1 只说“价格源”,现在需明确 v0.1 至少日线、复权、PIT ticker、退市感知。 | 多市场/汇率/tick 可 defer;复权和 PIT 不能 defer,否则 alpha/calibration 数字会错。 | QuantRocket + QC |
| calibration 回流 | HITL/interactive ML papers | 人机反馈可改模型,但循环可能不收敛;反复使用验证/测试信号会降低统计力。 | calibration 回测可产旋钮建议,但不应静默自动改 004 纪律。 | 支持 Opus: v0.1 应 human-on-the-loop;自动回流必须另设 gate 和 overfit guard。 | arXiv HITL + ease.ml/meter |
| 蓝图详略度 | 架构视图实践 + Strangler | 目标态给边界和接口,增量替换给当前切片细节。 | 现建器官画字段/AC;未来图谱/蒸馏只画 lane 签名+gate。 | 支持“两档详略”:充分彻底不等于把远期插槽 spec 化。 | 同上 Fowler/Azure + QuantConnect |

## 2. 用户外部材料消化

本轮 K 内无新增 URL/文件;X 5 标的就是全部一手材料。无新增材料会改变方向。SOTA 只用于压实 P1 first-take,不重审 008 合规,也不重刷 v1 已定的 TipRanks/DSR/PBO 方法论。

## 3. 修正后的视角

- P1“目标态是七环节数据流,不是统一壳”→ **站住**。QuantConnect 的模块隔离与 Strangler Fig 都支持“契约化增量器官”,不支持一次性大壳。
- P1“价格数据层 v0.1 范围不确定”→ **被明确化**。SOTA 要求 PIT ticker/date、复权/公司行动、退市感知;但多市场/汇率/tick 可 defer。
- P1“calibration 反馈自动还是人工不确定”→ **收敛到 human-on-the-loop**。HITL 文献显示反馈循环会受偏差、不收敛和 adaptive overfit 影响;v0.1 只给建议旋钮,由 human 确认生效。
- P1“蓝图详略度不确定”→ **两档化**。现建器官(PIT 数据层、alpha 头、calibration 头)画接口字段+AC;未来插槽(图谱、蒸馏)只画 StrategyModule 签名、输入输出、gate。
- 对 Opus A/B:我同意 A 的 human-on-the-loop,边界是“回测可建议,不得静默改权重/纪律阈值”;同意 B 的两档详略,分界=当前两期要建的器官 vs gated future lane。
