# Forge v1 · 009 · P3R2 · GPT55xHigh · 联合收敛 R2(finalize)

**Timestamp**: 2026-07-01T11:27:10+08:00
**Visibility**: 我已读对方 P3R2。
**Convergence mode**: strong-converge(从 inbox / forge-config 读)。

## 1. 我对每条分歧的最终立场 + 让步

- **分歧 1**(009 的交付身份:独立统一壳,还是契约化松耦合演进):
  - 对方在 P3R2 给的论证:"当前只证明需要共享数据层 + 两个评估头" → 接受。Opus 已接受我 P3R1 的判据:一套数据两用是必要价值,但当前只证明共享 point-in-time 数据层 + calibration/alpha 两个评估头,不足以证明 004/008 之外需要独立统一壳。
  - 我的最终立场:009 当前 = **闭环集成契约规范 + 共享回测地基**,落入 004 v1.0 回测 lane + 008 消费契约的松耦合演进;不先建独立统一壳。
  - 让步给对方的部分:接受“一套数据两用”作为未来升级 gate 的核心判据,但不把它作为当前统一壳的充分条件。统一壳只在 calibration/alpha 两头需要 004/008 都不拥有的独立回测内核、状态模型、验收口径时升级。

- **边界固化项**(上游融合/蒸馏与 004 红线 #9):
  - 对方在 P3R2 给的论证:"004 UI 永不显示'权威综合分'" → 完全接受。
  - 我的最终立场:上游 alpha 评分只能存在为回测内部指标或独立信号 lane;蒸馏技能只能落成独立 lane;004 端永不呈现权威综合分,alpha 再强也不推出自动执行。
  - 让步给对方的部分:无。双方已同向,本轮只把它转成 decision-list 与验收条款。

## 2. 联合 verdict(单一)

我和对方在 R2 后达成单一 verdict:009 的价值成立,但当前交付物不是独立统一壳,而是**闭环集成契约规范 + 共享回测地基**。保留 004 已 ship 的 StrategyModule 多 lane、advisor/XGBoost lane、correlation audit 纪律与 004/008 红线;把 008 forge v4 的可溯源证据 + 置信度契约作为上游输入边界。v0.1 最先新增共享 point-in-time 数据层和回测层,内建 walk-forward/OOS、交易成本、trial-count、DSR/PBO;其上分出 calibration 头(我的决策/不动反事实,服务承诺壳)与 alpha 头(分析师方向/真实股价,验证顾问可信度)。图谱 defer 到 v2+;蒸馏最后且只能独立 lane 化。统一壳升级为未来 gate:仅当两评估头需要 004/008 都不拥有的独立回测内核、状态模型、验收口径时才成立。无 unresolved。

## 3. 残余分歧降级为 v0.2 note

- v0.2 note 1:calibration 头与 alpha 头的指标模型不同,后续可能逼出独立回测内核。回头看的时机:两个头都跑通后,若共享 runner 为迁就另一头持续打补丁,触发统一壳 gate 重审。
- v0.2 note 2:008→回测的 as-of 时间戳契约需要 L4 细化。point-in-time 要求原文、摘要、结构化字段、价格数据都带当时可见时间;若 008 轻量包不足,回测层必须补 as-of 索引。
- v0.2 note 3:蒸馏技能的产品措辞要持续警惕。“自给自足/自主分析”只能表示一个独立 lane 的能力增强,不能滑成替人决策或综合打分。

## 4. W 形态产出的初步草稿建议

- **W 含 decision-list**:
  - 保留:004 StrategyModule IDL;lane 隔离/只读 provider;advisor lane + XGBoost lane;004 红线 #1/#9/#10;008 可溯源证据 + 置信度契约。
  - 调整:correlation_audit 从相关性审计升级为完整回测统计纪律;008↔004 粗包调整为 008→回测→StrategyModule→004 四段契约;proposal 第[4]条“自主分析”改写为“蒸馏独立信号 lane”。
  - 删除:当前不建 009 独立统一壳;不做 004 权威综合分;不做自动执行;v0.1 不做图谱。
  - 新增:共享 point-in-time 数据层;alpha 评估头;calibration 评估头;trial-count/DSR/PBO/OOS 验收;统一壳升级 gate。
- **W 含 next-PRD**:
  - v0.1 定位:契约规范 + 共享回测地基,不是新应用壳。
  - 核心用户故事:验证某分析师是否有 alpha;用回测校准我的承诺壳纪律强度;让 008 证据包可被回测与 004 消费。
  - Scope OUT:权威综合分、自动下单、统一壳先行、图谱先行、蒸馏自主决策。
- **W 含 next-dev-plan**:
  - M1:定义并落地 point-in-time/as-of 数据契约,接入 008 证据包与价格数据。
  - M2:先做 alpha 头,产分析师 hit rate、超额收益、显著性、DSR/PBO 与样本窗报告。
  - M3:做 calibration 头,把我的决策、不动反事实、004 档案接入同一回测 runner。
  - M4:把结果以独立 lane/内部指标接入 004;图谱/蒸馏仅在 M2/M3 证明价值后另起 gate。
- **W 含 refactor-plan**:
  - 回测层(new):共享数据层 + runner + 统计纪律,是 009 的实际枢纽。
  - 004 strategy 层(keep/refactor):保留 IDL 与多 lane,新增“分析师 alpha 得分/蒸馏信号”独立 lane,禁止综合分。
  - 008↔回测契约层(refactor):补 as-of 时间戳、source_ref、置信度、degraded 状态,保证回测可复现且不误认 008 在给建议。
