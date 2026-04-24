# Idea 002b-stablecoin-payroll · L3R1 · GPT-5.4 xhigh · Scope(no search)

**Timestamp**: 2026-04-24T01:10:27Z
**Inputs read**: `proposals/proposals.md`, `discussion/002/002b-stablecoin-payroll/FORK-ORIGIN.md`, `discussion/002/L1/stage-L1-inspire.md`, `discussion/002/002b-stablecoin-payroll/L2/stage-L2-explore-002b-stablecoin-payroll.md`, `discussion/002/002b-stablecoin-payroll/L2/pseudo-interview-002b.md`, `discussion/002/002b-stablecoin-payroll/L3/L3R0-intake.md`, `.claude/skills/scope-protocol/SKILL.md`, `CLAUDE.md`, `AGENTS.md`
**Searches used**: NONE
**Visibility**: 未打开或采纳对方 L3R1 文件

## 0. How I read the intake

intake 的核心不是“要不要做稳定币发薪”，而是**先服务谁，才能在 2-3 个月内跑出 10-15 个真实客户**。四条 red lines 已经把边界锁死:不碰钱、不碰税法责任、不接大公司/全职 payroll、不做 all-USDC；真正的张力来自另外四条现实约束:亚太时差、无 CPA、无 DAO 网络、几乎无 crypto 操作经验。所以三条 candidate 必须沿同一根轴分化: **DAO 火花 vs 分发可达性 vs 学习坡度**。我会保留 DAO-first 的最强定位，也会诚实给出更贴 human 现实的 cut。

## 1. Candidate A · “DAO Async Desk / DAO 异步发薪台”

### v0.1 in one paragraph
只服务 **2-15 人、contractor-heavy 小 DAO** 的月度 concierge。客户在 IM 里给你名单变动与例外，你回交一份可审批的发薪包、混合 payout 说明与归档 memo。卖点不是快，而是**把 DAO 月末 chaos 变成固定仪式**。

### User persona (sharpened from L2)
Lena，柏林 9 人链上研究 DAO 的 ops lead。她最怕月底 Google Sheet、多人审批和 contributor 追问同时爆。

### Core user stories (3-5)
- As a DAO ops lead, I can 用一条月度变更消息启动本月流程 so that 我不用重拼整张表。
- As a signer, I can 收到一份可审批的发薪包与例外摘要 so that 最终确认集中在一次。
- As an ops lead, I can 留住每位 contributor 的 payout 偏好与沟通口径 so that 每月不用重复解释。

### Scope IN
- 月度/双周 recurring contractor payout 服务
- contributor 名单、偏好、例外的固定 intake 节奏
- hybrid payout 说明、确认包、发薪后 memo
- 异步服务窗口与固定响应口径

### Scope OUT (explicit non-goals)
- 不做同日救火
- 不决定薪酬，只执行已确认名单
- 不做全职 payroll、token vesting、custody、税法责任

### Success looks like (observable outcomes)
- O1: 2-3 个月内有 8-10 个小 DAO 团队进入标准节奏
- O2: 至少 5 个团队完成第二轮 recurring 发薪
- O3: 每次发薪都有同格式确认包与 memo
- O4: 至少 3 位 ops lead 明确说价值是“少一次月末混乱”

### Honest time estimate under human's constraint
- 若坚持“从 0 网络起步 + 2-3 个月拿到 10-15 个 DAO 客户”，更像 **13-15 周 / 390-450 小时**。
- Confidence: 低。难点在信任建立、DAO 冷启动和 operator 自身 crypto ramp-up 同时发生。
- 结论: **不适合当前 240-360h 预算，但它的 spark 最强，值得保留对比。**

### UX principles (tradeoff stances, not designs)
- 组织仪式感 > 发薪速度
- 异步清晰 > 实时陪跑
- 少而稳的标准包 > 每家都定制
- hybrid 正常化 > crypto 纯度

### Biggest risk to this cut
最大风险不是市场，而是**你得在最不熟的人群里先证明自己**。DAO 客户对链上基本功和语境很敏感，而你同时没有 DAO 分发网络与 crypto 操作积累。

## 2. Candidate B · “Founder Payroll Sidekick / Founder 发薪副驾”

