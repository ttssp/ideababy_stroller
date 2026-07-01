# Forge v2 · 009 · P1 · GPT55xHigh · 独立审阅(no search)

**Timestamp**: 2026-07-01T13:54:50+08:00
**Searches used**: NONE.
**Visibility**: I did NOT read other P1.
**Reviewer stance**: 审阅人,非 daydream。

## 0. 我读到的标的清单 + 阅读策略

- 我读了:config、v1、004/008 PRD、strategy 四文件、alembic 五文件、P1 模板。
- 我跳过的:`discussion/009/forge/v2/moderator-notes.md` 不存在;未读 `P1-Opus47Max.md`。#4 strategy 与 #5 DB schema 均真实可读,没有使用 fallback。
- **K 摘要**:只画目标态蓝图,不推翻 v1;讲清形态/边界/分期;不建大壳,每期可用。
- **阅读策略**:按 Y 四视角映射 004/008/strategy/DB 到七环节,重点看两头接入。

## 1. 现状摘要(Y 视角)

### A · 架构/目标态

七环节映射:008=采集;008 轻量包+`advisor_reports`=结构化;`StrategyModule`=信号;`conflict_reports`/`decisions`=决策与纪律;缺 PIT 数据层+alpha/calibration 两头。图谱、蒸馏仅是未来 lane。

### B · 分期路线

分期沿 v1:数据层→alpha→calibration→004 lane。alpha 头已有跨周 `advisor_reports` 和 `strategy_signals`;calibration 缺事后价格、不动基线、反事实窗口。

### C · 边界

边界已清:008 不建议;004 human 拍板,无自动下单/综合分;lane 只读 provider。四念头:验证 alpha=alpha 头;回测=数据层+两头;图谱=v2+ gated lane;蒸馏=末位独立 lane。

### D · 工程纪律

纪律锚点:`source_id` 隔离、registry 防重复、无 winner/recommended、correlation audit fail-closed。AC-1..AC-5 可复用;回测层还缺 as-of、价格源、trial-count、反事实 schema、contract tests。

## 2. First-take

| Y | 倾向 | 理由 |
|---|---|---|
| 架构/目标态 | refactor + new | 保留旧器官,新建回测复盘;不是统一壳。 |
| 分期路线 | keep | v1 顺序成立;alpha 近,calibration 远。 |
| 边界 | keep + sharpen | 红线和 IDL 已隔开;四念头接口/gate 还要画清。 |
| 工程纪律 | new | 回测契约和跨器官验收要新增。 |

## 3. 我现在最不确定的 3 件事

1. calibration 反馈自动调阈值,还是只给 human 确认建议?
2. 价格数据层 v0.1 只做关注股日线,还是纳入多市场/复权/汇率/成本?
3. 蓝图实到字段/gate,还是服务边界?后者可能诱导 V4。
