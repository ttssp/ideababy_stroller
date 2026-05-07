# PRD · 004-pB · "决策账本 (承诺壳, impulse → discipline calibration)"

**Version**: 2.0  (按新 scope-protocol 重生成 — 拆 Scope OUT 与 Phased roadmap)
**Created**: 2026-04-29T03:35:31Z
**Source**: discussion/004/L3/stage-L3-scope-004.md · Candidate B
**Approved by**: human moderator (此版按更新后的 fork.md 模板再跑一次, v01 已归档为 PRD_v01.md)
**PRD-form**: phased
**Phases**: [v0.2, v0.5, v1.0, v1.5+]
**Phase-current**: v0.2
**Migrated**: 2026-05-07 (retroactive backfill — 本 PRD §6 已含 Phased roadmap,phased 标识反映 PRD 实际形态)

> **本版与 v01 的关系**: 内容来源同 (Candidate B), 但结构按更新后的 scope-protocol 拆分:
> - v01 的 §5 "Scope OUT" 把红线非目标 + v0.2/v0.5/v1.0/v1.5+ 阶段规划压在一起
> - v2.0 拆为: §5 Scope OUT (永远不做, 红线) + §6 Phased roadmap (committed, 按阶段交付)
> - 协议根因修复见 commits 76ee06c / 4071a23 / c1b5686 (branch `chore/scope-protocol-split-roadmap`)
> - 两版差异详细对比: `discussion/004/004-pB/COMPARE-v01-vs-v02.md`

## 0. Current state (本 PRD 文档代表的项目阶段)

> **v0.1 已 ship 于 2026-04-27** (`projects/004-pB/docs/v0.1-ship-summary.md`).
> 本 PRD 是 ship 当时的快照 + 未来 roadmap, **不是 forward-looking spec**.
> §1-§5 / §7-§10 描述的是 v0.1 设计意图 (大部分已落地);
> §6 是 v0.1 之后的 committed roadmap, 下一个 milestone = **v0.2** (1-3 个月内).
> §11 是 L4 spec-writer / v0.2 启动需要回答的 open questions.

**当前位置**:
- ✅ v0.1 spec / architecture / 632 测试 ship 完成
- ⚠️ v0.1.1 hotfix 余项: 见 `docs/known-issues-v0.1.md` (Codex review F1/F2/F3 处置)
- 🔜 v0.2 NEXT (见 §6.v0.2): 笔记 wiki 升级 + 自动化咨询师监控 + 私有模型 v1
- 📅 v0.2 启动前必读: §11 open questions + §6 v0.2.x 的 "v0.1 已留位 (实测)" 一栏

## 1. Problem / Context

Human 的痛点不是"我信息不够", 是"我约束不够"——知道很多, 但压力下不稳定, 临场乱动。Barber-Odean 等长期研究表明散户越频交易表现越差; calibration engine (校准自我) 必须早于 action engine (优化具体决策)。

GPT L3R2 scope-reality search 验证: Fiscal.ai / Koyfin / Aiera / Bridgewise / 雪球付费 五项产品全做**信息壳** (给你更多更快的信息), 无人做**承诺壳** (让你减少乱动)。B 是 uniquely 空白的 market slice。

L2 verdict 是 `unclear` (没有外部证据证明此机制能稳定赚钱), 所以 v0.1 的 success 不是"赚到 alpha", 而是"机制起作用的 proxy 可观察" — 8 周内可以从决策档案里筛出 "≥ 3 次 agent 阻止冲动动作"的记录。

## 2. Users

**Primary user (单一)**: human (project owner) 自己。

**痛点签名**:
- "回看近两月, 最后悔的是 知道很多, 但还是在焦虑里乱动"
- 动机是"成为会投资的人" (需要持续摩擦 + 自我建模), 不是"摆脱不知道该怎么办" (只想要清晰出口)

**不在受众范围**: 任何想要"免动脑投资工具"的人, 任何商业用户。

## 3. Core user stories

