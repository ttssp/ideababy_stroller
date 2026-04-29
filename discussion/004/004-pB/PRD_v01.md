# PRD · 004-pB · "决策账本"

**Version**: 1.0 (human-approved via fork)
**Created**: 2026-04-25T02:16:00Z
**Source**: `discussion/004/L3/stage-L3-scope-004.md` · Candidate B
**Approved by**: human moderator (2026-04-25)
**Status**: ready for L4 spec-writer

---

## 1. Problem / Context

这是一个**ML PhD 中年技术人自用的投资决策助手** (不商业化, 单用户). 用户已经付费订阅了一位哥大背景的华语投资顾问 (每周策略 + 盘前盘后), 能交易美股 / 港股 / A 股, 关注 30-50 只股票, 能承受 20% 回撤, 目标是为家庭财务负责, 不追求一夜暴富。

核心问题: **用户知道很多投资概念, 但在压力下不稳定, 临场乱动**。Barber-Odean 研究 (散户越频繁交易净回报越差) 直接说明, 这类用户最大的价值源不是"更聪明的 alpha", 是"**减少冲动乱动**"。

产品定位: **个人可进化的投资副驾驶 + 金融教练 + 私有策略编织层** —— 系统**首先是 calibration engine** (帮你判断什么时候不该动), **其次才是 action engine** (偶尔给出动作建议)。顺序反了会把"稳定赚钱"变"稳定放大错误"。

v0.1 的核心 loop: **每次 `动 / 不动 / 等待` 决策前, 都先过一道 "咨询师观点 × 占位模型信号 × agent 综合建议" 的三路冲突报告 + 写下 1 行理由 + 环境快照 → 落入决策档案 → 周末/月末回看**。这套流程的目标不是让你赚更多, 是让你成为一个**更稳的投资者**, 并在这个过程中逐步学会金融。

---

## 2. Users

**唯一用户 = 系统作者本人 (human moderator)**. 非商业化, 非 SaaS, 非多用户。

**用户画像** (L2 v2 §1 校正版):

- 35-50 岁, 中年, 技术背景 (ML 方向 CS PhD), 主业是 CS 不是金融
- **元能力超强但金融初级** — 知道价值投资、打新这类概念, 能看懂财报大结构, 但**不懂期权 / 大部分技术指标 / 大多数衍生品机制**
- 没时间系统学金融, **愿意在实操中学**
- 已付费订阅华语投顾 (每周策略 + 盘前盘后, 内容通过微信小程序发送, 含视频/音频/PDF/图文)
- 交易范围: 美股 + 港股 + A 股, 关注 30-50 只
- 风险容忍: 20% 回撤可接受, 每年数据预算 $500
- **心态**: 不追超额 alpha, 目标**跑赢标普 2-5% / 年** (来源: 更好的仓位管理 + 更少冲动错误, 不是 alpha 模型)
- **技术能力**: 能自己开发工具, 能插入私有 ML 模型 (未来, 不在 v0.1)
- **平台消费偏好**: Telegram (移动) + localhost Web UI (桌面, 研究向)

---

## 3. Core user stories

### S1. 冲动前 pre-commit (core loop)

作为用户, 当我想加仓 TSM 时, 我能打开 Web UI 一个 ≤ 30 秒表单, 看到 agent 拉出的三路冲突报告 (咨询师观点 A / 占位模型信号 B / agent 综合建议 C + 分歧根因), 选择 `按 / 不按 / 等待` + 写 1 行理由, 档案自动入库 + 环境快照 (价格、持仓、当周咨询师观点), **让我在每一次决策前都有一次结构化的自我对话机会**。

### S2. 周末回看 (calibration 第一层证据)

作为用户, 每周日晚上我能在 Web UI 打开"本周档案 review", 看到本周做了几次 action (按 agent / 按自己 / 不动), 各自回报; **特别看到 "不动" 是作为一等正式输出存在的, 不是失败状态**。

### S3. 三路冲突报告 UI (即使占位源弱, UI 骨架先立)

作为用户, 我能在 Web UI 打开冲突报告 tab, 看到三列表 (咨询师 / 占位"私有"模型 / agent 综合) + 白话根因; **当占位源没话说时, UI 显式显示 "暂无分歧" 不空屏尴尬**。Telegram 用叙事版 (移动端友好)。

### S4. 嵌入式金融教学 + 笔记 wiki (防学习假装)

作为用户, 当 agent 第一次解释某个金融术语 (例如 "右侧布局") 时, 解释自动存入个人金融笔记 wiki, **下次 agent 遇到相关话题不重复解释**。每 3 个月系统列出重点概念让我自查能否独立解释 — 若不能, **系统认为学习在失败**。

### S5. 校准证据的可观察证明 (8 周后)

