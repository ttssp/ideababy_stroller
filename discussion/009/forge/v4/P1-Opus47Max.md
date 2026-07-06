# Forge v4 · 009-pForge · P1 · Opus 4.8 Max · 独立审阅（no search）

**Timestamp**: 2026-07-06T04:15:33Z
**Searches used**: NONE（forge-lite · 不对标 · 纯内部架构审）
**Visibility**: 未读对方 P1（独立 first-take）
**Reviewer stance**: 审阅人 — 评判已存在物 + 已核实的真代码,不 daydream。

## §0 我读到的标的清单 + 阅读策略 + K 摘要

**读了（全 6 个 X 标的 · 均真读代码非仅 hand-back 描述）**:
- T015 hand-back（R1→R3 全轨迹 · 核心 X）
- `conflict_report_assembler.py` L142-214（**真读** signals_hash 构造）
- `telegram/conflict_narrative.py` L44-65（**真读** 渲染截断）
- `ui/router_conflicts.py` L160-176（**真读** · 发现 hand-back 断言反例）
- alpha_lane.py 语义（经 hand-back §1 + 决策链）+ realized_return.py L231 signed（经 hand-back R1-F1）

**阅读策略**:沿 R3-F1/F2 的病灶行追真代码,对每个 hand-back 断言做**独立复核**(不照单全收)。
重点验三件事:(1) 缓存键是否真漏 evidence 强度;(2) 两个渲染点是否**都**真丢第四路;(3) alpha 的
NO_VIEW 语义是否真的下游无处安放。

**K 摘要**:alpha 是「分析师历史 edge 质量旁证」非「第四路方向票」(上游 signed → 不能产方向,
R1/R2 已证)。要定死三子决策:(a) ConflictReport 承载方式 (b) 缓存键纳入强度 (c) 渲染分区。
binding:守 NO_VIEW 语义不重议 · R3-F1 silent-wrong 必须真解 · 守 OUT-10 · 产品展示要对 operator
真有用不误导 · 轻收尾。

## §1 现状摘要（按 Y 视角 · 基于真代码）

### 视角 A · 架构正确性 / 器官边界

**R3-F1 缓存 silent-wrong = 真 bug（复核确认）**。`assembler.py:160-164` 的 cache 键:
```python
triplet = "|".join(f"{s.source_id}={s.direction.value}:{_confidence_bucket(s.confidence)}" for s in sorted_signals)
triplet_hash = sha256(triplet)[:16]  # 进 cache_key_extras["signals_hash"]
```
AlphaLane 有效结果恒 `direction=NO_VIEW · confidence=0.0` → triplet 里 alpha 段恒
`analyst_alpha=NO_VIEW:<bucket(0.0)>` **不变**。真正的 alpha 信号(evidence_strength / z_excess)在
`inputs_used`,**从不进 triplet**。→ 强 alpha / 弱 alpha / provider-error / no-provider **四态同 hash** →
LLM 缓存命中同一 `divergence_root_cause`。用户看到 signals 里 evidence_strength 变了,但报告根因是旧的
= **silent-wrong**。注:L156-157 注释 + L205 `all_no_view` 表明作者防的是「3 路方向票的 direction 变化」,
**没设想过「direction 恒定但携带信息在别处」的第四路** —— 正是 O8 新概念撞旧假设。

**器官边界**:这是 004 spine(services/)的改动,不是 009 fork 内。但**改的动机来自 009 的新 lane**,
且 assembler 是「装配台」本就该正确 hash 所有影响输出的输入 —— 可论证为「修 assembler 的既有正确性缺陷」
(cache 键不完备本就是 bug,只是现在才被第四路触发),不是「为 alpha 特殊改 004」。OUT-10 边界要 forge 判:
改 004 spine 是否算越界,还是「T015 授权的下游集成」。

### 视角 B · 产品语义 / 用户可见性

**R3-F2 须拆成两个渲染点分别判 —— hand-back 把它们一概而论,不准**:
- **Telegram（`conflict_narrative.py:54`）= 真丢第四路**。`signals = report.signals[:3]` + `_THREE_PERMUTATIONS`
  (只有 3! 种排列)+ L60-62 三个显式 `order[0/1/2]`。结构**深度绑定 3 路**,不是随手切片。第四路
  alpha 在 Telegram **完全不可见**。确认病灶。
