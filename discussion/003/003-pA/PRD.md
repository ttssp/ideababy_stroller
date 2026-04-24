# PRD · 003-pA · "RecallKit" — 单人后训练决策循环

**Version**: 1.0(human-approved via fork)
**Created**: 2026-04-24T06:44:36Z
**Source**: `discussion/003/L3/stage-L3-scope-003.md` · 候选 A "RecallKit"
**Approved by**: human moderator
**Status**: 待 L4 / spec-writer 接手

---

## 1. Problem / Context

ML 从业者在做后训练实验(LoRA / SFT)时,真实痛点不是"训练框架不够多" — Axolotl、Unsloth、TRL、torchtune 都很成熟。痛点是**决策回路慢且容易自欺**:

- 写 baseline 脚本 → 跑 → 写 LoRA 脚本 → 跑 → 拼 eval → 看 log → 自己解读 — 全程手工拼接,每个步骤都可能出错
- "训练 loss 在降"不等于"eval 在涨";"eval 涨了 1%" 不等于"值得继续这个方向"
- 失败原因经常是 **数据格式错** / **学习率太大** / **eval 集与训练集分布漂移** / **基线本来就够强**,但你要读半小时 log 才能定位
- 跑完一次想换超参重跑 — 又是一遍手工拼脚本
- 5 个想法不知道哪个值得花 12 小时跑 LoRA

**RecallKit 的核心承诺**:让 1 个 Claude Code worker 自动完成 baseline → LoRA → eval → 决策报告闭环,**强制带失败归因**,你睡觉,早上看 markdown,给出"继续/停止/改方向"的证据化判断。

**生态定位**:Axolotl/Unsloth 是训练框架,**没有 agent 控制层**。RecallKit 在生态空白处。最低共识承诺:本地 run ledger + compare(对齐 MLflow / W&B / Trackio 的 runs/params/metrics/artifacts/compare 共识)。

---

## 2. Users

**Primary user**:**操作员本人**(single-operator)。

具体画像:
- 已有 Claude Code 与 Anthropic API 使用经验
- 已有 ML 工程基础(能读训练脚本,理解 LoRA / SFT / eval 概念)
- 主要研究方向:**小模型(7B 及以下)**
- 硬件:1× RTX 4090 24GB 本机 + 可动态申请 1-8× H200 弹性云
- 真实痛点:"有 N 个 LoRA 假设想验证,手工拼一遍流程要半天"

**Non-users**(v0.1 不服务):
- 团队 / 多用户(intake 红线)
- 没有本机 GPU 的人(候选 B 服务这群人)
- 想做 RLHF / DPO / RLOO 的人(v0.1 仅 LoRA SFT)
- 想做大模型(70B+)训练的人

---

## 3. Core user stories

| # | Story |
|---|---|
| **U1** | 作为研究者,我能用一行 CLI 定义研究问题 + 成功标准 + baseline,不用先写一堆 yaml。 |
| **U2** | 作为研究者,我能让 worker 自动跑 baseline → LoRA → eval 全流程,过夜后看 markdown 决策报告。 |
| **U3** | 作为研究者,worker 必须**自我归因失败**(loss 不下降?数据格式不对?LR 太大?),不让我自己读 log。 |
| **U4** | 作为研究者,我能 `pars retry --hypothesis "学习率太高"`,worker 改超参在原 run 基础上重跑(不重新生成所有脚本)。 |
| **U5** | 作为研究者,所有 artifact 落入**本地 run ledger**,我能 `pars compare runA runB` 跨 run 对比指标 / 配置 / 结论。 |

---

## 4. Scope IN(v0.1)

### 4.1 用户接口
- CLI 命令套:`pars sft start / status / retry / report / compare`
- 单一 markdown 决策报告作为最终产出物(强制含失败归因)

### 4.2 执行模型
- **1 worker 严格顺序**(无并行,无 forum,无 leaderboard,无 sidecar)
- worker = `claude -p` headless 进程,跑在 git worktree 里
- 全程可重启 / 可 resume(checkpoint 写盘到 worktree 外)

### 4.3 训练后端
- Axolotl **或** Unsloth 任选其一作训练后端(L4 spec 阶段二选一)
- 不自研训练框架
- 仅 LoRA SFT(不做 RLHF / DPO / RLOO 等其他后训练算法)

### 4.4 评测后端
- LM Eval Harness **或** 自包装小脚本作评测后端(L4 spec 二选一)
- eval 进程**外置**(与 worker 进程分离),避免 worker 自评作弊

### 4.5 Stuck 检测(关键 — 训练态白名单)
- 状态机区分:idle / training / downloading / truly_stuck
- 仅 `truly_stuck > 15min` 才 SIGINT
- 判据:GPU util / 子进程 CPU / 磁盘 IO 任一活跃即 not stuck
- 防止 LoRA 一 epoch 30-90min 全程无 tool_use 被误杀(预 L3 P1-10 真实成本)

