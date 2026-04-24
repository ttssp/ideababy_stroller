# L3 Scope Menu · 003 · "PARS — 单人后训练 / 研究决策实验台"

**Generated**: 2026-04-24
**Source**: L2 explore (PARS 14 周方案) + L3R0 intake + 2 轮 L3 辩论(Opus 4.7 + GPT-5.4 xhigh)
**Rounds completed**: L3R1 (双方各 3 候选,无搜索) + L3R2 (双方各 3 refined 候选 + 共 10 次 scope-reality 搜索)
**Searches run**: 10 次 scope-reality(Opus 6 + GPT 4)
**Moderator injections honored**: 24 项 P0/P1/P2 对抗审查发现作为预 L3 上下文,本菜单按"产品语言"消化,不再列具体 P 编号

---

## 如何阅读本菜单

这是 L3 的输出:**003 (PARS) 的候选 PRD 菜单**。每个候选都是**对等的同辈**——是同一个 idea 在你已声明的硬约束(2-3 个月 / 单人 / OSS / 不调度 / 不 Docker / 至少最小后训练)下的不同合法切法。你将分叉(fork)一个或多个候选进入 L4(spec + build):

    /fork 003 from-L3 candidate-X as 003-<prd-id>

分叉完成后,运行 `/plan-start 003-<prd-id>` 启动 L4(spec + build)。

---

## 入参摘要 — 我们 honor 了什么

### 硬约束(✅) — 所有候选必须满足
1. **时间**:2-3 个月交付 v0.1(对齐 ~10-12 周)
2. **投入**:1 人 × 30+ h/周 → 单人总预算 ~350-450 h
3. **用户**:single-operator(你自己)
4. **商业**:OSS 免费,GitHub README 即"分发渠道"
5. **优先级**(三选三):上线速度 + 运行成本低 + 技术简单
6. **必须支持**:某种形式的后训练(至少 LoRA/SFT 单 GPU 单任务) — 关键正向信号

### 软偏好(🤔) — 倾向但可调
- 平台:CLI 优先,本地极简 web 可有可无
- worker 数:1 / 2 / 3 都能接受(双方 R2 已收敛到 ≤2 worker)
- 评测:本地优先,LM Eval Harness / 自包装均可

### 红线 — 任何候选都未越线
1. 🚫 不做多用户 / 账号 / 权限
2. 🚫 不做 Docker / 容器隔离(macOS Seatbelt + worktree 上限)
3. 🚫 不做"复杂调度"(asyncio scheduler / GPU 分配 / 信号量)
4. 🚫 不做 Runpod / 云 GPU(本机为限)

### ❓ 由本菜单解决(每候选如何选择)

| ❓ 项 | 候选 A 决议 | 候选 B 决议 |
|---|---|---|
| v0.1 是否包含后训练? | ✅ 一等公民,首屏即 LoRA SFT | ⚠️ 升级路径(便宜实验先,LoRA 作为升级步) |
| v0.1 跑哪类研究任务? | 单一类:后训练决策循环 | 两类:prompt/scaffold 实验 + LoRA 升级路径 |
| 多 worker vs 串行? | 1 worker 严格顺序 | 1 主线 worker + 0 sidecar(默认),最多 2 worker |
| LLM-as-judge 是否进 v0.1? | ❌ 完全人审 + 客观 metric | ❌ 完全人审 + 客观 metric |
| 是否做 forum / leaderboard? | ❌ 仅 run ledger + compare | ❌ 仅 run ledger + compare |
| 是否做 workflow 契约 / 插件 | ❌ 当下不做(过度设计) | ⚠️ 仅在第二个工作流真要进来时引入 |
| 工作流账本(ledger/compare) | ✅ 必备 — 每次 run 落地账本 | ✅ 必备 — 每次 run 落地账本 |

> **注**:"prompt-only / 完全跳过后训练" 候选(Opus R2 的 DemoBench)与 GPT R2 的"主线+sidecar 摘要搭档"候选**未进入主菜单**——理由见下方"被淘汰候选"小节。

### ❓ 仍对人类开放的关键问题(菜单解决不了)

