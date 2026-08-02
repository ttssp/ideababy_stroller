# Forge Stage · 001 · v5 · "判据冻结前置一次裁死:ISO 29148 九特征 + 逐项本地化牙 + T040 warn 起跑"

**Generated**: 2026-08-02T23:10:00Z
**Source**: forge run v5 with X = 12 标的(IDS 4 件 + XenoDev worktree 8 件), Y = 架构设计 · 工程纪律 · 产品价值, Z = 对标 SOTA(判据可达性前置 / 挂产出侧还是验收侧 / 安全控制例外流程 / 术语同一性 / 测量窗起算点), W = verdict-only + decision-list + next-PRD
**Convergence mode**: strong-converge
**Rounds completed**: P1 (both), P2 (both), P3R1 (both), P3R2 (both) + Opus P3R2 §5「R2 后置接受」
**Searches run**: 28 次检索 + 1 次 WebFetch,覆盖约 23 个独立来源(Opus P2 7+1 · GPT P2 20 · Opus P3R1 1 条**验证性**复核)
**Moderator injections honored**: none(`forge/v5/moderator-notes.md` 不存在)
**Convergence outcome**: **converged**(双方 P3R2 §2 单一 verdict 对齐,**无 unresolved**;GPT 的 CONCERNS 指向落地前置,不是分歧)

> ⚠ **本文档正文约 5200 CJK 字符,超 synthesizer 质量栏的 4000 上限约 30%。** 未做机械压缩:
> 被砍的会是 12 项施工单里 item 2 / 10 / 12 的限定条件,而 GPT P3R2 §2 明写「任一被降级为
> 实施注记,联合 verdict 即降为 BLOCK」。⇒ 选择**具名超标**而非**有损压缩**——这正是本轮
> v0.2 note 3 要归 006 修的那条协议缺陷本身。

---

## How to read this

forge 是横切层(不是 L1-L4 pipeline 的一部分)。本文档是双专家(Opus 4.7 Max + GPT-5.5 xHigh)
独立审阅 + SOTA 对标 + 两轮联合收敛后的产出,**强制给出立场**。

本轮标的不是 12 个独立议题,而是**同一根轴的 12 次发作**:一条机器可判的验收判据被冻结成 gate
之后,才发现它判不了 / 判不稳 / 挂错了地方 / 有两种读法 / 指的不是同一个东西。v1–v4 四轮 forge
+ 38 条 hand-back 决议反复撞它,七次都是**真跑**(不是评审、不是推演)揭出来的。

读完后你应该:
- 知道 K 那四问(证什么 / 挂哪侧 / 谁写 / 什么词)的最终答案,以及它们**有现成国际标准**
- 知道 **T040 现在能不能起跑、按什么形态**(§"T040 起跑裁决" —— 本轮最实的验收)
- 拿到可直接交 spec-writer 的 **spec v0.6→v0.7 一次性 amendment 施工单**(12 项 · 每项 A + 判据 + 证不出则 B)
- 知道哪些证据是**跨模型对标推翻出来的**(§"Evidence map" 可逐条溯源)

---

## Verdict

**采 ISO/IEC/IEEE 29148 九特征作为「判据冻结前置」的分类框架,逐项本地化为可执行牙,12 项按其归位。**
K 的四问各有答案:**证什么** = 九特征(Feasible / Verifiable / Unambiguous / Complete);
**挂哪侧** = 九特征自带个体级/集合级二分 ⇒ §1-O2 (c) 是集合级属性被写成单 run 自足的个体级门,
改挂**集合验收侧**,产出侧**不给 judge 加下界**;**谁写** = 独立责任主体(批准人 ≠ 申请人);
**什么词** = bounded context 各自限定 + 术语章点名否决。

**但九特征只是分类,不是牙。** 自指链的终点不是「采标准即自动解除」,而是**「有资质者评审 + 真跑
证据」**——本地化表强制四列(对象/证据/责任人/fallback),**Feasible 栏不接受推演**。这是本仓
七次「推演≠真跑」的制度化收口。**T040 立即以 warn + versioned baseline + 只卡新增起跑。**

## T040 起跑裁决(K 写死的本轮最实验收)

> **能起跑。形态 = warn 模式 + versioned baseline + 只卡新增违规。**

- T040 的阻塞面**比想象中窄**:`depends_on:[T030,T031,T032]` 三者已 ship,6 个测文件里只有
  `test_o2_exemption_contract.py` 的 **1 条 (c) 断言**被阻(P1-Opus §1-B)。
