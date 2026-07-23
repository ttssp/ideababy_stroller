# Forge v1 · 009-pM3prime · P2 · Claude Opus 4.8 · 参照系评估(with search)

**Timestamp**: 2026-07-23T09:45:00Z
**Searches run**: 4,SOTA-benchmark(LLM-as-judge 独立性 / 多模型集成错误相关性 / 事实性抽取 vs 主观判断 / 人机标注相关性)
**Visibility**: 我已读对方(GPT-5.6-Sol)P1。

## 1. SOTA 对标

| 标的 X' | 参照项 | 它怎么做 / 发现 | 我们(D-7)怎么做 | gap | Source |
|---|---|---|---|---|---|
| D-7「Layer-2 用真人第二源避 echo-chamber」 | **"Nine Judges, Two Effective Votes"**(arxiv 2605.29800) | 多 LLM 评委面板错误高度相关:9 评委 n_eff≈2;**跨厂商不解决** —— 最相关的三对恰是跨 vendor(**Claude×Gemini φ=0.603 · GPT×Claude φ=0.588**);每族选最强反而更糟(n_eff 1.93) | 硬要 human · `:81` raise | **D-7 与 SOTA 同向** —— 异源 LLM 面板≠独立验证 | arxiv 2605.29800 |
| D-7 human 要求的必要性 | 同上 · human 对比数据 | "**Human annotator panels achieve ~2× higher n_eff (4.0–5.8 vs LLMs' 2.2–2.5)**";结论"No single LLM judge substitutes for human evaluation" | human 第二源 | **D-7 有硬数据支撑** —— 人的错误独立性实测是 LLM 两倍,非保守过度 | arxiv 2605.29800 |
| 强推理模型(GPT-5.6-Sol xhigh / Opus)当第二源 | 同上 · CoT 发现 | "**Chain-of-thought actually increases correlation** —— shared reasoning amplifies shared errors" | 议题拟用 xhigh 强模型 | **反转直觉** —— 越强推理越相关,不是越独立 | arxiv 2605.29800 |
| Layer-2 偏事实性抽取(NL→ticker 5 元组) | LLM 标注 error decomposition(arxiv 2601.11920)+ NER/span SOTA | "objective tasks(NER, span, relation extraction)LLMs match/outperform crowdworkers";**但** "task-inherent ambiguity → systematic errors 在 human 和 LLM **一致发生**" | Layer-2 机械比 5 维一致率 | **双刃** —— LLM 能力够当标注者,但**歧义处人机同错**(金标恰要抓歧义处) | arxiv 2601.11920 |
| LLM-as-judge 家族偏差缓解 | Play Favorites(2508.06709)+ self-preference 系列 | "judge from a different provider **systematically reduces family bias**"(但只减 self-preference,非消除 correlated error) | — | 换 provider 只解决"自己夸自己",**不解决"一起错"** | arxiv 2508.06709 |

## 2. 用户外部材料消化 / 对方 P1 关切

无 operator 外部链接。处理**对方(GPT-5.6-Sol)P1** + A/B P1 分野:

- **GPT P1 核心洞见"G-R1 未记录'所有异源模型对都不独立'"** → **P2 部分推翻**:G-R1 样本内确实没记异源观测,但**SOTA(2605.29800)恰好补上了这个观测 —— 异源(含 Claude×Gemini)错误相关性和同族一样高**。所以 GPT 的"外推边界待定"是对的,但边界一查就落在"D-7 那侧":异源不解决。GPT 要的证据出现了,方向对 D-7 有利。
- **A/B P1 架构维度分野(A=keep vs B=refactor)** → **我向 B 让步一半**。B 说"把治理结论焊成来源类型、没测量真正要防的相关错误 = 策略与度量耦合"——这个批评**站得住**。D-7 用 `kind=='human'` 当独立性的**代理**,确实没直接度量错误相关性。但 SOTA 又说:直接度量错误相关性在**缺 ground-truth 的金标场景不可行**(要先有"对"的答案才能算相关),所以"human 代理"在工程上可能是**唯一可落地的独立性保证**。→ 架构从 keep 微调到 **keep-but-annotate**:保留 human 硬约束,但在 schema/spec 记明"这是独立性代理,非能力门槛"。
- **对方 P1 §3.3"谁有资格定义 Layer-2 的对"** → 这是 A 侧没说透的好维度。SOTA 支持拆三层:**独立来源(错误正交)≠ 领域权威(能力)≠ 最终仲裁权(operator 不单独终审 C9)**。D-7 混谈了"领域"和"独立",这是可 refactor 处 —— 但方向不是"换成模型",是"讲清 human 要的是**独立性**"。

## 3. 修正后的视角(P1 哪些站住 / 被推翻)

- P1 判断"验证方法学 → **refactor**(D-7 把手段 human 当目的,异源模型可能够独立)" → **被 SOTA 大幅推翻**。异源(跨 vendor)LLM 错误相关性实测≈同族;强推理(CoT)更相关;人的独立性是 LLM 2倍。"异源模型可当源"缺经验支撑,**证据落在 D-7 那侧**。refactor 降级为"**refactor 措辞不 refactor 实质**":D-7 保 human,但重述"要的是错误独立性(human 是当前唯一可落地保证),非领域深度"。
- P1 判断"架构 → keep" → **部分被 B 的 refactor 推翻,收敛到 keep-but-annotate**:结构 keep,但补记"human=独立性代理"避免 B 说的"策略度量耦合"盲区。
- P1 判断"产品 → refactor(须给能真跑的路)" → **站住,但方向变**。既然异源模型不解决,能真跑的路是 **(b) 降级验收**(找一名懂美股真人标几十条 / 或只做 Layer-1 + Layer-2 标 known-limitation)或 **(c) 找真人源**,**不是 (a) 放宽到模型**。(a) 若放宽只能放宽到"独立性代理的等价物",而 SOTA 说模型不是等价物。
- **元层自证(A 侧 P1 §3.3 预警)**:本轮我俩 P1 又双双 refactor(重演 v5 回声室)。但 **P2 我主动搜到了反证并推翻了自己的 P1** —— 这恰恰是"引入正交手段(SOTA 实证)打破双模型收敛"的正确操作,印证了 G-R1 原始教训("M1 真实测 vs 纸上蓝图")。**这一步本身就是对'能否靠双模型互审自证'的否定回答:不能靠我俩收敛,要靠外部实证。**
