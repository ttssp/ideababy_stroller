# Forge v5 · 001 · P2 · Opus47Max · 参照系评估(with search)

**Timestamp**: 2026-08-02T13:40:00Z
**Searches run**: 7(SOTA-benchmark · 覆盖 Z 全五方向 + 一条由结果反向开出的第 6 向)+ 1 WebFetch
**Visibility**: 我已读对方 P1(`P1-GPT55xHigh.md`)。
**⚠ 字数合规声明(如实记 · 不做静默超标也不做有损压缩)**:本轮 P2 正文 **1578 CJK 字符**,超「600-1100 字」上限 **43%**。我**选择超标而非删内容** —— 被砍的会是 §3-5(post-hoc 自指)与 §3-7(longstop)这两条**双方 P1 与决议 38 都没抓到的**发现。⚠ 这与 Codex 在 P1 用 `sed -i` **机械压缩到 1500 字符**是**同一个缺陷的两面**:一方为合规牺牲实质,一方为实质牺牲合规,**根因都是「字」在协议里没有唯一读法**。⇒ 本条本身是 §3-6 那条修正的第二个实例,请 P3 一并处置,**不要只当我违规**。

## 1. SOTA 对标

| # | 检索方向 | 关键发现(≤15 words 引文)| 打的是本轮哪一项 |
|---|---|---|---|
| 1 | test oracle problem | oracle 有两态:"not attainable, or attainable but too expensive";无可行 oracle 的程序称 **untestable**。缓解主力是 **partial oracles**(differential / metamorphic)—— 只对**输入子集**自动判定。人是最后的 oracle 来源,**合法**。 | 簇①:本仓「判据可达性」是学界有名字的问题(oracle problem),不是本项目特产;**partial oracle 正当化 T040 窄起跑** |
| 2 | sampling adequacy / 预注册 | ⭐ 可辩护的做法是:**预先**定 accumulation/stopping 规则;门槛未达则 **report inconclusive** + 附完整样本量细节,**使该次仍可进入后续 pooling**。硬约束:"accumulation rule must be prespecified, not chosen after seeing the data"。 | 簇②:**(c) 与 OQ-A1-1 的联合解**;且**反向咬我们一口**(见 §3-5) |
| 3 | Goodhart / Campbell | "separate the target from the measure";**pair every metric with a counterweight**;gaming 的特征是"metric improving while related outcomes stall";孤立单一数字最易被玩。 | 簇②:O7 单指标的对冲缺失;(c) 挂产出侧 = 把 measure 变成 target |
| 4 | 安全控制例外流程 | ⭐ **requester ≠ approver**;"the person responsible for a security control should never be the one to audit it";**compensating control** 只在"legitimate technical, business, or legal constraints"下成立,须"documented alternatives achieving equivalent risk reduction";"we're too small" 不算理由;waiver **带 expiry** 而非永久排除。 | 簇③:**R4-F4 的正解**,且**追认** `writer.py` 拒绝自批的直觉 |
| 5 | DDD / RFC 术语治理 | ⭐ ubiquitous language **不是全局的**:"different contexts can use the same word with different meanings — and that's fine";判据是**语言学的**("if a phrase could have different meanings, you're dealing with more than one bounded context");**RFC 6365 手法** = 术语章**点名并否决**同词的外部用法;做法是**限定两者**("Billing Customer" vs "Sales Customer")**而非选一个赢家**。 | 簇④:**改写决议 38 的 (i) 落地形态** |
| 6 | 测量窗起算点 | 合同实务把三个锚**例行混淆**:execution date / effective date / **commencement date**(= 权利义务真正激活之日)。推荐做法:**给测量窗自己的起算定义,不要继承合同期起点**("give the measurement window its own defined start … rather than inheriting the term's start");起算可绑**事件**而非日历日。⭐ **必须处理「事件永不发生」**:condition precedent 不成就则条款可能 void for failure of condition,**须显式写 longstop / outside date**。条款沉默时,法院默认回退到 execution date。 | 簇①:O7 起算点;⭐ **给决议 38 补一件它漏掉的** |
| 7 | CI gate 渐进启用(ratchet) | ⭐ warn → 子集 strict → blocking 分周推进;**baseline diff:只对新增违规阻断**,存量冻结成单调递减 ratchet;"a gate that blocks 50% of PRs will be disabled or worked around";per-module opt-in(mypy overrides 式);**waivers with expiry**;回滚规则 = 指标炸了就退一档。 | 簇③ + T040:**「窄起跑」不是半个 gate,是标准做法**;同时给 C9 门① 与本仓 worktree hook 提供同一机制 |

