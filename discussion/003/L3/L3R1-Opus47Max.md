# Idea 003 (PARS) · L3R1 · Opus 4.7 Max · Scope (no search)

**Timestamp**: 2026-04-24
**Inputs read**: L2 explore report、L3R0-intake、moderator-notes(预 L3 对抗审查发现)
**Searches used**: NONE
**Visibility**: did NOT read GPT 的 L3R1
**Word count target**: ~1300

---

## 0. How I read the intake

human 的 intake 把 L2 报告里那个"14 周 / 6 工程师 / 47 分高风险" 的 PARS 从根本上**重新定义**了:从一个**研究平台**变成一个**single-operator 的并行研究 cockpit**。

**我承认的硬约束**:2-3 个月、单人 30+ h/周、纯 OSS、不做多用户/Docker/调度/Runpod。这给我大约 **350-450 单人小时** 的预算。

**我必须 honor 的红线**:不做调度、不做容器、不做 Runpod、不做账号系统。

**人类的关键正向信号**:"会涉及一些后训练" — 这把候选 v0.1 拉回到比"纯 prompt 优化玩具"更有意义的位置。L2 报告里 LoRA / Qwen3-4B 那条线**没有被砍掉**。

**我会 propose 选项的 ❓ 项**:
1. v0.1 跑 1 类还是 N 类研究任务?
2. 多 worker 是否仍是核心卖点 vs 顺序串行?
3. LLM-as-judge 是否进 v0.1 vs 全人审?
4. "后训练"切口多大(LoRA only / SFT+LoRA / 含 RLHF)?

**我对优先级的解读**:human 选了"速度+成本+简单" 三项,**没选**安全。但 moderator-notes 里 P0-5(API key)和 P0-6(prompt injection→pip 供应链) 是 single-operator 也躲不开的 — 我会把"最小必需安全"塞进每个候选,不接受任何候选完全不防 key exfil。

---

## 1. Candidate A · "WorkBench" — 纯 prompt/scaffold 实验台,完全跳过后训练

### v0.1 in one paragraph
一个跑在你 macOS / Linux 本机的 CLI 工具,你输入"研究目标",它启动 **2-3 个并行 Claude Code worker**,每个拿一个不同的"含糊种子",在 git worktree 里独立工作几小时,把结果写进本地 NDJSON forum。任务面**只支持两类**:prompt 模板优化(在 HumanEval-N / MMLU-子集 上跑分) + agent scaffold 优化(在 SWE-bench Lite 5-10 题上跑分)。**完全不碰**模型权重。

### User persona
**你**(single-operator)。每周晚上想测试某个新 prompt 套路是否真的提升 X benchmark 时,不想手工开 3 个终端窗口跑 3 套对比;想让 3 个 Claude Code worker 用不同种子并发跑,自动汇总,3 小时后回来看哪条种子赢了。

### Core user stories
- 作为操作员,我能在 CLI 输入 `pars run "试试 chain-of-verification 在 HumanEval 上"`,系统自动派生 3 个 worker 用 3 条种子并发跑,几小时后给我 leaderboard。
- 作为操作员,我能 `pars status` 看每个 worker 当前在做什么、烧了多少 token / USD。
- 作为操作员,我能 `pars review <run>` 看 forum 时间线 + artifact diff,人手判定哪个 worker 的方法值得保留。
- 作为操作员,我能 `pars kill <worker>` 紧急停掉跑飞的 worker(比如发现它进死循环)。
- 作为操作员,run 完成后我能 `pars export` 拿到 markdown 报告(种子 + 关键发现 + 分数表)。

### Scope IN
- CLI(`pars init/run/status/review/kill/export`)
- 2-3 worker 并行(用 `claude -p` headless + 不同 worktree;**没有 Python scheduler**,直接 shell-level 后台进程 + 文件 lock)
- 一个 forum 文件(append-only NDJSON,worker 用 MCP 工具或简单 Bash 写入)
- 一个 artifact 目录(本地文件系统 CAS,sha256 命名)
- 2 个评测插件:HumanEval 子集 + SWE-bench Lite 子集(都是公开数据集,封装成 Python 可调用)
- 极简预算:USD 硬上限 + 全局 wall-clock(超时 SIGTERM)
- 最小安全:**API key 走环境变量,不进 worktree**;最小 deny 清单(`rm -rf` / `curl 外部` / `cat .env`)
- README 教别人怎么装

### Scope OUT
- 后训练 / LoRA / 任何模型权重操作 ← **这是与 B 候选的关键差异**
- Docker / 容器隔离 / 网络策略 / Runpod
- 多用户 / 账号 / 权限
- LLM-as-judge(v0.1 你人审)
- 子智能体(fact-checker 等 5 件套)
- forum 反应系统、tag 搜索、FTS
- Streamlit web UI(只做 CLI)
- 文献挖矿、Meta-review、CoT monitor、自动种子扩展
- 熵坍缩监控 / MAST 失败标注 UI
- Stage 1.5 / shadow owner / runtime policy

