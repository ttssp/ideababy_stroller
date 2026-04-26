# HANDOFF-L4 · idea 004 · Candidate B "决策账本" (承诺壳)

**Handoff 时间**: 2026-04-24T14:10:00Z
**From**: 当前 session (完成 L1 → L2 → L3, 产出 stage-L3-scope-004.md 菜单)
**To**: 新 session (将在 clear 后跑 `/plan-start 004-pB`)
**Handoff 目的**: 压缩关键上下文, 让新 session 即使没有历史对话, 也能立即对齐并进入 L4 spec-writer 阶段。

---

## 一句话: 这是什么 idea

**一个 ML PhD 中年技术人给自己私人打造的 "投资决策账本"** (不商业化, 自用). Web-first + log-heavy, 核心价值是**减少冲动乱动**, 承诺"跑赢标普 2-5%/年"靠的不是 alpha 模型, 是**每次 action 前 pre-commit + 事后复盘**的 calibration engine。

## 一句话: 为什么选 Candidate B

**GPT L3R2 scope-reality search 证明: 信息壳市场已饱和 (Fiscal.ai/Koyfin/Aiera/Bridgewise/雪球付费), 承诺壳 (把"你自己的决定"当核心对象的 personal shell) 是 uniquely 空白的 slice**。A (研究收件箱) 饱和赛道, C (事件卡台) 样本稀疏风险, **B 独特无先例 + 直接命中 L2 v2 的 calibration-engine-first 洞见 + 直接回应 Barber-Odean 铁律 (散户越频交越差)**。

---

## Golden path (给新 session 的)

```
# 在 worktree root (/Users/admin/codes/ideababy_stroller/.claude/worktrees/idea004)

1. /fork 004 from-L3 candidate-B as 004-pB
   → 创建 discussion/004/004-pB/ 分支, PRD 作为 branch 起点

2. /plan-start 004-pB
   → spec-writer 读 PRD.md → 产出 spec.md / architecture.md / tech-stack.md 等
   → task-decomposer 产出 DAG + tasks/T001-TNNN.md
   → Codex adversarial 4-round review loop
   → 输出 build-ready spec package
```

---

## 本 idea 的关键 framing (**绝不丢**)

### 1. 不商业化 / 单用户私用

- **唯一用户 = human 自己**. 不做 SaaS, 不做 B2C/B2B2C, 不卖钱。
- L4 spec 时可以直接**用贵模型、大 context、localhost、无 auth、极 geek UX**。
- **没有"付费用户流失"概念**, 但 **"human 自己 6-8 周后停用"是最大失败模式** (L2 的 personal informatics research 证据)。

### 2. 🧭 Scope-shaping 铁律 (人类在 L3R0 intake 明确指定, 具有绑定力)

**v0.1 = pipeline + shell. 策略类模块 = 清晰接口 + 最简占位**。v0.1 **不**追求:
- 动手阈值调准
- 私有 ML 模型训练好
- 咨询师解析多模态深度

v0.1 **必须有的**:
- ✅ 清晰的接口契约 (IDL-level) 让策略模块后期独立迭代
- ✅ 最简占位实现 (规则 / 手工触发 / LLM 粗糙 prompt)
- ✅ 模块**完全解耦**, 单独可替换

**L4 spec-writer 请严格遵守**: 任何 "为了 v0.1 赶时间把 A/B/C 写成长函数" 的建议都要拒绝, 要求拆接口。

### 3. Core promise (L2 moderator-notes 校正后的定位)

- **不是** "投资纪律层 (商业, 不承诺 alpha)" — 这是旧 framing, **已作废**
- **是** "**个人可进化的投资副驾驶 + 金融教练 + 私有策略编织层**" (自用, **越过 alpha 红线**, 愿意给方向建议 + 仓位建议)
- 核心洞见 (L2R3-GPT): **系统首先是 calibration engine, 其次才是 action engine**. 顺序反了会把"稳定赚钱"变"稳定放大错误"。

### 4. 三路冲突报告 (intake hard constraint #4)

**v0.1 必须包含** "咨询师观点 / 占位模型信号 / agent 综合建议" 三路 conflict 报告 UI。默认无优先级 (human 在 intake Q6 选了 "Agent 泳道汇合 · 显式冲突报告, 无默认优先级")。

