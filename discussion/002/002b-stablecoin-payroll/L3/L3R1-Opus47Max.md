# Idea 002b-stablecoin-payroll · L3R1 · Opus 4.7 Max · Scope(no search)

**Timestamp**: 2026-04-23T23:42:00Z
**Inputs read**: L2 explore report · L3R0 intake · L2 pseudo-interview · FORK-ORIGIN
**Searches used**: NONE in this round
**Visibility**: did NOT read GPT-5.4's L3R1

---

## 0. How I read the intake

Human 给了一份**异常坦诚**的 intake:30+h/周 · 2-3 月 MVP · Signal 极轻交付 · 4 条红线全接 · 放弃 speed 但要 polish+简运营+differentiation 三选;但在 freeform 里自曝了四条会直接撕裂原 scope 的 ground truth——**住亚太服务欧美 / 无 CPA / 无 DAO 网络 / 几乎无虚拟币操作经验**。

Hard constraints 我全部遵守。**最大冲突**是:L2 证据最强的 cohort(小 DAO ops)与 operator 的现实网络 / crypto 经验两条约束直接相矛盾。L3R1 我不装作没这个冲突——三条 candidate 必须沿"**cohort vs operator 现状**"这条轴分化,让 human 在看到具体 trade-off 后自己裁决。

Unknowns 我全部提选项:定价($480 vs $360 vs 分档)、crypto ramp-up(集中 vs 并行 vs dogfood)、cohort funnel(具体 0→10 的路径)、换 cohort 去哪、两段式策略。红线 human 已命名完整 4 条,我不补提。

---

## 1. Candidate A · "DAO Ops First · 硬啃 cohort 最强证据"

### v0.1 in one paragraph
坚持 L2 公开证据最强的 cohort(2-15 人小 DAO ops),**直面 operator 无网络 + 无 crypto 经验的双重门槛**。v0.1 = 3 个月内从 0 到 8-10 客户,产出一份可复制的 **"DAO ops payroll SOP v1"** 和 operator 本人的 crypto 操作能力 upgrade。启动 30 天投入主要给 ramp-up(Safe / multisig / Superfluid / Request Finance / Coordinape / Utopia 实操熟练)和通过 002g DAO bounty 在多个 DAO 内自然渗透。第 31-60 天获取前 3 免费客户,第 61-90 天把产品/定价/SOP 打磨稳再接第 4-8 付费客户。

### User persona(sharpened from L2)
**Arjun**,12 人链上分析 DAO 的 ops lead,住欧洲 / 拉美 / 东南亚其中之一(时差对亚太 operator 友好),每月给 12 个 contributor 发 $35k USDC 预算,目前用 Gnosis Safe + Excel + Discord 三件套硬拼,每月一整天处理地址 / OKR / 审批 / 月报,最折磨他的不是金额是**"大家都默认我记得每个人上个月说过的话"**——每月在偿还一笔组织记忆的解释债。

### Core user stories(3-5)

1. **S1 · 月度 payroll 流程**:作为 DAO ops lead,我可以每月 25 号在 Signal 和 concierge 同步 (a) 名单变动、(b) bonus/deduction、(c) 新 contributor 引导,concierge 28 号给我一个打包好的 Safe tx batch,我一键确认即可发薪。
2. **S2 · 例外处理**:作为 DAO ops lead,当有 contributor 要改链 / 拆收 / 延期,我 Signal 告诉 concierge,由 concierge 统一记录并在下次 payroll 正确执行。
3. **S3 · 月度 treasury 报告**:每月月底 concierge 交付一份可直接给 token holder 公开的月度 treasury report(谁收了多少 · 何时发 · on 哪条链 · 汇总)。
4. **S4 · 新 contributor onboarding**:新 contributor 加入时 concierge 引导 contributor 完成 KYC / tax form / wallet 确认,帮 DAO ops 接住第一次摩擦。
5. **S5 · 季度 liability hygiene 检查**:每季度 concierge 产出一份"这个 DAO 本季度 payroll 合规 hygiene 清单"(不承担法律责任,只是 checklist),flag 任何需要补的文档。

