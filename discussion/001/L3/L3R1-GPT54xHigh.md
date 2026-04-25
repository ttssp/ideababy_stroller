# Idea 001 · L3R1 · GPT-5.4 xhigh · Scope (no search)

**Timestamp**: 2026-04-23T21:18:00+08:00
**Inputs read**: L2 report, L3R0-intake
**Searches used**: NONE in this round
**Visibility**: did NOT read Opus's L3R1

## 0. How I read the intake

我把这轮 intake 读成一个很清楚的命题：human 不是要一个“什么都做一点”的研究工具，而是要在每周约 20 小时的现实投入下，为 PI-first、operator-viable 的 AI lab 做出第一版可用的 research editor。所有候选都必须同时服务 Dr. Chen 这类 PI buyer 与 Maya 这类 senior PhD/postdoc operator，但重心先让 PI 感到“我对 lab 正在发生什么重新有把握”，而不是先把学生 onboarding 做满。与此同时，L2 已经把几条保护栏说得很明确，所以我会把 digest-first 首页、buyer/operator 双层、hybrid taste signal、可剪枝低价值留痕、未来付费层留缝、以及至少一种数据可移植承诺视为所有候选都要守住的底线。未知项我会主动给出 target delivery 与 red lines 的 options，但不会假装 Speed、Differentiation、Polish 可以同时最大化。

- Hard constraints I'm respecting:
  - 双 persona 必须都被服务，但 PI 优先，Carol/onboarding 降级到 v0.2+
  - 时间估算按 `~20h/week` 给出，超出就诚实写长
  - v0.1 先免费，预留未来 paid tier 的空间，但现在不做 billing 决策
  - 平台默认按 Web-first 的产品形状思考
  - digest-first、hybrid taste、可剪枝留痕、buyer/operator split、data portability 都要保留
- Unknowns I'll propose options for:
  - Target delivery 应该压在 3-6 周，还是接受 8-12 周换更完整 product shape
  - Red lines 哪些要升格为 v0.1 的硬宪法，哪些只做阶段性边界
- Red lines I'll honor:
  - 不把它做成通用论文发现器
  - 不承诺替代第一手阅读
  - 不做公开评分或论文社交市场

## 1. Candidate A · “牺牲 Polish：PI 决策简报台”

### v0.1 in one paragraph
这是一个偏“总编台”而不是“知识库”的 v0.1。首页只有一件事：把 8-15 个 topic 这一周有没有发生真正值得 PI 注意的状态变化讲清楚，并把每条新工作放进三种去向之一：值得读、只留痕、暂时略过。PI 看到的是 topic shift 与该不该投入注意力，Maya 看到的是一块高吞吐的 triage 工作台。它的独特点在于“低价值留痕”与“topic state shift”是第一公民，但为了尽快上线，我默认它的界面、协作手感、可视整理都会偏粗糙。

### User persona (sharpened from L2)
主 persona 是 Dr. Chen：带 7 人左右 AI lab，每周要快速判断哪些方向需要组会时间、哪些只是噪音。次 persona 是 Maya：每天都会替 lab 吸收新工作，但最怕“好像看过，之后再也找不回”。她愿意接受粗糙工具，只要真的省掉 triage 时间。

### Core user stories (3-5)
- As a PI, I can open one briefing and see which topics actually shifted so that I know where to spend this week's attention.
- As an operator, I can push each new work into read / leave-trace / skip so that the lab stops losing context to inbox overflow.
- As an operator, I can leave one-sentence “why I disagree” notes so that the system starts learning lab taste without heavy annotation.
- As a PI, I can review what was skipped but still preserved so that delegation feels reversible rather than blind.