### Success looks like
- 跑完一次"prompt 优化 in HumanEval-30"任务全程 <2 小时、<$15、3 worker 都成功 produce 至少 1 个可比较 artifact
- 操作员能在 1 分钟内通过 `pars review` 看出哪个种子赢了
- 重启电脑,`pars resume <run>` 能续上未完成 worker(这是 single-operator 真实痛点)
- README 里贴 3 个真实 run 案例 + 1 张 leaderboard 截图,GitHub README 即"产品页"

### Honest time estimate
~6-8 周(40 h/周 × 7 周 ≈ 280 h)。**Confidence: H**。理由:剥掉了所有"团队/平台"层,核心实现在 Claude Code 原生 worktree + 简单文件协议;难点仅在评测插件正确性 + headless `claude -p` 解析 stream-json 的 bug。

### UX principles
- CLI 输出**短、可读**(不堆 token 数 / 进度条),允许你后台跑、回来再 `status`
- forum 默认 markdown,不引入私有 schema
- 所有错误"在终端 println,不藏 log file"

### Biggest risk
"完全不做后训练"和 human "会涉及后训练"的备注**直接矛盾**。如果你 v0.1 就想跑 LoRA 实验,候选 A 没法做 — 你得跳到候选 B。但如果你愿意把"后训练"留到 v0.2 一并做,候选 A 是 350h 内最稳的赌注。

---

## 2. Candidate B · "BenchKit" — 单工作流 LoRA 训练 + eval 闭环,只 1 个 worker

### v0.1 in one paragraph
一个跑在本机 + 本机 GPU(假设你有 RTX 3090/4090 之类一张消费级 24GB 显存以上)的 CLI 工具。**只跑一种工作流**:你给一个研究问题(如"Qwen3-4B 在 X 数据上 LoRA SFT 后是否在 held-out Y 上更好"),它自动:(1) 让 1 个 Claude Code worker 写训练脚本、(2) 跑 LoRA SFT、(3) 在外置 eval 容器/进程里测分、(4) 写 markdown 报告。**没有并行**——一切顺序、可重启、可审。

### User persona
**你**,但今天的角色是"想验证某个 SFT 配方对不对"的 LLM 从业者。你不需要 9 个 worker 抢 leaderboard,你只想让 LLM **代你写训练 loop + 跑 + 自己测**,你睡觉,早上看 markdown。

### Core user stories
- 作为操作员,我能 `pars sft start "训练 Qwen3-4B 让它能解 GSM8K-100" --data data/gsm.jsonl --eval gsm-held100`,worker 自动写脚本、跑、测、出报告。
- 作为操作员,worker 跑训练时 `pars status` 能看到当前 epoch / loss / GPU 使用率,而不是"无 tool_use 15min 就 SIGINT"误杀(state machine 区分 idle/training/downloading)。
- 作为操作员,我能 `pars sft retry --hypothesis "学习率太高"` 让 worker 在原 run 基础上改超参重跑,而不是从零再生成所有脚本。
- 作为操作员,完成后报告里**强制包含**:训练曲线、eval 分数、与 baseline 对比、worker 自己的"诚实失败原因"(若有)。
- 作为操作员,run 完所有 artifact(脚本、checkpoint 路径、log)有版本号,我能引用旧 run 做对比。

### Scope IN
- CLI(`pars sft start/status/retry/report`)
- 1 个 worker(无并行,无 forum,无 leaderboard)
- 1 个评测器(LM Eval Harness 或自包装的小脚本,约定输入输出 schema)
- LoRA / QLoRA 训练支持(用 unsloth / trl / peft 任意一个开源,不自研训练框架)
- Stuck 检测**带训练态白名单**:GPU util / 子进程 CPU / 磁盘 IO 任一活跃即 not stuck(L3 moderator-notes P1-10 的最小化版本)
- 简单 budget:USD 硬上限 + 训练 wall-clock 上限 + GPU hours 上限(本地)
- 最小安全:API key 走环境变量、`HF_TOKEN` 类似处理、deny 清单(`pip install` 仅允许从 `requirements-locked.txt`)
- 最小报告:训练曲线 PNG + 分数表 + 失败原因
- README + 1 个 working sample(`gsm8k-100-lora-qwen-4b`)

### Scope OUT
- 多 worker 并行 / forum / leaderboard ← 与 A 的关键差异
- prompt 优化 / agent scaffold 评测(那是另一种工作流)
- Docker / 容器化(只在 macOS Seatbelt 或 Linux ulimit + read-only mount 程度)
- 多种训练算法(只 LoRA SFT,不做 RLHF / DPO / RLOO 等)
- 多模型(v0.1 只测 Qwen3 + Llama 3.1 8B 这两个;扩到第三个 v0.2)
- Web UI / 自动种子扩展 / 文献挖矿 / LLM judge

