# Spec — 004-pB · 决策账本 (承诺壳 · calibration engine first)

**Version**: 0.3.1
**Created**: 2026-04-25T15:00:00+08:00
**Updated**: 2026-04-26T20:30:00+08:00 (R4 surgical patch · Codex R3 BLOCK 修订, package-level 收口)
**Source PRD**: `discussion/004/004-pB/PRD.md` (v1.0, human-approved 2026-04-25)
**Lineage**: 004 (root) → L3 Candidate B → fork `004-pB`
**Status**: ready for adversarial review R4

---

## Revision History

| Version | Date | 修订摘要 | 触发 |
|---------|------|---------|------|
| 0.1 | 2026-04-25T15:00 | 初稿 (6-element contract + 20 prior decisions + O1-O10 verification) | spec-from-conclusion 首次 |
| 0.2 | 2026-04-25T19:30 | **R2 修订, surgical**: B1/B2/B3 contract-level fix · H1-H5 high · M1-M5 medium/low. 改 §1 O5 度量口径 (commit 阶段 wall-clock); §4 D7 IDL 拆 (StrategyModule.analyze 唯一职责); §4 D13 录入 UX = draft → commit 双阶段; §4 D19 修正 LLM 调用时点; §4 新增 D21/D22/D23/D24 + 删 D18; §6 O5 verification 同步; §7 Glossary 修 B-lite 定义; §8 Q4/Q5 → RESOLVED, 新增 Q11; 与 PRD 无冲突 (PRD §S1/§S6 pre-commit framing 是修订动力) | Codex R1 BLOCK · 见 `.codex-outbox/20260425T030218-004-pB-L4-adversarial-r1.md` |
| **0.3** | 2026-04-26T19:00 | **R3 surgical revision (路径 A · 守 PRD 原口径)**: 回退 R2 暗中改的 PRD §S1 / §6 O5 度量口径. R3 修向: <br/>(1) §0 删除"硬门槛重新定义"段, 改回 PRD 原口径 (GET → commit 全程 < 30s) <br/>(2) §1 O5 / §3 C11 重写, 守 PRD 原意: **wall-clock < 30s 包含 draft 阶段 LLM 调用** <br/>(3) §4 D13 / D19 / D21 重写, 诚实承认 Rebuttal 不可缓存 (因输入依赖 draft 内容); 强制 Rebuttal LLM 用最快 prompt + Sonnet 4.6 + max_tokens ≤ 100 + ≤ 3s 上限 <br/>(4) §5 task pack 真砍到 ≤ 160h 边界 (T011/T015/T016/T018/T019/T021/T022 共砍 21h, 181h → 160h) <br/>(5) §6 O5 verification 度量改为全程 wall-clock (从 GET /decisions/new 到 POST commit 200 OK) <br/>(6) §7 Glossary "录入 < 30 秒" 统一为 GET → commit 全程口径 <br/>(7) §8 删除 R2 引入的 Q11 (cache miss 5-10s 例外, 与 PRD 原口径冲突) <br/>(8) 与 PRD 无冲突 (PRD §S1 一句话 framing 是修订动力, R3 守它) | Codex R2 BLOCK · 见 `.codex-outbox/20260425T042650-004-pB-L4-adversarial-r2.md` |
| **0.3.1** | 2026-04-26T20:30 | **R4 surgical patch · package-level 收口 (Codex R3 BLOCK 修订)**. 仅文字级澄清, 无 scope/outcome 变化. 改动: <br/>(1) §4 D16 改为"纯 HTML table" (R3 修订 T011 砍 CSS 着色, line 166) — close Codex R3 LOW finding #4 <br/>(2) §8 整段删除 R2 Q11 删除线小节 (line 312-319), Revision History v0.3 entry 已记 — close Codex R3 BLOCK B-R2-5 残留半套 <br/>**未触动**: PRD / 任何 task estimated_hours / risks.md / non-goals.md / dependency-graph.mmd | Codex R3 BLOCK · 见 `.codex-outbox/20260426T120622-004-pB-L4-adversarial-r3.md` |

**与 v0.2 兼容性**: R3 修订是**回退 R2 暗中越权改 PRD 度量口径**. PRD 不动. Tasks 中 T007/T008/T009/T010/T011/T013/T015/T016/T017/T018/T019/T020/T021/T022 都 R3 同步修订 (含估时砍). dependency-graph.mmd 反映 T015/T017 不再 block T020.

**与 v0.3 兼容性**: R4 patch 是 R3 落地动作的 package-level 收口, **不重启决策**. T020 banner 文案改 CLI/runbook (与 T022 R3 CLI-only 一致); architecture.md 全文清残留"≤10s" / "commit-only"字样; open-questions.md Q7 默认假设改为 (b) human 手编 (与 T019 一致); architecture.md §9 不变量 #15 新增 strict mode CI 默认.

---

## 0. 文档定位

本 spec 是 PRD 在工程层的**契约**。**PRD 是产品决策的唯一权威**, 任何与 PRD 冲突
的工程选择都必须升级为 §Open Questions, 不得擅改 PRD。