- **UI（`router_conflicts.py:169`）= 反例 · 第四路其实透传不丢**。L169-176:
  ```python
  first_three = signals[:3]; remaining = signals[3:]
  ... return ordered_first_three + remaining
  ```
  它只把**排序**固定在前 3 路(permutation),`remaining`(含第四路 alpha)**append 透传**。所以 UI 路径
  第四路**不丢**,只是没有「方向票 vs 非方向 evidence」的视觉分区。**hand-back 的 R3-F2 对 UI 的断言错了。**

→ 产品缺口的真实形状:**Telegram 完全丢 + UI 混在方向票后无分区**。不是「两处都硬截断」。这直接影响
(c) 的工作量估算和修法。

## §2 三子决策 first-take 评分

| 子决策 | 我的 first-take verdict | 理由 |
|---|---|---|
| **(a) ConflictReport 承载** | **轻扩一等公民（中间路）**:ConflictReport / StrategySignal 加 `is_directional: bool` + `signal_kind` 已在 alpha_lane 有(经 Protocol);ConflictReport 层显式认「evidence lane」概念,但**不改 3 路方向票主结构**,把非方向 evidence 作旁路集合。**不复用 direction 5 值**(把 alpha 塞 NO_VIEW 会让「真中性观点」与「非方向证据」语义混淆,R2 已在 signal 层拒绝,ConflictReport 层同理该拒)。 |
| **(b) 缓存键** | **必须纳入 hash（硬解 · 不可降级）**:triplet 扩为纳入 `is_directional` + `signal_kind` + evidence 强度桶(evidence_strength 分桶,像 confidence_bucket 那样)。binding② 明令 silent-wrong 必须真解。**倾向纳入 hash 而非禁缓存**(禁缓存丢性能且掩盖问题;纳入 hash 是正解)。要点:evidence_strength 是 float,须像 confidence 一样分桶避免 hash 爆炸。 |
| **(c) 渲染** | **Telegram 必改 + UI 加分区**:Telegram 从「严格 3 行」改「3 路方向票 + 可选 evidence 区」(需重构 `_THREE_PERMUTATIONS` 假设);UI 已透传第四路 → 只需加「方向票/非方向 evidence」视觉分区(工作量比 hand-back 想的小)。**产品语义**:非方向 evidence 展示为「📊 分析师历史 edge:strong/moderate/weak(命中率 X% · 超额 Y% · DSR 显著性)」,明确标注「参考旁证 · 不计入多空」,防 operator 误读为第四张方向票。 |

**组合最优路径（first-take）**:(a) 轻扩一等公民 → 天然驱动 (b) 纳入新字段 hash + (c) 显式分区。
三者一致「显式区分方向票 vs 非方向 evidence」,是唯一不产生新语义脆点的组合。复用 direction 的省事路
(把 alpha 塞 NO_VIEW)会在 (b)(c) 各埋一个「二次判别 is-this-alpha」的脆判断,违 binding①的精神。

## §3 我现在最不确定的 3 件事

1. **OUT-10 边界判定**:改 assembler(004 spine)算不算越界?我倾向「R3-F1 是 assembler 既有 cache 完备性
   缺陷,修它是修 004 自己的 bug 不是为 alpha 特改」→ 不违 OUT-10。但若严格解「不碰 004 已 ship」,则需
   operator/forge 显式授权这是「下游集成」。这是归属定性问题,synthesizer 须给裁决。
2. **evidence_strength 进 hash 的分桶粒度**:太细(连续值)→ 每次微小强度变化都 cache miss(退化成禁缓存);
   太粗 → 强弱 alpha 又撞同桶重现 silent-wrong。需定一个像 `_confidence_bucket` 的合理分桶(几档?按显著性
   z 阈值分?)。可能超出最小契约 → 降级实现细节给 XenoDev。
3. **「非方向 evidence 怎么展示」的产品形态**是否属于 forge 该定死的,还是给 XenoDev/operator 迭代?我倾向
   forge 定**原则**(标注「旁证不计多空」+ 展示三件套强度),具体文案/emoji 给 XenoDev。但 Telegram 的
   「严格 3 行」重构是真架构改动(不只文案),这部分契约要定。

**forge-lite 自评**:若 Codex 也收敛到「(a) 轻扩一等公民 + (b) 纳入 hash + (c) Telegram 改/UI 分区」→
直接进 synthesizer 定契约。**关键待对齐点**:Codex 是否也复核出 UI router 透传(不丢)的反例 —— 若双方都
独立发现 hand-back R3-F2 对 UI 的断言不准,这个纠正就很稳。若 Codex 坚持复用 direction 或坚持两处都硬截断
→ 升级补 P2。