### Scope IN(v0.1)
- Signal/TG + Shared Notion workspace(每客户一个)
- SOP 文档:onboarding checklist · 月度 payroll run checklist · 地址变更流程 · contributor offboarding 流程 · 季度 hygiene 清单
- Safe multi-sig + Request Finance invoice batch 作为**客户操作工具**(concierge 只 guide,不签名、不碰 key)
- 月度 treasury report 模板(每客户可 fork + 对外公开)
- 支持主链白名单:Ethereum mainnet / Base / Arbitrum / Optimism(其他链 v0.1 拒绝)
- 稳定币白名单:USDC / USDT(v0.1 不支持 DAI / 其他)
- Hybrid payout 支持:contractor 可选 USDC 或 Wise USD(operator 帮 DAO 配路由,不做货币兑换)

### Scope OUT(explicit non-goals)
- ❌ 不做 Web dashboard / 独立产品 / 客户门户
- ❌ 不碰客户 Safe private key / 不签 multi-sig / 不保管助记词
- ❌ 不做税务申报本身,只整理文档(IRS 红线)
- ❌ 不接 >20 contributor 的 DAO(规模上限,防止被拖入 EOR 级复杂度)
- ❌ 不做 token vesting / airdrop / treasury investment advisory(是另一行业)
- ❌ 不承诺追回丢失资金(事故响应是 002f 的事)
- ❌ 不强推 all-USDC;若客户坚持只发 USDC,concierge flag 此为 risk 并书面 disclaimer
- ❌ 不做中国大陆客户(KYC / 监管不适配)

### Success looks like(observable outcomes)
- **O1**:第 90 天有 ≥6 付费客户(前 3 免费 + 3 付费起步),月营收 ≥ $1800($600/月 × 3)
- **O2**:每客户月度 payroll run 的 operator 实际投入 ≤ 3 小时(SOP 成熟度标尺)
- **O3**:零 custody 事故(operator 从未签过 tx、从未持有过客户 key)
- **O4**:零合规责任事故(operator 从未对客户的税务文件签字背书)
- **O5**:≥ 3 个客户在 Twitter / Farcaster / Discord 自发提及 concierge(organic referral signal)

### Honest time estimate under human's constraint
**8-12 周,confidence Medium-Low**。给定 30+h/周 × 12 周 = 360-480 小时:
- **Week 1-4 · Ramp-up + 第 1 客户**:~150 小时(crypto 操作栈自学 80h + 通过 002g bounty 接 2-3 单 40h + 第 1 免费客户 onboarding 30h)
- **Week 5-8 · 第 2-4 客户**:~150 小时(3-4 客户 onboarding 90h + 2 客户月度 payroll run 40h + SOP 产出 20h)
- **Week 9-12 · 打磨 + 第 5-8 客户**:~150 小时(4 客户月度 payroll run 60h + 新客户 60h + 定价结构调整 + 第 1 次退客户 / 改客户 30h)

**Confidence 打 Medium-Low 原因**:
- 🚨 最大未知是 "operator 通过 002g bounty 渗透 DAO 内圈" 的实际 funnel 效率——可能 4 周进 3 个 DAO 的 ops 内圈,也可能 4 周还没进任何一个
- 🚨 crypto ramp-up 曲线对无经验者通常是 2-3 个月,80h 集中学习可能不够——可能需要把 client work 向后推
- 🚨 "住亚太服务欧美 DAO"——DAO 分布倾向 UTC-5 至 UTC+2,亚太 operator 的工作时段是客户的深夜或凌晨,**异步能支撑大部分但不是 100%**

### UX principles(tradeoff stances)
- **Polish · 强**:每次客户触点必须像"有个靠谱的人"—— Signal 回复 24h 内、SOP 文档格式统一、月报有设计感
- **运营简单 · 中**:SOP 优先于个性化——每客户有基础模板 + 小量定制,不做"每客户独特一套"
- **Differentiation · 强**:对标时强调 "人格化 + 无 all-USDC 张扬 + 时差覆盖 + 专治 DAO 特殊 payroll"
- **Speed · 放弃**:第 1 客户在第 4 周才上,接受