作为用户, 8 周使用后, 我能从档案里筛出 **"3+ 次 如果没有 agent 我会操作但实际没动"** 的决策 — 这是 calibration engine 真正起作用的 proxy。如果 8 周后筛不出这个数字, **说明 core loop 没有形成**。

### S6. Devil's advocate 每次 action 前的一句反驳

作为用户, 每次我想 action (不管 agent 同意不同意), 系统都弹出一句 LLM 粗糙的反驳 (占位实现), **强制让我在 commit 前听一句反方**。这是 "calibration engine first" 的产品化体现, 也是 Vanguard Advisor Alpha 框架里 1.5%/年 行为教练价值的实现。

### S7. Telegram 入口 + 事件通知 (轻)

作为用户, 我在 Telegram 收到每周周报推送 (5 条消息内), 偶有 event 触发 (财报/FOMC/重大异动, 但节制), 能通过 Telegram 简单查询 (例如 "TSM 本周咨询师怎么看"), 但**所有重操作 (决策录入 / 冲突报告 / review) 都回到 Web UI**。

---

## 4. Scope IN (v0.1)

### 核心数据层
1. **咨询师周报 pipeline**: PDF/文本解析 (LLM prompt 占位实现)
2. **错位矩阵算法**: 咨询师强推 vs 你轻仓 / 咨询师谨慎 vs 你重仓 (规则 + 加权, 占位)
3. **关注股 (30-50 只) + 持仓快照录入**: JSON 或表单手动, 不接券商 API

### core loop
4. **决策档案系统** (core, v0.1 必含):
   - Schema: `{trade_id, ticker, action ∈ {buy/sell/hold/wait}, reason: str (≤ 1 行), pre_commit_at: ts, env_snapshot: {price, holdings, advisor_week_id, conflict_report_ref}, post_mortem: {executed_at, result_Npct, notes}}`
   - 录入 UX 门槛: **单次 < 30 秒** (默认填 + 快捷键 + 一键 commit)
5. **三路冲突报告 UI**:
   - Web: 三列表 + 白话根因 (默认空态: "暂无分歧", 不空屏)
   - Telegram: 叙事版 ("咨询师取 A, 模型取 B, 我得出 C, 分歧根因 X")
6. **Devil's advocate 占位** (每次 action 前 LLM 简单 prompt 出一句反驳)

### review & learning
7. **周度 review 生成器** (周日晚上自动出本周档案汇总)
8. **月度 review 生成器** (校准证据聚合)
9. **学习检查机制** (每 3 个月列重点概念自查)
10. **个人金融笔记 wiki** (自动去重, agent 不重复解释)

### 交付界面
11. **Telegram bot**:
    - 周报推送 (每周日晚)
    - Event 触发推送 (节制: 仅 human 持仓相关 event, 仅市场时间内)
    - 简单查询入口 ("XYZ 咨询师怎么看")
12. **本地 Web UI (localhost)**:
    - 多 tab: 矩阵 / 档案 / 笔记 / 冲突 / 周 review / 月 review
    - 无 auth (单用户 localhost)

### 架构关键
13. **`StrategyModule` IDL (核心接口)**:
    - `analyze(input, portfolio) → StrategySignal`
    - `conflict_resolve(signals) → ConflictReport`
    - `devil_advocate(decision, context) → Rebuttal`
    - v0.1 占位实现 (LLM prompt / 规则), v0.5+ 预留 `CustomStrategyModule` 扩展位
14. **模块完全解耦**: 咨询师 pipeline / 策略 / 冲突报告 / 档案 / review 各自独立可替换

---

## 5. Scope OUT (明确非目标)

### v0.5+ (下一版再说)
- ❌ 事件日历 / FOMC 预警 (可 v0.2+ 加, 或 fork C)
- ❌ 私有模型**真实**训练 (v0.1 只有占位接口)
- ❌ 多市场 cross-signal (v1.0+)
- ❌ 音频 / 视频解析 (v0.2+, 接口占位)
- ❌ 自动抓取 (v0.2+, v0.1 可接受 human 粘贴或半自动 Proxyman fetch)

### v1.0+
- ❌ 配偶可见度模块
- ❌ 回测环境

### v1.5+
- ❌ 半自动执行 (永远红线上限)