> **一句话**: 这是一个 ML PhD 中年技术人**自用**的投资**决策档案系统**, **首先是
> calibration engine (帮你判断什么时候不该动), 其次才是 action engine**。Web-first
> + log-heavy, 单用户 localhost, 5-6 周 / 100-160 小时交付。
>
> **核心 loop (pre-commit framing, PRD §S1 原意 · R3 守口径)**: 每次 `动 / 不动 /
> 等待` 想法 → **打开 draft 表单, 系统同步生成**三路冲突报告 (咨询师 / 占位模型 /
> agent 综合) **+ Devil's advocate 一句话** → human 看到三路 + 反方 → 选择 final
> action + 写 1 行理由 + 显式 yes/no `如果没看 agent 我会 X` + commit → 档案入库 →
> 周末/月末 review。
>
> **硬门槛 (PRD §S1 / §6 O5 原口径, R3 不改)**: **单次决策录入 wall-clock < 30 秒**
> (违反即系统失败) — 度量起点 = human 打开 `/decisions/new` (GET 200 OK), 度量终点 =
> commit 完成入档 (`POST /decisions/{draft_id}/commit` 200 OK), **全程 wall-clock 含
> draft 阶段 LLM 同步等待**. 系统达成此口径的工程路径见 §4 D13 / D21 (cache 预热 +
> Rebuttal fast-path); cache miss 时 draft > 5s 是系统失败信号, 走 OP-1 mitigation,
> 不允许 spec 自行宽容到 35-40s。

---

## 1. Outcomes (可观察、可度量、可测试)

每个 Outcome 编号 O1-O10, 一一对应 PRD §6 同名条目。所有 Outcome 在 §6 有对应
verification。

| # | Outcome | 度量口径 | 时点 |
|---|---------|---------|------|
| **O1** | v0.1 整体在 5-6 周内交付 (开发总工时 100-160 小时, 15-30 小时/周) | git log 首尾 commit 间隔 ≤ 6 周; 工时由 human 自报记录 | 交付日 |
| **O2** | 8 周稳定使用后, 决策档案条数 **≥ 15** | `SELECT COUNT(*) FROM decisions WHERE pre_commit_at >= ship_date AND status='committed'` | ship + 8 周 |
| **O3** | 决策档案中可筛出 **≥ 3 条** "如果没有 agent 我会操作但实际没动" 的记录 | 档案有显式字段 `would_have_acted_without_agent: bool` (commit 阶段强制 yes/no, 见 D13/M1); SQL count ≥ 3 | ship + 8 周 |
| **O4** | 学习检查能复述 **≥ 7 条**金融概念白话含义 (人工评分 ≥ 70%) | 季度自查表 (见 §6); human 自评 7/10 | ship + 12 周 |
| **O5** | **单次决策录入 wall-clock < 30 秒** (PRD §S1 / §6 O5 原口径, R3 守): 度量起点 = human 打开 `/decisions/new` (GET 200 OK), 度量终点 = commit 完成入档 (`POST /decisions/{draft_id}/commit` 200 OK). **全程 wall-clock < 30s 包含 draft 阶段 LLM 同步等待** (D13/D21 工程路径: cache 预热让 ConflictReport 命中常态 ≤ 1s, miss 上限 5s; Rebuttal fast-path ≤ 3s; 双调用并发 ≈ max(3s, 5s) = 5s, 留 25s 给 commit 阶段 form 操作). **violations 即系统失败** (cache miss 让 draft > 5s 也算违反, 走 OP-1 mitigation, 不允许 spec 自行宽容) | (a) 自动化 timing test (E2E + UX bench, T009): 度量 GET /decisions/new 到 POST commit 200 OK 全程 wall-clock < 30s; (b) 连续 5 次手动录入压测全部全程 < 30s, 写入 release_log.jsonl | 每次 release + ship 后 ad-hoc |
| **O6** | 首次 onboarding 在 **≤ 15 分钟**完成 (录入 30-50 关注股 + 持仓 + 1 份咨询师 PDF + 完成首次决策档案) | onboarding 流程内置计时, log 入库 | ship 后第一周 |
| **O7** | 稳定期(ship 后第 4 周起)每周维护时间 **≤ 3 小时** | human 自报每周维护工时 | ship + 4 周起持续 |
| **O8** | Telegram 主动推送严格遵守 **每周 1 次周报 + event 触发**上限, **per-market session window** (见 D24) | 监控统计 push 计数, 每周分组; per-market window 单测 | 持续 |
| **O9** | 12 个月 alpha 目标 (跑赢标普 2-5%/年) — **不在 v0.1 验证范围**, v0.1 仅要求 "机制起作用 proxy 可观察" (即 O3 + O4) | 不在 v0.1 contract; 仅作为长期 north star | 12+ 个月后 |
| **O10** | **失败告警机制存在并工作**: 连续 2 周决策档案 < 2 条 = 红色告警 (Telegram + Web banner); `pause_pipeline()` / `resume_pipeline()` hook 在 T010/T015 outputs 显式存在 (即使 v0.1 UI 暂不暴露 toggle) | 自动化测试可触发告警; 真实场景下 dry-run 一次确认告警出现; pause_pipeline hook 单测 | ship 当日 + 持续 |

---

## 2. Scope Boundaries

### 2.1 In scope for v0.1 (来自 PRD §4)

#### 核心数据层
- 咨询师周报 pipeline (PDF + 文本解析, LLM prompt 占位)
- 错位矩阵算法 (规则 + 加权, 占位)
- 关注股 (30-50) + 持仓快照录入 (JSON / 表单, 不接券商 API)

#### Core loop (pre-commit framing)
- **决策档案系统** (schema 详见 architecture.md, action ∈ {buy/sell/hold/wait}; status ∈ {draft/committed/abandoned})
- **三路冲突报告 UI** (Web 三列等宽 + 顺序 hash 随机化 + Telegram 叙事版) — **draft 阶段同步可见**
- **Devil's advocate 占位** (LLM prompt, 每次 action 前出一句反驳) — **draft 阶段同步可见**

#### Review & Learning
- 周度 review 生成器 (周日晚自动)
- 月度 review 生成器 (校准证据聚合)
- 学习检查机制 (每 3 个月)
- 个人金融笔记 wiki (自动去重)

#### 交付界面
- Telegram bot (周报 + event + 简单查询; per-market session window)
- 本地 Web UI (localhost, 多 tab, 无 auth)

