# Fork origin · 009-pM3prime

**Forked**: 2026-07-16
**Forked-from**: forge stage 文档(`discussion/009/forge/v5/stage-forge-009-v5.md` §Next-version PRD draft)——**非** L3 candidate
**Parent**: idea 009(root)· 建于 fork 009-pForge 已交付的 M1+M2 资产之上(PIT 价格层 + alpha 评估机器 · 743 passed · fork-complete)
**Fork decision**: operator 2026-07-16 选 forge v5 Decision menu **[A]**,并加约束「**先只授权 E0+E1**」(E2/E3 defer,gate 在 E1 真数字)

## 为什么有这个 fork

2026-07-16 operator 亲述事实修正(`discussion/009/operator-input-2026-07-16-implicit-signals.md`):
该分析师**不产显性荐股 call**,信号只以隐性形态存在 → M2 评估机器的显性信号输入假设对该
数据源永久不成立,07-07 smoke path 决议前提作废。forge v5(full · 8 rounds · strong-converge ·
converged)裁定:**M3'(信号提取头)提前成立,以最小证伪链 E0→E3 推进**。

本 fork 承接证伪链**前两站**:
- **E0** 口径预注册(疑似信号定义 + rejection taxonomy + 预注册密度阈值 + 三表 schema)
- **E1** 密度普查 + 两层金标(语料真数字 + 提取器可靠性验收 + record_tickers 语义查明)

E1 的 hand-back 数字交回 IDS 后,operator 另行决策 E2(历史窗先导)/ E3(forward 确证线)授权。

## 血缘链

```
proposal §009(2026-06-30)
  → forge v1(集成契约+回测地基)+ v2(七环节蓝图 · Strangler M1-M4)
    → fork 009-pForge(M1+M2 · 2026-07-01 → 07-06 fork-complete · 743 passed)
      → 07-07 P2-prod-precondition-gap(evaluate 无输入 · smoke path 决议)
        → 2026-07-16 operator 事实修正(分析师不荐股 · smoke path 前提推翻)
          → forge v3(双 as_of 轴)/ v4(O8 evidence 台面)不受影响,继续有效
          → forge v5(M3' 提取头 · 证伪链)→ 本 fork(E0+E1 授权)
```