### v0.1 in one paragraph
cohort 改成 **3-10 名跨境 contractor 的 founder-led 小团队**，尤其是欧洲或 crypto-adjacent remote startup。产品不是“Web3 payroll 专家”，而是一个极轻的 recurring service: founder 只给变更，你负责把发薪准备、贡献者沟通、混合 payout 口径和归档做顺。

### User persona (sharpened from L2)
Mateo，里斯本 6 人 AI 工具 startup 的 founder。团队跨 4 个国家，有人收部分 USDC，有人坚持法币。

### Core user stories (3-5)
- As a founder, I can 只提交本月人员与金额变更 so that 发薪不会重新占掉我一个下午。
- As a founder, I can 为不同 contractor 选择不同 payout 轨道 so that hybrid 成为默认而不是例外。
- As a founder, I can 复用同一套 onboarding 与变更说明 so that 新人加入时不会手忙脚乱。

### Scope IN
- 面向 founder 的 recurring contractor payroll concierge
- monthly change intake、contributor FAQ、hybrid payout 偏好整理
- 发薪前确认清单、发薪后归档包、标准沟通模板
- IM 为主、Notion/Drive 为辅的轻交付
- 首 3 个免费试点后的标准收费包

### Scope OUT (explicit non-goals)
- 不做 DAO 治理、社区 ops、token 分配
- 不做实时 emergency room
- 不碰 compensation strategy、税务建议或法律解释
- 不做大团队、全职员工和纯 all-USDC 方案

### Success looks like (observable outcomes)
- O1: 2-3 个月内有 10-12 个 founder 团队进入标准月度流程
- O2: 至少 4 个团队从免费试点走到第 2 次复用
- O3: 至少一半客户把“省心”而不是“省手续费”说成第一价值
- O4: 贡献者端对 hybrid 与记录方式没有持续抱怨

### Honest time estimate under human's constraint
- **9-10 周 / 270-320 小时**。
- Confidence: 中。它仍然需要 crypto ramp-up，但 cohort 更接近可触达的 founder/remote 小团队，不必先拿 DAO 身份背书。

### UX principles (tradeoff stances, not designs)
- 可复制 > 炫目的 niche 叙事
- founder 的安心感 > crypto 术语密度
- boring professional > web3 太野
- monthly rhythm > 高频打扰

### Biggest risk to this cut
这条最现实，但也最容易失去锋利度。若 ritual、文案和边界不够清楚，客户会把你理解成“稍懂稳定币的执行助理”，而不是值得持续付费的 payroll-ops 服务。

## 3. Candidate C · “Proof-to-DAO Wedge / 先样板后 DAO”

### v0.1 in one paragraph
这不是两门生意，而是**一条两段式 scope**。前 4-6 周先服务最容易接触到的 crypto-adjacent founder 团队，跑出 3 个免费样板并补 operator 的 crypto 基本功；后 6-8 周把同一套服务语言转成 “DAO-ready contractor payroll concierge”，带着样板与 SOP 去切小 DAO ops。

### User persona (sharpened from L2)
Ivo，阿姆斯特丹 5 人 crypto tooling studio 的 founder。团队还不是正式 DAO，但协作方式已经像 DAO。

### Core user stories (3-5)
- As a small crypto-adjacent founder, I can 在不改变团队支付习惯的前提下，把 recurring payout 流程标准化 so that 我先把月末 chaos 压下去。
- As a founder, I can 用同一套规则覆盖法币与稳定币 so that 团队不需要 all-in crypto 才能用这项服务。
- As a later-stage DAO-style team, I can 看见真实样板后决定是否切换 so that 我买的是被跑通的流程，不是概念。

### Scope IN
- 前段: 3 个免费样板客户、统一 SOP、统一交付包
- 后段: 以 “DAO-ready” 叙事切入小 DAO / collective / research team
- 同一套 hybrid payout 规则、月度节奏、例外处理与归档模板
- 明确的转介绍请求与 case-study 节点

### Scope OUT (explicit non-goals)
- 不并行服务多种完全不同的客户形态
- 不做一次性救火、咨询式审计或社区治理服务
- 不把 v0.1 做成 agency 大杂烩
- 不承诺在 2-3 个月内同时做深 founder 市场和 DAO 市场

