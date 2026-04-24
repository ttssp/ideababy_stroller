# Idea 003 · L3R1 · GPT-5.4 xhigh · Scope (no search)

**Timestamp**: 2026-04-24T05:37:59Z
**Inputs read**: `proposals/proposals.md`, `discussion/003/L2/stage-L2-explore-003.md`, `discussion/003/L3/moderator-notes.md`, `discussion/003/L3/L3R0-intake.md`, `.claude/skills/scope-protocol/SKILL.md`, `AGENTS.md`
**Searches used**: NONE in this round
**Visibility**: did NOT read other debater's L3R1

## 0. How I read the intake

human 要的不是 6 人平台的缩小版，而是一个 **单人、10-12 周内能用、成本低、且容纳一点后训练** 的研究工具。我的硬约束读法是：`single-operator / OSS / 不做多用户 / 不做 Docker / 不做复杂调度 / 不做 Runpod / 至少保留 LoRA/SFT 最小能力`。我会主动回答四个 ❓：主打哪类任务、纯串行还是保留最小互通、judge 放多深、后训练切口切多深。三个候选沿两条轴分化：**后训练做深还是研究回路做宽；以及要不要保留最小双 worker。**

## 1. Candidate A · “LoRA 闭环实验台”

### v0.1 in one paragraph
把 PARS 收成单人后训练实验台：围绕一个明确任务做 baseline、少量 LoRA/SFT 变体、统一评估和决策记录，回答“这类后训练值不值”。

### User persona
想认真试后训练但不想继续手拼脚本的个人研究者。

### Core user stories
- 作为研究者，我可以定义一个任务与成功标准，避免“先跑再说”。
- 我可以对同一任务连续跑 baseline 和少量后训练变体。
- 我可以在同一处比较指标、样例输出与本次结论。

### Scope IN
- L2 模块取舍：保留 M1/M5/M6/M8/M9；把 M4/M7 合并成实验记录簿；砍掉 M3、forum、dashboard。
- 后训练是 v0.1 的一等公民，默认单任务、默认串行。
- 每轮实验结束都有人类 keep/reject 关口。

### Scope OUT (explicit non-goals)
- 不做 prompt/agent 的完整产品面。
- 不做多 worker 协作、不做自动 judge、不做文献综述。
- 不做“无人值守跑很久再自动下结论”。

### Success looks like (observable outcomes)
- 一周内能跑完一个问题、若干变体，并形成明确取舍。
- 一个月后手头有可复用的后训练配方。

### Honest time estimate under human's constraint
- 约 7-9 周，信心中高。
- 最容易塞进 350-450h，但会主动放弃“广义研究系统”。

### UX principles
- 先能比较，再谈自动化。
- 高成本动作前必须让人看见后果。

### Biggest risk to this cut
若 human 的高频痛点不是后训练，这个切法会押注过早。

## 2. Candidate B · “单研究问题工作台”

### v0.1 in one paragraph
把 PARS 定义成 **单研究问题工作台**：human 先写 2-4 个研究种子，用便宜实验快速筛，再把一个方向升级成最小后训练尝试。它优先优化“更快得到下一步判断”。

### User persona
经常在“先试便宜方向，还是直接后训练”之间摇摆的个人研究者。

### Core user stories
- 我可以从一个研究问题出发，拆成几条可执行的小假设。
- 我可以先做便宜实验，再决定是否值得进入后训练。
- 我可以把不同尝试的结果放到同一研究条目里比较。

### Scope IN
- L2 模块取舍：保留 M1、轻量 M5/M6/M8/M9；把 M4/M7 合并为研究账本；保留一个最小后训练通道。
- prompt 优化、agent scaffold 是一等公民；LoRA/SFT 保留为升级路径。
- 默认全程人审，不把自动打分当主要裁决者。

### Scope OUT (explicit non-goals)
- 不做 3 类任务都做深。
- 不做 forum、leaderboard、复杂并发。
- 不做自我演化提示，也不做开放式文献综述。

