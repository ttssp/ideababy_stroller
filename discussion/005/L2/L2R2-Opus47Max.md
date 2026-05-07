# Idea 005 · L2R2 · Claude Opus 4.7 · Cross + Value Validation

**Timestamp**: 2026-05-06T16:50:00Z
**Opponent's L2R1 read**: yes (GPT-5.5 xHigh,全部 §0–§6)
**Searches run**: 4 value-validation queries(Devin 实测 / addy osmani agent-skills / 「stop and ask」vs hallucinate 学术研究 / vibe→agentic 行业转向)
**Origin**: Skip-mode standard L2R2; no redebate; no moderator note.

---

## 1. From opponent's L2R1, what sharpened my thinking

**(a) "最高自动化 ≠ 最少人工,而是最少低价值人工 + 最多可审计信心"**——GPT 这句把我之前一直绕的话说清楚了。我 R1 里用「工程纪律硬连线」描述同一件事,但描述偏机械(像 Toyota 生产线)。GPT 的「裁决经济学」(高杠杆决策保留 / 低价值救火外包)更贴合用户实际体验——human 不是想消失,是想从频繁救火升级为少量高价值裁决。这把 005 的体验设计变得更清晰:**管道不是无人化,而是把 human 从 lvl-1 救火员升级到 lvl-3 裁决者**。

**(b) "抗重做"作为核心约束**——GPT §0(D) 直接点出"前 4 次尝试连续 deprecate"这个事实,并把"第 5 次不能也是 deprecate-then-redo"提为本 idea 的硬约束。我 R1 §6 第 3 题问的也是这件事,但 GPT 把它从"问题"升级为"约束"——005 的设计要求**结构上抗重做**,而不是只看做出来好不好用。这是个更狠的 framing,它直接判 idea_gamma2 / vibe-workflow / autodev_pipe 这些"完整重做型"的方案为反面教材,任何 005 的候选设计都必须能演化、不能要求 v0.1 → v1.0 推倒重来。这个约束很硬,值得带进 L3。

**(c) "强需求表达者 + 弱工程交付直觉者"作为用户画像精确化**——我 R1 用"产品型创造者"形容用户,GPT 用更精准的二元分裂"能写 PRD 但缺工业肌肉记忆"。这个差别看似小,实际很重要:它把用户和"什么都不会的小白"以及"已经会写代码的开发者"都干净切开。这是 005 真正的甜蜜带。L3 写 PRD 时,目标用户必须用 GPT 这个定义,不能漂回成"非程序员"。

---

## 2. Where I'd push back on opponent's L2R1

**(a) GPT §3 场景三低估了"未必每次失败都能转化为下次更少返工"**。GPT 写"这次失败没有白费,它变成下一次更少返工的依据"——这是个**非常乐观的假设**,需要架构上专门的设计才能成立。如果只是"把每次的 retro 写下来",大概率是死档案,下一个项目根本不会读。real talk:human 自己已经有 4 次完整 retro 了(idea_gamma2 / vibe-workflow / autodev_pipe / 当前 repo),但每次仍是从零搭脚手架。这说明**仅靠"沉淀"不够,需要"可被自动调用的沉淀"**——这一点 GPT 没说透。我会在 L3 里把这个推到"系统必须主动 surface 历史决策"而不是被动归档。

**(b) GPT 的「治理框架」措辞太管理化**。我担心这个词会把 005 的实操形态推向"流程图、表格、汇报"这一类"看起来专业但产物薄"的东西。我自己 R1 也犯了类似的毛病——「Toyota 类比」也容易被读成"流水线管理"。两个 framing 都需要在 L3 阶段被**反向锚定到具体动作**(管道在 PRD 不清时具体如何停 / 具体如何把决策点暴露给 human / 具体如何让 retro 喂回到下次项目),不能停留在抽象的「制度」「治理」「纪律」语义层。