#### 架构关键
- `StrategyModule` IDL — **唯一方法** `analyze() → StrategySignal` (R2 修订, B2/B3 解决)
- `ConflictReportAssembler` — **中立 domain service**, 不是任一 lane (R2 修订)
- `DevilAdvocateService` — 独立反驳服务, 不是 StrategyModule
- 模块完全解耦 (咨询师 pipeline / 策略 / 冲突报告 / 档案 / review 各自可独立替换)

#### Non-functional v0.1
- 失败告警监控 (O10)
- "不动 / 等待" 一等输出 (UI + schema 双层体现)
- `pause_pipeline()` / `resume_pipeline()` hook 在 T010/T015 outputs 必含 (R2 修订, H1)

### 2.2 Explicitly out of scope for v0.1 (来自 PRD §5)

详见 `non-goals.md`。摘要:

- **v0.5+**: 事件日历 / 私有模型真训练 / 多市场 cross-signal / 音频视频解析 / 自动抓取
- **v1.0+**: 配偶可见度 (R2 修订: D18 删除, partner audience 推后到 v1.0+) / 回测环境
- **v1.5+**: 半自动执行 (永远红线上限)
- **永远不做**: 自动下单 (R1) / 期权·加密·高杠杆·日内 (R2) / 商业化 / 广谱 research terminal

---

## 3. Constraints

| # | Constraint | Source | Rigidity |
|---|-----------|--------|----------|
| **C1** | v0.1 在 5-6 周内交付; 总工时 100-160 小时 (15-30 小时/周 × 5-6 周) | PRD §6.O1, intake Q1+Q2 | Hard |
| **C2** | 平台 = Telegram bot + 本地 Web UI (localhost, 无 auth) | PRD §7.C2, intake Q8 | Hard |
| **C3** | Balanced core loop (calibration : action ≈ 1 : 1, 阈值占位) | PRD §7.C3 | Hard |
| **C4** | alpha 目标年跑赢标普 2-5% (12+ 月观察, **非 v0.1 验证项**) | PRD §7.C4 | Soft (long-term) |
| **C5** | 显式三路冲突报告必含, **无默认优先级**, **顺序随机化** | PRD §7.C5, R10 (R2 强化) | Hard |
| **C6** | Telegram 主动推送 = 每周 1 次 + event, 不做日晨报, event 仅 per-market session 内 (D24) | PRD §7.C6, R4 (R2 强化) | Hard |
| **C7** | 研究 rigor > 上线速度 > UX polish > 技术简单度 | PRD §7.C7 | Hard (排序) |
| **C8** | 咨询师 pipeline 必含 (微信小程序源, **v0.1 仅 PDF/文本**, 视频/音频接口占位) | PRD §7.C8 | Hard |
| **C9** | 🧭 策略类模块 = 接口 + 占位, 完全解耦, 不在策略准度上差异化 | PRD §7.C9, R9 | Hard |
| **C10** | 单用户私用, localhost, 不商业化, 无 auth | PRD §7.C10, L2 moderator-notes | Hard |
| **C11** | **单次决策录入 < 30 秒** (硬门槛, 违反即系统失败) — wall-clock 起点 = GET `/decisions/new`, 终点 = POST `/decisions/{draft_id}/commit` 200 OK; **draft 阶段 LLM 等待包含在 30s 全程内** (无"preview 后才计时"的例外); cache miss 让 draft > 5s 是系统失败信号, 走 OP-1 mitigation | PRD §6.O5 / §S1 原口径 (R3 守) | Hard (kill-switch) |
| **C12** | onboarding ≤ 15 分钟 | PRD §6.O6 | Hard |
| **C13** | 稳定期维护 ≤ 3 小时/周 | PRD §6.O7, R5 | Hard |
| **C14** | 数据预算 $500/年, LLM 开销合理 (无明确数字, 但需在 architecture 给出策略) | PRD §2 | Soft |
| **C15** | 不自动下单 (永远红线 R1) | PRD §8.R1 | Hard (永远) |
| **C16** | 不做期权 / 加密 / 高杠杆 / 日内交易 | PRD §8.R2 | Hard (永远) |
| **C17** | 每次建议必有白话解释 (不许信号黑箱) | PRD §8.R3 | Hard |
| **C18** | Agent 不许诱导高频交易 (Barber-Odean 铁律) | PRD §8.R6 | Hard |
| **C19** | 防"学习假装" (3 个月自查机制) | PRD §8.R7 | Hard |
| **C20** | 不路径依赖单一咨询师 (架构预留多源, 即使 v0.1 仅一个) | PRD §8.R8 | Hard |
| **C21** | "不动 / 等待" 是一等正式输出 (UI + schema + review 三处体现) | PRD §8.R11 | Hard |

---

## 4. Prior Decisions (锁定的工程级决定)

每条决定都锁定一个工程方向, 任何 Codex / task-decomposer / parallel-builder
**不得 re-litigate**。新增于 spec (非 PRD 直接给出) 的决策标 `[new in spec]`。

R2 修订标 `[R2 revised]` (含 v0.1 已存在但内容修改) 或 `[R2 new]` (本次新增).