### Success looks like
- `pars sft start` 一次端到端 <12h、<$30 API 费、产出可重现的 LoRA adapter + eval 报告
- README 给 1 个真实可复现的 baseline-vs-LoRA 提升 demo(哪怕只提 +3%)
- 重启电脑,`pars sft resume` 能续上中断训练(checkpoint 写盘到 worktree 外)
- 一份 GitHub README + 1 个长 issue 写"我用它做了什么 + 翻车了哪些事",作为传播

### Honest time estimate
~10-12 周(40 h/周 × 11 周 ≈ 440 h)。**Confidence: M**。理由:LoRA 训练框架**自己不写**(用 unsloth/trl),但 worker 写脚本 + 解释失败 + retry 机制是新东西;stuck 检测状态机要做对(P1-10);本地 GPU 显存 / 训练时长 / Apple Silicon 是否能跑(MPS 还是 CUDA?)需要先测。

### UX principles
- CLI 主流程**永远顺序**(start → 完成 → report),没有"哪个 worker 先完成"的并发认知负担
- 报告**不允许 LLM 美化**:loss 上升就明说,eval 退步就明说
- 任何"模型自己声称的提升"必须有 eval 数字 backing(借鉴 L2 §10 A1 失败模式缓解)

### Biggest risk
**本机硬件**是最大不确定性:Qwen3-4B 在消费级 24GB GPU 上 LoRA SFT 是 OK 的,但 8B+ 就紧张,4090 也只 24GB。如果你的本机没有合格 GPU,这个候选**整个不能做**(因为红线排除了 Runpod)。次要风险:LoRA stuck 检测状态机若做不对,15min 误杀会让你怀疑模型能力(P1-10 的真实成本)。

---

## 3. Candidate C · "Cockpit" — 中间路线,2-worker 并行 + 单工作流 prompt 优化 + 把后训练留作"第二版工作流插件"

### v0.1 in one paragraph
一个 CLI 工具,核心是 **2 worker 并行跑 prompt/scaffold 实验** 的简化版 A,但架构上预留一个**"工作流插件"接口**:v0.1 内置 1 个工作流(prompt 优化),但 LoRA SFT 工作流以**清晰文档 + 半成品 stub** 形式存在,你自己 v0.1.x / v0.2 时按文档实现并 plug-in。

### User persona
**你**,中长线操作员。今天的痛是"我想要并行 prompt 实验,但我也知道 3 个月后会想跑 LoRA"。你愿意 v0.1 暂时只用 prompt 工作流,但希望系统**长得像能扩**,而不是 v0.2 重写。

### Core user stories
- 作为操作员,`pars run --workflow prompt "..."` 启动 2 worker 并行 prompt 实验
- 作为操作员,我能看 `workflows/` 目录里有 `prompt-opt.py` 实现 + `lora-sft.py.stub`(只有空函数 + docstring 解释怎么填)
- 作为操作员,新工作流插件遵循一个**简单契约**:`def setup() / def run(seed) / def evaluate(artifact) / def report()`,我自己 200 行 Python 就能填出 LoRA stub
- 作为操作员,worker 报告统一 markdown schema,无论工作流是什么(便于跨 run 对比)

### Scope IN
- CLI(`pars run/status/review/kill`)
- 2 worker 并行(**仅 2,不是 3+**;减少 stuck 互相误判 + 显存竞争)
- forum:仅文件 NDJSON,无 FTS,无 react
- 工作流契约文档(`docs/workflow-contract.md`)
- 1 个完整工作流:prompt-opt(HumanEval-30 / MMLU-100)
- 1 个 stub 工作流:lora-sft(空函数 + 100 行 README 详细教怎么填)
- 评测层契约:`eval(artifact_path) → {score: float, details: dict}`
- 极简预算 + 最小 safety hooks
- README + 2 个真实 run 案例

### Scope OUT
- v0.1 不实现 LoRA 工作流(stub only)
- 3+ worker 并行(避免 P0-7 / P0-8 类问题不必正面解决)
- LLM-as-judge / 子智能体 / 自动种子扩展
- Docker / Runpod / 调度器
- Web UI

### Success looks like
- 1 个 prompt-opt run 端到端 <2h、<$20、2 worker 都成功 produce 可比较 artifact
- 你能在第 13 周(v0.1 完工后第 1 周)按 stub README 用 1 周时间填出可工作的 LoRA 工作流,**不需要改核心代码**
- README + workflow-contract.md 让 5 个其他人能在不读 core code 的前提下写新工作流

