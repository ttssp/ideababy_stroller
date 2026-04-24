# Fork origin

**This fork**: 002f-payroll-er
**Forked from**: 002 · L1(crypto pivot 菜单)
**Source stage doc**: ../L1/stage-L1-inspire.md
**Selected candidate**: Direction 6 · "Payroll-Day Emergency Room / 发薪事故急诊室"
**Candidate description (extracted from source)**:

这是 Direction 2(稳定币发薪管家)和 Direction 3(链上事故清创师)之间的 **窄缝切口**。不是长期 payroll 平台,而是 **专门处理"今天就要发薪,但发错链 / 发错地址 / 收款人无法落地"的当日救火**。客户买的是 **周五晚上那一口气**:把打包好的 TX 停住、帮收款人把链桥接正确、把错误交易写成 memo 备案、必要时协调 OTC desk 做补偿。单次救火 $300-800,一周 1-3 单可达 $100/天。

核心 framing:**时间压力 = 定价权**。D2 是 routine 服务(周五前把工资发顺),D6 是 **acute emergency**(routine 崩掉、钱卡在链上、员工明天要交房租的那一瞬间)。这个切面是 **基础设施普及之后长出来的新故障种类**——稳定币 payroll 采用率爬升会线性带来事故率爬升,但大机构(Chainalysis / TRM)只做大客户事故响应,**单笔 payroll 日常错误无人接手**。

**Spark**:这是二阶推理的产物——"基础设施普及 → 新故障种类 → 新急诊市场"。原 proposal 时人不容易想到"生态系统跟随症状"这个思路;必须先承认 D2 为前置,才能看到 D6。

**Sources**:
- GPT L1R2 §5(GPT-only · §5 新方向 · 融合 GPT 的"一类问题终结者" × Opus 的"稳定币 payroll")
- Opus L1R2 虽未独立提出,但在 §4 D2 中铺垫了前置基础设施

**Value validation evidence**(摘自菜单):
- Chainalysis / TRM 做大型机构事故响应,**单笔 payroll 日常错误切面无人服务**(太小太碎)
- Chainalysis 2025 中报:个人钱包受害占 stolen-funds activity 的 23.35%([中报](https://www.chainalysis.com/blog/2025-crypto-crime-mid-year-update/))
- Chainalysis 把 incident response 做成付费品类([Chainalysis 文章](https://www.chainalysis.com/blog/crypto-needs-proper-incident-response/))
- 稳定币 payroll 使用率在爬升(见 002b 前置验证),**事故率必然随之线性爬升**

**潜在风险**:
- 前置条件依赖——002b 级的 payroll 基础设施必须已经在客户中铺开,否则这条方向起步无量
- "承诺追回"是红线(会变骗局),定位必须严格在 **止血 + 取证 + 应急桥接**

**Forked at**: 2026-04-23T15:57:45Z
**Forked by**: human moderator (via /fork command · 三条并行 fork 之一)
**Rationale** (human 可自行补充):

[ 选择理由:D6 是 D2 的 acute 伴生切面,两者共享客户池、共享 user research、共享基础设施前置条件,并行 fork 可以最大化信息复用。D6 的单次定价远高于 D2 routine,是对"单月客户量不够"场景的单价对冲。 ]

---

## What this fork is for

现在 `002f-payroll-er` 是独立 sub-tree。下一层 L2(Explore)将把上面 candidate 视为一个已挑出的方向,做深度 unpack——**继续不讨论 tech / feasibility / cost**。L2 的任务是把 D6 的 **acute emergency 心理模型、时间窗、定价弹性、服务边界("追回" vs "止血"的红线)、与 D2 的客户共享逻辑** 挖透。

下一步:

```
/explore-start 002f-payroll-er
```

## Sibling forks (for cross-reference)

本次并行 fork 的兄弟分支(均 from 002 L1):
- **002b-stablecoin-payroll** — Direction 2 · Stablecoin Payroll Concierge(routine 服务 · D6 的前置基建)
- **002f-payroll-er**(本 fork)— Direction 6 · Payroll-Day Emergency Room(acute 急诊)
- **002g-dao-bounty** — Direction 7 · DAO Bounty as Skill Market(skill fallback 底线)

**与 002b 的关系**:D6 是 D2 的 "acute 伴生切面"。服务同一类客户(2-20 人小团队 / 小 DAO / 独立顾问),但切入时机与心理模型完全不同——D2 是 weekly routine,D6 是 once-in-a-quarter 的紧急时刻。L2 阶段可考虑两条 fork 之间的 user research 复用(见 002b FORK-ORIGIN.md)。

**警惕陷阱**(synthesizer 在菜单中已指出):D2 + D6 服务同一群人时,容易把客户变成"出事就找你"的无底洞——服务边界必须在 L3 PRD 阶段明确划定。
