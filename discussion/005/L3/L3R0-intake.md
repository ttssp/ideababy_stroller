# L3R0 · Human Intake · 005

**Captured**: 2026-05-07T01:52:12Z
**Method**: AskUserQuestion interactive (8 个问题分 6 批)
**Source**: 直接来自 L2 stage doc(`stage-L2-explore-005.md`),verdict = Y-with-conditions
**Idea**: auto agentic coding(PRD-to-confidence framework)

---

## Block 1 — Time reality

### Q1. 目标交付时间(v0.1 多快交到用户手里)
- ❓ Human 不确定 → "先不定 — 让模型先 scope 再匹配时间"
- **L3R1 必须**:在每个 candidate 下给出对应的诚实时间估算(用 Q2 的周小时数倒推),让 human 在看完候选后再决定接受哪个时间窗口

### Q2. 周投入小时
- ✅ "15-30 小时(认真投入) / 30+ 小时(几乎全职)"——选了**两个上区间合并**
- **解读**:human 把 005 当成主力项目,不是周末项目。可投入的真实 weekly hours **≈ 20-35 小时**,中位数取 **25 小时/周**。L3R1 的时间估算要按这个区间算。

---

## Block 2 — Audience reach

### Q3. v0.1 优先服务哪类用户
- ✅ Human 选了 **option 2 + option 3**(非互斥多选,human 显式答"2 和 3"):
  - **Persona A · ML 研究员 / CS PhD 型**——能写出质量 PRD 但缺工业交付肌肉肉。包含 human 自己 + 同类(实验室同事 / 另一位独立开发者)
  - **Persona B · 独立创业者**——有产品判断、会写 PRD,需要从 demo 跨到正式产品
- **L3R1 注意**:不是"只服务 human 自己",所以 005 的 scope 必须**考虑「不是我」的人能上手**。但也不是面向所有非程序员——切在 GPT R2 §1 那个"强需求表达者 + 弱工业交付直觉者"的二元定义上
- **隐含取舍**:Persona A 和 B 的差异——A 更偏内部工具/研究项目(可以容忍更技术化的 UI),B 更偏 demo→产品转化(需要更可视化的"信心地图")。L3R1 必须显式处理这个张力,不能含糊带过

---

## Block 3 — Business model

### Q4. v0.1 商业模式
- ✅ "现在免费 / 后续可能付费 tier"
- **解读**:不锁死路径,v0.1 拉人走得通,后期如果出现 PMF 信号再考虑加付费层。最灵活的选项。
- **L3R1 注意**:scope 不必为付费 tier 预留 hook,但**要避免**做出"未来不可能商业化"的架构决定(例如硬绑定免费 LLM API)

---

## Block 4 — Platform preference

### Q5. 平台/形态
- ✅ "无偏好 — 选最适合 idea 的"
- **L3R1 注意**:**这是 L3 的真实 scope 决策**(L1/L2 不能讨论,L4 不该决策),候选之间应**显式以 form factor 为差异轴**——例如"CLI/Claude Code skill"vs"Web dashboard"vs"Desktop app"——让 human 看到不同 form factor 如何影响"信心地图"的呈现和"用户级 calibration"的累积方式

---

## Block 5 — Red lines

### Q6. v0.1 绝对不做的事
Human 显式选择了 **3 条 + 让模型再提 3 条**(全 4 个选项都勾):

- ✅ **R1**:不做"代人写 PRD"的能力——PRD 是 human 责任区。直接对应 L2 §0(C) 的拒绝
- ✅ **R2**:不做"人完全在 loop 外"的黑箱交付——必须 human-on-the-loop。直接对应 L2 §6 条件 3
- ✅ **R3**:不做多人协作功能(>2 人)——v0.1 守住"1 human + N agent"单元生产力
- 💡 **R4**:Human 同意让 L3R1 再提 **3 条**常见红线(基于 L2 "Natural Limits" §5),human 之后看菜单接受/拒绝
- **给 Opus/GPT 的提示**:R4 的 3 条候选可以从 L2 §5 中抽——例如(a) 不做"自然语言一句话生成 app"(b) 不做实时协作(c) 不做面向已有大团队/强监管行业 (d) 不变成"万能 AI 工程公司"

---