1. **冲突报告 + 一行理由 + 30 秒录入 (核心 loop)** — Human 想加仓 TSM → Web UI 一个 ≤ 30 秒表单 → agent 拉出冲突报告 (咨询师 A / 占位"私有"源 B / agent 综合 C + 分歧根因) → human 选(按/不按/等待) + 1 行理由 → 档案入库 + 环境快照 (价格、持仓、当周咨询师观点)。
2. **周度 review, 不动是一等公民** — 每周日 Web UI "本周档案 review": 本周做了几次 action (按 agent / 按自己 / 不动), 各自回报。**"不动"作为一等输出**, 不是失败状态。
3. **冲突报告 UI 即使占位也要先立** — Web UI 冲突报告 tab (即使 v0.1 占位信号源弱, UI 骨架先立): 三列表 + 白话根因。占位源没话说时, 显式显示"暂无分歧", 不空屏尴尬。
4. **学习闭环 — 不重复解释** — 每次术语解释自动进笔记 wiki, 下次出现时 agent **不重复解释** (防"学习假装"信号)。
5. **8 周 calibration proxy** — 8 周使用后能从档案中筛出 "3+ 次 如果没有 agent 我会操作但实际没动" 的决策 — 这是 calibration engine 真正起作用的 proxy。

## 4. Scope IN (v0.1)

- 全部 Candidate A 的 IN (咨询师 pipeline + 错位矩阵 + Telegram + 笔记 wiki + 关注股/持仓录入)
- **决策档案系统** (表单 + 环境快照 + 事后字段)
- **冲突报告 UI** (Web 三列表 + Telegram 叙事版), 含白话根因
- **Devil's advocate 占位** (LLM 简单 prompt, 每次 action 前出一句反驳)
- **周度 + 月度 review 生成器**
- **学习检查机制** (每 3 个月列出重点概念, 自查能否解释)
- **策略模块占位接口** (StrategyModule / PrivateSignal IDL — 冲突报告面上必须体现占位源的独立存在, 即使 v0.1 实现是 "一条 SMA 规则" 或 "LLM 简单 prompt")

## 5. Scope OUT (永远不做 — red-line / 永久排除)

> **协议规则**: 本节**只**列与项目身份冲突 / 红线级别 / 永远不在任何版本做的项。**不要**把"v0.2 之后会做"的功能写到这里 — 那些归 §6 Phased roadmap。
>
> v0.1 architecture 对本节列举的项**不留扩展点** — 留了反而引诱人去做。

