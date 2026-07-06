# Forge Stage · 009-pForge · v4 · "O8 下游集成:非方向 evidence 怎么上台"

> **forge-lite · P1-only convergence** — 本 run 只跑 P1 双方独立审(无 P2 SOTA / 无 P3 辩论)。
> 双方零分歧强收敛,三子决策全一致 → 直接 synthesizer,不补 P2。

**Generated**: 2026-07-06T06:30:00Z
**Source**: forge-lite run v4 · X = 6 标的(全真读代码), Y = 架构正确性 + 产品语义, Z = 不对标, W = refactor-plan + decision-list
**Convergence mode**: strong-converge
**Rounds completed**: P1 (both · Opus 4.8 Max + GPT-5.5 xHigh) — P2/P3 skipped (forge-lite)
**Searches run**: 0(纯内部架构审 · 不对标)
**Moderator injections honored**: none
**Convergence outcome**: converged(单一 verdict · P1 双方独立收敛 + synthesizer 已真读代码复核)

---

## How to read this

forge 是横切层(不在 L1-L4 pipeline 内)。本文档是双专家独立审 + synthesizer 真读代码复核后的
**单一 verdict**(strong-converge · 不列并行 path)。它定死 T015 hand-back 揭的 O8 下游集成缺口的
三子决策 + 落地 refactor 契约,能直接指导 XenoDev 起 FU-task。

读完你应该:
- 拿到 (a)/(b)/(c) 三子决策的定死 verdict(§Verdict + §Decision list)
- 知道 forge 复核 T015 hand-back 三断言的结果 —— 尤其 **UI 那条被纠正了**(§hand-back 断言纠偏)
- 拿到改哪些文件 / 落哪个仓 / 怎么改的 refactor 契约(§Refactor plan)
- 知道 OUT-10 边界归属 + XenoDev 该拆新 task 还是并入 T016(§落哪个仓 + OUT-10 裁决)
- 能基于 §Decision menu 直接进下一步

---

## Verdict

**采纳「轻扩一等公民 + 纳入缓存指纹 + Telegram 真改/UI 加分区」的组合路径** —— 这是三子决策里
**唯一不产生新语义脆点**的组合。

- **(a)** ConflictReport **轻扩一等公民**:StrategySignal 把 `is_directional`/`signal_kind`/`evidence_strength`
  从 `inputs_used` dict **提升为一等字段**;ConflictReport 加 `evidence_lanes` 旁路认「非方向 evidence」概念,
  **不动 3 路方向票主结构**。**拒绝复用 direction 五值**(塞 NO_VIEW 会让每个下游消费者二次判别
  "is-this-alpha",在 (b)(c) 各埋一个脆判断)。
- **(b)** 缓存键 **必须纳入 evidence 指纹**(binding②:R3-F1 silent-wrong 是硬 bug,**不可降级**)。
  triplet 扩入 `is_directional`/`signal_kind`/`evidence_strength` 桶。无法规范化的路径则**禁 cache**,
  不许静默复用旧根因。
- **(c)** Telegram **真改**(拆 `_THREE_PERMUTATIONS` 的 3 路硬假设 → 方向票 + evidence 区);
  UI **只加分区**(已透传第四路,只是没展示 evidence)。展示标注「历史 edge 旁证 · 不计入多空」防
  operator 误读(binding⑤)。

**回应 K**:守 alpha_lane NO_VIEW 语义(binding①)· R3-F1 真解不降级(binding②)· 改的是 004 spine
但定性为**授权的下游集成**非越界(binding③)· 契约可直接起 FU-task(binding④)· 产品不误导(binding⑤)。

---

## Evidence map

