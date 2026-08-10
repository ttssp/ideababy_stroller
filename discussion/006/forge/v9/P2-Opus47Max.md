# Forge v9 · 006 · P2 · Opus47Max · 参照系评估(with search)

**Timestamp**: 2026-08-10T09:20:00Z
**Searches run**: 4 次定向 `WebFetch`(**非检索** · 见 §0 故障声明),mode = 对标 SOTA
**Visibility**: 我已读对方 P1(`P1-GPT55xHigh.md`)。

## 0 · ⚠ Z 执行故障声明(必须先读,影响本文所有负结论的效力)

`WebSearch` 三次同错 400(`output_config.effort 'xhigh' is not supported when thinking is disabled`),
与 **forge 001 v6 完全相同的后端故障,这是第二次复发**。Z 因此退化为**对已知权威源的定向 `WebFetch`**,
**不是检索**。⇒ 本文**不产出任何「未检索到 ⇒ 无先例」型结论**;
Z 第 5 条方向(**code review 轮次与缺陷发现率的经验研究**,对应 XD-44)**未取到**
(Google MCR 论文页只回摘要,正文在 PDF)—— 记「**未取到**」,不是「不存在」。
**XD-44 的 SOTA 对标本轮由 Codex 侧单侧承担**,与 v6 的 CVE 面同型(单侧覆盖,无跨模型交叉)。

## 1 · SOTA 对标

| 标的 X' | 参照项 | 它怎么做 | 我们怎么做 | gap | Source |
|---|---|---|---|---|---|
| **XD-43 + KG-B11(该跑而未跑)** | **in-toto layout / link** | 步骤在 **layout 中预先声明**;每步带 `THRESHOLD` = "how many pieces of link metadata must be provided";不足即验证失败。`expected_materials` / `expected_products` 用 MATCH 规则把该步**绑到具体内容 hash** | 无预期清单;消费点用「块在不在」当判据 | **缺一份独立于被检查对象的预声明步骤清单 + 内容绑定**。这正是双方 P1 各自到达的那个抽象,SOTA 里有成熟形态 | in-toto spec |
| **「缺席」的语义(K 第 3 条)** | **GitHub required status checks** | required check 必须取得 `successful` / `skipped` / `neutral` **状态**才能合入 ⇒ **「不适用」必须被显式报告成 `skipped`,不能靠沉默** | 沉默 = 不适用(`if grep -q` 不命中则整步跳过) | ⭐ **SOTA 把「缺席」转成一个必须主动申报的状态**。这是 K「要判『该带而未带』而不是『未带就拒』」的**成熟工业解**,而且不需要我们发明 | docs.github.com |
| **stale `approve/0`(安全)** | **GitHub dismiss stale reviews** | 批准**绑 diff**;新 commit 推入或 merge base 变动 ⇒ 批准**自动失效**,须重新评审 | `REVIEW-LOG.md` 至今对下游显示 v0.6 的 `approve / 0`(2026-07-26),内容早已变 | **批准未绑内容身份、无失效边** ⇒ stale 不是「旧」,是**反向正信号** | docs.github.com |
| **immutable review record(KG-B11 / post-P0 (b)(c))** | **Sigstore Rekor** | "immutable, tamper-resistant ledger";日志"remains append-only and entries are never mutated or removed";第三方可查 **inclusion proof 独立验证** | singleton 可被下轮覆盖;IDS 侧无独立复证面 | **可覆盖 + 无独立验证面** —— 恰是 `SHARED-CONTRACT:993` post-P0 (b)(c) 写的那两条,65 天没人接 | docs.sigstore.dev |
| ⚠ **反向 gap(限缩本轮野心)** | **SLSA v1.0 verifying-artifacts** | expectations 是**独立策略层**、绑 package name、"never the artifact autonomously";**但该规范并未规定 provenance 缺席时怎么办** | 我们容易期待「采一个标准就解决」 | ⭐ **采格式不解决本问题**。缺席语义必须由**我们自己的策略层**裁定,SOTA 不代劳;它给的是**期望层该独立存在**这一点,不是缺席判据本身 | slsa.dev |

paraphrase 为主,verbatim quote 均 ≤15 words。

## 2 · 用户外部材料消化

**n/a** —— `forge-config.md` §Z 明写「**外部材料叠加:无**」,K 中无外部链接/文本/文件。
本节不构造材料,亦不把 SOTA 结果冒充成 operator 提供的材料。

## 3 · 修正后的视角