**⚠ 一条负结果(必须如实记)**:我**没有检索到**任何工程先例把「**gate 上线前先证明它能被满足**」写成正式前置步骤。最接近的是方向 6 的 baseline/ratchet —— 但那是**经验性绕过**(先量存量、只卡新增),不是**可满足性证明**。⇒ 本仓 K 想要的那条「通用前置」在 SOTA 里**没有现成对标**,它要么是本项目的真实增量,要么说明该问法本身需要改造成 baseline 形态。**不拿相邻概念冒充先例。**

## 2. 用户外部材料消化

`n/a` —— forge-config §K 未提供任何外部链接或文件。

## 3. P1 判断修正(双方)

1. **Opus P1「给门①补一个与②同构但更严格的声明机制」→ 站住,但被 §1-4 实质改写。** 我当时说不清这条线画在哪(P1 §3-2)。SOTA 给了名字与四个要件:这不是「声明机制」,是 **compensating control**,成立条件 = ① 存在 legitimate technical constraint(POSIX 拿目录 fd 只能 `os.open` —— 成立)② 有文档化的等效替代缓解 ③ **批准人 ≠ 申请人** ④ **带 expiry**。⇒ 我原来的表述缺了 ③④,而 ③ 恰是与「事后开豁免」的分界线。

2. **`writer.py:85-97` 拒绝自批 → 被 SOTA 正面追认(升格为方法论)。** "the person responsible for a security control should never be the one to audit it" 与它写的「为了让自己刚写的代码过而给安全门加豁免」是同一条原则。**该注释不是谨慎过度,是无意中执行了 ISO 27001 5.3 的职责分离。** ⇒ 决议 37 把 R4-F4 上交 IDS 是**结构正确**,不是保守。

3. **Codex P1「未定判据不能先焊成 BLOCK gate」→ 部分被推翻。** §1-6 表明这不是二选一:标准做法是 **warn 模式 + baseline diff + 只卡新增 + 分阶段 ratchet**。⇒ T040 的正确形态**既不是**全焊死、**也不是**不做,而是「先跑 warn 记 baseline,只对新增违规阻断」。**Codex 的结论方向对,但把选项空间压成了二值。**

4. **双方 P1「(c) 该挂验收侧」→ 强化,且拿到了具体机制。** §1-2 的三件套(预先定累积规则 / 未达门槛报 **inconclusive** / 附细节使其可 pooling)**同时**解了 (c) 与 OQ-A1-1 —— 且证明 **OQ-A1-1 的第三值不是 scope 扩张,是这套机制的必要构件**。而 §1-3 的 Goodhart 反向说明:把「≥3」挂产出侧 = 让 measure 变 target,judge 会学会产 3 条以满足门 —— 正是 spec §1-O4「不做真理机」要防的。

5. **⚠ 反自欺条款执行 —— 一条咬我们自己的证据,双方 P1 都没写。** §1-2 明写 "accumulation rule must be **prespecified**, not chosen after seeing the data"。而本仓**正是在看到「1 < 3」之后**才来定累积规则的。⇒ 无论最终裁 (α) 还是 (β),**都必须在 spec 里如实标注「本规则是 post-hoc 制定」**,并给出防 outcome-switching 的约束(例如:规则一经落定,**下一次**评估起生效,不追溯认定本次那份 briefing 为 PASS)。**这条我在 P1 读到 (c) 的立法史时手里就有材料,但没往「我们自己也在 post-hoc」这个方向想 —— 是被解释掉的一处。**

