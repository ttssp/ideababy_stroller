# L3R0 · Human Intake · 003 (PARS)

**Captured**: 2026-04-24
**Method**: AskUserQuestion(交互问卷,4 批共 8 个问题)
**Source idea**: `discussion/003/L2/stage-L2-explore-003.md`(PARS 14 周/6 工程师/24 P0-P2 缺口)

---

## Block 1 · 时间现实

### Q1 · v0.1 交付目标
- ✅ 人类回答:**2-3 个月(单完整产品)**
- 含义:相当于原 L2 报告"Stage 1 + Stage 2"的子集,而非 14 周完整路线
- 与 L2 对比:L2 给的 MVP 第 1-4 周(对应 1-2 周这一档)、Prod-Ready 第 5-9 周;intake 落在两者之间偏后,意味着 v0.1 应**比 MVP 完整**但**比 L2 Prod 大砍**

### Q2 · 周投入小时
- ✅ 人类回答:**30 小时以上(全职推进)**
- 含义:按 12 周 × 35 h/周 ≈ **420 单人小时**总预算(不含睡觉 think time)
- 与 L2 对比:L2 假设 6 工程师 × 14 周 × ~30h ≈ 2520 工程小时;intake 实际可投入仅 **L2 假设的 ~17%**

---

## Block 2 · 受众

### Q3 · 首批用户
- ✅ 人类回答:**我自己 / single-operator 实验台**
- 含义:跑 1-3 worker 即可,**不需要团队治理 / 多用户 / shadow owner / runbook**
- 与 L2 对比:这**消解掉**了 L2 §7 整章 sprint 表与角色分配;moderator-notes P1-14 合同文档包大部分变得不必要(自己写代码自己看)
- ⚠️ 但 single-operator ≠ 不需要安全:prompt injection / API key exfil 仍是真实风险(参 P0-5、P0-6)

---

## Block 3 · 商业模式

### Q4 · 商业模式
- ✅ 人类回答:**完全免费 / OSS / 个人兴趣**
- 含义:**无需** auth、billing、quota 计费、计费延迟窗口、用户隔离
- 与 L2 对比:L2 §11 单位经济学讨论(每次 $600 vs 中级研究员 $3000)**对 OSS 仍部分成立**——但视角转为"我自己花的 API 钱省不省得回我自己时间"
- 推论:GitHub Repo + README 即"分发渠道",无需 landing page、定价页、注册流

---

## Block 4 · 平台

### Q5 · 平台偏好
- ✅ 人类回答:**不在乎 / 你安排**
- 含义:模型可基于优先级("速度+成本+简单")自由挑;暗示倾向 CLI 或最薄 Streamlit
- 推荐方向:CLI 主交互 + 极简本地 dashboard(Streamlit/HTML 均可)

---

## Block 5 · 红线(关键!)

### Q6 · v0.1 绝对不做
- ✅ 人类点选 + 备注:
  - **不做多用户 / 账号 / 权限系统**
  - **不做 Docker / 容器隔离**
  - **不做调度** (用户备注新增)
  - **不做 Runpod** (用户备注新增)
  - **但会涉及一些后训练** (用户备注新增 — 关键正向信号)

### 红线对 L2 架构的破坏性影响
| L2 模块 | 红线影响 | v0.1 状态 |
|---|---|---|
| M1 Orchestrator/Seed Manager | 保留(种子工程仍核心) | IN |
| M2 Worker Template | 简化(无子智能体 5 件套,可 1-2 个) | IN(瘦身) |
| **M3 Scheduler & Sandbox** | **不做调度 + 不做 Docker** → 大砍 | OUT 大部分 |
| M4 Forum + Artifact Store | single-operator 无需 forum;artifact 简化为本地目录 | OUT forum / IN 简化 artifact |
| M5 Eval Service | 后训练涉及 → eval **必须保留**(LoRA/SFT 后跑 held-out) | IN |
| M6 Budget Tracker | OSS 无 quota,但**自我成本控制**仍要 → 简化为"打印+硬帽" | IN(瘦身) |
| M7 Observability | 简化为本地日志 + 简单读取脚本 | IN(瘦身) |
| M8 Human Interface | 仅 CLI,Web 可后置 | IN(CLI) |
| M9 Safety Hooks | API key + prompt injection 仍真实 → 保留**最核心 hook** | IN(瘦身) |
| Stage 3 / GPU 弹性 / Runpod | 红线 OUT | OUT |
| 6-工程师 sprint 表 | OUT | OUT |
| Stage 1.5 / shadow owner / runtime policy | single-operator OUT | OUT |