1. **本机硬件假设**(决定性 ❓):候选 A 假设你有**一张 24GB+ 显存的消费级 GPU**(如 RTX 4090 / 3090 / Mac Studio M2 Ultra)。**若你没有合格 GPU,候选 A 整个不可行**(因为红线排除了 Runpod)。这一项 L3 无法替你决定,**强烈建议在 fork 前先回答**。
2. **"后训练"是不是你未来 6-12 周的真实高频痛点?** 候选 A 全押后训练;若你的真实痛点是"prompt/scaffold 实验"或"研究判断速度",候选 B 更合适。
3. **OSS 分发期望**:你对 GitHub star 数 / issue 流量 / 用户使用 friction 的容忍度?决定 README/onboarding 投入比例。

---

## 关键 tradeoff 轴

> **v0.1 的"灵魂任务"是后训练验证,还是研究判断流程?**

两条候选沿这一刀分化:

- **候选 A(后训练决策循环)**:押注"后训练就是 v0.1 的灵魂"。最窄、最深、生态空白,差异化最强,但**完全 hinge on 本机有合格 GPU**。
- **候选 B(研究问题账本)**:押注"研究判断速度比训练能力更核心"。先做便宜实验(prompt / scaffold),后训练作为升级步存在但不强制;**无 GPU 也能跑 v0.1 大部分功能**。

GPT R2 把这条轴说得最尖:"选 A 是后训练就是产品灵魂;选 B 是后训练是重要能力,但只是研究判断流程中的升级步骤。" 双方 R2 已经收敛在这条主轴上。

**次轴**(已退居第二位):是否引入轻量 sidecar agent 减脑负担。两轮辩论后双方都承认 — orchestration 层已饱和(`agent-orchestrator` 6.4k stars 等),sidecar 价值不够硬,因此**两个主菜单候选都默认 1 worker**;sidecar 仅作为候选 B 的 v0.2 选项。

---

## 候选 PRD

### 候选 A · "RecallKit" — 单人后训练决策循环

**建议 fork id**:`003-pA`
**来源**:Opus R2 Refined A + GPT R2 Refined A(双方独立收敛到几乎相同的形态)

#### v0.1 一段话

围绕**一个明确研究问题**(如 "Qwen3-4B 在 GSM8K 子集上 LoRA SFT 后是否在 held-out 集上更好"),系统在你本机自动:① 让 1 个 Claude Code worker 写 baseline 脚本并跑分;② 写 LoRA SFT 脚本并跑训练;③ 在外置 eval 进程跑 held-out 测分;④ 出 markdown 决策报告(含训练曲线 + 分数对比 + worker 自己的失败归因)。**完全顺序、可重启、可审**。回答的不是"能自动化多少事",而是"**这次后训练值不值得继续投时间**"。

#### User persona(具体)

**你**——今天扮演"想用 LoRA 验证一个具体假设"的 ML 从业者。你不需要 9 个 worker 抢 leaderboard,你只想让 LLM 代你写训练 loop + 跑 + 自测,睡一觉早上看 markdown,**给出"继续/停止/改方向"的证据化判断**。

#### Core user stories(3-5 条)

- 作为研究者,我能用一行 CLI 定义研究问题 + 成功标准 + baseline,不用先写一堆 yaml。
- 作为研究者,我能让 worker 自动跑 baseline → LoRA → eval 全流程,过夜后看 markdown 决策报告。
- 作为研究者,worker 必须**自我归因失败**(loss 不下降?数据格式不对?LR 太大?),不让我自己读 log。
- 作为研究者,我能 `pars retry --hypothesis "学习率太高"`,worker 改超参在原 run 基础上重跑(不重新生成所有脚本)。
- 作为研究者,所有 artifact 落入**本地 run ledger**,我能 `pars compare runA runB` 跨 run 对比指标 / 配置 / 结论。

#### Scope IN(v0.1)

- CLI(`pars sft start / status / retry / report / compare`)
- 1 worker 严格顺序(无并行,无 forum,无 leaderboard)
- Axolotl 或 Unsloth 任选其一作训练后端(不自研训练框架)
- LM Eval Harness 或自包装小脚本作评测后端(eval 进程外置,与 worker 进程分离)
- **Stuck 检测带训练态白名单**:GPU util / 子进程 CPU / 磁盘 IO 任一活跃即 not stuck(避免训练中误杀)
- 简单 budget:USD 硬上限 + 训练 wall-clock 上限 + GPU hours 本地上限
- **本地 run ledger + compare**:每个 run 落 `runs/<id>/{config,metrics,artifacts,report.md}`,可跨 run 比较参数 / 指标 / 结论
- 最小 safety:API key 走环境变量、`HF_TOKEN` 同样、`pip install` 仅允许从锁定 requirements 文件
- markdown 决策报告**强制含失败归因**(loss 上升明说,eval 退步明说,不允许 LLM 美化)
- README + 1 个真实可复现 demo(`gsm8k-100-lora-qwen3-4b`)