| # | Decision | Source |
|---|----------|--------|
| **D1** | 系统首先是 calibration engine, 其次才是 action engine。所有产品决策默认偏向"不动" | L2 stage doc §1 single biggest insight; PRD §1 |
| **D2** | "不动 / 等待"是一等正式输出 (UI tab 主场展示 + schema enum + review 单独类目) | PRD §R11; PRD §S2 |
| **D3** | 三路冲突报告**显式无默认优先级**, 占位源沉默时显示"暂无分歧"非空屏 | PRD §R10; PRD §S3 |
| **D4** | 越过"不承诺 alpha"红线 (因为是私用工具, 不是商业产品) | L2 moderator-notes §3 |
| **D5** | 单用户 localhost, 无 auth | L2 moderator-notes §1; PRD §C10 |
| **D6** | 策略类模块 (动手阈值 / 私有模型 / 多模态解析深度) v0.1 全部占位, **完全解耦** | L3R0 intake 🧭 原则; PRD §R9 |
| **D7** | `StrategyModule` IDL **唯一方法** `analyze() → StrategySignal` (签名: `(advisor_report, portfolio, ticker, env_snapshot)`); 预留 `CustomStrategyModule` 扩展位; **conflict_resolve 拆出到 ConflictReportAssembler 中立服务 (D22), devil_advocate 拆出到 DevilAdvocateService 独立服务 (D23)** | L3 stage doc §spec-writer 提示 #1; HANDOFF §spec-writer #1 (R2 revised: 解决 B2/B3, 解耦 IDL 自相矛盾) `[R2 revised]` |
| **D8** | 决策档案 schema 字段: `{trade_id, ticker, action, reason, pre_commit_at, env_snapshot, conflict_report_ref, devils_rebuttal_ref, post_mortem, would_have_acted_without_agent, status}`; **新增 status enum draft/committed/abandoned (R2 修订, 双阶段录入)** | HANDOFF §spec-writer #2; PRD §S5 (新增 `would_have_acted_without_agent` 用于 O3 度量); status 字段 R2 新增 `[R2 revised]` |
| **D9** | 咨询师 pipeline v0.1 路径 = **"human 触发 Proxyman fetch → watched folder = ~/decision_ledger/inbox/ → agent 解析"**; 触发方式 = `scripts/proxyman_fetch.sh` shell wrapper (human 手动调用, 可绑 Alfred/Raycast hotkey); fallback = Web UI 提供"贴 PDF" 按钮 (backup, 不是主路径) | HANDOFF §spec-writer #3; spec-writer 选择; **R2 修订: Q5 RESOLVED, 删除 "暂用默认假设" 字样** `[R2 revised]` |
| **D10** | 持久化 = **SQLite** (单文件、无运维、Python/JS 均原生支持、单用户并发足够) | HANDOFF §spec-writer 后续, PRD 留给 spec-writer 决 `[new in spec]` |
| **D11** | LLM 调用策略 = **Anthropic Claude API (Sonnet 4.6) + 本地缓存 (按 advisor_week_id + ticker hash)**, 缓存命中率作为开销监控信号; **缓存预热: D9 流程末尾 enqueue 30-50 关注股的 conflict report 预生成 (R2 新增, 服务于 D21)** | PRD §11 留给 spec-writer; 预算 $500/年 data + 合理 LLM `[R2 revised]` |
| **D12** | 主语言 = **Python 3.12 + uv** (因 LLM SDK ecosystem + pandas + Telegram bot 库成熟; Web UI 用 FastAPI + HTMX 轻量, 不引入 Next.js) | CLAUDE.md tool prefs (Python: uv); HANDOFF tech-stack 选项 `[new in spec]` |
| **D13** | **录入全程 < 30 秒的 UX 工程路径 (R3 修订, 守 PRD 原口径)**: <br/>**全程 wall-clock < 30s 包含 draft 阶段 LLM 调用**. **draft 阶段 LLM 调用必须 ≤ 5s** (cache 命中常态 ≤ 1s, miss 必须 ≤ 5s, 否则违反 C11). <br/>实现要求: <br/>(a) **ConflictCacheWarmer (D11)** 在 advisor_report 入库时预热 30-50 关注股 × 当周 advisor_week_id 的 conflict report (cache 命中目标 ≥ 95%). <br/>(b) **Rebuttal 因输入依赖 draft 内容不可缓存** (诚实承认), 故 Rebuttal LLM call **必须用最快配置: Sonnet 4.6 + max_tokens ≤ 100 + 极简 prompt + temperature 0.3, wall-clock 目标 ≤ 3s** (95th percentile). <br/>(c) draft + commit 两阶段总时长以 wall-clock 测量, **不分段**, 不允许 "preview 200 OK 之后才计时". <br/>**双阶段 UX 流**: <br/>**阶段 1 draft**: human 打开 `/decisions/new` → 录 ticker + intended_action + draft_reason → POST `/decisions/draft` 创建 draft (status='draft') → server 同步并发 (asyncio.gather) ConflictReport (D22) + Rebuttal (D23), wall-clock ≤ 5s 含 LLM 调用 → 渲染三列冲突 (顺序 hash 随机化) + 反方一句话页面. <br/>**阶段 2 commit**: human 看完三路 + 反方 → 可改 final action + 写 final reason ≤ 80 char + **强制 yes/no `would_have_acted_without_agent`** (M1) + Enter (commit) → POST `/decisions/{draft_id}/commit` → SQLite UPDATE status='committed', wall-clock < 1s. <br/>**若 draft 阶段 LLM 因 cache miss > 5s, 系统失败信号 → 走 OP-1 mitigation (UX 降级或 B-lite), 不允许 spec 自行扩大上限**. <br/>键盘快捷键 (1=buy / 2=sell / 3=hold / 4=wait) 在两阶段都可生效. | PRD §S1; HANDOFF spec-writer #2 提示 (R3 revised: 守 PRD 原口径, 不分段计时) `[R3 revised]` |
| **D14** | Web UI tab 列表: 决策档案 (主场) / 冲突报告 / 错位矩阵 / 笔记 wiki / 周 review / 月 review / 学习检查 / 设置 | PRD §4.12 `[new in spec, 列表化]` |
| **D15** | Telegram 仅承担: 周报推送 + event 通知 + 简单只读查询; **不承担**重操作 (录入 / 冲突报告 / review) | HANDOFF §spec-writer #4; PRD §S7 |
| **D16** | 错位矩阵可视化 = **纯 HTML table (server-rendered)** (R3 修订: T011 估时砍 3h, 删除 CSS 着色 / 排序; v0.2+ polish); 不引入 plotly / matplotlib (5 秒看完原则) | PRD §11 留给 spec-writer (R3 revised: 与 T011 R3 一致) `[new in spec, R3 revised]` |
| **D17** | "若未来商业化, 红线 R1/R2 + 合规需重来" — v0.1 不为商业化做任何预留 | PRD §5 永远不做; risks.md COM-1 |
| **D18** | ~~配偶可见度 v0.1 不实现, 但 ReviewGenerator 接口预留 audience 参数~~ **R2 删除** (M5 修订: PRD §11.4 把配偶可见度放到 v1.0+, v0.1 接口层预留属于弱 scope leak; partner audience 推后到 v1.0+ open question, 见 §8 Q4) | ~~PRD §11.4; L2 §4 v1.0 扩展~~ **R2 deleted** `[R2 deleted]` |
| **D19** | **LLM 调用时点 (R3 修订, 守 PRD 原口径)**: <br/>(a) **draft 阶段同步**: ConflictReport (D22) 与 Rebuttal (D23) 在 draft 创建时同步并发 (asyncio.gather), **总等待 ≤ 5s 包含在 30s 全程内** (R3: 删除 R2 "draft 阶段 LLM 同步等待 ≤ 10s 不算入 30s" 字样, 因为它越权改 PRD §S1 度量口径). <br/>(b) **commit 阶段无 LLM**: commit 路径只是 SQLite UPDATE status='committed', 不调任何 LLM, wall-clock < 1s. <br/>(c) **post-commit 异步**: 仅 weekly/monthly review 摘要 + post_mortem 解析等非关键路径 LLM 调用走 BackgroundTask. | PRD §S1 全程 30s 原口径 + PRD §UX 5 (R3 revised: 守 PRD 原意, 不分段) `[R3 revised]` |
| **D20** | 咨询师内容版权: 本地缓存仅服务于自用, 不 export, 不 republish (合规边界) | risks.md SEC-2 / LEG-2 `[new in spec]` |
| **D21** | **ConflictReport + Devil's Rebuttal 在 draft 阶段同步生成, 全程包含在 C11 30s 内 (R3 修订, 诚实承认 Rebuttal 不可缓存)**: <br/>**ConflictReport**: 可缓存. ConflictCacheWarmer (D11) 在 advisor_report 入库后预热 30-50 关注股 × 当周 advisor_week_id, 缓存命中目标 ≥ 95%, 命中场景 ≤ 1s; cache miss 时上限 5s (Sonnet 4.6 + 三路并发 + structured output). <br/>**Rebuttal**: **不可缓存** (输入依赖 `draft.intended_action` + `draft_reason`, 每次唯一). 故 Rebuttal LLM 调用必须用最快配置: **Sonnet 4.6 + max_tokens ≤ 100 + 极简 prompt + temperature 0.3**, wall-clock 目标 ≤ 3s (实测 95th percentile). <br/>**双调用并发** (asyncio.gather): 总 wall-clock ≈ max(ConflictReport latency, Rebuttal latency) = max(1s 命中 / 5s miss, 3s rebuttal) = ~3s 常态, ~5s miss. <br/>**留预算**: 25s 给 commit 阶段 form 操作 (常态) 或 25s commit (miss). <br/>**若实测 95th percentile draft 阶段 > 5s, 触发 OP-1 mitigation** (UX 降级或 B-lite), **不允许 spec 自行扩大上限到 10s 或更长**. | architecture.md §3.3 R3 重写 sequence diagram + §3.6 cache warmer fast-path 配置 `[R3 revised]` |
| **D22** | **ConflictReportAssembler 是中立 domain service** (不是 StrategyModule lane, R2 新增, B2 解决): <br/>签名 `assemble(signals: list[StrategySignal], env_snapshot: EnvSnapshot) → ConflictReport`. <br/>实现 = LLM prompt 严格 instruction "不要选 winner, 仅描述 X/Y/Z 三方观点, 共同点 / 分歧点". <br/>Web UI 三列**等宽**, 顺序由 `hash(source_id + day) % 6` 随机化 (避免固定位置 = 固定权重). <br/>`ConflictReport.signals` 永远 ≥ 3 (即使有 confidence=0.0 占位). <br/>无 `priority` / `winner` / `recommended` 字段 (R10 红线). | architecture.md §3.1 R2 重写 IDL `[R2 new]` |
| **D23** | **DevilAdvocateService 是独立服务** (不是 StrategyModule lane, R2 新增, B2 解决): <br/>签名 `generate(decision_draft: DecisionDraft, env_snapshot: EnvSnapshot) → Rebuttal`. <br/>实现 = LLM prompt ≤ 80 字反驳, R6 反诱导高频. <br/>调用时点 = draft 阶段同步 (与 ConflictReport 并行 asyncio.gather). | architecture.md §3.1 R2 重写 IDL `[R2 new]` |
| **D24** | **Per-market session config (R2 新增, H4 解决)**: event push 必须按 ticker.market 字段判断 session window. <br/>US (NYSE/NASDAQ): 09:30-16:00 ET. <br/>HK (HKEX): 09:30-16:00 HKT. <br/>CN (SSE/SZSE): 09:30-15:00 CST. <br/>session window 由 `ticker.market` enum 决定; 默认 'US' 若未填 (兼容 v0.1 单市场启动). | PRD §2 + R4 节制 (R2 H4) `[R2 new]` |

