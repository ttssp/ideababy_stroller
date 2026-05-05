# L3 Scope Menu · 004 · "个人自用投资副驾驶 + 金融教练 (v0.1 shell)"

**Generated**: 2026-04-29T (re-synthesized under updated scope-protocol with split Scope OUT / Phased roadmap)
**Source**: L2 v2 report (stage-L2-explore-004.md) + L3R0 intake + 2 轮辩论 (双方各 L3R1 + L3R2)
**Rounds completed**: L3R1 (Opus + GPT), L3R2 (Opus + GPT, 含 5 组 scope-reality search × 2)
**Searches run**: 10 组 scope-reality queries (不涉技术栈)
**Moderator injections honored**: 0 (L3 无 moderator 注入; L2 binding moderator note 已在 v2 report 中体现)
**Layer**: 根 idea 的 L3 synthesis (非 fork — human 在 L1 菜单选 [S] skip, 用原 proposal 进 L2)
**Verdict inherited from L2**: `unclear` on "稳定赚钱" core promise (证据不支持) · 但 idea 本身对这一个具体用户有真实价值
**Protocol version**: scope-protocol updated 2026-04-29 — Scope OUT 拆分为 "永远不做 (red-line)" + "Phased roadmap (committed)"。本菜单是首次按此结构重生成, 旧版 `stage-L3-scope-004_v01.md` 保留作为 backup。

---

## 如何阅读这份菜单

1. **v0.1 = 纯私人自用工具**, 不商业化, 用户 = human 本人 (不是 SaaS, 不是产品)。
2. **🧭 硬性原则 (来自 intake, 绑定所有 candidate)**: 策略类模块 (动手阈值 / 私有 ML 模型 / 咨询师多模态解析深度) 一律 **"清晰接口 + 最简占位实现"**, v0.1 不在策略准度上差异化, 只在 **shell 形态 + 平台主次 + 记录深度** 上差异化。
3. **关键 tradeoff 有两层**: GPT 在 L3R2 基于 search 证据提出了一个 **比 Opus 更根本** 的 axis (信息壳 vs 承诺壳), Opus 的 axis (calibration 场景类型) 是第二层。下文 §"关键 tradeoff" 会同时呈现两个 axis 及其相互关系, human 可按任一层决策 — 两者不冲突, 但 GPT axis 的 search 证据更硬。
4. **L2 verdict `unclear` 的 tension 继承**: "稳定赚钱"承诺未被外部证据支持, v0.1 无法在 3-6 周内验证这一点 — 只能通过 **v0.1 → v0.5 的自用数据 incremental 验证**。synthesizer 推荐不会假装这个 tension 不存在。
5. **【新协议要点】每个 candidate 的"非 v0.1"工作分两类**:
   - **Scope OUT (永远不做)** — red line, 项目身份冲突, 不留扩展点 (例如自动下单 / 期权 / 日内)
   - **Phased roadmap (committed, 按阶段交付)** — v0.2 / v0.5 / v1.0 / v1.5+, **必留扩展点**, 来源于 L2 §4 Natural extensions, 每项标注 phase / 难度 / 重要度 / 对应 L2 §4 风险编号
6. Fork 动作一旦选定, 进 L4 前 human 应先做 GPT §6 的 4 个"自我访谈", 特别是 **连续 5 次尝试决策档案录入 <30 秒** 这个压力测试 — 这是 v0.1 成败的最硬前置条件。

---

## Intake recap — 我们 honor 了什么

### 8 条 hard constraints (来自 L3R0 intake Summary, 每个 candidate 都遵守)
1. **3-6 周交付 v0.1** (≈45-180 小时开发预算)
2. **Balanced core loop** (calibration + action 1:1, 但 "动手阈值" = 占位, 后续调)
3. **温和 alpha 目标** (年跑赢标普 2-5%, 机制可解释) — 注意: v0.1 不要求已达到, 只要求机制成立
4. **显式冲突报告 UI** 是 v0.1 必含元素 (不是 nice-to-have)
5. **节奏 = 每周 1 次周报 + event 触发**, 不做日晨报 (防"看盘焦虑机")
6. **平台 = Telegram bot + 本地 Web UI (localhost)**, 两者都要
7. **优先级 = 研究 rigor > 速度 > UX polish > 技术简单度**
8. **咨询师 pipeline 必含** (微信小程序多模态源; v0.1 只做 PDF/文本, 视频/音频走接口占位)

### 🧭 scope-shaping 原则 (human 在 intake 明确补充, 绑定)
- **v0.1 核心 = pipeline + shell**, 策略类模块 = 接口 + 占位
- 每个策略模块必须: ✅ 清晰接口契约 · ✅ 最简占位实现 (规则 / 粗糙 LLM prompt / 手工皆可) · ✅ 单独可替换
- **差异化正确角度**: shell 形态 + 平台主次 + 记录深度, **不在策略准度**

### 红线 — never violated in any version (来自 L2R3 §5 + GPT L3R1 §5)
来自 L2R3 的 8 条 (这些是 **永远 no**, 不只是 v0.1 不做):
1. **不自动下单** — 永远保留最终决策权 (不留 hook, v0.1 / v∞ 都不做)
2. **不做期权 / 加密 / 高杠杆 / 日内** — 项目身份冲突, 不留接口
3. **不许"信号黑箱"** — 每次建议必须白话解释; 任何版本都不能跳过解释
4. **不做日推送焦虑机** — 频率上限永远不超 "每周 + event"
5. **不诱导高频交易** (Barber-Odean 铁律) — agent 默认偏向"不动 / 等确认", v∞ 不变
6. **防"学习假装发生"** — 3 个月可测的概念回答, 任何版本都要有此 check
7. **不单一咨询师路径依赖** — agent 永远追踪"按谁的 vs 按自己 vs 按模型"分布
8. **维护时间 ≤ 3 小时/周 (稳定期)** — 永远不允许工具吞噬主业

GPT L3R1 §5 补充的 2 条 (synthesizer 采纳, 升格为永久红线):
9. **不允许静默偏向某一路** — 冲突报告必须显式展示三泳道, **永远** 不能给默认优先级
10. **"等待 / 不动"必须是正式输出** — 永远不能被建模为失败状态

> **新协议要点**: 上述 10 条是 **永远 no**, 对应 v0.1 architecture 不该为它们留扩展点。下面每个 candidate 的 "Scope OUT (永远不做)" 章节会从这 10 条中挑出最 candidate-specific 的几条强调, 但全部 10 条对所有 candidate 都生效。

### ❓ items resolved by this menu
| ❓ item | Candidate A 的解法 | Candidate B | Candidate C |
|---|---|---|---|
| 冲突报告形态 | 混合式 (Telegram 叙事 + Web 轻矩阵) | **三列表 + 白话根因** (Web 主场) | 事件卡内嵌三路分歧片段 |
| "机制成立"可观察证据 | 流程证据 (4 周闭环) | 校准证据 (≥3 次"agent 阻止冲动"档案) + 学习证据 (≥7 概念可复述) | 事件证据 (≥2 次真 event 经过系统) |
| 咨询师 pipeline v0.1 边界 | PDF/文本 + 人工触发导入 | 同 A + 图片 OCR 入口 (为截图留后路) | 同 A + event 辅助源 (CME/TradingView public) |

### ❓ items STILL OPEN — 必须 human 亲自回答 (菜单无法替答)
以下是 L2R3-GPT §7 已列出的核心必答, 至今仍未精确落地。fork 进 L4 **之前** 最好先答:

