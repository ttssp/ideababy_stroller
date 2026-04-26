# Idea 004 · L3R1 · Opus 4.7 Max · Scope (no search)

**Timestamp**: 2026-04-24T13:33:37Z
**Inputs read**: L2 report (stage-L2-explore-004.md v2), L3R0-intake.md, L2 moderator-notes, scope-protocol
**Searches used**: NONE in this round
**Visibility**: did NOT read GPT-5.4's L3R1

---

## 0. How I read the intake

Human 已经清晰地把 v0.1 scope 定位成 **"管道 + 壳 (pipeline + shell), 策略类模块留占位 + 清晰接口"** 这一硬性原则。这把本来很纠结的几个 Unknowns (动手阈值 / 私有模型 / 多模态解析深度) 统一拉到了 "**占位, 后续迭代**" 这条线, 让 L3R1 可以专注在另一个层面: **shell 和 pipeline 本身到底覆盖多大**。

Hard constraints 我会严格 honor:
- 3-6 周交付 (预算 45-180 小时)
- Balanced core loop (但阈值是占位)
- Telegram + 本地 Web UI 双平台
- 每周 1 次 + event 频率
- 咨询师数据源 = 微信小程序多模态 (v0.1 只解 PDF/文本, 其余接口占位)
- 显式冲突报告必含
- 研究 rigor 优先于速度/UX/简单

Red lines 继承 L2R3 全部 8 条, 不重复陈述, 每个 Candidate 默认 honor。

**Candidate 差异化的真正维度** (按 intake 明确要求): 不在策略准度, 而在 **shell 形态 + pipeline 覆盖范围 + 占位的粗糙程度**。下面 3 个候选对应 **"v0.1 的 shell 有多宽"** 的三个档位:

- **Candidate A · 最小 Shell**: 一条 end-to-end 管道跑通, 验证 core loop 基本机制
- **Candidate B · 中等 Shell**: 管道 + 决策档案 + 冲突报告完整, v0.1 就是产品的"骨架"
- **Candidate C · 宽 Shell**: 再加事件日历 + 周度 review, 尽量把 L2 描绘的"有副驾驶日常"的样貌在 v0.1 先搭起来

---

## 1. Candidate A · "最小 Shell — 一条管道验证 core loop"

### v0.1 in one paragraph
用最小的 shell 跑通**一条端到端管道**: human 把本周咨询师周报的 PDF/文本**粘贴或放入指定目录** → agent 用 LLM 把它结构化成 `{方向, 关键标的, 置信度}` → 结合 human 预先录入的 30-50 只关注股持仓快照 → 产出一张**错位矩阵** (咨询师强推而你轻仓的, 咨询师谨慎而你重仓的) → 通过 Telegram 推送一份周报 + 一个 Web UI 页面显示矩阵图。**没有**事件触发, **没有**决策档案, **没有**冲突报告 (只有"咨询师观点 + 你持仓", 还没有私有模型, 也就没冲突可报)。

### 用户 persona
同 L2 §1: human 自己, 金融初级 ML PhD, 已订阅华语投顾。**Candidate A 假设 v0.1 阶段 human 还未建私有模型, 也未配冲突报告**, 只先验证 "能不能让咨询师周报真正落到自己的组合里"。

### Core user stories (3 条)
1. 作为 human, **每周日晚上**我把咨询师最新周报 PDF/文本投入系统, agent 在 5 分钟内给我一份结构化解读 + 错位矩阵图, 让我**看见自己这周没真正读进去的东西**。
2. 作为 human, 当我手动打开 Web UI, 能看到"错位矩阵" + "关注股按咨询师强度分层" 两个视图, **帮我想清楚本周要不要动**。
3. 作为 human, 我通过 Telegram 问 agent "TSM 本周咨询师怎么看?", 它用白话回我, 并**解释我不熟的术语** (第一次遇到"右侧布局"时 agent 讲一遍, 存进我的个人金融笔记, 下次不再重复)。

### Scope IN
- 咨询师周报 PDF/文本解析 (LLM prompt 简单实现, 占位)
- 错位矩阵算法 (规则实现, 简单加权)
- Telegram bot 周报推送 + 基本对话
- 本地 Web UI: 矩阵图 + 持仓表 + 金融笔记列表
- 30-50 股关注列表录入 (JSON 或简单表单)
- 持仓快照录入 (手动 JSON, 不接券商)
- 个人金融笔记 wiki (自动去重, agent 不重复解释)
- **策略模块占位**: 一个 `StrategyModule` 接口占位, 未来能插私有模型

