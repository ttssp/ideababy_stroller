# L3R0 · Human Intake · idea 004

**Captured**: 2026-04-24T11:55:00Z
**Method**: AskUserQuestion interactive (分 3 批, 共 10 个问题)
**Origin**: Root idea 004, L2 ran full (L1 menu skipped, L2R3 re-framed after moderator-notes)
**L2 verdict**: `unclear` (参见 stage-L2-explore-004.md)

---

## Block 1 — Time reality

### Q1. v0.1 交付时间
- ✅ **3-6 周 (中等量级)**
- 含义: core loop 能跑通 — 咨询师观点抓取 + 结合关注列表 + 白话解释 + 简单私有模型。**不做**: backtest 环境、多市场 cross-signal、事件日历主动预警、paper trading (这些是 v0.5+ 的事)。

### Q2. 每周可投入小时数
- ✅ **15-30 小时 (专注)**
- 含义: 3-6 周 × 15-30 小时 = **45-180 小时预算**。L2R3 Opus 提过"维护时间 ≤ 3 小时/周"红线 (指 v0.1 ship 后稳定期); 开发期不受此限。

---

## Block 2 — Audience

### Q3. User slice (N/A, 因为只有 1 个用户 = human 本人)
- ✅ **用户 = human 本人 (非商业化, L2 moderator-notes 明确)**
- L3R1 两个模型**不应**在这一层提"用户画像候选"——只有一个具体人, 画像参见 L2 §1 (ML PhD + 付费订阅华语投顾 + 金融初级 + 三市场 30-50 股 + 能承受 20% 回撤 + 每年 $500 数据预算)。
- **候选差异应在 core loop 形态, 不在 audience**。

---

## Block 3 — Core promise 定位 (替代了标准"business model"问题 — 因为非商业化)

### Q4. Core loop 定位 (GPT L2R3 指出的结构性选择)
- ✅ **Balanced (均衡 calibration + action)**
- 含义: Agent 既帮你 "不动", 也主动提 "备选标的/仓位调整"。两类建议比例大致 1:1。
- **关键约束**: human 需要自己设计重要的"动手阈值" — L3R1 两个模型应该**把"动手阈值"作为 Candidate 设计的核心变量** (阈值严 = Candidate 更偏 calibration-first, 阈值松 = 更偏 action-first)。

---

## Block 4 — Success definition (GPT 必答 #1)

### Q5. "稳定赚钱"的精确定义
- ✅ **跑赢标普 2-5%/年 (温和 alpha)**
- 来源可能: 更好的仓位管理 + 更少的冲动错误 + 咨询师+私有模型的信息翻译. 不追 5%+ alpha model (那需要统计学级 rigor, 超出 v0.1)。
- **Success observable for v0.1**: v0.1 不要求已达到 2-5% alpha (只有 3-6 周数据), 但要求**"机制成立"** — 即 Candidate 要能描述**它为何能在 6-12 个月达到这个目标**。

---

## Block 5 — Conflict resolution (GPT 必答 #2)

### Q6. 咨询师 vs 私有模型 vs agent 综合建议 三路冲突时
- ✅ **Agent 泳道汇合 (显式冲突报告, 无默认优先级)**
- 含义: Agent 不隐藏任何一路, 冲突时明确字面报告 "咨询师取 A, 模型取 B, 我最新得出 C, 三者分歧根本原因是 X", human 自己决策。
- **对 L3R1 设计的要求**: "冲突报告界面"是 v0.1 必须包含的一个 UI 元素。这是一个 **scope IN** 项, 不是 nice-to-have。

---

## Block 6 — Cadence (GPT 必答 #3)

### Q7. Agent 主动程度 (推送频率)
- ✅ **每周 1 次 (周报) + event 触发 (FOMC / 财报 / 重大异动)**
- 含义: **不是**每日晨报机. 每周一次是默认节拍 (周日晚?), event 是例外不是常态。
- 防 "看盘焦虑机" 红线: L2R3 已列入 natural limits。这条强化为 v0.1 hard constraint。

---

## Block 7 — Platform

