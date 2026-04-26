# L2 Explore Report · 004 · "个人可进化的投资副驾驶 + 金融教练 + 私有策略编织层"  (v2)

**Generated**: 2026-04-24T20:00:00+08:00
**Version**: v2 · 在 human 注入 binding moderator note 后重新合成 (v1 的"投资纪律层"framing 已被废弃)
**Source**: root proposal 004 → L1 已跑但 human 选择 [S] 跳过 fork,用原 proposal 直接进 L2
**Source rounds**:
- L2R1 (Opus + GPT, 旧 framing "投资纪律层")
- L2R2 (Opus + GPT, 旧 framing 下的交叉 + 搜索验证)
- **moderator-notes.md (2026-04-24T10:35Z · binding) — 新 framing 在此定义**
- L2R3-Opus (新 framing 下重新 unpack, R1 级别)
- L2R3-GPT (新 framing 下交叉 + 价值验证搜索, R2 级别,含 `unclear` 裁决)

**Searches run**: 10 次跨 15 个独立源 (L2R2 × 5 + L2R3 × 5)
**Moderator injections honored**: 1 (2026-04-24T10:35Z,binding)

---

## 如何阅读这份报告

- **这是一份 v2 synthesis**。v1 把 idea 读成"一个面向商业市场的投资纪律层",human 读完后发现那不是他想做的东西,于是注入了 binding moderator note 把 framing 彻底重塑,并跑了一轮 L2R3。本文档是在新 framing 下产生的权威版本,**v1 的商业化 / 付费意愿 / 抗付费流失 / "不承诺 alpha" 论述全部作废**。
- **关键 framing**:这是一个**纯私人自用工具**,不是 SaaS,不是产品,不是给任何其他用户用的。"用户 = human 自己一个人",目标是"做成一个能帮我稳定赚钱的助手,然后我自己一直用"。
- **最难听但最重要的一点**:新 framing 下 GPT 给出了 `unclear` 裁决——**不是说 idea 没价值,是说 "稳定赚钱" 这个 core promise 本身没被现有证据支撑**。这个裁决背后有硬证据 (Barber-Odean、AI 建议过度信任、金融教育元分析),不能回避。Human 读完本文档后如果仍要推进,理想状态是**先精确回答四个核心必答问题 (§7),再决定 L3 方向**。

---

## Executive summary

- **新 framing**:idea 从"投资纪律层"彻底重塑为 **"个人可进化的投资副驾驶 + 金融教练 + 私有策略编织层"三合一**。用户 = human 自己一个人,已付费订阅一位哥大背景华语投顾,覆盖美股/港股/A股 30-50 只,金融素养初级 (懂价值投资/打新,不懂期权/大部分技术指标),想在实战中学而不是先读 500 页教材。
- **GPT L2R3 裁决:unclear**。直译:"新 framing 的价值已被验证到值得探索,但最核心的 '稳定赚钱' 承诺,没被现有证据一起验证。" 原因:个人投资者交易频次与净回报负相关 (Barber-Odean 两组经典研究),AI 建议过度信任在金融情境被 2024/2026 两项研究直接证实,金融教育元分析显示知识改善强、行为改善弱。
- **最关键的结构性洞见 (L2R3 的 single biggest takeaway)**:**系统应该首先是 calibration engine,其次才是 action engine**。如果顺序反过来——先追求"更主动更具体地给建议"——它很可能把"稳定赚钱"变成"稳定放大错误"。这个顺序决定了整个 v0.1 的设计。
- **idea 本身的独特火花仍然真实**:把"外部付费顾问 + 私有 ML 模型 + 嵌入决策当下的金融教育 + 白话解释 + 错位矩阵"压成一个可行动视图,对"ML PhD + 华语投顾订阅者 + 金融初级 + 没时间系统学"这个非常具体的 user-of-one,确实构成了一个任何现成工具都不提供的 niche。
- **不是 novelty 问题,是 niche-self-use 问题**。"不商业化"反而解除了很多商业产品的枷锁 (合规、onboarding、抗付费流失都不需要考虑),但也立即引入了一个新的结构性失败风险:**单人系统没有外部 forcing function,个人信息学研究显示 lapse 才是常态**——死因不是赚不赚钱,是 upkeep 拖不动。

---

## 1. The idea, fully unpacked (新 framing 下)

### 用户画像:一个非常具体的人 (校正版)

