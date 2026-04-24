# L3 Scope Menu · 001 · "Research Radar —— lab 的外置研究编辑部"

**Generated**: 2026-04-23T14:35:00+08:00
**Source**: L2 报告（stage-L2-explore-001.md）+ L3R0 intake + 2 轮独立辩论
**Rounds completed**: L3R1（Opus 4.7 Max + GPT-5.4 xhigh），L3R2（Opus 4.7 Max + GPT-5.4 xhigh）
**Searches run**: 14 次 scope-reality queries（Opus 6 + GPT 8），覆盖 Readwise / Undermind / Notion / Elicit / Superhuman / Linear / Are.na / Height / Readwise Reader / IndieHackers 等
**Moderator injections honored**: 0（本 L3 未注入 moderator 注记）

## How to read this menu

这是 L3 对 001 Research Radar 的 scope 输出：三个 **peer 候选 PRD**。每个是**同一 idea 在你约束下一个合法的不同 cut**，不是"好中差"。你通过 `/fork` 把其中 1 个（或多个并行）推进到 L4：

```
/fork 001 from-L3 candidate-A as 001-pA
/plan-start 001-pA
```

读完后你应该能回答一个问题：**这一轮 v0.1 我想先押 "briefing value"（立刻可感、kill-window 短）还是 "compounding memory value"（3-6 个月才显现、kill-window 长）？** 这是本菜单的核心取舍轴。

L1 的 13 条灵感菜单和 L2 的深度报告独立保留。如果你读完这份菜单觉得"没有一条够锋利"，可以 `/fork 001 from-L2 <angle>` 或 `/status 001` 回退。

---

## Intake recap —— 我们honor了什么

### 硬约束（✅）—— 三个候选都遵守
- **双 persona，PI 优先**：PI（买单者、Dr. Chen 类型）作为经济 buyer，senior PhD/postdoc（高频 operator、Maya 类型）作为高频使用者，**两类用户都必须独立被 serve**（不允许"operator 共用 PI 账户"的简化）
- **15-30h/周 投入**（按 ~20h/周 估算）
- **v0.1 先免费，预留 auth 不做 billing**
- **L2 §6 的 6 条 conditions 全部继承**：data portability 承诺、digest-first 首页、hybrid taste signal、可剪枝低价值留痕、buyer+operator 双层、delegation 假设待验证

### 软偏好（🤔 但可商量）
- **Web-first**（所有候选默认 Web；C 包含 PWA 扩展）
- **时间由 scope 驱动**（不是相反）—— 因此三个候选各有独立的时间估算

### 红线 —— 三条绝对红线（三候选都遵守）
1. **v0.1 不扩成通用论文发现器**，守 8-15 topic 的护城河
2. **v0.1 只委托 triage，不承诺替代第一手阅读**（summary 限长 ≤ 3 句，skip 决策可追溯）
3. **v0.1 不做公开评分 / 社区 review / 公共排行榜**（所有 taste / belief / stance 数据只在 lab 内部）

另外 GPT R2 提出的 **red-line 分层法**（"绝对红线 + 阶段性边界"）被 Opus R2 接受为 v0.1 决策结构的结构性升级 —— 这不是软化红线，是承认某些边界（如"不把 graph 作为唯一首页入口"）适合在 30 天自用后 re-evaluate。

### ❓ items 本菜单已resolve的（各候选如何选）

| ❓ item | Candidate A | Candidate B | Candidate C |
|---|---|---|---|
| **Target delivery 时长** | ~5 周 | 12-14 周（beta，不是 launch） | ~6-7 周 |
| **Red lines 分层** | 3 条全部升格为硬宪法 | 2 条绝对 + 1-2 条阶段性（30 天后 re-evaluate） | 3 条全部升格为硬宪法 |
| **Platform 形态** | Web only | Web only | Web + PWA（iPad/手机） |
| **UX 三角取舍** | Speed + Differentiation，放弃 Polish | Differentiation + Polish，放弃 Speed | Speed + Polish，放弃 Differentiation |

### ❓ items **仍对 human 开放** 的

以下问题本菜单**不能替你决定**，需要你在选 candidate 时一并明确（或留给 L4 早期 spike 验证）：

1. **operator 真实愿意每周花 ≥ 20 分钟做 explicit taste signal 吗？** —— 这是 Candidate B 成立的 necessary condition；L2 §7 Q3 也标记过。**如果你选 B，必须在 week-4 checkpoint 前回答这个问题**；不确定的话建议先选 A（A 对这条假设的依赖更弱）
2. **data portability 的具体承诺形态**（self-host / JSON export / open format 三选至少一）—— 三候选都需要，但具体形态是 L4 早期决策；**建议默认 "JSON export + 自己 host Postgres/SQLite" 最轻量**
3. **"PI 用 30 秒真的能感到 aha" 这个假设**在哪个候选上成立 —— A 赌 week-1 briefing clarity、B 赌 day-45 memory compound、C 赌 polished presentation；**human 必须知道自己更信哪条**