**(c) GPT §6 第 2 题问"过去 4 次为什么不满意",但没有把这个问题倒过来问 human**。这是个 L3 必须问 human 的问题——不是 L2 能在 imagination 层回答的。但 GPT 的措辞让它看起来像是 L2 该回答的。我会在我的 §5 把这条明确移交给 L3 user research。

---

## 3. Search-based reality check

| Claim | Source side | What I searched | What I found | Verdict |
|---|---|---|---|---|
| "完全无人化的 agentic coding 已被市场证明产物不可信"(Opus §2 / GPT §0(B)) | both | Devin AI reliability 2025 实测数据 | Answer.AI 测试 Devin **15% 成功率**,Cognition 自报 PR merge rate 从 34% → 67%(仍 1/3 需大改);"Devin frequently pushed forward with a wrong or impractical solution instead of pausing"。see [The Register](https://www.theregister.com/2025/01/23/ai_developer_devin_poor_reviews/) / [Futurism](https://futurism.com/first-ai-software-engineer-devin-bungling-tasks) | **强证实**——纯无人化路线 1.5 年后仍在 ~67% 上限,且失败模式正是"碰到 ambiguity 时硬推而不停下"。这是 005 不能走的路。 |
| "PRD ambiguity 时停下问 vs 硬推"是核心未解张力(Opus §6 Q1) | opus | 学术研究 / Anthropic 官方表述 | **arxiv 2502.13069**(Stanford+CMU)直接证明:"LLMs default to non-interactive behavior...struggle to distinguish underspecified and well-specified inputs";强制 interaction 后性能 +74%,但仍只达 full-spec 的 80%。Anthropic 公开称"trains Claude to ask clarifying questions"。see [arxiv](https://arxiv.org/html/2502.13069v1) / [Anthropic](https://www.anthropic.com/research/measuring-agent-autonomy) | **强证实+开放**——市面 SOTA 模型也搞不清"该不该问",这是个仍未解决的研究问题。005 不能假设"模型自己判断 ambiguity",必须设计**结构化的 ambiguity-surfacing checkpoint**(L4 议题)。 |
| "addy osmani agent-skills + 自演进 agent 已经把工程纪律 + 复盘环搭起来,005 的 novelty 不在概念在落地"(Opus §2 / GPT §2) | both | addy 全集(agent-skills / self-improving / how-to-spec / agentic-engineering) | addy 已发布:**20 skills + 7 commands** + **AGENTS.md 自累积机制**(`agents update AGENTS.md - discovered patterns are documented`)+ how-to-write-good-spec 完整指南。Agent Skills 已是 production-grade。see [addyosmani.com/agent-skills](https://addyosmani.com/blog/agent-skills/) / [self-improving](https://addyosmani.com/blog/self-improving-agents/) | **大量证实**——概念层全被覆盖,005 必须诚实承认"概念 novelty 接近 0"。**但**:addy 的累积是**项目级 lore**(per-codebase),不是**用户级 calibration**(GPT 强调的"个人风格画像")。这个空白真存在。 |
| "vibe coding → agentic engineering 转向"作为 2026 行业 baseline | both | HN/Reddit/产业评论 | Amazon **Q3 2025 因 AI coding assistant 事故 ordered 90-day deployment freeze**;HN 2026/3 有"corrections coming"评论。"vibe coding fails when code moves from prototype to production...skips design, review, and testing"——产业共识。see [The New Stack](https://thenewstack.io/vibe-coding-agentic-engineering/) / [arxiv 2505.19443](https://arxiv.org/html/2505.19443v1) | **强证实**——005 是 2026 主流路径,不是逆潮流。市场对"可信赖 agentic"的需求是真的。但同时意味着**竞品很多+定位必须精准**,005 的差异化不能模糊。 |
| "强需求表达者 + 弱工程直觉者作为用户画像有市场"(GPT §1) | gpt | Reddit / HN 用户群体语言模式 | 从 Anthropic 的 measuring-agent-autonomy 数据看,该公司明确把"人类不在 loop 但保留高杠杆 decision points"作为研究方向;但**没有公开数据证明这类用户群体规模**。see [Anthropic](https://www.anthropic.com/research/measuring-agent-autonomy) | **概念合理但群体规模未证实**——这是 L3 user research 必答题。L2 imagination 给不出答案。 |

---

## 4. Refined picture

经过 R1 + 4 次 search,005 的精确读法是:

> **「为强需求表达者 + 弱工业交付直觉者设计的 PRD-driven 开发协作制度,核心赌注不在"agent 能写代码",而在两个 search 已证实的市场空白:(1) 把"ambiguity 检测 + 暴露 + 裁决"做成结构化 checkpoint(arxiv 2502.13069 证实这是 SOTA 模型仍无法靠自身判断的 hard problem);(2) 把 addy 已经做的"项目级 AGENTS.md 累积"扩展为"用户级长期 calibration profile"(addy 自己没走到这一步)。其他部分(spec-driven / TDD-gate / review-mandatory) 全部承认是站在 addy osmani agent-skills 的肩膀上,005 的差异化只在这两点;不在这两点上的 effort 是浪费。」**

这个 framing 比 R1 收紧了——R1 时我以为"工程纪律硬连线"是 005 的 novelty,search 显示 addy 已经做完了大部分。**真正的 novelty 是把现有 SOTA 的两个明确缺口(ambiguity 处理 + personal calibration)做对。**这是个比 R1 更窄、但更可验证的位置。

---

## 5. Open questions L2 cannot answer (for L3 / user research)

1. **「ambiguity 暴露 checkpoint 的频率/形式 trade-off」是 L3 PRD 的核心选项**——每个 PRD 不清的点都要 human 拍板(自动化承诺破灭)? 还是允许管道做"暴露+合理推断+TODO 标"?(005 倾向后者,但具体在哪些类型决策上允许哪些类型不允许,L3 必须明确)
2. **L3 必须问 human:在你的 4 次尝试里,真正让你不满意的是产物质量、还是流程难复用、还是失败时不知道为什么失败?**(GPT §6 Q2 问得对,但答案只有 human 能给——L2 给不了)
3. **「用户级 calibration profile」是否过早?**——这是 §4 我说的 005 真正 novelty 之一,但它需要**用户运行 ≥5 个项目才能开始有 signal**。v0.1 是不是必须包含这个,还是 v0.2 再加? L3 必须做这个 scope 决定。
4. **资源现实:human 能花多少时间在这个上?**——L3 的硬约束。如果是周末项目,005 v0.1 的 scope 应该极小(只做 ambiguity surfacing 一件事 + 复用 addy agent-skills);如果是 4 个月专注项目,可以同时做 calibration + ambiguity。
5. **failure mode 容忍度**:管道偶尔产出"看起来 OK 但深处有问题"的代码,human 如何抓出?——光靠 test pass 不够(Devin 数据证明)。L3/L4 需要明确"产物可信"的硬标准。

---

## 6. Three things I'd want a real user interview to ask

如果可以面对 5 位"会写 PRD 但没工程肌肉"的目标用户,我最想问:

1. **回放过去你让 AI 帮你做开发的最近 3 次:你"信任产物"的时刻和"完全不信"的时刻分别是什么?具体是什么信号让你切换信任状态?**——这个问题可以反向倒推"可信"的真实定义,比直接问"什么算可靠"准确得多。
2. **当 AI agent 给你一个"看起来合理但 PRD 里没写"的方案选择(如:"你没说支持 HEIC,我加了"),你的真实第一反应是?(感激?警惕?忽略?)**——这个直接告诉我们 ambiguity-surfacing checkpoint 应该多 verbose / 多频繁。
3. **你有多大概率会读 agent 写的 retro/changelog/decision log?如果你不读,你期望谁来读?**——这个回答决定了"用户级 calibration profile"的可行性。如果用户自己不会读、也没委托 agent 读,calibration 就是死档案。