### Scope OUT (explicit non-goals)
- ❌ **私有 ML 模型**: 接口占位, v0.5 才实现
- ❌ **冲突报告**: 因为只有一路信号 (咨询师), 没冲突
- ❌ **事件日历 / FOMC 预警**: v0.5
- ❌ **音频/视频解析**: 占位, 只做 PDF/文本
- ❌ **自动抓取**: human 继续手动 fetch 或粘贴
- ❌ **决策档案 / trade 前 pre-mortem**: v0.5
- ❌ **多市场 cross-signal**: v1.0

### Success looks like
- ✅ 3 周内跑通端到端 (手动粘贴 → 矩阵 → Telegram 推送)
- ✅ 连续 4 周的实际使用后, human 主观能答"咨询师周报第一次真的落到我组合里"
- ✅ 每周操作 (粘贴 + 读矩阵) 总时间 ≤ 15 分钟
- ✅ v0.1 stable 后, 维护时间 ≤ 2 小时/周 (优于红线 ≤ 3)
- ⚠️ **不**要求达到 2-5% alpha — 样本太少 (4-8 周) 不可验证, 但机制能被 human 口头描述为"合理"即可

### Time estimate 诚实版
**2-3 周** × 15-30 小时/周 = **30-90 小时**. 置信度: H。主要 risk 在微信小程序 PDF 格式多样, 可能 parsing 耗时超预期 — 但这是 v0.1 管道里最窄的关口, 值得先打穿。

### UX principles
- **fast > feature-rich**: v0.1 是验证机制不是打磨
- **research rigor > UI 精致**: 矩阵图可以 matplotlib 直接出 png, 不追 D3.js
- **本地 optimized > 云就绪**: localhost web + Telegram bot, 不配公网
- **接口 > 实现**: 每个占位模块的接口要先想清楚 (IDL-level), 实现可以最糙

### Biggest risk
**机制太单薄, 4 周后 human 觉得"不够用所以不用"**. 因为没冲突报告也没私有模型, agent 只是个"更结构化的咨询师周报摘要", **心理上的拉力可能撑不到 v0.5**。这是"最小 shell"的 inherent risk: 赢了就是极少浪费; 输了就是提前验证"这个方向不对"——本身也有价值, 但 human 情感上可能受挫。

---

## 2. Candidate B · "中等 Shell — 骨架完整, 策略全占位"

### v0.1 in one paragraph
v0.1 做出**"看起来已经是那个完整 agent"的骨架**: 咨询师管道 + 关注列表 + 持仓快照 + 错位矩阵 + **冲突报告** (即使 conflict source 有限, 也先把这个 UI 做起来 — human 自己手填第二种观点或 agent 用简单规则扮演"devil's advocate") + **决策档案** (每次 "加仓 / 减仓 / 不动" 都要 logging 一句理由) + Telegram 周报 + 本地 Web UI 覆盖矩阵 / 档案 / 笔记三个 tab。**私有模型接口 + 音频/视频接口都占位, 事件日历暂缓**。

### 用户 persona
同 Candidate A。

### Core user stories (5 条)
1. 每周日晚, human 投入新一期咨询师周报 → agent 输出错位矩阵 + "**本周 3 个可能的决策** (按咨询师观点和你持仓组合出来)" → human 选择一个, agent 扮演 devil's advocate (简单规则或 LLM prompt, 占位) 挑战一句, human 写下"我还要做 / 不要做"的理由, 档案存档。
2. 每次 human 想动手, 都先打开 Web UI 的"决策档案"tab 写一行理由 + 选 action, agent 存下本次环境快照 (价格 / 持仓 / 咨询师本周观点) — **哪怕占位得再糙, 决策留痕的 UX 先立住**。
3. 在 Telegram 上 human 可以问 "XYZ 我想加仓", agent 拉出: 咨询师最近对 XYZ 的观点 + 你持仓里 XYZ 当前占比 + 本月你关于 XYZ 写过的笔记 + **一个 mock 的 devil's advocate 反驳**. 给你三选一 (加/watch/不做), 记档。
4. Web UI 有一个 "冲突报告"页面, 即使 v0.1 的"私有模型"是占位 (比如一条简单 SMA-20 规则, 或 LLM 直接"如果让你独立看这个, 你会怎么想"), 也强制性 surface 一个 "咨询师 vs 占位模型 vs agent 综合建议" 的三列显示。即使此时三列常常重复或矛盾弱, **UI + 数据结构已经就位, 等真实私有模型接上即有意义**。
5. 每月第一个周日, agent 产出"本月决策回顾": 有多少次按建议 / 按自己 / 不动, 各自实际回报. 这是 calibration 最硬的 feedback loop, 哪怕只有 4 个月 data, 也能给 human 第一次"看见自己的模式"。