### Q8. 平台 (多选)
- ✅ **Telegram bot** + **简易本地 Web UI (localhost + 图表)**
- 含义: 交互的两个形态都要。**Telegram** 承载"周报 + event 快速通知 + 简单询问"; **Web UI** 承载"错位矩阵图 / 持仓分布 / 决策历史 / 私有模型调参" 这些图表和 research 类任务。
- **排除**: CLI (human 特意未选), Jupyter (未选 — 但 Jupyter 风格的 research 功能可以嵌入 Web UI)。
- 不要求是 production-grade, localhost 即可。

---

## Block 8 — Priorities

### Q9. Tradeoff 冲突时哪一条最重要 (多选 1-2)
- ✅ **投资准确度 (研究强度)** — human 明确愿意为"每次建议的技术指标都竟试准"妥协 1-2 周开发时间
- 隐含 (未选): 上线速度、技术简单度、UX 细节都在此之下
- **对 L3R1 的设计影响**:
  - 如果某个 Candidate 用了更准确但时间成本更高的 path (如 "私有模型 v1 用 XGBoost + 技术指标 而不是纯 LLM 直接出信号"), 这个 Candidate **应该受优先级加分**, 即使交付时间更接近 6 周上限。
  - "研究 rigor" 比 "UX polish" 重要; 比 "技术简单度" 重要; 比 "上线速度" 也略重要。

---

## Block 9 — Red lines

### Q10. 红线
- ✅ **没有特别新的红线** — L3R1 两个模型应按 L2R3 Opus §5 和 moderator-notes 已列的红线"推"
- L2R3 已列的核心红线 (L3R1 必须 honor):
  1. 不自动下单 (保留最终决策权)
  2. 不做期权 / 加密 / 高杠杆 / 日内
  3. 每次建议必须白话解释, 不许变"信号黑箱"
  4. 不许变"看盘焦虑机" (通知节制: 每周 + event, 不超)
  5. 工具维护时间 ≤ 3 小时/周 (稳定期)
  6. Agent 不许诱导"更高频交易" (Barber-Odean 铁律)
  7. 防"学习假装发生" (3 个月后仍说不清关键指标 = 失败)
  8. 不许路径依赖单一咨询师

---

## Block 10 — Freeform (💡)

### Q11. 其它需要 L3R1 知道的
**💡 Human's note** (一字不改):

> 我付费的投资分析师的建议是通过微信小程序发给我的。有视/音频, 有 pdf, 有图有文字。我现在是用 proxyman 监听拿到地址再 fetch 下来的。这部分信息对我很有用。得仔细想想怎么能自动化的获取这些消息。

**对 L3R1 设计的 scope 含义** (不谈具体实现, 只谈 scope):
- 咨询师信息 = **微信小程序内容**, 含视频/音频/PDF/图文. 目前 human 用 Proxyman 手动监听 + fetch, 已有 URL pattern 可复用。
- **v0.1 scope 必须包含**: 一个能接收已 fetch 内容并结构化解析的 pipeline (不管具体抓取自动化程度 — 可以是 human 半自动触发 → agent 解析, 也可以是 agent 调度 → 接管手动触发)。
- 多模态现实: **视频 + 音频 + PDF + 图 + 文本** 都要能被 agent 消化 → 转成结构化 (模型 → 方向 → 标的 → 置信度)。
- 这是一个**比 L2R3 想象的更具体/更难的 input pipeline** — L3R1 两模型应该在 Candidate 里**明确这部分的 scope 边界**:
  - Candidate 可能会差异化在: 解析多模态的深度 (Candidate A = 只解析 PDF/文本, Candidate B = 加音频转录, Candidate C = 加视频抽帧识别)
  - 或差异化在: 抓取自动化程度 (Candidate X = human 手动触发 fetch + agent 解析; Candidate Y = 半自动的 pipeline 基础设施)

---

## Summary for debaters

### Hard constraints (✅) — MUST honor in every candidate
1. **3-6 周交付 v0.1** (约 45-180 小时开发预算)
2. **Balanced core loop** (calibration + action 大致 1:1, 但 human 需要设定阈值)
3. **温和 alpha 目标** (年跑赢标普 2-5%, 机制可解释)
4. **显式冲突报告** 作为 v0.1 必含 UI 元素
5. **每周 1 次 + event** 主动频率, 不做日晨报
6. **平台 = Telegram bot + 本地 Web UI (localhost)**, 两者都要
7. **优先级 = 投资准确度/研究 rigor > 其它 tradeoff**
8. **咨询师内容 pipeline 必须包含** (微信小程序多模态: 视频/音频/PDF/图文)