---

## 5. Task Breakdown (phases only; tasks/T*.md 由 task-decomposer 展开)

下列 phase 边界是建议性的; task-decomposer 可调整粒度但应保持顺序依赖。

R2 修订: **T020 (失败告警 O10) 从 Phase 3 提前到 Phase 1 末段** (H1 解决), 与 T014 周度 review 并行启用. T021 解耦 T019 (H3 解决).

### Phase 0 · 基础 (T001-T005, 估 40h)
- T001 项目脚手架 (uv + pytest + ruff + pre-commit) — 6h
- T002 数据 schema 定义 (Decision / DecisionDraft / EnvSnapshot / Watchlist / Holding / AdvisorReport / ConflictReport / Rebuttal / Note / Alert / LLMUsage) — 9h
- T003 SQLite 持久化层 (Repository pattern, migration 工具) — 10h
- T004 Web UI shell + 多 tab + 免责 footer + alert banner endpoint — 7h
- T005 LLMClient 抽象 + 缓存 + 用量记账 — 8h

### Phase 1 · 核心 pipeline + core loop (T006-T013 + T020, 估 82h)
- T006 咨询师 PDF/文本解析 + watched folder + Proxyman 触发 + paste fallback — 13h
- T007 StrategyModule IDL (analyze only, R2 D7) + 三占位 + lane 隔离 — 12h
- T008 决策档案 **draft + commit 双阶段** UX (Web, D13) — 16h
- T009 全程 30 秒 timing test E2E + 手动压测脚本 (R3 守 PRD 原口径) — 6h
- T010 ConflictReportAssembler 中立服务 + cache warmer + pause hook — 11h
- T011 错位矩阵 HTML table (**R3 砍至 3h**: 仅 HTML table, 不做颜色着色 / 排序, v0.2+ polish) — 3h
- T012 关注股 + 持仓快照录入 UI — 6h
- T013 DevilAdvocateService 独立服务 (R3: fast-path 配置 max_tokens ≤ 100, ≤ 3s) — 4h
- T020 失败告警 O10 + dashboard + pause_pipeline façade (R2 H1 提前到 Phase 1 末段) — 8h