- **P1-Opus §1「四条机制侧全都写对了,失效整齐落在执行面」→ 站住,但措辞被 SOTA 精确化。**
  in-toto 的对照说明:我们缺的**不是「执行」而是「预先声明的义务 + 内容绑定」**。
  「执行面」这个词太宽,会把修法引向「催人执行」;真正缺的是 **obligation 层**。⇒ 该框架保留,**改述**。
- **P1-Opus「需要一个独立于被检查对象自身的预期声明」→ 最强站住(三方支持)。**
  SLSA 明写 expectations 从不由 artifact 自定;in-toto 的 layout 由项目主签发而非由被验步骤提供。
  ⚠ 且 **P1-GPT 在未读我 P1 的情况下独立到达同一抽象**(「obligation 由权威工作流状态预先生成…
  证据只能关闭 obligation,不能反过来决定 obligation 是否存在」)⇒ **双侧独立 + SOTA 印证**,
  是本轮迄今唯一同时具备两者的判断。
- **P1-Opus / K 第 3 条「严格化(缺即 REJECT)会误拒合法老包」→ 被 SOTA 给出更好的第三条路。**
  不必在「拒」与「豁免」之间二选一:**要求显式申报**。GitHub 的 `skipped` / `neutral` 是
  「合法不适用」的**主动状态**,不是沉默。⇒「该带而未带」可以落成一条可判定的规则:
  **期望清单里有 ∧ 既无内容绑定的成功记录 ∧ 也无显式 skip 申报 ⇒ 拒**。
  这把 P1 的核心开放问题关掉了一半,且**不误拒老包**(老包不进期望清单,或申报 skip)。
- **P1-Opus §3-2「expectation 会不会无限递归、终止点是否必须是人」→ 部分被推翻。**
  in-toto 的终止点是**被签名的 layout**:**人签一次,机器执行 N 次**。
  ⇒ 递归在「谁签期望清单」处自然终止,且是**一次性人力**,不是每包一次人力。
  同一条也覆盖 **P1-GPT §3-2 的攻击面**(「若包类型由 producer 自报,攻击者可连类型一起省略」)
  —— layout 不由 producer 提供,自报路径根本不存在。
- **P1-GPT「通用机制无法自动发现任意未调用步骤,各入口仍须逐点接线」→ 站住,且是必须写进 verdict 的限缩。**
  in-toto 同样要求 layout **逐步枚举**。⇒ 本轮 verdict **不得承诺**「一条通用条款自动覆盖所有入口」;
  期望清单的**枚举完备性**本身会成为下一个缺席面(谁保证清单没漏一步)。
- **P1-Opus §2 对 XD-44 的 `defer` 判断 → 本轮未被检验。** Z 第 5 条未取到(见 §0)。
  ⚠ 我注意到 **P1-GPT 给了比我更进一步的方案**:不是纯 defer,而是「**先保留有界 hard-stop
  + 增加风险/协议类分档 + 结构化 finding 类别**」——「结构化 finding 类别」正是让语义重复判据
  从不可靠变可靠的**前置条件**。**我倾向让步**,但要求该让步在 P3 记为 `post-hoc-accepted`。
- ⚠ **回声室自检(K 第 6 条)**:我在 P1 请 Codex **优先证伪**「执行面」框架与「两簇」划分。
  Codex **独立到达了同一框架**(它未读我的 P1)。**这不是证伪测试通过,只是双侧独立到达。**
  整齐的风险仍在,且现在多了一层「双方都同意」的诱惑 —— 承 001 forge v6 的教训:
  **回声室在 P1 被隔离后会于 P2 以「事后同意」形式回归**。真正的证伪机会在 P3,不在这里。
  另:我 P1 §3-3 的 reframe(「XD-44 是 task 粒度问题不是轮次上限问题」)**Codex 完全未提** ——
  既未证实也未证伪,**不得按「无反对即通过」处理**(这正是本轮在审的那个错误)。
- **两侧独立同意接手 `SHARED-CONTRACT:993` post-P0 backlog**:我判「挂 65 天、(b)(c)(d) 与本批重叠」,
  Codex 独立判「它正是本批的 **consumer 侧根**」并补上我漏掉的**施工约束**
  (改 spine 须 bump `contract_version` + Changelog)。⇒ 接手无分歧,**范围以 Codex 的更严版本为准**。

**篇幅**:正文约 1400 CJK 字符,**具名超标声明**(模板 600-1100)。超标来源是 §0 故障声明
与 §3 的双侧独立/回声室自检两段 —— 二者均属**不可有损压缩**的诚实边界,不做压缩。
