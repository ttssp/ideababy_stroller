# Idea 003 (PARS) · L3R2 · Opus 4.7 Max

**Timestamp**: 2026-04-24
**Opponent's L3R1 read**: ✅ yes (`L3R1-GPT54xHigh.md`)
**Searches run**: 6, scope-reality category only
**Word count target**: ~900

---

## 1. From opponent's candidates — what sharpened my thinking

GPT 的 R1 让我**承认我 R1 的 A 候选有押注问题**:

- **GPT 的 A "LoRA 闭环实验台" 直接把后训练放 first-class**——我之前的 A "WorkBench" 把后训练完全砍掉,结果与 human 备注"会涉及一些后训练"**字面冲突**。即使 human 接受 v0.1 不做后训练,候选 A 至少应"明示后训练在 v0.2 自然衔接"。我承认 GPT 的押注更勇敢,也更对称地处理了 intake。
- **GPT 多识别一条 tradeoff 轴**:"是否值得为协作感引入双 worker"——这是我 R1 漏掉的。我之前默认"2-3 worker 是 PARS 的灵魂",但搜索数据(见 §2)显示 worktree+并行已是过度饱和的开源主题,2-worker"sidecar"反而比"3-worker forum 风格"更稀缺也更有产品感。
- **GPT 的 C "sidecar 笔记助手" 比我的 C "插件契约扩展性" 更具体**——我的 C 是架构姿态("留口子"),GPT 的 C 是用户体验("减脑负担")。后者更易交付、更易演示、风险更可控。**我会回收 GPT 的 sidecar 概念**,但不会回退我的"统一工作流契约"——两者可以并存。
- **GPT 在产品层面消化 P0**(不无人值守烧钱、不给 forum 正当性、不给复杂并发正当性)——比我列具体 P0/P1 编号更克制、更"产品语言"。但 single-operator 也有真实的 API key exfil 与 LoRA stuck 误杀风险,这些**仍需在候选里点到**。

要 push back 的:
- **GPT 的 A 候选低估了"只做 LoRA 闭环"的窄度风险**——若 baseline 跑出来发现 LoRA 没用,你的 v0.1 的全部演示价值瞬间归零。我会保留"baseline 比较 + 失败归因 + 决策记录"作为产品价值,而不是"LoRA 比 baseline 高分"。
- **GPT 的 B "便宜实验先 → LoRA 升级路径" 实质是我 R1 的 C "Cockpit" 的另一种表述**——只是 GPT 用"研究问题 first"框架,我用"插件契约"框架。两者底层都是"先做便宜的,LoRA 留 hook"。L3R2 应合并这两支。

---

## 2. Scope-reality searches

跑了 6 个 scope-reality 搜索,核心数据点:

| Q | Finding | URL |
|---|---|---|
| 单人 LoRA OSS 工具 v0.1 典型功能 | 2026 单 RTX 4070 Ti 8-12GB VRAM 跑 7B QLoRA;Axolotl 走 YAML 配置,Unsloth 极致优化内存,LM Eval Harness 必备评估 | [DEV 2026 Guide](https://dev.to/jangwook_kim_e31e7291ad98/fine-tune-llms-with-lora-and-qlora-2026-guide-33lf) |
| 并行 Claude Code worktree 工具生态 | **饱和**——`parallel-code`、`agent-orchestrator`(6.4k stars)、`parallel-cc`、`parallel-worktrees`、`nano-claude-code` 已存在 | [agent-orchestrator](https://github.com/ComposioHQ/agent-orchestrator) |
| Axolotl/Unsloth 配置粒度 | 都是 YAML 单文件;Unsloth Feb 2026 加 12× MoE 训练 + 嵌入模型 + ultra-long context RL | [Spheron Comparison](https://www.spheron.network/blog/axolotl-vs-unsloth-vs-torchtune/) |
| 轻量实验追踪 | Trackio (HF, **local-first, W&B 兼容**) 是 2026 新势力;Neptune 即将关停 | [Trackio](https://www.towardsdeeplearning.com/trackio-vs-w-b-vs-mlflow-hugging-faces-lightweight-experiment-83f2f783e444) |
| solo OSS lessons | "validation, not code, determines early demand";"speed > perfection" 普遍共识;1 月 prototype OK | [Indie Hackers](https://www.indiehackers.com/post/i-shipped-a-productivity-saas-in-30-days-as-a-solo-dev-heres-what-ai-actually-changed-and-what-it-didn-t-15c8876106) |
| Claude Code headless 模式可用性 | `claude --headless` 已 production-ready;trap handler 处理 worktree 清理是 documented pattern | [DEV worktree pattern](https://dev.to/edwardkubiak/git-worktrees-headless-ai-sessions-a-pattern-for-parallel-code-generation-2i5) |

**关键 reality check**:
- **生态饱和**侧:任何"PARS = N worker + worktree + forum" 的 v0.1 在 2026 年都**很难差异化**。已有 6.4k-star 项目专做这事。
- **生态空白**侧:**"Claude Code worker 自动写训练脚本 + 跑 LoRA + 自我归因失败 + 出报告"** 这条工作流没有现成 OSS;Axolotl/Unsloth 只是**训练框架**,没有"Claude 主动控制 + 失败自省"的 agent 层。
- **Trackio 启示**:local-first + 兼容流行接口 = 2026 单人工具的成功公式。PARS v0.1 应该天然 local-first。

---

## 3. Refined candidates

合并 Opus R1 与 GPT R1 各 6 候选 → **3 refined peer 候选**:

### Refined A · "RecallKit" — single LoRA 决策循环 (吸收 GPT-A + 我的 B)

**v0.1 essence**: 单人 + 本机 GPU(假设有 24GB 消费卡)+ 1 worker 顺序工作流 + 后训练 first-class。流程:你给一个研究问题(如"Qwen3-4B 在 GSM8K 子集 LoRA SFT 是否超越 baseline?"),Claude Code worker 自动: ① 写 baseline 脚本跑分;② 写 LoRA SFT 脚本跑训练;③ 在外置 eval 进程跑 held-out 测分;④ 出 markdown 决策报告(含曲线 + 分数对比 + worker 自己的失败归因)。

**Persona**: 你今天扮演"想用 LoRA 验证一个具体假设"的 ML 从业者。

**Stories** (从 GPT-A + 我的 B 合并):
- 我能定义 1 个研究问题 + 1 个成功标准
- worker 自动写脚本、跑、测,我睡觉,早上看 markdown
- worker 自我归因失败(loss 不下降?数据不对?LR 太大?),不让我自己读 log
- 我能 retry --hypothesis "学习率太高",worker 改超参重跑
- 所有 artifact 版本化,可引用旧 run 做对比

**Scope IN**: CLI(`pars sft start/status/retry/report`)、1 worker 顺序、Axolotl 或 Unsloth 任选其一作训练后端、LM Eval Harness 作评测后端、stuck 检测带训练态白名单(P1-10)、API key 走 env、最小 deny 清单、markdown 决策报告强制含失败归因。

**Scope OUT**: 多 worker、forum、并发、prompt-opt 工作流、Docker、自己造训练框架、LLM judge、自动种子扩展。

**Success**: 一周内能跑完 1 个 baseline + 1 个 LoRA 变体 + 决策记录;markdown 报告里有曲线 + 分数 + 失败归因。

**Time**: ~10 周 / 380-420h。**Confidence: M**(同 GPT 与我先前判断,本机 GPU 是主要不确定性)。

**Scope-reality verdict**: **这是生态空白点**——Axolotl/Unsloth 只管"训练",没人做"agent 自动 control 训练 + 自省"。差异化合理。

**Best fit if**: human 真的会经常跑 LoRA 实验,且本机有 24GB+ GPU。

---

### Refined B · "Researcher's Cockpit" — sidecar 助手 + prompt 优化 + LoRA 留作 v0.2 (吸收 GPT-C + GPT-B + 我的 C)

**v0.1 essence**: 单人 + 1 主线 worker + 1 轻量 sidecar worker。主线跑 prompt/scaffold 实验;sidecar **不跑实验**,只持续整理"主线发现 + 待决问题 + 候选下一步动作",每隔 30 分钟生成"中间摘要" 给 human。LoRA 工作流以**完整 stub + 100 行 README** 形式存在,human v0.2 自己填。

**Persona**: 你今天扮演"想要 agent 协作减脑负担,但不想多 worker 抢算力"的研究者。

**Stories**:
- 主线 worker 推进 prompt 实验,sidecar worker 持续整理摘要
- 长 run 中我能拿"中间摘要" 决定要不要继续,而不是盲等 2 小时
- sidecar 给候选下一步动作,我审批或拒绝,不让它替我决定
- workflow 是契约化的(`setup/run/evaluate/report` 四函数),v0.2 我能 200 行 Python 加 LoRA stub
- 工作流 + 报告 schema 跨 workflow 统一

**Scope IN**: CLI、1 主线 + 1 sidecar(共 2 worker,严格不超)、prompt-opt workflow 完整实现、lora-sft workflow stub + README、4 函数工作流契约、append-only NDJSON forum、最小 budget hardcap、最小 safety hooks。

**Scope OUT**: 3+ worker、forum FTS/react、自动 judge 主裁、Docker、Runpod、文献综述。

**Success**: 一次 prompt-opt run <2h <$20;sidecar 摘要被 human 评价"有用"≥80%;v0.2 我能在 1 周内填出 LoRA stub。

**Time**: ~9 周 / 340-380h。**Confidence: M-H**。

**Scope-reality verdict**: **轻度差异化**——worktree+并行已饱和,但 "sidecar 摘要" 是少见模式。risk:可能像 [agent-orchestrator](https://github.com/ComposioHQ/agent-orchestrator) 这类已有项目吃掉空间。

**Best fit if**: human 70%+ 概率 v0.2 会回填 LoRA;且看重"减脑负担" 多于"训练验证"。

---

### Refined C · "DemoBench" — 极致瘦身 prompt-opt 单工作流 + 完全不留 LoRA 口子(吸收我的 A + GPT-B 的"先便宜")

**v0.1 essence**: 单人 + 1 worker + **只跑 prompt 优化**(HumanEval 子集 + MMLU 子集)+ 完全不留 LoRA 口子。最快上线、最简单维护、最便宜。完成后 v0.2 直接重写架构去做 LoRA — 不假装 v0.1 能扩展。

**Persona**: 你今天扮演"想最快做出能 demo 的 OSS 工具"的人。

**Stories**:
- `pars run "试 chain-of-verification"` 立即派 1 worker 跑 prompt 实验
- 全程 <1h <$5
- README 含 3 个真实案例 + leaderboard 截图
- 不假装能做后训练 — README 写明"v0.1 only handles prompt; for fine-tuning use Axolotl directly"

**Scope IN**: CLI、1 worker 顺序、HumanEval-30 + MMLU-100 评测插件、API key env、报告 markdown。

**Scope OUT**: **后训练完全 OUT**、多 worker、sidecar、forum、workflow 契约、所有"扩展性"代码。

**Success**: 6 周内 ship;README + 3 真实 run + 5+ GitHub star 即"成功"。

**Time**: ~6 周 / 220-260h。**Confidence: H**。

**Scope-reality verdict**: **饱和市场**——"用 Claude Code 跑 prompt 实验"的 OSS 工具已多。candidate C 的 GitHub 命运可能是"5 star 然后被遗忘"。但**如果 human 真实 first goal 是"用 PARS 学 Claude Code agent 模式"而非"造受欢迎工具"**,C 是最稳的学习载体。

**Best fit if**: human 视 PARS 为**学习项目**而非**长寿 OSS 项目**;且对"会涉及后训练" 的备注是"未来想做 != 现在 v0.1 必须做"。

---

## 4. The single biggest tradeoff human must decide

**轴名**:**v0.1 的"灵魂任务"是后训练验证 还是 prompt/scaffold 实验**。

GPT R1 已识别这条轴(其 §0)。L3R2 后,这条轴变得**更加锐利**:

- 选 **A (RecallKit)**:押注"后训练就是 v0.1 的灵魂"。**需要本机 24GB+ GPU**(否则整个候选不可行)。生态空白,差异化合理。380-420h。
- 选 **B (Cockpit)**:押注"协作感 + 留 LoRA 口子"。无 GPU 也能 v0.1。340-380h。**风险**:LoRA stub 可能成为死代码;sidecar 也可能复杂度爆炸。
- 选 **C (DemoBench)**:押注"先 ship 一个能跑的玩意",承认 v0.1 不解决后训练。220-260h。**生态饱和**,差异化弱。

**推荐**(若 human 不知道选哪个):
- 若你有 24GB+ GPU + 想认真做后训练 → **A**
- 若你没合格 GPU 或不确定 LoRA 是真痛点 → **B**
- 若你只想 6 周内 ship 一个能演示的东西 → **C**

**第二轴**(GPT 识别):**单 worker 顺序 vs 双 worker sidecar**。这条轴**只在 B 候选里活跃**(A 必单 worker、C 必单 worker)。如果选 B,sidecar 复杂度风险是次要决策点。

---

## 5. What I'm less sure about now than I was in R1

诚实更新:

1. **"工作流插件契约"在 R1 我是 C 的卖点**。R2 后我承认:对 single-operator 而言,**契约化反而是过度设计**。GPT 的 sidecar 概念更具体、更易交付。我把"契约"降级为 B 候选的次要 IN 项,不再当卖点。

2. **"单 worker LoRA 闭环 = 候选 B"在我的 R1 里**。R2 后承认:这其实更像 GPT 的 A,我应称为"窄但深"(单任务后训练)而非"我的 B"。我已在 Refined A 里采用 GPT 的命名直觉。

3. **"3 worker forum 风格"在我 R1 的 A 候选里**。R2 后:**完全砍掉**。生态饱和数据(`agent-orchestrator` 6.4k stars 等)显示 3-worker forum 已被吃掉。Refined 三候选都 ≤2 worker。

4. **moderator-notes 的 24 P0/P1 在 v0.1 单人下到底相关多少**——我在 R1 列了具体 P 编号(感觉太"工程师"),GPT 全用产品语言转译。R2 后我承认 GPT 的克制更对——P0/P1 应在 L4 spec 阶段重新动员,L3 只需说"API key env-only + stuck 状态机"就够了。

5. **本机硬件这个 ❓ 我在 R1 里轻轻带过**——R2 数据让它**主导级别**:24GB 消费卡在 2026 跑 7B QLoRA 是合理假设但**不能默认**。Refined A 的 success 完全 hinge on 这个;若 human 没合格 GPU,Refined A 就该淘汰。