**L2R1/R2 的旧画像 (已作废)**:"ML PhD + 付费订阅顾问 + 判断力强 + 只缺执行闭环。" 这个画像对"投资纪律层"成立,但对这一个人不成立。

**moderator-notes 校正后的真实画像**:一个 ML PhD 背景的中年技术人,**元能力强但金融是初级**——知道价值投资、打新这类概念,能看懂财报大结构,但不懂期权 / 大部分技术指标 / 大多衍生品机制。已经付费订阅了一位哥大背景的华语投顾 (每周策略 + 盘前盘后),可交易美股 / 港股 / A股,关注 30-50 只。能承受 20% 回撤,**没时间系统学金融** (主业是 CS 方向),愿意每年 $500 买数据。

这是一个在技术产品里**很少被精确服务的用户类型**:元能力超强但某领域新手。他不是小白 (robo-advisor 不适合他),也不是 practitioner (Bloomberg Terminal 对他溢出)。他学东西快,但他要**在实操中学**,他本能地拒绝"先读 500 页教材再开始"的路径。

### 没有这个副驾驶的日常

晚上 10 点,他刷完咨询师周报,看到"右侧布局半导体"。他有**观点 + 信息输入 + 交易能力**,但中间那一层——**把观点翻译成具体操作 + 知道为什么**——缺了:

- "右侧布局"具体是什么意思?等突破哪条均线?还是成交量确认?
- 30 只关注股里哪几只是半导体?TSM / NVDA / AMD / ASML / SMIC 的 trade 逻辑一样吗?
- 加仓多少合适?5%?10%?怎么换算成金额?
- 咨询师说的"右侧"是技术面的还是估值面的?

结果往往是三种失败:**凭感觉跟单** (没学到东西,且未必贴自己组合);**拖延查资料** (拖过了右侧点位);**完全不操作** (错过机会)。**这不是"信息不足"问题,是"翻译层缺失"问题**。

### 有了这个副驾驶的日常

晚上 10 点,他打开 agent。Agent 已经**主动做完了几件事** (不是等他问):

1. **监控并解析本周咨询师观点** — "本周核心三条:(a) 右侧布局半导体;(b) 谨慎港股消费;(c) 美元走弱利好黄金。"
2. **结合你的 30 只关注股** — "你关注列表里的半导体:TSM/NVDA/AMD/SMIC。按咨询师逻辑,TSM 和 AMD 当前技术面接近'右侧确认' (20 日均线站稳 + 成交量放大);NVDA 已 overshoot;SMIC 仍在左侧。**优先考虑 TSM 或 AMD**。"
3. **给出具体仓位建议** — "若采纳,建议 TSM 从当前 4.2% 加到 6%;半导体总暴露会到 18%,仍在你自定义的 25% 板块上限内。"
4. **白话教你为什么** — "'右侧布局'指股价已脱离底部并得到确认,通常看两个信号——20 日均线上方站稳 + 成交量放大。'左侧'相反,股价还在底部、未确认反转时入场,更便宜但风险更高。"
5. **私有模型交叉检验** — "你自建的动量模型今日信号:TSM +0.7 (中等看多),AMD +0.3 (弱看多)。模型和咨询师在 TSM 上共识,在 AMD 上你的模型弱于咨询师——可能你模型没纳入咨询师的某个行业叙事。"
6. **一个决策界面 + 档案留痕** — 三选一 (加仓/watch/不做),选完记录理由 + 环境快照。

他花 5 分钟决定,按了"加仓 TSM 到 6%"。**同时他学到了**:20 日均线 = 右侧信号之一,成交量放大 = 确认信号。这两条知识进了他的"个人金融笔记",agent 下次讲相关话题时不会重复解释。

### 30 秒 aha:第一次打开

Agent 不问他 API key,不让他连券商。先要三件东西:30-50 只关注股清单、咨询师最近 4 期周报文字/图、当前持仓板块大致分布。5 分钟录入。然后 agent 给他看一张**他从没真正看过的视图**——**错位矩阵**:

> "咨询师本月重点看好 AI 基础设施,你持仓在 AI 基础设施上只有 3% 暴露,远低于他的强度建议。咨询师谨慎消费,你持仓有 18% 消费股。上述'错位'里,有 60% 是你之前没意识到的 (即使你读了咨询师每一篇)。"