## Block 6 — Priorities

### Q7. tradeoff 冲突时哪个最重要(选 1-2)
- ✅ Human 选了 **2 个**:
  - **P1 · Differentiation**——推开 prior art,重点 ambiguity policy + 用户级 calibration
  - **P2 · Polish / UX quality**——优雅与亲和力
- **解读**(重要):
  - P1 直接执行 L2 §6 条件 1(scope 收紧到两个 novelty 缺口)
  - P2 是新信号——human 不仅要差异化,还要 v0.1 的体验**做得拿得出手**。这意味着 L3R1 的 candidates 不能是"概念验证级"的最小 demo,而要做到"看起来像产品"
  - P1 + P2 一起意味着 v0.1 即使小,也必须**在那个小切片上做到够细**——不能用"我们后期再补 polish"搪塞
  - **没选 Speed**:human 不抢时间窗,愿意为差异化和细节多花 1-2 周
  - **没选 Technical simplicity**:human 不要求路径上一定取最简(虽然 L4 会再讨论)

---

## Block 7 — Freeform catch-all

### Q8. 还有什么要在 L3R1 之前告诉模型的
- ✅ "没有 — 开始 L3R1"

---

## Summary for debaters(L3R1 必读)

### Hard constraints(必须遵守)
1. **Persona = ML 研究员/PhD 型 + 独立创业者**(二者并集,但需显式处理两者张力,不能含糊)
2. **Form factor = 候选必须以 form factor 为差异轴之一**(CLI/Web/Desktop)——这是 human 让模型选的真实 scope 决策
3. **R1-R3 红线已确认**:不代写 PRD / 不做黑箱交付 / 不做多人协作(>2 人)
4. **保留 ambiguity policy + 用户级 calibration 作为差异化核心**(直接来自 L2 §6 条件 1)
5. **必须 human-on-the-loop**(L2 §6 条件 3,把"几乎没有人工干预"重写为"几乎没有低价值人工陪护")
6. **抗重做硬约束**(L2 §6 条件 4):v0.1 不能要求 v0.1→v1.0 推倒重来。candidate 要展示能演化路径,不只是孤岛

### Soft preferences(强信号)
- **Polish > Speed**——v0.1 即使小也要做得拿得出手,没有"先粗后精"的妥协空间
- **Differentiation > Broad appeal**——宁愿少一类用户也要把核心两个 novelty 打深
- **可投入小时 ≈ 25/周**(中位数)——时间估算按这个走;最少 20、最多 35
- **不锁商业化**——免费 v0.1 但不挡未来付费 tier 路径

### ❓ Unknowns(模型必须主动给 options)
1. **目标交付时间**——L3R1 在每个 candidate 下给出诚实时间估算,human 看完再选时间窗
2. **R4 红线**——L3R1 提 **3 条**基于 L2 §5 的候选红线,human 在 R2/synthesizer 阶段挑

### 💡 L3R1 设计提示
- **候选必须 peer**——不是"main + alternatives";三个候选(如做 3 个)地位平等
- **关键张力轴需在 §0 中显式说出来**:"我看见的最重要的 scope 决策是 X 还是 Y"——这是 candidate 之间最大的差别
- 关键 scope 张力(候选的差异维度,可任选其一切片):
  - **形态轴**:CLI 工具 vs Web dashboard vs Desktop app
  - **持久度轴**:single-shot 工具(每次新跑) vs 累积型工具(用户级 calibration 从 v0.1 就开始)
  - **服务对象轴**:严格服务 Persona A(技术型用户,容忍 CLI 型) vs 兼顾 Persona B(创业者,需更视觉化)
  - **范围深度轴**:做完整 PRD-to-confidence 流程一次 vs 只做 ambiguity policy 单点工具
- 时间估算用 25 小时/周中位数,可分别给出乐观/现实/悲观三档

### Decision criteria(L3 之后 human 用什么挑)
- candidate 在 ambiguity policy + 用户级 calibration 上是否真的差异化(P1)
- candidate 在 v0.1 那个小切片上的体验密度是否够 polish(P2)
- candidate 的演化路径是否真的"抗重做"——能从 v0.1 长到 v1.0 而不推倒
- 时间估算是否在 human 的 25h/周区间能打住