- 其余 5 个文件按原计划建 block 测 + mutation 证 teeth;(c) 那条按 item 2 的新集合语义建。
- **正当性分两层如实标**(Opus 在分歧 1 让步后的最终表述):scoped verification(W3C / NASA /
  IEEE 29148 **标准条文**)**为主**;ratchet / baseline(**行业实践,非标准条文**)为**实施形态**。
- **焊的是 baseline,不是判据** —— 这正是「不给未定规则焊牙」与「现在就起跑」的兼容点。
- 验收必须额外证明:**存量违规只 warn、新增同类才 block**,否则就是「名为 ratchet、实为全量门」。

⚠ 起跑**前置**:R5 逐条裁决完成(见下)。T040 的 item 10/11 落点与 R5 相邻代码面重叠。

## Evidence map

| 结论 | 来源 | 引用(≤15 words) | 是否有反对证据 |
|---|---|---|---|
| 「gate 上线前先证其可满足」**有**正式先例(推翻 Opus P2 负结果) | P2-GPT §1 row1 → P3R1-Opus §1 独立复核 | "requirement 要抽成 assertion/test case,且 feasible/verifiable" | 已解决:Opus P2 §1「未检索到」为**未检索到**非无先例 |
| Verifiable 的标准定义即「存在一个过程能证明」 | P3R1-Opus §1(复核 ISO 29148) | "if and only if there exists a process that can prove" | - |
| 本仓「判据可达性族」= 九特征的重新发明(五例逐一映射) | P3R1-Opus §1 映射表 | "唯一可读性 → Unambiguous:allows only one interpretation" | - |
| OQ-A1-1 悬在 frozen spec 里本身违反 Complete | P3R1-Opus §3-2 | "完整集合 no TBD, TBS, or TBR clauses" | - |
| 九特征**不能**直接当 gate,不自动解除自指 | P3R1-GPT §3-5 → P3R2-Opus §1(全额让步) | "九特征是诊断分类,不是本仓可执行牙" | 反方(Opus P3R1 §4 打 ✅)**已撤回** |
| (c) 挂验收侧而非产出侧(双路同结论) | P2-Opus §1 row3 · P2-GPT §1 row3 | "样本充分性属验收设计";"separate the target from the measure" | - |
| 让 judge 凑 3 条 = 把 measure 变 target,违 §1-O4 | P2-Opus §3-4 · P2-GPT §1 row5 | "Goodhart 警告 proxy 过拟合" | - |
| judge 事实下界是 1 且 fail-loud,不是 0 | P1-Opus §1-B(读 judge.py) | "非稀疏叙事零有效判断 → raise 失败响亮" | - |
| 未达门槛的既定处置 = report inconclusive + 仍可 pooling | P2-Opus §1 row2(SPIRIT/预注册) | "报 inconclusive + 附样本细节使其仍可 pooling" | - |
| 累积规则必须 prespecified,本仓是 post-hoc ⇒ 不追溯 | P2-Opus §3-5(反自欺自陈) | "accumulation rule must be prespecified, not chosen after seeing data" | - |
| R4-F4 = compensating control,四要件(**双路独立同构**) | P2-Opus §1 row4(ISO 27001 5.3) · P2-GPT §1 row4(NIST RMF) | "requester ≠ approver";"风险接受由 authorizing official 负责" | **双方均未找到**支持「作者本地 allowlist 即合法例外」的材料 |
| `writer.py` 拒绝自批被追认为无意中执行职责分离 | P2-Opus §3-2 | "责任人不应是审计者" | - |
| O7 事件式起算漏了 longstop(决议 38 也没有) | P2-Opus §3-7 | "condition precedent 不成就则条款可能 void" | - |
| 词汇撞车正解是**各自限定**而非选赢家,不动 C″ | P2-Opus §1 row5(DDD + RFC 6365) | "different contexts can use the same word — and that's fine" | - |
| T040 窄起跑 = ratchet 标准做法,非「半个 gate」 | P2-Opus §1 row7 | "baseline diff:只对新增违规阻断" | ⚠ P2-GPT §4:"no strong direct source for 'half gate can ship'" ⇒ 已降级为两层表述 |

---

## Intake recap

### X · 审阅标的(12 件 · 全部 2026-08-02 实测可达)

**IDS 侧 4 件**:`HANDBACK-LOG.md`(793 行 · 38 条决议 SSOT)· 决议 37 源包
(`20260802T012127Z`)· 决议 38 源包(`20260802T073925Z`)· `PRD.md` v1.6(187 行)。