他的 aha 不是"AI 好厉害",是**一个认知刺痛**:"原来我一直在读,但我并没有真把咨询师的观点落到自己组合里。" 这种刺痛让他留下来。

### 6 个月熟练期

半年后,他的使用节奏稳定成:

- **早晨 5 分钟** — agent 推送"今日 3 件事需要关注 + 1 件事可能该动"
- **每周日 30 分钟** — review 本周决策,标记"按建议 / 按自己 / 不动"三类,计算各自回报
- **每月 1 次深调** — 调整私有模型参数
- **遇到 event** — 财报/FOMC/非农,提前 12 小时推送"这事对你哪些持仓有影响"

他开始**看见自己的进化轨迹**:
- 3 个月前 40% 的 trade 是"没想清楚就下单",现在降到 15%
- 掌握了 8-10 条技术指标的白话含义,能独立读懂大部分咨询师周报
- **6 个月后他真正得到的不是"投资变好了",是"他不再是投资新手了"**

### 核心结构性决策 (L2R3-GPT 的 single biggest insight)

如果被迫用一句话总结新 framing 的成败关键,是这句 (来自 GPT L2R3 §4):

> **"它首先是 calibration engine,其次才是 action engine。"**

- **Calibration engine** = 帮你判断什么时候该动、该不该动、该按谁的话动、不动的理由对不对。
- **Action engine** = 具体告诉你买什么、买多少、什么时候买。

**如果顺序反过来**——先追求"更主动、更具体、更频繁地给建议"——系统很可能把"稳定赚钱"变成"稳定放大错误"。Barber-Odean 两篇经典研究 (见 §6) 直接显示:个人投资者越频繁交易,净回报越差。Agent 如果把用户变得"更勤快更自信",这是**反向优化**。

**这一点是本轮 synthesis 的核心 takeaway**,它会直接影响 L3 scope 的每一个决策。

### 如果只有他一个人用 (不商业化)

- 不用考虑合规 → 可以直接给方向性建议、仓位建议,不用每页 disclaimer
- 不用考虑 scale → 可以用最贵的 LLM、最大的上下文、慢响应但更深分析
- 不用考虑多用户兼容 → 所有数据结构 / 私有模型为一人优化
- 不用考虑新手 onboarding → UX 可以 geek (Jupyter-style),不用 App Store 化
- 不用考虑"万一用户诉我" → agent 可大胆尝试,错了就改进下次

**但也失去了外部 forcing function**:没有付费用户会用退订投票,没有 PMF 压力推迟改进。**6-18 个月后停用 (个人信息学研究称 "lapse") 是自用工具最大失败模式**。

---

## 2. Novelty assessment (新 framing 下)

### 诚实判定:**Hyper-niche self-use · not novelty**

- "ML PhD 用 AI 做自用量化工具"这件事 **在 quant 圈并不新**。GitHub 有成千上万个人项目,有些还用 LLM 做周报监控。
- "把顾问观点翻译成个人化操作"这件事 **在财富管理行业 hybrid advice 里也在发生** (Vanguard Hybrid, Schwab Intelligent, Betterment Premium)。
- QuantConnect 的 Jupyter-based research environment (L2R3-GPT 找到的 prior art) 直接证明"user 即 developer"形态已经存在——但也仅证明形态可以成立,**不证明它会稳定赚钱**。

纯 novelty 压缩下来是:**"ML PhD + 华语投顾订阅者 + 金融初级 + 三市场 + 不商业化"这个 exact intersection**。全中国这样的人可能几万个。**这不是 novelty,是 hyper-niche self-use**。

### 但这不是坏消息

**个人项目的意义不需要 novelty 来合法化**。它不需要是新的,它只需要**对这一个人有用**。真正 novel 的那一小块,是"把嵌入决策当下的金融教育 + 私有模型 + 外部顾问翻译压成一个可行动视图"——这个 slice 对**这一个具体的人**有用,够了。

不需要为不存在的商业问题辩护 novelty 的合法性。v1 synthesis 把这件事讲成一个市场切片,是方向错的。

---

## 3. Utility — 具体使用场景 (新 framing 下,3 个)

### 场景 A · 周一晚 10 点:咨询师说"右侧布局半导体",他第一次不是凭感觉操作

已在 §1 展开。关键**情感 outcome**:他对妻子说晚饭时——"**这个工具让我感觉自己不是瞎买**。"