### 永远不做 (红线级别)
- ❌ **自动下单** (红线 #1, 永远保留 human 最终决策权)
- ❌ **期权 / 加密 / 高杠杆 / 日内交易** (红线 #2)
- ❌ **商业化 / 付费层 / 多用户** (这是私用项目, 不转化)
- ❌ **广谱 research terminal 功能** (是 Candidate A 的 feature, 不在 B 的主场 — 信息壳赛道饱和)

---

## 6. Success — observable outcomes

### O1. 交付 (5-6 周内)
v0.1 在 **5-6 周内**交付, 开发总工时 **100-160 小时** (15-30 小时/周 × 5-6 周)。

### O2. 决策档案积累 (8 周后)
8 周使用后决策档案 **≥ 15 条**。

### O3. 校准证据 (8 周后)
档案中能筛出 **≥ 3 次 "如果没有 agent 我会操作但实际没动"** 的记录 → calibration engine 真正起作用的 proxy。

### O4. 学习证据 (8 周后)
能复述 **≥ 7 条**金融概念的白话含义。

### O5. UX 硬门槛 (每次)
**单次决策录入 < 30 秒**. 违反即系统失败 (search 证据: > 20 分钟一周弃用, > 30 秒在自用场景会退化为日志)。

### O6. Onboarding (首次)
首周 onboarding **≤ 15 分钟**完成 (74% rule: 差 onboarding 放弃率)。

### O7. 维护负担 (稳定期)
v0.1 stable 后, **每周维护时间 ≤ 3 小时** (红线硬约束)。

### O8. 通知节制
Telegram 通知严格维持 **每周 1 次 + event 触发** 上限, 不变"看盘焦虑机"。

### O9. 2-5% alpha (12 个月)
**v0.1 不要求已达到**; v0.1 要求**机制起作用的 proxy 可观察** (O3 + O4). Alpha 目标是 12+ 个月可能达成, 通过 "更少乱动 + 更好仓位管理", 不通过 alpha 模型。

### O10. 失败告警
连续 2 周决策档案 < 2 条 = **红色告警**, 立即降级 UX 摩擦或改走 "B-lite" (砍冲突报告 + 月度 review)。

---

## 7. Real-world constraints (intake hard constraints)

| # | Constraint | Source |
|---|------------|--------|
| C1 | v0.1 在 3-6 周内交付, 预算 45-180 开发小时 | L3R0 intake Q1 + Q2 |
| C2 | 平台 = Telegram bot + 本地 Web UI (localhost) | L3R0 intake Q8 |
| C3 | Balanced core loop (calibration + action ≈ 1:1), 阈值属"策略类占位" | L3R0 intake Q3 |
| C4 | 温和 alpha 目标: 跑赢标普 2-5%/年 (12+ 个月观察, 非 v0.1 要求) | L3R0 intake Q5 |
| C5 | 显式三路冲突报告必含 UI, 无默认优先级 | L3R0 intake Q6 + GPT L3R1 红线 |
| C6 | 主动推送频率 = 每周 1 次 + event 触发, 不做日晨报 | L3R0 intake Q7 |
| C7 | 研究 rigor 优先于上线速度 / UX polish / 技术简单度 | L3R0 intake Q9 |
| C8 | 咨询师 pipeline 必含 (微信小程序多模态, v0.1 只做 PDF/文本) | L3R0 intake Q11 |
| C9 | 🧭 策略类模块 = 接口 + 占位实现, v0.1 不在策略准度上差异化, 完全解耦 | L3R0 intake 🧭 原则 |
| C10 | 单用户私用, 非商业化, 无 auth, localhost | L2 moderator-notes |

---

## 8. Red lines (all must be honored in v0.1)

### L2R3 原 8 条 (继承)
R1. **不自动下单** (永远保留 human 最终决策权)
R2. **不做期权 / 加密 / 高杠杆 / 日内交易**
R3. **每次建议必有白话解释** (不许 "信号黑箱")
R4. **不做日推送焦虑机** (通知节制 = 每周 + event)
R5. **工具维护时间 ≤ 3 小时/周** (稳定期)
R6. Agent **不许诱导高频交易** (Barber-Odean 铁律)
R7. **防"学习假装"** (3 个月自查, 说不清 = 失败信号)
R8. **不路径依赖单一咨询师** (架构预留多源, 即使 v0.1 只有一个)

### L3 新增
R9. **策略类模块完全解耦** (🧭 原则, 不许写长函数耦合)

### GPT L3R1 补充
R10. 三路冲突报告**显式**, **不偷偷给默认优先级**
R11. **"不动 / 等待"是一等正式输出**, 不是失败状态

---

## 9. UX principles (tradeoff stances)

1. **可复盘性 > 即时爽感**
2. **把"不动"当一等公民** (R11 的产品体现)
3. **解释质量 > 推送频率**
4. **Web UI 每个 tab 第一屏 ≤ 5 秒看完** (避免"作业感")
5. **档案录入**: 一键默认 + 可扩展, 不是强制长表单
6. **研究 rigor > UI polish** (C7)
7. **Telegram 极简**: 通知 + 简单查询 + event, 不承担重操作

---

## 10. Biggest product risks

### Risk #1 (最硬): Upkeep 负担 — 录入 > 30 秒即死

**证据**:
- Decision Journal app 官方文档: "需要用户总是记得 + 定期 review 导致多人弃用"
- 74% 用户在差 onboarding 后放弃
- 金融 app 30 天留存仅 4.6% (其它 vertical 多高得多)

**Mitigation**:
- O5 硬门槛 (单次 < 30 秒)
- O6 onboarding ≤ 15 分钟
- O10 红色告警监控 (连续 2 周档案 < 2 条立即降级)
- UX 迭代预留时间 (时间预算 M 置信度反映了这个)

### Risk #2: L2 `unclear` verdict 的 tension

**"稳定赚钱"承诺没被 L2 证据支持, 自用工具无外部 forcing function**. 一旦 upkeep 断, 没有付费用户退订信号来逼改进。

**Mitigation**:
- Success 标准明确分层 (O2-O4 为 v0.1 可观察, O9 alpha 目标移到 12 个月)
- 心理预期从"保证赚钱"调整为"成为更稳的投资者" (L2R3 §6 Q2 的动机问题)
- 8 周自我观察作为 go/no-go 决策点

### Risk #3: 工具吞噬主业 (L2R3 §5 红线)

若每周维护 > 3 小时或开发阶段溢出 180 小时, 系统对 user 整体生活是**负贡献** (主业 = CS 不是金融工具开发)。

**Mitigation**:
- C1 时间预算硬约束
- R5 稳定期维护红线
- 时间超限 → 必须 scope down (砍某子功能进 v0.2)

### Risk #4: "信息壳 vs 承诺壳" 竞争误区

若 v0.1 执行中滑成 "更好的咨询师摘要工具" (Candidate A 的形态), 就进了饱和赛道 (Fiscal.ai / Koyfin / Aiera / Bridgewise / 雪球付费). B 的核心差异是 "**承诺壳 = 把你自己的决定当核心对象**", 不是"更好的外部信息摘要"。

**Mitigation**:
- Scope OUT 明确写出 "广谱 research terminal 功能" 不在 B 主场
- 核心 UI 主场应是 "决策档案", 不是 "错位矩阵" (矩阵是辅助入口, 不是目的)

---

## 11. Open questions for L4 / Operator

### 仍需 human 回答 (不阻塞 L4 启动, 但 spec/implementation 过程会涉及)

1. **"稳定赚钱"精确定义的 benchmark 与时间尺度** (目标跑赢标普 2-5%, 但**多少年算"稳定"**? 6 个月样本不够, 12 个月? 3 年?)
2. **动机二选一** (L2R3 §6 Q2): "成为会投资的人" vs "摆脱'不知道该怎么办'的焦虑"? — 导向不同系统 tone / 建议频率 / 教学深度
3. **情绪承受预案** (L2R3 §6 Q1): 连续两次建议都亏钱, 能冷静区分"噪声 / 系统缺陷 / 自己没按规则"吗? spec 中是否需要明确"两周冷静期"机制?
4. **配偶可见度接口预留** (L3 honesty check): v0.1 是在接口层预留, 还是 v1.0 再说? 倾向 "v0.1 接口预留 + v1.0 实现", 让 `ReviewGenerator` 支持多受众参数。

### L4 技术边界问题 (由 spec-writer 展开)

- 咨询师 pipeline 具体路径 (human 粘贴 vs watched folder + Proxyman fetch) 由 spec-writer 选一条
- 决策档案 persistence (SQLite vs JSON file vs DuckDB) 由 spec-writer 依简单度优先决
- LLM 调用策略 (Claude API? local? 缓存?) 由 spec-writer 决定 (预算 $500/年数据 + 合理 LLM 开销)
- 错位矩阵可视化 (matplotlib png vs plotly vs 简单 HTML table) 由 spec-writer 依 5 秒看完原则决

---

## PRD Source

本 PRD 由 L3 fork 自动生成, 内容提取自 approved L3 Candidate B。完整上下文 (为什么选 B, scope-reality verdict, comparison matrix, 双模型 axis):

- **L3 menu**: `discussion/004/L3/stage-L3-scope-004.md` (Candidate B section line 192-264)
- **L2 unpack v2**: `discussion/004/L2/stage-L2-explore-004.md` (核心洞见 calibration-first)
- **L2 moderator-notes**: `discussion/004/L2/moderator-notes.md` (越过 alpha 红线的授权)
- **L3 intake**: `discussion/004/L3/L3R0-intake.md` (8 hard constraints + 🧭 原则)
- **FORK-ORIGIN**: `discussion/004/004-pB/FORK-ORIGIN.md` (本 fork 的 lineage)
- **HANDOFF-L4**: `discussion/004/HANDOFF-L4.md` (新 session 进入 L4 的压缩 brief)

**本 PRD 是 L4 spec-writer 的 source of truth**. 任何对 PRD 的更改需要 human 明确批准 — L4 agents **不得自动修改**。