**XenoDev worktree 侧 8 件**(权威副本在 worktree,领先 main 70 commits):`spec.md` v0.6 `frozen`
(327 行 · 多数改动落点)· `tasks/T040.md`(被阻塞的 task)· `ephemeral.py`(C9 双门本体)·
`writer.py`(R4-F4 冲突写死在注释里)· `judge.py`(下界议题代码面)· `selfcheck_sequence.py`
(词汇撞车的门)· `cli/evaluate.py` · `journal/cli.py`(R5-F2 修法 · **未经 codex 复核**)。

### Y · 审阅视角
架构设计(判据挂点拓扑 · C9 双门边界 · 两族产物两条 provenance 链)· 工程纪律(冻结前置 ·
T040 建测形态 · 守卫冲突正当处置 · 反自欺条款)· 产品价值(O7 完成率 · 消毒转义可读性 ·
1 条判断的决策价值)。

### Z · 参照系
mode: **对标 SOTA**,五方向收窄(判据可达性前置 / 产出侧 vs 验收侧 / 安全控制例外流程 /
术语同一性 / 测量窗起算点);v1–v4 已做过的四个检索族**不重跑**。用户外部材料:**无**。

### W · 产出形态
verdict-only ✅ · decision-list(12 项逐条 · 作 spec v0.6→v0.7 amendment 施工单)✅ · next-PRD ✅
+ 额外交付「T040 起跑条件」✅(见上)。

### K · 用户判准(核心问题)
> 一条机器可判的验收判据,在被冻结成 gate 之前,**必须先证明什么、挂在哪一侧、由谁写、用什么词指称**?

要能执行的裁决不要正确的综述;可达性判据本身要可达(防自指);**v5 结束时 T040 若仍不能起跑,
这场 forge 没解决主要问题**。后悔值不对称:存疑偏向不放松,但**只挂着不给可达路径 = 没裁**。
强制每条裁决写成「A + 判据 + 证不出则 B」。

### 收敛模式
**strong-converge** —— 单一 verdict;残余分歧降级为 v0.2 note;每条裁决带 fallback 分支
(这不是保留分歧,是把「实证可能推翻」预先写进契约,由判据触发切换而非再起一轮 forge)。

---

## Verdict rationale(W = verdict-only)

**为什么采既有标准而不是继续自造术语。** 本仓在册五例——KG-43 数学不可达(0.70 > 上界 0.69756)/
T022 judge 无下界(结构不可达)/ unlock-preflight 吃活体 top-200(可达但不可复现)/ §7-P2 双读法
(缺唯一可读性)/ O7 缺起算点——自造术语让它们看起来像**五个偶发事故**。映射到 29148 之后,
它们是**同一族的同一种违反**。收益不在换名字,在于九特征自带的**个体级 vs 集合级**二分:
这一刀直接诊断出本轮最核心的那处挂错侧——**(c) 是集合级属性,却被写成每 run 必须自足的个体级门**。

**为什么标准仍然不是牙**(GPT 分歧 5 全胜,Opus 全额让步)。要判「(c) 是否 Feasible」,得先知道
judge 能不能产 3 条,**而那正是只有真跑才知道的经验问题**。九特征**命名**了要证什么,没有**替你证**。
自指链的正确终点与 oracle 文献「人是最后的 oracle 来源,合法」同构——是**合法终点,不是自动解除**。
⇒ 本地化表强制四列,**Feasible 栏不接受推演,须真跑或历史证据**。

**为什么 (c) 改挂验收侧不是放松。** (c) 的立法初衷是防「全豁免空过」。改挂集合池后洞会从单 run
换到多 run,GPT P3R2 给了防线:**当前 run 至少 1 条非豁免且带证据的判断才可借池 PASS**,当前
全豁免 / 零有效判断一律 `INSUFFICIENT_EVIDENCE`,**旧池不得替它空过**。⇒ 换挂点不降门槛,且给了
可达路径(K 要的「只挂着不给路径 = 没裁」)。

**为什么 R4-F4 可以当场裁死。** 这是本轮**证据强度最高**的一条:Opus 走 ISO 27001 5.3 /
compensating control,GPT 走 NIST RMF authorizing official——**两个互不重叠的合规体系给出同构结论**,
且双方都**未找到**支持「作者本地 allowlist 即合法例外」的材料。`writer.py:85-97` 拒绝自批,
被追认为**无意中执行了职责分离**;决议 37 把 R4-F4 上交 IDS 是**结构正确**,不是保守。

**本 verdict 的可证伪点(采 GPT 改进版)**:warn 候选过 `review_by` 后**无证据仍被续期** →
说明九特征本地化表退化成 warn 模式的橡皮图章 → **触发 v6**。(比 Opus 原提的「Feasible 几乎总是
证不出」**更早、更可测**。)