### Scope IN
- digest-first 首页，按 topic 呈现本周 shift、稳定、待观察三类状态
- 面向 operator 的 triage 流，把新工作落到 `read / leave-trace / skip`
- 每个 topic 的简短状态卡，记录“为什么这周值得注意/不值得注意”
- 低价值留痕区，支持之后再提升或剪枝
- 极轻量的 taste feedback：同意 / 不同意 + 一句原因
- 基本的数据导出承诺，用来降低早期信任门槛

### Scope OUT (explicit non-goals)
- 不做漂亮的 topology/map 首页，因为这一版优先验证决策价值，不优先验证展示张力
- 不做 Carol 式 onboarding tour，因为 v0.1 先服务 buyer + operator 的高频决策场景
- 不做多 lab 网络或公共分享，因为这会稀释私密信任边界
- 不做“帮你把 paper 读完”的姿态，因为那会把 triage 产品误卖成替代阅读

### Success looks like
- Dr. Chen 每周至少两次打开首页，并能直接指出 1-2 个需要组会讨论的 topic
- Maya 每周能在固定时段完成大部分 triage，而不是全天被零碎信息打断
- 至少一批原本会被完全遗忘的“低价值工作”在 30 天内被重新找回并重判
- lab 对“自动略过”不再本能排斥，因为 skip 不是消失，而是可回看的留痕

### Honest time estimate
- `4-6 周 @ 20h/week`
- Confidence: `M`
- Unknowns:
  - PI 对粗糙体验的容忍度到底多高
  - Maya 是否愿意持续留下极短 taste feedback
  - 初始 8-15 个 topic 的边界划分会不会反复调整

### UX principles
- `Speed > Polish`
- `Decision clarity > completeness`
- `Digest-first > exploration-first`
- `Reversible delegation > confident automation`

### Biggest risk
最大风险不是“做不出来”，而是第一印象太像内部管理后台。这个候选把差异化押在 editorial judgment 与 pruneable breadcrumb 上，但如果呈现过粗，PI 很可能只看到“又一个需要人维护的面板”，而看不到“这让我的 lab 判断速度变快了”。它能最快验证独特价值，也最容易因为粗糙而失去信任。

## 2. Candidate B · “牺牲 Speed：Lab Topic Dossier”

### v0.1 in one paragraph
这是三个候选里最像“产品定义”的版本：首页仍是 digest-first，但每个 topic 后面都有一份持续生长的 dossier，记录 lab 当前立场、最近为什么改判、哪些工作只是留痕、哪些工作已经进入必读主线。PI 看到的是“我们 lab 对这个 topic 目前的判断”，Maya 看到的是“我如何把零碎发现沉淀成可继承的上下文”。这一版既保留 differentiation，也努力把手感做得足够稳，因此明确接受更长周期。

### User persona (sharpened from L2)
主 persona 仍是 Dr. Chen，但这次他不是只想看一份周报，而是想让自己的研究品味逐步外化成 lab 资产。次 persona 是 Maya，她不仅要 triage，还要在组会前迅速找回“我们上次为什么不信这条路线”。她需要的不只是队列，而是可继承的 topic memory。

### Core user stories (3-5)
- As a PI, I can see the current lab stance on a topic so that I enter meetings with a coherent point of view.
- As an operator, I can turn a new work into an update to the topic dossier so that context compounds instead of resetting each week.
- As a PI or operator, I can record why we disagree with the default take so that future recommendations reflect lab taste.
- As an operator, I can revisit previously ignored work in context so that “skip” stays reversible and useful.
- As a PI, I can separate stable topics from changing topics so that my attention goes to motion, not noise.

### Scope IN
- digest-first 首页，但每个 topic 可进入持续更新的 dossier
- dossier 内保留当前立场、最近变化、留痕层、待读主线
- PI 视角与 operator 视角都清楚存在，但共享同一 topic memory
- hybrid taste capture：显式不同意理由 + 日常使用中的隐式信号
- 可剪枝的 breadcrumb 机制，不把 archive 变成垃圾堆
- 明确的数据可移植承诺，降低“被平台绑住”的顾虑