1. **"稳定赚钱"的操作化定义** — intake 给了"年跑赢标普 2-5%", 但 v0.1 能观察到的是 proxy (例如 "≥3 次 agent 阻止冲动" vs "≥1 次真 event 不乱动"). 你要选哪个 proxy 当 v0.1 的 success anchor? (这决定了 A vs B vs C 的真实权重)
2. **GPT L3R2 §4 的核心问题 (第一层 axis)**: 你真正缺的是 "更多信息可见性" 还是 "更强自我约束"? — 这个答案决定信息壳 vs 承诺壳。
3. **Opus L3R2 §4 的核心问题 (第二层 axis)**: 回看最近两个月, 你最后悔的是 "错过机会" / "冲动乱动" / "event 前慌乱"? — 这个答案在第一层 axis 选定后细化为 A / B / C。
4. **L2R3-GPT §7 Q6 的动机二选一**: 你真想 "成为会投资的人" (需要持续摩擦 → B 更 fit), 还是想 "摆脱不知道该怎么办的焦虑" (需要清晰出口 → A 更 fit)? — 这个问题 intake 没问, 但会暗中决定 B 的 upkeep 能不能撑住。

菜单无法替答这 4 题, 但 **synthesizer 推荐 §会基于"证据 vs 直觉"的张力给出默认路径** — 见下文。

---

## 关键 tradeoff — 两个 axis 同时存在

本轮辩论最有价值的成果之一, 是双方在 L3R2 给出了 **两个不同的 axis**, 它们不冲突, 但层次不同:

### Axis 1 (GPT L3R2 · 基于 search 证据的 — **更根本**)

**信息壳 vs 承诺壳**

- **信息壳**: 把外部观点、事件、研究材料更好地映射到你的组合里, 减少"看了但没落地"。Candidate A / C 属于这一类。
- **承诺壳**: 把你每次动作前后的理由、分歧与结果沉淀下来, 减少"其实知道很多, 但临场还是乱动"。Candidate B 属于这一类。

**为什么 GPT 的 axis 更根本**: GPT 在 L3R2 做了 5 组 scope-reality search (Fiscal.ai / Koyfin / Aiera / Bridgewise StockWise / 雪球付费组合), 每一个现成产品都在做信息壳 — 覆盖更广、摘要更快、推荐更多、事件更全。**它们共同缺的**, 是一个把 "你自己的决定" 当核心对象的 personal shell。承诺壳是市场 uniquely 的空白 slice。信息壳则是拥挤赛道。

这一判断把"你需要信息还是约束"变成 **第一层问题**, 然后"哪种信息 / 哪种约束"才是第二层。

### Axis 2 (Opus L3R2 · 基于用户心理的 — **第二层**)

**v0.1 最该聚焦的 calibration 场景是哪一种?**

- **Candidate A (研究收件箱)** 回答 **noise → signal** (每周咨询师信息消化)
- **Candidate B (决策账本)** 回答 **impulse → discipline** (每次动手前的 pre-commit)
- **Candidate C (事件卡台)** 回答 **emotional reactivity → measured response** (event 前的冷静)

Opus 给了一条 human 可用的自测问题 (改写自 GPT L3R1 §6 Q4):

> 回看最近两个月, 你真正后悔的是 "错过机会" / "冲动乱动" / "event 前慌乱"?

- 后悔"错过机会" → A (补信息盲区)
- 后悔"冲动乱动" → B (pre-commit 档案 + 冲突报告)
- 后悔"event 前慌乱" → C (事件卡台)

### 两个 axis 如何组合成决策

**顺序**:
1. 先用 **GPT axis** 决定: 我要做信息壳还是承诺壳?
2. 若选承诺壳 → **B 是唯一候选**, Opus axis 不需要再走
3. 若选信息壳 → 再用 **Opus axis** 在 A (每周消化) 和 C (event 前) 之间细化

**如果两个 axis 答案冲突怎么办** — 比如 human 回看心理痛点是"错过机会"(倾向 A), 但理性上觉得"我其实是需要约束"(倾向 B):

→ **承诺壳 (B) 更值得做**, 因为市场空白性更有力, 证据也更硬。心理痛点可能被最显眼的"错过时刻"主导, 但 Barber-Odean 铁律 + L2 的 calibration-engine-first 洞见都在说: **更大的价值源在"减少乱动", 不在"更多命中"**。

但这也是 L2 verdict `unclear` 继续存在的地方 — 选 B 承担了 "我能坚持 < 30 秒录入 8 周" 这个自用工具最大风险。fork B 前做自我测试 (GPT §6 Q3) 不是可选项, 是硬前置。

---

## Candidate PRDs

### Candidate A · "研究收件箱" (信息壳, noise → signal calibration)

**建议 fork id**: `004-pA`
**Sources**: Opus L3R2 Refined A + GPT L3R2 Refined A (两侧 R2 收敛)

#### v0.1 in one paragraph
Telegram-first 周报驾驶舱。Human 每周日晚把咨询师 PDF/文本粘贴或上传 → agent 用 LLM 结构化成 `{方向, 关键标的, 置信度}` → 结合 30-50 只关注股 + 当前持仓快照 → 产出**错位矩阵** (咨询师强推而你轻仓的 / 咨询师谨慎而你重仓的) → Telegram 发周报 + 3 条可能决策 + 白话解释。Web UI 只做 research-viewer: 矩阵图、笔记 wiki、历史周报归档。**v0.1 没有完整的决策档案 / 月度回顾 / 事件日历**, 但 intake hard constraint #4 强制 v0.1 必含冲突报告 — A 用 "轻量混合式" (Telegram 叙事 + Web 简化卡) 实现, 不做完整三列表骨架。

#### User persona (同 L2 §1, 强调此候选的痛点)
ML PhD + 付费华语投顾订阅者 + 金融初级 + 三市场 30-50 股。**此候选假设的痛点**: "我其实有内容 (咨询师周报), 但没法快速把它落到自己的 30-50 只股票上。" 不是"我缺信息", 是"信息没落地"。

#### Core user stories
1. 每周日晚, human 粘贴咨询师 PDF → 2 分钟后 Telegram 收到周报 + 3 条可能决策 + 1 行白话解释
2. Web UI 打开错位矩阵, 一眼看到"咨询师看好的我轻仓 / 咨询师谨慎的我重仓"
3. 首次遇到"右侧布局"等术语时 agent 白话解释并自动存入笔记 wiki, 下次不重复解释
4. Telegram 里可以问 "TSM 本周咨询师怎么看", agent 白话回答 + 引用本周观点来源
5. 每条建议附**轻量冲突卡** (混合式: Telegram 用 1-2 句叙事 "咨询师强推 X, 占位规则模型弱看好 Y, 综合建议 Z"; Web 用简化两列对比) — 即使占位源弱, hard constraint #4 必须落地