### Scope IN
- 全部 Candidate A 的 IN
- **决策档案** (每次 action 必 logging, 含环境快照)
- **冲突报告 UI + 数据结构** (3 列: 咨询师 / 占位"私有"源 / agent 综合). 占位源可以是一条 SMA 规则或"LLM 无 context 独立判断"
- **Devil's advocate 占位** (LLM 简单 prompt, 每次 action 前出一句反驳)
- **月度回顾生成器** (agent 基于决策档案产出)
- **Web UI 多 tab** (矩阵 / 档案 / 笔记 / 冲突 / 月回顾), 接口化组件方便 v0.2+ 扩展

### Scope OUT (explicit)
- ❌ 事件日历 / FOMC 预警 (v0.5)
- ❌ 私有模型真正实现 (接口占位, 规则或 LLM 扮演)
- ❌ 多市场 cross-signal (v1.0)
- ❌ 半自动化执行 (v1.5)
- ❌ 配偶视角 (v1.0)
- ❌ 音频/视频解析 (接口占位)

### Success looks like
- ✅ 5-6 周交付
- ✅ 8 周使用后 human 能从决策档案中数出: 本期写了 N 次 "pre-mortem 理由", 其中 M 次事后回看"理由不成立" → 这是 **calibration engine 真正开始工作的第一个信号**
- ✅ 冲突报告 UI 即使"冲突"不多 (因占位源弱), human 每周打开看一次, 说明 UX 已内化
- ✅ 月度回顾让 human 第一次用数字形式"看见自己冲动 vs 纪律的占比"

### Time estimate
**5-6 周** × 15-30 小时/周 = **75-180 小时**. 置信度: M。主要 risk 是"冲突报告 + 决策档案" 这两个部件的 UI/UX 比想象中花时间 (human 要**真的每天愿意打开记录**), 可能需要 UX 迭代 2-3 次。

### UX principles
- 骨架的"**占位感**"要老实, 不装 — 每个占位模块在 UI 上明确标注 "v0.1 占位, v0.X 升级"
- 决策档案**必须轻录入** (单次 < 30 秒), 否则走 Barber-Odean 风险反面也走 journal-弃用反面
- 冲突报告要允许"空冲突"状态不难看 (当占位源没话说时, 显式说 "暂无分歧")

### Biggest risk
**"冲突报告 + 决策档案"过早做可能收益稀薄**. 因为占位源弱, 冲突报告 v0.1 大概率"常常没东西可报"; 决策档案前 2 个月数据点太少, 月回顾意义有限. human 可能在 6-8 周后觉得 "这骨架挺好看, 但我没真用进去". — **但这是 shell 论的必然取舍**: 用骨架的完整性换初期的"单位有效功能密度低"。

---

## 3. Candidate C · "宽 Shell — 再加事件日历, 尽量贴近 L2 的'副驾驶日常'"

### v0.1 in one paragraph
在 Candidate B 的骨架基础上再加 **事件日历主动推送** (财报/FOMC/非农 - event 触发) + **每周末 review** (不只月度, 每周都做一次短 review). 尝试在 v0.1 就构建出 L2 §1 描绘的"6 个月熟练期"的最小节奏雏形: 每周 1 次周报 + 每周末 review + event 预警. 策略类模块继续全占位, 但是**"副驾驶日常"的节奏骨架最全**。

### 用户 persona
同上。

### Core user stories (5-7 条)
所有 Candidate B 的 stories, 加上:

