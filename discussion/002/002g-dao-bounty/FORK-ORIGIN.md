# Fork origin

**This fork**: 002g-dao-bounty
**Forked from**: 002 · L1(crypto pivot 菜单)
**Source stage doc**: ../L1/stage-L1-inspire.md
**Selected candidate**: Direction 7 · "DAO Bounty as Skill Market / DAO 链上技能市场"
**Candidate description (extracted from source)**:

Dework / Superteam / Layer3 等平台已经是成熟的 bounty 基础设施。你作为一个 **已有链上可验证技能的人**(会写 solidity / 能做调研 / 能设计 / 能写内容),**系统化地接单**:每日接 1-2 个 100-500 USDC 的 bounty,累计 $100/天达成。不创业、不搭产品,就是 **在现有 DAO 技能市场里做一个高接单率的 operator**。

核心 framing:**认知跳跃最小的一条**——human 如果熟悉 crypto,自己可能也会想到这条路径。它的价值在于作为其他方向的 **fallback baseline** 和 **启动期现金流保底**——即使 002b / 002f 都跑不通,只要有可验证技能,这条底线就不破。

**Spark(不是方向 spark,而是组合 spark)**:
- 启动门槛清楚、每日可度量、失败惩罚小——是菜单里 **最"直接"** 的一条
- 作为 002b / 002f 客户积累期的 **现金流兜底**,避免"三个月没收入就破功"的心理崩盘
- 接单过程天然积累链上可验证 track record,可以直接喂给 D4 On-Chain Operator-in-Residence(若未来有兴趣 fork)

**Sources**:
- Opus L1R2 §3 #2 验证(skill-gated 可行但未进 Top 3)
- GPT L1R2 §3 #4(双方都列为 basis 但 spark 弱)
- 双方判断一致:**作为主线 spark 不够,作为 fallback 极其可靠**

**Value validation evidence**(摘自菜单):
- Dework 累计分发 $1.2M+ 奖励([DAO Times 2025](https://daotimes.com/dework-dao-tool-report-for-2025/))
- Superteam 上 100-1000+ USDC 的内容 / 设计 / 开发 bounty 常见([Superteam 示例](https://earn.superteam.fun/listing/tokenised-vaults-ugc-video-bounty/);[Dework](https://dework.xyz/))
- 全职 DAO 雇佣岗位存在([CryptoJobsList 2025](https://cryptojobslist.com/blog/dao-jobs-future))

**Failure cases**:
- **Skill-gated**——没有链上可验证技能的人直接起不来;技能缺口要先补
- **收入高度非恒定**(接不到就 0)——不是产品收入曲线,是 freelancer 收入曲线
- **议价权低**——作为 operator 被 DAO 市场定价,很难跳出时薪逻辑
- **锁死风险**(menu Cluster C 提到):警觉 D7 反客为主,把人锁死在低议价接单工人状态

**Forked at**: 2026-04-23T15:57:45Z
**Forked by**: human moderator (via /fork command · 三条并行 fork 之一)
**Rationale** (human 可自行补充):

[ 选择理由:D7 作为 002b / 002f 的 skill fallback。启动期可能需要 2-3 个月才能攒够 002b 的 20 个客户,D7 在这段时间维持 $100/天底线,并天然累积 crypto 可验证 track record。当 002b / 002f 稳定后,D7 自然可以退场或转为客源 funnel。 ]

---

## What this fork is for

现在 `002g-dao-bounty` 是独立 sub-tree。下一层 L2(Explore)会把这条方向的 **skill 具体化(哪些技能门槛最低但接单率最高)、接单节奏、时薪曲线、与 002b / 002f 的协同窗口、何时该退场** 挖透——**继续不讨论 tech / feasibility / cost**。

下一步:

```
/explore-start 002g-dao-bounty
```

## Sibling forks (for cross-reference)

本次并行 fork 的兄弟分支(均 from 002 L1):
- **002b-stablecoin-payroll** — Direction 2 · routine 服务(D7 的"毕业目标")
- **002f-payroll-er** — Direction 6 · acute 急诊(D2 伴生切面)
- **002g-dao-bounty**(本 fork)— Direction 7 · skill fallback

**与 002b / 002f 的关系**:D7 不是独立主线,是 **启动期的 skill-based 现金流兜底 + track record 积累轨道**。三条 fork 组合的设计意图是:
- **今天可跑**:D7(有技能就能接单)
- **3-6 个月攒客户**:D2(routine 服务 scale 到 20 客户)
- **D2 稳定后自然升级**:D6(acute 事故响应变现单次高)
- **D7 在 D2 稳定后退场或转为客源 funnel**

**L2 阶段特别 open question**:D7 和 D2/D6 之间是否存在"共享客户"的路径?比如接一个 DAO 的 bounty,顺势把 D2 的发薪服务推销进去。这是 L2 需要探索的"三条 fork 之间的 user journey 缝合"问题。