### Success looks like (observable outcomes)
- O1: 前 6 周拿下 3 个免费样板并完成至少 1 轮 recurring 发薪
- O2: 第 7-12 周总客户数达到 10 个左右，其中至少 3 个是 DAO-style 团队
- O3: 形成 2-3 份能复用的 case study / onboarding narrative
- O4: 第 3 个月结束时，可以明确判断是否继续转向 DAO-first

### Honest time estimate under human's constraint
- **10-11 周 / 300-340 小时**。
- Confidence: 中低。它比 B 更复杂，但仍装得进预算；前提是你严格把“样板期”和“DAO 切入期”切开，不临时扩 scope。

### UX principles (tradeoff stances, not designs)
- 先证明可交付 > 先占最性感的 niche
- 同一套服务骨架 > 每段换一套说法
- 学习速度 > 品牌纯度
- 样板可信度 > 口头定位

### Biggest risk to this cut
最大风险是**身份稀释**。前半段太 generic，后半段转 DAO 会生硬；一开始太 DAO，又拿不下样板客户。

## 4. Options for the human's ❓ items

### ❓1 cohort 最终确定
- **Option A: 纯 DAO ops**。火花最强，长期定位最清楚；代价是起步最慢、信任最难。
- **Option B: founder-led 小团队**。最贴近 human 现实约束；代价是 differentiation 弱一些。
- **Option C: 两段式**。先拿样板再转 DAO；代价是 positioning 管理更难。

### ❓2 定价 anchor
- **Option A: 第 4 客户起 $360/月 flat**。最利于快速转化，但可能把自己锁进低价助理心智。
- **Option B: 第 4 客户起 $480/月 core**。我认为最平衡，既不像 SaaS，也没有直接跳到 boutique accounting 档。
- **Option C: $720/月 high-touch**。只适合极窄 cohort；以 human 当前 cred 与时间，不建议作为 v0.1 默认。

### ❓3 crypto ramp-up 时间
- **Option A: 前 2 周专门学习期**。先补基本功，再碰客户；最稳，但会压缩获客窗口。
- **Option B: 每周固定 30% 时间边做边学**。更符合 2-3 月目标，但风险是同时承压。
- **Option C: 用 3 个免费样板当 dogfood 学习期**。最贴近真实交付，但要求你敢把 learning 明确塞进 beta 定义。

### ❓4 若坚持 DAO cohort，funnel 从哪来
- **Option A: 内容型**。公开写“小团队 hybrid payroll checklist / 月末 chaos 拆解”，吸引 ops lead 私聊。
- **Option B: 劳动型**。先在 bounty / ops support / contributor admin 里出现，再顺势接 recurring 发薪。
- **Option C: 工具邻接型**。围绕已经在用相关工具或模板的人群切入，卖“有人帮你把它跑顺”。

### ❓5 如果换 cohort，换哪个
- **Option A: 欧洲或 crypto-adjacent remote founder 团队**。最契合时差与异步协作。
- **Option B: 像 DAO 一样协作、但还没正式 DAO 化的小 collective / studio**。最适合 Candidate C。
- **Option C: 跨境 agency**。只有在你发现他们的 recurring 痛点强于公开信号时才考虑，不建议默认。

## 5. Red lines

human intake 的 4 条 red lines 已足够强，我只补 2 条明显缺的:

1. **不承诺“当日救火”或 24/7 实时响应**。你住亚太、服务欧美，若把紧急事故混入 v0.1，会直接把 scope 撕裂；那是 002f 的地盘。
2. **不替客户决定薪酬、奖金、贡献评级或雇佣关系归类**。这不是细枝末节，而是为了守住“执行与记录，不代替判断与责任”的边界。

## 6. Questions needing user interviews

1. 哪类客户会最先信任一个**无 CPA、住亚太、以异步为主**的 operator 来接 recurring payroll-ops？
2. 客户在 **$360 / $480 / $720** 三档上，分别会把这项服务理解成什么:助理、bookkeeper，还是值得长期留存的 ops wedge？
3. 对目标客户来说，真正最痛的是“月末混乱”“贡献者对专业度的感受”，还是“自己不想处理 hybrid payout 解释”？
