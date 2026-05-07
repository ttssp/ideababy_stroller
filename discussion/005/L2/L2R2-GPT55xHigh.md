# Idea 005 · L2R2 · GPT-5.5 xHigh · Cross + Value Validation

**Timestamp**: 2026-05-06T16:52:02Z
**Opponent's L2R1 read**: yes
**Searches run**: 6 thematic searches, value-validation only

## 1. From Opus's L2R1, what sharpened my thinking

第一，Opus 的“工程纪律硬连线”把我之前的“裁决经济学”变得更具体。我说 005 的关键是减少低价值人工、保留高杠杆裁决；Opus 补上了另一半：这些裁决不能只靠 prompt 里的软承诺，而要在流程语言里变成不可跳过的关口。两者合起来后，005 更像“信任生产线”，不是“更聪明的代码代理”。

第二，Opus 的 PRD ambiguity 问题抓住了核心体验。我的 R1 说 aha moment 是“知道每阶段该相信什么”；Opus 把它落到一个更尖锐的瞬间：系统遇到 PRD 没写清楚的边界时，究竟停下来问，还是合理推断并暴露决策。这个问题决定 005 是高频打断的陪护工具，还是低打扰但高可审计的异步制度。

第三，Opus 对“第五次尝试不能只是第五套流程”的担心和我的抗重做 framing 同向，但它更强调自我演进：005 必须把每次失败变成下一次流程资产。这个点让 novelty 从“个人信任系统”进一步收窄成“会积累判断史的个人自动化开发制度”。

## 2. Where I'd push back on Opus's L2R1

第一，我不同意把落点称为“PRD-driven 全自动开发管道”就够了。搜索后看，这个表述已经非常接近 Devin、Copilot agent、Superpowers、agent-skills 等方向。005 若只说“PRD 进去，可信软件出来”，novelty 会被现有 prior art 压得很薄。更强的说法应是：PRD 进去，系统先生产“哪些可自动、哪些必须裁决、哪些证据足以信任”的交付信心结构。

第二，Opus 稍微过度顺从了“几乎没有人工干预”。L2R2 的证据更支持 human-on-the-loop，而不是 human-out-of-the-loop。可靠性不是消灭人，而是把人从持续陪护变成少数裁决点；如果 005 不把“什么情况下必须问人”当成产品核心，它会重复无人化产品的常见失误。

第三，Opus 的 marketplace / SaaS 扩展可以保留为远期想象，但对 005 当前主线有稀释风险。005 首先要证明一个人能反复从 PRD 得到可信交付感；在这之前谈生态，容易让核心从“个人判断校准”滑向“工具平台”。

## 3. Search-based reality check

