# Codex Task · 002b-stablecoin-payroll · L3R1(Scope R1)

**Created**: 2026-04-24T00:58:49Z
**Recommended model**: gpt-5.4
**Recommended reasoning_effort**: xhigh
**Estimated tokens**: ~10-16k
**语言**:中文输出

## Your role

你是 GPT-5.4 xhigh,Debater B,L3R1 on **idea 002b-stablecoin-payroll**(稳定币发薪管家 concierge · v0.1 scope)。

L3 的任务:把 L2 的 rich understanding + L3R0 的 human 真实约束,**产出 2-3 个 peer candidate scopes**(每个都是 PRD 骨架级)。L3 **不**讨论 tech / 架构 / stack / API / 成本细节——那些是 L4。

## HARD CONSTRAINTS

1. **NO web search** this round(L3R1 无搜索,L3R2 才搜)
2. **DO NOT read** `discussion/002/002b-stablecoin-payroll/L3/L3R1-Opus47Max.md`(并行独立)
3. **NO tech / 架构 / stack / API / 代码 / framework 选型** 内容——product-level only
4. 每个 candidate 必须是 **peer**(并列 legitimate alternative,不是"主案 + 备选")
5. 每一条 ❓ (unknown)必须在 §4 提 ≥ 2 个具体选项
6. Intake 已命名 4 条 red lines,**无需**在 §5 补提(但若你发现明显漏的红线,可以 propose 1-2 条)
7. 语言:中文

## Read in this order

1. `proposals/proposals.md` ← root idea 002
2. `discussion/002/002b-stablecoin-payroll/FORK-ORIGIN.md` ← fork 来源
3. `discussion/002/L1/stage-L1-inspire.md` ← L1 菜单 Direction 2 描述(仅参考)
4. `discussion/002/002b-stablecoin-payroll/L2/stage-L2-explore-002b-stablecoin-payroll.md` ← **L2 explore report(最重要上下文)**
5. `discussion/002/002b-stablecoin-payroll/L2/pseudo-interview-002b.md` ← 公开素材聚合,替代用户访谈
6. `discussion/002/002b-stablecoin-payroll/L3/L3R0-intake.md` ← **human 真实约束,12 条 hard + 5 条 unknown + 4 条 red**
7. `.claude/skills/scope-protocol/SKILL.md` ← L3R1 模板
8. `CLAUDE.md` / `AGENTS.md`

## Write

`discussion/002/002b-stablecoin-payroll/L3/L3R1-GPT54xHigh.md`

使用 L3R1 模板 6 段:
- **§0 How I read the intake**(1 段。intake 里最 critical 的 hard constraint 和最大矛盾是什么?)
- **§1-3 Candidate A/B/[C]**(2-3 个 peer。每个 candidate 必须包含:)
  - v0.1 in one paragraph
  - User persona(具体到名字 / 公司大小 / 地点)
  - Core user stories(3-5 条,"As a X, I can Y so that Z" 格式)
  - Scope IN(v0.1 包含的)
  - Scope OUT(明确非目标)
  - Success looks like(可观测 outcomes,O1-O5 编号)
  - Honest time estimate under human's 30+h/周 × 2-3 月 = 240-360h budget
  - UX principles(tradeoff stance,不是 wireframe)
  - Biggest risk(一段)
- **§4 Options for ❓ items**(5 条 unknown 每条提 2-3 选项)
- **§5 Red lines**(若你发现 intake 漏的红线,可 propose 1-2 条)
- **§6 Questions needing user interviews**(L3 desktop research 无法回答的,需 real user 数据的题)

**长度**:800-1500 中文字,candidate 多密度大可到 2500-3500 中文字。

## Intake 关键信号(你写 candidate 时必须尊重)

### Hard constraints(12 条)

1. 2-3 月内 v0.1 到 10-15 客户手上
2. 30+h/周 full-time
3. 前 3 客户免费 + 第 4 客户起收费
4. 交付 = Signal/Telegram/WhatsApp 极轻 + Notion/Drive
5. 🚫 不碰 custody
6. 🚫 不假装 CPA / 律师责任
7. 🚫 不接 >50 人 / 全职 payroll
8. 🚫 不要求 all-USDC,hybrid 默认
9. **住亚太 · 服务欧美**(时差硬约束)
10. **无 CPA 资质**
11. **无已存 DAO 网络**
12. **几乎无虚拟币操作经验**