---

## Decision list · spec v0.6 → v0.7 一次性 amendment 施工单(W = decision-list)

### ⚠ 落地前置(表前 · 不可跳过)

**R5 逐条裁决完成** —— 对 codex R5 的每条 finding 标 **accepted / rejected / deferred**,并**映射到
下面 12 项**。理由:R5 四条修法**至今未经 codex 复核,IDS 也从未逐条裁决**(决议 37 只裁了「第 6 轮
何时跑」,没裁 R5 findings 本身),而 item 10/11 直接落在 R5 相关代码面(`journal/cli.py:172-187`
的 `lines[2]` 绑定 / R4-F4 相邻面)。**不先裁,12 项中有若干条建立在未裁决的地基上。**
(来源:P3R2-GPT §1 穷尽性检查 → P3R2-Opus §5 接受。)

### 12 项(以 P3R2-GPT §1 修订版为最终底稿)

| # | 项 | A(裁决) | 判据 | 证不出则 B(fallback) | 落点 |
|---|---|---|---|---|---|
| 1 | 通用前置 | spec 新增 **§0.1「判据冻结前置」**:拟冻结为 gate 的判据须填九特征本地化表(**对象 / 证据 / 责任人 / fallback** 四列);warn 候选**另填** `evidence_plan` / `review_by` / 升 block 条件 | 表填满 ∧ **Feasible 栏有真跑或历史证据(不收推演)**;**缺任一字段当场不通过** | Feasible 冻结前证不出 → 以 **shadow/warn 上线 + 记 baseline**;但**不得称已冻结 block gate**,**不得无证据自动续期**;首次过 `review_by` 仍无证据被续 warn → **触发 v6** | spec §0.1(新) |
| 2 | **§1-O2 (c)** | 改挂**集合验收侧**:池 = 跨 run 累积非豁免判断,**仅限同一 decision epoch 与 rubric**;epoch `closes_on` **预先固定、不得事后延长**;按「规范化 claim + direction」去重(同 claim 新 anchor 合并);抽样时 **anchor 必须仍有效**;**当前 run 至少 1 条非豁免且带证据的判断才可借池 PASS**;当前全豁免 / 零有效判断**一律 `INSUFFICIENT_EVIDENCE`,旧池不得替它空过** | 累积规则**预先**写死(池定义 / epoch / 去重 / 时效)∧ 明标 **post-hoc 制定 · 不追溯** | 方向被证不可比 → **拆池**,**而非**退回强迫单 run 产 3 条 | spec §1-O2 (c) · §6 O2 行 · §7-P2 |
| 3 | 唯一可读性 | 更名锚定 29148 **Unambiguous**;spec 加**术语章**,九特征作规范性引用 | 每条规范行用**稳定 requirement ID + 唯一 expected outcome**,验证命令 **1:1 引用同 ID**;语义歧义由**有资质者复核**(「不得推出两种实装」本身不可机器判,不作判据) | 某行天然需两种实装 → 不是 Unambiguous 违反,是**两个 bounded context**,转 item 11 | spec 术语章 · §6 表头注 |
| 4 | O7 起算点 | `start = min(first_journal_date, effective_date + 30d)`;**O7 截止 = start + 3 months**。本次首行已触发 ⇒ **2026-08-02 → 2026-11-02** | 机器可读;**禁把 longstop 的 30 日与 3 个月观察窗混写** | longstop 触发而仍无 journal 行 → O7 判 **FAIL(0/5)而非不可判**(时钟已起) | spec §1-O7 · §6 O7 行 |
| 5 | 用途分类 | 每条判据标 `usage: one-shot-gate \| recurring \| cumulative`(preflight=one-shot · O2=cumulative · C9=recurring) | 三类**穷尽互斥** ∧ 每条恰好一个标签 | 某判据跨两类 → **拆成两条**分别标,**禁一条兼任** | spec §1 各 O 行 |
| 6 | judge 下界 | **产出侧不加下界**;现状「非稀疏叙事零判断 fail-loud」= 下界 1,保留;产物侧只如实计数 | 产出数由证据决定;`renderer.py` 计数警示已在位 | ~~≥5 run~~ **删此无来源魔数**;改:**item 2 预先声明的首个 epoch 关闭时池仍 <3**,才起上游 provenance / anchor-map 任务,状态持续 `INSUFFICIENT_EVIDENCE`;**仍不**在 judge 加下界 | `judge.py` **零改动** + spec 注明理由 |
| 7 | OQ-A1-1 | **spec 语义层现在落**:非-PASS 细分 `INSUFFICIENT_EVIDENCE`(样本不足)vs `FAIL`(断链/违约);**CLI 退出码 + 状态字段协议留 T041**;**不追溯**把当前 briefing 判 PASS | OQ-A1-1 从 Open Questions **移除**(满足 Complete: no TBD/TBS/TBR) | 落语义层被证连带改 CLI 契约进而触 KG-B10 → 只落**文档语义**,产物侧沿用现有计数警示文本 | spec §1-O2 (c) · 删 OQ-A1-1 |
| 8 | **T040** | **立即起跑**,形态 = **warn + versioned baseline + 只卡新增**;6 个测文件中 5 个正常建 block 测,`test_o2_exemption_contract.py` 的 (c) 条按 item 2 新语义建 + mutation 证 teeth | `pytest tests/contract/ -q` 全绿 + 每条 mutation 的 red-green-log + **保存 baseline 版本** + **证明存量违规只 warn、新增同类才 block**(防「名为 ratchet 实为全量门」) | item 2 累积语义被证不可测(如池无持久化落点)→ 该条降 **warn-only 断言 + 记 baseline**,**不阻断**其余 5 文件 ship | `T040.md` · `tests/contract/` |
| 9 | 兜底举证 | spec 级规则:任何「本门可放行**因另一门会挡**」的论证,**须附另一门确实挡得住的可执行证据** | **必须有另一门实际转红的测试或 mutation 证据**(历史实例:C9 绕过 #1 判「可接受」的理由是 ②+⑤ 双红,而 #5 打掉了 ⑤ ⇒ 该判断已在无人知晓下失效) | 给不出可执行证据 → 按**无兜底**处理,**收紧本门** | spec §6 meta-note · T032 / T040 |
| 10 | **R4-F4** | 给门①建**与门②不同构**的 `COMPENSATING_CONTROLS` 表:① 合法技术约束陈述 ② 等效替代缓解 ③ **批准人 = operator(≠ 写码 agent)** ④ `expires_on` ⑤ **`review_by < expires_on`**。R4-F4 为首条,替代缓解 = 写后 verify + 失败删半成品 | 缺任一字段 → 门①仍红;**到 `review_by` 后 warn,到 expiry 后 fail closed(门①转红)**。⚠ **到期转红是风险接受到期的预期语义,不是缺陷**。NIST 不提供固定 N,提前量由 **operator 的 review SLA** 写入条目 | expiry 实装超 S → **只可**人工预警;**expiry 的机器转红不可省** | `ephemeral.py` 新表 · `writer.py` 补 dir fsync |
| 11 | 词汇撞车 | 裁 **(i)**;落地用 **DDD 限定词 + RFC 6365 手法**:「**解锁评估 run**」(reconstruct)/「**产品评估 run**」(evaluate),术语章**点名否决裸用**;并**命名 evaluate 自己那条 provenance 链**(RunProvenance + journal `lines[2]`);**不动 C″ 分流契约** | spec **规范性正文**中「评估 run」**裸用为 0**;**裸词扫描限规范性 spec,历史引文不计** | 波及面 >S(grep 命中过多)→ 先只在术语章 + §7-P2 + selfcheck 三处限定,其余加一次性脚注 | spec 术语章 + 全文 grep |
| 12 | **§5.6 可读性** | 起**独立 task**(本轮不修):**不是「反转义」,而是从规范存档生成上下文安全的展示投影**。定位 = **产品面风险**(O7 要 operator 每周真读 × PRD O1「信任第一块砖」),非渲染整洁 | operator 读一份产物**不需在脑内反转义** ∧ **恶意样本在目标上下文必须保持 inert** ∧ 可回指规范证据 | **证不出安全 → 展示版不 ship**,保留规范版并改善**非执行式**阅读辅助。⚠ **「不作证据用途」标签不能替代注入防御** | 新 task · PRD 风险段 |

### 四列矩阵归类

- **保留**:judge 现状(6)· **`selfcheck` 正向 allowlist**(它正确地拒绝了不属于它的产物族,不是 bug)·
  **C9 门② `DECLARED_READ_SITES` 声明机制** · **C″ 分流契约** · O7 机制与节奏
  ⚠ 后三条明写「保留」,**防落地时被误改**。
- **调整**:(c) 挂点(2)· O7 措辞加 longstop(4)· T040 形态(8)· 词汇限定(11)· 唯一可读性更名(3)
- **删除**:OQ-A1-1 作为 Open Question(7)· 「在 judge 加下界」这一候选(6)· 「给门①开豁免」三条坏路(10)·
  **`≥5 run` 无来源魔数**(6)· 「用『不作证据用途』标签解释注入风险」这条思路(12)
- **新增**:spec §0.1 判据冻结前置 + 九特征本地化表(1)· `usage:` 标签(5)· 兜底举证规则(9)·
  `COMPENSATING_CONTROLS` 表(10)· 术语章(3/11)· 展示投影 task(12)

### 耦合关系(哪些必须同批落)

- **同批(一次 amendment · 一次 codex review)**:1 / 2 / 3 / 5 / 6 / 7 / 9 / 11 —— 全落 spec 正文,
  且 2 与 7 语义互锁(第三值是累积机制的必要构件,不是 scope 扩张)。
- **可独立、但依赖上批语义**:8(T040)—— **不必等全部收敛即可 warn 起跑**,只需 item 2 的语义定稿。
- **代码面独立**:10(`ephemeral.py` / `writer.py`)· 12(新 task)—— 不阻塞 spec amendment。
- **全批前置**:R5 逐条裁决。

---

## Next-version PRD draft(W = next-PRD · PRD v1.6 → v1.7 修订方向)

**PRD 零骨架改动。Scope OUT 不改,O4 生效条款不改(v1.6 已生效,本轮零触碰)。** 只补三点:

```
# PRD · 001-radar-pA · v1.7(修订方向 · 待 human 批准)

**Status**: Draft from forge v5, awaiting human approval
**Sources**: stage-forge-001-v5.md · P3R2-GPT §4 · P3R2-Opus §4

## 修订 1 · Success O1 注记补 O7 时间锚
- 起算算法:start = min(首条真实评估 journal 行 date, spec v0.7 生效日 + 30 日)
- 本次:start = 2026-08-02,截止 = 2026-11-02(start + 3 months)
- longstop 触发而无 journal 行 → O7 判 FAIL(0/5),不判「不可判」
- (evidence: §"Evidence map" 第 13 行 · P2-Opus §3-7 longstop)

## 修订 2 · Biggest product risk 段新增一条
- **产物呈现面(消毒转义)是 O7 完成率的实质风险**,与差异化风险并列。
- 理由:O7 要 operator 每周真读一份、连做 5 次;PRD O1 是「信任第一块砖」;
  §5.6 实样显示叙事被转义成 `\*\*结构连接\*\*` 形态。
- ⚠ 修法**不是**反转义,是**上下文安全的展示投影**;证不出安全则展示版不 ship。
- (evidence: P1-Opus §1-C · P1-GPT §1-C · P3R2-GPT §1 item 12)

## 修订 3 · 判断数量的定位澄清
- 「≥3 条非豁免判断」是**集合验收采样口径**,**不是单次产出 KPI**。
- 显式 non-goal:不得为满足数量而让 judge 凑判断(违 O4「不做真理机」/ OUT-8)。
- (evidence: P2-GPT §1 row3/row5 Goodhart + SPIRIT · P2-Opus §3-4)

## Open questions(forge v5 也没解决的)
- 跨方向判断的长期可比性(见 v0.2 note 1)
- 强制多样本输出在其他评审系统是否有效(该面**未检索**,见 v0.2 note 4)
```

---

## 反自欺条款执行实绩(本仓方法论资产 · 如实记)

forge-config 的反自欺条款(承 009 forge v2「证据在场却被解释掉」先例)**本轮双向执行且有实绩**:

1. **GPT 自陈**(P2 §4):未检索「强制多样本输出是否在某些评审系统有效」。原句紧接着写「这不改变
   当前 verdict」——被 Opus P3R1 §3-4 点名为「自己识别出的缺口被同句话消解」。**GPT 已改为
   「结论在该面上不设防」。**
2. **Opus 自陈**(P2 §3-5):本仓是在看到「1 < 3」**之后**才定累积规则,而 SPIRIT 明写累积规则
   须 prespecified ⇒ **规则只对下一次评估生效,不追溯**。
3. **GPT 末轮又抓出 Opus 施工单里三处**(P3R2-Opus §5 逐条认领):
   - `≥5 run` 是**无来源魔数** —— 「本轮 forge 的主题正是判据的来源与可达性,而我在施工单里
     自己造了一个无来源阈值」。
   - item 3 **给 Unambiguous 写了一条自己不 Verifiable 的判据** —— 九特征在自己的施工单上的
     第一次实战检验,没通过。
   - item 12 用「不作证据用途」**标签解释掉了注入风险** —— 在同一轮里第二次犯同型错误。
4. **协议自身的自指实例**:P1 模板「800-1500 字」的中文「字」歧义,致 GPT 用 `sed` 机械压缩到
   1500、Opus 超标到 ~4000。**本轮要裁的 Unambiguous 缺陷,发生在裁它的这场 forge 的协议里。**
   ⚠ 归 `/expert-forge 006`,**不归本轮**。

⇒ **协议流程 note**:Opus P3R2 §5 是在对方 P3R2 落盘之后补写的。**协议无 P3R3**,§5 是 Opus
唯一的表态机会,内容是**全额接受对方修订**(「二者冲突处一律取对方版本」),已按此综合。

## v0.2 notes(残余分歧 · 不重开 verdict)

1. **累积池跨方向可比性** —— 首池达 3 条并抽样时复核;若三条来自不相干方向致 operator 无法作
   同一验收抽样 → 按 item 2 **拆池**。
2. **compensating control 的 expiry 实装代价** —— 超 S 只可人工预警;**机器转红不可省**。
   回头看时点:第二条 compensating control 条目出现时(一条可人工盯,两条起就该机器盯)。
3. **forge-protocol「字」歧义 → 归 `/expert-forge 006`**(不归本轮)。建议改「≤N CJK 字符 /
   ≤M words」双口径 + 「**宁可超标具名声明,禁有损机械压缩**」。**自指实例,值得单独记一笔。**
4. **强制多样本输出有效性面未检索** —— 首个 epoch 关闭后池仍 <3 再补该方向证据,
   **不事后改本 epoch 规则**。

---

## What this menu underweights(强制自批判)

- **反对证据未充分整合**:P2-GPT §4 明写 "no strong direct source for 'half gate can ship'"。
  主 verdict 仍让 T040 起跑,靠的是**降级表述**(scoped verification 是标准条文 / ratchet 是行业
  实践)。若 operator 认为「行业实践不足以支撑起跑」,item 8 应退回等 item 2 定稿后再动。
- **本轮最大增量来自一次纠错,不是来自共识**:Opus 的负结果被 GPT 推翻。这提示**单模型 forge
  会把「未检索到」当成「无先例」**——这条方法论教训比 12 项施工单本身更耐用。
- **回声室风险(第 6 次连续预警)**:v1/v2/v3 的裁决**没有一条是被「保留分歧」推翻的,全是被
  真跑推翻的**。本轮双方都同意的判断里,最可能被真跑打掉的是 **item 2 的可测性**(池的持久化
  落点从未有人验过)与 **item 12 的「上下文安全投影」是否真能证 inert**。fallback 已预置。
- **K 中未充分回应的项**:「1 条判断对 operator 到底还有没有决策价值」这个产品问题,双方最终
  只处理了**数量口径**(集合验收采样)与**呈现面**,**没有正面回答**「低置信单判断值不值得读」。
  P1-Opus §3-3 提出的事实问题(本次是否走了 `judge.py:118` 的 `not anchor_map` 退路)被
  P2-GPT 用 `evidence=(e9)` 排除了空锚退路,但「正常路径只返 1 条」的**归因仍未证实**。
- **Y 视角覆盖盲区**:Y 未含「安全」独立视角,但 item 12 的注入防御、item 10 的 compensating
  control 都是安全面判断,由工程纪律视角代管。若 operator 想要更强的安全审视,应在 v6 的 Y 里加。
- **X 标的覆盖局限**:R5 的四条修法**本身未进 X 的精读清单**(只在 X §12 提了一句「未经 codex
  复核」),这正是落地前置存在的原因。R5 裁决时若发现 finding 与 12 项冲突,**须回改施工单**。
- **forge versioning 提示**:触发 v6 的判据已写死 —— **warn 候选过 `review_by` 后无证据仍被续期**。
  另:若 item 2 的累积池实施后 O2 仍长期不可达,v0.2 note 4 那面需补检索再议。

---

## Decision menu(for human)

### [A] 接受 verdict,交 spec-writer 落 v0.6 → v0.7 一次性 amendment
```
执行顺序(不可颠倒):
1. R5 逐条裁决(accepted / rejected / deferred + 映射到 12 项)→ 写进 HANDBACK-LOG
2. spec-writer 消费本文档 §"Decision list" 12 项 → 一次 amendment(frontmatter
   amended_at_N + Amendment log + Version bump v0.6→v0.7)→ 走一次 codex review
3. T040 起跑(warn + versioned baseline + 只卡新增)
4. PRD v1.6→v1.7 三点修订(/scope-inject)
```
⚠ **item 2 / 10 / 12 必须采用本文档的修订版**。任一被降级为「实施注记」,联合 verdict
**即降为 BLOCK**(分别会重开「空过」/「隐藏例外到期」/「用标签解释安全风险」)。
⚠ 本文档 §"Next-version PRD draft" 是**修订方向**不是完整 PRD,不构成 `/plan-start` 的输入;
本轮不需要 fork 新 PRD branch。

### [B] 跑 forge v6(说明需要补什么)
```
/expert-forge 001
```
适用:R5 裁决后发现 findings 与 12 项冲突 / operator 认为 item 8 起跑证据不足 /
「1 条低置信判断的决策价值」需专门裁。**v5 整目录保留作历史参考。**

### [C] 局部接受
- ✅ 建议优先采纳:item 4(O7 longstop · 零争议 · 机器可读)· item 7(删 OQ-A1-1 · 解 Complete 违反)·
  item 10(双路独立同构 · 本轮证据最强)· item 5 / 9(纯新增规则,不动既有门)
- ⏸ 可挂起:item 12(独立 task · 不阻塞 amendment)· item 3 的术语章全量改造(可先三处限定)
- ❌ 不建议拆散:item 1 + 2 + 7(语义互锁,拆开落会重新制造 Complete 违反)

### [P] Park
```
/park 001
```
保留全部 forge 产物。⚠ 注意 park 会让 **O7 的 longstop 时钟继续走**(start 已定 2026-08-02,
截止 2026-11-02),到期无 journal 行则 O7 判 FAIL(0/5)——这是 item 4 的设计意图,不是缺陷。

### [Z] Abandon
```
/abandon 001
```
**本 verdict 不指向 abandon。** 它是「判据怎么冻结」的裁决,不是「要不要继续」;且 O7 首跑已
`decision_delta=true`,产品信号为正。仅当 operator 独立判定 radar 整体不做时才选此项。

---

## Forge log
(由 /expert-forge 命令更新;记录每次 forge run 的 v 序列 + 关键 verdict 一句话)

- v5: 2026-08-02 — verdict: "采 ISO/IEC/IEEE 29148 九特征作『判据冻结前置』分类框架 + 逐项本地化为可执行牙(对象/证据/责任人/fallback 四列 · **Feasible 栏不接受推演须真跑或历史证据**),12 项按其归位作 spec v0.6→v0.7 一次性 amendment 施工单;K 四问定案:证九特征 / (c) 从个体级门改挂**集合验收侧**(epoch+rubric 限定 · closes_on 不得延长 · claim+direction 去重 · anchor 抽样时须有效 · **当前 run 至少 1 条非豁免带证据判断才可借池 · 全豁免一律 INSUFFICIENT_EVIDENCE 旧池不得空过**)且**产出侧不给 judge 加下界**(Goodhart + 违 O4)/ 例外由**独立责任主体**批(R4-F4 = compensating control 四要件 + review_by<expires_on · **到期机器转红不可省** · ISO 27001 5.3 与 NIST RMF 双路独立同构)/ 词汇撞车按 DDD 限定词 + RFC 6365 点名否决处理**不动 C″**;OQ-A1-1 语义层现在落(INSUFFICIENT_EVIDENCE vs FAIL)协议留 T041 **不追溯**;O7 补 longstop(start=min(首条 journal date, 生效+30d) ⇒ 2026-08-02→2026-11-02,longstop 到而无 journal 行判 FAIL 非不可判);**T040 立即以 warn + versioned baseline + 只卡新增起跑**(须证存量只 warn/新增才 block);落地前置 = **R5 逐条裁决**;PRD 零骨架改动只补三点(O7 时间锚 / 呈现面是 O1 风险 / 判断数量是集合验收采样非单次 KPI)。**九特征只是分类不是牙,自指链终止于有资质者评审 + 真跑证据 = 合法终点非自动解除**;跨模型对标推翻 Opus『无先例』负结果 = 本轮最大单条价值;v6 触发判据 = warn 候选过 review_by 后无证据仍被续期。"
- v4: 2026-07-18 — verdict: "采 γ,以正式 amendment(非 waiver)落地:生效自证标的从『07-17 真产物』改写为『首个评估 run 产物』…(详见 v4 stage 文档)"
- v3: 2026-07-17 — verdict: "g1(人肉盲测二值签字)永久退役出解锁链;新 gate 形态 = 按 run 类型分流 + 两层 + 信号…(详见 v3 stage 文档)"
- v2: 2026-07-16 — verdict: "①② 从 T010/T011 解锁前置退役(采纳 KG-B9 · 循环依赖成立)…(详见 v2 stage 文档)"
- v1: 2026-07-16 — verdict: "P0.2 人肉盲测二值签字 gate 退役(采纳 KG-B8),T010/T011 改由机器可判三项解锁…(详见 v1 stage 文档)"