### Phase 2 · review / 学习 / Telegram (T014-T018, 估 26h)
- T014 周度 review 生成器 (cron + 维护工时, tz Asia/Taipei) — 8h
- T015 月度 review 生成器 (**R3 砍至 3h**: 仅生成 markdown 文本汇总 + Web view, 不实现 PNG 图表 / 月度自定义; partner audience 删除) — 3h
- T016 个人金融笔记 wiki (**R3 砍至 4h**: 仅 markdown 文件 + 简单全文搜索 grep, 不做 agent 自动去重 v0.1; v0.2+ 加 LLM 去重) — 4h
- T017 Telegram bot (周报 + event + per-market session window, R2 D24) — 11h
- T018 post-mortem 字段 UI (**R3 砍至 3h**: 仅 form 录入, 不做触发提醒 / 自动 N 天后弹窗 v0.2+) — 3h (重新调整 with T021)

注: T018 4h → 3h, R3 砍 1h.

### Phase 3 · 学习检查 + onboarding + B-lite (T019/T021/T022, 估 12h)
- T019 学习检查 (**R3 砍至 5h**: human 手编 master checklist, agent 仅按 checklist 抽问 + 评分; 不调 LLM 抽题) — 5h
- T021 Onboarding 15 分钟 (**R3 砍至 4h**: 仅文档 + 1 个 setup wizard route, 不做 in-app tooltip; step 7 极简空态; runbook + README 极简) — 4h
- T022 B-lite 降级路径 (**R3 砍至 3h**: 仅 `scripts/toggle_b_lite.py` CLI + runbook, 删除 `/settings/b-lite` UI toggle; pause_pipeline façade 已在 T020) — 3h

**总估 (R3 cut 后)**: **~120-160h** (Phase 0: 40h + Phase 1: 82h + Phase 2: 26h + Phase 3: 12h ≈ **160h** 边界).
- R3 共砍 21h: T011 -3h / T015 -5h / T016 -3h / T018 -1h / T019 -3h / T021 -4h / T022 -2h
- 181h (R2 task header 实和) - 21h = **160h** 满足 C1 hard max
- 详见 risks.md OP-2 mitigation (R3 修订)

---

## 6. Verification Criteria

每个 Outcome 必须有可执行 verification (runnable test / 度量数字 / 人工 sign-off)。