### Priorities(human 选 3 个,明确不选 Speed)

- Polish / UX quality(concierge 感)
- 运营简单(SOP 可复制)
- Differentiation(与 Deel / Rise 的 spark)
- ❌ 明确放弃 Speed

### ❓ Unknowns(必须 §4 提选项)

1. Cohort 最终(DAO ops 证据强 vs operator 无网络的矛盾)
2. 定价 anchor(第 4 客户起收多少)
3. Crypto ramp-up 时间占比
4. DAO funnel 具体路径(若坚持 DAO)
5. 若换 cohort,换哪个

## 建议的 candidate 分化轴(非 binding)

L3R0 里最大矛盾是"**cohort spark vs operator 现实**"。你可以:
- 沿此轴分化(一条 DAO-first / 一条 non-DAO / 一条两段)—— 与 Opus 可能重合
- 换其他分化轴(比如"定价卖深 vs 卖广" / "交付模式纯 IM vs 加 Notion" / "v0.1 服务 2-5 客户 deep 还是 10-15 客户 shallow")—— 提供差异化 cross view
- 两条路都 OK,只要每条 candidate 是 peer、每条 scope 完整、每条对 ❓ 都给 options

**如果 cross 后 Opus 和你沿同一轴,意味着这条轴是 L3R2 的主要仲裁题**——这本身是强信号,不是问题。

## When done

写 `.codex-outbox/20260424T005849-002b-stablecoin-payroll-L3R1.md`:

```markdown
# Codex Outbox · 002b-stablecoin-payroll · L3R1

**Finished**: <ISO>
**Model**: gpt-5.4 / xhigh
**Files written**: discussion/002/002b-stablecoin-payroll/L3/L3R1-GPT54xHigh.md (<字数>)
**Searches run**: 0(L3R1 不允许搜)

## Candidate headlines(每条一句话)
A. <name> — <v0.1 核心>
B. <name> — <v0.1 核心>
[C. <name> — <v0.1 核心>]

## Key tradeoff axis
<你认为 candidate 之间真正分化的那一根轴>

## ❓ items 你提了选项的(哪几条)
- ❓N: 给了 X 个选项

## Proposed red lines(if any added)
- <...>

## Questions needing user interviews(§6 里最关键的 1-2)
1. <...>

## Note for Claude Code
<任何要 Claude 注意的,比如你和 Opus 可能的 overlap / 你特别的切法 / 你对某条 hard constraint 的解读差异>
```

## 重要 · 诚实时间估算

human 的 time budget = 30+h/周 × 8-12 周 = 240-360 小时。

**不要 flatter** human 的预算——如果你的 candidate scope 装不进 360h,写"**这条 scope 需要 500h / 15 周,不适合 human 的 budget,但保留给对比**",然后产一个 reduced scope 真正能 fit 360h 的。

**特别提醒**:human 自述"几乎无虚拟币操作经验"。candidate 必须显式把 **crypto ramp-up 时间** 算进 240-360h 里,不要假装 operator day 1 就会用 Safe / multisig。

## 和 Opus 的期望分化

Opus 的 L3R1 已经写完(你不读它,但作为 "你不重复什么" 的指引,这些是 Opus 已写的):
- 三条 candidate 沿 "cohort 选择" 轴分化:DAO-first / Network-first / Two-stage
- 定价选项:$480 flat / $360-$700 分档 / 动态定价(推 Option 2c flexible)
- ramp-up:集中 Week 1-4 / 并行边学边做 / dogfood 前 1-2 周
- 额外 propose 的红线:不支付到 OFAC 制裁国家

**你不必重复这些**——可以沿同一轴但给不同的 candidate cut,或换一个 cohort-无关的切法(比如按服务深度 deep/shallow、按交付密度 weekly/monthly)让 human 在 L3R2 synthesis 时看到更多元的 tradeoff 选项。