这是他半年订阅费第一次被真正兑现。价值不在"多赚了多少",在"第一次感觉自己在根据 validated reasoning 做决策,而不是跟 Tips"。

### 场景 B · 周三下午 2 点:FOMC 前两小时的保护

他在会议间隙打开 agent。Agent 弹出:

> "2 小时后 FOMC 决议。你持仓中对利率最敏感的 5 只 (消费、小盘、地产 ETF) 合计 22%。过去 4 次 FOMC 后 24 小时,这类标的平均回撤 -1.8%。你上次在类似场景 (2026-01 FOMC) 选择了不动,事后 3 天内 +0.5%。**本次建议:不动,保留观察**。若决议鹰派,明日开盘 -2% 是你的止损或加仓 trigger——你上次设的是 stop-out,要不要改成 opportunistic buy?"

他意识到自己过去三次都在 FOMC 前慌张调仓,三次都吃亏。这次他选"不动 + -2% 加仓 trigger"。FOMC 没那么鸽也没那么鹰,没触发,他赢了 0.3%。

关键**情感 outcome**:他意识到——**agent 在把他自己的历史行为变成他自己的教材**。这比任何网课都更 personal。

**这个场景直接对应 §1 的核心洞见**:这里 agent 是 calibration engine (建议不动),不是 action engine (建议买卖)。这才是它真正的杠杆点。

### 场景 C · 6 个月周日晚:看见自己的进化曲线

打开"半年 review":

- 本期 38 个决策:27 个按 agent 建议,7 个按自己判断 (和 agent 分歧),4 个完全自己决定
- 按 agent 建议 27 个里:21 个正向 (+4.2%)
- 按自己判断 7 个里:3 个正向 (-0.8% 净)
- 完全自己决定 4 个:2 个正向 (+0.3% 净)
- 私有模型 v3 vs v1,胜率从 54% 升到 61%
- 最大学习:"我单独做决策比跟 agent 合作差 4%,但差别在**没耐心等确认**,不在方向看错。下半年我设一个规则——想偏离 agent 建议前,先写 3 句话理由,24 小时后再决定。"

关键**情感 outcome**:**"我变成了一个真的会投资的人,而且还在变好。"** 不是"我变富了",是"我变成了"。

---

## 4. Natural extensions (新 framing 下)

**原则**:每一项扩展都要对应解决一条红线或风险,否则就是功能堆砌。

### v0.2 (1-3 个月内) — 对应风险:重复解释 / 咨询师信息断档 / 模型空转
- **个人金融笔记 wiki** — 每次 agent 解释的新概念存进他自己的 wiki,agent 下次不重复解释 → 防"学习假装发生" (用户仍在问同一个概念 = 系统失败信号)
- **自动化咨询师监控** — 自动 parse 他的微信订阅,结构化 (模型 → 方向 → 标的 → 置信度) → 防"咨询师观点覆盖不全导致 agent 失去 anchor"
- **简单的私有模型 v1** — XGBoost + 技术指标特征 → 让 ML PhD 这一面能力真正进入系统,不做这一步等于工具少了半个大脑

### v0.5 (3-9 个月) — 对应风险:决策无反馈环 / 三市场脱节 / 事件错过
- **Pre-mortem + post-mortem 保留** — 旧 L2R1 的核心 loop 继承,但降格为子系统
- **多市场 cross-signal** — 美/港/A 的 cross-market 关联 (半导体链、美元/黄金/中概)
- **事件日历主动推送** — 财报/FOMC/非农 → 防"漏事件导致系统感 -1"

### v1.0 (9-18 个月) — 对应风险:模型过拟合 / 家庭不可见 / 用户金融素养停滞
- **私有模型 v2+** — backtest + 实盘对比环境,agent 主动挑战模型过拟合
- **配偶可见度模块 (可选)** — 简化版展示"家庭财务健康 + 最近决策理由",不用学金融术语
- **模型 tutor 升级** — 基于 6 个月决策样本,主动指出"你似乎在 [某种情境] 下倾向于 [某种错误]"——从"教金融概念"升级到"教他自己"

### v1.5+ (长期,不急) — 对应风险:决策到执行延迟 / 新策略没有 sandbox
- **半自动化执行** (仍需确认) — 事件触发时 agent 预先起草 order,一键确认
- **Paper trading 测试新策略** — 真钱外维护模拟账户,新想法先跑 1-3 个月