---

## The key tradeoff axis

**两轮独立收敛、经 6+8 次搜索验证的核心 axis**：

> **v0.1 先押 "briefing value"（立刻可感、kill-window 短）还是押 "compounding memory value"（复利 3-6 个月才显现、kill-window 长）？**

- **Briefing value** = week-1 就可感，user 立刻说 "省我时间" / "这周更清楚"；差异化门槛低，但验证快、回头容易。Superhuman、Linear、Undermind 走的是这条路径。
- **Compounding memory value** = 第 45-90 天才显现，user 的 aha 是"这个工具让我记得住我 lab 的 intellectual lineage"；护城河深，但要赌 operator 的持续投入。Readwise、Are.na 证明这条路径可成立，但 v0.1 通常必须窄 + 必须坚持。

**三候选对这条 axis 的 bet**：

- **A**（**PI Briefing Console**）：同时押两者，但把 briefing value 做 ultra-sharp + 把 memory value 压缩到**只有 breadcrumb resurface 一条线**（最 balanced、最快验证，5 周）
- **B**（**Lab Dossier Beta**）：All-in compounding memory value（12-14 周 beta，最高 reward + 最高 risk）
- **C**（**Polished Personal Lab Radar**）：All-in briefing value + presentation polish（6-7 周，最稳但上限低）

你的 intake 选了 **Speed + Differentiation + Polish 三项**。这条 axis 告诉我们：**Polish 服务于 briefing value 的即刻可感**（polish 让 week-1 感受强），**Differentiation 服务于 memory value**（memory 是护城河），**Speed 在两者之间权衡**。三角冲突的最接近解是 A —— 把 briefing 部分做锋利 + 保留 breadcrumb 这条最小 memory 线。

---

## Candidate PRDs

### Candidate A · "PI Briefing Console" （建议 fork id: `001-pA`）

**Sources**: Opus R1 + R2 refined、GPT R1 + R2 refined（双方独立提出、R2 双方收敛）

#### v0.1 essence

一个**只做每日 topic-state briefing + 低价值留痕**的极简 Web 工具。8-15 个 topic，每天一份 briefing，按 "state shift" 组织（不是按论文堆叠）；每篇新工作都有 4-action 归档（read / later / skip / breadcrumb），breadcrumb 带 resurface 逻辑。**不做 taste agent 完整闭环、不做 topology graph、不做 lab shared view 的深度协作 —— 砍到只剩一个 loop**：每天打开 → 读 briefing → 对每篇 4-action → 系统记住。v0.1 的 bet 是 "digest-first briefing + 可剪枝 breadcrumb" 这一对 novelty axis 值不值得花时间，其他留到 v0.2+。

#### User persona

**主 persona**: Dr. Chen 类型 PI —— 带 5-15 人 AI lab，覆盖 8-15 topic，每周要给学生做方向建议，最痛的是"漏看一篇 next week 会被学生问住的文章"。
**次 persona**: Maya 类型 senior PhD/postdoc —— **独立 login、独立 seat**（R2 共同修正了 R1 的"共用 login"错误），权限极简（全员 read+write，admin 只负责 topic 池管理），每天替 lab 做 triage，最怕"好像看过、之后再也找不回"。

#### Core user stories

- 作为 **PI**，我每天 8:00 可以打开 Web briefing，10 分钟内看完 8-15 topic 的 state 摘要，**确定今天要深入哪 1-2 个 shift**
- 作为 **PI 或 operator**，我可以对 briefing 里每一篇论文做 4-action（read now / read later / skip / breadcrumb），系统记住并在下次同类工作出现时体现
- 作为 **PI**，3 个月后我可以查"过去 90 天我为哪些 topic 标过 breadcrumb、其中哪些现在被 resurface 了"——形成"过去标过但可能要重看"的列表
- 作为 **operator**，我可以对系统的 skip / breadcrumb 决策写一句"why I disagree"（轻量 explicit taste signal，但不做闭环 agent）

#### Scope IN

- Topic 维护：8-15 topic，PI 手动 CRUD，每 topic 一个关键词池 + arXiv category + 可选 seed author
- 每日 briefing（Web page）：digest-first，每 topic 一行 state 摘要 + 至多 3 篇触发论文
- 4-action 标注（read / later / skip / breadcrumb），每次可附一句 why
- breadcrumb resurface 逻辑：6 周 / 3 个月 / 6 个月被系统 re-surface，带"为什么现在又回来"的上下文
- **PI + operator 各自独立 login**（轻量 invite by email token，≤ 15 用户），权限极简
- data portability：JSON export、数据库自持有

#### Scope OUT（明确不做）