### 4.6 Budget 控制
- 全局 USD 硬上限(超即 SIGINT)
- 训练 wall-clock 上限
- 本机 GPU hours 上限
- 简单实现(打印 + Redis 不必要,文件 lock 即可)

### 4.7 本地 Run Ledger + Compare
- 每 run 落 `runs/<id>/{config.yaml, metrics.jsonl, artifacts/, report.md}`
- `pars compare runA runB`:跨 run 对比 config / 指标 / 结论
- 跨 run 引用允许(`pars sft retry --from <run-id>`)

### 4.8 最小 Safety
- API key 走环境变量(`ANTHROPIC_API_KEY` / `HF_TOKEN`)
- worker 容器**不接触** key(L4 spec 决定:用 sub-key 或 API proxy 或 env-only)
- 最小 deny 清单:`rm -rf /` / `curl 外部` / `cat .env`
- `pip install` **仅允许**从锁定 `requirements-locked.txt`(防 P0-6 pypi 供应链)
- worker 工作目录与 host `.claude/` 配置只读分离(防 P0-2 hooks 自改)

### 4.9 决策报告
- markdown 强制含:训练曲线 PNG + 分数对比表 + worker 自我归因(loss 上升明说,eval 退步明说)
- 不允许 LLM 美化("模型自己声称的提升"必须有 eval 数字 backing)

### 4.10 文档
- README + 1 个真实可复现 demo(`gsm8k-100-lora-qwen3-4b` 或类似小模型 demo)

---

## 5. Scope OUT(明确不做)

### 5.1 与多 worker / 协作相关
- ❌ 多 worker 并行
- ❌ Forum / leaderboard / sidecar
- ❌ Worker 间互通(reasoning:1 worker 顺序已能解决"决策"问题)

### 5.2 与其他工作流相关
- ❌ Prompt 优化 / agent scaffold 工作流(那是候选 B 的剧本)
- ❌ Workflow 插件契约 / 通用扩展接口(过度设计)
- ❌ 多研究问题并发(v0.1 一次跟一个研究问题)

### 5.3 与训练算法相关
- ❌ RLHF / DPO / RLOO / 全参微调(留 v0.2)
- ❌ Multi-modal / vision 后训练
- ❌ 自研训练框架

### 5.4 与基础设施相关
- ❌ Docker / 容器化(intake 红线)
- ❌ 复杂调度器(asyncio scheduler / GPU 分配信号量,intake 红线)
- ❌ Runpod / 云 GPU 自动调度(intake 红线澄清:见 Constraints C5)
- ❌ Web UI / Streamlit dashboard
- ❌ 多用户 / 账号 / 权限系统(intake 红线)

### 5.5 与"高级 agent 能力"相关
- ❌ LLM-as-judge(v0.1 完全人审 + 客观 metric)
- ❌ 自动种子扩展(human 写就行)
- ❌ 文献挖矿 / Meta-review / 自我演化提示重写
- ❌ 向量库 / 语义检索(grep 即可)
- ❌ BenchJack 红队 / 攻击仿真
- ❌ Cross-run 知识迁移 / AgentRxiv 风格

---

## 6. Success — observable outcomes

| # | Outcome | 度量方式 |
|---|---|---|
| **O1** | 一周内能跑完 1 个 baseline + 1-2 个 LoRA 变体 + 决策记录 | 自跑 demo 验证 |
| **O2** | markdown 报告**必有**训练曲线 PNG + 分数对比表 + 失败归因文字 | 报告 schema 校验 |
| **O3** | 重启电脑后 `pars sft resume` 能续上中断训练 | 集成测试 |
| **O4** | README 给 1 个真实可复现 demo(即使是"诚实负面 demo"也算 ship 成功) | demo 可在他人本机重现 |
| **O5** | 端到端单 run < 12h、< $30 API 费 | 计时 + 账单 |
| **O6** | `pars compare runA runB` 输出可读的差异表(config / metric / 结论) | 集成测试 |
| **O7** | Stuck 检测在 LoRA 一 epoch 30-90min 全程不误杀 | 集成测试(用真实小模型 LoRA 任务验证) |

**Ship 标准**:O1-O7 全部达成 + GitHub repo 含 README + 1 个可复现 demo。

---

## 7. Real-world constraints