### Biggest risk to this cut
**Funnel 风险高于产品风险**。product risk 是可管理的(SOP 迭代)、operator capacity 风险是可管理的(full-time 30+h);但 "**无 DAO 网络 + 无 crypto 经验的亚太 operator,如何 3 月内进入 8 个 DAO 的 ops lead 微信圈 / Discord 内圈 / Telegram 小群**" 这一步,在 L3 无法用 desktop research 证明可行。最坏情况是 Week 4-8 出现 "客户 funnel 冷启动失败",此时 candidate A 退化成 "我有一份漂亮 SOP 但没人买"——**这是真正的失败模式**。

---

## 2. Candidate B · "Network-First · 换到 operator 已熟悉 cohort"

### v0.1 in one paragraph
**反转 cohort 选择**,诚实接受 operator 现实:**无 DAO 网络 = DAO 不做 v0.1**。转向 operator 可能已有或较易触达的 cohort——**欧洲远程 SaaS / AI 独立 founder + indie hacker 圈里的跨境团队**。这类客户对 stablecoin 接受度比"全无 crypto"客户高(YC SAFE 自 2026 支持 USDC),但 operator 不必是 crypto-native 就能卖 concierge 服务——因为他们也不是 crypto-native。v0.1 的 framing 从 "DAO payroll concierge" 换成 "跨境 contractor payroll concierge for crypto-curious SaaS founders"。

### User persona(sharpened from L2 + swap)
**Javier**,29 岁,从 YC W26 batch 拿 $500k USDC SAFE 融资,注册 Delaware C-corp,6 个 contractor 分散在美国 / 印度 / 波兰 / 阿根廷 / 越南,本人住西班牙巴塞罗那。第一次发薪就炸——税表 / 链选 / 汇率 / 平台费全部一起冒出来。他不是 crypto-native,但 YC 圈里"用 USDC 发 contractor"已成话题;他读过 Deel 但嫌 per-seat 贵,试过自跑但炸过一次。

### Core user stories(3-5)

1. **S1 · routing matrix 设计**:作为 founder,我可以第一次和 concierge 20 分钟 onboarding,让 concierge 给我一份 per-contractor routing matrix(谁走 USDC on Base · 谁走 Wise USD · 谁要什么 tax form)。
2. **S2 · 月度 batch run**:每月 25 号前在 Signal 和 concierge 确认当月名单 / bonus,concierge 在 28 号给我一个打包的 Request Finance invoice set + 一键 approve 链接。
3. **S3 · 年底税务准备**:年底 concierge 产出 1099-NEC 草稿 + 按 contractor 的地区分类的文档清单(我自己找会计过目签字,concierge 不背书)。
4. **S4 · 新 contractor onboarding**:新加 contractor 时 concierge 引导我问清 payout 偏好 / tax 身份 / 时区,更新 matrix。
5. **S5 · 季度成本 review**:每季度 concierge 给我一份对比 report(如果全走 Deel 会花多少 vs 实际花了多少),让我感受省了多少 + flag 任何该调整的 routing。

### Scope IN(v0.1)
- 与 A 相同的 tool stack(Signal + Notion + Request Finance + Wise + Safe for crypto leg)
- **加**:Wise / Payoneer 整合的 fiat leg(因为这个 cohort 一半客户会有 W-2 / 1099 型员工)
- SOP 文档:per-contractor routing matrix 模板 · 月度 run checklist · 年底 1099 草稿 checklist
- 支持主链 & 币:同 A(Base / Arbitrum / OP / mainnet · USDC/USDT)
- Hybrid payout 默认:**一半客户的一半 contractor 走 fiat rail**,concierge 不歧视

### Scope OUT(explicit non-goals)
- ❌ 不做 DAO ops v0.1(延后到 v0.2 或另开 fork)
- ❌ 不碰 key / 不签 tx / 不托管
- ❌ 不做税务申报 / 不假装 CPA
- ❌ 不接 >10 contractor 的客户(规模上限)
- ❌ 不做 equity grant / vesting
- ❌ 不中国大陆客户