---

## 5. Natural limits & 新红线

### 继承的限制 (旧 framing 下仍适用)

- 不做期权、加密、高杠杆、日内交易 (用户不懂、不感兴趣、违背稳健目标)
- 不自动下单 (用户保留最终决策权,心理舒适度 + 学习路径需要)
- 不 global,聚焦三市场 (美/港/A) + 华语输入 + 30-50 stocks

### 新 framing 下需要的**新红线** (直接回应 GPT L2R3 的 pushback)

这一节是 §5 最重要的部分,也是整个 v2 synthesis 相对 v1 最大的新增。

1. **不许变"信号黑箱"** — 每次建议强制白话解释。如果某天他不再读解释直接按,产品在悄悄失败。需定期测验 (3 个月问一次"这 10 个金融概念你能解释吗"),确保金融素养真在涨。
2. **不许私有模型过拟合** — ML PhD 最容易的错是把自己的测试集当 gospel。Agent 必须 **主动挑战** 模型:"你这个模型过去 3 个月在 [某情景] 表现反常,要不要 retrain?"
3. **不许路径依赖咨询师** — 那位哥大顾问是重要 input,不是 gospel。Agent 必须追踪"你按咨询师 vs 按自己 vs 按模型的结果",让他看清哪一路是真 edge、哪一路只是 anchor。
4. **不许变"看盘焦虑机"** — 主动通知严格节制:**上限为每日 1 次晨报 + 每周 1 次周报 + event 前 1 次**。目的是让他**更少焦虑**,不是更多。
5. **不许淹没主业** — 他的主业不是金融。工具维护时间 ≤ 3 小时/周 (实际使用时间不限)。如果突破这个上限,系统对整体生活就是负的。
6. **【关键新红线】不许变"更高频动手机器"** — **Barber-Odean 铁律**:交易越多净回报越差。Agent 默认偏向"不动 / 等确认"。每周 agent 可以建议 ≥5 次"什么都别做",不能变成每天都有"该操作的标的"。
7. **【关键新红线】不许学习假装发生** — 3 个月后如果用户仍解释不清关键指标,**这就是系统失败信号**,不是 "用户还在学习中"。

### 取消的限制 (v1 的商业枷锁,新 framing 不再约束)

- ~~"不承诺 alpha"~~ → 自用可以有稳定赚钱目标
- ~~"不给具体仓位建议"~~ → 自用可以给
- ~~"必须 mass-market UX"~~ → 可以 Jupyter-style geek
- ~~"必须抗付费流失"~~ → 无付费用户
- ~~"特定文化 slice 是弱点"~~ → 自用反而是优势
- ~~"必须不滑成荐股工具"~~ → 自用工具就是要给具体建议