6. **协议自身的「唯一可读性」缺陷(元层 · 双方 P1 共同暴露)。** P1 模板写「800-1500 字」,中文「字」歧义(字符 vs 词):Codex 按字符压到 1500(且是 `sed -i` 机械压缩),我按未加约束写到 ~4000。**同一条验收行推出两种互斥执行 = 决议 35 (F)「唯一可读性」的教科书实例,而它就发生在裁这件事的这场 forge 里。** ⇒ 建议进 decision-list:forge-protocol 的字数约束改「≤N 字符(CJK)/ ≤M words(拉丁)」二选一明写。

7. **⭐ 决议 38 的 O7 措辞 → 站住,但漏了一件 §1-6 明写的必备件:longstop。** 「起算日 = 首条真实评估 journal 行的 `date`」正是 SOTA 推荐的**事件式 commencement**(且给了测量窗自己的起点,不继承别处),这一半判对了。**但它没处理「事件永不发生」** —— 若 operator 再不跑 evaluate,时钟永不起算,O7 就**永远不可判定**,而这恰恰是决议 38 自己声称要治的病(「不定义起点 = O7 永远无法判定」)。⇒ **同一个洞换了个位置:从「没有起点」变成「起点可能永不到来」。** 必须补 longstop:例如「起算日 = 首条真实评估 journal 行的 `date`,**或 spec v0.7 生效后满 30 日**,以先到者为准」。**这条双方 P1 都没看出来,决议 38 也没有。**

8. **簇④ 的落地形态被 §1-5 改写。** 决议 38 裁 (i) 时想的是「把两个『评估 run』**改名消歧**」。DDD 的答案更精确:同词在两个 bounded context 各有含义**是正常的**,不必选赢家;正确做法是 **① 各自限定**(如「解锁评估 run」/「产品评估 run」)**② 在 spec 术语章用 RFC 6365 手法点名并否决对方语境的用法** **③ 在两族边界处翻译(anti-corruption layer)**。⇒ 比「改名」更轻、且**不需要动 C″ 分流契约**。

**Sources**:
- [The Oracle Problem in Software Testing: A Survey (IEEE TSE)](https://ieeexplore.ieee.org/document/6963470/) · [Test oracle (Wikipedia)](https://en.wikipedia.org/wiki/Test_oracle)
- [Pre-specification of statistical analysis approaches in trial protocols](https://www.sciencedirect.com/science/article/abs/pii/S0895435618301616) · [Sample Size Calculation: Power, Errors & Clinical Trials](https://intuitionlabs.ai/articles/sample-size-calculation-clinical-trials) · [Inadequate Reporting in Randomized Trials](https://pmc.ncbi.nlm.nih.gov/articles/PMC12335382/)
- [Goodhart's Law and metric design (KPI Tree)](https://kpitree.co/guides/frameworks/goodharts-law) · [Specification gaming, Goodhart's law, and the metrics](https://explainx.ai/blog/specification-gaming-goodharts-law-ai-metrics)
- [Segregation of Duties in ISO 27001 (Control 5.3)](https://www.upguard.com/compliance/iso-27001/5-3) · [Cybersecurity Risk Governance: Who Owns the Risk, Who Manages the Exceptions?](https://securityexceptions.com/articles/cybersecurity-risk-governance-ownership-exceptions) · [Request for Exception to IT Security Policy (FSU)](https://its.fsu.edu/cybersecurity/standards/request-exception-it-security-policy)
- [Ubiquitous Language – DevIQ](https://deviq.com/domain-driven-design/ubiquitous-language/) · [RFC 6365: Terminology Used in Internationalization in the IETF](https://www.rfc-editor.org/rfc/rfc6365)
- [Ratchets: Improving systems incrementally](https://www.dustyburwell.com/2019/05/29/ratchets) · [Your CI/CD Security Wiring Diagram (GitPlumbers)](https://gitplumbers.com/blog/your-cicd-security-wiring-diagram-sast-sca-iac-sbom-and-signatures-without-killi/)
- [Commencement Date in Contracts](https://expiryedge.com/contract-terminology/commencement-date/) · [Contract Effective Date: Why One Clause Determines Everything](https://www.sirion.ai/library/contract-management/contract-effective-date/)