### Success looks like
- **O1**:第 90 天有 ≥8 付费客户(前 3 免费 + 5 付费),月营收 ≥ $2400($480 × 5)
- **O2**:每客户月度 run ≤ 2 小时(payroll complexity 比 DAO 低)
- **O3**:≥ 2 客户来源于 YC / Indie Hackers / Twitter 公开曝光(非冷启动 cold reach)
- **O4**:零 custody / 合规责任事故
- **O5**:operator 同期 crypto 操作栈 mastery score 达到 DAO ops cohort 最低门槛(为 v0.2 切 DAO ops 做准备)

### Honest time estimate
**6-8 周,confidence Medium-High**。给定 30+h/周 × 8 周 = 240 小时:
- Week 1-2 · 对 fiat(Wise/Payoneer)+ crypto leg 基础栈熟练 + 第 1 免费客户 → 60h
- Week 3-4 · 第 2-3 免费客户 + SOP v1 产出 → 60h
- Week 5-6 · 第 4-5 付费客户 + 定价结构调整 → 60h
- Week 7-8 · 第 6-8 付费客户 + referral funnel 构建 → 60h

**Confidence 高于 A 的原因**:
- ✅ Cohort funnel 有现实路径:YC 公开 batch 校友网络 / Indie Hackers 发 thread / Farcaster / Twitter 建设者圈——operator 住亚太也能触达
- ✅ Crypto 操作栈要求较低(客户本身不 crypto-native,只需 USDC on Base/Arb 基础操作)
- ✅ 客户价格接受度可能更高(YC founder 有资本,比 DAO ops 的 treasury 决策链短)

### UX principles
- **Polish · 强**:YC 圈客户审美高,SOP 和交付物必须 look professional
- **运营简单 · 强**:SaaS founder cohort 的 SOP 比 DAO 更可标准化
- **Differentiation · 中**:这个 cohort 已有 Deel/Remote 等玩家,concierge 的差异在"**人 > 平台**"—— 但不是最锐利的 spark
- **Speed · 放弃**:6-8 周对比 A 的 8-12 周只快 2-4 周,不牺牲 polish

### Biggest risk to this cut
**Differentiation 被稀释的风险 > funnel 风险**。SaaS founder 是成熟市场——Deel/Remote 已经教育过"有人替我处理 contractor payment",concierge 的 spark 比 DAO ops 小。candidate B 的风险是"容易做但难讲清差异"——3 月后客户可能 churn 到 Deel($49/seat)或一个 cheaper 替代。**需要在 v0.1 就明确 concierge 要讲的那一句"他们不做但我们做"的 thing**——我暂定为 "**一个会讲中文 / 可覆盖亚太时差 / 为 crypto-curious 但不 crypto-native 的 founder 做 bridge 的真人**",但这要在客户访谈验证。

---

## 3. Candidate C · "Two-Stage · 先网络后 DAO"

### v0.1 in one paragraph
**承认 cohort 冲突且两段解决**。v0.1 前 60 天走 Candidate B 的 Network-First 路径(SaaS founder cohort,快速攒 5-6 客户 + crypto 栈 ramp-up + 现金流 baseline)。第 60-90 天开始**用 002g DAO bounty 做渗透**——每周接 1-2 个 DAO bounty 作为 side-gig,顺势进 DAO ops 内圈;同时把 SaaS founder 客户打磨到 10 客户 mark。v0.1 结束时,operator 已有 crypto 栈熟练度 + 7-10 SaaS founder 客户 + 2-3 个 DAO 的熟人通路,**v0.2 再切 DAO ops 作为第二个 cohort**。

### User persona
**阶段 1 · 同 B(Javier);阶段 2 · 同 A(Arjun)**。v0.1 刻意只 operationalize 第 1 阶段,第 2 阶段只攒通路不卖服务。

### Core user stories
1. **S1-S3 · 同 B 的 S1/S2/S3**(monthly routing / batch run / year-end tax prep)
2. **S4(第 60 天起)· 通过 002g bounty 建立 DAO 渗透档**:每周接 1-2 个 DAO bounty,operator 公开 track record 逐步积累
3. **S5 · 跨 cohort 学习**:从 SaaS founder 客户学到的 SOP 抽象为"通用 payroll concierge SOP",为 v0.2 切 DAO ops 复用