| 结论 | 来源 | 引用 | 是否有反对证据 |
|---|---|---|---|
| (a) 不复用 direction 五值 | P1-Opus §2 + P1-GPT §2(a) | "把语义藏在 inputs_used 会要求所有消费者二次判别" | - 双方一致 |
| (a) StrategySignal 现无一等 evidence 字段 | synthesizer 真读 `domain/strategy_signal.py:29-39` | `is_directional` 仅在 alpha_lane `inputs_used` dict | - 代码铁证 |
| (a) 用 `evidence_lanes` 旁路(非 discriminated union) | P1-GPT §3 #1(不确定点)→ synthesizer 裁决 | ConflictReport 有 `signals≥3` 硬不变量(#2) | ⚠ Codex 列为未定项 · 见 §underweights |
| (b) R3-F1 缓存 silent-wrong 是真 bug | P1-Opus §1 + P1-GPT §1 + synthesizer 真读 `assembler.py:159-164` | triplet 恒 `NO_VIEW:low` · evidence 从不进 hash | - 双方+代码三重确认 |
| (b) prompt 正文不在 cache key(唯一入口是 extras) | synthesizer 真读 `llm/cache.py:155` | `raw = week\|ticker\|version\|model\|extras_str` | - 代码铁证 |
| (b) 纳入 hash 而非禁 cache 为主解 | P1-Opus §2(b) + P1-GPT §2(b) | "禁缓存丢性能且掩盖问题;纳入 hash 是正解" | - 双方一致 |
| (c) Telegram 真丢第四路 | P1-Opus §1 + synthesizer 真读 `conflict_narrative.py:54-63` | `signals[:3]` + 3 显式 `order[0/1/2]` | - 双方+代码确认 |
| (c) UI 透传第四路(不丢)· hand-back 断言错 | P1-Opus §1 + P1-GPT §1 + synthesizer 真读 `router_conflicts.py:169-176` | `return ordered_first_three + remaining` | ⚠ 纠正 hand-back R3-F2 · 见 §纠偏 |
| (c) UI 仍误导(显示 no_view 0%) | P1-GPT §1 | "用户会看到 no_view 0% · 很难理解这是历史 alpha 旁证" | - 需产品分区解 |
| OUT-10:修 assembler = 修 004 既有 bug | P1-Opus §1 + §3 #1 → synthesizer 裁决 | "cache 键不完备本就是 bug · 只是现在才被第四路触发" | ⚠ Opus 列为最不确定点 · synthesizer 定性 |

---

## Intake recap

### X · 审阅标的(6 个 · 全真读代码)
1. T015 hand-back(R1→R3 全 adversarial 轨迹 · handback 类)
2. `conflict_report_assembler.py:159-164`(R3-F1 病灶 · 代码)— synthesizer 已真读复核
3. `telegram/conflict_narrative.py:54-63`(R3-F2 病灶之一 · 代码)— 已真读:真丢第四路
4. `ui/router_conflicts.py:169-176`(R3-F2 病灶之二 · 代码)— 已真读:透传不丢 · hand-back 断言错
5. `strategy/alpha_lane.py:239-267`(能力层 · NO_VIEW+evidence_strength 语义来源 · T015 worktree 未 merge)
6. `alpha/realized_return.py:231`(上游 signed 证据 · 为什么 alpha 只能 NO_VIEW)

### Y · 审阅视角
- 架构正确性 / 器官边界(非方向 evidence 怎么进 ConflictReport+缓存+渲染而不破「恰好 3 路方向票」不变量)
- 产品语义 / 用户可见性(alpha 质量旁证对不懂投资的 operator 怎么展示才有用又不误导)

### Z · 参照系
- mode: 不对标(forge-lite · 纯内部架构审 · 004 决策台自有器官无外部 SOTA)
- 用户外部材料: 无

### W · 产出形态
- refactor-plan ✅ · decision-list ✅(verdict-only / next-PRD / next-dev-plan / free-essay 未勾)

### K · 用户判准
守 alpha_lane 已定 NO_VIEW 非方向语义(①)· 最小冲击但 R3-F1 硬解不可降级(②)· 守 OUT-10 边界 ·
若必须改 spine/UI 明确是授权下游集成非越界(③)· 契约能直接起 FU-task(④)· 产品展示对 operator
真有用不误导(⑤)· 轻收尾 · 超最小契约就降级 v0.2 note(⑥)。

