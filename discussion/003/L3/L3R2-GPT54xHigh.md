# Idea 003 · L3R2 · GPT-5.4 xhigh

**Timestamp**: 2026-04-24T06:55:15Z  
**Opponent's L3R1 read**: yes  
**Searches run**: 6, scope-reality only

## 1. From opponent's candidates — what sharpened my thinking

- Opus R1/R2 最有价值的修正，是把“3-worker forum/orchestrator 就是产品灵魂”主动降级了。搜索后我同意这点：并行 worktree、dashboard、自动路由反馈已经是成熟主题，不足以构成 v0.1 的主卖点。
- 他把“会涉及一些后训练”当成一等信号，这比我 R1 更坚决；现在我接受这个更新。纯 prompt/playground 型 cut 依然能做，但更像学习项目，不像最该 fork 的正式 PRD 菜单。
- 我仍想 push back：Opus R2 把主轴定义成“v0.1 是否以后训练为灵魂任务”，现在看还不够精确。经过搜索，**所有还值得保留的候选都该碰后训练**；真正分歧变成“预算放在单问题闭环深度，还是放在研究过程辅助宽度”。

## 2. Scope-reality searches

| Q | Finding | URL |
|---|---|---|
| 单人 LoRA 工具的 v0.1 通常包含什么？ | Axolotl 的 quickstart 直接围绕 LoRA/QLoRA 训练、测试、合并展开；同一配置文件贯穿训练、推理、合并。现实信号：核心是**训练闭环**，不是协作层。 | https://docs.axolotl.ai/docs/getting-started.html |
| 2026 本地后训练工具的用户期待是什么？ | Unsloth 明确主打“本地硬件训练/运行”、训练与推理一体、训练观测与较低显存占用。现实信号：v0.1 应该 **local-first + 可观测**，而不是平台化。 | https://unsloth.ai/docs |
| 轻量实验追踪的最小健康范围是什么？ | Trackio 主打 `wandb` 兼容、local-first、本地持久化、轻量 dashboard、LLM-friendly。现实信号：日志/报告层应该做成**轻、兼容、本地**，不该做重后台。 | https://huggingface.co/docs/trackio/en/index |
| Claude Code 平行会话本身是不是稀缺能力？ | Anthropic 官方已把 worktree 并行、隔离工作副本、并行会话写进教程；这说明“我会并行 worktree”本身已是底座能力。 | https://code.claude.com/docs/en/tutorials |
| 并行 agent 编排是不是已经被 OSS 占满？ | `agent-orchestrator` 已提供 worktree-per-agent、dashboard、CI 反馈回流、PR 流程；2026-04-24 搜索页显示约 6.5k stars。现实信号：再做一个“并行 orchestrator”很难差异化。 | https://github.com/ComposioHQ/agent-orchestrator |
| sidecar/辅助 agent 这类形态有现实依据吗？ | Anthropic 官方 subagents 文档明确把“隔离高输出 side task”“并行 research”作为常见模式。现实信号：sidecar 是合理 UX 形态，但更像**辅助手段**，不是主产品 thesis。 | https://code.claude.com/docs/en/sub-agents |

**核心现实结论**：训练/评测/日志是 table stakes；并行调度/看板已拥挤；相对空白的是“让 agent 帮 single-operator 把一个后训练问题推进到可复审结论”。

## 3. Refined candidates

### Candidate A · “Train-to-Decision”

**User / stories**：面向有本机训练条件、想认真回答一个后训练问题的 single-operator。用户定义一个问题与成功标准，系统完成 baseline、1-2 个 LoRA/SFT 变体、held-out 对比与最终决策记录。  
**IN**：单研究问题、最小后训练闭环、统一本地日志、失败归因、最终 markdown 报告。  
**OUT**：多 worker 编排、论坛、自动 judge 主裁、开放式文献综述、通用 prompt playground。  
**Success / time / UX / risk**：8-10 周；成功是用户能对一个问题做 keep/kill 决策，而不是“跑了很多实验”。UX 上先证据后结论，昂贵动作前必须显式确认。最大风险是硬件前提不成立。  
**Scope-reality verdict**：最健康。它顺着 Axolotl/Unsloth 的真实使用面走，同时把差异化放在“agent 驱动决策闭环”而非训练框架本身。  
**Best-fit profile**：human 真痛点就是 LoRA/SFT 判断，而不是想玩并行 agent。

### Candidate B · “Gate-Then-Train Ledger”

**User / stories**：面向更在意速度与成本的研究者。先围绕一个研究问题做便宜验证，再由 human 批准进入一次最小后训练，最后把 cheap probe 与训练结果写进同一研究账本。  
**IN**：单问题账本、cheap-first gate、一次后训练通道、统一报告、本地轻量追踪。  
**OUT**：宽平台、自动分叉多个方向、重 dashboard、复杂协作层。  
**Success / time / UX / risk**：9-11 周；成功是 2-3 天内拿到“该不该上训练”的证据，并在同一条目里保留后续结果。UX 核心是先便宜后昂贵。最大风险是范围滑向“什么都沾一点”。  
**Scope-reality verdict**：现实感最强的折中案。它吸收了 local-first tracking 的经验，也避免把全部预算押在训练之前。  
**Best-fit profile**：human 不确定后训练是否应当天天发生，但又不想把它完全后置。

### Candidate C · “Training Sidecar Pair”

**User / stories**：面向愿意为“不中断上下文”付额外范围的人。主线只做一个训练/eval 闭环；sidecar 只负责摘要、风险、候选下一步，不自行扩张任务。  
**IN**：1 条主线 + 1 个摘要 sidecar、统一报告、明确人审闸门。  
**OUT**：3+ workers、自动合并、多 issue 编排、把 sidecar 发展成真正 orchestrator。  
**Success / time / UX / risk**：10-12 周；成功不是更高吞吐，而是用户在长 run 后能无缝接回思路。UX 原则是“助手只建议，人类做决定”。最大风险是 sidecar 很容易变成编排表演。  
**Scope-reality verdict**：可做，但不是 moat。官方文档给了它形态合法性，却没有给它强烈市场空白。  
**Best-fit profile**：human 最在乎的是连续性、解释性和认知负担，而不是最短工期。

## 4. The single biggest tradeoff human must decide

我现在认为真正主轴不是 Opus 说的“是否以后训练为灵魂任务”，而是：

**把 10-12 周预算押在“单问题证据闭环深度”，还是押在“研究过程辅助宽度”。**

- A 把预算几乎全压到 baseline → 后训练 → eval → 决策，最深，但最吃硬件前提。
- B 接受后训练必须在场，但先用便宜证据 gate 它，深度稍降，决策效率更稳。
- C 再拿出一部分预算去买“理解过程更顺”的体验，而不是更多结论密度。

所以 human 真正在选的，不是“要不要并行”，也不是“要不要一点后训练”；而是 **v0.1 要不要优先做成一个能结束争论的研究闭环**。这一点是我和 Opus R2 的主要分歧。

## 5. What I'm less sure about now than I was in R1

- 我比 R1 更不相信“双 worker/协作感”足以单独撑起产品切法；它现在只配做 UX 变体。
- 我比 R1 更不相信纯 prompt/scaffold 宽面候选值得进正式菜单；搜索显示这类入口已经太拥挤。
- 我比 R1 更确定：若 v0.1 连最小后训练通道都没有，PARS 很容易退化成又一个 worktree wrapper。