- **完整 Taste agent 闭环**（只收集 explicit disagree，不做 hybrid agent 反向影响 briefing）—— 延后 v0.2
- **Topology graph / topic 关系图主视图**—— digest-first 不需要它
- **Lab shared belief ledger / stance history**—— v0.1 不做
- **Paper 二次分析 / novelty 自动评分 / 跨 paper 对比**
- **Mobile native / CLI / PWA**—— Web only
- **PDF 全文解析**—— 仅用 abstract + metadata
- **Onboarding-focused view**（Carol 场景）—— 降级 v0.2

#### Success looks like（observable）

- **PI 连续使用 30 天**（日活 ≥ 25/30）—— briefing 不是 newsletter 是 ritual 的证据
- **PI 每月 ≥ 5 次 breadcrumb resurface 被实际点开** —— 低价值留痕的价值被用户自己验证
- **operator 每周 ≥ 2 次独立登入 briefing** —— operator seat 不会死
- **PI 可以说出 ≥ 2 个"没这工具会漏看"的真实案例**（30 天后访谈；day-60 是 breadcrumb resurface 的真正 aha window）

#### Time estimate under ~20h/week

- **~5 周 @ 20h/周**（双方 R2 合并：Opus R2 5-7、GPT R2 4-5 → 中值 ~5 周，**已包含 operator 独立 login 修正**）
- **Confidence: Medium-High**
- Unknown 主要在 "LLM 解读质量调优" —— 如果调优失败，briefing 可能退化成 summary list；建议 day-30 手动陪 PI 实际用 ≥ 10 次来校准

#### UX priorities（tradeoff stances）

- **Speed > Polish**：UI 粗糙可接受（表格 + 纯文本 briefing 就行）
- **Differentiation > Polish**：digest-by-state-shift + breadcrumb resurface 两条 core bet 必须做对
- **PI 优先，operator 独立可用**：两 seat 都必须能登、但重心和 UI 设计偏 PI 的使用节奏
- **一个视图解决一件事**：首页 = digest，无 sidebar、无 modal、其他功能通过 URL 进入

#### Biggest risk

**PI 把 briefing 当成 newsletter 读一周然后放弃** —— v0.1 没有完整 taste agent、breadcrumb 第一个月还没累积足够信号、topology 这个"wow moment"也不存在。风险缓解：**需要 60 天窗口**（不是 30 天，因为 Readwise spaced repetition 的 aha 需要 ~30 天累积、breadcrumb resurface 的 aha 更晚）；day-45/60 必须陪跑 ≥ 10 次现场使用校准；如果 60 天后 PI 还是只看不标注，证明"4-action loop" 这个 bet 错了，需要回 L2 重新思考。

#### Scope-reality verdict