### Honest time estimate
~9-10 周(40 h/周 × 9.5 周 ≈ 380 h)。**Confidence: M-H**。比 A 多 2 周(因为要做"插件契约"+ stub 文档),比 B 少 2 周(因为不实际做 LoRA)。

### UX principles
- 核心循环和 A 一致:CLI 短输出,人手 review,无 web
- 工作流契约**可读优先**:200 行能讲清楚的事情绝不抽象成 500 行框架

### Biggest risk
"留架构口子" 是经典过度设计陷阱:你可能为了让 LoRA 能 plug-in 而把 prompt 工作流也做得太通用,结果 v0.1 都没爽快。**对治**:契约 ≤ 5 个函数;若任何契约函数签名 > 3 参数,降级回 A。次要风险:你 v0.1 完工后**不实际去填 LoRA stub**(典型 OSS 用户行为),那 stub 就是死代码 — 这意味着候选 C 只对"高确定性会回填"的人才划算。

---

## 4. Options for the human's ❓ items

| ❓ Item | Option 1 | Option 2 | Option 3 |
|---|---|---|---|
| **v0.1 跑哪类研究任务** | 仅 prompt/scaffold(A) | 仅 LoRA SFT(B) | prompt + LoRA stub(C) |
| **多 worker vs 串行** | 3 worker forum 风格(A) | 1 worker 顺序(B) | 2 worker 折中(C) |
| **LLM-as-judge** | 完全不做,人审到 v0.2 | 仅做最简易"双 worker 互审"轻量版 | 等到有 ≥30 个真实 artifact 后再决定 |
| **"后训练" 切口大小** | LoRA SFT only,1 算法 1 框架(B/C) | LoRA + DPO 二选一(B+) | 留 stub 不实现(C) / 完全跳过(A) |
| **本机硬件假设** | 假设无 GPU,纯 API(A/C) | 假设有消费级 24GB GPU(B/C 后期) | 在 README 标注"本工具假设你已有 GPU"+ MPS 兜底说明 |
| **种子来源** | 你手写 6-9 条 yaml(全候选默认) | LLM 元提示扩展(v0.2) | 文献挖矿(v0.3) |

---

## 5. Red lines I'd propose(intake 没明确点出但建议接受)

基于 L2 报告 + moderator-notes,你可能想加这些:

1. **不做"自我演化提示重写" / Meta-review**(L2 Stage 3 内容)——理由:OSS 个人项目,自动改 prompt 一旦坏了你会调试到怀疑人生
2. **不做向量库 / 语义检索**(Qdrant / Chroma)——理由:single-operator 几百条 forum 帖,grep 即可
3. **不做 BenchJack 红队 / 攻击仿真**(L2 Stage 3 + moderator P1-12)——理由:OSS 个人不是攻击目标,真有人攻击 fork 自审就够
4. **不做 Streamlit dashboard**(L2 §5.7)——理由:你是 CLI 用户,Streamlit 是给团队评审用的
5. **不做种子 LLM 自动扩展**(L2 §5.1 mode=llm_expanded)——理由:你 6-9 条手写更准,且 moderator P2-24 警告幻觉种子
6. **不做"跨 run 知识迁移"**(AgentRxiv 风格)——理由:每 run 独立、artifact 文件可读已经够,跨 run 是 v1.0 议题

**接受/拒绝**:看候选菜单时挑哪些写进 PRD 红线区。

---

## 6. Questions that need real user interviews(L3 答不了)

1. **本机硬件实际**:你目前用什么机器?有没有合格 GPU?MPS 跑 LoRA 你能接受吗?——这决定 B/C 的可行性,**强烈建议在 fork 前自己回答**。
2. **"v0.2 实际会不会做 LoRA"**:候选 C 的全部价值靠这个回答。如果你 70%+ 概率会做 → C 划算;<40% → 选 A。
3. **OSS 分发期望**:你对 GitHub star 数、issue 流量、用户使用 friction 的容忍度?——决定 README/onboarding 投入比例。
4. **失败的可承受范围**:v0.1 跑完发现 LoRA 没真提升 baseline,你会(a)接受当作"诚实负面 demo"还是(b)觉得 v0.1 不该 ship?——决定候选 B 的 success 标准。

---

## 关键 tradeoff 轴(给 menu reader)

**"v0.1 是否包含后训练" 是这 3 个候选的核心分歧轴**。
- A:不含(纯 prompt/scaffold,最快最稳)
- B:全押(只做 LoRA,最贴 human "会涉及后训练" 备注)
- C:留口子(prompt 工作流 + LoRA stub,赌 v0.2 会回填)

human "会涉及后训练" 这句话**强烈倾向 B 或 C**;但 350-450h 预算、"速度+成本+简单"三优先 **强烈倾向 A**。这就是你看 menu 时要挑的那一刀。