| Outcome | Verification |
|---------|--------------|
| **O1** | `git log --pretty=format:"%h %ad" --date=short` 首尾间隔 ≤ 42 天; human 自报工时表 ≤ 160h (≥ 100h 表示有效投入) |
| **O2** | `pytest tests/integration/test_o2_decision_count.py` (在 ship + 8 周快照点对 production DB 跑) 断言 `count(*) where status='committed' >= 15` (R2 修订: 仅算 committed) |
| **O3** | `pytest tests/integration/test_o3_calibration_evidence.py` 断言 `count(*) where would_have_acted_without_agent = true AND status='committed' >= 3` |
| **O4** | `python -m scripts.learning_check --quarter Q1` 生成自查表; human 提交答案; 评分脚本 `scripts/grade_learning.py` 输出 ≥ 7/10 |
| **O5** | **R3 修订, 守 PRD 原口径, 度量改为全程 wall-clock**: <br/>(a) `pytest tests/e2e/test_decision_input_timing.py` 自动化模拟全程 wall-clock < 30s (**起点 = GET `/decisions/new` 200 OK**, **终点 = `POST /decisions/{draft_id}/commit` 200 OK**); 同时分解记录 draft 阶段 LLM 等待 (≤ 5s D21 上限, cache 命中常态 ≤ 1s) 和 commit 阶段 (< 1s, 无 LLM); cache miss 让 draft > 5s 走 OP-1 mitigation. <br/>(b) `scripts/manual_press_test.py` 引导 human 连续 5 次手工录入, **全程** wall-clock 全部 < 30s, 写入 `release_log.jsonl` (schema 见 architecture.md §10) |
| **O6** | `pytest tests/e2e/test_onboarding.py` 模拟首次启动 → 录入 → 首次决策 (含 draft → commit), 断言 elapsed < 900s |
| **O7** | weekly maintenance log 每周 sign-off, 4 周滚动平均 ≤ 3h |
| **O8** | `pytest tests/integration/test_telegram_cadence.py` 断言任意 7 天内 push 数 ≤ 1 + event 触发数; **per-market session window 单测 (US/HK/CN 三市场, R2 D24)** ; 监控 dashboard 周度图 |
| **O9** | **不在 v0.1 验证范围**; 12 个月后由 human 手动比对组合回报 vs SPX 总回报 |
| **O10** | `pytest tests/integration/test_failure_alert.py` mock 连续 2 周档案 < 2 条, 断言告警发出; ship 后 dry-run 一次 (临时插入 mock 数据) 确认 Telegram + Web banner 双通道告警; **`pytest tests/unit/test_pause_pipeline_hook.py` 断言 T010 `ConflictWorker.pause()` + T015 `MonthlyScheduler.pause()` hook 存在并可调用 (R2 H1)** |

**附加门控** (合并验收, 非单一 outcome):
- 全量 unit + integration test ≥ 85% 通过率, 0 critical bug
- ruff 0 violation, mypy strict 通过
- README + runbook 已写, human 能独立从 git clone 走通 onboarding

---

## 7. Glossary (术语权威定义)

| 术语 | 在本项目的精确含义 |
|------|------------------|
| **决策档案 (Decision)** | 一次 `动 / 不动 / 等待` 的结构化记录, schema 见 D8; **status ∈ {draft, committed, abandoned}** (R2) |
| **决策草稿 (DecisionDraft)** | **R2 新增**: pre-commit 阶段的临时记录, 未入正式档案. 30 分钟未 commit 自动 GC. 见 D13. |
| **错位矩阵 (Misalignment Matrix)** | "咨询师强推 vs 你轻仓 / 咨询师谨慎 vs 你重仓"的对齐度可视化, 规则+加权占位 |
| **三路冲突报告 (ConflictReport)** | 由 advisor_strategy / placeholder_model / agent_synthesis 三个 StrategyModule 实例产出的 StrategySignal 列表 + 白话根因, 显式三列**等宽**, 无默认优先级, **顺序 hash 随机化** (R2 D22) |
| **StrategyModule** | 抽象接口, **唯一方法** `analyze() → StrategySignal` (R2 修订, D7); v0.1 三个占位实现; **不承担 conflict_resolve / devil_advocate** (这两个职责拆给 ConflictReportAssembler / DevilAdvocateService) |
| **ConflictReportAssembler** | **R2 新增**: 中立 domain service, 不是 StrategyModule lane. `assemble(signals, env_snapshot) → ConflictReport`. LLM prompt 严格不选 winner, 仅描述三方观点 + 共同点 + 分歧点. 见 D22. |
| **DevilAdvocateService** | **R2 新增**: 独立反驳服务, 不是 StrategyModule lane. `generate(decision_draft, env_snapshot) → Rebuttal`. 一句反驳 ≤ 80 字. 见 D23. |
| **占位源 (Placeholder Strategy)** | v0.1 用规则 / 粗糙 LLM prompt / 手工触发**扮演**的"私有模型", 不是真 ML 模型 |
| **Calibration Engine** | 帮助判断"什么时候不该动"的能力子集; 是本系统的**首要**职能 |
| **Action Engine** | 帮助判断"该买/卖什么、买多少"的能力子集; 是本系统的**次要**职能 |
| **承诺壳 (Commitment Shell)** | 把"用户自己的决定"作为核心对象的 personal shell; 区别于"信息壳" (把外部信息更好映射到组合) |
| **信息壳 (Information Shell)** | 拥挤赛道 (Fiscal.ai/Koyfin/Aiera/Bridgewise/雪球付费), 不是 B 主场 |
| **EnvSnapshot** | 决策当时的 `{price, holdings, advisor_week_id}` 快照; 不可变 |
| **Devil's Advocate** | 每次 action 前 LLM 出一句反驳 (占位实现), 强制听一句反方意见; **由 DevilAdvocateService 实现** (R2) |
| **学习假装 (Learning Pretense)** | 用户用了 3 个月仍然解释不清关键概念的现象; v0.1 必须能检测 (R7) |
| **失败告警 (Failure Alert)** | 连续 2 周决策档案 < 2 条触发的红色告警, Telegram + Web banner 双通道 |
| **B-lite** | **R3 修订, M2 真正解决**: 应急降级路径概念 = 砍冲突报告 + 月度 review, 保留档案 + 周度 review。**v0.1 不实现 UI toggle, 也不实现 `/settings/b-lite` 路由** (R3: 与 R2 不一致已统一); 仅 `scripts/toggle_b_lite.py` CLI + runbook 即可触发. `pause_pipeline()` / `resume_pipeline()` hook 在 T010 (ConflictWorker) + T015 (MonthlyScheduler) outputs **必须存在** (T020 提前后, CLI 直接调这些 hook 而非"假设存在"). T022 仅是 CLI + runbook + meta_decisions 历史表 (无 UI toggle). |
| **Pause Pipeline Hook** | **R2 新增**: 在 T010/T015 显式暴露的接口 `pause_pipeline()` / `resume_pipeline()` / `is_paused()`, 用于 B-lite 等情境下停掉 ConflictWorker / MonthlyScheduler 而保留 Decision/Weekly review 流. 不在 v0.1 UI 暴露 toggle, 但 hook 必存在并单测覆盖. |

