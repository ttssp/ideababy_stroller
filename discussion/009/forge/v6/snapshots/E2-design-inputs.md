# E2 设计输入清单 + 接口草案(纯文档 · 零代码)

> **状态**:活文档(living)· 由 HANDBACK-LOG #22 决议 4 启动(2026-07-17)
> **性质**:**纸面设计输入** —— 记 E2(历史窗回测)前置发现 + 接口草案,供 E2 解锁后按单起跑。
> **不是**实装计划,**更不是**授权 E2 施工。

---

## §0 红线声明(先读 · 不可越)

per HANDBACK-LOG #22 决议 4 + forge v5 三条 BLOCK:

- **E2 / E3 = 零代码**。本文件是**纯设计输入**,不含也不触发任何回测/forward 消费方实装。
  在 XenoDev 写 E2 历史回测线 / E3 forward 确证线 = **越界 BLOCK**(证伪链哲学:上游未证真前
  下游零沉没成本 · 沉没成本会让人舍不得毙 = V4 失败模式)。
- **E2 解锁三条件(全满足才授权 · 当前均未满足)**:
  1. **真密度显著** —— 真 LLM proposer(非 literal 替身)跑真密度普查,per-market 密度足以支撑
     未来 DSR(operator 看完整报告人工终裁 · 阈值 30 是 advisory 参考非自动闸 · 决议 2)。
  2. **两层金标过** —— Layer-1 span + Layer-2 映射(真人第二源 · D-7)真验收通过(gate fail-closed
     默认关 · 未过不放行)。
  3. **operator 授权** —— 经 hand-back 决议显式授权 E2 施工。
- **本文件只增不减地积累设计输入**,E2 起跑前的每个新前置发现追加到 §2。

---

## §1 设计输入 #1(第一条 · review MED#4 known-gap · 决议 4 指定)

### gap:金标 gate 只按 caliber_version 过,不按 extractor_variant

**现状**(E1 已实装 · `extraction/gate.py` docstring 显式声明):
- `extracted_signals` / `trial_ledger` 是 **per-extractor_variant** 记账(migration 0017 · C1)。
- 但 `gold_layer1_result` / `gold_layer2_result` 表**无 `extractor_variant` 列**。
- `gate.assert_gold_passed` 只按 `caliber_version` 查两层 verdict。

**后果**:同一 `caliber_version` 下,若先验 `variant=v1` 过、后 census 出 `variant=v2` 的信号,
gate 会对 v2 也报"过"—— 而 v2 的信号**从未单独金标验收**。这是"新变体蹭旧变体的过"漏洞。

**E1 为何不修**(记录在案 · 非遗漏):E2 回测消费方本 fork 外、不存在 → 为不存在的消费方投机加列
= 过度设计。E1 选择显式声明 gap 而非静默(gate docstring + E1 hand-back 已交 operator)。

### E2 须做(设计输入 · 待 E2 解锁后实装)

1. **schema**:`gold_layer1_result` + `gold_layer2_result` 各加 `extractor_variant TEXT NOT NULL` 列
   (新 migration `0018+` · forward-only · 不改 0017 已 ship 表体 · 遵 C7 只 ADD)。
   - ⚠ 迁移历史数据:0017 建表时若已有金标行(本 fork 无真跑 → 无历史行),回填策略在 E2 设计时定
     (建议:无历史行 → 直接加 NOT NULL 列;有历史行 → 加列 + 显式回填已知 variant 或标 `unknown`)。
2. **gate WHERE 加维**:`_latest_passed` / `_both_layers_passed` / `assert_gold_passed` 的签名 +
   查询都加 `extractor_variant` 参数,令每 `(caliber_version, extractor_variant)` **各自独立**过两层才放行。
3. **mutation-killer 扩**:现 `test_gate_assertion_has_teeth` 扩一例 —— variant=v2 未验收时 gate 对
   v2 报"未过"(证加维后不再蹭 v1 的过)。
4. **census/金标写侧对齐**:金标验收写 `gold_layer*_result` 时必带 `extractor_variant`(与 census 写
   `extracted_signals` 的 variant 一致)。

---

## §2 E2 接口草案骨架(待细化 · 后续前置发现追加于此)

> 骨架级 · 不是最终接口。E2 解锁后由 spec/task 展开。

### §2.1 E2 消费 extracted_signals 的读契约(gate 前置)

- **必经 gate**:E2 回测消费方读 `extracted_signals` **前**必须先过
  `gate.assert_gold_passed(caliber_version, extractor_variant, conn=…)`(加维后 · §1)· 未过 raise。
  这是 C5 强门在 E2 侧的落点 —— 未过金标的信号**不得**进回测(OUT-12)。
- **读维度**:E2 按 `(caliber_version, extractor_variant, market)` 读 accepted 信号 · horizon 在
  **回测侧**选择(E2 才真按 horizon 算 realized-return · 提取侧信号无 horizon · 密度是 per-market · 决议 1)。

### §2.2 horizon 回测窗口口径(与 E0/E1 对齐)

- horizon ∈ {5, 20, 60}(合约集 · migration 0017 CHECK · M2 SLA C16)。
- **OOS 窗保留**(C12):25 底–26 初"有用"窗是 E1 口径开发/金标标注**避开**的 OOS 窗 —— E2 回测
  用它作**样本外验证**(不可用作训练/口径拟合 · 否则抄考卷)。E1 census 已 `is_in_oos_window` 排除
  该窗 record 进密度分母;E2 设计须定义如何在 OOS 窗上做 walk-forward 而不泄漏。
- **DSR/PBO 复用 M2**:E2 realized-return → alpha 显著性走 `alpha/deflate.py`(walk-forward 18/3/3 +
  `min_trials<20` → insufficient_sample · 已 ship)· `trial_ledger` e1_trial 行已按 `(variant,caliber,
  horizon,market)` 记账供 E2 交叉窗(0017 · C1)。

### §2.3 密度 advisory → E2 go/no-go 的人工闸(决议 2)

- E1 密度 verdict = `below_threshold_advisory`(< 30 参考阈值)**不自动毙** E2 —— operator 看完整
  密度报告(per-market 明细 + 拒绝构成)人工终裁。E2 设计须约定:go/no-go 决策**记入 hand-back / LOG**
  (留痕 · 不在代码里硬编 go 条件)。

---

## §3 待补前置发现(E2 起跑前 · append-only)

> 本节随 E1 放行后的 E2 前置分析持续追加。当前仅 §1 一条(决议 4 指定的首条)。

- (待补)…

---

## Provenance

- 决议 4(E2/E3 维持不授权 + 纸面设计先行 · gate variant-gap 为第一条):
  IDS `discussion/009/handback/HANDBACK-LOG.md` 第 22 条(2026-07-17)。
- variant-gap 根因:`specs/009-pM3prime/spec.md` review MED#4 + `extraction/gate.py` docstring known-gap。
- 三条 BLOCK 红线:forge v5 stage doc + 本 spec `non-goals.md` OUT-1/OUT-2。