### Scope OUT (explicit non-goals)
- 不做公共社区评论或跨 lab 共享层，因为信任必须先在私域成立
- 不做全自动“研究代理人”，因为这一版的目标是判断与记忆，不是替 lab 生成研究结论
- 不做大而全的 discovery 覆盖，因为 topic density 比 coverage 更重要
- 不做 onboarding-first 产品包装，因为 v0.1 的买单理由仍应来自日常判断质量

### Success looks like
- lab 能持续维护至少 8 个 topic dossier，并在 30 天内不出现“每周重头开始”的感觉
- Dr. Chen 在组会或一对一讨论前，会把 dossier 当成默认入口而不是临时搜索替代品
- Maya 找回“为何之前忽略过某条线索”的时间明显缩短
- 至少出现 2 次“因为 dossier 中的旧留痕被翻出，当前判断被修正”的真实案例

### Honest time estimate
- `9-12 周 @ 20h/week`
- Confidence: `L`
- Unknowns:
  - 用户究竟愿不愿长期维护 dossier，而不只是消费 digest
  - PI 和 Maya 对“同一 topic 两种视角入口”是否会有理解分歧
  - polished 协作体验需要多少轮真实使用修正

### UX principles
- `Differentiation + Polish > Speed`
- `Compounding context > rapid throughput`
- `Shared lab memory > personal convenience`
- `Calm confidence > feature count`

### Biggest risk
这个候选最接近 L2 看到的长期正确形状，但它也最容易在 v0.1 就背上过多期待。只要 delegation 边界、taste feedback 频率、topic dossier 的维护习惯里有任何一个不成立，较长的构建周期就会把学习速度拖慢。它不是“做不到”，而是“可能在真正知道用户信任边界前就做得太完整”。

## 3. Candidate C · “牺牲 Differentiation：高完成度研究简报工作台”

### v0.1 in one paragraph
这是最容易被理解、也最容易较快做得像样的 cut。它把产品定义压回“高质量 team research briefing”：首页给 PI 一个漂亮、明确、可快速浏览的 topic digest，Maya 在背后维护共享阅读队列、简单的 topic 状态卡、留痕归档和一句话 taste feedback。它仍然保留 L2 要求的关键底座，但不会在 v0.1 就把“lab 外置编辑部”的野心全部显化出来，因此差异化最弱。

### User persona (sharpened from L2)
主 persona 是第一次愿意让工具进周会流程的 Dr. Chen，他需要的是低学习成本与体面输出。次 persona 是 Maya，她不想再在多个地方切换，但也不想额外承担“维护一套复杂系统”的心理负担。她更在意顺手，而不是 worldview 级创新。

### Core user stories (3-5)
- As a PI, I can review the top shifts across my core topics in minutes so that I walk into meetings prepared.
- As an operator, I can maintain one shared read queue and one trace archive so that the lab has a single place to return to.
- As a PI or operator, I can mark “agree / disagree + why” on summaries so that personalization begins without friction.
- As an operator, I can promote an old trace back into the active queue so that weak signals are not lost forever.

### Scope IN
- 高完成度的 digest-first 首页，突出本周最该看的 topic 变化
- 基本 topic 状态卡，回答“现在值得关注吗”
- 共享阅读队列 + 留痕归档 + promote/prune
- 低摩擦 taste feedback
- 适合导出或分享给 lab 内部的 briefing 结果
- 基本权限与未来付费层留缝，但不展开商业化设计

### Scope OUT (explicit non-goals)
- 不做深度 dossier 或复杂立场历史，因为这一版选择先把“好用”做到极致
- 不做 map/topology explainer layer，因为它对首版理解成本与差异化收益不成正比
- 不做 onboarding / curriculum 体验，因为这会把产品拉向 Carol 场景
- 不做公共互动层，因为这会破坏私密协作定位