**GPT L3R1 补的 2 条硬红线** (spec 必含):
- 任何建议必须显式展示三路, 不能偷偷给默认优先级
- "不动 / 等待更多确认" 必须是**一等正式输出**, 不是失败状态

### 5. Cadence (intake hard constraint #5)

- **每周 1 次周报 + event 触发**, 不做日晨报
- 防"看盘焦虑机" 红线 (L2R3 #4)
- Telegram 通知必须有 muting 窗口 (event 仅市场时间内推)

### 6. 双平台定位 (intake hard constraint #6)

- **Telegram**: 承担通知 + 简单询问 + event 推送 (移动端)
- **本地 Web UI** (localhost): 承担决策档案 + 冲突报告 + 矩阵图 + 笔记 wiki + review (桌面主场)
- 两者都要, 但 **Web 是 B 的主场** (log-heavy 操作在这)

### 7. 咨询师数据源 (intake freeform - 关键实现约束)

- 来源: **微信小程序** (多模态: 视频/音频/PDF/图文)
- 现状: human 已用 **Proxyman 手动监听 + fetch**, 有 URL pattern 可复用
- **v0.1 只做 PDF/文本解析**, 视频/音频走接口占位 (v0.2+)
- **v0.1 抓取自动化**: 可以接受 "human 粘贴 PDF" 或 "半自动 pipeline (human 触发 Proxyman fetch → 入 watched folder → agent 解析)"。spec-writer 可选更方便的路径。

---

## Candidate B PRD 全文 (权威 PRD 从这里读, spec-writer 按此展开)

权威 PRD 位于 `discussion/004/L3/stage-L3-scope-004.md` 的 `## Candidate B · "决策账本"` section (约 line 192-264)。

**提炼** (spec-writer 的 source of truth):

### v0.1 Essence
Web-first + log-heavy 决策账本台。周报和 event 卡是入口, v0.1 核心是**每次 `动 / 不动 / 等待` 沉淀成"决策档案"**:
- 咨询师观点 (本周当前)
- 占位模型信号 (简单规则或 LLM 无 context 独立判断, 作为"私有模型" v0.1 占位)
- agent 综合建议
- 三路冲突报告 + 白话根因
- human 最终决定 (按/不按/等待) + 1 行理由
- 环境快照 (价格、持仓、当周咨询师观点)
- 事后回看字段 (trade 执行后 N 天回填)

### Scope IN (v0.1)
1. **咨询师 pipeline**: PDF/文本解析 (LLM prompt 占位)
2. **错位矩阵**: 咨询师强推 vs 你轻仓 / 咨询师谨慎 vs 你重仓
3. **关注股 (30-50) + 持仓快照**: JSON 或表单手动录入 (不接券商)
4. **决策档案系统**: 表单 + 环境快照 + 事后字段
5. **三路冲突报告 UI**: Web 三列表 (咨询师/占位模型/agent) + Telegram 叙事版
6. **Devil's advocate 占位**: LLM 简单 prompt, 每次 action 前出一句反驳
7. **周度 + 月度 review 生成器**
8. **学习检查机制**: 每 3 个月自查能否解释重点概念
9. **个人金融笔记 wiki**: 自动去重 (agent 不重复解释)
10. **Telegram bot**: 周报推送 + 事件触发 + 简单查询入口
11. **本地 Web UI** (localhost): 多 tab (矩阵 / 档案 / 笔记 / 冲突 / 月回顾)
12. **策略模块占位接口** (`StrategyModule` IDL): 动手阈值 / 私有模型 / 多模态解析深度 都是这套接口的占位实现

### Scope OUT (v0.1 明确 NOT)
- ❌ 事件日历 / FOMC 预警 (可 v0.2+ 加, 或 fork C)
- ❌ 私有模型真实训练 (接口占位)
- ❌ 多市场 cross-signal (v1.0)
- ❌ 半自动化执行 (v1.5, 红线上限)
- ❌ 配偶视角 (v1.0+)
- ❌ 音频 / 视频解析 (v0.2+)
- ❌ 广谱 research terminal 功能 (A 的 feature, 不是 B 的主场)
- ❌ 自动下单 (永远不做, 红线 #1)
- ❌ 期权 / 加密 / 高杠杆 / 日内 (永远不做, 红线 #2)
- ❌ 商业化 / 付费层 / 多用户 (红线, 永远不做)

### Success criteria (8 周内可观察)
- ✅ 5-6 周内交付 v0.1
- ✅ 8 周使用后决策档案 ≥ 15 条
- ✅ ≥ 3 次 "agent 阻止冲动动作" 的记录 (校准证据)
- ✅ 能复述 ≥ 7 条金融概念 (学习证据)
- ✅ **单次决策录入 < 30 秒** (**硬门槛, 破则死**)
- ✅ 首周 onboarding ≤ 15 分钟完成 (74% rule)
- ✅ 维护时间 ≤ 3 小时/周
- ⚠️ **不要求** 已达到 2-5% alpha, 要求 "机制起作用的 proxy 可观察"

### 时间预算
- **5-6 周 × 15-30 小时/周 = 100-160 开发小时**
- 置信度 M

### Biggest risk
**Upkeep 负担 — 录入 > 30 秒就死**. 
- Decision Journal app 官方文档: "需要用户总是记得 + 定期 review 导致多人弃用"
- 研究: 74% 用户在差 onboarding 后放弃; 金融 app 30 天留存仅 **4.6%**
- **监控信号**: 连续 2 周档案 < 2 条 = 红色告警, 需立即降级 UX 摩擦或改 B-lite 路径

**第二 risk**: L2 verdict `unclear` 的 tension — "稳定赚钱"承诺没被证据支持, 自用无外部 forcing function, 一旦 upkeep 断没人逼改进。只能通过 **8 周自我观察** 来管理。

### UX 优先级
1. 可复盘性 > 即时爽感
2. **把"不动"当一等公民** (红线 #10 的产品体现)
3. 解释质量 > 推送频率
4. Web UI 每个 tab 第一屏 ≤ 5 秒看完 (避免"作业感")
5. 档案录入 **一键默认 + 可扩展**, 不是强制长表单
6. 研究 rigor > UI polish (intake Q9)

---

## 所有红线 (红线模式, L4 spec 绝不违反)

### L2R3 原 8 条 (继承)

1. 不自动下单 (人保留最终决策权)
2. 不做期权 / 加密 / 高杠杆 / 日内
3. 每次建议必有白话解释 (不许"信号黑箱")
4. 不做日推送焦虑机
5. 工具维护 ≤ 3 小时/周 (稳定期)
6. Agent **不许诱导高频交易** (Barber-Odean 铁律)
7. 防"学习假装发生" (3 个月后仍说不清关键指标 = 失败信号)
8. 不单一咨询师路径依赖

### L3R0 intake 新增

9. 策略模块**必须接口化 + 占位实现**, 不许写长函数 (🧭 原则)

### GPT L3R1 补充的 2 条

10. 任何建议显式展示三路 (咨询师 / 占位模型 / agent), **不偷偷给默认优先级**
11. **"不动 / 等待" 是一等正式输出**, 不是失败状态

---

## 4 个 human 仍然需要自己回答的问题 (不影响 L4 启动, 但 spec/implementation 过程中需要)

这些**不是 blocker** (Candidate B 已经足够具体启动), 但 spec-writer 或未来的 moderator note 可能需要 human 补充:

1. "稳定赚钱"精确定义里的 **benchmark 与时间尺度** (目标是跑赢标普 2-5%/年, 但**多少年是"稳定"?** 6 个月样本不够)
2. GPT L2R3 问题: **动机是"成为会投资的人" vs "摆脱'不知道该怎么办'的焦虑"?** (导向不同系统形态)
3. GPT L2R3 问题: **连续两次建议都亏钱, 你能冷静区分"噪声 / 系统缺陷 / 自己没按规则"吗?** (情绪承受预案)
4. L3 Honesty check: **Candidate B 的"配偶可见度"是否在 v0.1 就预留接口, 还是 v1.0 再说?** (L3 synthesizer 将其标为 "v1.0+", 但接口层可以在 v0.1 就想)

---

## Spec-writer / task-decomposer 的关键提示

### spec-writer 应重点展开

1. **`StrategyModule` IDL (核心接口)** — 这是整个 v0.1 的架构枢纽。应包含:
   - `analyze(input: AdvisorWeeklyReport, portfolio: Portfolio) → StrategySignal` (占位: LLM prompt)
   - `conflict_resolve(signals: [StrategySignal]) → ConflictReport` (占位: 规则合并)
   - `devil_advocate(decision: Decision, context: EnvSnapshot) → Rebuttal` (占位: LLM prompt)
   - 预留**私有 ML 模型**的 v0.5 扩展位 (`CustomStrategyModule(StrategyModule)`)

2. **决策档案 Schema** — 字段最重要。至少包含:
   - `{trade_id, ticker, action: enum[buy/sell/hold/wait], reason: str (≤ 1 行), pre_commit_at: ts, env_snapshot: {price, holdings, advisor_week_id}, conflict_report_ref: uuid, post_mortem: {executed_at, result_Npct, retrospective_notes}}`
   - 录入 < 30 秒的 **UX 实现路径建议** (默认填 + 快捷键 + 一键 commit)

3. **咨询师 pipeline** — v0.1 可以选 "human 粘贴" 最轻, 或 "watched folder + Proxyman fetch" 中等。让 spec-writer 选一个具体路径, 但接口层要支持 v0.2+ 升级到自动抓取。

4. **Telegram vs Web UI 分工** — 清晰:
   - Telegram: 通知 / 简单查询 / event 推送
   - Web: 档案录入 / 冲突报告 / 研究视图 / review
   - 别让 Telegram 承担重操作

5. **冲突报告默认空态** — 占位模型经常没意见时, UI 显式说 "暂无分歧", 不能空屏尴尬 (L3R2 Opus 明确提到)

### task-decomposer 的优先级建议

- **第一层 T001-T005 推荐**: 数据模型 (持仓 + 关注股 + 咨询师报告 + 决策档案 schema) → 基础 persistence (SQLite 或 JSON 文件够) → 最简 pipeline (PDF 粘贴 → LLM parse → 结构化) → 最简 Web UI (一个 decision-log tab) → Telegram 最简 echo bot
- **第二层 T006-T010**: 错位矩阵算法 + StrategyModule IDL + 占位实现 + 冲突报告 UI + 笔记 wiki
- **第三层 T011-T015**: Devil's advocate 占位 + 周度 review 生成 + 月度 review + 学习检查 + onboarding 流程
- DAG 应该让 T001-T005 可并行, 其它层可部分并行

### Codex adversarial review 关注重点

审查 Codex 应该重点 challenge:
1. 录入 UX 真的能 < 30 秒吗? (搜索证据: > 20 分钟 = 一周弃用, 我们目标 < 30 秒才能 8 周存活)
2. 三路冲突报告真的不偷偷默认优先级吗? (红线 #10)
3. "不动"真的是一等输出吗 UI 上? (红线 #11)
4. 策略模块真的完全解耦吗? (🧭 原则)
5. Telegram 通知节制吗? 不会变焦虑机吗? (红线 #4)
6. Biggest risk "upkeep 负担" 的监控信号 ("连续 2 周档案 < 2 条") 真的有实现吗?

---

## Source of truth 文件

重要文件新 session 应该读的顺序:

1. **本 handoff** (你手里这份) — 压缩上下文
2. `discussion/004/L3/stage-L3-scope-004.md` — 完整 PRD 菜单 (Candidate B section)
3. `discussion/004/L3/L3R0-intake.md` — hard constraints 全集
4. `discussion/004/L2/moderator-notes.md` — L2 framing 校正 (越过 alpha 红线的授权)
5. `discussion/004/L2/stage-L2-explore-004.md` — L2 v2 report (深度 idea 理解)
6. `proposals/proposals.md` entry 004 — 最原始 proposal

**不需要读** (除非有特定疑问):
- L1 所有文件 (菜单被 skip 了, 保留给未来)
- L2R1 / L2R2 (旧 framing, 已被 moderator-notes 作废)
- L3R1 / L3R2 (已被 synthesizer 汇总进 stage-L3-scope)

---

## 一句话给新 session 的 orientation

> "你正在给一个 ML PhD 中年技术人自用的**投资决策账本**写 spec。核心是 Web-first + log-heavy, 服务于减少冲动交易 (Barber-Odean 铁律), core loop 是**每次 action 前先过一道三路冲突报告 + 1 行理由 + 环境快照的档案录入**, 录入必须 < 30 秒否则必死。策略模块全占位, 完全解耦, 后续独立打磨。5-6 周交付 v0.1, 45-180 小时预算。权威 PRD 在 `discussion/004/L3/stage-L3-scope-004.md` 的 Candidate B section."

Good luck.