### Red lines (硬 no)
1. 不自动下单
2. 不做期权/加密/高杠杆/日内
3. 每次建议必有白话解释
4. 不做成日推送焦虑机
5. 工具维护 ≤ 3 小时/周 (稳定期)
6. 不诱导高频交易
7. 防学习假装 (定期测用户是否真懂关键指标)
8. 不单一咨询师路径依赖

### Soft preferences (✅ 但可协商)
- **Web UI 可以只是 localhost** (不追 production-grade polish)
- **Telegram 承载推送 + 快速询问**, Web UI 承载图表 + research
- **15-30 小时/周 是中位数, 波动允许**

### Unknowns (❓) — 模型应在 L3R1 主动提 options
1. **"冲突报告" 具体是什么形态** — 表格? 决策树? 文字? 每个 Candidate 自己提。
2. **v0.1 的"成功机制"可观察证据** — 3-6 周后怎么知道"机制成立"? 自用单人无法做 A/B test。
3. **咨询师 pipeline 的 v0.1 scope 边界** — 见下方 "策略类模块" 原则; 但具体做到哪一层 (只 PDF/文本? 加音频? 加视频?) 是 Candidate 可差异化的点。

### 🧭 关键 scope-shaping 原则 (human 2026-04-24T12:10 明确补充 — **绑定**)

Human 明确把以下模块划为"**策略类模块**", v0.1 **先留口子, 不做完整实现**, 后期独立打磨迭代:
1. **"动手阈值"的具体设定** (Balanced 里的阈值调参)
2. **私有预测模型/策略** (你自建的 ML 模型)
3. **咨询师内容解析的深度** (PDF vs 音频 vs 视频, 到多结构化)

**对 L3R1 的硬性要求**:

- **v0.1 scope 的核心 = 管道 + 壳 (pipeline + shell), 策略类模块作为 "清晰接口 + 占位实现"**
- 每个策略模块必须有:
  - ✅ 清晰的**接口契约** (输入/输出格式)
  - ✅ 一个**最简占位实现** (规则 / 手工 / 粗糙 LLM prompt 即可, 让 core loop 能跑通)
  - ✅ **单独可替换** (能独立迭代, 不影响其他模块)
- **v0.1 不要求**: 这些模块做得精准、训练到位、覆盖多模态; 这些是 v0.2+ 的事

**这让 v0.1 回答的问题变成**: "**core loop 的 pipeline + shell 能不能跑通** + **接口设计得够不够好让后期能独立打磨**", 而不是 "策略有多准"。

**Candidate 差异化的正确角度**:
- 不该在 "谁的阈值/模型/解析更准" 上差异化 (都是占位, 差不多)
- 应该在 "**pipeline 和 shell 的形态**" 上差异化 (比如 v0.1 最小 shell 只做咨询师周报 → 错位矩阵 → Telegram 推送; 中等 shell 加事件日历; 大 shell 加决策档案+私有模型接口)
- 或在 "**哪些占位是规则实现 vs 粗糙 LLM prompt vs 完全手动触发**" 上差异化

**隐含取消的 Unknown** (不再是 L3R1 要 surface 的 options):
- ❌ "动手阈值怎么定" — 占位, 后续调
- ❌ "v0.1 是否包含私有 ML 模型" — 接口包含, 实现占位, 后续训
- ❌ "咨询师 pipeline 到音频/视频" — 接口包含, v0.1 只做 PDF/文本, 后续扩

---

### 💡 Freeform 重要信息
**咨询师信息源 = 微信小程序, 多模态 (视频/音频/PDF/图文), 已有 Proxyman 手动 fetch 方案**。

按上方"策略类模块"原则处理: **v0.1 只接 PDF/文本解析** (这已经涵盖人类投顾主要信息载体), 视频/音频走接口占位 (v0.2+); 抓取自动化也走占位 (v0.1 可以是 human 粘贴 / 半自动导入, v0.2+ 做自动调度)。