### Success looks like
- Dr. Chen 几乎不需要训练就能把它用进每周例行判断
- Maya 能在较低维护负担下持续更新 8-15 个 topic
- briefing 产物本身就足够体面，愿意直接拿给 lab 内部分享
- 团队不再依赖分散的 newsletter、书签、聊天记录来拼接“这周发生了什么”

### Honest time estimate
- `3-5 周 @ 20h/week`
- Confidence: `M/H`
- Unknowns:
  - 过于熟悉的形态是否会让用户觉得“这只是更好的简报工具”
  - 简化后的 topic memory 是否足够支撑 30 天后的复利感
  - PI 是否真的会因为 polished presentation 而更快建立信任

### UX principles
- `Speed + Polish > Differentiation`
- `Familiar workflow > novel worldview`
- `Presentation quality > memory depth`
- `Low-friction adoption > ambitious behavior change`

### Biggest risk
这个候选最容易出一个“大家都能懂、也愿意先用”的首版，但它也最可能落入“像一个更好的团队 newsletter/workspace”而不是明显不同的新类别。如果第一批用户感受到的是便利，而不是判断质量和记忆复利的跃升，那么它虽然好卖、好展示，却可能把真正的护城河延后得太久。

## 4. Options for ❓ items

### 4.1 ❓ Target delivery
- Path 1: 接受 `3-6 周` 为首发窗口。如果你要尽快把产品放进真实 lab 节奏里试，优先在 `A` 与 `C` 之间选：`A` 更独特但更粗，`C` 更体面但更像熟悉工具。
- Path 2: 接受 `8-12 周` 为首发窗口。如果你要验证的不是“简报工具有人用吗”，而是“lab 级 shared research memory 会不会形成复利”，选 `B` 更诚实。

### 4.2 ❓ Red lines
- Path 1: 把 §5 的 3 条主红线全部升格为 v0.1 硬宪法，optional 第 4 条只做提醒。这样 scope 最清楚，最适合 `A` 或 `C`。
- Path 2: 把 §5 的 1-2 条设为绝对红线，把第 3 条与 optional 第 4 条设为“v0.1 先遵守、30 天自用后再复核”的阶段边界。这样更适合 `B`，因为它更可能在长期 product shape 上继续生长。

## 5. Proposed red lines (3, basis: L2 §5)

1. **v0.1 不扩成通用论文发现器，只守 8-15 个重点 topic。**
   Basis: L2 明确把“聚焦 topic density”视为价值来源；一旦扩到全域，产品会退化成普通 discovery 工具。

2. **v0.1 只委托 triage，不承诺替代第一手阅读。**
   Basis: L2 把“替代阅读”定义为坏方向；好的方向是帮用户知道什么该读、什么只留痕、什么可以暂时略过。

3. **v0.1 不做公开评分、公开评论市场或论文社交 feed。**
   Basis: L2 把私密与信任视为基础；公开层会把 lab 的 shared brain 变成表演场，而不是判断资产。

4. **Optional: 不把 graph/map 当唯一首页入口。**
   Basis: L2 已经把 digest-first 视为首页默认，map 只能是 second-order explainer layer。

## 6. Questions that need real user interviews

- PI 真正想买的是“每周节省判断时间”，还是“让 lab 形成可继承的研究立场资产”？这决定 `A/C` 还是 `B` 更合理。
- Maya 这类 operator 愿意以多高频率留下 “why I disagree” 这类显式信号？如果频率太低，hybrid taste learning 只能停在口号。
- 当系统说“这批工作先 skip、只留痕”时，PI 与 operator 的信任边界分别在哪里？他们接受 summary，是否也接受 filtering？
- 低价值留痕应该主要归在个人层，还是 topic 共享层？如果这点错了，之后会出现 archive 无人维护的问题。
- 一个 lab 自用 30 天，是否已经能产生足够强的复利感，还是必须有更长周期才会显出差异？这关系到首发成功标准应设多高。
