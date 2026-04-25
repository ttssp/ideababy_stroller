# Non-Goals — 004-pB · 决策账本

**Version**: 0.1
**Created**: 2026-04-25T15:25:00+08:00
**Companion**: PRD §5 (Scope OUT) · spec.md §2.2

> 一份 spec 没有显式 non-goals 是**未完成的 spec**。Agents 默认会扩 scope, 显式
> non-goals 是唯一刹车。本文档对每条 non-goal 写明:
> 1. **它为什么诱人** (容易被加进 v0.1 的原因)
> 2. **为什么 v0.1 不做** (硬约束 / 红线 / 时间 / 反价值)
> 3. **何时重新评估** (v0.2 / v0.5 / v1.0 / 永远)

---

## A · v0.2+ 推迟 (1-3 个月内回看)

### A1. 事件日历 / FOMC / 财报预警主动推送

**诱人**: PRD §UX 7 提到 event 触发推送, 用户场景 (L2 §3 场景 B) 描绘了 FOMC 前 2 小时的保护场景, 数据源 (CME FedWatch + TradingView) 公开免费。

**v0.1 不做**:
- 这是 Candidate C 主场, B 的核心是**承诺壳**不是事件壳 (信息壳偏事件)
- 加进 v0.1 会把 Telegram push 节制 (R4 / O8) 边界推到模糊
- 事件→持仓映射逻辑是独立子系统, 5-6 周时间估算不含

**v0.1 范围**: event 触发推送 = **被动配置** (human 手动登记某些 ticker 的财报日, 系统 push), 不**主动**整合外部 event 数据库

**重新评估**: v0.2 (1-3 个月), 可与 fork 004-pC 合并

---

### A2. 私有模型真实训练 (XGBoost / LSTM / 自定义 ML)

**诱人**: human 是 ML PhD, 这是他的强项; L2 v2 §1 描绘的"私有策略编织层"承诺这一部分。