### "会涉及后训练"的关键解读
- L2 报告提到 LoRA / Qwen3-4B 微调
- 红线没排除后训练 → v0.1 **必须**支持运行 LoRA SFT 这类任务
- 对应 moderator-notes P0-8(并发能力测试)、P0-7(非单指标任务协调)的关切**仍部分相关**:即使 single-operator,LoRA 任务画像仍要心里有数(本地 GPU 容量、显存、训练时长 vs 15min stuck 误杀)
- 但**不需要**多 worker 并发 → P0-7 / P0-8 复杂度大幅下降

---

## Block 6 · 优先级

### Q7 · 1-2 项最看重
- ✅ 人类回答:**上线速度 + 运行成本低 + 技术简单/易维护**(选了 3 项)
- 解读:这是一组**互相强化**的取向(都指向"瘦身"),不是冲突
- **没选**:polish/UX、差异化、broad appeal、安全
- 推论:候选 PRD 偏 "thin tool" 而非 "polished platform";功能砍到不能再砍仍优于"做全做漂亮"

### 优先级与红线的次生约束
| 候选 scope 决策 | 优先级排位 |
|---|---|
| 自建 vs 用现成开源 | "技术简单" → **优先用现成**(只在 glue 层创新) |
| 高级安全 vs 信任本地环境 | "速度" → **接受本地 macOS Seatbelt + git worktree 双层**,放弃容器/网络隔离 |
| 完整 forum vs append-only 文件 | "简单" → **append-only NDJSON 文件**即可 |
| 自动 LLM judge vs 人手看输出 | "成本" → **先人手看,LLM judge 后置** |

---

## Block 7 · 自由文本

### Q8 · 补充
- 💡 人类回答:**暂时没有**

---

## Summary for L3R1 debaters

### Hard constraints(✅ 必须遵守)
1. **时间**:2-3 个月交付 v0.1(对齐到 ~10-12 周)
2. **投入**:1 人 × 30+ h/周 → 单人总预算 ~360-450 h
3. **用户**:single-operator(自己)
4. **商业**:OSS 免费,无任何 SaaS 基础设施
5. **优先级**(三选三):上线速度 + 运行成本低 + 技术简单
6. **必须支持**:某种形式的后训练(至少 LoRA / SFT 单 GPU)

### Red lines(🚫)
1. 不做多用户 / 账号 / 权限
2. 不做 Docker / 容器隔离(macOS Seatbelt + worktree 上限)
3. 不做"复杂调度"(asyncio scheduler / GPU 分配 / 并发信号量等)
4. 不做 Runpod / 云 GPU(本机为限)

### Soft preferences(可调)
- 平台:CLI 优先,本地 web 可有可无
- 单 worker / 双 worker / 三 worker 都接受 — 模型自定

### ❓ 不明 / 让 L3R1 提选项
- v0.1 究竟跑哪一类研究任务?(Prompt 优化?Agent scaffold?LoRA SFT 单任务?三选?)
- 是否要保留 forum 风格的 worker 自我互通 vs 完全顺序串行执行?
- 是否要 LLM-as-judge,还是 v0.1 完全人审?
- "会涉及后训练" 的最小切口:仅"包装 LoRA 训练脚本 + eval 闭环"够不够?

### 模型应主动提的红线候选(human 没列出但可能漏掉的)
- 不做"自我演化提示重写"(Stage 3 Meta-review)
- 不做向量库 / 语义检索
- 不做 BenchJack 红队 / 攻击仿真
- 不做 Streamlit dashboard (CLI 即可)
- 不做种子 LLM 自动扩展(human 写就行)

### 关键张力(给 L3R1 模型)
"single-operator + 不做调度 + 但要后训练" 这三者在 L2 原架构里**几乎所有模块都要重定位**——你的工作是在 ≤450h 总预算下,把 PARS 浓缩成**有意义、能用、能展示**的最小可行子集。