6. human 在 Telegram 上收到 "**下周三 FOMC, 你持仓中对利率最敏感的 5 只合计 22%. 过去 4 次 FOMC 后 24 小时平均回撤 -1.8%. 建议: 不动**". — 即使这条消息的"过去 4 次 FOMC 回撤" 是事件规则的占位 (v0.1 只做最简单的 agent: 拉历史价格 + 固定窗口对比), 但 event → action 整条链路已跑通。
7. 每周六晚上 Web UI 自动生成"**本周 review**": 本周发生了什么 events, agent 建议了什么, human 做了什么, 回报如何 (一页图), 比月度更高频地校准直觉。

### Scope IN
- 全部 Candidate B 的 IN
- **事件日历源** (可以是 Yahoo Finance 或手动维护一份 watchlist-events, v0.1 占位)
- **事件触发的推送逻辑** (通常提前 24h, 关联到 human 持仓)
- **"past similar events" 分析占位** (拉历史 price data, 简单窗口对比, 规则实现)
- **每周 review 生成器** (除月度外)

### Scope OUT (explicit)
- ❌ 私有模型真正实现 (仍占位)
- ❌ 多市场 cross-signal (v1.0)
- ❌ 半自动化执行
- ❌ 配偶视角
- ❌ 音频/视频解析
- 但**事件日历是新 IN, 不再是 OUT**

### Success looks like
- ✅ 6 周满 (顶到 3-6 周交付上限)
- ✅ 首次用过一次 "event 来了 agent 推送了 + 我按建议不动 + 事后 review" 的完整 loop
- ✅ 6 周后 human 打开 Telegram 的次数 vs 自己手动打开交易 app 的次数比值变化 (目标: 前者增加)
- ⚠️ 每周 review + 月度 review 存在**内容稀释**风险 — 也是需要 monitor 的

### Time estimate
**6-7 周** × 15-30 小时/周 = **90-210 小时**. 置信度: L-M. **可能超出 3-6 周上限**, 需要 human 愿意把上限松到 7 周或牺牲某些子功能。事件日历的 "past similar events" 分析是新 rabbit hole, 规则实现看着简单但跑起来 edge case 多。

### UX principles
- 事件推送**必有明确价值**, 不能成为噪音: 推的每一条都关联到 human 至少一只持仓
- 每周 review 做到 **< 2 分钟读完**, 否则和月度 review 一起成为"仪式负担"
- 事件日历"过去 N 次"的统计即使占位, 也要**明显标注置信度低 / 只供参考** — 防 blind trust

### Biggest risk
**Scope 溢出 + 时间超限**. 再加上事件日历, 本来就抓好 Candidate B 骨架的 5-6 周, 变成 6-7 周, 还伴随 event 推送 edge case 带来的迭代需求。**如果 human 实际每周只 15 小时且不能扩**, Candidate C 几乎必定 delay 到 v0.2。但如果 human 每周都能 25-30 小时, 这条是最接近 "L2 描绘的 6 个月熟练期" 的首次同构起点, 心理激励最强。

---

## 4. Options for human's ❓ items

### ❓ "冲突报告"具体形态

因为策略类模块占位, v0.1 的冲突报告也是"占位形态", 但 UX 骨架可以先立起来。两种 format 对比:

- **Option 1 · 三列对照表** (适合 Web UI, Candidate B/C 默认): `[咨询师 | 占位模型 | agent 综合]` × `[方向 | 置信度 | 关键理由]`. 优点: 结构化、清晰、等私有模型上线无需改结构. 缺点: 三列相近时看起来"没啥冲突", 有点空。
- **Option 2 · 决策树叙事** (适合 Telegram, 纯文本): "咨询师说 A 因 X; 占位模型说 B 因 Y; 综合后我倾向 C. 核心分歧在 Z — 你的判断?" 更像 chatbot. 优点: 移动端自然. 缺点: 数据不结构化, v0.2+ 改版成本高。

**我的建议**: v0.1 两边都做 — Web UI 用三列表 (为未来储备), Telegram 用叙事 format (为当下体验). 成本仅 10-15 额外小时。

### ❓ v0.1 的"机制成立"可观察证据

自用单人不能 A/B 测, 但有可观察的 proxy:
- **Proxy A**: 4-8 周后能从决策档案中找到 ≥ 3 次 "如果没有 agent 我大概率会操作" 的不动决策 (calibration engine 真正起作用的信号)
- **Proxy B**: 个人金融笔记 wiki 里有 ≥ 10 条由 agent 首次解释的金融概念, 且 human 在 8 周后能独立复述其中 ≥ 7 条含义 (学习在真发生的信号)
- **Proxy C**: human 的每周使用时间曲线 (打开 agent 的次数) 稳定或缓升, 而不是"头一周兴奋后迅速衰减" (personal informatics lapse 的早期 warning)