| # | Constraint | Source |
|---|---|---|
| **C1** | v0.1 在 ~10-12 周内交付(2026-04-24 起算到 ~2026-07 中) | L3R0 intake Block 1 |
| **C2** | 单人 × 30+ h/周 → 总预算 350-450h | L3R0 intake Block 2 |
| **C3** | OSS 免费,GitHub 即分发渠道(无 landing / 定价 / 注册) | L3R0 intake Block 3 |
| **C4** | 平台:CLI 优先,本地极简 web 可有可无(L4 spec 决定) | L3R0 intake Block 4 |
| **C5** | 训练后端假设 = 本机 GPU(操作员有 1× 4090 24GB);**不实现**云 GPU 自动调度(操作员手工把任务跑到 H200 是用户行为,不是产品功能) | L3R0 intake Block 5 + FORK-ORIGIN.md 硬件 context |
| **C6** | 不做 Docker / 多用户 / 复杂调度 / Runpod 集成 | L3R0 intake Block 5(红线) |
| **C7** | 必须支持 LoRA SFT(单 GPU 单任务) | L3R0 intake Block 5(关键正向信号) |
| **C8** | 优先级:速度 + 低成本 + 技术简单(三选三) | L3R0 intake Block 6 |
| **C9** | 训练脚本与 checkpoint 路径**需可移植**(便于操作员手动 rsync 到 H200 跑大任务) | FORK-ORIGIN.md 硬件 context |
| **C10** | API key 不进 worker 容器 / worktree(env-only 或 proxy) | 预 L3 moderator-notes P0-5 衍生 |

---

## 8. UX principles(tradeoff stances)

1. **CLI 主流程永远顺序**(start → 完成 → report),无"哪个 worker 先完成"的并发认知负担
2. **报告不允许 LLM 美化**:loss 上升明说,eval 退步明说;"模型自己声称的提升"必须有 eval 数字 backing
3. **短输出 > 进度条堆 token**:允许后台跑 + 回来 `status` 查看
4. **失败归因强制**:worker 不能交"成功了"或"失败了" — 必须给出可读因果链
5. **本地优先**:所有数据本地,不传云;run 历史 = 本地目录
6. **demo 可演示性 > 功能堆砌**:1 个能跑通的真实 demo 胜过 10 个"理论上能用"的功能

---

## 9. Biggest product risk

**本机硬件就是 go/no-go 决定** — 操作员已确认有 4090 24GB,gate 通过。但运行时风险仍真实:
- 7B 模型 QLoRA 在 4090 24GB 上紧张但可行;若想做 8B+ 需手动迁到 H200
- LoRA stuck 检测状态机若做不对,15min 误杀会让操作员怀疑模型能力,debug 几天才发现是检测 bug
- 若 baseline 跑出来发现 LoRA 没真提升,v0.1 演示价值弱化(但可作为"诚实负面 demo")
- worker 自我归因失败的质量是产品核心 — 若 LLM 给的归因都是"可能是数据问题,可能是超参问题",产品价值崩塌

---

## 10. Open questions for L4 / Operator

| # | Question | 谁来答 | 何时 |
|---|---|---|---|
| **OQ1** | 训练后端选 Axolotl 还是 Unsloth?(取舍:Axolotl YAML 灵活 vs Unsloth 速度内存优势) | L4 spec-writer + 操作员 | spec.md 写之前 |
| **OQ2** | 评测后端选 LM Eval Harness 还是自包装?(取舍:LM Eval 完整但重 vs 自包装快但要自己维护) | L4 spec-writer + 操作员 | spec.md 写之前 |
| **OQ3** | demo 选哪个数据集 + 模型组合?(候选:Qwen3-4B + GSM8K-100 / Llama 3.1 8B + Alpaca 子集) | 操作员 | demo 准备阶段 |
| **OQ4** | worker 写训练脚本是从零生成还是从模板修改?(取舍:零生成灵活 vs 模板可控) | L4 spec-writer | spec.md 关键决策 |
| **OQ5** | "失败归因"的具体 schema?(自由文本 vs 结构化字段) | L4 spec-writer | architecture.md |
| **OQ6** | run id 命名规则?(ULID / 时间戳 / 用户命名) | L4 spec-writer | 技术细节 |
| **OQ7** | 是否需要"研究问题 = 多 run 集合"的概念?(候选 B 有,候选 A 默认无,但可能 v0.1 也用得上) | 操作员 | spec.md 写之前 |

---

## PRD Source

This PRD was forked from L3 candidate A at 2026-04-24. Contents are derived from the approved L3 candidate plus operator hardware context. For full context (why this cut vs siblings, scope-reality verdict, comparison matrix, eliminated candidates rationale), see:

- **L3 menu**: `discussion/003/L3/stage-L3-scope-003.md`
- **L2 unpack**: `discussion/003/L2/stage-L2-explore-003.md`(原 PARS 14 周方案,作为 L4 architecture 参考)
- **Pre-L3 adversarial review**: `discussion/003/L3/moderator-notes.md`(24 P0/P1/P2 findings,L4 应消化与 v0.1 相关者)
- **FORK-ORIGIN.md** in this directory(硬件 context + 红线澄清)

This PRD is the **source of truth** for L4(spec-writer)。Changes to PRD require explicit human approval — never auto-revised by L4 agents.