### 收敛模式
strong-converge → 单一 verdict(P1 双方零分歧 · synthesizer 真读代码复核后确认)

---

## Decision list(三子决策矩阵)

| 子决策 | Verdict(定死) | 拒绝的备选 + 理由 | 冲击面 |
|---|---|---|---|
| **(a) ConflictReport 承载** | **轻扩一等公民**:StrategySignal 加一等 `is_directional`/`signal_kind`/`evidence_strength`;ConflictReport 加 `evidence_lanes` 旁路,**不动 3 路方向票主结构** | ❌ 复用 direction 五值(塞 NO_VIEW):让每个下游消费者二次判别 is-this-alpha = 新脆点,双方 §2 一致拒。❌ 把 `signals` 升级 discriminated union:大重构 + 危及 `signals≥3` 不变量(#2),synthesizer 裁决降级(见 §残余 v0.2) | `domain/strategy_signal.py`(加字段)+ `domain/conflict_report.py`(加旁路)· 中等 |
| **(b) 缓存键语义** | **必须纳入 evidence 指纹**(硬解不降级):triplet 扩入 `is_directional`+`signal_kind`+`evidence_strength` 桶;无法规范化路径禁 cache | ❌ 只禁 cache 不纳 hash:丢性能且掩盖问题(Opus §2b)。❌ 维持现状:强/弱/error alpha 四态同 hash → silent-wrong(binding② 明令必须真解) | `assembler.py:159-164` triplet 构造 · 小改(局部) |
| **(c) 渲染** | **Telegram 真改 + UI 加分区**:Telegram 拆 `_THREE_PERMUTATIONS` 3 路硬假设 → 方向票+evidence 区;UI 加视觉分区(已透传,只补展示)。展示标注「不计多空」 | ❌ 维持 Telegram 3 行:第四路完全不可见(真丢)。❌ UI 不加分区:显示 no_view 0% 误导 operator(GPT §1)。❌ 把「怎么展示」全给 XenoDev:Telegram 3 行重构是真架构改动非文案,须 forge 定原则 | Telegram `conflict_narrative.py:54`(重构)+ UI `router_conflicts.py`(加分区)· Telegram 中等 / UI 小 |

**组合约束链**:(a) 轻扩一等公民 → 天然驱动 (b) 纳入新一等字段 hash + (c) 显式分区。三者一致
「显式区分方向票 vs 非方向 evidence」→ 唯一不产新脆点的组合。复用 direction 的省事路会在 (b)(c)
各埋一个「二次判别 is-this-alpha」脆判断。

---

## hand-back 断言纠偏(forge 对抗验证留档)

forge v4 对 T015 hand-back 的三个核心断言做了**独立复核**(双方 P1 + synthesizer 真读代码)。结果:

| hand-back 断言 | forge 复核结论 | 证据 |
|---|---|---|
| **R3-F1 缓存 silent-wrong** | ✅ **站住**(三重确认) | `assembler.py:159-164` triplet 恒 `NO_VIEW:low`;`cache.py:155` prompt 正文不进 key,evidence 唯一入口是 extras → 强/弱/error alpha 四态同 hash 复用旧根因 |
| **R3-F2 渲染丢第四路** | ⚠ **部分站住 · 必须拆两点** | Telegram(`conflict_narrative.py:54-63`)**真丢**(`signals[:3]`+3 显式 order 硬绑);UI(`router_conflicts.py:169-176`)**透传不丢**(`return ordered_first_three + remaining`)—— hand-back 把两渲染面**一概而论「都硬截断」不准**。UI 真实缺口是「混在方向票后无分区 + 显示 no_view 0% 误导」,非「丢」 |
| **三子决策互相约束** | ✅ **站住** | (a) 的选择约束 (b)(c) 的形态(候选提示 + 双方 §2 组合分析一致) |

**为什么留档**:这是 forge 对抗验证的价值。未来看 T015 hand-back 的人**必须知道 UI R3-F2 断言被纠正** ——
UI 不是「硬截断第四路」,而是「透传但展示语义不合格」。这改变了 (c) 的工作量估算(UI 只需加分区,不需
拆截断逻辑)和修法归属。**双方独立发现 UI 透传反例** → 这个纠正很稳(非单模型臆断)。

---

## Refactor plan(改哪些文件 · 落哪个仓 · 怎么改)

**落仓总述**:全部改在 **004 spine + UI/Telegram**(`XenoDev/projects/004-pB/src/decision_ledger/`),
**不在 009 fork 内**。理由 + OUT-10 归属见下一节。alpha_lane 能力层(009-pForge/T015 worktree)保持不动 ——
它已正确定死 NO_VIEW+evidence 语义,下游接住即可。

### 模块 A · (a) 承载 — `domain/strategy_signal.py` + `domain/conflict_report.py`
- **当前问题**:StrategySignal 只有 `direction`/`confidence`/`inputs_used`(dict);`is_directional`/`signal_kind`/
  `evidence_strength` 藏在 alpha_lane 的 `inputs_used` dict(`alpha_lane.py:263-265`),**非一等字段** →
  所有下游要 dict-dig + 二次判别。ConflictReport 只有 `signals` 槽,无非方向 evidence 的一等位置。
- **目标态**:一等字段,下游 typed 读取不二次判别。
- **改造步骤**:
  1. StrategySignal 加一等字段:`is_directional: bool = True`(默认 True 向后兼容 3 路方向票)、
     `signal_kind: str = "directional"`、`evidence_strength: float | None = None`。alpha_lane 改为填一等字段
     (从 `inputs_used` 移出 · 但 `inputs_used` 里可保留供 audit)。
  2. ConflictReport 加 `evidence_lanes: list[StrategySignal] = []` 旁路(**默认空** → 现有 3 路方向票报告零冲击)。
     assembler 装配时把 `is_directional=False` 的 signal 分流进 `evidence_lanes`,方向票仍进 `signals`。
- **裁决 §3 双方不确定点(Codex #1:旁路 vs discriminated union)**:**倾向 `evidence_lanes` 旁路,不升级
  discriminated union**。理由:binding② 最小冲击;ConflictReport 有 `signals≥3` 硬不变量(#2,`conflict_report.py:35-43`)
  + R10 红线(无 priority/winner),discriminated union 大重构会牵动这两个不变量的所有校验点 →
  牵动无关 task(违 binding③「改动可控」)。discriminated union 若未来真需要 → §残余 v0.2 note。
- **风险**:`signals≥3` 不变量校验 —— 若把 alpha 移出 `signals` 进 `evidence_lanes`,须确认剩余方向票仍 ≥3
  (T015 场景是 3 方向票 + 1 alpha = alpha 走旁路后方向票恰好 3,不破不变量;但若未来 alpha 挤掉方向票要防)。
- **预估代价**:M(两个 domain 模型加字段 + assembler 分流逻辑 + alpha_lane 填一等字段)。

### 模块 B · (b) 缓存 — `services/conflict_report_assembler.py:159-164`
- **当前问题**:triplet = `{source_id}={direction.value}:{confidence_bucket}`,evidence_strength 从不进 hash;
  `cache.py:155` 证实 prompt 正文不进 cache key → evidence 唯一入口是 `cache_key_extras`。强/弱/error alpha
  四态同 hash = R3-F1 silent-wrong(硬 bug)。
- **目标态**:evidence 强度变化 → signals_hash 变 → 不复用旧根因。
- **改造步骤**:
  1. triplet 构造扩入 evidence 维度。方向票段保持 `{source_id}={direction.value}:{confidence_bucket}`;
     非方向 evidence 段改为 `{source_id}={signal_kind}:{is_directional}:{evidence_bucket}`
     (`evidence_bucket` = evidence_strength 分桶)。
  2. `evidence_strength` 是 float → **必须分桶**(像 `_confidence_bucket`)避免连续值 hash 爆炸退化成禁 cache。
  3. 无法规范化的路径(如 provider-error/no-provider 携带 `reason`/`error_type`)→ 把 `reason`/`error_type`
     也纳入 triplet;若某路径真无法规范化 → **该路径禁 cache**(`cache_lookup=False`),不许静默复用旧根因。
- **裁决 §3 双方不确定点(Codex #2:非方向 evidence 是否参与 `has_divergence`/`divergence_root_cause`)**:
  **参与 PROMPT(故必须进 cache 语义键),但不翻转 `has_divergence`**。理由:`has_divergence` 语义是**方向票间**
  的分歧(strategy_signal 方向冲突),非方向 evidence 不是方向票,不应改变「有无方向分歧」的判定。
  但 evidence 强度会进 prompt 影响 `divergence_root_cause` 的措辞(如「方向分歧 + 分析师历史 edge 强/弱」)→
  故 evidence 指纹**必须**进 cache 键(否则 root-cause 措辞对不上强度 = silent-wrong)。定性:evidence = 报告
  **附注**(影响 root-cause 上下文),非分歧计票项。
- **evidence_strength 分桶策略裁决**:默认**按显著性分档**(而非固定等距 bins)——
  `strong`(|z|≥2.58 / 99%)· `moderate`(1.96≤|z|<2.58 / 95%)· `weak`(|z|<1.96 显著性不足)· `none/error`。
  理由:显著性档位是产品语义边界(与 §c 展示对齐),比等距 bins 更抗「强弱撞桶重现 silent-wrong」。
  **具体档位阈值 = XenoDev 实现细节**(可迭代 · 见 §残余 v0.2 note),但「按显著性分档非等距」是 forge 定的原则。
- **风险**:分桶太粗 → 强弱 alpha 撞同桶重现 silent-wrong(Opus §3.2);太细 → 退化禁 cache。默认三档
  (strong/moderate/weak)+ 与 §c 展示同源是折中。
- **预估代价**:S(局部改 triplet 构造 + 加一个 `_evidence_bucket` helper)。

### 模块 C · (c) 渲染 — `telegram/conflict_narrative.py:54` + `ui/router_conflicts.py`
- **当前问题**:Telegram `signals[:3]`+`_THREE_PERMUTATIONS`(3! 排列)+3 显式 `order[0/1/2]` → 第四路完全不可见
  (真丢)。UI `return ordered_first_three + remaining` 透传第四路,但模板只渲染 direction/confidence/rationale,
  **不渲染 evidence_strength** → 用户看到 `no_view 0%` 误读(GPT §1)。
- **目标态**:方向票区 + 非方向 evidence 区显式分开;evidence 展示「历史 edge 旁证」语言标注「不计多空」。
- **改造步骤**:
  1. **Telegram(真改 · 中等)**:重构 `build_narrative`,从「严格 3 行」改「方向票区(N 行 · 现有 permutation
     逻辑保留给方向票)+ 可选 evidence 区」。拆 `_THREE_PERMUTATIONS` 的「恰好 3 路」硬假设 →
     permutation 只作用于 `report.signals`(方向票),evidence 区独立渲染 `report.evidence_lanes`。
  2. **UI(只加分区 · 小)**:`router_conflicts.py` 排序逻辑保持(已透传);模板加「方向票 / 非方向 evidence」
     视觉分区,evidence 区渲染 evidence_strength 等字段。**不需拆截断逻辑**(它本就没截断)。
- **产品语义定原则(binding⑤ · 裁决 Codex §3 #3:只给 evidence_strength 够不够)**:**给全,不只给
  evidence_strength**。非方向 evidence 展示为「📊 分析师历史 edge:strong/moderate/weak · 命中率 X% ·
  超额 Y% · 样本 N 笔 · horizon · 显著性(z / DSR)」,**显式标注「参考旁证 · 不计入多空方向」**。
  理由:binding⑤ 产品不误导优先;只给「strong」不给样本数/显著性,operator 无法判断这个 edge 可不可信
  (小样本的 strong 是噪声)。具体文案/emoji = XenoDev 实现(见 §残余 v0.2 note),但「给全 + 标注不计多空」
  是 forge 定的产品原则。
- **风险**:Telegram 重构若破坏现有 3 方向票的 permutation 随机化(R2 D22 `rendered_order_seed`)→ 须回归。
  evidence 区若展示不当仍可能被 operator 当第四票 → 「不计多空」标注是硬要求。
- **预估代价**:Telegram M(重构 permutation 假设)· UI S(加分区展示)。

---

## 落哪个仓 + OUT-10 归属裁决

**落仓**:全部改 004 spine(`domain/` + `services/` + `telegram/` + `ui/`),**不在 009 fork 内**。
alpha_lane 能力层(009-pForge/T015)不动。

**OUT-10 归属裁决(Opus §3.1 最不确定点)**:分两类定性 ——

1. **(b) assembler cache 修复 = 修 004 自己的既有 bug**(**非**为 alpha 特改 · **不违 OUT-10**)。
   定性理由:assembler 是「装配台」,**本就该正确 hash 所有影响输出的输入**。cache 键不纳入携带信息的输入
   是**既有正确性缺陷**(cache 键不完备本就是 bug),只是「direction 恒定但携带信息在别处」的第四路第一次
   触发它暴露。修它 = 修 004 的 completeness bug,属 004 自身职责。

2. **(a) domain 加字段 + (c) 渲染分区 = T015 授权的下游集成**(改 spine/UI · 但**是授权集成非越界**)。
   定性理由:O8「alpha 平权进 conflict_reports」是 D-M2-1 已定义的下游目标,T015 hand-back 明确揭这是
   「下游承载缺口」。改 domain/渲染承载新 lane 是**兑现 O8 定义**,非临时越界改 004 语义。binding③ 满足条件:
   ①不改 004 已 ship 的**方向票语义**(3 路方向票主结构+不变量+R10 全保留)· ②旁路默认空 → 现有报告零冲击 ·
   ③改动可控(不牵动无关 task)。

**XenoDev FU-task 边界裁决(binding④)**:**拆新 task「009-pForge O8 下游集成」,不并入 T016**。理由:
- 这是**跨三模块**(domain + services + telegram/ui)的独立集成工作,有自己的验收(§可测验收),
  语义边界清晰(承载非方向 evidence),不该混入 T016 的其他 scope。
- 依赖 alpha_lane(T015)已 ship 的能力层 → 是 T015 的**下游 follow-up**,新 task 更利于追溯「O8 缺口 →
  forge v4 定契约 → FU-task 落地」的链路。
- 新 task 建议 ID:`O8-下游集成`(或 XenoDev 侧命名规范的等价)· 引用本 stage doc 为 spec 输入。

---

## 可测验收

新 task 落地须通过(mutation-killer 优先):

- **(b) 缓存修复(mutation-killer)**:构造**强 alpha vs 弱 alpha**(evidence_strength 分属不同显著性档)→
  断言两者 `signals_hash` **不同** → 不复用同一 `divergence_root_cause`。再构造 provider-error vs no-provider →
  hash 亦不同。**杀掉「evidence 不进 hash」的 mutation**(把 evidence 段从 triplet 删掉应导致测试失败)。
- **(c) Telegram**:第四路 alpha 在 Telegram 输出**可见**(evidence 区存在 · 现有 3 方向票行不变)。
  断言 `_THREE_PERMUTATIONS` 重构后方向票 permutation 随机化(R2 D22)仍工作。
- **(c) UI**:方向票区 / evidence 区分区渲染 · evidence 区显示 evidence_strength + 样本数 + 显著性 ·
  **含「不计入多空」标注**(operator 不误读断言 —— 断言渲染输出含该标注文案锚点)。
- **(a) 不变量守恒**:`signals≥3`(#2)+ R10(无 priority/winner)在加 `evidence_lanes` 后仍成立;
  现有全 3 方向票报告(`evidence_lanes` 空)行为**逐字节不变**(向后兼容回归)。
- **全 004 套回归**:改 domain/assembler/渲染后,004-pB 现有测试全绿(防牵动无关 task · binding③)。

---

## 残余降级 v0.2 note(超出最小契约)

以下超出本 forge 最小契约,降级为实现细节 / 未来项(binding⑥):

- **evidence_strength 分桶档位阈值**:forge 定「按显著性分档(非等距 bins)」原则 + 默认 strong/moderate/weak
  三档;**具体 z 阈值 / 是否加更细档 = XenoDev 实现可迭代**。
- **Telegram/UI evidence 区具体文案 + emoji + 排版**:forge 定「给全(强度+样本+显著性)+ 标注不计多空」
  产品原则;**具体文案/视觉 = XenoDev 实现**。
- **ConflictReport `signals` 升级 discriminated union**:本 forge 裁决用 `evidence_lanes` 旁路(最小冲击)。
  若未来非方向 evidence **类型增多**(不止 alpha_quality)导致旁路 `list` 不够表达 → 再起 forge 议
  discriminated union 大重构。**当前不做**。
- **多 alpha / N 路 evidence**:本契约按「3 方向票 + 1 alpha」的 T015 场景定。若未来 evidence lane >1 路,
  分区渲染的排序/折叠策略需补(当前 evidence 区可简单列表)。

---

## What this menu underweights(强制自批判)

诚实标注本 stage doc 可能 underweight 的点。这是质量栏。

- **forge-lite + strong-converge 回声室风险(最大 underweight)**:双方 P1 都聚焦 R3-F1(缓存)/R3-F2(渲染)
  两个 hand-back 已点名的病灶。**没有独立扫「O8 平权是否还击穿别的下游消费点」**。未对抗验证的假设:
  - **只有 2 个渲染面(Telegram+UI)?** 双方读了这两个,但**没穷举** `report.signals` 的所有消费者。
    若存在第三个渲染/导出面(如 CSV 导出 / 别的 telegram 卡片 / API 序列化)也硬假设 3 路 → 会漏。
    → **FU-task 起手应先 grep 全仓 `report.signals` / `[:3]` / `_THREE_PERMUTATIONS` 的所有引用点**再动手。
  - **evidence lane 进 ConflictReport 后,conflict 检测/装配逻辑是否要改?** 本 doc 裁决 evidence 不翻转
    `has_divergence`,但**没验** assembler 的 `_build_prompt`(`assembler.py:192+`)在有 evidence_lanes 时
    prompt 怎么组织 —— 若 prompt 仍只喂 3 方向票不提 evidence,则 evidence 进了 cache 键却没进 prompt =
    hash 变了但输出不变的**新不一致**。**FU-task 须确认 evidence 同时进 prompt 和 cache 键**(§b 已要求,
    但 prompt 组织的具体改动本 doc 未展开 —— 属 underweight)。
  - **`all_no_view` 短路**(`assembler.py:205`):现有逻辑「全 no_view → 暂无分歧」。alpha 恒 NO_VIEW →
    若某场景方向票也全 NO_VIEW + 1 alpha,`all_no_view` 会 True 走短路,evidence 可能被吞。**未验此边界**。
- **Y 视角覆盖盲区**:Y 只含架构正确性 + 产品语义,**未含安全/性能**。禁 cache 路径的**性能退化**未量化
  (若很多路径无法规范化 → 大量禁 cache → LLM 调用成本上升);evidence 进 prompt 的**注入面**未审
  (evidence rationale 是否也需像 `_sanitize_signal_text` 那样防注入 —— `assembler.py:211` 现有 sanitize 只
  包方向票 rationale)。
- **K 中未充分回应**:binding⑥「轻收尾」—— 本 doc 偏详(refactor 契约较重),但 W 勾了 refactor-plan 故必要。
- **X 标的覆盖局限**:未读 assembler 的 `_build_prompt` 全文(只读 triplet 段 L142-218)· 未读 UI 模板
  `_three_columns.html`(Codex 提到但 synthesizer 未亲读)· 未读 T016 现状(故「拆新 task vs 并入 T016」
  裁决基于 scope 边界推理,非读 T016 内容)。
- **forge versioning 提示**:若 XenoDev build-time **复现测**发现 (a) 旁路破坏了某个未预见的 `signals`
  消费者,或 (b) 分桶粒度实测重现 silent-wrong,或发现第三个渲染面 → 触发 v5(记 dogfood-backlog 攒批回)。
  **重视 MEMORY 教训**:forge 理论决议会漏实证盲区(DB 语义/并发/原子性),009 一周期内已有 F6 幻影 bug +
  two-SELECT 原子性两次被 build-time 杀 —— 本 verdict 的「evidence 进 hash 就不 silent-wrong」是**推演**,
  **XenoDev 复现测(强弱 alpha 真跑一遍看 hash 真不同 + 根因真不复用)是最后防线**,别只信本 doc 推演。

## Decision menu(for human)

### [A] 接受 verdict → XenoDev 起 FU-task(下游集成)
```
本 forge W 未勾 next-PRD → 无 PRD draft 可直接进 /plan-start。
本 verdict 是**下游集成契约**,直接指导 XenoDev 起 FU-task(不走 IDS L4 plan-start):

1. 新开 XenoDev session(cd /Users/admin/codes/XenoDev && claude)
2. 起新 task「009-pForge O8 下游集成」(不并入 T016 · 见 §落哪个仓裁决)
   - spec 输入 = 本 stage doc §Refactor plan + §可测验收
   - 落仓:004-pB spine(domain/services/telegram/ui)· alpha_lane 不动
3. FU-task 起手先 grep 全仓 `report.signals`/`[:3]`/`_THREE_PERMUTATIONS` 所有引用点
   (§underweights 要求 · 防漏第三个消费面)
4. 按 §可测验收 TDD(mutation-killer 优先:强/弱 alpha hash 真不同)
```

### [B] 跑 forge v5(说明需要补什么)
```
/expert-forge 009
# Phase 0 intake 调整 X/Y/Z/W/K · 旧 v4 整目录保留
```
适用:若你认为 §underweights 的回声室风险需**独立 P2/P3 对抗**(如穷举下游消费面 /
审 prompt 组织 / 量化禁 cache 性能),或想加安全视角审 evidence 注入面。

### [C] 局部接受
- ✅ 采纳:(a)/(b)/(c) 三子决策 verdict + OUT-10 归属裁决 + FU-task 拆分
- ⏸ 挂起:evidence_strength 具体分桶阈值(§残余 v0.2 · 等 XenoDev 实测)· discriminated union(不做除非
  evidence 类型增多)
- ❌ 拒绝:(留空 · 无建议拒绝项)

### [P] Park
```
/park 009-pForge
```
保留所有 forge 产物 · 标暂停。复活不重做本层。

### [Z] Abandon
```
/abandon 009-pForge
```
(不适用 · O8 下游集成是 009 闭环蓝图的兑现项,非该放弃的方向。列出仅为菜单完整。)

---

## Forge log
- v4: 2026-07-06 — verdict: "O8 下游非方向 evidence:轻扩一等公民(evidence_lanes 旁路)+ 缓存纳 evidence 指纹(R3-F1 硬解)+ Telegram 真改/UI 加分区 · OUT-10 判为授权下游集成 · 拆新 FU-task"
- v3: 2026-07-03 — verdict: "provider 分离双 as_of 轴契约(factor_as_of 分离双轴)· entry 价执行时可见 PIT 严格 · 解 T012 R6 BLOCK"
- v2: — verdict: "七环节闭环蓝图 · PIT 层唯一新器官 · Strangler M1-M4"(已接受 · M1 已 ship)
- v1: — verdict: "集成契约 + 共享回测地基"(已接受)