**v0.1 不做**:
- C9 / R9 硬约束: 策略类模块 v0.1 全占位, 不在策略准度上差异化
- 训练真模型 = 多周专项工作 + 数据准备 + 验证 + 防过拟合 (L2 红线 #2)
- 占位实现 (规则 + 粗糙 LLM prompt) 已能驱动 core loop

**v0.1 范围**: `StrategyModule` IDL 已锁, `CustomStrategyModule` 扩展位预留 (D7)

**重新评估**: v0.5 (3-9 个月)。前提: v0.1 8 周自我观察证明 calibration 机制可行, 再训模型才不浪费

---

### A3. 多市场 cross-signal (美股 / 港股 / A 股关联)

**诱人**: PRD §2 用户跨三市场, 半导体链 / 美元-黄金-中概的关联是真实信号。

**v0.1 不做**:
- 跨市场 correlation 算法 + 时区处理 + 多市场行情数据源 = 复杂度炸开
- v0.1 30-50 关注股 + 单市场 advisor 已足以验证 core loop
- 加进来违反 C7 优先级 (研究 rigor > 速度), 但触发时间溢出风险 OP-2

**v0.1 范围**: ticker 字段不限市场, 但分析逻辑不跨市场

**重新评估**: v1.0 (9-18 个月)

---

### A4. 音频 / 视频解析 (咨询师多模态)

**诱人**: PRD §11 freeform 明确咨询师内容含视频/音频/PDF/图文, 用户实际**继续**手动消化视频/音频。

**v0.1 不做**:
- C8 显式: v0.1 仅 PDF/文本; 视频/音频走接口占位 (v0.2+)
- 视频转录 (Whisper / Anthropic vision) + 音频处理 + 图片 OCR = 数周专项
- 5-6 周时间估算下, 优先打穿 PDF/文本 pipeline

**v0.1 范围**: `AdvisorParser` 接口预留 `parse(file: Path) → AdvisorReport`, 实现仅 PDF; v0.2+ 同接口加 mp4/mp3/png 实现

**重新评估**: v0.2 (1-3 个月), 优先级在 A1 之后

---

### A5. 自动抓取咨询师内容 (微信小程序 auth + 调度)

**诱人**: human 已用 Proxyman 手动 fetch, 自动化是自然下一步; 减少 weekly 操作摩擦。

**v0.1 不做**:
- 微信小程序 auth / session / token 管理边界复杂 (违反 SEC-2)
- 半自动 (human 触发 Proxyman fetch → watched folder) 已足够低摩擦 (D9)
- 完整自动化 = 数周专项

**v0.1 范围**: WatchedFolderWatcher 接口稳定 (D9); v0.2+ 替换 trigger 源即可

**重新评估**: v0.2 (1-3 个月)

---

## B · v1.0+ 推迟 (9-18 个月)

### B1. 配偶可见度模块 (R2 修订: 接口也不预留)

**诱人**: PRD §11.4 + L2 §4 v1.0 扩展; 决策档案天然 partner-friendly (文本可读)。

**v0.1 不做** (R2 强化):
- L2R3-GPT Q10 答案未明 (PRD §11.4 仍 OPEN)
- 多受众视图 = 信息过滤 + 隐私边界 + UX 二次设计
- v0.1 单用户精简模式
- **R2 M5**: Codex R1 review 指出 v0.1 接口预留 `audience: enum {self, partner}` (D18) 也算超出 PRD §11.4 (v1.0+) — 弱 scope leak. **D18 删除**, 不预留接口.

**v0.1 范围 (R2 修订)**: `ReviewGenerator.generate(month_id)` 仅 `self` 视角, 无 audience 参数. `MonthlyReviewService.generate` 签名也对应修订.

**重新评估**: v1.0+, 由 human 与配偶外部对话决定优先级再实现 (届时配偶可见度信息过滤 + 隐私边界 + UX 二次设计完整重做, 不靠 v0.1 接口预留)

---

### B2. 回测环境

**诱人**: ML PhD 习惯 backtest 验证策略, 配合 A2 私有模型一起做更顺。

**v0.1 不做**:
- 策略全占位 (D6), backtest 没意义
- 历史行情数据 + backtest 引擎 + walk-forward 框架 = 重型子系统
- $500/年数据预算可能不够

**v0.1 范围**: 无 backtest, post-mortem 字段 (Decision.post_mortem) 是真实决策的事后回报

**重新评估**: v1.0+, 配合 A2

---

## C · v1.5+ (永远红线上限)

### C1. 半自动执行 (event 触发时 agent 起草 order, 一键确认)

**诱人**: 减少决策到执行延迟; L2 §4 v1.5+ 扩展提到。

**v0.1 不做**:
- 红线 R1 上限: 永远保留 human 最终决策权
- "一键确认" 的边界容易被工具滑成"自动下单"
- 自用单人, 没有"延迟"商业损失

**v0.1 范围**: 不接 broker API (TECH 视角), 不存账户凭证 (SEC 视角)

**重新评估**: 永远不在本 fork; 若有强需求, 应 fork 新 spec

---

## D · 永远不做 (硬红线, 任何版本不做)

### D1. 自动下单 (R1 红线)

**为什么不做**: 自用工具的核心价值是 calibration engine + 学习路径 + 心理舒适度。自动下单会:
- 把 human 从决策回路拿掉 → 反向于 calibration engine
- 引发监管认定为 robo-advisor (LEG-1)
- 出错时无 human review buffer

**永远不做的范围**: 任何形式的自动 order placement, 包括 paper trading 自动 (因为 paper trading 习惯会迁移到真账户)

---

### D2. 期权 / 加密 / 高杠杆 / 日内交易 (R2 红线)

**为什么不做**: PRD §2 用户画像 — "不懂期权 / 大部分技术指标 / 大多数衍生品机制", 不感兴趣, 违背稳健目标 (20% 回撤上限)。Barber-Odean 铁律对高频交易 (日内) 直接成立。

**永远不做的范围**: 系统不存 options / crypto / leverage / intraday 字段; ticker enum 不接受 ETF 杠杆产品 (TQQQ / SOXL 等也排除以保持纪律)

---

### D3. 商业化 / 付费层 / 多用户

**为什么不做**:
- D5 单用户 localhost 是架构基础, 多用户需重写整个 auth + tenant + scaling 层
- 商业化引发监管认定 (LEG-1) + 合规重审 (COM-1)
- 自用工具的 forcing function 与商业产品不同, 商业化会扭曲设计

**永远不做的范围**:
- 任何 auth 系统 (即使"为未来"预留也不允许)
- 任何 user_id / tenant_id 字段 (单 user 隐式)
- 任何对外 API (even read-only)
- 任何收费支付集成

**例外** (NOT in this fork): 若 human 改主意, 必须 **fork 新 spec** (e.g. `004-pB-commercial`), 不复用本 spec。本 spec 不为商业化做任何预留 (D17)。

---

### D4. 广谱 research terminal 功能

**为什么不做**: 这是 Candidate A 主场 (信息壳), 不是 B 主场 (承诺壳)。GPT L3R2 scope-reality search 已证明信息壳赛道饱和 (Fiscal.ai / Koyfin / Aiera / Bridgewise / 雪球付费)。

**永远不做的范围** (本 fork 内):
- 多源行情聚合 (yahoo / bloomberg / IB)
- earnings calendar UI (即使 v0.2+ 加, 也是 event 视角不是 research 视角)
- transcript 全文搜索
- screener / stock filtering
- 大盘 / 板块 dashboard (除了支持决策记录的最小集)

**注意**: OP-6 监控偏离 (是否 human 实际打开"错位矩阵 tab" > "决策档案 tab")

---

### D5. AI agent 推荐高频交易行为

**为什么不做**: R6 + Barber-Odean 铁律 — 散户越频繁交易净回报越差。Agent 默认偏向"不动 / 等确认"。

**永远不做的范围**:
- LLM prompt **不允许**输出 "建议本周做 X 笔操作"
- LLM prompt **必须**至少 50% 的 conflict_resolve 输出 "建议不动"
- weekly review 不展示"本周可能动作 candidate" 列表 (避免诱导)
- Telegram 不主动建议 buy/sell

**测试覆盖**: prompt 单元测试 + LLM 输出 sanity check (建议比例随机抽查 ≥ 50% "不动")

---

### D6. 信号黑箱 (没白话解释的建议)

**为什么不做**: R3 红线 + L2 §6 ScienceDirect 2024 + Springer 2026 研究 — 低 explainability 把用户推向 trust heuristic, blind trust 是 AI 财务建议最大失败模式。

**永远不做的范围**:
- StrategySignal.rationale_plain **永远非空** (架构不变量 §9.4)
- ConflictReport.divergence_root_cause **永远非空** (即使 has_divergence=False 时填 "暂无分歧")
- Devil's advocate Rebuttal.rebuttal_text 非空

---

### D7. 看盘焦虑机 (日推送 / 高频通知)

**为什么不做**: R4 红线 + PRD §UX 通知节制。

**永远不做的范围**:
- Telegram push 频率上限: 7 天滚动窗口 ≤ 1 周报 + event_count
- event push 仅在 ticker 对应市场的 session 时间 (R2 D24, 解决 H4):
  - US (NYSE/NASDAQ): 09:30-16:00 ET
  - HK (HKEX): 09:30-16:00 HKT
  - CN (SSE/SZSE): 09:30-15:00 CST
  - 默认 US 若 ticker.market 未填
- 不做 daily 晨报 / 收盘 summary
- 不做 ticker 价格变动通知 (即使 human 持仓)

**测试覆盖**: `test_telegram_cadence.py` (O8) + **R2 新增** `test_per_market_session.py` (D24 H4)

---

### D8. 单一咨询师路径依赖

**为什么不做**: R8 红线 — 即使 v0.1 只有一个咨询师, 架构必须预留多源。

**永远不做的范围**:
- AdvisorReport.advisor_id 必须是 enum / FK, 不是 hardcode
- LLM prompt 不 hardcode "哥大背景华语投顾"
- 错位矩阵算法不假设 advisor 数量 = 1

**v0.1 实际**: 只有一个 advisor 实例 (`advisor_id="primary"`), 但 schema 支持 N 个

---

### D9. 用户金融素养永远不被验证

**为什么不做**: R7 红线 — 防"学习假装"。

**永远不做的范围**:
- 不能因为"用户已经使用 3 个月"就假设懂金融
- 学习检查 (季度) 必须 invoke, 即使 human 自己想跳过, UI 也必须显示提醒

**v0.1 实现**: `LearningCheck` 季度自查表 (O4 verification)

---

## E · 未来可能扩展, 但**不在 v0.1 预留**

下列项不是 non-goal (v0.5+ 可能做), 但 v0.1 **不为它们 over-engineer 接口**:

- 多 LLM 提供商 (v0.1 只 Anthropic)
- 多语言 UI (v0.1 仅中文 + 英文 ticker)
- mobile native app (v0.1 Telegram 已覆盖移动)
- 数据可视化高级图表 (v0.1 HTML table 即可)
- AI 自动事后回报记录 (post_mortem 字段 v0.1 由 human 手动填)
- A/B test 不同 prompt 的效果 (v0.1 单 prompt)

**v0.1 不预留** = 接口可以重构, 不强求"将来灵活"。YAGNI 优先。

---

## 自查 (spec-writer 提交前)

- [x] non-goals 不为空 (anti-pattern 5 防御)
- [x] 每条 non-goal 给了"诱人原因 + v0.1 不做原因 + 何时重审"
- [x] 永远红线 (D1-D9) 与 PRD §8 / spec.md C15-C21 一致
- [x] 商业化 non-goal 明确 "不做预留, 改主意需 fork 新 spec"
- [x] 信息壳 vs 承诺壳的边界明确划开 (D4)