#### Scope OUT(明确不做)

- 多 worker 并行 / forum / leaderboard / sidecar — 因为 1 worker 顺序已能解决"决策"问题
- prompt 优化 / agent scaffold 工作流 — 因为那是另一种用户流程,与"后训练决策"不在一个剧本里
- Docker / Runpod / 云 GPU — 红线
- 多种训练算法 — 仅 LoRA SFT,不做 RLHF / DPO / RLOO(留 v0.2)
- 多模型支持 — v0.1 只测 Qwen3-4B + Llama 3.1 8B 两个;扩到第三个 v0.2
- Web UI / 自动种子扩展 / 文献挖矿 / LLM-as-judge / workflow 插件契约
- 自我演化提示重写 / Meta-review / 向量库 / 红队仿真

#### Success looks like(可观测产出)

- 一周内能跑完 1 个 baseline + 1-2 个 LoRA 变体 + 决策记录
- markdown 报告里**必有**训练曲线 PNG + 分数对比表 + 失败归因文字
- 重启电脑后 `pars sft resume` 能续上中断训练(checkpoint 写盘到 worktree 外)
- README 给 1 个真实可复现 demo,即使是"诚实负面 demo"(LoRA 没真提升 baseline)也算 ship 成功
- 端到端单 run <12h、<$30 API 费

#### Time estimate under 你的约束

- 给定 intake(35 h/周 × ~10-11 周): **~10 周 / 380-420 h**
- Confidence:**M**
- 不确定原因:本机 GPU 实测能力(MPS 还是 CUDA?显存够不够 7B QLoRA?)+ stuck 状态机要做对(P1-10 级别真实成本)+ Axolotl/Unsloth 选哪个的踩坑成本

#### UX 优先级(取舍立场)

- CLI 主流程**永远顺序**(start → 完成 → report),没有"哪个 worker 先完成"的并发认知负担
- 报告**不允许 LLM 美化**:loss 上升明说,eval 退步明说,"模型自己声称的提升"必须有 eval 数字 backing
- 短输出 > 进度条堆 token,允许后台跑 + 回来 `status`

#### Biggest risk(产品级)

**本机硬件就是 go/no-go 决定**——若你没有 24GB+ 显存的合格 GPU,这个候选**整个不能做**,因为红线排除了 Runpod。其次:若 baseline 跑出来发现 LoRA 没真提升,你的 v0.1 演示价值弱化(但可作为"诚实负面 demo");再次:LoRA stuck 检测状态机若做不对,15min 误杀会让你怀疑模型能力,debug 几天才发现是检测 bug。

#### Scope-reality verdict