- **Comparable products**:
  - **Readwise MVP**（原名 Rekindled）—— 一个 email loop + highlights + spaced repetition resurface 就是全部产品（[Readwise changelog](https://readwise.io/changelog)、[Medium review](https://medium.com/@ahumanwhoiswriting/readwise-a-comprehensive-review-d35d8ead3e28)）
  - **Undermind YC S24**（2026-01）—— 输入 topic → 2-3 min 深搜 → 邮件发 report，只做一件事（[Product Hunt](https://www.producthunt.com/products/undermind)、[YC](https://www.ycombinator.com/companies/undermind)）
  - **Superhuman Split Inbox** —— focused sections、VIP、批处理（[blog](https://blog.superhuman.com/how-to-split-your-inbox-in-superhuman/)）
  - **Linear early method** —— 小团队 1-3 weeks 模块、先给 beta 用户（[method](https://linear.app/method/scope-projects)）
- **Typical v0.1 includes**: 一个 email/digest loop + 最小 action 集 + resurface / memory 机制
- **Typical v0.1 cuts**: UI 打磨、多端同步、30+ 集成（Readwise 都是后来叠的）
- **Net read**: 🟢 **Typical** —— A 的 scope 密度（digest + 4-action + breadcrumb resurface，5 周）**紧贴 AI research tool 圈的 "Ship-in-<60-days MVP" 压倒性主流**；不 undershooting 也不 overreaching

#### Best fit for human who

想**快速验证 "digest-by-state-shift + breadcrumb resurface" 这两条 core bet**、愿意在 2 个月内决定 continue/kill、不介意 v0.1 UI 粗糙、希望保留三角冲突最平衡的解（Speed + Differentiation 并存、Polish 主动放弃）。如果你的心态是"先看看这能不能 work、再决定要不要全力投入"，A 是你的起点。A 的另一层优势：**即便 60 天后你决定放弃、A 已完成的 scope 仍有 ~40-60% 可复用，升级到 B 不是从 0 开始**。

---

### Candidate B · "Lab Dossier Beta" （建议 fork id: `001-pB`）

**Sources**: Opus R1 + R2 refined、GPT R1 + R2 refined（GPT R2 关键 rebrand："不叫 Lab Research Editor v0.1，叫 Lab Dossier **Beta**"）

#### v0.1 essence

一个**完整的 lab 级外置研究编辑部 beta**：digest + topic dossier（持续生长的立场 / 变更原因 / 待读主线 / 留痕层）+ hybrid taste 闭环 + 多用户 lab view + breadcrumb resurface + data portability。首页仍是 digest-first，但每个 topic 后面都有一份**持续生长的 dossier**，记录 lab 当前立场、最近为什么改判、哪些工作只留痕、哪些已入必读主线。**诚实放弃 Speed** —— 这是 3 个月的 beta 投入，不是几周的 MVP；**第一个里程碑是 beta，不是 polished launch**（GPT R2 的关键 rebrand，Opus R2 接受）。

#### User persona

**主 persona**: Dr. Chen 作为让自己研究品味逐步外化成 lab 资产的 PI —— 不再只看周报，而是在组会前把 dossier 当默认入口。
**次 persona**: Maya 作为让记忆复利的 operator —— 不仅 triage，还要在组会前迅速找回"我们上次为什么不信这条路线"；她需要的是**可继承的 topic memory**。
**核心 tension**: PI 买单的理由是"立刻更清楚"（briefing value），但产品真正 compound 依赖 operator 每周主动维护 dossier / breadcrumb / taste feedback（习惯养成 value）。两种 value curve 不同 —— B 押的是后者。

#### Core user stories

- 作为 **PI**，我能看到当前 topic 的 lab 立场（不是个人立场），带进组会有统一 point of view
- 作为 **operator**，我能把一篇新工作变成 dossier 的 stance update（"这件事让我们改判 / 加强原立场"），让 context 累积而不是每周重置
- 作为 **PI 或 operator**，我对任何系统判断可写 "why I disagree"，taste agent 记下、影响下次同类工作的标注（**hybrid explicit-implicit 闭环**）
- 作为 **operator**，我能把之前忽略的 breadcrumb 重新 promote 回当前 queue —— skip 是可逆的
- 作为 **PI**，我能把 stable topic 和 changing topic 分开看，注意力投向有 motion 的方向
- 作为 **任何 lab 成员**，我可以 export 整个 lab 的数据（JSON + markdown）

#### Scope IN

- 所有 Candidate A 的内容（digest + 4-action + breadcrumb + resurface + data export）
- **Topic dossier**：topic 下的当前立场 + 变更历史 + 必读主线 + 留痕层
- **Hybrid taste agent**：operator 每次 explicit disagree 被记录；系统用 implicit signal（read time / later→read ratio / breadcrumb hit rate）补充；每周产出 "lab taste drift" 简报
- **Multi-user lab view**：PI invite by email token（不用 OAuth），≤ 15 用户；每人独立账号 + 独立标注、共享 topic ledger
- **Belief ledger**：topic 下可写 stance 和 stance history
- **权限分层**：PI = admin、operator = member，可分 read-only / write
- **Topology explainer（二级 view）**：topic 内的 paper—relation—paper 图（supersedes / derives-from / contradicts）—— 作为 explainer，**不作为首页入口**

#### Scope OUT

- 公开打分 / 社区 review（Paperstars 失败模式）
- PDF 全文解析（abstract 够用）
- Post-experiment integration loop（lab 实验结果进 topic 图）—— v0.2+
- Carol-focused onboarding tour
- mobile / CLI / PWA
- cross-lab federation
- 原 proposal 的"最终目标 research agent"（2027+）

#### Success looks like

- v0.1 上线 60 天内：**至少 3 支真实 AI lab 同时在 beta 使用**（≥ PI + 2 operator 活跃）—— 注意这是 **"3 个 lab 在 beta dogfooding"，不是"产出 polished v0.1"**
- 每个活跃 lab 的 "taste drift 简报" 达到 PI 读 30 秒能说 "是的这就是我们 lab 这两个月的变化"
- Belief ledger 非空（每 lab ≥ 20 条 stance）
- 至少出现 **2 次"因为 dossier 中的旧留痕被翻出，当前判断被修正"的真实案例**
- **Differentiation 可被 3 分钟 demo 说清楚**：lab PI 看了 demo 能说 "我没见过这样的工具"

#### Time estimate under ~20h/week

- **~12-14 周 @ 20h/周**（双方 R2 合并：Opus R2 10-12、GPT R2 12-14 → 采用 GPT R2 上限 "更像 staged beta"）
- **Confidence: Medium-Low**
- **核心 unknown**：taste agent 在 cold start 期（前 4 周）如果 operator 写 disagree 频率太低，agent 学不动 —— 这一段工时可能从 35h 膨胀到 70h

#### **Explicit assumption（必须写出的前提）**

- **Operator 愿意每周花 ≥ 20 分钟做 explicit taste signal**（写 disagree、promote breadcrumb、维护 dossier stance） —— 这是 B 成立的 necessary condition
- **如果 week-4 checkpoint 显示 operator 不愿意，B 立刻 pivot 回 A 形态**（已完成 scope 可复用 40-60%）—— 这是 scope 成立的内置 escape hatch

#### **Mandatory checkpoints**（每 3 周一次）

- **Week 3**: digest + 多用户 auth 上线 → kill/pivot decision
- **Week 6**: topology explainer + breadcrumb + stance ledger → kill/pivot decision
- **Week 9**: taste agent 可用 → kill/pivot decision
- **Week 12**: 3 lab beta dogfooding 报告 → kill/pivot decision
- **Week 14**: beta 对外 —— 不是 polished launch

每个 checkpoint 必须有 PI-operator 双角色陪跑使用的实际记录。Notion 2016 launch 前做了 6 周 closed beta + 500 power users 反馈才上 Product Hunt —— B 是它的 solo-operator 结构化版本。

#### UX priorities

- **Differentiation + Polish > Speed**
- **Compounding context > rapid throughput**
- **Shared lab memory > personal convenience**
- **Calm confidence > feature count**
- **一切服从"研究编辑部"叙事**：每个 feature 对应 "发现 / 判断 / 归档 / 留痕 / 回看 / SOTA" 中的一个

#### Biggest risk

**12-14 周的 beta 周期里，任何一次中途验收都只是半成品**。operator 可能在 week-6 拿到 digest + multi-user 但没有 taste agent 的版本觉得"和 newsletter 没区别"而失去耐心。**次高 risk**：operator 持续维护 dossier 的动机与 operator 日常动机（快速完成 triage）之间有 tension —— 如果 taste feedback 频率 < 20min/周，整个 compound 会空转。**风险缓解**：强制 checkpoint + explicit assumption + 内置 pivot escape hatch；但它仍然是三候选中 confidence 最低的。

#### Scope-reality verdict

- **Comparable products**:
  - **Notion MVP（2016-03）** —— OSX + Web 双端 + offline-first + block 基础（[Flowjam playbook](https://www.flowjam.com/blog/how-did-notion-launch-2-000-word-playbook-for-founders)、[Nira history](https://nira.com/notion-history/)）
  - **Are.na** —— collections over time、协作 channel、私密/开放边界、export（[about](https://www.are.na/about)、[channels](https://help.are.na/docs/getting-started/channels)）
  - **Readwise 2019** —— 从 day 1 就押 "interrupt the process of forgetting"（[blog](https://blog.readwise.io/remember-more-of-what-you-read-with-readwise/)）
- **Typical v0.1 includes**: "全功能 at launch" 配 6+ 周 closed beta 反馈（Notion 模式）或 memory-first 极窄切片（Are.na / Readwise 模式）
- **Typical v0.1 cuts**: polish launch 节奏、protocol extensions、社区层
- **What this candidate cuts vs norm**: 比 Notion 那种 "closed beta + 全功能"少 YC 级工程资源；比 Are.na/Readwise 那种 "memory-first 极窄"在 v0.1 就背了更多 persona + 更多 feature
- **Net read**: 🟡 **Ambitious** —— 可做但不能再叫 10-12 周的轻量首版；更像 staged beta，而非短跑 MVP。solo 20h/周 走 B 是 stretch，**通过强制 checkpoint + explicit assumption 可以控制风险**，但不消除它

#### Best fit for human who

**真正相信买单理由最终来自 "lab 的研究判断会不会沉淀成资产"**、愿意接受更慢的验证周期、也**愿意把首个里程碑定义成 beta 不是 polished launch**、能容忍中途 kill → pivot 到 A 的可能性、且有能力**坚持 3 个月以上**专注。B 不适合"想快速验证能不能 work"的心态 —— 它假设你已经信了 memory value 的价值。

---

### Candidate C · "Polished Personal Lab Radar" （建议 fork id: `001-pC`）

**Sources**: Opus R1 + R2 refined、GPT R1 + R2 refined（GPT R2 把时间从 3-5 周修正到 6-8 周，Opus 坚持 5-7 —— 最终取 6-7 周）

#### v0.1 essence

一个**好看、好用、容易上手的个人版研究 radar**：每日 topic briefing + 简洁 paper 管理界面 + 智能 summary + search + 基础 personal knowledge base + PWA 多端。功能组合和现有工具（Elicit、ResearchRabbit、Undermind）有相当重叠，但执行得比任何单一工具都细腻：UI 讲究、响应快、多端同步、移动端 PWA 可用。**放弃 differentiation** 意味着不做 "digest-by-state-shift" 和 "breadcrumb resurface" 这两条未经验证的 novelty bet、也不做 lab shared view。走的是"我做得比现有工具都精致"这条产品主义路线。

#### User persona

**主 persona**: Dr. Chen 第一次愿意让工具进周会流程的 PI —— 需要的是低学习成本、体面输出。
**次 persona**: Maya 作为"同一套工具被 PI 推荐给学生"的次级传播对象（**v0.1 不做专门的 operator 视角**）—— 这是 C 对 L2 buyer/operator split 的有意识 concession。
**警告**: 这是**回到"个人工具"假设**的候选 —— 它在 v0.1 让 operator seat 次级化，violates L3R0 的"双 persona 都被 serve"硬约束的精神（虽然技术上可以说 operator 能用 PI 的账户访问）。**保留 C 在菜单里是为了展示三角冲突的另一个合法方向**，不是推荐。

#### Core user stories

- 作为 **PI**，我可以维护 8-15 topic 关注列表，系统每天为每个 topic 生成一份 digest
- 作为 **PI**，我可以搜索 / 过滤 / 收藏 / 加 tag 我关注的论文，UI 比 Zotero 更现代
- 作为 **PI**，我可以对收藏的论文写 notes，系统生成简单 summary + 相似度推荐
- 作为 **PI**，我可以在 iPad / 手机上用 PWA 版本快速扫 digest + 标注

#### Scope IN

- Daily digest（不做 state-shift 组织，做传统 paper-list 组织）
- Paper 管理（搜索 / 过滤 / 标签 / 收藏 / notes）
- 简单 summary 生成（LLM 摘要 + 关键词，限长 ≤ 3 句以守红线 2）
- 相似度推荐（基于 embedding）
- 多端：Web + PWA（iPad / 手机）
- 简单 auth（单人登录为主，multi-user 是未来 crack）
- 数据导出

#### Scope OUT

- **所有 A 的 state-shift / breadcrumb / resurface**（这些都是 Differentiation bet，放弃）
- **所有 B 的 lab view / taste agent / belief ledger / dossier**
- Topology view
- Operator-specific workflow（只服务 PI）

#### Success looks like

- **30 天**：PI 日活 ≥ 25/30
- **PI 收藏 ≥ 100 篇论文、≥ 20 篇有 notes**
- **PI 愿意把它推荐给学生**
- **但不会有**"没见过这样的工具"的震撼反馈 —— 它是 Better version of Elicit，不是 new thing

#### Time estimate under ~20h/week

- **~6-7 周 @ 20h/周**（双方 R2 合并：Opus R2 5-7、GPT R2 6-8 → 中值 6-7 周；双方都修正了 GPT R1 的 3-5 周乐观估算）
- **Confidence: High**
- 所有组件都是成熟路径，风险在"打磨耗时"而不是 unknown；超时概率低但超时范围小（最多 +2 周）

#### UX priorities

- **Polish > Speed > Differentiation**
- **Familiar workflow > novel worldview**
- **Presentation quality > memory depth**
- **Low-friction adoption > ambitious behavior change**

#### Biggest risk

**C 竞争不过 well-funded 的现有工具**。Elicit 在 2025-2026 持续迭代（88 feature / 125 周的迭代节奏，solo 20h/周 跟不上），ResearchRabbit 被 Litmaps 收购进入整合期。如果你 v0.1 用 6-7 周追上他们的功能，他们用 12 个月的工程资源可以保持领先。**C 的真正 risk 不是 v0.1 塌掉，是 v0.1 好看但 v1.0+ 的长期天花板低**——它会陷入"功能 parity + 差不多好用"的无人区。C 是所有候选中"失败但不痛"的候选 —— 不会塌但也不会赢。

#### Scope-reality verdict

- **Comparable products**:
  - **Readwise Reader（2021-2022）**—— cross-platform、PDF/RSS/newsletters、search、annotate、digest；surface area "rather vast"；公开 beta 前先私测、再打磨（[blog](https://blog.readwise.io/readwise-reading-app/)、[next chapter](https://blog.readwise.io/the-next-chapter-of-reader-public-beta/)）
  - **Elicit 首发（2021-08-31）**—— literature review 核心 + 2 年 88 feature / 125 周迭代（[changelog](https://support.elicit.com/en/articles/1475137)、[blog](https://blog.elicit.com/launching-a-feature-every-week/)）
  - **Height public access** —— 成熟协作工具公开发布前已私测约两年（[launch](https://height.app/blog/height-launches-public-access-and-raises-14m-to-build-the-project-management-tool-for-your-entire-company-2)）
- **Typical v0.1 includes**: polished single workflow + basic persistence + one annotation layer
- **Typical v0.1 cuts**: multi-user collaboration、advanced analytics、自定义 agent
- **What this candidate cuts vs norm**: lab-level assets（是 C 的有意 concession）
- **Net read**: 🟢 **Typical (v0.1)** / ⚠️ **Undershooting (v1.0+)** —— v0.1 很稳，但"Better Elicit"定位需要在 12 个月内保持领先，solo 20h/周 跟不上 88 feature / 125 周的迭代速度

#### Best fit for human who

**想要一个"绝不会塌的工具"**、**不打算长期单打独斗持续做这个产品**（把它作为 lab 内部工具或短期 portfolio 项目）、**接受第一性价值更像"better workflow"而不是"new category"**、**不 prioritize lab-level 资产沉淀**。如果你的目标是"给自己和 lab 一个顺手的 research 简报工具，不追求创新或商业化"，C 是诚实的选择。**否则 C 的长期天花板是问题**。

---

## Comparison matrix

| 维度 | Candidate A<br/>PI Briefing Console | Candidate B<br/>Lab Dossier Beta | Candidate C<br/>Polished Personal |
|---|---|---|---|
| **v0.1 时长 @ 20h/周** | ~5 周 | **12-14 周（beta）** | ~6-7 周 |
| **主 persona** | PI + operator（独立 seat） | PI + operator（双向深度协作） | 仅 PI（operator 次级） |
| **Dominant priority** | Speed + Differentiation | Differentiation + Polish | Speed + Polish |
| **放弃哪一角** | Polish | Speed | Differentiation |
| **Bet 的 value 类型** | briefing + 最小 memory（breadcrumb） | all-in compounding memory | all-in briefing + presentation |
| **kill-window** | 60 天（需 breadcrumb aha 窗口） | 90-120 天 beta dogfooding | 30 天可感 |
| **Platform** | Web only | Web only | Web + PWA |
| **Confidence** | Medium-High | Medium-Low | High |
| **Biggest risk** | PI 把 briefing 当 newsletter 放弃 | operator 不持续维护→compound 空转 | v1.0+ 天花板低、被现有产品挤到无人区 |
| **Scope-reality 对照** | Readwise MVP / Undermind / Superhuman | Notion 2016 / Are.na / Readwise 2019 | Readwise Reader / Elicit 首发 |
| **Scope-reality 判定** | 🟢 Typical | 🟡 Ambitious（需强制 checkpoint） | 🟢 Typical (v0.1) / ⚠️ Undershooting (v1.0+) |
| **是否可复用到其他候选** | 升级到 B 可复用 40-60% | —— | 不可复用到 A/B（范式不同） |
| **符合 20h/周 预算** | ✅ | ⚠️（长周期专注挑战） | ✅ |
| **符合 PI+operator 硬约束** | ✅（R2 修正后） | ✅ | ⚠️（operator 次级化是有意 concession） |
| **符合 3 条红线** | ✅ | ✅（第 4 条阶段性） | ✅ |

---

## Synthesizer recommendation

### **推荐 Candidate A 作为主 fork（`001-pA`），B 作为"A 验证成功后的升级路径"而非从 0 并行重建**。

**理由（3 点）**：

1. **A 是 intake 三角冲突（Speed + Differentiation + Polish）的最接近解**。你的 intake 三项全选，但三者数学上不可同时最大化。A 的选择是"Speed + Differentiation 并存、Polish 主动放弃"—— 这是三角冲突里**唯一保留 Differentiation 的短周期候选**（C 放弃了 Differentiation，B 放弃了 Speed）。你的 intake 没选"Low operating cost"或"Broad appeal"，说明你在意的是**独特 + 快上** —— 正是 A。

2. **A 的 scope 密度经 scope-reality search 认证**：Readwise MVP（一个 email loop 支撑 2-3 年产品生命）、Undermind（YC S24，极窄首发）、Superhuman / Linear 的"1-3 weeks 模块、先给 beta 用户"首发现实 —— A 的 5 周 / digest + 4-action + breadcrumb 紧贴这条 AI research tool 圈的主流路径。它**不 undershooting、不 overreaching**，风险窗口（60 天）也在 solo 20h/周 可承受范围内。

3. **A → B 的升级路径可复用 40-60% 已完成 scope**。如果你选 A 而 60 天后 PI 反馈强烈（breadcrumb resurface 真的在 day-45-60 出现 aha、operator 愿意写 "why I disagree" ≥ 20 min/周），你**直接把 A 扩展为 B**，不是从 0 并行建。**反过来则不行** —— 选 B 后 week-4 checkpoint 若 operator 不愿意，你得 pivot 回 A，但 B 已投入的 4 周 scope 部分浪费。**从风险管理角度，先 A 是 strictly dominant 的选择**。

### **不推荐从 0 并行 fork B 或 C**：

- **B 不推荐现在并行 fork**：B 在 A 验证前是 premature bet。B 的核心假设（operator 愿意持续 ≥ 20 min/周 explicit signal）**没有直接证据支持**；L3R2 双方都降低了对 B 的 confidence。如果 A 在 60 天内验证了 "digest + breadcrumb" 可行且 operator 愿意写 disagree，再 fork `001-pB` 从 A 基础上升级；如果 A 60 天后 PI 只看不标注，B 的核心前提已被证伪，就不该再花 12-14 周。
- **C 不推荐**：L3R2 两方都削弱了对 C 的认同 —— **"C 不再是比 A 明显更快的候选"（6-7 周 vs 5 周，差距已经很小）、"C 的长期天花板被 Elicit 88 feature / 125 周的迭代速度压住"、"C 让 operator seat 次级化违反 intake 精神"**。C 在菜单里保留是为了展示三角冲突的另一条合法路径、让你看到"放弃 Differentiation 也是一个真实选项"，但**不建议作为起点**。

### **如果 A 在 day-60 复盘结果**：

- ✅ **PI 持续使用 + breadcrumb resurface 出现 aha + operator 愿意写 disagree ≥ 2 次/周** → fork `001-pB` 从 A 升级，计划 8-9 周补完 dossier + hybrid taste agent + belief ledger（总工程量 ≈ 5 + 8-9 = 13-14 周，与直接选 B 的 12-14 周相当，但风险被 60 天 checkpoint 分担了）
- ⚠️ **PI 使用频率下降 + breadcrumb 没点开** → kill A，回 L2 重新思考（L2 §7 Q1/Q3 需要真实 user interview 才能继续）
- 🟡 **混合反馈（PI 用但不标注）**→ scope-inject 001-pA 继续 refine，不急着升级到 B

---

## Honesty check —— 菜单可能 underweight 了什么

诚实列出本菜单可能考虑不足的维度（mandatory section）：

1. **所有候选都假设 LLM 解读 / summary 的质量足够支撑"briefing 不退化成 paper-list"**。如果实际 LLM 对 AI 前沿论文的 novelty / impact 判断质量在 day-10 测试中不如预期（比如漏掉真正的 shift、或把 incremental 误标为 shift），三候选都会塌。**这是跨候选的公共 risk，未被单独列出**；建议 L4 早期做 2-3 天 LLM prompt spike 验证。

2. **三候选都默认你有 3+ lab 的获客渠道**。Candidate B 的 success criteria 写"3 支真实 AI lab beta dogfooding"；A 也需要至少 1 个 PI + 2 operator 持续使用。**如果你 lab 的人数 < 3 或外部 lab 不愿参与 dogfood，三候选的 validation loop 都会 degenerate 成"自用"**。intake 没问这个问题，菜单也没解。

3. **"data portability" 承诺的具体形态**（self-host / JSON export / open format）**本菜单没强制选一个**。L2 §6 明确 Mendeley 下线的教训，但三候选都只写"JSON export + 数据库自持"。**L4 早期必须明确形态**，否则早期用户信任会打折扣。

4. **B 的 12-14 周 beta 假设你能坚持 3 个月专注不被其他事情打断**。solo 20h/周 × 14 周 = 280h 连续投入，任何 2 周间断都会 break compound；intake 没测这个能力，菜单也没解。**如果你历史上 3 个月以上连续 side-project 完成率不高，B 的风险被低估了**。

5. **A 的"operator 独立 login 但权限极简"在真实 lab 里会不会引发政治问题没被测试**。R2 双方都修正了 R1 的"共用 login"错误 —— 这是 intake 合规的修正；但 lab 成员 ≤ 15、全员 read+write 的设计在 PI 不想让某些 operator 看到某些 topic 的场景下会塌。**菜单没测 lab 内部权限文化**。

---

## Decision menu （for the human）

### [F] Fork one candidate（**推荐 A**）

```
/fork 001 from-L3 candidate-A as 001-pA
/plan-start 001-pA
```

如果你相信我的推荐，这是 one-line 起步。

### [MF] Fork multiple candidates in parallel（不推荐但合法）

```
/fork 001 from-L3 candidate-A as 001-pA
/fork 001 from-L3 candidate-B as 001-pB
/plan-start 001-pA
/plan-start 001-pB
```

如果你真的想同时跑 A 和 B：**解释清楚为什么 —— solo 20h/周 × 2 = 要么减半投入、要么延长 2 倍周期**。我建议只选 A；60 天后再决定是否 fork B。

### [R] Re-scope with new input

```
/scope-inject 001 "<你的 steering>"
/scope-next 001
```

如果你读完菜单觉得**某个 axis 没被涵盖**（比如"能不能做一个只服务 onboarding 场景的候选 D"），注入 steering 后再跑一轮 L3R3。

### [B] Back to L2 — 重想这 idea

```
/status 001
```

如果三个候选都感觉不对（极少情况，但可能），回 L2 重新 explore。L2 的 13 条 L1 灵感仍在。

### [P] Park

```
/park 001
```

保留所有 artifact。复活条件：当你有能力回答 L2 §7 的 Q1/Q3（buyer vs operator 优先级、delegation 边界）时。

### [A] Abandon

```
/abandon 001
```

**不推荐** —— L2 verdict 是 Y-with-conditions，不是 N。除非你确认不再关心 AI research 跟进问题域。abandon 需要写 lesson 文档。

---

## Fork log

- 2026-04-23T13:27:47Z · candidate A ("PI Briefing Console") forked as `001-pA` (status: just-created) —— path: `discussion/001/001-pA/`