### Scope IN(v0.1)
- **阶段 1**(Week 1-8):全部同 Candidate B 的 Scope IN
- **阶段 2**(Week 9-12):加上 002g DAO bounty 接单工具(Superteam / Dework 账号 + profile 建设 + 1-2 个完成的 bounty 作品)

### Scope OUT
- 同 B 全部,加:❌ v0.1 阶段明确不卖 DAO payroll 服务(第 2 阶段只积累通路)

### Success looks like
- **O1**:第 90 天 7-10 付费 SaaS founder 客户 · 月营收 $3000+
- **O2**:第 90 天 operator 已完成 ≥3 个 DAO bounty · 和 ≥2 个 DAO 的 ops 有 1-on-1 对话
- **O3**:operator crypto 栈从 0 到 DAO ops v0.2 门槛之间的距离缩短 70%
- **O4**:零 custody / 合规事故
- **O5**:明确产出 "v0.2 DAO ops 切入计划" 作为 v0.1 deliverable 之一

### Honest time estimate
**10-12 周,confidence Medium-High**。Week 1-8 同 B(240h)+ Week 9-12 额外 150h(其中 100h 客户 / 50h DAO 渗透)= 总 390h。

**Confidence 高的原因**:
- ✅ v0.1 第一阶段 funnel 风险低(SaaS founder 比 DAO ops 易达)
- ✅ 第二阶段 DAO 渗透用 002g bounty 做通路,**不依赖冷启动网络**——是付费式获取通路
- ✅ 承认 operator 现实,不 over-promise,每个阶段的目标**各自可验证**

### UX principles
- 同 B 的 Polish + 运营简单 + Differentiation
- 加:**时间分层**(v0.1 是拼第 90 天的 SaaS founder cohort 成功,不是拼 90 天 DAO ops)

### Biggest risk to this cut
**阶段 2 被阶段 1 吃掉**——SaaS founder 客户如果在 Week 8 已有 5-6 个,需要大量 operator 时间维护 + 扩张,**阶段 2 的 DAO 渗透可能被挤压到 0 小时**。candidate C 的最大风险是"**看起来两段,实际只跑了一段**"——v0.1 结尾时 DAO 通路没有积累,v0.2 启动时依然是零。

**Mitigant**:阶段 2 必须**定量 protection**(每周 10h 强制给 DAO 渗透,不让客户吃掉),否则 candidate C 退化成 candidate B。

---

## 4. Options for human's ❓ items

### ❓1 · Cohort 最终
已在 candidate 层分化为 α(A)/β(B)/γ(C),不再另提选项。human 在看 candidate 后自然裁决。

### ❓2 · 定价 anchor(第 4 客户起的价格)
**三个选项**:
- **Option 2a · 统一 $480/月**(pseudo-interview 建议的 mid-anchor)—— 简单、易解释,第 4 客户起固定价
- **Option 2b · 分三档 $360 / $500 / $700**(按 contractor 数量 5/10/15 分档)—— 与 Humble Accounting 的 $135-$440 逻辑一致,但拉高上限
- **Option 2c · 动态定价 · 前 5 付费客户 $480 flat,然后根据 demand 调**—— 把定价决策推到第 5-8 客户,**最接近 pseudo-interview 的"L4 beta 验证"建议**

**建议 Option 2c · flexible**——given human 无 DAO 网络 + 无 crypto 经验双风险,第 1-5 客户的定价 noise 很大,不适合一开始锁死。

### ❓3 · Crypto ramp-up 时间
**三个选项**:
- **Option 3a · 集中 Week 1-4 全部学习**(80-120h 密集)—— candidate A 路径
- **Option 3b · 并行边学边做**(Week 1 开始就接免费客户,边做边补栈)—— candidate B/C 路径
- **Option 3c · Dogfood 路径**(前 2 周 operator 自己是自己的客户,用假 data 跑完整流程)—— 补充:**强烈建议无论选哪个 candidate 都做 dogfood 前 1-2 周**,把 SOP 在自己身上验证一遍