- **同类产品通常包含**(从 Unsloth / Axolotl GitHub 首页):快速开始、训练、示例 / 导出 — 都把"一次训练闭环跑通"放首屏(GPT R2 搜索)
- **本候选切掉**:协作层、并行 worker、forum、自动 judge — 与上述同类共识吻合
- **本候选独有**:agent 自动控制训练 + 自我归因失败 + 决策记录 — Axolotl/Unsloth 仅是训练框架,**没有 agent 控制层**(Opus R2 搜索:这是生态空白点)
- **2026 启示**:Trackio (HF) local-first + 兼容流行接口 = 单人工具的成功公式;run ledger 与 MLflow / W&B 的"runs / compare / artifacts" 最低共识对齐
- **净读**:**生态空白处的合理 MVP** — 差异化最强,但窄
- **代表性同类**:Axolotl(<https://github.com/axolotl-ai-cloud/axolotl>)、Unsloth(<https://github.com/unslothai/unsloth>)、Trackio(<https://huggingface.co/blog/trackio>)

#### Best fit for 一类人

你**已经有**一张 24GB+ 显存的消费级 GPU,**已经知道**自己接下来 6-12 周高频要做的事就是 LoRA / SFT 验证(而不是 prompt 实验或一般研究探索),**愿意接受** v0.1 围着"后训练决策"这一件事变窄。如果以上三个条件不全部成立,看候选 B。

---

### 候选 B · "BenchLedger" — 研究问题账本(便宜实验先 + 后训练升级路径)

**建议 fork id**:`003-pB`
**来源**:Opus R2 Refined B(Cockpit,去掉 sidecar)+ GPT R2 Refined B(研究问题账本)

#### v0.1 一段话

把 PARS 定义为**单研究问题工作台**。你先把一个研究问题(如"chain-of-verification 在 HumanEval 上是否提升?")拆成几次可比较的尝试;系统让 1 个 Claude Code worker 顺序跑这些**便宜实验**(prompt 优化 + agent scaffold),用本地 run ledger 记录所有结果;**当且仅当**便宜实验明确指向"值得后训练验证"时,你触发 `pars sft upgrade`,worker 进入 LoRA SFT 升级路径(与候选 A 的核心闭环相同,但作为 ledger 中的一条特殊 run)。核心承诺:**更快得到 go / no-go 判断**,而不是把任务面铺开。

#### User persona(具体)

**你**——今天扮演"经常在'先试便宜方向'和'直接做后训练'之间摇摆"的单人研究者。你的真实痛点是 "我有 5 个想法,不知道哪个值得花 12 小时跑 LoRA",你希望 v0.1 帮你**先用便宜实验筛掉 4 个**,再把剩下的 1 个升级到后训练。

#### Core user stories(3-5 条)

- 作为研究者,我能从一个模糊研究问题出发,在 CLI 写 2-4 条可执行假设,worker 顺序跑出可比较结果。
- 作为研究者,我能在同一研究账本里看每次尝试的 config / metric / 结论,**包括跨 workflow**(prompt vs LoRA)的对比维度。
- 作为研究者,我能在便宜实验出明确信号后,用 `pars sft upgrade --from <run-id>` 把同一个研究问题升级到 LoRA 验证。
- 作为研究者,worker 跑训练时 `pars status` 能看到 epoch / loss / GPU 利用率,而不是误杀 + 重启风暴。
- 作为研究者,2-3 天内能从"我想试这个"走到"值得继续 / 不值得 / 改方向"的证据化判断。

#### Scope IN(v0.1)

- CLI(`pars run / status / review / compare / sft upgrade`)
- 1 worker 顺序(可在 v0.2 增加 sidecar 摘要搭档,**v0.1 不上**)
- 两类工作流:① prompt-opt(HumanEval-30 / MMLU-100 子集);② LoRA SFT 升级路径(与候选 A 同款,但作为升级步触发)
- **本地 run ledger + compare**:每 run 落 `runs/<id>/{workflow, config, metrics, artifacts, report.md}`,跨 workflow 跨 run 可比较
- Stuck 检测带训练态白名单(同候选 A)
- 简单 budget:USD 硬上限 + 训练 wall-clock 上限
- 最小 safety:API key env、deny 清单、`pip install` 仅从 locked requirements
- markdown 决策报告强制含**横向对比段**(本次 vs 历史 baseline)+ 失败归因
- README + 2 个真实可复现 demo(1 个 prompt-opt、1 个升级到 LoRA)

#### Scope OUT(明确不做)

- 多 worker 并行 / forum / leaderboard / sidecar(v0.1 不上 sidecar,见 §"被淘汰候选")
- workflow 插件契约 / "扩展性"代码 — 第二个工作流(LoRA)用复制 + 改的方式实现,不抽象
- Docker / Runpod / 云 GPU / 复杂调度
- LLM-as-judge / 自动种子扩展 / 文献挖矿 / 自我演化提示
- 3+ 类任务面("agent scaffold 评测"留 v0.2)
- 多研究问题并发(v0.1 一次只跟一个研究问题走)

#### Success looks like(可观测产出)

- 2-3 天内能从"我想试这个"走到"go / no-go" 证据化判断
- run ledger 里至少能展示 1 个完整故事:5 条便宜实验 → 1 条 LoRA 升级 → 决策记录
- 重启电脑能 resume 中断的便宜实验或训练
- 单 prompt-opt run <2h <$20;升级到 LoRA 后单 run <12h <$30
- README + 2 个真实 demo(其中至少 1 个走完整"便宜→升级"剧本)

#### Time estimate under 你的约束

- 给定 intake(35 h/周 × ~10-12 周): **~10-11 周 / 350-420 h**
- Confidence:**M-H**
- 不确定原因:两类工作流 + ledger 跨 workflow 对比的设计要简洁(防止变成"每样都有一点,没一样够强"的陷阱);若你本机无 GPU,LoRA 升级路径降级为"用 colab 手跑 + 把结果手动 import 回 ledger" 的可行 fallback

#### UX 优先级(取舍立场)

- **先便宜后昂贵**:每条 LoRA 升级前必须有便宜实验作为信号 backing
- 研究问题比运行数量更重要 — `pars review` 默认按"研究问题 → 内部 runs"组织,不按"时间线 → 所有 runs"
- 报告统一 markdown schema,跨 workflow 可叠加比较
- 高成本动作前必须人审确认("worker 准备跑 LoRA SFT,预计 8h $25,是否继续?")

#### Biggest risk(产品级)

**容易掉进"每样都有一点,但没有一样足够强"的陷阱**——这是 GPT R1 直接点出的次轴风险。两类工作流(prompt + LoRA)都做最小但都做完整,意味着 v0.1 没有任何一个剧本能"震撼"用户。**对治**:成功标准必须是"完整故事跑通",而非"两类 workflow 单独可用"。次要风险:本机无 GPU 时 LoRA 升级路径降级为手工剧本,产品体验割裂。

#### Scope-reality verdict

- **同类产品通常包含**:run ledger 是 ML 工具最低共识(MLflow runs/params/metrics/artifacts/search/compare、W&B run/config/metrics/artifacts/比较)— 用户真正期待的是"结果可比较",不是 forum 或复杂调度(GPT R2 搜索)
- **本候选切掉**:并行 worker / forum / sidecar — orchestration 层 2026 已饱和(`agent-orchestrator` 6.4k stars),不抢这块空间
- **本候选独有**:"先便宜筛 → 再后训练验证"的统一账本(prompt 与 LoRA 在同一研究问题下可比较)— 这是 MLflow / W&B 都不直接做的"决策流"层
- **净读**:**最贴 ML 实践者最低共识形状的安全 MVP** — 差异化中等,风险低
- **代表性同类**:MLflow Tracking(<https://mlflow.org/docs/latest/ml/tracking/>)、W&B Models(<https://docs.wandb.ai/models/track>)、Trackio(<https://huggingface.co/blog/trackio>)

#### Best fit for 一类人

你**没有 24GB+ GPU 或对 LoRA 是不是真痛点不确定**,但**确定**自己接下来 6-12 周会做研究探索,**重视**"判断速度"多于"训练能力";或者你**既想做 prompt 实验也想留一条后训练升级路径**,但不想为"完美扩展性"买单。如果你已经 100% 确定要全押后训练,看候选 A。

---

## 比较矩阵

| 维度 | 候选 A · RecallKit | 候选 B · BenchLedger |
|---|---|---|
| v0.1 周数 | ~10 周 | ~10-11 周 |
| 工时预算 | 380-420 h | 350-420 h |
| 主 persona | 已确定要做 LoRA 的 ML 从业者 | 在便宜实验与后训练间摇摆的研究者 |
| 主导 UX 优先级 | 决策证据化 + 失败归因 | 判断速度 + 跨 workflow 比较 |
| 工作流数量 | 1(LoRA SFT 决策循环) | 2(prompt-opt + LoRA 升级路径) |
| Worker 数 | 1 严格顺序 | 1(v0.1)/ 可选 +1 sidecar(v0.2) |
| 是否需本机 GPU | **必需 24GB+ 显存** | 推荐有,无 GPU 也能用大部分功能 |
| Run ledger / compare | ✅ 必备 | ✅ 必备 |
| LLM-as-judge | ❌ 不做 | ❌ 不做 |
| forum / leaderboard | ❌ 不做 | ❌ 不做 |
| 工作流契约 | ❌ 不做 | ❌ 不抽象,第二工作流用复制 + 改 |
| 业务模式 | OSS 免费 | OSS 免费 |
| 平台 | CLI | CLI |
| 最大风险 | 本机 GPU 是 go/no-go;诚实负面 demo 价值弱化 | "每样一点,无一致命"陷阱 |
| Scope-reality fit | ✅ 生态空白(差异化最强) | ✅ ML 工具最低共识(差异化中等) |
| 适合你的工时预算 | ✅ 紧但能塞下 | ✅ 较舒适 |
| 是否守住所有红线 | ✅ | ✅ |
| Confidence | M(GPU + Axolotl/Unsloth 选型 + stuck 状态机不确定) | M-H(两类 workflow 设计简洁性是主要风险) |

---

## 被淘汰候选(以及淘汰理由)

为什么主菜单只有 2 个候选,而不是 3 个?L3R2 双方对以下两个候选有明确分歧,本菜单选择**显式淘汰** + 标注理由,而不是把它们留作"为了凑 3 个"的填充候选。这是给你的透明决策记录。

### 已淘汰 1 · "DemoBench" — 纯 prompt-opt + 完全跳过后训练

- **来源**:Opus R2 Refined C
- **GPT R2 立场**:明确建议淘汰("既弱化 intake 后训练信号,又落入饱和赛道")
- **Opus R2 立场**:保留为"学习项目位"
- **淘汰理由**:
  1. 与 intake 备注**直接冲突**——人类明确写 "会涉及一些后训练" 是关键正向信号,prompt-only 候选**字面违反这个信号**
  2. **生态饱和**:`agent-orchestrator` 6.4k stars + `parallel-code` / `parallel-cc` / `nano-claude-code` 等已存在;"用 Claude Code 跑 prompt 实验" 在 2026 年很难差异化(双方 R2 搜索一致)
  3. 候选 A 已经能在 ~10 周内 ship 后训练版本,候选 B 留了"便宜实验" 的余地——DemoBench 的"6 周快速 ship" 优势已被候选 B 的 350-420 h 紧 budget 吸收
- **如果你仍要这条路**:fork 候选 B,在 `/scope-inject` 中明确写"删除 LoRA 升级路径,只保留 prompt-opt + run ledger"

### 已淘汰 2 · "主线 + 摘要搭档 (sidecar)"

- **来源**:Opus R2 Refined B 把 sidecar 混入 Cockpit;GPT R2 Refined C 单独把 sidecar 作为候选
- **GPT R2 立场**:自己就把这一档评为"最弱"的一档("价值不够硬,容易沦为'多一个 agent、少一点清晰'")
- **Opus R2 立场**:把 sidecar 混入 Cockpit 但承认 "可能像 agent-orchestrator 这类已有项目吃掉空间"
- **淘汰理由**:
  1. 双 worker(主线 + sidecar)** 在搜索数据下没有产品理由**——orchestration 层已经满,sidecar 的"摘要 / 减脑负担" 价值在 single-operator 场景下偏弱
  2. **复杂度可能爆炸**:sidecar 看似轻量,但要解决"和主 worker 共享上下文"、"避免重复 token 烧"、"摘要的可信度"等问题——这些都是 v0.2 议题
  3. 候选 B 已经覆盖了"减脑负担"的核心需求(run ledger + 跨 run compare + 决策报告),不需要 sidecar
- **如果你仍要 sidecar**:把它作为候选 B 的 v0.2 增量,**v0.1 不上**

---

## 综合者(synthesizer)的推荐

> **本推荐是有条件的——条件就是上面那个"本机硬件 ❓"。**

### 如果你有 24GB+ 显存的合格 GPU **且** 后训练是真实高频痛点
→ **fork 候选 A(RecallKit)**

理由:你的 intake 备注 "会涉及一些后训练" + 候选 A 是 R2 搜索数据指向的"生态空白点"(Axolotl/Unsloth 是训练框架,无 agent 控制层)。窄而深,差异化最强,1 worker 顺序的简单性也最对得起你"速度+成本+简单"三优先。

### 如果你对 GPU 或 LoRA 是不是真痛点的**任一项**不确定
→ **fork 候选 B(BenchLedger)**

理由:候选 B 的"便宜实验先,后训练作为升级路径"模型对硬件没有硬要求,即使本机无 GPU,LoRA 升级路径仍可降级为"colab 手跑 + 手动 import 结果回 ledger" 的可行 fallback。candidate B 的 Scope-reality 也最接近 ML 工具的最低共识形状(MLflow / W&B 的 runs+compare),风险更低。

### 不要默认选哪个

L3 不替你决定 GPU 这个 ❓。**fork 前请先回答自己**:
- 我现在用什么机器?(具体型号、显存、CPU)
- 我能在本周内验证 Qwen3-4B QLoRA 能在我机器上跑通一个 epoch 吗?
- 如果不能,我接受候选 B 吗?

回答完上述三问再 fork。

---

## 诚实检查 — 本菜单可能低估了什么

按 SKILL 要求列出。这些是双方 R2 都没充分讨论但你应该知道的盲点:

1. **MPS / Apple Silicon 路径未实测**:候选 A 假设你有 NVIDIA 24GB+ GPU。若你的本机是 Mac Studio (M2/M3 Ultra),MPS 跑 7B QLoRA 是技术可行但**两轮辩论都没认真考察**生态成熟度。如果你是 Mac 用户,fork 后要在 L4 spec 阶段花 1 天做 MPS PoC。
2. **"诚实负面 demo" 是否真能 ship**:候选 A 的 success 标准包含"即使 LoRA 没真提升 baseline,也算 ship 成功"。但**OSS 用户对负面 demo 的接受度未验证**。如果你重视 GitHub star,这一点可能让你 v0.1 看起来比候选 B "失败"。
3. **候选 B 的"便宜→升级"剧本要靠你自己 demo**:候选 B 的成功 hinge on 至少 1 个完整剧本能跑通,但**这个剧本的题目是什么**两轮辩论都没具体化。fork 前你最好提前想 2-3 个候选研究问题(如"COVE 在 HumanEval 上是否提升?"、"Qwen3-4B 在某私有领域 SFT 后是否在 held-out 上更好?"),作为 v0.1 的"演示题"。
4. **moderator-notes 的 24 项 P0/P1/P2 在 single-operator + ≤2 worker 下大部分自动失效**(forum poisoning / capability token / 多 worker 协调 / Stage 1.5 都不再相关),但**API key exfil + prompt injection → pip 供应链 + LoRA stuck 误杀** 这三项**仍然真实**——两个候选都已 IN 了对应的最小 hook,但 L4 spec 阶段需要重新动员这些项。
5. **跨 run 知识迁移未在两个候选中**:候选 B 的 ledger 支持跨 run 比较,但**不会主动把"上 run 的发现"喂给下 run 的 worker**。这意味着 worker 每次都从零开始读 ledger。如果你后期发现这是真痛点,会需要 v0.2 加一层"上 run 摘要 → 下 run 系统提示"的轻量机制。

---

## 决策菜单(给操作员)

### [F] fork 一个候选进入 L4

```
# 选 A(后训练决策循环)
/fork 003 from-L3 candidate-A as 003-pA
/plan-start 003-pA

# 选 B(研究问题账本)
/fork 003 from-L3 candidate-B as 003-pB
/plan-start 003-pB
```

### [MF] 同时 fork 两个并行 PRD

```
/fork 003 from-L3 candidate-A as 003-pA
/fork 003 from-L3 candidate-B as 003-pB
# 然后各自 /plan-start,看哪个 spec 阶段更顺
```

> **建议**:除非你**真的**想看两份 spec 对比,否则不推荐 MF。L4 工时成本高,2 份 spec 同时推进 = 2× spec 时间 + 决策疲劳。

### [R] 重新 scope(不满意菜单的话)

```
/scope-inject 003 "<你的新限定,如:删除 LoRA 升级路径、只保留 prompt-opt;或:加入 sidecar 摘要搭档作为 v0.1 必需>"
/scope-next 003
```

### [B] 退回 L2 — 重新想 idea

```
/status 003
# 然后人工编辑 discussion/003/L2/stage-L2-explore-003.md 或重新 /explore-start 003
```

### [P] Park

```
/park 003
```

### [A] Abandon(带 lesson doc)

```
/abandon 003
```

---

## Fork log

(fork 命令运行后由 /fork 自动追加)

- 2026-04-24T06:44:36Z · 候选 A "RecallKit" forked as `003-pA`(status: just-created)
  - 操作员硬件 context:1× RTX 4090 24GB 本机 + 可动态 1-8× H200 弹性云,小模型方向
  - 红线澄清记入 `discussion/003/003-pA/FORK-ORIGIN.md`(C5)
  - 候选 B 暂不 fork(操作员明确"优先 A,后面会考虑 B")