| Claim | Source side | What I searched | What I found | Verdict | URLs |
|---|---|---|---|---|---|
| 完全无人化 coding agent 已有真实采用，但可靠性强依赖任务是否清晰、可审查。 | Opus | `Devin 2025 performance review PR merge rate autonomous coding agent` | 二手市场分析汇总 Cognition 口径称 Devin PR merge rate 从 34% 到 67%，但同文也强调模糊需求、开放式判断和隐含约束仍是主要失败区。 | 支持 005 存在需求，但反对“无人工”作为核心承诺。 | https://agentmarketcap.ai/blog/2026/04/07/devin-67-percent-pr-merge-rate-autonomous-coding-agent-performance |
| 用户不是不想用 AI coding，而是不信任“差一点正确”的产物。 | GPT R1 | `Stack Overflow 2025 developer survey AI tools trust accuracy coding` | Stack Overflow 2025 调查显示 AI 工具使用/计划使用率高，但 46% 不信任输出准确性，45% 抱怨调试 AI 代码耗时，77% 表示 vibe coding 不是专业工作的一部分。 | 强支持：005 的价值应锚定“信任与证据”，不是“更快生成”。 | https://stackoverflow.co/company/press/archive/stack-overflow-2025-developer-survey/ |
| agent-skills / Superpowers 已经覆盖了工程纪律迁移，005 的 novelty 不能停在 skills。 | Both | `addyosmani agent-skills GitHub`, `Superpowers Claude plugin TDD code review skills` | Addy repo 明确是 senior software engineer skills 集合，含 spec、plan、TDD、review 等映射；Superpowers 插件也提供 brainstorming、TDD、debugging、subagent review 等纪律化流程。 | 削弱 novelty：005 必须新增“个人裁决预算 + 信任记忆”，否则只是本地拼装。 | https://github.com/addyosmani/agent-skills/blob/main/AGENTS.md ; https://claude.com/plugins/superpowers |
| PRD ambiguity 时“问还是猜”不是哲学问题，已有研究把它变成可验证能力。 | Opus | `Ask or Assume uncertainty-aware clarification-seeking coding agents arxiv` | 2026 arXiv 论文在 underspecified SWE-bench 变体上评估澄清能力，报告 uncertainty-aware 多代理系统达到 69.40% task resolve rate，高于标准单代理 61.20%，并能在复杂任务上更主动提问。 | 强支持：005 应把 ambiguity policy 作为核心产品语言。 | https://arxiv.org/abs/2603.26233 |
| “从项目反馈中演化 playbook”有外部研究脉络，但要防止记忆越积越糊。 | GPT R1 | `Agentic Context Engineering evolving contexts self-improving language models Microsoft Research` | Microsoft ACE 把上下文视作会演化的 playbooks，强调通过生成、反思、整理来积累策略，同时指出 brevity bias 和 context collapse 会损害长期知识。 | 支持抗重做方向，也提醒 005 的复盘资产必须可整理、可裁剪。 | https://www.microsoft.com/en-us/research/publication/agentic-context-engineering-evolving-contexts-for-self-improving-language-models/ |
| 自我感觉“AI 让我更快”不可靠，真实项目的隐性要求会放大验证负担。 | GPT R1 | `METR early 2025 AI experienced open-source developer productivity` | METR RCT 中 16 名资深开源开发者完成 246 个真实任务；允许 AI 时平均慢 19%，而参与者事前预期加速、事后仍以为加速。作者特别提醒高质量项目与隐性要求会降低 AI 帮助。 | 支持 005 的证据导向：不能用主观顺滑感当可靠性。 | https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/ |

## 4. Refined picture

经过交叉和搜索，我会把 005 精确读成：**一个面向“会写 PRD 但缺工业交付直觉”的单人操作者的 PRD-to-confidence framework**。它不是承诺把人完全移出开发，而是把人工参与重新定价：低价值陪护尽量自动化，高价值裁决被压缩、命名、记录，并和信任证据绑定。PRD 的输出不应只是任务列表或代码产物，而应是一张“自动推进区 / 必须澄清区 / 事后可审计区 / 暂停区”的信心地图。

这也解释了 005 相对 addy agent-skills 和 Superpowers 的剩余 novelty：那些 prior art 主要把工程纪律交给 agent 使用；005 应该把纪律变成一个人的长期判断系统。它要回答的不是“agent 是否遵守 TDD、review、debugging”，而是“这个操作者什么时候该放心离开屏幕，什么时候必须回来裁决，失败后哪些经验进入下一次 PRD”。因此，“几乎没有人工干预”应改写为“几乎没有低价值人工陪护”。

## 5. Open questions that L2 cannot answer

1. L3 必须定义 005 的目标用户到底是“只服务 human 自己”，还是一类 PRD 能力强、工程经验弱的创造者；这会改变语言、默认假设和成功标准。
2. L3 必须选择可靠性的主指标：少返工、敢部署、能继续迭代、失败可解释，还是 PRD 到交付过程中的心理信心。
3. L3 必须决定 ambiguity policy：哪些问题必须打断询问，哪些可以合理推断但要留下审计记录，哪些应直接暂停。
4. L3 必须界定抗重做资产的形态：是项目复盘、个人偏好画像、PRD lint 反馈，还是跨项目的决策史。

## 6. Three things I'd want a real user interview to ask

1. 你最近一次让 agent 做软件失败时，最让你失去信任的是结果错了、过程看不见、需求被误解，还是你不知道如何验收？
2. 如果一个 PRD 进入系统，你最多愿意被打断几次？哪些问题你希望它必须问，哪些问题你宁愿它先合理处理、事后报告？
3. 什么样的证据会让你敢把 agent 产物继续用于下一轮迭代：测试报告、变更解释、风险清单、review 记录、真实用户试用，还是别的东西？