**注意**:这些限制的取消不代表"怎么都行"。它们被**新红线 (尤其是 #6 和 #7) 替代**——自用不用合规枷锁,但需要更严的"保护自己"机制。

---

## 6. Validation status

### 先验品 landscape (prior art)

| Name | Status | What it does | Lesson for us | URL |
|---|---|---|---|---|
| Vanguard Hybrid / Schwab Intelligent / Betterment Premium | 活跃 | 顾问 + AI 混合;AI 做分析/效率,人做 behavioral coaching | "顾问 + AI 放大"结构在商业端已发生;自用版可借用 architecture,不抄商业定位 | [Vanguard](https://advisors.vanguard.com/advisors-alpha) |
| QuantConnect (Jupyter research env) | 活跃 | 研究环境即 notebook,项目代码 / 模型训练 / 回测串起来 | "user 即 developer"形态有官方先例;证明形态可成立,不证明会赚钱 | [QuantConnect](https://www.quantconnect.com/docs/v2/research-environment/key-concepts/research-engine?ref=v1) |
| 雪球 / 富途 / 长桥 / 同花顺 (华语三市场 app) | 活跃 | 行情 + 社区 + AI 诊股 + 选股 | 分析 lane 拥挤;"私有模型 + 决策档案 + 嵌入式教育"lane 几乎空白 | 多 URL (见 L2R2-GPT) |
| IPS / 书面投资计划 | 长期存在 | 行为金融标配工具 | 不是发明新工具,是给被证明有效的工具去掉摩擦 | [Bogleheads](https://www.bogleheads.org/wiki/Investment_policy_statement) |
| TradeZella / TraderSync / Edgewonk | 活跃但高弃用 | 交易日志 | 金融 app 30 天留存 **4.6%**;失败模式真实 | [TradeZella](https://www.tradezella.com/blog/trading-journal-complete-guide) |
| GitHub 开源 LLM 多市场分析器 (e.g. `daily_stock_analysis`) | 活跃 | LLM 驱动 A/H/US 多市场分析 + 新闻 + 多数据源 + 多渠道推送 | 同形态免费开源方案存在;差异化必须在"决策纪律 + 嵌入教育",不在"分析/信号" | [GitHub](https://github.com/ZhuLinsen/daily_stock_analysis) |

### 需求信号 (demand signals)

| Source | Signal | Strength | URL |
|---|---|---|---|
| Janus Henderson 2024 Survey | 88% 投资者想提升知识,超三分之一把权益挪到现金/固收 | H (但:证明的是"想学"不是"想用这个具体工具") | [Janus](https://www.janushenderson.com/en-us/advisor/article/investor-survey-short-term-concerns-overshadowing-long-term-goals/) |
| Vanguard Advisor's Alpha | 把 behavioral coaching 定义为 advisor 最大潜在价值 | M (工业端信号,自用转译需当心) | [Vanguard](https://advisors.vanguard.com/advisors-alpha) |
| World Bank + NBER meta-analysis | 金融教育对知识有正效应,对**行为**改善弱得多 | H (对 idea 来说是警告信号,不是支持信号) | [World Bank](https://openknowledge.worldbank.org/items/a5264ed9-36d6-5507-95fc-014951964b40) / [NBER](https://www.nber.org/papers/w27057) |

### Failure cases (最关键的部分)

| Name / Study | Status | Why it died / What it showed | Avoidance for us | URL |
|---|---|---|---|---|
| **Barber & Odean "Trading is Hazardous to Your Wealth"** | 经典文献 | **个人投资者越频繁交易,净回报越差;最活跃组显著落后** | **直接结构性威胁**:如果 agent 让用户"更勤快",它就在反向优化。系统必须偏向"不动"。 | [Berkeley Haas](https://faculty.haas.berkeley.edu/odean/papers/returns/returns.html) |
| **Barber et al. RFS 2009 (Taiwan Full-Market)** | 经典文献 | 台湾全市场交易史:个人投资者交易带来**系统性、经济意义很大的**损失 | 强化 Barber-Odean 铁律的全市场证据 | [RFS 2009](https://academic.oup.com/rfs/article/22/2/609/1595677) |
| **AI advice overreliance (ScienceDirect 2024)** | 实验研究 | 人在**财务风险情境**里对 AI 建议产生过度依赖 | 白话解释不是 nice-to-have,是**保护栏**。不解释 = 默认滑向 blind trust。 | [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0747563224002206) |
| **Explainability in financial AI (Springer 2026)** | 金融场景研究 | 低 explainability 把用户推向 trust heuristic,放大 blind trust | 每个建议必须带"为什么";任何一次跳过解释都是系统失败的前兆 | [Springer](https://link.springer.com/article/10.1007/s10796-026-10727-1) |
| **Personal Informatics Lapse (PMC 2017)** | 研究综述 | 自我追踪 (finance/健康/位置) 工具里 **lapse 是常态**;死因是 upkeep、忘记、整合麻烦、兴趣退潮 | **"纯自用"≠"容易活久"**。死因不是赚不赚钱,是 upkeep 拖不动。 | [PMC 2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5428074/) |
| **Personal Informatics Lapse (PMC 2025)** | 最新研究 | 有些停止不是失败,是"目标变了/学够了";但 upkeep 型 lapse 仍是主要死因 | 可接受的退出条件要早想清楚 (什么时候放下是胜利?) | [PMC 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12435389/) |
| **Trading journal 30-day retention 4.6%** (from L2R2) | 产业数据 | 金融 app 30 天留存 4.6%,比新闻/购物都低 | 录入 ≤3 分钟 + 自动串联复盘是 day-1 门槛,不是"优化项" | [Devexperts](https://devexperts.com/blog/trading-apps-to-increase-user-retention-rates/) |
| **Financial education meta-analysis (World Bank)** | 元分析 | "边做边学"知识可学到;**行为**改善弱得多 | 不能假设"嵌入式学习自动把人变成熟手"。必须主动测验。 | [World Bank](https://openknowledge.worldbank.org/items/a5264ed9-36d6-5507-95fc-014951964b40) |
| **Financial education behavior gap (NBER w27057)** | 元分析 | 金融教育 intervention 效果强弱高度依赖 teachable moment + 贴近真实决策 | 支持"嵌入决策当下的教育"方向;但行为改变本身不会自动发生 | [NBER](https://www.nber.org/papers/w27057) |

### Net verdict

**Should this exist? `unclear`**

(沿用 GPT L2R3 裁决,synthesizer 不做外交润色)

### 展开解释

**不是说 idea 没价值**。新 framing 的确让 idea 变得比旧版更有火花——它不再是"投资纪律层",而是一个贴着真实仓位运行的私人系统:一边把付费顾问、市场叙事、私有模型编织成建议,一边在建议发生的当下把金融语言翻译成可被学会的白话。对"ML 很强但金融初级、又没空系统学"的这一个用户,这确实有真实吸引力。

**但证据同样清楚地指出三个结构性张力**:

1. **"稳定赚钱"承诺没被证据支持**。Barber-Odean 的铁律是"个人投资者越频繁交易净回报越差"。一旦 agent 把自己理解成"更主动、更自信、更具体地替你出手",它就踩在最危险的地带。
2. **"边做边学"不自动发生**。金融教育元分析显示行为改善远弱于知识改善。如果系统只让你按按钮,你可能是在**外包判断**,不是在学习。
3. **"纯自用 ≠ 容易活久"**。个人信息学研究显示 lapse 才是常态,死因是 upkeep——不是赚不赚钱。

### Verdict 的精确措辞 (from L2R3-GPT)

> **不是说 idea 没价值,是说新 framing 里最核心的"稳定赚钱"承诺本身没被现有证据验证。证据支持"这个系统可以帮你更少乱动 + 逐步学会判断",但远不支持"已经有充分世界证据说它会稳定赚钱"。**
>
> **最值得继续探索的不是"AI 替我找 alpha",是"它能不能把外部顾问、私有模型、白话解释压成一个更少犯错的决策时刻"**。

这句话是整个 v2 synthesis 的 single most important sentence。它同时否定了"更 active 的 action engine"路径,并肯定了"更准确的 calibration engine"路径。它也是 §1 和 §5 的所有红线设计背后的那条主线。

---

## 7. Open questions for L3 / 动手前 human 必答问题

### 来自 L2R3-GPT §5 的四个核心必答

| # | Question | Best answered by | Why it matters |
|---|---|---|---|
| 1 | **"稳定赚钱"到底什么意思?**跑赢现金?大盘?减少大亏?减少冲动交易? | Human 独立思考,不借外力 | 定义不精确,系统只会优化情绪不优化判断。这是整个 idea 成败的第一块石头。 |
| 2 | 咨询师观点 vs 私有模型 vs agent 综合建议三路冲突时,**哪一路优先?** | Human 独立思考 (L3 无法外包) | 没有内在 hierarchy = 系统制造更高级的困惑,不减少困惑。 |
| 3 | agent 主动程度:每日/每周/仅事件?**是否允许"本周什么都别做"?** | Human 独立思考 + 实战 1 个月校准 | 这直接决定系统是 calibration engine 还是 action engine。错了就是反向优化。 |
| 4 | 如何判断"在学习"vs"在外包大脑"? | Human 独立思考 + 设定可测指标 | 3 个月测不出 = 系统已开始失败。需要 ex ante 定义评估方法。 |

### 来自 L2R3-GPT §6 的三个情绪面问题

| # | Question | Best answered by | Why it matters |
|---|---|---|---|
| 5 | 连续两次建议都亏钱后,能冷静区分"市场噪声 / 系统缺陷 / 自己没按规则"三者吗? | Human 独立思考 + 配偶/朋友外部校验 | 不能冷静区分 = 情绪成本吞噬一切,工具还没到 6 个月就会被弃。 |
| 6 | **真想成为会投资的人,还是想摆脱"不知道该怎么办"的焦虑?**两种动机导向完全不同的系统形态。 | Human 独立思考,不允许"都想" | 动机不清 = 系统形态混乱。"想摆脱焦虑"会导致过度 automation,"想成为"需要持续摩擦。 |
| 7 | 愿意未来 3-6 个月做**轻但规律的 ritual** (每周 review + 每笔一句理由) 吗? | Human 独立评估自己的 bandwidth | 不愿意 = 工具大概率沦为短命自用工具 (lapse 风险)。 |

### 来自 L2R3-Opus 的额外问题

| # | Question | Best answered by | Why it matters |
|---|---|---|---|
| 8 | 工具维护时间 ≤ 3 小时/周现实吗? | Human 用 2 周小原型做校准 | 不现实 = 系统 6 个月后吞噬主业,对整体生活为负。 |
| 9 | 私有模型 v0.1 从什么开始?(XGBoost? LLM? 手工规则?) | L3 scope + ML PhD 经验 | 这不是 L4 问题,是 v0.1 的第一个产出边界——不决定就是一个会无限扩张的黑洞。 |
| 10 | "配偶可见度"是 v1.0 任务还是可以 v2+ 再说? | Human 和配偶直接对话 | 如果配偶每周 > 1 次聊投资决策 = must-have v1.0;如果每月 < 1 次 = v2+ 甚至可能干扰。 |

### 最重要的建议:先答 §7.1-4,再进 L3

四个核心必答 (Q1-Q4) 没有精确答案前进 L3,L3 会产出一份**假设不稳定的 PRD**。更诚实的路径是:
- 先把 Q1 写成一句话 (不超过 20 字)
- Q2 给三路一个固定 priority order (哪一路 tie-breaker)
- Q3 定一个"agent 主动度 budget" (每周主动发言上限)
- Q4 定一个 3 个月可测的 checkpoint

这四件事加起来不超过一个下午。做完再进 L3,scope 会清晰 10 倍。

---

## 8. Decision menu (for the human)

### [P] Park — synthesizer 强推荐 ← **因为 verdict 是 unclear,且四个核心必答未答**
```
/park 004
```
**强推荐理由**:
- verdict 是 `unclear`,不是 `Y`,意味着 L2 已尽力但还缺一些只有 human 自己能给的 input
- §7.1-4 的四个必答问题如果在 L3 之前没精确答案,L3 产出的 PRD 会漂移
- 这四个答案不需要更多搜索,只需要 human 一个下午的独立思考
- Park 不是放弃。所有 L1/L2 artifacts 完整保留,随时可以带着精确答案回来

### [R] 再注入 steering,先定义"稳定赚钱",再跑 L2R4
```
/explore-inject 004 "<精确定义了稳定赚钱的版本>"
/explore-next 004
```
如果 human 觉得 §7.1 的答案自己写出来就顺便解决了大部分不确定性,可以用这条路径让 L2R4 用精确 framing 重跑。成本:1 轮 R1+R2。

### [S] 带着 7 个必答问题进 L3 — 承担 unclear 风险
```
/scope-start 004
```
只在下列条件**同时满足**时推荐:
- human 承担"稳定赚钱"承诺没被证据验证的风险
- human 已在内心回答了 §7.1-4 (不必写成文字,但自己要清楚)
- human 接受 **Calibration Engine first, Action Engine second** 作为 L3 的一个 hard design constraint
- human 接受"单人工具 lapse 风险"并愿意在 L3 定义 "3 小时/周维护上限" 这个硬约束

如果不完全满足这些条件,[P] 比 [S] 是更诚实的选择。

### [F] Fork 一个更窄的 L2 角度
```
/fork 004 from-L2 calibration-engine-only as 004a
```
如果读完这份报告后 human 觉得"我其实只想要 calibration engine,完全不做 action engine 那一半",可以 fork 一个更窄的 004a。这会让 Barber-Odean 威胁直接消失,也让 §7.3 的答案提前 locked-in。

### [A] Abandon
```
/abandon 004
```
**不推荐**,除非 human 读完后意识到"我不是想要这个,我只是想要更好地和现有咨询师沟通"——那种情况下 004 应该直接换一个 idea 号重写。

### [V] 看完整报告
当前文档本身。

---

## Fork log

(暂无 sub-fork。若选 [F] 将在此登记。)

---

## Synthesizer 的最后一句话

如果 human 读完本文档只能带走一句话,请带走这一句:

> **系统应该首先是 calibration engine (帮你判断什么时候别动、该怎么想),其次才是 action engine (替你出具体手)。如果顺序反了,"稳定赚钱"会变成"稳定放大错误"。**

其余所有设计、所有红线、所有必答问题,都是这一条主线的展开。