这三个 proxy 建议在 Candidate 选定后写进 success 节。

---

## 5. Red lines I'd propose (if intake had left blank)

Intake 明确说"按 L2 红线推", L2R3 Opus §5 已列 8 条, 此处不复述, 只挑出在 L3 scope 决策层最硬的 3 条重申:

1. **每次 action 前, 至少有一行"为什么"** — 这是防学习假装的底线设计。决策档案没内容 = 系统失败。
2. **Agent 推送频率不超过"每周 1 次 + event"** — 防看盘焦虑机。Telegram 要做 notification muting (event 仅在市场时间内推)。
3. **策略模块绝对解耦** (intake 已明确, 但 L3 层强调): v0.1 不能因为赶时间就把"咨询师解析 → 矩阵生成 → 建议输出" 写成一条长函数. **3 周跑通也要拆接口**. 否则后期独立打磨的承诺破产, 整个 shell 论失去意义。

---

## 6. Questions that need real user interviews (L3 can't answer)

因为只有 1 个用户 = human 本人, 没有"访谈其他用户"可言。但有几件事 **human 自己要在动手前测一下**, 等于 "对自己做一次用户访谈":

1. **真拿 2 周的咨询师周报, 手动走一遍 core loop** — 在没有 agent 的情况下, human 能不能在 1 小时内把一周周报手动解析成"错位矩阵 + 3 个可能决策 + 1 行理由"? 如果能, v0.1 基本上只是自动化 + 记录的工具, 可以直接 Candidate B. 如果做不到, 说明 agent 要承担的解析脑力比想象大, 得先 Candidate A 验证 LLM parsing 质量够不够。

2. **真做 3 次决策档案** — 最近 3 次你想操作的 trade 前写下"加/减/不动 + 为什么 + 触发 trigger". 7 天后回看. 你愿意继续做吗? 如果做了 3 次就觉得烦, Candidate B/C 的决策档案 UX 要进一步加速 (< 15 秒一次, 比目前 30 秒更严)。

3. **真用 Proxyman fetch 2 周** — 现在的 Proxyman 手动路径是否稳定? 如果 2 周内有 1 次以上发生"URL 变了 / 格式变了 / 鉴权过期", 那么 v0.1 "咨询师 pipeline" 的输入端可靠性存疑 — 需要把"手动上传 (drag-and-drop PDF)"作为首选路径, Proxyman 作为 v0.2+ 的自动化改进。

这 3 次自我访谈只需总共 2-3 小时, 但能让 Candidate 选择更有把握。

---

## 总结

3 个 Candidate 代表 v0.1 shell 的三档, 都严格遵守"策略类模块占位 + 清晰接口"原则, 差异在 **shell 宽度**:

- **A (2-3 周, 最小)** — 只跑通 "咨询师周报 → 错位矩阵" 一条链. 最快验证, 但功能单薄, 情感激励弱。
- **B (5-6 周, 中等)** — 加上决策档案 + 冲突报告 + 月度回顾. "骨架完整, 等策略填肉". 最符合 intake 的 shell 论精神, 但占位内容稀薄期 (前 2 个月) 可能让 human 怀疑价值。
- **C (6-7 周, 宽)** — 加事件日历 + 周度 review. 最接近 L2 描绘的"副驾驶日常"雏形, 但最可能超出 3-6 周上限, 需要 human 15-30 小时上限的上半段。

**Key tradeoff axis** 从 Candidate 间看: **"v0.1 shell 的宽度 (节奏完整度)"** vs **"3-6 周时间预算的现实性"**。

Intake 优先级是"研究 rigor > 速度", 暗示 human 倾向更完整的骨架 (B 或 C), 但时间上限是硬约束 (3-6 周). 我的第一直觉推荐 **Candidate B**, 但最终由 GPT L3R2 + scope-synthesizer 的 scope-reality search 来决定。

---

**总字数**: ~3800 中文字
**自纪律**: 未做 web search; 未读 GPT L3R1; 未写技术栈/架构 (只在 "Web UI 可以 matplotlib 出 png" 这种 tradeoff 层级引用过大类工具, 没决定具体框架); 未下 "就选 B" 的结论, 留给 L3R2 scope-reality 验证。