#### Scope IN (v0.1)
- 咨询师周报 PDF/文本解析 pipeline (LLM prompt 占位)
- 错位矩阵算法 (规则 + 加权, 占位)
- Telegram bot 周报推送 + 简单对话
- 本地 Web UI: 矩阵图 + 持仓表 + 笔记 wiki + 历史周报归档
- 30-50 关注股录入 (JSON 或表单)
- 持仓快照录入 (手动 JSON, 不接券商)
- 个人金融笔记 wiki (自动去重)
- 策略模块占位接口 (`StrategyModule` IDL, 为后期插私有模型预留)
- **轻量混合冲突卡** (honor hard constraint #4 — 占位"私有"源 = 一条 SMA 简单规则或"LLM 无 context 独立判断")

#### Scope OUT (永远不做 — red line, v0.1 architecture 不留扩展点)
- ❌ **自动下单** (红线 #1) — 任何版本都保留最终决策权
- ❌ **期权 / 加密 / 高杠杆 / 日内** (红线 #2) — 项目身份冲突, 不接入此类标的的数据 / 信号
- ❌ **每日晨报或 push notification 高频化** (红线 #4) — 频率上限永远不破 "每周 + event"
- ❌ **隐藏式默认推荐** (红线 #9) — 即使 A 的冲突卡是轻量, 永远不能合并三路为一个"推荐"
- ❌ **"不动 / 等待"被建模为失败** (红线 #10) — UX 层永远把"不动"做成 first-class 输出

#### Phased roadmap (committed, 按阶段交付 — v0.1 architecture 必须留扩展点)

> 来源: L2 v2 report §4 Natural extensions。继承 L2 §4 的风险编号映射 (R-v0.2-* / R-v0.5-* / R-v1.0-* / R-v1.5-*)。
> 命名规则: 每项标注 **phase / 难度 (L/M/H) / 重要度 (L/M/H) / 对应 L2 §4 风险编号**。

##### v0.2 (NEXT, 1-3 个月内) — 详细描述
Candidate A 的 v0.2 核心是把 v0.1 已 deferred 的 "完整决策档案 + 冲突报告骨架" 补齐, 这样 A 在 6-8 周后可以**渐进升级到 B-like 形态**, 而不是被 v0.1 形态锁死。

1. **完整决策档案系统** · phase=v0.2 · 难度=M · 重要度=H · 风险=R-v0.5-1 (决策无反馈环) **[synthesizer-added: 因 A 的 v0.1 没做完整档案, 所以这一项实际是 A 特有的 v0.2 任务, 在 L2 §4 标准排期里属于 v0.5, 但 A 必须前置]**
   - **做什么**: 在每次 trade 前后强制 ≤ 30 秒表单, 含咨询师观点 / 占位模型信号 / agent 综合 / human 决定 / 1 行理由 / 环境快照 / 事后回看字段
   - **完成标准**: 8 周累积 ≥ 15 条档案; 单次录入实测 < 30 秒; "不动"作为一等输出可记录
   - **v0.1 已留位**: A 的 `StrategyModule` 接口已分离 "信号源 / 综合建议 / 决策记录" 三层, 决策记录层 v0.1 是 "笔记 wiki + 简单 log", v0.2 升级为完整档案表

2. **个人金融笔记 wiki 升级 (自动去重 + 主动复盘)** · phase=v0.2 · 难度=L · 重要度=M · 风险=R-v0.2-1 (重复解释 / 学习假装)
   - **做什么**: v0.1 只做"自动去重存储", v0.2 升级到 "每 3 个月让 human 自查能否复述 7 个核心概念", 不能复述时 agent 主动重新解释
   - **完成标准**: 第 3 个月触发首次自查, ≥ 7 个概念可独立复述 (≥ 70%)
   - **v0.1 已留位**: A 已实现笔记 wiki 数据结构 + 去重, v0.2 只需加 review trigger + 自查 UI

3. **自动化咨询师监控 (微信内容 fetch 自动化)** · phase=v0.2 · 难度=H · 重要度=H · 风险=R-v0.2-2 (咨询师信息断档)
   - **做什么**: 把现在的 Proxyman 手动 fetch 升级到半自动 pipeline (调度 + URL pattern 监控 + 失败告警), human 只需偶尔确认
   - **完成标准**: 连续 4 周自动获取无失败 + 失败时有 fallback 到人工
   - **v0.1 已留位**: A 的 PDF/文本输入接口 (`AdvisorContentInput`) 已抽象, v0.1 是 "human 粘贴"的实现, v0.2 加 "scheduled fetcher" 实现

4. **简单的私有模型 v1 (XGBoost + 技术指标)** · phase=v0.2 · 难度=H · 重要度=H · 风险=R-v0.2-3 (模型空转)
   - **做什么**: 把 v0.1 的占位"私有"源 (一条 SMA 规则) 升级为真 XGBoost 模型 + 技术指标特征
   - **完成标准**: 模型每日产生 30-50 只关注股的方向 + 置信度信号, 进入冲突卡的"私有模型"列
   - **v0.1 已留位**: A 的 `StrategyModule` IDL 已定义 `PrivateSignal { direction, confidence, reasoning }` 接口, 占位实现可整体替换

##### v0.5 (3-9 个月) — 一行摘要
- **Pre-mortem + post-mortem 完整保留** · phase=v0.5 · 难度=M · 重要度=H · 风险=R-v0.5-1 (决策无反馈环) — 决策档案的 pre/post 双侧机制完整化
- **多市场 cross-signal (美/港/A 关联)** · phase=v0.5 · 难度=H · 重要度=M · 风险=R-v0.5-2 (三市场脱节) — 半导体链 / 美元黄金中概等关联标的逻辑
- **事件日历主动推送 (FOMC/财报/非农)** · phase=v0.5 · 难度=M · 重要度=H · 风险=R-v0.5-3 (事件错过) — 注: 这是 Candidate C 在 v0.1 就做的, A 推迟到 v0.5

##### v1.0 (9-18 个月) — 一行摘要
- **私有模型 v2+ (backtest + 实盘对比)** · phase=v1.0 · 难度=H · 重要度=H · 风险=R-v1.0-1 (模型过拟合)
- **配偶可见度模块** · phase=v1.0 · 难度=L · 重要度=M (取决于 §7 Q10 答案) · 风险=R-v1.0-2 (家庭不可见)
- **模型 tutor 升级 ("你似乎在 X 情境下倾向于 Y 错误")** · phase=v1.0 · 难度=M · 重要度=H · 风险=R-v1.0-3 (用户金融素养停滞)

##### v1.5+ (长期, 不急) — 一行摘要
- **半自动化执行 (一键确认 + 必须 human 拍板)** · phase=v1.5 · 难度=H · 重要度=L · 风险=R-v1.5-1 (决策到执行延迟) — 红线 #1 永远不破: 必须 human 拍板
- **Paper trading sandbox (新策略真钱外测试)** · phase=v1.5 · 难度=M · 重要度=M · 风险=R-v1.5-2 (新策略无 sandbox)

#### Success looks like (observable in 4 周内)
- ✅ 连续 4 周周报闭环 (粘贴 → 矩阵 → Telegram 推送)
- ✅ 单次周报处理时间 ≤ 30 分钟
- ✅ 至少 1 次 "我没真读进去" 的 aha (人自己觉得)
- ✅ 维护时间 ≤ 2 小时/周 (优于红线)
- ✅ 冲突卡 (轻量) 在 4 周内出现 ≥ 4 次 — honor hard constraint #4 的 observable
- ⚠️ **不要求** 达到 2-5% alpha (样本不足), 要求"机制合理可口头描述"

#### 时间估算 (under 45-180 小时预算)
- **3-4 周, 60-100 小时**
- 置信度: **H**
- 主要不确定性: 微信小程序 PDF 格式多样, parsing 可能耗时; 但这是 v0.1 管道最窄关口, 先打穿有价值。

#### UX 优先级
- fast > feature-rich (v0.1 验证机制, 不打磨)
- research rigor > UI 精致 (矩阵图直接出 png 即可)
- Telegram 极简 (5 条消息以内解决 80% 使用)
- 本地 optimized > 云就绪

#### Biggest risk (非技术 / 产品级)
**机制太单薄, 4-6 周后 human 觉得"不够用所以不用"**。因为冲突卡是占位 (单一信号源 + 一条简单规则), agent 只是"更结构化的咨询师周报摘要"。**GPT L3R2 scope-reality 证据显示这条赛道饱和** (Fiscal.ai / Koyfin / Aiera / Bridgewise / 雪球付费都在做同类), 所以 A 即使做得好, 也有"**变成更好的研究终端, 而非更好的决策系统**"的结构性风险。

#### Scope-reality 验证结果
- 相似产品通常包括: watchlist / dashboard / earnings calendar / AI summary / transcripts (Fiscal.ai Pro, Koyfin Plus, Aiera, Bridgewise 都在这层)
- 此候选对比现成产品**切得更窄** (只做咨询师→组合映射, 不做广谱 research)
- 但也**没有独特空白**: 信息壳赛道 2026 年饱和度 H
- 引用可比: Fiscal.ai Pricing (`fiscal.ai/pricing`) · Koyfin Pricing (`koyfin.com/pricing`) · Aiera Platform (`aiera.com/platform`) · 雪球购买协议 (`xueqiu.com/law/buycube`)
- 净判断: **typical 信息壳 v0.1, 能跑起来但不独特**

#### 最适合的 human
"回看近两月, 最后悔的是 **明明看过咨询师内容, 却没转成组合动作**" — 你的痛点核心是信息落地摩擦, 不是压力下失控。

---

### Candidate B · "决策账本" (承诺壳, impulse → discipline calibration) — **synthesizer 推荐**

**建议 fork id**: `004-pB`
**Sources**: Opus L3R2 Refined B + GPT L3R2 Refined B (两侧 R2 强力收敛, scope-reality search 直接 validate)

#### v0.1 in one paragraph
Web-first + log-heavy 决策账本台。周报和 event 卡都仍然存在, 但它们是**入口**, 不是主角。v0.1 的核心是把每次 `动 / 不动 / 等待` 都沉淀成一条"决策档案": 咨询师观点 / 占位模型信号 / agent 综合建议 / 冲突报告 / human 最终决定 / 1 行理由 / 环境快照 / 事后回看字段。Web UI 是主场 (本地 localhost, 不追 polish), Telegram 只做提醒和入口。关键 UX 门槛: **单次决策录入 < 30 秒**, 否则退化为日志弃用工具。

#### User persona
同 L2 §1。**此候选假设的痛点**: "我知道很多, 但压力下不稳定, 临场乱动。" 不是"我信息不够", 是"我约束不够"。

#### Core user stories
1. Human 想加仓 TSM → Web UI 一个 ≤ 30 秒表单 → agent 拉出冲突报告 (咨询师 A / 占位"私有"源 B / agent 综合 C + 分歧根因) → human 选(按/不按/等待) + 1 行理由 → 档案入库 + 环境快照 (价格、持仓、当周咨询师观点)
2. 每周日 Web UI "本周档案 review": 本周做了几次 action (按 agent / 按自己 / 不动), 各自回报。**"不动"作为一等输出**, 不是失败状态
3. Web UI 冲突报告 tab (即使 v0.1 占位信号源弱, UI 骨架先立): 三列表 + 白话根因。占位源没话说时, 显式显示"暂无分歧", 不空屏尴尬
4. 每次术语解释自动进笔记 wiki, 下次出现时 agent **不重复解释** (防"学习假装"信号)
5. 8 周使用后能从档案中筛出 "3+ 次 如果没有 agent 我会操作但实际没动" 的决策 — 这是 calibration engine 真正起作用的 proxy

#### Scope IN (v0.1)
- 全部 Candidate A 的 IN (咨询师 pipeline + 错位矩阵 + Telegram + 笔记 wiki + 关注股/持仓录入)
- **决策档案系统** (表单 + 环境快照 + 事后字段)
- **冲突报告 UI** (Web 三列表 + Telegram 叙事版), 含白话根因
- **Devil's advocate 占位** (LLM 简单 prompt, 每次 action 前出一句反驳)
- **周度 + 月度 review 生成器**
- **学习检查机制** (每 3 个月列出重点概念, 自查能否解释)
- 策略模块占位接口 (同 A, 但冲突报告面上必须体现占位源的独立存在)

#### Scope OUT (永远不做 — red line, v0.1 architecture 不留扩展点)
- ❌ **自动下单** (红线 #1) — 决策档案永远要求 human 最终拍板, 不留 hook
- ❌ **期权 / 加密 / 高杠杆 / 日内** (红线 #2) — 项目身份冲突
- ❌ **隐藏式默认推荐** (红线 #9) — 三列冲突报告**永远** 不能合并; 即使 v∞ 的私有模型成熟, 三路也不能合并为一个"权威综合"
- ❌ **"不动 / 等待"被建模为失败** (红线 #10) — 月度 review 永远要把"不动"作为正向 outcome 数据点
- ❌ **决策档案静默"建议你高频"** (红线 #5 / Barber-Odean 铁律) — 永远不做"agent 周建议次数 KPI", 不诱导高频
- ❌ **跳过白话解释的"快速模式"** (红线 #3) — 任何版本都不能为了快削减解释

#### Phased roadmap (committed, 按阶段交付 — v0.1 architecture 必须留扩展点)

> 来源: L2 v2 report §4 Natural extensions。

##### v0.2 (NEXT, 1-3 个月内) — 详细描述

1. **个人金融笔记 wiki 升级 (主动复盘 + 概念健康度)** · phase=v0.2 · 难度=L · 重要度=M · 风险=R-v0.2-1 (重复解释 / 学习假装)
   - **做什么**: v0.1 已实现去重 + 自动收录, v0.2 加 "每 3 个月自查 7 个核心概念" + "agent 不再重复解释" 的 enforcement
   - **完成标准**: 第 3 个月触发首次自查, ≥ 7 概念独立复述 (≥ 70%); agent 在重复 query 时直接引用 wiki, 不再展开
   - **v0.1 已留位**: B 的笔记 wiki 已有 `concept_first_seen_at` 字段, v0.2 加 review trigger 即可

2. **自动化咨询师监控 (Proxyman 升级到自动化 pipeline)** · phase=v0.2 · 难度=H · 重要度=H · 风险=R-v0.2-2 (咨询师信息断档)
   - **做什么**: 半自动化 fetch + URL pattern 监控 + 失败告警 + 多模态接口预留
   - **完成标准**: 连续 4 周自动获取无失败; 失败时有人工 fallback
   - **v0.1 已留位**: B 的 `AdvisorContentInput` 接口已抽象 source / format / fetcher 三层, v0.1 是 "human 粘贴 + PDF parser", v0.2 加 "scheduled fetcher" 实现

3. **简单的私有模型 v1 (XGBoost + 技术指标)** · phase=v0.2 · 难度=H · 重要度=H · 风险=R-v0.2-3 (模型空转)
   - **做什么**: v0.1 占位 (一条 SMA 规则 / LLM "独立判断") 升级到真 XGBoost + 技术指标特征
   - **完成标准**: 模型每日产生 30-50 只关注股的方向 + 置信度; 进入冲突报告"私有模型"列, 不再是占位文字
   - **v0.1 已留位**: B 的冲突报告 UI 已有"私有模型"列 + `PrivateSignal` 接口, 整体替换占位实现即可

##### v0.5 (3-9 个月) — 一行摘要
- **Pre-mortem + post-mortem 双侧深化** · phase=v0.5 · 难度=M · 重要度=H · 风险=R-v0.5-1 — 决策档案的 pre/post 双侧从"基础字段"升到"提示性 pre-mortem 引导 + post-mortem 趋势聚合"
- **多市场 cross-signal (美/港/A 关联)** · phase=v0.5 · 难度=H · 重要度=M · 风险=R-v0.5-2 — cross-market 关联逻辑 (例如半导体链)
- **事件日历主动推送** · phase=v0.5 · 难度=M · 重要度=H · 风险=R-v0.5-3 — Candidate C 形态在 B 上叠加为子模块

##### v1.0 (9-18 个月) — 一行摘要
- **私有模型 v2+ (backtest + 实盘对比 + 主动挑战过拟合)** · phase=v1.0 · 难度=H · 重要度=H · 风险=R-v1.0-1
- **配偶可见度模块** · phase=v1.0 · 难度=L · 重要度=M (B 的决策档案天然配偶 friendly, 升级成本低) · 风险=R-v1.0-2
- **模型 tutor 升级 (基于 6 个月档案数据指出"你在 X 情境倾向 Y 错误")** · phase=v1.0 · 难度=M · 重要度=H · 风险=R-v1.0-3 — **B 的天然延续**: 决策档案积累就是 tutor 的训练数据

##### v1.5+ (长期, 不急) — 一行摘要
- **半自动化执行 (一键确认 + human 必拍板)** · phase=v1.5 · 难度=H · 重要度=L · 风险=R-v1.5-1 — 红线 #1 永远不破
- **Paper trading sandbox** · phase=v1.5 · 难度=M · 重要度=M · 风险=R-v1.5-2

#### Success looks like (observable in 8 周内)
- ✅ 5-6 周交付 v0.1
- ✅ **8 周使用后决策档案 ≥ 15 条**
- ✅ **≥ 3 次 "agent 阻止冲动动作" 的记录** (校准证据)
- ✅ **能复述 ≥ 7 条金融概念** (学习证据)
- ✅ **单次决策录入 < 30 秒** (search 验证的硬门槛 — 超过就弃用)
- ✅ **首周 onboarding ≤ 15 分钟完成** (74% onboarding rule)
- ✅ 维护时间 ≤ 3 小时/周 (红线硬约束)
- ⚠️ 同样不要求已达到 2-5% alpha, 但要求 "机制起作用的 proxy 可观察"

#### 时间估算 (under 45-180 小时预算)
- **5-6 周, 100-160 小时**
- 置信度: **M**
- 主要不确定性: "决策档案 + 冲突报告 UX" 比想象中花时间 — human 要**真的愿意每次打开记录**, UX 可能需要迭代 2-3 次; scope-reality 证据 (Decision Journal 官方自述 "74% 用户差 onboarding 后放弃") 提示 v0.1 就要把 "为什么 + 回看" 做得像**福利**不像**作业**。

#### UX 优先级
- 可复盘性 > 即时爽感
- 把"不动"当一等公民 (红线 #10 的产品体现)
- 解释质量 > 推送频率
- Web UI 每个 tab 第一屏 ≤ 5 秒看完 (避免"作业感")
- 档案录入 **一键默认 + 可扩展**, 不是强制长表单

#### Biggest risk (非技术 / 产品级)
**Upkeep 负担 — 录入 > 30 秒就死**。scope-reality 证据硬: Decision Journal app 官方文档自述 "需要用户总是记得 + 定期 review 导致多人弃用"; 研究显示 **74% 用户在差 onboarding 后放弃**; 金融 app 30 天留存仅 **4.6%**。如果 v0.1 没能把"为什么 + 回看"做成福利而非作业, B 会在 6-8 周内死掉。这是 B 最大也最具体的风险, 有明确失败信号 (连续 2 周档案 < 2 条 = 红色告警)。

**第二 risk**: L2 verdict `unclear` 的 tension — "稳定赚钱"承诺没被证据支持, 自用工具 **没有外部 forcing function**, 一旦 upkeep 断掉, 就没有付费用户退订这种市场信号来逼迫改进。这个风险只能通过 **v0.1 就观察自己 8 周行为** 来管理。

#### Scope-reality 验证结果
- 相似产品通常包括: 事后复盘工具 (TradersSync / TradesViz / Edgewonk) — 只做事后, 不做事前
- 此候选的独特 slice: **事前 pre-commit 决策 + 事后复盘双侧**
- GPT L3R2 search 5 项产品 (Fiscal.ai / Koyfin / Aiera / Bridgewise / 雪球付费) **全部做信息壳**, 无一做承诺壳
- 引用可比: TradersSync (`tradersync.com`) · TradesViz (`tradesviz.com`) · Edgewonk (`edgewonk.com`) · Decision Journal app (`decisionjournalapp.com`)
- 净判断: **独特定位, 无直接先例** — 双侧决策沉淀是 genuinely open slice

#### 最适合的 human
"回看近两月, 最后悔的是 **知道很多, 但还是在焦虑里乱动**" — 你的痛点核心是压力下的自我失控, 不是信息摩擦。**或者**: 你的动机是"成为会投资的人"(需要持续摩擦), 不是"摆脱不知道该怎么办"(只想要清晰出口)。

---

### Candidate C · "事件卡台" (信息壳偏事件层, event → measured response calibration)

**建议 fork id**: `004-pC`
**Sources**: Opus L3R2 Refined C + GPT L3R2 Refined C (两侧 R2 收敛, 有 scope-reality 降成本验证)

#### v0.1 in one paragraph
周报保留 (作为基线), 但 v0.1 的第一性体验是**重大事件前后的准备卡**。FOMC / 财报 / 重大异动来时, agent 立即推送 "受影响持仓 + 三路冲突报告 + 建议(多半是'不动' + 理由) + event 后记录链"。**public event 数据免费** (CME FedWatch + TradingView 公开指标), v0.1 实际只需做"事件→持仓映射"和"推送逻辑", 不用搭 event database。Web 与 Telegram 都重要, 但都服务于"事件前先想清楚"。

#### User persona
同 L2 §1, 特别对应 L2 §3 场景 B (FOMC 前两小时的保护)。**此候选假设的痛点**: "平时不太焦虑, 但一到重大事件前最容易犹豫或乱动。"

#### Core user stories
1. Event 前 24h Telegram 推送: "FOMC 明天, 你持仓 5 只利率敏感股合计 22%, 过去 4 次类似事件平均回撤 -1.8%, 建议不动, 理由 XXX"
2. Event 后 24h Telegram 推送: "FOMC 结果 X, 你昨天选了'不动', 实际回报 Y, 档案 updated"
3. Web UI "事件时间线": 所有经过的 event + 决策 + 事后结果放在一条时间线上, 每月末生成趋势图
4. 周报依然每周出, 但是"平日基线"而非"决策日"
5. 冲突报告在 event 卡里内嵌, 不单独成 tab (比 B 轻)

#### Scope IN (v0.1)
- Candidate B 的核心 IN (决策档案 + 冲突报告, 但简化版 — 只对 event 相关决策记档)
- **事件数据整合** (CME FedWatch + TradingView public 指标 + Yahoo 财报日历)
- **事件→持仓映射逻辑** (规则实现, 占位)
- **事件前后推送逻辑** (Telegram 主)
- **事件时间线 Web 视图**
- 基线周报 pipeline (同 A, 但简化, 不做完整错位矩阵)

#### Scope OUT (永远不做 — red line, v0.1 architecture 不留扩展点)
- ❌ **自动事件 response (event 触发自动下单)** (红线 #1) — event 卡永远只是"建议 + 等 human 确认", 不接 broker API
- ❌ **期权 / 加密 / 高杠杆 / 日内事件套利** (红线 #2) — event 卡永远不覆盖此类标的
- ❌ **event 触发的高频推送** (红线 #4) — 频率上限永远 "每周 + event", event 不会被滥用为"每日 event 流"
- ❌ **event 推送把"等待 / 不动"建模为失败** (红线 #10) — event 卡的默认 tone 永远是"沉稳, 多半不用动"
- ❌ **隐藏式 event 综合推荐** (红线 #9) — 即使 event 卡是 Telegram 短消息, 永远要显式列出三路分歧, 不能合并

#### Phased roadmap (committed, 按阶段交付 — v0.1 architecture 必须留扩展点)

> 来源: L2 v2 report §4 Natural extensions。注意: C 在 v0.1 已经把 L2 §4 v0.5 的 "事件日历主动推送" 提前实现, 因此 v0.5 phase 中此项不再列出。

##### v0.2 (NEXT, 1-3 个月内) — 详细描述

1. **完整决策档案系统 (从 event-only 扩到 daily decisions)** · phase=v0.2 · 难度=M · 重要度=H · 风险=R-v0.5-1 (决策无反馈环) **[synthesizer-added: C 的 v0.1 只对 event 决策记档, v0.2 必须扩到非 event 日常决策, 否则 calibration engine 不完整]**
   - **做什么**: 把 v0.1 的 "event 档案" 扩展为 "全量决策档案" (event + 周报触发 + 主动 trade), 字段统一, 时间线整合
   - **完成标准**: 8 周累积 ≥ 12 条档案 (含 ≥ 3 条 event + ≥ 6 条 weekly + ≥ 3 条主动)
   - **v0.1 已留位**: C 的 `DecisionRecord` 数据结构已支持 `trigger_type` 字段 (event / weekly / adhoc), v0.1 只填 event, v0.2 全开

2. **个人金融笔记 wiki + 概念健康度自查** · phase=v0.2 · 难度=L · 重要度=M · 风险=R-v0.2-1
   - **做什么**: v0.1 已有 wiki 雏形, v0.2 加 3 个月一次概念自查
   - **完成标准**: 第 3 个月自查 ≥ 7 概念可独立复述
   - **v0.1 已留位**: C 的笔记 wiki 已含 `concept_first_seen_at`

3. **自动化咨询师监控 (event 之外的非 event 内容也覆盖)** · phase=v0.2 · 难度=H · 重要度=H · 风险=R-v0.2-2
   - **做什么**: Proxyman 半自动 pipeline; v0.2 既覆盖 event-related 也覆盖 weekly 周报
   - **完成标准**: 连续 4 周自动 fetch 无失败
   - **v0.1 已留位**: C 的 `AdvisorContentInput` 接口已抽象 (与 A/B 同)

4. **简单的私有模型 v1 (XGBoost + 技术指标)** · phase=v0.2 · 难度=H · 重要度=H · 风险=R-v0.2-3
   - **做什么**: 占位升级到真模型, 进入 event 卡的"私有模型"列
   - **完成标准**: 模型每日 / 事件触发时产生信号
   - **v0.1 已留位**: C 的 event 卡 UI 已有"三路分歧"骨架, 私有模型列接口 ready

##### v0.5 (3-9 个月) — 一行摘要
- **Pre-mortem + post-mortem 完整深化** · phase=v0.5 · 难度=M · 重要度=H · 风险=R-v0.5-1 — 决策档案双侧深化, 与 B 的 v0.5 同形态
- **多市场 cross-signal** · phase=v0.5 · 难度=H · 重要度=M · 风险=R-v0.5-2 — 跨市场关联 (event 触发时尤其有用)
- ~~事件日历主动推送~~ — **C 的 v0.1 已实现, 此项 v0.5 不再列**

##### v1.0 (9-18 个月) — 一行摘要
- **私有模型 v2+ (backtest + 实盘对比)** · phase=v1.0 · 难度=H · 重要度=H · 风险=R-v1.0-1
- **配偶可见度模块** · phase=v1.0 · 难度=L · 重要度=M · 风险=R-v1.0-2
- **模型 tutor 升级** · phase=v1.0 · 难度=M · 重要度=H · 风险=R-v1.0-3

##### v1.5+ (长期, 不急) — 一行摘要
- **半自动化执行 (event-aware 一键确认)** · phase=v1.5 · 难度=H · 重要度=L · 风险=R-v1.5-1 — 红线 #1 永远不破
- **Paper trading sandbox (event 策略测试尤其有价值)** · phase=v1.5 · 难度=M · 重要度=M · 风险=R-v1.5-2

#### Success looks like (observable in 6 周内)
- ✅ 4-5 周交付
- ✅ Build 窗口内至少 2-4 次真实 event 经过系统
- ✅ 至少 1 次 "我本来会乱动但 agent 让我不动" 的记录
- ✅ 通知严格维持 "每周 + event" 边界
- ✅ human 能区分 "这次该动" 与 "这次只是焦虑"
- ⚠️ 不要求 alpha; 要求 event 决策模式能被观察

#### 时间估算 (under 45-180 小时预算)
- **4-5 周, 80-130 小时**
- 置信度: **M**
- **关键 scope-reality 降成本**: Opus L3R2 search 发现 event 数据可直接用 CME FedWatch / TradingView 公共源, 时间估算从 6-7 周下调到 4-5 周
- 主要不确定性: **3-6 周 build 窗口内 event 样本稀疏** — 4 次 FOMC 要全年才齐, 单月最多 1 次, 财报季能补但不均匀。fork C 前建议先查未来 4 周事件日历, 若 human 持仓相关 event ≤ 2 次, 选 C 不明智。

#### UX 优先级
- 关键时点清晰度 > 平时功能密度
- 节制提醒 > 覆盖一切 (红线 #4 的产品体现)
- 先保护不犯大错, 再追求多做动作 (Barber-Odean 铁律的产品体现)
- Event 前 tone **沉稳**: "你其实不用做什么" 是默认
- Event 后 tone **复盘**: 累积 "不动" 的实际回报数据

#### Biggest risk (非技术 / 产品级)
**Event 样本稀疏** — build 完那个月若恰好 event 少, 4-6 周后证据不够厚, human 会怀疑 "这条路对不对"。**配对 risk**: 若 event 多, 可能又超出 "每周 + event" 的节制上限, 或让 human 对 event 过敏感化, 走到 "看盘焦虑机" 红线 #4 的反面。

**第三 risk (信息壳共享)**: 事件研究赛道有 Aiera 等产品做得很厚 (但定位是 research speed, 不是 pre-commit), C 仍需非常窄的定位才能避免 "变成 Aiera-lite"。

#### Scope-reality 验证结果
- 相似产品通常包括: 事件研究终端 (Aiera) + 财报日历 (Yahoo / Seeking Alpha) + event-driven alert
- 此候选的独特 slice: 以 **personal 持仓为中心** 的 event → 决策 → 事后结果闭环
- 但赛道上 event 工具多, 个人视角是差异点但非全空白
- 引用可比: Aiera Platform (`aiera.com/platform`) · CME FedWatch (`cmegroup.com/markets/interest-rates/cme-fedwatch-tool.html`) · TradingView FOMC indicator
- 净判断: **typical + 新切法**, 不像 B 那样独特, 也不像 A 那样饱和

#### 最适合的 human
"回看近两月, 最后悔的是 **event 前慌乱调仓**" — 你的痛点集中在关键时点的情绪冲击, 平时反而稳定。

---

## Comparison matrix

| 维度 | A · 研究收件箱 | B · 决策账本 | C · 事件卡台 |
|---|---|---|---|
| **Axis 1 (GPT): 壳类型** | 信息壳 | **承诺壳** | 信息壳 (偏事件) |
| **Axis 2 (Opus): calibration 场景** | noise → signal | impulse → discipline | event → measured |
| v0.1 时间 | 3-4 周 / 60-100h | 5-6 周 / 100-160h | 4-5 周 / 80-130h |
| 平台主次 | Telegram-first | Web-first | 双平台 (event 均衡) |
| 记录深度 | 轻 (笔记 wiki 自动 + 轻量冲突卡) | **重 (决策档案 + 事后字段)** | 中 (仅 event 档案) |
| 冲突报告形态 | 轻量混合 | **三列表 + 白话根因** | event 卡内嵌 |
| 市场饱和度 | 高 (Fiscal/Koyfin/Aiera 等) | **极低 (唯一空白 slice)** | 中 (工具多, 个人视角少) |
| 置信度 | H | M | M |
| 最大风险 | "变成更好研究终端而非决策系统" | "录入 > 30 秒就死" (upkeep) | "event 样本稀疏" |
| Scope-reality fit | ✅ typical 信息壳 | ⚠ 独特, 无直接先例 | ✅ typical + 新切法 |
| 适合 Opus axis 回答 | 后悔"错过机会" | 后悔"冲动乱动" | 后悔"event 前慌乱" |
| 适合 GPT axis 回答 | "缺信息可见性" | "缺自我约束" | "event 前缺可见性" |
| 适合 L2R3-GPT Q6 动机 | "摆脱不知道该怎么办" | **"成为会投资的人"** | 介于两者之间 |
| 符合所有 hard 约束 | ✅ (轻量冲突卡 honor #4) | ✅ | ✅ |
| 符合所有红线 | ✅ | ✅ | ✅ |
| v0.2 phased 重点 | 补完整决策档案 (synth-added) | 笔记 wiki 自查 + 私有模型 v1 | 决策档案扩展到 non-event (synth-added) |
| 时间上限是否安全 (≤6 周) | ✅ 非常安全 | ✅ 贴近上限 | ✅ 安全 |

---

## Synthesizer recommendation

### 明确推荐: **Candidate B (决策账本)** 作为默认 fork

**推荐强度**: 中强 (不是无可动摇, 但证据明显收敛到 B)

**三个收敛证据**:

1. **GPT L3R2 的 scope-reality search 是 decisive 的**: 5 个主流产品 (Fiscal.ai / Koyfin / Aiera / Bridgewise / 雪球付费) 全部在做信息壳, 承诺壳 uniquely 空白。A 和 C 即使做得好, 都在拥挤赛道竞争 — 而 v0.1 是自用, 不需要跟市场竞争, 但这说明**市场没做承诺壳不是因为没市场, 是因为"个人决定当核心对象"这件事没人做好** — 它本身是个难 slice, 正好是 human 这个 hyper-niche self-use 的立足点。

2. **L2 v2 report 的核心洞见 "calibration engine first, action engine second" 直接指向 B**: L2 报告 §1 和 §5 整个结构都在论证 "减少乱动 > 更多命中", 红线 #6 直接硬写 "不诱导高频交易 (Barber-Odean 铁律)"。B 是唯一一个 **产品形态上就把 calibration engine 做成主场** 的候选 (档案 + 冲突报告 + "不动"作为一等公民)。A 和 C 都是 information-first 的再加一点档案, B 是 commitment-first 再服用信息。

3. **Barber-Odean 铁律 + AI 过度信任文献 (ScienceDirect 2024 + Springer 2026) 共同说明**: 个人投资者的最大价值源不是 "更准信号", 是 "更少乱动 + 更慢的 trust-build"。B 的决策档案机制直接是这两条的产品化 — 每次动手前显式 stop, 写理由, 回看。A / C 对这两条只有被动遵守, B 是主动实现。

### 推荐做法 (操作层)

**第一选择**: fork B 进 L4 PRD (`/fork 004 from-L3 candidate-B as 004-pB`)

但 **在 `/plan-start 004-pB` 之前**, human 先做 **3 件自我访谈** (总共需要 2-3 小时):

1. **连续 5 次尝试决策档案录入 (手工 paper + pen 模拟), 每次是否能 < 30 秒?** — 如果第 3 次就觉得烦, B 的 UX 要大幅降级, 或改 **"B-lite"** (砍掉冲突报告 + 月度 review, 保留档案 + 周度 review, 降到 4-5 周), 或改 A
2. **回答 L2R3-GPT §7 Q6**: 你真想 "成为会投资的人" 还是 "摆脱不知道该怎么办的焦虑"? — 如果诚实答案是后者, B 的 upkeep 撑不住, 改 A
3. **查未来 4 周事件日历, 数一下 human 持仓相关 event 数量** — 如果 ≥ 4 次, C 变得有吸引力 (样本充足), 可以考虑 F-Multi (fork B + C 并行)

### 如果你的自我测试结果偏离 B

- **结果 1 (录入 > 30 秒 or 动机是"摆脱焦虑")** → fork A (`/fork 004 from-L3 candidate-A as 004-pA`), 接受信息壳赛道饱和的竞争劣势 (但自用不怕竞争), 优势是时间短 + 风险低
- **结果 2 (未来 4 周 event ≥ 4 次 且心理痛点集中在 event)** → fork C 或 F-Multi B+C
- **结果 3 (三件事都偏 B 但仍犹豫)** → fork B, 但在 L4 spec 阶段设置 **2 周 kill switch**: 如果第 15 天决策档案 < 4 条, 降级为 B-lite 或切换 A

### 对 L2 verdict `unclear` 的诚实继承

**B 是最值得做的候选**, 但我不假装这个推荐解决了 "稳定赚钱" 承诺本身未被证据支持的问题。B 的价值证据 (双侧决策沉淀的独特性, Barber-Odean 的指向性) 支持 **"这个系统能帮你更少乱动 + 逐步学会判断"**, 但不支持 "它会稳定每年跑赢标普 2-5%"。这个 2-5% alpha 目标只能通过 **v0.1 → v0.5 → v1.0 的自用数据 incremental 验证** — 3-6 个月的档案积累才有微弱信号, 12 个月才有初步证据。

如果 human 的真实目标是 "**先把 calibration 机制搭对, 再看 alpha 是不是副产品**", B 是路径; 如果真实目标是 "**我要在 3-6 个月内看到 alpha 证据**", **这个目标和任何候选都不匹配**, 应该直接 [P] Park, 先独立回答 L2R3-GPT §7 Q1 的"稳定赚钱"精确定义。

---

## Honesty check — 菜单可能忽略的东西

这一节不是仪式性补全, 是 synthesizer 强制自查的诚实缺口。

1. **所有 candidate 都假设 human 会坚持 3-6 周持续投入 15-30 小时/周**, 但 L2R3 的个人信息学证据 (PMC 2017/2025) 显示 lapse 是常态。菜单的时间估算没有 penalty for motivation decay — 现实里第 2 周热情下降是普通事。B 的 5-6 周估算在这条下最脆弱。

2. **"稳定赚钱"承诺的 tension 没在任何单一 candidate 里被解决**, 只被延后到"v0.1 → v0.5 的自用数据 incremental 验证"。如果 human 对 "验证需要 6-12 个月" 这个时间尺度不能接受, 整个 idea 的 framing 需要重新谈 (Park 或回 L2)。

3. **多模态解析深度在 v0.1 全部降级为 "接口 + 占位"**, 但 intake 的 freeform note 明确提到 "我付费的投资分析师的建议通过微信小程序发给我, 有视频/音频/PDF/图文"。v0.1 只做 PDF/文本意味着 **human 仍需继续手动消化视频/音频那部分内容**。**新协议下这一项的归类**: 这是 **Phased roadmap 项 (v0.2+)** 而非 Scope OUT — 接口必须在 v0.1 留位 (`AdvisorContentInput` IDL 已为 audio / video format 预留 enum 值), v0.2+ 实现解析。所有三个 candidate 都把这一项纳入 v0.2 phased roadmap (虽然在上方 candidate 章节里没单独列出, 因为它和"自动化咨询师监控"高度耦合, 实际是同一项的细化)。

4. **"华语 + 三市场 + 30-50 股"的 exact intersection 让任何 scope-reality 搜索都有局限** — GPT 搜到的 Fiscal.ai / Koyfin / Aiera 是英文产品, 雪球付费是华语但不是个人可进化工具。真正可比的"ML PhD + 华语投顾订阅者 + 金融初级 + 自用"群体几乎无 public artifact 可对比。**菜单的 scope-reality 证据对信息壳赛道饱和度的判断可能偏紧**, 因为我们没找到专门做 "华语投顾订阅者 + personal shell" 的产品 — 如果有, 可能能落在 A 或 C 里填补。

5. **配偶可见度 (L2 §4 的 v1.0 扩展) 在所有 v0.1 candidate 里都没出现**, 但 L2R3-GPT Q10 特别问了 "配偶每周 > 1 次聊投资决策 = must-have v1.0"。如果这个答案是 yes, 某种程度上 B 的"决策档案"天然是配偶 friendly 的 (档案文本可读), A 和 C 反而偏 agent-only。这是 B 的隐藏加分项, 菜单没显式提。**新协议下归类**: 这是 v1.0 的 Phased roadmap 项 (R-v1.0-2), v0.1 不实现但 architecture 应预留 "decision_record 可导出为 human-readable summary" 的能力。

6. **没有 candidate 在 v0.1 就做"挑战模型过拟合"机制** (L2 红线 #2 相关 — 但严格说这条是 L2R3 §5 的另一条红线, 不在 10 条 red line 里, 因为 v0.1 没有真模型可过拟合)。**新协议下归类**: 这条对应 v1.0 的 R-v1.0-1 风险, v0.1 的 `PrivateSignal` 接口应预留 `validation_against_oos: optional` 字段, 给 v1.0 backtest 模块挂载用。

---

## Decision menu (for the human)

### [F] Fork B 进 L4 PRD (**synthesizer 强推**)
```
/fork 004 from-L3 candidate-B as 004-pB
/plan-start 004-pB
```
但先做 synthesizer §推荐做法 里的 3 件自我访谈。

### [F-Multi] Fork B + A 并行 (如果想同时验证信息壳的快速闭环)
```
/fork 004 from-L3 candidate-A as 004-pA
/fork 004 from-L3 candidate-B as 004-pB
/plan-start 004-pA  # 先起 A (短链, 3-4 周)
/plan-start 004-pB  # 稍后起 B
```
**适合**: 你无法在承诺壳和信息壳间早判, 且愿意 8-10 周 total 预算 (A 先做完再上 B, 或交错)。代价是 total 时间延长, 但 A 做完后 B 已经有 data 可验证冲突报告有没有意义。

### [F-Alt] Fork A 或 C 而非 B (如果你的 axis 回答偏向 A / C)
```
/fork 004 from-L3 candidate-A as 004-pA
/plan-start 004-pA
```
或:
```
/fork 004 from-L3 candidate-C as 004-pC
/plan-start 004-pC
```
**适合**: 你诚实回答 GPT axis 后偏信息壳, 或 Opus axis 后痛点明显不是"冲动乱动"。接受市场饱和 / 样本稀疏的对应风险。

### [R] Re-scope — 注入 moderator 指令再跑一轮
```
/scope-inject 004 "<你的 steering, 例如: 'B 的 < 30 秒录入我接受不了, 探索 B-lite 变体'>"
/scope-next 004
```
**适合**: 你读完菜单后有具体新约束想注入 (如 B-lite 变体; 或砍 Telegram 只做 Web; 或砍多平台只做 Telegram) — 让 L3 再跑一轮给你新 candidate。

### [B] Back to L2 — 读完菜单发现要重 explore
```
/status 004
# 然后用 /explore-inject 注入新 framing
```
**适合 (罕见)**: 读完菜单发现"这三个候选都不对, 我的 idea 其实是 [别的东西]", 需要回 L2 重 unpack。

### [P] Park — **synthesizer 对 verdict `unclear` 的兜底推荐**
```
/park 004
```
**适合**: 你读完菜单后意识到 L2R3-GPT §7 Q1-Q4 (尤其 Q1 "稳定赚钱"精确定义 + Q6 动机二选一) 还没在内心清晰答案。这些问题只需要一个下午的独立思考, 答完再回来 scope 会清晰 10 倍。Park 不是放弃, 所有 L1/L2/L3 artifacts 完整保留。

### [A] Abandon
```
/abandon 004
```
**不推荐**, 除非你读完菜单后确信 "我不是想要这个工具, 我其实想要 [别的]" — 那种情况下应该开一个新 idea 号重写, 不是 abandon 004。

---

## Fork log

- **2026-04-25T02:16:00Z** · Candidate B "决策账本" forked as `004-pB` · status: just-created · path: `discussion/004/004-pB/` · next: `/plan-start 004-pB` (来自旧版 v01 菜单, 保留)
- **2026-04-29T (本版 re-synth)** · 菜单按新协议重生成 (Scope OUT 拆分 + Phased roadmap 显式继承 L2 §4); Candidates 内容连续, 旧 fork (004-pB) 仍有效, 但其 PRD.md 应在下一次 sync 时按本菜单的 Scope OUT / Phased roadmap 双结构更新
- (Candidates A 和 C 仍在 menu 中未 fork, 可随时 `/fork 004 from-L3 candidate-A as 004-pA` 或 `candidate-C as 004-pC`)

---

## Synthesizer 的最后一句话

如果 human 读完这份菜单只能带走一句话, 请带走这一句:

> **B 是最值得做的 v0.1 候选 (承诺壳 + calibration-first, 市场 uniquely 空白), 但它的成功完全取决于你能不能把 "单次决策录入 < 30 秒" 这个 UX 门槛撑住 8 周。做 3 件自我访谈后再决定 fork — 如果撑不住, 降级 B-lite 或改 A, 诚实大于野心。**

新协议要点 (本版相对 v01 的关键差异):

- **Scope OUT 现在是真红线**: 仅列"永远不做"的项 (自动下单 / 期权 / 高频推送 / 隐藏式合并 等), v0.1 architecture 不留扩展点
- **所有"v0.5 / v1.0 / v1.5+"committed 工作 现在显式列入 Phased roadmap**, 继承 L2 §4 的风险编号映射, v0.1 architecture 必须留扩展点
- **v0.2 (NEXT) 详细描述, 其余阶段一行摘要** — 让 PRD 在 fork 后能直接读出"下一步是什么 + 凭什么 v0.1 已留位"
- **v0.5 的"事件日历主动推送"在 Candidate C 里被前置到 v0.1**, 因此 C 的 v0.5 phased roadmap 显式标注此项已交付, 不重复列
- **Candidate A 和 C 都新增了一个 synthesizer-added v0.2 项**: 完整决策档案, 因为 A/C 的 v0.1 都没做完整档案 (B 做了), 所以 A/C 必须把 "档案补齐"作为 v0.2 第一优先级, 否则他们渐进升级到 calibration-engine 的路径会断