### Success looks like (observable outcomes)
- 2-3 天内能从“一个问题”走到“继续/转向/停止”的证据化判断。
- 2 个月后积累的是可比较的研究案例。

### Honest time estimate under human's constraint
- 约 9-11 周，信心中等。
- 更像“研究系统”，但 breadth 更大，最容易吃掉预算余量。

### UX principles
- 先便宜后昂贵。
- 研究问题比运行数量更重要。

### Biggest risk to this cut
它最容易掉进“每样都有一点，但没有一样足够强”的陷阱。

## 3. Candidate C · “双 worker 研究搭档”

### v0.1 in one paragraph
保留 PARS 最小的一点“并行味道”：一个主研究流程，加一个轻量 sidecar worker 负责记要点、提候选动作、整理人审摘要；任何重训练始终只有一条主线。

### User persona
想保留一点 agent 协作感，但不愿背上额外复杂度的单人操作者。

### Core user stories
- 我可以在主流程推进时，让 sidecar 持续整理发现与待决问题。
- 我可以在长一点的运行过程中收到中间摘要，而不是盲等。
- 我可以在批准下一步前先看 sidecar 给的候选方案。

### Scope IN
- L2 模块取舍：保留瘦身版 M1/M2/M5/M6/M8/M9；只保留 M4 的“交接笔记”切片；砍掉 M3 完整调度、artifact 服务、dashboard。
- 最多一条重任务主线 + 一个轻量助手。
- 后训练与一个非训练任务类型同时支持，但都只做最小闭环。

### Scope OUT (explicit non-goals)
- 不做 3+ workers、不做领地划分、不做自动合并。
- 不做自动 judge 主裁决、不做 swarm 式文献综述。
- 不做把 sidecar 扩展成真正 orchestrator。

### Success looks like (observable outcomes)
- 1-2 小时的运行期间，human 不会丢掉上下文，能直接接上下一步。
- 研究日记与下一步候选能稳定沉淀。

### Honest time estimate under human's constraint
- 约 8-10 周，信心中等。
- 它看似折中，但隐含复杂度未必比 B 低。

### UX principles
- 并行只为减轻脑负担，不为追求规模。
- 助手只能建议，不能替 human 定夺。

### Biggest risk to this cut
最小双 worker 也可能偷偷把 L2 那套复杂性带回来。

## 4. Options for the human's ❓ items

- ❓v0.1 主打哪类任务
  - 选项 1：LoRA/SFT first，走 A。
  - 选项 2：研究问题 first，走 B。
  - 选项 3：双轨最小版，走 C。
- ❓执行形态是纯串行还是保留互通
  - 选项 1：纯串行，人是唯一协调者。
  - 选项 2：主线 + sidecar 笔记互通。
- ❓judge 放到什么程度
  - 选项 1：v0.1 完全人审。
  - 选项 2：judge 只做摘要或排序建议。
- ❓后训练最小切口有多深
  - 选项 1：只要“训练发起 + held-out eval + 结论记录”。
  - 选项 2：再加 run 对比与失败归因。

## 5. Red lines I'd propose

1. 不做自我演化提示/策略重写。对单人 v0.1 来说，收益远小于调试与失控成本。
2. 不做开放式 literature synthesis swarm。L2 的平台前提已被 intake 拆掉，这块最容易空耗预算。
3. 不做无人值守的长时高成本 run 自动采信结论。速度优先不等于允许“黑箱烧钱”。

## 6. Questions that need real user interviews (L3 can't answer)

- human 未来 6 周最常做的研究动作，到底是“先试很多便宜方向”还是“认真打磨一个后训练任务”？
- 在真实使用里，human 对“人审每一步”会觉得安心，还是会觉得打断流？
- 若只能保留一个惊喜时刻，human 更想看到“训练真的变好”，还是“研究决策明显变快”？