### ❓4 · DAO ops funnel 路径(若坚持 Candidate A)
**三条具体路径**(都不是 "Twitter 冷 DM",因为冷 DM 对 DAO ops 成功率极低):
- **Path a · 002g DAO bounty 内部渗透**:接 Superteam / Dework 上 contractor-oriented bounty,完成高质量作品,自然被 DAO ops 认识
- **Path b · 公开 thread 法**:Farcaster / Twitter 上每周发一则 "我帮一个虚构小 DAO 跑 payroll SOP 的公开文档"——用"不求不卖"的 positioning 吸引 DAO ops 主动咨询(参考 D5 Reverse Airdrop Farming 的逻辑)
- **Path c · 付费社群门票**:付 $500-2000 买 1-2 个高质量 DAO 社群(Bankless Citizens / Gitcoin / Optimism Collective 等)的 seat,6 个月内在群里建立 reputation

### ❓5 · 若换 cohort,换哪个
candidate B 默认选 **欧洲 + YC/Indie Hackers 圈的 SaaS founder**。备选:**日本/东南亚本地 crypto-curious founder**(亚太时差 0,但网络更小)。备选 2:**Southeast Asia remote-first design agencies**。我不推荐这两条作为 v0.1——因为本地亚太 founder 的稳定币支付意愿比欧美低,而 agency cohort pseudo-interview 证据最弱。

---

## 5. Red lines I'd propose
Human 已命名 4 条完整红线,我不补提。**额外 flag 一条**:human 没命名但值得考虑——

- **(Proposed) 不跨境支付到制裁名单国家(伊朗 / 朝鲜 / 叙利亚 / 俄罗斯等 OFAC 列表)** —— 这不是 human 已 flag 的 "大企业 / CPA / custody / all-USDC" 中任一条,但 2026 跨境 USDC payroll 踩到制裁红线会让 operator 个人承担刑事风险。建议 Candidate 里追加。

---

## 6. Questions that need real user interviews(L3 不能回答)

- **Q1 · 定价弹性的真实 yes/no 点**:$480 对 Javier 是 yes,但他第 4 个月愿意 renewal 吗?需要 ≥ 5 客户跑完 2 个月后才能知道。
- **Q2 · DAO ops 对"非 crypto-native 亚太 operator"的接受度**:Arjun 会因为 operator 不是 crypto-native / 住亚太 就 not hire 吗?这个问题 pseudo-interview 无法回答,只能真实 cold outreach 3-5 个 DAO ops 测反馈。
- **Q3 · "我能讲中文 / 亚太时差"作为 differentiation 的 real cash value**:Candidate B 依赖这条 spark 存活,但它对 Javier 是 "nice to have" 还是 "decisive"?
- **Q4 · Concierge 的续约率基准**:这类服务的 M6 retention 如果 <70%,整个 operator 模型崩(20 客户变 14 变 10 变 7)——这是 L3 看不到的数字,必须 v0.1 跑完后才能得到。

---

## Summary 给 human

三条 candidate 沿"cohort 选择 vs operator 现实网络"轴分化:
- **A · DAO Ops First** —— 尊重 L2 证据强度,接受高 funnel 风险
- **B · Network-First** —— 尊重 operator 现实,用较弱 differentiation 换较稳 funnel
- **C · Two-Stage** —— 承认冲突,90 天内攒 SaaS 客户 + DAO 通路,v0.2 再切 DAO

三者都遵守全部 12 条 hard constraints + 4 条 red lines。最大 tradeoff 轴 = **"cohort spark(L2 证据)" vs "cohort funnel(operator 现实)"**。human 的选择其实是在问自己:**我愿意花 90 天赌一个 possibly-empty 的 DAO funnel,还是愿意用 90 天建立一个 less sparkly 但 executable 的 SaaS cohort 基础?**

候选 GPT R2 之后,由 scope-synthesizer 做 comparison matrix 和最终 recommendation;human 可 fork 1-3 条成 PRD 进 L4。

---

**全文字数**:约 3800 中文字 ≈ 1500 英文词等效(略超上限,因 candidate 三条均需完整 8 小段结构 + ❓5 选项展开)。
**无任何 tech / 架构 / 成本 / API / 实现细节——全部 product-level**。