---

## 8. Open Questions for Operator

直接复刻 PRD §11 的 4 条, spec 阶段未独立解决, 需 human 决定。**这些不阻塞 spec
冻结, 但会影响 implementation 细节**。

R2 修订: **Q4 推后到 v1.0+** (M5 解决, D18 删除); **Q5 RESOLVED** (H5 解决, D9 锁死路径).

R3 修订: **删除 Q11** (R2 引入的 "cache miss 5-10s 例外" 与 PRD §S1 / §6 O5 原口径冲突, 路径 A 守 PRD 不允许此例外; 改为 D13 / D21 的 fast-path + cache 预热, OP-1 mitigation 兜底).

### Q1. "稳定赚钱" benchmark 与时间尺度
PRD §6.O9 给了 "跑赢标普 2-5%/年", 但**多少年算"稳定"**? 6 个月 / 12 个月 / 3 年?
**spec 影响**: 若选 12 个月, review generator 需输出年化对标数据; 若选 3 年, v0.1
仅积累数据不出年化, 减少假精度。
**默认假设 (spec 暂用)**: **12 个月** (一年滚动窗口), 但仍标 OPEN。

### Q2. 动机二选一
"成为会投资的人" (需要持续摩擦 → B 更 fit) vs "摆脱不知道该怎么办的焦虑" (需要清
晰出口 → A 更 fit)?
**spec 影响**: 若选后者, B 的 upkeep 撑不住, 应该已经改 fork A。spec 不为后者预留。
**默认假设**: **前者 (成为会投资的人)**, 已通过 fork B 隐含确认。

### Q3. 情绪承受预案 (两周冷静期机制)
连续两次建议都亏钱, 是否需要明确"两周冷静期"机制 (系统暂停推送 / 强制 review 才能
继续)?
**spec 影响**: 若需, 增加 `cooling_off_period` 状态机到 D2 review pipeline。
**默认假设 (spec 暂用)**: **不实现 v0.1, 进 v0.2 待 human 8 周自我观察后决定**。

### Q4. **(R2 推后)** 配偶可见度接口预留
**R2 修订**: D18 已删除 (M5: PRD §11.4 把配偶可见度放到 v1.0+, v0.1 接口层预留属于
弱 scope leak). v0.1 **不实现, 不预留接口**. v1.0+ 评估窗口再答此问题.
**Block 状态**: 推后到 v1.0+, 不阻塞 v0.1.

### Q5. **(R2 RESOLVED)** Proxyman 半自动 pipeline 的具体接入方式
**R2 修订**: D9 已锁死:
- watched folder = `~/decision_ledger/inbox/`
- 触发 = `scripts/proxyman_fetch.sh` shell wrapper, human 手动调用 (Mac 可用 Alfred / Raycast 绑快捷键)
- fallback = Web UI 提供"贴 PDF" 按钮 (backup, 不是主路径)

详见 D9 + open-questions.md Q5. 不再 OPEN.

---

## 9. spec-writer 自查 (交付前)

- [x] 6 个核心 section 全部存在
- [x] 每个 Outcome 引用 PRD §6 同名条目
- [x] 没有出现 PRD scope OUT 中的功能 (R2 删除 D18 后修复)
- [x] 每条 Prior Decision 都引 source (PRD / L2 moderator-notes / L3 stage / `[new in spec]` / `[R2 revised]` / `[R2 new]` / `[R2 deleted]` / `[R3 revised]` 标注)
- [x] 每条 Verification 都给出可执行命令 / 度量数字 / 人工 sign-off
- [x] Glossary 覆盖关键术语 (决策档案 / DecisionDraft / 错位矩阵 / 三路冲突报告 / StrategyModule / ConflictReportAssembler / DevilAdvocateService / 占位源 / calibration engine / 承诺壳 / Pause Pipeline Hook)
- [x] Open Questions 都标注了 spec 默认假设 (避免实现卡死); R3 删除 Q11
- [x] § 5 task phases 不写具体 T001-TXXX (留给 task-decomposer); 但反映 R2/R3 phase 调整 (T020 提前 / T021 解耦 / R3 cut 21h)
- [x] **R2 contract-level 修订**: B1 (pre-commit framing 修复) / B2 (agent_synthesis 拆) / B3 (IDL 自洽) 全部通过 D7/D13/D19/D21/D22/D23 解决
- [x] **R2 H1-H5**: H1 (T010/T015 pause hook 显式) / H2 (cut list 在 risks.md OP-2) / H3 (T021 解耦 T019) / H4 (per-market session D24) / H5 (D9 RESOLVED) 全部解决
- [x] **R2 M1-M5**: M1 (commit 阶段强制 yes/no) / M2 (B-lite glossary 统一) / M3 (Asia/Taipei + tzlocal fallback) / M4 (logs schema 在 architecture.md §10) / M5 (D18 删除) 全部解决
- [x] **R3 修订, 守 PRD 原口径**: B-R2-1 (O5/C11 度量回退到全程 wall-clock) / B-R2-2 (T008 删除 placeholder fallback) / B-R2-3 (D21 诚实承认 Rebuttal 不可缓存 + fast-path) / B-R2-4 (task pack 真砍 21h 到 160h) / B-R2-5 (Q11 删除) 全部解决
- [x] **R3 ⚠️ R1 残留**: ⚠️ B1 (与 B-R2-1 + B-R2-2 联合 close) / ⚠️ B3 (T007 加 contract-level 隔离 + runtime test) / ⚠️ H1 (T015/T017 删除旧 blocks [T020]) / ⚠️ M2 (B-lite 删 UI toggle) 全部解决