- ❌ **自动下单** (红线 #1) — 决策档案永远要求 human 最终拍板, 不留 hook。即使 v∞ 也不破。**Why invariant**: 项目 calibration 性质决定, 自动化执行会摧毁"压力下的训练"价值。
- ❌ **期权 / 加密 / 高杠杆 / 日内** (红线 #2) — 项目身份冲突。**Why invariant**: 与"温和 alpha + 长期持有"定位完全相反, 是不同游戏。
- ❌ **隐藏式默认推荐** (红线 #9) — 三列冲突报告**永远** 不能合并; 即使 v∞ 的私有模型成熟, 三路也不能合并为一个"权威综合"。**Why invariant**: 合并就回到了"信息壳", 失去承诺壳的独特价值 (让 human 看见分歧本身就是训练).
- ❌ **"不动 / 等待"被建模为失败** (红线 #10) — 月度 review 永远要把"不动"作为正向 outcome 数据点。**Why invariant**: Barber-Odean 铁律 — "减少乱动"才是最大价值源, 反向 KPI 会摧毁此机制.
- ❌ **决策档案静默"建议你高频"** (红线 #5 / Barber-Odean 铁律) — 永远不做"agent 周建议次数 KPI", 不诱导高频。**Why invariant**: 同上.
- ❌ **跳过白话解释的"快速模式"** (红线 #3) — 任何版本都不能为了快削减解释。**Why invariant**: 学习闭环依赖白话解释, 削减就退化成黑箱.

## 6. Phased roadmap (全部 committed, 按阶段交付)

> **协议规则**: 本节列**承诺将来会做**的功能, 顺序按 (1) 当前版本痛点 (2) 实现难度 (3) 解决的风险等级。
> **不是** "可能不做" — 是"排好的实现队列, 顺序可基于使用数据微调"。
>
> v0.1 architecture **必须**为本节每一项预留扩展点, 防止 v0.2+ 启动时全栈重写。
> 来源: L2 v2 report §4 Natural extensions (continued in stage-L3-scope-004.md candidate B)。

**Maintenance hint**: 每次 ship 后 PRD 维护:
- 把已完成阶段从本节删除 (例: v0.2 ship 后, 把 v0.2 整段移到 §10 Changelog)
- 把"下一阶段"从概要升级成详细描述 (例: v0.2 ship 后, 把 v0.5 的概要展开成 v0.2-style 的详细描述)
- 这是 PRD 持续演进, 不是一次写死。

### Phase v0.2 (NEXT, 1-3 个月内 — 详细)

#### v0.2.1 个人金融笔记 wiki 升级 (主动复盘 + 概念健康度)
[难度 L, 重要度 M] — 对应解决: L2 §4 风险 #R-v0.2-1 (重复解释 / 学习假装)

**v0.2 做什么**: v0.1 已实现去重 + 自动收录, v0.2 加 "每 3 个月自查 7 个核心概念" + "agent 不再重复解释" 的 enforcement 闭环。
**完成标准**:
- 第 3 个月触发首次自查
- ≥ 7 概念独立复述准确率 ≥ 70%
- agent 在重复 query 时直接引用 wiki, 不再展开新解释 (检测方式: 同一术语 30 天内被解释 ≤ 1 次)

**v0.1 已留位 (实测)**:
- ✅ 已有: `Note` 模型 (`src/decision_ledger/domain/note.py`) + `NoteRepository`. 基础 CRUD 闭环跑通.
- ⚠️ **未留**: `concept_first_seen_at` / `concept_recall_score` / Concept 模型 (区别于 Note) **均不存在**. v0.2 启动需先扩 schema 加这些字段或新建 Concept 表.
- 🔧 v0.2 工作量: schema migration + 自查 trigger + agent prompt 加 wiki lookup 短路逻辑.

#### v0.2.2 自动化咨询师监控 (Proxyman 升级到自动化 pipeline)
[难度 H, 重要度 H] — 对应解决: L2 §4 风险 #R-v0.2-2 (咨询师信息断档)

**v0.2 做什么**: 半自动化 fetch + URL pattern 监控 + 失败告警 + 多模态 (audio/video) 解析接口实装。v0.1 是 "human 粘贴 URL + PDF parser", v0.2 加 "scheduled fetcher" 实现。
**完成标准**:
- 连续 4 周自动获取无失败 (定义 "失败" = 错过 ≥ 1 条新内容超过 24 小时)
- 失败时有人工 fallback 通道 (Telegram 告警 → human 触发手动 fetch)
- 视频/音频内容能产出文本 transcript + 关键观点提取

**v0.1 已留位 (实测)**:
- ✅ 已有: `AdvisorParser` (`src/decision_ledger/pipeline/parser.py`) + `AdvisorParserOutput` 模型. PDF/text 走通.
- ⚠️ **未留**: source / format / fetcher 三层抽象**没真的拆开** (parser.py 是单一类), format enum 不存在, audio/video 类型完全没有 IDL.
- 🔧 v0.2 工作量: (a) 把 parser.py 拆 SourceAdapter / FormatHandler / Fetcher 三层 (b) 加 ContentFormat enum (含 PDF/text/audio/video) (c) 实现 scheduled fetcher (d) 加 transcription module. **比 PRD v01 暗示的"换实现即可"重得多, 大约一周工作量**.

#### v0.2.3 简单的私有模型 v1 (XGBoost + 技术指标)
[难度 H, 重要度 H] — 对应解决: L2 §4 风险 #R-v0.2-3 (模型空转)

**v0.2 做什么**: v0.1 占位 (一条 SMA 规则 / LLM "独立判断") 升级到真 XGBoost + 技术指标特征 (RSI / MACD / 量价关系等)。
**完成标准**:
- 模型每日产生 30-50 只关注股的方向 + 置信度
- 进入冲突报告"私有模型"列, 不再是占位文字
- 模型预测口径与咨询师独立 (相关系数 < 0.5, 否则没有冲突价值)

**v0.1 已留位 (实测)** — 这是**唯一真做对的扩展点**:
- ✅ 已有: `StrategyModule` Protocol IDL (`src/decision_ledger/strategy/base.py`) + `StrategySignal` 模型 (含 `direction` / `confidence` / `rationale_plain`) + `placeholder_model.py` 占位实现.
- ✅ 冲突报告 UI 已留独立列, 占位源 v0.1 已显式区分.
- 🔧 v0.2 工作量: 新写 `xgboost_model.py` 实现 `StrategyModule` Protocol + 训练流水线 + registry 加新 module 即可. **真正的"换实现"场景**, UI/接口都不动.

### Phase v0.5 (3-9 个月 — 一行概要)

- **Pre-mortem + post-mortem 双侧深化** [难度 M, 重要度 H] — 对应解决: L2 §4 风险 #R-v0.5-1 (单条决策档案不会自动产生模式洞察) — 决策档案的 pre/post 双侧从"基础字段"升到"提示性 pre-mortem 引导 + post-mortem 趋势聚合"。[v0.2 ship 后细化]
- **多市场 cross-signal (美/港/A 关联)** [难度 H, 重要度 M] — 对应解决: L2 §4 风险 #R-v0.5-2 (单市场视角错过关联机会) — cross-market 关联逻辑 (例如半导体链)。[v0.2 ship 后细化]
- **事件日历主动推送** [难度 M, 重要度 H] — 对应解决: L2 §4 风险 #R-v0.5-3 (事件型决策来不及反应) — Candidate C 形态在 B 上叠加为子模块。[v0.2 ship 后细化]

### Phase v1.0 (9-18 个月 — 一行概要)

- **私有模型 v2+ (backtest + 实盘对比 + 主动挑战过拟合)** [难度 H, 重要度 H] — 对应解决: L2 §4 风险 #R-v1.0-1 (模型过拟合 / 训练集污染). [远期]
- **配偶可见度模块** [难度 ~~L~~ M (修订, v0.1 未留 visibility/share 字段, 需扩 schema), 重要度 M] — 对应解决: L2 §4 风险 #R-v1.0-2 (家庭决策可见度 / 共识缺口). 决策档案天然 review-friendly (周/月 review 输出可直接共享), 但 v0.1 未实装 partner-readable 模式, v1.0 启动需加 visibility 字段 + share token 流程. [远期]
- **模型 tutor 升级 (基于 6 个月档案数据指出"你在 X 情境倾向 Y 错误")** [难度 M, 重要度 H] — 对应解决: L2 §4 风险 #R-v1.0-3 (个人偏差识别只能靠自省). **B 的天然延续**: 决策档案积累就是 tutor 的训练数据. [远期]

### Phase v1.5+ (长期, 不急 — 一行概要)

- **半自动化执行 (一键确认 + human 必拍板)** [难度 H, 重要度 L] — 对应解决: L2 §4 风险 #R-v1.5-1 (录入摩擦累积). 红线 #1 永远不破 (不是自动下单, 只是 "一键填表"). [远期]
- **Paper trading sandbox** [难度 M, 重要度 M] — 对应解决: L2 §4 风险 #R-v1.5-2 (新策略验证缺乏低成本通道). [远期]

## 7. Success — observable outcomes

> 时间锚点: v0.1 ship 于 **2026-04-27**. 下列 outcome 中:
> - 标 ✅ 已达成 = ship 时已完成且可验证
> - 标 ⏳ 进行中 = 需要 ship 后 N 周观察 (基准 = ship date)
> - 标 (待复盘) = 需要等到 v0.1.1 hotfix 完成后回填实际数据

- **O1**: 5-6 周交付 v0.1 — ✅ **已达成** (ship 2026-04-27, 见 `docs/v0.1-ship-summary.md`)
- **O2**: ship 后 8 周内**决策档案 ≥ 15 条** (calibration engine 在用的最低门槛) — ⏳ 进行中, 截止 2026-06-22
- **O3**: ship 后 8 周内**≥ 3 次 "agent 阻止冲动动作" 的记录** (calibration engine 起作用的 proxy) — ⏳ 进行中
- **O4**: ship 后 12 周内**能复述 ≥ 7 条金融概念** (学习证据, 防"学习假装") — ⏳ 进行中, 但 v0.1 wiki 自查机制未实装 (见 §6.v0.2.1), v0.2 才能真正度量
- **O5**: **单次决策录入 wall-clock < 30 秒** (search 验证的硬门槛 — 超过就弃用) — ✅ **已通过** spec.md C11 + SLA.md §1.4 + E2E timing test (5/5 手动压测通过, 见 `docs/v0.1-ship-summary.md` §3 O5)
- **O6**: 首周 onboarding ≤ 15 分钟完成 (74% onboarding rule, scope-reality 数据) — ⏳ (待复盘 — ship 后 1 周自评)
- **O7**: 维护时间 ≤ 3 小时/周 (intake 红线硬约束) — ⏳ 进行中, 取决于 v0.1.1 hotfix 收尾节奏
- **O8 (软)**: 同样不要求已达到 2-5% alpha, 但要求 "机制起作用的 proxy 可观察" — ⏳ 8 周后回看 O3

## 8. Real-world constraints

| # | Constraint | Source |
|---|------------|--------|
| C1 | 3-6 周交付 v0.1 (45-180 小时开发预算) | L3R0 intake Block 1 (Q1, Q2) |
| C2 | 平台 = Telegram bot + 本地 Web UI (localhost), 两者都要 | L3R0 intake hard constraint #6 |
| C3 | 自用单人, 不商业化 | L3R0 intake Block 3 |
| C4 | 维护时间 ≤ 3 小时/周 (稳定期) | L3R0 intake red line #5 |
| C5 | 咨询师内容 = 微信小程序多模态 (视频/音频/PDF/图文), v0.1 只解析 PDF/文本 + 留多模态接口 | L3R0 intake Block 10 + 🧭 原则 #3 |
| C6 | 策略类模块 v0.1 只做"清晰接口 + 占位实现" | L3R0 intake 🧭 原则 (绑定) |
| C7 | 投资准确度 / 研究 rigor 优先于其它 tradeoff | L3R0 intake hard constraint #7 |
| C8 | 咨询师内容 pipeline 必须包含 (不能砍) | L3R0 intake hard constraint #8 |

## 9. UX principles (tradeoff stances)

- **可复盘性 > 即时爽感** — 档案录入即使比"没档案"慢 10 秒, 也要保留, 因为可复盘性是核心价值。
- **把"不动"当一等公民** (红线 #10 的产品体现) — UI / review 不能让"不动"显得像"无操作"或"懒"。
- **解释质量 > 推送频率** (红线 #4) — 宁可少发一次, 也要保证每次都有白话解释。
- **Web UI 每个 tab 第一屏 ≤ 5 秒看完** — 避免"作业感", 这是 Decision Journal app 死亡复盘的关键教训。
- **档案录入 = 一键默认 + 可扩展** — 不是强制长表单; 默认值要尽量预填 (持仓、价格、当周咨询师观点都是 agent 自动填)。
- **Telegram = 提醒和入口, Web UI = 主场** — 不要在 Telegram 内做复杂表单。

## 10. Biggest product risk

**Upkeep 负担 — 录入 > 30 秒就死**。

scope-reality 证据硬:
- Decision Journal app 官方文档自述 "需要用户总是记得 + 定期 review 导致多人弃用"
- 研究显示 **74% 用户在差 onboarding 后放弃**
- 金融 app 30 天留存仅 **4.6%**

**v0.1 ship 时此风险的应对状态**:
- ✅ 30 秒 SLA 已工程级实装 (spec.md C11, SLA.md §1.4) + 5/5 手动压测通过
- ⏳ "为什么 + 回看 = 福利不是作业" 的 UX 体感, 只能通过 ship 后 6-8 周真实使用观察 (失败信号: 连续 2 周档案 < 2 条 = 红色告警 → 走 OP-1 mitigation 降级到 B-lite, 详见 SLA.md §3)

**第二 risk**: L2 verdict `unclear` 的 tension — "稳定赚钱"承诺没被证据支持, 自用工具 **没有外部 forcing function**, 一旦 upkeep 断掉, 就没有付费用户退订这种市场信号来逼迫改进。这个风险只能通过 **ship 后 8 周自我观察** 来管理 — 见 §7 O2/O3 是否达成。

## 11. Open questions

> 已 close 项 (移到本节末尾归档), 仍 open 项 (v0.2 启动需先回答):

### Open (v0.2 启动前需回答)

- ❓ **v0.1 的"成功机制"可观察证据 — 单人无法 A/B test** — spec.md C11 已把 O3 (≥ 3 次阻止冲动) 写为 acceptance, 但 ship 后 8 周回看时, human 是否真的接受 "≥ 3 次档案中 `would_have_acted_without_agent=yes` 但 final action ≠ acted" 算作"机制起作用"的证据? 还是需要更强 proxy (例如 outcome 字段事后回填)?  **决策时点: ship 后第 8 周回看时**.
- ❓ **笔记 wiki Concept schema 设计** — §6.v0.2.1 完成标准提到 "≥ 7 概念独立复述准确率 ≥ 70%", 但 v0.1 实际只有简单 `Note` 模型, 没有 Concept / first_seen_at / recall_score. v0.2 启动时 spec-writer 需先决定: (a) 在 Note 上加字段, 还是 (b) 新建 Concept 表 (Note 与 Concept 多对多). **决策时点: v0.2 spec.md kickoff**.
- ❓ **多模态接口拆分粒度** — §6.v0.2.2 实测显示 v0.1 的 `AdvisorParser` 是单一类, 没有 source/format/fetcher 三层. v0.2 启动时 spec-writer 需决定: (a) parser.py 大重构成三层 (b) 新写并行的 multimodal pipeline, 老 parser 保留作 PDF 路径 (c) 直接在 parser 加 if format=='audio' 分支. **决策时点: v0.2 spec.md kickoff**. 风险: (a) 工程量最大但最干净, (c) 最快但 v0.5+ 还会再重构.
- ❓ **配偶可见度 schema** — §6 v1.0 配偶可见度从"难度 L"修正到"难度 M" (因 visibility/share 字段未留). v1.0 启动时需决定: visibility 是 decision_archive 表加字段, 还是独立 share_link 表? **决策时点: v1.0 启动 (远期)**.

### Closed (v0.1 ship 时已解决)

- ✅ ~~"30 秒录入" 的 acceptance test 怎么做~~ — **已 close**: spec.md §3 C11 + SLA.md §1.4 + E2E timing test (`tests/e2e/test_decision_input_timing.py`) + 5 次手动压测,全程 wall-clock 度量 GET `/decisions/new` → POST `/decisions/{draft_id}/commit` 200 OK. ship summary §3 O5 记录 5/5 通过.

---

## PRD Source

This PRD was generated from L3 fork (v2.0 是按更新后的 fork.md 模板再生成, 协议拆 Scope OUT vs Phased roadmap). 内容派生自 approved L3 candidate. 完整背景:

- L3 menu: `discussion/004/L3/stage-L3-scope-004.md` (v2.0 同步重生成)
- L2 unpack: `discussion/004/L2/stage-L2-explore-004.md` (尤其 §4 Natural extensions, 是 §6 Phased roadmap 的权威来源)
- L1 inspire: `discussion/004/L1/stage-L1-inspire.md`
- FORK-ORIGIN.md: `discussion/004/004-pB/FORK-ORIGIN.md`
- v01 旧版 PRD: `discussion/004/004-pB/PRD_v01.md` (按旧协议 ship 的 v0.1, 已归档)
- v01 vs v2.0 差异对比: `discussion/004/004-pB/COMPARE-v01-vs-v02.md`

This PRD is the **source of truth** for L4 (spec-writer). Changes to PRD require explicit human approval — never auto-revised by L4 agents.
